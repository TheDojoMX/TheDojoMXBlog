# Capitulo 1: No confies en lo que no entiendes + Tu primera funcion hash

> "Llamar `sha256()` no es hacer criptografia, de la misma manera que llamar `print()` no es escribir una novela."

---

## 1.1 Que es la criptografia y por que te importa

En 2012, LinkedIn sufrio una de las filtraciones de datos mas emblematicas de la historia. Un atacante robo 6.5 millones de hashes de contrasenas, y en cuestion de horas la comunidad de seguridad habia revertido la mayoria de ellos. La razon no fue que SHA-1 estuviera "roto" en el sentido formal; la razon fue que LinkedIn almacenaba los hashes **sin salt** --un valor aleatorio que se agrega antes de hashear-- lo que permitio ataques masivos con tablas precalculadas. Cuando en 2016 se descubrio que la filtracion real abarcaba **117 millones de cuentas**, el 90% de las contrasenas fueron descifradas en 72 horas [Krebs, 2016].

Un ano despues, Adobe revelo que 153 millones de cuentas habian sido comprometidas. Pero su error fue aun mas grave: en lugar de usar una funcion hash, cifraron las contrasenas con **3DES en modo ECB** --un modo de operacion que produce el mismo texto cifrado para el mismo texto plano-- y usaron **la misma llave para todas las contrasenas**. Si dos usuarios tenian la misma contrasena, el texto cifrado era identico byte a byte [Schneier, 2013]. Para empeorar las cosas, las "pistas de contrasena" se almacenaban en texto plano, lo que permitio reconstruir contrasenas populares sin siquiera tocar el cifrado.

Estos no son errores de criptografos novatos. Son errores de **desarrolladores que no entendian las herramientas que estaban usando**.

Un estudio de investigadores del MIT analizo 269 vulnerabilidades criptograficas reportadas en la base de datos CVE entre 2011 y 2014, y encontro que el **83% de los fallos no estaban en las librerias criptograficas**, sino en el codigo de aplicacion que las usaba mal [Lazar, Chen y Zeldovich, 2014]. No eran bugs en OpenSSL o en libsodium; eran desarrolladores llamando funciones correctas con parametros incorrectos, eligiendo modos de operacion equivocados, o reutilizando valores que debian ser unicos.

Y el problema no ha disminuido. En la edicion 2021 del OWASP Top 10, "Cryptographic Failures" subio al **puesto numero 2**, anteriormente conocida como "Sensitive Data Exposure". La razon del cambio de nombre es reveladora: el problema no es solo que los datos queden expuestos, sino que la criptografia que deberia protegerlos falla sistematicamente.

Este libro existe para que entiendas lo que estas haciendo cuando llamas a una funcion criptografica.

### 1.1.1 Definicion moderna de criptografia

La palabra "criptografia" viene del griego *kryptos* (oculto) y *graphein* (escribir). Literalmente: **escritura oculta**. Pero la criptografia moderna va mucho mas alla de ocultar mensajes.

Una definicion practica para desarrolladores:

> La criptografia es el conjunto de tecnicas matematicas que nos permiten garantizar **confidencialidad**, **integridad** y **autenticacion** de la informacion, incluso en presencia de adversarios activos.

Estas tres propiedades forman la triada fundamental:

- **Confidencialidad**: solo las partes autorizadas pueden leer la informacion. Esto se logra mediante cifrado.
- **Integridad**: la informacion no ha sido alterada desde su creacion. Esto se logra mediante funciones hash y codigos de autenticacion de mensajes (MAC).
- **Autenticacion**: puedes verificar quien creo o envio la informacion. Esto se logra mediante firmas digitales y protocolos de autenticacion.

Un detalle importante sobre terminologia: en espanol correcto, el proceso de ocultar informacion se llama **cifrado**, y el proceso inverso se llama **descifrado**. "Encriptar" y "desencriptar" son barbarismos del ingles que, aunque se usan ampliamente, no existen formalmente en espanol. En este libro usaremos la terminologia correcta.

### 1.1.2 Donde se usa la criptografia en tu stack diario

Si eres desarrollador, la criptografia esta en todas partes de tu trabajo, aunque no la veas directamente:

- **HTTPS/TLS**: cada request HTTP que tu aplicacion envia o recibe pasa por un protocolo criptografico que negocia llaves, cifra el trafico y verifica la identidad del servidor. Sin TLS, cualquier intermediario en la red podria leer y modificar el trafico.

- **Contrasenas en la base de datos**: si tu framework web almacena contrasenas, esta usando una funcion de derivacion de llaves como Argon2 o bcrypt. No un hash de proposito general como SHA-256 (hablaremos de por que en el Capitulo 5).

- **Tokens JWT y cookies firmadas**: cuando generas un JSON Web Token para autenticar usuarios, estas usando un HMAC o una firma digital para garantizar que el token no ha sido alterado.

- **Git**: cada commit, blob y tree en Git se identifica con un hash SHA-1 (y el proyecto esta migrando a SHA-256). La integridad de todo el historial de tu repositorio depende de funciones hash.

- **Cifrado de disco**: FileVault en macOS, BitLocker en Windows y LUKS en Linux cifran todo el contenido del disco con AES, protegiendo tus datos incluso si alguien roba fisicamente tu computadora.

- **SSH**: cada vez que te conectas a un servidor remoto, SSH usa criptografia de llave publica para autenticarte y cifrado simetrico para proteger la sesion.

- **WiFi**: WPA2 y WPA3 usan AES para cifrar todo el trafico entre tu dispositivo y el punto de acceso.

La criptografia no es algo que uses "a veces". Es algo que usas en cada linea de codigo que toca una red, un archivo o un usuario.

### 1.1.3 Tres preguntas antes de escribir codigo criptografico

Antes de llamar a cualquier funcion criptografica, hazte estas tres preguntas:

**1. Que propiedad necesito garantizar?**

No es lo mismo proteger la confidencialidad de un mensaje (necesitas cifrado) que verificar que un archivo no fue alterado (necesitas un hash) o demostrar que tu fuiste quien firmo un documento (necesitas una firma digital). Usar la herramienta equivocada es el error mas comun, y es exactamente lo que hizo Adobe al cifrar contrasenas en lugar de hashearlas.

**2. Quien es mi adversario y que recursos tiene?**

Un atacante casual que intenta adivinar contrasenas es muy diferente de un estado-nacion con acceso a supercomputadoras. El nivel de seguridad que necesitas depende directamente de contra quien te proteges. En la mayoria de los casos, seguir los estandares establecidos (AES-256, SHA-3, Argon2) es suficiente.

**3. Estoy usando la herramienta correcta con los parametros correctos?**

El 83% de los fallos criptograficos no son fallos en los algoritmos, sino en como los usamos [Lazar et al., 2014]. Modo ECB en lugar de GCM. Llaves estaticas en lugar de efimeras. Vectores de inicializacion reutilizados. La primitiva correcta mal usada es igual de peligrosa que ninguna primitiva.

Si puedes responder estas tres preguntas con confianza, estas en buen camino. Si no puedes, este libro te dara las herramientas para hacerlo.

### 1.1.4 El mapa de primitivas criptograficas

Antes de sumergirnos en los hashes, hagamos un recorrido rapido por todas las herramientas criptograficas que tienes a tu disposicion. Piensa en esto como el mapa de un taller: necesitas saber que herramientas existen antes de elegir la correcta.

```
PRIMITIVAS CRIPTOGRAFICAS
==========================

FUNCIONES HASH              CIFRADO SIMETRICO          CIFRADO ASIMETRICO
(huella digital)            (una llave)                (dos llaves)
  |                           |                          |
  +-- SHA-256                 +-- AES-GCM                +-- RSA
  +-- SHA-3                   +-- ChaCha20-Poly1305      +-- ECDSA
  +-- BLAKE2/BLAKE3           +-- AES-CBC (cuidado)      +-- Ed25519
  |                           |                          +-- X25519
  |                           |                          |
  v                           v                          v
Integridad               Confidencialidad         Autenticacion
Deduplicacion            Cifrado de datos         Firmas digitales
Compromiso               Cifrado de disco         Intercambio de llaves

FUNCIONES DE DERIVACION     GENERADORES ALEATORIOS     MAC
(contrasenas/llaves)        (semillas, llaves, IVs)    (integridad + autenticacion)
  |                           |                          |
  +-- Argon2                  +-- os.urandom()           +-- HMAC-SHA256
  +-- scrypt                  +-- secrets module         +-- Poly1305
  +-- bcrypt                  +-- /dev/urandom           +-- KMAC
```

En este capitulo nos enfocaremos en la primera columna: **funciones hash**. Son la primitiva criptografica mas fundamental y la que usaras con mas frecuencia.

---

## 1.2 Tu primer hash: manos al codigo

Suficiente teoria. Vamos a escribir codigo.

### 1.2.1 La metafora del picadillo

La palabra "hash" viene de la cocina francesa y significa **picadillo**. Un platillo donde los ingredientes se pican tan finamente que es imposible separar los componentes originales. Eso es exactamente lo que hace una funcion hash con los datos: los "pica" hasta que son irreconocibles.

Formalmente, una funcion hash es una funcion que:

1. Acepta una entrada de **cualquier tamano** (desde un byte hasta terabytes)
2. Produce una salida de **tamano fijo** (por ejemplo, 256 bits para SHA-256)
3. Es **determinista**: la misma entrada siempre produce la misma salida
4. Es **irreversible**: no puedes recuperar la entrada a partir de la salida

Piensa en una licuadora: puedes meter un mango, dos platanos y un litro de leche. Siempre obtendras un vaso de licuado. Pero nadie puede mirar el licuado y separar de nuevo el mango, los platanos y la leche.

### 1.2.2 Hashea tu primer mensaje

Abre una terminal de Python y escribe esto:

```python
from hashlib import sha256

mensaje = b"Hola mundo"
h = sha256(mensaje).hexdigest()
print(h)
# ca8f60b2cc7f05837d98b208b57fb6481553fc5f1219d59618fd025002a66f5c
```

Vamos a descomponer lo que acaba de pasar:

1. `sha256()` crea un objeto de hasheo que implementa el algoritmo SHA-256, definido en NIST FIPS 180-4 [NIST, 2015].
2. Le pasamos `b"Hola mundo"` -- el prefijo `b` indica que es una secuencia de bytes, no una cadena de texto. Las funciones hash operan sobre bytes, no sobre caracteres.
3. `.hexdigest()` nos devuelve el hash como una cadena de **64 caracteres hexadecimales**. Cada caracter hexadecimal representa 4 bits, asi que 64 caracteres = 256 bits.

Ahora intenta con entradas de diferentes tamanos:

```python
from hashlib import sha256

# Un solo byte
print(sha256(b"a").hexdigest())
# ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb

# Una oracion
print(sha256(b"La criptografia es fascinante").hexdigest())
# 5f1d6a574b28a0d6eaf3b6aabe1b4e5bfcdc10b3f6bf01a2d48f0c6e80024f37

# Un parrafo completo
texto_largo = b"Lorem ipsum dolor sit amet, " * 100
print(sha256(texto_largo).hexdigest())
# Siempre 64 caracteres hexadecimales, sin importar la longitud de la entrada

print(f"Entrada: {len(texto_largo)} bytes -> Salida: {len(sha256(texto_largo).hexdigest())} caracteres hex")
```

Observa: sin importar si la entrada tiene 1 byte o 2,800 bytes, la salida **siempre** tiene exactamente 64 caracteres hexadecimales (256 bits). Esta propiedad de tamano fijo es fundamental.

Ahora hasheemos un archivo completo:

```python
from hashlib import sha256

def hashear_archivo(ruta):
    """Calcula el SHA-256 de un archivo, leyendolo en bloques."""
    h = sha256()
    with open(ruta, "rb") as f:
        while bloque := f.read(8192):  # Lee en bloques de 8 KB
            h.update(bloque)
    return h.hexdigest()

# Pruebalo con cualquier archivo en tu sistema
# hash_resultado = hashear_archivo("mi_archivo.pdf")
# print(hash_resultado)
```

La lectura en bloques es importante para archivos grandes: no necesitas cargar todo el archivo en memoria. El metodo `update()` va alimentando datos al algoritmo de manera incremental, y el hash final considera todos los bytes que recibio.

### 1.2.3 El efecto avalancha: tu primer "a-ha"

Ahora viene lo interesante. Observa que pasa cuando cambias un solo caracter en la entrada:

```python
from hashlib import sha256

h1 = sha256(b"Hola mundo").hexdigest()
h2 = sha256(b"Hola Mundo").hexdigest()  # Solo cambia 'm' por 'M'

print(f"Entrada 1: 'Hola mundo'")
print(f"Hash 1:    {h1}")
print()
print(f"Entrada 2: 'Hola Mundo'")
print(f"Hash 2:    {h2}")
print()

# Contemos cuantos caracteres son diferentes
diferentes = sum(1 for a, b in zip(h1, h2) if a != b)
print(f"Caracteres diferentes: {diferentes} de {len(h1)} ({diferentes/len(h1)*100:.1f}%)")
```

Resultado:

```
Entrada 1: 'Hola mundo'
Hash 1:    ca8f60b2cc7f05837d98b208b57fb6481553fc5f1219d59618fd025002a66f5c
Entrada 2: 'Hola Mundo'
Hash 2:    5e6586c8e33adae85abad95041a1bc994807e1d52e6e80d23a18e2e16c57a42a

Caracteres diferentes: 59 de 64 (92.2%)
```

Cambiar **una sola letra** -- de minuscula a mayuscula -- produjo un hash completamente diferente. Mas del 90% de los caracteres cambiaron. Esto se llama el **efecto avalancha**, y es una propiedad critica de cualquier funcion hash criptografica.

Veamoslo a nivel de bits para apreciar mejor el fenomeno:

```python
from hashlib import sha256

def hash_a_bits(mensaje):
    """Convierte un hash a su representacion binaria."""
    h = sha256(mensaje).digest()  # bytes crudos, no hex
    return ''.join(f'{byte:08b}' for byte in h)

bits1 = hash_a_bits(b"Hola mundo")
bits2 = hash_a_bits(b"Hola Mundo")

# Contar bits que cambiaron
bits_diferentes = sum(1 for a, b in zip(bits1, bits2) if a != b)
total_bits = len(bits1)

print(f"Total de bits: {total_bits}")
print(f"Bits que cambiaron: {bits_diferentes}")
print(f"Porcentaje: {bits_diferentes/total_bits*100:.1f}%")
```

```
Total de bits: 256
Bits que cambiaron: 131
Porcentaje: 51.2%
```

Aproximadamente el **50%** de los bits cambian. Esto no es coincidencia. Una funcion hash criptografica bien disenada debe cambiar, en promedio, la mitad de los bits de salida cuando un solo bit de entrada cambia. Es como si cada bit de la salida fuera decidido por un lanzamiento de moneda independiente [Aumasson, 2024].

Este es tu primer "a-ha" criptografico: **un cambio minimo en la entrada produce un cambio catastrofico e impredecible en la salida**. Esto es lo que hace util a un hash para verificar integridad. Si alguien modifica un solo byte de un archivo, el hash sera completamente diferente.

### 1.2.4 Propiedades formales de un hash

Resumamos las cuatro propiedades que acabamos de observar en codigo:

| Propiedad | Que significa | Por que importa |
|-----------|--------------|-----------------|
| **Tamano fijo** | La salida siempre tiene la misma longitud | Puedes comparar hashes sin importar el tamano de los datos originales |
| **Determinismo** | Misma entrada = misma salida, siempre | Permite verificacion: hasheas de nuevo y comparas |
| **Efecto avalancha** | Cambio minimo en entrada = cambio masivo en salida | Impide deducir la entrada a partir del hash |
| **Irreversibilidad** | No puedes recuperar la entrada desde la salida | Se pierde informacion: infinitas entradas mapean a cada salida |

La irreversibilidad merece una explicacion adicional. SHA-256 produce 256 bits de salida, lo que significa que hay exactamente 2^256 posibles hashes. Pero las entradas posibles son **infinitas** -- cualquier secuencia de bytes de cualquier longitud. Por el principio del palomar (o principio de Dirichlet), infinitas entradas deben compartir cada hash. La informacion simplemente **se pierde** durante el proceso de hasheo, y no hay forma de recuperarla.

---

## 1.3 Hashes criptograficos: cuando "picar" no es suficiente

No todas las funciones hash son iguales. La funcion `hash()` de Python, por ejemplo, esta disenada para tablas hash, no para seguridad. Necesitamos entender que hace *criptografico* a un hash.

### 1.3.1 Hashes no criptograficos vs criptograficos

Considera esta funcion hash extremadamente simple:

```python
def hash_simple(x):
    """Un hash no criptografico: el residuo de dividir entre 10."""
    return x % 10
```

Esta funcion cumple con ser determinista y de tamano fijo. Pero es completamente inutil para seguridad porque:

- Es facil encontrar colisiones: `hash_simple(7) == hash_simple(17) == hash_simple(27)`
- Es trivial revertirla para un rango de valores conocido
- No tiene efecto avalancha: entradas similares producen salidas similares

Funciones hash no criptograficas reales como **MurmurHash**, **FNV-1a**, **xxHash** y la funcion `hash()` de Python estan optimizadas para velocidad y distribucion uniforme, lo que las hace excelentes para tablas hash y estructuras de datos. Pero **no resisten ataques deliberados**. Un adversario puede encontrar colisiones y preimages con relativa facilidad.

Un hash criptografico agrega una propiedad crucial: su salida es **computacionalmente indistinguible de datos aleatorios**, incluso para una computadora. No revela ningun patron, ningun sesgo estadistico, ninguna pista sobre la entrada. Resiste analisis estadisticos sofisticados.

### 1.3.2 Las tres resistencias

Un hash criptografico seguro cumple con tres garantias formales. Estas son las propiedades que lo separan de un hash comun:

**Resistencia a preimagen (primera preimagen)**

Dado un hash `h`, es computacionalmente imposible encontrar un mensaje `m` tal que `hash(m) = h`.

```
Dado:     h = 5e6586c8e33adae85abad95041a1bc99...
Encontrar: m tal que SHA-256(m) = h

Complejidad: 2^256 intentos en el peor caso
             (mas que atomos en el universo observable)
```

Esto garantiza que si publicas el hash de un documento, nadie puede reconstruir el documento a partir del hash.

**Resistencia a segunda preimagen**

Dado un mensaje `m1` y su hash `h = hash(m1)`, es computacionalmente imposible encontrar un mensaje diferente `m2` tal que `hash(m2) = h`.

```
Dado:     m1 = "contrato_original.pdf"
          h  = SHA-256(m1) = a1b2c3d4...
Encontrar: m2 != m1 tal que SHA-256(m2) = a1b2c3d4...

Complejidad: 2^256 intentos
```

Esto garantiza que nadie puede crear un documento falso que tenga el mismo hash que tu documento original. Si firmas un contrato digitalmente (lo que internamente hashea el documento), nadie puede sustituirlo por otro contrato con la misma firma.

**Resistencia a colisiones**

Es computacionalmente imposible encontrar **cualquier par** de mensajes `m1` y `m2` (con `m1 != m2`) tales que `hash(m1) = hash(m2)`.

```
Encontrar: cualquier m1, m2 con m1 != m2
           tal que SHA-256(m1) = SHA-256(m2)

Complejidad: ~2^128 intentos (por la paradoja del cumpleanos)
```

Nota que la resistencia a colisiones es mas debil que la resistencia a preimagen. No necesitas encontrar un mensaje que coincida con un hash especifico; necesitas encontrar *cualquier* par que colisione. Por la paradoja del cumpleanos, esto requiere aproximadamente 2^(n/2) intentos para un hash de n bits, no 2^n.

Veamos la resistencia a colisiones en accion. Intentemos encontrar una colision parcial (los primeros 2 bytes del hash) por fuerza bruta:

```python
from hashlib import sha256
import time

def buscar_colision_parcial(n_bytes=2):
    """
    Busca dos mensajes diferentes cuyos hashes compartan
    los primeros n_bytes bytes. Demuestra la paradoja del cumpleanos.
    """
    vistos = {}  # hash parcial -> mensaje
    intentos = 0
    inicio = time.time()

    while True:
        # Genera un mensaje unico
        mensaje = f"mensaje_{intentos}".encode()
        h = sha256(mensaje).digest()[:n_bytes]  # Solo primeros n_bytes

        if h in vistos and vistos[h] != mensaje:
            duracion = time.time() - inicio
            print(f"Colision encontrada en {intentos:,} intentos ({duracion:.2f}s)")
            print(f"  Mensaje 1: {vistos[h]}")
            print(f"  Mensaje 2: {mensaje}")
            print(f"  Hash parcial ({n_bytes} bytes): {h.hex()}")
            print(f"  Esperado teorico: ~{2**(n_bytes*8//2):,} intentos")
            return vistos[h], mensaje

        vistos[h] = mensaje
        intentos += 1

# Colision en primeros 2 bytes (16 bits): ~256 intentos esperados
buscar_colision_parcial(2)

# Colision en primeros 3 bytes (24 bits): ~4,096 intentos esperados
buscar_colision_parcial(3)
```

Ejecuta este codigo y observa: encontrar una colision en 2 bytes toma alrededor de 256 intentos (2^8, la raiz cuadrada de 2^16 posibles valores). Para 3 bytes, toma alrededor de 4,096 intentos (2^12). Esto es la paradoja del cumpleanos en accion.

Ahora imagina escalar esto a 32 bytes (256 bits). Necesitarias aproximadamente 2^128 intentos. Incluso con todas las computadoras del planeta trabajando juntas, esto tomaria mas tiempo que la edad del universo.

### 1.3.3 Catalogo de funciones hash seguras

Ahora que entiendes las propiedades, veamos el catalogo completo de funciones hash que encontraras en la practica:

**MD5 -- ROTO. No usar nunca.**

- Salida: 128 bits (32 caracteres hex)
- Estado: colisiones encontradas en segundos con una laptop comun
- Historia: en 2012, el malware Flame --atribuido a operaciones de inteligencia de Estados Unidos e Israel-- forjo un certificado de Microsoft usando una colision MD5. Windows Update entrego malware firmado "legitimamente" a usuarios iranies [Schneier, 2012].
- Veredicto: no lo uses ni para integridad de archivos no critica. Existe demasiado codigo legacy que sigue dependiendo de MD5; si lo encuentras en tu proyecto, migralo.

**SHA-1 -- ROTO. Depreciado oficialmente.**

- Salida: 160 bits (40 caracteres hex)
- Estado: colision practica demostrada en 2017
- Historia: el 23 de febrero de 2017, investigadores de Google y CWI Amsterdam publicaron el ataque **SHAttered**, generando dos archivos PDF diferentes con el mismo hash SHA-1 en aproximadamente 2^63.1 evaluaciones. El ataque costo alrededor de $110,000 USD en computo en la nube [Stevens et al., 2017]. Git aun usa SHA-1 internamente, pero esta migrando a SHA-256.
- Veredicto: no lo uses para nuevos proyectos. Planifica la migracion si lo tienes en produccion.

**SHA-2 (SHA-256, SHA-384, SHA-512) -- Seguro. Estandar actual.**

- Salida: 256, 384 o 512 bits
- Estado: sin vulnerabilidades practicas conocidas
- Rendimiento: ~2.8-3.2 GB/s en procesadores x86-64 con instrucciones SHA-NI (Intel Alder Lake, AMD Zen 3+). En Apple M3, aproximadamente 2.1 GB/s.
- Estandar: NIST FIPS 180-4 [NIST, 2015]
- Veredicto: SHA-256 es la opcion segura por defecto. Bitcoin lo usa para su proof-of-work. Es la funcion hash mas desplegada en el mundo.

**SHA-3 (Keccak) -- Seguro. Diseno completamente diferente.**

- Salida: 224, 256, 384 o 512 bits (mas funciones de salida variable: SHAKE128, SHAKE256)
- Estado: sin vulnerabilidades conocidas
- Rendimiento: mas lento que SHA-2 en software puro (~2-3x mas lento sin aceleracion por hardware), pero su diseno interno (construccion esponja) es fundamentalmente diferente de SHA-2
- Estandar: NIST FIPS 202 [NIST, 2015]
- Veredicto: recomendado para nuevos proyectos donde la diversidad criptografica importa. Si SHA-2 fuera comprometido, SHA-3 no se veria afectado porque usa matematicas completamente diferentes.

**BLAKE2 / BLAKE3 -- Seguro. El mas rapido.**

- Salida: configurable (BLAKE2b hasta 512 bits, BLAKE3 hasta 256 bits)
- Estado: sin vulnerabilidades conocidas
- Rendimiento: BLAKE3 es 4-10x mas rapido que SHA-256 gracias a su diseno paralelizable
- Veredicto: excelente cuando el rendimiento es critico. BLAKE2 esta disponible en `hashlib` de Python desde la version 3.6.

Tabla comparativa:

```
| Funcion   | Bits salida | Velocidad relativa | Estado     | Usar para...              |
|-----------|-------------|--------------------| -----------|---------------------------|
| MD5       | 128         | ++++++             | ROTO       | NADA (migrar urgente)     |
| SHA-1     | 160         | +++++              | ROTO       | NADA (migrar)             |
| SHA-256   | 256         | +++                | Seguro     | Estandar general          |
| SHA-512   | 512         | +++                | Seguro     | Cuando necesitas mas bits |
| SHA3-256  | 256         | ++                 | Seguro     | Nuevos proyectos          |
| BLAKE2b   | hasta 512   | ++++               | Seguro     | Rendimiento + seguridad   |
| BLAKE3    | 256         | +++++++            | Seguro     | Maximo rendimiento        |
```

Veamos como usar varias de estas funciones en Python:

```python
from hashlib import sha256, sha3_256, blake2b, md5, sha1

mensaje = b"Criptografia aplicada para desarrolladores"

# SHA-256: el estandar
print(f"SHA-256:   {sha256(mensaje).hexdigest()}")

# SHA-3-256: la alternativa moderna
print(f"SHA3-256:  {sha3_256(mensaje).hexdigest()}")

# BLAKE2b: rapido y seguro
print(f"BLAKE2b:   {blake2b(mensaje).hexdigest()}")

# MD5 y SHA-1: solo para mostrar que estan disponibles.
# NUNCA los uses para seguridad.
print(f"MD5 (NO!): {md5(mensaje).hexdigest()}")
print(f"SHA1 (NO!):{sha1(mensaje).hexdigest()}")
```

---

## 1.4 Que hash usar y cuando

### 1.4.1 Arbol de decision para elegir un hash

Cuando necesites una funcion hash, sigue este arbol de decision:

```
Necesito un hash para...
|
+-- Contrasenas?
|   |
|   NO -> Nunca uses SHA-256/SHA-3 para contrasenas.
|          Usa Argon2id, scrypt, o bcrypt. (Ver Capitulo 5)
|
+-- Integridad de archivos / firmas digitales?
|   |
|   +-- Necesito compatibilidad con sistemas existentes? -> SHA-256
|   +-- Es un proyecto nuevo? -> SHA-3-256
|   +-- La velocidad es critica? -> BLAKE3
|
+-- Estructura de datos interna (tabla hash, cache)?
|   |
|   No necesitas un hash criptografico.
|   Usa xxHash, MurmurHash, o hash() de Python.
|
+-- Deduplicacion de datos?
|   |
|   SHA-256 o BLAKE2b (necesitas resistencia a colisiones)
|
+-- Proof-of-work (como Bitcoin)?
|   |
|   SHA-256 (es el estandar de la industria)
```

La regla general: **SHA-256 para compatibilidad, SHA-3-256 para proyectos nuevos, BLAKE3 cuando la velocidad importa**. Y nunca, bajo ninguna circunstancia, uses un hash de proposito general para contrasenas.

### 1.4.2 Caso real: SHAttered -- la muerte de SHA-1

El 23 de febrero de 2017, un equipo liderado por Marc Stevens de CWI Amsterdam y Elie Bursztein de Google publico el primer ataque de colision practico contra SHA-1, llamado **SHAttered**.

El equipo genero dos archivos PDF visualmente diferentes que producen exactamente el mismo hash SHA-1. El ataque requirio:

- Mas de 9.2 quintillones (9.2 x 10^18) de evaluaciones SHA-1
- El equivalente a 6,500 anos de computo CPU y 100 anos de computo GPU
- Un costo aproximado de $110,000 USD en la nube de Google

Aunque suena a mucho, es **100,000 veces mas rapido** que un ataque de fuerza bruta. Y el costo es trivial para una corporacion, un gobierno, o un grupo criminal organizado.

El impacto fue masivo:

- **Certificados TLS**: las autoridades certificadoras habian dejado de emitir certificados SHA-1, pero muchos aun estaban en uso.
- **Git**: cada objeto en Git se identifica con SHA-1. Aunque el ataque no compromete la seguridad de Git de manera inmediata (porque Git verifica mas que solo el hash), el proyecto inicio la migracion a SHA-256.
- **Firmas de codigo**: software firmado con SHA-1 ya no puede considerarse autenticamente verificado.

La leccion es dolorosa pero simple: **cuando los criptografos dicen que un algoritmo esta depreciado, la migracion es urgente, no "cuando tengamos tiempo"**.

### 1.4.3 Caso real: Flame y la falsificacion de certificados con MD5

En 2012, investigadores de seguridad descubrieron **Flame**, un malware extremadamente sofisticado que se habia propagado silenciosamente por redes en Medio Oriente. Lo que hizo unico a Flame fue su metodo de distribucion: se propagaba a traves de **Windows Update**.

Como lo logro? Los atacantes explotaron una colision en MD5 para falsificar un certificado de Microsoft. El certificado falso parecia legitimo para Windows, que acepto y ejecuto el malware como si fuera una actualizacion oficial de Microsoft.

El ataque funcionaba asi:

1. Microsoft usaba un servicio de licencias que firmaba certificados con MD5
2. Los atacantes generaron un certificado falso que colisionaba con uno legitimo
3. Windows Update confiaba en ese certificado y ejecutaba el malware

Un hash roto en **una sola parte** de la cadena de confianza comprometio todo el sistema de actualizaciones de uno de los sistemas operativos mas usados del mundo.

---

## 1.5 Usos reales de los hashes

Antes de pasar al ejercicio, veamos tres usos cotidianos donde los hashes trabajan silenciosamente:

### Verificacion de integridad de descargas

Cuando descargas un ISO de Linux o un binario de un proyecto open source, frecuentemente encuentras junto al archivo una linea como:

```
sha256sum: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

El proceso es simple: descargas el archivo, calculas su hash localmente, y comparas con el hash publicado. Si coinciden, el archivo no fue alterado durante la descarga (o por un atacante que comprometio el servidor de distribucion).

```python
from hashlib import sha256

def verificar_descarga(ruta_archivo, hash_esperado):
    """Verifica que un archivo descargado no fue alterado."""
    h = sha256()
    with open(ruta_archivo, "rb") as f:
        while bloque := f.read(8192):
            h.update(bloque)

    hash_calculado = h.hexdigest()

    if hash_calculado == hash_esperado:
        print(f"VERIFICADO: El archivo es integro.")
        return True
    else:
        print(f"ALERTA: El archivo fue modificado!")
        print(f"  Esperado:  {hash_esperado}")
        print(f"  Calculado: {hash_calculado}")
        return False
```

### Deduplicacion de datos

Los sistemas de almacenamiento como ZFS, servicios en la nube y herramientas de respaldo usan hashes para detectar archivos duplicados. En lugar de comparar el contenido byte a byte (costoso para archivos grandes), comparan hashes:

```python
from hashlib import sha256
from pathlib import Path

def encontrar_duplicados(directorio):
    """Encuentra archivos duplicados en un directorio usando SHA-256."""
    hashes = {}  # hash -> lista de rutas

    for archivo in Path(directorio).rglob("*"):
        if archivo.is_file():
            h = sha256()
            with open(archivo, "rb") as f:
                while bloque := f.read(8192):
                    h.update(bloque)
            digest = h.hexdigest()

            if digest not in hashes:
                hashes[digest] = []
            hashes[digest].append(str(archivo))

    # Filtrar solo los que tienen duplicados
    return {h: rutas for h, rutas in hashes.items() if len(rutas) > 1}

# duplicados = encontrar_duplicados("/ruta/a/mi/directorio")
# for hash_val, archivos in duplicados.items():
#     print(f"Duplicados (hash: {hash_val[:16]}...):")
#     for archivo in archivos:
#         print(f"  {archivo}")
```

### Git: integridad de todo tu historial

Cada objeto en Git --commits, blobs (archivos), trees (directorios)-- se identifica con un hash de su contenido. Esto significa que todo el historial de tu repositorio esta encadenado por hashes: si cambias un solo byte en un commit antiguo, su hash cambia, lo que cambia el hash del commit que lo referencia, y asi sucesivamente en cascada hasta el HEAD actual.

```python
# Asi es como Git calcula el hash de un blob:
from hashlib import sha1  # Git aun usa SHA-1 (migrando a SHA-256)

contenido = b"print('hola mundo')\n"
header = f"blob {len(contenido)}\0".encode()
hash_git = sha1(header + contenido).hexdigest()
print(f"Hash de Git para este blob: {hash_git}")
```

---

## 1.6 Ejercicio integrador: verificador de integridad de archivos

Ahora vamos a construir algo real. Un programa que monitorea un directorio y detecta si algun archivo fue modificado, creado o eliminado.

```python
#!/usr/bin/env python3
"""
integrity_checker.py - Verificador de integridad de archivos

Uso:
  python integrity_checker.py crear /ruta/al/directorio
    -> Calcula hashes y crea un manifiesto

  python integrity_checker.py verificar /ruta/al/directorio
    -> Compara el estado actual contra el manifiesto y reporta cambios
"""

import sys
import json
import time
from hashlib import sha3_256
from pathlib import Path


def calcular_hash(ruta_archivo):
    """Calcula el SHA-3-256 de un archivo."""
    h = sha3_256()
    try:
        with open(ruta_archivo, "rb") as f:
            while bloque := f.read(8192):
                h.update(bloque)
        return h.hexdigest()
    except (PermissionError, OSError) as e:
        print(f"  Advertencia: no se pudo leer {ruta_archivo}: {e}")
        return None


def escanear_directorio(directorio):
    """Calcula hashes de todos los archivos en un directorio."""
    directorio = Path(directorio)
    if not directorio.is_dir():
        print(f"Error: {directorio} no es un directorio valido.")
        sys.exit(1)

    hashes = {}
    archivos = sorted(directorio.rglob("*"))

    for archivo in archivos:
        if archivo.is_file():
            ruta_relativa = str(archivo.relative_to(directorio))
            hash_valor = calcular_hash(archivo)
            if hash_valor:
                hashes[ruta_relativa] = hash_valor

    return hashes


def crear_manifiesto(directorio):
    """Escanea un directorio y guarda el manifiesto de hashes."""
    directorio = Path(directorio)
    ruta_manifiesto = directorio / ".integrity_manifest.json"

    print(f"Escaneando {directorio}...")
    hashes = escanear_directorio(directorio)

    # Excluir el propio manifiesto
    manifiesto_rel = ".integrity_manifest.json"
    hashes.pop(manifiesto_rel, None)

    manifiesto = {
        "version": 1,
        "algoritmo": "SHA3-256",
        "creado": time.strftime("%Y-%m-%d %H:%M:%S"),
        "directorio": str(directorio.resolve()),
        "archivos": hashes,
    }

    with open(ruta_manifiesto, "w") as f:
        json.dump(manifiesto, f, indent=2, ensure_ascii=False)

    print(f"Manifiesto creado: {ruta_manifiesto}")
    print(f"Archivos registrados: {len(hashes)}")


def verificar_integridad(directorio):
    """Compara el estado actual contra el manifiesto guardado."""
    directorio = Path(directorio)
    ruta_manifiesto = directorio / ".integrity_manifest.json"

    if not ruta_manifiesto.exists():
        print(f"Error: no existe manifiesto en {directorio}")
        print("Ejecuta primero: python integrity_checker.py crear <directorio>")
        sys.exit(1)

    with open(ruta_manifiesto) as f:
        manifiesto = json.load(f)

    hashes_guardados = manifiesto["archivos"]
    hashes_actuales = escanear_directorio(directorio)

    # Excluir el manifiesto de la comparacion
    hashes_actuales.pop(".integrity_manifest.json", None)

    archivos_guardados = set(hashes_guardados.keys())
    archivos_actuales = set(hashes_actuales.keys())

    # Detectar cambios
    nuevos = archivos_actuales - archivos_guardados
    eliminados = archivos_guardados - archivos_actuales
    comunes = archivos_guardados & archivos_actuales
    modificados = {
        a for a in comunes
        if hashes_guardados[a] != hashes_actuales[a]
    }
    sin_cambios = comunes - modificados

    # Reporte
    print(f"\n{'='*60}")
    print(f"REPORTE DE INTEGRIDAD")
    print(f"Directorio: {directorio.resolve()}")
    print(f"Manifiesto creado: {manifiesto['creado']}")
    print(f"Algoritmo: {manifiesto['algoritmo']}")
    print(f"{'='*60}\n")

    if modificados:
        print(f"[MODIFICADOS] {len(modificados)} archivo(s):")
        for a in sorted(modificados):
            print(f"  ! {a}")
            print(f"    Antes:  {hashes_guardados[a][:32]}...")
            print(f"    Ahora:  {hashes_actuales[a][:32]}...")

    if nuevos:
        print(f"\n[NUEVOS] {len(nuevos)} archivo(s):")
        for a in sorted(nuevos):
            print(f"  + {a}")

    if eliminados:
        print(f"\n[ELIMINADOS] {len(eliminados)} archivo(s):")
        for a in sorted(eliminados):
            print(f"  - {a}")

    if not (modificados or nuevos or eliminados):
        print("Todo en orden. Ningun archivo fue modificado.")

    print(f"\nResumen: {len(sin_cambios)} sin cambios, "
          f"{len(modificados)} modificados, "
          f"{len(nuevos)} nuevos, "
          f"{len(eliminados)} eliminados.")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("crear", "verificar"):
        print("Uso:")
        print("  python integrity_checker.py crear <directorio>")
        print("  python integrity_checker.py verificar <directorio>")
        sys.exit(1)

    comando = sys.argv[1]
    directorio = sys.argv[2]

    if comando == "crear":
        crear_manifiesto(directorio)
    else:
        verificar_integridad(directorio)
```

Para probarlo:

```bash
# Crea un directorio de prueba
mkdir -p /tmp/prueba_integridad
echo "archivo original" > /tmp/prueba_integridad/datos.txt
echo "otro archivo" > /tmp/prueba_integridad/config.ini

# Crea el manifiesto
python integrity_checker.py crear /tmp/prueba_integridad

# Modifica un archivo
echo "archivo modificado" > /tmp/prueba_integridad/datos.txt

# Agrega un archivo nuevo
echo "intruso" > /tmp/prueba_integridad/nuevo.txt

# Verifica
python integrity_checker.py verificar /tmp/prueba_integridad
```

La salida te mostrara exactamente que cambio, que es nuevo y que fue eliminado. Este es el mismo principio que usan herramientas como `sha256sum`, Tripwire, y AIDE para monitorear la integridad de sistemas en produccion.

---

## Takeaway del capitulo

Un hash criptografico tiene **tres garantias medibles**:

1. **Resistencia a preimagen**: no puedes encontrar la entrada a partir del hash.
2. **Resistencia a segunda preimagen**: no puedes encontrar otra entrada que produzca el mismo hash.
3. **Resistencia a colisiones**: no puedes encontrar ningun par de entradas con el mismo hash.

Cuando alguien te diga "usamos SHA-256", pregunta: *para que?* Un hash de proposito general no sirve para contrasenas. Un hash roto no sirve para nada. Y el hash mas seguro del mundo no te protege si lo usas mal.

La proxima vez que escribas `sha256()`, sabras exactamente que estas pidiendo y que garantias recibes a cambio.

---

**En el siguiente capitulo**, descubriremos las matematicas que hacen posible que estas garantias se sostengan. No necesitas un doctorado: con aritmetica modular, numeros primos y XOR entenderas el 90% de la criptografia practica.

---

### Referencias del capitulo

- [Aumasson, 2024] Aumasson, J.P. *Serious Cryptography*, 2nd Edition. No Starch Press.
- [Lazar, Chen y Zeldovich, 2014] Lazar, D., Chen, H., Wang, X., & Zeldovich, N. "Why does cryptographic software fail? A case study and open problems." MIT CSAIL.
- [NIST, 2015] National Institute of Standards and Technology. "FIPS 180-4: Secure Hash Standard" y "FIPS 202: SHA-3 Standard."
- [Schneier, 2012] Schneier, B. "Flame." *Schneier on Security Blog*.
- [Schneier, 2013] Schneier, B. "Cryptographic Blunders Revealed by Adobe's Password Leak." *Schneier on Security Blog*.
- [Stevens et al., 2017] Stevens, M. et al. "The first collision for full SHA-1." CWI Amsterdam y Google Research.
- [Krebs, 2016] Krebs, B. "As Scope of 2012 Breach Expands, LinkedIn to Again Reset Passwords for Some Users." *Krebs on Security*.
