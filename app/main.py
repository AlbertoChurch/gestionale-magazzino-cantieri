from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

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
