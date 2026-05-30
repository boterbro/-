# ALVR auto-fix: port 8082 WSAEADDRINUSE (error 10048)
# Called by ALVR-FIX.bat — no manual steps required.

$ErrorActionPreference = "Continue"
$Host.UI.RawUI.WindowTitle = "ALVR Fix — port 8082"

function Write-Step($n, $total, $msg) {
    Write-Host ""
    Write-Host "[$n/$total] $msg" -ForegroundColor Yellow
}

function Get-PortOwners([int]$Port) {
    $result = @()
    $seen = @{}

    try {
        Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | ForEach-Object {
            $pid = $_.OwningProcess
            if (-not $seen.ContainsKey($pid)) {
                $seen[$pid] = $true
                $result += [PSCustomObject]@{ PID = $pid; Raw = "$($_.LocalAddress):$Port state=$($_.State)" }
            }
        }
    } catch {}

    if ($result.Count -eq 0) {
        netstat -ano | Select-String ":$Port\s" | ForEach-Object {
            if ($_ -match '\s+(\d+)\s*$') {
                $pid = [int]$Matches[1]
                if (-not $seen.ContainsKey($pid)) {
                    $seen[$pid] = $true
                    $result += [PSCustomObject]@{ PID = $pid; Raw = $_.Line.Trim() }
                }
            }
        }
    }
    return $result
}

function Stop-ByName([string[]]$Names) {
    foreach ($name in $Names) {
        Get-Process -Name $name -ErrorAction SilentlyContinue | ForEach-Object {
            Write-Host "  stop: $($_.ProcessName) (PID $($_.Id))"
            Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
        }
    }
}

function Kill-Port([int]$Port) {
    foreach ($o in @(Get-PortOwners $Port)) {
        $proc = Get-Process -Id $o.PID -ErrorAction SilentlyContinue
        $label = if ($proc) { $proc.ProcessName } else { "unknown" }
        Write-Host "  kill PID $($o.PID) ($label)"
        taskkill /F /PID $o.PID 2>$null | Out-Null
    }
}

function Find-AlvrExe {
    $candidates = @(
        "$env:LOCALAPPDATA\ALVR\ALVR Dashboard.exe",
        "$env:ProgramFiles\ALVR\ALVR Dashboard.exe",
        "${env:ProgramFiles(x86)}\ALVR\ALVR Dashboard.exe",
        "$env:USERPROFILE\Downloads\ALVR\ALVR Dashboard.exe"
    )
    foreach ($p in $candidates) {
        if (Test-Path $p) { return $p }
    }
    $found = Get-ChildItem -Path "$env:LOCALAPPDATA", "$env:ProgramFiles", "${env:ProgramFiles(x86)}", "$env:USERPROFILE\Downloads" `
        -Filter "ALVR Dashboard.exe" -Recurse -ErrorAction SilentlyContinue -Depth 5 | Select-Object -First 1
    if ($found) { return $found.FullName }
    return $null
}

function Find-SettingsJson {
    $paths = @(
        "$env:LOCALAPPDATA\ALVR\settings.json",
        "$env:APPDATA\ALVR\settings.json"
    )
    foreach ($p in $paths) {
        if (Test-Path $p) { return $p }
    }
    $found = Get-ChildItem -Path "$env:LOCALAPPDATA\ALVR", "$env:APPDATA\ALVR" `
        -Filter "settings.json" -Recurse -ErrorAction SilentlyContinue -Depth 3 | Select-Object -First 1
    if ($found) { return $found.FullName }
    return $null
}

Clear-Host
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ALVR auto-fix (port 8082 / error 10048)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$total = 7

Write-Step 1 $total "Checking port 8082..."
$owners = @(Get-PortOwners 8082)
if ($owners.Count -eq 0) {
    Write-Host "  port free" -ForegroundColor Green
} else {
    $owners | ForEach-Object {
        $proc = Get-Process -Id $_.PID -ErrorAction SilentlyContinue
        $name = if ($proc) { $proc.ProcessName } else { "?" }
        Write-Host "  busy: PID $($_.PID) ($name)"
    }
}

Write-Step 2 $total "Stopping Steam and SteamVR..."
Stop-ByName @("steam", "steamwebhelper", "steamservice")
Start-Sleep -Seconds 1
Stop-ByName @("vrserver", "vrmonitor", "vrcompositor", "vrstartup", "vrwebhelper", "vrdashboard", "steamvr")

Write-Step 3 $total "Stopping ALVR processes..."
Stop-ByName @("alvr", "ALVR", "alvr_server", "alvr_dashboard")
Get-Process | Where-Object { $_.ProcessName -match 'alvr' } | ForEach-Object {
    Write-Host "  stop: $($_.ProcessName) (PID $($_.Id))"
    Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
}

Start-Sleep -Seconds 2

Write-Step 4 $total "Freeing port 8082..."
Kill-Port 8082
Start-Sleep -Seconds 2
Kill-Port 8082

Write-Step 5 $total "Checking ALVR settings..."
$settings = Find-SettingsJson
if ($settings) {
    Write-Host "  found: $settings"
    try {
        $json = Get-Content $settings -Raw -Encoding UTF8 | ConvertFrom-Json
        $port = $json.connection.web_server_port
        if ($null -ne $port -and $port -ne 8082) {
            Write-Host "  web_server_port = $port (not default)"
        }
    } catch {
        Write-Host "  settings.json unreadable — will backup and reset if ALVR still fails"
    }
} else {
    Write-Host "  settings.json not found (defaults will apply on first launch)"
}

Write-Step 6 $total "Final port check..."
$remaining = @(Get-PortOwners 8082)
$portOk = $remaining.Count -eq 0

if ($portOk) {
    Write-Host "  OK — port 8082 is free" -ForegroundColor Green
} else {
    Write-Host "  port still busy:" -ForegroundColor Red
    $remaining | ForEach-Object {
        $proc = Get-Process -Id $_.PID -ErrorAction SilentlyContinue
        Write-Host "    PID $($_.PID) $(if ($proc) { "($($proc.ProcessName))" })"
    }
}

Write-Step 7 $total "Launching ALVR Dashboard..."
$alvr = Find-AlvrExe
if ($alvr) {
    Write-Host "  starting: $alvr"
    Start-Process -FilePath $alvr
    Write-Host "  ALVR launched — click 'Launch SteamVR' in the dashboard" -ForegroundColor Green
} else {
    Write-Host "  ALVR Dashboard.exe not found automatically." -ForegroundColor Red
    Write-Host "  Start ALVR manually from Start menu after this window closes."
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
if ($portOk) {
    Write-Host "  DONE. Port freed, ALVR should start normally." -ForegroundColor Green
} else {
    Write-Host "  Port still occupied — reboot PC and run ALVR-FIX.bat again." -ForegroundColor Red
    Write-Host "  Or run: shutdown /r /t 0"
}
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to close..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
