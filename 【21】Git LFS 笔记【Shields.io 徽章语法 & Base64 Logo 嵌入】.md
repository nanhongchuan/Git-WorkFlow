# Git LFS 笔记

## 1. 为什么需要 Git LFS

* **Git 的限制**

  * 单个文件 > 50 MB：push 时会触发警告
  * 单个文件 > 100 MB：push 会被拒绝
* **原因**

  * Git 每次 commit 都会保存文件快照（包括大文件）。
  * 如果对大文件反复修改，`.git` 文件夹会迅速膨胀（如 1GB 文件改 5 次，本地就占 5GB）。
  * 导致本地磁盘占用过大、Git 运行变慢。

## 2. 什么是 Git LFS

* Git Large File Storage（大文件存储系统）。
* 使用单独的文件存储服务器来保存大文件。
* 仓库里只存大文件的引用（pointer 文件）。
* 克隆/切换分支时，大文件会自动从 LFS 服务器下载。
* 好处：避免把所有历史版本的大文件存到本地，节省空间。

## 3. Git LFS 的使用流程

1. **进入项目目录**

   ```bash
   cd git-test
   ```

2. **安装 LFS 功能**

   ```bash
   git lfs install
   ```

3. **指定需要 LFS 管理的文件类型**

   * 例如指定所有 `.mp4` 文件：

     ```bash
     git lfs track "*.mp4"
     ```

4. **上传大文件（流程与普通文件相同）**

   ```bash
   git status
   git add .
   git commit -m "add large file"
   git push
   ```

5. **验证上传**

   * 到 GitHub 仓库网页查看，大文件已经成功上传。

## 4. 注意事项

* **存储空间限制**

  * GitHub 免费提供：1GB 存储 + 1GB 带宽
  * 存储空间包含历史版本，可能很快用完。

* **超出限制**

  * 需要付费购买扩展包。

* **建议**

  * 非必要情况下尽量避免使用 Git LFS，避免额外费用和超限风险。
  * 控制文件大小，合理规划版本管理。

---

# Shields.io 徽章语法 & Base64 Logo 嵌入

## 1️⃣ Markdown 徽章语法构成

### 语法示例

```markdown
[![MinerU](https://img.shields.io/badge/Official%20Site-blue?logo=data:image/svg+xml;base64,BASE64编码内容)](https://mineru.net)
```

### 拆解说明

| 部分                                 | 说明                                                                                         |
| ---------------------------------- | ------------------------------------------------------------------------------------------ |
| `[![MinerU](...)]`                 | Markdown 图片语法。`MinerU` 是 **alt text**，图片无法显示时会显示，或者给屏幕阅读器使用。                               |
| `(https://mineru.net)`             | 点击徽章跳转的目标网址。                                                                               |
| `https://img.shields.io/badge/...` | Shields.io 生成的徽章 URL。                                                                      |
| `badge/<Label>-<Message>-<Color>`  | 徽章的文字和颜色：<br>- `<Label>` 左边文字（可留空，logo 会显示在左侧）<br>- `<Message>` 右边文字<br>- `<Color>` 徽章背景颜色 |
| `?logo=...`                        | 徽章左侧小图标：<br>1. 已知品牌名（如 github）<br>2. 图片 URL<br>3. Base64 SVG 编码                            |

### 注意

* **Logo 参数不要修改**，可以保留原来的 Base64 SVG 以显示 MinerU logo。
* 外层链接 `(https://mineru.net)` 控制点击跳转。

---

## 2️⃣ 图片转换为 Base64（嵌入徽章）

### 方法 1：Mac / Linux

```bash
base64 mineru-logo.svg > mineru-logo.txt
```

* 输出文件 `mineru-logo.txt` 内容即 Base64 编码。
* 在 URL 中使用：

```
?logo=data:image/svg+xml;base64,<编码内容>
```

### 方法 2：Windows PowerShell

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("mineru-logo.svg")) > mineru-logo.txt
```

### 方法 3：在线工具

* 网站示例：

  * [https://www.base64-image.de/](https://www.base64-image.de/)
  * [https://www.base64-image.online/](https://www.base64-image.online/)
* 上传图片 → 生成 Base64 → 放入 `?logo=data:image/svg+xml;base64,...`

### 注意事项

* **推荐 SVG** → 清晰、不会模糊。
* **PNG/JPG 也可** → URL 会较长。
* Base64 可以直接嵌入 URL，无需单独托管图片。
* 完整 URL 放在 Markdown 图片语法中即可使用。

---

✅ 这样你就可以保留原有 MinerU logo，并自定义右侧文字和跳转链接。

