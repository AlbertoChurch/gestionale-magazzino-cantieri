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
    ordini: Mapped[list["Ordine"]] = relationship(back_populates="utente")

class Fornitore(Base):
    __tablename__ = "fornitori"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), index=True)
    email: Mapped[Optional[str]] = mapped_column(String(150), unique=True, index=True, nullable=True)
    telefono: Mapped[Optional[str]] = mapped_column(String(20), index=True, nullable=True)

    materiali: Mapped[list["Materiale"]] = relationship(back_populates="fornitore")
    ordini: Mapped[list["Ordine"]] = relationship(back_populates="fornitore")

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

class MaterialeOrdine(Base):
    __tablename__ = "materiali_ordini"

    materiale_id: Mapped[int] = mapped_column(ForeignKey("materiali.id"), primary_key=True)
    ordine_id: Mapped[int] = mapped_column(ForeignKey("ordini.id"), primary_key=True)
    quantita: Mapped[float] = mapped_column(Numeric(10, 2))

    materiale: Mapped["Materiale"] = relationship(back_populates="ordini")
    ordine: Mapped["Ordine"] = relationship(back_populates="materiale_ordinato")

class Materiale(Base):
    __tablename__ = "materiali"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), index=True)
    fornitore_id: Mapped[int] = mapped_column(ForeignKey("fornitori.id"))
    unita_misura_id: Mapped[int] = mapped_column(ForeignKey("unita_misura.id"))

    fornitore: Mapped["Fornitore"] = relationship(back_populates="materiali")
    unita_misura: Mapped["UnitaMisura"] = relationship(back_populates="materiali")
    tipi_materiale: Mapped[list["TipoMateriale"]] = relationship(secondary="materiali_tipi_materiale", back_populates="materiali")
    ordini: Mapped[list["MaterialeOrdine"]] = relationship(back_populates="materiale")


class StatoOrdine(Base):
    __tablename__ = "stati_ordine"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    ordini: Mapped[list["Ordine"]] = relationship(back_populates="stato_ordine")

class Ordine(Base):
    __tablename__ = "ordini"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    data_ordine: Mapped[Optional[datetime]] = mapped_column(DateTime, index=True)
    utente_id: Mapped[int] = mapped_column(ForeignKey("utenti.id"))
    stato_ordine_id: Mapped[int] = mapped_column(ForeignKey("stati_ordine.id"))
    fornitore_id: Mapped[int] = mapped_column(ForeignKey("fornitori.id"))

    utente: Mapped["Utente"] = relationship(back_populates="ordini")
    stato_ordine: Mapped["StatoOrdine"] = relationship(back_populates="ordini")
    materiale_ordinato: Mapped[list["MaterialeOrdine"]] = relationship(back_populates="ordine")
    fornitore: Mapped["Fornitore"] = relationship(back_populates="ordini")

class MaterialeTipoMateriale(Base):
    __tablename__ = "materiali_tipi_materiale"

    materiale_id: Mapped[int] = mapped_column(ForeignKey("materiali.id"), primary_key=True)
    tipo_materiale_id: Mapped[int] = mapped_column(ForeignKey("tipi_materiale.id"), primary_key=True)


class Bolla(Base):
    __tablename__ = "bolle"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    data: Mapped[Optional[datetime]] = mapped_column(DateTime, index=True)
    numero: Mapped[str] = mapped_column(String(50))


class BollaOdine(Base):
    __tablename__ = "bolle_ordini"

    bolla_id: Mapped[int] = mapped_column(ForeignKey("bolle.id"), primary_key=True)
    ordine_id: Mapped[int] = mapped_column(ForeignKey("ordini.id"), primary_key=True)

class StatoLotto(Base):
    __tablename__ = "stati_lotti"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True, index=True)

class Lotto(Base):
    __tablename__ = "lotti"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    bolla_id: Mapped[int] = mapped_column(ForeignKey("bolle.id"))
    quantita_iniziale: Mapped[float] = mapped_column(Numeric(10, 2), index=True)
    quantita_disponibile: Mapped[float] = mapped_column(Numeric(10, 2), index=True)
    stato_lotto_id: Mapped[int] = mapped_column(ForeignKey("stati_lotti.id"))

class Movimento(Base):
    __tablename__ = "movimenti"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lotto_id: Mapped[int] = mapped_column(ForeignKey("lotti.id"))
    posizione_partenza_id: Mapped[Optional[int]] = mapped_column(ForeignKey("posizioni.id"), nullable=True)
    posizione_arrivo_id: Mapped[int] = mapped_column(ForeignKey("posizioni.id"))
    quantita_usata: Mapped[float] = mapped_column(Numeric(10, 2), index=True)
    data_movimento: Mapped[Optional[datetime]] = mapped_column(DateTime, index=True)
    note: Mapped[Optional[str]] = mapped_column(String(255), index=True, nullable=True)
