# Docker 学习笔记

### **一、Docker 核心概念**

### **1. 容器（Container）**

- **定义：** 容器是应用程序的独立运行环境。
- **宿主机（Host）：** 运行 Docker 容器的计算机。
- **与虚拟机的区别：** Docker 容器共享同一个系统内核，而每个虚拟机都包含一个完整的操作系统内核。因此，Docker 容器更轻、更小，启动速度更快。

### **2. 镜像（Image）**

- **定义：** 镜像是容器的模板。
- **与容器的关系：** 类似于软件安装包与安装出的软件，或者制作糕点的模具与做出的糕点。一个镜像可以创建多个容器。

### **3. Docker 仓库（Registry）**

- **定义：** 存放和分享 Docker 镜像的地方。
- **Docker Hub：** Docker 的官方仓库，上面存储了许多人分享的 Docker 镜像。

### **4. 镜像的组成**

一个完整的镜像名称通常包含四部分：

`registry/namespace/repository:tag`。

- **`registry`：** 仓库注册表地址，如 `docker.io`（Docker Hub 官方仓库，可省略）。
- **`namespace`：** 命名空间，通常是作者的名字，用于区分同名镜像 9。Docker 官方维护的镜像命名空间是
    
    `library`，可省略 。
    
- **`repository`：** 镜像库，即镜像的名字。
- **`tag`：** 镜像的标签名，表示版本号，如 `:latest` 或 `:1.28.0`，不写默认为最新版。

### **5. 镜像库（Repository）**

- **定义：** Registry（仓库地址）+ Namespace（命名空间）+ 镜像名，组合起来是一个 Repository。一个镜像库存储的是同一个镜像的不同版本。

### **二、Docker 安装**

### **1. 在 Linux 上安装**

- **推荐环境：** Linux 系统是 Docker 的最佳实战环境，因为 Docker 基于 Linux 容器化技术。
- **安装步骤：**
    1. 访问`get.docker.com`。
    2. 复制并执行第一步和第四步的命令。
    3. 如果不是`root` 用户，需要在所有 `docker` 命令前加上 `sudo` 。

### **2. 在 Windows 上安装**

- **前提：** Windows 和 Mac 电脑通过虚拟一个 Linux 子系统来运行 Docker。
- **安装 WSL (适用于 Linux 的 Windows 子系统)：**
    1. 在 Windows 功能中勾选“虚拟机平台”（Virtual Machine Platform）和“适用于 Linux 的 Windows 子系统”（WSL）。
    2. 重启电脑。
    3. 以管理员身份打开命令提示符（CMD），输入
        
        `wsl --set-default-version 2` 设置 WSL 默认版本为 2。
        
    4. 执行`wsl --update` 安装 WSL。
    5. 如果网络不好，可以加上`-web-download` 参数 。
- **安装 Docker Desktop：**
    1. 从 Docker 官网下载 Docker Desktop 安装包，选择与 CPU 架构对应的版本（Windows 通常是 AMD64）。
    2. 安装过程简单，一路“下一步”即可。
    3. 安装完成后，确保 Docker Desktop 软件保持运行状态。
    4. 在终端输入`docker --version` 验证是否安装成功。

### **3. 在 Mac 上安装**

- **步骤：** 根据自己的芯片（Intel 或 Apple Silicon）下载对应的 Docker Desktop 安装包，然后安装即可。

### **三、Docker 镜像命令**

### **1. `docker pull`：下载镜像**

- **作用：** 从仓库下载镜像。
- **示例：** `docker pull nginx` (从 Docker Hub 官方仓库下载最新版的 Nginx 镜像)。
- **特定版本：** 可以指定标签，如 `docker pull nginx:1.28.0`。
- **特定 CPU 架构：** 使用 `--platform` 参数，如 `docker pull --platform linux/arm64 nginx`。

### **2. `docker images`：列出镜像**

- **作用：** 列出所有已下载的 Docker 镜像。

### **3. `docker rmi`：删除镜像**

- **作用：** 删除指定镜像。
- **示例：** `docker rmi nginx` 或 `docker rmi <image_id>` 。

### **4. 配置镜像站**

- **作用：** 解决在中国网络环境下下载镜像慢或失败的问题。
- **Linux 配置：** 修改 `/etc/docker/daemon.json` 配置文件，添加 `registry-mirrors`。然后重启 Docker 服务 (`sudo systemctl restart docker`) 。
- **Windows/Mac 配置：** 在 Docker Desktop 的设置中找到 `Docker Engine`，修改 `registry-mirrors` 配置，然后点击 `Apply & Restart`。

### **四、Docker 容器命令**

### **1. `docker run`：创建并运行容器**

- **作用：** 使用镜像创建并运行容器，这是最重要的命令。
- **基础用法：** `docker run <image_name>`。
- **自动拉取：** 如果本地不存在镜像，`docker run` 会自动先拉取镜像再创建运行容器。

### **2. `docker ps`：查看容器**

- **作用：** 查看正在运行的容器。
- **`docker ps -a`：** 查看所有容器（包括已停止的）。

### **3. `docker stop` 和 `docker start`：启停容器**

- **`docker stop <container_id_or_name>`：** 停止正在运行的容器。
- **`docker start <container_id_or_name>`：** 启动已停止的容器。
- **特点：** 使用这两个命令启停容器时，之前设置的端口映射、挂载卷等参数会被保留。

### **4. `docker rm`：删除容器**

- **作用：** 删除已停止的容器。
- **强制删除：** 使用 `-f` 参数可以强制删除正在运行的容器，如 `docker rm -f <container_id>`。

### **五、`docker run` 重要参数**

### **1. `d`：后台运行（Detached Mode）**

- **作用：** 让容器在后台运行，不阻塞当前终端窗口。
- **示例：** `docker run -d nginx`。

### **2. `p`：端口映射（Port Mapping）**

- **作用：** 将宿主机的端口与容器的端口进行绑定，使得宿主机可以访问容器内部的网络。
- **格式：** `-p <host_port>:<container_port>`（先外后内）。
- **示例：** `docker run -p 80:80 nginx` (将宿主机的 80 端口映射到容器的 80 端口)。

### **3. `v`：挂载卷（Volume）**

- **作用：** 将宿主机的目录与容器的目录进行绑定，实现数据的持久化保存。
- **绑定挂载（Bind Mount）：**
    - **格式：** `-v <host_path>:<container_path>`。
    - **特点：** 宿主机目录会覆盖容器内的目录。
- **命名卷挂载（Named Volume）：**
    - **创建卷：** `docker volume create <volume_name>`。
    - **使用卷：** `-v <volume_name>:<container_path>`。
    - **特点：** 第一次使用时，Docker 会将容器的文件夹同步到命名卷中进行初始化。
    - **查看卷的真实目录：** `docker volume inspect <volume_name>`。
    - **管理卷：**
        - `docker volume ls`：列出所有卷。
        - `docker volume rm <volume_name>`：删除指定卷。
        - `docker volume prune -a`：删除所有未被容器使用的卷。

### **4. `e`：设置环境变量（Environment）**

- **作用：** 向容器内部传递环境变量，常用于配置数据库用户名、密码等 66。
- **格式：** `-e <KEY>=<VALUE>`。
- **示例：** `docker run -e MONGO_INITDB_ROOT_USERNAME=user -e MONGO_INITDB_ROOT_PASSWORD=password ...`。
- **查找环境变量：** 可以去 Docker Hub 上的镜像文档或项目的 GitHub 仓库查找可用的环境变量。

### **5. `-name`：自定义容器名称**

- **作用：** 给容器起一个自定义的名字，方便记忆和管理。
- **特点：** 容器名称在宿主机上必须是唯一的。
- **示例：** `docker run --name my-nginx ... nginx`。

### **6. `it`：交互式进入容器**

- **作用：** 进入容器内部，获得一个交互式的命令行环境。
- **`-rm`：** 当容器停止时自动删除容器 。
- **常用组合：** `docker run -it --rm <image_name> <command>` (常用于临时调试)。

### **7. `-restart`：重启策略**

- **作用：** 配置容器在停止时的重启策略。
- **`always`：** 只要容器停止（包括内部错误、宿主机断电等），就会立即重启。
- **`unless-stopped`：** 除非手动停止，否则会自动重启。

### **六、Docker 容器的其他操作**

### **1. `docker inspect`：查看容器详细信息**

- **作用：** 查看容器的详细信息，包括端口映射、挂载卷、环境变量等。
- **示例：** `docker inspect <container_id_or_name>`。

### **2. `docker create`：只创建不启动**

- **作用：** 只创建容器，但不立即启动。
- **启动方式：** 使用 `docker start <container_id>` 启动。

### **3. `docker logs`：查看日志**

- **作用：** 查看容器的日志。
- **`docker logs -f`：** 滚动查看实时日志。

### **4. `docker exec`：在容器内执行命令**

- **作用：** 在正在运行的容器内部执行命令。
- **示例：**
    - **执行一次性命令：** `docker exec <container_id> <command>`。
    - **进入交互式环境：** `docker exec -it <container_id> /bin/sh` (或 `/bin/bash`) 。

### **七、Docker 技术原理**

- **cgroups (control groups)：** 限制和隔离进程的资源使用，为每个容器设定 CPU、内存、网络带宽等上限。
- **Namespaces：** 隔离进程的资源视图，使得容器只能看到自己的内部进程、网络和文件目录。
- **本质：** 容器本质上是一个特殊的进程。

### **八、Dockerfile：制作镜像的“图纸”**

- **定义：** 一个用于制作 Docker 镜像的文件，没有后缀名，且 D 大写。
- **常用指令：**
    - `FROM <base_image>`：选择一个基础镜像。
    - `WORKDIR <path>`：设置工作目录，后续命令都在此目录下执行。
    - `COPY <source> <destination>`：将宿主机文件拷贝到镜像中。
    - `RUN <command>`：在镜像构建过程中执行命令。
    - `EXPOSE <port>`：声明镜像提供的服务端口，仅作提示，不强制。
    - `CMD <command>`：容器运行时执行的默认启动命令，一个 Dockerfile 只能有一个 `CMD` 。
    - `ENTRYPOINT`：与 `CMD` 类似，但优先级更高，不易被覆盖 98。
- **构建镜像：** `docker build -t <image_name>:<tag> .` (最后一个点表示在当前目录构建) 。
- **推送镜像：**
    1. **登录 Docker Hub：** `docker login` 。
    2. **重新打 Tag：** `docker tag <image_name> <your_username>/<image_name>:<tag>` (镜像名前必须带上自己的用户名) 。
    3. **推送：** `docker push <your_username>/<image_name>:<tag>` 。

### **九、Docker 网络**

### **1. Bridge（桥接模式）**

- **默认模式：** 所有容器默认连接到这个网络。
- **特点：** 每个容器分配一个内部 IP 地址（通常是 172.17 开头），容器之间可以通过内部 IP 互相访问，但与宿主机网络隔离。

### **2. 自定义子网**

- **创建子网：** `docker network create <network_name>`。
- **特点：**
    - 同一个子网的容器可以互相通信。
    - 跨子网不能通信。
    - 同一个子网的容器可以使用容器名字互相访问（通过 Docker 内部的 DNS 机制）。

### **3. Host（主机模式）**

- **作用：** Docker 容器直接共享宿主机的网络。
- **特点：**
    - 容器直接使用宿主机的 IP 地址。
    - 无需
        - `p` 参数进行端口映射 。
    - 容器内的服务直接运行在宿主机的端口上。

### **4. None（不联网模式）**

- **作用：** 容器不联网。

### **5. 网络管理命令**

- **`docker network ls`：** 列出所有 Docker 网络。
- **`docker network rm <network_name>`：** 删除自定义子网。

### **十、Docker Compose：容器编排**

- **定义：** 一种轻量级的容器编排技术，使用 YAML 文件管理多个容器。
- **优点：** 简化多容器应用的创建和管理，适合个人或单机运行。
- **Docker Compose 文件（`docker-compose.yml`）：**
    - `services`：顶级元素，每个 service 对应一个容器。
    - `image`：指定镜像。
    - `environment`：设置环境变量。
    - `volumes`：设置挂载卷。
    - `ports`：设置端口映射。
    - **自动创建子网：** 同一个 Compose 文件中定义的所有容器会自动加入同一个子网。
    - **启动顺序：** 可以使用 `depends_on` 指定容器启动顺序。
- **常用命令：**
    - **`docker compose up`：** 启动 Compose 文件中定义的所有容器。
    - **`docker compose up -d`：** 在后台启动。
    - **`docker compose down`：** 停止并删除容器。
    - **`docker compose stop`：** 只停止，不删除容器。
    - **`docker compose start`：** 启动已停止的容器。
    - **`docker compose -f <filename> up`：** 指定非标准文件名的 Compose 文件。