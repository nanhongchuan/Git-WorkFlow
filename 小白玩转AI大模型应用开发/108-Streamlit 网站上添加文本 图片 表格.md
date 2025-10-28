# 108-Streamlit 网站上添加文本 图片 表格

本节主要介绍如何在Streamlit空白网页上添加内容，了解常用组件。

1.  **项目准备与运行**
    *   **新建文件:** 新建一个空白的 `.py` 文件。
    *   **导入库:** 在文件开头导入 Streamlit 库，通常使用别名 `st`。
        ```python
        import streamlit as st
        ```
    *   **运行应用:** 在终端中输入 `streamlit run <你的代码文件路径>` 来运行 Streamlit 应用。
        ```bash
        streamlit run page.py
        ```
    *   **停止服务器:** 在运行 `streamlit run` 命令的终端中，按 `Ctrl + C` 即可终止网页服务器。

2.  **显示文本内容**
    *   **`st.write()` 函数 (通用显示器):**
        *   用于在网页上显示字符串、Markdown、Python数据结构等。
        *   **显示普通字符串:**
            ```python
            st.write("早上好，感叹号！")
            ```
        *   **显示 Markdown 格式文本:** 在字符串中使用 Markdown 语法。
            ```python
            st.write("## 这是一个二级标题")
            st.write("### 这是一个三级标题")
            ```
        *   **显示 Python 数据类型:** 可自动以简洁样式展示数字、列表、字典等。
            ```python
            st.write(123)
            st.write([1, 2, "hello"])
            st.write({"key": "value", "number": 42})
            ```
    *   **Streamlit "魔法命令":**
        *   无需调用 `st.write()`，直接将字符串或变量放在代码中，Streamlit 会自动将其显示在页面上（等同于 `st.write()`）。
        ```python
        "这是一个直接显示的字符串"
        my_number = 456
        my_number # 直接显示变量值
        ```
    *   **`st.title()` 函数 (网页大标题):**
        *   用于添加网页的主标题，支持 emoji。
        ```python
        st.title("我的第一个 Streamlit 应用 ✨")
        ```

3.  **添加图片**
    *   **`st.image()` 函数:**
        *   用于在网页上显示图片。
        *   **参数:** 第一个参数为图片路径（相对于你的 .py 文件），`width` 参数可选，用于指定图片宽度。
        ```python
        # 确保 project_folder/your_image.jpg 存在
        st.image("your_image.jpg", width=400)
        ```

4.  **添加表格 (需 Pandas)**
    *   **安装 Pandas 库:**
        *   Pandas 是一个强大的数据分析库，用于创建和处理表格数据 (DataFrame)。
        *   在终端中运行以下命令安装：
            ```bash
            pip install pandas
            ```
    *   **导入 Pandas:**
        ```python
        import pandas as pd
        ```
    *   **创建 Pandas DataFrame:**
        *   使用字典创建 DataFrame，字典的键作为列名，值作为包含数据的列表。
        ```python
        data_for_table = {
            '学号': [101, 102, 103, 104],
            '班级': ['一班', '二班', '一班', '三班'],
            '成绩': [95, 88, 92, 79]
        }
        df = pd.DataFrame(data_for_table)
        ```
    *   **显示交互式表格 (`st.dataframe()`):**
        *   显示功能丰富的交互式表格，支持排序、搜索、下载和全屏查看。
        ```python
        st.dataframe(df)
        ```
    *   **显示静态表格 (`st.table()`):**
        *   显示非交互式的静态表格，不带排序、搜索等功能。适用于不需要用户交互的简单数据展示。
        ```python
        st.table(df)
        ```

5.  **内容分隔**
    *   **`st.divider()` 函数:**
        *   在不同内容块之间添加一条水平分隔线，使页面结构更清晰。
        ```python
        st.divider()
        ```

6.  **开发效率提示**
    *   **自动检测与更新:** Streamlit 会自动检测源文件的变化。
    *   **手动刷新:** 页面右上角出现提示时，点击 "Rerun" 按钮可更新。
    *   **始终重新运行 (推荐):** 在页面右上角点击 "Always rerun"，之后每次保存代码改动，网页都会自动实时更新，无需手动刷新。

---