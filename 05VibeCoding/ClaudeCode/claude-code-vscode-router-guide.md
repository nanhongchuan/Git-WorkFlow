# Claude Code 在 VS Code 右侧面板接入 claude-code-router（小白版）

这篇教程适合你这种情况：

- 你已经能在终端里用 `claude`
- 终端里的 Claude Code 实际走的是 `claude-code-router`
- router 后面接的是 GLM 或别的第三方模型
- 你现在想把 **VS Code 右侧的 Claude Code 插件面板** 也接到同一套路由上

---

## 目标

做完后，你会得到这个效果：

- 终端里的 `claude` 继续可用
- VS Code 右侧的 Claude Code 面板也可用
- 两边尽量共用同一套配置，不再强制走 Anthropic 官方登录

---

## 先说结论：你只需要做 3 件事

1. 启动 `claude-code-router`
2. 把 router 的地址和 token 写进 `~/.claude/settings.json`
3. 在 VS Code 里打开 **Disable Login Prompt**

照着下面一步一步做就行。

---

## 第 1 步：启动 claude-code-router

打开一个终端，执行：

```bash
ccr start
```

先不要关掉这个终端。

如果你平时本来就已经在跑 `ccr start`，那这一步可以跳过。

你也可以顺手检查一下状态：

```bash
ccr status
```

---

## 第 2 步：取出 router 需要的两个值

再打开一个新终端，执行：

```bash
ccr activate
```

它会打印出一串环境变量。你重点看这两个：

- `ANTHROPIC_BASE_URL`
- `ANTHROPIC_AUTH_TOKEN`

一般会长这样：

```bash
export ANTHROPIC_BASE_URL=http://127.0.0.1:3456
export ANTHROPIC_AUTH_TOKEN=你的token
```

### 你需要记住什么？

- `ANTHROPIC_BASE_URL`：Claude Code 该连到哪里
- `ANTHROPIC_AUTH_TOKEN`：Claude Code 连过去时带什么 token

先把这两个值复制出来，下一步要用。

---

## 第 3 步：创建 Claude Code 的配置文件

在终端执行：

```bash
mkdir -p ~/.claude
open -e ~/.claude/settings.json
```

如果这个文件原来不存在，会自动新建。

然后把下面内容完整粘进去：

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "env": {
    "ANTHROPIC_BASE_URL": "把你刚才看到的 ANTHROPIC_BASE_URL 粘贴到这里",
    "ANTHROPIC_AUTH_TOKEN": "把你刚才看到的 ANTHROPIC_AUTH_TOKEN 粘贴到这里"
  }
}
```

### 示例

如果你刚才看到的是：

```bash
export ANTHROPIC_BASE_URL=http://127.0.0.1:3456
export ANTHROPIC_AUTH_TOKEN=abc123
```

那你的 `~/.claude/settings.json` 应该写成：

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "env": {
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:3456",
    "ANTHROPIC_AUTH_TOKEN": "abc123"
  }
}
```

保存文件。

---

## 第 4 步：在 VS Code 里关闭登录弹窗

打开 VS Code。

然后按：

```text
Cmd + ,
```

在搜索框里输入：

```text
Claude Code login
```

找到这个选项：

```text
Disable Login Prompt
```

把它勾上。

### 这一步的作用

默认情况下，Claude Code 扩展会优先弹出 Anthropic 登录页面。

你现在不是要走官方网页登录，而是要让它走你自己的 router，所以这一步一定要开。

---

## 第 5 步：重载 VS Code

按：

```text
Cmd + Shift + P
```

输入：

```text
Developer: Reload Window
```

回车。

这一步做完，相当于让 VS Code 重新读取扩展配置。

---

## 第 6 步：打开右侧 Claude Code 面板

你可以任选一种方式打开：

### 方法 A：编辑器右上角火花图标
打开一个代码文件后，点右上角的 Claude Code 图标。

### 方法 B：左侧边栏图标
点左边栏里的 Claude Code 图标。

### 方法 C：命令面板
按：

```text
Cmd + Shift + P
```

搜索：

```text
Claude Code
```

选择打开 Claude Code 面板。

---

## 第 7 步：验证是否真的接通了

在右侧 Claude Code 面板输入：

```text
/status
```

如果能正常返回状态，基本说明已经通了。

你也可以直接问一句：

```text
帮我看看当前项目里有哪些主要文件
```

如果它能正常回复，就说明 VS Code 右侧面板已经在工作了。

---

# 最常见的 3 个问题

## 问题 1：还是弹 Anthropic 登录页

先确认两件事：

### 1）你有没有勾选 Disable Login Prompt
去 VS Code 设置里再检查一遍。

### 2）你的 `~/.claude/settings.json` 有没有写对
终端执行：

```bash
cat ~/.claude/settings.json
```

确认里面确实有这两个字段：

- `ANTHROPIC_BASE_URL`
- `ANTHROPIC_AUTH_TOKEN`

### 3）彻底退出 VS Code，再从终端启动
执行：

```bash
code .
```

这样启动的 VS Code 更容易继承终端环境。

---

## 问题 2：面板打开了，但一直没反应

大概率是 router 没跑起来。

先检查：

```bash
ccr status
```

如果没启动，就执行：

```bash
ccr start
```

如果还不行，再检查你的 `ANTHROPIC_BASE_URL` 是不是填错了，比如端口不是 `3456`。

---

## 问题 3：终端里能用，VS Code 面板不能用

这通常说明：

- 终端吃到了 `ccr activate` 的环境变量
- 但 VS Code 插件没有吃到

最稳的处理方式就是：

- 不要只依赖 `.zshrc`
- 直接把 `ANTHROPIC_BASE_URL` 和 `ANTHROPIC_AUTH_TOKEN` 写进 `~/.claude/settings.json`

这样扩展和 CLI 更容易共用一套配置。

---

# 我建议你现在就这样操作

按这个顺序来：

```bash
ccr start
ccr activate
mkdir -p ~/.claude
open -e ~/.claude/settings.json
```

然后：

1. 把 `ccr activate` 里看到的两个值写进 `~/.claude/settings.json`
2. 打开 VS Code
3. 搜索并勾选 `Disable Login Prompt`
4. 执行 `Developer: Reload Window`
5. 打开右侧 Claude Code 面板
6. 输入 `/status`

---

# 一份可直接参考的最终模板

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "env": {
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:3456",
    "ANTHROPIC_AUTH_TOKEN": "替换成你自己的token"
  }
}
```

---

# 补充说明

如果你后面换了 router 端口、token，或者换了新的 provider，只需要改这个文件：

```text
~/.claude/settings.json
```

通常不用每次都重新折腾 VS Code 插件。

---

# 参考依据

这份教程是根据以下资料整理的：

1. Anthropic / Claude Code 官方文档（VS Code 集成）
2. Anthropic / Claude Code 官方文档（环境变量与 `settings.json`）
3. `musistudio/claude-code-router` 官方 README

关键点包括：

- VS Code 扩展支持通过 `Disable Login Prompt` 适配第三方 provider
- provider 配置写在 `~/.claude/settings.json` 时，扩展和 CLI 可以共享配置
- `ANTHROPIC_BASE_URL` 可用于把请求导向 proxy / gateway
- `ANTHROPIC_AUTH_TOKEN` 用于自定义 `Authorization` 头
- `ccr activate` 会输出 `ANTHROPIC_BASE_URL` 和 `ANTHROPIC_AUTH_TOKEN`
- 使用前要先确保 `ccr start` 已运行

