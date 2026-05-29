from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import json

from database.db import get_db
from services.gmail_service import (
    get_authorization_url,
    exchange_code_for_token,
    fetch_emails
)
from models.email_model import Email
from models import User  # your existing User model

router = APIRouter(prefix="/gmail", tags=["Gmail"])


@router.get("/connect")
def connect_gmail():
    """
    Step 1: Redirect user to Google login page.
    Frontend calls this → user logs into Google.
    """
    auth_url, state = get_authorization_url()
    return {"auth_url": auth_url}


@router.get("/callback")
def gmail_callback(code: str, db: Session = Depends(get_db)):
    """
    Step 2: Google redirects here after user approves access.
    We exchange the code for tokens and store them.
    """
    try:
        token_data = exchange_code_for_token(code)

        # For now: store token for user_id = 1 (hardcoded for testing)
        # Day 4: replace with JWT to get real logged-in user
        user = db.query(User).filter(User.id == 1).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Save token as JSON string in user record
        user.gmail_token = json.dumps(token_data)
        db.commit()

        return {"message": "Gmail connected successfully!"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/emails")
def get_emails(user_id: int = 1, db: Session = Depends(get_db)):
    """
    Fetch emails from Gmail for a user and save to database.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.gmail_token:
        raise HTTPException(status_code=400, detail="Gmail not connected for this user")

    token_data = json.loads(user.gmail_token)

    # Fetch from Gmail API
    emails = fetch_emails(token_data, max_results=10)

    saved = []
    for e in emails:
        # Avoid duplicates
        existing = db.query(Email).filter(Email.gmail_id == e["gmail_id"]).first()
        if not existing:
            new_email = Email(
                user_id=user_id,
                gmail_id=e["gmail_id"],
                sender=e["sender"],
                subject=e["subject"],
                snippet=e["snippet"],
                body=e["body"],
                date=e["date"]
            )
            db.add(new_email)
            saved.append(e)

    db.commit()

    return {
        "fetched": len(emails),
        "new_saved": len(saved),
        "emails": emails
    }


@router.get("/emails/db")
def get_emails_from_db(user_id: int = 1, db: Session = Depends(get_db)):
    """
    Return emails already stored in the database (no Gmail call).
    """
    emails = db.query(Email).filter(Email.user_id == user_id).all()
    return {"count": len(emails), "emails": emails}