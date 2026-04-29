"""`ewankb analyze-code` — AST-based code analysis using graphify."""

from pathlib import Path
from collections import Counter


def run(args):
    path = Path(args.path).resolve()
    print(f"Analyzing code at {path}...")

    from graphify import extract, collect_files

    files = collect_files(path)
    if not files:
        print("No source files found.")
        return

    print(f"  Found {len(files)} files")
    result = extract(files)

    nodes = result.get("nodes", [])
    edges = result.get("edges", [])
    type_counts = Counter(n.get("type", "unknown") for n in nodes)
    print(f"  Extracted {len(nodes)} nodes, {len(edges)} edges")
    print(f"  Node types:")
    for t, c in type_counts.most_common():
        print(f"    {t}: {c}")
