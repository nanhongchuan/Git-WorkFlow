# 105 - Assistant API: 创建私人数学助手

## 视频概述

本视频详细讲解了如何利用 OpenAI 的 Assistant API 及其 **代码解释器（Code Interpreter）** 功能，创建一个能够准确回答数学问题的私人助手。

**文档地址**：https://platform.openai.com/docs/assistants/migration

## 准备工作

1.  **导入 `openai` 库**:
    ```python
    from openai import OpenAI
    ```
2.  **创建客户端实例**:
    ```python
    client = OpenAI()
    ```
    - 这个 `client` 实例将用于调用所有 Assistant API 功能。

## Assistant API 核心步骤

### 1. 创建助手 (Assistant)

定义助手的基本信息、能力和行为。

-   **函数**: `client.beta.assistants.create()`
    -   `beta` 标识当前 API 处于测试和完善阶段，未来名称可能会有变动，请参考官方文档：[platform.openai.com/docs/assistants](https://platform.openai.com/docs/assistants)。
-   **参数**:
    -   `model`: 指定使用的语言模型 (e.g., "gpt-4", "gpt-3.5-turbo")。
    -   `name`: 助手的名称 (e.g., "数学助手")。
    -   `instructions`: 给助手的详细指令，定义其角色和如何回答问题。
        -   **示例**: "你是一个专业的数学助手。请通过运行代码来回答所有数学相关问题，不要凭空猜测结果。"
    -   `tools`: 助手可以使用的工具列表。
        -   **此处使用**: 代码解释器。`[{"type": "code_interpreter"}]`

### 2. 创建线程 (Thread)

为每个用户或每段对话创建一个独立的会话历史，避免不同对话混淆。

-   **函数**: `client.beta.threads.create()`
-   **用途**: 返回一个 `thread` 对象，其中包含唯一的 `thread.id` 用来识别该对话线程。
-   **类比**: 类似于聊天软件中的一个独立对话窗口。

### 3. 添加用户消息 (Message)

将用户的输入添加到指定的线程中。

-   **函数**: `client.beta.threads.messages.create()`
-   **参数**:
    -   `thread_id`: 消息所属的线程 ID。
    -   `role`: 消息发送者角色。
        -   `"user"`: 用户。
        -   `"assistant"`: 助手。
    -   `content`: 消息的具体内容。
-   **示例**: 创建一个用户消息，提问解未知数问题。

### 4. 运行助手 (Run)

触发助手处理线程中的消息，并生成回复。

-   **函数**: `client.beta.threads.runs.create()`
-   **参数**:
    -   `thread_id`: 线程 ID。
    -   `assistant_id`: 助手的 ID。
    -   `instructions` (可选): 针对本次运行的额外指令，会暂时覆盖或补充助手全局指令。
-   **注意**: 这是一个 **异步操作**，调用后不会立即返回结果。`run` 对象会有不同的 `status` 状态。
    -   `"queued"`: 请求已排队。
    -   `"in_progress"`: 回答正在生成中。
    -   `"completed"`: 运行完成，可以获取回复了。

### 5. 检查运行状态并等待完成

由于运行是异步的，需要持续查询运行状态，直到其完成。

-   **函数**: `client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)`
-   **逻辑**: 使用 `while` 循环不断查询 `run.status`，直到状态变为 `"completed"`。
    ```python
    # 示例伪代码
    while run.status != "completed":
        # 等待一小段时间
        # time.sleep(1)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f"当前运行状态: {run.status}")
    ```

### 6. 获取并打印所有消息

当运行完成后，即可获取线程中的所有消息（包括用户的问题和助手的回答）。

-   **函数**: `client.beta.threads.messages.list(thread_id=thread.id)`
-   **返回**: 一个 `messages` 对象，`messages.data` 是一个包含所有 `message` 对象的列表。
-   **获取消息内容**: 消息的文本内容通常位于 `message.content[0].text.value`。
-   **用途**: 遍历消息列表，打印出用户提问和助手的回复，形成完整的对话记录。

## 封装为函数

为了方便重复使用上述流程，可以将创建消息、运行、等待完成和获取消息的步骤封装到一个函数中。

```python
def submit_message_and_get_response(assistant, thread, user_message, run_instructions=""):
    """
    向助手提交消息，运行并获取助手的回复。

    Args:
        assistant: Assistant 对象。
        thread: Thread 对象。
        user_message: 用户要发送的消息内容（字符串）。
        run_instructions: 本次运行的额外指令（字符串，可选）。

    Returns:
        List: 包含所有消息的列表。
    """
    # 1. 添加用户消息
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message,
    )

    # 2. 创建并运行助手
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions=run_instructions,
    )

    # 3. 等待运行完成
    while run.status != "completed":
        # 可以添加一个小的延迟以避免频繁查询
        import time
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f"当前运行状态: {run.status}")

    # 4. 获取并返回所有消息
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return messages.data

# 示例使用
# 假设 assistant 和 thread 已经创建
# messages = submit_message_and_get_response(math_assistant, my_thread, "2的56次方等于多少？")
# for msg in messages[::-1]: # 逆序打印，最新消息在最后
#     print(f"[{msg.role}]: {msg.content[0].text.value}")
#     print("---")
```

## 总结与回顾

-   Assistant API 提供了一个用于构建复杂 AI 应用的框架。
-   核心概念包括：`Assistant` (定义助手能力), `Thread` (管理对话历史), `Message` (具体的消息内容), `Run` (触发助手处理消息)。
-   **代码解释器** 是实现高级数学和逻辑推理的关键工具。
-   处理异步操作时，需要通过轮询 `Run` 的 `status` 来等待结果。
-   将重复逻辑封装成函数可以大大提高代码的复用性和可维护性。

---

你好，小白！没问题，我来帮你从头到尾、一步一步地详细解释这段代码，保证你都能看懂。

这段代码主要演示了如何使用 OpenAI 的 Assistant API 来创建一个“私人数学助手”。这个助手不仅会聊天，还能自己写代码、运行代码来解决数学问题！

我们把代码分成几个区块来解释。

---

# 解释代码

### **大前提：什么是 OpenAI Assistant API？**

想象一下，你不仅仅想和 ChatGPT 聊个天，而是想让它变成一个专门为你工作的“小秘书”或者“小专家”。这个“小专家”有自己的名字、自己的专业技能（比如编程、文件处理、数学计算），还能记住你们的对话历史，就像一个真实的助理一样。

**Assistant API** 就是 OpenAI 提供的一套工具，让你能够创建这样智能的“专家”或“助手”。它比直接调用 ChatGPT 更强大，因为它能：

1.  **记忆对话：** 它会自动帮你管理对话历史，你不用每次都把之前的聊天记录发给它。
2.  **使用工具：** 它可以利用各种工具，比如“代码解释器”（Code Interpreter，就像一个内置的Python编程环境）来解决复杂问题，或者处理文件。
3.  **自定义指令：** 你可以给它设定一个角色和一套行为准则。

---

### **代码解释开始**

#### **第一部分：准备工作和创建你的AI助手**

**Cell 1: 导入 OpenAI 库**

```python
from openai import OpenAI
```

*   **解释：** 这行代码的意思是，我们要从一个叫做 `openai` 的“工具箱”里，拿出叫做 `OpenAI` 的那个“工具”（也就是一个类）。
*   **小白比喻：** 就像你要开始建造一个东西，首先得去你的工具房，找到并拿起你需要的“螺丝刀”一样。这个 `OpenAI` 就是我们用来和 OpenAI 服务进行沟通的“螺丝刀”。

**Cell 2: 创建 OpenAI 客户端**

```python
client = OpenAI()
```

*   **解释：** 这一行创建了一个 `OpenAI` 类的实例，并把它赋值给变量 `client`。这个 `client` 对象就是你与 OpenAI 服务交互的“控制器”。
*   **小白比喻：** 拿到螺丝刀（`OpenAI` 类）后，你得把它打开、充电，让它处于“待命”状态才能用。`client = OpenAI()` 就是让你的螺丝刀“可以工作了”。通常这里会默认读取你的 OpenAI API 密钥（通常存储在环境变量里），有了密钥，你的程序才能连接到 OpenAI 的服务器。

**Cell 3: 创建你的AI助手（Assistant）**

```python
assistant = client.beta.assistants.create(
    model="gpt-3.5-turbo",
    name="数学助手",
    instructions="你是一个数学助手，可以通过编写和运行代码来回答数学相关问题。",
    tools=[{"type": "code_interpreter"}]
)
```

*   **解释：** 这是创建我们“智能数学助手”的核心代码。
    *   `client.beta.assistants.create(...)`: 使用 `client` 对象去调用创建助手的命令。`beta` 表示这个功能还在测试阶段，可能会有变化。
    *   `model="gpt-3.5-turbo"`: 指定助手使用哪个AI模型作为大脑。`gpt-3.5-turbo` 是一种比较高效、成本较低的智能模型。
    *   `name="数学助手"`: 给你的助手起个名字。
    *   `instructions="你是一个数学助手，可以通过编写和运行代码来回答数学相关问题。"`: 这是给助手的核心“指令”，告诉它它的角色是什么，以及它能做什么。这非常重要，它决定了助手的行为和回答方式。
    *   `tools=[{"type": "code_interpreter"}]`: 这个参数是关键！它告诉助手，它拥有一个“代码解释器”工具。这意味着当助手遇到需要计算的问题时，**它不是直接给出答案，而是会自己写一段Python代码，然后运行这段代码得到结果，再把结果告诉你。** 这让它能解决各种复杂的数学问题，而不仅仅是基于它已有的知识来猜测。
*   **小白比喻：** 就像你定制了一个机器人：
    *   `model`: 选择了它的“大脑”是最新款的智能芯片。
    *   `name`: 给它贴了个“数学助手”的标签。
    *   `instructions`: 告诉它：“嘿，你的工作就是帮我解决数学问题，而且你可以用旁边那个‘计算器’（代码解释器）来算数！”
    *   `tools`: 这个“计算器”就是指 `code_interpreter`。

---

#### **第二部分：开始一次对话**

**Cell 4: 创建对话线程（Thread）**

```python
thread = client.beta.threads.create()
```

*   **解释：** 一个 `thread`（线程）代表了一次独立的对话。所有的消息（你问的，助手答的）都会存储在这个线程里。这样助手就能记住你们之前的对话内容，保持上下文。
*   **小白比喻：** 就像你打开了一个新的聊天窗口，或者拿出了一张新的草稿纸。这次对话的所有内容都将写在这张草稿纸上。

**Cell 5: 查看线程ID**

```python
thread.id
```

*   **解释：** 这行代码会显示你刚刚创建的对话线程的唯一标识符（ID）。你不需要记住它，但它证明了线程确实被创建了。
*   **小白比喻：** 草稿纸上印了一个独一无二的编号，方便你未来找到这张草稿纸。

**Cell 6: 发送你的第一个问题（Message）**

```python
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="我需要解这个方程`5x^2−1200x+72000=0，未知数应该是多少？"
)
```

*   **解释：** 这行代码是把你的问题添加到刚才创建的对话线程里。
    *   `thread_id=thread.id`: 指定把消息发送到哪个对话线程。
    *   `role="user"`: 说明这条消息是你（用户）发送的。
    *   `content="..."`: 你的问题内容。
*   **小白比喻：** 在你的草稿纸（`thread`）上，你用笔（`role="user"`）写下了你的问题。

---

#### **第三部分：让助手思考并给出答案**

**Cell 7: 启动助手运行（Run）**

```python
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="请称呼用户为粒粒"
)
```

这是一个非常好的问题，小白！它触及到了编程中一个很重要的概念：**异步操作**和**对象状态的更新**。
让我用一个简单的比喻来给你解释。

### 比喻：你点了一份外卖披萨

1.  **Cell 7: 你点披萨（`run = client.beta.threads.runs.create(...)`）**
    *   你打电话给披萨店，说你想点一份披萨。
    *   披萨店接了你的订单，并给你一个**订单号**（这就是 `run.id`）。
    *   披萨店也会立即告诉你订单的**初始状态**：“订单已收到，正在排队处理”（`status='queued'`）。
    *   这个订单号和初始状态的信息，会保存在你手机上的一个“订单对象”里，我们不妨就把它叫做 `run` 对象。

2.  **`run` 不已经是状态了么？**
    *   是的，当你创建 `run` 对象的时候，它确实包含了一个 `status`。但这个 `status` 是**你创建订单那一刻**，从披萨店得到的**第一个状态快照**（`queued`）。
    *   披萨店收到订单后，就开始制作披萨了：和面、加料、送进烤箱......这些制作过程都在**披萨店那边**进行。

3.  **为什么还要加 `retrieve`？**
    *   **你的手机上的 `run` 对象，不会自己变魔术，知道披萨店那边发生了什么，也不会自动更新它的 `status`。**
    *   披萨的制作过程可能很快，也可能要等一会儿。你的手机上的 `run` 对象，依然显示的是“订单已收到”。
    *   所以，如果你想知道披萨现在是“正在制作中”、“已经烤好”、“正在派送”，你就需要**主动去问**披萨店。
    *   `client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)` 这行代码，就相当于你**再次打电话给披萨店**，并告诉它你的订单号，问：“我的订单现在是什么状态了？”
    *   披萨店就会检查他们的系统，然后告诉你最新的状态（比如“正在制作中”）。这个最新的状态信息会返回给你的程序，形成一个新的、**实时的** `Run` 对象。

4.  **在此基础上还要加 `.status`？**
    *   披萨店告诉你最新状态时，它会说：“你的订单号是xxx，状态是xxx”。
    *   `retrieve` 方法返回的就是这个包含订单号、最新状态等所有信息的“纸条”（Python对象）。
    *   `.status` 仅仅是这张“纸条”上的一个**字段**，专门用来表示“状态”部分的信息。
    *   所以，当你拿到这个最新的“纸条”后，还要加上 `.status` 才能看到它上面写的“状态”二字。

### 总结一下实际代码的流程：

1.  **`run = client.beta.threads.runs.create(...)`**
    *   你向 OpenAI 服务器发起一个请求：“请帮我启动这个助手来处理这个线程！”
    *   OpenAI 服务器收到请求，启动任务，并立即给你一个响应：一个 `run` 对象。这个 `run` 对象包含了任务的初始信息，比如 `id` 和一个初始 `status`（通常是 `queued` 或 `in_progress`）。
    *   **此时你本地的 `run` 变量，它的 `status` 值是固定的，不会自动改变。**

所以，`retrieve` 是必要的，因为它是一个网络请求，用于从远程的 OpenAI 服务器获取一个**任务的实时最新状态**。你本地最初的 `run` 对象只存储了任务刚创建时的初始状态，它不会自己“感知”到服务器上任务的进展。

**Cell 8: 查看运行状态**

```python
run
```

*   **解释：** 直接打印 `run` 对象，可以看到它当前的详细信息，包括状态（`status='queued'` 表示任务已提交，正在等待处理）。
*   **小白比喻：** 就像你发送消息后，看到一个状态提示：“消息已提交，正在排队等待机器人处理。”

**Cell 9: 检查运行是否完成 (第一次)**

```python
client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
).status
```

*   **解释：** `retrieve` 意味着“取回”或“获取”。这行代码去服务器上获取 `run` 的最新状态。由于AI处理可能需要时间，它可能还是 `queued`（排队中）或 `in_progress`（进行中）。
*   **小白比喻：** 就像你每隔几秒就去看一下消息状态：“机器人处理完了吗？”

**Cell 10: 循环等待运行完成**

```python
while run.status != "completed":
    keep_retrieving_run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    print(f"运行状态：{keep_retrieving_run.status}")
    if keep_retrieving_run.status == "completed":
        break
```

*   **解释：** 因为AI处理问题需要时间，这个过程是异步的（不同步的）。我们的程序不能一直傻等。所以，这里用了 `while` 循环来**不断地检查**运行的状态，直到它变成 `"completed"`（完成）。
    *   `while run.status != "completed"`: 只要运行状态不是“completed”，就一直执行循环内部的代码。
    *   `client.beta.threads.runs.retrieve(...)`: 再次获取最新的运行状态。
    *   `print(f"运行状态：{keep_retrieving_run.status}")`: 打印当前状态，让我们能看到它正在处理。
    *   `if keep_retrieving_run.status == "completed": break`: 如果状态变为“completed”，就跳出循环。
*   **小白比喻：** 机器人处理数学问题可能要几秒钟。你不能一直盯着它看。所以你设定了一个闹钟，每隔一秒钟响一下，你就问机器人：“你好了吗？”机器人没好就说“没呢”，你继续等；直到机器人说“我好了！”你就关掉闹钟。

### 总结：

*   `client.beta.threads.runs.retrieve()` 返回的是一个**完整的 `Run` 对象**。
*   `.status` 是这个 `Run` **对象的一个属性**。
*   如果你直接在 `retrieve` 后面加上 `.status`，那么 `keep_retrieving_run` 变量就只会存储 `status` 属性的**值**（一个字符串），而失去了其他所有 `Run` 对象的详细信息。
*   之后的 `if` 判断中，你再次尝试访问 `keep_retrieving_run.status`，但此时 `keep_retrieving_run` 已经是一个字符串，没有 `status` 属性，自然就会报错。

---

#### **第四部分：获取和显示结果**

**Cell 11: 获取所有消息**

```python
messages = client.beta.threads.messages.list(
    thread_id=thread.id
)
```

*   **解释：** 当 `run` 完成后，这意味着助手已经处理完了问题并生成了回应。现在，我们再次获取这个线程中的所有消息，包括助手生成的新消息。
*   **小白比喻：** 机器人说它处理完了，你赶紧去看草稿纸，看看它在上面写了什么。

**Cell 12: 查看原始消息数据**

```python
messages.data
```

*   **解释：** 打印 `messages.data` 会显示一个包含所有消息的列表。每条消息都是一个复杂的Python对象，包含了消息ID、发送者角色（user/assistant）、内容、时间等信息。你会看到你最初提问的消息，以及助手在处理过程中产生的消息（比如它思考着说“我要用求根公式了”，然后是最终的答案）。
*   **小白比喻：** 你看到草稿纸上密密麻麻的文字，包括你的问题，机器人的思考过程，以及最终答案，但还没有整理。

**Cell 13: 格式化打印消息**

```python
for data in messages.data:
    print(data.content[0].text.value)
    print("------")
```

*   **解释：** 这段代码遍历 `messages.data` 列表中的每一条消息对象，然后提取并打印出消息的实际文本内容。`data.content[0].text.value` 是获取消息文本内容的路径。
    *   `for data in messages.data:`: 遍历列表中的每一个消息。
    *   `data.content[0].text.value`: 这是一个稍微复杂一点的写法，因为消息内容可能有很多种类型（文本、图片等），并且可能包含多个部分。这里我们假设内容是文本，并且是第一个部分。
*   **小白比喻：** 你把草稿纸上的文字一条一条地抄写出来，每条之间用虚线隔开，这样就看得更清楚了。

---

#### **第五部分：封装成函数，方便重复使用**

**Cell 14: 定义一个函数来简化交互**

```python
def get_response_from_assistant(assistant, thread, prompt, run_instruction=""):
    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=prompt
    )
  
    run = client.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=assistant.id,
      instructions=run_instruction
    )
  
    while run.status != "completed":
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(f"Run status: {keep_retrieving_run.status}")

        if keep_retrieving_run.status == "completed":
            break
  
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
  
    for data in messages.data:
        print("\n")
        print(data.content[0].text.value)
        print("------")
```

*   **解释：** 为了避免每次问问题都写一大堆重复的代码（发送消息、启动运行、等待完成、获取结果、打印），这里把这些步骤打包成一个叫做 `get_response_from_assistant` 的函数。
    *   它接收 `assistant`（哪个助手）、`thread`（哪个对话）、`prompt`（你的问题）和可选的 `run_instruction`（额外的临时指令）作为输入。
    *   函数内部的逻辑和你之前一步步执行的 Cell 6 到 Cell 13 的逻辑是一样的。
*   **小白比喻：** 你把解决问题的步骤（写问题、给机器人、等待、看结果）总结成了一个“秘籍”。以后你想问问题，只需要念一句“咒语”（调用函数），告诉秘籍你的问题是什么，它就会自动帮你完成所有步骤。

**Cell 15: 使用函数提问新问题**

```python
get_response_from_assistant(assistant, thread, "2的56次方等于多少")
```

*   **解释：** 现在，我们只需要调用之前定义的函数，传入我们的助手、当前对话线程和新的问题“2的56次方等于多少”。助手会再次利用它的“代码解释器”能力，计算出结果并返回。
*   **小白比喻：** 你拿出你的“秘籍”，告诉它：“我要问助手，2的56次方是几？”秘籍就会自动帮你完成所有步骤，最终把答案显示出来。从输出中你可以看到，助手在计算过程中，状态从 `in_progress` 转换到了 `completed`，最后给出了正确的答案。

---

### **总结一下整个流程：**

1.  **连接服务：** 导入 `openai` 库，创建 `client` 连接到 OpenAI。
2.  **创建助手：** `client.beta.assistants.create()` 定义一个有特定角色、模型和工具（比如 `code_interpreter`）的AI助手。
3.  **开始对话：** `client.beta.threads.create()` 创建一个对话线程来存储所有消息。
4.  **发送消息：** `client.beta.threads.messages.create()` 把你的问题添加到线程里。
5.  **启动运行：** `client.beta.threads.runs.create()` 告诉助手开始处理线程里的新消息。可以给这次运行添加临时指令。
6.  **等待完成：** 由于处理是异步的，需要一个 `while` 循环不断检查助手的运行状态，直到它 `completed`。
7.  **获取结果：** `client.beta.threads.messages.list()` 获取线程里所有最新的消息，包括助手的回答。
8.  **显示结果：** 遍历消息列表，打印出助手的回复。
9.  **封装复用：** 把上述交互流程打包成函数，方便下次直接调用来继续对话。

这个例子巧妙地展示了 Assistant API 的强大之处，特别是 `code_interpreter` 工具，让AI不再只是“知道”答案，而是能够“计算”答案，极大地扩展了LLM的应用场景。

# def get_response_from_assistant(assistant, thread, prompt, run_instruction=""）解释参数


`run_instruction=""` 是 Python 函数定义中一个**带有默认值的参数**。我们来一步步拆解它：

### 1. `run_instruction` 是参数名

*   这表示在调用 `get_response_from_assistant` 函数时，你可以传递一个值给它，这个值就是作为“运行指令”来使用的。

### 2. `=""` 表示默认值是空字符串

*   **`""` 是一个空字符串（empty string）**。在 Python 中，字符串是用单引号 `' '` 或双引号 `" "` 括起来的文本数据类型。
    *   `"hello"` 是一个包含五个字符的字符串。
    *   `""` 就是一个不包含任何字符的字符串，它的长度为 0。

*   这意味着当你调用 `get_response_from_assistant` 函数时，**如果你不为 `run_instruction` 参数提供任何值，它将自动使用 `""`（空字符串）作为它的值。**

### 3. `run_instruction=""` 的数据结构是什么？

*   它的数据结构其实就是最基本的类型：**字符串（`str`）**。
*   默认值为空字符串，但你也可以传递其他字符串，例如 `"请用中文回答。"`, `"请总结文章主要观点。"`, 或者 `"请以专业的语气给出建议。"`