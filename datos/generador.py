import random


def _validate_size(n: int) -> None:
    if n < 0:
        raise ValueError("n cannot be negative")


def generate_keys(n: int, seed: int = 42) -> list[str]:
    _validate_size(n)
    rng = random.Random(seed)
    return [f"account-{rng.randrange(max(1, n // 2 + 1)):04d}" for _ in range(n)]


def generate_transactions(n: int, seed: int = 42) -> list[dict]:
    _validate_size(n)
    rng = random.Random(seed)
    return [
        {
            "transaction_id": f"tx-{index:06d}",
            "account_id": f"account-{rng.randrange(max(1, n // 2 + 1)):04d}",
            "amount": round(rng.uniform(1.0, 5000.0), 2),
            "is_anomalous": rng.random() < 0.05,
        }
        for index in range(n)
    ]
