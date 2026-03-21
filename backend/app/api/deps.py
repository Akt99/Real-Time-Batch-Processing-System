from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.job_service import JobService


def get_job_service(db: Session) -> JobService:
    return JobService(db)
