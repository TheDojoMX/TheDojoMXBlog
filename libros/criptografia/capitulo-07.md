# Capitulo 7: Cifrados de bloque -- AES y como se protege la informacion en reposo

> "Un cifrado de bloque convierte un bloque fijo de bits en ruido indistinguible. Si lo usas bien, nadie en el universo puede recuperar el mensaje original. Si lo usas mal, un estudiante con una laptop puede hacerlo en minutos."

---

Cada vez que abres WhatsApp, tu telefono ejecuta AES miles de veces por segundo. Cada vez que tu navegador establece una conexion HTTPS, negocia un cifrado simetrico --casi siempre AES-- para proteger los datos en transito. Cada vez que tu disco duro cifrado arranca, AES descifra sector por sector a velocidades de gigabytes por segundo.

Este algoritmo, disenado por dos criptografos belgas en los anos 90, protege mas secretos que cualquier otro invento humano. Y funciona mezclando bytes en una tabla de 4x4, entre 10 y 14 veces seguidas.

Pero AES por si solo no es suficiente. El algoritmo correcto con el **modo de operacion** incorrecto es igual de peligroso que no cifrar. En 2013, Adobe perdio 153 millones de contrasenas cifradas con 3DES en modo ECB --un modo que nunca debio usarse-- y los atacantes pudieron descifrar millones de ellas sin romper el cifrado, simplemente observando patrones [Schneier, 2013; Krebs, 2013].

Este capitulo te ensena como funciona AES por dentro, por que los modos de operacion importan tanto como el algoritmo, y como implementar cifrado autenticado correctamente en Python.

---

## 7.1 Cifrado simetrico: una llave para gobernarlos a todos

### 7.1.1 El concepto

El cifrado simetrico es la forma mas antigua y directa de criptografia: una sola llave sirve tanto para cifrar como para descifrar. Alice cifra un mensaje con la llave K, se lo envia a Bob, y Bob lo descifra con la misma llave K.

La analogia clasica es un candado con dos copias de la misma llave. Alice pone el mensaje en una caja, la cierra con su copia, y Bob la abre con la suya. El problema obvio es: como le haces llegar la llave a Bob sin que alguien la intercepte? Este es el **problema de la distribucion de llaves**, que resolveremos en capitulos posteriores cuando hablemos de criptografia asimetrica y protocolos como Diffie-Hellman.

Por ahora, asumiremos que ambas partes ya comparten una llave secreta. En la practica, esto es exactamente lo que sucede despues de que TLS negocia una llave de sesion: todo el trafico se cifra con un cifrado simetrico.

### 7.1.2 Cifrados de bloque vs cifrados de flujo

Los cifrados simetricos se dividen en dos grandes familias:

- **Cifrados de bloque**: toman un bloque de tamano fijo (por ejemplo, 128 bits) y producen un bloque cifrado del mismo tamano. Para mensajes mas largos que un bloque, se usan **modos de operacion**.
- **Cifrados de flujo**: generan un flujo continuo de bits pseudo-aleatorios (el *keystream*) y lo combinan con el mensaje mediante XOR. Pueden cifrar datos de tamano arbitrario sin necesidad de dividir en bloques.

En este capitulo nos concentramos en cifrados de bloque. El capitulo 8 cubrira los cifrados de flujo en detalle.

### 7.1.3 Permutaciones pseudo-aleatorias

Un cifrado de bloque es, matematicamente, una **permutacion pseudo-aleatoria** (PRP). Dado un bloque de entrada y una llave, produce un bloque de salida que es indistinguible de una permutacion elegida al azar entre todas las permutaciones posibles de bloques de ese tamano.

Claude Shannon, el padre de la teoria de la informacion, establecio en 1949 dos principios que todo cifrado debe cumplir:

- **Confusion**: cada bit del texto cifrado debe depender de multiples bits de la llave. Esto hace que la relacion entre la llave y el texto cifrado sea lo mas compleja posible.
- **Difusion**: cada bit del texto plano debe influir en muchos bits del texto cifrado. Si cambias un solo bit de la entrada, aproximadamente la mitad de los bits de la salida deben cambiar.

AES implementa ambos principios de manera elegante a traves de sus cuatro operaciones internas.

---

## 7.2 AES por dentro: las cuatro operaciones

### 7.2.1 Historia: de DES a Rijndael

Para entender por que AES existe, hay que entender por que su predecesor fallo.

El **Data Encryption Standard** (DES) fue adoptado como estandar federal de Estados Unidos en 1977. Usaba bloques de 64 bits y una llave de 56 bits. En su momento, 2^56 operaciones (aproximadamente 72 mil billones) parecian un muro infranqueable.

No duro. En 1998, la Electronic Frontier Foundation construyo una maquina llamada "Deep Crack" por 250,000 dolares que rompio DES por fuerza bruta en 56 horas. En 1999, combinando Deep Crack con una red distribuida, lo rompieron en menos de 24 horas [EFF, 1998].

La respuesta inmediata fue **Triple DES** (3DES): aplicar DES tres veces con tres llaves diferentes, dando una seguridad efectiva de 112 bits. Funcionaba, pero era tres veces mas lento que DES y tenia bloques de solo 64 bits, lo que lo hacia vulnerable a ataques de cumpleanos despues de 2^32 bloques (el ataque Sweet32 de 2016 demostro esto en la practica).

La NIST (National Institute of Standards and Technology) reconocio que necesitaba un reemplazo fundamental. En 1997 lanzo un concurso abierto internacional para seleccionar el nuevo estandar. Se presentaron 15 candidatos de todo el mundo. Despues de tres anos de analisis publico intensivo, el ganador fue **Rijndael**, creado por los criptografos belgas Joan Daemen y Vincent Rijmen --el mismo Daemen que anos despues co-disenaria Keccak (SHA-3).

En 2001, Rijndael se convirtio oficialmente en AES. Los criterios de seleccion fueron claros: seguridad, velocidad, simplicidad de implementacion y flexibilidad.

### 7.2.2 La matriz de estado 4x4

AES trabaja con bloques de **128 bits** (16 bytes). Estos 16 bytes se organizan en una **matriz de estado** de 4 filas por 4 columnas:

```
Bloque de entrada (16 bytes): b0 b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 b14 b15

Matriz de estado:
+-----+-----+-----+-----+
| b0  | b4  | b8  | b12 |
+-----+-----+-----+-----+
| b1  | b5  | b9  | b13 |
+-----+-----+-----+-----+
| b2  | b6  | b10 | b14 |
+-----+-----+-----+-----+
| b3  | b7  | b11 | b15 |
+-----+-----+-----+-----+

Nota: los bytes se llenan por columnas, no por filas.
```

Sobre esta matriz se aplican cuatro operaciones en secuencia, y esta secuencia se repite multiples veces. Cada repeticion se llama un **round** (ronda):

| Tamano de llave | Rondas |
|-----------------|--------|
| 128 bits        | 10     |
| 192 bits        | 12     |
| 256 bits        | 14     |

Cada ronda aplica las mismas cuatro operaciones en orden:

```
Estado inicial
    |
    v
+--[AddRoundKey]--+  (solo la ronda 0: mezcla con la llave inicial)
    |
    v
+--[SubBytes]-----+
|  [ShiftRows]    |
|  [MixColumns]   |  x  (Nr - 1) rondas
|  [AddRoundKey]  |
+-----------------+
    |
    v
+--[SubBytes]-----+
|  [ShiftRows]    |  ultima ronda (sin MixColumns)
|  [AddRoundKey]  |
+-----------------+
    |
    v
Texto cifrado
```

Veamos cada operacion.

### 7.2.3 SubBytes: la S-Box

**SubBytes** es la operacion de **confusion**. Reemplaza cada byte de la matriz de estado por otro byte, usando una tabla de sustitucion llamada **S-Box** (Substitution Box).

La S-Box no es arbitraria. Se construye en dos pasos:

1. Se calcula el **inverso multiplicativo** de cada byte en el campo finito GF(2^8) (el mismo campo de Galois del que hablamos en el capitulo 2). El byte 0x00 se mapea a si mismo.
2. Se aplica una **transformacion afin** a nivel de bits.

La no-linealidad es critica. Sin ella, AES seria un sistema de ecuaciones lineales que un atacante podria resolver algebraicamente. La S-Box asegura que la relacion entre entrada y salida sea lo mas compleja posible.

En la practica, la S-Box se implementa como una tabla de 256 entradas precalculada:

```
S-Box de AES (hexadecimal, primeros 4 filas):

     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
0 [ 63 7c 77 7b f2 6b 6f c5 30 01 67 2b fe d7 ab 76 ]
1 [ ca 82 c9 7d fa 59 47 f0 ad d4 a2 af 9c a4 72 c0 ]
2 [ b7 fd 93 26 36 3f f7 cc 34 a5 e5 f1 71 d8 31 15 ]
3 [ 04 c7 23 c3 18 96 05 9a 07 12 80 e2 eb 27 b2 75 ]
...

Para sustituir el byte 0x53: fila 5, columna 3 -> resultado: 0xed
```

Veamos la sustitucion en Python:

```python
"""
subbytes_demo.py

Demostracion de la operacion SubBytes de AES.
"""

# S-Box completa de AES (256 valores)
SBOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5,
    0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0,
    0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc,
    0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a,
    0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0,
    0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
    0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85,
    0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5,
    0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17,
    0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88,
    0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c,
    0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9,
    0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6,
    0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e,
    0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94,
    0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68,
    0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,
]


def sub_bytes(estado: list[list[int]]) -> list[list[int]]:
    """Aplica SubBytes: sustituye cada byte usando la S-Box."""
    return [[SBOX[byte] for byte in fila] for fila in estado]


# Ejemplo: estado de 4x4 bytes
estado = [
    [0x32, 0x88, 0x31, 0xe0],
    [0x43, 0x5a, 0x31, 0x37],
    [0xf6, 0x30, 0x98, 0x07],
    [0xa8, 0x8d, 0xa2, 0x34],
]

resultado = sub_bytes(estado)
print("Estado original:")
for fila in estado:
    print("  ", " ".join(f"{b:02x}" for b in fila))

print("\nDespues de SubBytes:")
for fila in resultado:
    print("  ", " ".join(f"{b:02x}" for b in fila))
```

### 7.2.4 ShiftRows y MixColumns: difusion

**ShiftRows** y **MixColumns** son las operaciones de **difusion**. Juntas aseguran que cada bit de entrada afecte todos los bits de salida despues de unas pocas rondas.

**ShiftRows** desplaza ciclicamente las filas de la matriz de estado:

```
Antes de ShiftRows:          Despues de ShiftRows:

+----+----+----+----+        +----+----+----+----+
| a0 | a1 | a2 | a3 |  <--  | a0 | a1 | a2 | a3 |  fila 0: sin cambio
+----+----+----+----+        +----+----+----+----+
| b0 | b1 | b2 | b3 |  <--  | b1 | b2 | b3 | b0 |  fila 1: rotar 1 posicion a la izquierda
+----+----+----+----+        +----+----+----+----+
| c0 | c1 | c2 | c3 |  <--  | c2 | c3 | c0 | c1 |  fila 2: rotar 2 posiciones
+----+----+----+----+        +----+----+----+----+
| d0 | d1 | d2 | d3 |  <--  | d3 | d0 | d1 | d2 |  fila 3: rotar 3 posiciones
+----+----+----+----+        +----+----+----+----+
```

La implementacion es directa:

```python
def shift_rows(estado: list[list[int]]) -> list[list[int]]:
    """Desplaza ciclicamente las filas de la matriz de estado."""
    return [
        estado[0],                              # fila 0: sin cambio
        estado[1][1:] + estado[1][:1],          # fila 1: rotar 1
        estado[2][2:] + estado[2][:2],          # fila 2: rotar 2
        estado[3][3:] + estado[3][:3],          # fila 3: rotar 3
    ]
```

**MixColumns** opera sobre cada columna de la matriz, mezclando los cuatro bytes usando multiplicacion de matrices en el campo finito GF(2^8). Cada columna se multiplica por una matriz fija:

```
                  Columna de entrada     Columna de salida
+--+--+--+--+     +----+                +----+
| 2  3  1  1 |    | c0 |                | r0 |
| 1  2  3  1 |  x | c1 |  =            | r1 |
| 1  1  2  3 |    | c2 |                | r2 |
| 3  1  1  2 |    | c3 |                | r3 |
+--+--+--+--+     +----+                +----+

Todas las operaciones son en GF(2^8), no aritmetica normal.
```

La multiplicacion en GF(2^8) no es la multiplicacion entera que conocemos. Es una operacion sobre polinomios modulo un polinomio irreducible. Pero el efecto practico es claro: cada byte de salida depende de los **cuatro** bytes de la columna de entrada. Despues de dos rondas de ShiftRows + MixColumns, cada byte del estado depende de **todos** los bytes de la entrada original.

```python
def xtime(a: int) -> int:
    """Multiplicacion por 2 en GF(2^8)."""
    resultado = a << 1
    if resultado & 0x100:  # si desborda 8 bits
        resultado ^= 0x11b  # reducir con polinomio irreducible de AES
    return resultado & 0xff


def mul_gf(a: int, b: int) -> int:
    """Multiplicacion general en GF(2^8)."""
    resultado = 0
    temp = a
    for i in range(8):
        if b & (1 << i):
            resultado ^= temp
        temp = xtime(temp)
    return resultado


def mix_columns(estado: list[list[int]]) -> list[list[int]]:
    """Mezcla cada columna usando multiplicacion en GF(2^8)."""
    resultado = [[0] * 4 for _ in range(4)]
    # La matriz fija de MixColumns
    matriz = [
        [2, 3, 1, 1],
        [1, 2, 3, 1],
        [1, 1, 2, 3],
        [3, 1, 1, 2],
    ]
    for col in range(4):
        columna = [estado[fila][col] for fila in range(4)]
        for fila in range(4):
            resultado[fila][col] = 0
            for k in range(4):
                resultado[fila][col] ^= mul_gf(matriz[fila][k], columna[k])
    return resultado
```

### 7.2.5 AddRoundKey y expansion de llave

**AddRoundKey** es la operacion mas simple pero la mas critica: combina cada byte del estado con un byte de la **subllave de ronda** mediante XOR.

```
Estado              Subllave de ronda       Resultado
+----+----+----+----+   +----+----+----+----+   +----+----+----+----+
| s0 | s4 | s8 | sC |   | k0 | k4 | k8 | kC |   |s0^k0|    |    |    |
+----+----+----+----+ ^ +----+----+----+----+ = +----+----+----+----+
| s1 | s5 | s9 | sD |   | k1 | k5 | k9 | kD |   |    |    |    |    |
+----+----+----+----+   +----+----+----+----+   +----+----+----+----+
| ...                |   | ...                |   | ...                |
+----+----+----+----+   +----+----+----+----+   +----+----+----+----+
```

Sin AddRoundKey, las demas operaciones serian una funcion fija e invertible que cualquiera podria revertir. Es la llave, inyectada en cada ronda, la que hace que solo quien posee la llave pueda descifrar.

La **expansion de llave** (Key Schedule) genera las subllaves de cada ronda a partir de la llave original. Para AES-128 (10 rondas), se necesitan 11 subllaves de 128 bits (una para la ronda inicial + una por cada ronda). Para AES-256, se necesitan 15 subllaves.

El Key Schedule usa las mismas operaciones que el cifrado principal --SubBytes y XOR con constantes de ronda-- para derivar cada subllave de la anterior. Esto asegura que las subllaves sean suficientemente diferentes entre si.

```python
def add_round_key(estado: list[list[int]],
                  subllave: list[list[int]]) -> list[list[int]]:
    """XOR del estado con la subllave de ronda."""
    return [
        [estado[fila][col] ^ subllave[fila][col]
         for col in range(4)]
        for fila in range(4)
    ]
```

### 7.2.6 AES en hardware: instrucciones AES-NI

En 2010, Intel introdujo el conjunto de instrucciones **AES-NI** (AES New Instructions) en sus procesadores. ARM agrego instrucciones equivalentes poco despues. Estas instrucciones ejecutan las operaciones de AES directamente en el hardware del procesador.

El impacto en rendimiento es enorme:

```
Implementacion            Rendimiento aproximado
-----------------------------------------------------
AES en software puro      ~28 ciclos por byte
AES con AES-NI            ~1.3 ciclos por byte (AES-128)
                          ~3.5 ciclos por byte (AES-256-GCM)

Factor de aceleracion: 3x a 13x segun implementacion
```

Fuentes: Intel, benchmarks con Crypto++ [Intel, 2010; Wei Dai, Crypto++].

Las implicaciones son profundas:

1. **AES es el cifrado mas rapido en hardware moderno**. Cualquier alternativa puramente software sera mas lenta en procesadores con AES-NI.
2. **Resistencia a ataques de canal lateral**. Las implementaciones en hardware son resistentes a ataques de temporizado (timing attacks), porque la ejecucion toma tiempo constante independientemente de los datos.
3. **Cifrado transparente**. Cifrar y descifrar a velocidades de gigabytes por segundo hace posible el cifrado completo de disco y el cifrado de todo el trafico de red sin impacto perceptible.

Para verificar si tu procesador soporta AES-NI:

```python
"""
aes_ni_check.py

Verifica si el procesador soporta instrucciones AES-NI.
"""

import subprocess
import platform


def tiene_aes_ni() -> bool:
    """Detecta soporte de AES-NI en el procesador."""
    sistema = platform.system()
    try:
        if sistema == "Linux":
            resultado = subprocess.run(
                ["grep", "-c", "aes", "/proc/cpuinfo"],
                capture_output=True, text=True
            )
            return int(resultado.stdout.strip()) > 0
        elif sistema == "Darwin":  # macOS
            resultado = subprocess.run(
                ["sysctl", "-n", "hw.optional.aes"],
                capture_output=True, text=True
            )
            return resultado.stdout.strip() == "1"
        elif sistema == "Windows":
            # En Windows, la libreria cryptography usa AES-NI automaticamente
            return True  # Casi todos los procesadores x86 desde 2010
    except Exception:
        pass
    return False


if tiene_aes_ni():
    print("Tu procesador soporta AES-NI.")
    print("La libreria 'cryptography' de Python la usara automaticamente.")
else:
    print("Tu procesador NO soporta AES-NI.")
    print("Considera usar ChaCha20-Poly1305 (ver Capitulo 8).")
```

---

## 7.3 Modos de operacion: donde vive el peligro

AES cifra exactamente **un bloque de 128 bits** (16 bytes). Pero en la vida real, los mensajes tienen tamanos arbitrarios: un archivo de 50 MB, una cookie de 200 bytes, un documento de 3 KB. Los **modos de operacion** definen como aplicar un cifrado de bloque a datos de tamano arbitrario.

Elegir el modo incorrecto puede destruir completamente la seguridad, incluso usando AES-256. Esto no es teoria: es exactamente lo que le paso a Adobe en 2013.

### 7.3.1 ECB: el modo prohibido

**Electronic Codebook** (ECB) es el modo mas simple posible: divide el mensaje en bloques de 16 bytes y cifra cada uno independientemente con la misma llave.

```
Texto plano:  [Bloque 1] [Bloque 2] [Bloque 3] [Bloque 4]
                  |            |            |            |
               AES(K)      AES(K)      AES(K)      AES(K)
                  |            |            |            |
Texto cifrado: [Cifrado 1] [Cifrado 2] [Cifrado 3] [Cifrado 4]
```

El problema es devastador: **si dos bloques de texto plano son identicos, sus bloques cifrados tambien lo son**. Esto filtra informacion sobre la estructura del mensaje sin romper el cifrado.

La demostracion mas famosa es el **pinguino ECB**. Si tomas una imagen del pinguino Tux (la mascota de Linux) y la cifras con AES-ECB, el resultado sigue siendo reconocible como un pinguino. Las grandes regiones de color uniforme --blanco, negro-- producen bloques identicos que se cifran al mismo bloque cifrado, preservando la silueta [Filippo Valsorda, 2013].

```
Imagen original:        Cifrada con ECB:        Cifrada con CBC:

    .---.                   .---.               %%%&$@!#*^
   / o o \                 / # # \              @#$%^&*(!@
  |   <   |               |   ?   |             !@#$%^&*()
  |  ===  |               |  ###  |             *&^%$#@!)(
   \_____/                 \_###_/              #$%^&*(!@#
   /|   |\                /|###|\              ^&*(!@#$%^
  (_|   |_)              (_|###|_)             !@#$%^&*()

  (Se reconoce           (Se reconoce          (Ruido total:
   el pinguino)           el pinguino!)         CORRECTO)
```

**El caso Adobe (2013)**

Adobe no uso ECB para cifrar imagenes, sino algo peor: uso 3DES en modo ECB para "cifrar" 153 millones de contrasenas de usuario. Con la misma llave para todos los usuarios.

El resultado: si dos usuarios tenian la misma contrasena, su texto cifrado era identico. Los investigadores pudieron identificar que "123456" era la contrasena mas comun (aparecia 1.9 millones de veces) sin descifrar nada --solo contando bloques repetidos. Combinando esto con las pistas de contrasena que Adobe almacenaba en texto plano junto a los cifrados, se reconstruyeron millones de contrasenas [Schneier, 2013; Filippo Valsorda, 2013].

**[PELIGRO]** Nunca uses ECB para nada. La unica razon por la que existe en las librerias es para construir otros modos de operacion y para fines educativos. Si ves ECB en codigo de produccion, es un error de seguridad critico.

Veamos como se ve el problema en codigo:

```python
"""
ecb_inseguro_demo.py

Demostracion de por que ECB filtra informacion.
NO USES ECB EN PRODUCCION.
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

llave = os.urandom(32)  # AES-256

# Mensaje con bloques repetidos (cada bloque = 16 bytes)
bloque_a = b"AAAAAAAAAAAAAAAA"  # 16 bytes identicos
bloque_b = b"BBBBBBBBBBBBBBBB"
mensaje = bloque_a + bloque_a + bloque_b + bloque_a  # 64 bytes

# Cifrar con ECB
cifrador_ecb = Cipher(algorithms.AES(llave), modes.ECB()).encryptor()
cifrado_ecb = cifrador_ecb.update(mensaje) + cifrador_ecb.finalize()

print("ECB - Bloques cifrados (hex):")
for i in range(0, len(cifrado_ecb), 16):
    bloque = cifrado_ecb[i:i+16].hex()
    print(f"  Bloque {i//16}: {bloque}")

# Observa: los bloques 0, 1 y 3 son IDENTICOS
# porque el texto plano es identico. Esto filtra informacion.

print()

# Comparar con CBC
iv = os.urandom(16)
cifrador_cbc = Cipher(algorithms.AES(llave), modes.CBC(iv)).encryptor()
from cryptography.hazmat.primitives import padding
padder = padding.PKCS7(128).padder()
datos_padded = padder.update(mensaje) + padder.finalize()
cifrado_cbc = cifrador_cbc.update(datos_padded) + cifrador_cbc.finalize()

print("CBC - Bloques cifrados (hex):")
for i in range(0, len(cifrado_cbc), 16):
    bloque = cifrado_cbc[i:i+16].hex()
    print(f"  Bloque {i//16}: {bloque}")

# Todos los bloques son diferentes, incluso para texto plano repetido.
```

### 7.3.2 CBC: encadenamiento de bloques

**Cipher Block Chaining** (CBC) resuelve el problema de ECB encadenando cada bloque con el anterior: antes de cifrar un bloque, se le aplica XOR con el bloque cifrado anterior.

```
IV (aleatorio)
  |
  v
Bloque 1 --XOR--> AES(K) --> Cifrado 1 ----+
                                             |
Bloque 2 --XOR--> AES(K) --> Cifrado 2 ----+
                   ^                         |
                   |                         |
              (cifrado anterior)             |
                                             v
Bloque 3 --XOR--> AES(K) --> Cifrado 3
                   ^
                   |
              (cifrado anterior)
```

El primer bloque se combina con un **vector de inicializacion** (IV) generado aleatoriamente. Esto asegura que cifrar el mismo mensaje dos veces con la misma llave pero diferente IV produce resultados completamente diferentes.

CBC fue el modo dominante durante anos y sigue siendo seguro si se implementa correctamente. Pero tiene dos debilidades importantes:

1. **No es paralelizable para cifrado**. Cada bloque depende del anterior, asi que no puedes cifrar multiples bloques simultaneamente. (El descifrado si es paralelizable.)

2. **Vulnerable a ataques de padding oracle**. CBC requiere que el ultimo bloque se rellene (padding) para completar 16 bytes. Si un servidor revela si el padding es valido o invalido --por ejemplo, con mensajes de error diferentes--, un atacante puede descifrar el mensaje entero byte por byte.

El ataque **POODLE** (Padding Oracle On Downgraded Legacy Encryption) de 2014 exploto exactamente esto en SSL 3.0. Los investigadores de Google demostraron que un atacante de red podia forzar un downgrade a SSL 3.0 y luego usar el oraculo de padding para descifrar cookies de sesion, necesitando en promedio solo 256 peticiones por cada byte descifrado [Moller, Duong, Kotowicz, 2014].

**[BUENA PRACTICA]** Si debes usar CBC (por compatibilidad con sistemas existentes), nunca reveles informacion sobre errores de padding. Mejor aun: usa cifrado autenticado (GCM) que elimina esta clase de ataques por completo.

### 7.3.3 CTR: el modo contador

**Counter Mode** (CTR) transforma un cifrado de bloque en algo que se comporta como un cifrado de flujo. En lugar de cifrar los bloques de texto plano, cifra un **nonce** concatenado con un **contador** que se incrementa para cada bloque, y luego combina el resultado con el texto plano mediante XOR.

```
Nonce|Ctr=0     Nonce|Ctr=1     Nonce|Ctr=2
    |                |                |
  AES(K)           AES(K)           AES(K)
    |                |                |
    v                v                v
Keystream 0     Keystream 1     Keystream 2
    |                |                |
   XOR              XOR              XOR
    |                |                |
Bloque 1        Bloque 2        Bloque 3
    |                |                |
    v                v                v
Cifrado 1       Cifrado 2       Cifrado 3
```

Las ventajas de CTR son notables:

- **Completamente paralelizable**: cada bloque es independiente. Puedes cifrar o descifrar multiples bloques simultaneamente.
- **No requiere padding**: la operacion XOR funciona con cualquier tamano. Si el ultimo bloque tiene 5 bytes, solo usas 5 bytes del keystream.
- **Acceso aleatorio**: puedes descifrar el bloque numero 1,000,000 sin descifrar los anteriores. Solo necesitas calcular el keystream para ese contador.

Pero CTR tiene una debilidad critica: **si reutilizas el nonce con la misma llave, la seguridad desaparece completamente**. Si cifras dos mensajes M1 y M2 con el mismo nonce y la misma llave, el keystream es identico. Un atacante que observe C1 y C2 puede calcular:

```
C1 XOR C2 = (M1 XOR keystream) XOR (M2 XOR keystream)
           = M1 XOR M2

El keystream se cancela. El atacante obtiene el XOR de los mensajes
en claro, y con analisis de frecuencia puede recuperar ambos.
```

**[PELIGRO]** La reutilizacion de nonces en modo CTR (y en GCM, que se basa en CTR) es la forma mas comun de romper cifrado simetrico correctamente implementado. Volveremos a este tema en la seccion de GCM.

### 7.3.4 GCM: cifrado autenticado

Hasta ahora, todos los modos que hemos visto proporcionan **confidencialidad** pero no **integridad**. Un atacante no puede leer el mensaje, pero puede modificar el texto cifrado sin que el receptor lo detecte. Esto es un problema serio.

Imagina que cifras una transferencia bancaria: "Transferir $100 a cuenta 12345". Un atacante que conoce la estructura del mensaje puede modificar bits del texto cifrado para cambiar la cantidad o el destino, sin conocer la llave ni el mensaje original.

**Galois/Counter Mode** (GCM) resuelve esto combinando dos mecanismos:

1. **CTR** para cifrado (confidencialidad).
2. **GHASH** para autenticacion (integridad), basado en aritmetica en el campo de Galois GF(2^128).

El resultado es **AEAD** (Authenticated Encryption with Associated Data): cifrado autenticado con datos asociados. Ademas de cifrar el mensaje, GCM calcula un **tag de autenticacion** que cubre tanto el texto cifrado como datos adicionales que no se cifran pero si se autentican (como encabezados de un protocolo).

```
Entradas:                    Salidas:
+----------------+           +-------------------+
| Llave (K)      |           | Texto cifrado (C) |
| Nonce (N)      |   AES    | Tag de            |
| Texto plano (P)|  -GCM->  |   autenticacion   |
| Datos          |           |   (T, 16 bytes)   |
|   asociados (A)|           |                   |
+----------------+           +-------------------+

Al descifrar: si alguien modifico C, A, o T, el descifrado FALLA.
```

GCM es el modo recomendado para la inmensa mayoria de casos de uso en 2026. Es el modo obligatorio en TLS 1.3, lo usa WireGuard, SSH, y la mayoria de APIs de cifrado modernas.

Aqui esta la implementacion correcta en Python:

```python
"""
aes_gcm_cifrado.py

Cifrado y descifrado con AES-256-GCM usando la libreria cryptography.
Este es el codigo que deberias usar en produccion.
"""

import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def cifrar_aes_gcm(mensaje: bytes,
                   datos_asociados: bytes | None = None) -> tuple[bytes, bytes, bytes]:
    """
    Cifra un mensaje con AES-256-GCM.

    Retorna: (llave, nonce, texto_cifrado_con_tag)

    La llave debe almacenarse de forma segura.
    El nonce y el texto cifrado pueden almacenarse/transmitirse juntos.
    """
    # Generar llave de 256 bits (32 bytes)
    llave = AESGCM.generate_key(bit_length=256)

    # Generar nonce de 96 bits (12 bytes) -- tamano recomendado para GCM
    nonce = os.urandom(12)

    # Crear cifrador y cifrar
    aesgcm = AESGCM(llave)
    texto_cifrado = aesgcm.encrypt(nonce, mensaje, datos_asociados)
    # El texto cifrado incluye el tag de autenticacion al final (16 bytes)

    return llave, nonce, texto_cifrado


def descifrar_aes_gcm(llave: bytes,
                      nonce: bytes,
                      texto_cifrado: bytes,
                      datos_asociados: bytes | None = None) -> bytes:
    """
    Descifra un mensaje cifrado con AES-256-GCM.

    Lanza InvalidTag si el texto cifrado o los datos asociados
    fueron modificados.
    """
    aesgcm = AESGCM(llave)
    return aesgcm.decrypt(nonce, texto_cifrado, datos_asociados)


# --- Demostracion ---

# 1. Cifrado basico
mensaje = b"Transferir $1,000 a cuenta 98765"
datos_asociados = b"usuario:alice|fecha:2026-03-25"

llave, nonce, cifrado = cifrar_aes_gcm(mensaje, datos_asociados)

print(f"Mensaje original:  {mensaje.decode()}")
print(f"Llave (hex):       {llave.hex()}")
print(f"Nonce (hex):       {nonce.hex()}")
print(f"Cifrado (hex):     {cifrado.hex()}")
print(f"  - Texto cifrado: {len(cifrado) - 16} bytes")
print(f"  - Tag:           {len(cifrado) - len(mensaje)} bytes (ultimos 16)")

# 2. Descifrado exitoso
descifrado = descifrar_aes_gcm(llave, nonce, cifrado, datos_asociados)
print(f"\nDescifrado:        {descifrado.decode()}")

# 3. Demostrar que la modificacion se detecta
print("\n--- Intentando modificar el texto cifrado ---")
cifrado_modificado = bytearray(cifrado)
cifrado_modificado[0] ^= 0x01  # Cambiar un solo bit
cifrado_modificado = bytes(cifrado_modificado)

try:
    descifrar_aes_gcm(llave, nonce, cifrado_modificado, datos_asociados)
    print("ERROR: deberia haber fallado!")
except Exception as e:
    print(f"Deteccion exitosa: {type(e).__name__}")
    print("El texto cifrado fue modificado y la autenticacion fallo.")

# 4. Demostrar que modificar datos asociados tambien se detecta
print("\n--- Intentando modificar datos asociados ---")
datos_falsos = b"usuario:mallory|fecha:2026-03-25"

try:
    descifrar_aes_gcm(llave, nonce, cifrado, datos_falsos)
    print("ERROR: deberia haber fallado!")
except Exception as e:
    print(f"Deteccion exitosa: {type(e).__name__}")
    print("Los datos asociados fueron modificados y la autenticacion fallo.")
```

**[BUENA PRACTICA]** Siempre usa cifrado autenticado (AES-GCM o ChaCha20-Poly1305). Cifrar sin autenticar es como enviar una carta en un sobre opaco pero sin sellar: nadie puede leerla, pero cualquiera puede reemplazar el contenido.

### 7.3.5 El error silencioso: reutilizacion de nonce en GCM

GCM hereda de CTR la misma debilidad critica: **si reutilizas un nonce con la misma llave, pierdes tanto la confidencialidad como la autenticidad**.

En concreto, reutilizar un nonce en AES-GCM permite a un atacante:

1. Obtener el XOR de los textos planos (como en CTR).
2. Recuperar la subllave de autenticacion GHASH, lo que le permite falsificar tags para **cualquier** mensaje futuro.

Este no es un ataque teorico. En 2010, Sony firmo el firmware de la PlayStation 3 con ECDSA usando un nonce fijo. Los investigadores extrajeron la llave privada de Sony algebraicamente. Aunque el ataque era sobre firmas y no sobre GCM, el principio es identico: la reutilizacion de un valor que debe ser unico destruye toda la seguridad [fail0verflow, 2010].

Para minimizar el riesgo de reutilizacion de nonce en GCM:

```python
"""
nonce_seguro.py

Estrategias para gestionar nonces de forma segura.
"""

import os
import struct
import time


# Estrategia 1: Nonce aleatorio (la mas simple)
# Funciona bien si no cifras mas de 2^32 mensajes con la misma llave.
# Con nonces de 96 bits aleatorios, la probabilidad de colision
# alcanza 50% despues de 2^48 mensajes (birthday bound).
# Para la mayoria de aplicaciones, esto es mas que suficiente.
def nonce_aleatorio() -> bytes:
    return os.urandom(12)  # 96 bits


# Estrategia 2: Nonce basado en contador
# Garantiza unicidad siempre que el contador no se reinicie.
# Ideal para: cifrado de disco, bases de datos, logs.
class ContadorNonce:
    def __init__(self, prefijo: bytes = b""):
        """
        prefijo: identificador unico de esta instancia (4 bytes max).
        El nonce sera: prefijo (4 bytes) + contador (8 bytes) = 12 bytes.
        """
        self.prefijo = prefijo.ljust(4, b'\x00')[:4]
        self.contador = 0

    def siguiente(self) -> bytes:
        nonce = self.prefijo + struct.pack(">Q", self.contador)
        self.contador += 1
        return nonce


# Estrategia 3: Rotar llaves periodicamente
# Si cifras muchos mensajes, rota la llave antes de
# alcanzar el limite seguro de nonces.
# Para AES-256-GCM con nonces aleatorios de 96 bits:
# rotar despues de 2^32 mensajes (4 mil millones) como maximo.
MAX_MENSAJES_POR_LLAVE = 2**32

print("Estrategias de gestion de nonces para AES-GCM:")
print(f"  Aleatorio: seguro hasta ~{2**48:,} mensajes por llave")
print(f"  Contador:  seguro hasta ~{2**64:,} mensajes por llave")
print(f"  Recomendacion: rotar llave cada {MAX_MENSAJES_POR_LLAVE:,} mensajes")
```

---

## 7.4 DES, 3DES y otros: el cementerio de cifrados

### DES (1977-1999)

56 bits de llave. Roto por fuerza bruta en 1999 con hardware de 250,000 dolares. Completamente obsoleto.

### Triple DES (1998-2023)

Aplica DES tres veces con tres llaves para obtener 112 bits de seguridad efectiva. Ineficiente (tres veces mas lento que DES), con bloques de solo 64 bits. El ataque **Sweet32** (2016) demostro que despues de capturar ~32 GB de datos cifrados con un cifrado de bloque de 64 bits, un atacante puede explotar colisiones de cumpleanos para descifrar informacion. Esto afecto a OpenVPN y TLS con 3DES [Bhargavan, Leurent, 2016]. La NIST depreco 3DES en 2023.

### Serpent

Finalista del concurso AES. Aplica 32 rondas (contra 10-14 de AES) para un margen de seguridad mayor. Los mejores ataques conocidos alcanzan 12 de las 32 rondas. La desventaja: es aproximadamente 3 veces mas lento que AES. Sigue siendo seguro pero poco usado por la falta de aceleracion por hardware.

### Twofish

Otro finalista del concurso AES, disenado por Bruce Schneier y equipo. Tiene una estructura tipo Feistel similar a DES con 16 rondas. Los autores argumentan que ofrece mas margen de seguridad que AES, pero la falta de adopcion generalizada y de soporte en hardware lo han relegado a un nicho.

**[BUENA PRACTICA]** Usa AES. Si tu procesador tiene AES-NI (virtualmente todos desde 2013), AES es simultaneamente el mas rapido y el mas probado. Si estas en un entorno sin AES-NI, considera ChaCha20-Poly1305 (capitulo 8).

---

## 7.5 Casos reales

### 7.5.1 POODLE (2014): la muerte de CBC en SSL

En octubre de 2014, tres investigadores de Google --Bodo Moller, Thai Duong y Krzysztof Kotowicz-- publicaron el ataque POODLE (Padding Oracle On Downgraded Legacy Encryption).

El ataque funcionaba en dos fases:

1. **Downgrade de protocolo**: un atacante de red forzaba al navegador y al servidor a negociar SSL 3.0 (un protocolo de 1996) en lugar de TLS moderno.
2. **Oraculo de padding**: explotaba una debilidad en como SSL 3.0 manejaba el padding en modo CBC. El atacante modificaba bytes del texto cifrado y observaba si el servidor aceptaba o rechazaba la conexion. Con 256 intentos promedio por byte, podia descifrar cookies de sesion completas.

El impacto fue inmediato: los principales navegadores deshabilitaron SSL 3.0 en cuestion de semanas. La leccion: el modo CBC combinado con padding crea una superficie de ataque que requiere cuidado extremo. Es mucho mejor usar GCM, que no usa padding y proporciona autenticacion integrada.

### 7.5.2 Sweet32 (2016): bloques pequenos, problemas grandes

Los investigadores Karthikeyan Bhargavan y Gaetan Leurent demostraron que los cifrados de bloque con bloques de 64 bits --como 3DES y Blowfish-- son vulnerables a ataques de cumpleanos (birthday attacks) en conexiones de larga duracion.

El ataque: despues de capturar aproximadamente 2^32 bloques de 64 bits (~32 GB de datos), la probabilidad de encontrar dos bloques cifrados identicos se acerca al 50%. Esos bloques identicos filtran informacion sobre el texto plano, similar a ECB.

Esto afecto directamente a:
- OpenVPN (que usaba Blowfish por defecto)
- TLS con suites de cifrado basadas en 3DES

La solucion: usar cifrados con bloques de 128 bits (AES) y limitar la cantidad de datos cifrados por sesion.

### 7.5.3 Reutilizacion de nonce: el error que destruye todo

En 2010, el grupo fail0verflow presento en el Chaos Communication Congress como habian extraido la llave privada de Sony para la PlayStation 3. Sony habia firmado todo su firmware con ECDSA, pero cometio un error catastrofico: uso el mismo valor de nonce `k` en cada firma.

Con dos firmas (s1, s2) del mismo nonce, la matematica es directa:

```
s1 = k^(-1) * (hash1 + r * llave_privada) mod n
s2 = k^(-1) * (hash2 + r * llave_privada) mod n

Restando: s1 - s2 = k^(-1) * (hash1 - hash2) mod n
Despejando k: k = (hash1 - hash2) * (s1 - s2)^(-1) mod n
Despejando la llave: llave_privada = (s1 * k - hash1) * r^(-1) mod n
```

Aunque este ataque fue contra ECDSA y no contra AES-GCM, el principio es universal: **cualquier valor que debe ser unico, si se reutiliza, puede destruir la seguridad completa del sistema**. En AES-GCM, reutilizar un nonce revela tanto los mensajes como la subllave de autenticacion.

---

## 7.6 Ejercicio integrador: cifrador de archivos con AES-256-GCM

```python
"""
ejercicio_cap7_cifrador_archivos.py

Ejercicio integrador del Capitulo 7.
Cifra y descifra archivos usando AES-256-GCM con manejo correcto de nonces.

Objetivos:
1. Cifrar un archivo con AES-256-GCM.
2. Demostrar que modificar 1 byte del ciphertext hace fallar la autenticacion.
3. Implementar derivacion de llave desde password con Argon2id.

Prerequisitos:
  pip install cryptography argon2-cffi
"""

import os
import json
import struct
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# ---------- Parte 1: Cifrado basico de archivos ----------

def cifrar_archivo(ruta_entrada: str, ruta_salida: str,
                   llave: bytes, metadata: dict | None = None) -> None:
    """
    Cifra un archivo con AES-256-GCM.

    Formato del archivo cifrado:
    [4 bytes: tamano del nonce]
    [12 bytes: nonce]
    [4 bytes: tamano de datos asociados]
    [N bytes: datos asociados (JSON)]
    [resto: texto cifrado + tag (16 bytes)]
    """
    # Leer archivo
    with open(ruta_entrada, "rb") as f:
        datos = f.read()

    # Preparar nonce y datos asociados
    nonce = os.urandom(12)
    datos_asociados = json.dumps(
        metadata or {"archivo": str(ruta_entrada)}
    ).encode()

    # Cifrar
    aesgcm = AESGCM(llave)
    cifrado = aesgcm.encrypt(nonce, datos, datos_asociados)

    # Escribir archivo cifrado
    with open(ruta_salida, "wb") as f:
        f.write(struct.pack(">I", len(nonce)))
        f.write(nonce)
        f.write(struct.pack(">I", len(datos_asociados)))
        f.write(datos_asociados)
        f.write(cifrado)

    tamano_original = len(datos)
    tamano_cifrado = os.path.getsize(ruta_salida)
    print(f"Archivo cifrado: {ruta_salida}")
    print(f"  Original:  {tamano_original:,} bytes")
    print(f"  Cifrado:   {tamano_cifrado:,} bytes")
    print(f"  Overhead:  {tamano_cifrado - tamano_original:,} bytes "
          f"(nonce + metadata + tag)")


def descifrar_archivo(ruta_cifrada: str, ruta_salida: str,
                      llave: bytes) -> dict:
    """
    Descifra un archivo cifrado con AES-256-GCM.
    Retorna los datos asociados como diccionario.
    Lanza excepcion si el archivo fue modificado.
    """
    with open(ruta_cifrada, "rb") as f:
        # Leer nonce
        tamano_nonce = struct.unpack(">I", f.read(4))[0]
        nonce = f.read(tamano_nonce)

        # Leer datos asociados
        tamano_ad = struct.unpack(">I", f.read(4))[0]
        datos_asociados = f.read(tamano_ad)

        # Leer texto cifrado + tag
        cifrado = f.read()

    # Descifrar (lanza InvalidTag si fue modificado)
    aesgcm = AESGCM(llave)
    datos = aesgcm.decrypt(nonce, cifrado, datos_asociados)

    # Escribir archivo descifrado
    with open(ruta_salida, "wb") as f:
        f.write(datos)

    metadata = json.loads(datos_asociados.decode())
    print(f"Archivo descifrado: {ruta_salida}")
    print(f"  Tamano: {len(datos):,} bytes")
    print(f"  Metadata: {metadata}")
    return metadata


# ---------- Parte 2: Deteccion de manipulacion ----------

def demostrar_deteccion_manipulacion(ruta_cifrada: str, llave: bytes) -> None:
    """
    Modifica un solo byte del archivo cifrado y demuestra
    que la autenticacion falla.
    """
    # Leer archivo cifrado
    with open(ruta_cifrada, "rb") as f:
        contenido = bytearray(f.read())

    # Modificar un byte en el area de datos cifrados
    # (despues del encabezado)
    posicion = len(contenido) // 2  # mitad del archivo
    contenido[posicion] ^= 0x01    # cambiar un solo bit

    ruta_modificada = ruta_cifrada + ".tampered"
    with open(ruta_modificada, "wb") as f:
        f.write(contenido)

    print(f"\nArchivo modificado: byte {posicion} alterado (1 bit)")

    try:
        descifrar_archivo(ruta_modificada, "/dev/null", llave)
        print("ERROR: deberia haber detectado la manipulacion!")
    except Exception as e:
        print(f"Manipulacion detectada: {type(e).__name__}")
        print("El cifrado autenticado protege contra modificaciones.")
    finally:
        os.remove(ruta_modificada)


# ---------- Parte 3: Derivacion de llave desde password ----------

def llave_desde_password(password: str) -> tuple[bytes, dict]:
    """
    Deriva una llave AES-256 desde un password usando Argon2id.
    Retorna la llave y los parametros para poder reproducir la derivacion.
    """
    try:
        from argon2.low_level import hash_secret_raw, Type
    except ImportError:
        print("Instala argon2-cffi: pip install argon2-cffi")
        raise

    salt = os.urandom(16)

    # Parametros OWASP 2024 para Argon2id
    parametros = {
        "time_cost": 2,          # iteraciones
        "memory_cost": 19456,    # 19 MiB
        "parallelism": 1,
        "hash_len": 32,          # 256 bits para AES-256
        "salt": salt.hex(),
    }

    llave = hash_secret_raw(
        secret=password.encode(),
        salt=salt,
        time_cost=parametros["time_cost"],
        memory_cost=parametros["memory_cost"],
        parallelism=parametros["parallelism"],
        hash_len=parametros["hash_len"],
        type=Type.ID,
    )

    return llave, parametros


# ---------- Demo completa ----------

if __name__ == "__main__":
    # Crear archivo de prueba
    archivo_prueba = "/tmp/prueba_aes_gcm.txt"
    with open(archivo_prueba, "w") as f:
        f.write("Este es un mensaje secreto.\n" * 100)
    print("=== Ejercicio Capitulo 7: Cifrado de archivos con AES-256-GCM ===\n")

    # Generar llave
    llave = AESGCM.generate_key(bit_length=256)

    # Cifrar
    archivo_cifrado = archivo_prueba + ".enc"
    cifrar_archivo(archivo_prueba, archivo_cifrado, llave,
                   metadata={"autor": "alice", "tipo": "documento"})

    # Descifrar
    print()
    archivo_descifrado = archivo_prueba + ".dec"
    descifrar_archivo(archivo_cifrado, archivo_descifrado, llave)

    # Verificar integridad
    with open(archivo_prueba, "rb") as f1, open(archivo_descifrado, "rb") as f2:
        assert f1.read() == f2.read(), "Los archivos no coinciden!"
    print("Verificacion: archivo original y descifrado son identicos.")

    # Demostrar deteccion de manipulacion
    demostrar_deteccion_manipulacion(archivo_cifrado, llave)

    # Demostrar cifrado con password
    print("\n--- Cifrado con password (Argon2id + AES-256-GCM) ---")
    try:
        llave_pwd, params = llave_desde_password("mi_password_seguro_2026!")
        print(f"Llave derivada (hex): {llave_pwd.hex()[:32]}...")
        print(f"Salt (hex):           {params['salt'][:32]}...")
        print(f"Memoria: {params['memory_cost']} KiB, "
              f"Iteraciones: {params['time_cost']}")
    except ImportError:
        print("(Salta esta parte: instala argon2-cffi)")

    # Limpiar
    for archivo in [archivo_prueba, archivo_cifrado, archivo_descifrado]:
        if os.path.exists(archivo):
            os.remove(archivo)

    print("\n=== Ejercicio completado ===")
```

**Extensiones sugeridas:**

1. Modifica el programa para cifrar directorios completos recursivamente.
2. Agrega compresion (zlib) antes del cifrado. Discute por que comprimir **antes** de cifrar es importante y por que comprimir **despues** no sirve.
3. Implementa rotacion de llaves: despues de cifrar N archivos con la misma llave, genera una nueva.
4. Compara el rendimiento de AES-256-GCM contra ChaCha20-Poly1305 (anticipo del capitulo 8).

---

## Resumen del capitulo

| Concepto | Lo esencial |
|----------|-------------|
| Cifrado simetrico | Una llave cifra y descifra. Rapido, pero requiere compartir la llave. |
| AES | Cifrado de bloque de 128 bits. 10/12/14 rondas segun tamano de llave. Estandar global. |
| SubBytes | Sustitucion no lineal (confusion). Basada en inversos en GF(2^8). |
| ShiftRows + MixColumns | Difusion: cada bit afecta todos los bits en pocas rondas. |
| AddRoundKey | XOR con subllave de ronda. La operacion que introduce la llave. |
| AES-NI | Instrucciones de hardware. Aceleracion de 3-13x. |
| ECB | PROHIBIDO. Bloques identicos producen cifrado identico. |
| CBC | Encadena bloques. Vulnerable a padding oracle (POODLE). |
| CTR | Modo contador. Paralelizable, pero nonce unico es critico. |
| GCM | AEAD: cifrado + autenticacion. Estandar actual. Usa CTR + GHASH. |
| Reutilizacion de nonce | Destruye confidencialidad Y autenticidad en GCM. |

**Takeaway:** AES es el cifrado simetrico que debes usar. Pero el algoritmo correcto con el modo incorrecto es igual de peligroso que no cifrar. Usa siempre AES-256-GCM con nonces unicos.

---

**En el proximo capitulo:** cifrados de flujo. Cuando no sabes el tamano de lo que vas a cifrar, cuando el rendimiento en software puro importa mas que en hardware, y cuando necesitas una alternativa a AES que no dependa de instrucciones especiales del procesador. Conoceremos a ChaCha20 y a su companero Poly1305.
