# Capitulo 5: Hashes para passwords: por que SHA-256 es la peor opcion

> "La rapidez de un hash seguro es la peor enemiga de tus passwords."

---

En los capitulos anteriores aprendimos a valorar la velocidad de las funciones hash. SHA-256 procesa gigabytes por segundo. BLAKE3 es todavia mas rapido. SHA-3 fue disenado para ser eficiente en hardware y software. La velocidad es una virtud cuando necesitas verificar la integridad de un archivo o calcular el hash de un bloque en una blockchain.

Pero hay un contexto donde la velocidad se convierte en tu peor enemiga: el almacenamiento de contrasenas.

En 2012, LinkedIn perdio 6.5 millones de hashes de contrasenas. Estaban hasheados con SHA-1, sin salt. Un atacante con una GPU de gama media pudo revertir el 90% de ellos en menos de 72 horas. Cuando en 2016 se revelo que la filtracion real abarcaba **117 millones de cuentas**, el resultado fue el mismo: la inmensa mayoria fueron descifradas en horas, no en dias [Krebs, 2016; TechCrunch, 2016].

El problema no era SHA-1. El problema era que SHA-1 es **demasiado rapido**.

Este capitulo explica por que los hashes de proposito general son peligrosos para contrasenas, que alternativas existen, y como implementar correctamente el almacenamiento de contrasenas usando Argon2id --el estado del arte en 2026.

---

## 5.1 Por que los hashes normales no sirven para contrasenas

### 5.1.1 El modelo de amenaza

Para entender por que SHA-256 es una mala eleccion para contrasenas, necesitamos pensar como un atacante.

El escenario es este: un atacante obtiene acceso a tu base de datos. Tiene una tabla con nombres de usuario y hashes de contrasenas. Su objetivo es revertir esos hashes --encontrar las contrasenas originales que producen cada hash.

Sabemos que un hash criptografico es irreversible: no existe una funcion que reciba un hash y devuelva la entrada original. Pero un atacante no necesita revertir el hash. Necesita **adivinarlo**.

La estrategia es simple: el atacante toma una contrasena candidata, calcula su hash, y compara el resultado con los hashes de la base de datos. Si coincide, encontro la contrasena. Repite esto millones, miles de millones de veces.

Esto funciona porque las contrasenas humanas tienen muy poca entropia. No son cadenas aleatorias de 256 bits. Son palabras del diccionario, nombres de mascotas, fechas de nacimiento, y variaciones predecibles como "P@ssw0rd1!". La lista RockYou --filtrada en 2009 cuando la empresa almacenaba contrasenas en **texto plano**-- contiene 14 millones de contrasenas reales, y la contrasena mas comun era "123456", usada por 290,731 personas [RockYou, Wikipedia].

El factor critico es la **velocidad de hasheo**. Cuantos hashes por segundo puede calcular el atacante? Aqui es donde SHA-256 se vuelve tu enemigo.

### 5.1.2 La velocidad mata: benchmarks reales

Veamos que tan rapido puede un atacante probar contrasenas con hardware moderno. La herramienta **hashcat** es el estandar de la industria para crackeo de contrasenas, y sus benchmarks en una NVIDIA RTX 4090 son reveladores:

```
Algoritmo                   Hashes por segundo (RTX 4090)
------------------------------------------------------------
MD5                         ~164,000,000,000  (164 mil millones)
SHA-1                       ~52,000,000,000   (52 mil millones)
SHA-256                     ~22,000,000,000   (22 mil millones)
SHA-512                     ~3,500,000,000    (3.5 mil millones)
bcrypt (cost=12)            ~33,000           (33 mil)
scrypt (N=2^14, r=8, p=1)  ~2,800            (2,800)
Argon2id (19 MiB, t=2)     ~1,000            (1,000)
```

Fuente: Hashcat v6.2.6, benchmarks en RTX 4090 [Chick3nman, 2023; OnlineHashCrack, 2025].

Lee esos numeros de nuevo. Con SHA-256, un atacante puede probar **22 mil millones de contrasenas por segundo** en una sola GPU de consumo. Un diccionario de 14 millones de contrasenas (como RockYou) se recorre en menos de un milisegundo. Incluso un ataque de fuerza bruta sobre contrasenas de 8 caracteres alfanumericos (62^8 = ~218 billones de combinaciones) tomaria menos de 3 horas.

Con Argon2id, el mismo atacante puede probar **mil contrasenas por segundo**. El mismo ataque de fuerza bruta tomaria **casi 7 millones de anos**.

Esa diferencia de **22 millones a uno** es la razon por la que necesitamos hashes especializados para contrasenas.

### 5.1.3 Ataques de fuerza bruta y diccionario

Un atacante sofisticado no prueba contrasenas al azar. Usa estrategias que explotan la predecibilidad humana:

**Ataques de diccionario**: el atacante prueba una lista de contrasenas comunes. Las listas modernas incluyen millones de contrasenas filtradas de brechas reales. La lista `rockyou.txt` es el ejemplo clasico, pero hay compilaciones mucho mas grandes disponibles publicamente.

**Reglas de mutacion**: herramientas como hashcat aplican transformaciones a las palabras del diccionario: "password" se convierte en "Password", "p@ssword", "password1", "P@ssw0rd!", "PASSWORD123", y cientos de variaciones mas. Esto cubre la mayoria de las estrategias que los usuarios creen "creativas".

**Ataques hibridos**: combinan palabras del diccionario con fuerza bruta parcial. Por ejemplo, una palabra del diccionario seguida de 1-4 digitos cubre patrones como "dragon2024" o "carlos1985".

```python
"""
fuerza_bruta_demo.py

Demostracion de por que SHA-256 es peligroso para contrasenas.
Compara el tiempo de ataque con SHA-256 vs Argon2id.
"""

import hashlib
import time

# Simular ataque de diccionario con SHA-256
contrasenas_comunes = [
    "123456", "password", "12345678", "qwerty", "abc123",
    "monkey", "1234567", "letmein", "trustno1", "dragon",
    "baseball", "master", "michael", "shadow", "ashley",
    "football", "jesus", "mustang", "password1", "batman"
]

# La contrasena "objetivo" que el atacante busca
contrasena_objetivo = "batman"
hash_objetivo = hashlib.sha256(contrasena_objetivo.encode()).hexdigest()

# Ataque de diccionario contra SHA-256
inicio = time.time()
intentos = 0
for contrasena in contrasenas_comunes:
    intentos += 1
    h = hashlib.sha256(contrasena.encode()).hexdigest()
    if h == hash_objetivo:
        tiempo_sha256 = time.time() - inicio
        print(f"SHA-256: contrasena encontrada en {intentos} intentos")
        print(f"  Tiempo: {tiempo_sha256*1000:.3f} ms")
        break

# Ahora con Argon2id
try:
    from argon2 import PasswordHasher

    ph = PasswordHasher(
        time_cost=2,
        memory_cost=19456,  # 19 MiB (minimo OWASP)
        parallelism=1,
        hash_len=32,
        salt_len=16
    )
    hash_argon2 = ph.hash(contrasena_objetivo)

    inicio = time.time()
    intentos = 0
    for contrasena in contrasenas_comunes:
        intentos += 1
        try:
            ph.verify(hash_argon2, contrasena)
            tiempo_argon2 = time.time() - inicio
            print(f"\nArgon2id: contrasena encontrada en {intentos} intentos")
            print(f"  Tiempo: {tiempo_argon2*1000:.1f} ms")
            break
        except Exception:
            continue

    print(f"\nFactor de proteccion: Argon2id es "
          f"~{tiempo_argon2/tiempo_sha256:.0f}x mas lento")
    print("Esto se multiplica por miles de millones en un ataque real.")

except ImportError:
    print("\n(Instala argon2-cffi: pip install argon2-cffi)")
```

### 5.1.4 Rainbow tables: el ataque del tiempo precalculado

Las rainbow tables representan un enfoque diferente: en lugar de calcular hashes en tiempo real, el atacante precalcula una tabla gigante de pares (contrasena, hash) y luego simplemente busca cada hash robado en la tabla.

Imagina una tabla con dos columnas:

```
Contrasena          SHA-256
----------          -------
123456              8d969eef6ecad3c29a3a629280e686cf...
password            5e884898da28047151d0e56f8dc62927...
qwerty              65e84be33532fb784c48129675f9eff3...
dragon              8621faf6e8097c831a32d0093f27c280...
...                 ...
(millones de filas)
```

Una rainbow table completa para SHA-256 con contrasenas de hasta 8 caracteres alfanumericos ocuparia varios terabytes, pero se puede construir una sola vez y reutilizar infinitamente. Es un intercambio de tiempo de computo por espacio de almacenamiento.

Las rainbow tables reales son mas sofisticadas que una simple tabla de busqueda: usan cadenas de reduccion para comprimir el espacio, pero el principio es el mismo. Existen rainbow tables publicas para MD5, SHA-1 y SHA-256 sin salt que cubren millones de contrasenas.

La defensa contra rainbow tables es el **salt**, que veremos en la siguiente seccion.

---

## 5.2 Salt: la primera defensa

### 5.2.1 Que es un salt y como funciona

Un **salt** es un valor aleatorio unico que se genera para cada usuario y se agrega a la contrasena antes de hashearla:

```python
import os
import hashlib

contrasena = "mi_contrasena_secreta"

# Sin salt: el hash es siempre el mismo
hash_sin_salt = hashlib.sha256(contrasena.encode()).hexdigest()
print(f"Sin salt: {hash_sin_salt}")
print(f"Sin salt: {hashlib.sha256(contrasena.encode()).hexdigest()}")
print("(identicos -- vulnerable a rainbow tables)")
print()

# Con salt: el hash es diferente cada vez
salt1 = os.urandom(16)  # 16 bytes = 128 bits
salt2 = os.urandom(16)

hash_con_salt1 = hashlib.sha256(salt1 + contrasena.encode()).hexdigest()
hash_con_salt2 = hashlib.sha256(salt2 + contrasena.encode()).hexdigest()

print(f"Salt 1: {salt1.hex()}")
print(f"Hash 1: {hash_con_salt1}")
print(f"Salt 2: {salt2.hex()}")
print(f"Hash 2: {hash_con_salt2}")
print("(completamente diferentes -- rainbow tables inutiles)")
```

El salt cumple una funcion precisa: **invalida las rainbow tables**. Si cada usuario tiene un salt diferente, el atacante necesitaria construir una rainbow table completa **por cada usuario**. Con un salt de 16 bytes (128 bits), hay 2^128 posibles salts, haciendo que las tablas precalculadas sean completamente inutiles.

Un detalle importante: **el salt no es secreto**. Se almacena junto al hash en la base de datos, tipicamente concatenado o en un campo separado. El salt no necesita ser secreto porque su proposito no es agregar entropia a la contrasena --es hacer que cada hash sea unico incluso si dos usuarios tienen la misma contrasena.

### 5.2.2 Errores comunes con el salt

El concepto de salt es simple, pero se implementa mal con una frecuencia alarmante:

**Error 1: salt global (el mismo para todos los usuarios)**

```python
# MAL: un solo salt para toda la aplicacion
SALT_GLOBAL = b"mi_salt_secreto_2024"

def hashear_password_mal(password: str) -> str:
    return hashlib.sha256(SALT_GLOBAL + password.encode()).hexdigest()

# Dos usuarios con la misma contrasena producen el mismo hash
h1 = hashear_password_mal("dragon")
h2 = hashear_password_mal("dragon")
print(f"Usuario 1: {h1}")
print(f"Usuario 2: {h2}")
print(f"Son iguales: {h1 == h2}")  # True -- MAL
# El atacante solo necesita una rainbow table con este salt
```

**Error 2: salt corto o predecible**

```python
# MAL: salt de 4 bytes (solo 2^32 = ~4 mil millones de posibilidades)
salt_corto = os.urandom(4)

# MAL: salt basado en datos predecibles
salt_predecible = hashlib.md5(username.encode()).digest()[:8]
# El atacante puede calcular el salt de cada usuario
```

**Error 3: confundir salt con pepper**

Un **pepper** es un valor secreto que se agrega a la contrasena, pero a diferencia del salt, **no se almacena en la base de datos**. Se guarda en una variable de entorno, un archivo de configuracion protegido, o un HSM (Hardware Security Module). El pepper agrega una capa de defensa: incluso si el atacante roba la base de datos completa, no tiene el pepper y no puede verificar contrasenas.

```python
import os

# Salt: unico por usuario, almacenado en la base de datos
salt = os.urandom(16)

# Pepper: secreto global, almacenado FUERA de la base de datos
PEPPER = os.environ.get("APP_PEPPER", "").encode()

# Uso correcto: pepper + salt + contrasena
# (En la practica, usa Argon2id que maneja el salt automaticamente)
hash_final = hashlib.sha256(PEPPER + salt + contrasena.encode()).hexdigest()
```

El salt y el pepper son complementarios, no sustitutos. El salt protege contra rainbow tables; el pepper protege contra el robo completo de la base de datos.

**Buena practica**: usa siempre un salt de al menos 16 bytes (128 bits), generado con `os.urandom()` o `secrets.token_bytes()`, unico para cada usuario. Mejor aun: usa una libreria como `argon2-cffi` que genera el salt automaticamente.

---

## 5.3 Los cuatro jinetes del hashing de contrasenas

El salt resuelve el problema de las rainbow tables, pero no resuelve el problema fundamental: la velocidad. SHA-256 con salt sigue siendo SHA-256 --22 mil millones de hashes por segundo en una GPU moderna. El atacante simplemente agrega el salt a cada intento.

Necesitamos funciones disenadas para ser **deliberadamente lentas**. Funciones que obliguen al atacante a gastar cantidades significativas de tiempo, memoria, o ambas, por cada intento. Estas funciones se llaman **funciones de hashing de contrasenas** (password hashing functions) o, mas formalmente, **funciones de derivacion de llaves basadas en contrasenas** (password-based key derivation functions).

Veamos las cuatro mas importantes, en orden cronologico.

### 5.3.1 PBKDF2: el veterano jubilandose

**PBKDF2** (Password-Based Key Derivation Function 2) fue publicada en el RFC 2898 en el ano 2000 [Kaliski, 2000]. Su estrategia es la mas simple posible: aplica un hash (tipicamente HMAC-SHA-256) de forma iterativa, miles o cientos de miles de veces.

```python
import hashlib
import os
import time

password = b"mi_contrasena_segura"
salt = os.urandom(16)

# PBKDF2 con 600,000 iteraciones (recomendacion OWASP para SHA-256)
inicio = time.time()
dk = hashlib.pbkdf2_hmac(
    'sha256',       # Algoritmo base
    password,       # Contrasena
    salt,           # Salt
    600_000,        # Iteraciones
    dklen=32        # Tamano de salida en bytes
)
duracion = time.time() - inicio

print(f"PBKDF2-SHA256 (600,000 iteraciones)")
print(f"  Salt: {salt.hex()}")
print(f"  Hash: {dk.hex()}")
print(f"  Tiempo: {duracion*1000:.1f} ms")
```

La logica interna es directa:

```
U1 = HMAC-SHA256(password, salt || 0x00000001)
U2 = HMAC-SHA256(password, U1)
U3 = HMAC-SHA256(password, U2)
...
Un = HMAC-SHA256(password, U(n-1))
DK = U1 XOR U2 XOR U3 XOR ... XOR Un
```

Cada iteracion depende del resultado de la anterior, lo que impide paralelizar el calculo. El parametro configurable es el numero de iteraciones: mas iteraciones, mas lento, mas seguro.

**La debilidad critica de PBKDF2** es que solo es intensiva en CPU. No usa memoria significativa. Esto significa que un atacante con hardware especializado (GPUs, FPGAs, ASICs) puede ejecutar miles de instancias de PBKDF2 en paralelo, cada una usando una cantidad minima de memoria. El costo por intento baja drasticamente con hardware dedicado.

Django usaba PBKDF2 como algoritmo por defecto durante anos. OWASP todavia lo acepta como alternativa con un minimo de 600,000 iteraciones para HMAC-SHA-256, pero ya no lo recomienda como primera opcion [OWASP, 2025].

**Veredicto**: funcional pero obsoleto. Usalo solo si no puedes usar bcrypt, scrypt o Argon2.

### 5.3.2 bcrypt: solido pero con limitaciones

**bcrypt** fue presentado por Niels Provos y David Mazieres en 1999, basado en el cifrado de bloques Blowfish [Provos y Mazieres, 1999]. Su innovacion fue el concepto de **cost factor** (factor de costo): un parametro que duplica el tiempo de hasheo con cada incremento.

```python
import bcrypt
import time

password = b"mi_contrasena_segura"

# bcrypt con cost factor 12
# Cada incremento de 1 duplica el tiempo
inicio = time.time()
hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))
duracion = time.time() - inicio

print(f"bcrypt (cost=12)")
print(f"  Hash: {hashed.decode()}")
print(f"  Tiempo: {duracion*1000:.1f} ms")
print()

# Verificacion
inicio = time.time()
valido = bcrypt.checkpw(password, hashed)
duracion = time.time() - inicio
print(f"  Verificacion: {'OK' if valido else 'FALLO'}")
print(f"  Tiempo verificacion: {duracion*1000:.1f} ms")
```

El formato de salida de bcrypt es autodescriptivo:

```
$2b$12$LJ3m4ys3Tl0bHPBl6LsuHeUMGUdJpXQoEXo9hFqKR/ekxwn6W8G5a
 |  |  |                                                   |
 |  |  +-- Salt (22 chars base64 = 16 bytes)               |
 |  +-- Cost factor (2^12 = 4096 iteraciones internas)      |
 +-- Version ($2b$ = la version actual)                     |
                                                  Hash (31 chars)
```

bcrypt incluye el salt automaticamente en la salida, lo que simplifica el almacenamiento: un solo campo en la base de datos contiene la version, el cost factor, el salt y el hash.

**Las limitaciones de bcrypt:**

1. **Limite de 72 bytes**: bcrypt trunca la entrada a 72 bytes. Si una contrasena es mas larga, los bytes extra se ignoran silenciosamente. Esto significa que "contrasena_muy_larga_de_exactamente_setenta_y_dos_bytes_xxxxxx" y "contrasena_muy_larga_de_exactamente_setenta_y_dos_bytes_xxxxxxABC123" producen el **mismo hash**. En la practica esto rara vez es un problema (pocas contrasenas superan los 72 bytes), pero es una limitacion que Argon2 no tiene.

2. **Memoria fija**: bcrypt usa solo 4 KB de RAM, independientemente del cost factor. Esto lo hace vulnerable a ataques con FPGAs y ASICs que pueden ejecutar miles de instancias en paralelo con poca memoria. Un estudio de 2014 demostro que un ataque con FPGAs podia alcanzar rendimientos significativos contra bcrypt [Malvoni, Knezovic y Stipcevic, 2014].

3. **Solo intensivo en CPU**: como PBKDF2, bcrypt no tiene parametro de memoria. La defensa contra hardware especializado es limitada.

**Veredicto**: sigue siendo una opcion aceptable con cost factor >= 12. Pero Argon2id es superior en todos los aspectos. OWASP lo lista como alternativa aceptable, no como primera recomendacion [OWASP, 2025].

### 5.3.3 scrypt: anadiendo memoria a la ecuacion

**scrypt** fue disenado por Colin Percival en 2009 con un objetivo explicito: ser resistente a ataques con hardware especializado [Percival, 2009]. Su innovacion fue hacer el algoritmo no solo intensivo en CPU, sino tambien **intensivo en memoria**.

La idea es elegante: si el algoritmo requiere una cantidad significativa de RAM para ejecutarse, entonces el atacante necesita esa misma cantidad de RAM **por cada instancia paralela**. Las GPUs tienen muchos nucleos pero memoria compartida limitada. Los FPGAs y ASICs son caros en RAM. Si bcrypt necesita 4 KB por instancia, scrypt puede necesitar 16 MB o mas.

```python
import hashlib
import os
import time

password = b"mi_contrasena_segura"
salt = os.urandom(16)

# scrypt con parametros recomendados por OWASP
# N = 2^17 (CPU/memoria), r = 8 (tamano de bloque), p = 1 (paralelismo)
inicio = time.time()
dk = hashlib.scrypt(
    password,
    salt=salt,
    n=2**17,    # Factor de CPU/memoria (debe ser potencia de 2)
    r=8,        # Tamano de bloque (1024 bytes por bloque)
    p=1,        # Factor de paralelismo
    dklen=32    # Tamano de salida
)
duracion = time.time() - inicio

# Memoria usada: 128 * N * r bytes = 128 * 131072 * 8 = 128 MB
memoria_mb = 128 * 2**17 * 8 / (1024 * 1024)

print(f"scrypt (N=2^17, r=8, p=1)")
print(f"  Salt: {salt.hex()}")
print(f"  Hash: {dk.hex()}")
print(f"  Tiempo: {duracion*1000:.1f} ms")
print(f"  Memoria estimada: {memoria_mb:.0f} MB")
```

scrypt tiene tres parametros:

- **N** (CPU/memoria): el factor principal. Debe ser una potencia de 2. Duplicar N duplica tanto el tiempo como la memoria.
- **r** (tamano de bloque): controla el tamano de los bloques de memoria. Valores mayores usan mas memoria pero poco mas de CPU. El valor estandar es 8.
- **p** (paralelismo): permite usar multiples nucleos en la verificacion legitima. Cada hilo necesita su propia copia de memoria.

scrypt fue adoptado como proof-of-work en Litecoin y otras criptomonedas, lo que valido su resistencia a hardware especializado (durante anos, no fue rentable fabricar ASICs para scrypt).

**La limitacion de scrypt**: la relacion entre tiempo y memoria es rigida. No puedes aumentar la memoria sin aumentar tambien el tiempo de forma proporcional. Argon2 permite ajustar tiempo y memoria de forma independiente.

**Veredicto**: una opcion solida y madura. OWASP la recomienda como segunda opcion despues de Argon2id, con parametros minimos de N=2^17, r=8, p=1 [OWASP, 2025].

### 5.3.4 Argon2: el ganador de la Password Hashing Competition

En 2013, un grupo de criptografos liderado por Jean-Philippe Aumasson organizo la **Password Hashing Competition** (PHC), una competencia abierta y publica para disenar la funcion de hashing de contrasenas definitiva. La motivacion era clara: bcrypt tenia 14 anos y sus limitaciones de memoria eran cada vez mas evidentes; scrypt era prometedora pero tenia deficiencias teoricas conocidas; y PBKDF2 era simplemente insuficiente.

La competencia recibio 24 candidatos de equipos de todo el mundo. Despues de dos anos de analisis criptografico intenso, el 20 de julio de 2015, el panel anuncio al ganador: **Argon2**, disenado por Alex Biryukov, Daniel Dinu y Dmitry Khovratovich de la Universidad de Luxemburgo [Biryukov, Dinu y Khovratovich, 2015]. Cuatro algoritmos recibieron mencion especial: Catena, Lyra2, yescrypt y Makwa.

Argon2 fue seleccionado por varias razones:

1. **Resistencia demostrable contra trade-offs tiempo-memoria**: un atacante que usa menos memoria necesita exponencialmente mas tiempo.
2. **Parametros independientes**: tiempo y memoria se configuran por separado.
3. **Resistencia a ataques side-channel** (en su variante Argon2i/Argon2id).
4. **Diseno simple y analizable**: usa internamente BLAKE2b y operaciones sobre bloques de 1024 bytes.

#### Argon2d vs Argon2i vs Argon2id: cuando usar cada uno

Argon2 tiene tres variantes que difieren en como acceden a la memoria:

**Argon2d** (data-dependent): los patrones de acceso a memoria dependen de los datos de entrada (la contrasena). Esto lo hace mas resistente a ataques de fuerza bruta con GPUs y ASICs, porque el patron de acceso no se puede predecir sin conocer la contrasena. Sin embargo, es vulnerable a **ataques de canal lateral** (side-channel attacks) donde un atacante puede observar los patrones de acceso a cache del procesador.

**Argon2i** (data-independent): los patrones de acceso a memoria son independientes de la entrada. Es inmune a ataques de canal lateral, pero menos resistente a ataques de fuerza bruta que Argon2d porque el patron de acceso es predecible.

**Argon2id** (hibrido): combina ambos enfoques. La primera mitad de las pasadas sobre la memoria usa el modo Argon2i (resistente a side-channel), y la segunda mitad usa Argon2d (resistente a fuerza bruta). Es lo mejor de ambos mundos.

```
+-------------------+------------------+-------------------+
| Variante          | Resistencia a    | Resistencia a     |
|                   | side-channel     | fuerza bruta GPU  |
+-------------------+------------------+-------------------+
| Argon2d           | Baja             | Alta              |
| Argon2i           | Alta             | Media             |
| Argon2id          | Media-Alta       | Alta              |
+-------------------+------------------+-------------------+

Recomendacion: Argon2id para la inmensa mayoria de casos.
```

**La recomendacion es unanime**: usa **Argon2id** para hasheo de contrasenas. Es la recomendacion de OWASP, del RFC 9106, y de la comunidad criptografica en general [OWASP, 2025; RFC 9106, 2022].

---

## 5.4 Argon2 en la practica: parametros, calibracion y codigo

### 5.4.1 Los parametros de Argon2

Argon2 tiene cuatro parametros principales que controlan su costo computacional:

1. **memory_cost (m)**: la cantidad de memoria en kibibytes (KiB) que usa el algoritmo. Mas memoria = mas dificil de atacar con hardware paralelo.

2. **time_cost (t)**: el numero de iteraciones (pasadas sobre la memoria). Mas iteraciones = mas tiempo de CPU.

3. **parallelism (p)**: el numero de hilos que pueden trabajar en paralelo. Permite aprovechar multiples nucleos en la verificacion legitima.

4. **hash_len**: el tamano del hash resultante en bytes. 32 bytes (256 bits) es el estandar.

5. **salt_len**: el tamano del salt. 16 bytes (128 bits) es el minimo recomendado.

### 5.4.2 Parametros recomendados por OWASP

OWASP proporciona dos configuraciones equivalentes en seguridad [OWASP Password Storage Cheat Sheet, 2025]:

```
Opcion 1 (mas memoria, menos tiempo):
  m = 47104 (46 MiB), t = 1, p = 1

Opcion 2 (menos memoria, mas tiempo):
  m = 19456 (19 MiB), t = 2, p = 1
```

Estas son configuraciones **minimas**. Si tu servidor tiene recursos disponibles, puedes y debes usar parametros mas altos. La regla general es: usa la mayor cantidad de memoria y tiempo que tu servidor pueda permitirse sin degradar la experiencia del usuario.

### 5.4.3 Implementacion completa con argon2-cffi

La libreria `argon2-cffi` es la implementacion de referencia de Argon2 para Python. Veamos una implementacion completa de registro y login:

```python
"""
auth_argon2.py

Sistema completo de registro y login con Argon2id.
Incluye calibracion de parametros y re-hash automatico.

Requisitos: pip install argon2-cffi
"""

from argon2 import PasswordHasher, Type
from argon2.exceptions import (
    VerifyMismatchError,
    VerificationError,
    InvalidHashError
)
import time


def crear_hasher(memory_cost: int = 47104,
                 time_cost: int = 1,
                 parallelism: int = 1) -> PasswordHasher:
    """
    Crea un PasswordHasher con los parametros especificados.

    Parametros por defecto: OWASP Opcion 1 (46 MiB, 1 iteracion).
    """
    return PasswordHasher(
        time_cost=time_cost,
        memory_cost=memory_cost,   # KiB
        parallelism=parallelism,
        hash_len=32,               # 256 bits
        salt_len=16,               # 128 bits
        type=Type.ID               # Argon2id
    )


# --- REGISTRO ---

def registrar_usuario(password: str,
                      ph: PasswordHasher = None) -> str:
    """
    Hashea una contrasena para almacenarla en la base de datos.

    Retorna un string que contiene todos los parametros,
    el salt y el hash en formato estandar PHC.
    """
    if ph is None:
        ph = crear_hasher()

    # argon2-cffi genera un salt aleatorio automaticamente
    hash_completo = ph.hash(password)
    return hash_completo


# --- LOGIN ---

def verificar_login(hash_almacenado: str,
                    password_ingresado: str,
                    ph: PasswordHasher = None) -> dict:
    """
    Verifica una contrasena contra el hash almacenado.

    Retorna un diccionario con:
      - valido: True/False
      - necesita_rehash: True si los parametros son obsoletos
      - mensaje: descripcion del resultado
    """
    if ph is None:
        ph = crear_hasher()

    resultado = {
        "valido": False,
        "necesita_rehash": False,
        "mensaje": ""
    }

    try:
        # verify() lanza una excepcion si la contrasena no coincide
        ph.verify(hash_almacenado, password_ingresado)
        resultado["valido"] = True
        resultado["mensaje"] = "Autenticacion exitosa"

        # Verificar si los parametros del hash son obsoletos
        if ph.check_needs_rehash(hash_almacenado):
            resultado["necesita_rehash"] = True
            resultado["mensaje"] += " (se requiere re-hash)"

    except VerifyMismatchError:
        resultado["mensaje"] = "Contrasena incorrecta"

    except VerificationError as e:
        resultado["mensaje"] = f"Error de verificacion: {e}"

    except InvalidHashError as e:
        resultado["mensaje"] = f"Hash invalido: {e}"

    return resultado


# --- RE-HASH ---

def rehash_si_necesario(hash_almacenado: str,
                        password: str,
                        ph: PasswordHasher = None) -> str:
    """
    Si los parametros del hash son obsoletos, genera un nuevo hash.
    Retorna el hash original si no necesita actualizacion.

    Esto permite migrar gradualmente a parametros mas fuertes
    sin forzar a todos los usuarios a cambiar su contrasena.
    """
    if ph is None:
        ph = crear_hasher()

    if ph.check_needs_rehash(hash_almacenado):
        return ph.hash(password)
    return hash_almacenado


# --- DEMOSTRACION ---

if __name__ == "__main__":
    ph = crear_hasher()

    print("Sistema de autenticacion con Argon2id")
    print("=" * 55)

    # 1. Registro
    password = "Mi_Contrasena_Segura_2026!"
    hash_almacenado = registrar_usuario(password, ph)
    print(f"\n1. Registro:")
    print(f"   Hash: {hash_almacenado}")
    print(f"   (contiene: version, tipo, parametros, salt y hash)")

    # 2. Login correcto
    resultado = verificar_login(hash_almacenado, password, ph)
    print(f"\n2. Login correcto:")
    print(f"   Valido: {resultado['valido']}")
    print(f"   Mensaje: {resultado['mensaje']}")

    # 3. Login incorrecto
    resultado = verificar_login(hash_almacenado, "contrasena_incorrecta", ph)
    print(f"\n3. Login incorrecto:")
    print(f"   Valido: {resultado['valido']}")
    print(f"   Mensaje: {resultado['mensaje']}")

    # 4. Deteccion de parametros obsoletos
    # Simulamos un hash creado con parametros viejos (menos memoria)
    ph_viejo = crear_hasher(memory_cost=8192, time_cost=1)
    hash_viejo = ph_viejo.hash(password)

    resultado = verificar_login(hash_viejo, password, ph)
    print(f"\n4. Hash con parametros obsoletos:")
    print(f"   Hash viejo: {hash_viejo[:60]}...")
    print(f"   Valido: {resultado['valido']}")
    print(f"   Necesita rehash: {resultado['necesita_rehash']}")

    # 5. Re-hash automatico
    hash_nuevo = rehash_si_necesario(hash_viejo, password, ph)
    print(f"\n5. Re-hash automatico:")
    print(f"   Hash actualizado: {hash_nuevo[:60]}...")
    print(f"   Son diferentes: {hash_viejo != hash_nuevo}")
```

El formato de salida de Argon2 sigue el estandar PHC (Password Hashing Competition):

```
$argon2id$v=19$m=47104,t=1,p=1$c2FsdF9hbGVhdG9yaW8$hash_base64_aqui
 |        |    |               |                     |
 |        |    |               +-- Salt (base64)     +-- Hash (base64)
 |        |    +-- Parametros: memoria, tiempo, paralelismo
 |        +-- Version de Argon2 (19 = 0x13)
 +-- Tipo: argon2id
```

Este formato es autodescriptivo: contiene toda la informacion necesaria para verificar el hash en el futuro, incluso si cambias los parametros. Esto es lo que permite la migracion gradual.

### 5.4.4 Calibracion de parametros: como elegir los valores correctos

Los parametros "correctos" dependen de tu hardware y de cuanto tiempo puedes permitirte por verificacion. La regla practica es:

1. Decide un tiempo maximo aceptable por verificacion (tipicamente 250-1000 ms).
2. Maximiza la memoria dentro de lo que tu servidor pueda permitirse.
3. Ajusta las iteraciones hasta alcanzar el tiempo objetivo.

```python
"""
calibracion_argon2.py

Calibra los parametros de Argon2id para tu hardware.
Ejecuta este script en el servidor donde correra tu aplicacion.

Requisitos: pip install argon2-cffi
"""

from argon2 import PasswordHasher, Type
import time


def calibrar_argon2(tiempo_objetivo_ms: float = 500.0,
                    memoria_max_kib: int = 256 * 1024,
                    paralelismo: int = 1) -> dict:
    """
    Encuentra los parametros optimos de Argon2id para tu hardware.

    Estrategia:
    1. Fija el paralelismo (tipicamente 1 para servidores web)
    2. Empieza con la memoria maxima disponible
    3. Reduce la memoria si es necesario
    4. Ajusta las iteraciones para alcanzar el tiempo objetivo

    Parametros:
        tiempo_objetivo_ms: tiempo deseado por hash en milisegundos
        memoria_max_kib: memoria maxima en KiB (256 MiB por defecto)
        paralelismo: numero de hilos
    """
    print(f"Calibrando Argon2id...")
    print(f"  Tiempo objetivo: {tiempo_objetivo_ms} ms")
    print(f"  Memoria maxima: {memoria_max_kib // 1024} MiB")
    print(f"  Paralelismo: {paralelismo}")
    print()

    password_prueba = "password_de_calibracion_12345"
    mejor_config = None

    # Probar diferentes niveles de memoria (de mayor a menor)
    memorias_kib = []
    mem = memoria_max_kib
    while mem >= 19456:  # Minimo OWASP: 19 MiB
        memorias_kib.append(mem)
        mem //= 2

    for memoria in memorias_kib:
        for iteraciones in [1, 2, 3, 4, 5, 8, 10]:
            ph = PasswordHasher(
                time_cost=iteraciones,
                memory_cost=memoria,
                parallelism=paralelismo,
                hash_len=32,
                salt_len=16,
                type=Type.ID
            )

            # Medir tiempo promedio (3 intentos)
            tiempos = []
            for _ in range(3):
                inicio = time.time()
                ph.hash(password_prueba)
                tiempos.append((time.time() - inicio) * 1000)

            tiempo_promedio = sum(tiempos) / len(tiempos)
            memoria_mib = memoria / 1024

            # Queremos el maximo uso de recursos dentro del tiempo objetivo
            if tiempo_promedio <= tiempo_objetivo_ms:
                config = {
                    "memory_cost": memoria,
                    "time_cost": iteraciones,
                    "parallelism": paralelismo,
                    "tiempo_ms": tiempo_promedio,
                    "memoria_mib": memoria_mib
                }

                # Preferir mas memoria sobre mas iteraciones
                if (mejor_config is None or
                    config["memory_cost"] > mejor_config["memory_cost"] or
                    (config["memory_cost"] == mejor_config["memory_cost"] and
                     config["time_cost"] > mejor_config["time_cost"])):
                    mejor_config = config

                print(f"  m={memoria:>7} KiB ({memoria_mib:>5.0f} MiB), "
                      f"t={iteraciones}, p={paralelismo}: "
                      f"{tiempo_promedio:>7.1f} ms {'<-- candidato' if config == mejor_config else ''}")

    print()
    if mejor_config:
        print("Parametros optimos encontrados:")
        print(f"  memory_cost = {mejor_config['memory_cost']} "
              f"({mejor_config['memoria_mib']:.0f} MiB)")
        print(f"  time_cost   = {mejor_config['time_cost']}")
        print(f"  parallelism = {mejor_config['parallelism']}")
        print(f"  Tiempo:       {mejor_config['tiempo_ms']:.1f} ms")
        print()
        print("Codigo para usar estos parametros:")
        print(f"  ph = PasswordHasher(")
        print(f"      time_cost={mejor_config['time_cost']},")
        print(f"      memory_cost={mejor_config['memory_cost']},")
        print(f"      parallelism={mejor_config['parallelism']},")
        print(f"      hash_len=32,")
        print(f"      salt_len=16,")
        print(f"      type=Type.ID")
        print(f"  )")
    else:
        print("No se encontraron parametros que cumplan el objetivo.")
        print("Reduce el tiempo objetivo o el uso de memoria.")
        print("Parametros minimos OWASP: m=19456, t=2, p=1")

    return mejor_config


if __name__ == "__main__":
    # Calibrar para 500 ms con hasta 256 MiB
    config = calibrar_argon2(
        tiempo_objetivo_ms=500.0,
        memoria_max_kib=256 * 1024,
        paralelismo=1
    )
```

La idea es simple: ejecutas este script en tu servidor de produccion, y te dice los parametros maximos que puedes usar dentro de tu presupuesto de tiempo. Recalibra periodicamente, especialmente cuando actualices hardware.

---

## 5.5 Funciones de derivacion de llaves (KDF)

### 5.5.1 De contrasena a llave de cifrado

Hasta ahora hemos hablado de hasheo de contrasenas para **almacenamiento**: convertir una contrasena en un hash que se guarda en la base de datos para verificacion futura. Pero hay otro caso de uso: convertir una contrasena en una **llave de cifrado**.

Si necesitas cifrar un archivo con una contrasena que el usuario te da, no puedes usar la contrasena directamente como llave de AES-256 (necesita exactamente 32 bytes de material pseudoaleatorio). Necesitas una **funcion de derivacion de llaves** (Key Derivation Function, KDF).

Todas las funciones que vimos --PBKDF2, bcrypt, scrypt, Argon2-- son tecnicamente KDFs, pero en la practica hay una distincion importante:

- **Password hashing** (almacenamiento): el objetivo es ser lento. La salida se almacena y se compara.
- **Key derivation** (derivacion de llaves): el objetivo es producir material criptografico de alta calidad a partir de un secreto de baja entropia.

### 5.5.2 HKDF: extraer y expandir

Para derivar multiples llaves a partir de un secreto de alta entropia (como una llave maestra negociada via Diffie-Hellman), se usa **HKDF** (HMAC-based Key Derivation Function, RFC 5869). HKDF tiene dos fases:

1. **Extract**: condensa el material de entrada en una llave pseudoaleatoria.
2. **Expand**: expande esa llave en tantos bytes como necesites.

```python
"""
kdf_demo.py

Demostracion de derivacion de llaves con HKDF y Argon2.
"""

from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

# Derivar una llave AES-256 de un secreto compartido
secreto_compartido = b"secreto_de_diffie_hellman_de_32b"

hkdf = HKDF(
    algorithm=hashes.SHA256(),
    length=32,                     # 32 bytes = AES-256
    salt=None,                     # Opcional
    info=b"cifrado_de_archivos"    # Contexto de uso
)

llave_aes = hkdf.derive(secreto_compartido)
print(f"Llave AES-256 derivada: {llave_aes.hex()}")
print()

# Derivar MULTIPLES llaves del mismo secreto
# usando diferentes valores de 'info'
for uso in [b"cifrado", b"autenticacion", b"firma"]:
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=uso
    )
    llave = hkdf.derive(secreto_compartido)
    print(f"Llave para {uso.decode():>15}: {llave.hex()[:32]}...")
```

### 5.5.3 Cuando usar que

```
Necesito...

+-- Almacenar una contrasena en la base de datos?
|   --> Argon2id (o bcrypt/scrypt como alternativa)
|
+-- Derivar una llave de cifrado desde una contrasena?
|   --> Argon2id (para la parte lenta) + HKDF (para la expansion)
|
+-- Derivar multiples llaves de una llave maestra?
|   --> HKDF directamente (no necesitas lentitud)
|
+-- Generar material aleatorio determinista?
    --> HKDF o SHAKE256
```

La regla es: si la entrada tiene baja entropia (una contrasena humana), necesitas una funcion lenta. Si la entrada tiene alta entropia (una llave criptografica), HKDF es suficiente.

---

## 5.6 Casos reales: cuando el hashing falla

### 5.6.1 LinkedIn (2012): SHA-1 sin salt

En junio de 2012, un atacante publico 6.5 millones de hashes de contrasenas de LinkedIn. Los hashes eran SHA-1 **sin salt** --lo que significaba que cualquier contrasena identica entre dos usuarios producia el mismo hash, y las rainbow tables eran directamente aplicables.

En cuestion de horas, la comunidad de seguridad habia revertido la mayoria de los hashes. El metodo era trivial: comparar los hashes filtrados contra rainbow tables existentes y diccionarios de contrasenas comunes.

Lo peor vino en mayo de 2016, cuando se revelo que la filtracion real abarcaba **117 millones de cuentas** (de un total de 167 millones en el dataset). Motherboard reporto que el 90% de las contrasenas fueron descifradas en 72 horas [Vice Motherboard, 2016]. Tan solo 50 contrasenas comunes representaban mas de 2.2 millones de cuentas.

**Lecciones:**
- SHA-1 sin salt no es almacenamiento de contrasenas; es un directorio publico.
- Las contrasenas humanas tienen entropia tan baja que incluso un hash "seguro" usado incorrectamente es trivial de romper.
- Una brecha puede tener consecuencias anos despues cuando la escala real se descubre.

### 5.6.2 RockYou (2009): texto plano

En diciembre de 2009, un atacante exploto una vulnerabilidad de inyeccion SQL en RockYou, una empresa que proporcionaba widgets para MySpace y Facebook. La base de datos contenia **32 millones de contrasenas almacenadas en texto plano** --sin hash, sin cifrado, sin nada [Wikipedia, RockYou].

El atacante no necesito ningun tipo de ataque criptografico. Simplemente leyo las contrasenas directamente de la base de datos.

La filtracion tuvo un impacto duradero: la lista de contrasenas de RockYou se convirtio en el archivo `rockyou.txt`, que hasta hoy es la herramienta estandar para ataques de diccionario. Viene preinstalada en distribuciones de pentesting como Kali Linux y Parrot OS. Cuando alguien dice "voy a probar con un diccionario", probablemente esta usando rockyou.txt.

**Lecciones:**
- Almacenar contrasenas en texto plano es negligencia, no un "error tecnico".
- Las consecuencias de una filtracion se extienden decadas en el futuro.
- rockyou.txt es un recordatorio permanente de que millones de personas usan "123456" como contrasena.

### 5.6.3 Adobe (2013): 3DES en modo ECB

En octubre de 2013, Adobe revelo una filtracion de **153 millones de cuentas**. Pero el error de Adobe no fue usar un hash rapido --fue algo peor: usaron **cifrado simetrico** (3DES) en lugar de hasheo [Schneier, 2013; Sophos, 2013].

Y no solo eso: usaron modo ECB (Electronic Codebook), el modo mas basico y peligroso que vimos conceptualmente en el Capitulo 1. En modo ECB, el mismo texto plano siempre produce el mismo texto cifrado. Si dos usuarios tenian la contrasena "123456", su campo cifrado era **byte a byte identico**.

Para empeorar la situacion, Adobe almacenaba las **pistas de contrasena en texto plano** junto al cifrado. Si un usuario tenia como pista "el nombre de mi perro" y su cifrado era identico al de otro usuario con pista "personaje de Dragon Ball + numero", un atacante podia deducir la contrasena sin siquiera tocar el cifrado.

La comunidad de seguridad tardo aproximadamente tres horas en determinar las 100 contrasenas mas comunes del dataset, simplemente agrupando los textos cifrados identicos y leyendo las pistas asociadas [Graham Cluley, 2013].

**Lecciones:**
- Las contrasenas se **hashean**, no se cifran. El cifrado es reversible; el hash no. Si cifras contrasenas, un atacante que obtenga la llave puede revertir **todas** las contrasenas de golpe.
- Modo ECB revela patrones que destruyen cualquier seguridad.
- Las pistas de contrasena son un vector de ataque que la mayoria de los desarrolladores ignoran.

### 5.6.4 Dropbox (2012, revelado 2016): bcrypt bien hecho

No todas las historias son malas. En 2012, Dropbox tambien fue victima de una filtracion. Pero a diferencia de LinkedIn, Dropbox usaba **bcrypt con salt** para sus contrasenas. Cuando los hashes se hicieron publicos en 2016, la comunidad de seguridad confirmo que descifrarlos era extremadamente costoso y lento.

La filtracion afecto 68 millones de cuentas, pero el impacto real fue minimo: bcrypt con un cost factor adecuado hizo que los ataques de fuerza bruta fueran impracticables para la inmensa mayoria de las contrasenas.

**Leccion**: usar el algoritmo correcto mitiga dramaticamente el dano de una filtracion. La base de datos siempre puede ser robada; la pregunta es cuanto le costara al atacante extraer informacion util.

---

## 5.7 Tabla resumen: comparacion de algoritmos

```
+----------+--------+--------+-----------+-------------+------------------+
| Algoritmo| Ano    | Memory | Parametros| Limite      | Recomendacion    |
|          |        | hard?  |           | entrada     | OWASP 2025       |
+----------+--------+--------+-----------+-------------+------------------+
| PBKDF2   | 2000   | No     | iters,    | Sin limite  | Tercera opcion   |
|          |        |        | algo      |             | (>= 600k iters)  |
+----------+--------+--------+-----------+-------------+------------------+
| bcrypt   | 1999   | No     | cost      | 72 bytes    | Segunda opcion   |
|          |        | (4 KB) |           |             | (cost >= 10)     |
+----------+--------+--------+-----------+-------------+------------------+
| scrypt   | 2009   | Si     | N, r, p   | Sin limite  | Segunda opcion   |
|          |        |        |           |             | (N>=2^17,r=8,p=1)|
+----------+--------+--------+-----------+-------------+------------------+
| Argon2id | 2015   | Si     | m, t, p,  | Sin limite  | PRIMERA OPCION   |
|          |        |        | hash_len  |             | (m>=19MiB, t>=2) |
+----------+--------+--------+-----------+-------------+------------------+
```

---

## 5.8 Ejercicio integrador: sistema de login seguro

```python
#!/usr/bin/env python3
"""
ejercicio_capitulo_05.py

Ejercicio: Implementa un sistema completo de registro y login
con las siguientes caracteristicas:

1. Registro con Argon2id
2. Login con verificacion
3. Re-hash automatico cuando los parametros cambian
4. Calibracion de parametros para tu hardware
5. Pepper desde variable de entorno (opcional)

Requisitos: pip install argon2-cffi

Instrucciones:
- Completa las funciones marcadas con TODO
- Ejecuta el script para verificar que todo funciona
- Experimenta con diferentes parametros y observa los tiempos
"""

import os
import time
import json
from argon2 import PasswordHasher, Type
from argon2.exceptions import VerifyMismatchError

# Simulacion de base de datos en memoria
BASE_DE_DATOS = {}

# Pepper (opcional): leer de variable de entorno
PEPPER = os.environ.get("APP_PEPPER", "").encode()


def obtener_hasher() -> PasswordHasher:
    """
    Retorna un PasswordHasher con los parametros actuales.
    En produccion, estos parametros vendrian de la configuracion.
    """
    return PasswordHasher(
        time_cost=2,
        memory_cost=19456,   # 19 MiB (minimo OWASP)
        parallelism=1,
        hash_len=32,
        salt_len=16,
        type=Type.ID
    )


def preparar_password(password: str) -> str:
    """
    Prepara la contrasena antes de hashear.
    Si hay pepper, lo concatena.
    """
    if PEPPER:
        return password + PEPPER.decode()
    return password


def registrar(username: str, password: str) -> bool:
    """
    Registra un nuevo usuario.
    Retorna True si el registro fue exitoso, False si el usuario ya existe.
    """
    if username in BASE_DE_DATOS:
        print(f"  Error: el usuario '{username}' ya existe.")
        return False

    ph = obtener_hasher()
    password_preparado = preparar_password(password)
    hash_almacenado = ph.hash(password_preparado)

    BASE_DE_DATOS[username] = {
        "hash": hash_almacenado,
        "creado": time.time()
    }

    print(f"  Usuario '{username}' registrado exitosamente.")
    return True


def login(username: str, password: str) -> bool:
    """
    Intenta autenticar un usuario.
    Si los parametros del hash son obsoletos, re-hashea automaticamente.
    """
    if username not in BASE_DE_DATOS:
        print(f"  Error: usuario '{username}' no encontrado.")
        return False

    ph = obtener_hasher()
    password_preparado = preparar_password(password)
    hash_almacenado = BASE_DE_DATOS[username]["hash"]

    try:
        ph.verify(hash_almacenado, password_preparado)

        # Verificar si necesita re-hash
        if ph.check_needs_rehash(hash_almacenado):
            nuevo_hash = ph.hash(password_preparado)
            BASE_DE_DATOS[username]["hash"] = nuevo_hash
            print(f"  Hash actualizado con parametros nuevos.")

        print(f"  Login exitoso para '{username}'.")
        return True

    except VerifyMismatchError:
        print(f"  Contrasena incorrecta para '{username}'.")
        return False


def benchmark_parametros():
    """
    Mide el tiempo de hasheo con diferentes parametros.
    Ejecuta en tu servidor para elegir los parametros adecuados.
    """
    print("\nBenchmark de parametros Argon2id:")
    print("-" * 60)

    configuraciones = [
        {"memory_cost": 19456,  "time_cost": 2, "desc": "OWASP minimo"},
        {"memory_cost": 47104,  "time_cost": 1, "desc": "OWASP opcion 1"},
        {"memory_cost": 65536,  "time_cost": 2, "desc": "64 MiB, 2 iters"},
        {"memory_cost": 131072, "time_cost": 2, "desc": "128 MiB, 2 iters"},
        {"memory_cost": 262144, "time_cost": 1, "desc": "256 MiB, 1 iter"},
    ]

    for config in configuraciones:
        ph = PasswordHasher(
            time_cost=config["time_cost"],
            memory_cost=config["memory_cost"],
            parallelism=1,
            hash_len=32,
            salt_len=16,
            type=Type.ID
        )

        tiempos = []
        for _ in range(3):
            inicio = time.time()
            ph.hash("password_de_prueba")
            tiempos.append(time.time() - inicio)

        promedio = sum(tiempos) / len(tiempos) * 1000
        memoria_mib = config["memory_cost"] / 1024
        print(f"  {config['desc']:>25}: "
              f"m={memoria_mib:>5.0f} MiB, t={config['time_cost']}: "
              f"{promedio:>7.1f} ms")


# --- EJECUCION ---

if __name__ == "__main__":
    print("=" * 60)
    print("EJERCICIO: Sistema de Login con Argon2id")
    print("=" * 60)

    # 1. Registrar usuarios
    print("\n--- Registro ---")
    registrar("alice", "Contrasena_Fuerte_2026!")
    registrar("bob", "dragon123")
    registrar("alice", "otra_contrasena")  # Debe fallar

    # 2. Login exitoso
    print("\n--- Login ---")
    login("alice", "Contrasena_Fuerte_2026!")
    login("bob", "dragon123")

    # 3. Login fallido
    print("\n--- Login fallido ---")
    login("alice", "contrasena_incorrecta")
    login("charlie", "no_existe")

    # 4. Benchmark
    benchmark_parametros()

    print("\n--- Contenido de la 'base de datos' ---")
    for user, datos in BASE_DE_DATOS.items():
        print(f"  {user}: {datos['hash'][:60]}...")
```

**Extensiones sugeridas:**

1. Agrega un pepper leyendo la variable de entorno `APP_PEPPER` antes de ejecutar.
2. Cambia los parametros del hasher a valores mas altos y observa como `check_needs_rehash` detecta los hashes viejos.
3. Implementa un limite de intentos de login (rate limiting) para defensa en profundidad.
4. Mide cuanto tarda un "ataque de diccionario" con 1000 contrasenas contra Argon2id vs SHA-256.

---

## Referencias del capitulo

- Biryukov, A., Dinu, D., y Khovratovich, D. (2015). *Argon2: the memory-hard function for password hashing and other applications*. Password Hashing Competition.
- Kaliski, B. (2000). *PKCS #5: Password-Based Cryptography Specification Version 2.0*. RFC 2898.
- Krebs, B. (2016). "As Scope of 2012 Breach Expands, LinkedIn to Again Reset Passwords for Some Users". Krebs on Security.
- Malvoni, K., Knezovic, J., y Stipcevic, M. (2014). *Are Your Passwords Safe: Energy-Efficient Bcrypt Cracking with Low-Cost Parallel Hardware*. USENIX WOOT '14.
- OWASP (2025). *Password Storage Cheat Sheet*. OWASP Cheat Sheet Series.
- Password Hashing Competition (2015). https://www.password-hashing.net/
- Percival, C. (2009). *Stronger Key Derivation via Sequential Memory-Hard Functions*. Tarsnap.
- Provos, N. y Mazieres, D. (1999). *A Future-Adaptable Password Scheme*. USENIX Annual Technical Conference.
- RFC 9106 (2022). *Argon2 Memory-Hard Function for Password Hashing and Proof-of-Work Applications*.
- Schneier, B. (2013). "Cryptographic Blunders Revealed by Adobe's Password Leak". Schneier on Security.
- TechCrunch (2016). "117 million LinkedIn emails and passwords from a 2012 hack just got posted online".
