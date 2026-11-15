from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.tasks.kanban import get_timeline_tasks, toggle_task_done

router = APIRouter(prefix="/api/kanban", tags=["Tasks"])

@router.get("/tasks")
def list_tasks(owner: Optional[str] = Query("all"), status: Optional[str] = Query("all")):
    tasks = get_timeline_tasks(owner_type=owner, filter_status=status)
    # Thống kê
    all_tasks = get_timeline_tasks()
    javis_count = sum(1 for t in all_tasks if t["owner_type"] == "javis")
    mine_count = sum(1 for t in all_tasks if t["owner_type"] == "mine")
    today_count = sum(1 for t in all_tasks if t["status"] == "today")
    upcoming_count = sum(1 for t in all_tasks if t["status"] == "upcoming")
    done_count = sum(1 for t in all_tasks if t["status"] == "done")
    
    return {
        "tasks": tasks,
        "counts": {
            "all": len(all_tasks),
            "javis": javis_count,
            "mine": mine_count,
            "today": today_count,
            "upcoming": upcoming_count,
            "done": done_count,
            "recurring": 9
        }
    }

class ToggleDonePayload(BaseModel):
    task_id: str

@router.post("/toggle")
def toggle_done(payload: ToggleDonePayload):
    toggle_task_done(payload.task_id)
    return {"status": "success"}
