#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenLMP 第二批扩充：70 → 78（新增 8 个）。
来源：METHOD-UNIVERSE 候选队列中「干净落在现有 8 大类、与已收录低重叠」者。
硬约束同前：category ∈ 八类；checkpoint 禁模糊词；instruction 禁自行决定/视情况而定；
全文纯度扫描（禁 注册/登录/API Key/上传云端/订阅付费/引流微信）。
"""
import json, os, sys, datetime

OUT = sys.argv[1] if len(sys.argv) > 1 else "E:/视频创作/AIST2030/openlmp/skills"
TODAY = datetime.date.today().isoformat()

NEW = [
    # ============================== 记忆巩固（+2）==============================
    {
        "id": "sleep-wake-memory", "name": "睡前醒后记忆", "name_en": "Sleep-Wake Memory",
        "category": "记忆巩固", "evidence": "anecdotal", "evidence_refs": [],
        "description": "把难记的材料安排在睡前过一遍、醒后先测一遍，利用睡眠巩固和前后摄干扰少的窗口提升保持率。",
        "when_to_use": ["记了就忘", "有连夜的记忆任务", "想利用睡眠巩固"],
        "when_not_to_use": ["第二天一早就考的临场内容（直接集中背更即时）"],
        "params": {
            "type": "object", "required": ["material"],
            "properties": {"material": {"type": "string", "description": "要睡前编码的材料"}}
        },
        "steps": [
            {"id": "schedule", "name": "选定材料与时段", "duration_min": 4,
             "instruction": "选定要记的材料，安排在睡前 30 分钟内过一遍，并约定次日醒后先测再干别的事。",
             "checkpoint": "写下了材料与睡前时段；且约定醒后先测",
             "output": "记忆计划"},
            {"id": "encode", "name": "睡前精细编码", "duration_min": 20,
             "instruction": "睡前逐条过材料，每条用自己的话复述并想一个例子；不解的标记，不硬背。",
             "checkpoint": "每条都有自述复述；且不解处被标记",
             "output": "睡前编码记录"},
            {"id": "retrieve", "name": "醒后先测", "duration_min": 10,
             "instruction": "醒来第一件事，在看手机前合上材料，把能想起的写出或说出，标出想不出的。",
             "checkpoint": "醒后已先于其他活动完成一次回忆；且想不出的条目标出",
             "output": "晨间回忆结果"},
            {"id": "target", "name": "只补晨间缺口", "duration_min": 12,
             "instruction": "只对晨间想不出的条目重点巩固，已想起的快速过；连续几天重复此循环。",
             "checkpoint": "仅晨间缺口条目被重点巩固；且循环天数已记录",
             "output": "巩固记录", "fail_to": "encode"}
        ],
        "evaluate": {
            "self_check": ["我醒后是真的先测，还是先刷了手机？", "晨间想不出的，是没编码好还是没睡够？"],
            "success_criteria": ["晨间回忆率高于无睡前编码时", "连续几晚缺口逐晚减少"]
        },
        "agent_contract": {
            "input": ["material"], "output": ["记忆计划", "晨间回忆结果", "巩固记录"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：睡前列清单、醒后口头自测"
        }
    },
    {
        "id": "mnemonic-association", "name": "谐音联想法", "name_en": "Mnemonic Association",
        "category": "记忆巩固", "evidence": "anecdotal", "evidence_refs": [],
        "description": "把要记的无意义材料用谐音、图像、故事强行挂到熟悉事物上，化抽象为具体、化无序为有序。",
        "when_to_use": ["记无意义材料，如术语、编号、词表", "纯死记总忘", "需要快速记一批条目"],
        "when_not_to_use": ["需要精确用法的复杂概念（联想只作钩子，会引入偏差）"],
        "params": {
            "type": "object", "required": ["items"],
            "properties": {"items": {"type": "string", "description": "要记的条目清单"}}
        },
        "steps": [
            {"id": "list", "name": "列出待记条目", "duration_min": 5,
             "instruction": "把要记的条目列成清单，每条限定为一个最小记忆单元。",
             "checkpoint": "清单条目至少 5 条；且每条为最小记忆单元",
             "output": "待记清单"},
            {"id": "hook", "name": "逐条造联想", "duration_min": 15,
             "instruction": "为每条造一个谐音或形象联想，写成一个具体画面或小故事，越夸张越好。",
             "checkpoint": "每条都配了一个具体画面或故事；且无空白联想的条目",
             "output": "联想表"},
            {"id": "encode", "name": "复述联想", "duration_min": 8,
             "instruction": "盖住原条目，只看联想表复述对应内容，卡住的强化那个画面。",
             "checkpoint": "每条都经过一次据联想复述；且卡住条目被强化",
             "output": "复述结果"},
            {"id": "decay", "name": "隔时重测", "duration_min": 8,
             "instruction": "隔一段时间，如当晚和隔天，重测并统计仍靠联想才想起的条目，淘汰想不起来的联想并重造。",
             "checkpoint": "完成了隔时重测；且想不起来的联想被重造",
             "output": "重测与迭代", "fail_to": "hook"}
        ],
        "evaluate": {
            "self_check": ["我的联想是真有画面，还是只是换个词？", "隔天后，是联想在帮我还是我已直接记住了？"],
            "success_criteria": ["隔时重测保持率高于纯死记", "多数条目最终脱离联想也能想起"]
        },
        "agent_contract": {
            "input": ["items"], "output": ["联想表", "重测结果"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：口头编故事并复述"
        }
    },
    # ============================== 评测验证（+1）==============================
    {
        "id": "blank-sheet-daily", "name": "白纸默写法", "name_en": "Daily Blank-Sheet Recall",
        "category": "评测验证", "evidence": "anecdotal", "evidence_refs": [],
        "description": "每天固定拿一张白纸，限时把当天所学默写出来，用还原度衡量真实掌握，并看长期曲线。",
        "when_to_use": ["想每天检验掌握度", "学了但说不清学会了什么", "追踪长期保持曲线"],
        "when_not_to_use": ["当天几乎没学新内容（无料可默）"],
        "params": {
            "type": "object", "required": [],
            "properties": {"minutes": {"type": "integer", "default": 10, "description": "每日默写限时分钟"}}
        },
        "steps": [
            {"id": "setup", "name": "定时定点", "duration_min": 3,
             "instruction": "固定每天一个时段，如睡前，和一张白纸作为每日默写仪式；先想后写。",
             "checkpoint": "时段与形式已固定；且连续执行天数已记录",
             "output": "默写计划"},
            {"id": "dump", "name": "限时默写", "duration_min": 10,
             "instruction": "在 minutes 内，不看任何资料，把当天所学尽量写出或画出；想不出的留空并标记。",
             "checkpoint": "在限定时间内产出默写稿；且想不出处被留空标记",
             "output": "默写稿"},
            {"id": "diff", "name": "对照补全", "duration_min": 6,
             "instruction": "现在才对照当天材料，标出默写稿中遗漏和错误的部分，只标注不改写原文。",
             "checkpoint": "遗漏与错误被逐条标出；且标注阶段未改动默写稿",
             "output": "差异标注"},
            {"id": "trend", "name": "记录还原度", "duration_min": 4,
             "instruction": "估算本次还原度，即写出内容占当天要点的比例，记入曲线；连续走低就回头补前几日缺口。",
             "checkpoint": "给出了本次还原度数值并入曲线；且连续走低时标出了应补的日期",
             "output": "还原度曲线", "fail_to": "dump"}
        ],
        "evaluate": {
            "self_check": ["我默写时是凭记忆，还是脑子在翻当天的笔记？", "还原度低，是没学会还是当时没记全？"],
            "success_criteria": ["还原度曲线整体平稳或上升", "能据曲线定位保持率骤降的知识点"]
        },
        "agent_contract": {
            "input": ["minutes"], "output": ["默写稿", "差异标注", "还原度曲线"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：固定纸笔每日默写并画曲线"
        }
    },
    # ============================== 计划执行（+2）==============================
    {
        "id": "micro-habits", "name": "微习惯", "name_en": "Micro-Habits",
        "category": "计划执行", "evidence": "anecdotal", "evidence_refs": [],
        "description": "把目标缩到小得不可能失败，靠持续不断积累势能，先解决启动难的问题。",
        "when_to_use": ["总是无法开始", "大目标让人望而却步", "想先建立稳定出现频率"],
        "when_not_to_use": ["目标需要一次性高强度完成（微习惯只解决启动）"],
        "params": {
            "type": "object", "required": ["habit"],
            "properties": {"habit": {"type": "string", "description": "想养成的习惯"}}
        },
        "steps": [
            {"id": "shrink", "name": "缩到不可能失败", "duration_min": 4,
             "instruction": "把想养成的习惯缩到一个极小、当天任何状态都能完成的量，如 1 分钟、1 页、1 个。",
             "checkpoint": "习惯被改写为可在 1 分钟内完成的量；且该量在任何状态下可完成",
             "output": "微习惯定义"},
            {"id": "anchor", "name": "挂到既有日程", "duration_min": 4,
             "instruction": "把这个微习惯挂到一个每天必然发生的事之后，如刷牙后，写成做了某件事就做微习惯。",
             "checkpoint": "微习惯被挂到一个每日必发事件后；且写出了触发句式",
             "output": "锚点"},
            {"id": "streak", "name": "记录连续天数", "duration_min": 2,
             "instruction": "每天完成后在日历记一格，重点是连续不中断，哪怕只做了最小量。",
             "checkpoint": "每天完成均有记录；且记录以连续天数为目标",
             "output": "连续记录"},
            {"id": "scale", "name": "稳定后再放大", "duration_min": 3,
             "instruction": "连续两周稳定后才把量上调一档；一旦中断连续记录，就退回上一档而不是放弃。",
             "checkpoint": "上调发生在连续两周稳定后；且中断时退回上一档而非中止",
             "output": "放量记录", "fail_to": "anchor"}
        ],
        "evaluate": {
            "self_check": ["我把量缩到真的不会失败了吗，还是仍偏大？", "中断时我是退档了，还是直接放弃了？"],
            "success_criteria": ["连续出现天数达到目标", "放量后仍能维持不断档"]
        },
        "agent_contract": {
            "input": ["habit"], "output": ["微习惯定义", "连续记录"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸上画连续格记录"
        }
    },
    {
        "id": "energy-management", "name": "精力管理", "name_en": "Energy Management",
        "category": "计划执行", "evidence": "anecdotal", "evidence_refs": [],
        "description": "把任务按体能、情绪、专注几个能量维度排进个人高低谷时段，把高价值事放到高能量时，而非只管理时间。",
        "when_to_use": ["时间表排满了却总完不成", "重要事总被排在低效时段", "下午就疲乏"],
        "when_not_to_use": ["任务时间被外部固定、无调度自由度时"],
        "params": {
            "type": "object", "required": ["tasks"],
            "properties": {"tasks": {"type": "string", "description": "要按能量安排的待办清单"}}
        },
        "steps": [
            {"id": "audit", "name": "记录一周能量曲线", "duration_min": 30,
             "instruction": "连续几天，每小时给体能、情绪、专注三项各打 1-5 分，画出自己的高低谷。",
             "checkpoint": "记录了至少 5 天的逐时段评分；且画出了能量曲线",
             "output": "能量曲线"},
            {"id": "classify", "name": "给任务标能量需求", "duration_min": 8,
             "instruction": "把待办按所需能量分级：高难度或创造类、常规类、恢复类。",
             "checkpoint": "每条任务被标为高能量、常规或恢复三类之一",
             "output": "任务分级"},
            {"id": "match", "name": "高价值配高能量", "duration_min": 10,
             "instruction": "把最重要且需高能量的任务排到个人能量高峰时段；恢复类和琐事排到低谷。",
             "checkpoint": "高能量时段被分配给高价值任务；且低谷时段安排了恢复或琐事",
             "output": "能量排程"},
            {"id": "recover", "name": "插入恢复节律", "duration_min": 15,
             "instruction": "在高峰块之间安排短恢复，如走动、冥想、小憩，并记录恢复后专注度是否回升。",
             "checkpoint": "高峰块之间插入了恢复时段；且记录了恢复后专注度变化",
             "output": "恢复记录", "fail_to": "classify"}
        ],
        "evaluate": {
            "self_check": ["我是按能量排的，还是按惯性把难事排到了犯困时段？", "恢复真的让我回升了，还是只是拖延？"],
            "success_criteria": ["高价值任务完成率上升", "高峰时段专注度评分高于低谷时段"]
        },
        "agent_contract": {
            "input": ["tasks"], "output": ["能量曲线", "能量排程", "恢复记录"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸质记录能量曲线并手排日程"
        }
    },
    # ============================== 元认知（+3）==============================
    {
        "id": "morning-evening-review", "name": "晨间晚间复盘", "name_en": "Morning-Evening Review",
        "category": "元认知", "evidence": "anecdotal", "evidence_refs": [],
        "description": "早晨用三个问题定调一天，晚上用复盘收束一天，两头各几分钟，让行动对齐意图、经验被沉淀。",
        "when_to_use": ["一天过完不知道干了什么", "想建立每日反思闭环", "意图和行动总脱节"],
        "when_not_to_use": ["当天极度特殊，如重病或紧急事件，可跳过不自责"],
        "params": {
            "type": "object", "required": [],
            "properties": {"day": {"type": "string", "default": "", "description": "可选：指定复盘日期，默认今天"}}
        },
        "steps": [
            {"id": "morning", "name": "晨间三问", "duration_min": 5,
             "instruction": "起床后回答三个问题并写下：今天想要什么心态、要好好对待谁、要推进哪一件要事。",
             "checkpoint": "三个问题各有一条书面回答；且其中要事唯一明确",
             "output": "晨间意图"},
            {"id": "carry", "name": "把要事排进日程", "duration_min": 3,
             "instruction": "把晨间定的那件要事排进当天时间表的一个具体时段。",
             "checkpoint": "要事被排到当天某一具体时段",
             "output": "当日要事位"},
            {"id": "evening", "name": "晚间复盘", "duration_min": 8,
             "instruction": "睡前对照晨间意图复盘心态、待人、要事各做到几分，写一条今天学到的和一个明天的改进。",
             "checkpoint": "三项各有自评；且产出了一条今日所得与一条明日改进",
             "output": "晚间复盘"},
            {"id": "loop", "name": "汇总成周视图", "duration_min": 10,
             "instruction": "把每天复盘汇总成周视图，找出反复出现的同一个问题，定为下周唯一改进点。",
             "checkpoint": "周视图已汇总；且高频问题被定为下周唯一改进点",
             "output": "周复盘与改进点", "fail_to": "morning"}
        ],
        "evaluate": {
            "self_check": ["晨间三问我是认真想的，还是走形式？", "反复出现的那个问题，我看见了吗？"],
            "success_criteria": ["要事完成率逐周上升", "每周都产出一个明确改进点"]
        },
        "agent_contract": {
            "input": ["day"], "output": ["晨间意图", "晚间复盘", "周改进点"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：固定本子早晚各写一段"
        }
    },
    {
        "id": "life-wheel", "name": "生命之花", "name_en": "Life Wheel",
        "category": "元认知", "evidence": "anecdotal", "evidence_refs": [],
        "description": "在多个生活维度给自己打分，一眼看出哪块鼓、哪块瘪，用失衡可视化代替感觉还行的自我欺骗。",
        "when_to_use": ["觉得生活失衡却说不出哪失衡", "季度或年度自我盘点", "决定下一阶段重点"],
        "when_not_to_use": ["正处于单一维度冲刺期（短期不平衡是正常的）"],
        "params": {
            "type": "object", "required": [],
            "properties": {"dims": {"type": "integer", "default": 8, "description": "维度数量"}}
        },
        "steps": [
            {"id": "define", "name": "选定维度", "duration_min": 10,
             "instruction": "选定 8 个维度，如健康、家庭、朋友、成长、工作、财务、休闲、贡献，各写一句这个维度好是什么样。",
             "checkpoint": "维度数等于指定值；且每维有一句好的样子描述",
             "output": "维度定义"},
            {"id": "score", "name": "逐维打分", "duration_min": 12,
             "instruction": "每个维度按当前真实状态打 1-10 分，打分时写下支撑这个分的一条事实，不凭感觉。",
             "checkpoint": "每维都有 1-10 分；且每分附了一条支撑事实",
             "output": "打分与依据"},
            {"id": "map", "name": "画成轮图", "duration_min": 6,
             "instruction": "把八个分数画成一个轮子，标出最高和最低的两块，直观看不平衡处。",
             "checkpoint": "产出了轮图；且最高与最低各一块被标出",
             "output": "生命之花轮图"},
            {"id": "act", "name": "只补最低一块", "duration_min": 8,
             "instruction": "为最低分维度定一个下周期的小改进动作，只补这一块，其余维持；下周期重打分看变化。",
             "checkpoint": "为最低维度定了一个具体改进动作；且其余维度本轮不动",
             "output": "改进计划", "fail_to": "score"}
        ],
        "evaluate": {
            "self_check": ["我的打分有事实支撑，还是全是感觉？", "只补最低一块，我忍得住不动其他吗？"],
            "success_criteria": ["最低维度分数下周期上升", "各维度分差逐周期收窄"]
        },
        "agent_contract": {
            "input": ["dims"], "output": ["打分依据", "轮图", "改进计划"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：纸上画八分轮并逐维打分"
        }
    },
    {
        "id": "four-step-review", "name": "四步复盘", "name_en": "Four-Step Retrospective",
        "category": "元认知", "evidence": "anecdotal", "evidence_refs": [],
        "description": "对一段经历或一个项目做结构化复盘：回顾目标、评估结果、分析原因、总结规律，让经验变成可复用资产。",
        "when_to_use": ["做完一个项目或经历一件事", "想从成败里提炼可复用经验", "同类错误反复犯"],
        "when_not_to_use": ["事情还没结束（复盘会变成半成品猜测）"],
        "params": {
            "type": "object", "required": ["event"],
            "properties": {"event": {"type": "string", "description": "要复盘的事件或项目"}}
        },
        "steps": [
            {"id": "goal", "name": "回顾原定目标", "duration_min": 6,
             "instruction": "写下这件事最初想达成什么，尽量引用当时写下的原话，不用现在的记忆篡改。",
             "checkpoint": "写出了初始目标；且尽量引用当时原始表述",
             "output": "初始目标"},
            {"id": "result", "name": "对照实际结果", "duration_min": 8,
             "instruction": "列出实际发生了什么，与初始目标逐条对照，标出达成、未达成、意外三种。",
             "checkpoint": "实际结果逐条列出；且每条被标为达成、未达成或意外",
             "output": "结果对照"},
            {"id": "cause", "name": "分析成败原因", "duration_min": 12,
             "instruction": "对未达成和意外项，区分是方法问题、执行问题还是外部变化，各写主因，不泛泛归因于不够努力。",
             "checkpoint": "每个未达成与意外项都有主因；且主因区分为方法、执行或外部三类之一",
             "output": "原因分析"},
            {"id": "rule", "name": "总结可复用规律", "duration_min": 8,
             "instruction": "写出 1-3 条下次可直接套用的规律或动作，各标注适用条件，然后存入可检索的复盘库。",
             "checkpoint": "产出 1-3 条带适用条件的规律；且已存入复盘库",
             "output": "规律清单", "fail_to": "cause"}
        ],
        "evaluate": {
            "self_check": ["我复盘用的是当时的原话，还是事后编的？", "总结的规律有适用条件，还是放之四海皆准的空话？"],
            "success_criteria": ["规律能在下次同类事中被套用", "复盘库可按主题检索到本条"]
        },
        "agent_contract": {
            "input": ["event"], "output": ["结果对照", "原因分析", "规律清单"],
            "side_effects": ["仅写本地文件"], "degrade_to": "无工具时：按四步纸笔复盘并归档"
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
