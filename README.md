# Gestionale Magazzino/Cantieri

Applicazione web per tenere traccia dei materiali che arrivano da un fornitore,
entrano in magazzino e vengono spostati tra magazzini e cantieri: bolle di
consegna, lotti, movimenti, giacenze per posizione e uno storico di tutto
quello che è successo.

Progetto personale, sviluppato passo passo con FastAPI e SQLAlchemy. Pensato
per un solo PC (il server ascolta solo su `127.0.0.1`): non esporlo su internet.

## Provalo in pochi minuti (con dati di esempio)

Serve [Python 3.14](https://www.python.org/downloads/) (la versione con cui è
sviluppato e provato). Da PowerShell:

```powershell
git clone https://github.com/AlbertoChurch/gestionale-magazzino-cantieri.git
cd gestionale-magazzino-cantieri
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python deploy/dati_demo.py
uvicorn app.main:app
```

Poi apri <http://127.0.0.1:8000> e accedi con:

| Ruolo | Email | Password |
|---|---|---|
| Amministratore | `admin@example.com` | `demo1234` |
| Operatore | `operatore@example.com` | `demo1234` |

(Su macOS/Linux al posto di `.venv\Scripts\Activate.ps1` si usa
`source .venv/bin/activate`. Se PowerShell rifiuta l'attivazione, lancia prima
`Set-ExecutionPolicy -Scope Process Bypass`.)

I dati sono inventati: un magazzino, tre cantieri, tre fornitori con i loro
materiali, tre bolle già arrivate e qualche spostamento già fatto. Per
ricominciare da zero cancella `gestionale.db` e rilancia `deploy/dati_demo.py`
(lo script si rifiuta di girare su un database che contiene già dei dati).

## Cosa puoi provare

- **Giacenze** — dove si trova ogni materiale e in che quantità. Cerca e filtra
  per posizione. Lo stesso materiale può comparire su più righe: una per
  posizione, e una a parte se ha una condizione o una nota diversa (per esempio
  il trapano rientrato "difettoso" con la nota "mandrino da riparare").
- **Nuovo movimento** — scegli da dove parte e dove arriva, poi aggiungi
  all'elenco **più materiali** e registrali in un colpo solo. È "tutto o niente":
  se una riga non è valida (per esempio chiedi più di quanto c'è) non viene
  registrato nessun movimento e ti viene detto quale riga è il problema.
  Prova a spostare 100 kg di *Sabbia lavata* e 50 *Tasselli* dal *Magazzino
  centrale* al *Cantiere Via Roma*.
- **Rientro difettoso** — sposta un materiale da un cantiere al magazzino
  scegliendo la condizione "difettoso" e una nota: in Giacenze compare come riga
  distinta, senza confondersi con quello in buone condizioni.
- **Storico** — tutti i movimenti, con filtri combinabili (date, materiale,
  posizioni, condizione, note). Ogni movimento si può correggere (quantità,
  condizione, note, data) o eliminare; se la modifica renderebbe incoerenti le
  giacenze (per esempio un materiale già spostato altrove) viene rifiutata con un
  messaggio chiaro.
- **Inserimento materiale** — registra una nuova bolla del fornitore e aggiungi i
  materiali arrivati uno alla volta: finiscono nel magazzino che scegli e
  compaiono subito in Giacenze.
- **Bolle e Fornitori** — elenchi con ricerca, pagina di dettaglio del fornitore
  con i suoi contatti e i materiali che fornisce. **Archivio** per le bolle più
  vecchie di 12 mesi e per i cantieri/magazzini chiusi.
- **Aggiungi dati** — fornitori, posizioni, materiali, condizioni, unità di
  misura. Eliminare un elemento richiede due clic ("Sei sicuro?") ed è bloccato,
  con un avviso giallo, se è ancora in uso da qualche parte. Un cantiere si può
  chiudere e riaprire.
- **Account utente** (solo amministratore) e cambio password.

Cosa **non** c'è ancora: un'azione "segna come usato/consumato" (oggi un
movimento sposta il materiale ma non lo consuma), il collegamento con gli ordini
ai fornitori (si fanno fuori dal gestionale), l'uso da più PC. Le sessioni di
accesso stanno in memoria: riavviando il server bisogna rifare il login.

## Stack

- **Python 3.14**, **FastAPI**, pagine HTML con **Jinja2** (niente framework
  JavaScript)
- **SQLAlchemy 2.0** su **SQLite** (un solo file, `gestionale.db`, non versionato)
- **Pydantic** per la validazione dei dati in ingresso

## Struttura

```
app/
├── main.py        # rotte e logica (movimenti, giacenze, eliminazioni sicure)
├── models.py      # tabelle (SQLAlchemy)
├── schemas.py     # validazione dei dati in ingresso (Pydantic)
├── database.py    # connessione al database
├── templates/     # pagine HTML (Jinja2)
└── static/        # CSS e JavaScript
deploy/            # installazione sul PC di un cliente, dati demo, import da Excel
```

Per installarlo sul PC di un cliente (avvio automatico, backup giornaliero,
import di fornitori e materiali da Excel) vedi [deploy/README.md](deploy/README.md).
