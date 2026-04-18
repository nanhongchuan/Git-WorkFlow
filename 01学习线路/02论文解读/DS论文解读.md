# DeepSeek-OCR: Contexts Optical Compression

**论文地址**：[https://huggingface.co/deepseek-ai/DeepSeek-OCR](https://huggingface.co/deepseek-ai/DeepSeek-OCR)

---

这篇论文《**DeepSeek-OCR: Contexts Optical Compression**》提出了一种全新的思路——通过**视觉方式压缩长文本上下文（Optical Context Compression）**，用较少的视觉token表示更多文本token，从而为大模型（LLM）解决长上下文开销问题提供新路径。

---

## 🧩 一、研究动机

* **背景问题**：LLM在处理长文本时计算量随序列长度平方增长，极度昂贵。
* **核心设想**：一页文字可转为一张图像，图像token远少于文本token ⇒ 可用视觉模态作为高效压缩介质。
* **目标**：探索“通过OCR任务实现视觉-文本压缩映射”，即从图像中重建原文。

---

## ⚙️ 二、模型架构（DeepSeek-OCR）

由两个部分组成：

1. **DeepEncoder（视觉压缩器）**

   * 由SAM-base（局部注意力）+ CLIP-large（全局注意力）+ 16×卷积压缩模块组成。
   * 能在高分辨率输入下保持低激活内存和少量vision tokens。
   * 多分辨率模式（Tiny、Small、Base、Large、Gundam）支持从64到800个vision tokens。

2. **DeepSeek3B-MoE-A570M（解码器）**

   * 采用MoE结构（激活约5.7亿参数），从压缩的视觉latent中重建文本。
   * 既具3B模型的表达能力，又保持小模型的推理效率。

---

## 🧠 三、数据引擎（Data Engine）

训练数据覆盖四类：

1. **OCR 1.0 数据**：传统文档和场景文字（约30M页，含中英及百种语言）。
2. **OCR 2.0 数据**：图表、化学式、几何图形等结构化图像解析。
3. **通用视觉数据**：图像描述、检测、grounding等任务，保留视觉理解接口。
4. **纯文本数据**：用于语言能力微调（约10%）。

训练框架采用两阶段：

* 先独立训练 DeepEncoder；
* 再用 DeepSeek3B-MoE 端到端训练 DeepSeek-OCR。

---

## 📊 四、实验结果

### 1. **压缩比实验（Fox Benchmark）**

| 压缩比  | Vision Tokens | OCR 精度     |
| :--- | :------------ | :--------- |
| 约10× | 64~100        | **96–97%** |
| 约15× | —             | 85–90%     |
| 约20× | —             | 约60%       |

👉 说明视觉压缩在10×以内几乎无损；20×仍可维持可识别结果。

### 2. **OmniDocBench实测**

* 使用仅 **100个视觉token** 即超过 GOT-OCR2.0（需256 token）；
* 使用 **400~800个token（Gundam模式）** 超越 MinerU2.0（平均需7000 token）；
* 每页OCR精度领先同类端到端模型。

### 3. **实际产能**

单张 A100-40G GPU 每日可生成 **20万页训练数据**；20节点集群可达 **3300万页/天**。

---

## 🔍 五、拓展能力

* **深层解析（Deep Parsing）**：能从文档中解析图表、化学式、几何图形甚至自然图像。
* **多语言识别**：支持约100种语言的PDF文档OCR。
* **通用视觉理解**：保留图像描述、目标检测、grounding等功能。

---

## 🧩 六、讨论与启示

* **光学上下文压缩（Optical Context Compression）**
  可实现对对话历史或长文档的高效压缩（10×），启发LLM记忆衰退（Forgetting Mechanism）研究。
* **“视觉遗忘”机制**：通过逐步降低图像分辨率模拟人类记忆衰退，减少旧信息的token开销。
* **未来方向**：结合数字-光学混合预训练、needle-in-a-haystack测试，验证极长上下文下的表现。

---

## 🧾 七、结论

> DeepSeek-OCR首次系统验证了“上下文光学压缩”的可行性。
> 在10×压缩下可近乎无损恢复文本，为LLM超长上下文处理提供了全新研究范式。
> 同时作为实用OCR系统，其在OmniDocBench上表现SOTA，并具备大规模数据生产能力。

---

# Language Modelling with Pixels

**论文地址**：[https://arxiv.org/abs/2207.06991](https://arxiv.org/abs/2207.06991)

---

## 🧠 一、核心思想

传统的语言模型（如BERT、GPT）都是**基于「文本 token」的序列**来训练的。
但这种方式有一个根本限制：

* 不同语言有不同的字符体系；
* 少数语言或特殊符号需要扩充词表；
* 跨语言迁移困难。

这篇论文由 **Phillip Rust 等人（2022/2023）** 提出一种全新的思路：

> **把文字当作图片（Pixels）来建模。**

他们提出了一个模型叫 **PIXEL（Pixel-based Encoder of Language）**：

* 不再把文字切成词或子词，而是先渲染成一张“文字图片”；
* 然后模型输入的是像素块（patch），任务是**重建被遮盖的图像区域**；
* 就像“图像版的BERT”，但预测的不是单词，而是被遮住的图像块。

---

## 📚 二、核心优势

1. **跨语言、跨文字体系**
   模型直接处理文本图像，因此对拉丁、阿拉伯、中文、日文等所有文字一视同仁，不需要繁琐的分词或词表。

2. **对噪声更鲁棒**
   拼写错误、字体变化、OCR 噪声，对 PIXEL 来说都只是像素差异，影响很小。

3. **无需巨大词表或 softmax 层**
   不再有庞大的词汇表训练问题（上万个token的softmax）。

4. **跨脚本迁移能力强**
   即使只在英文（拉丁字母）上预训练，也能较好迁移到未见过的文字体系（如阿拉伯语）。

---

## 🔬 三、实验与表现

* 模型参数：约 **8600 万（86M）**。
* 预训练数据：与 BERT 相同的英文语料。
* 任务：跨语言的句法、语义任务。

**结果：**

* 对未见过的文字（如阿拉伯语、西里尔文），PIXEL 明显优于 BERT；
* 对熟悉的文字（拉丁文），BERT 略优；
* 对字体扰动、拼写扰动任务，PIXEL 表现更稳。

---

## ⚙️ 四、原理（简化版）

1. **文本渲染 → 图像输入**
   把文字渲染成一张固定尺寸的图片。

2. **Mask 图像块**
   随机遮掉一些小块（类似于 BERT 的 [MASK] ）。

3. **模型结构**
   使用 ViT（Vision Transformer）结构编码整张图像；
   模型学习恢复被遮住的像素块。

4. **Fine-tune 阶段**
   把学到的特征用于文本分类、翻译、语义匹配等 NLP 任务。

---

## ⚠️ 五、局限性

* **计算成本高**：渲染文字+处理像素图像，速度比 token 模型慢；
* **生成能力弱**：目前 PIXEL 只能做理解（编码），不能直接生成文字；
* **字体依赖性**：如果训练与测试字体差异太大，模型可能受影响；
* **规模偏小**：只有 86M 参数，还没达到 GPT/BERT 级别的大模型效果。

---

## 🌍 六、潜在应用场景

* 多语种 OCR 与文档理解（直接吃图像）
* 小语种、无标准分词资源的语言模型
* 噪声文本（社交媒体、扫描文档）理解
* 后续可与生成式像素语言模型结合（例如 2024 年的 **PIXAR: Auto-Regressive Language Modeling in Pixel Space**）

---

## 💬 七、总结

| 对比项   | 传统 Token 模型 | PIXEL 像素模型 |
| :---- | :---------- | :--------- |
| 输入形式  | Token 序列    | 文本图像（像素）   |
| 语言依赖  | 高（需词表/分词）   | 低（所有文字通用）  |
| 噪声鲁棒性 | 较差          | 较强         |
| 速度    | 快           | 慢（渲染+视觉模型） |
| 跨语言迁移 | 弱           | 强          |
| 当前应用  | 主流          | 新方向（研究阶段）  |

---

# CLIPPO: Image-and-Language Understanding from Pixels Only

**论文地址**：[https://openaccess.thecvf.com/content/CVPR2023/papers/Tschannen_CLIPPO_Image-and-Language_Understanding_From_Pixels_Only_CVPR_2023_paper.pdf](https://openaccess.thecvf.com/content/CVPR2023/papers/Tschannen_CLIPPO_Image-and-Language_Understanding_From_Pixels_Only_CVPR_2023_paper.pdf)

---

![Image](https://www.winklersmagicwarehouse.com/wp-content/uploads/2019/02/Clipper-The-Clown-Clippo-Trick.jpg)

![Image](https://www.researchgate.net/publication/372162983/figure/fig1/AS%3A11431281172890972%401688699387003/Basic-framework-of-our-four-methods_Q320.jpg)

![Image](https://i.ytimg.com/vi/7JwlZ-lv-HY/sddefault.jpg)


### 一、论文简介

* 作者：Michael Tschannen、Basil Mustafa、Neil Houlsby（来自 Google Research, Brain Team） 
* 会议：CVPR 2023（Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition） 
* 论文链接与摘要：该模型名为 **CLIP-Pixels Only（CLIPPO）**，其核心是：**使用单一一个编码器，把文本渲染为图像（像素）后，与普通图像一起输入，做图像-文本、多模态任务。** 无需传统的 text-encoder／tokenizer／embedding 层。 

---

### 二、核心方法

* **输入形式统一**：将文本（如 caption、语句）渲染为图像（例如将文字用字体渲染成RGB图像），再与普通图片一起作为输入。 
* **单一编码器**：使用一个视觉 Transformer（如 ViT）模型，既处理图像，也处理文本渲染图像。没有专门的“文本编码器塔（text-tower）”。 
* **训练目标**：主要是对比学习（contrastive loss）——让“图像 ↔ 正确文字渲染图像”对在 embedding 空间靠近，而“图像 ↔ 不相关文字渲染”远离。没有传统的语言建模（如 masked LM）或词汇预测损失。 
* **扩展任务**：在多模态任务中，比如将图像和文本（问题）一起渲染后输入模型，实现如视觉问答（VQA）等。 
* **多语种支持**：因为没有 tokenizer，也就没有固定词汇表／子词表，理论上能自然支持多语言、多文字体系。 

---

### 三、优势与亮点

* **架构简洁**：相比传统的例如 CLIP: Contrastive Language‑Image Pre‑training 模型（CLIP 通常有一个图像编码器 + 一个文本编码器），“CLIPPO”只用一个编码器，减少了模型复杂度。 
* **无需分词器（tokenizer-free）**：文字是通过渲染变成图像输入，不再依赖词汇表、分词器、token 嵌入。这样在语言种类繁多、词汇资源有限的场景中尤为有用。 
* **跨模态任务表现良好**：实验显示，在零样本图像分类、图像-文本检索、多语种检索、VQA 等任务中，CLIPPO 接近甚至匹配了一些 token 基础模型的表现。 
* **模型参数较少**：论文中提到，其模型用参数数目比一些专用模型少，却能取得近似效果。
---

### 四、实验与性能

* 对比任务包括：零样本／少样本图像分类、图像-文本检索、多语种检索、自然语言理解任务（如 GLUE）等。* 在多语种图像／文本检索任务（如 Crossmodal3600 数据集）上，CLIPPO 在许多语言上表现匹配或优于有 tokenizer 的模型。* 在自然语言理解（NLU）任务上，虽然并不是语言模型，但当联合训练下，CLIPPO 在一些基准（如 GLUE）上超越了此前的纯像素语言建模工作。
---

### 五、局限与挑战

* **文字渲染带来的限制**：将文字变为图像虽然消除了 tokenizer，但文字语义结构（如词、句法）可能比直接处理 token 更难学习；渲染质量、字体、大小、行间距、图像噪声等都会影响效果。
* **效率与计算成本**：图像处理（文字变图像 +视觉 Transformer）在计算上可能比纯文本处理更昂贵；尤其是在批量化、超大规模训练时。
* **与专用文本模型相比仍有差距**：在仅文本任务（例如大规模语言建模）或熟悉语言（如英语）任务上，传统 token 模型仍可能更高效或更强。
* **任务适应性**：虽然在检索、分类、VQA 等任务上表现强，但在生成式任务（例如文本生成、翻译）其表现可能受限，因为它不是专用的语言生成模型。
* **文字渲染多样性问题**：在不同语言、不同字体、不同排版、不同文字方向（如阿拉伯语、竖排中文）等复杂场景，效果可能变差。

---

### 六、应用场景

* 多语言／低资源语言的图像-文本任务：由于无需 tokenizer，CLIPPO 在多语言环境中有天然优势。
* 文本＋图像混合场景：例如在图像中有文字（海报、产品图、截图），或者需同时理解图像与文字的场景。
* 简化模型部署：对于同时处理图像与文字但希望降低架构复杂度的系统，CLIPPO 可以作为一个“统一”的编码器解决方案。
* 多模态检索系统：如图片检索、图像对应多语言文本检索、跨语言图像／文本匹配。
* 教育、辅助技术、OCR增强场景：文字变成图像再与图像一起处理，可能与 OCR、视觉理解结合。

---

### 七、与其他类似工作的关系

* 与 CLIP 的区别：CLIP 模型一般为图像编码器＋文本编码器，文本通过 tokenizer 和词嵌入处理；CLIPPO 则将文本也当作图像直接输入，使用同一编码器。
* 与前面提到的像素化语言模型（如 Language Modeling with Pixels）有近似思想：即把文字渲染或转换成像素输入。但 CLIPPO 是跨模态（图像+文字）而不仅仅语言。
* 在多模态研究中，这是“无 tokenizer／统一编码器”的一种探索方向。

---

# Pix2Struct: Screenshot Parsing as Pretraining for Visual Language Understanding

**论文地址**：[https://proceedings.mlr.press/ 02/lee23g.html](https://proceedings.mlr.press/ 02/lee23g.html)

---

![Image](https://substackcdn.com/image/fetch/%24s_%217KxJ%21%2Cf_auto%2Cq_auto%3Agood%2Cfl_progressive%3Asteep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe244f638-0387-48c1-ad0f-cd7ac9416f8b_1748x672.png)

![Image](https://substackcdn.com/image/fetch/%24s_%21w8Ll%21%2Cf_auto%2Cq_auto%3Agood%2Cfl_progressive%3Asteep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdb3915c9-da20-41e3-b363-a0790627204f_1285x881.png)

![Image](https://miro.medium.com/ /resize%3Afit%3A1400/1%2Aon1BG3pHA9h1Q3wLIBbmyQ.png)

### 一、论文简介

* 题目：*Pix2Struct: Screenshot Parsing as Pretraining for Visual Language Understanding*
* 作者：Kenton Lee、Mandar Joshi、Iulia Raluca Turc、Hexiang Hu、Fangyu Liu、Julian Martin Eisenschlos、Urvashi Khandelwal、Peter Shaw、Ming‑Wei Chang、Kristina Toutanova。 * 出版／会议：在 International Conference on Machine Learning（ICML）2023 上发表。 * 核心摘要：论文提出一个预训练模型 `Pix2Struct`，用于 **纯视觉语言理解（visually-situated language understanding）**，即处理图片里含有文字、表格、界面元素的场景。预训练任务是将被遮蔽的网页截图解析成简化的 HTML 结构。使用这一通用预训练后，在多个下游任务（文档、插图、用户界面、自然图像）上表现优异。  

---

### 二、核心方法

以下几个关键点构成其方法创新：

1. **预训练任务 —— 截图解析**

   * 将网页截图（包含文字、图片、表格、按钮、表单等视觉语言元素）作为输入。
   * 随机遮蔽（mask）其中某些区域或元素。模型的任务是输出一个 “简化 HTML” 表示（包括文字节点、图片 alt-text、布局结构等）来 “解释” 这个截图。  
   * 这种任务结合了 OCR（文字识别）、语言建模（预测文字节点）、图像 captioning /结构理解（理解视觉 +布局）等预训练信号。  

2. **模型架构**

   * 一个 “图像编码器 + 文本解码器”架构（即 image-to-text）。编码器将截图转成视觉特征，解码器生成输出序列（HTML 表示）。  
   * 引入 **可变分辨率输入表示（variable-resolution input representation）**，目的是在保留截图原始宽高比与细节的同时，使模型适应不同类型输入（网页、UI、文本图、自然图像）而不只是固定尺寸。  

3. **语言提示与视觉融合**

   * 在某些场景下，除了截图本身，还会把“问题提示”或“任务提示”（比如问答问题、说明句）渲染在截图上（即把语言 prompt 也当作视觉输入的一部分）。这样模型能够处理 “图像 + 语言提示” 的输入形式。  
   * 这种方式使模型可用于 VQA（视觉问答）、界面理解等任务，输入既是视觉也含提示语。

4. **通用下游微调**

   * 预训练之后，该模型可微调到各种下游任务：文档理解（带文字 / 布局）、插图理解、用户界面（UI）元素理解、自然图像（含文字/图表）等。论文中展示其在 4 个领域共 9 个任务上的实验。  

---

### 三、主要实验与结果

* 预训练模型在多个任务上微调后，达成了令人印象深刻的效果：在 9 个下游任务中 **6 个任务**取得了 **SOTA（最优）或接近最优**。  
* 任务领域包括：

  * 文档（例如带文字+表格+图像的页面）
  * 插图（如科学图表、教科书插图）
  * 用户界面（UI 元素识别、界面截图解析）
  * 自然图像（增强场景：图像中含有文字或图表）
* 模型还在 Hugging Face 上有开源实现及多种微调版本，例如 `google/pix2struct-base`、截至文档查看。  
* 例如在 PapersWithCode 报表中，模型在 ChartQA、DocVQA、InfographicVQA 等数据集上表现出良好成绩。  

---

### 四、亮点与创新

* **统一视角**：以截图解析为预训练任务，统一了 OCR、布局理解、语言预测等多个任务信号。相比传统一个任务专一个模型的方法，这更通用。
* **多场景适用**：通过可变分辨率 + prompt 渲染 +通用架构，`Pix2Struct` 能够覆盖 UI、文档、自然图像等多个“视觉＋语言”场景。
* **减少工程依赖**：传统文档理解往往依赖 OCR 模块、布局检测、文字识别模块；而该模型通过视觉-文本直接端到端，减少外部管道依赖。
* **良好的下游迁移能力**：预训练任务设计为“网页截图解析”这一丰富多样的场景，为模型提供了强泛化能力。

---

### 五、局限性与挑战

* **任务类型偏向“识别/理解”**：虽然能处理多种视觉语言任务，但主要还是识别、解析、问答型任务；在“生成型”或“交互型”任务（如长文本生成、对话）上的探索还比较少。
* **预训练数据偏网页截图**：虽然网页截图多样，但还是局限于“结构化网页”这一类型。对于完全不同的视觉语言场景（如手绘图、复杂科学仪表板、极端布局）可能仍有差距。
* **模型计算成本**：处理高分辨率截图 +视觉编码器 +文本解码器，可能比单纯 text 模型或简单 OCR 管道更昂贵。
* **输出表达受限**：输出是“简化 HTML”结构，而不是任意自由文本，这可能会限制在某些任务上的灵活性。
* **解析能力 vs 理解深度**：虽然解析结构优秀，但模型是否真正理解语义（如逻辑关系、隐含意图）还有待进一步研究。

---

### 六、应用场景

* 文档理解：例如扫描文件、PDF 教材、报告中既有图片、表格、文字的场景。
* 用户界面理解：截图中含有按钮、导航、表单等 UI 元素，需要理解其功能或提取描述。
* 图表/教科书插图解析：例如科学图、流程图、示意图加文字说明。
* 多模态搜索／检索：比如用户上传截图并问问题，模型解析视觉内容+文字提示后回答。
* 辅助工具／无障碍辅助：将 UI 界面、图表、截图中的内容解析成文字描述，帮助视觉障碍用户。

---

### 七、与其他工作的对比

* 相比于传统 OCR + NLP 模型（先识别文字，再语言理解）而言，Pix2Struct 一体化 一个端到端模型。
* 与像 Language Modeling with Pixels（将文字渲染成图像用于语言建模）不同：Pix2Struct 不仅处理文字，还处理“视觉 + 布局 +语言提示”，侧重于 **视觉语言理解** 而非纯语言。
* 与像 CLIPPO: Image‑and‑Language Understanding from Pixels Only（把文本渲染成图像，实现统一视觉输入）相比，Pix2Struct 更专注“图像→文本”解码，并且任务是结构解析（HTML），更具理解结构的意味。
* 在 Hugging Face 上其模型接口已被集成，使用方便。

---

# Improving Language Understanding from Screenshots

**论文链接**：[https://arxiv.org/abs/2402.14073](https://arxiv.org/abs/2402.14073)

---

### 一、论文简介

* 标题：Improving Language Understanding from Screenshots
* 作者：Tianyu Gao、Zirui Wang、Adithya Bhaskar、Danqi Chen。  
* 摘要：该工作聚焦于“截图语言模型”（screenshot LMs）——即输入为图像（其中包含文本内容的截图）而不仅仅是纯文本模型。作者指出当前这类模型在语言理解任务上还落后于纯文本模型。于是提出了一种新的预训练目标 “Patch-and-Text Prediction (PTP)” 来提升截图模型的文本理解能力。  
* 关键词：截图输入、视觉-语言模型、纯视觉输入、mask patch＋mask text、语言理解任务。

---

### 二、核心方法

* **设置**：为了明确聚焦文本理解，作者把输入限定为“从纯文本渲染而来的截图”（即将文本渲染为图像，再作为模型输入）——这样就将问题简化为：一个接收视觉输入（其实是文字的图片形式）模型，如何在语言理解上达到与传统文本模型接近的表现。  
* **PTP 目标（Patch-and-Text Prediction）**：

  * 在截图图像中随机「遮盖（mask）」图像中的一些 patch（像素块） **和** 文本内的若干内容。
  * 模型输入是带有遮盖的截图图像，任务是同时恢复被遮盖的像素块 + 恢复被遮盖的文字内容。  
* **设计细节**：

  * 作者做了关于遮盖比例、patch 大小、训练稳定性的消融研究。  
  * 模型为“纯视觉输入”模型：即没有额外的 OCR 模块、也没有将截图先转换为文字再输入，而是直接让视觉模型去理解截图里的文字+结构。  
* **结果目标**：论文中目标是让截图模型在语言理解任务（比如 GLUE 一类任务）上表现接近传统的纯文本模型（如 BERT）。  

---

### 三、关键实验与结果

* 在 GLUE 任务组（8 项任务）中：模型“仅凭视觉输入”的版本在 **6 项任务中** 达到了 “与 BERT 相差在 2% 内” 的性能。  
* 相比已有 “截图语言模型” 的方法，该方法在某些数据集上提升了 **最多约 8%**。  
* 除了理解任务，作者还将 PTP 扩展用于 **自回归截图语言模型**（autoregressive screenshot LMs），显示截图上下文能够显著降低困惑度（perplexity）。  

---

### 四、亮点与贡献

* 着重于 “视觉输入中对语言理解能力的提升”——而非仅仅视觉＋语言模型。其简化设置（纯文本渲染为截图）让对比更清晰。
* 引入了同时 mask patch + mask text 的联合目标，这比单纯做图像 mask 或文字 mask 更进一步。
* 实验上证明：截图模型如果设计得当，在语言理解任务上完全有能力接近传统文本模型。
* 消融研究丰富：探讨了遮盖比例、patch 大小、训练稳定性这些“工程”细节。

---

### 五、局限性与待改进方向

* 虽然结果十分令人印象深刻，但模型仍然是在 “文字渲染截图” 的简化场景中验证，而并非所有截图场景都这么理想（真实截图可能含图像、复杂布局、噪声、OCR难题）。
* 模型仍然是理解导向（理解 +恢复），而在生成、对话、交互式任务上的表现尚未大规模验证。
* 视觉输入处理的计算成本可能比传统文本模型更高，且对于不同字体、排版、截图质量的鲁棒性还有待考察。
* 虽然“与 BERT 差距小”是好消息，但在一些任务中是否能超过或优于文本模型，还未完全体现。

---

### 六、应用前景

* 在需要“从截图直接理解文字内容”的场景（如网页截图、聊天截图、用户界面截图、表格图像）中，这种模型非常有价值。
* 可以应用于文档理解、UI 自动化、图表理解、OCR替代/补充方案。
* 对于多语言、多字体、多排版的图像化文字理解，也具备潜力。
* 未来若能扩展到截图 + 结构理解 +交互生成，将有望用于用户界面问答、屏幕自动化、辅助技术等。

---

# Leveraging Visual Tokens for Extended Text Contexts in Multi‑Modal Learning

**论文链接**：[https://proceedings.neurips.cc/paper_files/paper/2024/file/19f10adb6749b0c9f1ff7610bd01d44d-Paper-Conference.pdf](https://proceedings.neurips.cc/paper_files/paper/2024/file/19f10adb6749b0c9f1ff7610bd01d44d-Paper-Conference.pdf)

---

![Image](https://www.researchgate.net/publication/381158426/figure/fig3/AS%3A11431281249451030%401717572918274/sInContext-significantly-improves-the-OCR-ability-of-LLM-We-present-the-Rendered-Text.ppm)

![Image](https://cdn.bytez.com/mobilePapers/v2/neurips/94826/images/2-0.png)

![Image](https://substackcdn.com/image/fetch/%24s_%21PSVd%21%2Cf_auto%2Cq_auto%3Agood%2Cfl_progressive%3Asteep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2db43e7b-e61c-4425-b1f2-2b801ea75f97_1600x895.png)


### 一、背景与问题

* 随着大语言模型（LLM）和多模态大语言模型（MLLM, Multi-modal Large Language Models）发展，能够处理**长上下文（long-context）**的问题越来越重要。论文指出：在多模态模型中，要同时处理图像、文本、甚至图文混合，对于“文本上下文长度”也有很大挑战。  
* 具体地，在多模态场景中，文本长度（比如一整篇文档、很多上下文提示）带来的 token 数量和计算量非常大，导致 GPU 内存占用高、FLOPs（浮点运算）大、效率低。  
* 因此，如何在**不显著增加计算资源**的情况下，扩展模型可处理的“文本上下文长度”成为一个关键问题。

---

### 二、方法：Visualized In-Context Text Processing（VisInContext）

论文提出的方法叫做 **VisInContext（Visualized In-Context Text Processing）**。其核心思路为：

1. **将长文本渲染为图像**

   * 对于那些很长、难以直接作为文本 token 序列输入的上下文，先将文本渲染成图像（即“文字 → 图片”）。  
   * 这样做的目的是：视觉编码器（vision encoder）通常比文本编码器在处理“视觉 patch token”方面更高效（尤其在多模态模型中已有设计），所以把一部分文本“换成”视觉形式，从而降低用文本 token 直接编码带来的负担。

2. **视觉 token 代替文本 token 输入**

   * 渲染后的文本图像通过视觉编码器生成视觉 tokens，这些视觉 tokens 与原本的文本 token 一起被输入到多模态模型中。  
   * 因为视觉 token “压缩”了原本需要的文本 token 数量，所以模型可以在“等同或接近计算量”的情况下，处理更长的上下文（比如从 256 token 扩展到 2048 token）而几乎不增加 FLOPs。  

3. **具体机制细节**

   * **文本渲染**：把文本以某种字体、字号渲染成图像；一个典型尺寸如 224×224 的文本图像可以“承载”约 290 余个文本 token 的信息。  
   * **重采样 (resampler)**：模型中设计了从视觉编码器输出特征中抽取固定数量 token 的机制（resampler）以与语言模型的 token 对齐。  
   * **遮蔽 (Masking) 与对比学习 (Contrastive Loss)**：

     * 在训练期间，模型会在视觉 tokens（原图像 tokens 或文本图像 tokens）中随机遮蔽，促使模型从“文本图像”token 中学习语义。  
     * 引入了一个 “Text-Centric Contrastive Learning (TCCL)” 的损失，用于将视觉文本表示（从文本渲染图像来的 tokens）与文本 tokenizer 的 embedding 对齐，从而保证视觉 token 表示和传统文本 token 表示语义一致。  

4. **训练与推理效率提升**

   * 论文中指出，对于一个 560 亿参数的 MOE（Mixture-of-Experts）模型，使用 VisInContext 后，将 in-context 文本长度从 256 提高到 2048，而 FLOPs 几乎没有增加。  
   * 表明这种方法在训练阶段和推理阶段都非常节省资源。

---

### 三、实验结果

* 在 **few-shot（少样本）in-context evaluation** 中，使用 VisInContext 的模型在多模态任务（如 VQA、图像＋文本检索）上表现优于基线。  
* 在文档理解任务（Document QA）与**顺序文档检索 (sequential document retrieval)** 任务中也显示了较强潜力。  
* 举例来说，在 TextVQA 的 32-shot 设置下，使用 VisInContext 的模型 accuracy 从 23.2% 提升至 31.2%。（见摘要整理）  
* 论文也展示了，不仅训练时 context 长度提升，推理阶段也可输入更长文本作为视觉 token，得到近似“全文输入”的效果但计算成本低。

---

### 四、优点与创新

* **增强长上下文能力**：通过视觉 token 替代部分文本 token，突破了传统文本 token 数量限制，扩展了可用上下文长度。
* **计算效率高**：几乎不增加 FLOPs 的情况下，实现了较大提升。
* **多模态内在契合**：利用了视觉编码器在多模态模型中的优势，把文本作为视觉模块一部分，思路新颖。
* **通用性强**：该方法可作为已有多模态大语言模型（MLLM）扩展长文本处理能力的“插件”式方法。
* **提升文档理解**：在文档类任务、检索类任务中展示出应用潜力，而这些长期以来是文本模型＋OCR 模型的强项。

---

### 五、局限性与待改进方向

* **渲染为图像存在固定尺寸/效率限制**：目前文本渲染为固定大小图像，有时即使文本较少也需要处理整张图像。论文提到未来将考虑根据内容动态缩减无效 token。  
* **纯视觉文本仍有损失**：虽然渲染成图像可以“压缩”文本信息，但可能在理解细节（如结构、排版、标点）上略逊于直接文本 token。
* **适用场景可能受限**：主要适用于“长文本 + 多模态”场景；对于纯短文本或纯语言模型任务，这方法的优势可能不显著。
* **对图像／视觉资源依赖更多**：引入视觉编码、渲染流程，可能对部署设备/环境提出更高要求。
* **尚未完全替代文本 token 流程**：论文本身说明这是一种探索性方法，并非目前的主流标准。  

---

### 六、应用前景

* **文档理解系统**：如法律合同、研究报告、手册等含大量文本与图像混合的文档，可利用更长上下文理解能力。
* **多模态检索**：如用户输入一大段文本说明或历史对话，再加上图像，模型可更好理解上下文。
* **界面／网页理解**：网页、UI 界面往往包含大量文本＋布局＋图像，此方法可应用于分析与理解。
* **少样本提示 (few-shot) 系统**：在多模态 few-shot 场景中，输入更多示例上下文通常有帮助；这方法允许用更长提示而不显著加成本。
* **面向未来的大规模长文本+视觉场景**：例如会议记录＋幻灯片图片、教材＋插图、动态图像＋说明文档等，均可受益。

---

# Vision-centric Token Compression in Large Language Model

**论文链接**：[https://arxiv.org/abs/2502.00791](https://arxiv.org/abs/2502.00791)

---

### 一、论文简介

* **标题**：Vision-Centric Token Compression in Large Language Model
* **作者**：Ling Xing、Alex Jinpeng Wang、Rui Yan、Jinhui Tang
* **发表日期**：2025年2月2日
* **摘要**：该论文提出了一种新的视觉语言模型压缩方法，旨在提高长文本上下文处理的效率。通过模拟人类阅读过程，采用“慢-快”压缩框架，将远距离的低相关文本转换为图像，由轻量级的视觉编码器处理，从而减少计算和内存消耗。实验结果表明，该方法在多个基准任务上取得了显著的性能提升，并减少了计算和内存消耗。  

---

### 二、核心方法：VIST

* **方法概述**：VIST（Vision-Centric Token Compression）提出了一种“慢-快”压缩框架，模拟人类阅读过程。具体而言，

  * **快路径（Fast Path）**：将远距离的低相关文本转换为图像，由冻结的轻量级视觉编码器处理，快速获取全局上下文。
  * **慢路径（Slow Path）**：将近距离的高相关文本输入大型语言模型（LLM），进行细粒度推理。

* **关键技术**：

  * **概率感知视觉增强（Probability-Informed Visual Enhancement，PVE）**：在训练过程中，使用频率掩蔽策略，指导视觉编码器关注语义丰富的区域，模拟人类在阅读时对功能词的选择性忽略。
  * **视觉编码器**：采用轻量级的视觉编码器，处理转换后的文本图像，提取紧凑的视觉特征。

---

### 三、实验结果

* **性能提升**：在 TriviaQA、NQ、PopQA、TREF、SST2 和 SST5 等基准任务上，VIST 方法在性能上平均提升了 5.7%。
* **计算效率**：与传统的文本编码器方法相比，VIST 方法减少了约 16% 的 FLOPs 和 50% 的内存使用。

---

### 四、应用前景

* **长文本理解**：在需要处理大量文本信息的任务中，VIST 可以有效提高处理效率。
* **多模态任务**：VIST 的视觉编码器可以与文本编码器协同工作，处理包含图像和文本的多模态任务。
* **资源受限环境**：在计算资源有限的环境中，VIST 可以减少对大型模型的依赖，降低计算和内存消耗。

---
