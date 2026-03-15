# 建议通过 powershell -ExecutionPolicy Bypass -File 脚本/初始化环境.ps1 调用
$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot
$cliPath = Join-Path $PSScriptRoot "cli.py"

Write-Host "== Init Obsidian Harness ==" -ForegroundColor Cyan
python $cliPath init
Write-Host ""
Write-Host "== Current Status ==" -ForegroundColor Cyan
python $cliPath status
