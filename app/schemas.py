from typing import Optional
from pydantic import BaseModel, ConfigDict

#fornitori

class FornitoreCreate(BaseModel):
    nome: str
    email: Optional[str] = None
    telefono: Optional[str] = None

class FornitoreRead(FornitoreCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

#Posizione

class PosizioneCreate(BaseModel):
    nome: str
    indirizzo: Optional[str] = None
    tipo_posizione_id: int

class PosizioneRead(PosizioneCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

#PosizioneTipo

class TipoPosizioneCreate(BaseModel):
    nome: str

class TipoPosizioneRead(TipoPosizioneCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

#Ruolo

class RuoloCreate(BaseModel):
    nome: str

class RuoloRead(RuoloCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

#UnitàMisura

class UnitaMisuraCreate(BaseModel):
    nome: str

class UnitaMisuraRead(UnitaMisuraCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

#TipoMateriale

class TipoMaterialeCreate(BaseModel):
    nome: str

class TipoMaterialeRead(TipoMaterialeCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

#StatoOrdine

class StatoOrdineCreate(BaseModel):
    nome: str

class StatoOrdineRead(StatoOrdineCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

#StatoLotto

class StatoLottoCreate(BaseModel):
    nome: str

class StatoLottoRead(StatoLottoCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

#materiale
class MaterialeCreate(BaseModel):
    nome: str
    fornitore_id: int
    unita_misura_id: int
    tipo_materiale_ids: list[int] = []

class MaterialeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    fornitore_id: int
    unita_misura_id: int
    tipi_materiale: list[TipoMaterialeRead] = []

#utente

class UtenteCreate(BaseModel):
    nome: str
    cognome: str
    email: str
    password: str
    ruolo_id: int

class UtenteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    cognome: str
    email: str
    ruolo_id: int
