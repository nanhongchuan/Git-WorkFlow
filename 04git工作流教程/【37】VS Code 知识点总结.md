# 🧠 VS Code 知识点总结

## 一、VS Code 基础概念

* **VS Code 是什么**：微软推出的跨平台、开源、免费的集成开发环境（IDE）。
* **IDE 全称**：Integrated Development Environment（集成开发环境）。
* **核心特性**：

  * 支持多语言编辑与运行（Python、C/C++、JS 等）
  * 丰富的插件生态
  * 集成 SSH工具、     Git、Docker、API 测试、数据库、AI 助手等
  * 可在浏览器中直接使用（网页版 VS Code）

---

## 二、安装与启动

* 官方下载地址：[code.visualstudio.com](https://code.visualstudio.com)
* 蓝色图标 → **VS Code**
* 紫色图标 → **Visual Studio（用于 .NET / C++）**
* 支持 **Windows、macOS、Linux**
* 浏览器版可通过 GitHub 打开项目：
  在 GitHub 项目页按下 **句号（.）键** 即可进入网页版 VS Code

---

## 三、基础使用

* **打开项目**：File → Open Folder
* **新建文件**：点击 “New File” → 输入文件名（如 `demo.py`）
* **语言识别**：自动识别语言并提示安装对应插件
* **执行代码**：

  * 点击右上角运行按钮 ▶️
  * 默认使用 PowerShell 控制台
* **终端管理**：

  * 可添加多种 shell（PowerShell、命令提示符、WSL）
  * 可修改颜色与图标
  * 支持自定义任务（task.json 保存常用命令）

---

## 四、虚拟环境（Python 示例）

* 创建虚拟环境：

  1. 打开命令面板（Ctrl+Shift+P）
  2. 输入 `Python: Create Environment`
  3. 选择 `venv` 或 `Conda`
  4. 选择 Python 版本（如 3.12）
* 创建成功后右下角显示 `.venv` 环境标识
* 优点：项目依赖隔离，不影响全局环境

---

## 五、Git 与 GitHub 集成

* 打开左侧 **Git 图标**
* 初始化仓库：`Initialize Repository`
* 发布到 GitHub：`Publish to GitHub`
* 可选：

  * Private（私有）
  * Public（公开）
* 克隆仓库：`Clone Git Repository` → 输入 URL 或从 GitHub 选择项目
* 本地修改：

  * 写 commit message
  * 点击 **Commit**
  * 点击 **Sync Changes** 推送到远端

### 🔧 Git 插件推荐

#### 1. GitLens

* 显示每行代码的提交人、日期、commit message
* 提供图形化提交记录（Commit Graph）
* 快速查看分支、合并、历史记录

---

## 六、远程开发相关插件

### 1. Remote SSH

* 安装 `Remote - SSH` 插件（微软官方）
* 添加 SSH 链接：`ssh user@ip`
* 自动生成配置文件
* 连接后可直接打开远程服务器目录
* 终端即为远程 Linux 环境，可直接运行代码

### 2. Docker 插件

* 插件名：`Docker`（微软官方）
* 功能：

  * 查看镜像、容器、网络、卷
  * 图形化操作容器
  * 可视化 Docker registry 管理

### 3. WSL 插件

* 插件名：`WSL`（微软官方）
* 用途：与 Windows 下的 Linux 子系统无缝连接
* 使用方式：

  * 在 PowerShell 启动 `wsl`
  * 输入 `code .` 即可在 VS Code 打开该目录
  * 命令行同步显示 Linux 环境

---

## 七、API 调试与开发工具插件

### 1. REST Client（⭐重点推荐）

* 使用文件方式发起请求
* 支持 GET / POST / PUT / DELETE
* 可查看 response、headers、body
* 可导出为 `curl` 命令
* 可直接识别 curl 请求执行
  
### 2. Thunder Client

* 类似 **Postman** 的可视化 API 调试工具
* 在 VS Code 内集成 API 调试界面

### 3. 数据库插件

* MySQL 插件：图形化查看表、列、执行 SQL
* SQLite 插件：可视化操作 SQLite 数据库
* Redis 插件：查看键值与结构

---

## 八、前端开发相关插件

### 通用插件

* **Auto Rename Tag**：自动同步修改成对 HTML 标签
* **Live Server**：实时预览 HTML 页面，代码变动自动刷新
* **CSS Peek**：查看 CSS 定义并快速跳转
* **ESLint / Prettier**：格式化与规范前端代码
* **Console Ninja**：在 VS Code 中直接显示 `console.log` 输出

### 框架专用插件

* **Vue 3 Snippets**：生成 Vue 代码片段
* **Vue Official**：代码补全、语法检查
* **ES7+ React Snippets**：React 代码片段生成与格式检查
* **Java Debugger**：JS/TS 调试断点自动映射到浏览器

---

## 九、辅助开发与效率插件

| 插件名称                          | 功能说明                      |
| ----------------------------- | ------------------------- |
| **Polacode**                  | 一键生成美观的代码截图               |
| **Code Spell Checker**        | 检查代码拼写错误并提示修复             |
| **Markdown Preview Enhanced** | 实时预览 Markdown 文档          |
| **Bookmarks**                 | 给代码加书签，快速定位               |
| **TODO Highlight**            | 高亮显示注释中的 TODO / FIXME 等标识 |

---

## 十、AI 编程插件

| 插件名称                               | 功能说明        |
| ---------------------------------- | ----------- |
| **GitHub Copilot**                 | 智能代码补全与自动生成 |
| **Tabnine**                        | 基于上下文预测补全   |
| **IntelliCode / PHP IntelliSense** | 针对语言优化的智能提示 |
| **Blackbox AI**                    | 代码生成与自动化辅助  |

---

## 十一、总结

VS Code 不仅是轻量级编辑器，更是一个功能完备的多语言开发中心。
通过插件扩展，它可以承担：

* 代码编写与运行
* Git / SSH / Docker 管理
* API 调试与数据库管理
* 前端开发与预览
* Markdown / AI 辅助创作
  几乎覆盖整个软件开发生命周期。

---