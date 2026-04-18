- Linux 终端操作知识点总结
- Conda 的一些基本操作命令（字母含义举例）
- curl VS wget 简明对比
- Jupyter Notebook 安装与启动简洁教程
- 本地文件传到云端服务器
- 对比：`vi` vs `nano`
- 总结表：Ubuntu 中不同工具创建虚拟环境后的程序与依赖存储位置
- 【案例】一次搞定：Jupyter Notebook 安装 + 配置远程访问 全流程
- Ubuntu 上升级显卡驱动
- Ubuntu 查看与关闭进程操作总结
- Ubuntu 分区与文件系统概念总结


## 1️⃣✅ Linux 终端操作知识点总结

### 一、基本文件与目录操作命令

| 命令          | 作用                   |
| ----------- | -------------------- |
| `ls`        | 列出当前目录下的文件与文件夹       |
| `cd 目录名`    | 进入指定目录               |
| `cd ..`     | 返回上一级目录              |
| `cd`（不加参数）  | 回到用户主目录              |
| `pwd`       | 显示当前所在目录的绝对路径        |
| `mkdir 目录名` | 新建目录(创建文件夹）           |
| `touch 文件名` | 创建空文件                |
| `rm 文件名`    | 删除文件                 |
| `rm -r 目录名` | 删除目录及其内容             |
| `mv 源 目标`   | 移动文件或重命名             |
| `cp 源 目标`   | 复制文件或目录（加 `-r` 表示递归） |
| `ls`                | 列出当前目录下的**非隐藏文件**               |
| `ls -a`             | 显示**所有文件**，包括以 `.` 开头的**隐藏文件**  |
| `ls -l`             | 以**详细列表形式**显示（权限、大小、修改时间等）      |
| `ls -la` 或 `ls -al` | 显示**所有文件 + 详细信息**，这两个顺序都可以      |
| `ls -lh`            | 显示详细信息，文件大小用**人类可读格式**（如 KB、MB） |
| `ls -lt`            | 按**修改时间排序**（最新的排最上面）            |
| `ls -ltr`           | 按时间排序 + **反向显示**（最旧的排最上面）       |
| `ls -R`             | **递归**显示子目录中的内容                 |
| `ls -d */`          | 只列出当前目录下的**文件夹**（不显示文件）         |
| `ls -S`             | 按**文件大小排序**（从大到小）               |
| `ls --color=auto`   | 显示带颜色的文件名（通常系统默认设置为自动）          |

---

### 二、路径表示法
| 符号      | 含义说明                                                           |
| ------- | -------------------------------------------------------------- |
| `.`     | 当前目录（current directory）                                        |
| `..`    | 上一级目录（parent directory）                                        |
| `./`    | 当前目录，常用于执行当前目录下的脚本（如 `./run.sh`）                               |
| `/`     | 根目录（absolute path 起点），比如 `/home/user` 表示从系统根目录开始               |
| `~`     | 当前用户的**主目录（home 目录）**，通常是 `/home/用户名`，比如 `~` 可能是 `/home/ubuntu` |
| `~/xxx` | 表示主目录下的某个子目录，比如 `~/Downloads` 就是 `/home/用户名/Downloads`         |


---

### 三、终端操作快捷键与技巧

| 快捷键 / 操作     | 功能说明                 |
| ------------ | -------------------- |
| `Tab`        | 自动补全命令、文件或目录名        |
| `Ctrl + C`   | 终止当前运行的命令            |
| `Ctrl + L`   | 清屏（等同于 `clear`）      |
| `Ctrl + A`   | 将光标移动到当前行首           |
| `Ctrl + E`   | 将光标移动到当前行末           |
| `Ctrl + U`   | 删除从光标到行首的内容          |
| `Ctrl + K`   | 删除从光标到行尾的内容          |
| `Ctrl + R`   | 搜索历史命令（模糊匹配）         |
| `↑ / ↓`（方向键） | 浏览历史命令               |
| `history`    | 查看命令历史               |
| `!数字`        | 执行对应编号的历史命令（如 `!88`） |

---

| 场景                       | `Ctrl + C` 的效果     | `Ctrl + D` 的效果         |
| ------------------------ | ------------------ | ---------------------- |
| 正在运行一个程序（如 `ping`）       | **终止程序运行**，马上返回命令行 | 没有作用，不会终止，程序继续运行       |
| 使用 `cat > file.txt` 输入内容 | 无法结束输入，直接中断（内容不保存） | **正常结束输入**，文件写入完成      |
| 在终端中直接按（什么都没输入）          | 没有任何效果             | **退出终端**（等于 `exit`）    |
| 在 Python 交互环境（REPL）      | 终止当前输入，回到新的一行      | 退出 Python 交互环境（关闭解释器）  |
| 输入密码或命令时按下               | 中断整个输入（不会执行）       | 表示“我没有要输的内容”，结束输入/直接退出 |

---

### 四、命令组合与重定向

| 操作符  | 功能说明                  |
| ---- | --------------------- |
| `&&` | 多条命令连续执行，前一条成功后才执行下一条 |
| `>`  | 将输出重定向到文件（覆盖原文件）      |
| `>>` | 将输出追加到文件末尾            |

---

### 五、终端中常用快捷操作补充知识点

#### 1. `..` 表示上一级目录

在终端中，`..` 是一个特殊的路径标识，表示当前目录的上一级。例如：

```bash
cd ..
```

也可以连续使用：

```bash
cd ../..
```

表示向上返回两级目录。

---

#### 2. `./` 表示当前目录

`./` 表示当前所在目录，常用于执行当前目录下的脚本或程序：

```bash
./run.sh
```

等价于“从当前目录运行 `run.sh`”，而不是去系统 PATH 中查找。

---

#### 3. Tab 自动补全功能

在输入命令或路径时，可以按下 **Tab 键** 来自动补全：

* 如果有唯一匹配项，会自动补全；
* 如果有多个匹配项，按两次 Tab 会显示所有候选项。

例如：

```bash
cd Doc[TAB]    # 自动补全为 Documents/
```

---

#### 4. `Ctrl + C` 终止当前命令

如果你在终端执行了一个运行中的命令，但想中断它，可以按下：

```bash
Ctrl + C
```

该操作会立即终止当前正在运行的程序或命令。

---

#### 5. 上方向键 ⬆️ 查看历史命令

在终端中按下键盘上的 **↑（上方向键）** 可以浏览你之前执行过的命令，反复按可翻看更早的记录。

同样，**↓（下方向键）** 可以回到较新的历史命令。

---

#### 6. `Ctrl + L` 清屏

这个组合键的作用等同于执行 `clear` 命令，会清除终端中当前的显示内容，但不会退出终端或中断命令历史。

---

#### 7. `Ctrl + A` / `Ctrl + E` 移动光标

* `Ctrl + A`：将光标移动到当前行的开头
* `Ctrl + E`：将光标移动到当前行的末尾
  常用于快速编辑命令行中的长命令。

---

#### 8. `Ctrl + U` / `Ctrl + K` 删除文本

* `Ctrl + U`：删除光标到行首的内容
* `Ctrl + K`：删除光标到行尾的内容
  非常方便修改输错的命令。

---

#### 9. `Ctrl + R` 反向搜索历史命令

按下 `Ctrl + R` 后，输入关键词即可搜索历史中执行过的命令，自动匹配显示。例如：

```
(reverse-i-search)`conda`: conda activate base
```

连续按 `Ctrl + R` 可搜索更多历史项。

---

#### 10. `history` 命令查看所有历史命令

输入：

```bash
history
```

即可列出所有历史执行的命令，并带有编号。可以通过如下方式快速执行某条命令：

```bash
!123   # 执行第 123 条历史命令
```

---

#### 11. `&&` 连接多个命令

可以将多个命令在一行中依次执行，前一条成功后再执行下一条：

```bash
mkdir test && cd test
```

---

#### 12. 使用 `>` 和 `>>` 重定向输出到文件

* `>`：覆盖写入文件
* `>>`：追加写入文件

示例：

```bash
ls > filelist.txt     # 将 ls 输出写入 filelist.txt（覆盖）
ls >> filelist.txt    # 将 ls 输出追加写入 filelist.txt
```

---

## 2️⃣✅Conda 的一些基本操作命令

#### **提问 1：** Conda 是什么？为什么在开发中会用到它？

**回答 1：** Conda 是一个开源的包管理系统和环境管理系统。它可以帮助你轻松地安装、运行和升级软件包（例如，Python 库），以及创建、管理和切换独立的环境。在开发中，Conda 主要用于隔离不同项目所需的依赖包，避免版本冲突，并保持开发环境的整洁和可复用。

#### **提问 2：** 如何查看当前 Conda 的版本？

**回答 2：** 可以使用以下命令查看 Conda 的版本信息：

```bash
conda --version
```

或

```bash
conda -V
```

#### **提问 3：** 如何更新 Conda 到最新版本？

**回答 3：** 可以使用以下命令更新 Conda：

```bash
conda update conda
```

建议定期更新 Conda，以获取最新的功能和修复。

#### **提问 4：** 如何查看当前 Conda 管理的所有环境？

**回答 4：** 可以使用以下命令列出所有已创建的 Conda 环境：

```bash
conda env list
```

或

```bash
conda info --envs
```

输出会显示环境的名称以及它们在文件系统中的路径。当前激活的环境会有一个星号 `*` 标记。

#### **提问 5：** 如何创建一个新的 Conda 环境？

**回答 5：** 可以使用以下命令创建一个新的 Conda 环境，并指定 Python 版本（可选）：

```bash
conda create --name <环境名称> [python=<版本号>]

#或

conda create -n <环境名称> [python=<版本号>]
```

例如，创建一个名为 `myenv` 的 Python 3.9 环境：

```bash
conda create --name myenv python=3.9
```

如果不指定 Python 版本，Conda 会安装其默认的 Python 版本。

---

#### 字母含义举例

```bash
# 创建一个名为 mineru 的 Conda 虚拟环境，并指定使用 Python 3.12 版本，-y 表示自动确认无需手动输入
conda create -n mineru 'python=3.12' -y

# 激活刚才创建的 mineru 虚拟环境
conda activate mineru

# 从 [PyPI（Python Package Index）](https://pypi.org) 上下载并安装 `magic-pdf` 包的最新版，并包括其 `[full]` 可选功能模块中的所有依赖。安装 magic-pdf 库及其所有可选功能（例如带 OCR、解析增强等），用于处理 PDF 文件
pip install -U "magic-pdf[full]"

# 根据当前目录下的 requirements.txt 文件安装所有依赖包
pip install -r requirements.txt

#这个是正确的
pip install -r -U requirements.txt 
#这个也是正确的
pip install -r requirements.txt --upgrade
```

`-y`, `--yes`：自动确认所有提示，相当于对所有确认提示回答 "yes"。

---

`pip install -U "magic-pdf[full]"`中 

`-U`：是 `-upgrade` 的缩写，表示升级包到最新版本。如果包已经安装，则升级到最新版本；如果包没有安装，则安装最新版本。

---

`[full]`：这是一个可选的特征或依赖项集，称为 "extras"。在这个例子中，`[full]` 表示安装 `magic-pdf` 包的完整功能集，包括所有额外的依赖项或特征。

`full`：是一个特征名称，可能代表包的完整或全部功能。具体含义取决于包的作者如何定义这个特征。

---

`-r` 是一个选项，代表 **"read"** ，意思是 "从文件中读取"，它告诉 `pip` 从指定的文件中读取包名和版本号。

在大多数情况下，你可以省略 `-r` 选项。但使用 `-r` 选项可以明确指定文件类型和行为，所以在某些情况下，使用 `-r` 选项可能更安全、更明确。

例如，如果你有一个名为 **requirements.txt** 的文件，但它不是一个标准的 **requirements** 文件，使用 `-r` 选项可以强制 `pip` 将其视为 **requirements** 文件。

---

#### **提问 6：** 如何激活和停用 Conda 环境？

**回答 6：**

  * **激活环境：** 使用以下命令激活一个已创建的 Conda 环境：

    ```bash
    conda activate <环境名称>
    ```

    激活后，你的命令行提示符通常会显示当前激活的环境名称。

    例如，激活名为 `myenv` 的环境：

    ```bash
    conda activate myenv
    ```

  * **停用环境（返回 base 或默认环境）：** 使用以下命令停用当前激活的 Conda 环境：

    ```bash
    conda deactivate
    ```

#### **提问 7：** 如何在激活的环境中安装软件包？

**回答 7：** 激活相应的 Conda 环境后，可以使用以下命令安装软件包：

```bash
conda install <软件包名称1> [软件包名称2] ...
```

例如，在激活的环境中安装 `numpy` 和 `pandas`：

```bash
conda install numpy pandas
```

Conda 会自动解决依赖关系并安装所需的软件包。你也可以指定安装特定版本的软件包，例如：

```bash
conda install numpy=1.20
```

#### **提问 8：** 如何从特定的 Conda 渠道安装软件包？

**回答 8：** Conda 软件包通常从默认的 `anaconda` 渠道获取。如果需要从其他渠道安装（例如 `conda-forge`），可以使用 `-c` 选项：

```bash
conda install -c <渠道名称> <软件包名称>
```

例如，从 `conda-forge` 渠道安装 `scikit-learn`：

```bash
conda install -c conda-forge scikit-learn
```

#### **提问 9：** 如何列出当前激活环境中已安装的软件包？

**回答 9：** 在激活的 Conda 环境中，可以使用以下命令列出所有已安装的软件包及其版本：

```bash
conda list
```

#### **提问 10：** 如何导出和导入 Conda 环境的依赖？

**回答 10：**

  * **导出环境依赖：** 可以将当前环境的依赖导出到一个 YAML 文件中，方便在其他地方重建相同的环境：

    ```bash
    conda env export > environment.yml
    ```

    这会将当前环境的所有包及其版本信息保存到名为 `environment.yml` 的文件中。

  * **导入环境依赖（从 YAML 文件创建环境）：** 可以使用导出的 `environment.yml` 文件创建一个新的 Conda 环境：

    ```bash
    conda env create -f environment.yml
    ```

    Conda 会读取 `environment.yml` 文件中的依赖信息，并尝试安装相应的软件包。

#### **提问 11：** 如何移除一个已安装的软件包？

**回答 11：** 在激活的 Conda 环境中，可以使用以下命令移除一个或多个已安装的软件包：

```bash
conda remove <软件包名称1> [软件包名称2] ...
```

例如，移除 `numpy`：

```bash
conda remove numpy
```

可以使用 `--force` 选项强制移除，但通常不建议这样做，因为它可能破坏环境的依赖关系。

#### **提问 12：** 如何移除一个不再需要的 Conda 环境？

**回答 12：** 可以使用以下命令移除一个已创建的 Conda 环境：

```bash
conda env remove --name <环境名称>
```

例如，移除名为 `myenv` 的环境：

```bash
conda env remove --name myenv
```

Conda 会提示你确认是否要移除该环境。

**总结：**

Conda 提供了一套强大的命令行工具来管理软件包和开发环境。掌握 `conda --version`, `conda update`, `conda env list`, `conda create`, `conda activate`, `conda deactivate`, `conda install`, `conda list`, `conda env export`, `conda env create`, `conda remove`, `conda env remove` 等基本命令，能够有效地管理你的 Python 项目依赖和开发环境。记住在操作环境和软件包之前，最好先激活相应的 Conda 环境。

---

#### 提问 13:   Python 解释器和 Miniconda 和 Anaconda 的关系和作用

| 名称          | 是否包含Python解释器 | 是否自带常用库 | 是否自带conda | 体积大小 | 主要用途   |
| ----------- | ------------- | ------- | --------- | ---- | ------ |
| Python官方解释器 | 是             | 否       | 否         | 小    | 纯粹运行代码 |
| Miniconda   | 是             | 否       | 是         | 中    | 自定义安装  |
| Anaconda    | 是             | 是       | 是         | 大    | 开箱即用   |

---

```bash
`docker compose up -d`
```

使用 Docker Compose 启动服务，并以守护进程模式运行。

`docker compose up` 是用来启动基于 `docker-compose.yml` 文件定义的多个容器服务的命令。

`-d` 是单词 `"detach"` 的缩写。该参数表示以后台模式（守护进程模式）运行容器，运行后不会占用当前终端。

---

当然，以下是**凝练版总结**，保留了你需要的关键对比和例子，适合复制保存：

---

## 3️⃣🧾 curl vs wget 简明对比（适合新手）

### 🌐 curl：用于访问网页或与服务器交互（比如 API 请求）

### 📥 wget：用于直接下载文件（简单快捷）

---

### ✅ 基本用法示例

| 操作        | 命令                                              |
| --------- | ----------------------------------------------- |
| curl 下载文件 | `curl https://example.com/file.txt -o file.txt` |
| wget 下载文件 | `wget https://example.com/file.txt`             |

---

### 📊 功能对比表

| 功能/区别      | curl                | wget           |
| ---------- | ------------------- | -------------- |
| 默认显示内容到屏幕？ | ✅ 是                 | ❌ 否（自动下载）      |
| 自动保存文件名？   | ❌ 否，需要 `-o` 参数      | ✅ 是，直接保存       |
| 支持 API 请求？ | ✅ 支持 GET/POST/PUT 等 | ❌ 不支持          |
| 递归下载整站？    | ❌ 不支持               | ✅ 支持 `wget -r` |
| 推荐用途       | 调试接口、获取网页数据、模拟登录    | 下载文件、镜像网站      |

---

### 🎯 使用建议

* **下载文件就用 `wget`** 👉 简单省事
* **访问网页/调用 API 用 `curl`** 👉 功能全面

---

## 4️⃣🔹 **Jupyter Notebook** 中最常用的快捷键指令

（按 `Esc` 进入，蓝边框）

| 快捷键               | 功能说明              |
| ----------------- | ----------------- |
| `A`               | 在当前单元格上方插入新单元格    |
| `B`               | 在当前单元格下方插入新单元格    |
| `D` `D`           | 删除当前单元格           |
| `Z`               | 撤销删除单元格           |
| `Y`               | 将单元格转为代码模式        |
| `M`               | 将单元格转为Markdown模式  |
| `R`               | 将单元格转为Raw模式       |
| `C`               | 复制当前单元格           |
| `X`               | 剪切当前单元格           |
| `V`               | 粘贴到下方             |
| `Shift` + `V`     | 粘贴到上方             |
| `S`               | 保存当前Notebook      |
| `Enter`           | 进入编辑模式            |
| `Shift` + `Enter` | 运行当前单元格并跳到下一个     |
| `Ctrl` + `Enter`  | 运行当前单元格           |
| `Alt` + `Enter`   | 运行当前单元格并在下方插入新单元格 |

---

### 🔹 **编辑模式（Edit Mode）**

（按 `Enter` 进入，绿边框）

| 快捷键               | 功能说明       |
| ----------------- | ---------- |
| `Ctrl` + `Enter`  | 运行当前单元格    |
| `Shift` + `Enter` | 运行并跳转下一单元格 |
| `Tab`             | 代码补全或缩进    |
| `Shift` + `Tab`   | 查看函数参数/帮助  |
| `Ctrl` + `/`      | 注释/取消注释当前行 |
| `Esc`             | 返回命令模式     |

---

### ✅ 小技巧补充：

* 多选单元格：按住 `Shift` + 点击其他单元格
* 查找替换：在编辑模式中按 `Ctrl` + `F`
* 启动命令面板：`Cmd/Ctrl` + `Shift` + `P`

---

### ✅**Windows / macOS / Linux** 的 **Jupyter Notebook 安装与启动简洁教程**

#### ✅ 通用前提：已安装 Python 3（推荐 3.8+）

测试是否已安装：

```bash
python3 --version
pip3 --version
```

---

## 🪟 Windows 系统

### ① 安装 Jupyter Notebook：

```bash
pip install notebook
```

### ② 启动 Jupyter：

```bash
jupyter notebook
```

浏览器将自动打开 Notebook 页面。

---

## 🍎 macOS 系统

### ① 安装 Jupyter Notebook：

```bash
pip3 install --user notebook
```

### ② 启动 Jupyter：

```bash
jupyter notebook
```

若未自动打开浏览器，可手动复制终端中的链接。

---

## 🐧 Linux 系统（如 Ubuntu）

### ① 安装 pip3（如未安装）：

```bash
sudo apt update
sudo apt install python3-pip
```

### ② 安装 Jupyter Notebook：

```bash
pip3 install --user notebook
```

### ③ 启动 Jupyter：

```bash
jupyter notebook
```

---

## 🔧 可选：使用虚拟环境安装（推荐）

```bash
python3 -m venv jupyter_env
source jupyter_env/bin/activate
pip install notebook
jupyter notebook
```

---

## 5️⃣本地文件传到云端服务器

### 【问题描述】  
我想把我本机（Mac）上的文件或文件夹上传到一台已经能通过 SSH 登录的 Linux 服务器（如 Ubuntu），用什么命令？VSCode 用 Remote SSH 登录服务器后，能直接上传Mac本地文件吗？如果遇到 `Permission denied (publickey)` 或找不到私钥怎么办？

---

1. **传输方法（推荐用scp）**  
   在 Mac 本地终端（Terminal 或 iTerm2）用如下命令上传文件或目录到服务器：
   ```bash
   scp -i <本地私钥路径> [-P <端口>] [-r] <本地文件或目录> <用户名>@<服务器IP>:<服务器路径>
   ```
   - `-i <本地私钥路径>`：指定用于 server 登录的私钥（如 `~/.ssh/id_rsa` 或其他）
   - `-P <端口>`：如不是标准 22 端口需指定
   - `-r`：上传文件夹时要加

   示例：

   ```bash
   scp -i ~/.ssh/server.pem -r ~/Documents/myfolder ubuntu@服务器IP:/home/ubuntu/目标目录
   ```
   
   > 注意：这个命令一定要在 Mac 的本地终端执行，而**不是**在 VSCode Remote SSH 或服务器 shell 里执行。

2. **VSCode Remote SSH 与本地终端的区别**  
   - VSCode Remote SSH 的终端窗口本质上就是服务器上的 shell，**无法访问或上传你本地文件**，也没有权限调用你本机的私钥。
   - **必须**回到 Mac 本地终端，用上面命令才行。

3. **报错排查**
   - `Warning: Identity file not accessible`  
     ⇒ 私钥路径写错或文件不存在，先用 `ls ~/.ssh/` 查找实际私钥名称。
   - `Permission denied (publickey)`  
     ⇒ 没用对私钥，或者 server 没添加你的公钥，需确认公钥已在服务器 `~/.ssh/authorized_keys`。
   - 文件权限错误（如 `bad permissions`）  
     ⇒ 用 `chmod 600 <私钥>` 修改权限。
   - 如果是在远程 shell 执行，会因为路径和私钥都“不可见”而失败。

4. **VSCode 文件上传快捷方式**  
   - 推荐：在 VSCode 的「REMOTE EXPLORER」或「资源管理器」面板，直接拖拽本地文件到服务器目录，或右键选择上传。

5. **适用场景**  
   - 任何需要从本地 Mac 上传文件到远程 Linux 服务器时，优先考虑用本地终端的 scp 或 sftp 命令；
   - 如果已打开了 VSCode 远程，可以直接用 VSCode 图形界面上传文件。

---

### 统一结论

- **用 Mac 本地的终端（而不是服务器 shell）执行 scp 命令上传本地文件。**
- **VSCode 远程终端仅能管理服务器端，不可以直接“看到”你 Mac 的本地数据。**
- **遇到报错先检查私钥路径和文件，有必要可用 VSCode 上传界面配合操作。**


## 6️⃣vi和nano都是ubuntu里面的笔记本编辑工具么？

`vi` 和 `nano` 都是 **Ubuntu（以及其他Linux系统）中的文本编辑器**，你可以把它们理解成命令行下的“记事本”，但它们的**使用方式和难度差别很大**👇：

---

### 🧠 对比：`vi` vs `nano`

| 特点   | `nano`                  | `vi` / `vim`              |
| ---- | ----------------------- | ------------------------- |
| 易用性  | ✅ 非常简单，适合新手             | ❌ 初学者易懵，操作复杂              |
| 使用方式 | 类似普通记事本，直接打字保存          | 分为“命令模式”和“编辑模式”，操作难       |
| 安装情况 | Ubuntu 默认安装了            | 通常也默认安装（或者是 `vim`）        |
| 退出方式 | `Ctrl + X` 然后按 `Y` 保存退出 | 需要先按 `Esc`，再输入 `:wq` 保存退出 |
| 推荐对象 | 新手、快速编辑配置文件             | 老手、高级编辑需求                 |

---

### ✅ 示例：

#### 1. 用 `nano` 编辑文件（推荐新手用）

```bash
nano ~/.jupyter/jupyter_notebook_config.py
```

* 直接进入文本界面可以编辑
* 修改完按 `Ctrl + O`（写入保存）
* 按 `Enter` 确认
* 然后按 `Ctrl + X` 退出

---

#### 2. 用 `vi` 或 `vim` 编辑文件（高手向）

```bash
vi ~/.jupyter/jupyter_notebook_config.py
```

* 进入后是“命令模式”，你按 `i` 进入“编辑模式”才能打字
* 编辑完后按 `Esc` 回到命令模式
* 输入 `:wq` 保存退出，或者 `:q!` 不保存强退

---

### 🧡 总结一句话：

> 如果你是新手，**就用 `nano`**，简单、安全、直接。
> `vi` 很强大，但对初学者不友好，**容易误操作关不掉**。


---
### ✅ 总结表：Ubuntu 中不同工具创建虚拟环境后的程序与依赖存储位置

| 包管理工具                                           | 是否可指定目录            | 程序和依赖存储位置（相对于当前文件夹）                                                       | 可执行程序位置                          | 备注说明                             |
| ----------------------------------------------- | ------------------ | ------------------------------------------------------------------------- | -------------------------------- | -------------------------------- |
| **venv**                                        | ✅ 是                | `myenv/lib/pythonX.Y/site-packages/`                                      | `myenv/bin/`                     | 自包含在虚拟环境目录中                      |
| **virtualenv**                                  | ✅ 是                | `myenv/lib/pythonX.Y/site-packages/`                                      | `myenv/bin/`                     | 和 venv 相似，适用于旧版 Python           |
| **conda --prefix**                              | ✅ 是                | `conda_env/lib/pythonX.Y/site-packages/`                                  | `conda_env/bin/`                 | 需加 `--prefix ./conda_env` 明确路径   |
| **conda (默认)**                                  | ❌ 否（集中管理）          | `~/anaconda3/envs/env_name/lib/pythonX.Y/site-packages/`                  | `~/anaconda3/envs/env_name/bin/` | 统一放在 Anaconda 安装目录               |
| **pipx**                                        | ❌ 否（全局隔离）          | `~/.local/pipx/venvs/package_name/lib/...`                                | `~/.local/bin/`                  | 安装为独立小环境，全局命令可用                  |
| **uv pip install**（例如：`uv pip install jupyter`） | ✅ 是（取决于是否在 venv 里） | 如果在虚拟环境中：跟 venv 一样 <br> 如果系统级：`~/.cache/uv` 缓存源码，实际安装到系统 `site-packages/` | 当前环境的 `bin/` 或全局路径               | `uv` 是加速型工具，本质还是调用 Python 的包管理方式 |

---

### 🔎 举例说明

你在目录 `/home/user/myproject/` 下：

```bash
cd /home/user/myproject/
python3 -m venv myenv
source myenv/bin/activate
pip install jupyter
```

* 程序安装路径 → `/home/user/myproject/myenv/lib/python3.X/site-packages/jupyter/`
* 执行程序路径 → `/home/user/myproject/myenv/bin/jupyter`

---

### ✅ 结论：

* **用哪个工具建环境，就在哪建就在哪存，不同工具有不同“风格”**：

  * `venv` / `conda --prefix` 是“就地放包”
  * `conda` 默认是集中式存放
  * `pipx` 是独立、轻量
  * `uv` 是高性能 pip 工具，依赖是否在当前路径取决于你是否用虚拟环境

---

# Ubuntu 上升级显卡驱动

在 Ubuntu 上升级显卡驱动（通常是 **NVIDIA 驱动**，因为用到 GPU 加速的 Docker/AI 容器一般要求较新驱动），你可以按以下步骤操作。  
（如果你是用的 AMD 显卡，也可以说明，我再提供 AMD 升级办法）

---

## 一、确定你的显卡型号

先确认你的 GPU 类型和型号：
```bash
lspci | grep VGA
```
或者（NVIDIA 专用）：
```bash
nvidia-smi
```

---

## 二、更新系统源

先把系统的软件包源更新到最新：
```bash
sudo apt update
sudo apt upgrade -y
```

---

## 三、查看当前可用驱动

这一步可以看到你能装哪些版本：

```bash
ubuntu-drivers devices
```

它会列出适合你的 NVIDIA 驱动版本，比如：
```
driver   : nvidia-driver-535 - third-party free recommended
driver   : nvidia-driver-525 - third-party free
driver   : xserver-xorg-video-nouveau - distro free builtin
```
有 `recommended` 标签的为推荐驱动。

---

## 四、一键安装推荐驱动 **（推荐！）**

```bash
sudo ubuntu-drivers autoinstall
```

它会自动安装**推荐的最新版驱动**，大部分情况用这个就对了。

---

## 五、自选特定版本安装

比如你想装 535 版本：
```bash
sudo apt install nvidia-driver-535
```

---

## 六、重启电脑

完成安装后**要重启系统！**
```bash
sudo reboot
```

---

## 七、验证驱动是否生效

重启后，运行：
```bash
nvidia-smi
```
能看到你的显卡信息和驱动版本，说明新驱动生效了。

---

### （可选）如果你需要最新**官方**驱动

1. 你可以去 [NVIDIA官网](https://www.nvidia.com/Download/index.aspx?lang=en-us) 下载.run 安装包手动安装，但通常 Ubuntu 已经支持绝大多数新驱动，**用上面方法更安全省事**。

---

## 常见问题

- 驱动无法生效？  
    - 检查 Secure Boot 是否关闭。有的笔记本或服务器装完驱动后 Secure Boot 没关会导致驱动不起效。
- 出现 自动装后 nvidia-smi 报找不到驱动？
    - 可以先卸载再重装：
      ```bash
      sudo apt purge nvidia*
      sudo apt install nvidia-driver-535
      sudo reboot
      ```

---

## 总结流程

1. `sudo apt update && sudo apt upgrade -y`
2. `ubuntu-drivers devices`
3. `sudo ubuntu-drivers autoinstall` 或 `sudo apt install nvidia-driver-xxx`
4. `sudo reboot`
5. `nvidia-smi` 验证

---

# 📌 VSCode 远程登录 Linux 服务器（含 SSH 密钥管理）详尽笔记


## 1️⃣ VSCode 远程连接原理

- VSCode 使用 **Remote - SSH** 插件
- 本质上就是 VSCode 本地跑一个 SSH 客户端
- 远程服务器跑一个 VSCode server 组件
- 通过 SSH 隧道把本地 VSCode 和远程 VSCode server 连接起来
- 这样就能在本地编辑、远程运行

---

## 2️⃣ VSCode 配置 Remote-SSH

### 2.1 安装插件

- 打开 VSCode → Extensions → 搜索 `Remote - SSH` → 安装
- 安装后左下角会出现一个绿色远程连接按钮

### 2.2 添加远程主机

- 点击左下角绿色按钮 → 选择 **Remote-SSH: Connect to Host...**
- 输入 `user@ip`（例如 `ubuntu@192.168.1.10`）
- VSCode 会把你的主机信息写入 `~/.ssh/config`

示例 SSH 配置文件：

```sshconfig
Host myserver
    HostName 192.168.1.10
    User ubuntu
    Port 22
    IdentityFile ~/.ssh/id_rsa
````

---

## 3️⃣ 生成 SSH 密钥对

> SSH 密钥 = 私钥 + 公钥
> 公钥放到服务器
> 私钥放在你电脑
> 登录时只要密钥匹配就免密登录，且安全性高

---

### 3.1 生成一对普通密钥

在本地终端执行：

```bash
ssh-keygen
```

提示：

```
Enter file in which to save the key (/Users/you/.ssh/id_rsa):
```

直接回车，默认保存在：

* 私钥：`~/.ssh/id_rsa`
* 公钥：`~/.ssh/id_rsa.pub`

---

### 3.2 生成一对带邮箱注释的定制化密钥

如果想备注邮箱方便识别（多开发者场景推荐）：

```bash
ssh-keygen -t rsa -b 4096 -C "youremail@example.com"
```

含义：

* `-t rsa` → 使用 RSA 算法
* `-b 4096` → 4096 位强度
* `-C` → 注释（方便以后看到公钥是谁）

它同样会提示：

```
Enter file in which to save the key (/Users/you/.ssh/id_rsa):
```

你也可以输入：

```
/Users/you/.ssh/id_rsa_myserver
```

这样就能管理多把钥匙。

---

## 4️⃣ 把公钥添加到服务器

### 4.1 ssh-copy-id（推荐）

```bash
ssh-copy-id user@remote_ip
```

会自动把你的公钥写进服务器的 `~/.ssh/authorized_keys`。

---

### 4.2 手动复制

如果 `ssh-copy-id` 不可用：

```bash
cat ~/.ssh/id_rsa.pub
```

复制里面的内容，然后在服务器上：

```bash
nano ~/.ssh/authorized_keys
```

粘贴进去并保存即可。

---

## 5️⃣ 管理 authorized\_keys（服务器端）

### 5.1 查看

```bash
cat ~/.ssh/authorized_keys
```

### 5.2 删除

用编辑器打开：

```bash
nano ~/.ssh/authorized_keys
```

手动删除不需要的公钥行。

### 5.3 替换

同样编辑 `authorized_keys`，把旧公钥行删掉，粘贴新的。

---

## 6️⃣ 本地 SSH 配置文件

路径：

```bash
~/.ssh/config
```

示例结构：

```sshconfig
Host myserver
    HostName 192.168.1.10
    User ubuntu
    IdentityFile ~/.ssh/id_rsa_myserver
    Port 22
```

* `Host` → 别名
* `HostName` → IP 或域名
* `User` → 登录用户名
* `IdentityFile` → 私钥文件
* `Port` → 端口

---

## 7️⃣ VSCode 使用技巧

✅ 通过左下角绿色按钮切换服务器
✅ `F1` → `Remote-SSH: Add New SSH Host` 添加新主机
✅ VSCode 自动远程同步文件
✅ VSCode 会远程运行终端和调试

---

## 8️⃣ known\_hosts 文件原理

* 第一次连接一个服务器时：

  ```
  The authenticity of host '1.2.3.4' can't be established.
  ```

  这时输入 `yes` 会把服务器的指纹存到

  ```bash
  ~/.ssh/known_hosts
  ```
* 以后再次连接时会自动校验指纹

  * 如果匹配 → 正常登录
  * 如果不匹配 → 报错：

    ```
    REMOTE HOST IDENTIFICATION HAS CHANGED!
    ```

  可能原因：

  * 服务器重装
  * 被中间人攻击

### ⚙ 解决 known\_hosts 冲突

* 手动编辑

  ```bash
  nano ~/.ssh/known_hosts
  ```

  删除对应的行
* 或者一键清理

  ```bash
  ssh-keygen -R 服务器IP
  ```

---

## 9️⃣ 权限检查与安全提示

✅ 私钥权限必须安全：

```bash
chmod 600 ~/.ssh/id_rsa
```

✅ `~/.ssh` 目录：

```bash
chmod 700 ~/.ssh
```

✅ `authorized_keys`：

```bash
chmod 600 ~/.ssh/authorized_keys
```

✅ 服务器要确认 SSH 服务正常：

```bash
sudo systemctl status ssh
```

✅ 确保云服务器防火墙或者安全组允许 22 端口（或指定端口）

---

## 🔟 查看密钥内容

### 10.1 查看本地公钥

```bash
cat ~/.ssh/id_rsa.pub
```

### 10.2 查看本地私钥

```bash
cat ~/.ssh/id_rsa
```

> **切记：不要把私钥暴露给任何人。**

---

### ✅ 总结一句话

* VSCode Remote SSH = VSCode client + 远程 VSCode server + ssh 隧道
* 公钥放服务器，私钥保存在本地
* 配置好之后就可以快速安全免密登录

---

## 📌 Ubuntu 查看与关闭进程操作总结

### 一、查看进程

#### 1. 使用 `ps` 命令查看当前进程

```bash
ps aux
```

* 显示所有用户的所有进程（包括后台进程）。
* 常用字段说明：

  * USER：进程所属用户
  * PID：进程ID
  * %CPU/%MEM：占用CPU/内存百分比
  * COMMAND：启动命令

#### 2. 使用 `top` 实时监控进程

```bash
top
```

* 实时显示系统资源占用和运行中的进程。
* 按 `q` 退出，`k` 输入 PID 后可直接杀死进程。

#### 3. 使用 `htop`（更美观，需要安装）

```bash
sudo apt install htop
htop
```

* 支持上下键选择、F9 关闭进程，界面更友好。

#### 4. 根据进程名查找 PID

```bash
ps aux | grep <进程名>
```

示例：

```bash
ps aux | grep python
```

#### 5. 使用 `pidof` 查找可执行文件的 PID（仅限后台运行程序）

```bash
pidof <程序名>
```

示例：

```bash
pidof nginx
```

---

### 二、关闭（杀死）进程

#### 1. 使用 `kill` 根据 PID 杀死进程

```bash
kill <PID>
```

* 发送默认 `SIGTERM (15)` 信号，要求进程正常退出。
* 示例：

```bash
kill 12345
```

#### 2. 使用 `kill -9` 强制终止进程

```bash
kill -9 <PID>
```

* 强制终止进程（发送 `SIGKILL` 信号），无法被拦截。

#### 3. 使用 `pkill` 根据名称关闭进程

```bash
pkill <进程名>
```

* 示例：

```bash
pkill firefox
```

#### 4. 使用 `killall` 杀死所有同名进程

```bash
killall <程序名>
```

* 示例：

```bash
killall python3
```

---

## ✅ 小技巧

* 使用 `ps -ef` 可查看父子进程关系：

```bash
ps -ef | grep <进程名>
```

* 杀掉占用端口的进程（以 8080 为例）：

```bash
sudo lsof -i :8080
sudo kill -9 <PID>
```

---
## 【Ubuntu】 分区与文件系统概念总结

1. Ubuntu 是否有分区概念？
是的，Ubuntu (以及所有 Linux 系统) 拥有明确的分区概念。
- 硬盘在使用前必须进行分区，将一个物理硬盘划分为一个或多个逻辑区域。
- 每个分区可以独立格式化并用于存储数据。

2. Linux 文件系统树结构 (与 Windows/macOS 对比)
Linux 采用统一的“文件系统树”结构，这是其与 Windows 和 macOS 的主要区别：
- 单一根目录 **/****：** 所有文件和目录都从一个共同的根目录 / (斜杠) 开始。
- 挂载点： 所有的分区、外部硬盘、USB 设备等，最终都会被“挂载”到这个 / 目录树下的某个子目录里。
- 与 Windows 不同： Windows 使用盘符 (C:, D:, E:) 来表示不同的分区或驱动器。
- 与 macOS 不同： macOS 内部也分区，但通常对用户隐藏了底层分区细节，只呈现一个大的“Macintosh HD”。Linux 则更透明，用户可以清楚地看到分区和挂载点。


3. 分区和挂载的形象比喻
- 整个 Ubuntu 文件系统 就像一座大房子，入口是 /。
- 不同的分区 就像房子里的不同房间 (如 / 根分区、/home 用户数据分区、/boot 启动分区等)。
- 挂载外部硬盘 就像在房子里开辟一个新房间或连接一个外部仓库。这个“新房间”或“仓库”通过一个“门” (即**挂载点**) 连接到房子内部的某个位置。
  - 例如，外部硬盘 /dev/sdb1 可能被挂载到 /mnt/data 目录下。访问 /mnt/data 实际上就是访问该外部硬盘的内容。

4. 如何在 Ubuntu 中查看分区和文件系统信息
以下是常用的命令行工具：

4.1 lsblk (推荐，最常用且直观)
- 功能： 列出所有块设备 (硬盘、分区、逻辑卷等) 的信息，以树状结构显示，并显示挂载点。 
- 命令：
lsblk
- 示例输出解释：
  - NAME: 设备名称 (如 sda 是硬盘，sda1 是分区)。
  - TYPE: 设备类型 (disk 硬盘, part 分区, lvm 逻辑卷)。
  - MOUNTPOINTS: 挂载点，表示该分区被挂载到文件系统的哪个位置。

4.2 sudo fdisk -l (查看分区表，需 root 权限)
- 功能： 列出系统中所有硬盘的分区表信息，包括分区大小、类型等。
- 命令：
sudo fdisk -l

4.3 sudo parted -l (查看分区表，更详细，需 root 权限)
- 功能： 与 fdisk 类似，但通常提供更详细的分区信息，尤其适用于 GPT 分区表。
- 命令：
sudo parted -l

4.4 df -h (查看已挂载文件系统使用情况)
- 功能： 显示已挂载的文件系统 (通常对应分区) 的磁盘空间使用情况。
- 命令：
df -h
- 示例输出解释：
  - Filesystem: 对应的设备或分区。
  - Mounted on: 挂载点。
  - Size, Used, Avail, Use%: 空间使用统计。


