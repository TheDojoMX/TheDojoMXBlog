---
title: "Qué es la compilación Just In Time (JIT)"
date: 2023-01-18
author: Héctor Patricio
tags: jit compiladores compilers compilación just-in-time
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

Compilar es **traducir de un lenguaje a otro**. Lo que entendemos como lenguajes compilados generalmente son lenguajes que se  traducen de un lenguaje de programación a un lenguaje de máquina, es decir, a código binario que puede ser ejecutado por un procesador en algunos casos o a código para una máquina virtual (aquí a veces se llama _código de bytes_ o _bytecode_).

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

La compilación "Just in time", que significa literalmente "justo a tiempo" (en español me gustaría llamarla compilación bajo demanda), más que un proceso de traducción se trata de **optimización**.

Esta compilación sucede solamente en lenguajes que usan una representación intermedia antes de que el procesador los ejecute. Esta representación intermedia normalmente es un [bytecode](https://www.techopedia.com/definition/3760/bytecode). El bytecode puede ser ejecutado por una máquina virtual o intérprete. El compilador JIT transforma este bytecode en código máquina directamente para acelerar su ejecución.

### Funcionamiento de un compilador bajo demanda

Para optimizar la ejecución mientras está sucediendo el compilador JIT tiene que hacer por lo menos tres cosas:

1. **Observar** la ejecución y el código para _identificar_ partes que se beneficiarían de compilar su código a código máquina. Por ejemplo, código que se ejecuta muchas veces o que se lleva la mayor parte del tiempo de ejecución. A esta etapa se le llama _profiling_.

2. **Compilar el bytecode** en código máquina y _optimizarlo_.

3. Como puede que esta compilación no sea tan buena como el bytecode original, el compilador debe **regresar** el bytecode original si la ejecución no mejora.

## Ejemplo con V8

El motor de JavaScript V8 creado por Google, es un ejemplo brillante del uso de compilación bajo demanda.

En el artículo ["Qué es un Engine de JavaScript"](/2020/05/17/que-es-un-engine-de-javascript.html) explicamos el funcionamiento con más detalle. Pero en este diagrama puedes ver las partes principales:

![diagrama de funcionamiento de V8](https://res.cloudinary.com/hectorip/image/upload/v1589700777/1_ZIH_wjqDfZn6NRKsDi9mvA_wc08nl.png){: .align-center}

Después de la lectura del código fuente y la transformación en una estructura que ya puede ser ejecutada (el Abstract Syntax Tree), el código se ejecuta en el intérprete.

El intérprete, llamado **Ignition** genera además el bytecode que más adelante será compilado por el compilador **TurboFan** en caso de que sea conveniente. TurboFan recibe las métricas de uso del bytecode (recogidas por Ignition), es decir, los resultados del profiling y basado en eso decide qué compilará a código máquina. Después de compilarlo y observar su funcionamiento (si mejoró la velocidad y se mantuvo la estabilidad) del código, V8 decide si lo mantiene o si regresa al bytecode original. Esta es la línea roja que vemos en el diagrama, cuando algo se "des-optimiza".

Y esto es básicamente el funcionamiento de un compilador bajo demanda. La observación del código en acción y la mejora en el mismo momento.

## Otros lenguajes que la usan

Las primeras instancias de compilación bajo demanda (también llamada compilación dinámica) se vieron desde los años 60, en Lisp y más adelante con Smalltalk y Self. En este documento puedes ver una historia corta de la compilación bajo demanda y los lenguajes que lo han usado: [A Brief History of Just-In-Time](http://eecs.ucf.edu/~dcm/Teaching/COT4810-Spring2011/Literature/JustInTimeCompilation.pdf)

El lenguaje que popularizó el término JIT fue Java con su máquina virtual [HotSpot](https://www.oracle.com/java/technologies/whitepaper.html) creada en Sun Microsystems y ahora poseída por Oracle. Esta máquina virtual se caracterizó por el desempeño que logra. [Lars Bak](https://dblp.org/pid/30/2083.html) participó en el desaarrollo de HotSpot, V8 y recientemente en el de la máquina virtual de [Dart](https://dart.dev/). Como te puedes imaginar, Dart también usa compilación bajo demanda. [Lua](https://luajit.org/luajit.html) también tie su compilador JIT. Y finalmente, [C#](https://www.telerik.com/blogs/understanding-net-just-in-time-compilation), al ser un competidor directo de Java, tiene usar JIT para ser por lo menos tan rápido como su este.

Los lenguajes que recientemente han agregado JIT a su máquina virtual o intérprete son:

- Ruby con [YJIT](https://www.infoworld.com/article/3647999/ruby-31-arrives-with-new-jit-compiler.html)
- PHP desde su versión 8: [PHP 8.0](https://php.watch/versions/8.0/JIT)
- Erlang desde su versión 24: [Erlang 24](https://www.erlang.org/blog/a-first-look-at-the-jit/)

Como puedes ver, tanto lenguajes compilados como interpretados usan JIT. El único requisito es que el lenguaje utilice un código intermedio.

## Desventajas

Como te imaginarás, no todo es miel sobre hojuelas. La compilación bajo demanda tiene algunas desventajas:

- Al ser un proceso de compilación dinámica, abre la puerta a algunas vulnerabilidades de seguridad, por ejemplo el [JIT Spraying](https://conference.hitb.org/hitbsecconf2010ams/materials/D1T2%20-%20Alexey%20Sintsov%20-%20JIT%20Spray%20Attacks%20and%20Advanced%20Shellcode.pdf)

- El compilador JIT compite con el intérprete por el uso de la CPU. Esto puede afectar el rendimiento del programa.

- El consumo de recursos en general es mayor.

- Puede que la forma en la que está hecha tu programa no se beneficie en absoluto de la compilación bajo demanda, por lo que incluso a veces es posible apagarlos.

Si estás en un entorno en el que algo de esto sea muy importante, considera si el entorno en el que estás trabajando puede dessactivarse el JIT. V8, por ejemplo, puede funcionar sin JIT: [JIT-less V8](https://v8.dev/blog/jitless).

## Conclusión

La compilación bajo demanda ha sido un gran avance en el desarrollo de software, y es un trabajo de ingeniería muy interesante.

Permite que la ejecución de nuestros programas sea más eficiente y rápida.  Además, a mi punto de ver, es una maravilla de la ingeniería de software. Si quieres aprender más: puedes visitar el [sitio oficial de V8](https://v8.dev/), en el que explican muchas cosas acerca del desarrollo de este sistema pionero en compilación bajo demanda.

También puedes ver como funciona un compilador por adelantado todavía más antiguo y muy interesante: [Java HotSpot VM](https://developers.redhat.com/articles/2021/06/23/how-jit-compiler-boosts-java-performance-openjdk#deoptimization_and_speculation).
