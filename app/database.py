import logging

from sqlalchemy import create_engine, event, inspect
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./gestionale.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False})


@event.listens_for(engine, "connect")
def attiva_vincoli_fk(connessione_dbapi, _):
    # SQLite non controlla le foreign key di default: senza questo, cancellare
    # una riga ancora referenziata altrove lascia i riferimenti orfani invece
    # di dare errore.
    cursore = connessione_dbapi.cursor()
    cursore.execute("PRAGMA foreign_keys=ON")
    cursore.close()

def _migra_schema():
    """Aggiunge colonne nuove alle tabelle già esistenti sul disco. SQLite non
    supporta ALTER TABLE ... ADD COLUMN IF NOT EXISTS: si controlla prima a
    mano, e solo se la tabella esiste già (altrimenti la crea create_all con
    la colonna inclusa)."""
    with engine.connect() as connessione:
        tabelle = {riga[0] for riga in connessione.exec_driver_sql(
            "SELECT name FROM sqlite_master WHERE type='table'")}
        if "fornitori" in tabelle:
            colonne = {riga[1] for riga in connessione.exec_driver_sql("PRAGMA table_info(fornitori)")}
            if "descrizione" not in colonne:
                connessione.exec_driver_sql("ALTER TABLE fornitori ADD COLUMN descrizione VARCHAR(150)")
                connessione.commit()

_migra_schema()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def avvisa_tabelle_obsolete():
    """create_all non elimina mai le tabelle: se si toglie un modello, la sua tabella
    resta nel file .db e, con le foreign key attive, può bloccare le eliminazioni
    (IntegrityError). Non si cancella nulla da soli (si perderebbero dati senza
    backup): si avvisa all'avvio, perché il residuo non passi più inosservato.
    Da chiamare dopo aver importato i models, altrimenti Base.metadata è vuoto."""
    in_piu = sorted(set(inspect(engine).get_table_names()) - set(Base.metadata.tables))
    if in_piu:
        logging.getLogger("uvicorn.error").warning(
            "Nel database ci sono tabelle che non esistono più nei models: %s. "
            "Se hanno foreign key verso tabelle attive bloccano le eliminazioni. "
            "Dopo un backup vanno rimosse con DROP TABLE (esempio: deploy/pulisci_tabelle_ordini.py).",
            ", ".join(in_piu))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()