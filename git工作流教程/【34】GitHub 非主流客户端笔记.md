# GitHub 非主流客户端笔记

## 一、概述
本节课介绍了 **GitHub 的两种非主流客户端**：
1. **GitHub CLI（Command Line Interface）**
2. **GitHub 手机 App**

---

## 二、GitHub CLI（命令行客户端）

### 1. 基本概念
- CLI 全称：**Command Line Interface**
- 功能：在命令行中执行 GitHub 的操作（无需网页或 GitHub Desktop）
- 适用场景：Linux 用户或无图形界面的系统
- 作用：可在命令行中完成几乎所有 GitHub 网页端操作

---

### 2. 安装方法

**官方网站**：[https://cli.github.com](https://cli.github.com)

#### 各系统安装方式
- **MacOS**：使用 `brew install gh`
- **Linux**：提供 `.deb` 或 `.rpm` 安装包
- **Windows**：下载可执行安装包直接安装

安装验证：
```bash
gh
````

若显示命令帮助，即表示安装成功。

---

### 3. 登录 GitHub CLI

执行命令：

```bash
gh auth login
```

登录流程：

1. 选择登录方式：`GitHub.com`
2. 选择克隆方式：`HTTPS`
3. 是否将认证链接至 Git：输入 `y`
4. 登录方式：选择 “通过浏览器登录”
5. 复制 CLI 提供的验证码 → 浏览器打开登录页 → 粘贴验证码
6. 点击 **Authorize** 授权
   登录成功后显示：

```
logged in as <username>
```

---

### 4. 使用 CLI 创建仓库

命令：

```bash
gh repo create
```

操作流程：

1. 选择创建方式：

   * 在 GitHub 网站上创建 
   * 使用模板创建
   * 推送本地仓库
2. 输入仓库名称（如 `cli-test`）
3. 选择 **Owner**（自己或组织）
4. 填写仓库描述
5. 设置可见性（public/private）
6. 是否添加：

   * README → `yes`
   * .gitignore → `no`
   * license → `yes`（如 Apache 协议）
7. 最后确认 → 输入 `y`
8. 是否克隆到本地 → 输入 `yes`

成功后：

* 仓库自动在本地克隆
* 可直接在网页查看新建仓库

---

### 5. CLI 常用命令示例

#### （1）创建 Issue

 以 Windows 系统为例

* ** cli参考文档**：https://cli.github.com/manual/

1. 搜索命令：

   ```
   gh issue create
   ```
2. 执行命令并填写：

   * issue 标题
   * issue 内容
   * 提交方式（submit）
3. 创建完成后可通过链接查看

#### （2）创建分支与提交

```bash
git checkout -b feature        # 创建分支
git push -u origin feature     # 推送到远端
echo "test" > test.py          # 创建文件
git add . && git commit -m "add test"
git push origin feature
```

#### （3）创建 Pull Request

```bash
gh pr create
```

依次填写：

* PR 标题
* PR 内容
  提交后自动生成 PR，可在网页中查看。

---

### 6. CLI 文档与功能扩展

* CLI 提供详细官方文档：[https://cli.github.com/manual](https://cli.github.com/manual)
* 文档中可通过搜索（Ctrl + F）查找所有命令（如 `issue`, `repo`, `pr` 等）
* 可执行的操作包括：

  * 管理仓库
  * 创建/关闭 issue
  * 发起/合并 PR
  * 管理 release 等等

---

## 三、GitHub 手机 App

### 1. 获取方式

* 国内应用商店无法直接下载
* 需通过 **Google Play** 安装：

  1. 安装 Google Play
  2. 确保网络可访问 Google
  3. 搜索 “GitHub” 并下载官方 App

---

### 2. 登录步骤

1. 打开 App → 点击“使用 GitHub 登录”
2. 输入用户名和密码
3. 完成双重身份验证
4. 点击 **授权（Authorize）**
5. 登录成功后进入主界面

---

### 3. 手机 App 功能介绍

#### 首页布局

* 显示待处理事项：

  * **Issues**
  * **Pull Requests**
* 可直接查看、评论、审核代码

#### PR 审核功能

* 在手机端可直接查看代码差异
* 支持发表评论或选择“通过/不通过”审核

#### 搜索功能

* 支持搜索：

  * 仓库（Repositories）
  * 代码（Code）
* 搜索结果与网页版一致
  例如搜索 “tts”，会显示热门 TTS 仓库

#### 探索（Explore）页面

* 显示 GitHub 热门仓库和动态
* 查看自己或关注仓库的活动

#### 通知（Inbox）

* 显示与网页版相同的 GitHub 通知
* 包含仓库事件、评论、PR 等信息

---

## 四、总结

| 客户端               | 平台  | 特点                     | 适用场景        |
| ----------------- | --- | ---------------------- | ----------- |
| **GitHub CLI**    | 命令行 | 无需图形界面，可执行所有 GitHub 操作 | Linux/服务器环境 |
| **GitHub 手机 App** | 移动端 | 随时管理 Issues、PR、通知      | 移动办公、代码审核   |

CLI + App 的组合能让用户在任意环境下完成完整的 GitHub 操作流程。
