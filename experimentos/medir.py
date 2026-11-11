import time
from statistics import median, pstdev
from typing import Callable, Iterable


def medir_puntos(
    preparar: Callable[[int], object],
    ejecutar: Callable[[object], object],
    tamanos: Iterable[int],
    repeticiones: int = 5,
) -> list[dict[str, float | int]]:
    """Measure execution only; preparation happens outside the timer."""
    if repeticiones < 5:
        raise ValueError("repeticiones debe ser al menos 5")
    resultados = []
    for tamano in tamanos:
        datos = preparar(tamano)
        tiempos = []
        for _ in range(repeticiones):
            inicio = time.perf_counter()
            ejecutar(datos)
            tiempos.append(time.perf_counter() - inicio)
        resultados.append(
            {
                "tamano": tamano,
                "mediana_s": median(tiempos),
                "desviacion_s": pstdev(tiempos),
            }
        )
    return resultados
