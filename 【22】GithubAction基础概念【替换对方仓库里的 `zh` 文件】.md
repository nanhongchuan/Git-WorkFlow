# GitHub Actions 基础概念笔记

## 一、GitHub Actions 是什么

* **定义**：GitHub Actions 是 GitHub 提供的自动化流水线（Automation Pipeline）功能。
* **核心作用**：通过编写一个 Action 脚本，让 GitHub 自动完成一系列操作。
* **常见用途**：实现 CI/CD（持续集成 Continuous Integration、持续交付 Continuous Delivery）。

---

## 二、CI/CD 典型应用场景

当我们提交代码后，可以自动执行以下任务：

* 自动运行单元测试
* 自动编译与构建程序
* 自动推送到服务器
* 自动部署项目

> 整个自动化流程称为 **CI/CD 流程（Pipeline）**。

---

## 三、Action 的复用与共享机制

* GitHub 允许将每个自动化操作写成独立的 **Action 脚本**。
* 这些 Action 文件可以存放在仓库中，供他人复用。
* 开发者无需重新编写复杂脚本，直接**引用别人写好的 Action** 即可。

### 官方与社区资源

* **官方 Actions 市场**：

  * 地址：`https://github.com/actions`
  * 提供 70+ 官方 Action（例如 `checkout` 用于代码检出）
* **社区 Marketplace**：

  * 地址：`https://github.com/marketplace`
  * 可搜索社区编写的各种 Action（如打包工具、部署工具等）

---

## 四、引用他人编写的 Action

### 基本格式

```yaml
uses: 作者名/Action名@版本号
```

* **uses**：表示使用其他人编写的 Action
* **版本号**：对应 Git 仓库中的 tag
* **示例**：

```yaml
uses: actions/checkout@v3
```

或：

```yaml
uses: pyinstaller/pyinstaller-action@v1.6.1
```

> 版本号 `v1.6.1` 实际上就是仓库中的 Git Tag。

---

## 五、GitHub Actions 核心术语与层级结构

| 概念           | 含义    | 特点                                                |
| ------------ | ----- | ------------------------------------------------- |
| **Workflow** | 工作流程  | 存放在 `.github/workflows/` 目录下的 `.yml` 文件；定义整个自动化任务 |
| **Job**      | 任务    | 一个 Workflow 中可包含多个 Job；**并行执行**；各自运行在独立的虚拟环境      |
| **Step**     | 步骤    | 每个 Job 由多个 Step 组成；**顺序执行**，共享同一虚拟环境              |
| **Event**    | 事件触发器 | 定义 Workflow 何时运行（如 push、pull_request、定时执行等）       |

### 层级关系

```
Workflow
 ├─ Job 1
 │   ├─ Step 1
 │   ├─ Step 2
 └─ Job 2
     ├─ Step 1
     ├─ Step 2
```

---

## 六、Event（事件触发器）

常见事件包括：

* `push`：代码推送
* `pull_request`：提交 PR
* `create`：创建分支或 Tag
* `schedule`：定时任务
* 其他 GitHub 内置事件（如 issue、release 等）

---

## 七、Workflow 文件结构示例

```yaml
name: Python Application

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.12

      - name: Install dependencies
        run: |
          pip install flake8 pytest
          pip install -r requirements.txt

      - name: Lint with flake8
        run: flake8 .

      - name: Test with pytest
        run: pytest
```

---

## 八、Job 与 Step 的执行机制

* **Job**

  * 默认 **并行执行**
  * 每个 Job 运行在独立的虚拟机（Ubuntu、Windows、macOS）
  * Job 之间互不干扰

* **Step**

  * 在同一虚拟环境中 **按顺序执行**
  * 上一步的结果可影响下一步

---

## 九、多 Job 示例

示例：在同一 Workflow 中添加第二个 Job（打包为可执行文件）

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: 3.12
      - run: pip install -r requirements.txt

  package:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - name: Package app
        uses: pyinstaller/pyinstaller-action@v1.6.1
        with:
          python-version: 3.12
          spec: main.py
          options: --onefile
```

> 上述 `build` 与 `package` Job 并行执行。

---

## 十、执行与结果查看

* 每次提交到触发分支（如 `main`）时，GitHub 会自动运行对应 Workflow。
* 在仓库的 **Actions** 选项卡中可以查看执行状态与日志。
* **黄色圆圈** 表示执行中，**绿色对勾** 表示成功。
* **Artifacts**：表示执行过程中生成的产物（如打包的可执行文件）。

---

## 十一、GitHub Actions 的收费机制

| 类型                     | 免费额度         | 限制          |
| ---------------------- | ------------ | ----------- |
| **公共仓库（Public Repo）**  | 永久免费         | 无执行时间限制     |
| **私有仓库（Private Repo）** | 每月 2000 分钟免费 | 存储上限 500 MB |

查看方式：
进入 **Settings → Billing and Plans → Usage this month** 查看：

* Actions 使用时长
* Packages 用量
* Storage 用量

---

## 十二、总结

* **GitHub Actions** 是一个基于事件触发的自动化平台。
* **核心思想**：通过配置 `.yml` 文件，让 GitHub 自动执行 CI/CD 流程。
* **三层结构**：Workflow → Job → Step
* **灵活性**：

  * 支持跨平台运行（Linux、Windows、macOS）
  * 支持并行与顺序执行
  * 可引用社区 Action，快速搭建自动化流程
* **性价比高**：公共仓库完全免费，可用于构建、测试、打包、部署、发布等多种自动化任务。

---



# 替换对方仓库里的 `zh` 文件

## 目标

把你本地准备好的 `zh` 文件夹替换对方仓库里的 `zh` 文件夹，并通过 Pull Request 合并到对方仓库，无论网络是否能直接 clone。

---

## 方法一：网络正常，可直接 clone

### 1️⃣ 在 GitHub 上 Fork 对方仓库

1. 打开原仓库页面，例如：`https://github.com/opendatalab/MinerU`
2. 点击 **Fork**，将仓库 Fork 到自己的 GitHub 账号下

---

### 2️⃣ Clone 你 Fork 的仓库到本地

```bash
git clone https://github.com/<你的用户名>/MinerU.git
cd MinerU
```

> 进入仓库目录，准备操作

---

### 3️⃣ 添加上游仓库（upstream）

```bash
git remote add upstream https://github.com/opendatalab/MinerU.git
```

> `upstream` 指向原仓库，用于同步最新内容

查看远程仓库：

```bash
git remote -v
```

---

### 4️⃣ 同步上游仓库

```bash
git fetch upstream
# 这个命令会把原始仓库的所有新内容（新的提交、分支等）下载到你的本地 Git 数据库中，但不会自动合并或修改你当前工作区的文件。它只是让你知道上游仓库有哪些更新。

git checkout main
# 切换你的工作目录和 HEAD 指针到本地的 main 分支上。要求你在进行任何新工作前，先确保本地的主分支（main）已经和上游仓库的主分支（upstream/main）对齐。当执行 git checkout main 时，如果本地或远程仓库中不存在名为 main 的分支，执行该命令会失败并报错

git merge upstream/main
# 将上游仓库的最新内容（你通过 git fetch upstream 下载的）合并到你当前的本地分支。作用是更新你本地的 main 分支的代码和历史，使其与上游仓库的最新状态保持同步。

```

### 为什么不直接 `git pull upstream main`?

命令 `git pull upstream main` 默认等同于 `git fetch upstream` 接着 `git merge upstream/main`。看起来是更简洁的，但在这个特定的开源同步流程中，**手动拆分成两步更优越**：

#### 1. 可控性 (Control)

* **`git fetch upstream`** 只是下载数据，但不会改变你当前分支或工作区。它允许你在本地数据库中**检查**原始仓库 (`upstream`) 有哪些变化（例如，通过 `git log HEAD..upstream/main`），然后再决定是否合并。
* **`git pull`** 默认是自动执行 `merge` 的，一旦执行，你本地的 `main` 分支就立即被更新了。如果远程分支上有一些意外的、你不想立即合并的修改，你没有机会暂停和检查。

#### 2. 避免意外创建合并提交 (Avoiding Unnecessary Merge Commits)

当你在本地 `main` 分支上工作时，你通常希望它是一个**线性的历史**，完美地反映原始仓库的历史。

* **`git pull`** 默认是 `fetch` + `merge`。如果你的本地 `main` 分支已经有了一些提交（哪怕是你忘了删除的临时提交），`git pull` 会尝试将你的本地提交和远程 `upstream/main` 的提交进行三方合并，**产生一个额外的合并提交 (Merge Commit)**。
* **理想状态**下，`main` 分支应该只包含来自 `upstream` 的提交。额外的合并提交会使得你的 `main` 历史变得不干净。

### 总结

虽然 `git pull upstream main` 在功能上是等价的，但分解操作（`fetch` 然后 `checkout` 再 `merge`）是 **“谨慎且专业的”** 工作流：

| 分解操作 (`fetch` + `merge`) | `git pull` (一键操作) |
| :--- | :--- |
| **可控**：有机会在合并前检查 `upstream/main`。 | **自动**：立即执行合并，没有中间检查步骤。 |
| **清晰**：明确操作的目标和来源。 | **可能产生**：在某些情况下，会在本地 `main` 上产生不必要的合并提交。 |

因此，手动执行 `git fetch upstream` 后，确保在正确的本地基准分支（`main`）上执行 `git merge upstream/main`，是保持本地代码库与上游仓库**干净同步**的最佳实践。


> 如果原仓库主分支是 `master`，请把 `main` 改为 `master`

> **❗️提示**：我 clone 的是 fork 的 origin 仓库，那么与此同时，原始的 upstream 仓库，可能又有更新了，所以我要从 upstream 上 fetch，然后在 checkout，并 merege upstream/main。
---

### 5️⃣ 创建新分支

```bash
git checkout -b update-zh
#  Git 会以你当前所在的分支（在这个流程中，是你刚刚同步到最新状态的 main 分支）的 HEAD 指针（也就是最新的那次提交）作为起点，来创建新的 update-zh 分支。继承历史： 这意味着 update-zh 分支的历史记录，与 main 分支的历史记录是完全相同的。它拥有 main 分支上所有的提交记录。继承内容： 你的工作目录中的所有文件内容，在 update-zh 分支创建时，也完全是 main 分支当时的最新状态。
```

> 新分支操作更安全，不会影响 `main` 分支git

---

### 6️⃣ 替换 `zh` 文件夹

1. 将本地准备好的 `zh` 文件夹复制到仓库目录下
2. 覆盖原来的 `zh` 文件夹
3. 检查替换：

```bash
ls zh
```

---

### 7️⃣ 添加修改到 Git 暂存区

```bash
git add zh
```

---

### 8️⃣ 提交修改

```bash
git commit -m "替换 zh 文件夹内容"
```

---

### 9️⃣ 推送分支到你 Fork 的远程仓库

```bash
git push -u origin update-zh
```

---

### 1️⃣0️⃣ 创建 Pull Request

1. 打开你 Fork 的仓库页面
2. 点击 **Compare & pull request**
3. 填写：

   * **Title**：替换 zh 文件夹内容
   * **Description**：本次 PR 替换了 zh 文件夹内容，内容已更新为最新翻译/文档。请审核合并。
4. Base repository：原仓库 `opendatalab/MinerU`
5. Base branch：原仓库 `main` 或 `master`
6. 点击 **Create pull request**

---

### 1️⃣1️⃣ 等待合并

* 审核通过后，`zh` 文件夹更新到原仓库
* 对方提出修改意见时，可继续在同一分支修改，`add → commit → push`，PR 自动更新

## 方法二（改进版）：下载 ZIP + 强制同步远程分支

  * **适用场景：** 网络不好无法 `git clone`，需要从 ZIP 开始，但又想让本地 Git 仓库具备远程分支的历史记录和引用。
  * **前提：** 你已在 GitHub 上 Fork 了原仓库 (`opendatalab/MinerU`)。

### 1️⃣ 准备工作：下载 & 初始化

1.  打开原仓库页面，点击 **Code → Download ZIP**，解压到 `MinerU` 目录。
2.  进入目录并初始化本地 Git 仓库：

<!-- end list -->

```bash
cd MinerU
git init
```

### 2️⃣ 配置远程仓库

  * 将你的 Fork 仓库 (`nanhongchuan/MinerU`) 设置为 `origin`。
  * 将原仓库 (`opendatalab/MinerU`) 设置为 `upstream`。

<!-- end list -->

```bash
git remote add upstream https://github.com/opendatalab/MinerU.git
git remote add origin https://github.com/nanhongchuan/MinerU.git
```

### 3️⃣ 强制同步远程分支内容 (✅ 关键步骤)

  * **目的：** 获取 `origin` 仓库的完整历史记录和分支结构，并用它覆盖本地当前的主分支（`master` 或 `main`）。

<!-- end list -->

```bash
# 1. 获取远程仓库（origin）的所有分支和历史记录的引用
git fetch origin

# 2. 强制将本地的主分支（master）指向远程 origin/master 的状态
#    这会丢弃 ZIP 带来的初始内容，用远程分支的历史记录和文件内容替换
git reset --hard origin/master

# 检查当前状态，应显示在 master 分支上
git status
```

### 4️⃣ 创建新的工作分支

  * **目的：** 基于刚刚同步好的 `master` 分支，创建一个新的分支来工作。

<!-- end list -->

```bash
git checkout -b update-zh
```

### 5️⃣ 进行修改、提交

1.  将本地准备好的最新 `zh` 文件夹内容**覆盖**到仓库目录中。

<!-- end list -->

```bash
# 1. 添加所有修改
git add .

# 2. 提交修改
git commit -m "feat: 更新 zh 文件夹内容到最新文档"
```

### 6️⃣ 推送到 Fork 远程仓库

  * **目的**：将本地的新分支 `update-zh` 推送到你的远程 Fork 仓库 `origin` 上。

<!-- end list -->

```bash
# -u 选项设置了上游跟踪，update-zh是本地仓库的名字，如果远端没有会自动创建
git push -u origin update-zh
```

> **解释：上游仓库没变，`push -u` 只是设置了**（你本地）**目前分支的 上游跟踪分支（或称上游引用）。**

1.  **全局上游仓库（Upstream Remote）没变：**
    * 原始仓库 **`upstream`** (`https://github.com/opendatalab/MinerU.git`) **永远是上游仓库**，与 `-u` 命令无关。

2.  **`push -u` 的作用范围：**
    * `-u` 作用于 **本地分支**（`update-zh`）和 **你的远程仓库**（`origin`）之间。
    * 它设置的是本地分支 `update-zh` 的 **默认拉取/推送目标**，即 `origin/update-zh`。

这个默认目标被称为 **"upstream"** 或 **"tracking branch"**（上游跟踪分支），但这个 **"upstream"** 仅在 **本地分支配置的上下文** 中使用，与全局的 `upstream` 远程仓库名是两个概念。

**简而言之：** `-u` 只是帮你配置了一个**默认同步对象**，让你在使用 `git push` 或 `git pull` 时更省事。

---

> **查看命令**

可以使用 `git status` 或 `git branch -vv` 命令来查看当前或所有分支的跟踪关系。

`git branch -vv`这个命令会列出所有本地分支，以及它们各自跟踪的远程分支和它们的同步状态：

```bash
git branch -vv
```

**输出示例：**

```
  main           cbf8e07 [origin/main] Initial commit
* update-zh      0397969 [origin/update-zh] update
  feature-branch a1b2c3d [upstream/master: ahead 2] Commit on feature branch
```

在上面的示例中：

  * `update-zh` 正在跟踪 `[origin/update-zh]`。
  * `feature-branch` 正在跟踪 `[upstream/master]`。

---

### 7️⃣ 创建 Pull Request (PR)

1.  打开你的 Fork 仓库页面 (`https://github.com/nanhongchuan/MinerU`)。
2.  点击 **"Compare & pull request"** 提示或导航到 PR 页面。
3.  确保 PR 是从 **`nanhongchuan/MinerU:update-zh`** 提向 **`opendatalab/MinerU:master` (或`main`)**。
4.  填写标题和描述，点击创建 PR。

-----

### ⚠️ 关于 `git fetch origin` & `git reset --hard origin/master`

这个组合在这里能跑通，是因为：

1.  **`git fetch origin`** 成功下载了 `origin` 仓库（你的 Fork）的所有历史记录和分支引用（例如 `origin/master`），但**没有**改变你的工作区。
2.  **`git reset --hard origin/master`** 强制将你当前分支（通常是 ZIP 解压后首次 `init` 后的 **`master`** 或 **`main`**）**重置**到 `origin/master` 这个远程引用所指向的最新提交。这同时会更新你的工作区文件，使它们与远程分支完全一致。

通过这一步骤，你成功地将一个从 ZIP 开始的本地仓库，变成了一个**仿佛是 `git clone` 出来的**、拥有完整历史记录和正确分支引用（`origin/master`）的本地仓库。