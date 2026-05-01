# GitHub项目移交

![alt text](image-5.png)

---

## **方案 1：先上传到个人 GitHub，再移交**

### **步骤 A：上传项目到个人 GitHub**

1. 在 GitHub 上创建一个新的仓库（Repository），比如叫 `my-project`。
2. 在本地项目文件夹里，初始化 Git 并添加远程仓库：

```bash
cd path/to/your/project
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<你的用户名>/my-project.git
git push -u origin main
```

### **步骤 B：移交仓库到公司组织**

1. 等你加入公司组织账号（Organization）后，在 GitHub 上进入你的个人仓库。
2. 点击 **Settings → General → Transfer ownership**。
3. 在弹出的框里，输入公司组织账号的名称，例如 `company-org`。
4. 确认仓库名称和新的拥有者账号，然后提交。
5. 移交完成后，该仓库就属于公司组织了，你和组织成员都能访问。

**注意事项：**

* 你个人仓库移交后，你的个人账户仍然可以选择保留该仓库的管理员权限，具体看组织的设置。
* 移交前确保仓库没有敏感信息，或者公司允许你先上传到个人账号。
* 移交过程中，仓库的 URL 会变，例如原来是：

  ```
  https://github.com/yourusername/my-project
  ```

  移交后会变成：

  ```
  https://github.com/company-org/my-project
  ```

  本地 Git 的远程地址也要更新：

  ```bash
  git remote set-url origin https://github.com/company-org/my-project.git
  ```

---

## **方案 2：等待加入组织再上传**

如果公司对代码安全要求严格，不希望在个人账号托管，可以先在本地开发，等加入组织后再直接在组织下建仓库上传。

**建议**：如果你能确定组织允许先上传到个人仓库，方案 1 更方便。
