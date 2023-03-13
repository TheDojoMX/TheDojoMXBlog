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

1. Delimitar precisamente la abstracción
2. Expresar o explicar esa abstracción a otras personas

Y esto **_precisamente_** es lo que necesitamos al programar: delimitar nuestras abstracciones y expresarlas en algún lenguaje de programación, como una tabla en una base de datos o de alguna otra forma que las computadoras puedan capturar y procesar, **a esto es a lo que nos referimos cuando hablamos de abstraer en la programación**.

Lo que hace más difíciles las abstracciones en la programación es que normalmente los conceptos no son tan sencillos e incluso son de áreas con las que no estamos familiarizados o no tenemos experiencia.

La capacidad de abstraer es muy importante en casi todo trabajo intelectual, sobre todo aquellos relacionados con la lógica, por eso es supremamente importante en la programación.

¿Por qué decimos esto? Aquí es donde la programación se parece al trabajo de un matemático: **debes traducir un problema informal de la vida real, normalmente en lenguaje natural a un lenguaje formal que una computadora pueda entender**. Para hacer esto, debes abstraer los aspectos más importantes del problema para representarlos de manera efectiva en tu programa final.

### Ejemplos de abstracciones

Hablemos de algunos ejemplos y cómo caen en las definiciones que hemos hablado.

### Carrito de compras

Cuando queremos representar algo en un carrito de compra en un programa, lo que hacemos es abstraer el concepto de "carrito de compra" y representarlo en el programa.

En la vida real, un carrito o una bolsa de compra es donde almacenamos las cosas que estamos a punto de comprar mientras estamos en la tienda.

La abstracción del carrito de compra, entonces, es un conjunto de productos, cada uno con su precio y cantidad. En el programa, el carrito de compra es una lista de productos que se guarda mientras el usuario no termine de comprar.

En esta abstracción se mantuvieron las propiedades importantes:
para no ir a pagar artículo por artículo, se tiene un contenedor que nos ayuda a mantener lo que vamos a comprar y pagarlo todo de una vez.

La abstracción consiste en que "tiramos fuera" esas propiedades y eliminamos los detalles, por ejemplo si es un carrito, una canasta, una bolsa, un acompañante que carga tus productos, etc.

Aquí entra otra de las características de las abstracciones. Aunque normalmente somos capaces de entender para lo que sirve el carrito de compra, si le preguntas a un cliente común sobre la abstracción, va a ser difícil que la ponga en palabras, por lo que simplemente usamos ese objeto para representar la abstracción en los lugares en los que el usuario lo ve. No le decimos "contenedor de tus productos mientras terminas la compra".

### Abstracción de un usuario

Esta es una de las abstracciones más comunes en los sistemas de software. ¿Qué características esenciales necesitamos de alguna entidad para que use nuestro sistema? Nota que mencionamos "entidad" y no "humano", porque puede que el usuario de nuestro sistema sea otro sistema, por ejemplo.

En sistemas como AWS, GCP y Azure, por ejemplo, existen cuentas para computadoras o para que sean usadas por otro servicio (se llaman _cuentas de servicio_).

Pensando en esto, ¿qué representa a un usuario? Yo me atrevería a decir que los únicos datos absolutamente esenciales para esta abstracción son los que permiten verificar **la identidad**, aquellos que le permiten a la entidad comprobar que en efecto es ella, o en el caso de sistemas, que puede actuar en nombre de ella.

Pensando más ampliamente, la abstracción del usuario tendrá más atributos dependiendo de lo que aplicación haga. Imagínate una aplicación en la que los usuarios sean pacientes clínicos. ¿Qué datos nos interesan de una persona para esta aplicación?

## Niveles de abstracción

Cuando hablamos de abstracción en programación, a veces se escucha el término "nivel de abstracción".
¿A qué se refiere un "nivel"? La siguiente imagen nos puede ayudar a entenderlo:

![Niveles de abstracción](https://i.imgur.com/0Z7Z7Zm.png)

Mientras más cerca esté de la implementación técnica (llegando hasta el hardware), podemos decir que la abstracción está más "abajo". Mientras más cerca esté de los pensamientos o la forma en la que los humanos vemos las cosas cotidianamente, la abstracción está más "arriba".

A esto se refiere la abstracción de bajo nivel y la abstracción de alto nivel. Cuando hacemos un programa, utilizamos una "cadena" de abstracciones, es decir, abstracciones que se sirven de otras abstracciones para funcionar. Usemos de nuevo el carrito de compras como ejemplo.

El carrito es la abstracción de más alto nivel, porque es la que más se acerca al pensamiento cotidiano. Esta se sirve de la abstracción del "contenedor". Pensando en que la implementamos como una lista, la lista es la siguiente abstracción. La lista, dependiendo del lenguaje en el que estemos, se sirve de la abstracción de un arreglo. El arreglo, a su vez, se sirve de la abstracción de la memoria. La memoria usa la abstracción de los bits. Y finalmente los bits son un voltaje presente en un circuito, pero esto a lo que llamamos "voltaje" sigue siendo una abstracción.

Por lo tanto un nivel de abstracción son todas las abstracciones de nuestro programa que están más o menos igual de separadas que el pensamiento humano. Por ejemplo, el carrito de compras, el checkout (terminar y pagar la compra), una biblioteca, un producto, etc. son abstracciones que están al mismo nivel porque son cosas que el usuario puede entender y con las que trata directamente.

Es importante entender los niveles de abstracción porque es buena idea mantener cerrados los niveles de abstracción mientras programas, es decir, no dejar pasar detalles de niveles superiores o inferiores hacia el otro lado de la cadena de abstracción. Por ejemplo, al cliente no le debería afectar si el carrito está implementado como una lista, un arreglo directamente, una tupla o un árbol. Dejar pasar esos detalles afectaría la experiencia del usuario, al mismo tiempo que haría más difícil de mantener el código.

## Dificultades para abstraer

Abstraer no es tan sencillo como ha parecido hasta ahorita. De hecho, si te has dedicado a programar por un tiempo, puede que ya te hayas dado cuenta de eso. La primera dificultad es **la naturaleza de la información**.

No nos vamos a poner a filosofar sobre qué es lo que permite definir algo, para eso te recomiendo el libro [Data and Reality de William Kent](https://www.goodreads.com/en/book/show/1753248), que te romperá la cabeza con respecto a las abstracciones y las diferentes cosas que debes analizar para representar la realidad en una computadora, más concretamente, en una base de datos.

Lo único que quiero sacar de este libro por el momento es: el mundo real, a diferencia del mundo ideal que nos imaginamos, **no tiene límites definidos**, no existen los conceptos tan delimitados y tan claros como los queremos hacer ven en los diccionarios.

Esto nos lleva a que las representaciones (las abstracciones que hacemos en el código) **siempre sean subjetivas y arbitrarias**. No existe **LA ABSTRACCIÓN** que represente la realidad sin fallas, todas ellas tienen un punto de vista y se tienen que adecuar para la función que las crees.

Otra dificultad es lo que hablamos arriba sobre los _niveles de abstracción_. Algo para lo que se usan las abstracciones en la programación es para _ocultar_ información entre componentes del sistema. Crear abstracciones que no revelen detalles no necesarios a veces no es tan sencillos, y se tienen que pensar detenidamente.

## Cómo mejorar tu capacidad de abstraer

Esta es una de las preguntas que todo programador se hace cuando quiere mejorar su manera y velocidad al programar. Cuando hablamos de "la manera" de programar, nos referimos a la calidad del código que produce.

Vamos a hablar de

### Encontrar patrones

Quiero citar a Manuel Rubio en una respuesta que me dio personalmente:

> Estar atento a estos patrones y saber cómo aprovecharlos en nuestro beneficio puede ayudarnos a crear abstracciones del código que desarrollamos. Hay que ser metódico y organizar bien los datos, nombrar las cosas correctamente, mantener las responsabilidades desligadas unas de otras y entonces los patrones se ven claros.

## Evita los extremos

A veces nos pasamos con las abstracciones, tanto en el nivel de abstracción que usamos como en el momento en el que lo hacemos.

## El costo de las abstracciones

Las abstracciones cuestan más que el código que las sustituyen.

### Zero-cost abstractions (Abstracciones sin costo)

Las abstracciones de costo cero son una propuesta de algunos entornos y lenguajes de programación. Como abstraer normalmente supone un costo en el tiempo de ejecución del programa, las abstracciones sin costo proponen que, aunque puedes usar elementos de más alto nivel en el código, no te van a costar rendimiento en tiempo de ejecución.

¿Entonces en dónde cuestan? Normalmente le cuestan al compilador, reemplazar o expandir macros en tiempo de construcción.

## Conclusión

Mejorar tu capacidad de abstraer conceptos, pero sobr e todo de representarlos de manera eficiente en el lenguaje de programación de tu elección te llevará lejos en la carrera de desarrollo de software.
