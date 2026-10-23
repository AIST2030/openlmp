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
从 skills/*.json 重建 registry/registry.json。

为什么要有这个脚本：registry 曾是手工维护的，扩到 50 个方法时忘了同步，
导致索引停在 count=22（README 也残留 22/11 的历史数字）。本脚本让索引可一键重建，
cid 复用 runtime/lmp.py 的 skill_cid()，保证与执行器口径一致。

用法：python tools/build_registry.py
排除 _ 前缀的样板文件（_template.json）。
"""
import json, os, sys, datetime

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "runtime"))
from lmp import skill_cid  # 复用执行器的内容寻址算法

SKILLS_DIR = os.path.join(HERE, "skills")
OUT = os.path.join(HERE, "registry", "registry.json")


def build():
    entries = []
    for fn in sorted(os.listdir(SKILLS_DIR)):
        if not fn.endswith(".json") or fn.startswith("_"):
            continue
        with open(os.path.join(SKILLS_DIR, fn), encoding="utf-8") as f:
            d = json.load(f)
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
            "file": "skills/" + fn,
        })
    entries.sort(key=lambda e: e["id"])

    reg = {
        "registry": "openlmp-skill-index",
        "lmp": "0.1",
        "generated_at": datetime.date.today().isoformat(),
        "note": "本清单不是唯一真理。任何人都可本地维护并提供 diff；我们不设唯一官方 registry。",
        "count": len(entries),
        "skills": entries,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("registry rebuilt: count=%d -> %s" % (len(entries), OUT))


if __name__ == "__main__":
    build()
