---
title: "Claridad en el código"
date: 2022-12-22
author: Héctor Patricio
tags: claridad código-claro pláticas
comments: true
excerpt: "Todos quisiéramos tener bases de código perfectas, fáciles de mantener y totalmente claras. Esto es casi imposible, pero podemos acercarnos. Vemos cómo."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1672204121/ivan-bandura-8VePVILfCKU-unsplash_bhsnsa.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_300/v1672204121/ivan-bandura-8VePVILfCKU-unsplash_bhsnsa.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Hablemos de las cosas que hacen más entendible y claro tu código.

Muchas de estas ideas están basadas en la plática ["Clarity" de Saša Jurić](https://www.youtube.com/watch?v=6sNmJtoKDCo) de la Elixir Conf EU de 2021, de hecho, podríamos considerar este artículo como un análisis y extensión de esa plática.

- Cuando trabajamos con bases de código normalmente necesitamos entenderlas. Incluso aunque vayamos a escribir algo nuevo necesitamos entender lo demás para poder integrarlo. Esto lo hacemos mediante la lectura de código.

- Los escritores del código nos transmiten información mediante ese código, lo quieran o no.

- La forma en la que obtenemos conocimiento del código es leyéndolo.

## ¿Qué es la claridad y por qué es mejor que 'el código limpio'?

La claridad como se define en esta plática, es qué tan bien una pieza de código comunica sus verdaderas intenciones. El código claro puede ser entendido sin mucho esfuerzo por alguien que conoce bien el lenguaje: se entiende tanto el problema como la solución que el autor escogió.

La claridad nos hace más eficientes y efectivos. Primero porque obtenemos información más rápido y segundo porque obtenemos la información correcta.

Finalmente, la claridad le da poder al equipo porque hace que cualquiera pueda tomar el código y trabajar con él, en vez de sólo el autor, como muchos estamos acostumbrados.

Para conseguir claridad se tiene que invertir tiempo constantemente.

## Prácticas que mejoran la claridad

Hablemos de cosas que tú y tu equipo pueden hacer para producir código más claro.

### Revisión de código

Esto es la práctica de un equipo de integrar el código a la rama principal solamente cuando ha sido evaluado por cierto números de miembros del equipo. El foco principal de la revisión debería ser la claridad del código.

Para facilitar el proceso, tanto el autor como el revisor pueden seguir ciertas reglas para que el resultado sea código más claro y la revisión sea más fácil.

### Prácticas en el código

Separación de aspectos - No tenía - Dijkstra lo mencionó en su artículo [On the scientific thougth](https://www.cs.utexas.edu/users/EWD/transcriptions/EWD04xx/EWD447.html)
