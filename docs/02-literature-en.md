# 第二章 英文研究综述（2021–2026）：AI 味是什么、从哪来、怎么认、怎么改

> 范围：2021 年 1 月到 2026 年 10 月的英文论文，加一份维基百科编辑整理的实践清单。每条结论都对应下面参考文献里我实际打开过的来源（至少读过摘要）。数字照原文抄，没有自己推算。检索日期：2026-10-18。

---

## 要点（一页看完）

- **普通人基本认不出 AI 文字，但"常用 AI 写东西的人"能认出来。** GPT-3 时代，没受过训练的读者判断准确率约 50%，等于瞎猜 [1]；4,600 人的实验里也只有 50–52% [2]。但 2025 年的研究发现，5 位经常用 LLM 写东西的人投票表决，300 篇文章只错 1 篇 [3]。关键不在聪明，而在"见得多"和"看对地方"。
- **普通人的直觉是错的。** 很多人把"用第一人称""用缩写""聊家庭"当成人写的标志 [2]，把"语法完美""语气中性""用词高级"当成 AI 的标志 [3]。这些线索都不可靠，还容易被利用。
- **AI 味能被拆开描述。** 职业作家把 AI 文字的问题归成 7 类：陈词滥调、不必要的解释、辞藻堆砌（purple prose）、句子结构差、缺少具体细节、用词别扭、时态不一致 [11]。语言学测量发现，指令微调后的模型偏爱名词化、信息密集的写法：GPT-4o 用现在分词从句的频率是人的 5.3 倍，名词化是 2.1 倍 [13]。
- **AI 味主要是"后训练"造成的，不是预训练数据本身。** 同一系列模型里，base 模型的用词和语法接近人类，指令微调后差距反而变大 [13]。RLHF 降低输出多样性 [21]；标注员偏爱"熟悉、典型"的文字（typicality bias），这是模式坍缩（mode collapse）的一个数据层面原因 [22]；后训练会把小说的主题变化、情绪起伏和风格差异一起压平 [23]。
- **AI 味已经进入人类语言。** 2024 年 PubMed 摘要中至少 13.5% 经过 LLM 处理 [14]；ChatGPT 偏爱的 "delve" 等词在播客口语里也明显变多 [20]。
- **最大的长期风险是"大家越写越像"。** 个人用 AI 写得更好，但群体作品更相似 [32]；不同公司的模型彼此也很像 [29][34]；用 LLM 润色会让写作复杂度的方差下降 21–50% [31]；二语写作者的个人语气和礼貌习惯会被改成统一的英美式 [35]。
- **读者知道是 AI 写的，就会打折。** 跨 16 个实验、27,491 人的研究显示，只要读者相信文字由 AI 写或 AI 参与，评价就下降，中介变量是"真实感"（authenticity），而且很难消除 [36]。但盲测时，普通读者常常更喜欢 AI 文字 [5][38][39]。
- **机器检测不是可靠的裁判。** 检测器会被改写攻击轻松绕过 [44][45]，还会把非母语者的作文误判成 AI（平均误报率 61.3%）[43]。水印（如 SynthID-Text）是另一条路，但需要模型提供方配合 [42]。

---

## 一、人能认出 AI 写的东西吗？

**早期结论：认不出。** Clark 等人 [1] 让没受过训练的评估者区分人写的文字和 GPT-3 写的文字（故事、新闻、菜谱三类），准确率 49.9%，和随机猜一样。他们试了三种快速培训方法，准确率最高只升到 55%，而且各领域不稳定。评估者的理由近一半关注"形式"（格式、风格、语气），只有四分之一关注"内容"，理由之间还常常互相矛盾。

**为什么认不出：直觉本身有偏差。** Jakesch 等人 [2] 做了 6 个实验，4,600 人判断个人简介（求职、民宿、约会场景）是人写还是 AI 写，准确率只有 50–52%；给钱或给反馈都没用。但大家的判断并不随机，而是"错得很一致"：人们把第一人称代词、缩写、谈家庭等特征当成人写的标志。作者进一步证明，AI 可以利用这些直觉，写出被认为"比人更像人"的文字。

**转折：有经验的人能认出来。** Russell、Karpinska 和 Iyyer [3]（ACL 2025）找人读 300 篇英文非虚构文章（GPT-4o、Claude-3.5-Sonnet、o1-Pro 生成，部分经过改写或"人性化"处理）。结果分成两群：
- 很少用 LLM 写作的人，平均真阳性率（TPR）56.7%，假阳性率（FPR）约 52%，接近瞎猜。
- 经常用 LLM 写作的 5 位"专家"，平均 TPR 92.7%，FPR 约 3–4%；五人多数投票在 300 篇里只错 1 篇（错在 o1-Pro 那一组）。在最难的"o1-Pro + 人性化"设置下，多数投票 TPR 仍是 100%，而开源检测器 Binoculars 只有 6.7%，Fast-DetectGPT 只有 23.3%。只有商业检测器 Pangram 能和专家打平。

专家用的线索（按出现在解释中的比例）：词汇 53.1%（如 vibrant、crucial、testament）、句子结构 35.9%（如 "not only … but also"、总是列三项、句长太均匀）、语法 24.8%、原创性 23.7%（"安全"、没惊喜、没幽默）、清晰度 19.5%（过度解释、"讲"而不是"演"）。此外还有：引语格式总是一样（比如总放在段尾）、结论乐观而空泛、人名前加头衔的频率偏高。新手常犯的错恰好相反：把一切"高级词"都当 AI 标志、以为人写的语法更正确（其实人犯的语法错误更多）、把中性语气当成 AI。即使模型被要求避开"AI 词汇"，专家仍能靠结构、原创性等线索认出来；但一位过度依赖"口语化 = 人写"的专家被 o1-Pro 骗过了。

**其他语言、其他人群的结果：**
- 日语：Zaitsu 等人 [4] 对比 100 篇人写和 7 个 LLM 写的 350 篇公共评论。文体统计特征（短语模式、词性二元组、虚词）配随机森林分类，准确率 99.8%；但 403 名日本参与者判断能力"有限"。人写文本只有 31.5% 被正确认成人写；更流畅的 o1 让人更容易误判成"人写"，同时更自信。参与者主要靠措辞、句尾、连词、标点等表面印象判断。
- 德语学术文本：63 位大学讲师对 AI 文本识别率 57%，对人写文本 64%，和检测器没有显著差别；"专业水平"的 AI 文本只有不到 20% 的人认出来 [6]。
- 捷克语：254 人参加实验，有即时反馈的那组准确率和信心校准都明显提升；没有反馈时，人在"最有信心"时错得最多 [7]。
- 多语言：16 个数据集、9 种语言、19 位标注员，平均准确率 87.6%；主要差别在具体性、文化细节和多样性 [8]。
- 2026 年的新结果有分歧：一项研究发现"更频繁、更多样地使用 AI 平台"反而和更低的辨别力相关，但带标签样例 + 即时反馈的训练能显著提高准确率 [9]；另一项 1,054 人的新闻研究认为普通人"不能可靠地分辨"，自评领域专长和准确率相关（r = .35），连续判断约 30 篇后会因疲劳下降 [10]。这和 [3] 并不完全矛盾：[3] 的"专家"是**经常用 LLM 写作**的人，读的是长文，并且写了详细理由；[9] 测量的是泛泛的 AI 使用频率。

**小结：** "人认不出 AI" 只对新手成立。识别能力可以学，靠的是对具体模式的熟悉加上反馈，而不是凭感觉。

**对写作者的启示**
- 你的读者里越来越多人是"常用 AI 的人"。他们不看你有没有用"高级词"，而是看结构是否套路、有没有具体信息、有没有出人意料的地方。
- 别指望靠加缩写、加口语、加"我觉得"来去 AI 味。这些正是最容易被模仿、也最容易误导人的线索 [2][3]。
- 想练"AI 味雷达"，最有效的办法是拿已知来源的文本做对照练习，并及时核对答案 [7][9]。

---

## 二、AI 味由什么组成？

**作家视角：7 类毛病。** Chakrabarty、Laban、Wu [11]（CHI 2025）请 18 位职业作家编辑 LLM 生成的段落，归纳出 7 类问题：陈词滥调（cliché）、不必要/重复的解释（unnecessary exposition，作家称为 "fluff"）、辞藻堆砌（purple prose）、句子结构差、缺少具体性和细节、用词和措辞别扭、时态不一致。据此建了 LAMP 语料库：1,057 段 LLM 文字及作家的细粒度修改。GPT-4o、Claude-3.5-Sonnet、Llama-3.1-70B 三家在写作质量上没有谁明显更好，说明这些是跨模型的共同问题。专家最喜欢别的专家改过的版本，但自动编辑方法也有一定效果。

**"Slop" 的维度。** Shaib 等人 [12] 访谈了 19 位 NLP、写作、新闻、哲学领域的专家，把 "slop" 拆成三组：信息效用（信息密度、相关性）、信息质量（事实性、偏见）、风格质量（重复、模板化、连贯性、流畅度、啰嗦、用词复杂度、语气）。他们在 150 篇新闻和 100 段问答上做片段级标注，发现"是不是 slop"的二元判断有一定主观性，但和连贯性、相关性等维度相关；现有自动指标和强推理模型都还不能可靠地找出 slop。注意：slop 和"是否 AI 写的"不是一回事，人写的东西也可能是 slop。

**语言学测量：名词化、信息密集。** Reinhart 等人 [13]（PNAS 2025）用 Biber 的 66 个词汇—语法特征比较人和 Llama 3、GPT-4o 的文字。指令微调模型偏爱现在分词从句、"that" 主语从句、名词化和短语并列，这是一种名词重、信息密的风格，即使被要求模仿口语也改不掉。例如 GPT-4o 的现在分词从句是人的 5.3 倍，名词化 2.1 倍，"that" 主语从句 2.6 倍。词汇上，GPT-4o 用 camaraderie、palpable、tapestry、intricate 的频率超过人类 100 倍，23% 的 GPT-4o 输出里出现了 "tapestry"。关键发现：**Llama 3 base 模型的特征频率接近人类，指令微调版本差得更远**，所以作者认为偏差来自指令微调，而不只是训练数据。

**大规模痕迹：学术写作。**
- Kobak 等人 [14] 借用"超额死亡"的思路，分析 2010–2024 年 1,510 万篇 PubMed 摘要，发现 delves（超额比 28.0）、underscores（13.8）、showcasing（10.7）等"风格词"突然增多；据此估计**至少 13.5%** 的 2024 年摘要经过 LLM 处理，部分子语料高达 40%。这个变化超过了新冠疫情对用词的影响。
- Liang 等人 [15] 分析 950,965 篇论文：计算机科学领域 LLM 修改内容比例增长最快，最高约 17.5%；数学和 Nature 系列最低（最高约 6.3%）。
- Liang 等人 [16] 估计 ICLR、NeurIPS 等 AI 会议同行评审中 6.5%–16.9% 的文字可能被 LLM 大幅修改；临近截止日期、评审者自评信心低的评审里比例更高；"commendable" 等形容词频率突然上升。
- Juzek 和 Ward [19] 找出 21 个"焦点词"（delve、intricate、underscore 等），没有发现模型架构、算法或训练数据是原因的证据，模型对比结果与 RLHF 起作用的说法一致。

**创意写作的差距。** Chakrabarty 等人 [17]（CHI 2024）设计了 14 项创意写作测试（TTCW），10 位作家评估 48 篇故事：LLM 故事通过的测试比职业作家少 3–10 倍，而且没有一个 LLM 评审和专家判断正相关。

**实践者清单。** 维基百科的 "Signs of AI writing" 页面 [18]（WikiProject AI Cleanup 维护）用真实条目举例，列出：夸大意义和影响（"stands as a testament""plays a pivotal role"）、句尾挂"-ing"分词短语做肤浅分析（"highlighting its importance"）、广告或旅游手册腔（"nestled""vibrant""rich cultural heritage"）、模糊归属（"experts argue"）、套路化的"挑战与展望"结尾、否定式排比（"not just X, but Y"）、三项并列、回避简单的 "is/has" 等。这份清单有三点值得注意：（1）它明确说这是"观察，不是规则"，并提醒不要只靠检测工具；（2）它专门列出"无效指标"：语法完美、"高级"或正式的用词、孤立的过渡词、"乏味"的文风都不可靠；（3）它把破折号过度使用标为"历史指标（2022–2026 年 9 月）"，因为新模型已被调成少用甚至不用破折号，结果标点种类反而变少了，这本身成了新的迹象。可见 AI 味的表面特征会随模型版本变化，深层特征（空泛、套路、缺少具体信息）更稳定。

**对写作者的启示**
- 先查"内容层"的问题，再查"词汇层"：有没有具体的人、数、地、事？有没有不必要的解释和总结？词换掉了，空泛还在，AI 味就还在 [11][12]。
- 留意自己的"名词化"和"-ing 尾巴"：把 "the implementation of" 改回动词，把句尾 "…, highlighting its significance" 删掉或改成具体结果 [13][18]。
- 不要把某个"AI 词表"当成标准答案：词表会过时，而且人也会用这些词 [3][18]。

---

## 三、AI 味是怎么来的？

**后训练压缩多样性。** Kirk 等人 [21]（ICLR 2024）比较 SFT、奖励模型、RLHF 各阶段：RLHF 的泛化能力更好，但和 SFT 相比明显降低输出多样性，二者之间存在取舍。Padmakumar 和 He [33] 发现，和反馈微调过的 InstructGPT 一起写作会降低多样性，和 base GPT-3 一起写则不会。Peeperkorn 等人 [24] 在 OLMo 系列上逐阶段测量，发现 DPO 对多样性影响最大。

**偏好数据本身偏爱"典型"。** Zhang 等人 [22]（Verbalized Sampling，arXiv 2025，ICML 2026）认为模式坍缩不只是算法问题，还有一个数据层面的原因：典型性偏差（typicality bias），也就是标注员根据认知心理学中早已知道的规律，系统地偏爱熟悉、流畅、可预测的文字。他们提出一个无需训练的提示方法：让模型"写 5 个回答并给出各自概率"，在创意写作中把多样性提高到直接提示的 1.6–2.1 倍，同时不损害安全性和事实准确性。

**把小说压平。** Li 等人 [23]（"Narrative Flattening"，arXiv 2026）用 OLMo-32B 的四个检查点（Base、SFT、DPO、RLVR）续写三类人类小说（StoryStar、TMAS、《纽约客》）。随着后训练推进，主题转换变得更均匀，高强度情绪让位于中性，故事之间的风格差异缩小；专业文学小说被压缩得最厉害；到 RLVR 阶段，不同来源之间的风格差异比人类水平下降 90% 以上。作者也强调这是"阶段性、几何上"的证据，不能说明是哪种数据或奖励造成的。

**奖励模型偏爱"讨好、注水、含糊"。** Sharma 等人 [26] 发现五个主流助手都有谄媚（sycophancy）倾向，人类偏好数据中和用户观点一致的回答更容易被选中。Bharadwaj 等人 [27]（ICLR 2026）检查长度、结构、术语、谄媚、含糊五种特征：偏好模型在超过 60% 的情况下偏爱被放大这些特征的回答，和人类偏好相比误校准约 40%。这些特征和人类标签只有弱负相关（r = −0.12），却和强奖励模型的标签正相关（r = +0.36）。Juzek 和 Ward [28] 用 Llama 模拟人类反馈学习（LHF）实验，发现参与者会系统地偏爱包含某些词的版本，把 "delve" 等词的过度使用和 LHF 联系起来。LAMP 论文也把冗余解释和华丽辞藻部分归因于偏好标注中的"啰嗦偏差"（verbosity bias）[11]。

**格式模板和解码。** Yun 等人 [25] 发现，指令模型的聊天模板（角色标记、特殊 token）本身就会造成"多样性坍缩"，提高温度也解决不了；去掉结构 token 的输出最多样。针对解码，[24] 提出用更"野"的 base 模型引导指令模型（conformative decoding）；Paech 等人 [30] 的 Antislop 在推理时回溯并屏蔽过度使用的字符串，并用 token 级偏好优化去掉这些模式。

**对写作者的启示**
- AI 的"默认答案"是平均答案。想要不同的东西，就要明确要求多个方案，或者让它给出不同概率的候选，再由你挑选 [22]。
- 模型天生偏向"讨好、全面、稳妥"。让它少总结、少夸奖、给出明确立场，往往比换同义词更有效 [26][27]。
- 小说和个人写作受影响最大：情绪起伏和意外转折正是后训练会削掉的东西，要靠人补回来 [23]。

---

## 四、同质化：大家越写越像

- **个人变好，群体变窄。** Doshi 和 Hauser [32]（Science Advances 2024）让 293 位写作者写短篇故事，由 600 人评分：能看到 5 个 AI 点子的写作者，作品新颖度提高 8.1%，有用性提高 9.0%，在创造力较低的写作者中提升更明显；但用 AI 写的故事彼此更相似。作者称之为"社会困境"：个人得益，集体损失。
- **跨模型也一样。** Wenger 和 Kenett [34] 用标准创造力测试比较人和多个 LLM：LLM 的回答彼此之间比人和人之间更相似，换模型也躲不开。Jiang 等人 [29]（"Artificial Hivemind"，NeurIPS 2025）用 2.6 万条真实开放式问题测试 70 多个模型，发现单个模型反复给出相似回答，而不同模型之间的趋同更严重。
- **语言多样性在缩小。** Sourati 等人 [31]（Nature Human Behaviour 2026）通过三项研究、七个数据集、超过 88 万篇文本发现：LLM 润色保留核心内容，但统一了风格，写作复杂度的方差显著下降 21–50%；同时放大"主流"特征、压低其他特征。作者认为，这会干扰人们从文字中读出作者身份和心理状态（研究检验了人格、政治倾向等推断）。
- **二语写作者的声音被抹掉。** Liu 和 Zhu [35]（arXiv 2026）用四个 LLM 润色中国 B2 水平大学生的议论文（ICNALE 语料）：语法错误被改正，命题意思保留，但所有模型都大幅删去与读者对话的"互动标记"，把协商式表达改成单向断言；在认知立场（如模糊限制语）上，有的模型删光，有的反而加入脱离语境的谨慎表达。作者的结论是：AI 把二语作者的修辞身份改写成了统一的英美范式。

**对写作者的启示**
- 用 AI 找点子没问题，但不要直接采用它的第一个点子；它的第一个点子很可能也是别人的第一个点子 [29][32]。
- 润色时只让 AI 改错，不要让它"重写得更好"；改完后对比原文，把被删掉的个人语气、犹豫和对读者说的话找回来 [31][35]。

---

## 五、读者怎么反应？

- **知道是 AI，就打折。** Raj、Berg、Seamans [36]（Journal of Experimental Psychology: General 2026）的 16 个实验共 27,491 人：只要参与者相信作品由 AI 写或有 AI 帮助，对创意写作的评价就下降，中介变量是感知到的真实感。这个"AI 披露惩罚"在不同指标、场景、文体中都存在，研究者试过的多种干预都没能可靠地减弱它。据密歇根大学新闻稿，平均降幅为 6.2% [46]。
- **社交和人际写作受影响最大。** Nakano 等人 [37]（IUI 2026，261 人、990 次评价）发现，披露 AI 参与会降低读者对作者的信任、关心、能力和好感；在社交和人际类写作中下降最明显，原因是"缺乏真诚""省力"和"场合不合适"。AI 素养较高的读者更宽容。
- **盲测时反而更喜欢 AI。** Porter 和 Machery [5]（Scientific Reports 2024）的参与者辨别 AI 诗和名诗人作品的准确率只有 46.6%，低于随机；AI 诗在节奏、美感等方面得分更高，因为更简单好懂；人们把"自己喜欢"误当成"这是人写的"。但一旦被告知是 AI 写的，评价就下降。Parshakov 等人 [38] 在问答中也发现：来源隐藏时人们偏爱 AI 回答，来源公开后这种偏好明显减弱。
- **专家和大众的口味不同。** Chakrabarty、Ginsburg、Dhillon [39]（arXiv 2025）让模型模仿 50 位获奖作家的风格：仅靠提示时，28 位 MFA 背景读者明显不喜欢 AI 文本（质量 OR = 0.13），516 位普通读者却更偏爱 AI（OR = 1.82）；用作者全集微调后，两类读者都更偏爱 AI，而且检测器只把 3% 的微调输出标为 AI（提示输出为 97%）。中介分析显示，微调消除了会被扣分的"AI 怪癖"。

**对写作者的启示**
- 在意真实感的场合（个人故事、致谢、道歉、社交信息），AI 痕迹的代价最高，最好自己写 [36][37]。
- "读起来顺"不等于"读者认为好"：内行读者恰恰会因为 AI 特有的套路给你扣分 [3][39]。

---

## 六、机器检测（简述）

- **零样本方法：** DetectGPT [40] 利用"模型生成的文字往往位于对数概率函数的负曲率区域"这一性质，不需要训练分类器；Binoculars [41] 对比两个相近模型的分数，在 0.01% 误报率下能检出 90% 以上的 ChatGPT 文字。
- **水印：** SynthID-Text [42]（Nature 2024）用 Tournament 采样嵌入水印，在近 2,000 万条 Gemini 回答的线上实验中没有发现质量下降。缺点是只对加了水印的模型有效。
- **脆弱：** 改写模型 DIPPER 让 DetectGPT 的检出率（1% 误报率下）从 70.3% 降到 4.6% [44]；RAID 基准（600 万条以上生成文本、11 种攻击）显示检测器很容易被攻击、采样策略变化和没见过的模型骗过 [45]。在 [3] 中，"人性化"处理后的 o1-Pro 文章让多个开源检测器几乎失效。
- **不公平：** Liang 等人 [43] 测试了 7 个检测器，它们把 91 篇托福作文中超过一半误判为 AI，平均误报率 61.3%，原因是非母语写作的困惑度（perplexity）较低；而美国八年级学生作文基本被判对。

**对写作者的启示**
- 不要用"能不能骗过检测器"衡量去 AI 味的效果。检测器分数低，读者可能依然觉得有 AI 味，反过来也一样 [3][44]。
- 简单、规范的写法容易被检测器误判。如果你是非母语写作者，要保留草稿和修改记录作为证据 [43]。

---

## 七、总结：研究之间的共识与空白

共识：（1）AI 味不是某几个词，而是一组从词汇、句法到内容和结构的稳定偏好；（2）这些偏好主要由后训练和偏好数据放大；（3）它会通过人机合写扩散到人类语言，造成同质化；（4）有经验的人能认出来，读者知道后会打折。

空白：大多数研究只针对英语，而且集中在 GPT-4o 这一代模型；2026 年的新模型已经开始主动压制表面特征（比如破折号），表面线索正在失效 [18]。中文语境下的系统研究，留给下一章讨论。

---

## 参考文献

[1] Clark, E., August, T., Serrano, S., Haduong, N., Gururangan, S., & Smith, N. A. (2021). All That's 'Human' Is Not Gold: Evaluating Human Evaluation of Generated Text. *ACL 2021*. https://doi.org/10.18653/v1/2021.acl-long.565

[2] Jakesch, M., Hancock, J. T., & Naaman, M. (2023). Human heuristics for AI-generated language are flawed. *PNAS*, 120. https://doi.org/10.1073/pnas.2208839120

[3] Russell, J., Karpinska, M., & Iyyer, M. (2025). People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text. *ACL 2025* (Long Papers), pp. 5342–5373. https://doi.org/10.18653/v1/2025.acl-long.267 （arXiv:2501.15654）

[4] Zaitsu, W., Jin, M., Ishihara, S., Tsuge, S., & Inaba, M. (2025). Stylometry can reveal artificial intelligence authorship, but humans struggle: A comparison of human and seven large language models in Japanese. *PLOS One*, 20(10), e0335369. https://doi.org/10.1371/journal.pone.0335369

[5] Porter, B., & Machery, E. (2024). AI-generated poetry is indistinguishable from human-written poetry and is rated more favorably. *Scientific Reports*. https://doi.org/10.1038/s41598-024-76900-1

[6] Fiedler, A., & Döpke, J. (2025). Do humans identify AI-generated text better than machines? Evidence based on excerpts from German theses. *International Review of Economics Education*, 49, 100321. https://doi.org/10.1016/j.iree.2025.100321

[7] Milička, J., Marklová, A., Drobil, O., & Pospíšilová, E. (2025). Learning to detect AI texts and learning the limits. *PLOS One*. https://doi.org/10.1371/journal.pone.0333007 （预印本标题：Humans can learn to detect AI-generated texts, or at least learn when they can't，arXiv:2505.01877）

[8] Wang, Y., Xing, R., et al. (2025). Is Human-Like Text Liked by Humans? Multilingual Human Detection and Preference Against AI. arXiv:2502.11614. https://arxiv.org/abs/2502.11614

[9] Manhede, T., Fartachuk, Y., Martinez, S. A., Langer, A., & Chein, J. M. (2026). Human discernment of artificial intelligence in online markets can be shaped by experience and training. *AI & Society*. https://doi.org/10.1007/s00146-026-03373-3

[10] Loth, A., & Kappes, M. (2026). Can Humans Tell? A Dual-Axis Study of Human Perception of LLM-Generated News. *WebSci Companion '26*. https://doi.org/10.1145/3795513.3807431 （arXiv:2604.03755）

[11] Chakrabarty, T., Laban, P., & Wu, C.-S. (2025). Can AI writing be salvaged? Mitigating Idiosyncrasies and Improving Human-AI Alignment in the Writing Process through Edits. *CHI 2025*. https://doi.org/10.1145/3706598.3713559 （arXiv:2409.14509）

[12] Shaib, C., Chakrabarty, T., Garcia-Olano, D., & Wallace, B. C. (2025). Measuring AI "Slop" in Text. arXiv:2509.19163. https://arxiv.org/abs/2509.19163

[13] Reinhart, A., Markey, B., Laudenbach, M., Pantusen, K., Yurko, R., Weinberg, G., & Brown, D. W. (2025). Do LLMs write like humans? Variation in grammatical and rhetorical styles. *PNAS*, 122. https://doi.org/10.1073/pnas.2422455122

[14] Kobak, D., González-Márquez, R., Horvát, E.-Á., & Lause, J. (2025). Delving into LLM-assisted writing in biomedical publications through excess vocabulary. *Science Advances*. https://doi.org/10.1126/sciadv.adt3813

[15] Liang, W., Zhang, Y., Wu, Z., Lepp, H., et al. (2024). Mapping the Increasing Use of LLMs in Scientific Papers. *COLM 2024*. https://arxiv.org/abs/2404.01268

[16] Liang, W., Izzo, Z., Zhang, Y., Lepp, H., et al. (2024). Monitoring AI-Modified Content at Scale: A Case Study on the Impact of ChatGPT on AI Conference Peer Reviews. *ICML 2024*, PMLR 235. https://proceedings.mlr.press/v235/liang24b.html

[17] Chakrabarty, T., Laban, P., Agarwal, D., Muresan, S., & Wu, C.-S. (2024). Art or Artifice? Large Language Models and the False Promise of Creativity. *CHI 2024*. https://doi.org/10.1145/3613904.3642731

[18] Wikipedia contributors (WikiProject AI Cleanup). Wikipedia:Signs of AI writing. 2026-10-18 访问. https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing

[19] Juzek, T. S., & Ward, Z. B. (2025). Why Does ChatGPT "Delve" So Much? Exploring the Sources of Lexical Overrepresentation in Large Language Models. *COLING 2025*. https://aclanthology.org/2025.coling-main.426/

[20] Yakura, H., Lopez-Lopez, E., Brinkmann, L., Serna, I., et al. (2024/2026). Empirical evidence of Large Language Model's influence on human spoken communication. arXiv:2409.01754（v4）. https://arxiv.org/abs/2409.01754

[21] Kirk, R., Mediratta, I., Nalmpantis, C., Luketina, J., Hambro, E., Grefenstette, E., & Raileanu, R. (2024). Understanding the Effects of RLHF on LLM Generalisation and Diversity. *ICLR 2024*. https://arxiv.org/abs/2310.06452

[22] Zhang, J., Yu, S., Chong, D., Sicilia, A., Tomz, M. R., Manning, C. D., & Shi, W. (2025). Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity. arXiv:2510.01171；*ICML 2026*, PMLR 306. https://proceedings.mlr.press/v306/zhang26hy.html

[23] Li, Z., Zhu, Y., Wu, S., Bao, H., & Evans, J. A. (2026). Narrative Flattening: How Post-Training Compresses Thematic, Affective, and Stylistic Variation in LLM Fiction. arXiv:2605.27878. https://arxiv.org/abs/2605.27878

[24] Peeperkorn, M., Kouwenhoven, T., Brown, D., & Jordanous, A. (2025). Mind the Gap: Conformative Decoding to Improve Output Diversity of Instruction-Tuned Large Language Models. arXiv:2507.20956. https://doi.org/10.48550/arXiv.2507.20956

[25] Yun, L., An, C., Wang, Z., Peng, L., & Shang, J. (2025). The Price of Format: Diversity Collapse in LLMs. arXiv:2505.18949. https://doi.org/10.48550/arXiv.2505.18949

[26] Sharma, M., Tong, M., Korbak, T., et al. (2024). Towards Understanding Sycophancy in Language Models. *ICLR 2024*. https://arxiv.org/abs/2310.13548

[27] Bharadwaj, A., Malaviya, C., Joshi, N., & Yatskar, M. (2026). Flattery, Fluff, and Fog: Diagnosing and Mitigating Idiosyncratic Biases in Preference Models. *ICLR 2026*. https://arxiv.org/abs/2506.05339

[28] Juzek, T. S., & Ward, Z. B. (2025). Word Overuse and Alignment in Large Language Models: The Influence of Learning from Human Feedback. arXiv:2508.01930. https://arxiv.org/abs/2508.01930

[29] Jiang, L., Chai, Y., Li, M., Liu, M., Fok, R., Dziri, N., Tsvetkov, Y., Sap, M., Albalak, A., & Choi, Y. (2025). Artificial Hivemind: The Open-Ended Homogeneity of Language Models (and Beyond). *NeurIPS 2025*. https://arxiv.org/abs/2510.22954

[30] Paech, S. J., Roush, A. G., Goldfeder, J., & Shwartz-Ziv, R. (2025). Antislop: A Comprehensive Framework for Identifying and Eliminating Repetitive Patterns in Language Models. arXiv:2510.15061. https://arxiv.org/abs/2510.15061

[31] Sourati, Z., Karimi-Malekabadi, F., Ozcan, M., McDaniel, C., Ziabari, A., Trager, J., Tak, A. N., Chen, M., Morstatter, F., & Dehghani, M. (2026). The shrinking landscape of linguistic diversity in the age of large language models. *Nature Human Behaviour*. https://doi.org/10.1038/s41562-026-02550-0 （arXiv:2502.11266）

[32] Doshi, A. R., & Hauser, O. P. (2024). Generative AI enhances individual creativity but reduces the collective diversity of novel content. *Science Advances*, 10(28), eadn5290. https://doi.org/10.1126/sciadv.adn5290

[33] Padmakumar, V., & He, H. (2024). Does Writing with Language Models Reduce Content Diversity? *ICLR 2024*. https://arxiv.org/abs/2309.05196

[34] Wenger, E., & Kenett, Y. (2025). We're Different, We're the Same: Creative Homogeneity Across LLMs. arXiv:2501.19361. https://arxiv.org/abs/2501.19361

[35] Liu, A., & Zhu, S. (2026). The Cost of Perfect English: Pragmatic Flattening and the Erasure of Authorial Voice in L2 Writing Supported by GenAI. arXiv:2605.13055. https://arxiv.org/abs/2605.13055

[36] Raj, M., Berg, J. M., & Seamans, R. (2026). The artificial intelligence disclosure penalty: Humans persistently devalue AI-generated creative writing. *Journal of Experimental Psychology: General*. https://doi.org/10.1037/xge0001889 （只读到摘要）

[37] Nakano, H., Takezawa, J., Matulic, F., Yang, C.-L., & Yatani, K. (2026). Understanding Reader Perception Shifts upon Disclosure of AI Authorship. *IUI 2026*. https://doi.org/10.1145/3742413.3789076 （只读到摘要）

[38] Parshakov, P., Naidenova, I., Paklina, S., Matkin, N., & Nesseler, C. (2025). Users Favor LLM-Generated Content -- Until They Know It's AI. arXiv:2503.16458. https://arxiv.org/abs/2503.16458

[39] Chakrabarty, T., Ginsburg, J. C., & Dhillon, P. (2025). Readers Prefer Outputs of AI Trained on Copyrighted Books over Expert Human Writers. arXiv:2510.13939. https://arxiv.org/abs/2510.13939

[40] Mitchell, E., Lee, Y., Khazatsky, A., Manning, C. D., & Finn, C. (2023). DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature. *ICML 2023*, PMLR 202. https://proceedings.mlr.press/v202/mitchell23a.html

[41] Hans, A., Schwarzschild, A., Cherepanova, V., Kazemi, H., Saha, A., Goldblum, M., Geiping, J., & Goldstein, T. (2024). Spotting LLMs With Binoculars: Zero-Shot Detection of Machine-Generated Text. *ICML 2024*, PMLR 235. https://arxiv.org/abs/2401.12070

[42] Dathathri, S., See, A., Ghaisas, S., Huang, P.-S., McAdam, R., et al. (2024). Scalable watermarking for identifying large language model outputs. *Nature*. https://doi.org/10.1038/s41586-024-08025-4

[43] Liang, W., Yuksekgonul, M., Mao, Y., Wu, E., & Zou, J. (2023). GPT detectors are biased against non-native English writers. *Patterns*. https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961/

[44] Krishna, K., Song, Y., Karpinska, M., Wieting, J., & Iyyer, M. (2023). Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense. *NeurIPS 2023*. https://arxiv.org/abs/2303.13408

[45] Dugan, L., Hwang, A., Trhlik, F., Ludan, J. M., Zhu, A., Xu, H., Ippolito, D., & Callison-Burch, C. (2024). RAID: A Shared Benchmark for Robust Evaluation of Machine-Generated Text Detectors. *ACL 2024*. https://arxiv.org/abs/2405.07940

[46] Karoub, J. (2026-01-26). Lit bots beware: Readers less favorable toward AI-generated creative writing, U-M research finds. *University of Michigan News*（新闻稿，用来补充 [36] 的 16 个实验和 6.2% 两个数字）. https://news.umich.edu/lit-bots-beware-readers-less-favorable-toward-ai-generated-creative-writing-u-m-research-finds/

---

### 附：对任务清单中数字的核对

| 原清单中的说法 | 核对结果 |
|---|---|
| Russell 等：5 位专家，多数投票 300 篇错 1 篇 | 正确。补充：专家平均 TPR 92.7%；唯一的错误出现在 o1-Pro 实验中 [3] |
| Reinhart 等：现在分词从句 2–5 倍，名词化 1.5–2 倍 | **正文没找到这两个区间。** 正文只给出 GPT-4o 的数字：现在分词从句 5.3 倍，名词化 2.1 倍（"that" 主语从句 2.6 倍）。区间可能是从各模型的图里读出来的，未核对，本章只用正文数字 [13] |
| Kobak 等：2024 年 PubMed 摘要 ≥13.5% | 正确（是下限；部分子语料达 40%）[14] |
| Sourati 等：88 万篇文本，复杂度方差 −21–50% | 正确。正式版是"三项研究、七个数据集"；arXiv v1 写的是"四项研究" [31] |
| AI 披露惩罚：N = 27,491，中介为真实感 | 正确。作者是 Raj、Berg、Seamans；共 16 个实验，平均降幅 6.2% 来自新闻稿 [36][46] |
| Verbalized Sampling 2025 | 2025 年 arXiv，已在 ICML 2026 发表 [22] |
| Narrative Flattening arXiv 2605.27878；L2 arXiv 2605.13055 | 编号正确；后者标题为 "The Cost of Perfect English…" [23][35] |
