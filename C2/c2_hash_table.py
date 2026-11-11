from typing import Any


_EMPTY = object()
_DELETED = object()


class ResizableHashTable:
    """Open-addressing hash table with linear probing and resizing."""

    def __init__(self, initial_capacity: int = 8, max_load_factor: float = 0.7):
        if initial_capacity < 1:
            raise ValueError("initial_capacity must be positive")
        if not 0 < max_load_factor < 1:
            raise ValueError("max_load_factor must be between 0 and 1")
        self._slots = [_EMPTY] * initial_capacity
        self._size = 0
        self._max_load_factor = max_load_factor

    @property
    def capacity(self) -> int:
        return len(self._slots)

    def __len__(self) -> int:
        return self._size

    def _find_slot(self, key: Any) -> tuple[int, bool]:
        hash(key)
        start = hash(key) % self.capacity
        first_deleted = None
        for offset in range(self.capacity):
            index = (start + offset) % self.capacity
            slot = self._slots[index]
            if slot is _EMPTY:
                return (first_deleted if first_deleted is not None else index, False)
            if slot is _DELETED:
                if first_deleted is None:
                    first_deleted = index
            elif slot[0] == key:
                return index, True
        if first_deleted is not None:
            return first_deleted, False
        raise RuntimeError("hash table has no available slot")

    def _resize(self) -> None:
        old_slots = self._slots
        self._slots = [_EMPTY] * (len(old_slots) * 2)
        old_size = self._size
        self._size = 0
        for slot in old_slots:
            if slot is not _EMPTY and slot is not _DELETED:
                index, _ = self._find_slot(slot[0])
                self._slots[index] = slot
                self._size += 1
        assert self._size == old_size

    def put(self, key: Any, value: Any) -> None:
        index, found = self._find_slot(key)
        if found:
            self._slots[index] = (key, value)
            return
        if (self._size + 1) / self.capacity > self._max_load_factor:
            self._resize()
            index, _ = self._find_slot(key)
        self._slots[index] = (key, value)
        self._size += 1

    def get(self, key: Any, default: Any = None) -> Any:
        index, found = self._find_slot(key)
        return self._slots[index][1] if found else default

    def contains(self, key: Any) -> bool:
        return self._find_slot(key)[1]

    def remove(self, key: Any) -> Any:
        index, found = self._find_slot(key)
        if not found:
            raise KeyError(key)
        value = self._slots[index][1]
        self._slots[index] = _DELETED
        self._size -= 1
        return value
