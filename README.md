# Proyecto Final - Detección de fraude en transacciones

Implementación de C1, C2 y C3 del caso del Grupo 4.

## Alcance actual

- **C1:** subarreglo de suma máxima por divide y vencerás, en `src/c1_max_subarray.py`.
- **C2:** tabla hash con direccionamiento abierto, sondeo lineal, tombstones y duplicación de capacidad, en `src/c2_hash_table.py`.
- **C3:** mochila 0/1 mediante programación dinámica bottom-up, en `src/c3_knapsack.py`.
- Generación reproducible de claves y transacciones en `src/data_generator.py`.
- Disco en memoria con conteo de E/S en `src/disco_simulado.py`.

C4, C5, C6, benchmarking formal y bonificaciones quedan fuera de esta fase.

## Estructura del repositorio

Cada componente contiene su implementación y sus pruebas:

```text
C1/                  algoritmo y test de C1
C2/                  algoritmo y test de C2
C3/                  algoritmo y test de C3
DiscoSimulado/       disco simulado y test de E/S
datos/               generador reproducible y test
experimentos/        medición común y runners de C1-C3
docs/                informe, diseño y planes
```

## Pruebas por módulo

```powershell
python -m pytest C1 -q
python -m pytest C2 -q
python -m pytest C3 -q
python -m pytest datos -q
python -m pytest DiscoSimulado -q
python -m pytest -q
```

## Experimentos

Los runners separan la generación de datos del tiempo medido, usan cinco repeticiones por defecto y reportan mediana y desviación estándar:

```powershell
python -m experimentos.experimento_c1
python -m experimentos.experimento_c2
python -m experimentos.experimento_c3
```

Se pueden pasar tamaños propios con `--tamanos 100 200 400 800 1600` y cambiar las repeticiones con `--repeticiones 5`.

## Ejecución

Se requiere Python 3.10 o posterior. Para instalar la dependencia de pruebas:

```powershell
python -m pip install pytest
```

Para ejecutar la suite:

```powershell
python -m pytest -q
```

## Complejidad esperada

- C1: `T(n) = 2T(n/2) + Θ(n)`, por tanto `Θ(n)` en tiempo y `Θ(log n)` de pila recursiva.
- C2: búsqueda, inserción y eliminación `O(1)` esperado con una función hash razonable; una redimensión cuesta `Θ(n)` y la inserción es `O(1)` amortizada.
- C3: `Θ(nW)` en tiempo y memoria usando una tabla completa para reconstruir la selección.
- `DiscoSimulado`: cada lectura o escritura de bloque es `O(1)` sin contar el tamaño fijo del bloque.

## Integridad académica y uso de herramientas

El núcleo de C1, C2 y C3 fue implementado directamente para este proyecto. No se usan `sorted`, `heapq`, `networkx`, `scikit-learn` ni bibliotecas equivalentes para resolver los algoritmos. Se usan únicamente la biblioteca estándar y `pytest` para pruebas.

Se utilizó un asistente de IA (Codex) para consultar la estructura del trabajo, proponer casos de prueba, depurar un desempate de C1 y revisar la documentación. El equipo debe poder explicar cada decisión, función y prueba durante la sustentación.
