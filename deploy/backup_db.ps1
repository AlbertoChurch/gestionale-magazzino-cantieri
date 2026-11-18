# Copia di sicurezza di gestionale.db, con data/ora nel nome.
# Lanciato ogni giorno dall'attivita' pianificata "GestionaleMagazzinoBackup"
# (creata da installa.ps1) - non va lanciato a mano dal cliente.
#
# La cartella di backup e' volutamente FUORI da C:\Gestionale: se la
# cartella del programma viene cancellata o corrotta per sbaglio, il
# backup resta intatto. E' comunque sullo stesso disco: se il disco si
# rompe fisicamente si perde anche quello - da spostare su un secondo
# disco/cloud appena possibile.

$root = Split-Path -Parent $PSScriptRoot
$backupDir = Join-Path (Split-Path -Parent $root) "GestionaleBackup"

New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

$data = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item -Path "$root\gestionale.db" -Destination "$backupDir\gestionale_$data.db"

# Tiene solo gli ultimi 30 giorni di backup, per non riempire il disco.
Get-ChildItem -Path $backupDir -Filter "gestionale_*.db" |
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } |
    Remove-Item -Force
