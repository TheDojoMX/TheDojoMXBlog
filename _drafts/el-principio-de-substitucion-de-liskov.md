---
title: "El principio de sustitución de Liskov"
date: 2023-03-01
author: Héctor Patricio
tags: lsp liskov solid principios
comments: true
excerpt: "El principio de sustitución de Liskov es uno de las reglas de comportamiento más famosas entre los desarrolladores. Hablemos de lo que significa."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1677648049/brett-jordan-DDupbpu4MS4-unsplash_jdapyu.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1677648049/brett-jordan-DDupbpu4MS4-unsplash_jdapyu.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

El tercer principio enunciado en los principios **SOLID** es el principio de sustitución de Liskov. ¿Qué significa este principio? Y más importante, ¿vale la pena seguirlo? Pero antes de hablar del principio, hablemos de **Barbara Liskov**, la persona que lo inspiró y que estableció los conceptos principales.

## Un poco de historia: Barbara Liskov

Barbara Liskov es una matemática muy reconocida en las ciencias de la computación por los grandes aportes que ha hecho. Es conocida por su trabajo en el diseño de lenguajes de programación y la teoría de tipos. En 1994 junto con Jeannette Wing publicó el artículo del que Robert Martin se sacó lo que el llamó "el principio de sustitución de Liskov" o "LSP" (Liskov Substitution Principle). Ya ves que los _inicialismos_ le dan un aire de importancia a lo que escribes.

En su libro, ["Mentes Geniales. La vida y obra de 12 grandes informáticos"](https://www.marcombo.com/mentes-geniales-la-vida-y-obra-de-12-grandes-informaticos-9788426733573/), Camilo Chacón nos da una semblanza de las contribuciones de Barbara a las ciencias de la computación. Sus principales aportaciones, resumidas son:

- Lenguajes de programación que aplican ideas de polimorfismo, modularidad, abstracción de datos y manejo de excepciones
- Sistemas distribuidos (inventó Paxos antes que Leslie Lamport)
- Abstracción de datos y tipos de datos abstractos

## El principio de sustitución de Liskov

El espíritu de este principio está basado en las ideas sobre **subtipado** de Bárbara Liskov. Estas ideas tienen muy poco que ver en realidad con herencia en los lenguajes de programación orientados a objetos y mucho más con la **abstracción**.
