---
title: ¿Cómo funciona un intérprete?
date: 2024-06-20
author: Héctor Patricio
tags: compiladores intérprete lenguajes-de-programación
comments: true
excerpt: "Hablemos brevemente de las etapas de una de las formas de correr tu código: un intérprete."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1721878999/daniele-levis-pelusi-FLEZ4rYjP0w-unsplash_auzjkk.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1721878999/daniele-levis-pelusi-FLEZ4rYjP0w-unsplash_auzjkk.jpg
  overlay_filter: 'rgba(0, 0, 0, 0.5)'
---

Un intérprete es un programa que lee código fuente y se encarga de
ejecutarlo. En este artículo vamos a hablar de sus etapas y las principales
tareas que realiza, para darte la idea de cómo funciona y si lo deseas, puedas
tener idea de cómo hacerlo tu mismo.

Empecemos por hablar de la diferencia con un compilador.

## Intérprete vs compilador

Ambos tipos de programas tienen la característica de recibir
código fuente, pero la diferencia está en lo que devuelven, y por lo tanto
en las etapas que les permiten lograrlo.

**Un compilador traduce** el código fuente a otro lenguaje, normalmente a un
lenguaje máquina que puede ser ejecutado por un procesador de una arquitectura
específica. Pero esto no es necesariamente así, ya que la principal tarea del  
compilador es **traducir**. Un ejemplo es el compilador de Java:
no compila al lenguaje de una arquitectura de procesador específica, sino a
bytecode que puede ser ejecutado por la JVM. Si no sabes que es el bytecode,
hablamos de él [en este artículo](/2023/01/22/entendiendo-el-bytecode.html).

Los compiladores tradicionales compilan el código fuente a código máquina,
es decir, a las instrucciones que un procesador puede ejecutar directamente. Así,
si quieres ejecutar un programa de C o de C++ en un procesador con arquitectura
x86, necesitas un compilador traduzca para las instrucciones de esta arquitectura.
Si después requieres ese mismo programa para ARM, necesitas compilar de nuevo.

Un intérprete también recibe el código fuente, pero en lugar de devolver la
traducción en otro lenguaje, **ejecuta** el código fuente directamente. A veces
este proceso tiene como producto secundario la traducción del código fuente
en un lenguaje intermedio, pero su objetivo principal es **la ejecución**.

Ahora sí hablemos de las etapas de un intérprete.

## Las etapas de un intérprete

Para ejecutar el código de un programa, podemos dividir el trabajo en varios
pasos. Para entenderlo pongamos un ejemplo. Supongamos que alguien te pide
que hagas una tarea, por ejemplo, un trabajo escolar. Si tú fueras el intérprete,
tendrías que hacer más o menos los siguientes pasos:

1. Leer las instrucciones de la tarea.
2. Entender claramente y sin ambigüedades lo que se te pide.
3. Crear un plan para ejecutar la tarea.
4. Ejecutar uno a uno los pasos del plan.

Esos son los pasos que un intérprete hace para ejecutar un programa.

1. **Tokenización**: Leer el código en fuente y transformarlo en una forma
que pueda entender.
2. **Parsing**: Convertir el código fuente en una estructura de datos que pueda
ser ejecutada. En nuestro plan esto serían los pasos 2 y 3.
3. **Ejecución**: Ejecutar uno a uno los pasos del plan para lograr el resultado.

### Parsing o Parseo - Análisis léxico y sintáctico

A veces a la etapa completa de leer el código fuente y convertirlo en una
estructura de datos que pueda ser ejecutada se le llama **Parsing**.

¿Cómo puede un programa informático leer un programa y entenderlo? Lo hace de forma
limitada, claro, pero lo suficiente para poder ejecutar el código. Un lenguaje
de programación es un lenguaje creado a partir de un alfabeto (un conjunto de símbolos),
que a su vez forman palabras y estas palabras forman sentencias. Un **programa**, por
lo tanto, es una secuencia de sentencias.

Para que un intérprete "entienda" un programa, la primera etapa consiste en
convertir el código fuente (un conjunto de símbolos), en una secuencia de
palabras conocidas por el intérprete. Esto es un tipo de clasificación de
las palabras. A la representación interna de estas palabras en el intérprete
se le llama **tokens**. Debido a que en un lenguaje es muy importante el orden
de las palabras, esta clasificación debe mantener el orden de las palabras. Como te
imaginarás, este proceso es al que se le llama **tokenización**.

Después de tener la lista de palabras conocidas, necesitamos "entenderlas". Como un
lenguaje tiene una estructura, esta estructura.

Después, este conjunto de _tokens_ es convertido en una estructura de datos
llamada el **Árbol de Sintaxis Abstracta** o **AST** (Abstract Syntax Tree). Este
proceso se llama **parsing**, que en inglés significa "analizar".

### Construcción del AST

Ya con la lista ordenada de tokens que representan el programa, tenemos que construir la
estructura de datos que representa las operaciones que vamos a ejecutar, **el
AST**.

Esta estructura se parece a un árbol, con cada nodo representando una operación
que a su vez puede estar compuesta de más operaciones, es una
estructura recursiva. Por ejemplo, si tenemos un programa muy sencillo como
`a = 1 + 2`, el AST podría verse así:

![AST de a = 1 + 2](https://res.cloudinary.com/hectorip/image/upload/c_scale,q_69,w_600/v1727416535/Screenshot_2024-09-26_at_23.54.41_spehcz.png)

### Ejecución

Lo que sigue es lo más sencillo de entender, la ejecución del programa. El
intérprete debe tener la capacidad de actuar sobre el sistema operativo para
ejecutar las operaciones representadas en el AST.

### Opcional: optimización

Los intérpretes modernos tienen que se usan en entornos de producción se

#### JIT Compilation

Una forma de optimización usada por los intérpretes y máquinas virtuales es lo
que se conoce como **Just In Time Compilation**

## Conclusión

Ahora entiendes mejor cómo funcionan los intérpretes de manera general. Este
conocimiento te puede ayudar cuando trabajes con ellos y probablemente tengas
algún problema directamente relacionado con su funcionamiento interno.

También tienes el conocimiento básico para avanzar a aprender cómo hacer el tuyo
en caso de que lo necesites.
