from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.tasks.kanban import get_kanban_tasks, create_kanban_task, update_task_status, delete_kanban_task

router = APIRouter(prefix="/api/kanban", tags=["Kanban"])

class TaskCreatePayload(BaseModel):
    title: str
    description: Optional[str] = ""
    priority: Optional[str] = "medium"
    due_date: Optional[str] = ""

class TaskStatusPayload(BaseModel):
    task_id: str
    status: str # 'todo', 'in_progress', 'done'

@router.get("/tasks")
def list_tasks():
    return {"tasks": get_kanban_tasks()}

@router.post("/task")
def add_task(payload: TaskCreatePayload):
    task = create_kanban_task(payload.title, payload.description or "", payload.priority or "medium", payload.due_date or "")
    return {"status": "success", "task": task}

@router.put("/task")
def change_status(payload: TaskStatusPayload):
    if payload.status not in ["todo", "in_progress", "done"]:
        raise HTTPException(status_code=400, detail="Trạng thái không hợp lệ")
    update_task_status(payload.task_id, payload.status)
    return {"status": "success"}

@router.delete("/task/{task_id}")
def remove_task(task_id: str):
    delete_kanban_task(task_id)
    return {"status": "success"}
