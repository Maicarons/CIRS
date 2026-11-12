#!/usr/bin/env bash
# 拉取并合并 FIRS 上游更新，然后运行翻译校验。
# 用法：tools/sync_upstream.sh
set -euo pipefail

cd "$(dirname "$0")/.."

UPSTREAM_URL="https://github.com/andythenorth/firs.git"

# 首次使用时自动添加 upstream 远程
if ! git remote get-url upstream >/dev/null 2>&1; then
    echo "[SYNC] adding upstream remote: ${UPSTREAM_URL}"
    git remote add upstream "${UPSTREAM_URL}"
fi

echo "[SYNC] fetching upstream branches and tags"
git fetch upstream --tags

echo "[SYNC] merging upstream/main into $(git branch --show-current)"
# 合并冲突时保留两个开发线的改动，按并集处理；解决后重新运行本脚本
GIT_MERGE_AUTOEDIT=no git merge upstream/main

echo "[SYNC] checking translations"
python tools/check_translations.py

echo "[SYNC] done. Review the diff, then push to origin."
