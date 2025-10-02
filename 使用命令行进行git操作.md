# Git 知识点总结（完整版）

## 1. Git 基础操作

* **查看版本**

  ```bash
  git --version
  ```
* **克隆仓库**

  ```bash
  git clone <repo-url>
  ```
* **查看状态**

  ```bash
  git status
  ```
* **添加文件到暂存区**

  ```bash
  git add <file>
  git add .   # 添加所有修改
  ```
* **提交修改**

  ```bash
  git commit -m "message"
  git commit -am "message"   # 修改的文件直接添加+提交
  ```
* **推送到远端**

  ```bash
  git push
  ```
* **拉取更新**

  ```bash
  git pull             # fetch + merge
  git pull --rebase    # fetch + rebase（推荐）
  ```

---

## 2. 暂存区与文件操作

* **从暂存区移除文件**（不删除工作区的修改）

  ```bash
  git restore --staged <file>
  ```
* **丢弃工作区修改**

  ```bash
  git restore <file>
  ```
* **删除文件**

  ```bash
  git rm <file>
  ```
* **移动/重命名文件**

  ```bash
  git mv oldname newname
  ```

---

## 3. 合并与 Rebase

* `git pull = git fetch + git merge`

  * 会生成额外的 **merge commit (D)**
* `git pull --rebase`

  * 把你的提交“接到”远端最新提交后面，保持历史线性。

设置默认 rebase：

```bash
git config --global pull.rebase true
```

---

## 4. 查看历史

* **查看提交记录**

  ```bash
  git log
  ```


* **常用退出方法**
  - **q**  
  在 `git log` 打开的界面（`less`）中按 `q`，立即退出并返回 shell。（首选）

  - **Ctrl+C**  
  强制中断当前进程，适用在 `q` 无效或卡住时的应急手段。

   - **Ctrl+Z**  
  将 pager 挂起到后台（shell 提示符会回来），可用 `fg` 恢复；不推荐作为常规退出方式，只作临时挂起。
  

* **查看某次提交详情**

  ```bash
  git show <commit-id>
  ```

---

## 5. Git 的“后悔药”

### 1）Discard（丢弃修改，也叫rollback）

* 单个文件：

  ```bash
  git restore <file>
  ```
* 所有文件：

  ```bash
  git reset --hard
  ```

### 2）Reset（重置到历史提交）最常用：

```bash
git reset --mixed <commit-id>
```

⚠️ 若已推送远端 → 需要 `git push -f`（危险，不推荐在公共分支）。

### 3）Revert（安全撤销）

```bash
git revert <commit-id>
```

生成反向提交，抵消历史修改。多人协作推荐。

### 4）Amend（修改最后一次提交）

```bash
git commit --amend
```

* 只能改最新提交
* 若已推送远端 → 需要强推（⚠️ 不要在公共分支使用）

---

## 6. 总结

* **merge** → 会产生额外提交，历史复杂
* **rebase** → 保持线性历史，推荐
* **restore --staged** → 把文件从暂存区移回工作区（容易被忽视）
* 四大“后悔药”：Discard、Reset、Revert、Amend

---

 | Git操作  | Git 命令                           | 使用场景                          | 注意事项                                                                 |
|----------|------------------------------------|-----------------------------------|--------------------------------------------------------------------------|
| discard  | `git restore <文件名>` （单个文件）<br>`git reset --hard` （所有文件） | 工作区的修改还未 commit             | 舍弃掉工作区修改的文件                                                    |
| reset    | `git reset <commit ID>`            | 还原到某个 commit 的状态，舍弃之后的 commit | 如果 reset 已经推送远端的 commit，会造成强制推送，集成分支禁止强推                       |
| revert   | `git revert <commit ID>`           | 使用一个新的提交抵消掉某次 commit 的修改 |                                                                          |
| amend    | `git commit --amend`               | 只能修改最新的一次 commit           | 如果 amend 已经推送远端 commit，会造成强制推送，集成分支禁止强推                         |
