# Windows PowerShell 与 CMD 笔记

## 1. 为什么Windows有两个命令行工具？

Windows系统内置了两个主要的命令行工具：`cmd`（命令提示符 Command-line shells）和 `PowerShell`。

*   **`cmd` (命令提示符)**：
    *   Windows中最早内置的Shell。
    *   只能用于执行Windows命令和批处理文件（`.bat`）。
    *   功能相对有限，是老旧的DOS操作系统产物。

*   **`PowerShell`**:
    *   设计目的是扩展 `cmd` Shell的功能。
    *   不仅能运行Windows命令，还能运行 `Command-lets`（PowerShell专属命令）。
    *   提供更可扩展的脚本语言功能，是一个完整的脚本语言运行环境。

## 2. CMD 与 PowerShell 的核心区别

| 特性           | `cmd` (命令提示符)                               | `PowerShell`                                                |
| :------------- | :----------------------------------------------- | :---------------------------------------------------------- |
| **命令类型**   | 只能运行 **Windows命令**                         | 可运行 **Windows命令** 和 **PowerShell `Command-lets`**     |
| **运算能力**   | 不支持数字运算 (`1+1` 会报错)                    | 支持数字运算 (`1+1` 输出 `2`)，可定义变量并进行运算         |
| **输出格式**   | 通常返回 **纯文本** 输出，解析和处理困难         | `Command-lets` 返回 **.NET对象**，支持复杂和精确的数据操作 |
| **脚本文件**   | `.bat` 文件，语法老旧，功能局限 (如不支持 `if` 嵌套，多用 `goto`) | `.ps1` 文件，更像现代编程语言，支持括号和嵌套，代码更简洁易读 |
| **底层实现**   | 简单的Windows命令                                | `Command-lets` 由 `.NET` 库编写                             |
| **功能扩展性** | 功能有限                                         | 强大，是一个完整的脚本语言运行环境                          |

## 3. PowerShell 的核心特性与优势

### 3.1 `Command-lets`

*   **定义**：专门在Windows PowerShell中使用的命令，由`.NET`库编写。
*   **命名规范**：遵循“动词-横杠-名词”的格式，例如 `Get-Process` (获取进程)、`Set-Location` (切换目录)。
*   **功能增强**：
    *   `Set-Location` 不仅仅能用于更改文件目录，还可以用于更改注册表目录、证书存储目录等，比传统的 `cmd` 中的 `CD` 更强大。
    *   返回 `.NET` 对象，使得数据在管道中传递时能保留其结构。

### 3.2 别名（Alias）机制

为了兼容性和易用性，PowerShell引入了别名机制。

*   **兼容旧版CMD命令**：旧版 `cmd` 命令在PowerShell中通过别名链接到对应的 `Command-let`。
    *   例如：`CD` 是 `Set-Location` 的别名。在PowerShell中，`CD` 和 `Set-Location` 完全等价。
    *   **注意**：尽管名称相似，PowerShell中的 `CD` 底层实现是 `.NET` 库编写的 `Command-let`，而非简单的Windows命令。
*   **兼容部分Linux命令**：PowerShell还吸纳了一些Linux命令作为别名，降低Linux用户的学习成本。
    *   例如：`LS` 是 `Get-ChildItem` 的别名。在PowerShell中输入 `LS` 会显示当前目录文件结构，而在 `cmd` 中会报错。
    *   例如：`pwd` 是 `Get-Location` 的别名。
*   **查看别名**：
    *   `Get-Alias`：查看所有别名关系。
    *   `Get-Command`：查看命令（可显示别名）。

### 3.3 管道与管道符 (`|`)

*   **定义**：管道符 (`|`) 意思是把上一个命令的输出结果作为下一个命令的输入。
*   **优势**：由于 `Command-lets` 返回的是 `.NET` 对象，可以非常方便地使用管道符进行命令拼接，形成“流水线”式的数据处理。
*   **示例**：
    *   获取前五个CPU占用率最高的进程：`Get-Process | Sort-Object -Property CPU | Select-Object -First 5`
    *   计算Windows目录下所有EXE文件的大小：`Get-ChildItem C:\Windows -Filter *.exe | Measure-Object -Property Length -Sum`
    *   处理CSV文件：`Import-Csv data.csv | Where-Object { $_.Age -gt 30 } | ConvertTo-Html | Out-File output.html`

### 3.4 脚本编程能力

*   **`.bat` vs. `.ps1`**：
    *   `.bat` 文件：功能局限，语法老旧，例如不允许 `if` 嵌套，多使用 `goto` 语句，导致代码难以阅读和维护。
    *   `.ps1` 文件：更像现代编程语言，支持括号和嵌套 `if` 语句，代码层级清晰，更符合人类阅读习惯，大大降低编写复杂批处理程序的痛苦。

### 3.5 常用 `Command-lets` 及 Linux 兼容命令

除了基本的Windows命令，PowerShell还提供了丰富的 `Command-lets` 和通过别名兼容的Linux命令：

*   **获取命令信息**：
    *   `Get-Command`：获取所有PowerShell支持的命令。
    *   `Update-Help`：更新帮助文档。
    *   `Get-Help <Command-Name>`：查看单个命令的帮助文档和详细信息。

*   **Linux 兼容命令 (通过别名)**：
    *   `pwd` (Print Working Directory `输出当前的工作目录`) -> `Get-Location`
    *   `ls` (List `列出的当前目录的文件`) -> `Get-ChildItem`
    *   `clear` (Clear Screen `清屏`)
    *   `cat` (Concatenate/Display File `查看某个文件的内容`) -> `Get-Content`
    *   `mkdir` (Make Directory `新建一个文件夹`) -> `New-Item -ItemType Directory`
    *   `mv` (Move File/Directory `把某个文件移动到某个文件夹里`) -> `Move-Item`
    *   `cp` (Copy File/Directory `把文件复制到某个文件夹里`) -> `Copy-Item`
    
    ```powershell
    PS C:\Users\93917\Desktop\测试> cp .\测试2\powershell.ps1 ./
    ```
    ```powershell
    PS C:\Users\93917\Desktop\测试> rm .\powershell.ps1
    ```

    > **提示**
    >
    > 在 PowerShell 中，`./` 和 `.\` 都表示**当前目录**，两者在功能上是等价的，之所以可以混用，是因为 PowerShell 对路径分隔符有兼容性处理：
    > 1. **`.\`**：是 Windows 传统的路径表示方式（使用反斜杠 `\`），符合 Windows 系统的路径规范。
    > 2. **`./`**：是类 Unix 系统（如 Linux、macOS）的路径表示方式（使用正斜杠 `/`），但 PowerShell 为了兼容跨平台脚本，也支持这种写法。
    > 在 Windows 环境下的 PowerShell 中，这两种写法没有本质区别，都会被正确解析为当前目录。使用哪种写法主要看个人习惯，或者脚本是否需要兼顾跨平台场景（此时更推荐用 `/`，因为它在所有系统中都通用）。
    > 所以在你提供的命令中，`./` 和 `.\` 可以互换，效果完全相同。
    `remove` (Remove File/Directory `删除文件`) -> `Remove-Item`

*   **数据输出**：
    * 例如：
        * `ps(显示当前所有进程) | export.csv -Path test.csv` :`Export-Csv`：将数据输出为CSV格式文件。
        *   `ps ｜ convertTo-html > test.html`：将数据转换为HTML格式并输出到文件。

## 4. 总结

Windows PowerShell 不仅仅是 `cmd` 的简单替代品，它是一个**更强大、更现代化、功能更全面的命令行工具和脚本语言运行环境**。

*   **对于 `cmd` 用户**：可以无缝过渡到PowerShell，因为其兼容旧版命令。
*   **对于 Linux 用户**：可以丝滑学习和使用PowerShell，因为很多命令是共通的。

因此，PowerShell 完全可以作为 `cmd` 命令行的上位替代，推荐用户尝试和学习使用。