# Steering Committee PowerPoint

How to turn current Jira data into an updated Steering Committee deck that
looks exactly like `assets/steering-committee/TemplateSteerco.pptx` — the
brand-compliant template provided by the user (colors and fonts already
match `assets/steering-committee/brand-tokens.json`, extracted from the
Arcese Corporate Design Manual).

Trigger this workflow on requests like "prepara il PowerPoint dello
steering committee", "aggiorna la presentazione dello steerco", "genera
le slide per lo Steering Committee TMS/SIMA".

## Golden rule

**Section 3 (Iniziative, slides 9-12) must change as little as possible
graphically.** Only the table *contents* (cell text and the RAG cell
fill) may change — never touch fonts, table style, column widths, row
height, borders, header row fill, or slide layout in that section. When in
doubt, prefer leaving a graphical property untouched over "improving" it.

## Template structure (12 slides)

| # | Purpose | What changes on refresh |
|---|---|---|
| 1 | Cover — "LTL e Contract Logistics / Steering Committee / <Month Year>" | Update month/year to the meeting date |
| 2 | Agenda overview (all 3 items same color/weight) | Usually static |
| 3 | Section divider — **Summary** highlighted, other two dimmed to `bg1` (white) | Static (divider mechanism, see below) |
| 4 | **Summary**: 2 update bullets, 3 KPI stat callouts, 1 native stacked bar chart | Fully data-driven, see below |
| 5 | Section divider — **Focus on Tavoli TMS** highlighted | Static |
| 6 | **Focus Tavoli SIMA** table (PRIO / Codice / Tavolo / Descrizione / Stato / Last Updates / Next Step / Live) | Fully data-driven, see below |
| 7 | **Focus Tavoli SIMA - Gantt** (week-by-week swimlanes + "Oggi" marker) | Semi-manual, see limitation below |
| 8 | Section divider — **Iniziative** highlighted | Static |
| 9-11 | **Iniziative in corso** tables (ID / TITLE / RAG / % / PHASE / RELEASE / Ultimo Stato / Prossimi Passi), paginated ~7 rows/slide | Fully data-driven, minimal-touch (golden rule) |
| 12 | **Suspended Initiatives** — same table schema, filtered to suspended items | Fully data-driven, minimal-touch (golden rule) |

### Section divider mechanism (slides 2, 3, 5, 8)

Each of the three agenda items ("Summary", "Focus on Tavoli TMS",
"Iniziative") is its own text run. The *current* section's run has no
explicit fill (inherits the theme's dark/red text color); the other two
runs have `<a:solidFill><a:schemeClr val="bg1"/></a:solidFill>` (white),
which makes them blend into the background and read as "dimmed". To move
the highlight, only toggle that `bg1` fill on/off per run — never
duplicate or restyle the shapes.

### Slide 4 — Summary

Shapes (by name, from `ppt/slides/slide4.xml`):
- `Rectangle 15`: two bullet lines under "Principali aggiornamenti" — replace with the 1-2 top headline updates for the period.
- `Rectangle 3` / `Rectangle 8` / `Rectangle 17`: KPI **labels** ("Numero di nuove attività (CR/WAV)", "Numero di attività completate negli ultimi 30 gg (CR/WAV)", "Numero di attività in rilascio nei prossimi 30 gg (CR/WAV)").
- `Rectangle 14` / `Rectangle 12` / `Rectangle 19`: the corresponding KPI **numbers** (separate shapes from their labels — update only the number shape's text).
- A native embedded chart (`ppt/charts/chart1.xml`, linked via `rId3`) — a stacked bar with categories `0 - Pipeline`, `1 - In Corso`, `2 - Completate`, `3 - Annullate/Sospese` and series `BR, HLD, LLD, Development, Test, Live, Live ultimi 30 giorni`. Update with `chart.replace_data(CategoryChartData)` (python-pptx) — never delete/recreate the chart part, or the brand colors/legend formatting is lost.

KPI numbers and the chart categories/series counts should come from the
same CR/Wave extraction described in `jira-extraction-recipe.md` and
`jira-data-model.md`: bucket every in-scope CR/Wave by its current status
into the 4 pipeline stages, and additionally split "Live" into
"Live" vs "Live ultimi 30 giorni" (went live in the last 30 days).

### Slide 6 — Focus Tavoli SIMA

One row per Wave/CR belonging to the Tavoli SIMA workstream, sorted by
`PRIO` ascending (same "Product Priority ascending" convention as
`templates-examples.md`). Columns map directly to the extraction template:

| Table column | Source |
|---|---|
| PRIO | Product Priority |
| Codice | Wave/CR key (e.g. `WAV328`) |
| Tavolo | the SIMA "tavolo" / workstream name |
| Descrizione | Summary/description |
| Stato | current phase/status label |
| Last Updates | latest `**Stato aggiornato**` comment (see extraction recipe) |
| Next Step | Next Steps from the same comment convention, keep the `@Owner` tags inline |
| Live | go-live date, or `tbd` if not committed |

### Slide 7 — Gantt (semi-manual)

This slide is not a data table but 55 individually positioned shapes
(bar segments per phase per week) plus connector lines (the "Oggi" —
"today" — vertical marker) laid over a week-header table. Faithfully
regenerating it from Jira dates requires computing each phase's start/end
week and mapping it to the x-position of that week's table column.

For now: update the "Oggi <date>" label and reposition the "Oggi"
connector line to the current week's column x-coordinate (read it from
the week-header row of the table in that slide); leave the phase bars as
in the template unless the user explicitly asks for a full Gantt rebuild,
in which case flag it as a manual/careful pass rather than a scripted one.

### Slides 9-12 — Iniziative (golden-rule section)

Same 8-column schema on every slide: `ID, TITLE, RAG, %, PHASE, RELEASE,
Ultimo Stato, Prossimi Passi`. `RAG` carries **no text** — only a cell
background fill from `assets/steering-committee/brand-tokens.json` →
`rag_status_fill_colors` (green/yellow/red). Everything else is plain
text in the existing run/paragraph formatting.

- Slides 9-11: "Iniziative in corso" — all non-suspended in-scope
  initiatives, ~7 rows/slide (paginate in Jira sort order, same order as
  the CR/Wave monitoring list).
- Slide 12: "Suspended Initiatives" — items whose status is suspended/on
  hold, same 8 columns (RELEASE is typically blank for suspended items).

When the initiative count differs from the template's row count, clone
the last data row's `<a:tr>` XML (deep copy) to add rows, or drop trailing
rows to remove them — never touch header row XML, column widths, or the
`<a:tblPr>`/style reference.

## Data model reminder

Reuse the existing PM skill machinery rather than re-deriving it:
- `references/jira-data-model.md` for the Iniziativa → Progetto/CR → Wave/CR hierarchy and the `LTL / B2C` / `Contract Logistics` product filter.
- `references/jira-extraction-recipe.md` for the actual JQL/cloudId/custom-field-ID recipe, including the `**Stato aggiornato**` comment convention that supplies `Ultimo stato` / `Next Steps`.
- `references/templates-examples.md` for the extraction template columns and the "sort ascending by Product Priority" convention — reuse it as-is for slides 6 and 9-12.

## Workflow to produce the deck

1. Run the Jira extraction (per `jira-extraction-recipe.md`), scoped to
   the CRs/Waves/Iniziative relevant to this steering committee (TMS/SIMA
   workstream + tracked initiatives).
2. Shape the extraction into the per-slide data needed above (KPIs/chart
   buckets for slide 4, sorted Tavolo rows for slide 6, paginated
   Iniziative rows for slides 9-12, suspended items for slide 12).
3. Copy `assets/steering-committee/TemplateSteerco.pptx` to the output
   path — never edit the template in place.
4. Use `scripts/build_steerco_pptx.py` (python-pptx) to fill in the copy:
   it exposes one function per slide (`update_cover`, `update_summary`,
   `update_focus_table`, `update_gantt_today_marker`,
   `update_iniziative_tables`) so each section can be filled
   independently and the Iniziative-section functions only ever touch
   cell text/fill, per the golden rule.
5. Validate: `python <pptx-skill>/scripts/office/validate.py output.pptx
   --original assets/steering-committee/TemplateSteerco.pptx`, then dump
   with `markitdown output.pptx` and check every row/number landed and no
   `TODO`/placeholder text remains.
6. Visually spot-check the rendered slides (see the `pptx` skill's
   "Converting to Images" section) before delivering, especially slide 4's
   chart and slide 7's Gantt if it was touched.
7. Never invent numbers — if a field is missing from Jira, write `TBD`
   exactly as the template already does in several cells, rather than
   guessing.
