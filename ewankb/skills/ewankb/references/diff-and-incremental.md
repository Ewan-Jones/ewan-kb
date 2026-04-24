# Diff 与增量构建

## diff 执行

当用户输入 `/ewankb diff` 时，检测 source 目录变化并展示受影响的域。

```bash
cd "{kb_dir}"
ewankb diff
```

解析 JSON 输出，展示：
- 代码/文档各有多少新增、修改、删除
- 受影响的域列表

如果 hash 缓存不存在（首次执行），告诉用户"尚无基线，请先执行一次完整构建。"

## 增量构建逻辑

当 `/ewankb` 完整构建时，如果 `source/.cache/hashes.json` 已存在（非首次构建），在第 4 步之前插入增量检测：

1. 运行 `ewankb diff`，获取受影响的域列表
2. 如果无变更 → "源数据无变化，跳过构建"，直接跳到图谱构建
3. 如果有变更 → 执行清理：

```python
from tools.incremental import clean
result = clean(affected_domains)
```

4. 然后正常执行 `ewankb knowledgebase --skip-discover`，流水线自动只重跑被清理的域
5. 构建完成后 `update_hash` 自动内置在流水线末尾

如果 hash 缓存不存在（首次构建），跳过增量检测，走全量构建。
