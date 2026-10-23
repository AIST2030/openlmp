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
OpenLMP 商业子库 openlmp/business/ 第一批：15 个商业框架 Skill。
与主库同 schema（category 用商业四类：商业分析/商业战略/商业管理/商业表达）。
主库 selftest 只扫 skills/，不扫 business/skills/，两者互不干扰。
硬约束同主库：checkpoint 禁模糊词、instruction 禁自行决定/视情况而定、全文纯度扫描。
"""
import json, os, sys, datetime

OUT = sys.argv[1] if len(sys.argv) > 1 else "E:/视频创作/AIST2030/openlmp/business/skills"
TODAY = datetime.date.today().isoformat()

NEW = [
    # ============================== 商业分析（+7）==============================
    {
        "id": "swot", "name": "SWOT 分析", "name_en": "SWOT Analysis",
        "category": "商业分析", "evidence": "anecdotal", "evidence_refs": [],
        "description": "从优势、劣势、机会、威胁四象限盘点一个对象，再据四象限交叉推导策略，把盘点变成行动。",
        "when_to_use": ["战略盘点", "立项或投标前自评", "竞争分析"],
        "when_not_to_use": ["只想知道单一维度优劣时"],
        "params": {"type": "object", "required": ["subject"], "properties": {"subject": {"type": "string", "description": "要盘点的对象，如产品/项目/公司"}}},
        "steps": [
            {"id": "list", "name": "列四象限事实", "duration_min": 10,
             "instruction": "针对对象从优势、劣势、机会、威胁四方面各列至少 2 条事实；优势与劣势看内部，机会与威胁看外部。",
             "checkpoint": "四方面各至少 2 条；且优势劣势为内部、机会威胁为外部",
             "output": "SWOT 清单"},
            {"id": "cross", "name": "交叉推导", "duration_min": 10,
             "instruction": "用四象限交叉：优势抓机会、劣势补机会、优势抗威胁、劣势避威胁，各出一条策略。",
             "checkpoint": "四类交叉各出一条策略",
             "output": "交叉策略"},
            {"id": "prioritize", "name": "排优先级", "duration_min": 6,
             "instruction": "给每条策略按影响力和可行性打分，选出本周期要执行的 1-2 条。",
             "checkpoint": "每条策略有影响力与可行性评分；且选出 1-2 条",
             "output": "优先策略"},
            {"id": "act", "name": "落到行动", "duration_min": 6,
             "instruction": "把选中的策略写成带负责人和时间的行动项。",
             "checkpoint": "选中策略被拆成带时间的行动项",
             "output": "行动计划", "fail_to": "cross"}
        ],
        "evaluate": {"self_check": ["我把内部和外部因素分清了吗？", "策略是四象限推出来的，还是另想的？"], "success_criteria": ["策略可由 SWOT 推出", "至少一条策略进入执行"]},
        "agent_contract": {"input": ["subject"], "output": ["SWOT 清单", "交叉策略", "行动计划"], "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面画四象限并交叉推导"}
    },
    {
        "id": "pestel", "name": "PESTEL 宏观扫描", "name_en": "PESTEL Analysis",
        "category": "商业分析", "evidence": "anecdotal", "evidence_refs": [],
        "description": "从政治、经济、社会、技术、环境、法律六个维度扫描宏观环境，判断大势对对象的影响方向。",
        "when_to_use": ["进入新市场或新地域", "评估宏观大势影响", "战略规划的环境扫描"],
        "when_not_to_use": ["微观运营问题（用不上宏观扫描）"],
        "params": {"type": "object", "required": ["scope"], "properties": {"scope": {"type": "string", "description": "要扫描宏观环境的对象或市场"}}},
        "steps": [
            {"id": "scan", "name": "逐维扫描", "duration_min": 15,
             "instruction": "对政治、经济、社会、技术、环境、法律六个维度，各列 1-2 个影响对象的外部因素。",
             "checkpoint": "六维度各有因素；且每条标注了对对象是利好还是利空",
             "output": "PESTEL 清单"},
            {"id": "direction", "name": "判影响方向", "duration_min": 8,
             "instruction": "给每个因素标一个影响方向，即助推或阻碍，和强弱，只基于事实不臆测。",
             "checkpoint": "每个因素有方向与强弱判断",
             "output": "影响方向表"},
            {"id": "key", "name": "找关键外力", "duration_min": 5,
             "instruction": "选出强弱最高的 2-3 个因素作为关键外力，它们最可能改变格局。",
             "checkpoint": "关键外力 2-3 个被选出；且依据强弱排序",
             "output": "关键外力"},
            {"id": "respond", "name": "定应对", "duration_min": 6,
             "instruction": "对每个关键外力写一条应对动作，借势或避险，并带上时间。",
             "checkpoint": "每个关键外力都有应对动作；且动作带时间",
             "output": "应对计划", "fail_to": "scan"}
        ],
        "evaluate": {"self_check": ["我的因素是查证的事实还是感觉？", "关键外力真的强弱最高吗？"], "success_criteria": ["每个关键外力有应对", "应对基于影响方向"]},
        "agent_contract": {"input": ["scope"], "output": ["PESTEL 清单", "应对计划"], "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面六格逐维扫描"}
    },
    {
        "id": "porter-five-forces", "name": "波特五力", "name_en": "Porter's Five Forces",
        "category": "商业分析", "evidence": "anecdotal", "evidence_refs": [],
        "description": "用现有竞争、潜在进入者、替代品、供方与买方议价力五种力量评估一个行业的吸引力。",
        "when_to_use": ["评估要不要进入一个行业", "分析行业利润空间", "竞争格局判断"],
        "when_not_to_use": ["单个企业微观运营优化"],
        "params": {"type": "object", "required": ["industry"], "properties": {"industry": {"type": "string", "description": "要评估的行业"}}},
        "steps": [
            {"id": "assess", "name": "逐力评估", "duration_min": 15,
             "instruction": "对现有竞争、潜在进入者、替代品、供方议价、买方议价五种力量各评一个强中弱，并写一条支撑事实。",
             "checkpoint": "五种力量各有强弱评级；且每条有事实支撑",
             "output": "五力评级"},
            {"id": "profit", "name": "判行业吸引力", "duration_min": 6,
             "instruction": "据五力强弱判断行业整体吸引力：力量越弱行业越有利可图。",
             "checkpoint": "给出了行业吸引力结论；且结论可由五力推出",
             "output": "吸引力结论"},
            {"id": "strong", "name": "定位最强力量", "duration_min": 4,
             "instruction": "标出对行业利润威胁最大的那股力量，它是主要矛盾。",
             "checkpoint": "标出了最强威胁力量",
             "output": "主要矛盾"},
            {"id": "strategy", "name": "定对策", "duration_min": 6,
             "instruction": "针对最强力量写一条应对策略，如建立壁垒、差异化或重新定位。",
             "checkpoint": "给出了针对最强力量的应对策略",
             "output": "对策", "fail_to": "assess"}
        ],
        "evaluate": {"self_check": ["五力评级有事实支撑吗？", "我是不是漏评了替代品这一力？"], "success_criteria": ["五力齐全且有据", "对策对准最强力量"]},
        "agent_contract": {"input": ["industry"], "output": ["五力评级", "吸引力结论", "对策"], "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面五力逐条评级"}
    },
    {
        "id": "bcg-matrix", "name": "BCG 矩阵", "name_en": "BCG Matrix",
        "category": "商业分析", "evidence": "anecdotal", "evidence_refs": [],
        "description": "按市场增长率和相对份额把业务分到明星、金牛、问题、瘦狗四象限，据象限配资源。",
        "when_to_use": ["多业务线配资源", "决定投入还是砍掉", "产品组合审视"],
        "when_not_to_use": ["单一业务（无需组合管理）"],
        "params": {"type": "object", "required": ["businesses"], "properties": {"businesses": {"type": "string", "description": "要分类的业务或产品清单"}}},
        "steps": [
            {"id": "place", "name": "放四象限", "duration_min": 12,
             "instruction": "给每个业务按市场增长率高低和相对份额高低，放入明星、金牛、问题、瘦狗四象限。",
             "checkpoint": "每个业务都归入唯一象限；且高低有数据依据",
             "output": "BCG 矩阵"},
            {"id": "role", "name": "定各象限角色", "duration_min": 6,
             "instruction": "给四象限定角色：明星加投、金牛供血、问题选择性投、瘦狗收缩或退出。",
             "checkpoint": "四个象限各有明确角色定位",
             "output": "角色定位"},
            {"id": "allocate", "name": "配资源", "duration_min": 8,
             "instruction": "据角色给每个业务分配资源，金牛的产出优先供明星。",
             "checkpoint": "每个业务有资源处置；且金牛产出被导向明星",
             "output": "资源配置"},
            {"id": "review", "name": "定期复评", "duration_min": 6,
             "instruction": "定期用新数据重放矩阵，看业务是否发生象限迁移，据此再调配。",
             "checkpoint": "完成了复评；且记录了象限迁移",
             "output": "复评结果", "fail_to": "place"}
        ],
        "evaluate": {"self_check": ["高低划分有数据还是拍的？", "金牛的血真的输送给明星了吗？"], "success_criteria": ["每个业务有明确处置", "资源配置随象限迁移调整"]},
        "agent_contract": {"input": ["businesses"], "output": ["BCG 矩阵", "资源配置"], "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面画四象限并逐业务落位"}
    },
    {
        "id": "ansoff", "name": "安索夫矩阵", "name_en": "Ansoff Matrix",
        "category": "商业分析", "evidence": "anecdotal", "evidence_refs": [],
        "description": "按产品与市场的新旧组合出渗透、开发、产品开发、多元化四条增长路径并选主攻。",
        "when_to_use": ["寻找增长方向", "决定推新品还是拓新市场", "增长策略选择"],
        "when_not_to_use": ["只想优化现有业务效率（用运营改进法）"],
        "params": {"type": "object", "required": ["business"], "properties": {"business": {"type": "string", "description": "要求增长的业务"}}},
        "steps": [
            {"id": "map", "name": "填四格路径", "duration_min": 10,
             "instruction": "按产品与市场的新旧组合，填出市场渗透、市场开发、产品开发、多元化四条路径，各写一句做法。",
             "checkpoint": "四格路径各有一句做法",
             "output": "安索夫四格"},
            {"id": "assess", "name": "评估风险收益", "duration_min": 8,
             "instruction": "给每条路径按风险和潜在收益各评高低，通常渗透最稳、多元化最险。",
             "checkpoint": "每条路径有风险与收益评级",
             "output": "路径评级"},
            {"id": "pick", "name": "选主攻路径", "duration_min": 6,
             "instruction": "结合自身资源选一条主攻路径和一条备选，写明选择依据。",
             "checkpoint": "选出了主攻与备选路径；且写明了依据",
             "output": "主攻路径"},
            {"id": "plan", "name": "定首步", "duration_min": 6,
             "instruction": "为主攻路径写第一个可执行动作和验证指标。",
             "checkpoint": "主攻路径有首步动作与验证指标",
             "output": "首步计划", "fail_to": "map"}
        ],
        "evaluate": {"self_check": ["路径评估是基于资源还是跟风？", "多元化是不是被我想得太美？"], "success_criteria": ["选定主攻路径且有依据", "首步可执行可验证"]},
        "agent_contract": {"input": ["business"], "output": ["安索夫四格", "主攻路径", "首步计划"], "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面画四格并逐格填做法"}
    },
    {
        "id": "value-chain", "name": "价值链分析", "name_en": "Value Chain Analysis",
        "category": "商业分析", "evidence": "anecdotal", "evidence_refs": [],
        "description": "把经营活动拆成主要活动与支持活动，逐环找成本与差异点，定位竞争优势所在环节。",
        "when_to_use": ["想找到自己的竞争优势来源", "降本或提质不知从哪环下手", "与对手逐环对比"],
        "when_not_to_use": ["只关心单一环节优化（直接优化即可）"],
        "params": {"type": "object", "required": ["business"], "properties": {"business": {"type": "string", "description": "要拆解价值链的业务"}}},
        "steps": [
            {"id": "decompose", "name": "拆活动", "duration_min": 12,
             "instruction": "把业务拆成主要活动，如进货、生产、出货、营销、服务，和支持活动，如人力、技术、采购、基建，逐环列出。",
             "checkpoint": "主要与支持活动都被拆出；且每环有描述",
             "output": "价值链图"},
            {"id": "cost-diff", "name": "逐环找差异", "duration_min": 12,
             "instruction": "逐环对比自身与主要对手，标出成本更低或价值更高的环节。",
             "checkpoint": "每环都有与对手的对比标注",
             "output": "差异环节"},
            {"id": "advantage", "name": "定位优势环节", "duration_min": 6,
             "instruction": "选出成本或价值差异最大的 1-2 个环节，即为竞争优势来源。",
             "checkpoint": "选出了 1-2 个优势环节；且依据差异排序",
             "output": "优势环节"},
            {"id": "reinforce", "name": "强化或补短", "duration_min": 6,
             "instruction": "对优势环决定如何放大，对明显短板决定自建还是外包，各写一条动作。",
             "checkpoint": "优势环有放大动作；短板有自建或外包决策",
             "output": "行动", "fail_to": "decompose"}
        ],
        "evaluate": {"self_check": ["我拆的活动覆盖全流程了吗？", "优势环节是数据对比出来的吗？"], "success_criteria": ["定位到具体优势环节", "每个关键环有明确处置"]},
        "agent_contract": {"input": ["business"], "output": ["价值链图", "优势环节", "行动"], "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面画价值链并逐环对比"}
    },
    {
        "id": "business-model-canvas", "name": "商业模式画布", "name_en": "Business Model Canvas",
        "category": "商业分析", "evidence": "anecdotal", "evidence_refs": [],
        "description": "用九宫格一次说清客户、价值、渠道、收入、资源、活动、伙伴、成本，把商业模式摆到一页纸。",
        "when_to_use": ["设计或审视商业模式", "创业立项梳理", "向他人讲清商业模式"],
        "when_not_to_use": ["只想验证单一假设（用精益画布更轻）"],
        "params": {"type": "object", "required": ["business"], "properties": {"business": {"type": "string", "description": "要梳理商业模式的业务"}}},
        "steps": [
            {"id": "fill", "name": "逐格填写", "duration_min": 20,
             "instruction": "按九格逐格填写客户细分、价值主张、渠道、客户关系、收入来源、核心资源、关键活动、重要伙伴、成本结构。",
             "checkpoint": "九格全部填写；且每格内容具体非空话",
             "output": "九宫格草稿"},
            {"id": "coherence", "name": "检查一致性", "duration_min": 10,
             "instruction": "检查价值主张与客户细分是否匹配、渠道能否触达、收入能否覆盖成本，标出不匹配处。",
             "checkpoint": "标出了不匹配环节；且覆盖主张、客户、渠道、收入、成本五者对账",
             "output": "一致性检查"},
            {"id": "risk", "name": "找最弱一格", "duration_min": 5,
             "instruction": "选出九格中最薄弱或最不确定的一格，它是模式的最大风险点。",
             "checkpoint": "标出了最薄弱一格",
             "output": "风险点"},
            {"id": "test", "name": "设计验证", "duration_min": 8,
             "instruction": "针对最弱一格设计一个最小验证动作和判定标准。",
             "checkpoint": "给出了最弱格的验证动作与判定标准",
             "output": "验证计划", "fail_to": "fill"}
        ],
        "evaluate": {"self_check": ["九格我是真填满了，还是几格空的？", "最弱格是真风险还是我回避的地方？"], "success_criteria": ["九格完整且对账一致", "最弱格有可执行验证"]},
        "agent_contract": {"input": ["business"], "output": ["九宫格草稿", "一致性检查", "验证计划"], "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面画九宫格逐格填写"}
    },
    # ============================== 商业战略（+3）==============================
    {
        "id": "positioning", "name": "定位理论", "name_en": "Positioning",
        "category": "商业战略", "evidence": "anecdotal", "evidence_refs": [],
        "description": "在目标客户心智中为一个品牌或产品占据一个独特且清晰的位置，用差异化对抗同质竞争。",
        "when_to_use": ["同质化竞争想差异化", "品牌或产品定位不清", "想占据一个清晰心智位置"],
        "when_not_to_use": ["全新品类尚无对手（先做品类教育）"],
        "params": {"type": "object", "required": ["brand"], "properties": {"brand": {"type": "string", "description": "要定位的品牌或产品"}}},
        "steps": [
            {"id": "competitor", "name": "列竞品心智占位", "duration_min": 10,
             "instruction": "列出主要竞品在客户心智中已占据的位置，找出无人占据或占据薄弱的空位。",
             "checkpoint": "列出了竞品占位；且标出了空位",
             "output": "竞品占位图"},
            {"id": "define", "name": "定义独特位置", "duration_min": 8,
             "instruction": "为品牌写一句在目标客户心智中的独特定位，须与竞品占位明显不同。",
             "checkpoint": "定位句写出；且与竞品占位不重合",
             "output": "定位陈述"},
            {"id": "support", "name": "找支撑点", "duration_min": 8,
             "instruction": "列出 2-3 个能支撑这一定位的产品或事实依据，支撑不住就调整定位。",
             "checkpoint": "定位有 2-3 个支撑点；且支撑点属实",
             "output": "支撑点"},
            {"id": "align", "name": "对齐动作", "duration_min": 6,
             "instruction": "检查产品、传播、渠道是否都在强化这一定位，标出偏离的动作并纠正。",
             "checkpoint": "标出了偏离定位的动作；且给出了纠正",
             "output": "对齐结果", "fail_to": "define"}
        ],
        "evaluate": {"self_check": ["我的定位是真差异，还是换了说法的同质？", "支撑点撑得起定位吗？"], "success_criteria": ["定位与竞品明显区隔", "各触点动作对齐定位"]},
        "agent_contract": {"input": ["brand"], "output": ["定位陈述", "支撑点", "对齐结果"], "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面列竞品占位并找空位"}
    },
    {
        "id": "second-curve", "name": "第二曲线", "name_en": "Second Curve",
        "category": "商业战略", "evidence": "anecdotal", "evidence_refs": [],
        "description": "在主营业务见顶前提前布局并投入新增长曲线，用第一曲线的资源养第二曲线接力。",
        "when_to_use": ["主业增长见顶", "想提前布局新增长", "避免被单一业务锁死"],
        "when_not_to_use": ["主业仍在高速增长且无资源余量时"],
        "params": {"type": "object", "required": ["business"], "properties": {"business": {"type": "string", "description": "当前主营业务"}}},
        "steps": [
            {"id": "diagnose", "name": "判断主业阶段", "duration_min": 8,
             "instruction": "用增长数据和市场饱和度判断主业处于导入、成长、成熟还是衰退，标出距见顶的时间。",
             "checkpoint": "给出了主业阶段判断；且估出了距见顶时间",
             "output": "阶段诊断"},
            {"id": "scout", "name": "寻找第二曲线", "duration_min": 12,
             "instruction": "列出 2-3 个可能的新增长方向，各写它为什么能接力、需要什么资源。",
             "checkpoint": "候选方向 2-3 个；且各有接力理由与资源需求",
             "output": "候选曲线"},
            {"id": "seed", "name": "投入种子资源", "duration_min": 10,
             "instruction": "用主业现金流给最有潜力的方向投一小笔种子资源和一个小团队，设独立考核。",
             "checkpoint": "种子资源与团队到位；且第二曲线有独立考核",
             "output": "种子项目"},
            {"id": "handover", "name": "规划接力", "duration_min": 6,
             "instruction": "定下第二曲线接力的触发条件和时间表，避免与主业抢同一资源。",
             "checkpoint": "接力条件与时间表写明；且资源冲突有规避",
             "output": "接力计划", "fail_to": "scout"}
        ],
        "evaluate": {"self_check": ["我是真在布局第二曲线，还是主业一忙就停了？", "种子项目有独立空间吗？"], "success_criteria": ["第二曲线获得持续投入", "接力条件明确可触发"]},
        "agent_contract": {"input": ["business"], "output": ["阶段诊断", "候选曲线", "接力计划"], "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面诊断主业并列候选方向"}
    },
    {
        "id": "flywheel", "name": "飞轮效应", "name_en": "Flywheel Effect",
        "category": "商业战略", "evidence": "anecdotal", "evidence_refs": [],
        "description": "找出能自我强化的关键动作循环，让每个环节推动下一环节，越转越快形成复利。",
        "when_to_use": ["想找到增长飞轮", "各动作各自为战没形成复利", "想用系统替代单点发力"],
        "when_not_to_use": ["业务初期关键环节尚未验证（先验证单点）"],
        "params": {"type": "object", "required": ["business"], "properties": {"business": {"type": "string", "description": "要找飞轮的业务"}}},
        "steps": [
            {"id": "loop", "name": "画出飞轮", "duration_min": 12,
             "instruction": "找出 3-5 个能互相推动的关键动作，画成一个闭环，每步写出它如何推动下一步。",
             "checkpoint": "飞轮 3-5 步成环；且每步有推动下一步的说明",
             "output": "飞轮图"},
            {"id": "entry", "name": "选入口", "duration_min": 5,
             "instruction": "选一个最容易推动的环节作为飞轮入口，先让它转起来。",
             "checkpoint": "选定了入口环节；且它是最易推动的",
             "output": "飞轮入口"},
            {"id": "push", "name": "单点突破", "duration_min": 15,
             "instruction": "集中资源推动入口环节，观察它是否带动下一环，记录传导效果。",
             "checkpoint": "入口环节被集中推动；且记录了向下一环的传导",
             "output": "传导记录"},
            {"id": "measure", "name": "测转速", "duration_min": 6,
             "instruction": "用一个核心指标测飞轮转速，定期看它是否在加快，慢了就找卡住的环节。",
             "checkpoint": "设了转速指标；且定期记录了转速变化",
             "output": "转速曲线", "fail_to": "loop"}
        ],
        "evaluate": {"self_check": ["我的飞轮是真闭环，还是硬凑的因果？", "入口环节真的带动下一环了吗？"], "success_criteria": ["飞轮形成闭环传导", "转速指标持续加快"]},
        "agent_contract": {"input": ["business"], "output": ["飞轮图", "传导记录", "转速曲线"], "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面画闭环并找入口"}
    },
    # ============================== 商业管理（+3）==============================
    {
        "id": "okr", "name": "OKR 目标管理", "name_en": "OKR",
        "category": "商业管理", "evidence": "anecdotal", "evidence_refs": [],
        "description": "设定一个有挑战的目标和 3-4 个可衡量的关键结果，用关键结果的完成度驱动目标，聚焦优先事项。",
        "when_to_use": ["团队对齐聚焦重点", "想设定有挑战的目标", "季度目标管理"],
        "when_not_to_use": ["目标常规无挑战（用任务清单即可）"],
        "params": {"type": "object", "required": ["team"], "properties": {"team": {"type": "string", "description": "要设 OKR 的团队"}}},
        "steps": [
            {"id": "objective", "name": "定目标", "duration_min": 6,
             "instruction": "写一个定性的、有挑战、能鼓舞人的目标，一个周期只定一个主目标。",
             "checkpoint": "目标唯一且定性有挑战",
             "output": "目标 O"},
            {"id": "kr", "name": "定关键结果", "duration_min": 10,
             "instruction": "为目标定 3-4 个可衡量的关键结果，每个带基线值和目标值。",
             "checkpoint": "关键结果 3-4 个；且每个有基线与目标值",
             "output": "关键结果 KR"},
            {"id": "align", "name": "对齐与拆解", "duration_min": 8,
             "instruction": "把每个 KR 拆到团队或个人，确认每人知道自己负责哪个 KR 的哪部分。",
             "checkpoint": "每个 KR 都有负责人；且拆解到人",
             "output": "责任对齐"},
            {"id": "track", "name": "定期打分", "duration_min": 10,
             "instruction": "每周给每个 KR 打 0 到 1 的完成分，低于预期就调整资源或改 KR，不攒到期末。",
             "checkpoint": "每周有 KR 打分；且低分 KR 有调整动作",
             "output": "打分记录", "fail_to": "kr"}
        ],
        "evaluate": {"self_check": ["我的 KR 是真可衡量，还是定性描述？", "打分我是诚实打的还是都打高分？"], "success_criteria": ["KR 完成度可量化", "低分 KR 被及时调整"]},
        "agent_contract": {"input": ["team"], "output": ["目标与 KR", "责任对齐", "打分记录"], "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面写 O 与 KR 并每周打分"}
    },
    {
        "id": "kpi", "name": "KPI 绩效指标", "name_en": "KPI",
        "category": "商业管理", "evidence": "anecdotal", "evidence_refs": [],
        "description": "把战略拆成少数可量化的关键绩效指标，用指标牵引行为并定期复盘达成。",
        "when_to_use": ["想把战略变成可追踪数字", "团队缺量化牵引", "绩效管理"],
        "when_not_to_use": ["目标无法量化或处于探索期（用 OKR 更合适）"],
        "params": {"type": "object", "required": ["role"], "properties": {"role": {"type": "string", "description": "要设 KPI 的团队或岗位"}}},
        "steps": [
            {"id": "derive", "name": "从目标导 KPI", "duration_min": 8,
             "instruction": "从团队目标出发，导出 3-5 个能反映目标达成的关键指标，每个注明它服务哪个目标。",
             "checkpoint": "KPI 3-5 个；且每个标注了对应目标",
             "output": "KPI 清单"},
            {"id": "baseline", "name": "定基线与目标值", "duration_min": 6,
             "instruction": "给每个 KPI 定当前基线值和周期目标值，目标值要有挑战但可达。",
             "checkpoint": "每个 KPI 有基线与目标值",
             "output": "KPI 目标表"},
            {"id": "instrument", "name": "建采集", "duration_min": 8,
             "instruction": "定每个 KPI 的数据来源和采集频率，确保数字可自动或半自动取得。",
             "checkpoint": "每个 KPI 有数据来源与频率",
             "output": "采集方案"},
            {"id": "review", "name": "定期复盘", "duration_min": 10,
             "instruction": "按周期复盘各 KPI 达成，分析未达成的根因并定改进，而非只报数字。",
             "checkpoint": "每个 KPI 有达成复盘；未达者有根因与改进",
             "output": "复盘报告", "fail_to": "derive"}
        ],
        "evaluate": {"self_check": ["KPI 是真反映目标，还是只挑好看的？", "复盘我是在找根因，还是只报数字？"], "success_criteria": ["KPI 可由数据取得", "未达 KPI 有根因分析"]},
        "agent_contract": {"input": ["role"], "output": ["KPI 目标表", "采集方案", "复盘报告"], "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面列 KPI 并定期手记达成"}
    },
    {
        "id": "balanced-scorecard", "name": "平衡计分卡", "name_en": "Balanced Scorecard",
        "category": "商业管理", "evidence": "anecdotal", "evidence_refs": [],
        "description": "从财务、客户、内部流程、学习成长四个维度设定指标，用四维平衡避免只盯财务短视。",
        "when_to_use": ["想平衡长期与短期", "只用财务指标导致短视", "战略落地到多维度"],
        "when_not_to_use": ["小微企业维度太多反而重"],
        "params": {"type": "object", "required": ["org"], "properties": {"org": {"type": "string", "description": "要用平衡计分卡的组织"}}},
        "steps": [
            {"id": "four", "name": "四维定指标", "duration_min": 15,
             "instruction": "在财务、客户、内部流程、学习成长四个维度各定 2-3 个指标，每个注明对应战略。",
             "checkpoint": "四维度各有 2-3 个指标；且每个标注对应战略",
             "output": "四维指标"},
            {"id": "target", "name": "定目标值", "duration_min": 8,
             "instruction": "给每个指标定基线值和周期目标值。",
             "checkpoint": "每个指标有基线与目标值",
             "output": "目标值表"},
            {"id": "link", "name": "找因果链", "duration_min": 8,
             "instruction": "画出学习成长驱动内部流程、流程驱动客户、客户驱动财务的因果链，确认指标互相支撑。",
             "checkpoint": "画出了四维因果链；且指标沿链支撑",
             "output": "因果链"},
            {"id": "review", "name": "四维复盘", "duration_min": 10,
             "instruction": "按周期四维一起复盘，避免只升财务而降其它三维，记录四维均衡度。",
             "checkpoint": "四维均有复盘；且记录了均衡度",
             "output": "复盘报告", "fail_to": "four"}
        ],
        "evaluate": {"self_check": ["我是不是又在财务维度放最多指标？", "因果链是真驱动还是硬连？"], "success_criteria": ["四维指标均衡", "复盘覆盖四维而非只财务"]},
        "agent_contract": {"input": ["org"], "output": ["四维指标", "因果链", "复盘报告"], "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面四象限各列指标并连因果"}
    },
    # ============================== 商业表达（+2）==============================
    {
        "id": "pyramid-principle", "name": "金字塔原理", "name_en": "Pyramid Principle",
        "category": "商业表达", "evidence": "anecdotal", "evidence_refs": [],
        "description": "表达时结论先行、以上统下、归类分组、逻辑递进，先给塔顶结论再用下层论据支撑。",
        "when_to_use": ["写报告或汇报想清晰有力", "对方时间有限要结论先行", "表达混乱需结构化"],
        "when_not_to_use": ["纯创意发散阶段（先发散再套结构）"],
        "params": {"type": "object", "required": ["topic"], "properties": {"topic": {"type": "string", "description": "要结构化表达的主题"}}},
        "steps": [
            {"id": "top", "name": "先写顶层结论", "duration_min": 6,
             "instruction": "先用一句话写出整个表达的核心结论，放在最顶端。",
             "checkpoint": "写出了一句核心结论作为塔顶",
             "output": "顶层结论"},
            {"id": "group", "name": "归类下层论据", "duration_min": 10,
             "instruction": "把支撑结论的论据归成 3-5 组作为第二层，组间不重叠。",
             "checkpoint": "论据归成 3-5 组；且组间不重叠",
             "output": "第二层分组"},
            {"id": "order", "name": "逻辑递进", "duration_min": 8,
             "instruction": "给每组和组内论据按逻辑排序，如时间、结构、重要性，确保读起来有推进感。",
             "checkpoint": "每组及组内都有明确排序依据",
             "output": "排序后金字塔"},
            {"id": "check", "name": "自上而下检验", "duration_min": 6,
             "instruction": "从塔顶往下问：这个结论被这些组支撑吗？每组被其下论据支撑吗？断链处补上。",
             "checkpoint": "每层都被下层支撑；且断链处被补齐",
             "output": "检验后的金字塔", "fail_to": "group"}
        ],
        "evaluate": {"self_check": ["我真是结论先行，还是先铺垫半天？", "每一层都被下层撑住了吗？"], "success_criteria": ["塔顶结论一句话说清", "金字塔无断链"]},
        "agent_contract": {"input": ["topic"], "output": ["金字塔结构"], "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸面画金字塔并自上而下检验"}
    },
    {
        "id": "prep", "name": "PREP 表达", "name_en": "PREP Expression",
        "category": "商业表达", "evidence": "anecdotal", "evidence_refs": [],
        "description": "按观点、理由、例证、重申观点四步组织一段表达，让每段话都有论点有支撑。",
        "when_to_use": ["即兴发言想有结构", "写短文或回复", "训练清晰表达"],
        "when_not_to_use": ["长篇报告（用金字塔原理更全）"],
        "params": {"type": "object", "required": ["point"], "properties": {"point": {"type": "string", "description": "要表达的观点"}}},
        "steps": [
            {"id": "point", "name": "亮观点", "duration_min": 3,
             "instruction": "第一句直接说出你的观点，不含糊不铺垫。",
             "checkpoint": "第一句为明确观点句",
             "output": "观点 P"},
            {"id": "reason", "name": "给理由", "duration_min": 5,
             "instruction": "紧跟一句支撑观点的核心理由，说明为什么这么看。",
             "checkpoint": "写出了支撑观点的理由",
             "output": "理由 R"},
            {"id": "example", "name": "举例证", "duration_min": 8,
             "instruction": "补一个具体例子或数据佐证理由，例子要能真的支撑理由。",
             "checkpoint": "例子与理由相关且能佐证",
             "output": "例证 E"},
            {"id": "restate", "name": "重申观点", "duration_min": 3,
             "instruction": "最后一句重申观点并可带一个行动或结论，收束全段。",
             "checkpoint": "末句重申了观点或给出行动",
             "output": "重申 P", "fail_to": "reason"}
        ],
        "evaluate": {"self_check": ["我的观点是真的明确，还是和稀泥？", "例子真能支撑理由吗？"], "success_criteria": ["四步齐全且顺序正确", "例子与观点强相关"]},
        "agent_contract": {"input": ["point"], "output": ["PREP 段落"], "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：口头按四步组织"}
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

    print("商业子库新增 %d 个：" % len(created))
    for c in created:
        print("  +", c)
    if skipped:
        print("\n跳过 %d 个（已存在）：%s" % (len(skipped), ", ".join(skipped)))


if __name__ == "__main__":
    main()
