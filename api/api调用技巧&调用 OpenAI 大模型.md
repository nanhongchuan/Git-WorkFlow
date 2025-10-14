# 📝 Python 调用 MinerU API 知识点整理

## 1️⃣ requests.post() 基础

* `requests.post()` 用于向服务器发送 **POST 请求**。
* POST 请求特点：

  * 发送数据给服务器（如提交任务、上传文件）。
  * 与 GET 请求不同，GET 是获取数据。

### 参数结构

```python
requests.post(url, headers=..., json=...)
```

| 参数        | 含义     | 是否固定      | 说明                         |
| --------- | ------ | --------- | -------------------------- |
| `url`     | 目标接口地址 | ✅ 固定函数参数名 | 可以通过位置参数传，也可以写 `url=...`   |
| `headers` | 请求头信息  | ✅ 固定函数参数名 | 告诉服务器请求类型和认证信息             |
| `json`    | 请求体数据  | ✅ 固定函数参数名 | 自动将 Python 字典转成 JSON 字符串发送 |

> 注意：`url`、`headers`、`json` 是 **requests.post() 函数的固定参数名**，
> 但是你前面赋值的变量名（如 `api_address`、`my_header`、`task_info`）可以自己取。

---

## 2️⃣ 变量定义（可自定义）

```python
api_address = "https://mineru.net/api/v4/extract/task"   # API 地址
my_header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}  # 请求头
task_info = {
    "url": "https://cdn-mineru.openxlab.org.cn/demo/example.pdf",
    "is_ocr": True,
    "enable_formula": False
}  # 请求体内容
```

* 这些变量名可以自由命名，但在 `requests.post()` 中要对应传入正确位置或关键字参数。

---

## 3️⃣ `data=` vs `json=`

| 参数      | 数据发送格式                                       | 使用场景                              |
| ------- | -------------------------------------------- | --------------------------------- |
| `data=` | 表单格式（`x-www-form-urlencoded`）                | 传统 Web 表单提交                       |
| `json=` | JSON 格式，自动加 `Content-Type: application/json` | 调用现代 RESTful API（如 MinerU、OpenAI） |

> 对 MinerU API，一定要用 `json=`，否则服务器会报 400 错误。

---

## 4️⃣ 请求返回值 Response

调用 `requests.post()` 返回一个 `Response` 对象：

```python
res = requests.post(url, headers=header, json=data)
```

### 常用方法

| 方法                   | 功能                             |
| -------------------- | ------------------------------ |
| `res.status_code`    | 打印 HTTP 状态码（200 成功、4xx/5xx 出错） |
| `res.json()`         | 将服务器返回的 JSON 字符串转换为 Python 字典  |
| `res.json()["data"]` | 取出返回字典中的 `data` 部分（实际结果内容）     |
| `res.text`           | 如果返回不是 JSON，可查看原始字符串内容         |

---

## 5️⃣ 调用 API 的完整示例

```python
import requests

token = "你的API Token"
api_address = "https://mineru.net/api/v4/extract/task"
my_header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
task_info = {
    "url": "https://cdn-mineru.openxlab.org.cn/demo/example.pdf",
    "is_ocr": True,
    "enable_formula": False,
}

res = requests.post(url=api_address, headers=my_header, json=task_info)

# 查看结果
print(res.status_code)       # HTTP 状态码
print(res.json())            # 整个返回内容
print(res.json()["data"])    # 只看 data 部分
```

---

## 6️⃣ 参数传递小技巧

1. **位置参数**：

```python
requests.post(api_address, headers=my_header, json=task_info)
```

第一个参数默认就是 `url`，可省略 `url=`。

2. **关键字参数**（推荐，更清晰）：

```python
requests.post(url=api_address, headers=my_header, json=task_info)
```

3. **注意顺序**：

* 关键字参数后不能再跟位置参数，否则会报错。

---

## 7️⃣ 调试小技巧

* 打印请求体看看实际发送的内容：

```python
print(res.request.body)
```

* 如果返回不是 JSON，可先打印：

```python
print(res.text)
```

---

✅ **总结一句话**

* `requests.post()` 发送 POST 请求，`url`、`headers`、`json` 是固定参数名，
* 前面定义的变量名可自由命名；
* `json=` 一般用于发送 JSON 请求体，是调用现代 API 的标准方式；
* Response 对象提供状态码、返回内容和解析 JSON 的方法。

---

| 名称                     | 性质                        | 代表作                                       | 关系说明                                              |
| :--------------------- | :------------------------ | :---------------------------------------- | :------------------------------------------------ |
| **Google**             | 科技巨头公司                    | 论文《Attention is All You Need》 (2017)      | 他们首次提出了“Transformer”架构，是现代大语言模型（如 GPT、BERT）的基础。   |
| **Transformer (模型架构)** | 一种**神经网络结构**              | 用于 NLP、视觉、多模态任务                           | GPT、BERT、T5、PaLM、Gemini 等都基于这个架构。                 |
| **Hugging Face**       | 一家 AI 公司                  | 开源库 `transformers`、`datasets`、`diffusers` | 把 Transformer 架构实现成**易用的 Python 库**，并建立了一个社区模型平台。 |
| **`transformers` 库**   | Hugging Face 出品的 Python 库 | 支持 100+ 模型（BERT、GPT、T5、LLaMA 等）           | 让开发者一句代码就能使用各种预训练模型。                              |


# 调用 OpenAI 大模型（GPT-4 / GPT-5）的标准 Python 代码


## ✅ 一、先确保你已经：

1. 在 [OpenAI 官网](https://platform.openai.com/api-keys) 申请了一个 **API Key**
2. 安装了 `openai` Python SDK

在终端运行以下命令安装：

```bash
pip install openai
```

---

## ✅ 二、Python 调用示例

```python
from openai import OpenAI

# 创建客户端（用你的 API key）
client = OpenAI(api_key="你的API密钥")

# 调用模型（gpt-4 或 gpt-5）
response = client.chat.completions.create(
    model="gpt-4o-mini",  # 可以换成 "gpt-4o" 或 "gpt-5"
    messages=[
        {"role": "system", "content": "你是一个知识渊博的AI助手。"},
        {"role": "user", "content": "帮我解释一下量子纠缠。"}
    ]
)

# 输出结果
print(response.choices[0].message.content)
```

---

## ✅ 三、可选：通过环境变量存储 API Key（更安全）

不要把 key 写进代码里，可用以下方式：

### 设置环境变量（macOS / Linux）

```bash
export OPENAI_API_KEY="你的API密钥"
```

### 然后在代码中这样写：

```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

---

## ✅ 四、如果你想调用不同类型的接口：

| 功能   | 示例函数                                   | 说明            |
| ---- | -------------------------------------- | ------------- |
| 聊天模型 | `client.chat.completions.create()`     | 生成文本（对话）      |
| 文本补全 | `client.completions.create()`          | 类似旧版 GPT-3 接口 |
| 图像生成 | `client.images.generate()`             | 生成图片          |
| 语音识别 | `client.audio.transcriptions.create()` | 转写音频（语音 → 文本） |

---