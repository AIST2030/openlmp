# OpenLMP 商业方法子库（openlmp-business）

商业与管理框架的独立子库。与 [OpenLMP 主库](../README.md) **同 schema、同执行器、同验收线**，
只是聚焦"商业/管理/营销/战略/表达"这一域，category 用商业四类：**商业分析 / 商业战略 / 商业管理 / 商业表达**。

## 为什么单独拆出来

主库 OpenLMP 的定位是**学习方法协议**——帮你"学得会、想得清、做得对"。
商业框架（SWOT、波特五力、商业模式画布、OKR……）是**组织经营工具**，与个人学习是两件事。
混在一个库会稀释两边定位；拆成子库则：
- 主库保持"学习方法"的纯粹，循证等级清晰；
- 商业库可自由扩展管理/营销/战略框架，不受"学习方法"定位束缚；
- 两者仍是同一协议家族：JSON 结构、`runtime/lmp.py`、CID、验收线全部通用，Skill 可跨库引用。

## 收录标准（与主库一致）

每个框架都做成**可执行 Skill**：能拆步、每步有可判定 checkpoint、不含注册登录/密钥/上传云端/订阅付费/引流。
做不成可判定验收的，不进库。

## 第一批已收录（15 个）

**商业分析（7）** · `swot` SWOT 分析 · `pestel` PESTEL 宏观扫描 · `porter-five-forces` 波特五力 · `bcg-matrix` BCG 矩阵 · `ansoff` 安索夫矩阵 · `value-chain` 价值链分析 · `business-model-canvas` 商业模式画布

**商业战略（3）** · `positioning` 定位理论 · `second-curve` 第二曲线 · `flywheel` 飞轮效应

**商业管理（3）** · `okr` OKR 目标管理 · `kpi` KPI 绩效指标 · `balanced-scorecard` 平衡计分卡

**商业表达（2）** · `pyramid-principle` 金字塔原理 · `prep` PREP 表达

## 候选队列（后续批次）

| 类别 | 候选框架 |
|---|---|
| 商业分析 | 3C、GE–麦肯锡九格、蓝海战略 ERRC、VRIO、精益画布、STP、RFM、漏斗分析、A/B 测试 |
| 商业战略 | 波特三大通用战略、核心能力理论、4P/4C/4R/7P、产品生命周期、品牌资产、颠覆性创新、长尾理论、三层面增长、经验曲线 |
| 商业管理 | MBO 目标管理、EVA 经济增加值、GTD、艾森豪威尔矩阵、议题树、假设驱动法 |
| 商业表达 | SCQA 故事框架、二八法则（资源分配版） |

## 使用

```bash
# 校验本子库全部 Skill
python runtime/lmp.py validate business/skills

# 列出本子库全部框架
python runtime/lmp.py list --dir business/skills

# 按业务问题本地检索（零网络请求）
python runtime/lmp.py recommend "要不要进新市场" --dir business/skills

# 打印某个框架的执行剧本
python runtime/lmp.py run swot --dir business/skills

# 装进你的 AI（SkillHub，腾讯出品）
skillhub install aist2030-openlmp-business

# 学习方法库（主库 107 个方法）
skillhub install aist2030-openlmp
```

> `--dir` 让同一个执行器既能服务主库也能服务子库：主库命令省略该参数即用 `skills/`。

索引见 [`registry/registry.json`](registry/registry.json)（含每个框架的 CID）。
15 个框架定义全部以 **CC0-1.0** 释出，可自由商用；执行器等代码随主库为木兰宽松许可证 v2（见根目录 `LICENSE` 分层说明）。
