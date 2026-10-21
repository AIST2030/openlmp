#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 OpenLMP 从 50 个扩充到 70 个（新增 20 个）。
来源：用户提供的约 300 方法总清单中，筛选「契合可判定验收线模型、且与现有 50 个低重叠」者。
只取学习方法/思维方法域；国学修行、冥想、临床疗法、商业战略框架不做成可执行 skill
（无法满足机器可判定验收），另建 references/METHOD-UNIVERSE.md 索引。

硬约束同 expand_to_50.py：
  - category ∈ 八类；evidence ∈ {high, medium, anecdotal}（high 才需 refs）
  - steps ≥ 2，每步含 id/name/instruction/checkpoint
  - checkpoint 禁模糊词（理解/掌握/熟悉/深入/领会/吃透）
  - instruction 禁「自行决定」「视情况而定」
  - 纯度：全文禁 注册/登录/API Key/上传云端/订阅付费/引流微信
"""
import json, os, sys, datetime

OUT = sys.argv[1] if len(sys.argv) > 1 else "E:/视频创作/AIST2030/openlmp/skills"
TODAY = datetime.date.today().isoformat()

NEW = [
    # ============================== 技能习得（+2）==============================
    {
        "id": "simon-learning", "name": "西蒙学习法", "name_en": "Simon Learning Method",
        "category": "技能习得", "evidence": "anecdotal", "evidence_refs": [],
        "description": "一次只锁定一个目标，连续数月每天投入整块时间深耕，用单点饱和攻击代替四处浅尝。",
        "when_to_use": ["想在一个领域达到可用水平", "总是同时开好几个坑都半途而废", "有整块时间能长期投入"],
        "when_not_to_use": ["只有几天零碎时间", "目标本身还没选对"],
        "params": {
            "type": "object", "required": ["goal"],
            "properties": {
                "goal": {"type": "string", "description": "唯一要攻下的目标，写成「能做到X」"},
                "daily_min": {"type": "integer", "default": 240, "description": "每天深耕的分钟数"},
                "months": {"type": "integer", "default": 6, "description": "持续月数"}
            }
        },
        "steps": [
            {"id": "pick", "name": "锁定唯一目标", "duration_min": 6,
             "instruction": "写下这一个要攻下的目标，写成「能做到X」而非「学完X」，并把同期其他学习计划显式列出后删除，只保留这一个。",
             "checkpoint": "写下 1 个以「能做到X」表述的目标；且同期其他学习计划被列出并删除",
             "output": "唯一目标陈述"},
            {"id": "slice", "name": "切成可验收的子能力", "duration_min": 10,
             "instruction": "把目标拆成 4-6 项按顺序习得的子能力，每项写一条「做到什么算会」的可核对描述。",
             "checkpoint": "子能力 4-6 项；且每项都有一条可核对的达标描述",
             "output": "子能力清单"},
            {"id": "daily", "name": "每天整块投入", "duration_min": 240,
             "instruction": "每天在固定时段投入 daily_min 分钟，只练当前子能力；做完在日志记一行日期、内容、卡点。",
             "checkpoint": "连续记录天数 = 计划天数；且每天日志含日期、内容、卡点三要素",
             "output": "每日深耕日志"},
            {"id": "gate", "name": "逐项过关", "duration_min": 20,
             "instruction": "每项子能力用一条实作或真题验收，达标才进下一项；未达标就地重练，不跳过。",
             "checkpoint": "每项子能力都有一次验收结果记录；未达标项被重练而非跳过",
             "output": "过关记录", "fail_to": "daily"}
        ],
        "evaluate": {
            "self_check": ["这一小时我真的只砸在这一个目标上吗？", "过关是凭感觉，还是凭那条可核对的达标描述？"],
            "success_criteria": ["按计划天数完成深耕，无连续 2 天中断", "全部子能力通过验收"]
        },
        "agent_contract": {
            "input": ["goal", "daily_min", "months"], "output": ["唯一目标", "子能力清单", "深耕日志", "过关记录"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：用纸质日志记录每日投入与验收"
        }
    },
    {
        "id": "shadowing", "name": "影子跟读法", "name_en": "Shadowing",
        "category": "技能习得", "evidence": "medium", "evidence_refs": [],
        "description": "放着母语音频慢半拍同步复述，强迫耳朵、嘴巴、节奏对齐，专治看得懂但说不出、听得清却反应慢。",
        "when_to_use": ["练口语语感和发音节奏", "听力反应慢", "学到会读不会说的阶段"],
        "when_not_to_use": ["完全零基础的语音（先学音标再跟读）"],
        "params": {
            "type": "object", "required": ["audio"],
            "properties": {
                "audio": {"type": "string", "description": "带文稿的母语音频"},
                "lag_ms": {"type": "integer", "default": 500, "description": "落后原声的毫秒数"},
                "rounds": {"type": "integer", "default": 3, "description": "跟读轮数"}
            }
        },
        "steps": [
            {"id": "prep", "name": "选材并通听", "duration_min": 8,
             "instruction": "选一段 30-60 秒、带文稿的母语音频，先不看文稿完整听一遍，标出听不懂的位置。",
             "checkpoint": "音频时长在 30-60 秒；且标出了听不懂的位置",
             "output": "标疑点的音频"},
            {"id": "shadow", "name": "慢半拍跟读", "duration_min": 15,
             "instruction": "播放音频，比原声晚约 lag_ms 毫秒复述，尽量模仿语调重音；跟不上就暂停重来，不跳过。",
             "checkpoint": "完成 rounds 轮跟读；且每轮均晚于原声开口，未与原声同时",
             "output": "跟读记录"},
            {"id": "diff", "name": "对照文稿找差距", "duration_min": 8,
             "instruction": "现在看文稿，标出跟读中漏词、错音、语调跑偏的位置，逐条记下。",
             "checkpoint": "列出了漏词、错音、语调三类差距；且每类定位到具体词句",
             "output": "差距清单"},
            {"id": "loop", "name": "收窄差距重跟", "duration_min": 12,
             "instruction": "针对差距清单重跟，每轮统计仍出错的条目数，直到该轮新增出错为 0 或达到 rounds 上限。",
             "checkpoint": "给出了每轮出错条目数；且末轮出错数不高于首轮",
             "output": "收窄结果", "fail_to": "shadow"}
        ],
        "evaluate": {
            "self_check": ["我是真的在跟，还是等原声念完才开口？", "差距清单里的问题，下一轮真的少了吗？"],
            "success_criteria": ["末轮漏词与错音数不超过首轮一半", "不看文稿也能跟上语速"]
        },
        "agent_contract": {
            "input": ["audio", "lag_ms", "rounds"], "output": ["差距清单", "收窄结果"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无音频时：由 Agent 朗读，用户慢半拍复述"
        }
    },
    # ============================== 理解构建（+6）==============================
    {
        "id": "constructivist-learning", "name": "建构主义学习", "name_en": "Constructivist Learning",
        "category": "理解构建", "evidence": "medium", "evidence_refs": [],
        "description": "学新知识前先激活旧知识，把新内容挂到已有体系上，主动填补挂不上的缺口，而不是把新知识当孤立信息接收。",
        "when_to_use": ["学新知总觉得隔着一层", "知识点记住了但连不起来", "跨领域迁移"],
        "when_not_to_use": ["全新领域毫无基础时（先建立最小骨架）"],
        "params": {
            "type": "object", "required": ["topic"],
            "properties": {"topic": {"type": "string", "description": "要学习的新主题"}}
        },
        "steps": [
            {"id": "activate", "name": "先倒出已知", "duration_min": 8,
             "instruction": "在接触新材料前，先把关于这个主题你已经知道的东西全部写出，包括不确定的。",
             "checkpoint": "写出了至少 5 条已有认知；且含至少 1 条标注为不确定的条目",
             "output": "先备知识清单"},
            {"id": "read", "name": "带着清单读新材料", "duration_min": 20,
             "instruction": "读新材料时，每遇到一点就判断它证实了哪条、推翻了哪条、还是全新的一条，分别标注。",
             "checkpoint": "新材料要点被分为证实、推翻、全新三类；且每类都有具体条目",
             "output": "三色标注"},
            {"id": "graft", "name": "把新点挂到旧体系", "duration_min": 12,
             "instruction": "为每个「全新」点找到它在先备知识里的挂靠位置，写一句它和哪条旧知有什么关系。",
             "checkpoint": "每个全新点都写出了一条与旧知的关联；挂不上的被单独标为缺口",
             "output": "挂靠关系表"},
            {"id": "patch", "name": "补缺口并重画体系", "duration_min": 15,
             "instruction": "针对缺口补最小必要知识，再画一张更新后的知识关系图，标出本次新增与修改的节点。",
             "checkpoint": "缺口被逐条补齐或标注所缺前提；且产出了标注新增与修改节点的关系图",
             "output": "更新后的知识图", "fail_to": "activate"}
        ],
        "evaluate": {
            "self_check": ["我是在把新知接旧知，还是在背一份新名单？", "挂不上的地方，我说得清缺什么吗？"],
            "success_criteria": ["每个新点都能说出一条与旧知的关联", "关系图可据以复述整个主题"]
        },
        "agent_contract": {
            "input": ["topic"], "output": ["先备知识", "三色标注", "知识图"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸上完成先备、标注、挂靠三步"
        }
    },
    {
        "id": "thick-thin", "name": "薄厚互返法", "name_en": "Thick-then-Thin Reading",
        "category": "理解构建", "evidence": "anecdotal", "evidence_refs": [],
        "description": "第一遍把书读厚：大量批注、联想、质疑；第二遍再把书读薄：压缩成几张骨架卡，一厚一薄完成输入到内化。",
        "when_to_use": ["啃一本重要的书或长篇材料", "读过就忘、留不下东西", "想真正吃透一部经典"],
        "when_not_to_use": ["查资料找答案（只需检索，不必读厚）"],
        "params": {
            "type": "object", "required": ["material"],
            "properties": {"material": {"type": "string", "description": "要精读的书或长篇材料"}}
        },
        "steps": [
            {"id": "thick", "name": "读厚——密集批注", "duration_min": 40,
             "instruction": "第一遍细读，在边缘大量批注：联想、质疑、举例、反驳。禁止只画线不写字。",
             "checkpoint": "每章至少 3 处含文字的批注；且批注含联想、质疑、举例中的至少一类",
             "output": "批注版材料"},
            {"id": "harvest", "name": "捞出批注里的真问题", "duration_min": 10,
             "instruction": "把所有批注过一遍，挑出其中真正的困惑与分歧，写成问题清单，丢掉纯感叹。",
             "checkpoint": "问题清单至少 5 条；且每条为可回答的问题而非感叹",
             "output": "问题清单"},
            {"id": "thin", "name": "读薄——压成骨架", "duration_min": 20,
             "instruction": "合上材料，仅凭记忆与问题清单，把全书压缩成 1 张骨架图加若干要点卡，每张卡一句话。",
             "checkpoint": "产出 1 张骨架图；且要点卡每张仅一句话",
             "output": "骨架图与要点卡"},
            {"id": "reconcile", "name": "对照补漏", "duration_min": 10,
             "instruction": "重新打开材料，对照骨架图补遗漏的重要结构，但只补结构级遗漏，不把细节倒回去。",
             "checkpoint": "列出了结构级遗漏并已补入骨架；且未把大段细节倒回要点卡",
             "output": "定稿骨架", "fail_to": "thin"}
        ],
        "evaluate": {
            "self_check": ["我读薄时是靠记忆，还是又翻回了原文？", "骨架图能不能支撑我给别人讲这本书？"],
            "success_criteria": ["能凭骨架图复述全书结构", "要点卡覆盖了全部主要章节"]
        },
        "agent_contract": {
            "input": ["material"], "output": ["骨架图", "要点卡"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸质批注加手绘骨架"
        }
    },
    {
        "id": "case-study", "name": "案例研习", "name_en": "Case Study Method",
        "category": "理解构建", "evidence": "medium", "evidence_refs": [],
        "description": "拆解真实案例：还原情境、决策与结果，提炼可迁移的规律，再用新案例验证规律是否成立。",
        "when_to_use": ["想把理论用起来", "学管理、策略、诊断类知识", "从他人成败中学教训"],
        "when_not_to_use": ["只有理论、无真实案例可依时"],
        "params": {
            "type": "object", "required": ["domain"],
            "properties": {"domain": {"type": "string", "description": "要研习的领域"}}
        },
        "steps": [
            {"id": "collect", "name": "选 3 个同域案例", "duration_min": 15,
             "instruction": "选 3 个同一领域、结果不同的真实案例，至少 1 个成功、1 个失败，各写清背景。",
             "checkpoint": "案例数为 3；且成功与失败案例都至少 1 个，背景已写明",
             "output": "案例包"},
            {"id": "decompose", "name": "按同框架拆解", "duration_min": 25,
             "instruction": "用同一套维度拆每个案例：情境、关键决策、依据、结果，逐项填写，不写评价。",
             "checkpoint": "每个案例的四个维度都已填写；且内容为事实描述",
             "output": "拆解表"},
            {"id": "extract", "name": "提炼可迁移规律", "duration_min": 15,
             "instruction": "对比三个案例，写下 2-3 条「在什么条件下、什么做法、导致什么结果」的规律，每条注明来自哪些案例。",
             "checkpoint": "规律 2-3 条；且每条含条件、做法、结果三要素并标注案例来源",
             "output": "规律清单"},
            {"id": "transfer", "name": "用新案例验证", "duration_min": 12,
             "instruction": "找 1 个没拆过的新案例，只用上面的规律预测其结果，再对照真实结果。",
             "checkpoint": "用规律给出了预测；且对照了真实结果并记录是否命中",
             "output": "验证结论", "fail_to": "extract"}
        ],
        "evaluate": {
            "self_check": ["我提炼的是可迁移的规律，还是对单个案例的复述？", "新案例预测命中了吗？没命中是规律错还是漏了条件？"],
            "success_criteria": ["规律能预测新案例结果", "每条规律都能追溯到一个以上案例"]
        },
        "agent_contract": {
            "input": ["domain"], "output": ["拆解表", "规律清单", "验证结论"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：口头拆解并记录规律"
        }
    },
    {
        "id": "blooms-taxonomy", "name": "布鲁姆分层推进", "name_en": "Bloom's Taxonomy Ladder",
        "category": "理解构建", "evidence": "medium", "evidence_refs": [],
        "description": "按记忆、理解、应用、分析、评价、创造六层逐级推进，每层都要产出对应层次的证据，防止停在看着懂的低层。",
        "when_to_use": ["学一门系统性学科", "复习时不知道练到什么程度够", "自测学习深度"],
        "when_not_to_use": ["只需记住少量事实的场景"],
        "params": {
            "type": "object", "required": ["topic"],
            "properties": {"topic": {"type": "string", "description": "要分层推进的主题"}}
        },
        "steps": [
            {"id": "ladder", "name": "列出六级任务", "duration_min": 12,
             "instruction": "为该主题写六级各一条任务：记忆等于默写定义，理解等于改写释义，应用等于解新题，分析等于拆解结构，评价等于给方案排序并说理由，创造等于组合成新方案。",
             "checkpoint": "六级各有 1 条任务；且每条任务的动词与所在层级匹配",
             "output": "六级任务单"},
            {"id": "climb", "name": "自下而上闯关", "duration_min": 40,
             "instruction": "从记忆级开始逐级完成，本级产出被判定达标后才进上一级；跳级需说明理由。",
             "checkpoint": "每级都有对应产出；且未出现无产出就进级的记录，跳级均有理由说明",
             "output": "各级产出"},
            {"id": "locate", "name": "标出卡壳层级", "duration_min": 8,
             "instruction": "记录每一级是否一次通过，标出需要回头补的层级，那才是你真实的水平上限。",
             "checkpoint": "每级标注了是否一次通过；且指出了需回补的层级",
             "output": "层级诊断"},
            {"id": "drill", "name": "只补卡壳层", "duration_min": 20,
             "instruction": "针对卡壳层设计 2 条同级练习重做，其余层级本轮不重复练。",
             "checkpoint": "为卡壳层各设计了 2 条同级练习并完成；且未对已过关层级重复练习",
             "output": "补练结果", "fail_to": "climb"}
        ],
        "evaluate": {
            "self_check": ["我是真的逐层闯上来的，还是一直在记忆层打转？", "卡壳的那层，说得出差在哪吗？"],
            "success_criteria": ["六个层级都有对应产出", "卡壳层经补练后能一次通过"]
        },
        "agent_contract": {
            "input": ["topic"], "output": ["六级任务单", "各级产出", "层级诊断"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：对话式逐层提问检验"
        }
    },
    {
        "id": "inquiry-learning", "name": "探究式学习", "name_en": "Inquiry-Based Learning",
        "category": "理解构建", "evidence": "medium", "evidence_refs": [],
        "description": "以一个真问题为起点，自己提假设、找证据、下结论并反思过程，把学结论变成重走发现之路。",
        "when_to_use": ["想真正吃透一个现象", "培养独立解决问题的能力", "研究入门"],
        "when_not_to_use": ["只需套用现成步骤的操作性任务"],
        "params": {
            "type": "object", "required": ["question"],
            "properties": {"question": {"type": "string", "description": "想探究的问题"}}
        },
        "steps": [
            {"id": "frame", "name": "把好奇变成可研究的问题", "duration_min": 8,
             "instruction": "把一个模糊的好奇写成一个具体、可查证的问题，界定范围和变量。",
             "checkpoint": "问题被改写为含范围和变量的可查证问句",
             "output": "研究问题"},
            {"id": "hypothesize", "name": "先提可证伪的假设", "duration_min": 10,
             "instruction": "写下 2 个相互竞争的假设，各附一条「如果看到 X 就支持我」的判据。",
             "checkpoint": "假设数为 2；且每个假设都附了一条可判真伪的观察判据",
             "output": "假设与判据"},
            {"id": "gather", "name": "按判据找证据", "duration_min": 30,
             "instruction": "针对每个假设收集证据，只记录支持或反对的事实，并标注来源。",
             "checkpoint": "每条证据都标注了支持或反对哪个假设及其来源",
             "output": "证据表"},
            {"id": "conclude", "name": "下结论并反思", "duration_min": 12,
             "instruction": "对照判据给出结论，说明哪个假设被支持或否决、依据是什么；再反思过程里哪一步最可能出错。",
             "checkpoint": "给出了明确结论及对应证据；且写出了过程中最可能出错的环节",
             "output": "结论与反思", "fail_to": "hypothesize"}
        ],
        "evaluate": {
            "self_check": ["我先有了结论再去找证据，还是先有判据？", "被否决的假设，我是据理否的还是舍不得丢？"],
            "success_criteria": ["结论可由所列证据推出", "能指出本次探究最脆弱的环节"]
        },
        "agent_contract": {
            "input": ["question"], "output": ["假设与判据", "证据表", "结论"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：以对话推进假设、证据、结论"
        }
    },
    {
        "id": "first-principles", "name": "第一性原理", "name_en": "First Principles Thinking",
        "category": "理解构建", "evidence": "anecdotal", "evidence_refs": [],
        "description": "抛开别人都这么做的类比和经验，把问题拆到最基本、不可再分的事实，再从这些事实重新推理出路。",
        "when_to_use": ["面对从来如此的做法想质疑", "类比推理走进死胡同", "评估一个方案是否真的必要"],
        "when_not_to_use": ["已被充分验证的标准做法（重新推导性价比低）"],
        "params": {
            "type": "object", "required": ["problem"],
            "properties": {"problem": {"type": "string", "description": "要用第一性原理重拆的问题"}}
        },
        "steps": [
            {"id": "strip", "name": "剥掉类比和惯例", "duration_min": 10,
             "instruction": "写下关于这个问题「大家都这么认为或这么做」的 3 条默认假设，逐条标注哪些是事实、哪些只是惯例。",
             "checkpoint": "列出 3 条默认假设；且每条被标注为事实或惯例",
             "output": "假设剥离表"},
            {"id": "bedrock", "name": "沉到基本事实", "duration_min": 15,
             "instruction": "把问题继续往下拆，直到剩下不可再争辩的基本事实，如物理约束、定义、已被证的量，列出这些基石。",
             "checkpoint": "基石至少 3 条；且每条为不可再争辩的事实而非观点",
             "output": "基石清单"},
            {"id": "rebuild", "name": "从基石重推", "duration_min": 20,
             "instruction": "只使用基石清单，从零推理出一个方案，禁止引用被标为惯例的假设。",
             "checkpoint": "方案仅由基石推出；且推理过程未引用任何被标为惯例的假设",
             "output": "重推方案"},
            {"id": "compare", "name": "与旧方案对比", "duration_min": 10,
             "instruction": "把重推方案与现有做法并列，逐条比差异与代价，得出保留、替换或折中的结论。",
             "checkpoint": "列出了差异与代价；且给出了保留、替换、折中之一的明确结论",
             "output": "对比结论", "fail_to": "bedrock"}
        ],
        "evaluate": {
            "self_check": ["我的基石真的是事实，还是换了个说法的惯例？", "重推时我有没有偷偷把老假设放回来？"],
            "success_criteria": ["方案每一步都能追溯到某条基石", "能说清新旧方案差异的根源"]
        },
        "agent_contract": {
            "input": ["problem"], "output": ["基石清单", "重推方案", "对比结论"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸笔完成剥离、基石、重推"
        }
    },
    # ============================== 知识管理（+2）==============================
    {
        "id": "mind-map", "name": "思维导图", "name_en": "Mind Mapping",
        "category": "知识管理", "evidence": "medium", "evidence_refs": [],
        "description": "以中心词为根向外辐射分层，每枝只用关键词，用颜色和图像强化记忆，把一本书或一科知识画成一棵树。",
        "when_to_use": ["梳理一科或一本书的结构", "记忆量大需要视觉锚点", "备课或演讲前组织思路"],
        "when_not_to_use": ["需要严格逻辑推导的过程（导图会弱化推理链）"],
        "params": {
            "type": "object", "required": ["topic"],
            "properties": {"topic": {"type": "string", "description": "要画成导图的主题"}}
        },
        "steps": [
            {"id": "center", "name": "定中心与主干", "duration_min": 8,
             "instruction": "在纸或白板中央写下中心主题，向外拉出 4-7 条主干，每条一个核心方面，只用关键词。",
             "checkpoint": "主干 4-7 条；且每条均为关键词而非句子",
             "output": "中心与主干"},
            {"id": "branch", "name": "向外分层", "duration_min": 20,
             "instruction": "每条主干继续向下分叉，子枝同样只写关键词；同一层的枝保持粒度一致。",
             "checkpoint": "每条主干至少有 2 级子枝；且同层枝粒度一致，无长短句混用",
             "output": "分层导图"},
            {"id": "code", "name": "上色与配图", "duration_min": 12,
             "instruction": "给每个主干分配一种颜色，在关键枝上画简单图标；每张图旁只配一个关键词。",
             "checkpoint": "每个主干有唯一颜色；且至少 3 个关键枝配有图标加单一关键词",
             "output": "着色导图"},
            {"id": "recall", "name": "盖图复述", "duration_min": 10,
             "instruction": "盖住导图，凭记忆复述中心与各主干；复述不出的枝用粗笔标出，作为薄弱点回补。",
             "checkpoint": "完成了盖图复述；且复述失败的枝被标出",
             "output": "复述与薄弱点", "fail_to": "center"}
        ],
        "evaluate": {
            "self_check": ["我写的是关键词，还是偷偷写了整句？", "盖图后能从头讲到尾吗，哪条枝断了？"],
            "success_criteria": ["盖图能复述全部主干", "薄弱枝经回补后复述成功"]
        },
        "agent_contract": {
            "input": ["topic"], "output": ["分层导图", "薄弱点清单"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：手绘导图并口头复述"
        }
    },
    {
        "id": "three-color-notes", "name": "三色笔记法", "name_en": "Three-Color Notes",
        "category": "知识管理", "evidence": "anecdotal", "evidence_refs": [],
        "description": "固定三种颜色各司其职：一色记要点、一色记疑点、一色记补充或行动，用颜色规则让笔记自带优先级。",
        "when_to_use": ["笔记混成一锅粥", "分不清哪些是重点哪些是疑问", "复习时想快速定位疑点"],
        "when_not_to_use": ["电子环境无法方便用色时（可改用三种标记符号）"],
        "params": {
            "type": "object", "required": ["topic"],
            "properties": {"topic": {"type": "string", "description": "本次笔记主题"}}
        },
        "steps": [
            {"id": "rules", "name": "先定三色规则", "duration_min": 4,
             "instruction": "开记前先写下三色各自代表什么，分别对应要点、疑点、补充或行动，并固定下来不中途改。",
             "checkpoint": "写明了三色各自的含义；且三种颜色互不重复指代",
             "output": "配色规则"},
            {"id": "record", "name": "按色记录", "duration_min": 20,
             "instruction": "记录时严格按规则着色，要点、疑点、补充分别用对应颜色，一条一色不混用。",
             "checkpoint": "每条记录都归属且仅归属一种颜色；且无未着色的裸条目",
             "output": "三色笔记"},
            {"id": "triage", "name": "疑点优先处理", "duration_min": 12,
             "instruction": "复习时先只扫疑点色的条目，逐条解决或转成问题；要点色快速过，补充色仅在有行动时看。",
             "checkpoint": "疑点条目被逐条处理；且每条给出了解决结果或转化为待答问题",
             "output": "疑点处理结果"},
            {"id": "distill", "name": "提炼行动项", "duration_min": 6,
             "instruction": "从补充或行动色里挑出真正要做的，写成带截止时间的待办，其余归档。",
             "checkpoint": "产出了含截止时间的待办；且非行动类补充被归档不占待办",
             "output": "行动待办", "fail_to": "rules"}
        ],
        "evaluate": {
            "self_check": ["我是先想清楚内容再上色，还是随手涂颜色？", "疑点色里的问题，真的被解决了吗？"],
            "success_criteria": ["疑点全部有处理结果", "行动待办均可执行且带期限"]
        },
        "agent_contract": {
            "input": ["topic"], "output": ["三色笔记", "疑点处理", "行动待办"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无颜色时：用【要】【疑】【补】三种前缀符号替代"
        }
    },
    # ============================== 计划执行（+5）==============================
    {
        "id": "pomodoro", "name": "番茄工作法", "name_en": "Pomodoro Technique",
        "category": "计划执行", "evidence": "anecdotal", "evidence_refs": [],
        "description": "25 分钟全情投入一件事，铃响休息 5 分钟，四个番茄后长休息，用固定节律对抗拖延和分心。",
        "when_to_use": ["迟迟无法开始", "任务庞大想不动", "容易分心需要外力节律"],
        "when_not_to_use": ["需要长时间连续心流的深度创作（可拉长单钟）"],
        "params": {
            "type": "object", "required": ["task"],
            "properties": {
                "task": {"type": "string", "description": "这一个番茄要做的唯一任务"},
                "work_min": {"type": "integer", "default": 25, "description": "单钟工作分钟"},
                "short_break": {"type": "integer", "default": 5, "description": "短休息分钟"}
            }
        },
        "steps": [
            {"id": "commit", "name": "选定单个任务", "duration_min": 3,
             "instruction": "开始前只选定这一个任务并写下来；期间冒出的其他事记到旁路清单，不当场切换。",
             "checkpoint": "写下 1 个任务；且设立了旁路清单用于暂存临时念头",
             "output": "任务与旁路清单"},
            {"id": "work", "name": "一个番茄只做它", "duration_min": 25,
             "instruction": "设定 work_min 倒计时，期间只做该任务；被打断就重开这一个番茄，不续命。",
             "checkpoint": "完成了计划数量的番茄；且每个番茄内未切换任务，中断则重开",
             "output": "番茄执行记录"},
            {"id": "break", "name": "到点强制休息", "duration_min": 5,
             "instruction": "每个番茄结束立刻停，休息 short_break 分钟，起身或远眺，不刷信息流。",
             "checkpoint": "每个番茄后都有一次 short_break 时长的休息；且休息期间未刷信息流",
             "output": "休息记录"},
            {"id": "longbreak", "name": "四钟长休并复盘", "duration_min": 20,
             "instruction": "每完成 4 个番茄进行一次 15-30 分钟长休息，并回顾这几个番茄的完成度与分心次数。",
             "checkpoint": "每 4 个番茄后有 1 次 15-30 分钟长休；且记录了完成度与分心次数",
             "output": "阶段复盘", "fail_to": "work"}
        ],
        "evaluate": {
            "self_check": ["铃响我是真停了，还是再看一分钟？", "分心都发生在第几分钟，有没有规律？"],
            "success_criteria": ["按计划完成番茄数且中断多选择重开", "分心次数逐轮下降"]
        },
        "agent_contract": {
            "input": ["task", "work_min", "short_break"], "output": ["番茄执行记录", "阶段复盘"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无计时器时：用手机秒表或 Agent 报时"
        }
    },
    {
        "id": "smart-goals", "name": "SMART 目标法", "name_en": "SMART Goals",
        "category": "计划执行", "evidence": "anecdotal", "evidence_refs": [],
        "description": "把愿望改写成同时满足具体、可衡量、可达成、相关、有时限五条的目标，缺一不可。",
        "when_to_use": ["目标总是落不了地", "计划写得很虚无法验收", "季度或年度规划"],
        "when_not_to_use": ["探索期方向未明时（先探索再定目标）"],
        "params": {
            "type": "object", "required": ["wish"],
            "properties": {"wish": {"type": "string", "description": "想改写成目标的愿望"}}
        },
        "steps": [
            {"id": "specific", "name": "具体化", "duration_min": 5,
             "instruction": "把愿望改写成含明确对象和动作的陈述，删掉更好、提升一类空词。",
             "checkpoint": "目标含明确对象与动作；且不含更好、提升、一些等空词",
             "output": "具体化目标"},
            {"id": "measurable", "name": "可衡量", "duration_min": 5,
             "instruction": "给目标加一个数字或可观察的达成标志，并写清怎么算达标。",
             "checkpoint": "目标附带数值或可观察标志；且写明了达标判定方式",
             "output": "衡量标准"},
            {"id": "achievable", "name": "掂量可达成", "duration_min": 6,
             "instruction": "对照现有资源与时间判断目标是否够得着；过高的拆小，过低的调高，并说明依据。",
             "checkpoint": "给出了可达成性判断；且对过高或过低给出了调整及依据",
             "output": "调整后目标"},
            {"id": "relevant", "name": "对齐大方向", "duration_min": 4,
             "instruction": "写一句这个目标服务于哪个更上层的目标，说不出关联就标记为待定或放弃。",
             "checkpoint": "写出了所服务的上层目标；无关联者被标记待定或放弃",
             "output": "关联说明"},
            {"id": "timebound", "name": "定时限", "duration_min": 4,
             "instruction": "给目标设定明确的起止日期和至少一个中间检查点，并落到日历。",
             "checkpoint": "目标有起止日期；且至少设定 1 个中间检查点并落到日历",
             "output": "带期限目标", "fail_to": "specific"}
        ],
        "evaluate": {
            "self_check": ["五条里我是不是只在具体上下了功夫？", "这个目标月底我真能判断达成没有吗？"],
            "success_criteria": ["目标五要素齐全", "到期可直接判定达成或未达成"]
        },
        "agent_contract": {
            "input": ["wish"], "output": ["带期限目标"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面逐条过 SMART 五问"
        }
    },
    {
        "id": "dual-goal", "name": "双重目标法", "name_en": "Dual Goals",
        "category": "计划执行", "evidence": "anecdotal", "evidence_refs": [],
        "description": "同时设一个冲刺目标和一个保底目标：够到冲刺最好，够不到也先锁定保底，避免一次失败就全盘放弃。",
        "when_to_use": ["目标有难度、怕一次达不到就泄气", "状态波动大的长期任务", "想保住最低完成线"],
        "when_not_to_use": ["标准明确、非达即败的任务（勿为退缩留后门）"],
        "params": {
            "type": "object", "required": ["goal"],
            "properties": {"goal": {"type": "string", "description": "要设双层级的目标"}}
        },
        "steps": [
            {"id": "define", "name": "定两级目标", "duration_min": 6,
             "instruction": "写一个冲刺目标和一个保底目标，两者用同一衡量标准、不同数值。",
             "checkpoint": "冲刺与保底两个目标都已写出；且二者用同一衡量标准、仅数值不同",
             "output": "双目标"},
            {"id": "plan", "name": "分别定路线", "duration_min": 10,
             "instruction": "为冲刺目标准备完整计划，同时标出其中哪些步是保底目标的最小必需步。",
             "checkpoint": "冲刺计划已列出；且标出了保底所需的最小步骤子集",
             "output": "分级计划"},
            {"id": "run", "name": "先锁保底再冲刺", "duration_min": 30,
             "instruction": "执行时优先保证保底所需步骤全部完成，再投入冲刺增量；状态差时至少守住保底。",
             "checkpoint": "保底步骤被优先完成；且状态差的日期也有保底动作记录",
             "output": "执行记录"},
            {"id": "settle", "name": "到期分级结算", "duration_min": 8,
             "instruction": "到期分别判定冲刺与保底是否达成并记录差距；若仅达保底，明确差在哪、下次冲刺要补什么。",
             "checkpoint": "两级目标各有达成判定；未达冲刺者写出了差距与补救方向",
             "output": "结算报告", "fail_to": "define"}
        ],
        "evaluate": {
            "self_check": ["保底是不是被我当成了轻易放弃的借口？", "只达保底时，我清楚差在哪吗？"],
            "success_criteria": ["保底目标达成率高于单一目标时期", "每次只达保底都伴随明确的差距分析"]
        },
        "agent_contract": {
            "input": ["goal"], "output": ["双目标", "分级计划", "结算报告"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面定双目标并分级记录"
        }
    },
    {
        "id": "reverse-learning", "name": "逆向学习法", "name_en": "Reverse Learning",
        "category": "计划执行", "evidence": "anecdotal", "evidence_refs": [],
        "description": "先看目标长什么样，再倒推最短学习路径，只为要用到的学，跳过暂时用不上的。",
        "when_to_use": ["有明确考核或交付目标", "时间紧要直奔结果", "自学容易迷失在细节里"],
        "when_not_to_use": ["想系统打基础、无近期目标时（正向系统学更稳）"],
        "params": {
            "type": "object", "required": ["goal"],
            "properties": {"goal": {"type": "string", "description": "要直达的目标或考核"}}
        },
        "steps": [
            {"id": "inspect", "name": "先研究目标形态", "duration_min": 20,
             "instruction": "找到目标的真实样子：几套真题、一个成品样例或一份验收标准，逐条研究它长什么样。",
             "checkpoint": "获得了至少 2 个目标实例或 1 份验收标准；且已逐条研究",
             "output": "目标样本分析"},
            {"id": "decompose", "name": "倒推必需知识点", "duration_min": 15,
             "instruction": "对照样本，倒推出要做出它必须会哪些点，列成必需清单；用不到的先不学。",
             "checkpoint": "必需清单已列出；且每条标注了对应样本中的哪个要求",
             "output": "必需知识点清单"},
            {"id": "shortcut", "name": "排最短路径", "duration_min": 10,
             "instruction": "把必需点按依赖关系排成最短学习顺序，能合并的合并，标出可跳过的非必需内容。",
             "checkpoint": "给出了学习顺序；且标出了被跳过的非必需内容及其理由",
             "output": "最短路径"},
            {"id": "mock", "name": "用样本自测", "duration_min": 25,
             "instruction": "学完后用一套没用过的样本做模拟，对照验收标准自评，未达标处回到对应知识点补。",
             "checkpoint": "完成了 1 次模拟自测；且未达标处被定位到具体知识点",
             "output": "模拟自测结果", "fail_to": "decompose"}
        ],
        "evaluate": {
            "self_check": ["我是在为通过或交付学，还是又漫游进了细节？", "跳过的非必需内容，真的不影响达标吗？"],
            "success_criteria": ["能用未见过样本通过验收", "学习时长集中在必需清单内"]
        },
        "agent_contract": {
            "input": ["goal"], "output": ["必需清单", "最短路径", "模拟结果"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无样本时：让 Agent 按目标形态生成模拟验收题"
        }
    },
    {
        "id": "zeigarnik-pause", "name": "留一点学习法", "name_en": "Zeigarnik Pause",
        "category": "计划执行", "evidence": "anecdotal", "evidence_refs": [],
        "description": "在状态正佳或情节紧要处主动停下，利用未完成更难忘的心理，让下次更容易重新进入并保持念想。",
        "when_to_use": ["长篇材料一次啃不完", "想保持对一件事的持续惦记", "容易开头难、难在续上"],
        "when_not_to_use": ["需要一口气打完的战斗或调试（强停会丢上下文）"],
        "params": {
            "type": "object", "required": ["material"],
            "properties": {"material": {"type": "string", "description": "要分段推进的材料"}}
        },
        "steps": [
            {"id": "setup", "name": "规划停顿点", "duration_min": 4,
             "instruction": "开读前先标出几个预定停顿点，如每章末或悬念处，而不是读到哪算哪。",
             "checkpoint": "标出了至少 2 个预定停顿点；且停顿点位于章节末或悬念处",
             "output": "停顿点计划"},
            {"id": "pause", "name": "到点即停", "duration_min": 3,
             "instruction": "到达停顿点立刻停，哪怕还想继续；在停处写一句接下来最想弄清的 1 个问题。",
             "checkpoint": "在每个停顿点停下；且每处都写下了一个接下来想弄清的问题",
             "output": "带问题的停点"},
            {"id": "resume", "name": "先答题再继续", "duration_min": 20,
             "instruction": "下次回来先尝试回答上次留下的问题，再往下读；答不上就带着问题读。",
             "checkpoint": "继续前先尝试回答了上次的问题；答不上者带着问题继续",
             "output": "续读记录"},
            {"id": "close", "name": "收尾时清问题", "duration_min": 10,
             "instruction": "全部读完后，把过程中积累的待答问题逐条了结或明确搁置，避免只剩一堆悬案。",
             "checkpoint": "待答问题逐条有了结果，已答或明确搁置；无未处理的悬留问题",
             "output": "问题了结清单", "fail_to": "resume"}
        ],
        "evaluate": {
            "self_check": ["我停的时候是真到点，还是其实已经读腻了？", "留下的问题，下次真的推动我回来了吗？"],
            "success_criteria": ["停顿点问题多数在续读时被回答", "同一材料重启次数少于无停顿时"]
        },
        "agent_contract": {
            "input": ["material"], "output": ["停顿点计划", "问题了结清单"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：书签加便签记录待答问题"
        }
    },
    # ============================== 评测验证（+3）==============================
    {
        "id": "thirty-second-recall", "name": "30 秒速览", "name_en": "Thirty-Second Recall",
        "category": "评测验证", "evidence": "anecdotal", "evidence_refs": [],
        "description": "对每个知识点限时 30 秒自测能否立刻想出要点，想不出的当场标记，用反应速度区分真会和眼熟。",
        "when_to_use": ["复习时快速筛查薄弱点", "分不清眼熟和真会", "考前过一遍知识点"],
        "when_not_to_use": ["第一次学的新知识（还没内容可回忆）"],
        "params": {
            "type": "object", "required": ["scope"],
            "properties": {"scope": {"type": "string", "description": "要速览的知识范围"}}
        },
        "steps": [
            {"id": "list", "name": "列知识点", "duration_min": 6,
             "instruction": "把要测的范围拆成知识点清单，每条一个可独立回忆的点。",
             "checkpoint": "清单条目至少 8 条；且每条为可独立回忆的单个知识点",
             "output": "知识点清单"},
            {"id": "rapid", "name": "逐条 30 秒回想", "duration_min": 10,
             "instruction": "从第一条开始，限时 30 秒内写出或说出该点要点；时间到或想不出即停并标记，不拖延。",
             "checkpoint": "每条都有 30 秒内的产出；且想不出的条目标记为未通过",
             "output": "速览结果"},
            {"id": "bucket", "name": "分三堆", "duration_min": 5,
             "instruction": "把结果分为秒出、犹豫后出、想不出三堆，统计各堆数量。",
             "checkpoint": "每条被归入三堆之一；且给出了三堆各自的数量",
             "output": "分堆统计"},
            {"id": "attack", "name": "只攻后两堆", "duration_min": 15,
             "instruction": "对犹豫后出和想不出两堆重点复习并重测；秒出堆本轮不再占用时间。",
             "checkpoint": "后两堆被重测；且秒出堆本轮未重复占用时间",
             "output": "重测结果", "fail_to": "rapid"}
        ],
        "evaluate": {
            "self_check": ["秒出的是真会，还是刚好看到提示？", "想不出的点，我是真补上了还是又看了一遍？"],
            "success_criteria": ["重测后想不出堆清零或显著减少", "同一知识点二次能进入秒出堆"]
        },
        "agent_contract": {
            "input": ["scope"], "output": ["速览结果", "分堆统计", "重测结果"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：口头逐条 30 秒自测"
        }
    },
    {
        "id": "time-capsule-quiz", "name": "时间胶囊出题", "name_en": "Time-Capsule Quiz",
        "category": "评测验证", "evidence": "anecdotal", "evidence_refs": [],
        "description": "学习时由现在的你给未来的你出题并封存，到期后由未来的你作答，用时间差检验记忆是否真的留下来。",
        "when_to_use": ["想检验长期记忆而非临时记忆", "对抗学完就忘", "给自己设计阶段性测验"],
        "when_not_to_use": ["明天就要考（时间隔太短无意义）"],
        "params": {
            "type": "object", "required": ["topic"],
            "properties": {
                "topic": {"type": "string", "description": "要封存测验的主题"},
                "days": {"type": "integer", "default": 7, "description": "多少天后开封"}
            }
        },
        "steps": [
            {"id": "author", "name": "现在出题封存", "duration_min": 15,
             "instruction": "学完当场，就本主题出 5-8 道能考住自己的题并附答案，标注出题日期，封存到指定日期再看。",
             "checkpoint": "出题 5-8 道且每题附答案；且标注了出题与开封日期",
             "output": "封存题卡"},
            {"id": "seal", "name": "设定开封日", "duration_min": 3,
             "instruction": "把开封日设为 days 天后并在日历设提醒；封存后到日前不得偷看。",
             "checkpoint": "开封日已设定并落到日历；且承诺到期前不偷看",
             "output": "开封计划"},
            {"id": "open", "name": "到期独立作答", "duration_min": 20,
             "instruction": "到期后先不看书独立作答全部题目并记录用时；不会的题明确标注想不出。",
             "checkpoint": "全部题目被独立作答；且想不出的题被明确标注",
             "output": "作答记录"},
            {"id": "score", "name": "对答案算保持率", "duration_min": 8,
             "instruction": "对答案，计算答对率即保持率，按题目标注哪些全忘、哪些半忘，作为回补重点。",
             "checkpoint": "给出了保持率数值；且题目被分为全忘、半忘、记得三类",
             "output": "保持率报告", "fail_to": "open"}
        ],
        "evaluate": {
            "self_check": ["我出题是奔着考住未来的我，还是随便写了送分题？", "保持率低，是当时没学会还是真忘了？"],
            "success_criteria": ["保持率随时间推移仍不低于目标线", "全忘类题目被回补后重考答对"]
        },
        "agent_contract": {
            "input": ["topic", "days"], "output": ["封存题卡", "保持率报告"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：手写题卡装入信封写开封日"
        }
    },
    {
        "id": "tally-forgetting", "name": "正字统计法", "name_en": "Tally-the-Forgetting",
        "category": "评测验证", "evidence": "anecdotal", "evidence_refs": [],
        "description": "每次回忆就用正字给想不出的知识点记一笔，用涂改次数把我忘了多少次可视化，专攻涂得最多的。",
        "when_to_use": ["反复忘同一批点", "想把遗忘变成可见数据", "安排复习优先级"],
        "when_not_to_use": ["第一次记忆的新材料（先记再统计）"],
        "params": {
            "type": "object", "required": ["scope"],
            "properties": {"scope": {"type": "string", "description": "要统计遗忘的范围"}}
        },
        "steps": [
            {"id": "baseline", "name": "建正字榜", "duration_min": 5,
             "instruction": "把范围列成知识点清单，每条留一个正字计数位，初始为 0。",
             "checkpoint": "清单每条都有计数位；且初始值均为 0",
             "output": "正字榜"},
            {"id": "recall", "name": "逐条回忆并计数", "duration_min": 12,
             "instruction": "逐条回忆，想不出或回忆失败的就在该条记一笔，想出的不记。",
             "checkpoint": "每条都经过一次回忆尝试；且失败条目的笔画数与失败次数一致",
             "output": "计数字榜"},
            {"id": "rank", "name": "按涂改数排序", "duration_min": 4,
             "instruction": "数出每条的总笔画，从多到少排序，前几名就是最该攻的点。",
             "checkpoint": "给出了按笔画数排序的列表；且前几名被标为优先攻坚",
             "output": "优先级排序"},
            {"id": "attack", "name": "只攻前几名", "duration_min": 18,
             "instruction": "只对笔画最多的前 3 名专项复习并重测，重测仍失败的补一笔；其余本轮不动。",
             "checkpoint": "仅对前 3 名进行了专项复习；且重测结果被记录",
             "output": "攻坚结果", "fail_to": "recall"}
        ],
        "evaluate": {
            "self_check": ["我是在诚实计数，还是只想快点划完？", "笔画最多的点，是真不会还是从没记住过？"],
            "success_criteria": ["前几名攻坚后笔画数下降", "同一知识点不再连续多轮上榜"]
        },
        "agent_contract": {
            "input": ["scope"], "output": ["正字榜", "优先级排序", "攻坚结果"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸上画正字统计"
        }
    },
    # ============================== 元认知（+1）==============================
    {
        "id": "familiarity-count", "name": "回看计数法", "name_en": "Familiarity Counting",
        "category": "元认知", "evidence": "medium", "evidence_refs": [],
        "description": "初读时给每个似曾相识的点计数，把眼熟和真能回忆分开，眼熟是高发的假会信号。",
        "when_to_use": ["预习时估不准哪些真会", "读一遍感觉都懂却考不出", "分配复习优先级"],
        "when_not_to_use": ["全新领域几乎没有旧知可唤起时"],
        "params": {
            "type": "object", "required": ["material"],
            "properties": {"material": {"type": "string", "description": "要初读并计数的材料"}}
        },
        "steps": [
            {"id": "preview", "name": "初读并标记眼熟", "duration_min": 12,
             "instruction": "快速通读材料，遇到好像见过或学过的点就标记并计数，遇到全新的另标一类。",
             "checkpoint": "每个点被标为眼熟或全新之一；且眼熟点被计数",
             "output": "眼熟与全新分类"},
            {"id": "split", "name": "拆分眼熟点", "duration_min": 6,
             "instruction": "把眼熟点按能说出大意和只是觉得见过说不清再分两堆，分别计数。",
             "checkpoint": "眼熟点被分为两类；且两类各自计数",
             "output": "眼熟细分"},
            {"id": "probe", "name": "对眼熟点做真回忆", "duration_min": 12,
             "instruction": "只对眼熟点合上材料做真实回忆，能复述的打钩，复述不出的打叉并记录。",
             "checkpoint": "每个眼熟点都有真回忆结果，钩或叉；且回忆期间未看材料",
             "output": "真回忆结果"},
            {"id": "reprioritize", "name": "用数据重排优先级", "duration_min": 5,
             "instruction": "统计眼熟但复述不出的数量，这是最危险的假会区，列为最高优先级；真能复述的降级。",
             "checkpoint": "给出了假会区条目数与清单；且假会区被列为最高优先级",
             "output": "重排优先级", "fail_to": "probe"}
        ],
        "evaluate": {
            "self_check": ["我的眼熟是真学过，还是这次刚读过？", "假会区的点，我以前是不是一直误以为会了？"],
            "success_criteria": ["假会区被识别并优先攻克", "复习优先级由回忆结果而非感觉决定"]
        },
        "agent_contract": {
            "input": ["material"], "output": ["眼熟细分", "真回忆结果", "优先级"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：通读时用两种符号标记并口头复述"
        }
    },
    # ============================== 协作学习（+1）==============================
    {
        "id": "peer-instruction", "name": "同伴教学法", "name_en": "Peer Instruction",
        "category": "协作学习", "evidence": "medium", "evidence_refs": [],
        "description": "先抛一个概念题让大家各自投票，再与同伴讨论理由后二次投票，用观点碰撞把误解暴露并修正。",
        "when_to_use": ["小组课的难点概念", "自己拿不准的理解", "想借他人视角发现盲区"],
        "when_not_to_use": ["无同伴可讨论时（可用 Agent 模拟反方）"],
        "params": {
            "type": "object", "required": ["concept"],
            "properties": {"concept": {"type": "string", "description": "要通过同伴教学攻克的概念"}}
        },
        "steps": [
            {"id": "pose", "name": "出一道概念题", "duration_min": 8,
             "instruction": "针对该概念出一道有迷惑选项的概念题，选项覆盖常见误解，先不给答案。",
             "checkpoint": "题目已出且含迷惑选项；且覆盖至少 1 个常见误解",
             "output": "概念题"},
            {"id": "vote1", "name": "各自独立投票", "duration_min": 4,
             "instruction": "每人先独立作答并记下所选与一句理由，此时不得讨论。",
             "checkpoint": "每人都有独立投票记录及理由；且投票期间无讨论",
             "output": "首轮投票"},
            {"id": "discuss", "name": "结对说服", "duration_min": 10,
             "instruction": "与同伴就不同选择讨论，各自陈述理由说服对方，记录被说服或坚持的原因。",
             "checkpoint": "每人记录了讨论后是否改变选择及原因",
             "output": "讨论记录"},
            {"id": "vote2", "name": "二次投票并揭晓", "duration_min": 8,
             "instruction": "再次独立投票，然后公布答案与解析，重点讲正确项为何对、错误项错在哪。",
             "checkpoint": "完成二轮投票；且解析覆盖正确项与各错误项的错因",
             "output": "二轮投票与解析", "fail_to": "pose"}
        ],
        "evaluate": {
            "self_check": ["首轮我是不是凭感觉选的？", "被说服是因为想清楚了，还是碍于情面？"],
            "success_criteria": ["二轮正确率高于首轮", "能说出每个错误选项错在哪"]
        },
        "agent_contract": {
            "input": ["concept"], "output": ["概念题", "两轮投票", "解析"],
            "side_effects": ["仅写本地文件"], "degrade_to": "单人时：让 Agent 扮演持不同观点的同学进行辩论"
        }
    },
]


def main():
    os.makedirs(OUT, exist_ok=True)
    created, skipped = [], []
    for s in NEW:
        path = os.path.join(OUT, s["id"] + ".json")
        if os.path.exists(path):
            skipped.append(s["id"])
            continue
        doc = {
            "lmp": "0.1",
            "id": s["id"],
            "name": s["name"],
            "name_en": s["name_en"],
            "version": "0.1.0",
            "license": "CC0-1.0",
            "authors": ["OpenLMP 公共领域贡献"],
            "category": s["category"],
            "evidence": s["evidence"],
            "evidence_refs": s["evidence_refs"],
            "description": s["description"],
            "when_to_use": s["when_to_use"],
            "when_not_to_use": s["when_not_to_use"],
            "params": s["params"],
            "requires": {"tools": [], "assets": []},
            "steps": s["steps"],
            "evaluate": s["evaluate"],
            "agent_contract": s["agent_contract"],
            "resources": [],
            "metadata": {"created_at": TODAY, "updated_at": TODAY, "contributors": []},
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
            f.write("\n")
        created.append(s["id"])

    print("新增 %d 个：" % len(created))
    for c in created:
        print("  +", c)
    if skipped:
        print("\n跳过 %d 个（已存在）：%s" % (len(skipped), ", ".join(skipped)))
    total = len([f for f in os.listdir(OUT) if f.endswith(".json") and not f.startswith("_")])
    print("\n当前方法总数：%d" % total)


if __name__ == "__main__":
    main()
