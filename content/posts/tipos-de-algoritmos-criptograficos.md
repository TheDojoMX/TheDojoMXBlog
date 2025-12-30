---
title: "Tipos de algoritmos criptográficos: cifrados de bloque"
date: 2020-12-03
author: "Héctor Patricio"
tags: ['cryptografía', 'cryptography', 'aes', 'des', '3-des', 'serpent']
description: "¿Sabes que es un cifrado de bloque? En este artículo hablamos de eso y te damos algunos ejemplos."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1438/v1606978976/snapbuilder_2_ba3zxt.png"
draft: false
---

Ya hablamos de lo que es [la criptografía](/2019/11/12/criptografia-basica-para-programadores-que-es-la-criptografia.html), ahora empecemos a hablar de los tipos de
algoritmos criptográficos que existen, sus características y sus principales diferencias. En este artículo hablaremos de los cifrados de bloque.

### ¿Qué es un cifrado de bloque?

Los cifrados de bloque trabajan sobre un conjunto de bits de tamaño fijo, produciendo un texto cifrado del mismo tamaño. Para cifrar datos de tamaño arbitrario como sucede en la vida real, se utiliza el algoritmo de cifrado de bloque combinado con diferentes técnicas llamadas **Modos de Operación**.

Algunos ejemplos de estos algoritmos de cifrado son el DES (Estadounidense), GOST 28147-89 (Ruso) y el actual **AES**.

Un bloque cifrado debe ser _permutación pseudo-aleatoria_ de bits, es decir, un conjunto de bits que sean _indistinguibles de bits generados completamente de manera aleatoria_. Es como si aventaras un montón de bits y dijeras que esa es la salida de tu algoritmo.

Esta propiedad evita que un atacante obtenga información sobre el contenido del mensaje que fue cifrado.

## Ejemplos de Cifrado de Bloque

Veamos algunos ejemplos de cifrados de bloque y sus características principales. Algunos se usan mientras que otros ya cayeron en el olvido.

### DES y Triple DES

El **Data Encryption Standard** era el algoritmo que más se usaba en la década de los 90, lo suficientemente seguro para el poder de cómputo de aquel entonces. Usa una llave de 56 bits y bloques de 64 bits. Debido a estas características, el poder de cómputo actual hace que sea demasiado fácil de romper con el suficiente poder computacional (2^56, el tamaño de la llave, no se considera seguro ya), así que su uso está completamente desrecomendado.

Su sucesor, el Triple DES realiza tres veces el mismo proceso usando tres llaves diferentes, con un tamaño de llave de 168 bits. Esto evita que sea posible romperlo a base de fuerza bruta, pero este proceso provee solamente una seguridad de 112 bits, por lo que se considera ineficiente (usas el cómputo de tres DES para obtener seguridad de una llave del doble de tamaño) y por lo tanto su uso no es recomendado también.

### AES

Debido a las visibles fallas de DES y triple DES, la NIST (National Institute of Standards and Technology de Estados Unidos) quería un algoritmo de cifrado que fuera dado a conocer públicamente y "capaz de proteger la información sensible del gobierno por los próximos cien años".

El **Advanced Encryption Standard** (Estándar de cifrado avanzado), es en realidad un subconjunto de los cifrados posibles de otro algoritmo llamado [Rijndael](https://csrc.nist.gov/csrc/media/projects/cryptographic-standards-and-guidelines/documents/aes-development/rijndael-ammended.pdf) y que fue el ganador del concurso que la NIST hizo para seleccionar el nuevo algoritmo de cifrado estándar que sustituiría a DES.

Rijndael fue creado por analistas criptográficos Belgas con objetivos claros: que fuera rápido y simple. Es una familia de cifrados que permiten cifrar bloques en múltiplos de 32 bits, desde 128 hasta 256 bits (128, 160, 192, 224, 256 bits). Las longitudes de llaves posibles son los mismos desde 128 hasta 256 bits.

AES es Rijndael con bloques de **128 bits** y llaves que pueden ser de 128, 192 o 256 bits.

AES aplica internamente una misma operación múltiples veces dependiendo del tamaño de la llave, y esto le permite se más seguro aumentando el tamaño de la llave. Esto es lo que se conoce como los "rounds" de AES, usando 10 para llaves de 128 bits, 12 para 192 bits y 14 para 256 bits.

AES tiene un diseño de operaciones concurrentes, que es fácilmente paralelizable y puede implementarse muy eficientemente en hardware, de hecho los procesadores modernos normalmente lo traen implementado en sus circuitos, es parte del conjunto de instrucciones del procesador.

La seguridad de AES según ciertos criptanalistas (por ejemplo, los creadores de Twofish) está completamente rota _teóricamente_, ya que hay ataques que pueden romper el cifrado de 14 ciclos (los ciclos completos que hace la versión de la llave de 256 bits) con ciertas condiciones, con 2^176 operaciones (lo cuál es un ataque que no se puede llevar a la práctica fácilmente).

Los ataques mencionados anteriormente no tienen nada de prácticos, es decir, no se pueden llevar a la realidad en entornos normales, por lo que no se piensa por ningún lado que la seguridad de AES está comprometida. Si necesitas un algoritmo de cifrado confiable y rápido, con AES no te puedes equivocar.

## Otros algoritmos

Como finalistas del concurso de la NIST hay otros algoritmos que vale la pena mencionar:

1. **Serpent.** Es un algoritmo de cifrado de bloque que está pensado completamente para ser resistente. Aplicaca una operación repetidamente (rounds) pero a diferencia de AES la aplica 32 veces. Los criptanalistas han logrado romper 12 de esos 32 rounds, por lo que se piensa que tiene bastante espacio de reserva para continuar siendo seguro. La desventaja contra AES es que es 3 veces más lento.

2. **TwoFish.** Este algoritmo tiene una construcción parecida a DES, y aplica su operación básica 16 veces. Los autores del algoritmo mencionan que es casi tan rápido como AES pero ofreciendo más margen de seguridad.

### Modos de operación

Un modo de operación es la forma en que se aplica un cifrado de bloque a un texto no cifrado que no es del tamaño exacto del bloque. Existen diferentes técnicas para hacer hacer que un algoritmo que acepta bloques de tamaño fijo acepte bloques arbitrarios. Los más conocidos son:

1. **Electronic Codebook (ECB)**. Este modo de operación parte el contenido en bloques del tamaño aceptado (rellenando los bits faltantes para hacer un múltiplo exacto) y manda cada bloque a cifrar de manera independiente. Este modo de operación está completamente prohibido si quieres hacer que tu programa sea seguro, ya que bloques en tu mensaje con el mismo contenido siempre dará el mismo resultado, dando pistas sobre la información subyacente a observadores meticulosos. **NO USES POR NINGÚN MOTIVO AES EN ECB**.

2. **Cypher Block Chaining (CBC)**. Este modo de igual manera parte el contenido en bloques del tamaño aceptado, pero en vez de cifrar cada bloque independientemente cifra el resultado de aplicar la operación XOR con el resultado del bloque anterior. De esta manera "encadena" los bloques haciendo que cada bloque dependa de los anteriores. Para cifrar el primer bloque utiliza un valor inicial generado de manera aleatoria. Para descifrar el valor se tiene que pasar el valor inicial aleatorio junto con el texto cifrado.

3. **Counter mode (CTR)**. En este modo de operación no se cifran los bloques de texto sino la combinación de un número de uso único (_nonce_) y un contador (de ahí su nombre). Después, ese cifrado se combina con un bloque del mensaje. El contador se aumenta en cada bloque del mensaje, mientras que el número de uso único sólo cambia entre cifrados de diferentes mensajes. El modo contador no requiere relleno, ya que la operación XOR se puede realizar con contenido de cualquier tamaño. Este es el modo de operación más rápido y elegante, pero es muy fácil de usar mal ya que la repetición de _nonces_ lo hace vulnerable.

### Completado de bloques

Los modos de operación ECB y CBC siguen requiriendo bloques del tamaño aceptado por el algoritmo, por lo que deben existir técnicas para completar mensajes que no sean del tamaño de un múltiplo del bloque. Hablaremos de dos:

1. Relleno (_padding_). Esta técnica completa el último bloque del contenido que no alcanza el tamaño requerido con bytes que comunican el número de bytes que se están rellenando. Ejemplo: Si faltan 15 bytes para rellenar el mensaje agrega 15 bytes con el valor `0f`, si falta un sólo byte agrega un byte con `01`. Esta técnica sólo funciona para mensajes que construído de bytes completos. Puedes ver una especificación aquí: [RFC 5652](https://tools.ietf.org/html/rfc5652)

2. Robo de texto cifrado (cyphertext stealing). Esta técnica es un poco más compleja pero más flexible. Consiste básicamente en tomar los bits que falten para el último bloque del texto cifrado anterior y dejar los bits no usados de ese mismo mensaje como el último bloque cifrado. Es un poco más complicado que esto, pero la idea básica aquí está. La NIST menciona tres formas de implementarlo [aquí](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38a-add.pdf).

## ¿Qué algoritmo debería usar?

La respuesta corta: AES con el mayor de tamaño de llave que tus recursos te permitan. Si tienes restricciones más fuertes de seguridad puedes pensar en TwoFish o Serpent, pero debes tener en cuenta que al no ser tan populares como AES puede que sus implementaciones en el lenguaje de programación de tu elección no estén disponibles o tengan vulnerabilidades no conocidas.
