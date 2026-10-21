#!/usr/bin/env bash
# 给 GitHub 仓库补门面：description + homepage + topics
# 用法：GH_TOKEN=ghp_xxx bash tools/set-repo-meta.sh
# 注意：token 只走环境变量，不落盘、不写 git config

set -euo pipefail

REPO="AIST2030/openlmp"
DESC="让学习方法成为公共资产。OpenLMP 学习方法协议：50 个方法、214 步可判定验收线，纯 JSON + 零依赖 Python 执行器，CC0-1.0 公共领域，可商用。"
HOMEPAGE="https://atomgit.com/gcw_QqOH7CjT/openlmp"

TOPICS='["openlmp","lmp","learning-methods","learning-protocol","learning-science","study-skills","spaced-repetition","active-recall","feynman-technique","zettelkasten","deliberate-practice","interleaving","metacognition","self-explanation","retrieval-practice","knowledge-management","self-directed-learning","cc0","public-domain","zero-dependency"]'

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