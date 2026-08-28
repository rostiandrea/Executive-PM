# Template ed esempi di analisi — dati Jira

Questo documento raccoglie i template concreti da usare quando si
estraggono o monitorano dati Jira. Usa sempre queste strutture, così
l'output resta consistente nel tempo.

I template generici non specifici a Jira (Daily PM Brief, escalation,
comunicazione stakeholder, decision support) sono in `CLAUDE.md` alla
radice del repo.

## 1. Template di estrazione dati Jira

Colonne del template di estrazione (in quest'ordine esatto — riflette
l'export reale da Jira/Excel):

```
Iniziativa | Progetto | Key | Summary | Product Priority | Status |
Project Phase | Requested live date | Release Date | Ultimo stato |
Next Steps | Demand ref. | SME Factory | Operation ref. |
Project manager | Requestor | Etichette | OLD key |
BR Actual Start Date | BR Actual Due Date | BR Planned Start Date |
BR Planned Due Date | HLD Actual Start Date | HLD Actual Due Date |
HLD Planned Start Date | HLD Planned Due Date | Status | Main product
```

Nota: il campo `Status` compare due volte nel template originale
(una dopo `Product Priority`, una prima di `Main product`) — mantienilo
così quando riproduci il template, non è un errore da correggere.

Nota sulle colonne `Ultimo stato` / `Next Steps`: nel template Excel
originale erano `Last update` / `What's next`, due campi dell'app
Structure non raggiungibili dal connettore Atlassian (vedi
`jira-extraction-recipe.md`). Da agosto 2026 queste due colonne **non
vengono più lasciate `Not available`**: sono popolate leggendo l'ultimo
commento Jira con marker `**Stato aggiornato**` sulla CR/Wave (lo stesso
commento che l'agente scrive/aggiorna a partire dalle minute fornite
dall'utente — vedi `jira-extraction-recipe.md` § Commenti). Se una
CR/Wave non ha ancora un commento con quel marker, riporta comunque
`Not available` per entrambe le colonne.

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
Ultimo stato: Not available (nessun commento con marker "Stato aggiornato" su questa issue)
Next Steps: Not available
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

| Product Priority | Key | Summary | Status | Project Phase | Release Date | Ultimo stato | Next Steps | Project manager | Main product |
|---|---|---|---|---|---|---|---|---|---|
| 0 | WAV-280 | New Order In e Followup - Cognitive AI for DDT - WebApp & EDI | In corso | LLD | 30/11/2026 | Not available | Not available | Alessandro Auteri | LTL / B2C |

Esempio con commento "Stato aggiornato" presente (CR-438):

| Product Priority | Key | Summary | Status | Ultimo stato | Next Steps | Main product |
|---|---|---|---|---|---|---|
| — | CR-438 | (summary) | — | In validazione LT | Validazione documento approval (Owner LT - Due date 10/9) | LTL / B2C |

Se il set di colonne è molto ampio, puoi mostrare in tabella solo le
colonne più operative (come sopra) e riportare le rimanenti solo se
richieste esplicitamente o rilevanti per un punto di attenzione (es. una
data BR/HLD in ritardo).

## 3. Jira mismatch (riunione vs Jira)

Esempio:

```
Jira mismatch: During today's meeting, delivery was agreed for 05/09,
while Jira currently shows 29/08.
```

## 4. Segnali di dato mancante

Non inventare mai un valore mancante. Usa sempre una di queste due
etichette (vedi anche `CLAUDE.md` § Data Integrity):

- `Not available` — il dato non è disponibile nella fonte consultata.
- `TBD` — il dato è atteso ma non è ancora stato definito/comunicato.
