# Capitulo 4: SHA-3 y Keccak: la construccion de esponja

> "SHA-3 no es una version mejorada de SHA-2. Es una familia completamente diferente, disenada desde cero con una arquitectura que no se parece a nada que vimos en el capitulo anterior."

---

Que pasaria si todos los hashes de la familia SHA compartieran una misma debilidad estructural? No una debilidad en un algoritmo especifico como la funcion de compresion de MD5, sino una debilidad en la **arquitectura misma** --la construccion de Merkle-Damgard?

El NIST decidio no esperar a descubrirlo. En 2007, organizo una competencia publica global para encontrar un hash con un diseno radicalmente diferente. Sesenta y cuatro algoritmos de equipos de todo el mundo compitieron durante cinco anos. El ganador fue un algoritmo que se parece mas a una esponja que a una trituradora.

Este capitulo explica como funciona ese algoritmo, por que es inmune a los ataques que afectan a SHA-2, y cuando deberias elegirlo.

---

## 4.1 El concurso SHA-3: como se elige un estandar criptografico

### 4.1.1 Por que el NIST lanzo un concurso

En 2004, Xiaoyun Wang destrozo MD5 con ataques de colision practicos. Un ano despues, publico ataques teoricos contra SHA-1 que reducian la complejidad de colision a 2^69, muy por debajo del nivel ideal de 2^80 [Wang, Yin y Yu, 2005].

SHA-2 no estaba comprometido --y sigue sin estarlo en 2026-- pero comparte la misma construccion Merkle-Damgard que MD5 y SHA-1. Si alguien descubriera un ataque contra la construccion misma, toda la familia SHA caeria junta.

El NIST decidio que necesitaba **diversidad algoritmica**: un hash construido con matematicas completamente diferentes, que pudiera servir como respaldo en caso de que SHA-2 fuera comprometido. En 2007, convoco una competencia publica, siguiendo el modelo exitoso que habia usado para seleccionar AES (el cifrado simetrico estandar) en el ano 2000 [NIST, 2007].

### 4.1.2 Los finalistas y la seleccion

La respuesta fue masiva: 64 candidatos fueron enviados antes de la fecha limite a finales de 2008. La primera ronda de evaluacion elimino a los que tenian vulnerabilidades obvias o rendimiento inaceptable, dejando 51 candidatos validos. Una segunda ronda en julio de 2009 redujo el campo a 14 algoritmos. Finalmente, en diciembre de 2010, cinco finalistas fueron seleccionados:

1. **BLAKE** - Basado en ChaCha (cifrado de flujo). Extremadamente rapido. Su sucesor, BLAKE2, se convirtio en un favorito de la industria.
2. **Grostl** - Basado en la estructura de AES. Buena seguridad pero rendimiento moderado.
3. **JH** - Disenado por Hongjun Wu. Enfoque innovador pero menos analizado.
4. **Keccak** - Construccion de esponja. Diseno radicalmente diferente de todo lo anterior.
5. **Skein** - Disenado por Bruce Schneier y equipo. Basado en el cifrado de bloques Threefish.

Los criterios de evaluacion incluian seguridad, rendimiento en software y hardware, simplicidad del diseno, y flexibilidad. El 2 de octubre de 2012, el NIST anuncio que **Keccak** era el ganador [NIST, 2012].

Keccak gano no por ser el mas rapido (BLAKE era mas rapido en software) ni por tener el diseno mas conservador (Skein estaba respaldado por nombres mas conocidos). Gano porque su construccion de esponja era **completamente diferente** de Merkle-Damgard. Si SHA-2 cayera, SHA-3 no caeria con el, porque no comparten ninguna debilidad estructural.

Como dijo el equipo del NIST: "La razon principal de la seleccion de Keccak es la diversidad. Su diseno difiere fundamentalmente de SHA-2 en una forma que ofrece proteccion contra cualquier ataque futuro a la estructura Merkle-Damgard" [NIST, 2012].

### 4.1.3 La polemica de los parametros

Despues de seleccionar a Keccak, el NIST propuso en 2013 un cambio que provoco una reaccion fuerte de la comunidad criptografica. Los disenadores originales de Keccak habian propuesto una capacidad de `c = 2d` (donde `d` es el tamano del digest), lo que proporcionaria seguridad completa equivalente a SHA-2. El NIST propuso reducirla a `c = d`, lo que habria acelerado el algoritmo pero reducido la resistencia a preimagen a la mitad.

La reaccion fue rapida y contundente. **Bruce Schneier** advirtio que el NIST arriesgaba "publicar un algoritmo en el que nadie va a confiar". Daniel Bernstein y otros criptografos prominentes escribieron cartas publicas de preocupacion.

En noviembre de 2013, John Kelsey del NIST propuso volver a los parametros originales (`c = 2d`). Los parametros finales, publicados en FIPS 202 en agosto de 2015, mantienen la seguridad completa propuesta por los disenadores [NIST, 2015].

El episodio es revelador: la comunidad criptografica funciona como un sistema de revisores vigilantes. Cualquier intento de debilitar un estandar --intencional o no-- genera una respuesta inmediata.

---

## 4.2 La construccion de esponja: como funciona Keccak

### 4.2.1 Intuicion: por que "esponja"

Imagina una esponja de cocina. En la fase de **absorcion**, la sumerges en agua y absorbe liquido. En la fase de **exprimido**, la aprietas y sale agua. La cantidad de agua que sale depende de cuanto aprietes, no de cuanto absorbio.

La construccion de esponja funciona de manera analoga con datos:

1. **Absorcion**: el mensaje se "absorbe" en un estado interno grande, bloque por bloque
2. **Exprimido**: el hash se "exprime" del estado interno, tantos bits como necesites

Esta es la diferencia fundamental con Merkle-Damgard: en la esponja, el tamano de la salida es flexible. Puedes pedir 256 bits, 512 bits, o 10,000 bits. Esto abre la puerta a las funciones de salida extensible (XOF) que veremos mas adelante.

### 4.2.2 El estado interno y la permutacion keccak-f

El corazon de SHA-3 es una **funcion de permutacion** llamada **keccak-f[1600]**. No es un cifrado (no usa llave). Es una permutacion: toma 1600 bits y los mezcla de manera determinista para producir 1600 bits.

El estado interno se organiza como una matriz tridimensional de 5 x 5 x 64 bits:

```
Estado de Keccak: 5 x 5 x 64 = 1600 bits

Visualizado como una matriz 5x5 de "lanes" de 64 bits:

     Col 0    Col 1    Col 2    Col 3    Col 4
    +--------+--------+--------+--------+--------+
R0  | 64 bit | 64 bit | 64 bit | 64 bit | 64 bit |
    +--------+--------+--------+--------+--------+
R1  | 64 bit | 64 bit | 64 bit | 64 bit | 64 bit |
    +--------+--------+--------+--------+--------+
R2  | 64 bit | 64 bit | 64 bit | 64 bit | 64 bit |
    +--------+--------+--------+--------+--------+
R3  | 64 bit | 64 bit | 64 bit | 64 bit | 64 bit |
    +--------+--------+--------+--------+--------+
R4  | 64 bit | 64 bit | 64 bit | 64 bit | 64 bit |
    +--------+--------+--------+--------+--------+

Total: 25 lanes x 64 bits = 1600 bits
```

La permutacion keccak-f[1600] aplica **24 rondas** de cinco operaciones en cada ronda:

1. **Theta (th)**: calcula la paridad de cada columna y la combina con columnas vecinas usando XOR. Proporciona difusion lineal rapida.

2. **Rho (rh)**: rota cada uno de los 25 "lanes" de 64 bits por una cantidad diferente de posiciones (basada en numeros triangulares: 0, 1, 3, 6, 10, 15...). Esto mezcla los bits verticalmente.

3. **Pi (pi)**: permuta la posicion de los 25 lanes dentro de la matriz. Es una reorganizacion espacial fija.

4. **Chi (chi)**: combina bits a lo largo de cada fila con la operacion `x = x XOR (NOT(y) AND z)`. Esta es la **unica operacion no lineal** de toda la permutacion, y es critica para la seguridad.

5. **Iota (io)**: XOR una constante de ronda en una posicion del estado para romper la simetria entre rondas.

```
Una ronda de keccak-f:

Estado entrada (1600 bits)
    |
    v
  [theta]  -- difusion lineal (paridad de columnas)
    |
    v
  [rho]    -- rotaciones por lane
    |
    v
  [pi]     -- permutacion de posiciones
    |
    v
  [chi]    -- mezcla no lineal (unica no lineal)
    |
    v
  [iota]   -- constante de ronda
    |
    v
Estado salida (1600 bits)

(Repetir 24 veces)
```

Lo elegante de este diseno es su simplicidad: toda la seguridad proviene de repetir cinco operaciones simples 24 veces. No hay tablas de sustitucion complejas (como las S-boxes de AES), no hay expansion de mensaje (como en SHA-256). Solo XOR, AND, NOT, y rotaciones.

### 4.2.3 Absorcion y exprimido: el proceso completo

El estado de 1600 bits se divide en dos partes:

- **Rate (r)**: la porcion del estado que interactua con la entrada/salida
- **Capacity (c)**: la porcion del estado que permanece oculta

La relacion es simple: `r + c = 1600`.

El **rate** determina la velocidad: cuanto mayor sea, mas datos se procesan por iteracion. La **capacity** determina la seguridad: cuanto mayor sea, mas bits permanecen inaccesibles para el atacante.

```
Estado de 1600 bits:

+------------------------+------------------+
|       Rate (r)         |  Capacity (c)    |
|                        |                  |
|  Interactua con los    |  Oculto.         |
|  datos de entrada      |  No se toca      |
|  y salida.             |  directamente.   |
|                        |                  |
+------------------------+------------------+
|<-------- 1600 bits totales ------------->|
```

**Fase de absorcion:**

1. El estado se inicializa con todos los bits en cero.
2. El mensaje se divide en bloques de `r` bits (con padding si es necesario).
3. Para cada bloque:
   a. Se aplica XOR entre el bloque y los primeros `r` bits del estado.
   b. Se aplica la permutacion keccak-f[1600] al estado completo.

**Fase de exprimido:**

1. Se leen los primeros `r` bits del estado como el primer bloque de salida.
2. Si se necesitan mas bits de salida:
   a. Se aplica keccak-f[1600] al estado.
   b. Se leen los siguientes `r` bits.
   c. Se repite hasta obtener la cantidad de bits deseada.

```
Fase de ABSORCION:

  M1        M2        M3
  |         |         |
  v         v         v
 [XOR]     [XOR]     [XOR]
  |  c=0    |         |
  v         v         v
[keccak-f][keccak-f][keccak-f]
                       |
                       v
Fase de EXPRIMIDO:
                       |
                  Lee r bits --> Z1 (primer bloque de salida)
                       |
                  [keccak-f]
                       |
                  Lee r bits --> Z2 (segundo bloque, si se necesita)
                       |
                      ...

Donde:
  Mn = Bloques del mensaje (de r bits cada uno)
  Zn = Bloques de salida (de r bits cada uno)
  [XOR] = XOR del bloque con los primeros r bits del estado
  [keccak-f] = Permutacion completa de 1600 bits
```

Veamos los parametros para cada variante de SHA-3:

```
| Variante   | Rate (r) | Capacity (c) | Salida | Seguridad    |
|            | (bits)   | (bits)       | (bits) | colision     |
|------------|----------|--------------|--------|--------------|
| SHA3-224   | 1152     | 448          | 224    | 112 bits     |
| SHA3-256   | 1088     | 512          | 256    | 128 bits     |
| SHA3-384   | 832      | 768          | 384    | 192 bits     |
| SHA3-512   | 576      | 1024         | 512    | 256 bits     |
| SHAKE128   | 1344     | 256          | var.   | min(d/2,128) |
| SHAKE256   | 1088     | 512          | var.   | min(d/2,256) |
```

Observa el trade-off: SHA3-512 tiene la mayor seguridad (c = 1024) pero el rate mas pequeno (r = 576), lo que lo hace mas lento. SHA3-256 es el punto dulce para la mayoria de aplicaciones.

### 4.2.4 Por que la esponja es inmune al ataque de extension de longitud

En el capitulo anterior vimos que el ataque de extension de longitud funciona porque en Merkle-Damgard el hash final **es** el estado interno completo. Conociendo el hash, conoces el estado y puedes continuar hasheando.

En la construccion de esponja, esto no funciona. La razon es la **capacity**:

```
Estado despues de la absorcion (1600 bits para SHA3-256):

+---------------------+-------------------+
|     Rate: 1088      |  Capacity: 512    |
|                     |                   |
|  Estos bits se      |  Estos bits NO    |
|  publican como      |  se publican.     |
|  parte del hash.    |  El atacante no   |
|                     |  los conoce.      |
+---------------------+-------------------+
       |                      |
       v                      v
  Hash publicado         Desconocido
  (256 bits)             para el atacante
```

El hash de SHA3-256 es solo una porcion del rate (256 de los 1088 bits del rate), y los 512 bits de capacity nunca se revelan. Un atacante que conoce el hash no puede reconstruir el estado interno completo porque le faltan, como minimo, los 512 bits de capacity.

Sin el estado interno completo, es imposible continuar la operacion de la esponja. El ataque de extension de longitud queda bloqueado estructuralmente.

Esto tiene una implicacion practica importante: `SHA3-256(secreto || mensaje)` **no es vulnerable** al ataque de extension de longitud. Esto no significa que debas usarlo asi --HMAC sigue siendo la mejor practica porque proporciona garantias de seguridad formales mas amplias--, pero si significa que SHA-3 es inherentemente mas robusto ante errores de uso.

### 4.2.5 Implementacion simplificada de una esponja

Para solidificar la comprension, implementemos una construccion de esponja simplificada. Esta version usa operaciones basicas en lugar de keccak-f, y es solo para fines educativos:

```python
"""
esponja_educativa.py

Implementacion simplificada de una construccion de esponja.
SOLO PARA FINES EDUCATIVOS. NO usar en produccion.
La permutacion real (keccak-f) tiene propiedades criptograficas
que esta version simplificada NO tiene.
"""


def permutacion_simple(estado: list[int], rondas: int = 12) -> list[int]:
    """
    Permutacion simplificada para demostrar el concepto.
    En Keccak real, esta seria keccak-f[1600] con 24 rondas
    de theta, rho, pi, chi, iota sobre 1600 bits.

    Esta version trabaja con bytes para simplicidad.
    """
    estado = list(estado)  # Copia
    n = len(estado)

    for ronda in range(rondas):
        # Paso 1: mezcla tipo theta (XOR con vecinos)
        temp = [0] * n
        for i in range(n):
            temp[i] = estado[i] ^ estado[(i + 1) % n] ^ estado[(i - 1) % n]

        # Paso 2: rotacion tipo rho (desplazar valores)
        for i in range(n):
            temp[i] = ((temp[i] << (ronda + i + 1)) | (temp[i] >> (8 - (ronda + i + 1) % 8))) & 0xFF

        # Paso 3: mezcla no lineal tipo chi
        resultado = [0] * n
        for i in range(n):
            resultado[i] = temp[i] ^ ((~temp[(i + 1) % n] & 0xFF) & temp[(i + 2) % n])

        # Paso 4: constante de ronda tipo iota
        resultado[0] ^= (ronda * 0x9E + 0x3779B9) & 0xFF

        estado = resultado

    return estado


def esponja(mensaje: bytes, rate: int = 4, capacity: int = 4,
            longitud_salida: int = 8) -> bytes:
    """
    Construccion de esponja simplificada.

    Parametros:
        mensaje: datos de entrada
        rate: tamano del rate en bytes (interactua con entrada/salida)
        capacity: tamano de la capacity en bytes (oculto)
        longitud_salida: bytes de salida deseados

    En Keccak real:
        rate + capacity = 200 bytes (1600 bits)
        rate = 136 bytes para SHA3-256
        capacity = 64 bytes para SHA3-256
    """
    tamano_estado = rate + capacity
    estado = [0] * tamano_estado

    # --- PADDING ---
    # Padding simple: agregar byte 0x06 y luego 0x80 al final del bloque
    # (Keccak real usa un padding especifico con el bit de dominio)
    mensaje_padded = bytearray(mensaje)
    mensaje_padded.append(0x06)
    while len(mensaje_padded) % rate != 0:
        mensaje_padded.append(0x00)
    mensaje_padded[-1] |= 0x80

    # --- FASE DE ABSORCION ---
    bloques = [mensaje_padded[i:i+rate] for i in range(0, len(mensaje_padded), rate)]

    for bloque in bloques:
        # XOR del bloque con los primeros 'rate' bytes del estado
        for i in range(rate):
            estado[i] ^= bloque[i]

        # Aplicar la permutacion al estado completo
        estado = permutacion_simple(estado)

    # --- FASE DE EXPRIMIDO ---
    salida = []
    while len(salida) < longitud_salida:
        # Extraer los primeros 'rate' bytes del estado
        salida.extend(estado[:rate])

        # Aplicar permutacion para obtener mas bytes si es necesario
        if len(salida) < longitud_salida:
            estado = permutacion_simple(estado)

    return bytes(salida[:longitud_salida])


# --- DEMOSTRACION ---
if __name__ == "__main__":
    # Hash basico
    msg1 = b"Hola mundo"
    msg2 = b"Hola Mundo"  # Solo una letra diferente

    h1 = esponja(msg1)
    h2 = esponja(msg2)

    print("Demostracion de la construccion de esponja")
    print("=" * 55)
    print(f"Mensaje 1: {msg1}")
    print(f"Hash 1:    {h1.hex()}")
    print(f"Mensaje 2: {msg2}")
    print(f"Hash 2:    {h2.hex()}")

    # Verificar efecto avalancha
    bits_diferentes = sum(
        bin(a ^ b).count('1') for a, b in zip(h1, h2)
    )
    total_bits = len(h1) * 8
    print(f"\nBits diferentes: {bits_diferentes}/{total_bits} "
          f"({bits_diferentes/total_bits*100:.1f}%)")
    print()

    # Demostrar salida de tamano variable (como XOF)
    print("Salida de tamano variable (como SHAKE):")
    for longitud in [4, 8, 16, 32]:
        h = esponja(b"semilla", longitud_salida=longitud)
        print(f"  {longitud:2d} bytes: {h.hex()}")

    print()
    print("Observa que los primeros bytes son consistentes:")
    print("Esto es una propiedad de la fase de exprimido.")

    # Demostrar inmunidad a extension de longitud
    print()
    print("Inmunidad a extension de longitud:")
    print("-" * 55)
    h_original = esponja(b"secreto" + b"mensaje")
    h_extendido = esponja(b"secreto" + b"mensaje" + b"extra")
    print(f"hash(secreto||mensaje):        {h_original.hex()}")
    print(f"hash(secreto||mensaje||extra): {h_extendido.hex()}")
    print("No hay relacion predecible entre ambos hashes.")
    print("Un atacante no puede calcular el segundo a partir del primero")
    print("porque no conoce los bits de capacity del estado interno.")
```

---

## 4.3 SHA-3 en la practica: codigo Python

### 4.3.1 Las cuatro variantes de tamano fijo

SHA-3 ofrece cuatro variantes de tamano fijo, disenadas como reemplazos directos de las variantes correspondientes de SHA-2:

```python
from hashlib import sha3_224, sha3_256, sha3_384, sha3_512

mensaje = b"Criptografia aplicada para desarrolladores"

# Las cuatro variantes de SHA-3
print("Variantes de SHA-3:")
print(f"  SHA3-224: {sha3_224(mensaje).hexdigest()}")
print(f"  SHA3-256: {sha3_256(mensaje).hexdigest()}")
print(f"  SHA3-384: {sha3_384(mensaje).hexdigest()}")
print(f"  SHA3-512: {sha3_512(mensaje).hexdigest()}")
print()

# Longitudes de salida
for nombre, func in [("SHA3-224", sha3_224), ("SHA3-256", sha3_256),
                     ("SHA3-384", sha3_384), ("SHA3-512", sha3_512)]:
    h = func(mensaje).hexdigest()
    print(f"  {nombre}: {len(h)} chars hex = {len(h)*4} bits")
```

Para la gran mayoria de aplicaciones, **SHA3-256** es la eleccion correcta. Ofrece 128 bits de seguridad contra colisiones y 256 bits contra preimagen, que es mas que suficiente para cualquier escenario practico actual.

### 4.3.2 SHAKE128 y SHAKE256: funciones de salida extensible (XOF)

Las funciones de salida extensible (XOF, por Extendable-Output Functions) son una de las innovaciones mas importantes que la construccion de esponja habilita. A diferencia de un hash de tamano fijo, una XOF puede producir **cualquier cantidad de bytes de salida** que necesites.

SHAKE128 y SHAKE256 estan definidas en el mismo estandar FIPS 202 [NIST, 2015]. Los numeros 128 y 256 se refieren al **nivel de seguridad** (bits de seguridad contra colisiones), no al tamano de salida.

```python
from hashlib import shake_128, shake_256

semilla = b"mi semilla criptografica"

# SHAKE puede producir salida de cualquier tamano
print("SHAKE256 con diferentes tamanos de salida:")
print(f"  16 bytes:  {shake_256(semilla).hexdigest(16)}")
print(f"  32 bytes:  {shake_256(semilla).hexdigest(32)}")
print(f"  64 bytes:  {shake_256(semilla).hexdigest(64)}")
print(f"  128 bytes: {shake_256(semilla).hexdigest(128)}")
print()

# Los primeros bytes siempre son los mismos
h16 = shake_256(semilla).hexdigest(16)
h32 = shake_256(semilla).hexdigest(32)
h64 = shake_256(semilla).hexdigest(64)

print("Consistencia de la salida (los primeros bytes no cambian):")
print(f"  16 bytes:  {h16}")
print(f"  32 bytes:  {h32}")
print(f"  64 bytes:  {h64}")
print(f"  Los primeros 32 chars son iguales? {h16 == h32[:32]}")
print(f"  Los primeros 64 chars son iguales? {h32 == h64[:64]}")
```

Esta propiedad es una consecuencia directa de la fase de exprimido: pedir mas bytes simplemente aplica mas rondas de permutacion y extrae mas datos del rate. Los bytes anteriores no cambian.

**Casos de uso de SHAKE:**

```python
from hashlib import shake_256

# 1. Generacion de llaves de tamano arbitrario
def derivar_llave(semilla: bytes, tamano_bytes: int) -> bytes:
    """
    Usa SHAKE256 como funcion de derivacion de llaves simple.
    Para derivacion real de llaves a partir de passwords,
    usa Argon2 (ver Capitulo 5).
    """
    return shake_256(semilla).digest(tamano_bytes)


# Generar una llave AES-256 (32 bytes)
llave_aes = derivar_llave(b"material_de_llave_123", 32)
print(f"Llave AES-256: {llave_aes.hex()}")

# Generar un IV de 16 bytes y una llave de 32 bytes del mismo material
material = b"material_de_llave_456"
todo = shake_256(material).digest(48)  # 32 + 16 bytes
llave = todo[:32]
iv = todo[32:48]
print(f"Llave: {llave.hex()}")
print(f"IV:    {iv.hex()}")
print()

# 2. Generador de bytes pseudo-aleatorios determinista
def generar_bytes_aleatorios(semilla: bytes, cantidad: int) -> bytes:
    """
    Generador pseudo-aleatorio determinista basado en SHAKE256.
    La misma semilla siempre produce la misma secuencia.

    NOTA: Para aleatoriedad criptografica real, usa os.urandom()
    o secrets.token_bytes(). Esto es util para pruebas
    reproducibles o derivacion determinista.
    """
    return shake_256(semilla).digest(cantidad)


datos = generar_bytes_aleatorios(b"mi_semilla_secreta", 100)
print(f"100 bytes pseudo-aleatorios: {datos.hex()[:80]}...")
print()

# 3. Hash de dominio separado (domain separation)
def hash_con_dominio(dominio: str, datos: bytes, tamano: int = 32) -> bytes:
    """
    Hashea datos con separacion de dominio usando SHAKE256.
    Diferentes dominios producen hashes completamente diferentes
    incluso con los mismos datos.
    """
    entrada = dominio.encode() + b'\x00' + datos
    return shake_256(entrada).digest(tamano)


# El mismo dato con diferente dominio produce hashes diferentes
dato = b"usuario_123"
h_auth = hash_con_dominio("autenticacion", dato)
h_cache = hash_con_dominio("cache", dato)
print(f"Dominio 'autenticacion': {h_auth.hex()}")
print(f"Dominio 'cache':         {h_cache.hex()}")
print(f"Son diferentes:          {h_auth != h_cache}")
```

### 4.3.3 Funciones derivadas: TupleHash, ParallelHash, cSHAKE

El NIST estandarizo funciones adicionales derivadas de Keccak en NIST SP 800-185 [NIST, 2016]:

- **cSHAKE** (customizable SHAKE): permite agregar una cadena de personalizacion al hash, proporcionando separacion de dominio estandarizada. Es la base de las demas funciones derivadas.

- **TupleHash**: hashea una tupla de datos de manera no ambigua. Resuelve el problema de que `hash("ab" + "cd") == hash("a" + "bcd")` al codificar la longitud de cada elemento.

- **ParallelHash**: disenado para hashear datos grandes de forma paralelizable. Divide la entrada en bloques que se pueden procesar en paralelo antes de combinar los resultados.

- **KMAC**: un MAC (codigo de autenticacion de mensajes) basado en Keccak que puede reemplazar a HMAC.

Estas funciones no estan disponibles en la libreria estandar de Python, pero si en la libreria `pycryptodome`:

```python
# pip install pycryptodome

# cSHAKE: SHAKE personalizable
from Crypto.Hash import cSHAKE128

# Dos hashes del mismo dato con diferente personalizacion
h1 = cSHAKE128.new(data=b"datos", custom=b"aplicacion_A")
h2 = cSHAKE128.new(data=b"datos", custom=b"aplicacion_B")

print(f"cSHAKE128 (app A): {h1.read(32).hex()}")
print(f"cSHAKE128 (app B): {h2.read(32).hex()}")
print("Los hashes son diferentes gracias a la personalizacion.")
print()

# KMAC: MAC basado en Keccak (alternativa a HMAC)
from Crypto.Hash import KMAC128

llave = b"mi_llave_secreta_de_32_bytes!!!!!"
mac = KMAC128.new(key=llave, data=b"mensaje a autenticar",
                  mac_len=32)
print(f"KMAC128: {mac.hexdigest()}")
```

---

## 4.4 SHA-2 vs SHA-3 vs BLAKE3: la comparacion definitiva

### 4.4.1 Rendimiento: quien gana y por que

La velocidad no lo es todo en criptografia, pero importa. Veamos una comparacion de rendimiento real:

```python
import hashlib
import time

def benchmark(nombre, funcion_hash, datos, repeticiones=5000):
    """Ejecuta un benchmark de rendimiento."""
    inicio = time.time()
    for _ in range(repeticiones):
        funcion_hash(datos).digest()
    duracion = time.time() - inicio
    tamano_mb = len(datos) * repeticiones / (1024 * 1024)
    velocidad = tamano_mb / duracion
    print(f"  {nombre:>12}: {duracion:.3f}s  ({velocidad:>8.1f} MB/s)")
    return velocidad


# Datos de prueba
datos_1kb = b"x" * 1024
datos_1mb = b"x" * (1024 * 1024)

# ---- Benchmark con datos pequenos (1 KB) ----
print("Benchmark con datos de 1 KB (50,000 repeticiones):")
print("-" * 55)
benchmark("SHA-256", hashlib.sha256, datos_1kb, 50000)
benchmark("SHA-512", hashlib.sha512, datos_1kb, 50000)
benchmark("SHA3-256", hashlib.sha3_256, datos_1kb, 50000)
benchmark("SHA3-512", hashlib.sha3_512, datos_1kb, 50000)
benchmark("BLAKE2b", hashlib.blake2b, datos_1kb, 50000)

# Intentar BLAKE3 si esta instalado
try:
    import blake3
    inicio = time.time()
    for _ in range(50000):
        blake3.blake3(datos_1kb).digest()
    dur = time.time() - inicio
    vel = len(datos_1kb) * 50000 / (1024 * 1024 * dur)
    print(f"  {'BLAKE3':>12}: {dur:.3f}s  ({vel:>8.1f} MB/s)")
except ImportError:
    print("  (BLAKE3 no instalado: pip install blake3)")

print()

# ---- Benchmark con datos grandes (1 MB) ----
print("Benchmark con datos de 1 MB (500 repeticiones):")
print("-" * 55)
benchmark("SHA-256", hashlib.sha256, datos_1mb, 500)
benchmark("SHA-512", hashlib.sha512, datos_1mb, 500)
benchmark("SHA3-256", hashlib.sha3_256, datos_1mb, 500)
benchmark("SHA3-512", hashlib.sha3_512, datos_1mb, 500)
benchmark("BLAKE2b", hashlib.blake2b, datos_1mb, 500)

try:
    import blake3
    inicio = time.time()
    for _ in range(500):
        blake3.blake3(datos_1mb).digest()
    dur = time.time() - inicio
    vel = len(datos_1mb) * 500 / (1024 * 1024 * dur)
    print(f"  {'BLAKE3':>12}: {dur:.3f}s  ({vel:>8.1f} MB/s)")
except ImportError:
    pass

print()
print("Notas:")
print("  - SHA-512 suele ser mas rapido que SHA-256 en CPUs de 64 bits")
print("  - SHA-3 es mas lento en software puro (sin instrucciones de HW)")
print("  - BLAKE2b es muy rapido incluso en software puro")
print("  - BLAKE3 es el mas rapido con datos grandes (paralelizable)")
print("  - Con datos pequenos (<1KB), las diferencias se reducen mucho")
```

Los resultados tipicos en hardware moderno (circa 2025-2026):

```
| Hash     | 1 KB (MB/s) | 1 MB (MB/s) | Notas                        |
|----------|-------------|-------------|------------------------------|
| SHA-256  | ~600-800    | ~600-800    | Con SHA-NI: ~2.8-3.2 GB/s   |
| SHA-512  | ~700-900    | ~700-900    | Mas rapido en CPUs de 64 bit |
| SHA3-256 | ~300-500    | ~300-500    | Sin aceleracion de hardware  |
| SHA3-512 | ~200-350    | ~200-350    | Rate menor = mas lento       |
| BLAKE2b  | ~800-1100   | ~800-1100   | Excelente balance            |
| BLAKE3   | ~800-1100   | ~3-8 GB/s   | Paralelizable para datos >4KB|
```

SHA-3 es consistentemente mas lento que SHA-2 en software puro. Esto no es un defecto; es una consecuencia del diseno. La permutacion keccak-f[1600] opera sobre 1600 bits de estado, mientras que la funcion de compresion de SHA-256 opera sobre bloques de 512 bits con 256 bits de estado. Mas estado significa mas mezcla por ronda, pero tambien mas trabajo.

Sin embargo, Keccak fue disenado para ser extremadamente eficiente en **hardware**. En implementaciones ASIC y FPGA, SHA-3 puede igualar o superar a SHA-2. Por eso paises y organizaciones que construyen hardware criptografico dedicado ven a SHA-3 como una opcion atractiva.

### 4.4.2 BLAKE2 y BLAKE3: la alternativa rapida

BLAKE fue uno de los finalistas del concurso SHA-3 y, aunque no gano, su sucesor BLAKE2 se convirtio en un favorito de la industria gracias a su velocidad excepcional [Aumasson et al., 2013].

**BLAKE2** viene en dos variantes:

- **BLAKE2b**: optimizado para plataformas de 64 bits, hasta 512 bits de salida
- **BLAKE2s**: optimizado para plataformas de 32 bits, hasta 256 bits de salida

BLAKE2 es mas rapido que MD5 pero tan seguro como SHA-3. Se usa en:

- **Argon2**: la funcion de hasheo de contrasenas recomendada (ver Capitulo 5)
- **WireGuard**: el VPN moderno que reemplazo a OpenVPN en muchos escenarios
- **IPFS**: el sistema de archivos interplanetario

**BLAKE3** (publicado en 2020) lleva el concepto mas alla con un arbol de Merkle interno que permite **paralelizacion nativa**. En procesadores modernos con multiples nucleos, BLAKE3 puede alcanzar velocidades de 8-15 GB/s, ordenes de magnitud mas rapido que cualquier otro hash.

```python
import hashlib

# BLAKE2b esta en la libreria estandar desde Python 3.6
mensaje = b"Criptografia aplicada"

# BLAKE2b con diferentes tamanos de salida
h_64 = hashlib.blake2b(mensaje, digest_size=64).hexdigest()
h_32 = hashlib.blake2b(mensaje, digest_size=32).hexdigest()
h_16 = hashlib.blake2b(mensaje, digest_size=16).hexdigest()

print("BLAKE2b con diferentes tamanos de salida:")
print(f"  64 bytes: {h_64}")
print(f"  32 bytes: {h_32}")
print(f"  16 bytes: {h_16}")
print()

# BLAKE2b con llave (funciona como MAC, sin necesidad de HMAC)
llave = b"mi_llave_secreta_de_auth"
h_mac = hashlib.blake2b(mensaje, key=llave, digest_size=32).hexdigest()
print(f"BLAKE2b como MAC: {h_mac}")
print("(BLAKE2 soporta keyed hashing nativamente, sin HMAC)")
print()

# BLAKE3 (requiere pip install blake3)
try:
    import blake3

    h3 = blake3.blake3(mensaje).hexdigest()
    print(f"BLAKE3: {h3}")

    # BLAKE3 tambien soporta tamano variable
    h3_64 = blake3.blake3(mensaje).hexdigest(length=64)
    print(f"BLAKE3 (64 bytes): {h3_64}")

    # BLAKE3 con derivacion de llaves
    h3_keyed = blake3.blake3(mensaje, key=b"0" * 32).hexdigest()
    print(f"BLAKE3 keyed: {h3_keyed}")
except ImportError:
    print("(BLAKE3 no instalado: pip install blake3)")
```

### 4.4.3 Guia de decision: cual elegir

```
Necesito un hash para...

+-- Cumplimiento regulatorio (FIPS, gobierno, finanzas)?
|   |
|   +-- Ya tengo SHA-2 en produccion? --> SHA-256 (FIPS 180-4)
|   +-- Nuevo sistema, quiero diversidad? --> SHA-3-256 (FIPS 202)
|
+-- Rendimiento es la prioridad?
|   |
|   +-- Necesito estandar reconocido? --> BLAKE2b
|   +-- Maximo rendimiento absoluto? --> BLAKE3
|   +-- Datos muy grandes y paralelizables? --> BLAKE3
|
+-- Necesito salida de tamano variable?
|   |
|   +-- Con seguridad de 256 bits? --> SHAKE256
|   +-- Con seguridad de 128 bits? --> SHAKE128
|
+-- MAC (autenticacion de mensajes)?
|   |
|   +-- Estandar NIST? --> HMAC-SHA-256 o KMAC
|   +-- Rendimiento? --> BLAKE2b con llave o BLAKE3 keyed
|
+-- Contrasenas?
|   |
|   NUNCA un hash de proposito general.
|   --> Argon2id (ver Capitulo 5)
|
+-- No se, dame la respuesta segura por defecto
    |
    --> SHA-256 (si necesitas compatibilidad)
    --> SHA3-256 (si es un proyecto nuevo)
```

La regla practica: **SHA-256 para compatibilidad, SHA-3-256 para proyectos nuevos, BLAKE3 cuando la velocidad importa**. Y como siempre: nunca uses un hash de proposito general para contrasenas.

---

## 4.5 Verificacion: SHA-3 es inmune a extension de longitud

Para cerrar el capitulo, demostremos empiricamente que SHA-3 no es vulnerable al ataque de extension de longitud que afecta a SHA-2:

```python
from hashlib import sha256, sha3_256

def demostrar_inmunidad_sha3():
    """
    Demuestra que SHA-3 no es vulnerable a extension de longitud,
    mientras que SHA-256 si lo es (en teoria, con las herramientas
    adecuadas).
    """
    secreto = b"mi_secreto_de_16b"
    mensaje = b"datos_originales"
    extension = b"datos_extra"

    # --- SHA-256 ---
    # El hash de SHA-256(secreto || mensaje) revela el estado interno completo
    h_sha256 = sha256(secreto + mensaje).hexdigest()

    # Un atacante puede reconstruir el estado interno
    # de los 8 registros de 32 bits directamente del hash
    import struct
    registros = struct.unpack('>8I', bytes.fromhex(h_sha256))
    print("SHA-256 -- Estado interno expuesto:")
    print(f"  Hash:      {h_sha256}")
    print(f"  Registros: {[hex(r) for r in registros]}")
    print(f"  El atacante conoce TODO el estado interno.")
    print(f"  Puede continuar hasheando desde este punto.")
    print()

    # --- SHA-3-256 ---
    h_sha3 = sha3_256(secreto + mensaje).hexdigest()

    # El hash de SHA-3-256 solo revela 256 de los 1600 bits del estado
    # Los 512 bits de capacity + los bits restantes del rate son desconocidos
    print("SHA-3-256 -- Estado interno protegido:")
    print(f"  Hash:                {h_sha3}")
    print(f"  Bits conocidos:      256 de 1600 ({256/1600*100:.1f}%)")
    print(f"  Bits desconocidos:   {1600-256} ({(1600-256)/1600*100:.1f}%)")
    print(f"  Bits de capacity:    512 (SIEMPRE ocultos)")
    print(f"  El atacante NO puede reconstruir el estado interno.")
    print(f"  El ataque de extension de longitud es IMPOSIBLE.")
    print()

    # --- Verificacion empirica ---
    # Si SHA-3 fuera vulnerable, hash(s||m||pad||ext) se podria calcular
    # a partir de hash(s||m). Verifiquemos que no es predecible:
    print("Verificacion empirica:")
    for ext in [b"a", b"b", b"c", b"admin", b"root"]:
        h = sha3_256(secreto + mensaje + ext).hexdigest()
        print(f"  SHA3-256(secreto||mensaje||{ext.decode():>5}): {h[:32]}...")
    print("  Cada extension produce un hash completamente impredecible.")
    print("  No hay patron que un atacante pueda explotar.")


demostrar_inmunidad_sha3()
```

---

## 4.6 Ejercicio integrador: benchmark y esponja

```python
#!/usr/bin/env python3
"""
sha3_benchmark.py

Ejercicio del Capitulo 4:
1. Benchmark completo de SHA-256 vs SHA-3-256 vs BLAKE2b
2. Uso de SHAKE256 como generador pseudo-aleatorio
3. Verificacion de inmunidad a extension de longitud

Requisitos: pip install blake3 (opcional, para benchmark de BLAKE3)
Uso: python sha3_benchmark.py
"""

import hashlib
import time
import os


def benchmark_completo():
    """Benchmark de todas las funciones hash principales."""
    print("=" * 70)
    print("BENCHMARK DE FUNCIONES HASH")
    print("=" * 70)

    tamanos = [64, 256, 1024, 4096, 65536, 1048576]  # bytes
    funciones = {
        "SHA-256": hashlib.sha256,
        "SHA-512": hashlib.sha512,
        "SHA3-256": hashlib.sha3_256,
        "SHA3-512": hashlib.sha3_512,
        "BLAKE2b": hashlib.blake2b,
    }

    # Intentar agregar BLAKE3
    try:
        import blake3
        funciones["BLAKE3"] = lambda d: blake3.blake3(d)
    except ImportError:
        pass

    # Encabezado
    print(f"{'Funcion':>12}", end="")
    for tam in tamanos:
        if tam >= 1048576:
            print(f"{'%dMB' % (tam // 1048576):>10}", end="")
        elif tam >= 1024:
            print(f"{'%dKB' % (tam // 1024):>10}", end="")
        else:
            print(f"{'%dB' % tam:>10}", end="")
    print()
    print("-" * (12 + 10 * len(tamanos)))

    for nombre, func in funciones.items():
        print(f"{nombre:>12}", end="")
        for tam in tamanos:
            datos = os.urandom(tam)
            # Ajustar repeticiones segun tamano
            reps = max(100, 100000 // max(tam, 1))

            inicio = time.time()
            for _ in range(reps):
                func(datos).digest()
            duracion = time.time() - inicio

            velocidad_mb = (tam * reps) / (1024 * 1024 * duracion)
            print(f"{velocidad_mb:>9.1f}M", end="")
        print()

    print()
    print("Valores en MB/s (mayor es mejor)")


def demostrar_shake():
    """Demuestra usos practicos de SHAKE256."""
    print()
    print("=" * 70)
    print("SHAKE256: FUNCIONES DE SALIDA EXTENSIBLE")
    print("=" * 70)
    print()

    # 1. Generar multiples llaves de una semilla maestra
    semilla_maestra = os.urandom(32)
    print(f"Semilla maestra: {semilla_maestra.hex()}")
    print()

    # Derivar 4 llaves de 32 bytes cada una
    material = hashlib.shake_256(semilla_maestra).digest(128)
    llaves = [material[i:i+32] for i in range(0, 128, 32)]

    print("Llaves derivadas:")
    for i, llave in enumerate(llaves):
        print(f"  Llave {i+1}: {llave.hex()}")

    print()

    # 2. Comparar con SHA-3-256 (tamano fijo)
    h_fijo = hashlib.sha3_256(semilla_maestra).hexdigest()
    h_shake_32 = hashlib.shake_256(semilla_maestra).hexdigest(32)

    print("SHA-3-256 vs SHAKE256 (32 bytes):")
    print(f"  SHA-3-256:        {h_fijo}")
    print(f"  SHAKE256(32):     {h_shake_32}")
    print(f"  Son diferentes:   {h_fijo != h_shake_32}")
    print("  (Usan diferentes bits de dominio en el padding)")


def verificar_extension():
    """Verifica inmunidad de SHA-3 a extension de longitud."""
    print()
    print("=" * 70)
    print("VERIFICACION: INMUNIDAD A EXTENSION DE LONGITUD")
    print("=" * 70)
    print()

    secreto = os.urandom(16)
    mensaje = b"operacion=transferir&monto=100"

    # Hash original
    h_original = hashlib.sha3_256(secreto + mensaje).hexdigest()
    print(f"Hash original: {h_original}")
    print()

    # Intentar "extender" (sin conocer el secreto)
    # Con Merkle-Damgard, conociendo h_original podemos calcular
    # el hash del mensaje extendido. Con SHA-3, NO.
    extension = b"&monto=999999"

    # Lo que un atacante intentaria:
    # Reconstruir el estado de 1600 bits a partir de 256 bits
    # Esto es imposible: le faltan 1344 bits (512 de capacity + 832 del rate)

    # Verificacion: el hash del mensaje extendido no es predecible
    h_extendido = hashlib.sha3_256(secreto + mensaje + extension).hexdigest()
    print(f"Hash extendido: {h_extendido}")
    print()
    print(f"Bits del estado conocidos por el atacante: 256 / 1600")
    print(f"Bits faltantes: 1344 (incluyendo 512 de capacity)")
    print(f"Intentos necesarios para adivinar: 2^512 (capacity)")
    print(f"Conclusion: el ataque de extension es computacionalmente imposible")


if __name__ == "__main__":
    benchmark_completo()
    demostrar_shake()
    verificar_extension()

    print()
    print("=" * 70)
    print("RESUMEN DE RECOMENDACIONES")
    print("=" * 70)
    print()
    print("  Compatibilidad / sistemas existentes --> SHA-256")
    print("  Proyectos nuevos / diversidad         --> SHA-3-256")
    print("  Rendimiento critico                   --> BLAKE2b o BLAKE3")
    print("  Salida de tamano variable              --> SHAKE256")
    print("  Contrasenas                            --> NUNCA un hash normal")
    print("                                            Usa Argon2id (Cap. 5)")
```

---

## Resumen del capitulo

En este capitulo exploramos SHA-3 y la construccion de esponja. Los puntos clave son:

1. **SHA-3 nacio de un concurso global** lanzado por el NIST en 2007 para crear un hash con diversidad algoritmica frente a SHA-2. De 64 candidatos, Keccak gano en 2012 por su diseno radicalmente diferente.

2. **La construccion de esponja** divide el estado en rate (velocidad) y capacity (seguridad). La fase de absorcion procesa la entrada con XOR y permutaciones; la fase de exprimido extrae la salida.

3. **SHA-3 es inmune al ataque de extension de longitud** porque los bits de capacity nunca se revelan. Un atacante no puede reconstruir el estado interno a partir del hash.

4. **SHAKE128 y SHAKE256** son funciones de salida extensible (XOF) que producen salidas de tamano arbitrario. Son utiles para derivacion de llaves, generacion pseudo-aleatoria y protocolos flexibles.

5. **La eleccion entre SHA-2, SHA-3 y BLAKE3** depende de tus prioridades: compatibilidad (SHA-256), diversidad y seguridad a futuro (SHA-3-256), o rendimiento (BLAKE3).

6. **La permutacion keccak-f[1600]** usa cinco operaciones simples (theta, rho, pi, chi, iota) repetidas 24 veces sobre un estado de 1600 bits. Su simplicidad es una fortaleza: menos componentes significa menos superficie para ataques.

En el siguiente capitulo abordaremos un problema diferente: por que los hashes de proposito general son **peligrosamente inadecuados** para almacenar contrasenas, y que funciones especializadas debes usar en su lugar.

---

## Referencias

- Aumasson, J.P. (2024). *Serious Cryptography*, 2nd ed. No Starch Press.
- Aumasson, J.P. et al. (2013). "BLAKE2: simpler, smaller, fast as MD5." ACNS 2013.
- Bertoni, G., Daemen, J., Peeters, M. y Van Assche, G. (2011). "The Keccak reference." Submission to NIST, Round 3.
- NIST (2007). "Announcing Request for Candidate Algorithm Nominations for a New Cryptographic Hash Algorithm (SHA-3) Family." Federal Register, Vol. 72, No. 212.
- NIST (2012). "NIST Selects Winner of Secure Hash Algorithm (SHA-3) Competition." Press release, October 2.
- NIST (2015). "SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions." FIPS PUB 202.
- NIST (2016). "SHA-3 Derived Functions: cSHAKE, KMAC, TupleHash and ParallelHash." SP 800-185.
- Stevens, M. et al. (2017). "The first collision for full SHA-1." Advances in Cryptology -- CRYPTO 2017.
- Wang, X., Yin, Y.L. y Yu, H. (2005). "Finding Collisions in the Full SHA-1." Advances in Cryptology -- CRYPTO 2005.
- Wong, D. (2021). *Real-World Cryptography*. Manning Publications.
