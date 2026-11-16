import tempfile


class DiscoSimulado:
    """Fixed-size binary-file blocks with explicit I/O counters."""

    def __init__(self, num_blocks: int, block_size: int = 4096):
        if num_blocks < 1 or block_size < 1:
            raise ValueError("num_blocks and block_size must be positive")
        self._block_size = block_size
        self._num_blocks = num_blocks
        self._file = tempfile.TemporaryFile(mode="w+b")
        self._file.truncate(num_blocks * block_size)
        self.read_count = 0
        self.write_count = 0

    @property
    def num_blocks(self) -> int:
        return self._num_blocks

    @property
    def block_size(self) -> int:
        return self._block_size

    def _validate_index(self, index: int) -> None:
        if not 0 <= index < self._num_blocks:
            raise IndexError("block index out of range")

    def read_block(self, index: int) -> bytes:
        self._validate_index(index)
        self.read_count += 1
        self._file.seek(index * self._block_size)
        data = self._file.read(self._block_size)
        return data.ljust(self._block_size, b"\0")

    def leer_bloque(self, index: int) -> bytes:
        return self.read_block(index)

    def write_block(self, index: int, data: bytes) -> None:
        self._validate_index(index)
        if len(data) > self._block_size:
            raise ValueError("data exceeds block size")
        self._file.seek(index * self._block_size)
        self._file.write(bytes(data).ljust(self._block_size, b"\0"))
        self._file.flush()
        self.write_count += 1

    def escribir_bloque(self, index: int, data: bytes) -> None:
        self.write_block(index, data)

    def close(self) -> None:
        self._file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
