---
title: "¿Qué es un engine de JavaScript?"
date: 2020-05-17
author: "Héctor Patricio"
tags: ['js', 'javascript', 'compiladores', 'javascript-engine', 'v8', 'chrome']
description: "Hablemos de qué es y cómo funciona un motor de Javascript."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1589701068/538FF576-00FA-4723-9142-920622E07743_djzuh4.jpg"
draft: false
---

Me llamó mucho la atención  la salida de [Deno v1 esta semana](https://deno.land/v1) y le quise echar un ojito. Pero desde la explicación que da inicialmente, no entiendo _exactamente_ lo que es y hace:

> "Deno is a simple, modern and secure runtime for JavaScript and TypeScript that uses V8 and is built in Rust."

Aquí me surgió la pregunta: ¿Qué es un **runtime** para JavaScript?

Pero para contestarla, antes tengo que entender **qué es V8**. La respuesta es: un _engine_ o _motor_ de JavaScript. En este artículo explicaremos qué es y cómo funciona.

## Explicación rápida

Puedes pensar en un engine o motor de JavaScript como en el programa encargado de correr el código de JavaScript. Todos los navegadores tienen uno:

|Navegador | Engine|
|----------|-------|
|**Chrome** y **Opera** | [V8](https://v8.dev/)|
**Firefox** | [SpiderMonkey](https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey)|
**Safari** | [WebKit JSCore](https://trac.webkit.org/wiki/JavaScriptCore)
**Edge** | [Chakra](https://github.com/microsoft/ChakraCore)|

Este, combinado con el motor web componen la mayor parte de un navegador. Los engines se pueden usar fuera de los navegadores para otras tareas, como en Deno o Node.

> El **motor de JavaScript** es quien convierte tu código de JavaScript en código ejecutable por la máquina en la que va a correr.

## Teoría: Compilación contra Interpretación

Para correr un programa en cualquier lenguaje, hay que convertirlo en instrucciones que las computadoras puedan entender. Esto es el **código máquina**.

Los lenguajes compilados transforman todo el código **antes de ejecutarlo**, por lo que pueden hacer optimizaciones generales para que el programa sea más eficiente.

Para que el programa compile tiene que estar libre de errores. Generalmente esa compilación lleva un poco de tiempo, que va creciendo dependiendo del tamaño y complejidad del programa. Los programas compilados pueden ser más eficientes en ejecución, pero cuesta más empezarlos a correr.

Los lenguajes interpretados van ejecutando **línea por línea**, sentencia por sentencia. Por esto mismo no pueden hacer optimizaciones generales, pero es más fácil y rápido para el programador _empezar_ a ejecutarlos. Normalmente tienen un **REPL** (Read - Eval - Print - Loop) que puede servir para jugar con ellos y hacer pruebas.

Se pude pensar que es _más fácil_ desarrollar en lenguajes interpretados que compilados, por lo que su desarrollo es _más rápido_. Pero como los lenguajes compilados pueden hacer optimizaciones generales, son **más eficientes**.

## La ejecución de JavaScript

JavaScript _nació_ como lenguaje **interpretado**, para correr dentro del navegador Netscape. La idea principal de esto es que no necesitara de un paso de _compilación_ previa, entendida como la generación de un producto intermedio que sea ejecutable.

El encargado de esta "interpretación", es decir, de convertir instrucciones de JavaScript en
instrucciones de la computadora es el _engine o motor_.

Pero los motores modernos de JavaScript están muy optimizados, la ejecución de JS puede a veces compararse con la de lenguajes completamente compilados. Y esto es gracias las optimizaciones de compilación en el momento de la ejecución: _just in time_ o **JIT**.

En resumen: JavaScript dejó de de ser un lenguaje _puramente interpretado_ para convertirse en un lenguaje híbrido, con interpretación y compilado JIT. Se comporta como interpretado cuando un programador lo corre, pero el motor compila el código, produciendo algunas veces un producto intermedio (bytecode) que puede ser optimizado para que las siguientes ejecuciones sean mucho más rápidas.

## Las etapas de un motor de JavaScript

Ls principales etapas son:

1. **Escaneo**. Convierte el texto del código que escribes en _tokens_. Un token es un bloque de carácteres que tienen un significado sintáctico. Ejemplo: `x=33` está compuesto por 3 tokens: Un identificador (`x`), un operador (`=`) y un número (`33`). Puedes irte por el hoyo del conejo si quieres entender como funciona el scanner de V8 aquí: [Blazingly fast parsing](https://v8.dev/blog/scanner)

2. **Parseo**. No encontré la palabra correcta para traducirlo, pero se puede entender como la 'lectura' de un texto que lo transforma en una estructura de datos. Esta fase convierte el conjunto de _tokens_ generados por el scanner en un Árbol de Sintaxis Abstracta (AST - Abstract Sintax Tree). Este árbol representa tu programa sintácticamente y se pasa a la siguiente fase de la compilación.

3. **Interpretación**. En esta fase se toma el AST y se convierte en una primera versión de código que la máquina ya puede ejecutar, _sin optimizaciones_. Genera además código intermedio (bytecode) que puede ser pasado a la siguiente etapa para optimizarlo. En V8 se llama [Ignition](https://medium.com/dailyjs/understanding-v8s-bytecode-317d46c94775)

4. **Optimización**. Esta parte es ejecutada por un compilador JIT, que analiza el código, cómo se comporta, los tipos de datos usados para crear una versión más optimizada en código máquina. Si las optimizaciones fallan, el bytecode sigue siendo ejecutado por el intérprete. En V8 se llama [TurboFan](https://v8.dev/docs/turbofan).

Las últimas dos etapas son donde el código se ejecuta, una en forma de bytecode interpretado y la otra en forma de código máquina **altamente eficiente y optimizado**.

Aquí puedes ver un diagrama de la secuencia de operaciones de V8.

![Ejecución de un script de JavaScript](https://res.cloudinary.com/hectorip/image/upload/v1589700777/1_ZIH_wjqDfZn6NRKsDi9mvA_wc08nl.png)

## Ejecución

Durante la ejecución, el motor de JavaScript debe mantener por lo menos dos cosas:

1. La información de tu programa
2. En qué parte del programa estamos

Esto lo hace mediante dos espacios de memoria organizados específicamente para estas tareas:

1. El **Heap**. Encargado de mantener la información de las variables y todo otro dato ocupado por el programa.
2. El **Stack**. Encargado de llevar un registro de las llamadas a funciones y contextos de ejecución.

Además necesitamos a alguien que libere memoria para que nuestro programa no crezca infinitamente en la memoria y el _heap_ sea fácil de acceder. Esto es el **garbage collector** o _recolector de basura_.

Todo este proceso complejo se explica en mayor profundidad aquí: [Visualizing memory management in V8 Engine](https://deepu.tech/memory-management-in-v8/).

## Conclusión

Esto es lo básico que necesitamos entender de lo que hace un motor de JavaScript, el encargado de ejecutar el código. Pero no es suficiente contar con alguien que pueda correr el código, necesitamos además **algo que nos proporcione el material para trabajar**, ya que los programas en general actúan sobre algo, u obtienen información de algún lado. Esto es el **Runtime**, que explicaremos en el siguiente artículo.
