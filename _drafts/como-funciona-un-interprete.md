---
title: ¿Cómo funciona un intérprete?
date: 2024-06-20T00:00:00.000Z
author: Héctor Patricio
tags: compiladores intérprete
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
hacer uno, aunque sea muy sencillo.

Emepecemos por hablar de la diferencia con un compilador.

## Intérprete vs compilador

Cuando alguien comienza en las ciencias de la computación, una de las primeras
cosas que escucha es acerca de lenguajes compilados y su diferencia con los
interpretados. Ambos tipos de progrmas tienen la característica de recibir
código fuente, pero la diferencia está en lo que devuelven.

Un **compilador traduce** el código fuente a otro lenguaje, normalmente a un
lenguaje máquina que puede ser ejecutado por un procesador de una arquitectura
específica. Pero esto no es necesariamente así, ya que la principal tarea del  
compilador es **traducir**. Un ejemplo es el compilador de Java:
no compila al lenguaje de una arquitectura de procesador específica, sino a
bytecode que puede ser ejecutado por la JVM. Si no sabes que es el bytecode,
hablamos de él [en este artículo](/2023/01/22/entendiendo-el-bytecode.html).

Un intérprete también recibe el código fuente, pero en lugar de devolver la
traducción en otro lenguaje, **ejecuta** el código fuente directamente. A veces
este proceso tiene como producto secundario la traducción del código fuente
en un lenguaje intermedio, pero su objetivo principal es **la ejecución**.

Ahora sí hablemos de las etapas de un intérplrete.

## Las etapas de un intérprete

Para ejecutar el código de un programa, podemos dividir el tracajo en varios
pasos. El siguiente diagrama muestra las etapas comunes de un intérprete:

Empecemos por la primera etapa que podemos dividir en dos partes.

### Parsing

Esta etapa se encarga de leer el código fuente y convertirlo en una estructura
de datos que pueda ser ejecutada más fácilmente. La primera etapa consiste en
pasar el texto a una secuencia de valores que representan un tipo de palabra
en el lenguaje, llamados comunmente "tokens", de ahí que a este proceso le
llamemos **"tokenización"**.

Después, este conjunto de _tokens_ es convertido en una estructura de datos
llamada el **Árbol de Sintaxis Abstracta** o **AST** (Abstract Syntax Tree).

### Construcción del AST

Ya con los tokens que representan el programa, tenemos que construir la
estructura de datos que representa las operaciones que vamos a ejecutar, **el
AST**.

Esta estructura se parece a un árbol, con cada nodo representando una operación
que a su vez puede estar compuesta de más operaciones, es decir, es una
estructura recursiva. Por ejemplo, si tenemos un programa muy sencillo como
`a = 1 + 2`, el AST podría verse así:

### Ejecució> [!NOTE]
>

Lo que sigue es lo más sencillo de enetender, la ejecución del programa. El
intérprete debe tener la capacidad de actuar sobre el sistema operativo para
ejecutar las operaciones representadas en el AST.

### Opcional: optimización

#### JIT Compilation

Una forma de optimización usada por los intérpretes y máquinas virtuales es lo
que se conoce como **Just In Time Compilation**

## Conclusión
