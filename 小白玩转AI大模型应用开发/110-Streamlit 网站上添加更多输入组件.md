# 110-Streamlit 网站上添加更多输入组件

#### 1. 概述

*   本指南将介绍 Streamlit 中更丰富的输入组件，以支持用户提供不同类型的信息，包括单选、多选、范围选择和文件上传。
*   所有组件的使用都遵循 Streamlit 的核心运行机制：用户交互会导致脚本从上到下重新运行。

#### 2. 项目设置与运行

*   **创建文件:** 新建一个 `.py` 脚本文件。
*   **导入库:** 在脚本开头导入 `streamlit` 库：
    ```python
    import streamlit as st
    ```
*   **运行应用:** 在终端中使用 `streamlit run your_app_name.py` 命令。

#### 3. 核心输入组件详解

---

##### 3.1. 单选按钮 (`st.radio`)

*   **用途:** 让用户从多个互斥选项中选择一个。
*   **函数:** `st.radio(label, options, index=0)`
*   **参数:**
    *   `label` (必填, 字符串): 对输入进行介绍的问题或说明。
    *   `options` (必填, 列表/元组): 包含所有可选项目的列表。
    *   `index` (可选, 整数或 `None`):
        *   `0` (默认值): 默认选中 `options` 列表中的第一个选项。
        *   其他整数: 默认选中对应索引的选项 (e.g., `index=1` 选中第二个)。
        *   `None`: 不设置默认选中项 (用户需手动选择)。
*   **返回值:** 用户当前选择的选项的字符串值。
*   **示例:**
    ```python
    gender = st.radio("请选择您的性别", ["男", "女", "其他"], index=1) # 默认选中"女"
    if gender:
        st.write(f"您选择了: {gender}")
    ```

---

##### 3.2. 单选下拉框 (`st.selectbox`)

*   **用途:** 当选项较多时，以下拉列表形式让用户从多个互斥选项中选择一个。
*   **函数:** `st.selectbox(label, options, index=0)`
*   **参数:**
    *   `label` (必填, 字符串): 对输入进行介绍的问题或说明。
    *   `options` (必填, 列表/元组): 包含所有可选项目的列表。
    *   `index` (可选, 整数): 默认选中对应索引的选项 (默认 `0`，即第一个)。
*   **返回值:** 用户当前选择的选项的字符串值。
*   **示例:**
    ```python
    contact_method = st.selectbox("偏好的联系方式", ["电子邮件", "电话", "短信"])
    if contact_method:
        st.write(f"您偏好的联系方式是: {contact_method}")
    ```

---

##### 3.3. 多选下拉框 (`st.multiselect`)

*   **用途:** 允许用户从多个选项中选择零个、一个或多个。
*   **函数:** `st.multiselect(label, options, default=None)`
*   **参数:**
    *   `label` (必填, 字符串): 对输入进行介绍的问题或说明。
    *   `options` (必填, 列表/元组): 包含所有可选项目的列表。
    *   `default` (可选, 列表): 默认选中的选项列表。
*   **返回值:** 一个列表，包含用户选择的所有选项的字符串值。如果用户未选择任何项，则返回空列表 `[]`。
*   **示例:**
    ```python
    fruits = st.multiselect("请选择喜欢的水果", ["苹果", "香蕉", "橙子", "葡萄"], default=["苹果"])
    if fruits:
        st.write("您选择了以下水果:")
        for fruit in fruits:
            st.write(f"- {fruit}")
    else:
        st.write("您没有选择任何水果。")
    ```

---

##### 3.4. 滑块 (`st.slider`)

*   **用途:** 让用户通过拖动滑块来选择一个数值，特别适用于选择范围内的值。
*   **函数:** `st.slider(label, min_value=0.0, max_value=100.0, value=None, step=None)`
*   **参数:**
    *   `label` (必填, 字符串): 介绍滑块所代表的数值。
    *   `min_value` (可选, 数字): 允许选择的最小值 (默认 `0.0`)。
    *   `max_value` (可选, 数字): 允许选择的最大值 (默认 `100.0`)。
    *   `value` (可选, 数字或元组): 滑块的初始默认值。如果是单个数字，则表示单点值；如果是元组 `(start, end)`，则表示范围选择。
    *   `step` (可选, 数字): 滑动一步所改变的数值 (默认取决于 `min_value` 和 `max_value` 的范围)。
*   **返回值:**
    *   如果 `value` 参数是单个数字，则返回用户选择的数字。
    *   如果 `value` 参数是元组 `(start, end)`，则返回一个包含用户选择范围 `(start, end)` 的元组。
*   **示例 (单值选择):**
    ```python
    volume = st.slider("调整音量", min_value=0, max_value=100, value=50, step=1)
    st.write(f"当前音量: {volume}")
    ```
*   **示例 (范围选择):** 滑块也可以用于选择一个范围，此时 `value` 应设置为一个包含起始和结束值的元组。
    ```python
    price_range = st.slider("选择价格区间", min_value=0, max_value=1000, value=(100, 500), step=10)
    st.write(f"您选择的价格区间是: ${price_range[0]} - ${price_range[1]}")
    ```

---

##### 3.5. 文件上传器 (`st.file_uploader`)

*   **用途:** 允许用户上传文件到Streamlit应用。
*   **函数:** `st.file_uploader(label, type=None)`
*   **参数:**
    *   `label` (必填, 字符串): 介绍文件上传器的作用。
    *   `type` (可选, 列表): 限制允许上传的文件类型。传入一个字符串列表，包含允许的文件扩展名 (e.g., `['png', 'jpg', 'pdf']`)。默认为 `None`，表示允许所有文件类型。
*   **返回值:**
    *   如果用户已上传文件，则返回 `UploadedFile` 类的一个实例。
    *   如果用户未上传文件，则返回 `None`。
*   **`UploadedFile` 实例的属性和方法:**
    *   `name`: 文件名 (字符串)。
    *   `type`: 文件的MIME类型 (字符串)。
    *   `size`: 文件大小 (字节)。
    *   `read()`: 读取文件内容作为字节字符串。
    *   `getvalue()`: 获取文件内容的字节流。
    *   `seek(offset)`: 移动文件指针到指定偏移量。
    *   `readline()`, `readlines()`: 读取文件行 (文本文件)。
*   **文件内容读取:**
    *   **文本文件 (如 `.txt`, `.py`):** 使用 `uploaded_file.read().decode('utf-8')` (或相应编码) 将字节内容解码为字符串。
    *   **二进制文件 (如图片):** 直接使用 `uploaded_file.read()` 获取字节数据，然后可用于图像处理、显示等。
*   **示例:**
    ```python
    uploaded_file = st.file_uploader("请上传图片文件", type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None:
        st.write(f"文件名: {uploaded_file.name}")
        st.write(f"文件大小: {uploaded_file.size} 字节")

        # 假设上传的是文本文件，可以读取内容并显示
        if uploaded_file.type == "text/plain" or uploaded_file.name.endswith('.py'):
            content = uploaded_file.read().decode('utf-8')
            st.text_area("文件内容:", content, height=300)
        # 如果是图片，可以显示图片
        elif uploaded_file.type.startswith('image/'):
            st.image(uploaded_file, caption="上传的图片", use_column_width=True)
    ```

---