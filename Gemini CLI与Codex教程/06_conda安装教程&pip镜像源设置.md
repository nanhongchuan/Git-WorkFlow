
**视频教程**：https://www.bilibili.com/video/BV1BFSJYEEj2
。

# 1. Miniconda 是什么
- 轻量级 Conda 发行版，仅包含 conda 和最小 Python 运行时。
- 核心优势：隔离环境、版本切换、依赖解析；适合数据科学、深度学习与多项目并行。

# 2. 下载与安装

## 官方与镜像链接
- 官方说明页：https://docs.anaconda.com/miniconda/
- 官方下载目录（全平台、全版本）：https://repo.anaconda.com/miniconda/
- 清华开源镜像站（镜像主页）：https://mirrors.tuna.tsinghua.edu.cn/
- 清华 Anaconda/Conda 镜像帮助（配置示例）：https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/
- 清华 Anaconda 镜像根目录（浏览镜像结构）：https://mirrors.tuna.tsinghua.edu.cn/anaconda/

可选（社区构建，默认 conda-forge，解析快）：
- Miniforge/Mambaforge：https://github.com/conda-forge/miniforge
- Releases 列表：https://github.com/conda-forge/miniforge/releases

## Windows 安装步骤
1) 在上面的官方目录或镜像找到适合你的安装器（通常选 Miniconda3-latest-Windows-x86_64.exe）。
2) 双击安装器 → Next → 同意协议 → 选择安装路径。
   - 建议不要装在 C 盘（后期环境会占空间），可用 D:\Dev\miniconda3 或 C:\ProgramData\miniconda3。
3) “Advanced Options”保持默认（不勾选 Add to PATH，避免污染全局 PATH；后续用 conda init 即可）。
4) 完成后，开始菜单搜索 “Anaconda Prompt (Miniconda3)” 打开，或在安装目录打开终端验证。

## 安装后快速验证
在“Anaconda Prompt (Miniconda3)”或命令行执行：
```
conda --version
conda info
```
能显示版本与配置信息，即安装成功。

# 3. 初始化 Shell（必做）
让当前终端识别 conda activate。根据你用的终端执行一次相应命令：

- CMD:
```
conda init cmd.exe
```

- PowerShell:
```
conda init powershell
```

- Git Bash 或 WSL Bash:
```
conda init bash
```

执行后关闭并重开对应终端，再测试：
```
conda activate
conda deactivate
where conda
```

注意：不建议手动改系统 PATH 来“激活 conda”。如确需在 .bat 中使用而不做 init，可调用激活脚本：
```
call "C:\Users\你的用户名\miniconda3\Scripts\activate.bat"
```

# 4.（可选）手动配置 PATH 的三条路径
仅当你非常明确需要手动 PATH 时添加，且添加后要重开终端。按实际安装路径修改：

用户安装示例：
- C:\Users\你的用户名\miniconda3
- C:\Users\你的用户名\miniconda3\Scripts
- C:\Users\你的用户名\miniconda3\Library\bin

全局安装示例：
- C:\ProgramData\miniconda3
- C:\ProgramData\miniconda3\Scripts
- C:\ProgramData\miniconda3\Library\bin

再次提醒：优先使用 conda init，而非 PATH 直链。

# 5. 配置国内镜像（清华 TUNA）
推荐使用 .condarc 文件或 conda config 命令设置，能显著加速下载与解析。

## 方式 A：命令行设置（推荐）
```
conda config --set show_channel_urls true
conda config --set channel_priority strict

conda config --remove-key channels        2> NUL
conda config --remove-key default_channels 2> NUL
conda config --remove-key custom_channels  2> NUL

conda config --add default_channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --add default_channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
conda config --add default_channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2

conda config --add custom_channels conda-forge https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
conda config --add custom_channels pytorch     https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
conda config --add custom_channels nvidia      https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
```

## 方式 B：直接编辑 .condarc
编辑文件：C:\Users\你的用户名\.condarc，填入：
```
show_channel_urls: true
channel_priority: strict
channels:
  - defaults
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  nvidia: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
```

## 验证镜像是否生效
```
conda config --show-sources
conda config --show | findstr /i "default_channels custom_channels channel_priority show_channel_urls"
conda search python
```

## 恢复官方默认源（如需）
```
del %USERPROFILE%\.condarc
conda config --remove-key channels         2> NUL
conda config --remove-key default_channels 2> NUL
conda config --remove-key custom_channels  2> NUL
```

## 更新 conda 自身（建议）
```
conda update -n base conda
```

# 6. 创建与管理虚拟环境

## 创建环境（教程示例：名为 SD，Python 3.10.6）
```
conda create -n SD python=3.10.6 -y
```

## 激活/退出
```
conda activate SD
conda deactivate
```

## 查看/删除环境
```
conda env list
conda env remove -n SD
```

## 安装与查看包
- 在当前激活环境中安装：
```
conda install numpy pandas
```
- 指定环境安装：
```
conda install -n SD numpy pandas
```
- 搜索包：
```
conda search scipy
```
- 查看已装包：
```
conda list
```

## 推荐习惯
- 优先用 conda 安装能在 conda 源找到的包；找不到再用 pip。
- 需要 pip 时，先确保已激活对应 conda 环境。

# 7. pip 的国内镜像（常用但易忽略）
- 临时使用清华镜像：
```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
```
- 永久设置 pip 源（当前用户）：
```python
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn

# 将 pip 的默认包下载源配置为清华大学的 PyPI 镜像（https://pypi.tuna.tsinghua.edu.cn/simple），并且信任这个镜像的主机（pypi.tuna.tsinghua.edu.cn），以确保在下载包时不会因 SSL 证书问题而中断。å
```
- 查看与还原：
```
pip config list
pip config unset global.index-url
```

# 8. 一键进入环境并运行脚本（.bat 模板）

已执行过 conda init 的常见模板：
```
@echo off
REM 进入指定环境，运行脚本
conda activate SD
python launch.py
pause
```

未执行 conda init，需要手动调用激活脚本：
```
@echo off
call "C:\Users\你的用户名\miniconda3\Scripts\activate.bat"
conda activate SD
python launch.py
pause
```

安装在 ProgramData 时：
```
@echo off
call "C:\ProgramData\miniconda3\Scripts\activate.bat"
conda activate SD
python launch.py
pause
```

# 9. 常见问题与排查

- 现象：conda 不是内部或外部命令/activate 无效  
  处理：
  - 在你使用的终端里运行对应的 `conda init ...`，重启终端。
  - 或在批处理脚本中 `call ...\Scripts\activate.bat`。
  - 检查位置：`where conda`。

- 现象：镜像配置不生效/下载慢  
  处理：
  - 查看生效的配置与来源：`conda config --show-sources`。
  - 确认 `.condarc` 在用户主目录且内容正确。
  - 启用严格优先级：`conda config --set channel_priority strict`。
  - 需要时清缓存再试：`conda clean -a -y`。

- 现象：环境或包解析冲突  
  处理：
  - 更换环境名或放宽/更改包的版本约束。
  - 新建一个干净环境逐步安装定位问题。
  - 查看详细求解日志：`conda install <pkg> -vvv`。

- 现象：pip 与 conda 混用导致冲突  
  处理：
  - 尽量用 conda 安装能在 conda 源找到的包。
  - 必须使用 pip 时，先激活环境，优先设置 pip 镜像，最后可用 `conda list`/`pip list` 核对版本。

- 快速自检命令
```
conda info
conda info --envs
python --version
pip --version
```

# 10. macOS/Linux 简要说明

- 安装器：从 https://repo.anaconda.com/miniconda/ 下载对应 .sh 安装脚本（如 Miniconda3-latest-MacOSX-x86_64.sh / Miniconda3-latest-Linux-x86_64.sh）。
- 安装：
```
bash Miniconda3-latest-<OS>-x86_64.sh
# 按提示选择安装目录，默认在 ~/miniconda3
```
- 初始化当前 Shell（zsh 或 bash）：
```
conda init zsh   # macOS 默认 zsh
# 或
conda init bash
```
- 其他步骤（镜像、创建环境、安装包）与 Windows 基本一致；.condarc 路径为 ~/.condarc。

# 11. 一次复制即用的最小命令集（Windows）

按顺序执行（PowerShell 或 CMD）：
```
conda init powershell
# 若使用 CMD: conda init cmd.exe

# 关闭并重开终端后：
conda config --set show_channel_urls true
conda config --set channel_priority strict
conda config --remove-key channels        2> NUL
conda config --remove-key default_channels 2> NUL
conda config --remove-key custom_channels  2> NUL
conda config --add default_channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --add default_channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
conda config --add default_channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
conda config --add custom_channels conda-forge https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
conda config --add custom_channels pytorch     https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
conda config --add custom_channels nvidia      https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud

conda update -n base conda -y

conda create -n SD python=3.10.6 -y
conda activate SD
python --version
pip --version

# 示例安装常用包
conda install numpy pandas -y
```