import uuid

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.models.transaction import Transaction


class TransactionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def bulk_create(self, transactions: list[Transaction]) -> None:
        self.db.add_all(transactions)
        self.db.commit()

    def get_paginated(
        self,
        job_id: uuid.UUID,
        status: str | None,
        page: int,
        page_size: int,
    ) -> tuple[list[Transaction], int]:
        query: Select[tuple[Transaction]] = select(Transaction).where(Transaction.job_id == job_id)
        count_query = select(func.count(Transaction.id)).where(Transaction.job_id == job_id)

        if status:
            query = query.where(Transaction.status == status)
            count_query = count_query.where(Transaction.status == status)

        query = query.order_by(Transaction.id).offset((page - 1) * page_size).limit(page_size)
        items = list(self.db.scalars(query).all())
        total = self.db.scalar(count_query) or 0
        return items, total
