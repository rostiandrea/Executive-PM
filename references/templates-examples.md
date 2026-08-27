# Template ed esempi di analisi

Questo documento raccoglie i template concreti da usare in output e alcuni
esempi realistici applicati. Usa sempre queste strutture quando produci
l'analisi corrispondente, così l'output resta consistente nel tempo.

## 1. Template di estrazione dati Jira

Colonne del template di estrazione (in quest'ordine esatto — riflette
l'export reale da Jira/Excel):

```
Iniziativa | Progetto | Key | Summary | Product Priority | Status |
Project Phase | Requested live date | Release Date | Last update |
What's next | Demand ref. | SME Factory | Operation ref. |
Project manager | Requestor | Etichette | OLD key |
BR Actual Start Date | BR Actual Due Date | BR Planned Start Date |
BR Planned Due Date | HLD Actual Start Date | HLD Actual Due Date |
HLD Planned Start Date | HLD Planned Due Date | Status | Main product
```

Nota: il campo `Status` compare due volte nel template originale
(una dopo `Product Priority`, una prima di `Main product`) — mantienilo
così quando riproduci il template, non è un errore da correggere.

### Esempio reale (riga dati)

```
Iniziativa: INI-222 | New Order In e Followup (include OCR) 2026
Progetto: PRJ-574 | Cognitive AI OCR 2026
Key: WAV-280
Summary: New Order In e Followup - Cognitive AI for DDT - WebApp & EDI
Product Priority: 0
Status: In corso
Project Phase: LLD
Requested live date: (vuoto)
Release Date: 30/11/2026
Last update: (vuoto)
What's next: (vuoto)
Demand ref.: Andrea Rosti
SME Factory: Stefano Gioffrè
Operation ref.: Lucchesi Valerio
Project manager: Alessandro Auteri
Requestor: (vuoto)
Etichette: (vuoto)
OLD key: (vuoto)
BR Actual Start Date ... HLD Planned Due Date: (vuoti)
Status: In corso
Main product: LTL / B2C
```

Interpretazione dei campi principali:

- **Iniziativa** / **Progetto**: riportano `KEY | Titolo` dell'oggetto
  padre a livello Iniziativa e Progetto/CR (vedi `jira-data-model.md`).
- **Key**: la key dell'oggetto corrente (in questo caso una Wave, WAV-280).
- **Product Priority**: valore numerico usato per l'ordinamento nella
  lista di monitoraggio (crescente = priorità più alta prima). è un numero che va da 1 a 99
- **Main product**: il valore da controllare per il filtro di perimetro
  (`LTL / B2C` o `Contract Logistics`).

## 2. Lista di monitoraggio CR/Wave (output richiesto)

Quando viene chiesto il monitoraggio periodico, produci una tabella con
le colonne del template sopra, contenente solo oggetti **CR** o **WAV**
con Main Product in `LTL / B2C` o `Contract Logistics`,
ordinata **crescente per Product Priority**. Non estrarre le voci con stato "Annullato"

Esempio di riga in output (formato tabella):

| Product Priority | Key | Summary | Status | Project Phase | Release Date | Project manager | Main product |
|---|---|---|---|---|---|---|---|
| 0 | WAV-280 | New Order In e Followup - Cognitive AI for DDT - WebApp & EDI | In corso | LLD | 30/11/2026 | Alessandro Auteri | LTL / B2C |

Se il set di colonne è molto ampio, puoi mostrare in tabella solo le
colonne più operative (come sopra) e riportare le rimanenti solo se
richieste esplicitamente o rilevanti per un punto di attenzione (es. una
data BR/HLD in ritardo).

## 3. Daily PM Brief

Struttura fissa da usare per il briefing giornaliero:

```
Daily PM Brief

🔴 Critical / Overdue
[Elementi che richiedono attenzione immediata]

🟠 At Risk
[Elementi dove consegna o scadenza sono potenzialmente a rischio]

🟡 Due Soon
[Attività con scadenze imminenti]

🔵 Today
[Azioni o impegni che richiedono attenzione oggi]

⚪ Open Points
[Questioni o decisioni importanti non ancora risolte]

🎯 Recommended Focus
[Massimo 3–5 azioni su cui l'utente dovrebbe concentrarsi per prime]
```

Esempio (estratto):

```
🔴 Critical / Overdue
- CR-1198 — Scaduta il 20/08, nessun aggiornamento di stato. Owner: M. Bianchi.

🟠 At Risk
- WAV-280 — Due 30/11. Fase LLD non ancora completata, nessuna stima
  aggiornata di consegna.

🎯 Recommended Focus
1. Sollecitare aggiornamento su CR-1198 (owner M. Bianchi).
2. Verificare stato fase LLD su WAV-280.
```

## 4. Nota di escalation

Formato: **Issue → Impact → Required action**

```
Escalation recommended: [problema]. This puts [scadenza/rilascio] at
risk. [Azione richiesta] is required by [data].
```

Esempio:

```
Escalation recommended: Development is blocked by the missing business
requirement. This puts the 15/09 release at risk. Business confirmation
is required by 30/08.
```

## 5. Comunicazione verso stakeholder

Formato: **facts → impact → required action → deadline**

Esempio:

```
The activity is currently overdue and is impacting the planned delivery.
Please provide an updated completion date by tomorrow.
```

## 6. Decision support

Quando viene chiesta un'opinione o una raccomandazione, struttura la
risposta così:

```
Situation: [contesto sintetico]
Key considerations: [fattori rilevanti]
Recommendation: [raccomandazione esplicita]
Risks / implications: [rischi o conseguenze]
Next action: [prossimo passo concreto]
```

## 7. Jira mismatch (riunione vs Jira)

Esempio:

```
Jira mismatch: During today's meeting, delivery was agreed for 05/09,
while Jira currently shows 29/08.
```

## 8. Segnali di dato mancante

Non inventare mai un valore mancante. Usa sempre una di queste due
etichette:

- `Not available` — il dato non è disponibile nella fonte consultata.
- `TBD` — il dato è atteso ma non è ancora stato definito/comunicato.
