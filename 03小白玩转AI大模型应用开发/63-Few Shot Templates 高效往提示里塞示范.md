# 63-Few Shot Templates 高效往提示里塞示范

## 一、概念与作用
- **小样本提示（Few-shot prompting）** 是一种让 AI 快速适应新任务的方式。  
- 通过提供**多个对话示例（human–AI 交互样例）**，让模型在推理时参考格式与风格。  
- 相较于微调（fine-tuning），这种方法：
  - **无需训练模型**
  - **成本低、灵活性高**
  - **可高效应用于不同任务**

---

## 二、为什么需要模板化
- 在多个示例（few-shot examples）中：
  - 虽然具体内容不同，但**消息结构一致**（如“用户提问—AI回答”）。
- 因此，这类示例的数据模式可用模板来统一生成。  

---

## 三、核心工具：`FewShotChatMessagePromptTemplate`
- 来自 `langchain.prompts` 模块
- 用于**高效构建小样本提示结构**。

### 参数说明
| 参数 | 说明 |
|------|------|
| `example_prompt` | 示例模板（prompt 模板），可插入动态变量 |
| `examples` | 示例内容列表。每个示例是一个 `dict`，键与模板变量名对应，值为具体样本数据 |

---

## 四、构建流程

### Step 1. 创建模板（`example_prompt`）
- 定义对话结构（human ↔ AI），示例模板可包含变量。  
- 示例（伪代码式说明）：

```python
example_prompt = ChatPromptTemplate.from_messages([
    ("human", "问题：{question}"),
    ("ai", "回答：{answer}")
])
```

> ⚠️ 注意：此模板用于**构建示范对话**，不是最终用户输入的提示！

---

### Step 2. 准备示例数据
- 将每个示例放入列表，结构如下：

```python
examples = [
    {"question": "我今年5岁，我多大？", "answer": "你5岁"},
    {"question": "我住在北京", "answer": "你来自北京市"}
]
```

---

### Step 3. 生成 Few-shot 模板
将上述两个变量传入构造函数：

```python
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples
)
```

这样就得到了一个可复用的小样本模板。

---

## 五、在完整 Prompt 中嵌入 Few-shot 模板
- 最终的 prompt 应该以“用户消息”结尾（不能是 AI 消息）。
- 可以使用 `ChatPromptTemplate.from_messages()` 将 few-shot 模板插入主模板：

```python
final_prompt = ChatPromptTemplate.from_messages([
    few_shot_prompt,
    ("human", "{input}")
])
```

---

## 六、调用模板生成实际消息

- 使用 `.invoke()` 方法，并传入动态变量（如用户输入）：

```python
prompt_value = final_prompt.invoke({"input": "请帮我计算我的年龄"})
```

- 得到的 `prompt_value` 包含 `messages` 属性，可查看完整生成的消息序列。  
  与手动写出的多条示例消息效果相同。  

---

## 七、扩展示例的高效方式
- 若需新增 Few-shot 示例，只需：
  - 在 `examples` 列表中追加新的字典；
  - 无需手动编写所有消息。  
- 模板方式极大节约了编写与维护时间。

---

## 八、模型调用与效果
- 将 `.messages` 传入模型的 `invoke` 或 `generate` 方法：
  - 模型会遵循 few-shot 示例的格式要求。
- 实例中，模型自动：
  - 在年龄后加上“岁”字；
  - 自动补全地名所属的省份；
  - 等效地学习了示例风格与细节。

---

## 九、总结
- **FewShotPromptTemplates 的优点：**
  - 构建输入效率高  
  - 批量扩展容易  
  - 结构清晰可维护  
- 是 few-shot prompting 实践中的重要工具。  

---

没问题！我们来一步步拆解这段代码，保证你这个“小白”也能彻底明白。

这个文件的标题是 **"03 Few Shot Prompt Templates _ 往提示里面塞例子"**，光看标题我们就能知道它的核心思想：**给AI（大语言模型）提供一些“例子”，让它向这些例子学习，从而更好地完成我们的任务。** 这就是所谓的“Few-Shot Prompting”（少样本提示）。

想象一下，你是一个师傅，要教徒弟（AI）做菜。你直接告诉他“做一道酸辣土豆丝”可能他做得不好。但如果你先给他看两道你做好的酸辣土豆丝（例子），并告诉他具体步骤和最终成品的样子，他学起来就快多了，也更容易做出符合你要求的菜。

这段代码就是用 LangChain 这个工具，来做“往提示里塞例子”这件事。

---

# 代码详解

#### 第一部分：导入必要的工具 (Cell 1)

```python
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate
```

*   `from langchain_openai import ChatOpenAI`:
    *   `LangChain` 是一个非常流行的 Python 框架，专门用来构建基于大语言模型（LLM）的应用。
    *   `ChatOpenAI` 是 LangChain 中用来连接 OpenAI 公司的聊天模型（比如 `gpt-3.5-turbo`, `gpt-4`）的工具。你可以把它理解为和 OpenAI 的 AI 聊天机器人沟通的桥梁。
*   `from langchain.schema import HumanMessage`:
    *   `HumanMessage` 代表一个人（用户）对 AI 说的话。在聊天模型中，对话是由一系列消息组成的，这些消息有不同的“角色”，比如人类（`Human`）和AI（`AI`）。
*   `from langchain.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate`:
    *   `Prompt`（提示）就是你写给 AI 的指令或问题。
    *   `PromptTemplate`（提示模板）像是一个填空题模板，预设了一些结构和变量，你可以填入具体内容后生成最终的提示。
    *   `ChatPromptTemplate` 是专门用来构建聊天对话形式的提示模板，支持不同的角色消息。
    *   `FewShotChatMessagePromptTemplate` 是今天的主角，它是一个特殊的提示模板，专门用于把“少量例子”嵌入到聊天提示中。

**总结 Cell 1:** 导入了和 OpenAI 聊天模型交互的工具，以及构建带有聊天消息和“少量例子”的提示模板的工具。

---

#### 第二部分：定义一个“例子”的结构 (Cell 2)

```python
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "格式化以下客户信息：\n姓名 -> {customer_name}\n年龄 -> {customer_age}\n 城市 -> {customer_city}"),
        ("ai", "##客户信息\n- 客户姓名：{formatted_name}\n- 客户年龄：{formatted_age}\n- 客户所在地：{formatted_city}")
    ]
)
```

*   `example_prompt`: 我们给这个变量起名叫 `example_prompt`，顾名思义，它用来描述一个**单独的例子**应该长什么样。
*   `ChatPromptTemplate.from_messages(...)`: 这里我们用聊天提示模板来定义这个例子。
*   `("human", "...")`: 这是一个人类（用户）发出的消息。它是一个字符串模板，里面有 `{customer_name}`、`{customer_age}`、`{customer_city}` 这样的**占位符**。这意味着在实际的例子中，这些 `{}` 里的内容会被真实数据替代。
    *   比如，当 AI 看到一个例子时，它会看到人类输入“格式化以下客户信息：\n姓名 -> 张三\n年龄 -> 27\n 城市 -> 长沙”。
*   `("ai", "...")`: 这是一个 AI 给出的回复消息。它也有 `formatted_name`、`formatted_age`、`formatted_city` 这些占位符，用来表示 AI 应该如何格式化信息。
    *   比如，AI 会看到它的回复是“##客户信息\n- 客户姓名：张三\n- 客户年龄：27岁\n- 客户所在地：湖南省长沙市”。

**总结 Cell 2:** 我们定义了一个**模板**，告诉 LangChain，当我们提供一个客户信息的“例子”时，这个例子的人类输入（`human`）应该是什么格式，以及对应的 AI 回复（`ai`）应该是什么格式。它就像一个表格的表头，定义了每列数据的含义。

---

#### 第三部分：准备实际的“例子”数据 (Cell 3)

```python
examples = [
    {
        "customer_name": "张三", 
        "customer_age": "27",
        "customer_city": "长沙",
        "formatted_name": "张三",
        "formatted_age": "27岁",
        "formatted_city": "湖南省长沙市"
    },
    {
        "customer_name": "李四", 
        "customer_age": "42",
        "customer_city": "广州",
        "formatted_name": "李四",
        "formatted_age": "42岁",
        "formatted_city": "广东省广州市"
    },
]
```

*   `examples`: 这是一个 Python 的列表（`[]`），里面包含多个字典（`{}`）。每个字典就是一个真实的“例子”。
*   每个字典里的键（比如 `"customer_name"`）都对应着 `example_prompt` 中定义的占位符的名字。
*   值（比如 `"张三"`）就是用来填充这些占位符的具体数据。
*   我们这里提供了两个例子，分别展示了如何把客户的姓名、年龄、城市格式化成我们想要的样子（比如，年龄加上“岁”，城市前面加上“省”）。

**总结 Cell 3:** 我们准备了两个**具体的数据示例**。这些例子会按照 `example_prompt` 定义的格式，被塞进最终给 AI 的提示中。这就像是按照表头（`example_prompt`）填写了两行数据。

---

#### 第四部分：创建“少样本提示模板” (Cell 4)

```python
few_shot_template = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)
```

*   `few_shot_template`: 这是我们创建的少样本提示模板。
*   `FewShotChatMessagePromptTemplate(...)`: 我们用这个类来创建一个特殊的模板。
*   `example_prompt=example_prompt`: 传入之前定义的**单个例子**的结构。它告诉 `FewShotChatMessagePromptTemplate` 每个例子应该如何被格式化。
*   `examples=examples`: 传入之前准备好的**实际例子数据**。它告诉 `FewShotChatMessagePromptTemplate` 有哪些具体的数据要作为例子。

**总结 Cell 4:** 这一步是把“例子模板”（`example_prompt`）和“实际例子数据”（`examples`）结合起来，生成一个**包含了这些例子**的提示模块。这个模块知道如何把每个例子渲染成一个 `human` 消息和 `ai` 消息对。

---

#### 第五部分：构建最终的提示模板 (Cell 5)

```python
final_prompt_template = ChatPromptTemplate.from_messages(
    [
        few_shot_template,
        ("human", "{input}"),
    ]
)
```

*   `final_prompt_template`: 这是我们最终要发给 AI 的完整提示的模板。
*   `ChatPromptTemplate.from_messages(...)`: 再次使用聊天提示模板。
*   `few_shot_template`: 把之前创建的**包含了所有例子**的模板放进来。这意味着，最终的提示会先包含我们的所有例子。
*   `("human", "{input}")`: 在所有的例子之后，接着是一个新的“人类”消息。这个 `{input}` 也是一个占位符，用来接收我们真正想让 AI 处理的**新问题或新数据**。

**总结 Cell 5:** 我们创建了一个**总的提示模板**。这个模板的思路是：
1.  首先把我们准备好的所有“示范例子”都放进去。
2.  然后放上我们**真正要问 AI 的问题**（或者要它处理的新数据）。
这样 AI 在回答新问题之前，就先看到了我们的“示范例子”，知道我们希望它以什么格式来回复。

---

#### 第六部分：填充并生成最终提示 (Cell 6)

```python
final_prompt = final_prompt_template.invoke({"input": "格式化以下客户信息：\n姓名 -> 王五\n年龄 -> 31\n 城市 -> 郑州'"})
```

*   `final_prompt_template.invoke(...)`: 这一步是“调用”提示模板，把占位符 `{input}` 替换成真实的值。
*   `{"input": "..."}`: 这里我们给 `input` 传递了一个新的客户信息：“王五，31岁，郑州”。

**总结 Cell 6:** 我们把需要 AI 处理的**新数据**填入到 `final_prompt_template` 中的 `{input}` 占位符里。现在， `final_prompt` 变量就包含了所有（例子 + 新问题）的完整提示，可以发给 AI 了。

---

#### 第七部分：查看生成的提示内容 (Cell 7)

```python
final_prompt.messages
```

*   `final_prompt.messages`: 这会打印出 `final_prompt` 这个对象里面实际包含的**一系列消息**。
*   **输出解释：**
    *   你会看到第一个 HumanMessage 和 AIMessage 对就是“张三”的例子。
    *   接着的第二个 HumanMessage 和 AIMessage 对就是“李四”的例子。
    *   最后是一个 HumanMessage，内容就是我们刚才输入的“王五”的新数据。

    这种结构正是我们想要的：AI 先看到前面两组示范的问答，然后才看到真正要求它回答的问题。这就像你给学生出了两道示范题和答案，然后出了第三道类似的题让他自己做。

**总结 Cell 7:** 我们可以看到 LangChain 已经把所有的例子都根据 `example_prompt` 的格式展开成了 `HumanMessage` 和 `AIMessage` 的对话对，并且把我们新的问题放在了最后。这是要发送给 AI 的**真实内容**。

---

#### 第八部分：调用大语言模型并获取回复 (Cell 8)

```python
model = ChatOpenAI(model="gpt-3.5-turbo")
response = model.invoke(final_prompt)
print(response.content)
```

*   `model = ChatOpenAI(model="gpt-3.5-turbo")`: 初始化我们的聊天模型连接。这里指定使用 OpenAI 的 `gpt-3.5-turbo` 模型。
*   `response = model.invoke(final_prompt)`: 把我们准备好的 `final_prompt` （包含了例子和新问题）发送给 `gpt-3.5-turbo` 模型，并得到 AI 的回复。
*   `print(response.content)`: 打印出 AI 模型的回复内容。

*   **预期输出：**
    ```
    ##客户信息
    - 客户姓名：王五
    - 客户年龄：31岁
    - 客户所在地：河南省郑州市
    ```
    你会发现 AI 成功地学习了例子中的格式（年龄加“岁”，城市前加“省”），并用相同的风格格式化了“王五”的信息。这就证明了 Few-Shot Prompting 的效果！

**总结 Cell 8:** 这一步是真正与 AI 交互。我们把包含了例子和新问题的完整提示发给 AI，AI 会根据前面看到的例子，模仿那种格式和风格来回答我们的新问题。

---

### 整体总结

这段代码演示了如何使用 LangChain 中的 **Few-Shot Prompt Templates** 来：
1.  定义你期望 AI 回答的**格式**（通过 `example_prompt`）。
2.  提供具体的**示范例子**（通过 `examples` 列表）。
3.  将这些例子和你的新问题结合起来，生成一个**完整的提示** (`final_prompt_template`)。
4.  将这个提示发送给大语言模型，让它根据例子来**模仿并完成新任务**。
