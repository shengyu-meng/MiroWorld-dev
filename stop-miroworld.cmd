@echo off
setlocal
powershell.exe -ExecutionPolicy Bypass -File "%~dp0stop-miroworld.ps1" %*
if errorlevel 1 (
  echo.
  echo MiroWorld-dev stop script failed.
  pause
  exit /b %errorlevel%
)
endlocal
