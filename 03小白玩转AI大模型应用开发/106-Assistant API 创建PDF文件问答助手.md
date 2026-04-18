# 106-Assistant API：创建PDF文件问答助手**

**核心目标：**
*   利用 Assistant API 的检索器（retrieval）功能，创建一个能基于文件内容回答问题的问答助手。

**支持的文件类型**：https://platform.openai.com/docs/assistants/tools/code-interpreter#supported-files

---

# 代码解释

### 积木1：导入OpenAI库
```python
from openai import OpenAI
```
*   **作用：** 导入 `OpenAI` 这个工具包。
*   **小白比喻：** 想象一下你是一个木匠，你要开始做木工活了。这行代码就像是把你需要的 `OpenAI` 工具箱搬进了你的工作室。没有这个工具箱，你就无法使用里面的工具。

### 积木2：创建OpenAI客户端实例
```python
client = OpenAI()
```
*   **作用：** 创建一个 `OpenAI` 客户端对象，它是你与 OpenAI 服务进行通信的“遥控器”。
*   **小白比喻：** 你搬来了工具箱，现在你需要拿起一个“遥控器”来操作里面的高科技工具。这个 `client` 变量就是你的遥控器。当你运行这行代码时，它会偷偷地去寻找你电脑里设置的 OpenAI API Key（这是你的身份凭证，告诉OpenAI你是谁，并且允许你使用他们的服务），然后连接到OpenAI的服务器。

### 积木3：上传文件
```python
file = client.files.create(
    file=open("论文介绍.pdf", "rb"),
    purpose="assistants"
)
```
*   **作用：** 把你的本地文件（这里是 `论文介绍.pdf`）上传到 OpenAI 的云端服务器上。
*   **小白比喻：** 你家里有一本很厚的“论文介绍”书（`论文介绍.pdf`）。我们现在要让 OpenAI 的聪明助手来阅读它。助手不能直接从你家里读这本书，所以你需要把这本书的电子版上传到 OpenAI 的“云图书馆”里。
    *   `client.files.create()`：这是你用“遥控器”发出的一个命令，告诉 OpenAI “我要上传一个文件。”
    *   `file=open("论文介绍.pdf", "rb")`：
        *   `open("论文介绍.pdf", "rb")`： 这是 Python 代码，表示“打开当前文件夹里名字叫 `论文介绍.pdf` 的文件”。
            *   `"rb"` 也很重要，它表示“以**二进制读取模式**打开”。因为 PDF 文件不是简单的文本文件，它包含图片、格式等，所以要用二进制方式读取。
    *   `purpose="assistants"`：这告诉 OpenAI，你上传这个文件是专门为了给“助手”（Assistant）使用的。这样 OpenAI 就能正确地处理和管理它。
*   **结果：** `file` 这个变量会保存 OpenAI 服务器上这个已上传文件的信息，其中最重要的是它的唯一ID。

### 积木4：创建智能问答助手
```python
assistant = client.beta.assistants.create(
    model="gpt-3.5-turbo",
    name="AI论文问答助手",
    instructions="你是一个智能助手，可以访问文件来回答人工智能领域论文的相关问题。",
    tools=[{"type": "retrieval"}],
    file_ids=[file.id]
)
```
*   **作用：** 定义并创建一个拥有特定能力（能看文件）的智能助手。
*   **小白比喻：** 你的书上传到云图书馆了，现在你需要“雇佣”一位专业的“图书馆管理员”来帮你管理和解答关于这本书的问题。
    *   `client.beta.assistants.create()`： 这是用“遥控器”发出的命令，告诉 OpenAI “我要创建一个助手！”（`beta` 表示这是个新功能，可能还在测试阶段，但现在很稳定）。
    *   `model="gpt-3.5-turbo"`： 助手用哪个“大脑”来思考？这里我们选择了 `gpt-3.5-turbo`，这是一个非常强大的模型，擅长理解和生成文本。你也可以选择更高级的 `gpt-4-turbo`。
    *   `name="AI论文问答助手"`： 给你的助手起个好听的名字。
    *   `instructions="你是一个智能助手，可以访问文件来回答人工智能领域论文的相关问题。"`： 这非常重要！这是给助手的“任务说明书”。你告诉助手它的角色是什么（智能助手），能做什么（访问文件来回答问题），以及它应该关注什么领域（人工智能论文）。这些指令会指导助手如何回答问题。
    *   `tools=[{"type": "retrieval"}]`： 这就是让助手能“**看文件**”的关键！
        *   `tools` 是一个列表，里面可以放助手的能力。
        *   `{"type": "retrieval"}`： 这是一个特殊的工具类型，叫做“检索器”。有了这个工具，助手就获得了在它被关联的文件中**搜索、阅读和提取信息**的能力。如果没有这个，即使你上传了文件，助手也不知道怎么用。
    *   `file_ids=[file.id]`： 这里把你之前上传的“论文介绍.pdf”文件（通过它的 `file.id`）和这个助手关联起来。你告诉图书馆管理员：“这是我希望你阅读的那本书的ID。” 助手就知道要根据这本书来回答问题。
*   **结果：** `assistant` 这个变量会保存你创建的智能助手的信息，包括它的唯一ID。

### 积木5：创建对话线程
```python
thread = client.beta.threads.create()
```
*   **作用：** 创建一个“对话线程”（Thread）。
*   **小白比喻：** 想象你和你的图书馆管理员（助手）要开始聊天了。一个“线程”就像是一个空白的聊天窗口或者一个笔记本。你所有的问题和它的所有回答都会记录在这个特定的聊天窗口里，形成一个完整的对话历史。每次新的对话，你都可以创建一个新的线程。
*   **结果：** `thread` 这个变量会保存这个对话线程的信息，包括它的唯一ID。

### 积木6：定义获取助手回复的函数
```python
def get_response_from_assistant(assistant, thread, prompt, run_instruction=""):
    # 1. 用户发送消息
    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=prompt
    )

    # 2. 助手开始运行
    run = client.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=assistant.id,
      instructions=run_instruction
    )

    # 3. 等待助手完成运行
    while run.status != "completed":
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(f"Run status: {keep_retrieving_run.status}")

        if keep_retrieving_run.status == "completed":
            break

    # 4. 获取并打印所有消息
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    for data in messages.data:
        print("\n")
        print(data.content[0].text.value)
        print("------")
```
*   **作用：** 这是一个Python函数，它把“问问题”和“获取答案”这一系列操作打包起来，方便我们重复使用。
*   **小白比喻：** 这就像你写了一个“问答流程自动化”的脚本。每次你想问问题，只需要调用这个脚本，它就会帮你完成所有必须的步骤。
    *   `def get_response_from_assistant(...)`: 定义了一个函数，它需要几个信息才能工作：
        *   `assistant`: 你的智能助手是谁？
        *   `thread`: 在哪个聊天窗口里对话？
        *   `prompt`: 你要问的问题是什么？
        *   `run_instruction=""`: （可选）针对这次运行的额外指令。

    *   **函数内部的步骤：**
        1.  **`message = client.beta.threads.messages.create(...)`**：
            *   你作为“用户”（`role="user"`），把你问的问题 (`prompt`) 发送到你指定的聊天窗口（`thread.id`）里。
        2.  **`run = client.beta.threads.runs.create(...)`**：
            *   你告诉助手：“我已经把问题放到聊天窗口了，现在请你开始工作，处理一下这个聊天窗口里的新消息，并给出你的回答。” `assistant.id` 指定了哪个助手来处理。
        3.  **`while run.status != "completed": ...`**：
            *   OpenAI 的助手处理问题需要时间（可能要搜索文件、思考、生成回答）。这个 `while` 循环是一个等待机制。它会反复地检查助手的“工作状态”（`run.status`）。
            *   只要状态不是 `"completed"`（完成），它就会继续检查，并且打印当前状态（例如 `in_progress` 表示正在进行中）。
            *   一旦状态变为 `"completed"`，说明助手已经完成工作，循环就 `break`（停止）了。
        4.  **`messages = client.beta.threads.messages.list(...)`**：
            *   助手工作完成后，我们去你指定的聊天窗口（`thread.id`）里，把**所有**的消息（包括你的问题和助手的回答）都取出来。
        5.  **`for data in messages.data: ...`**：
            *   循环遍历这些消息，然后把每条消息的文本内容（`data.content[0].text.value`）打印出来。`content[0].text.value` 看起来有点复杂，这是因为消息的内容可以是多种类型（比如文本、图片），而且可能有多条，所以要这样一层一层地去取到具体的文字信息。

### 积木7：使用助手进行问答
```python
get_response_from_assistant(assistant, thread, "哪篇论文介绍了Transformer架构？论文链接是什么？")
```
*   **作用：** 调用我们之前定义好的函数，真正地向助手提问。
*   **小白比喻：** 就像你拿着你的“问答流程自动化”脚本，然后对它说：“请你用这个 `assistant` 助手，在这个 `thread` 聊天窗口里，问这个问题：‘哪篇论文介绍了Transformer架构？论文链接是什么？’”。
*   **运行结果：**
    *   你会看到打印出多条 `Run status: in_progress`，这表示助手正在思考和处理中。
    *   最后，当助手完成工作后，会打印出 `Run status: completed`。
    *   接着，会打印出对话中的所有消息，首先是助手对你问题的回答（它会从 `论文介绍.pdf` 中检索信息来回答），然后是你的原始问题。

---

**总结一下整个流程：**

1.  **准备工具：** 导入 `OpenAI` 库，创建 `client` 遥控器。
2.  **上传资料：** 把你的 PDF 文件上传到 OpenAI 的云端，得到一个文件 ID。
3.  **雇佣专家：** 创建一个智能 `assistant` 助手，告诉它用哪个大脑 (`model`)，它的名字 (`name`)，它的职责 (`instructions`)，给它能查文件的能力 (`retrieval` tool)，并告诉它查哪个文件 (`file_ids`)。
4.  **开启对话：** 创建一个 `thread` (聊天窗口) 来记录你和助手的对话。
5.  **搭建问答机制：** 定义一个 `get_response_from_assistant` 函数，这个函数封装了“发送问题 → 助手工作 → 等待 → 获取答案”的完整流程。
6.  **开始提问：** 调用 `get_response_from_assistant` 函数，然后助手就会根据你上传的 PDF 文件来回答你的问题啦！
