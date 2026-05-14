"""`ewankb preflight` — Check environment readiness."""

import json
import os
import sys
from pathlib import Path

from ._helpers import EWANKB_ROOT, find_global_kb


def _resolve_target(args) -> Path:
    if getattr(args, "dir", None):
        return Path(args.dir).resolve()
    name = getattr(args, "name", None)
    if name:
        kb_dir = find_global_kb(name)
        if kb_dir is None:
            print(f"Error: KB '{name}' not found in ~/.ewankb/", file=sys.stderr)
            print("Register it in ~/.ewankb/kb_registry.json or use --dir to specify a path.", file=sys.stderr)
            sys.exit(1)
        return kb_dir.resolve()
    return Path.cwd().resolve()


def run(args):
    target = _resolve_target(args)
    result = {
        "ewankb_root": str(EWANKB_ROOT),
        "kb_dir": str(target),
        "installed": True,
        "dirs": {},
        "counts": {},
        "api": {},
        "graph": {},
        "ready": True,
        "blockers": [],
    }

    dir_checks = {
        "project_config": target / "project_config.json",
        "llm_config": target / "llm_config.json",
        "source": target / "source",
        "source_repos": target / "source" / "repos",
        "source_docs": target / "source" / "docs",
        "domains": target / "domains",
        "knowledgeBase": target / "knowledgeBase",
        "graph": target / "graph",
    }
    for key, path in dir_checks.items():
        result["dirs"][key] = path.exists()

    if args.fix:
        for d in ["source/repos", "source/docs", "domains/_meta",
                   "knowledgeBase/_meta", "knowledgeBase/_state", "graph/.cache"]:
            (target / d).mkdir(parents=True, exist_ok=True)
        for key, path in dir_checks.items():
            result["dirs"][key] = path.exists()

        cfg_path = target / "project_config.json"
        llm_path = target / "llm_config.json"
        if not cfg_path.exists() or not llm_path.exists():
            from ewankb.tools.config_loader import create_project_config, get_global_config
            gcfg = get_global_config()
            create_project_config(target, f"{target.name}业务知识库")
            result["dirs"]["project_config"] = True
            result["dirs"]["llm_config"] = True
            result["config_created"] = True
            result["config_values"] = {
                "base_url": gcfg.base_url or "(default: api.anthropic.com)",
                "model": gcfg.default_model,
            }

    repos_dir = target / "source" / "repos"
    docs_dir = target / "source" / "docs"
    java_files = list(repos_dir.rglob("*.java")) if repos_dir.exists() else []
    doc_files = list(docs_dir.rglob("*.md")) if docs_dir.exists() else []
    result["counts"]["java_files"] = len(java_files)
    result["counts"]["doc_files"] = len(doc_files)

    try:
        os.environ["EWANKB_DIR"] = str(target)
        import ewankb.tools.config_loader as _cfg_mod
        _cfg_mod._global_cfg = None
        _cfg_mod._project_cfg = None
        _cfg_mod._llm_cfg = None

        from ewankb.tools.config_loader import get_project_config, get_llm_config
        llm = get_llm_config()
        pcfg = get_project_config()
        api_key = llm.get("api_key") or pcfg.get("api_key", "")
        base_url = llm.get("base_url") or pcfg.get("base_url", "")
        model = llm.get("model") or pcfg.get("model", "")
        result["api"] = {
            "key_configured": bool(api_key),
            "key_preview": (api_key[:8] + "...") if api_key else "",
            "base_url": base_url,
            "model": model,
        }
    except Exception as e:
        result["api"] = {"key_configured": False, "error": str(e)}

    graph_file = target / "graph" / "graph.json"
    if graph_file.exists():
        try:
            with open(graph_file, encoding="utf-8") as f:
                gdata = json.load(f)
            meta = gdata.get("metadata", {})
            result["graph"] = {
                "exists": True,
                "nodes": meta.get("num_nodes", len(gdata.get("nodes", []))),
                "links": meta.get("num_links", len(gdata.get("links", []))),
                "engine": meta.get("engine", "?"),
                "created_at": meta.get("created_at", "?"),
            }
        except Exception:
            result["graph"] = {"exists": True, "error": "parse_failed"}
    else:
        result["graph"] = {"exists": False}

    blockers = []
    for required_dir in ("source", "domains", "knowledgeBase", "graph"):
        if not result["dirs"].get(required_dir):
            blockers.append(f"no_{required_dir}")
    if not result["dirs"]["project_config"]:
        blockers.append("no_project_config")
    if not args.query:
        if not result["dirs"]["llm_config"]:
            blockers.append("no_llm_config")
        if result["counts"]["java_files"] == 0:
            blockers.append("no_java_files")
        if not result["api"].get("key_configured"):
            blockers.append("no_api_key")
    result["blockers"] = blockers
    result["ready"] = len(blockers) == 0

    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not result["ready"]:
        sys.exit(1)
