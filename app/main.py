import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.core.config import settings
from app.core.database import init_db
from app.api.vault import router as vault_router
from app.api.mcp import router as mcp_router
from app.api.kanban import router as kanban_router
from app.api.chat import router as chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Khởi tạo cơ sở dữ liệu SQLite
    init_db()
    print("🚀 [Brain Thịnh Vượng Số] Hệ thống AI OS đã khởi động thành công!")
    yield
    print("🛑 [Brain Thịnh Vượng Số] Đang tắt máy chủ an toàn...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký các router chức năng
app.include_router(vault_router)
app.include_router(mcp_router)
app.include_router(kanban_router)
app.include_router(chat_router)

# Mount thư mục static frontend
frontend_dir = settings.BASE_DIR / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

    @app.get("/")
    def serve_index():
        index_file = frontend_dir / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {"status": "running", "message": "Frontend đang được khởi tạo"}
