from app.services.validators import validate_row
from app.models.transaction import TransactionStatus


def test_suspicious_transaction() -> None:
    seen: set[str] = set()
    payload, error = validate_row(
        {
            "transaction_id": "123e4567-e89b-12d3-a456-426614174000",
            "user_id": "123e4567-e89b-12d3-a456-426614174001",
            "amount": "80000",
            "timestamp": "2024-01-01T10:00:00+00:00",
        },
        seen,
    )

    assert error is None
    assert payload["status"] == TransactionStatus.suspicious
