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
citation_lint.py —— 引用真实性闸门（零第三方依赖，Python 3.8+）

作用：校验所有 evidence: "high" 的方法，其 evidence_refs 每一条都必须能命中
      「已核验引用白名单」docs/evidence-audit/verified_refs.json 中的某一条。

匹配规则：年份 + 作者姓 + 期刊名（或书名）+ 卷期 + 页码 五项，
          全部以「子串」方式命中（忽略大小写、标点、空格）。
          这能精确抓住本次审计发现的三类错误：
            - 期刊写错（Atkinson 2000 写成 JEP，实为 RER）
            - 卷期写错（Bahrick 1993 写成 4(3)，实为 4(5)）
            - 查无来源（Bromley 1990 不在白名单即报错）

用法：
    python tools/citation_lint.py                     # 主库 skills/
    python tools/citation_lint.py --dir business/skills
    python tools/citation_lint.py --json              # 机器可读输出

退出码：0 = 全部通过；1 = 存在未命中/缺失的引用（CI 应视为失败）。
"""
import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_ALLOWLIST = os.path.join(ROOT, "docs", "evidence-audit", "verified_refs.json")
DEFAULT_DIR = os.path.join(ROOT, "skills")

# 归一化：只保留 数字 / 小写字母 / 中文，其余（空格、标点、连字符）全部剔除
_NON = re.compile(r"[^0-9a-z\u4e00-\u9fff]")


def norm(s):
    if s is None:
        return ""
    return _NON.sub("", str(s).lower())


def load_allowlist(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("refs", [])


def entry_tokens(e):
    """返回该白名单条目要求全部命中的归一化 token 列表。"""
    toks = [str(e.get("year", "")), norm(e.get("surname", ""))]
    # 期刊或书名
    venue = norm(e.get("venue", "") or e.get("title_key", ""))
    if venue:
        toks.append(venue)
    if e.get("type") == "journal":
        if e.get("volume_issue"):
            toks.append(norm(e["volume_issue"]))
        if e.get("pages"):
            toks.append(norm(e["pages"]))
    else:  # book：用书名关键字补足
        tk = norm(e.get("title_key", ""))
        if tk:
            toks.append(tk)
    return [t for t in toks if t]


def match_ref(ref, allowlist):
    """返回命中的白名单条目 id，或 None。"""
    nr = norm(ref)
    for e in allowlist:
        if all(tok in nr for tok in entry_tokens(e)):
            return e.get("id")
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description="校验 evidence:high 的引用是否全部命中已核验白名单")
    ap.add_argument("--dir", default=DEFAULT_DIR, help="要扫描的 skills 目录（默认主库 skills/）")
    ap.add_argument("--allowlist", default=DEFAULT_ALLOWLIST, help="白名单 JSON 路径")
    ap.add_argument("--json", action="store_true", help="输出 JSON 而非人类可读文本")
    args = ap.parse_args(argv)

    if not os.path.isfile(args.allowlist):
        sys.stderr.write("找不到白名单文件: %s\n" % args.allowlist)
        return 2

    allowlist = load_allowlist(args.allowlist)
    files = sorted(glob.glob(os.path.join(args.dir, "*.json")))

    results = []
    n_high = 0
    n_refs = 0
    n_ok = 0
    failures = []

    for path in files:
        base = os.path.basename(path)
        if base.startswith("_"):  # 模板文件跳过
            continue
        try:
            with open(path, encoding="utf-8") as f:
                sk = json.load(f)
        except Exception as exc:
            failures.append({"skill": base, "ref": None, "reason": "JSON 解析失败: %s" % exc})
            continue
        if sk.get("evidence") != "high":
            continue
        n_high += 1
        refs = sk.get("evidence_refs") or []
        if not refs:
            failures.append({"skill": base, "ref": None,
                             "reason": "evidence=high 但 evidence_refs 为空"})
            continue
        for ref in refs:
            n_refs += 1
            hit = match_ref(ref, allowlist)
            if hit:
                n_ok += 1
                results.append({"skill": base, "ref": ref, "matched": hit, "ok": True})
            else:
                failures.append({"skill": base, "ref": ref, "reason": "未命中已核验白名单"})
                results.append({"skill": base, "ref": ref, "matched": None, "ok": False})

    with_doi = sum(1 for e in allowlist if e.get("doi"))

    if args.json:
        print(json.dumps({
            "dir": args.dir,
            "high_methods": n_high,
            "refs_checked": n_refs,
            "refs_matched": n_ok,
            "allowlist_size": len(allowlist),
            "allowlist_with_doi": with_doi,
            "failures": failures,
            "ok": not failures,
        }, ensure_ascii=False, indent=1))
        return 0 if not failures else 1

    print("引用白名单校验 —— 目录: %s" % args.dir)
    print("  白名单条目: %d 条（其中 %d 条带 DOI）" % (len(allowlist), with_doi))
    print("  evidence=high 方法: %d 个" % n_high)
    print("  引用条目: %d 条，命中 %d 条" % (n_refs, n_ok))
    if failures:
        print("\n❌ 未通过，共 %d 处：" % len(failures))
        for fl in failures:
            if fl["ref"] is None:
                print("  - [%s] %s" % (fl["skill"], fl["reason"]))
            else:
                print("  - [%s] %s" % (fl["skill"], fl["reason"]))
                print("      引用: %s" % fl["ref"])
        print("\n提示：新增 high 引用须先入 docs/evidence-audit/verified_refs.json 并填 verified_on。")
        return 1
    print("\n✅ 全部通过：所有 evidence:high 引用均命中已核验白名单。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
