# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
Personale d'ufficio e di magazzino di un'azienda cliente che gestisce materiali per campi sportivi (erba sintetica, inerti, porte, reti, ferramenta). Utenti non tecnici, uso quotidiano da PC desktop in ufficio, spesso persone diverse sullo stesso computer. Il lavoro: registrare spostamenti di materiale tra magazzini e cantieri, consultare le giacenze, registrare le bolle di arrivo, tenere l'anagrafica di fornitori e materiali.

## Product Purpose
Tracciare dove si trova ogni materiale (magazzino o cantiere), da quale bolla/fornitore arriva, in che condizione e in che quantita', con uno storico corretto dei movimenti. Successo: chi registra o consulta capisce subito cosa sta facendo e non puo' sbagliare in modo irreversibile.

## Operating Context
App server-rendered (FastAPI + Jinja2), gira in locale su un solo PC dell'ufficio cliente (127.0.0.1), niente internet garantito: nessun CDN, nessun font o script esterno. JavaScript solo vanilla. Versione 0.1 per un singolo utente di prova, con aggiornamenti futuri via git.

## Capabilities and Constraints
Pagine: Giacenze, Nuovo movimento, Storico (filtri), Inserimento materiale (bolla + lotti), Bolle, Fornitori e prodotti (filtri), Archivio (bolle vecchie, posizioni chiuse), Aggiungi dati (fornitori, posizioni, materiali, anagrafiche semplici, account), cambio password, login. Eliminazioni a due passi ("Elimina" poi "Sei sicuro?"), popup di esito (verde/giallo/rosso) via parametro URL. Nessuna dipendenza nuova: solo CSS e JS vanilla, nessun GSAP.

## Brand Commitments
Identita' cromatica scelta dal committente: verde che ricordi l'erba sintetica, con nero/verde scurissimo per la navigazione laterale; niente bianco puro (superfici verdi molto chiare). Lingua dell'interfaccia: italiano.

## Product Principles
1. Chiarezza prima dell'espressivita': un utente non tecnico deve capire cosa sta facendo senza istruzioni.
2. Gli errori si prevengono e si spiegano in pagina, mai con JSON grezzo o blocchi silenziosi.
3. Le azioni distruttive hanno sempre una conferma e un esito visibile.
4. Funziona offline e senza installazioni: ogni risorsa e' servita dall'app stessa.
5. Miglioramenti di usabilita' solo dove i fatti di dominio sono noti; dove mancano informazioni, il comportamento resta invariato.

## Accessibility & Inclusion
Contrasto leggibile su schermi d'ufficio (anche datati), bersagli cliccabili comodi, stato di focus visibile, rispetto di prefers-reduced-motion.
