from sqlalchemy import create_engine, event
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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()