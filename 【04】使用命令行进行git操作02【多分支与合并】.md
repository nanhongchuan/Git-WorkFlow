# Git 分支与合并 — 要点速记

## 1. 查看分支

* 列出**本地**分支：

```bash
git branch
```

* 列出**所有**分支（含远端）：

```bash
git branch -a
```

> 远端分支会以 `remotes/origin/...` 或 `origin/...` 的形式显示。&#x20;

---

## 2. 创建与切换分支

* 在**当前分支基础上创建并切换**：

```bash
git checkout -b <branch-name>
# 或等效
git switch -c <branch-name>
```

* 注意：新分支是基于当前所在分支创建的（即继承当前的提交历史）。&#x20;

---

## 3. 将本地分支推送到远端并建立关联（upstream）

```bash
git push --set-upstream origin <branch-name>
# 简写
git push -u origin <branch-name>
```

> 这样本地分支与远端分支建立追踪关系（后续 `git push` / `git pull` 更方便）。&#x20;

---

## 4. 切换 & 删除分支（小d与大D）

* **删除本地分支（安全删除）**：

```bash
git switch <other-branch>    # 不能删除当前分支，先切换
git branch -d <branch-name>  # 仅当该分支已被合并时可删除
```

* **强制删除本地分支**（不论是否合并）：

```bash
git branch -D <branch-name>
```

* **删除远端分支**：

```bash
git push origin --delete <branch-name>
```

> 小提示：不能删除当前分支，先 `git switch` 到别的分支再删除。&#x20;

---

## 5. 同步远端分支与在本地检出远端分支

* 远端新建分支后，本地不会自动出现，需要先同步远端引用：

```bash
git fetch
```

* 同步后，远端分支会显示在 `git branch -a` 中；可以检出为本地分支并建立追踪：

```bash
git checkout <remote-branch-name>   # 若远端存在，会自动创建本地并关联
# 或显式
git checkout -t origin/<branch-name>

# 或使用
git switch <remote-branch-name>   # Git 2.23 后推荐用这个替代 checkout 的分支切换功能
```

> `git fetch` 只同步引用，不会自动合并。&#x20;

> 都是把当前工作区切换到 main 分支。

---

## 6. 合并（merge）

* 切换到**接收合并**的分支，然后合并另一个分支进去：

```bash
git switch <target-branch>
git merge <source-branch>
```

* 也可以直接合并远端分支：

```bash
git merge origin/<branch-name>
```

> 合并成功后会把 source 的改动应用到 target。&#x20;

---

## 7. Fast-forward（快速前进）与 Non-fast-forward（非快速前进）

* **Fast-forward**：当目标分支没有新的提交（未分叉），合并时只需把指针向前移动即可（不会产生新的 merge commit）。
* **Non-fast-forward**：当两个分支各自有新的提交（已分叉），合并会产生一个新的合并提交（merge commit），并把两个历史线合并到一起。
* 如果你**即使可以快速前进也想保留合并提交**，使用 `--no-ff`：

```bash
git merge --no-ff <branch>
```

> `--no-ff` 会强制生成一个合并提交，即便本可用 fast-forward。&#x20;

---

## 8. Rebase（变基）

* 把当前分支的提交“移到”另一个分支之上（重放提交）：

```bash
git switch <feature-branch>
git rebase <base-branch>
```

* **注意**：rebase 会重写历史，若已推送到远端并被其他人基于，推送时通常需要强制推送（`--force` 或更安全的 `--force-with-lease`）。
* **例外**：当 feature 与 base 处于 fast-forward（无分叉）状态时，rebase 后可能不需要强制推送，普通 `git push` 即可。&#x20;

---

## 9. 比较分支：`git log` 与 `git diff`

* **按提交比较（两点 `..`）**（顺序重要）：

```bash
git log A..B     # 显示在 B 上但不在 A 上的提交（即 B 相对于 A 的新增提交）
git log B..A     # 反过来显示 A 相对于 B 的新增提交
```

* **三点 `...`（symmetric difference）**：

```bash
git log A...B    # 显示 A 与 B 各自独有的提交（两边不共有的提交）
```

* **按文件差异比较**：`git diff` 同理可用 `A..B` / `B..A`：

```bash
git diff A..B
# 下一节详细展开
```

> 两点比较有方向性，三点显示双方各自独有的提交集合。&#x20;

---

## 10. Squash Merge（压缩合并）

* 把多个提交压缩成一个提交合并到目标分支：

```bash
git switch <target-branch>
git merge --squash <source-branch>
# 注意：--squash 只把改动放到暂存区，不会自动生成 commit
git commit -m "合并并压缩 <source-branch> 的提交为一个"
git push
```

> `--squash` 需要手动 `git commit`，因为它不会自动生成合并提交。&#x20;

---

## 11. 处理冲突（merge / rebase）

* **合并冲突（merge）**：

  1. 执行 `git merge <branch>`，若出现冲突，Git 会标记冲突文件。
  2. 打开冲突文件，手动编辑，选择/合并要保留的内容，删除冲突标记（`<<<<<<<` / `=======` / `>>>>>>>`）。
  3. `git add <file>`。
  4. `git commit -m "resolve conflict"`（merge 会生成一次提交）。
  5. `git push`。
* **Rebase 冲突**：

  1. 在 rebase 过程遇到冲突，解决文件后 `git add <file>`。
  2. 继续 rebase：

     ```bash
     git rebase --continue
     ```
  3. 若放弃本次 rebase：

     ```bash
     git rebase --abort
     ```
  4. 提交信息编辑器（如果出现）可用 `i` 进入编辑，完成后 `Esc`，输入 `:wq!` 保存并退出（文档示例为 vim 操作）。&#x20;

---

## 12. Cherry-pick（挑选提交）

* 将某个分支上的一个或多个具体提交应用到当前分支：

```bash
git log main..feature 
# 查看feature分支比main分支多的commit信息

git cherry-pick <commit-id> [<commit-id> ...]
```

* 例如：只挑 `green` 和 `blue` 的提交（不要 `red`），把对应的 commit-id `cherry-pick` 到目标分支，然后 `git push`。&#x20;

---

## 13. 常用辅助命令与注意事项

* `git status`：查看当前分支、工作区和暂存区状态（非常常用）。
* `git add <file>` / `git commit -m "msg"`：常规提交流程；`git commit -am "msg"` 可跳过 `git add` 但仅对已跟踪文件有效。
* `git fetch`：仅同步远端引用，不自动合并。
* 推送时若改写了历史（rebase），**尽量**使用 `git push --force-with-lease`（比单纯 `--force` 更安全）。
* 不要在公共分支（多人协作已经基于的分支）上随意做 `rebase` 或改写已推送的历史，避免破坏他人工作流。&#x20;

---

## 14. 示例流程速查（常见操作顺序）

* 新建分支并推远端：

```bash
git switch -c feature2
# 做改动并提交
git push -u origin feature2
```

* 合并并解决冲突：

```bash
git switch main
git merge feature2
# 若冲突：编辑 -> git add <file> -> git commit -m "resolve conflict" -> git push
```

* 用 rebase 清理提交再推送：

```bash
git switch feature
git rebase main
# 处理冲突（若有） -> git rebase --continue
git push --force-with-lease
```

* 挑选单个提交到 main：

```bash
git switch main
git cherry-pick <commit1> <commit2>
git push
```

> 上面范例均来自课程笔记示例与操作步骤。&#x20;

---

## 15. 推荐的好习惯（来自笔记/实践）

* 合并前先 `git fetch`、`git status`、`git log` 检查差异与分叉情况。
* rebase 前确认是否会影响已推送的公共历史；若会，提前通知团队并优先用 `--force-with-lease` 推送。
* 解决冲突时小心保留正确代码，删除冲突标记后再 `git add`。
* 使用清晰的 commit message（例如 `resolve conflict`、`squash: three commits into one`）。&#x20;
