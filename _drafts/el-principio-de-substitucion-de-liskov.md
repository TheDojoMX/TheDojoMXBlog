---
title: "El principio de sustitución de Liskov"
date: 2023-03-05
author: Héctor Patricio
tags: lsp liskov solid principios solid-principles
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

Pero Bárbara Liskov expandió esto, proponiendo lo que llamamos **Abstract Data Type** o **Tipo de Dato Abstracto** (les llamaremos **ADT**). Un tipo abstracto de dato es una **definición de un tipo de dato**.

Este tipo de dato no tiene una implementación concreta, sino que define la interfaz que debe tener cualquier implementación de este tipo de dato, siendo responsabilidad del programador implementar esta interfaz.

Ejemplos de ADT's son por ejemplo las Colas (Queues), Listas (Lists), Pilas (Stacks), etc. El ADT define que interfaz debe tener cualquier implementación de este, y cada lenguaje o programador puede implementarlo como le convenga.

Ahora, ¿qué es un subtipo?

### ¿Qué es un subtipo?

Un subtipo es una derivación de un tipo. Esta derivación puede ser una variación, una generalización o una especialización de este tipo. Normalmente se usan para hacer **especializaciones**.

Y aquí es donde empezamos a entrar en el terreno del LSP. Una de las restricciones más importantes que Liskov propone es que si un tipo de dato tiene definido un método X, entonces cualquier subtipo de este tipo (que en relación con este se llama "supertipo") también debe tener este método definido.

Para hacerlo más generalizable podemos cambiar "método" por cualquier elemento visible en la interfaz de este tipo de dato.

Así, nos podremos usar que estas clases sean intercambiables entre ellas, sin siquiera tener que hacer consciente a la parte del programa que la usa de qué clase se está usando, mientras sea una clase derivada de la clase base.

Un ejemplo de la vida real puede ser con un cámara. Todos tenemos en la mente las funciones básicas de una cámara electrónica:

- Podemos encenderla y apagarla
- Puede tomar fotos (disparador)
- Puede mostrarnos las fotos
- Podemos descargar las fotos
- Podemos borrar las fotos

Mientras la cámara cumpla con esas características (su interfaz) no tendremos problema para usarla, independientemente de la marca o modelo de la cámara. Los subtipos del tipo de dato abstracto `Cámara` podría ser entonces:

- `Cámara DSLR`
- `Cámara Compacta`
- `Cámara Mirrorless`
- `Cámara de teléfono móvil`

En realidad en la programación, esta interfaz es un poco más estricta: los métodos deben de llamarse igual y tener la misma firma (parámetros y tipo de retorno). Es como si la cámara tuviera los botones en el mismo lugar y se usaran de la misma forma.

Y esto es básicamente el principio de sustitución de Liskov, la capacidad de usar clases derivadas de una clase principal sin ningún cambio en el código que rodea. ¿Crees que es útil?

## Crítica sobre el LSP

Tal como lo describimos aquí (mal llamado, para mi) principio de sustitución de Liskov parece una muy buena idea, ya que permitirá que crees nuevos comportamientos en partes específicas de tu código sin en tener que afectar a muchas partes de tu código.

Lo que no estuvo tan bien, _históricamente_, es que este principio siempre ha sido explicado y relacionado con la HERENCIA de clases, en lugar de poner énfasis en la abstracción de tipos de datos. Esto ha hecho que muchos desarrolladores piensen que esta práctica sólo aplica a la programación orientada a objetos y no al paradigma funcional, por ejemplo.

De hecho, el principio como es enunciado en [Design Principles and Patterns](/assets/pdfs/DesignPrinciplesAndPatterns.pdf) dice:

> Subclasses should be substitutable for their base classes.
---
> Las subclases deben ser sustituibles por sus clases base.

También, como se menciona en el artículo en el que se presenta originalmente este principio dice:

> FUNCTIONS THAT USE POINTERS OR REFERENCES TO BASE CLASSES MUST BE ABLE TO USE OBJECTS OF DERIVED CLASSES WITHOUT KNOWING IT
---
> Funciones que usen punteros o referencias a clases base deben ser capaces de usar objetos de clases derivadas sin saberlo

Como puedes ver, el consejo es que está directamente relacionado con la herencia de clases y jerarquías de objetos. Incluso llega a hablar de punteros y referencias a clases base, es decir, a la clase padre.

De hecho, esto tiene cierta justificación, porque Barbara Liskov siempre habla de objetos. Lo que Liskov nunca hace es hablar de _Clases_ y jerarquías de clases. Ella habla de tipos de datos abstractos, que son una abstracción de los objetos, por lo que esta idea se extiende a **cualquier artefacto computacional que se encargue de encapsular un comportamiento**.

¿Qué es encapsular? Es **ocultar la implementación** y exponer sólo lo necesario para que el resto del programa pueda usarlo. Esto es lo que hace una clase, un módulo, una función, etc.

¿Qué te recuerda esto? Lo mismo de lo que hemos hablado en los principios anteriores: **abstracción**. Esconder lo más que se pueda la información, _Information Hiding_.

### Conclusión
