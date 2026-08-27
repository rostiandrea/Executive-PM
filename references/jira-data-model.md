# Modello dati Jira

Questo documento spiega come interpretare la struttura degli oggetti Jira
usata da questa organizzazione, così da poter identificare correttamente
gerarchia, campi rilevanti e perimetro di interesse prima di qualunque
estrazione o analisi.

## Gerarchia a livelli

Jira organizza gli oggetti su più livelli, collegati tra loro dal campo
**"my parent is"** (relazione padre → figlio).

### Livello 1 — Iniziativa (INI)

È il "cappello" legato a un'iniziativa di budget.

Informazioni chiave, oltre a titolo, codice e date di inizio/fine:

- **Codici budget**
- **Main Product**
- **Product di riferimento**

### Livello 2 — Progetto (PRJ) o CR (CR)

Sta sotto un'Iniziativa. Può essere un Progetto oppure una CR.

Informazioni chiave, oltre a titolo, codice e date di inizio/fine:

- **Project Manager**
- **Demand Reference**
- **Operations Reference**
- **SME**
- **Main Product**
- **Product di riferimento**

### Livello 3 — Wave (WAV) o CR (CR)

Sta sotto un Progetto. Può essere una Wave oppure un'altra CR.

Informazioni chiave, oltre a titolo, codice e date di inizio/fine:

- **Project Manager**
- **Demand Reference**
- **Operations Reference**
- **SME**
- **Main Product**
- **Product di riferimento**

### Livelli successivi

Sotto le CR e le Wave possono esistere altri oggetti Jira. Per il momento
questi oggetti non vanno considerati nelle analisi di questa skill.

## Legame padre-figlio

Il collegamento tra un oggetto e il suo livello superiore è espresso dal
campo **"my parent is"** sull'oggetto figlio. Usa questo campo per
ricostruire la catena Iniziativa → Progetto/CR → Wave/CR quando serve
contesto (es. per sapere a quale iniziativa/progetto appartiene una Wave).

## Perimetro di interesse (filtro obbligatorio)

Jira contiene anche altri tipi di oggetti che, per il momento, **non vanno
considerati**.

Sono rilevanti solo gli oggetti il cui **Main Product** o **Involved
Product** contiene almeno uno di questi valori:

- `LTL / B2C`
- `Contract Logistics`

Qualsiasi oggetto che non abbia nessuno di questi due valori su Main
Product o Involved Product va escluso da ogni estrazione, monitoraggio o
analisi, anche se altrimenti sembra rilevante.

## Output di monitoraggio richiesto

Per il monitoraggio periodico, l'output atteso è:

> Una lista di tutte le CR o le Wave relative a `LTL / B2C` o
> `Contract Logistics`, ordinata in **ordine crescente per Product
> Priority**, secondo il template descritto in `templates-examples.md`.

Note operative:

- Considera solo oggetti di tipo **CR** o **WAV** (non le Iniziative INI
  né i Progetti PRJ, che restano contesto/padre ma non entrano nella
  lista).
- Applica sempre prima il filtro di prodotto (LTL / B2C o Contract
  Logistics) e poi l'ordinamento per Product Priority crescente.
- Se `Product Priority` manca per un oggetto, indicalo esplicitamente
  (`Not available`) invece di ometterlo o di inventare un valore, e
  posizionalo in coda alla lista con una nota.
- Usa la catena "my parent is" per riportare, quando richiesto,
  l'Iniziativa e il Progetto/CR di appartenenza di ogni CR/Wave elencata.
