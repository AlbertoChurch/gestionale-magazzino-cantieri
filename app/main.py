from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

app = FastAPI(title="Gestionale Magazzion/cantiere")

@app.get("/")
async def root():
    return {"status": "ok", "messaggio": "Gestionale attivo"}

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
    
