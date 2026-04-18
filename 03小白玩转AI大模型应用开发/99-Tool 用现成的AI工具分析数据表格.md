 # 99-Tool 用现成的AI工具分析数据表格

#### **1. CSV文件基础知识**

*   **定义：** Comma Separated Values (逗号分隔值)，一种非常常见的纯文本数据储存格式。
*   **格式特点：**
    *   每一个值之间都用英文逗号 `,` 进行分隔。
    *   可用记事本打开查看原始文本。
    *   用Excel等表格软件打开时，能直接看到表格形式，逗号会自动对齐并分隔值。
*   **兼容性：** Excel文件可以导出成CSV格式。
*   **用途：** 储存表格数据。

#### **2. LangChain CSV Agent 简介**

*   **目的：** 方便地分析CSV数据文件，回答如“数据集里所有房子平均价格是多少”等问题。
*   **解决方案：** LangChain 提供一个**开箱即用**的Agent执行器 (`create_csv_agent`)。
*   **位置：** `langchain_experimental.agents.agent_toolkits` 模块。

#### **3. 环境准备与安装**

*   **核心库：** `langchain_experimental` (如果未安装，需安装此库)。
*   **底层依赖：** CSV Agent 底层会用到 `pandas` 和 `tabulate` 库。
*   **安装命令示例 (如果尚未安装)：**
    ```bash
    pip install langchain_experimental pandas tabulate
    ```

#### **4. 创建与配置 CSV Agent**

*   **导入函数：**
    ```python
    from langchain_experimental.agents.agent_toolkits import create_csv_agent
    ```
*   **创建 Agent 实例：** 使用 `create_csv_agent()` 函数。
*   **核心参数：**
    *   `llm`：必选，指定要使用的AI模型实例。
    *   `path`：必选，指定要分析的CSV文件的路径。
    *   `verbose=True`：可选，设为 `True` 以展示 AI 的思考过程（action/observation）。
    *   `agent_executor_kwargs`：可选，用于传递更多参数给 Agent 执行器。
        *   `handle_parsing_errors=True`：设置在 `agent_executor_kwargs` 字典中，避免 Agent 出错后直接报错，而是尝试处理。
*   **示例代码结构：**
    ```python
    agent_executor = create_csv_agent(
        llm=your_llm_instance,
        path='/path/to/your/data.csv',
        verbose=True,
        agent_executor_kwargs={"handle_parsing_errors": True}
    )
    ```

#### **5. CSV Agent 的工作原理 (幕后)**

*   **Agent 结构：** `create_csv_agent` 函数定义了一个 Agent 执行器，你可以打印查看其内部组件。
*   **提示模板 (Prompt Template)：**
    *   内置预设的英文模板。
    *   大致告诉 AI 模型：“你正在与 Python 的 `pandas` Data Frame 打交道，该 Data Frame 的名字是 `df`。”
    *   包含变量值，会在后续被插入（如工具介绍）。
*   **思考框架：** 模型采用 **ReAct 框架**进行思考（Reasoning and Acting）。
*   **核心工具 (Tool)：**
    *   `pandas_interactive_executor`：一个交互式 Python 解释器，主要用于执行与 `pandas` 相关的代码，进行数据操作和查询。

#### **6. 与 CSV Agent 交互 (提问与验证)**

*   **提问方法：** 对 `agent_executor` 调用 `invoke()` 方法，传入你的问题。
    ```python
    response = agent_executor.invoke("你的问题在这里")
    print(response)
    ```
*   **关键点：** 如果提示模板是英文，为了确保中文回复，可在问题中明确要求“用中文回复”。

*   **常见问题示例及AI思考过程：**

    1.  **问：** “数据集有多少行？”
        *   **AI思考：** 利用 `data frame` 的 `shape` 方法。
        *   **AI行动：** 选择并应用与 `pandas` 代码执行相关的工具。
        *   **结果验证：** 可直接查看原始CSV文件验证回答。

    2.  **问：** “数据集包含哪些变量？”
        *   **AI思考：** 通过查看表格的列名。
        *   **AI行动：** 执行输出列名的命令。

    3.  **问：** “价格平均值是多少？”
        *   **AI思考：** 计算指定列的平均值。
        *   **AI行动：** 执行 `pandas` 代码进行计算。
        *   **结果可信度：** 答案是代码执行得出的，因此可信度高，可自行校验。

    4.  **问：** “房间数量的取值范围是什么？这些取值范围可能代表什么？” (事实与主观结合)
        *   **AI行动：** 通过代码执行查看变量值的种类、范围。
        *   **AI推断：** 根据变量值思考其含义并给出解释。

#### **7. 总结与展望**

*   **核心价值：** 通过短短几行代码，即可拥有一个能够与本地CSV数据文件交互的AI助手。
*   **扩展性：** LangChain 除了 CSV Agent，还提供其他开箱即用的 Agent 执行器（如 Pandas Agent、SQL Agent 等），鼓励探索和尝试。
https://python.langchain.com/does/integrations/toolkfts/