# Capitulo 9: Numeros aleatorios -- el fundamento invisible de toda la criptografia

> "Si tu fuente de aleatoriedad es mala, nada de lo demas importa. Puedes usar AES-256, puedes usar curvas elipticas, puedes implementar todo perfectamente. Pero si las llaves, los nonces o los IVs que alimentan esos algoritmos son predecibles, un atacante no necesita romper la matematica: solo necesita adivinar tus numeros."

---

En los capitulos anteriores hemos dado por sentado algo fundamental: que podemos generar numeros aleatorios cuando los necesitamos. Cada vez que escribimos `os.urandom(32)` para crear una llave, cada vez que generamos un nonce de 12 bytes para ChaCha20-Poly1305, cada vez que un servidor TLS inicia un handshake, dependemos de que esos bytes sean genuinamente impredecibles.

Pero que significa "genuinamente impredecible"? Como puede una maquina determinista --una computadora que ejecuta instrucciones paso a paso, produciendo siempre el mismo resultado para la misma entrada-- generar algo aleatorio?

La respuesta corta: no puede. Lo que puede hacer es recolectar pedazos de imprevisibilidad del mundo fisico y usarlos como semilla para generadores matematicos disenados para expandir esa imprevisibilidad. El resultado no es aleatoriedad perfecta, pero es suficientemente bueno para que ningun adversario pueda distinguirlo de aleatoriedad verdadera en tiempo razonable.

Este capitulo explora como funciona esa maquinaria, por que es tan fragil, y que sucede cuando falla.

---

## 9.1 Entropia: midiendo la incertidumbre

### 9.1.1 Que es la entropia

El termino "entropia" proviene de la termodinamica, donde mide el desorden de un sistema. Claude Shannon lo adopto en 1948 para la teoria de la informacion, donde mide algo ligeramente diferente: la **cantidad de incertidumbre** en una variable aleatoria [Shannon, 1948].

En criptografia, la entropia responde a una pregunta practica: cuantas posibilidades reales tiene un atacante que quiere adivinar un valor?

Si lanzas una moneda justa, hay dos resultados posibles, cada uno con probabilidad 1/2. La entropia es 1 bit. Si lanzas un dado justo de seis caras, la entropia es log2(6) = 2.58 bits. Si generas una llave de 256 bits verdaderamente aleatoria, la entropia es 256 bits: el atacante necesita probar hasta 2^256 posibilidades.

La formula matematica de Shannon para la entropia es:

```
H(X) = -SUM(p(xi) * log2(p(xi)))

Donde:
  X    = variable aleatoria
  xi   = cada valor posible
  p(xi) = probabilidad de ese valor
```

### 9.1.2 Entropia en la practica

Veamos la entropia con codigo:

```python
"""
entropia_demo.py

Calcula la entropia de Shannon de diferentes fuentes de datos.
"""

import math
from collections import Counter


def entropia_shannon(datos: bytes) -> float:
    """
    Calcula la entropia de Shannon en bits por byte.
    Maximo teorico: 8.0 bits/byte (distribucion uniforme de 256 valores).
    """
    if not datos:
        return 0.0

    conteo = Counter(datos)
    total = len(datos)

    entropia = 0.0
    for frecuencia in conteo.values():
        probabilidad = frecuencia / total
        if probabilidad > 0:
            entropia -= probabilidad * math.log2(probabilidad)

    return entropia


# --- Ejemplos ---

# 1. Texto en espanol: baja entropia (muchas letras repetidas)
texto = b"En un lugar de la Mancha de cuyo nombre no quiero acordarme"
print(f"Texto espanol:    {entropia_shannon(texto):.2f} bits/byte")

# 2. Bytes de un contador: baja entropia
contador = bytes(range(256)) * 4
print(f"Contador 0-255:   {entropia_shannon(contador):.2f} bits/byte")

# 3. Bytes aleatorios del sistema operativo: alta entropia
import os
aleatorio = os.urandom(1024)
print(f"os.urandom(1024): {entropia_shannon(aleatorio):.2f} bits/byte")

# 4. Todos ceros: entropia minima
ceros = bytes(1024)
print(f"Todos ceros:      {entropia_shannon(ceros):.2f} bits/byte")
```

Salida tipica:

```
Texto espanol:    4.52 bits/byte
Contador 0-255:   8.00 bits/byte
os.urandom(1024): 7.98 bits/byte
Todos ceros:      0.00 bits/byte
```

Un detalle importante: la entropia de Shannon mide la distribucion estadistica de los bytes, no su imprevisibilidad criptografica. Un contador de 0 a 255 tiene entropia de Shannon perfecta (8.0 bits/byte) porque cada valor aparece con la misma frecuencia, pero es completamente predecible. Para criptografia necesitamos algo mas fuerte: que un adversario computacionalmente poderoso no pueda predecir el siguiente byte dado todos los anteriores.

### 9.1.3 Fuentes de entropia en una computadora

Una computadora recolecta entropia de multiples fuentes fisicas:

```
Fuentes de entropia tipicas en un sistema moderno:

+--------------------------------------------+
|  HARDWARE                                  |
|  - Ruido termico en semiconductores        |
|  - Variaciones en el reloj del CPU         |
|  - RDRAND/RDSEED (Intel/AMD)               |
|  - Generadores cuanticos (QRNG)            |
+--------------------------------------------+
         |
         v
+--------------------------------------------+
|  SISTEMA OPERATIVO                         |
|  - Tiempos de interrupciones de hardware   |
|  - Variaciones en acceso a disco           |
|  - Tiempos de paquetes de red              |
|  - Movimiento del raton / teclado          |
|  - Jitter del reloj entre CPUs             |
+--------------------------------------------+
         |
         v
+--------------------------------------------+
|  POOL DE ENTROPIA DEL KERNEL               |
|  (Linux: /dev/urandom, /dev/random)        |
|  (Windows: CryptGenRandom / BCryptGenRandom)|
|  (macOS: Fortuna -> /dev/urandom)          |
+--------------------------------------------+
         |
         v
+--------------------------------------------+
|  APLICACION                                |
|  os.urandom(), secrets, SecureRandom, etc. |
+--------------------------------------------+
```

El sistema operativo actua como un intermediario que recolecta entropia de multiples fuentes, la mezcla en un pool interno, y la distribuye a las aplicaciones cuando la solicitan. Este diseno es fundamental porque ninguna fuente individual de entropia es completamente confiable.

---

## 9.2 True RNG vs Pseudo-RNG vs CSPRNG: tres niveles, tres usos

### 9.2.1 True Random Number Generators (TRNG)

Un generador de numeros verdaderamente aleatorios extrae su imprevisibilidad directamente de fenomenos fisicos. Los mas comunes:

- **Ruido termico en semiconductores**: las fluctuaciones aleatorias de electrones en un circuito generan voltajes impredecibles.
- **Decaimiento radioactivo**: fundamentalmente impredecible segun la mecanica cuantica.
- **Generadores cuanticos (QRNG)**: miden propiedades cuanticas como la polarizacion de fotones.
- **Instrucciones de hardware**: Intel RDRAND y RDSEED, ARM RNDR.

```
TRNG: Fenomeno fisico -> Medicion -> Bits aleatorios

  Ruido termico
  en circuito     -->  [ADC]  -->  101001110010...
                       (medicion)   (bits verdaderamente
                                     aleatorios)
```

**Ventajas**: la aleatoriedad es genuina, no depende de ninguna suposicion matematica.

**Desventajas**: son lentos (tipicamente kilobits por segundo para TRNG puros), pueden ser sesgados por condiciones fisicas, y son vulnerables a manipulacion del entorno (temperatura, voltaje, campos electromagneticos).

### 9.2.2 Pseudo-Random Number Generators (PRNG)

Un PRNG es un algoritmo determinista que, dada una semilla inicial, produce una secuencia de numeros que *parece* aleatoria pero es completamente predecible si conoces la semilla y el algoritmo.

```
PRNG: Semilla -> Algoritmo determinista -> Secuencia "aleatoria"

  Semilla: 42
      |
      v
  [Mersenne Twister]  -->  0.37454  0.95071  0.73199  0.59865 ...
      |
  Misma semilla = misma secuencia. SIEMPRE.
```

El ejemplo mas conocido es **Mersenne Twister** (MT19937), usado internamente por `random.random()` en Python, `Math.random()` en JavaScript, y funciones analogas en la mayoria de los lenguajes. Es excelente para simulaciones y juegos, pero **completamente inadecuado para criptografia** por tres razones:

1. **Es predecible**: observando 624 salidas consecutivas de MT19937, puedes reconstruir el estado interno completo y predecir todas las salidas futuras (y pasadas).
2. **No tiene forward secrecy**: si un atacante obtiene el estado interno en cualquier momento, puede calcular toda la secuencia.
3. **Su periodo, aunque largo (2^19937 - 1), no compensa la predecibilidad**: la longitud del periodo no importa si puedes reconstruir el estado.

```python
"""
mersenne_twister_predecible.py

Demuestra que Mersenne Twister es predecible.
NUNCA uses random() para criptografia.
"""

import random

# Fijar la semilla
random.seed(12345)

# Generar 10 numeros "aleatorios"
secuencia1 = [random.random() for _ in range(10)]

# Reiniciar con la misma semilla
random.seed(12345)

# La secuencia es IDENTICA
secuencia2 = [random.random() for _ in range(10)]

assert secuencia1 == secuencia2
print("Misma semilla = misma secuencia.")
print(f"Primeros 5 valores: {secuencia1[:5]}")

# En criptografia, un atacante que conozca la semilla
# puede calcular TODAS las llaves, nonces y tokens generados.
```

### 9.2.3 Cryptographically Secure PRNG (CSPRNG)

Un CSPRNG es un PRNG con dos propiedades adicionales que lo hacen seguro para criptografia:

1. **Forward secrecy (discrecion hacia adelante)**: conocer los bits generados hasta ahora no permite predecir los bits futuros. Formalmente: no existe un algoritmo de tiempo polinomial que, dados los primeros N bits de la salida, pueda predecir el bit N+1 con probabilidad significativamente mayor que 50%.

2. **Backward secrecy (discrecion hacia atras)**: si un atacante obtiene el estado interno del generador en un momento dado, no puede reconstruir los bits generados anteriormente. Esto se logra mediante operaciones no invertibles en la actualizacion del estado.

```
CSPRNG: Entropia real + Algoritmo seguro -> Bits indistinguibles de aleatorio

  Pool de entropia
  del kernel          Semilla de alta entropia
      |               |
      v               v
  +--[CSPRNG: CTR_DRBG, HMAC_DRBG, etc.]--+
  |                                         |
  |  Estado interno                         |
  |  (se actualiza continuamente con        |
  |   nueva entropia del pool)              |
  |                                         |
  +----> Bits criptograficamente seguros    |
         0xA3 0x7F 0x12 0xE8 ...            |
                                            |
  Si el estado se compromete en T=5:        |
  - No puedes reconstruir salida de T<5     |
  - Tras re-seed, T>5 es seguro de nuevo    |
  +------------------------------------------+
```

La diferencia fundamental entre un PRNG y un CSPRNG no es solo la calidad estadistica de la salida --ambos pueden pasar tests estadisticos como NIST SP 800-22 o TestU01--. La diferencia es que un CSPRNG resiste a un adversario computacionalmente poderoso que intenta predecir la salida, mientras que un PRNG no.

### 9.2.4 Comparacion directa

```
+------------------+------------+-----------+-----------+
| Propiedad        | TRNG       | PRNG      | CSPRNG    |
+------------------+------------+-----------+-----------+
| Fuente           | Fisica     | Semilla   | Entropia  |
|                  |            |           | + semilla |
| Determinista     | No         | Si        | Si *      |
| Predecible       | No         | Si        | No **     |
| Velocidad        | Lenta      | Rapida    | Rapida    |
| Forward secrecy  | N/A        | No        | Si        |
| Backward secrecy | N/A        | No        | Si        |
| Uso cripto       | Semilla    | NUNCA     | SI        |
| Ejemplo          | RDRAND     | MT19937   | /dev/     |
|                  |            |           | urandom   |
+------------------+------------+-----------+-----------+

*  Determinista dado el estado, pero el estado incluye
   entropia del mundo real que lo hace impredecible.
** No predecible sin conocer el estado interno, y el estado
   se actualiza constantemente con nueva entropia.
```

---

## 9.3 /dev/urandom, os.urandom(), secrets: que usar en cada lenguaje

### 9.3.1 El debate /dev/random vs /dev/urandom: resuelto

Durante anos, existio un debate en la comunidad de seguridad sobre cual de los dos dispositivos de Linux era "mas seguro":

- `/dev/random`: bloquea cuando el kernel estima que no hay suficiente entropia en el pool.
- `/dev/urandom`: nunca bloquea; si el pool esta bajo en entropia estimada, sigue generando bytes usando su estado interno.

El argumento a favor de `/dev/random` era que "garantizaba" entropia real. Pero este argumento es erroneo por varias razones que criptografos como Daniel Bernstein, Thomas Pornin y otros han explicado extensamente [Bernstein, 2014; Pornin, 2013]:

1. **La estimacion de entropia del kernel es heuristica, no una medicion real**. El kernel no puede saber cuanta entropia verdadera tiene; solo estima basandose en eventos de hardware. Bloquear basandose en una estimacion imprecisa no proporciona garantias reales.

2. **Una vez que el CSPRNG tiene suficiente entropia inicial (~256 bits), su seguridad no depende de recibir mas entropia**. Un CSPRNG correctamente implementado y semillado produce salida computacionalmente indistinguible de aleatoriedad verdadera.

3. **Bloquear causa problemas reales**: servidores que se quedan colgados al arranque esperando entropia, contenedores Docker sin fuentes de entropia de hardware, maquinas virtuales en la nube con entropia limitada.

El consenso actual, expresado tanto por criptografos academicos como por desarrolladores del kernel de Linux, es claro: **usa `/dev/urandom` para todo** [Myths about /dev/urandom, 2014]. La unica excepcion es la generacion de llaves durante el arranque muy temprano del sistema, antes de que el pool de entropia se haya inicializado. Para ese caso, Linux ofrece la llamada al sistema `getrandom()` (desde el kernel 3.17), que bloquea solo hasta que el pool tenga entropia inicial suficiente y luego se comporta como `/dev/urandom`.

A partir del kernel 5.6 de Linux (2020), `/dev/random` y `/dev/urandom` usan internamente el mismo CSPRNG. La unica diferencia es que `/dev/random` puede bloquear si el pool no ha sido inicializado. En la practica, son equivalentes una vez que el sistema arranca.

### 9.3.2 Fuentes criptograficas por sistema operativo

```
+------------------+-------------------------------------------+
| Sistema          | Fuente                                    |
+------------------+-------------------------------------------+
| Linux >= 3.17    | getrandom() (recomendado)                 |
|                  | /dev/urandom (alternativa)                |
| macOS / iOS      | /dev/urandom (Fortuna internamente)       |
|                  | SecRandomCopyBytes() (API nativa)         |
| Windows          | BCryptGenRandom() (moderno)               |
|                  | CryptGenRandom() (legacy, aun soportado)  |
| FreeBSD          | /dev/urandom (Fortuna)                    |
+------------------+-------------------------------------------+
```

### 9.3.3 Que usar en Python

Python ofrece tres niveles de acceso a aleatoriedad criptografica:

```python
"""
fuentes_aleatorias_python.py

Las tres formas correctas de generar aleatoriedad criptografica en Python.
"""

import os
import secrets

# ==================================================================
# Nivel 1: os.urandom() -- acceso directo al CSPRNG del sistema
# ==================================================================

# Genera 32 bytes (256 bits) para una llave AES-256
llave_aes = os.urandom(32)
print(f"Llave AES-256:  {llave_aes.hex()}")

# Genera 12 bytes para un nonce de AES-GCM o ChaCha20-Poly1305
nonce = os.urandom(12)
print(f"Nonce (96 bit): {nonce.hex()}")

# Genera 16 bytes para un IV de AES-CBC
iv = os.urandom(16)
print(f"IV (128 bit):   {iv.hex()}")


# ==================================================================
# Nivel 2: secrets -- modulo de alto nivel (Python 3.6+, PEP 506)
# ==================================================================

# Token hexadecimal seguro (para URLs, APIs, tokens de sesion)
token_hex = secrets.token_hex(32)  # 32 bytes = 64 caracteres hex
print(f"\nToken hex:      {token_hex}")

# Token en bytes (para uso criptografico directo)
token_bytes = secrets.token_bytes(32)
print(f"Token bytes:    {token_bytes.hex()}")

# Token URL-safe en base64
token_url = secrets.token_urlsafe(32)
print(f"Token URL-safe: {token_url}")

# Comparacion en tiempo constante (previene timing attacks)
tag_esperado = b"etiqueta_correcta"
tag_recibido = b"etiqueta_correcta"
es_valido = secrets.compare_digest(tag_esperado, tag_recibido)
print(f"\nComparacion constant-time: {es_valido}")

# Eleccion aleatoria segura (para passwords, seleccion de items)
import string
alfabeto = string.ascii_letters + string.digits + "!@#$%"
password = ''.join(secrets.choice(alfabeto) for _ in range(20))
print(f"Password seguro: {password}")

# Numero entero aleatorio en un rango
valor = secrets.randbelow(2**128)
print(f"Entero < 2^128: {valor}")


# ==================================================================
# Nivel 3: SystemRandom -- clase que usa el CSPRNG del sistema
# ==================================================================

import random

# SystemRandom usa os.urandom() internamente, no Mersenne Twister
rng_seguro = random.SystemRandom()

# util cuando necesitas la interfaz de random pero con seguridad
dado = rng_seguro.randint(1, 6)
elemento = rng_seguro.choice(["opcion_a", "opcion_b", "opcion_c"])
print(f"\nSystemRandom dado:     {dado}")
print(f"SystemRandom eleccion: {elemento}")
```

**Regla general**: para criptografia directa (llaves, nonces, IVs), usa `os.urandom()`. Para tokens, passwords y APIs, usa `secrets`. Nunca uses el modulo `random` para nada relacionado con seguridad.

### 9.3.4 Que usar en otros lenguajes

```python
"""
REFERENCIA RAPIDA: Fuentes criptograficas por lenguaje

+---------------+-----------------------------------------+-----------------------------+
| Lenguaje      | Funcion correcta                        | Funcion INCORRECTA          |
+---------------+-----------------------------------------+-----------------------------+
| Python        | os.urandom(), secrets                   | random.random()             |
|               |                                         | random.randbytes()          |
+---------------+-----------------------------------------+-----------------------------+
| JavaScript    | crypto.getRandomValues() (browser)      | Math.random()               |
| (Node.js)     | crypto.randomBytes() (Node)             |                             |
+---------------+-----------------------------------------+-----------------------------+
| Go            | crypto/rand.Read()                      | math/rand                   |
+---------------+-----------------------------------------+-----------------------------+
| Rust          | rand::rngs::OsRng                       | rand::rngs::SmallRng        |
|               | getrandom crate                         | (para no-cripto)            |
+---------------+-----------------------------------------+-----------------------------+
| Java          | java.security.SecureRandom              | java.util.Random            |
+---------------+-----------------------------------------+-----------------------------+
| C/C++         | getrandom() (Linux)                     | rand()                      |
|               | BCryptGenRandom (Windows)               | srand(time(NULL))           |
|               | arc4random_buf() (BSD/macOS)            |                             |
+---------------+-----------------------------------------+-----------------------------+
| Ruby          | SecureRandom.random_bytes               | rand()                      |
+---------------+-----------------------------------------+-----------------------------+
| PHP           | random_bytes() (PHP 7+)                 | rand()                      |
|               | random_int()                            | mt_rand()                   |
+---------------+-----------------------------------------+-----------------------------+

REGLA UNIVERSAL: usa el modulo "crypto" o "security" de tu lenguaje.
                  NUNCA el modulo "math" o la funcion "rand" generica.
"""
```

---

## 9.4 Errores clasicos: semillas predecibles, PRNG en lugar de CSPRNG

### 9.4.1 Error 1: Usar random() para generar tokens de sesion

Este es probablemente el error mas comun en aplicaciones web:

```python
"""
error_random_tokens.py

[PELIGRO] Este codigo genera tokens de sesion predecibles.
"""

import random
import time

# ERROR: sembrar con el tiempo actual
random.seed(int(time.time()))

# ERROR: generar token con PRNG no criptografico
token = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=32))
print(f"Token 'aleatorio': {token}")

# Un atacante que conozca la hora aproximada del servidor
# (con precision de +/- 1 segundo) solo necesita probar ~2 semillas.
# Con precision de +/- 1 hora: 3600 semillas.
# Con precision de +/- 1 dia: 86400 semillas.
#
# TRIVIAL de adivinar por fuerza bruta.
```

La correccion es simple:

```python
"""
correccion_random_tokens.py

[BUENA PRACTICA] Tokens de sesion criptograficamente seguros.
"""

import secrets

# CORRECTO: usar secrets para generar tokens
token = secrets.token_urlsafe(32)  # 256 bits de entropia
print(f"Token seguro: {token}")

# Esto produce tokens como:
# "xY9kMp2-q5R8tW3v_nB7dF1hJ4cL6aE0gI2mK"
# Con 256 bits de entropia, un atacante necesita ~2^256 intentos.
```

### 9.4.2 Error 2: Sembrar un PRNG con el PID del proceso

Este es exactamente lo que sucedio con el bug de Debian OpenSSL (que veremos en detalle mas adelante):

```python
"""
error_semilla_pid.py

[PELIGRO] Demuestra por que el PID es una semilla terrible.
"""

import os
import random
import hashlib

# Simular el error de Debian: usar solo el PID como semilla
pid = os.getpid()
random.seed(pid)

# "Generar" una llave
llave_mala = random.randbytes(32)
print(f"PID actual: {pid}")
print(f"Llave generada: {llave_mala.hex()}")

# Un atacante solo necesita probar ~32768 semillas (PIDs posibles en Linux)
print(f"\nPIDs posibles en Linux: {32768}")
print(f"Tiempo para probar todas: < 1 segundo")

# Demostracion: adivinar la llave
for pid_candidato in range(1, 32769):
    random.seed(pid_candidato)
    llave_candidata = random.randbytes(32)
    if llave_candidata == llave_mala:
        print(f"\nLlave encontrada con PID = {pid_candidato}")
        break
```

### 9.4.3 Error 3: Reutilizar nonces

Ya vimos este error en el capitulo 8 (caso Sony PS3), pero vale la pena reforzarlo:

```python
"""
error_nonce_reutilizado.py

[PELIGRO] Demostrar el peligro de reutilizar nonces.
"""

import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

llave = os.urandom(32)
chacha = ChaCha20Poly1305(llave)

# Generar un nonce... y reutilizarlo (ERROR FATAL)
nonce = os.urandom(12)

mensaje1 = b"Transferir $100 a cuenta A"
mensaje2 = b"Password: super_secreto!!"

# Cifrar dos mensajes con el mismo nonce
cifrado1 = chacha.encrypt(nonce, mensaje1, None)
cifrado2 = chacha.encrypt(nonce, mensaje2, None)

# Un atacante con ambos textos cifrados puede obtener m1 XOR m2
# (el tag de Poly1305 tambien se compromete)

print("[PELIGRO] Ambos mensajes cifrados con el mismo nonce.")
print("Un atacante puede recuperar informacion de ambos mensajes.")

# CORRECTO: un nonce nuevo para cada mensaje
nonce1 = os.urandom(12)
nonce2 = os.urandom(12)
cifrado1_seguro = chacha.encrypt(nonce1, mensaje1, None)
cifrado2_seguro = chacha.encrypt(nonce2, mensaje2, None)
print("\n[CORRECTO] Cada mensaje con su propio nonce.")
```

### 9.4.4 Error 4: Confiar en Math.random() de JavaScript

```
// [PELIGRO] Este codigo es vulnerable
function generarTokenSesion() {
    return Math.random().toString(36).substring(2);
}

// Math.random() usa xoshiro256** en V8 (Chrome/Node):
// - Estado interno de 256 bits
// - Predecible con suficientes muestras
// - No usa entropia del sistema operativo

// [CORRECTO] Usar crypto
function generarTokenSeguro() {
    const bytes = new Uint8Array(32);
    crypto.getRandomValues(bytes);
    return Array.from(bytes, b => b.toString(16).padStart(2, '0')).join('');
}
```

---

## 9.5 NIST SP 800-90A: los generadores estandarizados

### 9.5.1 El marco DRBG

El NIST (National Institute of Standards and Technology) publico en 2006 la especificacion SP 800-90A, que define tres mecanismos para generadores de bits aleatorios deterministas (DRBG: Deterministic Random Bit Generator) [NIST, 2015]:

1. **Hash_DRBG**: basado en funciones hash (SHA-256, SHA-512).
2. **HMAC_DRBG**: basado en HMAC (que veremos en el capitulo 10).
3. **CTR_DRBG**: basado en cifrados de bloque en modo contador (AES-128, AES-256).

Los tres comparten una arquitectura comun con cuatro operaciones:

```
DRBG: Arquitectura general

1. Instantiate(entropia, nonce, personalization)
   --> Inicializa el estado interno
   --> La entropia viene del pool del sistema
   --> El nonce garantiza unicidad
   --> personalization: datos opcionales del contexto

2. Reseed(entropia_nueva)
   --> Actualiza el estado con nueva entropia
   --> Proporciona backward secrecy

3. Generate(num_bytes)
   --> Produce bytes pseudo-aleatorios
   --> Actualiza el estado interno

4. Uninstantiate()
   --> Destruye el estado (zeroization)
   --> Previene extraccion forense
```

### 9.5.2 CTR_DRBG: el mas usado

CTR_DRBG es el DRBG mas comun en implementaciones reales porque aprovecha las instrucciones AES-NI del hardware. OpenSSL lo usa por defecto desde la version 1.1.1.

El funcionamiento simplificado:

```
CTR_DRBG con AES-256:

Estado interno:
  - V: valor de 128 bits (el contador)
  - Key: llave AES de 256 bits

Generate(N bytes):
  1. Incrementar V
  2. output_block = AES_Encrypt(Key, V)
  3. Repetir hasta generar N bytes
  4. Actualizar (Key, V) usando la salida:
     Key || V = AES_CTR(Key, V, 0x00...00)
  5. Retornar los N bytes

  +------+     +-----+     +------------------+
  | Key  |---->| AES |---->| output_block     |
  +------+     +-----+     +------------------+
                  ^
                  |
               +-----+
               |  V  | (contador, se incrementa)
               +-----+
```

El paso 4 es crucial: despues de generar salida, el estado se actualiza de manera que conocer la salida no revela el estado. Esto proporciona forward secrecy.

### 9.5.3 HMAC_DRBG: el mas conservador

HMAC_DRBG es preferido en contextos donde se quiere evitar depender de la seguridad de un cifrado de bloque. Su estado interno se actualiza usando HMAC, que tiene pruebas formales de seguridad bajo suposiciones mas debiles [Bellare, Canetti, Krawczyk, 1996]:

```python
"""
hmac_drbg_simplificado.py

Implementacion educativa simplificada de HMAC_DRBG.
Basada en NIST SP 800-90A seccion 10.1.2.
NO USAR EN PRODUCCION -- usa la implementacion del sistema.
"""

import hmac
import hashlib


class HMAC_DRBG_Educativo:
    """
    HMAC_DRBG simplificado con SHA-256.
    Solo para fines educativos.
    """

    def __init__(self, entropia: bytes, nonce: bytes = b"",
                 personalization: bytes = b""):
        """Instantiate: inicializa el estado con entropia."""
        self.K = b"\x00" * 32  # Llave HMAC: 32 bytes de ceros
        self.V = b"\x01" * 32  # Valor V: 32 bytes de unos

        semilla = entropia + nonce + personalization
        self._actualizar(semilla)

    def _hmac(self, datos: bytes) -> bytes:
        """Calcula HMAC-SHA-256 con la llave interna K."""
        return hmac.new(self.K, datos, hashlib.sha256).digest()

    def _actualizar(self, datos_proporcionados: bytes = b"") -> None:
        """Actualiza el estado interno (K, V)."""
        # Paso 1: K = HMAC(K, V || 0x00 || datos)
        self.K = self._hmac(self.V + b"\x00" + datos_proporcionados)
        # Paso 2: V = HMAC(K, V)
        self.V = self._hmac(self.V)

        if datos_proporcionados:
            # Paso 3: K = HMAC(K, V || 0x01 || datos)
            self.K = self._hmac(self.V + b"\x01" + datos_proporcionados)
            # Paso 4: V = HMAC(K, V)
            self.V = self._hmac(self.V)

    def generate(self, num_bytes: int) -> bytes:
        """Generate: produce num_bytes bytes pseudo-aleatorios."""
        resultado = b""
        while len(resultado) < num_bytes:
            self.V = self._hmac(self.V)
            resultado += self.V

        # Actualizar estado (forward secrecy)
        self._actualizar()

        return resultado[:num_bytes]

    def reseed(self, nueva_entropia: bytes) -> None:
        """Reseed: actualiza el estado con nueva entropia."""
        self._actualizar(nueva_entropia)


# --- Demostracion ---
import os

# Instanciar con entropia del sistema
entropia = os.urandom(48)  # 384 bits de entropia
nonce = os.urandom(16)

drbg = HMAC_DRBG_Educativo(entropia, nonce, b"demo_capitulo_9")

# Generar bytes
llave = drbg.generate(32)
nonce_generado = drbg.generate(12)

print(f"Llave:   {llave.hex()}")
print(f"Nonce:   {nonce_generado.hex()}")

# Cada llamada produce salida diferente (el estado se actualiza)
llave2 = drbg.generate(32)
print(f"Llave 2: {llave2.hex()}")
assert llave != llave2  # Siempre diferente

# Re-seed con nueva entropia (backward secrecy)
drbg.reseed(os.urandom(32))
llave3 = drbg.generate(32)
print(f"Llave 3 (post-reseed): {llave3.hex()}")
```

---

## 9.6 Dual_EC_DRBG: la puerta trasera de la NSA

### 9.6.1 El cuarto DRBG

La version original de NIST SP 800-90A (2006) incluia un cuarto generador: **Dual_EC_DRBG** (Dual Elliptic Curve Deterministic Random Bit Generator). A diferencia de los otros tres, este generador fue propuesto directamente por la NSA.

Dual_EC_DRBG era anomalo desde su concepcion. Era ordenes de magnitud mas lento que los otros tres generadores. Su diseno era innecesariamente complejo. Y depenia de dos puntos de curva eliptica, P y Q, cuyos valores habian sido elegidos por la NSA sin explicacion publica de como se seleccionaron [Schneier, 2007].

### 9.6.2 La advertencia temprana

En agosto de 2007, durante la conferencia CRYPTO, los criptografos Dan Shumow y Niels Ferguson presentaron un hallazgo perturbador: si existia una relacion matematica secreta entre los puntos P y Q --especificamente, si alguien conocia un numero `e` tal que Q = e * P--, entonces esa persona podia predecir toda la salida del generador despues de observar solo 32 bytes.

```
La puerta trasera de Dual_EC_DRBG (simplificada):

Parametros publicos: P (punto generador), Q (punto "aleatorio")

Si la NSA conoce 'e' tal que Q = e * P:

  1. El generador publica un punto r * Q como parte de su salida
  2. El atacante calcula: r * Q * e^(-1) = r * P
  3. Con r * P, puede predecir TODO el estado interno
  4. Y con ello, toda la salida futura del generador

  Generador                       Atacante (con 'e')
  ---------                       ------------------
  s_i = (s_{i-1} * P).x
  r_i = (s_i * Q).x              Observa r_i
  output = truncar(r_i)           Calcula e^{-1} * r_i * Q
                                  --> Recupera s_i
                                  --> Predice toda salida futura
```

Bruce Schneier escribio en su blog en noviembre de 2007: "No puedo pensar en ninguna razon para poner una puerta trasera en un estandar criptografico a menos que tengas la intencion de explotarla. Mi recomendacion: no uses Dual_EC_DRBG bajo ninguna circunstancia" [Schneier, 2007].

### 9.6.3 La confirmacion

En septiembre de 2013, documentos filtrados por Edward Snowden confirmaron lo que los criptografos sospechaban. Segun reportes del New York Times y The Guardian, la NSA habia trabajado activamente durante el proceso de estandarizacion para convertirse en la unica editora del estandar Dual_EC_DRBG, con el objetivo expreso de mantener una capacidad de acceso a las comunicaciones cifradas.

En diciembre de 2013, Reuters revelo que RSA Security habia recibido un pago secreto de 10 millones de dolares de la NSA para que Dual_EC_DRBG fuera el generador por defecto en BSAFE, su libreria criptografica ampliamente usada [Reuters, 2013].

### 9.6.4 Juniper Networks: la puerta trasera de la puerta trasera

En 2015, Juniper Networks revelo que habia descubierto "codigo no autorizado" en ScreenOS, el sistema operativo de sus firewalls. La investigacion revelo que ScreenOS usaba Dual_EC_DRBG, y que alguien --se desconoce quien-- habia reemplazado los puntos de curva Q del NIST por otros diferentes.

Esto significaba que quien hubiera insertado los nuevos puntos poseia su propia puerta trasera en el generador, permitiendole descifrar todo el trafico VPN de los firewalls de Juniper. Era una puerta trasera dentro de una puerta trasera.

### 9.6.5 El desenlace

En abril de 2014, el NIST retiro oficialmente Dual_EC_DRBG de SP 800-90A Revision 1.

Las lecciones son profundas y multiples:

1. **La procedencia de un algoritmo importa tanto como su diseno**. Un algoritmo propuesto por una agencia de inteligencia sin justificacion transparente de sus parametros debe tratarse con escepticismo extremo.

2. **"Nada bajo la manga" (nothing-up-my-sleeve numbers)**: los parametros criptograficos deben generarse de forma verificable. Los puntos P y Q de Dual_EC_DRBG no tenian justificacion publica. Contrasta esto con las constantes de SHA-256 (derivadas de las raices cuadradas de los primeros 8 primos) o las de ChaCha20 ("expand 32-byte k" en ASCII).

3. **La estandarizacion no garantiza seguridad**. Un estandar del NIST, aprobado por un proceso formal, contenia una puerta trasera deliberada. La confianza debe basarse en la transparencia del proceso y la verificabilidad de los parametros, no solo en la autoridad del emisor.

4. **Nunca uses un CSPRNG que no sea el proporcionado por tu sistema operativo**, a menos que tengas razones extraordinarias y la experiencia para evaluarlo.

---

## 9.7 Codigo Python: genera llaves, IVs y nonces correctamente

### 9.7.1 Funcion de generacion de llaves

```python
"""
generacion_llaves.py

Generacion correcta de llaves, IVs y nonces para diferentes algoritmos.
"""

import os
import secrets
from enum import Enum


class Algoritmo(Enum):
    """Algoritmos soportados y sus parametros."""
    AES_128_GCM = {"llave": 16, "nonce": 12, "nombre": "AES-128-GCM"}
    AES_256_GCM = {"llave": 32, "nonce": 12, "nombre": "AES-256-GCM"}
    AES_256_CBC = {"llave": 32, "iv": 16, "nombre": "AES-256-CBC"}
    CHACHA20_POLY1305 = {"llave": 32, "nonce": 12, "nombre": "ChaCha20-Poly1305"}
    XCHACHA20_POLY1305 = {"llave": 32, "nonce": 24, "nombre": "XChaCha20-Poly1305"}
    HMAC_SHA256 = {"llave": 32, "nombre": "HMAC-SHA-256"}


def generar_llave(algoritmo: Algoritmo) -> bytes:
    """
    Genera una llave criptografica del tamano correcto.
    Usa os.urandom() que lee del CSPRNG del sistema operativo.
    """
    params = algoritmo.value
    tamano = params["llave"]
    return os.urandom(tamano)


def generar_nonce(algoritmo: Algoritmo) -> bytes:
    """
    Genera un nonce del tamano correcto para el algoritmo.
    Cada nonce DEBE ser unico para cada mensaje cifrado con la misma llave.
    """
    params = algoritmo.value
    if "nonce" in params:
        return os.urandom(params["nonce"])
    elif "iv" in params:
        return os.urandom(params["iv"])
    else:
        raise ValueError(f"{params['nombre']} no requiere nonce/IV")


def generar_material_criptografico(algoritmo: Algoritmo) -> dict:
    """
    Genera todo el material criptografico necesario para un algoritmo.
    Retorna un diccionario con llave y nonce/IV si aplica.
    """
    params = algoritmo.value
    resultado = {
        "algoritmo": params["nombre"],
        "llave": generar_llave(algoritmo),
    }

    if "nonce" in params:
        resultado["nonce"] = generar_nonce(algoritmo)
    elif "iv" in params:
        resultado["iv"] = generar_nonce(algoritmo)

    return resultado


# --- Demostracion ---

print("Generacion de material criptografico")
print("=" * 55)

for algo in Algoritmo:
    material = generar_material_criptografico(algo)
    print(f"\n{material['algoritmo']}:")
    print(f"  Llave ({len(material['llave']) * 8} bits): {material['llave'].hex()}")
    if "nonce" in material:
        print(f"  Nonce ({len(material['nonce']) * 8} bits): {material['nonce'].hex()}")
    elif "iv" in material:
        print(f"  IV    ({len(material['iv']) * 8} bits): {material['iv'].hex()}")
```

### 9.7.2 Gestion segura de llaves con contexto

```python
"""
gestion_segura_llaves.py

Patron para gestion segura de material criptografico en memoria.
"""

import os
import ctypes


class LlaveSegura:
    """
    Envoltorio para material criptografico que se limpia
    de memoria al dejar de usarse.
    """

    def __init__(self, tamano_bytes: int):
        """Genera y almacena una llave criptografica."""
        self._datos = bytearray(os.urandom(tamano_bytes))
        self._tamano = tamano_bytes
        self._activa = True

    @property
    def bytes(self) -> bytes:
        """Accede al material criptografico."""
        if not self._activa:
            raise RuntimeError("Llave ya destruida")
        return bytes(self._datos)

    def destruir(self) -> None:
        """
        Sobreescribe la llave en memoria con ceros.
        No es una garantia absoluta (el garbage collector
        puede haber copiado los datos), pero es mejor practica
        que dejar la llave en memoria indefinidamente.
        """
        if self._activa:
            # Sobreescribir con ceros
            for i in range(self._tamano):
                self._datos[i] = 0
            self._activa = False

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.destruir()

    def __del__(self):
        self.destruir()

    def __repr__(self) -> str:
        if self._activa:
            return f"LlaveSegura({self._tamano} bytes, activa)"
        return f"LlaveSegura({self._tamano} bytes, DESTRUIDA)"


# --- Uso con context manager ---

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

mensaje = b"Datos confidenciales que quiero proteger"

with LlaveSegura(32) as llave:
    print(f"Llave: {llave}")

    # Cifrar
    aesgcm = AESGCM(llave.bytes)
    nonce = os.urandom(12)
    cifrado = aesgcm.encrypt(nonce, mensaje, None)
    print(f"Cifrado: {cifrado.hex()[:40]}...")

# Fuera del bloque with, la llave se destruyo
print(f"Llave: {llave}")  # "LlaveSegura(32 bytes, DESTRUIDA)"

# Descifrar requiere la misma llave (guardada de otra forma)
# En produccion, las llaves se almacenan en:
# - Hardware Security Modules (HSM)
# - Key Management Services (AWS KMS, Google Cloud KMS)
# - Vaults (HashiCorp Vault)
# NUNCA en codigo fuente, variables de entorno sin proteccion,
# o archivos de configuracion sin cifrar.
```

### 9.7.3 Verificacion de calidad de entropia

```python
"""
verificar_entropia.py

Verifica que tu sistema genera bytes con entropia adecuada.
"""

import os
import math
from collections import Counter


def test_entropia(datos: bytes, nombre: str) -> None:
    """
    Ejecuta pruebas basicas de entropia sobre un bloque de bytes.
    Estas NO son pruebas criptograficas formales (para eso usa
    NIST SP 800-22 o TestU01), pero detectan problemas obvios.
    """
    n = len(datos)
    print(f"\n{'=' * 50}")
    print(f"Test de entropia: {nombre} ({n} bytes)")
    print(f"{'=' * 50}")

    # 1. Entropia de Shannon
    conteo = Counter(datos)
    entropia = -sum(
        (c / n) * math.log2(c / n)
        for c in conteo.values()
        if c > 0
    )
    print(f"Entropia de Shannon: {entropia:.4f} bits/byte (ideal: 8.0)")

    # 2. Distribucion de bytes
    esperado = n / 256
    chi_cuadrado = sum(
        (conteo.get(i, 0) - esperado) ** 2 / esperado
        for i in range(256)
    )
    # Para 255 grados de libertad, chi-cuadrado < 310 es aceptable (p > 0.05)
    print(f"Chi-cuadrado: {chi_cuadrado:.2f} (< 310 es aceptable)")

    # 3. Proporcion de bits en 1
    total_bits = sum(bin(b).count('1') for b in datos)
    proporcion = total_bits / (n * 8)
    print(f"Proporcion de 1s: {proporcion:.4f} (ideal: 0.5000)")

    # 4. Bytes unicos
    unicos = len(conteo)
    print(f"Bytes unicos: {unicos}/256 ({unicos/256*100:.1f}%)")

    # Veredicto
    ok = (entropia > 7.9 and
          chi_cuadrado < 310 and
          0.48 < proporcion < 0.52 and
          unicos > 240)
    print(f"\nVeredicto: {'ACEPTABLE' if ok else 'SOSPECHOSO'}")


# Probar con diferentes fuentes
test_entropia(os.urandom(10000), "os.urandom()")

import random
random.seed(42)
test_entropia(random.randbytes(10000), "random.randbytes() (semilla fija)")

# Nota: random.randbytes() pasara los tests estadisticos
# porque Mersenne Twister tiene buena distribucion.
# La diferencia es que es PREDECIBLE, no que sea estadisticamente malo.
# Los tests estadisticos NO detectan predecibilidad criptografica.
```

---

## 9.8 Casos reales

### 9.8.1 Debian OpenSSL (2008): 32,767 llaves para todo el mundo

En mayo de 2008, Luciano Bello descubrio que el paquete OpenSSL de Debian y Ubuntu tenia un generador de numeros aleatorios completamente roto desde septiembre de 2006 --casi dos anos de vulnerabilidad silenciosa.

La causa fue tragicamente simple. En 2006, Kurt Roeckx, un mantenedor de Debian, uso Valgrind (una herramienta de deteccion de errores de memoria) para analizar OpenSSL. Valgrind reporto que el codigo usaba memoria no inicializada. Roeckx comento dos lineas de codigo para silenciar la advertencia.

Esas dos lineas eran la fuente principal de entropia del generador. Sin ellas, el PRNG de OpenSSL se semillaba unicamente con el PID (Process ID) del proceso, un numero entre 1 y 32,768 en Linux [Debian Security Advisory DSA-1571, 2008].

El impacto fue devastador:

- **Todas** las llaves SSH generadas en Debian/Ubuntu durante ese periodo eran una de solo 32,767 posibilidades.
- **Todas** las llaves SSL/TLS generadas en ese periodo eran igualmente predecibles.
- Un atacante podia generar las 32,767 llaves posibles para cada tipo y tamano de llave, y probarlas sistematicamente contra cualquier servidor.

La leccion no es solo tecnica sino organizacional: no modifiques codigo criptografico sin entenderlo a profundidad. Lo que parece un "bug" puede ser un comportamiento intencional y critico.

### 9.8.2 PlayStation 3 (2010): el nonce que se reutilizo

Este caso, que ya mencionamos en el capitulo 8, es relevante tambien desde la perspectiva de la aleatoriedad. Sony firmaba el firmware de la PS3 con ECDSA, que requiere un nonce aleatorio unico `k` para cada firma. Sony genero `k` una vez y lo reutilizo para todas las firmas.

Con dos firmas que comparten el mismo `k`, la llave privada se puede extraer algebraicamente. El grupo fail0verflow publico la llave privada de Sony en el 27th Chaos Communication Congress [fail0verflow, 2010].

El error de Sony no fue usar un mal generador de numeros aleatorios. Fue no usar ninguno: un valor fijo no es un valor aleatorio.

### 9.8.3 Android SecureRandom (2013): Bitcoin en peligro

En agosto de 2013, se descubrio que la implementacion de `java.security.SecureRandom` en Android tenia un defecto que hacia que las llaves ECDSA generadas por aplicaciones de Bitcoin fueran predecibles.

El problema: la clase `SecureRandom` de Android no inicializaba correctamente su pool de entropia en ciertas versiones. El resultado fue que multiples usuarios de billeteras Bitcoin generaron llaves que compartian componentes, permitiendo a atacantes extraer llaves privadas y robar bitcoins [Bitcoin.org Security Advisory, 2013].

Google publico un parche que corrigio la inicializacion de `SecureRandom` e instruyo a los desarrolladores de aplicaciones de Bitcoin a generar nuevas llaves.

---

## 9.9 Ejercicio integrador: generador de material criptografico con auditoria

```python
"""
ejercicio_cap9_generador_seguro.py

Ejercicio integrador del Capitulo 9.

Objetivos:
1. Construir un generador de material criptografico para una aplicacion.
2. Implementar un HMAC_DRBG educativo y compararlo con os.urandom().
3. Demostrar el ataque a un PRNG con semilla predecible.
4. Verificar la calidad de la salida con pruebas estadisticas.

Prerequisitos:
  pip install cryptography
"""

import os
import hmac
import hashlib
import math
import time
import random
from collections import Counter
from cryptography.hazmat.primitives.ciphers.aead import (
    AESGCM, ChaCha20Poly1305
)


# ---------- Parte 1: Generador de material criptografico ----------

print("=" * 65)
print("PARTE 1: Generador de material criptografico")
print("=" * 65)


class MaterialCriptografico:
    """
    Genera y gestiona material criptografico para una aplicacion.
    Registra cada generacion para auditoria.
    """

    def __init__(self, nombre_app: str):
        self.nombre_app = nombre_app
        self.registro = []

    def generar_llave_aes256(self) -> bytes:
        """Genera una llave AES-256 (32 bytes)."""
        llave = os.urandom(32)
        self._registrar("AES-256 key", 32)
        return llave

    def generar_llave_chacha20(self) -> bytes:
        """Genera una llave ChaCha20-Poly1305 (32 bytes)."""
        llave = os.urandom(32)
        self._registrar("ChaCha20 key", 32)
        return llave

    def generar_nonce_gcm(self) -> bytes:
        """Genera un nonce para AES-GCM (12 bytes)."""
        nonce = os.urandom(12)
        self._registrar("AES-GCM nonce", 12)
        return nonce

    def generar_nonce_chacha20(self) -> bytes:
        """Genera un nonce para ChaCha20-Poly1305 (12 bytes)."""
        nonce = os.urandom(12)
        self._registrar("ChaCha20 nonce", 12)
        return nonce

    def generar_iv_cbc(self) -> bytes:
        """Genera un IV para AES-CBC (16 bytes)."""
        iv = os.urandom(16)
        self._registrar("AES-CBC IV", 16)
        return iv

    def generar_sal(self, tamano: int = 16) -> bytes:
        """Genera una sal para hashing de passwords (minimo 16 bytes)."""
        if tamano < 16:
            raise ValueError("La sal debe tener al menos 16 bytes")
        sal = os.urandom(tamano)
        self._registrar("Salt", tamano)
        return sal

    def _registrar(self, tipo: str, tamano: int) -> None:
        """Registra una generacion para auditoria."""
        self.registro.append({
            "tipo": tipo,
            "tamano_bytes": tamano,
            "timestamp": time.time(),
            "fuente": "os.urandom"
        })

    def reporte(self) -> str:
        """Genera un reporte de todo el material generado."""
        lineas = [
            f"Reporte de material criptografico: {self.nombre_app}",
            f"Total de generaciones: {len(self.registro)}",
            ""
        ]
        for i, reg in enumerate(self.registro, 1):
            lineas.append(
                f"  {i}. {reg['tipo']} ({reg['tamano_bytes']} bytes) "
                f"via {reg['fuente']}"
            )
        return "\n".join(lineas)


# Usar el generador
gen = MaterialCriptografico("mi_app_segura")

llave = gen.generar_llave_aes256()
nonce = gen.generar_nonce_gcm()
sal = gen.generar_sal()

print(gen.reporte())

# Cifrar algo con el material generado
aesgcm = AESGCM(llave)
mensaje = b"Ejercicio del Capitulo 9: todo funciona!"
cifrado = aesgcm.encrypt(nonce, mensaje, b"capitulo-9")
descifrado = aesgcm.decrypt(nonce, cifrado, b"capitulo-9")
print(f"\nMensaje original:  {mensaje.decode()}")
print(f"Descifrado:        {descifrado.decode()}")
assert mensaje == descifrado


# ---------- Parte 2: Ataque a PRNG con semilla predecible ----------

print("\n" + "=" * 65)
print("PARTE 2: Ataque a PRNG con semilla predecible")
print("=" * 65)


def generar_token_inseguro(semilla: int) -> str:
    """
    [PELIGRO] Genera un token usando random con semilla predecible.
    """
    rng = random.Random(semilla)
    return ''.join(rng.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=32))


# El servidor genera un token usando el timestamp como semilla
timestamp_servidor = int(time.time())
token_victima = generar_token_inseguro(timestamp_servidor)
print(f"Token de la victima: {token_victima}")

# El atacante sabe la hora aproximada (ventana de +/- 10 segundos)
print("\nAtacante: intentando adivinar el token...")
intentos = 0
for offset in range(-10, 11):
    intentos += 1
    semilla_candidata = timestamp_servidor + offset
    token_candidato = generar_token_inseguro(semilla_candidata)
    if token_candidato == token_victima:
        print(f"Token encontrado en {intentos} intentos!")
        print(f"Semilla: {semilla_candidata}")
        break

# Comparar con token seguro
token_seguro = os.urandom(32).hex()
print(f"\nToken seguro: {token_seguro}")
print("Un atacante necesitaria ~2^256 intentos para adivinarlo.")


# ---------- Parte 3: Comparacion estadistica ----------

print("\n" + "=" * 65)
print("PARTE 3: Comparacion estadistica (no detecta predecibilidad)")
print("=" * 65)


def entropia_shannon(datos: bytes) -> float:
    """Calcula entropia de Shannon en bits/byte."""
    n = len(datos)
    conteo = Counter(datos)
    return -sum(
        (c / n) * math.log2(c / n)
        for c in conteo.values()
    )


# Generar datos de ambas fuentes
datos_seguros = os.urandom(10000)
random.seed(42)
datos_inseguros = random.randbytes(10000)

print(f"os.urandom()       entropia: {entropia_shannon(datos_seguros):.4f} bits/byte")
print(f"random.randbytes() entropia: {entropia_shannon(datos_inseguros):.4f} bits/byte")
print("\nAmbos tienen buena entropia estadistica!")
print("Pero random.randbytes() es PREDECIBLE: misma semilla = misma salida.")
print("Los tests estadisticos NO detectan predecibilidad criptografica.")
print("Esta es la razon por la que SIEMPRE debes usar os.urandom() o secrets.")


# ---------- Parte 4: Cifrado completo con material seguro ----------

print("\n" + "=" * 65)
print("PARTE 4: Flujo completo de cifrado con material seguro")
print("=" * 65)

# Generar material para ChaCha20-Poly1305
llave_chacha = os.urandom(32)
chacha = ChaCha20Poly1305(llave_chacha)

# Cifrar multiples mensajes, cada uno con su propio nonce
mensajes = [
    b"Primer mensaje confidencial",
    b"Segundo mensaje con datos sensibles",
    b"Tercer mensaje: coordenadas 19.4326, -99.1332",
]

pares_cifrados = []
for msg in mensajes:
    nonce = os.urandom(12)  # Nonce unico por mensaje
    cifrado = chacha.encrypt(nonce, msg, b"ejercicio-cap9")
    pares_cifrados.append((nonce, cifrado))
    print(f"Cifrado: nonce={nonce.hex()}, datos={cifrado.hex()[:30]}...")

# Descifrar todos
print("\nDescifrado:")
for nonce, cifrado in pares_cifrados:
    descifrado = chacha.decrypt(nonce, cifrado, b"ejercicio-cap9")
    print(f"  {descifrado.decode()}")

print("\nTodos los mensajes cifrados y descifrados correctamente")
print("con material criptografico generado de forma segura.")
```

---

## 9.10 Resumen del capitulo

La aleatoriedad es el fundamento sobre el que se construye toda la criptografia. Sin numeros genuinamente impredecibles, las llaves son adivinables, los nonces se repiten, y los protocolos se derrumban.

**Conceptos clave**:

- **Entropia** mide cuantas posibilidades reales tiene un atacante. Una llave de 256 bits generada correctamente tiene 256 bits de entropia; generada con `random.seed(time())` tiene quiza 20 bits.

- **TRNG** extrae aleatoriedad de fenomenos fisicos. Son lentos pero genuinos.

- **PRNG** produce secuencias que parecen aleatorias pero son deterministas. **Nunca** para criptografia.

- **CSPRNG** combina entropia real con algoritmos disenados para resistir adversarios computacionales. Es lo que debes usar siempre.

- **Los errores de aleatoriedad son invisibles**: bytes generados por un PRNG roto se ven identicos a bytes aleatorios. Solo la revision del codigo fuente puede detectar el problema.

**Regla universal**: para cualquier operacion criptografica, usa `os.urandom()` o `secrets` en Python, y el modulo `crypto` equivalente en otros lenguajes. Nunca uses `random()`, `Math.random()`, o funciones analogas.

En el proximo capitulo veremos como usar llaves para autenticar mensajes --una propiedad diferente e independiente del cifrado-- con MACs, HMAC y Poly1305.

---

## Referencias del capitulo

- [Shannon, 1948] Shannon, C.E. "A Mathematical Theory of Communication." Bell System Technical Journal, 1948.
- [NIST, 2015] NIST SP 800-90A Rev. 1. "Recommendation for Random Number Generation Using Deterministic Random Bit Generators." Junio 2015.
- [Bellare, Canetti, Krawczyk, 1996] Bellare, M., Canetti, R., Krawczyk, H. "Keying Hash Functions for Message Authentication." CRYPTO 1996.
- [Schneier, 2007] Schneier, B. "The Strange Story of Dual_EC_DRBG." Schneier on Security, Noviembre 2007.
- [Reuters, 2013] Menn, J. "Exclusive: Secret contract tied NSA and security industry pioneer." Reuters, Diciembre 2013.
- [Debian Security Advisory DSA-1571, 2008] "openssl -- predictable random number generator." Mayo 2008.
- [fail0verflow, 2010] "Console Hacking 2010: PS3 Epic Fail." 27th Chaos Communication Congress.
- [Bitcoin.org Security Advisory, 2013] "Android Security Vulnerability." Agosto 2013.
- [Bernstein, 2014] Bernstein, D.J. "Entropy Attacks!" cr.yp.to.
- [Shumow, Ferguson, 2007] "On the Possibility of a Back Door in the NIST SP800-90 Dual Ec Prng." CRYPTO 2007 Rump Session.
- [Myths about /dev/urandom, 2014] Huhn, T. "Myths about /dev/urandom." 2uo.de.
