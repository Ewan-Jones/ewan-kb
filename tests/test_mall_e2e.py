"""
End-to-end test for ewankb build + query pipeline using the mall fixture project.

Usage: pytest tests/test_mall_e2e.py -v

Prerequisites:
  - ANTHROPIC_API_KEY set in environment or ~/.config/ewankb/ewankb.toml
  - ewankb installed (pip install -e .)
"""

import json
import os
import shutil
from pathlib import Path

import pytest

EWANKB_ROOT = Path(__file__).resolve().parent.parent
FIXTURE_DIR = EWANKB_ROOT / "tests" / "fixtures" / "商城项目"
KB_OUTPUT_DIR = Path("/tmp/ewankb_test_mall")

# Resolve API key at module level for skipif marker
_api_key = os.environ.get("ANTHROPIC_API_KEY", "")
if not _api_key:
    cfg_dir = Path.home() / ".config" / "ewankb"
    cfg_file = cfg_dir / "ewankb.toml"
    if cfg_file.exists():
        import tomllib
        with open(cfg_file, "rb") as f:
            data = tomllib.load(f)
        _api_key = data.get("api", {}).get("api_key", "")

pytestmark = pytest.mark.skipif(
    not _api_key,
    reason="No API key available. Set ANTHROPIC_API_KEY or configure ~/.config/ewankb/ewankb.toml",
)


def _reset_config_caches():
    """Reset config_loader singleton caches so EWANKB_DIR is re-read."""
    import tools.config_loader as cfg
    cfg._global_cfg = None
    cfg._project_cfg = None
    cfg._llm_cfg = None


def _setup_kb_dir():
    """Initialize a KB directory at KB_OUTPUT_DIR with fixture source data."""
    if KB_OUTPUT_DIR.exists():
        shutil.rmtree(KB_OUTPUT_DIR)

    KB_OUTPUT_DIR.mkdir(parents=True)

    # Create directory structure
    (KB_OUTPUT_DIR / "source").mkdir()
    (KB_OUTPUT_DIR / "source" / "repos").mkdir()
    (KB_OUTPUT_DIR / "source" / "docs").mkdir()
    (KB_OUTPUT_DIR / "domains").mkdir()
    (KB_OUTPUT_DIR / "domains" / "_meta").mkdir()
    (KB_OUTPUT_DIR / "knowledgeBase").mkdir()
    (KB_OUTPUT_DIR / "graph").mkdir()
    (KB_OUTPUT_DIR / "graph" / ".cache").mkdir()

    # Copy fixture source data
    shutil.copytree(
        FIXTURE_DIR / "source" / "repos",
        KB_OUTPUT_DIR / "source" / "repos",
        dirs_exist_ok=True,
    )
    shutil.copytree(
        FIXTURE_DIR / "source" / "docs",
        KB_OUTPUT_DIR / "source" / "docs",
        dirs_exist_ok=True,
    )

    # Copy template knowledgeBase
    template_dir = EWANKB_ROOT / "ewankb" / "templates" / "knowledgeBase"
    shutil.copytree(
        template_dir,
        KB_OUTPUT_DIR / "knowledgeBase",
        dirs_exist_ok=True,
    )

    # Set EWANKB_DIR and create configs
    os.environ["EWANKB_DIR"] = str(KB_OUTPUT_DIR)
    _reset_config_caches()

    from tools.config_loader import create_project_config, get_global_config

    gcfg = get_global_config()
    create_project_config(KB_OUTPUT_DIR, "商城项目业务知识库")

    # Write API key into llm_config.json
    llm_cfg = {
        "api_key": _api_key,
        "base_url": gcfg.base_url,
        "model": gcfg.default_model,
        "api_protocol": "anthropic",
    }
    with open(KB_OUTPUT_DIR / "llm_config.json", "w", encoding="utf-8") as f:
        json.dump(llm_cfg, f, indent=2, ensure_ascii=False)

    # Create .gitignore
    (KB_OUTPUT_DIR / ".gitignore").write_text(
        "graph/.cache/\nknowledgeBase/_state/\n.env\nllm_config.json\n"
    )

    print(f"KB directory initialized at {KB_OUTPUT_DIR}", flush=True)


def test_full_pipeline():
    """Run full ewankb pipeline: init -> discover -> build KB -> build graph -> query."""
    _setup_kb_dir()

    # ── Step 1: Discover domains ──
    os.environ["EWANKB_DIR"] = str(KB_OUTPUT_DIR)
    _reset_config_caches()

    from tools.discover.discover_domains import discover

    result = discover(KB_OUTPUT_DIR, use_ai=True)
    domain_list = result.get("domain_list", [])
    print(f"Discovered {len(domain_list)} domains: {domain_list}", flush=True)
    assert len(domain_list) >= 3, f"Expected ≥3 domains, got {len(domain_list)}"

    # Verify domains.json written
    domains_file = KB_OUTPUT_DIR / "domains" / "_meta" / "domains.json"
    assert domains_file.exists(), "domains.json not created"
    with open(domains_file, encoding="utf-8") as f:
        data = json.load(f)
    all_english_keys = []
    for info in data.get("domains", {}).values():
        all_english_keys.extend(info.get("english_keys", []))
    assert "order" in all_english_keys, f"order not found in english_keys: {all_english_keys}"

    # ── Step 2: Build knowledge base ──
    os.environ["EWANKB_DIR"] = str(KB_OUTPUT_DIR)
    _reset_config_caches()
    os.chdir(KB_OUTPUT_DIR)

    from ewankb.__main__ import cmd_knowledgebase

    cmd_knowledgebase(skip_discover=True)

    # Verify BM25 index exists
    bm25_cache = KB_OUTPUT_DIR / "knowledgeBase" / "_state" / "bm25_index.pkl"
    assert bm25_cache.exists(), "BM25 index not created"

    # ── Step 3: Build graph ──
    os.environ["EWANKB_DIR"] = str(KB_OUTPUT_DIR)
    _reset_config_caches()

    from tools.build_graph.graph_builder import build_graph

    graph = build_graph(
        source_dir=KB_OUTPUT_DIR / "source",
        domains_dir=KB_OUTPUT_DIR / "domains",
        graph_dir=KB_OUTPUT_DIR / "graph",
    )
    nodes = graph.get("nodes", [])
    links = graph.get("links", [])
    meta = graph.get("metadata", {})
    print(f"Graph: {meta.get('num_nodes', len(nodes))} nodes, {meta.get('num_links', len(links))} links", flush=True)
    assert len(nodes) > 0, "Graph has no nodes"

    # Verify graph.json written
    graph_file = KB_OUTPUT_DIR / "graph" / "graph.json"
    assert graph_file.exists(), "graph.json not created"

    # ── Step 4: Query graph ──
    from ewankb.context import KBContext

    ctx = KBContext(KB_OUTPUT_DIR)
    ctx.load_graph()

    graph_result = ctx.query_graph("订单创建流程", verbose=True)
    matched = graph_result.get("matched_start_nodes", [])
    visited = graph_result.get("nodes", [])
    print(f"Query '订单创建流程': {len(matched)} matched, {len(visited)} visited", flush=True)
    assert len(matched) > 0 or len(visited) > 0, "Graph query returned no results"

    # ── Step 5: Query KB ──
    ctx.load_bm25()
    assert ctx.docs is not None, "BM25 docs not loaded"
    assert len(ctx.docs) > 0, "No BM25 documents found"

    kb_result = ctx.query_kb("库存校验规则", max_results=5)
    print(f"Query-KB '库存校验规则': {len(kb_result)} chars returned", flush=True)
    assert len(kb_result) > 50, "KB query returned too short result"

    # ── Cleanup ──
    shutil.rmtree(KB_OUTPUT_DIR)
    print("E2E test passed, cleanup done.", flush=True)