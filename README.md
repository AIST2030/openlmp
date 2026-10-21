# OpenLMP

**让学习方法成为全人类共有的公共资产。**

这不是一个平台。这是一份协议 + 一个方法库。

零注册 · 零 API Key · 零安装 · 数据不出本地 · 永不作恶

---

## 30 秒上手

```bash
# 看有哪些方法（当前 107 个）
python runtime/lmp.py list

# 遇到问题，本地检索推荐（零网络请求）
python runtime/lmp.py recommend "我记住了但过两天就忘"

# 打印某个方法的完整执行剧本
python runtime/lmp.py run feynman --topic "间隔重复的原理"

# 端到端自检（含 3 类反向测试）
python runtime/lmp.py selftest
```

零第三方依赖，Python 3.8+。**不需要注册、不需要 API Key、不需要下载任何模型。**

---

## 这不是 AI 教育产品

这是本项目最重要的一个决定，理由很硬：

> 任何 AI 教育产品都必须回答三个问题：谁在提供算力、谁在保存数据、谁对结果负责。
> 三个答案都指向「中心」，而中心就是可以被关停、可以被私有化的东西。

所以 OpenLMP **不做**：账号系统 · 在线服务 · 数据采集 · 收益分成 · K12 学科培训

我们**只做**：一套任何人都能自由复制、修改、分发的学习方法规范。

---

## 已收录的 107 个方法

**记忆巩固（15）** · `active-recall` 主动回忆练习（强） · `spaced-repetition` 间隔重复调度（强） · `retrieval-spread` 高频短时提取（中） · `dual-coding` 双重编码（中） · `interleaving` 交错练习（强） · `method-of-loci` 记忆宫殿（中） · `sleep-wake-memory` 睡前醒后记忆（经验） · `mnemonic-association` 谐音联想（经验） · `tree-memory` 树状图记忆（经验） · `emotion-anchoring` 情绪联动（经验） · `backstitch-review` 回针缝复习（经验）

**理解构建（15）** · `feynman` 费曼学习法（中） · `elaborative-interrogation` 精细追问法（强） · `sq3r` SQ3R 教材精读（中） · `socratic` 苏格拉底式追问（中） · `first-principles` 第一性原理（经验） · `inquiry-learning` 探究式学习（中） · `case-study` 案例研习（中） · `blooms-taxonomy` 布鲁姆分层（中） · `constructivist-learning` 建构主义（中） · `thick-thin` 薄厚互返（经验） · `spiral-learning` 螺旋学习（经验）

**技能习得（8）** · `deliberate-practice` 刻意练习（强） · `project-based-learning` 721 行动学习（经验） · `simon-learning` 西蒙学习法（经验） · `shadowing` 影子跟读（中） 等 8 个

**知识管理（11）** · `concept-map` 概念图构建（中） · `zettelkasten` 卡片盒笔记（经验） · `progressive-summarization` 渐进式总结（经验） · `mind-map` 思维导图（中） · `three-color-notes` 三色笔记（经验） · `sq4r` SQ4R 阅读（中） · `two-column-notes` 二等分笔记（经验） · `qa-notes` 一问一答笔记（经验）

**评测验证（12）** · `error-notebook` 错题本溯源（强） · `critical-thinking` 批判性思维核查（强） · `closed-book-writing` 合书写作（强） · `time-capsule-quiz` 时间胶囊出题（经验） · `tally-forgetting` 正字统计（经验） · `thirty-second-recall` 30 秒速览（经验） · `blank-sheet-daily` 白纸默写（经验） · `pen-not-erasable` 圆珠笔法（经验） · `write-to-recall` 书写记忆检查（经验）

**计划执行（15）** · `goal-decomposition` 目标四级拆解（中） · `pomodoro-diagnose` 专注节奏诊断（经验） · `pomodoro` 番茄工作法（经验） · `smart-goals` SMART 目标（经验） · `dual-goal` 双重目标（经验） · `reverse-learning` 逆向学习（经验） · `zeigarnik-pause` 留一点学习（经验） · `micro-habits` 微习惯（经验） · `energy-management` 精力管理（经验） · `gantt-progress` 甘特进度（经验） · `habit-consistency` 习惯性学习（经验） · `goal-backward` 目标逆向（经验）

**元认知（11）** · `learning-journal` 学习日志与错因归因（中） · `diary-question` 今天学到了什么（中） · `transfer-question` 迁移提问训练（强） · `familiarity-count` 回看计数（中） · `morning-evening-review` 晨间晚间复盘（经验） · `life-wheel` 生命之花（经验） · `four-step-review` 四步复盘（经验） · `effort-outcome-matrix` 努力分解矩阵（经验）

**协作学习（4）** · `pair-learning` 结对学习（中） · `peer-instruction` 同伴教学（中） 等 4 个

**思维方法（7）** · `five-whys` 5Why 追因（经验） · `five-w1h` 5W1H 拆解（经验） · `mece` MECE 分解（经验） · `logic-tree` 逻辑树（经验） · `six-hats` 六顶思考帽（经验） · `scamper` SCAMPER 创意（经验） · `lateral-listing` 横向列方案（经验）

**分析方法（9）** · `pareto` 帕累托分析（经验） · `fishbone` 鱼骨图（经验） · `decision-matrix` 决策矩阵（经验） · `pdca` PDCA 循环（经验） · `ooda` OODA 循环（经验） · `gap-analysis` 差距分析（经验） · `hypothesis-method` 假设法（经验） · `elimination` 排除法（经验） · `reductio` 反证法（经验）

「强/中/经验」= 循证等级（high / medium / anecdotal），标注在每个 Skill 的 `evidence` 字段。
标 `high` 的必须给文献引用，CI 会拦截虚标。
完整可检索清单见 `registry/registry.json`（含每个方法的 CID 内容寻址标识）。

> 商业与管理框架（SWOT、波特五力、商业模式画布、OKR……）另入 **[商业子库 `business/`](business/README.md)**，与主库同协议、独立成库。

全部以 **CC0-1.0** 释出到公共领域（见 `LICENSE`）。

---

## 三条不可协商的规则

**1. Skill 是纯 JSON，不含任何可执行代码。**
不需要实现任何东西就能读懂它。这是防垄断的关键。

**2. 每个 step 必须有客观可判定的 checkpoint。**
禁止「理解」「掌握」「熟悉」这类不可判定词。CI 会直接拒绝。
绝大多数学习方法失败在「执行者假装做完了」。

**3. 协议里不存在「上传用户数据」的接口。**
这是设计意图，不是待办事项。`learner-state.json` 永远只在用户自己的机器上。

---

## 质量保证是可执行的代码，不是口号

```bash
python runtime/lmp.py selftest
```

7 类测试，其中 3 类是**反向测试**（故意注入违规，必须被拒绝）：

| 测试 | 注入的违规 | 期望 |
|---|---|---|
| 纯度 | 「请先注册账号并输入 API Key」 | 拦截 ✓ |
| checkpoint | 「深刻理解这个概念」 | 判为不可判定 ✓ |
| 循证 | `evidence: high` 但无引用 | 拒绝（防虚标）✓ |

外加 SM-2 四项边界 + ease 下界锁定 + CID 稳定性。

CI 在 Python 3.8 / 3.11 / 3.12 三个版本上自动跑同一套检查，
并验证**无任何第三方依赖**。

---

## 为什么值得信：一个方法不会自己说好话

每个 Skill 都有 **`when_not_to_use`**（什么时候别用我）字段，
检索命中时会明确告诉你「这情况请改用 X」。

这不是免责声明，是功能 —— 一个只会说自己好的方法库，是营销话术，不是方法库。

```bash
$ python runtime/lmp.py recommend "想学会写代码"
spaced-repetition  间隔重复调度
  若你的情况是「只考一次的短期突击」→ 改用：active-recall
```

---

## 如何贡献

```bash
cp skills/_template.json skills/my-method.json
python runtime/lmp.py validate skills/my-method.json
```

评审只看三件事（见 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)）：

1. checkpoint 是否客观可判定
2. 是否违反纯度规则（无注册 / 无 Key / 无云端同步）
3. evidence 标注是否诚实

你的贡献不会给你钱，也不会给你流量。
它会给你一个永远跟着你的名字。

---

## 目录结构

```
SPEC.md                          协议规范 v0.1（含「不做什么」）
CODE_OF_CONDUCT.md               贡献者准则
LICENSE                         CC0-1.0 官方全文
schema/skill-0.1.json            Skill JSON Schema
schema/learner-state-0.1.json    本地状态 Schema
skills/*.json                    方法库（107 个 + 样板）
runtime/lmp.py                   参考执行器（零依赖）
registry/registry.json           内容寻址清单（CID）
docs/                            目标对齐、发布策略、路线图
```

---

## 更多

- [目标对齐书](docs/00-目标对齐书.md) — 为什么砍掉链上治理 / 收益分成 / K12
- [发布策略与执行清单](docs/发布策略与执行清单.md) — 发布到哪里、为什么不发布到应用商店
- [路线图](docs/ROADMAP.md) — 分期与每期唯一的成功标准
- [方法宇宙索引](docs/METHOD-UNIVERSE.md) — 约 300 种方法按九域对照，标注已收录 / 候选 / 仅参考

---

**下一步不是加功能，是继续加好方法——每一条都要过验收线。**