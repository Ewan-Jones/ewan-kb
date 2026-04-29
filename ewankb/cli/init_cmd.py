"""`ewankb init` — Initialize a new knowledge base."""

import sys
import shutil
from pathlib import Path

from ._helpers import EWANKB_ROOT


def run(args):
    kb_dir = Path(args.name).resolve()
    if kb_dir.exists():
        print(f"Error: directory '{kb_dir}' already exists.", file=sys.stderr)
        sys.exit(1)

    print(f"Initializing knowledge base at {kb_dir}...")

    template_dir = EWANKB_ROOT / "ewankb" / "templates" / "knowledgeBase"
    shutil.copytree(template_dir, kb_dir / "knowledgeBase")

    (kb_dir / "source").mkdir()
    (kb_dir / "source" / "docs").mkdir()
    (kb_dir / "source" / "repos").mkdir()
    (kb_dir / "domains").mkdir()
    (kb_dir / "domains" / "_meta").mkdir()
    (kb_dir / "graph").mkdir()
    (kb_dir / "graph" / ".cache").mkdir()

    gitignore = kb_dir / ".gitignore"
    gitignore.write_text(
        "# Build state (rebuilt automatically)\n"
        "graph/.cache/\n"
        "knowledgeBase/_state/\n\n"
        "# Environment and config (contains API keys)\n"
        ".env\n"
        "llm_config.json\n",
        encoding="utf-8",
    )

    from ewankb.tools.config_loader import create_project_config
    create_project_config(kb_dir, args.name)
    print(f"  Created project_config.json + llm_config.json")

    print(f"\nCreated {kb_dir}/")
    print(f"Next steps:")
    print(f"  1. cd {kb_dir}")
    print(f"  2. Edit llm_config.json — fill in your API key (see examples/llm_config.example.json)")
    print(f"  3. Place backend Java code in source/repos/")
    print(f"  4. Place .md documents in source/docs/ (optional)")
    print(f"  5. ewankb build")
    print(f"  6. ewankb query 'your question'")
    print(f"")
    print(f"Directory structure:")
    print(f"  source/         Raw materials (code + docs)")
    print(f"  domains/        Auto-discovered business domains")
    print(f"  knowledgeBase/  AI-refined documents by type")
    print(f"  graph/          Knowledge graph")
