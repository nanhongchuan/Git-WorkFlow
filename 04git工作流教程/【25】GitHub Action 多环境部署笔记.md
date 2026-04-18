# 🧩 GitHub Action 多环境部署笔记

## 一、概述

在软件正式发布到生产环境之前，通常会经过多个测试与验证阶段。
**多环境管理配置（Environments）** 是 CI/CD（持续集成与持续部署）的重要部分，能够让不同环境（如 QA、Stage、Production）具备独立的配置、审批机制和密钥变量。

---

## 二、GitHub 多环境配置步骤

### 1️⃣ 进入环境配置

* 打开 GitHub 仓库 → 进入 **Settings → Environments**
* 点击 **New environment** 新建环境
  本例创建了三个环境：

  * `qa`（测试环境）
    - “QA 环境”是 Quality Assurance environment 的缩写，意思是**质量保证环境**。
  * `stg` / `stage`（沙箱环境）
    - STG（Staging）环境，又称 预发布环境 或 沙箱环境，是介于测试环境（QA）与生产环境（Production）之间的关键环节。
  * `production`（生产环境）
    - Production 环境是软件系统 正式对外提供服务的运行环境，也就是用户实际访问、操作、使用的那一套系统。所有最终上线的功能、数据、接口、日志等都在这个环境中真实运行。

---

## 三、环境配置内容

每个环境都可以独立配置以下三类信息：

### （1）Protection Rules（保护规则）

定义部署前的限制条件：

* **审批机制（Required reviewers）**
  需特定人员审批后方可部署，例如生产环境需领导审核。
* **等待时间（Wait timer）**
  部署前等待指定时间，允许团队做最后检查。
* **管理员豁免**
  勾选后，管理员可绕过规则约束。
* **分支限制（Branch restriction）**
  限制特定分支可部署到特定环境，如：

  * `qa` 分支 → 仅部署至 QA 环境
  * `main` 分支 → 部署至 Stage 环境
  * `release` 分支 → 部署至 Production 环境

---

### （2）Environment Secrets（环境密钥）

用于存放敏感信息（如服务器密钥、数据库密码）。

* 示例：

  ```bash
  SECRET_NAME: SSH_PRIVATE_KEY
  ```

  每个环境拥有独立的密钥，确保安全隔离。

---

### （3）Environment Variables（环境变量）

配置环境特有的普通变量（如服务器 IP）。

* 示例：

  ```bash
  VARIABLE_NAME: SERVER_IP
  VALUE: 192.168.x.x
  ```

  在 Action 中可通过 `env` 调用。

---

## 四、示例环境设置

| 环境名          | 特征       | 等待时间 | 审批要求   | 密钥与变量            |
| ------------ | -------- | ---- | ------ | ---------------- |
| `qa`         | 测试环境，最宽松 | 无    | 否      | QA密钥、QA服务器IP     |
| `stg`        | 沙盒环境     | 1分钟  | 否      | STG密钥、STG服务器IP   |
| `production` | 生产环境，最严格 | 1分钟  | ✅ 需要审批 | PROD密钥、PROD服务器IP |

---

## 五、创建 Action 流程

进入项目的 `.github/workflows` 目录，新建一个 Action 文件。

### 示例结构：

```yaml
name: multi-env-deploy
on:
  workflow_dispatch:   # 手动触发

jobs:
  deploy_qa:
    runs-on: ubuntu-latest
    environment: qa
    steps:
      - name: Deploy QA
        run: echo "Deploying to QA environment"

  deploy_stg:
    runs-on: ubuntu-latest
    environment: stg
    steps:
      - name: Deploy Staging
        run: echo "Deploying to Staging environment"

  deploy_prod:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy Production
        run: echo "Deploying to Production environment"
```

### 注意事项：

* `environment:` 的名称必须与配置的环境名一致。
* 每个 `job` 可读取对应环境的 secrets 与 variables。
* 三个部署任务可并行执行，但会受等待时间和审批机制影响。

---

## 六、执行与审批流程

1. 进入 **Actions** → 手动触发工作流。
2. `qa` 环境先执行（无等待时间）。
3. `stg` 环境等待 1 分钟后执行。
4. `production` 环境等待 1 分钟并 **等待审批**：

   * 页面显示 `Waiting for a review`
   * 点击 **Review deployment → Approve** 即可批准执行。

---

## 七、在 Action 中使用环境变量与密钥

### 示例：

```yaml
- name: SSH to Server
  run: |
    ssh -i ${{ secrets.SSH_PRIVATE_KEY }} user@${{ env.SERVER_IP }}
```

说明：

* `${{ secrets.SSH_PRIVATE_KEY }}` → 获取当前环境的密钥
* `${{ env.SERVER_IP }}` → 获取当前环境的服务器 IP
* Action 会根据 `environment` 自动匹配对应环境的变量与密钥。

---

## 八、总结

| 分类   | 内容                           |
| ---- | ---------------------------- |
| 配置位置 | 仓库 → Settings → Environments |
| 核心功能 | 审批、等待、分支限制、变量隔离              |
| 安全性  | 每个环境独立管理密钥与变量                |
| 灵活性  | QA、STG、PROD 可并行部署、独立控制       |
| 实践意义 | 支撑 CI/CD 流程中的多阶段部署与安全审查      |

---

✅ **核心记忆点**

* Environment 是 GitHub Action 管理多环境部署的关键。
* 可独立配置 **保护规则 + 密钥 + 变量**。
* 与 `jobs.environment` 名称一一对应。
* 支持 **审批机制 + 延迟部署 + 分支约束**。
* 可通过 `${{ secrets.xxx }}` 与 `${{ env.xxx }}` 引用环境特定配置。

---