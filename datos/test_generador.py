import pytest

from datos.generador import generate_keys, generate_transactions


def test_generators_are_reproducible_and_have_requested_size():
    assert generate_keys(5, seed=10) == generate_keys(5, seed=10)
    assert generate_transactions(5, seed=10) == generate_transactions(5, seed=10)
    assert len(generate_keys(5)) == 5
    assert len(generate_transactions(5)) == 5


def test_generators_reject_negative_size():
    with pytest.raises(ValueError):
        generate_keys(-1)
    with pytest.raises(ValueError):
        generate_transactions(-1)
