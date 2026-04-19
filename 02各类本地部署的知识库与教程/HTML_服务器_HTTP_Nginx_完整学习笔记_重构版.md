# HTML、HTTP 服务、端口、`http.server`、nginx、systemctl、进程：一份讲透的完整笔记

> 这是一份给小白看的系统化笔记。目标不是只记住几条命令，而是把这些问题真正串起来：
>
> - 为什么 HTML 文件放到服务器上，外部不一定能访问
> - `python3 -m http.server` 到底做了什么
> - 为什么浏览器默认 80，而 `http.server` 默认 8000
> - nginx 是什么，和 `http.server` 有什么区别
> - `systemctl`、进程、worker、`ps -ef | grep` 分别在看什么
>
> 学完这份笔记，你应该能把“文件、服务、端口、进程、访问链路”一次性理顺。

---

# 目录

1. [先记住最核心的一句话](#先记住最核心的一句话)
2. [一张图先把整体关系看懂](#一张图先把整体关系看懂)
3. [为什么 HTML 文件在服务器上，外部却不一定能访问](#为什么-html-文件在服务器上外部却不一定能访问)
4. [什么是 Web 服务](#什么是-web-服务)
5. [端口到底是什么](#端口到底是什么)
6. [`python3 -m http.server` 到底是什么](#python3--m-httpserver-到底是什么)
7. [这条命令逐个拆开理解](#这条命令逐个拆开理解)
8. [`http.server` 默认发布哪个文件](#httpserver-默认发布哪个文件)
9. [浏览器默认 80，为什么 `http.server` 默认 8000](#浏览器默认-80为什么-httpserver-默认-8000)
10. [`127.0.0.1`、服务器内网 IP、`0.0.0.0` 分别是什么](#127001服务器内网-ip0000-分别是什么)
11. [服务启动后会一直开着吗](#服务启动后会一直开着吗)
12. [怎么看服务还在不在](#怎么看服务还在不在)
13. [怎么关闭 `http.server`](#怎么关闭-httpserver)
14. [nginx 是什么](#nginx-是什么)
15. [nginx 和 `http.server` 的区别](#nginx-和-httpserver-的区别)
16. [nginx 的安装、启动与验证](#nginx-的安装启动与验证)
17. [什么是服务，什么是进程](#什么是服务什么是进程)
18. [一个进程可以叫 worker 吗](#一个进程可以叫-worker-吗)
19. [`systemctl` 是什么](#systemctl-是什么)
20. [`systemctl status nginx` 怎么看](#systemctl-status-nginx-怎么看)
21. [`ps -ef | grep http.server` 是什么意思](#ps--ef--grep-httpserver-是什么意思)
22. [`continue` 和 `proceed` 的区别](#continue-和-proceed-的区别)
23. [页面打不开时，更合理的排查顺序](#页面打不开时更合理的排查顺序)
24. [最常见的误区](#最常见的误区)
25. [一组最好记的结论](#一组最好记的结论)
26. [命令速查表](#命令速查表)

---

## 先记住最核心的一句话

**把一个 HTML 文件放到服务器上，只是把文件存到了磁盘里；这不等于别人就能通过浏览器访问它。**

想让外部浏览器访问，至少要满足这几件事：

1. 文件确实在服务器上。
2. 有一个 Web 服务程序在运行。
3. 这个服务正在监听某个端口。
4. 外部网络能访问到这个端口。

也就是说：

- **放文件**，只是把内容准备好。
- **启动服务**，才是把内容“发布出去”。

---

## 一张图先把整体关系看懂

```text
浏览器
   ↓
发起 HTTP 请求
   ↓
访问服务器的某个端口（比如 80 / 8000）
   ↓
Web 服务程序接收请求（比如 http.server / nginx）
   ↓
服务对应的进程去磁盘找文件
   ↓
把 HTML 返回给浏览器
   ↓
浏览器渲染成网页
```

你可以把它理解成：

- **HTML 文件**：仓库里的货
- **Web 服务**：窗口工作人员
- **端口**：窗口号
- **浏览器**：来取货的人

只有“货在仓库里”还不够，**还得有人在窗口值班，把货递出来。**

---

## 为什么 HTML 文件在服务器上，外部却不一定能访问

很多人会下意识觉得：

> 我都把 `test.html` 传到服务器了，浏览器为什么还打不开？

原因很简单：**操作系统不会自动把一个普通文件变成网站。**

比如服务器上有这个文件：

```bash
/root/test.html
```

它本质上只是磁盘上的一个普通文件，和下面这些没有本质区别：

```bash
/root/a.txt
/root/demo.pdf
/root/pic.png
```

浏览器并不知道：

- 这个文件是不是网页
- 该从哪个端口访问它
- 该由哪个程序把它返回出来

所以中间还差一个关键角色：

> **必须有一个程序站出来，对外说：谁来访问我这个端口，我就把对应文件返回给他。**

这个程序就是 Web 服务器程序。常见的有：

- `python3 -m http.server`
- `nginx`
- `apache`

---

## 什么是 Web 服务

Web 服务本质上就是一个“接待浏览器请求、并把内容返回出去”的程序。

它通常会做下面几件事：

1. 监听某个端口，比如 `80`、`8000`。
2. 接收浏览器发来的 HTTP 请求。
3. 根据访问路径去磁盘上找文件。
4. 把文件内容返回给浏览器。
5. 浏览器再把内容渲染成网页。

所以可以把它理解成：

> **Web 服务 = 一个负责接电话、找文件、回消息的程序。**

---

## 端口到底是什么

端口可以先简单理解成：

> **服务器上的一个“窗口号”或“门牌号”。**

同一台服务器上可以同时运行很多服务：

- 一个服务监听 `80`
- 一个服务监听 `22`
- 一个服务监听 `3306`

不同程序通过不同端口区分彼此。

常见例子：

- `80`：HTTP 网站
- `443`：HTTPS 网站
- `22`：SSH 远程登录
- `8000`：很多开发测试服务常用端口

所以：

- 你访问 `http://服务器IP/`，浏览器默认找的是 `80`
- 你访问 `http://服务器IP:8000/`，浏览器找的是 `8000`

---

## `python3 -m http.server` 到底是什么

最常见的临时启动方式就是：

```bash
python3 -m http.server
```

它的作用是：

> **用 Python 自带的简易 HTTP 服务，把“当前目录”临时对外开放出来。**

这里非常容易误解的一点是：

**它不是“自动发布某一个 HTML 文件”，而是“把当前目录当成一个小网站目录开放出来”。**

也就是说，它默认发布的是：

> **当前目录里的内容**

而不是某一个指定文件。

---

## 这条命令逐个拆开理解

完整例子：

```bash
python3 -m http.server 80
```

逐个看：

### 1. `python3`

表示调用 Python 3 解释器。

### 2. `-m`

`-m` 表示：

> **module**

意思是：把后面的内容当成 Python 模块来运行。

所以：

```bash
python3 -m 某模块
```

意思就是：

> 用 Python 运行某个模块。

### 3. `http.server`

这是 Python 自带的模块名。

- `http`：HyperText Transfer Protocol，超文本传输协议
- `server`：服务器

合起来就是：

> 一个简易 HTTP 服务器模块。

### 4. `80`

这是端口号，表示让这个服务监听 `80` 端口。

### 5. `--bind 0.0.0.0`

例如：

```bash
python3 -m http.server 80 --bind 0.0.0.0
```

含义：

- `--bind`：绑定到指定地址
- `0.0.0.0`：监听所有网卡地址

这通常更适合“让外部机器也能访问”的场景。

---

## `http.server` 默认发布哪个文件

这是一个必须彻底搞清楚的知识点。

### 核心结论

**`python3 -m http.server` 默认发布的是“当前目录”，不是某一个单独文件。**

例如：

```bash
cd /root/site
python3 -m http.server
```

它真正做的事更接近于：

> 把 `/root/site` 这个目录开放出来，让浏览器可以访问这个目录里的文件。

### 情况一：目录里有 `index.html`

假设目录内容是：

```bash
/root/site/index.html
/root/site/about.html
/root/site/logo.png
```

此时访问：

```text
http://你的IP:8000/
```

通常会默认打开：

```bash
/root/site/index.html
```

也就是说：

> **`index.html` 通常会被当作首页。**

你也可以显式访问：

```text
http://你的IP:8000/about.html
http://你的IP:8000/logo.png
```

### 情况二：目录里没有 `index.html`

假设目录里只有：

```bash
/root/site/1.html
/root/site/2.html
/root/site/report.html
```

此时访问：

```text
http://你的IP:8000/
```

通常不会自动猜“哪个文件是首页”，而是显示一个目录列表。

这说明：

> **没有 `index.html` 时，默认一般是列出目录，而不是替你选一个 HTML 打开。**

### 情况三：想访问某个具体文件

假设目录里有：

```bash
/root/site/test.html
```

那访问地址就是：

```text
http://你的IP:8000/test.html
```

如果你监听的是 `80` 端口：

```bash
python3 -m http.server 80
```

则地址变成：

```text
http://你的IP/test.html
```

### 情况四：我就想让某个页面成为首页

最简单的方法就是把它命名成：

```bash
index.html
```

这样访问：

```text
http://你的IP:8000/
```

通常就会直接打开它。

---

## 浏览器默认 80，为什么 `http.server` 默认 8000

这是最容易混淆的问题之一。

### 先记结论

- **浏览器访问 `http://xxx` 时，没写端口，默认就是 `80`**
- **`python3 -m http.server` 不写端口时，默认监听的是 `8000`**

这两个默认值：

> **不是同一套规则。**

### 1. 浏览器默认 80，是 HTTP 协议的习惯规则

当你访问：

```text
http://example.com
```

浏览器会默认理解成：

```text
http://example.com:80
```

而如果是：

```text
https://example.com
```

默认会理解成：

```text
https://example.com:443
```

所以可以记成：

- `http://` 默认 `80`
- `https://` 默认 `443`

### 2. `http.server` 默认 8000，是 Python 工具自己的设计选择

`http.server` 的典型用途是：

- 本地预览
- 临时测试
- 开发调试
- 临时共享文件

它默认选 `8000` 而不是 `80`，主要因为：

#### 原因 A：少权限麻烦

很多 Linux 系统里，较小端口尤其是 `1024` 以下端口更敏感，`80` 经常需要更高权限或更规范的服务方式。

#### 原因 B：减少冲突

`80` 很容易已经被这些服务占用：

- `nginx`
- `apache`
- 其他网站服务

`8000` 更适合临时测试，不容易跟正式服务冲突。

#### 原因 C：它本来就是个轻量测试工具

`http.server` 更像“临时摆摊”，不是“正式营业的网站前台”。

### 3. 最直观的例子

如果你执行：

```bash
python3 -m http.server
```

它几乎等价于：

```bash
python3 -m http.server 8000
```

此时应该访问：

```text
http://你的IP:8000/
```

而不是：

```text
http://你的IP/
```

因为后者默认会去找 `80` 端口。

如果你真的想直接访问：

```text
http://你的IP/
```

那你就得显式让服务监听 `80`：

```bash
python3 -m http.server 80 --bind 0.0.0.0
```

---

## `127.0.0.1`、服务器内网 IP、`0.0.0.0` 分别是什么

这部分决定了“谁能访问到这个服务”。

### 1. `127.0.0.1`

表示：

> **本机回环地址，只允许服务器自己访问自己。**

如果服务只绑定在 `127.0.0.1`，通常意味着：

- 服务器本机能访问
- 外部机器访问不到

### 2. 服务器内网 IP

例如：

```text
10.x.x.x
172.x.x.x
192.168.x.x
```

通常表示服务器在局域网或云内网里的地址。内网中的其他机器可能能访问，但公网不一定能直接访问。

### 3. `0.0.0.0`

表示：

> **监听所有网络接口。**

例如：

```bash
python3 -m http.server 80 --bind 0.0.0.0
```

意思是这个服务会对所有网卡地址监听，通常更适合“希望外部访问”的场景。

### 一句话区分

- `127.0.0.1`：只给自己访问
- 内网 IP：给局域网/云内网访问
- `0.0.0.0`：监听所有地址

---

## 服务启动后会一直开着吗

这取决于你是怎么启动它的。

### 一、前台启动

如果你直接在终端里运行：

```bash
python3 -m http.server
```

通常表示：

- 服务在当前终端前台运行
- 当前终端会被它占住
- 按 `Ctrl + C`，服务就停
- 直接关掉这个终端，服务通常也会停

你一般会看到类似输出：

```text
Serving HTTP on 0.0.0.0 port 8000 ...
```

### 二、后台启动

例如：

```bash
nohup python3 -m http.server 8000 >/tmp/http.log 2>&1 &
```

这表示它在后台运行。

特点：

- 终端关了，它也可能继续跑
- 不会一直占住当前窗口
- 以后需要单独查进程再关闭

---

## 怎么看服务还在不在

### 方法 1：看端口有没有监听

如果是 `8000`：

```bash
ss -tlnp | grep 8000
```

如果是 `80`：

```bash
ss -tlnp | grep 80
```

看到 `LISTEN`，通常说明确实有程序在监听这个端口。

### 方法 2：看进程还在不在

```bash
ps -ef | grep http.server
```

如果还能看到：

```text
python3 -m http.server
```

说明这个进程还在。

### 方法 3：本机实际访问测试

```bash
curl -I http://127.0.0.1:8000
curl -I http://127.0.0.1
```

如果能收到 HTTP 响应，说明服务大概率是正常的。

---

## 怎么关闭 `http.server`

### 方法 A：前台运行时直接关

如果就是当前终端前台启动的，直接按：

```text
Ctrl + C
```

### 方法 B：查 PID 再关

先找进程：

```bash
ps -ef | grep http.server
```

例如看到：

```text
root   12345  ... python3 -m http.server 8000
```

这里的 `12345` 就是 PID。然后：

```bash
kill 12345
```

如果还不退出，再用：

```bash
kill -9 12345
```

### 方法 C：按命令名直接关

```bash
pkill -f "python3 -m http.server"
```

这个很方便，但要注意：

> 如果你同时开了多个这样的服务，它可能会一起杀掉。

---

## nginx 是什么

### 一句话理解

**nginx 是一个更正式、更专业、更常用的 Web 服务器。**

如果说：

- `python3 -m http.server` 像临时摆摊

那么：

- `nginx` 更像正式门店、长期营业的前台

### nginx 怎么读

一般读作：

> **engine-x**

它不是普通英文单词，更像一个产品名。

### nginx 最核心是做什么的

你可以把 nginx 理解成：

> **服务器门口的总接待台。**

浏览器的请求先到 nginx 这里，nginx 再决定：

- 直接返回 HTML 文件
- 返回 CSS、JS、图片等静态资源
- 把请求转发给后端程序
- 处理 HTTPS
- 做访问控制
- 做负载均衡

### 在“放 HTML 页面”的场景里，nginx 做了什么

假设服务器上有：

```bash
/usr/share/nginx/html/index.html
```

外部访问：

```text
http://服务器IP/
```

nginx 会：

1. 接收这个请求
2. 去指定目录找文件
3. 找到后把内容返回给浏览器
4. 浏览器再把它渲染成网页

所以在静态页面场景里，nginx 和 `http.server` 的核心动作很像：

> 接请求 → 找文件 → 返回文件

只是 nginx 更正式、功能更多、长期运行能力更强。

---

## nginx 和 `http.server` 的区别

| 对比项 | `python3 -m http.server` | nginx |
|---|---|---|
| 典型用途 | 临时测试、快速预览、临时共享 | 正式网站、长期运行 |
| 配置复杂度 | 很低 | 较高 |
| 功能 | 基础 | 很完整 |
| 是否适合生产环境 | 一般不适合 | 更适合 |
| HTTPS | 基本不靠它 | 常见能力 |
| 反向代理 | 基本不用它 | 核心能力之一 |
| 负载均衡 | 不擅长 | 常见能力 |

一句话总结：

- **`http.server`：测试小工具**
- **nginx：正式 Web 服务器**

---

## nginx 的安装、启动与验证

### 1. 安装 nginx

#### CentOS / Rocky / 阿里云 Linux 一类系统

```bash
dnf install -y nginx
```

有些环境也可能是：

```bash
yum install -y nginx
```

#### Ubuntu / Debian

```bash
apt update
apt install -y nginx
```

### 2. 启动 nginx

```bash
systemctl start nginx
```

### 3. 查看 nginx 状态

```bash
systemctl status nginx
```

### 4. 设置开机自启

```bash
systemctl enable nginx
```

### 5. 默认网页目录

很多系统里默认目录是：

```bash
/usr/share/nginx/html/
```

所以最常见的做法是：

- 把 `index.html` 放进去
- 启动 nginx
- 浏览器访问 `http://服务器IP/`

### 6. 最核心的访问链路

```text
浏览器 → 80端口 → nginx → HTML文件
```

---

## 什么是服务，什么是进程

这是很多初学者最容易混掉的一组概念。

### 服务（service）

服务更像是：

> **一个功能或一套被管理的运行单元**

例如：

- nginx 服务
- mysql 服务
- sshd 服务

### 进程（process）

进程更像是：

> **操作系统里真正跑起来的程序实例**

例如：

- 一个 `python3 -m http.server` 进程
- 一个 nginx master 进程
- 多个 nginx worker 进程

### 两者关系

可以先简单理解成：

```text
服务（抽象概念）
   ↓
真正运行时会表现为一个或多个进程（操作系统里的实体）
```

所以：

- **服务**是你从“功能管理”角度看的名字
- **进程**是系统里真实跑着的东西

---

## 一个进程可以叫 worker 吗

你前面问过一个关键问题：

> 1 个进程可以叫做 worker 吗？

答案是：

> **可以，但要看语境。**

### 1. `worker` 不是“进程”的通用翻译

- `process`：进程
- `worker`：工作者、执行任务的工作单元

所以严格说，`worker` 不是所有进程的统称。

### 2. 但在很多系统里，worker 常常就是一个工作进程

例如在 nginx 里，结构常写成：

```text
master process
    ↓
worker processes
```

这里的 `worker` 指的就是：

> **负责真正处理请求的工作进程**

所以在 nginx 这个语境下：

- `worker = worker process`
- 本质上它就是进程

### 3. 最准确的说法

可以这么记：

> **worker 是一种角色名；在很多程序里，这个角色恰好由一个进程来承担。**

因此：

- 在 nginx 里，说“worker 进程”完全正确
- 但不是所有进程都叫 worker

---

## `systemctl` 是什么

### 一句话理解

`systemctl` 是 Linux 里用于管理服务的常用命令。

### 名字怎么理解

很多人会想：

> `systemctl` 是不是 `system control`？

从记忆角度这么理解不算离谱，但更准确一点，它是：

> **systemd control 的命令工具**

也就是：

- `systemd`：系统和服务管理器
- `systemctl`：控制 `systemd` 的命令行工具

### 它主要用来干什么

比如：

- 启动服务
- 停止服务
- 重启服务
- 查看服务状态
- 设置开机自启

常见例子：

```bash
systemctl start nginx
systemctl stop nginx
systemctl restart nginx
systemctl reload nginx
systemctl status nginx
systemctl enable nginx
```

---

## `systemctl status nginx` 怎么看

执行：

```bash
systemctl status nginx
```

你通常会看到几块关键信息。

### 1. Loaded

表示：

- 这个服务的配置文件有没有被 systemd 识别
- 是否支持开机启动

### 2. Active

例如：

```text
Active: active (running)
```

表示：

> **nginx 这个服务当前正在运行。**

如果看到：

```text
inactive (dead)
```

就表示没在运行。

### 3. Main PID

表示这个服务的主进程 PID。

### 4. 日志片段

下面通常还会附带最近几行日志，帮助你快速判断：

- 是正常启动了
- 还是启动失败了
- 还是端口冲突了

### 一句话总结

`systemctl status nginx` 的核心，就是看这句：

```text
Active: active (running)
```

看到它，通常说明 nginx 服务已经正常起来了。

---

## `ps -ef | grep http.server` 是什么意思

这是查看进程的经典命令。

```bash
ps -ef | grep http.server
```

可以拆成两部分理解。

### 第一部分：`ps -ef`

- `ps`：查看进程
- `-e`：显示所有进程
- `-f`：显示完整信息

所以它的意思是：

> 列出系统里所有进程的详细信息。

### 第二部分：`grep http.server`

`grep` 是过滤关键词。

所以整条命令就是：

> 把所有进程列出来，再筛选出包含 `http.server` 的那些行。

### 你通常会看到什么

可能看到：

```text
root   12345  ... python3 -m http.server 8000
root   12388  ... grep http.server
```

第一行是真正的服务进程。

第二行是 `grep` 自己，因为它自己的命令里也包含 `http.server` 这个词。

### 更优雅的写法

```bash
ps -ef | grep [h]ttp.server
```

这样一般就不会把 `grep` 自己匹配出来。

### 这条命令的用途

最核心用途就是：

> **判断某个进程还在不在。**

---

## `continue` 和 `proceed` 的区别

你前面还问过：除了 `continue`，是不是还有一个 `pro...` 开头的词。

是的，经常在命令行和安装流程里看到：

```text
Do you want to proceed?
```

意思就是：

> 你要继续执行吗？

### 区别可以先这么记

| 单词 | 常见语气 | 常见场景 |
|---|---|---|
| continue | 更日常 | 一般表达继续 |
| proceed | 更正式 | CLI、安装器、提示框、文档 |

### 直观理解

- `continue`：继续
- `proceed`：继续往下执行、继续下一步操作

所以在系统提示里：

```text
Do you want to proceed?
```

往往比：

```text
Do you want to continue?
```

更像“正式确认是否继续执行接下来的动作”。

---

## 页面打不开时，更合理的排查顺序

很多人一遇到“网页打不开”，马上就怀疑：

- 公网问题
- 安全组问题
- 防火墙问题
- NAT 问题

这些当然有可能，但更稳妥的顺序应该是下面这样。

### 第 1 步：先确认文件在不在

例如：

```bash
ls -l /root/test.html
```

如果文件压根不存在，后面都不用查了。

### 第 2 步：确认服务有没有起来

例如：

```bash
ss -tlnp | grep 80
ss -tlnp | grep 8000
```

看有没有程序在监听你要访问的端口。

### 第 3 步：先测试本机访问

这一步非常关键：

```bash
curl -I http://127.0.0.1
curl -I http://127.0.0.1:8000
```

如果这里都不通，通常说明：

> **本机服务就没起来。**

这时先别急着怪公网、防火墙、安全组。

### 第 4 步：确认监听地址对不对

检查服务是不是只绑定在 `127.0.0.1`，还是已经监听 `0.0.0.0`。

如果只绑定本机，那外部很可能访问不到。

### 第 5 步：本机通了，再查外部网络

本机确认没问题以后，再继续排查：

- 云安全组
- 服务器防火墙
- 公网映射
- NAT / 端口转发
- 外部机器到服务器的网络链路

### 为什么这个顺序更合理

因为很多“外面打不开”的根本原因，其实不是公网，而是：

- 服务没启动
- 监听错了端口
- 只监听在 `127.0.0.1`
- 访问路径写错了

先把本机链路打通，再查外网，效率最高。

---

## 最常见的误区

### 误区 1：文件在服务器上，就等于网站已经上线

不对。

文件在服务器上，只代表“内容存在”，不代表“已经通过 Web 服务对外发布”。

### 误区 2：`python3 -m http.server` 默认会发布某一个 HTML

不对。

它默认发布的是**当前目录**。

- 有 `index.html`，通常把它当首页
- 没有 `index.html`，通常显示目录列表

### 误区 3：浏览器默认 80，所以 `http.server` 也应该默认 80

不对。

- 浏览器默认 `80`，是 HTTP 协议的约定
- `http.server` 默认 `8000`，是 Python 工具自己的设计选择

这两个默认值不是一套逻辑。

### 误区 4：`127.0.0.1` 不通，也可能只是公网有问题

通常不是。

如果：

```bash
curl -I http://127.0.0.1:8000
```

直接报 `Connection refused`，更常见的含义是：

> 本机对应端口根本没有程序在监听。

也就是服务本身没起来。

### 误区 5：没看到公网 IP，就一定不能公网访问

不一定。

在云服务器场景下，系统里看到的往往是内网 IP，但云厂商可能给它额外做了公网映射。

所以：

> **服务器网卡里没直接看到公网 IP，不等于公网一定访问不了。**

### 误区 6：服务器自己访问自己的公网 IP 失败，就等于别人也访问不了

也不一定。

有些云环境中：

- 外部机器访问公网 IP 是通的
- 但服务器自己回环访问自己的公网 IP 不一定成功

所以公网测试更靠谱的方法通常是：

- 本地电脑访问
- 手机流量访问
- 另一台机器访问

### 误区 7：`Connection refused` 和 timeout 差不多

不完全一样。

- **`Connection refused`**：更像目标端口没人监听，或系统明确拒绝连接
- **timeout**：更像网络链路、防火墙、路由、中间设备有问题

所以这两个报错传达的含义不同。

---

## 一组最好记的结论

### 结论 1

**放文件不等于能访问。**

还必须有 Web 服务把它发布出去。

### 结论 2

**`python3 -m http.server` 默认发布当前目录，不是默认发布某一个文件。**

### 结论 3

**目录里有 `index.html`，通常会把它当首页；没有时，通常显示目录列表。**

### 结论 4

**浏览器默认端口和服务默认端口不是一回事。**

- `http://xxx` 默认 `80`
- `https://xxx` 默认 `443`
- `python3 -m http.server` 默认 `8000`

### 结论 5

**本机不通，先别怪公网。**

如果 `curl 127.0.0.1` 都不通，先检查服务有没有起来。

### 结论 6

**`http.server` 适合测试，nginx 适合正式网站。**

### 结论 7

**服务和进程不是一回事。**

- 服务是被管理的功能单元
- 进程是系统里真正跑起来的实体

### 结论 8

**在 nginx 语境里，worker 通常就是工作进程。**

---

## 命令速查表

### 1. 在当前目录启动临时服务（默认 8000）

```bash
python3 -m http.server
```

### 2. 显式监听 8000

```bash
python3 -m http.server 8000
```

### 3. 显式监听 80，并监听所有地址

```bash
python3 -m http.server 80 --bind 0.0.0.0
```

### 4. 查看端口是否被监听

```bash
ss -tlnp | grep 8000
ss -tlnp | grep 80
```

### 5. 查看 `http.server` 进程

```bash
ps -ef | grep http.server
```

### 6. 更优雅地查进程

```bash
ps -ef | grep [h]ttp.server
```

### 7. 本机访问测试

```bash
curl -I http://127.0.0.1:8000
curl -I http://127.0.0.1
```

### 8. 关闭前台服务

```text
Ctrl + C
```

### 9. 查 PID 后关闭

```bash
ps -ef | grep http.server
kill PID
```

### 10. 按命令名直接关闭

```bash
pkill -f "python3 -m http.server"
```

### 11. 安装 nginx

```bash
dnf install -y nginx
```

或：

```bash
apt install -y nginx
```

### 12. 启动 nginx

```bash
systemctl start nginx
```

### 13. 查看 nginx 状态

```bash
systemctl status nginx
```

### 14. 重启 nginx

```bash
systemctl restart nginx
```

### 15. 设置 nginx 开机启动

```bash
systemctl enable nginx
```

---

## 最后一段总结

一个 HTML 文件想被浏览器访问，本质上至少要完成两件事：

1. 文件已经放到服务器上。
2. 有服务在某个端口上把它发布出去。

真正要彻底分清楚的，是下面这几件事：

- **浏览器默认访问哪个端口**
- **服务实际监听的是哪个端口**
- **服务默认发布的是单个文件，还是整个目录**
- **服务背后对应的到底是哪个进程**
- **你是在用临时测试工具，还是在用正式 Web 服务器**

把这些关系理顺之后，绝大多数“为什么页面打不开”“这个命令到底在干嘛”“nginx 和进程是什么关系”的问题，就不会再混了。


很好，这一步我帮你做成**可直接替换的完整 MD 版本补充**，把你刚刚学到的 nginx 核心知识（配置、index、root、反向代理等）**系统性补进原笔记里**，而且保证逻辑清晰、不重复、不漏关键点。

下面是你可以**直接追加到原 MD 文件里的新章节**👇（建议放在 nginx 相关章节后面，比如第 16 节后）

---

# 🔥 新增：nginx 配置、静态托管与反向代理（核心补全）

## nginx 配置文件在哪里

### 核心结论

👉 nginx 的主配置文件是：

```bash
/etc/nginx/nginx.conf
```

但**真正日常修改的通常不是它**，而是：

```bash
/etc/nginx/conf.d/*.conf
```

---

## nginx 配置结构（非常重要）

典型结构：

```text
/etc/nginx/
├── nginx.conf        # 主配置（入口）
├── conf.d/           # 推荐：放网站配置
│   └── xxx.conf
```

在 `nginx.conf` 里通常有一句：

```nginx
include /etc/nginx/conf.d/*.conf;
```

👉 意思是：

> 自动加载 `conf.d` 目录下所有配置文件

---

## 推荐实践（必须记住）

* ❌ 不要把所有配置写进 nginx.conf
* ✅ 每个网站一个 `.conf` 文件

例如：

```bash
vim /etc/nginx/conf.d/ocr.conf
```

---

# nginx 最核心的一段配置

```nginx
location / {
    root /data/www/ocr;
    index index.html;
}
```

---

## 每一行到底在干什么（必须吃透）

```nginx
location / {
```

👉 匹配所有访问路径（几乎所有请求）

---

```nginx
root /data/www/ocr;
```

👉 指定网站文件目录

---

```nginx
index index.html;
```

👉 指定“访问目录时默认返回的文件”

---

# 🔥 index 到底是什么（重点）

## 一句话理解

👉 **index = 访问目录时的默认文件**

---

## 举例

访问：

```text
http://你的IP/
```

nginx 会去找：

```bash
/data/www/ocr/index.html
```

---

## 可以改名吗？

👉 可以

例如：

```nginx
index home.html;
```

---

## 可以写多个（推荐）

```nginx
index index.html index.htm default.html;
```

👉 按顺序找：

1. index.html
2. index.htm
3. default.html

---

## 一个关键点（很多人忽略）

👉 `index` **只在访问目录时生效**

---

### 举例

访问：

```text
http://你的IP/about.html
```

👉 nginx 不会用 index
👉 直接找：

```bash
/data/www/ocr/about.html
```

---

# 🔥 root 的真正逻辑（容易误解）

## 关键公式

```text
实际文件路径 = root + 请求路径
```

---

## 举例

配置：

```nginx
root /data/www/ocr;
```

---

访问：

```text
http://IP/test.html
```

nginx 实际找：

```bash
/data/www/ocr/test.html
```

---

访问：

```text
http://IP/img/logo.png
```

找：

```bash
/data/www/ocr/img/logo.png
```

---

# 🔥 nginx 两种核心模式（必须区分）

## ✅ 1. 静态文件托管

```text
浏览器 → nginx → 磁盘文件 → 浏览器
```

配置：

```nginx
location / {
    root /data/www/ocr;
    index index.html;
}
```

👉 nginx 自己返回文件

---

## ✅ 2. 反向代理

```text
浏览器 → nginx → 后端程序 → nginx → 浏览器
```

配置：

```nginx
location / {
    proxy_pass http://127.0.0.1:3000;
}
```

👉 nginx 转发请求

---

# 🔥 一句话区分（非常重要）

👉 **静态托管 = nginx 自己读文件**
👉 **反向代理 = nginx 把请求转发给别人**

---

# 🔥 两种模式可以同时存在（生产常见）

```nginx
server {
    listen 80;

    # 静态页面
    location / {
        root /data/www/ocr;
        index index.html;
    }

    # 接口请求
    location /api/ {
        proxy_pass http://127.0.0.1:3000;
    }
}
```

---

## 访问效果

| 请求            | 行为      |
| ------------- | ------- |
| `/`           | 返回 HTML |
| `/about.html` | 返回文件    |
| `/api/user`   | 转发到后端   |

---

# 🔥 nginx 配置修改流程（必须记住）

## 1️⃣ 修改配置

```bash
vim /etc/nginx/conf.d/xxx.conf
```

---

## 2️⃣ 检查语法

```bash
nginx -t
```

---

## 3️⃣ 重新加载

```bash
systemctl reload nginx
```

---

## 4️⃣ 如果有问题再重启

```bash
systemctl restart nginx
```

---

# 🔥 nginx 生效的前提（很多人忽略）

即使配置写对，还必须满足：

---

## 1. nginx 在运行

```bash
systemctl status nginx
```

---

## 2. 端口开放（80）

* 云安全组
* 防火墙

---

## 3. 文件真实存在

```bash
/data/www/ocr/index.html
```

---

## 4. 路径写对

`root` 指向的目录必须正确

---

# 🔥 最关键总结（这一段一定要记）

👉 nginx 本质是一个“入口层程序”，它可以：

* 返回静态文件
* 转发请求
* 管理访问入口

---

## 最核心理解

```text
浏览器
   ↓
nginx（入口）
   ↓
① 返回文件（静态）
② 转发请求（代理）
```

---

## 一句话终极总结

👉 **nginx = 网站的“门口接待员”**

* 要文件 → 给文件
* 要接口 → 转给后端

---

# ✅ 建议你现在做的事

把你那个 HTML：

```bash
/root/OCR竞品调研-xxx.html
```

执行：

```bash
mkdir -p /data/www/ocr
cp /root/xxx.html /data/www/ocr/index.html
```

然后用这段配置：

```nginx
location / {
    root /data/www/ocr;
    index index.html;
}
```

---

# 📌 最后说明

我已经把这部分内容整理成：

👉 **可以直接补进你原 MD 文件的结构化章节**

并且已经覆盖：

* nginx 配置文件位置
* root / index 原理
* 静态 vs 反向代理
* 配置修改流程
* 常见误区

---

如果你下一步想继续升级这份笔记，我可以帮你再补一层：

👉 **“nginx + 域名 + HTTPS + 多站点”完整实战章节**

这一步就已经接近真实生产环境了。

