# 75-Conversation Chain 开箱即用的带记忆对话链

### 1. `Conversation Chain` 是什么？
*   一个预构建的、开箱即用的对话链（通常在 `chains` 模块下）。
*   专门用于进行带记忆的对话。
*   能够自动从内存中加载和保存上下文。

### 2. 使用 `Conversation Chain` 的准备工作
*   **大型语言模型 (LLM)**：用于对话本身，例如各种AI模型。
*   **记忆模块 (Memory)**：用于存储和加载对话历史，例如 `ConversationBufferMemory`。

### 3. 创建 `Conversation Chain`
*   实例化 `Conversation Chain` 时，需要传入 `llm` 和 `memory` 参数。
*   **示例代码结构：**
    ```python
    # 假设你已经创建了 llm_model 和 memory_module
    from langchain.chains import ConversationChain
  
    conversation_chain = ConversationChain(
        llm=llm_model, 
        memory=memory_module
    )
    ```

### 4. 使用 `Conversation Chain` 进行对话
*   通过调用 `.invoke()` 方法来使用链。
*   **输入格式：** 一个字典，用户的提示（输入）必须放入 `input` 键所对应的值中。
*   **示例代码：**
    ```python
    response = conversation_chain.invoke({"input": "你的问题在这里"})
    ```
*   **输出内容：** 结果会包含给模型的输入、记忆中的历史消息以及AI的回应。

### 5. `Conversation Chain` 的核心优势（自动记忆管理）
*   **无需手动加载记忆：** 每次调用前，不需要手动调用 `memory.load_memory_variables()` 来载入记忆里的对话。
*   **无需手动保存记忆：** 每次调用后，新一轮对话会自动被加入到记忆里，不需要手动调用 `memory.save_context()` 方法。
*   **实现丝滑连续对话：** 极大地简化了带记忆的连续对话的实现代码，非常方便。

### 6. 自定义提示模板 (Prompt Template)
*   `Conversation Chain` 支持指定提示模板，用于设定AI的人设或行为（例如：脾气暴躁、喜欢阴阳怪气的助手）。
*   **提示模板中的变量名要求：**
    *   表示用户输入的变量名 **必须** 是 `input`。
    *   表示历史消息的变量名 **必须** 是 `history`。
    *   **注意：** 如果变量名与 `Conversation Chain` 预期不符，将出现报错。
*   **集成方法：** 将提示模板赋值给 `ConversationChain` 的 `prompt` 参数。
*   **示例代码结构：**
    ```python
    from langchain.prompts import PromptTemplate
    # ... (你的 llm_model 和 memory_module)
  
    template = """
    你是一个脾气暴躁、喜欢阴阳怪气的助手。
    历史对话:
    {history}
    用户: {input}
    助手（阴阳怪气地回应）:
    """
    prompt = PromptTemplate(input_variables=["history", "input"], template=template)
  
    conversation_chain_with_prompt = ConversationChain(
        llm=llm_model, 
        memory=memory_module, 
        prompt=prompt
    )
    ```

### 7. 关于记忆类型
*   `ConversationBufferMemory` 只是众多记忆类型中的一种。
*   未来会有更多其他类型的记忆模块介绍。

---