---
title: "Los diferentes grados de diseño de software"
date: 2024-10-19
author: Héctor Patricio
tags: diseño-de-software arquitectura-de-software
comments: true
excerpt: "Hablemos de los diferente niveles de diseño de software y cómo puedes aprender cada uno de ellos."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,e_oil_paint:30,w_1400/v1725143065/natalia-y-DIewyzpUbRc-unsplash_npwcd3.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,e_oil_paint:30,w_400/v1725143065/natalia-y-DIewyzpUbRc-unsplash_npwcd3.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Hay una confusión enorme sobre el diseño de software. Cuando se habla de arquitectura, se empieza
a hablar de patrones de diseño, infraestructura, y otras cosas con las que no nos conviene
meternos en ese nivel.

Es por eso que en este artículo vamos a proponer una taxonomía para los diferentes grados de diseño
de software. Pero antes hablemos de por qué te conviene hacer una distinción clara.

También presentaremos una serie de recursos que puedes usar más para aprender de cada uno de
estos niveles de abstracción en el diseño de software.

## Por qué te conviene distinguir los grados de diseño de software

Lo primero que debemos entender es que hacer software **implica** diseñar software. Las raíces
de la palabra diseñar son las mismas que las de la palabra designar: las dos cosas tienen que ver
con **decisiones**. Cuando _diseñamos_ entendemos que estamos tomando decisiones y documentándolas
por adelantado. Pero aunque ni las tomemos por adelantado, ni las documentemos, esas decisiones
están ahí y por lo tanto el diseño existe.

Teniendo esto presente, nos conviene ponerle atención al diseño desde el principio, para crear
software que **cumpla tanto con las funciones como con las características que se esperan de él**.

¿Ahora bien, por dónde empezamos a diseñar? Es aquí en donde entran los grados de abstracción
en diseño: conocer el nivel que necesitamos nos ayudará a empezar en el lugar adecuado.

## Los grados de abstracción en diseño de software

Hablemos de cada uno de los grados de abstracción en diseño de software, qué es lo que se espera
y cómo contribuya a la solución final.

### Arquitectura de soluciones

El propósito del software o de cualquier sistema es resolver problemas para un usuario. Estos
sistemas están dentro de un contexto completo que le da sentido a su existencia. Es en este nivel
en donde se define la arquitectura de la solución.

Tomando en cuenta el contexto completo de dónde va a funcionar el software, la organización
o los individuos que lo van a usar, el contexto social, económico e incluso político, se define
la arquitectura de la solución, es decir, se toman en cuenta los componentes principales que van
influir en que el software pueda cumplir con su propósito.

Este nivel de diseño es el más alto relacionado con el software y requiere capacidad técnica, pero
también amplias capacidades a nivel de negocio, administración y otros campos relacionados con
el funcionamiento de las organizaciones.

Lo anterior implica que este nivel es poco específico en cuanto los detalles de la solución,
pero tiene gran impacto tanto en el que software cumpla con lo que se espera de él, como con
conseguir los recursos necesarios para su desarrollo. Además las decisiones que se toman aquí
tienen un gran impacto en los negocios que solicitan el software.

¿Qué tanto debe saber sobre _construcción de software_ un arquitecto de soluciones? Como dijimos,
este nivel requiere poca especificidad técnica, pero gran capacidad para combinar conocimientos
de lo que es posible construir con el software, el contexto del negocio y proyección de los cambios
que el entorno va a sufrir. Este es un rol más amplio que profundo.

Un arquitecto de soluciones debe ser el traductor entre lo que el negocio necesita, tomando en cuenta
el contexto amplio de este, y el tipo de software que se puede construir o adquirir.

#### Recursos para aprender arquitectura de soluciones

En esta sección te presento algunos recursos que te pueden ayudar a aprender sobre este nivel de
abstracción en el diseño de software, pero recuerda que nada sustituye la experiencia práctica:

- [Solution Architecture Foundations](https://www.oreilly.com/library/view/solution-architecture-foundations/9781780175676/). Este libro es una excelente introducción a la arquitectura de soluciones y tiene
un enfoque práctico.

- [An Elegant Puzzle: Systems of Engineering Management](https://press.stripe.com/an-elegant-puzzle). Está escrito
por un ingeniero de software y líder de ingeniería en grandes empresas de software. Este libre es un conjunto de
ensayos sobre la administración de equipos de ingeniería, pero también incluye valiosas lecciones sobre
cómo guiar a una organización en la que su principal activo es el software.

### Arquitectura de software

El siguiente nivel de abstracción es la arquitectura de software. Esta actividad es una de las
más mal entendidas y por lo tanto mal ejecutadas a mi parecer. La arquitectura tiene que ver
con las características que una pieza de software demuestra a nivel estructural, es decir,
cualidades que surgen de la interacción de sus componentes.

Un error muy común al intentar practicar la arquitectura de software es irse demasiado rápido
a los detalles de implementación (si vamos a usar tal o cuál patrón de diseño, etc). Mi propuesta
es que la arquitectura de software se practique en un nivel de abstracción más alto, es decir,
más cerca de las necesidades del negocio.

Por lo tanto, la principal actividad en este nivel es transformar las necesidades del negocio en
características de software. A estas características las llamamos **atributos de estructurales o
de calidad**. Pero la arquitectura de software también se encarga de lograr que el software haga
las cosas que el negocio necesita.

También toma en cuenta la estructura de la organización y su composición para definir _la forma_
en que el software se va a desarrollar.

¿Qué tanto debe saber sobre _construcción de software_ un arquitecto de software? Un arquitecto de
software, según la tradición medieval, es _el constructor principal_. Por lo tanto, debe tener 
una muy amplia experiencia técnica, conocer cómo funcionan la mayoría de los componentes principales
comunes del software, pero también debe tener experiencia tratando con las necesidades del negocio.

Un arquitecto es el principal traductor entre lo que el negocio necesita y _cómo_ se puede
**construir** o **armar** un sistema que cumpla con esas necesidades.

#### Recursos para aprender arquitectura de software

En este apartado hay muchos recursos, los que yo te recomiendo son:

- [Software Architecture in Practice, 4th Edition](https://www.oreilly.com/library/view/software-architecture-in/9780136885979/). Si
tuviera la necesidad de elegir un solo libro para aprender arquitectura de software,
este sería el que recomendaría. Analiza todos los aspectos fundamentales para construir
una arquitectura de software sin centrarse en el conocimiento trivial del que muchos creen que se trata
la arquitectura.

- [Fundamentals of Software Architecture](https://www.oreilly.com/library/view/fundamentals-of-software/9781098175504/).
En este libro encontrarás todas las ideas fundamentales clásicas sobre arquitectura de software, y los
términos que se usan para habla sobre estos temas.

- [Just Enough Software Architecture: A Risk-Driven Approach](https://www.georgefairbanks.com/book/). Aquí
encontrarás un enfoque diferente para la arquitectura de software: el enfocado en los riesgos. Este libro te
ayudará a encontrar el equilibrio al tomar decisiones en tu arquitectura.

### Diseño de sistemas

Una vez que sabemos qué características y funciones debe tener el software y cómo las vamos a lograr
debemos de ponerle nombre y detalles a cada pieza de software. De esto se encarga el diseño de sistemas.

Este, para mi, es el nivel más clásico y conocido en el diseño de software y el que más le emociona
a la mayoría de los desarrolladores. Es aquí donde dices que vas usar tal o cuál base de datos específica,
si vas a usar réplicas de lectura, cómo vas a manejar a un millón de usuarios concurrentes, e incluso
detalles de bajo nivel como el almacenamiento de datos y el tipo de infraestructura que vas a usar.

También es aquí donde muchas de las entrevistas de trabajo se centran cuando se quiere poner a prueba
la capacidad técnica de un desarrollador puro, ya que es un paso intermedio entre la arquitectura, que
tiene que ver mucho con el negocio, y la programación, que es todo lo que haría un desarrollador que a
penas está empezando.

Demostrar habilidad en este nivel es un proxy para entender qué tanto has desarrollado software, pero
tristemente, al igual que todas las medidas que se convierten en el objetivo, ha perdido gran parte
de su capacidad evaluadora ya que se puede simular fácilmente (estudiando los problemas clásicos de
entrevistas).

¿Vale la pena estudiarlo aisladamente? Sí, pero es no es suficiente. Este nivel no se trata de seguir
recetas de diseño de sistemas, aunque se pueda entender así, sino de conocer cómo se implementan las
soluciones arquitectónicas ahora con los detalles de implementación. Así que su verdadero valor viene
de la **experiencia** desarrollando software.

Creo que esta pregunta ya es obvia, pero demos una respuesta explícita al igual que en las otras
secciones: ¿Qué tanto debe saber sobre _construcción de software_ un diseñador de sistemas? Mucho,
y mientras más experiencia real tenga, mejor.

Un diseñador de software lleva la visión arquitectónica dibujada en papel a su forma final, lista
para ser implementada.

#### Recursos para aprender diseño de sistemas

El área de diseño de sistemas es muy amplia y recomiendo mucho estudiarla por partes. Primero,
puedes empezar por los problemas clásicos, usando uno de los libros que te prepara para entrevistas
como referencia, pero después tienes que profundizar:

- [Acing the System Design Interview](https://www.oreilly.com/library/view/acing-the-system/9781633439108/).
Este libro te prepara para las entrevistas de trabajo, tocando todos los temas fundamentales de diseño de
sistemas.

- [System Design Interview – An Insider’s Guide](https://www.oreilly.com/library/view/acing-the-system/9781633439108/). Otro 
libro que te prepara para la entrevista de diseño, pero es un poco más informal que
el anterior. Tiene una segunda parte que puedes encotrar aquí: [System Design Interview - An Insider's Guide: Volume 2](https://amzn.to/3Ysb0ux).

Ahora sí, podemos empezar a profundizar:

- [Designing Data-Intensive Applications](https://dataintensive.net/). Este trata sobre el diseño de sistemas
de alta disponibilidad, escalabilidad y mantenibilidad y que tratan con muchos datos. Analiza cómo se usan
los sistemas que manejan datos para lograrlos y se va a un poco más abajo para que veas cómo están construidos,
así que también te prepara para el nivel de abajo.

- [Building Microservices](https://www.oreilly.com/library/view/building-microservices-2nd/9781492034018/). Una
de las formas más comunes de diseñar sistemas a grana escala es usando microservicios. Aunque no siempre los
vayas a usar, entender los patrones fundamentales y los problemas que resuelven te ayudará a implementar esos
principios en otros contextos.

- [Foundations of Scalable Systems](https://www.oreilly.com/library/view/foundations-of-scalable/9781098106058/).
La escalabilidad es un tema clave en el diseño de sistemas, entender los medios para lograrla te ayudará
a ser un mejor diseñador.

### Diseño de código

Para mi, el siguiente nivel tiene que ver con la **implementación de los diseños**. La pregunta en este
nivel es: ¿Cómo cumplo con las características y funcione que se esperan de esta pieza de software?

Ya dijimos que el software siempre tiene que ver con decisiones, de hecho podríamos decir que una
base de código es un conjunto de decisiones registradas en un lenguaje de programación. Un programador
que quiere cumplir con las funciones y características que se esperan de sus programas hace bien
en tomar decisiones por adelantado y en adoptar un conjunto de prácticas que le ayuden a cumplir
con lo que casi siempre se espera de esos sistemas de software.

En esta parte es donde se aplican los patrones de diseño, los principios de división modular y de
separación modular, donde se eligen nombres y donde se escoge el mejor algoritmo para resolver un problema
específico. El comportamiento alto nivel de los sistemas depende completamente de las decisiones que
se tomen a esta nivel y que se cumpla con lo que se espera de cada uno de los componentes.

Aquí es donde se elige si se usa un bubble sort, un merge sort o un quicksort para ordenar una lista,
si se usa la cierto módulo de terceros para una funcionalidad o si mejor lo implementamos.

La pregunta de las otras secciones no aplica aquí, este nivel es el más técnico y en el que se
está poniendo en práctica todo lo que sabemos de construcción de software.

Un programador, usa el diseño para lograr que cada pieza de software cumpla con lo que se espera de ella.

#### Recursos para aprender diseño de código

En este nivel vamos a encontrar muchos recursos, pero muchos de ellos se contradicen entre sí, por lo que
creo que es fundamental escoger una escuela de pensamiento y seguirla, pero también echarle un vistazo 
a las otras y contrastar los puntos de vista, para que generes tu propio estilo.

A continuación recomiendo mis libros favoritos en este nivel:

- [A Philosophy of Software Design](https://milkov.tech/assets/psd.pdf). Este es mi libro favorito respecto
a diseño de código porque creo que viene de alguien con experiencia y errores reales. Contradice muchos consejos
encontrados en "Clean Code", que es el libro más admirado en este aspecto, pero que creo que ha envejecido muy
mal.

- [Modern Software Engineering](https://www.patkua.com/blog/book-review-modern-software-engineering/). Te presenta
las prácticas más modernas para desarrollar software, igual, escrito por un ingeniero de software con mucha experiencia.

En [este artículo](https://blog.thedojo.mx/2023/05/25/libros-que-todo-desarrollador-de-software-deberia-leer-desarrollo.html) te
recomiendo otros libros que te pueden ayudar a mejorar tu diseño de código.


## Conclusión

En cada nivel de diseño requerimos diferentes tipos de conocimiento y habilidades. Estas cuatro niveles
no son necesariamente niveles secuenciales de desarrollo de carrera. Es decir, un muy buen programador
no tiene por qué aprender a diseñar a nivel de sistemas, por ejemplo, podría dedicarse a cada vez
diseñar mejor componentes individuales o incluso algoritmos específicos. Por ejemplo, los desarrolladores
de drivers o contribuidores individuales en equipos gigantes que se dedican una parte del sistema.

También, si estás implementando software con un objetivo ya definido, es poco probable que necesites aprender
sobre arquitectura de soluciones o arquitectura de software a muy alto nivel, ese aprendizaje sólo
te distraerá del conocimiento que realmente necesitas para resolver el problema.

Y también funciona en la otra dirección. Conocer los detalles de implementación de cierto algoritmo
no te hará un mejor arquitecto de software o de soluciones.

Así que ya sabes, ningún conocimiento es mejor que otro aunque puede que algunos piensen que así sea,
cada uno tiene su lugar y su propósito.
