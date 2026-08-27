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

- **`Last update` e `What's next`**: sono campi custom dell'app **Structure**
  (ALM Works), non campi Jira nativi/esposti dalla REST API standard. Il
  connettore Atlassian di questa sessione **non li vede**. Riportali sempre
  come `Not available` in estrazione — non è un dato mancante nel senso
  Jira, è un limite del connettore. Se in futuro viene collegato un
  connettore/integrazione Structure dedicato, questi due campi potranno
  essere popolati.
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
  `created`, `updated`).
- Scrivere/aggiornare: `addCommentToJiraIssue` (aggiunge un commento
  nuovo; passando `commentId` aggiorna un commento esistente invece di
  crearne uno nuovo).
- Per un flusso "ultimo commento = stato attuale sintetico", conviene
  aggiornare **sempre lo stesso commento** (salvando il suo `commentId`,
  o convenzionalmente riconoscendolo da un marker testuale tipo
  `**Stato aggiornato**`) invece di accumulare commenti nuovi ogni volta.
