"""`ewankb discover` — Re-run domain discovery."""

import os

from ._helpers import resolve_kb_dir


def run(args):
    kb_dir = resolve_kb_dir()
    os.chdir(kb_dir)

    from ewankb.tools.discover.discover_domains import discover
    discover(kb_dir, use_ai=True)

    from ewankb.tools.incremental import update_hash
    result = update_hash()
    print(f"Hash cache updated: {result['total_files']} files")
