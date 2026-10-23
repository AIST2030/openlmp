#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# Copyright (c) 2026 AIST2030（贵州省团之家智付科技有限公司）
#
# 本文件以木兰宽松许可证 v2（MulanPSL-2.0）释出，许可全文见仓库
# licenses/MulanPSL-2.0.txt（http://license.coscl.org.cn/MulanPSL2）。
# 您可依据该许可证条款复制、使用、修改、分发本文件；分发时必须随附
# 许可证副本并保留本声明。本文件按「原样」提供，不带任何明示或默示担保。
#
# 注意：skills/、business/skills/、registry/ 中的方法内容为 CC0-1.0 公共
# 领域贡献，详见根目录 LICENSE 分层说明；「OpenLMP」商标不在任何许可证
# 授权范围内（木兰 v2 第 3 条 / CC0 均不授予商标权）。
# ---------------------------------------------------------------------------

# -*- coding: utf-8 -*-
"""
OpenLMP 第三批：78 → 98（新增 20 个）。
= METHOD-UNIVERSE 🔵候选中「非商业」的学习方法 14 个 + 思维方法 6 个。
分析方法 9 个见 expand_to_107.py；商业框架进 business/ 子库。
每个都与已收录 Skill 做了差异化（见各 description 的定位），避免重复造轮子。
硬约束同前；思维方法为本次新增分类（已扩 schema）。
"""
import json, os, sys, datetime

OUT = sys.argv[1] if len(sys.argv) > 1 else "E:/视频创作/AIST2030/openlmp/skills"
TODAY = datetime.date.today().isoformat()

NEW = [
    # ============================== 学习方法：知识管理（+3）==============================
    {
        "id": "sq4r", "name": "SQ4R 阅读法", "name_en": "SQ4R Reading",
        "category": "知识管理", "evidence": "medium", "evidence_refs": [],
        "description": "在 SQ3R 五步之外，插入一步反思：把新内容和已知或其它学科显式关联，让阅读从接收变成织网。",
        "when_to_use": ["精读教材想比 SQ3R 更进一步", "知识碎片化连不起来", "跨学科阅读"],
        "when_not_to_use": ["只需检索信息的泛读（六步太重）"],
        "params": {
            "type": "object", "required": ["material"],
            "properties": {"material": {"type": "string", "description": "要精读的一章或一节材料"}}
        },
        "steps": [
            {"id": "survey", "name": "浏览搭骨架", "duration_min": 5,
             "instruction": "读标题、小结、图表，用一句话写出本节要解决的核心问题。",
             "checkpoint": "写下了一句核心问题；且列出了本节的主要小标题",
             "output": "骨架与核心问题"},
            {"id": "question", "name": "把标题变问题", "duration_min": 5,
             "instruction": "把每个小标题改写成一个是非问句，作为阅读时要回答的问题。",
             "checkpoint": "每个小标题都被改写为一个问句",
             "output": "问题清单"},
            {"id": "read", "name": "带着问题读", "duration_min": 20,
             "instruction": "逐段读，边读边在问题旁记下答案要点，读不懂的段落标记待回看。",
             "checkpoint": "每个问题都有对应答案要点；且读不懂处被标记",
             "output": "带答案的问题清单"},
            {"id": "recite", "name": "合书复述", "duration_min": 8,
             "instruction": "合上材料，凭记忆口述每问的答案，卡住的标记后重点回看。",
             "checkpoint": "每问都完成了一次合书复述；卡住处被标记",
             "output": "复述记录"},
            {"id": "reflect", "name": "反思关联（第四 R）", "duration_min": 8,
             "instruction": "为每个要点写一条它和已知知识或其它学科的联系；写不出联系的标注为孤立点。",
             "checkpoint": "每个要点都有至少一条关联；孤立点被单独标出",
             "output": "关联表与孤立点清单"},
            {"id": "review", "name": "隔期复习", "duration_min": 6,
             "instruction": "隔一天只看问题清单重答，重点补上一轮标记的卡壳与孤立点。",
             "checkpoint": "问题清单被重新作答；卡壳与孤立点被优先处理",
             "output": "复习结果", "fail_to": "recite"}
        ],
        "evaluate": {
            "self_check": ["我比 SQ3R 多做的反思，是真关联还是硬凑？", "孤立点我打算怎么补？"],
            "success_criteria": ["多数要点能说出一条关联", "隔期重答卡壳减少"]
        },
        "agent_contract": {
            "input": ["material"], "output": ["问题清单", "关联表", "复习结果"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面完成六步"
        }
    },
    {
        "id": "two-column-notes", "name": "二等分笔记法", "name_en": "Two-Column Notes",
        "category": "知识管理", "evidence": "anecdotal", "evidence_refs": [],
        "description": "把纸面一分为二：右栏照记、左栏只做加工（压缩成关键词或提问），逼自己把抄录变成再处理，是康奈尔等法的通用底座。",
        "when_to_use": ["笔记越记越像抄书", "想给笔记加一道加工工序", "作为康奈尔/卢曼前的通用训练"],
        "when_not_to_use": ["只需原样留存的会议记录（左栏加工反而添乱）"],
        "params": {
            "type": "object", "required": ["topic"],
            "properties": {"topic": {"type": "string", "description": "本次笔记主题"}}
        },
        "steps": [
            {"id": "rule", "name": "定两栏规则", "duration_min": 3,
             "instruction": "把纸竖分为左右两栏，规定右栏照记原内容、左栏只写关键词或对右栏的提问，先写下规则。",
             "checkpoint": "写明了左右栏各自规则；且左栏限定为关键词或提问",
             "output": "分栏规则"},
            {"id": "record", "name": "右栏照记", "duration_min": 18,
             "instruction": "在右栏如实记录听到或读到的内容，不做加工；数量不限。",
             "checkpoint": "右栏有完整记录；且右栏未混入加工内容",
             "output": "右栏原始记录"},
            {"id": "process", "name": "左栏加工", "duration_min": 12,
             "instruction": "针对右栏每条，在左栏写一个关键词或一个能考住自己的问题；不许照抄右栏原句。",
             "checkpoint": "每条右栏内容都有左栏对应；且左栏无照抄右栏的原句",
             "output": "左栏加工"},
            {"id": "cover", "name": "盖右栏自测", "duration_min": 8,
             "instruction": "盖住右栏，只看左栏关键词或问题复述原内容，复述不出的回看并加粗该条左栏提示。",
             "checkpoint": "完成了盖栏复述；且复述失败处被加粗标记",
             "output": "自测结果", "fail_to": "process"}
        ],
        "evaluate": {
            "self_check": ["左栏我是真在加工，还是在换种方式抄？", "盖栏后我能还原右栏吗？"],
            "success_criteria": ["左栏全部为关键词或问题", "盖栏复述成功率高于无左栏时"]
        },
        "agent_contract": {
            "input": ["topic"], "output": ["左栏加工", "自测结果"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸上分两栏记录并盖栏自测"
        }
    },
    {
        "id": "qa-notes", "name": "一问一答笔记", "name_en": "Q&A Notes",
        "category": "知识管理", "evidence": "anecdotal", "evidence_refs": [],
        "description": "把所有笔记一律记成问答对：左写问题、右写答案，让笔记天然可自测，复习时盖住答案即可检索练习。",
        "when_to_use": ["笔记是陈述句堆叠、没法自测", "想把复习直接变成主动回忆", "备考整理"],
        "when_not_to_use": ["记录操作流程或清单（用条目式更清晰）"],
        "params": {
            "type": "object", "required": ["topic"],
            "properties": {"topic": {"type": "string", "description": "要整理成问答的主题"}}
        },
        "steps": [
            {"id": "extract", "name": "抽取知识点", "duration_min": 8,
             "instruction": "把原始材料里的知识点逐条抽出来，每条应是可独立提问的一个点。",
             "checkpoint": "抽出的知识点至少 8 条；且每条可独立成问",
             "output": "知识点清单"},
            {"id": "author", "name": "改写成问答对", "duration_min": 12,
             "instruction": "把每个知识点改写成一个问题加一个答案，答案要完整到能单独看懂，问题要能考住自己。",
             "checkpoint": "每条知识点都有配对的问与答；且问题具备可考性",
             "output": "问答对笔记"},
            {"id": "quiz", "name": "盖答案自测", "duration_min": 10,
             "instruction": "盖住答案列，只看问题逐条作答，再对照答案标注对错。",
             "checkpoint": "每条问题都被作答并对照；且对错被标注",
             "output": "自测记录"},
            {"id": "fix", "name": "只补错题", "duration_min": 8,
             "instruction": "把答错的问答对改写得更易记或拆成更小的问题，答对的本轮不再占用时间。",
             "checkpoint": "答错问答对已被改写或拆分；答对项本轮未重复占用时间",
             "output": "修订后的问答对", "fail_to": "quiz"}
        ],
        "evaluate": {
            "self_check": ["我的问题是真能考住人，还是答案的复述？", "盖答案时我是真在想，还是在默背答案句？"],
            "success_criteria": ["盖答案自测正确率逐步上升", "问答对可脱离原材料独立使用"]
        },
        "agent_contract": {
            "input": ["topic"], "output": ["问答对笔记", "自测记录"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸上左问右答并盖答案自测"
        }
    },
    # ============================== 学习方法：记忆巩固（+3）==============================
    {
        "id": "tree-memory", "name": "树状图记忆法", "name_en": "Tree-Diagram Memory",
        "category": "记忆巩固", "evidence": "anecdotal", "evidence_refs": [],
        "description": "按含义的包含关系把知识组织成一棵层级树，从上位到下位逐层默背，用结构顺序代替零散死记。",
        "when_to_use": ["知识有清晰层级，如分类体系", "一堆并列名词记不住", "想把零散点挂到结构上"],
        "when_not_to_use": ["知识是网络关系而非层级（用概念图更合适）"],
        "params": {
            "type": "object", "required": ["scope"],
            "properties": {"scope": {"type": "string", "description": "要组织成树的知识范围"}}
        },
        "steps": [
            {"id": "root", "name": "定树根与主干", "duration_min": 6,
             "instruction": "确定最上位概念作树根，向下分出若干主干，每个主干是该根下的一个大类。",
             "checkpoint": "树根唯一明确；且主干至少 3 个",
             "output": "树根与主干"},
            {"id": "branch", "name": "逐层分到叶", "duration_min": 15,
             "instruction": "每个主干继续按包含关系向下分，直到分到最小可记单元；同层按同一标准划分。",
             "checkpoint": "每个主干都分到了叶节点；且同层按同一标准划分",
             "output": "完整层级树"},
            {"id": "climb", "name": "逐层默背", "duration_min": 10,
             "instruction": "从树根开始逐层默背，盖住某层复述其下所有子项，卡住的枝标记。",
             "checkpoint": "每层都完成了一次盖层复述；卡住的枝被标记",
             "output": "默背记录"},
            {"id": "repair", "name": "只补断枝", "duration_min": 8,
             "instruction": "只重背标记的断枝及其到根的路径，其余不动；隔日重测整棵树。",
             "checkpoint": "仅断枝被重背；且安排了隔日整树重测",
             "output": "补背结果", "fail_to": "climb"}
        ],
        "evaluate": {
            "self_check": ["我的分层是按包含关系，还是随便归类？", "盖层后我能从上位推出下位吗？"],
            "success_criteria": ["整棵树可逐层复述", "断枝经补背后减少"]
        },
        "agent_contract": {
            "input": ["scope"], "output": ["层级树", "补背结果"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸上画树并逐层默背"
        }
    },
    {
        "id": "emotion-anchoring", "name": "情绪联动记忆", "name_en": "Emotion Anchoring",
        "category": "记忆巩固", "evidence": "anecdotal", "evidence_refs": [],
        "description": "把要记的内容主动绑到一个带情绪的个人场景上，用情绪强度给记忆加挂钉，事后靠场景回捞内容。",
        "when_to_use": ["记枯燥的清单或术语", "需要长期记住的少量关键信息", "常规方法记不牢时"],
        "when_not_to_use": ["需精确复述的法律条文或数据（情绪联想易引入偏差）"],
        "params": {
            "type": "object", "required": ["items"],
            "properties": {"items": {"type": "string", "description": "要记的内容清单"}}
        },
        "steps": [
            {"id": "pick", "name": "选锚点场景", "duration_min": 5,
             "instruction": "回忆几个自己情绪强烈的真实场景，如某次惊喜、尴尬、紧张，各起一个名字备用。",
             "checkpoint": "列出了至少 3 个带情绪的锚点场景；且每个有名字",
             "output": "锚点场景库"},
            {"id": "bind", "name": "逐条绑定", "duration_min": 12,
             "instruction": "把每条内容塞进一个锚点场景，写成一句这个场景里发生了什么、如何体现该内容。",
             "checkpoint": "每条内容都绑定到一个场景；且写出了场景与内容的关联句",
             "output": "绑定清单"},
            {"id": "recall", "name": "靠场景回捞", "duration_min": 8,
             "instruction": "只看锚点场景名，回捞对应内容；回捞不出的条目重绑到更强的场景。",
             "checkpoint": "每个场景都完成了一次回捞；回捞失败项被重绑",
             "output": "回捞记录"},
            {"id": "decay", "name": "隔时重测", "duration_min": 6,
             "instruction": "隔一两天重测，统计仍靠场景才想起的条目，逐步练习脱离场景直接回忆。",
             "checkpoint": "完成了隔时重测；且记录了脱离场景可直接回忆的比例",
             "output": "重测结果", "fail_to": "bind"}
        ],
        "evaluate": {
            "self_check": ["我绑的场景是真有情绪，还是硬编的？", "我是在靠场景回捞，还是直接记住了内容？"],
            "success_criteria": ["初期靠场景回捞成功率高于无锚点时", "逐步提高脱离场景直接回忆的比例"]
        },
        "agent_contract": {
            "input": ["items"], "output": ["绑定清单", "回捞记录"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：口头编场景并复述"
        }
    },
    {
        "id": "backstitch-review", "name": "回针缝复习", "name_en": "Backstitch Review",
        "category": "记忆巩固", "evidence": "anecdotal", "evidence_refs": [],
        "description": "像回针缝一样，每学新的一段就回头缝一针复习前面，边前进边回缝，让旧内容不脱线。",
        "when_to_use": ["连续学多章，前面开始忘", "长课程或长文阅读", "想边学边保温"],
        "when_not_to_use": ["章节相互独立、无需前后关联时（单独安排复习更省）"],
        "params": {
            "type": "object", "required": ["scope"],
            "properties": {"scope": {"type": "string", "description": "要连续推进的学习范围"}}
        },
        "steps": [
            {"id": "segment", "name": "切成针脚段", "duration_min": 4,
             "instruction": "把范围切成若干小段，每段是一个针脚；定下每学完一段就回缝前几段的规则。",
             "checkpoint": "范围被切成至少 5 段；且写明了回缝规则",
             "output": "分段与回缝规则"},
            {"id": "advance", "name": "学新段", "duration_min": 20,
             "instruction": "按顺序学当前这一段，学完在本段末尾写下三句话要点。",
             "checkpoint": "当前段已学完；且写下了三句话要点",
             "output": "本段要点"},
            {"id": "backstitch", "name": "回缝前几段", "duration_min": 8,
             "instruction": "不看书，只凭记忆复述前两段的要点，卡住的标注；然后才继续下一段。",
             "checkpoint": "前两段要点被复述；且卡住处被标注",
             "output": "回缝记录"},
            {"id": "tighten", "name": "锁紧断线段", "duration_min": 6,
             "instruction": "每完成 5 段，把所有标注过的断线段集中重缝一遍，再继续前进。",
             "checkpoint": "每 5 段后集中重缝一次；且重缝覆盖了全部标注段",
             "output": "重缝结果", "fail_to": "backstitch"}
        ],
        "evaluate": {
            "self_check": ["我是真在回缝，还是只顾往前赶？", "回缝时卡住的，是当时没懂还是真忘了？"],
            "success_criteria": ["回缝复述成功率随针脚保持稳定", "断线段经重缝后减少"]
        },
        "agent_contract": {
            "input": ["scope"], "output": ["本段要点", "回缝记录"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：每段末尾默述前两段要点"
        }
    },
    # ============================== 学习方法：评测验证（+2）==============================
    {
        "id": "pen-not-erasable", "name": "圆珠笔学习法", "name_en": "Non-Erasable Pen Method",
        "category": "评测验证", "evidence": "anecdotal", "evidence_refs": [],
        "description": "用不能擦的笔作答和订正，让错误痕迹留在纸上，复盘时按出错密度定位薄弱，而不是一擦了之。",
        "when_to_use": ["习惯一错就擦、看不到自己错在哪", "想积累个人错误样本", "复盘缺数据"],
        "when_not_to_use": ["正式考试或需整洁提交的场合"],
        "params": {
            "type": "object", "required": [],
            "properties": {"topic": {"type": "string", "default": "", "description": "本次练习范围"}}
        },
        "steps": [
            {"id": "setup", "name": "换不可擦笔", "duration_min": 2,
             "instruction": "练习一律改用不能擦的笔；提前约定错误用划线保留、不改写，只在其后补正。",
             "checkpoint": "确认使用不可擦笔；且写明了错误保留与补正规则",
             "output": "工具与规则"},
            {"id": "answer", "name": "留痕作答", "duration_min": 20,
             "instruction": "正常作答，错了不擦，用单线划掉错误部分并在旁边写正解，保留原始错误可见。",
             "checkpoint": "错误处被划掉而非擦除；且每处错误旁有补正",
             "output": "带痕迹的作答"},
            {"id": "tally", "name": "统计出错密度", "duration_min": 6,
             "instruction": "数出每类错误的划改次数，标出次数最多的错误类型和对应知识点。",
             "checkpoint": "给出了各类错误次数；且标出了最高频错误类型",
             "output": "出错密度表"},
            {"id": "target", "name": "只攻最高频", "duration_min": 12,
             "instruction": "针对最高频错误类型专项重练，重练仍错继续划线保留；其余类型本轮不动。",
             "checkpoint": "仅最高频错误类型被专项重练；且重练错误仍被保留",
             "output": "专项结果", "fail_to": "answer"}
        ],
        "evaluate": {
            "self_check": ["我是不是又在找橡皮？", "出错密度最高的，是真不会还是粗心？"],
            "success_criteria": ["同类错误划改次数逐轮下降", "能据痕迹定位个人薄弱知识点"]
        },
        "agent_contract": {
            "input": ["topic"], "output": ["出错密度表", "专项结果"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：任何不可擦笔均可执行"
        }
    },
    {
        "id": "write-to-recall", "name": "书写记忆检查", "name_en": "Write-to-Recall Check",
        "category": "评测验证", "evidence": "anecdotal", "evidence_refs": [],
        "description": "就一个主题把脑子里能想到的全部倾泻到纸上，用还原完整度衡量记住多少，专抓'只记得一半'的模糊点。",
        "when_to_use": ["想知道对一个主题到底记得全不全", "感觉会但一写就缺", "考前查漏"],
        "when_not_to_use": ["第一次学的新主题（先学再检查）"],
        "params": {
            "type": "object", "required": ["topic"],
            "properties": {"topic": {"type": "string", "description": "要检查还原度的主题"}}
        },
        "steps": [
            {"id": "dump", "name": "限时倾泻", "duration_min": 10,
             "instruction": "就主题在不看资料的情况下，把能想到的全部写到纸上，包括不确定的，不组织语言只求倒空。",
             "checkpoint": "在限定时间内产出倾泻稿；且包含标注为不确定的条目",
             "output": "倾泻稿"},
            {"id": "recover", "name": "对照算还原度", "duration_min": 6,
             "instruction": "对照原始材料，标出倾泻稿覆盖了哪些要点、漏了哪些，算出还原比例。",
             "checkpoint": "给出了还原比例数值；且漏点被逐条列出",
             "output": "还原度与漏点"},
            {"id": "patch", "name": "补漏并复述", "duration_min": 8,
             "instruction": "只补遗漏要点，补完再倾泻一次，看还原比例是否上升。",
             "checkpoint": "遗漏要点被补齐；且完成了第二次倾泻并对比比例",
             "output": "复测结果", "fail_to": "dump"}
        ],
        "evaluate": {
            "self_check": ["我倒得够空吗，还是组织得太好漏了边角？", "还原度低，是没学全还是想不起来？"],
            "success_criteria": ["第二次还原比例高于第一次", "漏点被定位到具体内容"]
        },
        "agent_contract": {
            "input": ["topic"], "output": ["还原度与漏点", "复测结果"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸上倾泻并对照原材料"
        }
    },
    # ============================== 学习方法：计划执行（+3）==============================
    {
        "id": "gantt-progress", "name": "甘特进度法", "name_en": "Gantt Progress Tracking",
        "category": "计划执行", "evidence": "anecdotal", "evidence_refs": [],
        "description": "把计划画成甘特图并按完成百分比着色，用视觉进度替代'感觉在推进'，滞后一眼可见。",
        "when_to_use": ["多任务并行难掌握度", "计划总是虎头蛇尾", "想量化进度"],
        "when_not_to_use": ["只有一两个任务的简单待办（列清单即可）"],
        "params": {
            "type": "object", "required": ["tasks"],
            "properties": {"tasks": {"type": "string", "description": "要排期的任务及起止"}}
        },
        "steps": [
            {"id": "bar", "name": "画甘特条", "duration_min": 10,
             "instruction": "把每个任务按起止时间画成横条，横轴为时间，纵轴为任务。",
             "checkpoint": "每个任务都有一条含起止的横条；且横轴时间刻度一致",
             "output": "甘特图"},
            {"id": "shade", "name": "按百分比着色", "duration_min": 5,
             "instruction": "每周给每条按真实完成度着色一段，写下完成百分比，不凭感觉估。",
             "checkpoint": "每条都有本周着色段与百分比；且百分比有据可依",
             "output": "进度甘特图"},
            {"id": "lag", "name": "标滞后条", "duration_min": 5,
             "instruction": "对照计划与实际着色，标出落后于时间轴的条，算出滞后天数。",
             "checkpoint": "落后条被标出；且每条给出了滞后天数",
             "output": "滞后清单"},
            {"id": "rebalance", "name": "只调整最滞后条", "duration_min": 8,
             "instruction": "对滞后最严重的任务做增援或改期，只动它不动全局；下周复看是否追上。",
             "checkpoint": "仅最滞后任务被调整；且记录了下周复看安排",
             "output": "调整记录", "fail_to": "shade"}
        ],
        "evaluate": {
            "self_check": ["百分比是有据的，还是拍脑袋？", "我是不是只更新好看的那些条？"],
            "success_criteria": ["滞后条数量逐周下降", "计划整体按期完成率上升"]
        },
        "agent_contract": {
            "input": ["tasks"], "output": ["进度甘特图", "滞后清单"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸笔画横条并每周着色"
        }
    },
    {
        "id": "effort-outcome-matrix", "name": "努力分解矩阵", "name_en": "Effort-Outcome Matrix",
        "category": "元认知", "evidence": "anecdotal", "evidence_refs": [],
        "description": "把各项努力按'投入高低×结果好坏'分进四象限，对高投入低结果的止损、对低投入高结果的加码。",
        "when_to_use": ["很努力却不见成效", "想裁掉低效努力", "资源重新分配"],
        "when_not_to_use": ["刚起步尚无结果数据可判时"],
        "params": {
            "type": "object", "required": ["efforts"],
            "properties": {"efforts": {"type": "string", "description": "要评估的若干努力项"}}
        },
        "steps": [
            {"id": "list", "name": "列努力项并打分", "duration_min": 8,
             "instruction": "列出近期的努力项，每项按投入高低和结果好坏各评高或低，各附一条事实依据。",
             "checkpoint": "努力项至少 4 个；且每项有投入、结果两级判断及事实依据",
             "output": "打分表"},
            {"id": "place", "name": "填入四象限", "duration_min": 5,
             "instruction": "按投入和结果把每项放入四象限：高投高果、高投低果、低投高果、低投低果。",
             "checkpoint": "每个努力项都归入唯一象限；且象限划分无重叠",
             "output": "四象限图"},
            {"id": "act", "name": "分象限定动作", "duration_min": 8,
             "instruction": "高投低果项定止损或改法，低投高果项定加码，其余各定保持或维持观察，逐项写明。",
             "checkpoint": "每个象限都有对应动作；且每个努力项都有明确处置",
             "output": "动作清单"},
            {"id": "recheck", "name": "下周期复评", "duration_min": 6,
             "instruction": "下周期用新数据重打一次分，看高投低果项是否减少、低投高果项是否增加。",
             "checkpoint": "完成复评；且对比了两类象限的增减",
             "output": "复评结果", "fail_to": "place"}
        ],
        "evaluate": {
            "self_check": ["结果好坏是有数据的，还是我感觉？", "高投低果项我是真止损了，只是说说？"],
            "success_criteria": ["高投低果项占比下降", "低投高果项获得更多投入"]
        },
        "agent_contract": {
            "input": ["efforts"], "output": ["四象限图", "动作清单"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸上画四象限并逐项落位"
        }
    },
    {
        "id": "habit-consistency", "name": "习惯性学习法", "name_en": "Habitual Learning",
        "category": "计划执行", "evidence": "anecdotal", "evidence_refs": [],
        "description": "把学习固化成固定时间、固定地点、固定开场的自动流程，用环境一致性降低每次启动的意志消耗。",
        "when_to_use": ["每次开始学习都要下很大决心", "状态时好时坏", "想让它变成默认动作"],
        "when_not_to_use": ["日程高度不固定、无法保证同时同地时"],
        "params": {
            "type": "object", "required": [],
            "properties": {"cue": {"type": "string", "default": "", "description": "固定触发线索，如每天早饭后"}}
        },
        "steps": [
            {"id": "fix", "name": "固定时空", "duration_min": 5,
             "instruction": "选定一个每天最可能兑现的时段和一个专属地点，写下'每天X时在Y地学习'。",
             "checkpoint": "时段与地点已写死；且该时段每日可得",
             "output": "固定时空约定"},
            {"id": "ritual", "name": "设固定开场", "duration_min": 5,
             "instruction": "设计一个 60 秒的开场动作，如泡茶、放固定歌单、翻开固定本子，作为进入信号。",
             "checkpoint": "开场动作已设计且可在 60 秒内完成；且与学习地点绑定",
             "output": "开场仪式"},
            {"id": "run", "name": "到点即执行", "duration_min": 25,
             "instruction": "每天到点就地执行开场动作后开始学习，不等'有状态'；做了就记一格。",
             "checkpoint": "连续天数有记录；且每次都以开场动作启动",
             "output": "执行记录"},
            {"id": "protect", "name": "保护不中断", "duration_min": 5,
             "instruction": "出现中断风险时启用最小版（只做 5 分钟）保住连续，而不是跳过一整天。",
             "checkpoint": "中断日启用了最小版；且连续记录未被清零",
             "output": "保护记录", "fail_to": "ritual"}
        ],
        "evaluate": {
            "self_check": ["我是到点就启动，还是在等状态？", "中断时我保了最小版，还是直接跳过了？"],
            "success_criteria": ["连续执行天数稳定增长", "启动所需的意志感下降"]
        },
        "agent_contract": {
            "input": ["cue"], "output": ["执行记录", "保护记录"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：固定本子画连续格"
        }
    },
    # ============================== 学习方法：理解构建（+1）==============================
    {
        "id": "spiral-learning", "name": "螺旋学习法", "name_en": "Spiral Learning",
        "category": "理解构建", "evidence": "anecdotal", "evidence_refs": [],
        "description": "对一个知识体做多轮覆盖，每轮都比上一轮更深更细，先建立整体轮廓再逐层加深，而非一轮求全。",
        "when_to_use": ["面对庞大知识体不知从何下手", "一轮啃不透", "想先有全局再钻细节"],
        "when_not_to_use": ["范围很小、一轮即可掌握时"],
        "params": {
            "type": "object", "required": ["scope"],
            "properties": {"scope": {"type": "string", "description": "要螺旋学习的知识范围"}}
        },
        "steps": [
            {"id": "outline", "name": "画整体轮廓", "duration_min": 15,
             "instruction": "第一轮只求全局：快速过完整个范围，画出它由哪几大块组成，不深究细节。",
             "checkpoint": "画出了整体分块图；且本轮未陷入单一细节",
             "output": "整体轮廓图"},
            {"id": "deepen", "name": "逐轮加深", "duration_min": 30,
             "instruction": "第二轮起每轮选中一块加深一层，同时用一页纸复述其它块的当前理解，保持全局不凉。",
             "checkpoint": "本轮有指定加深块；且其它块被一页纸复述保温",
             "output": "加深记录与保温页"},
            {"id": "connect", "name": "连接各块", "duration_min": 10,
             "instruction": "每轮结束时写一条本轮加深块与其它块的关联，逐步把块连成网。",
             "checkpoint": "每轮产出至少一条块间关联",
             "output": "关联积累"},
            {"id": "assess", "name": "评估进入下轮", "duration_min": 8,
             "instruction": "评估当前轮的理解深度，决定是继续加深本块还是进入下一块，写下判断依据。",
             "checkpoint": "给出了继续或转块的判断及依据",
             "output": "轮次决策", "fail_to": "deepen"}
        ],
        "evaluate": {
            "self_check": ["我是在逐轮加深，还是第一轮就卡死在一块？", "保温页让我保住了全局吗？"],
            "success_criteria": ["各块理解深度逐轮递增", "能说出块与块之间的关联"]
        },
        "agent_contract": {
            "input": ["scope"], "output": ["整体轮廓图", "关联积累"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸上画轮廓并逐轮加深复述"
        }
    },
    # ============================== 思维方法（新分类，+6）==============================
    {
        "id": "five-whys", "name": "5Why 追因法", "name_en": "Five Whys",
        "category": "思维方法", "evidence": "anecdotal", "evidence_refs": [],
        "description": "对一个问题连续追问为什么，每层答案作为下一层的问题，直到触及可干预的根本原因。",
        "when_to_use": ["问题反复出现想除根", "只知症状不知病因", "复盘找根因"],
        "when_not_to_use": ["问题本身是多因并发（改用鱼骨图）"],
        "params": {
            "type": "object", "required": ["problem"],
            "properties": {"problem": {"type": "string", "description": "要追根因的问题"}}
        },
        "steps": [
            {"id": "state", "name": "写清问题", "duration_min": 4,
             "instruction": "用一句话写下要解决的具体问题，避免笼统描述。",
             "checkpoint": "问题被写成一句具体陈述；且不含多个问题混堆",
             "output": "问题陈述"},
            {"id": "chain", "name": "连续追问为什么", "duration_min": 12,
             "instruction": "从问题出发追问为什么得到答案一，再就答案一问为什么得答案二，至少追五层，每层附依据。",
             "checkpoint": "追问链至少 5 层；且每层答案附了一条依据",
             "output": "为什么链条"},
            {"id": "root", "name": "锁定根因", "duration_min": 6,
             "instruction": "在链条末端标出根本原因，并确认它是可干预的；若不可干预则回上一层。",
             "checkpoint": "标出了根本原因；且确认其可被干预",
             "output": "根因结论"},
            {"id": "counter", "name": "对根因定对策", "duration_min": 8,
             "instruction": "针对根因写一条可执行的防止再发对策，并说明它切断了链条哪一环。",
             "checkpoint": "对策被写明且可执行；且指明了切断的环节",
             "output": "对策", "fail_to": "chain"}
        ],
        "evaluate": {
            "self_check": ["我是一直在往下追，还是在同层打转？", "找到的根因我真能干预吗？"],
            "success_criteria": ["得到可干预的根因", "对策实施后问题复发减少"]
        },
        "agent_contract": {
            "input": ["problem"], "output": ["为什么链条", "根因结论", "对策"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：口头连续追问并记录"
        }
    },
    {
        "id": "five-w1h", "name": "5W1H 拆解法", "name_en": "5W1H Analysis",
        "category": "思维方法", "evidence": "anecdotal", "evidence_refs": [],
        "description": "从事、因、时、地、人、法六个维度把一个对象或问题拆全，用维度清单防止遗漏。",
        "when_to_use": ["分析一个事件或方案怕漏维度", "写方案前先把要素想全", "信息杂乱待理清"],
        "when_not_to_use": ["只需单点深入时（六维反而稀释焦点）"],
        "params": {
            "type": "object", "required": ["subject"],
            "properties": {"subject": {"type": "string", "description": "要六维拆解的对象"}}
        },
        "steps": [
            {"id": "frame", "name": "列出六维问题", "duration_min": 5,
             "instruction": "把六个维度各写成一个针对本对象的问题：是什么、为什么、何时、何地、涉及谁、如何做。",
             "checkpoint": "六个维度各有一个针对本对象的问题",
             "output": "六维问题清单"},
            {"id": "fill", "name": "逐维填写", "duration_min": 15,
             "instruction": "逐维回答，能查证的回答事实，查不到的标注待查，不编造。",
             "checkpoint": "六个维度都有回答或待查标记；且无编造内容",
             "output": "六维回答"},
            {"id": "gap", "name": "找维度缺口", "duration_min": 6,
             "instruction": "检查哪个维度回答最薄或待查最多，那通常是盲区，列为优先补全项。",
             "checkpoint": "标出了最薄弱维度；且列出待补全清单",
             "output": "缺口清单"},
            {"id": "synthesize", "name": "汇成结论", "duration_min": 6,
             "instruction": "把六维回答汇成一段结论，明确指出哪个维度对结论影响最大。",
             "checkpoint": "产出结论段；且指出了影响最大的维度",
             "output": "综合结论", "fail_to": "fill"}
        ],
        "evaluate": {
            "self_check": ["六个维度我是都认真答了，还是有几个空的？", "最薄的那个维度，我是不是在回避？"],
            "success_criteria": ["六维均有实质回答", "结论可由六维回答支撑"]
        },
        "agent_contract": {
            "input": ["subject"], "output": ["六维回答", "综合结论"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面六格逐维填写"
        }
    },
    {
        "id": "mece", "name": "MECE 分解", "name_en": "MECE Principle",
        "category": "思维方法", "evidence": "anecdotal", "evidence_refs": [],
        "description": "把一个问题分解成若干子项，做到相互独立、完全穷尽，既不重叠也不遗漏。",
        "when_to_use": ["分解问题怕重叠或漏项", "搭分析框架", "列原因/类型清单"],
        "when_not_to_use": ["早期发散阶段（先发散再收敛套 MECE）"],
        "params": {
            "type": "object", "required": ["problem"],
            "properties": {"problem": {"type": "string", "description": "要分解的问题"}}
        },
        "steps": [
            {"id": "draft", "name": "先列子项", "duration_min": 8,
             "instruction": "把问题按一个标准先分解成若干子项，写下所用标准。",
             "checkpoint": "列出了至少 3 个子项；且写明了分解标准",
             "output": "初版分解"},
            {"id": "check-mutually", "name": "查重叠", "duration_min": 6,
             "instruction": "两两比对子项，找出能同时归入多项的情况，合并或重新界定边界。",
             "checkpoint": "完成两两比对；且重叠项被合并或划清边界",
             "output": "去重后分解"},
            {"id": "check-exhaustive", "name": "查遗漏", "duration_min": 6,
             "instruction": "设想一个原问题的具体实例，检查它能否落到某一子项；落不下的即为遗漏，补上。",
             "checkpoint": "用至少 2 个实例验证；且落不下的实例触发了补项",
             "output": "补全后分解"},
            {"id": "freeze", "name": "定稿框架", "duration_min": 4,
             "instruction": "确认子项既无重叠又覆盖全部实例后，定稿为可复用框架并写下标准。",
             "checkpoint": "框架无重叠且通过实例覆盖测试；且标准被写明",
             "output": "MECE 框架", "fail_to": "check-mutually"}
        ],
        "evaluate": {
            "self_check": ["我查重叠是真比对了，还是目测？", "我的实例真的能检验遗漏吗？"],
            "success_criteria": ["子项相互独立无重叠", "新实例总能落到唯一子项"]
        },
        "agent_contract": {
            "input": ["problem"], "output": ["MECE 框架"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面列项并两两比对"
        }
    },
    {
        "id": "logic-tree", "name": "逻辑树分解", "name_en": "Logic Tree",
        "category": "思维方法", "evidence": "anecdotal", "evidence_refs": [],
        "description": "把核心问题作为树根，逐层拆成彼此独立、可分别验证的子问题，用树定位该先攻哪一枝。",
        "when_to_use": ["大问题无从下手", "要把问题拆到可执行/可验证", "排优先级"],
        "when_not_to_use": ["问题本身已足够小（直接解决）"],
        "params": {
            "type": "object", "required": ["question"],
            "properties": {"question": {"type": "string", "description": "要分解的核心问题"}}
        },
        "steps": [
            {"id": "root", "name": "定树根问题", "duration_min": 4,
             "instruction": "把核心问题写成一句待解答的问句，作为逻辑树的根。",
             "checkpoint": "树根被写成一句明确的问句",
             "output": "树根问题"},
            {"id": "branch", "name": "逐层拆子问题", "duration_min": 12,
             "instruction": "把根问题按 MECE 拆成第一层子问题，每个子问题可独立验证；继续下拆到可行动作为止。",
             "checkpoint": "第一层子问题相互独立且可验证；且已下拆到可行动层",
             "output": "逻辑树"},
            {"id": "locate", "name": "标最可能枝", "duration_min": 6,
             "instruction": "给每个末端子问题标一个最可能的原因或最优先的处理项，选出要优先验证的分支。",
             "checkpoint": "每个末端子问题都被标注；且选出了优先分支",
             "output": "优先级标注"},
            {"id": "verify", "name": "验证优先枝", "duration_min": 12,
             "instruction": "只对优先分支收集证据验证，成立则沿树下钻，不成立则换并列分支。",
             "checkpoint": "优先分支被验证；且记录了下钻或换支的结论",
             "output": "验证结论", "fail_to": "branch"}
        ],
        "evaluate": {
            "self_check": ["我的子问题是能独立验证的，还是又一句大话？", "优先枝是真可能，还是看着顺眼？"],
            "success_criteria": ["逻辑树可下钻到可行动层", "优先分支验证有明确结论"]
        },
        "agent_contract": {
            "input": ["question"], "output": ["逻辑树", "验证结论"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸上画树并逐层拆解"
        }
    },
    {
        "id": "six-hats", "name": "六顶思考帽", "name_en": "Six Thinking Hats",
        "category": "思维方法", "evidence": "anecdotal", "evidence_refs": [],
        "description": "把思考分成白、红、黑、黄、绿、蓝六种模式，每次只戴一顶帽、只做那一类思考，避免混乱对抗。",
        "when_to_use": ["讨论变成情绪和逻辑混战", "想系统审视一个方案", "团队/个人全面评估"],
        "when_not_to_use": ["只需快速表态的简单决定"],
        "params": {
            "type": "object", "required": ["topic"],
            "properties": {"topic": {"type": "string", "description": "要用六顶帽审视的议题"}}
        },
        "steps": [
            {"id": "white", "name": "白帽列事实", "duration_min": 6,
             "instruction": "只列已知事实和数据，不加解释和判断；缺数据的标为待补。",
             "checkpoint": "列出了事实清单；且每条为事实而非判断；缺数据处被标注",
             "output": "事实清单"},
            {"id": "red", "name": "红帽说直觉", "duration_min": 4,
             "instruction": "只说出当下的直觉、喜好和顾虑，不必论证。",
             "checkpoint": "记录了直觉与顾虑；且无需论证",
             "output": "直觉记录"},
            {"id": "black-yellow", "name": "黑帽黄帽找利弊", "duration_min": 10,
             "instruction": "先戴黑帽只列风险与不足，再戴黄帽只列收益与亮点，两类分开不混。",
             "checkpoint": "风险与收益被分成两列；且两类未混填",
             "output": "利弊清单"},
            {"id": "green", "name": "绿帽出替代", "duration_min": 8,
             "instruction": "只提新想法、替代方案和变通，暂不评判可行性。",
             "checkpoint": "提出了至少 3 个替代想法；且提出阶段未评判",
             "output": "替代方案"},
            {"id": "blue", "name": "蓝帽做总结", "duration_min": 6,
             "instruction": "回顾各帽产出，给出结论、下一步和还需补哪些数据。",
             "checkpoint": "产出结论与下一步；且列出待补数据",
             "output": "总结与行动", "fail_to": "white"}
        ],
        "evaluate": {
            "self_check": ["我戴黑帽时是不是又掺进了乐观？", "六顶帽我都戴了，还是跳过了一顶？"],
            "success_criteria": ["各帽产出分开不混", "结论覆盖利弊与替代"]
        },
        "agent_contract": {
            "input": ["topic"], "output": ["事实清单", "利弊清单", "替代方案", "总结"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：按六顶帽顺序口头过一遍并记录"
        }
    },
    {
        "id": "scamper", "name": "SCAMPER 创意法", "name_en": "SCAMPER",
        "category": "思维方法", "evidence": "anecdotal", "evidence_refs": [],
        "description": "用替代、合并、调整、修改、他用、消除、重排七个提问 systematically 改造一个对象，逼出非常规方案。",
        "when_to_use": ["想改进一个产品或流程", "创意枯竭", "需要一批备选方案"],
        "when_not_to_use": ["对象已最优、只需执行时"],
        "params": {
            "type": "object", "required": ["target"],
            "properties": {"target": {"type": "string", "description": "要改造的对象或方案"}}
        },
        "steps": [
            {"id": "setup", "name": "写下七问", "duration_min": 5,
             "instruction": "把七个提问各写成一句针对本对象的问题：能替代什么、能和谁合并、能如何调整等。",
             "checkpoint": "七个维度各有一句针对本对象的问题",
             "output": "七问清单"},
            {"id": "generate", "name": "逐问产方案", "duration_min": 18,
             "instruction": "逐问强制作答，每问至少产出一个改造想法，先不评判好坏。",
             "checkpoint": "每问至少一个想法；且产生阶段未评判",
             "output": "想法池"},
            {"id": "screen", "name": "筛选可行项", "duration_min": 8,
             "instruction": "给每个想法按可行性和潜在价值各打高低分，选出高分项。",
             "checkpoint": "每个想法都有可行性与价值评分；且高分项被选出",
             "output": "筛选结果"},
            {"id": "prototype", "name": "落地一个", "duration_min": 10,
             "instruction": "把最高分想法写成可执行的最小改造步骤，先做这一步。",
             "checkpoint": "最高分想法被拆成最小改造步骤",
             "output": "改造方案", "fail_to": "generate"}
        ],
        "evaluate": {
            "self_check": ["我是七问都认真过了，还是挑顺手的做？", "筛选是凭标准还是凭喜好？"],
            "success_criteria": ["七问均有产出", "至少一个改造方案被落地"]
        },
        "agent_contract": {
            "input": ["target"], "output": ["想法池", "改造方案"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：按七问口头产想法并记录"
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
            "lmp": "0.1", "id": s["id"], "name": s["name"], "name_en": s["name_en"],
            "version": "0.1.0", "license": "CC0-1.0",
            "authors": ["OpenLMP 公共领域贡献"],
            "category": s["category"], "evidence": s["evidence"], "evidence_refs": s["evidence_refs"],
            "description": s["description"], "when_to_use": s["when_to_use"], "when_not_to_use": s["when_not_to_use"],
            "params": s["params"], "requires": {"tools": [], "assets": []},
            "steps": s["steps"], "evaluate": s["evaluate"], "agent_contract": s["agent_contract"],
            "resources": [], "metadata": {"created_at": TODAY, "updated_at": TODAY, "contributors": []},
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
