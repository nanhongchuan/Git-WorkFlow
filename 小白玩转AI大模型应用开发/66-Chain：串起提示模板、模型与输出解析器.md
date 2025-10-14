# 66-Chain：串起提示模板、模型与输出解析器

## 一、背景与核心思想  
在前几节中，我们已经接触了以下三个核心组件：  
1. **聊天模型 (Chat Model)**  
2. **聊天提示模板 (Chat Prompt Template)**  
3. **输出解析器 (Output Parser)**  

无论是：
- `ChatPromptTemplate`、`FewShotChatMessagePromptTemplate` 等提示模板；
- `ChatOpenAI` 等聊天模型；
- `CommaSeparatedListOutputParser`、`PydanticOutputParser` 等输出解析器；  
它们都 **具备一个共同点：都实现了 `invoke` 方法**。

---

## 二、`invoke` 方法的设计理念

`invoke` 方法是 **LangChain 表达式语言**（LCEL）中通用的可调用接口。  
三类组件中 `invoke` 的输入输出关系如下：

| 组件 | 输入 | 输出 |
|------|------|------|
| Prompt Template | 输入变量的字典 | Prompt Value（提示值） |
| Chat Model | Prompt Value / 消息列表 | Chat Message（聊天响应） |
| Output Parser | Chat Message | 解析结果 |

因此，整个调用链可以理解为：

```
输入变量 → 提示模板 → 聊天模型 → 输出解析器 → 最终结果
```

从而实现 **层层调用** 或 **一次性调用形成完整链路**。

---

## 三、链式调用 (Chain) 思想

因为每个组件的输出是下一个组件的输入，所以可以用连续 `invoke` 调用的方式：

```python
result = output_parser.invoke(
    model.invoke(
        prompt_template.invoke(inputs)
    )
)
```

但这种层层嵌套写法较繁琐。LangChain 提供了更简洁的写法：**管道操作符 `|`**。

---

## 四、管道操作符 `|` 与 LCEL 表达式语言

通过 **管道语法**，可以更清晰地表达组件之间的流向关系。例如：

```python
chain = prompt | model | output_parser
```

这表示：
- 将提示模板的输出传递给模型；  
- 再将模型的输出传递给输出解析器。

这套写法被称为 **LangChain Expression Language (LCEL)**，能把多个组件串联成一条「链（Chain）」。

---

## 五、调用链的执行与参数传递

当我们定义好 chain 后，只需调用一次 `invoke` 即可执行整个流程：

```python
final_result = chain.invoke(inputs)
```

🧠 注意：
- `invoke()` 所需的参数就是传递给 **第一个组件** 的输入；
- 后续各组件自动接受前一组件的输出。

---

## 六、灵活组合与扩展

LangChain 的链式思想具有高度灵活性：
- 中间的 ChatModel 组件也可替换为其他模型类型；
- 提示模板与输出解析器都不是必须的；
- 可以自由组合出复杂的多步骤流程。

通过 **LCEL** 表达式语言，我们能够将复杂的上下游关系以清晰直观的形式展现出来。

---

## 七、小结

🔗 **Chain 的核心要义：**
- 统一的 `invoke` 接口  
- 组件的可组合性  
- 使用管道符 `|` 串联组件  
- 一次调用，完成端到端任务  

Chain 机制让模型调用流程更清晰、更模块化，是 LangChain 架构设计的核心优势。

---