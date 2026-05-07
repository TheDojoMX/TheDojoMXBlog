# Capitulo 8: Cifrados de flujo -- protege datos en movimiento

> "Si no sabes el tamano de lo que vas a cifrar, necesitas un cifrado de flujo. Y si lo sabes, probablemente tambien te convenga uno."

---

En 2001, investigadores descubrieron que las comunicaciones WiFi protegidas con WEP podian descifrarse en minutos. La causa: un cifrado de flujo llamado RC4 con una implementacion que reutilizaba vectores de inicializacion. Millones de redes domesticas y corporativas quedaron expuestas de la noche a la manana. No porque RC4 fuera un mal algoritmo --era debatible en ese momento--, sino porque la forma en que WEP lo usaba violaba las reglas fundamentales de los cifrados de flujo [Fluhrer, Mantin, Shamir, 2001].

Quince anos despues, un cifrado de flujo disenado por un solo criptografo --Daniel J. Bernstein-- protege una fraccion significativa del trafico de internet. ChaCha20-Poly1305 esta en TLS, en WireGuard, en SSH, en Android, en Chrome. Su adopcion demuestra que los cifrados de flujo no son reliquias del pasado: son herramientas modernas, elegantes, y en muchos contextos **mas rapidas** que AES.

Este capitulo explica como funcionan los cifrados de flujo, por que RC4 fallo, como ChaCha20 triunfo, y cuando elegir uno u otro.

---

## 8.1 Cifrados de flujo: cifrar bit a bit

### 8.1.1 Definicion y contraste con cifrados de bloque

En el capitulo anterior vimos que un cifrado de bloque toma un bloque de tamano fijo y produce un bloque cifrado del mismo tamano. Para cifrar datos mas grandes, necesitas modos de operacion.

Un cifrado de flujo toma un enfoque diferente: genera un flujo continuo de bits pseudo-aleatorios llamado **keystream** y lo combina con el texto plano mediante XOR, bit a bit.

```
Llave + Nonce
      |
      v
+-------------+
| Generador   |
| de          |---> Keystream: k0 k1 k2 k3 k4 k5 k6 k7 ...
| keystream   |
+-------------+

Texto plano:     p0 p1 p2 p3 p4 p5 p6 p7 ...
                 |  |  |  |  |  |  |  |
                XOR XOR XOR XOR XOR XOR XOR XOR
                 |  |  |  |  |  |  |  |
Texto cifrado:  c0 c1 c2 c3 c4 c5 c6 c7 ...

Para descifrar: aplicar XOR de nuevo con el mismo keystream.
ci XOR ki = (pi XOR ki) XOR ki = pi
```

Las ventajas sobre los cifrados de bloque son claras:

1. **No requieren padding**: la operacion XOR funciona con cualquier tamano. Si tu mensaje tiene 137 bytes, produces 137 bytes de keystream y obtienes 137 bytes de texto cifrado. Sin relleno, sin desperdicios.

2. **Procesamiento en tiempo real**: puedes cifrar datos conforme llegan, sin esperar a acumular un bloque completo. Ideal para streaming de audio, video, o comunicaciones en tiempo real.

3. **Simplicidad de implementacion**: la complejidad se concentra en el generador de keystream. La operacion de cifrado en si es un simple XOR.

### 8.1.2 Estado interno vs contador

Los cifrados de flujo se dividen en dos familias segun como generan el keystream:

**Cifrados con estado interno**: despues de inicializarse con una llave y un nonce, mantienen un estado secreto que se actualiza en cada byte o bloque generado. El proximo byte del keystream depende del estado actual, que depende de todos los bytes anteriores.

```
Inicializacion: Estado_0 = f(Llave, Nonce)

Generacion:
  Estado_1 = g(Estado_0) --> keystream_0
  Estado_2 = g(Estado_1) --> keystream_1
  Estado_3 = g(Estado_2) --> keystream_2
  ...
```

RC4 es el ejemplo clasico de esta familia. Su desventaja: no puedes saltar al byte numero 1,000,000 sin generar todos los anteriores, y no puedes paralelizar la generacion.

**Cifrados con contador**: reciben la llave, un nonce y un numero de contador. El keystream para cada posicion depende solo de estos tres valores, no del estado previo.

```
keystream_0 = F(Llave, Nonce, contador=0)
keystream_1 = F(Llave, Nonce, contador=1)
keystream_2 = F(Llave, Nonce, contador=2)
...

Cada bloque es independiente: acceso aleatorio y paralelizable.
```

Salsa20 y ChaCha20 pertenecen a esta familia. Las ventajas son enormes: puedes descifrar cualquier posicion sin procesar las anteriores (acceso aleatorio), y puedes generar multiples bloques de keystream en paralelo.

De hecho, un cifrado de bloque en modo CTR es esencialmente un cifrado de flujo con contador. Como lo describio JP Aumasson, autor de "Serious Cryptography": es un cifrado de bloque disfrazado de cifrado de flujo.

### 8.1.3 Cuando usar cifrados de flujo

Los cifrados de flujo son la eleccion natural en estos escenarios:

- **Streaming de datos**: video cifrado, audio en tiempo real, telemetria de sensores IoT. Los datos llegan continuamente y no puedes esperar a tener un bloque completo.

- **Protocolos de red**: TLS, WireGuard, SSH. Los paquetes tienen tamanos variables y el overhead de padding es indeseable.

- **Dispositivos con recursos limitados**: microcontroladores y sensores IoT donde la memoria es escasa y no hay instrucciones AES-NI.

- **Software puro**: cuando tu procesador no tiene aceleracion por hardware para AES, un cifrado de flujo como ChaCha20 puede ser significativamente mas rapido.

---

## 8.2 El keystream: la cadena pseudo-aleatoria que lo hace posible

Antes de ver algoritmos especificos, entendamos que hace bueno a un keystream.

Un keystream ideal seria una secuencia verdaderamente aleatoria de la misma longitud que el mensaje --el one-time pad de Vernam que vimos en el capitulo 2. Pero generar y distribuir tanta aleatoriedad real es impracticable. Un cifrado de flujo usa una llave corta (128 o 256 bits) para generar un keystream **pseudo-aleatorio** que es computacionalmente indistinguible de la aleatoriedad verdadera.

"Computacionalmente indistinguible" significa que ningun algoritmo que se ejecute en tiempo razonable puede distinguir el keystream de bits verdaderamente aleatorios con probabilidad significativamente mayor que 50%. Si pudiera distinguirlos, podria usarse para extraer informacion sobre la llave.

Las propiedades criticas de un buen keystream:

1. **Distribucion uniforme**: cada bit tiene probabilidad 50% de ser 0 o 1.
2. **Independencia aparente**: conocer N bits del keystream no te da informacion sobre el bit N+1.
3. **Periodo largo**: el keystream no debe repetirse antes de 2^64 bytes como minimo.
4. **Dependencia de la llave**: cambiar un bit de la llave debe cambiar ~50% de los bits del keystream.
5. **Dependencia del nonce**: cambiar el nonce debe producir un keystream completamente diferente.

Veamos la demostracion mas basica de un cifrado de flujo:

```python
"""
cifrado_flujo_basico.py

Demostracion del principio fundamental de un cifrado de flujo:
keystream XOR texto plano = texto cifrado.
"""

import os


def cifrado_xor_simple(datos: bytes, keystream: bytes) -> bytes:
    """XOR byte a byte entre datos y keystream."""
    return bytes(d ^ k for d, k in zip(datos, keystream))


# Generar un keystream pseudo-aleatorio (simulando lo que hace un cifrado real)
llave_semilla = os.urandom(32)

# En un cifrado de flujo real, el keystream se genera deterministicamente
# a partir de la llave y el nonce. Aqui simplificamos.
mensaje = b"Los cifrados de flujo cifran bit a bit con XOR"
keystream = os.urandom(len(mensaje))

# Cifrar
cifrado = cifrado_xor_simple(mensaje, keystream)
print(f"Mensaje:   {mensaje}")
print(f"Cifrado:   {cifrado.hex()[:60]}...")

# Descifrar: mismo keystream, mismo XOR
descifrado = cifrado_xor_simple(cifrado, keystream)
print(f"Descifrad: {descifrado}")
assert descifrado == mensaje

# --- Demostrar por que reutilizar el keystream es fatal ---
print("\n--- Peligro: reutilizacion de keystream ---")
mensaje2 = b"Este es otro mensaje con el mismo keystream!!"
cifrado2 = cifrado_xor_simple(mensaje2, keystream[:len(mensaje2)])

# Si un atacante tiene ambos textos cifrados...
# c1 XOR c2 = (m1 XOR ks) XOR (m2 XOR ks) = m1 XOR m2
xor_mensajes = bytes(
    c1 ^ c2 for c1, c2 in zip(cifrado[:len(mensaje2)], cifrado2)
)

# El atacante obtiene el XOR de los mensajes en claro
# Con analisis de frecuencia puede reconstruir ambos
print(f"c1 XOR c2: {xor_mensajes.hex()[:60]}...")
print(f"m1 XOR m2: {bytes(a ^ b for a, b in zip(mensaje[:len(mensaje2)], mensaje2)).hex()[:60]}...")
print("Son identicos! El atacante obtiene m1 XOR m2 sin conocer la llave.")
```

---

## 8.3 RC4: la leccion de lo que pasa cuando un cifrado se usa demasiado

### 8.3.1 Diseno y popularidad

RC4 fue disenado por Ron Rivest en 1987 para RSA Security. "RC" significaba originalmente "Ron's Code". El algoritmo era propietario, pero en 1994 su codigo fuente se filtro de forma anonima en una lista de correo, y se convirtio en el cifrado de flujo mas usado del mundo.

La razon de su popularidad era su simplicidad extrema: el nucleo del algoritmo cabe en unas pocas lineas de codigo y usa solo operaciones de bytes --sumas, intercambios, indices en un arreglo de 256 bytes.

```python
"""
rc4_demo.py

Implementacion educativa de RC4.
NO USAR EN PRODUCCION -- RC4 esta completamente roto.
"""


def rc4_keystream(llave: bytes, longitud: int) -> bytes:
    """
    Genera 'longitud' bytes de keystream RC4.
    SOLO PARA FINES EDUCATIVOS.
    """
    # Inicializacion del estado (KSA: Key Scheduling Algorithm)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + llave[i % len(llave)]) % 256
        S[i], S[j] = S[j], S[i]

    # Generacion del keystream (PRGA: Pseudo-Random Generation Algorithm)
    keystream = bytearray()
    i = j = 0
    for _ in range(longitud):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        k = S[(S[i] + S[j]) % 256]
        keystream.append(k)

    return bytes(keystream)


# Demostracion
llave = b"llave_secreta"
mensaje = b"Hola mundo con RC4"

keystream = rc4_keystream(llave, len(mensaje))
cifrado = bytes(m ^ k for m, k in zip(mensaje, keystream))
print(f"Cifrado (hex): {cifrado.hex()}")

# Descifrar: generar el mismo keystream
keystream2 = rc4_keystream(llave, len(mensaje))
descifrado = bytes(c ^ k for c, k in zip(cifrado, keystream2))
print(f"Descifrado:    {descifrado.decode()}")
```

RC4 se uso en:

- **WEP** (1997): proteccion de redes WiFi
- **WPA-TKIP** (2003): sucesor temporal de WEP
- **SSL/TLS**: como cifrado de flujo preferido durante anos
- **Microsoft PPTP**: protocolo VPN
- **Kerberos**: autenticacion en redes Windows

### 8.3.2 La cadena de ataques

La caida de RC4 fue lenta pero inevitable:

**2001 -- Ataque FMS contra WEP**: Scott Fluhrer, Itsik Mantin y Adi Shamir descubrieron que los primeros bytes del keystream de RC4 tienen sesgos estadisticos. Si el nonce y la llave se concatenan directamente (como hacia WEP), un atacante que capture suficientes paquetes puede reconstruir la llave. WEP podia romperse en minutos con herramientas como `aircrack-ng` [Fluhrer, Mantin, Shamir, 2001].

**2005 -- Ataque de Klein**: Andreas Klein encontro correlaciones adicionales entre el keystream y la llave, haciendo el ataque aun mas eficiente. Erik Tews y colaboradores crearon `aircrack-ptw`, que rompia WEP con 128 bits de llave en menos de un minuto capturando 40,000 paquetes [Klein, 2005; Tews, Weinmann, Pychkine, 2007].

**2013 -- Ataques contra RC4 en TLS**: investigadores demostraron que los sesgos estadisticos de RC4 podian explotarse para descifrar cookies de sesion en TLS. El ataque requeria capturar millones de conexiones cifradas con la misma cookie, pero era practicable en escenarios reales [AlFardan, Bernstein, Paterson, Poettering, Schuldt, 2013].

**2015 -- RC4 NOMORE**: Mathy Vanhoef y Frank Piessens demostraron un ataque practico que podia descifrar cookies en HTTPS usando RC4 en aproximadamente 52 horas, y en WPA-TKIP en una hora [Vanhoef, Piessens, 2015].

**2015 -- Prohibicion oficial**: la IETF publico el RFC 7465, prohibiendo formalmente el uso de RC4 en todas las versiones de TLS. NIST siguio con una prohibicion similar. Los principales navegadores dejaron de soportar RC4.

**[PELIGRO]** RC4 esta completamente roto. No lo uses bajo ninguna circunstancia. Si encuentras un sistema que todavia lo use --un router con WEP, un servidor TLS antiguo--, es un riesgo de seguridad critico.

### 8.3.3 Lecciones de RC4

La historia de RC4 deja lecciones importantes:

1. **Los sesgos pequenos importan**. Los primeros bytes del keystream de RC4 tienen sesgos estadisticos minusculos. Individualmente insignificantes. Pero con suficientes muestras, se convierten en ataques practicos.

2. **El uso incorrecto acelera la muerte**. RC4 como algoritmo tenia debilidades, pero WEP hizo todo lo posible por amplificarlas: nonces cortos que se reutilizaban, concatenacion directa con la llave, sin autenticacion.

3. **La depreciacion tarda demasiado**. Desde los primeros ataques en 2001 hasta la prohibicion formal en 2015 pasaron 14 anos. Millones de dispositivos siguieron vulnerables durante todo ese tiempo.

---

## 8.4 Salsa20 y ChaCha20: la alternativa moderna

### 8.4.1 Salsa20: el diseno de Bernstein

En 2005, Daniel J. Bernstein --un criptografo y matematico conocido por su enfoque minimalista y su escepticismo hacia los estandares gubernamentales-- publico Salsa20, un cifrado de flujo basado en contador con un diseno radicalmente diferente a RC4.

Salsa20 organiza su estado interno como una matriz de 4x4 palabras de 32 bits (512 bits en total):

```
Estado inicial de Salsa20 (16 palabras de 32 bits):

+----------+----------+----------+----------+
| "expa"   | Llave[0] | Llave[1] | Llave[2] |
+----------+----------+----------+----------+
| Llave[3] | "nd 3"   | Nonce[0] | Nonce[1] |
+----------+----------+----------+----------+
| Contador | Contador | "2-by"   | Llave[4] |
+----------+----------+----------+----------+
| Llave[5] | Llave[6] | Llave[7] | "te k"   |
+----------+----------+----------+----------+

Las constantes "expand 32-byte k" ocupan las esquinas.
```

La operacion fundamental es el **quarter-round** (cuarto de ronda), que mezcla cuatro palabras usando solo tres tipos de operaciones: **suma** entera de 32 bits, **XOR**, y **rotacion** de bits. Este patron se llama **ARX** (Add-Rotate-XOR).

```
Quarter-round de Salsa20 (sobre palabras a, b, c, d):

b ^= (a + d) <<< 7
c ^= (b + a) <<< 9
d ^= (c + b) <<< 13
a ^= (d + c) <<< 18
```

El quarter-round se aplica repetidamente sobre las columnas y luego sobre las diagonales de la matriz, en un patron de 20 rondas (10 rondas de columna + 10 rondas de diagonal). Al final, la matriz resultante se suma elemento a elemento con la matriz original para producir 64 bytes de keystream.

Las variantes de rendimiento son:
- **Salsa20/20**: 20 rondas (seguridad completa)
- **Salsa20/12**: 12 rondas (recomendado por eSTREAM)
- **Salsa20/8**: 8 rondas (rapido, seguridad reducida)

Salsa20 fue seleccionado por el proyecto europeo eSTREAM como uno de los cifrados de flujo recomendados para software.

### 8.4.2 ChaCha20: la evolucion

En 2008, Bernstein publico ChaCha, una variante de Salsa20 con **mejor difusion por ronda**. La diferencia principal esta en el quarter-round:

```
Quarter-round de ChaCha20 (sobre palabras a, b, c, d):

a += b; d ^= a; d <<<= 16
c += d; b ^= c; b <<<= 12
a += b; d ^= a; d <<<= 8
c += d; b ^= c; b <<<= 7
```

La mejora clave: en Salsa20, cada palabra se actualiza una vez por quarter-round. En ChaCha20, cada palabra se actualiza **dos veces**. Esto significa que la difusion (el efecto avalancha donde un bit de cambio afecta muchos bits de salida) es significativamente mas rapida.

Ademas, ChaCha20 logra esta mejor difusion usando un registro menos que Salsa20 en implementaciones naturales, lo que puede traducirse en mejor rendimiento en ciertos procesadores.

La matriz de estado de ChaCha20:

```
Estado inicial de ChaCha20 (16 palabras de 32 bits):

+----------+----------+----------+----------+
| "expa"   | "nd 3"   | "2-by"   | "te k"   |  <- Constantes
+----------+----------+----------+----------+
| Llave[0] | Llave[1] | Llave[2] | Llave[3] |  <- Llave (128 bits)
+----------+----------+----------+----------+
| Llave[4] | Llave[5] | Llave[6] | Llave[7] |  <- Llave (128 bits)
+----------+----------+----------+----------+
| Contador | Nonce[0] | Nonce[1] | Nonce[2] |  <- Contador + Nonce
+----------+----------+----------+----------+

Nota: las constantes estan en la primera fila (en Salsa20
estaban en las esquinas).
```

Las 20 rondas se organizan como 10 iteraciones de dos fases:

```
Para cada iteracion (10 veces):

  Ronda de columnas:
    QuarterRound(estado[0], estado[4], estado[8],  estado[12])
    QuarterRound(estado[1], estado[5], estado[9],  estado[13])
    QuarterRound(estado[2], estado[6], estado[10], estado[14])
    QuarterRound(estado[3], estado[7], estado[11], estado[15])

  Ronda de diagonales:
    QuarterRound(estado[0], estado[5], estado[10], estado[15])
    QuarterRound(estado[1], estado[6], estado[11], estado[12])
    QuarterRound(estado[2], estado[7], estado[8],  estado[13])
    QuarterRound(estado[3], estado[4], estado[9],  estado[14])
```

Veamos la implementacion completa del bloque de ChaCha20:

```python
"""
chacha20_internals.py

Implementacion educativa del bloque de ChaCha20.
Muestra las operaciones internas del algoritmo.
"""

import struct


def rotar_izquierda(valor: int, bits: int) -> int:
    """Rotacion circular a la izquierda de un entero de 32 bits."""
    return ((valor << bits) | (valor >> (32 - bits))) & 0xFFFFFFFF


def quarter_round(estado: list[int], a: int, b: int, c: int, d: int) -> None:
    """
    Quarter-round de ChaCha20.
    Modifica cuatro palabras del estado in-place.
    """
    estado[a] = (estado[a] + estado[b]) & 0xFFFFFFFF
    estado[d] ^= estado[a]
    estado[d] = rotar_izquierda(estado[d], 16)

    estado[c] = (estado[c] + estado[d]) & 0xFFFFFFFF
    estado[b] ^= estado[c]
    estado[b] = rotar_izquierda(estado[b], 12)

    estado[a] = (estado[a] + estado[b]) & 0xFFFFFFFF
    estado[d] ^= estado[a]
    estado[d] = rotar_izquierda(estado[d], 8)

    estado[c] = (estado[c] + estado[d]) & 0xFFFFFFFF
    estado[b] ^= estado[c]
    estado[b] = rotar_izquierda(estado[b], 7)


def bloque_chacha20(llave: bytes, contador: int, nonce: bytes) -> bytes:
    """
    Genera un bloque de 64 bytes de keystream ChaCha20.

    llave:    32 bytes (256 bits)
    contador: entero de 32 bits
    nonce:    12 bytes (96 bits) -- version IETF (RFC 8439)
    """
    # Constantes "expand 32-byte k" en little-endian
    constantes = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]

    # Construir estado inicial
    k = struct.unpack("<8I", llave)      # 8 palabras de 32 bits
    n = struct.unpack("<3I", nonce)      # 3 palabras de 32 bits

    estado = list(constantes) + list(k) + [contador] + list(n)

    # Copiar estado original (se sumara al final)
    estado_original = estado.copy()

    # 20 rondas (10 iteraciones de columna + diagonal)
    for _ in range(10):
        # Rondas de columna
        quarter_round(estado, 0, 4,  8, 12)
        quarter_round(estado, 1, 5,  9, 13)
        quarter_round(estado, 2, 6, 10, 14)
        quarter_round(estado, 3, 7, 11, 15)
        # Rondas de diagonal
        quarter_round(estado, 0, 5, 10, 15)
        quarter_round(estado, 1, 6, 11, 12)
        quarter_round(estado, 2, 7,  8, 13)
        quarter_round(estado, 3, 4,  9, 14)

    # Sumar estado original (esto previene que las rondas sean invertibles)
    estado = [(s + o) & 0xFFFFFFFF for s, o in zip(estado, estado_original)]

    # Serializar en bytes little-endian
    return struct.pack("<16I", *estado)


# --- Demostracion ---

llave = bytes(range(32))       # Llave de prueba: 0x00..0x1f
nonce = bytes(range(12))       # Nonce de prueba: 0x00..0x0b
contador = 1

keystream = bloque_chacha20(llave, contador, nonce)
print(f"Llave (hex):     {llave.hex()}")
print(f"Nonce (hex):     {nonce.hex()}")
print(f"Contador:        {contador}")
print(f"Keystream (hex): {keystream.hex()}")
print(f"Longitud:        {len(keystream)} bytes (1 bloque)")

# Cifrar un mensaje
mensaje = b"ChaCha20 genera keystream de 64 bytes por bloque"
# Solo usar los primeros len(mensaje) bytes del keystream
cifrado = bytes(m ^ k for m, k in zip(mensaje, keystream))
print(f"\nMensaje:  {mensaje.decode()}")
print(f"Cifrado:  {cifrado.hex()}")

# Descifrar
descifrado = bytes(c ^ k for c, k in zip(cifrado, keystream))
print(f"Descifr:  {descifrado.decode()}")
```

La version IETF de ChaCha20 (RFC 8439) modifico ligeramente el diseno original de Bernstein: usa un nonce de **96 bits** y un contador de **32 bits** (en lugar de nonce de 64 bits y contador de 64 bits). Esto limita el tamano maximo de datos a 256 GB por nonce (2^32 bloques de 64 bytes), pero proporciona un nonce mas grande que reduce el riesgo de colisiones.

### 8.4.3 Salsa20 vs ChaCha20: diferencias clave

| Caracteristica | Salsa20 | ChaCha20 |
|---------------|---------|----------|
| Autor | Daniel J. Bernstein (2005) | Daniel J. Bernstein (2008) |
| Difusion por ronda | Cada palabra actualizada 1 vez | Cada palabra actualizada 2 veces |
| Registros necesarios | 17 | 16 |
| Nonce (original) | 64 bits | 64 bits |
| Nonce (IETF) | -- | 96 bits |
| Ataques conocidos | 8 de 20 rondas | 7 de 20 rondas |
| Adopcion | eSTREAM, NaCl | TLS, WireGuard, SSH |

ChaCha20 es estrictamente mejor que Salsa20 en todos los aspectos relevantes. No hay razon para elegir Salsa20 en un proyecto nuevo. La unica razon para encontrarlo es en sistemas legacy o en librerias como NaCl que lo usan por razones historicas.

### 8.4.4 AES-CTR como cifrado de flujo

Como mencionamos brevemente, cualquier cifrado de bloque en modo CTR se comporta como un cifrado de flujo. AES en modo CTR (AES-CTR) genera keystream cifrando un nonce + contador, exactamente como ChaCha20.

La diferencia: AES-CTR requiere la operacion completa de AES para cada bloque de 16 bytes, mientras que ChaCha20 genera 64 bytes por bloque. En procesadores con AES-NI, AES-CTR es extremadamente rapido. En procesadores sin AES-NI, ChaCha20 suele ganar.

---

## 8.5 ChaCha20-Poly1305: cifrado autenticado sin AES-NI

### 8.5.1 Por que necesitamos autenticacion

En el capitulo anterior aprendimos que cifrar sin autenticar es peligroso. Lo mismo aplica a los cifrados de flujo: si solo usas ChaCha20 sin autenticacion, un atacante puede modificar el texto cifrado y alterar el mensaje sin que lo detectes.

Peor aun, en un cifrado de flujo basado en XOR, el atacante tiene un poder especial: si conoce parte del texto plano (por ejemplo, un encabezado de protocolo predecible), puede calcular el keystream correspondiente y reemplazar esa parte del mensaje con lo que quiera:

```
Conocido: posiciones 0-15 del texto plano son "HTTP/1.1 200 OK\r"
Keystream: texto_cifrado[0:16] XOR "HTTP/1.1 200 OK\r"
Nuevo mensaje: keystream XOR "HTTP/1.1 301 MOV"  (redireccion!)
```

ChaCha20-Poly1305 resuelve esto combinando ChaCha20 para cifrado con **Poly1305** para autenticacion.

### 8.5.2 Poly1305: el autenticador de Bernstein

Poly1305 es un codigo de autenticacion de mensajes (MAC) disenado por Bernstein. Funciona evaluando un polinomio modulo el primo 2^130 - 5 (de ahi su nombre). Es extremadamente rapido y tiene una prueba matematica formal de seguridad.

La combinacion funciona asi:

```
Entradas:
  Llave (256 bits) + Nonce (96 bits)
  Texto plano
  Datos asociados (opcional)

Proceso:
  1. ChaCha20 genera keystream con contador=0 -> subllave Poly1305
  2. ChaCha20 genera keystream con contador=1,2,3... -> cifra el texto plano
  3. Poly1305 calcula tag sobre:
     - Datos asociados (si existen)
     - Texto cifrado
     - Longitudes de ambos

Salida:
  Texto cifrado + Tag de 128 bits (16 bytes)
```

Lo elegante: la subllave de Poly1305 se genera a partir de ChaCha20 con contador 0. Esto significa que toda la construccion depende de una sola llave y un solo nonce. No hay llaves separadas para cifrado y autenticacion.

### 8.5.3 Implementacion en Python

```python
"""
chacha20_poly1305_cifrado.py

Cifrado autenticado con ChaCha20-Poly1305 usando la libreria cryptography.
"""

import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


def cifrar_chacha20(mensaje: bytes,
                    datos_asociados: bytes | None = None
                    ) -> tuple[bytes, bytes, bytes]:
    """
    Cifra un mensaje con ChaCha20-Poly1305.

    Retorna: (llave, nonce, texto_cifrado_con_tag)
    """
    # Llave de 256 bits (32 bytes) -- unico tamano soportado
    llave = ChaCha20Poly1305.generate_key()

    # Nonce de 96 bits (12 bytes) -- tamano fijo para IETF ChaCha20
    nonce = os.urandom(12)

    # Cifrar
    chacha = ChaCha20Poly1305(llave)
    cifrado = chacha.encrypt(nonce, mensaje, datos_asociados)
    # cifrado contiene: texto_cifrado + tag (16 bytes al final)

    return llave, nonce, cifrado


def descifrar_chacha20(llave: bytes,
                       nonce: bytes,
                       cifrado: bytes,
                       datos_asociados: bytes | None = None) -> bytes:
    """
    Descifra un mensaje cifrado con ChaCha20-Poly1305.
    Lanza InvalidTag si fue modificado.
    """
    chacha = ChaCha20Poly1305(llave)
    return chacha.decrypt(nonce, cifrado, datos_asociados)


# --- Demostracion ---

mensaje = b"ChaCha20-Poly1305: cifrado autenticado rapido en software"
datos_asociados = b"protocolo:tls|version:1.3"

print("=== ChaCha20-Poly1305 ===\n")

# Cifrar
llave, nonce, cifrado = cifrar_chacha20(mensaje, datos_asociados)
print(f"Mensaje:     {mensaje.decode()}")
print(f"Llave (hex): {llave.hex()}")
print(f"Nonce (hex): {nonce.hex()}")
print(f"Cifrado:     {cifrado.hex()[:60]}...")
print(f"  Texto cifrado: {len(cifrado) - 16} bytes")
print(f"  Tag Poly1305:  16 bytes")

# Descifrar
descifrado = descifrar_chacha20(llave, nonce, cifrado, datos_asociados)
print(f"\nDescifrado:  {descifrado.decode()}")

# Verificar integridad
print("\n--- Prueba de integridad ---")
cifrado_alterado = bytearray(cifrado)
cifrado_alterado[5] ^= 0x01  # cambiar un bit

try:
    descifrar_chacha20(llave, nonce, bytes(cifrado_alterado), datos_asociados)
    print("ERROR: no detecto la alteracion!")
except Exception as e:
    print(f"Alteracion detectada: {type(e).__name__}")
```

---

## 8.6 Cuando usar AES-GCM vs ChaCha20-Poly1305

Esta es una de las decisiones mas frecuentes en criptografia aplicada. La respuesta depende del contexto:

### 8.6.1 AES-GCM es mejor cuando...

- **Tienes AES-NI disponible**: en procesadores Intel/AMD modernos (desde ~2010) y ARM con extensiones criptograficas (desde ~2016), AES-GCM es hasta 3 veces mas rapido que ChaCha20-Poly1305.
- **Necesitas el maximo rendimiento en servidores**: servidores web, proxies TLS, VPNs de alto rendimiento.
- **Compatibilidad con estandares**: AES-GCM es el estandar en la mayoria de regulaciones (FIPS 140-2, PCI-DSS).

### 8.6.2 ChaCha20-Poly1305 es mejor cuando...

- **No tienes AES-NI**: dispositivos IoT, microcontroladores, procesadores ARM antiguos sin extensiones criptograficas.
- **Software puro es la unica opcion**: entornos donde no puedes acceder a instrucciones de hardware especiales.
- **Preocupa la resistencia a timing attacks**: ChaCha20 usa solo operaciones ARX (suma, rotacion, XOR), que naturalmente se ejecutan en tiempo constante. AES en software puro es vulnerable a ataques de cache timing.
- **Necesitas nonces mas largos**: XChaCha20-Poly1305 usa nonces de 192 bits, lo que virtualmente elimina el riesgo de colision de nonces. Ideal para llaves de larga vida.

### 8.6.3 Arbol de decision

```
Tu procesador tiene AES-NI? (o ARM crypto extensions)
  |
  +-- SI --> AES-256-GCM es tu mejor opcion
  |            (excepto si necesitas nonces largos -> XChaCha20)
  |
  +-- NO --> ChaCha20-Poly1305
  |
  +-- NO SE --> Ambos son seguros. Elige el que tu framework soporte.
               En la duda, ChaCha20-Poly1305 es la opcion mas segura
               por defecto (sin riesgos de timing attacks).
```

### 8.6.4 Comparacion de rendimiento

```python
"""
benchmark_aes_vs_chacha.py

Compara el rendimiento de AES-256-GCM vs ChaCha20-Poly1305.
"""

import os
import time
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305


def benchmark(nombre: str, cifrador, llave: bytes,
              tamano_datos: int, iteraciones: int) -> float:
    """
    Ejecuta un benchmark de cifrado y retorna MB/s.
    """
    datos = os.urandom(tamano_datos)
    datos_asociados = b"benchmark"

    # Calentar (evitar efectos de cache)
    for _ in range(10):
        nonce = os.urandom(12)
        cifrador.encrypt(nonce, datos, datos_asociados)

    # Medir
    inicio = time.perf_counter()
    for _ in range(iteraciones):
        nonce = os.urandom(12)
        cifrador.encrypt(nonce, datos, datos_asociados)
    fin = time.perf_counter()

    total_bytes = tamano_datos * iteraciones
    total_segundos = fin - inicio
    mb_por_segundo = (total_bytes / 1_000_000) / total_segundos

    print(f"{nombre:>25}: {mb_por_segundo:>8.1f} MB/s "
          f"({total_segundos:.3f}s para {iteraciones} iteraciones)")
    return mb_por_segundo


print("=== Benchmark: AES-256-GCM vs ChaCha20-Poly1305 ===\n")

# Configurar
tamano = 1_000_000  # 1 MB por iteracion
iteraciones = 50

llave_aes = AESGCM.generate_key(bit_length=256)
llave_chacha = ChaCha20Poly1305.generate_key()

aes_gcm = AESGCM(llave_aes)
chacha = ChaCha20Poly1305(llave_chacha)

print(f"Datos por iteracion: {tamano:,} bytes")
print(f"Iteraciones: {iteraciones}\n")

velocidad_aes = benchmark("AES-256-GCM", aes_gcm, llave_aes,
                          tamano, iteraciones)
velocidad_chacha = benchmark("ChaCha20-Poly1305", chacha, llave_chacha,
                             tamano, iteraciones)

print()
if velocidad_aes > velocidad_chacha:
    ratio = velocidad_aes / velocidad_chacha
    print(f"AES-256-GCM es {ratio:.1f}x mas rapido en este sistema.")
    print("(Probablemente tienes AES-NI.)")
else:
    ratio = velocidad_chacha / velocidad_aes
    print(f"ChaCha20-Poly1305 es {ratio:.1f}x mas rapido en este sistema.")
    print("(Probablemente no tienes AES-NI o esta deshabilitado.)")

print("\nNota: la libreria 'cryptography' de Python usa OpenSSL internamente,")
print("que aprovecha AES-NI automaticamente si esta disponible.")
```

### 8.6.5 La situacion en 2026

Es importante notar que el panorama ha evolucionado desde los primeros anos de ChaCha20. En 2015, cuando Google promovio ChaCha20-Poly1305 para Android, la mayoria de los telefonos moviles no tenian instrucciones AES por hardware. Hoy, en 2026, practicamente todos los procesadores ARM modernos incluyen extensiones criptograficas.

Esto significa que la ventaja de rendimiento de ChaCha20 en dispositivos moviles ha disminuido considerablemente. Sin embargo, ChaCha20-Poly1305 sigue siendo relevante por:

1. **Resistencia intrinseca a timing attacks**: la implementacion en software puro es naturalmente segura contra ataques de canal lateral.
2. **XChaCha20**: la variante con nonces de 192 bits es ideal para aplicaciones que necesitan nonces largos (cifrado de disco, cifrado a nivel de aplicacion con llaves de larga duracion).
3. **Simplicidad y confianza**: el diseno es elegante, bien entendido, y ha resistido 18 anos de criptoanalisis sin ataques practicos.

TLS 1.3 soporta tanto AES-256-GCM como ChaCha20-Poly1305, y el servidor tipicamente elige segun las capacidades del cliente. WireGuard usa exclusivamente ChaCha20-Poly1305.

---

## 8.7 Aleatoriedad: el ingrediente que no puedes falsificar

### 8.7.1 Por que la aleatoriedad importa tanto para cifrados de flujo

Todo cifrado de flujo depende de que el keystream sea **indistinguible de bits aleatorios**. Si un atacante puede predecir aunque sea una porcion del keystream, puede descifrar la porcion correspondiente del mensaje.

La fuente de esta imprevisibilidad tiene dos componentes:
1. La **llave**: debe ser generada con aleatoriedad criptograficamente segura.
2. El **nonce**: debe ser unico para cada mensaje cifrado con la misma llave.

Si falla cualquiera de los dos, la seguridad se derrumba.

### 8.7.2 CSPRNG: generadores criptograficamente seguros

Para generar llaves y nonces necesitas un **CSPRNG** (Cryptographically Secure Pseudo-Random Number Generator). Estos generadores tienen dos propiedades que los distinguen de generadores normales como Mersenne Twister:

- **Forward secrecy**: conocer los bits generados hasta ahora no permite predecir los bits futuros.
- **Backward secrecy**: obtener el estado interno actual no permite reconstruir bits pasados.

Cada lenguaje de programacion tiene su fuente de aleatoriedad criptografica:

```python
"""
aleatoriedad_correcta.py

Fuentes correctas e incorrectas de aleatoriedad para criptografia.
"""

import os
import secrets

# ===== CORRECTO para criptografia =====

# 1. os.urandom(): lee de /dev/urandom (Linux/macOS) o CryptGenRandom (Windows)
llave = os.urandom(32)
print(f"os.urandom(32):    {llave.hex()}")

# 2. secrets: modulo de Python disenado para criptografia
token = secrets.token_hex(32)
nonce = secrets.token_bytes(12)
print(f"secrets.token_hex: {token}")
print(f"secrets.token_bytes: {nonce.hex()}")

# 3. secrets.choice(): seleccion aleatoria segura
import string
password = ''.join(secrets.choice(string.ascii_letters + string.digits)
                   for _ in range(20))
print(f"Password seguro:   {password}")


# ===== INCORRECTO para criptografia =====

import random

# random.random() usa Mersenne Twister: predecible con ~624 muestras
valor_inseguro = random.random()
print(f"\nrandom.random():   {valor_inseguro}  <-- NO USAR PARA CRIPTO")

# random.randbytes() tambien usa Mersenne Twister internamente
bytes_inseguros = random.randbytes(32)
print(f"random.randbytes:  {bytes_inseguros.hex()}  <-- NO USAR PARA CRIPTO")

print("""
REGLA: Para criptografia, usa SIEMPRE:
  Python:     os.urandom() o secrets
  JavaScript: crypto.getRandomValues()
  Go:         crypto/rand
  Rust:       rand::rngs::OsRng
  Java:       java.security.SecureRandom
  C/C++:      /dev/urandom o BCryptGenRandom (Windows)

NUNCA uses random(), Math.random(), rand(), o mt_rand()
para generar llaves, nonces, tokens, o cualquier valor criptografico.
""")
```

### 8.7.3 El error de Debian OpenSSL (2008)

En mayo de 2008, se descubrio que el paquete OpenSSL de Debian y Ubuntu habia tenido un generador de numeros aleatorios roto durante **dos anos**.

La historia: en 2006, un mantenedor de Debian, Kurt Roeckx, uso la herramienta Valgrind para buscar errores de memoria en OpenSSL. Valgrind reporto que dos lineas de codigo usaban memoria no inicializada. El mantenedor comento esas lineas para silenciar la advertencia.

El problema: esas dos lineas eran la fuente principal de entropia del generador aleatorio. Sin ellas, el PRNG se inicializaba unicamente con el PID del proceso --un numero entre 1 y 32,767.

El resultado catastrofico:

- Solo existian **32,767 posibles semillas** para el generador.
- Todas las llaves SSH, SSL, VPN y GPG generadas en Debian/Ubuntu entre septiembre 2006 y mayo 2008 eran predecibles.
- Un atacante podia generar las 32,767 llaves posibles y probar cada una en segundos.
- Se estimo que millones de llaves SSH en internet estaban comprometidas [Debian Security Advisory DSA-1571, 2008].

La leccion es doble:

1. **No modifiques codigo criptografico sin entenderlo completamente**. Las "anomalias" que encuentras pueden ser intencionales y criticas.
2. **La aleatoriedad no se puede inspeccionar visualmente**. Los bytes generados por el PRNG roto de Debian se veian perfectamente aleatorios. No habia forma de detectar el problema mirando la salida; solo revisando el codigo fuente.

---

## 8.8 Casos reales

### 8.8.1 PlayStation 3 ECDSA (2010): el nonce que Sony reutilizo

Este caso es tan importante que vale la pena revisarlo desde la perspectiva de los cifrados de flujo y la aleatoriedad.

Sony firmaba el firmware de la PlayStation 3 con ECDSA (Elliptic Curve Digital Signature Algorithm). Para cada firma, ECDSA requiere un valor aleatorio `k` (un nonce) que debe ser unico para cada firma con la misma llave.

Sony genero `k` una vez y lo reutilizo para todas las firmas.

Con dos firmas (s1, s2) que usen el mismo `k`, las ecuaciones se simplifican y un atacante puede despejar primero `k` y luego la llave privada. El grupo fail0verflow presento el ataque en el 27th Chaos Communication Congress en diciembre de 2010 y publico la llave privada de Sony.

El resultado: cualquiera podia firmar software para PS3 como si fuera Sony. El homebrew y la pirateria de juegos se volvieron triviales. Sony intento parchear el sistema, pero el dano estaba hecho: la llave privada estaba expuesta publicamente.

La conexion con los cifrados de flujo: en un cifrado de flujo basado en XOR, reutilizar el nonce tiene exactamente el mismo efecto --el keystream se cancela y los mensajes quedan expuestos. El principio es universal: **todo valor que debe ser unico, si se reutiliza, destruye la seguridad**.

### 8.8.2 Juniper Dual_EC_DRBG (2015): una puerta trasera en el generador

En 2015 se descubrio que Juniper Networks habia estado usando el generador de numeros pseudo-aleatorios **Dual_EC_DRBG** en sus firewalls ScreenOS.

Dual_EC_DRBG habia sido estandarizado por el NIST en 2006, pero criptografos independientes habian advertido desde 2007 que el algoritmo contenia una posible puerta trasera. Los puntos de curva eliptica usados como parametros del generador podrian haber sido elegidos por la NSA de forma que permitiera predecir la salida del generador a quien conociera la relacion secreta entre esos puntos.

En 2013, documentos filtrados por Edward Snowden confirmaron que la NSA habia promovido activamente Dual_EC_DRBG y habia pagado a RSA Security 10 millones de dolares para que lo usara como generador por defecto en su libreria BSAFE [Reuters, 2013].

El caso de Juniper fue aun peor: ademas de usar Dual_EC_DRBG, alguien (se desconoce quien) habia modificado los parametros del generador en ScreenOS, reemplazando los puntos de curva por unos diferentes. Esto significaba que quien hubiera hecho la modificacion podia descifrar todo el trafico VPN de los firewalls de Juniper.

La leccion: la procedencia y la transparencia del generador de numeros aleatorios importan tanto como su diseno matematico. Un generador con una puerta trasera es peor que no cifrar, porque proporciona una **falsa sensacion de seguridad**.

---

## 8.9 Ejercicio integrador: cifrado de streams y ataque de reutilizacion de nonce

```python
"""
ejercicio_cap8_cifrado_stream.py

Ejercicio integrador del Capitulo 8.

Objetivos:
1. Demostrar la inseguridad de un cifrado XOR con keystream fijo.
2. Ejecutar un ataque de reutilizacion de nonce.
3. Cifrar un flujo de datos en tiempo real con ChaCha20-Poly1305.
4. Comparar rendimiento de AES-256-GCM vs ChaCha20-Poly1305.

Prerequisitos:
  pip install cryptography
"""

import os
import time
from cryptography.hazmat.primitives.ciphers.aead import (
    AESGCM, ChaCha20Poly1305
)


# ---------- Parte 1: Inseguridad de XOR con keystream fijo ----------

print("=" * 65)
print("PARTE 1: Por que un keystream fijo (o reutilizado) es fatal")
print("=" * 65)

# Simular un cifrado de flujo "casero" con keystream fijo
keystream = os.urandom(100)

mensaje1 = b"TRANSFERIR $10000 A CUENTA 12345678"
mensaje2 = b"PASSWORD: mi_contrasena_secreta!!"

# Cifrar ambos con el mismo keystream (ERROR!)
cifrado1 = bytes(m ^ k for m, k in zip(mensaje1, keystream))
cifrado2 = bytes(m ^ k for m, k in zip(mensaje2, keystream))

print(f"\nMensaje 1: {mensaje1.decode()}")
print(f"Mensaje 2: {mensaje2.decode()}")
print(f"\nCifrado 1 (hex): {cifrado1.hex()}")
print(f"Cifrado 2 (hex): {cifrado2.hex()}")

# Ataque: XOR de los dos cifrados cancela el keystream
xor_cifrados = bytes(c1 ^ c2 for c1, c2 in zip(cifrado1, cifrado2))
xor_mensajes = bytes(m1 ^ m2 for m1, m2 in zip(mensaje1, mensaje2))

print(f"\nc1 XOR c2:  {xor_cifrados.hex()[:60]}...")
print(f"m1 XOR m2:  {xor_mensajes.hex()[:60]}...")
print(f"Identicos:  {xor_cifrados[:len(xor_mensajes)] == xor_mensajes}")
print("\nEl atacante obtiene m1 XOR m2 sin conocer el keystream ni la llave.")
print("Con analisis de frecuencia o texto plano parcialmente conocido,")
print("puede reconstruir ambos mensajes.")


# ---------- Parte 2: Ataque de reutilizacion de nonce ----------

print("\n" + "=" * 65)
print("PARTE 2: Ataque de reutilizacion de nonce con ChaCha20")
print("=" * 65)

# Demostrar que reutilizar el nonce es equivalente
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

llave = os.urandom(32)
nonce_repetido = os.urandom(16)  # Nonce que se "reutiliza"

# Cifrar dos mensajes con el mismo nonce (usando ChaCha20 crudo)
# Nota: usamos la API de bajo nivel para demostrar el problema.
# En produccion, SIEMPRE usa ChaCha20Poly1305 que previene esto.

cifrador1 = Cipher(
    algorithms.ChaCha20(llave, nonce_repetido),
    mode=None
).encryptor()
cifrador2 = Cipher(
    algorithms.ChaCha20(llave, nonce_repetido),  # MISMO nonce!
    mode=None
).encryptor()

m1 = b"Este mensaje es secreto y privado"
m2 = b"Otro mensaje cifrado con mismonc"

c1 = cifrador1.update(m1)
c2 = cifrador2.update(m2)

# Ataque
xor_c = bytes(a ^ b for a, b in zip(c1, c2))
xor_m = bytes(a ^ b for a, b in zip(m1, m2))

print(f"\nNonce reutilizado: {nonce_repetido.hex()}")
print(f"c1 XOR c2 == m1 XOR m2: {xor_c == xor_m}")

# Si el atacante conoce m1 (o parte), puede recuperar m2
print(f"\nSi el atacante conoce m1, recupera m2:")
m2_recuperado = bytes(a ^ b for a, b in zip(xor_c, m1))
print(f"  m2 recuperado: {m2_recuperado.decode()}")
print("  La seguridad queda COMPLETAMENTE destruida.")


# ---------- Parte 3: Cifrado correcto de un stream de datos ----------

print("\n" + "=" * 65)
print("PARTE 3: Cifrado correcto de un stream con ChaCha20-Poly1305")
print("=" * 65)


def cifrar_stream(datos_stream: list[bytes],
                  llave: bytes,
                  contexto: bytes = b"") -> list[tuple[bytes, bytes]]:
    """
    Cifra una secuencia de fragmentos de datos, cada uno con su
    propio nonce unico. Retorna lista de (nonce, cifrado).
    """
    chacha = ChaCha20Poly1305(llave)
    resultado = []
    for i, fragmento in enumerate(datos_stream):
        # Cada fragmento tiene un nonce unico
        nonce = os.urandom(12)
        # Los datos asociados incluyen el indice para prevenir reordenamiento
        datos_asociados = contexto + f"|seq:{i}".encode()
        cifrado = chacha.encrypt(nonce, fragmento, datos_asociados)
        resultado.append((nonce, cifrado))
    return resultado


def descifrar_stream(fragmentos_cifrados: list[tuple[bytes, bytes]],
                     llave: bytes,
                     contexto: bytes = b"") -> list[bytes]:
    """
    Descifra una secuencia de fragmentos cifrados.
    Verifica autenticidad e integridad de cada uno.
    """
    chacha = ChaCha20Poly1305(llave)
    resultado = []
    for i, (nonce, cifrado) in enumerate(fragmentos_cifrados):
        datos_asociados = contexto + f"|seq:{i}".encode()
        descifrado = chacha.decrypt(nonce, cifrado, datos_asociados)
        resultado.append(descifrado)
    return resultado


# Simular un stream de datos (como paquetes de red)
llave_stream = ChaCha20Poly1305.generate_key()
paquetes = [
    b"Paquete 1: Hola, este es el inicio de la comunicacion.",
    b"Paquete 2: Aqui van los datos importantes del sensor.",
    b"Paquete 3: Temperatura=23.5C, Humedad=67%, Presion=1013hPa",
    b"Paquete 4: Fin de la transmision. Checksum OK.",
]

print(f"\nCifrando {len(paquetes)} paquetes de datos...")
cifrados = cifrar_stream(paquetes, llave_stream, b"sensor:temp-01")

for i, (nonce, cifrado) in enumerate(cifrados):
    print(f"  Paquete {i}: nonce={nonce.hex()[:16]}... "
          f"cifrado={len(cifrado)} bytes")

# Descifrar
descifrados = descifrar_stream(cifrados, llave_stream, b"sensor:temp-01")
print(f"\nDescifrados correctamente: {len(descifrados)} paquetes")
for i, paquete in enumerate(descifrados):
    print(f"  {paquete.decode()}")

# Demostrar que reordenar paquetes se detecta
print("\n--- Intento de reordenamiento ---")
cifrados_reordenados = [cifrados[2], cifrados[0], cifrados[1], cifrados[3]]
try:
    descifrar_stream(cifrados_reordenados, llave_stream, b"sensor:temp-01")
    print("ERROR: deberia haber fallado!")
except Exception as e:
    print(f"Reordenamiento detectado: {type(e).__name__}")
    print("Los datos asociados incluyen el numero de secuencia,")
    print("por lo que cambiar el orden invalida la autenticacion.")


# ---------- Parte 4: Benchmark AES-GCM vs ChaCha20-Poly1305 ----------

print("\n" + "=" * 65)
print("PARTE 4: Benchmark AES-256-GCM vs ChaCha20-Poly1305")
print("=" * 65)


def bench(nombre: str, cifrador, tamano: int, iteraciones: int) -> float:
    """Mide rendimiento en MB/s."""
    datos = os.urandom(tamano)
    ad = b"benchmark"

    # Calentar
    for _ in range(5):
        cifrador.encrypt(os.urandom(12), datos, ad)

    inicio = time.perf_counter()
    for _ in range(iteraciones):
        cifrador.encrypt(os.urandom(12), datos, ad)
    duracion = time.perf_counter() - inicio

    mbps = (tamano * iteraciones / 1_000_000) / duracion
    print(f"  {nombre:>25}: {mbps:>8.1f} MB/s")
    return mbps


tamanos = [64, 1_024, 16_384, 1_048_576]  # 64B, 1KB, 16KB, 1MB
iteraciones_por_tamano = [10_000, 5_000, 500, 50]

llave_a = AESGCM.generate_key(bit_length=256)
llave_c = ChaCha20Poly1305.generate_key()
aes = AESGCM(llave_a)
chacha = ChaCha20Poly1305(llave_c)

print()
for tamano, iters in zip(tamanos, iteraciones_por_tamano):
    print(f"\nTamano de datos: {tamano:>10,} bytes ({iters} iteraciones)")
    vel_aes = bench("AES-256-GCM", aes, tamano, iters)
    vel_chacha = bench("ChaCha20-Poly1305", chacha, tamano, iters)
    if vel_aes > vel_chacha:
        print(f"  {'AES gana':>25}: {vel_aes/vel_chacha:.2f}x mas rapido")
    else:
        print(f"  {'ChaCha20 gana':>25}: {vel_chacha/vel_aes:.2f}x mas rapido")


print("\n=== Ejercicio completado ===")
```

**Extensiones sugeridas:**

1. Implementa XChaCha20-Poly1305 (nonces de 192 bits) usando la libreria `pynacl` y compara con la version IETF de 96 bits.
2. Modifica la Parte 3 para cifrar un archivo grande en chunks, simulando streaming real. Asegurate de que cada chunk tenga su propio nonce y numero de secuencia.
3. Investiga cuanto trafico puede cifrar una sola llave de ChaCha20-Poly1305 antes de que el riesgo de colision de nonces sea inaceptable. Calcula el birthday bound para nonces de 96 bits.
4. Implementa un detector de reutilizacion de nonces: dado un registro de (nonce, cifrado), alerta si se detecta un nonce repetido.

---

## Resumen del capitulo

| Concepto | Lo esencial |
|----------|-------------|
| Cifrado de flujo | Genera keystream pseudo-aleatorio, lo combina con XOR. Tamano arbitrario. |
| Keystream | Flujo de bits indistinguible de ruido aleatorio. La pieza critica. |
| RC4 | ROTO. Sesgos estadisticos explotables. Prohibido por RFC 7465 (2015). |
| Salsa20 | Diseno ARX de Bernstein (2005). Seguro, pero reemplazado por ChaCha20. |
| ChaCha20 | Evolucion de Salsa20. Mejor difusion. 20 rondas ARX. Estandar en TLS. |
| Poly1305 | MAC basado en aritmetica modular. Complemento de autenticacion para ChaCha20. |
| ChaCha20-Poly1305 | AEAD: cifrado + autenticacion. Sin AES-NI, es la mejor opcion. |
| AES-GCM vs ChaCha20 | Con AES-NI: AES-GCM. Sin AES-NI: ChaCha20-Poly1305. Ambos seguros. |
| CSPRNG | Usar os.urandom() o secrets. Nunca random(). |
| Reutilizacion de nonce | Destruye toda la seguridad. El error mas comun y mas fatal. |

**Takeaway:** Los cifrados de flujo son elegantes y rapidos, pero su seguridad depende completamente de dos cosas: la calidad de la aleatoriedad para generar llaves, y la unicidad absoluta del nonce. Nunca, bajo ninguna circunstancia, reutilices un nonce.

---

**En el proximo capitulo:** dejamos el cifrado simetrico para entrar al mundo de la criptografia asimetrica. Dos llaves diferentes --una publica, una privada-- que resuelven el problema de distribucion de llaves que hemos ignorado hasta ahora. Conoceremos a RSA, Diffie-Hellman, y las curvas elipticas.
