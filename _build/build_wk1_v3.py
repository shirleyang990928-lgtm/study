# -*- coding: utf-8 -*-
def S(en,zh): return f'<span class="sent"><span class="se">{en}</span><span class="sz">{zh}</span></span>'
# 对白：每个说话人一段，用 speaker 前缀
def D(speaker, en, zh):
    return f'<span class="sent"><span class="se"><b>{speaker}:</b> {en}</span><span class="sz"><b>{speaker}:</b> {zh}</span></span>'
def DIALOG(*turns): return '<div class="para dialog"><p class="en">'+' '.join(turns)+' </p></div>\n'
def Q(tag,*ps): return f'<div class="quote"><span class="tag ui">{tag}</span>\n<p class="en">'+' '.join(S(e,z) for e,z in ps)+' </p></div>\n'
def KP(*points): return '  <div class="keypoints ui"><b>要点</b><ul>\n'+''.join(f'    <li>{p}</li>\n' for p in points)+'  </ul>\n  </div>\n'
def EX(*points): return '  <div class="explain ui"><b>💡 这节在教什么</b><ul>\n'+''.join(f'    <li>{p}</li>\n' for p in points)+'  </ul>\n  </div>\n'
SEC=[]
def sec(num,sid,title,time,kp,ex,body):
    return (f'<!-- {sid.upper()} -->\n<section id="{sid}">\n'
            f'  <div class="sec-head"><span class="sec-num">{num}</span><h2>{title}</h2></div>\n'
            f'  <div class="sec-time ui">{time}</div>\n{KP(*kp)}{EX(*ex)}{body}</section>\n\n')

# ================= PART 1 =================
# S1 开场（纯寒暄→压要点；一进入"打招呼用语教学"→逐句还原）
SEC.append(sec('01','s1','开场 · 暖场与几种打招呼用语','00:00 – 04:00',
 ['(纯寒暄部分)新学期第一课,Alex 逐个问候:Alice 假期去韩国穿了韩服;Kaelyn 面试了想去的学校,Alex 教她 "fingers crossed(祝好运)"',
  '随后进入教学:让学生从屏幕上几种打招呼说法里各选一个说说看'],
 ['第一课先用问候建立轻松、被在乎的关系,再自然滑入第一个小教学点:英语里的多种问候语及其语域(正式/随意/老派)。'],
 DIALOG(
   D('Alex',"How are you getting on? That's a very common greeting. Any of these that stand out for you? Choose one, say it, and maybe tell me the answer as well.",
     "How are you getting on? 这是很常见的问候语。有没有哪一个让你印象深刻?选一个说说看,顺便回答它。"),
   D('Alice',"How are things going?","How are things going?(近来如何?)"),
   D('Alex',"How are things going with you? Good answer, good question. What about you, Kaelyn? Which one would you choose?",
     "How are things going with you? 好回答、好问题。你呢,Kaelyn?你会选哪个?"),
   D('Kaelyn',"I think I choose \"How's life?\" There's a running joke in my school that every time we don't have anything to start a conversation, we just go, \"How's life?\"",
     "我选 \"How's life?\"。我们学校有个梗:每次没话找话,我们就来一句 \"How's life?\"。"),
   D('Alex',"That's funny. It's quite common — you wouldn't use it with someone you see every day, but if you haven't seen someone for weeks or months, you might say \"How's life?\"",
     "有意思。这个挺常见——不会对天天见面的人用,但如果几周、几个月没见,就可以说 \"How's life?\"。"))
 +Q('Alex · 教一个老派说法',
   ("\"How do you do?\" — that's quite old-fashioned, quite upper-class. Almost the queen might say that. Very rarely asked in real life.",
    "\"How do you do?\"——这个相当老派、相当上流。几乎是女王会说的话。现实生活中很少有人这样问。"))
))

# S2 找企鹅（教学游戏，逐句还原）
SEC.append(sec('02','s2','暖场游戏 · 在巨嘴鸟里找企鹅','04:00 – 06:30',
 ['游戏规则:一大群巨嘴鸟(toucan)里藏着一只企鹅(penguin)——两种鸟很像,但企鹅没有白色脸罩,只有黑身 + 黄喙',
  'Kaelyn 很快找到,Alex 追问"相对位置在哪";Kaelyn 精确描述:"从黄衬衫沿对角线向上两格"',
  'Alice 说她本来不知道 toucan 是什么;Kaelyn 说自己家附近常见巨嘴鸟停在枝上讨食'],
 ['这个游戏在练侦探的第一项能力——<b>注意到别人忽略的小差异(观察)</b>。而 Alex 追问"精确位置"、表扬 Kaelyn "描述得好",练的是第二项——<b>把观察清楚地表达出来</b>。观察 + 表达,正是侦探和作者共同的基本功。'],
 DIALOG(
   D('Alex',"There's a penguin hiding among the toucans. Two different birds, very similar. They've all got black fur, a white mask, a white face, and a yellow beak. But there's a penguin that doesn't have the white mask — just black fur and a yellow beak. See if you can find it.",
     "有一只企鹅藏在巨嘴鸟群里。两种鸟很像:都是黑身、白色脸罩、白脸、黄喙。但有一只企鹅没有白色脸罩——只有黑身和黄喙。看你能不能找到。"),
   D('Alex',"Kaelyn's got her hand up already. Very quick, very perceptive. Tell me, Kaelyn.",
     "Kaelyn 已经举手了。真快,很敏锐。说说看,Kaelyn。"),
   D('Kaelyn',"It's the one around the midline, on my right side. I see the yellow shirt — go diagonally up two spaces.",
     "在中线附近,我的右手边。我看到那件黄衬衫——从那儿沿对角线向上两格。"),
   D('Alex',"Excellent. Very good, and very nicely described as well.",
     "非常好。找得好,而且描述得也很到位。"))
))

# S3 主题宣布（正式，逐句全留）
SEC.append(sec('03','s3','本学期主题 · 写自己的犯罪/侦探故事','06:30 – 08:00',
 ['<b>Alex 正式宣布本学期主题:"Build the suspense(构建悬念)"——我们要写自己的犯罪故事</b>',
  'Kaelyn 说很期待,"和我平时写的很不一样";Alice 说自己一直爱读"dark crime stories"',
  '<b>Alex 点出这类故事的核心机制:仍然有主角(protagonist)、甚至有反派(villain),但悬念、趣味来自"不知道谁犯了罪"</b>'],
 ['这是整个单元的"定调时刻",所以老师的原话完整保留。<b>侦探故事与普通故事最大的不同,是把"信息"当武器——故意不告诉读者凶手是谁,用这个悬念拉着人一直读。</b>'],
 DIALOG(
   D('Alex',"That was just a quick intro, because this term we are going to be looking at \"Build the Suspense\". We're going to be writing our own crime stories. Exciting times. What are your first thoughts on hearing that?",
     "刚才只是个小热身,因为这学期我们要做的是「构建悬念」。我们要写自己的犯罪故事。激动人心的时刻。听到这个,你们的第一反应是什么?"),
   D('Kaelyn',"This is probably really interesting. I'm looking forward to this — probably a bit different from what I usually write.",
     "这大概会很有意思。我很期待——应该和我平时写的挺不一样。"),
   D('Alex',"It is a little bit different. We've still got some elements — we're still gonna have a protagonist, our main character. We might even have a villain. But with a crime story, the suspense, the interest comes from not knowing who's committed the crime.",
     "确实有点不一样。有些元素还在——我们仍然会有主角、我们的主要人物。甚至可能有反派。但在犯罪故事里,悬念、趣味,来自'不知道是谁犯下了罪'。"),
   D('Alice',"I always read the dark crime stories, and I'm really interested.",
     "我一直读那些黑暗的犯罪故事,我真的很感兴趣。"),
   D('Alex',"Excellent. That's perfect. That's exactly what we're looking for.",
     "太好了。那太完美了。正是我们要做的。"))
))

# S4 认识经典（逐句）
SEC.append(sec('04','s4','认识经典 · 福尔摩斯、阿加莎与 Cluedo','08:00 – 12:00',
 ['Alex 介绍三个参照:柯南·道尔(Sir Arthur Conan Doyle)——他笔下的福尔摩斯是最著名的侦探之一;阿加莎·克里斯蒂(Agatha Christie)——英语世界最著名的侦探作家之一;桌游 Cluedo(《妙探寻凶》)',
  'Kaelyn 不认识柯南·道尔,但猜到"他是不是写了福尔摩斯"(答对);Yuhan 后来说老师课上放过福尔摩斯改编电影',
  '<b>Alex 解释 Cluedo:名字来自 clue(线索),给定"某人在某时某地被某凶器所杀"的框架,要用它推出凶手——和侦探故事同一套逻辑</b>'],
 ['先读经典、认作家,是为了在学生心里立起"好的侦探故事长什么样"的标尺——有参照,才知道往哪写。',
  'Cluedo 是这套单元的"活教具":它把侦探故事的逻辑(嫌疑人、不在场证明、凶器、地点)变成一个能上手玩的框架,后面的谜案练习都建立在它之上。'],
 DIALOG(
   D('Alex',"The first one is Sir Arthur Conan Doyle — The Hound of the Baskervilles. Has anyone heard of the author? Does anyone know the most famous detective from him?",
     "第一位是阿瑟·柯南·道尔——《巴斯克维尔的猎犬》。有人听过这位作者吗?有人知道他笔下最著名的侦探吗?"),
   D('Kaelyn',"I actually have no idea who he is, sorry. But — did he write Sherlock Holmes?",
     "我其实不知道他是谁,抱歉。但是——他是不是写了福尔摩斯?"),
   D('Alex',"He did indeed. That's why it was a bit of a trick question. You might not have heard of Conan Doyle, but his creation, Sherlock Holmes, is probably one of the most well-known detectives we've ever come across.",
     "他确实写了。所以这是个有点狡猾的问题。你也许没听过柯南·道尔,但他创造的福尔摩斯,大概是我们所知最著名的侦探之一。"),
   D('Alex',"Next, Agatha Christie — one of the most famous detective writers, at least in English. Same kind of story: the suspense comes from not knowing who committed the crime.",
     "接下来,阿加莎·克里斯蒂——至少在英语世界里,最著名的侦探作家之一。同一类故事:悬念来自不知道谁犯了罪。"),
   D('Alex',"Last one isn't a book — it's a game called Cluedo. As the name suggests, it's about clues. We get characters, a murder in a certain place, and using a framework we have to find out who the killer is. Same logic we see in detective stories.",
     "最后一个不是书——是个叫 Cluedo 的游戏。顾名思义,它讲的是线索(clue)。有一群角色、一桩发生在某地的谋杀,我们要用一套框架推出凶手是谁。和侦探故事是同一套逻辑。"))
))

# ================= PART 2 =================
# S5 deduce 概念（逐句）
SEC.append(sec('05','s5','核心概念 · 什么是"推理"(deduce)【本课关键】','12:00 – 13:30',
 ['Alice 朗读"像侦探一样思考"引子:侦探擅长 deduce(推理)——根据最微小的线索(体态、衣着、随身物、指甲)推断发生过什么',
  '<b>Alex 讲透 deduce 与 guess 的区别:guess(猜)可能随机瞎蒙;deduce(推理)是"用线索找出答案",像顺着一条小路走</b>',
  '福尔摩斯的关键特质:注意到一切——任何看似无关的微小细节,他都能连成解释"凶手是谁"的线索链'],
 ['这节给出整个单元最底层的能力词:<b>deduce(推理)。</b>它是"观察→推断"的思维动作,是这堂课乃至整学期所有练习的地基。',
  '<b>记住这个区分:guess 是碰运气,deduce 是拿证据。</b>好侦探(和好作者)从不瞎猜,而是让每个细节都"说话"。'],
 Q('Alice 朗读 · 什么是推理',
   ("Detectives are brilliant at deducing, which means working out things that have happened based on the smallest clues. They will study a suspect intensely — his body language, his clothes, his possessions, perhaps his fingernails. All these could be vital clues.",
    "侦探擅长推理,意思是根据最微小的线索推断出发生过的事。他们会仔细研究嫌疑人——体态、衣着、随身物品,也许还有指甲。这些都可能是关键线索。"))
 +DIALOG(
   D('Alex',"One of the key characteristics of Sherlock Holmes is that he notices everything. Any minor detail that we might think has no importance, he uses it, connects it to a chain of events that eventually explains who committed the crime.",
     "福尔摩斯的一个关键特质,就是他什么都注意到。任何我们以为毫无意义的微小细节,他都能用上、连成一条最终解释'谁犯了罪'的事件链。"),
   D('Alex',"To get there he uses a technique called deduction — to deduce. It's kind of like guess, but guess can be a bit random. Deduce is more like: use the clues to find an answer. It's like following a pathway.",
     "为此他用一种叫'演绎/推理'的方法——deduce。它有点像猜,但'猜'可能有点随机。'推理'更像是:用线索去找出答案,像顺着一条小路走。"))
))

BODY_P12=''.join(SEC)
open('wk1_body_p12.html','w').write(BODY_P12)
print("Part1+2 done, sections:",len(SEC),"chars:",len(BODY_P12))
