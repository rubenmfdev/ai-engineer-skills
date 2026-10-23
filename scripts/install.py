#!/usr/bin/env python3
"""Install skills from this repo into an agent's skills directory. Stdlib only."""
import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = {"claude": ".claude/skills"}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--target", choices=sorted(TARGETS), default="claude")
    p.add_argument("--dest", help="explicit skills directory (overrides --target)")
    p.add_argument("--project", action="store_true", help="install into ./ instead of ~/")
    p.add_argument("--only", help="comma-separated skill names")
    p.add_argument("--copy", action="store_true", help="copy instead of symlink")
    a = p.parse_args()

    if a.dest:
        dest = Path(a.dest).expanduser()
    else:
        base = Path.cwd() if a.project else Path.home()
        dest = base / TARGETS[a.target]
    dest.mkdir(parents=True, exist_ok=True)

    only = set(a.only.split(",")) if a.only else None
    found = {s.parent.name: s.parent for s in (ROOT / "skills").rglob("SKILL.md")}
    if only and only - set(found):
        sys.exit("unknown skills: %s" % ", ".join(sorted(only - set(found))))

    for name, src in sorted(found.items()):
        if only and name not in only:
            continue
        out = dest / name
        if out.is_symlink() or out.is_file():
            out.unlink()
        elif out.exists():
            shutil.rmtree(out)
        if a.copy:
            shutil.copytree(src, out)
        else:
            out.symlink_to(src, target_is_directory=True)
        print("installed %s -> %s" % (name, out))


if __name__ == "__main__":
    main()
