# 大脑库 · 学习科学依据与改版建议(2026-09-24)

> 先说结论:页面现在「输入」很强(旁白、术语、原句、原文),「提取」偏弱。研究里最一致的结论是:**学会 = 反复从脑子里把东西取出来,并且隔开时间取**;划线、重读、看全文几乎不产生长期记忆。改版方向:每页前后都加「先想 → 再看 → 合上 → 自己说」这个回路,复习系统从「重看页面」改成「答题 + 自评 + 调间隔」。

## A. 证据强的学习原理(强度:高 / 中 / 低 = Dunlosky 等 2013 的效用评级,或元分析结论)

| 原理 | 是什么 | 证据 | 页面/站点怎么用 |
|---|---|---|---|
| 提取练习 retrieval practice | 不看材料,自己回忆 | **高**。Roediger & Karpicke 2006;Karpicke & Blunt 2011 发现提取练习胜过画概念图;Rowland 2014 元分析 g≈0.50;Adesope 2017 | 第 8 节自测改为**自由回忆**(先写答案再展开);每节标题下加「合上想一想」;第 2 节一句话核心默认遮住 |
| 间隔重复 spaced repetition | 把复习分散开 | **高**。Ebbinghaus 1885 遗忘曲线;Cepeda 2008:最佳间隔约为目标保持期的 10–20%;Leitner 盒、SM-2、FSRS(按每题的难度/稳定性/可提取性动态排期,Anki 23.10 起内置) | 现行 1/3/7/14/30 固定表可以用,但要**按每道题**排期,不按每页;答错回到 1 天,答对按自评拉长;有余力换 ts-fsrs |
| 交错 interleaving | 不同主题混着练 | **中**。Rohrer & Taylor 2007;Kornell & Bjork 2008 | 「今日复习」跨学科、跨页面混抽,不按页连续出题 |
| 精细追问 elaborative interrogation | 问「为什么是真的?」 | **中** | 第 6 节「追问与反例」保留,改成先自己答,再显示参考 |
| 自我解释 self-explanation | 用自己的话解释每一步 | **中**。Chi 等 1994 | 第 9 节「我的输出」给固定提示:讲给 12 岁孩子听 + 举一个自己生活里的例子 |
| 生成效应 generation effect | 自己生成的比读到的记得牢 | **高**(实验室)。Slamecka & Graf 1978;Bertsch 等 2007 元分析 | 术语卡、原句卡做**填空/遮词**;生词本先看中文猜英文 |
| 双重编码 dual coding | 文字 + 图像两条通道 | **中**。Paivio 1986;Mayer 多媒体原则 | 第 3 节论证脉络可配一张简图(因果链/流程),**只放和内容直接相关的图** |
| 合意困难 desirable difficulties | 当下更费力,长期更好 | **高**(理论框架)。Bjork & Bjork 2011 | 所有「显示答案」都要先点一下,不自动展开;做题觉得难是正常的 |
| 费曼法 Feynman technique | 用简单的话讲清楚,找出卡壳的地方 | **低**(没有直接实验,是自我解释 + 生成的组合) | 第 2 节保留,但要求**先写我自己的版本**,再对照页面版本 |
| 具体例子 concrete examples | 抽象原则配多个例子 | **中**。Rawson 等 2015 | 每个关键概念至少配 2 个不同领域的例子(帮助迁移) |
| 划线 / 重读 / 摘要 | — | **低**(Dunlosky 2013 明确评为低效用;摘要要训练过才有用) | 保留工具,但降级(见 D) |
| 卡片盒 Zettelkasten | 一张卡一个想法,用自己的话写,互相链接 | 以实践经验为主(Ahrens 2017),机理和生成/精细化一致 | 第 7 节每条链接都写**「为什么连」一句话**,不要只列标题 |
| 迁移 transfer | 学到的东西能用到新情境 | 提取练习能促进迁移,近迁移强、远迁移弱(Pan & Rickard 2018) | 每页自测至少 1 道「应用题」:换个情境来问 |

## B. 阅读与笔记设计

- **康奈尔笔记 Cornell**:右栏记笔记、左栏写提问、底部写摘要。对应做法:每节末加一个「线索问题」(cue),复习时只看问题、回忆内容。
- **渐进式总结 progressive summarization**(Forte 2017):分层加粗 → 高亮 → 执行摘要,核心是「为未来的自己做能快速重读的笔记」。这正好适合「像翻自己大脑一样找东西」的目标,但它本身是整理,不是学习,**要配提取练习**。
- **SQ3R**(Survey–Question–Read–Recite–Review):真正起作用的是 Question(读前提问)和 Recite(读后复述)。对应「读前先提问」+「读后合上复述」。
- **自己的话 vs 逐字照抄**:逐字抄录是浅加工。Mueller & Oppenheimer 2014 发现逐字记录不利于概念理解,但 Urry 等 2021 大样本复制没能重现手写优势,所以结论要保守地说成「转述优于照抄」。
- **为什么全文转录本身不产生学习**:读得顺会让人误以为「我懂了」(流畅错觉 fluency illusion,Bjork);没有提取就没有巩固。原文的价值在于**核对和检索**,阅读原文本身不算学习动作。
- **原文和主动加工怎么结合**:先读笔记和问题 → 自己答 → 再用原文核对答错的地方。第 10 节原文放最后、默认折叠,这个做法是对的。

## C. 学习型网页设计

- **可读性**:正文行长英文约 50–75 字符,中文约 25–40 字(Dyson 2004 屏幕阅读研究);正文 16–18px,行高 1.6–1.8(中文可以到 1.8);对比度至少 4.5:1(WCAG 2.2)。
- **认知负荷 cognitive load**(Sweller 1988):内在负荷(内容本身的难度)减不掉,外在负荷(界面干扰)要尽量减,把脑力留给相关负荷(理解和建构)。所以工具栏平时收起,颜色标记最多 3 种含义。
- **Mayer 原则**:连贯 coherence(去掉装饰性内容)、信号 signalling(用标题、加粗、小结指路)、分段 segmenting(一屏一个意思,节可折叠)、冗余 redundancy(**朗读时不要同时逐字高亮大段相同文字**;非母语学习者可以放宽)、预训练 pre-training(术语放在前面)。
- **双语呈现**:字幕和双语文本对二语词汇学习有明显帮助(Montero Perez 等 2013 元分析),但如果中文一直显示,人就只看中文了。建议**英文在上、中文默认隐藏,点一下或长按才显示**(先试英文);原句段用平行对照,长原文用逐句交错。
- **进度提示**:侧栏标出已读的节和自测完成度;不要做分数、连续打卡这类有压力的游戏化(外在激励的证据弱)。
- **深色模式 / 移动端**:两套配色的对比度都要达标;移动端单栏,按钮至少 44px,划线和笔记用长按菜单。

## D. 具体改版建议

### 必须做(Must)
1. **页首加「读前先想」**:给 2–3 个问题,先写下自己的猜测(预测试 pretesting,Richland 等 2009;Pan & Carpenter 2023)。就算猜错,后面也记得更牢。
2. **第 8 节自测改成自由回忆 + 自评**:先在文本框写答案 → 点「看答案」→ 自评「忘了 / 模糊 / 记得 / 轻松」。**不用选择题**(认出来 recognition 不等于想起来 recall)。
3. **复习按题排期**:每道题单独记录,答错回到 1 天,按自评拉长间隔(1/3/7/14/30 可以继续用,也可以换 ts-fsrs)。「今日复习」混抽各学科(交错)。
4. **生词本改成主动回忆**:卡片先显示中文或挖空的原句,自己说出英文再翻面,同样按间隔表复习。
5. **第 2 节一句话核心默认遮住**,旁边放「先写你的一句话」输入框,写完再对照。
6. **每节末加 1 个线索问题**(相当于康奈尔笔记左栏)。复习模式下只显示这些问题,本身就是一份「翻大脑」目录。

### 应该做(Should)
7. **划线时附上「为什么」**:划线时弹出一行备注「为什么重要 / 和什么有关」;没写备注的划线不进复习。划线默认只用 1 种颜色。
8. **第 7 节知识连线**每条写一句「为什么连」,并支持反向链接(被哪些页引用)。
9. **第 9 节我的输出**给固定三问:用我自己的话怎么说?我生活里有什么例子?它哪里可能不对、什么时候不适用?
10. **第 5 节原句**:中文默认隐藏,先读英文;加一个「遮词填空」模式。
11. 每页自测至少 1 道应用/迁移题。

### 可以做(Could)
12. 第 3 节配一张因果简图(双重编码)。
13. 每周自动生成「本周回顾」:随机 10 题 + 本周「我的输出」汇总。
14. 显示遗忘提示,例如「上次复习是 N 天前,估计还记得 x%」。

### 去掉或降级
- **第 10 节全文原文**:保留,但默认折叠、放最后,定位成「核对用」;不要把「读完全文」当成学完了。
- **重读 / 划线**:不再当作主要的学习动作。首页不要推「继续阅读」,改推「今日复习」。
- **朗读**:只当辅助;朗读时不要整段逐字高亮(冗余)。
- 精简各节里装饰性的配色和提示语(连贯原则)。

## E. 可以做成库页的阅读清单

1. Dunlosky 等 2013《Improving Students' Learning With Effective Learning Techniques》https://journals.sagepub.com/doi/10.1177/1529100612453266 (PDF:https://www.whz.de/fileadmin/lehre/hochschuldidaktik/docs/dunloskiimprovingstudentlearning.pdf)
2. Brown, Roediger & McDaniel 2014《Make It Stick》(书)https://www.hup.harvard.edu/books/9780674729018
3. Bjork & Bjork 2011《Making things hard on yourself, but in a good way》https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/04/EBjork_RBjork_2011.pdf
4. Roediger & Karpicke 2006 测试效应 https://doi.org/10.1111/j.1467-9280.2006.01693.x
5. Cepeda 等 2008 间隔效应的「时间脊线」 https://laplab.ucsd.edu/articles/Cepeda%20et%20al%202008_psychsci.pdf
6. Ahrens 2017《How to Take Smart Notes》https://www.soenkeahrens.de/en/takesmartnotes
7. The Learning Scientists 六大学习策略(免费海报与讲解)https://www.learningscientists.org/downloadable-materials
8. TED-Ed《How to practice effectively... for just about anything》(库里已有,可当样板)https://ed.ted.com/lessons/how-to-practice-effectively-for-just-about-anything-annie-bosler-and-don-greene

## 参考文献

- Adesope, Trevisan & Sundararajan 2017. Rethinking the use of tests. *Review of Educational Research*. https://doi.org/10.3102/0034654316689306
- Ahrens 2017. *How to Take Smart Notes*. https://www.soenkeahrens.de/en/takesmartnotes
- Bertsch et al. 2007. The generation effect: a meta-analytic review. *Memory & Cognition*. https://doi.org/10.3758/BF03193441
- Bjork & Bjork 2011. 见 E3。
- Cepeda, Vul, Rohrer, Wixted & Pashler 2008. *Psychological Science* 19(11). https://escholarship.org/uc/item/0kp5q19x
- Chi et al. 1994. Eliciting self-explanations improves understanding. *Cognitive Science*. https://doi.org/10.1207/s15516709cog1803_3
- Dunlosky et al. 2013. 见 E1。
- Dyson 2004. How physical text layout affects reading from screen. *Behaviour & Information Technology*. https://doi.org/10.1080/01449290410001715714
- Ebbinghaus 1885/1913. *Memory*. https://psychclassics.yorku.ca/Ebbinghaus/index.htm
- Forte 2017. Progressive Summarization. https://fortelabs.com/blog/progressive-summarization-a-practical-technique-for-designing-discoverable-notes/
- FSRS 算法说明 https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-Algorithm ;TypeScript 实现 https://open-spaced-repetition.github.io/ts-fsrs/
- Karpicke & Blunt 2011. *Science* 331. https://doi.org/10.1126/science.1199327
- Kornell & Bjork 2008. Learning concepts and categories: is spacing the "enemy of induction"? *Psychological Science*. https://doi.org/10.1111/j.1467-9280.2008.02127.x
- Mayer 2021. *Multimedia Learning* (3rd ed.). Cambridge UP. https://doi.org/10.1017/9781316941355
- Montero Perez, Van Den Noortgate & Desmet 2013. Captioned video for L2 listening and vocabulary learning: a meta-analysis. *System*. https://doi.org/10.1016/j.system.2013.07.013
- Mueller & Oppenheimer 2014. *Psychological Science*. https://doi.org/10.1177/0956797614524581 ;复制研究 Urry et al. 2021 https://doi.org/10.1177/0956797620965541
- Paivio 1986. *Mental Representations: A Dual Coding Approach*. Oxford UP.
- Pan & Rickard 2018. Transfer of test-enhanced learning. *Psychological Bulletin*. https://doi.org/10.1037/bul0000151
- Rawson, Thomas & Jacoby 2015. The power of examples. *Educational Psychology Review*. https://doi.org/10.1007/s10648-014-9273-3
- Richland, Kornell & Kao 2009. The pretesting effect. *Journal of Experimental Psychology: Applied*. https://doi.org/10.1037/a0016496
- Roediger & Karpicke 2006. 见 E4。
- Rohrer & Taylor 2007. The shuffling of mathematics problems improves learning. *Instructional Science*. https://doi.org/10.1007/s11251-007-9015-8
- Rowland 2014. The effect of testing versus restudy on retention: a meta-analytic review. *Psychological Bulletin*. https://doi.org/10.1037/a0037559
- Slamecka & Graf 1978. The generation effect. *JEP: Human Learning and Memory*. https://doi.org/10.1037/0278-7393.4.6.592
- Sweller 1988. Cognitive load during problem solving. *Cognitive Science*. https://doi.org/10.1207/s15516709cog1202_4
- WCAG 2.2 对比度 https://www.w3.org/TR/WCAG22/#contrast-minimum
