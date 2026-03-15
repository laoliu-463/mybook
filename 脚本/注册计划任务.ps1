param(
    [string]$TaskName = "ObsidianHarnessAutoRun",
    [int]$IntervalMinutes = 30
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$pythonExe = (Get-Command python).Source
$schedulerScript = Join-Path $projectRoot "脚本\自动调度器.py"

if (-not (Test-Path $schedulerScript)) {
    throw "未找到自动调度器脚本: $schedulerScript"
}

$action = New-ScheduledTaskAction -Execute $pythonExe -Argument "`"$schedulerScript`" --once" -WorkingDirectory $projectRoot

$baseTrigger = New-ScheduledTaskTrigger -Once -At (Get-Date).Date.AddMinutes(1)
$baseTrigger.Repetition = (New-ScheduledTaskTrigger -Once -At (Get-Date).Date.AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes $IntervalMinutes) -RepetitionDuration ([TimeSpan]::MaxValue)).Repetition

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $baseTrigger -Settings $settings -Description "定时运行 Obsidian Harness 自动调度器" -Force | Out-Null

Write-Host "已注册计划任务: $TaskName" -ForegroundColor Green
Write-Host "Python: $pythonExe"
Write-Host "脚本: $schedulerScript --once"
Write-Host "间隔: $IntervalMinutes 分钟"
