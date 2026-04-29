"""`ewankb build-graph` — Build graph.json from source + domains."""

import os

from ._helpers import resolve_kb_dir


def run(args):
    from ewankb.tools.build_graph.graph_builder import build_graph

    kb_dir = resolve_kb_dir()
    os.chdir(kb_dir)

    from ewankb.tools import config_loader as cfg
    incremental = cfg.get_global_config().incremental

    print(f"Building graph (incremental={incremental})...")
    graph = build_graph(incremental=incremental)
    meta = graph["metadata"]
    print(f"Done. {meta['num_nodes']} nodes, {meta['num_links']} links")
    print(f"  Code files: {meta.get('code_files', '?')}")
    print(f"  Semantic nodes: {meta.get('semantic_nodes', 0)}")
    print(f"  Semantic edges: {meta.get('semantic_edges', 0)}")
    print(f"  Communities: {meta.get('communities', '?')}")
    print(f"  Engine: {meta.get('engine', '?')}")
    print(f"  Source hash: {meta['source_hash']}")
    print(f"  KB hash:     {meta['kb_hash']}")
