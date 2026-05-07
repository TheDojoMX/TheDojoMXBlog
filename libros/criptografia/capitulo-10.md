# Capitulo 10: MACs -- Verifica que el mensaje no fue alterado

> "Cifrar no es autenticar. Puedes cambiar un mensaje cifrado sin descifrarlo. En 2014, investigadores demostraron que podian alterar mensajes cifrados de iMessage de Apple sin que el receptor lo notara. El cifrado protegia la confidencialidad, pero nadie verificaba la integridad."

---

Imagina que envias una transferencia bancaria cifrada: "Transferir $100 a la cuenta 12345678". Un atacante intercepta el mensaje cifrado. No puede leerlo --el cifrado funciona-- pero sabe que el monto esta en cierta posicion del mensaje. Si el cifrado usa XOR (como un cifrado de flujo o AES-CTR), el atacante puede aplicar XOR selectivamente a los bytes del monto y convertir "$100" en "$999" sin conocer la llave, sin descifrar el mensaje, sin dejar evidencia de la modificacion.

Esto no es un escenario teorico. Es exactamente lo que ocurre cuando cifras sin autenticar. Y es exactamente lo que los codigos de autenticacion de mensajes (MACs) estan disenados para prevenir.

En los capitulos 7 y 8 aprendimos a cifrar con AES y ChaCha20. Vimos brevemente que AES-GCM y ChaCha20-Poly1305 incluyen autenticacion. En este capitulo entenderemos **por que** esa autenticacion es necesaria, **como** funciona por dentro, y **como** implementarla correctamente cuando no tienes un cifrado autenticado integrado.

---

## 10.1 El problema de la autenticidad

### 10.1.1 Cifrar no es autenticar

La criptografia clasica se enfoca en **confidencialidad**: evitar que un adversario lea el mensaje. Pero la confidencialidad, por si sola, no protege contra **modificacion**.

Estas son propiedades independientes:

| Propiedad | Que protege | Herramienta |
|-----------|------------|-------------|
| Confidencialidad | Que nadie mas lea el mensaje | Cifrado (AES, ChaCha20) |
| Integridad | Que el mensaje no fue modificado | MAC (HMAC, CMAC, Poly1305) |
| Autenticidad | Que el mensaje viene de quien dice | MAC + llave compartida |

Un MAC (Message Authentication Code) es una funcion que toma un mensaje y una **llave secreta** y produce una etiqueta (tag) de tamano fijo. Solo quien posee la llave puede generar o verificar la etiqueta. Si alguien modifica el mensaje, la etiqueta no coincidira.

```
Generacion:
  Mensaje + Llave secreta ---> MAC() ---> Tag (etiqueta)

Verificacion:
  Mensaje recibido + Llave secreta ---> MAC() ---> Tag calculado
  Comparar Tag calculado con Tag recibido (en tiempo constante!)
  Si son iguales: mensaje autentico e integro
  Si difieren: mensaje modificado o falso
```

### 10.1.2 Ataques por falta de autenticacion

Sin autenticacion, los cifrados son vulnerables a varias clases de ataques:

**Bit-flipping en cifrados de flujo y modos CTR:**

Como vimos en el capitulo 8, un cifrado de flujo produce el texto cifrado como `C = M XOR keystream`. Si el atacante aplica XOR a un bit especifico del cifrado, el mismo bit cambia en el texto plano descifrado:

```python
"""
bit_flipping_demo.py

Demuestra el ataque de bit-flipping contra cifrado sin autenticacion.
"""

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms


def cifrar_chacha20_sin_auth(llave: bytes, nonce: bytes,
                              mensaje: bytes) -> bytes:
    """
    Cifra con ChaCha20 crudo (sin Poly1305).
    PELIGRO: sin autenticacion, vulnerable a manipulacion.
    """
    cifrador = Cipher(
        algorithms.ChaCha20(llave, nonce), mode=None
    ).encryptor()
    return cifrador.update(mensaje)


def descifrar_chacha20_sin_auth(llave: bytes, nonce: bytes,
                                 cifrado: bytes) -> bytes:
    """Descifra sin verificar integridad."""
    descifrador = Cipher(
        algorithms.ChaCha20(llave, nonce), mode=None
    ).decryptor()
    return descifrador.update(cifrado)


# Escenario: transferencia bancaria
llave = os.urandom(32)
nonce = os.urandom(16)

mensaje_original = b"Transferir $0100 a cuenta 12345678"
print(f"Mensaje original: {mensaje_original.decode()}")

# Cifrar (sin autenticacion)
cifrado = cifrar_chacha20_sin_auth(llave, nonce, mensaje_original)

# --- Ataque: el atacante NO conoce la llave ---
# Pero sabe que los bytes 13-16 son el monto "$0100"
# Quiere cambiar "$0100" a "$9999"
cifrado_alterado = bytearray(cifrado)

# XOR los bytes del monto con el valor original y el deseado
monto_original = b"0100"
monto_deseado = b"9999"
offset_monto = 13  # Posicion del monto en el mensaje

for i in range(4):
    cifrado_alterado[offset_monto + i] ^= (
        monto_original[i] ^ monto_deseado[i]
    )

# Descifrar el mensaje alterado
descifrado = descifrar_chacha20_sin_auth(
    llave, nonce, bytes(cifrado_alterado)
)
print(f"Mensaje alterado:  {descifrado.decode()}")
print(f"\nEl atacante cambio el monto de $0100 a $9999")
print(f"sin conocer la llave ni descifrar el mensaje.")
```

**Padding oracle en AES-CBC:**

El ataque de padding oracle, descrito por Serge Vaudenay en 2002, explota la falta de autenticacion en AES-CBC. El atacante envia textos cifrados modificados al servidor y observa si el servidor reporta un "error de padding" o un "error de descifrado". Con suficientes intentos (tipicamente unos pocos miles de requests por bloque), puede descifrar el mensaje completo byte por byte [Vaudenay, 2002].

Este ataque fue explotado en la practica contra ASP.NET (2010), contra Java Server Faces, y contra versiones antiguas de TLS (el ataque POODLE de 2014 contra SSL 3.0 y el ataque Lucky13 contra TLS 1.0-1.2).

**Caso iMessage (2014):**

En 2014, investigadores de la Universidad Johns Hopkins demostraron que iMessage de Apple era vulnerable a ataques de manipulacion. Apple cifraba los mensajes pero no los autenticaba correctamente. Los investigadores pudieron alterar adjuntos cifrados y, explotando el oraculo creado por los servidores de Apple, eventualmente descifrar contenido [Green et al., 2016].

La leccion es universal: **cifrar sin autenticar es insuficiente**. La autenticacion no es opcional ni un "extra de seguridad". Es un componente fundamental sin el cual el cifrado puede volverse peor que inutil --porque proporciona una falsa sensacion de seguridad.

### 10.1.3 Que es un MAC formalmente

Un MAC es una funcion `Tag = MAC(K, M)` donde:

- `K` es una llave secreta compartida entre las partes.
- `M` es el mensaje de longitud arbitraria.
- `Tag` es la etiqueta de tamano fijo (tipicamente 128 o 256 bits).

Para ser seguro, un MAC debe cumplir la propiedad de **infalsificabilidad bajo ataques de mensaje elegido** (EUF-CMA: Existential Unforgeability under Chosen Message Attack). Esto significa que un atacante que puede solicitar tags para mensajes de su eleccion no puede producir un tag valido para un mensaje nuevo --uno cuyo tag no haya solicitado previamente.

La diferencia con un hash es crucial:

| | Hash | MAC |
|-|------|-----|
| Usa llave? | No | Si |
| Cualquiera puede calcular? | Si | Solo quien tiene la llave |
| Protege contra modificacion por un tercero? | No (cualquiera recalcula el hash) | Si |
| Ejemplo | SHA-256(mensaje) | HMAC-SHA-256(llave, mensaje) |

Un hash sin llave puede verificar integridad contra corrupcion accidental (errores de disco, de red), pero no contra un adversario activo que puede recalcular el hash del mensaje modificado. Un MAC resiste adversarios activos porque requiere la llave secreta.

---

## 10.2 HMAC: el estandar para autenticacion basada en hash

### 10.2.1 Por que hash(llave || mensaje) no es seguro

La primera idea que se le ocurre a cualquier desarrollador para construir un MAC es simple: "tomo un hash, le concateno la llave al principio, y listo". Algo como:

```python
# PELIGRO: MAC casero vulnerable
tag = sha256(llave + mensaje).hexdigest()
```

Esto es vulnerable al **ataque de extension de longitud** (length extension attack) que vimos en el capitulo 3. Los hashes basados en la construccion de Merkle-Damgard (MD5, SHA-1, SHA-256) tienen una propiedad peligrosa: dado `hash(X)` y la longitud de `X`, puedes calcular `hash(X || padding || extension)` sin conocer `X`.

Si el atacante conoce `tag = SHA-256(llave || mensaje)` y la longitud de `llave || mensaje`, puede calcular:

```
SHA-256(llave || mensaje || padding || datos_extra)
```

Sin conocer la llave. Esto le permite crear tags validos para mensajes extendidos.

Poner la llave al final (`SHA-256(mensaje || llave)`) tampoco es seguro: si el hash subyacente tiene colisiones (como MD5), el atacante puede encontrar dos mensajes con el mismo hash interno y ambos tendran el mismo tag.

SHA-3 (Keccak) no es vulnerable a extension de longitud por su diseno de esponja, por lo que `SHA3-256(llave || mensaje)` es seguro en principio. Sin embargo, HMAC sigue siendo la practica recomendada porque proporciona una capa adicional de seguridad: incluso si se descubriera una debilidad en el hash subyacente, la construccion HMAC tiene margenes de seguridad propios.

### 10.2.2 La construccion HMAC

HMAC fue disenado por Mihir Bellare, Ran Canetti y Hugo Krawczyk en 1996 y publicado como RFC 2104 [Bellare, Canetti, Krawczyk, 1996]. Su construccion resuelve elegantemente los problemas de `hash(llave || mensaje)`.

La formula es:

```
HMAC(K, M) = H( (K XOR opad) || H( (K XOR ipad) || M ) )
```

Donde:
- `H` es la funcion hash subyacente (SHA-256, SHA-512, etc.).
- `K` es la llave, ajustada al tamano de bloque del hash (si es mas corta, se rellena con ceros; si es mas larga, se hashea primero).
- `ipad` es el byte `0x36` repetido hasta completar el tamano de bloque.
- `opad` es el byte `0x5C` repetido hasta completar el tamano de bloque.

El proceso paso a paso:

```
1. Si |K| > tamano_bloque: K = H(K)
2. Si |K| < tamano_bloque: K = K || 0x00...00 (rellenar con ceros)
3. Calcular K_ipad = K XOR ipad
4. Calcular hash_interno = H(K_ipad || mensaje)
5. Calcular K_opad = K XOR opad
6. Calcular tag = H(K_opad || hash_interno)
```

La construccion de doble hash es critica: el hash interno protege contra extension de longitud (su salida es de tamano fijo), y el hash externo proporciona una capa adicional de seguridad.

Implementemos HMAC desde cero para entender cada paso:

```python
"""
hmac_manual.py

Implementacion educativa de HMAC-SHA-256 desde cero.
Solo para entender la construccion -- en produccion, usa hmac.new().
"""

import hashlib


def hmac_sha256_manual(llave: bytes, mensaje: bytes) -> bytes:
    """
    Implementacion educativa de HMAC-SHA-256.
    Sigue RFC 2104 paso a paso.

    NO USAR EN PRODUCCION -- usa hmac.new() de la libreria estandar.
    """
    # SHA-256 tiene un tamano de bloque de 64 bytes (512 bits)
    tamano_bloque = 64

    # Paso 1: ajustar la llave al tamano de bloque
    if len(llave) > tamano_bloque:
        # Si la llave es mas larga, hashearla primero
        llave = hashlib.sha256(llave).digest()
    if len(llave) < tamano_bloque:
        # Si es mas corta, rellenar con ceros
        llave = llave + b'\x00' * (tamano_bloque - len(llave))

    # Paso 2: construir ipad y opad
    ipad = bytes(k ^ 0x36 for k in llave)
    opad = bytes(k ^ 0x5C for k in llave)

    # Paso 3: hash interno
    hash_interno = hashlib.sha256(ipad + mensaje).digest()

    # Paso 4: hash externo (el tag final)
    tag = hashlib.sha256(opad + hash_interno).digest()

    return tag


# --- Verificar contra la implementacion estandar ---

import hmac

llave = b"mi_llave_secreta_de_ejemplo"
mensaje = b"Este mensaje debe ser autenticado"

# Nuestra implementacion
tag_manual = hmac_sha256_manual(llave, mensaje)

# Implementacion estandar
tag_estandar = hmac.new(llave, mensaje, hashlib.sha256).digest()

print("=== Verificacion de HMAC-SHA-256 ===\n")
print(f"Llave:       {llave.decode()}")
print(f"Mensaje:     {mensaje.decode()}")
print(f"Tag manual:  {tag_manual.hex()}")
print(f"Tag hmac:    {tag_estandar.hex()}")
print(f"Coinciden:   {tag_manual == tag_estandar}")

# Demostrar que cambiar un byte del mensaje cambia todo el tag
mensaje_alterado = b"Este mensaje debe ser autentificado"  # 'autentificado'
tag_alterado = hmac_sha256_manual(llave, mensaje_alterado)
print(f"\nMensaje alt: {mensaje_alterado.decode()}")
print(f"Tag alt:     {tag_alterado.hex()}")
print(f"Tags iguales: {tag_manual == tag_alterado}")
```

### 10.2.3 Prueba de seguridad de HMAC

La seguridad de HMAC fue demostrada formalmente por Bellare, Canetti y Krawczyk en 1996. Su prueba original requeria dos supuestos:

1. Que la **funcion de compresion** del hash subyacente sea una funcion pseudo-aleatoria (PRF).
2. Que la funcion hash iterada sea debilmente resistente a colisiones.

Cuando se descubrieron colisiones practicas en MD5 (2004) y SHA-1 (2017), el supuesto (2) cayo para esos hashes. Esto ponia en duda la seguridad de HMAC-MD5 y HMAC-SHA-1.

En 2006, Bellare publico una nueva prueba que solo requiere el supuesto (1): que la funcion de compresion sea una PRF [Bellare, 2006]. Dado que no se conocen ataques contra la propiedad de pseudo-aleatoriedad de las funciones de compresion de MD5 o SHA-1, HMAC-MD5 y HMAC-SHA-1 siguen siendo tecnicamente seguros como MACs, aunque se recomienda migrar a HMAC-SHA-256 por prudencia.

La implicacion practica: HMAC proporciona un margen de seguridad mas alla del hash subyacente. Incluso si el hash tiene debilidades (como colisiones), HMAC puede seguir siendo seguro. Esta es una de las razones por las que HMAC sigue siendo recomendado incluso con SHA-3, que no necesitaria la construccion HMAC por no ser vulnerable a extension de longitud.

### 10.2.4 HMAC en la practica con Python

```python
"""
hmac_practico.py

Uso correcto de HMAC en Python para escenarios reales.

Prerequisitos:
  pip install cryptography
"""

import hmac
import hashlib
import os
import time
import secrets


# ============================================================
# 1. Firmado y verificacion basica
# ============================================================

print("=== 1. Firmado y verificacion basica ===\n")

llave = os.urandom(32)  # 256 bits -- SIEMPRE generar con CSPRNG
mensaje = b"Orden #4521: transferir $5000 a cuenta 98765432"

# Generar tag
tag = hmac.new(llave, mensaje, hashlib.sha256).digest()
print(f"Mensaje: {mensaje.decode()}")
print(f"Tag:     {tag.hex()}")
print(f"Tamano:  {len(tag)} bytes ({len(tag) * 8} bits)")

# Verificar (SIEMPRE usar compare_digest, NUNCA ==)
tag_recibido = tag  # En la practica, vendria con el mensaje
es_valido = hmac.compare_digest(
    tag,
    hmac.new(llave, mensaje, hashlib.sha256).digest()
)
print(f"Valido:  {es_valido}")

# Intentar verificar con mensaje alterado
mensaje_falso = b"Orden #4521: transferir $9999 a cuenta 98765432"
es_valido_falso = hmac.compare_digest(
    tag,
    hmac.new(llave, mensaje_falso, hashlib.sha256).digest()
)
print(f"Falso:   {es_valido_falso}")


# ============================================================
# 2. Firmado de webhooks (como lo hacen GitHub, Stripe, Slack)
# ============================================================

print("\n=== 2. Firmado de webhooks ===\n")


def firmar_webhook(secreto: bytes, payload: bytes) -> str:
    """
    Genera una firma HMAC-SHA-256 para un webhook.
    Retorna el tag como string hexadecimal con prefijo 'sha256='.
    (Formato usado por GitHub y Stripe.)
    """
    tag = hmac.new(secreto, payload, hashlib.sha256).hexdigest()
    return f"sha256={tag}"


def verificar_webhook(secreto: bytes, payload: bytes,
                       firma_recibida: str) -> bool:
    """
    Verifica la firma de un webhook.
    Usa comparacion en tiempo constante para prevenir timing attacks.
    """
    firma_esperada = firmar_webhook(secreto, payload)
    return hmac.compare_digest(firma_esperada, firma_recibida)


# Simular un webhook de GitHub
secreto_webhook = b"mi_secreto_de_webhook_super_seguro"
payload = b'{"action":"push","ref":"refs/heads/main","commits":[...]}'

firma = firmar_webhook(secreto_webhook, payload)
print(f"Payload: {payload.decode()[:50]}...")
print(f"Firma:   {firma}")

# Verificar
print(f"Valida:  {verificar_webhook(secreto_webhook, payload, firma)}")

# Intento de falsificacion
payload_falso = b'{"action":"push","ref":"refs/heads/main","commits":[MALWARE]}'
print(f"Falsa:   {verificar_webhook(secreto_webhook, payload_falso, firma)}")


# ============================================================
# 3. Proteccion contra replay attacks
# ============================================================

print("\n=== 3. Proteccion contra replay attacks ===\n")


class VerificadorAntiReplay:
    """
    Verifica mensajes con HMAC y proteccion contra replay.
    Incluye timestamp para rechazar mensajes viejos.
    """

    def __init__(self, llave: bytes, ventana_segundos: int = 300):
        self.llave = llave
        self.ventana = ventana_segundos
        self.nonces_vistos: set[str] = set()

    def firmar(self, mensaje: bytes) -> dict:
        """Firma un mensaje con timestamp y nonce anti-replay."""
        timestamp = str(int(time.time())).encode()
        nonce = secrets.token_hex(16)

        # El tag cubre: mensaje + timestamp + nonce
        datos = mensaje + b"|ts:" + timestamp + b"|nonce:" + nonce.encode()
        tag = hmac.new(self.llave, datos, hashlib.sha256).hexdigest()

        return {
            "mensaje": mensaje,
            "timestamp": timestamp.decode(),
            "nonce": nonce,
            "tag": tag,
        }

    def verificar(self, paquete: dict) -> tuple[bool, str]:
        """
        Verifica un mensaje firmado.
        Retorna (valido, razon).
        """
        # 1. Verificar timestamp (rechazar mensajes viejos)
        ts = int(paquete["timestamp"])
        ahora = int(time.time())
        if abs(ahora - ts) > self.ventana:
            return False, "Timestamp fuera de ventana"

        # 2. Verificar nonce (rechazar replays)
        if paquete["nonce"] in self.nonces_vistos:
            return False, "Nonce reutilizado (replay detectado)"

        # 3. Verificar HMAC
        datos = (paquete["mensaje"]
                 + b"|ts:" + paquete["timestamp"].encode()
                 + b"|nonce:" + paquete["nonce"].encode())
        tag_esperado = hmac.new(
            self.llave, datos, hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(tag_esperado, paquete["tag"]):
            return False, "Tag HMAC invalido"

        # Todo OK: registrar nonce como usado
        self.nonces_vistos.add(paquete["nonce"])
        return True, "Valido"


# Demo
llave = os.urandom(32)
verificador = VerificadorAntiReplay(llave)

# Firmar y verificar un mensaje
paquete = verificador.firmar(b"Transferir $500")
valido, razon = verificador.verificar(paquete)
print(f"Primera verificacion: {valido} ({razon})")

# Intentar replay (mismo paquete)
valido, razon = verificador.verificar(paquete)
print(f"Replay del paquete:   {valido} ({razon})")

# Mensaje nuevo: OK
paquete2 = verificador.firmar(b"Consultar saldo")
valido, razon = verificador.verificar(paquete2)
print(f"Mensaje nuevo:        {valido} ({razon})")
```

### 10.2.5 Errores comunes con HMAC

**1. Comparacion no constant-time (timing attack):**

El error mas peligroso y mas comun. Si comparas dos tags con `==`, Python compara byte por byte y retorna `False` en el primer byte diferente. Un atacante puede medir el tiempo de respuesta y deducir cuantos bytes del tag son correctos, adivinando el tag completo byte por byte.

```python
"""
timing_attack_demo.py

Demuestra por que la comparacion con == es vulnerable a timing attacks.
"""

import hmac
import hashlib
import time
import os


def comparacion_insegura(tag_esperado: bytes, tag_recibido: bytes) -> bool:
    """
    PELIGRO: comparacion vulnerable a timing attack.
    Retorna False en el primer byte diferente, lo cual filtra informacion.
    """
    return tag_esperado == tag_recibido


def comparacion_segura(tag_esperado: bytes, tag_recibido: bytes) -> bool:
    """
    CORRECTO: comparacion en tiempo constante.
    Siempre compara TODOS los bytes, sin importar donde difieren.
    """
    return hmac.compare_digest(tag_esperado, tag_recibido)


# Demostrar la diferencia conceptual
llave = os.urandom(32)
mensaje = b"datos importantes"
tag_real = hmac.new(llave, mensaje, hashlib.sha256).digest()

# Crear tags con N bytes correctos y el resto incorrectos
print("=== Timing attack conceptual ===\n")
print("Bytes correctos | Comparacion == | compare_digest")
print("-" * 55)

for n_correctos in [0, 4, 8, 16, 24, 31, 32]:
    # Construir un tag con los primeros n_correctos bytes correctos
    tag_parcial = tag_real[:n_correctos] + bytes(32 - n_correctos)

    # Medir tiempo de comparacion insegura (muchas repeticiones)
    repeticiones = 100_000
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        comparacion_insegura(tag_real, tag_parcial)
    t_insegura = time.perf_counter() - inicio

    # Medir tiempo de comparacion segura
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        comparacion_segura(tag_real, tag_parcial)
    t_segura = time.perf_counter() - inicio

    print(f"{n_correctos:>16} | {t_insegura*1000:>12.3f} ms | {t_segura*1000:>12.3f} ms")

print(f"\nNota: en la comparacion insegura, el tiempo puede aumentar")
print(f"con mas bytes correctos (depende de la implementacion de CPython).")
print(f"La comparacion segura toma tiempo constante sin importar")
print(f"cuantos bytes coinciden.")
print(f"\nREGLA: SIEMPRE usa hmac.compare_digest() o secrets.compare_digest()")
```

En la practica, este ataque fue demostrado contra la API de Flickr en 2009, donde la comparacion no constant-time de la firma HMAC permitia forjar firmas caracter por caracter [Lawson, 2009].

**2. Llave demasiado corta:**

La llave de HMAC debe tener al menos tantos bits como la seguridad del hash subyacente. Para HMAC-SHA-256, usa llaves de al menos 32 bytes (256 bits). Una llave de 8 bytes reduce la seguridad a solo 64 bits --atacable por fuerza bruta.

**3. Usar MD5 como hash base:**

Aunque HMAC-MD5 no esta formalmente roto (la prueba de seguridad de HMAC no depende de resistencia a colisiones), MD5 tiene debilidades suficientes como para que su uso sea desaconsejado. Usa HMAC-SHA-256 como minimo.

**4. No incluir contexto en el mensaje:**

Si firmas solo el cuerpo de un request HTTP sin incluir el metodo, la URL y las cabeceras relevantes, un atacante puede tomar una firma valida de un GET y usarla en un POST, o redirigir el request a un endpoint diferente.

---

## 10.3 CMAC: autenticacion basada en cifrados de bloque

### 10.3.1 Construccion de CMAC

CMAC (Cipher-based Message Authentication Code), estandarizado en NIST SP 800-38B, usa un cifrado de bloque (tipicamente AES) para construir un MAC. La idea es aplicar AES en modo CBC al mensaje y usar el ultimo bloque cifrado como tag.

La construccion es mas compleja que simplemente "AES-CBC del mensaje":

1. Se derivan dos subllaves K1 y K2 a partir de la llave principal cifrando un bloque de ceros.
2. El mensaje se divide en bloques de 128 bits (el tamano de bloque de AES).
3. Se procesan los bloques en modo CBC (sin IV -- se usa un bloque de ceros).
4. El ultimo bloque se trata de forma especial: si el mensaje es multiplo exacto del tamano de bloque, se aplica XOR con K1; si no, se rellena y se aplica XOR con K2.
5. El ultimo bloque cifrado (o un truncamiento de este) es el tag.

```python
"""
cmac_demo.py

Uso de AES-CMAC con la libreria cryptography.

Prerequisitos:
  pip install cryptography
"""

import os
from cryptography.hazmat.primitives.cmac import CMAC
from cryptography.hazmat.primitives.ciphers import algorithms


def generar_cmac(llave: bytes, mensaje: bytes) -> bytes:
    """
    Genera un tag AES-CMAC.

    llave: 16 bytes (AES-128) o 32 bytes (AES-256).
    """
    c = CMAC(algorithms.AES(llave))
    c.update(mensaje)
    return c.finalize()


def verificar_cmac(llave: bytes, mensaje: bytes, tag: bytes) -> bool:
    """
    Verifica un tag AES-CMAC.
    Retorna True si es valido, False si no.
    """
    c = CMAC(algorithms.AES(llave))
    c.update(mensaje)
    try:
        c.verify(tag)
        return True
    except Exception:
        return False


# --- Demo ---

llave = os.urandom(32)  # AES-256-CMAC
mensaje = b"Mensaje autenticado con AES-CMAC"

tag = generar_cmac(llave, mensaje)
print(f"=== AES-CMAC ===\n")
print(f"Mensaje: {mensaje.decode()}")
print(f"Tag:     {tag.hex()}")
print(f"Tamano:  {len(tag)} bytes ({len(tag) * 8} bits)")

# Verificar
print(f"Valido:  {verificar_cmac(llave, mensaje, tag)}")
print(f"Falso:   {verificar_cmac(llave, b'mensaje alterado', tag)}")
```

### 10.3.2 CMAC vs HMAC

| Aspecto | HMAC | CMAC |
|---------|------|------|
| Base | Funcion hash | Cifrado de bloque |
| Velocidad (con AES-NI) | Depende del hash | Muy rapido |
| Velocidad (sin AES-NI) | Generalmente mas rapido | Mas lento |
| Tamano de tag | Variable (hash output) | 128 bits (AES) |
| Uso tipico | TLS, APIs, JWT | WiFi WPA2, Bluetooth LE, IEEE 802.1AE |
| Madurez | RFC 2104 (1997) | NIST SP 800-38B (2005) |

En la practica, HMAC es mas comun en protocolos de aplicacion (HTTPS, APIs, tokens). CMAC se usa mas en protocolos de bajo nivel y hardware (WiFi, Bluetooth, redes de area local seguras).

---

## 10.4 Poly1305 y MACs modernos

### 10.4.1 Poly1305: el MAC ultrarapido

Poly1305, disenado por Daniel J. Bernstein en 2005, es un MAC radicalmente diferente a HMAC y CMAC. En lugar de usar un hash o un cifrado de bloque iterativamente, calcula una evaluacion de un **polinomio** en un campo finito.

El nombre viene del primo usado: 2^130 - 5. El tag se calcula como:

```
Tag = ((c1 * r^n + c2 * r^(n-1) + ... + cn * r) mod (2^130 - 5)) + s) mod 2^128
```

Donde:
- `r` es una llave de autenticacion de 128 bits (con ciertos bits fijados a cero para eficiencia).
- `s` es una llave de cifrado de 128 bits que se suma al final.
- `c1, c2, ..., cn` son los bloques del mensaje de 128 bits cada uno.

La velocidad de Poly1305 es excepcional: en software puro, es significativamente mas rapido que HMAC-SHA-256 y comparable a AES-CMAC con AES-NI. Esto lo hace ideal para dispositivos moviles y sistemas embebidos.

### 10.4.2 La restriccion critica: una llave por mensaje

Poly1305 tiene una restriccion fundamental que lo distingue de HMAC y CMAC: **la llave (r, s) debe ser unica para cada mensaje**. Si un atacante obtiene dos tags generados con la misma llave `r` para dos mensajes diferentes, puede recuperar `r` algebraicamente y a partir de ahi forjar tags para cualquier mensaje.

Por esta razon, Poly1305 **nunca se usa solo**. Se combina con un cifrado de flujo que genera una llave fresca para cada mensaje:

- **ChaCha20-Poly1305**: ChaCha20 genera la subllave de Poly1305 usando el bloque 0 del keystream. Cada mensaje tiene una llave Poly1305 diferente porque cada mensaje tiene un nonce diferente.
- **AES-GCM**: GHASH (el MAC de GCM) es conceptualmente similar a Poly1305 --ambos evaluan polinomios sobre campos finitos-- aunque opera sobre GF(2^128) en lugar de un campo primo.

### 10.4.3 SipHash: para hashtables y mensajes cortos

SipHash, disenado por Jean-Philippe Aumasson y Bernstein en 2012, ocupa un nicho diferente. No es un MAC criptografico completo en el sentido tradicional --su tag es mas corto (64 o 128 bits) y esta optimizado para mensajes de pocos bytes.

Su uso principal es proteger hashtables contra ataques de flooding (HashDoS). Python, Rust, y Redis usan SipHash internamente para generar hashes de cadenas, protegiendo contra ataques que generan colisiones deliberadas para degradar el rendimiento de las hashtables de O(1) a O(n) [Aumasson, Bernstein, 2012].

### 10.4.4 Comparacion de MACs

```python
"""
comparacion_macs.py

Compara rendimiento de diferentes MACs.

Prerequisitos:
  pip install cryptography
"""

import os
import hmac
import hashlib
import time
from cryptography.hazmat.primitives.cmac import CMAC
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


def benchmark_mac(nombre: str, funcion, iteraciones: int,
                  tamano_datos: int) -> float:
    """Ejecuta benchmark de un MAC y retorna operaciones/segundo."""
    datos = os.urandom(tamano_datos)

    # Calentar
    for _ in range(100):
        funcion(datos)

    inicio = time.perf_counter()
    for _ in range(iteraciones):
        funcion(datos)
    duracion = time.perf_counter() - inicio

    ops_por_segundo = iteraciones / duracion
    mbps = (tamano_datos * iteraciones / 1_000_000) / duracion
    print(f"  {nombre:>25}: {ops_por_segundo:>10,.0f} ops/s | {mbps:>8.1f} MB/s")
    return mbps


# Configurar MACs
llave_hmac = os.urandom(32)
llave_cmac = os.urandom(32)
llave_chacha = ChaCha20Poly1305.generate_key()

# HMAC-SHA-256
def mac_hmac(datos: bytes) -> bytes:
    return hmac.new(llave_hmac, datos, hashlib.sha256).digest()

# HMAC-SHA-512
def mac_hmac_512(datos: bytes) -> bytes:
    return hmac.new(llave_hmac, datos, hashlib.sha512).digest()

# AES-256-CMAC
def mac_cmac(datos: bytes) -> bytes:
    c = CMAC(algorithms.AES(llave_cmac))
    c.update(datos)
    return c.finalize()

# ChaCha20-Poly1305 (extrae solo el tag, usando la AEAD completa)
chacha = ChaCha20Poly1305(llave_chacha)
def mac_poly1305(datos: bytes) -> bytes:
    nonce = os.urandom(12)
    # El tag son los ultimos 16 bytes del cifrado
    cifrado = chacha.encrypt(nonce, datos, None)
    return cifrado[-16:]  # Solo el tag


# Benchmarks con diferentes tamanos
for tamano in [64, 1024, 16384]:
    iters = 50_000 if tamano <= 1024 else 5_000
    print(f"\nTamano de mensaje: {tamano} bytes ({iters} iteraciones)")
    benchmark_mac("HMAC-SHA-256", mac_hmac, iters, tamano)
    benchmark_mac("HMAC-SHA-512", mac_hmac_512, iters, tamano)
    benchmark_mac("AES-256-CMAC", mac_cmac, iters, tamano)
    benchmark_mac("ChaCha20-Poly1305", mac_poly1305, iters, tamano)
```

---

## 10.5 Encrypt-then-MAC vs MAC-then-Encrypt vs Encrypt-and-MAC

### 10.5.1 Las tres formas de combinar cifrado y MAC

Cuando necesitas tanto confidencialidad como autenticidad, debes combinar un cifrado con un MAC. Hay tres ordenes posibles, y **el orden importa enormemente**:

**Encrypt-and-MAC (E&M):**
Cifras el mensaje y calculas el MAC del mensaje en claro. Envias ambos.
```
C = Encrypt(Ke, M)
T = MAC(Ka, M)
Enviar: C || T
```
Problema: el MAC se calcula sobre el texto plano. Si el MAC filtra informacion sobre el mensaje (por ejemplo, si dos mensajes identicos producen el mismo tag), la confidencialidad se ve comprometida. Este fue el esquema usado originalmente por SSH.

**MAC-then-Encrypt (MtE):**
Calculas el MAC del mensaje en claro, lo concatenas al mensaje, y cifras todo junto.
```
T = MAC(Ka, M)
C = Encrypt(Ke, M || T)
Enviar: C
```
Problema: para verificar el MAC, primero debes descifrar. Si el cifrado es AES-CBC, los errores de descifrado pueden revelar informacion sobre el texto plano antes de que el MAC se verifique. Esto habilita ataques de padding oracle. Este fue el esquema de SSL/TLS hasta la version 1.2, y fue la razon de los ataques POODLE, Lucky13, y BEAST.

**Encrypt-then-MAC (EtM):**
Cifras el mensaje primero, luego calculas el MAC del texto cifrado.
```
C = Encrypt(Ke, M)
T = MAC(Ka, C)
Enviar: C || T
```
Ventaja: verificas el MAC **antes** de descifrar. Si el MAC no coincide, rechazas el mensaje sin intentar descifrarlo. Esto elimina toda la clase de ataques de padding oracle y cualquier manipulacion del texto cifrado. Este es el esquema de IPsec y el unico esquema probado como seguro por Krawczyk [Krawczyk, 2001].

### 10.5.2 La prueba de Krawczyk

En 2001, Hugo Krawczyk publico un analisis formal que demostro:

1. **Encrypt-then-MAC es seguro** si el cifrado es CPA-seguro (seguro contra ataques de texto plano elegido) y el MAC es un MAC seguro. Es decir, la composicion de un cifrado seguro con un MAC seguro siempre produce un esquema de cifrado autenticado seguro.

2. **MAC-then-Encrypt no es genericamente seguro**. Krawczyk construyo un ejemplo de un cifrado que es CPA-seguro pero que, combinado con cualquier MAC en el esquema MtE, produce un sistema completamente inseguro [Krawczyk, 2001].

3. **Encrypt-and-MAC no es genericamente seguro**. El MAC puede revelar informacion sobre el texto plano, comprometiendo la confidencialidad.

Estos resultados no son teoricos: los ataques practicos contra SSL/TLS (que usaba MtE) confirmaron la prediccion.

```python
"""
encrypt_then_mac.py

Implementa los tres patrones y demuestra por que solo
Encrypt-then-MAC es correcto.

Prerequisitos:
  pip install cryptography
"""

import os
import hmac
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


def pad(datos: bytes, tamano_bloque: int = 128) -> bytes:
    """Aplica padding PKCS7."""
    padder = padding.PKCS7(tamano_bloque).padder()
    return padder.update(datos) + padder.finalize()


def unpad(datos: bytes, tamano_bloque: int = 128) -> bytes:
    """Remueve padding PKCS7."""
    unpadder = padding.PKCS7(tamano_bloque).unpadder()
    return unpadder.update(datos) + unpadder.finalize()


def aes_cbc_cifrar(llave: bytes, iv: bytes, datos: bytes) -> bytes:
    """Cifra con AES-CBC."""
    cifrador = Cipher(algorithms.AES(llave), modes.CBC(iv)).encryptor()
    return cifrador.update(pad(datos)) + cifrador.finalize()


def aes_cbc_descifrar(llave: bytes, iv: bytes, cifrado: bytes) -> bytes:
    """Descifra con AES-CBC."""
    descifrador = Cipher(algorithms.AES(llave), modes.CBC(iv)).decryptor()
    return unpad(descifrador.update(cifrado) + descifrador.finalize())


# ============================================================
# Esquema 1: Encrypt-then-MAC (CORRECTO)
# ============================================================

print("=== Encrypt-then-MAC (EtM) -- CORRECTO ===\n")


def etm_cifrar(ke: bytes, ka: bytes, mensaje: bytes) -> dict:
    """Cifra y luego autentica el cifrado."""
    iv = os.urandom(16)
    cifrado = aes_cbc_cifrar(ke, iv, mensaje)

    # MAC sobre IV + cifrado (ambos son publicos)
    tag = hmac.new(ka, iv + cifrado, hashlib.sha256).digest()

    return {"iv": iv, "cifrado": cifrado, "tag": tag}


def etm_descifrar(ke: bytes, ka: bytes, paquete: dict) -> bytes:
    """Verifica el MAC ANTES de descifrar."""
    # 1. Verificar MAC primero (sin descifrar)
    tag_esperado = hmac.new(
        ka, paquete["iv"] + paquete["cifrado"], hashlib.sha256
    ).digest()
    if not hmac.compare_digest(tag_esperado, paquete["tag"]):
        raise ValueError("MAC invalido: mensaje rechazado sin descifrar")

    # 2. Solo descifrar si el MAC es valido
    return aes_cbc_descifrar(ke, paquete["iv"], paquete["cifrado"])


ke = os.urandom(32)  # Llave de cifrado
ka = os.urandom(32)  # Llave de autenticacion (SEPARADA!)

mensaje = b"Encrypt-then-MAC es el patron correcto"
paquete = etm_cifrar(ke, ka, mensaje)
descifrado = etm_descifrar(ke, ka, paquete)
print(f"Descifrado: {descifrado.decode()}")

# Intentar alterar el cifrado
paquete_falso = dict(paquete)
cifrado_alterado = bytearray(paquete["cifrado"])
cifrado_alterado[0] ^= 0x01
paquete_falso["cifrado"] = bytes(cifrado_alterado)

try:
    etm_descifrar(ke, ka, paquete_falso)
    print("ERROR: no detecto la alteracion!")
except ValueError as e:
    print(f"Alteracion detectada: {e}")
    print("El mensaje se rechazo SIN intentar descifrar.")


# ============================================================
# Esquema 2: MAC-then-Encrypt (VULNERABLE)
# ============================================================

print("\n=== MAC-then-Encrypt (MtE) -- VULNERABLE ===\n")


def mte_cifrar(ke: bytes, ka: bytes, mensaje: bytes) -> dict:
    """Autentica el mensaje y luego cifra mensaje+tag."""
    tag = hmac.new(ka, mensaje, hashlib.sha256).digest()
    # Cifrar mensaje + tag juntos
    iv = os.urandom(16)
    cifrado = aes_cbc_cifrar(ke, iv, mensaje + tag)
    return {"iv": iv, "cifrado": cifrado}


def mte_descifrar(ke: bytes, ka: bytes, paquete: dict) -> bytes:
    """
    DEBE descifrar primero para verificar el MAC.
    Esto es el problema: si el descifrado falla de forma
    diferente segun el contenido, filtra informacion.
    """
    # 1. Descifrar (ANTES de verificar MAC -- PELIGROSO)
    datos = aes_cbc_descifrar(ke, paquete["iv"], paquete["cifrado"])

    # 2. Separar mensaje y tag
    mensaje = datos[:-32]
    tag = datos[-32:]

    # 3. Verificar MAC
    tag_esperado = hmac.new(ka, mensaje, hashlib.sha256).digest()
    if not hmac.compare_digest(tag_esperado, tag):
        raise ValueError("MAC invalido")

    return mensaje


mensaje = b"MAC-then-Encrypt puede ser vulnerable"
paquete = mte_cifrar(ke, ka, mensaje)
descifrado = mte_descifrar(ke, ka, paquete)
print(f"Descifrado: {descifrado.decode()}")
print(f"PROBLEMA: el descifrado ocurre ANTES de la verificacion del MAC.")
print(f"Un atacante puede explotar errores de padding para descifrar")
print(f"el mensaje sin conocer la llave (padding oracle attack).")


# ============================================================
# La solucion moderna: AEAD
# ============================================================

print("\n=== Solucion moderna: AEAD ===\n")
print("AES-GCM y ChaCha20-Poly1305 implementan Encrypt-then-MAC")
print("internamente, de forma atomica y sin posibilidad de error.")
print("SIEMPRE prefiere AEAD sobre composicion manual.")
```

### 10.5.3 La solucion moderna: AEAD

La mejor forma de combinar cifrado y autenticacion es **no hacerlo manualmente**. Los cifrados autenticados con datos asociados (AEAD) integran ambas operaciones en una sola primitiva atomica:

- **AES-GCM**: combina AES-CTR para cifrado con GHASH para autenticacion.
- **ChaCha20-Poly1305**: combina ChaCha20 para cifrado con Poly1305 para autenticacion.

Ambos implementan el patron Encrypt-then-MAC internamente y hacen imposible olvidar la autenticacion, usar el orden incorrecto, o reutilizar llaves entre cifrado y MAC.

```python
"""
aead_vs_manual.py

Compara AEAD (integrado) vs Encrypt-then-MAC manual.

Prerequisitos:
  pip install cryptography
"""

import os
from cryptography.hazmat.primitives.ciphers.aead import (
    AESGCM, ChaCha20Poly1305
)


# ============================================================
# AEAD: la forma correcta (y simple)
# ============================================================

print("=== AEAD: cifrado autenticado integrado ===\n")

# AES-256-GCM
llave_aes = AESGCM.generate_key(bit_length=256)
aesgcm = AESGCM(llave_aes)
nonce = os.urandom(12)

mensaje = b"AEAD combina cifrado y autenticacion en una sola operacion"
datos_asociados = b"metadatos que se autentican pero no se cifran"

# Una sola llamada: cifra Y autentica
cifrado = aesgcm.encrypt(nonce, mensaje, datos_asociados)
print(f"Mensaje:  {mensaje.decode()}")
print(f"Cifrado:  {cifrado.hex()[:60]}...")
print(f"Tamano:   {len(cifrado)} bytes (mensaje: {len(mensaje)}, tag: 16)")

# Una sola llamada: descifra Y verifica
descifrado = aesgcm.decrypt(nonce, cifrado, datos_asociados)
print(f"Descif:   {descifrado.decode()}")

# Cualquier modificacion se detecta automaticamente
cifrado_alterado = bytearray(cifrado)
cifrado_alterado[10] ^= 0x01

try:
    aesgcm.decrypt(nonce, bytes(cifrado_alterado), datos_asociados)
    print("ERROR: no detecto alteracion!")
except Exception as e:
    print(f"\nAlteracion detectada: {type(e).__name__}")

# Modificar datos asociados tambien falla
try:
    aesgcm.decrypt(nonce, cifrado, b"metadatos alterados")
    print("ERROR: no detecto alteracion de datos asociados!")
except Exception as e:
    print(f"Datos asociados alterados: {type(e).__name__}")


# ChaCha20-Poly1305 (misma API)
print("\n--- ChaCha20-Poly1305 ---")
llave_chacha = ChaCha20Poly1305.generate_key()
chacha = ChaCha20Poly1305(llave_chacha)
nonce = os.urandom(12)

cifrado = chacha.encrypt(nonce, mensaje, datos_asociados)
descifrado = chacha.decrypt(nonce, cifrado, datos_asociados)
print(f"Descif:   {descifrado.decode()}")


# ============================================================
# Tabla de decision
# ============================================================

print("\n=== Que usar segun tu escenario ===\n")

tabla = """
Escenario                          | Recomendacion
-----------------------------------+----------------------------------
Cifrar datos (nuevo proyecto)      | AES-256-GCM o ChaCha20-Poly1305
Solo autenticar (sin cifrar)       | HMAC-SHA-256
Firmado de API/webhooks            | HMAC-SHA-256
JWT con llave simetrica            | HMAC-SHA-256 (HS256)
Protocolo de bajo nivel/hardware   | AES-CMAC
Dispositivo sin AES-NI             | ChaCha20-Poly1305
Protocolo existente (sin AEAD)     | Encrypt-then-MAC con llaves sep.
Composicion manual de E+MAC        | NO. Usa AEAD en su lugar.
"""
print(tabla)
```

---

## 10.6 Caso real: JWT y el peligro de "alg: none"

### 10.6.1 JWT y HMAC

Los JSON Web Tokens (JWT) son uno de los usos mas visibles de HMAC en la web moderna. Un JWT firmado con HS256 (HMAC-SHA-256) contiene tres partes codificadas en Base64:

```
header.payload.signature

Header:  {"alg": "HS256", "typ": "JWT"}
Payload: {"sub": "1234567890", "name": "Hector", "admin": false}
Signature: HMAC-SHA-256(base64(header) + "." + base64(payload), secreto)
```

El servidor genera el token con su secreto y lo entrega al cliente. En cada request, el cliente envia el token y el servidor verifica la firma. Si alguien modifica el payload (por ejemplo, cambiando `"admin": false` a `"admin": true`), la firma no coincidira y el servidor rechazara el token.

### 10.6.2 El ataque "alg: none"

En 2015, investigadores descubrieron que muchas librerias JWT aceptaban tokens con `"alg": "none"` --un algoritmo que significa "sin firma". Un atacante podia:

1. Tomar un JWT valido.
2. Cambiar el header a `{"alg": "none"}`.
3. Modificar el payload a voluntad.
4. Eliminar la firma.
5. El servidor aceptaba el token como valido.

La vulnerabilidad existia porque las librerias usaban el campo `alg` del token recibido (controlado por el atacante) para decidir como verificar, en lugar de usar una configuracion del servidor [McLean, 2015].

```python
"""
jwt_alg_none_demo.py

Demuestra conceptualmente el ataque "alg: none" contra JWT.
Solo para fines educativos.
"""

import base64
import json
import hmac
import hashlib


def base64url_encode(datos: bytes) -> str:
    """Codifica en Base64 URL-safe sin padding."""
    return base64.urlsafe_b64encode(datos).rstrip(b"=").decode()


def base64url_decode(s: str) -> bytes:
    """Decodifica Base64 URL-safe."""
    s += "=" * (4 - len(s) % 4)
    return base64.urlsafe_b64decode(s)


def crear_jwt(payload: dict, secreto: bytes,
              algoritmo: str = "HS256") -> str:
    """Crea un JWT firmado con HMAC-SHA-256."""
    header = {"alg": algoritmo, "typ": "JWT"}
    h = base64url_encode(json.dumps(header).encode())
    p = base64url_encode(json.dumps(payload).encode())

    if algoritmo == "none":
        return f"{h}.{p}."

    firma = hmac.new(
        secreto, f"{h}.{p}".encode(), hashlib.sha256
    ).digest()
    s = base64url_encode(firma)
    return f"{h}.{p}.{s}"


def verificar_jwt_VULNERABLE(token: str, secreto: bytes) -> dict:
    """
    VULNERABLE: confía en el campo 'alg' del token.
    Un atacante puede enviar alg=none para saltarse la verificacion.
    """
    partes = token.split(".")
    header = json.loads(base64url_decode(partes[0]))
    payload = json.loads(base64url_decode(partes[1]))

    if header.get("alg") == "none":
        # Libreria vulnerable: acepta sin firma!
        return payload

    firma = base64url_decode(partes[2])
    firma_esperada = hmac.new(
        secreto, f"{partes[0]}.{partes[1]}".encode(), hashlib.sha256
    ).digest()

    if hmac.compare_digest(firma, firma_esperada):
        return payload
    raise ValueError("Firma invalida")


def verificar_jwt_SEGURO(token: str, secreto: bytes,
                          algoritmo_esperado: str = "HS256") -> dict:
    """
    SEGURO: ignora el campo 'alg' del token y usa la
    configuracion del servidor.
    """
    partes = token.split(".")
    header = json.loads(base64url_decode(partes[0]))

    # CRITICO: verificar que el algoritmo sea el esperado
    if header.get("alg") != algoritmo_esperado:
        raise ValueError(
            f"Algoritmo inesperado: {header.get('alg')} "
            f"(esperado: {algoritmo_esperado})"
        )

    if len(partes) < 3 or not partes[2]:
        raise ValueError("Token sin firma")

    firma = base64url_decode(partes[2])
    firma_esperada = hmac.new(
        secreto, f"{partes[0]}.{partes[1]}".encode(), hashlib.sha256
    ).digest()

    if not hmac.compare_digest(firma, firma_esperada):
        raise ValueError("Firma invalida")

    return json.loads(base64url_decode(partes[1]))


# --- Demo ---
secreto = b"mi_secreto_jwt_super_seguro_de_256_bits!"

# Token legitimo
token_valido = crear_jwt(
    {"sub": "user123", "admin": False},
    secreto
)
print("=== JWT y el ataque 'alg: none' ===\n")
print(f"Token valido: {token_valido[:50]}...")

# Verificacion correcta
payload = verificar_jwt_SEGURO(token_valido, secreto)
print(f"Payload: {payload}")

# Atacante crea token con alg=none y admin=True
token_atacante = crear_jwt(
    {"sub": "user123", "admin": True},
    b"",  # Sin secreto
    algoritmo="none"
)
print(f"\nToken del atacante: {token_atacante[:50]}...")

# Verificacion VULNERABLE (acepta el token falso!)
payload_falso = verificar_jwt_VULNERABLE(token_atacante, secreto)
print(f"Vulnerable acepta: {payload_falso}")
print(f"Admin = {payload_falso['admin']}  (falsificado!)")

# Verificacion SEGURA (rechaza el token)
try:
    verificar_jwt_SEGURO(token_atacante, secreto)
except ValueError as e:
    print(f"\nSeguro rechaza: {e}")

print(f"\nREGLA: NUNCA confies en el campo 'alg' del JWT.")
print(f"El servidor debe imponer el algoritmo esperado.")
```

---

## 10.7 Ejercicio integrador: API firmada con HMAC y proteccion completa

```python
"""
ejercicio_cap10_api_firmada.py

Ejercicio integrador del Capitulo 10.

Objetivos:
1. Implementar firmado HMAC-SHA-256 de requests HTTP.
2. Verificar con comparacion constant-time.
3. Proteger contra replay attacks con timestamps y nonces.
4. Demostrar timing attack contra comparacion ingenua.
5. Migrar a cifrado autenticado con ChaCha20-Poly1305.

Prerequisitos:
  pip install cryptography
"""

import os
import hmac
import hashlib
import json
import time
import secrets
from typing import Optional
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


# ============================================================
# Parte 1: Cliente y servidor con HMAC-SHA-256
# ============================================================

print("=" * 65)
print("PARTE 1: API firmada con HMAC-SHA-256")
print("=" * 65)


class ClienteAPI:
    """Cliente que firma requests con HMAC-SHA-256."""

    def __init__(self, api_key: str, api_secret: bytes):
        self.api_key = api_key
        self.api_secret = api_secret

    def firmar_request(self, metodo: str, path: str,
                        body: str = "") -> dict:
        """
        Firma un request HTTP.
        Incluye timestamp y nonce para proteccion anti-replay.
        """
        timestamp = str(int(time.time()))
        nonce = secrets.token_hex(16)

        # Mensaje a firmar: metodo + path + body + timestamp + nonce
        mensaje = f"{metodo}\n{path}\n{body}\n{timestamp}\n{nonce}"

        firma = hmac.new(
            self.api_secret,
            mensaje.encode(),
            hashlib.sha256
        ).hexdigest()

        return {
            "method": metodo,
            "path": path,
            "body": body,
            "headers": {
                "X-API-Key": self.api_key,
                "X-Timestamp": timestamp,
                "X-Nonce": nonce,
                "X-Signature": firma,
            }
        }


class ServidorAPI:
    """Servidor que verifica firmas HMAC-SHA-256."""

    def __init__(self, ventana_segundos: int = 300):
        self.clientes: dict[str, bytes] = {}
        self.nonces_usados: set[str] = set()
        self.ventana = ventana_segundos

    def registrar_cliente(self, api_key: str, api_secret: bytes):
        """Registra un cliente con su secreto."""
        self.clientes[api_key] = api_secret

    def verificar_request(self, request: dict) -> tuple[bool, str]:
        """
        Verifica un request firmado.
        Retorna (valido, razon).
        """
        headers = request["headers"]
        api_key = headers.get("X-API-Key", "")
        timestamp = headers.get("X-Timestamp", "")
        nonce = headers.get("X-Nonce", "")
        firma_recibida = headers.get("X-Signature", "")

        # 1. Verificar que el cliente existe
        if api_key not in self.clientes:
            return False, "Cliente desconocido"

        # 2. Verificar timestamp (proteccion contra replay)
        try:
            ts = int(timestamp)
            ahora = int(time.time())
            if abs(ahora - ts) > self.ventana:
                return False, f"Timestamp expirado (diferencia: {abs(ahora-ts)}s)"
        except ValueError:
            return False, "Timestamp invalido"

        # 3. Verificar nonce (proteccion contra replay exacto)
        if nonce in self.nonces_usados:
            return False, "Nonce reutilizado (replay detectado)"

        # 4. Recalcular la firma
        secreto = self.clientes[api_key]
        mensaje = (f"{request['method']}\n{request['path']}\n"
                   f"{request['body']}\n{timestamp}\n{nonce}")

        firma_esperada = hmac.new(
            secreto,
            mensaje.encode(),
            hashlib.sha256
        ).hexdigest()

        # 5. Comparacion CONSTANT-TIME (critico!)
        if not hmac.compare_digest(firma_esperada, firma_recibida):
            return False, "Firma invalida"

        # 6. Todo OK: registrar nonce como usado
        self.nonces_usados.add(nonce)
        return True, "Autenticado"


# --- Demo ---

# Setup
api_key = "cliente_001"
api_secret = os.urandom(32)

cliente = ClienteAPI(api_key, api_secret)
servidor = ServidorAPI()
servidor.registrar_cliente(api_key, api_secret)

# Request valido
request = cliente.firmar_request("POST", "/api/transferir",
                                  '{"monto": 500, "destino": "cuenta_xyz"}')
valido, razon = servidor.verificar_request(request)
print(f"\nRequest valido:     {valido} ({razon})")

# Replay del mismo request
valido, razon = servidor.verificar_request(request)
print(f"Replay:             {valido} ({razon})")

# Request con body alterado
request_falso = cliente.firmar_request("POST", "/api/transferir",
                                        '{"monto": 500}')
# Alterar el body despues de firmar
request_falso["body"] = '{"monto": 99999}'
valido, razon = servidor.verificar_request(request_falso)
print(f"Body alterado:      {valido} ({razon})")

# Request nuevo valido
request2 = cliente.firmar_request("GET", "/api/saldo", "")
valido, razon = servidor.verificar_request(request2)
print(f"Request nuevo:      {valido} ({razon})")


# ============================================================
# Parte 2: Timing attack contra comparacion ingenua
# ============================================================

print("\n\n" + "=" * 65)
print("PARTE 2: Timing attack contra comparacion ingenua")
print("=" * 65)


def verificar_firma_INSEGURA(firma_esperada: str,
                              firma_recibida: str) -> bool:
    """VULNERABLE: retorna False en el primer caracter diferente."""
    if len(firma_esperada) != len(firma_recibida):
        return False
    for a, b in zip(firma_esperada, firma_recibida):
        if a != b:
            return False
    return True


def verificar_firma_SEGURA(firma_esperada: str,
                            firma_recibida: str) -> bool:
    """SEGURA: siempre compara todos los caracteres."""
    return hmac.compare_digest(firma_esperada, firma_recibida)


# Simular timing attack
firma_real = hmac.new(
    api_secret, b"datos", hashlib.sha256
).hexdigest()

print(f"\nFirma real: {firma_real[:32]}...")

# Medir tiempos con diferente numero de caracteres correctos
hexchars = "0123456789abcdef"
print(f"\n{'Chars correctos':>15} | {'== (ms)':>10} | {'compare_digest (ms)':>20}")
print("-" * 55)

for n_correctos in [0, 8, 16, 32, 48, 64]:
    firma_parcial = firma_real[:n_correctos] + "0" * (64 - n_correctos)

    repeticiones = 50_000

    inicio = time.perf_counter()
    for _ in range(repeticiones):
        verificar_firma_INSEGURA(firma_real, firma_parcial)
    t_insegura = (time.perf_counter() - inicio) * 1000

    inicio = time.perf_counter()
    for _ in range(repeticiones):
        verificar_firma_SEGURA(firma_real, firma_parcial)
    t_segura = (time.perf_counter() - inicio) * 1000

    print(f"{n_correctos:>15} | {t_insegura:>10.3f} | {t_segura:>20.3f}")


# ============================================================
# Parte 3: Migracion a cifrado autenticado (AEAD)
# ============================================================

print("\n\n" + "=" * 65)
print("PARTE 3: Migracion a cifrado autenticado (ChaCha20-Poly1305)")
print("=" * 65)


class ClienteAPISeguro:
    """Cliente con cifrado autenticado de payloads."""

    def __init__(self, api_key: str, llave_cifrado: bytes,
                 llave_firma: bytes):
        self.api_key = api_key
        self.llave_firma = llave_firma
        self.chacha = ChaCha20Poly1305(llave_cifrado)

    def enviar_request(self, metodo: str, path: str,
                        body: dict) -> dict:
        """Cifra y autentica el payload completo."""
        timestamp = str(int(time.time()))
        nonce_firma = secrets.token_hex(16)
        nonce_cifrado = os.urandom(12)

        # Cifrar el body con datos asociados
        body_bytes = json.dumps(body).encode()
        datos_asociados = f"{metodo}|{path}|{timestamp}".encode()

        cifrado = self.chacha.encrypt(
            nonce_cifrado, body_bytes, datos_asociados
        )

        # Firmar todo el request (metadatos + cifrado)
        mensaje_firma = (f"{metodo}\n{path}\n{timestamp}\n"
                         f"{nonce_firma}\n{cifrado.hex()}")
        firma = hmac.new(
            self.llave_firma,
            mensaje_firma.encode(),
            hashlib.sha256
        ).hexdigest()

        return {
            "method": metodo,
            "path": path,
            "headers": {
                "X-API-Key": self.api_key,
                "X-Timestamp": timestamp,
                "X-Nonce": nonce_firma,
                "X-Encryption-Nonce": nonce_cifrado.hex(),
                "X-Signature": firma,
            },
            "body_cifrado": cifrado.hex(),
        }


class ServidorAPISeguro:
    """Servidor con descifrado autenticado."""

    def __init__(self):
        self.clientes: dict[str, dict] = {}
        self.nonces_usados: set[str] = set()

    def registrar_cliente(self, api_key: str, llave_cifrado: bytes,
                          llave_firma: bytes):
        self.clientes[api_key] = {
            "chacha": ChaCha20Poly1305(llave_cifrado),
            "llave_firma": llave_firma,
        }

    def procesar_request(self, request: dict) -> tuple[bool, str, Optional[dict]]:
        """Verifica firma, descifra body, retorna payload."""
        headers = request["headers"]
        api_key = headers.get("X-API-Key", "")

        if api_key not in self.clientes:
            return False, "Cliente desconocido", None

        config = self.clientes[api_key]

        # Verificar timestamp
        ts = int(headers["X-Timestamp"])
        if abs(int(time.time()) - ts) > 300:
            return False, "Timestamp expirado", None

        # Verificar nonce
        if headers["X-Nonce"] in self.nonces_usados:
            return False, "Replay detectado", None

        # Verificar firma HMAC
        mensaje_firma = (f"{request['method']}\n{request['path']}\n"
                         f"{headers['X-Timestamp']}\n{headers['X-Nonce']}\n"
                         f"{request['body_cifrado']}")
        firma_esperada = hmac.new(
            config["llave_firma"],
            mensaje_firma.encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(firma_esperada, headers["X-Signature"]):
            return False, "Firma invalida", None

        # Descifrar body (ChaCha20-Poly1305 verifica integridad)
        nonce_cifrado = bytes.fromhex(headers["X-Encryption-Nonce"])
        cifrado = bytes.fromhex(request["body_cifrado"])
        datos_asociados = (f"{request['method']}|{request['path']}|"
                           f"{headers['X-Timestamp']}").encode()

        try:
            body_bytes = config["chacha"].decrypt(
                nonce_cifrado, cifrado, datos_asociados
            )
        except Exception:
            return False, "Descifrado fallido (integridad violada)", None

        self.nonces_usados.add(headers["X-Nonce"])
        payload = json.loads(body_bytes)
        return True, "OK", payload


# --- Demo ---

api_key = "cliente_seguro_001"
llave_cifrado = ChaCha20Poly1305.generate_key()
llave_firma = os.urandom(32)

cliente_seguro = ClienteAPISeguro(api_key, llave_cifrado, llave_firma)
servidor_seguro = ServidorAPISeguro()
servidor_seguro.registrar_cliente(api_key, llave_cifrado, llave_firma)

# Enviar request cifrado y firmado
request = cliente_seguro.enviar_request(
    "POST", "/api/transferir",
    {"monto": 5000, "destino": "cuenta_xyz", "moneda": "MXN"}
)

print(f"\nBody cifrado: {request['body_cifrado'][:60]}...")
print(f"Firma:        {request['headers']['X-Signature'][:40]}...")

valido, razon, payload = servidor_seguro.procesar_request(request)
print(f"\nVerificacion: {valido} ({razon})")
if payload:
    print(f"Payload descifrado: {json.dumps(payload, indent=2)}")

# Intentar replay
valido, razon, _ = servidor_seguro.procesar_request(request)
print(f"\nReplay: {valido} ({razon})")


print("\n\n=== Ejercicio completado ===")
```

**Extensiones sugeridas:**

1. Implementa un esquema de rotacion de llaves: cada N mensajes o cada T segundos, el cliente y el servidor derivan una nueva llave HMAC a partir de la anterior usando HKDF (que veremos en capitulos posteriores).

2. Agrega soporte para multiples algoritmos de firma (HMAC-SHA-256, HMAC-SHA-512, HMAC-SHA-3-256) y un mecanismo seguro de negociacion del algoritmo (que no sea vulnerable al ataque "alg: none" de JWT).

3. Implementa un servicio de verificacion de webhooks compatible con GitHub, Stripe o Slack. Consulta su documentacion y verifica webhooks reales.

4. Mide cuantos requests por segundo puede verificar tu servidor con HMAC-SHA-256 vs ChaCha20-Poly1305 completo. Usa `timeit` para un benchmark riguroso.

5. Investiga la construccion KMAC (KECCAK Message Authentication Code), estandarizada en NIST SP 800-185. Implementala usando SHA-3 y compara con HMAC-SHA-256.

---

## Resumen del capitulo

| Concepto | Lo esencial |
|----------|-------------|
| MAC | Funcion con llave que produce un tag de tamano fijo. Protege integridad y autenticidad. |
| HMAC | MAC basado en hash. Doble hash con ipad/opad. Estandar universal (RFC 2104). |
| CMAC | MAC basado en cifrado de bloque (AES). Usado en WiFi WPA2, Bluetooth. |
| Poly1305 | MAC ultrarapido basado en evaluacion de polinomio. Requiere llave unica por mensaje. |
| Encrypt-then-MAC | Cifra primero, luego MAC del cifrado. Unico patron probado como seguro. |
| MAC-then-Encrypt | MAC del plano, cifra todo. Vulnerable a padding oracle. Evitar. |
| AEAD | Cifrado autenticado integrado. AES-GCM, ChaCha20-Poly1305. La solucion moderna. |
| compare_digest | Comparacion en tiempo constante. SIEMPRE usar para verificar tags y firmas. |
| Timing attack | Ataque que mide tiempo de comparacion para adivinar el tag byte por byte. |

**Takeaway:** Nunca cifres sin autenticar. La confidencialidad sin integridad es una invitacion a que el atacante manipule tus datos cifrados. HMAC-SHA-256 es el estandar universal para autenticacion de mensajes. Pero la mejor solucion es usar AEAD (AES-GCM o ChaCha20-Poly1305), que combina cifrado y autenticacion en una sola operacion atomica, eliminando la posibilidad de error en la composicion.

---

## Referencias del capitulo

- [Bellare, Canetti, Krawczyk, 1996] Bellare, M., Canetti, R., Krawczyk, H. "Keying Hash Functions for Message Authentication." CRYPTO 1996. RFC 2104 (1997).
- [Bellare, 2006] Bellare, M. "New Proofs for NMAC and HMAC: Security Without Collision-Resistance." CRYPTO 2006.
- [Krawczyk, 2001] Krawczyk, H. "The Order of Encryption and Authentication for Protecting Communications." CRYPTO 2001.
- [Vaudenay, 2002] Vaudenay, S. "Security Flaws Induced by CBC Padding -- Applications to SSL, IPSEC, WTLS..." EUROCRYPT 2002.
- [Bernstein, 2005] Bernstein, D.J. "The Poly1305-AES message-authentication code." FSE 2005.
- [Aumasson, Bernstein, 2012] Aumasson, J.P., Bernstein, D.J. "SipHash: a fast short-input PRF." INDOCRYPT 2012.
- [NIST SP 800-38B] Dworkin, M. "Recommendation for Block Cipher Modes of Operation: The CMAC Mode for Authentication." 2005.
- [Green et al., 2016] Green, M., et al. "Dancing on the Lip of the Volcano: Chosen Ciphertext Attacks on Apple iMessage." USENIX Security 2016.
- [Lawson, 2009] Lawson, N. "Timing attack in Google Keyczar library." Root Labs, 2009.
- [McLean, 2015] McLean, T. "Critical vulnerabilities in JSON Web Token libraries." Auth0, 2015.
- [RFC 7366] Gutmann, P. "Encrypt-then-MAC for Transport Layer Security (TLS) and Datagram Transport Layer Security (DTLS)." 2014.
