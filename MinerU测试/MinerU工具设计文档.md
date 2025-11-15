# MinerU 文档解析工具设计文档

## 一、功能需求

### 1.1 核心功能
- 在侧边栏输入 MinerU API Token
- 支持批量上传多个文档（PDF等格式）
- 配置解析选项：是否开启公式识别、是否开启表格识别
- 提交文档到 MinerU 进行解析
- 查看解析任务状态
- 解析完成后可下载解析结果

### 1.2 用户界面
- **左侧边栏**：
  - MinerU Token 输入框
  - 公式识别开关（enable_formula）
  - 表格识别开关（enable_table）
  - 语言选择（默认中文 "ch"）
  
- **主页面**：
  - 多文件上传组件
  - 任务列表显示（文件名、状态、操作按钮）
  - 下载按钮（解析完成后显示）

## 二、技术架构

### 2.1 前端（Streamlit）
- 文件：`main.py`
- 组件：
  - `st.sidebar`：侧边栏配置
  - `st.file_uploader`：多文件上传
  - `st.button`：提交和下载按钮
  - `st.progress`：任务进度显示
  - `st.status`：任务状态展示

### 2.2 后端（Python）
- 文件：`mineru_utils.py`
- 主要函数：
  - `upload_files_to_mineru()`: 上传文件到 MinerU
  - `create_extract_task()`: 创建解析任务
  - `check_task_status()`: 查询任务状态
  - `download_result()`: 下载解析结果

## 三、API 调用流程

### 3.1 MinerU API 工作流程
1. **申请上传链接**：`POST /api/v4/file-urls/batch`
   - 请求参数：token, enable_formula, enable_table, files
   - 返回：batch_id, file_urls

2. **上传文件**：`PUT file_urls[i]`
   - 将本地文件上传到返回的 URL

3. **创建解析任务**：`POST /api/v4/extract/task`（如果需要）
   - 基于 batch_id 创建解析任务
   - 返回：task_id

4. **查询任务状态**：`GET /api/v4/extract/task/{task_id}`
   - 轮询任务状态直到完成
   - 返回：status, result_url

5. **下载结果**：`GET result_url`
   - 下载解析后的文档

### 3.2 数据流
```
用户上传文件 → 申请上传URL → 上传文件 → 创建任务 → 轮询状态 → 下载结果
```

## 四、实现细节

### 4.1 后端函数设计

#### `upload_files_batch(token, files, enable_formula, enable_table, language)`
- **功能**：批量上传文件到 MinerU
- **参数**：
  - `token`: MinerU API Token
  - `files`: 文件列表（Streamlit UploadedFile 对象）
  - `enable_formula`: 是否开启公式识别
  - `enable_table`: 是否开启表格识别
  - `language`: 文档语言（默认 "ch"）
- **返回**：`{"batch_id": str, "file_data": list}`

#### `create_extract_task(token, batch_id)`
- **功能**：基于 batch_id 创建解析任务
- **参数**：
  - `token`: MinerU API Token
  - `batch_id`: 批量处理 ID
- **返回**：`{"task_id": str, "status": str}`

#### `check_task_status(token, task_id)`
- **功能**：查询任务解析状态
- **参数**：
  - `token`: MinerU API Token
  - `task_id`: 任务 ID
- **返回**：`{"status": str, "result_url": str, "progress": float}`

#### `download_result(token, result_url, save_path)`
- **功能**：下载解析结果
- **参数**：
  - `token`: MinerU API Token
  - `result_url`: 结果下载链接
  - `save_path`: 保存路径
- **返回**：文件路径

### 4.2 前端状态管理

使用 `st.session_state` 存储：
- `tasks`: 任务列表
  ```python
  {
    "file_name": str,
    "batch_id": str,
    "task_id": str,
    "status": str,  # "pending", "processing", "completed", "failed"
    "result_url": str,
    "progress": float
  }
  ```

### 4.3 错误处理
- API 调用失败：显示错误信息
- 文件上传失败：重试机制或提示用户
- 任务查询超时：设置最大轮询次数

## 五、代码结构

```
main.py
├── 导入库
├── 页面标题和侧边栏配置
│   ├── Token 输入
│   ├── 公式识别开关
│   ├── 表格识别开关
│   └── 语言选择
├── 文件上传组件
├── 任务管理
│   ├── 提交任务按钮
│   ├── 任务列表显示
│   └── 下载按钮
└── 状态更新逻辑

mineru_utils.py
├── upload_files_batch()      # 批量上传文件
├── create_extract_task()     # 创建解析任务
├── check_task_status()       # 查询任务状态
└── download_result()          # 下载结果
```

## 六、使用说明

1. **配置 Token**：在左侧边栏输入 MinerU API Token
2. **设置选项**：选择是否开启公式识别和表格识别
3. **上传文件**：点击上传按钮，选择多个文档
4. **提交任务**：点击"开始解析"按钮提交任务
5. **查看状态**：页面会显示每个文件的任务状态
6. **下载结果**：解析完成后，点击"下载"按钮保存结果

## 七、注意事项

1. **API 限制**：注意 MinerU API 的调用频率限制
2. **文件大小**：大文件可能需要较长的处理时间
3. **异步处理**：任务解析是异步的，需要轮询状态
4. **临时文件**：注意清理临时上传的文件
5. **错误恢复**：建议实现任务状态的持久化存储

