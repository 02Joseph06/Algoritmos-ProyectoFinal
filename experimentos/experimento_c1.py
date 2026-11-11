import argparse
import json
import random

from C1.c1_max_subarray import max_subarray_divide_conquer
from experimentos.medir import medir_puntos


def ejecutar(tamanos: list[int], repeticiones: int = 5) -> list[dict]:
    def preparar(n: int) -> list[int]:
        rng = random.Random(42 + n)
        return [rng.randint(-100, 100) for _ in range(n)]

    return medir_puntos(preparar, max_subarray_divide_conquer, tamanos, repeticiones)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mide C1 por tamaños geométricos")
    parser.add_argument("--tamanos", nargs="+", type=int, default=[100, 200, 400, 800, 1600])
    parser.add_argument("--repeticiones", type=int, default=5)
    args = parser.parse_args()
    print(json.dumps(ejecutar(args.tamanos, args.repeticiones), indent=2))
