---
title: "No hagas hagas DevOps por convivir"
date: 2020-09-10
author: "Héctor Patricio"
tags: ['live', 'youtube', 'microservicios', 'java', 'domix', 'hype', 'devops']
description: "En este artículo resumiremos una plática muy interesante que tuvimos con Domingo Suárez sobre DevOps y otras cosas."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1440/v1599714511/1CF0CA4A-211C-4310-9D85-0C49D92B014D_ymceki.jpg"
draft: false
---

Tuvimos una plática con Domingo Suárez([@domix](https://twitter.com/domix)) acerca de diferentes temas que le interesan a los desarrolladores.

En este artículo te vamos a dar un resumen.

## Cómo nos dejamos influir para adoptar una tecnología

Lo primero de lo que hablamos es de la forma en que muchas veces adoptamos la tecnología: **por moda**. A veces es porque alguien con autoridad la mencionó o muchos miembros de la comunidad la están usando. A los desarrolladores nos gustan las cosas _brillantes_.

Generalmente esa decisión tiene un costo bastante alto:

- Te metes en cosas de las que no hay la suficiente información disponible
- Te enfrentas con problemas totalmente desconocidos
- Gastas recursos que podrías gastar mejor en otro lado.

**La lección:** no tienes que aprender y usar todo lo nuevo que sale. Usa tecnología _aburrida_: probada por el tiempo, de la que exista mucha información y usada por muchos desarrolladores de los que podrás aprender rápidamente y enfocarte en los verdaderos problemas que **diferencian** a tu solución.

## ¿Qué es DevOps?

Uno de los temas principales que tratamos es la aclaración de lo que de verdad significa el término **DevOps**.

Domingo explicó que DevOps es una **cultura** que intenta mejorar el flujo de trabajo que existe entre el área de desarrollo y la de operación del software (la encargada de ponerlo en manos de los usuarios y monitorearlo). Intenta **mejorar los hilos organizacionales**.

Nos explicó que el término "DevOps" originalmente era un hashtag de Twitter para hablar de esta cultura en una conferencia organizada por [Patrick Debois](https://blog.newrelic.com/engineering/devops-name/).

Domingo dejó muy claro que **DevOps no es un puesto, ni un rol.** No lo puedes comprar con una herramienta, sino que es una serie de prácticas y **una forma de pensar** que _tu empresa_ debe desarrollar.

Platicamos a además de que DevOps establece _"Las 3 vías"_ que son tres procesos o tres formas en las que la información viaja.

La primera vía consiste en poner el código en producción lo más rápido posible, con opciones como quitarlo rápidamente si no funciona bien (rollback).

La segunda vía es **el monitoreo del software en producción**, para poder actuar rápidamente. Puede ser para mejorarlo, para corregir fallas y para aprender del verdadero uso que los usuarios finales le dan.

La tercer vía es la repetición de estos dos procesos y la ejecución de ejercicios con el objetivo de pulir los procesos y aprender más cosas. Esta vía incluye simulaciones de falla, sesiones de estudio, sesiones de preparación y análisis de fallos, etc.

## Mentores y aprendizaje

Un tema repetido desde el principio es que Domingo tuvo un mentor que se llama **Humberto**.  Una persona que sin darse cuenta le ayudó mucho a adoptar hábitos sanos de aprendizaje y le enseñó muchas cosas directamente.

De esto salió que en la industria de desarrollo de productos digitales **falta en práctica poner más en práctica la mentoría**, ya que nos puede ayudar avanzar y puede a crear personas más hábiles.

Llegamos a una conclusión: **la mentoría es una responsabilidad compartida**. El mentor tiene la responsabilidad de guíar al aprendiz de la mejor forma, porque puede influir de formas muy poderosas en su vida, pero la responsabilidad de aprovechar bien esa guía y aplicar los consejos es de la persona que está siendo mentoreada.

En este punto Alex levantó un punto interesante: en lugares como Silicon Valley, los directivos tienen la idea de que preparar gente dentro de su empresa es beneficioso en general para el ecosistema. Si todos adoptan esa mentalidad, la próxima persona que llegue a tu empresa habrá sido entrenada de la mejor manera, **elvando el nivel de la comunidad**.

Le lección: Aceptar o pedir una mentoría **te hará crecer** y adoptar la idea de que preparar a las personas es beneficioso ayudará a todo el ecosistema.

## Cómo avanzar en tu carrera como desarrollador

Conectado con el tema anterior, hablamos un poco de **cómo puedes volverte mejor desarrollador**, alcanzar un nuevo puesto y obtener un mejor sueldo. La conclusión es:

1. Tienes que mantenerte **siempre aprendiendo** nuevas cosas, no sabes lo que puede servirte más adelante.

2. **No estudies sólo lo relacionado con tu trabajo actual**, estudiar cosas que no tienen nada que ver con lo que haces hoy puede abrirte las puertas a nuevas oportunidades.

3. Haz proyectos de las cosas que estás aprendiendo, no sólo leas o veas videos.

4. Has cosas que de verdad disfrutes.

## Microservicios

La mayoría de las empresas no los necesita, porque aunque quieran imitar a Netflix o Google o Amazon o Facebook, no tienes sus mismos problemas.

Además la arquitectura de microservicios tiene retos a los que tal vez no te quieres enfrentar, como las transacciones distribuidas.

**¿Cuándo es buena idea usar microservicios?** Domingo dio dos criterios:

1. Tu base de usuarios es muy grande, los microservicios te ayudarán a escalar mejor.
2. Tu base de código es muy grande. Así la podrás dividir mejor entre tus _decenas_ de programadores.

## Aprender Java vale la pena

Después, hablamos de qué tanto vale la pena aprender Java en 2020, ya que Domingo es un **Java Champion**, uno de los pocos de México y de LATAM.

La conclusión: **Java es un lenguaje que vale la pena aprender, por ser una tecnología probada (aburrida) y con muchas cosas desarrolladas**.

Algunas de las características que resaltamos de Java:

- La JVM es una pieza de software magnífica que tiene optimizaciones para ser muy eficiente, para ayudarte aunque tu código no sea tan bueno.
- Un montón de lenguajes corren sobre la JVM. Si te gusta más otro que Java puedes combinarlos y compartir lo que ya existe en el ecosistema de Java
- Java como lenguaje ha avanzado mucho, adoptando formas de programar más modernas.
- Sus características intrínsecas, como su compilador y el tipado estático lo hacen ideal para cierto tipo de problemas en los que tienes que reducir al mínimo los errores en tiempo de ejecución.

El consejo de domingo es: Si quieres empezar con Java empieza con algún framework modernos como [Micronaut](https://micronaut.io/).

## Recomendaciones de libros

- [The Phoenix Project](https://amzn.to/3jVxLQu)
- [Site Reliability Engineering](https://landing.google.com/sre/books/)
- [Joel on Software](https://amzn.to/3k2ZTRD)

Disfrutamos mucho de esta plática y esperamos tenerlo con nosotros de nuevo pronto. La puedes ver aquí:

<iframe width="560" height="315" src="https://www.youtube.com/embed/3zQ3qSFDdW0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
