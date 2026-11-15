import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
import yaml
from app.core.config import settings

def parse_markdown_file(file_path: Path) -> Dict[str, Any]:
    """Phân tích một file markdown: frontmatter, content, wikilinks, tags."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return {}

    frontmatter = {}
    body = content

    # Kiểm tra YAML frontmatter (--- ... ---)
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if fm_match:
        try:
            frontmatter = yaml.safe_load(fm_match.group(1)) or {}
            body = fm_match.group(2)
        except Exception:
            pass

    # Trích xuất Wikilinks [[Tên Note]]
    wikilinks = re.findall(r"\[\[(.*?)\]\]", content)
    clean_links = []
    for link in wikilinks:
        # Nếu có alias [[link|label]]
        target = link.split("|")[0].strip()
        if target:
            clean_links.append(target)

    # Trích xuất Tags (#tag)
    tags = re.findall(r"(?:^|\s)#([a-zA-Z0-9_\-\/]+)", content)
    if "tags" in frontmatter and isinstance(frontmatter["tags"], list):
        tags.extend(frontmatter["tags"])

    rel_path = str(file_path.relative_to(settings.VAULT_DIR))
    title = frontmatter.get("title") or file_path.stem

    return {
        "id": rel_path,
        "title": title,
        "path": rel_path,
        "filename": file_path.name,
        "folder": str(file_path.parent.relative_to(settings.VAULT_DIR)),
        "frontmatter": frontmatter,
        "tags": list(set(tags)),
        "wikilinks": list(set(clean_links)),
        "size": len(content),
        "updated_at": file_path.stat().st_mtime,
        "excerpt": body.strip()[:200] + ("..." if len(body.strip()) > 200 else "")
    }

def get_all_notes() -> List[Dict[str, Any]]:
    """Duyệt toàn bộ thư mục Second Brain để lấy danh sách ghi chú."""
    notes = []
    if not settings.VAULT_DIR.exists():
        return notes

    for file_path in settings.VAULT_DIR.rglob("*.md"):
        # Bỏ qua thư mục ẩn hoặc rác
        if any(part.startswith(".") for part in file_path.parts):
            continue
        note_data = parse_markdown_file(file_path)
        if note_data:
            notes.append(note_data)

    notes.sort(key=lambda x: x["updated_at"], reverse=True)
    return notes

def get_note_content(rel_path: str) -> Optional[str]:
    """Đọc nội dung đầy đủ của 1 note."""
    file_path = settings.VAULT_DIR / rel_path
    if file_path.exists() and file_path.is_file():
        return file_path.read_text(encoding="utf-8")
    return None
