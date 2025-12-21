from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskResponse, TaskStatusUpdate, TaskUpdate
from app.core.database import get_db
from app.models.user import User
from app.services.user import get_current_user
from app.services.task import get_tasks, get_task_by_id, create_task, update_task, delete_task, completed_task_status
from app.models.task import Task
from typing import List


task_router = APIRouter(prefix="/tasks")


@task_router.get("/", response_model=List[TaskResponse])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_tasks(db, current_user.id, skip, limit)


@task_router.get("/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_task_by_id(db, task_id, current_user.id)


@task_router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return create_task(db, task, current_user.id)


@task_router.put("/{task_id}", response_model=TaskResponse)
def update_existing_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return update_task(db, task_id, task_update, current_user.id)


@task_router.delete("/{task_id}")
def delete_existing_task(task_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return delete_task(db, task_id, current_user.id)


@task_router.patch("/{task_id}/completed", response_model=TaskResponse)
def completed_task(task_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return completed_task_status(db, task_id, current_user.id)