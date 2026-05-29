from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database.db import get_db
from models.email_model import Email
from services.classifier_service import (
    classify_email,
    classify_bulk,
    get_model_info,
    train_model
)

router = APIRouter(prefix="/classify", tags=["Classification"])


class EmailInput(BaseModel):
    subject: str
    body:    str
    sender:  str = ""


@router.get("/model-info")
def model_info():
    """
    Show ML model details — great for supervisor demo!
    """
    return get_model_info()


@router.post("/single")
def classify_single(email: EmailInput):
    """
    Classify a single email instantly.
    """
    category = classify_email(
        subject=email.subject,
        body=email.body,
        sender=email.sender
    )
    return {
        "subject":  email.subject,
        "category": category
    }


@router.post("/all")
def classify_all_emails(user_id: int = 1, db: Session = Depends(get_db)):
    """
    Classify all stored emails for a user and update database.
    """
    emails = db.query(Email).filter(Email.user_id == user_id).all()

    if not emails:
        raise HTTPException(status_code=404, detail="No emails found")

    updated = []
    for email in emails:
        category = classify_email(
            subject=email.subject or "",
            body=email.body or "",
            sender=email.sender or ""
        )
        email.category = category
        updated.append({
            "gmail_id": email.gmail_id,
            "subject":  email.subject,
            "category": category
        })

    db.commit()

    return {
        "message": f"Classified {len(updated)} emails successfully",
        "results": updated
    }


@router.get("/summary")
def get_classification_summary(user_id: int = 1, db: Session = Depends(get_db)):
    """
    Get count of emails per category.
    """
    emails = db.query(Email).filter(Email.user_id == user_id).all()

    summary = {}
    for email in emails:
        cat = email.category or "uncategorized"
        summary[cat] = summary.get(cat, 0) + 1

    return {
        "total":   len(emails),
        "summary": summary
    }


@router.get("/category/{category}")
def get_emails_by_category(
    category: str,
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    """
    Get all emails of a specific category.
    """
    emails = db.query(Email).filter(
        Email.user_id  == user_id,
        Email.category == category
    ).all()

    return {
        "category": category,
        "count":    len(emails),
        "emails":   emails
    }


@router.post("/retrain")
def retrain_model():
    """
    Retrain the ML model from scratch.
    """
    train_model()
    return {"message": "Model retrained successfully!"}