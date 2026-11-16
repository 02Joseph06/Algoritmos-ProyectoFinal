from C4.c4_universal_hash import ChainingHashTable, colliding_keys, run_collision_comparison


def test_adversarial_fixed_hash_is_quadratic_but_seeded_family_spreads_keys():
    keys = colliding_keys(31, 120)
    result = run_collision_comparison(keys, 31, seed=42)
    assert result["comparaciones_hash_fijo"] == 120 * 121 // 2
    assert result["comparaciones_universal"] < result["comparaciones_hash_fijo"]


def test_universal_table_finds_inserted_key_and_rejects_unknown_key():
    table = ChainingHashTable(17, seed=7)
    table.put("account-A")
    assert table.contains("account-A")
    assert not table.contains("unknown")
