import pytest

from C3.c3_knapsack import knapsack_01


def test_finds_optimal_value_and_selected_indices():
    value, selected = knapsack_01([2, 3, 4], [3, 4, 5], 5)
    assert value == 7
    assert selected == [0, 1]


def test_does_not_select_an_item_twice():
    value, selected = knapsack_01([3], [10], 6)
    assert value == 10
    assert selected == [0]


def test_handles_zero_capacity_and_empty_input():
    assert knapsack_01([1, 2], [10, 20], 0) == (0, [])
    assert knapsack_01([], [], 5) == (0, [])


def test_rejects_invalid_inputs():
    with pytest.raises(ValueError):
        knapsack_01([1], [2, 3], 4)
    with pytest.raises(ValueError):
        knapsack_01([-1], [2], 4)
    with pytest.raises(ValueError):
        knapsack_01([1], [2], -1)


def test_reconstructs_without_including_zero_value_or_tied_items():
    assert knapsack_01([1], [0], 1) == (0, [])
    assert knapsack_01([1, 1], [1, 1], 1) == (1, [0])


def test_reconstructs_positive_value_zero_weight_item():
    assert knapsack_01([0], [4], 0) == (4, [0])
