$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
python build_snapshot.py
Write-Host "Dashboard available at http://localhost:8000"
python -m http.server 8000
