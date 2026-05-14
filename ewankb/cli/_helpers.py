"""Shared helpers for CLI commands."""

import os
import sys
from pathlib import Path

EWANKB_ROOT = Path(__file__).resolve().parent.parent.parent


def resolve_kb_dir() -> Path:
    env_dir = os.environ.get("EWANKB_DIR", "")
    if env_dir:
        return Path(env_dir).resolve()
    cwd = Path.cwd()
    if (cwd / "project_config.json").exists():
        return cwd
    if (cwd / "pyproject.toml").exists() and (cwd / "tools").exists():
        print("Error: Run this command from your knowledge base directory, "
              "or set EWANKB_DIR.", file=sys.stderr)
        sys.exit(1)
    print("Error: project_config.json not found in current directory.", file=sys.stderr)
    print("Run 'ewankb init <name>' first, or 'cd' to your knowledge base directory.", file=sys.stderr)
    sys.exit(1)


def graph_file() -> Path:
    kb_dir = resolve_kb_dir()
    gf = kb_dir / "graph" / "graph.json"
    if not gf.exists():
        print("Error: graph.json not found. Run 'ewankb build' first.", file=sys.stderr)
        sys.exit(1)
    return gf
