"""A small perceptron learner and a realizable-PAC VC sample bound."""

from __future__ import annotations

import math
import random
from typing import Sequence


def pac_sample_bound(feature_dimension: int, epsilon: float, delta: float) -> int:
    """Sufficient realizable-PAC sample count using VC dimension d+1."""
    if feature_dimension < 1 or not 0 < epsilon < 1 or not 0 < delta < 1:
        raise ValueError("d >= 1 and epsilon, delta in (0, 1) are required")
    vc_dimension = feature_dimension + 1
    bound = (4 * math.log(2 / delta) + 8 * vc_dimension * math.log(13 / epsilon)) / epsilon
    return math.ceil(bound)


def generate_linear_data(count: int, seed: int = 42, dimension: int = 2) -> tuple[list[list[float]], list[int]]:
    if count < 0 or dimension < 1:
        raise ValueError("count must be nonnegative and dimension positive")
    rng = random.Random(seed)
    points = [[rng.uniform(-1, 1) for _ in range(dimension)] for _ in range(count)]
    # Fixed unit normal and a margin create a realizable distribution.
    weights = [1.0 / math.sqrt(dimension)] * dimension
    labels = [1 if sum(w * x for w, x in zip(weights, point)) >= 0 else -1 for point in points]
    return points, labels


class Perceptron:
    def __init__(self, dimension: int):
        self.weights = [0.0] * dimension
        self.bias = 0.0

    def predict(self, point: Sequence[float]) -> int:
        return 1 if sum(w * x for w, x in zip(self.weights, point)) + self.bias >= 0 else -1

    def fit(self, points: Sequence[Sequence[float]], labels: Sequence[int], max_epochs: int = 1000) -> None:
        if len(points) != len(labels):
            raise ValueError("points and labels must have the same length")
        if not points:
            raise ValueError("training set cannot be empty")
        if any(label not in (-1, 1) for label in labels):
            raise ValueError("labels must be -1 or 1")
        self.weights = [0.0] * len(points[0])
        self.bias = 0.0
        for _ in range(max_epochs):
            mistakes = 0
            for point, label in zip(points, labels):
                if label * (sum(w * x for w, x in zip(self.weights, point)) + self.bias) <= 0:
                    self.weights = [w + label * x for w, x in zip(self.weights, point)]
                    self.bias += label
                    mistakes += 1
            if mistakes == 0:
                return


def error_rate(model: Perceptron, points: Sequence[Sequence[float]], labels: Sequence[int]) -> float:
    if len(points) != len(labels) or not labels:
        raise ValueError("nonempty points and labels of equal length are required")
    return sum(model.predict(point) != label for point, label in zip(points, labels)) / len(labels)
