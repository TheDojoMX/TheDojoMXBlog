---
title: "A Philosophy of Software Design: Desarrollo Táctico vs Estratégico"
date: 2020-02-11
author: Héctor Patricio
tags: a-philosophy-of-software-design complejidad APoSD
comments: true
excerpt: "Dos diferentes formas de desarrollar sistemas de software"
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1600/v1585958798/877DD1C2-5C29-428A-8FEE-BC9685FE108F_ym4tl1.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_200/v1585958798/877DD1C2-5C29-428A-8FEE-BC9685FE108F_ym4tl1.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Cuando desarrollas software tienes dos actitudes para escoger: desarrollas de forma rápida y sucia (desarrollo táctico) o de forma ordenada, planeada y pensando en el futuro. Cada uno de estos tipos de desarrollo o filosofías de desarrollo tiene ventajas y desventajas. Pero veamos a más detalle de qué trata cada uno.

## Desarrollo táctico

Está caracterizado por la alta velocidad inicial con la que empiezas a desarrollar y crear las funciones de tu programa. Con esta actitud, tu principal objetivo es tener _código que funcione_. Con esta forma de trabajo no gastas mucho tiempo buscando el mejor diseño para tu programa sino que te enfocas en terminar lo más rápido posible. Tu vista está en el **corto plazo**.

Con tal de terminar con la tarea lo más pronto posible, no importa si agregas algo de complejidad al sistema.

Este tipo de desarrollo es alentado por los negocios que quieren que su código o programa esté tan pronto como sea posible sin importar el costo. ¿Tiene uso este código y esta forma de pensar? Por supuesto: cuando se quiere construir un producto muy muy rápido y se tiene conciencia de que _será desechable_.

Pero otra cosa que te puede llevar a desarrollar de esta manera es la falta de planeación: estimar en mucho menos tiempo una tarea o malgastar el tiempo que tenías disponible.

El desarrollo táctico produce programas que con el tiempo se van haciendo más y más difíciles de mantener, hasta que es tan impráctico que parece más fácil volver a hacerlo. **La velocidad de desarrollo se va reduciendo.**

Una vez que empiezas a programar un sistema de esta forma, es muy difícil cambiar. Y lo más triste es que la mayoría de las organizaciones y programadores prefieren este método.

Algunos ejemplos de desarrollo táctico:

- Hard-coding de parámetros que deberían ser configurables
- Duplicación innecesaria
- Abstracciones deficientes o complicadas en extremo
- Código difícil de entender
- Manejo de excepciones deficiente(envolver todo en un try/catch, no manejar excepciones)

## Desarrollo Estratégico

Este tipo de desarrollo se caracteriza por poner atención en el diseño y la calidad del código. Lo más importante no es directamente terminar la tarea pendiente, sino también hacerlo de manera que facilite las tareas futuras y mantenga la complejidad bajo control. La tarea principal es _crear un muy buen diseño_.

Para el desarrollo estratégico **código que funciona no es suficiente**. En vez de introducir partes que hagan más complejo el código, buscas mejorar aunque sea una pequeña parte del código cada que trabajas en él.

Esto no quiere decir que harás todo el diseño por adelantado, sino que se va a ir creando un buen diseño de las partes que se vayan necesitando.

Es tener una actitud de inversión en la base de código.

Esta actitud te hará ir más lento al principio, pero con el tiempo el equipo acelerará y podrá crear nuevas funciones muy rápido.

Ejemplos de prácticas desarrollo estratégico:

- Probar varias implementaciones hasta encontrar la más limpia
- Documentar y comentar el código
- Limpiar y mejorar el código cada que sea posible (cada que lo toques)
- Crear pruebas unitarias
- Revisión de código

La siguiente imagen ilustra cómo se comporta el avance total en las dos formas de programar:

![Comparación desarrollo táctico vs estratégico](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_800/v1636240255/Ilustracio%CC%81n_sin_ti%CC%81tulo_6_htdc68.png)


Como se puede ver, el desarrollo estratégico tarda más en entregar resultados, pero vale la pena si es un proyecto importante con un tiempo de vida esperado largo. Puedes pensarlo como la diferencia entre construir una choza o construcción sin ningún tipo de diseño contra una casa bien diseñada y con buenos materiales, como en la historia de los tres cochinitos. ¿Cuál aguantará más?

Muchas veces aquí está la diferencia entre si algo "escala" o "no escala", no en la tecnología elegida. Es obvio que a una choza no le puedes construir un segundo piso.

Pero no seamos puristas y pensemos que si no es de la forma estratégica no vale la pena, la pregunta es: _¿Qué tipo de desarrollo conviene para tu proyecto según su tiempo de vida?_

Este y los siguientes artículos están basados en el libro ["A Philosophy of Software Design"](https://amzn.to/2H92nwA) de John K. Ousterhout.
