import uuid

from sqlalchemy.orm import Session

from app.models.job import Job, JobStatus


class JobRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, file_path: str) -> Job:
        job = Job(file_path=file_path, status=JobStatus.pending)
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def get(self, job_id: uuid.UUID) -> Job | None:
        return self.db.get(Job, job_id)

    def update(self, job: Job, **kwargs) -> Job:
        for key, value in kwargs.items():
            setattr(job, key, value)
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job
