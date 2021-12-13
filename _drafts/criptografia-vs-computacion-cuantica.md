---
title: "Criptografía VS computación cuántica"
date: 2021-12-11
author: Héctor Patricio
tags: criptografía, quantum, matemáticas
comments: true
excerpt: "Se ha escuchado mucho sobre que la criptografía está completamente acabada si la computación cuántica tiene éxito. Entendamos si esto es verdad."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1120/v1639258127/anton-maksimov-juvnsky-wrkNQmhmdvY-unsplash_zfe4zr.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_320/v1639258127/anton-maksimov-juvnsky-wrkNQmhmdvY-unsplash_zfe4zr.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

La computación cuántica es una tecnología muy prometedora que lleva décadas en gestación y cada vez la vemos más cerca. Una las cosas que más le llama la atención es la capacidad de cómputo que las computadoras cuánticas pueden tener, sin embargo, en este artículo aclararemos de qué se trata todo esto y cómo se relaciona con la criptografía, uno de los campos más afectados.

Si no tienes no has escuchado mucho sobre , este video de una presentación dada por [Ignacio Cirac](https://www.xataka.com/investigacion/algun-dia-se-construye-ordenador-cuantico-plenamente-funcional-sera-gracias-parte-a-este-cientifico-espanol-hablamos-ignacio-cirac) nos da una introducción a lo que promete y las bases de funcionamiento de la computación cuántica.

<iframe width="560" height="315" src="https://www.youtube.com/embed/WJ3r6btgzBM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

---

Ahora veamos a más detalle cómo **computa** una máquina cuántica y entendamos por qué no _toda la criptografía está perdida_, aunque tuviéramos una computadora cuántica funcional hoy mismo.

## Principios de funcionamiento de una computadora cuántica

Hablemos un poco de los principios físicos y matemáticos que hacen especial a una computadora cuántica.

### Superposición cuántica

Una computadora cuántica está basada en el [principio de superposición cuántica](https://es.wikipedia.org/wiki/Superposici%C3%B3n_cu%C3%A1ntica), que establece en palabras comunes que una partícula puede poseer múltiples estados a la vez de diferentes magnitudes físicas. Una forma fácil en la que se ha mencionado este principio es que "puede estar en don lugares a la vez". Lo que sale de nuestra comprensión común de la física es que esto de tener múltiples estados desaparece cuando lo observamos, se dice que su _ecuación de onda_ colapsa, lo que significa que la partícula "se decide" por uno de los múltiples estados en los que podía estar.

El ejercicio mental del [Gato de Schrödinger](https://www.youtube.com/watch?v=lzxKZx7we4s) te puede ayudar a imaginarlo, pero en [este video puedes de Quantum Fracture](https://www.youtube.com/watch?v=9JlOmEEyTOU) te ayudará a profundizar más en la complejidad del tema y como no es tan sencillo como "puede estar en dos estados a la vez", sino en un número _infinito de estados_.

Este artículo te explicará el principio de superposición cuántica sin matemáticas avanzadas: [Superposición, una aproximación sin matemáticas avanzadas a la motivación de la mecánica cuántica](https://www.elclaustro.edu.mx/agnosia/index.php/component/k2/item/427-superposicion-una-aproximacion-sin-matematicas-avanzadas-a-la-motivacion-de-la-mecanica-cuantica).

**Resumen:** Una particula como un átomo, un electron o un fotón, puede poseer múltiples estados físicos a la vez, con diferentes combinaciones entre todos sus posibles estados, dando lugar a una infinidad de estados posibles. Las probabilidades de cada estado están contenidas en su _función de onda_, y cuando medimos (miramos) una partícula se define en un estado de toso los psobles.