# GitHub 三种 pr 合并方式与对应 Git 命令（笔记版）

## 约定
- 远端：`origin`
- 基准分支：`main`
- PR 编号：`#123`（会抓取为本地分支 `pr-123`）
- 目的：在本地复现 GitHub 的三种“合并 PR”方式

---

## 一、获取 PR 分支（二选一）

方式 A：按 PR 编号抓取（推荐）
```bash
git fetch origin pull/123/head:pr-123
```

```bash
git fetch origin pull/<PR编号>/head:<本地分支名>
```

方式 B：从贡献者远端抓取（已知分支名）
```bash
git remote add contributor https://github.com/<user>/<repo>.git
git fetch contributor
git checkout -b pr-123 contributor/<feature-branch>
```

---

## 二、Create a merge commit（创建合并提交）
- 效果：保留 PR 的所有 commits，并新增一个“Merge pull request …”合并提交

命令
```bash
git checkout main
git pull origin main --ff-only

# 合并并强制生成合并提交（no-ff）
git merge --no-ff pr-123 -m "Merge pull request #123 from <user>/<branch>"

git push origin main
```

要点
- `--no-ff`：即便能快进，也创建一个合并 commit，便于保留 PR 边界
- Author/Committer：合并提交的 Author/Committer 通常为执行合并的人

---

## 三、Squash and merge（压缩为单个提交）
- 效果：将 PR 内多个 commits 压缩为 1 个新提交

命令
```bash
git checkout main
git pull origin main --ff-only

git merge --squash pr-123

# 以 PR 作者身份提交（可选修改）
git commit -m "feat: <summary> (squashed from #123)" --author="PR Author <email>"

# 如需联合署名（把下面行附加到提交消息中）
# Co-authored-by: Name <email>

git push origin main
```

要点
- 原始多个 commits 不会出现在主分支；贡献统计可通过 `Co-authored-by` 体现
- Author/Committer 可在提交时调整

---

## 四、Rebase and merge（变基后快进合并）
- 效果：把 PR 的每个提交线性“平铺”到 `main` 上；不产生额外合并提交

命令
```bash
# 先将 PR 分支变基到最新 main
git checkout pr-123
git fetch origin
git rebase origin/main
# 若冲突：解决后
# git add -A
# git rebase --continue

# 完成变基后，快进合并进 main
git checkout main
git pull origin main --ff-only
git merge --ff-only pr-123
git push origin main
```

要点
- Rebase 会改写提交的 SHA（历史“重写”）；Author 保留但 SHA 变化
- `--ff-only` 确保历史保持线性

---

## 五、合并结果验证
```bash
# 查看最近 30 条历史（图形化、简洁）
git log --graph --oneline --decorate -n 30

# 仅看合并提交（适用于 merge-commit 方式）
git log --merges --oneline

# 查看某 PR 分支的提交范围
git log origin/main..pr-123 --oneline
```

---

## 六、常见注意事项
- 受保护分支可能禁止直接 push 到 `main`；需使用有权限账号或 GitHub 网页端合并
- 贡献者邮箱未绑定 GitHub 账号时，提交记录可能显示为纯邮箱；建议绑定以正确归属
- `--no-ff` 与 `--ff-only` 组合使用，明确你的历史风格偏好

---

## 七、回滚与撤销（参考）
- 回滚某次合并提交（常用于 merge-commit 模式）
```bash
git revert -m 1 <merge-commit-sha>
git push origin main
```
- 回退分支指针（仅在无人共同协作或允许重写历史时）
```bash
git reset --hard <previous-sha>
git push -f origin main
```
