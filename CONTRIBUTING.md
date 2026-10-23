# 参与 OpenLMP

先读 [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)。这里只讲怎么把贡献送进仓库。

## 我们只收三类贡献

1. **新方法**：`skills/*.json`（商业框架走 `business/skills/`，先读 `business/README.md`）
2. **修正**：引用错误、checkpoint 不可判定、`when_not_to_use` 缺失、纯度违规
3. **协议与工具**：`SPEC.md`、`runtime/`、`tools/` 的改进

不收：AI 教育产品功能、账号系统、数据上传接口、收益分成、K12 学科培训内容（见 `docs/00-目标对齐书.md`）。

## 三步流程

```bash
# 1. 拷贝样板，改内容（id 用 kebab-case）
cp skills/_template.json skills/your-method.json

# 2. 本地过三关，全过再提 PR
python runtime/lmp.py validate skills/your-method.json
python tools/citation_lint.py
python runtime/lmp.py selftest

# 3. 提 PR，把模板里的贡献者声明逐项勾选
```

## 贡献者声明（提交 PR 即视为确认以下全部条款）

**一、权利保证**
我确认对本次提交的内容拥有合法权益，有权以本仓库的分层许可（内容 CC0-1.0 / 协议与代码木兰宽松许可证 v2）向公众释出；内容不侵犯任何第三方的专利权、商标权、著作权、商业秘密、肖像权或其他合法权益，不含任何第三方保密信息。

**二、人身权维度的不可撤销授权**
我知晓并同意：依中国《著作权法》第二十条，署名权、修改权、保护作品完整权等人身权利依法不可放弃。我保留上述人身权利；同时，我授予 OpenLMP 项目及其后续维护者一项**永久的、不可撤销的、全球范围内的、免费的非独占许可**，以实施、复制、修改、分发、再许可本次提交的内容。此项授权用于在 CC0 无法覆盖人身权的法域内，为项目提供合同层面的兜底——它不剥夺你的署名权，只是让项目在任何法域都能合法运转。

**三、许可落层**
本次提交的内容按本仓库 [`LICENSE`](LICENSE) 的分层规则释出：方法定义与数据入 CC0-1.0，协议规范与代码入木兰宽松许可证 v2（MulanPSL-2.0）。

**四、可追溯**
我承诺：如本次提交的权利状态发生变化（权利被转让、出现第三方权利主张等），将主动告知项目维护者。

## 评审只看四件事

1. **checkpoint 是否客观可判定**——禁「理解」「掌握」「熟悉」，每条 step 必须能判过/判废
2. **纯度**——无注册、无 API Key、无云端同步、无数据上传接口
3. **evidence 是否诚实**——标 `high` 必须有引用，且引用须命中 [`docs/evidence-audit/verified_refs.json`](docs/evidence-audit/verified_refs.json) 白名单（CI 用 `tools/citation_lint.py` 拦截虚标）
4. **不重复**——先查 [`docs/METHOD-UNIVERSE.md`](docs/METHOD-UNIVERSE.md) 与 `registry/registry.json`

## 提交信息惯例

建议 DCO 式署名（不强制，但便于追溯）：

```bash
git commit -s
# 提交信息末尾自动带 Signed-off-by: Your Name <you@example.com>
```

## 你的贡献不会给你钱，也不会给你流量

CC0 与木兰 v2 都不要求署名，但 `registry/registry.json` 的 CID 内容寻址会永久记录你提交过什么。你的名字，会一直在数据里。
