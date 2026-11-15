#!/usr/bin/env bash
# Script khởi chạy hệ điều hành AI OS - Brain Thịnh Vượng Số

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=========================================================="
echo "   🧠 BRAIN THỊNH VƯỢNG SỐ - AI OPERATING SYSTEM"
echo "=========================================================="

# Kiểm tra virtualenv
if [ ! -d ".venv" ]; then
    echo "⚠️  Chưa tìm thấy .venv, đang khởi tạo..."
    uv venv --python 3.12 .venv
    uv pip install --python .venv/bin/python --only-binary :all: fastapi "uvicorn[standard]" websockets httpx pydantic pydantic-settings pyyaml aiofiles python-multipart
fi

echo "🚀 Đang khởi động Server tại: http://localhost:8000 và http://localhost:7777 ..."
node proxy7777.js &
.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
