---
title: "Compilación Just in Time: qué es y cuándo te conviene"
date: 2023-01-09
author: Héctor Patricio
tags:
comments: true
excerpt: "¿Has escuchado que varios lenguajes están agregando la capacidad de compilación Just In Time a sus entornos? Hablemos de qué es y cómo te beneficia."
header:
  overlay_image: #image
  teaser: #image
  overlay_filter: rgba(0, 0, 0, 0.5)
---
<!-- Introducción -->

## ¿Qué es compilar?

Compilar es un traducir de un lenguaje a otro. Lo que entendemos como lenguajes compilados generalmente son lenguajes que traducen de un lenguaje de programación a un lenguaje de máquina, es decir, a código binario que puede ser ejecutado por un procesador en algunos casos o a código para una máquina virtual.

A veces usamos el término "transpilación" (transpilation), que se entiende como una forma de traducir o transformar de un lenguaje entendido por los humanos (de alto nivel a veces se les llama) a otro. Por ejemplo de TypeScript a JavaScript. Esto no es más que otra forma de compilación.

### Historia de la compilación

En el libro "Historia de los lenguajes de programación" de Manuel Rubio, se nos cuenta cómo la compilación nació. Al principio los programadores hacían todo lo que su programa necesitaba desde cero. Una programadora muy experimenta y que estuvo desde los comienzos, Grace Hopper, empezó a juntar código que hacía tareas que se repetían vez tras vez y simplemente lo insertaba donde necesitaba esa tarea.

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

Lars Bak desarrolló V8.
