"""Elimina dal database le tabelle dell'ormai rimosso concetto "Ordine".

Non sono piu' in app/models.py ma restano nel file .db: con PRAGMA foreign_keys=ON
le righe orfane di materiali_ordini bloccano l'eliminazione di un materiale nuovo
che riusa un id gia' presente li' (IntegrityError).

Uso, dalla cartella che contiene gestionale.db (meglio a server fermo):
    python deploy/pulisci_tabelle_ordini.py [percorso/del/file.db]

Idempotente: se le tabelle non ci sono piu' non fa nulla, nemmeno il backup.
Non importa app/: importarla lancerebbe _migra_schema() sul database.
"""
import os
import sqlite3
import sys
from datetime import datetime

# Dal figlio al padre: con le foreign key attive DROP TABLE cancella prima le righe
# e fallisce se qualcuno le referenzia ancora.
TABELLE_LEGACY = ["materiali_ordini", "bolle_ordini", "ordini", "stati_ordine"]


def pulisci(percorso: str) -> int:
    if not os.path.exists(percorso):  # connect() creerebbe un db vuoto
        print(f"File non trovato: {percorso}. Nessuna modifica.")
        return 1
    con = sqlite3.connect(percorso, isolation_level=None)  # transazione gestita a mano
    try:
        esistenti = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        da_eliminare = [t for t in TABELLE_LEGACY if t in esistenti]
        if not da_eliminare:
            print("Nessuna tabella legacy degli ordini presente: niente da fare.")
            return 0

        # Se una tabella ancora in uso le referenzia, il DROP sarebbe un danno, non una pulizia.
        bloccanti = [
            f"{t} -> {rif[2]}"
            for t in sorted(esistenti - set(TABELLE_LEGACY)) if not t.startswith("sqlite_")
            for rif in con.execute(f'PRAGMA foreign_key_list("{t}")') if rif[2].lower() in TABELLE_LEGACY
        ]
        if bloccanti:
            print("STOP: queste tabelle puntano ancora a quelle degli ordini. Nessuna modifica:")
            print("  " + "\n  ".join(bloccanti))
            return 1

        backup = f"{percorso}.bak-{datetime.now():%Y%m%d-%H%M%S}"
        copia = sqlite3.connect(backup)
        con.backup(copia)  # copia coerente anche se il file e' in uso
        copia.close()

        righe = {t: con.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] for t in da_eliminare}
        con.execute("BEGIN")
        try:
            for t in da_eliminare:
                con.execute(f'DROP TABLE "{t}"')
            con.execute("COMMIT")
        except Exception:
            con.execute("ROLLBACK")
            raise
    finally:
        con.close()

    print(f"Backup creato: {backup}")
    for t in da_eliminare:
        print(f"Eliminata la tabella {t} (righe: {righe[t]})")
    print("Fatto.")
    return 0


if __name__ == "__main__":
    sys.exit(pulisci(sys.argv[1] if len(sys.argv) > 1 else "gestionale.db"))
