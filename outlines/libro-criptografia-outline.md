# Criptografia Aplicada para Desarrolladores

## Outline Completo del Libro

**Autor:** Hector Patricio
**Palabras estimadas totales:** ~85,000-95,000
**Capitulos:** 13 + Prologo + Apendices
**Audiencia:** Desarrolladores de software con experiencia intermedia que quieren dominar criptografia aplicada

---

## Principios de estructura

1. **Front-load del valor**: El lector escribe su primer hash en Python antes de la pagina 15
2. **Primer "a-ha" antes de pagina 20**: "Cambiar un solo bit de la entrada cambia completamente el hash"
3. **Teaching Conversations**: Cada capitulo abre con una pregunta provocadora y un escenario real
4. **Matematicas DESPUES de la motivacion**: Cap 2 llega cuando el lector ya quiere saber el "por que"
5. **Vulnerabilidades reales como ancla emocional**: Cada primitiva se ata a un incidente de seguridad real

---

## PROLOGO: Por que este libro existe

**Palabras:** ~2,000
**Tipo:** [CASO REAL]
**Post base:** criptografia-basica-para-programadores-que-es-la-criptografia.md (parcial)
**Contenido nuevo:** Todo, excepto la definicion basica de criptografia

### Secciones

#### P.1 La historia del bug que costo 600 millones de dolares (~500 palabras)
- Abrir con el caso de Mt. Gox (2014): maleabilidad de transacciones Bitcoin
- Desarrolladores que NO entendian criptografia construyeron un exchange
- Conectar con: "Este libro existe para que no seas tu"

#### P.2 Para quien es este libro (~500 palabras)
- Desarrolladores con 2+ anios de experiencia
- No necesitas ser matematico
- Lo que SI necesitas: Python basico, curiosidad, tolerancia a la incomodidad
- Lo que NO es este libro: un tratado academico, una guia de hacking

#### P.3 Como leer este libro (~500 palabras)
- Ruta rapida (Caps 1, 3, 8, 11): "Necesito saber que usar YA"
- Ruta completa: Secuencial, con ejercicios
- Ruta profunda: Incluye matematicas y ejercicios avanzados
- Todos los ejemplos en Python 3.10+ con hashlib, cryptography, y liboqs

#### P.4 Convenciones y setup del entorno (~500 palabras)
- Instalar Python, pip install cryptography pynacl argon2-cffi
- Notacion usada: [PELIGRO], [BUENA PRACTICA], [PROFUNDIZAR]
- Repositorio de codigo companiero del libro

**Takeaway:** La criptografia no es solo para criptografos; cada desarrollador la usa a diario, y usarla mal tiene consecuencias reales y costosas.

---

## CAPITULO 1: Tu primer hash en 10 minutos (Intro + Hashes fusionados)

**Palabras:** ~8,000
**Hook:** "Si cambias una sola coma en la Constitucion de Mexico y la hasheas, el resultado es completamente diferente. Pero si hasheas el universo entero, el resultado tiene el mismo tamano. Como es eso posible?"
**Post base:** criptografia-basica-para-programadores-que-es-la-criptografia.md + algoritmos-criptograficos-que-es-un-hash.md
**Takeaway:** Un hash es una huella digital de los datos: pequena, unica en la practica, e irreversible. Es la herramienta criptografica mas comun que usaras.
**Ejercicio del capitulo:** Construir un verificador de integridad de archivos en Python que detecte si un archivo fue modificado.

### Secciones

#### 1.1 Que es la criptografia y por que te importa (~1,200 palabras)
**Tipo:** [TEORIA]
**Post base:** criptografia-basica-para-programadores-que-es-la-criptografia.md
**Contenido nuevo:** Actualizar ejemplos a 2026, agregar contexto de APIs, microservicios, TLS en todas partes

- 1.1.1 Definicion moderna de criptografia (~400 palabras)
  - Escritura oculta: de Julio Cesar a TLS 1.3
  - Cifrado vs descifrado (y por que "encriptar" no existe en espanol)
  - La triada: confidencialidad, integridad, autenticacion

- 1.1.2 Donde se usa la criptografia en tu stack diario (~400 palabras)
  - HTTPS/TLS en cada request
  - Passwords en la base de datos
  - Tokens JWT, cookies firmadas
  - Git commits (SHA-1 internamente)
  - Cifrado de disco, WiFi, SSH

- 1.1.3 Esteganografia: la prima oculta (~400 palabras)
  - Diferencia entre ocultar y cifrar
  - Micro-puntos en impresiones, datos en imagenes
  - Por que la criptografia es mas importante hoy

#### 1.2 Tu primer hash: manos al codigo (~1,500 palabras)
**Tipo:** [CODIGO PYTHON]
**Post base:** algoritmos-criptograficos-que-es-un-hash.md
**Contenido nuevo:** Ejercicio guiado paso a paso, efecto avalancha demostrado con codigo

- 1.2.1 La metafora del picadillo (~300 palabras)
  - Hash viene de "picar": datos de entrada se pican hasta ser irreconocibles
  - Entrada de cualquier tamano, salida de tamano fijo
  - Analogia: una licuadora que siempre llena el mismo vaso

- 1.2.2 Hashea tu primer mensaje (~500 palabras)
  ```python
  from hashlib import sha256
  mensaje = b"Hola mundo"
  h = sha256(mensaje).hexdigest()
  print(h)  # 64 caracteres hexadecimales
  ```
  - Ejercicio: hashea tu nombre, tu email, un archivo
  - Observacion: sin importar el tamano de la entrada, la salida siempre tiene 64 hex chars

- 1.2.3 El efecto avalancha: la prueba de fuego (~400 palabras)
  ```python
  h1 = sha256(b"Hola mundo").hexdigest()
  h2 = sha256(b"Hola Mundo").hexdigest()  # Solo una mayuscula
  # h1 y h2 son completamente diferentes
  # PRIMER "A-HA" DEL LIBRO
  ```
  - Cambiar 1 bit -> ~50% de los bits de salida cambian
  - Esto es lo que hace a un hash "criptografico"

- 1.2.4 Propiedades formales de un hash (~300 palabras)
  - Tamano fijo de salida
  - Determinismo
  - Rapidez
  - Irreversibilidad (se pierde informacion)

#### 1.3 Hashes criptograficos: cuando "picar" no es suficiente (~2,000 palabras)
**Tipo:** [TEORIA] + [CODIGO PYTHON]
**Post base:** algoritmos-criptograficos-que-es-un-hash.md
**Contenido nuevo:** Explicacion mas detallada de las tres resistencias, diagramas ASCII

- 1.3.1 Hashes no criptograficos vs criptograficos (~400 palabras)
  - `hash()` de Python, fnv1a, SeaHash: rapidos pero predecibles
  - Un hash criptografico es impredecible incluso para una computadora
  - Resistente a analisis estadisticos

- 1.3.2 Las tres resistencias (~800 palabras)
  - **Resistencia a preimagen**: dado un hash h, no puedes encontrar un mensaje m tal que hash(m) = h
  - **Resistencia a segunda preimagen**: dado m1, no puedes encontrar m2 != m1 tal que hash(m1) = hash(m2)
  - **Resistencia a colisiones**: no puedes encontrar ningun par (m1, m2) con m1 != m2 tal que hash(m1) = hash(m2)
  - Diagrama de preimagen/imagen
  - Codigo: intentar encontrar una colision parcial (primeros 4 bytes) por fuerza bruta

- 1.3.3 Catalogo de funciones hash seguras (~800 palabras)
  - **MD5**: ROTO. 128 bits. Colisiones en segundos. No usar NUNCA.
  - **SHA-1**: ROTO. 160 bits. Google demostro colision en 2017 (SHAttered). Git lo usa aun pero esta migrando.
  - **SHA-2 (SHA-256, SHA-512)**: Seguro. Estandar actual. Bitcoin lo usa.
  - **SHA-3 (Keccak)**: Seguro. Diseno completamente diferente. Recomendado para nuevos proyectos.
  - **BLAKE2/BLAKE3**: Seguro. Mas rapido que SHA-3. Excelente para rendimiento.
  - Tabla comparativa: tamano de salida, velocidad relativa, estado de seguridad

#### 1.4 Que hash usar y cuando (~1,300 palabras)
**Tipo:** [TEORIA] + [CASO REAL]
**Post base:** algoritmos-criptograficos-que-es-un-hash.md (seccion final)
**Contenido nuevo:** Arbol de decision, casos de uso reales, vulnerabilidades

- 1.4.1 Arbol de decision para elegir un hash (~400 palabras)
  - Necesitas velocidad -> BLAKE3
  - Necesitas estandar -> SHA-3-256
  - Compatibilidad con sistemas existentes -> SHA-256
  - Passwords -> NUNCA un hash de proposito general (ver Cap 5)
  - Tabla resumen

- 1.4.2 Caso real: SHAttered - la muerte de SHA-1 (~500 palabras)
  **Tipo:** [VULNERABILIDAD]
  - Google y CWI Amsterdam generan dos PDFs diferentes con el mismo SHA-1
  - Impacto: certificados TLS, firmas de codigo, Git
  - Leccion: la depreciacion es urgente, no "cuando tengamos tiempo"

- 1.4.3 Caso real: Flame malware y MD5 (~400 palabras)
  **Tipo:** [VULNERABILIDAD]
  - Malware estatal (2012) que forjo un certificado de Microsoft usando colision MD5
  - Windows Update entrego malware firmado "legitimamente"
  - Leccion: un hash roto en una parte de la cadena compromete todo

#### 1.5 Ejercicio integrador: Verificador de integridad de archivos (~1,000 palabras)
**Tipo:** [EJERCICIO]
**Contenido nuevo:** 100%

```python
# integrity_checker.py
# Programa que:
# 1. Recibe un directorio como argumento
# 2. Calcula SHA-3-256 de cada archivo
# 3. Guarda los hashes en un archivo JSON
# 4. En ejecuciones posteriores, compara y reporta archivos modificados/nuevos/eliminados
```

- Paso 1: Calcular hashes de un directorio
- Paso 2: Almacenar el manifiesto
- Paso 3: Detectar cambios
- Extension: agregar firma HMAC al manifiesto (adelanto del Cap 11)

---

## CAPITULO 2: Las matematicas detras de la cortina

**Palabras:** ~7,000
**Hook:** "No necesitas un doctorado en matematicas para usar criptografia. Pero si quieres entender POR QUE puedes confiar tu dinero, tu identidad y tus secretos a un algoritmo, necesitas entender cinco conceptos. Solo cinco."
**Post base:** matematicas-para-criptografia.md
**Contenido nuevo:** ~70%. El post es un listado de recursos; el capitulo necesita ENSENAR las matematicas con ejemplos y codigo.
**Takeaway:** La criptografia se sostiene sobre aritmetica modular, numeros primos, y la dificultad de revertir ciertas operaciones. Estos conceptos son accesibles para cualquier programador.
**Ejercicio del capitulo:** Implementar el cifrado de Cesar y el cifrado afin usando aritmetica modular en Python.

### Secciones

#### 2.1 Aritmetica modular: el reloj de la criptografia (~1,500 palabras)
**Tipo:** [MATEMATICAS] + [CODIGO PYTHON]
**Post base:** matematicas-para-criptografia.md (mencion de teoria de numeros)
**Contenido nuevo:** 95%

- 2.1.1 La analogia del reloj (~300 palabras)
  - 15:00 horas es lo mismo que 3:00 PM: 15 mod 12 = 3
  - En criptografia, trabajamos siempre "dentro del reloj"
  - Operador % en Python

- 2.1.2 Operaciones modulares (~500 palabras)
  - Suma, resta, multiplicacion modular
  - Exponenciacion modular: pow(base, exp, mod)
  - Por que la exponenciacion modular es una "trampa": facil de calcular, dificil de revertir
  ```python
  # Facil: calcular 7^123 mod 1000
  result = pow(7, 123, 1000)
  # Dificil: dado result y 7, encontrar 123 (logaritmo discreto)
  ```

- 2.1.3 El inverso modular (~400 palabras)
  - Concepto: el "reverso" de una multiplicacion en un espacio modular
  - Algoritmo extendido de Euclides
  - pow(a, -1, m) en Python 3.8+

- 2.1.4 El cifrado de Cesar como aritmetica modular (~300 palabras)
  ```python
  def cifrado_cesar(texto, k):
      return ''.join(chr((ord(c) - 65 + k) % 26 + 65) for c in texto.upper() if c.isalpha())
  ```

#### 2.2 Numeros primos: los atomos de la criptografia (~1,500 palabras)
**Tipo:** [MATEMATICAS] + [CODIGO PYTHON]
**Contenido nuevo:** 100%

- 2.2.1 Que es un numero primo y por que importa (~400 palabras)
  - Definicion: solo divisible por 1 y por si mismo
  - El teorema fundamental de la aritmetica: todo entero se descompone en primos de forma unica
  - Conexion: RSA depende de que factorizar sea dificil

- 2.2.2 Generacion de primos grandes (~500 palabras)
  - El test de primalidad de Miller-Rabin (probabilistico)
  - Como genera Python numeros primos para criptografia
  ```python
  from Crypto.Util.number import getPrime
  p = getPrime(2048)  # Un primo de 2048 bits
  ```
  - Por que necesitamos primos de 2048+ bits

- 2.2.3 El problema de la factorizacion (~600 palabras)
  - Multiplicar dos primos: instantaneo
  - Factorizar el producto: computacionalmente intratable para numeros grandes
  - Ejemplo con numeros pequenos vs grandes
  - Conexion directa con RSA (adelanto)

#### 2.3 XOR: la operacion perfecta para cifrar (~1,000 palabras)
**Tipo:** [MATEMATICAS] + [CODIGO PYTHON]
**Post base:** tipos-de-algoritmos-criptograficos-cifrados-de-flujo.md (mencion de XOR)
**Contenido nuevo:** 80%

- 2.3.1 Tabla de verdad de XOR (~300 palabras)
  - 0 XOR 0 = 0, 0 XOR 1 = 1, 1 XOR 0 = 1, 1 XOR 1 = 0
  - Propiedad magica: A XOR B XOR B = A (involucion)
  - Por que es perfecta para cifrado: aplica la llave, aplica de nuevo para descifrar

- 2.3.2 El one-time pad: cifrado perfecto (~400 palabras)
  - Cifrado perfecto de Vernam
  - Por que es perfecto: la llave es tan larga como el mensaje y completamente aleatoria
  - Por que no se usa: distribucion de llaves
  ```python
  import os
  mensaje = b"secreto"
  llave = os.urandom(len(mensaje))
  cifrado = bytes(a ^ b for a, b in zip(mensaje, llave))
  descifrado = bytes(a ^ b for a, b in zip(cifrado, llave))
  ```

- 2.3.3 Por que XOR sin aleatoriedad no sirve (~300 palabras)
  **Tipo:** [VULNERABILIDAD]
  - Caso: cifrado XOR con llave repetida
  - Ataque: analisis de frecuencia
  - Leccion: la herramienta perfecta usada mal es peor que nada

#### 2.4 Campos finitos y curvas elipticas: una vision panoramica (~1,500 palabras)
**Tipo:** [MATEMATICAS]
**Post base:** matematicas-para-criptografia.md (mencion de algebra lineal, geometria analitica)
**Contenido nuevo:** 95%

- 2.4.1 Campos finitos (Galois Fields) (~500 palabras)
  - GF(p): numeros del 0 al p-1 con aritmetica modular
  - GF(2^8): el campo que usa AES internamente
  - Por que los campos finitos son utiles: todo se queda dentro de un rango

- 2.4.2 Curvas elipticas intuitivamente (~500 palabras)
  - La ecuacion y^2 = x^3 + ax + b
  - Suma de puntos en la curva (geometricamente)
  - El problema del logaritmo discreto en curvas elipticas
  - Por que 256 bits de ECC equivalen a 3072 bits de RSA

- 2.4.3 Mapa de conexiones: que matematica usa cada algoritmo (~500 palabras)
  - Tabla: Algoritmo -> Concepto matematico -> Problema dificil
  - AES -> Campos finitos GF(2^8) -> Confusion/difusion
  - RSA -> Factorizacion de primos -> Factorizacion
  - ECDSA -> Curvas elipticas -> Logaritmo discreto
  - ML-KEM -> Reticulas -> Learning With Errors

#### 2.5 Ejercicio integrador: cifrado afin y ataque (~500 palabras)
**Tipo:** [EJERCICIO]
**Contenido nuevo:** 100%

```python
# Implementar cifrado afin: E(x) = (ax + b) mod 26
# Implementar descifrado usando inverso modular
# Implementar ataque de fuerza bruta (solo 12*26 = 312 llaves posibles)
# Reflexion: por que el espacio de llaves tan pequeno lo hace inseguro
```

---

## CAPITULO 3: MD5 y SHA-2 -- Los caballos de batalla

**Palabras:** ~7,000
**Hook:** "En 2012, un malware llamado Flame se hizo pasar por una actualizacion oficial de Windows. La razon: MD5 llevaba anos roto, pero Microsoft seguia usandolo para firmar actualizaciones. Cuanto cuesta no migrar a tiempo?"
**Post base:** algoritmos-criptograficos-que-es-un-hash.md (secciones sobre MD5, SHA-1, SHA-2)
**Contenido nuevo:** ~75%. Necesita internals de Merkle-Damgard, ataques detallados, historia.
**Takeaway:** Entender COMO se rompe un hash te ensena POR QUE confiar en los que aun no se han roto. SHA-2 sigue siendo seguro, pero no para siempre.
**Ejercicio del capitulo:** Implementar una version simplificada de Merkle-Damgard y demostrar el ataque de extension de longitud.

### Secciones

#### 3.1 La construccion de Merkle-Damgard (~1,500 palabras)
**Tipo:** [TEORIA] + [MATEMATICAS]
**Post base:** crea-hashes-resistentes-a-balas-con-keccak.md (mencion de Merkle-Damgard)
**Contenido nuevo:** 90%

- 3.1.1 Como se construye un hash de proposito general (~500 palabras)
  - La funcion de compresion: toma un bloque + estado anterior -> nuevo estado
  - Padding del mensaje
  - Valor inicial (IV)
  - Diagrama paso a paso

- 3.1.2 Fortalezas del diseno (~400 palabras)
  - Teorema: si la funcion de compresion es resistente a colisiones, el hash completo tambien
  - Eficiencia: procesa bloques secuencialmente, usa poca memoria

- 3.1.3 Debilidad critica: ataque de extension de longitud (~600 palabras)
  **Tipo:** [VULNERABILIDAD]
  - El estado final es publico, se puede continuar hasheando
  - hash(secreto || mensaje) es vulnerable
  - Impacto: firmado de APIs, tokens, autenticacion casera
  - Codigo demostrativo del ataque
  ```python
  # Demostrar que conociendo hash(m1) puedes calcular hash(m1 || padding || m2)
  # sin conocer m1
  ```

#### 3.2 MD5: autopsia de un hash roto (~1,500 palabras)
**Tipo:** [TEORIA] + [VULNERABILIDAD]
**Contenido nuevo:** 90%

- 3.2.1 Diseno y operacion de MD5 (~400 palabras)
  - Ron Rivest, 1991
  - 128 bits de salida, bloques de 512 bits
  - 4 rondas de 16 operaciones cada una

- 3.2.2 Historia de los ataques (~500 palabras)
  - 1996: Dobbertin encuentra pseudo-colisiones
  - 2004: Wang et al. encuentran colisiones en 1 hora
  - 2006: colisiones en segundos en una laptop
  - 2008: investigadores crean un certificado CA falso usando colision MD5
  - 2012: Flame malware (detalle extendido)

- 3.2.3 Por que MD5 sigue en uso y por que debes eliminarlo (~300 palabras)
  - Checksums no criptograficos (aceptable con reservas)
  - Sistemas legacy, compatibilidad
  - Herramientas para detectar uso de MD5 en tu codebase

- 3.2.4 Caso real: Flame y los certificados de Microsoft (~300 palabras)
  **Tipo:** [VULNERABILIDAD]
  - Detalle tecnico del ataque chosen-prefix collision
  - Impacto en Windows Update

#### 3.3 SHA-1: la depreciacion mas lenta de la historia (~1,000 palabras)
**Tipo:** [TEORIA] + [VULNERABILIDAD]
**Contenido nuevo:** 85%

- 3.3.1 De SHA-0 a SHA-1 (~300 palabras)
  - NSA diseno SHA-0 (1993), encontraron flaw, publicaron SHA-1 (1995)
  - 160 bits de salida
  - Dominante por 15 anos

- 3.3.2 SHAttered: el clavo final (~400 palabras)
  - Google + CWI Amsterdam, 2017
  - Dos PDFs diferentes, mismo SHA-1
  - 6,500 anos de CPU + 110 anos de GPU (equivalente)
  - Impacto en Git, certificados, firmas

- 3.3.3 La leccion de la depreciacion gradual (~300 palabras)
  - Chrome empezando a marcar SHA-1 como inseguro en 2014
  - CAs dejando de emitir certificados SHA-1 en 2016
  - Git aun en transicion a SHA-256 en 2026
  - Analogia: cambiar las tuberias de una casa mientras vives en ella

#### 3.4 SHA-2: el estandar actual (~1,500 palabras)
**Tipo:** [TEORIA] + [CODIGO PYTHON]
**Post base:** algoritmos-criptograficos-que-es-un-hash.md (seccion sobre SHA-2)
**Contenido nuevo:** 70%

- 3.4.1 Familia SHA-2: variantes y tamanos (~400 palabras)
  - SHA-224, SHA-256, SHA-384, SHA-512
  - SHA-512/256: truncado seguro
  - Tamano de bloque vs tamano de salida
  - Tabla de comparacion

- 3.4.2 Por que SHA-2 sigue siendo seguro (~400 palabras)
  - Ningun ataque practico conocido
  - Margen de seguridad amplio
  - Diferencias con SHA-1 que hacen los ataques mas dificiles

- 3.4.3 SHA-256 en la practica (~400 palabras)
  ```python
  import hashlib
  # Hash de un archivo grande por bloques
  def hash_archivo(ruta, bloque=65536):
      h = hashlib.sha256()
      with open(ruta, 'rb') as f:
          while bloque_datos := f.read(bloque):
              h.update(bloque_datos)
      return h.hexdigest()
  ```

- 3.4.4 Caso real: Bitcoin y SHA-256 (~300 palabras)
  **Tipo:** [CASO REAL]
  - Proof of Work: encontrar un nonce tal que SHA-256(bloque + nonce) empiece con N ceros
  - Por que SHA-256 y no otro hash
  - El costo energetico de la seguridad

#### 3.5 Ejercicio integrador: ataque de extension de longitud (~1,000 palabras)
**Tipo:** [EJERCICIO]
**Contenido nuevo:** 100%

```python
# Implementar:
# 1. Un "servidor" que firma mensajes con: SHA-256(secreto || mensaje)
# 2. Un "atacante" que, sin conocer el secreto, extiende el mensaje firmado
# 3. Demostrar que el servidor acepta el mensaje extendido
# 4. Corregir el servidor usando HMAC (adelanto del Cap 11)
```

---

## CAPITULO 4: SHA-3 y Keccak -- La esponja que absorbe el futuro

**Palabras:** ~6,500
**Hook:** "Que pasaria si todos los hashes de la familia SHA compartieran una misma debilidad estructural? El NIST decidio no esperar a descubrirlo: organizo una competencia global para encontrar un sucesor con un diseno radicalmente diferente. Gano un algoritmo que se parece mas a una esponja que a una trituradora."
**Post base:** crea-hashes-resistentes-a-balas-con-keccak-tambien-llamado-sha-3.md
**Contenido nuevo:** ~50%. El post cubre bien la esponja, pero falta historia del concurso, comparacion profunda, XOFs.
**Takeaway:** SHA-3 no es solo "otro SHA" -- es una arquitectura completamente diferente que abre la puerta a funciones de salida extensible y otras primitivas flexibles. Es el hash que deberias elegir para nuevos proyectos.
**Ejercicio del capitulo:** Implementar una construccion de esponja simplificada en Python y comparar rendimiento de SHA-2 vs SHA-3 vs BLAKE3.

### Secciones

#### 4.1 El concurso SHA-3: como se elige un estandar (~1,000 palabras)
**Tipo:** [CASO REAL]
**Contenido nuevo:** 90%

- 4.1.1 Por que el NIST lanzo un concurso (~300 palabras)
  - SHA-1 roto, SHA-2 tiene el mismo diseno
  - Diversidad algoritmica como seguro contra catastrofe
  - 2007: convocatoria abierta, 64 candidatos

- 4.1.2 Los finalistas (~400 palabras)
  - BLAKE, Grostl, JH, Keccak, Skein
  - Criterios: seguridad, rendimiento en software/hardware, simplicidad
  - Por que Keccak gano: diseno completamente novedoso, no depende de Merkle-Damgard

- 4.1.3 La polemica de los parametros (~300 palabras)
  - NIST redujo la capacidad de seguridad respecto a la propuesta original
  - La comunidad cripto reacciono con preocupacion
  - Resultado: SHA-3 final es seguro pero con margen menor al propuesto

#### 4.2 Construccion de esponja: como funciona Keccak (~2,000 palabras)
**Tipo:** [TEORIA] + [MATEMATICAS]
**Post base:** crea-hashes-resistentes-a-balas-con-keccak.md (seccion de esponja)
**Contenido nuevo:** 40%

- 4.2.1 La funcion de permutacion keccak-f (~500 palabras)
  - Permutacion de 1600 bits (5x5 matriz de 64 bits)
  - 24 rondas de transformaciones
  - Operaciones: theta, rho, pi, chi, iota
  - No es un cifrado, es una permutacion: no usa llave

- 4.2.2 Absorcion y exprimido (~600 palabras)
  - Fase de absorcion: XOR del mensaje con el estado + permutacion
  - Fase de exprimido: extraer bits del estado + permutacion
  - Rate (velocidad) vs Capacity (seguridad): el compromiso fundamental
  - Diagrama paso a paso (reproducir y expandir el del post)

- 4.2.3 Por que la esponja es inmune al ataque de extension de longitud (~400 palabras)
  - La capacidad oculta bits que el atacante no puede ver ni manipular
  - Comparacion directa con Merkle-Damgard
  - Implicacion practica: SHA-3(secreto || mensaje) es seguro (aunque HMAC sigue siendo mejor practica)

- 4.2.4 Implementacion simplificada de una esponja (~500 palabras)
  **Tipo:** [CODIGO PYTHON]
  ```python
  # Esponja con permutacion XOR-rotate-XOR simplificada
  # Solo para demostrar el concepto, NO para produccion
  def esponja_simple(mensaje, rate=4, capacity=4, output_len=4):
      state = [0] * (rate + capacity)
      # Fase de absorcion
      for bloque in dividir_en_bloques(mensaje, rate):
          for i in range(rate):
              state[i] ^= bloque[i]
          state = permutacion_simple(state)
      # Fase de exprimido
      output = []
      while len(output) < output_len:
          output.extend(state[:rate])
          state = permutacion_simple(state)
      return bytes(output[:output_len])
  ```

#### 4.3 Variantes de SHA-3 y funciones de salida extensible (~1,000 palabras)
**Tipo:** [TEORIA] + [CODIGO PYTHON]
**Post base:** crea-hashes-resistentes-a-balas-con-keccak.md (seccion de tamanos)
**Contenido nuevo:** 60%

- 4.3.1 SHA-3-224/256/384/512 (~300 palabras)
  - Tamanos de salida fijos
  - Bits de seguridad de cada variante
  - Cual elegir: SHA-3-256 para uso general

- 4.3.2 SHAKE128 y SHAKE256: funciones de salida extensible (XOF) (~400 palabras)
  - XOF: puedes pedir la cantidad de bytes que necesites
  - Uso: generacion de llaves, derivacion, protocolos
  ```python
  from hashlib import shake_256
  # Obtener 64 bytes de salida
  h = shake_256(b"semilla").digest(64)
  ```

- 4.3.3 TupleHash, ParallelHash, cSHAKE (~300 palabras)
  - Funciones derivadas estandarizadas por NIST
  - TupleHash: hash de tuplas sin ambiguedad
  - ParallelHash: hasheo paralelizable para archivos grandes
  - cSHAKE: personalizacion del hash para separacion de dominios

#### 4.4 BLAKE2 y BLAKE3: la alternativa rapida (~1,000 palabras)
**Tipo:** [TEORIA] + [CODIGO PYTHON]
**Post base:** algoritmos-criptograficos-que-es-un-hash.md (mencion de BLAKE2)
**Contenido nuevo:** 80%

- 4.4.1 BLAKE2: de finalista a favorito (~400 palabras)
  - Mas rapido que MD5, tan seguro como SHA-3
  - BLAKE2b (64 bits) vs BLAKE2s (32 bits)
  - Usado en: Argon2, WireGuard, IPFS

- 4.4.2 BLAKE3: el hash mas rapido (~300 palabras)
  - Arbol de Merkle interno: paralelizable nativamente
  - 2-3x mas rapido que BLAKE2
  ```python
  # pip install blake3
  import blake3
  h = blake3.blake3(b"datos").hexdigest()
  ```

- 4.4.3 SHA-3 vs BLAKE3: cual elegir (~300 palabras)
  - SHA-3: estandar NIST, maxima confianza regulatoria
  - BLAKE3: maximo rendimiento, excelente seguridad
  - Decision practica: SHA-3 si necesitas cumplimiento, BLAKE3 si necesitas velocidad

#### 4.5 Ejercicio integrador (~500 palabras)
**Tipo:** [EJERCICIO]
**Contenido nuevo:** 100%

```python
# 1. Benchmark: SHA-256 vs SHA-3-256 vs BLAKE3 hasheando un archivo de 1GB
# 2. Implementar construccion de esponja simplificada (expandir 4.2.4)
# 3. Usar SHAKE256 como generador de bytes pseudo-aleatorios
# 4. Verificar que SHA-3 no es vulnerable a extension de longitud
```

---

## CAPITULO 5: Hashes para passwords -- El arte de ser lento a proposito

**Palabras:** ~7,000
**Hook:** "En 2012, LinkedIn perdio 6.5 millones de passwords. Estaban hasheados con SHA-1 sin salt. Un atacante con una GPU de $500 pudo descifrar el 90% en menos de 72 horas. El problema no era el hash. El problema era que era demasiado rapido."
**Post base:** algoritmos-criptograficos-hashes-seguros-para-alamcenar-passwords.md
**Contenido nuevo:** ~45%. El post cubre bien los algoritmos pero falta profundidad en ataques, configuracion, casos reales.
**Takeaway:** Los hashes de proposito general son PELIGROSOS para passwords porque son rapidos. Usa Argon2id con parametros calibrados para tu hardware.
**Ejercicio del capitulo:** Implementar un sistema de registro/login seguro con Argon2id en Python, incluyendo calibracion de parametros.

### Secciones

#### 5.1 Por que los hashes normales no sirven para passwords (~1,200 palabras)
**Tipo:** [TEORIA] + [VULNERABILIDAD]
**Post base:** algoritmos-criptograficos-hashes-seguros-para-alamcenar-passwords.md (intro + ataques)
**Contenido nuevo:** 30%

- 5.1.1 El error mas comun en seguridad web (~400 palabras)
  - SHA-256(password) parece seguro pero no lo es
  - Velocidad de hasheo: millones de intentos por segundo en GPU
  - hashcat y las GPU modernas: benchmarks reales

- 5.1.2 Ataques de fuerza bruta y diccionario (~400 palabras)
  - Listas de passwords comunes (rockyou.txt: 14 millones de passwords)
  - Reglas de mutacion: "password" -> "P@ssw0rd1!"
  - Hardware: NVIDIA RTX 4090 hashea ~25 mil millones de SHA-256/s

- 5.1.3 Rainbow tables (~400 palabras)
  - Tablas pre-calculadas de hash -> password
  - Intercambio tiempo-memoria
  - Existen rainbow tables para MD5, SHA-1, SHA-256 sin salt

#### 5.2 Salt: la primera defensa (~800 palabras)
**Tipo:** [TEORIA] + [CODIGO PYTHON]
**Post base:** algoritmos-criptograficos-hashes-seguros-para-alamcenar-passwords.md (seccion de salt)
**Contenido nuevo:** 50%

- 5.2.1 Que es un salt y como funciona (~400 palabras)
  - Valor aleatorio unico por usuario
  - hash(salt + password): invalida rainbow tables
  - El salt NO es secreto: se almacena junto al hash

- 5.2.2 Errores comunes con salt (~400 palabras)
  - Salt global (mismo para todos): NO SIRVE
  - Salt corto o predecible: reduce proteccion
  - Salt como pepper (secreto): util pero diferente proposito
  ```python
  import os
  salt = os.urandom(16)  # Salt minimo: 16 bytes
  ```

#### 5.3 Los cuatro jinetes del hashing de passwords (~2,500 palabras)
**Tipo:** [TEORIA] + [CODIGO PYTHON]
**Post base:** algoritmos-criptograficos-hashes-seguros-para-alamcenar-passwords.md (seccion de algoritmos)
**Contenido nuevo:** 40%

- 5.3.1 PBKDF2: el veterano (~500 palabras)
  - Aplica hash N veces iterativamente
  - Configurable: iteraciones, algoritmo base, tamano de salida
  - Debilidad: solo intensivo en CPU, no en memoria -> vulnerable a GPU/ASIC
  - Django lo usaba por defecto (ya no recomendado como primera opcion)
  ```python
  import hashlib
  dk = hashlib.pbkdf2_hmac('sha256', b'password', salt, 600000)
  ```

- 5.3.2 bcrypt: el popular (~500 palabras)
  - Basado en Blowfish, cost factor configurable
  - Salt automatico, formato $2b$
  - Debilidad: limitado a 72 bytes de entrada, vulnerable a FPGA
  - Estudio de 2011 sobre ataques con hardware especializado
  ```python
  import bcrypt
  hashed = bcrypt.hashpw(b'password', bcrypt.gensalt(rounds=12))
  ```

- 5.3.3 scrypt: el memory-hard (~500 palabras)
  - Intensivo en CPU Y en memoria
  - Parametros: N (CPU/memoria), r (tamano de bloque), p (paralelismo)
  - Resistente a GPU, FPGA, ASIC
  - Usado en Litecoin como proof of work
  ```python
  import hashlib
  dk = hashlib.scrypt(b'password', salt=salt, n=2**14, r=8, p=1)
  ```

- 5.3.4 Argon2: el estado del arte (~1,000 palabras)
  - Ganador del Password Hashing Competition (2015)
  - Tres variantes: Argon2d, Argon2i, Argon2id
  - Parametros: memoria, iteraciones, paralelismo, tamano de hash
  - Argon2id: hibrido recomendado para la mayoria de casos
  - Como calibrar parametros para tu hardware
  ```python
  from argon2 import PasswordHasher
  ph = PasswordHasher(
      time_cost=3,        # iteraciones
      memory_cost=65536,   # 64 MB
      parallelism=4,
      hash_len=32,
      salt_len=16
  )
  hash = ph.hash("mi_password_seguro")
  assert ph.verify(hash, "mi_password_seguro")
  ```

#### 5.4 Funciones de derivacion de llaves (KDF) (~700 palabras)
**Tipo:** [TEORIA]
**Post base:** algoritmos-criptograficos-hashes-seguros-para-alamcenar-passwords.md (nota sobre KDF)
**Contenido nuevo:** 60%

- 5.4.1 De password a llave de cifrado (~300 palabras)
  - KDF: genera bytes pseudo-aleatorios a partir de un secreto
  - Diferencia: password hashing busca lentitud, KDF busca derivacion segura
  - HKDF: la KDF estandar para extraer-y-expandir

- 5.4.2 Cuando usar una KDF vs un password hash (~400 palabras)
  - Almacenar password: Argon2id
  - Derivar llave de cifrado desde password: Argon2id + HKDF
  - Derivar multiples llaves de una master key: HKDF
  - Tabla de decision

#### 5.5 Casos reales de filtraciones (~800 palabras)
**Tipo:** [VULNERABILIDAD]
**Contenido nuevo:** 100%

- 5.5.1 LinkedIn (2012): SHA-1 sin salt (~300 palabras)
  - 6.5 millones de hashes filtrados
  - 90% crackeados en 72 horas

- 5.5.2 Adobe (2013): 3DES en modo ECB (~300 palabras)
  - 153 millones de cuentas
  - Cifrado simetrico en vez de hash: error conceptual
  - ECB: patrones visibles revelaron passwords populares

- 5.5.3 Dropbox (2012, revelado 2016): bcrypt bien hecho (~200 palabras)
  - bcrypt + salt: la filtracion fue menos grave
  - Leccion: usar el algoritmo correcto mitiga el dano

#### 5.6 Ejercicio integrador: sistema de login seguro (~1,000 palabras)
**Tipo:** [EJERCICIO]
**Contenido nuevo:** 100%

```python
# Implementar:
# 1. Registro de usuario con Argon2id
# 2. Login con verificacion y deteccion de parametros obsoletos
# 3. Re-hash automatico cuando los parametros cambian
# 4. Calibracion de parametros: medir tiempo en tu hardware
# 5. Pepper opcional desde variable de entorno
```

---

## CAPITULO 6: Complejidad computacional -- Por que confiamos en la criptografia

**Palabras:** ~7,000
**Hook:** "Imagina que te doy el numero 15 y te pido que encuentres sus factores primos. Facil: 3 y 5. Ahora imagina que te doy un numero de 617 digitos. El mejor algoritmo conocido tardaria mas que la edad del universo. Toda la seguridad de internet descansa sobre esa asimetria."
**Post base:** problemas-dificiles-de-la-computacion-y-su-relacion-con-la-criptografia.md + maquinas-de-turing-no-deterministas-y-problemas-np.md
**Contenido nuevo:** ~40%. Los posts cubren bien P, NP, Big O, pero falta conexion explicita con cada primitiva criptografica y ejemplos computacionales.
**Takeaway:** La criptografia no promete "imposible" sino "tan dificil que nadie con los recursos del planeta puede hacerlo en un tiempo razonable". Esa confianza se basa en la teoria de complejidad computacional.
**Ejercicio del capitulo:** Medir experimentalmente la complejidad de factorizar numeros de tamano creciente y extrapolar para tamanos criptograficos.

### Secciones

#### 6.1 Complejidad computacional para criptografos (~1,500 palabras)
**Tipo:** [TEORIA] + [CODIGO PYTHON]
**Post base:** problemas-dificiles-de-la-computacion.md (secciones de complejidad y Big O)
**Contenido nuevo:** 30%

- 6.1.1 Que es complejidad computacional (~400 palabras)
  - Relacion entre tamano de entrada y operaciones requeridas
  - Ejemplo: contar letras = O(n), busqueda binaria = O(log n)

- 6.1.2 Notacion Big O (~400 palabras)
  - Limite superior asintotico
  - O(1), O(n), O(n^2), O(2^n): de trivial a imposible
  - Constantes no importan: O(2n) = O(n)

- 6.1.3 Complejidad polinomial vs exponencial (~700 palabras)
  - P: resoluble en tiempo polinomial
  - EXP: resoluble en tiempo exponencial
  - La frontera: numeros concretos
    - 2^128 operaciones: mas que los atomos del universo (~2^80)
    - Ejemplo numerico con la supercomputadora Frontier
  ```python
  # Demostrar la explosion exponencial
  import time
  for n in range(20, 30):
      start = time.time()
      # "Busqueda exhaustiva" simulada
      for i in range(2**n):
          pass
      print(f"2^{n} = {2**n:>12,} iteraciones: {time.time()-start:.3f}s")
  ```

#### 6.2 Clases de complejidad P, NP y mas alla (~1,500 palabras)
**Tipo:** [TEORIA]
**Post base:** problemas-dificiles-de-la-computacion.md (seccion NP) + maquinas-de-turing-no-deterministas.md
**Contenido nuevo:** 35%

- 6.2.1 La clase P (~300 palabras)
  - Problemas con solucion eficiente garantizada
  - Ejemplos: ordenar una lista, busqueda binaria, multiplicar matrices

- 6.2.2 La clase NP (~500 palabras)
  - "Facil de verificar, dificil de encontrar"
  - Maquinas de Turing no deterministas
  - Ejemplo criptografico: verificar una llave AES es O(1), encontrarla es O(2^n)

- 6.2.3 NP-Complete y NP-Hard (~400 palabras)
  - Los problemas mas dificiles de NP
  - Si resuelves uno en tiempo polinomial, resuelves todos
  - Problema del viajante, satisfactibilidad booleana

- 6.2.4 P vs NP: el misterio del millon de dolares (~300 palabras)
  - Si P = NP, la criptografia colapsa
  - Por que la mayoria cree que P != NP
  - Lo que "creemos que es dificil" vs lo que "probamos que es dificil"

#### 6.3 Problemas dificiles que sostienen la criptografia (~2,000 palabras)
**Tipo:** [TEORIA] + [CODIGO PYTHON]
**Contenido nuevo:** 85%

- 6.3.1 Factorizacion de enteros (~500 palabras)
  - Base de RSA
  - Multiplicar primos: O(n^2). Factorizar: mejor algoritmo conocido es sub-exponencial
  - General Number Field Sieve: O(exp(c * n^(1/3) * (log n)^(2/3)))
  ```python
  # Factorizacion ingenua vs tamano del numero
  def factorizar_ingenuo(n):
      factores = []
      d = 2
      while d * d <= n:
          while n % d == 0:
              factores.append(d)
              n //= d
          d += 1
      if n > 1:
          factores.append(n)
      return factores
  # Medir tiempos para numeros de 10, 20, 30, 40 digitos
  ```

- 6.3.2 Logaritmo discreto (~500 palabras)
  - Base de Diffie-Hellman, DSA, ElGamal
  - g^x mod p = y: dado g, p, y, encontrar x
  - Tan dificil como factorizar (heuristicamente)

- 6.3.3 Logaritmo discreto en curvas elipticas (~400 palabras)
  - Base de ECDSA, ECDH, EdDSA
  - Sin algoritmo sub-exponencial conocido: mas eficiente que factorizacion
  - Por que 256 bits de ECC ~ 3072 bits de RSA

- 6.3.4 Learning With Errors (LWE) (~600 palabras)
  - Base de la criptografia post-cuantica (ML-KEM, ML-DSA)
  - Sistema de ecuaciones lineales con "ruido" anadido
  - Dificil para computadoras clasicas Y cuanticas
  - Conexion con el Cap 13

#### 6.4 Bits de seguridad: la metrica universal (~1,000 palabras)
**Tipo:** [TEORIA]
**Contenido nuevo:** 100%

- 6.4.1 Que significa "128 bits de seguridad" (~400 palabras)
  - Un atacante necesita 2^128 operaciones en promedio
  - Equivalencias fisicas: energia del sol, atomos del universo
  - Tabla: bits de seguridad de cada algoritmo comun

- 6.4.2 El principio del eslabon mas debil (~300 palabras)
  - AES-256 (256 bits) + SHA-256 (128 bits de seguridad contra colision) = 128 bits
  - La seguridad del sistema es la del componente mas debil
  - Error comun: mezclar niveles de seguridad

- 6.4.3 Recomendaciones de NIST para 2026-2030 (~300 palabras)
  - Minimo 128 bits de seguridad
  - Recomendado 256 bits para proteccion a largo plazo
  - Tabla de algoritmos por nivel

#### 6.5 Ejercicio integrador (~500 palabras)
**Tipo:** [EJERCICIO]
**Contenido nuevo:** 100%

```python
# 1. Medir tiempo de factorizacion para primos de 8, 16, 24, 32, 40 digitos
# 2. Graficar el crecimiento (matplotlib)
# 3. Extrapolar: cuanto tardaria factorizar un RSA-2048?
# 4. Comparar con fuerza bruta de AES-128: cuantas operaciones?
# 5. Calcular: con la Frontier (10^18 ops/s), cuanto tardaria cada ataque?
```

---

## CAPITULO 7: Cifrados de bloque -- AES y el arte de mezclar bits

**Palabras:** ~8,000
**Hook:** "Cada vez que abres WhatsApp, tu telefono ejecuta AES miles de veces por segundo. Este algoritmo, disenado por dos belgas en los 90s, protege mas secretos que cualquier otro invento humano. Y funciona mezclando bytes en una tabla de 4x4, 10 veces seguidas."
**Post base:** tipos-de-algoritmos-criptograficos.md
**Contenido nuevo:** ~55%. El post cubre DES, AES, modos de operacion. Falta: internals de AES, cifrado autenticado, AEAD, caso Heartbleed para contexto TLS.
**Takeaway:** AES es el cifrado simetrico que debes usar. Pero el algoritmo correcto con el modo incorrecto es igual de peligroso que no cifrar.
**Ejercicio del capitulo:** Cifrar y descifrar archivos con AES-256-GCM en Python, incluyendo manejo correcto de nonces.

### Secciones

#### 7.1 Cifrado simetrico: una llave para gobernarlos a todos (~1,000 palabras)
**Tipo:** [TEORIA]
**Contenido nuevo:** 70%

- 7.1.1 El concepto (~400 palabras)
  - Misma llave para cifrar y descifrar
  - Analogia: un candado con dos copias de la misma llave
  - El problema de la distribucion de llaves

- 7.1.2 Cifrados de bloque vs cifrados de flujo (~300 palabras)
  - Bloque: tamano fijo de entrada/salida
  - Flujo: bit por bit
  - Cuando usar cada uno (adelanto del Cap 8)

- 7.1.3 Permutaciones pseudo-aleatorias (~300 palabras)
  - La salida debe ser indistinguible de ruido aleatorio
  - Confusion y difusion (Shannon, 1949)

#### 7.2 AES por dentro: las cuatro operaciones (~2,500 palabras)
**Tipo:** [TEORIA] + [MATEMATICAS] + [CODIGO PYTHON]
**Post base:** tipos-de-algoritmos-criptograficos.md (seccion AES)
**Contenido nuevo:** 80%

- 7.2.1 Historia y seleccion de Rijndael (~400 palabras)
  - Concurso NIST 1997-2000, 15 candidatos
  - Joan Daemen y Vincent Rijmen (el mismo Daemen de Keccak)
  - Criterios: velocidad, simplicidad, seguridad

- 7.2.2 La matriz de estado 4x4 (~400 palabras)
  - Bloque de 128 bits = 16 bytes = matriz 4x4
  - SubBytes, ShiftRows, MixColumns, AddRoundKey
  - 10 rondas (AES-128), 12 (AES-192), 14 (AES-256)

- 7.2.3 SubBytes: la S-Box (~500 palabras)
  - Sustitucion no lineal
  - Basada en inversos en GF(2^8)
  - Por que la no linealidad es critica para seguridad

- 7.2.4 ShiftRows y MixColumns: difusion (~500 palabras)
  - ShiftRows: desplaza filas de la matriz
  - MixColumns: multiplicacion de matrices en GF(2^8)
  - Juntos aseguran que cada bit de entrada afecte todos los bits de salida

- 7.2.5 AddRoundKey y expansion de llave (~400 palabras)
  - XOR del estado con la subllave de cada ronda
  - Key schedule: genera subllaves a partir de la llave original

- 7.2.6 AES en hardware: instrucciones AES-NI (~300 palabras)
  - Procesadores Intel/AMD ejecutan AES en hardware
  - 3-4 ciclos por bloque
  - Implicacion: AES es el mas rapido Y el mas seguro

#### 7.3 Modos de operacion: donde vive el peligro (~2,000 palabras)
**Tipo:** [TEORIA] + [CODIGO PYTHON] + [VULNERABILIDAD]
**Post base:** tipos-de-algoritmos-criptograficos.md (seccion modos de operacion)
**Contenido nuevo:** 50%

- 7.3.1 ECB: el modo prohibido (~500 palabras)
  - Cada bloque cifrado independientemente
  - El "pinguino ECB": imagen clasica que muestra patrones
  - CASO REAL: Adobe (2013) cifro passwords con 3DES-ECB
  ```python
  # Demostrar ECB: cifrar imagen BMP y observar patrones
  from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
  ```

- 7.3.2 CBC: encadenamiento de bloques (~400 palabras)
  - XOR con bloque anterior
  - Requiere IV aleatorio
  - Debilidad: vulnerable a ataques de padding oracle (POODLE, 2014)

- 7.3.3 CTR: el modo contador (~400 palabras)
  - Convierte cifrado de bloque en cifrado de flujo
  - Nonce + contador, paralelizable
  - Peligro: reutilizar nonce destruye toda la seguridad

- 7.3.4 GCM: cifrado autenticado (~400 palabras)
  **Tipo:** [TEORIA] + [CODIGO PYTHON]
  - AES-GCM: cifrado + autenticacion en uno solo
  - AEAD: Associated Authenticated Encryption with Associated Data
  - El estandar para TLS 1.3
  ```python
  from cryptography.hazmat.primitives.ciphers.aead import AESGCM
  key = AESGCM.generate_key(bit_length=256)
  aesgcm = AESGCM(key)
  nonce = os.urandom(12)
  ct = aesgcm.encrypt(nonce, b"mensaje secreto", b"datos asociados")
  pt = aesgcm.decrypt(nonce, ct, b"datos asociados")
  ```

- 7.3.5 ChaCha20-Poly1305: la alternativa a AES-GCM (~300 palabras)
  - Disenado por Daniel J. Bernstein
  - Mas rapido en software sin AES-NI (dispositivos moviles)
  - Usado en TLS, WireGuard, SSH

#### 7.4 DES, 3DES y otros: el cementerio de cifrados (~500 palabras)
**Tipo:** [TEORIA]
**Post base:** tipos-de-algoritmos-criptograficos.md (seccion DES)
**Contenido nuevo:** 20%

- DES: 56 bits de llave, roto por fuerza bruta en 1999
- 3DES: 112 bits efectivos, ineficiente, deprecado
- Serpent y Twofish: finalistas de AES, aun seguros pero poco usados

#### 7.5 Casos reales (~1,000 palabras)
**Tipo:** [VULNERABILIDAD]
**Contenido nuevo:** 100%

- 7.5.1 POODLE (2014): ataque a CBC padding (~400 palabras)
  - Padding oracle en SSL 3.0
  - Permitia descifrar cookies de sesion
  - Leccion: CBC + padding = superficie de ataque

- 7.5.2 Sweet32 (2016): ataques de cumpleanos contra 3DES/Blowfish (~300 palabras)
  - Bloques de 64 bits colisionan despues de ~2^32 bloques
  - OpenVPN y TLS afectados

- 7.5.3 Reutilizacion de nonce en AES-GCM: el error silencioso (~300 palabras)
  - Si reutilizas nonce, pierdes confidencialidad Y autenticidad
  - PS3 ECDSA: nonce reutilizado revelo la llave privada de Sony
  - Leccion: la gestion de nonces es tan critica como el algoritmo

#### 7.6 Ejercicio integrador (~500 palabras)
**Tipo:** [EJERCICIO]
**Contenido nuevo:** 100%

```python
# 1. Cifrar un archivo con AES-256-GCM
# 2. Demostrar que modificar 1 byte del ciphertext hace fallar la autenticacion
# 3. Cifrar una imagen BMP con ECB y con GCM, comparar visualmente
# 4. Implementar cifrado con password: Argon2id -> llave AES -> GCM
```

---

## CAPITULO 8: Cifrados de flujo y la importancia de la aleatoriedad

**Palabras:** ~7,500
**Hook:** "En 2001, investigadores descubrieron que las comunicaciones WiFi protegidas con WEP podian descifrarse en minutos. La causa: un cifrado de flujo llamado RC4 con una implementacion que reutilizaba vectores de inicializacion. Millones de redes quedaron expuestas."
**Post base:** tipos-de-algoritmos-criptograficos-cifrados-de-flujo.md + generadores-de-numeros-aleatorios-y-su-importancia-para-el-desarrollo.md
**Contenido nuevo:** ~50%
**Takeaway:** Los cifrados de flujo son elegantes y rapidos, pero su seguridad depende completamente de la calidad de la aleatoriedad y la unicidad del nonce. Nunca reutilices un nonce.
**Ejercicio del capitulo:** Implementar un cifrado de flujo simplificado, demostrar el ataque de reutilizacion de nonce, y cifrar un stream de datos con ChaCha20.

### Secciones

#### 8.1 Cifrados de flujo: cifrar bit a bit (~1,200 palabras)
**Tipo:** [TEORIA]
**Post base:** tipos-de-algoritmos-criptograficos-cifrados-de-flujo.md (definicion y funcionamiento)
**Contenido nuevo:** 30%

- 8.1.1 Definicion y contraste con cifrados de bloque (~400 palabras)
  - Entrada de tamano arbitrario -> salida del mismo tamano
  - Keystream: flujo de bits pseudo-aleatorios
  - XOR de keystream con plaintext

- 8.1.2 Estado interno vs contador (~400 palabras)
  - Cifrados con estado: actualizan estado secreto en cada llamada
  - Cifrados con contador: llave + nonce + contador
  - Ventaja del contador: acceso aleatorio, paralelizable

- 8.1.3 Cuando usar cifrados de flujo (~400 palabras)
  - Streaming de datos (video, audio cifrado)
  - Protocolos de red en tiempo real
  - Dispositivos con recursos limitados (IoT)

#### 8.2 Salsa20 y ChaCha20: los cifrados modernos (~1,500 palabras)
**Tipo:** [TEORIA] + [CODIGO PYTHON]
**Post base:** tipos-de-algoritmos-criptograficos-cifrados-de-flujo.md (seccion Salsa20)
**Contenido nuevo:** 60%

- 8.2.1 Salsa20: diseno de Daniel J. Bernstein (~400 palabras)
  - Quarter-round como operacion basica
  - 20 rondas, variantes de 12 y 8 rondas
  - Llave de 256 bits + nonce de 64 bits + contador de 64 bits

- 8.2.2 ChaCha20: la evolucion (~500 palabras)
  - Misma estructura, mejor difusion
  - Nonce de 96 bits + contador de 32 bits
  - Adoptado por TLS, WireGuard, SSH
  ```python
  from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
  key = ChaCha20Poly1305.generate_key()
  chacha = ChaCha20Poly1305(key)
  nonce = os.urandom(12)
  ct = chacha.encrypt(nonce, b"mensaje secreto", b"datos asociados")
  ```

- 8.2.3 AES-CTR como cifrado de flujo (~300 palabras)
  - "Cifrado de bloque disfrazado de cifrado de flujo"
  - Mismo principio: cifrar nonce+contador, XOR con plaintext
  - Cuando preferir AES-CTR vs ChaCha20

- 8.2.4 RC4 y A5/1: lecciones del pasado (~300 palabras)
  - RC4: vulnerable, no usar. Fue la base de WEP y versiones antiguas de TLS.
  - A5/1: cifrado 2G, completamente roto

#### 8.3 Aleatoriedad: el ingrediente secreto (~2,500 palabras)
**Tipo:** [TEORIA] + [CODIGO PYTHON]
**Post base:** generadores-de-numeros-aleatorios-y-su-importancia-para-el-desarrollo.md
**Contenido nuevo:** 40%

- 8.3.1 Que es aleatoriedad y entropia (~500 palabras)
  - Distribucion uniforme: cada valor es igualmente probable
  - Entropia: bits de informacion impredecible
  - Un generador con N bits de entropia tiene 2^N estados posibles

- 8.3.2 True Random Number Generators (TRNG) (~400 palabras)
  - Fuentes fisicas: ruido termico, movimiento del raton, sensores
  - QRNGs: generadores cuanticos
  - Problema: lentos, pueden quedarse sin entropia

- 8.3.3 Pseudo-Random Number Generators (PRNG) (~400 palabras)
  - Deterministas: misma semilla = misma secuencia
  - Mersenne Twister: bueno para simulaciones, PELIGROSO para criptografia
  - La funcion random() de tu lenguaje NO es segura para criptografia

- 8.3.4 CSPRNG: generadores criptograficamente seguros (~500 palabras)
  - Forward secrecy: no puedes predecir bits futuros
  - Backward secrecy: no puedes reconstruir bits pasados
  - /dev/urandom, Fortuna, RDRAND/RDSEED
  ```python
  import os
  import secrets
  # CORRECTO para criptografia:
  llave = os.urandom(32)
  token = secrets.token_hex(32)
  # INCORRECTO para criptografia:
  import random
  llave_mala = random.randbytes(32)  # NUNCA hagas esto para criptografia
  ```

- 8.3.5 Como usar CSPRNG en cada lenguaje (~400 palabras)
  - Python: os.urandom(), secrets
  - JavaScript: crypto.getRandomValues()
  - Go: crypto/rand
  - Rust: rand::rngs::OsRng
  - Regla: siempre usa el modulo crypto de tu lenguaje

- 8.3.6 Nota sobre la API correcta en Python (~300 palabras)
  - `random` vs `secrets` vs `os.urandom`
  - Cuando usar cada uno
  - secrets.choice(), secrets.token_bytes(), secrets.compare_digest()

#### 8.4 Casos reales (~1,300 palabras)
**Tipo:** [VULNERABILIDAD]
**Contenido nuevo:** 100%

- 8.4.1 Debian OpenSSL (2008): el PRNG que solo generaba 32,767 llaves (~500 palabras)
  - Un mantenedor comento dos lineas de codigo en OpenSSL
  - Resultado: el PRNG se semillaba solo con el PID del proceso
  - 32,767 llaves posibles para TODA la criptografia de Debian durante 2 anos
  - Todas las llaves SSH, SSL, VPN generadas en ese periodo eran adivinables
  - Leccion: no modifiques codigo criptografico sin entenderlo

- 8.4.2 PS3 ECDSA (2010): el nonce que Sony reutilizo (~500 palabras)
  - Sony firmo el firmware de PS3 con ECDSA
  - Reutilizaron el mismo nonce k en multiples firmas
  - Con dos firmas y el mismo nonce, se puede extraer la llave privada algebraicamente
  ```python
  # Demostracion simplificada del ataque:
  # s1 = k^-1 * (hash1 + r * privkey) mod n
  # s2 = k^-1 * (hash2 + r * privkey) mod n
  # s1 - s2 = k^-1 * (hash1 - hash2) mod n
  # k = (hash1 - hash2) / (s1 - s2) mod n
  # privkey = (s1 * k - hash1) / r mod n
  ```
  - Leccion: un solo nonce repetido revela la llave privada completa

- 8.4.3 Juniper Dual_EC_DRBG (2015): puerta trasera en un PRNG (~300 palabras)
  - NSA posiblemente introdujo una backdoor en el generador Dual_EC
  - Juniper lo implemento en sus firewalls
  - Leccion: la procedencia del PRNG importa tanto como su diseno

#### 8.5 Ejercicio integrador (~500 palabras)
**Tipo:** [EJERCICIO]
**Contenido nuevo:** 100%

```python
# 1. Implementar cifrado de flujo con XOR y keystream fijo (demostrar inseguridad)
# 2. Demostrar ataque de reutilizacion de nonce:
#    c1 = m1 XOR keystream, c2 = m2 XOR keystream
#    c1 XOR c2 = m1 XOR m2 (se cancela el keystream!)
# 3. Cifrar un stream de datos en tiempo real con ChaCha20-Poly1305
# 4. Comparar velocidad: AES-256-GCM vs ChaCha20-Poly1305
```

---

## CAPITULO 9: Cifrado asimetrico -- La magia de las dos llaves

**Palabras:** ~7,000
**Hook:** "En 1976, Whitfield Diffie y Martin Hellman resolvieron un problema que se creia imposible: como dos personas pueden crear un secreto compartido gritandose mensajes en una plaza publica, aunque todos los escuchen. La solucion no es un truco: es matematica."
**Contenido nuevo:** ~95%. No hay post base directo; solo menciones indirectas en el post de cuantica.
**Takeaway:** La criptografia asimetrica resuelve el problema de la distribucion de llaves, pero es lenta y esta amenazada por la computacion cuantica. Se usa para intercambio de llaves y firmas, no para cifrar datos directamente.
**Ejercicio del capitulo:** Implementar intercambio de llaves Diffie-Hellman simplificado, generar un par RSA, y firmar/verificar con ECDSA.

### Secciones

#### 9.1 El problema de la distribucion de llaves (~1,000 palabras)
**Tipo:** [TEORIA] + [CASO REAL]
**Contenido nuevo:** 100%

- 9.1.1 El dilema de los generales (~400 palabras)
  - Alice y Bob quieren comunicarse en secreto
  - Si comparten una llave simetrica, necesitan un canal seguro
  - Pero si ya tuvieran canal seguro, no necesitarian criptografia
  - Circulo vicioso: la distribucion de llaves pre-internet

- 9.1.2 La idea revolucionaria (~300 palabras)
  - Llave publica: todos pueden conocerla
  - Llave privada: solo el dueno la conoce
  - Cifrar con publica, descifrar con privada
  - Firmar con privada, verificar con publica

- 9.1.3 Analogia del candado abierto (~300 palabras)
  - Alice envia un candado abierto (llave publica) a Bob
  - Bob pone su mensaje en una caja y cierra con el candado
  - Solo Alice tiene la llave (privada) para abrir

#### 9.2 Diffie-Hellman: intercambio de llaves (~1,500 palabras)
**Tipo:** [TEORIA] + [MATEMATICAS] + [CODIGO PYTHON]
**Contenido nuevo:** 100%

- 9.2.1 El protocolo paso a paso (~500 palabras)
  - Parametros publicos: primo p y generador g
  - Alice: elige a, calcula A = g^a mod p
  - Bob: elige b, calcula B = g^b mod p
  - Secreto compartido: A^b mod p = B^a mod p = g^(ab) mod p
  - Diagrama de flujo

- 9.2.2 Implementacion simplificada (~400 palabras)
  ```python
  # DH simplificado (NO para produccion)
  from secrets import randbelow
  p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1  # Primo grande
  g = 2
  # Alice
  a = randbelow(p - 2) + 1
  A = pow(g, a, p)
  # Bob
  b = randbelow(p - 2) + 1
  B = pow(g, b, p)
  # Secreto compartido
  secreto_alice = pow(B, a, p)
  secreto_bob = pow(A, b, p)
  assert secreto_alice == secreto_bob
  ```

- 9.2.3 ECDH: Diffie-Hellman con curvas elipticas (~300 palabras)
  - Misma idea, sobre curvas elipticas
  - X25519: la curva moderna recomendada
  - Llaves de 256 bits vs 2048+ bits en DH clasico

- 9.2.4 Vulnerabilidad: Man-in-the-Middle (~300 palabras)
  **Tipo:** [VULNERABILIDAD]
  - DH no autentica: un atacante puede interceptar
  - Necesitas firmas digitales o certificados para autenticar
  - Conexion con TLS (donde DH + certificados se combinan)

#### 9.3 RSA: el algoritmo que cambio el mundo (~1,500 palabras)
**Tipo:** [TEORIA] + [CODIGO PYTHON]
**Contenido nuevo:** 100%

- 9.3.1 Generacion de llaves (~400 palabras)
  - Elegir dos primos grandes p, q
  - n = p * q (modulo publico)
  - e = 65537 (exponente publico)
  - d tal que e * d = 1 mod phi(n) (exponente privado)
  - Seguridad: depende de la dificultad de factorizar n

- 9.3.2 Cifrado y descifrado (~400 palabras)
  - Cifrar: c = m^e mod n
  - Descifrar: m = c^d mod n
  - Por que funciona: teorema de Euler

- 9.3.3 RSA en la practica (~400 palabras)
  - Nunca cifres datos directamente con RSA (es lento)
  - Cifrado hibrido: RSA cifra una llave AES, AES cifra los datos
  - Padding OAEP: por que RSA sin padding es inseguro
  ```python
  from cryptography.hazmat.primitives.asymmetric import rsa, padding
  from cryptography.hazmat.primitives import hashes
  private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
  public_key = private_key.public_key()
  # Cifrar
  ct = public_key.encrypt(b"secreto", padding.OAEP(
      mgf=padding.MGF1(algorithm=hashes.SHA256()),
      algorithm=hashes.SHA256(), label=None))
  # Descifrar
  pt = private_key.decrypt(ct, padding.OAEP(
      mgf=padding.MGF1(algorithm=hashes.SHA256()),
      algorithm=hashes.SHA256(), label=None))
  ```

- 9.3.4 Tamanos de llave y depreciacion (~300 palabras)
  - RSA-2048: minimo aceptable
  - RSA-4096: recomendado para proteccion a largo plazo
  - NIST: deprecar RSA para 2030, prohibir para 2035

#### 9.4 Firmas digitales (~1,500 palabras)
**Tipo:** [TEORIA] + [CODIGO PYTHON]
**Contenido nuevo:** 100%

- 9.4.1 Concepto: el equivalente digital de una firma manuscrita (~400 palabras)
  - Firmar: hash del mensaje + llave privada -> firma
  - Verificar: hash del mensaje + llave publica + firma -> valido/invalido
  - Propiedades: autenticacion, integridad, no repudio

- 9.4.2 RSA-PSS y ECDSA (~400 palabras)
  - RSA-PSS: firma RSA con padding probabilistico
  - ECDSA: firmas con curvas elipticas (mas eficiente)
  - Ed25519: la curva moderna para firmas (rapida, segura, simple)

- 9.4.3 Firmas en la practica (~400 palabras)
  ```python
  from cryptography.hazmat.primitives.asymmetric import ec
  private_key = ec.generate_private_key(ec.SECP256R1())
  # Firmar
  signature = private_key.sign(b"documento", ec.ECDSA(hashes.SHA256()))
  # Verificar
  public_key = private_key.public_key()
  public_key.verify(signature, b"documento", ec.ECDSA(hashes.SHA256()))
  ```

- 9.4.4 Certificados digitales y PKI (~300 palabras)
  - X.509, CAs, cadenas de confianza
  - Cada conexion HTTPS verifica un certificado
  - Let's Encrypt: democratizacion de certificados

#### 9.5 Ejercicio integrador (~500 palabras)
**Tipo:** [EJERCICIO]
**Contenido nuevo:** 100%

```python
# 1. Implementar DH simplificado y derivar llave AES del secreto compartido
# 2. Generar par RSA-4096, cifrar/descifrar un mensaje
# 3. Firmar un archivo con Ed25519 y verificar la firma
# 4. Simular ataque Man-in-the-Middle contra DH sin autenticacion
```

---

## CAPITULO 10: Protocolos criptograficos -- TLS y como se conecta todo

**Palabras:** ~6,000
**Hook:** "Cada vez que ves el candado en tu navegador, ocurre una danza criptografica de menos de 100 milisegundos: intercambio de llaves, verificacion de certificados, cifrado simetrico, MACs. Uno solo de estos pasos mal implementado y toda tu seguridad se desmorona."
**Contenido nuevo:** ~95%
**Takeaway:** Los protocolos criptograficos combinan multiples primitivas para resolver problemas del mundo real. Entender TLS te da el framework mental para usar la criptografia correctamente en cualquier sistema.
**Ejercicio del capitulo:** Analizar un handshake TLS 1.3 real con Python y verificar los pasos del protocolo.

### Secciones

#### 10.1 De primitivas a protocolos (~1,000 palabras)
**Tipo:** [TEORIA]
**Contenido nuevo:** 100%

- 10.1.1 Por que las primitivas solas no son suficientes (~400 palabras)
  - AES cifra, pero no autentica
  - RSA autentica, pero es lento
  - Un hash verifica integridad, pero no origen
  - Se necesitan combinar correctamente

- 10.1.2 El patron cifrado hibrido (~300 palabras)
  - Asimetrico para intercambiar llave
  - Simetrico para cifrar datos
  - MAC o AEAD para autenticar

- 10.1.3 Suites criptograficas (~300 palabras)
  - TLS_AES_256_GCM_SHA384: que significa cada parte
  - Como leer una cipher suite
  - Por que hay tantas combinaciones

#### 10.2 TLS 1.3: el protocolo que protege internet (~2,500 palabras)
**Tipo:** [TEORIA] + [CODIGO PYTHON]
**Contenido nuevo:** 100%

- 10.2.1 El handshake paso a paso (~800 palabras)
  - ClientHello: versiones, cipher suites, key shares
  - ServerHello: seleccion de parametros, key share
  - Derivacion de llaves con HKDF
  - Certificado y firma del servidor
  - Finished: verificacion mutua
  - Diagrama de secuencia

- 10.2.2 Que mejoro respecto a TLS 1.2 (~500 palabras)
  - 1-RTT handshake (era 2-RTT)
  - Sin cipher suites inseguras
  - Forward secrecy obligatorio (DH efimero)
  - 0-RTT para reconexion (con reservas)

- 10.2.3 Inspeccionar un handshake TLS con Python (~500 palabras)
  ```python
  import ssl, socket
  context = ssl.create_default_context()
  with socket.create_connection(("example.com", 443)) as sock:
      with context.wrap_socket(sock, server_hostname="example.com") as ssock:
          print(ssock.version())       # TLSv1.3
          print(ssock.cipher())        # ('TLS_AES_256_GCM_SHA384', 'TLSv1.3', 256)
          cert = ssock.getpeercert()
          print(cert['subject'])
  ```

- 10.2.4 Errores comunes al configurar TLS (~400 palabras)
  - Permitir TLS 1.0/1.1 por "compatibilidad"
  - Certificados auto-firmados en produccion
  - No verificar el hostname
  - No fijar las cipher suites permitidas

- 10.2.5 Post-cuantico en TLS (~300 palabras)
  - X25519Kyber768: intercambio hibrido
  - Chrome y Firefox ya lo soportan
  - Adelanto del Cap 13

#### 10.3 Otros protocolos criptograficos (~1,000 palabras)
**Tipo:** [TEORIA]
**Contenido nuevo:** 100%

- 10.3.1 SSH: acceso remoto seguro (~300 palabras)
  - Ed25519 para autenticacion
  - ChaCha20-Poly1305 para cifrado
  - Por que debes migrar de RSA a Ed25519 en tus llaves SSH

- 10.3.2 Signal Protocol: cifrado end-to-end (~400 palabras)
  - Double Ratchet: forward y backward secrecy
  - Usado por WhatsApp, Signal, Facebook Messenger
  - Por que es mejor que PGP para mensajeria

- 10.3.3 WireGuard: VPN moderna (~300 palabras)
  - Solo 4,000 lineas de codigo (vs 100,000+ de OpenVPN)
  - Noise framework, ChaCha20, BLAKE2
  - Simplicidad como propiedad de seguridad

#### 10.4 Caso real: Heartbleed (2014) (~1,000 palabras)
**Tipo:** [VULNERABILIDAD]
**Contenido nuevo:** 100%

- 10.4.1 El bug que sacudio internet (~400 palabras)
  - Buffer over-read en OpenSSL
  - Extension heartbeat de TLS: se podia leer memoria del servidor
  - Llaves privadas, passwords, cookies expuestas
  - 17% de servidores HTTPS vulnerables

- 10.4.2 Anatomia tecnica del bug (~300 palabras)
  - El payload_length no se validaba
  - El servidor copiaba mas bytes de los que debia
  - 64KB de memoria por request

- 10.4.3 Lecciones (~300 palabras)
  - Un bug de implementacion puede ser peor que un fallo criptografico
  - Auditoria de codigo es critica
  - OpenSSL vs LibreSSL vs BoringSSL: fragmentacion post-Heartbleed

#### 10.5 Ejercicio integrador (~500 palabras)
**Tipo:** [EJERCICIO]
**Contenido nuevo:** 100%

```python
# 1. Conectar a 5 sitios populares y reportar: version TLS, cipher suite, certificado
# 2. Verificar que un sitio usa forward secrecy (DH efimero)
# 3. Construir un protocolo simplificado: DH + AES-GCM + HMAC
# 4. Demostrar que sin autenticacion, el protocolo es vulnerable a MITM
```

---

## CAPITULO 11: MACs -- Garantizando autenticidad e integridad

**Palabras:** ~5,500
**Hook:** "Cifrar un mensaje garantiza que nadie mas puede leerlo. Pero no garantiza que no haya sido modificado. En 2014, un ataque contra iMessage de Apple demostro que se podian alterar mensajes cifrados sin que el receptor lo notara. La pieza faltante: autenticacion."
**Post base:** criptografia-para-desarrolladores-codigos-de-autenticacion-de-mensajes.md
**Contenido nuevo:** ~45%. El post cubre bien HMAC y CMAC, pero falta profundidad en ataques, Poly1305 detallado, y el patron "encrypt-then-MAC".
**Takeaway:** Nunca cifres sin autenticar. HMAC-SHA-256 o Poly1305 son tus herramientas para garantizar que un mensaje no fue modificado y proviene de quien dice ser.
**Ejercicio del capitulo:** Implementar una API de firmado de requests con HMAC-SHA-256, incluyendo proteccion contra replay attacks.

### Secciones

#### 11.1 El problema de la autenticidad (~1,000 palabras)
**Tipo:** [TEORIA]
**Post base:** criptografia-para-desarrolladores-codigos-de-autenticacion-de-mensajes.md (intro)
**Contenido nuevo:** 60%

- 11.1.1 Cifrar no es autenticar (~400 palabras)
  - Cifrado protege confidencialidad
  - MAC protege integridad y autenticidad
  - Son propiedades independientes: puedes tener una sin la otra

- 11.1.2 Ataques por falta de autenticacion (~300 palabras)
  - Bit-flipping attacks en cifrados de flujo
  - Padding oracle attacks en CBC
  - Caso iMessage (2014)

- 11.1.3 Encrypt-then-MAC vs MAC-then-Encrypt vs Encrypt-and-MAC (~300 palabras)
  - Encrypt-then-MAC: el patron correcto (IPsec)
  - MAC-then-Encrypt: vulnerable a ataques (SSL/TLS antiguo)
  - Encrypt-and-MAC: vulnerable a filtracion (SSH original)
  - Mejor solucion: AEAD (AES-GCM, ChaCha20-Poly1305) que combina ambos

#### 11.2 HMAC: el estandar para autenticacion basada en hash (~1,500 palabras)
**Tipo:** [TEORIA] + [CODIGO PYTHON]
**Post base:** criptografia-para-desarrolladores-codigos-de-autenticacion-de-mensajes.md (seccion HMAC)
**Contenido nuevo:** 40%

- 11.2.1 Construccion de HMAC (~500 palabras)
  - Por que hash(llave || mensaje) no es seguro (extension de longitud)
  - HMAC: H((K XOR opad) || H((K XOR ipad) || mensaje))
  - Padding interno y externo
  - Resistencia a ataques de extension de longitud

- 11.2.2 HMAC en codigo (~400 palabras)
  ```python
  import hmac, hashlib
  key = os.urandom(32)
  mensaje = b"datos importantes"
  tag = hmac.new(key, mensaje, hashlib.sha256).digest()
  # Verificar (constant-time comparison)
  hmac.compare_digest(tag, tag_recibido)
  ```

- 11.2.3 Errores comunes con HMAC (~300 palabras)
  - Comparacion no constant-time: vulnerable a timing attacks
  - Llave demasiado corta
  - Usar MD5 como hash base (funciona pero no recomendado)

- 11.2.4 HMAC vs hash(secreto + mensaje) con SHA-3 (~300 palabras)
  - SHA-3 no es vulnerable a extension de longitud
  - Pero HMAC sigue siendo mejor practica
  - Defensa en profundidad: si el hash se rompe, HMAC tiene margen extra

#### 11.3 CMAC y MACs con diseno independiente (~1,000 palabras)
**Tipo:** [TEORIA]
**Post base:** criptografia-para-desarrolladores-codigos-de-autenticacion-de-mensajes.md (secciones CMAC y MACs independientes)
**Contenido nuevo:** 40%

- 11.3.1 AES-CMAC (~300 palabras)
  - MAC basado en cifrado de bloque
  - Usado en protocolos 802.11i (WiFi WPA2)

- 11.3.2 Poly1305: el MAC ultrarapido (~400 palabras)
  - Disenado por DJB
  - Usado siempre con ChaCha20 (ChaCha20-Poly1305)
  - Universal hash: seguridad basada en una sola evaluacion de polinomio

- 11.3.3 SipHash: para hashtables y mensajes cortos (~300 palabras)
  - Proteccion contra hash flooding (HashDoS)
  - Usado en Python, Rust, Redis
  - No es un MAC criptografico completo, pero previene ataques

#### 11.4 Caso real y aplicaciones (~1,000 palabras)
**Tipo:** [CASO REAL] + [VULNERABILIDAD]
**Contenido nuevo:** 100%

- 11.4.1 Webhooks y firmado de APIs (~400 palabras)
  - GitHub, Stripe, Slack: firman webhooks con HMAC
  - Como verificar un webhook correctamente
  - Errores comunes: no verificar, timing leak, replay

- 11.4.2 JWT: tokens firmados (~300 palabras)
  - HMAC-SHA-256 (HS256) vs RS256
  - El peligro del "alg: none" en JWT
  - Por que validar el algoritmo del lado del servidor

- 11.4.3 Caso: Flickr API signing bypass (2009) (~300 palabras)
  - Comparacion de HMAC no constant-time
  - Timing attack permitia forjar firmas caracter por caracter
  - Leccion: hmac.compare_digest() siempre

#### 11.5 Ejercicio integrador (~1,000 palabras)
**Tipo:** [EJERCICIO]
**Contenido nuevo:** 100%

```python
# Implementar API firmada:
# 1. Cliente genera HMAC-SHA-256 del request (metodo + path + body + timestamp)
# 2. Servidor verifica con compare_digest
# 3. Proteccion contra replay: rechazar requests con timestamp > 5 minutos
# 4. Demostrar timing attack contra comparacion ingenua (== vs compare_digest)
# 5. Migrar a ChaCha20-Poly1305 para autenticar y cifrar
```

---

## CAPITULO 12: Criptografia vs computacion cuantica

**Palabras:** ~6,000
**Hook:** "En 2019, Google anuncio que su procesador cuantico Sycamore realizo en 200 segundos un calculo que a la supercomputadora mas poderosa del mundo le habria tomado 10,000 anos. No fue un calculo util para romper criptografia, pero fue la primera senal de que la amenaza cuantica no es ciencia ficcion."
**Post base:** criptografia-vs-computacion-cuantica.md
**Contenido nuevo:** ~50%. El post cubre bien Shor, Grover, y el impacto general. Falta: qubits necesarios, timelines actualizados, HNDL.
**Takeaway:** La computacion cuantica destruira la criptografia asimetrica actual (RSA, ECC). La criptografia simetrica sobrevivira duplicando tamanos de llave. La migracion debe empezar AHORA por la amenaza "harvest now, decrypt later".
**Ejercicio del capitulo:** Clasificar los algoritmos criptograficos de tu proyecto como "cuantico-seguro" o "cuantico-vulnerable" y proponer un plan de migracion.

### Secciones

#### 12.1 Computacion cuantica para programadores (~1,500 palabras)
**Tipo:** [TEORIA]
**Post base:** criptografia-vs-computacion-cuantica.md (principios de funcionamiento)
**Contenido nuevo:** 40%

- 12.1.1 Superposicion cuantica: mas alla de 0 y 1 (~400 palabras)
  - Un qubit puede estar en superposicion de 0 y 1
  - n qubits representan 2^n estados simultaneamente
  - Colapso al medir: la superposicion se resuelve en un estado concreto

- 12.1.2 Qubits, compuertas cuanticas y circuitos (~400 palabras)
  - Compuertas: Hadamard, CNOT, rotaciones
  - Circuitos cuanticos: secuencia de compuertas
  - Medicion: extraer el resultado

- 12.1.3 Aceleracion cuantica: que se acelera y que no (~400 palabras)
  - NO todo es mas rapido en una computadora cuantica
  - Solo ciertos problemas tienen algoritmos cuanticos eficientes
  - Factorizacion: exponencial -> polinomial (Shor)
  - Busqueda: O(N) -> O(sqrt(N)) (Grover)

- 12.1.4 Estado actual del hardware cuantico (~300 palabras)
  - 2026: ~1,000-1,500 qubits logicos (IBM, Google)
  - Para romper RSA-2048: se necesitan ~4,000 qubits logicos con correccion de errores
  - Estimaciones: 10-20 anos para computadora cuantica criptograficamente relevante

#### 12.2 El algoritmo de Shor: el fin de RSA y ECC (~1,500 palabras)
**Tipo:** [TEORIA] + [MATEMATICAS]
**Post base:** criptografia-vs-computacion-cuantica.md (seccion de Shor)
**Contenido nuevo:** 50%

- 12.2.1 Que resuelve Shor (~500 palabras)
  - Factorizacion de enteros en tiempo polinomial cuantico
  - Transforma el problema en encontrar el periodo de una funcion exponencial
  - La transformada cuantica de Fourier encuentra el periodo eficientemente
  - O(log n)^3 operaciones cuanticas

- 12.2.2 Impacto: que algoritmos mueren (~500 palabras)
  - RSA: depende de factorizacion -> MUERTO
  - ECDSA/ECDH: depende de logaritmo discreto -> MUERTO
  - Diffie-Hellman clasico: depende de logaritmo discreto -> MUERTO
  - DSA: depende de logaritmo discreto -> MUERTO

- 12.2.3 Qubits necesarios: cuanto falta (~500 palabras)
  - RSA-2048: ~4,000 qubits logicos (millones de fisicos)
  - ECC-256: ~2,330 qubits logicos
  - Correccion de errores cuanticos: factor 1000x-10000x
  - Timelines optimistas (2030) vs conservadores (2040)

#### 12.3 El algoritmo de Grover: la mitad de la seguridad (~800 palabras)
**Tipo:** [TEORIA]
**Post base:** criptografia-vs-computacion-cuantica.md (seccion de Grover)
**Contenido nuevo:** 40%

- 12.3.1 Busqueda cuadraticamente mas rapida (~400 palabras)
  - Busqueda en base de datos no ordenada: O(sqrt(N)) vs O(N)
  - AES-128: seguridad efectiva = 64 bits (insuficiente)
  - AES-256: seguridad efectiva = 128 bits (suficiente)
  - SHA-256: seguridad de colision = 128 bits (aun suficiente)

- 12.3.2 La solucion para cifrados simetricos y hashes (~400 palabras)
  - Duplicar tamanos de llave: AES-256 como minimo
  - SHA-384/512 para hashes
  - Argon2 y bcrypt: no afectados significativamente

#### 12.4 La amenaza "Harvest Now, Decrypt Later" (~1,000 palabras)
**Tipo:** [CASO REAL]
**Post base:** migracion-a-criptografia-post-cuantica.md (seccion HNDL)
**Contenido nuevo:** 30%

- 12.4.1 El escenario mas urgente (~400 palabras)
  - Adversarios capturan trafico cifrado HOY
  - Almacenan el trafico para descifrarlo cuando tengan computadoras cuanticas
  - Datos con vida util > 10 anos ya estan comprometidos

- 12.4.2 Que datos estan en riesgo (~300 palabras)
  - Secretos de estado, historiales medicos, propiedad intelectual
  - Comunicaciones diplomaticas
  - Datos financieros de largo plazo

- 12.4.3 Por que la migracion es urgente AHORA (~300 palabras)
  - No se trata de cuando exista la computadora cuantica
  - Se trata de cuando los datos dejen de ser sensibles
  - Si tus datos necesitan 15+ anos de confidencialidad, ya estas tarde

#### 12.5 Tabla de impacto cuantico por algoritmo (~700 palabras)
**Tipo:** [TEORIA]
**Contenido nuevo:** 80%

- Tabla completa: Algoritmo | Tipo | Amenaza cuantica | Accion requerida
  - AES-128 -> Duplicar a AES-256
  - AES-256 -> Seguro
  - SHA-256 -> Seguro (128 bits post-cuanticos)
  - RSA-2048 -> MIGRAR a ML-KEM
  - ECDSA -> MIGRAR a ML-DSA
  - ECDH -> MIGRAR a ML-KEM
  - Argon2 -> Seguro

#### 12.6 Ejercicio integrador (~500 palabras)
**Tipo:** [EJERCICIO]
**Contenido nuevo:** 100%

```python
# 1. Inventario criptografico: escanear tu proyecto y clasificar algoritmos
#    como "cuantico-seguro" o "cuantico-vulnerable"
# 2. Calcular: si un adversario captura tu trafico hoy y descifra en 15 anos,
#    que datos estarian expuestos?
# 3. Para cada algoritmo vulnerable, identificar el reemplazo post-cuantico
# 4. Estimar el impacto en tamano de mensajes (comparar tamanos de llave)
```

---

## CAPITULO 13: Criptografia post-cuantica -- El futuro ya esta aqui

**Palabras:** ~7,500
**Hook:** "En agosto de 2024, el NIST publico los primeros estandares de criptografia post-cuantica, culminando un proceso de 8 anos con 82 candidatos de 25 paises. No es un ejercicio academico: Chrome ya usa criptografia post-cuantica en cada conexion HTTPS."
**Post base:** migracion-a-criptografia-post-cuantica.md
**Contenido nuevo:** ~45%. El post (en borrador) tiene estructura solida pero necesita codigo, profundidad tecnica, y guia practica completa.
**Takeaway:** Los estandares post-cuanticos ya existen, las bibliotecas ya estan disponibles, y los mandatos gubernamentales ya tienen fecha. No hay excusa para no empezar la migracion.
**Ejercicio del capitulo:** Realizar un intercambio de llaves con ML-KEM y verificar una firma con ML-DSA usando liboqs-python.

### Secciones

#### 13.1 Los nuevos estandares del NIST (~2,000 palabras)
**Tipo:** [TEORIA]
**Post base:** migracion-a-criptografia-post-cuantica.md (seccion de algoritmos NIST)
**Contenido nuevo:** 40%

- 13.1.1 El proceso de seleccion: 8 anos, 82 candidatos (~400 palabras)
  - 2016: convocatoria
  - 2022: finalistas
  - Agosto 2024: FIPS 203, 204, 205 publicados
  - Criterios: seguridad, rendimiento, tamano de llave/firma

- 13.1.2 ML-KEM (CRYSTALS-Kyber): intercambio de llaves (~500 palabras)
  - Reemplazo de ECDH y RSA-KEM
  - Basado en Module Learning With Errors
  - Tres niveles: ML-KEM-512/768/1024
  - Tamanos: llave publica 800-1568 bytes (vs 32 de X25519)
  - Rendimiento: sorprendentemente rapido, comparable a RSA

- 13.1.3 ML-DSA (CRYSTALS-Dilithium): firmas digitales (~500 palabras)
  - Reemplazo de ECDSA y RSA-PSS
  - Tambien basado en reticulas
  - Tres niveles de seguridad
  - Firma de 2420-4627 bytes (vs 64 de ECDSA)
  - Caso de uso: certificados TLS, firmas de codigo

- 13.1.4 SLH-DSA (SPHINCS+): firmas basadas en hash (~300 palabras)
  - La opcion conservadora: solo depende de la seguridad de funciones hash
  - Firmas mas grandes pero confianza maxima
  - Cuando preferir SLH-DSA sobre ML-DSA
  - Conexion con los capitulos de hashes: SHA-3 y las propiedades que ya estudiamos

- 13.1.5 Tabla comparativa de tamanos y rendimiento (~300 palabras)
  - Algoritmo | Llave publica | Llave privada | Firma/Ciphertext | Ops/segundo
  - Comparacion visual con algoritmos clasicos

#### 13.2 Criptografia basada en reticulas: la intuicion (~1,500 palabras)
**Tipo:** [MATEMATICAS]
**Post base:** migracion-a-criptografia-post-cuantica.md (seccion de reticulas y LWE)
**Contenido nuevo:** 50%

- 13.2.1 Que es un reticula (lattice) (~500 palabras)
  - Definicion intuitiva: cuadricula regular en muchas dimensiones
  - Formalmente: combinaciones enteras de vectores base
  - Visualizacion en 2D: puntos regularmente espaciados
  - En dimensiones altas (>500): los problemas se vuelven dificilisimos

- 13.2.2 El problema del vector mas corto (SVP) (~400 palabras)
  - Dado un reticula, encontrar el vector no nulo mas corto
  - En 2D: trivial. En 500+ dimensiones: imposible (incluso para computadoras cuanticas)
  - No se conoce algoritmo cuantico eficiente

- 13.2.3 Learning With Errors (LWE) (~600 palabras)
  - Sistema de ecuaciones lineales + "ruido" aleatorio
  - Sin ruido: resolucion facil (eliminacion gaussiana)
  - Con ruido: imposible recuperar la solucion
  - Reduccion a SVP: romper LWE es al menos tan dificil como SVP
  - Module-LWE: la version estructurada usada en ML-KEM y ML-DSA

#### 13.3 Guia practica de migracion (~2,000 palabras)
**Tipo:** [CODIGO PYTHON] + [CASO REAL]
**Post base:** migracion-a-criptografia-post-cuantica.md (seccion de migracion)
**Contenido nuevo:** 50%

- 13.3.1 El enfoque hibrido: cinturon y tirantes (~500 palabras)
  - Combinar clasico + post-cuantico: X25519 + ML-KEM-768
  - El atacante debe romper AMBOS algoritmos
  - Recomendado durante la transicion (2025-2035)
  - Ya desplegado: Chrome, Firefox, Cloudflare

- 13.3.2 ML-KEM en codigo (~500 palabras)
  ```python
  # pip install liboqs-python
  import oqs
  # Generacion de llaves
  kem = oqs.KeyEncapsulation("ML-KEM-768")
  public_key = kem.generate_keypair()
  # Encapsulacion (lado del cliente)
  ciphertext, shared_secret_client = kem.encap_secret(public_key)
  # Decapsulacion (lado del servidor)
  shared_secret_server = kem.decap_secret(ciphertext)
  assert shared_secret_client == shared_secret_server
  # Usar shared_secret como llave AES-256
  ```

- 13.3.3 ML-DSA en codigo (~400 palabras)
  ```python
  sig = oqs.Signature("ML-DSA-65")
  public_key = sig.generate_keypair()
  # Firmar
  signature = sig.sign(b"documento importante")
  # Verificar
  is_valid = sig.verify(b"documento importante", signature, public_key)
  ```

- 13.3.4 Plan de migracion paso a paso (~600 palabras)
  - Paso 1: Inventario criptografico (CBOM - Cryptographic Bill of Materials)
  - Paso 2: Priorizar por riesgo (datos de larga vida primero)
  - Paso 3: Implementar modo hibrido en TLS
  - Paso 4: Migrar firmas digitales
  - Paso 5: Auditoria continua
  - Herramientas: cbom, oqs-provider para OpenSSL

#### 13.4 Mandatos y timelines (~1,000 palabras)
**Tipo:** [CASO REAL]
**Post base:** migracion-a-criptografia-post-cuantica.md (seccion de mandatos)
**Contenido nuevo:** 30%

- 13.4.1 NIST IR 8547 (~300 palabras)
  - RSA/ECC deprecados para 2030
  - Prohibidos para 2035
  - Minimo AES-256 para simetrico

- 13.4.2 NSA CNSA 2.0 (~300 palabras)
  - Agencias de EE.UU.: migracion completa para 2033-2035
  - Hitos intermedios desde 2025

- 13.4.3 Europa y el resto del mundo (~400 palabras)
  - ENISA: planes nacionales para 2026
  - UK NCSC: tres fases hasta 2035
  - Impacto en cumplimiento regulatorio
  - Si tu software se usa en gobierno o finanzas: la migracion es obligatoria

#### 13.5 Ejercicio integrador (~500 palabras)
**Tipo:** [EJERCICIO]
**Contenido nuevo:** 100%

```python
# 1. Intercambio de llaves con ML-KEM-768 y derivar llave AES-256
# 2. Firmar un documento con ML-DSA-65 y verificar
# 3. Comparar tamanos: generar par de llaves ECDSA vs ML-DSA, medir bytes
# 4. Implementar intercambio hibrido: X25519 + ML-KEM-768
#    shared_secret = HKDF(X25519_secret || ML-KEM_secret)
# 5. Benchmark: comparar rendimiento ECDH vs ML-KEM
```

---

## APENDICE A: Instalacion del entorno de desarrollo

**Palabras:** ~1,500
**Tipo:** [CODIGO PYTHON]
**Contenido nuevo:** 100%

### Secciones

- A.1 Python 3.10+ y pip (~300 palabras)
- A.2 Bibliotecas necesarias (~400 palabras)
  ```
  pip install cryptography pynacl argon2-cffi blake3 liboqs-python pycryptodome
  ```
- A.3 Verificar la instalacion (~300 palabras)
- A.4 Repositorio del libro (~200 palabras)
- A.5 Docker para entorno reproducible (~300 palabras)

---

## APENDICE B: Tabla de referencia rapida de algoritmos

**Palabras:** ~1,500
**Tipo:** [TEORIA]
**Contenido nuevo:** 100%

### Secciones

- B.1 Hashes: SHA-2, SHA-3, BLAKE2/3 con tamanos y bits de seguridad
- B.2 Hashes para passwords: Argon2id, scrypt, bcrypt con parametros recomendados
- B.3 Cifrados simetricos: AES-256-GCM, ChaCha20-Poly1305
- B.4 Cifrados asimetricos: RSA-4096, X25519, Ed25519
- B.5 Post-cuanticos: ML-KEM-768, ML-DSA-65, SLH-DSA
- B.6 MACs: HMAC-SHA-256, Poly1305
- B.7 KDFs: HKDF, Argon2

---

## APENDICE C: Recursos para seguir aprendiendo

**Palabras:** ~1,500
**Tipo:** [TEORIA]
**Post base:** recursos-para-aprender-criptografia-en-2021.md
**Contenido nuevo:** 40%

### Secciones

- C.1 Libros recomendados (~500 palabras)
  - Serious Cryptography (Aumasson)
  - Real-World Cryptography (Wong)
  - Cryptography Engineering (Schneier, Ferguson, Kohno)
  - A Graduate Course in Applied Cryptography (Boneh, Shoup)

- C.2 Retos y practica (~300 palabras)
  - Cryptopals Crypto Challenges
  - CryptoHack
  - CTFs con componente criptografico

- C.3 Cursos en linea (~300 palabras)
  - Coursera: Cryptography I (Dan Boneh)
  - Udacity: Applied Cryptography
  - Recursos en espanol

- C.4 Comunidades y conferencias (~200 palabras)
  - Real World Crypto
  - IACR conferences
  - Reddit r/crypto

- C.5 Estandares y documentos de referencia (~200 palabras)
  - NIST FIPS 197 (AES), 203 (ML-KEM), 204 (ML-DSA), 205 (SLH-DSA)
  - RFCs relevantes

---

## APENDICE D: Glosario

**Palabras:** ~2,000
**Tipo:** [TEORIA]
**Contenido nuevo:** 100%

- ~60-80 terminos clave definidos en espanol con su equivalente en ingles
- Desde "AEAD" hasta "XOR", pasando por "colision", "entropia", "nonce", "preimagen", "reticula", "salt", etc.

---

## Resumen de metricas

| Seccion | Palabras est. | Contenido del blog | Contenido nuevo |
|---------|--------------|-------------------|-----------------|
| Prologo | 2,000 | 10% | 90% |
| Cap 1: Tu primer hash | 8,000 | 50% | 50% |
| Cap 2: Matematicas | 7,000 | 20% | 80% |
| Cap 3: MD5 y SHA-2 | 7,000 | 25% | 75% |
| Cap 4: SHA-3 y Keccak | 6,500 | 50% | 50% |
| Cap 5: Passwords | 7,000 | 55% | 45% |
| Cap 6: Complejidad | 7,000 | 60% | 40% |
| Cap 7: Cifrados de bloque | 8,000 | 45% | 55% |
| Cap 8: Flujo + aleatoriedad | 7,500 | 50% | 50% |
| Cap 9: Asimetrico | 7,000 | 5% | 95% |
| Cap 10: Protocolos/TLS | 6,000 | 0% | 100% |
| Cap 11: MACs | 5,500 | 55% | 45% |
| Cap 12: Cuantica | 6,000 | 50% | 50% |
| Cap 13: Post-cuantica | 7,500 | 30% | 70% |
| Apendices A-D | 6,500 | 15% | 85% |
| **TOTAL** | **~98,500** | **~33%** | **~67%** |

---

## Vulnerabilidades reales incluidas (por capitulo)

| Vulnerabilidad | Capitulo | Primitiva afectada |
|---------------|----------|-------------------|
| Mt. Gox (2014) | Prologo | Maleabilidad de transacciones |
| SHAttered (2017) | Cap 1, 3 | SHA-1 colision |
| Flame malware (2012) | Cap 1, 3 | MD5 colision |
| Ataque extension longitud | Cap 3 | Merkle-Damgard |
| Bitcoin SHA-256 | Cap 3 | SHA-256 (uso legit) |
| LinkedIn (2012) | Cap 5 | SHA-1 sin salt |
| Adobe (2013) | Cap 5, 7 | 3DES-ECB |
| Dropbox (2012) | Cap 5 | bcrypt (bien hecho) |
| POODLE (2014) | Cap 7 | CBC padding oracle |
| Sweet32 (2016) | Cap 7 | 3DES bloques 64-bit |
| Penguin ECB | Cap 7 | AES-ECB |
| WEP/RC4 (2001) | Cap 8 | RC4 reutilizacion IV |
| Debian OpenSSL (2008) | Cap 8 | PRNG roto |
| PS3 ECDSA (2010) | Cap 8 | Nonce reutilizado |
| Dual_EC_DRBG/Juniper (2015) | Cap 8 | Backdoor en PRNG |
| iMessage (2014) | Cap 11 | Falta de autenticacion |
| Flickr API (2009) | Cap 11 | Timing attack en HMAC |
| Heartbleed (2014) | Cap 10 | Buffer over-read en OpenSSL |
| HNDL (ongoing) | Cap 12 | RSA/ECC captura previa |
| Google Sycamore (2019) | Cap 12 | Supremacia cuantica |

---

## Notas de produccion

1. **Diagrama por capitulo**: Cada capitulo necesita al menos 2-3 diagramas (flujo, arquitectura, comparacion)
2. **Cajas de texto especiales**: [PELIGRO] para anti-patrones, [BUENA PRACTICA] para recomendaciones, [PROFUNDIZAR] para material opcional
3. **Teaching Conversations**: Cada capitulo abre con un escenario o historia que crea tension, seguido de "vamos a resolverlo"
4. **Repositorio companiero**: GitHub con todo el codigo, notebooks Jupyter para ejercicios, Dockerfile
5. **Revision tecnica**: Necesaria por al menos un criptologo profesional antes de publicacion
