"""`ewankb install` — Install ewankb skills to Claude Code."""

import os
import shutil
import sys
from pathlib import Path

from ._helpers import EWANKB_ROOT


def run(args):
    skills_src = EWANKB_ROOT / "ewankb" / "skills"
    if not skills_src.exists():
        skills_src = EWANKB_ROOT / ".claude" / "skills"
    if not skills_src.exists():
        print("Error: skill files not found.", file=sys.stderr)
        print("Please reinstall ewankb or copy skill files manually.", file=sys.stderr)
        sys.exit(1)

    if os.name == "nt":
        home = Path(os.environ.get("USERPROFILE", Path.home()))
    else:
        home = Path.home()
    skills_dst = home / ".claude" / "skills"
    skills_dst.mkdir(parents=True, exist_ok=True)

    copied = []
    for skill_dir in sorted(skills_src.iterdir()):
        if not skill_dir.is_dir() or not (skill_dir / "SKILL.md").exists():
            continue
        dst_dir = skills_dst / skill_dir.name
        if dst_dir.exists():
            shutil.rmtree(dst_dir)
        shutil.copytree(skill_dir, dst_dir)
        copied.append(skill_dir.name)

    print(f"Installed {len(copied)} skill(s) to {skills_dst}/")
    for d in copied:
        print(f"  - {skills_dst / d}/SKILL.md")

    claude_md = home / ".claude" / "CLAUDE.md"
    ewankb_section = (
        "# ewankb\n"
        "- **ewankb** (`~/.claude/skills/ewankb/`) — build knowledge base from Java code + docs. Trigger: `/ewankb`\n"
        "When the user types `/ewankb`, invoke the Skill tool with `skill: \"ewankb\"` before doing anything else.\n"
    )

    if claude_md.exists():
        content = claude_md.read_text(encoding="utf-8")
        if "# ewankb" not in content:
            content = content.rstrip() + "\n\n" + ewankb_section
            claude_md.write_text(content, encoding="utf-8")
            print(f"\nAdded ewankb trigger to {claude_md}")
        else:
            print(f"\newankb trigger already in {claude_md}")
    else:
        claude_md.parent.mkdir(parents=True, exist_ok=True)
        claude_md.write_text(ewankb_section, encoding="utf-8")
        print(f"\nCreated {claude_md} with ewankb trigger")

    print(f"\nDone. Use /ewankb in Claude Code to build a knowledge base.")
