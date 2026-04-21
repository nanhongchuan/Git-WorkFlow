# `curl` 常见参数可以按“你最常用的场景”来记。

先给你一个最好用的速查版：

### 1. 发请求相关

`-X`
指定请求方法。

```bash
curl -X GET https://example.com
curl -X POST https://example.com
```

`-d`
发送请求体，常用于 POST。

```bash
curl -X POST -d "name=tom&age=18" https://example.com
```

`-H`
添加请求头。

```bash
curl -H "Content-Type: application/json" https://example.com
curl -H "Authorization: Bearer xxx" https://example.com
```

`-F`
上传表单或文件。

```bash
curl -F "file=@test.jpg" https://example.com/upload
```

---

### 2. 查看返回结果

`-i`
显示响应头 + 响应体。

```bash
curl -i https://example.com
```

`-I`
只看响应头，不看响应体。

```bash
curl -I https://example.com
```

`-v`
显示详细过程，排查问题特别常用。

```bash
curl -v https://example.com
```

`-s`
静默模式，不显示进度条。

```bash
curl -s https://example.com
```

`-S`
通常和 `-s` 一起用。静默，但出错时仍显示错误。

```bash
curl -sS https://example.com
```

---

### 3. 保存内容

`-o`
保存到指定文件名。

```bash
curl -o page.html https://example.com
```

`-O`
按远程文件原名保存。

```bash
curl -O https://example.com/file.zip
```

---

### 4. 跟重定向

`-L`
自动跟随 301/302 跳转。

```bash
curl -L http://example.com
```

很多网站不用 `-L`，你拿到的可能只是跳转信息。

---

### 5. 证书 / HTTPS

`-k`
忽略 HTTPS 证书校验。

```bash
curl -k https://example.com
```

这个常用于测试环境、自签名证书环境。

---

### 6. 用户认证

`-u`
携带用户名密码。

```bash
curl -u user:password https://example.com
```

---

### 7. 超时控制

`--connect-timeout`
连接超时。

```bash
curl --connect-timeout 5 https://example.com
```

`-m` 或 `--max-time`
整个请求最大耗时。

```bash
curl -m 10 https://example.com
```

---

### 8. 指定代理

`-x`
走代理。

```bash
curl -x http://127.0.0.1:7890 https://example.com
```

---

### 9. 指定输出信息

`-w`
自定义输出，比如看状态码。

```bash
curl -o /dev/null -s -w "%{http_code}\n" https://example.com
```

很适合检查接口是否通。

---

### 10. 续传 / 断点下载

`-C -`
从上次中断处继续下载。

```bash
curl -C - -O https://example.com/bigfile.zip
```

---

## 你在服务器上最常用的几种组合

### 看网页/接口是否通

```bash
curl -I https://example.com
```

### 看详细排错信息

```bash
curl -v https://example.com
```

### 忽略证书测试 HTTPS

```bash
curl -k -I https://example.com
```

### POST 一个 JSON

```bash
curl -X POST https://example.com/api \
  -H "Content-Type: application/json" \
  -d '{"name":"tom","age":18}'
```

### 下载文件

```bash
curl -O https://example.com/file.tar.gz
```

### 查看状态码

```bash
curl -o /dev/null -s -w "%{http_code}\n" https://example.com
```

---

## 一句话理解几个容易混的参数

* `-i`：响应头 + 内容都看
* `-I`：只看响应头
* `-o`：自己命名保存
* `-O`：按原文件名保存
* `-s`：安静模式
* `-v`：详细调试模式
* `-L`：跟跳转
* `-k`：忽略证书报错

---

## 最后给你一个适合记笔记的版本

```bash
curl [参数] URL
```

常见参数：

```bash
-X    指定请求方法
-d    发送请求数据
-H    添加请求头
-F    上传文件/表单
-i    显示响应头+响应体
-I    只显示响应头
-v    显示详细调试信息
-s    静默模式
-sS   静默但保留错误信息
-o    保存为指定文件名
-O    按远程原名保存
-L    跟随重定向
-k    忽略 HTTPS 证书校验
-u    用户名密码认证
-x    指定代理
-m    最大请求时间
--connect-timeout  连接超时
-w    自定义输出结果
-C -  断点续传
```

要不要我顺手再给你整理一个 **“curl 新手最常见 20 个实战命令.md”** 版本？
