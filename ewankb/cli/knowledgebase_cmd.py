"""`ewankb knowledgebase` — Build domains/ + knowledgeBase/ (7-step pipeline)."""

import os
import sys
import subprocess

from ._helpers import EWANKB_ROOT, resolve_kb_dir


def run(args):
    kb_dir = resolve_kb_dir()
    os.chdir(kb_dir)

    def _run_script(script_path, extra_args=None):
        if not script_path.exists():
            print(f"  ({script_path.name} not found — skipping)")
            return
        env = dict(os.environ)
        env["EWANKB_DIR"] = str(kb_dir)
        env["PYTHONPATH"] = str(EWANKB_ROOT)
        env["PYTHONIOENCODING"] = "utf-8"
        rel = script_path.relative_to(EWANKB_ROOT)
        module = str(rel.with_suffix("")).replace("/", ".")
        cmd = [sys.executable, "-m", module]
        if extra_args:
            cmd.extend(extra_args)
        result = subprocess.run(cmd, env=env, capture_output=False)
        if result.returncode != 0:
            print(f"  WARNING: {script_path.name} exited with code {result.returncode}")

    scripts = EWANKB_ROOT / "ewankb" / "tools" / "extract_kb"
    skip_discover = getattr(args, 'skip_discover', False)

    if skip_discover:
        print("Step 1/7: Skipped (--skip-discover)")
    else:
        print("Step 1/7: Discovering domains from backend code...")
        from ewankb.tools.discover.discover_domains import discover
        discover(kb_dir, use_ai=True)

    print("\nStep 2/7: Analyzing code modules...")
    _run_script(scripts / "analyze_code.py")

    print("\nStep 3/7: Extracting and classifying documents...")
    _run_script(scripts / "extract_to_kb.py")

    print("\nStep 3b/7: Generating code module documentation...")
    _run_script(scripts / "gen_code_module_docs.py")

    print("\nStep 4/7: Enriching documents with code associations...")
    _run_script(scripts / "enrich_kb.py")

    print("\nStep 5/7: Generating domain overviews...")
    _run_script(scripts / "gen_domain_overview.py")

    print("\nStep 6/7: Generating process documents...")
    _run_script(scripts / "gen_processes.py")

    print("\nStep 7/7: Migrating documents to knowledgeBase/...")
    _run_script(scripts / "migrate_to_kb.py")

    from ewankb.tools.extract_kb.extract_to_kb import cleanup_empty_dirs
    cleanup_empty_dirs(kb_dir / "knowledgeBase")
    cleanup_empty_dirs(kb_dir / "domains")

    from ewankb.tools.incremental import update_hash
    result = update_hash()
    print(f"\nHash cache updated: {result['total_files']} files, {result['doc_mappings']} doc mappings")

    from ewankb.tools.graph_runtime.bm25_index import load_or_build
    bm25, docs = load_or_build()
    print(f"BM25 index built: {len(docs)} documents")

    print("\n=== Knowledge base build complete ===")
