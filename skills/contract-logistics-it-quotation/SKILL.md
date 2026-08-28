---
name: contract-logistics-it-quotation
description: "Compila il file Excel di quotazione costi IT (foglio 'IT Costs') per una gara/tender di Contract Logistics Arcese, a partire dalla richiesta ricevuta via mail da Solution Design/Pricing (es. Galbiati Selene, Giupponi Stefano, Arrigoni Martina) e dal file Excel base allegato. Usare quando l'utente chiede di preparare/completare una quotazione IT per un tender, un RFQ, una gara di magazzino/logistica, o cita un treno mail tipo 'Quotazione IT - Nome Cliente' o 'RFQ Nome Cliente Sito'."
---

# Quotazione IT per tender di Contract Logistics (Arcese)

## Quando usare questa skill

L'utente (T&T Demand Manager / Solution Design) riceve via mail da un referente Pricing &
Solution Design (es. Selene Galbiati, Stefano Giupponi) una richiesta di stima costi IT per
un tender di Contract Logistics. La mail contiene una descrizione testuale del sito/cliente e
in allegato un file Excel con il foglio "IT Costs" parzialmente compilato (solo i dati base:
location, mq, FTE, eventuali flag Yes/No). Il compito è restituire lo stesso file completato
con tutti i costi, mantenendo intatte le formule del template così che i **totali si
ricalcolino automaticamente e tornino**.

## Procedura

1. **Trova la mail/il treno mail rilevante** (Outlook). Di solito il soggetto è del tipo
   "Quotazione IT - Nome Cliente" o "RFQ Nome Cliente Sito". Leggi TUTTI i messaggi del thread in
   ordine cronologico, non solo il primo: spesso le richieste iniziali vengono precisate o
   corrette in risposte successive (es. "niente EDI, solo la VPN", "teniamo il pacchetto
   base per il momento").
2. **Recupera il file Excel allegato** al primo messaggio (foglio "IT Costs") ed estrai i dati
   base già presenti: location, mq magazzino/ufficio, WMS Arcese Yes/No, WMS Customer Yes/No,
   FTE (Blue Collar, White Collar, Support, Contract Manager), eventuali interfacce/VPN/cabling
   già indicati.
3. **Parti dal template di riferimento** in `reference/TEMPLATE_QUOTATION.xlsx` (stesso file che
   Andrea Rosti usa come esempio "già completato"): copialo e modifica solo le celle di input
   (quantità in colonna C, i flag Yes/No, le celle di testo in "Sizing"), lasciando invariate le
   formule delle colonne D/E/F/G e la formula di totale in F66/G66 (`=+SUM(F6:F64)` /
   `=+SUM(G6:G64)`). Non scrivere mai un totale a mano.
4. **Applica le regole di pricing** (vedi tabella sotto).
5. **Ricalcola con LibreOffice** (`scripts/recalc.py` della skill `xlsx`) e verifica
   `total_errors: 0` prima di consegnare il file.
6. **Segnala sempre le assunzioni fatte** (in chat/mail, non nel foglio): dati non specificati
   dal cliente (es. cablaggio, mq ufficio), il criterio usato per stampanti/scanner, eventuali
   punti ancora da confermare dal thread mail (es. "Selene deve risentire un collega lunedì").

## Regole di pricing (IT Costs)

### 1. WMS Activation (righe 6-18)
- Se **WMS Arcese = Yes** (il cliente userà il WMS Arcese, non un WMS proprio):
  - Startup WMS Arcese = **1.500 €** (cella F6, valore fisso, non formula legata a C6).
  - Vanno indicate le interfacce da prevedere: ogni interfaccia = **900 €** di startup.
    Se il numero di interfacce non è indicato da nessuna parte nella mail o nel file base,
    usa **5** come default.
  - Metti il conteggio interfacce in C10 (o nella riga Easy/Medium/Hard più coerente con la
    richiesta) e il relativo costo in F10 = numero_interfacce × 900.
- Se **WMS Arcese = No** (il cliente vuole usare un proprio WMS, come nel caso Ford Colonia):
  tutta la sezione WMS Activation/Integration/Reporting/Customization resta a **0** — non si
  applica la regola sopra. Metti C7 "WMS Customer" = Yes.

### 2. Connectivity (righe 32-35)
- Pacchetto **Small**: Startup = **3.000 €** (F32), Running annuo = **6.000 €** (G32). Sono
  valori di pacchetto fissi (non moltiplicati per quantità).
- Usa Small come default per siti piccoli/nuovi salvo indicazioni diverse nella mail
  (es. necessità esplicita di banda/interfacce EDI maggiori → valutare Medium/Large, non
  documentato in dettaglio: chiedere o usare buon senso e segnalarlo come assunzione).
- Il flag VPN (C35, Yes/No) va impostato in base a quanto scritto nella mail, ma **non ha un
  costo proprio aggiuntivo**: è incluso nel pacchetto di Connectivity scelto.

### 3. Network Device (righe 37-39)
- Pacchetto **Medium**: Startup = **15.000 €** (F38), Running annuo = **1.000 €** (G38).
  Valori di pacchetto fissi. È il default osservato sia per siti grandi (7.500 mq) sia piccoli
  (5.500 mq) — dipende più dalla copertura di rete del magazzino che dal numero di persone.
  Usa Medium come default; scegli Small/Large solo se la mail dà indicazioni esplicite sulla
  dimensione dell'infrastruttura di rete richiesta.

### 4. End-User Device (righe 41-56)
Tutte le formule di riga (F/G) restano quelle del template: si tocca solo la quantità in
colonna C (o si lascia la formula già presente per le righe derivate).

| Voce | Regola |
|---|---|
| Laptop standard (C41) | 1 per ogni White Collar + Contract Manager + Support function |
| Desktop (C43) | almeno 1 ogni 5 Blue Collar (arrotondato per eccesso) |
| Monitor (C44) | formula già presente `=C43+C41` — non toccare |
| Docking e accessori (C45) | formula già presente `=C44` — non toccare |
| MS Office license (C55) | formula già presente `=C44` — non toccare |
| Parallels license (C56) | formula già presente `=C55` — non toccare |
| Multi-functional/Laser/Thermal/Mobile thermal printer, Radio-frequency scanner, barcode scanner, TV monitor | **Non c'è una formula fissa**: proponi un numero proporzionato al personale richiesto. Criterio usato finora: 1 stampante multifunzione b/n per ufficio/White Collar; 1 stampante termica fissa ("Zebra") e 1 radio-scanner ("Palmare") per ogni Blue Collar operativo (pacchetto "base" per operatore di magazzino: PC/Desktop + Monitor + Palmare + Zebra + Stampante); stampante mobile/laser aggiuntiva solo per siti più grandi o se richiesta esplicitamente. Segnala sempre che è una proposta, non un dato ricevuto dal cliente. |

### 5. Cyber & Effort (righe 58-62)
- **Email security (C58)** e **Formazione cybersecurity (C59)**: la quantità **non è un
  numero fisso**, deve essere pari al numero di utenti dispositivo, cioè la stessa quantità
  già calcolata per Monitor/Docking/MS Office/Parallels. Metti una formula, non un numero:
  `C58 = =C44` e `C59 = =C44` (dove C44 = Desktop + Laptop, riga "Number of Monitor"). I costi
  unitari restano quelli standard: 180 €/anno per Email security (formula G58 = E58×C58),
  132 €/anno per la formazione (formula G59 = E59×C59).
- Effort Internal: 4 giornate, 300 €/giornata (formula F61 = C61×D61) — valore di pacchetto
  standard, non scalato sugli utenti salvo diversa indicazione esplicita nella mail.
- Effort External: 4 giornate, 500 €/giornata (formula F62 = C62×D62) — idem.

### 6. Totali
Non scrivere mai un numero fisso nei totali. F66 = `=+SUM(F6:F64)`, G66 = `=+SUM(G6:G64)`
devono restare invariati: se le regole sopra sono applicate correttamente sulle celle di
input, i totali "tornano" automaticamente.

## File di riferimento

- `reference/TEMPLATE_QUOTATION.xlsx`: template con tutte le formule, i formati e i prezzi
  unitari standard già impostati. Usalo sempre come base di partenza per una nuova
  quotazione (copialo, non ripartire da un foglio vuoto), così formule, formattazione e
  data validation (liste Yes/No) restano intatte.

## Note operative

- Usa sempre la skill `xlsx` per l'editing (apre/salva con `openpyxl`, poi `recalc.py` per
  ricalcolare le formule con LibreOffice — obbligatorio prima di consegnare il file).
- Nomina il file di output in modo chiaro, es. `IT Quotation - Nome Cliente Sito.xlsx`.
- Se dal thread mail emergono ancora punti aperti (es. "risentiamo un collega per conferma"),
  non bloccarti: consegna comunque una prima versione con le assunzioni più ragionevoli e
  segnala chiaramente cosa resta da confermare.
