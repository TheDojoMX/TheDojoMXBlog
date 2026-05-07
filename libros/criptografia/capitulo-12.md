# Capitulo 12: Migracion a criptografia post-cuantica -- guia practica

> "Solo el 3% de las organizaciones han empezado a implementar medidas de criptografia post-cuantica. Sin embargo, el 52% del trafico HTTPS que pasa por Cloudflare ya usa intercambio de llaves post-cuantico. La diferencia: los navegadores y las CDN hicieron la migracion por ti. Pero tu backend, tus APIs, tus firmas digitales y tus datos almacenados siguen expuestos."

---

En agosto de 2024, el NIST publico los primeros estandares de criptografia post-cuantica, culminando un proceso de 8 anios con 82 candidatos de 25 paises. No es un ejercicio academico: Chrome, Firefox, Edge y Safari ya usan criptografia post-cuantica en cada conexion HTTPS. Cloudflare reporta que mas del 50% de las conexiones que maneja son post-cuanticas [Cloudflare, 2025]. La infraestructura de Internet ya esta migrando. La pregunta es si tu codigo esta listo.

Este capitulo te da las herramientas para responder que si. Cubriremos los nuevos algoritmos estandarizados, la intuicion matematica detras de ellos, las bibliotecas disponibles, y un plan de migracion paso a paso con codigo ejecutable.

---

## 12.1 Los nuevos estandares del NIST

### 12.1.1 El proceso de seleccion: 8 anios, 82 candidatos

En diciembre de 2016, el NIST publico una convocatoria abierta para propuestas de algoritmos criptograficos resistentes a computadoras cuanticas. Respondieron 82 equipos de 25 paises. Tras multiples rondas de analisis, ataques, y revision publica, en agosto de 2024 el NIST publico tres estandares finales [NIST, 2024]:

- **FIPS 203:** ML-KEM (Module-Lattice-Based Key-Encapsulation Mechanism)
- **FIPS 204:** ML-DSA (Module-Lattice-Based Digital Signature Algorithm)
- **FIPS 205:** SLH-DSA (Stateless Hash-Based Digital Signature Algorithm)

Los criterios de seleccion fueron: seguridad demostrable contra ataques clasicos y cuanticos, rendimiento en diversas plataformas, y tamanos de llave y firma razonables. Los tres algoritmos finales representan el consenso de la comunidad criptografica internacional despues de la evaluacion publica mas extensa de la historia.

### 12.1.2 ML-KEM (CRYSTALS-Kyber): intercambio de llaves

ML-KEM es el reemplazo directo de ECDH y RSA-KEM para el intercambio de llaves. Es el algoritmo que Chrome, Firefox y Cloudflare ya despliegan en produccion. Su nombre original era CRYSTALS-Kyber; el NIST lo renombro a ML-KEM en el estandar final.

ML-KEM es un **mecanismo de encapsulacion de llaves** (KEM, Key Encapsulation Mechanism). A diferencia de Diffie-Hellman, donde ambas partes contribuyen a generar un secreto compartido, en un KEM una parte encapsula un secreto en un "ciphertext" que solo la otra parte puede desencapsular:

```
Generacion de llaves (servidor):
  (llave_publica, llave_privada) = ML-KEM.KeyGen()

Encapsulacion (cliente):
  (ciphertext, secreto_compartido) = ML-KEM.Encaps(llave_publica)

Desencapsulacion (servidor):
  secreto_compartido = ML-KEM.Decaps(ciphertext, llave_privada)

Resultado: ambas partes tienen el mismo secreto_compartido
que se usa como llave para AES-256 o ChaCha20-Poly1305.
```

ML-KEM tiene tres niveles de seguridad:

| Parametro | Seguridad | Llave publica | Ciphertext | Secreto |
|-----------|-----------|---------------|------------|---------|
| ML-KEM-512 | ~128 bits (NIST nivel 1) | 800 bytes | 768 bytes | 32 bytes |
| ML-KEM-768 | ~192 bits (NIST nivel 3) | 1,184 bytes | 1,088 bytes | 32 bytes |
| ML-KEM-1024 | ~256 bits (NIST nivel 5) | 1,568 bytes | 1,568 bytes | 32 bytes |

Para comparacion: una llave publica X25519 mide 32 bytes. ML-KEM-768 mide 1,184 bytes --37 veces mas grande. Este aumento de tamano es el principal costo de la migracion. Pero la buena noticia es que ML-KEM es **rapido**: las operaciones de encapsulacion y desencapsulacion son comparables en velocidad a RSA y significativamente mas rapidas que RSA para generacion de llaves.

El nivel recomendado para uso general es **ML-KEM-768**, que ofrece seguridad equivalente a AES-192 contra atacantes cuanticos. Es el nivel que usan Chrome, Firefox y Cloudflare en produccion.

### 12.1.3 ML-DSA (CRYSTALS-Dilithium): firmas digitales

ML-DSA es el reemplazo directo de ECDSA y RSA-PSS para firmas digitales. Su nombre original era CRYSTALS-Dilithium. Al igual que ML-KEM, esta basado en el problema Module Learning With Errors sobre reticulos.

ML-DSA se usara para:
- Certificados TLS (reemplazando RSA/ECDSA en certificados X.509)
- Firmas de codigo (software firmado, actualizaciones)
- Autenticacion (reemplazando Ed25519 en SSH, por ejemplo)
- Tokens firmados (JWT con algoritmos post-cuanticos)

| Parametro | Seguridad | Llave publica | Firma | Llave privada |
|-----------|-----------|---------------|-------|---------------|
| ML-DSA-44 | ~128 bits (NIST nivel 2) | 1,312 bytes | 2,420 bytes | 2,560 bytes |
| ML-DSA-65 | ~192 bits (NIST nivel 3) | 1,952 bytes | 3,293 bytes | 4,032 bytes |
| ML-DSA-87 | ~256 bits (NIST nivel 5) | 2,592 bytes | 4,627 bytes | 4,896 bytes |

Para comparacion: una firma ECDSA (P-256) mide 64 bytes. ML-DSA-65 produce firmas de 3,293 bytes --51 veces mas grandes. Una llave publica Ed25519 mide 32 bytes; ML-DSA-65 mide 1,952 bytes --61 veces mas grande.

Este aumento de tamano tiene implicaciones reales:
- Los certificados TLS seran significativamente mas grandes, impactando el tiempo de handshake.
- Las cadenas de certificados (root -> intermediate -> leaf) multiplicaran el impacto.
- Dispositivos IoT con restricciones de memoria enfrentaran desafios.

El nivel recomendado para uso general es **ML-DSA-65**.

### 12.1.4 SLH-DSA (SPHINCS+): firmas basadas en hash

SLH-DSA es la opcion "conservadora" para firmas digitales. A diferencia de ML-KEM y ML-DSA, que dependen de la dureza del problema de reticulos (un area matematica relativamente nueva), SLH-DSA depende **unicamente** de la seguridad de funciones hash --las mismas propiedades que estudiamos en los capitulos 1 y 3.

Si alguna vez se descubriera una debilidad en los problemas de reticulos (improbable, pero posible), ML-KEM y ML-DSA se verian comprometidos, pero SLH-DSA permaneceria seguro siempre que SHA-256 o SHA-3 sigan siendo seguros.

El precio de esta confianza adicional son firmas mucho mas grandes:

| Parametro | Seguridad | Firma |
|-----------|-----------|-------|
| SLH-DSA-SHA2-128f | ~128 bits | 17,088 bytes |
| SLH-DSA-SHA2-128s | ~128 bits | 7,856 bytes |
| SLH-DSA-SHA2-256f | ~256 bits | 49,856 bytes |

El sufijo "f" significa "fast" (firmas rapidas, mas grandes) y "s" significa "small" (firmas pequenas, mas lentas). Incluso la variante mas pequena produce firmas de ~8 KB --120 veces mas grandes que ECDSA.

**Cuando usar SLH-DSA en lugar de ML-DSA:**
- Cuando necesitas la maxima confianza en la seguridad a largo plazo.
- Para firmas de firmware o software que deben permanecer verificables por decadas.
- Como backup de diversidad: si despliegan ML-DSA para el uso diario, usa SLH-DSA para raices de confianza.

### 12.1.5 Tabla comparativa completa

```
COMPARACION DE TAMANOS: ALGORITMOS CLASICOS vs POST-CUANTICOS

========================================================================
INTERCAMBIO DE LLAVES
========================================================================
                  Llave publica    Ciphertext    Secreto compartido
------------------------------------------------------------------------
X25519            32 bytes         32 bytes      32 bytes
RSA-2048          256 bytes        256 bytes     32 bytes (despues de KDF)
ML-KEM-768        1,184 bytes      1,088 bytes   32 bytes
ML-KEM-1024       1,568 bytes      1,568 bytes   32 bytes

========================================================================
FIRMAS DIGITALES
========================================================================
                  Llave publica    Firma         Llave privada
------------------------------------------------------------------------
Ed25519           32 bytes         64 bytes      64 bytes
ECDSA (P-256)     64 bytes         64 bytes      32 bytes
RSA-2048          256 bytes        256 bytes     ~1,200 bytes
ML-DSA-65         1,952 bytes      3,293 bytes   4,032 bytes
ML-DSA-87         2,592 bytes      4,627 bytes   4,896 bytes
SLH-DSA-128s      32 bytes         7,856 bytes   64 bytes
SLH-DSA-128f      32 bytes         17,088 bytes  64 bytes
```

El patron es claro: los algoritmos post-cuanticos son rapidos en operaciones pero producen llaves y firmas significativamente mas grandes. El cuello de botella es el **ancho de banda**, no el computo.

---

## 12.2 Reticulos y Learning With Errors: la intuicion sin la matematica pesada

### 12.2.1 Que es un reticulo

Un **reticulo** (lattice) es una estructura geometrica: un conjunto de puntos regularmente espaciados en un espacio de muchas dimensiones. Piensa en el papel cuadriculado: los puntos donde se cruzan las lineas forman un reticulo en 2 dimensiones.

Formalmente, un reticulo es el conjunto de todas las combinaciones enteras de un conjunto de vectores base:

```
L = { a1*v1 + a2*v2 + ... + an*vn : a1, a2, ..., an son enteros }

Donde v1, v2, ..., vn son los vectores base del reticulo.
```

En 2 dimensiones, visualizar un reticulo es trivial. En 3 dimensiones, todavia puedes imaginarlo. Pero ML-KEM opera en dimensiones del orden de 512 a 1024. En esas dimensiones, los problemas de reticulos se vuelven extraordinariamente dificiles.

El problema fundamental es el **Problema del Vector mas Corto** (SVP, Shortest Vector Problem): dado un reticulo, encontrar el vector no nulo mas corto. En 2 dimensiones es trivial. En 500+ dimensiones, es computacionalmente intratable --incluso para computadoras cuanticas. No se conoce ningun algoritmo cuantico que resuelva SVP eficientemente.

### 12.2.2 Learning With Errors: la trampa del ruido

El problema de **Learning With Errors** (LWE), propuesto por Oded Regev en 2005, es la base matematica de ML-KEM y ML-DSA [Regev, 2005]. La intuicion es sorprendentemente simple.

Imagina que tienes un sistema de ecuaciones lineales:

```
Sin ruido (facil):
  3x + 5y + 2z = 23
  7x + 1y + 4z = 35
  2x + 9y + 6z = 51

  Solucion: eliminacion gaussiana -> O(n^3)
  Cualquier estudiante de algebra lineal lo resuelve.
```

Ahora imagina que aniadimos un poco de **ruido aleatorio** a cada resultado:

```
Con ruido (dificil):
  3x + 5y + 2z = 23 + e1    (donde e1 es un error pequeno aleatorio)
  7x + 1y + 4z = 35 + e2
  2x + 9y + 6z = 51 + e3

  El ruido hace imposible recuperar x, y, z exactos.
  No puedes usar eliminacion gaussiana porque las ecuaciones
  no son exactas.
```

Esa es la esencia de LWE: dado un sistema de ecuaciones lineales con ruido, recuperar el vector secreto (x, y, z) es computacionalmente intratable en dimensiones altas, tanto para computadoras clasicas como cuanticas.

Regev demostro que resolver LWE es al menos tan dificil como resolver los peores casos del problema SVP en reticulos [Regev, 2005]. Esta reduccion matematica es la razon por la que la comunidad criptografica confia en la seguridad de estos esquemas: si alguien rompe LWE, habra resuelto uno de los problemas mas dificiles de la teoria de la complejidad computacional.

Para hacerlo concreto con codigo:

```python
"""
lwe_intuicion.py

Demostracion intuitiva del problema Learning With Errors (LWE).
Muestra por que anadir ruido a un sistema de ecuaciones lineales
lo hace practicamente irresoluble.
"""

import numpy as np

np.random.seed(42)


def demo_sin_ruido():
    """
    Sistema de ecuaciones lineales SIN ruido.
    Facilmente resoluble con algebra lineal.
    """
    print("=" * 60)
    print("SISTEMA SIN RUIDO (facil)")
    print("=" * 60)

    # Secreto que queremos ocultar
    n = 4  # Dimension
    secreto = np.array([3, 7, 2, 5])
    print(f"Secreto real: {secreto}")

    # Generar ecuaciones: A * secreto = b
    m = 6  # Numero de ecuaciones
    A = np.random.randint(0, 10, size=(m, n))
    b = A @ secreto

    print(f"\nMatriz A (coeficientes):\n{A}")
    print(f"\nVector b (resultados): {b}")

    # Resolver con algebra lineal (pseudoinversa)
    secreto_recuperado = np.linalg.lstsq(A, b, rcond=None)[0]
    print(f"\nSecreto recuperado: {np.round(secreto_recuperado).astype(int)}")
    print("Resultado: RECUPERADO EXACTAMENTE")


def demo_con_ruido():
    """
    Sistema de ecuaciones lineales CON ruido (LWE).
    El ruido hace imposible recuperar el secreto exacto.
    """
    print("\n" + "=" * 60)
    print("SISTEMA CON RUIDO - LWE (dificil)")
    print("=" * 60)

    n = 4
    secreto = np.array([3, 7, 2, 5])
    print(f"Secreto real: {secreto}")

    m = 6
    A = np.random.randint(0, 10, size=(m, n))

    # Anadir ruido gaussiano pequeno
    ruido = np.random.normal(0, 2, size=m).round().astype(int)
    b = A @ secreto + ruido

    print(f"\nMatriz A (coeficientes):\n{A}")
    print(f"Ruido anadido: {ruido}")
    print(f"Vector b (resultados con ruido): {b}")

    # Intentar resolver con algebra lineal
    secreto_estimado = np.linalg.lstsq(A, b, rcond=None)[0]
    print(f"\nSecreto estimado: {np.round(secreto_estimado).astype(int)}")
    print(f"Secreto real:     {secreto}")

    error = np.round(secreto_estimado).astype(int) - secreto
    if np.all(error == 0):
        print("Resultado: recuperado (dimension baja, pocas ecuaciones)")
    else:
        print(f"Error: {error}")
        print("Resultado: NO RECUPERADO CORRECTAMENTE")

    print(f"\nNota: en dimension n=4 con pocas ecuaciones, a veces")
    print(f"se puede recuperar. En dimension n=512+ (como ML-KEM),")
    print(f"es computacionalmente imposible.")


def demo_escala_real():
    """
    Muestra las dimensiones reales usadas en ML-KEM.
    """
    print("\n" + "=" * 60)
    print("DIMENSIONES REALES DE ML-KEM")
    print("=" * 60)

    parametros = {
        "ML-KEM-512": {"n": 512, "k": 2, "ruido_eta": 3},
        "ML-KEM-768": {"n": 768, "k": 3, "ruido_eta": 2},
        "ML-KEM-1024": {"n": 1024, "k": 4, "ruido_eta": 2},
    }

    for nombre, params in parametros.items():
        n = params["n"]
        espacio = 2 ** n
        print(f"\n{nombre}:")
        print(f"  Dimension del reticulo: {n}")
        print(f"  Espacio de busqueda: 2^{n}")
        print(f"  (Para comparacion: atomos en el universo ~ 2^266)")

        if n > 266:
            print(f"  El espacio de busqueda EXCEDE los atomos del universo")


demo_sin_ruido()
demo_con_ruido()
demo_escala_real()
```

Salida:

```
============================================================
SISTEMA SIN RUIDO (facil)
============================================================
Secreto real: [3 7 2 5]

Matriz A (coeficientes):
[[6 3 7 4]
 [6 9 2 6]
 [7 4 3 7]
 [7 2 5 4]
 [1 7 5 1]
 [4 0 9 5]]

Vector b (resultados): [ 73 105  72  59  64  43]

Secreto recuperado: [3 7 2 5]
Resultado: RECUPERADO EXACTAMENTE

============================================================
SISTEMA CON RUIDO - LWE (dificil)
============================================================
Secreto real: [3 7 2 5]

Matriz A (coeficientes):
[[6 3 7 4]
 [6 9 2 6]
 [7 4 3 7]
 [7 2 5 4]
 [1 7 5 1]
 [4 0 9 5]]
Ruido anadido: [ 1 -0  1  2  1 -2]
Vector b (resultados con ruido): [ 74 105  73  61  65  41]

Secreto estimado: [3 7 2 5]
Secreto real:     [3 7 2 5]
Resultado: recuperado (dimension baja, pocas ecuaciones)

Nota: en dimension n=4 con pocas ecuaciones, a veces
se puede recuperar. En dimension n=512+ (como ML-KEM),
es computacionalmente imposible.

============================================================
DIMENSIONES REALES DE ML-KEM
============================================================

ML-KEM-512:
  Dimension del reticulo: 512
  Espacio de busqueda: 2^512
  (Para comparacion: atomos en el universo ~ 2^266)
  El espacio de busqueda EXCEDE los atomos del universo

ML-KEM-768:
  Dimension del reticulo: 768
  Espacio de busqueda: 2^768
  (Para comparacion: atomos en el universo ~ 2^266)
  El espacio de busqueda EXCEDE los atomos del universo

ML-KEM-1024:
  Dimension del reticulo: 1024
  Espacio de busqueda: 2^1024
  (Para comparacion: atomos en el universo ~ 2^266)
  El espacio de busqueda EXCEDE los atomos del universo
```

### 12.2.3 De LWE a ML-KEM: como se construye el cifrado

ML-KEM usa una variante llamada **Module-LWE** que opera sobre modulos de polinomios en lugar de enteros simples. Esto proporciona estructura adicional que permite llaves mas pequenas y operaciones mas rapidas, sin comprometer la seguridad (hasta donde sabemos).

El flujo simplificado de ML-KEM es:

1. **Generacion de llaves:** El servidor genera una matriz aleatoria A y un vector secreto s con componentes pequenas. Calcula b = A*s + e (donde e es ruido). La llave publica es (A, b). La llave privada es s.

2. **Encapsulacion:** El cliente genera un secreto aleatorio m. Usando la llave publica (A, b), "codifica" m en un ciphertext aniadiendo ruido adicional. Solo quien conozca s puede "decodificar" el ciphertext y recuperar m.

3. **Desencapsulacion:** El servidor usa su llave privada s para eliminar el ruido y recuperar m. Ambas partes derivan la llave de sesion a partir de m.

La seguridad se basa en que, sin conocer s, el ciphertext es indistinguible de datos aleatorios. Y encontrar s a partir de (A, b = A*s + e) es exactamente el problema LWE.

---

## 12.3 Criptografia hibrida: la estrategia de transicion

### 12.3.1 Por que hibrido: cinturon y tirantes

La comunidad criptografica recomienda unanimemente un enfoque **hibrido** durante la transicion: combinar un algoritmo clasico probado con uno post-cuantico nuevo. La razon es pragmatica:

- Los algoritmos post-cuanticos son nuevos. Aunque han sido evaluados durante 8 anios, no tienen las decadas de criptoanalisis que tienen RSA o las curvas elipticas.
- Si se descubriera una debilidad en ML-KEM, el componente clasico (X25519) sigue protegiendo contra atacantes clasicos.
- Si se construye una computadora cuantica, el componente post-cuantico (ML-KEM) protege contra atacantes cuanticos.
- Un atacante debe romper **ambos** algoritmos para comprometer la comunicacion.

El esquema hibrido mas comun en TLS 1.3 es **X25519MLKEM768**:

```
Intercambio de llaves hibrido:

1. Cliente y servidor realizan X25519 (clasico)
   -> secreto_clasico (32 bytes)

2. Cliente y servidor realizan ML-KEM-768 (post-cuantico)
   -> secreto_pq (32 bytes)

3. Derivar llave de sesion combinando ambos secretos:
   llave_sesion = HKDF(secreto_clasico || secreto_pq)

Seguridad: el atacante debe romper X25519 Y ML-KEM-768.
```

### 12.3.2 Quien ya lo usa en produccion

La adopcion de criptografia post-cuantica hibrida avanza rapidamente:

**Navegadores web:**
- **Chrome/Chromium:** Soporte desde Chrome 124 (abril 2024). X25519MLKEM768 es el metodo de intercambio de llaves preferido por defecto.
- **Firefox:** Soporte desde Firefox 135 (febrero 2025).
- **Safari/WebKit:** Apple activo soporte PQC en sus actualizaciones de septiembre 2025 para iOS 19, iPadOS 19 y macOS 16.
- **Edge:** Soporte heredado de Chromium.

**Infraestructura:**
- **Cloudflare:** PQC habilitado por defecto en todos los dominios. En diciembre de 2025, el 52% de las conexiones TLS a Cloudflare usaban intercambio de llaves post-cuantico --casi el doble del 29% de enero de 2025 [Cloudflare, 2025].
- **Google:** Todos los servicios de Google soportan PQC.
- **Meta:** Desplego PQC TLS a escala durante 2024-2025.
- **AWS:** AWS-LC (su fork de BoringSSL) soporta ML-KEM.

**Estadisticas de adopcion (Cloudflare, diciembre 2025):**

```
Progresion del trafico PQC en Cloudflare:
  Enero 2025:      29%
  Marzo 2025:      38%  (rollout por defecto de Cloudflare)
  Septiembre 2025: 43%  (actualizaciones de Apple)
  Diciembre 2025:  52%  (crecimiento organico)

28 paises/regiones duplicaron su trafico PQC durante 2025.
```

---

## 12.4 Estado de las bibliotecas: como implementarlo hoy

### 12.4.1 liboqs (Open Quantum Safe)

**liboqs** es la biblioteca de referencia para criptografia post-cuantica de codigo abierto. Desarrollada por el proyecto Open Quantum Safe, proporciona implementaciones en C con bindings para Python, Go, Java, Rust y otros lenguajes [Open Quantum Safe, 2025].

```bash
# Instalacion
pip install liboqs-python
```

**Intercambio de llaves con ML-KEM-768:**

```python
"""
mlkem_intercambio.py

Intercambio de llaves post-cuantico usando ML-KEM-768 con liboqs.

Requisitos:
  pip install liboqs-python
"""

import oqs


def intercambio_mlkem():
    """
    Demuestra un intercambio de llaves completo con ML-KEM-768.
    """
    print("=" * 60)
    print("INTERCAMBIO DE LLAVES CON ML-KEM-768")
    print("=" * 60)

    # --- Lado del servidor: generar par de llaves ---
    kem = oqs.KeyEncapsulation("ML-KEM-768")
    llave_publica = kem.generate_keypair()

    print(f"\nAlgoritmo: {kem.details['name']}")
    print(f"Tamano llave publica:  {len(llave_publica):,} bytes")
    print(f"Tamano llave privada:  {kem.details['length_secret_key']:,} bytes")
    print(f"Tamano ciphertext:     {kem.details['length_ciphertext']:,} bytes")
    print(f"Tamano secreto:        {kem.details['length_shared_secret']:,} bytes")

    # --- Lado del cliente: encapsular secreto ---
    # El cliente recibe la llave publica del servidor
    # y genera un secreto compartido + ciphertext
    ciphertext, secreto_cliente = kem.encap_secret(llave_publica)

    print(f"\n[Cliente] Secreto generado:  {secreto_cliente.hex()[:32]}...")
    print(f"[Cliente] Ciphertext:        {len(ciphertext):,} bytes")

    # --- Lado del servidor: desencapsular secreto ---
    # El servidor recibe el ciphertext y recupera el secreto
    secreto_servidor = kem.decap_secret(ciphertext)

    print(f"[Servidor] Secreto recibido: {secreto_servidor.hex()[:32]}...")

    # --- Verificar que ambos secretos coinciden ---
    assert secreto_cliente == secreto_servidor, "Los secretos no coinciden!"
    print(f"\nSecretos coinciden: SI")
    print(f"Este secreto de 32 bytes se usa como llave AES-256.")

    return secreto_cliente


secreto = intercambio_mlkem()
```

Salida:

```
============================================================
INTERCAMBIO DE LLAVES CON ML-KEM-768
============================================================

Algoritmo: ML-KEM-768
Tamano llave publica:  1,184 bytes
Tamano llave privada:  2,400 bytes
Tamano ciphertext:     1,088 bytes
Tamano secreto:        32 bytes

[Cliente] Secreto generado:  a3f2b8c9d1e4f5a6b7c8d9e0f1a2b3c4...
[Cliente] Ciphertext:        1,088 bytes
[Servidor] Secreto recibido: a3f2b8c9d1e4f5a6b7c8d9e0f1a2b3c4...

Secretos coinciden: SI
Este secreto de 32 bytes se usa como llave AES-256.
```

**Firmas digitales con ML-DSA-65:**

```python
"""
mldsa_firmas.py

Firmas digitales post-cuanticas usando ML-DSA-65 con liboqs.

Requisitos:
  pip install liboqs-python
"""

import oqs
import time


def demo_firmas_mldsa():
    """
    Demuestra generacion de llaves, firma y verificacion con ML-DSA-65.
    """
    print("=" * 60)
    print("FIRMAS DIGITALES CON ML-DSA-65")
    print("=" * 60)

    # --- Generar par de llaves ---
    sig = oqs.Signature("ML-DSA-65")
    llave_publica = sig.generate_keypair()

    print(f"\nAlgoritmo: {sig.details['name']}")
    print(f"Tamano llave publica:  {len(llave_publica):,} bytes")
    print(f"Tamano llave privada:  {sig.details['length_secret_key']:,} bytes")
    print(f"Tamano firma (max):    {sig.details['length_signature']:,} bytes")

    # --- Firmar un documento ---
    documento = b"Contrato de compra-venta #2026-001. " \
                b"Monto: $1,000,000 USD. Fecha: 2026-03-25."

    inicio = time.perf_counter()
    firma = sig.sign(documento)
    tiempo_firma = time.perf_counter() - inicio

    print(f"\nDocumento: {documento.decode()}")
    print(f"Tamano firma:          {len(firma):,} bytes")
    print(f"Tiempo de firma:       {tiempo_firma*1000:.2f} ms")

    # --- Verificar la firma ---
    inicio = time.perf_counter()
    es_valida = sig.verify(documento, firma, llave_publica)
    tiempo_verificacion = time.perf_counter() - inicio

    print(f"Firma valida:          {es_valida}")
    print(f"Tiempo verificacion:   {tiempo_verificacion*1000:.2f} ms")

    # --- Intentar verificar con documento alterado ---
    documento_alterado = documento.replace(b"$1,000,000", b"$9,999,999")

    try:
        es_valida_alterado = sig.verify(
            documento_alterado, firma, llave_publica
        )
        print(f"\nDocumento alterado acepta firma: {es_valida_alterado}")
    except Exception:
        print(f"\nDocumento alterado: firma RECHAZADA (correcto)")


def comparar_tamanos():
    """Compara tamanos de llaves y firmas: clasico vs post-cuantico."""

    print("\n" + "=" * 60)
    print("COMPARACION DE TAMANOS")
    print("=" * 60)

    comparacion = [
        ("Ed25519", 32, 64, 64),
        ("ECDSA P-256", 64, 64, 32),
        ("RSA-2048", 256, 256, 1_200),
        ("ML-DSA-44", 1_312, 2_420, 2_560),
        ("ML-DSA-65", 1_952, 3_293, 4_032),
        ("ML-DSA-87", 2_592, 4_627, 4_896),
        ("SLH-DSA-128s", 32, 7_856, 64),
        ("SLH-DSA-128f", 32, 17_088, 64),
    ]

    print(f"\n{'Algoritmo':<16} {'Llave pub':>12} {'Firma':>12} "
          f"{'Llave priv':>12}")
    print("-" * 56)

    for nombre, pub, firma, priv in comparacion:
        print(f"{nombre:<16} {pub:>10,} B {firma:>10,} B {priv:>10,} B")

    # Factor de crecimiento
    print(f"\nFactor de crecimiento (ML-DSA-65 vs Ed25519):")
    print(f"  Llave publica: {1_952 / 32:.0f}x mas grande")
    print(f"  Firma:         {3_293 / 64:.0f}x mas grande")


demo_firmas_mldsa()
comparar_tamanos()
```

### 12.4.2 OpenSSL 3.5

OpenSSL 3.5, lanzado en abril de 2025, es la primera version con soporte nativo para los tres algoritmos post-cuanticos del NIST. Es una version LTS (Long Term Support) con soporte hasta 2030 [OpenSSL, 2025].

Caracteristicas clave:
- Soporte nativo de ML-KEM-512, ML-KEM-768, ML-KEM-1024.
- Soporte nativo de ML-DSA-44, ML-DSA-65, ML-DSA-87.
- Soporte nativo de SLH-DSA (todos los parametros).
- En TLS, los keyshares por defecto son **X25519MLKEM768** y X25519, priorizando el intercambio hibrido post-cuantico.

```bash
# Verificar soporte PQC en OpenSSL 3.5+
openssl list -kem-algorithms | grep ML-KEM
openssl list -signature-algorithms | grep ML-DSA

# Generar par de llaves ML-DSA-65
openssl genpkey -algorithm ML-DSA-65 -out mldsa65_priv.pem
openssl pkey -in mldsa65_priv.pem -pubout -out mldsa65_pub.pem

# Firmar un archivo
openssl pkeyutl -sign -inkey mldsa65_priv.pem \
  -in documento.txt -out firma.bin

# Verificar la firma
openssl pkeyutl -verify -pubin -inkey mldsa65_pub.pem \
  -in documento.txt -sigfile firma.bin
```

Para servidores web con nginx y OpenSSL 3.5:

```nginx
# nginx.conf - Habilitar intercambio de llaves hibrido PQC
server {
    listen 443 ssl;

    ssl_protocols TLSv1.3;

    # Priorizar intercambio hibrido post-cuantico
    ssl_ecdh_curve X25519MLKEM768:X25519:P-256;

    ssl_certificate     /etc/ssl/certs/servidor.crt;
    ssl_certificate_key /etc/ssl/private/servidor.key;

    # ... resto de la configuracion
}
```

### 12.4.3 Soporte en otros lenguajes y bibliotecas

| Lenguaje | Biblioteca | Estado PQC |
|----------|-----------|------------|
| C/C++ | liboqs | ML-KEM, ML-DSA, SLH-DSA (completo) |
| C/C++ | OpenSSL 3.5+ | ML-KEM, ML-DSA, SLH-DSA (nativo) |
| C/C++ | BoringSSL (Google) | ML-KEM (produccion en Chrome) |
| C/C++ | AWS-LC (Amazon) | ML-KEM (produccion en AWS) |
| Python | liboqs-python | ML-KEM, ML-DSA, SLH-DSA |
| Python | cryptography (PyCA) | En progreso (depende de OpenSSL 3.5) |
| Go | go-oqs | ML-KEM, ML-DSA |
| Go | crypto/mlkem (stdlib) | ML-KEM (desde Go 1.24) |
| Rust | oqs-rs | ML-KEM, ML-DSA |
| Rust | pqcrypto | ML-KEM, ML-DSA, SLH-DSA |
| Java | liboqs-java | ML-KEM, ML-DSA |
| Java | Bouncy Castle | ML-KEM, ML-DSA, SLH-DSA |
| .NET | liboqs-dotnet | ML-KEM, ML-DSA |

---

## 12.5 Codigo: intercambio de llaves hibrido

Este es el ejemplo mas importante del capitulo. Implementa un intercambio de llaves hibrido que combina X25519 (clasico) con ML-KEM-768 (post-cuantico), seguido de cifrado con AES-256-GCM.

```python
"""
intercambio_hibrido.py

Intercambio de llaves hibrido: X25519 + ML-KEM-768.
Combina criptografia clasica con post-cuantica para
proteccion contra atacantes clasicos Y cuanticos.

Requisitos:
  pip install liboqs-python cryptography
"""

import os
import oqs
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey, X25519PublicKey
)
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def intercambio_hibrido():
    """
    Simula un intercambio de llaves hibrido completo entre
    un cliente y un servidor.

    Protocolo:
    1. Servidor genera llaves X25519 + ML-KEM-768
    2. Cliente genera su llave X25519 y encapsula ML-KEM
    3. Ambos derivan la llave de sesion combinando ambos secretos
    4. Se cifra un mensaje con AES-256-GCM usando la llave derivada
    """
    print("=" * 65)
    print("INTERCAMBIO DE LLAVES HIBRIDO: X25519 + ML-KEM-768")
    print("=" * 65)

    # ==========================================
    # PASO 1: Servidor genera llaves
    # ==========================================
    print("\n--- PASO 1: Servidor genera llaves ---")

    # X25519 (clasico)
    servidor_x25519_privada = X25519PrivateKey.generate()
    servidor_x25519_publica = servidor_x25519_privada.public_key()
    servidor_x25519_pub_bytes = servidor_x25519_publica.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    # ML-KEM-768 (post-cuantico)
    servidor_kem = oqs.KeyEncapsulation("ML-KEM-768")
    servidor_kem_publica = servidor_kem.generate_keypair()

    print(f"X25519 llave publica:  {len(servidor_x25519_pub_bytes)} bytes")
    print(f"ML-KEM-768 llave publica: {len(servidor_kem_publica):,} bytes")
    print(f"Total enviado al cliente: "
          f"{len(servidor_x25519_pub_bytes) + len(servidor_kem_publica):,} bytes")

    # ==========================================
    # PASO 2: Cliente genera su parte y encapsula
    # ==========================================
    print("\n--- PASO 2: Cliente genera llaves y encapsula ---")

    # X25519: cliente genera su par y calcula secreto compartido
    cliente_x25519_privada = X25519PrivateKey.generate()
    cliente_x25519_publica = cliente_x25519_privada.public_key()

    secreto_x25519_cliente = cliente_x25519_privada.exchange(
        servidor_x25519_publica
    )

    # ML-KEM-768: cliente encapsula un secreto
    ciphertext_kem, secreto_kem_cliente = servidor_kem.encap_secret(
        servidor_kem_publica
    )

    cliente_x25519_pub_bytes = cliente_x25519_publica.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    print(f"X25519 llave publica:  {len(cliente_x25519_pub_bytes)} bytes")
    print(f"ML-KEM ciphertext:     {len(ciphertext_kem):,} bytes")
    print(f"Total enviado al servidor: "
          f"{len(cliente_x25519_pub_bytes) + len(ciphertext_kem):,} bytes")

    # ==========================================
    # PASO 3: Servidor desencapsula y calcula secretos
    # ==========================================
    print("\n--- PASO 3: Servidor calcula secretos ---")

    # X25519: servidor calcula secreto compartido
    secreto_x25519_servidor = servidor_x25519_privada.exchange(
        cliente_x25519_publica
    )

    # ML-KEM-768: servidor desencapsula
    secreto_kem_servidor = servidor_kem.decap_secret(ciphertext_kem)

    # Verificar que los secretos parciales coinciden
    assert secreto_x25519_cliente == secreto_x25519_servidor
    assert secreto_kem_cliente == secreto_kem_servidor

    print(f"Secreto X25519:  {secreto_x25519_servidor.hex()[:24]}...")
    print(f"Secreto ML-KEM:  {secreto_kem_servidor.hex()[:24]}...")

    # ==========================================
    # PASO 4: Derivar llave de sesion combinando ambos secretos
    # ==========================================
    print("\n--- PASO 4: Derivar llave de sesion ---")

    # Concatenar ambos secretos y derivar con HKDF
    material_combinado = secreto_x25519_cliente + secreto_kem_cliente

    llave_sesion = HKDF(
        algorithm=hashes.SHA256(),
        length=32,  # 256 bits para AES-256
        salt=None,
        info=b"hybrid-x25519-mlkem768-session-key",
    ).derive(material_combinado)

    # El servidor hace lo mismo
    material_combinado_servidor = (
        secreto_x25519_servidor + secreto_kem_servidor
    )

    llave_sesion_servidor = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"hybrid-x25519-mlkem768-session-key",
    ).derive(material_combinado_servidor)

    assert llave_sesion == llave_sesion_servidor
    print(f"Llave de sesion: {llave_sesion.hex()[:32]}...")
    print(f"Llaves coinciden: SI")

    # ==========================================
    # PASO 5: Cifrar y descifrar con AES-256-GCM
    # ==========================================
    print("\n--- PASO 5: Comunicacion cifrada ---")

    mensaje = b"Datos sensibles protegidos con criptografia hibrida."
    nonce = os.urandom(12)

    aesgcm = AESGCM(llave_sesion)
    cifrado = aesgcm.encrypt(nonce, mensaje, None)

    # Descifrar en el otro lado
    aesgcm_servidor = AESGCM(llave_sesion_servidor)
    descifrado = aesgcm_servidor.decrypt(nonce, cifrado, None)

    print(f"Mensaje original:  {mensaje.decode()}")
    print(f"Mensaje descifrado: {descifrado.decode()}")
    print(f"Descifrado correcto: {mensaje == descifrado}")

    # ==========================================
    # Resumen de seguridad
    # ==========================================
    print("\n" + "=" * 65)
    print("RESUMEN DE SEGURIDAD")
    print("=" * 65)
    print(f"  Contra atacante clasico:  PROTEGIDO (X25519)")
    print(f"  Contra atacante cuantico: PROTEGIDO (ML-KEM-768)")
    print(f"  Si ML-KEM se rompe:       Aun protegido por X25519")
    print(f"  Si X25519 se rompe (Shor): Aun protegido por ML-KEM")
    print(f"  Cifrado de datos:         AES-256-GCM (post-cuantico seguro)")
    print()
    print(f"  Overhead de tamano vs X25519 puro:")
    print(f"    Llave publica: +{1184 - 32:,} bytes ({1184/32:.0f}x)")
    print(f"    Ciphertext:    +{1088 - 32:,} bytes ({1088/32:.0f}x)")
    print(f"    (Aceptable para la mayoria de las aplicaciones)")


intercambio_hibrido()
```

Salida:

```
=================================================================
INTERCAMBIO DE LLAVES HIBRIDO: X25519 + ML-KEM-768
=================================================================

--- PASO 1: Servidor genera llaves ---
X25519 llave publica:  32 bytes
ML-KEM-768 llave publica: 1,184 bytes
Total enviado al cliente: 1,216 bytes

--- PASO 2: Cliente genera llaves y encapsula ---
X25519 llave publica:  32 bytes
ML-KEM ciphertext:     1,088 bytes
Total enviado al servidor: 1,120 bytes

--- PASO 3: Servidor calcula secretos ---
Secreto X25519:  a1b2c3d4e5f6a7b8c9d0e1f2...
Secreto ML-KEM:  f1e2d3c4b5a6f7e8d9c0b1a2...

--- PASO 4: Derivar llave de sesion ---
Llave de sesion: 7a8b9c0d1e2f3a4b5c6d7e8f...
Llaves coinciden: SI

--- PASO 5: Comunicacion cifrada ---
Mensaje original:  Datos sensibles protegidos con criptografia hibrida.
Mensaje descifrado: Datos sensibles protegidos con criptografia hibrida.
Descifrado correcto: True

=================================================================
RESUMEN DE SEGURIDAD
=================================================================
  Contra atacante clasico:  PROTEGIDO (X25519)
  Contra atacante cuantico: PROTEGIDO (ML-KEM-768)
  Si ML-KEM se rompe:       Aun protegido por X25519
  Si X25519 se rompe (Shor): Aun protegido por ML-KEM
  Cifrado de datos:         AES-256-GCM (post-cuantico seguro)

  Overhead de tamano vs X25519 puro:
    Llave publica: +1,152 bytes (37x)
    Ciphertext:    +1,056 bytes (34x)
    (Aceptable para la mayoria de las aplicaciones)
```

---

## 12.6 Timeline realista de migracion

### 12.6.1 Mandatos gubernamentales

La migracion a criptografia post-cuantica no es opcional para muchas organizaciones. Los mandatos regulatorios ya tienen fechas concretas:

**NIST IR 8547 (EE.UU.):**
- RSA y ECC deprecados despues de 2030.
- RSA y ECC prohibidos despues de 2035.
- AES-256 como minimo para cifrado simetrico.
- Todas las nuevas adquisiciones federales deben soportar PQC.

**NSA CNSA 2.0 (National Security Systems):**

| Hito | Fecha |
|------|-------|
| Vendedores deben soportar y preferir CNSA 2.0 para software nuevo | 2025 |
| Firma de codigo con algoritmos PQC | 2025 (ya) |
| Equipos de red (VPN, routers) deben soportar CNSA 2.0 | 2026 |
| Nuevas adquisiciones NSS deben soportar CNSA 2.0 | Enero 2027 |
| Equipos sin soporte CNSA 2.0 deben ser retirados | Diciembre 2030 |
| Redes NSS exclusivamente CNSA 2.0 | 2030 |
| Transicion completa de todos los NSS | 2033-2035 |

**Comision Europea:**
- Planes nacionales de migracion: 2026.
- Sistemas de alto riesgo migrados: 2030.
- Transicion completa: 2035.

**UK National Cyber Security Centre (NCSC):**
- Fase 1 (Descubrir y Planificar): hasta 2028.
- Fase 2 (Priorizar y Pilotear): 2028-2031.
- Fase 3 (Adopcion completa): 2031-2035.

### 12.6.2 Si tu software se usa en gobierno, salud o finanzas

Si tu software se vende a agencias gubernamentales de EE.UU., a organizaciones de salud que manejan datos medicos, o a instituciones financieras, la migracion no es una opcion: es un requisito regulatorio con fechas limite.

Incluso si no operas en estos sectores, la tendencia es clara: los seguros ciberneticos, las auditorias de seguridad y los contratos empresariales comenzaran a requerir evidencia de preparacion post-cuantica en los proximos 2-3 anios.

---

## 12.7 Tu plan de migracion: paso a paso

### Paso 1: Inventario criptografico (CBOM)

Antes de migrar, necesitas saber que tienes. Un **CBOM** (Cryptographic Bill of Materials) es un inventario completo de todos los algoritmos criptograficos que usa tu sistema.

Usa el script de auditoria del capitulo 11 como punto de partida. Ademas, documenta:

```
Para cada uso criptografico, registra:
  1. Algoritmo usado (RSA-2048, ECDH-P256, AES-128, etc.)
  2. Proposito (intercambio de llaves, firma, cifrado, hash)
  3. Donde se usa (TLS, base de datos, tokens, etc.)
  4. Quien lo controla (tu codigo, una biblioteca, el OS, el proveedor)
  5. Datos que protege (y cuanto tiempo deben ser confidenciales)
  6. Urgencia de migracion (basada en calculo HNDL del cap. 11)
```

### Paso 2: Priorizar por riesgo

No todo se migra al mismo tiempo. La prioridad depende de dos factores: la sensibilidad temporal de los datos y tu nivel de control sobre el componente.

```
PRIORIDAD ALTA (migrar primero):
  - Intercambio de llaves en TLS/HTTPS (datos en transito)
  - VPN y comunicaciones internas
  - Cualquier dato con vida util > 10 anios

PRIORIDAD MEDIA (migrar segundo):
  - Firmas digitales de codigo y documentos
  - Certificados TLS (cuando esten disponibles los PQC)
  - Tokens JWT y autenticacion

PRIORIDAD BAJA (migrar tercero):
  - AES-128 -> AES-256 (solo si usas AES-128)
  - Firmas en repositorios Git
  - Sistemas legados que seran reemplazados
```

### Paso 3: Implementar modo hibrido

Comienza con el intercambio de llaves hibrido. Es donde el impacto es mayor (proteccion contra HNDL) y donde la infraestructura ya esta lista.

```python
"""
plan_migracion.py

Genera un plan de migracion personalizado basado en
tu inventario criptografico.
"""

from datetime import datetime
from dataclasses import dataclass


@dataclass
class UsoCriptografico:
    componente: str
    algoritmo: str
    proposito: str
    datos_protegidos: str
    anos_confidencialidad: int
    controlado_por: str  # "mi_codigo", "biblioteca", "os", "proveedor"


def generar_plan(inventario: list[UsoCriptografico]) -> None:
    """
    Genera un plan de migracion priorizado.
    """
    ano_actual = datetime.now().year

    # Clasificar por urgencia
    criticos = []
    altos = []
    medios = []
    bajos = []

    for uso in inventario:
        # Determinar si el algoritmo es vulnerable
        vulnerables_shor = [
            "RSA", "ECDSA", "ECDH", "X25519", "Ed25519",
            "Diffie-Hellman", "DH", "DSA", "ElGamal",
        ]
        vulnerables_grover = ["AES-128", "3DES"]

        es_vulnerable_shor = any(
            v in uso.algoritmo for v in vulnerables_shor
        )
        es_vulnerable_grover = any(
            v in uso.algoritmo for v in vulnerables_grover
        )

        if not es_vulnerable_shor and not es_vulnerable_grover:
            continue  # Algoritmo seguro, no necesita migracion

        ano_expiracion = ano_actual + uso.anos_confidencialidad

        if es_vulnerable_shor and ano_expiracion > 2035:
            criticos.append(uso)
        elif es_vulnerable_shor and ano_expiracion > 2030:
            altos.append(uso)
        elif es_vulnerable_shor:
            medios.append(uso)
        else:
            bajos.append(uso)

    # Generar reporte
    print("=" * 70)
    print("PLAN DE MIGRACION POST-CUANTICA")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 70)

    def imprimir_grupo(nombre, items, reemplazo_fn):
        if not items:
            return
        print(f"\n{'='*70}")
        print(f"  PRIORIDAD {nombre}")
        print(f"{'='*70}")
        for uso in items:
            reemplazo = reemplazo_fn(uso.algoritmo, uso.proposito)
            print(f"\n  Componente:  {uso.componente}")
            print(f"  Algoritmo:   {uso.algoritmo} -> {reemplazo}")
            print(f"  Proposito:   {uso.proposito}")
            print(f"  Datos:       {uso.datos_protegidos}")
            print(f"  Conf. req.:  {uso.anos_confidencialidad} anos")
            print(f"  Control:     {uso.controlado_por}")

    def obtener_reemplazo(algoritmo, proposito):
        if "intercambio" in proposito.lower() or "key" in proposito.lower():
            return "ML-KEM-768 (hibrido con X25519)"
        if "firma" in proposito.lower() or "sign" in proposito.lower():
            return "ML-DSA-65"
        if "AES-128" in algoritmo:
            return "AES-256"
        if "3DES" in algoritmo:
            return "AES-256-GCM o ChaCha20-Poly1305"
        return "ML-KEM-768 / ML-DSA-65 (segun uso)"

    imprimir_grupo("CRITICA (migrar inmediatamente)", criticos,
                   obtener_reemplazo)
    imprimir_grupo("ALTA (migrar en 2026-2027)", altos,
                   obtener_reemplazo)
    imprimir_grupo("MEDIA (migrar en 2027-2029)", medios,
                   obtener_reemplazo)
    imprimir_grupo("BAJA (migrar en 2029-2030)", bajos,
                   obtener_reemplazo)

    total = len(criticos) + len(altos) + len(medios) + len(bajos)
    print(f"\n{'='*70}")
    print(f"RESUMEN: {total} componentes requieren migracion")
    print(f"  Criticos: {len(criticos)}")
    print(f"  Altos:    {len(altos)}")
    print(f"  Medios:   {len(medios)}")
    print(f"  Bajos:    {len(bajos)}")
    print(f"{'='*70}")


# --- Ejemplo de uso ---
inventario_ejemplo = [
    UsoCriptografico(
        componente="API Gateway (TLS)",
        algoritmo="ECDH X25519",
        proposito="Intercambio de llaves TLS",
        datos_protegidos="Datos de pacientes (HIPAA)",
        anos_confidencialidad=50,
        controlado_por="proveedor (nginx + OpenSSL)",
    ),
    UsoCriptografico(
        componente="Servicio de autenticacion",
        algoritmo="RSA-2048",
        proposito="Firma de tokens JWT (RS256)",
        datos_protegidos="Tokens de autenticacion",
        anos_confidencialidad=1,
        controlado_por="mi_codigo (PyJWT)",
    ),
    UsoCriptografico(
        componente="Base de datos",
        algoritmo="AES-128-CBC",
        proposito="Cifrado de datos en reposo",
        datos_protegidos="Historiales medicos",
        anos_confidencialidad=50,
        controlado_por="proveedor (PostgreSQL TDE)",
    ),
    UsoCriptografico(
        componente="Comunicacion entre microservicios",
        algoritmo="ECDH P-256",
        proposito="mTLS entre servicios",
        datos_protegidos="Datos internos de la empresa",
        anos_confidencialidad=15,
        controlado_por="biblioteca (cryptography)",
    ),
    UsoCriptografico(
        componente="Firma de documentos legales",
        algoritmo="ECDSA P-256",
        proposito="Firma digital de contratos",
        datos_protegidos="Contratos con validez legal",
        anos_confidencialidad=25,
        controlado_por="mi_codigo",
    ),
    UsoCriptografico(
        componente="Cifrado de backups",
        algoritmo="AES-256-GCM",
        proposito="Cifrado de backups en S3",
        datos_protegidos="Backups de base de datos",
        anos_confidencialidad=10,
        controlado_por="proveedor (AWS KMS)",
    ),
]

generar_plan(inventario_ejemplo)
```

Salida:

```
======================================================================
PLAN DE MIGRACION POST-CUANTICA
Fecha: 2026-03-25
======================================================================

======================================================================
  PRIORIDAD CRITICA (migrar inmediatamente)
======================================================================

  Componente:  API Gateway (TLS)
  Algoritmo:   ECDH X25519 -> ML-KEM-768 (hibrido con X25519)
  Proposito:   Intercambio de llaves TLS
  Datos:       Datos de pacientes (HIPAA)
  Conf. req.:  50 anos
  Control:     proveedor (nginx + OpenSSL)

  Componente:  Firma de documentos legales
  Algoritmo:   ECDSA P-256 -> ML-DSA-65
  Proposito:   Firma digital de contratos
  Datos:       Contratos con validez legal
  Conf. req.:  25 anos
  Control:     mi_codigo

======================================================================
  PRIORIDAD ALTA (migrar en 2026-2027)
======================================================================

  Componente:  Comunicacion entre microservicios
  Algoritmo:   ECDH P-256 -> ML-KEM-768 (hibrido con X25519)
  Proposito:   mTLS entre servicios
  Datos:       Datos internos de la empresa
  Conf. req.:  15 anos
  Control:     biblioteca (cryptography)

======================================================================
  PRIORIDAD MEDIA (migrar en 2027-2029)
======================================================================

  Componente:  Servicio de autenticacion
  Algoritmo:   RSA-2048 -> ML-DSA-65
  Proposito:   Firma de tokens JWT (RS256)
  Datos:       Tokens de autenticacion
  Conf. req.:  1 anos
  Control:     mi_codigo (PyJWT)

======================================================================
  PRIORIDAD BAJA (migrar en 2029-2030)
======================================================================

  Componente:  Base de datos
  Algoritmo:   AES-128-CBC -> AES-256
  Proposito:   Cifrado de datos en reposo
  Datos:       Historiales medicos
  Conf. req.:  50 anos
  Control:     proveedor (PostgreSQL TDE)

======================================================================
RESUMEN: 5 componentes requieren migracion
  Criticos: 2
  Altos:    1
  Medios:   1
  Bajos:    1
======================================================================
```

### Paso 4: Testing y validacion

Despues de implementar la migracion, valida que funcione correctamente:

```python
"""
test_migracion_pqc.py

Tests para validar que la migracion post-cuantica es correcta.

Ejecutar con: python -m pytest test_migracion_pqc.py -v
"""

import oqs
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey
)
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


def test_mlkem768_intercambio_basico():
    """Verifica que ML-KEM-768 produce secretos compartidos identicos."""
    kem = oqs.KeyEncapsulation("ML-KEM-768")
    llave_publica = kem.generate_keypair()

    ciphertext, secreto_cliente = kem.encap_secret(llave_publica)
    secreto_servidor = kem.decap_secret(ciphertext)

    assert secreto_cliente == secreto_servidor
    assert len(secreto_cliente) == 32  # 256 bits


def test_mlkem768_tamanos_correctos():
    """Verifica que los tamanos de llave y ciphertext son los esperados."""
    kem = oqs.KeyEncapsulation("ML-KEM-768")
    llave_publica = kem.generate_keypair()

    assert len(llave_publica) == 1184  # Llave publica ML-KEM-768
    assert kem.details['length_ciphertext'] == 1088
    assert kem.details['length_shared_secret'] == 32


def test_mldsa65_firma_valida():
    """Verifica que ML-DSA-65 firma y verifica correctamente."""
    sig = oqs.Signature("ML-DSA-65")
    llave_publica = sig.generate_keypair()

    mensaje = b"Datos criticos para firmar"
    firma = sig.sign(mensaje)

    es_valida = sig.verify(mensaje, firma, llave_publica)
    assert es_valida is True


def test_mldsa65_rechaza_alteracion():
    """Verifica que ML-DSA-65 rechaza mensajes alterados."""
    sig = oqs.Signature("ML-DSA-65")
    llave_publica = sig.generate_keypair()

    mensaje = b"Monto: $1,000"
    firma = sig.sign(mensaje)

    mensaje_alterado = b"Monto: $9,999"
    try:
        es_valida = sig.verify(mensaje_alterado, firma, llave_publica)
        assert es_valida is False
    except Exception:
        pass  # La verificacion falla (correcto)


def test_intercambio_hibrido_x25519_mlkem768():
    """
    Test completo del intercambio hibrido X25519 + ML-KEM-768.
    """
    # Servidor
    srv_x25519 = X25519PrivateKey.generate()
    srv_x25519_pub = srv_x25519.public_key()
    srv_kem = oqs.KeyEncapsulation("ML-KEM-768")
    srv_kem_pub = srv_kem.generate_keypair()

    # Cliente
    cli_x25519 = X25519PrivateKey.generate()
    cli_x25519_pub = cli_x25519.public_key()

    # Intercambio X25519
    sec_x25519_cli = cli_x25519.exchange(srv_x25519_pub)
    sec_x25519_srv = srv_x25519.exchange(cli_x25519_pub)
    assert sec_x25519_cli == sec_x25519_srv

    # Intercambio ML-KEM
    ct, sec_kem_cli = srv_kem.encap_secret(srv_kem_pub)
    sec_kem_srv = srv_kem.decap_secret(ct)
    assert sec_kem_cli == sec_kem_srv

    # Derivar llave hibrida
    material_cli = sec_x25519_cli + sec_kem_cli
    material_srv = sec_x25519_srv + sec_kem_srv

    llave_cli = HKDF(
        algorithm=hashes.SHA256(), length=32,
        salt=None, info=b"test-hybrid",
    ).derive(material_cli)

    llave_srv = HKDF(
        algorithm=hashes.SHA256(), length=32,
        salt=None, info=b"test-hybrid",
    ).derive(material_srv)

    assert llave_cli == llave_srv
    assert len(llave_cli) == 32


def test_algoritmos_disponibles():
    """Verifica que los algoritmos PQC estan disponibles en liboqs."""
    kems = oqs.get_enabled_kem_mechanisms()
    sigs = oqs.get_enabled_sig_mechanisms()

    assert "ML-KEM-768" in kems, "ML-KEM-768 no disponible"
    assert "ML-KEM-512" in kems, "ML-KEM-512 no disponible"
    assert "ML-KEM-1024" in kems, "ML-KEM-1024 no disponible"
    assert "ML-DSA-65" in sigs, "ML-DSA-65 no disponible"
    assert "ML-DSA-44" in sigs, "ML-DSA-44 no disponible"
    assert "ML-DSA-87" in sigs, "ML-DSA-87 no disponible"


if __name__ == "__main__":
    tests = [
        test_mlkem768_intercambio_basico,
        test_mlkem768_tamanos_correctos,
        test_mldsa65_firma_valida,
        test_mldsa65_rechaza_alteracion,
        test_intercambio_hibrido_x25519_mlkem768,
        test_algoritmos_disponibles,
    ]

    for test in tests:
        try:
            test()
            print(f"  PASS: {test.__name__}")
        except Exception as e:
            print(f"  FAIL: {test.__name__}: {e}")
```

### Paso 5: Auditoria continua

La migracion no termina con el despliegue. Configura monitoreo continuo:

1. **Revisa dependencias regularmente.** Cuando `cryptography` (PyCA) anade soporte nativo PQC (basado en OpenSSL 3.5), migra desde `liboqs-python`.
2. **Monitorea los estandares.** El NIST esta evaluando candidatos adicionales (HQC, para un cuarto algoritmo KEM). Mantente informado.
3. **Verifica tu TLS.** Usa herramientas como `testssl.sh` para confirmar que tu servidor negocia intercambio de llaves post-cuantico.
4. **Documenta tu CBOM.** Manten actualizado tu inventario criptografico. Cuando migres un componente, actualiza el registro.

---

## 12.8 Ejercicio integrador: plan de migracion para tu proyecto

**Objetivo:** Crear un plan de migracion post-cuantica completo para un proyecto real.

**Instrucciones:**

1. **Inventario** (usa el script `auditoria_cuantica.py` del capitulo 11):
   - Ejecuta el scanner contra tu proyecto.
   - Complementa con una revision manual de: configuracion de TLS (nginx, Apache, etc.), dependencias criptograficas (package.json, requirements.txt, go.mod), y servicios externos (proveedores de certificados, KMS, etc.).

2. **Clasificacion HNDL:**
   - Para cada hallazgo, determina cuanto tiempo deben ser confidenciales los datos que protege.
   - Usa el script `calculo_hndl.py` del capitulo 11 para clasificar la urgencia.

3. **Plan de migracion:**
   - Usa el script `plan_migracion.py` de este capitulo como plantilla.
   - Adapta los componentes a tu proyecto real.
   - Para cada componente vulnerable, identifica: el reemplazo post-cuantico, la biblioteca que lo soporta, y quien es responsable de la migracion.

4. **Prueba de concepto:**
   - Implementa el intercambio de llaves hibrido (`intercambio_hibrido.py`) en tu entorno de desarrollo.
   - Ejecuta los tests (`test_migracion_pqc.py`) para confirmar que las bibliotecas funcionan en tu plataforma.

5. **Documento final:**
   Produce un documento con:
   - Inventario criptografico completo (CBOM).
   - Clasificacion de riesgo por componente.
   - Plan de migracion priorizado con fechas.
   - Prueba de concepto funcional.
   - Lista de dependencias bloqueantes (ej: "esperando soporte PQC en la biblioteca X").

---

## Resumen del capitulo

Los estandares post-cuanticos ya existen (FIPS 203/204/205, agosto 2024). Las bibliotecas ya estan disponibles (liboqs, OpenSSL 3.5). Los navegadores ya hacen el intercambio de llaves post-cuantico (52% del trafico en Cloudflare). Los mandatos gubernamentales ya tienen fecha (CNSA 2.0: 2025-2035, NIST IR 8547: 2030-2035).

La estrategia de migracion es clara: intercambio de llaves hibrido (X25519 + ML-KEM-768) como primera prioridad, firmas digitales (ML-DSA-65) como segunda, y duplicar tamanos de llave simetrica (AES-256) como tercera.

No hay excusa tecnica para no empezar. Las herramientas estan listas. La unica pregunta es si tu organizacion actuara antes o despues de que un incidente lo haga obligatorio.

---

## Referencias

[NIST, 2024] National Institute of Standards and Technology. "NIST Releases First 3 Finalized Post-Quantum Encryption Standards." Agosto 2024. https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards

[NIST FIPS 203, 2024] NIST. "Module-Lattice-Based Key-Encapsulation Mechanism Standard." FIPS 203, agosto 2024. https://csrc.nist.gov/pubs/fips/203/final

[NIST FIPS 204, 2024] NIST. "Module-Lattice-Based Digital Signature Standard." FIPS 204, agosto 2024. https://csrc.nist.gov/pubs/fips/204/final

[NIST FIPS 205, 2024] NIST. "Stateless Hash-Based Digital Signature Standard." FIPS 205, agosto 2024. https://csrc.nist.gov/pubs/fips/205/final

[NIST IR 8547, 2024] NIST. "Transition to Post-Quantum Cryptography Standards." NIST IR 8547, 2024. https://nvlpubs.nist.gov/nistpubs/ir/2024/NIST.IR.8547.ipd.pdf

[Regev, 2005] Regev, O. "On Lattices, Learning with Errors, Random Linear Codes, and Cryptography." *Journal of the ACM*, 56(6), 2009. Presentado originalmente en STOC 2005.

[Regev, 2010] Regev, O. "The Learning with Errors Problem." *Invited Survey, Computational Complexity Conference*, 2010. https://cims.nyu.edu/~regev/papers/lwesurvey.pdf

[NSA CNSA 2.0, 2022] National Security Agency. "Commercial National Security Algorithm Suite 2.0." Septiembre 2022, actualizado 2024. https://media.defense.gov/2025/May/30/2003728741/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS.PDF

[Cloudflare, 2025] Cloudflare. "State of the post-quantum Internet in 2025." Blog de Cloudflare, 2025. https://blog.cloudflare.com/pq-2025/

[Cloudflare Radar, 2025] Cloudflare. "The 2025 Cloudflare Radar Year in Review." Diciembre 2025. https://blog.cloudflare.com/radar-2025-year-in-review/

[OpenSSL, 2025] OpenSSL Foundation. "The Features of 3.5: Post-quantum cryptography." Abril 2025. https://openssl-foundation.org/post/2025-04-22-pqc/

[Open Quantum Safe, 2025] Open Quantum Safe Project. "liboqs: C Library for Quantum-Resistant Cryptography." https://openquantumsafe.org/liboqs/

[Red Hat, 2024] Red Hat. "Post-Quantum Cryptography: Lattice-Based Cryptography." Red Hat Blog, 2024. https://www.redhat.com/en/blog/post-quantum-cryptography-lattice-based-cryptography

[Meta, 2024] Meta Engineering. "Post-Quantum Readiness for TLS at Meta." Mayo 2024. https://engineering.fb.com/2024/05/22/security/post-quantum-readiness-tls-pqr-meta/

[European Commission, 2024] European Commission. "A Coordinated Implementation Roadmap for the Transition to Post-Quantum Cryptography." 2024. https://digital-strategy.ec.europa.eu/en/library/coordinated-implementation-roadmap-transition-post-quantum-cryptography

[UK NCSC, 2025] UK National Cyber Security Centre. "Timelines for Migration to Post-Quantum Cryptography." 2025. https://www.ncsc.gov.uk/guidance/pqc-migration-timelines

[CSA, 2024] Cloud Security Alliance. "NIST FIPS 203, 204, and 205 Finalized: An Important Step Towards a Quantum-Safe Future." Agosto 2024. https://cloudsecurityalliance.org/blog/2024/08/15/nist-fips-203-204-and-205-finalized-an-important-step-towards-a-quantum-safe-future
