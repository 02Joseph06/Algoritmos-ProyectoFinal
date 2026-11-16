from typing import Sequence


def knapsack_01(
    weights: Sequence[int], values: Sequence[int], capacity: int
) -> tuple[int, list[int]]:
    """Return the best value and indices selected for a 0/1 knapsack."""
    if len(weights) != len(values):
        raise ValueError("weights and values must have the same length")
    if capacity < 0:
        raise ValueError("capacity cannot be negative")
    if any(weight < 0 for weight in weights):
        raise ValueError("weights cannot contain negative values")

    item_count = len(weights)
    table = [[0] * (capacity + 1) for _ in range(item_count + 1)]

    for item in range(1, item_count + 1):
        weight = weights[item - 1]
        value = values[item - 1]
        for remaining in range(capacity + 1):
            without_item = table[item - 1][remaining]
            with_item = without_item
            if weight <= remaining:
                with_item = value + table[item - 1][remaining - weight]
            table[item][remaining] = max(without_item, with_item)

    selected: list[int] = []
    remaining = capacity
    for item in range(item_count, 0, -1):
        # Recalcular la decisión evita inferir inclusión solo por una
        # diferencia entre filas, especialmente con ceros o empates.
        without_item = table[item - 1][remaining]
        weight = weights[item - 1]
        value = values[item - 1]
        with_item = (
            value + table[item - 1][remaining - weight]
            if weight <= remaining
            else without_item
        )
        # La tabla conserva la solución sin el elemento cuando hay empate.
        if weight <= remaining and with_item > without_item:
            index = item - 1
            selected.append(index)
            remaining -= weights[index]
    selected.reverse()
    return table[item_count][capacity], selected
