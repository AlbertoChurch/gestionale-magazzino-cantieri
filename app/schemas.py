from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class FornitoreCreate(BaseModel):
    nome: str
    descrizione: Optional[str] = None
    email_generale: Optional[str] = None
    email_commerciale: Optional[str] = None
    email_tecnico: Optional[str] = None
    email_amministrazione: Optional[str] = None
    telefono_fisso: Optional[str] = None
    cellulare_1: Optional[str] = None
    cellulare_2: Optional[str] = None
    referente_1: Optional[str] = None
    referente_2: Optional[str] = None

class FornitoreRead(FornitoreCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class PosizioneCreate(BaseModel):
    nome: str
    indirizzo: Optional[str] = None
    tipo_posizione_id: int

class PosizioneRead(PosizioneCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class TipoPosizioneCreate(BaseModel):
    nome: str

class TipoPosizioneRead(TipoPosizioneCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class RuoloCreate(BaseModel):
    nome: str

class RuoloRead(RuoloCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class UnitaMisuraCreate(BaseModel):
    nome: str

class UnitaMisuraRead(UnitaMisuraCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class TipoMaterialeCreate(BaseModel):
    nome: str

class TipoMaterialeRead(TipoMaterialeCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CondizioneMaterialeCreate(BaseModel):
    nome: str

class CondizioneMaterialeRead(CondizioneMaterialeCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

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

class LoginRequest(BaseModel):
    email: str
    password: str


class BollaCreate(BaseModel):
    numero: str
    data: Optional[datetime] = None
    numero_ordine_riferimento: Optional[str] = None
    fornitore_id: int
    firmatario: Optional[str] = None
    operatori_scarico: Optional[str] = None

class BollaRead(BollaCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class LottoCreate(BaseModel):
    bolla_id: int
    materiale_id: int
    quantita_iniziale: float

class LottoRead(LottoCreate):
    model_config = ConfigDict(from_attributes=True)
    quantita_disponibile: float
    id: int


class MovimentoCreate(BaseModel):
    lotto_id: int
    posizione_partenza_id: Optional[int] = None
    posizione_arrivo_id: int
    quantita_usata: float = Field(allow_inf_nan=False)
    data_movimento: Optional[datetime] = None
    note: Optional[str] = None
    condizione_id: Optional[int] = None
    nota_partenza: Optional[str] = None
    condizione_partenza_id: Optional[int] = None

class RigaMovimentoForm(BaseModel):
    """Una riga dell'elenco 'materiali da spostare' del form Registra movimento
    (partenza e arrivo sono uguali per tutte le righe e arrivano a parte)."""
    lotto_id: int
    quantita_usata: float = Field(allow_inf_nan=False)
    condizione_id: Optional[int] = None
    note: Optional[str] = None
    condizione_partenza_id: Optional[int] = None
    nota_partenza: Optional[str] = None

class MovimentoRead(MovimentoCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
