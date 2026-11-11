import argparse
import json

from C2.c2_hash_table import ResizableHashTable
from datos.generador import generate_keys
from experimentos.medir import medir_puntos


def ejecutar(tamanos: list[int], repeticiones: int = 5) -> list[dict]:
    def preparar(n: int) -> list[str]:
        return generate_keys(n, seed=42 + n)

    def medir_tabla(keys: list[str]) -> None:
        table = ResizableHashTable(initial_capacity=8)
        for index, key in enumerate(keys):
            table.put(key, index)
        for key in keys:
            table.get(key)

    return medir_puntos(preparar, medir_tabla, tamanos, repeticiones)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mide C2 por tamaños geométricos")
    parser.add_argument("--tamanos", nargs="+", type=int, default=[100, 200, 400, 800, 1600])
    parser.add_argument("--repeticiones", type=int, default=5)
    args = parser.parse_args()
    print(json.dumps(ejecutar(args.tamanos, args.repeticiones), indent=2))
