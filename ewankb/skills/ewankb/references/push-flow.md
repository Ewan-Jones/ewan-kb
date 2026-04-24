# Push 执行

构建完成后，commit 并推送到远程。

**前提**：`.gitignore` 中必须包含 `source/repos/**/.git`。如果不存在，自动追加。

## 步骤 1 — 检查 .gitignore

```bash
cd "{kb_dir}"
grep -qF 'source/repos/**/.git' .gitignore 2>/dev/null || echo 'source/repos/**/.git' >> .gitignore
```

## 步骤 2 — commit + 推送

```bash
cd "{kb_dir}"
git add -A
git diff --cached --quiet || git commit -m "update knowledge base"
git push origin main
```

如果 push 失败（远程有新提交），先 `git pull --rebase origin main` 再重试。
如果尚未配置 remote，通过对话询问用户仓库地址，然后 `git remote add origin <地址>`。
