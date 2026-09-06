# -*- coding: utf-8 -*-
def D(speaker, en, zh):
    return f'<span class="sent"><span class="se"><b>{speaker}:</b> {en}</span><span class="sz"><b>{speaker}:</b> {zh}</span></span>'
def DIALOG(*turns): return '<div class="para dialog"><p class="en">'+' '.join(turns)+' </p></div>\n'
def S(en,zh): return f'<span class="sent"><span class="se">{en}</span><span class="sz">{zh}</span></span>'
def Q(tag,*ps): return f'<div class="quote"><span class="tag ui">{tag}</span>\n<p class="en">'+' '.join(S(e,z) for e,z in ps)+' </p></div>\n'
def KP(*points): return '  <div class="keypoints ui"><b>要点</b><ul>\n'+''.join(f'    <li>{p}</li>\n' for p in points)+'  </ul>\n  </div>\n'
def EX(*points): return '  <div class="explain ui"><b>💡 这节在教什么</b><ul>\n'+''.join(f'    <li>{p}</li>\n' for p in points)+'  </ul>\n  </div>\n'
def sec(num,sid,title,time,kp,ex,body):
    return (f'<!-- {sid.upper()} -->\n<section id="{sid}">\n'
            f'  <div class="sec-head"><span class="sec-num">{num}</span><h2>{title}</h2></div>\n'
            f'  <div class="sec-time ui">{time}</div>\n{KP(*kp)}{EX(*ex)}{body}</section>\n\n')
SEC=[]

# S6 推理练习A/B（逐句）
SEC.append(sec('06','s6','推理练习(1) · 干燥的鼻子、磨损的袖口','13:30 – 22:00',
 ['<b>核心练习:给一个"可观察的小细节",推断背后发生了什么。</b>Alex 强调:没有唯一正确答案,重在"像侦探一样思考"',
  '例A · 鼻子周围皮肤干燥:Kaelyn 先想到"化学灼伤→用化学品杀人",被 Alex 温和拨回;Alice 想到"去了炎热的地方";Alex 引导成"匆忙出门忘了防晒→为什么匆忙"一层层往下挖',
  '例B · 体面西装白衬衫但袖口磨损(frayed cuffs):Alice 推"二手/thrifted";Kaelyn 推"要见重要的人却没钱做西装" → 学到 thrifted(二手购入)、thrifty(节俭)'],
 ['这节把抽象的"推理"变成可操作的写作练习:<b>一个细节 → 一段背景故事</b>,正是塑造人物、埋伏笔的起手式。',
  '<b>两条重要纪律:①别过度戏剧化</b>(Kaelyn 的"化学品杀人"被拨回)——小细节可以只指向简单日常的背景,那才可信;<b>②juxtaposition(并置)</b>——体面西装配磨损袖口,两个矛盾细节一并置,不用解释就生出"这人有故事"的悬念。'],
 DIALOG(
   D('Alex',"Person A has dry skin around their nose. What do you deduce has recently happened to them? There's no right or wrong — it's about thinking. Any guesses?",
     "A 号人物鼻子周围皮肤干燥。你推断他最近发生了什么?没有对错——重点在思考。有想法吗?"),
   D('Kaelyn',"Maybe it could be a chemical burn, if the dryness is really severe.",
     "也许是化学灼伤,如果干燥非常严重的话。"),
   D('Alex',"It could be, but what would that suggest? What could we deduce from that?",
     "有可能,但那说明什么?我们能从中推出什么?"),
   D('Kaelyn',"Maybe she used chemicals to kill someone. I don't know.",
     "也许她用化学品杀了人。我也不知道。"),
   D('Alex',"Good try, but we don't always have to go to the most violent or horrible description. Alice, what else might dry skin around the nose indicate? Don't overthink it.",
     "不错的尝试,但我们不必总往最暴力、最可怕的方向想。Alice,鼻子周围皮肤干燥还可能说明什么?别想太多。"),
   D('Alice',"She went to a very hot area.",
     "她去了一个很炎热的地方。"),
   D('Alex',"Good. He went somewhere hot, forgot his moisturiser or sun cream — which means, perhaps, he left in a hurry. Why did he leave in a hurry? We're starting to pull out those links, like unravelling a ball of string.",
     "很好。他去了炎热的地方,忘了保湿霜或防晒霜——这也许意味着,他匆忙出门。他为什么匆忙?我们开始一点点扯出这些联系,像解开一团线。"))
 +DIALOG(
   D('Alex',"Person B wears a smart suit and white shirt, but the cuffs are frayed. What does that tell you? First — what are frayed cuffs, Kaelyn?",
     "B 号人物穿着体面的西装和白衬衫,但袖口磨损了(frayed)。这说明什么?先说——什么是磨损的袖口,Kaelyn?"),
   D('Kaelyn',"It's when the fabric gets stringy, like it starts to come apart.",
     "就是布料变得起毛、开始一点点散开。"),
   D('Alex',"Right. So why the smart suit but frayed cuffs? What's the backstory?",
     "对。那为什么西装体面、袖口却磨损?背后有什么故事?"),
   D('Alice',"The clothing was really old — the person thrifted it.",
     "衣服其实很旧——这人是二手买来的(thrifted)。"),
   D('Kaelyn',"I was thinking person B is meeting someone important, but doesn't have the money for a tailored suit, yet somehow got a new suit to wear, and no one knows how.",
     "我在想,B 要见一个重要的人,但没钱做定制西装,却不知怎么弄到一套新的穿上,没人知道怎么来的。"),
   D('Alex',"I like all of that. \"No one knows how\" — that's the bit we'd scratch at a little more. Maybe they found it, borrowed it, begged, borrowed, stole — who knows?",
     "这些我都喜欢。'没人知道怎么来的'——这一点正是我们可以再深挖的地方。也许是捡的、借的、求来的、偷来的——谁知道呢?"))
 +Q('Alex · 并置制造悬念',
   ("We call it a juxtaposition when we put these two things next to each other: on the one hand, really smart clothing; on the other, the clothes are old and frayed. Why is that?",
    "把这两样东西并排放在一起,我们叫它'并置':一方面是体面的衣着,另一方面衣服又旧又磨损。这是为什么呢?"))
))

# S7 推理练习C/D/E/F（谎言、alibi、反向心理）逐句
SEC.append(sec('07','s7','推理练习(2) · 谎言、不在场证明与"反向心理"','36:00 – 46:00',
 ['例D · 有人被审问时完全不看你的眼睛:Kaelyn 说"完全不对视是撒谎的强信号";<b>xuanying 提出惊艳的"反向心理":有人说真话时故意不对视,好让"不对视=撒谎"这个预期反过来替自己脱罪</b>',
  '例E · 有人"三次、精确到9点整"告诉你昨晚在做什么,信吗?——引出关键术语 <b>alibi(不在场证明)</b>。Kaelyn:"说三次、还精确到9点,太刻意了,像在造 alibi";Yuhan:"改口的 alibi 很 sus(可疑)"',
  'xuanying 补充判断法则:<b>大事件才会记得精确,小细节记得太清反而可疑</b>;Alice 补充:"重复时前后对不上、忘词,就可疑"',
  '例F · 自称"6岁起在英国上学"却没听过小熊维尼:Alex 点明重点不是维尼,而是<b>"大文化参照点"</b>;Yuhan:"要看背景,贫民窟长大可能真没接触过"'],
 ['这节把"推理"从"推背景"升级到"识破伪装",直指侦探故事的引擎:<b>谎言与不在场证明(alibi)。</b>',
  '<b>xuanying 的"反向心理"最值得记:高手会利用读者的"预期"来骗读者</b>——正因大家都以为"不对视=撒谎",一个说真话却不对视的角色就能误导。这是下周 Week 2("玩弄读者的怀疑")的预告。',
  '<b>"什么被记住、什么被遗忘"是可迁移的写作工具</b>:让角色对该记得的含糊、对不该记得的异常精确,读者立刻嗅到不对劲。'],
 DIALOG(
   D('Alex',"If someone doesn't look you in the eye when you question them — do you think they're shy, or something's amiss?",
     "如果有人被你审问时不看你的眼睛——你觉得是害羞,还是有点不对劲?"),
   D('Kaelyn',"I think it's suspicious. Even shy people give me eye contact 20–30% of the time. No eye contact at all is a huge sign — there probably isn't a way someone's interrogating you and you're staring at the floor the whole time.",
     "我觉得可疑。就算害羞的人也会有 20%–30% 的对视。完全不对视是很强的信号——被审问时全程盯着地板,几乎说不过去。"),
   D('xuanying',"Based on normal people, they're probably lying. But think about it in reverse psychology: you're telling the truth, but you don't want them to know it's the truth, so you don't look at them — creating the impression that when you tell the truth you don't make eye contact, when it's actually the opposite.",
     "按常人来看,他们多半在撒谎。但用'反向心理'想一想:你在说真话,却不想让对方知道这是真话,所以你不看他们——制造出'我说真话时不对视'的假象,而实际上恰恰相反。"),
   D('Alex',"I'm not sure what we're unearthing here, Shen Ying — this is very dark. But you're right: that expectation can get someone out of a tight spot.",
     "我不太确定我们挖出了什么,xuanying——这很黑暗。但你说得对:那种'预期'反而能让人脱身。"))
 +DIALOG(
   D('Alex',"Person E tells you three times, exactly, what they were doing at 9pm last night. Do you believe them? What do we call it in a crime story when someone has a reason they couldn't have been at the scene? Begins with A.",
     "E 号人物三次、精确地告诉你昨晚9点整在做什么。你信吗?在犯罪故事里,一个人有理由证明自己不可能在现场,我们叫它什么?A 开头。"),
   D('Kaelyn',"Is it called an alibi?",
     "是叫 alibi(不在场证明)吗?"),
   D('Alex',"Exactly. An alibi is someone or something that puts you in a certain place at a certain time. \"I couldn't possibly have committed the murder — I was at home with all my family.\" A solid alibi is hard to break.",
     "正是。alibi 是能证明你某时某刻在某地的人或物。'我不可能是凶手——当时我和全家人在家。'一个扎实的不在场证明很难被推翻。"),
   D('Kaelyn',"I'd say no — three times is stretching it, and \"exactly 9pm\" is too precise. If they tell me the same thing word for word, they're probably lying; if every time something's new, also probably lying.",
     "我会说不信——说三次太刻意,而且'精确到9点'太精准了。如果每次一字不差,多半在撒谎;如果每次都冒出新细节,也多半在撒谎。"),
   D('xuanying',"It depends what they were doing. A big event you'd remember. But a small random detail — what's deemed irrelevant gets forgotten quickly, so you're probably making it up.",
     "要看他们在做什么。大事件你会记得。但随机的小细节——被认为无关的东西很快会被忘掉,所以你多半在编。"),
   D('Yuhan',"I wouldn't believe them. If I find a new detail while investigating and the person also knows it and changes their alibi — that's kind of sus.",
     "我不会信。如果我调查时发现一个新细节,这个人也知道、然后改了口供——这就有点 sus(可疑)。"))
 +Q('Alex · 谎言难以自洽',
   ("It's much harder to keep a lie consistent. Telling a lie once isn't so hard, but if you ask repeatedly, ask for more specific details — that's where we slip up.",
    "让一个谎言保持前后一致要难得多。撒一次谎不难,但如果你反复追问、要更具体的细节——破绽就出在那里。"))
))

# ================= PART 3 =================
# S8 从侦探到作者
SEC.append(sec('08','s8','从侦探到作者 · 写你自己的"细节谜题"','46:00 – 53:00',
 ['<b>关键转身:Alex 让学生"从侦探变成作者"——仿照刚才的练习,写出你自己的"细节 + 推理"(prompt + answer)</b>',
  'xuanying 说她"喜欢从一张照片里挖出大量关于一个人的推断,有时到不健康的程度",Alex 顺势教了一个好词 inference(推断)',
  'Alex 用"湿头发"再示范:普通解释是"出门前洗了澡";但也可以是"沾上了会暴露自己的强烈气味,不得不冲掉"——同一细节藏着一整段背景',
  '因时间不够,Alex 把"写自己的细节谜题"改为课堂只做一个、其余带回家'],
 ['这节是全课的"输出转身":<b>学了怎么读线索,马上要求你反过来"造线索"。</b>会读 ≠ 会写,只有亲手设计一个"细节谜题",观察力才真正变成创作力。',
  '<b>判断线索好不好只有一条:它能不能同时容纳"平常"和"可疑"两种解释?</b>湿头发既能是洗澡、也能是灭迹——正因两解并存,读者才会停下来想。这就是好伏笔的定义。'],
 DIALOG(
   D('Alex',"It's time to go from detectives to writers. Can you make your own version of the prompts we've just looked at? Give me a question that raises your hackles, that makes you think \"hmm, what's been going on here?\" — and give me the answer too.",
     "该从侦探变成作者了。你能仿照刚才看的例子,写出你自己的版本吗?给我一个让你心里一紧、忍不住想'嗯?这里发生了什么'的问题——再给我答案。"),
   D('xuanying',"I enjoy sourcing out a lot of information from people — sometimes to an unhealthy amount. I can make a lot of inferences from just one picture.",
     "我喜欢从别人身上挖出大量信息——有时到了不太健康的程度。我能只凭一张照片做出很多推断。"),
   D('Alex',"Very good word there — inferences. I like that.",
     "用了个很好的词——inferences(推断)。我喜欢。"))
 +Q('Alex · 好线索的标准:能藏一整段背景',
   ("Wet hair could be a completely normal explanation — they had a shower. But it can also mean they had to shower because they were exposed to a strong smell that would give them away. There's a whole backstory involved. That's the kind of thing we're looking for.",
    "湿头发可以有完全正常的解释——他们洗了澡。但也可以是:他们不得不洗澡,因为沾上了会暴露自己的强烈气味。这背后藏着一整段故事。这正是我们要找的东西。"))
))

# S9 实战谜案 + 作业
SEC.append(sec('09','s9','实战谜案 · Lady Lavinia 之死 + 本周作业','53:00 – 59:30',
 ['进入一个完整的 Cluedo 式谋杀案(学生轮流朗读原文):Lady Lavinia 死在玫瑰花丛旁,身体发绿、表情惊恐,没有外伤,只有脖子上一个针刺孔(pinprick)和一小滴干血',
  '三名嫌疑人(学生逐一朗读设定):①<b>Fenton</b>——前夜刚满18岁、继承母亲财产的儿子(下午3:17发现尸体却拖到4点才报警);②<b>Sally</b>——他的未婚妻、银行职员,被视为"拜金女",掌管其母账户;③<b>Dr. Thorpe</b>——家庭医生,用花草为死者配药,租温室种植物,袖口沾着玫瑰茎',
  '<b>Yuhan 第一反应"是医生吧"——Alex 立刻借机点出关键写作原则:别让最明显的嫌疑人就是凶手,要让读者"以为是别人"</b>',
  '<b>本周作业:①谁是凶手?②更重要的是 how——那个针刺孔与死因如何关联?③写你自己的"细节谜题"(至少两个 prompt+answer)</b>'],
 ['这节把整堂课学的"推理"落到一个真实案子上,并抛出侦探写作最关键的一课:<b>凶手不能是"一眼看穿"的那个。</b>',
  '<b>作业里"how(怎么做到的)比 who(谁)更重要</b>——训练的是"设计诡计"的能力,直接通向下周 Week 2("玩弄读者的怀疑")。',
  '<b>如果你是外人、想自己练:</b>找一个"可观察细节"(磨损袖口、湿头发、发绿的皮肤),先写细节,再倒推出一个"既合理、又出人意料"的背景。这就是侦探写作的第一块砖。'],
 Q('案件原文 · Lady Lavinia 之死(Kaelyn 朗读)',
   ("Lady Lavinia was found lying in her garden by the rose bushes, dead. She was a strange greenish colour and had a shocked expression. There were no marks on her body except a small pinprick on her neck and a tiny spot of dried blood. Police are still investigating what could have made the pinprick, and whether it is related to her death.",
    "Lavinia 夫人被发现死在花园的玫瑰丛旁。她身体呈现奇怪的绿色,表情惊恐。身上没有任何外伤,只有脖子上一个小小的针刺孔和一小滴干血。警方仍在调查针刺孔是什么造成的、以及它是否与她的死有关。"))
 +Q('嫌疑人设定 · 三人(学生朗读)',
   ("① Fenton, who celebrated his 18th birthday the night before, making him heir to his mother's fortune — he woke at 1pm, found her at 3:17, yet didn't call police until 4. ② Sally, Fenton's fiancée and a bank clerk, seen as a gold-digger, who handles payments from his mother's account. ③ Dr. John Thorpe, the family doctor who made tinctures from herbs, rents a greenhouse on the estate — with a rose stem on his sleeve.",
    "①Fenton,前一晚刚过18岁生日、因此继承母亲财产——他下午1点才醒,3:17发现尸体,却拖到4点才报警。②Sally,Fenton 的未婚妻、银行职员,被视为拜金女,经手他母亲账户的支出。③John Thorpe 医生,家庭医生,用花草配制药水,在庄园租了温室——袖子上沾着一根玫瑰茎。"))
 +Q('Alex · 别让凶手太明显',
   ("The way these things usually work: let's not always make it the most obvious suspect. That's part of the game — we make the reader believe it is someone else.",
    "这类故事通常的玩法:别总让最明显的嫌疑人当凶手。这正是游戏的一部分——我们要让读者相信凶手是另一个人。"))
 +Q('本周作业 · Teacher Alex',
   ("Homework: who is the killer, and — the most interesting thing — how? How is the pinprick related to their death? And write your own prompt and answer, at least two.",
    "作业:谁是凶手?以及——最有趣的部分——怎么做到的?那个针刺孔和死亡如何关联?另外,写你自己的'细节谜题',至少两个(提示+答案)。"))
))

# S10 专业课程评析
SEC.append(sec('10','s10','专业课程评析 · 以世界级课程分析师的视角','课后复盘',
 ['<i>以下是站在"世界级创意写作课程分析师"角度的复盘,供你(老师/学习者)参考,不是课堂原话。</i>',
  '<b>这堂课好不好?</b> —— 很好。作为整个单元的第一课,它没急着讲"怎么写",而是先装底层引擎——deduce(推理):用"找企鹅"热身、用六个"细节谜题"反复操练、最后用一个完整案子收口,由易到难。唯一可加强:后半段时间偏紧,"写自己的谜题"被压成了作业',
  '<b>它到底教了什么?</b> —— 一条主线:<b>侦探写作 = 把"信息"变成武器。</b>观察细节→推理背景→识破谎言→反过来自己造线索。核心概念:deduce、clue、alibi、juxtaposition、inference、克制、"别让凶手太明显"',
  '<b>我怎样才能学会?</b> —— 不是记术语,而是"用一次":拿一个日常细节(湿头发/磨损袖口),写出两种解释——一个平常、一个可疑;再挑可疑那个,往下追三层背景',
  '<b>能应用在哪?</b> —— 远不止侦探小说:写任何人物都能用"一个细节暗示一段背景";人物访谈、写案例、观察生活里的人,"从细节推背景"都是通用的洞察力'],
 ['<b>这堂课的设计逻辑(值得你以后备课借鉴):</b>先装引擎(推理概念)→ 大量低风险小操练(六个细节谜题)→ 转为输出(自己造谜题)→ 综合实战(完整案子)。概念-操练-输出-实战,一条龙。',
  '<b>另一个亮点:Alex 全程"顺着学生往下带"</b>——Kaelyn 的化学品、xuanying 的反向心理、Yuhan 的"sus",他都不否定,而是接住、命名(inference/alibi)、升华成写作原则。这是"以学生的思考为材料"的教学法。',
  '<b>留给你的一步:自己写一段。</b>用一句话回答:"这堂课教会我的一个技巧是____,我打算用它来写/做____。"写下来,它才真的属于你。'],
 Q('一句话总结 · 这堂课的内核',
   ("A good detective — and a good writer — never guesses. They deduce: they make every tiny detail earn its place, so that even a frayed cuff or a strand of wet hair can hide an entire story.",
    "好的侦探——也是好的作者——从不瞎猜。他们推理:让每一个微小的细节都对得起自己的位置,于是连一截磨损的袖口、一缕湿发,都能藏下一整个故事。"))
))

BODY_REST=''.join(SEC)
open('wk1_body_rest.html','w').write(BODY_REST)
print("Part2cont+3+analysis, sections:",len(SEC),"chars:",len(BODY_REST))
