from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

import hashlib, secrets
from datetime import datetime
from decimal import Decimal

app = FastAPI(title="Gestionale Magazzion/cantiere")

@app.get("/")
async def root():
    return {"status": "ok", "messaggio": "Gestionale attivo"}

#Fornitori

@app.post("/fornitori", response_model=schemas.FornitoreRead)
def create_fornitore(fornitore: schemas.FornitoreCreate, db: Session = Depends(get_db)):
    nuovo = models.Fornitore(**fornitore.model_dump())
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/fornitori", response_model=list[schemas.FornitoreRead])
def leggi_fornitori(db: Session = Depends(get_db)):
    return db.query(models.Fornitore).all()

#Posizioni

@app.post("/posizioni", response_model=schemas.PosizioneRead)
def create_posizione(posizione: schemas.PosizioneCreate, db: Session = Depends(get_db)):
    nuovo = models.Posizione(**posizione.model_dump())
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/posizioni", response_model=list[schemas.PosizioneRead])
def leggi_posizioni(db: Session = Depends(get_db)):
    return db.query(models.Posizione).all()

#PosizioniTipo

@app.post("/tipo_posizioni", response_model=schemas.TipoPosizioneRead)
def create_tipo_posizione(tipo_posizione: schemas.TipoPosizioneCreate, db: Session = Depends(get_db)):
    nuovo = models.TipoPosizione(**tipo_posizione.model_dump())
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/tipo_posizioni", response_model=list[schemas.TipoPosizioneRead])
def leggi_tipo_posizioni(db: Session = Depends(get_db)):
    return db.query(models.TipoPosizione).all()

#Ruoli

@app.post("/ruoli", response_model=schemas.RuoloRead)
def create_ruoli(ruolo: schemas.RuoloCreate, db: Session = Depends(get_db)):
    nuovo = models.Ruolo(**ruolo.model_dump())
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/ruoli", response_model=list[schemas.RuoloRead])
def leggi_ruoli(db: Session = Depends(get_db)):
    return db.query(models.Ruolo).all()

#UnitaMisura

@app.post("/unita_misura", response_model=schemas.UnitaMisuraRead)
def create_unita_misura(unita_misura: schemas.UnitaMisuraCreate, db: Session = Depends(get_db)):
    nuovo = models.UnitaMisura(**unita_misura.model_dump())
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/unita_misura", response_model=list[schemas.UnitaMisuraRead])
def leggi_unita_misura(db: Session = Depends(get_db)):
    return db.query(models.UnitaMisura).all()

#TipoMateriali

@app.post("/tipo_materiali", response_model=schemas.TipoMaterialeRead)
def create_tipo_materiali(tipo_materiale: schemas.TipoMaterialeCreate, db: Session = Depends(get_db)):
    nuovo = models.TipoMateriale(**tipo_materiale.model_dump())
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/tipo_materiali", response_model=list[schemas.TipoMaterialeRead])
def leggi_tipo_materiali(db: Session = Depends(get_db)):
    return db.query(models.TipoMateriale).all()

#StatoOrdini

@app.post("/stato_ordini", response_model=schemas.StatoOrdineRead)
def create_stato_ordini(stato_ordine: schemas.StatoOrdineCreate, db: Session = Depends(get_db)):
    nuovo = models.StatoOrdine(**stato_ordine.model_dump())
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/stato_ordini", response_model=list[schemas.StatoOrdineRead])
def leggi_stato_ordini(db: Session = Depends(get_db)):
    return db.query(models.StatoOrdine).all()

#StatoLotti

@app.post("/stato_lotti", response_model=schemas.StatoLottoRead)
def create_stato_lotti(stato_lotto: schemas.StatoLottoCreate, db: Session = Depends(get_db)):
    nuovo = models.StatoLotto(**stato_lotto.model_dump())
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/stato_lotti", response_model=list[schemas.StatoLottoRead])
def leggi_stato_lotti(db: Session = Depends(get_db)):
    return db.query(models.StatoLotto).all()

#materiale

@app.post("/materiali", response_model=schemas.MaterialeRead)
def create_materiale(materiale: schemas.MaterialeCreate, db: Session = Depends(get_db)):
    tipi = db.query(models.TipoMateriale).filter(models.TipoMateriale.id.in_(materiale.tipo_materiale_ids)).all()
    nuovo = models.Materiale(**materiale.model_dump(exclude={"tipo_materiale_ids"}))
    db.add(nuovo)
    nuovo.tipi_materiale = tipi
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/materiali", response_model=list[schemas.MaterialeRead])
def leggi_materiali(db: Session = Depends(get_db)):
    return db.query(models.Materiale).all()

#utente

@app.post("/utenti", response_model=schemas.UtenteRead)
def create_utente(utente: schemas.UtenteCreate, db: Session = Depends(get_db)):
    salt = secrets.token_bytes(16)
    hash_password = hashlib.scrypt(utente.password.encode(), salt=salt, n=2**14, r=8, p=1)
    password_hash = salt.hex() + "$" + hash_password.hex()

    nuovo = models.Utente(**utente.model_dump(exclude={"password"}), password_hash=password_hash)
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/utenti", response_model=list[schemas.UtenteRead])
def leggi_utenti(db: Session = Depends(get_db)):
    return db.query(models.Utente).all()

#ordine

@app.post("/ordini", response_model=schemas.OrdineRead)
def create_ordine(ordine: schemas.OrdineCreate, db: Session = Depends(get_db)):
    dati = ordine.model_dump()
    if dati["data_ordine"] is None:
        dati["data_ordine"] = datetime.now()
    nuovo = models.Ordine(**dati)
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/ordini", response_model=list[schemas.OrdineRead])
def leggi_ordini(db: Session = Depends(get_db)):
    return db.query(models.Ordine).all()

#materialeordine

@app.post("/materiali-ordini", response_model=schemas.MaterialeOrdineRead)
def create_materiale_ordine(materiale_ordine:schemas.MaterialeOrdineCreate, db: Session = Depends(get_db)):
    nuovo = models.MaterialeOrdine(**materiale_ordine.model_dump())
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/materiali-ordini", response_model=list[schemas.MaterialeOrdineRead])
def leggi_materiali_ordini(db: Session = Depends(get_db)):
    return db.query(models.MaterialeOrdine).all()

#Bolla

@app.post("/bolle", response_model=schemas.BollaRead)
def create_bolla(bolla: schemas.BollaCreate, db: Session = Depends(get_db)):
    dati = bolla.model_dump()
    if dati["data"] is None:
        dati["data"] = datetime.now()
    nuovo = models.Bolla(**dati)
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/bolle", response_model=list[schemas.BollaRead])
def leggi_bolle(db: Session = Depends(get_db)):
    return db.query(models.Bolla).all()

#BollaOrdine

@app.post("/bolle-ordini", response_model=schemas.BollaOrdineRead)
def create_bolla_ordine(bolla_ordine:schemas.BollaOrdineCreate, db: Session = Depends(get_db)):
    nuovo = models.BollaOrdine(**bolla_ordine.model_dump())
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/bolle-ordini", response_model=list[schemas.BollaOrdineRead])
def leggi_bolle_ordini(db: Session = Depends(get_db)):
    return db.query(models.BollaOrdine).all()

#Lotto

@app.post("/lotti", response_model=schemas.LottoRead)
def create_lotto(lotto: schemas.LottoCreate, db: Session = Depends(get_db)):
    dati = lotto.model_dump()
    dati["quantita_disponibile"] = dati["quantita_iniziale"]
    nuovo = models.Lotto(**dati)
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/lotti", response_model=list[schemas.LottoRead])
def leggi_lotti(db: Session = Depends(get_db)):
    return db.query(models.Lotto).all()

#Movimento

@app.post("/movimenti", response_model=schemas.MovimentoRead)
def create_movimento(movimento: schemas.MovimentoCreate, db: Session = Depends(get_db)):
    lotto = db.query(models.Lotto).filter(models.Lotto.id == movimento.lotto_id).first()
    if lotto is None:
        raise HTTPException(status_code=404, detail="Lotto non trovato")
    posizione_arrivo = db.query(models.Posizione).filter(models.Posizione.id == movimento.posizione_arrivo_id).first()
    if posizione_arrivo is None:
        raise HTTPException(status_code=404, detail="Posizione di arrivo non trovata")
    if posizione_arrivo.tipo_posizione.nome != "magazzino":
        lotto.quantita_disponibile -= Decimal(str(movimento.quantita_usata)) # type: ignore
    else:
        lotto.quantita_disponibile += Decimal(str(movimento.quantita_usata)) # type: ignore
    dati = movimento.model_dump()
    if dati["data_movimento"] is None:
        dati["data_movimento"] = datetime.now()
    nuovo = models.Movimento(**dati)
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/movimenti", response_model=list[schemas.MovimentoRead])
def leggi_movimenti(db: Session = Depends(get_db)):
    return db.query(models.Movimento).all()

