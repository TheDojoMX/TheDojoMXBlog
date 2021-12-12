---
title: "La regla del 'Cero, Uno o Infinito'"
date: 2021-12-10
author: Héctor Patricio
tags:
comments: true
excerpt: "A veces necesitamos reglas que nos ayuden a desarrollar mejor software. La regal de 'Cero, Uno o Infinito' es una guía para que creemos software más usable."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1120/v1639259189/michael-dziedzic-uZr0oWxrHYs-unsplash_koqk3a.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_320/v1639259189/michael-dziedzic-uZr0oWxrHYs-unsplash_koqk3a.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

La regla del 'Cero, Uno o Infinito' es una guía para diseñar software que sea más fácil de usar, tanto para otros desarrolladores como para los usuarios finales. La regla en inglés es:

> “Allow none of foo, one of foo, or any number of foo.” - Willem van der Poel

Esta regla establece que respecto a la existencia de elementos, deberías permitir que no exista ninguno, solamente uno o un número arbitrario (potencialmente infinito, mientras las limitantes ) de estos elementos. La idea **principal es que no existan límites arbitrarios impuestos por alguna idea sin explicación**.

Algunos ejemplos de esta regla, puesta en práctica:

- Una estructura de datos no limita arbitrariamente el grado de anidado que puede tener
- No existe un normalmente un límite impuesto de recursividad (más allá del dado por el tamaño del _stack_ de ejecución)
- En las bases de datos relacionales existen tres cardinalidades: 1-1 (permitir una), 1-N (un padre puede tener muchos hijos), N-N (varios artículos pueden pertenecer a la misma categoría y un artículo puede tener varias categorías)
- Los carácteres especiales básicos de las expresiones regulares son: `.` (un carácter cualquiera), `+` (uno o más carácteres), `*` (cualquier número de caracteres).


Y esta regla parece que también existe en la naturaleza:

- La procreación es ilimitada mientras los recursos sean suficientes (puedes tener N hijos)
- Tus ancestros directos son uno de cada género (tienes un padre y una madre)
- Tus ancestros indirectos pueden ser infinitos (tu linea genealógica y los hijos de tus hijos pueden ser infinitos)
- Cuando tienes un límite de uno y lo abres para dos, ¿entonces por qué no abrirlo para tres? Si aplicamos esta regla recursivamente llegamos infinito. (Un ejemplo pueden ser las relaciones poliamorosas)


##

