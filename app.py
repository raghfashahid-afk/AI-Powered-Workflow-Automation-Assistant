from fastapi import FastAPI
from database.db import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Workflow Assistant API",
    description="FYP Backend - University of Lahore",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"message": "Workflow Assistant API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok", "database": "connected"}