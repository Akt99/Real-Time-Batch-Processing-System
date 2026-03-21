import uuid
from typing import Literal

from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.job import JobCreateResponse, JobStatusResponse, StartJobResponse
from app.schemas.transaction import PaginatedTransactionsResponse
from app.services.job_service import JobService


router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> JobService:
    return JobService(db)


@router.post("", response_model=JobCreateResponse)
async def create_job(
    file: UploadFile = File(...),
    service: JobService = Depends(get_service),
) -> JobCreateResponse:
    job = await service.create_job(file)
    return JobCreateResponse(job_id=job.id, status=job.status)


@router.post("/{job_id}/start", response_model=StartJobResponse)
def start_job(job_id: uuid.UUID, service: JobService = Depends(get_service)) -> StartJobResponse:
    job, task_id = service.start_job(job_id)
    return StartJobResponse(job_id=job.id, status=job.status.value, message=f"Processing started with task {task_id}")


@router.get("/{job_id}", response_model=JobStatusResponse)
def get_job(job_id: uuid.UUID, service: JobService = Depends(get_service)) -> JobStatusResponse:
    return JobStatusResponse.model_validate(service.get_job(job_id))


@router.get("/{job_id}/transactions", response_model=PaginatedTransactionsResponse)
def get_transactions(
    job_id: uuid.UUID,
    status: Literal["valid", "invalid", "suspicious"] | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    service: JobService = Depends(get_service),
) -> PaginatedTransactionsResponse:
    return service.get_transactions(job_id, status, page, page_size)
