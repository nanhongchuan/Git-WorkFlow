# 从 0 到上线一个完整网站：域名绑定、HTTPS 自动证书、nginx 多服务配置、前后端 + API 跑通（超详细实战版）

> 这是一份按**真实上线顺序**写的实战教程。  
> 目标不是只把页面“跑起来”，而是让你从 0 完整走到：
>
> - 域名能访问
> - HTTP 能跳 HTTPS
> - TLS 证书自动续期
> - nginx 能同时托管前端和 API
> - 后端进程能被 systemd 管理
> - 你知道哪里容易出错，以及怎么排查
>
> 这份教程尽量兼容常见 Linux 服务器思路，命令以 **nginx + Linux + Certbot + Node/Python 风格后端** 为主。  
> 你也可以把它当成“以后上线任何网站”的底层模板。

---

# 目录

1. [先建立完整脑图：一个网站上线到底经过哪些层](#先建立完整脑图一个网站上线到底经过哪些层)
2. [你要先准备什么](#你要先准备什么)
3. [整体架构先看懂](#整体架构先看懂)
4. [第 0 步：先明确你要上线的是什么](#第-0-步先明确你要上线的是什么)
5. [第 1 步：买域名，并把域名解析到服务器](#第-1-步买域名并把域名解析到服务器)
6. [第 2 步：服务器基础准备](#第-2-步服务器基础准备)
7. [第 3 步：安装 nginx](#第-3-步安装-nginx)
8. [第 4 步：把前端静态文件准备好](#第-4-步把前端静态文件准备好)
9. [第 5 步：先只用 IP 跑通一个最简单的网站](#第-5-步先只用-ip-跑通一个最简单的网站)
10. [第 6 步：给 nginx 配一个正式站点配置文件](#第-6-步给-nginx-配一个正式站点配置文件)
11. [第 7 步：把域名接入 nginx](#第-7-步把域名接入-nginx)
12. [第 8 步：先用 HTTP 跑通域名访问](#第-8-步先用-http-跑通域名访问)
13. [第 9 步：准备后端 API 服务](#第-9-步准备后端-api-服务)
14. [第 10 步：用 systemd 托管后端进程](#第-10-步用-systemd-托管后端进程)
15. [第 11 步：用 nginx 做前后端分流](#第-11-步用-nginx-做前后端分流)
16. [第 12 步：申请 HTTPS 证书（Let’s Encrypt + Certbot）](#第-12-步申请-https-证书lets-encrypt--certbot)
17. [第 13 步：把 HTTP 自动跳转到 HTTPS](#第-13-步把-http-自动跳转到-https)
18. [第 14 步：验证自动续期](#第-14-步验证自动续期)
19. [第 15 步：一台服务器托管多个站点](#第-15-步一台服务器托管多个站点)
20. [第 16 步：常见目录组织方式](#第-16-步常见目录组织方式)
21. [第 17 步：完整示例配置（可直接参考）](#第-17-步完整示例配置可直接参考)
22. [第 18 步：完整上线检查清单](#第-18-步完整上线检查清单)
23. [第 19 步：最常见故障与排查方法](#第-19-步最常见故障与排查方法)
24. [第 20 步：生产环境建议](#第-20-步生产环境建议)
25. [第 21 步：一张图总结全部关系](#第-21-步一张图总结全部关系)
26. [命令速查表](#命令速查表)

---

# 先建立完整脑图：一个网站上线到底经过哪些层

很多人一开始会把“网页打不开”理解成一个单点问题，实际上不是。  
一个网站从“文件在服务器里”到“用户浏览器能打开”，中间至少要经过下面这些层：

```text
浏览器
   ↓
输入域名（或 IP）
   ↓
DNS 把域名解析成服务器公网 IP
   ↓
浏览器访问 IP:80 或 IP:443
   ↓
云安全组 / 防火墙允许这个端口通过
   ↓
nginx 在对应端口监听
   ↓
nginx 判断：
   - 这是前端页面请求？
   - 还是 API 请求？
   ↓
如果是前端请求：
   nginx 去磁盘找静态文件（HTML/CSS/JS）
   ↓
如果是 API 请求：
   nginx 转发给本机后端程序
   ↓
浏览器收到响应并渲染
```

你只要记住：

> **上线一个完整网站，本质上就是把“域名、端口、nginx、前端文件、后端程序、证书”这几层串通。**

---

# 你要先准备什么

在开始前，你至少要有：

1. 一台 Linux 服务器  
   - 最好有公网 IP
   - 能 SSH 登录
   - 你有 root 或 sudo 权限

2. 一个域名  
   - 比如 `example.com`
   - 你能登录它的 DNS 管理后台

3. 一个前端项目  
   - 最简单可以只是一个 `index.html`
   - 如果是 React/Vue 项目，至少要能打包出静态文件

4. 一个后端程序（可选，但本教程会演示）  
   - 可以是 Node、Python、Go、Java 任意一种
   - 只要它能在本机某个端口上跑起来并返回 HTTP 响应

---

# 整体架构先看懂

我们这份教程最终会搭成这个结构：

```text
域名：example.com
        ↓
      nginx
   ┌───────────────┬────────────────┐
   │               │                │
前端页面请求       API 请求         HTTPS 终止
/、/index.html     /api/*           443 证书
   │               │
静态文件目录       127.0.0.1:3000 的后端程序
```

也就是说：

- nginx 负责做**统一入口**
- 前端资源由 nginx 直接返回
- 后端 API 由 nginx 反向代理到本机服务
- 外部用户只看见一个域名，不会直接看到你的后端端口

---

# 第 0 步：先明确你要上线的是什么

这一点非常关键，因为不同网站的部署方式不一样。

---

## 情况 A：纯静态网站

例如：

- 一个单独的 HTML 页面
- 一个打包后的静态站点（React/Vue/Next export 后的纯静态文件）
- 一个文档页、作品集、产品介绍页

特点：

- 只需要 nginx
- 不需要后端服务
- nginx 直接读文件即可

---

## 情况 B：前端 + API

例如：

- 前端页面用 React/Vue
- 后端接口用 Node / Python / Java
- 页面里会请求 `/api/user`、`/api/login` 之类的接口

特点：

- nginx 负责统一入口
- 前端走静态托管
- API 走反向代理

---

## 情况 C：只有后端程序

例如：

- 一个 FastAPI / Flask 服务
- 一个 Node Express 服务
- 一个管理面板

特点：

- nginx 主要做反向代理
- 有时不一定需要静态目录

---

本教程按 **情况 B** 来讲，因为它覆盖面最大。  
你学会 B，A 和 C 都会更简单。

---

# 第 1 步：买域名，并把域名解析到服务器

这是“让别人不用记 IP，而用域名访问你的网站”的前提。

---

## 1. 域名是什么

域名就是 IP 的人类可读别名。

例如：

- 服务器公网 IP：`1.2.3.4`
- 域名：`example.com`

用户更愿意访问：

```text
https://example.com
```

而不是：

```text
http://1.2.3.4
```

---

## 2. 最常见要配的 DNS 记录

### 根域名

让：

```text
example.com
```

指向你的服务器 IP

通常加一条：

- 类型：`A`
- 主机记录 / Name：`@`
- 值 / Value：你的公网 IP

---

### www 子域名

让：

```text
www.example.com
```

也能访问

常见做法有两种：

#### 做法 1：再加一条 A 记录

- 类型：`A`
- Name：`www`
- Value：你的公网 IP

#### 做法 2：CNAME 到根域名

- 类型：`CNAME`
- Name：`www`
- Value：`example.com`

---

## 3. DNS 生效不是立刻的

有时几分钟，有时几小时。  
所以如果刚配好域名但访问还不通，不一定是 nginx 问题，也可能只是 DNS 还没完全生效。

---

## 4. 怎么检查域名是否已经解析到你的服务器

你可以在本地或服务器上执行：

```bash
ping example.com
```

或者更稳一点：

```bash
nslookup example.com
```

如果返回的是你的公网 IP，就说明解析基本对了。

---

# 第 2 步：服务器基础准备

在正式部署前，先做这些基础确认。

---

## 1. 确认公网 IP

可以执行：

```bash
curl ip.sb
```

或者：

```bash
curl ifconfig.me
```

记住这个 IP，因为 DNS 要指向它。

---

## 2. 确认安全组 / 防火墙开放端口

至少要允许：

- `80/tcp`（HTTP）
- `443/tcp`（HTTPS）
- `22/tcp`（SSH）

如果你的 API 在本机跑 `3000`，**不要对公网开放 3000**。  
它只需要让 nginx 在本机访问即可。

---

## 3. 建议先规划目录结构

一个比较清晰的目录结构，例如：

```text
/data/www/example-frontend/     # 前端静态文件
/data/apps/example-api/         # 后端程序
/etc/nginx/conf.d/              # nginx 站点配置
```

你也可以用 `/var/www/`，都可以。  
重点是：**别把一切都堆在 /root**。

---

# 第 3 步：安装 nginx

不同系统安装命令略有区别。

---

## RHEL / CentOS / Rocky / 阿里云 Linux

```bash
dnf install -y nginx
```

有些旧系统是：

```bash
yum install -y nginx
```

---

## Ubuntu / Debian

```bash
apt update
apt install -y nginx
```

---

## 启动 nginx

```bash
systemctl start nginx
```

设置开机自启：

```bash
systemctl enable nginx
```

查看状态：

```bash
systemctl status nginx
```

如果你看到：

```text
Active: active (running)
```

说明 nginx 已经起来了。

---

# 第 4 步：把前端静态文件准备好

---

## 方案 1：你只有一个 HTML 文件

比如：

```text
/root/index.html
```

那你可以准备一个目录：

```bash
mkdir -p /data/www/example-frontend
cp /root/index.html /data/www/example-frontend/index.html
```

---

## 方案 2：你有一个前端打包产物

例如 React/Vue 打包后会得到一堆文件：

```text
dist/
  index.html
  assets/
  favicon.ico
```

那就把整个目录内容放进去：

```bash
mkdir -p /data/www/example-frontend
cp -r dist/* /data/www/example-frontend/
```

---

## 为什么不建议直接用 `/root`

技术上不是绝对不行，但不推荐，原因有三个：

1. `/root` 是 root 用户家目录，权限更敏感
2. nginx 读取 `/root` 内容更容易碰到权限问题
3. 以后迁移、备份、管理都更乱

更稳妥的是：

- `/data/www/...`
- `/var/www/...`

---

# 第 5 步：先只用 IP 跑通一个最简单的网站

在接入域名和证书之前，**先确认 nginx + 文件本身没问题**。

---

## 1. 最简单的测试配置

先看 nginx 主配置是否会 include 站点配置：

```bash
grep -n "include" /etc/nginx/nginx.conf
```

你通常会看到：

```nginx
include /etc/nginx/conf.d/*.conf;
```

---

## 2. 新建一个站点配置

例如：

```bash
vim /etc/nginx/conf.d/example.conf
```

写入：

```nginx
server {
    listen 80;
    server_name _;

    location / {
        root /data/www/example-frontend;
        index index.html;
    }
}
```

---

## 3. 检查配置语法

```bash
nginx -t
```

如果看到：

```text
syntax is ok
test is successful
```

说明配置没写错。

---

## 4. 重载 nginx

```bash
systemctl reload nginx
```

---

## 5. 浏览器直接访问公网 IP

```text
http://你的公网IP
```

如果能打开页面，说明下面这些至少已经通了：

- nginx 在跑
- 80 端口开放
- root 配置没错
- index.html 存在

---

# 第 6 步：给 nginx 配一个正式站点配置文件

等 IP 已经能通以后，再把配置改成正式站点的样子。

---

## 一个完整的基础 server 配置

```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    location / {
        root /data/www/example-frontend;
        index index.html;
    }
}
```

---

## 每一行在干什么

### `server { ... }`

表示一个站点配置块。  
你可以理解为：“下面这一整段，是一个网站的规则”。

---

### `listen 80;`

监听 HTTP 默认端口。  
当浏览器访问：

```text
http://example.com
```

本质上就是访问 `80` 端口。

---

### `server_name example.com www.example.com;`

表示这个站点处理这两个域名的请求：

- `example.com`
- `www.example.com`

这样 nginx 就知道：请求进来以后，如果 Host 是这两个域名，就用这套配置处理。

---

### `location / { ... }`

表示匹配以 `/` 开头的请求，也就是网站的大多数请求。

---

### `root /data/www/example-frontend;`

告诉 nginx：

> 这个网站的静态文件从 `/data/www/example-frontend` 这个目录开始找。

---

### `index index.html;`

表示当用户访问的是目录时，默认返回 `index.html`。  
所以访问：

```text
http://example.com/
```

nginx 会尝试找：

```text
/data/www/example-frontend/index.html
```

---

# 第 7 步：把域名接入 nginx

如果 DNS 已经指向服务器 IP，那么这一步主要是让 nginx 用域名匹配请求。

---

## 为什么 `server_name` 很重要

nginx 收到一个请求后，不只是看端口，还会看请求头里的 Host。

例如浏览器访问：

```text
http://example.com
```

请求里会带一个 Host：

```text
Host: example.com
```

nginx 会根据这个 Host 去匹配 `server_name`。

所以：

- 配了 `server_name example.com;`，访问这个域名就会匹配到
- 没配或配错了，可能就落到默认站点上

---

## 推荐写法

```nginx
server_name example.com www.example.com;
```

这样根域名和 www 都覆盖了。

---

# 第 8 步：先用 HTTP 跑通域名访问

在申请 HTTPS 之前，先确认域名 HTTP 是好的。

---

## 1. 重载 nginx

```bash
nginx -t
systemctl reload nginx
```

---

## 2. 浏览器访问

```text
http://example.com
http://www.example.com
```

如果这时打不开，优先排查：

1. DNS 是否真的指向了你的公网 IP
2. 安全组是否放开 80
3. nginx 是否在跑
4. `server_name` 是否写对
5. 这个站点配置是否已被 include

---

# 第 9 步：准备后端 API 服务

这一步开始做“前后端 + API”的完整结构。

---

## 原则

后端程序通常不直接暴露给公网，而是：

- 后端程序只监听本机端口，例如 `127.0.0.1:3000`
- 外部用户访问的是 nginx
- nginx 再把 `/api/` 请求转发给后端程序

这样更安全，也更统一。

---

## 示例：Node 版最简 API

例如在：

```text
/data/apps/example-api/server.js
```

写一个简单程序：

```javascript
const http = require("http");

const server = http.createServer((req, res) => {
  if (req.url === "/api/hello") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ message: "hello from api" }));
    return;
  }

  res.writeHead(404, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ error: "not found" }));
});

server.listen(3000, "127.0.0.1", () => {
  console.log("API listening on 127.0.0.1:3000");
});
```

运行：

```bash
node /data/apps/example-api/server.js
```

本机测试：

```bash
curl http://127.0.0.1:3000/api/hello
```

如果返回 JSON，说明后端本身已经 OK。

---

## 示例：Python 版最简 API（Flask 风格伪思路）

重点不是语言，而是结构：  
只要后端能在本机某个端口正常响应，nginx 就能代理它。

---

# 第 10 步：用 systemd 托管后端进程

正式上线时，不建议直接靠一个终端窗口手动跑后端。  
更稳妥的方式是：让 systemd 管理它。

---

## 为什么要用 systemd

因为它可以：

- 开机自启
- 自动拉起
- 统一看状态
- 统一看日志
- 崩了以后更容易恢复

---

## 例子：给 Node API 写一个 service

新建：

```bash
vim /etc/systemd/system/example-api.service
```

写入：

```ini
[Unit]
Description=Example API Service
After=network.target

[Service]
Type=simple
WorkingDirectory=/data/apps/example-api
ExecStart=/usr/bin/node /data/apps/example-api/server.js
Restart=always
RestartSec=3
User=root
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

---

## 让它生效

```bash
systemctl daemon-reload
systemctl enable example-api
systemctl start example-api
systemctl status example-api
```

如果状态是 `active (running)`，说明后端已被系统托管。

---

## 为什么这里后端不监听 0.0.0.0

因为我们只希望 nginx 在本机访问它。  
所以绑定到：

```text
127.0.0.1:3000
```

通常更安全。

---

# 第 11 步：用 nginx 做前后端分流

这一步是完整网站的关键：  
**同一个域名，同时提供前端页面和 API。**

---

## 目标效果

- 用户访问：
  ```text
  https://example.com/
  ```
  打开前端页面

- 前端页面里请求：
  ```text
  https://example.com/api/hello
  ```
  实际被 nginx 转发到：
  ```text
  http://127.0.0.1:3000/api/hello
  ```

---

## nginx 配置示例

```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    location / {
        root /data/www/example-frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 为什么这里加了 `try_files`

这一句：

```nginx
try_files $uri $uri/ /index.html;
```

对单页应用（SPA）很重要。

如果你的 React/Vue 前端使用前端路由，比如：

```text
/example
/dashboard
/user/123
```

这些路径在磁盘上不一定真的有对应文件。  
如果不加 `try_files`，nginx 可能直接返回 404。

加了它以后，含义大致是：

1. 先试着找真实文件 `$uri`
2. 再试目录 `$uri/`
3. 都找不到，就回退到 `/index.html`

这样前端路由才能接管。

---

## `proxy_pass` 有什么作用

```nginx
proxy_pass http://127.0.0.1:3000;
```

意思是：

> 把这个 location 里的请求转发给本机 3000 端口的后端程序。

---

## 为什么要加 `proxy_set_header`

这些头常用来把原始请求信息传给后端。

例如：

- 原始 Host 是什么
- 客户端真实 IP 是谁
- 外部访问用的是 http 还是 https

很多后端框架在生成回调地址、记录日志、做鉴权时会用到这些头。

---

# 第 12 步：申请 HTTPS 证书（Let’s Encrypt + Certbot）

到这一步之前，建议你已经确认：

- `http://example.com` 能打开
- `http://www.example.com` 能打开
- nginx 配置没问题
- 域名 DNS 已经正确指向服务器

因为 Certbot 常见的失败原因之一，就是域名压根还没正确指到当前机器。

---

## 1. Let’s Encrypt 是什么

它是一个免费证书颁发机构（CA），可以给你的域名签发 TLS 证书。  
有了证书，你的网站才能用 HTTPS。

---

## 2. Certbot 是什么

它是最常见的 ACME 客户端之一。  
它可以帮你：

- 申请证书
- 自动修改 nginx 配置（如果用 nginx 插件）
- 设置自动续期

---

## 3. 常见安装方式

不同发行版略有不同，但思路一致。  
你可以使用系统包、Snap，或者发行版推荐方式。

常见 Ubuntu 系列会用类似：

```bash
apt install certbot python3-certbot-nginx
```

RHEL 系则会按对应仓库安装。  
如果系统仓库版本不理想，也可以参考官方文档选择合适方式。

---

## 4. 使用 nginx 插件申请证书

最常见命令类似：

```bash
certbot --nginx -d example.com -d www.example.com
```

执行后，Certbot 会大致做这些事：

1. 验证你确实控制这个域名
2. 向 Let’s Encrypt 申请证书
3. 找到 nginx 对应站点配置
4. 自动插入 HTTPS 配置
5. 询问你是否要自动跳转 HTTP → HTTPS

---

## 5. 证书成功后会发生什么

成功后，nginx 通常会得到：

- 一个监听 `443 ssl` 的 server
- 一个证书文件路径
- 一个私钥文件路径
- 一个 HTTP 到 HTTPS 的重定向

常见证书目录类似：

```text
/etc/letsencrypt/live/example.com/
```

里面会有：

- `fullchain.pem`
- `privkey.pem`

---

# 第 13 步：把 HTTP 自动跳转到 HTTPS

如果 Certbot 自动帮你改了，一般会生成类似两段配置。

---

## HTTP 重定向配置

```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    return 301 https://$host$request_uri;
}
```

---

## HTTPS 正式站点配置

```nginx
server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    location / {
        root /data/www/example-frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 为什么重定向很重要

因为这样用户无论输入：

```text
http://example.com
```

还是：

```text
https://example.com
```

最终都会落到 HTTPS，体验更一致，也更安全。

---

# 第 14 步：验证自动续期

Let’s Encrypt 证书不是永久的。  
它通常有效期较短，因此自动续期非常重要。

---

## 1. 续期机制

Certbot 通常会安装一个 systemd timer 或 cron 任务，定期检查证书是否临近过期。

---

## 2. 测试续期流程

建议手动跑一次模拟测试：

```bash
certbot renew --dry-run
```

如果这个命令能通过，通常说明自动续期链路没大问题。

---

## 3. 你不需要每次都手工续期

正常配置好以后，Certbot 会自动处理。  
但上线后建议你至少手动验证过一次 `--dry-run`。

---

# 第 15 步：一台服务器托管多个站点

nginx 非常适合做这件事。

---

## 场景示例

同一台服务器上放：

- `example.com`
- `admin.example.com`
- `blog.example.com`

每个站点都可以有自己独立配置：

```text
/etc/nginx/conf.d/example.conf
/etc/nginx/conf.d/admin.conf
/etc/nginx/conf.d/blog.conf
```

---

## 多站点的核心原理

还是靠 `server_name` 匹配。

例如：

```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    ...
}

server {
    listen 80;
    server_name admin.example.com;
    ...
}
```

浏览器访问哪个 Host，就会匹配到对应 server。

---

## 一台服务器托管多个 API 服务也一样

比如：

- `api1.example.com` → 127.0.0.1:3001
- `api2.example.com` → 127.0.0.1:3002

nginx 只负责根据域名把请求分到不同后端。

---

# 第 16 步：常见目录组织方式

推荐把配置和代码分开。

---

## 一个比较整洁的例子

```text
/data/www/
  example-frontend/
    index.html
    assets/
  admin-frontend/
    index.html

/data/apps/
  example-api/
    server.js
  admin-api/
    app.py

/etc/nginx/conf.d/
  example.conf
  admin.conf
```

这样有几个好处：

1. 看一眼就知道谁是前端、谁是后端
2. 迁移项目更方便
3. 日后多站点不会乱

---

# 第 17 步：完整示例配置（可直接参考）

下面给你一份比较接近真实生产结构的示例。

---

## HTTP：统一跳转 HTTPS

```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    return 301 https://$host$request_uri;
}
```

---

## HTTPS：前端 + API

```nginx
server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    access_log /var/log/nginx/example.access.log;
    error_log /var/log/nginx/example.error.log;

    location / {
        root /data/www/example-frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 为什么我建议单独写 access_log 和 error_log

因为站点多起来以后，分开日志更容易排查。

例如：

- 某个 API 502
- 某个页面一直 404
- 某个站点流量异常

分站点日志会好排查很多。

---

# 第 18 步：完整上线检查清单

在你觉得“应该没问题了”的时候，用这份清单一条条过。

---

## A. 域名层

- [ ] 域名已经购买
- [ ] `A` 记录已指向公网 IP
- [ ] `www` 是否也已配置
- [ ] `ping` / `nslookup` 能解析到正确 IP

---

## B. 服务器层

- [ ] 服务器有公网 IP
- [ ] SSH 能正常登录
- [ ] 安全组开放了 80 / 443
- [ ] 系统防火墙没有拦住 80 / 443

---

## C. nginx 层

- [ ] nginx 已安装
- [ ] `systemctl status nginx` 为 running
- [ ] `nginx -t` 语法通过
- [ ] `systemctl reload nginx` 成功
- [ ] `server_name` 配置正确
- [ ] `root` 指向目录真实存在
- [ ] `index.html` 存在

---

## D. 后端层

- [ ] 后端服务本机可访问
- [ ] `curl http://127.0.0.1:3000/...` 能返回正常内容
- [ ] 已由 systemd 托管
- [ ] `systemctl status example-api` 正常

---

## E. HTTPS 层

- [ ] `certbot --nginx ...` 成功执行
- [ ] 443 端口放通
- [ ] 浏览器访问证书正常
- [ ] `certbot renew --dry-run` 通过

---

# 第 19 步：最常见故障与排查方法

这部分非常重要，因为真正的上线能力，很大一部分来自排错能力。

---

## 问题 1：IP 可以打开，域名打不开

优先排查：

1. DNS 解析是否正确
2. `server_name` 是否配置正确
3. 域名是否真的解析到了这台机器
4. DNS 是否还在传播中

---

## 问题 2：HTTP 能打开，HTTPS 不行

优先排查：

1. 443 端口是否放开
2. 证书是否申请成功
3. nginx 是否真的有 `listen 443 ssl`
4. 证书路径是否存在
5. `nginx -t` 是否通过

---

## 问题 3：页面能打开，API 502

这通常说明：

> nginx 能工作，但后端没接住请求。

优先排查：

1. 后端服务是否在运行
2. `curl http://127.0.0.1:3000/api/...` 是否能通
3. `proxy_pass` 地址是否写对
4. 后端是不是只监听了别的地址/端口
5. systemd 服务是不是崩了
6. nginx error log 有没有 502 线索

---

## 问题 4：刷新前端路由后 404

这是 SPA 很典型的问题。

优先看：

```nginx
try_files $uri $uri/ /index.html;
```

有没有写。

---

## 问题 5：Certbot 申请失败

最常见原因：

1. 域名没正确指向服务器
2. 80 端口没开放
3. nginx 配置冲突
4. 站点配置不规范，Certbot 找不到对应 server block
5. DNS 还没生效

---

## 问题 6：nginx 配置修改了但没生效

检查顺序：

1. `nginx -t`
2. `systemctl reload nginx`
3. 当前改的是不是被 include 的那个文件
4. 是否其实访问到了另一个 server block
5. 浏览器缓存 / CDN 缓存

---

## 问题 7：VS Code 里看不到 `/usr/share/nginx/html`

这不是 nginx 问题，而是你当前 VS Code 打开的目录树问题。

如果你打开的是：

```text
/root
```

那么左侧只会显示 `/root` 下面的内容。  
而 `/usr/share/nginx/html` 是另一个顶层目录分支。

Linux 顶层大致是：

```text
/
├── root
├── usr
├── etc
├── var
```

所以你需要在 VS Code 里：

- 重新打开 `/`
- 或直接打开 `/usr/share/nginx/html`
- 或直接打开你真实使用的目录，例如 `/data/www/example-frontend`

---

# 第 20 步：生产环境建议

这部分是“从能跑”到“更稳”的差别。

---

## 1. 不要直接把业务目录全放在 `/root`

更推荐：

- `/data/www/`
- `/data/apps/`
- `/var/www/`

---

## 2. 后端不要直接对公网开放

更推荐：

- 后端只监听 `127.0.0.1`
- 外部统一走 nginx
- 统一做 TLS、日志、限流、域名路由

---

## 3. 每个站点一个 nginx 配置文件

例如：

```text
/etc/nginx/conf.d/example.conf
/etc/nginx/conf.d/admin.conf
```

不要把所有站点都写进一个大文件里。

---

## 4. 每个后端一个独立 systemd service

例如：

```text
example-api.service
admin-api.service
```

这样状态和日志更清晰。

---

## 5. 先本机通，再外网通

排错时，永远先确认：

```bash
curl http://127.0.0.1:3000
curl http://127.0.0.1
```

如果本机都不通，先别怪公网。

---

## 6. 上线前先把日志想好

至少建议：

- 每个站点分开 access log / error log
- 后端进程能用 `journalctl -u xxx -f` 看日志
- 出问题时有证据，不靠猜

---

# 第 21 步：一张图总结全部关系

```text
用户浏览器
   ↓
访问 https://example.com
   ↓
DNS 把 example.com 解析到服务器公网 IP
   ↓
公网 443 进入服务器
   ↓
nginx 接住请求
   ├── 如果是 /、/assets/、/index.html
   │      ↓
   │    返回 /data/www/example-frontend 里的静态文件
   │
   └── 如果是 /api/*
          ↓
        转发给 127.0.0.1:3000 的后端程序
          ↓
        后端返回 JSON
          ↓
        nginx 再返回给浏览器
```

你只要把这张图真正理解了，后面的很多部署问题都会顺很多。

---

# 命令速查表

## nginx 基础

```bash
systemctl start nginx
systemctl stop nginx
systemctl restart nginx
systemctl reload nginx
systemctl status nginx
nginx -t
```

---

## 端口 / 监听检查

```bash
ss -tlnp | grep 80
ss -tlnp | grep 443
ss -tlnp | grep 3000
```

---

## 本机测试

```bash
curl -I http://127.0.0.1
curl -I http://127.0.0.1:3000
curl http://127.0.0.1:3000/api/hello
```

---

## 域名解析检查

```bash
ping example.com
nslookup example.com
```

---

## systemd 管理后端

```bash
systemctl daemon-reload
systemctl enable example-api
systemctl start example-api
systemctl status example-api
journalctl -u example-api -f
```

---

## Certbot 常用

```bash
certbot --nginx -d example.com -d www.example.com
certbot renew --dry-run
```

---

# 最后一段总结

从 0 到上线一个完整网站，真正要打通的是这几件事：

1. **域名是否正确指向你的服务器**
2. **80 / 443 是否真的能进来**
3. **nginx 是否正确监听并匹配这个域名**
4. **前端文件是否放在 nginx 能读取的目录**
5. **后端服务是否在本机正常运行**
6. **nginx 是否把 `/api/` 正确代理到了后端**
7. **HTTPS 是否申请成功并配置了自动续期**

把这些层次分清楚之后，你会发现：

> 网站上线不是“某一条命令神奇成功”，而是把每一层都接好。

---

# 一句话终极总结

**域名负责把人带到服务器，nginx 负责接待和分流，前端负责页面，后端负责业务，HTTPS 负责加密。**

