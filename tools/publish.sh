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

# OpenLMP 推送脚本 v2 —— 支持 token 直传，无需 gh auth login
#
# 用法一（推荐，最快）：
#   bash tools/publish.sh --token ghp_xxxxxxxxxxxx 用户名 [AtomGit用户名]
#
# 用法二（已 gh auth login 时）：
#   bash tools/publish.sh 用户名 [AtomGit用户名]
#
# 安全说明：
#   - token 只在内存中通过环境变量传递，不写入 git config，不落盘
#   - 推送完成后请立刻去 GitHub 设置页吊销该 token

set -euo pipefail

GH_TOKEN_ARG=""
if [ "${1:-}" = "--token" ]; then
  GH_TOKEN_ARG="${2:?--token 后必须跟 token}"
  shift 2
fi

GH_USER="${1:?用法: bash tools/publish.sh [--token TOKEN] <GitHub用户名> [AtomGit用户名]}"
AT_USER="${2:-}"
REPO="openlmp"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "=============================================="
echo " OpenLMP 发布"
echo " GitHub 用户: $GH_USER"
echo " AtomGit 用户: ${AT_USER:-（跳过）}"
echo "=============================================="

# ---------- 0. 发布前强制自检：不过就不许发 ----------
echo ""
echo "[0/6] 发布前自检（不通过则中止发布）"
PY=""
for c in python python3 py; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c "import sys;sys.exit(0 if sys.version_info>=(3,8) else 1)" 2>/dev/null; then
    PY="$c"; break
  fi
done
[ -n "$PY" ] || { echo "  ✗ 未找到 Python 3.8+"; exit 1; }
"$PY" runtime/lmp.py selftest   >/dev/null || { echo "  ✗ selftest 未通过，拒绝发布"; exit 1; }
"$PY" runtime/lmp.py validate skills/ >/dev/null || { echo "  ✗ Skill 校验未通过，拒绝发布"; exit 1; }
echo "  ✓ selftest + validate 全绿"

# ---------- 1. 隐私硬检查 ----------
echo ""
echo "[1/6] 隐私硬检查（协议核心承诺）"
if git ls-files | grep -qi "learner-state.json"; then
  echo "  ✗ learner-state.json 被跟踪，违反「数据不出本地」，中止发布"
  exit 1
fi
echo "  ✓ learner-state.json 未被跟踪"
if git ls-files | grep -qiE "(2265205847|18589521211)"; then
  echo "  ⚠ 警告：仓库中疑似含个人联系方式文件，建议移除"
else
  echo "  ✓ 仓库中无个人联系方式文件"
fi

# ---------- 2. commit / tag ----------
echo ""
echo "[2/6] 检查 commit 与 tag"
git rev-parse HEAD >/dev/null || { echo "  ✗ 尚无 commit"; exit 1; }
echo "  ✓ $(git log --oneline -1)"
TAGS="$(git tag -l | tr '\n' ' ')"
echo "  ✓ tags: $TAGS"

# ---------- 3. 认证准备 ----------
echo ""
echo "[3/6] 认证"
if [ -n "$GH_TOKEN_ARG" ]; then
  export GH_TOKEN="$GH_TOKEN_ARG"
  export GITHUB_TOKEN="$GH_TOKEN_ARG"
  AUTHED="$(gh api user --jq .login 2>/dev/null || echo "$GH_USER")"
  echo "  ✓ 使用 token 认证，账号: $AUTHED"
else
  export PATH="$PATH:/c/Program Files/GitHub CLI"
  if ! command -v gh >/dev/null 2>&1; then
    echo "  ✗ 未找到 gh CLI，也未提供 --token"; exit 1
  fi
  if ! gh auth status >/dev/null 2>&1; then
    echo "  ✗ 未登录。请执行 gh auth login --web，或改用 --token 方式"; exit 1
  fi
  AUTHED="$(gh api user --jq .login 2>/dev/null || echo "$GH_USER")"
  echo "  ✓ 使用 gh 认证，账号: $AUTHED"
fi

# ---------- 4. GitHub 仓库创建 + 推送 ----------
echo ""
echo "[4/6] GitHub"
GH_REPO_URL="https://github.com/$AUTHED/$REPO.git"
if gh repo view "$AUTHED/$REPO" >/dev/null 2>&1; then
  echo "  ✓ 仓库已存在"
else
  gh repo create "$AUTHED/$REPO" --public \
    --description "让学习方法成为全人类共有的公共资产。纯 JSON 协议 + 零依赖执行器，CC0。" \
    --enable-wiki=false >/dev/null
  echo "  ✓ 已创建公开仓库"
fi
git remote remove origin 2>/dev/null || true
git remote add origin "$GH_REPO_URL"
if git push -u origin main; then
  echo "  ✓ main 已推送"
  for t in $TAGS; do git push origin "$t" 2>/dev/null || echo "  ⚠ tag $t 推送失败"; done
  echo "  ✓ tags 已推送"
else
  echo "  ✗ main 推送失败。请确认 token 有 public_repo 权限。"; exit 1
fi

# ---------- 5. AtomGit（开放原子基金会） ----------
echo ""
echo "[5/6] AtomGit"
if [ -n "$AT_USER" ]; then
  AT_URL="https://atomgit.com/$AT_USER/$REPO.git"
  git remote remove atomgit 2>/dev/null || true
  git remote add atomgit "$AT_URL"
  echo "  仓库地址：$AT_URL"
  echo "  认证：用户名填你的 AtomGit 账号，密码位置粘贴【访问令牌】"
  echo "  令牌获取：AtomGit → 个人设置 → 访问令牌 → 新建（勾 repo 读写权限）"
  if git push -u atomgit "$(git rev-parse --abbrev-ref HEAD)"; then
    echo "  ✓ 当前分支已推送 → $AT_URL"
    for t in $TAGS; do git push atomgit "$t" 2>/dev/null || echo "  ⚠ tag $t 推送失败"; done
    echo "  ✓ tags 已推送"
  else
    echo "  ⚠ AtomGit 推送失败（不影响 GitHub 那份）"
  fi
else
  echo "  – 未提供 AtomGit 用户名，跳过"
fi

# ---------- 6. 收尾 ----------
echo ""
echo "[6/6] 完成"
echo "=============================================="
git remote -v | sed 's/^/  /'
echo ""
echo " 后续："
echo "  1. 检查 Actions 是否全绿（仓库 Settings → Actions）"
echo "  2. ⚠️ 立刻去 GitHub 设置页吊销刚才用的 token"
echo "     https://github.com/settings/tokens"
echo "=============================================="
unset GH_TOKEN GITHUB_TOKEN