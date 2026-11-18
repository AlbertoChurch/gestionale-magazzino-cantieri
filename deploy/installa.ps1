# Installazione della v0.1 su un PC nuovo. Va lanciato UNA volta,
# da PowerShell come Amministratore, con la cartella corrente sulla
# radice del progetto (quella appena clonata con git, es. C:\Gestionale).
#
# Uso:
#   cd C:\Gestionale
#   powershell -ExecutionPolicy Bypass -File deploy\installa.ps1

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot

if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)) {
    Write-Host "Rilancia PowerShell come Amministratore (serve per creare l'avvio automatico)." -ForegroundColor Red
    exit 1
}

Write-Host "--- Verifica prerequisiti ---"
foreach ($comando in "python", "git") {
    if (-not (Get-Command $comando -ErrorAction SilentlyContinue)) {
        Write-Host "'$comando' non trovato nel PATH. Installalo prima di continuare." -ForegroundColor Red
        exit 1
    }
}

Write-Host "--- Ambiente virtuale + dipendenze ---"
if (-not (Test-Path "$root\venv")) {
    python -m venv "$root\venv"
}
& "$root\venv\Scripts\pip.exe" install -r "$root\requirements.txt"

New-Item -ItemType Directory -Force -Path "$root\logs" | Out-Null

Write-Host "--- Primo utente amministratore ---"
$env:PYTHONPATH = $root
& "$root\venv\Scripts\python.exe" "$root\deploy\primo_admin.py"

Write-Host "--- Avvio automatico all'accesso a Windows ---"
$nomeTask = "GestionaleMagazzino"
Unregister-ScheduledTask -TaskName $nomeTask -Confirm:$false -ErrorAction SilentlyContinue
$azione = New-ScheduledTaskAction -Execute "wscript.exe" -Argument "`"$root\deploy\avvia_silenzioso.vbs`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1) -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName $nomeTask -Action $azione -Trigger $trigger -Settings $settings -Description "Avvia in background il server del Gestionale Magazzino/Cantieri." | Out-Null
Start-ScheduledTask -TaskName $nomeTask

Write-Host "--- Backup giornaliero del database ---"
$nomeTaskBackup = "GestionaleMagazzinoBackup"
Unregister-ScheduledTask -TaskName $nomeTaskBackup -Confirm:$false -ErrorAction SilentlyContinue
$azioneBackup = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$root\deploy\backup_db.ps1`""
$triggerBackup = New-ScheduledTaskTrigger -Daily -At "20:00"
Register-ScheduledTask -TaskName $nomeTaskBackup -Action $azioneBackup -Trigger $triggerBackup -Description "Copia di sicurezza giornaliera del database del Gestionale." | Out-Null

Write-Host "--- Icona sul Desktop ---"
$desktop = [Environment]::GetFolderPath("Desktop")
$collegamento = @"
[InternetShortcut]
URL=http://127.0.0.1:8000
"@
Set-Content -Path "$desktop\Gestionale.url" -Value $collegamento -Encoding ASCII

Write-Host ""
Write-Host "Fatto. Apri http://127.0.0.1:8000 nel browser (o l'icona 'Gestionale' sul Desktop) per verificare." -ForegroundColor Green
