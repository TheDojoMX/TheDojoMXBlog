---
title: "Compilación Just in Time: qué es y cuándo te conviene"
date: 2023-01-09
author: Héctor Patricio
tags: jit compiladores compilers
comments: true
excerpt: "¿Has escuchado que varios lenguajes están agregando la capacidad de compilación Just In Time a sus entornos? Hablemos de qué es y cómo te beneficia."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_crop,h_450,w_1024/v1673577537/DALL_E_2023-01-12_20.38.31_-_a_mechanical_brain_in_the_back_of_a_robot_s_head_made_as_a__membrane__that_is_a_complex_machine_made_of_very_tiny_gears_levers_and_other_mechanical_dexwfs.png
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_crop,h_450,w_1024/v1673577537/DALL_E_2023-01-12_20.38.31_-_a_mechanical_brain_in_the_back_of_a_robot_s_head_made_as_a__membrane__that_is_a_complex_machine_made_of_very_tiny_gears_levers_and_other_mechanical_dexwfs.png
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Los lenguajes de programación y los compiladores son de las cosas más interesantes en el desarrollo   de software. Hace tiempo ha empezado a sonar más un término: **JIT** o compilación **Just In Time**, ya que varios lenguajes lo han integrado a sus entornos de ejecución, aquí la llamaremos "compilación bajo demanda" (gracias a Manuel Rubio por la sugerencia). Durante el artículo entenderás por qué creemos que esta traducción es adecuada.

Este tipo de compilación es poco entendida, por eso en este artículo hablaremos de por qué es algo tan usado. Primero empecemos hablando de la compilación en general y después entendamos este **_tipo especial de ejecución_**. Pero empecemos desde las bases.

## ¿Qué es compilar?

Compilar es **traducir de un lenguaje a otro**. Lo que entendemos como lenguajes compilados generalmente son lenguajes que se  traducen de un lenguaje de programación a un lenguaje de máquina, es decir, a código binario que puede ser ejecutado por un procesador en algunos casos o a código para una máquina virtual (aquí a veces se llama código de bytes o _bytecode_).

A veces usamos el término _"transpilación"_ (_transpilation_ en inglés), que se entiende como una forma de traducir o transformar de un lenguaje entendido por los humanos a otro del mismo nivel. Por ejemplo de TypeScript a JavaScript. Esto no es más que otra forma de compilación. Hablemos de cómo surgió la compilación.

### Historia de la compilación

En el capítulo 9 del libro ["Historia de los lenguajes de programación"](https://altenwald.com/historia-de-los-lenguajes-de-programacion) de [Manuel Rubio](https://mobile.twoitter.com/mronerlang), se nos cuenta cómo la compilación nació. Al principio los programadores escribían todo lo que su programa necesitaba desde cero. Una programadora muy experimentada y que estuvo desde los comienzos de la programación, **Grace Hopper**, empezó a juntar código que hacía tareas que se repetían vez tras vez y simplemente lo insertaba donde necesitaba esa tarea.

Después, se dio cuenta que podía hacer un programa que hiciera lo mismo que ella hacía manualmente, pero que lo hiciera de manera más rápida y eficiente. Así nació el primer compilador" [**el A-0**](https://www.computinghistory.org.uk/det/5487/Grace-Hopper-completes-the-A-0-Compiler/).

Se llama **compilador** (Hopper acuñó el término) y no "traductor" porque más allá de simplemente pasar de un lenguaje a otro, junta (compila) todas las piezas de código invocadas en el programa original y las pone en el programa resultante. El programa original para el A-0 consistía en códigos numéricos que indicaban la subrutina a usar seguidos de los datos a introducir en cada una.

Es interesante pensar que cuando **Grace** tuvo la idea de crear un programa que hiciera esto, muchos se opusieron diciendo que no era posible que una computadora se programara a sí misma y que aunque lo hiciera, los programas nunca iban a ser tan buenos como los que podía hacer un programador humano.

A partir de ahí, se fueron creando compiladores más avanzados y la comunidad al poco tiempo se dio cuenta de que el ahorro de tiempo era muy conveniente para todos, aunque con una pequeña penalización en el desempeño del programa final.

### Compilación por adelantado

La compilación tradicional, conocida en inglés como _"ahead of time"_ (AOT), que en español la llamaríamos **"compilación adelantada"**, es la que se ha usado desde el principio de la programación. En este tipo compilación, el código fuente se traduce a código final que se ejecutará por un CPU o por una máquina virtual. El código puede ser el código binario o bytecode.

Gran parte de lo que hacen los compiladores actuales hacen a parte de traducir es optimizar el código, con el objetivo de que el programa sea lo más eficiente posible en ejecución.

## Compilación "Just in Time" (JIT)

La compilación "Just in time", que significa literalmente "justo a tiempo" (en realidad, español me gustaría llamarla compilación bajo demanda), más que un proceso de traducción se trata de **optimización**.

## Ejemplo con V8

JavaScript y el popular motor V8 creado por Google, es uno de ejemplo brillante del uso de compilación en el momento.

## Otros lenguajes que la usan

Erlang
Julia
Ruby
Lua
JavaScript

## Historia de JIT

Las primeras instancias de compilación bajo demanda (también llamada compilación dinámica)

[Lars Bak](https://dblp.org/pid/30/2083.html) desarrolló V8 y también participó en la creación de y de JAVA. [Dart](https://dart.dev/), un lenguaje de programación que se ejecuta en la máquina virtual de Google, [Dart VM](https://dart.dev/tools/dart-vm). En una entrevista, [Lars Bak](https://www.youtube.com/watch?v=5q6X0Z9Z1Zs) habla de cómo se desarrolló V8 y cómo se creó Dart.

## Conclusión

La compilación bajo demanda ha sido un gran avance en el desarrollo de software. Permite que la ejecución de nuestros programas sea más eficiente y rápida. Además, a mi punto de ver, es una maravilla de la ingeniería de software. Si quieres aprender más: puedes visitar el [sitio oficial de V8](https://v8.dev/), en el que explican muchas cosas acerca del desarrollo de este sistema pionero en compilación bajo demanda.

También puedes ver como funciona un compilador por adelantado todavía más antiguo y muy interesante: [Java HotSpot VM](https://developers.redhat.com/articles/2021/06/23/how-jit-compiler-boosts-java-performance-openjdk#deoptimization_and_speculation).
