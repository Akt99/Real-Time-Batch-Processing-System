import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, computed_field

from app.models.job import JobStatus


class JobCreateResponse(BaseModel):
    job_id: uuid.UUID
    status: JobStatus


class JobStatusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: JobStatus
    total_records: int
    processed_records: int
    valid_records: int
    invalid_records: int
    suspicious_records: int
    created_at: datetime

    @computed_field
    @property
    def progress_percent(self) -> float:
        if self.total_records == 0:
            return 0.0
        return round((self.processed_records / self.total_records) * 100, 2)


class StartJobResponse(BaseModel):
    job_id: uuid.UUID
    status: str
    message: str
