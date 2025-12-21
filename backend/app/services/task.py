from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def get_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Task).filter(Task.user_id == user_id).all()


def get_task_by_id(db: Session, task_id: int, user_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )
    
    return task


def create_task(db: Session, task: TaskCreate, user_id: int):
    db_task = Task(
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        user_id=user_id
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return db_task


def update_task(db: Session, task_id: int, task_update: TaskUpdate, user_id: int):
    db_task = get_task_by_id(db, task_id, user_id)
    
    update_data = task_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    
    return db_task


def delete_task(db: Session, task_id: int, user_id: int):
    db_task = get_task_by_id(db, task_id, user_id)
    
    db.delete(db_task)
    db.commit()
    
    return {"message": "Задача удалена"}


def completed_task_status(db: Session, task_id: int, user_id: int):
    db_task = get_task_by_id(db, task_id, user_id)
    
    db_task.is_completed = not db_task.is_completed
    db.commit()
    db.refresh(db_task)
    
    return db_task