---
title: "Entendiendo la cohesión y el acoplamiento en el software"
date: 2021-12-05
author: Héctor Patricio
tags: Cohesión acoplamiento software
comments: true
excerpt: "En este artículo intentamos establecer de manera sencilla qué son la cohesión, el acomplamiento y cómo afectan al diseño de tu software y el código"
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1120/v1638804031/adrian-trinkaus-7UCmXtyg1CQ-unsplash_zhc1uk.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_320/v1638804031/adrian-trinkaus-7UCmXtyg1CQ-unsplash_zhc1uk.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Siempre se dice que una buena base de código tiene alta **cohesión**, pero bajo **acoplamiento**. ¿Cómo se puede entender esto? ¿Cómo podemos llevar este principio a la práctica?

En este artículo vamos a definir cada uno de esos términos de manera sencilla, y con ejemplos de cómo llegar a la aplicación real de estos términos.

## Un poco de historia

Estos dos conceptos y otros relacionados fueron desarrollados por [Larry Constantine](https://history.computer.org/pioneers/constantine.html) en la década de los 60's y publicados en los años siguientes, junto con el nacimiento del [diseño estructurado de sistemas](https://www.win.tue.nl/~wstomv/quotes/structured-design.html). Estos conceptos han sido aceptados y han sido objeto de muchos estudios sobre cómo afectan a la calidad del software realmente. Ahora sí empecemos hablando de lo que quisiéramos lograr con nuestro software.

## Cohesión

La **cohesión** de los módulos se refiere al grado en que los componentes de cierto módulo **se relacionan entre sí**. Es decir, un módulo tiene **alta cohesión** si todos, o la mayoría de sus componentes trabajan para un mismo objetivo y no para cosas dispares o no relacionadas.

Una buena cohesión permitirá que el componente _utilice menos otros módulos externos_, ya que la mayoría de lo que requiere para realizar su trabajo está en el mismo módulo.

Para lograr esto, normalmente tienes que reducir las tareas de las que el módulo es responsable al menor grado posible, tratando de seguir el principio de responsabilidad única.

Pongamos un ejemplo: imagina que estás creando un chatbot, un programa que, usando las API's de los aplicaciones de comunicación te permite interactuar con tus usuarios en forma de chat. El sistema tiene como requerimiento que la lógica de conversación sea fácil de reemplazar y mantener. Una buena cohesión se refiere a por ejemplo a que por ejemplo, la lógica de conversación y todo lo necesario para manejarla existe en un sólo módulo. Así mismo con los conectores para la comunicación con cada uno de los sistemas, etc.

Una forma efectiva de entender la cohesión es **"juntar"** todas las partes que tienen que ver con un tema, una abstracción o una decisión de diseño lo más cerca posible, de preferencia en el mismo módulo[^1] o clase.

## Acoplamiento

El **acoplamiento** consiste en el grado de dependencia de las diferentes partes de un sistema entre ellas. La pregunta clave para entender el acoplamiento es: **¿Cuánto se necesita saber de un módulo para entender otro módulo?**

Mientras más necesites saber de **A** para entender **B**, más **A** relacionados, o acoplados están.

Por ejemplo, imagina una aplicación de e-commerce, que consiste de un catálogo, un carrito de compras y la parte del pago. Estos tres elementos pueden estar muy acoplados entre sí, en el sentido de que cualquier cambio en el catálogo afecta al carrito de compras y al pago, o al revés. Si puedes cambiar cualquiera de los tres módulos sin tener que tocar los otros, hay un bajo acoplamiento.

El acoplamiento **ideal sería cero**, pero como te imaginarás esto es imposible.

Los módulos pueden depender entre ellos de diferentes formas, tanto conceptualmente como en implementación. Constantine menciona que los siguientes cuatro factores pueden afectar el grado de acoplamiento de los módulos:

1. Tipo de conexión entre los módulos. ¿Escriben a las mismas variables globales? ¿Uno usa al otro? ¿Uno es la especialización de otro?
2. Complejidad de la interfaz: ¿Qué tan intrincada es la conexión entre los módulos?
3. Tipo de información que pasa entre la conexión: ¿se pasan grandes estructuras de datos que procesan de manera secuencial? O, ¿un módulo modifica la forma de trabajar de otro?
4. Tiempo en el que sucede la conexión: ¿depende uno de que el otro corra para poder ejecutarse?

Tener en cuenta estos factores puede ayudar a reducir el acoplamiento de los módulos.

## Relación entre cohesión y acoplamiento

Constantine menciona que mientras más cohesión tengan los módulos, menos acoplamiento tendrán entre ellos. Esto suena lógico porque mientras más "autocontenido" sea un módulo (más cohesión) menos va a necesitar de otros para poder funcionar.

> "A mayor cohesión de los módulos individuales en el sistema, menor será el acoplamiento" - [Structured Design by Yourdon and Constantine](https://www.win.tue.nl/~wstomv/quotes/structured-design.htm)

Como podrás ver, no son medidas independientes, sino correlacionadas en la práctica.

## Cómo lograr alta cohesión y bajo acoplamiento

La principal forma de lograr esta buena estructura es dedicando tiempo al diseño del software,prestando especial atención a la forma en la que se modulariza el sistema, es decir, la forma en la que se divide el problemas en otros más pequeños.

_Constantine y Yourdon_ afirman que la única forma de lograr esto es con práctica, práctica y más práctica.

## Conclusiones

El principio de "Alta cohesión y bajo acoplamiento" sin duda es útil para que nuestro software sea más claro, más fácil de mantener y de cambiar. No hay manera de aprender cómo dividir el sistema en módulos si no es mediante la práctica de diseño e implementación de sistemas reales. Así que, ya sabes, **manos a la obra**.

[^1]: Cuando decimos "módulo" estamos hablando de la forma de tu lenguaje de agrupar funcionalidades, puede ser literalmente un módulo, un paquete, una aplicación etc.