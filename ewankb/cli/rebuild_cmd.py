"""`ewankb rebuild` — Delete all generated artifacts for a clean rebuild."""

import shutil

from ._helpers import resolve_kb_dir


def run(args):
    kb_dir = resolve_kb_dir()

    targets = [
        kb_dir / "domains",
        kb_dir / "knowledgeBase",
        kb_dir / "graph",
        kb_dir / "source" / ".cache",
    ]

    removed = []
    for t in targets:
        if t.exists():
            shutil.rmtree(t)
            removed.append(str(t.relative_to(kb_dir)))

    if removed:
        print(f"已清理: {', '.join(removed)}")
    else:
        print("无需清理（目录均不存在）。")
    print("可以重新运行 ewankb build 进行全量构建。")
