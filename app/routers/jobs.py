from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.tasks import send_email, process_data
from app.celery_app import celery

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.JobResponse)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    if job.job_type == "send_email":
        task = send_email.delay(
            recipient=job.payload.get("recipient"),
            subject=job.payload.get("subject")
        )
    elif job.job_type == "process_data":
        task = process_data.delay(data=job.payload)
    else:
        raise HTTPException(status_code=400, detail="Unknown job type")

    db_job = models.Job(
        task_id=task.id,
        job_type=job.job_type,
        status="pending"
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/{task_id}", response_model=schemas.JobResponse)
def get_job(task_id: str, db: Session = Depends(get_db)):
    db_job = db.query(models.Job).filter(models.Job.task_id == task_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")

    task_result = celery.AsyncResult(task_id)
    db_job.status = task_result.state.lower()
    if task_result.ready():
        db_job.result = str(task_result.result)
    db.commit()

    return db_job