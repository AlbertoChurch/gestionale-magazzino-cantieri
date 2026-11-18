"""Crea il primo utente Amministratore su un database nuovo/vuoto.

Serve solo la primissima volta: creare utenti dall'interfaccia richiede
gia' di essere loggati come amministratore, quindi il primissimo account
va creato a mano. Va eseguito con la working directory sulla radice del
progetto (ci pensa installa.ps1). Puo' essere rilanciato in sicurezza:
se un amministratore esiste gia' non fa nulla.
"""
import getpass
import sys

from app.database import Base, engine, SessionLocal
from app import models
from app.main import genera_password_hash

Base.metadata.create_all(engine)
db = SessionLocal()

ruolo = db.query(models.Ruolo).filter(models.Ruolo.nome == "Amministratore").first()
if ruolo is None:
    ruolo = models.Ruolo(nome="Amministratore")
    db.add(ruolo)
    db.commit()
    db.refresh(ruolo)

if db.query(models.Utente).filter(models.Utente.ruolo_id == ruolo.id).first():
    print("Esiste gia' un amministratore, non ne creo un altro.")
else:
    print("Creazione del primo utente amministratore.")
    nome = input("Nome: ").strip()
    cognome = input("Cognome: ").strip()
    email = input("Email di accesso: ").strip()
    if sys.stdin.isatty():
        # getpass legge direttamente dalla console: se lo stdin non e'
        # una console vera (es. input rediretto) resterebbe bloccato in
        # attesa di un tasto che non arrivera' mai, va evitato a monte.
        password = getpass.getpass("Password: ")
    else:
        password = input("Password (visibile, niente console per nasconderla): ")
    utente = models.Utente(
        nome=nome, cognome=cognome, email=email,
        password_hash=genera_password_hash(password), ruolo_id=ruolo.id,
    )
    db.add(utente)
    db.commit()
    print(f"Fatto. Accesso: {email}")

db.close()
