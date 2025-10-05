# 如何终端里查看当前 Git 配置使用的 **GitHub 账号信息**

| 目标          | 命令                                     | 说明                 |
| ----------- | -------------------------------------- | ------------------ |
| 查看全局用户名     | `git config --global user.name`        | Git 提交者名称          |
| 查看全局邮箱      | `git config --global user.email`       | Git 提交者邮箱          |
| 查看当前仓库配置   | `git config --list`                    | 所有配置               |
| **查看远程仓库地址**   | `git remote -v`                        | 可识别 GitHub 用户名     |
| 查看 SSH 公钥   | `cat ~/.ssh/id_rsa.pub`                | 验证与 GitHub 绑定的 key |
| 查看 HTTPS 凭证 | `git credential-osxkeychain get`（mac）等 | 查系统保存的登录信息         |

## 🧩 一、查看 Git 配置的用户名和邮箱

这是 **Git 本地配置的身份信息**（提交 commit 时使用，不一定等同于 GitHub 登录账号）。

```bash
# 查看全局配置（适用于所有仓库）
git config --global user.name
git config --global user.email

# 查看当前仓库配置（仅当前项目有效）
git config user.name
git config user.email

# 一次性查看所有配置项（方便排查）
git config --list
```

> 📘 输出示例：
>
> ```
> user.name=Liqun
> user.email=liqun@example.com
> ```

---

## 🧭 二、查看 GitHub 认证方式（SSH 或 HTTPS）

### 🧱 1. 如果你使用 SSH 方式（通常看远程地址以 `git@github.com:` 开头）

查看 SSH 公钥对应的 GitHub 账号：

```bash
# 查看当前远程仓库地址
git remote -v
```

示例输出：

```
origin  git@github.com:LiqunLab/demo.git (fetch)
origin  git@github.com:LiqunLab/demo.git (push)
```

可以看到用户名是 `LiqunLab`（即 GitHub 账号名）。

进一步查看系统上保存的 SSH Key：

```bash
cat ~/.ssh/id_rsa.pub
```

然后你可以复制这串公钥，到你的 GitHub 个人主页：

> **GitHub → Settings → SSH and GPG keys**
> 确认这把 key 是否存在。

---

### 🧱 2. 如果你使用 HTTPS 方式（看远程地址以 `https://github.com/...` 开头）

同样先查看远程：

```bash
git remote -v
```

示例输出：

```
origin  https://github.com/LiqunLab/demo.git (fetch)
origin  https://github.com/LiqunLab/demo.git (push)
```

如果你使用了 HTTPS + 个人访问令牌（PAT）登录，系统可能缓存了凭证。
你可以查看系统凭证管理器（取决于操作系统）：

* **macOS**：

  ```
  git credential-osxkeychain get
  ```

  （会提示输入 `protocol=https`、`host=github.com`）

* **Windows**：
  打开 “凭据管理器（Credential Manager） → Windows 凭据 → github.com”

* **Linux**（如果配置了凭证缓存）：

  ```
  git config --list | grep credential
  ```

---

## ⚙️ 三、查看远程仓库配置（确认 GitHub 绑定账户）

```bash
git remote -v
```

这条命令能直接看到仓库对应的 GitHub 用户名。例如：

```
origin  git@github.com:LiqunLab/myproject.git (fetch)
```

这里的 `LiqunLab` 就是你当前仓库连接的 GitHub 账户。

---

# 🧭 Git 配置的三层结构（核心概念）

Git 的配置（config）一共有 **三个层级**：

| 层级              | 配置范围            | 说明        |
| --------------- | --------------- | --------- |
| **系统级（system）** | 影响整台电脑上所有用户     | 很少改       |
| **全局级（global）** | 影响当前系统登录用户的所有仓库 | 常用于设置个人信息 |
| **仓库级（local）**  | 仅影响当前项目（仓库）     | 项目专属配置    |

Git 会按以下优先级读取配置：

> **local（当前仓库） > global（全局） > system（系统）**

也就是说：
👉 **同一个配置项如果在多个层级都存在，Git 会采用优先级最高的那个。**

---

# 🧩 举个直观例子

假设你的电脑上有两个 Git 仓库：

* A 项目（工作项目）
* B 项目（开源项目）

你在全局设置了：

```bash
git config --global user.name "Alice Zhang"
git config --global user.email "alice@company.com"
```

这表示：

> 在任何新仓库里提交代码时，Git 默认用这套身份（除非你覆盖它）。

---

## 📁 然后你进入 B 项目，想用另一个身份（比如开源账号）

你可以在 **当前仓库（B项目）** 里单独配置：

```bash
git config user.name "AliceOpen"
git config user.email "alice.open@gmail.com"
```

这样：

* 在 **B 项目** 提交时，使用 `AliceOpen` 这个身份；
* 但在 **A 项目** 或别的仓库中，仍然使用全局配置的公司邮箱。

---
