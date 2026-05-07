# Capitulo 6: Que tan dificil es "dificil"? Complejidad computacional y criptografia

> "La criptografia se sostiene en problemas que suponemos dificiles. Si esa suposicion resulta incorrecta, toda la seguridad de internet se desmorona en un instante."

---

Imagina que te doy el numero 15 y te pido que encuentres sus factores primos. Facil: 3 y 5. Ahora imagina que te doy un numero de 617 digitos. El mejor algoritmo conocido, ejecutandose en todas las computadoras del planeta trabajando juntas, tardaria mas que la edad del universo.

Toda la seguridad de internet descansa sobre esa asimetria.

En los capitulos anteriores hemos usado palabras como "imposible", "irreversible" y "seguro" para describir funciones hash y algoritmos de hashing de contrasenas. Pero la criptografia no promete "imposible". Promete algo mas preciso y mas honesto: **tan dificil que nadie con los recursos del planeta puede hacerlo en un tiempo razonable**.

Esa confianza se basa en la teoria de complejidad computacional --una rama de las ciencias de la computacion que clasifica problemas segun cuantos recursos necesitan para resolverse. Este capitulo conecta esa teoria con las primitivas criptograficas que ya conoces.

---

## 6.1 Complejidad computacional: cuanto cuesta resolver un problema

### 6.1.1 La pregunta fundamental

Cuando un algoritmo recibe una entrada y produce una salida, necesita realizar cierta cantidad de **operaciones**. La complejidad computacional estudia como esa cantidad de operaciones crece cuando crece el tamano de la entrada.

La pregunta no es "cuanto tarda este algoritmo" (eso depende del hardware). La pregunta es: **como escala?**

Veamos un ejemplo concreto:

```python
"""
complejidad_demo.py

Demostracion visual de diferentes complejidades computacionales.
"""

import time


def busqueda_lineal(lista, objetivo):
    """O(n): revisa cada elemento una vez."""
    for i, elemento in enumerate(lista):
        if elemento == objetivo:
            return i
    return -1


def busqueda_binaria(lista_ordenada, objetivo):
    """O(log n): descarta la mitad en cada paso."""
    izq, der = 0, len(lista_ordenada) - 1
    while izq <= der:
        medio = (izq + der) // 2
        if lista_ordenada[medio] == objetivo:
            return medio
        elif lista_ordenada[medio] < objetivo:
            izq = medio + 1
        else:
            der = medio - 1
    return -1


def pares_duplicados(lista):
    """O(n^2): compara cada elemento con todos los demas."""
    duplicados = []
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] == lista[j]:
                duplicados.append(lista[i])
    return duplicados


# Medir como escala cada algoritmo
print("Como escala la complejidad con el tamano de entrada:")
print("-" * 65)
print(f"{'n':>10} {'O(log n)':>12} {'O(n)':>12} {'O(n^2)':>12} {'O(2^n)':>15}")
print("-" * 65)

for n in [10, 100, 1_000, 10_000, 100_000, 1_000_000]:
    log_n = len(bin(n)) - 2  # Aproximacion de log2(n)
    n_ops = n
    n2_ops = n * n
    exp_ops = 2 ** min(n, 40)  # Limitamos para no desbordar

    print(f"{n:>10,} {log_n:>12,} {n_ops:>12,} {n2_ops:>12,} "
          f"{'INFINITO' if n > 40 else f'{exp_ops:>15,}'}")
```

El resultado es revelador:

```
         n     O(log n)         O(n)       O(n^2)          O(2^n)
-----------------------------------------------------------------
        10            3           10          100           1,024
       100            6          100       10,000              --
     1,000            9        1,000    1,000,000              --
    10,000           13       10,000  100,000,000              --
   100,000           16      100,000         --                --
 1,000,000           19    1,000,000         --                --
```

Los espacios marcados con `--` representan numeros tan grandes que no caben en ninguna computadora. A partir de O(n^2) con entradas grandes, el computo se vuelve impracticable. Y O(2^n) explota incluso con entradas pequenas.

### 6.1.2 Notacion Big O

La **notacion Big O** es la herramienta estandar para expresar complejidad. Describe un **limite superior asintotico** --el peor caso de crecimiento cuando la entrada es lo suficientemente grande.

Las reglas son simples:

1. **Se eliminan las constantes**: O(2n) = O(n). O(5n^2) = O(n^2). Las constantes dependen del hardware; la forma de crecimiento no.

2. **Se conserva solo el termino dominante**: O(n^2 + n) = O(n^2). Cuando n es grande, n^2 domina completamente.

3. **Se compara crecimiento, no velocidad absoluta**: un algoritmo O(n) puede ser mas lento que uno O(n^2) para entradas pequenas, pero eventualmente sera mas rapido.

Las complejidades que nos importan en criptografia, de menor a mayor:

```
Complejidad    Nombre           Ejemplo criptografico
-------------------------------------------------------------
O(1)           Constante        Verificar una firma (dada la llave)
O(log n)       Logaritmica      Exponenciacion modular (square-and-multiply)
O(n)           Lineal           Hashear un mensaje de n bytes
O(n^2)         Cuadratica       Multiplicacion de numeros grandes (ingenua)
O(n^3)         Cubica           Algunas operaciones de algebra lineal
O(2^(n^1/3))   Sub-exponencial  Factorizacion (GNFS) -- romper RSA
O(2^(n/2))     Exponencial      Busqueda de colisiones en un hash
O(2^n)         Exponencial      Fuerza bruta contra un cifrado de n bits
```

La frontera critica esta entre **polinomial** (O(n^k) para alguna constante k) y **exponencial** (O(2^n)). Los problemas polinomiales son "faciles" en el sentido de que escalan de manera manejable. Los problemas exponenciales son "dificiles" porque escalan de manera catastrofica.

### 6.1.3 La frontera entre lo posible y lo imposible

Para entender que tan grande es "exponencial", hagamos numeros concretos.

```python
"""
explosion_exponencial.py

Demostracion numerica de por que la complejidad exponencial
hace imposibles los ataques de fuerza bruta contra cifrados modernos.
"""

import time


def calcular_tiempo_ataque(bits_seguridad: int,
                           ops_por_segundo: float,
                           nombre_hardware: str) -> str:
    """
    Calcula cuanto tardaria un ataque de fuerza bruta
    con un nivel dado de seguridad y hardware.
    """
    operaciones = 2 ** bits_seguridad
    segundos = operaciones / ops_por_segundo

    # Convertir a unidades humanas
    minutos = segundos / 60
    horas = minutos / 60
    dias = horas / 24
    anios = dias / 365.25
    edad_universo = 13.8e9  # anios

    if anios < 1:
        tiempo_str = f"{dias:.1f} dias"
    elif anios < 1000:
        tiempo_str = f"{anios:.1f} anios"
    elif anios < 1e9:
        tiempo_str = f"{anios:.2e} anios"
    else:
        veces_universo = anios / edad_universo
        tiempo_str = f"{veces_universo:.1e}x la edad del universo"

    return (f"  {nombre_hardware:>30}: {tiempo_str}")


print("Cuanto tardaria romper diferentes niveles de seguridad?")
print("=" * 70)

# Hardware real (operaciones por segundo)
hardware = [
    (1e9,    "Laptop (1 GHz)"),
    (1e12,   "GPU RTX 4090"),
    (1e18,   "Frontier (supercomp.)"),
    (1e24,   "Toda la Tierra (estimado)"),
]

for bits in [32, 48, 64, 80, 128, 192, 256]:
    print(f"\n{bits} bits de seguridad (2^{bits} = {2**bits:.2e} operaciones):")
    for ops, nombre in hardware:
        print(calcular_tiempo_ataque(bits, ops, nombre))


# Comparacion visual
print("\n\nReferencias fisicas:")
print(f"  Atomos en el universo observable: ~2^266")
print(f"  Segundos desde el Big Bang:       ~2^58")
print(f"  Operaciones de Frontier por ano:  ~2^84")
print(f"  Energia del Sol por ano (julios):  ~2^110")
print()
print("128 bits de seguridad significa:")
print("  Incluso si CADA ATOMO del universo fuera una computadora,")
print("  y cada una hiciera un BILLON de operaciones por segundo,")
print("  desde el Big Bang hasta hoy,")
print(f"  solo habrian completado ~2^{266+40+58} = 2^364 operaciones.")
print(f"  Eso es {2**364 / 2**128:.0e} veces mas de lo necesario...")
print(f"  Espera, eso es suficiente! Pero en la practica, coordinar")
print(f"  esa cantidad de computadoras es fisicamente imposible.")
```

El punto clave es este: **128 bits de seguridad no es una barrera tecnologica que algun dia superaremos con hardware mas rapido. Es una barrera fisica que esta mas alla de los limites de la energia disponible en el universo.**

Duplicar la velocidad del hardware reduce la seguridad en exactamente un bit. Para reducir 128 bits de seguridad a algo manejable, necesitarias un aceleramiento de 2^80 --un factor de un cuatrillon de cuatrillones. Las leyes de la fisica no lo permiten.

---

## 6.2 Clases de complejidad: P, NP y el misterio del millon de dolares

### 6.2.1 La clase P: problemas con solucion eficiente

La clase **P** (Polynomial) contiene todos los problemas que se pueden resolver en tiempo polinomial --es decir, en O(n^k) para alguna constante k. En terminos practicos, estos son los problemas "faciles": existe un algoritmo eficiente que los resuelve.

Ejemplos:
- **Ordenar una lista**: O(n log n) con mergesort.
- **Busqueda binaria**: O(log n).
- **Multiplicar dos numeros**: O(n^2) con el algoritmo ingenuo, O(n log n) con algoritmos avanzados.
- **Verificar si un numero es primo**: O(n^6) con el algoritmo AKS [Agrawal, Kayal y Saxena, 2002]. El exponente es grande, pero es polinomial.

En criptografia, las operaciones **legitimas** deben estar en P: cifrar, descifrar, hashear, firmar y verificar deben ser eficientes. Si cifrar un mensaje tardara mil anos, nadie usaria criptografia.

### 6.2.2 La clase NP: facil de verificar, dificil de encontrar

La clase **NP** (Nondeterministic Polynomial) contiene los problemas cuya solucion se puede **verificar** en tiempo polinomial, aunque **encontrar** la solucion puede ser mucho mas dificil.

La definicion formal involucra maquinas de Turing no deterministas (NTM), que son un modelo teorico de computacion donde la maquina puede "adivinar" entre multiples caminos de ejecucion. Una NTM no es una computadora real --no existe hardware que funcione asi. Es una construccion matematica que nos permite razonar sobre problemas.

Una maquina de Turing no determinista se puede entender como una maquina que, en cada paso de su ejecucion, puede "bifurcarse" y explorar multiples caminos simultaneamente. Si **algun** camino lleva a una solucion, el problema es resoluble por la NTM. En la practica, simular una NTM en una computadora real requiere explorar todos los caminos posibles, lo que toma tiempo exponencial [Rabin y Scott, 1959; Turing, 1936].

Las siglas NP significan "Nondeterministic Polynomial": una NTM puede resolver el problema en tiempo polinomial, porque hay al menos un camino que llega a la solucion rapidamente. El problema es saber **cual** camino.

El ejemplo criptografico mas claro es la busqueda de llaves:

```python
"""
np_criptografia.py

La asimetria P/NP en la criptografia:
encontrar una llave es dificil, verificarla es facil.
"""

import hashlib
import time
import os

# --- Ejemplo: buscar una llave AES por fuerza bruta ---
# (version simplificada con espacio de llaves reducido)

def cifrar_simple(mensaje: bytes, llave: int) -> bytes:
    """Cifrado XOR simple para demostracion (NO usar en produccion)."""
    llave_bytes = llave.to_bytes(3, 'big')  # Solo 24 bits para demo
    return bytes(m ^ llave_bytes[i % 3] for i, m in enumerate(mensaje))


def verificar_llave(texto_cifrado: bytes, llave: int,
                    texto_plano_esperado: bytes) -> bool:
    """
    Verificar una llave: O(n) -- FACIL (esta en P).
    Solo necesitas descifrar y comparar.
    """
    descifrado = cifrar_simple(texto_cifrado, llave)
    return descifrado == texto_plano_esperado


# Configuracion
texto_plano = b"mensaje secreto!"
llave_real = 0xABCDEF  # 24 bits
texto_cifrado = cifrar_simple(texto_plano, llave_real)

# VERIFICAR es rapido (P)
inicio = time.time()
assert verificar_llave(texto_cifrado, llave_real, texto_plano)
t_verificar = time.time() - inicio
print(f"Verificar una llave: {t_verificar*1e6:.1f} microsegundos")

# ENCONTRAR es lento (exponencial en el numero de bits)
print(f"\nBuscando la llave por fuerza bruta (24 bits = {2**24:,} posibilidades)...")
inicio = time.time()
for llave_candidata in range(2**24):
    if verificar_llave(texto_cifrado, llave_candidata, texto_plano):
        t_buscar = time.time() - inicio
        print(f"Llave encontrada: 0x{llave_candidata:06X}")
        print(f"Tiempo de busqueda: {t_buscar:.2f} segundos")
        print(f"Intentos: {llave_candidata + 1:,}")
        break

print(f"\nFactor de dificultad: buscar es {t_buscar/t_verificar:.0f}x "
      f"mas lento que verificar")
print(f"\nCon AES-128 (128 bits), el espacio seria 2^128 = {2**128:.2e}")
print(f"Eso es {2**128 / 2**24:.2e}x mas grande que nuestro ejemplo")
```

Esta asimetria --verificar es facil, encontrar es dificil-- es exactamente lo que la criptografia necesita:

- **Cifrar/descifrar con la llave correcta**: rapido (P).
- **Encontrar la llave sin conocerla**: lento (probablemente no esta en P).

### 6.2.3 NP-Completo y NP-Duro

Dentro de NP existen problemas especiales llamados **NP-Completos** (NP-Complete). Estos son los problemas "mas dificiles" de NP, con una propiedad extraordinaria: si encontraras un algoritmo eficiente (polinomial) para resolver **cualquiera** de ellos, podrias resolver **todos** los problemas de NP eficientemente.

Los problemas NP-Completos incluyen:

- **SAT** (satisfactibilidad booleana): dada una formula logica, existe una asignacion de valores que la haga verdadera? Fue el primer problema demostrado NP-Completo [Cook, 1971].
- **El problema del viajante**: cual es la ruta mas corta que visita todas las ciudades exactamente una vez?
- **Coloracion de grafos**: se puede colorear un grafo con k colores sin que dos nodos adyacentes tengan el mismo color?

Los problemas **NP-Duros** (NP-Hard) son al menos tan dificiles como los NP-Completos, pero no necesariamente estan en NP (sus soluciones pueden no ser verificables en tiempo polinomial).

Seria ideal que la criptografia se basara en problemas NP-Completos, porque eso garantizaria que romperlos es tan dificil como resolver cualquier otro problema NP. Pero en la practica, los problemas criptograficos no son NP-Completos --son problemas que **creemos** dificiles basandonos en decadas de intentos fallidos de resolverlos, pero sin una prueba formal de su dificultad.

### 6.2.4 P vs NP: el misterio del millon de dolares

La pregunta **P = NP?** pregunta: todo problema cuya solucion es facil de verificar, es tambien facil de resolver?

Si **P = NP**, significaria que para cada problema donde puedes verificar una respuesta rapidamente, existe un algoritmo eficiente para encontrar esa respuesta. Las consecuencias para la criptografia serian catastroficas:

- Encontrar una llave de cifrado seria tan facil como verificarla.
- Factorizar numeros grandes seria eficiente.
- Las firmas digitales podrian ser falsificadas.
- Toda la infraestructura de seguridad de internet colapsaria.

Si **P != NP** (lo que la mayoria cree), entonces existen problemas fundamentalmente dificiles de resolver, y la criptografia tiene una base solida.

El estado actual: **nadie ha podido probar ni P = NP ni P != NP** en mas de 50 anos. El Instituto Clay lo incluye como uno de los siete Problemas del Milenio, con un premio de un millon de dolares. En una encuesta de 2019 entre expertos en teoria de la complejidad, el 99% creia que P != NP [Gasarch, 2019].

Pero "creer" no es "saber". Toda la criptografia descansa sobre una conjetura --la mas fuerte y mejor respaldada de la ciencia de la computacion, pero una conjetura al fin.

```
La jerarquia de complejidad (como la entendemos):

+-----------------------------------------------+
|                                               |
|                  NP-Hard                      |
|                                               |
|  +------------------------------------------+|
|  |                                          ||
|  |              NP-Complete                 ||
|  |          (SAT, viajante, etc.)           ||
|  |                                          ||
|  +------------------+-----------------------+|
|  |                  |                        |
|  |    NP            |                        |
|  |  (verificar      |   Problemas            |
|  |   es facil)      |   criptograficos:       |
|  |                  |   factorizacion,        |
|  |  +--------+      |   log. discreto,       |
|  |  |        |      |   LWE                   |
|  |  |   P    |      |                        |
|  |  |(resolver|      |   (creemos que estan   |
|  |  | es     |      |    fuera de P, pero    |
|  |  | facil) |      |    no lo hemos probado) |
|  |  +--------+      |                        |
|  +------------------+------------------------+|
+-----------------------------------------------+

Si P = NP, el circulo interno se expande y todo colapsa.
```

---

## 6.3 Funciones de un solo sentido: la base de la criptografia

### 6.3.1 Definicion intuitiva

Una **funcion de un solo sentido** (one-way function) es una funcion que es facil de calcular pero dificil de invertir. En terminos formales:

- **Facil de calcular**: dado x, calcular f(x) toma tiempo polinomial.
- **Dificil de invertir**: dado y = f(x), encontrar cualquier x' tal que f(x') = y toma tiempo super-polinomial (para la inmensa mayoria de las entradas).

Las funciones hash son el ejemplo mas directo: dado un mensaje, calcular su hash es rapido. Pero dado un hash, encontrar un mensaje que lo produzca es computacionalmente inviable (resistencia a preimagen).

### 6.3.2 Funciones de un solo sentido con trampa

Las **funciones de un solo sentido con trampa** (trapdoor one-way functions) agregan un elemento crucial: existe un "secreto" (la trampa) que hace que la inversion sea facil para quien lo conoce.

Este es exactamente el modelo de la criptografia de llave publica:

- **Sin la trampa** (llave privada): invertir la funcion es computacionalmente imposible.
- **Con la trampa** (llave privada): invertir la funcion es trivial.

```python
"""
funcion_trampa_demo.py

Demostracion de funcion de un solo sentido con trampa
usando RSA simplificado con numeros pequenos.
"""


def exponenciacion_modular(base, exponente, modulo):
    """Calcula base^exponente mod modulo de forma eficiente."""
    return pow(base, exponente, modulo)


# --- RSA simplificado ---
# (numeros pequenos para demostracion; en produccion serian de 2048+ bits)

# Generacion de llaves
p = 61      # Primo 1
q = 53      # Primo 2
n = p * q   # n = 3233 (modulo publico)
phi = (p - 1) * (q - 1)  # phi(n) = 3120

e = 17      # Exponente publico (coprimo con phi)
d = pow(e, -1, phi)  # Exponente privado (inverso modular)

print("RSA simplificado como funcion de un solo sentido con trampa")
print("=" * 60)
print(f"  Llave publica:  (e={e}, n={n})")
print(f"  Llave privada:  (d={d}, n={n})")
print(f"  Primos secretos: p={p}, q={q}")
print()

# Cifrar (facil: cualquiera con la llave publica)
mensaje = 42
cifrado = exponenciacion_modular(mensaje, e, n)
print(f"Cifrar (facil, llave publica):")
print(f"  mensaje^e mod n = {mensaje}^{e} mod {n} = {cifrado}")

# Descifrar CON trampa (facil: solo con la llave privada)
descifrado = exponenciacion_modular(cifrado, d, n)
print(f"\nDescifrar CON trampa (facil, llave privada):")
print(f"  cifrado^d mod n = {cifrado}^{d} mod {n} = {descifrado}")

# Descifrar SIN trampa (dificil: necesitarias factorizar n)
print(f"\nDescifrar SIN trampa (dificil):")
print(f"  Necesitas encontrar d, que requiere conocer phi(n).")
print(f"  phi(n) = (p-1)(q-1), que requiere factorizar n={n}.")
print(f"  Para n={n}, factorizar es trivial.")
print(f"  Para n de 617 digitos (RSA-2048), factorizar es imposible.")
print()

# La asimetria
print("La asimetria fundamental:")
print(f"  Multiplicar p*q:     {p} * {q} = {n}  (instantaneo)")
print(f"  Factorizar n:        {n} = ? * ?       (trivial aqui, ")
print(f"                       imposible con 2048 bits)")
```

### 6.3.3 Existencia de funciones de un solo sentido

He aqui un dato que deberia incomodar a cualquier desarrollador que dependa de la criptografia: **no sabemos si las funciones de un solo sentido existen**.

La existencia de funciones de un solo sentido es una conjetura abierta. Si existieran, implicaria que P != NP (porque una funcion facil de calcular pero imposible de invertir eficientemente significaria que ciertos problemas de NP no estan en P). Pero la implicacion no funciona al reves: que P != NP no garantiza que existan funciones de un solo sentido.

Investigacion reciente de Shuichi Hirahara y otros ha establecido conexiones fascinantes entre la existencia de funciones de un solo sentido y la dureza de ciertos problemas de meta-complejidad --problemas sobre la complejidad de otros problemas [Hirahara, 2023; Hirahara y Lu, 2024]. Especificamente, demostraron que una funcion de un solo sentido existe si y solo si es NP-dificil aproximar la complejidad de Kolmogorov distribucional bajo reducciones aleatorizadas de tiempo polinomial.

En la practica, esto es menos aterrador de lo que suena. Tenemos candidatos concretos a funciones de un solo sentido --factorizacion, logaritmo discreto, problemas de reticulas-- que han resistido decadas de ataques intensivos. No podemos **probar** que son de un solo sentido, pero la evidencia empirica es abrumadora.

---

## 6.4 Problemas dificiles que sostienen la criptografia

### 6.4.1 Factorizacion de enteros

La **factorizacion de enteros** es el problema de, dado un numero compuesto N, encontrar sus factores primos. Es la base de la seguridad de **RSA**, el criptosistema de llave publica mas ampliamente desplegado en la historia.

La asimetria es dramatica:

- **Multiplicar** dos primos de 1024 bits: nanosegundos.
- **Factorizar** su producto: el mejor algoritmo conocido (General Number Field Sieve, GNFS) tiene complejidad sub-exponencial: O(exp(c * n^(1/3) * (log n)^(2/3))), donde n es el numero de bits del numero.

```python
"""
factorizacion_demo.py

Demostracion de la dificultad de factorizar
numeros de tamano creciente.
"""

import time
import math


def factorizar_ingenuo(n: int) -> list[int]:
    """
    Factorizacion por division de prueba.
    Complejidad: O(sqrt(n)) = O(2^(bits/2))

    Para numeros grandes, existen algoritmos mejores
    (Pollard's rho, ECM, GNFS), pero todos son
    super-polinomiales en el numero de bits.
    """
    factores = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factores.append(d)
            n //= d
        d += 1
    if n > 1:
        factores.append(n)
    return factores


def generar_semiprimo(bits: int) -> tuple[int, int, int]:
    """Genera un semiprimo (producto de dos primos) de aprox. bits bits."""
    from random import getrandbits
    from sympy import nextprime

    p = nextprime(getrandbits(bits // 2))
    q = nextprime(getrandbits(bits // 2))
    return p * q, p, q


# Medir el crecimiento del tiempo de factorizacion
print("Tiempo de factorizacion vs tamano del numero:")
print("=" * 60)
print(f"{'Digitos':>8} {'Bits':>6} {'Tiempo':>12} {'Factores'}")
print("-" * 60)

# Numeros semiprimos (producto de dos primos) de tamano creciente
import random
random.seed(42)

from sympy import nextprime

for digitos in [6, 8, 10, 12, 14, 16, 18, 20]:
    bits_aprox = int(digitos * 3.32)  # log2(10)
    mitad = bits_aprox // 2

    p = nextprime(random.getrandbits(mitad))
    q = nextprime(random.getrandbits(mitad))
    n = p * q

    inicio = time.time()
    factores = factorizar_ingenuo(n)
    duracion = time.time() - inicio

    print(f"{len(str(n)):>8} {n.bit_length():>6} {duracion:>11.6f}s "
          f"{' x '.join(str(f) for f in factores)}")

print()
print("Observa como el tiempo crece EXPONENCIALMENTE con los digitos.")
print()

# Extrapolacion para tamanos criptograficos
print("Extrapolacion para tamanos criptograficos (GNFS):")
print("-" * 60)

def tiempo_gnfs_estimado(bits: int) -> float:
    """
    Estima el tiempo de factorizacion con GNFS.
    Complejidad: exp(c * n^(1/3) * (ln n)^(2/3))
    donde c ≈ 1.923 y n es el numero de bits.

    Calibramos con RSA-250 (829 bits), factorizado en ~2700 anos-nucleo (2020).
    """
    c = 1.923
    n = bits * math.log(2)  # Convertir bits a valor de ln(N)

    # Valor de la funcion L para n bits
    L = math.exp(c * (n ** (1/3)) * (math.log(n) ** (2/3)))

    # Calibrar con RSA-250: 829 bits, ~2700 anos-nucleo
    L_ref = math.exp(c * ((829 * math.log(2)) ** (1/3)) *
                     (math.log(829 * math.log(2)) ** (2/3)))
    anos_nucleo_ref = 2700

    return anos_nucleo_ref * (L / L_ref)

for bits in [512, 768, 1024, 2048, 3072, 4096]:
    anos = tiempo_gnfs_estimado(bits)
    if anos < 1:
        tiempo_str = f"{anos * 365.25:.1f} dias-nucleo"
    elif anos < 1e6:
        tiempo_str = f"{anos:.0f} anos-nucleo"
    elif anos < 1e15:
        tiempo_str = f"{anos:.2e} anos-nucleo"
    else:
        tiempo_str = f"{anos/1.38e10:.1e}x edad del universo"

    seguridad = "INSEGURO" if anos < 1e6 else "SEGURO" if anos < 1e30 else "MUY SEGURO"
    print(f"  RSA-{bits:>4}: {tiempo_str:>30}  [{seguridad}]")
```

**El record actual**: en 2020, un equipo internacional factorizo RSA-250, un numero de 829 bits (250 digitos decimales), usando aproximadamente 2,700 anos-nucleo de computo. RSA-2048 (617 digitos) esta completamente fuera de alcance con la tecnologia actual.

### 6.4.2 El logaritmo discreto

El **problema del logaritmo discreto** es: dado un grupo ciclico con generador g, un modulo primo p, y un valor y, encontrar x tal que g^x mod p = y.

Es la base de seguridad de:
- **Diffie-Hellman** (intercambio de llaves)
- **DSA** (firmas digitales)
- **ElGamal** (cifrado)

La asimetria es la misma que en factorizacion:

```python
"""
logaritmo_discreto_demo.py

La exponenciacion modular es facil.
El logaritmo discreto es dificil.
"""

import time
import random

# Parametros (pequenos para demostracion)
p = 104729  # Un primo
g = 2       # Generador

# --- Direccion facil: exponenciacion modular ---
x_secreto = random.randint(2, p - 2)

inicio = time.time()
y = pow(g, x_secreto, p)  # g^x mod p
t_exp = time.time() - inicio

print("Exponenciacion modular (FACIL):")
print(f"  g^x mod p = {g}^{x_secreto} mod {p} = {y}")
print(f"  Tiempo: {t_exp*1e6:.1f} microsegundos")

# --- Direccion dificil: logaritmo discreto (fuerza bruta) ---
print(f"\nLogaritmo discreto por fuerza bruta (DIFICIL):")
print(f"  Dado g={g}, p={p}, y={y}, encontrar x tal que g^x = y mod p")

inicio = time.time()
for x_candidato in range(1, p):
    if pow(g, x_candidato, p) == y:
        t_log = time.time() - inicio
        print(f"  x encontrado: {x_candidato}")
        print(f"  Tiempo: {t_log:.3f} segundos")
        print(f"  Intentos: {x_candidato:,}")
        break

print(f"\nFactor de dificultad: {t_log/t_exp:.0f}x")
print(f"\nCon p de 2048 bits, la fuerza bruta requeriria ~2^2048 intentos.")
print(f"El mejor algoritmo (index calculus) es sub-exponencial,")
print(f"similar en complejidad a GNFS para factorizacion.")
```

El logaritmo discreto y la factorizacion tienen complejidades similares con los mejores algoritmos conocidos. Ambos son sub-exponenciales, y los avances en uno tipicamente se traducen en avances en el otro.

### 6.4.3 El logaritmo discreto en curvas elipticas

En el Capitulo 2 vimos que las curvas elipticas definen un grupo donde se puede hacer "multiplicacion escalar": dado un punto G en la curva y un escalar k, calcular k*G es eficiente. Pero dado G y k*G, encontrar k es el **problema del logaritmo discreto en curvas elipticas** (ECDLP).

La diferencia critica con el logaritmo discreto clasico es que **no existe un algoritmo sub-exponencial conocido** para ECDLP. El mejor algoritmo conocido es Pollard's rho, con complejidad O(2^(n/2)) donde n es el tamano del grupo.

Esto tiene una consecuencia practica enorme:

```
Seguridad equivalente:

Nivel de    RSA (bits    ECC (bits    Ratio
seguridad   del modulo)  de la curva)
--------    -----------  -----------  -----
80 bits     1024         160          6.4:1
112 bits    2048         224          9.1:1
128 bits    3072         256          12:1
192 bits    7680         384          20:1
256 bits    15360        512          30:1
```

Una llave ECC de 256 bits proporciona la misma seguridad que una llave RSA de 3072 bits. Esto significa llaves mas pequenas, firmas mas pequenas, y operaciones mas rapidas. Es la razon por la que la criptografia moderna esta migrando de RSA a curvas elipticas (Ed25519, P-256, X25519).

### 6.4.4 Learning With Errors (LWE): el problema post-cuantico

Los tres problemas anteriores --factorizacion, logaritmo discreto, ECDLP-- comparten una vulnerabilidad: el **algoritmo de Shor** puede resolverlos en tiempo polinomial en una computadora cuantica suficientemente grande [Shor, 1994]. Cuando (no si) las computadoras cuanticas de gran escala existan, RSA y ECC dejaran de ser seguros.

El problema **Learning With Errors** (LWE) es la base de la criptografia post-cuantica. Funciona asi:

1. Toma un sistema de ecuaciones lineales: A * s = b (mod q)
2. Agrega "ruido" aleatorio a cada ecuacion: A * s + e = b (mod q)
3. El problema: dado A y b, encontrar s

Sin ruido, resolver el sistema es trivial (eliminacion gaussiana, O(n^3)). Con ruido, el problema se vuelve extremadamente dificil --y no se conoce ningun algoritmo cuantico eficiente para resolverlo.

LWE es la base de:
- **ML-KEM** (antes CRYSTALS-Kyber): intercambio de llaves post-cuantico, estandarizado por NIST en 2024.
- **ML-DSA** (antes CRYSTALS-Dilithium): firmas digitales post-cuanticas.

Veremos mas sobre criptografia post-cuantica en el Capitulo 13.

---

## 6.5 Bits de seguridad: la metrica universal

### 6.5.1 Que significa "128 bits de seguridad"

Cuando decimos que un algoritmo tiene **n bits de seguridad**, significa que el mejor ataque conocido requiere aproximadamente 2^n operaciones.

Esta es la metrica que unifica todos los algoritmos criptograficos, independientemente de como funcionan internamente. Permite comparar manzanas con naranjas:

```
Algoritmo            Tipo                Bits de seguridad
----------------------------------------------------------------
AES-128              Cifrado simetrico   128 (fuerza bruta)
AES-256              Cifrado simetrico   256 (fuerza bruta)
SHA-256              Hash (colision)     128 (paradoja cumpleanos)
SHA-256              Hash (preimagen)    256
SHA-3-256            Hash (colision)     128
SHA-3-256            Hash (preimagen)    256
RSA-2048             Cifrado asimetrico  112 (GNFS)
RSA-3072             Cifrado asimetrico  128 (GNFS)
ECDSA P-256          Firma digital       128 (Pollard's rho)
Ed25519              Firma digital       128 (Pollard's rho)
ML-KEM-768           KEM post-cuantico   192 (mejor ataque conocido)
Argon2id (19MiB,t=2) Hash de password    ~depende del atacante~
```

Nota que SHA-256 tiene 256 bits de seguridad contra preimagen pero solo 128 contra colision. La diferencia se debe a la **paradoja del cumpleanos**: para encontrar una colision (dos entradas cualesquiera con el mismo hash), necesitas solo 2^(n/2) intentos, no 2^n.

### 6.5.2 El principio del eslabon mas debil

La seguridad de un sistema criptografico es la de su **componente mas debil**.

```python
"""
eslabon_debil.py

Demostracion del principio del eslabon mas debil.
"""

# Un sistema tipico de TLS usa:
componentes = {
    "AES-256":         256,  # Cifrado simetrico
    "SHA-384":         192,  # Hash para MAC (seguridad contra colision)
    "ECDHE P-384":     192,  # Intercambio de llaves
    "RSA-2048 (cert)": 112,  # Certificado del servidor
}

print("Seguridad de un sistema TLS tipico:")
print("=" * 50)

for nombre, bits in componentes.items():
    barra = "#" * (bits // 8)
    print(f"  {nombre:>20}: {bits:>3} bits  {barra}")

min_bits = min(componentes.values())
componente_debil = [k for k, v in componentes.items() if v == min_bits][0]

print(f"\nSeguridad del sistema: {min_bits} bits")
print(f"Eslabon mas debil: {componente_debil}")
print(f"\nNo importa que AES-256 tenga 256 bits si el certificado")
print(f"RSA-2048 solo proporciona 112 bits de seguridad.")
```

Este principio tiene implicaciones practicas:
- No tiene sentido usar AES-256 si tus llaves se derivan de contrasenas debiles.
- No tiene sentido usar Ed25519 (128 bits) con SHA-512 (256 bits de preimagen) si tu RSA-2048 solo da 112 bits.
- La seguridad real se mide por el componente mas fragil, no por el mas fuerte.

### 6.5.3 Recomendaciones del NIST para 2026-2030

El NIST proporciona guias claras sobre niveles de seguridad minimos [NIST SP 800-57, 2020]:

```
Periodo de proteccion     Bits minimos    Algoritmos recomendados
--------------------------------------------------------------------
Hasta 2030                112             RSA-2048, P-224, AES-128
Hasta 2030 (recomendado)  128             RSA-3072, P-256, AES-128
Mas alla de 2030          192             RSA-7680, P-384, AES-192
Proteccion a largo plazo  256             RSA-15360, P-521, AES-256
Post-cuantico             128+            ML-KEM-768, ML-DSA-65
```

La recomendacion practica para 2026: **apunta a 128 bits de seguridad como minimo**, 256 bits si necesitas proteccion a largo plazo (datos que deben permanecer confidenciales por decadas). Y empieza a planificar la migracion a criptografia post-cuantica.

---

## 6.6 Reducciones: como probamos seguridad relativa

### 6.6.1 La idea de una reduccion

No podemos probar que un algoritmo criptografico es "seguro" en terminos absolutos --eso requeriria probar que P != NP, que no hemos logrado. Lo que si podemos hacer es probar que **romper el algoritmo es al menos tan dificil como resolver un problema que creemos dificil**.

Esto se llama una **reduccion de seguridad** y funciona asi:

1. Supongamos que existe un atacante A que puede romper el algoritmo X eficientemente.
2. Demostramos que podemos usar a A como "caja negra" para resolver el problema dificil Y.
3. Conclusion: si Y es dificil, entonces X es seguro.

Formalmente: "Si puedes romper X, entonces puedes resolver Y". La contrapositiva: "Si Y es dificil, entonces X es seguro".

```
Reduccion de seguridad (ejemplo RSA):

"Si puedes descifrar RSA eficientemente,
 entonces puedes factorizar eficientemente."

Equivalente a:
"Si factorizar es dificil,
 entonces RSA es seguro."

En la practica:
  Nadie ha podido factorizar numeros grandes en 40+ anos.
  --> Confiamos en que RSA es seguro (para numeros suficientemente grandes).
```

### 6.6.2 Reducciones en la practica

Algunos ejemplos de reducciones que sostienen algoritmos reales:

- **RSA**: su seguridad se reduce al problema de factorizacion. Mas precisamente, al "RSA problem" (calcular raices e-esimas modulo N compuesto), que se cree equivalente a factorizar.

- **Diffie-Hellman**: su seguridad se reduce al "Computational Diffie-Hellman problem" (CDH), que se reduce al problema del logaritmo discreto.

- **Argon2**: su seguridad contra ataques de trade-off tiempo-memoria se prueba mediante reducciones a problemas de grafos de acceso a memoria.

- **ML-KEM** (post-cuantico): su seguridad se reduce al problema "Module Learning With Errors", que se reduce a problemas de reticulas que se creen dificiles incluso para computadoras cuanticas.

Las reducciones no son perfectas. Pueden tener "perdidas" (la reduccion puede ser menos eficiente que el ataque original), y siempre dependen de la suposicion de que el problema subyacente es dificil. Pero son lo mejor que tenemos, y han demostrado ser notablemente confiables en la practica.

---

## 6.7 Conexion con lo que ya sabemos

### 6.7.1 Hashes y complejidad

Los hashes que vimos en los Capitulos 1, 3 y 4 dependen de la dificultad de encontrar preimagen y colisiones:

- **Resistencia a preimagen** de SHA-256: requiere ~2^256 operaciones. Esto es seguro incluso contra avances algoritmicos significativos.
- **Resistencia a colision** de SHA-256: requiere ~2^128 operaciones (paradoja del cumpleanos). Sigue siendo seguro, pero con menor margen.
- **SHA-3**: ademas de la seguridad numerica, su construccion de esponja proporciona propiedades estructurales que Merkle-Damgard no tiene (inmunidad a extension de longitud).

### 6.7.2 Hashing de contrasenas y complejidad

Los algoritmos del Capitulo 5 agregan una dimension diferente a la complejidad: la complejidad **por operacion**. Argon2id no cambia la clase de complejidad del ataque (sigue siendo exponencial en la entropia de la contrasena), pero cambia la **constante** de cada operacion de nanosegundos a milisegundos. Esto se traduce en un factor de ~10^7 en tiempo total de ataque.

```python
"""
conexion_complejidad.py

Como los bits de seguridad se conectan con
los algoritmos que ya conocemos.
"""

import math


def tiempo_ataque(bits_entropia: int, tiempo_por_intento_seg: float,
                  nombre: str) -> str:
    """Calcula el tiempo estimado de un ataque de fuerza bruta."""
    intentos = 2 ** bits_entropia
    segundos = intentos * tiempo_por_intento_seg
    anios = segundos / (365.25 * 24 * 3600)

    if anios < 0.001:
        return f"{nombre}: {segundos:.2f} segundos"
    elif anios < 1:
        return f"{nombre}: {anios*365.25:.1f} dias"
    elif anios < 1e6:
        return f"{nombre}: {anios:,.0f} anios"
    else:
        return f"{nombre}: {anios:.2e} anios"


print("Cuanto cuesta atacar una contrasena de 40 bits de entropia?")
print("(~8 caracteres aleatorios minusculas)")
print("=" * 55)

# 40 bits de entropia = ~1 billon de posibilidades
bits = 40

# Tiempos por intento para diferentes algoritmos
algoritmos = [
    (1 / 22e9,    "SHA-256 (GPU)"),          # 22 mil millones/seg
    (1 / 33e3,    "bcrypt cost=12 (GPU)"),    # 33 mil/seg
    (1 / 2.8e3,   "scrypt (GPU)"),            # 2,800/seg
    (1 / 1e3,     "Argon2id 19MiB (GPU)"),    # 1,000/seg
]

for tiempo_intento, nombre in algoritmos:
    print(f"  {tiempo_ataque(bits, tiempo_intento, nombre)}")

print()
print("Con 60 bits de entropia (~10 caracteres alfanumericos):")
bits = 60
for tiempo_intento, nombre in algoritmos:
    print(f"  {tiempo_ataque(bits, tiempo_intento, nombre)}")

print()
print("Leccion: Argon2id no cambia la complejidad (sigue siendo O(2^n)),")
print("pero multiplica el costo por intento por ~22,000,000x vs SHA-256.")
print("Esto convierte ataques viables en ataques imposibles en la practica.")
```

---

## 6.8 Ejercicio integrador: la economia de romper criptografia

```python
#!/usr/bin/env python3
"""
ejercicio_capitulo_06.py

Ejercicio: Mide experimentalmente la complejidad de factorizar
numeros de tamano creciente y extrapola para tamanos criptograficos.

Requisitos: pip install sympy matplotlib

Instrucciones:
1. Ejecuta el benchmark de factorizacion
2. Grafica el crecimiento (si matplotlib esta disponible)
3. Extrapola para tamanos criptograficos
4. Compara con fuerza bruta contra AES
5. Calcula costos usando la supercomputadora Frontier
"""

import time
import math
import random


# --- PARTE 1: Factorizacion experimental ---

def factorizar_prueba(n: int) -> list[int]:
    """Factorizacion por division de prueba."""
    factores = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factores.append(d)
            n //= d
        d += 1
    if n > 1:
        factores.append(n)
    return factores


def generar_semiprimo(bits: int) -> int:
    """Genera un numero que es producto de dos primos."""
    from sympy import nextprime
    p = nextprime(random.getrandbits(bits // 2))
    q = nextprime(random.getrandbits(bits // 2))
    return p * q


print("PARTE 1: Benchmark de factorizacion")
print("=" * 60)

resultados = []
try:
    from sympy import nextprime

    for bits in [16, 20, 24, 28, 32, 36, 40, 44, 48]:
        n = generar_semiprimo(bits)
        digitos = len(str(n))

        inicio = time.time()
        factores = factorizar_prueba(n)
        duracion = time.time() - inicio

        resultados.append((bits, digitos, duracion))
        print(f"  {bits:>3} bits ({digitos:>2} digitos): "
              f"{duracion:>10.6f}s  "
              f"{'x'.join(str(f) for f in factores)}")

except ImportError:
    print("  (sympy no disponible, usando numeros fijos)")

    numeros_prueba = [
        (143, 8),           # 11 * 13
        (10403, 14),        # 101 * 103
        (1018081, 20),      # 1009 * 1009
        (100140049, 27),    # 10007 * 10007
        (10000600009, 34),  # 100003 * 100003
    ]

    for n, bits_aprox in numeros_prueba:
        inicio = time.time()
        factores = factorizar_prueba(n)
        duracion = time.time() - inicio
        resultados.append((bits_aprox, len(str(n)), duracion))
        print(f"  ~{bits_aprox:>3} bits ({len(str(n)):>2} digitos): "
              f"{duracion:>10.6f}s  "
              f"{'x'.join(str(f) for f in factores)}")


# --- PARTE 2: Grafica (opcional) ---

print("\nPARTE 2: Visualizacion del crecimiento")
print("=" * 60)

try:
    import matplotlib.pyplot as plt

    bits_list = [r[0] for r in resultados]
    tiempos = [r[2] for r in resultados]

    plt.figure(figsize=(10, 6))
    plt.semilogy(bits_list, tiempos, 'bo-', markersize=8)
    plt.xlabel('Bits del numero')
    plt.ylabel('Tiempo de factorizacion (segundos, escala log)')
    plt.title('Crecimiento del tiempo de factorizacion')
    plt.grid(True, alpha=0.3)
    plt.savefig('factorizacion_benchmark.png', dpi=150, bbox_inches='tight')
    print("  Grafica guardada en factorizacion_benchmark.png")

except ImportError:
    print("  (matplotlib no disponible, omitiendo grafica)")
    print("  Instala con: pip install matplotlib")


# --- PARTE 3: Extrapolacion ---

print("\nPARTE 3: Extrapolacion a tamanos criptograficos")
print("=" * 60)

# Frontier: 1.194 exaflops = ~1.194 * 10^18 operaciones/seg
frontier_ops = 1.194e18
costo_frontier_hora = 500  # USD/hora estimado

print("\nCon la supercomputadora Frontier (1.194 ExaFLOPS):")
print()

for nombre, operaciones, desc in [
    ("AES-128",        2**128,     "fuerza bruta"),
    ("AES-256",        2**256,     "fuerza bruta"),
    ("SHA-256 colision", 2**128,   "paradoja cumpleanos"),
    ("RSA-1024",       2**80,      "GNFS estimado"),
    ("RSA-2048",       2**112,     "GNFS estimado"),
    ("RSA-4096",       2**152,     "GNFS estimado"),
    ("ECDSA P-256",    2**128,     "Pollard's rho"),
]:
    segundos = operaciones / frontier_ops
    anios = segundos / (365.25 * 24 * 3600)
    costo = (segundos / 3600) * costo_frontier_hora

    if anios < 1:
        tiempo = f"{anios * 365.25:.1f} dias"
    elif anios < 1e6:
        tiempo = f"{anios:,.0f} anios"
    elif anios < 1e15:
        tiempo = f"{anios:.2e} anios"
    else:
        universos = anios / 1.38e10
        tiempo = f"{universos:.1e}x edad universo"

    if costo < 1e6:
        costo_str = f"${costo:,.0f}"
    elif costo < 1e15:
        costo_str = f"${costo:.2e}"
    else:
        costo_str = f"${costo:.1e}"

    print(f"  {nombre:>17} ({desc:>22}): {tiempo:>25}  {costo_str}")


# --- PARTE 4: Comparacion practica ---

print("\n\nPARTE 4: Que nivel de seguridad necesitas?")
print("=" * 60)

print("""
Nivel        Protege contra              Ejemplo de uso
------       --------------------------  -------------------------
64 bits      Atacante casual, horas      Datos temporales
80 bits      Atacante motivado, meses    Datos de corta vida
112 bits     Estado-nacion, anos         Estandar minimo NIST
128 bits     Cualquiera, > edad universo Recomendado para 2026+
192 bits     Post-cuantico parcial       Datos sensibles a largo plazo
256 bits     Cuantico completo           Maxima seguridad disponible

Recomendacion practica:
  - Usa 128 bits como MINIMO para cualquier sistema nuevo.
  - Usa 256 bits si los datos deben ser confidenciales por > 10 anios.
  - Comienza la migracion a criptografia post-cuantica (ML-KEM, ML-DSA).
""")
```

---

## 6.9 Resumen del capitulo

La criptografia no promete seguridad absoluta. Promete seguridad **computacional**: los mejores ataques conocidos requieren tantos recursos que son fisicamente imposibles de ejecutar.

Las ideas centrales de este capitulo:

1. **Complejidad computacional** clasifica los problemas segun cuantos recursos necesitan. La frontera critica es entre polinomial y exponencial.

2. **P vs NP** es la pregunta fundamental: si verificar es facil, encontrar tambien lo es? Probablemente no (P != NP), pero no lo hemos probado.

3. **Funciones de un solo sentido** son la base teorica de la criptografia. Probablemente existen, pero no lo hemos probado.

4. **Los problemas que sostienen la criptografia** (factorizacion, logaritmo discreto, ECDLP, LWE) han resistido decadas de ataques. No hemos probado que son dificiles, pero la evidencia es abrumadora.

5. **Bits de seguridad** es la metrica universal: 128 bits = 2^128 operaciones = fisicamente imposible.

6. **Reducciones** nos permiten probar que romper un algoritmo es al menos tan dificil como resolver un problema que creemos dificil.

7. **El eslabon mas debil** determina la seguridad del sistema completo.

En el proximo capitulo, aplicaremos todo este conocimiento cuando entremos al mundo del cifrado simetrico con AES: veremos como la teoria de complejidad se traduce en decisiones practicas sobre tamano de llaves, modos de operacion y niveles de seguridad.

---

## Referencias del capitulo

- Agrawal, M., Kayal, N., y Saxena, N. (2002). "PRIMES is in P". Annals of Mathematics.
- Cook, S. A. (1971). "The Complexity of Theorem-Proving Procedures". Proceedings of the Third Annual ACM Symposium on Theory of Computing.
- Gasarch, W. (2019). "Guest Column: The Third P =? NP Poll". SIGACT News.
- Hirahara, S. (2023). "Capturing One-Way Functions via NP-Hardness of Meta-Complexity". Proceedings of STOC 2023.
- Hirahara, S. y Lu, Z. (2024). "One-Way Functions and pKt Complexity". Cryptology ePrint Archive 2024/1388.
- NIST (2020). *SP 800-57 Part 1 Rev. 5: Recommendation for Key Management*.
- Rabin, M. y Scott, D. (1959). "Finite Automata and Their Decision Problems". IBM Journal of Research and Development.
- Shor, P. (1994). "Algorithms for Quantum Computation: Discrete Logarithms and Factoring". Proceedings of FOCS 1994.
- Turing, A. (1936). "On Computable Numbers, with an Application to the Entscheidungsproblem". Proceedings of the London Mathematical Society.
