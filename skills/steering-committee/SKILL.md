---
name: steering-committee
description: >
  Preparazione del documento di Steering Committee LTL / Contract
  Logistics (deck PowerPoint periodico con Summary, Focus Tavoli e
  Iniziative in corso, basato su dati Jira CR/Wave/Progetto). Usa questa
  skill quando l'utente chiede di preparare, aggiornare o compilare il
  documento/deck per lo Steering Committee, una presentazione di stato
  progetti per il management, o cita esplicitamente "Steering Committee",
  "SteerCo", "deck per il comitato", "presentazione mensile progetti".
---

# Steering Committee

Questa skill produce il deck PowerPoint periodico di Steering Committee
per l'area LTL/B2C e Contract Logistics, seguendo la struttura e i
formati del template aziendale.

Il *comportamento* dell'agente (tono, prioritizzazione, gestione
scadenze, data integrity) è definito in `CLAUDE.md` alla radice del repo
ed è sempre attivo. I dati sorgente (CR/Wave/Progetto, stato, RAG, fasi,
date) vanno ottenuti seguendo la skill `jira-pmo`.

## Reference files

- **`references/template-steercom.md`** — Struttura slide-per-slide del
  template Steering Committee (copertina, agenda, Summary con KPI e
  grafico per fase, Focus Tavolo con tabella dettagliata e Gantt,
  Iniziative in corso paginate, Suspended Initiatives), con le colonne
  esatte di ogni tabella e le convenzioni di contenuto. Leggi questo
  prima di generare o aggiornare il deck.

## Come generare il deck

1. **Raccogli i dati.** Usa la skill `jira-pmo` per estrarre CR/Wave/
   Progetti in perimetro (`LTL / B2C`, `Contract Logistics`), con stato,
   fase, % avanzamento, release date, Ultimo stato/Next Steps.
2. **Segui la struttura di `template-steercom.md`** per popolare le
   sezioni (Summary, eventuali Focus Tavolo, Iniziative in corso,
   Suspended Initiatives). Non inventare KPI o percentuali: se un dato
   manca, riportalo come `Not available` o `TBD` (vedi `CLAUDE.md` §
   Data Integrity).
3. **Genera il file `.pptx`** con la skill `pptx` di sistema, riusando
   layout, palette e loghi del template aziendale esistente (quando
   disponibile un file `.pptx` di partenza, editalo invece di ripartire
   da zero — vedi la sezione "Editing existing decks" della skill
   `pptx`). La grafica va sempre affinata rispetto alla bozza raw: segui
   le linee guida di design della skill `pptx` (palette coerente, un
   solo elemento visivo dominante per slide, niente slide di solo testo).
4. **Non inventare dati.** Se il numero di iniziative attive/completate/
   nuove, o un valore RAG, non è ricavabile dai dati Jira disponibili,
   segnalalo esplicitamente invece di stimarlo.
