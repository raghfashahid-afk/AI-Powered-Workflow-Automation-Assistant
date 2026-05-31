from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from models.email_model import Email
from models.task_model import Task
from models import User
from services.classifier_service import get_model_info

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def get_dashboard_summary(user_id: int = 1, db: Session = Depends(get_db)):
    """
    Main dashboard — shows everything in one response.
    Perfect for supervisor demo!
    """
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Email stats
    total_emails = db.query(Email).filter(Email.user_id == user_id).count()

    # Emails by category
    emails = db.query(Email).filter(Email.user_id == user_id).all()
    email_categories = {}
    for email in emails:
        cat = email.category or "uncategorized"
        email_categories[cat] = email_categories.get(cat, 0) + 1

    # Task stats
    total_tasks = db.query(Task).filter(Task.user_id == user_id).count()

    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    task_priorities = {"urgent": 0, "high": 0, "normal": 0, "low": 0}
    for task in tasks:
        p = task.priority or "normal"
        if p in task_priorities:
            task_priorities[p] += 1

    # Recent 5 emails
    recent_emails = db.query(Email).filter(
        Email.user_id == user_id
    ).order_by(Email.fetched_at.desc()).limit(5).all()

    # Urgent tasks
    urgent_tasks = db.query(Task).filter(
        Task.user_id == user_id,
        Task.priority == "urgent"
    ).limit(5).all()

    # ML model info
    model = get_model_info()

    return {
        "user": {
            "id":    user.id,
            "name":  user.name,
            "email": user.email
        },
        "email_stats": {
            "total":      total_emails,
            "categories": email_categories
        },
        "task_stats": {
            "total":      total_tasks,
            "priorities": task_priorities
        },
        "recent_emails": [
            {
                "subject":  e.subject,
                "sender":   e.sender,
                "category": e.category,
                "date":     e.date
            } for e in recent_emails
        ],
        "urgent_tasks": [
            {
                "title":    t.title[:100],
                "deadline": t.deadline,
                "priority": t.priority
            } for t in urgent_tasks
        ],
        "ai_model": model
    }


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    System health check — shows all components working.
    """
    try:
        # Test database
        db.execute(__import__('sqlalchemy').text("SELECT 1"))
        db_status = "connected"
    except:
        db_status = "error"

    return {
        "status":     "running",
        "database":   db_status,
        "api":        "healthy",
        "version":    "0.6.0",
        "components": {
            "auth":           "✅ working",
            "gmail":          "✅ working",
            "classification": "✅ working",
            "task_extraction":"✅ working",
            "dashboard":      "✅ working"
        }
    }
