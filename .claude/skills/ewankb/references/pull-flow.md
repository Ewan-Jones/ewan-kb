# Pull 执行

拉取知识库和源码。

## 步骤 1 — 拉取 KB 仓库

```bash
cd "{kb_dir}"
git pull --rebase origin main
```

如果有冲突，告诉用户冲突文件列表。
如果尚未配置 remote，通过对话询问用户仓库地址，然后 `git remote add origin <地址>`。

## 步骤 2 — 同步源码仓库

读取 `source/repos/repos.json`（如果不存在，检查 `tools/fetch_repos/repos.json`），调用 fetch_repos：

```bash
cd "{kb_dir}"
python tools/fetch_repos/fetch_repos.py
```

如果 `repos.json` 不存在，通过对话引导配置：
1. 询问代码仓库列表（仓库名、git 地址、分支）
2. 用 Write 工具生成 `source/repos/repos.json`（参考 `tools/fetch_repos/repos.template.json`）
3. 生成后继续执行 fetch_repos

## 步骤 3 — 同步 Confluence 文档

读取 `source/docs/docs.json`，如果存在则拉取文档：

1. 通过对话询问用户 Confluence 账号和密码
2. 读取 `base_url` 和所有 `roots[].page_id`，拼接为逗号分隔的 ID 串
3. 执行拉取（全量覆盖）：

```bash
cd "{kb_dir}"
CONFLUENCE_BASE_URL="{base_url}" CONFLUENCE_USERNAME="{用户名}" CONFLUENCE_PASSWORD="{密码}" python tools/scrape_cf/scrape_confluence.py --root "{page_ids}" --output source/docs/
```

如果 `docs.json` 不存在，跳过。用户要求配置时引导：
1. 询问 Confluence 地址和根页面 ID（及描述）
2. 用 Write 工具生成 `source/docs/docs.json`（参考 `tools/scrape_cf/docs.template.json`）
3. 生成后继续执行拉取
