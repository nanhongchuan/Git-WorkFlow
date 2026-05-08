# 【01】笔记07-GitHub构建软件包&发布 Release 全流程
![alt text](32f7455b7779ebf572ebe5a21302e0da.png)

## 1️⃣ 先了解软件包

**软件包**就是用户可以直接安装或运行的文件：

| 平台      | 常见文件类型               |
| ------- | -------------------- |
| Windows | `.exe` / `.msi`      |
| macOS   | `.dmg` / `.pkg`      |
| Linux   | `.deb` / `.AppImage` |
| 跨平台     | `.zip` / `.tar.gz`   |

> 打包的目的：让别人不用看源码就能使用你的程序。

---

## 2️⃣ 写打包脚本（语言相关）

不同语言打包方法不同，但原理一样：**源代码 → 可执行文件 → 安装包/压缩包**

| 语言                 | 打包方式                        | 可执行文件           | 发布文件               |
| ------------------ | --------------------------- | --------------- | ------------------ |
| Python             | `PyInstaller` / `cx_Freeze` | `.exe` / `.app` | `.exe` / `.zip`    |
| Node.js / Electron | `pkg` / `electron-builder`  | `.exe` / `.dmg` | `.exe` / `.zip`    |
| Java               | `jar` → `Launch4j`          | `.exe` 或 `.jar` | `.exe` / `.zip`    |
| Go                 | `go build`                  | 可执行文件           | `.exe` / `.tar.gz` |
| C/C++              | 编译器                         | 可执行文件           | `.exe` / 安装包       |

> ⚠️ 解释型语言（Python、JavaScript、Java）打包后**源码可能被反编译**，编译型语言（C/C++、Go、Rust）安全性更高。

---

## 3️⃣ 使用 GitHub Actions 自动化（可选）

* **作用**：每次你推送代码，Actions 自动帮你打包、生成安装包/压缩包
* **流程**：

```
代码推送 → Actions 执行打包脚本 → 生成安装包/压缩包 → 上传 Release
```

* **示例（Python Windows exe）**：

```yaml id="z7k4vi"
name: Build Installer

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - run: pip install pyinstaller
      - run: pyinstaller --onefile main.py
      - uses: actions/upload-artifact@v3
        with:
          name: my-program
          path: dist/
```

> 对其他语言，只需替换打包命令，流程一样。

---

## 4️⃣ 上传 Release（发布软件包）

1. 进入仓库 → 点击 **“Releases”** → **“Draft a new release”**
2. 填写版本号，例如 `v1.0.0`
3. 填写更新说明
4. 上传你的安装包或压缩包
5. 发布后，用户可以直接下载并使用

> ⚡ Tips：Actions 可以自动上传 Release（`actions/create-release` + `actions/upload-release-asset`）

---

## 5️⃣ 考虑源码安全性

* **解释型语言打包**：源码容易被提取和反编译
* **编译型语言打包**：源码不容易被看到，但仍可通过反汇编分析
* **保护方法**：

  1. 混淆代码（Python: `pyarmor`，JS: `javascript-obfuscator`，Java: `ProGuard`）
  2. 关键逻辑放编译型语言或服务端
  3. 仅在客户端放必要功能，核心算法走服务端

---

## 6️⃣ 小白三步法总结

1. **写打包脚本** → 告诉电脑怎么生成安装包/压缩包
2. **配置 GitHub Actions** → 自动化执行打包（可选，本地也可）
3. **上传 Release** → 发布文件给用户下载

---

💡 总结：

* 语言不同，打包工具不同，但流程通用
* Actions 可选，但能省下重复手动操作
* 发布 Release 就是把打包好的文件发给用户
* 源码安全性要看语言和打包方式，可用混淆或服务端策略保护

---
