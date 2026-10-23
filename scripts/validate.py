#!/usr/bin/env python3
"""Validate every SKILL.md under skills/. Stdlib only."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME, MAX_DESC, MAX_LINES = 64, 1024, 500
LINK_RE = re.compile(r"\]\((?!https?://|#|mailto:)([^)\s]+)\)")


def parse(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    fm = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip("\"'")
    return fm, text[end + 4:]


def check(skill_md):
    errs = []
    text = skill_md.read_text(encoding="utf-8")
    fm, body = parse(text)
    if fm is None:
        return ["missing or unterminated frontmatter"]
    name, desc = fm.get("name", ""), fm.get("description", "")
    if not name:
        errs.append("missing name")
    elif not NAME_RE.match(name) or len(name) > MAX_NAME:
        errs.append("invalid name %r" % name)
    elif name != skill_md.parent.name:
        errs.append("name %r does not match folder %r" % (name, skill_md.parent.name))
    if not desc:
        errs.append("missing description")
    elif len(desc) > MAX_DESC:
        errs.append("description over %d chars" % MAX_DESC)
    if len(text.splitlines()) > MAX_LINES:
        errs.append("over %d lines, move detail to references/" % MAX_LINES)
    for target in LINK_RE.findall(body):
        if not (skill_md.parent / target.split("#")[0]).exists():
            errs.append("broken link %s" % target)
    return errs


def check_external():
    import json
    errs, seen = [], set()
    local = {s.parent.name for s in (ROOT / "skills").rglob("SKILL.md")}
    data = json.loads((ROOT / "external-skills.json").read_text(encoding="utf-8"))
    for e in data["skills"]:
        for key in ("id", "category", "topic", "default", "license", "source", "description"):
            if key not in e:
                errs.append("external %s: missing %s" % (e.get("id", "?"), key))
        src = e.get("source", {})
        if e.get("kind") == "tool":
            if not (src.get("repo") and e.get("install")):
                errs.append("external %s: tool needs source.repo and install" % e.get("id"))
        elif not (src.get("repo") and "path" in src and src.get("ref")):
            errs.append("external %s: source needs repo, path, ref" % e.get("id"))
        if e.get("id") in seen or e.get("id") in local:
            errs.append("external %s: duplicate id" % e.get("id"))
        seen.add(e.get("id"))
    for e in data["skills"]:
        for dep in e.get("requires", []):
            if dep not in seen and dep not in local:
                errs.append("external %s: requires unknown skill %s" % (e["id"], dep))
    for e in errs:
        print("ERROR external-skills.json: %s" % e)
    return len(errs)


def main():
    skills = sorted((ROOT / "skills").rglob("SKILL.md"))
    failed, names = 0, {}
    for s in skills:
        rel = s.relative_to(ROOT)
        errs = check(s)
        names.setdefault(s.parent.name, []).append(rel)
        for e in errs:
            print("ERROR %s: %s" % (rel, e))
        failed += bool(errs)
    for n, paths in names.items():
        if len(paths) > 1:
            print("ERROR duplicate skill name %s: %s" % (n, ", ".join(map(str, paths))))
            failed += 1
    failed += check_external()
    print("%d skills checked, %d with errors" % (len(skills), failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
