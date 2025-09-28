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



# 本地准备好的 `zh` 文件夹替换对方仓库里的 `zh` 文件

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
git checkout main
git merge upstream/main
```

> 如果原仓库主分支是 `master`，请把 `main` 改为 `master`

---

### 5️⃣ 创建新分支

```bash
git checkout -b update-zh
```

> 新分支操作更安全，不会影响 `main` 分支

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

---

## 方法二：网络不好，只能下载 ZIP + 初始化仓库

### 1️⃣ 下载原仓库源码

1. 打开原仓库页面，例如：`https://github.com/opendatalab/MinerU`
2. 点击 **Code → Download ZIP**
3. 解压到本地，例如 `MinerU`

---

### 2️⃣ 初始化本地 Git 仓库

```bash
cd MinerU
git init
```

---

### 3️⃣ 添加远程仓库

* 添加上游仓库：

```bash
git remote add upstream https://github.com/opendatalab/MinerU.git
```

* 添加自己 Fork 的仓库：

```bash
git remote add origin https://github.com/<你的用户名>/MinerU.git
```

> ⚠️ 关键点：`upstream` 用于同步原仓库，`origin` 用于推送到 Fork 并创建 PR

---

### 4️⃣ 创建新分支

```bash
git checkout -b update-zh
```

---

### 5️⃣ 替换 `zh` 文件夹

1. 将本地准备好的 `zh` 文件夹复制到仓库目录
2. 覆盖原有 `zh` 文件夹
3. 检查替换：

```bash
ls zh
```

---

### 6️⃣ 添加修改到 Git 暂存区

```bash
git add zh
```

---

### 7️⃣ 提交修改

```bash
git commit -m "替换 zh 文件夹内容"
```

---

### 8️⃣ 推送到 Fork 的远程仓库

```bash
git push -u origin update-zh
```

> 这时修改在远程 Fork 仓库的新分支上，GitHub 会识别可创建 PR

---

### 9️⃣ 创建 Pull Request

1. 打开你 Fork 的仓库页面
2. 点击 **Compare & pull request**
3. 填写：

   * **Title**：替换 zh 文件夹内容
   * **Description**：本次 PR 替换了 zh 文件夹内容，内容已更新为最新翻译/文档
4. Base repository：原仓库 `opendatalab/MinerU`
5. Base branch：原仓库 `main` 或 `master`
6. 点击 **Create pull request**

> 如果不想本地操作，也可以直接在 Fork 的网页上传 `zh` 文件夹，创建新分支，再 PR

---

### 1️⃣0️⃣ 等待合并

* 审核通过后，`zh` 文件夹更新到原仓库
* 对方提出修改意见时，可继续在同一分支修改，`add → commit → push`，PR 自动更新

---

## 总结表

| 方法  | 适用情况          | 核心流程                                                                       |
| --- | ------------- | -------------------------------------------------------------------------- |
| 方法一 | 网络正常，可 clone  | Fork → Clone → 添加 upstream → 同步 → 新分支 → 替换 → add → commit → push → PR      |
| 方法二 | 网络不好，无法 clone | 下载 ZIP → init → 添加 upstream & origin → 新分支 → 替换 → add → commit → push → PR |