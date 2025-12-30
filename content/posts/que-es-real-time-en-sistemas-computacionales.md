---
title: "¿Qué es Real Time en sistemas de software?"
date: 2023-12-09
author: "Héctor Patricio"
tags: ['real-time', 'tiempo-real', 'sistemas-críticos']
description: "Hablemos que significa que los sistemas sean Real Time y qué principios puedes seguir para lograr que tu sistema lo sea."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1450/v1696829214/nathan-dumlao-LPRrEJU2GbQ-unsplash_cmhwgx.jpg"
draft: false
---

A veces, los programadores usamos muy libremente los conceptos. Uno de ellos es el de Real Time. En este artículo vamos a hablar de lo que significa realmente el término, lo vamos a definir claramente y sobre todo aprenderemos a diferenciar los distintos niveles o garantías que debe ofrecer un sistema en tiempo real.

## ¿Qué es Real Time?

Un sistema que provee garantías de Tiempo Real o Real Time es aquel que **garantiza** que una tarea se va a ejecutar en un tiempo determinado. Esto es muy importante en sistemas críticos, como los que se usan en la industria automotriz, aeroespacial, médica, en los que ejecutar NO ejecutar una tarea en un tiempo determinado puede tener consecuencias catastróficas.

Pero también hay sistemas en los que es _deseable_ que una tarea se ejecute antes de cierto tiempo, por ejemplo, cuando estamos transmitiendo información en forma de audio o video de algo que es importante que se comunique rápidamente. Así, podemos hacer llamadas o videollamadas que son útiles.

Los dos casos anteriores, nos dan la pauta para por lo menos distinguir dos tipos de sistemas Real Time:

1. **Hard Realtime**. Son sistemas que deben garantizar con un 100% de certeza que la tarea que quieres que hagan se va a realizar _máximo_ en el tiempo qu especifica el mismo sistema. En estos sistemas no hay margen de error, si el sistema no puede cumplir con el tiempo especificado se considera que falló, por lo que no es seguro operarlo. Este tipo de sistemas se usan en ocasiones en las que es muy muy importante que la tarea en cuestión se ejecute lo más rápido posible, normalmente porque el no hacerlo o tener un retraso podría tener consecuencias mortales o catastróficas.

2. **Soft Realtime**. Los sistemas de este tipo, garantizan que _mínimo_ cierto porcentaje de las veces que un sistema se ejecute, la tarea se va a ejecutar en el tiempo especificado, normalmente lo más rápido posible. A diferencia de los sistemas de tiempo real fuerte, puede que cierto número de acciones tarden un poco más de lo esperado, pero esto no llevaría a pensar que el sistema falló. Este tipo de sistemas se usa para cosas no tan críticas pero en las que es deseable que la tarea está lista lo más rápido posible, por ejemplo, en juegos, aplicaciones de videoconferencia, sistemas de coordinación de trabajo (Figma, Google Docs, etc).

## Cómo puedes lograr un sistema Real Time

Lo primero en que debemos pensar es qué tipo de realtime necesitamos. Como te puedes imaginar, lograr un sistema Hard Realtime es mucho más complicado que lograr un sistema Soft Realtime. Esto es porque en el primero, no hay margen de error, mientras que en el segundo, podemos relajarnos un poco.

Algunas sugerencias para lograr sistemas realtime son:

1. **Usa un ecosistema que esté pensado para esto**. Hay lenguajes de programación y plataformas que mediante diferentes técnicas te ayudan a lograr funcionalidades real time, pero normalmente se queden al nivel de aplicaciones de soft realtime. Algunos ejemplos son lenguajes que aprovechan la concurrencia y controlan efectivamente el tiempo de ejecución de tu programa o te permiten hacerlo de manera sencilla, como: Go, Elixir y NodeJS.

2. **Usa un lenguaje de programación que te de control granular sobre el tiempo de ejecución**. Con esto principalmente me refiero a una cosa: que no tengan recolector de basura. Recuerda que este proceso puede parar el programa por un tiempo no conocido y de manera no controlada, por lo que si quieres lograr aplicaciones hard realtime, será una tarea extremadamente difícil. Lamento decírtelo, pero si quieres asegurar que tu programa se comporte como deseas, vas a tener que controlar casi cada detalle, en lenguajes como C, C++ o Rust.

3. **Asegura la fiabilidad de tu infraestructura**. Para que un sistema realtime sea confiable, vas a necesitar que la infraestructura sea resistente a fallas. Esto lo logras eliminando puntos únicos de fallo, es decir, aquellos puntos de tu programa o infraestructura que si fallan hacen que todo el sistema se caiga. Para lograr esto tienes que pensar en arquitecturas distribuidas, redundancia de datos, escalamiento automático, etc.

Espero que estos consejos te sirvan y si se me está pasando alguno, por favor, déjame un comentario.

## Conclusión

Conocer los diferentes niveles de servicio que un sistema puede garantizar y comprender las características que presentan, te puede ayudar a tomar en serio la responsabilidad de diseñar un sistema realtime y la dificultad que implica.

Piensa profundamente si realmente se requiere un sistema con estas características (sobre todo si es hard realtime) y si es así, toma en serio la responsabilidad de diseñarlo y construirlo, espero que los consejos que te di en este artículo te sirvan para lograrlo.
