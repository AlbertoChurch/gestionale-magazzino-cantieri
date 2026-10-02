# Da lanciare tu, in visita/da remoto, per portare il PC del cliente
# all'ultima versione. Non tocca mai gestionale.db (escluso da git).
#
# Uso:
#   cd C:\Gestionale
#   powershell -ExecutionPolicy Bypass -File deploy\aggiorna.ps1

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot

Write-Host "--- Fermo il server ---"
Stop-ScheduledTask -TaskName "GestionaleMagazzino" -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "$root*" } | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host "--- Scarico l'ultima versione ---"
git -C $root pull

Write-Host "--- Aggiorno le dipendenze ---"
& "$root\venv\Scripts\pip.exe" install -r "$root\requirements.txt"

Write-Host "--- Riavvio il server ---"
Start-ScheduledTask -TaskName "GestionaleMagazzino"

Write-Host ""
Write-Host "Fatto. Verifica su http://127.0.0.1:8000" -ForegroundColor Green
