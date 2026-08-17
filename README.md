# Gestionale Magazzino/Cantieri

API REST per tracciare materiali tra magazzini e cantieri: ordini a
fornitore, bolle di consegna, lotti e movimenti tra posizioni.

Progetto personale di apprendimento — sviluppato passo passo con FastAPI e
SQLAlchemy, ancora in fase iniziale di sviluppo.

## Stack
- **Python 3.14**
- **FastAPI** — framework API
- **SQLAlchemy 2.0** — ORM verso il database
- **Pydantic** — validazione dati in input/output
- **SQLite** — database (sviluppo locale)

## Avvio in locale

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows
pip install -r requirements.txt

python -c "from app.database import Base, engine; from app import models; Base.metadata.create_all(engine)"

uvicorn app.main:app --reload
```

Documentazione interattiva (Swagger UI), generata automaticamente da
FastAPI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Struttura

```
app/
├── database.py   # connessione e sessione al database
├── models.py     # tabelle (SQLAlchemy)
├── schemas.py    # validazione input/output API (Pydantic)
└── main.py       # endpoint
```

## Stato

Modello dati completo (anagrafiche, ordini, bolle, lotti, movimenti).
Endpoint implementati finora: CRUD Fornitore (`POST`/`GET /fornitori`).
