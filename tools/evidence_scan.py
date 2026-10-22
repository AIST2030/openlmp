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
