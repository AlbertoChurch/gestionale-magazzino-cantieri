---
name: Gestionale Magazzino
description: Strumento interno calmo e leggibile in verde erba sintetica, con barra laterale verde scurissimo e nessun bianco puro.
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
rounded:
  sm: "7px"
  md: "10px"
  pill: "50%"
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
    textColor: "#ffffff"
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
  button-danger-confirm:
    backgroundColor: "{colors.danger}"
    textColor: "#ffffff"
    rounded: "{rounded.sm}"
    padding: "0 13px"
    height: "36px"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "10px 12px"
    height: "42px"
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
    textColor: "#ffffff"
  toast:
    backgroundColor: "{colors.turf-green}"
    textColor: "#ffffff"
    rounded: "{rounded.md}"
    padding: "14px 20px"
  step-number:
    backgroundColor: "{colors.turf-green}"
    textColor: "#ffffff"
    rounded: "{rounded.pill}"
    size: "26px"
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
---

# Design System: Gestionale Magazzino

## Overview

**Creative North Star: "Il Campo in Ordine"**

Un gestionale per chi registra spostamenti di materiale per campi sportivi, usato ogni giorno da personale non tecnico su PC desktop. Il sistema e' un campo ben tenuto: superfici verde erba molto chiare, una barra laterale verde quasi nero che fa da bordo del campo, un solo verde pieno per le azioni. Tutto e' piano, leggibile, prevedibile; l'espressivita' cede sempre alla chiarezza.

La densita' e' da strumento di lavoro: tabelle, filtri e form in card ordinate su una colonna centrale di 1200px. La struttura (card, passi numerati, tabelle) porta il significato; il colore dice solo stato e azione. Il tema erba sintetica e' letterale in un solo punto, lo sfondo del login, dove compaiono le strisce di sfalcio. Altrove e' solo tinta.

Il sistema rifiuta il bianco puro come superficie (impegno del committente), i font o risorse esterni (l'app gira offline) e il movimento che non comunica uno stato.

**Key Characteristics:**
- Verdi con una punta di giallo, mai bianco puro come superficie; il bianco appare solo come testo su verde pieno o scuro.
- Un solo accento pieno (verde erba); rosso e giallo solo per esito e pericolo.
- Piatto con ombre minime: la profondita' viene dai toni delle superfici, l'ombra forte solo per popup e login.
- Font di sistema Segoe UI, scala tipografica corta in rem.
- Movimento breve e leggero, spento con prefers-reduced-motion.

## Colors

Tavolozza monocromatica verde-giallastra con neutri tinti di verde; rosso e giallo riservati agli stati.

### Primary
- **Verde Erba** (`turf-green`, #1e7a3c): bottoni primari, numeri dei passi, toast di successo, focus ring, accent-color dei controlli nativi. Testo bianco su di esso: 5.38:1.
- **Verde Erba Profondo** (`turf-green-deep`, #145a2b): hover dei bottoni, link, intestazioni di tabella (7.87:1 su surface, 6.8:1 su surface-alt).
- **Verde Erba Tenue** (`turf-green-soft`, #d3e8d2): riepilogo, selezione testo, riga di tabella in hover (a 45% di opacita').

### Secondary
- **Rosso Allarme** (`danger`, #c62828): azione distruttiva di conferma, toast di errore, asterisco obbligatorio. Testo bianco: 5.62:1. Variante testo `danger-text` (#9b1c1c, 6.95:1 su danger-soft) per messaggi d'errore e giacenze sotto soglia; `danger-soft` e `danger-border` per il riquadro errore.
- **Giallo Segnale** (`warning`, #fde047): toast di avviso con testo scuro (12.24:1). `warning-soft` (#fff3b0) e `warning-border` (#d9a406) segnano i movimenti modificati.

### Neutral
- **Campo** (`field-bg`, #e9f1e4): sfondo pagina.
- **Superficie** (`surface`, #f6faf3): card, tabelle, campi di input. E' il piu' chiaro del sistema.
- **Superficie Scura** (`surface-alt`, #e0ecda): testata tabelle, pannello info, hover secondario, campo disabilitato.
- **Bordo** (`border`, #cddcc5) e **Bordo Forte** (`border-strong`, #b4c9ab): divisori e contorni; il forte per input, bottoni secondari e righe tratteggiate.
- **Inchiostro** (`ink`, #16241a): testo, 15.28:1 su surface. **Inchiostro Smorzato** (`ink-muted`, #4b5f53): etichette e meta, 6.5:1 su surface, 5.61:1 su surface-alt.
- **Barra laterale**: `sidebar-bg` #0f2519, testo #dfeae4 (13.11:1), testo smorzato #9bb8a6 (7.54:1 su sfondo, 6.22:1 su hover), hover #193523, attivo #1f4a31 con testo bianco (10.09:1).
- **Strisce login** (#1a5029 / #1c5a30): solo sfondo del login.

### Named Rules
**The No Pure White Rule.** Nessuna superficie e' #fff: la piu' chiara e' #f6faf3. Il bianco e' ammesso solo come testo o icona su verde pieno, rosso o barra laterale.
**The One Green Rule.** Un solo verde pieno comanda le azioni; gli stati passano per rosso e giallo, mai per un secondo verde.
**The Tinted Neutral Rule.** Ogni grigio e' tirato verso il verde della tavolozza; niente grigi neutri.

## Typography

**Display e Body Font:** Segoe UI Variable Text (con Segoe UI, system-ui, Helvetica Neue, Arial, sans-serif). Una sola famiglia di sistema, nessun font caricato.

**Character:** Neutro e da sportello: pesi 600-700 per gerarchia, 400-500 per lettura. I numeri in tabella usano cifre tabulari.

### Hierarchy
- **Headline** (700, 1.625rem, 1.25, -0.015em): titolo di pagina (h1).
- **Title** (650, 1.25rem, 1.25, -0.01em): titolo di card (h2); anche marchio del login.
- **Subtitle** (650, 1.0625rem): legend dei fieldset, titolo dei passi, nome marchio nella barra, voce vuota in evidenza.
- **Body** (400, 0.9375rem, 1.5): testo, input, celle, bottoni primari (600).
- **Body small** (500-600, 0.875rem): etichette dei campi (500, ink-muted), testata tabelle (650), bottoni secondari (600), meta, tabelle dense.
- **Label** (600, 0.78rem): dt dei pannelli dati e sezioni della barra laterale (maiuscolo con 0.07em, solo li').

### Named Rules
**The Short Ladder Rule.** Si usano solo i sei passi della scala (0.78 / 0.875 / 0.9375 / 1.0625 / 1.25 / 1.625rem); un valore fuori scala va aggiunto alla scala o evitato.
**The Tabular Numbers Rule.** Le tabelle usano cifre tabulari e colonne numeriche allineate a destra.

## Layout

Barra laterale fissa di 248px (sticky, altezza piena, scorre al proprio interno) piu' colonna principale centrata a 1200px massimo, con padding 36px 32px 56px. Le pagine sono pile di card con 24px di spazio sotto. I form usano una griglia a colonne automatiche (minimo 240px, gap colonne 22px) oppure due colonne fisse; i campi larghi occupano tutta la riga. I filtri usano una griglia con minimo 170px, gap 14px, allineata al fondo. Ritmo ricorrente: 6, 10, 12, 14, 18, 24px. Sotto 860px la barra diventa una fascia orizzontale in alto, il main passa a padding 24px 16px, la card a 18px e le due colonne a una. Gli input hanno larghezza massima 420px fuori dalle griglie.

## Elevation & Depth

Ibrido, per lo piu' tonale: superficie chiara su campo piu' scuro con bordo da 1px; ombra minima sulle card, ombra forte solo per cio' che galleggia.

### Shadow Vocabulary
- **Card** (`box-shadow: 0 1px 2px rgba(22,36,26,0.06), 0 2px 8px rgba(22,36,26,0.04)`): ogni card, a riposo.
- **Pop** (`box-shadow: 0 1px 3px rgba(14,26,18,0.2), 0 10px 28px rgba(14,26,18,0.22)`): toast e card del login.
- **Focus ring dei campi** (`0 0 0 3px rgba(30,122,60,0.2)` piu' bordo verde): solo in focus.

### Named Rules
**The Flat-Until-Floating Rule.** Le superfici di lavoro sono quasi piatte; l'ombra marcata e' per toast e login.

## Shapes

Angoli morbidi ma sobri: 10px per card e toast, 7px per bottoni, campi, tabelle, riquadri e voci della barra; cerchio per il numero del passo. Bordi da 1px in verde chiaro; divisori tratteggiati (1px dashed) per elenchi e ricevute. Le tabelle dentro una card dedicata arrivano a filo dei bordi (padding 0, celle laterali 18px).

## Components

### Buttons
- **Shape:** angoli da 7px, altezza minima 42px, padding 0 20px, testo 0.9375rem peso 600.
- **Primary:** verde erba, testo bianco; hover verde profondo; pressione con scala 0.96; disabilitato in border-strong con testo smorzato.
- **Secondary** (`.btn-secondario`, anche come `a.btn-secondario` per i link con aspetto di bottone): superficie chiara, bordo forte, testo inchiostro, altezza 36px (42px nella variante grande, 32px nelle tabelle dense), hover su surface-alt con bordo verde. Anche il link replica la pressione 0.96.
- **Elimina in due passi:** secondo tocco "Sei sicuro?" in rosso, altezza 36px, entra con scala da 0.92 in 150ms.

### Cards / Containers
- **Corner Style:** 10px. **Background:** surface. **Border:** 1px border. **Shadow:** ombra card. **Padding:** 24px (18px su schermi stretti), margine sotto 24px.
- **Card tabella:** padding 0, tabella a filo, overflow orizzontale se serve.

### Inputs / Fields
- **Style:** surface, bordo forte 1px, 7px, altezza 42px; etichetta sopra in ink-muted 0.875rem peso 500.
- **Hover/Focus:** bordo verde in hover; focus con bordo verde e anello 3px verde al 20%. Placeholder #566a5e (5.5:1).
- **Disabled:** sfondo surface-alt, testo smorzato, cursore non consentito. Obbligatorio con asterisco rosso.
- **Fieldset:** senza bordo, legend a 1.0625rem peso 650, 18px tra fieldset.

### Navigation
Barra laterale verde scurissimo con marchio (icona SVG verde chiaro piu' nome), sezioni in maiuscoletto smorzato, voci con icona SVG a tratto 1.6. Hover su #193523; voce attiva su #1f4a31 con testo bianco, peso 600 e icona verde chiaro. I sottomenu si aprono in altezza naturale con transizione di grid-template-rows (350ms), chevron che ruota di 90 gradi, guida verticale a sinistra; le voci interne sono piu' piccole e smorzate. Utente e uscita in fondo, separati da una linea. Focus: anello verde chiaro interno.

### Tables
Superficie con bordo, testata surface-alt in verde profondo peso 650, righe con divisore, hover verde tenue. Celle 11px 12px; variante densa (Storico) 10px 8px a 0.875rem con bottoni da 32px. Colonne numeriche a destra. Valore basso in danger-text grassetto; riga modificata in giallo tenue.

### Toast
Fisso in alto a destra, 14px 20px, 10px di raggio, ombra pop. Verde per successo, rosso per errore, giallo con testo scuro per avviso. Entra con salita da 16px, scala 0.97 e sfocatura 2px in 350ms, esce in 250ms; tocco per chiudere.

### Empty states
Testo centrato, padding 38px 16px; frase principale in grassetto inchiostro a 1.0625rem, sotto spiegazione smorzata e, se serve, la via d'uscita ("Azzera filtri").

### Step headers (Nuovo movimento)
Intestazione di passo con cerchio verde 26px numerato in bianco e titolo 1.0625rem peso 650; i passi sono separati da una linea di 1px e 22px di spazio.

### Summary banner and info panel
Il riepilogo e' un riquadro verde tenue con bordo forte (peso 500) che conferma cosa sta per succedere; il pannello info e' surface-alt con coppie dt/dd in griglia (dt 0.78rem smorzato, dd peso 600).

### Login backdrop
Unico luogo in cui il tema e' letterale: sfondo verde scuro con strisce di sfalcio verticali da 64px (#1a5029 / #1c5a30) e vignettatura radiale scura; card da 360px con ombra pop e senza bordo, marchio bianco sopra.

### Motion
Scala condivisa: quick 150ms (hover, focus, colori), fast 250ms (chevron, uscita toast), medium 350ms (sottomenu, entrata toast); easing unico cubic-bezier(0.22, 1, 0.36, 1). Pressione dei bottoni a scala 0.96. Dissolvenza di pagina nativa (view transition, 150ms) con la barra laterale che resta ferma grazie al nome proprio. Con prefers-reduced-motion: reduce tutte le durate scendono a 0.01ms e la view transition non e' attiva.

## Do's and Don'ts

### Do:
- **Do** usare solo i token del :root (colori, scala dei font, raggi, ombre, durate) e aggiungerne uno prima di scrivere un valore nuovo.
- **Do** tenere superfici in verde chiaro (#f6faf3 e piu' scure), mai #fff.
- **Do** usare il verde erba pieno solo per l'azione principale della vista; i bottoni secondari per tutto il resto.
- **Do** dare ai bersagli cliccabili almeno 36px di altezza (42px per azioni primarie e campi).
- **Do** far seguire ogni eliminazione da una conferma in due passi e da un toast di esito.
- **Do** verificare il contrasto del testo su ogni nuovo fondo; i valori attuali stanno tra 5.09:1 e 15.28:1.
- **Do** rispettare prefers-reduced-motion per ogni nuova animazione.

### Don't:
- **Don't** usare le strisce di sfalcio fuori dal login: e' l'unico punto letterale del tema.
- **Don't** caricare font, icone o script da risorse esterne: l'app gira offline.
- **Don't** usare il colore come unico segnale: rosso e giallo accompagnano sempre un testo.
- **Don't** introdurre un secondo accento pieno oltre al verde erba.
- **Don't** aggiungere ombre marcate alle card di lavoro: l'ombra pop e' per toast e login.
- **Don't** annidare un button dentro un link: usare `a.btn-secondario`.
