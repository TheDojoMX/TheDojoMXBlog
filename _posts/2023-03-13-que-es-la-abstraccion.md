---
title: "¿Qué es la abstracción?"
date: 2023-03-13
author: Héctor Patricio
tags: abstracción abstracto abstraction
comments: true
excerpt: "Muchos programadores piden consejos para mejorar su capacidad de abstracción. Vamos a hablar de lo que es y cómo se puede usar para programar mejor."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1678168555/shubham-dhage-w06BFh5bRRA-unsplash_xek5go.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1678168555/shubham-dhage-w06BFh5bRRA-unsplash_xek5go.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Gran parte del trabajo que hacemos como desarrolladores de software consiste en "abstraer", pero a veces no entendemos lo que esto significa.

En este artículo vamos a empezar explicando qué es la abstracción en general y luego cómo puedes mejorar tu habilidad de abstraer para programar más rápido y para crear mejores programas. La capacidad de **crear mejores abstracciones te permitirá crear programas que no creías que pudieran existir o que tú pudieras crear**.

Empecemos por las mismísimas bases.

## Etimología: ¿de dónde viene la palabra abstracción?

**"Abstracción"** viene del latín _abstrahere_, que tiene dos partes principales: **abs** que significa "fuera de", "sin", "a distancia" y **trahere** que significa "tirar". La palabra _abstrahere_ significa literalmente "tirar fuera".

La palabra _abstrahere_ se usa en el sentido de "separar" o "extraer" en el contexto de la filosofía, la matemática y la física. En el contexto de las matemáticas, la abstracción es el proceso de separar un concepto de sus propiedades físicas.

A veces entendemos el proceso de abstraer como la capacidad de generalización. Por ejemplo, si queremos abstraer el concepto de "mesa", lo que hacemos es quitar todas las _características concretas_ de todas las mesas que hemos visto en la vida y entonces vemos lo que tienen todas en común: nos permiten hacer algo sobre ellas, sea parados o sentados. De esta manera tenemos el concepto abstracto de una mesa en nuestra mente. Después podemos aplicar ese concepto a diferentes cosas que veamos.

**Los seres humanos somos máquinas de abstraer.** Si a un niño pequeño le presentas unos cuantos gatos o perros, es capaz de aprender el concepto "gato" y extenderlo a otros gatos que vea aunque no se parezcan mucho a los que ya vio. Lo que no es capaz de hacer normalmente, es definir en palabras lo que es un "gato" de manera precisa.

Como **resumen**: abstraer es "tirar fuera", sacar las características que definen algo de su contexto concreto y ser capaz de entender ese concepto de manera general. Esta capacidad nos permite comprender el mundo y movernos en él.

Algunos definen las abstracciones como lo contrario: quitarle todo lo que no es necesario a un concepto para 1) resaltar y hacer **visible** lo que importa y 2) Ocultar detalles que _no deben_ ser tomados en cuenta.

A estas abstracciones a veces las llamamos _**modelos**_. **¿Te suena?**

![Imagen que ilustra la abstracción]()

## Cómo la usamos en la programación

Aunque los seres humanos nos la pasamos abstrayendo todo lo que vemos en la vida real (de hecho, lo único que tenemos en nuestra cabeza son abstracciones), no siempre podemos hacer las siguientes dos cosas:

1. Delimitar **precisamente** la abstracción
2. Expresar o explicar esa abstracción a otras personas, en lenguaje común.

Y esto **_precisamente_** es lo que necesitamos al programar: delimitar nuestras abstracciones y expresarlas en algún lenguaje de programación, como una tabla en una base de datos o de alguna otra forma que las computadoras puedan capturar y procesar, **a esto es a lo que nos referimos cuando hablamos de abstraer en la programación**.

Lo que hace más difíciles las abstracciones en la programación es que normalmente los conceptos no son tan sencillos e incluso son de áreas con las que no estamos familiarizados o no tenemos experiencia.

La capacidad de abstraer es muy importante en casi todo trabajo intelectual, sobre todo aquellos relacionados con la lógica, por eso es supremamente importante en la programación. Aquí es donde la programación se parece al trabajo de un matemático: **debes traducir un problema informal de la vida real, normalmente en lenguaje natural a un lenguaje formal que una computadora pueda entender**. Para hacer esto, debes dejar los aspectos más importantes del problema para representarlos de manera efectiva en tu programa final.

Pero recuerda que las abstracciones en programación también deben _ocultar_ detalles que no _queremos_ que se vean en otras partes del programa, por lo que se incluye una tarea más: refinar estas abstracciones hasta que contengan la información completamente necesaria.

La abstracciones las podemos ver en muchas formas en la programación:

- Modelos de datos
- Tipos de datos
- Clases y objetos
- Funciones
- Clases

Todas estas cosas que mencionamos tienen una característica en común: presentan una **interfaz**. Así estas abstracciones lo pueden ser en dos sentidos:

1. La representación de un concepto de la vida real en el programa
2. El lugar donde se _ocultan_ detalles o información detrás de una interfaz a otra parte del programa

### Ejemplos de abstracciones

Hablemos de algunos ejemplos y cómo caen en las definiciones que hemos hablado.

### Carrito de compras

Cuando queremos representar algo en un carrito de compra en un programa, lo que hacemos es abstraer el concepto de "carrito de compra" y representarlo en el programa.

En la vida real, un carrito o una bolsa de compra es donde almacenamos las cosas que estamos a punto de comprar mientras estamos en la tienda.

La abstracción del carrito de compra, entonces, es un conjunto de productos, cada uno con su precio y cantidad. En el programa, el carrito de compra es una lista de productos que se guarda mientras el usuario no termine de comprar.

En esta abstracción se mantuvieron las propiedades importantes:
para no ir a pagar artículo por artículo, se tiene un contenedor que nos ayuda a mantener lo que vamos a comprar y pagarlo todo de una vez.

La abstracción consiste en que "tiramos fuera" esas propiedades y eliminamos los detalles, por ejemplo si es un carrito, una canasta, una bolsa, un acompañante que carga tus productos, etc.

Aquí entra otra de las características de las abstracciones. Aunque normalmente somos capaces de entender para lo que sirve el carrito de compra, si le preguntas a un cliente común sobre la abstracción, va a ser difícil que la ponga en palabras, por lo que simplemente usamos ese objeto para representar la abstracción para el usuario. No le decimos "contenedor de tus productos mientras terminas la compra" sino simplemente "carrito de compras".

En la segunda forma en la que este carrito de compras puede ser una abstracción es que en tu programa, tal vez hay un clase que representa este contenedor. Para el resto del programa, este carrito tiene una interfaz que podría consistir en:

- Agregar producto
- Obtener total
- Vaciar carrito
- Agregar Cupón
- Obtener total

La manera en que esta clase hace todas esas operaciones debería estar oculta de todo el resto del programa. Incluso la manera en que almacena la información sólo le concierne a esta _abstracción_. Esto permite **ocultar información** y hace que las piezas del programa sean menos dependientes entre ellas.

### Abstracción de un usuario

Esta es una de las abstracciones más comunes en los sistemas de software. ¿Qué características esenciales necesitamos de alguna entidad para que use nuestro sistema? Nota que mencionamos "entidad" y no "humano", porque puede que el usuario de nuestro sistema sea otro sistema, por ejemplo.

En sistemas como AWS, GCP y Azure, por ejemplo, existen cuentas para computadoras o para que sean usadas por otro servicio (se llaman _cuentas de servicio_).

Pensando en esto, ¿qué representa a un usuario? Yo me atrevería a decir que los únicos datos absolutamente esenciales para esta abstracción son los que permiten verificar **la identidad**, aquellos que le permiten a la entidad comprobar que en efecto es ella, o en el caso de sistemas, que puede actuar en nombre de ella.

Pensando más ampliamente, la abstracción del usuario tendrá más atributos dependiendo de lo que aplicación haga. Imagínate una aplicación en la que los usuarios sean pacientes clínicos. ¿Qué datos nos interesan de una persona para esta aplicación?

## Niveles de abstracción

Cuando hablamos de abstracciones en programación, a veces se escucha el término "nivel de abstracción".
¿A qué se refiere un "nivel"? La siguiente imagen nos puede ayudar a entenderlo:

![Niveles de abstracción](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_800/v1678759133/Ilustracio%CC%81n_sin_ti%CC%81tulo_f7ag0e.png){: .align-center}

Mientras más cerca esté de la implementación técnica (llegando hasta el hardware), podemos decir que la abstracción está más "abajo". Mientras más cerca esté de los pensamientos o la forma en la que los humanos vemos las cosas cotidianamente, la abstracción está más "arriba".

A esto se refiere la abstracción de bajo nivel y la abstracción de alto nivel. Cuando hacemos un programa, utilizamos una "cadena" de abstracciones, es decir, abstracciones que se sirven de otras abstracciones para funcionar. Usemos de nuevo el carrito de compras como ejemplo.

El carrito es la abstracción de más alto nivel, porque es la que más se acerca al pensamiento cotidiano. Esta se sirve de la abstracción del "contenedor". Si lo implementamos como una lista, esta es la siguiente abstracción. La lista, dependiendo del lenguaje en el que estemos, puede servirse de la abstracción de un arreglo dinámico. El arreglo, a su vez, se sirve de la abstracción de los bloques y direcciones de memoria. La memoria usa la abstracción de los bits. Y finalmente los bits son un voltaje presente en un circuito, pero esto, a lo que llamamos "voltaje" sigue siendo una abstracción.

Un **nivel de abstracción** está compuesto por todas las abstracciones de nuestro programa que están más o menos igual de separadas de el pensamiento humano. Por ejemplo, el carrito de compras, el checkout (terminar y pagar la compra), una biblioteca, un producto, etc. son abstracciones que están al mismo nivel porque son cosas que el usuario puede entender y con las que trata directamente. Una lista, un cola, un árbol (estructura de datos), una pila, son cosas que están al mismo nivel porque las entendemos como maneras de organizar datos.

## Dificultades para abstraer

Abstraer no es tan sencillo como ha parecido hasta ahorita. Más bien, abstraer es algo que hacemos todo el tiempo, pero crear abstracciones adecuadas y expresarlas correctamente no es tan sencillo. De hecho, si te has dedicado a programar por un tiempo, puede que ya te hayas dado cuenta de eso. La primera dificultad es **la naturaleza de la información**.

No nos vamos a poner a filosofar sobre qué es lo que permite definir algo, para eso te recomiendo el libro [Data and Reality de William Kent](https://www.goodreads.com/en/book/show/1753248), que te romperá la cabeza con respecto a las abstracciones y las diferentes cosas que debes analizar para representar la realidad en una computadora, más concretamente, en una base de datos.

Lo único que quiero sacar de este libro por el momento es: el mundo real, a diferencia del mundo ideal que nos imaginamos, **no tiene límites definidos**, no existen los conceptos tan delimitados y tan claros como los queremos hacer ven en los diccionarios.

Esto nos lleva a que las representaciones (las abstracciones que hacemos en el código) **siempre sean subjetivas y arbitrarias**. No existe **LA ABSTRACCIÓN** que represente la realidad sin fallas, todas ellas tienen un punto de vista y se tienen que adecuar para la función que las necesites. Una misma cosa puede ser representada de millones de maneras diferentes y todas estas maneras pueden ser válidas.

Otra dificultad es lo que hablamos arriba sobre los _niveles de abstracción_. Algo para lo que se usan las abstracciones en la programación es para _ocultar_ información entre componentes del sistema. Crear abstracciones que no revelen detalles no necesarios a veces no es tan sencillo, y se tienen que pensar detenidamente.

Finalmente, la complejidad intrínseca de los elementos que representamos puede ser en sí mismo un gran reto para crear abstracciones convenientes. Por ejemplo, en vez de representar gatos, tenemos que representar un proceso de suministro de insumos para una cadena de producción, la logística compleja de programación de vuelos y asignación de aviones y tripulación para una aerolínea, o el estado de una conversación compleja entre dos entidades.

Es por eso que a veces creemos que necesitamos ayuda para mejorar nuestras capacidades de abstracción.

## Cómo mejorar tu capacidad de abstraer

Esta es una de las preguntas que todo programador se hace cuando quiere mejorar su manera y velocidad al programar. Cuando hablamos de "la manera" de programar, nos referimos a _la calidad_ del código que produce.

Vamos a hablar de las técnicas que puedes seguir para mejorar tu capacidad de crear y _expresar_ mejores abstracciones.

### Consigue información y ejemplos

Ya hemos dicho que los seres humanos somos _muy buenos_ creando abstracciones por naturaleza, pero somos tan buenos que podemos crear abstracciones demasiado temprano cuando entendemos algo bien.

Para evitar las abstracciones tempranas, **consigue la mmayor cantidad de información posible**. Mientras más ejemplos diferentes del mismo fenómeno o entidad tengamos, mejores abstracciones vamos a crear, ya que encontraremos ejemplos que se contradicen entre ellos, excepciones y casos límite (aquellos que están en los valores extremos o combinaciones de características raras).

### Crear niveles de abstracción cerrados

Es importante entender los _niveles de abstracción_ porque esto nos permitirá diseñar abstracciones que no dejen pasar detalles de niveles superiores o inferiores hacia el otro lado de la cadena de abstracción. Por ejemplo, al cliente no le debería afectar si el carrito está implementado como una lista, un arreglo directamente, una tupla o un árbol. Dejar pasar esos detalles afectaría la experiencia del usuario, al mismo tiempo que haría más difícil de mantener el código.

Estos niveles de abstracción se mantienen de dos formas:

1. Creando conjuntos de abstracciones relacionados que tengan el mismo nivel. A esto le llamamos una "capa".
2. Creando interfaces que oculten los detalles de capas superiores o inferiores.

Es muy difícil que este diseño te quede bien a la primera, por lo que debes tener en cuenta que tus interfaces y tus abstracciones irán evolucionando con el tiempo.

### Encontrar patrones

Quiero citar a [**Manuel Rubio**](https://altenwald.com/) en una respuesta que me dio personalmente:

> Estar atento a estos patrones y saber cómo aprovecharlos en nuestro beneficio puede ayudarnos a crear abstracciones del código que desarrollamos. Hay que ser metódico y organizar bien los datos, nombrar las cosas correctamente, mantener las responsabilidades desligadas unas de otras y entonces los patrones se ven claros.

Este consejo está directamente ligado a la cantidad de información que tenemos sobre el problema. Mientras más diversa y rica sea, más probable es que encontremos los patrones que subyacen en los comportamientos y procesos que tenemos que abstraer (o modelar). Aquí lo importante es ser explícitos con esos patrones, expresarlos y documentarlos de la manera más clara posible.

Haber visto y sobre todo documentado una gran cantidad de patrones también nos puede ayudar a diseñar abstracciones de manera más efectiva y rápida en el futuro. Esto es de lo que los **patrones de diseño** se tratan: soluciones comunes a problemas recurrentes. Sólo hay que ser muy cuidadosos de no encajar problemas en patrones que no corresponden completamente al problema, sólo por el hecho de querer salir rápido del problema o de querer aplicar cierto patrón.

### Diseña dos veces

El diseño del software puede hacerse como la escritura: primero escribes y después editas. Son dos etapas diferentes y tan independientes que dos personas diferentes las pueden hacer. El diseño en el software puede hacerse de manera parecida. Primero diseñas tus representaciones y puedes pedirle a alguien que te corrija o revise, o puedes hacerlo tú mismo después de haber dejado pasar un poco de tiempo.

Esta revisión te llevará a pensar cosas como "¿Qué estaba pensando cuando escribí esto?" o "Creo que esta no es la abstracción correcta", gracias a que normalmente te has parado un poco a distancia de tu propio diseño.

## Desarrolla la capacidad de absorber información

Debido a que tienes que representar cosas de dominios en los que probablemente no conoces, tener la capacidad de estudiar de manera efectiva te permitirá analizar la información necesaria para crear buenas abstracciones.

### Expande tu mente

Mientras más cosas sepas de diferentes campos o dominios, será más probable que encuentres cosas que te puedan servir para _entender_ lo que estás tratando de representar y sobre todo para extraer sus componentes principales, así como la información que vale la pena excluir. Así que no te limites en aprender todo lo que puedas de todos los campos posibles, pero recuerda también que esto tiene rendimientos decrecientes: mientras más profundices en un campo, más te costará adquirir nueva información que valga la pena.

Es por esto mismo que muchos programadores son buenos programando para ciertos dominios: financiero, de automatización industrial, de juegos, de programas científicos, etc. No lo podemos saber todo y muchas veces son el conocimiento de una sóla área es suficiente para entretenernos por décadas.

### Practica

Este es el concepto más gastado de todos, pero aquí le vamos a dar un pequeño giro. No sirve de mucho para mejorar sólo hacer abstracciones sin reflexionar en ellas. Tienes que pensar detenidamente en tus diseños y contestar preguntas como:

- ¿Qué información tenía disponible y pasé por alto?
- ¿Cómo hubiera podido conocer u obtener esa información?
- ¿Qué detalles de implementación dejé escapar de mi abstracción?
- ¿Quién pudo haberme dado más ejemplos sobre el problema?
- ¿Quién puede hacer una revisión sobre el diseño y darme comentarios para mejorar?

A esto se le llama práctica enfocada y hay ejercicios llamados [Code Katas](http://codekata.com/) que te pueden ayudar a mejorar en el diseño de software.

¿Tienes algún consejo más que te haya ayudado a mejorar la forma en la que creas abstracciones? Me gustaría escucharlo en los comentarios.

## Evita los extremos

A veces nos pasamos con las abstracciones, tanto en el nivel como en el momento en el que lo hacemos. En esta sección nos referimos exclusivamente a las abstracciones que generalizan un proceso o concepto, y las que ocultan información de otras partes del programa.

Una señal de que estamos abstrayendo demasiado es que haya una gran diferencia entre la dificultad natural del problema base y nuestro código. Por ejemplo, imagina que tienes que encontrar una cadena de texto en un texto más grande. La cadena a encontrar es una de tres posibles "Kilo", "Mega", "Giga". ¿Valdrá la pena hacer la abstracción de un buscador general de cadenas cualquiera en textos arbitrarios con el uso de autómatas finitos deterministas? Lo más probable es que no: con un un simple "contains" o la función equivalente usado en el lugar de la búsqueda es suficiente.

Esto se puede meter directamente con nuestro orgullo: lo fácil o sencillo no nos hace parecer inteligente. Pero recuerda que la simplicidad es la mejor sofisticación. Mientras más simples sean tus diseños, mejor.

El otro punto importante es **cuándo** creamos estas abstracciones. Si quieres crear el programa más complejo desde el principio, lo más probable es que vas a tardar mucho en implementarlo, además de que puede que crees abstracciones que no vas a necesitar. Mejor usa las cosas más concretas posible hasta que de verdad el problema o los requerimientos de los usuarios te hagan generalizar algo. Es cierto que a veces prever algún cambio simplificará tu trabajo en el futuro, pero la mayoría de veces nos equivocamos. Lo hacemos tanto, que existe un inicialismo para refrenarnos de crear abstracciones prematuramente: YAGNI (You aren't gonna need it - No lo vas a necesitar).

## El costo de las abstracciones

Una abstracción del tipo que esconde código de otras partes del programa, es decir, de las que están detrás de una interfaz (Clase, módulo, función, etc), normalmente cuestan más en tiempo de diseño, de compilación o de ejecución. Normalmente en los tres, a menos que sea una abstracción con la que tengas mucha familiaridad. Esta es otra razón para refrenarnos de crear todas las abstracciones que se nos ocurran en un programa, o de crear cadenas de abstracciones demasiado grandes.

Esto lo tienes que pensar sobre todo cuando los beneficios de crear cierta abstracción no están tan claros. Con algunos entornos, hay excepciones.

### Zero-cost abstractions (Abstracciones sin costo)

Las abstracciones de costo cero son una propuesta de algunos entornos y lenguajes de programación modernos. Como abstraer normalmente supone un costo en el tiempo de ejecución del programa, las abstracciones sin costo proponen que, aunque puedes usar elementos de más alto nivel en el código, no te van a costar rendimiento en tiempo de ejecución.

¿Entonces en dónde cuestan? Normalmente le cuestan al compilador, reemplazar o expandir macros en tiempo de construcción. Rust es un ejemplo de esto, aunque estas abstracciones están a bastante bajo nivel (te evitan manejos de memoria que podrían ser complicados, por ejemplo).

## Conclusión

Mejorar tu capacidad de abstraer conceptos, pero sobre todo de representarlos de manera eficiente en el lenguaje de programación de tu elección te llevará lejos en la carrera de desarrollo de software.

Este tema es de los más importantes en las ciencias de la computación y desarrollo de software, así que es algo de lo que puedes seguir aprendiendo a lo largo de toda tu carrera. Algunos documentos que puedes consultar para aprender más son:

1. [Programación y Tecnología: Un camino equivocado hacia la construcción de
artefactos](https://www.docdroid.com/ST0qbY8/programacion-y-tecnologia-un-camino-equivocado-pdf)
2. [Abstraction in Computer Science Education:
An Overview](/assets/pdfs/EJ1329311.pdf)
3. [Abstraction](/assets/pdfs/chap02.pdf)

Espero que este artículo te sirva en tu camino profesional en la carrera de desarrollo de software.
