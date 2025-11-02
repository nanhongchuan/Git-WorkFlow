 # 79-克隆AI聊天助手 创建AI请求

本节目标是实现AI请求功能，确保对话连贯性 (带记忆)。

#### **1. 项目准备与依赖安装**

*   **文件下载：** 将课程配套资料中的 `requirements.txt` 文件下载并拖入项目文件夹。
*   **依赖安装：** 在终端中执行命令 `pip install -r requirements.txt` 安装所有依赖。
*   **代码文件创建：** 新建一个Python文件，所有与AI大模型交互的代码将在此文件中编写。

#### **2. 定义 `get_response` 函数 (核心)**

*   **函数目的：** 封装对AI模型的请求逻辑。
*   **函数参数：**
    *   `user_prompt`：用户的提示/消息内容。
    *   `api_key`：用户提供的API密钥。
    *   `memory`：**（关键）** 外部传入的记忆对象。
        *   **重要性：** 记忆必须从外部传入，而不是在函数内部初始化。否则，每次调用函数都会创建一个空的对话列表，模型无法获取之前的对话内容，无法实现连贯对话。

#### **3. LangChain 核心组件集成**

*   **导入模型：**
    *   从 `langchain_openai` 导入 `ChatOpenAI`。
    *   实例化 `ChatOpenAI` 模型，传入 `model` 型号和 `openai_api_key` (即从参数中获取的 `api_key`)。
*   **导入对话链：**
    *   从 `langchain.chains` 导入 `ConversationChain` (带记忆的对话链)。
*   **定义对话链：**
    *   实例化 `ConversationChain`，传入两个主要参数：
        *   `llm`：设置为前面定义的 `model` 实例。
        *   `memory`：设置为函数参数中传入的 `memory` 对象。
    *   **好处：** `ConversationChain` 会自动处理记忆的加载和新对话的加入，避免手动操作的遗漏和错误。

#### **4. 调用对话链并处理响应**

*   **调用链：** 使用 `conversation_chain.invoke()` 方法调用对话链。
*   **参数：** `invoke` 方法接收一个字典作为输入，其中用户提示需要放入 `input` 键所对应的值，例如 `{"input": user_prompt}`。
*   **响应结构：** `invoke` 返回的内容 (`response` 变量) 会是一个字典，包含用户输入、历史对话以及AI模型的回应。
*   **返回内容：** 由于我们只需要AI模型的回应，实际返回的是 `response` 字典中 `response` 键所对应的值 (`response['response']`)。

#### **5. 可用性测试**

*   **导入记忆模块：** 在测试前，从 `langchain.memory` 导入最简单易懂的 `ConversationBufferMemory`。
*   **初始化记忆：** 在调用 `get_response` 之前，定义并初始化 `memory` 对象（例如 `memory = ConversationBufferMemory()`）。
*   **首次调用：** 调用 `get_response`，传入：
    1.  一个随机字符串作为用户消息内容。
    2.  前面定义的 `memory` 对象。
    3.  从环境变量中获取的API密钥。
*   **打印结果：** 将 `get_response` 返回的内容打印出来，以查看AI的回应。
*   **二次调用 (测试记忆)：** 紧接着再次调用 `get_response`，使用**同一个** `memory` 对象，并询问AI上一个问题是什么 (例如 "上一个问题问的是啥?")。
*   **验证：** 运行代码并观察输出。如果AI能正确回答上一个问题，则证明对话链中的记忆功能正常工作。

#### **6. 后续计划**

*   下一节将着手开发克隆 ChatGPT 网站的前端部分。

---