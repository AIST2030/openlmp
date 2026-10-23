#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 OpenLMP 主库按「主题批次」拆成多个 SkillHub 发布包。

为什么要拆：SkillHub 上用户是带着问题来搜的。「我想记住东西」命中
「记忆巩固」包的概率，远高于命中「107 个方法」大包。主题聚焦 = 搜索
命中率高 + 采用门槛低 + 每包案例能写透。

与 build_dist.py（全家桶）的区别：
  - 只打包指定 category 的方法
  - registry.json 是**子集**（用 lmp.skill_cid 重算），不是复制全库 107 条
  - SKILL.md 每批定制（Role/Context/案例/约束都针对该主题）
  - 全家桶包保留为总入口，在各分批包的 SKILL.md 里互相索引

用法：
  python build_topic_dist.py memory            # 打记忆巩固批
  python build_topic_dist.py --list            # 列出已配置的批次
  python build_topic_dist.py all               # 打全部已配置批次

新增批次：往 PACKS 里加一项即可，数字（方法数/步数/循证分布）全部动态推导。
"""
import json, os, sys, glob, shutil, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "E:/视频创作/AIST2030/openlmp"

# build_dist.py 位于 openlmp-dist/（构建产物目录，不纳入 git）。本脚本可从
# openlmp/tools/ 或 openlmp-dist/ 任一位置运行，用环境变量覆盖路径即可。
DEFAULT_DIST = os.path.join(os.path.dirname(REPO), "openlmp-dist")
if os.path.basename(HERE) == "tools":
    DEFAULT_DIST = os.path.join(os.path.dirname(os.path.dirname(HERE)), "openlmp-dist")
DIST = os.environ.get("OPENLMP_DIST_DIR", DEFAULT_DIST)
SRC = DIST

sys.path.insert(0, SRC)
sys.path.insert(0, os.path.join(REPO, "runtime"))
import build_dist  # 复用渲染函数，保证手册格式与全家桶完全一致
from lmp import skill_cid

EVIDENCE_CN = build_dist.EVIDENCE_CN

# ---------------------------------------------------------------------------
# 批次配置：新增一批就往这里加一项。文字部分（role/context/案例/约束）必须
# 针对该主题定制，不能用模板套；数字全部由脚本从 JSON 推导，禁止硬编码。
# ---------------------------------------------------------------------------
PACKS = {
    "memory": {
        "slug": "aist2030-openlmp-memory",
        "pkg_id": "AIST2030-openlmp-memory-v1",
        "display_name": "OpenLMP 记忆巩固方法库",
        "categories": ["记忆巩固"],
        "safe_names": {"记忆巩固": "01-memory"},
        "capability": "memory_method_library",
        "tags": ["记忆", "间隔重复", "主动回忆", "遗忘曲线", "学习方法",
                 "背单词", "备考", "记忆宫殿", "spaced repetition", "active recall"],
        "summary": ("15 个记忆巩固方法（主动回忆、间隔重复调度、交错练习、睡眠巩固、"
                    "组块化、双重编码、记忆宫殿等），每个方法拆成步骤、每步配可判定的验收线，"
                    "附零依赖执行器与结构化数据，可被 AI 直接调度。循证等级如实标注："
                    "强证据 4 / 中等 6 / 经验 5。方法内容 CC0 公共领域，协议与执行器木兰宽松许可证 v2，可商用。"),
        "tagline": ("学过的东西过两天就忘、背了又忘、看着眼熟就是想不起来——"
                    "本库把「记不住」拆成编码、存储、提取三个可诊断的环节，"
                    "每个环节给出具体方法与**可判定的验收线**，而不是「多复习几遍」这种正确的废话。"),
        "role": ("你是一名记忆策略教练。你的价值不是「报得出很多记忆法名字」，而是**能判断用户忘在哪个环节**——"
                 "编码没做深（信息没接上意思）、存储没调度（复习时机不对）、还是提取没练（看着眼熟但想不出）——"
                 "然后给对应的方法，并对每一步给出可判定的验收线。你不替用户记，也不承诺「过目不忘」。"),
        "context_extra": ("- **典型场景**：考前突击、长期保持、大量事实性材料（单词 / 法条 / 药名 / 名词解释）、"
                          "「背了就忘」的反复失败。\n"
                          "- **用户画像**：学生、考证人群（法考 / CPA / 医考 / 考研）、需要大量记忆的职业培训学员。"),
        "task": [
            "**诊断**：判断用户卡在哪个环节——编码（没理解没接上意思）、存储（没有复习调度）、还是提取（看着眼熟想不出）",
            "**选型**：针对该环节选方法，说明为什么是它、为什么不是同类备选",
            "**展开**：把每一步变成具体动作，写明产出物（一张卡 / 一份自测题 / 一条复习日程）",
            "**给验收线**：每步一条可判定的 checkpoint，并说明怎么算通过",
            "**给自检**：执行结束时给自检问题与带时间维度的达标判据",
        ],
        "constraint": [
            "**不承诺结果**：不说「过目不忘」「7 天记住一万个单词」。记忆法是提高保持率的工具，不是超能力",
            "**循证如实告知**：本包 15 个方法中强证据 4 个、中等 6 个、经验级 5 个。"
            "经验级方法（回针缝复习、情绪联动记忆、谐音联想、睡前醒后记忆、树状图记忆）是实践总结，"
            "必须如实说，不得包装成「科学验证」",
            "**记忆法不替代理解**：如果用户连材料本身都没理解，先去解决理解问题（理解构建类方法），"
            "不要教人把不懂的东西硬背下来",
            "**checkpoint 必须可判定**：出现「多复习」「加深印象」这类词即不合格，要换成可验证的产出物描述",
            "**不越界**：不提供学科内容本身（不替用户整理考点、不给资料），只给「怎么记」的方法与纪律",
            "输出语言：简体中文",
        ],
        "anti_dup": [
            "信息没进脑子（记不住新东西）→ 编码类：组块化 / 双重编码 / 精细复述 / 谐音联想",
            "学了后面忘前面（保持不住）→ 存储调度类：间隔重复调度 / 回针缝复习 / 必要难度 / 树状图记忆",
            "看着眼熟想不出（提取不出来）→ 提取类：主动回忆练习 / 高频短时提取 / 交错练习",
            "想长期固化（睡一觉就忘）→ 巩固类：睡眠巩固 / 睡前醒后记忆 / 记忆宫殿",
        ],
        "examples": [
            ("核心技术：背了就忘的专业课名词",
             "「考研专业课的名词解释，背了三遍，合上书还是写不出来，下周就考试了。」",
             "诊断=**提取环节**没练（一直重复阅读，没做提取）；推荐主动回忆练习（active-recall，high）打底 + "
             "间隔重复调度（spaced-repetition，high）排期；4 步（列提取清单→闭卷默写→对漏补洞→按 SM-2 排下次）；"
             "验收线=合上书写出的条目数与资料一致，漏的单独进下一轮；自检=「我是不是在重读而不是在提取」。"),
            ("典型行业：医考 / 法考大量事实性材料",
             "「药名和适应症记了忘、忘了记，题一混合就选错。」",
             "诊断=**提取 + 辨别**双重问题（不仅记不住，还分不清该用哪个）；推荐交错练习（interleaving，high）"
             "把同类题混着练 + 组块化（chunking，medium）按药理分类打包；验收线=混合抽测正确率高于分章练习；"
             "自检=「我是不是靠上一题的惯性在选」。"),
            ("边界说明：什么时候不该用本包",
             "「我把整本教材用记忆宫殿背下来了，为什么还是不会做题？」",
             "这是**理解问题不是记忆问题**——记忆宫殿解决的是「记住」，不是「会用」。此时应转理解构建类方法"
             "（费曼学习法 / 自我解释 / 精细追问），本包不适用。另一条边界：经验级方法（如谐音联想）适合"
             "临时应付无意义材料，不要拿它当长期知识体系的主力——它记得快，忘得也快，且不产生理解。"),
        ],
    },
}


# ---------------------------------------------------------------------------
# 渲染
# ---------------------------------------------------------------------------
def load_by_categories(skills_dir, cats):
    out = []
    for f in sorted(glob.glob(os.path.join(skills_dir, "*.json"))):
        if os.path.basename(f).startswith("_"):
            continue
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        if d.get("category") in cats:
            out.append(d)
    out.sort(key=lambda x: x["id"])
    return out


def build_sub_registry(skills):
    """生成该批次的子集 registry（CID 与执行器口径一致）"""
    entries = []
    for d in skills:
        entries.append({
            "id": d["id"],
            "name": d["name"],
            "name_en": d.get("name_en", ""),
            "version": d.get("version", "0.1.0"),
            "license": d.get("license", "CC0-1.0"),
            "category": d.get("category", ""),
            "evidence": d.get("evidence", ""),
            "authors": d.get("authors", ["OpenLMP 公共领域贡献"]),
            "cid": skill_cid(d),
            "file": "skills/" + d["id"] + ".json",
        })
    entries.sort(key=lambda e: e["id"])
    return {
        "registry": "openlmp-skill-index",
        "lmp": "0.1",
        "generated_at": datetime.date.today().isoformat(),
        "note": "本清单不是唯一真理。任何人都可本地维护并提供 diff；我们不设唯一官方 registry。",
        "count": len(entries),
        "skills": entries,
    }


def render_skill_md(cfg, skills, steps, ev_cnt, safe_map):
    n = len(skills)
    hi, md, an = ev_cnt.get("high", 0), ev_cnt.get("medium", 0), ev_cnt.get("anecdotal", 0)
    cat_names = " / ".join(cfg["categories"])
    cats_list = cfg["categories"]

    task_md = "\n".join(f"{i + 1}. {t}" for i, t in enumerate(cfg["task"]))
    constraint_md = "\n".join(f"- {c}" for c in cfg["constraint"])
    antidup_md = "\n".join(f"- {a}" for a in cfg["anti_dup"])
    tags_md = "\n".join(f"  - {t}" for t in cfg["tags"])

    # 资源清单表
    res_rows = [
        ("`references/ALL-SKILLS.md`", f"{n} 个方法总览速查（按 {cat_names} 分组）"),
    ]
    for cat in cats_list:
        safe = safe_map.get(cat)
        sub = [s for s in skills if s.get("category") == cat]
        names = "、".join(s["name"] for s in sub)
        res_rows.append((f"`references/{safe}.md`", f"{cat}（{len(sub)} 个）：{names}"))
    res_rows += [
        ("`assets/skills/*.json`", f"{n} 个方法的结构化定义（可被程序直接读取）"),
        ("`assets/lmp.py`", "零依赖执行器（纯标准库，Python 3.8+），支持 `validate` / `selftest`"),
        ("`assets/registry.json`", f"本批次注册表（{n} 条，含 CID 内容寻址标识）"),
        ("`references/licenses/`", "许可证全文：CC0-1.0 + 木兰宽松许可证 v2"),
    ]
    res_md = "\n".join(f"| {a} | {b} |" for a, b in res_rows)

    ex_md = "\n\n".join(
        f"**{t}**\n\n```\n输入：{i}\n输出：{o}\n```" for t, i, o in cfg["examples"])

    gate_md = "\n".join([
        "- [ ] 是否先**诊断了环节**（编码 / 存储 / 提取），再选方法？",
        "- [ ] 每一步是否都有**可判定**的 checkpoint（无「多复习」「加深印象」等不可判定词）？",
        "- [ ] 是否如实标注循证等级，没把经验级方法说成科学验证？",
        "- [ ] 是否说明了「为什么不是同类备选方法」？",
        "- [ ] 是否越界提供了学科内容本身，或承诺了记忆效果？",
        "- [ ] 用户其实是理解问题时，是否明确告知本包不适用并指向理解构建类方法？",
    ])

    return f"""---
id: {cfg['pkg_id']}
name: AIST2030 {cfg['display_name']}
displayName: {cfg['display_name']}
slug: {cfg['slug']}
module: 知识库(kb)
version: 1.0.0
internal_version: v1.0.0
owner: AIST2030
author: AIST2030
summary: {cfg['summary']}
license: MulanPSL-2.0
capability: {cfg['capability']}
pricing:
  model: free
description: 输入：要记住的材料 + 记忆场景（考前突击 / 长期保持 / 大量事实性材料）+ 当前卡住的环节。输出：环节诊断 + 方法选型 + 逐步执行计划（每步含产出物与可判定验收线）+ 执行后自检。适用边界：只解决「怎么记住」，不提供学科内容、不替代理解、不承诺记忆效果。
tags:
{tags_md}
role: {cfg['role']}
context: |
  输入为用户的记忆材料与场景；目标是先诊断卡在哪个环节（编码 / 存储 / 提取），再选方法并逐步执行、判定通过与否。
  本包构成为 {n} 个方法 / {steps} 个步骤 / {len(cats_list)} 类（{cat_names}）。
  循证等级如实标注：强证据 {hi} 个、中等 {md} 个、经验级 {an} 个——经验级是实践总结，不得说成实验定律。
task: {cfg['task'][0]}；{cfg['task'][1]}；{cfg['task'][2]}；{cfg['task'][3]}；{cfg['task'][4]}。
format: |
  固定四段式：① 环节诊断（编码 / 存储 / 提取，给出判断依据）；② 选型结论（推荐方法 + 为什么是它 + 为什么不是备选）；
  ③ 执行计划（每步含：做什么 / 产出物 / 验收线 / 不通过回到哪步）；④ 执行后自检（3 条自检问题 + 2-3 条带时间维度的达标判据）。
constraint: |
{chr(10).join('  ' + c for c in cfg['constraint'])}
anti_dup: 同一场景反复问时换切入角度（{cfg['anti_dup'][0].split('→')[0].strip()}→编码类；{cfg['anti_dup'][1].split('→')[0].strip()}→存储类；{cfg['anti_dup'][2].split('→')[0].strip()}→提取类），避免模板化结论。
input_schema: 记忆材料（自然语言或要点）+ 记忆场景 + 当前卡住的环节（若用户说不清则由 Agent 诊断）
output_schema: 环节诊断 + 方法选型 + 执行计划（每步含产出物/验收线）+ 执行后自检
example_io: |
  输入：「考研专业课名词解释背了三遍，合上书还是写不出来，下周考试。」
  输出：诊断=提取环节未练（一直在重读）；推荐主动回忆练习（active-recall, high）+ 间隔重复调度（spaced-repetition, high）；
  4 步（列提取清单→闭卷默写→对漏补洞→按 SM-2 排下次）；验收线=合上书写出的条目数与资料一致；自检=「我是在重读还是在提取」。
---

# OpenLMP · {cfg['display_name']}

> **这个库解决什么问题**
>
> {cfg['tagline']}
>
> 本包的做法：每个方法拆成**步骤**，每步配一条**可判定的 checkpoint**（不是「多复习几遍」，而是
> 「合上书写出的条目数与资料一致」），并如实标注循证等级。Agent 可以据此诊断、选型、执行、判定通过与否。
>
> 本包是 OpenLMP 主库（107 个方法）按主题切出的**第一批**专题包，共 {n} 个方法 / {steps} 个步骤。

## Role（角色）

{cfg['role']}

## Context（上下文）

{cfg['context_extra']}
- **库的构成**：{n} 个方法，{steps} 个步骤，{len(cats_list)} 类（{cat_names}）。
- **循证说明**：强证据 {hi} 个（{ev_high_names(skills)}）、中等 {md} 个、经验级 {an} 个。
  强证据方法附真实文献引用（卷期页码已核验）；经验级是实践总结，必须如实告知。

## Task（任务）

{task_md}

## Format（格式）

**环节诊断**

```
诊断结果：<编码 / 存储 / 提取>
判断依据：<用户原话里暴露的线索>
```

**选型结论**

```
推荐方法：<名称>（id: <slug>，循证：<等级>）
适用环节：<编码 / 存储 / 提取>
为什么是它：<针对用户场景的匹配理由>
为什么不是 <备选方法>：<一句话排除理由>
```

**执行计划**

对每一步输出：

```
第N 步：<步骤名>（约 X 分钟）
做什么：<具体动作>
产出物：<可交付的东西>
验收线：<可判定的完成标准>
不通过就回到：<步骤 id>
```

**执行后自检**

- 自检问题：3 条（要能引导用户发现自己没做扎实的环节）
- 达标判据：2-3 条（带时间维度的，如「三天后闭卷复测仍能写出 80%」）

**方法清单速查**：见 `references/ALL-SKILLS.md`（{n} 个方法一句话作用）。
**分类执行手册**：见 `references/{safe_map[cats_list[0]]}.md`，含完整步骤、验收线、Agent 契约。

## 使用案例

{ex_md}

## Constraint（约束）

{constraint_md}

## Anti_Dup（防同质化）

同一场景反复问时，**不要重复同一套说辞**。按记忆环节换个切入角度：

{antidup_md}

## Quality_Gate（发布前自检）

{gate_md}

## Input / Output Schema

**输入**：记忆材料（自然语言或要点）+ 记忆场景 + 当前卡住的环节（说不清则由 Agent 诊断）。
**输出**：环节诊断 + 方法选型 + 执行计划（每步含产出物 / 验收线）+ 执行后自检。

## 附：资源清单

| 路径 | 内容 |
|---|---|
{res_md}

> 学习方法库其余主题（理解构建 / 评测验证 / 计划执行 / 知识管理 / 元认知 / 分析与思维 / 技能习得）
> 以**同系列专题包**分开发布；完整 107 方法见全家桶 skill `aist2030-openlmp`。

## 命令用法

```bash
# 校验 {n} 个方法是否全部符合 schema 与纯度规则
python assets/lmp.py validate assets/skills/

# 列出本包全部方法
python assets/lmp.py list --dir assets/skills

# 按记忆问题本地检索（零网络请求）
python assets/lmp.py recommend "背了就忘" --dir assets/skills

# 端到端自检（含反向测试：拒绝模糊 checkpoint、拒绝虚标循证）
python assets/lmp.py selftest
```

## 数据规范

- **方法内容**：CC0-1.0 公共领域贡献——可自由使用、修改、商用、闭源分发，无署名义务
- **协议规范与执行器**：木兰宽松许可证 v2（MulanPSL-2.0，OSI 批准）——同样可自由使用、修改、商用，唯一义务是分发时随附许可证副本并保留声明
- **证据标注**：`high` / `medium` / `anecdotal` 三级。`high` 必须附真实文献引用，且须通过引用白名单校验（`citation_lint`）
- 许可证全文随包分发：`references/licenses/MulanPSL-2.0.txt`、`references/licenses/CC0-1.0.txt`

## License

分层释出（完整见仓库根目录 `LICENSE`）：

- **{n} 个方法定义与数据**：CC0-1.0 公共领域贡献——可自由使用、修改、商用、闭源分发，无署名义务
- **协议规范与执行器**：木兰宽松许可证 v2（MulanPSL-2.0，OSI 批准）——同样可自由使用、修改、商用，唯一义务是分发时随附许可证副本并保留声明
- **商标**：「OpenLMP」名称与标识不在两层许可证授权范围内
"""


def ev_high_names(skills):
    hs = [s["name"] for s in skills if s.get("evidence") == "high"]
    return "、".join(hs) if hs else "无"


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def build_pack(key, repo=REPO, out_root=SRC):
    cfg = PACKS[key]
    out = os.path.join(out_root, cfg["slug"] + "-v1")
    skills_dir = os.path.join(repo, "skills")

    skills = load_by_categories(skills_dir, cfg["categories"])
    if not skills:
        print(f"[{key}] 没有匹配的方法，跳过")
        return None
    steps = sum(len(s.get("steps", [])) for s in skills)
    ev_cnt = {}
    for s in skills:
        ev_cnt[s.get("evidence", "?")] = ev_cnt.get(s.get("evidence", "?"), 0) + 1
    print(f"[{key}] 载入 {len(skills)} 个方法 / {steps} 步 / 循证 {ev_cnt}")

    refs = os.path.join(out, "references")
    assets = os.path.join(out, "assets")
    os.makedirs(os.path.join(refs, "licenses"), exist_ok=True)
    for sub in ("skills", "schema"):
        os.makedirs(os.path.join(assets, sub), exist_ok=True)

    # 1) references：总览 + 分类手册（复用 build_dist 渲染，格式与全家桶一致）
    orig_order, orig_safe = build_dist.CATEGORY_ORDER, build_dist.SAFE_NAME
    build_dist.CATEGORY_ORDER = cfg["categories"]
    build_dist.SAFE_NAME = {**orig_safe, **cfg["safe_names"]}
    try:
        title = f"OpenLMP {cfg['display_name'].replace('OpenLMP ', '')} {len(skills)} 个方法 · 总览速查"
        overview, by_cat = build_dist.render_overview(
            skills, title,
            "按用途分组。左列循证等级是重要信息：**high 有较强实验证据支持，"
            "anecdotal 主要是实践经验**，选型时优先挑 high。\n")
        with open(os.path.join(refs, "ALL-SKILLS.md"), "w", encoding="utf-8") as f:
            f.write(overview)
        for cat in cfg["categories"]:
            items = by_cat.get(cat)
            if not items:
                continue
            safe, body = build_dist.render_manual(cat, items)
            with open(os.path.join(refs, f"{safe}.md"), "w", encoding="utf-8") as f:
                f.write(body)
            print(f"  写出 references/{safe}.md（{len(items)} 个方法）")
    finally:
        build_dist.CATEGORY_ORDER, build_dist.SAFE_NAME = orig_order, orig_safe

    # 2) assets：本批 JSON + 执行器 + schema + 子集 registry
    n = 0
    for s in skills:
        src = os.path.join(skills_dir, s["id"] + ".json")
        shutil.copy2(src, os.path.join(assets, "skills", s["id"] + ".json"))
        n += 1
    for f in glob.glob(os.path.join(repo, "schema", "*.json")):
        shutil.copy2(f, os.path.join(assets, "schema", os.path.basename(f)))
    shutil.copy2(os.path.join(repo, "runtime", "lmp.py"), os.path.join(assets, "lmp.py"))
    reg = build_sub_registry(skills)
    with open(os.path.join(assets, "registry.json"), "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"  复制 {n} 个方法 JSON + 执行器 + schema + 子集 registry（count={reg['count']}）")

    # 3) 许可证全文
    for lic in ("MulanPSL-2.0.txt", "CC0-1.0.txt"):
        src = os.path.join(repo, "licenses", lic)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(refs, "licenses", lic))

    # 4) SKILL.md
    skill_md = render_skill_md(cfg, skills, steps, ev_cnt, cfg["safe_names"])
    with open(os.path.join(out, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(skill_md)
    print(f"  写出 SKILL.md（{len(skill_md)} 字节）")
    print(f"[{key}] 完成 → {out}")
    return out


def main():
    args = sys.argv[1:]
    if not args or args[0] == "--list":
        print("已配置批次：")
        for k, v in PACKS.items():
            print(f"  {k:12s} -> {v['slug']}  「{v['display_name']}」  分类={v['categories']}")
        return
    keys = list(PACKS.keys()) if args[0] == "all" else args
    for k in keys:
        if k not in PACKS:
            print(f"未知批次：{k}")
            continue
        build_pack(k)


if __name__ == "__main__":
    main()
