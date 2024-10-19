---
title: "Los diferentes grados de diseño de software"
date: 2024-10-18
author: Héctor Patricio
tags: diseño-de-software arquitectura-de-software
comments: true
excerpt: "Escribe aquí un buen resumen de tu artículo"
header:
  overlay_image: #image
  teaser: #image
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Hay una confusión enorme sobre el diseño de software. Cuando se habla de arquitectura, se empieza
a hablar de patrones de diseño, infraestructura, y otras cosas con las que no nos conviene
meternos en ese nivel.

Es por eso que en este artículo vamos a proponer una taxonomía para los diferentes grados de diseño
de software. Pero antes hablemos de por qué te conviene hacer una distinción clara.

Finalmente, presentaremos una serie de recursos que puedes usar más para aprender de cada uno de
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

Empecemos por el nivel más alto de abstracción la **arquitectura del negocio o de la solución**.

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
