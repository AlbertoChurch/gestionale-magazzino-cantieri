---
name: Gestionale Magazzino
description: Strumento interno calmo e leggibile in verde erba sintetica, con barra laterale verde scurissimo e nessun bianco puro come superficie.
colors:
  turf-green: "#1e7a3c"
  turf-green-deep: "#145a2b"
  turf-green-soft: "#d3e8d2"
  field-bg: "#e9f1e4"
  surface: "#f6faf3"
  surface-alt: "#e0ecda"
  border: "#cddcc5"
  border-strong: "#b4c9ab"
  ink: "#16241a"
  ink-muted: "#4b5f53"
  placeholder: "#566a5e"
  on-fill: "#ffffff"
  danger: "#c62828"
  danger-deep: "#a31f1f"
  danger-text: "#9b1c1c"
  danger-soft: "#fbe9e7"
  danger-border: "#f0b8b2"
  warning: "#fde047"
  warning-soft: "#fff3b0"
  warning-border: "#d9a406"
  sidebar-bg: "#0f2519"
  sidebar-text: "#dfeae4"
  sidebar-muted: "#9bb8a6"
  sidebar-hover: "#193523"
  sidebar-active: "#1f4a31"
  sidebar-brand-green: "#7fd08f"
  sidebar-active-green: "#8ee09e"
  login-brand-green: "#9be5aa"
  login-stripe-dark: "#1a5029"
  login-stripe-light: "#1c5a30"
typography:
  headline:
    fontFamily: "Segoe UI Variable Text, Segoe UI, system-ui, -apple-system, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.625rem"
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "-0.015em"
  title:
    fontFamily: "Segoe UI Variable Text, Segoe UI, system-ui, -apple-system, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.25rem"
    fontWeight: 650
    lineHeight: 1.25
    letterSpacing: "-0.01em"
  subtitle:
    fontFamily: "Segoe UI Variable Text, Segoe UI, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 650
    lineHeight: 1.25
  body:
    fontFamily: "Segoe UI Variable Text, Segoe UI, system-ui, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 400
    lineHeight: 1.5
  body-small:
    fontFamily: "Segoe UI Variable Text, Segoe UI, system-ui, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 500
    lineHeight: 1.5
  label:
    fontFamily: "Segoe UI Variable Text, Segoe UI, system-ui, sans-serif"
    fontSize: "0.78rem"
    fontWeight: 600
    lineHeight: 1.5
  compact-button:
    fontFamily: "Segoe UI Variable Text, Segoe UI, system-ui, sans-serif"
    fontSize: "0.8125rem"
    fontWeight: 600
    lineHeight: 1.5
rounded:
  sm: "7px"
  md: "10px"
  pill: "50%"
  scrollbar-thumb: "4px"
spacing:
  xs: "6px"
  sm: "12px"
  md: "18px"
  lg: "24px"
  page-x: "32px"
  sidebar: "248px"
components:
  button-primary:
    backgroundColor: "{colors.turf-green}"
    textColor: "{colors.on-fill}"
    typography: "{typography.body}"
    rounded: "{rounded.sm}"
    padding: "0 20px"
    height: "42px"
  button-primary-hover:
    backgroundColor: "{colors.turf-green-deep}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.body-small}"
    rounded: "{rounded.sm}"
    padding: "0 13px"
    height: "36px"
  button-secondary-hover:
    backgroundColor: "{colors.surface-alt}"
  button-secondary-large:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.body-small}"
    rounded: "{rounded.sm}"
    padding: "0 13px"
    height: "42px"
  button-secondary-compact:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.compact-button}"
    rounded: "{rounded.sm}"
    padding: "0 10px"
    height: "32px"
  button-danger-confirm:
    backgroundColor: "{colors.danger}"
    textColor: "{colors.on-fill}"
    rounded: "{rounded.sm}"
    padding: "0 13px"
    height: "36px"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "10px 12px"
    height: "42px"
  combo-input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "10px 38px 10px 12px"
    height: "42px"
  combo-list:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "4px"
  combo-option:
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "9px 10px"
  combo-option-active:
    backgroundColor: "{colors.turf-green-soft}"
  combo-option-selected:
    textColor: "{colors.turf-green-deep}"
  card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.md}"
    padding: "24px"
  table-header:
    backgroundColor: "{colors.surface-alt}"
    textColor: "{colors.turf-green-deep}"
    typography: "{typography.body-small}"
    padding: "11px 12px"
  nav-item:
    backgroundColor: "{colors.sidebar-bg}"
    textColor: "{colors.sidebar-text}"
    rounded: "{rounded.sm}"
    padding: "9px 10px"
  nav-item-active:
    backgroundColor: "{colors.sidebar-active}"
    textColor: "{colors.on-fill}"
  toast:
    backgroundColor: "{colors.turf-green}"
    textColor: "{colors.on-fill}"
    rounded: "{rounded.md}"
    padding: "14px 20px"
  step-number:
    backgroundColor: "{colors.turf-green}"
    textColor: "{colors.on-fill}"
    rounded: "{rounded.pill}"
    size: "26px"
  count-chip:
    backgroundColor: "{colors.turf-green-soft}"
    textColor: "{colors.turf-green-deep}"
    typography: "{typography.body-small}"
    rounded: "{rounded.sm}"
    padding: "0 8px"
    height: "26px"
  empty-compact:
    textColor: "{colors.ink-muted}"
    rounded: "{rounded.sm}"
    padding: "18px 14px"
  summary-banner:
    backgroundColor: "{colors.turf-green-soft}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "12px 16px"
  info-panel:
    backgroundColor: "{colors.surface-alt}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "12px 16px"
  error-box:
    backgroundColor: "{colors.danger-soft}"
    textColor: "{colors.danger-text}"
    rounded: "{rounded.sm}"
    padding: "12px 16px"
---

# Design System: Gestionale Magazzino

## Overview

**Creative North Star: "Il Campo in Ordine"**

Un gestionale per chi registra spostamenti di materiale per campi sportivi, usato ogni giorno da personale non tecnico su PC desktop. Il sistema e' un campo ben tenuto: superfici verde erba molto chiare, una barra laterale verde quasi nero che fa da bordo del campo, un solo verde pieno per le azioni. Tutto e' piano, leggibile, prevedibile; l'espressivita' cede sempre alla chiarezza.

La densita' e' da strumento di lavoro: tabelle, filtri e form in card ordinate su una colonna centrale di 1200px. La struttura (card, passi numerati, tabelle) porta il significato; il colore dice solo stato e azione. Il tema erba sintetica e' letterale in un solo punto, lo sfondo del login, dove compaiono le strisce di sfalcio. Altrove e' solo tinta.

Il sistema rifiuta il bianco puro come superficie (impegno del committente), i font o risorse esterni (l'app gira offline) e il movimento che non comunica uno stato.

**Key Characteristics:**
- Verdi con una punta di giallo, mai bianco puro come superficie; il bianco appare solo come testo su verde pieno, rosso o barra scura.
- Un solo accento pieno (verde erba); rosso e giallo solo per esito e pericolo.
- Piatto con ombre minime: la profondita' viene dai toni delle superfici, l'ombra forte solo per cio' che galleggia (toast, elenco a tendina, login).
- Font di sistema Segoe UI, scala tipografica corta in rem.
- Le liste a tendina sono campi in cui si scrive, sopra un select nativo che resta la fonte dei dati.
- Movimento breve e leggero, spento con prefers-reduced-motion.

## Colors

Tavolozza monocromatica verde-giallastra con neutri tinti di verde; rosso e giallo riservati agli stati.

### Primary
- **Verde Erba** (`turf-green`): bottoni primari, numeri dei passi, toast di successo, focus ring, accent-color dei controlli nativi. Testo bianco su di esso: 5.38:1.
- **Verde Erba Profondo** (`turf-green-deep`): hover dei bottoni, link, intestazioni di tabella, voce selezionata e testo cercato nell'elenco a tendina, numero nel contatore (7.87:1 su surface, 6.8:1 su surface-alt).
- **Verde Erba Tenue** (`turf-green-soft`): riepilogo, contatore della lista, voce attiva dell'elenco a tendina, selezione testo, riga di tabella in hover (a 45% di opacita').

### Secondary
- **Rosso Allarme** (`danger`): azione distruttiva di conferma, toast di errore, asterisco obbligatorio. Testo bianco: 5.62:1. Variante testo `danger-text` (6.95:1 su danger-soft) per messaggi d'errore e giacenze sotto soglia; `danger-soft` e `danger-border` per il riquadro errore.
- **Giallo Segnale** (`warning`): toast di avviso con testo scuro (12.24:1). `warning-soft` e `warning-border` segnano i campi e i movimenti modificati, anche quando il campo e' una lista a tendina.

### Neutral
- **Campo** (`field-bg`): sfondo pagina.
- **Superficie** (`surface`): card, tabelle, campi di input, elenco a tendina. E' il piu' chiaro del sistema.
- **Superficie Scura** (`surface-alt`): testata tabelle, pannello info, hover secondario, campo disabilitato.
- **Bordo** (`border`) e **Bordo Forte** (`border-strong`): divisori e contorni; il forte per input, bottoni secondari, elenco a tendina e righe tratteggiate.
- **Inchiostro** (`ink`): testo, 15.28:1 su surface. **Inchiostro Smorzato** (`ink-muted`): etichette, meta, freccia dell'elenco, 6.5:1 su surface, 5.61:1 su surface-alt.
- **Segnaposto** (`placeholder`, 5.5:1 su surface): solo il testo segnaposto dei campi, e' il valore piu' chiaro ammesso per testo non critico.
- **Barra laterale**: `sidebar-bg`, testo `sidebar-text` (13.11:1), testo smorzato `sidebar-muted` (7.54:1 su sfondo, 6.22:1 su hover), `sidebar-hover`, `sidebar-active` con testo bianco (10.09:1).
- **Verdi di accento su scuro**: `sidebar-brand-green` (icona del marchio nella barra, circa 8.7:1 su sidebar-bg), `sidebar-active-green` (icona della voce attiva e anello di focus nella barra), `login-brand-green` (icona del marchio nel login, circa 6.4:1 su strisce). Servono solo su fondi scuri, solo per icone e anelli, mai come testo corrente ne' su superfici chiare.
- **Strisce login** (`login-stripe-dark` / `login-stripe-light`): solo sfondo del login.

### Named Rules
**The No Pure White Rule.** Nessuna superficie e' #fff: la piu' chiara e' #f6faf3. Il bianco (`on-fill`, #ffffff) e' ammesso solo come TESTO o icona su riempimenti saturi o scuri: bottone primario, conferma elimina, numero del passo, toast, voce attiva e marchio della barra, marchio del login. Mai come sfondo.
**The One Green Rule.** Un solo verde pieno comanda le azioni; gli stati passano per rosso e giallo, mai per un secondo verde. I tre verdi chiari su fondo scuro sono tinte di icona, non azioni.
**The Tinted Neutral Rule.** Ogni grigio e' tirato verso il verde della tavolozza; niente grigi neutri.

## Typography

**Display e Body Font:** Segoe UI Variable Text (con Segoe UI, system-ui, Helvetica Neue, Arial, sans-serif). Una sola famiglia di sistema, nessun font caricato.

**Character:** Neutro e da sportello: pesi 600-700 per gerarchia, 400-500 per lettura. I numeri in tabella usano cifre tabulari.

### Hierarchy
- **Headline** (700, 1.625rem, 1.25, -0.015em): titolo di pagina (h1).
- **Title** (650, 1.25rem, 1.25, -0.01em): titolo di card (h2); anche marchio del login.
- **Subtitle** (650, 1.0625rem): legend dei fieldset, titolo dei passi, nome marchio nella barra, voce vuota in evidenza.
- **Body** (400, 0.9375rem, 1.5): testo, input, celle, voci dell'elenco a tendina, bottoni primari (600).
- **Body small** (500-700, 0.875rem): etichette dei campi (500, ink-muted), testata tabelle (650), bottoni secondari (600), meta, tabelle dense, contatore della lista (700).
- **Label** (600, 0.78rem): dt dei pannelli dati e sezioni della barra laterale (maiuscolo con 0.07em, solo li').
- **Compact button** (600, 0.8125rem): solo i bottoni secondari dentro tabelle dense (`.tabella-densa`: Modifica, Elimina, Togli). Fuori scala per scelta: 0.875rem non entra nella cella da 32px di altezza accanto ad altri bottoni senza allargare la riga.

### Named Rules
**The Short Ladder Rule.** Si usano i sei passi della scala (0.78 / 0.875 / 0.9375 / 1.0625 / 1.25 / 1.625rem); l'unica eccezione registrata e' 0.8125rem per i bottoni compatti nelle tabelle dense. Ogni altro valore va aggiunto alla scala o evitato.
**The Tabular Numbers Rule.** Le tabelle usano cifre tabulari e colonne numeriche allineate a destra.

## Layout

Barra laterale fissa di 248px (sticky, altezza piena, scorre al proprio interno) piu' colonna principale centrata a 1200px massimo, con padding 36px 32px 56px. Le pagine sono pile di card con 24px di spazio sotto. I form usano una griglia a colonne automatiche (minimo 240px, gap colonne 22px) oppure due colonne fisse; i campi larghi occupano tutta la riga. I filtri usano una griglia con minimo 170px, gap 14px, allineata al fondo. Ritmo ricorrente: 6, 10, 12, 14, 18, 24px. Sotto 860px la barra diventa una fascia orizzontale in alto, il main passa a padding 24px 16px, la card a 18px e le due colonne a una. Gli input hanno larghezza massima 420px fuori dalle griglie; l'elenco a tendina segue la stessa regola e occupa tutta la cella dentro griglie, filtri e modifica in linea.

Utilita' di layout ricorrenti: `.sottotitolo` (riga di spiegazione sotto il titolo, margine -10px 0 18px), `.nota-form` (nota sopra un form, 14px sotto), `.nowrap` (date e valori che non vanno a capo), `.barra-azioni` (riga di bottoni con gap 10px, `.staccata` aggiunge 20px sopra per separarla dal contenuto).

La pagina Nuovo movimento e' una card unica con tre passi in colonna, separati da una linea di 1px e 22px di spazio.

## Elevation & Depth

Ibrido, per lo piu' tonale: superficie chiara su campo piu' scuro con bordo da 1px; ombra minima sulle card, ombra forte solo per cio' che galleggia.

### Shadow Vocabulary
- **Card** (`box-shadow: 0 1px 2px rgba(22,36,26,0.06), 0 2px 8px rgba(22,36,26,0.04)`): ogni card, a riposo.
- **Pop** (`box-shadow: 0 1px 3px rgba(14,26,18,0.2), 0 10px 28px rgba(14,26,18,0.22)`): toast, elenco a tendina aperto e card del login.
- **Focus ring dei campi** (`0 0 0 3px rgba(30,122,60,0.2)` piu' bordo verde): solo in focus.

### Named Rules
**The Flat-Until-Floating Rule.** Le superfici di lavoro sono quasi piatte; l'ombra marcata e' per toast, elenco a tendina aperto e login.

## Shapes

Angoli morbidi ma sobri, su due soli passi: 10px (`--radius`) per card, toast ed elenco a tendina aperto; 7px (`--radius-sm`) per bottoni, campi, tabelle, riquadri, voci dell'elenco, contatore e voci della barra; cerchio per il numero del passo. Eccezione deliberata: il pollice della barra di scorrimento della barra laterale ha 4px, perche' e' largo 8px e un raggio da 7px lo trasformerebbe in una pillola. Bordi da 1px in verde chiaro; divisori e riquadri vuoti tratteggiati (1px dashed) per elenchi, ricevute e stato vuoto compatto. Le tabelle dentro una card dedicata arrivano a filo dei bordi (padding 0, celle laterali 18px).

## Components

### Buttons
- **Shape:** angoli da 7px, altezza minima 42px, padding 0 20px, testo 0.9375rem peso 600.
- **Primary:** verde erba, testo bianco; hover verde profondo; pressione con scala 0.96; disabilitato in border-strong con testo smorzato.
- **Secondary** (`.btn-secondario`): superficie chiara, bordo forte, testo inchiostro, altezza 36px, 0.875rem peso 600, hover su surface-alt con bordo verde.
  - **Grande** (`.btn-secondario.grande`): altezza 42px, per l'azione secondaria di una riga di campi o di un passo ("Aggiungi alla lista", "Azzera filtri").
  - **Compatto:** altezza 32px, padding 0 10px, 0.8125rem, solo dentro `.tabella-densa`.
  - **Come link** (`a.btn-secondario`): stesso aspetto su un `<a>` (inline-flex, senza sottolineatura, testo inchiostro anche in hover), con la stessa pressione 0.96. E' il modo per un link con aspetto di bottone; mai un button dentro un link.
- **Elimina in due passi:** secondo tocco "Sei sicuro?" in rosso, altezza 36px, entra con scala da 0.92 in 150ms.

### Cards / Containers
- **Corner Style:** 10px. **Background:** surface. **Border:** 1px border. **Shadow:** ombra card. **Padding:** 24px (18px su schermi stretti), margine sotto 24px.
- **Card tabella:** padding 0, tabella a filo, overflow orizzontale se serve.

### Inputs / Fields
- **Style:** surface, bordo forte 1px, 7px, altezza 42px; etichetta sopra in ink-muted 0.875rem peso 500.
- **Hover/Focus:** bordo verde in hover; focus con bordo verde e anello 3px verde al 20%. Placeholder in `placeholder` (5.5:1).
- **Disabled:** sfondo surface-alt, testo smorzato, cursore non consentito. Obbligatorio con asterisco rosso.
- **Modificato:** un campo il cui valore e' stato cambiato rispetto all'originale diventa giallo tenue con bordo giallo scuro; vale anche per l'elenco a tendina.
- **Errore in linea** (`.errore.in-linea`): il riquadro errore a blocco con margine 6px sopra e 0 sotto, subito sotto il campo o la riga a cui si riferisce, con `role="alert"`; il riquadro errore normale (margine 0 0 18px) sta sopra la card.
- **Fieldset:** senza bordo, legend a 1.0625rem peso 650, 18px tra fieldset.

### Searchable select ("combo")
Ogni `<select>` e' sostituito da un campo in cui si scrive (`.combo-input`, come un input, con 38px a destra per la freccia). Il `<select class="combo-nativo">` resta sotto, invisibile e non cliccabile, ed e' la fonte dei dati: invio del form, validazione "obbligatorio", onchange e select.value funzionano come prima. Escluso con `data-combo="no"`; i select multipli non sono toccati.
- **Freccia** (`.combo-freccia`): chevron 14px in ink-muted, zona cliccabile 38x42px a destra; ruota di 180 gradi quando aperto (250ms); da disabilitato opacita' 0.5 e cursore non consentito. Da aperto il bordo del campo e' verde.
- **Elenco** (`.combo-lista`): sotto il campo con 4px di stacco; si apre sopra (`.sopra`) se sotto restano meno di 220px e sopra c'e' piu' spazio. Surface, bordo forte, 10px, ombra pop, padding 4px, altezza massima tra 140 e 280px, scorre al proprio interno, z-index 60.
- **Voce** (`.combo-opzione`): 0.9375rem, padding 9px 10px, 7px, testo a capo anche su stringhe lunghe. Attiva (`.combo-attiva`, tastiera o mouse): sfondo verde tenue. Selezionata (`aria-selected="true"`): peso 650 in verde profondo con segno di spunta disegnato a destra. Voce vuota di invito: corsivo smorzato (solo per campi obbligatori, dove non e' scegliibile).
- **Evidenza** (`.combo-evidenza`): la parte di testo corrispondente a quanto scritto, in grassetto 700 verde profondo.
- **Nessun risultato** (`.combo-nessuno`): riga smorzata "Nessun risultato", padding 10px.
- **Tastiera:** frecce su e giu' aprono e muovono la voce attiva; Invio sceglie la voce attiva; Esc chiude e ripristina il testo; Tab conferma la voce evidenziata se si e' scritto qualcosa. Scrivere filtra senza distinguere maiuscole e accenti, per parole in qualsiasi ordine, con le voci che iniziano per la prima parola davanti. Si possono scegliere solo voci che esistono: uscendo dal campo si ripristina il testo valido, o si conferma una corrispondenza esatta (e, se il campo non e' obbligatorio, il testo vuoto sceglie la voce vuota "Tutti").

### Navigation
Barra laterale verde scurissimo con marchio (icona SVG in `sidebar-brand-green` piu' nome), sezioni in maiuscoletto smorzato, voci con icona SVG a tratto 1.6. Hover su `sidebar-hover`; voce attiva su `sidebar-active` con testo bianco, peso 600 e icona in `sidebar-active-green`. I sottomenu si aprono in altezza naturale con transizione di grid-template-rows (350ms), chevron che ruota di 90 gradi, guida verticale a sinistra; le voci interne sono piu' piccole e smorzate. Utente e uscita in fondo, separati da una linea. Focus: anello `sidebar-active-green` interno. La barra di scorrimento e' sottile, in sidebar-muted, con pollice da 4px.

### Tables
Superficie con bordo, testata surface-alt in verde profondo peso 650, righe con divisore, hover verde tenue. Celle 11px 12px; variante densa (`.tabella-densa`: Storico e lista dei materiali) 10px 8px a 0.875rem con bottoni compatti da 32px. Colonne numeriche a destra. Valore basso in danger-text grassetto; riga modificata in giallo tenue. Una tabella dentro un form che puo' superare la larghezza sta in `.tabella-scroll` (scorrimento orizzontale, 16px sotto).

### Toast
Fisso in alto a destra, 14px 20px, 10px di raggio, ombra pop. Verde per successo, rosso per errore, giallo con testo scuro per avviso. Entra con salita da 16px, scala 0.97 e sfocatura 2px in 350ms, esce in 250ms; tocco per chiudere.

### Empty states
Testo centrato, padding 38px 16px; frase principale in grassetto inchiostro a 1.0625rem, sotto spiegazione smorzata e, se serve, la via d'uscita ("Azzera filtri").
**Compatto** (`.vuoto-compatto`): per un elenco vuoto dentro un passo di form; padding 18px 14px, 16px sotto, riquadro tratteggiato 1px in border-strong, 7px. Stessa gerarchia testuale.

### Step headers (Nuovo movimento)
Intestazione di passo con cerchio verde 26px numerato in bianco e titolo 1.0625rem peso 650; i passi sono separati da una linea di 1px e 22px di spazio. Il passo 3 aggiunge accanto al titolo il contatore.

### Materiali da spostare (lista del movimento)
Il passo 2 sceglie materiale (elenco a tendina, abilitato solo dopo la partenza), quantita', condizione, note, mostra il pannello info del lotto e una nota gialla che spiega il campo modificato; il bottone "Aggiungi alla lista" (`.btn-secondario.grande`) aggiunge la riga (Invio nei campi quantita' e note fa lo stesso) e gli errori di riga compaiono in un riquadro errore sopra al bottone. Il passo 3 mostra:
- **Contatore** (`.conteggio-lista`): chip 26px di altezza, minimo 26px di larghezza, verde tenue con numero in verde profondo peso 700, 7px; visibile solo con almeno una riga.
- **Stato vuoto compatto** quando la lista e' vuota ("La lista e' vuota" con istruzione).
- **Tabella** `.tabella-densa` in `.tabella-scroll` con colonne Materiale, Quantita' (a destra), Unita', Condizione, Note e un bottone secondario "Togli" per riga (con aria-label che nomina il materiale); sotto, "Svuota la lista" come secondario.
- **Riepilogo** (`.riepilogo`): banner verde tenue con bordo forte, `role="status"`, solo con lista piena e arrivo scelto; avvisa anche quando partenza e arrivo coincidono senza cambio di condizione o note.
- **Invio unico:** un solo bottone primario registra tutte le righe insieme, tutto o niente; con piu' righe l'etichetta diventa "Registra N spostamenti" e si disabilita dopo il clic. Con la lista vuota ma un materiale scelto, l'invio lo aggiunge da solo; con lista piena e materiale scelto ma non aggiunto, blocca e lo segnala. La partenza non si cambia finche' la lista non e' vuota.

### Summary banner and info panel
Il riepilogo e' un riquadro verde tenue con bordo forte (peso 500) che conferma cosa sta per succedere; il pannello info e' surface-alt con coppie dt/dd in griglia (dt 0.78rem smorzato, dd peso 600).

### Login backdrop
Unico luogo in cui il tema e' letterale: sfondo verde scuro con strisce di sfalcio verticali da 64px (`login-stripe-dark` / `login-stripe-light`) e vignettatura radiale scura; card da 360px con ombra pop e senza bordo, marchio bianco sopra con icona in `login-brand-green`.

### Motion
Scala condivisa: quick 150ms (hover, focus, colori), fast 250ms (chevron, freccia dell'elenco, uscita toast), medium 350ms (sottomenu, entrata toast); easing unico cubic-bezier(0.22, 1, 0.36, 1). Pressione dei bottoni (anche `a.btn-secondario`) a scala 0.96. Dissolvenza di pagina nativa (view transition, 150ms) con la barra laterale che resta ferma grazie al nome proprio. Con prefers-reduced-motion: reduce tutte le durate scendono a 0.01ms e la view transition non e' attiva.

## Do's and Don'ts

### Do:
- **Do** usare solo i token del :root (colori, scala dei font, raggi, ombre, durate) e aggiungerne uno prima di scrivere un valore nuovo.
- **Do** tenere superfici in verde chiaro (#f6faf3 e piu' scure), mai #fff; il bianco solo come testo o icona su verde pieno, rosso o fondi scuri.
- **Do** usare il verde erba pieno solo per l'azione principale della vista; i bottoni secondari per tutto il resto.
- **Do** dare ai bersagli cliccabili almeno 36px di altezza (42px per azioni primarie e campi; 32px solo per i bottoni compatti nelle tabelle dense).
- **Do** usare i raggi 10px e 7px; ogni nuovo elemento sceglie uno dei due.
- **Do** far seguire ogni eliminazione da una conferma in due passi e da un toast di esito.
- **Do** lasciare che ogni `<select>` diventi un elenco a tendina con ricerca, tenendo il select nativo come fonte dei dati; per i link con aspetto di bottone usare `a.btn-secondario`.
- **Do** raccogliere piu' righe in una lista e registrarle con un solo invio, tutto o niente.
- **Do** verificare il contrasto del testo su ogni nuovo fondo; i valori attuali stanno tra 5.09:1 e 15.28:1.
- **Do** rispettare prefers-reduced-motion per ogni nuova animazione.

### Don't:
- **Don't** usare le strisce di sfalcio fuori dal login: e' l'unico punto letterale del tema.
- **Don't** caricare font, icone o script da risorse esterne: l'app gira offline.
- **Don't** usare il colore come unico segnale: rosso e giallo accompagnano sempre un testo; la voce selezionata dell'elenco ha anche spunta e peso.
- **Don't** introdurre un secondo accento pieno oltre al verde erba, ne' usare i verdi chiari da fondo scuro su superfici chiare o come testo.
- **Don't** aggiungere ombre marcate alle card di lavoro: l'ombra pop e' per toast, elenco a tendina e login.
- **Don't** annidare un button dentro un link: usare `a.btn-secondario`.
- **Don't** permettere nell'elenco a tendina valori che non esistono tra le opzioni.
