---
title: "Pilares fundamentales de las ciencias de la computación"
date: 2023-05-19
author: Héctor Patricio
tags: computer-science cs ciencias-de-la-computación
comments: true
excerpt: "Siempre que se habla de ciencias de la computación se habla de complejidad, algoritmos, etc. Pero hay cosas más importantes que tenemos que comprender."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1684557119/IMG_3866_xtomdi.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1684557119/IMG_3866_xtomdi.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Entender la computación **profundamente** es importante para cualquier desarrollador de software, porque al avanzar en su carrera se encontrará con problemas relacionados con las principios más fundamentales de la computación. Piensa en los siguientes casos:

- ¿Es mejor mantener este sistema como un monolito o dividirlo en _microservicios_?
- ¿Cómo puedo hacer que este sistema sea más **rápido**?
- ¿Cómo puedo hacer mi base de código más **mantenible**?
- ¿Cómo puedo **representar mejor** este problema en código?
- ¿Cómo puedo **asegurar el mayor tiempo de actividad** posible en el sistema?
- ¿Puedo **garantizar** que los mensajes que envío lleguen a su destino?
- ¿Cómo evito que la **complejidad** de esta base de código crezca más de lo que la voy a poder controlar?

Tener herramientas para entender estos problemas evitará que te estanques o frustres, y te habilitará para crear sistemas que cumplan con lo se necesita de ellos. Además, te hará un miembro más valioso de cualquier organización.

Un conocimiento sólido de cómo funciona la computación te ayudará por lo menos en los siguientes puntos:

 . Entender los entender los **límites** de lo que se puede hacer
 . Diseñar mejor software (y hardware si se necesita)
 . Trasladar mejor los problemas del mundo real a algo que la computadora pueda entender
 . Explicar en palabras comunes tus ideas
 . Descomponer los problemas computacionales en sus componentes básicos
 . Disfrutar más de tu trabajo

Entender la computación profundamente incluye "_mejorar tu lógica de programación_", un objetivo que muchos quieren lograr para obtener un nuevo puesto o trabajar en la empresa de sus sueños.

En este artículo vamos a hablar de los seis aspectos que tienes que entender acerca de la computación, digamos que son sus **principios fundamentales**. Además veremos cómo se relaciona esto con las cosas comunes que oímos acerca de las ciencias de la computación: complejidad, algoritmos, estructuras de datos, etc.

Pero antes definamos qué es la **computación**.

## ¿Qué es la Computación?

Aquí vamos a hablar de la computación como la **disciplina de usar las computadoras y el software** para lograr nuestros objetivos, sean estos científicos, de negocios, de entretenimiento, etc.

Estos objetivos pueden ser tan arbitrarios y diversos como lo es la cantidad de personas que actualmente usan las computadoras para sus propios objetivos.

La computación se puede ver desde tres perspectivas diferentes:

> It has been argued that there are three particularly lucid traditions in computer science: the theoretical tradition, the empirical tradition, and the engineering tradition. - **Peter Denning**

Según esto podemos ver la computación desde tres perspectivas:

- La tradición teórica: ver la computación como una ciencia
- La tradición empírica: ver la computación en la práctica
- La tradición de la ingeniería: ver la computación como una herramienta

Con tradición, el Denning se refiere a la forma en la que se ha desarrollado históricamente el área. Cada una de estas tradiciones ha desarrollado el área de una forma diferente, pero todas son importantes para entender la computación. Para que seamos profesionales completos, debemos entender lo suficiente de cada una de las áreas.

## Los límites de la computación

Algunas personas piensan que todo es posible dentro de una computadora. Sin embargo, "The Great Principles of Computing" nos dice que:

> Computing is governed by scientific principles and laws that tell us what computers can and cannot do. - **Peter Denning**

Que podemos traducir como:

> La computación **está gobernada por principios** y leyes científicas que nos dicen qué pueden y qué no pueden hacer las computadoras. - Peter Denning

Así que las computación tiene límites y estos están dictados por los principios científicos que conocemos de otras áreas como la física y las matemáticas.

> The computer is the tool but not the object of study. - **Peter Denning**

Aunque nos hemos dividido en áreas de dominios como:

. Inteligencia artificial
. Sistemas distribuidos
. Computación en la nube
. Tratamiento y análisis de datos
. Seguridad informática
. Muchas más y siguen apareciendo

Todas estas áreas que tienen que ver con la computación **obedecen a los mismos principios de los que hablaremos** en este artículo.

## Historia y nacimiento de la computación moderna

Aunque la computación en sí misma es mucho más que las computadoras que usamos, es importante entender cómo llegamos a este punto y junto con eso, las limitaciones que esto nos ha creado, así como las oportunidades que tenemos.

Entender esta historia no te dará súper poderes de programación, pero te ayudará a saber donde estás parado en el flujo del tiempo.

Este contexto te dará más bases para buscar por diferentes lados.

## Modelos de computación

Un modelo de computación es una forma de representar una  mediante un sistema matemático. Esto nos permite analizar el problema y encontrar soluciones.

## Comunicación

Gran parte de la computación tiene que ver con transmitir datos entre diferentes partes que ejecutan los cálculos, pueden ser diferentes computadoras o diferentes ejecutores de una misma computadora. También puede incluir mover información entre diferentes lugares de almacenamiento.

Asegurarnos de que la información llegue a su destino consistentemente y sin errores (o poder detectarlos y corregirlos) es uno de los problemas que la computación tiene que resolver. Esto es especialmente importante en los sistemas distribuidos.

## Cálculos o Computación

En este "cristal" queremos entender que es lo que puede ser calculado o resuelto usando una computadora. Esto incluye conocer la complejidad de las soluciones y en general, si es posible resolver el problema, en qué tiempo y en **qué medios de cómputo**.

Para esto se necesita un poco de matemáticas, pero además creatividad e inventiva, ya que hay que pensar en las diferentes formas en las que un algoritmo se puede comportar. Además, hay que saber notar y demostrar cuando un problema no tiene solución, o las soluciones que existen no son factibles.

## Coordinación

No es siempre cierto que _"el orden de los factores no altera el producto"_. Además, para aprovechar el poder completo de un sistema, normalmente se necesita coordinar las diferentes partes que lo componen. Esto es cierto sobre todo con los sistemas de cómputo actuales, pero además con los sistemas de software que ocupan muchas computadoras.

La coordinación tiene que ver con la concurrencia, el paralelismo y la forma de compartir datos y ponerse de acuerdo entre múltiples ejecutores para realizar una tarea de forma correcta.

## Recolección

¿Cómo conseguimos los datos para procesar? ¿O cómo recogemos los resultados de la computación? ¿Cómo los almacenamos y acomodamos? Esto es la recolección de datos.

## Diseño

No sólo se trata de echar código, también hay que pensarlo bien antes de ponerlo. El tiempo gastado en el diseño de un sistemas puede pagar dividendos grandes en el futuro.

## Más recursos

En  este blog tenemos un post dedicado a los libros que te pueden servir para aprender más acerca de las ciencias de la computación: [Libros para aprender ciencias de la computación](https://blog.thedojo.mx/2023/05/13/libros-que-todo-desarrollador-de-software-deberia-leer-cs.html).

También puedes visitar la página [Teach Yourself Computer Science](https://teachyourselfcs.com/), que tiene una lista de los temas que debes aprender y los recursos que puedes usar para aprenderlos.

## Conclusión

Aprender ciencias de la computación es algo que todo desarrollador debe **aprender en su carrera**. Te puede ayudar a ser más eficiente, a disfrutar mucho más de tu trabajo y resolver problemas que antes no creías posibles. Pero como acabas de ver, es un camino largo, que requiere de bastante esfuerzo sostenido.

Sigue aprendiendo y verás cómo cada cosa nueva que le sumes a tus bases de conocimiento te ayudará a ser un **mejor profesional**.

## Referencias

A continuación algunas de las fuentes usadas para este artículo:

- The Great Principles of Computing, Peter Denning y Craig Martell
- Teach Yourself Computer Science, https://teachyourselfcs.com/
- Concrethe Mathematics, Ronald L. Graham, Donald E. Knuth y Oren Patashnik
- The Art of Computer Programming, Donald E. Knuth