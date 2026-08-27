#!/usr/bin/env python3
"""
Build dashboard_data_slim.json from the raw Jira extraction files.

Expects, in --data-dir (default: current directory):
  full_all.jsonl     one JSON object per line, one per CR/Wave, with the fields
                      listed in ../references/jira-extraction-recipe.md
                      (key, project, type, summary, status, statusCategory,
                      priority, phase, reqlive, release, resolutiondate,
                      plannedStart, plannedDue, demand, sme, ops, pm,
                      requestor, labels, oldkey, mainprod, involved, parent,
                      statoComment)
  grandparents.jsonl one JSON object per line: {"key": "PRJ-xxx"/"CR-xxx",
                      "summary": "...", "parent": {"key": "INI-xxx", "summary": "..."} | null}
                      — resolves the Iniziativa for every Progetto/CR that is
                      itself the parent of a CR/Wave.

Writes dashboard_data_slim.json in --data-dir.

See references/jira-extraction-recipe.md in this repo for how to produce
full_all.jsonl and grandparents.jsonl from Jira, and dashboard-refresh-procedure.md
for the end-to-end refresh + publish flow this script is one step of.
"""
import json, re, datetime, argparse, os

NEXT_STEP_RE = re.compile(
    r'^(?P<text>.*?)\s*\(\s*owner\s+(?P<owner>[^-)]+?)\s*(?:-\s*)?(?:due date|entro)\s+(?P<due>[^)]+?)\s*\)\s*$',
    re.IGNORECASE
)

def parse_date(raw, default_year):
    raw = raw.strip().lower()
    if raw in ("tbd", "", "n/a", "na"):
        return None
    m = re.match(r'^(\d{1,2})[/\-](\d{1,2})(?:[/\-](\d{2,4}))?$', raw)
    if not m:
        return None
    d, mo, y = m.groups()
    y = int(y) if y else default_year
    if y < 100:
        y += 2000
    try:
        return datetime.date(y, int(mo), int(d)).isoformat()
    except ValueError:
        return None

def parse_stato_comment(body, default_year):
    if not body:
        return None, []
    stato_m = re.search(r'\*\*Stato:\*\*\s*(.+?)(?:\n\n|\n\*\*Next steps|\Z)', body, re.DOTALL)
    stato = stato_m.group(1).strip() if stato_m else None
    steps = []
    steps_section = re.search(r'\*\*Next steps:\*\*\s*(.+?)\Z', body, re.DOTALL)
    if steps_section:
        for line in steps_section.group(1).splitlines():
            line = line.strip().lstrip("-*").strip()
            if not line:
                continue
            m = NEXT_STEP_RE.match(line)
            if m:
                due_raw = m.group("due").strip()
                steps.append({
                    "text": m.group("text").strip(),
                    "owner": m.group("owner").strip(),
                    "dueRaw": due_raw,
                    "dueISO": parse_date(due_raw, default_year),
                    "done": False,
                })
            else:
                steps.append({"text": line, "owner": None, "dueRaw": None, "dueISO": None, "done": False})
    return stato, steps

def fmt_kv(key, summary):
    if not key:
        return None
    return f"{key} | {summary}" if summary else key

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=".")
    args = ap.parse_args()
    d = args.data_dir
    today = datetime.date.today()

    base = {}
    with open(os.path.join(d, "full_all.jsonl")) as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                base[row["key"]] = row

    gp = {}
    with open(os.path.join(d, "grandparents.jsonl")) as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                gp[row["key"]] = row.get("parent")

    def resolve_chain(row):
        parent = row.get("parent")
        if not parent or not parent.get("key"):
            return None, None
        ptype = parent["key"].split("-")[0]
        if ptype == "INI":
            return fmt_kv(parent["key"], parent["summary"]), None
        progetto = fmt_kv(parent["key"], parent["summary"])
        grandparent = gp.get(parent["key"])
        iniziativa = fmt_kv(grandparent["key"], grandparent["summary"]) if grandparent and grandparent.get("key") else None
        return iniziativa, progetto

    rows = []
    next_step_counter = 0
    for key, row in base.items():
        iniziativa, progetto = resolve_chain(row)
        stato_comment = row.get("statoComment")
        ultimo_stato, next_steps = (None, [])
        if stato_comment:
            ultimo_stato, next_steps = parse_stato_comment(stato_comment.get("body"), today.year)
        for ns in next_steps:
            next_step_counter += 1
            ns["id"] = f"ns-{next_step_counter}"
            ns["issueKey"] = key

        priority = row.get("priority")
        priority = priority if priority not in (None, "NA") else None

        resdate_raw = row.get("resolutiondate")
        resdate_iso = resdate_raw[:10] if resdate_raw else None

        rows.append({
            "key": key,
            "url": f"https://arcese.atlassian.net/browse/{key}",
            "type": row["project"],
            "resolutionDate": resdate_iso,
            "plannedStart": row.get("plannedStart"),
            "plannedDue": row.get("plannedDue"),
            "iniziativa": iniziativa,
            "progetto": progetto,
            "summary": row["summary"],
            "priority": priority,
            "status": row.get("status"),
            "statusCategory": row.get("statusCategory"),
            "projectPhase": row.get("phase") if row.get("phase") != "NA" else None,
            "requestedLiveDate": row.get("reqlive") if row.get("reqlive") != "NA" else None,
            "releaseDate": row.get("release") if row.get("release") != "NA" else None,
            "demand": row.get("demand") if row.get("demand") != "NA" else None,
            "sme": row.get("sme") if row.get("sme") != "NA" else None,
            "ops": row.get("ops") if row.get("ops") != "NA" else None,
            "pm": row.get("pm") if row.get("pm") != "NA" else None,
            "requestor": row.get("requestor") if row.get("requestor") != "NA" else None,
            "labels": row.get("labels") or [],
            "oldKey": row.get("oldkey") if row.get("oldkey") != "NA" else None,
            "mainProduct": row.get("mainprod") if row.get("mainprod") != "NA" else None,
            "ultimoStato": ultimo_stato,
            "nextSteps": next_steps,
        })

    def sort_key(r):
        p = r["priority"]
        if p is None:
            return (1, 0, r["key"])
        return (0, float(p), r["key"])

    rows.sort(key=sort_key)

    out_path = os.path.join(d, "dashboard_data_slim.json")
    with open(out_path, "w") as f:
        json.dump({"generatedAt": today.isoformat(), "items": rows}, f, ensure_ascii=False)

    print(f"wrote {out_path}: {len(rows)} items")
    with_status = sum(1 for r in rows if r["ultimoStato"])
    total_steps = sum(len(r["nextSteps"]) for r in rows)
    print(f"with ultimoStato: {with_status}, total next steps: {total_steps}")

if __name__ == "__main__":
    main()
