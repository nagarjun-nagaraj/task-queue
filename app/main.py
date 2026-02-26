from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import jobs

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Queue API")
app.include_router(jobs.router)