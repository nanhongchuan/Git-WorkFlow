# Claude Code 核心技巧速查表

> 来源：B站视频《最火AI编程Claude Code详细攻略，一期视频精通》
> 整理时间：2026-04-18

---

## 一、基础启动方式

| 方式 | 命令 | 说明 |
|------|------|------|
| 官方账户登录 | `claude` | Pro 或 Max 用户直接启动，登录官网账户 |
| API 接入（通过 CCR） | `CCR Code` | 用 Claude Code Router 开源项目，可接入任意大模型 API |

---

## 二、核心命令一览

| 命令 | 功能 | 使用场景 |
|------|------|---------|
| `/init` | 通读项目所有文件，生成 `Claude.md` 作为上下文 | 新项目接手时初始化 |
| `/compact` | 压缩对话上下文，排除无关内容 | 长对话降 token 消耗、提升专注度 |
| `/clear` | 清除对话记录 | 每次开启新任务前 |
| `/resume` | 回溯历史话题，继续之前的对话 | 中断后继续工作 |
| `/IDE` | 连接 VSCode 等 IDE，代码修改有对比视图 | 习惯 GUI 操作时 |
| `/permissions` | 精细化控制工具权限（allow/deny） | 安全管控工具调用 |
| `/export` | 导出当前对话到剪贴板 | 备份或交叉验证 |
| `/mcp` | 查看已安装的 MCP Server 列表 | MCP 管理 |
| `/agents` → `create` | 创建子代理（Subagent） | 并行处理多任务 |

---

## 三、思考深度控制

| 指令 | 强度 | 适用场景 |
|------|------|---------|
| `think <任务>` | ⭐ | 一般任务 |
| `think hard <任务>` | ⭐⭐ | 较复杂推理 |
| `think harder <任务>` | ⭐⭐⭐ | 高复杂度任务 |
| `ultra think <任务>` | ⭐⭐⭐⭐ | 关键架构决策、核心算法 |

> 以上为 Claude Code 官方内置指令，非提示词技巧。

---

## 四、快捷键与交互技巧

| 操作 | 说明 |
|------|------|
| `! + 命令` | 在对话中直接执行 shell 命令（如 `!npm install`），结果自动加入上下文 |
| `#` 进入记忆模式 | 内容存入 `Claude.md`（项目级）或云端配置（全局生效） |
| `@文件/@目录` | 精确注入上下文 |
| `Esc` | 立即停止当前执行 |
| `Shift+Tab`（按两次） | 切换 Plan Mode，只规划不执行 |
| `Ctrl+G` | 跳转到历史对话 |
| `Ctrl+Z` | 挂起 Claude Code 会话，返回终端 |

---

## 五、MCP（Model Context Protocol）

### 核心命令

| 操作 | 命令 |
|------|------|
| 安装 MCP | `claude mcp add <名称>` |
| 安装（用户级全局） | `claude mcp add <名称> --scope user` |
| 查看已安装 MCP | `/mcp` |
| 删除 MCP | `claude mcp remove <名称>` |
| 远程 SSE 调用 | `claude mcp add <名称> --protocol sse --url <服务地址>` |
| 远程 HTTP 调用 | `claude mcp add <名称> --protocol streamable-http --url <服务地址>` |

### 实用示例
- 装 `context7` 查最新代码文档
- 要求 AI 将 Tailwind V3 项目升级到 V4

---

## 六、权限管理

| 模式 | 命令/参数 | 说明 |
|------|----------|------|
| 精细化权限 | `/permissions` → `allow`/`deny` | 自定义哪些工具可自动调用 |
| 高权限模式 | `--dangerously-skip-permissions` | 启动时加此参数，跳过所有确认，权限最大，**慎用** |

---

## 七、自定义命令 & Hooks

### 自定义命令
- **存放位置**：
 - 项目级：`.cloud/commands/`
 - 用户级：Claude Code 配置目录下的 `commands/`（全局生效）
- **创建方式**：在 commands 文件夹创建 `.md` 文件，文件名即命令名
- **参数传递**：使用 `$arguments` 占位
- **示例**：创建 `codereview.md`，命令 `/codereview <分支名>` 执行 Git diff 并给出 Code Review 意见

### Hooks（钩子）
- **配置文件**：`.cloud/settings.json` 或 `.cloud/settings.local.json`
- **触发时机**：`PreToolUse`（工具调用前）、`PostToolUse`（工具调用后）、`PostToolUseFailure`（失败后）、`Notification`、`UserPromptSubmit`
- **实用示例**：AI 修改代码后自动跑 `npx prettier check` 检查格式，发现错误自动修复

---

## 八、子代理（Subagents）

| 配置项 | 说明 |
|--------|------|
| 描述 | 用自然语言描述 Subagent 的任务和期望结果 |
| 工具权限 | 赋予 Subagent 所需工具的权限 |
| 模型 | 选择使用的模型 |
| 颜色 | 分配代表颜色区分 |

**工作流程**：主 Agent 接收任务 → 自动拆解为子任务 → 分配给不同 Subagent **并行执行** → 主 Agent 整合结果

**适用场景**：代码审核 + 天气查询等多任务并行、复杂任务拆解

---

## 九、GitHub 集成

| 步骤 | 操作 |
|------|------|
| 1 | 确保安装 `gh CLI`，执行 `gh repo list` 验证 |
| 2 | 让 Claude Code 读取 GitHub Issue 内容 |
| 3 | Claude Code 本地完成代码修复 |
| 4 | 创建新分支并推送到 GitHub |

形成 **读取 Issue → 本地修复 → 推送到 GitHub** 的完整闭环。

---

## 十、对话 & 代码回退

| 操作 | 命令/工具 | 说明 |
|------|----------|------|
| 回退对话 | `/resume` | 仅回退对话内容，不回退代码 |
| 同步回退 | `ccundo <编号>` | 对话和代码状态同步回退（需安装 ccundo 工具） |
| 列出历史 | `ccundo list` | 列出所有历史记录及编号 |

---

## 十一、可视化界面：Claudia

| 功能 | 说明 |
|------|------|
| 安装方式 | GitHub 下载预编译包（社区 Fork 版本） |
| 历史管理 | 管理历史项目及对话记录 |
| 思考长度 | 左下角可调节 AI 思考深度 |
| 可视化操作 | 创建 MCP、编辑 `Claude.md` 等 |

> 官方账户可直接用；API/CCR 启动需在设置中配置 `Anthropic Auth Token` 和 `Anthropic Base URL`。

---

## 十二、非交互模式

| 命令 | 说明 |
|------|------|
| `claude -p <问题>` | 一次性后台对话，结果打印输出，适合脚本集成 |
| `CCR Code -p <问题>` | 通过 CCR 启动时用法 |
