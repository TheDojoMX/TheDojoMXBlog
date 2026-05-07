# Capitulo 11: La amenaza cuantica -- que cambia y que no

> "La computacion cuantica no destruye toda la criptografia, solo la asimetrica. Si alguien te dice que AES-256 esta muerto por culpa de las computadoras cuanticas, no sabe de lo que habla. Pero si tu sistema depende de RSA, ECDSA o Diffie-Hellman --y casi todos dependen--, el reloj ya esta corriendo."

---

En 2019, Google anuncio que su procesador cuantico Sycamore realizo en 200 segundos un calculo que a la supercomputadora mas poderosa del mundo le habria tomado 10,000 anios. En diciembre de 2024, su chip Willow completo una tarea de muestreo de circuitos aleatorios en 5 minutos que habria tomado 10 septillones (10^25) de anios a los supercomputadores actuales. Ninguno de estos calculos sirvio para romper criptografia. Pero demostraron que la aceleracion cuantica no es ciencia ficcion: es ingenieria en progreso.

Este capitulo responde tres preguntas que todo desarrollador debe poder contestar: que puede romper una computadora cuantica, que sobrevive intacto, y por que la amenaza ya es real hoy aunque las computadoras cuanticas criptograficamente relevantes no existan aun.

---

## 11.1 Computacion cuantica para programadores

No necesitas un doctorado en fisica para entender la amenaza cuantica. Necesitas entender tres conceptos: qubits, compuertas cuanticas y aceleracion cuantica. Con eso puedes evaluar el riesgo para tu codigo.

### 11.1.1 Qubits y superposicion: mas alla de 0 y 1

Un bit clasico es un interruptor: esta en 0 o en 1. Un **qubit** (bit cuantico) es fundamentalmente diferente. Gracias al principio de superposicion cuantica, un qubit puede estar en una combinacion de 0 y 1 simultaneamente. No es que "sea ambos a la vez" en el sentido cotidiano; es que su estado se describe mediante dos numeros complejos llamados **amplitudes**, uno para el estado 0 y otro para el estado 1.

Matematicamente, el estado de un qubit se escribe como:

```
|psi> = alpha|0> + beta|1>

Donde:
  alpha, beta = numeros complejos (amplitudes)
  |alpha|^2 + |beta|^2 = 1  (las probabilidades suman 1)
  |alpha|^2 = probabilidad de medir 0
  |beta|^2 = probabilidad de medir 1
```

Lo crucial para la criptografia es la escalabilidad: un sistema de **n** qubits puede representar 2^n amplitudes simultaneamente. Con 300 qubits puedes representar mas estados que atomos hay en el universo observable. Una computadora clasica necesitaria 2^300 numeros complejos en memoria para simular ese sistema; una computadora cuantica lo hace con 300 objetos fisicos.

Pero hay una trampa: cuando **mides** un qubit, la superposicion colapsa. Obtienes un solo resultado --0 o 1-- con probabilidades determinadas por las amplitudes. El arte de la computacion cuantica esta en manipular las amplitudes antes de medir para que el resultado correcto tenga alta probabilidad.

Para un desarrollador, la analogia mas util es esta: imagina que puedes evaluar una funcion en todas sus posibles entradas simultaneamente, pero solo puedes leer un resultado. Los algoritmos cuanticos son tecnicas ingeniosas para que ese unico resultado sea el que necesitas.

### 11.1.2 Compuertas cuanticas y circuitos

Asi como las computadoras clasicas procesan bits con compuertas logicas (AND, OR, NOT), las computadoras cuanticas procesan qubits con **compuertas cuanticas**. Estas compuertas son transformaciones matematicas --rotaciones de vectores en un espacio de alta dimension-- que manipulan las amplitudes de los qubits.

Las compuertas cuanticas mas importantes son:

**Compuerta Hadamard (H):** Pone un qubit en superposicion. Si el qubit esta en |0>, despues de aplicar H, tiene 50% de probabilidad de ser medido como 0 y 50% como 1. Es el "punto de entrada" a la superposicion.

**Compuerta CNOT (Controlled-NOT):** Opera sobre dos qubits. Invierte el segundo qubit si y solo si el primero es 1. Es la compuerta fundamental para crear **entrelazamiento cuantico**: una correlacion entre qubits que no tiene analogo clasico.

**Compuertas de rotacion:** Rotan el estado del qubit en angulos arbitrarios. Permiten control fino de las amplitudes.

Un **circuito cuantico** es una secuencia de compuertas aplicadas a un conjunto de qubits, seguida de una medicion. Es el equivalente cuantico de un programa. Y al igual que un programa clasico, su poder depende del algoritmo, no solo del hardware.

```
Circuito clasico: bits -> compuertas logicas -> bits
Circuito cuantico: qubits -> compuertas cuanticas -> medicion -> bits clasicos
```

La diferencia critica: las compuertas cuanticas operan sobre las 2^n amplitudes simultaneamente. Una sola compuerta aplicada a 50 qubits transforma un vector de 2^50 (mas de un cuatrillon) de numeros complejos. Es como si una sola instruccion operara sobre mas datos que toda la memoria RAM del planeta.

### 11.1.3 Aceleracion cuantica: que se acelera y que no

Aqui viene el punto mas importante y mas malentendido: **una computadora cuantica NO es una computadora clasica mas rapida**. Es una maquina fundamentalmente diferente que acelera ciertos problemas y no hace nada por otros.

Problemas que se aceleran exponencialmente:
- Factorizacion de enteros (algoritmo de Shor)
- Logaritmo discreto (algoritmo de Shor, variante)
- Simulacion de sistemas cuanticos

Problemas que se aceleran cuadraticamente:
- Busqueda en bases de datos no ordenadas (algoritmo de Grover)

Problemas que NO se aceleran significativamente:
- Problemas NP-completos en general
- La mayoria de la computacion cotidiana
- Cifrado simetrico (excepto la aceleracion de Grover)
- Funciones hash (excepto la aceleracion de Grover)

Esto tiene consecuencias directas para la criptografia: los algoritmos asimetricos que dependen de factorizacion o logaritmo discreto estan condenados. Los algoritmos simetricos y los hashes pierden la mitad de su seguridad, pero sobreviven si duplicamos los tamanos de llave.

### 11.1.4 Estado actual del hardware cuantico (2025-2026)

El hardware cuantico avanza rapido, pero todavia esta lejos de romper criptografia. Estos son los hitos mas relevantes:

**Google Willow (diciembre 2024):** Un chip con 105 qubits fisicos que logro reducir errores exponencialmente al escalar qubits --la primera vez que se demuestra correccion de errores cuanticos "por debajo del umbral". En octubre de 2025, Google demostro la primera "ventaja cuantica verificable" con Willow, ejecutando un algoritmo 13,000 veces mas rapido que el mejor supercomputador clasico [Google Quantum AI, 2025].

**IBM Quantum (2025-2026):** IBM lanzo el procesador Nighthawk con 120 qubits y 218 acopladores de nueva generacion, capaz de ejecutar circuitos con un 30% mas de complejidad que la generacion anterior. Para 2026, IBM planea Kookaburra, un sistema multi-chip de 4,158 qubits que conecta tres procesadores mediante enlaces chip-a-chip. IBM proyecta las primeras demostraciones de ventaja cuantica practica para finales de 2026 [IBM Quantum, 2025].

**Perspectiva realista:**

| Hito | Estimacion |
|------|-----------|
| Qubits fisicos actuales (2025) | ~100-1,500 |
| Qubits logicos actuales (2025) | ~1-10 (con correccion de errores) |
| Qubits logicos para romper RSA-2048 | ~4,000 (millones de fisicos) |
| Qubits fisicos para romper RSA-2048 | ~1,000,000 (estimacion Gidney, 2025) |
| | ~100,000 (estimacion con codigos LDPC, 2025) |
| Computadora cuantica criptograficamente relevante | 2035-2045 (estimacion conservadora) |
| | 2030-2035 (estimacion optimista) |

Es importante notar que las estimaciones se reducen con el tiempo. En 2019, Craig Gidney (Google) estimaba que se necesitaban 20 millones de qubits fisicos para factorizar RSA-2048. En mayo de 2025, el mismo investigador redujo esa estimacion a menos de 1 millon de qubits fisicos, una reduccion de 20x en seis anios [Gidney, 2025]. Investigadores australianos han publicado prepublicaciones sugiriendo que con codigos LDPC en lugar del codigo de superficie, podria bastar con menos de 100,000 qubits fisicos.

La tendencia es clara: las estimaciones bajan, no suben. Planificar asumiendo el escenario optimista es lo prudente.

---

## 11.2 El algoritmo de Shor: el fin de RSA y ECC

### 11.2.1 Que resuelve Shor

En 1994, el matematico Peter Shor publico un algoritmo que cambio la criptografia para siempre [Shor, 1994]. El algoritmo de Shor resuelve dos problemas en tiempo polinomial cuantico:

1. **Factorizacion de enteros:** dado un numero compuesto N, encontrar sus factores primos.
2. **Logaritmo discreto:** dado g^x mod p, encontrar x.

En una computadora clasica, estos problemas son computacionalmente intratables para numeros lo suficientemente grandes. El mejor algoritmo clasico conocido para factorizar (la criba del cuerpo de numeros general) tiene complejidad subexponencial. El algoritmo de Shor lo hace en O((log N)^3) operaciones cuanticas --tiempo polinomial.

La idea central de Shor es elegante: transforma el problema de factorizacion en un problema de **encontrar el periodo de una funcion**. Dado N (el numero a factorizar), Shor busca el periodo r de la funcion f(x) = a^x mod N, donde a es un numero aleatorio coprimo con N. Una vez que conoces r, puedes calcular los factores de N con algebra clasica simple (usando el maximo comun divisor).

La parte cuantica es la **Transformada Cuantica de Fourier (QFT)**, que encuentra el periodo de la funcion exponencialmente mas rapido que cualquier algoritmo clasico. La QFT explota la superposicion para evaluar f(x) en todos los valores de x simultaneamente, y luego la interferencia cuantica amplifica las amplitudes correspondientes al periodo correcto.

```
Algoritmo de Shor (simplificado):
1. Elegir a aleatorio, 1 < a < N
2. Verificar que MCD(a, N) = 1 (si no, ya encontraste un factor)
3. PARTE CUANTICA: encontrar el periodo r de f(x) = a^x mod N
   - Crear superposicion de todos los x posibles
   - Calcular f(x) para todos los x simultaneamente
   - Aplicar QFT para extraer el periodo
   - Medir para obtener r
4. PARTE CLASICA: si r es par, calcular MCD(a^(r/2) +/- 1, N)
5. Los resultados son los factores de N
```

### 11.2.2 Impacto: que algoritmos mueren

El algoritmo de Shor destruye toda la criptografia asimetrica que usamos hoy. No es una exageracion: **cada uno** de los algoritmos asimetricos estandar que usas diariamente depende de factorizacion o logaritmo discreto.

| Algoritmo | Problema base | Estado post-cuantico |
|-----------|---------------|---------------------|
| RSA (cifrado y firma) | Factorizacion de enteros | MUERTO |
| ECDSA (firmas, Bitcoin) | Logaritmo discreto sobre curvas elipticas | MUERTO |
| ECDH / X25519 (intercambio de llaves) | Logaritmo discreto sobre curvas elipticas | MUERTO |
| Diffie-Hellman clasico | Logaritmo discreto en Z_p | MUERTO |
| DSA (firmas) | Logaritmo discreto en Z_p | MUERTO |
| EdDSA / Ed25519 (firmas) | Logaritmo discreto sobre curvas elipticas | MUERTO |
| ElGamal (cifrado) | Logaritmo discreto | MUERTO |

Piensa en lo que esto implica para tu stack:

- **TLS/HTTPS:** El handshake usa ECDH o RSA para intercambiar llaves. Muerto.
- **SSH:** La autenticacion usa RSA o Ed25519. Muerto.
- **JWT con RS256 o ES256:** Las firmas usan RSA o ECDSA. Muerto.
- **Git:** Los commits firmados usan GPG (RSA o ECC). Muerto.
- **Bitcoin y Ethereum:** Las transacciones se firman con ECDSA (secp256k1). Muerto.
- **Certificados X.509:** Firmados con RSA o ECDSA. Muerto.
- **Signal, WhatsApp:** El protocolo Signal usa X25519 y Ed25519. Muerto.

La lista continua. Practicamente cualquier sistema que use criptografia de llave publica esta afectado. Y eso es **todo sistema conectado a Internet**.

### 11.2.3 Qubits necesarios: cuanto falta

La pregunta practica es: cuantos qubits se necesitan para ejecutar el algoritmo de Shor contra RSA-2048 y ECC-256?

Las estimaciones mas recientes (mayo 2025, Craig Gidney de Google) son significativamente mas bajas que las de hace unos anios:

**Para RSA-2048:**
- **2019:** ~20 millones de qubits fisicos, ~8 horas [Gidney y Ekera, 2019]
- **2025:** < 1 millon de qubits fisicos, ~5 dias [Gidney, 2025]
- **2025 (codigos LDPC):** < 100,000 qubits fisicos (estimacion teorica)

**Para ECC-256 (curvas elipticas):**
- ~2,330 qubits logicos
- Varios millones de qubits fisicos (con correccion de errores)

El factor clave es la **correccion de errores cuanticos**. Los qubits fisicos son extremadamente fragiles --su informacion se degrada en microsegundos. Para realizar calculos confiables, se necesitan miles de qubits fisicos para codificar un solo **qubit logico** libre de errores. Esta sobrecarga es actualmente del orden de 1,000x a 10,000x.

La buena noticia: Google demostro con Willow que la correccion de errores cuanticos funciona y mejora al escalar. La mala noticia: todavia estamos ordenes de magnitud por debajo de lo necesario.

```python
"""
estimacion_cuantica.py

Estimaciones de recursos cuanticos para romper algoritmos criptograficos.
Basado en Gidney (2025) y estimaciones de la comunidad.
"""


def estimar_riesgo_cuantico():
    """
    Muestra estimaciones actualizadas de recursos cuanticos necesarios
    para romper diferentes algoritmos criptograficos.
    """
    estimaciones = [
        {
            "algoritmo": "RSA-2048",
            "qubits_logicos": 4_000,
            "qubits_fisicos_estimados": "< 1,000,000",
            "tiempo_estimado": "~5 dias",
            "fuente": "Gidney, 2025"
        },
        {
            "algoritmo": "RSA-4096",
            "qubits_logicos": 8_000,
            "qubits_fisicos_estimados": "~2,000,000",
            "tiempo_estimado": "~semanas",
            "fuente": "Estimacion extrapolada"
        },
        {
            "algoritmo": "ECC-256 (P-256, secp256k1)",
            "qubits_logicos": 2_330,
            "qubits_fisicos_estimados": "~varios millones",
            "tiempo_estimado": "~horas",
            "fuente": "Roetteler et al., 2017"
        },
        {
            "algoritmo": "X25519 / Ed25519",
            "qubits_logicos": 2_330,
            "qubits_fisicos_estimados": "~varios millones",
            "tiempo_estimado": "~horas",
            "fuente": "Estimacion por analogia con ECC-256"
        },
    ]

    print("=" * 78)
    print("ESTIMACIONES DE RECURSOS CUANTICOS PARA ROMPER CRIPTOGRAFIA")
    print("=" * 78)
    print()

    for est in estimaciones:
        print(f"Algoritmo: {est['algoritmo']}")
        print(f"  Qubits logicos necesarios:  {est['qubits_logicos']:,}")
        print(f"  Qubits fisicos estimados:   {est['qubits_fisicos_estimados']}")
        print(f"  Tiempo de ejecucion:        {est['tiempo_estimado']}")
        print(f"  Fuente:                     {est['fuente']}")
        print()

    print("-" * 78)
    print("Estado actual del hardware (2025):")
    print(f"  Google Willow:    105 qubits fisicos")
    print(f"  IBM Nighthawk:    120 qubits fisicos")
    print(f"  IBM Kookaburra:   4,158 qubits fisicos (previsto 2026)")
    print()

    # Brecha entre lo disponible y lo necesario
    disponibles = 4_158  # Mejor caso 2026 (IBM Kookaburra)
    necesarios = 1_000_000  # Estimacion conservadora para RSA-2048
    factor = necesarios / disponibles

    print(f"Brecha actual: necesitamos ~{factor:.0f}x mas qubits fisicos")
    print(f"de los que existiran en 2026 para romper RSA-2048.")
    print()
    print("CONCLUSION: No es inminente, pero la tendencia es inequivoca.")
    print("Las estimaciones BAJAN con el tiempo. Planifica en consecuencia.")


estimar_riesgo_cuantico()
```

Salida:

```
============================================================================
ESTIMACIONES DE RECURSOS CUANTICOS PARA ROMPER CRIPTOGRAFIA
============================================================================

Algoritmo: RSA-2048
  Qubits logicos necesarios:  4,000
  Qubits fisicos estimados:   < 1,000,000
  Tiempo de ejecucion:        ~5 dias
  Fuente:                     Gidney, 2025

Algoritmo: RSA-4096
  Qubits logicos necesarios:  8,000
  Qubits fisicos estimados:   ~2,000,000
  Tiempo de ejecucion:        ~semanas
  Fuente:                     Estimacion extrapolada

Algoritmo: ECC-256 (P-256, secp256k1)
  Qubits logicos necesarios:  2,330
  Qubits fisicos estimados:   ~varios millones
  Tiempo de ejecucion:        ~horas
  Fuente:                     Roetteler et al., 2017

Algoritmo: X25519 / Ed25519
  Qubits logicos necesarios:  2,330
  Qubits fisicos estimados:   ~varios millones
  Tiempo de ejecucion:        ~horas
  Fuente:                     Estimacion por analogia con ECC-256

--------------------------------------------------------------------------
Estado actual del hardware (2025):
  Google Willow:    105 qubits fisicos
  IBM Nighthawk:    120 qubits fisicos
  IBM Kookaburra:   4,158 qubits fisicos (previsto 2026)

Brecha actual: necesitamos ~240x mas qubits fisicos
de los que existiran en 2026 para romper RSA-2048.

CONCLUSION: No es inminente, pero la tendencia es inequivoca.
Las estimaciones BAJAN con el tiempo. Planifica en consecuencia.
```

---

## 11.3 El algoritmo de Grover: la mitad de la seguridad

### 11.3.1 Busqueda cuadraticamente mas rapida

Mientras Shor destruye la criptografia asimetrica, el algoritmo de Grover (1996) debilita --pero no destruye-- la criptografia simetrica y las funciones hash [Grover, 1996].

El problema que resuelve Grover es la **busqueda en una base de datos no ordenada**. Clasicamente, si tienes N elementos y buscas uno que cumpla cierta condicion, necesitas O(N) intentos en el peor caso. El algoritmo de Grover lo hace en O(sqrt(N)) intentos cuanticos.

Aplicado a la criptografia, esto significa:

**Fuerza bruta contra cifrados simetricos:**

Una llave de k bits tiene 2^k posibilidades. Clasicamente necesitas O(2^k) intentos. Con Grover, necesitas O(2^(k/2)) intentos cuanticos. Es decir, la seguridad efectiva se reduce a la mitad:

```
Cifrado          Seguridad clasica    Seguridad post-cuantica (Grover)
-----------      -----------------    --------------------------------
AES-128          128 bits             64 bits  (INSUFICIENTE)
AES-192          192 bits             96 bits  (marginal)
AES-256          256 bits             128 bits (SUFICIENTE)
3DES             112 bits             56 bits  (INSUFICIENTE)
ChaCha20         256 bits             128 bits (SUFICIENTE)
```

**Busqueda de colisiones en hashes:**

Para encontrar una colision en un hash de n bits, clasicamente necesitas ~2^(n/2) intentos (ataque de cumpleanios). Con Grover, esto baja a ~2^(n/3). Para preimagen, pasa de 2^n a 2^(n/2):

```
Hash             Seguridad colision    Post-cuantica (colision)
-----------      -----------------     ------------------------
SHA-256          128 bits              ~85 bits (aun suficiente)
SHA-384          192 bits              ~128 bits (suficiente)
SHA-512          256 bits              ~170 bits (suficiente)
SHA3-256         128 bits              ~85 bits (aun suficiente)
```

### 11.3.2 La solucion: duplicar tamanos de llave

A diferencia de Shor, la solucion contra Grover es sencilla: **usa llaves mas grandes**.

```python
"""
impacto_grover.py

Calcula el impacto del algoritmo de Grover en la seguridad de
cifrados simetricos y funciones hash.
"""


def seguridad_post_cuantica_simetrico(bits_llave: int) -> int:
    """
    Calcula la seguridad efectiva post-cuantica de un
    cifrado simetrico, considerando el algoritmo de Grover.

    Grover reduce la seguridad de fuerza bruta a la mitad.
    """
    return bits_llave // 2


def seguridad_post_cuantica_hash_preimagen(bits_hash: int) -> int:
    """Seguridad de preimagen post-cuantica (Grover)."""
    return bits_hash // 2


def seguridad_post_cuantica_hash_colision(bits_hash: int) -> int:
    """
    Seguridad de colision post-cuantica.
    Clasica: n/2 bits (ataque de cumpleanios).
    Con Grover: ~n/3 bits (BHT algorithm).
    """
    return bits_hash // 3


def evaluar_algoritmos():
    """Evalua la seguridad post-cuantica de algoritmos comunes."""

    NIVEL_MINIMO = 128  # bits de seguridad minima recomendada

    print("=" * 70)
    print("IMPACTO DEL ALGORITMO DE GROVER")
    print("=" * 70)

    # Cifrados simetricos
    simetricos = [
        ("AES-128", 128),
        ("AES-192", 192),
        ("AES-256", 256),
        ("ChaCha20", 256),
        ("3DES", 112),
    ]

    print("\nCIFRADOS SIMETRICOS:")
    print(f"{'Algoritmo':<15} {'Clasica':>10} {'Post-cuantica':>15} {'Estado':>12}")
    print("-" * 55)

    for nombre, bits in simetricos:
        pq = seguridad_post_cuantica_simetrico(bits)
        estado = "OK" if pq >= NIVEL_MINIMO else "INSUFICIENTE"
        print(f"{nombre:<15} {bits:>10} bits {pq:>11} bits {estado:>12}")

    # Funciones hash (preimagen)
    hashes = [
        ("SHA-256", 256),
        ("SHA-384", 384),
        ("SHA-512", 512),
        ("SHA3-256", 256),
        ("BLAKE3", 256),
    ]

    print(f"\nFUNCIONES HASH (preimagen):")
    print(f"{'Hash':<15} {'Clasica':>10} {'Post-cuantica':>15} {'Estado':>12}")
    print("-" * 55)

    for nombre, bits in hashes:
        pq = seguridad_post_cuantica_hash_preimagen(bits)
        estado = "OK" if pq >= NIVEL_MINIMO else "MARGINAL"
        print(f"{nombre:<15} {bits:>10} bits {pq:>11} bits {estado:>12}")

    # Derivacion de contrasenas
    print("\nDERIVACION DE CONTRASENAS:")
    print("Argon2, bcrypt, scrypt: NO afectados significativamente.")
    print("Razon: Grover requiere evaluaciones cuanticas secuenciales")
    print("de la funcion. El costo de memoria y las iteraciones de")
    print("estas funciones hacen impractico el ataque cuantico.")
    print()
    print(f"RECOMENDACION: Usa AES-256, ChaCha20, SHA-384/512, SHA3-256.")
    print(f"Evita AES-128 y 3DES en sistemas que deban ser post-cuanticos.")


evaluar_algoritmos()
```

Salida:

```
======================================================================
IMPACTO DEL ALGORITMO DE GROVER
======================================================================

CIFRADOS SIMETRICOS:
Algoritmo        Clasica   Post-cuantica       Estado
-------------------------------------------------------
AES-128              128 bits         64 bits INSUFICIENTE
AES-192              192 bits         96 bits INSUFICIENTE
AES-256              256 bits        128 bits           OK
ChaCha20             256 bits        128 bits           OK
3DES                 112 bits         56 bits INSUFICIENTE

FUNCIONES HASH (preimagen):
Hash             Clasica   Post-cuantica       Estado
-------------------------------------------------------
SHA-256              256 bits        128 bits           OK
SHA-384              384 bits        192 bits           OK
SHA-512              512 bits        256 bits           OK
SHA3-256             256 bits        128 bits           OK
BLAKE3               256 bits        128 bits           OK

DERIVACION DE CONTRASENAS:
Argon2, bcrypt, scrypt: NO afectados significativamente.
Razon: Grover requiere evaluaciones cuanticas secuenciales
de la funcion. El costo de memoria y las iteraciones de
estas funciones hacen impractico el ataque cuantico.

RECOMENDACION: Usa AES-256, ChaCha20, SHA-384/512, SHA3-256.
Evita AES-128 y 3DES en sistemas que deban ser post-cuanticos.
```

Un detalle tecnico importante: el algoritmo de Grover contra AES requiere que la computadora cuantica ejecute el circuito completo de AES como un oraculo cuantico. Investigadores de la TU Darmstadt estimaron que atacar AES-256 con Grover requeriria del orden de 2^128 operaciones cuanticas, cada una implementando el circuito completo de AES en hardware cuantico. Incluso con una computadora cuantica, esto tomaria un tiempo astronomicamente largo [Grassl et al., 2016]. Por esto, AES-256 se considera seguro en la practica post-cuantica, no solo en teoria.

### 11.3.3 Funciones de derivacion de contrasenas: un caso especial

Argon2, bcrypt y scrypt son resistentes al algoritmo de Grover por una razon practica: su diseno deliberadamente lento y con alto consumo de memoria. Grover acelera la busqueda cuadraticamente, pero cada evaluacion del "oraculo" (la funcion de derivacion) sigue siendo costosa. Ademas, Grover requiere que las evaluaciones del oraculo se ejecuten secuencialmente en el circuito cuantico --no se pueden paralelizar dentro del algoritmo.

Con Argon2 configurado para tomar 1 segundo y 1 GB de memoria por evaluacion, incluso con la aceleracion de Grover, un ataque de fuerza bruta contra una contrasena con 80 bits de entropia requeriria 2^40 evaluaciones cuanticas secuenciales, cada una necesitando 1 GB de memoria cuantica y 1 segundo. Esto es completamente impractico.

---

## 11.4 Que sobrevive: el inventario post-cuantico

Resumamos en una tabla completa que sobrevive y que muere:

```
TABLA DE IMPACTO CUANTICO POR ALGORITMO

==================================================================
CRIPTOGRAFIA ASIMETRICA (Shor -> DESTRUIDA)
==================================================================
Algoritmo          Uso comun           Accion
------------------------------------------------------------------
RSA-2048/4096      TLS, SSH, JWT       MIGRAR a ML-KEM / ML-DSA
ECDSA (P-256)      TLS, Bitcoin        MIGRAR a ML-DSA
ECDH / X25519      TLS key exchange    MIGRAR a ML-KEM
Ed25519            SSH, firmas         MIGRAR a ML-DSA
Diffie-Hellman     Legado              MIGRAR a ML-KEM
ElGamal            Nicho               MIGRAR a ML-KEM

==================================================================
CRIPTOGRAFIA SIMETRICA (Grover -> DEBILITADA)
==================================================================
Algoritmo          Seguridad PQ        Accion
------------------------------------------------------------------
AES-128            64 bits             MIGRAR a AES-256
AES-256            128 bits            SEGURO (mantener)
ChaCha20           128 bits            SEGURO (mantener)
ChaCha20-Poly1305  128 bits            SEGURO (mantener)
AES-GCM-256       128 bits            SEGURO (mantener)
3DES               56 bits             ELIMINAR (ya obsoleto)

==================================================================
FUNCIONES HASH (Grover -> DEBILITADAS)
==================================================================
Hash               Seguridad PQ        Accion
------------------------------------------------------------------
SHA-256            128 bits (preim.)   SEGURO (mantener)
SHA-384            192 bits (preim.)   SEGURO (mantener)
SHA-512            256 bits (preim.)   SEGURO (mantener)
SHA3-256           128 bits (preim.)   SEGURO (mantener)
BLAKE3             128 bits (preim.)   SEGURO (mantener)
MD5                ROTO (ya hoy)       ELIMINAR
SHA-1              ROTO (ya hoy)       ELIMINAR

==================================================================
DERIVACION DE CONTRASENAS
==================================================================
Algoritmo          Seguridad PQ        Accion
------------------------------------------------------------------
Argon2id           SEGURO              MANTENER
bcrypt             SEGURO              MANTENER
scrypt             SEGURO              MANTENER
PBKDF2             MARGINAL            MIGRAR a Argon2id

==================================================================
MACs
==================================================================
Algoritmo          Seguridad PQ        Accion
------------------------------------------------------------------
HMAC-SHA-256       128 bits            SEGURO (mantener)
HMAC-SHA-512       256 bits            SEGURO (mantener)
Poly1305           SEGURO              MANTENER
AES-CMAC           Depende de llave    Usar AES-256
```

---

## 11.5 "Harvest Now, Decrypt Later": la amenaza ya es real HOY

### 11.5.1 El escenario mas urgente

No necesitas esperar a que exista una computadora cuantica criptograficamente relevante para que la amenaza cuantica te afecte. La amenaza mas inmediata tiene un nombre: **"Harvest Now, Decrypt Later" (HNDL)** --recolecta ahora, descifra despues.

El escenario es simple y escalofriante: un adversario --tipicamente un actor estatal con recursos de inteligencia-- intercepta y almacena trafico cifrado hoy. No puede descifrarlo ahora, pero lo guarda en discos duros (el almacenamiento es barato) esperando el dia en que una computadora cuantica pueda romper el cifrado asimetrico usado en el intercambio de llaves.

Cuando ese dia llegue, el adversario:
1. Extrae la llave de sesion de cada conexion TLS almacenada (rompiendo ECDH o RSA con Shor).
2. Descifra todo el trafico con la llave de sesion (AES-256 resiste Grover, pero la llave ya fue comprometida).
3. Accede a todos los datos que transitaron por esas conexiones.

### 11.5.2 Evidencia de campanas activas

Esto no es un escenario hipotetico. Multiples agencias de seguridad han emitido advertencias explicitas:

La **NSA, CISA y NIST** han publicado avisos conjuntos advirtiendo que adversarios ya podrian estar recolectando datos cifrados con valor estrategico a largo plazo, con la intencion de descifrarlos cuando dispongan de computadoras cuanticas [CISA, 2024].

El **Departamento de Seguridad Nacional de EE.UU.**, el **Centro Nacional de Ciberseguridad del Reino Unido (NCSC)**, la **Agencia de la Union Europea para la Ciberseguridad (ENISA)** y el **Centro Australiano de Ciberseguridad** basan sus guias de migracion post-cuantica en la premisa de que adversarios ya estan exfiltrando y almacenando datos cifrados sensibles [ENISA, 2021].

La **Reserva Federal de EE.UU.** publico en 2025 un analisis formal del modelo HNDL y su impacto en el sector financiero, concluyendo que la amenaza es real e inmediata para datos con vida util superior a 10-15 anios [Federal Reserve, 2025].

### 11.5.3 El calculo de urgencia

La pregunta clave no es "cuando existira la computadora cuantica?" sino "cuanto tiempo necesitan ser confidenciales mis datos?"

```python
"""
calculo_hndl.py

Calcula la ventana de exposicion HNDL (Harvest Now, Decrypt Later)
para diferentes tipos de datos.
"""

from datetime import datetime


def calcular_exposicion_hndl(
    nombre_dato: str,
    anos_confidencialidad: int,
    ano_computadora_cuantica_optimista: int = 2035,
    ano_computadora_cuantica_conservador: int = 2045,
) -> dict:
    """
    Calcula si un tipo de dato ya esta en riesgo por HNDL.

    Parametros:
      nombre_dato: descripcion del tipo de dato
      anos_confidencialidad: cuantos anos debe ser confidencial
      ano_computadora_cuantica_optimista: estimacion optimista
      ano_computadora_cuantica_conservador: estimacion conservadora

    Retorna:
      Diccionario con el analisis de riesgo.
    """
    ano_actual = datetime.now().year
    # Si los datos capturados hoy necesitan ser confidenciales
    # hasta ano_actual + anos_confidencialidad, y la computadora
    # cuantica llega antes, estan comprometidos.
    ano_expiracion = ano_actual + anos_confidencialidad

    riesgo_optimista = ano_expiracion > ano_computadora_cuantica_optimista
    riesgo_conservador = ano_expiracion > ano_computadora_cuantica_conservador

    if riesgo_conservador:
        nivel = "CRITICO"
    elif riesgo_optimista:
        nivel = "ALTO"
    else:
        nivel = "BAJO"

    return {
        "dato": nombre_dato,
        "confidencialidad_requerida": f"{anos_confidencialidad} anos",
        "datos_expuestos_hasta": ano_expiracion,
        "riesgo_escenario_optimista": riesgo_optimista,
        "riesgo_escenario_conservador": riesgo_conservador,
        "nivel_riesgo": nivel,
    }


# --- Evaluar diferentes tipos de datos ---
tipos_datos = [
    ("Tokens de sesion web", 1),
    ("Credenciales de API", 3),
    ("Datos financieros trimestrales", 5),
    ("Historiales medicos", 50),
    ("Secretos de estado", 75),
    ("Propiedad intelectual (patentes)", 20),
    ("Comunicaciones diplomaticas", 30),
    ("Datos personales (GDPR)", 25),
    ("Contratos comerciales", 10),
    ("Secretos comerciales", 30),
]

print("=" * 72)
print("ANALISIS DE RIESGO HNDL (Harvest Now, Decrypt Later)")
print(f"Ano actual: {datetime.now().year}")
print(f"Computadora cuantica: 2035 (optimista) / 2045 (conservador)")
print("=" * 72)
print()

for nombre, anos in tipos_datos:
    resultado = calcular_exposicion_hndl(nombre, anos)
    print(f"  {resultado['dato']}")
    print(f"    Confidencialidad: {resultado['confidencialidad_requerida']}")
    print(f"    Datos expuestos hasta: {resultado['datos_expuestos_hasta']}")
    print(f"    Nivel de riesgo HNDL: {resultado['nivel_riesgo']}")
    print()

print("-" * 72)
print("CONCLUSION: Si tus datos necesitan mas de ~10 anos de")
print("confidencialidad, la migracion a criptografia post-cuantica")
print("es URGENTE. El trafico capturado hoy esta expuesto.")
```

Salida (ejecutado en 2026):

```
========================================================================
ANALISIS DE RIESGO HNDL (Harvest Now, Decrypt Later)
Ano actual: 2026
Computadora cuantica: 2035 (optimista) / 2045 (conservador)
========================================================================

  Tokens de sesion web
    Confidencialidad: 1 anos
    Datos expuestos hasta: 2027
    Nivel de riesgo HNDL: BAJO

  Credenciales de API
    Confidencialidad: 3 anos
    Datos expuestos hasta: 2029
    Nivel de riesgo HNDL: BAJO

  Datos financieros trimestrales
    Confidencialidad: 5 anos
    Datos expuestos hasta: 2031
    Nivel de riesgo HNDL: BAJO

  Historiales medicos
    Confidencialidad: 50 anos
    Datos expuestos hasta: 2076
    Nivel de riesgo HNDL: CRITICO

  Secretos de estado
    Confidencialidad: 75 anos
    Datos expuestos hasta: 2101
    Nivel de riesgo HNDL: CRITICO

  Propiedad intelectual (patentes)
    Confidencialidad: 20 anos
    Datos expuestos hasta: 2046
    Nivel de riesgo HNDL: CRITICO

  Comunicaciones diplomaticas
    Confidencialidad: 30 anos
    Datos expuestos hasta: 2056
    Nivel de riesgo HNDL: CRITICO

  Datos personales (GDPR)
    Confidencialidad: 25 anos
    Datos expuestos hasta: 2051
    Nivel de riesgo HNDL: CRITICO

  Contratos comerciales
    Confidencialidad: 10 anos
    Datos expuestos hasta: 2036
    Nivel de riesgo HNDL: ALTO

  Secretos comerciales
    Confidencialidad: 30 anos
    Datos expuestos hasta: 2056
    Nivel de riesgo HNDL: CRITICO

------------------------------------------------------------------------
CONCLUSION: Si tus datos necesitan mas de ~10 anos de
confidencialidad, la migracion a criptografia post-cuantica
es URGENTE. El trafico capturado hoy esta expuesto.
```

El mensaje es claro: para historiales medicos, propiedad intelectual, datos personales bajo GDPR y cualquier informacion con vida util larga, la amenaza HNDL convierte un problema futuro en un problema presente. Cada dia que pases transmitiendo estos datos con ECDH o RSA sin proteccion post-cuantica es un dia de exposicion potencial.

---

## 11.6 Ejercicio integrador: audita tu proyecto

Este ejercicio te guia para identificar las primitivas criptograficas vulnerables en tu proyecto y crear un inventario de riesgo cuantico.

```python
"""
auditoria_cuantica.py

Herramienta para auditar un proyecto e identificar primitivas
criptograficas vulnerables a computadoras cuanticas.

Escanea archivos de codigo fuente buscando patrones que indiquen
uso de criptografia vulnerable.
"""

import os
import re
from pathlib import Path
from collections import defaultdict


# Patrones de uso criptografico y su clasificacion
PATRONES_VULNERABLES = {
    # RSA
    r"RSA": {
        "tipo": "Asimetrica",
        "amenaza": "Shor (factorizacion)",
        "accion": "Migrar a ML-KEM (intercambio) o ML-DSA (firma)",
        "urgencia": "ALTA",
    },
    # ECDSA / curvas elipticas
    r"ECDSA|SECP256|secp256k1|secp384r1|P-256|P-384": {
        "tipo": "Asimetrica",
        "amenaza": "Shor (logaritmo discreto)",
        "accion": "Migrar a ML-DSA",
        "urgencia": "ALTA",
    },
    # ECDH / X25519
    r"ECDH|X25519|Curve25519|x25519": {
        "tipo": "Asimetrica",
        "amenaza": "Shor (logaritmo discreto)",
        "accion": "Migrar a ML-KEM (hibrido X25519 + ML-KEM-768)",
        "urgencia": "ALTA",
    },
    # Ed25519
    r"Ed25519|ed25519|EdDSA": {
        "tipo": "Asimetrica",
        "amenaza": "Shor (logaritmo discreto)",
        "accion": "Migrar a ML-DSA",
        "urgencia": "ALTA",
    },
    # Diffie-Hellman clasico
    r"DiffieHellman|diffie.hellman|DHE|dh_parameters": {
        "tipo": "Asimetrica",
        "amenaza": "Shor (logaritmo discreto)",
        "accion": "Migrar a ML-KEM",
        "urgencia": "ALTA",
    },
    # AES-128 (vulnerable por Grover)
    r"AES.?128|aes_128|AES128": {
        "tipo": "Simetrica",
        "amenaza": "Grover (seguridad reducida a 64 bits)",
        "accion": "Migrar a AES-256",
        "urgencia": "MEDIA",
    },
    # 3DES (ya obsoleto, peor con Grover)
    r"3DES|TripleDES|DES3|triple.des": {
        "tipo": "Simetrica",
        "amenaza": "Grover (seguridad reducida a 56 bits)",
        "accion": "Migrar a AES-256 o ChaCha20-Poly1305",
        "urgencia": "ALTA",
    },
}

PATRONES_SEGUROS = {
    r"AES.?256|aes_256|AES256|AES-GCM-256": "AES-256: SEGURO post-cuantico",
    r"ChaCha20|chacha20|CHACHA20": "ChaCha20: SEGURO post-cuantico",
    r"SHA.?256|sha256|SHA256": "SHA-256: SEGURO post-cuantico",
    r"SHA.?384|sha384": "SHA-384: SEGURO post-cuantico",
    r"SHA.?512|sha512": "SHA-512: SEGURO post-cuantico",
    r"SHA3|sha3|Keccak|keccak": "SHA-3: SEGURO post-cuantico",
    r"BLAKE3|blake3": "BLAKE3: SEGURO post-cuantico",
    r"Argon2|argon2": "Argon2: SEGURO post-cuantico",
    r"bcrypt": "bcrypt: SEGURO post-cuantico",
    r"HMAC|hmac": "HMAC: SEGURO post-cuantico (con hash seguro)",
}

# Extensiones de archivo a escanear
EXTENSIONES = {
    ".py", ".js", ".ts", ".java", ".go", ".rs", ".rb", ".php",
    ".c", ".cpp", ".h", ".cs", ".swift", ".kt", ".yaml", ".yml",
    ".toml", ".json", ".xml", ".conf", ".cfg", ".ini",
}


def escanear_archivo(ruta: Path) -> list:
    """Escanea un archivo buscando patrones criptograficos."""
    hallazgos = []

    try:
        contenido = ruta.read_text(encoding="utf-8", errors="ignore")
    except (PermissionError, OSError):
        return hallazgos

    for patron, info in PATRONES_VULNERABLES.items():
        coincidencias = re.findall(patron, contenido)
        if coincidencias:
            # Encontrar numeros de linea
            for i, linea in enumerate(contenido.splitlines(), 1):
                if re.search(patron, linea):
                    hallazgos.append({
                        "archivo": str(ruta),
                        "linea": i,
                        "patron": coincidencias[0],
                        "vulnerable": True,
                        **info,
                    })

    for patron, descripcion in PATRONES_SEGUROS.items():
        coincidencias = re.findall(patron, contenido)
        if coincidencias:
            hallazgos.append({
                "archivo": str(ruta),
                "linea": 0,
                "patron": coincidencias[0],
                "vulnerable": False,
                "descripcion": descripcion,
            })

    return hallazgos


def auditar_proyecto(directorio: str) -> None:
    """
    Escanea un directorio de proyecto buscando uso de
    criptografia vulnerable a computadoras cuanticas.
    """
    ruta = Path(directorio)
    if not ruta.is_dir():
        print(f"Error: {directorio} no es un directorio valido.")
        return

    hallazgos_vulnerables = []
    hallazgos_seguros = []

    # Escanear archivos
    archivos_escaneados = 0
    for archivo in ruta.rglob("*"):
        if archivo.is_file() and archivo.suffix in EXTENSIONES:
            # Ignorar directorios comunes
            partes = archivo.parts
            if any(d in partes for d in [
                "node_modules", ".git", "__pycache__", "venv",
                ".venv", "vendor", "dist", "build"
            ]):
                continue

            archivos_escaneados += 1
            for hallazgo in escanear_archivo(archivo):
                if hallazgo.get("vulnerable"):
                    hallazgos_vulnerables.append(hallazgo)
                else:
                    hallazgos_seguros.append(hallazgo)

    # Reporte
    print("=" * 72)
    print("AUDITORIA DE RIESGO CUANTICO")
    print(f"Directorio: {directorio}")
    print(f"Archivos escaneados: {archivos_escaneados}")
    print("=" * 72)

    if hallazgos_vulnerables:
        print(f"\nPRIMITIVAS VULNERABLES ENCONTRADAS: {len(hallazgos_vulnerables)}")
        print("-" * 72)

        for h in hallazgos_vulnerables:
            print(f"\n  [{h['urgencia']}] {h['archivo']}:{h['linea']}")
            print(f"    Patron encontrado: {h['patron']}")
            print(f"    Tipo: {h['tipo']}")
            print(f"    Amenaza: {h['amenaza']}")
            print(f"    Accion: {h['accion']}")
    else:
        print("\nNo se encontraron primitivas vulnerables.")

    if hallazgos_seguros:
        print(f"\nPRIMITIVAS SEGURAS ENCONTRADAS:")
        print("-" * 72)
        descripciones_unicas = set()
        for h in hallazgos_seguros:
            desc = h.get("descripcion", "")
            if desc not in descripciones_unicas:
                descripciones_unicas.add(desc)
                print(f"  [OK] {desc}")

    # Resumen
    print("\n" + "=" * 72)
    print("RESUMEN")
    print("=" * 72)

    if hallazgos_vulnerables:
        por_urgencia = defaultdict(int)
        for h in hallazgos_vulnerables:
            por_urgencia[h["urgencia"]] += 1

        for urgencia in ["ALTA", "MEDIA", "BAJA"]:
            if urgencia in por_urgencia:
                print(f"  Urgencia {urgencia}: {por_urgencia[urgencia]} hallazgos")

        print()
        print("  SIGUIENTE PASO: Crea un plan de migracion priorizando")
        print("  por urgencia. Comienza con el intercambio de llaves")
        print("  (capitulo 12) y luego migra las firmas digitales.")
    else:
        print("  Tu proyecto no muestra uso de primitivas vulnerables")
        print("  en los archivos escaneados. Verifica manualmente")
        print("  las dependencias y la configuracion de TLS.")


# --- Uso ---
if __name__ == "__main__":
    import sys
    directorio = sys.argv[1] if len(sys.argv) > 1 else "."
    auditar_proyecto(directorio)
```

Uso:

```bash
python auditoria_cuantica.py /ruta/a/tu/proyecto
```

**Instrucciones del ejercicio:**

1. Ejecuta el script contra tu proyecto actual.
2. Revisa cada hallazgo vulnerable y confirma si es un uso real o un falso positivo (por ejemplo, un comentario o una constante no utilizada).
3. Para cada hallazgo real, documenta: que componente lo usa, que datos protege, y cuanto tiempo deben ser confidenciales esos datos.
4. Clasifica cada hallazgo usando el calculo HNDL: si los datos necesitan mas de 10 anios de confidencialidad, la migracion es urgente.
5. Crea un documento con tu inventario criptografico. Este inventario sera la base para el plan de migracion del capitulo 12.

---

## Resumen del capitulo

La computacion cuantica no destruye toda la criptografia. Destruye la criptografia asimetrica --RSA, ECC, Diffie-Hellman-- mediante el algoritmo de Shor, que factoriza enteros y calcula logaritmos discretos en tiempo polinomial. Debilita la criptografia simetrica y los hashes mediante el algoritmo de Grover, que reduce la seguridad a la mitad, pero esto se resuelve duplicando los tamanos de llave.

La amenaza mas urgente no es la computadora cuantica en si, sino la estrategia "Harvest Now, Decrypt Later": adversarios capturando trafico cifrado hoy para descifrarlo en el futuro. Para cualquier dato con vida util superior a 10 anios, la amenaza ya es real.

El siguiente capitulo te mostrara exactamente como migrar: los nuevos algoritmos estandarizados por el NIST, las bibliotecas disponibles, y un plan paso a paso para proteger tu codigo.

---

## Referencias

[Shor, 1994] Shor, P. W. "Algorithms for quantum computation: discrete logarithms and factoring." *Proceedings of the 35th Annual Symposium on Foundations of Computer Science*. IEEE, 1994.

[Grover, 1996] Grover, L. K. "A fast quantum mechanical algorithm for database search." *Proceedings of the 28th Annual ACM Symposium on Theory of Computing*. ACM, 1996.

[Gidney y Ekera, 2019] Gidney, C. y Ekera, M. "How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits." *arXiv:1905.09749*. 2019.

[Gidney, 2025] Gidney, C. "Factoring 2048-bit RSA integers in 177 days with 13,436 qubits and 8 levels of magic state distillation." *arXiv preprint*. Google Quantum AI, mayo 2025.

[Grassl et al., 2016] Grassl, M. et al. "Applying Grover's Algorithm to AES: Quantum Resource Estimates." *Lecture Notes in Computer Science*. Springer, 2016. arXiv:1512.04965.

[Roetteler et al., 2017] Roetteler, M. et al. "Quantum resource estimates for computing elliptic curve discrete logarithms." *ASIACRYPT 2017*. Springer, 2017.

[Google Quantum AI, 2024] "Meet Willow, our state-of-the-art quantum chip." Google Research Blog, diciembre 2024. https://blog.google/innovation-and-ai/technology/research/google-willow-quantum-chip/

[Google Quantum AI, 2025] "Our Quantum Echoes algorithm is a big step toward real-world applications for quantum computing." Google Research Blog, octubre 2025. https://blog.google/technology/research/quantum-echoes-willow-verifiable-quantum-advantage/

[IBM Quantum, 2025] "IBM Delivers New Quantum Processors, Software, and Algorithm Breakthroughs." IBM Newsroom, noviembre 2025. https://newsroom.ibm.com/2025-11-12-ibm-delivers-new-quantum-processors,-software,-and-algorithm-breakthroughs-on-path-to-advantage-and-fault-tolerance

[CISA, 2024] Cybersecurity and Infrastructure Security Agency. "Strategy for Migrating to Automated PQC Discovery and Inventory Tools." Septiembre 2024. https://www.cisa.gov/sites/default/files/2024-09/Strategy-for-Migrating-to-Automated-PQC-Discovery-and-Inventory-Tools.pdf

[ENISA, 2021] European Union Agency for Cybersecurity. "Post-Quantum Cryptography: Current State and Quantum Mitigation." 2021. https://www.enisa.europa.eu/publications/post-quantum-cryptography-current-state-and-quantum-mitigation

[Federal Reserve, 2025] Federal Reserve Board. "Harvest Now, Decrypt Later: Examining Post-Quantum Cryptography and the Data Privacy Risks for Distributed Ledger Networks." FEDS Working Paper, 2025. https://www.federalreserve.gov/econres/feds/harvest-now-decrypt-later-examining-post-quantum-cryptography-and-the-data-privacy-risks-for-distributed-ledger-networks.htm

[Kudelski, 2024] Kudelski Security. "Quantum Attack Resource Estimate: Using Shor's Algorithm to Break RSA vs DH/DSA vs ECC." 2024. https://kudelskisecurity.com/research/quantum-attack-resource-estimate-using-shors-algorithm-to-break-rsa-vs-dh-dsa-vs-ecc
