# Capitulo 3: MD5, SHA-2 y la evolucion de los hashes

> "MD5 esta roto, pero no como crees. No es que deje de funcionar. Es que ya no puedes confiar en el."

---

En 2012, un malware llamado **Flame** se hizo pasar por una actualizacion oficial de Windows. La razon: MD5 llevaba anos roto, pero Microsoft seguia usandolo para firmar actualizaciones. El costo de no migrar a tiempo fue que un estado-nacion distribuyo software espia a traves del mecanismo de actualizacion mas confiable del mundo.

Este capitulo trata sobre como se construyen los hashes por dentro, por que algunos se rompen y otros no, y que significa realmente "roto" en el contexto de una funcion hash. Vamos a abrir la caja negra.

---

## 3.1 La construccion de Merkle-Damgard

### 3.1.1 Como se construye un hash de proposito general

En el Capitulo 1 usamos funciones hash como `sha256()` sin preguntarnos como funcionan internamente. Ahora es momento de mirar bajo el capo.

La gran mayoria de las funciones hash que usamos a diario --MD5, SHA-1, SHA-256, SHA-512-- comparten la misma arquitectura interna. Se llama **construccion de Merkle-Damgard**, nombrada en honor a Ralph Merkle e Ivan Damgard, quienes la describieron independientemente a finales de los anos 70 y principios de los 80 [Merkle, 1979; Damgard, 1989].

La idea es elegante en su simplicidad. Tienes un problema: necesitas procesar una entrada de tamano arbitrario y producir una salida de tamano fijo. La solucion: divide la entrada en bloques de tamano fijo y procesalos uno a la vez, acumulando el resultado en un **estado interno**.

El mecanismo funciona asi:

1. **Padding**: el mensaje se rellena hasta que su longitud sea multiplo del tamano de bloque del algoritmo (512 bits para MD5 y SHA-256, 1024 bits para SHA-512). El padding incluye la longitud original del mensaje codificada al final.

2. **Division en bloques**: el mensaje rellenado se divide en bloques de tamano fijo: M1, M2, ..., Mn.

3. **Valor inicial (IV)**: el algoritmo comienza con un valor inicial fijo y publico, especificado en el estandar.

4. **Compresion iterativa**: cada bloque se combina con el estado anterior a traves de una **funcion de compresion** f, que toma dos entradas de tamano fijo y produce una salida de tamano fijo.

5. **Finalizacion**: el resultado de la ultima iteracion es el hash final.

Veamoslo como diagrama:

```
Mensaje: "Criptografia aplicada para desarrolladores"
                    |
                    v
            [  Padding  ]
                    |
                    v
    +-------+-------+-------+-------+
    |  M1   |  M2   |  M3   |  M4   |
    +-------+-------+-------+-------+
        |       |       |       |
        v       v       v       v
IV --> [f] --> [f] --> [f] --> [f] --> Hash final
        ^       ^       ^       ^
        |       |       |       |
       M1      M2      M3      M4

Donde:
  IV  = Valor inicial (constante del algoritmo)
  f   = Funcion de compresion
  Mn  = Bloque n del mensaje (con padding)
```

Cada invocacion de la funcion de compresion toma el **estado anterior** (o el IV en la primera iteracion) y un bloque del mensaje, y produce un nuevo estado. El estado final es el hash.

Lo que hace solida a esta construccion es un teorema fundamental: **si la funcion de compresion f es resistente a colisiones, entonces el hash completo tambien lo es** [Merkle, 1979]. Esto significa que el problema de disenar un buen hash se reduce a disenar una buena funcion de compresion.

### 3.1.2 El padding de Merkle-Damgard

El padding no es un detalle trivial. Es una parte critica de la seguridad. El esquema de padding compatible con Merkle-Damgard (llamado "MD-compliant padding") debe cumplir tres condiciones [Bellare y Rogaway, 2006]:

1. El mensaje original debe ser un prefijo del mensaje rellenado
2. Mensajes de la misma longitud producen padding de la misma longitud
3. Mensajes de diferente longitud producen bloques finales diferentes

La tercera condicion es la que requiere incluir la longitud del mensaje en el padding. Para SHA-256, el padding funciona asi:

1. Agrega un bit `1` despues del ultimo bit del mensaje
2. Agrega tantos bits `0` como sea necesario para que la longitud total sea congruente con 448 mod 512
3. Agrega la longitud original del mensaje como un entero de 64 bits

Veamoslo en codigo:

```python
import struct

def padding_sha256(mensaje_bytes):
    """
    Calcula el padding SHA-256 para un mensaje.
    Retorna el mensaje completo con padding.
    """
    longitud_original = len(mensaje_bytes)
    longitud_bits = longitud_original * 8

    # Paso 1: agregar byte 0x80 (bit 1 seguido de 7 ceros)
    mensaje_bytes += b'\x80'

    # Paso 2: agregar ceros hasta que longitud mod 64 == 56 (448 bits mod 512)
    while len(mensaje_bytes) % 64 != 56:
        mensaje_bytes += b'\x00'

    # Paso 3: agregar la longitud original en bits como entero de 64 bits big-endian
    mensaje_bytes += struct.pack('>Q', longitud_bits)

    return mensaje_bytes


# Ejemplo
mensaje = b"abc"
con_padding = padding_sha256(bytearray(mensaje))

print(f"Mensaje original: {mensaje}")
print(f"Longitud original: {len(mensaje)} bytes")
print(f"Con padding: {len(con_padding)} bytes ({len(con_padding) * 8} bits)")
print(f"Padding hex: {con_padding.hex()}")
```

```
Mensaje original: b'abc'
Longitud original: 3 bytes
Con padding: 64 bytes (512 bits)
Padding hex: 6162638000000000000000000000000000000000000000000000000000000000
             0000000000000000000000000000000000000000000000000000000000000018
```

Observa el `80` despues de `616263` (que es "abc" en ASCII), seguido de muchos ceros, y al final `18` (que es 24 en hexadecimal, la longitud en bits del mensaje original). Todo el bloque tiene exactamente 512 bits.

### 3.1.3 La funcion de compresion en la practica

La funcion de compresion es donde ocurre la magia criptografica. En SHA-256, por ejemplo, la funcion de compresion trabaja con:

- Un estado de 256 bits (ocho registros de 32 bits: a, b, c, d, e, f, g, h)
- Un bloque de mensaje de 512 bits
- 64 rondas de operaciones que mezclan el estado con partes del bloque

Cada ronda aplica operaciones bit a bit (AND, OR, XOR, rotaciones, desplazamientos) y sumas modulares que producen el efecto avalancha que vimos en el Capitulo 1. Despues de las 64 rondas, el nuevo estado se suma al estado anterior (operacion feedforward).

No necesitas memorizar los detalles internos para usar SHA-256 correctamente. Pero necesitas entender la estructura de Merkle-Damgard para comprender la vulnerabilidad que veremos a continuacion.

---

## 3.2 Que significa realmente "roto" para un hash

Antes de hablar de ataques, aclaremos un malentendido comun. Cuando un criptografo dice que un hash esta "roto", **no** significa que deja de funcionar. No significa que `md5("hola")` produce un resultado diferente cada vez. El hash sigue siendo determinista, sigue produciendo salidas de tamano fijo, sigue siendo irreversible en la practica.

"Roto" significa que alguna de las tres resistencias formales --preimagen, segunda preimagen o colision-- ha sido comprometida. Mas especificamente, significa que alguien encontro un ataque que requiere **significativamente menos esfuerzo** que el ataque de fuerza bruta teorico.

Para un hash de 128 bits como MD5:

| Propiedad | Esfuerzo ideal | Esfuerzo real (MD5) | Estado |
|-----------|---------------|---------------------|--------|
| Resistencia a preimagen | 2^128 | ~2^123 (leve debilidad) | Preocupante pero no practico |
| Resistencia a 2da preimagen | 2^128 | No roto practicamente | Debilitado en teoria |
| Resistencia a colisiones | 2^64 | Segundos en una laptop | **Completamente roto** |

La distincion importa. MD5 esta roto **para colisiones** pero no para preimagen. Esto significa que:

- **No puedes** (en la practica) tomar un hash MD5 y encontrar el mensaje original
- **Si puedes** crear dos mensajes diferentes que produzcan el mismo hash MD5

Esto tiene implicaciones enormes. Si un sistema usa MD5 para verificar que un documento no fue alterado (integridad), un atacante puede crear un documento malicioso que tenga el mismo hash que el documento legitimo. El sistema de verificacion dira "todo bien" cuando todo esta mal.

---

## 3.3 El ataque de extension de longitud

### 3.3.1 La debilidad estructural de Merkle-Damgard

La construccion de Merkle-Damgard tiene una propiedad que parece inofensiva pero resulta devastadora en ciertos contextos: **el hash final es exactamente el estado interno del algoritmo al terminar de procesar el mensaje**.

Piensa en lo que esto significa. Si conoces `SHA-256("mensaje")`, conoces el estado interno del algoritmo despues de procesar "mensaje". Y si conoces el estado interno, puedes **continuar** hasheando como si fueras el algoritmo original.

Formalmente: dado `H(M)` y la longitud de `M`, puedes calcular `H(M || padding || M')` para cualquier `M'` que elijas, **sin conocer M**.

Esto se llama **ataque de extension de longitud** (length extension attack), y afecta a MD5, SHA-1, SHA-256 y SHA-512 [Duong y Rizzo, 2009].

Donde `||` denota concatenacion y "padding" es el padding de Merkle-Damgard que el algoritmo agrego internamente a `M`.

### 3.3.2 Por que esto es un problema real

Imagina un sistema de autenticacion de API que funciona asi:

```
firma = SHA-256(secreto || mensaje)
```

El servidor tiene un secreto que el cliente no conoce. El cliente envia un mensaje y la firma correspondiente. El servidor calcula la firma esperada y la compara con la recibida.

Parece seguro: sin el secreto, el cliente no puede generar firmas validas. Pero con el ataque de extension de longitud, un atacante que intercepta una firma valida puede:

1. Tomar la firma `SHA-256(secreto || mensaje_original)`
2. Usarla como estado interno del algoritmo
3. Continuar hasheando datos adicionales
4. Producir `SHA-256(secreto || mensaje_original || padding || datos_maliciosos)`

El resultado es una firma valida para un mensaje que el atacante modifico, **sin conocer el secreto**. Si el mensaje original era `amount=100&to=alice`, el atacante podria extenderlo a `amount=100&to=alice[padding]&amount=1000000&to=eve`, y la firma seria valida.

### 3.3.3 El ataque paso a paso con codigo Python

Vamos a demostrar el ataque. Primero, implementaremos una version simplificada que muestra el concepto, y luego usaremos la herramienta `hlextend` para hacer un ataque real contra SHA-256.

**Paso 1: El servidor vulnerable**

```python
from hashlib import sha256
import hmac

# El secreto del servidor (el atacante NO lo conoce)
SECRETO = b"mi_llave_secreta_2024"

def firmar_mensaje(mensaje: bytes) -> str:
    """
    Firma un mensaje usando SHA-256(secreto || mensaje).
    VULNERABLE a extension de longitud.
    """
    return sha256(SECRETO + mensaje).hexdigest()


def verificar_firma(mensaje: bytes, firma: str) -> bool:
    """Verifica que la firma corresponda al mensaje."""
    firma_esperada = sha256(SECRETO + mensaje).hexdigest()
    return firma == firma_esperada


# El usuario legitimo obtiene una firma
mensaje_original = b"amount=100&to=alice"
firma_original = firmar_mensaje(mensaje_original)

print(f"Mensaje: {mensaje_original}")
print(f"Firma:   {firma_original}")
print(f"Valida?  {verificar_firma(mensaje_original, firma_original)}")
```

**Paso 2: El atacante extiende el mensaje**

Para hacer el ataque completo necesitamos reconstruir el estado interno de SHA-256 a partir del hash conocido. Los registros internos de SHA-256 son ocho enteros de 32 bits, y el hash de 256 bits es exactamente esos ocho enteros concatenados:

```python
import struct

def hash_a_estado(hash_hex: str):
    """
    Convierte un hash SHA-256 hexadecimal a los 8 registros
    internos de 32 bits. Esto es posible porque el hash final
    ES el estado interno.
    """
    hash_bytes = bytes.fromhex(hash_hex)
    # SHA-256 usa 8 registros de 32 bits, big-endian
    return struct.unpack('>8I', hash_bytes)


def estado_a_hash(estado: tuple) -> str:
    """Convierte los 8 registros de vuelta a hash hex."""
    return struct.pack('>8I', *estado).hex()


# Demostracion: el hash es equivalente al estado
mensaje = b"test"
h = sha256(mensaje).hexdigest()
estado = hash_a_estado(h)
reconstruido = estado_a_hash(estado)

print(f"Hash original:    {h}")
print(f"Estado (8 x u32): {[hex(r) for r in estado]}")
print(f"Reconstruido:     {reconstruido}")
print(f"Coinciden: {h == reconstruido}")
```

```
Hash original:    9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08
Estado (8 x u32): ['0x9f86d081', '0x884c7d65', '0x9a2feaa0', '0xc55ad015',
                    '0xa3bf4f1b', '0x2b0b822c', '0xd15d6c15', '0xb0f00a08']
Reconstruido:     9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08
Coinciden: True
```

**Paso 3: Construir el padding del mensaje original**

El atacante necesita saber (o adivinar) la longitud del secreto para calcular el padding correcto:

```python
def calcular_padding_md(longitud_total_bytes: int) -> bytes:
    """
    Calcula el padding de Merkle-Damgard para SHA-256.
    longitud_total_bytes = len(secreto) + len(mensaje_original)
    """
    longitud_bits = longitud_total_bytes * 8

    # Byte 0x80
    padding = b'\x80'

    # Ceros hasta que (longitud_total + padding) mod 64 == 56
    padding_len = (56 - (longitud_total_bytes + 1) % 64) % 64
    padding += b'\x00' * padding_len

    # Longitud original en bits, 64 bits big-endian
    padding += struct.pack('>Q', longitud_bits)

    return padding


# Si el atacante sabe que el secreto tiene 21 bytes ("mi_llave_secreta_2024")
longitud_secreto = 21  # El atacante puede probar diferentes valores
longitud_total = longitud_secreto + len(mensaje_original)

padding = calcular_padding_md(longitud_total)
print(f"Padding calculado ({len(padding)} bytes): {padding.hex()}")
```

**Paso 4: El ataque completo**

Para completar el ataque, necesitamos una implementacion de SHA-256 que nos permita inyectar un estado inicial personalizado. La libreria `hashlib` de Python no expone esta funcionalidad directamente, pero podemos usar la libreria `hlextend`:

```python
# pip install hlextend
# Esta libreria implementa el ataque de extension de longitud
# para MD5, SHA-1, SHA-256 y SHA-512

import hlextend

# Datos que el atacante conoce
firma_interceptada = firma_original  # El hash SHA-256(secreto || mensaje)
mensaje_conocido = b"amount=100&to=alice"
longitud_secreto = 21  # Puede ser adivinada o probada por fuerza bruta

# Datos que el atacante quiere agregar
datos_maliciosos = b"&amount=999999&to=eve"

# Ejecutar el ataque
sha = hlextend.new('sha256')
nuevo_hash = sha.extend(
    datos_maliciosos,       # Lo que queremos agregar
    mensaje_conocido,       # El mensaje original conocido
    longitud_secreto,       # Longitud del secreto (adivinada)
    firma_interceptada      # El hash original interceptado
)
nuevo_mensaje = sha.payload  # El mensaje extendido (con padding incluido)

print(f"Hash forjado:    {nuevo_hash}")
print(f"Mensaje extendido (hex): {nuevo_mensaje.hex()}")
print()

# Verificacion: el servidor acepta la firma forjada?
valida = verificar_firma(nuevo_mensaje, nuevo_hash)
print(f"El servidor acepta la firma forjada? {valida}")
```

Si todo funciona correctamente, el servidor aceptara la firma como valida, a pesar de que el atacante nunca conocio el secreto. El mensaje extendido contendra bytes de padding entre el mensaje original y los datos maliciosos, pero en muchos protocolos de la vida real estos bytes son ignorados o tolerados.

### 3.3.4 La solucion: HMAC

La forma correcta de autenticar mensajes con un secreto no es `SHA-256(secreto || mensaje)`, sino **HMAC** (Hash-based Message Authentication Code):

```python
import hmac
from hashlib import sha256

def firmar_mensaje_seguro(mensaje: bytes, secreto: bytes) -> str:
    """
    Firma un mensaje usando HMAC-SHA-256.
    INMUNE a extension de longitud.
    """
    return hmac.new(secreto, mensaje, sha256).hexdigest()


def verificar_firma_segura(mensaje: bytes, firma: str, secreto: bytes) -> bool:
    """Verifica la firma usando comparacion de tiempo constante."""
    firma_esperada = hmac.new(secreto, mensaje, sha256).hexdigest()
    return hmac.compare_digest(firma, firma_esperada)


# HMAC calcula: H((K xor opad) || H((K xor ipad) || mensaje))
# La doble aplicacion del hash con padding interno y externo
# hace imposible el ataque de extension de longitud
```

HMAC funciona aplicando el hash dos veces con paddings diferentes (llamados `ipad` y `opad`), lo que rompe la relacion directa entre el hash final y el estado interno del ultimo bloque procesado. Profundizaremos en HMAC en el Capitulo 11, pero la regla es clara: **nunca uses hash(secreto || mensaje) para autenticacion. Usa HMAC.**

---

## 3.4 MD5: autopsia de un hash roto

### 3.4.1 Diseno y operacion

MD5 (Message Digest 5) fue disenado por **Ron Rivest** en 1991 como sucesor de MD4 [Rivest, 1992]. Produce un hash de 128 bits (32 caracteres hexadecimales) y procesa bloques de 512 bits. Su funcion de compresion ejecuta 4 rondas de 16 operaciones cada una, para un total de 64 pasos.

En su momento, MD5 era considerado rapido y seguro. Se convirtio en el hash mas desplegado del mundo, usado en todo, desde verificacion de descargas hasta firmas de certificados digitales.

```python
from hashlib import md5

# MD5 todavia funciona -- pero no confies en el
h = md5(b"Criptografia aplicada").hexdigest()
print(f"MD5: {h}")
print(f"Longitud: {len(h)} caracteres hex = {len(h)*4} bits")
```

```
MD5: a1d8d7f26349cf7edbcf22a5f7c7a4e0
Longitud: 32 caracteres hex = 128 bits
```

### 3.4.2 Cronologia de la caida

La historia de como MD5 paso de "estandar de la industria" a "nunca usar" es una leccion sobre la velocidad con la que la seguridad criptografica puede deteriorarse:

**1996**: Hans Dobbertin encuentra pseudo-colisiones en la funcion de compresion de MD5. Es una senal de alarma, pero no un ataque practico contra el hash completo.

**2004**: Xiaoyun Wang y sus colegas presentan el primer ataque de colision practico contra MD5 completo. Pueden generar colisiones en aproximadamente una hora de computo [Wang y Yu, 2005]. La comunidad criptografica reacciona con alarma, pero la industria se mueve lentamente.

**2006**: Vlastimil Klima publica un metodo para encontrar colisiones MD5 en menos de un minuto usando una computadora portatil comun [Klima, 2006].

**2008**: Alexander Sotirov y un equipo de investigadores crean un **certificado de autoridad certificadora (CA) falso** usando una colision MD5. Demuestran que pueden crear certificados TLS falsos que los navegadores aceptan como legitimos [Sotirov et al., 2008]. Es la primera demostracion de impacto catastrofico en el mundo real.

**2012**: Se descubre **Flame**, el malware mas sofisticado de su epoca, que usa colisiones MD5 para falsificar certificados de Microsoft.

Hoy, generar una colision MD5 toma **menos de un segundo** en cualquier computadora moderna:

```python
# Para demostrar lo rapido que es MD5 (NO para seguridad):
from hashlib import md5
import time

inicio = time.time()
# hashcat puede probar ~60 mil millones de hashes MD5/segundo en una GPU moderna
# Aqui simplemente mostramos la velocidad de hasheo
for i in range(1_000_000):
    md5(str(i).encode()).digest()
duracion = time.time() - inicio

print(f"1,000,000 hashes MD5 en {duracion:.2f}s")
print(f"Velocidad: {1_000_000/duracion:,.0f} hashes/segundo")
print(f"Una GPU moderna con hashcat: ~60,000,000,000 hashes/segundo")
```

### 3.4.3 Caso real: Flame y los certificados de Microsoft

En mayo de 2012, investigadores de seguridad en Kaspersky Lab descubrieron **Flame** (tambien conocido como Flamer o sKyWIper), un malware de espionaje que habia estado operando silenciosamente en redes de Medio Oriente, principalmente en Iran. Lo que hizo a Flame extraordinario no fue solo su complejidad --con mas de 20 MB de codigo, era el malware mas grande conocido hasta entonces-- sino su metodo de distribucion.

Flame se propagaba a traves de **Windows Update**.

El ataque funcionaba de la siguiente manera [Microsoft Security Response Center, 2012]:

1. **El punto debil**: Microsoft mantenia un servicio de licenciamiento de Terminal Services que firmaba certificados usando MD5. Estos certificados estaban encadenados a la autoridad raiz de Microsoft ("Microsoft Root Authority").

2. **La prediccion**: Los atacantes descubrieron que los numeros de serie y las fechas de validez de los certificados eran predecibles. Esto les permitio planificar una colision de prefijo elegido (chosen-prefix collision) contra MD5.

3. **La colision**: Usando una variante **completamente nueva** del ataque de colision de prefijo elegido --diferente de las tecnicas publicadas en la literatura academica-- los atacantes generaron un certificado falso cuyo hash MD5 coincidia con un certificado legitimo firmado por la CA de Microsoft.

4. **La infiltracion**: El certificado falso permitia firmar codigo que Windows aceptaba como una actualizacion genuina de Microsoft. El malware se distribuyia como si fuera una actualizacion oficial, incluso en Windows Vista y versiones posteriores.

5. **El impacto**: Computadoras en Iran, Libano, Sudan y otros paises de Medio Oriente ejecutaron software espia creyendo que era una actualizacion de seguridad de Microsoft.

Lo mas inquietante del analisis posterior fue la conclusion de los criptografos: la variante del ataque de colision usada en Flame era desconocida para la comunidad academica. Esto significaba que los atacantes --presumiblemente un estado-nacion-- tenian **capacidades criptoanaliticas de primer nivel mundial** [Sotirov, 2012].

La leccion es doblemente dolorosa:

1. Un hash roto en **una sola parte** de la cadena de confianza comprometio todo el sistema de actualizaciones de Windows.
2. Las vulnerabilidades conocidas desde 2004 no fueron corregidas hasta que fue demasiado tarde.

```python
# [PELIGRO] Detectar uso de MD5 en tu codigo Python
# Busca estas importaciones en tu codebase:

patrones_peligrosos = [
    "from hashlib import md5",
    "hashlib.md5(",
    "MD5.new(",              # PyCryptodome
    "md5(",
    "algorithm='md5'",
    "digest: md5",
]

# Si encuentras alguno de estos patrones, migra a SHA-256 o SHA-3
# a menos que sea para compatibilidad con un sistema legacy
# que no controlas y no tiene uso de seguridad
```

### 3.4.4 Por que MD5 sigue en uso

A pesar de estar roto desde hace mas de dos decadas, MD5 sigue apareciendo en codebases de produccion. Las razones mas comunes son:

- **Checksums no criptograficos**: algunos sistemas usan MD5 como checksum rapido para detectar corrupcion accidental (no maliciosa) de datos. Esto es *tecnicamente* aceptable si no hay un adversario, pero es una mala practica porque crea deuda tecnica y habitos peligrosos.

- **Compatibilidad con sistemas legacy**: protocolos antiguos, APIs de terceros y formatos de archivo que especifican MD5.

- **Ignorancia o inercia**: simplemente nadie se tomo el tiempo de migrar.

La recomendacion es simple: **elimina MD5 de tu codigo**. Si necesitas un checksum rapido no criptografico, usa CRC32 o xxHash. Si necesitas un hash criptografico, usa SHA-256 o SHA-3. No hay un caso de uso moderno donde MD5 sea la mejor opcion.

---

## 3.5 SHA-1: la depreciacion mas lenta de la historia

### 3.5.1 De SHA-0 a SHA-1

SHA-1 fue disenado por la NSA y publicado por el NIST en 1995 como sucesor de SHA-0 (publicado en 1993 y retirado rapidamente despues de que se descubriera una debilidad interna). SHA-1 produce un hash de 160 bits y usa la construccion de Merkle-Damgard con bloques de 512 bits.

Durante 15 anos, SHA-1 fue el hash dominante en internet. Lo usaban:

- Certificados TLS/SSL
- Firmas de codigo (incluyendo actualizaciones de Windows y macOS)
- Git (para identificar commits, blobs y trees)
- PGP/GPG para firmas de email
- IPsec y otros protocolos VPN

### 3.5.2 SHAttered: el clavo final

Las senales de alarma empezaron en 2005, cuando Wang, Yin y Yu publicaron ataques teoricos que reducian la complejidad de encontrar colisiones SHA-1 de 2^80 (el nivel ideal) a 2^69 [Wang, Yin y Yu, 2005]. Pero la colision practica tardo mas de una decada en llegar.

El 23 de febrero de 2017, un equipo liderado por **Marc Stevens** de CWI Amsterdam y **Elie Bursztein** de Google publico **SHAttered**: la primera colision practica contra SHA-1 completo [Stevens et al., 2017].

El equipo genero dos archivos PDF visualmente diferentes --uno con un fondo azul y otro con un fondo rojo-- que producen exactamente el mismo hash SHA-1. El ataque requirio:

- Mas de **9.2 quintillones** (9.2 x 10^18) de evaluaciones SHA-1
- El equivalente a **6,500 anos de CPU** y **110 anos de GPU**
- Un costo aproximado de **$110,000 USD** en computo en la nube de Google
- El uso de clusters heterogeneos de GPU (K20, K40, K80) distribuidos en 8 locaciones fisicas

La complejidad fue de aproximadamente **2^63.1 evaluaciones SHA-1**, lo que es 100,000 veces mas rapido que un ataque de fuerza bruta generico, pero mucho mas caro que los ataques contra MD5.

Puedes verificarlo tu mismo. Los dos PDFs estan disponibles en shattered.io:

```python
from hashlib import sha1, sha256

# Si descargas los PDFs de shattered.io:
# wget https://shattered.io/static/shattered-1.pdf
# wget https://shattered.io/static/shattered-2.pdf

# Los SHA-1 son identicos (colision!)
# sha1_1 = sha1(open("shattered-1.pdf", "rb").read()).hexdigest()
# sha1_2 = sha1(open("shattered-2.pdf", "rb").read()).hexdigest()
# assert sha1_1 == sha1_2  # True!

# Pero los SHA-256 son diferentes (SHA-256 no esta roto)
# sha256_1 = sha256(open("shattered-1.pdf", "rb").read()).hexdigest()
# sha256_2 = sha256(open("shattered-2.pdf", "rb").read()).hexdigest()
# assert sha256_1 != sha256_2  # True!

# Este es el hash SHA-1 compartido por ambos PDFs:
print("SHA-1 de ambos PDFs: 38762cf7f55934b34d179ae6a4c80cadccbb7f0a")
```

### 3.5.3 La leccion de la depreciacion gradual

La migracion fuera de SHA-1 es un caso de estudio sobre lo dificil que es abandonar tecnologia obsoleta:

- **2005**: ataques teoricos publicados. El NIST recomienda migrar.
- **2011**: NIST deprecia formalmente SHA-1 para firmas digitales.
- **2014**: Google Chrome empieza a marcar certificados SHA-1 como inseguros.
- **2016**: las autoridades certificadoras dejan de emitir certificados SHA-1.
- **2017**: SHAttered demuestra la colision practica.
- **2020**: Git comienza la migracion a SHA-256 (aun en progreso).
- **2026**: Git todavia soporta SHA-1 por compatibilidad, aunque SHA-256 esta disponible.

Pasaron **21 anos** desde los primeros ataques teoricos hasta que los sistemas mas grandes completaron (o estan completando) la migracion. Es como cambiar las tuberias de una casa mientras vives en ella: no puedes cortar el agua, pero tampoco puedes seguir usando tuberias con fugas.

La leccion: **cuando los criptografos dicen "migra", la ventana de tiempo es mas corta de lo que crees**. No esperes a que alguien demuestre un ataque practico contra tu sistema.

---

## 3.6 SHA-2: los caballos de batalla actuales

### 3.6.1 Familia SHA-2: variantes y tamanos

SHA-2 es una familia de funciones hash disenada por la NSA y estandarizada por el NIST en 2001 (FIPS 180-2, actualizado en FIPS 180-4 en 2015). A pesar de compartir la construccion Merkle-Damgard con SHA-1, SHA-2 introdujo mejoras significativas en la funcion de compresion que lo hacen mucho mas resistente a los ataques que derribaron a sus predecesores.

La familia incluye varias variantes:

```
| Variante    | Salida  | Bloque   | Registros | Seguridad contra  |
|             | (bits)  | (bits)   | internos  | colisiones (bits) |
|-------------|---------|----------|-----------|-------------------|
| SHA-224     | 224     | 512      | 8 x 32    | 112               |
| SHA-256     | 256     | 512      | 8 x 32    | 128               |
| SHA-384     | 384     | 1024     | 8 x 64    | 192               |
| SHA-512     | 512     | 1024     | 8 x 64    | 256               |
| SHA-512/224 | 224     | 1024     | 8 x 64    | 112               |
| SHA-512/256 | 256     | 1024     | 8 x 64    | 128               |
```

Las variantes SHA-384 y SHA-512/256 son especiales: al ser versiones **truncadas** de SHA-512, son inmunes al ataque de extension de longitud. El hash publicado no contiene el estado interno completo, asi que un atacante no puede reconstruirlo.

SHA-256 y SHA-512 son las variantes mas usadas. SHA-512 es, sorprendentemente, mas rapido que SHA-256 en procesadores de 64 bits porque sus registros internos son de 64 bits.

### 3.6.2 Por que SHA-2 sigue siendo seguro

A pesar de usar la misma construccion Merkle-Damgard que MD5 y SHA-1, SHA-2 no ha sido comprometido. Las razones son:

1. **Funcion de compresion mas robusta**: SHA-256 usa 64 rondas (contra 80 de SHA-1, pero con operaciones mas complejas y un diseno de mensaje expandido que resiste los ataques diferenciales que funcionaron contra SHA-1).

2. **Margen de seguridad amplio**: los mejores ataques contra SHA-256 reducida llegan a 46 de 64 rondas [Aoki et al., 2009]. Quedan 18 rondas de margen.

3. **Mayor tamano de salida**: 256 bits proporcionan 128 bits de seguridad contra colisiones, lo que requiere 2^128 operaciones --un numero que esta fuera del alcance de cualquier tecnologia concebible hoy.

4. **Dos decadas de criptoanalisis intensivo**: miles de investigadores han intentado romper SHA-2 sin exito practico.

### 3.6.3 SHA-256 en la practica

SHA-256 es la funcion hash mas desplegada del mundo. Veamos como usarla correctamente para diferentes escenarios:

**Hash de archivos grandes (lectura por bloques)**

```python
import hashlib

def sha256_archivo(ruta, tamano_bloque=65536):
    """
    Calcula SHA-256 de un archivo grande sin cargarlo
    completamente en memoria.
    """
    h = hashlib.sha256()
    with open(ruta, 'rb') as f:
        while bloque := f.read(tamano_bloque):
            h.update(bloque)
    return h.hexdigest()


# Ejemplo de uso
# hash_resultado = sha256_archivo("/ruta/a/archivo-grande.iso")
# print(f"SHA-256: {hash_resultado}")
```

**Hash de multiples campos con separacion segura**

```python
from hashlib import sha256

def hash_campos(*campos):
    """
    Hashea multiples campos de forma segura, evitando
    ambiguedades de concatenacion.

    Sin separacion: hash("ab" + "cd") == hash("abc" + "d")
    Con separacion: cada campo se prefija con su longitud.
    """
    h = sha256()
    for campo in campos:
        dato = campo.encode() if isinstance(campo, str) else campo
        # Prefijo de longitud de 4 bytes (hasta 4 GB por campo)
        h.update(len(dato).to_bytes(4, 'big'))
        h.update(dato)
    return h.hexdigest()


# Estos producen hashes diferentes, como debe ser
print(hash_campos("ab", "cd"))
print(hash_campos("abc", "d"))
print(hash_campos("abcd"))
```

**Comparacion de rendimiento de la familia SHA-2**

```python
import hashlib
import time

def benchmark_hash(nombre, datos, repeticiones=10000):
    """Mide el rendimiento de una funcion hash."""
    h_func = getattr(hashlib, nombre)
    inicio = time.time()
    for _ in range(repeticiones):
        h_func(datos).digest()
    duracion = time.time() - inicio
    velocidad_mb = (len(datos) * repeticiones) / (1024 * 1024 * duracion)
    print(f"{nombre:>12}: {duracion:.3f}s ({velocidad_mb:.1f} MB/s)")
    return duracion


# Datos de prueba: 1 MB
datos = b"x" * (1024 * 1024)

print("Benchmark de la familia SHA-2 (1 MB, 10,000 iteraciones):")
print("-" * 55)
benchmark_hash("sha224", datos)
benchmark_hash("sha256", datos)
benchmark_hash("sha384", datos)
benchmark_hash("sha512", datos)
print()
print("Nota: SHA-384 y SHA-512 son mas rapidos en CPUs de 64 bits")
print("porque usan registros de 64 bits internamente.")
```

### 3.6.4 Caso real: Bitcoin y SHA-256

Bitcoin es probablemente el uso mas visible de SHA-256 en el mundo. El mecanismo de **Proof of Work** de Bitcoin consiste en encontrar un valor (llamado **nonce**) tal que el doble hash SHA-256 del encabezado del bloque empiece con un numero determinado de ceros en binario:

```python
from hashlib import sha256
import struct
import time

def doble_sha256(datos):
    """Bitcoin usa SHA-256 aplicado dos veces."""
    return sha256(sha256(datos).digest()).digest()


def minar_bloque_simple(datos_bloque, dificultad_ceros=20):
    """
    Simulacion simplificada de minado Bitcoin.
    Busca un nonce tal que el hash empiece con N bits en cero.
    """
    objetivo = 2 ** (256 - dificultad_ceros)
    nonce = 0
    inicio = time.time()

    while True:
        # Concatenar datos del bloque con el nonce
        intento = datos_bloque + struct.pack('<I', nonce)
        h = doble_sha256(intento)

        # Interpretar el hash como un numero
        valor = int.from_bytes(h, 'big')

        if valor < objetivo:
            duracion = time.time() - inicio
            print(f"Bloque minado!")
            print(f"  Nonce: {nonce:,}")
            print(f"  Hash: {h.hex()}")
            print(f"  Intentos: {nonce + 1:,}")
            print(f"  Tiempo: {duracion:.2f}s")
            print(f"  Velocidad: {(nonce + 1)/duracion:,.0f} hashes/s")
            return nonce

        nonce += 1
        if nonce % 1_000_000 == 0:
            print(f"  Intentos: {nonce:,}...")


# Simulacion con dificultad baja (20 bits de ceros)
# La red real de Bitcoin requiere ~80+ bits de ceros
print("Minando un bloque con dificultad 20 (20 bits de ceros)...")
print("(La red Bitcoin real requiere ~80+ bits)")
minar_bloque_simple(b"bloque_de_prueba_2024", dificultad_ceros=20)
```

Bitcoin eligio SHA-256 por varias razones:

1. **Seguridad probada**: en 2008, cuando Satoshi Nakamoto diseno Bitcoin, SHA-256 ya tenia 7 anos de criptoanalisis sin vulnerabilidades.
2. **Amplia disponibilidad**: SHA-256 estaba implementado en practicamente todas las plataformas.
3. **Doble aplicacion**: Bitcoin aplica SHA-256 dos veces (`SHA-256(SHA-256(x))`), lo que protege contra el ataque de extension de longitud.

### 3.6.5 Cuando usar SHA-2 y cuando no

**Usa SHA-2 (SHA-256 o SHA-512) cuando:**

- Necesitas compatibilidad con sistemas existentes (la mayoria del mundo usa SHA-256)
- Cumplimiento regulatorio requiere FIPS 180-4
- Estas integrando con protocolos que especifican SHA-256 (TLS, Bitcoin, etc.)
- Necesitas un hash probado con mas de dos decadas de criptoanalisis

**No uses SHA-2 cuando:**

- Necesitas hashear contrasenas (usa Argon2id, ver Capitulo 5)
- Construyes un esquema `hash(secreto || mensaje)` (usa HMAC en su lugar)
- El rendimiento es critico y no necesitas cumplimiento FIPS (considera BLAKE3)
- Estas disenando un sistema nuevo y quieres diversidad criptografica (considera SHA-3)

---

## 3.7 Ejercicio integrador: demuestra el ataque de extension de longitud

En este ejercicio construiras un sistema completo que demuestra el ataque de extension de longitud y su solucion.

```python
#!/usr/bin/env python3
"""
length_extension_demo.py

Demuestra el ataque de extension de longitud contra SHA-256
y como HMAC lo previene.

Requisitos: pip install hlextend

Uso: python length_extension_demo.py
"""

import hmac as hmac_module
import struct
import os
from hashlib import sha256

# ============================================================
# PARTE 1: Servidor vulnerable (SHA-256 ingenuo)
# ============================================================

class ServidorVulnerable:
    """
    Servidor que firma mensajes con SHA-256(secreto || mensaje).
    VULNERABLE a extension de longitud.
    """

    def __init__(self):
        # Secreto aleatorio -- el atacante NO lo conoce
        self.secreto = os.urandom(16)
        print(f"[Servidor] Secreto generado: {self.secreto.hex()}")
        print(f"[Servidor] Longitud del secreto: {len(self.secreto)} bytes")

    def firmar(self, mensaje: bytes) -> str:
        return sha256(self.secreto + mensaje).hexdigest()

    def verificar(self, mensaje: bytes, firma: str) -> bool:
        esperada = sha256(self.secreto + mensaje).hexdigest()
        return firma == esperada


# ============================================================
# PARTE 2: Servidor seguro (HMAC)
# ============================================================

class ServidorSeguro:
    """
    Servidor que firma mensajes con HMAC-SHA-256.
    INMUNE a extension de longitud.
    """

    def __init__(self):
        self.secreto = os.urandom(32)
        print(f"[Servidor Seguro] Secreto generado: {self.secreto.hex()}")

    def firmar(self, mensaje: bytes) -> str:
        return hmac_module.new(self.secreto, mensaje, sha256).hexdigest()

    def verificar(self, mensaje: bytes, firma: str) -> bool:
        esperada = hmac_module.new(self.secreto, mensaje, sha256).hexdigest()
        return hmac_module.compare_digest(firma, esperada)


# ============================================================
# PARTE 3: Ataque de extension de longitud (manual)
# ============================================================

def padding_sha256(longitud_total: int) -> bytes:
    """Calcula el padding SHA-256 para un mensaje de longitud dada."""
    longitud_bits = longitud_total * 8
    padding = b'\x80'
    padding_len = (56 - (longitud_total + 1) % 64) % 64
    padding += b'\x00' * padding_len
    padding += struct.pack('>Q', longitud_bits)
    return padding


def ataque_extension(firma_original: str, mensaje_original: bytes,
                     longitud_secreto: int, datos_extra: bytes) -> tuple:
    """
    Ejecuta el ataque de extension de longitud.

    Retorna (nuevo_mensaje, nueva_firma) que el servidor
    vulnerable aceptara como validos.

    NOTA: Requiere hlextend. Alternativamente, se puede
    implementar manualmente con una version modificada de SHA-256.
    """
    try:
        import hlextend
        sha = hlextend.new('sha256')
        nueva_firma = sha.extend(
            datos_extra,
            mensaje_original,
            longitud_secreto,
            firma_original
        )
        nuevo_mensaje = sha.payload
        return nuevo_mensaje, nueva_firma
    except ImportError:
        print("[!] Instala hlextend: pip install hlextend")
        print("[!] Calculando manualmente (solo padding)...")

        # Demostracion sin hlextend: solo mostramos la estructura
        longitud_total = longitud_secreto + len(mensaje_original)
        pad = padding_sha256(longitud_total)
        nuevo_mensaje = mensaje_original + pad + datos_extra
        print(f"[!] Mensaje extendido (hex): {nuevo_mensaje.hex()}")
        print(f"[!] Para completar el ataque, necesitas hlextend")
        return nuevo_mensaje, None


# ============================================================
# PARTE 4: Demostracion
# ============================================================

def main():
    print("=" * 70)
    print("DEMOSTRACION: Ataque de Extension de Longitud contra SHA-256")
    print("=" * 70)
    print()

    # --- Servidor vulnerable ---
    print("[1] Creando servidor vulnerable...")
    servidor = ServidorVulnerable()
    print()

    mensaje = b"user=alice&role=viewer"
    firma = servidor.firmar(mensaje)
    print(f"[2] Mensaje original: {mensaje}")
    print(f"    Firma: {firma}")
    print(f"    Valida? {servidor.verificar(mensaje, firma)}")
    print()

    # --- Ataque ---
    print("[3] Ejecutando ataque de extension de longitud...")
    datos_extra = b"&role=admin"

    # El atacante necesita adivinar la longitud del secreto
    # En la practica, se prueban valores comunes: 16, 20, 24, 32 bytes
    longitud_secreto = 16  # Coincide con os.urandom(16)

    nuevo_mensaje, nueva_firma = ataque_extension(
        firma, mensaje, longitud_secreto, datos_extra
    )

    if nueva_firma:
        print(f"    Mensaje extendido: {nuevo_mensaje}")
        print(f"    Firma forjada: {nueva_firma}")
        print(f"    Servidor acepta? {servidor.verificar(nuevo_mensaje, nueva_firma)}")
    print()

    # --- Servidor seguro ---
    print("[4] Creando servidor seguro (HMAC)...")
    servidor_seguro = ServidorSeguro()
    firma_hmac = servidor_seguro.firmar(mensaje)
    print(f"    Mensaje: {mensaje}")
    print(f"    Firma HMAC: {firma_hmac}")
    print(f"    Valida? {servidor_seguro.verificar(mensaje, firma_hmac)}")
    print()

    # El ataque de extension NO funciona contra HMAC
    print("[5] Intentando extension contra HMAC...")
    print("    (El ataque de extension no es aplicable a HMAC)")
    print("    HMAC calcula: H((K xor opad) || H((K xor ipad) || m))")
    print("    La doble aplicacion del hash rompe la relacion")
    print("    entre el hash final y el estado interno.")
    print()

    print("=" * 70)
    print("CONCLUSION:")
    print("  SHA-256(secreto || mensaje) es VULNERABLE")
    print("  HMAC-SHA-256(secreto, mensaje) es SEGURO")
    print("  SIEMPRE usa HMAC para autenticacion de mensajes.")
    print("=" * 70)


if __name__ == "__main__":
    main()
```

---

## Resumen del capitulo

En este capitulo abrimos la caja negra de las funciones hash. Aprendiste:

1. **La construccion de Merkle-Damgard** es la arquitectura compartida por MD5, SHA-1 y SHA-2. Funciona procesando el mensaje en bloques a traves de una funcion de compresion iterativa.

2. **"Roto" no significa "deja de funcionar"**. Significa que una de las tres resistencias (preimagen, segunda preimagen, colision) ha sido comprometida significativamente.

3. **El ataque de extension de longitud** explota que en Merkle-Damgard el hash final es el estado interno. Nunca uses `hash(secreto || mensaje)` para autenticacion; usa HMAC.

4. **MD5 esta completamente roto** para colisiones. El caso Flame demostro las consecuencias catastroficas de no migrar.

5. **SHA-1 esta roto** para colisiones desde 2017 (SHAttered). La migracion tardo mas de 20 anos.

6. **SHA-2 sigue siendo seguro** despues de mas de dos decadas de criptoanalisis. SHA-256 es el estandar actual para uso general.

En el proximo capitulo veremos SHA-3 y la construccion de esponja: un diseno radicalmente diferente que elimina las debilidades estructurales de Merkle-Damgard.

---

## Referencias

- Aumasson, J.P. (2024). *Serious Cryptography*, 2nd ed. No Starch Press.
- Bellare, M. y Rogaway, P. (2006). "The Security of Triple Encryption and a Framework for Code-Based Game-Playing Proofs." Advances in Cryptology -- EUROCRYPT 2006.
- Damgard, I. (1989). "A Design Principle for Hash Functions." Advances in Cryptology -- CRYPTO '89.
- Duong, T. y Rizzo, J. (2009). "Flickr's API Signature Forgery Vulnerability."
- Klima, V. (2006). "Tunnels in Hash Functions: MD5 Collisions Within a Minute." IACR ePrint.
- Merkle, R. (1979). "Secrecy, Authentication, and Public Key Systems." Ph.D. thesis, Stanford University.
- Microsoft Security Response Center (2012). "Flame Malware Collision Attack Explained."
- NIST (2015). "Secure Hash Standard (SHS)." FIPS PUB 180-4.
- Rivest, R. (1992). "The MD5 Message-Digest Algorithm." RFC 1321.
- Sotirov, A. (2012). "Analyzing the MD5 collision in Flame." Presentacion en CRYPTO 2012 Rump Session.
- Sotirov, A. et al. (2008). "MD5 considered harmful today: Creating a rogue CA certificate."
- Stevens, M. et al. (2017). "The first collision for full SHA-1." Advances in Cryptology -- CRYPTO 2017.
- Wang, X. y Yu, H. (2005). "How to Break MD5 and Other Hash Functions." Advances in Cryptology -- EUROCRYPT 2005.
- Wang, X., Yin, Y.L. y Yu, H. (2005). "Finding Collisions in the Full SHA-1." Advances in Cryptology -- CRYPTO 2005.
