# OpenLMP 引用真实性核查报告（Evidence Citation Audit）

- **日期**：2026-10-22
- **范围**：主库 `skills/` 中所有 `evidence: high` 的方法（共 15 条 / 17 篇独立文献）
- **触发**：评估报告提出核心隐患——「CI 无法验证引用是否真实存在」。本核查即按该建议执行，验证隐患是否属实、严重程度如何。
- **方法**：`tools/evidence_scan.py` 扫描 → 导出 `high_refs.json` → 逐篇 WebSearch 核对期刊/卷期/页码/标题/DOI → 存疑项二次核验。

---

## 一、整体结论（一句话）

**15 条 `evidence:high` 方法引用的 17 篇文献中，11 篇精确正确（约 65%），但存在 2 处硬伤（张冠李戴）、1 处虚标嫌疑、1 处卷期小错、1 处极不严谨——评估报告的担忧被部分证实：`evidence:high` 并非全部经得起核验，且现有 CI 完全无法捕捉这类错误。**

---

## 二、证据分布（全库）

| evidence 等级 | 方法数 |
|---|---|
| anecdotal | 55 |
| medium | 38 |
| high | 15 |
| **合计** | **108**（含 1 个模板文件） |

---

## 三、核查明细表（17 篇独立文献）

| # | 文献（OpenLMP 所写） | 核验结果 | 修正后正确引用 |
|---|---|---|---|
| 1 | Dunlosky et al. 2013, PSPI 14(1) 4–58 | ✅ 精确正确 | — |
| 2 | Kang, McDermott & Roediger 2007, PS 18(6) 409–414 | ✅ 精确正确 | — |
| 3 | Murphy et al. 2009, JEP 101(3) 740–764 | ✅ 精确正确 | — |
| 4 | Paul & Elder 2007（书）| ❓ 合理未深核 | Critical Thinking: The Art of Socratic Questioning（书名合理，低风险）|
| 5 | Ericsson et al. 1993, PR 100(3) 363–406 | ✅ 精确正确 | — |
| 6 | Cepeda et al. 2006, PB 132(3) 354–380 | ✅ 精确正确 | — |
| 7 | Pressley 1987/1989, JEP（无卷期页）| ⚠️ 极不严谨 | 须补全卷期页码（应用前核验）|
| 8 | Bahrick et al. 1993, PS 4(3) 316–321 | ⚠️ 卷期错 | PS **4(5)** 316–321（DOI 10.1111/j.1467-9280.1993.tb00571.x）|
| 9 | Taylor & Rohrer 2010, JEP 102(3) 837–844 | ✅ 精确正确 | — |
| 10 | Roediger & Karpicke 2006, PS 17(3) 249–255 | ✅ 精确正确 | — |
| 11 | Pan 2015, PB 141(4) 785–806 | ❌ 硬伤 | PB 141(4) 实为 *Sleep and Motor Learning* pp 812–834（睡眠主题）；正确预测试文献待替换（见 F1）|
| 12 | Chi et al. 1994, CS 18(3) 439–477 | ✅ 精确正确 | — |
| 13 | Atkinson et al. 2000, JEP 92(1) 43–53 | ❌ 硬伤（期刊错）| **Review of Educational Research 70(2) 181–214**（DOI 10.3102/00346543070002181）|
| 14 | Walker & Stickgold 2004, Neuron 44(1) 121–133 | ✅ 精确正确 | — |
| 15 | McClelland et al. 1995, PR 102(3) 419–457 | ✅ 精确正确 | — |
| 16 | Bromley 1990, ER 19(4) 102–111 | ❌ 未找到/虚标嫌疑 | ER 19(4) 1990 实为 Connelly & Clandinin 叙事探究文；无此 Bromley 迁移文献 |
| 17 | Sweller 1988, CS 12(2) 257–285 | ✅ 精确正确 | — |

---

## 四、问题分级与对 `evidence:high` 信度的影响

### ❌ 硬伤（张冠李戴，不可接受）
- **Pan 2015（pretesting 方法）**：页码错 + 主题错。影响方法仍保有 Roediger & Karpicke 2006 这一有效 high 引用，故该方法 high 等级可保，但 Pan 这条必须删除/替换。
- **Atkinson 2000（self-explanation + worked-examples 两方法共用）**：期刊完全写错。两方法均另有有效 high 引用（Chi 1994 / Sweller 1988），故 high 等级可保，但 Atkinson 这条必须改正。

### ❌ 虚标嫌疑（找不到来源）
- **Bromley 1990（transfer-question 方法）**：该方法是**唯一** high 引用。来源查无，等于该方法 `evidence:high` 没有任何支撑。最严重——建议降级为 `medium` 或补真实来源。

### ⚠️ 小错（卷期）
- **Bahrick 1993（error-notebook 方法）**：4(3)→4(5)。方法另有 Dunlosky 2013 有效 high 引用，high 等级可保，改卷期即可。

### ⚠️ 不严谨（缺卷期页码）
- **Pressley 1987/1989（elaborative-interrogation 方法）**：该方法是**唯一** high 引用，且只写年份无卷期页。等于 high 等级薄弱。建议补全或降级。

### 影响汇总
- 15 条 high 方法中，**13 条仍至少保有 1 条有效 high 引用**（high 等级站得住，但其中 4 条含须修正的坏引用）。
- **2 条方法（transfer-question、elaborative-interrogation）的 high 等级实质无支撑**，是优先处置项。

---

## 五、建议修复清单（待决策是否执行）

| 编号 | 方法 | 动作 | 修正后引用 |
|---|---|---|---|
| F1 | pretesting | 删除/替换 Pan 2015 | 建议 Kornell, Hays & Bjork (2009) *JEP:LMC* 35(4) 989–998（预测试/尝试提取经典；应用前核验 DOI）|
| F2 | self-explanation | 改 Atkinson 2000 期刊 | Atkinson, Derry, Renkl & Wortham (2000) *Review of Educational Research* 70(2) 181–214（DOI 10.3102/00346543070002181）|
| F3 | worked-examples | 同 F2 | 同 F2 |
| F4 | error-notebook | 改 Bahrick 卷期 | Bahrick et al. (1993) *Psychological Science* 4(5) 316–321（DOI 10.1111/j.1467-9280.1993.tb00571.x）|
| F5 | transfer-question | 降级 `medium` 或补真实来源 | 待定（Bromley 1990 查无）|
| F6 | elaborative-interrogation | 补全 Pressley 卷期页码 | 待定（应用前核验具体年期页）|

> **状态（2026-10-22 更新）：F1–F6 已全部执行落库。** F1/F5/F6 的替换文献均在应用前逐条核验了卷期页码与 DOI。详见第六节。

---

## 六、修复执行记录（2026-10-22 已全部落库）

| 编号 | 方法 | 已执行动作 | 核验依据 |
|---|---|---|---|
| F1 | pretesting | Pan 2015 → Kornell, Hays & Bjork 2009, *JEP: LMC* 35(4) 989–998 | ERIC v35 n4 p989-998；PubMed PMID 19586265，DOI 10.1037/a0015729 |
| F2 | self-explanation | Atkinson 2000 期刊改正 → *Review of Educational Research* 70(2) 181–214 | ERIC EJ627412；DOI 10.3102/00346543070002181 |
| F3 | worked-examples | 同 F2 | 同 F2 |
| F4 | error-notebook | Bahrick 1993 卷期 4(3) → 4(5) | DOI 10.1111/j.1467-9280.1993.tb00571.x（ScienceGate / Google Scholar 均记 4(5)）|
| F5 | transfer-question | 查无的 Bromley 1990 → Gick & Holyoak 1983, *Cognitive Psychology* 15(1) 1–38（保留 high） | DOI 10.1016/0010-0285(83)90002-6；Semantic Scholar / Google Scholar 卷期页一致 |
| F6 | elaborative-interrogation | Pressley 补全 → *JEP: LMC* 13(2) 291–300，并补 Dunlosky 2013 佐证 | Ovid 原题「Generation and precision of elaboration」；Dunlosky 2013 将该法评为中等效用 |

连带处理：
- **历史生成脚本 `expand_to_50.py`** 中 `REF_ATKINSON` / `REF_PAN` 两个常量同样写错，已一并改正，避免日后重跑脚本再次播种错误引用。
- 改动使 6 个方法的 CID 变化，`tools/build_registry.py` 已重建注册表（count=107）。
- 发布快照（`openlmp-dist/` 两个包 + 仓库内 `workbuddy-skill/`）已同步重建，避免再现「仓库内快照停在旧版本」的问题。

复核结果：`validate skills/` 107 个文件 0 错误；`selftest` 11 项全部通过（107 方法 / 445 步 / 循证 high 15）。

---

## 七、工程化改进已落地

1. ✅ **新增 `tools/citation_lint.py`**（零第三方依赖，Python 3.8+）：校验 `evidence:high` 的每条引用是否命中白名单，未命中即报错、退出码 1。匹配取「年份 + 作者姓 + 期刊名 + 卷期 + 页码」五项子串全命中，可精确抓住本次审计发现的三类错误。
2. ✅ **建立「已核验引用白名单」** `docs/evidence-audit/verified_refs.json`（17 条，6 条带 DOI），含本次核查结论与 `verified_on` 日期。**新增 high 引用须先入表**。
3. ✅ **接进 CI**：`.github/workflows/selftest.yml` 新增 `Citation lint (evidence:high refs)` 步骤，位于 validate 之后、selftest 之前。
4. ✅ **反向测试通过**：用审计出的 5 条坏引用（Pan 2015 / Atkinson 旧写法 / Bahrick 4(3) / Bromley 1990 / Pressley 旧写法）喂给 lint，全部返回未命中被拦住；4 条正确引用全部命中。**闸门确实有牙**。
5. ⏳ **暂未做**：`evidence:high` 强制要求可解析 DOI、否则自动降级 `medium`——部分经典文献（Pressley 1987、Sweller 1988 等）无 DOI 或未核验，强制降级会误伤，建议待白名单 DOI 补齐后再上。

---

## 八、下一步

- 本次改动已落库并通过全部自检，但**尚未提交/推送**，也**尚未重新发布 SkillHub**（线上仍是 v2.0.0、含旧的错误引用）。
- 建议：提交并推送到 GitHub + AtomGit；如需同步线上，把包升到 **v2.0.1** 后重新发布（SkillHub 不接受同版本号重复提交）。
