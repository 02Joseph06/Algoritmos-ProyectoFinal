import pytest

from C2.c2_hash_table import ResizableHashTable


class CollisionKey:
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return 1

    def __eq__(self, other):
        return isinstance(other, CollisionKey) and self.name == other.name


def test_stores_and_retrieves_colliding_keys():
    table = ResizableHashTable(initial_capacity=4)
    keys = [CollisionKey(str(i)) for i in range(3)]
    for key in keys:
        table.put(key, key.name)
    assert [table.get(key) for key in keys] == ["0", "1", "2"]
    assert len(table) == 3


def test_updating_key_does_not_increase_length():
    table = ResizableHashTable(initial_capacity=4)
    table.put("account", 1)
    table.put("account", 2)
    assert table.get("account") == 2
    assert len(table) == 1


def test_missing_key_returns_default_and_contains_is_false():
    table = ResizableHashTable()
    assert table.get("missing", "fallback") == "fallback"
    assert not table.contains("missing")


def test_remove_uses_tombstone_without_hiding_later_collision():
    table = ResizableHashTable(initial_capacity=8)
    first, second = CollisionKey("first"), CollisionKey("second")
    table.put(first, 1)
    table.put(second, 2)
    assert table.remove(first) == 1
    assert not table.contains(first)
    assert table.get(second) == 2
    assert len(table) == 1


def test_table_doubles_capacity_and_keeps_entries():
    table = ResizableHashTable(initial_capacity=4, max_load_factor=0.6)
    for index in range(8):
        table.put(f"key-{index}", index)
    assert table.capacity >= 8
    assert [table.get(f"key-{index}") for index in range(8)] == list(range(8))


def test_validates_capacity_and_unhashable_keys():
    with pytest.raises(ValueError):
        ResizableHashTable(initial_capacity=0)
    with pytest.raises(TypeError):
        ResizableHashTable().put([], 1)
