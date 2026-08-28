# Template deck Steering Committee — LTL / Contract Logistics

Struttura del deck ricavata dal template aziendale (`.pptx` fornito
dall'utente). Riproduci l'ordine delle sezioni e le colonne delle
tabelle esattamente come descritto qui; la grafica (palette, layout,
icone) va affinata seguendo le linee guida della skill `pptx` — questo
documento descrive solo contenuto e struttura, non lo stile visivo.

## Struttura generale

1. **Copertina** — titolo area (`LTL e Contract Logistics`), sottotitolo
   `Steering Committee`, mese/anno di riferimento.
2. **Agenda** (slide divisore, ripetuta prima di ogni sezione con la voce
   corrente evidenziata):
   - Summary
   - Focus on Tavoli [nome tavolo, es. TMS]
   - Iniziative
3. **Summary**
4. **Agenda** (divisore)
5. **Focus Tavolo** (una o più, una per "tavolo" attivo) + **Gantt**
   associato
6. **Agenda** (divisore)
7. **Iniziative in corso** (una o più slide, paginate)
8. **Suspended Initiatives** (se presenti iniziative sospese)

## 1. Copertina

Solo titolo area + "Steering Committee" + mese/anno. Nessun contenuto
tabellare.

## 2. Slide Agenda (divisore di sezione)

Elenco fisso delle 3 macro-sezioni (Summary, Focus on Tavoli [X],
Iniziative), con logo aziendale. Ripetuta identica prima di ogni
sezione — non serve evidenziare graficamente la voce corrente nel
contenuto testuale, ma è buona pratica nella versione rifinita.

## 3. Summary

Contenuto per questa slide:

- **Principali aggiornamenti** — 2-4 bullet di sintesi esecutiva del
  periodo (es. "Abbiamo vinto il nuovo tender X", "Riviste le priorità
  dei tavoli Y"). Non inventare: usa solo eventi realmente comunicati
  dall'utente o ricavabili da Jira/riunioni.
- **3 KPI numerici**, sempre in quest'ordine:
  1. Numero di attività in rilascio nei prossimi 30 gg (CR/WAV)
  2. Numero di attività completate negli ultimi 30 gg (CR/WAV)
  3. Numero di nuove attività (CR/WAV)
- **Grafico a barre impilate per fase**, con categorie (righe):
  - `0 - Pipeline`
  - `1 - In Corso`
  - `2 - Completate`
  - `3 - Annullate/Sospese`

  e serie (colonne/fasi): `BR`, `HLD`, `LLD`, `Development`, `Test`,
  `Live`, `Live ultimi 30 giorni` (quest'ultima solo per la riga
  Completate). Conta le CR/WAV in perimetro per fase corrente,
  ricavando la fase da `Project Phase` (skill `jira-pmo`).

Se un numero non è ricavabile dai dati disponibili, riportalo come `TBD`
o `Not available` (vedi `CLAUDE.md` § Data Integrity) invece di stimarlo.

## 4. Focus Tavolo (tabella dettagliata)

Una tabella per "tavolo"/workstream attivo (es. "Focus Tavoli SIMA"),
con colonne in quest'ordine esatto:

```
PRIO | Codice | Tavolo | Descrizione | Stato | Last Updates | Next Step | Live
```

- **PRIO**: ranking numerico interno al tavolo (non è `Product Priority`
  Jira, è un ordinamento manuale delle iniziative del tavolo).
- **Codice**: key Jira (WAV/CR/PRJ).
- **Tavolo**: nome del workstream/processo (es. "Planning", "XDOCK").
- **Descrizione**: sintesi in una frase dello scope.
- **Stato**: fase/step corrente in linguaggio naturale (non
  necessariamente lo `status` Jira testuale — es. "Stima tempi e costi",
  "Hypercare").
- **Last Updates**: sintesi discorsiva degli ultimi eventi rilevanti
  (spesso multi-riga). Fonte: commento Jira `**Stato aggiornato**`
  (`Ultimo stato`) se disponibile, integrato con contesto da riunioni.
- **Next Step**: azioni pianificate, tipicamente con owner tra `@` (es.
  `@Business`, `@T&T/PTV`). Fonte: `Next Steps` da Jira, riformattato
  con gli owner marcati `@Owner`.
- **Live**: data di go-live prevista/effettiva, o `tbd` se non definita.

Righe vuote separatrici tra gruppi di iniziative sono ammesse nel
template originale (usate per separare iniziative correlate) — non è un
errore, riproducile solo se ha senso raggruppare visivamente.

## 5. Gantt del tavolo

Per lo stesso tavolo della slide precedente, un Gantt settimanale:

- Colonne: `Iniziativa` (key), `Descrizione`, `Fase` corrente, poi una
  colonna per settimana (`W1`, `W2`, ... con la data di inizio settimana
  sotto, es. `11/5`) a coprire l'orizzonte del piano (tipicamente
  ~20-22 settimane).
- Per ogni iniziativa, evidenzia sulle settimane pertinenti le fasi
  pianificate (es. "Incontri con Sima e analisi", "Chiusura requisiti",
  "Costi e tempi", "Approval", "Dev", "SIT", "UAT", "Deploy", "HC",
  "Go-Live") con la data di Go-Live finale marcata esplicitamente.
- Includi una legenda dei colori/pattern usati per distinguere le fasi
  (es. Plausibility / HLD / Delivery / Delivery tbc).
- Usa note a piè slide (footnote numerate `¹ ² ³`) per qualificare stime
  provvisorie o dipendenze esterne (es. "Il piano di delivery è
  provvisorio perché ancora da approvare").
- Riporta sempre la data di riferimento del piano in alto alla slide
  (es. "Oggi 24/8").

## 6. Iniziative in corso

Tabella (paginata su più slide se il numero di righe non ci sta in una),
colonne in quest'ordine esatto:

```
ID | TITLE | RAG | % | PHASE | RELEASE | Ultimo Stato | Prossimi Passi
```

- **ID**: key Jira (WAV/CR/PRJ) o `NA` per iniziative non tracciate su
  Jira (es. release tecniche).
- **TITLE**: summary/nome iniziativa.
- **RAG**: indicatore semaforico Red/Amber/Green dello stato di salute
  (colore, non testo) — deriva da una valutazione di rischio (vedi
  `CLAUDE.md` § Deadline Management: Overdue/At Risk/Blocked → Red,
  Due Soon con incertezza → Amber, On Track → Green), non da un campo
  Jira diretto. Non inventare il colore se non c'è base per assegnarlo:
  lascialo vuoto.
- **%**: percentuale di avanzamento (0-100), stimata o comunicata.
- **PHASE**: fase corrente (`BR`, `HLD`, `LLD`, `DEV`, `TEST`, `UAT`,
  `SCOUTING`, `Da avviare`, ...).
- **RELEASE**: data di rilascio pianificata; se cambiata rispetto a una
  data precedente comunicata, puoi riportare `vecchia data nuova data`
  sulla stessa cella (es. `30/04 15/07`) per rendere visibile lo
  slittamento — altrimenti una sola data, o `TBD`/`2027` se lontana/
  incerta.
- **Ultimo Stato**: da commento Jira `**Stato aggiornato**` (skill
  `jira-pmo`), può contenere più righe/bullet.
- **Prossimi Passi**: da `Next Steps` Jira, idem.

Numera le slide se il contenuto è paginato (stesso titolo "Iniziative in
corso" ripetuto).

## 7. Suspended Initiatives

Stessa struttura della tabella "Iniziative in corso" (`ID | TITLE | RAG
| % | PHASE | RELEASE | Ultimo Stato | Prossimi Passi`), ma limitata alle
iniziative sospese. Le colonne `RELEASE`, `Ultimo Stato`, `Prossimi
Passi` sono tipicamente vuote/non applicabili per un'iniziativa sospesa,
a meno che non ci sia un motivo di sospensione noto da riportare in
`Ultimo Stato` (es. "Sospeso su indicazione di ...").

## Note generali

- Non mescolare mai CR/Wave fuori perimetro (vedi filtro `jira-pmo` —
  solo `LTL / B2C` o `Contract Logistics`).
- Ogni cifra (KPI, %, conteggio) deve essere tracciabile a un dato Jira
  o a un'informazione fornita dall'utente — mai stimata per riempire la
  slide.
- Il numero di "tavoli" con Focus dedicato e Gantt varia da SteerCo a
  SteerCo: includi solo quelli su cui l'utente chiede focus in questa
  edizione, non tutti quelli storicamente esistiti.
