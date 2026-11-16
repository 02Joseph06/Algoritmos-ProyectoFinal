import argparse
import json
import time
from statistics import median, pstdev

from C4.c4_universal_hash import colliding_keys, run_collision_comparison


def ejecutar(tamanos: list[int], capacidad: int = 257, repeticiones: int = 5) -> list[dict]:
    resultados = []
    for n in tamanos:
        keys = colliding_keys(capacidad, n)  # preparación fuera de la medición
        tiempos = []
        conteos = None
        for repeticion in range(repeticiones):
            inicio = time.perf_counter()
            conteos = run_collision_comparison(keys, capacidad, seed=4200 + repeticion)
            tiempos.append(time.perf_counter() - inicio)
        resultados.append({
            **conteos,
            "mediana_s": median(tiempos),
            "desviacion_s": pstdev(tiempos),
        })
    return resultados


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compara hashing universal y claves adversarias")
    parser.add_argument("--tamanos", nargs="+", type=int, default=[100, 200, 400, 800, 1600])
    parser.add_argument("--capacidad", type=int, default=257)
    parser.add_argument("--repeticiones", type=int, default=5)
    args = parser.parse_args()
    if args.repeticiones < 5:
        parser.error("--repeticiones debe ser al menos 5")
    print(json.dumps(ejecutar(args.tamanos, args.capacidad, args.repeticiones), indent=2))
