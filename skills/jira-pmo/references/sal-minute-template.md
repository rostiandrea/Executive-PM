# Minuta SAL interno di Prodotto (formato email)

Quando l'utente chiede il recap/la minuta di un SAL interno di Prodotto
(LTL & Contract Logistics) **in formato mail**, usa esattamente questa
struttura. È il formato realmente inviato da Andrea Rosti al team
(thread ricorrente `LTL&CL - PRODUCT TEAM PLANNING AND TRACKING`) e
validato come template di riferimento il 02/09/2026.

Non è lo stesso output della lista di monitoraggio o del Daily PM Brief
(vedi `templates-examples.md` e `CLAUDE.md`): qui niente tabelle, niente
emoji, niente riepilogo KPI — è una mail discorsiva, breve per punto,
pensata per essere letta in 2 minuti da tutto il team di prodotto.

## Oggetto

Rispondi mantenendo il thread della ricorrenza settimanale esistente:

```
Re: LTL&CL - PRODUCT TEAM PLANNING AND TRACKING
```

Non aprire un nuovo oggetto/thread per un recap periodico.

## Struttura del corpo

```
Ciao a tutti,
di seguito il recap del SAL di oggi, diviso per iniziativa/CR/Wave.

[KEY] – [Nome esteso dell'oggetto Jira]
- [punto elenco con l'update sintetico: fatto, owner tra parentesi, date]
- [secondo punto se necessario]

[KEY] – [Nome esteso]
- ...

(una sezione per ogni CR/Wave/Progetto toccato nel SAL, nell'ordine in
cui sono stati discussi)

Temi aperti senza un ID Jira:
- [tema] — [contesto sintetico, eventuali owner/prossimo passo]

Un saluto,
Andrea
```

## Regole di stile (osservate dall'esempio reale)

- **Ogni sezione inizia con `KEY – Nome` in grassetto**, mai il solo
  KEY: es. `WAV-416 – Adozione DeCA - Arcese Spagna Wave 1`, non
  `WAV-416`. Recupera il nome esatto da Jira (`summary`), non
  parafrasarlo — vedi `jira-extraction-recipe.md`.
- **Quando un item non ha novità rispetto al giro precedente**, scrivilo
  esplicitamente — non ometterlo. Formula standard:
  `Confermata [stato/situazione]. Nessun elemento nuovo.`
  Questo tiene visibile a tutto il team che l'item è stato comunque
  monitorato, anche se fermo.
- **Punti elenco brevi e discorsivi**: fatti, owner tra parentesi (es.
  `Owner Salvini`), date nel formato `gg/m` (es. `7/9`, non `07/09/2026`).
  Niente formalismi ("si comunica che", "si segnala quanto segue").
- **Temi senza un ID Jira chiaro vanno in una sezione dedicata in
  fondo**, mai forzati dentro un CR/Wave esistente solo perché
  tematicamente vicini. Se durante la raccolta emergono dubbi su quale
  CR/Wave corrisponda a un argomento discusso, verifica su Jira (vedi
  `jira-extraction-recipe.md`) prima di scrivere la mail — se resta
  incerto, meglio lasciarlo tra i "temi senza ID" che assegnargli un
  codice sbagliato.
- **Nessuna emoji, nessuna tabella** nel corpo della mail (a differenza
  dell'output a schermo/chat, dove tabelle ed emoji di stato restano
  appropriate — vedi `templates-examples.md` § Lista di monitoraggio).
- Chiusura sempre con `Un saluto,` seguito dal nome — mantieni la firma
  aziendale esistente se stai rispondendo in un thread già firmato.

## Collegamento con l'aggiornamento Jira

La minuta è tipicamente il momento in cui emergono aggiornamenti di
stato/next steps da riportare su Jira. Dopo aver prodotto la mail:

1. Proponi all'utente, **per ciascun CR/Wave/Progetto citato**, se e come
   aggiornare il commento `**Stato aggiornato**` corrispondente — sempre
   indicando **KEY + Nome esteso** insieme, mai il solo KEY (vedi
   `jira-extraction-recipe.md` § Convenzione "Stato aggiornato").
2. Non scrivere nulla su Jira finché l'utente non conferma quali
   aggiornamenti applicare.
3. I "temi senza un ID Jira" restano tali nella proposta di aggiornamento
   — non inventare un CR/Wave a cui agganciarli.
