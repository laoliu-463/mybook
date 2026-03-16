[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$TaskName = "ObsidianHarnessAutoRun",
    [int]$IntervalMinutes = 30
)

$ErrorActionPreference = "Stop"

if ($IntervalMinutes -lt 1) {
    throw "IntervalMinutes must be >= 1."
}

$projectRoot = Split-Path -Parent $PSScriptRoot
$pythonExe = (Get-Command python -ErrorAction Stop).Source
$schtasksExe = Join-Path $env:SystemRoot "System32\schtasks.exe"
$schedulerScript = Join-Path $projectRoot "autorun_scheduler.py"

if (-not (Test-Path $schtasksExe)) {
    throw "schtasks.exe not found: $schtasksExe"
}

if (-not (Test-Path $schedulerScript)) {
    throw "Scheduler script not found: $schedulerScript"
}

$startBoundary = (Get-Date).AddMinutes(1).ToString("HH:mm")
$taskCommand = "`"$pythonExe`" `"$schedulerScript`" --once"

$arguments = @(
    "/Create",
    "/SC", "MINUTE",
    "/MO", $IntervalMinutes.ToString(),
    "/ST", $startBoundary,
    "/TN", $TaskName,
    "/TR", $taskCommand,
    "/F"
)

$preview = @(
    "TaskName: $TaskName",
    "Python: $pythonExe",
    "Script: $schedulerScript",
    "StartTime: $startBoundary",
    "IntervalMinutes: $IntervalMinutes",
    "Command: $schtasksExe $($arguments -join ' ')"
)

if (-not $PSCmdlet.ShouldProcess($TaskName, "Register scheduled task")) {
    $preview | ForEach-Object { Write-Host $_ }
    return
}

& $schtasksExe @arguments
if ($LASTEXITCODE -ne 0) {
    throw "schtasks.exe failed with exit code $LASTEXITCODE. The script is valid, but this environment could not create a scheduled task."
}

$preview | ForEach-Object { Write-Host $_ }
Write-Host "Scheduled task registered successfully."
