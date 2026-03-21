from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.transaction import TransactionStatus


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    transaction_id: str
    user_id: str
    amount: Decimal | None
    timestamp: datetime | None
    status: TransactionStatus
    error_message: str | None


class PaginatedTransactionsResponse(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[TransactionResponse]
