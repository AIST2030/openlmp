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
"""扫描 OpenLMP 主库方法的 evidence 等级分布，导出 evidence:high 的引用清单。"""
import json, glob, os, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else r"E:/视频创作/AIST2030/openlmp"
SKILL_DIR = os.path.join(ROOT, "skills")

files = sorted(glob.glob(os.path.join(SKILL_DIR, "*.json")))
dist = {}
recs = []
for f in files:
    try:
        d = json.load(open(f, encoding="utf-8"))
    except Exception as e:
        print("ERR", f, e)
        continue
    ev = d.get("evidence")
    dist[ev] = dist.get(ev, 0) + 1
    if ev == "high":
        recs.append({
            "id": d.get("id"),
            "name": d.get("name"),
            "category": d.get("category"),
            "evidence_refs": d.get("evidence_refs"),
        })

print("=== evidence 分布 ===")
for k in sorted(dist, key=lambda x: (x is None, str(x))):
    print(f"  {k!s:8} : {dist[k]}")
print(f"\n=== evidence:high 总数: {len(recs)} ===")
for r in recs:
    print(f"\n--- {r['id']} | {r['name']} | {r['category']}")
    print("   refs:", json.dumps(r["evidence_refs"], ensure_ascii=False))

out = os.path.join(ROOT, "docs", "evidence-audit", "high_refs.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump({"total": len(recs), "records": recs},
          open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n写到", out)
