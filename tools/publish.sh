#!/usr/bin/env bash
# OpenLMP 一键推送脚本
# 用途：登录 GitHub 后，一条命令同时推到 GitHub + AtomGit。
#
# 用法：
#   bash tools/publish.sh <你的GitHub用户名> [你的AtomGit用户名]
#
# 前置条件：
#   1. 已安装 gh CLI 并完成 gh auth login
#   2. 本地已完成首次 commit（已自带 v0.1.0 tag）
#   3. 两个平台上已建好**空的公开仓库** openlmp（不要勾选自动添加 README/LICENSE）

set -euo pipefail

GH_USER="${1:?用法: bash tools/publish.sh <GitHub用户名> [AtomGit用户名]}"
AT_USER="${2:-}"
REPO="openlmp"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "=============================================="
echo " OpenLMP 发布 ·$(cd "$ROOT" && pwd)"
echo " GitHub 用户: $GH_USER"
echo " AtomGit 用户: ${AT_USER:-（跳过）}"
echo "=============================================="

# ---------- 0. 发布前强制自检：不过就不许发 ----------
echo ""
echo "[0/6] 发布前自检（不通过则中止）"
PY=""
for c in python python3 py; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c "import sys;sys.exit(0 if sys.version_info>=(3,8) else 1)" 2>/dev/null; then
    PY="$c"; break
  fi
done
[ -n "$PY" ] || { echo "✗ 未找到 Python 3.8+"; exit 1; }
"$PY" runtime/lmp.py selftest >/dev/null || { echo "✗ selftest 未通过，拒绝发布"; exit 1; }
"$PY" runtime/lmp.py validate skills/ >/dev/null || { echo "✗ Skill 校验未通过，拒绝发布"; exit 1; }
echo "  ✓ selftest + validate 全绿"

# ---------- 1. 隐私硬检查：个人学习数据绝不入库 ----------
echo ""
echo "[1/6] 隐私硬检查"
if git ls-files | grep -qi "learner-state.json"; then
  echo "  ✗ learner-state.json 被跟踪，违反「数据不出本地」承诺，中止"
  exit 1
fi
echo "  ✓ learner-state.json 未被跟踪"

# ---------- 2. 检查 commit 与 tag ----------
echo ""
echo "[2/6] 检查 commit 与 tag"
git rev-parse HEAD >/dev/null || { echo "✗ 尚无 commit，请先 git commit"; exit 1; }
git rev-parse v0.1.0 >/dev/null 2>&1 || { echo "  ⚠ 未找到 v0.1.0 tag"; }
echo "  ✓ commit: $(git log --oneline -1)"
echo "  ✓ tag: $(git tag -l | tr '\n' ' ')"

# ---------- 3. GitHub：确保登录 ----------
echo ""
echo "[3/6] GitHub 认证状态"
export PATH="$PATH:/c/Program Files/GitHub CLI"
if ! command -v gh >/dev/null 2>&1; then
  echo "  ✗ 未找到 gh CLI"; exit 1
fi
if ! gh auth status >/dev/null 2>&1; then
  echo "  ✗ 未登录。请先执行： gh auth login"; exit 1
fi
AUTHED="$(gh api user --jq .login 2>/dev/null || echo "")"
echo "  ✓ 已登录为 $AUTHED"
if [ "$AUTHED" != "$GH_USER" ]; then
  echo "  ⚠ 当前登录账号是 $AUTHED，与传入的 $GH_USER 不一致，仍继续（以登录账号为准）"
fi

# ---------- 4. 创建/确认 GitHub 仓库 ----------
echo ""
echo "[4/6] GitHub 仓库"
GH_REPO_URL="https://github.com/$AUTHED/$REPO.git"
if gh repo view "$AUTHED/$REPO" >/dev/null 2>&1; then
  echo "  ✓ 仓库已存在：$AUTHED/$REPO"
else
  gh repo create "$AUTHED/$REPO" --public \
    --description "让学习方法成为全人类共有的公共资产。纯 JSON 协议 + 零依赖执行器，CC0。" \
    --disable-issues=false --enable-wiki=false >/dev/null
  echo "  ✓ 已创建公开仓库：$AUTHED/$REPO"
fi

git remote remove origin 2>/dev/null || true
git remote add origin "$GH_REPO_URL"
git push -u origin main
git push origin v0.1.0 2>/dev/null || echo "  ⚠ tag 推送失败（可稍后补）"
echo "  ✓ 已推送 → $GH_REPO_URL"

# ---------- 5. AtomGit ----------
echo ""
echo "[5/6] AtomGit 推送"
if [ -n "$AT_USER" ]; then
  # AtomGit 的 git 地址实测为 gitcode.com 域
  AT_URL="https://gitcode.com/$AT_USER/$REPO.git"
  git remote remove atomgit 2>/dev/null || true
  git remote add atomgit "$AT_URL"
  if git push -u atomgit main 2>&1 | tail -5; then
    echo "  ✓ 已推送 → $AT_URL"
    git push atomgit v0.1.0 2>/dev/null || echo "  ⚠ tag 推送失败"
  else
    echo "  ⚠ AtomGit 推送失败。请确认：① 仓库已建好 ② 仓库为公开 ③ 你已配置访问令牌"
    echo "    需要帮助随时说，不影响 GitHub 那份。"
  fi
else
  echo "  –未提供 AtomGit 用户名，跳过"
fi

# ---------- 6. 汇总 ----------
echo ""
echo "[6/6] 完成"
echo "=============================================="
echo " 远端列表："
git remote -v | sed 's/^/   /'
echo ""
echo " 下一步（建议）："
echo "   1. 去仓库设置里确认 README 正常显示"
echo "   2. 检查 Actions 是否全绿（Settings → Actions）"
echo "   3. 打 v0.1.1 之前，先补更多 Skill —— 数量是唯一护城河"
echo "=============================================="
echo ""
echo "提醒：仓库里永远不要放你的电话/邮箱。"
echo "      你不是项目的单点故障，你应该是项目之外的人。"
echo "=============================================="