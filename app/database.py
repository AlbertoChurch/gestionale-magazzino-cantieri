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

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()