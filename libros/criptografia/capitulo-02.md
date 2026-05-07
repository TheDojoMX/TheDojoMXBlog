# Capitulo 2: Las matematicas son tu aliado, no tu enemigo

> "Toda la criptografia moderna se sostiene en operaciones que aprendiste en secundaria... llevadas al extremo."

---

No necesitas un doctorado en matematicas para usar criptografia. Pero si quieres entender **por que** puedes confiar tu dinero, tu identidad y tus secretos a un algoritmo, necesitas entender cinco conceptos. Solo cinco:

1. Aritmetica modular
2. Numeros primos
3. Probabilidad (y por que 2^128 es "imposible")
4. XOR
5. Campos finitos (una introduccion suave)

Cada uno de estos conceptos aparecera una y otra vez en los capitulos siguientes. Invertir tiempo aqui te ahorrara horas de confusion mas adelante.

Y lo mejor: cada concepto viene con codigo Python que puedes ejecutar ahora mismo.

---

## 2.1 Aritmetica modular: el reloj que hace posible la criptografia

### 2.1.1 La analogia del reloj

Mira un reloj de pared. Si son las 10:00 y pasan 5 horas, que hora es? Las 3:00 de la tarde, no las 15:00. El reloj "da la vuelta" al llegar a 12.

Eso es exactamente aritmetica modular:

```
10 + 5 = 15
15 mod 12 = 3
```

En Python, el operador `%` (modulo) hace exactamente esto:

```python
print(15 % 12)   # 3
print(27 % 12)   # 3
print(100 % 12)  # 4
```

En aritmetica modular, decimos que 15 y 3 son **congruentes modulo 12**, y lo escribimos:

```
15 ≡ 3 (mod 12)
```

Esto significa que 15 y 3 dan el mismo residuo al dividirse entre 12.

Por que le importa esto a la criptografia? Porque la aritmetica modular crea un **espacio cerrado y finito** donde podemos hacer operaciones sin que los numeros crezcan sin control. En un campo modular, todo resultado "da la vuelta" y se queda dentro del rango 0 a n-1. Esto es esencial para que los algoritmos criptograficos puedan trabajar con numeros de tamano fijo --exactamente como las computadoras representan la informacion.

### 2.1.2 Operaciones modulares en Python

Todas las operaciones aritmeticas que conoces funcionan en aritmetica modular. Veamoslas:

```python
# Definimos nuestro modulo
m = 17  # Un numero primo (veras por que importa)

# Suma modular
a, b = 12, 9
print(f"{a} + {b} mod {m} = {(a + b) % m}")
# 12 + 9 mod 17 = 4   (porque 21 mod 17 = 4)

# Resta modular
print(f"{a} - {b} mod {m} = {(a - b) % m}")
# 12 - 9 mod 17 = 3

# Multiplicacion modular
print(f"{a} * {b} mod {m} = {(a * b) % m}")
# 12 * 9 mod 17 = 6   (porque 108 mod 17 = 6)
```

Hasta aqui nada sorprendente. Pero ahora viene la operacion que sostiene gran parte de la criptografia de llave publica:

**Exponenciacion modular**

```python
# Exponenciacion modular: base^exponente mod modulo
base = 7
exponente = 123
modulo = 1000

# Forma ingenua (funciona pero es lenta para numeros grandes):
resultado_ingenuo = (base ** exponente) % modulo

# Forma eficiente con pow() de Python:
resultado = pow(base, exponente, modulo)

print(f"{base}^{exponente} mod {modulo} = {resultado}")
# 7^123 mod 1000 = 343
```

La funcion `pow(base, exp, mod)` de Python es especial: no calcula primero `base^exp` (que seria un numero astronomico) y luego toma el modulo. Internamente usa un algoritmo llamado **exponenciacion rapida** (square-and-multiply) que mantiene los numeros intermedios pequenos tomando el modulo en cada paso. Esto permite calcular exponenciales modulares con numeros de miles de digitos en milisegundos.

Ahora viene la pregunta crucial: **podemos revertir esta operacion?**

```python
# FACIL: calcular 7^123 mod 1000
resultado = pow(7, 123, 1000)
print(f"Resultado: {resultado}")  # 343

# DIFICIL: dado que resultado = 343, base = 7, modulo = 1000
# encontrar el exponente 123
# Esto se llama el LOGARITMO DISCRETO
# No existe algoritmo eficiente para resolverlo en general
```

Calcular `7^123 mod 1000` es instantaneo. Pero dado el resultado 343 y la base 7, encontrar el exponente 123 (lo que se llama el **logaritmo discreto**) no tiene solucion eficiente conocida. Esta asimetria --facil en una direccion, dificil en la otra-- es el corazon matematico de algoritmos como Diffie-Hellman y la criptografia de curvas elipticas [Aumasson, 2024].

Veamos que tan dificil es con numeros grandes:

```python
import time

# Con numeros pequenos, la fuerza bruta funciona
def logaritmo_discreto_fuerza_bruta(resultado, base, modulo):
    """Encuentra exp tal que base^exp mod modulo = resultado."""
    for exp in range(modulo):
        if pow(base, exp, modulo) == resultado:
            return exp
    return None

# Ejemplo pequeno: resolvible
inicio = time.time()
exp = logaritmo_discreto_fuerza_bruta(343, 7, 1000)
duracion = time.time() - inicio
print(f"Logaritmo discreto (mod 1000): {exp}, tiempo: {duracion:.4f}s")

# Ejemplo mediano: ya se nota la lentitud
inicio = time.time()
resultado_grande = pow(7, 98765, 1_000_000)
exp2 = logaritmo_discreto_fuerza_bruta(resultado_grande, 7, 1_000_000)
duracion2 = time.time() - inicio
print(f"Logaritmo discreto (mod 1,000,000): {exp2}, tiempo: {duracion2:.2f}s")

# Con modulos de 2048 bits (como los que usa RSA):
# No hay suficiente tiempo en el universo para resolverlo por fuerza bruta
```

### 2.1.3 El inverso modular

En aritmetica normal, el inverso de 5 es 1/5 (o 0.2), porque 5 x 0.2 = 1. En aritmetica modular, el inverso de `a` modulo `m` es un numero `b` tal que:

```
a * b ≡ 1 (mod m)
```

Es decir, `b` es el numero que multiplicado por `a` da 1 dentro del espacio modular.

```python
# Encontrar el inverso modular de 3 mod 17
# Buscamos b tal que 3 * b mod 17 = 1

# Metodo 1: fuerza bruta (para entender)
def inverso_modular_fuerza_bruta(a, m):
    for b in range(m):
        if (a * b) % m == 1:
            return b
    return None  # No existe si gcd(a, m) != 1

inv = inverso_modular_fuerza_bruta(3, 17)
print(f"Inverso de 3 mod 17 = {inv}")    # 6
print(f"Verificacion: 3 * 6 mod 17 = {(3 * 6) % 17}")  # 1

# Metodo 2: Python 3.8+ tiene pow(a, -1, m)
inv2 = pow(3, -1, 17)
print(f"Inverso (pow): {inv2}")  # 6

# Metodo 3: usando el Teorema de Euler/Fermat
# Si m es primo, entonces a^(-1) ≡ a^(m-2) (mod m)
inv3 = pow(3, 17 - 2, 17)
print(f"Inverso (Fermat): {inv3}")  # 6
```

El inverso modular no siempre existe. Solo existe cuando `a` y `m` son **coprimos** (su maximo comun divisor es 1). Si `m` es primo, todo numero del 1 al m-1 tiene inverso. Esta es una de las razones por las que los primos son tan importantes en criptografia.

El algoritmo clasico para calcular el inverso modular de manera eficiente es el **Algoritmo Extendido de Euclides**:

```python
def euclides_extendido(a, b):
    """
    Dado a y b, encuentra x, y tal que a*x + b*y = gcd(a, b).
    Si gcd(a, b) = 1, entonces x es el inverso modular de a mod b.
    """
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = euclides_extendido(b % a, a)
    x = y1 - (b // a) * x1
    y = x1

    return gcd, x, y


def inverso_modular(a, m):
    """Calcula el inverso modular usando el algoritmo extendido de Euclides."""
    gcd, x, _ = euclides_extendido(a % m, m)
    if gcd != 1:
        raise ValueError(f"El inverso modular de {a} mod {m} no existe (gcd = {gcd})")
    return x % m


# Ejemplo
inv = inverso_modular(3, 17)
print(f"Inverso de 3 mod 17 = {inv}")      # 6
print(f"Verificacion: 3 * {inv} mod 17 = {(3 * inv) % 17}")  # 1

# Un ejemplo mas grande
inv_grande = inverso_modular(12345, 1000003)
print(f"Inverso de 12345 mod 1000003 = {inv_grande}")
print(f"Verificacion: {(12345 * inv_grande) % 1000003}")  # 1
```

### 2.1.4 El cifrado de Cesar como aritmetica modular

Ahora vamos a conectar la teoria con la practica criptografica. El cifrado de Cesar --uno de los cifrados mas antiguos de la historia, usado por Julio Cesar para comunicarse con sus generales-- es pura aritmetica modular:

```python
def cifrado_cesar(texto, k):
    """
    Cifra un texto con el cifrado de Cesar.
    Cada letra se desplaza k posiciones en el alfabeto (mod 26).
    """
    resultado = []
    for c in texto.upper():
        if c.isalpha():
            # Convertir letra a numero (A=0, B=1, ..., Z=25)
            numero = ord(c) - ord('A')
            # Desplazar k posiciones mod 26
            cifrado = (numero + k) % 26
            # Convertir de vuelta a letra
            resultado.append(chr(cifrado + ord('A')))
        else:
            resultado.append(c)
    return ''.join(resultado)


def descifrado_cesar(texto_cifrado, k):
    """Descifra restando k (o sumando 26-k, que es lo mismo mod 26)."""
    return cifrado_cesar(texto_cifrado, -k)


# Ejemplo
mensaje = "CRIPTOGRAFIA APLICADA"
llave = 7

cifrado = cifrado_cesar(mensaje, llave)
descifrado = descifrado_cesar(cifrado, llave)

print(f"Original:    {mensaje}")
print(f"Cifrado (k={llave}): {cifrado}")
print(f"Descifrado:  {descifrado}")
```

```
Original:    CRIPTOGRAFIA APLICADA
Cifrado (k=7): JYPWAVNYHmph HWSPJHKH
Descifrado:  CRIPTOGRAFIA APLICADA
```

El cifrado de Cesar es trivial de romper (solo hay 25 llaves posibles), pero ilustra el principio fundamental: **cifrar es aplicar una operacion modular con una llave, y descifrar es aplicar la operacion inversa**. Los algoritmos modernos como AES usan este mismo principio, pero con operaciones mucho mas complejas y espacios de llaves astronomicamente mas grandes.

---

## 2.2 Numeros primos: los atomos de la criptografia

### 2.2.1 Que es un numero primo y por que importa

Un numero primo es un entero mayor que 1 que solo es divisible por 1 y por si mismo. Los primeros primos son: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29...

El **Teorema Fundamental de la Aritmetica** establece que todo entero mayor que 1 se puede descomponer en factores primos de forma **unica**. Por ejemplo:

```python
# Factorizacion unica
# 84 = 2 * 2 * 3 * 7 = 2^2 * 3 * 7
# No hay otra forma de factorizarlo en primos

def factorizar(n):
    """Encuentra la factorizacion en primos de n."""
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

print(f"84 = {' * '.join(map(str, factorizar(84)))}")
# 84 = 2 * 2 * 3 * 7

print(f"1000003 = {' * '.join(map(str, factorizar(1000003)))}")
# 1000003 es primo, asi que solo se factoriza como si mismo
```

Por que importa esto para la criptografia? Porque **multiplicar dos primos es instantaneo, pero factorizar el producto es extremadamente dificil** cuando los primos son grandes. Esta asimetria es la base de RSA, uno de los algoritmos criptograficos mas importantes de la historia [Schneier, 2015].

```python
import time

# FACIL: multiplicar dos primos
p = 104729
q = 104743
n = p * q
print(f"p * q = {p} * {q} = {n}")  # Instantaneo

# FACIL para numeros pequenos: factorizar
inicio = time.time()
factores = factorizar(n)
duracion = time.time() - inicio
print(f"Factorizacion de {n}: {factores} ({duracion:.4f}s)")

# Ahora intenta con primos un poco mas grandes...
p2 = 1000000007  # Primo de 10 digitos
q2 = 1000000009  # Primo de 10 digitos
n2 = p2 * q2
print(f"\np2 * q2 = {n2}")

inicio = time.time()
factores2 = factorizar(n2)
duracion2 = time.time() - inicio
print(f"Factorizacion: {factores2} ({duracion2:.2f}s)")
# Notaras que ya toma mas tiempo
```

### 2.2.2 Generacion de primos grandes

En criptografia real, necesitamos primos de **2048 bits o mas** (numeros de alrededor de 617 digitos). Como generamos y verificamos que un numero tan grande es primo?

La respuesta es el **Test de Primalidad de Miller-Rabin**, un algoritmo **probabilistico** que determina si un numero es primo con una certeza arbitrariamente alta:

```python
import random

def es_probablemente_primo(n, k=40):
    """
    Test de Miller-Rabin: determina si n es primo.

    Retorna False si n es definitivamente compuesto.
    Retorna True si n es probablemente primo.
    La probabilidad de error es como maximo 4^(-k).
    Con k=40, la probabilidad de error es ~2^(-80), despreciable.
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Escribir n-1 como 2^r * d con d impar
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Realizar k rondas de prueba
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # Definitivamente compuesto

    return True  # Probablemente primo


# Verificar algunos primos conocidos
print(f"17 es primo? {es_probablemente_primo(17)}")       # True
print(f"18 es primo? {es_probablemente_primo(18)}")       # False
print(f"1000003 es primo? {es_probablemente_primo(1000003)}")  # True


def generar_primo(bits):
    """Genera un numero primo aleatorio de la cantidad de bits especificada."""
    while True:
        # Generar un numero aleatorio impar del tamano correcto
        candidato = random.getrandbits(bits)
        candidato |= (1 << (bits - 1)) | 1  # Asegurar bit mas alto y que sea impar

        if es_probablemente_primo(candidato):
            return candidato


# Generar un primo de 512 bits (para demostracion; en produccion usa 2048+)
import time
inicio = time.time()
primo = generar_primo(512)
duracion = time.time() - inicio
print(f"\nPrimo de 512 bits generado en {duracion:.2f}s:")
print(f"  {primo}")
print(f"  ({len(str(primo))} digitos)")
```

En produccion, no deberias implementar tu propio generador de primos. Las librerias criptograficas como `cryptography` de Python usan implementaciones optimizadas y auditadas:

```python
from cryptography.hazmat.primitives.asymmetric import rsa

# Asi genera Python primos para RSA internamente:
# Genera un par de llaves RSA de 2048 bits,
# lo que requiere encontrar dos primos de ~1024 bits cada uno
llave_privada = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Extraer los primos (solo para demostracion, NUNCA expongas esto)
numeros_privados = llave_privada.private_numbers()
p = numeros_privados.p
q = numeros_privados.q
n = numeros_privados.public_numbers.n

print(f"Primo p ({len(str(p))} digitos): {str(p)[:40]}...")
print(f"Primo q ({len(str(q))} digitos): {str(q)[:40]}...")
print(f"n = p*q ({len(str(n))} digitos): {str(n)[:40]}...")
print(f"\nVerificacion: p * q == n? {p * q == n}")
```

### 2.2.3 El problema de la factorizacion

Regresemos a la pregunta fundamental. Si te doy el numero `n = p * q` donde `p` y `q` son primos grandes, puedes encontrar `p` y `q`?

```python
import time

# Vamos a medir cuanto tarda factorizar numeros de diferentes tamanos
def factorizar_prueba(bits):
    """Genera n = p*q con primos de `bits` bits y mide cuanto tarda factorizar."""
    p = generar_primo(bits)
    q = generar_primo(bits)
    n = p * q

    inicio = time.time()
    factores = factorizar(n)
    duracion = time.time() - inicio

    return bits * 2, duracion, len(factores) == 2


# Prueba con diferentes tamanos
print(f"{'Bits de n':>10} | {'Tiempo':>12} | {'Factorizado?'}")
print("-" * 40)

for bits in [16, 20, 24, 28, 32]:
    total_bits, duracion, exito = factorizar_prueba(bits)
    print(f"{total_bits:>10} | {duracion:>10.4f}s | {'Si' if exito else 'No (timeout)'}")
```

Observa como el tiempo crece **exponencialmente** con el tamano de los numeros. Para numeros de 64 bits, la factorizacion ya toma segundos. Para numeros de 2048 bits (como los que usa RSA), los mejores algoritmos conocidos (como la criba del campo numerico general) requeririan miles de millones de anos con todo el poder de computo disponible en el planeta [Lenstra et al., 2017].

Esta es la **funcion trampa** (trapdoor function) que hace posible RSA:

```
MULTIPLICACION (facil):    p * q = n           -> Instantaneo
FACTORIZACION (dificil):   n = ? * ?           -> Miles de millones de anos
DESCIFRADO (con trampa):   Conociendo p y q    -> Instantaneo

RSA funciona asi:
- Tu llave PUBLICA contiene n (el producto)
- Tu llave PRIVADA contiene p y q (los factores)
- Quien tiene la llave publica puede cifrar, pero no descifrar
- Quien tiene la llave privada puede descifrar, porque conoce la "trampa"
```

### 2.2.4 Divisibilidad y el maximo comun divisor (GCD)

El maximo comun divisor (GCD, por *Greatest Common Divisor*) de dos numeros es el numero mas grande que divide a ambos. Es fundamental en criptografia porque nos dice si dos numeros son **coprimos** (GCD = 1), condicion necesaria para que exista el inverso modular.

```python
def gcd(a, b):
    """Algoritmo de Euclides para el GCD. Mas de 2000 anos de antiguedad."""
    while b:
        a, b = b, a % b
    return a

# Ejemplos
print(f"gcd(12, 8) = {gcd(12, 8)}")     # 4
print(f"gcd(17, 13) = {gcd(17, 13)}")    # 1 (coprimos!)
print(f"gcd(100, 75) = {gcd(100, 75)}")  # 25

# Python tiene esto en la libreria estandar desde 3.5
from math import gcd as math_gcd
print(f"math.gcd(12, 8) = {math_gcd(12, 8)}")

# Verificar si dos numeros son coprimos
def son_coprimos(a, b):
    return gcd(a, b) == 1

print(f"\n17 y 13 son coprimos? {son_coprimos(17, 13)}")  # True
print(f"12 y 8 son coprimos? {son_coprimos(12, 8)}")      # False
```

El Algoritmo de Euclides para calcular el GCD es uno de los algoritmos mas antiguos conocidos (circa 300 a.C.) y sigue siendo usado en implementaciones criptograficas modernas. Su elegancia es notable: reduce un problema sobre dos numeros a un problema sobre numeros cada vez mas pequenos, hasta llegar a cero.

---

## 2.3 Probabilidad: por que 2^128 intentos es "imposible"

### 2.3.1 Entendiendo los numeros astronomicos

Cuando decimos que un algoritmo criptografico tiene "128 bits de seguridad", estamos diciendo que un atacante necesitaria, en promedio, **2^128 intentos** para romperlo por fuerza bruta. Pero que tan grande es 2^128?

```python
# Pongamos 2^128 en perspectiva

dos_128 = 2 ** 128
print(f"2^128 = {dos_128:,}")
# 340,282,366,920,938,463,463,374,607,431,768,211,456

# Comparaciones:
atomos_universo = 10 ** 80  # Estimacion de atomos en el universo observable
segundos_universo = 4.3e17  # Edad del universo en segundos (~13.8 mil millones de anos)
operaciones_por_segundo = 10 ** 18  # Supercomputadora mas rapida (1 exaFLOPS)

intentos_por_edad_universo = operaciones_por_segundo * segundos_universo

print(f"\nAtomoa en el universo: ~10^80")
print(f"2^128 = ~3.4 * 10^38")
print(f"\nSupercomputadora mas rapida: {operaciones_por_segundo:.0e} operaciones/segundo")
print(f"Edad del universo: {segundos_universo:.2e} segundos")
print(f"Operaciones en toda la edad del universo: {intentos_por_edad_universo:.2e}")
print(f"2^128: {dos_128:.2e}")
print(f"\nNecesitarias {dos_128 / intentos_por_edad_universo:.2e} edades del universo")
print(f"con la computadora mas rapida del mundo para probar todas las llaves.")
```

```
Necesitarias 7.9e+20 edades del universo
con la computadora mas rapida del mundo para probar todas las llaves.
```

Eso es 790 trillones de veces la edad del universo. Con **todas las computadoras del planeta trabajando juntas**. Por eso decimos que 128 bits de seguridad es "computacionalmente imposible" de romper por fuerza bruta.

### 2.3.2 La paradoja del cumpleanos

La paradoja del cumpleanos es un resultado contraintuitivo de probabilidad con enormes implicaciones para la criptografia.

**La pregunta**: en un grupo de personas, cuantas necesitas reunir para que haya una probabilidad mayor al 50% de que dos personas compartan cumpleanos?

La respuesta intuitiva suele ser "alrededor de 183" (la mitad de 365). La respuesta real es **solo 23**.

```python
import math

def probabilidad_colision(n, d=365):
    """
    Probabilidad de que al menos dos de n personas compartan cumpleanos
    en un espacio de d dias posibles.
    """
    if n > d:
        return 1.0
    # P(no colision) = (d/d) * ((d-1)/d) * ((d-2)/d) * ... * ((d-n+1)/d)
    log_prob_no_colision = sum(math.log(1 - i/d) for i in range(n))
    return 1 - math.exp(log_prob_no_colision)


# Encontrar n para superar 50%
for n in range(1, 100):
    prob = probabilidad_colision(n)
    if prob >= 0.5:
        print(f"Con {n} personas, P(colision) = {prob:.4f} (> 50%!)")
        break

# Tabla de probabilidades
print(f"\n{'Personas':>10} | {'P(colision)':>12}")
print("-" * 25)
for n in [5, 10, 15, 20, 23, 30, 50, 70]:
    print(f"{n:>10} | {probabilidad_colision(n):>11.4f}")
```

Que tiene que ver esto con la criptografia? Recuerda la **resistencia a colisiones** del Capitulo 1. Si una funcion hash produce salidas de `n` bits, el ataque del cumpleanos puede encontrar una colision en aproximadamente **2^(n/2)** intentos, no 2^n.

```python
# Impacto en la seguridad de funciones hash
print("Seguridad efectiva contra colisiones:")
print(f"{'Hash':>10} | {'Bits salida':>12} | {'Ataque preimagen':>18} | {'Ataque colision':>18}")
print("-" * 65)
for nombre, bits in [("MD5", 128), ("SHA-1", 160), ("SHA-256", 256), ("SHA-512", 512)]:
    print(f"{nombre:>10} | {bits:>12} | {'2^' + str(bits):>18} | {'2^' + str(bits//2):>18}")
```

```
Hash       |  Bits salida | Ataque preimagen |  Ataque colision
-----------------------------------------------------------------
       MD5 |          128 |            2^128 |             2^64
     SHA-1 |          160 |            2^160 |             2^80
   SHA-256 |          256 |            2^256 |            2^128
   SHA-512 |          512 |            2^512 |            2^256
```

Por eso SHA-256 ofrece "128 bits de seguridad" contra colisiones (2^128 intentos), no 256. Y por eso SHA-1 con sus 160 bits ofrecia solo 80 bits de seguridad contra colisiones --un nivel que ya esta al alcance de atacantes con recursos [Schneier, 2015].

---

## 2.4 XOR: la operacion perfecta para cifrar

### 2.4.1 La tabla de verdad de XOR

XOR (exclusive OR, "o exclusivo") es una operacion logica bit a bit. Su tabla de verdad es simple:

```
A | B | A XOR B
--|---|--------
0 | 0 |   0
0 | 1 |   1
1 | 0 |   1
1 | 1 |   0
```

En palabras: el resultado es 1 cuando los bits son **diferentes**, y 0 cuando son **iguales**. En Python, el operador XOR es `^`:

```python
# XOR bit a bit
print(f"0 ^ 0 = {0 ^ 0}")  # 0
print(f"0 ^ 1 = {0 ^ 1}")  # 1
print(f"1 ^ 0 = {1 ^ 0}")  # 1
print(f"1 ^ 1 = {1 ^ 1}")  # 0

# XOR con numeros mas grandes (opera bit a bit)
a = 0b11001010  # 202 en decimal
b = 0b10110101  # 181 en decimal
c = a ^ b

print(f"\n  {a:08b}  ({a})")
print(f"^ {b:08b}  ({b})")
print(f"= {c:08b}  ({c})")
```

Ahora viene la propiedad **magica** que hace al XOR perfecto para criptografia:

```python
# La propiedad de involucion: A XOR B XOR B = A
mensaje = 42
llave = 137

# Cifrar
cifrado = mensaje ^ llave
print(f"Mensaje:  {mensaje:08b} ({mensaje})")
print(f"Llave:    {llave:08b} ({llave})")
print(f"Cifrado:  {cifrado:08b} ({cifrado})")

# Descifrar: aplicar XOR con la misma llave
descifrado = cifrado ^ llave
print(f"Descifrado: {descifrado:08b} ({descifrado})")
print(f"\nMensaje original recuperado? {descifrado == mensaje}")
```

Tres propiedades criticas de XOR para la criptografia:

```python
# 1. INVOLUCION: A ^ B ^ B = A (aplica la llave dos veces para revertir)
a, b = 200, 99
assert (a ^ b ^ b) == a
print("1. A ^ B ^ B = A  (involucion)")

# 2. CONMUTATIVA: A ^ B = B ^ A
assert (a ^ b) == (b ^ a)
print("2. A ^ B = B ^ A  (conmutativa)")

# 3. ASOCIATIVA: (A ^ B) ^ C = A ^ (B ^ C)
c = 150
assert ((a ^ b) ^ c) == (a ^ (b ^ c))
print("3. (A ^ B) ^ C = A ^ (B ^ C)  (asociativa)")

# 4. IDENTIDAD: A ^ 0 = A
assert a ^ 0 == a
print("4. A ^ 0 = A  (identidad)")

# 5. AUTO-INVERSO: A ^ A = 0
assert a ^ a == 0
print("5. A ^ A = 0  (auto-inverso)")
```

La propiedad de involucion es la que hace a XOR perfecto: **la misma operacion cifra y descifra**. No necesitas una operacion inversa separada. Esto simplifica enormemente el diseno de algoritmos criptograficos.

### 2.4.2 El One-Time Pad: cifrado perfecto

En 1917, Gilbert Vernam invento el **One-Time Pad** (OTP), el unico sistema de cifrado que se puede demostrar matematicamente que es **perfecto** -- es decir, que un atacante con recursos computacionales infinitos no puede romperlo.

El principio es simple: aplica XOR entre el mensaje y una llave **del mismo tamano que el mensaje** y **completamente aleatoria**:

```python
import os

def otp_cifrar(mensaje_bytes):
    """Cifra con One-Time Pad. Retorna (cifrado, llave)."""
    llave = os.urandom(len(mensaje_bytes))  # Llave aleatoria criptografica
    cifrado = bytes(m ^ k for m, k in zip(mensaje_bytes, llave))
    return cifrado, llave


def otp_descifrar(cifrado, llave):
    """Descifra con One-Time Pad."""
    return bytes(c ^ k for c, k in zip(cifrado, llave))


# Ejemplo completo
mensaje = "Criptografia aplicada".encode('utf-8')
print(f"Mensaje original: {mensaje}")

cifrado, llave = otp_cifrar(mensaje)
print(f"Cifrado:          {cifrado.hex()}")
print(f"Llave:            {llave.hex()}")

descifrado = otp_descifrar(cifrado, llave)
print(f"Descifrado:       {descifrado}")
print(f"Correcto?         {descifrado == mensaje}")
```

Por que es **perfecto**? Porque el cifrado es estadisticamente indistinguible de datos aleatorios. Sin la llave, cada posible mensaje es igualmente probable. Un atacante que intercepta el cifrado no obtiene absolutamente ninguna informacion sobre el mensaje, ni siquiera con poder computacional infinito [Shannon, 1949].

Entonces, por que no usamos siempre el OTP? Porque tiene un problema practico devastador: **la llave debe ser tan larga como el mensaje y debe transmitirse de manera segura**. Si tienes un canal seguro para enviar la llave, ya tienes un canal seguro para enviar el mensaje. Es un circulo vicioso.

Ademas, cada llave solo puede usarse **una sola vez** (de ahi el nombre "one-time"). Si reutilizas la llave, el cifrado se rompe trivialmente:

### 2.4.3 Por que XOR sin aleatoriedad no sirve

```python
# PELIGRO: reutilizar la llave con XOR
mensaje1 = b"ataque al norte"
mensaje2 = b"ataque al sur  "  # Mismo largo para la demostracion
llave = os.urandom(len(mensaje1))

cifrado1 = bytes(m ^ k for m, k in zip(mensaje1, llave))
cifrado2 = bytes(m ^ k for m, k in zip(mensaje2, llave))

# Un atacante que tiene ambos cifrados puede hacer XOR entre ellos:
xor_cifrados = bytes(c1 ^ c2 for c1, c2 in zip(cifrado1, cifrado2))

# Esto ELIMINA la llave completamente:
# cifrado1 ^ cifrado2 = (mensaje1 ^ llave) ^ (mensaje2 ^ llave)
#                      = mensaje1 ^ mensaje2 ^ (llave ^ llave)
#                      = mensaje1 ^ mensaje2 ^ 0
#                      = mensaje1 ^ mensaje2

xor_mensajes = bytes(m1 ^ m2 for m1, m2 in zip(mensaje1, mensaje2))

print(f"cifrado1 XOR cifrado2:   {xor_cifrados.hex()}")
print(f"mensaje1 XOR mensaje2:   {xor_mensajes.hex()}")
print(f"Son iguales?             {xor_cifrados == xor_mensajes}")
```

Al hacer XOR entre los dos textos cifrados, **la llave desaparece**. Lo que queda es el XOR de los dos mensajes originales, que contiene informacion significativa. Con tecnicas como analisis de frecuencia y conocimiento del idioma, un atacante puede recuperar ambos mensajes.

Esta vulnerabilidad no es teorica. En la Segunda Guerra Mundial, los sovieticos reutilizaron llaves de OTP en el sistema VENONA, y la inteligencia estadounidense logro descifrar mensajes criticos [Schneier, 2015].

La leccion: **la herramienta perfecta usada mal es peor que nada**, porque te da una falsa sensacion de seguridad. Esto es exactamente lo que pasa con muchos de los fallos criptograficos en software real -- la primitiva es correcta, pero el uso es incorrecto.

---

## 2.5 Campos finitos: una introduccion suave

### 2.5.1 Que es un campo finito

Ya viste que en aritmetica modular podemos sumar, restar y multiplicar sin que los numeros se salgan de un rango. Un **campo finito** (tambien llamado **campo de Galois**, en honor al matematico frances Evariste Galois) formaliza esta idea: es un conjunto finito de elementos donde podemos hacer las cuatro operaciones aritmeticas basicas (suma, resta, multiplicacion, division) y las propiedades algebraicas que esperamos se cumplen.

El campo finito mas simple es **GF(p)**, donde `p` es un numero primo. Este campo contiene los numeros {0, 1, 2, ..., p-1} con aritmetica modulo `p`:

```python
class CampoFinito:
    """
    Implementacion simple de un campo finito GF(p).
    Demuestra que las operaciones se mantienen dentro del campo.
    """

    def __init__(self, valor, primo):
        self.valor = valor % primo
        self.primo = primo

    def __add__(self, otro):
        return CampoFinito((self.valor + otro.valor) % self.primo, self.primo)

    def __sub__(self, otro):
        return CampoFinito((self.valor - otro.valor) % self.primo, self.primo)

    def __mul__(self, otro):
        return CampoFinito((self.valor * otro.valor) % self.primo, self.primo)

    def __truediv__(self, otro):
        """Division = multiplicar por el inverso modular."""
        inverso = pow(otro.valor, -1, self.primo)
        return CampoFinito((self.valor * inverso) % self.primo, self.primo)

    def __repr__(self):
        return f"{self.valor}"

    def __eq__(self, otro):
        return self.valor == otro.valor and self.primo == otro.primo


# Trabajemos en GF(17) -- un campo finito con 17 elementos
p = 17
a = CampoFinito(12, p)
b = CampoFinito(9, p)

print(f"Campo: GF({p})")
print(f"a = {a}, b = {b}")
print(f"a + b = {a + b}")      # (12 + 9) mod 17 = 4
print(f"a - b = {a - b}")      # (12 - 9) mod 17 = 3
print(f"a * b = {a * b}")      # (12 * 9) mod 17 = 6
print(f"a / b = {a / b}")      # 12 * inverso(9, 17) mod 17

# Verificar que la division funciona: (a / b) * b debe dar a
resultado = (a / b) * b
print(f"(a / b) * b = {resultado}")  # Debe dar 12
print(f"Verificado: {resultado == a}")
```

Por que importan los campos finitos en criptografia?

1. **AES** trabaja internamente en **GF(2^8)** -- un campo con 256 elementos, perfecto para representar bytes. Todas las operaciones de mezcla y sustitucion de AES son operaciones algebraicas en este campo [Daemen y Rijmen, 2002].

2. **RSA** trabaja en GF(n) donde n es el producto de dos primos grandes.

3. **La criptografia de curvas elipticas** trabaja con puntos en curvas definidas sobre campos finitos.

### 2.5.2 Curvas elipticas: una vision panoramica

Las curvas elipticas son el fundamento de la criptografia moderna mas eficiente. Una curva eliptica es el conjunto de puntos (x, y) que satisfacen una ecuacion de la forma:

```
y^2 = x^3 + ax + b
```

Lo fascinante es que podemos definir una operacion de "suma" entre puntos de la curva. Si tomas dos puntos P y Q en la curva, trazas una linea entre ellos, esa linea intersecta la curva en un tercer punto, y el "reflejo" de ese punto es P + Q.

```python
# Visualizacion simplificada del concepto (no para uso criptografico)

def puntos_curva_eliptica(a, b, p):
    """
    Encuentra todos los puntos de la curva y^2 = x^3 + ax + b
    sobre el campo finito GF(p).
    """
    puntos = []
    for x in range(p):
        rhs = (x**3 + a*x + b) % p
        for y in range(p):
            if (y * y) % p == rhs:
                puntos.append((x, y))
    return puntos


# Curva y^2 = x^3 + 2x + 3 sobre GF(97)
a, b, p = 2, 3, 97
puntos = puntos_curva_eliptica(a, b, p)

print(f"Curva: y^2 = x^3 + {a}x + {b} sobre GF({p})")
print(f"Numero de puntos: {len(puntos)}")
print(f"Primeros 10 puntos: {puntos[:10]}")
```

El **problema del logaritmo discreto en curvas elipticas** (ECDLP) es aun mas dificil que el logaritmo discreto clasico o la factorizacion de primos. Por eso, las llaves de curvas elipticas son mucho mas cortas que las de RSA para el mismo nivel de seguridad:

```python
# Comparacion de tamanos de llave para seguridad equivalente
print(f"{'Nivel de seguridad':>20} | {'RSA (bits)':>12} | {'ECC (bits)':>12} | {'Ratio':>8}")
print("-" * 60)
comparaciones = [
    ("80 bits", 1024, 160),
    ("112 bits", 2048, 224),
    ("128 bits", 3072, 256),
    ("192 bits", 7680, 384),
    ("256 bits", 15360, 521),
]
for nivel, rsa_bits, ecc_bits in comparaciones:
    print(f"{nivel:>20} | {rsa_bits:>12} | {ecc_bits:>12} | {rsa_bits/ecc_bits:>7.1f}x")
```

```
Nivel de seguridad   |   RSA (bits) |   ECC (bits) |    Ratio
------------------------------------------------------------
             80 bits |         1024 |          160 |    6.4x
            112 bits |         2048 |          224 |    9.1x
            128 bits |         3072 |          256 |   12.0x
            192 bits |         7680 |          384 |   20.0x
            256 bits |        15360 |          521 |   29.5x
```

Para 128 bits de seguridad, RSA necesita llaves de 3072 bits, mientras que ECC solo necesita 256 bits. Eso es **12 veces mas compacto**. Esto importa enormemente para dispositivos moviles, IoT, y protocolos como TLS donde el tamano de las llaves afecta directamente el rendimiento [NIST SP 800-57, 2020].

### 2.5.3 Mapa de conexiones: que matematica usa cada algoritmo

Ahora que hemos recorrido los cinco conceptos fundamentales, veamos como se conectan con los algoritmos criptograficos reales:

```
| Algoritmo       | Concepto matematico       | Problema dificil              |
|-----------------|---------------------------|-------------------------------|
| AES             | Campos finitos GF(2^8)    | Confusion/difusion (Shannon)  |
| RSA             | Aritmetica modular, primos| Factorizacion de enteros      |
| Diffie-Hellman  | Exponenciacion modular    | Logaritmo discreto            |
| ECDSA / Ed25519 | Curvas elipticas sobre GF  | ECDLP (log. discreto en EC)  |
| SHA-256         | Operaciones bit a bit, XOR| Funcion de una via            |
| ChaCha20        | Suma modular, XOR, rotacion| PRF (funcion pseudoaleatoria)|
| ML-KEM (Kyber)  | Reticulas (lattices)      | Learning With Errors (LWE)    |
```

Cada algoritmo se sostiene en matematicas que acabas de aprender (o que por lo menos ahora puedes reconocer). La aritmetica modular y XOR aparecen en **todos** ellos. Los numeros primos sustentan RSA y Diffie-Hellman. Los campos finitos hacen posible AES y las curvas elipticas. Y la probabilidad nos permite cuantificar exactamente cuanta seguridad proporciona cada uno.

---

## 2.6 Ejercicio integrador: cifrado afin y ataque por fuerza bruta

El **cifrado afin** es una generalizacion del cifrado de Cesar que usa dos operaciones modulares: multiplicacion y suma. Es mas fuerte que Cesar, pero aun asi es facil de romper, lo que lo hace perfecto para entender por que el tamano del espacio de llaves importa.

```python
#!/usr/bin/env python3
"""
cifrado_afin.py - Cifrado afin y ataque por fuerza bruta

El cifrado afin cifra cada letra con la formula:
  E(x) = (a * x + b) mod 26

donde:
  - x es la posicion de la letra (A=0, B=1, ..., Z=25)
  - a es la llave multiplicativa (debe ser coprima con 26)
  - b es la llave aditiva (desplazamiento, como en Cesar)

Para descifrar:
  D(y) = a^(-1) * (y - b) mod 26

donde a^(-1) es el inverso modular de a mod 26.
"""

from math import gcd


def valores_validos_a():
    """
    Encuentra todos los valores validos de 'a' para el cifrado afin.
    'a' debe ser coprimo con 26 para que el inverso modular exista.
    """
    return [a for a in range(1, 26) if gcd(a, 26) == 1]


def cifrar_afin(texto, a, b):
    """Cifra un texto con el cifrado afin: E(x) = (a*x + b) mod 26."""
    if gcd(a, 26) != 1:
        raise ValueError(f"'a' ({a}) debe ser coprimo con 26. Valores validos: {valores_validos_a()}")

    resultado = []
    for c in texto.upper():
        if c.isalpha():
            x = ord(c) - ord('A')
            cifrado = (a * x + b) % 26
            resultado.append(chr(cifrado + ord('A')))
        else:
            resultado.append(c)
    return ''.join(resultado)


def descifrar_afin(texto_cifrado, a, b):
    """Descifra usando el inverso modular: D(y) = a^(-1) * (y - b) mod 26."""
    a_inv = pow(a, -1, 26)  # Inverso modular de a mod 26

    resultado = []
    for c in texto_cifrado.upper():
        if c.isalpha():
            y = ord(c) - ord('A')
            descifrado = (a_inv * (y - b)) % 26
            resultado.append(chr(descifrado + ord('A')))
        else:
            resultado.append(c)
    return ''.join(resultado)


def ataque_fuerza_bruta(texto_cifrado):
    """
    Prueba TODAS las combinaciones posibles de (a, b).
    El espacio de llaves es pequeno: 12 valores de a * 26 valores de b = 312.
    """
    validos_a = valores_validos_a()
    intentos = 0

    print(f"Valores validos de a: {validos_a} ({len(validos_a)} valores)")
    print(f"Valores de b: 0-25 ({26} valores)")
    print(f"Espacio total de llaves: {len(validos_a) * 26} combinaciones\n")

    resultados = []
    for a in validos_a:
        for b in range(26):
            intentos += 1
            descifrado = descifrar_afin(texto_cifrado, a, b)
            resultados.append((a, b, descifrado))

    return resultados, intentos


# === Demostracion ===

# 1. Cifrar un mensaje
mensaje_original = "CRIPTOGRAFIA APLICADA PARA DESARROLLADORES"
a, b = 7, 13  # Nuestra llave secreta

cifrado = cifrar_afin(mensaje_original, a, b)
descifrado = descifrar_afin(cifrado, a, b)

print("=== CIFRADO AFIN ===")
print(f"Mensaje:    {mensaje_original}")
print(f"Llave:      a={a}, b={b}")
print(f"Cifrado:    {cifrado}")
print(f"Descifrado: {descifrado}")
print(f"Correcto?   {descifrado == mensaje_original}")
print()

# 2. Ataque de fuerza bruta
print("=== ATAQUE DE FUERZA BRUTA ===")
resultados, intentos = ataque_fuerza_bruta(cifrado)

# Filtrar resultados que contengan palabras en espanol comunes
# (en un ataque real, usarias analisis de frecuencia o un diccionario)
palabras_clave = ["PARA", "CRIPTOGRAFIA", "APLICADA"]

print(f"Total de intentos: {intentos}")
print(f"\nResultados que contienen palabras clave:")
for a_test, b_test, texto in resultados:
    if any(palabra in texto for palabra in palabras_clave):
        print(f"  a={a_test:2d}, b={b_test:2d}: {texto}")

print(f"\nReflexion: con solo 312 llaves posibles,")
print(f"probar TODAS toma milisegundos.")
print(f"Esto es por que necesitamos espacios de llaves de 2^128 o mas.")
```

Ejecuta este programa y reflexiona: el cifrado afin tiene solo **312 llaves posibles**. Una computadora las prueba todas en milisegundos. Compara esto con AES-256, que tiene 2^256 llaves posibles -- un numero tan grande que probar todas es fisicamente imposible.

El tamano del espacio de llaves es la diferencia entre un cifrado de juguete y uno real.

### Ejercicio adicional: verifica propiedades de XOR

```python
#!/usr/bin/env python3
"""
xor_propiedades.py - Verifica experimentalmente las propiedades de XOR
que hacen posible la criptografia.
"""

import os


def demostrar_involucion():
    """XOR aplicado dos veces devuelve el valor original."""
    print("=== INVOLUCION: A ^ K ^ K = A ===")
    for _ in range(5):
        a = int.from_bytes(os.urandom(4), 'big')
        k = int.from_bytes(os.urandom(4), 'big')
        cifrado = a ^ k
        descifrado = cifrado ^ k
        assert descifrado == a, "La involucion fallo!"
        print(f"  {a:>12} ^ {k:>12} = {cifrado:>12} ^ {k:>12} = {descifrado:>12} (OK)")
    print()


def demostrar_distribucion():
    """XOR con una llave aleatoria produce una distribucion uniforme."""
    print("=== DISTRIBUCION UNIFORME ===")
    conteo = [0] * 256
    llave = os.urandom(1)[0]
    # XOR de todos los bytes posibles con la misma llave
    for byte in range(256):
        resultado = byte ^ llave
        conteo[resultado] += 1

    # Cada valor debe aparecer exactamente 1 vez (permutacion)
    assert all(c == 1 for c in conteo), "La distribucion no es uniforme!"
    print(f"  XOR con llave={llave:3d}: cada valor de 0-255 aparece exactamente 1 vez")
    print(f"  Esto significa que XOR con una llave fija es una PERMUTACION")
    print(f"  (una biyeccion -- cada entrada produce una salida unica)")
    print()


def demostrar_cancelacion_llave():
    """Muestra por que reutilizar la llave rompe el cifrado."""
    print("=== PELIGRO DE REUTILIZACION ===")
    m1 = b"mensaje secreto uno"
    m2 = b"mensaje secreto dos"
    llave = os.urandom(len(m1))

    c1 = bytes(a ^ b for a, b in zip(m1, llave))
    c2 = bytes(a ^ b for a, b in zip(m2, llave))

    # Al hacer XOR entre los cifrados, la llave desaparece
    c1_xor_c2 = bytes(a ^ b for a, b in zip(c1, c2))
    m1_xor_m2 = bytes(a ^ b for a, b in zip(m1, m2))

    print(f"  c1 XOR c2 = {c1_xor_c2.hex()}")
    print(f"  m1 XOR m2 = {m1_xor_m2.hex()}")
    print(f"  Son iguales? {c1_xor_c2 == m1_xor_m2}")
    print(f"  La llave DESAPARECIO. Un atacante tiene m1 XOR m2,")
    print(f"  que revela informacion sobre ambos mensajes.")
    print()


if __name__ == "__main__":
    demostrar_involucion()
    demostrar_distribucion()
    demostrar_cancelacion_llave()
    print("Todas las demostraciones completadas.")
```

---

## Takeaway del capitulo

Con los cinco conceptos de este capitulo entiendes el **90% de la base matematica** de la criptografia practica:

1. **Aritmetica modular**: crea un espacio cerrado donde las operaciones no desbordan. Es la base de RSA, Diffie-Hellman y muchos otros protocolos.

2. **Numeros primos**: son los "atomos" indivisibles. Multiplicar primos es facil; factorizar el producto es casi imposible. RSA depende de esto.

3. **Probabilidad**: te permite cuantificar la seguridad. 2^128 intentos es "imposible". La paradoja del cumpleanos reduce la resistencia a colisiones a la mitad de los bits.

4. **XOR**: la operacion perfecta para cifrar. Autoinversa, uniforme, y la base de la mayoria de los algoritmos simetricos. Pero reutilizar la llave la destruye.

5. **Campos finitos**: formalizan la aritmetica modular. AES trabaja en GF(2^8), RSA en GF(n), las curvas elipticas en GF(p). Todo se queda dentro de un rango controlado.

Cada vez que en los proximos capitulos encontres una operacion que parece misteriosa, regresa aqui. La respuesta probablemente esta en una de estas cinco ideas.

---

**En el siguiente capitulo**, usaremos estas matematicas para construir algo real: entenderemos como funcionan los generadores de numeros aleatorios criptograficos y por que son la base de toda la seguridad informatica.

---

### Referencias del capitulo

- [Aumasson, 2024] Aumasson, J.P. *Serious Cryptography*, 2nd Edition. No Starch Press.
- [Daemen y Rijmen, 2002] Daemen, J. y Rijmen, V. *The Design of Rijndael: AES -- The Advanced Encryption Standard*. Springer.
- [Lenstra et al., 2017] Lenstra, A. et al. "Key Lengths." *Handbook of Financial Cryptography and Security*.
- [NIST SP 800-57, 2020] National Institute of Standards and Technology. "Recommendation for Key Management."
- [Schneier, 2015] Schneier, B. *Applied Cryptography*, 20th Anniversary Edition. Wiley.
- [Shannon, 1949] Shannon, C. "Communication Theory of Secrecy Systems." *Bell System Technical Journal*.
