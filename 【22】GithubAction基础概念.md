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

是否希望我帮你在末尾加一份「GitHub Actions 常用 Action 清单（官方 + 社区推荐）」？这样笔记会更实用。
