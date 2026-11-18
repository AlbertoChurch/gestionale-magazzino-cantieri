/* Liste a tendina con ricerca.

   Trasforma ogni <select> in un campo in cui si puo' scrivere: mentre scrivi compaiono
   le voci esistenti piu' vicine a quello che cerchi; un clic sul campo o sulla freccia
   apre l'elenco intero. Si possono scegliere solo voci che esistono.

   Il <select> originale resta nella pagina (nascosto, sopra il campo) e rimane la fonte
   dei dati: l'invio del form, i controlli "obbligatorio", gli onchange e il codice che
   legge o imposta select.value continuano a funzionare senza modifiche.
   Per escludere una lista: data-combo="no". */
(function () {
    'use strict';

    var contatore = 0;
    var proprietaValore = Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, 'value');
    var proprietaIndice = Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, 'selectedIndex');
    var ALTEZZA_MASSIMA = 280;

    function normalizza(testo) {
        return String(testo || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();
    }

    function nomeAccessibile(select) {
        if (select.getAttribute('aria-label')) return select.getAttribute('aria-label');
        var etichetta = select.closest('label');
        var primo = etichetta && etichetta.firstChild;
        return primo && primo.nodeType === 3 ? primo.textContent.trim() : '';
    }

    function potenzia(select) {
        if (select.multiple || select.size > 1 || select.dataset.combo === 'no' || select.closest('.combo')) return;

        var id = 'combo-' + (++contatore);
        var aveva_il_focus = document.activeElement === select;
        var contenitore = document.createElement('div');
        contenitore.className = 'combo';
        select.parentNode.insertBefore(contenitore, select);
        contenitore.appendChild(select);
        select.classList.add('combo-nativo');
        select.tabIndex = -1;
        select.setAttribute('aria-hidden', 'true');

        var campo = document.createElement('input');
        campo.type = 'text';
        campo.className = 'combo-input';
        campo.setAttribute('autocomplete', 'off');
        campo.setAttribute('autocapitalize', 'off');
        campo.spellcheck = false;
        campo.setAttribute('role', 'combobox');
        campo.setAttribute('aria-autocomplete', 'list');
        campo.setAttribute('aria-haspopup', 'listbox');
        campo.setAttribute('aria-controls', id + '-lista');
        campo.setAttribute('aria-expanded', 'false');
        if (nomeAccessibile(select)) campo.setAttribute('aria-label', nomeAccessibile(select));

        var freccia = document.createElement('span');
        freccia.className = 'combo-freccia';
        freccia.setAttribute('aria-hidden', 'true');
        freccia.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>';

        var lista = document.createElement('ul');
        lista.className = 'combo-lista';
        lista.id = id + '-lista';
        lista.setAttribute('role', 'listbox');
        if (nomeAccessibile(select)) lista.setAttribute('aria-label', nomeAccessibile(select));
        lista.hidden = true;

        contenitore.appendChild(campo);
        contenitore.appendChild(freccia);
        contenitore.appendChild(lista);
        if (aveva_il_focus) campo.focus();

        var aperta = false;
        var filtro = null;          // null = elenco intero; stringa = quello che l'utente ha scritto
        var risultati = [];
        var attivo = -1;

        // Per un campo obbligatorio (o marcato data-segnaposto) la voce con valore vuoto e'
        // solo un invito ("Seleziona..."): si mostra in grigio e non e' scegliibile.
        // Altrimenti ("Tutti", "Non specificata") e' una vera scelta.
        function eSegnaposto() { return select.required || select.hasAttribute('data-segnaposto'); }

        function opzioni() {
            return Array.prototype.map.call(select.options, function (o, indice) {
                return { indice: indice, valore: o.value, testo: o.text, disabilitata: o.disabled, vuota: o.value === '' };
            });
        }

        function testoCorrente() {
            var o = select.options[select.selectedIndex];
            if (!o) return '';
            if (o.value === '' && eSegnaposto()) return '';
            return o.text;
        }

        function testoSegnaposto() {
            var vuota = Array.prototype.find.call(select.options, function (o) { return o.value === ''; });
            return vuota ? vuota.text : '';
        }

        function haFiltro() { return !!(filtro && normalizza(filtro)); }

        function sincronizza() {
            // se le opzioni cambiano mentre l'utente sta scrivendo, non gli si cancella il testo
            if (!(aperta && filtro !== null)) campo.value = testoCorrente();
            campo.placeholder = eSegnaposto() ? testoSegnaposto() : '';
            campo.setAttribute('aria-required', select.required ? 'true' : 'false');
            campo.disabled = select.disabled;
            contenitore.classList.toggle('disabilitato', select.disabled);
            if (select.disabled && aperta) chiudi(false);
            if (aperta) disegna();
        }

        function calcolaRisultati() {
            var parole = filtro ? normalizza(filtro).split(/\s+/).filter(Boolean) : [];
            var trovati = opzioni().filter(function (o) {
                if (o.disabilitata) return false;
                if (o.vuota) return !parole.length && !eSegnaposto();
                if (!parole.length) return true;
                var testo = normalizza(o.testo);
                return parole.every(function (p) { return testo.indexOf(p) !== -1; });
            });
            if (parole.length) {
                trovati.sort(function (a, b) {
                    var sa = normalizza(a.testo).indexOf(parole[0]) === 0 ? 0 : 1;
                    var sb = normalizza(b.testo).indexOf(parole[0]) === 0 ? 0 : 1;
                    return (sa - sb) || (a.indice - b.indice);
                });
            }
            return trovati;
        }

        function evidenzia(riga, testo) {
            // un unico contenitore: la riga e' un flex e le parti del testo non devono
            // diventare elementi separati
            var contenuto = document.createElement('span');
            contenuto.className = 'combo-testo';
            riga.appendChild(contenuto);
            // ricerca senza accenti/maiuscole: si tiene la corrispondenza fra ogni lettera
            // normalizzata e la sua posizione nel testo originale, per evidenziare quella giusta
            var cercato = normalizza(filtro || '');
            var normale = '';
            var mappa = [];
            for (var i = 0; i < testo.length; i++) {
                var pezzo = testo.charAt(i).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
                for (var k = 0; k < pezzo.length; k++) { normale += pezzo.charAt(k); mappa.push(i); }
            }
            var posizione = cercato ? normale.indexOf(cercato) : -1;
            if (posizione < 0) { contenuto.textContent = testo; return; }
            var inizio = mappa[posizione];
            var fine = mappa[posizione + cercato.length - 1] + 1;
            var forte = document.createElement('strong');
            forte.className = 'combo-evidenza';
            forte.textContent = testo.substring(inizio, fine);
            contenuto.appendChild(document.createTextNode(testo.substring(0, inizio)));
            contenuto.appendChild(forte);
            contenuto.appendChild(document.createTextNode(testo.substring(fine)));
        }

        function impostaAttivo(posizione, senzaScorrere) {
            var righe = lista.querySelectorAll('.combo-opzione');
            if (righe[attivo]) righe[attivo].classList.remove('combo-attiva');
            attivo = posizione;
            if (righe[attivo]) {
                righe[attivo].classList.add('combo-attiva');
                campo.setAttribute('aria-activedescendant', righe[attivo].id);
                if (!senzaScorrere) righe[attivo].scrollIntoView({ block: 'nearest' });
            } else {
                campo.removeAttribute('aria-activedescendant');
            }
        }

        function disegna() {
            risultati = calcolaRisultati();
            lista.textContent = '';
            attivo = -1;
            if (!risultati.length) {
                var nessuno = document.createElement('li');
                nessuno.className = 'combo-nessuno';
                nessuno.setAttribute('role', 'option');
                nessuno.setAttribute('aria-disabled', 'true');
                nessuno.textContent = 'Nessun risultato';
                lista.appendChild(nessuno);
                campo.removeAttribute('aria-activedescendant');
                return;
            }
            risultati.forEach(function (o, posizione) {
                var riga = document.createElement('li');
                riga.className = 'combo-opzione' + (o.vuota ? ' combo-opzione-vuota' : '');
                riga.id = id + '-' + posizione;
                riga.setAttribute('role', 'option');
                riga.setAttribute('aria-selected', o.indice === select.selectedIndex ? 'true' : 'false');
                riga.dataset.posizione = posizione;
                evidenzia(riga, o.testo);
                lista.appendChild(riga);
            });
            if (haFiltro()) {
                impostaAttivo(0);
            } else {
                var scelta = risultati.findIndex(function (o) { return o.indice === select.selectedIndex; });
                if (scelta >= 0) impostaAttivo(scelta);
            }
        }

        function posiziona() {
            var rettangolo = campo.getBoundingClientRect();
            var sotto = window.innerHeight - rettangolo.bottom;
            var sopra = rettangolo.top;
            var inAlto = sotto < 220 && sopra > sotto;
            lista.classList.toggle('sopra', inAlto);
            lista.style.maxHeight = Math.max(140, Math.min(ALTEZZA_MASSIMA, (inAlto ? sopra : sotto) - 16)) + 'px';
        }

        function apri(testoFiltro) {
            if (select.disabled) return;
            filtro = testoFiltro;
            aperta = true;
            lista.hidden = false;
            campo.setAttribute('aria-expanded', 'true');
            contenitore.classList.add('aperto');
            posiziona();
            disegna();
        }

        function chiudi(ripristina) {
            aperta = false;
            filtro = null;
            lista.hidden = true;
            campo.setAttribute('aria-expanded', 'false');
            campo.removeAttribute('aria-activedescendant');
            contenitore.classList.remove('aperto');
            if (ripristina) campo.value = testoCorrente();
        }

        function scegli(o) {
            var cambiata = select.selectedIndex !== o.indice;
            proprietaIndice.set.call(select, o.indice);
            chiudi(false);
            campo.value = testoCorrente();
            if (cambiata) {
                select.dispatchEvent(new Event('input', { bubbles: true }));
                select.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }

        campo.addEventListener('focus', function () { campo.select(); });
        campo.addEventListener('click', function () { if (!aperta) apri(null); });
        campo.addEventListener('input', function () { apri(campo.value); });

        campo.addEventListener('keydown', function (evento) {
            var tasto = evento.key;
            if (tasto === 'ArrowDown' || tasto === 'ArrowUp') {
                evento.preventDefault();
                if (!aperta) {
                    apri(null);
                    if (attivo < 0 && risultati.length) impostaAttivo(0);
                } else if (risultati.length) {
                    if (tasto === 'ArrowDown') impostaAttivo(attivo < 0 ? 0 : Math.min(risultati.length - 1, attivo + 1));
                    else impostaAttivo(Math.max(0, attivo - 1));
                }
            } else if (tasto === 'Enter') {
                evento.preventDefault();
                if (aperta && attivo >= 0) scegli(risultati[attivo]);
            } else if (tasto === 'Escape') {
                if (aperta) { evento.preventDefault(); evento.stopPropagation(); chiudi(true); }
            } else if (tasto === 'Tab') {
                if (aperta && haFiltro() && attivo >= 0) scegli(risultati[attivo]);
            }
        });

        campo.addEventListener('blur', function () {
            var scritto = normalizza(campo.value);
            if (scritto) {
                // se il testo e' quello della voce gia' scelta non si cambia nulla: con piu'
                // voci dal testo identico (es. due lotti uguali) altrimenti la scelta
                // salterebbe in silenzio sulla prima
                var corrente = select.options[select.selectedIndex];
                if (corrente && normalizza(corrente.text) === scritto) { chiudi(true); return; }
                var esatta = opzioni().find(function (o) { return !o.disabilitata && !o.vuota && normalizza(o.testo) === scritto; });
                if (esatta) { if (select.selectedIndex !== esatta.indice) scegli(esatta); else chiudi(true); return; }
            } else if (!select.required) {
                var vuota = opzioni().find(function (o) { return o.vuota && !o.disabilitata; });
                if (vuota) { if (select.selectedIndex !== vuota.indice) scegli(vuota); else chiudi(true); return; }
            }
            chiudi(true);
        });

        lista.addEventListener('mousedown', function (evento) { evento.preventDefault(); });
        lista.addEventListener('click', function (evento) {
            evento.preventDefault();
            var riga = evento.target.closest('.combo-opzione');
            if (riga) scegli(risultati[Number(riga.dataset.posizione)]);
        });
        lista.addEventListener('mousemove', function (evento) {
            var riga = evento.target.closest('.combo-opzione');
            if (riga && Number(riga.dataset.posizione) !== attivo) impostaAttivo(Number(riga.dataset.posizione), true);
        });

        freccia.addEventListener('mousedown', function (evento) { evento.preventDefault(); });
        freccia.addEventListener('click', function (evento) {
            evento.preventDefault();
            if (select.disabled) return;
            if (aperta) { chiudi(true); return; }
            campo.focus();
            apri(null);
        });

        // Il codice della pagina continua a leggere/impostare select.value come prima:
        // ogni impostazione dall'esterno aggiorna anche il testo visibile.
        Object.defineProperty(select, 'value', {
            configurable: true,
            get: function () { return proprietaValore.get.call(select); },
            set: function (valore) { proprietaValore.set.call(select, valore); sincronizza(); }
        });
        Object.defineProperty(select, 'selectedIndex', {
            configurable: true,
            get: function () { return proprietaIndice.get.call(select); },
            set: function (indice) { proprietaIndice.set.call(select, indice); sincronizza(); }
        });
        select.addEventListener('change', sincronizza);
        // Chi cerca di mettere a fuoco il <select> (autofocus, avviso "campo obbligatorio")
        // arriva invece sul campo visibile.
        select.addEventListener('focus', function () { campo.focus(); });
        new MutationObserver(sincronizza).observe(select, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ['disabled'] });
        if (select.form) select.form.addEventListener('reset', function () { setTimeout(sincronizza, 0); });

        sincronizza();
    }

    document.querySelectorAll('select').forEach(potenzia);
})();
