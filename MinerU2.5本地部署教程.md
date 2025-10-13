# MinerU2.5本地部署教程


## 第一步：环境准备

在开始之前，我们需要确保系统环境配置正确。

### 1.1 检查系统环境

首先检查你的CUDA环境和GPU状态：

```bash
# 检查CUDA版本（需要CUDA 11.8或以上）
nvcc --version
# nvcc 是 NVIDIA CUDA Compiler 的缩写，它是NVIDIA提供的CUDA编译器工具

# 检查GPU状态和显存
nvidia-smi
# smi在NVDIA的语境下特指 NVIDIA System Management Interface
```

**重要提示**：如果你没有NVIDIA显卡，也可以使用CPU版本，只是速度会慢一些。

### 1.2 创建专用虚拟环境

为了避免依赖冲突，强烈建议创建独立的虚拟环境：

**方案一：默认路径创建**
```bash
# 创建Python 3.10环境
conda create -n mineru python=3.10
conda activate mineru
```

**方案二：自定义路径创建（推荐）**
```bash
# 指定安装路径（适合C盘空间不足的情况）
conda create --prefix=D:\Computer\Anaconda\envs\mineru python=3.10 
# --prefix 参数的含义是：指定路径前缀，设置安装路径的前缀部分
conda activate mineru
```

创建完成后，你会看到命令行前面出现 `(mineru)` 标识，说明环境激活成功。

## 🛠️ 第二步：安装MinerU

接下来我们开始正式安装MinerU。

### 2.1 GPU版本安装（有显卡推荐）

如果你有NVIDIA显卡，强烈推荐使用GPU版本，速度会快很多：

```bash
# 1. 安装包管理工具
pip install uv

# 2. 清理旧版本（防止冲突）
pip uninstall mineru -y
# -y 表示 "yes"，即自动确认卸载操作，无需手动输入 "y" 或 "yes" 来确认

# 3. 安装MinerU完整版本
uv pip install -U "mineru[core]" -i https://mirrors.aliyun.com/pypi/simple
# -U 含义：--upgrade 的简写，作用：升级已安装的包到最新版本
# -i 含义：--index-url 的简写，作用：指定 pip 安装包的镜像源

# 4. 安装PyTorch GPU版本（根据CUDA版本选择）
# CUDA 12.1用户
pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu121
```
### 2.2 验证安装

安装完成后，让我们验证一下是否安装成功：

```bash
# 查看版本信息
mineru --version

# 查看帮助信息
mineru --help
```

如果能正常输出版本号和帮助信息，说明安装成功了！


## 📥 第三步：下载模型文件

MinerU需要下载一些模型文件才能正常工作，这一步非常重要：

### 自动下载所有模型（推荐）

```bash
# 下载所有必要的模型文件（大约8-12GB）
mineru-models-download --model_type all
```

**注意事项：**
- 首次下载需要比较长的时间，请耐心等待
- 如果下载失败，可以多试几次

## ✅ 第四步：功能测试

模型下载完成后，我们来测试一下MinerU是否能正常工作：

### 4.1 准备测试文件

首先创建一个测试目录，并准备一些PDF文件：

```bash
# 创建测试目录
mkdir test_pdfs
mkdir test_output

# 将你要测试的PDF文件放到test_pdfs目录中
# 或者下载一些测试文件
```

### 4.2 基础功能测试

```bash
# 测试单个PDF文件解析（Pipeline模式，速度快）
mineru -p ./pdfs/demo1.pdf -o ./test_output/ --backend pipeline

# 如果你有NVIDIA显卡，可以启用GPU加速
mineru -p ./test_pdfs/your_file.pdf -o test_output/ --backend pipeline --device cuda
```

### 4.3 高精度模式测试

```bash
# VLM模式（精度更高，但速度较慢）
mineru -p ./pdfs/demo0.pdf -o test_output/ --backend vlm-transformers --device cuda

# CPU用户请用这个命令
mineru -p ./test_pdfs/your_file.pdf -o test_output/ --backend vlm-transformers --device cpu
```

### 4.4 批量处理测试

```bash
# 批量处理整个文件夹的PDF
mineru -p ./pdfs -o test_output/ --backend pipeline --batch-size 8
```

## 🌐 第五步：启动Web界面

MinerU还提供了一个友好的Web界面，让我们可以通过浏览器来使用：

### 5.1 启动Web服务

```bash
# 确保在正确的环境中
conda activate mineru

# 启动Web界面服务
mineru-gradio --server-port 8080
```

### 5.2 访问Web界面

启动成功后，在浏览器中访问：**http://localhost:8080**

你将看到一个漂亮的Web界面，可以直接上传PDF文件进行解析！

### 5.3 常见问题解决

**如果Web界面启动失败，可以尝试以下解决方案：**

1. **更换端口**：
```bash
# 尝试使用其他端口
mineru-gradio --server-port 7860
```

2. **重置网络配置**（Windows用户）：
```bash
# 以管理员身份运行命令提示符，依次执行：
netsh winsock reset
netsh int ip reset
ipconfig /flushdns
```
重启电脑后再次尝试启动。

## 🚀 第六步：在线体验与开源地址

**无需本地部署，直接在线体验MinerU**：  
  [MinerU在线体验地址](https://mineru.net)

**查看/参与开源项目，获取最新代码与文档**：  
  [MinerU GitHub开源仓库](https://github.com/opendatalab/MinerU)

## 🎯 总结

恭喜你！现在你已经成功部署了MinerU2.5文档解析大模型。

### 📋 使用要点回顾

1. **环境激活**：每次使用前记得激活环境
   ```bash
   conda activate mineru
   ```

2. **两种使用方式**：
   - **命令行模式**：适合批量处理和脚本自动化
   - **Web界面模式**：适合日常使用，界面友好

3. **性能建议**：
   - 有NVIDIA显卡的用户优先使用GPU模式
   - 大文件建议使用Pipeline模式（速度快）
   - 需要最高精度时使用VLM模式

4. **常用命令**：
   ```bash
   # 单文件处理
   mineru -p your_file.pdf -o output/ --backend pipeline --device cuda
   
   # 批量处理
   mineru -p pdf_folder/ -o output/ --backend pipeline --batch-size 4
   
   # 启动Web界面
   mineru-gradio --server-port 8080
   ```

---

# NVDIA 5090 vLLM部署指令

目前最新版的 MinerU 仅对 vLLM 进行了支持，请确保在 Linux 环境下进行部署，Windows 用户请确保已经安装好了 WSL 2，同时确保 Cuda 已经正确安装。换句话说，你至少要有20系以上的 N 卡，才能体验最新版。

## 第一步：环境准备

首先打开 Windows 终端，或在 Windwos 下运行 WSL2。

1. **建立虚拟空间**

```bash
 conda create -n <空间名> python=3.12 -y
```

2. **激活虚拟运行空间**

```bash
conda activate <空间名>
```

3. **安装uv工具**
```bash
pip install --upgrade uv
```

## 第二步：安装vLLM

> vLLM 不同版本对`PyTorch FlashAttention`、`Transformer`的版本对应有明确的要求。以下命令为针对 NVIDIA 5090系显卡运行的指令。

4. **在已经激活的虚拟空间中部署vLLM**

```bash
# 安装 flash-attn 工具
pip install https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.2/flash_attn-2.8.2+cu12torch2.7cxx11abiFALSE-cp312-cp312-linux_x86_64.whl
```

5. **安装 vLLM 与对应的 Pytorch 版本**

```bash
# 安装 vLLM 0.10.0 版本与 Pytorch 版本
pip install vllm==0.10.0 --extra-index-url https://download.pytorch.org/whl/cu128
```

6. **安装 Transformers**

```bash
pip install --upgrade transformers==4.53.2
```

## 第三步：部署 MinerU

7. **部署 MinerU**

```bash
uv pip install mineru[all]
```

8. **确认版本号出现，表示部署成功**

```bash
mineru -v
```

9. **启动 vLLM 后端**

```bash
mineru-vllm-server --port <端口号>
# 首次启动需要下载模型，请确保国际网络畅通
```
> **提示**：当出现下列三行代码，表示 MinerU vLLM 后端启动成功
```bash
[INFO: Started server process [606]
[INFO: Waiting for application startup.
[INFO: Waiting Application startup complete
```
**不要关闭该终端**：重新打开一个终端，Windows 系统无需重开 WSL2 窗口，可以使用自带的 CMD 终端。

10. **创建 MinerU 轻量级客户端运行空间**

```bash
conda create -n <空间名> python=3.12 -y
```

11. **激活轻量级客户端虚拟运行空间**

```bash
conda activate <空间名>
```

12. **安装 MinerU 轻量级客户端**

```bash
uv pip install mineru
```

13. **命令行处理模式**

```bash
# 需保持 MinerU vLLM 后端处于
运行状态
mineru -p <input_path> -o <output_path> -b vlm-http-client -u http://127.0.0.1:30000
```