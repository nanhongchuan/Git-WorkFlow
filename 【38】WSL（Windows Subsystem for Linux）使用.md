# WSL（Windows Subsystem for Linux）使用笔记

## 一、WSL简介

* **全称**：Windows Subsystem for Linux
* **功能**：在Windows系统中运行Linux环境，实现两者的无缝融合。
* **优势**：

  * Windows终端直接运行Linux命令
  * Linux中可调用Windows软件
  * 支持Docker运行
  * 支持显卡直通（GPU Passthrough）
  * 文件、网络、剪贴板等系统资源共享

---

## 二、WSL 1 与 WSL 2 的区别

| 对比项           | WSL 1                          | WSL 2                          |
| ------------- | ------------------------------ | ------------------------------ |
| 实现方式          | 翻译层（将Linux指令翻译为Windows NT内核指令） | 基于Hyper-V虚拟化平台                 |
| 是否运行真实Linux内核 | 否                              | 是                              |
| 兼容性           | 有限制（如无法运行Docker）               | 完整兼容（支持Docker）                 |
| 性能            | I/O性能较低                        | 更高效，支持显卡直通                     |
| 维护成本          | 高                              | 低                              |
| 架构说明          | 无独立虚拟机                         | Windows和Linux分别运行在Hyper-V上的虚拟机 |

---

## 三、使用WSL 2 的前提条件

### 1. 启用CPU虚拟化

* 打开任务管理器 → 性能 → CPU → 检查“虚拟化”是否已启用
* 若未启用：

  * 进入BIOS设置
  * Intel CPU：开启“Intel VT-x”或“VMX”
  * AMD CPU：开启“AMD-V”

### 2. 启用Windows功能

路径：**控制面板 → 启用或关闭 Windows 功能**
勾选以下选项：

* `适用于 Linux 的 Windows 子系统`
* `虚拟机平台`

完成后点击“确定”，并**重启电脑**

---

## 四、安装WSL与Linux发行版

### 1. 安装WSL命令

```bash
wsl --install
```

> 若在国内网络环境下，建议添加参数：

```bash
wsl --install --web-download 
```

### 2. 默认安装的发行版

* 默认安装：**Ubuntu 22.04**
* 可更换发行版：使用命令查看列表

```bash
wsl --list --online
```

* 安装指定发行版：

```bash
wsl --install <发行版名称> --web-download
# 例如
wsl --install kali-linux  --web-download
```

### 3. 设置用户名和密码

桌面右键终端打开， 默认是powershell打开。

首次进入Linux后，系统会提示设置用户名和密码。

---

## 五、子系统管理命令

### 查看已安装的子系统

```bash
wsl --list --v
```

输出示例：

* 星号（*）表示当前默认子系统
* “Running” 表示正在运行
* “Stopped” 表示已停止

### 切换默认子系统

```bash
wsl --set-default <发行版名称>
```

### 启动子系统

```bash
wsl -d <发行版名称>

# 或者在powershell里直接打开对应系统的按钮
```

### 退出子系统

```bash
exit
```

### 卸载子系统

```bash
wsl --unregister <发行版名称>
```

---

## 六、子系统备份与恢复

### 备份命令

```bash
wsl --export <发行版名称> <文件名.tar>
```

### 恢复/导入命令

```bash
# 切换到D盘
cd D:
# 新建一个文件夹
mkdir wsl
# 导入文件
wsl --import <新名称> <导入目录> <备份文件路径>
# 例如
wsl --import Ubuntu2 D:\wsl
```

导入后，会在对应目录生成一个Hyper-V镜像文件。（例如：ext4.vhdx)   

---

## 七、文件共享与访问

### Linux访问Windows磁盘

* 在Linux终端输入：

  ```bash
  df -h
  ```

  可看到Windows盘符被挂载到 `/mnt/c/`、`/mnt/d/` 等目录下。

> ⚠️ **注意**：挂载卷IO性能较差，如涉及大量I/O操作，建议文件直接拷贝到Linux系统内部。

### Windows访问Linux文件

* 打开“此电脑”，在左侧会看到🐧图标“Linux”。
* 展开后可直接浏览、增删改查Linux文件。

---

## 八、跨系统命令互操作

### 在Linux中调用Windows程序

示例：

```bash
pwd                      # 查看当前工作目录
vi                       # 新建一个文本文件,随便打点文字
cat test.txt             # 查看这个文件
notepad.exe file.txt     # 打开Windows记事本
explorer.exe .           # 打开当前目录的资源管理器，点表现当前目录
```

### 在Windows中调用Linux命令

在PowerShell中：

```powershell
Get-ChildItem | wsl grep video 
```

> 前半段为Windows命令，后半段为Linux命令，实现混合管道操作。

---

## 九、图形界面支持（WSLg）

* WSLg允许Linux GUI程序直接以Windows窗口形式运行。
* 示例：

  ```bash
  sudo apt install gimp
  gimp
  ```

  → 直接以独立窗口形式打开Linux版GIMP。

---

## 十、GPU直通

* 在Linux中可直接识别Windows显卡：

  ```bash
  nvidia-smi
  ```
* 支持CUDA计算，可直接运行AI模型，无需复杂虚拟机设置。

---

## 十一、Kali Linux专属黑科技：Kex

### 安装与启动

```bash
sudo apt install kali-win-kex -y
kex --esm --ip --sound
```

* 通过远程桌面方式连接
* 提供完整图形桌面环境

---

## 十二、Ubuntu系统的远程桌面连接

- 推荐使用 Windows 电脑 HyperV 虚拟机安装 Ubuntu
- 参考视频：https://www.bilibili.com/video/BV1QG411e7pn/


## 十三、⚙️ 高级配置详解（重点）

### （一）配置文件类型

| 文件名             | 位置                                           | 作用范围          |
| --------------- | -------------------------------------------- | ------------- |
| `.wslconfig`    | Windows 用户目录（如 `C:\Users\<name>\.wslconfig`） | 全局配置，对所有子系统生效 |
| `/etc/wsl.conf` | Linux 子系统内（每个发行版独立）                          | 专有配置，仅对该子系统生效 |

---

### （二）配置修改规则

* 修改配置后必须执行：

```bash
wsl --shutdown
```

* 等待 **约 8 秒** 后重启子系统方可生效

---

### （三）示例 1：启用 systemd

> systemd 是 Linux 的核心进程管理系统

1. 编辑 `/etc/wsl.conf`

```bash
sudo vi /etc/wsl.conf
```

2. 添加以下内容：

```ini
[boot]
systemd=true
```

3. 保存退出后执行：

```bash
wsl --shutdown
```

4. 等待 8 秒后重启：

```bash
systemctl list-units
```

> 若能列出服务列表，表示 **`systemd`** 已成功启用 

---

### （四）示例 2：修改网络为镜像模式（Mirror Mode）

- **`.wslconfig`** 用来修改网络文件的配置

#### 默认情况

* Ubuntu系统里输入`ifconfig` 显示：172.31.x.x
* Windows系统里输入`ipconfig` 显示：192.168.x.x
* 处于不同网段（NAT 模式），外部设备（宿主机） 无法访问 WSL 网络

#### 修改步骤
* 让我的虚拟机（Ubuntu系统）和宿主机（windows系统）

1. 在 Windows 用户目录创建 `.wslconfig`
   路径示例：
   `C:\Users\<用户名>\.wslconfig`
2. 用记事本打开它，然后添加以下内容：

```ini
[wsl2]
networkMode=mirror
```

3. 执行：

```bash
wsl --shutdown
```

4. 等待 8 秒后重启，运行：

```bash
ifconfig
```

> 现在 WSL 与 Windows 共享同一个 IP（桥接模式）

---

## 十四、Docker 使用（配合 WSL2）

### 1️⃣ 安装

* 下载并安装 Docker Desktop（Windows 版）
* 可通过 GitHub Release 获取

### 2️⃣ 命令行安装（自定义路径）

```bash
start /w "" "Docker Desktop Installer.exe" install --installation-dir=D:\Docker 
```

### 3️⃣ 设置镜像源（加速下载）

1. 打开 Docker Desktop → Settings → Docker Engine
2. 在 JSON 最外层添加：

```json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false,  # 要记得加逗号
  "registry-mirrors": [   # 换源新加列
    "https://docker.m.daocloud.io", # 换源新加列
    "https://docker.lpanel.live" # 换源新加列
  ]
}
```

3. 点击 **Apply & Restart**

---

## ✅ 小结

* WSL2 是 Windows 与 Linux 融合的核心桥梁，兼顾虚拟机性能与系统原生交互。
* 可一键运行 Docker、调用 Linux 命令、显卡直通、systemd 服务、甚至图形界面。
* `.wslconfig` 与 `/etc/wsl.conf` 的配置能力极大增强了可定制性。
* 建议结合 Hyper-V 管理器进行虚拟化管理，避免手动网络配置出错。

