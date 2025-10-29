 # 113-Streamlit 创建多页面网站

**Streamlit 创建多页面网站知识点**

*   **目的：** 当Streamlit应用内容庞大或功能模块多时，通过创建多页面网站，实现用户在不同页面间跳转，提高应用的可管理性和用户体验。

*   **实现步骤：**
    1.  **选择主页（Main Page）：** 从现有的Streamlit `.py` 应用文件中，选择一个作为网站的启动页面和主页。
    2.  **创建并命名 `pages` 文件夹：** 在项目根目录下（与主页文件同级），创建一个名为 `pages` 的新文件夹。
    3.  **移动其他页面：** 将所有其他非主页的Streamlit应用文件（`.py` 扩展名）移动到新创建的 `pages` 文件夹中。
    4.  **重要命名约定：** `pages` 文件夹的名称必须**严格为 `pages`** (小写)。

*   **运行与效果：**
    1.  **运行方式：** 只需运行选定的主页文件（例如 `streamlit run main_page.py`），无需单独运行 `pages` 文件夹内的文件。
    2.  **自动生成侧边栏：** Streamlit会自动在应用界面左侧生成一个侧边栏导航。
    3.  **页面导航：** 侧边栏会列出 `pages` 文件夹中所有`.py`文件的名称（默认为文件名，可配置显示名称），作为可点击的页面链接。用户点击即可在不同页面间无缝跳转。

*   **核心特性 - 会话状态 (Session State) 的持久性：**
    1.  **跨页保留：** 在多页面应用中，只要用户不关闭当前的浏览器标签页/会话，Streamlit的会话状态 (`st.session_state`) 会持续存在。
    2.  **数据连贯性：** 这意味着即使在不同页面之间跳转，通过 `st.session_state` 保存的数据（如用户输入、临时配置等）也会被保留和访问。
    3.  **重要意义：** 强调了会话状态在多页面应用中保持数据一致性和用户体验的重要性。

---

# Python 导入不同路径下文件的规则总结

### ✅ 一、同一文件夹下

可以直接导入：

```python
from utils import generate_script
```

---

### ✅ 二、不同文件夹下

如果文件结构是：

```
project/
├── app/
│   └── main.py
└── utils/
    └── abc/
        └── helper.py
```

在 `main.py` 中导入 `helper.py` 的函数写法如下：

```python
from utils.abc.helper import generate_script
```

> 启动程序时需在项目根目录执行，例如：
>
> ```bash
> cd project
> python app/main.py
> ```

---

### ✅ 三、临时修改路径导入（不推荐但可用）

```python
import sys
sys.path.append('../utils')
from helper import generate_script
```

---

### ✅ 四、相对导入（仅适用于包内模块）

若 `app` 和 `utils` 都有 `__init__.py` 文件，则可写：

```python
from ..utils.helper import generate_script
```

> 运行方式需为包模式：
>
> ```bash
> python -m app.main
> ```

---

💡**总结一句话：**

> 同目录可直接导入；不同目录需写清模块路径（推荐 `from package.module import func`），或在运行时修改 `sys.path`。


# `utils` 介绍

在 Python 项目里，`utils` 是 **“utilities（工具）”** 的缩写，
一般表示 **工具函数模块** 或 **工具包**，专门放那些“通用的小功能函数”。

> `utilities`  **->**   /juːˈtɪlətiz/

---

### 📘 通俗理解：

`utils.py` 或 `utils/` 文件夹，就像一个“工具箱”，
里面放的不是业务逻辑，而是你在项目里**到处可能会用到的小函数**。

---

### 🧰 举几个常见例子：

| 功能类别  | 函数示例                               | 说明          |
| ----- | ---------------------------------- | ----------- |
| 文件操作  | `read_json()`, `save_csv()`        | 读取或保存文件     |
| 字符串处理 | `clean_text()`, `slugify()`        | 统一清洗或格式化字符串 |
| 日志工具  | `log_info()`, `log_error()`        | 封装打印或日志写入   |
| 网络请求  | `fetch_data(url)`                  | 封装 HTTP 请求  |
| 时间处理  | `get_timestamp()`, `format_date()` | 统一日期格式      |

---

### 💡 举个例子

假设 `utils.py` 里写：

```python
def clean_text(text):
    return text.strip().lower()
```

在 `main.py` 中：

```python
from utils import clean_text

content = " Hello World "
print(clean_text(content))  # 输出：hello world
```

---

✅ **一句话总结：**

> `utils` 通常是放“可复用的小工具函数”的文件或包，用来让主程序更简洁、模块化。


