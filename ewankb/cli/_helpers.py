"""Shared helpers for CLI commands."""

import json
import os
import sys
from pathlib import Path

EWANKB_ROOT = Path(__file__).resolve().parent.parent.parent
GLOBAL_KB_DIR = Path.home() / ".ewankb"
GLOBAL_REGISTRY = GLOBAL_KB_DIR / "kb_registry.json"


def _scan_global_kbs() -> list[Path]:
    """Return list of KB directories found under ~/.ewankb/."""
    if not GLOBAL_KB_DIR.is_dir():
        return []
    results = []
    for entry in sorted(GLOBAL_KB_DIR.iterdir()):
        if entry.is_dir() and (entry / "project_config.json").exists():
            results.append(entry)
    return results


def find_global_kb(name: str) -> Path | None:
    """Look up a named KB in ~/.ewankb/kb_registry.json.

    Returns the resolved directory path, or None if not found.
    """
    if GLOBAL_REGISTRY.exists():
        try:
            with open(GLOBAL_REGISTRY, encoding="utf-8") as f:
                registry = json.load(f)
            entry = registry.get(name)
            if entry and isinstance(entry, dict):
                dir_name = entry.get("dir", name)
                kb_dir = GLOBAL_KB_DIR / dir_name
                if kb_dir.is_dir() and (kb_dir / "project_config.json").exists():
                    return kb_dir
        except (json.JSONDecodeError, OSError):
            pass
    # Fallback: try direct directory match
    direct = GLOBAL_KB_DIR / name
    if direct.is_dir() and (direct / "project_config.json").exists():
        return direct
    return None


def resolve_kb_dir() -> Path:
    env_dir = os.environ.get("EWANKB_DIR", "")
    if env_dir:
        return Path(env_dir).resolve()
    cwd = Path.cwd()
    if (cwd / "project_config.json").exists():
        return cwd
    # Fallback: check ~/.ewankb/ for global KBs
    global_kbs = _scan_global_kbs()
    if len(global_kbs) == 1:
        return global_kbs[0]
    if len(global_kbs) > 1:
        names = [d.name for d in global_kbs]
        print(f"Error: Multiple global KBs found in {GLOBAL_KB_DIR}: {', '.join(names)}", file=sys.stderr)
        print("Use --dir or EWANKB_DIR to specify which one.", file=sys.stderr)
        sys.exit(1)
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
