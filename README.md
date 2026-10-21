# OpenLMP

**让学习方法成为全人类共有的公共资产。**

这不是一个平台。这是一份协议 + 一个方法库。

零注册 · 零 API Key · 零安装 · 数据不出本地 · 永不作恶

---

## 30 秒上手

```bash
# 看有哪些方法（当前 10 个）
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

## 已收录的 22 个方法

**记忆巩固** · `active-recall` 主动回忆练习（强） · `spaced-repetition` 间隔重复调度（强） · `retrieval-spread` 高频短时提取（中） · `dual-coding` 双重编码（中）

**理解构建** · `feynman` 费曼学习法（中） · `elaborative-interrogation` 精细追问法（强） · `sq3r` SQ3R 教材精读（中） · `socratic` 苏格拉底式追问（中）

**技能习得** · `deliberate-practice` 刻意练习（强） · `project-based-learning` 721 行动学习（经验）

**知识管理** · `concept-map` 概念图构建（中） · `zettelkasten` 卡片盒笔记（经验） · `progressive-summarization` 渐进式总结（经验）

**评测验证** · `error-notebook` 错题本溯源（强） · `critical-thinking` 批判性思维核查（强） · `closed-book-writing` 合书写作（强）

**计划执行** · `goal-decomposition` 目标四级拆解（中） · `pomodoro-diagnose` 专注节奏诊断（经验）

**元认知** · `learning-journal` 学习日志与错因归因（中） · `diary-question` 今天学到了什么（中） · `transfer-question` 迁移提问训练（强）

**协作学习** · `pair-learning` 结对学习（中）

「强/中/经验」= 循证等级（high / medium / anecdotal），标注在每个 Skill 的 `evidence` 字段。
标 `high` 的必须给文献引用，CI 会拦截虚标。

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
skills/*.json                    方法库（10 个 + 样板）
runtime/lmp.py                   参考执行器（零依赖）
registry/registry.json           内容寻址清单（CID）
docs/                            目标对齐、发布策略、路线图
```

---

## 更多

- [目标对齐书](docs/00-目标对齐书.md) — 为什么砍掉链上治理 / 收益分成 / K12
- [发布策略与执行清单](docs/发布策略与执行清单.md) — 发布到哪里、为什么不发布到应用商店
- [路线图](docs/ROADMAP.md) — 分期与每期唯一的成功标准

---

**下一步不是加功能，是加第 11 个好方法。**