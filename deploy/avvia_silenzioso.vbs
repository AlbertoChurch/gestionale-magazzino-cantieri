' Avvia avvia_server.bat senza mostrare la finestra nera del prompt.
' Usato dall'attivita' pianificata di Windows, non va lanciato a mano dal cliente.
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
cartella = fso.GetParentFolderName(WScript.ScriptFullName)
bat = cartella & "\avvia_server.bat"
shell.Run """" & bat & """", 0, False
