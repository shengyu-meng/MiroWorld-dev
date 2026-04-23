@echo off
setlocal
powershell.exe -ExecutionPolicy Bypass -File "%~dp0start-miroworld.ps1" %*
if errorlevel 1 (
  echo.
  echo MiroWorld-dev startup failed.
  pause
  exit /b %errorlevel%
)
endlocal
