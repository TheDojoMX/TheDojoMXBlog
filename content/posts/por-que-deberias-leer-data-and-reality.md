---
title: "¿Por qué deberías leer Data and Reality?"
date: 2023-05-06
author: "Héctor Patricio"
tags: ['libros', 'modelado-de-datos', 'filosofía', 'desarrollo-de-software', 'data-and-reality']
description: "Hablemos de Data and Reality, un libro que te ayudará a ser mejor desarrollador de software, porque se va a las raíces de los problemas que resolvemos a diario."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1682777065/ilgmyzin-GHazVhDDPZs-unsplash_poxzc5.jpg"
draft: false
---

Gran parte de nuestro trabajo como desarrolladores consiste en **modelar entidades** del mundo real en el código, transformarlas, guardarlas y recuperarlas. Estas entidades se pasan entre diferentes procesos para producir un resultado. A veces también nos tenemos que inventar entidades para representar conceptos abstractos que no existen físicamente.

**Modelar datos** es una de las habilidades **fundamentales** cuando estamos desarrollando.Cuando estás programando un algoritmo, estás modelando un _procedimiento_ de la vida real en código. Este proceso normalmente incluye **datos**, que son representaciones de _entidades_ del mundo real.

Por lo anterior, cualquier cosa que puedas aprender sobre modelado de datos, te ayudará directamente en tu carrera como desarrollador. En este artículo hablaremos de un libro muy especial que te puede ayudar a ser mejor en esta área, independientemente del nivel en el que te encuentres en tu carrera. Y si después de leerlo lo meditas más profundamente, puede que te ayude a desarrollar una forma de pensar más adecuada a los problemas que queremos resolver en la actualidad.

**Data and Reality** trata sobre modelado de datos, escrito po William Kent, alguien con mucha experiencia en el tema. El libro tiene tres ediciones la primera es de 1978, la segunda (una actualización) es de 2000 y la tercera, después que Kent murió, es de 2012.

La mejor de todas es segunda edición, ya que la tercera se podría considerar un libro completamente diferente, recortado y con comentarios de [Steve Hoberman](https://technicspub.com/steve-hoberman/), otro modelador de datos pero siento que con un enfoque bastante diferente al de Kent.

Hablemos de los temas principales del libro y por qué te conviene leerlo. Pero antes, veamos algo de lo que se habla en el prefacio de la edición de 2012 que me parece muy relevante.

## Buscando las respuestas donde parece más sencillo

Hay muchas cosas difíciles de resolver en el desarrollo de software y parece que siempre estamos buscando la respuesta en el lugar que parece más obvio o en el que es más fácil buscar, en lugar de donde es más probable que encontremos las respuestas.

El ejemplo que utilizan en el libro para explicarlo y que me parece acertado es una broma acerca de un borracho que pierde sus llaves y se la pasa toda la noche buscando bajo una farola. Cuando alguien le pregunta por qué no busca en otro lado, **el borracho responde que es porque AHÍ HAY MÁS LUZ.**

En el desarrollo de software podría parecer que a veces hacemos exactamente lo mismo. Para buscar la solución a un problema siempre nos vamos a los mismos lados porque es donde nos sentimos cómodos o porque **SIEMPRE SE HA BUSCADO AHÍ**. Por ejemplo, nos centramos en la tecnología, en las plataformas o en los lenguajes. Pero es muy probable que el problema no esté ahí, sino en lugares más profundos.

Es por eso que este libro se enfoca en cuestiones profundas del modelado de datos. No en los lugares comunes, ni siquiera en hablar de cómo hacerlo, sino en preguntas que te llevaran a pensar cosas de las que se habla poco y que probablemente modifiquen tu visión del mundo y tu forma de trabajar **permanentemente**.

La intención de este artículo es dejarte con más dudas, pero llevarte a lugares en los que tal ve no habías estado antes, tal como avanzar a un nuevo lugar en el mapa en un juego de video.

## Cuestiones principales

Hablemos de los conceptos principales de representación de información en los sistemas electrónicos.

### Entidades

Cuando guardamos cosas en una base de datos o las representamos en código, casi siempre nos referimos a ellas como **entidades**.

Por eso el libro empieza cuestionando, **¿qué es una entidad?**

La primera respuesta es que una entidad "es un **_estado_** de la mente". **¿Cómo?** Está bastante rara esa definición. Esta frase significa que una **entidad** más allá de algo que exista en la **realidad** como algo identificable e indivisible, algo que tiene límites fijos, es algo a lo que nosotros le damos significado, y que nosotros delimitamos o entendemos en ciertos contextos. Esta delimitación normalmente no es singular, tiene que ser compartida por un grupo de personas para que tenga sentido.

Pongamos algunos ejemplos para entender eso. La leyenda del barco de **Teseo** relata que cuando él regresó de Creta, donde había matado al Minotauro, el pueblo de Atenas le rindió honores y conservó su barco en lo alto de una colina como un monumento para recordar su hazaña.

Con el tiempo, el barco se fue deteriorando y se le fueron cambiando las partes, hasta que ya no quedó ninguna parte original.

La pregunta es: ¿sigue siendo el _"Barco de Teseo"_? ¿Es el mismo barco si no tiene ninguna parte original? ¿Es el mismo barco si se le cambia una sola parte, o muy pocas?

Esta historia sirve para ilustrar que las entidades como objetos inmutables y permanentes no existen en la vida real, sino que son cosas que en nuestra mente delimitamos y que, junto con otras personas, les asignamos una identidad y un significado. El _"Barco de Teseo"_ sigue siendo el mismo mientras nosotros lo consideremos así.

Exactamente así se comportan las entidades que como desarrolladores modelamos en nuestros programas. No son cosas permanentes, a veces ni siquiera cosas completamente definidas, sino que nosotros les asignamos límites y **significado**.

Las personas, los objetos e incluso los conceptos están en constante evolución y parte de nuestro trabajo es capturar esa evolución en nuestros sistemas.

## Identidad y cambio

Cuando queremos registrar algo en una computadora, normalmente necesitamos una forma de referirnos a ese registro para después poder recuperarlo. Esto que usamos para referirnos a las entidades se llama **identificador**.

Un identificador es un elemento inmutable y único entre todas las entidades de nuestro sistemas. Aquí nos podemos encontrar con varios casos:

- La entidad no tiene nada único por lo que podamos referirnos a ella (elementos que se repiten, por ejemplo libros producidos en serie)
- El conjunto de todos los _atributos_ de la entidad puede constituir una identidad
- Las entidades tienen varios atributos únicos y hay que escoger uno

Pensar en la naturaleza de nuestro problema, en los términos de arriba nos puede llevar a la solución de seleccionar un elemento identificador. Piensa en el primer caso, por ejemplo: cuando algo no tiene identificador natural, tendemos a asignar un identificador único arbitrario a la entidad cuando la metemos en el sistema.

Por ejemplo, es un práctica muy común asignar identificadores numéricos incrementales. La primera entidad registrada del tipo es la 1, la segunda es la 2, etc. También se pueden usar los UUIDs, que son identificadores únicos generados aleatoriamente, y que por lo general evitan problemas como el de permitir que alguien adivine el identificador de otra entidad.

Pero si la entidad tiene un identificador único inmutable, ¿por qué no usarlo? **¿Puede ser una solución más _natural_?**

¿Qué pasa cuando lo que creíamos inmutable cambia? Eso es algo que normalmente rompe lo que hicimos y tenemos que idear formas de componerlo. Todo este tipo de preguntas pensadas por adelantado te pueden llevar a crear sistemas de software que soporten mejor el paso del tiempo y te den menos problemas cuando estén funcionando en producción.


## Relaciones

Will Kent afirma que las relaciones son el tejido de la información que representamos en nuestros sistemas. Se puede entender una relación como una asociación o una conexión entre mínimo dos entidades.

Las relaciones tienen varias características que las pueden definir:

- Grado: El número de entidades de diferentes tipos que participan en la relación
- Dominios: El conjunto de valores que son válidos en cada lado de la relación
- Rol: El papel que juega cada entidad en la relación
- Complejidad (cardinalidad): el número de entidades de cada tipo que participan en la relación

Aquí en las relaciones y su representación empezan a surgir diferentes preguntas y problemas ya de definición, por ejmplo: ¿cómo identificas una relación? Algunas relaciones sólo son significativas con un contexto, ¿cómo lo representas? ¿Deberían ser las relaciones entidades también?

Sin duda, leer este capítulo del libro te ayudará a plantearte todas estas cuestiones y a entender mejor cómo representar la información en tus sistemas.

### Atributos

Los atributos son los datos que "pertenecen" a una entidad. Forman el conjunto de información que tenemos sobre esta.

Los atributos en el mundo real pueden ser infinitos, pero a nosotros normalmente sólo nos interesa un subconjunto de ellos. Data and Reality propone que los atributos son un conjunto de tres elementos:

- El sujeto, la entidad a la que pertenece el atributo
- El objeto, el valor del atributo
- La _relación_, que es por lo que el sujeto y el objeto están conectados

Supongamos por ejemplo el atributo `nombre` de una persona. "Él se llama Héctor": El sujeto es la persona a la que nos estamos refiriendo, el objeto es el nombre "Héctor" y la relación es el hecho de que la persona se llama así.

Si puedes ver, esto nos empieza a meter en problemas de definición. Son realmente los atributos, ¿relaciones?

## Símbolos y valores

Otra cosa que hay que aprender a distinguir cuando estamos modelando entidades y registrándolas es la diferencia entre el valor y el **símbolo**. Cuando ponemos un valor para representarlo en una computadora usamos una representación, esto es el símbolo. El valor es la entidad que estamos representando.

Por ejemplo, hablando de atributos podemos querer expresar la altura de una persona. Esta altura se puede expresar como "172cm", "1.72m", "5'8''", `172` (como entero) etc. Todos estos son símbolos que representan el valor de la altura de la persona. Lo que en realidad queremos expresar es la distancia que existe entre dos puntos.

## Categorías

Cuando guardamos información en los sistemas informáticos normalmente queremos organizarla. Las categorías son una forma de hacerlo, y la manera intuitiva de entenderlo parece suficiente.

Sin embargo, la creación de categorías es algo que también se debe pensar muy bien, ya que esto repercutirá en la forma en que guardamos información y en cómo la recuperamos.

Algunos de los problemas en los que tienes que pensar:

- ¿Qué pasa cuando una entidad puede pertenecer a más de una categoría?
- ¿Qué clasificación es más conveniente para el problema que estás resolviendo?

Las respuestas a estas preguntas son completamente arbitrarias y finalmente dependen del problema y del campo para el que estés programando.
## Filosofía del conocimiento

Finalicemos este resumen hablando de la cosa más profunda o analítica que el libro trata: la naturaleza del conocimiento mismo. Hay varias posturas con respecto a "la realidad". Las dos extremas son:

1. No existe una realidad objetiva, todo es subjetivo, y los seres humanos construyen esta realidad con su mente.
2. Existe una realidad objetiva, y los seres humanos la perciben y la pueden conocer siempre.

En el libro se habla sobre una postura intermedia, y que me parece completamente razonable: es que existe una realidad objetiva, pero que los seres humanos **no la pueden conocer completamente**, la accedemos a través de la percepción, pero como en mucha posturas filosóficas, la percepción es imperfecta.

### ¿Qué es un modelo?

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
