#!/usr/bin/env bash
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

# 给 GitHub 仓库补门面：description + homepage + topics
# 用法：GH_TOKEN=ghp_xxx bash tools/set-repo-meta.sh
# 注意：token 只走环境变量，不落盘、不写 git config

set -euo pipefail

REPO="AIST2030/openlmp"
DESC="让学习方法成为公共资产。OpenLMP 学习方法协议：主库 107 个方法 / 445 步可判定验收线 + 商业子库 15 个商业决策框架，纯 JSON + 零依赖 Python 执行器；方法内容 CC0-1.0 公共领域，协议与执行器木兰宽松许可证 v2（MulanPSL-2.0），可商用。"
HOMEPAGE="https://atomgit.com/gcw_QqOH7CjT/openlmp"

TOPICS='["openlmp","lmp","learning-methods","learning-protocol","learning-science","study-skills","spaced-repetition","active-recall","feynman-technique","zettelkasten","deliberate-practice","metacognition","retrieval-practice","knowledge-management","self-directed-learning","cc0","public-domain","zero-dependency","business-framework","thinking-analysis-methods"]'

if [ -z "${GH_TOKEN:-}" ]; then
  echo "错误：请先设置 GH_TOKEN 环境变量。"
  echo "  export GH_TOKEN=你的令牌"
  exit 1
fi

echo "==> 设置 description / homepage"
curl -sS -X PATCH \
  -H "Authorization: Bearer $GH_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$REPO" \
  -d "$(python -c "import json,sys;print(json.dumps({'description':sys.argv[1],'homepage':sys.argv[2]}))" "$DESC" "$HOMEPAGE")" \
  -o /dev/null -w "  HTTP:%{http_code}\n"

echo "==> 设置 topics"
curl -sS -X PUT \
  -H "Authorization: Bearer $GH_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$REPO/topics" \
  -d "{\"names\":$TOPICS}" \
  -o /dev/null -w "  HTTP:%{http_code}\n"

echo ""
echo "==> 核对结果"
curl -sS "https://api.github.com/repos/$REPO" | python -c "
import sys,json
d=json.load(sys.stdin)
print('  description :', d.get('description'))
print('  homepage    :', d.get('homepage'))
print('  topics      :', ', '.join(d.get('topics',[])))
"