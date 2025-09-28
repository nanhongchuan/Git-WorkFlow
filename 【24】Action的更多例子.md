# GitHub Actions 实践笔记（第24课：Action 的更多例子）

> 本节重点讲解 GitHub Actions 的更多实用玩法，包括跨平台打包、定时推送、签到自动化等。  
> 通过三个完整示例掌握 Action 的配置方法、触发机制与 Secrets 环境变量使用。

---

## 一、GitHub Actions 的多样用途

- 可用于执行定时小任务，如：
  - 天气推送
  - 自动签到
  - 自动打包与发布
- 无需服务器、无需额外费用即可实现自动化。
- 所有任务均通过 `.github/workflows/*.yml` 定义。

---

## 二、样例一：跨平台打包程序

### 🎯 目标
自动将 Python 程序打包为不同操作系统的可执行文件（Windows / Ubuntu / macOS）。

### ⚙️ 主要步骤
1. **Fork 示例仓库**  
   将示例仓库保存到自己账号下。

2. **进入 Actions → 选择对应脚本**  
   以 `love_heart_windows.yml` 为例。

3. **手动触发执行**
   - 点击 “Run workflow”
   - 查看执行日志和状态灯（绿色表示成功）
   - 构建结果保存在 `Artifacts` 中，可下载查看。

### ⚙️ 关键配置讲解
```yaml
name: love heart windows

on:
  workflow_dispatch  # 手动触发，可改为 schedule 定时触发

jobs:
  build:
    runs-on: windows-latest  # 可改为 ubuntu-latest 或 macos-latest
    steps:
      - name: 打包 Python 程序
        uses: Nuitka/compile-action@v1
        with:
          python-version: '3.12'
          script-name: love_heart.py
          onefile: true       # 打包为单文件
          windowed: true      # 以窗口模式运行
````

### 💡 跨平台差异

* **唯一差别**：`runs-on` 参数（指定虚拟机操作系统）
* GitHub 会自动分配对应系统的虚拟环境执行。

### 🧪 测试验证

1. 在 Ubuntu 虚拟机中下载生成文件。
2. 修改执行权限：

   ```bash
   chmod +x love_heart
   ./love_heart
   ```
3. 程序成功运行，证明打包可行。

---

## 三、样例二：微信天气定时推送

### 🎯 目标

利用 GitHub Actions 实现每日早晨自动发送天气信息到微信（基于测试号）。

### ⚙️ 所需准备

* 注册一个 **微信测试号**
* 获取以下信息并配置为 GitHub Secrets：

  * `APP_ID`
  * `APP_SECRET`
  * `OPEN_ID`
  * `TEMPLATE_ID`

### ⚙️ 环境变量配置

路径：**Settings → Secrets and variables → Actions**

```bash
APP_ID
APP_SECRET
OPEN_ID
TEMPLATE_ID
```

### ⚙️ Workflow 样例

```yaml
name: weather report

on:
  schedule:
    - cron: '0 23 * * *'  # 每天 UTC 23 点 = 北京时间早 7 点
  workflow_dispatch:       # 支持手动触发

jobs:
  weather_push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: 安装依赖
        run: |
          pip install -r requirements.txt
      - name: 执行天气推送
        env:
          APP_ID: ${{ secrets.APP_ID }}
          APP_SECRET: ${{ secrets.APP_SECRET }}
          OPEN_ID: ${{ secrets.OPEN_ID }}
          TEMPLATE_ID: ${{ secrets.TEMPLATE_ID }}
        run: python weather_report.py
```

### 📦 Python 代码中获取环境变量

```python
import os

app_id = os.environ.get("APP_ID")
app_secret = os.environ.get("APP_SECRET")
```

### 🧾 执行方式

* 手动执行：在 Actions 中点击 **Run workflow**
* 定时执行：每天早晨 7 点自动推送天气消息。

---

## 四、样例三：京东自动签到（薅羊毛任务）

### 🎯 目标

使用 GitHub Actions 定时执行 Python 脚本，自动登录京东账号签到，获取京豆奖励。

### ⚙️ 核心流程

1. 获取京东 Cookie。
2. 将 Cookie 存入 GitHub Secrets。
3. 编写 Python 签到脚本。
4. 设置每日定时任务执行。

### 🍪 获取 Cookie 步骤

1. 打开 [京东官网](https://www.jd.com)。
2. 按 **F12** 打开开发者工具 → 切换到 **仿真移动设备模式**。
3. 刷新页面 → 打开 Network → 找到 `jd.com` 请求。
4. 查看 **Headers（标头）** → 复制 Cookie 字符串。
5. 进入 GitHub 仓库 →
   **Settings → Secrets → Actions → New repository secret**

   ```bash
   Name: JD_COOKIE
   Value: <复制的 Cookie 内容>
   ```

### ⚙️ Workflow 样例

```yaml
name: jd sign

on:
  schedule:
    - cron: '0 0 * * *'  # 每天 UTC 0 点（北京时间 8 点）

jobs:
  sign:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: pip install -r requirements.txt
      - name: 执行京东签到脚本
        env:
          JD_COOKIE: ${{ secrets.JD_COOKIE }}
        run: python jd_sign.py
```

---

## 五、GitHub Actions Marketplace（插件市场）

### 💡 概念

* Marketplace 是 GitHub 官方的 Action 脚本市场。
* 可直接复用他人编写的 Actions，无需从零配置。

### 🧰 常用插件示例

| 插件名称                          | 功能                |
| ----------------------------- | ----------------- |
| `Nuitka/compile-action`       | 自动打包 Python 可执行文件 |
| `actions/checkout`            | 拉取项目代码            |
| `actions/setup-python`        | 设置 Python 版本      |
| `softprops/action-gh-release` | 自动创建 Release      |
| `docker/build-push-action`    | 构建并推送 Docker 镜像   |
| `easingthemes/ssh-deploy`     | 自动部署到远程服务器        |

### 🧭 使用方式

1. 打开 [GitHub Marketplace → Actions](https://github.com/marketplace?type=actions)
2. 搜索目标 Action。
3. 点击查看使用示例。
4. 复制配置片段到自己的 workflow 文件中。

---

## 六、本节核心要点总结

| 模块                 | 知识点                            | 说明                            |
| ------------------ | ------------------------------ | ----------------------------- |
| **Action 基础**      | workflow / job / step / runner | Action 的基本组成单元                |
| **触发机制**           | workflow_dispatch / schedule   | 手动执行与定时任务                     |
| **环境变量**           | secrets 配置                     | 隐私信息安全存储与引用                   |
| **跨平台打包**          | runs-on 参数控制系统类型               | Windows / Ubuntu / macOS 构建差异 |
| **自动推送**           | cron 表达式                       | UTC 与北京时间换算                   |
| **Cookie 自动化**     | secrets 存放敏感信息                 | 避免明文暴露账号                      |
| **Marketplace 应用** | 直接复用社区脚本                       | 提高自动化效率                       |

---

## 七、学习建议

* 掌握 GitHub Actions 的触发语法与 YAML 结构。
* 学会通过 **Secrets** 管理敏感信息。
* 理解 `cron` 时间表达式（UTC 与本地时差）。
* 善用 **Marketplace** 复用成熟自动化脚本。
* 实践定时任务、签到、推送类项目，理解 Actions 的灵活性。

---

```
```
