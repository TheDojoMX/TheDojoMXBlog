---
title: "Tipos de algoritmos criptográficos: cifrados de flujo"
date: 2021-12-12
author: Héctor Patricio
tags: cifrado cypher flujo aes
comments: true
excerpt: "Ya hemos hablado en este blog sobre qué es la criptografía, los cifrados de bloque y ahora ha llegado la hora de hablar de cifrados de flujo. Veamos qué son y para qué sirven."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1120/v1639633812/solen-feyissa-IfWFKG3FXE4-unsplash_dvnbjc.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_320/v1639633812/solen-feyissa-IfWFKG3FXE4-unsplash_dvnbjc.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Ya hablamos de lo que es la criptografía y del tipo de cifrado más fuerte y seguro que existe en la criptografía: los cifrados de bloque. Ahora hablemos de cómo puedes transformar cadenas de texto plano de tamaño indeterminado en cadenas de texto cifradas del mismo tamaño. Esto se logra con los cifrados de _flujo_ o **stream cyphers**.


## Definición de cifrado de flujo

La mejor manera de entenderlos es en contraste con los cifrados de bloque: mientras los cifrados de bloque toman pedazos de contenido de tamaño fijo y los cifran, aplicando diferentes técnicas para abarcar todo el contenido, los cifrados de flujo toman contenido de tamaño arbitrario y lo cifran, devolviéndote un texto cifrado del mismo tamaño.

Son muy útiles cuando no sabes el tamaño del contenido que vas a cifrar o cuando va ir llegando de manera continua sin que sepas exactamente cuánto y cada cuando, justamente como un **flujo**.

## Funcionamiento

Un cifrado de flujo trabaja generando una cadena de bits pseudo-aleatorios que después combina con el contenido que va a cifrar mediante la operación **XOR**. Para descifrar un texto cifrado, algoritmo genera los mismos bits pseudo-aleatorios y los vuelve a combinar, dejando así solamente el texto claro. A esta cadena de bits pseudo-aletoria se le conoce como el _keystream_ o _cadena de bits de clave_.

Un cifrado de flujo normalmente utiliza una llave y un **nonce**, un número usado una única vez con esa llave.

A muy alto nivel, los cifrados  
## Ejemplos de algoritmos de cifrados de flujo

## Conclusión y aplicaciones