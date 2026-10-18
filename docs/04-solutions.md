# 第四章 怎样减少 AI 味：方法、证据和可用的做法

> 写作日期：2026-10-18。文中每个事实都标了来源编号，对应文末参考文献。标「（未核对）」的是没有打开原文核对过的说法。

## 要点

1. **"降低 AI 味"其实有三个不同目标，不能混在一起**：(a) 写得更好（专家更喜欢）；(b) 更像某位作者本人；(c) 不被检测器认出来。很多工具只做 (c)，但 (c) 不等于 (a) 或 (b)。[3][22][23]
2. **证据最强的是"改"而不是"说"**：按问题片段做细粒度编辑，专家编辑效果最好，自动编辑也明显好于原稿。[3][4]
3. **用作者全部作品微调，是目前效果最强的单项方法**：专家盲评从 82.7% 偏好人类，变成 62% 偏好 AI。但成本、版权和伦理问题都很大。[9][10]
4. **谁先下笔很重要**：AI 起草、人来改，成稿在风格上仍更接近 AI，而且作者自己感觉不到 [1]；人写初稿、AI 只做编辑，留下的痕迹小得多，也不同于 AI 生成的痕迹 [2]。
5. **只靠提示词，效果有限**：指令微调模型就算被要求写口语风格，也还是名词堆叠、信息过密 [5]；"保留原声"类提示只能减轻改动幅度，改不了方向 [18]；"不要用 X"这种指令本身会让模型想到 X [12]。
6. **解码和采样的证据比宣传弱**：min-p 的效果被重新分析后受到质疑 [6][7]；Verbalized Sampling 能明显提高多样性，但多样性不等于没有 AI 味 [8]。
7. **评估不能只靠 LLM 打分**：现成大模型判断写作质量接近随机 [4]，而且偏爱自己写的东西 [25]。要用人类盲评，加上风格距离和多样性指标。

---

## 0. 先分清目标

读者说一段文字"有 AI 味"，可能指三件事：

- **质量问题**：陈词滥调、多余解释、辞藻堆砌、句子别扭、不具体。Chakrabarty 等人请 18 位受过 MFA 训练的作家编辑 LLM 段落，总结出七类问题：陈词滥调（cliché）、多余或重复的说明、辞藻堆砌（purple prose）、句子结构差、缺少具体细节、用词和措辞别扭、时态不一致 [3]。
- **不像本人**：写的东西没错，但不像这个人平时的样子 [1][15]。
- **统计特征**：熵、词汇多样性、某些高频词，这些是检测器在看的东西 [2][29]。

三者有关联，但改善一个不一定改善另一个。下面每一节都会标明它主要针对哪个目标。

---

## 1. 提示词：风格指令、禁用词表、人设、作者范文

**证据强度：弱到中**
**适用场景**：成本最低的第一步；适合格式和语气的大方向调整，不适合追求"像本人"。

**有什么证据支持：**

- 用作者自己的文本做 few-shot，在结构化文体上有用。Wang 等人用 400 多位真实作者的样本测试，发现 LLM 在新闻、邮件这类格式固定的文体上能接近作者风格，但在博客、论坛这类随意、细腻的写作上明显不行；增加示例数量的效果也有限 [15]。
- 先从作者作品中提炼"写作说明书"，再让模型照着写，效果好于直接写。Kumar 等人的 Author Writing Sheet 方法，在"抓住作者过去风格"上对无个性化基线的胜率是 78%，和作者真实作品的相似度胜率是 59%；人工评估也支持这个结果。他们还发现语言使用比情节更容易模仿 [16]。

**已知的限制：**

- **风格偏向是模型训练出来的，提示词压不住。** Reinhart 等人发现，指令微调模型使用现在分词从句的频率是人类的 2–5 倍，名词化是 1.5–2 倍；即使提示它模仿非正式的口语和写作，它仍然是名词多、信息过密的写法 [5]。
- **"保留原声"的提示只减轻程度。** van Nuenen 让三个前沿模型用三种提示改写 300 篇个人叙事。无论是"改好一点"还是"只是改写"，功能词、缩写形式、第一人称代词都会减少，词汇多样性、词长、标点都会增加。"保留作者声音"的提示能缩小变化幅度，但方向不变 [18]。
- **否定指令会适得其反。** Rana 的机制分析（单作者预印本，4 万个样本）发现，"不要用词 X"失败时，87.5% 属于"启动失败"：指令里提到这个词，反而激活了它 [12]。更早的 Pink Elephant 研究也发现，单靠提示让模型"别谈某个话题"效果不如专门训练 [13]。Anthropic 的官方提示指南也建议"告诉模型该做什么，而不是不该做什么"，并且让提示本身的风格接近你想要的输出 [14]。这属于厂商的实践建议，不是对照实验。
- **禁用词表在解码层做比在提示里做更可靠。** Antislop 研究发现，有些套话在 LLM 输出中出现的频率是人类文本的 1000 倍以上。用回溯采样器可以压住 8000 多个模式且保持质量，而简单的 token 禁用在 2000 个时就没法用了 [11]。也就是说，"禁用词"这个思路可以用，但最好放在采样器里，而不是写进提示词。

**小结**：提示词适合定方向，不适合做最后一步。正面描述（"短句、多用具体名词、可以用口语"）比列禁用词更好；作者范文加提炼出的风格说明，比只给范文更好。

---

## 2. 作者个人风格：风格指南、谁先下笔

**证据强度：中到强**（两项大样本研究从两个角度得出一致的结论）
**适用场景**：个人写作、署名专栏、个人品牌内容等，"像本人"很重要的场景。

**"AI 写、人改"：** Baumler 等人做了一项预注册研究（n=81）。被试先列要点，由模型生成婚礼誓词、道歉信等草稿，再按自己的风格修改。用 LUAR 风格嵌入测量的结果是：修改后的文本更像被试自己写的，也更不像 LLM。**但成稿在风格上仍然比被试独立写的文本更接近 LLM 文本，风格多样性也更低。** 更关键的是，被试认为修改稿和自己独立写的文本一样能代表自己的风格（差异不显著，p=.9062）。主观感受和模型测量只有弱相关（r≈0.24）[1]。也就是说：**你以为改掉了，其实没有。** 作者还发现，限制人们使用这种流程的，主要不是改稿费力，而是草稿内容缺乏新意 [1]。

**"人写、AI 改"：** Shan、Lee、Hao 分析了 45,000 篇人类和 AI 生成的文本（8 个模型、5 个领域），以及 273,420 篇 AI 编辑过的人类文本（3 个模型、31 种编辑提示、8 类编辑）。AI 生成的文本有稳定的"风格计量足迹"：熵和词汇多样性都偏高。生成文本的词汇多样性比人类高约 2 个标准差，熵高约 1 个标准差。AI 编辑却不会复制这个足迹：相对人类原文，只是词汇多样性略升、熵下降，主要变化落在词汇密度上。用风格特征区分"编辑稿和生成稿"很容易（AUC 0.98），区分"编辑稿和人类原文"难得多（AUC 0.80）[2]。

**两项研究放在一起看：** 起点决定成稿离谁更近。人先写，AI 只做编辑，成稿在统计上仍然靠近人；AI 先写，人再改，成稿仍然靠近 AI。需要注意两点：一是 [2] 测的是统计特征，不是读者感受，也没有测质量；二是两项研究都只用了英文。对中文是否成立，目前没有直接证据。

**风格指南：** 从作者语料中提炼风格说明，有 [16] 的正面证据。但 [15] 显示，越是随意、个人化的文体，越难只靠说明和示例模仿出来。

---

## 3. 编辑：专家编辑、自动编辑、人机协作

**证据强度：强**
**适用场景**：几乎所有场景，尤其是已经有 AI 初稿、需要提升质量的时候。

- **CHI 2025《Can AI writing be salvaged?》** [3]：作家们编辑了 1,057 段 LLM 文本，得到 LAMP 语料。GPT-4o、Claude-3.5-Sonnet、Llama-3.1-70B 三个模型的写作质量没有显著差别，说明问题是各家共有的。作者做了两步自动编辑流程：先找出问题片段并归类，再用分类别的 few-shot 提示（每类 25 个专家改写示例）去改写。在 600 次偏好排序中：作家编辑稿最受欢迎（65% 的情况排第一，平均名次 1.5），自动编辑稿第二（平均 1.99），原稿最差，差异显著。有意思的是，让作家标出问题片段再交给模型改，和完全自动的版本得分几乎一样 [3]。专家编辑的操作大约 65% 是替换、25% 是删除、10% 是插入 [3]。这说明**改 AI 文本主要靠删和换，而不是加**。
- **《AI-Slop to AI-Polish?》** [4]：作者把五个写作偏好数据集合成 4,729 条判断（WQ 基准）。多数强基线，包括擅长推理的前沿 LLM，在这个基准上**只比随机略好**。用专家编辑数据训练的写作质量奖励模型（WQRM）准确率 74%。再用它给多份编辑稿排序、选最好的一份（best-of-N），9 位有经验的作家有 66% 的情况同意它的选择；奖励分差大于 1 时是 72.2% [4]。
- **代价**：在 [3] 中，作家每批编辑 25 段，大约要 3 小时，报酬 100 美元。专家编辑有效，但不便宜。

**小结**：最划算的组合是"自动找问题片段 + 人工或模型按类别改写"。七类问题清单可以直接拿来当编辑检查表 [3]。

---

## 4. 模型侧：基座模型、解码、多样性、微调、奖励模型

### 4.1 基座模型 vs 指令微调模型

**证据强度：中**（诊断层面证据强；作为写作方法，缺少质量评估）
Reinhart 等人发现 Llama 3 基座模型的语法特征频率接近人类，指令微调后反而离人类更远；模型变大也没有变得更像人 [5]。Padmakumar 和 He 也发现，用 InstructGPT 协作写作会显著降低多样性，用 GPT-3 基座模型则不会 [27]。**启示**：AI 味很大一部分来自后训练。但基座模型难控制、会重复 [5]，实际用法通常是"基座模型出素材，指令模型或人来整理"。这个组合目前只是实践做法，没有对照研究。

**适用场景**：有能力部署开源模型的团队，用来做头脑风暴或生成多样的初稿。

### 4.2 解码：温度、min-p

**证据强度：弱（有争议）**
min-p 采样在 ICLR 2025 被报告能在高温下同时提升质量和多样性，人工评估也偏好它 [6]。但 Schaeffer 等人重新分析后指出：原文的人工评估遗漏数据、统计检验有误；控制超参数数量后，min-p 并不优于基线 [7]。**结论**：调高温度、换采样器可以增加变化，但没有可靠证据表明它能减少 AI 味。

### 4.3 对抗模式坍缩：Verbalized Sampling

**证据强度：中**
Zhang 等人认为模式坍缩的一个数据层原因是"典型性偏好"：标注者在偏好数据里系统性地偏爱熟悉的文本。他们提出让模型"列出 5 个回答并给出各自概率"，在创意写作上把多样性提高到直接提示的 1.6–2.1 倍，而且越强的模型受益越多 [8]。**限制**：多样性提高说明不再千篇一律，但单篇文字有没有套话，要另外检查。

**适用场景**：选题、标题、开头等需要多个备选的环节。

### 4.4 用高质量书籍或作者作品微调

**证据强度：强**（两项研究，其中一项预注册）
Chakrabarty 和 Dhillon（CHI 2026）让 28 位 MFA 作家和三个 LLM 一起模仿 50 位知名作家。在只用提示的条件下，专家评审 82.7% 偏好人类作品；用作者全部作品微调 GPT-4o 后，变成 62% 偏好 AI。普通读者在两种条件下都偏好 AI [9]。微调需要的 token 量平均是提示条件的 583 倍 [9]。同组的预注册扩展研究（28 位 MFA 读者、516 位普通读者）报告：微调后的输出只有 3% 被主流检测器标为 AI，提示条件下是 97%；每位作者的微调成本中位数约 81 美元；中介分析表明，微调去掉了那些让读者扣分的"AI 怪癖" [10]。

**个人规模**：Panza 用微调加检索增强，用不到 100 封邮件就能让模型较好地模仿用户写邮件，还能在很有限的算力上跑 [17]。作者也明确提醒：这同时是一种冒充他人的攻击手段 [17]。

**风险**：版权（[9][10] 用的是购买的电子书，并讨论了合理使用问题）、冒充他人、绕过检测。只应该用你自己或已经得到授权的语料。

### 4.5 写作奖励模型和偏好优化

**证据强度：中**
- 专门训练的写作奖励模型比现成 LLM 当裁判更准：WQRM 74% [4]；LitBench 上训练的奖励模型 78%，最强的现成裁判（Claude-3.7-Sonnet）73% [26]。
- **DPO 要小心用。** Antislop 发现，用 DPO 去压套话，写作质量和词汇多样性都明显下降，压制效果也更弱；它提出的逐 token 方法 FTPO 能减少 90% 的套话，同时保持或提高跨领域评测成绩 [11]。
- 用作者本人的数据做 DPO：本章没有找到针对"降低 AI 味"的对照研究，证据空白。

---

## 5. 多步流水线：起草 → 批评 → 修改

**证据强度：弱到中**（方向一致，但直接研究很少）
**适用场景**：事实类、说明类文本，用来查错补漏；如果目标是保留个人声音，要谨慎使用。

**支持的证据**：[3] 的"找片段 → 改片段"本身就是两步流水线，而且有效；[4] 的"多次编辑 + 奖励模型挑选"也有效。共同点是：**有明确的问题清单或外部打分，而且只改局部。**

**反对的证据：**
- 自我评审有偏差。LLM 会认出并偏爱自己的输出 [25]；[4] 也引用了这样的观察：LLM 甚至偏爱自己的文字胜过诺贝尔奖得主的文字。用同一个模型当作者和批评者，容易越改越像它自己。
- 多轮改写会趋同。一篇硕士论文用 292 篇 NeurIPS 引言做实验，发现反复改写会收敛到一个稳定版本，离原文越来越远；不同模型收敛到各自的风格 [20]。这只是学位论文，用的是 7B–30B 的小模型，证据较弱。
- 多智能体互相讨论会让内容同质化；让各方独立修改、只交换反馈，效果更好 [19]。
- 整篇改写有"抛光"效果，会削弱个人声音 [18]。

**一条实践观察（假设，不是结论）**：本项目在一次小规模的金句实验中注意到，"起草 → 批评 → 修改"流水线产出的句子，比"带风格指南直接模仿"更短、更整齐划一。样本很小，没有盲评，也没有统计检验，只能当作待检验的假设：**批评环节可能在把文字往"安全、规整"的方向推。** 这和 [18][20] 的方向一致，但需要正式实验验证。

---

## 6. "Humanizer"：绕过检测器的工具

**证据强度：强（说明它能骗过部分检测器）/ 强（说明它不能提高质量，也骗不过有经验的人）**
**适用场景**：本章不推荐用于任何需要诚信的场景。

- **它们做什么**：改写 AI 文本，让检测器认不出来。早在 2023 年，DIPPER 改写器就能把 DetectGPT 的检出率从 70.3% 降到 4.6%（假阳性率 1% 时）[21]。Masrour 等人测了 19 个 humanizer 和改写工具，发现很多检测器认不出改写后的文本，而且这些工具在保留原意上有问题；同时他们也训练出了能识别 humanizer 文本的检测器 [22]。
- **骗过检测器 ≠ 写得好**：humanizer 优化的是检测器分数，不是读者感受。经常用 ChatGPT 写作的人是很强的"人肉检测器"：5 人多数投票在 300 篇文章中只错 1 篇，面对改写和 humanizer 也很稳。他们除了看"AI 词汇"，还会看正式程度、原创性、清晰度，这些是自动检测器难以捕捉的 [23]。
- **军备竞赛**：改写可以攻击检测器 [21]，检测方也在用检索 [21] 和数据增强 [22] 反击。而作者自有语料微调的输出，几乎不会被检测器标出 [10]。这说明"能不能被检测出来"越来越不能代表文本是怎么写出来的。
- **伦理问题**：检测器会把非英语母语者的文字误判为 AI [24]。这意味着有人会被迫用 humanizer 来"自证清白"，而真正作弊的人也会用同样的工具。在学术和考试场景，用 humanizer 隐瞒 AI 使用是不诚信的；正确做法是按规定披露（见第 8 节 c）。

---

## 7. 评估：怎么知道 AI 味真的降了

**证据强度：中**（每种方法都有研究支持，但没有公认的组合标准）

| 评估方式 | 能测什么 | 已知问题 |
|---|---|---|
| 专家盲评（成对比较） | 质量、风格忠实度 | 贵；专家和普通读者的偏好不同 [9][10] |
| 普通读者盲评 | 实际受众感受 | 普通读者常偏好 AI 文本 [9]，不能代表"没有 AI 味" |
| 有经验的 LLM 用户识别 | 能不能被认出 | 很准，可以当作"红队" [23] |
| LLM 当裁判 | 便宜、可规模化 | 写作质量判断接近随机 [4]；偏爱自己的输出 [25]；最好的也只有约 73% [26] |
| 专门训练的写作奖励模型 | 质量排序 | 74–78% [4][26]，适合筛选，不适合当最终裁判 |
| 风格嵌入距离（如 LUAR） | 像不像本人 | 和作者主观感受只弱相关 [1] |
| 风格计量特征（熵、词汇多样性、词汇密度等） | 统计痕迹 | 生成和编辑留下的痕迹不同 [2] |
| 多样性指标（同提示多次输出的相似度、Sui Generis 分数等） | 是否千篇一律 | Sui Generis 和人类"惊讶感"中度相关 [28]；多样性≠质量 |
| 过量词频统计 | 群体层面的 AI 使用 | 适合大语料，例如对 1500 万篇生物医学摘要的分析 [29]，不适合判断单篇 |

**建议的最小评估组合**：(1) 一组和作者过往文本做的成对盲评；(2) 和作者语料的风格距离；(3) 同一提示多次输出的多样性；(4) 七类问题清单 [3] 的人工抽查。LLM 裁判只用来初筛，而且不要用生成模型给自己打分 [25]。

---

## 方法对比表

| 方法 | 原理 | 证据 | 成本 | 风险 |
|---|---|---|---|---|
| 风格指令 / 人设提示 | 用文字描述目标风格 | 弱：后训练偏向压不住 [5][18] | 很低 | 以为有效，其实没变 |
| 禁用词表（写在提示里） | 告诉模型别用某些词 | 弱：否定指令会启动目标词 [12][13] | 很低 | 适得其反；换成近义套话 |
| 禁用词（放在采样器里） | 解码时回溯、压掉模式 | 中：可压 8000+ 模式 [11] | 中（需要开源模型） | 只管词汇，不管结构 |
| 作者范文 few-shot | 上下文模仿 | 中：正式文体有效，随意文体弱 [15] | 低 | 抄袭范文内容 |
| 作者风格说明书 | 先提炼风格，再按说明写 | 中：胜率 78% [16] | 低到中 | 说明书本身被写成套话 |
| 人写初稿 + AI 轻编辑 | 起点是人 | 中到强：痕迹小 [2] | 中（人要先写） | 多轮整篇润色会抹平声音 [18][20] |
| AI 初稿 + 人改 | 起点是 AI | 中到强：有改善，但仍偏 AI，自己察觉不到 [1] | 低到中 | 残留 AI 风格 |
| 专家按类别编辑 | 删、换问题片段 | 强 [3] | 高（[3] 中每 25 段约 100 美元） | 依赖编辑本人的水平 |
| 自动"找片段 → 改片段" | 两步流水线 | 强：显著好于原稿，不如专家 [3] | 低 | 改不到深层问题 |
| 奖励模型 best-of-N | 多份候选里挑最好的 | 中：66–72% 和专家一致 [4] | 中 | 奖励被钻空子 |
| 基座模型生成素材 | 绕开后训练偏向 | 中（诊断层面）[5][27] | 中 | 难控制、会重复 |
| min-p / 调温度 | 改采样分布 | 弱（有争议）[6][7] | 很低 | 不连贯 |
| Verbalized Sampling | 让模型给出分布 | 中：多样性 1.6–2.1 倍 [8] | 低 | 多样≠无套话 |
| 作者语料微调 | 学会作者的分布 | 强 [9][10]；小数据也可以 [17] | 中到高 | 版权、冒充他人、绕过检测 |
| DPO 压套话 | 偏好优化 | 弱到反面：质量和多样性下降 [11] | 高 | 伤害写作质量 |
| 起草-批评-修改流水线 | 自我批评再改 | 弱到中：局部改有效，整篇改易趋同 [3][19][20][25] | 中 | 越改越整齐、越像模型 |
| Humanizer | 针对检测器改写 | 能骗过部分检测器 [21][22]，骗不过有经验的人 [23] | 低 | 不诚信；不提高质量 |

---

## 8. 推荐做法

下面三套做法按证据强度排列步骤。每一步标明：**【研究】** 有直接研究支持；**【推论】** 由研究推出，但没有直接检验；**【实践】** 只是常见做法。

### (a) 个人写作者，手里有自己过去的文章

1. **自己先写初稿，哪怕很粗糙。** 【研究】起点决定成稿离谁更近 [1][2]。AI 可以帮你列提纲、提问题，但第一版句子最好由你自己写。
2. **AI 只做局部编辑，不做整篇润色。** 请它按七类问题 [3] 标出有问题的句子，你决定改不改。【研究】局部编辑有效 [3]；整篇改写会抹掉代词、缩写、口语等个人特征 [18]。
3. **把常见问题写成正面要求，而不是禁用词表。** 比如写"用具体例子，句子长短交替"，而不是"不要用'赋能'"。【研究+实践】[12][14]
4. **从过去 20–50 篇文章中提炼一份风格说明，和 3–5 篇范文一起给模型。** 【研究】[16]（数量是实践建议，研究中平均每位作者 16 篇）；文体越随意，效果越差 [15]。
5. **可选：语料多、有算力时，用自己的文本做轻量微调。** 【研究】[9][10][17]。只用自己的语料。
6. **自检**：隔几天，把 AI 参与的稿子和你独立写的旧稿混在一起盲读；或者请一位常用 ChatGPT 的朋友来认。【研究】你自己的感觉不可靠 [1]，有经验的读者很准 [23]。

### (b) 团队规模化生产内容

1. **建立编辑清单和片段级标注流程**：用七类问题 [3] 加上团队自己的高频套话表。【研究】[3]
2. **自动"找片段 → 改片段"做第一轮，人工编辑抽检第二轮。** 【研究】自动编辑显著好于原稿，但不如专家 [3]；让人标片段、机器改写，和全自动差不多 [3]，所以人工时间最好花在最后判断上。
3. **一个选题生成多份候选，用专门的写作奖励模型初筛，再由人选。** 【研究】[4][26]。不要用生成模型给自己的稿子打分 [25]。
4. **用开源模型时，把禁用模式放进采样器（例如 Antislop 回溯采样），不要只写在提示里。** 【研究】[11]
5. **选题和开头阶段用 Verbalized Sampling 或基座模型拓宽思路。** 【研究】多样性 [8][27]；【推论】这样做能减少全站同质化。
6. **品牌声音稳定后，用团队授权的历史稿件微调。** 【研究】[9][10]；【实践】注意版权和数据授权。
7. **流水线不要过长。** 批评环节只指出问题，由人或独立的模型改；不要让同一个模型整篇改很多轮。【研究+推论】[19][20][25]；本项目金句实验的观察（假设）。
8. **每月做一次评估**：成对盲评、和品牌语料的风格距离、同提示多样性。【研究】见第 7 节。

### (c) 学术写作

1. **先查规定并按要求披露。** 例如 Nature 及 Springer Nature 期刊：LLM 不能署名为作者，使用 LLM 要在方法或致谢部分说明 [30]；也有学者提出了可以直接引用的使用声明 [31]。【研究/政策】
2. **论点、数据、引用由人负责；AI 只做语言层面的编辑。** 【研究】人写、AI 改，痕迹最小 [2]；而且 AI 不能为内容负责 [30]。
3. **学术腔本身就是 AI 腔的放大版，要主动减少名词化和分词从句。** 指令微调模型用名词化是人类的 1.5–2 倍，用分词从句是 2–5 倍 [5]。学术写作中尤其要检查"AI 高频词"：分析显示 2024 年至少 13.5% 的生物医学摘要经过 LLM 处理，有些子领域达到 40% [29]。【研究】
4. **避免多轮整篇润色。** 一轮语法修改通常就够了。【研究（弱）】反复改写会让科学文本趋同、偏离原作者 [20]。
5. **不要用 humanizer。** 它不能提高质量 [23]，还可能构成学术不端；如果被检测器误判（非母语作者更容易被误判 [24]），应该用写作过程记录（草稿、版本历史）来证明，而不是改写来"过检测"。【研究+实践】

---

## 参考文献

[1] Connor Baumler, Calvin Bao, Huy Nghiem, Xinchen Yang, Marine Carpuat, Hal Daumé III. "Can You Make It Sound Like You? Post-Editing LLM-Generated Text for Personal Style." ACL 2026 (Long). https://aclanthology.org/2026.acl-long.2030/ ；arXiv:2604.24444

[2] Zhengyang Shan, Yukyung Lee, Sophie Hao. "AI Writers Have a Consistent Stylometric Footprint, but AI Editors Do Not." arXiv:2608.27855, 2026（arXiv 注明 EMNLP 2026 Main）. https://arxiv.org/abs/2608.27855

[3] Tuhin Chakrabarty, Philippe Laban, Chien-Sheng Wu. "Can AI writing be salvaged? Mitigating Idiosyncrasies and Improving Human-AI Alignment in the Writing Process through Edits." CHI 2025. https://doi.org/10.1145/3706598.3713559 ；arXiv:2409.14509

[4] Tuhin Chakrabarty, Philippe Laban, Chien-Sheng Wu. "AI-Slop to AI-Polish? Aligning Language Models through Edit-Based Writing Rewards and Test-time Computation." arXiv:2504.07532, 2025. https://arxiv.org/abs/2504.07532

[5] Alex Reinhart, Ben Markey, Michael Laudenbach, Kachatad Pantusen, Ronald Yurko, Gordon Weinberg, David West Brown. "Do LLMs write like humans? Variation in grammatical and rhetorical styles." PNAS 122 (2025) e2422455122. https://doi.org/10.1073/pnas.2422455122

[6] Minh Nhat Nguyen, Andrew Baker, Clement Neo, Allen Roush, Andreas Kirsch, Ravid Shwartz-Ziv. "Turning Up the Heat: Min-p Sampling for Creative and Coherent LLM Outputs." ICLR 2025 (Oral). https://arxiv.org/abs/2407.01082

[7] Rylan Schaeffer, Joshua Kazdan, Yegor Denisov-Blanch. "Min-p, Max Exaggeration: A Critical Analysis of Min-p Sampling in Language Models." arXiv:2506.13681, 2025. https://arxiv.org/abs/2506.13681

[8] Jiayi Zhang, Simon Yu, Derek Chong, Anthony Sicilia, Michael R. Tomz, Christopher D. Manning, Weiyan Shi. "Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity." arXiv:2510.01171, 2025; ICML 2026 (PMLR v306). https://arxiv.org/abs/2510.01171

[9] Tuhin Chakrabarty, Paramveer S. Dhillon. "Can Good Writing Be Generative? Expert-Level AI Writing Emerges through Fine-Tuning on High Quality Books." CHI 2026. https://doi.org/10.1145/3772318.3791276 ；arXiv:2601.18353

[10] Tuhin Chakrabarty, Jane C. Ginsburg, Paramveer Dhillon. "Readers Prefer Outputs of AI Trained on Copyrighted Books over Expert Human Writers." arXiv:2510.13939, 2025（预印本，审稿中）. https://arxiv.org/abs/2510.13939

[11] Samuel Paech, Allen Roush, Judah Goldfeder, Ravid Shwartz-Ziv. "Antislop: A Comprehensive Framework for Identifying and Eliminating Repetitive Patterns in Language Models." ICLR 2026. https://arxiv.org/abs/2510.15061

[12] Shailesh Rana. "Semantic Gravity Wells: Why Negative Constraints Backfire." arXiv:2601.08070, 2026（单作者预印本）. https://arxiv.org/abs/2601.08070

[13] Louis Castricato, Nathan Lile, Suraj Anand, Hailey Schoelkopf, Siddharth Verma, Stella Biderman. "Suppressing Pink Elephants with Direct Principle Feedback." arXiv:2402.07896, 2024. https://arxiv.org/abs/2402.07896

[14] Anthropic. "Prompting best practices"（Claude 官方文档，访问于 2026-10-18）. https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices

[15] Zhengxiang Wang, Nafis Irtiza Tripto, Solha Park, Zhenzhen Li, Jiawei Zhou. "Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors." Findings of EMNLP 2025. https://aclanthology.org/2025.findings-emnlp.532/ ；arXiv:2509.14543

[16] Nischal Ashok Kumar, Chau Minh Pham, Mohit Iyyer, Andrew Lan. "Whose story is it? Personalizing story generation by inferring author styles." IJCNLP-AACL 2025. https://arxiv.org/abs/2502.13028

[17] Armand Nicolicioiu, Eugenia Iofinova, Andrej Jovanovic, Eldar Kurtic, Mahdi Nikdan, Andrei Panferov, Ilia Markov, Nir Shavit, Dan Alistarh. "Panza: Design and Analysis of a Fully-Local Personalized Text Writing Assistant." arXiv:2407.10994, 2024. https://arxiv.org/abs/2407.10994

[18] Tom van Nuenen. "Voice Under Revision: Large Language Models and the Normalization of Personal Narrative." arXiv:2604.22142, 2026. https://arxiv.org/abs/2604.22142

[19] Weiyue Li, Mingxiao Song, Zhenda Shen, Dachuan Zhao 等. "LLM Review: Enhancing Creative Writing via Blind Peer Review Feedback." arXiv:2601.08003, 2026. https://arxiv.org/abs/2601.08003

[20] Νικόλαος Χ. Χαραλαμπίδης (Nikolaos Ch. Charalampidis). "The Vanishing Author: Do Multi-Turn LLM revisions drive scientific writing toward a uniform style?" 学位论文, Aristotle University of Thessaloniki, 2026. https://doi.org/10.26262/heal.auth.ir.375923

[21] Kalpesh Krishna, Yixiao Song, Marzena Karpinska, John Wieting, Mohit Iyyer. "Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense." NeurIPS 2023. https://arxiv.org/abs/2303.13408

[22] Elyas Masrour, Bradley Emi, Max Spero. "DAMAGE: Detecting Adversarially Modified AI Generated Text." arXiv:2501.03437, 2025（作者来自检测器公司 Pangram Labs，存在利益相关）. https://arxiv.org/abs/2501.03437

[23] Jenna Russell, Marzena Karpinska, Mohit Iyyer. "People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text." ACL 2025. https://doi.org/10.18653/v1/2025.acl-long.267 ；arXiv:2501.15654

[24] Weixin Liang, Mert Yuksekgonul, Yining Mao, Eric Wu, James Zou. "GPT detectors are biased against non-native English writers." Patterns, 2023. https://arxiv.org/abs/2304.02819

[25] Arjun Panickssery, Samuel R. Bowman, Shi Feng. "LLM Evaluators Recognize and Favor Their Own Generations." NeurIPS 2024. https://arxiv.org/abs/2404.13076

[26] Daniel Fein, Sebastian Russo, Violet Xiang, Kabir Jolly, Rafael Rafailov, Nick Haber. "LitBench: A Benchmark and Dataset for Reliable Evaluation of Creative Writing." EACL 2026. https://arxiv.org/abs/2507.00769

[27] Vishakh Padmakumar, He He. "Does Writing with Language Models Reduce Content Diversity?" ICLR 2024. https://arxiv.org/abs/2309.05196

[28] Weijia Xu, Nebojsa Jojic, Sudha Rao, Chris Brockett, Bill Dolan. "Echoes in AI: Quantifying lack of plot diversity in LLM outputs." PNAS, 2025. https://doi.org/10.1073/pnas.2504966122

[29] Dmitry Kobak, Rita González-Márquez, Emőke-Ágnes Horvát, Jan Lause. "Delving into LLM-assisted writing in biomedical publications through excess vocabulary." Science Advances 11(27), 2025. https://doi.org/10.1126/sciadv.adt3813

[30] Nature 社论. "Tools such as ChatGPT threaten transparent science; here are our ground rules for their use." Nature 613, 612 (2023). https://www.nature.com/articles/d41586-023-00191-1

[31] Sebastian Porsdam Mann, Anuraag A. Vazirani, Mateo Aboy, Brian D. Earp, Timo Minssen, I. Glenn Cohen, Julian Savulescu 等. "Guidelines for ethical use and acknowledgement of large language models in academic writing." Nature Machine Intelligence, 2024. https://www.nature.com/articles/s42256-024-00922-7 （只看过摘要和页面，没读正文）

**非文献来源**：第 5 节的"金句实验"是本项目内部的实践观察，没有发表，样本小，只作为假设。
