---
title: "Tipos de algoritmos criptográficos: cifrados de flujo"
date: 2021-12-12
author: "Héctor Patricio"
tags: ['cifrado', 'cypher', 'flujo', 'aes']
description: "Ya hemos hablado en este blog sobre qué es la criptografía, los cifrados de bloque y ahora ha llegado la hora de hablar de cifrados de flujo. Veamos qué son y para qué sirven."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1120/v1639633812/solen-feyissa-IfWFKG3FXE4-unsplash_dvnbjc.jpg"
draft: false
---

Ya hablamos de [lo que es la criptografía](/2019/11/12/criptografia-basica-para-programadores-que-es-la-criptografia.html) y del tipo de cifrado más fuerte y seguro que existe en la criptografía: [los cifrados de bloque](/2020/12/03/tipos-de-algoritmos-criptograficos.html).

Ahora hablemos de cómo puedes transformar cadenas de texto plano de tamaño indeterminado en cadenas de texto cifradas del mismo tamaño. Esto se logra con los cifrados de _flujo_ o **stream ciphers**.

## Definición de cifrado de flujo

La mejor manera de entenderlos es en _contraste_ con los cifrados de bloque: mientras los cifrados de bloque toman pedazos de contenido de tamaño fijo y los cifran, aplicando diferentes técnicas para abarcar todo el contenido, los cifrados de flujo toman **contenido de tamaño arbitrario y lo cifran**, bit por bit, devolviéndote un texto cifrado del mismo tamaño.

Son muy útiles cuando no sabes el tamaño del contenido que vas a cifrar o cuando van ir llegando de manera continua sin que sepas exactamente cuánto y cada cuando, justamente como un **flujo de información**.

Los cifrados de flujo se consideraban "cifrados de hardware" porque eran más ligeros que los de bloque y se podían implementar en menos espacio en un chip, pero ahora tanto los cifrados de bloque como los de flujo son adecuados para implementarse en hardware.

## Funcionamiento

Un cifrado de flujo trabaja generando una cadena de bits pseudo-aleatorios que después combina con el contenido que va a cifrar mediante la operación **XOR**, también conocida como **suma módulo 2**. Para descifrar un texto cifrado, algoritmo genera los mismos bits pseudo-aleatorios y los vuelve a combinar, dejando así solamente el texto claro. A esta cadena de bits pseudo-aleatoria se le conoce como el _keystream_ o _cadena de bits de clave_. En el video ["XOR de tamaño fijo \| Cryptopals Crypto Challenges"](https://youtu.be/74MYHpGzRR8) explicamos por qué el XOR es una operación perfecta para usarse en criptografía y por qué en algunos recursos se la llama "suma módulo 2".


La parte más importante es entonces el generador del _keystream_, y que sea capaz de volver a generar los mismos bits pseudo-aleatorios para descifrar.

Un cifrado de flujo normalmente utiliza una llave y un **nonce**, un número usado una única vez con esa llave.

A muy alto nivel, los cifrados de flujo pueden trabajar de dos formas:

1. **Mediante mantener un estado secreto**. Después de haber sido inicializados con una llave y un nonce, el algoritmo mantiene un estado interno que se va actualizando en cada nueva llamada.
2. **Mediante un contador**. Este tipo de algoritmos recibe a parte de la llave y el nonce, un contador que se incrementa en cada llamada, de esta manera no es necesario mantener un estado interno secreto.

## Ejemplos de cifrados de flujo

Veamos algunos ejemplos de cifrados de flujo, sus características y sus usos, así como qué tan seguros son.

### RC4

Es el cifrado de software que se usaba para la comunicación entre los routers WI-FI que usaban WEP y tus dispositivos. También se usaba en las comunicaciones TLS. Fue diseñado por el mismo inventor de MD5, [Ron Rivest](https://people.csail.mit.edu/rivest/){:target=blank}. Trivia: RC significaba originalmente: "**R**on's **C**ode". Se conocen ataques contra el cifrado y sobre todo sobre sus implementaciones, pero se sigue usando, así que ten mucho cuidado cuando los dispositivos que usas te ofrezcan configurarlo (como en el caso de los routers con "seguridad" WEP).

### A5/1

Fue el cifrado de flujo de hardware de que se usaba para cifrar las comunicaciones inalámbricas 2G. Se encontraron vulnerabilidades en él, al principio de la década de los 2000 y ahora se puede descifrar completamente.

## Grain-128a

Es uno de los cifrados de flujo recomendados por la [´EAM competition](http://www.ecrypt.eu.org/stream/project.html),
usa una llave 128 bits y un nonce de 96 bits. Está pensado para ser implementado en hardware.

Es seguro todavía y usado en sistemas de hardware de bajo presupuesto que requieran un cifrado ligero.
### Salsa20

Es un cifrado de flujo, orientado a software que también fue recomendado por la ´EAM competition. Tiene una implementación sencilla, lo que lo ha hecho popular. Usa una llave, un nonce y un contador para generar el flujo de cifrado.

Aplica una serie de transformaciones en "rounds" y tiene tres variaciones, dependiendo del nivel de seguridad necesario y la velocidad que deseemos: Salsa20 (20 rounds), Salsa20/12 (12 rounds), Salsa20/8 (8 rounds), siendo el de 8 rounds el que menos seguridad  ofrece. Hay un ataque teórico contra Salsa20/8 que reduce su seguridad a 2^251 operaciones, todavía imposible de llevar a la práctica.

### AES-CTR

Este es un cifrado de bloque disfrazado de cifrado de flujo, como diría JP Aumasson, el autor de "Serious Cryptography". Es el cifrado AES usado en **Counter Mode** o **modo contador**, que ya explicamos en el [artículo sobre los cifrados de bloque y sus modos de operación](/2020/12/03/tipos-de-algoritmos-criptograficos.html). Cualquier cifrado de bloque que pueda ser usado en modo **counter** se comportará como un cifrado de flujo.

La desventaja de esto es que normalmente queremos que los cifrados de flujo sean ligeros y rápidos y la velocidad de esta implementación dependerá en gran medida del cifrado que se use.

## Evitando errores

Si estás usando un cifrado de flujo, **debes evitar en todo momento re-usar el nonce**, recuerda que la única razón de existencia del _nonce_ es ser usado una única vez con la misma llave. Esta es la forma más fácil de usar mal los cifrados de flujo, y elimina completamente la seguridad teórica que puedan ofrecer.

## Conclusión y aplicaciones

Los cifrados de flujo actualmente son seguros (Salsa20, Grain-128a y  AES-CTR) y los puedes usar con confianza siempre que requieras cifrar datos de longitud desconocida o que llega (o se va) con un flujo de información.

Evita reutilizar el Nonce, el counter y elige una llave segura, lo más aleatoria posible y estarás listo para usarlos en cualquier desarrollo.