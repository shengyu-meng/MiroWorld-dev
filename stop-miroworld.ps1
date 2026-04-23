$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$runtimeDir = Join-Path $root 'logs\local-dev'
$pidFiles = @(
  @{ Name = 'API'; Path = (Join-Path $runtimeDir 'api.pid'); Port = 8000 },
  @{ Name = 'Web'; Path = (Join-Path $runtimeDir 'web.pid'); Port = 4173 }
)

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

function Stop-TrackedProcess {
  param([string]$Name, [string]$PidFile, [int]$Port)

  if (-not (Test-Path $PidFile)) {
    $listener = Get-ListeningProcessInfo -Port $Port
    $shouldStop = $false

    if ($Name -eq 'API') {
      $shouldStop = Test-IsMiroWorldApiProcess $listener
    } elseif ($Name -eq 'Web') {
      $shouldStop = Test-IsMiroWorldWebProcess $listener
    }

    if ($shouldStop) {
      & taskkill.exe /PID $listener.ProcessId /T /F | Out-Null
      Write-Host "$Name stopped via port listener (PID $($listener.ProcessId))." -ForegroundColor Green
    } else {
      Write-Host "$Name is not tracked as running."
    }
    return
  }

  $rawPid = Get-Content $PidFile | Select-Object -First 1
  if (-not $rawPid) {
    Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
    Write-Host "$Name pid file was empty and has been cleared."
    return
  }

  try {
    $process = Get-Process -Id ([int]$rawPid) -ErrorAction Stop
    & taskkill.exe /PID $process.Id /T /F | Out-Null
    Write-Host "$Name stopped (PID $($process.Id))." -ForegroundColor Green
  } catch {
    $listener = Get-ListeningProcessInfo -Port $Port
    $shouldStop = $false

    if ($Name -eq 'API') {
      $shouldStop = Test-IsMiroWorldApiProcess $listener
    } elseif ($Name -eq 'Web') {
      $shouldStop = Test-IsMiroWorldWebProcess $listener
    }

    if ($shouldStop) {
      & taskkill.exe /PID $listener.ProcessId /T /F | Out-Null
      Write-Host "$Name stopped via port listener (PID $($listener.ProcessId))." -ForegroundColor Green
    } else {
      Write-Host "$Name process was already gone." -ForegroundColor DarkYellow
    }
  } finally {
    Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
  }
}

foreach ($pidFile in $pidFiles) {
  Stop-TrackedProcess -Name $pidFile.Name -PidFile $pidFile.Path -Port $pidFile.Port
}

Write-Host "Done. Logs remain in $runtimeDir"
