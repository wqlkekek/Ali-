#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "❌ 未检测到 python3，请先安装 Python 3.10+（建议使用官方安装包或 Homebrew）。"
  exit 1
fi

PYTHON_VERSION="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
REQUIRED_MAJOR=3
REQUIRED_MINOR=10

if ! python3 - <<'PY'
import sys
ok = (sys.version_info.major, sys.version_info.minor) >= (3, 10)
raise SystemExit(0 if ok else 1)
PY
then
  echo "❌ 当前 Python 版本为 ${PYTHON_VERSION}，需要 3.10 或更高版本。"
  exit 1
fi

echo "✅ Python 版本检查通过：${PYTHON_VERSION}"

if [ ! -d ".venv" ]; then
  echo "➡️ 首次运行：创建虚拟环境 .venv"
  python3 -m venv .venv
else
  echo "✅ 检测到已有虚拟环境 .venv"
fi

# shellcheck source=/dev/null
source .venv/bin/activate

echo "➡️ 升级 pip"
python -m pip install --upgrade pip

echo "➡️ 安装项目依赖"
pip install -r requirements.txt

HOST="0.0.0.0"
PORT="8000"

if lsof -iTCP:"${PORT}" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "⚠️ 端口 ${PORT} 已被占用。将自动改用 8010。"
  PORT="8010"
fi

echo "🚀 正在启动服务：http://127.0.0.1:${PORT}/"
echo "📘 Swagger 文档：http://127.0.0.1:${PORT}/docs"

# 尝试自动打开浏览器（失败不影响服务启动）
open "http://127.0.0.1:${PORT}/" >/dev/null 2>&1 || true

exec uvicorn app.main:app --host "$HOST" --port "$PORT" --reload
