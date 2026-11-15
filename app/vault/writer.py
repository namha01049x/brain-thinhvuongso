import os
from pathlib import Path
from typing import Optional, Dict, Any
import yaml
from app.core.config import settings
from app.vault.git_engine import git_commit

def save_note(rel_path: str, content: str, commit_msg: Optional[str] = None) -> bool:
    """Lưu hoặc cập nhật ghi chú và commit vào Git an toàn."""
    try:
        # Chuẩn hóa đường dẫn
        clean_path = rel_path.strip().lstrip("/")
        if not clean_path.endswith(".md"):
            clean_path += ".md"
            
        full_path = settings.VAULT_DIR / clean_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        full_path.write_text(content, encoding="utf-8")
        
        # Git commit tự động
        msg = commit_msg or f"Cập nhật note: {clean_path}"
        git_commit(msg)
        return True
    except Exception as e:
        print(f"Error saving note: {e}")
        return False

def delete_note(rel_path: str) -> bool:
    """Xóa một ghi chú an toàn."""
    try:
        full_path = settings.VAULT_DIR / rel_path
        if full_path.exists() and full_path.is_file():
            full_path.unlink()
            git_commit(f"Xóa note: {rel_path}")
            return True
        return False
    except Exception as e:
        print(f"Error deleting note: {e}")
        return False
