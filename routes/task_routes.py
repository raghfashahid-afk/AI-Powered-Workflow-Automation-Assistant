from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from models.email_model import Email
from models.task_model import Task
from services.task_extractor import extract_tasks_from_email

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/extract")
def extract_tasks(user_id: int = 1, db: Session = Depends(get_db)):
    """
    Extract tasks from all stored emails and save to database.
    """
    emails = db.query(Email).filter(Email.user_id == user_id).all()

    if not emails:
        raise HTTPException(status_code=404, detail="No emails found")

    all_tasks = []

    for email in emails:
        tasks = extract_tasks_from_email(
            email_text=email.body or "",
            email_subject=email.subject or ""
        )

        for task in tasks:
            # Avoid duplicates
            existing = db.query(Task).filter(
                Task.title   == task["title"],
                Task.user_id == user_id
            ).first()

            if not existing:
                new_task = Task(
                    user_id=user_id,
                    email_id=email.id,
                    title=task["title"],
                    deadline=task["deadline"],
                    priority=task["priority"],
                    status="pending"
                )
                db.add(new_task)
                all_tasks.append(task)

    db.commit()

    return {
        "message":        f"Extracted {len(all_tasks)} tasks",
        "tasks_extracted": len(all_tasks),
        "tasks":           all_tasks
    }


@router.get("/all")
def get_all_tasks(user_id: int = 1, db: Session = Depends(get_db)):
    """
    Get all extracted tasks for a user.
    """
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return {
        "total": len(tasks),
        "tasks": tasks
    }


@router.get("/priority/{priority}")
def get_tasks_by_priority(
    priority: str,
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    """
    Get tasks filtered by priority: urgent, high, normal, low
    """
    tasks = db.query(Task).filter(
        Task.user_id == user_id,
        Task.priority == priority
    ).all()

    return {
        "priority": priority,
        "count":    len(tasks),
        "tasks":    tasks
    }


@router.get("/summary")
def get_task_summary(user_id: int = 1, db: Session = Depends(get_db)):
    """
    Summary of tasks by priority and status.
    """
    tasks = db.query(Task).filter(Task.user_id == user_id).all()

    summary = {"urgent": 0, "high": 0, "normal": 0, "low": 0}
    for task in tasks:
        p = task.priority or "normal"
        if p in summary:
            summary[p] += 1

    return {
        "total":   len(tasks),
        "summary": summary
    }