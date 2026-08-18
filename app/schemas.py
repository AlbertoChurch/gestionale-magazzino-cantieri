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