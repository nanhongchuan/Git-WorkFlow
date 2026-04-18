# Webhook 与 REST API 知识点笔记

## 一、概念与区别

### 1. Webhook
- **定义**：Webhook（网络钩子）是一种**被动通知机制**。当 GitHub 上发生事件（如 Push、PR 创建等）时，会通过 HTTP 请求的方式通知到我们指定的服务器。
- **工作原理**：  
  - GitHub 作为 **客户端** 调用我们的 **服务器**。
  - 一旦事件触发（例如 push），GitHub 会发送 HTTP POST 请求到我们配置的 URL。
- **应用场景**：
  - 代码推送自动通知
  - 自动部署、CI/CD
  - 消息推送（如推送到企业微信、Slack 等）

### 2. REST API
- **定义**：GitHub 提供的一组 **主动操作接口**，我们可以通过调用这些 API 实现仓库相关的操作。
- **工作原理**：  
  - GitHub 作为 **服务端**，我们作为 **客户端** 调用。
  - 通过 API 可实现自动化操作，代替网页上的手动操作。
- **应用场景**：
  - 自动创建 issue、release、tag
  - 自动更新仓库内容
  - 项目自动化管理

---

## 二、Webhook 实操流程

### 1. 前置条件
- 需要一台 **有公网 IP 的服务器**
- 在服务器上搭建 **HTTP 服务端**
- 本例使用 **Python + FastAPI**

### 2. 环境准备
```bash
# 检查 Python 版本
python3 --version

# 安装工具
sudo apt install python3-pip python3-venv

# 创建虚拟环境
python3 -m venv webhook_env
source webhook_env/bin/activate

# 安装3个依赖
pip install fastapi uvicorn python-multipart

# 新建一个文件
vi web_hook.py
````

### 3. FastAPI 服务器示例

```python
# 按 i 开始写入
from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.post("/web_hook")
async def print_json(request: Request):
    print(await request.form())
    return {"message": "Data received and printed"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
# 点击 ESC 键，输入wq！ 回车
```

运行服务器：

```bash
python3 webhook.py
```

监听端口：`80`

---

### 4. GitHub Webhook 配置步骤

1. 打开仓库 → **Settings** → **Webhooks** → **Add webhook**
2. 填写：

   * **Payload URL**：服务器地址，如 `http://<your_ip>/webhook`
   * **Content type**：`application/json`
   * **Secret**：自定义密钥（用于签名验证）
   * **事件选择**：如 `Just the push event`
3. 点击 **Add webhook**
4. 进入 **Recent Deliveries** → 可查看 GitHub 测试推送日志

---

### 5. 验证 Webhook Secret

**原理**：
GitHub 使用 Secret 对请求体（payload）做 `SHA-256 HMAC` 签名，并在请求头中传递。
服务器端应使用相同的密钥对 payload 再次签名并比对。

**验证示例代码：**

```python
```python
from fastapi import FastAPI, Request
import uvicorn
import hashlib
import hmac

app = FastAPI()

@app.post("/web_hook")
async def print_json(request: Request):
    body = await request.body()
    verify_signature(body, "tech-shrimp-secret", request.headers["X-Hub-Signature-256"])
    return {"message": "Data received and printed"}

def verify_signature(request_body, secret_token, signature_header):
    hash_object = hmac.new(secret_token.encode('utf-8'), msg=request_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature_header):
        raise Exception("Request signatures didn't match!")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
```

若签名一致，则确认请求确实来自 GitHub。

---

### 6. 域名与 HTTPS 配置

* 可通过 **Cloudflare** 免费实现 HTTPS：

  1. 在 Cloudflare 添加域名解析（A 记录指向服务器 IP）
  2. 替换 Webhook URL 为 `https://yourdomain.com/webhook`
  3. Cloudflare 提供 SSL/TLS 加密，无需在服务器上安装证书

---

### 7. Webhook 可触发的事件

Webhook 支持的事件非常多，包括但不限于：

* 分支操作（创建、删除、保护变更）
* Commit 评论
* Discussion 创建
* Fork 创建
* Issue 创建/评论
* PR 创建/提交
* Release 发布
* Push 操作
  → 几乎 GitHub 上所有动作都可触发，需要勾哪个勾哪个

---

## 三、REST API 实操流程

### 1. 入口文档

官方文档地址：

```
https://docs.github.com/en/rest
```

路径：
**Developer → REST API → API Reference**

### 2. 使用 Postman 发送 API 请求

示例：创建一个 Issue

#### 请求示例（cURL） 

```bash
curl -X POST \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Found a bug",
    "body": "There is a bug in...",
    "assignees": ["yourname"],
    "labels": ["bug"]
  }' \
  https://api.github.com/repos/<username>/<repo>/issues
```

#### 步骤：

1. 打开 **Postman** → Import 上述 curl 命令
2. 在 **Body** 设置为 `raw` + `JSON` 格式
3. 在 **Header** 中添加：

   ```
   Authorization: Bearer <Your Personal Access Token>
   ```
4. 点击 **Send**
5. 若返回状态码 **201 Created** → 表示创建成功

---

### 3. 生成 Personal Access Token

操作路径：

```
GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
```

生成步骤：

1. 点击 **Generate new token**
2. 设置名称与过期时间（例如 7 天）
3. 授权权限：

   * `repo`（仓库访问）
   * `contents`（代码编辑）
   * `issues`（issue 操作）
4. 生成后复制保存（只显示一次）

---

### 4. 示例：创建一个 Release

#### 调用接口

```curl
curl -L \
-X POST \
-H "Accept: application/vnd.github+json" \
-H "Authorization: Bearer <YOUR-TOKEN>" \
-H "X-GitHub-Api-Version: 2022-11-28" \
https://api.github.com/repos/OWNER/REPO/releases \
-d '{"tag_name":"v1.0.0","target_commitish":"master","name":"v1.0.0","body":"Description of the release","draft":false,"prerelease":false,"generate_release_notes":false}'
```

1. 打开 **Postman** → Import 上述 curl 命令
2. 在 **Body** 设置为 `raw` +  `JSON` 格式
3. 在 **Header** 中添加：
```json
{
  "tag_name": "v1.0.0",
  "target_commitish": "master",
  "name": "v1.0.0",
  "body": "Description of the release",
  "draft": false,
  "prerelease": false,
  "generate_release_notes": false
}
```
4. 先在本地创建 tag 并推送：

   ```bash
   git tag v2.0.0
   git push origin v2.0.0 
   ```
5. 进入 Postman 调用接口
 - post上的 
 - header那里 Bearer<YOUR-TOKEN>也要改 
3. 点击`send`，返回 `201 Created` 表示成功
   页面可见新创建的 Release。

---

### 5. 使用代码调用 API（Python 示例）

Postman 可自动生成请求代码，示例：

```python
import requests

url = "https://api.github.com/repos/<username>/<repo>/issues"
headers = {
    "Authorization": "Bearer <TOKEN>",
    "Content-Type": "application/json"
}
data = {
    "title": "Found a bug",
    "body": "Description here",
    "labels": ["bug"]
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code, response.json())
```
* 在程序中使用这段代码可以达到同样的效果

---

## 四、总结对比

| 对比项  | Webhook        | REST API              |
| ---- | -------------- | --------------------- |
| 调用方向 | GitHub → 服务器   | 服务器 → GitHub          |
| 功能定位 | 事件通知           | 主动操作                  |
| 使用场景 | 被动监听（Push、PR等） | 主动控制（创建issue、release） |
| 触发方式 | GitHub 事件触发    | 手动/程序发起               |
| 安全性  | Secret 验证签名    | Token 鉴权              |
| 典型用途 | CI/CD 自动部署     | 自动化脚本、机器人操作           |

---

## 五、延伸应用

* **Webhook + REST API 联合使用**

  * 例如：Push 事件触发 Webhook → 服务器自动调用 REST API 创建 Release、发送通知等。
* **自动化示例**

  * 自动合并 PR
  * 自动发布版本
  * 自动同步仓库状态到内部系统