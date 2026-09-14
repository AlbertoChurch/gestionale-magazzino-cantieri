from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class Ruolo(Base):
    __tablename__ = "ruoli"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    utenti: Mapped[list["Utente"]] = relationship(back_populates="ruolo")

class Utente(Base):
    __tablename__ = "utenti"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), index=True)
    cognome: Mapped[str] = mapped_column(String(100), index=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    ruolo_id: Mapped[int] = mapped_column(ForeignKey("ruoli.id"))

    ruolo: Mapped["Ruolo"] = relationship(back_populates="utenti")

class Fornitore(Base):
    __tablename__ = "fornitori"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), index=True)
    descrizione: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    email_generale: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    email_commerciale: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    email_tecnico: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    email_amministrazione: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    telefono_fisso: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    cellulare_1: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    cellulare_2: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    referente_1: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    referente_2: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    materiali: Mapped[list["Materiale"]] = relationship(back_populates="fornitore")
    bolle: Mapped[list["Bolla"]] = relationship(back_populates="fornitore")

class TipoPosizione(Base):
    __tablename__ = "tipi_posizione"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    posizioni: Mapped[list["Posizione"]] = relationship(back_populates="tipo_posizione")

class Posizione(Base):
    __tablename__ = "posizioni"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), index=True)
    indirizzo: Mapped[Optional[str]] = mapped_column(String(255), index=True, nullable=True)
    tipo_posizione_id: Mapped[int] = mapped_column(ForeignKey("tipi_posizione.id"))
    data_apertura: Mapped[Optional[datetime]] = mapped_column(DateTime, index=True, nullable=True)
    data_chiusura: Mapped[Optional[datetime]] = mapped_column(DateTime, index=True, nullable=True)

    tipo_posizione: Mapped["TipoPosizione"] = relationship(back_populates="posizioni")

class UnitaMisura(Base):
    __tablename__ = "unita_misura"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    materiali: Mapped[list["Materiale"]] = relationship(back_populates="unita_misura")

class TipoMateriale(Base):
    __tablename__ = "tipi_materiale"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    materiali: Mapped[list["Materiale"]] = relationship(secondary="materiali_tipi_materiale", back_populates="tipi_materiale")

class Materiale(Base):
    __tablename__ = "materiali"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), index=True)
    fornitore_id: Mapped[int] = mapped_column(ForeignKey("fornitori.id"))
    unita_misura_id: Mapped[int] = mapped_column(ForeignKey("unita_misura.id"))

    fornitore: Mapped["Fornitore"] = relationship(back_populates="materiali")
    unita_misura: Mapped["UnitaMisura"] = relationship(back_populates="materiali")
    tipi_materiale: Mapped[list["TipoMateriale"]] = relationship(secondary="materiali_tipi_materiale", back_populates="materiali")


class MaterialeTipoMateriale(Base):
    __tablename__ = "materiali_tipi_materiale"

    materiale_id: Mapped[int] = mapped_column(ForeignKey("materiali.id"), primary_key=True)
    tipo_materiale_id: Mapped[int] = mapped_column(ForeignKey("tipi_materiale.id"), primary_key=True)


class Bolla(Base):
    __tablename__ = "bolle"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    data: Mapped[Optional[datetime]] = mapped_column(DateTime, index=True)
    numero: Mapped[str] = mapped_column(String(50))
    numero_ordine_riferimento: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    fornitore_id: Mapped[int] = mapped_column(ForeignKey("fornitori.id"))
    firmatario: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    operatori_scarico: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    fornitore: Mapped["Fornitore"] = relationship(back_populates="bolle")


class Lotto(Base):
    __tablename__ = "lotti"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    bolla_id: Mapped[int] = mapped_column(ForeignKey("bolle.id"))
    materiale_id: Mapped[int] = mapped_column(ForeignKey("materiali.id"))
    quantita_iniziale: Mapped[float] = mapped_column(Numeric(10, 2), index=True)
    quantita_disponibile: Mapped[float] = mapped_column(Numeric(10, 2), index=True)

    materiale: Mapped["Materiale"] = relationship()
    bolla: Mapped["Bolla"] = relationship()

class CondizioneMateriale(Base):
    __tablename__ = "condizioni_materiale"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True, index=True)

class Movimento(Base):
    __tablename__ = "movimenti"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lotto_id: Mapped[int] = mapped_column(ForeignKey("lotti.id"))
    posizione_partenza_id: Mapped[Optional[int]] = mapped_column(ForeignKey("posizioni.id"), nullable=True)
    posizione_arrivo_id: Mapped[int] = mapped_column(ForeignKey("posizioni.id"))
    quantita_usata: Mapped[float] = mapped_column(Numeric(10, 2), index=True)
    data_movimento: Mapped[Optional[datetime]] = mapped_column(DateTime, index=True)
    note: Mapped[Optional[str]] = mapped_column(String(255), index=True, nullable=True)
    condizione_id: Mapped[Optional[int]] = mapped_column(ForeignKey("condizioni_materiale.id"), nullable=True)
    nota_partenza: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    condizione_partenza_id: Mapped[Optional[int]] = mapped_column(ForeignKey("condizioni_materiale.id"), nullable=True)

    posizione_arrivo: Mapped["Posizione"] = relationship(foreign_keys=[posizione_arrivo_id])
    posizione_partenza: Mapped[Optional["Posizione"]] = relationship(foreign_keys=[posizione_partenza_id])
    lotto: Mapped["Lotto"] = relationship()
    condizione: Mapped[Optional["CondizioneMateriale"]] = relationship(foreign_keys=[condizione_id])
    condizione_partenza: Mapped[Optional["CondizioneMateriale"]] = relationship(foreign_keys=[condizione_partenza_id])
