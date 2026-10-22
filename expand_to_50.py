#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 OpenLMP 方法库从 22 个扩充到 50 个（新增 28 个）。

硬约束（每条都会过 runtime/lmp.py validate）：
  - lmp="0.1"、id 为 kebab-case、version 为 semver、license=CC0-1.0
  - category ∈ VALID_CATEGORIES 八类
  - evidence ∈ {high, medium, anecdotal}；evidence=high 必须给 evidence_refs
  - steps ≥ 2；每步含 id/name/instruction/checkpoint
  - checkpoint 不得含 VAGUE_CHECKPOINT 里的不可判定词
    （理解 / 掌握 / 熟悉 / 深入 / 领会 / 吃透）
  - instruction 不得含「自行决定」「视情况而定」
  - 纯度：序列化后不得命中 FORBIDDEN_PATTERNS
    （注册/登录/API Key/上传同步云端/订阅付费/引流等）
"""
import json, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "E:/视频创作/AIST2030/openlmp/skills"

REF_DUNLOSKY = "Dunlosky et al. 2013, Psychological Science in the Public Interest, 14(1) 4-58"
REF_ROEDIGER = "Roediger & Karpicke 2006, Psychological Science, 17(3) 249-255"
REF_CEPEDA = "Cepeda et al. 2006, Psychological Bulletin, 132(3) 354-380"
REF_CHI = "Chi et al. 1994, Cognitive Science, 18(3) 439-477"
REF_ATKINSON = "Atkinson, Derry, Renkl & Wortham 2000, Review of Educational Research, 70(2) 181-214"
REF_PAAS = "Paas et al. 2003, Educational Psychologist, 38(1) 23-32"
REF_RICKEY = "Rittle-Johnson & Star 2007, Journal of Educational Psychology, 99(3) 561-574"
REF_SWELLER = "Sweller 1988, Cognitive Science, 12(2) 257-285"
REF_BJORK = "Bjork 1994, Memory & Cognition (编), Cambridge: MIT Press"
REF_SCHWARTZ = "Schwartz & Bransford 1998, Cognition and Instruction, 16(4) 435-477"
REF_GICK = "Gick & Holyoak 1983, Cognitive Psychology, 15(1) 1-38"
REF_MCCLELLAND = "McClelland et al. 1995, Psychological Review, 102(3) 419-457"
REF_WALKER = "Walker & Stickgold 2004, Neuron, 44(1) 121-133"
REF_KORNELL = "Kornell et al. 2009, Psychonomic Bulletin & Review, 16(5) 942-948"
REF_TAYLOR = "Taylor & Rohrer 2010, Journal of Educational Psychology, 102(3) 837-844"
REF_COLLINS = "Collins et al. 1989, 收录于 Knowing, Learning, and Instruction (Resnick 编), 453-494"
REF_PAN = "Kornell, Hays & Bjork 2009, Journal of Experimental Psychology: Learning, Memory, and Cognition, 35(4) 989-998"
REF_FIORELLA = "Fiorella & Mayer 2016, Educational Psychology Review, 28(3) 339-368"

NEW = [
    # ============================== 记忆巩固（+6 → 10）==============================
    {
        "id": "interleaving", "name": "交错练习", "name_en": "Interleaving",
        "category": "记忆巩固", "evidence": "high",
        "evidence_refs": [REF_TAYLOR, REF_DUNLOSKY],
        "description": "把同一科的多种题型混着练，逼大脑每次先判断「该用哪招」，而不是无脑套上一个刚练的模式。",
        "when_to_use": ["分章节练都挺顺、一综合就不会", "公式/方法长得像容易混", "数学或编程刷题"],
        "when_not_to_use": ["完全零基础的新题型（先分块练熟再交错）"],
        "params": {
            "type": "object", "required": ["topic"],
            "properties": {
                "topic": {"type": "string", "description": "本次交错练习覆盖的范围，如「求极值」"},
                "rounds": {"type": "integer", "default": 12, "description": "题目总道数"}
            }
        },
        "steps": [
            {"id": "inventory", "name": "列出待混题型", "duration_min": 4,
             "instruction": "把这个范围里会考的题型写成清单，每种一句话说明「看到什么特征就该用它」。至少 3 种。",
             "checkpoint": "题型清单 ≥ 3 种，且每种都附了一条可判别的识别特征",
             "output": "题型清单"},
            {"id": "shuffle", "name": "打乱出题",
             "instruction": "按清单混合出题，相邻两题不出现同一类型。让 Agent 一次只给一题，做完再给下一题。",
             "duration_min": 20,
             "checkpoint": "题序中不存在相邻同型；作答期间未展示答案",
             "output": "混合题组与作答记录"},
            {"id": "diagnose", "name": "归因错误类型",
             "instruction": "逐题标注错因：① 选错方法 ② 方法对但算错 ③ 概念不清。只标不改正。",
             "duration_min": 6,
             "checkpoint": "每道错题都归入①②③之一，且未混入评价性描述",
             "output": "错因标注表"},
            {"id": "repair", "name": "只补最集中的一类",
             "instruction": "统计三类各占多少，挑数量最多的那一类专项重练 5 题，其余两类先不动。",
             "duration_min": 10,
             "checkpoint": "专项重练题数 = 5，且全部属于被选中的那一类",
             "output": "专项重练结果", "fail_to": "shuffle"}
        ],
        "evaluate": {
            "self_check": ["我做错的是因为不知道用哪个方法，还是知道用哪个但做错了？",
                        "混着练的时候，我有没有先停顿判断题型，还是直接开做？"],
            "success_criteria": ["综合卷的错题里「选错方法」占比下降", "相邻同型题不再连错"]
        },
        "agent_contract": {
            "input": ["topic", "rounds"], "output": ["题型清单", "作答记录", "错因标注表"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：对话式一问一答出题，不联网检索"
        }
    },
    {
        "id": "desirable-difficulty", "name": "必要难度", "name_en": "Desirable Difficulty",
        "category": "记忆巩固", "evidence": "medium",
        "evidence_refs": [],
        "description": "刻意把学习搞得「稍微费劲一点」——慢一点、隔久一点、换个形式，当下更累但记得更牢。",
        "when_to_use": ["学得太顺反而记不住", "一遍遍看觉得都会", "想提升长期保持率"],
        "when_not_to_use": ["时间极紧的临时突击（此时需要的是效率不是保持率）"],
        "params": {
            "type": "object", "required": ["material"],
            "properties": {
                "material": {"type": "string", "description": "当前觉得「已经会了」的材料"}
            }
        },
        "steps": [
            {"id": "measure", "name": "确认是真会还是看着眼熟", "duration_min": 5,
             "instruction": "不参考资料，把材料要点写出来，再逐条对照。把「以为会其实不会」的条目标出来。",
             "checkpoint": "产出了一份在核对前完成的默写稿，且标出了不相符的条目",
             "output": "对照差异表"},
            {"id": "raise", "name": "加一层难度",
             "instruction": "从以下选一项施加：① 延迟 1 天再复习 ② 换成另一种题型表述 ③ 打乱顺序。每次只加一项。",
             "duration_min": 8,
             "checkpoint": "明确写明了施加的是①②③中的哪一项，且只施加了一项",
             "output": "难度施加记录"},
            {"id": "retest", "name": "隔天复测",
             "instruction": "至少间隔 24 小时后，不看资料重做一遍上次标出的条目，记录正确率。",
             "duration_min": 8,
             "checkpoint": "复测与首次默写间隔 ≥ 24 小时，且记录了正确条目数与总条目数",
             "output": "复测正确率", "fail_to": "raise"}
        ],
        "evaluate": {
            "self_check": ["我选的「更费劲」是真的费劲，还是只是更花时间？",
                        "隔天复测的正确率比之前高了吗？"],
            "success_criteria": ["隔天复测正确率高于当天即时复测", "所需提示次数减少"]
        },
        "agent_contract": {
            "input": ["material"], "output": ["对照差异表", "复测正确率"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：口头默写与核对，不需要外部资料"
        }
    },
    {
        "id": "method-of-loci", "name": "记忆宫殿", "name_en": "Method of Loci",
        "category": "记忆巩固", "evidence": "medium",
        "evidence_refs": [],
        "description": "把要记的东西挂在你熟得闭眼都能走的空间路线上，用空间顺序当索引，回想时沿路走一遍。",
        "when_to_use": ["要背一长串有序内容", "演讲提纲、清单、流程", "视觉记忆好的人"],
        "when_not_to_use": ["内容之间有强逻辑关联（用概念图更好）"],
        "params": {
            "type": "object", "required": ["items"],
            "properties": {
                "items": {"type": "string", "description": "要记的条目，用逗号或换行分隔"},
                "route": {"type": "string", "default": "自家从门口到卧室的路线", "description": "用作索引的熟悉空间"}
            }
        },
        "steps": [
            {"id": "route", "name": "定路线和桩点", "duration_min": 5,
             "instruction": "选一条你极其熟悉的路线，按顺序数出与条目数相同的固定位置（如鞋柜→沙发→餐桌…）。把位置写成编号清单。",
             "checkpoint": "桩点数量 ≥ 条目数量，且每个桩点都是可独立指认的固定位置",
             "output": "桩点编号清单"},
            {"id": "encode", "name": "挂上夸张图像",
             "instruction": "为每条内容造一个视觉夸张、动作荒诞的图像，放到对应桩点上。图像越离谱越好记。",
             "duration_min": 15,
             "checkpoint": "每个桩点都配了一个含动作的画面描述，且描述里含具体名词与动词",
             "output": "图像-桩点对照表"},
            {"id": "walk", "name": "沿路走一遍回忆",
             "instruction": "不看书，按桩点顺序逐个说出对应内容。卡住的桩点标红，不跳过去。",
             "duration_min": 6,
             "checkpoint": "覆盖全部桩点一次；卡壳桩点被显式标出且数量已统计",
             "output": "回忆结果表"},
            {"id": "strengthen", "name": "只重做卡壳桩点",
             "instruction": "把标红桩点的图像改得更夸张，重新走一遍。至少连续 2 次全对为止。",
             "duration_min": 8,
             "checkpoint": "连续 2 轮回忆中标红桩点数 = 0",
             "output": "强化结果", "fail_to": "encode"}
        ],
        "evaluate": {
            "self_check": ["我的图像够不够具体，能不能「看见」它在动？",
                        "卡壳的位置是固定几个，还是每次都不一样？"],
            "success_criteria": ["按序回忆时能一次不卡走完全程", "一周后仍能按序说出 ≥80% 的条目"]
        },
        "agent_contract": {
            "input": ["items", "route"], "output": ["桩点清单", "图像对照表", "回忆结果表"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：纯文字描述桩点与图像，靠对话完成走桩"
        }
    },
    {
        "id": "chunking", "name": "组块化", "name_en": "Chunking",
        "category": "记忆巩固", "evidence": "medium",
        "evidence_refs": [],
        "description": "把零散信息按意义打包成少数几个块，绕开短时记忆的容量上限。",
        "when_to_use": ["记号码/清单/长串步骤", "信息碎且多", "背单词或术语表"],
        "when_not_to_use": ["材料本身已成体系（直接建结构更快）"],
        "params": {
            "type": "object", "required": ["material"],
            "properties": {
                "material": {"type": "string", "description": "需要压缩记忆的零散材料"},
                "chunk_size": {"type": "integer", "default": 4, "description": "每个块内的条目上限"}
            }
        },
        "steps": [
            {"id": "group", "name": "按意义分组",
             "instruction": "把材料按语义/用途/时间分成若干组，每组不超过 chunk_size 条。给每组起一个短标题。",
             "duration_min": 8,
             "checkpoint": "所有条目都归入了某一组，且每组都有标题、条数 ≤ chunk_size",
             "output": "分组表"},
            {"id": "label", "name": "提炼组标签",
             "instruction": "为每组造一个能提示全部内容的短标签（≤6 字），越有画面感越好。",
             "duration_min": 5,
             "checkpoint": "每组都有标签，且标签长度 ≤6 字",
             "output": "标签清单"},
            {"id": "recall", "name": "只凭标签还原",
             "instruction": "只看标签清单，逐组写出全部原始条目。写不出就留空，不要翻原文。",
             "duration_min": 8,
             "checkpoint": "产出了一份按标签组织的还原稿，且空项被显式保留",
             "output": "还原稿"},
            {"id": "diff", "name": "核对并压缩",
             "instruction": "对照原文统计每组漏了几条。把漏得多的组再拆小，直到每组还原都能全对。",
             "duration_min": 7,
             "checkpoint": "记录了每组漏条数；对漏条数 >0 的组给出了新的拆分方案",
             "output": "压缩方案与漏条统计", "fail_to": "group"}
        ],
        "evaluate": {
            "self_check": ["我的分组依据是意义，还是仅仅因为凑在一起？",
                        "标签能不能真的提示出全部内容？"],
            "success_criteria": ["凭标签还原的完整率逐轮上升", "所需组数稳定不再增加"]
        },
        "agent_contract": {
            "input": ["material", "chunk_size"], "output": ["分组表", "标签清单", "还原结果"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：对话中完成分组、贴标签与还原核对"
        }
    },
    {
        "id": "elaborative-rehearsal", "name": "精细复述", "name_en": "Elaborative Rehearsal",
        "category": "记忆巩固", "evidence": "medium",
        "evidence_refs": [],
        "description": "不满足于把信息念很多遍，而是给每条信息接上一个意思、一个例子、一个画面。",
        "when_to_use": ["反复念但记不住", "背定义、背单词", "信息孤立无关联"],
        "when_not_to_use": ["只需短期记住马上就能丢的内容"],
        "params": {
            "type": "object", "required": ["item"],
            "properties": {
                "item": {"type": "string", "description": "要记住的那一条信息"}
            }
        },
        "steps": [
            {"id": "ask-why", "name": "问它为什么成立", "duration_min": 4,
             "instruction": "针对这条信息，写出一个「因为……」的理由。写不出就明确记录「原因不明，待查」。",
             "checkpoint": "产出了一个以「因为」开头的完整句子，或一条明确的待查记录",
             "output": "理由句"},
            {"id": "hook", "name": "接一个已知事物",
             "instruction": "找一个你已经熟悉的东西跟它做关联，写成一句「它就像……，只不过……」。",
             "duration_min": 6,
             "checkpoint": "产出了一句含「就像」和「只不过」的类比句",
             "output": "类比句"},
            {"id": "scene", "name": "放一个具体场景",
             "instruction": "想一个这条信息真正会被用到的具体场景，写出场景里发生了什么、谁在做、结果如何。",
             "duration_min": 5,
             "checkpoint": "场景描述里同时含有人物、动作与结果三个要素",
             "output": "场景描述"},
            {"id": "retrieve", "name": "不看原文复述",
             "instruction": "合上资料，把这三层（理由/类比/场景）各说一遍。说不全的部分标出来，回到对应步骤重做。",
             "duration_min": 5,
             "checkpoint": "三层内容都被复述且缺失项被标出；缺失项已指定回退到哪一步",
             "output": "复述结果", "fail_to": "ask-why"}
        ],
        "evaluate": {
            "self_check": ["我是真的给它加了意思，还是只是多念了几遍？",
                        "这条信息现在挂在我的哪块已有知识上？"],
            "success_criteria": ["不看资料能说出理由、类比与场景三层", "三天后仍能回忆出场景"]
        },
        "agent_contract": {
            "input": ["item"], "output": ["理由句", "类比句", "场景描述"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：口头完成三层加工"
        }
    },
    {
        "id": "sleep-consolidation", "name": "睡眠巩固", "name_en": "Sleep Consolidation",
        "category": "记忆巩固", "evidence": "high",
        "evidence_refs": [REF_WALKER, REF_MCCLELLAND],
        "description": "把难啃的内容安排在睡前学、睡够再复盘，让睡眠帮你把当天的记忆固化下来。",
        "when_to_use": ["需要长期记住的硬内容", "考前复习安排", "背大量材料"],
        "when_not_to_use": ["需要当堂立刻输出的即时任务"],
        "params": {
            "type": "object", "required": ["material"],
            "properties": {
                "material": {"type": "string", "description": "计划睡前学习的材料"},
                "hours": {"type": "number", "default": 7.5, "description": "当晚计划睡眠时长（小时）"}
            }
        },
        "steps": [
            {"id": "pick", "name": "挑出最该巩固的部分", "duration_min": 4,
             "instruction": "从当天学的内容里挑出 3 条最难、最需要长期记住的。不要超过 3 条。",
             "checkpoint": "选定条目数 = 3，且每条都注明了为什么难",
             "output": "重点条目"},
            {"id": "evening", "name": "睡前过一遍",
             "instruction": "在入睡前 1 小时内，把这 3 条快速过一遍（朗读或默写均可），不做新内容。",
             "duration_min": 10,
             "checkpoint": "学习发生在入睡 1 小时内，且未引入新材料",
             "output": "睡前复习记录"},
            {"id": "protect", "name": "保住睡眠时长",
             "instruction": f"确保当晚睡眠不少于 {7.5} 小时的计划值。记录实际睡眠时长。",
             "duration_min": 2,
             "checkpoint": "记录了计划睡眠时长与实际睡眠时长两个数值",
             "output": "睡眠时长记录"},
            {"id": "morning", "name": "醒后立刻检验",
             "instruction": "起床后不看书，先写出昨晚那 3 条。统计写出了几条，与睡前正确率对比。",
             "duration_min": 5,
             "checkpoint": "记录了醒后正确条目数与睡前正确条目数，并给出两者差值",
             "output": "保持率对比", "fail_to": "evening"}
        ],
        "evaluate": {
            "self_check": ["我昨晚睡够了吗，还是熬了夜？",
                        "醒后想起来的，是不是睡前最难的那几条？"],
            "success_criteria": ["醒后回忆正确条目数不低于睡前", "连续 3 天保持率不下降"]
        },
        "agent_contract": {
            "input": ["material", "hours"], "output": ["重点条目", "睡眠时长记录", "保持率对比"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：靠自述睡眠时长与晨间默写完成"
        }
    },

    # ============================== 理解构建（+4 → 8）==============================
    {
        "id": "self-explanation", "name": "自我解释", "name_en": "Self-Explanation",
        "category": "理解构建", "evidence": "high",
        "evidence_refs": [REF_CHI, REF_ATKINSON],
        "description": "边看例题边对自己讲「这一步为什么这么做」，把每一步跟背后的原理对上号，而不是只记操作步骤。",
        "when_to_use": ["看例题看得懂、自己做就不会", "想搞清步骤背后的道理", "学数理和编程"],
        "when_not_to_use": ["纯流程性的操作步骤（照做即可，无需解释）"],
        "params": {
            "type": "object", "required": ["example"],
            "properties": {
                "example": {"type": "string", "description": "要拆解的例题或材料"},
                "depth": {"type": "integer", "default": 3, "description": "对每步追问的层数"}
            }
        },
        "steps": [
            {"id": "segment", "name": "切成步骤", "duration_min": 5,
             "instruction": "把例题按动作切成一个个步骤，逐步编号。每步只含一个动作。",
             "checkpoint": "步骤数 ≥ 3，且每步只描述了一个动作",
             "output": "步骤编号表"},
            {"id": "explain", "name": "给每步找理由",
             "instruction": "对每个步骤，写出它依据的是哪条规则、为什么在这里用。写不出就标「待补」。",
             "duration_min": 12,
             "checkpoint": "每步都配了一句依据说明，或一条「待补」标记；待补项已列出",
             "output": "逐步依据表"},
            {"id": "generalize", "name": "抽成通用句式",
             "instruction": "把依据抽成一句可复用的条件句：「当……时，就……」。至少写出 2 句。",
             "duration_min": 8,
             "checkpoint": "产出了 ≥2 条含「当……时，就……」结构的条件句",
             "output": "条件句清单"},
            {"id": "verify", "name": "换题验证",
             "instruction": "做一道没见过的新题，全程只用上面的条件句判断。做错就回到「给每步找理由」补缺口。",
             "duration_min": 12,
             "checkpoint": "新题作答完成；若出错，明确指出了缺口对应哪一步",
             "output": "验证结果", "fail_to": "explain"}
        ],
        "evaluate": {
            "self_check": ["我讲的是「为什么这么做」，还是在复述「做了什么」？",
                        "换一道新题我还能说出依据吗？"],
            "success_criteria": ["新题能独立做对并说出每步依据", "条件句在新场景仍适用"]
        },
        "agent_contract": {
            "input": ["example", "depth"], "output": ["步骤表", "依据表", "条件句清单"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：对话式逐步口述解释"
        }
    },
    {
        "id": "worked-examples", "name": "例题研习", "name_en": "Worked Examples",
        "category": "理解构建", "evidence": "high",
        "evidence_refs": [REF_ATKINSON, REF_SWELLER],
        "description": "先用完整解答的例题把思路看透，再自己做，避免新手在还没建立模式时就硬做题卡死。",
        "when_to_use": ["刚入门某个新题型", "做题总是卡在第一步", "自学新技能"],
        "when_not_to_use": ["已经会做但想提速（此时该直接练）"],
        "params": {
            "type": "object", "required": ["topic"],
            "properties": {
                "topic": {"type": "string", "description": "要研习的题型"},
                "examples": {"type": "integer", "default": 3, "description": "要看的例题道数"}
            }
        },
        "steps": [
            {"id": "study", "name": "逐行研读完整解答",
             "instruction": "让 Agent 提供带完整步骤与理由的解答。读的时候每一步都暂停，先自问「它为什么这么做」再看答案。",
             "duration_min": 15,
             "checkpoint": "每道例题都被逐步读过；且每步都先自问再对照",
             "output": "例题研读记录"},
            {"id": "faded", "name": "抽掉一步自己补",
             "instruction": "重新看同一道例题，但让 Agent 隐去中间某一步，自己补上。补对了再隐去下一步。",
             "duration_min": 12,
             "checkpoint": "每道例题至少被隐去并成功补全 1 步；卡住的步骤已被记下",
             "output": "补步结果"},
            {"id": "solo", "name": "不看解答独立做",
             "instruction": "找一道同类型新题，不看任何解答独立完成，只在最后对答案。",
             "duration_min": 12,
             "checkpoint": "新题独立作答完成；且作答期间未查阅解答",
             "output": "独立作答结果", "fail_to": "study"}
        ],
        "evaluate": {
            "self_check": ["我是看懂了思路，还是只是记住了这道题的答案？",
                        "从研读到独立做，中间缺的是哪一步？"],
            "success_criteria": ["同类型新题能独立做对", "需要的提示次数逐题减少"]
        },
        "agent_contract": {
            "input": ["topic", "examples"], "output": ["研读记录", "补步结果", "独立作答结果"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：以对话形式逐步讲解与补步"
        }
    },
    {
        "id": "contrast-cases", "name": "对比辨析", "name_en": "Contrasting Cases",
        "category": "理解构建", "evidence": "medium",
        "evidence_refs": [REF_RICKEY],
        "description": "把两个像但关键处不同的案例摆在一起逐项比，逼出你以为懂、实际模糊的那条边界。",
        "when_to_use": ["两个概念老是搞混", "知道定义但分不清适用场合", "学相似语法/API/术语"],
        "when_not_to_use": ["两个东西差异本来就一目了然"],
        "params": {
            "type": "object", "required": ["case_a", "case_b"],
            "properties": {
                "case_a": {"type": "string", "description": "第一个案例或概念"},
                "case_b": {"type": "string", "description": "第二个案例或概念"},
                "dims": {"type": "integer", "default": 4, "description": "对比维度数量"}
            }
        },
        "steps": [
            {"id": "collect", "name": "摆出两个案例",
             "instruction": "把两个容易混淆的案例并排列出，各自写一句最简描述。",
             "duration_min": 5,
             "checkpoint": "两个案例都被列出，且各配了一句描述",
             "output": "案例对照"},
            {"id": "dimensions", "name": "列出对比维度",
             "instruction": f"列出 {4} 个用来比较的维度（如：输入/输出/适用条件/失败后果），写成表头。",
             "duration_min": 6,
             "checkpoint": "维度数量 = 指定值，且每个维度都是可逐项填写的比较项",
             "output": "维度表头"},
            {"id": "fill", "name": "逐格填入差异",
             "instruction": "把两个案例在每个维度下的表现分别填进去，只写事实不写评价。",
             "duration_min": 10,
             "checkpoint": "表格每个单元格都已填写，且内容为可核对的事实描述",
             "output": "对比表"},
            {"id": "boundary", "name": "写出判据句",
             "instruction": "根据对比表，写一句可操作的判据：「出现 X 特征时用 A，出现 Y 特征时用 B」。",
             "duration_min": 6,
             "checkpoint": "产出了 1 句含两个明确特征与对应选择的判据句",
             "output": "判据句"},
            {"id": "stress", "name": "造反例压测判据",
             "instruction": "自己造 2 个边界情况，用判据句判断该选谁。判不出来就重写判据句。",
             "duration_min": 8,
             "checkpoint": "构造了 2 个边界案例；对判不出的情况给出了重写后的判据",
             "output": "压测结果", "fail_to": "boundary"}
        ],
        "evaluate": {
            "self_check": ["我填的是差异事实，还是在给两边贴好坏标签？",
                        "我的判据句在边界情况下还成立吗？"],
            "success_criteria": ["能独立写出区分两个案例的判据", "边界案例判断正确"]
        },
        "agent_contract": {
            "input": ["case_a", "case_b", "dims"], "output": ["案例对照", "对比表", "判据句"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：对话中口头对比并产出判据"
        }
    },
    {
        "id": "analogy-mapping", "name": "类比映射", "name_en": "Analogy Mapping",
        "category": "理解构建", "evidence": "medium",
        "evidence_refs": [REF_GICK],
        "description": "给陌生概念找一个结构相同的熟悉事物，逐项把对应关系摆出来，用已知推未知。",
        "when_to_use": ["新概念完全没直觉", "抽象概念难建立画面", "跨领域理解"],
        "when_not_to_use": ["只需要精确的技术细节（类比会引入误差）"],
        "params": {
            "type": "object", "required": ["concept"],
            "properties": {
                "concept": {"type": "string", "description": "要弄懂的新概念"},
                "source": {"type": "string", "description": "拿来类比的熟悉事物，可留空让 Agent 提议"}
            }
        },
        "steps": [
            {"id": "target", "name": "写下新概念的关键结构", "duration_min": 5,
             "instruction": "把新概念拆成 3-5 个关键要素，并画出它们之间的关系（谁作用于谁、谁依赖谁）。",
             "checkpoint": "要素数量在 3-5 之间，且要素间关系被显式写出",
             "output": "目标结构图"},
            {"id": "source", "name": "找一个同结构的熟悉事物",
             "instruction": "找一个你非常熟悉、且要素关系与目标相同的事物。若想不出，让 Agent 提供 2 个候选并说明各自的对应关系。",
             "duration_min": 8,
             "checkpoint": "确定了一个类比源；且源与目标的要素数量一致",
             "output": "类比源"},
            {"id": "map", "name": "逐项对应",
             "instruction": "把目标的每个要素与源的对应物一一配对，写成两列表。",
             "duration_min": 7,
             "checkpoint": "两列表行数 = 目标要素数，且无空行",
             "output": "映射表"},
            {"id": "limits", "name": "标出类比失效处",
             "instruction": "至少写出 2 处这个类比推不下去、会误导的地方。类比的边界比类比本身更重要。",
             "duration_min": 6,
             "checkpoint": "列出了 ≥2 条类比失效情形，且每条都说明为什么会误导",
             "output": "失效清单"}
        ],
        "evaluate": {
            "self_check": ["我类比的是结构关系，还是只是表面像？",
                        "这个比喻在哪一步会把人带偏？"],
            "success_criteria": ["能用类比推出新场景下的结论", "能说出类比什么时候不能用"]
        },
        "agent_contract": {
            "input": ["concept", "source"], "output": ["目标结构图", "映射表", "失效清单"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：口头给出类比与失效点"
        }
    },

    # ============================== 知识管理（+3 → 6）==============================
    {
        "id": "cornell-notes", "name": "康奈尔笔记", "name_en": "Cornell Notes",
        "category": "知识管理", "evidence": "medium",
        "evidence_refs": [],
        "description": "把纸（或文档）分成「主笔记 / 提示栏 / 摘要」三块，逼自己在记完当场提炼，而不是事后补救。",
        "when_to_use": ["上课或听讲座", "会后整理纪要", "读书做笔记"],
        "when_not_to_use": ["需要快速记录流水账的场合"],
        "params": {
            "type": "object", "required": ["topic"],
            "properties": {
                "topic": {"type": "string", "description": "本次笔记的主题"},
                "cues": {"type": "integer", "default": 5, "description": "提示栏关键词数量上限"}
            }
        },
        "steps": [
            {"id": "record", "name": "主栏记要点",
             "instruction": "在右侧主栏记录内容要点。每条一行，用自己的话，不抄原文长句。",
             "duration_min": 15,
             "checkpoint": "主栏条目 ≥ 5 条，且每条为单行的要点表述",
             "output": "主栏笔记"},
            {"id": "cue", "name": "左栏提炼提示词",
             "instruction": f"在左侧提示栏写出能唤起主栏内容的关键词或问题，不超过 {5} 个。",
             "duration_min": 6,
             "checkpoint": "提示词数量 ≤ 上限，且每个提示都能对应到主栏的具体条目",
             "output": "提示栏"},
            {"id": "summary", "name": "底部写摘要",
             "instruction": "在底部用 2-3 句话概括这一页的核心。必须包含一条结论或行动项。",
             "duration_min": 5,
             "checkpoint": "摘要 2-3 句，且其中含明确的结论或待办项",
             "output": "底部摘要"},
            {"id": "recite", "name": "盖住主栏复述",
             "instruction": "只看左栏提示词，复述主栏内容。复述不出的条目标出，回去补关键词。",
             "duration_min": 8,
             "checkpoint": "遍历全部提示词一次；复述失败的条目被标出且已补充关键词",
             "output": "复述结果", "fail_to": "cue"}
        ],
        "evaluate": {
            "self_check": ["我的提示词真能唤起内容，还是只是个标题？",
                        "摘要里有没有一句是可以马上执行的？"],
            "success_criteria": ["盖住主栏能复述 ≥80% 的要点", "一周后看摘要仍能想起要点"]
        },
        "agent_contract": {
            "input": ["topic", "cues"], "output": ["主栏笔记", "提示栏", "底部摘要"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：纯对话完成三栏整理"
        }
    },
    {
        "id": "three-pass-reading", "name": "三遍阅读法", "name_en": "Three-Pass Reading",
        "category": "知识管理", "evidence": "medium",
        "evidence_refs": [],
        "description": "同一份材料读三遍，每遍只干一件事：先摸骨架，再抠细节，最后挑刺。避免一遍就想全懂。",
        "when_to_use": ["啃长文或论文", "教材新章节", "读不懂的硬材料"],
        "when_not_to_use": ["消遣性阅读或已熟悉的材料"],
        "params": {
            "type": "object", "required": ["material"],
            "properties": {
                "material": {"type": "string", "description": "要精读的材料标题或路径"}
            }
        },
        "steps": [
            {"id": "skeleton", "name": "第一遍：只找骨架", "duration_min": 8,
             "instruction": "看标题、小标题、首尾段与图表，写出这份材料回答了哪几个问题。不读细节。",
             "checkpoint": "写出的待答问题数 ≥ 2，且未涉及细节内容",
             "output": "骨架问题清单"},
            {"id": "detail", "name": "第二遍：逐段填细节",
             "instruction": "逐段精读，每段用一句自己的话概括，并记下看不懂的地方。不纠结、不回看。",
             "duration_min": 25,
             "checkpoint": "每段都配了一句概括；且所有读不懂处都被逐条记下",
             "output": "段落概括与疑点清单"},
            {"id": "critique", "name": "第三遍：回头挑刺",
             "instruction": "带着疑点回看，逐条尝试解答；仍不通的，明确写出「缺什么前提才能懂」。",
             "duration_min": 15,
             "checkpoint": "疑点清单每条都有处理结果（已解决 / 缺某前提），且未解决的列出了所缺前提",
             "output": "疑点处理结果", "fail_to": "detail"}
        ],
        "evaluate": {
            "self_check": ["我是先建立结构再看细节，还是一头扎进字里？",
                        "看不懂的地方，我能不能说清具体缺什么？"],
            "success_criteria": ["能不看材料复述其骨架与关键细节", "疑点大多被自己解决"]
        },
        "agent_contract": {
            "input": ["material"], "output": ["骨架问题清单", "段落概括", "疑点处理结果"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：口头完成三遍阅读流程"
        }
    },
    {
        "id": "note-flow-code", "name": "笔记流水线", "name_en": "Capture-Organize-Distill-Express",
        "category": "知识管理", "evidence": "anecdotal",
        "evidence_refs": [],
        "description": "把笔记拆成捕获、组织、提炼、表达四道固定工序，解决「记了一堆但从来不看」的问题。",
        "when_to_use": ["笔记越记越乱", "收藏了很多但没消化", "想让笔记产出作品"],
        "when_not_to_use": ["只需临时记录、用完即弃的信息"],
        "params": {
            "type": "object", "required": ["inbox"],
            "properties": {
                "inbox": {"type": "string", "description": "待处理的原始笔记或素材"},
                "output_form": {"type": "string", "default": "一段可直接发布的文字", "description": "最终想产出的形式"}
            }
        },
        "steps": [
            {"id": "capture", "name": "无脑捕获",
             "instruction": "把脑子里冒出来的、看到的都丢进收集箱，不做整理不判断价值。",
             "duration_min": 8,
             "checkpoint": "收集箱内条目 ≥ 5 条，且收集期间未做删改判断",
             "output": "收集箱"},
            {"id": "organize", "name": "按用途分堆",
             "instruction": "把收集箱内容按「要做的 / 要留的 / 要扔的」三堆分开。扔的那堆立刻删掉。",
             "duration_min": 8,
             "checkpoint": "每条都被分入三堆之一；且「要扔的」条目数已被记录并清除",
             "output": "三堆分类"},
            {"id": "distill", "name": "提炼成要点",
             "instruction": "对「要留的」逐条压缩成一句话要点，保留原始出处。",
             "duration_min": 12,
             "checkpoint": "每条「要留的」都产出了一句要点且附出处",
             "output": "要点清单"},
            {"id": "express", "name": "输出成成品",
             "instruction": "按 output_form 把要点组织成一段能直接交出去的成品，不堆砌要点。",
             "duration_min": 15,
             "checkpoint": "产出的成品符合 output_form，且为连贯文字而非要点罗列",
             "output": "成品文本", "fail_to": "distill"}
        ],
        "evaluate": {
            "self_check": ["我囤的东西有多少真的被提炼过？",
                        "这次的成品能不能直接发出去，还是还要再改？"],
            "success_criteria": ["收集箱能清空到 0 条", "每次提炼都产出了一件成品"]
        },
        "agent_contract": {
            "input": ["inbox", "output_form"], "output": ["要点清单", "成品文本"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：对话式完成四道工序"
        }
    },

    # ============================== 评测验证（+3 → 6）==============================
    {
        "id": "practice-testing", "name": "练习测验", "name_en": "Practice Testing",
        "category": "评测验证", "evidence": "high",
        "evidence_refs": [REF_ROEDIGER, REF_DUNLOSKY],
        "description": "不等考试，自己先做一遍低风险的测验，把「以为会」和「真的会」分开。",
        "when_to_use": ["复习完想验证效果", "考前自查", "学完一章"],
        "when_not_to_use": ["第一次接触材料（还没内容可测）"],
        "params": {
            "type": "object", "required": ["scope"],
            "properties": {
                "scope": {"type": "string", "description": "本次测验覆盖的范围"},
                "count": {"type": "integer", "default": 8, "description": "题目数量"}
            }
        },
        "steps": [
            {"id": "blueprint", "name": "先定考什么", "duration_min": 5,
             "instruction": "列出这次要测的知识点清单及其权重，按权重分配题量。",
             "checkpoint": "知识点清单含权重；各知识点分配题量之和 = 总题数",
             "output": "命题蓝图"},
            {"id": "generate", "name": "出题（先不给答案）",
             "instruction": "让 Agent 按蓝图出题，一次一题，答案在全部答完前不展示。",
             "duration_min": 20,
             "checkpoint": "题数 = 指定值；且作答过程中未展示任何答案",
             "output": "题目序列与作答记录"},
            {"id": "grade", "name": "对答案并统计",
             "instruction": "逐题核对，按知识点统计正确率，找出正确率最低的 2 个知识点。",
             "duration_min": 8,
             "checkpoint": "每个知识点都算出了正确率；正确率最低的 2 个被点名",
             "output": "知识点正确率表"},
            {"id": "remediate", "name": "只补最弱的两个",
             "instruction": "针对最弱的 2 个知识点重学并重测，其余不动。重测后更新正确率。",
             "duration_min": 15,
             "checkpoint": "重测覆盖了那 2 个知识点；且记录了重测后的正确率",
             "output": "补救结果", "fail_to": "remediate"}
        ],
        "evaluate": {
            "self_check": ["我测的是「记没记住」，还是「认不认得」？",
                        "正确率最低的点，我是真补上了还是只是又看了一遍？"],
            "success_criteria": ["最弱知识点的重测正确率 ≥ 80%", "总体正确率逐轮上升"]
        },
        "agent_contract": {
            "input": ["scope", "count"], "output": ["命题蓝图", "作答记录", "知识点正确率表"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：口头出题与核对"
        }
    },
    {
        "id": "think-aloud", "name": "出声思维", "name_en": "Think-Aloud Protocol",
        "category": "评测验证", "evidence": "medium",
        "evidence_refs": [],
        "description": "做题或解决问题时把脑子里的每一步说出来（或写出来），让隐性思路变成可检查的对象。",
        "when_to_use": ["总是犯莫名其妙的错误", "想找出思路断在哪", "调试或解题过程复盘"],
        "when_not_to_use": ["熟练到已自动化的操作（说出来反而拖慢）"],
        "params": {
            "type": "object", "required": ["task"],
            "properties": {
                "task": {"type": "string", "description": "要边做边说的具体任务"}
            }
        },
        "steps": [
            {"id": "setup", "name": "定任务并约定规则",
             "instruction": "选定一个具体任务。规则：全程出声，不说「我在想」，只说想的内容；卡住也要说卡在哪。",
             "duration_min": 3,
             "checkpoint": "任务已写明；规则被完整转述一遍",
             "output": "任务与规则"},
            {"id": "perform", "name": "边做边说",
             "instruction": "开始执行任务，把每一步的想法说出来。让 Agent 同步记录，不打断不提示。",
             "duration_min": 15,
             "checkpoint": "产出了连续的思路记录；且记录期间无外部提示介入",
             "output": "出声记录"},
            {"id": "audit", "name": "回看找断点",
             "instruction": "对照记录，标出三类位置：跳步（省略了推理）、误判（基于错误前提）、回头（反复改主意）。",
             "duration_min": 10,
             "checkpoint": "三类位置各被标出至少 1 处；若某类没有则显式写「无」",
             "output": "断点标注"},
            {"id": "patch", "name": "给断点加动作",
             "instruction": "为每个断点写一条具体动作来补（如「跳步处必须写下中间结论」），下次执行时照做。",
             "duration_min": 8,
             "checkpoint": "每个断点都配了一条可执行动作；动作描述含具体行为",
             "output": "动作清单", "fail_to": "perform"}
        ],
        "evaluate": {
            "self_check": ["我说的是真实想法，还是事后编的理由？",
                        "断点是不是集中在同一类地方？"],
            "success_criteria": ["下一轮执行时断点数量下降", "同类错误不再重复出现"]
        },
        "agent_contract": {
            "input": ["task"], "output": ["出声记录", "断点标注", "动作清单"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：以文字逐条写出当时的想法"
        }
    },
    {
        "id": "rubric-check", "name": "量规自检", "name_en": "Rubric Self-Assessment",
        "category": "评测验证", "evidence": "medium",
        "evidence_refs": [],
        "description": "先定好「做到什么样算合格」的评分表，再照表逐项给自己打分，把主观感觉换成可核对的清单。",
        "when_to_use": ["做完作品不知道够不够好", "提交前最后检查", "写作/设计/代码评审"],
        "when_not_to_use": ["探索阶段的草稿（过早打分会限制思路）"],
        "params": {
            "type": "object", "required": ["work"],
            "properties": {
                "work": {"type": "string", "description": "待评估的作品或成果"},
                "dims": {"type": "integer", "default": 5, "description": "评分维度数量"}
            }
        },
        "steps": [
            {"id": "define", "name": "先写评分表",
             "instruction": f"列出 {5} 个评价维度，每个维度写清「做到什么算合格」。先定表再看作品。",
             "duration_min": 10,
             "checkpoint": "维度数 = 指定值；每维都有一条可核对的合格标准",
             "output": "评分量规"},
            {"id": "score", "name": "逐项打分并举证",
             "instruction": "对每个维度打 0-2 分（0=没做到，2=达标），并附上作品里的具体位置作为证据。",
             "duration_min": 12,
             "checkpoint": "每维都有分数与证据引用；分数为 0 或 1 的都给出了证据",
             "output": "评分与证据表"},
            {"id": "fix", "name": "只改 0 分项",
             "instruction": "把所有 0 分项列成待办，逐条改完再重评一次。1 分项本次不动。",
             "duration_min": 15,
             "checkpoint": "生成了 0 分项待办清单；且改完后重评，0 分项数量归零或已记录剩余项",
             "output": "修复结果", "fail_to": "score"}
        ],
        "evaluate": {
            "self_check": ["我的评分表是动手前定的，还是看到作品后补的？",
                        "每个低分我都能指出具体位置吗？"],
            "success_criteria": ["重评后 0 分项数量下降", "评分有证据支撑而非印象"]
        },
        "agent_contract": {
            "input": ["work", "dims"], "output": ["评分量规", "评分与证据表", "修复结果"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：口头完成量规与打分"
        }
    },

    # ============================== 技能习得（+4 → 6）==============================
    {
        "id": "cognitive-apprenticeship", "name": "认知学徒", "name_en": "Cognitive Apprenticeship",
        "category": "技能习得", "evidence": "medium",
        "evidence_refs": [REF_COLLINS],
        "description": "让高手把原本藏在脑子里的思考过程外放出来：先示范、再带着做、然后放手，最后让你自己讲一遍。",
        "when_to_use": ["跟着师傅学手艺", "学难以言传的判断力", "带新人/带徒弟"],
        "when_not_to_use": ["有清晰文档和标准流程的任务（直接照文档更快）"],
        "params": {
            "type": "object", "required": ["skill"],
            "properties": {
                "skill": {"type": "string", "description": "要习得的具体技能"},
                "expert": {"type": "string", "description": "示范者是谁，可留空用 Agent 模拟"}
            }
        },
        "steps": [
            {"id": "model", "name": "看高手做一遍",
             "instruction": "让示范者边做边把判断依据说出来，重点是「为什么这么做」而不是「做了什么」。",
             "duration_min": 15,
             "checkpoint": "记录中包含 ≥3 处明确的判断依据说明",
             "output": "示范记录"},
            {"id": "coach", "name": "在提示下做一遍",
             "instruction": "自己动手做，卡住时示范者只给提示不给答案。记录每处提示。",
             "duration_min": 25,
             "checkpoint": "完成了一遍尝试；且每处提示都被逐条记录",
             "output": "尝试记录与提示清单"},
            {"id": "fade", "name": "撤掉提示独立做",
             "instruction": "不看提示独立完成同一任务。与前一次对比，统计还需要提示的地方。",
             "duration_min": 20,
             "checkpoint": "独立完成了任务；且给出了与上次相比提示次数的变化",
             "output": "独立完成结果", "fail_to": "coach"},
            {"id": "articulate", "name": "讲一遍自己怎么做的",
             "instruction": "把整个判断过程讲给示范者听，让他指出你漏掉或讲错的环节。",
             "duration_min": 10,
             "checkpoint": "完成了口头复述；且被指出的遗漏/错误点被记录",
             "output": "讲解记录与反馈"}
        ],
        "evaluate": {
            "self_check": ["我能说出高手的判断依据，还是只记住了他的动作？",
                        "独立做时卡的地方，和上次一样吗？"],
            "success_criteria": ["独立完成时不再需要提示", "能把判断依据讲给别人听"]
        },
        "agent_contract": {
            "input": ["skill", "expert"], "output": ["示范记录", "尝试记录", "讲解反馈"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：Agent 扮演示范者，用追问代替真人反馈"
        }
    },
    {
        "id": "mental-rehearsal", "name": "心理演练", "name_en": "Mental Rehearsal",
        "category": "技能习得", "evidence": "medium",
        "evidence_refs": [],
        "description": "不动手，只在脑中把整个操作流程完整过一遍，包括每个分支和出错时的应对。",
        "when_to_use": ["动手机会少或成本高", "上台/比赛/演示前", "巩固已学流程"],
        "when_not_to_use": ["从没实际做过的全新流程（脑中演练会建立错误模式）"],
        "params": {
            "type": "object", "required": ["procedure"],
            "properties": {
                "procedure": {"type": "string", "description": "要在脑中演练的具体流程"}
            }
        },
        "steps": [
            {"id": "script", "name": "写出完整流程",
             "instruction": "把流程按顺序写成步骤，含判断分支（如果出现 X 就走 Y）。",
             "duration_min": 10,
             "checkpoint": "步骤数 ≥ 4，且至少含 1 个判断分支",
             "output": "流程脚本"},
            {"id": "visualize", "name": "闭眼过一遍",
             "instruction": "闭眼按脚本在脑中走完全程，想象每个动作和反馈。卡住就记下卡在哪一步。",
             "duration_min": 12,
             "checkpoint": "完成了一次全程演练；卡壳步骤被记录",
             "output": "演练记录"},
            {"id": "branch", "name": "演练出错分支",
             "instruction": "针对每个判断分支，在脑中走一遍「出错时怎么办」的路径。",
             "duration_min": 10,
             "checkpoint": "每个分支的异常处理路径都被演练过；分支数与演练记录条数一致",
             "output": "分支演练记录"},
            {"id": "compare", "name": "实操对照",
             "instruction": "找机会真正做一次，记录与演练不一致的地方，回头修订流程脚本。",
             "duration_min": 15,
             "checkpoint": "完成了一次实操；且列出了与演练不一致之处并给出修订",
             "output": "对照结果与修订", "fail_to": "script"}
        ],
        "evaluate": {
            "self_check": ["我演练的是完整流程，还是只演了顺利的那条路？",
                        "真正做的时候，哪里跟我脑中不一样？"],
            "success_criteria": ["实操时无计划外中断", "流程脚本经实操修订后无遗漏分支"]
        },
        "agent_contract": {
            "input": ["procedure"], "output": ["流程脚本", "演练记录", "对照结果"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：文字化演练，靠自述记录卡点"
        }
    },
    {
        "id": "bisect-debug", "name": "二分定位调试", "name_en": "Bisect Debugging",
        "category": "技能习得", "evidence": "anecdotal",
        "evidence_refs": [],
        "description": "出错时别乱猜，用二分法把范围对半砍，几步就把问题锁到具体位置。",
        "when_to_use": ["报错但看不出原因", "一堆改动后突然坏了", "定位复杂问题"],
        "when_not_to_use": ["错误信息已直接指出位置（直接改即可）"],
        "params": {
            "type": "object", "required": ["problem"],
            "properties": {
                "problem": {"type": "string", "description": "出问题的系统或流程描述"},
                "max_steps": {"type": "integer", "default": 5, "description": "最多二分几轮"}
            }
        },
        "steps": [
            {"id": "bound", "name": "先定问题边界",
             "instruction": "确认「哪里是好的、哪里是坏的」：找到一个正常工作的输入和一个失败的输入。",
             "checkpoint": "存在一组可对比的正常案例与失败案例，且两者差异被写明",
             "output": "边界案例对"},
            {"id": "halve", "name": "对半砍",
             "instruction": "把从正常到失败之间的范围对半切，测中点属于正常还是失败，把范围缩小一半。重复直到范围只剩一处。",
             "duration_min": 20,
             "checkpoint": "每轮范围减半；且每轮都记录了中点的判定结果",
             "output": "二分过程记录"},
            {"id": "confirm", "name": "单点验证",
             "instruction": "对锁定位置单独改动一次，确认问题消失；再改回去确认问题复现。两次都成立才算定位成功。",
             "duration_min": 10,
             "checkpoint": "完成了「改掉→恢复」与「恢复→复现」两次验证；两者结论一致",
             "output": "验证结论"},
            {"id": "record", "name": "记入错题本",
             "instruction": "把「根因 → 判据 → 修法」三行写进错题本，并设定复习时间。",
             "duration_min": 5,
             "checkpoint": "记录含根因、判据、修法三项；且已设定复习时间",
             "output": "错题记录", "fail_to": "halve"}
        ],
        "evaluate": {
            "self_check": ["我是在系统定位，还是在碰运气改？",
                        "改好之后我验证「改回去会再坏」了吗？"],
            "success_criteria": ["定位过程 ≤ max_steps 轮", "同类问题下次能直接认出"]
        },
        "agent_contract": {
            "input": ["problem", "max_steps"], "output": ["边界案例", "二分记录", "验证结论"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：口头引导二分定位，靠提问收窄范围"
        }
    },
    {
        "id": "scaffold-fading", "name": "脚手架渐隐", "name_en": "Scaffold Fading",
        "category": "技能习得", "evidence": "medium",
        "evidence_refs": [],
        "description": "先给足提示和模板把事情做成，然后一轮轮抽掉辅助，最后不留痕迹也能独立做。",
        "when_to_use": ["学新东西总做不出来", "带教/培训场景", "想摆脱对模板的依赖"],
        "when_not_to_use": ["已经能独立完成、只是想提速"],
        "params": {
            "type": "object", "required": ["task"],
            "properties": {
                "task": {"type": "string", "description": "要掌握的具体任务"},
                "rounds": {"type": "integer", "default": 3, "description": "渐隐轮数"}
            }
        },
        "steps": [
            {"id": "full", "name": "第一轮：全模板",
             "instruction": "提供完整模板、步骤与示例，让学习者照着做一遍做出成品。",
             "duration_min": 20,
             "checkpoint": "学习者在全模板辅助下产出了 1 件成品",
             "output": "首轮成品"},
            {"id": "partial", "name": "第二轮：抽掉细节",
             "instruction": "保留步骤框架，隐去具体写法与提示，让学习者补齐空缺部分。",
             "duration_min": 20,
             "checkpoint": "学习者在仅保留框架的情况下补齐了空缺并产出成品",
             "output": "二轮成品"},
            {"id": "bare", "name": "第三轮：只给目标",
             "instruction": "只说明要做什么和验收标准，不给任何模板。让学习者独立完成。",
             "duration_min": 20,
             "checkpoint": "学习者无任何模板辅助下独立完成并通过验收标准",
             "output": "三轮成品", "fail_to": "partial"}
        ],
        "evaluate": {
            "self_check": ["我去掉的是「辅助」，还是把「要求」也一起去掉了？",
                        "不给模板时卡住的地方，是记忆问题还是判断问题？"],
            "success_criteria": ["无模板独立产出且达标", "每轮辅助递减且成品质量不下降"]
        },
        "agent_contract": {
            "input": ["task", "rounds"], "output": ["各轮成品"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：对话式逐步撤除提示"
        }
    },

    # ============================== 计划执行（+3 → 5）==============================
    {
        "id": "timeboxing", "name": "时间盒", "name_en": "Timeboxing",
        "category": "计划执行", "evidence": "anecdotal",
        "evidence_refs": [],
        "description": "给每件事预先定死一段时间，时间一到就停或换，用「时间边界」替代「做完为止」。",
        "when_to_use": ["一件事总拖着做不完", "日程老被一件事挤爆", "想给重要但不紧急的事留时间"],
        "when_not_to_use": ["需要连续心流的深度创作（频繁中断反而伤效率）"],
        "params": {
            "type": "object", "required": ["tasks"],
            "properties": {
                "tasks": {"type": "string", "description": "今天要处理的事，用逗号或换行分隔"},
                "slot_min": {"type": "integer", "default": 45, "description": "单个时间盒时长（分钟）"}
            }
        },
        "steps": [
            {"id": "list", "name": "列事并估时",
             "instruction": "把今天要做的事逐条列出，为每条估计一个时间盒长度（不超过 slot_min 的 2 倍）。",
             "duration_min": 6,
             "checkpoint": "任务清单每条都配了时间盒长度；且单盒长度 ≤ slot_min×2",
             "output": "任务与盒长表"},
            {"id": "place", "name": "排进时间轴",
             "instruction": "把各时间盒按优先级排进当天时间表，盒与盒之间留 10 分钟缓冲。",
             "duration_min": 6,
             "checkpoint": "时间轴上各盒不重叠；且相邻盒之间均留 10 分钟缓冲",
             "output": "当日时间表"},
            {"id": "enforce", "name": "到点就停",
             "instruction": "每个盒结束时立刻停下当前动作，记录「完成了什么 / 卡在哪」。不延长盒子。",
             "duration_min": 3,
             "checkpoint": "每个盒结束时均有完成度与卡点记录；且未出现延长盒子的情况",
             "output": "执行记录"},
            {"id": "adjust", "name": "按实绩调盒长",
             "instruction": "对比估计与实际耗时，把偏差超过 50% 的盒长调整为实测值的 1.2 倍。",
             "duration_min": 5,
             "checkpoint": "列出了偏差 >50% 的条目；并给出按实测×1.2 调整后的新盒长",
             "output": "盒长调整表", "fail_to": "list"}
        ],
        "evaluate": {
            "self_check": ["我停下来了，还是「再五分钟就好」？",
                        "估时偏差集中在哪类事上？"],
            "success_criteria": ["当日时间表完成率 ≥ 70%", "估时偏差逐日收窄"]
        },
        "agent_contract": {
            "input": ["tasks", "slot_min"], "output": ["任务与盒长表", "当日时间表", "执行记录"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：口头排程与提醒"
        }
    },
    {
        "id": "if-then-planning", "name": "执行意图", "name_en": "Implementation Intentions",
        "category": "计划执行", "evidence": "medium",
        "evidence_refs": [],
        "description": "不说「我要多练」，而说「如果到了 X 时地，我就做 Y」，把决心绑到具体触发条件上。",
        "when_to_use": ["总说要做但总没做", "计划写得好却执行不了", "想养成固定习惯"],
        "when_not_to_use": ["需要临场判断的复杂任务（绑定过死会僵化）"],
        "params": {
            "type": "object", "required": ["goal"],
            "properties": {
                "goal": {"type": "string", "description": "想实现的具体行为，如「每天复习 20 分钟」"}
            }
        },
        "steps": [
            {"id": "specify", "name": "把愿望写成动作",
             "instruction": "把目标改成一个可观察的具体动作，含频率与时长。禁止出现「多」「尽量」这类词。",
             "duration_min": 5,
             "checkpoint": "目标被改写为含频率与时长的动作；且不含「多」「尽量」等模糊量词",
             "output": "行为定义"},
            {"id": "trigger", "name": "绑一个触发条件",
             "instruction": "指定一个一定会发生的时地作为触发器，写成「如果[时地]，我就[动作]」。",
             "duration_min": 6,
             "checkpoint": "存在一条「如果…我就…」句式；且触发条件为每日必然出现的时地",
             "output": "执行意图句"},
            {"id": "obstacle", "name": "预设障碍与对策",
             "instruction": "列出 3 个最可能让你不做的障碍，各写一条「如果出现 X，我就改用 Y」。",
             "duration_min": 8,
             "checkpoint": "列出 3 条障碍及对应对策；每条均为「如果出现…我就…」句式",
             "output": "障碍对策表"},
            {"id": "review", "name": "一周后回顾触发率",
             "instruction": "统计这一周触发器出现次数与实际执行次数，算出执行率。低于 60% 就换触发条件。",
             "duration_min": 6,
             "checkpoint": "记录了触发次数、执行次数与执行率；且给出是否更换触发条件的判定",
             "output": "执行率报告", "fail_to": "trigger"}
        ],
        "evaluate": {
            "self_check": ["我的触发条件是「一定会发生」的吗？",
                        "没做到的时候，是忘了还是刻意回避？"],
            "success_criteria": ["周执行率 ≥ 60%", "障碍对策至少用上一次"]
        },
        "agent_contract": {
            "input": ["goal"], "output": ["行为定义", "执行意图句", "障碍对策表"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：对话引导写出 if-then 并口头复盘"
        }
    },
    {
        "id": "distributed-practice", "name": "分散练习", "name_en": "Distributed Practice",
        "category": "计划执行", "evidence": "high",
        "evidence_refs": [REF_CEPEDA, REF_DUNLOSKY],
        "description": "把同样长的学习时间拆成多次，中间隔开；总量不变，但长期保持率明显更高。",
        "when_to_use": ["计划复习节奏", "准备长期考试", "想减少临时抱佛脚"],
        "when_not_to_use": ["明天就考（此时集中练习的即时效果更高）"],
        "params": {
            "type": "object", "required": ["material"],
            "properties": {
                "material": {"type": "string", "description": "要安排练习的材料"},
                "total_min": {"type": "integer", "default": 120, "description": "计划投入的总分钟数"},
                "sessions": {"type": "integer", "default": 4, "description": "拆成几次"}
            }
        },
        "steps": [
            {"id": "budget", "name": "定总时长与次数",
             "instruction": f"把总时长 {120} 分钟拆成 {4} 次，算出每次时长。单次不低于 15 分钟。",
             "duration_min": 4,
             "checkpoint": "给出了每次时长；且单次时长 ≥ 15 分钟，次数×单次 = 总时长",
             "output": "练习预算表"},
            {"id": "schedule", "name": "排到日历上",
             "instruction": "把每次练习排到具体日期与时段，相邻两次至少隔 1 天。",
             "duration_min": 5,
             "checkpoint": "每次练习都有日期与时段；且相邻两次间隔 ≥ 1 天",
             "output": "练习日程"},
            {"id": "log", "name": "每次记录正确率",
             "instruction": "每次练习结束记录正确率与耗时，追加到练习日志。",
             "duration_min": 3,
             "checkpoint": "每次练习都有一行含正确率与耗时的日志",
             "output": "练习日志"},
            {"id": "tune", "name": "按曲线调间隔",
             "instruction": "看正确率走势：连续两次 ≥85% 就把间隔拉长 1.5 倍；出现 <60% 就缩短一半。",
             "duration_min": 5,
             "checkpoint": "给出了基于最近正确率的间隔调整结论；且调整方向符合规则",
             "output": "间隔调整方案", "fail_to": "schedule"}
        ],
        "evaluate": {
            "self_check": ["我是真的分次练了，还是攒到最后一次？",
                        "间隔是根据我的正确率调的还是拍脑袋定的？"],
            "success_criteria": ["练习次数达到计划值", "末次正确率高于首次"]
        },
        "agent_contract": {
            "input": ["material", "total_min", "sessions"],
            "output": ["练习预算表", "练习日程", "练习日志"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：口头排程与记录"
        }
    },

    # ============================== 元认知（+3 → 6）==============================
    {
        "id": "calibration-training", "name": "校准训练", "name_en": "Calibration Training",
        "category": "元认知", "evidence": "medium",
        "evidence_refs": [],
        "description": "每次做题前先预测「我能对几成」，做完再对账，把「自我感觉」校准到接近真实水平。",
        "when_to_use": ["常觉得会了但考砸", "估不准自己的水平", "备考自我诊断"],
        "when_not_to_use": ["完全陌生的领域（没有可参照的判断基准）"],
        "params": {
            "type": "object", "required": ["task"],
            "properties": {
                "task": {"type": "string", "description": "要做的一组题目或任务"},
                "count": {"type": "integer", "default": 10, "description": "题目或任务数量"}
            }
        },
        "steps": [
            {"id": "predict", "name": "做之前先预测",
             "instruction": "在开始前写下预测正确率（百分比）与预计耗时。必须先于作答完成。",
             "duration_min": 3,
             "checkpoint": "存在作答前记录的预测正确率与预计耗时两个数值",
             "output": "预测记录"},
            {"id": "perform", "name": "正常完成",
             "instruction": "按常规完成全部题目，记录实际正确率与实际耗时。",
             "duration_min": 25,
             "checkpoint": "存在实际正确率与实际耗时两个数值",
             "output": "实际记录"},
            {"id": "compare", "name": "算偏差",
             "instruction": "计算预测与实际正确率的差值、预计与实际耗时的差值。逐题标注哪些是「以为会其实错」。",
             "duration_min": 6,
             "checkpoint": "给出了两类差值；且列出了「以为会其实错」的条目",
             "output": "偏差报告"},
            {"id": "recalibrate", "name": "修正下一次预测",
             "instruction": "根据偏差方向，写明下次预测要上调还是下调及幅度，作为下一轮的预测基准。",
             "duration_min": 4,
             "checkpoint": "给出了下轮预测的方向与幅度；且幅度与本次偏差同量级",
             "output": "校准策略", "fail_to": "predict"}
        ],
        "evaluate": {
            "self_check": ["我预测时是凭感觉还是有依据？",
                        "偏差是系统性偏高还是忽高忽低？"],
            "success_criteria": ["预测与实际正确率差值 ≤ 15 个百分点", "漏判的「以为会」条目减少"]
        },
        "agent_contract": {
            "input": ["task", "count"], "output": ["预测记录", "实际记录", "偏差报告", "校准策略"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：口头预测与对账"
        }
    },
    {
        "id": "metacognitive-monitor", "name": "学习判断监控", "name_en": "Judgment of Learning",
        "category": "元认知", "evidence": "medium",
        "evidence_refs": [],
        "description": "学完每一小段就问自己「我等下能想起来吗」，并当场打分，用即时判断替代事后错觉。",
        "when_to_use": ["读完感觉都懂", "复习时不知从哪下手", "分配有限的学习时间"],
        "when_not_to_use": ["材料本身极短或极简单"],
        "params": {
            "type": "object", "required": ["material"],
            "properties": {
                "material": {"type": "string", "description": "要分段判断的材料"}
            }
        },
        "steps": [
            {"id": "split", "name": "切成小段",
             "instruction": "把材料切成 5-8 个小段，每段一个完整意思。",
             "duration_min": 5,
             "checkpoint": "段数在 5-8 之间，且每段表达一个完整意思",
             "output": "分段清单"},
            {"id": "judge", "name": "逐段打回忆把握分",
             "instruction": "学完每段立刻打 0-100 的「等下能想起来的把握」分。不回看、不修改。",
             "duration_min": 12,
             "checkpoint": "每段都有 0-100 的把握分；且打分在学完该段后立即完成",
             "output": "把握分清单"},
            {"id": "test", "name": "实际回忆检验",
             "instruction": "全部学完后，不看书逐段回忆，记录能想起的段落。",
             "duration_min": 12,
             "checkpoint": "逐段记录了能/不能想起；且回忆过程未查阅原文",
             "output": "回忆结果"},
            {"id": "contrast", "name": "对比把握与实绩",
             "instruction": "逐段对比把握分与实际结果，标出「高把握但没想起」的段落——这些是优先复习对象。",
             "duration_min": 6,
             "checkpoint": "列出了「高把握但没想起」的段落；且这些段落被标为优先复习",
             "output": "优先复习清单", "fail_to": "judge"}
        ],
        "evaluate": {
            "self_check": ["我的把握分是学完立刻打的，还是回忆之后补的？",
                        "哪些段落我自信但没想起来？"],
            "success_criteria": ["高把握段落的实绩回忆率 ≥ 80%", "优先清单逐轮缩短"]
        },
        "agent_contract": {
            "input": ["material"], "output": ["分段清单", "把握分清单", "回忆结果", "优先清单"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：口头打分与回忆检验"
        }
    },
    {
        "id": "pretesting", "name": "预测试效应", "name_en": "Pretesting Effect",
        "category": "元认知", "evidence": "high",
        "evidence_refs": [REF_PAN, REF_ROEDIGER],
        "description": "学之前先硬猜一遍，哪怕全错也行；猜错会让后面正式学时印象更深。",
        "when_to_use": ["开始学新章节前", "发现学了记不住", "想提高听课效率"],
        "when_not_to_use": ["需要精确记忆的少量事实（猜错可能形成干扰）"],
        "params": {
            "type": "object", "required": ["topic"],
            "properties": {
                "topic": {"type": "string", "description": "即将学习的新主题"},
                "questions": {"type": "integer", "default": 6, "description": "预测试题量"}
            }
        },
        "steps": [
            {"id": "guess", "name": "先猜，不看资料",
             "instruction": "让 Agent 就这个主题提问，你直接猜答案。不会也必须猜一个。此时严禁查看任何资料。",
             "duration_min": 10,
             "checkpoint": "每道题都有猜测答案（含明确写「不会」的条目）；且猜题期间未查资料",
             "output": "猜测记录"},
            {"id": "study", "name": "正式学习",
             "instruction": "现在才打开材料学习，重点看与自己猜测不一致的地方。",
             "duration_min": 25,
             "checkpoint": "学习完成；且已标注出与猜测不一致的关键点",
             "output": "学习记录与差异点"},
            {"id": "retest", "name": "重测对比",
             "instruction": "重新回答预测试的问题，统计「猜错但这次答对」的比例——这部分就是预测试带来的增益。",
             "duration_min": 10,
             "checkpoint": "给出了「猜错→答对」的条目数与占比",
             "output": "重测对比结果"},
            {"id": "consolidate", "name": "只巩固增益项",
             "instruction": "把「猜错且这次仍错」的条目单独拉出来重点攻，其余快速过一遍。",
             "duration_min": 10,
             "checkpoint": "列出了「仍错」条目并给出针对动作；其余条目被快速回顾",
             "output": "巩固结果", "fail_to": "study"}
        ],
        "evaluate": {
            "self_check": ["我猜的时候是真动脑了吗，还是随便填的？",
                        "猜错的地方，这次真记住了吗？"],
            "success_criteria": ["「猜错→答对」占比 ≥ 50%", "「仍错」条目逐轮减少"]
        },
        "agent_contract": {
            "input": ["topic", "questions"], "output": ["猜测记录", "学习差异点", "重测对比"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无工具时：对话式提问与猜测，不联网检索答案"
        }
    },

    # ============================== 协作学习（+2 → 3）==============================
    {
        "id": "teach-back-circle", "name": "互讲圈", "name_en": "Teach-Back Circle",
        "category": "协作学习", "evidence": "medium",
        "evidence_refs": [],
        "description": "几个人轮流讲同一个知识点，每人讲完由其他人复述并挑错，靠同伴的压力把盲区挤出来。",
        "when_to_use": ["小组复习备考", "团队知识对齐", "自己讲容易自我欺骗时"],
        "when_not_to_use": ["独自学习或时间极紧"],
        "params": {
            "type": "object", "required": ["topic"],
            "properties": {
                "topic": {"type": "string", "description": "本轮要互讲的知识点"},
                "people": {"type": "integer", "default": 3, "description": "参与人数"}
            }
        },
        "steps": [
            {"id": "teach", "name": "一人主讲",
             "instruction": "指定一人主讲该知识点，其他人只听不打断，记录听不懂的地方。",
             "duration_min": 12,
             "checkpoint": "主讲完成；且听众记录了听不懂处",
             "output": "讲解与疑问清单"},
            {"id": "echo", "name": "听众复述",
             "instruction": "由一名听众不看任何资料复述刚才的内容，主讲不得提示。",
             "duration_min": 6,
             "checkpoint": "复述完成；且复述期间主讲未给提示",
             "output": "复述记录"},
            {"id": "challenge", "name": "集体挑错",
             "instruction": "所有人指出复述里遗漏或说错的地方，逐条记下。只记录事实偏差，不争论措辞。",
             "duration_min": 8,
             "checkpoint": "列出了遗漏/错误条目；且每条为可核对的事实偏差",
             "output": "错题清单"},
            {"id": "rotate", "name": "换人重讲",
             "instruction": "换下一个人主讲同一知识点，重点补上刚才的错题清单。讲完再复盘一次。",
             "duration_min": 12,
             "checkpoint": "换人后重讲覆盖了错题清单；且复盘给出了剩余问题",
             "output": "二轮讲解与复盘", "fail_to": "echo"}
        ],
        "evaluate": {
            "self_check": ["我挑出来的错是事实偏差，还是只是说法不同？",
                        "换人讲之后，第一轮的问题真的解决了吗？"],
            "success_criteria": ["二轮复述遗漏数少于首轮", "同一盲区不再复现"]
        },
        "agent_contract": {
            "input": ["topic", "people"], "output": ["讲解记录", "复述记录", "错题清单"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "单人时：让 Agent 扮演听众，负责复述与挑错"
        }
    },
    {
        "id": "peer-review-loop", "name": "同伴互评", "name_en": "Peer Review Loop",
        "category": "协作学习", "evidence": "medium",
        "evidence_refs": [],
        "description": "互相按同一份评分表批改对方的作品，写清楚扣分依据；批改别人的过程反过来提升自己的判断力。",
        "when_to_use": ["写作或代码需要外部视角", "小组作业互评", "想练出评审眼光"],
        "when_not_to_use": ["作品涉密或不宜示人"],
        "params": {
            "type": "object", "required": ["work"],
            "properties": {
                "work": {"type": "string", "description": "待互评的作品"},
                "criteria": {"type": "integer", "default": 4, "description": "评分维度数量"}
            }
        },
        "steps": [
            {"id": "rubric", "name": "先统一评分表",
             "instruction": f"共同确定 {4} 个评分维度及各自的合格标准，写成一页量规。评分前必须完成。",
             "duration_min": 10,
             "checkpoint": "量规含指定数量维度；且每维有可核对的合格标准",
             "output": "共用量规"},
            {"id": "review", "name": "各自独立批改",
             "instruction": "每人按量规给对方作品打分，每条扣分必须写明对应作品的具体位置。",
             "duration_min": 20,
             "checkpoint": "每位参与者都有评分记录；且每条扣分附了作品位置引用",
             "output": "评分记录"},
            {"id": "compare", "name": "对差异项讨论",
             "instruction": "把两人评分不一致的项挑出来逐条讨论，直到对量规理解一致。",
             "duration_min": 12,
             "checkpoint": "列出了不一致项；且每项给出了统一后的判定",
             "output": "差异讨论结论"},
            {"id": "revise", "name": "按反馈改稿",
             "instruction": "作者按收到的反馈逐条修改，标注改了哪里、为什么这么改。",
             "duration_min": 20,
             "checkpoint": "每条反馈都有对应修改；且修改处注明了理由",
             "output": "修订稿", "fail_to": "review"}
        ],
        "evaluate": {
            "self_check": ["我的扣分能指出具体位置吗？",
                        "评分不一致时，是量规模糊还是我理解偏了？"],
            "success_criteria": ["两人评分差 ≤ 1 分（总分制）", "反馈条目均被处理"]
        },
        "agent_contract": {
            "input": ["work", "criteria"], "output": ["评分记录", "差异结论", "修订稿"],
            "side_effects": ["仅写本地文件"],
            "degrade_to": "无人互评时：Agent 按量规逐条批注并说明依据"
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
            "metadata": {"created_at": "2026-10-21", "updated_at": "2026-10-21",
                         "contributors": []},
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
            f.write("\n")
        created.append(s["id"])

    print(f"新增 {len(created)} 个：")
    for c in created:
        print("  +", c)
    if skipped:
        print(f"\n跳过 {len(skipped)} 个（已存在）：{', '.join(skipped)}")
    print(f"\n当前总数：{len([f for f in os.listdir(OUT) if f.endswith('.json') and not f.startswith('_')])}")


if __name__ == "__main__":
    main()