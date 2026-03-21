import csv
import uuid
from collections import Counter

from celery import shared_task

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.job import Job, JobStatus
from app.models.transaction import Transaction
from app.services.validators import validate_headers, validate_row


@shared_task(name="app.workers.tasks.process_job_task", bind=True)
def process_job_task(self, job_id: str) -> None:
    db = SessionLocal()
    try:
        job = db.get(Job, uuid.UUID(job_id))
        if job is None:
            return

        if job.status != JobStatus.running:
            return

        seen_transaction_ids: set[str] = set()
        processed = 0
        counts = Counter()

        with open(job.file_path, "r", encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            validate_headers(reader.fieldnames)
            job.total_records = sum(1 for _ in reader)
            db.add(job)
            db.commit()

        with open(job.file_path, "r", encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            validate_headers(reader.fieldnames)
            batch: list[Transaction] = []

            for row in reader:
                payload, _ = validate_row(row, seen_transaction_ids)
                batch.append(Transaction(job_id=job.id, **payload))

                if len(batch) == settings.batch_size:
                    processed, counts = _commit_batch(db, job, batch, processed, counts)
                    batch = []

            if batch:
                processed, counts = _commit_batch(db, job, batch, processed, counts)

        job.status = JobStatus.completed
        db.add(job)
        db.commit()
    except Exception:
        failed_job = db.get(Job, uuid.UUID(job_id))
        if failed_job is not None:
            failed_job.status = JobStatus.failed
            db.add(failed_job)
            db.commit()
        raise
    finally:
        db.close()


def _commit_batch(db, job: Job, batch: list[Transaction], processed: int, counts: Counter) -> tuple[int, Counter]:
    db.add_all(batch)
    processed += len(batch)
    counts.update(transaction.status.value for transaction in batch)

    job.processed_records = processed
    job.valid_records = counts.get("valid", 0)
    job.invalid_records = counts.get("invalid", 0)
    job.suspicious_records = counts.get("suspicious", 0)
    db.add(job)
    db.commit()
    return processed, counts
