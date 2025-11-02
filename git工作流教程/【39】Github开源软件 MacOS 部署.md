# 39_Github开源软件 MacOS 部署笔记

## 一、项目概述
- **目标**：在 Windows 上运行 Linux 子系统 (WSL) 的 Docker 中安装 macOS，实现“三层套娃系统”。
- **用途**：
  - 运行 macOS 专用软件
  - 开发跨平台软件
  - 测试软件兼容性
- **项目来源**：`Docker-OSX` 项目，可通过 Docker 启动 macOS。
- **硬件要求**：较高；普通 Linux 小主机性能不足，建议使用性能较强的 Windows 电脑。

---

## 二、前置知识与准备
- 需了解：
  - **WSL**（Windows Subsystem for Linux）
  - **Docker Desktop** 及其基本操作
- 建议先观看相关基础视频。

---

## 三、WSL 安装与配置

### 1. 检查 CPU 虚拟化
- 打开 **任务管理器 → 性能 → CPU**
- 确认“虚拟化”已开启。

### 2. 启用必要功能
- 打开“启用或关闭 Windows 功能”：
  - 勾选：
    - “适用于 Linux 的 Windows 子系统”
    - “虚拟机平台”
- 点击确定并重启电脑。

### 3. 安装 WSL
- 以 **管理员身份** 运行 `cmd`
- 执行命令：
    ```bash
     wsl --install
    ```

* 若网络在国内，建议加参数：

    ```bash
    wsl --install --web-download
    ```
* 默认安装 **Ubuntu**。
* 设置用户名与密码。

---

## 四、WSL 配置文件修改

### 1. 创建配置文件

* 路径：

  ```
  C:\Users\<用户名>\
  ```
* 新建文件：

  ```
  .wslconfig
  ```
* 内容示例：

  ```ini
  [wsl2]
  nestedVirtualization=true
  ```

  （用于启用虚拟机嵌套）

### 2. 应用配置

```bash
wsl --shutdown
```

重新打开 WSL 以生效。

---

## 五、安装与配置 Docker Desktop

### 1. 下载与安装

* 前往项目 Release 页下载 **Windows 版 Docker Desktop**。
* 若速度慢，可使用国内加速源或阿里云镜像下载。

### 2. 设置调整

* 打开 Docker Desktop → 设置（齿轮图标）：

  * **General**：勾选 `Use the WSL 2 based engine`
  * **Resources → WSL Integration**：

    * 勾选 `Enable integration with my default WSL`
    * 勾选 Ubuntu
* 点击 **Apply & Restart**。

### 3. 验证 Docker 是否可用

* 在 Windows 系统桌面右键打开终端，选择 Ubuntu   系统输入：
```bash
docker ps
```

若显示容器信息，则安装成功。

---

## 六、安装虚拟化与远程桌面依赖

### 1. 安装 KVM

```bash
sudo apt update # 更新一下 apt 索引
sudo apt -y install bridge-utils cpu-checker libvirt-clients libvirt-daemon qemu qemu-kvm
``` 

验证：

```bash
kvm-ok
```

显示 `KVM acceleration can be used` 即成功。

### 2. 安装 X11（远程桌面）

```bash
sudo apt install x11-apps -y
```

---

## 七、运行 Docker-OSX 启动 macOS

### 1. 拉取镜像命令（使用阿里云私库）

* 原始镜像过大（约 2GB），Docker Hub 速度慢。
* 可替换为：

  ```
  registry.cn-hangzhou.aliyuncs.com/用户名/macos:latest
  ```

### 2. 修改命令配置

* 替换 Linux 版为 Windows 版路径。
* 使用自己上传的镜像地址。

### 3. 启动容器

```bash
docker run -it --device /dev/kvm --name macos --privileged -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY <镜像名>
```

---

## 八、macOS 系统安装步骤

1. 弹出 **QEMU 窗口**
2. 打开 **Disk Utility → Continue**
3. 选择最大磁盘（虚拟磁盘不占满物理空间）
4. `Erase`   格式化磁盘，命名如 `ShrimpDisk`
5. 退出窗口 → 选择 **Reinstall macOS**
6. 一路点击 Continue、Agree
7. 选择刚创建的磁盘
8. 等待安装完成（约 1-2 小时）
9. 跳过 Apple ID 登录
10. 创建用户名与密码

> ⚠️ 性能较低，仅适合软件测试用途。

---

## 九、系统保存与重启

### 1. 关闭系统

* 直接关闭 QEMU 窗口
* Docker 容器即停止运行。

### 2. 查看容器状态

```bash
docker ps -a
```

### 3. 重启容器

```bash
docker start -ai <容器ID>
```

---

## 十、总结

* **核心流程**：

  1. 启用 WSL & 虚拟机平台
  2. 安装 Ubuntu + Docker Desktop
  3. 配置嵌套虚拟化
  4. 拉取 Docker-OSX 镜像
  5. 启动 macOS 虚拟机
* **主要价值**：

  * 在 Windows 环境下体验 macOS
  * 测试软件跨平台兼容性
  * 为开发者提供虚拟 macOS 环境 
