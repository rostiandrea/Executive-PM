# Ricetta di estrazione Jira (CR / Wave) — riusa questa, non ripartire da zero

Questo file documenta *come* eseguire tecnicamente l'estrazione descritta in
`jira-data-model.md` e `templates-examples.md` tramite il connettore
Atlassian (Jira Cloud). Leggilo prima di lanciare qualunque estrazione CR/Wave
così da riusare cloudId, chiavi progetto, JQL e field mapping già scoperti,
invece di ririsalirli ogni volta.

## Istanza e cloudId

- Sito: `arcese.atlassian.net`
- `cloudId`: `24113ed2-2fb1-40f0-9a18-01ebc6c7c4c5`
  (recuperabile anche con `getAccessibleAtlassianResources` se cambia).

## Progetti Jira coinvolti nella gerarchia PMO

La gerarchia Iniziativa → Progetto/CR → Wave/CR descritta in
`jira-data-model.md` è distribuita su progetti Jira dedicati (non issue type
dentro un unico progetto):

| Livello                    | Project key | Nome progetto Jira    | Issue type principale |
|-----------------------------|-------------|------------------------|------------------------|
| Iniziativa                  | `INI`       | (categoria Management) | —                      |
| Progetto (liv. 2)            | `PRJ`       | —                       | `Arcese project`       |
| CR (liv. 2 o 3)              | `CR`        | Change requests         | `Change request`       |
| Wave (liv. 3)                | `WAV`       | Waves                   | `Wave`                 |

Attenzione: esiste anche un issue type generico "Change request" usato in
molti altri progetti applicativi (es. `WOA`, `TEMPCR`, `OCR`, ecc.) che
**non c'entra nulla** con la gerarchia PMO — sono CR tecniche di team dev.
Filtra sempre per `project in (CR, WAV)`, mai per solo `issuetype`.

## Query JQL di base per il monitoraggio CR/Wave

```
project in (CR, WAV)
AND ("Main product" in ("LTL / B2C", "Contract Logistics")
     OR "Involved products" in ("LTL / B2C", "Contract Logistics"))
AND status != "Annullato"
ORDER BY key
```

Al 2026-08-27 restituisce ~310 issue. Usa `searchJiraIssuesUsingJql` con
`maxResults: 100` e pagina con `nextPageToken` finché
`pageInfo.hasNextPage` è `false`. Se serve solo il conteggio, usa
`searchResultMode: "count"` prima di paginare.

I risultati sono grandi: il tool salva l'output su file quando supera il
limite di token. Non provare a leggerlo con `Read`: usa `jq` per estrarre
subito solo i campi che servono e scarta il resto (vedi sotto).

## Field ID → nome (custom field mapping scoperto)

Recuperato una volta con `getJiraIssue(..., expand:"names")` su `WAV-280`.
Questi ID sono stabili per questa istanza Jira, riusali direttamente nelle
query invece di rifare la scoperta:

| Field ID              | Nome Jira                  | Colonna nel template          |
|------------------------|------------------------------|--------------------------------|
| `customfield_10677`   | Product Priority             | Product Priority               |
| `customfield_10290`   | Main product                 | Main product                   |
| `customfield_10291`   | Involved products             | (filtro perimetro)             |
| `customfield_10319`   | Project Phase                 | Project Phase                  |
| `customfield_10311`   | Requested live date           | Requested live date            |
| `duedate`             | Data di scadenza              | Release Date                   |
| `customfield_10306`   | Demand ref.                    | Demand ref.                    |
| `customfield_10307`   | SME Factory                    | SME Factory                    |
| `customfield_10308`   | Operation ref.                 | Operation ref.                 |
| `customfield_10313`   | Project manager                | Project manager                |
| `customfield_10289`   | Requestor                      | Requestor                      |
| `labels`               | Etichette                      | Etichette                      |
| `customfield_10941`   | OLD key                        | OLD key                        |
| `customfield_11139`   | BR Actual Start Date           | BR Actual Start Date           |
| `customfield_11140`   | BR Actual Due Date             | BR Actual Due Date             |
| `customfield_11046`   | BR Planned Start Date          | BR Planned Start Date          |
| `customfield_11048`   | BR Planned Due Date            | BR Planned Due Date            |
| `customfield_11141`   | HLD Actual Start Date          | HLD Actual Start Date          |
| `customfield_11142`   | HLD Actual Due Date            | HLD Actual Due Date            |
| `customfield_11049`   | HLD Planned Start Date         | HLD Planned Start Date         |
| `customfield_11051`   | HLD Planned Due Date           | HLD Planned Due Date           |
| `status`               | Stato                          | Status (compare 2 volte)       |
| `issuelinks`           | Ticket collegati (per parent)   | usato per Iniziativa/Progetto  |
| `customfield_10135`   | Checklist Progress (testo, es. "Checklist: 3/4") | — |
| `customfield_10136`   | Checklist Progress %           | — |
| `customfield_10137`   | Checklist Template              | vedi limitazioni sotto         |
| `customfield_10138`   | Checklist Text (view-only)      | vedi limitazioni sotto         |

### Campi NON disponibili tramite il connettore Atlassian

- **`Last update` e `What's next` (i campi Jira nativi dell'app Structure)**:
  sono campi custom dell'app **Structure** (ALM Works), non campi Jira
  nativi/esposti dalla REST API standard. Il connettore Atlassian di questa
  sessione **non li vede** e non c'è modo di leggerli.
  **Dal 2026-08-27 queste due colonne del template non vengono più
  lasciate `Not available` per definizione**: sono state sostituite da
  `Ultimo stato` e `Next Steps`, popolate leggendo l'ultimo commento Jira
  con marker `**Stato aggiornato**` sulla issue (vedi § Commenti Jira /
  Convenzione "Stato aggiornato" più sotto) — un surrogato mantenuto da
  Claude su richiesta dell'utente, non un campo Structure. Se una CR/Wave
  non ha (ancora) un commento con quel marker, riporta `Not available` per
  entrambe.
- **Testo dei singoli item della checklist**: verificato su `CR-190`
  (checklist "3/4", 75%) che `customfield_10137` e `customfield_10138`
  tornano `null` anche quando la checklist esiste e ha progresso. Il
  connettore espone solo il *riepilogo* (`customfield_10135`,
  `customfield_10136`), non il testo/owner/due date dei singoli punti.
  Per leggere i punti checklist (formato "Attività [Owner] (Due date)")
  serve verificare caso per caso se sono ricostruibili (es. via commenti,
  o via un'altra rappresentazione del campo) prima di fare affidamento su
  questa lettura in automatico.

## Risalire Iniziativa/Progetto (catena "my parent is")

Il link è di tipo `Hierarchy`, con `type.outward == "my parent is"` su
**tutti** i link della issue (anche quelli verso i figli, dove
`outwardIssue` è `null`). Filtra sempre anche su `outwardIssue != null`,
altrimenti si rischia di prendere il primo link sbagliato:

```
[.fields.issuelinks[]?
  | select(.type.outward=="my parent is" and .outwardIssue != null)
  | {key: .outwardIssue.key, summary: .outwardIssue.fields.summary}
][0]
```

Algoritmo:
1. Richiama `issuelinks` per ogni CR/Wave nella query principale.
2. Estrai il parent immediato con il filtro sopra.
   - Se il parent è `INI-...` → è già l'Iniziativa, non c'è Progetto/CR
     intermedio (CR di livello 2).
   - Se il parent è `PRJ-...` o `CR-...` → è il Progetto/CR (livello 2),
     serve un secondo hop per risalire all'Iniziativa.
3. Per il secondo hop, raccogli le chiavi parent uniche (`PRJ-*`/`CR-*`,
   tipicamente poche decine anche su centinaia di CR/Wave) e fai un'unica
   query aggiuntiva `key in (...)` con `fields: ["summary","issuelinks"]`
   per risolvere il loro parent (Iniziativa).
4. Se manca del tutto il link "my parent is" (capita, non è un errore da
   correggere), riporta `Not available`.

## Pipeline pratica (evita di intasare il contesto)

1. Esegui la JQL con `fields` minimi necessari (inclusi `issuelinks` se
   serve la catena parent).
2. Ogni pagina viene salvata su file dal tool se supera il limite di
   token — è normale, non è un errore.
3. Usa `jq` per proiettare subito ogni pagina in JSONL compatto (una riga
   per issue, solo i campi utili) in uno scratch file, poi concatena le
   pagine.
4. Fai lo stesso per i parent (`PRJ`/`CR` unici) in un secondo file JSONL.
5. Costruisci l'output finale (xlsx o tabella) leggendo solo i JSONL
   compatti, mai i dump grezzi.

## Commenti Jira

- Leggere: `getJiraIssue` con `fields: ["comment"]` (torna
  `fields.comment.comments[]`, con `author`, `body` in ADF/markdown,
  `created`, `updated`). Per molte issue insieme, usa
  `searchJiraIssuesUsingJql` con `key in (...)` e `fields: ["comment"]`
  invece di una `getJiraIssue` per issue.
- Scrivere/aggiornare: `addCommentToJiraIssue` (aggiunge un commento
  nuovo; passando `commentId` aggiorna un commento esistente invece di
  crearne uno nuovo).

### Convenzione "Stato aggiornato" (fonte di `Ultimo stato` / `Next Steps`)

Dal 2026-08-27 questo è il meccanismo standard, sostituisce i campi
Structure irraggiungibili `Last update`/`What's next` nel template di
estrazione (vedi `templates-examples.md`).

**Formato del commento** (markdown), scritto/aggiornato da Claude a
partire da input dell'utente (es. un file Excel con colonne `Key`,
`Stato`, `Next Steps`, o minute di riunione):

```
**Stato aggiornato** (DD/MM/YYYY)

**Stato:** <sintesi stato attuale>

**Next steps:**
- <attività 1> (Owner <nome> - Due date <data o tbd>)
- <attività 2> (Owner <nome> - Due date <data o tbd>)
```

La sezione `**Next steps:**` è opzionale (ometterla se non ci sono next
step da riportare); la sezione `**Stato:**` è opzionale allo stesso modo
se si vuole riportare solo i next step.

**Scrittura — sempre 1 commento marcato per issue, mai duplicarlo:**
1. Leggi i commenti esistenti della issue (`fields: ["comment"]`).
2. Cerca un commento il cui `body` inizi con `**Stato aggiornato**`.
3. Se esiste, aggiorna **quello stesso commento** passando il suo `id`
   come `commentId` ad `addCommentToJiraIssue` (non crearne uno nuovo).
4. Se non esiste, crea un nuovo commento con `addCommentToJiraIssue`
   (senza `commentId`).
5. Aggiorna sempre la data `(DD/MM/YYYY)` nell'intestazione con la data
   dell'aggiornamento corrente.

**Lettura — per popolare `Ultimo stato` / `Next Steps` in estrazione:**
1. Fra i commenti della issue, prendi l'ultimo (per `created`/`updated`)
   il cui `body` inizia con `**Stato aggiornato**`. Se non ce n'è nessuno
   → entrambe le colonne `Not available`.
2. `Ultimo stato` = testo dopo `**Stato:**` fino alla riga vuota
   successiva (o fino a `**Next steps:**` se non c'è riga vuota).
3. `Next Steps` = le righe bullet (`- ...`) sotto `**Next steps:**`,
   riportate come da originale (contengono già `Owner` e `Due date`
   nel testo libero — non serve parsarle in campi separati, ma sono già
   nel formato "Attività (Owner ... - Due date ...)" utile per capire a
   colpo d'occhio se un next step ha una scadenza definita o è `tbd`).
4. Se manca solo `**Stato:**` o solo `**Next steps:**` nel commento
   trovato, la colonna mancante è `Not available`.

**Esempio reale** (CR-438, commento id 35612, creato 2026-08-27):
```
**Stato aggiornato** (27/08/2026)

**Stato:** In validazione LT

**Next steps:**
- Validazione documento approval (owner LT entro 10/9)
```
→ `Ultimo stato` = "In validazione LT",
  `Next Steps` = "Validazione documento approval (owner LT entro 10/9)".

### Convenzione "💶 Costi e Benefici" (fonte del campo `costiBenefici`)

Dal 2026-08-27, stesso pattern della convenzione "Stato aggiornato" ma per
i dati economici di una CR/Wave (benefici annui, capex, opex esterni/interni,
giorni interni). **Importante**: questi valori vivono SOLO come commento
Jira — non esiste un campo custom dedicato — quindi se una sessione diversa
rigenera l'estrazione senza leggere anche questo commento, il dato sparisce
dalla dashboard al refresh successivo pur restando su Jira. Va sempre letto
insieme al commento "Stato aggiornato" nello stesso fetch dei commenti.

**Formato del commento** (markdown), scritto/aggiornato da Claude su
richiesta esplicita dell'utente (es. "per CR-xxx metti benefici annui
5000€, capex 2000€, opex esterni 0, opex interni 900€, 3 gg interni"):

```
**💶 Costi e Benefici**

| Voce | Valore |
| --- | --- |
| Benefici Annui | <valore o "Not available" o descrizione qualitativa> |
| Costi Capex | <valore o "Not available"> |
| Costi Opex - esterni | <valore o "Not available"> |
| Costi Opex - interni | <valore o "Not available"> |
| GG Interni | <valore o "Not available"> |

_Aggiornato il DD/MM/YYYY - Executive PM tracker_
```

I valori NON sono sempre numerici: possono essere importi (`€ 2.800`),
giorni (`3 gg`), o testo qualitativo (`non stimabili - solo qualitativi`,
`Must Have Normativo`, `In stima`, `Not available`). Vanno riportati così
come forniti dall'utente, senza forzare un formato numerico.

**Scrittura — sempre 1 commento marcato per issue, mai duplicarlo:**
Stessa procedura della convenzione "Stato aggiornato" (cerca un commento
il cui `body` contenga `💶 Costi e Benefici`; se esiste aggiornalo con
`commentId`, altrimenti creane uno nuovo; aggiorna sempre la data in
`_Aggiornato il DD/MM/YYYY..._`).

**Lettura — per popolare `costiBenefici` in estrazione:**
1. Fra i commenti della issue, prendi l'ultimo il cui `body` contiene
   `💶 Costi e Benefici`.
2. Estrai le 5 righe della tabella per etichetta (`Benefici Annui`,
   `Costi Capex`, `Costi Opex - esterni`, `Costi Opex - interni`,
   `GG Interni`) col valore della seconda colonna, come stringa.
3. Se non c'è nessun commento con questo marker, `costiBenefici` è `null`
   (il drawer della dashboard non mostra la sezione).
4. Implementato in `dashboard/build_dashboard_data.py`
   (`parse_costi_benefici`) — legge dal campo `cbComment` di ogni riga di
   `full_all.jsonl`, popolato allo stesso modo di `statoComment` (vedi
   Passo 2 di `dashboard/README.md`: nella query dei commenti per ogni
   issue, va cercato ANCHE questo marker, non solo "Stato aggiornato").

**Esempio reale** (WAV-323, commento id 35681, creato 2026-08-27):
```
**💶 Costi e Benefici**

| Voce | Valore |
| --- | --- |
| Benefici Annui | € 5.416 / anno |
| Costi Capex | € 2.800 |
| Costi Opex - esterni | € 0 |
| Costi Opex - interni | € 900 |
| GG Interni | 3 gg |

_Aggiornato il 27/08/2026 - Executive PM tracker_
```
