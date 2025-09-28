# 32_仓库高级管理与GitHub创建组织

## 一、仓库可见性管理

### 1. 修改仓库可见性

* 进入仓库 → `Settings` → `General` → 滚动至 **Danger Zone**
* 点击 **Change repository visibility**

  * 可从 **Public → Private** 或反向修改
* ⚠️ 注意事项：

  * 更改为私有不会影响他人已 fork 的项目（仍为公开）。
  * 修改可见性后：

    * ⭐Star 数、👁️ Watcher 数清零
    * Fork 出的仓库脱离与母仓库的关联

### 2. 删除仓库

* `Danger Zone` → **Delete this repository**
* 输入仓库名确认删除
* ⚠️ 已 fork 的仓库不会被删除，只会删除你自己的仓库。

---

## 二、仓库所有权转移

* 进入设置 → `Transfer ownership`
* 可转移至：

  * 另一个用户
  * 一个组织
* 填写接收者用户名 + 仓库名确认
* 接收方会收到确认邮件 → 点击确认链接完成转移
* 原所有者失去访问权限，仓库出现在新所有者名下。

---

## 三、仓库归档（Archive）

* 作用：让仓库进入 **只读状态**

  * 不可提交 Issue、PR、评论
* 设置路径：`Settings` → **Archive this repository**
* 恢复方法：

  * 点击 **Unarchive this repository** → 填写仓库名确认
  * 恢复后可重新提交代码、PR。

---

## 四、协作者管理（Collaborators）

* 进入 `Settings` → `Access` → **Collaborators**
* 点击 **Add people** → 输入用户名添加
* 对方会收到邀请邮件 → 点击 **Accept** 确认
* 协作者权限：

  * 可直接修改代码（无需 PR 流程）
  * 可随时移除协作者

### ⚠️ 个人项目的限制：

* 无法进行精细化权限管理
* 如需更细权限控制 → 建议转为 **组织项目**

---

## 五、交互与权限限制

### 1.    options（评论冷却）

* 可设置新用户或贡献者的评论间隔时间（如 24h、3天）
* 防止刷评论、灌水等行为。

### 2. Code review limit（代码审查限制）

* 勾选后，仅仓库所有者和协作者可：

  * Approve（批准）
  * Request changes（请求修改）
* 普通用户仅可发表评论。

---

## 六、仓库规则（Rules）

### 1. 创建规则

* 路径：`Settings` → `Rules` → **Create new rule**
* 可对 **Tag** 或 **Branch** 设置规则

### 2. 示例规则：禁止删除分支

* 规则名：`no delete`
* 配置：

  * **Bypass list**：不受规则限制的用户（如管理员）
  * **Target**：应用于哪些分支（如 all branches）
  * **Restrict deletions**：禁止除管理员外删除分支
  * **Block force push**：禁止强制推送

### 3. 示例规则：合并必须通过 PR

* **Require a pull request before merging**

  * 可设置：

    * 需多少人批准（0~10）
    * 新提交取消已有批准
    * 必须代码所有者审核
    * 必须解决 PR 中的所有问题才能合并
* 提高代码审查质量，保证安全合并。
* 详细可参考：https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets 
---

## 七、创建组织（Organization）

### 1. 创建流程

* 顶部点击 **New Organization**
* 选择免费计划（Free Plan）
* 填写信息：

  * 组织名称（如 `Shrimp Organization`）
  * 联系邮箱
  * 归属类型（个人 / 公司）
* 完成验证后创建成功。

### 2. 邀请成员

* 在组织页面 → `People` → **Invite member**
* 填写成员用户名或邮箱 → 对方收到邮件 → 点击 **Join**

---

## 八、组织仓库与角色权限

### 1. 创建组织仓库

* `Organization` → `Repositories` → **New Repository**
* 可选择 Public / Private
* 创建后可添加文件。

### 2. 添加协作者并设置权限

* 路径：`Settings` → `Collaborators and Teams` → **Add people**
* 权限等级：

  | 角色           | 权限说明                 |
  | ------------ | -------------------- |
  | **Read**     | 只读，无修改权限             |
  | **Triage**   | 可提交 Issue/PR，不能直接改代码 |
  | **Write**    | 可直接修改代码              |
  | **Maintain** | 可配置仓库，无法执行高危操作       |
  | **Admin**    | 最高权限，可删仓库、设安全策略等     |

---

## 九、创建团队（Team）

* 进入组织 → `Teams` → **New Team**
* 示例：创建 `APP Developer` 团队
* 可设置：

  * 公有（显示在组织列表）
  * 私有（隐藏团队）

### 1. 添加成员

* 在团队页面 → **Add member** → 输入成员用户名

### 2. 绑定仓库与团队权限

* 进入组织仓库 → `Settings` → `Collaborators and Teams`
* 移除单个用户权限 → 添加团队
* 为团队分配权限（如 Write）

---

## 十、保护主分支（Protected Branch）

* 希望保护主分支，只能提pr，其他分支可以随意写代码

* 选中 Setting -> Rulesets，点击New branch ruleset 
* 创建规则：`only PR to main`
  * 仅允许通过 **PR** 合并代码到 main
  * **Bypass list**：仅管理员不受限制
  * **Target**：main 分支
  * 勾选 **Require a PR before merging**（合并代码必须通过pr）
  * 设置至少选择 1 人批准
  * 点击 creat
  * 记得Rulesets顶端 Enforcement status ->勾选 Active，点击 `save`


### 1. 测试流程

* 开发者（团队成员）尝试提交 → 无法直接推送到 main
* 需创建新分支 → 发起 PR → 等待管理员审核
* 管理员批准 → Merge Pull Request → 代码合并成功
* 写入时会提示：You can't commit to main because it is a protected branchCreate a new branch for this commit and start a pull request 
---

## ✅ 总结

* 仓库高级管理涵盖：

  * 可见性修改、删除、转移、归档
  * 协作者与权限管理
  * 审核与分支保护规则
  * 组织与团队协作体系
* 通过 **规则 + 组织 + 团队**，可实现企业级的协作与安全控制。

---
