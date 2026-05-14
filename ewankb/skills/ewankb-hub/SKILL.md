---
name: ewankb-hub
description: 跨系统知识库查询枢纽。强制指定知识库名称查询，支持列出已有知识库。用法：/ewankb-hub list 列出知识库，/ewankb-hub <库名> [graph|kb|deep] <问题> 查询。
trigger: /ewankb-hub
---

# /ewankb-hub

跨系统知识库查询入口：必须指定知识库名称。

## 用法

```
/ewankb-hub list                           # 列出所有可用知识库
/ewankb-hub <库名> <问题>                  # 指定知识库，图谱查询（默认）
/ewankb-hub <库名> graph <问题>            # 指定知识库，图谱查询
/ewankb-hub <库名> kb <问题>               # 指定知识库，文档检索
/ewankb-hub <库名> deep <问题>             # 指定知识库，双路对比查询
```

库名为注册表中的简称，如 `oms`、`crm`、`erp` 等。用户输入库名，内部映射到文件夹路径。

## 关键规则

**必须将工具输出写入回复文本**。用户无法看到 Bash/Grep 等工具的原始输出，所有关键信息（表格、查询结果、文件内容）必须直接写入回复文本中展示给用户，不能仅在文字里笼统概括。

## 库名与文件夹映射

注册表 `~/.ewankb/kb_registry.json` 中，key 为库名（用户输入的简称），`dir` 字段为 `~/.ewankb/` 下的文件夹名。`dir` 可缺省，缺省时等于 key。

举例：
| 库名 | 文件夹 | 中文名称 |
|------|--------|----------|
| bms | bms-ewan-kb | BMS预算管理系统 |
| crm | crm-ewan-kb | CRM客户关系管理系统 |
| eam | eam-ewan-kb | EAM设备资产管理系统 |
| ems | ems-ewan-kb | EMS能源管理系统 |
| erp | erp-ewan-kb | ERP企业资源计划系统 |
| oms | oms-ewan-kb | OMS物流订单管理系统 |

## 执行步骤

### 0. 参数解析

从用户输入中解析参数：

- 如果输入为 `list` → 执行步骤 1（列出知识库），然后停止
- 否则，第一个词为 `库名`，后续为查询内容：
  - 库名后面紧跟 `graph`/`kb`/`deep` → 查询模式为对应类型，其余部分为问题
  - 库名后面不是上述子命令 → 图谱模式（默认），整个后续部分为问题
- **必须提供库名**。如果用户未提供库名，先自动执行步骤 1 列出可用知识库，然后停止，提示用户重新输入带库名的命令

### 1. 列出知识库（list 模式）

一键执行扫描脚本：

```bash
PYTHONIOENCODING=utf-8 python ~/.claude/skills/ewankb-hub/scan.py
```

脚本自动读取 `~/.ewankb/kb_registry.json` 注册表，输出表格（库名、名称、概述、文档库/图谱/源码状态）和用法提示。

**必须将表格内容完整写入回复文本**，用 markdown 表格格式展示给用户。

### 2. 定位知识库

根据用户提供的库名，从注册表获取文件夹名：

```bash
PYTHONIOENCODING=utf-8 python ~/.claude/skills/ewankb-hub/scan.py --json
```

从 JSON 结果中找到库名对应的条目：
- `kb_name` = 库名（用户输入的简称）
- `dir` = 文件夹名
- 设定 `kb_dir=~/.ewankb/{dir}`

如果库名不在 JSON 结果中 → 提示库名无效，建议运行 `/ewankb-hub list` 查看可用库名，停止

检查查询条件：
- 如果需要图谱模式但 `graph` 为 false → 提示切换到 kb 模式或运行 `/ewankb --build-graph`，停止
- 如果 `kb` 为 false → 知识库不完整，提示运行 `/ewankb --build-graph`，停止

### 3. 拉取最新数据（自动）

如果 `kb_dir` 是 git 仓库且有 remote：

```bash
cd "{kb_dir}" && git remote -v
```

有 remote 则静默拉取：

```bash
cd "{kb_dir}" && git pull --rebase origin main 2>&1 || true
```

### 4. 执行查询

以 `{kb_dir}` 作为知识库路径，按照 `/ewankb-query` skill 中的步骤 3A/3B/3C 执行对应模式的查询，步骤 3D 代码穿透也照原样执行。

具体命令：

- **图谱模式**：`ewankb query "用户问题" --json --dir "{kb_dir}"`
- **kb 模式**：`ewankb query-kb "用户问题" --dir "{kb_dir}"`
- **双路对比模式**：并行启动两个 subagent，分别执行 graph 和 kb 查询

**查询结果必须完整写入回复文本**，不能仅概括。

### 5. 回答约束

与 `/ewankb-query` 的回答约束完全一致：

- 严格模式约束：只用选定查询模式的结果回答，不自动切换模式
- 代码穿透是标配：所有模式回答后都执行代码穿透验证
- 结论优先、面向非技术人员、保持原问题、溯源到底、规格与实现必须对齐
- 不编造信息，引用具体文件路径和类名

回答开头注明选定的知识库：

```
基于 [{库名}] ({中文名称}) 知识库查询结果：
```
