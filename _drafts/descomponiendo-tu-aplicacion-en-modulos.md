---
title: "Descomponiendo tu aplicación en módulos"
date: 2023-03-18
author: Héctor Patricio
tags: módulos diseño arquitectura
comments: true
excerpt: "La tarea principal de un desarrollador de software es "
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1679205046/javier-miranda-3yQY9GPM8Mg-unsplash_nkacdz.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1679205046/javier-miranda-3yQY9GPM8Mg-unsplash_nkacdz.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Hay un dicho que tiene que ver con la guerra que es un gran consejo para crear gran software:

> Divide y vencerás

Dividir un problema para resolverlo por partes tiene muchas ventajas, en este artículo vamos a hablar de ellas, así como de las técnicas y los criterios que puedes seguir para hacerlo efectivamente. Específicamente, en este artículo vamos a hablar de cómo dividir la aplicación en módulos. Pero antes definamos lo que es un módulo.

## ¿Qué es un módulo?

En este artículo los módulos son cualquier cosa que encapsule una implementación detrás de una API o interfaz. Los módulos tienen diferentes nombres dependiendo del lenguaje de programación, pueden ser:

- Paquetes en Python
- Módulos en JavaScript
- Clases y paquetes en Java
- Bibliotecas en C
- Aplicaciones en Erlang o Elixir

Esta lista no es para nada exhaustiva, pero comunica la idea de lo que es un módulo conceptualmente.

### Ventajas de dividir tu aplicación en módulos

¿Qué es más sencillo? ¿Dar subir 100 escalones de 15cm o dar un salto de 15m? Humanamente ni siquiera es posible dar un salto de 15m, por lo que tenemos que recurrir a usar las escaleras.

Lo mismo sucede intelectualmente, la mayoría de los problemas que resolvemos en programación son más grandes de lo que puede caber en nuestra mente en un tiempo determinado. Es por esto que tenemos que descomponer los problemas en partes más pequeñas.

La modularización a parte te permite cambiar el sistema de forma más sencilla, mientras respetes la interfaz entre los módulos (su API), puedes cambiar el módulo que resuelve cierta parte del problema sin afectar el sistema entero.

Finalmente, crear módulos lo más independientes posible te permite reutilizarlos en otros sistemas, lo que llamamos reutilización de código. Dependiendo de tu entorno de programación estos módulos pueden ser paquetes, bibliotecas, aplicaciones, o un incluso puedes construir un framework.

### Desventajas

Al igual que si pudiéramos mágicamente dar un salto de 15m nos evitaría construir unas escaleras, con todo lo que ello implica, el uso de módulos en tu aplicación agregar algo más de complejidad.

En primero, se requiere una infraestructura para que los módulos puedan comunicarse entre sí. Si los módulos son construcciones naturales de tus sistema de programación, entonces sólo tienes que preocuparte por usarla bien y crear interfaces convenientes.

## Criterios para dividir tu aplicación en módulos

Esto en realidad es una exploración de las diferentes formas en las que tu aplicación podría estar dividida y las abstracciones que creas.

Además, dividir en módulos introduce el riesgo de crear complejidad adicional debida a las dependencias entre los módulos.

## Recursos para aprender más

El artículo en el que está basado este artículo es ["On the Criteria to be Used in Decomposing Systems into Modules"](https://www.win.tue.nl/~wstomv/edu/2ip30/references/criteria_for_modularization.pdf).

Otro recurso del que tal vez ya estés harto de escuchar si lees este blog es [A Philosophy of Software Design](https://www.amazon.com/Philosophy-Software-Design-John-Ousterhout/dp/1732102201).

## Conclusión

Descomponer tus aplicaciones en módulos es algo esencial en el desarrollo de software. Pensarlo un poco antes de hacerlo nos dará una gran ventaja para crear software de mejor calidad, que sea más fácil de mantener y que podamos evolucionar mejor.
