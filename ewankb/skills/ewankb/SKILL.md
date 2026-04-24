---
name: ewankb
description: 从 Java 后端代码 + Confluence 文档构建结构化业务知识库。
trigger: /ewankb
---

# /ewankb

四层架构知识库构建工具：`source/` → `domains/` → `knowledgeBase/` → `graph/`

## 命令路由

| 输入 | 动作 |
|------|------|
| `/ewankb` 或 `/ewankb <路径>` | 完整构建（preflight → discover → 模块映射 → build） |
| `/ewankb --build-kb` | 仅 domains + knowledgeBase（含 discover + 模块映射） |
| `/ewankb --build-kb --skip-discover` | 跳到 [skip-discover 执行](#skip-discover-执行) |
| `/ewankb --build-graph` | 跳到 [references/graph-build.md](references/graph-build.md) |
| `/ewankb discover` | 跳到 [discover 单独执行](#discover-单独执行) |
| `/ewankb pull` | 跳到 [references/pull-flow.md](references/pull-flow.md) |
| `/ewankb push` | 跳到 [references/push-flow.md](references/push-flow.md) |
| `/ewankb diff` | 跳到 [references/diff-and-incremental.md](references/diff-and-incremental.md) |

## 完整构建流程

### 第 1 步 — preflight 检查 + 自动修复

```bash
cd "目标路径"
ewankb preflight --fix --dir .
```

解析 JSON 输出：
- `ready: true` 且无 `config_created` → 继续第 2 步
- `blockers` 含 `no_java_files` → 告诉用户把 Java 代码放到 `source/repos/`，停止
- `blockers` 含 `no_api_key` → 通过对话询问用户 API key，然后用 Edit 工具写入 `llm_config.json`
- `blockers` 含 `no_llm_config` → `llm_config.json` 缺失，用 `ewankb preflight --fix` 自动创建，然后询问用户填入 API key
- **`config_created: true`** → 首次初始化。**必须**调用 `AskUserQuestion` 展示大模型配置（API Key 前缀、Base URL、Model），让用户选择"继续使用当前配置"或"修改配置"

如果 `ewankb` 命令不存在，请先运行 `pip install ewankb`。

### 第 2 步 — 域发现

```bash
ewankb discover
```

扫描 `source/repos/` Java 包路径 → AI 翻译中文域名 → 写入 `domains/_meta/domains.json` + `module_mapping_context.md`。

### 第 3 步 — 代码模块映射（AI 自主探索）

读取 `domains/_meta/module_mapping_context.md`，检查是否存在 modules 为空的域。

**如果存在待映射的域**：
1. 阅读目录树，初步判断每个域的代码目录
2. 不确定的目录，浏览 Java 文件名和 `package` 语句确认归属
3. 用 Edit 工具修改 `domains/_meta/domains.json`，填充 `modules` 字段

映射规则：
- `modules` 值是目录路径列表（相对于 `source/repos/`）
- 微服务：服务模块目录名（如 `contract-atomic-service`）
- 单体：包路径中的业务子目录
- 一个域可对应多个目录，多个域可共享同一大目录的不同子包
- 只改 `modules` 字段，找不到代码的域保留 `modules: []`

**如果所有域都已有 modules**，跳过此步。

### 第 4 步 — 执行剩余流水线

```bash
ewankb knowledgebase --skip-discover
```

执行：analyze_code → extract → gen_code_module_docs → enrich → gen_overview → gen_processes → migrate

### 第 5 步 — 构建图谱

按 [references/graph-build.md](references/graph-build.md) 执行语义提取 + AST + 合并。

### 第 6 步 — 汇报结果

> 知识库构建完成。可用 `/ewankb push` 推送到远程仓库。
> 查询方式（使用 `/ewankb-query`）：
> - `/ewankb query "问题"` — 图谱查询
> - `/ewankb query-kb "问题"` — 文档直接查询
> - `/ewankb query-deep "问题"` — 双路对比查询

如果 `graph/domain_suggestions.json` 存在，读取 `data["suggestions"][:3]` 展示。

---

## 子命令

### --skip-discover 执行

用户输入 `/ewankb --build-kb --skip-discover` 时：
1. 运行 preflight 检查（第 1 步）
2. 跳过第 2、3 步
3. 直接运行 `ewankb knowledgebase --skip-discover`（第 4 步）
4. 汇报结果

### discover 单独执行

用户输入 `/ewankb discover` 时：
1. 运行 `ewankb discover`
2. 读取 `module_mapping_context.md`，按第 3 步规则完成 modules 填充
3. 展示域列表
