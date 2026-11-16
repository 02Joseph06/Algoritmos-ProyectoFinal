import argparse
import json
import time
from statistics import median, pstdev

from C6.c6_pac_perceptron import Perceptron, error_rate, generate_linear_data, pac_sample_bound


def ejecutar(tamanos: list[int], repeticiones: int = 5, epsilon: float = 0.1, delta: float = 0.05) -> list[dict]:
    resultados = []
    for n in tamanos:
        errores = []
        errores_entrenamiento = []
        tiempos = []
        for repeticion in range(repeticiones):
            train_x, train_y = generate_linear_data(n, seed=6000 + n * 17 + repeticion)
            test_x, test_y = generate_linear_data(5000, seed=900000 + n * 31 + repeticion)
            model = Perceptron(2)
            inicio = time.perf_counter()
            model.fit(train_x, train_y)
            tiempos.append(time.perf_counter() - inicio)
            errores_entrenamiento.append(error_rate(model, train_x, train_y))
            errores.append(error_rate(model, test_x, test_y))
        resultados.append({
            "muestras_entrenamiento": n,
            "error_empirico_mediano": median(errores),
            "dispersion_error": pstdev(errores),
            "error_entrenamiento_mediano": median(errores_entrenamiento),
            "mediana_entrenamiento_s": median(tiempos),
            "dispersion_entrenamiento_s": pstdev(tiempos),
            "errores_por_semilla": errores,
            "epsilon_objetivo": epsilon,
            "delta": delta,
            "cota_PAC_muestras_VC": pac_sample_bound(2, epsilon, delta),
        })
    return resultados


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Curva empírica de error y cota PAC/VC para perceptrón")
    parser.add_argument("--tamanos", nargs="+", type=int, default=[20, 40, 80, 160, 320])
    parser.add_argument("--repeticiones", type=int, default=5)
    parser.add_argument("--epsilon", type=float, default=0.1)
    parser.add_argument("--delta", type=float, default=0.05)
    args = parser.parse_args()
    if args.repeticiones < 5:
        parser.error("--repeticiones debe ser al menos 5")
    print(json.dumps(ejecutar(args.tamanos, args.repeticiones, args.epsilon, args.delta), indent=2))
