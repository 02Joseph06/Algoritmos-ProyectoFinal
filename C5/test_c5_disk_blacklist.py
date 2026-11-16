from C5.c5_disk_blacklist import DiskLinearHashBlacklist
from DiscoSimulado.disco_simulado import DiscoSimulado


def test_bloom_filter_skips_absent_account_disk_io_and_finds_present():
    with DiscoSimulado(200, block_size=256) as disk:
        index = DiskLinearHashBlacklist(disk, 10, initial_buckets=2)
        index.add("account-A")
        before = disk.read_count
        assert index.contains("absent-account") is False
        assert disk.read_count == before
        assert index.contains("account-A") is True
        assert disk.read_count > before


def test_linear_hash_splits_and_preserves_membership():
    with DiscoSimulado(300, block_size=256) as disk:
        index = DiskLinearHashBlacklist(disk, 100, initial_buckets=2)
        keys = [f"account-{i}" for i in range(40)]
        for key in keys:
            index.add(key)
        assert index.bucket_count > 2
        assert all(index.contains(key) for key in keys)
