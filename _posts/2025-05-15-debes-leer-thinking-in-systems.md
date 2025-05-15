---
title: "Debes leer 'Thinking in Systems'"
date: 2025-05-15
author: Héctor Patricio
tags: libros sistemas complejidad
comments: true
excerpt: "El pensamiento de sistemas es una de las habilidades más importantes para los desarrolladores de software. Hablemos de un libro que te ayuda a cultivarlo."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1440/v1740059354/ricardo-frantz-nEd9E9V8Qx0-unsplash_wnklhe.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_440/v1740059354/ricardo-frantz-nEd9E9V8Qx0-unsplash_wnklhe.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

El libro "Thinking in Systems" de [Donella Hager Meadows](https://en.wikipedia.org/wiki/Donella_H._Meadows)
es un libro muy importante para cualquier desarrollador de software. ¿Por qué? Los desarrolladores nos dedicamos
a hacer _sistemas_, y este es justo el tema principal del libro, escrito por una experta en sistemas complejos.

Veamos por qué puede ser una buena lectura para ti y por que te recomiendo leerlo lo antes posible.

## A cerca de Thinking in Systems

**Thinking in systems** es un libro un poco antiguo, publicado hace casi 17 años, en 2008, después del
fallecimiento de su autora. Pero el primer borrador de libro ya estaba circulando en **1993**.
Esto te lo estoy diciendo como un recordatorio más de que muchas de las ideas que vale la pena leer tienen
mucho tiempo de haber sido escritas, sobre todo en comparadas con las ideas a las que les hacemos
caso en el mundo del software.

## De qué trata Thinking in Systems

Pero, ¿de qué trata **Thinking in Systems**? Este libro te da una introducción a los conceptos básicos
del modelado de sistemas, empezando por ejemplos muy sencillos y avanzando un poco en complejidad, sin
presentarte nada realmente complejo. Te ayuda a comprender cómo empezar a modelar un sistema usando
ejemplos y diagramas sencillos.

Pero antes, ¿qué es un sistema? El libro lo define como una conjunto de elementos que interactúan entre sí
para lograr un objetivo. Lo más importante de un sistema es que su comportamiento no se puede explicar
observando el comportamiento individual de sus elementos, por lo que se dice lo que distingue a un sistema
de un montón de elementos que no lo son es que **"un sistema es más que la suma de sus partes"**.

Los componentes principales de un sistema son:

- **Almacenes (stock)**: Es un lugar físico o virtual donde se almacenan o van acumulando cosas,
en sistemas de software los puedes pensar como un buffer. Los stocks pueden tener límites o no. En el libro
se usa el ejemplo de las existencias de una agencia automotriz, el stock es el inventario de autos
que tienen para la venta.
- **Flujos (flow)**: Son los movimientos, es decir, entrada y salidas de las cosas que se mueven entre
almacenes o dentro y fuera del sistema.

Y ya, con esto puedes empezar a modelar un sistema. Existen casos especiales sobre todo de flujos que
son muy importantes y que son lo que les da su comportamiento interesante:

- **Flujos de retroalimentación**: Cuando los cambios en la condición de un almacén causan cambios en
sus flujos de entrada y de salida, tenemos un flujo de retroalimentación. Piénsalo en el caso 
de un sistema de control de inventario, si se ve que no hay suficientes autos para la venta de la
siguiente semana, se piden bastantes autos, pero si el almacén está casi lleno, se piden menos.

- **Tasas de cambio**: Algo que considerar es que los cambios en el mundo real no son instantáneos, por lo que
todo lo que hemos hablado hasta ahora está afectado por un ritmo de cambio.

Pero ya te estoy adelantando de más, para que comprendas esto mejor, te recomiendo leer el libro.

### Tipos de sistemas

Lo más interesante de este libro es el análisis de los comportamientos de los sistemas, y cómo es que
aunque un sistema esté compuesto de partes completamente entendidas, el comportamiento del sistema
no es obvio o fácil de predecir, sin embargo, sí hay patrones que puedes identificar y entender.

El libro te presenta una clasificación de sistemas a la que le llama "un zoológico de sistemas",
clasificándolos como si fueran especies bien entendidas de animales. Aquí podemos ver varios tipos
de sistemas y sus destinos finales:

- Sistemas que se mantienen estables y funcionando.
- Sistemas resilientes que se adaptan a los cambios.
- Sistemas destinados a desaparecer: por su crecimiento desmedido o porque no producen resultados.

En esta parte podrás aprender a identificar varios patrones más.

## Cómo controlar y cambiar un sistema

Una de las lecciones más importantes de "Thinking in Systems" es que los sistemas son muy sensibles
a los cambios y que no es fácil comprender su efectos. Por lo tanto, un sistema es **difícil de controlar**
o cambiar y no nos queda más que hacer experimentos para entender cómo cambiarlo.

El libro da una lista de 12 cosas que podemos hacer para cambiar un sistema, pero deja claro que ninguna
de esas cosas es infalible. Esto es importante porque los desarrolladores de software somos muy propensos
a sentir que entendemos un sistema más de lo que realmente lo entendemos y segundo a pensar que lo podemos
cambiar con facilidad haciendo intervenciones sencillas. Esto normalmente lleva al desastre.

### Reglas para vivir en un mundo de sistemas complejos

Finalmente, Donella da una lista de 15 reglas o principios para comportarnos mejor en un mundo en
el que los sistemas son engañosos, que se me hacen esenciales para cualquier persona que trabaje en el área del conocimiento,
y son especialmente importantes para los desarrolladores de software. Cuando los leas verás que tienen mucho
que ver con las "buenas prácticas" que se fomentan en diferentes metodologías de desarrollo de software.

La mayoría tienen que ver con la idea de manejar correctamente la información que tenemos, clarificarla,
registrarla y compartirla.

## Qué podemos aprender los desarrolladores de software

Ya hemos repetido hasta el cansancio que los desarrolladores de software _debemos ser expertos en modelar
sistemas_. ¿Pero por qué? Recuerda que tu trabajo es representar el mundo real en un lenguaje de programación,
conectar diferentes piezas de software para que la información fluya, y mantener esos sistemas funcionando,
al mismo tiempo que cuidas de los recursos que consumen y te aseguras de que evolucionen para que sigan siendo
precisos y útiles.

Todo lo anterior implica **primero** entender el sistema del mundo real y **después** representarlo en nuestras
computadoras. Así que creo que es obvio por qué este libro es tan buena lectura para cualquier desarrollador de
software que quiera avanzar en su carrera: te ayudará a ser mejor en tu trabajo.

Pero el libro tiene una lección que me parece de suma importancia: los sistemas del mundo real son más complejos
de lo que podemos representar en cualquier medio de representación humano, por lo que debemos ser explícitos
sobre lo que estamos modelando y sus límite, siempre manteniendo una actitud de curiosidad, aprendizaje y
humildad intelectual. Este punto específicamente es lo que los desarrolladores de software se beneficiarán
de aprender a hacer, y es una de las razones por las que este libro es tan importante.

## Conclusión

Si eres desarrollador de software y quieres mejorar tu habilidad para crear
sistemas complejos que sirvan en el mundo real, mientras antes leas este libro, mejor. No solo lo leas,
**estudia** Thinking in Systems, _toma notas_, y pon en práctica lo que aprendas en los nuevos sistemas que
diseñes y construyas.

El mensaje de fondo de Meadows es que aquellos que nos dedicamos a entender y modelar el mundo podemos
tener un gran impacto en la forma en la que funcionan las cosas, pero ese impacto no es fácil de lograr y
mucho menos inmediato. A final de cuentas, ¿no quieres que tu trabajo sea importante? Si es así, seguir
los consejos de este libro te ayudará a que eso suceda.
