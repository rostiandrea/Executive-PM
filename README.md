# Executive-PM

Repository di supporto Claude per un assistente Executive Project
Manager / PMO: trasforma dati di progetto (estrazioni Jira, note di
riunione, aggiornamenti di stato) in priorità, decisioni, azioni, owner,
scadenze, rischi e follow-up, con il tono e la disciplina di un Project
Manager senior.

## Mappa del repo

- [`CLAUDE.md`](./CLAUDE.md) — **istruzioni permanenti**, sempre attive:
  identità, personalità e principi operativi dell'agente (non è una
  skill a trigger: si applica ad ogni interazione).
- `skills/` — le skill a trigger, caricate solo quando la richiesta è
  pertinente:
  - [`skills/jira-pmo/`](./skills/jira-pmo/SKILL.md) — interpretazione
    della gerarchia Jira (Iniziativa/Progetto/CR/Wave), filtro di
    perimetro (`LTL / B2C`, `Contract Logistics`), ricetta tecnica di
    estrazione via connettore Atlassian, template di estrazione e
    monitoraggio.
  - [`skills/steering-committee/`](./skills/steering-committee/SKILL.md)
    — preparazione del deck PowerPoint periodico di Steering Committee
    (Summary, Focus Tavoli, Iniziative in corso), a partire dai dati
    Jira ottenuti tramite `jira-pmo`.
  - [`skills/creaasupport/`](./skills/creaasupport/SKILL.md) — apertura
    autonoma di un ticket sul portale SU&GO Arcese
    (aplatform.arcese.com/support).
  - [`skills/contract-logistics-it-quotation/`](./skills/contract-logistics-it-quotation/SKILL.md)
    — compilazione del file Excel di quotazione costi IT ("IT Costs")
    per un tender/RFQ di Contract Logistics Arcese.
  - [`skills/stileex/`](./skills/stileex/SKILL.md) — stile di
    comunicazione "StileEX" (executive, diretto, pragmatico) per email e
    testi professionali.
- [`dashboard/`](./dashboard/README.md) — webapp/artifact "Product Team
  Management": dashboard operativa che si rigenera automaticamente da
  Jira (Routine schedulate, vedi `dashboard/README.md` per la procedura
  di refresh).

## Come si integrano

`CLAUDE.md` definisce sempre *come* comportarsi. Le skill in `skills/`
si attivano in base al task e forniscono *cosa sapere* per eseguirlo
(dati Jira, formati di output). `dashboard/` è un'applicazione a sé che
consuma gli stessi dati Jira (via `jira-pmo`) ma vive fuori dal
perimetro delle skill, con la propria documentazione operativa.
