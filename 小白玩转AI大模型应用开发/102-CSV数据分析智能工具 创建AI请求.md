# 102-CSV数据分析智能工具 创建AI请求

#### **一、 章节目标与核心任务**
*   **目标：** 完成向AI发送请求，以响应用户对表格的任意问题、数据提取或图表绘制需求。
*   **挑战：** 根据AI响应的不同内容（字符串、表格、图表），前端展示方式不同。因此，需要在提示词中明确返回内容的格式。

#### **二、 项目初始设置**
1.  **项目文件夹：** 已创建。
2.  **依赖安装：**
    *   下载 `requirements.txt` 文件并拖入项目。
    *   打开终端，执行命令：`pip install -r requirements.txt` 安装所有依赖。
3.  **代码文件：**
    *   新建一个Python代码文件，所有与AI大模型交互的代码将在此文件中。

#### **三、 核心功能：封装AI请求函数**
*   定义一个名为 **`data_frame_agent`** (暂定名，原视频未明确给出函数名，但根据功能推断) 的函数，用于封装AI大模型交互逻辑。

##### **3.1 函数参数**
1.  `api_key`: 用户提供的API密钥（字符串）。
2.  `df`: 表示表格数据，类型为 **pandas.DataFrame**。
3.  `user_query`: 用户的提问或要求（字符串）。

##### **3.2 AI模型初始化**
1.  **导入：** `from langchain_community.llms import OpenAI`
    *   *(注：原视频可能指的是旧版langchain的 `from langchain.llms import OpenAI`)*
2.  **实例化：**
    ```python
    llm = OpenAI(
        model="模型的型号",  # 指定使用的模型型号
        openai_api_key=api_key,
        temperature=0       # 核心设置：温度设为最低的0
    )
    ```
3.  **`temperature=0` 的原因：** 让AI严格遵循React思考框架，不自行发挥创造力，避免解析失败。

##### **3.3 Agent执行器初始化**
1.  **导入：** `from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent`
2.  **实例化：**
    ```python
    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        agent_executor_kwargs={"handle_parsing_errors": True}, # 核心设置
        verbose=True                                            # 核心设置
    )
    ```
3.  **`agent_executor_kwargs={"handle_parsing_errors": True}` 的作用：** 尽可能让模型自行消化和处理错误，而不是直接终止程序。
4.  **`verbose=True` 的作用：** 在程序运行时，终端会显示AI的完整思考过程。

#### **四、 关键：响应内容的格式规范（提示词工程）**
*   **问题：** 前端需要明确知道是显示字符串、表格还是图表。
*   **解决方案：** 让AI返回一个 **JSON字符串**，该字符串解析成字典后，根据字典的键判断展示类型。

##### **4.1 AI提示词内容（核心）**
    你是一个数据分析助手，能够根据用户的不同请求来返回不同的内容。
    不管响应的格式被要求成啥样，你都要返回JSON字符串，并且所有的字符串都要用双引号进行包围。

    *   **A. 文字回答：**
        如果用户需要文字回答，返回字典格式：
        ```json
        {"answer": "回答的字符串"}
        ```
    *   **B. 表格数据：**
        如果用户需要提取数据（表格形式），返回字典格式：
        ```json
        {
            "table": {
                "columns": ["列名1", "列名2", ...],
                "data": [
                    ["内容1_1", "内容1_2", ...],
                    ["内容2_1", "内容2_2", ...],
                    ...
                ]
            }
        }
        ```
    *   **C. 图表数据：**
        如果用户需要图表（条形图、折线图、散点图），返回字典格式：
        *   **条形图 (bar)：**
            ```json
            {
                "bar": {
                    "columns": ["x轴数据列名", "y轴数据列名"],
                    "data": [
                        ["值1", "值2"],
                        ["值3", "值4"],
                        ...
                    ]
                }
            }
            ```
        *   **折线图 (line)：** 格式同条形图
            ```json
            {"line": {"columns": [...], "data": [...]}}
            ```
        *   **散点图 (scatter)：** 格式同条形图
            ```json
            {"scatter": {"columns": [...], "data": [...]}}
            ```

##### **4.2 构造最终Prompt**
*   将用户的原始问题 (`user_query`) 与上述格式要求拼接起来，形成完整的提示词。

#### **五、 调用Agent与解析响应**
1.  **调用 `invoke` 方法：**
    ```python
    response = agent.invoke({"input": prompt}) # 将拼接好的prompt作为输入
    ```
    *   Agent返回的内容在 `response["output"]` 中。
2.  **解析JSON字符串：**
    *   **导入：** `import json`
    *   **解析：** `parsed_response = json.loads(response["output"])`
    *   **目的：** 将AI返回的JSON字符串解析成Python字典，方便前端使用。
3.  **返回值：** 函数返回 `parsed_response` 字典。

#### **六、 函数测试与验证**
1.  **导入模块：**
    *   `import os` (用于获取环境变量中的API密钥)
    *   `import pandas` (用于创建DataFrame)
2.  **示例步骤：**
    *   准备一个示例CSV文件（拖入项目文件夹）。
    *   **加载API密钥：** `os.environ["OPENAI_API_KEY"] = "你的密钥"` (或从环境变量中读取)
    *   **创建DataFrame：** `df = pandas.read_csv("你的示例文件.csv")`
    *   **定义测试问题：** `query = "数据里出现最多的职业是什么？"`
    *   **调用函数：** `result = data_frame_agent(os.environ["OPENAI_API_KEY"], df, query)`
    *   **打印结果：** `print(result)`
3.  **验证：**
    *   观察 `verbose=True` 输出的AI思考过程，确认逻辑是否正确。
    *   检查返回的 `result` 字典格式是否符合预期，以及回答是否准确。

---

**下一节：** 将一起实现数据分析智能工具的前端网站。