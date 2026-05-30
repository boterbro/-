# ALVR fix: port 8082 already in use (WSAEADDRINUSE / error 10048)
# Run PowerShell as Administrator, then:
#   Set-ExecutionPolicy -Scope Process Bypass -Force
#   .\alvr-fix-port-8082.ps1

$ErrorActionPreference = "Continue"

Write-Host "=== ALVR port 8082 fix ===" -ForegroundColor Cyan
Write-Host ""

function Get-Port8082Owners {
    $connections = Get-NetTCPConnection -LocalPort 8082 -ErrorAction SilentlyContinue
    if (-not $connections) {
        $connections = netstat -ano | Select-String ":8082" | ForEach-Object {
            if ($_ -match '\s+(\d+)\s*$') {
                [PSCustomObject]@{
                    PID = [int]$Matches[1]
                    Raw = $_.Line.Trim()
                }
            }
        }
    } else {
        $connections | ForEach-Object {
            [PSCustomObject]@{
                PID = $_.OwningProcess
                Raw = "$($_.LocalAddress):$($_.LocalPort) -> $($_.RemoteAddress):$($_.RemotePort) state=$($_.State)"
            }
        }
    }
}

Write-Host "[1/4] Processes using port 8082:" -ForegroundColor Yellow
$owners = @(Get-Port8082Owners)
if ($owners.Count -eq 0) {
    Write-Host "  Port 8082 is free (or in TIME_WAIT — reboot may help)." -ForegroundColor Green
} else {
    $owners | ForEach-Object {
        $proc = Get-Process -Id $_.PID -ErrorAction SilentlyContinue
        $name = if ($proc) { $proc.ProcessName } else { "unknown" }
        Write-Host "  PID $($_.PID) ($name) — $($_.Raw)"
    }
}

Write-Host ""
Write-Host "[2/4] Stopping ALVR / SteamVR processes..." -ForegroundColor Yellow
$targets = @(
    "alvr", "ALVR", "vrserver", "vrmonitor", "vrcompositor",
    "vrstartup", "vrwebhelper", "vrdashboard", "steamvr"
)
foreach ($name in $targets) {
    Get-Process -Name $name -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "  Stopping $($_.ProcessName) (PID $($_.Id))..."
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
    }
}

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "[3/4] Force-killing remaining PIDs on port 8082..." -ForegroundColor Yellow
$owners = @(Get-Port8082Owners)
foreach ($o in $owners) {
    Write-Host "  taskkill /F /PID $($o.PID)"
    taskkill /F /PID $o.PID 2>$null
}

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "[4/4] Final check:" -ForegroundColor Yellow
$remaining = @(Get-Port8082Owners)
if ($remaining.Count -eq 0) {
    Write-Host "  OK — port 8082 is free. Start ALVR Dashboard now." -ForegroundColor Green
} else {
    Write-Host "  Port still busy. Reboot PC, then run this script again." -ForegroundColor Red
    $remaining | ForEach-Object { Write-Host "    PID $($_.PID)" }
}

Write-Host ""
Write-Host "If ALVR still crashes after this:" -ForegroundColor Cyan
Write-Host "  1. Close Steam completely"
Write-Host "  2. Open ALVR -> Installation -> Remove driver"
Write-Host "  3. Start Steam -> ALVR -> Register driver -> Launch SteamVR"
Write-Host "  3b. Or delete settings.json in ALVR folder and re-pair Quest"
Write-Host ""
