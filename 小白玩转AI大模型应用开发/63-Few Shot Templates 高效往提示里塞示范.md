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
- 来自 `langchain.prompts` 模块（文中写作 “feels hot chat message prompt template”）。  
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