---
title: "Compilación Just in Time: qué es y cuándo te conviene"
date: 2023-01-09
author: Héctor Patricio
tags:
comments: true
excerpt: "¿Has escuchado que varios lenguajes están agregando la capacidad de compilación Just In Time a sus entornos? Hablemos de qué es y cómo te beneficia."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_crop,h_450,w_1024/v1673577537/DALL_E_2023-01-12_20.38.31_-_a_mechanical_brain_in_the_back_of_a_robot_s_head_made_as_a__membrane__that_is_a_complex_machine_made_of_very_tiny_gears_levers_and_other_mechanical_dexwfs.png
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_crop,h_450,w_1024/v1673577537/DALL_E_2023-01-12_20.38.31_-_a_mechanical_brain_in_the_back_of_a_robot_s_head_made_as_a__membrane__that_is_a_complex_machine_made_of_very_tiny_gears_levers_and_other_mechanical_dexwfs.png
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Los lenguajes de programación y los compiladores son de las cosas más interesantes en el desarrollo de software. Hace tiempo ha empezado a sonar más comúnmente un término: **JIT** o compilación **Just In Time**, ya que varios lenguajes lo han integrado a sus entornos de ejecución.

Sin embargo, es poco entendida, en este artículo hablaremos de por qué es algo tan sonado y usado. Primero empecemos hablando de la compilación en general y después entendamos este tipo especial de ejecución.

## ¿Qué es compilar?

Compilar es **traducir de un lenguaje a otro**. Lo que entendemos como lenguajes compilados generalmente son lenguajes que traducen de un lenguaje de programación a un lenguaje de máquina, es decir, a código binario que puede ser ejecutado por un procesador en algunos casos o a código para una máquina virtual.

A veces usamos el término "traspilación" (_transpilation_ en inglés), que se entiende como una forma de traducir o transformar de un lenguaje entendido por los humanos (de alto nivel a veces se les llama) a otro del mismo nivel. Por ejemplo de TypeScript a JavaScript. Esto no es más que otra forma de compilación.

### Historia de la compilación

En el libro ["Historia de los lenguajes de programación"](https://altenwald.com/historia-de-los-lenguajes-de-programacion) de [Manuel Rubio](https://mobile.twitter.com/mronerlang), se nos cuenta cómo la compilación nació. Al principio los programadores hacían todo lo que su programa necesitaba desde cero. Una programadora muy experimentada y que estuvo desde los comienzos, **Grace Hopper**, empezó a juntar código que hacía tareas que se repetían vez tras vez y simplemente lo insertaba donde necesitaba esa tarea.

Después, se dio cuenta que podía hacer un programa que hiciera lo mismo que ella hacía, pero que lo hiciera de manera más rápida y eficiente. Así nació el primer compilador, se llama **compilador** y no "traductor" porque más allá de simplemente pasar de un lenguaje a otro, junta (compila) todas las piezas de código invocadas en el programa original y las pone en el programa resultante.

Es interesante pensar que cuando **Grace** tuvo la idea de crear un programa que hiciera esto, muchos se opusieron diciendo que no era posible que una computadora se programara a sí misma y que aunque lo hiciera, los programas nunca iban a ser tan buenos como los que podía hacer un programador humano.

## Compilación por adelantado

La compilación tradicional, conocida en inglés como "ahead of time" (AOT), o en español la llamaríamos "por adelantado", es la que se ha usado desde hace mucho tiempo. En esta compilación, el código fuente se traduce a código final antes de que el programa sea ejecutado. Esto como siempre, tiene ventajas y desventajas.

## Compilación "Just in Time" (JIT)

La compilación "Just in time", que significa "justo a tiempo" (en realidad, español me gustaría llamarla compilación retardada), más que un proceso de traducción se trata de **optimización**.

## Ejemplo con V8

JavaScript y el popular motor V8 creado por Google, es uno de ejemplo birllate del uso de compilación en el momento.

## Otros lenguajes que la usan

Julia
Ruby
Lua
JavaScript

## poner historia de JIT?

[Lars Bak]() desarrolló V8 y también participó en la creación de y de JAVA. [Dart](https://dart.dev/), un lenguaje de programación que se ejecuta en la máquina virtual de Google, [Dart VM](https://dart.dev/tools/dart-vm). En una entrevista, [Lars Bak](https://www.youtube.com/watch?v=5q6X0Z9Z1Zs) habla de cómo se desarrolló V8 y cómo se creó Dart.
