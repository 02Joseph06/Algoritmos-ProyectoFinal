from typing import Sequence


def max_subarray_divide_conquer(values: Sequence[int]) -> tuple[int, int, int]:
    """Return the maximum contiguous sum and its inclusive bounds."""
    if not values:
        raise ValueError("values cannot be empty")

    def solve(left: int, right: int) -> tuple[int, int, int]:
        if left == right:
            return values[left], left, right

        middle = (left + right) // 2
        left_result = solve(left, middle)
        right_result = solve(middle + 1, right)

        left_sum = values[middle]
        running = 0
        best_left = middle
        for index in range(middle, left - 1, -1):
            running += values[index]
            if running > left_sum:
                left_sum = running
                best_left = index

        right_sum = values[middle + 1]
        running = 0
        best_right = middle + 1
        for index in range(middle + 1, right + 1):
            running += values[index]
            if running > right_sum:
                right_sum = running
                best_right = index

        crossing = (left_sum + right_sum, best_left, best_right)
        best = left_result
        for candidate in (right_result, crossing):
            if candidate[0] > best[0] or (
                candidate[0] == best[0]
                and (candidate[1], candidate[2]) < (best[1], best[2])
            ):
                best = candidate
        return best

    return solve(0, len(values) - 1)
