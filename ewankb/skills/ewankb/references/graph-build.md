# Build Graph 执行

当用户输入 `/ewankb --build-graph` 时，执行 AST 提取 + 域文档语义提取 + 图谱构建。

## 步骤 1 — 收集 domains/ 下的文档文件

```bash
cd "{kb_dir}"
python -c "
import json
from pathlib import Path

doc_files = []
domains_dir = Path('domains')
if domains_dir.exists():
    for f in sorted(domains_dir.rglob('*.md')):
        doc_files.append(str(f))
    dj = domains_dir / '_meta' / 'domains.json'
    if dj.exists():
        doc_files.append(str(dj))
Path('graph/.doc_files.txt').write_text('\n'.join(doc_files), encoding='utf-8')
print(f'域文档文件数: {len(doc_files)}')
"
```

如果文档数为 0，跳到步骤 3（只做 AST 图谱）。

## 步骤 2 — 逐域语义提取

读取 `domains/_meta/domains.json` 获取域列表，逐域处理：

对每个域：
1. Read `domains/{域名}/README.md`
2. Read `domains/{域名}/PROCESSES.md`
3. 提取：
   - **域概念**（职责、实体、表/接口/模块）→ node（每域至少 5-10 个）
   - **业务流程**（每个流程步骤独立节点，步骤间 `precedes` 边）→ node + edge
   - **代码类名引用** → `belongs_to` 边（文档节点 → AST 节点）
4. 累积到 nodes/edges 列表

**提取粒度**：
- 每域至少 5 个概念节点（职责、实体、接口、表、规则）
- PROCESSES.md 每个流程的每个步骤都是独立节点
- README 中列出的每个 Rest/Controller/Service 类都创建 `belongs_to` 边

**提取规则**：
- node id：`{域名}_{概念名}`
- node 字段：`id`、`label`、`file_type`（`"document"`）、`source_file`、`domain`
- edge relation：`contains`、`references`、`depends_on`、`precedes`、`belongs_to`、`manages`
- 代码实体 target 用**小写类名**（如 `anomalyrecordrest`），AST 节点的实际 ID 格式。`build_graph()` 也支持 `路径::类名` 模糊匹配
- 置信度：
  - `EXTRACTED`（1.0）：文档明确声明
  - `INFERRED`（0.6-0.9）：合理推断
  - `AMBIGUOUS`（0.1-0.3）：不确定

写入 `graph/.semantic_extraction.json`：
```json
{
  "nodes": [{"id": "...", "label": "...", "file_type": "document", "source_file": "...", "domain": "..."}],
  "edges": [{"source": "...", "target": "...", "relation": "...", "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "..."}]
}
```

## 步骤 3 — 构建图谱

`build_graph()` 自动检测 `graph/.semantic_extraction.json` 与 AST 结果合并。

```bash
ewankb build-graph
```

## 步骤 4 — 清理 + 汇报

```bash
rm -f graph/.doc_files.txt graph/.semantic_extraction.json
```

展示节点/边数量统计。如果 `graph/domain_suggestions.json` 存在，读取 `data["suggestions"][:3]` 展示。
