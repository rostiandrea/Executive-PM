#!/usr/bin/env python3
"""
Inject dashboard_data_slim.json (base data) and an edits JSON (viewer edits
already saved on the live artifact) into dashboard_template.html, producing
a self-contained HTML file ready to hand to the Artifact tool.

Usage:
  python3 publish_dashboard.py --data-dir . --template dashboard_template.html \
      --edits current_edits.json --out dashboard_final.html

If --edits is omitted or the file doesn't exist, an empty edits object is
used (fine for the very first publish; NEVER do this on a refresh of an
already-live artifact that has real edits on it — see
dashboard-refresh-procedure.md for how to fetch and reuse them).
"""
import json, argparse, os

def escape_for_script(s):
    return s.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=".")
    ap.add_argument("--template", default="dashboard_template.html")
    ap.add_argument("--edits", default=None)
    ap.add_argument("--out", default="dashboard_final.html")
    args = ap.parse_args()

    with open(os.path.join(args.data_dir, "dashboard_data_slim.json")) as f:
        base_json_text = f.read()

    if args.edits and os.path.exists(args.edits):
        with open(args.edits) as f:
            edits_obj = json.load(f)
    else:
        edits_obj = {"items": {}}

    base_escaped = escape_for_script(base_json_text)
    edits_escaped = escape_for_script(json.dumps(edits_obj, ensure_ascii=False))

    tpl = open(args.template).read()
    if "__BASE_DATA_JSON__" not in tpl:
        raise SystemExit("template missing __BASE_DATA_JSON__ marker")
    out = tpl.replace("__BASE_DATA_JSON__", base_escaped).replace("__EDITS_JSON__", edits_escaped)

    with open(args.out, "w") as f:
        f.write(out)
    print(f"wrote {args.out}: {len(out)} bytes")

if __name__ == "__main__":
    main()
