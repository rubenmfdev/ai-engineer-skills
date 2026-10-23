#!/usr/bin/env python3
"""Browse and install skills from this catalog (local skills plus curated external ones).

Examples:
  install.py --list                          show everything
  install.py --category swift --project      install default Swift skills into ./.claude/skills
  install.py --category swift --topic security,accessibility
  install.py --only swiftui-expert-skill,adr-writing
  install.py --category swift --all          include optional and alternative skills too
Stdlib only. External skills are cloned from their own repositories at install time.
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = {"claude": ".claude/skills"}


def read_description(skill_md):
    text = skill_md.read_text(encoding="utf-8")
    for line in text.split("---")[1].splitlines() if text.startswith("---") else []:
        if line.startswith("description:"):
            return line.partition(":")[2].strip().strip("\"'")
    return ""


def load_catalog():
    entries = []
    for md in sorted((ROOT / "skills").rglob("SKILL.md")):
        entries.append({
            "id": md.parent.name,
            "category": md.parent.parent.name,
            "topic": "own",
            "default": True,
            "license": "MIT",
            "source": {"local": str(md.parent.relative_to(ROOT))},
            "description": read_description(md),
        })
    ext = json.loads((ROOT / "external-skills.json").read_text(encoding="utf-8"))
    entries.extend(ext["skills"])
    return entries


def split(value):
    return {v.strip() for v in value.split(",") if v.strip()} if value else set()


def select(entries, a):
    ids, cats, topics = split(a.only), split(a.category), split(a.topic)
    unknown = ids - {e["id"] for e in entries}
    if unknown:
        sys.exit("unknown skills: %s" % ", ".join(sorted(unknown)))
    out = []
    for e in entries:
        if ids:
            if e["id"] in ids:
                out.append(e)
            continue
        if cats and e["category"] not in cats:
            continue
        if topics and e["topic"] not in topics:
            continue
        if not (e["default"] or a.all):
            continue
        out.append(e)
    by_id = {e["id"]: e for e in entries}
    seen = {e["id"] for e in out}
    queue = list(out)
    while queue:
        for dep in queue.pop().get("requires", []):
            if dep not in seen:
                seen.add(dep)
                out.append(by_id[dep])
                queue.append(by_id[dep])
    return out


def print_list(entries, as_json):
    if as_json:
        print(json.dumps(entries, indent=2, ensure_ascii=False))
        return
    for e in entries:
        src = e["source"].get("local") or e["source"]["repo"]
        flag = "" if e["default"] else " (optional)"
        if e.get("kind") == "tool":
            flag += " [tool: run the commands yourself]"
        print("%-34s %-16s %-14s %s%s" % (e["id"], e["category"], e["topic"], src, flag))
        print("    " + e["description"][:150])


def git(*args, cwd=None):
    subprocess.run(["git"] + list(args), cwd=cwd, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def show_tool(e):
    print("TOOL %s (%s): not a skill folder, install it yourself." % (e["id"], e["license"]))
    print("  " + e["description"])
    for need in e.get("needs", []):
        print("  needs: %s" % need)
    for cmd in e["install"]:
        print("  run:   %s" % cmd)
    if e.get("usage"):
        print("  use:   %s" % e["usage"])
    if e.get("note"):
        print("  note:  %s" % e["note"])


def install(e, dest, clones, tmp, copy, dry):
    if e.get("kind") == "tool":
        show_tool(e)
        return
    out = dest / e["id"]
    src_desc = e["source"].get("local") or "%s/%s" % (e["source"]["repo"], e["source"]["path"])
    if e["license"] == "NONE":
        print("  note: %s declares no license; check with the author before redistributing" % e["id"])
    if dry:
        print("would install %s from %s -> %s" % (e["id"], src_desc, out))
        return
    if out.is_symlink() or out.is_file():
        out.unlink()
    elif out.exists():
        shutil.rmtree(out)
    if "local" in e["source"]:
        src = ROOT / e["source"]["local"]
        if copy:
            shutil.copytree(src, out)
        else:
            out.symlink_to(src, target_is_directory=True)
    else:
        repo, ref = e["source"]["repo"], e["source"]["ref"]
        if repo not in clones:
            target = Path(tmp) / repo.replace("/", "__")
            git("clone", "--depth", "1", "--branch", ref, "https://github.com/%s.git" % repo, str(target))
            sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=target, capture_output=True,
                                 text=True, check=True).stdout.strip()
            clones[repo] = (target, sha)
        target, sha = clones[repo]
        src = target / e["source"]["path"]
        if not (src / "SKILL.md").exists():
            sys.exit("%s has no SKILL.md at %s (catalog out of date?)" % (repo, e["source"]["path"]))
        noise = [".git"] + ([".github", "tests", "node_modules", "assets"] if not e["source"]["path"] else [])
        shutil.copytree(src, out, ignore=shutil.ignore_patterns(*noise))
        (out / ".source").write_text("https://github.com/%s/tree/%s/%s\n" % (repo, sha, e["source"]["path"]))
    print("installed %-34s <- %s" % (e["id"], src_desc))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--list", action="store_true", help="list matching skills and exit")
    p.add_argument("--json", action="store_true", help="with --list, print JSON")
    p.add_argument("--category", help="comma-separated, e.g. swift,devops")
    p.add_argument("--topic", help="comma-separated, e.g. security,store (see --list)")
    p.add_argument("--only", help="comma-separated skill ids")
    p.add_argument("--all", action="store_true", help="include optional and alternative skills")
    p.add_argument("--target", choices=sorted(TARGETS), default="claude")
    p.add_argument("--dest", help="explicit skills directory (overrides --target)")
    p.add_argument("--project", action="store_true", help="install into ./ instead of ~/")
    p.add_argument("--project-dir", help="install into <dir>/.claude/skills (implies --project)")
    p.add_argument("--copy", action="store_true", help="copy local skills instead of symlinking")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()

    entries = load_catalog()
    if a.list:
        chosen = select(entries, a) if (a.only or a.category or a.topic) else entries
        if not (a.only or a.category or a.topic or a.all):
            chosen = entries
        print_list(chosen, a.json)
        return
    if not (a.only or a.category or a.topic):
        sys.exit("choose what to install with --category, --topic or --only (see --list)")

    chosen = select(entries, a)
    if not chosen:
        sys.exit("nothing matched")
    if a.dest:
        dest = Path(a.dest).expanduser()
    else:
        if a.project_dir:
            base = Path(a.project_dir).expanduser().resolve()
        else:
            base = Path.cwd() if a.project else Path.home()
        dest = base / TARGETS[a.target]
    if not a.dry_run:
        dest.mkdir(parents=True, exist_ok=True)

    clones = {}
    with tempfile.TemporaryDirectory() as tmp:
        for e in chosen:
            install(e, dest, clones, tmp, a.copy or "local" not in e["source"], a.dry_run)
    tools = sum(1 for e in chosen if e.get("kind") == "tool")
    print("%d skills -> %s" % (len(chosen) - tools, dest) + ("; %d tool(s) need manual install" % tools if tools else ""))


if __name__ == "__main__":
    main()
