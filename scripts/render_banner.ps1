# Renders assets/src/banner.html to assets/banner.png (2x) with headless Edge.
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$src = Join-Path $root 'assets\src\banner.html'
$out = Join-Path $root 'assets\banner.png'
$profileDir = Join-Path $env:TEMP 'allanhert-banner-edge'
& $edge --headless=new --disable-gpu --hide-scrollbars --user-data-dir="$profileDir" `
  --force-device-scale-factor=2 --window-size=1280,320 --virtual-time-budget=4000 `
  --screenshot="$out" "file:///$($src -replace '\\','/')" | Out-Null
Write-Output "ok: $out"
