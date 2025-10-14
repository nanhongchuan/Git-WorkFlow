# 65-Output Parser：从模型输出里提取 JSON

## 一、Output Parser 的功能与作用

**核心作用：**
1. 给模型下达指令，让模型按照指定格式输出内容。  
2. 解析模型的输出，从中提取目标信息。  

常见格式包括：
- 逗号分隔列表  
- JSON（更易解析，可直接转为字典、列表或类实例）

---

## 二、使用场景举例

假设我们经营一个书籍点评网站，拥有大量未整理的书籍介绍。  
目标：让 AI 从描述中提取出以下信息：
- 书名（Book Name）
- 作者（Author Name）
- 题材（Genres）

输出应为符合预期结构的 **JSON** 数据。  
若字段名或数据类型不符合要求，会导致解析失败（例如，类型不是字符串或列表）。

---

## 三、LAN Chain 的解析器：`PydanticOutputParser`

`PydanticOutputParser` 能：
- 指挥 AI 按照指定格式输出。
- 根据模式验证并解析生成的数据。

它依赖的是 Python 的 **Pydantic** 库，用于**数据模型验证与解析**。  
会根据类型提示确保：
- 字段存在；
- 字段值类型正确；
- 符合格式规范。

---

## 四、环境准备

需要安装并导入模块：
```python
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from typing import List
```

说明：
- `BaseModel`：创建数据模型的基类（相当于数据说明书）。
- `Field`：为字段提供额外信息（描述、验证条件）。
- `List`：用于指定列表类型。

---

## 五、定义数据模型

以书籍信息为例，定义一个 `BookInfo` 类：

```python
class BookInfo(BaseModel):
    book_name: str = Field(description="书籍名称")
    author_name: str = Field(description="作者名称")
    genres: List[str] = Field(description="书籍题材列表")
```

说明：
- 类型定义格式：`字段名: 类型`
- 可以使用 `Field` 的 `description` 参数为 AI 提供字段意义，帮助理解输出要求。

---

## 六、创建解析器实例

用定义好的数据模型，创建 `PydanticOutputParser`：

```python
parser = PydanticOutputParser(pydantic_object=BookInfo)
```

实现两大功能：
1. 指导模型输出符合格式要求的 JSON；
2. 将模型输出解析为 `BookInfo` 实例。

---

## 七、查看解析指令

使用：

```python
parser.get_format_instructions()
```

解析器会自动生成格式说明，教模型如何按照数据模式输出。  
无需手动撰写复杂的 JSON 格式提示，解析器会替你完成这一步。

---

## 八、构造提示模板（ChatPromptTemplate）

使用 `ChatPromptTemplate` 创建消息模板：

```python
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个图书信息提取助手。{instructions}"),
    ("user", "{book_description}")
])

formatted_prompt = prompt.invoke({
    "instructions": parser.get_format_instructions(),
    "book_description": "《活着》是余华创作的小说，讲述了中国农村家庭的悲欢离合。"
})
```

---

## 九、传入模型并获取输出

将构造好的提示传给模型：

```python
response = model.invoke(formatted_prompt)
print(response)
```

输出结果应为：
- 字段名与 `BookInfo` 模型一致；
- 值类型符合定义（字符串或字符串列表）。

---

## 十、解析模型输出

模型输出通常是 JSON 字符串，不便直接使用。  
可调用解析器的 `parse` 方法（或 `parse_response`）：

```python
book_info = parser.parse(response)
print(book_info)
```

此时，JSON 会自动转换为 `BookInfo` 的实例对象。  
可以像操作对象一样方便地访问字段：

```python
print(book_info.book_name)
print(book_info.author_name)
print(book_info.genres)
```

---

## 十一、总结

**`PydanticOutputParser` 的优势**
1. 自动指挥 LLM 输出正确结构；
2. 自动验证字段与类型；
3. 自动将结果转为类对象；
4. 极大便利结构化信息提取任务。

---

## 十二、延伸学习

课程文件中提供本节对应的 Jupyter Notebook 示例。  
可用于复现与实验练习。

---

✅ **你学会了吗？**  
通过 `PydanticOutputParser`，你可以：
- 控制 AI 输出 JSON 格式；
- 自动解析并验证结果；
- 快速提取结构化数据，用于后续系统开发或展示。

---