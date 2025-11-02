# 97-Agent 自定义你的AI工具

#### 1. Agent 核心概念

*   **定义：** Agent（智能体/代理）是能理解用户的查询或指令，进行推理，并执行特定任务，最后输出响应的服务。
*   **构成：** 是 **Reason (推理)** 和 **Action (行动)** 的结合。
*   **AI Agent 需求：**
    *   根据用户输入和环境进行动态推理。
    *   基于推理采取合理行动。
    *   在需要时借助合适的外部工具。
    *   增强模型的功能和效率。
*   **根基：** 大语言模型（LLM），但 Agent 会经过多个步骤来产生输出。

#### 2. Agent 的工作机制：推理-行动-观察 (ReAct) 框架

Agent 的每个步骤通常遵循 **推理-行动-观察（Reasoning-Action-Observation）** 框架，循环执行直到任务完成。

*   **1. 推理 (Reasoning)：**
    *   **模型扮演角色：** 作为思考的大脑。
    *   **目的：** 了解下一步应该做什么。
    *   **输入：** 用户的输入、环境信息、提示词（包含能利用的工具信息）。
    *   **输出：**
        *   下一步的 **行动 (Action)** 及给工具的 **输入** (例如：`Search` + 搜索词)。
        *   或者，如果任务已完成，返回 **完成信息** 及给用户的 **响应内容**。
*   **2. 行动 (Action)：**
    *   **执行者：** Agent Executor (Agent 执行器)。
    *   **过程：** 把从推理步骤得到的输入传递给工具，让工具与环境进行交互。
    *   **输出：** 工具的执行结果。
*   **3. 观察 (Observation)：**
    *   **目的：** 查看行动步骤得到的结果。
    *   **结果：** 这一观察又会引发下一轮的推理。
*   **循环：** 推理 → 行动 → 观察 持续循环，直到推理步骤认为已得到答案。

#### 3. 构建 Agent 的核心组件

*   **1. 模型 (Model)：**
    *   **作用：** Agent 的大脑，不可或缺。
    *   **建议参数：** `temperature` 设置为很小的数字（例如0），以确保模型严格按 ReAct 框架输出，减少创造性。
*   **2. 工具 (Tools)：**
    *   **作用：** 补充大语言模型本身的缺陷（例如：LLM不擅长精确计数），提供特定能力。
    *   **定义方法：**
        *   定义一个类，继承自 `langchain.tools.BaseTool` (需从 `langchain.tools` 导入)。
        *   **类变量：**
            *   `name`：工具的名称，用于 Agent 选择。
            *   `description`：工具的描述，帮助 Agent 理解工具作用。
        *   **核心功能：** 在 `_run` 方法中实现工具的实际功能（该方法会在 Agent 调用工具时被执行）。
        *   **集合：** 将工具类的实例放入一个 `tools` 列表，供 Agent 执行器使用。
*   **3. 提示词 (Prompt)：**
    *   **作用：** 告知模型要遵循 ReAct 框架，并介绍可使用的工具。
    *   **获取来源：**
        *   **LangChain Hub：** 一个用于管理和共享 LangChain 相关资源的在线平台，可获取预定义的提示词模板。
        *   **获取方式：**
            1.  安装 `langchainhub` 库。
            2.  从 `langchain` 导入 `hub`。
            3.  调用 `hub.pull()` 并传入提示词在 LangChain Hub 上的路径（例如：`"hwchase17/structured-chat-agent"`）。
        *   **输出：** `ChatPromptTemplate` 对象。

#### 4. Agent 的初始化与执行 (LangChain)

*   **1. 初始化 Agent：**
    *   **导入：** 从 `langchain.agents` 导入 `create_structured_chat_agent`。
    *   **调用：** `create_structured_chat_agent(llm=模型实例, tools=工具列表, prompt=提示模板)`。
    *   **作用：** 定义了 Agent 的思考方式和可用能力。
*   **2. 初始化 Agent Executor (Agent 执行器)：**
    *   **作用：** 实际执行 Agent 逻辑和调用工具的组件。
    *   **导入：** 从 `langchain.agents` 导入 `AgentExecutor`。
    *   **调用：** `AgentExecutor.from_agent_and_tools(agent=已定义Agent, tools=工具列表)`。
    *   **可选参数：**
        *   `memory`：实现连续对话。
            *   `memory_key` 必须设置为 `chat_history` (与提示模板中的变量名一致)。
        *   `handle_parsing_errors=True`：
            *   **默认：** `False` (解析错误时程序终止)。
            *   **设置 `True` 时：** Agent 执行器会将解析错误作为 **观察 (Observation)** 发送回大模型，让大模型自行推理处理错误。
            *   **注意：** LLM 输出具有不稳定性，即便开启此功能，仍可能需要二次尝试。
        *   `verbose=True`：
            *   **默认：** `False` (只返回最终结果)。
            *   **设置 `True` 时：** 以详细模式运行，打印 Agent 的行动过程日志（推理-行动-观察的每一步）。
*   **3. 运行 Agent：**
    *   调用 `AgentExecutor` 实例的 `invoke()` 方法，传入用户问题 (例如：`executor.invoke({"input": "你的问题"})`)。
    *   **输出：** 一个包含 `input`、`output` 和 `chat_history` 的字典。
    *   **获取结果：** 可以直接提取 `output` 键的值。

#### 5. Agent 的优势

*   集成适应不同需求和问题的工具。
*   具备复杂的决策和推理过程。
*   能更好地理解用户需求。
*   能处理复杂的问题。
*   助力创造更智能和强大的 AI 助手。

---