import pytest

from DiscoSimulado.disco_simulado import DiscoSimulado


def test_round_trip_and_counters():
    disk = DiscoSimulado(num_blocks=2, block_size=4)
    disk.escribir_bloque(0, b"abcd")
    assert disk.leer_bloque(0) == b"abcd"
    assert disk.write_count == 1
    assert disk.read_count == 1


def test_validates_blocks_and_size():
    disk = DiscoSimulado(num_blocks=1, block_size=4)
    with pytest.raises(IndexError):
        disk.read_block(1)
    with pytest.raises(ValueError):
        disk.write_block(0, b"too long")
