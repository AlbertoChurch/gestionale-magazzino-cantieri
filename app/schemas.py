from typing import Optional
from pydantic import BaseModel, ConfigDict

class FornitoreCreate(BaseModel):
    nome: str
    email: Optional[str] = None
    telefono: Optional[str] = None

class FornitoreRead(FornitoreCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

    