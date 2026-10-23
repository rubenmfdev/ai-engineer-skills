#!/usr/bin/env python3
"""Index and lint a folder of specs. Stdlib only.

  specs_index.py --init            create docs/specs/README.md and _template.md
  specs_index.py                   regenerate the index in README.md
  specs_index.py --check           lint, exit 1 on problems
  specs_index.py --next AREA       print the next free spec id
"""
import argparse
import re
import sys
from pathlib import Path

START, END = "<!-- specs-index:start -->", "<!-- specs-index:end -->"
REQUIRED = ("id", "title", "status", "area", "summary", "updated")
STATUSES = ("draft", "approved", "implemented", "deprecated", "superseded")
SKIP = {"README.md", "_template.md"}


def parse(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    fm = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, val = line.partition(":")
            val = val.strip().strip("\"'")
            if val.startswith("[") and val.endswith("]"):
                val = [v.strip().strip("\"'") for v in val[1:-1].split(",") if v.strip()]
            fm[key.strip()] = val
    return fm, text[end + 4:]


def load(root):
    specs = []
    for p in sorted(root.rglob("*.md")):
        if p.name in SKIP:
            continue
        fm, body = parse(p)
        specs.append((p, fm, body))
    return specs


def lint(root, specs, readme_text):
    errs, ids = [], {}
    for p, fm, body in specs:
        rel = p.relative_to(root)
        if fm is None:
            errs.append("%s: missing front matter" % rel)
            continue
        for key in REQUIRED:
            if not fm.get(key):
                errs.append("%s: missing %s" % (rel, key))
        if fm.get("status") and fm["status"] not in STATUSES:
            errs.append("%s: unknown status %r" % (rel, fm["status"]))
        sid = fm.get("id")
        if sid:
            if sid in ids:
                errs.append("%s: duplicate id %s (also %s)" % (rel, sid, ids[sid]))
            ids[sid] = rel
        if fm.get("status") in ("approved", "implemented") and not re.search(r"\*\*AC\d+\*\*", body):
            errs.append("%s: %s spec has no acceptance criteria (**AC1** ...)" % (rel, fm["status"]))
    for p, fm, _ in specs:
        if not fm:
            continue
        refs = [fm.get("supersedes"), fm.get("superseded_by")]
        refs += fm.get("related", []) if isinstance(fm.get("related"), list) else []
        for ref in refs:
            if ref and re.match(r"^[A-Z]+-\d+$", ref) and ref not in ids:
                errs.append("%s: references unknown spec %s" % (p.relative_to(root), ref))
    expected = render(root, specs)
    if START not in readme_text or expected not in readme_text:
        errs.append("README.md index is out of date, run specs_index.py")
    return errs


def render(root, specs):
    rows = []
    for p, fm, _ in specs:
        if not fm:
            continue
        rows.append((fm.get("area", ""), fm.get("id", ""), fm.get("title", ""), fm.get("status", ""),
                     fm.get("updated", ""), fm.get("summary", ""), p.relative_to(root)))
    lines = [START, "", "| ID | Title | Area | Status | Updated | Summary |", "| --- | --- | --- | --- | --- | --- |"]
    for area, sid, title, status, updated, summary, rel in sorted(rows):
        lines.append("| %s | [%s](%s) | %s | %s | %s | %s |" % (sid, title, rel.as_posix(), area, status, updated, summary))
    lines += ["", END]
    return "\n".join(lines)


def next_id(specs, area):
    prefix = re.sub(r"[^A-Z]", "", area.upper())[:6] or "SPEC"
    nums = [int(m.group(1)) for _, fm, _ in specs if fm and (m := re.match(r"^%s-(\d+)$" % prefix, fm.get("id", "")))]
    return "%s-%04d" % (prefix, max(nums, default=0) + 1)


README = """# Specs

Specs describe what the system should do, in testable terms. Agents: read this index first, then open only the specs that match your task. Update the spec in the same PR as the code.

Status: draft, approved, implemented, deprecated, superseded. Template: [_template.md](_template.md).

%s
%s
%s
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default="docs/specs")
    ap.add_argument("--init", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--next", metavar="AREA")
    a = ap.parse_args()
    root = Path(a.root)

    if a.init:
        root.mkdir(parents=True, exist_ok=True)
        template = Path(__file__).resolve().parent.parent / "assets" / "spec-template.md"
        if not (root / "_template.md").exists():
            (root / "_template.md").write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
        if not (root / "README.md").exists():
            (root / "README.md").write_text(README % (START, "", END), encoding="utf-8")
        print("initialized %s" % root)
        return 0
    if not root.exists():
        sys.exit("%s not found, run with --init" % root)

    specs = load(root)
    if a.next:
        print(next_id(specs, a.next))
        return 0
    readme = root / "README.md"
    text = readme.read_text(encoding="utf-8") if readme.exists() else ""
    if a.check:
        errs = lint(root, specs, text)
        for e in errs:
            print("ERROR " + e)
        print("%d specs checked, %d problems" % (len(specs), len(errs)))
        return 1 if errs else 0

    block = render(root, specs)
    if START in text and END in text:
        new = text[:text.index(START)] + block + text[text.index(END) + len(END):]
    else:
        new = README % (block, "", "") if not text else text.rstrip() + "\n\n" + block + "\n"
    readme.write_text(new, encoding="utf-8")
    print("index updated: %d specs" % len(specs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
