from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app import models, schemas
from app.database import get_db

import hashlib, secrets, json, os
from datetime import datetime
from decimal import Decimal
from typing import Optional
from urllib.parse import quote

app = FastAPI(title="Gestionale Magazzion/cantiere")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
# Versione basata sulla data di modifica del file: il browser scarica il CSS
# aggiornato appena cambia, senza bisogno di ricordarsi di svuotare la cache.
templates.env.globals["versione_css"] = lambda: int(os.path.getmtime("app/static/style.css"))


@app.exception_handler(IntegrityError)
async def gestisci_integrity_error(request: Request, exc: IntegrityError):
    return JSONResponse(status_code=409, content={"detail": "Valore duplicato o dato non valido: controlla di non aver già inserito lo stesso valore."})


def redirect_con_messaggio(url: str, messaggio: str, tipo: str = "ok") -> RedirectResponse:
    """Redirect che porta con sé un messaggio da mostrare come popup nella pagina di arrivo.
    La query va inserita prima dell'eventuale #ancora, non dopo (altrimenti finisce dentro
    il fragment e il browser non la considera più query string)."""
    base, _, ancora = url.partition("#")
    separatore = "&" if "?" in base else "?"
    query = f"{separatore}flash={quote(messaggio)}&flash_tipo={tipo}"
    return RedirectResponse(url=f"{base}{query}{'#' + ancora if ancora else ''}", status_code=303)


def valore_gia_esistente(db: Session, modello, nome: str) -> bool:
    """Controllo duplicati (spazi/maiuscole ignorati) prima di inserire, per dare un
    errore chiaro invece di far esplodere il vincolo unique sul nome in database."""
    return db.query(modello).filter(func.lower(func.trim(modello.nome)) == nome.strip().lower()).first() is not None

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


@app.post("/condizioni_materiale", response_model=schemas.CondizioneMaterialeRead)
def create_condizione_materiale(condizione: schemas.CondizioneMaterialeCreate, db: Session = Depends(get_db)):
    nuovo = models.CondizioneMateriale(**condizione.model_dump())
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/condizioni_materiale", response_model=list[schemas.CondizioneMaterialeRead])
def leggi_condizioni_materiale(db: Session = Depends(get_db)):
    return db.query(models.CondizioneMateriale).all()


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


def genera_password_hash(password: str) -> str:
    salt = secrets.token_bytes(16)
    hash_password = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return salt.hex() + "$" + hash_password.hex()


@app.post("/utenti", response_model=schemas.UtenteRead)
def create_utente(utente: schemas.UtenteCreate, db: Session = Depends(get_db)):
    nuovo = models.Utente(**utente.model_dump(exclude={"password"}), password_hash=genera_password_hash(utente.password))
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/utenti", response_model=list[schemas.UtenteRead])
def leggi_utenti(db: Session = Depends(get_db)):
    return db.query(models.Utente).all()

def verifica_credenziali(email: str, password: str, db: Session) -> models.Utente | None:
    utente = db.query(models.Utente).filter(models.Utente.email == email).first()
    if utente is None:
        return None
    salt_hex, hash_hex = utente.password_hash.split("$")
    salt = bytes.fromhex(salt_hex)
    hash_atteso = bytes.fromhex(hash_hex)
    hash_calcolato = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    if not secrets.compare_digest(hash_calcolato, hash_atteso):
        return None
    return utente


@app.post("/login", response_model=schemas.UtenteRead)
def login(login_request: schemas.LoginRequest, db: Session = Depends(get_db)):
    utente = verifica_credenziali(login_request.email, login_request.password, db)
    if utente is None:
        raise HTTPException(status_code=401, detail="Credenziali non valide")
    return utente


# ponytail: sessioni in un dict in memoria di processo — si perdono a ogni
# riavvio del server e non funzionano con più processi/worker. Va bene per
# un solo utente/demo; se servirà login multi-processo o persistente,
# passare a un vero session store (es. tabella nel database).
sessioni: dict[str, int] = {}


def get_utente_da_sessione(request: Request, db: Session = Depends(get_db)) -> models.Utente:
    """Per pagine HTML: se non autenticato, redirige a /login invece di dare un 401 grezzo."""
    token = request.cookies.get("session_token")
    utente_id = sessioni.get(token) if token else None
    utente = db.query(models.Utente).filter(models.Utente.id == utente_id).first() if utente_id else None
    if utente is None:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    return utente


@app.get("/login")
def form_login(request: Request):
    return templates.TemplateResponse(request, "login.html", {"errore": None})


@app.post("/login-form")
def login_da_form(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    utente = verifica_credenziali(email, password, db)
    if utente is None:
        return templates.TemplateResponse(
            request, "login.html", {"errore": "Credenziali non valide"}, status_code=401
        )
    token = secrets.token_urlsafe(32)
    sessioni[token] = utente.id
    redirect = RedirectResponse(url="/magazzino", status_code=303)
    redirect.set_cookie(key="session_token", value=token, httponly=True)
    return redirect


@app.get("/logout")
def logout(request: Request):
    token = request.cookies.get("session_token")
    sessioni.pop(token, None)
    redirect = RedirectResponse(url="/login", status_code=303)
    redirect.delete_cookie("session_token")
    return redirect



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


@app.post("/movimenti", response_model=schemas.MovimentoRead)
def create_movimento(movimento: schemas.MovimentoCreate, db: Session = Depends(get_db)):
    return registra_movimento(movimento, db)

@app.post("/movimenti/nuovo")
def crea_movimento_da_form(
    request: Request,
    lotto_id: int = Form(...),
    posizione_partenza_id: str = Form(""),
    posizione_arrivo_id: int = Form(...),
    quantita_usata: float = Form(...),
    note: str = Form(""),
    condizione_id: str = Form(""),
    nota_partenza: str = Form(""),
    condizione_partenza_id: str = Form(""),
    db: Session = Depends(get_db),
    utente: models.Utente = Depends(get_utente_da_sessione),
):
    movimento = schemas.MovimentoCreate(
        lotto_id=lotto_id,
        posizione_partenza_id=int(posizione_partenza_id) if posizione_partenza_id else None,
        posizione_arrivo_id=posizione_arrivo_id,
        quantita_usata=quantita_usata,
        note=note or None,
        condizione_id=int(condizione_id) if condizione_id else None,
        nota_partenza=nota_partenza or None,
        condizione_partenza_id=int(condizione_partenza_id) if condizione_partenza_id else None,
    )
    try:
        registra_movimento(movimento, db)
    except HTTPException as errore:
        contesto = contesto_form_movimento(db, utente)
        contesto["errore"] = errore.detail
        return templates.TemplateResponse(request, "movimento_form.html", contesto, status_code=errore.status_code)
    return redirect_con_messaggio("/movimenti/nuovo", "Movimento registrato")


RigaGiacenza = tuple[int, Optional[int], Optional[str]]  # (posizione_id, condizione_id, note)


def righe_giacenza_lotto(lotto_id: int, db: Session) -> dict[RigaGiacenza, Decimal]:
    """Saldo del lotto per ogni combinazione (posizione, condizione, nota), sommando
    tutti i suoi movimenti (arrivi - partenze). Un lotto spostato solo in parte resta
    con un saldo anche nella posizione di partenza; una condizione o una nota diversa
    da quella di partenza genera una riga di giacenza distinta, anche nella stessa
    posizione (es. materiale rientrato "difettoso" non si somma a quello "nuovo" già
    presente lì)."""
    saldi: dict[RigaGiacenza, Decimal] = {}
    for m in db.query(models.Movimento).filter(models.Movimento.lotto_id == lotto_id).all():
        chiave_arrivo = (m.posizione_arrivo_id, m.condizione_id, m.note)
        saldi[chiave_arrivo] = saldi.get(chiave_arrivo, Decimal(0)) + m.quantita_usata
        if m.posizione_partenza_id is not None:
            chiave_partenza = (m.posizione_partenza_id, m.condizione_partenza_id, m.nota_partenza)
            saldi[chiave_partenza] = saldi.get(chiave_partenza, Decimal(0)) - m.quantita_usata
    return {chiave: q for chiave, q in saldi.items() if q > 0}


def registra_movimento(movimento: schemas.MovimentoCreate, db: Session):
    lotto = db.query(models.Lotto).filter(models.Lotto.id == movimento.lotto_id).first()
    if lotto is None:
        raise HTTPException(status_code=404, detail="Lotto non trovato")
    posizione_arrivo = db.query(models.Posizione).filter(models.Posizione.id == movimento.posizione_arrivo_id).first()
    if posizione_arrivo is None:
        raise HTTPException(status_code=404, detail="Posizione di arrivo non trovata")
    riga_partenza: RigaGiacenza = (movimento.posizione_partenza_id, movimento.condizione_partenza_id, movimento.nota_partenza)
    riga_arrivo: RigaGiacenza = (movimento.posizione_arrivo_id, movimento.condizione_id, movimento.note)
    if riga_partenza == riga_arrivo:
        raise HTTPException(status_code=400, detail="Partenza e arrivo coincidono (stessa posizione, condizione e nota): nessuna modifica da registrare")
    disponibile_qui = righe_giacenza_lotto(lotto.id, db).get(riga_partenza, Decimal(0))
    if disponibile_qui < Decimal(str(movimento.quantita_usata)):
        raise HTTPException(
            status_code=400,
            detail=f"In quella posizione di partenza sono disponibili solo {disponibile_qui}, non {movimento.quantita_usata}",
        )
    # Uno spostamento sposta solo la posizione: quantita_disponibile è
    # "quanto esiste ancora del lotto", non cambia per un semplice
    # trasferimento (a magazzino o a cantiere). Scenderà solo quando ci
    # sarà un'azione dedicata "segna come usato/consumato" (non ancora
    # costruita) — per ora un movimento non consuma nulla.
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

def contesto_form_movimento(db: Session, utente: models.Utente) -> dict:
    posizioni = db.query(models.Posizione).filter(models.Posizione.data_chiusura.is_(None)).all()
    condizioni = db.query(models.CondizioneMateriale).all()
    nomi_condizione = {c.id: c.nome for c in condizioni}
    lotti_per_posizione: dict[int, list[dict]] = {}
    for lotto in db.query(models.Lotto).filter(models.Lotto.quantita_disponibile > 0).all():
        for (posizione_id, condizione_id, note), quantita in righe_giacenza_lotto(lotto.id, db).items():
            lotti_per_posizione.setdefault(posizione_id, []).append({
                "lotto_id": lotto.id,
                "materiale": lotto.materiale.nome,
                "quantita_disponibile": float(quantita),
                "unita_misura": lotto.materiale.unita_misura.nome,
                "bolla": lotto.bolla.numero,
                "condizione_id": condizione_id,
                "condizione": nomi_condizione.get(condizione_id),
                "note": note,
            })
    return {
        "posizioni": posizioni,
        "condizioni": condizioni,
        "lotti_per_posizione_json": json.dumps(lotti_per_posizione),
        "utente": utente,
        "errore": None,
    }


@app.get("/movimenti/nuovo")
def form_movimento(request: Request, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    return templates.TemplateResponse(request, "movimento_form.html", contesto_form_movimento(db, utente))


@app.get("/prova")
def pagina_prova(request: Request):
    return templates.TemplateResponse(request, "prova.html", {"messaggio": "Funziona!"})

@app.get("/magazzino")
def pagina_magazzino(request: Request, posizione_id: str = "", db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    tutte_posizioni = {p.id: p for p in db.query(models.Posizione).all()}
    tutte_condizioni = {c.id: c for c in db.query(models.CondizioneMateriale).all()}
    righe = []
    for lotto in db.query(models.Lotto).all():
        saldi = righe_giacenza_lotto(lotto.id, db)
        if not saldi:
            righe.append({"lotto": lotto, "quantita": lotto.quantita_disponibile, "posizione": None, "condizione": None, "note": None})
            continue
        for (pid, condizione_id, note), quantita in saldi.items():
            righe.append({
                "lotto": lotto,
                "quantita": quantita,
                "posizione": tutte_posizioni.get(pid),
                "condizione": tutte_condizioni.get(condizione_id),
                "note": note,
            })
    for riga in righe:
        riga["sotto_soglia"] = float(riga["quantita"]) < float(riga["lotto"].quantita_iniziale) * 0.2
    posizioni = db.query(models.Posizione).all()
    posizione_selezionata = None
    if posizione_id:
        posizione_selezionata = db.query(models.Posizione).filter(models.Posizione.id == int(posizione_id)).first()
        righe = [r for r in righe if r["posizione"] and r["posizione"].id == int(posizione_id)]
    return templates.TemplateResponse(request, "magazzino.html", {
        "righe": righe,
        "posizioni": posizioni,
        "posizione_selezionata": posizione_selezionata,
        "utente": utente,
    })

def _lotti_per_bolla(db: Session) -> dict[int, list[models.Lotto]]:
    lotti_per_bolla: dict[int, list[models.Lotto]] = {}
    for lotto in db.query(models.Lotto).all():
        lotto.condizione_iniziale = condizione_iniziale_lotto(lotto.id, db)
        lotti_per_bolla.setdefault(lotto.bolla_id, []).append(lotto)
    return lotti_per_bolla


def data_limite_archivio() -> datetime:
    """12 mesi esatti fa da oggi (le bolle più vecchie di questa data vanno in archivio)."""
    oggi = datetime.now()
    try:
        return oggi.replace(year=oggi.year - 1)
    except ValueError:
        # 29 febbraio in un anno non bisestile un anno fa: un giorno prima
        return oggi.replace(year=oggi.year - 1, day=oggi.day - 1)


@app.get("/bolle-elenco")
def pagina_bolle(request: Request, anno: str = "", db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    limite = data_limite_archivio()
    bolle = db.query(models.Bolla).filter(models.Bolla.data >= limite).all()
    anni_disponibili = sorted({b.data.year for b in db.query(models.Bolla).all() if b.data}, reverse=True)
    if anno:
        bolle = [b for b in bolle if b.data and b.data.year == int(anno)]
    bolle = sorted(bolle, key=lambda b: b.numero.lower())
    return templates.TemplateResponse(request, "bolle.html", {
        "bolle": bolle,
        "lotti_per_bolla": _lotti_per_bolla(db),
        "anni_disponibili": anni_disponibili,
        "anno_selezionato": anno,
        "utente": utente,
    })


@app.get("/archivio/bolle")
def pagina_archivio_bolle(request: Request, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    limite = data_limite_archivio()
    bolle = [b for b in db.query(models.Bolla).all() if b.data and b.data < limite]
    bolle = sorted(bolle, key=lambda b: b.numero.lower())
    return templates.TemplateResponse(request, "archivio.html", {
        "bolle": bolle,
        "lotti_per_bolla": _lotti_per_bolla(db),
        "utente": utente,
    })


@app.get("/archivio/posizioni")
def pagina_archivio_posizioni(request: Request, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    posizioni_chiuse = db.query(models.Posizione).filter(models.Posizione.data_chiusura.isnot(None)).all()
    return templates.TemplateResponse(request, "archivio_posizioni.html", {"posizioni": posizioni_chiuse, "utente": utente})

# Anagrafiche semplici (solo nome): un endpoint generico invece di N copie identiche

TABELLE_ANAGRAFICHE_SEMPLICI = {
    "ruolo": ("Ruoli", models.Ruolo),
    "condizione_materiale": ("Condizioni materiale", models.CondizioneMateriale),
    "tipo_posizione": ("Tipi posizione", models.TipoPosizione),
    "unita_misura": ("Unità di misura", models.UnitaMisura),
}


def costruisci_gruppi_anagrafiche(db: Session) -> list[dict]:
    return [
        {"chiave": chiave, "etichetta": etichetta, "elementi": db.query(Modello).all()}
        for chiave, (etichetta, Modello) in TABELLE_ANAGRAFICHE_SEMPLICI.items()
    ]


@app.get("/anagrafiche")
def pagina_anagrafiche(request: Request, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    return templates.TemplateResponse(request, "anagrafiche.html", {"gruppi": costruisci_gruppi_anagrafiche(db), "utente": utente, "errore": None, "gruppo_attivo": None})


@app.post("/anagrafiche/{tipo}")
def crea_anagrafica_semplice(
    request: Request,
    tipo: str,
    nome: str = Form(...),
    db: Session = Depends(get_db),
    utente: models.Utente = Depends(get_utente_da_sessione),
):
    voce = TABELLE_ANAGRAFICHE_SEMPLICI.get(tipo)
    if voce is None:
        raise HTTPException(status_code=404, detail="Tipo anagrafica sconosciuto")
    etichetta, Modello = voce
    nome = nome.strip()
    if valore_gia_esistente(db, Modello, nome):
        return templates.TemplateResponse(
            request, "anagrafiche.html",
            {
                "gruppi": costruisci_gruppi_anagrafiche(db), "utente": utente,
                "errore": f'"{nome}" esiste già in {etichetta.lower()}',
                "gruppo_attivo": tipo,
            },
            status_code=400,
        )
    db.add(Modello(nome=nome))
    db.commit()
    return redirect_con_messaggio(f"/anagrafiche#gruppo-{tipo}", f'"{nome}" aggiunto a {etichetta.lower()}')



@app.get("/fornitori/nuovo")
def form_fornitore(request: Request, utente: models.Utente = Depends(get_utente_da_sessione)):
    return templates.TemplateResponse(request, "fornitore_form.html", {"utente": utente})


@app.post("/fornitori/nuovo")
def crea_fornitore_da_form(
    nome: str = Form(...),
    email_generale: str = Form(""),
    email_commerciale: str = Form(""),
    email_tecnico: str = Form(""),
    email_amministrazione: str = Form(""),
    telefono_fisso: str = Form(""),
    cellulare_1: str = Form(""),
    cellulare_2: str = Form(""),
    referente_1: str = Form(""),
    referente_2: str = Form(""),
    db: Session = Depends(get_db),
    utente: models.Utente = Depends(get_utente_da_sessione),
):
    nuovo = models.Fornitore(
        nome=nome,
        email_generale=email_generale or None,
        email_commerciale=email_commerciale or None,
        email_tecnico=email_tecnico or None,
        email_amministrazione=email_amministrazione or None,
        telefono_fisso=telefono_fisso or None,
        cellulare_1=cellulare_1 or None,
        cellulare_2=cellulare_2 or None,
        referente_1=referente_1 or None,
        referente_2=referente_2 or None,
    )
    db.add(nuovo)
    db.commit()
    return redirect_con_messaggio("/fornitori/nuovo", "Fornitore aggiunto")


@app.get("/fornitori/{fornitore_id}")
def pagina_fornitore(fornitore_id: int, request: Request, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    fornitore = db.query(models.Fornitore).filter(models.Fornitore.id == fornitore_id).first()
    if fornitore is None:
        raise HTTPException(status_code=404, detail="Fornitore non trovato")
    materiali = db.query(models.Materiale).filter(models.Materiale.fornitore_id == fornitore_id).all()
    return templates.TemplateResponse(request, "fornitore_dettaglio.html", {"fornitore": fornitore, "materiali": materiali, "utente": utente})



@app.post("/posizioni/nuovo")
def crea_posizione_da_form(
    nome: str = Form(...),
    indirizzo: str = Form(""),
    tipo_posizione_id: int = Form(...),
    db: Session = Depends(get_db),
    utente: models.Utente = Depends(get_utente_da_sessione),
):
    nuovo = models.Posizione(nome=nome.strip(), indirizzo=indirizzo.strip() or None, tipo_posizione_id=tipo_posizione_id)
    db.add(nuovo)
    db.commit()
    return redirect_con_messaggio("/posizioni-elenco", "Posizione aggiunta")


@app.get("/posizioni-elenco")
def pagina_posizioni(request: Request, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    posizioni = db.query(models.Posizione).filter(models.Posizione.data_chiusura.is_(None)).all()
    tipi = db.query(models.TipoPosizione).all()
    return templates.TemplateResponse(request, "posizioni_elenco.html", {"posizioni": posizioni, "tipi": tipi, "utente": utente})


@app.post("/posizioni/{posizione_id}/chiudi")
def chiudi_posizione(posizione_id: int, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    posizione = db.query(models.Posizione).filter(models.Posizione.id == posizione_id).first()
    if posizione is None:
        raise HTTPException(status_code=404, detail="Posizione non trovata")
    posizione.data_chiusura = datetime.now()
    db.commit()
    return redirect_con_messaggio("/posizioni-elenco", "Posizione chiusa")


@app.post("/posizioni/{posizione_id}/riapri")
def riapri_posizione(posizione_id: int, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    posizione = db.query(models.Posizione).filter(models.Posizione.id == posizione_id).first()
    if posizione is None:
        raise HTTPException(status_code=404, detail="Posizione non trovata")
    posizione.data_chiusura = None
    db.commit()
    return redirect_con_messaggio("/archivio/posizioni", "Posizione riaperta")



@app.get("/materiali/nuovo")
def form_materiale(request: Request, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    fornitori = db.query(models.Fornitore).all()
    unita = db.query(models.UnitaMisura).all()
    return templates.TemplateResponse(request, "materiale_form.html", {"fornitori": fornitori, "unita": unita, "utente": utente})


@app.post("/materiali/nuovo")
def crea_materiale_da_form(
    nome: str = Form(...),
    fornitore_id: int = Form(...),
    unita_misura_id: int = Form(...),
    db: Session = Depends(get_db),
    utente: models.Utente = Depends(get_utente_da_sessione),
):
    nuovo = models.Materiale(nome=nome, fornitore_id=fornitore_id, unita_misura_id=unita_misura_id)
    db.add(nuovo)
    db.commit()
    return redirect_con_messaggio("/materiali/nuovo", "Materiale aggiunto")



@app.get("/bolle/nuovo")
def form_bolla(request: Request, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    fornitori = db.query(models.Fornitore).all()
    return templates.TemplateResponse(request, "bolla_form.html", {"fornitori": fornitori, "utente": utente})


@app.post("/bolle/nuovo")
def crea_bolla_da_form(
    fornitore_id: int = Form(...),
    numero: str = Form(...),
    numero_ordine_riferimento: str = Form(""),
    data: str = Form(""),
    firmatario: str = Form(""),
    operatori_scarico: str = Form(""),
    db: Session = Depends(get_db),
    utente: models.Utente = Depends(get_utente_da_sessione),
):
    nuova_bolla = models.Bolla(
        fornitore_id=fornitore_id,
        numero=numero,
        numero_ordine_riferimento=numero_ordine_riferimento or None,
        data=datetime.strptime(data, "%Y-%m-%d") if data else datetime.now(),
        firmatario=firmatario or None,
        operatori_scarico=operatori_scarico or None,
    )
    db.add(nuova_bolla)
    db.commit()
    db.refresh(nuova_bolla)
    return redirect_con_messaggio(f"/bolle/{nuova_bolla.id}/lotti/nuovo", "Bolla creata, ora aggiungi i materiali")



@app.get("/bolle/{bolla_id}/lotti/nuovo")
def form_lotto(bolla_id: int, request: Request, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    bolla = db.query(models.Bolla).filter(models.Bolla.id == bolla_id).first()
    if bolla is None:
        raise HTTPException(status_code=404, detail="Bolla non trovata")
    materiali = db.query(models.Materiale).filter(models.Materiale.fornitore_id == bolla.fornitore_id).all()
    condizioni = db.query(models.CondizioneMateriale).all()
    magazzini = (
        db.query(models.Posizione)
        .join(models.TipoPosizione)
        .filter(func.lower(func.trim(models.TipoPosizione.nome)) == "magazzino", models.Posizione.data_chiusura.is_(None))
        .all()
    )
    lotti_aggiunti = db.query(models.Lotto).filter(models.Lotto.bolla_id == bolla_id).all()
    for lotto in lotti_aggiunti:
        lotto.condizione_iniziale = condizione_iniziale_lotto(lotto.id, db)
    return templates.TemplateResponse(request, "lotto_form.html", {
        "bolla": bolla, "materiali": materiali, "condizioni": condizioni, "magazzini": magazzini,
        "lotti_aggiunti": lotti_aggiunti, "utente": utente,
    })


@app.post("/bolle/{bolla_id}/lotti/nuovo")
def crea_lotto_da_form(
    bolla_id: int,
    materiale_id: int = Form(...),
    quantita_iniziale: float = Form(...),
    condizione_id: int = Form(...),
    posizione_iniziale_id: int = Form(...),
    db: Session = Depends(get_db),
    utente: models.Utente = Depends(get_utente_da_sessione),
):
    nuovo = models.Lotto(
        bolla_id=bolla_id,
        materiale_id=materiale_id,
        quantita_iniziale=quantita_iniziale,
        quantita_disponibile=quantita_iniziale,
    )
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    # Movimento "di arrivo" creato a mano (non con registra_movimento): la
    # quantita_disponibile è già quantita_iniziale dalla creazione del lotto,
    # quindi passare da registra_movimento la sommerebbe una seconda volta.
    # Qui serve solo a dare al lotto una posizione e una condizione iniziali.
    primo_movimento = models.Movimento(
        lotto_id=nuovo.id,
        posizione_partenza_id=None,
        posizione_arrivo_id=posizione_iniziale_id,
        quantita_usata=quantita_iniziale,
        data_movimento=datetime.now(),
        note="Arrivo iniziale in magazzino",
        condizione_id=condizione_id,
    )
    db.add(primo_movimento)
    db.commit()
    return redirect_con_messaggio(f"/bolle/{bolla_id}/lotti/nuovo", "Materiale aggiunto alla bolla")


def condizione_iniziale_lotto(lotto_id: int, db: Session) -> models.CondizioneMateriale | None:
    """Condizione registrata sul primo movimento del lotto (l'arrivo)."""
    primo = (
        db.query(models.Movimento)
        .filter(models.Movimento.lotto_id == lotto_id, models.Movimento.posizione_partenza_id.is_(None))
        .order_by(models.Movimento.id.asc())
        .first()
    )
    return primo.condizione if primo else None



@app.get("/storico")
def pagina_storico(request: Request, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    movimenti = (
        db.query(models.Movimento)
        .order_by(models.Movimento.data_movimento.desc(), models.Movimento.id.desc())
        .all()
    )
    return templates.TemplateResponse(request, "storico.html", {"movimenti": movimenti, "utente": utente})



def richiedi_amministratore(utente: models.Utente):
    if utente.ruolo.nome != "Amministratore":
        raise HTTPException(status_code=403, detail="Solo un amministratore può farlo")


@app.get("/utenti/nuovo")
def form_nuovo_utente(request: Request, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    richiedi_amministratore(utente)
    ruoli = db.query(models.Ruolo).all()
    return templates.TemplateResponse(request, "utente_form.html", {"ruoli": ruoli, "utente": utente, "errore": None})


@app.post("/utenti/nuovo")
def crea_utente_da_form(
    request: Request,
    nome: str = Form(...),
    cognome: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    ruolo_id: int = Form(...),
    db: Session = Depends(get_db),
    utente: models.Utente = Depends(get_utente_da_sessione),
):
    richiedi_amministratore(utente)
    if db.query(models.Utente).filter(models.Utente.email == email).first() is not None:
        ruoli = db.query(models.Ruolo).all()
        return templates.TemplateResponse(
            request, "utente_form.html",
            {"ruoli": ruoli, "utente": utente, "errore": "Esiste già un account con questa email"},
            status_code=400,
        )
    nuovo = models.Utente(
        nome=nome, cognome=cognome, email=email,
        password_hash=genera_password_hash(password), ruolo_id=ruolo_id,
    )
    db.add(nuovo)
    db.commit()
    return redirect_con_messaggio("/utenti/nuovo", "Utente creato")



@app.get("/cambia-password")
def form_cambia_password(request: Request, utente: models.Utente = Depends(get_utente_da_sessione)):
    return templates.TemplateResponse(request, "cambia_password.html", {"utente": utente, "errore": None})


@app.post("/cambia-password")
def cambia_password(
    request: Request,
    password_attuale: str = Form(...),
    password_nuova: str = Form(...),
    db: Session = Depends(get_db),
    utente: models.Utente = Depends(get_utente_da_sessione),
):
    if verifica_credenziali(utente.email, password_attuale, db) is None:
        return templates.TemplateResponse(
            request, "cambia_password.html",
            {"utente": utente, "errore": "Password attuale errata"},
            status_code=400,
        )
    utente.password_hash = genera_password_hash(password_nuova)
    db.commit()
    return redirect_con_messaggio("/cambia-password", "Password aggiornata")
