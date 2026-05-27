from fastapi import FastAPI
from database.db import engine, Base
from routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Workflow Assistant API",
    description="FYP Backend - University of Lahore",
    version="0.2.0"
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Workflow Assistant API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok", "database": "connected"}