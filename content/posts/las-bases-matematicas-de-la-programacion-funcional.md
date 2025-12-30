---
title: "Las bases matemáticas de la programación funcional"
date: 2021-03-18
author: "Héctor Patricio"
tags: ['matemáticas', 'math', 'fp', 'programación-funcional']
description: "La programación funcional tiene bases matemáticas muy interesantes, hablemos un poco de ellas y cómo te pueden ayudar a entenderla mejor."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1616045099/michael-dziedzic-VlZYu3nZIRI-unsplash_yxm6kr.jpg"
draft: false
---

La programación funcional tiene conceptos muy relacionados con las matemáticas. Aquí te vamos a platicar de sus orígenes y de algunos conceptos matemáticos directamente embebidos en la programación funcional.

Lo primero que tienes que recordar es que las matemáticas no tienen que ver  _necesariamente_ con números, sino con el razonamiento y la _formalización_ de este. En este artículo hablamos más de ello: [Las matemáticas que necesitas para programar](/2019/12/25/las-matematicas-que-debes-saber-para-programar.html).

Ahora sí, empecemos con lo más fundamental de las matemáticas que soportan la programación funcional, no sin mencionar que podemos afirmar que la programación funcional _es una forma de matemáticas_.

## Cálculo Lambda

El cálculo lambda es una forma de definir todo lo que entendemos como matemáticas y de describir _cálculos_ o _cómputo_. Es una notación que permite definir todos los elementos necesarios para crear razonamientos formales abstractos.

El cálculo lambda fue diseñado por **Alonzo Church** como una forma de responder a un problema muy profundo de las matemáticas: **"¿Es posible encontrar una forma de computación universal que, mediante la representación de problemas y una serie de pasos definido y finitos permita resolverlos?"**.

Esta pregunta fue planteada por David Hilbert y se conoce como el *Entscheidungsproblem*, o _"El problema de la decisión"_. De esta pregunta se deriva toda la computación moderna, ya que para responder estas preguntas **Alan Turing** diseñó las _Máquinas de Turing_. Si quieres saber más de esto, el libro [La Mente Nueva del Emperador de Roger Penrose](https://www.cs.buap.mx/~jitalo/libros/lanueva.pdf) lo explica muy bien, junto con muchas otras cosas.

### Funciones

Las funciones o abstracciones son la base del cómputo en el Cálculo Lambda y lo son también en la programación funcional. Puedes pensar en las funciones como en la parte central del cómputo, la que representa las acciones a realizar con la información introducida, que en el Cálculo lambda, **siempre será otra función**. Así es, no existen los número naturales, y todo se puede representar con funciones. Si quieres un idea más clara de cómo se puede lograr esto la plática de John Huges, [Why Functional Programming Matters](https://www.youtube.com/watch?v=XrNdvWqxBvA) da algunos ejemplos con Lisp.

Además esta plática en español explica más del Cálculo Lambda: [Cálculo Lambda por Jaime Pavlich-Mariscal](https://www.youtube.com/watch?v=i1zYBLdlxfc).

Y aquí hay un libro gratuito que puedes estudiar si quieres adentrarte más en esto: [Introduction to Lambda Calculus](http://www.cse.chalmers.se/research/group/logic/TypesSS05/Extra/geuvers.pdf)

## Combinadores

Un combinador es una abstracción o función en el cálculo lambda, que no tiene variables libres o, en su defecto, sólo usa otros combinadores en su definición. Son funciones que sirven para crear cálculos más complejos mediante la mezcla de ellas.

Las variables libres son las que **no se reciben como parámetros**. Los combinadores sirven para crear un lenguaje sobre el cálculo lambda y crear abstracciones más fácilmente y han sido el objeto de estudio de varios matemáticos.

Uno de ellos Raymond Smullyan, los enumeró poniéndoles nombres de aves, basados en las letras con las que se les identificaba y en su libro [To Mock a Mockingbird](http://douxnet.weebly.com/uploads/2/0/4/1/20418601/raymond_m._smullyan-to_mock_a_mockingbird_and_other_logic_puzzles__including__an_amazing_adventure_in_combinatory_logic-knopf_1985.pdf) los usa para crear algunos acertijos.

Puedes aprender más de los combinadores con ejemplos en JavaScript en esta plática: [Lambda Calculus - Fundamentals of Lambda Calculus & Functional Programming in JavaScript](https://www.youtube.com/watch?v=3VQ382QG-y4)

Aquí hay algunos ejemplos de combinadores en JavaSCript

```javascript
// Combinador I, Idiot o función identidad
const I = (x) => x
// Combinador K, Kestrel o función constante
const K = (x) => (y) => x
// Combinador S, Starling o función de substitución
const S = f => g => x => f (x) (g (x))
```

Justo de esta rama de la lógica viene el famoso [Y combinator](https://medium.com/@ayanonagon/the-y-combinator-no-not-that-one-7268d8d9c46), el combinador que permite la recursión. Aquí hay artículo que explica cómo se llega a él, si te quieres ir por el hoyo del conejo: [Deriving Y Combinator](https://homes.cs.washington.edu/~sorawee/en/blog/2017/10-05-deriving-Y.html)


### Cálculo SKI

Debido a que todas las matemáticas y cosas computables se pueden expresar con los combinadores S, K e I, existe toda una rama llamada **Cálculo SKI**, en el que estos tres combinadores son los únicos elementos necesarios para expresar todo lo demás.

## Teoría de categorías

La teoría de categorías explora la composición de elementos y la creación de grupos con "objetos" relacionados entre ellos. [Bartosz Mileswsky](https://bartoszmilewski.com/) afirma que la teoría de categorías es muy importante para los programadores porque nos permite entender la composición y esta es la base para construir programas complejos.

La teoría de categorías se extiende más allá de la programación funcional, de hecho todos los sistemas de tipos de los lenguajes se comportan como una categoría. Puedes entender más de qué se trata en el libro de Bartosz Mileswsky ["Category Theory for Programmers"](https://github.com/hmemcpy/milewski-ctfp-pdf).

## ¿Y todo esto, a mi qué?

Conocer las bases de la programación funcional te puede dar un índice muy valioso como referencia a temas en los que tienes que profundizar si quieres ser un mejor programador@ funcional y tú lógica en general.

La programación funcional y las ideas provenientes de ella están mejorando la forma en que hacemos software, ya que dan permiten un mejor tratamiento de la información que en muchos casos es más fácil de entender que su contraparte imperativa.

Puedes ver algunas de las características y ventajas de la programación funcional en [este artículo](/2019/03/30/que-es-la-programacion-funcional.html) y si quiere aprender, compilamos algunos recursos aquí: [Los mejores recursos para aprender programación funcional.](/educación/2019/04/06/los-mejores-recursos-para-aprender-programacion-funcional.html)
