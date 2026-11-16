"""Linear hashing on DiscoSimulado with an in-memory Bloom filter."""

from __future__ import annotations

import hashlib
import json
import math

from DiscoSimulado.disco_simulado import DiscoSimulado


def _digest(data: bytes, salt: int) -> int:
    return int.from_bytes(hashlib.blake2b(data, digest_size=8, person=salt.to_bytes(8, "little")).digest(), "big")


class BloomFilter:
    def __init__(self, expected_items: int, false_positive_rate: float = 0.01):
        if expected_items < 1 or not 0 < false_positive_rate < 1:
            raise ValueError("expected_items must be positive and rate must be in (0, 1)")
        self.bit_count = max(8, math.ceil(-expected_items * math.log(false_positive_rate) / math.log(2) ** 2))
        self.hash_count = max(1, round(self.bit_count / expected_items * math.log(2)))
        self._bits = bytearray((self.bit_count + 7) // 8)

    def _positions(self, key: str):
        raw = key.encode("utf-8")
        first, second = _digest(raw, 1), _digest(raw, 2) | 1
        for index in range(self.hash_count):
            yield (first + index * second) % self.bit_count

    def add(self, key: str) -> None:
        for position in self._positions(key):
            self._bits[position // 8] |= 1 << (position % 8)

    def might_contain(self, key: str) -> bool:
        return all(self._bits[position // 8] & (1 << (position % 8)) for position in self._positions(key))


class DiskLinearHashBlacklist:
    """Linear hash with primary bucket IDs and disk-resident overflow chains.

    M records are reserved for the Bloom filter / working set; every bucket
    access itself goes through the block API of DiscoSimulado.
    """

    def __init__(self, disk: DiscoSimulado, expected_items: int, *, bloom_rate: float = 0.01, initial_buckets: int = 2):
        if initial_buckets < 2 or initial_buckets & (initial_buckets - 1):
            raise ValueError("initial_buckets must be a power of two >= 2")
        if disk.num_blocks <= initial_buckets:
            raise ValueError("disk needs bucket blocks and overflow space")
        self.disk = disk
        self.bloom = BloomFilter(max(1, expected_items), bloom_rate)
        self._base = initial_buckets
        self._level = 0
        self._split = 0
        self._bucket_count = initial_buckets
        self._overflow_next = disk.num_blocks - 1
        self._record_capacity = max(1, disk.block_size // 64)
        self._items = 0
        for block_id in range(initial_buckets):
            self._write_block(block_id, [], None)

    @property
    def bucket_count(self) -> int:
        return self._bucket_count

    def _bucket(self, key: str) -> int:
        value = _digest(key.encode("utf-8"), 3)
        index = value % (self._base << self._level)
        if index < self._split:
            index = value % (self._base << (self._level + 1))
        return index

    def _read_block(self, block_id: int) -> dict:
        return json.loads(self.disk.read_block(block_id).split(b"\0", 1)[0] or b"{}")

    def _write_block(self, block_id: int, keys: list[str], next_id: int | None) -> None:
        payload = json.dumps({"keys": keys, "next": next_id}, separators=(",", ":")).encode()
        self.disk.write_block(block_id, payload)

    def _chain(self, bucket: int):
        block_id: int | None = bucket
        while block_id is not None:
            block = self._read_block(block_id)
            yield block_id, block
            block_id = block["next"]

    def _allocate_overflow(self) -> int:
        if self._overflow_next <= self._bucket_count:
            raise RuntimeError("disk overflow region exhausted")
        block_id = self._overflow_next
        self._overflow_next -= 1
        return block_id

    def add(self, key: str) -> None:
        bucket = self._bucket(key)
        last_id = bucket
        last_block = None
        for block_id, block in self._chain(bucket):
            if key in block["keys"]:
                self.bloom.add(key)
                return
            if len(block["keys"]) < self._record_capacity:
                block["keys"].append(key)
                self._write_block(block_id, block["keys"], block["next"])
                self._items += 1
                self.bloom.add(key)
                self._maybe_split()
                return
            last_id, last_block = block_id, block
        new_id = self._allocate_overflow()
        self._write_block(new_id, [key], None)
        self._write_block(last_id, last_block["keys"], new_id)
        self._items += 1
        self.bloom.add(key)
        self._maybe_split()

    def _maybe_split(self) -> None:
        if self._items / (self._bucket_count * self._record_capacity) > 0.75:
            self._split_bucket()

    def _split_bucket(self) -> None:
        old_bucket = self._split
        new_bucket = self._bucket_count
        all_keys = [key for _, block in self._chain(old_bucket) for key in block["keys"]]
        self._bucket_count += 1
        for block_id, block in self._chain(old_bucket):
            if block_id != old_bucket:
                self._write_block(block_id, [], None)
        self._write_block(old_bucket, [], None)
        self._write_block(new_bucket, [], None)
        self._split += 1
        if self._split == (self._base << self._level):
            self._level += 1
            self._split = 0
        for key in all_keys:
            destination = self._bucket(key)
            target_id = destination
            target = None
            last_id, last_block = destination, None
            for block_id, block in self._chain(destination):
                last_id, last_block = block_id, block
                if len(block["keys"]) < self._record_capacity:
                    target_id, target = block_id, block
                    break
            if target is None:
                target_id, target = last_id, last_block
            if len(target["keys"]) >= self._record_capacity:
                overflow = self._allocate_overflow()
                self._write_block(overflow, [key], None)
                self._write_block(target_id, target["keys"], overflow)
            else:
                self._write_block(target_id, target["keys"] + [key], target["next"])

    def contains(self, key: str) -> bool:
        if not self.bloom.might_contain(key):
            return False
        for _, block in self._chain(self._bucket(key)):
            if key in block["keys"]:
                return True
        return False

    def estimated_bloom_false_positive_rate(self) -> float:
        return (1 - math.exp(-self.bloom.hash_count * self._items / self.bloom.bit_count)) ** self.bloom.hash_count

    def predicted_query_io(self, true_positive_queries: int, negative_queries: int) -> float:
        """Expected lookup I/O: true hits plus Bloom false positives times one bucket block."""
        fp = self.estimated_bloom_false_positive_rate()
        return true_positive_queries + negative_queries * fp
