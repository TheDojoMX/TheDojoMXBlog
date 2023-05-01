---
title: "¿Por qué deberías leer Data and Reality?"
date: 2023-04-22
author: Héctor Patricio
tags: libros modelado-de-datos filosofía desarrollo-de-software
comments: true
excerpt: "Hablemos de Data and Reality, un libro que te ayudará a ser mejor desarrollador de software, porque se va a las raíces de los problemas que resolvemos a diario."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1682777065/ilgmyzin-GHazVhDDPZs-unsplash_poxzc5.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1682777065/ilgmyzin-GHazVhDDPZs-unsplash_poxzc5.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Todos los desarrolladores de software tienen algo que ver con el modelado de datos, aunque nunca tengan que trabajar con una base de datos directamente.

Gran parte de nuestro trabajo consiste en modelar entidades del mundo real en el código, transformarlas, guardarlas y recuperarlas. En mi opinión, es una de las habilidades **fundamentales** cuando estamos desarrollando. De hecho, si lo piensas, cuando estás programando un algoritmo, estás modelando un _procedimiento_ de la vida real en código. Este proceso normalmente incluye **datos**, que son representaciones de _entidades_ del mundo real.

Por lo anterior, cualquier cosa que puedas aprender sobre modelado de datos, te ayudará directamente en tu carrera como desarrollador. En este artículo hablaremos de un libro muy especial que te puede ayudar a ser mejor en esta área independientemente del nivel en el que te encuentres en tu carrera. Y si lo piensas más profundamente, puede que te ayude a desarrollar una forma de pensar más adecuada a los problemas que queremos resolver en la actualidad.

**Data and Reality** trata sobre modelado de datos, escrito po William Kent, alguien con mucha experiencia en el tema. El libro tiene tres ediciones la primera es de 1978, la segunda (una actualización) es de 2000 y la tercera, después que Kent murió, es de 2012. La mejor de todas es segunda edición, ya que la tercera se podría considerar un libro completamente diferente, recortado y con comentarios de [Steve Hoberman](https://technicspub.com/steve-hoberman/), otro modelador de datos pero siento que con u enfoque bastante diferente al de Kent.

Hablemos de los temas principales del libro y por qué te conviene leerlo.

## Buscando las respuestas donde parece más sencillo

Hay muchas cosas difíciles de resolver en el desarrollo de software y parece que siempre estamos buscando la respuesta en el lugar que parece más obvio o en el que es más fácil buscar, en lugar de donde es más probable que encontremos las respuestas.

El ejemplo que utilizan en el libro para explicarlo y que me parece completamente acertado es una broma acerca de un borracho que pierde sus llaves y se la pasa toda la noche buscando bajo una farola. Cuando alguien le pregunta por qué no busca en otro lado, **el borracho responde que es porque ahí hay luz.**

En el desarrollo de software podría parecer que a veces hacemos lo mismo. Para buscar la solución a un problema, siempre nos vamos a los mismos lados porque es donde nos sentimos cómodos o porque siempre se ha buscado ahí. Por ejemplo, nos centramos en la tecnología, en las plataformas o en los lenguajes. Pero es muy probable que el problema no esté ahí, sino en lugares más profundos.

Es por eso que este libro se enfoca en cuestiones más profundas del modelado de datos. No en los lugares comunes, ni siquiera en hablar de cómo hacerlo, sino en preguntas que te llevaran a pensar cosas profundas y que probablemente modifiquen tu visión del mundo y tu forma de trabajar **permanentemente**.

Así que, empecemos hablando de lo que este libro enseña y de qué lecciones podemos sacar de él.

## Cuestiones principales

Hablemos de los conceptos principales de representación de información.

### Entidades

Cuando guardamos cosas en una base de datos o las representamos en código, casi siempre nos referimos a ellas como **entidades**.

El libro empieza cuestionando, **¿qué es una entidad?**

La primera respuesta y que ya te pone a pensar es que una entidad "es un estado de la mente". ¿Cómo? Está bastante rara esa definición. Esta frase va por el lado de que una **entidad** más allá de algo que exista en la **realidad** como algo identificable e indivisible, algo que tiene límites fijos, _en realidad_ es algo a lo que nosotros le damos significado, y que nosotros delimitamos o entendemos en ciertos contextos.

Pongamos algunos ejemplos para entender eso. La leyenda del barco de **Teseo** relata que cuando él regresó de Creta, donde había matado al **Minotauro**, el pueblo de Atenas le rindió honores y conservó su barco en lo alto de una colina como un monumento para recordar su hazaña.

Con el tiempo, el barco se fue deteriorando y se le fueron cambiando las partes, hasta que ya no quedó ninguna parte original.

La pregunta es: ¿sigue siendo el _"Barco de Teseo"_? ¿Es el mismo barco si no tiene ninguna parte original? ¿Es el mismo barco si se le cambia una sola parte, o muy pocas?

Esta historia sirve para ilustrar que las entidades como objetos inmutables no existen en la vida real, sino que son cosas que en nuestra mente delimitamos y que, junto con otras personas, les asignamos una identidad y un significado. El _"Barco de Teseo"_ sigue siendo el mismo mientras nosotros lo consideremos así.

Exactamente así se comportan las entidades que como desarrolladores modelamos en nuestros programas. No son cosas permanentes, a veces ni siquiera cosas completamente definidas, sino que nosotros les asignamos límites y **significado**.

## Identidad y cambio

Cuando queremos registrar algo en una computadora, normalmente necesitamos una forma de referirnos a ese "algo", a esa entidad. Esto que usamos para referirnos a las entidades se llama **identidad**.

Idealmente una identidad es un elemento inmutable
y único entre todas las entidades de nuestro sistemas. Aquí nos podemos encontrar con varios casos:

- La entidad no tiene nada único por lo que podamos referirnos a ella (elementos que se hacen repiten, por ejemplo libros)
- El conjunto de todos los _atributos_ de la entidad puede constituir una identidad
- Las entidades tienen varios atributos únicos y hay que escoger uno

Pensar en la naturaleza de nuestro problema, en los términos de arriba nos puede llevar a la solución. Piensa en el primer caso, por ejemplo: cuando algo no tiene identificador natural, tendemos a asignar un identificador único arbitrario a la entidad cuando la metemos en el sistema. Por ejemplo, es un práctica muy común asignar identificadores numéricos incrementales. La primera entidad registrada del tipo es la 1, la segunda es la 2, etc. También se pueden usar los UUIDs, que son identificadores únicos generados aleatoriamente, y que por lo general evitan problemas como el de permitir que alguien adivine el identificador de otra entidad.

Pero si la entidad tiene un identificador único inmutable, ¿por qué no usarlo? ¿Puede ser una solución más natural?

¿Qué pasa cuando lo que creíamos inmutable cambia? Eso es algo que normalmente rompe lo que hicimos y tenemos que idear formas de componerlo.

### Atributos

Los atributos son los datos que "pertenecen" a una entidad. Forman el conjunto de información que tenemos sobre esta.

Los atributos en el mundo real pueden ser infinitos, pero a nosotros normalmente sólo nos interesa un subconjunto de ellos.
### Relaciones

### Categorías

## El modelo de registros

Casi todo lo que hacemos para guardar datos en gestores de bases de datos y también en una computadora en general, está basado o pensado en el modelo de "registros".

Un registro es un conjunto de datos relacionados con una entidad, lo que pensaríamos que es una fila en una tabla de una base de datos, mientras que cada una de las columnas sería un atributo de la entidad.

## Filosofía del conocimiento

Hay varias posturas con respecto a "la realidad". Las dos extremas son:

1. No existe una realidad objetiva, todo es subjetivo, y los seres humanos construyen esta realidad con su mente.
2. Existe una realidad objetiva, y los seres humanos la perciben y la pueden conocer siempre.

En el libro se nos habla sobre una postura intermedia, y que me parece completamente razonable: es que existe una realidad objetiva, pero que los seres humanos **no la pueden conocer completamente**, la accedemos a través de la percepción, pero como en mucha posturas filosóficas, la percepción es imperfecta.

## ¿Qué es un modelo?

De esto ya hemos hablado repetidas veces en este blog, pero vamos a decirlo una vez más: uno modelo es una abstracción, una representación simplificada de la realidad.

Lo que el análisis de este libro nos hace entender es que esa **representación simplificada** tiene más que ver con NUESTRA VISIÓN y NUESTROS INTERESES que con una visión objetiva de la realidad.

## Conclusión

La conclusión más grande que me gustaría sacar de este libro es esta:

**La realidad es compleja, confusa y no tiene los límites que nos imaginamos**. Todo el orden que intentamos poner en nuestros sistemas es en realidad **uno de los múltiples** órdenes posibles que podemos ponerle a la realidad, es un punto de vista, y eso no quiere decir que sea el mejor o el más correcto, o que los demás son incorrectos. La representación de la realidad en los sistemas de información dependerá siempre de para quién lo estemos haciendo, y del uso que se le vaya a dar.

Hablando del dominio de modelado de datos, no hay una distinción clara entre lo que es un atributo, una categoría y una relación, nosotros definimos cuándo un aspecto del mundo real se comporta como uno u otro.

Las entidades, su naturaleza y permanencia, están completamente definidos por el uso que les vayamos a dar.

En resumen: **gran parte de lo que creemos que es una representación objetiva, en realidad es una representación subjetiva y arbitraria**. Pero eso no es malo, es como las cosas funcionan y tenerlo en cuenta nos ayudará a tener discusiones más productivas y a entender mejor los sistemas que construimos.

Algunas representaciones son más útiles que otras desde el punto de vista de otras personas, así que esforzarnos por entender lo que otros están viendo es muy buena idea.

### ¿Qué sigue?

Pensar en todas estas cuestiones te ayudará a notar que no todo lo que tiene que ver con la tecnología y más importante aún: **no siempre hay una respuesta correcta**. Sigue flexibilizando tu pensamiento y abriéndolo, sigue pensando más allá de lo establecido y no te centres en la tecnología.

No seas como el borracho que busca las llaves perdidas bajo el poste porque ahí hay más luz, busca las llaves donde sea más probable encontrarlas.

