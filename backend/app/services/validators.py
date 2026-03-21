from collections.abc import Iterable
from datetime import datetime
from decimal import Decimal, InvalidOperation
from uuid import UUID

from app.models.transaction import TransactionStatus

REQUIRED_FIELDS = {"transaction_id", "user_id", "amount", "timestamp"}


def _is_guid(value: str) -> bool:
    try:
        UUID(value)
        return True
    except (ValueError, TypeError):
        return False


def validate_headers(headers: Iterable[str] | None) -> None:
    if headers is None or set(headers) != REQUIRED_FIELDS:
        raise ValueError(
            "CSV headers must exactly match: transaction_id,user_id,amount,timestamp"
        )


def validate_row(row: dict[str, str], seen_transaction_ids: set[str]) -> tuple[dict, str | None]:
    errors: list[str] = []
    transaction_id = (row.get("transaction_id") or "").strip()
    user_id = (row.get("user_id") or "").strip()
    amount_raw = (row.get("amount") or "").strip()
    timestamp_raw = (row.get("timestamp") or "").strip()

    if not transaction_id:
        errors.append("transaction_id is required")
    elif transaction_id in seen_transaction_ids:
        errors.append("transaction_id must be unique within job")
    elif not _is_guid(transaction_id):
        errors.append("transaction_id must be a GUID")

    if not user_id:
        errors.append("user_id is required")
    elif not _is_guid(user_id):
        errors.append("user_id must be a GUID")

    amount = None
    if not amount_raw:
        errors.append("amount is required")
    else:
        try:
            amount = Decimal(amount_raw)
        except (InvalidOperation, ValueError):
            errors.append("amount must be numeric")

    parsed_timestamp = None
    if not timestamp_raw:
        errors.append("timestamp is required")
    else:
        try:
            parsed_timestamp = datetime.fromisoformat(timestamp_raw.replace("Z", "+00:00"))
        except ValueError:
            errors.append("timestamp must be ISO format")

    status = TransactionStatus.invalid
    error_message = "; ".join(errors) if errors else None

    if not errors:
        seen_transaction_ids.add(transaction_id)
        if amount is not None and (amount < 0 or amount > 50000):
            status = TransactionStatus.suspicious
        else:
            status = TransactionStatus.valid

    return {
        "transaction_id": transaction_id,
        "user_id": user_id,
        "amount": amount,
        "timestamp": parsed_timestamp,
        "status": status,
        "error_message": error_message,
    }, error_message
