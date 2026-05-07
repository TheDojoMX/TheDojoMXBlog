# Epilogo: Tu checklist criptografico permanente

> "La criptografia es un campo vivo. Los algoritmos que usas hoy no seran los mismos que uses en diez anios. Pero los principios que aprendiste en este libro --elegir la primitiva correcta, usarla con los parametros correctos, y no inventar lo que ya esta resuelto-- esos no cambian."

---

Llegaste al final de este libro. Has recorrido un camino que va desde tu primer hash en Python hasta la migracion a criptografia post-cuantica, pasando por las matematicas de la aritmetica modular, los internals de AES y SHA-3, la criptografia de curvas elipticas, los MACs, y los protocolos que sostienen Internet.

Este epilogo tiene un proposito concreto: darte una referencia rapida que puedas consultar cada vez que enfrentes una decision criptografica. No pretende reemplazar los capitulos anteriores, sino condensar las lecciones mas importantes en un formato que te permita actuar con confianza.

---

## Las 10 reglas de oro de la criptografia aplicada

Estas reglas destilan las lecciones de los trece capitulos anteriores. No son opcionales. Son el resultado de decadas de errores --muchos de ellos costosos-- de la comunidad de ingenieria de software.

### Regla 1: No implementes tu propia criptografia

Jamas. Usa bibliotecas probadas y auditadas: `cryptography` (PyCA), `libsodium`/`pynacl`, `ring` (Rust), o el modulo `crypto` de tu lenguaje cuando este bien mantenido. La criptografia correcta a nivel de algoritmo puede ser catastroficamente insegura a nivel de implementacion por timing attacks, manejo incorrecto de memoria, o generacion debil de aleatoriedad.

Esto no significa que no debas *entender* como funcionan los algoritmos --para eso leiste este libro. Significa que la comprension te permite *elegir y usar* las herramientas correctas, no *construirlas* desde cero.

### Regla 2: Usa cifrado autenticado, siempre

Nunca cifres sin autenticar. Usa AES-256-GCM o ChaCha20-Poly1305. Si necesitas cifrar y autenticar por separado (raro), aplica **encrypt-then-MAC** con HMAC-SHA-256. Los modos no autenticados (CBC sin HMAC, CTR sin MAC) son vulnerables a ataques de bit-flipping y padding oracle, como vimos en los capitulos 7, 8 y 10.

### Regla 3: Las llaves deben ser aleatorias de verdad

Usa generadores criptograficamente seguros: `os.urandom()` en Python, `crypto/rand` en Go, `SecureRandom` en Java, `/dev/urandom` en Linux. Jamas uses `random.random()`, `Math.random()`, ni numeros predecibles como timestamps, PIDs o direcciones de memoria (capitulo 8).

### Regla 4: Los nonces nunca se reutilizan

Un nonce (numero usado una sola vez) reutilizado con la misma llave destruye la seguridad de AES-GCM y ChaCha20-Poly1305. Genera un nonce aleatorio de 96 bits para cada operacion de cifrado, o usa un contador estrictamente creciente si puedes garantizar su persistencia. Si no puedes garantizar unicidad, considera AES-256-GCM-SIV, que es mas tolerante a nonces repetidos (capitulos 7 y 8).

### Regla 5: Los hashes de proposito general no sirven para contrasenas

SHA-256 hashea miles de millones de contrasenas por segundo en una GPU moderna. Usa **Argon2id** con parametros calibrados para tu hardware: minimo 64 MB de memoria, 3 iteraciones, y 4 hilos de paralelismo. Si Argon2 no esta disponible, usa bcrypt con cost 12 o superior. Nunca uses MD5, SHA-1, SHA-256 sin salt ni PBKDF2 como primera opcion (capitulo 5).

### Regla 6: Verifica siempre la identidad del otro lado

Cifrar un canal sin autenticar a la otra parte es vulnerable a ataques de intermediario (MITM). Verifica certificados TLS, valida hostnames, y no desactives la verificacion de certificados "para pruebas" en produccion. En APIs, firma los requests con HMAC o firmas digitales (capitulos 9 y 10).

### Regla 7: Usa forward secrecy

Prefiere intercambios de llaves efimeros (ECDHE con X25519) sobre transporte de llaves estaticas (RSA key transport). Si graban tu trafico hoy y roban tu llave manana, las sesiones pasadas deben seguir siendo seguras. TLS 1.3 impone esto; asegurate de que tu configuracion tambien lo haga (capitulos 9 y 13).

### Regla 8: Planifica para el cambio (agilidad criptografica)

Encapsula los algoritmos detras de interfaces abstractas. Almacena identificadores de algoritmo junto con los datos cifrados. Mantiene un inventario criptografico (CBOM). Cuando --no si-- necesites cambiar de algoritmo, el cambio debe ser de configuracion, no de codigo (capitulo 13).

### Regla 9: Prepara tu sistema para la era post-cuantica

Los algoritmos asimetricos clasicos (RSA, ECDSA, ECDH, Ed25519) seran vulnerables a computadoras cuanticas. Implementa intercambio de llaves hibrido (X25519 + ML-KEM-768) y planifica la migracion de firmas digitales a ML-DSA-65. El cifrado simetrico y los hashes sobreviven con tamanos de llave adecuados: AES-256 y SHA-256 son seguros (capitulos 11 y 12).

### Regla 10: La criptografia no es seguridad

La criptografia es una *herramienta* de seguridad, no la seguridad misma. De nada sirve AES-256-GCM si la llave esta hardcodeada en el codigo fuente, si el servidor tiene una inyeccion SQL que expone la base de datos, o si el usuario reutiliza contrasenas en todos los sitios. La criptografia protege datos; la seguridad es un sistema completo que incluye autenticacion, autorizacion, logging, actualizaciones, y cultura organizacional.

---

## Tabla de decision: que primitiva usar para cada caso

La siguiente tabla esta basada en las recomendaciones de Latacora ("Cryptographic Right Answers", edicion post-cuantica 2024), las guias del NIST, y los estandares estudiados en este libro. Es tu referencia rapida para elegir la herramienta correcta.

### Cifrado simetrico

| Necesitas | Usa | No uses | Capitulo |
|-----------|-----|---------|----------|
| Cifrar datos en reposo | AES-256-GCM | AES-CBC sin MAC, DES, 3DES, RC4 | 7 |
| Cifrar datos en transito | AES-256-GCM o ChaCha20-Poly1305 | Cualquier modo no autenticado | 7, 8 |
| Cifrar en dispositivos sin AES-NI | ChaCha20-Poly1305 | AES en software puro (lento, timing attacks) | 8 |
| Cifrado de disco | AES-256-XTS | AES-ECB, AES-CBC | 7 |
| Tamano de llave | 256 bits | 128 bits (marginal para PQ) | 6, 11 |

### Funciones hash

| Necesitas | Usa | No uses | Capitulo |
|-----------|-----|---------|----------|
| Hash de proposito general | SHA-256 o SHA-3-256 | MD5, SHA-1 | 1, 3, 4 |
| Hash de alto rendimiento | BLAKE3 | MD5, CRC32 | 4 |
| Cumplimiento regulatorio (FIPS) | SHA-3-256 | BLAKE (no FIPS) | 4 |
| Hash de salida variable (XOF) | SHAKE256 | Truncar SHA-256 | 4 |
| Integridad de archivos | SHA-256 o BLAKE3 | MD5, SHA-1 | 1 |

### Almacenamiento de contrasenas

| Necesitas | Usa | No uses | Capitulo |
|-----------|-----|---------|----------|
| Hashear contrasenas | Argon2id (64 MB, 3 iter, 4 hilos) | SHA-256, MD5, SHA-1, bcrypt < cost 10 | 5 |
| Si Argon2 no esta disponible | bcrypt (cost >= 12) | PBKDF2 con pocas iteraciones | 5 |
| Ultimo recurso | PBKDF2-SHA256 (600,000 iter) | SHA-256 con salt casero | 5 |

### Autenticacion de mensajes (MAC)

| Necesitas | Usa | No uses | Capitulo |
|-----------|-----|---------|----------|
| MAC de proposito general | HMAC-SHA-256 | HMAC-MD5, HMAC-SHA-1 | 10 |
| MAC integrado en cifrado | Poly1305 (via AEAD) | MAC casero, CRC32 | 10 |
| Firmar API requests | HMAC-SHA-256 con timestamp | MD5(secreto + mensaje) | 10 |

### Intercambio de llaves

| Necesitas | Usa | No uses | Capitulo |
|-----------|-----|---------|----------|
| Intercambio de llaves (clasico) | X25519 (ECDH) | RSA key transport, DH < 2048 | 9 |
| Intercambio de llaves (PQ-seguro) | X25519 + ML-KEM-768 (hibrido) | Solo clasico para datos de larga vida | 12 |
| Derivar llaves de un secreto | HKDF-SHA256 | Inventar tu propia KDF | 5 |

### Firmas digitales

| Necesitas | Usa | No uses | Capitulo |
|-----------|-----|---------|----------|
| Firmas digitales (clasico) | Ed25519 | RSA-1024, ECDSA con nonce deterministico | 9 |
| Firmas digitales (PQ-seguro) | ML-DSA-65 (o hibrido Ed25519 + ML-DSA) | Solo clasico para documentos de larga vida | 12 |
| Firmas conservadoras (maxima confianza) | SLH-DSA (basado en hash) | -- | 12 |
| Certificados TLS | ECDSA P-256 o Ed25519 (hoy); ML-DSA-65 (futuro) | RSA-2048 para nuevos certificados | 9, 12 |

### Generacion de aleatoriedad

| Necesitas | Usa | No uses | Capitulo |
|-----------|-----|---------|----------|
| Bytes aleatorios criptograficos | `os.urandom()` / `secrets` module | `random.random()`, timestamps, PIDs | 8 |
| Token aleatorio (URL-safe) | `secrets.token_urlsafe(32)` | UUID v4 como secreto, `random.choice()` | 8 |
| Nonce para AEAD | `os.urandom(12)` | Contador sin persistencia, timestamp | 7, 8 |

---

## Decision rapida: el arbol

Cuando no tengas tiempo para consultar la tabla completa, sigue este arbol:

```
Que necesitas proteger?
|
+-- Datos en transito (red)
|   -> Usa TLS 1.3 (no reinventes)
|   -> Si necesitas E2E: estudia Signal Protocol
|
+-- Datos en reposo (disco/DB)
|   +-- Contrasenas -> Argon2id
|   +-- Datos generales -> AES-256-GCM + llave en KMS
|   +-- Archivos -> AES-256-GCM con llave derivada de HKDF
|
+-- Integridad (no fue modificado?)
|   +-- Con llave secreta -> HMAC-SHA-256
|   +-- Sin llave (publico) -> SHA-256 o BLAKE3
|
+-- Autenticidad (quien lo envio?)
|   +-- Ambas partes tienen llave -> HMAC-SHA-256
|   +-- Solo el firmante tiene llave -> Ed25519 (o ML-DSA-65)
|
+-- Intercambio de llaves
|   -> X25519 + ML-KEM-768 (hibrido)
|   -> Derivar con HKDF-SHA256
```

---

## Recursos para seguir aprendiendo

### Libros

- **Serious Cryptography** (Jean-Philippe Aumasson, 2024, segunda edicion). El complemento natural de este libro. Cubre las mismas primitivas con mas profundidad matematica y ejemplos de ataques reales. La segunda edicion incluye criptografia post-cuantica.

- **Real-World Cryptography** (David Wong, 2021). Enfocado en protocolos y aplicaciones: TLS, Signal, Bitcoin, passwords. Excelente para entender como las primitivas se combinan en sistemas reales.

- **Cryptography Engineering** (Ferguson, Schneier, Kohno, 2010). Mas antiguo pero sigue siendo relevante para principios de diseno de sistemas criptograficos. La perspectiva de ingenieria --no solo matematica-- es unica.

- **A Graduate Course in Applied Cryptography** (Dan Boneh y Victor Shoup). Disponible gratuitamente en linea. Es el libro de texto mas completo y riguroso sobre criptografia moderna. Requiere comodidad con matematicas formales.

### Retos y practica

- **Cryptopals Crypto Challenges** (cryptopals.com). 48 ejercicios que te ensenan criptografia atacandola. Empiezas rompiendo XOR y terminas implementando ataques contra RSA y CBC padding oracle. Es probablemente el mejor recurso practico que existe.

- **CryptoHack** (cryptohack.org). Retos interactivos en el navegador, organizados por tema: introduccion, matematicas, RSA, Diffie-Hellman, curvas elipticas, AES. Mas accesible que Cryptopals.

- **CTFs (Capture The Flag)** con componente criptografico. Las competencias anuales como PicoCTF, Google CTF y CryptoHack incluyen desafios de criptografia que van desde basicos hasta investigacion de frontera.

### Cursos en linea

- **Cryptography I** de Dan Boneh (Stanford/Coursera). El curso mas influyente sobre criptografia moderna. Gratuito. Cubre lo que este libro cubre, pero con demostraciones matematicas formales.

- **Introduction to Cryptography** de Christof Paar (Ruhr University Bochum). Disponible en YouTube. Mas orientado a hardware y a la implementacion de bajo nivel.

### Estandares y documentos de referencia

- **NIST FIPS 197** (AES), **FIPS 180-4** (SHA-2), **FIPS 202** (SHA-3), **FIPS 203** (ML-KEM), **FIPS 204** (ML-DSA), **FIPS 205** (SLH-DSA). Los estandares oficiales. Son densos pero son la fuente de verdad.

- **NIST CSWP 39** (Considerations for Achieving Crypto Agility, 2025). La guia oficial para agilidad criptografica.

- **RFC 8446** (TLS 1.3), **RFC 7748** (X25519/X448), **RFC 8032** (Ed25519). Los estandares de Internet para los protocolos y algoritmos que usamos.

- **Latacora: Cryptographic Right Answers** (2024, edicion post-cuantica). Una guia concisa y opinada sobre que algoritmos usar. Actualizada regularmente.

### Comunidades

- **Real World Crypto** (rwc.iacr.org). La conferencia anual donde investigadores y practitioners presentan el estado del arte en criptografia aplicada.

- **IACR** (International Association for Cryptologic Research). Publica los proceedings de las conferencias Crypto, Eurocrypt y Asiacrypt, y mantiene el ePrint Archive donde se publican prepublicaciones.

---

## Cierre: la criptografia es un campo vivo

En el primer capitulo de este libro citamos un estudio del MIT que encontro que el **83% de las vulnerabilidades criptograficas no estaban en las librerias, sino en el codigo de aplicacion que las usaba mal** [Lazar, Chen y Zeldovich, 2014]. Ese dato fue la motivacion de todo lo que leiste despues.

Ahora, trece capitulos mas tarde, tienes las herramientas para estar en el otro 17%. Sabes que un hash no es un cifrado. Sabes por que AES-ECB es peligroso y AES-GCM es seguro. Sabes que los nonces no se reutilizan. Sabes que Argon2id existe y por que SHA-256 no sirve para contrasenas. Sabes que las llaves efimeras proporcionan forward secrecy. Sabes que las computadoras cuanticas amenazan la criptografia asimetrica pero no la simetrica, y que los estandares post-cuanticos ya estan listos.

Y sabes algo mas importante que cualquier algoritmo individual: sabes *hacer las preguntas correctas*. Que propiedad necesito? Quien es mi adversario? Estoy usando la herramienta correcta con los parametros correctos? Esas tres preguntas, que planteamos en el capitulo 1, son tu brujula permanente.

La criptografia no se queda quieta. Los algoritmos evolucionan. Nuevos ataques aparecen. Las computadoras se vuelven mas poderosas. Los estandares se actualizan. Pero los principios fundamentales --la confidencialidad, la integridad, la autenticacion, la aleatoriedad como recurso critico, la importancia de no reinventar lo que ya esta resuelto-- esos principios tienen decadas de validez por delante.

Este libro te dio las bases. Ahora tu trabajo es mantenerlas actualizadas. Revisa las recomendaciones del NIST periodicamente. Lee los "Cryptographic Right Answers" de Latacora cuando se actualicen. Sigue las conferencias Real World Crypto. Y cuando dudes, recurre a la regla mas simple de todas: **no inventes, no improvises, usa lo que la comunidad criptografica ha probado y validado**.

La criptografia no es solo para criptografos. Es para todo desarrollador que se toma en serio la proteccion de los datos que le confian. Y ahora, tu eres uno de ellos.

---

## Referencias citadas en este epilogo

- Lazar, D., Chen, H., Wang, X. y Zeldovich, N. (2014). *Why does cryptographic software fail? A case study and open problems*. 5th Asia-Pacific Workshop on Systems (APSys '14).
- NIST (2025). *CSWP 39: Considerations for Achieving Crypto Agility: Strategies and Practices*.
- Latacora (2024). *Cryptographic Right Answers: Post Quantum Edition*.
- Aumasson, J.-P. (2024). *Serious Cryptography*, segunda edicion. No Starch Press.
- Wong, D. (2021). *Real-World Cryptography*. Manning.
- Ferguson, N., Schneier, B. y Kohno, T. (2010). *Cryptography Engineering*. Wiley.
- Boneh, D. y Shoup, V. (2023). *A Graduate Course in Applied Cryptography*. Disponible en https://toc.cryptobook.us/.

---
