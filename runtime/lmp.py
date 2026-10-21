#!/usr/bin/env python3
"""
OpenLMP 参考执行器 v0.1
======================
零第三方依赖。Python 3.8+。

设计原则（与 SPEC.md 一致）：
  1. Skill 是纯 JSON 声明，本文件只做「调度」，不做「内容生成」。
  2. 所有状态写在用户本地的 learner-state.json，协议不定义任何上传路径。
  3. 校验器严格执行纯度规则：Skill 里不得出现注册/登录/API Key/云端同步。

命令：
  list                      列出全部 Skill
  show <id>                 查看单个 Skill
  validate <path...>        按 schema + 纯度规则校验
  recommend "<描述>"        本地检索推荐方法（不联网）
  run <id> --topic X        打印该 Skill 的执行剧本（给人或给 Agent 照做）
  review                    今日到期复习队列 + SM-2 重算
  selftest                  端到端自检
"""

import json
import os
import sys
import glob
import hashlib
import re
import datetime
import argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIR = os.path.join(ROOT, "skills")
SCHEMA_PATH = os.path.join(ROOT, "schema", "skill-0.1.json")
STATE_PATH = os.path.join(ROOT, "learner-state.json")

# ---------------------------------------------------------------- 纯度规则
# 这些不是建议，是协议级硬约束。违反者不收录。
FORBIDDEN_PATTERNS = [
    (r"\b(注册|登录|sign\s*up|log\s*in|login)\b", "不得要求用户注册/登录"),
    (r"\b(api[\s_-]?key|access[\s_-]?token|secret)\b", "不得要求 API Key/密钥"),
    (r"(上传|同步|存储)[^。]{0,6}(云端|服务器|我们的|平台)", "不得把用户数据引到中心服务"),
    (r"(订阅|付费后解锁|购买会员)", "方法本体不得设付费墙"),
    (r"(微信|支付宝|微信号|公众号).{0,8}(加|联系|扫码)", "不得在协议内夹带引流"),
]
VAGUE_CHECKPOINT = ["理解", "掌握", "熟悉", "深入", "领会", "吃透"]
REQUIRED_FIELDS = ["lmp", "id", "name", "version", "license", "description", "steps"]
VALID_CATEGORIES = [
    "理解构建", "记忆巩固", "技能习得", "知识管理",
    "计划执行", "元认知", "协作学习", "评测验证",
]

# 违规严重度：error 阻止收录，warn 提示人工复核
VAGUE = "error"
FORBIDDEN = "error"


# ---------------------------------------------------------------- 工具函数
def load_skills():
    out = []
    for p in sorted(glob.glob(os.path.join(SKILL_DIR, "*.json"))):
        base = os.path.basename(p)
        if base.startswith("_"):
            continue  # _template 不是 Skill
        try:
            with open(p, "r", encoding="utf-8") as f:
                obj = json.load(f)
            obj["__path"] = p
            out.append(obj)
        except Exception as e:
            print("[WARN] 跳过无法解析的文件 %s: %s" % (base, e), file=sys.stderr)
    return out


def skill_cid(skill):
    """内容寻址标识。去掉内部字段后 canonical JSON + blake2b。"""
    d = {k: v for k, v in skill.items() if not k.startswith("__")}
    raw = json.dumps(d, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    h = hashlib.blake2b(raw.encode("utf-8"), digest_size=20).digest()
    b32 = "0123456789abcdefghijklmnopqrstuv"
    bits = "".join(format(b, "08b") for b in h)
    enc = "".join(b32[int(bits[i:i + 5], 2)] for i in range(0, len(bits), 5))
    return "lmp:" + enc[:39]


def today_str():
    return datetime.date.today().isoformat()


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "lmp": "0.1",
        "learner_id": "local-" + hashlib.blake2b(
            str(datetime.datetime.now()).encode(), digest_size=6
        ).hexdigest(),
        "created_at": today_str(),
        "skills": {},
        "privacy": {"telemetry": "off", "sync": "none"},
    }


def save_state(st):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, indent=2)
    print("[state] 已写入 %s" % STATE_PATH)


# ---------------------------------------------------------------- SM-2
def sm2(reps, ease, interval, q):
    """SPEC §5。q ∈ [0,5]。返回 (ease, interval, reps)。"""
    q = max(0.0, min(5.0, float(q)))
    ease = ease + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    ease = max(1.3, min(3.0, ease))       # 协议硬边界
    if q < 3:
        return ease, 1.0, 0
    reps += 1
    if reps == 1:
        interval = 1.0
    elif reps == 2:
        interval = 6.0
    else:
        interval = interval * ease
    return ease, interval, reps


# ---------------------------------------------------------------- 校验
def validate_one(obj, path="<memory>"):
    errs, warns = [], []

    for f in REQUIRED_FIELDS:
        if f not in obj:
            errs.append("缺少必填字段 `%s`" % f)

    if obj.get("lmp") != "0.1":
        errs.append("lmp 字段必须为 \"0.1\"，当前 %r" % obj.get("lmp"))

    if "id" in obj and not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", str(obj.get("id", ""))):
        errs.append("id 必须是 kebab-case，当前 %r" % obj.get("id"))

    if "version" in obj and not re.match(r"^\d+\.\d+\.\d+$", str(obj.get("version"))):
        errs.append("version 必须是 semver，当前 %r" % obj.get("version"))

    if obj.get("license") not in ("CC0-1.0", "CC-BY-4.0"):
        errs.append("license 必须是 CC0-1.0 或 CC-BY-4.0（方法属公共领域）")

    if obj.get("category") not in VALID_CATEGORIES:
        errs.append("category 非法：%r（合法值见 schema）" % obj.get("category"))

    if obj.get("evidence") not in ("high", "medium", "anecdotal"):
        errs.append("evidence 必须是 high/medium/anecdotal")

    # evidence=high 必须给引用，否则是虚标
    if obj.get("evidence") == "high" and not obj.get("evidence_refs"):
        errs.append("evidence=high 但 evidence_refs 为空 —— 禁止虚标循证等级")

    steps = obj.get("steps") or []
    if not isinstance(steps, list) or len(steps) < 2:
        errs.append("steps 至少 2 步")
    step_ids = set()
    for i, s in enumerate(steps):
        tag = "steps[%d]" % i
        for f in ("id", "name", "instruction", "checkpoint"):
            if not s.get(f):
                errs.append("%s 缺少 %s" % (tag, f))
        sid = s.get("id")
        if sid in step_ids:
            errs.append("%s step id 重复：%r" % (tag, sid))
        step_ids.add(sid)
        cp = str(s.get("checkpoint", ""))
        for w in VAGUE_CHECKPOINT:
            if w in cp:
                errs.append("%s checkpoint 含不可判定词「%s」：%s" % (tag, w, cp[:40]))
                break
        if "自行决定" in str(s.get("instruction", "")) or "视情况而定" in str(s.get("instruction", "")):
            errs.append("%s instruction 把决策推回给用户，执行者无法自主完成" % tag)
        ft = s.get("fail_to")
        if ft and ft not in {x.get("id") for x in steps}:
            errs.append("%s fail_to 指向不存在的 step：%r" % (tag, ft))

    ev = obj.get("evaluate") or {}
    if not ev.get("self_check"):
        errs.append("evaluate.self_check 不可为空 —— 这是本方法生效的最低保障")

    # 纯度扫描：整个文件序列化后扫
    blob = json.dumps(obj, ensure_ascii=False)
    for pat, msg in FORBIDDEN_PATTERNS:
        m = re.search(pat, blob, re.IGNORECASE)
        if m:
            errs.append("[纯度] %s（命中：%s）" % (msg, m.group(0)))

    for w in errs:
        print("  ERROR  %s" % w)
    for w in warns:
        print("  WARN   %s" % w)
    return errs, warns


def cmd_validate(args):
    paths = list(getattr(args, "paths", None) or [])
    targets = []
    for p in paths:
        if os.path.isdir(p):
            targets += sorted(glob.glob(os.path.join(p, "*.json")))
        else:
            targets.append(p)
    if not targets:
        targets = sorted(glob.glob(os.path.join(SKILL_DIR, "*.json")))
    targets = [t for t in targets if not os.path.basename(t).startswith("_")]

    total_err = 0
    for t in targets:
        name = os.path.basename(t)
        try:
            with open(t, "r", encoding="utf-8") as f:
                obj = json.load(f)
        except Exception as e:
            print("[%s] JSON 解析失败: %s" % (name, e))
            total_err += 1
            continue
        print("[%s]" % name)
        errs, _ = validate_one(obj, t)
        if errs:
            total_err += 1
        else:
            print("  OK  cid=%s" % skill_cid(obj))
    print("\n%d 个文件，%d 个有错误。" % (len(targets), total_err))
    return 1 if total_err else 0


# ---------------------------------------------------------------- 命令
def cmd_list(args):
    skills = load_skills()
    by_cat = {}
    for s in skills:
        by_cat.setdefault(s.get("category", "?"), []).append(s)
    print("OpenLMP v0.1 — 已收录 %d 个学习方法（全部 CC0 公共领域）\n" % len(skills))
    for cat in sorted(by_cat):
        print("【%s】" % cat)
        for s in by_cat[cat]:
            ev = {"high": "循证强", "medium": "循证中", "anecdotal": "经验"}.get(
                s.get("evidence"), "?")
            dur = sum(x.get("duration_min", 0) for x in s.get("steps", []))
            print("  %-28s %-22s %-5s %2d步/~%dmin" % (
                s["id"], s["name"], ev, len(s.get("steps", [])), dur))
        print("")
    return 0


def cmd_show(args):
    skills = {s["id"]: s for s in load_skills()}
    if args.id not in skills:
        print("没有这个方法。可用：%s" % ", ".join(sorted(skills)))
        return 1
    print(json.dumps(skills[args.id], ensure_ascii=False, indent=2))
    return 0


def _tokenize(text):
    """中文用二元切分（CJK bigram），拉丁/数字用词。零依赖，无外部词典。"""
    t = text.lower()
    tokens = set()
    # 拉丁词与数字
    for w in re.findall(r"[a-z0-9][a-z0-9\-_]*", t):
        tokens.add(w)
    # CJK 二元切分：单字信息量太低，二元命中更准
    for run in re.findall(r"[\u4e00-\u9fff]+", t):
        if len(run) == 1:
            tokens.add(run)
        else:
            for i in range(len(run) - 1):
                tokens.add(run[i:i + 2])
    return tokens


def cmd_recommend(args):
    """本地关键词检索，零网络。"""
    query = args.query
    qt = _tokenize(query)
    skills = load_skills()
    scored = []
    for s in skills:
        # 字段权重：名称 > 描述 > 适用场景（名称命中说明用户问的正是这个方法）
        name = " ".join([s.get("name", ""), s.get("name_en", "")])
        desc = s.get("description", "")
        use = " ".join(s.get("when_to_use", []))
        nt, dt = _tokenize(name), _tokenize(desc)
        ut = _tokenize(use)
        score = 0
        for w in qt:
            if w in nt:
                score += 6
            if w in dt:
                score += 3
            if w in ut:
                score += 2
        # 否定指向软惩罚：本 Skill 说「这情况该用别的」时轻度降权。
        # ⚠️ 刻意不做成硬过滤——一旦惩罚过强会出现「全被压成0 → 诚实报不命中」，
        #   而这违背协议精神（本方法是帮你找到方法，不是劝退）。
        #   正确做法是：排后 + 在输出里明示「这情况请改用 X」，让人自己判断。
        if s.get("when_not_to_use"):
            nwt = _tokenize(" ".join(s["when_not_to_use"]))
            if qt & nwt:
                score = score * 0.5
        if score:
            scored.append((score, s))
    # 同分时按 id 稳定排序，保证结果可复现
    scored.sort(key=lambda x: (-x[0], x[1]["id"]))
    if not scored:
        print("没有命中。协议规定：匹配不到就诚实说没有，不要硬凑。")
        return 1
    print("针对「%s」的本地检索结果（无网络请求）：\n" % args.query)
    for score, s in scored[:5]:
        print("  %-26s %-14s  ← %s" % (s["id"], s["name"], s["description"]))
        print("  %s适用于：%s" % (" " * 26, "；".join(s.get("when_to_use", [])[:2])))
        # 把「别用我时用谁」显式告诉用户 —— 这是本协议的检索独有设计
        nua = s.get("when_not_to_use") or []
        if nua:
            for x in nua:
                m = re.findall(r"用\s*([a-z0-9][a-z0-9\-]*)", x)
                if m:
                    print("  %s若你的情况是「%s」→ 改用：%s"
                          % (" " * 26, x[:18], ", ".join(m)))
                    break
        print("")
    return 0


def cmd_run(args):
    skills = {s["id"]: s for s in load_skills()}
    if args.id not in skills:
        print("没有这个方法。可用：%s" % ", ".join(sorted(skills)))
        return 1
    s = skills[args.id]
    topic = args.topic or "(未指定主题)"
    print("=" * 66)
    print("%s  %s  v%s   cid=%s" % (s["name"], s["name_en"], s["version"], skill_cid(s)))
    print("循证等级：%s   协议：LMP %s   许可：%s" % (
        s.get("evidence"), s["lmp"], s["license"]))
    print("解决：%s" % s["description"])
    print("主题：%s" % topic)
    print("=" * 66)
    nua = s.get("when_not_to_use", [])
    if nua:
        print("\n⚠ 不适用场景（先看这个）：")
        for x in nua:
            print("   · %s" % x)
    print("\n执行剧本：\n")
    for i, st in enumerate(s.get("steps", []), 1):
        print("─" * 64)
        print("步骤 %d/%d  %s   [%s分钟]   (id=%s)" % (
            i, len(s["steps"]), st["name"], st.get("duration_min", "?"), st["id"]))
        print("\n%s\n" % st["instruction"])
        print("  ✓ 完成判据：%s" % st["checkpoint"])
        if st.get("fail_to"):
            print("  ↩ 未达成则回到：%s" % st["fail_to"])
        if st.get("output"):
            print("  → 产出：%s" % st["output"])
    print("\n" + "─" * 64)
    print("结束后必须逐条自检：")
    for q in s.get("evaluate", {}).get("self_check", []):
        print("   1. %s" % q)
    print("\n生效标准：")
    for c in s.get("evaluate", {}).get("success_criteria", []):
        print("   · %s" % c)
    dc = (s.get("agent_contract") or {}).get("degrade_to")
    if dc:
        print("\n降级路径：%s" % dc)
    print("\n全程本地执行，无注册、无上传、无 API Key。")
    return 0


def cmd_review(args):
    st = load_state()
    today = today_str()
    queue = []
    for sid, rec in st.get("skills", {}).items():
        nd = rec.get("next_due")
        if nd and nd <= today:
            queue.append((nd, sid, rec))
    queue.sort()
    print("今日复习队列（基准 %s），共 %d 条\n" % (today, len(queue)))
    if not queue:
        print("队列为空 —— 这可能意味着还没入库，也可能是过度拖期。")
        return 0
    for nd, sid, rec in queue:
        sname = sid
        skills = {x["id"]: x for x in load_skills()}
        if sid in skills:
            sname = "%s(%s)" % (skills[sid]["name"], sid)
        print("  到期 %s  %-34s ease=%.2f int=%.1fd reps=%d" % (
            nd, sname, rec.get("ease_factor", 2.5),
            rec.get("interval_days", 0), rec.get("repetitions", 0)))
    print("\n自评分规范（q 0-5，q<3 会把 interval 重置为 1 天）：")
    print("  0=完全想不出  1=想了很久才出  2=提示后想起")
    print("  3=基本想出   4=轻松想出    5=毫不费力")
    print("\n按协议：每条复习后必须写回 learner-state.json；单日总时长上限 20 分钟。")
    return 0


def cmd_selftest(args):
    print("OpenLMP v0.1 自检\n" + "=" * 60)
    ok = True
    skills = load_skills()
    print("1. Skill 数量：%d" % len(skills))
    ok &= len(skills) >= 10

    print("\n2. 逐个校验：")
    bad = 0
    for s in skills:
        errs, _ = validate_one(s)
        if errs:
            bad += 1
            print("   ✗ %s（%d 个问题）" % (s["id"], len(errs)))
    print("   通过 %d / %d" % (len(skills) - bad, len(skills)))
    ok &= (bad == 0)

    print("\n3. 纯度反向测试（故意塞违规，应被拒绝）：")
    dirty = json.loads(json.dumps(skills[0]))
    dirty["steps"][0]["instruction"] += "，请先注册账号并输入 API Key"
    errs, _ = validate_one(dirty)
    caught = any("纯度" in e for e in errs)
    print("   %s 注入的注册/API Key 违规被拦截" % ("✓" if caught else "✗"))
    ok &= caught

    print("\n4. 模糊 checkpoint 反向测试：")
    dirty2 = json.loads(json.dumps(skills[0]))
    dirty2["steps"][0]["checkpoint"] = "深刻理解这个概念"
    errs2, _ = validate_one(dirty2)
    caught2 = any("不可判定" in e for e in errs2)
    print("   %s 「深刻理解」被判为不可判定" % ("✓" if caught2 else "✗"))
    ok &= caught2

    print("\n5. 虚标循证反向测试：")
    dirty3 = json.loads(json.dumps(skills[0]))
    dirty3["evidence"] = "high"
    dirty3["evidence_refs"] = []
    errs3, _ = validate_one(dirty3)
    caught3 = any("虚标" in e for e in errs3)
    print("   %s evidence=high 无引用被拒绝" % ("✓" if caught3 else "✗"))
    ok &= caught3

    print("\n6. SM-2 边界测试：")
    e, i, r = sm2(0, 2.5, 0, 0)
    ok_i = (i == 1.0 and r == 0)
    print("   %s q=0 → interval 归 1、reps 归 0（实测 i=%.1f r=%d）" % (
        "✓" if ok_i else "✗", i, r))
    ok &= ok_i
    e2, i2, r2 = sm2(0, 2.5, 1, 5)
    ok2 = abs(i2 - 1.0) < 1e-9
    print("   %s q=5 首答 → interval=1（实测 %.1f）" % ("✓" if ok2 else "✗", i2))
    ok &= ok2
    # reps 表示「本次之前已成功次数」，函数内先 +1 再定 interval
    _, i3, _ = sm2(1, 2.5, 1, 5)
    ok3 = abs(i3 - 6.0) < 1e-9
    print("   %s q=5 二答 → interval=6（实测 %.1f）" % ("✓" if ok3 else "✗", i3))
    ok &= ok3
    _, i4, _ = sm2(2, 2.5, 6, 5)
    ok4 = abs(i4 - 6 * 2.6) < 0.1
    print("   %s q=5 三答 → interval=6×ease=15.6（实测 %.1f）" % (
        "✓" if ok4 else "✗", i4))
    ok &= ok4
    e4, _, _ = sm2(5, 1.3, 10, 0)
    ok4 = e4 >= 1.3
    print("   %s ease 下界锁定 1.3（实测 %.3f）" % ("✓" if ok4 else "✗", e4))
    ok &= ok4

    print("\n7. CID 稳定性：")
    c1 = skill_cid(skills[0])
    c2 = skill_cid(json.loads(json.dumps({k: v for k, v in skills[0].items()
                                         if not k.startswith("__")})))
    print("   %s 同内容同 CID：%s" % ("✓" if c1 == c2 else "✗", c1))
    ok &= (c1 == c2)

    print("\n" + "=" * 60)
    print("结果：%s" % ("全部通过 ✅" if ok else "存在失败 ❌"))
    return 0 if ok else 1


# ---------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser(
        prog="lmp", description="OpenLMP 参考执行器 v0.1（零依赖，全本地）")
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("list", help="列出全部 Skill")
    p_show = sub.add_parser("show", help="查看单个 Skill")
    p_show.add_argument("id")
    p_val = sub.add_parser("validate", help="按 schema + 纯度规则校验")
    p_val.add_argument("paths", nargs="*")
    p_rec = sub.add_parser("recommend", help="本地检索推荐方法")
    p_rec.add_argument("query")
    p_run = sub.add_parser("run", help="打印某方法的执行剧本")
    p_run.add_argument("id")
    p_run.add_argument("--topic", default="")
    sub.add_parser("review", help="今日到期复习队列")
    sub.add_parser("selftest", help="端到端自检")

    args = ap.parse_args()
    if not args.cmd:
        ap.print_help()
        return 0
    return {
        "list": cmd_list,
        "show": cmd_show,
        "validate": cmd_validate,
        "recommend": cmd_recommend,
        "run": cmd_run,
        "review": cmd_review,
        "selftest": cmd_selftest,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())