"""Riempie un database NUOVO con dati di esempio inventati, per provare l'app.

Uso, dalla radice del progetto:
    python deploy/dati_demo.py

Crea le tabelle, due utenti (un amministratore e un operatore), un magazzino e
tre cantieri, tre fornitori con i loro materiali, tre bolle con i lotti arrivati
e qualche movimento gia' fatto (anche un rientro "difettoso"): cosi' Giacenze e
Storico non sono vuoti e si puo' provare subito a spostare del materiale.

Si rifiuta di girare se il database contiene gia' qualcosa: non mischia mai i
dati di esempio con dati veri. Per ripartire da zero cancella gestionale.db.
"""
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
os.chdir(RADICE)  # database.py e main.py usano percorsi relativi alla radice del progetto
sys.path.insert(0, str(RADICE))

from app.database import Base, engine, SessionLocal  # noqa: E402
from app import models, schemas  # noqa: E402
from app.main import genera_password_hash, registra_movimento  # noqa: E402

PASSWORD = "demo1234"
NOTA_ARRIVO = "Arrivo iniziale in magazzino"  # stessa nota che scrive il form "Inserimento materiale"

Base.metadata.create_all(engine)
db = SessionLocal()

if any(db.query(modello).first() for modello in (models.Utente, models.Fornitore, models.Materiale, models.Posizione)):
    print("Il database contiene gia' dei dati: non aggiungo quelli di esempio per non mischiarli con dati veri.")
    print("Per ripartire da zero cancella (o rinomina) gestionale.db e rilancia.")
    sys.exit(1)

adesso = datetime.now()


def giorni_fa(n: int) -> datetime:
    return adesso - timedelta(days=n)


def crea(modello, **campi):
    oggetto = modello(**campi)
    db.add(oggetto)
    db.flush()  # serve l'id subito, per collegare le righe successive
    return oggetto


# --- Utenti ---
amministratore = crea(models.Ruolo, nome="Amministratore")
operatore = crea(models.Ruolo, nome="Operatore")
crea(models.Utente, nome="Anna", cognome="Demo", email="admin@example.com",
     password_hash=genera_password_hash(PASSWORD), ruolo_id=amministratore.id)
crea(models.Utente, nome="Marco", cognome="Demo", email="operatore@example.com",
     password_hash=genera_password_hash(PASSWORD), ruolo_id=operatore.id)

# --- Anagrafiche ---
pezzi, kg, metri, sacchi = (crea(models.UnitaMisura, nome=n) for n in ("pezzi", "kg", "metri", "sacchi"))
tipo_magazzino = crea(models.TipoPosizione, nome="magazzino")
tipo_cantiere = crea(models.TipoPosizione, nome="cantiere")
buone = crea(models.CondizioneMateriale, nome="buone condizioni")
difettoso = crea(models.CondizioneMateriale, nome="difettoso")
crea(models.CondizioneMateriale, nome="inutilizzabile")

magazzino = crea(models.Posizione, nome="Magazzino centrale", indirizzo="Via dell'Industria 1",
                 tipo_posizione_id=tipo_magazzino.id, data_apertura=giorni_fa(120))
via_roma = crea(models.Posizione, nome="Cantiere Via Roma", indirizzo="Via Roma 12",
                tipo_posizione_id=tipo_cantiere.id, data_apertura=giorni_fa(60))
scuola = crea(models.Posizione, nome="Cantiere Scuola Media", indirizzo="Via delle Scuole 5",
              tipo_posizione_id=tipo_cantiere.id, data_apertura=giorni_fa(45))
palestra = crea(models.Posizione, nome="Cantiere Palestra comunale", indirizzo="Piazza dello Sport 1",
                tipo_posizione_id=tipo_cantiere.id, data_apertura=giorni_fa(20))

# --- Fornitori (tutti inventati) e materiali ---
rossi = crea(models.Fornitore, nome="Ferramenta Rossi", descrizione="Viteria, fissaggi, utensili",
             referente_1="Luca Rossi", email_generale="info@example.com", email_commerciale="vendite@example.com",
             telefono_fisso="000 0000001", cellulare_1="300 0000001")
bianchi = crea(models.Fornitore, nome="Edilcentro Bianchi", descrizione="Cemento, sabbia, laterizi",
               referente_1="Paola Bianchi", email_generale="info@example.com", telefono_fisso="000 0000002")
verdi = crea(models.Fornitore, nome="Elettroforniture Verdi", descrizione="Cavi, quadri, illuminazione",
             referente_1="Carlo Verdi", email_tecnico="assistenza@example.com", telefono_fisso="000 0000003")

viti = crea(models.Materiale, nome="Viti 6x60", fornitore_id=rossi.id, unita_misura_id=pezzi.id)
tasselli = crea(models.Materiale, nome="Tasselli 10 mm", fornitore_id=rossi.id, unita_misura_id=pezzi.id)
trapano = crea(models.Materiale, nome="Trapano a percussione", fornitore_id=rossi.id, unita_misura_id=pezzi.id)
cemento = crea(models.Materiale, nome="Cemento 32.5", fornitore_id=bianchi.id, unita_misura_id=sacchi.id)
sabbia = crea(models.Materiale, nome="Sabbia lavata", fornitore_id=bianchi.id, unita_misura_id=kg.id)
mattoni = crea(models.Materiale, nome="Mattoni forati", fornitore_id=bianchi.id, unita_misura_id=pezzi.id)
cavo = crea(models.Materiale, nome="Cavo elettrico 3x1,5", fornitore_id=verdi.id, unita_misura_id=metri.id)
faretti = crea(models.Materiale, nome="Faretti LED", fornitore_id=verdi.id, unita_misura_id=pezzi.id)

# --- Bolle e lotti arrivati in magazzino ---
bolla_rossi = crea(models.Bolla, data=giorni_fa(14), numero="DDT-101", numero_ordine_riferimento="ORD-501",
                   fornitore_id=rossi.id, firmatario="Giorgio (capomagazzino)", operatori_scarico="Luca, Paolo")
bolla_bianchi = crea(models.Bolla, data=giorni_fa(10), numero="DDT-202", numero_ordine_riferimento="ORD-502",
                     fornitore_id=bianchi.id, firmatario="Giorgio (capomagazzino)", operatori_scarico="Paolo")
bolla_verdi = crea(models.Bolla, data=giorni_fa(6), numero="DDT-303", numero_ordine_riferimento="ORD-503",
                   fornitore_id=verdi.id, firmatario="Giorgio (capomagazzino)", operatori_scarico="Luca")


def arrivo(bolla, materiale, quantita):
    # Come fa il form: il lotto nasce con tutta la quantita' disponibile, e il suo
    # primo movimento (arrivo, senza partenza) gli da' posizione e condizione.
    lotto = crea(models.Lotto, bolla_id=bolla.id, materiale_id=materiale.id,
                 quantita_iniziale=quantita, quantita_disponibile=quantita)
    crea(models.Movimento, lotto_id=lotto.id, posizione_partenza_id=None, posizione_arrivo_id=magazzino.id,
         quantita_usata=quantita, data_movimento=bolla.data, note=NOTA_ARRIVO, condizione_id=buone.id)
    return lotto


lotto_viti = arrivo(bolla_rossi, viti, 5000)
lotto_tasselli = arrivo(bolla_rossi, tasselli, 2000)
lotto_trapano = arrivo(bolla_rossi, trapano, 4)
lotto_cemento = arrivo(bolla_bianchi, cemento, 200)
lotto_sabbia = arrivo(bolla_bianchi, sabbia, 3000)
lotto_mattoni = arrivo(bolla_bianchi, mattoni, 1500)
lotto_cavo = arrivo(bolla_verdi, cavo, 500)
lotto_faretti = arrivo(bolla_verdi, faretti, 60)


def sposta(lotto, a, quantita, giorni, da=magazzino, condizione_da=buone, nota_da=NOTA_ARRIVO,
           condizione_a=buone, nota_a=None):
    # Passa da registra_movimento, la stessa funzione dell'app: se un dato demo
    # violasse le sue regole (giacenza insufficiente, ecc.) lo script si fermerebbe qui.
    registra_movimento(schemas.MovimentoCreate(
        lotto_id=lotto.id, posizione_partenza_id=da.id, posizione_arrivo_id=a.id, quantita_usata=quantita,
        data_movimento=giorni_fa(giorni), condizione_id=condizione_a.id, note=nota_a,
        condizione_partenza_id=condizione_da.id, nota_partenza=nota_da,
    ), db, commit=False)


# --- Qualche movimento gia' fatto ---
sposta(lotto_cemento, via_roma, 60, giorni=8)
sposta(lotto_viti, via_roma, 1000, giorni=8)
sposta(lotto_mattoni, scuola, 500, giorni=5)
sposta(lotto_trapano, scuola, 2, giorni=5)
sposta(lotto_cavo, palestra, 200, giorni=3)
sposta(lotto_faretti, palestra, 20, giorni=3)
# Un trapano rientra in magazzino rotto: in Giacenze diventa una riga a parte ("difettoso").
sposta(lotto_trapano, magazzino, 1, giorni=1, da=scuola, nota_da=None,
       condizione_a=difettoso, nota_a="mandrino da riparare")

db.commit()
db.close()

print("Dati di esempio creati.")
print("Accedi con:")
print(f"  amministratore: admin@example.com / {PASSWORD}")
print(f"  operatore:      operatore@example.com / {PASSWORD}")
print("Avvia il server con:  uvicorn app.main:app")
