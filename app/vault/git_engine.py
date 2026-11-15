import os
import subprocess
from pathlib import Path
from app.core.config import settings

def git_commit(message: str) -> bool:
    """Tự động commit thay đổi vào Git để đảm bảo an toàn dữ liệu."""
    if not settings.AUTO_COMMIT_GIT:
        return True
    try:
        # Kiểm tra xem có phải git repo không
        subprocess.run(["git", "status"], cwd=settings.BASE_DIR, check=True, capture_output=True)
        # Add vault data và system state
        subprocess.run(["git", "add", "vault_data", ".data"], cwd=settings.BASE_DIR, check=True, capture_output=True)
        # Commit
        res = subprocess.run(
            ["git", "commit", "-m", f"[AI OS Auto-Sync] {message}"],
            cwd=settings.BASE_DIR,
            capture_output=True,
            text=True
        )
        return res.returncode == 0 or "nothing to commit" in res.stdout
    except Exception as e:
        print(f"Git commit error: {e}")
        return False

def git_history(limit: int = 10):
    """Lấy danh sách các commit gần đây để xem lịch sử hoặc Undo."""
    try:
        res = subprocess.run(
            ["git", "log", f"-{limit}", "--pretty=format:%h|%an|%ar|%s"],
            cwd=settings.BASE_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        history = []
        for line in res.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split("|")
            if len(parts) >= 4:
                history.append({
                    "hash": parts[0],
                    "author": parts[1],
                    "time": parts[2],
                    "message": parts[3]
                })
        return history
    except Exception:
        return []
