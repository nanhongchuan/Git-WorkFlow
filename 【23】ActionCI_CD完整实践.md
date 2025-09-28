
# GitHub Actions CI/CD 实践笔记

## 一、课程内容概述
本节介绍两个完整的 CI/CD 实例，展示软件交付的两种方式：
1. **发布可执行文件到 GitHub Release（Python 项目）**
2. **自动部署到服务器（Java Maven 项目）**

---

## 二、第一个例子：Python 项目自动发布 Release

### 1. 实现目标
将 Python 程序打包为可执行文件（如 `.exe`），自动上传到 GitHub Release，供用户下载。

### 2. 操作流程
1. **新建工作流**
   - 在 GitHub 仓库中进入 **Actions** → 点击 **New workflow**
   - 选择 **set up yourself** 自定义配置
   - 命名文件为 `release.yml`

2. **编写工作流文件**
   ```yaml
   name: create release

   on:
     push:
       tags:
         - 'v*'   # 仅当 tag 以 v 开头时触发，例如 v1.0.0

   permissions:
     contents: write  # 创建 release 需要写权限

   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - name: 打包可执行文件
           uses: actions/setup-python@v3.12
           with:
             entrypoint: your_main_file.py

         - name: 创建 Release
           uses: softprops/action-gh-release@v1
           with:
             files: dist/*
        ```


3. **触发条件**

   * 创建一个以 `v` 开头的 tag，例如：

     ```bash
     git tag v1.0
     git push origin v1.0
     ```
   * 触发后自动执行 workflow。

4. **结果验证**

   * GitHub 自动生成一个 Release。
   * Release 中包含：

     * 打包生成的可执行文件（如 `.exe`）
     * 源代码压缩包
   * 可手动补充 Release 说明内容。

---

## 三、第二个例子：Java Maven 项目自动部署到服务器

### 1. 实现目标

在 push 到 `main` 分支后，自动执行：

* Maven 打包生成 `.jar`
* 通过 SSH 将包上传到服务器
* 在服务器上重启服务，实现自动部署

### 2. 环境准备

#### （1）服务器配置

* 使用百度云或其他云服务器。
* **设置 SSH 密钥登录：**

  ```bash
  ssh-keygen -t rsa
  # 一路回车生成密钥对
  cd ~/.ssh
  cat id_rsa.pub >> authorized_keys
  ```
* 将私钥文件下载到本地保存。

#### （2）服务器端准备部署环境

1. 创建部署目录：

   ```bash
   mkdir /root/springboot
   ```
2. 安装 Java（以 Ubuntu 为例）：

   ```bash
   sudo apt update
   sudo apt install openjdk-17-jdk
   java -version  # 验证安装
   ```

---

### 3. GitHub Action 配置

#### （1）创建 workflow 文件

路径：`.github/workflows/maven.yml`

```yaml
name: maven deploy

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: 检出代码
        uses: actions/checkout@v2

      - name: 设置 JDK 环境
        uses: actions/setup-java@v3
        with:
          java-version: '17'

      - name: Maven 打包
        run: mvn package -DskipTests

      - name: 部署到服务器
        uses: easingthemes/ssh-deploy@main
        with:
          ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}
          source: target/*.jar
          remote-host: your.server.ip
          remote-user: root
          target: /root/springboot/github-action.jar
          script-after: |
            pkill -f java
            nohup java -jar /root/springboot/github-action.jar &
```

#### （2）添加密钥

* 进入仓库 → **Settings → Secrets and variables → Actions**
* 点击 **New repository secret**

  * Name: `SSH_PRIVATE_KEY`
  * Value: 将生成的私钥内容完整粘贴（含开头 `-----BEGIN OPENSSH PRIVATE KEY-----`）

---

### 4. 触发与验证

1. 将代码推送到 main 分支：

   ```bash
   git add .
   git commit -m "auto deploy"
   git push origin main
   ```

2. GitHub 自动执行工作流：

   * Step 1：Maven 构建
   * Step 2：通过 SSH 上传 jar 包
   * Step 3：执行服务器启动命令

3. 登录服务器验证：

   ```bash
   cd /root/springboot
   ls   # 查看 jar 包是否上传
   ps -ef | grep java  # 检查进程是否启动
   ```

4. 浏览器访问 `http://服务器IP:8080/actions`，查看是否正常运行。

---

## 四、实践重点总结

| 分类            | 关键点                                                     | 说明                            |
| ------------- | ------------------------------------------------------- | ----------------------------- |
| **触发方式**      | tag 触发 / push 触发                                        | Python 用 tag，Java 用 push main |
| **权限配置**      | contents: write                                         | 发布 release 需要写权限              |
| **环境准备**      | JDK / SSH 密钥 / 部署目录                                     | 提前在服务器配置好                     |
| **安全注意**      | 密钥放在 GitHub Secrets                                     | 避免泄露敏感信息                      |
| **常见 action** | `softprops/action-gh-release`、`easingthemes/ssh-deploy` | 官方推荐的 release 和部署插件           |
| **自动化流程**     | 打包 → 上传 → 启动服务                                          | 实现持续集成与持续部署                   |

---

## 五、学习要点

* GitHub Actions 可实现 **CI（持续集成）+ CD（持续部署）** 全流程自动化。
* 使用 `tag`、`branch push` 等事件触发构建。
* 所有敏感信息（如 SSH 密钥、API Token）必须放入 GitHub Secrets。
* 自动化部署大大减少了人工干预，提升开发与运维效率。

```
```
