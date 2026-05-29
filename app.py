from fastapi import FastAPI
from database.db import engine, Base

import models
import models.email_model

from routes import router as auth_router
from routes.gmail_routes import router as gmail_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Workflow Assistant API",
    description="FYP Backend - University of Lahore",
    version="0.3.0"
)

app.include_router(auth_router, prefix="/auth")
app.include_router(gmail_router, prefix="/auth")