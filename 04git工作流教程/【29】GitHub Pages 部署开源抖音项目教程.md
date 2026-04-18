# GitHub Pages 部署开源抖音项目教程

## 一、项目简介

* 本项目是基于 GitHub Pages 部署的 **开源“抖音”仿站**。
* 网站会轮播视频内容，可自由替换成自己的视频。
* 使用 **GitHub 免费服务** 完成托管和自动部署。
* 项目开源，可根据个人需求自由修改。

---

## 二、技术栈介绍

| 技术                 | 说明                       |
| ------------------ | ------------------------ |
| **Vue.js (Vivo)**  | 前端渐进式框架，支持组件化和响应式渲染      |
| **Vite 5**         | 新一代前端构建工具，编译速度快          |
| **Pinia**          | Vue 的状态管理库，用于全局状态管理      |
| **GitHub Pages**   | 免费的静态网站托管服务              |
| **GitHub Actions** | 持续集成（CI/CD）工具，用于自动化构建和部署 |

> ✅ 优点：全程免费、无需服务器、全自动部署上线。

---

## 三、GitHub Pages 发布原理

* 将 HTML、CSS、JS 静态资源托管在 GitHub 仓库中。
* 每次提交后，GitHub Actions 自动执行构建并发布网站。
* 最终网站可通过 `https://用户名.github.io` 或自定义域名访问。

---

## 四、部署流程

### 1. Fork 开源项目

1. 登录 GitHub。
2. 打开开源抖音项目主页。
3. 点击 **Fork**（将项目复制到自己的账号下）。
4. 仓库命名建议：

   ```
   英文名.github.io
   ```

   例如：`techshrimp.github.io`

---

### 2. 启用 GitHub Actions

1. 打开仓库 → **Settings → Pages**

   * 选择来源：**GitHub Actions**
2. 打开顶部 **Actions** 标签页。
3. 启动 **Action 功能** → 选择 `Deploy on GitHub Pages` 工作流。
4. 点击 **Run workflow** 手动触发部署。

---

### 3. Actions 工作流解析

GitHub Actions 自动执行以下步骤：

| 步骤 | 内容                                 |
| -- | ---------------------------------- |
| 1  | 检出仓库代码                             |
| 2  | 安装 pnpm                            |
| 3  | 设置 Node.js 环境（版本 18）               |
| 4  | 执行 `pnpm install` 安装依赖             |
| 5  | 执行 `pnpm build` 进行打包               |
| 6  | 将编译后的静态文件（dist 目录）上传到 GitHub Pages |
| 7  | 发布网站到 `https://用户名.github.io`      |

> 💡 构建完成后，Actions 状态出现 ✅ 即代表部署成功。

---

## 五、网站个性化修改

### 1. 替换视频内容

1. 打开项目目录：

   ```
   src/assets/data/posts.json
   ```
2. 文件内保存视频数据（如 ID、封面、URL 等）。
3. 若想替换为自己的视频：

   * 打开浏览器开发者工具 (F12)。
   * 访问抖音页面，在 Network → Filter 中搜索 `post`。
   * 找到接口返回的 JSON 数据，复制响应内容。
   * 清理多余字段，使其结构与 `posts.json` 相同。
   * 使用 VSCode 全局替换工具 `Ctrl+H` 修改字段名。
   * 删除防盗链字段，仅保留可直接播放的 URL。
   * 替换原文件内容后 **Commit changes**。

> 每次提交后，GitHub Actions 会自动重新部署更新内容。

---

## 六、自定义域名绑定

### 1. 购买域名

* 可在任意域名服务商购买（如腾讯云、Cloudflare 等）。

### 2. Cloudflare 配置步骤

1. 登录 Cloudflare → 选择你的域名。
2. 打开 **DNS 记录**。
3. 添加记录：

| 类型    | 名称        | 目标值               |
| ----- | --------- | ----------------- |
| CNAME | 抖音（或子域名名） | `<用户名>.github.io` |

⚠️ 注意：

* 将 `<用户名>` 替换为你的 GitHub 英文用户名。
* 不要勾选 “Enforce HTTPS”。

### 3. GitHub Pages 设置

1. 返回仓库 → **Settings → Pages**。
2. 在 **Custom domain** 中填写你的域名。
3. 等待验证出现 ✅ 表示成功。

---

## 七、常见问题与优化

| 问题     | 解决方案                         |
| ------ | ---------------------------- |
| 页面无法访问 | 检查 CNAME 配置与 GitHub Pages 状态 |
| 视频无法播放 | 保留合法的公开 URL（避免防盗链）           |
| 部署失败   | 检查 Actions 工作流日志             |
| 想要更短网址 | 使用根目录的 `index.html` 作为入口页    |

---

## 八、总结

| 项目    | 内容                 |
| ----- | ------------------ |
| 托管平台  | GitHub Pages       |
| 构建工具  | Vite + pnpm        |
| 前端框架  | Vue.js             |
| 状态管理  | Pinia              |
| 自动化工具 | GitHub Actions     |
| 自定义域名 | 支持，推荐使用 Cloudflare |
| 特点    | 免费部署、支持自定义内容、自动化发布 |

---

