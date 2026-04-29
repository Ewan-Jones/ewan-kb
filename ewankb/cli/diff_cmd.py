"""`ewankb diff` — Detect source changes and show affected domains."""

import json
import os

from ._helpers import resolve_kb_dir


def run(args):
    kb_dir = resolve_kb_dir()
    os.chdir(kb_dir)

    from ewankb.tools.incremental import diff
    result = diff()

    if not result["has_changes"]:
        print("源数据无变化。")
        return

    changes = result["changes"]
    for cat in ("repos", "docs"):
        c = changes[cat]
        if any(c.values()):
            print(f"\n{cat}:")
            if c["added"]:
                print(f"  新增: {len(c['added'])} 个文件")
                for f in c["added"][:5]:
                    print(f"    + {f}")
                if len(c["added"]) > 5:
                    print(f"    ... 共 {len(c['added'])} 个")
            if c["modified"]:
                print(f"  修改: {len(c['modified'])} 个文件")
                for f in c["modified"][:5]:
                    print(f"    ~ {f}")
                if len(c["modified"]) > 5:
                    print(f"    ... 共 {len(c['modified'])} 个")
            if c["deleted"]:
                print(f"  删除: {len(c['deleted'])} 个文件")
                for f in c["deleted"][:5]:
                    print(f"    - {f}")
                if len(c["deleted"]) > 5:
                    print(f"    ... 共 {len(c['deleted'])} 个")

    domains = result["affected_domains"]
    if domains:
        print(f"\n受影响的域 ({len(domains)}):")
        for d in domains:
            print(f"  - {d}")
    else:
        print("\n未能确定受影响的域（新增文档无映射记录），建议全量构建。")

    print(f"\n[JSON] {json.dumps(result, ensure_ascii=False)}")
