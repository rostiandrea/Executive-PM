# Executive-PM

Skill Claude per un assistente Executive Project Manager / PMO: trasforma
dati di progetto (estrazioni Jira, note di riunione, aggiornamenti di
stato) in priorità, decisioni, azioni, owner, scadenze, rischi e
follow-up, con il tono e la disciplina di un Project Manager senior.

## Contenuto

- [`SKILL.md`](./SKILL.md) — punto di ingresso della skill: quando si
  attiva e come usare i file di riferimento.
- [`references/agent-behavior.md`](./references/agent-behavior.md) —
  identità, personalità e principi operativi dell'agente.
- [`references/jira-data-model.md`](./references/jira-data-model.md) —
  come interpretare la gerarchia degli oggetti Jira (Iniziativa, Progetto,
  CR, Wave) e il filtro di perimetro (`LTL / B2C`, `Contract Logistics`).
- [`references/templates-examples.md`](./references/templates-examples.md)
  — template di estrazione dati ed esempi concreti delle analisi
  ricorrenti (monitoraggio CR/Wave, Daily PM Brief, escalation, ecc.).
- [`references/jira-extraction-recipe.md`](./references/jira-extraction-recipe.md)
  — ricetta tecnica verificata per l'estrazione via connettore Atlassian:
  cloudId, project key, mapping dei custom field, JQL di base, risoluzione
  della catena Iniziativa/Progetto, limiti noti del connettore (campi
  Structure, testo checklist) e lettura/scrittura dei commenti Jira.
