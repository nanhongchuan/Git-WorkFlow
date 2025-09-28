# MkDocs 文档站点搭建与自动部署指南（GitHub Pages + Actions）

## 一、前提条件

* 已安装 **Python 3.6+**
* 已配置 **Git** 环境
* `pip3` 可正常使用

检查命令：

```bash
python3 --version
pip3 --version
git --version
```

---

## 二、GitHub 仓库初始化与拉取

1. 登录 [GitHub](https://github.com)，点击右上角 **“+” → New repository**
2. 填写仓库名称（如 `my-docs`），建议设为 **Public（公开）**
3. 创建仓库后，复制仓库地址（HTTPS 或 SSH）
4. 本地克隆仓库：

```bash
git clone <远程仓库地址>
cd my-docs
```

> 后续所有操作都在本地仓库目录下完成。

---

## 三、安装 MkDocs 与主题

1. 安装 MkDocs 与 Material 主题：

```bash
pip install mkdocs mkdocs-material
```

2. 初始化 MkDocs 项目：

```bash
mkdocs new .
```

生成文件结构：

```
mkdocs.yml
docs/
  └── index.md
```

---

## 四、编辑与配置项目

编辑 `mkdocs.yml`：

```yaml
site_name: My Documentation
theme:
  name: material
```

可配置：

* **主题**
* **导航结构**：

```yaml
nav:
  - 首页: index.md
  - 教程: tutorial.md
```

* **站点信息**：

```yaml
site_author: Your Name
site_description: Documentation built with MkDocs
```

* **插件和扩展功能**（可选）

---

## 五、本地预览

启动本地服务：

```bash
mkdocs serve
```

浏览器访问：

```
http://127.0.0.1:8000
```

修改 `docs/` 下 Markdown 文件，页面会自动刷新。

---

## 六、提交与推送代码

1. 添加并提交修改：

```bash
git add .
git commit -m "Initialize MkDocs site"
```

2. 推送到远程仓库：

```bash
git push origin main
```

---

## 七、GitHub 设置（必要步骤）

### 1. Actions 权限

仓库页面 → **Settings → Actions → General**

* 勾选 **Read and write permissions**
* 勾选 **Allow GitHub Actions to create and approve pull requests**

### 2. GitHub Pages

仓库页面 → **Settings → Pages → Source**

* Source 选择 **Deploy from a branch → Branch: gh-pages → Folder: /(root)**
* 点击 **Save**

---

## 八、部署网站（mkdocs gh-deploy）

```bash
mkdocs gh-deploy
# 手动push然后发布
```

### 功能说明

1. **构建静态网站**：Markdown → HTML + CSS + JS
2. **上传到 GitHub Pages**：生成 `gh-pages` 分支并推送
3. **访问网站**：

```
https://<用户名>.github.io/<仓库名>/
```

> ✅ `mkdocs gh-deploy` = 构建 + 上传 + 部署，无需手动操作 Actions。

---

## 九、自动部署 GitHub Actions（可选）

如果希望每次 push 自动部署，可在仓库创建 `.github/workflows/gh-pages.yml`：

```yaml
name: Deploy MkDocs

on:
  push:
    branches:
      - main  # 每次推送 main 分支时触发
  workflow_dispatch: # 可手动触发

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          pip install mkdocs mkdocs-material

      - name: Build and deploy to GitHub Pages
        run: |
          mkdocs gh-deploy --force
```

> 工作原理：
>
> * push 代码到 main 分支 → 自动执行 workflow → 构建静态网站 → 推送到 `gh-pages` → 页面更新。

---

## 🔑 完整流程总结

1. GitHub 创建仓库
2. 本地 `git clone` 拉取
3. 安装 `mkdocs` 与 `mkdocs-material`
4. `mkdocs new .` 初始化项目
5. 编辑 `mkdocs.yml` 配置主题、导航
6. 本地预览 `mkdocs serve`
7. 提交并推送代码
8. GitHub Settings → Actions / Pages 权限设置
9. **手动部署**：`mkdocs gh-deploy`
10. **自动部署（可选）**：配置 GitHub Actions workflow → push 自动部署

---

一个直观流程图，把整个 MkDocs 文档从 Markdown 到 GitHub Pages 的流程可视化。这里用文本方式表示流程：

```
┌───────────────┐
│  本地 Markdown │
│    文件 (.md) │
└───────┬───────┘
        │ mkdocs build / mkdocs gh-deploy
        ▼
┌───────────────┐
│   MkDocs 构建  │
│ HTML + CSS + JS│
└───────┬───────┘
        │ gh-deploy 或 Actions workflow
        ▼
┌───────────────┐
│  GitHub 仓库   │
│  gh-pages 分支 │
└───────┬───────┘
        │ GitHub Pages 服务
        ▼
┌───────────────┐
│ 浏览器访问网站 │
│ https://<用户名>│
│ .github.io/<仓库名>/ │
└───────────────┘
```

---

### 流程说明

1. **本地 Markdown 文件**：你编辑的文档内容。
2. **MkDocs 构建**：将 Markdown 文件转换成 HTML、CSS、JS 静态网页。
3. **部署到 GitHub**：

   * `mkdocs gh-deploy`：本地执行命令直接上传并更新 `gh-pages` 分支
   * **或** GitHub Actions workflow：每次 push 自动触发构建并部署
4. **GitHub Pages**：读取 `gh-pages` 分支生成静态网站。
5. **浏览器访问**：最终用户通过 Pages URL 访问文档网站。

