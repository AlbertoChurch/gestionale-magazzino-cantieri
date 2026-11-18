# Consegna al cliente (v0.1) — procedura per te

Pensato per un solo PC del cliente, nessuna esposizione su internet:
il server gira in background su quel PC e il cliente lo usa dal browser
sullo stesso PC (`http://127.0.0.1:8000`).

## La prima volta (installazione)

1. **Accesso remoto**: fatti installare [AnyDesk](https://anydesk.com)
   al cliente (gratuito, un file solo, non serve account) — o usa
   quello che ha già, se lo ha. Fatti dare il codice e connettiti.
2. **Prerequisiti sul PC del cliente** — verifica che ci siano già,
   altrimenti installali (installer normale, avanti-avanti-fine):
   - [Python 3.14](https://www.python.org/downloads/) — durante
     l'installazione spunta **"Add python.exe to PATH"**.
   - [Git](https://git-scm.com/downloads) — opzioni di default vanno bene.
3. Apri **PowerShell come Amministratore** sul PC del cliente (tasto
   destro sul menu Start → "Terminal (Amministratore)" o simile).
4. Clona il progetto ed entra nella cartella:
   ```
   git clone https://github.com/AlbertoChurch/gestionale-magazzino-cantieri.git C:\Gestionale
   cd C:\Gestionale
   ```
5. Lancia l'installazione:
   ```
   powershell -ExecutionPolicy Bypass -File deploy\installa.ps1
   ```
   Fa tutto da solo: ambiente Python, dipendenze, ti chiede i dati per
   il primo utente amministratore (nome/email/password — usane una
   vera, non "a"/"a"), avvio automatico all'accesso a Windows, backup
   giornaliero del database, icona "Gestionale" sul Desktop.
6. **Verifica**: apri `http://127.0.0.1:8000` nel browser, fai login
   con l'account appena creato, controlla che Giacenze carichi.
   Controlla anche che l'icona sul Desktop funzioni.
7. Mostra al cliente la procedura in caso di problemi (vedi nota
   "Procedura cliente v0.1" nella cartella `appunti progetto
   gestionale`, da stampare o mandare).

## Le volte successive (aggiornamenti)

Riconnettiti con AnyDesk, poi:
```
cd C:\Gestionale
powershell -ExecutionPolicy Bypass -File deploy\aggiorna.ps1
```
Scarica l'ultima versione da GitHub, aggiorna le dipendenze se servono,
riavvia il server. Non tocca mai `gestionale.db` (è escluso da git).

## Dati iniziali forniti dal cliente (fornitori/materiali)

1. Manda al cliente `deploy/modello_dati_fornitori.xlsx` — file Excel
   con fogli "Fornitori" e "Materiali" (istruzioni nel primo foglio,
   una riga di esempio in ciascuno). Fallo compilare e rimandare.
2. Quando arriva, sul tuo PC (dal `.venv` di questo progetto, **non**
   serve farlo sul PC del cliente):
   ```
   .venv\Scripts\python deploy\importa_dati.py percorso\al\file_del_cliente.xlsx
   ```
   Se un'unità di misura o un riferimento non torna, non importa nulla
   e stampa esattamente la riga da correggere — sistema il file (o
   aggiungi prima l'anagrafica mancante da "Aggiungi dati" nell'app) e
   rilancia. Rilanciarlo sullo stesso file più volte è sicuro: i
   fornitori/materiali già presenti vengono saltati, non duplicati.
3. Avvia il server in locale e controlla su `/fornitori-elenco` che i
   dati siano quelli giusti prima di consegnare.
4. Quando è tutto a posto, questo `gestionale.db` (con già dentro i
   dati) è quello da portare/copiare sul PC del cliente durante
   l'installazione — non serve reimportare tutto da capo lì.

> **Attenzione al database da consegnare.** Il tuo `gestionale.db` di
> sviluppo contiene ancora le vecchie tabelle degli ordini
> (`materiali_ordini`, `bolle_ordini`, `ordini`, `stati_ordine`), con
> righe orfane che oggi bloccano l'eliminazione di alcuni materiali
> nuovi (errore 409). Un cliente non deve ereditarle: per lui crea un
> database **pulito** (rinomina il tuo `gestionale.db`, lancia
> `python -c "from app.database import Base, engine; from app import models; Base.metadata.create_all(engine)"`,
> poi `deploy\primo_admin.py` e `deploy\importa_dati.py`) e consegna
> quel file.

## Cose da sapere

- Il server ascolta solo su `127.0.0.1` (non raggiungibile da altri PC
  della rete) — è voluto per la v0.1, un solo PC. Quando servirà farlo
  vedere da più postazioni in ufficio, cambia `--host 127.0.0.1` in
  `--host 0.0.0.0` in `avvia_server.bat` e usa l'IP del PC invece di
  `127.0.0.1` dagli altri computer.
- I backup del database finiscono in `C:\GestionaleBackup\` (fuori
  dalla cartella del programma, tenuti 30 giorni). Sposta anche questa
  cartella su un secondo disco/drive esterno/cloud appena possibile —
  oggi protegge solo da "cartella cancellata per sbaglio", non da un
  disco rotto.
- Se qualcosa si blocca: riavviare il PC del cliente risolve quasi
  sempre (il server riparte da solo). Se persiste, riconnettiti e
  controlla `C:\Gestionale\logs\server.log`.
