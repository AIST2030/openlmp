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
OpenLMP 第四批：96 → 107（新增 11 个）。
= 分析方法 9 个（新分类"分析方法"）+ 补两个学习候选：横向列方案（思维方法）、目标逆向思维（计划执行）。
商业框架不进本库，另建 business/ 子库。硬约束同前。
"""
import json, os, sys, datetime

OUT = sys.argv[1] if len(sys.argv) > 1 else "E:/视频创作/AIST2030/openlmp/skills"
TODAY = datetime.date.today().isoformat()

NEW = [
    # ============================== 分析方法（新分类，+9）==============================
    {
        "id": "pareto", "name": "帕累托分析", "name_en": "Pareto Analysis",
        "category": "分析方法", "evidence": "anecdotal", "evidence_refs": [],
        "description": "找出贡献约 80% 结果的那 20% 关键因素，把精力压到关键少数上。",
        "when_to_use": ["资源有限想抓重点", "一堆事项分不清主次", "想提升投入产出比"],
        "when_not_to_use": ["各项都薄弱、无明显关键项时"],
        "params": {
            "type": "object", "required": ["items"],
            "properties": {"items": {"type": "string", "description": "要分析的因素及其贡献数据"}}
        },
        "steps": [
            {"id": "tally", "name": "统计各因素贡献", "duration_min": 10,
             "instruction": "列出相关因素，给每个因素一个可衡量的贡献值，如次数、金额、时长，并排出序。",
             "checkpoint": "每个因素都有贡献值；且已按贡献从高到低排序",
             "output": "贡献排序表"},
            {"id": "cumulative", "name": "算累计占比", "duration_min": 8,
             "instruction": "从高到低累加各因素贡献，算出累计占总量的比例，标出累计到约 80% 的切点。",
             "checkpoint": "给出了累计占比；且标出了累计约 80% 的切点",
             "output": "累计占比"},
            {"id": "identify", "name": "锁定关键少数", "duration_min": 5,
             "instruction": "把累计约 80% 以上的因素列为关键少数，其余归为次要多数。",
             "checkpoint": "关键少数被标出；且其余被归为次要多数",
             "output": "关键少数清单"},
            {"id": "act", "name": "只攻关键少数", "duration_min": 15,
             "instruction": "本周期只对关键少数投入改进资源，次要多数维持不动，记录关键少数改进后的变化。",
             "checkpoint": "仅关键少数获得改进资源；且记录了改进后变化",
             "output": "改进结果", "fail_to": "cumulative"}
        ],
        "evaluate": {
            "self_check": ["贡献值是真数据还是估的？", "关键少数我真的在攻，还是又摊平了？"],
            "success_criteria": ["关键少数贡献占比进一步提升", "单位投入产出比上升"]
        },
        "agent_contract": {
            "input": ["items"], "output": ["贡献排序表", "关键少数清单", "改进结果"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：列表排序并手算累计占比"
        }
    },
    {
        "id": "fishbone", "name": "鱼骨图分析", "name_en": "Fishbone Diagram",
        "category": "分析方法", "evidence": "anecdotal", "evidence_refs": [],
        "description": "以问题为鱼头，从人、方法、材料、设备、环境等维度逐层拆潜在原因，用多支分类避免只盯单一链条。",
        "when_to_use": ["问题多因并发", "想系统性枚举原因", "5Why 追不出根因时"],
        "when_not_to_use": ["原因单一明确（直接处理即可）"],
        "params": {
            "type": "object", "required": ["problem"],
            "properties": {"problem": {"type": "string", "description": "要分析原因的问题"}}
        },
        "steps": [
            {"id": "head", "name": "定鱼头问题", "duration_min": 4,
             "instruction": "把要分析的问题写成一句具体陈述，放在图的一端作鱼头。",
             "checkpoint": "问题被写成一句具体陈述；且位于图的一端作鱼头",
             "output": "鱼头问题"},
            {"id": "bones", "name": "定主骨维度", "duration_min": 6,
             "instruction": "选定 4-6 个原因维度作大骨，如人、方法、材料、设备、环境、测量。",
             "checkpoint": "大骨 4-6 个；且每个维度命名明确",
             "output": "主骨框架"},
            {"id": "twigs", "name": "逐骨列原因", "duration_min": 15,
             "instruction": "每个大骨下继续列具体原因作小骨，每根小骨是一个可查证的可能原因。",
             "checkpoint": "每个大骨下至少 2 根小骨；且每根小骨可查证",
             "output": "完整鱼骨图"},
            {"id": "verify", "name": "验证主因", "duration_min": 12,
             "instruction": "给每根小骨标一个可能程度，选出最可能的 2-3 根去查证，确认或排除。",
             "checkpoint": "每根小骨标了可能程度；且最可能的 2-3 根被查证",
             "output": "主因结论", "fail_to": "bones"}
        ],
        "evaluate": {
            "self_check": ["我的维度分全了吗，还是漏了一类？", "主因是查证出来的，还是看着像？"],
            "success_criteria": ["原因枚举覆盖多个维度", "主因经查证被确认"]
        },
        "agent_contract": {
            "input": ["problem"], "output": ["鱼骨图", "主因结论"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸上画鱼头鱼骨并逐骨列因"
        }
    },
    {
        "id": "decision-matrix", "name": "决策矩阵", "name_en": "Decision Matrix",
        "category": "分析方法", "evidence": "anecdotal", "evidence_refs": [],
        "description": "给候选方案按若干维度打分并加权求和，用可比较的分数替代拍脑袋取舍。",
        "when_to_use": ["多个方案难取舍", "想透明化决策依据", "团队需对齐选择"],
        "when_not_to_use": ["只有一个方案（无从比较）"],
        "params": {
            "type": "object", "required": ["options"],
            "properties": {"options": {"type": "string", "description": "候选方案列表"}}
        },
        "steps": [
            {"id": "criteria", "name": "定维度与权重", "duration_min": 8,
             "instruction": "选定 3-5 个决策维度，按重要性分配权重，权重之和为 1。",
             "checkpoint": "维度 3-5 个；且权重之和等于 1",
             "output": "维度与权重"},
            {"id": "score", "name": "逐方案打分", "duration_min": 12,
             "instruction": "每个方案在每个维度按统一标准打分，并写下打分理由。",
             "checkpoint": "每个方案每个维度都有分；且每分有理由",
             "output": "打分矩阵"},
            {"id": "weight", "name": "加权求和排序", "duration_min": 6,
             "instruction": "把每个方案的各维度分乘以权重后求和，按总分排序。",
             "checkpoint": "给出了每个方案加权总分；且按总分排序",
             "output": "排序结果"},
            {"id": "sensitivity", "name": "做敏感性检查", "duration_min": 8,
             "instruction": "把最高与最低权重对调一次，看排序是否翻转；翻转则说明结果对权重敏感，需重估权重。",
             "checkpoint": "完成了一次权重对调；且记录了排序是否翻转",
             "output": "敏感性结论", "fail_to": "score"}
        ],
        "evaluate": {
            "self_check": ["打分是真按标准，还是凭好恶？", "排序翻转时我重估权重了吗？"],
            "success_criteria": ["给出可复算的加权总分", "结论对权重扰动有明确稳健性判断"]
        },
        "agent_contract": {
            "input": ["options"], "output": ["打分矩阵", "排序结果", "敏感性结论"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面画矩阵并手算加权分"
        }
    },
    {
        "id": "pdca", "name": "PDCA 循环", "name_en": "PDCA Cycle",
        "category": "分析方法", "evidence": "anecdotal", "evidence_refs": [],
        "description": "按计划、执行、检查、处理四步循环推进，每轮把结果反馈回计划，让改进持续滚动。",
        "when_to_use": ["改进一项工作或流程", "想建立持续迭代机制", "质量或效率提升"],
        "when_not_to_use": ["一次性任务（无循环必要）"],
        "params": {
            "type": "object", "required": ["goal"],
            "properties": {"goal": {"type": "string", "description": "本轮要改进的目标"}}
        },
        "steps": [
            {"id": "plan", "name": "定计划", "duration_min": 8,
             "instruction": "写下本轮要改进的目标、具体动作和预期指标。",
             "checkpoint": "目标、动作、预期指标三者的书面记录齐备",
             "output": "计划"},
            {"id": "do", "name": "执行", "duration_min": 20,
             "instruction": "按计划执行，记录实际发生的情况与数据。",
             "checkpoint": "计划动作被执行；且记录了实际数据",
             "output": "执行记录"},
            {"id": "check", "name": "检查对比", "duration_min": 6,
             "instruction": "把实际指标与预期指标对比，标出达成项与偏差。",
             "checkpoint": "实际与预期逐项对比；且偏差被标出",
             "output": "检查结果"},
            {"id": "handle", "name": "处理并进入下轮", "duration_min": 6,
             "instruction": "达成项固化为标准，未达成项分析原因并写入下一轮计划，明确下一轮的计划。",
             "checkpoint": "达成项被固化；未达成项进入下一轮计划",
             "output": "处理与下轮计划", "fail_to": "plan"}
        ],
        "evaluate": {
            "self_check": ["检查是真对比数据，还是凭感觉？", "未达成项我写进下一轮了吗？"],
            "success_criteria": ["每轮都有进入下一轮的明确改进", "关键指标逐轮趋近目标"]
        },
        "agent_contract": {
            "input": ["goal"], "output": ["计划", "检查结果", "下轮计划"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面四步循环记录"
        }
    },
    {
        "id": "ooda", "name": "OODA 循环", "name_en": "OODA Loop",
        "category": "分析方法", "evidence": "anecdotal", "evidence_refs": [],
        "description": "按观察、判断、决策、行动四步快速循环，用缩短回路应对变化，比一次规划到底更灵活。",
        "when_to_use": ["环境变化快需快速应变", "竞争或对抗场景", "信息不完整需边做边调"],
        "when_not_to_use": ["环境稳定、一次规划即可的长周期任务"],
        "params": {
            "type": "object", "required": ["situation"],
            "properties": {"situation": {"type": "string", "description": "当前处境描述"}}
        },
        "steps": [
            {"id": "observe", "name": "观察", "duration_min": 8,
             "instruction": "收集当前环境的可观察事实，标注哪些确定、哪些待确认。",
             "checkpoint": "列出了观察事实；且区分了确定与待确认",
             "output": "观察清单"},
            {"id": "orient", "name": "判断", "duration_min": 6,
             "instruction": "基于观察形成对形势的判断，写出关键假设和最可能的走向。",
             "checkpoint": "写出了形势判断；且列出关键假设",
             "output": "判断"},
            {"id": "decide", "name": "决策", "duration_min": 5,
             "instruction": "基于判断定下一步行动，只定一个最优先动作。",
             "checkpoint": "定出了唯一优先动作",
             "output": "决策"},
            {"id": "act", "name": "行动并回观察", "duration_min": 15,
             "instruction": "执行该动作，完成后立刻回到观察，用新结果更新判断，进入下一循环。",
             "checkpoint": "动作被执行；且回到观察形成循环",
             "output": "行动与循环记录", "fail_to": "observe"}
        ],
        "evaluate": {
            "self_check": ["我的观察是全的，还是只看了想看的？", "循环真的转起来了吗，还是做完一轮就停？"],
            "success_criteria": ["循环持续运转", "每轮判断比上轮更接近实际"]
        },
        "agent_contract": {
            "input": ["situation"], "output": ["观察清单", "判断", "决策", "循环记录"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：按四步口头快速过并记录"
        }
    },
    {
        "id": "gap-analysis", "name": "差距分析", "name_en": "Gap Analysis",
        "category": "分析方法", "evidence": "anecdotal", "evidence_refs": [],
        "description": "对比现状与目标的差距，定位差距出在哪，并按事实、解释、行动三步落地，避免只有愿望没有动作。",
        "when_to_use": ["知道要提升却不知差多少", "想定位差距环节", "把目标变成行动"],
        "when_not_to_use": ["现状数据缺失、无法量化差距时"],
        "params": {
            "type": "object", "required": ["goal"],
            "properties": {"goal": {"type": "string", "description": "想达成改进的目标"}}
        },
        "steps": [
            {"id": "measure", "name": "量化现状与目标", "duration_min": 6,
             "instruction": "给目标和现状各定一个可衡量的数值，算出差距大小。",
             "checkpoint": "目标与现状都有数值；且算出了差距",
             "output": "差距数值"},
            {"id": "locate", "name": "定位差距环节", "duration_min": 10,
             "instruction": "把整体差距拆到具体环节，找出贡献最大的差距环节。",
             "checkpoint": "差距被拆到环节级；且标出了最大差距环节",
             "output": "差距分解"},
            {"id": "explain", "name": "解释原因", "duration_min": 8,
             "instruction": "对最大差距环节给出原因解释，并附上作为依据的事实，事实与解释分开写。",
             "checkpoint": "给出了带事实依据的原因解释；且事实与解释分开",
             "output": "原因解释"},
            {"id": "act", "name": "给行动", "duration_min": 6,
             "instruction": "针对原因写下下一步行动，每条对应一个差距环节，并带上完成时间。",
             "checkpoint": "每个目标差距环节都有对应行动；且行动带时间",
             "output": "行动计划", "fail_to": "locate"}
        ],
        "evaluate": {
            "self_check": ["差距是真量化的，还是拍脑袋？", "行动真的对准最大差距环节了吗？"],
            "success_criteria": ["差距可量化到环节", "行动实施后差距收窄"]
        },
        "agent_contract": {
            "input": ["goal"], "output": ["差距分解", "行动计划"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面算差距并按事实、解释、行动三步记录"
        }
    },
    {
        "id": "hypothesis-method", "name": "假设法", "name_en": "Hypothesis-Driven Analysis",
        "category": "分析方法", "evidence": "anecdotal", "evidence_refs": [],
        "description": "先提出一个最可能的假设，再针对性验证，用假设聚焦信息收集，避免全面撒网。",
        "when_to_use": ["信息多、时间少需聚焦", "排查问题想快速定位", "想提高分析效率"],
        "when_not_to_use": ["对领域毫无概念、提不出合理假设时"],
        "params": {
            "type": "object", "required": ["question"],
            "properties": {"question": {"type": "string", "description": "要分析验证的问题"}}
        },
        "steps": [
            {"id": "propose", "name": "提最可能假设", "duration_min": 6,
             "instruction": "针对问题提出一个最可能的假设，并写下如果假设成立会观察到什么。",
             "checkpoint": "假设被提出；且附了可观察判据",
             "output": "假设与判据"},
            {"id": "target", "name": "定向收集", "duration_min": 12,
             "instruction": "只收集能验证或推翻该假设的信息，不碰无关信息。",
             "checkpoint": "收集的信息均指向假设判据；且无关信息被排除",
             "output": "定向证据"},
            {"id": "test", "name": "判定", "duration_min": 6,
             "instruction": "对照判据判定假设成立、被推翻或证据不足。",
             "checkpoint": "给出了成立、推翻或不足之一的判定",
             "output": "判定结果"},
            {"id": "iterate", "name": "换假设再来", "duration_min": 10,
             "instruction": "假设被推翻或证据不足时，提出下一个最可能假设并重复定向验证。",
             "checkpoint": "被推翻或不足时提出了新假设；且重复了定向验证",
             "output": "迭代记录", "fail_to": "propose"}
        ],
        "evaluate": {
            "self_check": ["我先有假设再找证据，还是反过来？", "被推翻时我痛快换假设了吗？"],
            "success_criteria": ["用较少信息得出可靠判定", "假设收敛到被证实项"]
        },
        "agent_contract": {
            "input": ["question"], "output": ["假设与判据", "判定结果"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：口头提假设并定向查证"
        }
    },
    {
        "id": "elimination", "name": "排除法", "name_en": "Elimination Method",
        "category": "分析方法", "evidence": "anecdotal", "evidence_refs": [],
        "description": "逐一排除不可能的选项，用排除缩小范围，剩下的即为最可能解，适合候选有限的排查。",
        "when_to_use": ["候选有限想快速锁定", "排查故障或谜题", "逐一验证成本低于盲猜"],
        "when_not_to_use": ["候选无限或难以逐一验证时"],
        "params": {
            "type": "object", "required": ["candidates"],
            "properties": {"candidates": {"type": "string", "description": "全部候选选项"}}
        },
        "steps": [
            {"id": "list", "name": "列全部候选", "duration_min": 6,
             "instruction": "把可能的选项全部列出，不漏不重。",
             "checkpoint": "候选清单完整；且无重复项",
             "output": "候选清单"},
            {"id": "rule", "name": "定排除判据", "duration_min": 8,
             "instruction": "为每个候选写一条能判定其是否可能的客观判据。",
             "checkpoint": "每个候选都有一条客观判据",
             "output": "判据表"},
            {"id": "eliminate", "name": "逐条排除", "duration_min": 15,
             "instruction": "按判据逐一验证，凡被证伪的候选立即移出，并记录排除依据。",
             "checkpoint": "每个被排除项都有依据；且未被证伪的保留",
             "output": "剩余候选"},
            {"id": "converge", "name": "收敛结论", "duration_min": 6,
             "instruction": "当只剩一个候选时即为结论；若剩多个则补新判据继续排除。",
             "checkpoint": "给出了单一结论或补充了新判据",
             "output": "结论", "fail_to": "rule"}
        ],
        "evaluate": {
            "self_check": ["我的判据是真能证伪，还是怎么说都对？", "剩下的那个，我是排除了其它还是直接猜的？"],
            "success_criteria": ["每个排除项有客观依据", "结论收敛到可验证的单一候选"]
        },
        "agent_contract": {
            "input": ["candidates"], "output": ["剩余候选", "结论"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：列表逐条打勾叉排除"
        }
    },
    {
        "id": "reductio", "name": "反证法", "name_en": "Proof by Contradiction",
        "category": "分析方法", "evidence": "anecdotal", "evidence_refs": [],
        "description": "想证明一个命题，先假设它不成立并推出矛盾，从而反证原命题成立，用矛盾钉死结论。",
        "when_to_use": ["直接证明困难", "想严格确立一个命题", "数学或逻辑推理"],
        "when_not_to_use": ["命题可用例子直接证实时（不必绕道）"],
        "params": {
            "type": "object", "required": ["proposition"],
            "properties": {"proposition": {"type": "string", "description": "要证明的命题"}}
        },
        "steps": [
            {"id": "negate", "name": "写出反面假设", "duration_min": 5,
             "instruction": "把原命题改写为它的否定，作为待推出矛盾的假设。",
             "checkpoint": "写出了原命题的明确否定",
             "output": "反面假设"},
            {"id": "derive", "name": "从反面推导", "duration_min": 15,
             "instruction": "仅从反面假设和已知前提一步步推导，记录每一步的依据。",
             "checkpoint": "推导每一步都有前提依据；且未使用原命题本身",
             "output": "推导链"},
            {"id": "contradict", "name": "找出矛盾", "duration_min": 6,
             "instruction": "在推导中找出与已知事实或前提相冲突的一步，即为矛盾点。",
             "checkpoint": "标出了矛盾点；且矛盾指向已知前提或事实",
             "output": "矛盾点"},
            {"id": "conclude", "name": "反证结论", "duration_min": 4,
             "instruction": "因反面假设导致矛盾，故反面不成立、原命题得证，写下结论并说明矛盾所在。",
             "checkpoint": "得出原命题成立的结论；且说明了矛盾所在",
             "output": "反证结论", "fail_to": "derive"}
        ],
        "evaluate": {
            "self_check": ["我推出的是真矛盾，还是只是不方便？", "推导有没有偷偷用了原命题？"],
            "success_criteria": ["矛盾指向确定的前提或事实", "结论仅由反证得出"]
        },
        "agent_contract": {
            "input": ["proposition"], "output": ["推导链", "反证结论"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面写出反面并逐步推导"
        }
    },
    # ============================== 补：思维方法 / 计划执行（+2）==============================
    {
        "id": "lateral-listing", "name": "横向列方案", "name_en": "Lateral Option Listing",
        "category": "思维方法", "evidence": "anecdotal", "evidence_refs": [],
        "description": "遇事先横向列出多个可选方案再排优先级，用先发散列全、再收敛排序，避免一条路走到黑。",
        "when_to_use": ["习惯性只想一个方案", "想比较多个选项", "避免过早收敛"],
        "when_not_to_use": ["唯一可行方案明确时"],
        "params": {
            "type": "object", "required": ["goal"],
            "properties": {"goal": {"type": "string", "description": "要寻求方案的目标"}}
        },
        "steps": [
            {"id": "list", "name": "列多个方案", "duration_min": 10,
             "instruction": "针对目标先不加评判地列出至少 5 个可选方案，哪怕有的看着不靠谱。",
             "checkpoint": "方案至少 5 个；且列出阶段未评判",
             "output": "方案池"},
            {"id": "criteria", "name": "定排序标准", "duration_min": 5,
             "instruction": "写下 2-3 个排序标准，如成本、速度、风险，并分配权重。",
             "checkpoint": "标准 2-3 个；且权重之和为 1",
             "output": "排序标准"},
            {"id": "rank", "name": "按标准排序", "duration_min": 10,
             "instruction": "用标准给每个方案打分并排序，写出每个方案的长处与短处。",
             "checkpoint": "每个方案都有打分；且长短处被写明",
             "output": "排序结果"},
            {"id": "pick", "name": "定主案与备案", "duration_min": 5,
             "instruction": "选得分最高的作主案，同时保留一个备案及其切换触发条件。",
             "checkpoint": "定出了主案；且备案与切换条件被写明",
             "output": "主案与备案", "fail_to": "criteria"}
        ],
        "evaluate": {
            "self_check": ["我是真列了多个，还是列了三个凑数？", "排序是按标准还是按第一印象？"],
            "success_criteria": ["方案数达标且经标准排序", "有明确主案与备案"]
        },
        "agent_contract": {
            "input": ["goal"], "output": ["方案池", "排序结果", "主案与备案"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸上列方案并按标准排序"
        }
    },
    {
        "id": "goal-backward", "name": "目标逆向思维", "name_en": "Goal-Backward Planning",
        "category": "计划执行", "evidence": "anecdotal", "evidence_refs": [],
        "description": "从想要的结果出发倒推现在该做的关键动作，用终点约束过程，砍掉与目标无关的分支。",
        "when_to_use": ["事情杂不知从何入手", "想只做关键动作", "过程容易跑偏"],
        "when_not_to_use": ["目标本身不明（先用 SMART 明确）"],
        "params": {
            "type": "object", "required": ["goal"],
            "properties": {"goal": {"type": "string", "description": "想达成的终点目标"}}
        },
        "steps": [
            {"id": "define", "name": "写清终点", "duration_min": 5,
             "instruction": "用一句话写下要达成的终点状态，并含可判定的达标标准。",
             "checkpoint": "终点被写成一句含判定标准的陈述",
             "output": "终点定义"},
            {"id": "milestone", "name": "倒推里程碑", "duration_min": 10,
             "instruction": "从终点往回推，列出达成前必须完成的 3-5 个里程碑，越靠近终点越具体。",
             "checkpoint": "里程碑 3-5 个；且按距终点远近排列",
             "output": "里程碑链"},
            {"id": "key", "name": "找当前关键动作", "duration_min": 6,
             "instruction": "只看离终点最近的未完成里程碑，推出当下唯一该做的关键动作。",
             "checkpoint": "定出了唯一当前关键动作；且它服务于最近里程碑",
             "output": "当前关键动作"},
            {"id": "prune", "name": "剪无关分支", "duration_min": 6,
             "instruction": "把当前在做但与任何里程碑无关的事列出并暂停，把时间让给关键动作。",
             "checkpoint": "无关事项被列出并暂停；且关键动作获得时间",
             "output": "剪枝记录", "fail_to": "milestone"}
        ],
        "evaluate": {
            "self_check": ["我的里程碑真是从终点倒推的吗，还是正着排的？", "我剪的是真无关，还是不顺手的？"],
            "success_criteria": ["动作链可回溯到终点", "无关事项被有效暂停"]
        },
        "agent_contract": {
            "input": ["goal"], "output": ["里程碑链", "当前关键动作", "剪枝记录"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面从终点往回画里程碑"
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
