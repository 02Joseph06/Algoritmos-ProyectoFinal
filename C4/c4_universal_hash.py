"""Separate-chaining tables for fixed and universal hashing experiments."""

from __future__ import annotations

import hashlib
import random
from typing import Iterable

_PRIME = 2**61 - 1


def stable_integer(key: str) -> int:
    """Map UTF-8 keys deterministically into the universal-hash domain."""
    digest = hashlib.blake2b(key.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "big") % _PRIME


class ChainingHashTable:
    """A chaining table that exposes the number of key comparisons."""

    def __init__(self, capacity: int, *, seed: int | None = None):
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._buckets: list[list[str]] = [[] for _ in range(capacity)]
        self._comparisons = 0
        self._universal = seed is not None
        if self._universal:
            rng = random.Random(seed)
            self._a = rng.randrange(1, _PRIME)
            self._b = rng.randrange(0, _PRIME)
        else:
            self._a = self._b = 0

    def _index(self, key: str) -> int:
        if self._universal:
            return ((self._a * stable_integer(key) + self._b) % _PRIME) % self.capacity
        return stable_integer(key) % self.capacity

    @property
    def comparisons(self) -> int:
        return self._comparisons

    def reset_comparisons(self) -> None:
        self._comparisons = 0

    def put(self, key: str) -> None:
        bucket = self._buckets[self._index(key)]
        for current in bucket:
            self._comparisons += 1
            if current == key:
                return
        bucket.append(key)

    def contains(self, key: str) -> bool:
        for current in self._buckets[self._index(key)]:
            self._comparisons += 1
            if current == key:
                return True
        return False


def colliding_keys(capacity: int, count: int, *, bucket: int = 0) -> list[str]:
    """Find distinct keys colliding in the fixed (non-random) hash function."""
    if capacity < 1 or count < 0 or not 0 <= bucket < capacity:
        raise ValueError("invalid capacity, count, or bucket")
    found: list[str] = []
    candidate = 0
    while len(found) < count:
        key = f"adversarial-account-{candidate}"
        if stable_integer(key) % capacity == bucket:
            found.append(key)
        candidate += 1
    return found


def run_collision_comparison(keys: Iterable[str], capacity: int, seed: int = 42) -> dict[str, int]:
    keys = list(keys)
    fixed = ChainingHashTable(capacity)
    universal = ChainingHashTable(capacity, seed=seed)
    for key in keys:
        fixed.put(key)
        universal.put(key)
    fixed.reset_comparisons()
    universal.reset_comparisons()
    for key in keys:
        fixed.contains(key)
        universal.contains(key)
    return {
        "n": len(keys),
        "comparaciones_hash_fijo": fixed.comparisons,
        "comparaciones_universal": universal.comparisons,
    }
