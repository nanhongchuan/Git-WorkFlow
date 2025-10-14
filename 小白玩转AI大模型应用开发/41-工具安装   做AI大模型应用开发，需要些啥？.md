# 41-工具安装   做AI大模型应用开发，需要些啥？

## 一、背景与工具清单

- 已具备（前置）：
  - Python 解释器
  - 代码编辑器（如 PyCharm、VS Code）
- 新增推荐安装：
  - Jupyter Notebook（基于网页的交互式计算环境，适合教学与实验）
- 课程使用场景：
  - 教学篇：主要使用 Jupyter Notebook
  - 项目开发篇：主要使用代码编辑器（PyCharm / VS Code 等）

## 二、为什么使用 Jupyter Notebook

1. 按单元格（Cell）运行，省时省钱  
   - 只需运行你改动或关注的那一小段代码，避免每次从头跑到尾。  
   - 调用大模型 API 通常按量计费，减少不必要的重复调用可节省费用与时间。

2. 交互式环境，更直观  
   - 与命令行模式相比，Notebook 能直接展示表达式结果；很多时候无需 `print` 也能看到输出。

3. 更丰富的展示与分享  
   - 支持 Markdown 标记语言，注释层级清晰，文档化程度高。  
   - 可导出为 HTML 等格式，分享后展示效果保持一致，便于他人直观理解。

## 三、安装 Jupyter Notebook

- Windows
  1. 打开命令提示符：开始菜单搜索 “cmd” 并打开。
  2. 安装命令：
     ```bash
     pip install notebook
     ```

- macOS / Linux
  1. 打开终端（Terminal）：macOS 可点击右上角放大镜搜索 “Terminal”。
  2. 安装命令：
     ```bash
     pip3 install notebook
     ```

- 启动与验证安装
  - 在命令行输入：
    ```bash
    jupyter notebook
    ```
  - 看到浏览器自动打开 Jupyter Notebook 页面即表示安装成功。

## 四、正确关闭 Jupyter Notebook（重要细节）

- 仅关闭浏览器标签页不等于关闭后台服务。  
- 回到启动它的命令行窗口，按下：
  - 通用：`Ctrl + C`
  - macOS / Linux：通常会提示是否确认关闭，输入 `y` 回车确认。
  - Windows：按下 `Ctrl + C` 即终止（一般无需再输入 `y`）。

## 五、使用建议与实践顺序

- 在 Notebook 中将代码拆成多个单元格：  
  - 修改提示词（prompt）或某段逻辑时，仅重跑相关单元格即可。
- 教学/实验阶段：优先使用 Notebook 进行快速迭代与可视化记录。  
- 项目落地阶段：回归编辑器与脚本方式，便于结构化管理与部署。

## 六、快速命令清单（便于复制）

```bash
# 安装（根据环境选择 pip 或 pip3）
pip install notebook
# 或
pip3 install notebook

# 启动
jupyter notebook

# 关闭（在启动的控制台/终端中）
Ctrl + C
# macOS/Linux 可能需要：
y 回车
```