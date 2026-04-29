"""`ewankb query` / `ewankb query-graph` / `ewankb query-kb`."""

import json
import os
import sys
from pathlib import Path


def run(args):
    from ewankb.query import query, query_graph_json

    if getattr(args, 'dir', None):
        kb_dir = Path(args.dir).resolve()
        os.environ["EWANKB_DIR"] = str(kb_dir)
        import ewankb.tools.config_loader as _cfg_mod
        _cfg_mod._global_cfg = None
        _cfg_mod._project_cfg = None
        _cfg_mod._llm_cfg = None
        graph_file = kb_dir / "graph" / "graph.json"
    else:
        graph_file = None

    traversal = args.traversal
    if args.depth and not traversal:
        traversal = "bfs"

    max_nodes = None
    if args.depth:
        max_nodes = args.depth * 15
        if args.limit and args.limit < max_nodes:
            max_nodes = args.limit
    elif args.limit:
        max_nodes = args.limit

    if args.json:
        result = query_graph_json(
            args.text,
            graph_file=graph_file,
            traversal=traversal,
            max_nodes=max_nodes,
            verbose=args.verbose,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        result = query(
            args.text,
            graph_file=graph_file,
            traversal=traversal,
            max_nodes=max_nodes,
            max_tokens=args.max_tokens,
        )
        if args.verbose:
            print(f"[DEBUG] Query: {args.text}", file=sys.stderr)
            print(f"[DEBUG] Traversal: {traversal}, max_nodes: {max_nodes}", file=sys.stderr)
        print(result)


def run_kb(args):
    from ewankb.query import query_kb

    if getattr(args, 'dir', None):
        kb_dir = Path(args.dir).resolve()
        os.environ["EWANKB_DIR"] = str(kb_dir)
        import ewankb.tools.config_loader as _cfg_mod
        _cfg_mod._global_cfg = None
        _cfg_mod._project_cfg = None
        _cfg_mod._llm_cfg = None

    result = query_kb(
        args.text,
        domain_filter=args.domain,
        max_results=args.max_results,
    )
    print(result)
