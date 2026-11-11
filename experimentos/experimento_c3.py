import argparse
import json

from C3.c3_knapsack import knapsack_01
from experimentos.medir import medir_puntos


def ejecutar(tamanos: list[int], repeticiones: int = 5) -> list[dict]:
    def preparar(n: int) -> tuple[list[int], list[int], int]:
        weights = [1 + (index % 20) for index in range(n)]
        values = [2 + ((index * 7) % 100) for index in range(n)]
        return weights, values, max(10, n // 2)

    return medir_puntos(preparar, lambda datos: knapsack_01(*datos), tamanos, repeticiones)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mide C3 por tamaños geométricos")
    parser.add_argument("--tamanos", nargs="+", type=int, default=[20, 40, 80, 160, 320])
    parser.add_argument("--repeticiones", type=int, default=5)
    args = parser.parse_args()
    print(json.dumps(ejecutar(args.tamanos, args.repeticiones), indent=2))
