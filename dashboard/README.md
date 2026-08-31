# Procedura di refresh automatico della dashboard "Product Team Management"

Questo documento descrive, passo per passo, come rigenerare i dati Jira e
ripubblicare l'artifact della dashboard **senza perdere le modifiche fatte
dagli utenti dentro la pagina** (stato, ultimo stato, next steps aggiunti/
completati/eliminati). È pensato per essere eseguibile da una sessione
Claude "fresca" (senza contesto della conversazione originale), quindi ogni
passo è esplicito.

- **URL fisso dell'artifact**: `https://claude.ai/code/artifact/8490f5ab-9201-47ed-83e2-09894ac25bcf`
  (va sempre passato come `url` nella action `publish`, mai omesso, altrimenti
  si crea un artifact nuovo invece di aggiornare quello esistente).
- **Title**: `Product Team Management`
- **Favicon**: `🚦`
- **Capabilities**: `{"artifact": {}}`
- File sorgenti nel repo: `dashboard/dashboard_template.html`,
  `dashboard/build_dashboard_data.py`, `dashboard/publish_dashboard.py`,
  `dashboard/grandparents.jsonl` (cache della catena Iniziativa/Progetto).

## Attenzione — sessioni Claude Code parallele / branch multipli

Questo artifact può essere modificato sia dall'utente nel browser, sia da
un'ALTRA sessione Claude Code (una chat diversa, magari su un branch
diverso) che pubblica una propria versione. Il Passo 1 protegge le
modifiche fatte dall'utente NELLA PAGINA (stato, next steps — vivono in
`edits-data`), ma **non protegge funzionalità di codice aggiunte da
un'altra sessione** se questa sessione ricostruisce l'HTML da un
`dashboard/dashboard_template.html` locale/di branch più vecchio: il
publish sovrascrive silenziosamente sia il codice che eventuali dati che
quella funzionalità portava con sé. È già successo due volte: la sezione
"💶 Costi e Benefici" è stata aggiunta da una sessione su un branch, persa
da un refresh su un altro branch che non la conosceva, recuperata, e poi
persa di nuovo quando il repo è stato riorganizzato su `main` senza
portare quella modifica. Prima di ricostruire il template per QUALSIASI
motivo (restyle, nuova funzionalità, refresh dati, o anche solo perché le
istruzioni del trigger puntano a un branch diverso da quello che hai
usato l'ultima volta):
1. Fai `Artifact action="read"` sull'URL live e leggi per intero
   `<style id="app-style">` e `<script id="app-script">` dell'HTML
   restituito (non solo `edits-data`).
2. Fai un diff testuale con `dashboard/dashboard_template.html` sul
   branch che stai per usare (`git diff`, non a occhio). Se il live ha
   funzionalità/markup che il template locale non ha, il branch è
   indietro — porta prima quelle modifiche (e aggiorna questo documento
   e `jira-extraction-recipe.md` se introducono una nuova convenzione
   dati), poi procedi. Non fidarti del branch che le istruzioni del
   trigger dicono di usare: verifica sempre contro il live.
3. Solo a questo punto applica le tue modifiche e ripubblica.

## Passo 0 — checkout del repo

Clona/aggiorna `rostiandrea/Executive-PM` e lavora dentro `dashboard/`.
Usa un working dir pulito (es. una scratch dir) per i file di estrazione
temporanei (`full_all.jsonl`, ecc.) — non vanno committati, solo
`grandparents.jsonl` viene aggiornato e committato se cambia.

## Passo 1 — leggere l'edits-data live (NON saltare questo passo)

Prima di generare qualunque cosa, leggi l'artifact attualmente pubblicato:

```
Artifact action="read" url="https://claude.ai/code/artifact/8490f5ab-9201-47ed-83e2-09894ac25bcf"
```

Nel file HTML restituito, estrai il contenuto del tag
`<script id="edits-data" type="application/json">...</script>` (è un JSON
`{"items": {...}}` con le modifiche fatte dagli utenti dentro la pagina —
status override, ultimo stato modificato a mano, next steps aggiunti/
completati/eliminati). Salvalo così com'è in un file locale, es.
`current_edits.json`. Se il tag non esiste o è vuoto, usa `{"items": {}}`.

**Questo passo è l'unica cosa che protegge il lavoro fatto dagli utenti
nella dashboard.** Se lo salti, il refresh sovrascrive silenziosamente
qualunque modifica fatta a mano nella pagina.

## Passo 2 — estrazione fresca da Jira

Segui `skills/jira-pmo/references/jira-extraction-recipe.md` per cloudId,
project key (`CR`, `WAV`), JQL di base e field mapping. Per un refresh conviene fare
**una sola query per pagina** con tutti i campi insieme (invece di query
separate per commenti/resolutiondate/gantt), usando questo field set:

```
["summary","status","project","issuetype","customfield_10677",
 "customfield_10290","customfield_10291","customfield_10319",
 "customfield_10311","duedate","customfield_10306","customfield_10307",
 "customfield_10308","customfield_10313","customfield_10289","labels",
 "customfield_10941","updated","issuelinks","resolutiondate",
 "customfield_11007","customfield_11008","comment"]
```

Pagina con `maxResults: 100` finché `pageInfo.hasNextPage` è `false`
(sono ~310 issue, quindi ~4 pagine). Per ogni pagina, proietta subito con
`jq` in JSONL compatto (un oggetto per issue) con questi campi — vedi
`jira-extraction-recipe.md` per il filtro esatto sulla catena "my parent
is" e sul commento `**Stato aggiornato**`:

```
key, project, type, summary, status, statusCategory, priority, phase,
reqlive, release, updated, resolutiondate, plannedStart, plannedDue,
demand, sme, ops, pm, requestor, labels, oldkey, mainprod, involved,
parent, statoComment, cbComment
```

`cbComment` è l'ultimo commento il cui `body` contiene `💶 Costi e
Benefici` (stesso array di commenti già letto per `statoComment`, cercalo
in parallelo — non serve una query separata). Vedi la convenzione
"💶 Costi e Benefici" in `skills/jira-pmo/references/jira-extraction-recipe.md`.
**Non ometterlo**: è dati inseriti dall'utente su Jira, non ricostruibile
se lo perdi nel JSONL — se una riga non ha commenti con questo marker,
`cbComment` è semplicemente assente/`null` per quella issue, non un
errore.

Concatena tutte le pagine in `full_all.jsonl` (una riga per issue, 1 issue
= 1 oggetto JSON).

## Passo 3 — aggiornare la catena Iniziativa (grandparents.jsonl)

`dashboard/grandparents.jsonl` nel repo è la cache nota
`{PRJ/CR key → {key, summary, parent: {INI key, summary}}}`. Per ogni
`parent.key` che compare in `full_all.jsonl` e inizia per `PRJ-` o `CR-`
ma **non** è già presente in `grandparents.jsonl`, risolvilo con una query
`key in (...)` (`fields: ["summary","issuelinks"]`) e aggiungilo al file
(append, non sovrascrivere). Se non ci sono chiavi nuove, non serve fare
nulla in questo passo.

## Passo 4 — build dei dati

```
cd dashboard
python3 build_dashboard_data.py --data-dir <scratch-dir-con-full_all.jsonl-e-grandparents.jsonl>
```

Nota: `build_dashboard_data.py` legge `grandparents.jsonl` dalla
`--data-dir`, quindi copia lì dentro la versione aggiornata del repo prima
di lanciarlo. Produce `dashboard_data_slim.json` nella stessa directory.

## Passo 5 — generare l'HTML finale

```
python3 publish_dashboard.py --data-dir <scratch-dir> \
  --template dashboard_template.html \
  --edits <scratch-dir>/current_edits.json \
  --out dashboard_final.html
```

Questo inietta sia i dati Jira freschi sia gli edits letti al Passo 1 —
nessuna modifica utente viene persa.

## Passo 6 — pubblicare

```
Artifact
  file_path=<scratch-dir>/dashboard_final.html
  url=https://claude.ai/code/artifact/8490f5ab-9201-47ed-83e2-09894ac25bcf
  title="Product Team Management"
  description="Dashboard operativa sulle CR/Wave Jira (Arcese LTL/B2C & Contract Logistics): sommario, scadenze/next steps stile board e Gantt — editabile e persistente."
  favicon="🚦"
  capabilities={"artifact": {}}
```

Se il publish viene rifiutato per "newer version" (qualcuno ha pubblicato
nel frattempo, es. un edit fatto in pagina proprio mentre giri il refresh),
**non forzare**: rileggi l'artifact (Passo 1), riprendi gli edits più
recenti e ripeti dal Passo 5.

## Passo 7 — commit della cache (se `grandparents.jsonl` è cambiato)

Se al Passo 3 hai aggiunto righe nuove, copia il `grandparents.jsonl`
aggiornato su `dashboard/grandparents.jsonl` nel repo, committa e pusha sul
branch di lavoro di questa skill. Non è bloccante: se il push fallisce, il
refresh dei dati e la pubblicazione sono comunque validi — riprova il
commit al giro successivo.

## Schedulazione

Questa procedura gira automaticamente **nei giorni lavorativi alle 8:45 e
alle 13:45, ora italiana**, tramite due Routine (scheduled trigger)
lato Claude. L'orario in UTC va ricalcolato quando cambia l'ora legale in
Italia (CEST = UTC+2 in estate, CET = UTC+1 in inverno) — se le esecuzioni
iniziano a comparire un'ora fuori orario dopo il cambio dell'ora, aggiorna
il `cron_expression` delle due Routine.
