"""Importa fornitori e materiali dal file Excel compilato dal cliente
(modello: deploy/modello_dati_fornitori.xlsx).

Uso:
    python deploy/importa_dati.py percorso\\al\\file.xlsx

Puo' essere rilanciato in sicurezza sullo stesso file aggiornato: i
fornitori/materiali gia' presenti (stesso nome, maiuscole/spazi
ignorati) vengono saltati, non duplicati. Se in "Materiali" c'e' un
riferimento a un fornitore o un'unita' di misura che non esiste, non
importa NULLA (nessuna scrittura parziale) e stampa cosa correggere.
"""
import sys

from openpyxl import load_workbook
from sqlalchemy import func

from app.database import Base, engine, SessionLocal
from app import models
from app.main import valore_gia_esistente

if len(sys.argv) != 2:
    print("Uso: python deploy/importa_dati.py percorso\\al\\file.xlsx")
    sys.exit(1)

Base.metadata.create_all(engine)
db = SessionLocal()
wb = load_workbook(sys.argv[1])


def testo(cella) -> str:
    return str(cella).strip() if cella is not None else ""


def trova_per_nome(modello, nome: str):
    return db.query(modello).filter(func.lower(func.trim(modello.nome)) == nome.strip().lower()).first()


# --- Fornitori ---
creati_fornitori = saltati_fornitori = 0
for riga in wb["Fornitori"].iter_rows(min_row=2, values_only=True):
    nome = testo(riga[0])
    if not nome or nome.upper().startswith("ESEMPIO"):
        continue
    if valore_gia_esistente(db, models.Fornitore, nome):
        saltati_fornitori += 1
        continue
    db.add(models.Fornitore(
        nome=nome,
        descrizione=testo(riga[1]) or None,
        referente_1=testo(riga[2]) or None,
        referente_2=testo(riga[3]) or None,
        email_generale=testo(riga[4]) or None,
        email_commerciale=testo(riga[5]) or None,
        email_tecnico=testo(riga[6]) or None,
        email_amministrazione=testo(riga[7]) or None,
        telefono_fisso=testo(riga[8]) or None,
        cellulare_1=testo(riga[9]) or None,
        cellulare_2=testo(riga[10]) or None,
    ))
    creati_fornitori += 1
db.commit()
print(f"Fornitori creati: {creati_fornitori}, gia' presenti (saltati): {saltati_fornitori}")

# --- Materiali ---
creati_materiali = saltati_materiali = 0
errori = []
for numero_riga, riga in enumerate(wb["Materiali"].iter_rows(min_row=2, values_only=True), start=2):
    nome_fornitore = testo(riga[0])
    nome_materiale = testo(riga[1])
    nome_unita = testo(riga[2])
    if not nome_fornitore and not nome_materiale:
        continue
    if nome_fornitore.upper().startswith("ESEMPIO"):
        continue

    fornitore = trova_per_nome(models.Fornitore, nome_fornitore)
    unita = trova_per_nome(models.UnitaMisura, nome_unita)
    if fornitore is None:
        errori.append(f'riga {numero_riga}: fornitore "{nome_fornitore}" non trovato')
        continue
    if unita is None:
        errori.append(f'riga {numero_riga}: unita\' di misura "{nome_unita}" non trovata')
        continue

    esiste = db.query(models.Materiale).filter(
        func.lower(func.trim(models.Materiale.nome)) == nome_materiale.lower(),
        models.Materiale.fornitore_id == fornitore.id,
    ).first()
    if esiste:
        saltati_materiali += 1
        continue
    db.add(models.Materiale(nome=nome_materiale, fornitore_id=fornitore.id, unita_misura_id=unita.id))
    creati_materiali += 1

if errori:
    db.rollback()
    print("Materiali NON importati, correggi il file e rilancia:")
    for errore in errori:
        print(" -", errore)
else:
    db.commit()
    print(f"Materiali creati: {creati_materiali}, gia' presenti (saltati): {saltati_materiali}")

db.close()
