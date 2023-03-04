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

Si quieres saber más de ella en poco tiempo, te recomiendo mucho su capítulo en ese libro, es muy interesante, además de que obtiene lecciones muy valiosas de su vida. Ahora sí hablemos de lo que más gente conoce de ella.

## El principio de sustitución de Liskov

El artículo en el que lo definió se llama ["A Behavioral Notion of Subtyping"](/assets/pdfs/subtyping.pdf). Tiene notación matemática que cuesta un poco leer si no tienes nociones de lenguaje matemático formal, pero resumiremos las ideas básicas aquí.

El espíritu del LSP está basado en las ideas de **subtipado** que Liskov describió en este artículo. Estas ideas tienen _muy poco_ que ver en realidad con herencia en los lenguajes de programación orientados a objetos y mucho más con la **abstracción** y restricciones que hay que tener en cuenta para considerar que un tipo es un subtipo de otro.
Es cierto que Liskov usó las jerarquías de clases para ilustrar sus ideas, pero el principio de su trabajo tiene que ver mucho más con el comportamiento externo de un tipo de datos que con la forma en la que se encapsula este comportamiento.

Pero vayamos a la parte más profunda de la teoría para entender si lo que Liskov propone tiene sentido.

### ¿Qué es un tipo?

Un tipo es la definición de lo que un valor almacenado tiene, puede hacer o las operaciones que se pueden hacer sobre él.

Pongamos un ejemplo. En JavaScript el tipo `Number` define un valor que representa un número de cualquier tipo. Este tipo de dato define las operaciones que podemos hacer sobre los valores con este tipo, por ejemplo:

- Podemos usar el operador `+` para sumar dos datos de este tipo
- Podemos usar el operador `-` para restar dos datos de este tipo
- Las operaciones (excepto las comparativas) entre el tipo de dato `Number` siempre devuelven un valor de este tipo

También definen la _interfaz_ de este tipo de datos, es decir, la forma en la que podemos interactuar con ellos. Normalmente, en lenguajes orientados a objetos, esta interfaz está compuesta por los métodos públicos que se pueden llamar sobre este tipo de dato.

Por ejemplo en JavaScript, el tipo `Number` tiene definido el método `toString` que nos devuelve este valor como una cadena de texto.

Pero Bárbara Liskov expandió esto, proponiendo lo que llamamos **Abstract Data Type** o **Tipo de Dato Abstracto**. Este tipo de dato no tiene una implementación concreta, sino que define la interfaz que debe tener cualquier implementación de este tipo de dato, siendo responsabilidad del programador implementar esta interfaz.

### ¿Qué es un subtipo?

Una de las restricciones más importantes que Liskov propone es que si un tipo de datos tiene definido un método X, entonces cualquier subtipo de est tipo (que en relación con este se llama "supertipo") también debe tener este método definido.

Para hacerlo más generalizable podemos cambiar "método" por cualquier elemento visible en la interfaz de este tipo de dato.
