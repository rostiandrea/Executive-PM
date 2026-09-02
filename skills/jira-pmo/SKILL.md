---
name: jira-pmo
description: >
  Interpretazione e estrazione dati Jira per il PMO Arcese (gerarchia
  Iniziativa/Progetto/CR/Wave, filtro di perimetro LTL/B2C e Contract
  Logistics, mapping custom field, JQL verificata, convenzione dei
  commenti "Stato aggiornato"). Usa questa skill ogni volta che serve
  interpretare, estrarre, filtrare o monitorare dati Jira — es. "estrai
  le CR aperte", "dammi lo stato dei progetti", "controlla le scadenze
  Jira", "lista di monitoraggio CR/Wave", "chi sta seguendo questa
  iniziativa", "aggiorna il commento di stato su Jira" — anche quando
  l'utente non dice esplicitamente "Jira".
---

# Jira PMO

Questa skill spiega come leggere la struttura Jira di questa
organizzazione e come estrarla tecnicamente via connettore Atlassian, in
modo consistente e riusabile (non riscoprire ogni volta cloudId, field ID
e JQL).

Il *comportamento* dell'agente (tono, prioritizzazione, gestione
scadenze) è definito in `CLAUDE.md` alla radice del repo ed è sempre
attivo — questa skill copre solo la parte "dati Jira".

## Reference files

- **`references/jira-data-model.md`** — Come Jira è strutturato per
  questa organizzazione: la gerarchia Iniziativa (INI) → Progetto/CR
  (PRJ/CR) → Wave/CR (WAV/CR), il collegamento `"my parent is"`, i campi
  rilevanti per livello, e il filtro di perimetro obbligatorio (solo
  oggetti con Main Product o Involved Product in `LTL / B2C` o
  `Contract Logistics`). Leggi questo prima di interpretare o estrarre
  qualunque dato Jira.

- **`references/jira-extraction-recipe.md`** — La ricetta tecnica
  verificata per l'estrazione via connettore Atlassian: cloudId, project
  key (CR/PRJ/WAV/INI), mapping field ID → nome, JQL di base, come
  risolvere la catena Iniziativa/Progetto, limiti noti del connettore
  (campi Structure, testo checklist), e come leggere/scrivere i commenti
  Jira — inclusa la convenzione `**Stato aggiornato**` che alimenta le
  colonne `Ultimo stato` / `Next Steps`. Leggi questo prima di lanciare
  un'estrazione CR/Wave per riusare la query e i field ID già noti.

- **`references/templates-examples.md`** — Il template di estrazione dati
  (colonne + esempio reale) e il formato della lista di monitoraggio
  CR/Wave, più il formato per segnalare un mismatch riunione-vs-Jira.
  Leggi questo prima di produrre qualunque estrazione o monitoraggio
  Jira così l'output rispetta esattamente il formato atteso.

- **`references/sal-minute-template.md`** — Il formato esatto (oggetto,
  struttura, stile) della minuta di SAL interno di Prodotto quando viene
  richiesta **in formato mail** — diverso dalla lista di monitoraggio a
  tabella. Leggi questo quando l'utente chiede un recap/minuta di SAL da
  inviare via mail, e usalo anche per collegare la minuta alla proposta
  di aggiornamento dei commenti `**Stato aggiornato**` su Jira.

## Core workflow

1. **Interpreta la gerarchia e applica il filtro.** Usa
   `jira-data-model.md` per identificare il livello di ogni oggetto,
   risolvere il parent/child via `"my parent is"`, e filtrare a Main
   Product/Involved Product `LTL / B2C` o `Contract Logistics`. Ignora
   tutto il resto.
2. **Riusa la ricetta tecnica.** Usa `jira-extraction-recipe.md` per
   cloudId, JQL, field mapping e pipeline di estrazione (paginazione,
   proiezione jq) invece di riscoprirli ogni volta.
3. **Produci output nel formato atteso.** Usa `templates-examples.md` —
   in particolare, per un monitoraggio CR/Wave, ordina **crescente per
   Product Priority** con le colonne del template.
4. **Non inventare mai un dato mancante** — vedi la sezione Data
   Integrity in `CLAUDE.md` (`Not available` / `TBD`).
