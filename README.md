# Proyecto Final - Detección de fraude en transacciones

Implementación de C1, C2 y C3 del caso del Grupo 4, realizado por Luigi Rincon, Juan Holguin y Daivid Sanchez.

## Alcance

- **C1:** subarreglo de suma máxima por divide y vencerás, en [`C1/c1_max_subarray.py`](./C1/c1_max_subarray.py).
- **C2:** tabla hash con direccionamiento abierto, sondeo lineal, tombstones y duplicación de capacidad, en [`C2/c2_hash_table.py`](./C2/c2_hash_table.py).
- **C3:** mochila 0/1 mediante programación dinámica bottom-up, en [`C3/c3_knapsack.py`](./C3/c3_knapsack.py).
- **Generador:** claves y transacciones reproducibles, en [`datos/generador.py`](./datos/generador.py).
- **Disco:** memoria simulada con conteo de E/S, en [`DiscoSimulado/disco_simulado.py`](./DiscoSimulado/disco_simulado.py).

La entrega incluye C1–C6. La bonificación Count-Min Sketch queda fuera del alcance actual.

## Estructura del repositorio

```text
C1/                  algoritmo y pruebas de C1
C2/                  algoritmo y pruebas de C2
C3/                  algoritmo y pruebas de C3
DiscoSimulado/       disco simulado y pruebas de E/S
datos/               generador reproducible y pruebas
experimentos/        medición común y runners de C1-C6
C4/                  hashing universal frente a colisiones adversarias
C5/                  hashing lineal en disco y filtro Bloom
C6/                  perceptrón y análisis PAC/VC
```

## Correcciones solicitadas por la retroalimentación

### C1: Teorema Maestro

La recurrencia del algoritmo de divide y vencerás es:

```text
T(n) = 2T(n/2) + Θ(n)
```

Aquí `a = 2`, `b = 2` y `f(n) = Θ(n)`. Como `n^(log_b(a)) = n`, se aplica el caso 2 del Teorema Maestro:

```text
T(n) = Θ(n log n)
```

Por tanto, la afirmación previa `Θ(n)` era incorrecta y queda corregida. La implementación usa `Θ(n)` trabajo por nivel y `Θ(log n)` niveles de recursión; el tiempo total es `Θ(n log n)` y la pila recursiva es `Θ(log n)`.

### C2: análisis amortizado por método contable

El análisis esperado de hashing no reemplaza el análisis amortizado de las redimensiones. Se usa el siguiente sistema de créditos para cada **inserción de una clave nueva**:

1. Se cobra un costo amortizado de **4 unidades**.
2. Una unidad paga la inserción/probe actual.
3. Las tres unidades restantes se almacenan como créditos en la entrada insertada.
4. Cuando la tabla se duplica, cada entrada existente consume un crédito para pagar su movimiento al arreglo nuevo.

Si la capacidad pasa de `c/2` a `c`, antes de la siguiente redimensión hay al menos `αc/2` inserciones nuevas, donde `α` es el factor de carga máximo (`0.7` por defecto). Esas inserciones acumulan `3αc/2` créditos, que cubren los `O(c)` movimientos de la redimensión. Como `3α/2 > 1` para el factor configurado, el saldo alcanza para pagarla. Las actualizaciones de claves existentes no requieren créditos nuevos y las eliminaciones dejan tombstones sin provocar una redimensión descendente.

Así, una redimensión individual cuesta `Θ(n)`, pero el costo amortizado de una inserción es `O(1)`. Búsqueda, inserción y eliminación son `O(1)` esperado bajo una función hash razonable; el método contable justifica específicamente el costo acumulado de las redimensiones.

### C3: reconstrucción robusta

La tabla DP conserva `max(sin_elemento, con_elemento)`. Durante la reconstrucción, [`knapsack_01`](./C3/c3_knapsack.py) recalcula ambas alternativas y solo incluye el elemento si `con_elemento > sin_elemento` y además cabe en la capacidad restante. Esto hace explícita la política de desempate hacia la solución sin el elemento y evita asumir que toda diferencia entre filas significa inclusión.

La regla funciona también con valores cero, empates y pesos cero. Un elemento de valor cero no se incluye innecesariamente; uno de peso cero y valor positivo sí se incluye.

### Plan de experimentos y generador

El código del generador está disponible en [`datos/generador.py`](./datos/generador.py) y se prueba en [`datos/test_generador.py`](./datos/test_generador.py). Usa `random.Random(seed)` local, por lo que no altera el generador global y produce exactamente los mismos datos para la misma pareja `(n, seed)`.

Ejemplo de construcción reproducible:

```python
from datos.generador import generate_keys, generate_transactions

keys = generate_keys(1000, seed=1042)
transactions = generate_transactions(1000, seed=1042)
```

Los runners preparan los datos antes de iniciar el cronómetro. [`experimentos/medir.py`](./experimentos/medir.py) solo mide `ejecutar(datos)`, de modo que la generación, las semillas y la configuración no contaminan el tiempo del algoritmo. Cada tamaño usa al menos cinco repeticiones y reporta mediana y desviación estándar.

## Presentación web

La presentación visual del proyecto está en la carpeta local `presentacion/`. Está excluida de Git porque se utiliza como material de exposición y contiene únicamente HTML, CSS y JavaScript estático.

Para verla, abre [`presentacion/index.html`](./presentacion/index.html) directamente en el navegador. No requiere servidor, instalación de dependencias ni conexión a internet.

La página está completamente en español e incluye el problema, la arquitectura, los módulos C1-C6, complejidades, resultados, conclusiones e integridad académica.

## Pruebas

Se requiere Python 3.10 o posterior y `pytest` (`python -m pip install pytest`).

```powershell
python -m pytest C1 -q
python -m pytest C2 -q
python -m pytest C3 -q
python -m pytest C4 -q
python -m pytest C5 -q
python -m pytest C6 -q
python -m pytest datos -q
python -m pytest DiscoSimulado -q
python -m pytest -q
```

## Experimentos

```powershell
python -m experimentos.experimento_c1
python -m experimentos.experimento_c2
python -m experimentos.experimento_c3
python -m experimentos.experimento_c4
python -m experimentos.experimento_c5
python -m experimentos.experimento_c6
```

Se pueden pasar tamaños propios con `--tamanos 100 200 400 800 1600` y cambiar las repeticiones con `--repeticiones 5`.

## Complejidad esperada

- **C1:** `Θ(n log n)` en tiempo y `Θ(log n)` de pila.
- **C2:** operaciones `O(1)` esperado; redimensión `Θ(n)` individual e inserción `O(1)` amortizada.
- **C3:** `Θ(nW)` en tiempo y memoria, con `n` elementos y capacidad `W`.
- **C4:** función fija adversaria `Θ(n)` por operación y `Θ(n²)` total; hashing universal, `O(1+n/m)` esperado por operación en encadenamiento.
- **C5:** las consultas negativas descartadas por Bloom requieren `0` E/S; las positivas requieren una lectura de bucket esperada, más E/S de overflow cuando exista.
- **C6:** clasificador lineal con dimensión VC `d+1`; la muestra PAC suficiente crece como `O((d log(1/ε)+log(1/δ))/ε)`.
- **DiscoSimulado:** cada lectura o escritura de bloque es `O(1)` sin contar el tamaño fijo del bloque.

## C4: hashing universal aleatorizado

[`C4/c4_universal_hash.py`](./C4/c4_universal_hash.py) compara encadenamiento con una función fija determinista frente a la familia universal `h_{a,b}(x) = ((ax+b) mod p) mod m`, con `p = 2^61-1`, `a` uniforme no nulo y `b` uniforme en `0..p-1`. Las claves se convierten a enteros mediante BLAKE2b estable. Para dos enteros distintos del dominio primo, la probabilidad de colisión tras comprimir a `m` casillas está acotada por `1/m + 1/p`; aplicado a identificadores de texto, la garantía queda condicionada a que sus huellas BLAKE2b sean distintas (colisión criptográfica despreciable, pero fuera de la prueba algebraica).

La hipótesis experimental es de adversario **oblivious**: se generan claves que colisionan para la función fija y se usa una semilla independiente para escoger la función universal. En encadenamiento, una búsqueda cuesta `Θ(1+k)` cuando el bucket tiene `k` claves; una función fija atacada permite `Θ(n)` por consulta y `Θ(n²)` comparaciones para cargar/buscar `n` claves. Bajo hashing universal, el número esperado de colisiones de una clave con las otras es como máximo `(n-1)/m`, así que la búsqueda esperada es `O(1+n/m)` (esperado `O(1)` si el factor de carga `n/m` está acotado). Esto no garantiza seguridad frente a un atacante adaptativo que aprende la semilla.

El runner genera cinco tamaños por defecto, fuera del cronómetro, repite cinco veces y reporta comparaciones, mediana y dispersión:

```powershell
python -m experimentos.experimento_c4
python -m experimentos.experimento_c4 --tamanos 100 200 400 800 1600 --capacidad 257 --repeticiones 5
```

## C5: memoria secundaria, hashing lineal y Bloom

[`C5/c5_disk_blacklist.py`](./C5/c5_disk_blacklist.py) mantiene los buckets y cadenas de desbordamiento en [`DiscoSimulado/disco_simulado.py`](./DiscoSimulado/disco_simulado.py), que ahora respalda los bloques con un archivo binario temporal. Toda E/S del índice pasa por `read_block`/`write_block`; no se abre el archivo desde el algoritmo. El filtro Bloom permanece en memoria y no produce falsos negativos.

Parámetros: `N` es el número de cuentas, `M` la memoria interna disponible en registros, `B` el tamaño de bloque en bytes, y `q = floor(B/64)` la capacidad nominal de registros por bucket-block. El índice trabaja con su bloque actual y metadatos del hashing; el filtro Bloom reserva aproximadamente `m = ceil(-N ln(p)/(ln 2)^2)` bits y `k = round((m/N) ln 2)` funciones, para tasa objetivo `p`. La fórmula de memoria externa para consultas es:

```text
p_Bloom ≈ (1 - exp(-kN/m))^k
E[lecturas] ≈ Q+ + Q- · p_Bloom
```

`Q+` son consultas a cuentas registradas y `Q-` a cuentas ausentes. La fórmula supone un bloque de bucket por consulta positiva o falso positivo (sin desbordamiento); el experimento también informa las lecturas reales, que incorporan cualquier bloque de overflow. La construcción reporta por separado lecturas y escrituras contadas. `M` se informa como presupuesto experimental; la representación del Bloom ocupa `ceil(m/8)` bytes y debe caber en dicho presupuesto junto con el bloque de trabajo.

```powershell
python -m experimentos.experimento_c5
python -m experimentos.experimento_c5 --tamanos 5000 10000 20000 40000 80000 --bloque-bytes 4096 --repeticiones 5
```

El JSON entrega `N`, `M`, `B`, E/S de construcción, E/S de consultas observadas, E/S predichas, tasa Bloom estimada y medianas/dispersión de construcción y consulta. Por defecto se elige `M=floor(N/20)` y se valida que alcance para Bloom más el bloque residente; si se pasa `--memoria-registros`, debe respetar ambas cotas. Las claves de consulta se preparan antes del cronómetro; el conteo de E/S es independiente de la duración de CPU.

## C6: garantía PAC basada en dimensión VC

[`C6/c6_pac_perceptron.py`](./C6/c6_pac_perceptron.py) entrena un perceptrón desde cero sobre datos etiquetados por un separador lineal realizable en `d` dimensiones. Los clasificadores lineales tienen dimensión VC `d+1`. Para una hipótesis consistente, el argumento PAC realizable da la cota suficiente:

```text
m ≥ (1/ε) [4 ln(2/δ) + 8(d+1) ln(13/ε)]
```

Con probabilidad al menos `1-δ`, el error verdadero es a lo sumo `ε`, siempre que los ejemplos sean i.i.d. y exista un separador consistente. El perceptrón termina con error de entrenamiento cero en el caso separable; para margen geométrico `γ` y vectores de norma a lo sumo `R`, el teorema clásico acota las actualizaciones por `(R/γ)^2`. El trabajo de entrenamiento es `O(E n d)`, donde `E` es el número de pasadas y `n` el número de ejemplos; la memoria del modelo es `O(d)`. En datos separables con margen `γ` y norma `R`, las pasadas hasta converger son a lo sumo el límite de actualizaciones más una. La profundidad secuencial es `O(E n d)` y no hay costo de comunicación paralelo en esta implementación. La cota de muestras es suficiente, no una predicción de que el perceptrón use exactamente ese tamaño.

El runner compara cinco tamaños de entrenamiento, cinco semillas y un conjunto de prueba independiente de 5000 ejemplos; emite error empírico y dispersión, tiempo de entrenamiento, `ε`, `δ` y la cota PAC para contrastar la tendencia. La generación ocurre fuera del cronómetro:

```powershell
python -m experimentos.experimento_c6
python -m experimentos.experimento_c6 --tamanos 20 40 80 160 320 --repeticiones 5 --epsilon 0.1 --delta 0.05
```

La validación empírica ilustra la curva de error, pero no sustituye la garantía probabilística ni constituye por sí sola una prueba de que el tamaño observado alcance la cota.

## Integridad académica y uso de herramientas

El núcleo de C1, C2 y C3 fue implementado directamente para este proyecto. No se usan `sorted`, `heapq`, `networkx`, `scikit-learn` ni bibliotecas equivalentes para resolver los algoritmos. Se usan únicamente la biblioteca estándar y `pytest` para pruebas.

Se utilizó un asistente de IA (Codex) para consultar la estructura del trabajo, proponer casos de prueba, depurar un desempate de C1 y revisar la documentación. El equipo debe poder explicar cada decisión, función y prueba durante la sustentación.
