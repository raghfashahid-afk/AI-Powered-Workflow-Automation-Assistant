from fastapi import FastAPI
from database.db import engine, Base

import models
import models.email_model
import models.task_model  

from routes import router as auth_router
from routes.gmail_routes import router as gmail_router
from routes.classify_routes import router as classify_router
from routes.task_routes import router as task_router 
from routes.dashboard_routes import router as dashboard_router
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Workflow Assistant API",
    description="FYP Backend - University of Lahore",
    version="0.4.0"
)

app.include_router(auth_router,     prefix="/auth")
app.include_router(gmail_router,    prefix="/auth")
app.include_router(classify_router, prefix="/emails")
app.include_router(task_router,     prefix="/emails")   
app.include_router(dashboard_router,  prefix="/api") 