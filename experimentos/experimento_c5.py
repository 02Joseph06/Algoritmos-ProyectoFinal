import argparse
import json
import math
import time
from statistics import median, pstdev

from C5.c5_disk_blacklist import DiskLinearHashBlacklist
from DiscoSimulado.disco_simulado import DiscoSimulado


def ejecutar(tamanos: list[int], memoria_registros: int | None = None, bloque_bytes: int = 4096, repeticiones: int = 5) -> list[dict]:
    resultados = []
    for n in tamanos:
        capacidad_registros_bloque = max(1, bloque_bytes // 64)
        base_buckets = 2
        max_bloques = max(100, 2 * n // capacidad_registros_bloque + 100)
        consultas_positivas = [f"account-{i}" for i in range(n)]
        consultas_negativas = [f"missing-{i}" for i in range(n)]
        m_registros = memoria_registros if memoria_registros is not None else n // 20
        bloom_bytes = (math.ceil(-n * math.log(0.01) / math.log(2) ** 2) + 7) // 8
        min_memory = math.ceil((bloom_bytes + bloque_bytes) / 64)
        if m_registros > n // 20 or m_registros < min_memory:
            raise ValueError(f"M debe cumplir M <= N/20 y M >= {min_memory} registros para Bloom + un bloque")
        build_times, query_times = [], []
        build_reads = build_writes = query_reads = 0
        predicted = 0.0
        fp_rate = 0.0
        for _ in range(repeticiones):
            with DiscoSimulado(max_bloques, bloque_bytes) as disk:
                index = DiskLinearHashBlacklist(disk, n, initial_buckets=base_buckets)
                start = time.perf_counter()
                for key in consultas_positivas:
                    index.add(key)
                build_times.append(time.perf_counter() - start)
                build_reads, build_writes = disk.read_count, disk.write_count
                start = time.perf_counter()
                for key in consultas_positivas + consultas_negativas:
                    index.contains(key)
                query_times.append(time.perf_counter() - start)
                query_reads = disk.read_count - build_reads
                predicted = index.predicted_query_io(n, n)
                fp_rate = index.estimated_bloom_false_positive_rate()
        resultados.append({
            "N": n,
            "M_registros": m_registros,
            "B_bytes": bloque_bytes,
            "repeticiones": repeticiones,
            "E_S_construccion_leidas": build_reads,
            "E_S_construccion_escritas": build_writes,
            "E_S_consultas_contadas": query_reads,
            "E_S_consultas_predichas": predicted,
            "tasa_falsos_positivos_estimada": fp_rate,
            "mediana_construccion_s": median(build_times),
            "dispersion_construccion_s": pstdev(build_times),
            "mediana_consultas_s": median(query_times),
            "dispersion_consultas_s": pstdev(query_times),
        })
    return resultados


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="E/S del hashing lineal en disco + filtro Bloom")
    parser.add_argument("--tamanos", nargs="+", type=int, default=[5000, 10000, 20000, 40000, 80000])
    parser.add_argument("--memoria-registros", type=int)
    parser.add_argument("--bloque-bytes", type=int, default=4096)
    parser.add_argument("--repeticiones", type=int, default=5)
    args = parser.parse_args()
    if args.repeticiones < 5:
        parser.error("--repeticiones debe ser al menos 5")
    print(json.dumps(ejecutar(args.tamanos, args.memoria_registros, args.bloque_bytes, args.repeticiones), indent=2))
