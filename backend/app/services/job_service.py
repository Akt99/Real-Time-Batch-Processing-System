import csv
import os
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.job import Job, JobStatus
from app.repositories.job_repository import JobRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import PaginatedTransactionsResponse
from app.services.validators import validate_headers
from app.workers.tasks import process_job_task


class JobService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.job_repository = JobRepository(db)
        self.transaction_repository = TransactionRepository(db)

    async def create_job(self, file: UploadFile) -> Job:
        if not file.filename or not file.filename.endswith(".csv"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only CSV files are supported")

        upload_dir = Path(settings.upload_dir)
        upload_dir.mkdir(parents=True, exist_ok=True)

        job_file_name = f"{uuid.uuid4()}-{file.filename}"
        file_path = upload_dir / job_file_name

        content = await file.read()
        file_path.write_bytes(content)

        try:
            with file_path.open("r", encoding="utf-8", newline="") as csv_file:
                reader = csv.DictReader(csv_file)
                validate_headers(reader.fieldnames)
        except ValueError as exc:
            os.remove(file_path)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

        return self.job_repository.create(file_path=str(file_path))

    def start_job(self, job_id: uuid.UUID) -> tuple[Job, str]:
        job = self._get_job_or_404(job_id)
        if job.status != JobStatus.pending:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Job cannot be started from status '{job.status.value}'",
            )

        updated_job = self.job_repository.update(job, status=JobStatus.running)
        async_result = process_job_task.delay(str(updated_job.id))
        return updated_job, async_result.id

    def get_job(self, job_id: uuid.UUID) -> Job:
        return self._get_job_or_404(job_id)

    def get_transactions(
        self,
        job_id: uuid.UUID,
        status_filter: str | None,
        page: int,
        page_size: int,
    ) -> PaginatedTransactionsResponse:
        self._get_job_or_404(job_id)
        items, total = self.transaction_repository.get_paginated(job_id, status_filter, page, page_size)
        return PaginatedTransactionsResponse(page=page, page_size=page_size, total=total, items=items)

    def _get_job_or_404(self, job_id: uuid.UUID) -> Job:
        job = self.job_repository.get(job_id)
        if job is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
        return job
