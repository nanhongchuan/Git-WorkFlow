# 94-智能PDF问答工具 创建AI请求

#### **一、项目环境与依赖安装**

*   **任务目标**: 读取用户上传文档，结合提问传给AI，获得基于文档的回答。
*   **流程概述**: 加载 -> 切割 -> 向量化 -> 检索 -> 对话。
*   **准备步骤**:
    1.  创建项目文件夹。
    2.  下载并拖入课程配套的 `requirements.txt` 文件。
    3.  打开终端，执行命令 `pip install -r requirements.txt` 安装所有依赖项。
    4.  新建Python文件，例如 `_ai.py` (或 `xiaopai.py`)，所有与AI大模型交互的代码将存放于此。

#### **二、`qa_agent` 函数的定义与参数**

*   **函数作用**: 封装与AI大模型的交互请求，实现基于文档的问答。
*   **函数名示例**: `qa_agent`
*   **接收参数**:
    *   **API密钥**: `api_key` (用户提供，用于AI模型认证)。
    *   **记忆(Memory)**: `memory` (用于维持对话上下文，**必须从外部传入**，否则每次调用函数都会被初始化，导致对话列表为空)。
    *   **上传的PDF文件**: `uploaded_file` (用户在网页上传的PDF内容，初始在内存中)。
    *   **用户提问**: `user_question` (用户提出的问题)。

#### **三、AI模型与组件初始化**

1.  **大模型 (LLM) 初始化**:
    *   **导入**: `from langchain_openai import OpenAI`
    *   **实例化**: `model = OpenAI(model_name="...", openai_api_key=api_key)`

2.  **文档加载器 (PDF Loader)**:
    *   **导入**: `from langchain_community.document_loaders import PyPDFLoader`
    *   **问题**: `PyPDFLoader` 默认接收本地文件路径，但用户上传文件在内存中没有路径。
    *   **解决方案**:
        *   **读取内存文件**: `bytes_content = uploaded_file.read()` (获取二进制数据)。
        *   **创建临时本地文件**: 定义一个临时文件路径，例如 `temp_file_path = "temp.pdf"`。
        *   **写入临时文件**: 使用 `with open(temp_file_path, 'wb') as f: f.write(bytes_content)` 将二进制内容写入本地。
        *   **实例化加载器**: `loader = PyPDFLoader(temp_file_path)`。
        *   **加载文档**: `documents = loader.load()` (得到 document 列表)。

3.  **文本切割器 (Text Splitter)**:
    *   **导入**: `from langchain.text_splitter import RecursiveCharacterTextSplitter`
    *   **实例化**: `splitter = RecursiveCharacterTextSplitter(chunk_size=..., chunk_overlap=..., separators=["...", "..."])`
        *   `separators` 参数可设置为更适合中文文本的分隔符。
    *   **切割文档**: `split_documents = splitter.split_documents(documents)`。

4.  **向量嵌入模型 (Embedding Model)**:
    *   **导入**: 需导入一个嵌入模型（具体类型未明确提及，但通常是 `OpenAIEmbeddings` 或 `HuggingFaceEmbeddings` 等）。
    *   **实例化**: `embedding_model = EmbeddingModel(...)`。

5.  **向量数据库 (VectorStore)**:
    *   **导入**: `from langchain_community.vectorstores import FAISS` (示例中选择FAISS，你也可以选择其他本地或云端数据库)。
    *   **向量化并存储**: `vector_db = FAISS.from_documents(split_documents, embedding_model)` (将分割后的文档向量化并存入数据库)。
    *   **获取检索器 (Retriever)**: `retriever = vector_db.as_retriever()` (用于在数据库中进行检索)。

#### **四、构建对话链 (Conversational Chain)**

*   **链类型**: 带有记忆的检索增强对话链 (Conversational Retrieval Chain)。
*   **导入**: `from langchain.chains import ConversationalRetrievalChain`
*   **实例化**: `chain = ConversationalRetrievalChain.from_llm(llm=model, retriever=retriever, memory=memory)`
    *   `llm`: 传入之前初始化的大模型实例。
    *   `retriever`: 传入之前获取的检索器实例。
    *   `memory`: 传入外部提供的记忆实例。

#### **五、调用链并返回结果**

*   **调用方法**: `chain.invoke()`
*   **传入参数**: 一个字典，包含：
    *   `"chat_history"`: 对应 `memory` (包含了历史对话)。
    *   `"question"`: 对应 `user_question` (用户当前的问题)。
*   **返回结果**: `return chain.invoke({"chat_history": memory, "question": user_question})` (得到AI基于文档的回答)。

---