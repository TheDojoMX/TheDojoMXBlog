---
title: "¿Qué es la abstracción?"
date: 2023-03-10
author: Héctor Patricio
tags: abstracción abstracto abstraction
comments: true
excerpt: "Muchos programadores piden consejos para mejorar su capacidad de abstracción. Vamos a hablar de lo que es y cómo se puede usar para programar mejor."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1678168555/shubham-dhage-w06BFh5bRRA-unsplash_xek5go.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1678168555/shubham-dhage-w06BFh5bRRA-unsplash_xek5go.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Muchos programadores saben intuitivamente que gran parte del trabajo que hacemos como desarrolladores de software consiste en "abstraer", sin llegar a entender completamente qué significa esto.

En este artículo vamos a empezar explicando qué es la abstracción en general y luego cómo puedes mejorar tu habilidad de abstraer para programar más rápido y para crear mejores programas. La capacidad de **crear mejores abstracciones te permitirá crear programas que no creías que pudieran existir o que tú pudieras crear**.

Empecemos por las mismísimas bases.

## Etimología: ¿de dónde viene la palabra abstracción?

**"Abstracción"** viene del latín _abstrahere_, que tiene dos partes principales: **abs** que significa "fuera de", "sin", "a distancia" y **trahere** que significa "tirar". La palabra _abstrahere_ significa literalmente "tirar fuera".

La palabra _abstrahere_ se usa en el sentido de "separar" o "extraer" en el contexto de la filosofía, la matemática y la física. En el contexto de las matemáticas, la abstracción es el proceso de separar un concepto de sus propiedades físicas.

A veces entendemos el proceso de abstraer como la capacidad de generalización. Por ejemplo, si queremos abstraer el concepto de "mesa", lo que hacemos es quitar todas las características concretas de todas las mesas que hemos visto en la vida y entonces vemos lo que tienen todas en común: nos permiten hacer algo sobre ellas, sea parados o sentados. De esta manera tenemos el concepto abstracto de una mesa en nuestra mente. Después podemos aplicar ese concepto a diferentes cosas que veamos.

Los seres humanos somos máquinas de abstraer. Si a un niño pequeño le presentas unos cuantos gatos o perros, es capaz de aprender el concepto "gato" y extenderlo a otros gatos que vea aunque no se parezcan mucho a los que ya vio. Lo que no es capaz de hacer normalmente, es definir en palabras lo que es un "gato" de manera precisa.

Como **resumen**: abstraer es "tirar fuera", sacar las características que definen algo de su contexto concreto y ser capaz de entender ese concepto de manera general.

A estas abstracciones a veces las llamamos **modelos**. ¿Te suena?

## Cómo la usamos en la programación

Ya hemos dicho que aunque los seres humanos nos la pasamos abstrayendo todo lo que vemos en la vida real, no siempre podemos:

1. Delimitar precisamente la abstracción.
2. Expresar o explicar esa abstracción a otras personas.

Y esto precisamente es lo que necesitamos al programar: delimitar nuestras abstracciones y expresarlas en algún lenguaje de programación, como una tabla en una base de datos o de alguna otra forma que las computadoras puedan capturar y procesar, **a esto es a lo que nos referimos cuando hablamos de abstraer en la programación**.

Lo que hace más difíciles las abstracciones en la programación es que normalmente los conceptos no son tan sencillos e incluso son de áreas con las que no estamos familiarizados o no tenemos experiencia.

La capacidad de abstraer es muy importante en casi todo trabajo intelectual, sobre todo aquellos relacionados con la lógica, por eso es supremamente importante en la programación.

¿Por qué decimos esto? Es en esto en lo que la programación se parece al trabajo de un matemático: **debes traducir un problema informal de la vida real, normalmente en lenguaje natural a un lenguaje formal que una computadora pueda entender**. Para hacer esto, debes abstraer los aspectos más importantes del problema para representarlos de manera efectiva en tu programa final.

No nos vamos a poner a filosofar lo que define algo, para eso te recomiendo el libro [Data and Reality de William Kent](https://www.goodreads.com/en/book/show/1753248)

### Ejemplo: un inventario de productos

Cuando queremos representar algo en un carrito de compra en un programa, lo que hacemos es abstraer el concepto de "carrito de compra" y representarlo en el programa.

En este caso, el carrito de compra es un conjunto de productos, cada uno con su precio y cantidad. En el programa, el carrito de compra es una lista de productos, cada uno con su precio y cantidad.

## Cómo mejorar tu capacidad de abstraer

Esta es una de las preguntas que todo programador se hace cuando quiere mejorar su manera y velocidad al programar. Cuando hablamos de "la manera" de programar, nos referimos a la calidad del código que produce.

## Evita los extremos

A veces nos pasamos con las abstracciones, tanto en el nivel de abstracción que usamos como en el momento en el que lo hacemos.

## El costo de las abstracciones

Las abstracciones cuestan más que el código que las sustituyen.

### Zero-cost abstractions (Abstracciones sin costo)

Las abstracciones de costo cero son una propuesta de algunos entornos y lenguajes de programación. Como abstraer normalmente supone un costo en el tiempo de ejecución del programa, las abstracciones sin costo proponen que, aunque puedes usar elementos de más alto nivel en el código, no te van a costar rendimiento en tiempo de ejecución.

¿Entonces en dónde cuestan? Normalmente le cuestan al compilador, reemplazar o expandir macros en tiempo de construcción.

## Conclusión

Mejorar tu capacidad de abstraer conceptos, pero sobr e todo de representarlos de manera eficiente en el lenguaje de programación de tu elección te llevará lejos en la carrera de desarrollo de software.
