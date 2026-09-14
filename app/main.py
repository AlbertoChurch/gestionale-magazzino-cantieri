from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError

from app import models, schemas
from app.database import get_db

import hashlib, secrets, os
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
    return JSONResponse(status_code=409, content={"detail": "Operazione non consentita: valore duplicato, dato non valido, oppure elemento ancora collegato ad altri dati."})


def redirect_con_messaggio(url: str, messaggio: str, tipo: str = "ok") -> RedirectResponse:
    """Redirect che porta con sé un messaggio da mostrare come popup nella pagina di arrivo.
    La query va inserita prima dell'eventuale #ancora, non dopo (altrimenti finisce dentro
    il fragment e il browser non la considera più query string)."""
    base, _, ancora = url.partition("#")
    separatore = "&" if "?" in base else "?"
    query = f"{separatore}flash={quote(messaggio)}&flash_tipo={tipo}"
    return RedirectResponse(url=f"{base}{query}{'#' + ancora if ancora else ''}", status_code=303)


def valore_gia_esistente(db: Session, modello, nome: str, escludi_id: int | None = None) -> bool:
    """Controllo duplicati (spazi/maiuscole ignorati) prima di inserire o modificare, per
    dare un errore chiaro invece di far esplodere il vincolo unique sul nome in database."""
    query = db.query(modello).filter(func.lower(func.trim(modello.nome)) == nome.strip().lower())
    if escludi_id is not None:
        query = query.filter(modello.id != escludi_id)
    return query.first() is not None


def elemento_in_uso(db: Session, *condizioni) -> bool:
    """True se una qualsiasi delle query passate (una per tabella che potrebbe
    referenziare l'elemento) trova almeno una riga."""
    return any(db.query(modello).filter(condizione).first() is not None for modello, condizione in condizioni)


# ponytail: sessioni in un dict in memoria di processo — si perdono a ogni
# riavvio del server e non funzionano con più processi/worker. Va bene per
# un solo utente/demo; se servirà login multi-processo o persistente,
# passare a un vero session store (es. tabella nel database).
sessioni: dict[str, int] = {}


def get_utente_da_sessione(request: Request, db: Session = Depends(get_db)) -> models.Utente:
    """Per pagine HTML e per gli endpoint JSON: se non autenticato, redirige a /login
    (le pagine) o dà un 401 (le chiamate JSON, che non seguono redirect)."""
    token = request.cookies.get("session_token")
    utente_id = sessioni.get(token) if token else None
    utente = db.query(models.Utente).filter(models.Utente.id == utente_id).first() if utente_id else None
    if utente is None:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    return utente


def richiedi_amministratore(utente: models.Utente):
    if utente.ruolo.nome != "Amministratore":
        raise HTTPException(status_code=403, detail="Solo un amministratore può farlo")


@app.get("/")
async def root():
    return {"status": "ok", "messaggio": "Gestionale attivo"}


@app.post("/fornitori", response_model=schemas.FornitoreRead)
def create_fornitore(fornitore: schemas.FornitoreCreate, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    nuovo = models.Fornitore(**fornitore.model_dump())
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/fornitori", response_model=list[schemas.FornitoreRead])
def leggi_fornitori(db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    return db.query(models.Fornitore).all()


@app.post("/posizioni", response_model=schemas.PosizioneRead)
def create_posizione(posizione: schemas.PosizioneCreate, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    nuovo = models.Posizione(**posizione.model_dump())
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/posizioni", response_model=list[schemas.PosizioneRead])
def leggi_posizioni(db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    return db.query(models.Posizione).all()


@app.post("/tipo_posizioni", response_model=schemas.TipoPosizioneRead)
def create_tipo_posizione(tipo_posizione: schemas.TipoPosizioneCreate, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    nuovo = models.TipoPosizione(**tipo_posizione.model_dump())
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/tipo_posizioni", response_model=list[schemas.TipoPosizioneRead])
def leggi_tipo_posizioni(db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    return db.query(models.TipoPosizione).all()


@app.post("/ruoli", response_model=schemas.RuoloRead)
def create_ruoli(ruolo: schemas.RuoloCreate, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    richiedi_amministratore(utente)
    nuovo = models.Ruolo(**ruolo.model_dump())
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/ruoli", response_model=list[schemas.RuoloRead])
def leggi_ruoli(db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    return db.query(models.Ruolo).all()


@app.post("/unita_misura", response_model=schemas.UnitaMisuraRead)
def create_unita_misura(unita_misura: schemas.UnitaMisuraCreate, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    nuovo = models.UnitaMisura(**unita_misura.model_dump())
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/unita_misura", response_model=list[schemas.UnitaMisuraRead])
def leggi_unita_misura(db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    return db.query(models.UnitaMisura).all()


@app.post("/tipo_materiali", response_model=schemas.TipoMaterialeRead)
def create_tipo_materiali(tipo_materiale: schemas.TipoMaterialeCreate, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    nuovo = models.TipoMateriale(**tipo_materiale.model_dump())
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/tipo_materiali", response_model=list[schemas.TipoMaterialeRead])
def leggi_tipo_materiali(db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    return db.query(models.TipoMateriale).all()


@app.post("/condizioni_materiale", response_model=schemas.CondizioneMaterialeRead)
def create_condizione_materiale(condizione: schemas.CondizioneMaterialeCreate, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    nuovo = models.CondizioneMateriale(**condizione.model_dump())
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/condizioni_materiale", response_model=list[schemas.CondizioneMaterialeRead])
def leggi_condizioni_materiale(db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    return db.query(models.CondizioneMateriale).all()


@app.post("/materiali", response_model=schemas.MaterialeRead)
def create_materiale(materiale: schemas.MaterialeCreate, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    tipi = db.query(models.TipoMateriale).filter(models.TipoMateriale.id.in_(materiale.tipo_materiale_ids)).all()
    nuovo = models.Materiale(**materiale.model_dump(exclude={"tipo_materiale_ids"}))
    db.add(nuovo)
    nuovo.tipi_materiale = tipi
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/materiali", response_model=list[schemas.MaterialeRead])
def leggi_materiali(db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    return db.query(models.Materiale).all()


def genera_password_hash(password: str) -> str:
    salt = secrets.token_bytes(16)
    hash_password = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return salt.hex() + "$" + hash_password.hex()


@app.post("/utenti", response_model=schemas.UtenteRead)
def create_utente(utente: schemas.UtenteCreate, db: Session = Depends(get_db), utente_sessione: models.Utente = Depends(get_utente_da_sessione)):
    richiedi_amministratore(utente_sessione)
    nuovo = models.Utente(**utente.model_dump(exclude={"password"}), password_hash=genera_password_hash(utente.password))
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/utenti", response_model=list[schemas.UtenteRead])
def leggi_utenti(db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    richiedi_amministratore(utente)
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
def create_bolla(bolla: schemas.BollaCreate, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    dati = bolla.model_dump()
    if dati["data"] is None:
        dati["data"] = datetime.now()
    nuovo = models.Bolla(**dati)
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/bolle", response_model=list[schemas.BollaRead])
def leggi_bolle(db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    return db.query(models.Bolla).all()


@app.post("/lotti", response_model=schemas.LottoRead)
def create_lotto(lotto: schemas.LottoCreate, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    dati = lotto.model_dump()
    dati["quantita_disponibile"] = dati["quantita_iniziale"]
    nuovo = models.Lotto(**dati)
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@app.get("/lotti", response_model=list[schemas.LottoRead])
def leggi_lotti(db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    return db.query(models.Lotto).all()


@app.post("/movimenti", response_model=schemas.MovimentoRead)
def create_movimento(movimento: schemas.MovimentoCreate, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
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
    except IntegrityError:
        db.rollback()
        contesto = contesto_form_movimento(db, utente)
        contesto["errore"] = "Dato non più valido (es. condizione o posizione nel frattempo eliminata): riprova."
        return templates.TemplateResponse(request, "movimento_form.html", contesto, status_code=400)
    return redirect_con_messaggio("/movimenti/nuovo", "Movimento registrato")


RigaGiacenza = tuple[int, Optional[int], Optional[str]]  # (posizione_id, condizione_id, note)


def righe_giacenza_da_movimenti(movimenti) -> dict[RigaGiacenza, Decimal]:
    """Saldo per ogni combinazione (posizione, condizione, nota) a partire da una lista
    di movimenti già in memoria (usata sia per le Giacenze vere, sia per simulare
    'cosa succederebbe se' prima di modificare/eliminare un movimento passato)."""
    saldi: dict[RigaGiacenza, Decimal] = {}
    for m in movimenti:
        quantita = Decimal(str(m.quantita_usata))
        chiave_arrivo = (m.posizione_arrivo_id, m.condizione_id, m.note)
        saldi[chiave_arrivo] = saldi.get(chiave_arrivo, Decimal(0)) + quantita
        if m.posizione_partenza_id is not None:
            chiave_partenza = (m.posizione_partenza_id, m.condizione_partenza_id, m.nota_partenza)
            saldi[chiave_partenza] = saldi.get(chiave_partenza, Decimal(0)) - quantita
    return saldi


def replay_giacenza_valido(movimenti) -> bool:
    """Ripercorre i movimenti in ordine cronologico e controlla che nessuna giacenza sia
    MAI andata negativa in nessun momento della storia. Non basta controllare il saldo
    finale: un prelievo può risultare "coperto" solo da un arrivo successivo nel tempo,
    il che vorrebbe dire che in quel momento la giacenza reale era negativa —
    fisicamente impossibile, anche se il totale di oggi torna."""
    ordinati = sorted(movimenti, key=lambda m: (m.data_movimento or datetime.min, m.id))
    saldi: dict[RigaGiacenza, Decimal] = {}
    for m in ordinati:
        quantita = Decimal(str(m.quantita_usata))
        if m.posizione_partenza_id is not None:
            chiave_partenza = (m.posizione_partenza_id, m.condizione_partenza_id, m.nota_partenza)
            nuovo_saldo = saldi.get(chiave_partenza, Decimal(0)) - quantita
            if nuovo_saldo < 0:
                return False
            saldi[chiave_partenza] = nuovo_saldo
        chiave_arrivo = (m.posizione_arrivo_id, m.condizione_id, m.note)
        saldi[chiave_arrivo] = saldi.get(chiave_arrivo, Decimal(0)) + quantita
    return True


def righe_giacenza_lotto(lotto_id: int, db: Session) -> dict[RigaGiacenza, Decimal]:
    """Saldo del lotto per ogni combinazione (posizione, condizione, nota), sommando
    tutti i suoi movimenti (arrivi - partenze). Un lotto spostato solo in parte resta
    con un saldo anche nella posizione di partenza; una condizione o una nota diversa
    da quella di partenza genera una riga di giacenza distinta, anche nella stessa
    posizione (es. materiale rientrato "difettoso" non si somma a quello "nuovo" già
    presente lì)."""
    movimenti = db.query(models.Movimento).filter(models.Movimento.lotto_id == lotto_id).all()
    saldi = righe_giacenza_da_movimenti(movimenti)
    return {chiave: q for chiave, q in saldi.items() if q > 0}


def posizione_ha_giacenza(db: Session, posizione_id: int) -> bool:
    """True se un qualsiasi lotto ha ancora del materiale fisicamente in questa posizione."""
    for lotto in db.query(models.Lotto).filter(models.Lotto.quantita_disponibile > 0).all():
        for (pid, _, _) in righe_giacenza_lotto(lotto.id, db):
            if pid == posizione_id:
                return True
    return False


def modifica_movimento_sicura(db: Session, movimento: "models.Movimento", quantita_usata: float, condizione_id: Optional[int], note: Optional[str], data_movimento: Optional[datetime]) -> Optional[str]:
    """Applica le modifiche e le committa SOLO se nessuna giacenza del lotto risulta
    negativa dopo il cambiamento (es. un movimento successivo che prelevava proprio da
    qui). In caso contrario annulla tutto e ritorna un messaggio d'errore."""
    movimento.quantita_usata = quantita_usata
    movimento.condizione_id = condizione_id
    movimento.note = note
    if data_movimento is not None:
        movimento.data_movimento = data_movimento
    db.flush()
    tutti = db.query(models.Movimento).filter(models.Movimento.lotto_id == movimento.lotto_id).all()
    if not replay_giacenza_valido(tutti):
        db.rollback()
        return "Questa modifica lascerebbe una giacenza negativa in un certo momento della storia: probabilmente un movimento successivo dipende dalla quantità che aveva spostato questo. Correggi prima quello."
    if movimento.posizione_partenza_id is None:
        # è l'arrivo iniziale del lotto: la quantità totale esistente segue quella del movimento
        movimento.lotto.quantita_iniziale = quantita_usata
        movimento.lotto.quantita_disponibile = quantita_usata
    db.commit()
    return None


def elimina_movimento_sicuro(db: Session, movimento: "models.Movimento") -> Optional[str]:
    """Elimina il movimento SOLO se non lascia nessuna giacenza negativa e non è
    l'arrivo iniziale di un lotto (quello è legato alla creazione del lotto stesso,
    non gestibile con una semplice eliminazione)."""
    if movimento.posizione_partenza_id is None:
        return "Non è possibile eliminare il movimento di arrivo iniziale di un lotto."
    lotto_id = movimento.lotto_id
    db.delete(movimento)
    db.flush()
    tutti = db.query(models.Movimento).filter(models.Movimento.lotto_id == lotto_id).all()
    if not replay_giacenza_valido(tutti):
        db.rollback()
        return "Non è possibile eliminare questo movimento: un movimento successivo dipende dalla quantità che aveva spostato."
    db.commit()
    return None


def registra_movimento(movimento: schemas.MovimentoCreate, db: Session):
    if movimento.quantita_usata <= 0:
        raise HTTPException(status_code=400, detail="La quantità deve essere maggiore di zero")
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
def leggi_movimenti(db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
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
        "lotti_per_posizione": lotti_per_posizione,
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
    try:
        id_posizione_filtro = int(posizione_id) if posizione_id else None
    except ValueError:
        id_posizione_filtro = None
    if id_posizione_filtro is not None:
        posizione_selezionata = db.query(models.Posizione).filter(models.Posizione.id == id_posizione_filtro).first()
        righe = [r for r in righe if r["posizione"] and r["posizione"].id == id_posizione_filtro]
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
    if anno.isdigit():
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

CONTROLLI_USO_ANAGRAFICHE = {
    "ruolo": lambda db, id_: elemento_in_uso(db, (models.Utente, models.Utente.ruolo_id == id_)),
    "condizione_materiale": lambda db, id_: elemento_in_uso(
        db,
        (models.Movimento, or_(models.Movimento.condizione_id == id_, models.Movimento.condizione_partenza_id == id_)),
    ),
    "tipo_posizione": lambda db, id_: elemento_in_uso(db, (models.Posizione, models.Posizione.tipo_posizione_id == id_)),
    "unita_misura": lambda db, id_: elemento_in_uso(db, (models.Materiale, models.Materiale.unita_misura_id == id_)),
}
assert set(CONTROLLI_USO_ANAGRAFICHE) == set(TABELLE_ANAGRAFICHE_SEMPLICI), (
    "Ogni voce di TABELLE_ANAGRAFICHE_SEMPLICI deve avere un controllo 'in uso' corrispondente, "
    "altrimenti l'eliminazione di quel tipo non controlla nulla."
)


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
    if tipo == "ruolo":
        richiedi_amministratore(utente)
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


@app.post("/anagrafiche/{tipo}/{elemento_id}/modifica")
def modifica_anagrafica_semplice(
    request: Request,
    tipo: str,
    elemento_id: int,
    nome: str = Form(...),
    db: Session = Depends(get_db),
    utente: models.Utente = Depends(get_utente_da_sessione),
):
    voce = TABELLE_ANAGRAFICHE_SEMPLICI.get(tipo)
    if voce is None:
        raise HTTPException(status_code=404, detail="Tipo anagrafica sconosciuto")
    if tipo == "ruolo":
        richiedi_amministratore(utente)
    etichetta, Modello = voce
    elemento = db.query(Modello).filter(Modello.id == elemento_id).first()
    if elemento is None:
        raise HTTPException(status_code=404, detail="Elemento non trovato")
    nome = nome.strip()
    if valore_gia_esistente(db, Modello, nome, escludi_id=elemento_id):
        return templates.TemplateResponse(
            request, "anagrafiche.html",
            {
                "gruppi": costruisci_gruppi_anagrafiche(db), "utente": utente,
                "errore": f'"{nome}" esiste già in {etichetta.lower()}',
                "gruppo_attivo": tipo,
            },
            status_code=400,
        )
    elemento.nome = nome
    db.commit()
    return redirect_con_messaggio(f"/anagrafiche#gruppo-{tipo}", f'"{nome}" modificato')


@app.post("/anagrafiche/{tipo}/{elemento_id}/elimina")
def elimina_anagrafica_semplice(
    tipo: str,
    elemento_id: int,
    db: Session = Depends(get_db),
    utente: models.Utente = Depends(get_utente_da_sessione),
):
    voce = TABELLE_ANAGRAFICHE_SEMPLICI.get(tipo)
    if voce is None:
        raise HTTPException(status_code=404, detail="Tipo anagrafica sconosciuto")
    if tipo == "ruolo":
        richiedi_amministratore(utente)
    _, Modello = voce
    elemento = db.query(Modello).filter(Modello.id == elemento_id).first()
    if elemento is None:
        raise HTTPException(status_code=404, detail="Elemento non trovato")
    controllo = CONTROLLI_USO_ANAGRAFICHE.get(tipo)
    if controllo and controllo(db, elemento_id):
        return redirect_con_messaggio(f"/anagrafiche#gruppo-{tipo}", "Non è possibile eliminare questo elemento perché già in uso", tipo="avviso")
    nome = elemento.nome
    db.delete(elemento)
    db.commit()
    return redirect_con_messaggio(f"/anagrafiche#gruppo-{tipo}", f'"{nome}" eliminato')



def _campi_fornitore_form(
    nome: str = Form(...),
    descrizione: str = Form(""),
    email_generale: str = Form(""),
    email_commerciale: str = Form(""),
    email_tecnico: str = Form(""),
    email_amministrazione: str = Form(""),
    telefono_fisso: str = Form(""),
    cellulare_1: str = Form(""),
    cellulare_2: str = Form(""),
    referente_1: str = Form(""),
    referente_2: str = Form(""),
) -> dict:
    return dict(
        nome=nome.strip(),
        descrizione=descrizione.strip() or None,
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


@app.get("/fornitori/nuovo")
def form_fornitore(request: Request, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    fornitori = db.query(models.Fornitore).all()
    return templates.TemplateResponse(request, "fornitore_form.html", {"utente": utente, "fornitori": fornitori, "fornitore": None, "errore": None})


@app.post("/fornitori/nuovo")
def crea_fornitore_da_form(
    request: Request,
    campi: dict = Depends(_campi_fornitore_form),
    db: Session = Depends(get_db),
    utente: models.Utente = Depends(get_utente_da_sessione),
):
    if valore_gia_esistente(db, models.Fornitore, campi["nome"]):
        fornitori = db.query(models.Fornitore).all()
        return templates.TemplateResponse(
            request, "fornitore_form.html",
            {"utente": utente, "fornitori": fornitori, "fornitore": None, "errore": f'"{campi["nome"]}" esiste già'},
            status_code=400,
        )
    db.add(models.Fornitore(**campi))
    db.commit()
    return redirect_con_messaggio("/fornitori/nuovo", "Fornitore aggiunto")


@app.get("/fornitori/{fornitore_id}/modifica")
def form_modifica_fornitore(fornitore_id: int, request: Request, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    fornitore = db.query(models.Fornitore).filter(models.Fornitore.id == fornitore_id).first()
    if fornitore is None:
        raise HTTPException(status_code=404, detail="Fornitore non trovato")
    fornitori = db.query(models.Fornitore).all()
    return templates.TemplateResponse(request, "fornitore_form.html", {"utente": utente, "fornitori": fornitori, "fornitore": fornitore, "errore": None})


@app.post("/fornitori/{fornitore_id}/modifica")
def modifica_fornitore(
    fornitore_id: int,
    request: Request,
    campi: dict = Depends(_campi_fornitore_form),
    db: Session = Depends(get_db),
    utente: models.Utente = Depends(get_utente_da_sessione),
):
    fornitore = db.query(models.Fornitore).filter(models.Fornitore.id == fornitore_id).first()
    if fornitore is None:
        raise HTTPException(status_code=404, detail="Fornitore non trovato")
    if valore_gia_esistente(db, models.Fornitore, campi["nome"], escludi_id=fornitore_id):
        fornitori = db.query(models.Fornitore).all()
        return templates.TemplateResponse(
            request, "fornitore_form.html",
            {"utente": utente, "fornitori": fornitori, "fornitore": fornitore, "errore": f'"{campi["nome"]}" esiste già'},
            status_code=400,
        )
    for campo, valore in campi.items():
        setattr(fornitore, campo, valore)
    db.commit()
    return redirect_con_messaggio("/fornitori/nuovo", "Fornitore modificato")


@app.post("/fornitori/{fornitore_id}/elimina")
def elimina_fornitore(fornitore_id: int, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    fornitore = db.query(models.Fornitore).filter(models.Fornitore.id == fornitore_id).first()
    if fornitore is None:
        raise HTTPException(status_code=404, detail="Fornitore non trovato")
    if elemento_in_uso(
        db,
        (models.Materiale, models.Materiale.fornitore_id == fornitore_id),
        (models.Bolla, models.Bolla.fornitore_id == fornitore_id),
    ):
        return redirect_con_messaggio("/fornitori/nuovo", "Non è possibile eliminare questo elemento perché già in uso", tipo="avviso")
    db.delete(fornitore)
    db.commit()
    return redirect_con_messaggio("/fornitori/nuovo", "Fornitore eliminato")


@app.get("/fornitori/{fornitore_id}")
def pagina_fornitore(fornitore_id: int, request: Request, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    fornitore = db.query(models.Fornitore).filter(models.Fornitore.id == fornitore_id).first()
    if fornitore is None:
        raise HTTPException(status_code=404, detail="Fornitore non trovato")
    materiali = db.query(models.Materiale).filter(models.Materiale.fornitore_id == fornitore_id).all()
    return templates.TemplateResponse(request, "fornitore_dettaglio.html", {"fornitore": fornitore, "materiali": materiali, "utente": utente})


@app.get("/fornitori-elenco")
def pagina_fornitori_elenco(request: Request, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    fornitori = db.query(models.Fornitore).order_by(models.Fornitore.nome).all()
    return templates.TemplateResponse(request, "fornitori_elenco.html", {"fornitori": fornitori, "utente": utente})


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


@app.post("/posizioni/{posizione_id}/modifica")
def modifica_posizione(
    posizione_id: int,
    nome: str = Form(...),
    indirizzo: str = Form(""),
    tipo_posizione_id: int = Form(...),
    db: Session = Depends(get_db),
    utente: models.Utente = Depends(get_utente_da_sessione),
):
    posizione = db.query(models.Posizione).filter(models.Posizione.id == posizione_id).first()
    if posizione is None:
        raise HTTPException(status_code=404, detail="Posizione non trovata")
    posizione.nome = nome.strip()
    posizione.indirizzo = indirizzo.strip() or None
    posizione.tipo_posizione_id = tipo_posizione_id
    db.commit()
    return redirect_con_messaggio("/posizioni-elenco", "Posizione modificata")


@app.post("/posizioni/{posizione_id}/elimina")
def elimina_posizione(posizione_id: int, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    posizione = db.query(models.Posizione).filter(models.Posizione.id == posizione_id).first()
    if posizione is None:
        raise HTTPException(status_code=404, detail="Posizione non trovata")
    if elemento_in_uso(
        db,
        (models.Movimento, or_(models.Movimento.posizione_partenza_id == posizione_id, models.Movimento.posizione_arrivo_id == posizione_id)),
    ):
        return redirect_con_messaggio("/posizioni-elenco", "Non è possibile eliminare questo elemento perché già in uso", tipo="avviso")
    db.delete(posizione)
    db.commit()
    return redirect_con_messaggio("/posizioni-elenco", "Posizione eliminata")


@app.post("/posizioni/{posizione_id}/chiudi")
def chiudi_posizione(posizione_id: int, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    posizione = db.query(models.Posizione).filter(models.Posizione.id == posizione_id).first()
    if posizione is None:
        raise HTTPException(status_code=404, detail="Posizione non trovata")
    if posizione_ha_giacenza(db, posizione_id):
        return redirect_con_messaggio("/posizioni-elenco", "Non puoi chiudere questa posizione: contiene ancora del materiale", tipo="avviso")
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



def _materiale_duplicato(db: Session, nome: str, fornitore_id: int, escludi_id: int | None = None) -> bool:
    """Stesso nome, stesso fornitore (due fornitori diversi possono vendere lo stesso
    prodotto con lo stesso nome, non è un duplicato)."""
    query = db.query(models.Materiale).filter(
        models.Materiale.fornitore_id == fornitore_id,
        func.lower(func.trim(models.Materiale.nome)) == nome.strip().lower(),
    )
    if escludi_id is not None:
        query = query.filter(models.Materiale.id != escludi_id)
    return query.first() is not None


@app.get("/materiali/nuovo")
def form_materiale(request: Request, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    fornitori = db.query(models.Fornitore).all()
    unita = db.query(models.UnitaMisura).all()
    materiali = db.query(models.Materiale).all()
    return templates.TemplateResponse(request, "materiale_form.html", {"fornitori": fornitori, "unita": unita, "materiali": materiali, "materiale": None, "utente": utente, "errore": None})


@app.post("/materiali/nuovo")
def crea_materiale_da_form(
    request: Request,
    nome: str = Form(...),
    fornitore_id: int = Form(...),
    unita_misura_id: int = Form(...),
    db: Session = Depends(get_db),
    utente: models.Utente = Depends(get_utente_da_sessione),
):
    nome = nome.strip()
    if _materiale_duplicato(db, nome, fornitore_id):
        fornitori = db.query(models.Fornitore).all()
        unita = db.query(models.UnitaMisura).all()
        materiali = db.query(models.Materiale).all()
        return templates.TemplateResponse(
            request, "materiale_form.html",
            {"fornitori": fornitori, "unita": unita, "materiali": materiali, "materiale": None, "utente": utente, "errore": f'"{nome}" esiste già per questo fornitore'},
            status_code=400,
        )
    nuovo = models.Materiale(nome=nome, fornitore_id=fornitore_id, unita_misura_id=unita_misura_id)
    db.add(nuovo)
    db.commit()
    return redirect_con_messaggio("/materiali/nuovo", "Materiale aggiunto")


@app.get("/materiali/{materiale_id}/modifica")
def form_modifica_materiale(materiale_id: int, request: Request, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    materiale = db.query(models.Materiale).filter(models.Materiale.id == materiale_id).first()
    if materiale is None:
        raise HTTPException(status_code=404, detail="Materiale non trovato")
    fornitori = db.query(models.Fornitore).all()
    unita = db.query(models.UnitaMisura).all()
    materiali = db.query(models.Materiale).all()
    return templates.TemplateResponse(request, "materiale_form.html", {"fornitori": fornitori, "unita": unita, "materiali": materiali, "materiale": materiale, "utente": utente, "errore": None})


@app.post("/materiali/{materiale_id}/modifica")
def modifica_materiale(
    materiale_id: int,
    request: Request,
    nome: str = Form(...),
    fornitore_id: int = Form(...),
    unita_misura_id: int = Form(...),
    db: Session = Depends(get_db),
    utente: models.Utente = Depends(get_utente_da_sessione),
):
    materiale = db.query(models.Materiale).filter(models.Materiale.id == materiale_id).first()
    if materiale is None:
        raise HTTPException(status_code=404, detail="Materiale non trovato")
    nome = nome.strip()
    if _materiale_duplicato(db, nome, fornitore_id, escludi_id=materiale_id):
        fornitori = db.query(models.Fornitore).all()
        unita = db.query(models.UnitaMisura).all()
        materiali = db.query(models.Materiale).all()
        return templates.TemplateResponse(
            request, "materiale_form.html",
            {"fornitori": fornitori, "unita": unita, "materiali": materiali, "materiale": materiale, "utente": utente, "errore": f'"{nome}" esiste già per questo fornitore'},
            status_code=400,
        )
    materiale.nome = nome
    materiale.fornitore_id = fornitore_id
    materiale.unita_misura_id = unita_misura_id
    db.commit()
    return redirect_con_messaggio("/materiali/nuovo", "Materiale modificato")


@app.post("/materiali/{materiale_id}/elimina")
def elimina_materiale(materiale_id: int, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    materiale = db.query(models.Materiale).filter(models.Materiale.id == materiale_id).first()
    if materiale is None:
        raise HTTPException(status_code=404, detail="Materiale non trovato")
    if elemento_in_uso(
        db,
        (models.Lotto, models.Lotto.materiale_id == materiale_id),
        (models.MaterialeTipoMateriale, models.MaterialeTipoMateriale.materiale_id == materiale_id),
    ):
        return redirect_con_messaggio("/materiali/nuovo", "Non è possibile eliminare questo elemento perché già in uso", tipo="avviso")
    db.delete(materiale)
    db.commit()
    return redirect_con_messaggio("/materiali/nuovo", "Materiale eliminato")



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
    posizione = (
        db.query(models.Posizione)
        .join(models.TipoPosizione)
        .filter(models.Posizione.id == posizione_iniziale_id, func.lower(func.trim(models.TipoPosizione.nome)) == "magazzino")
        .first()
    )
    if posizione is None:
        raise HTTPException(status_code=400, detail="La posizione scelta non è un magazzino")
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


@app.get("/movimenti/{movimento_id}/modifica")
def form_modifica_movimento(movimento_id: int, request: Request, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    movimento = db.query(models.Movimento).filter(models.Movimento.id == movimento_id).first()
    if movimento is None:
        raise HTTPException(status_code=404, detail="Movimento non trovato")
    condizioni = db.query(models.CondizioneMateriale).all()
    return templates.TemplateResponse(request, "movimento_modifica.html", {"movimento": movimento, "condizioni": condizioni, "utente": utente, "errore": None})


@app.post("/movimenti/{movimento_id}/modifica")
def modifica_movimento(
    movimento_id: int,
    request: Request,
    quantita_usata: float = Form(...),
    condizione_id: str = Form(""),
    note: str = Form(""),
    data_movimento: str = Form(""),
    db: Session = Depends(get_db),
    utente: models.Utente = Depends(get_utente_da_sessione),
):
    movimento = db.query(models.Movimento).filter(models.Movimento.id == movimento_id).first()
    if movimento is None:
        raise HTTPException(status_code=404, detail="Movimento non trovato")
    nuova_data = datetime.strptime(data_movimento, "%Y-%m-%dT%H:%M") if data_movimento else None
    errore = modifica_movimento_sicura(db, movimento, quantita_usata, int(condizione_id) if condizione_id else None, note or None, nuova_data)
    if errore:
        condizioni = db.query(models.CondizioneMateriale).all()
        return templates.TemplateResponse(request, "movimento_modifica.html", {"movimento": movimento, "condizioni": condizioni, "utente": utente, "errore": errore}, status_code=400)
    return redirect_con_messaggio("/storico", "Movimento modificato")


@app.post("/movimenti/{movimento_id}/elimina")
def elimina_movimento(movimento_id: int, db: Session = Depends(get_db), utente: models.Utente = Depends(get_utente_da_sessione)):
    movimento = db.query(models.Movimento).filter(models.Movimento.id == movimento_id).first()
    if movimento is None:
        raise HTTPException(status_code=404, detail="Movimento non trovato")
    errore = elimina_movimento_sicuro(db, movimento)
    if errore:
        return redirect_con_messaggio("/storico", errore, tipo="avviso")
    return redirect_con_messaggio("/storico", "Movimento eliminato")


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
