class DiscoSimulado:
    """Fixed-size in-memory blocks with explicit I/O counters."""

    def __init__(self, num_blocks: int, block_size: int = 4096):
        if num_blocks < 1 or block_size < 1:
            raise ValueError("num_blocks and block_size must be positive")
        self._block_size = block_size
        self._blocks = [bytes(block_size) for _ in range(num_blocks)]
        self.read_count = 0
        self.write_count = 0

    def _validate_index(self, index: int) -> None:
        if not 0 <= index < len(self._blocks):
            raise IndexError("block index out of range")

    def read_block(self, index: int) -> bytes:
        self._validate_index(index)
        self.read_count += 1
        return self._blocks[index]

    def leer_bloque(self, index: int) -> bytes:
        return self.read_block(index)

    def write_block(self, index: int, data: bytes) -> None:
        self._validate_index(index)
        if len(data) > self._block_size:
            raise ValueError("data exceeds block size")
        self._blocks[index] = bytes(data).ljust(self._block_size, b"\0")
        self.write_count += 1

    def escribir_bloque(self, index: int, data: bytes) -> None:
        self.write_block(index, data)
