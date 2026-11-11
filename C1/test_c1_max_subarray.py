import pytest

from C1.c1_max_subarray import max_subarray_divide_conquer


def brute_force(values):
    best = None
    for start in range(len(values)):
        total = 0
        for end in range(start, len(values)):
            total += values[end]
            candidate = (total, start, end)
            if best is None or candidate[0] > best[0]:
                best = candidate
    return best


def test_finds_crossing_maximum_subarray():
    assert max_subarray_divide_conquer([2, -5, 4, 6, -3, 1]) == (10, 2, 3)


def test_handles_all_negative_values():
    assert max_subarray_divide_conquer([-8, -3, -5]) == (-3, 1, 1)


def test_handles_single_value():
    assert max_subarray_divide_conquer([7]) == (7, 0, 0)


def test_rejects_empty_input():
    with pytest.raises(ValueError, match="empty"):
        max_subarray_divide_conquer([])


def test_matches_brute_force_for_deterministic_arrays():
    cases = ([3, -1, 2, -8, 4], [-2, 5, -1, 2, -6, 3], [0, -1, 0, 2])
    for values in cases:
        assert max_subarray_divide_conquer(values) == brute_force(values)
