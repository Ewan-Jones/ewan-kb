#!/usr/bin/env python
"""扫描 ~/.ewankb 下所有知识库，输出名称和可用状态。"""
import json, os, sys

EWANKB_DIR = os.path.join(os.path.expanduser("~"), ".ewankb")
REGISTRY_PATH = os.path.join(EWANKB_DIR, "kb_registry.json")

def load_registry():
    if not os.path.isfile(REGISTRY_PATH):
        return {}
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return {k: v for k, v in data.items() if not k.startswith("_")}

def scan():
    if not os.path.isdir(EWANKB_DIR):
        print("ERROR: ~/.ewankb 目录不存在，请先运行 /ewankb 构建知识库")
        sys.exit(1)

    registry = load_registry()

    results = []
    scanned_dirs = set()
    for d in sorted(os.listdir(EWANKB_DIR)):
        kb_dir = os.path.join(EWANKB_DIR, d)
        if os.path.isfile(os.path.join(kb_dir, "project_config.json")):
            scanned_dirs.add(d)

    for kb_name, entry in sorted(registry.items()):
        dir_name = entry.get("dir", kb_name)
        display_name = entry.get("name") or kb_name
        description = entry.get("description", "")
        kb_dir = os.path.join(EWANKB_DIR, dir_name)
        kb_ok = os.path.isdir(os.path.join(kb_dir, "knowledgeBase"))
        graph_ok = os.path.isfile(os.path.join(kb_dir, "graph", "graph.json"))
        source_ok = os.path.isdir(os.path.join(kb_dir, "source", "repos"))
        results.append({"kb_name": kb_name, "dir": dir_name,
                        "display_name": display_name, "description": description,
                        "kb": kb_ok, "graph": graph_ok, "source": source_ok})

    for d in sorted(scanned_dirs):
        if any(r["dir"] == d for r in results):
            continue
        config_path = os.path.join(EWANKB_DIR, d, "project_config.json")
        with open(config_path, encoding="utf-8") as f:
            project_name = json.load(f).get("project_name", "")
        kb_dir = os.path.join(EWANKB_DIR, d)
        kb_ok = os.path.isdir(os.path.join(kb_dir, "knowledgeBase"))
        graph_ok = os.path.isfile(os.path.join(kb_dir, "graph", "graph.json"))
        source_ok = os.path.isdir(os.path.join(kb_dir, "source", "repos"))
        results.append({"kb_name": d, "dir": d,
                        "display_name": project_name or d, "description": "",
                        "kb": kb_ok, "graph": graph_ok, "source": source_ok})

    if "--json" in sys.argv:
        print(json.dumps(results, ensure_ascii=False))
        return

    if not results:
        print("ERROR: ~/.ewankb 下没有可用的知识库，请先运行 /ewankb 构建知识库")
        sys.exit(1)

    print(f"| {'库名':<6} | {'名称':<20} | {'概述':<36} |")
    print(f"|{'-'*8}|{'-'*22}|{'-'*38}|")
    for r in results:
        desc = r["description"] or "-"
        print(f"| {r['kb_name']:<6} | {r['display_name']:<20} | {desc:<36} |")
    print()
    print("用法: /ewankb-hub <库名> <问题>")
    print(f"示例: /ewankb-hub {results[0]['kb_name']} 出库直发单怎么解析")

scan()
