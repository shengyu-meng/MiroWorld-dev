param(
  [switch]$NoBrowser,
  [switch]$SkipInstall
)

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$runtimeDir = Join-Path $root 'logs\local-dev'
$envFile = Join-Path $root '.env'
$envExample = Join-Path $root '.env.example'
$venvDir = Join-Path $root '.venv'
$venvPython = Join-Path $venvDir 'Scripts\python.exe'
$webRoot = Join-Path $root 'apps\web'
$viteScript = Join-Path $root 'node_modules\vite\bin\vite.js'
$apiPidFile = Join-Path $runtimeDir 'api.pid'
$webPidFile = Join-Path $runtimeDir 'web.pid'
$apiOutLog = Join-Path $runtimeDir 'api.out.log'
$apiErrLog = Join-Path $runtimeDir 'api.err.log'
$webOutLog = Join-Path $runtimeDir 'web.out.log'
$webErrLog = Join-Path $runtimeDir 'web.err.log'
$apiUrl = 'http://127.0.0.1:8000/health'
$webUrl = 'http://127.0.0.1:4173'

function Write-Step {
  param([string]$Message)
  Write-Host "`n==> $Message" -ForegroundColor Cyan
}

function Find-CommandPath {
  param([string[]]$Names)
  foreach ($name in $Names) {
    $command = Get-Command $name -ErrorAction SilentlyContinue
    if ($command) {
      return $command.Source
    }
  }
  return $null
}

function Invoke-Native {
  param(
    [string]$FilePath,
    [string[]]$Arguments,
    [string]$WorkingDirectory = $root
  )

  Push-Location $WorkingDirectory
  try {
    & $FilePath @Arguments
    if ($LASTEXITCODE -ne 0) {
      throw ("Command failed with exit code {0}: {1} {2}" -f $LASTEXITCODE, $FilePath, ($Arguments -join ' '))
    }
  } finally {
    Pop-Location
  }
}

function Get-TrackedProcess {
  param([string]$PidFile)
  if (-not (Test-Path $PidFile)) {
    return $null
  }

  $rawPid = Get-Content $PidFile | Select-Object -First 1
  if (-not $rawPid) {
    Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
    return $null
  }

  try {
    return Get-Process -Id ([int]$rawPid) -ErrorAction Stop
  } catch {
    Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
    return $null
  }
}

function Wait-ForUrl {
  param(
    [string]$Url,
    [string]$Name,
    [int]$TimeoutSeconds = 90
  )

  $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
  while ((Get-Date) -lt $deadline) {
    try {
      $response = Invoke-WebRequest -UseBasicParsing -Uri $Url -TimeoutSec 5
      if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) {
        Write-Host "$Name is ready: $Url" -ForegroundColor Green
        return
      }
    } catch {
      Start-Sleep -Milliseconds 800
    }
  }

  throw "$Name did not become ready within $TimeoutSeconds seconds."
}

function Show-RecentLog {
  param([string]$Label, [string]$Path)
  if (Test-Path $Path) {
    Write-Host "`n--- $Label ($Path) ---" -ForegroundColor Yellow
    Get-Content $Path -Tail 40
  }
}

function Stop-ProcessTree {
  param([int]$ProcessId)
  & taskkill.exe /PID $ProcessId /T /F | Out-Null
}

function Get-ListeningProcessInfo {
  param([int]$Port)

  $connection = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue | Select-Object -First 1
  if (-not $connection) {
    return $null
  }

  $processInfo = Get-CimInstance Win32_Process -Filter "ProcessId = $($connection.OwningProcess)" -ErrorAction SilentlyContinue
  if (-not $processInfo) {
    return $null
  }

  return [pscustomobject]@{
    ProcessId = $processInfo.ProcessId
    Name = $processInfo.Name
    ExecutablePath = $processInfo.ExecutablePath
    CommandLine = $processInfo.CommandLine
  }
}

function Test-IsMiroWorldApiProcess {
  param($ProcessInfo)

  if (-not $ProcessInfo) {
    return $false
  }

  $details = "$($ProcessInfo.ExecutablePath) $($ProcessInfo.CommandLine)"
  return $details -match 'uvicorn' -and $details -match 'main:app' -and $details -match 'apps/api/src'
}

function Test-IsMiroWorldWebProcess {
  param($ProcessInfo)

  if (-not $ProcessInfo) {
    return $false
  }

  $details = "$($ProcessInfo.ExecutablePath) $($ProcessInfo.CommandLine)"
  return $details -match 'vite\.js' -and $details -match [regex]::Escape($root)
}

New-Item -ItemType Directory -Force -Path $runtimeDir | Out-Null
Set-Location $root

$npmCmd = Find-CommandPath @('npm.cmd', 'npm')
$pythonCmd = Find-CommandPath @('python', 'py')
$nodeCmd = Find-CommandPath @('node.exe', 'node')

if (-not $npmCmd) {
  throw 'npm was not found. Install Node.js 20+ first.'
}

if (-not $pythonCmd) {
  throw 'python was not found. Install Python 3.11+ first.'
}

if (-not $nodeCmd) {
  throw 'node was not found. Install Node.js 20+ first.'
}

if (-not (Test-Path $envFile) -and (Test-Path $envExample)) {
  Write-Step 'Creating local .env from .env.example'
  Copy-Item $envExample $envFile
  Write-Host 'Created .env. You can add your MiniMax key there later. The app can still start without it.' -ForegroundColor Yellow
}

if (-not $SkipInstall) {
  $nodeModulesDir = Join-Path $root 'node_modules'
  $packageLock = Join-Path $root 'package-lock.json'
  $needsNodeInstall = -not (Test-Path $nodeModulesDir)

  if (-not $needsNodeInstall -and (Test-Path $packageLock)) {
    $needsNodeInstall = (Get-Item $packageLock).LastWriteTimeUtc -gt (Get-Item $nodeModulesDir).LastWriteTimeUtc
  }

  if ($needsNodeInstall) {
    Write-Step 'Installing npm dependencies'
    Invoke-Native -FilePath $npmCmd -Arguments @('install')
  }

  if (-not (Test-Path $venvPython)) {
    Write-Step 'Creating local Python virtual environment'
    Invoke-Native -FilePath $pythonCmd -Arguments @('-m', 'venv', $venvDir)
  }

  $needsApiInstall = $true
  try {
    & $venvPython -c "import fastapi, uvicorn, httpx, pydantic, dotenv" | Out-Null
    $needsApiInstall = $false
  } catch {
    $needsApiInstall = $true
  }

  if ($needsApiInstall) {
    Write-Step 'Installing API dependencies into .venv'
    Invoke-Native -FilePath $venvPython -Arguments @('-m', 'pip', 'install', '--upgrade', 'pip')
    Invoke-Native -FilePath $venvPython -Arguments @('-m', 'pip', 'install', '-e', '.[dev]') -WorkingDirectory (Join-Path $root 'apps\api')
  }
} elseif (-not (Test-Path $venvPython)) {
  throw 'Missing .venv. Re-run without -SkipInstall once so the local Python environment can be created.'
}

$env:VITE_API_BASE_URL = 'http://127.0.0.1:8000'

$startedApi = $false
$startedWeb = $false
$apiProcess = $null
$webProcess = $null

try {
  $apiListener = Get-ListeningProcessInfo -Port 8000
  $apiProcess = Get-TrackedProcess $apiPidFile
  if ($apiListener -and -not (Test-IsMiroWorldApiProcess $apiListener)) {
    throw "Port 8000 is already used by PID $($apiListener.ProcessId) ($($apiListener.Name))."
  } elseif ($apiListener) {
    $apiProcess = Get-Process -Id $apiListener.ProcessId -ErrorAction SilentlyContinue
    Set-Content -Path $apiPidFile -Value $apiListener.ProcessId
    Write-Host "Detected existing MiroWorld API on port 8000 (PID $($apiListener.ProcessId))." -ForegroundColor DarkYellow
  } elseif ($apiProcess) {
    Write-Host "API already running with PID $($apiProcess.Id)." -ForegroundColor DarkYellow
  } else {
    Write-Step 'Starting API server'
    $apiProcess = Start-Process `
      -FilePath $venvPython `
      -ArgumentList '-m', 'uvicorn', '--app-dir', 'apps/api/src', 'main:app', '--host', '127.0.0.1', '--port', '8000' `
      -WorkingDirectory $root `
      -RedirectStandardOutput $apiOutLog `
      -RedirectStandardError $apiErrLog `
      -PassThru
    Set-Content -Path $apiPidFile -Value $apiProcess.Id
    $startedApi = $true
  }

  $webListener = Get-ListeningProcessInfo -Port 4173
  $webProcess = Get-TrackedProcess $webPidFile
  if ($webListener -and -not (Test-IsMiroWorldWebProcess $webListener)) {
    throw "Port 4173 is already used by PID $($webListener.ProcessId) ($($webListener.Name))."
  } elseif ($webListener) {
    $webProcess = Get-Process -Id $webListener.ProcessId -ErrorAction SilentlyContinue
    Set-Content -Path $webPidFile -Value $webListener.ProcessId
    Write-Host "Detected existing MiroWorld web app on port 4173 (PID $($webListener.ProcessId))." -ForegroundColor DarkYellow
  } elseif ($webProcess) {
    Write-Host "Web app already running with PID $($webProcess.Id)." -ForegroundColor DarkYellow
  } else {
    Write-Step 'Starting Vite web app'
    $webProcess = Start-Process `
      -FilePath $nodeCmd `
      -ArgumentList $viteScript, '--host', '127.0.0.1', '--port', '4173' `
      -WorkingDirectory $webRoot `
      -RedirectStandardOutput $webOutLog `
      -RedirectStandardError $webErrLog `
      -PassThru
    Set-Content -Path $webPidFile -Value $webProcess.Id
    $startedWeb = $true
  }

  Write-Step 'Waiting for services'
  Wait-ForUrl -Url $apiUrl -Name 'API'
  Wait-ForUrl -Url $webUrl -Name 'Web'

  & $venvPython -c "import fastapi, uvicorn, httpx, pydantic, dotenv" | Out-Null
  if ($LASTEXITCODE -ne 0) {
    throw 'Python dependencies are still incomplete inside .venv.'
  }

  if (-not $NoBrowser) {
    Write-Step 'Opening browser'
    Start-Process $webUrl | Out-Null
  }

  Write-Host "`nMiroWorld-dev is ready." -ForegroundColor Green
  Write-Host "Web: $webUrl"
  Write-Host "API: http://127.0.0.1:8000"
  Write-Host "Logs: $runtimeDir"
  Write-Host "Stop: .\stop-miroworld.cmd"
} catch {
  Write-Host "`nStartup failed: $($_.Exception.Message)" -ForegroundColor Red
  Show-RecentLog -Label 'API stderr' -Path $apiErrLog
  Show-RecentLog -Label 'Web stderr' -Path $webErrLog

  if ($startedApi -and $apiProcess) {
    Stop-ProcessTree -ProcessId $apiProcess.Id
    Remove-Item $apiPidFile -Force -ErrorAction SilentlyContinue
  }

  if ($startedWeb -and $webProcess) {
    Stop-ProcessTree -ProcessId $webProcess.Id
    Remove-Item $webPidFile -Force -ErrorAction SilentlyContinue
  }

  exit 1
}
