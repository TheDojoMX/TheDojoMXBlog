---
title: ¿Cómo funciona un intérprete?
date: 2024-06-20T00:00:00.000Z
author: Héctor Patricio
tags: null
comments: true
excerpt: Escribe aquí un buen resumen de tu artículo
header:
  overlay_image: null
  teaser: null
  overlay_filter: 'rgba(0, 0, 0, 0.5)'
---
Un intérprete es un programa que lee código fuente y se encarga de
ejecutarlo. En este artículo vamos a hablar de sus etapas y las principales
tareas que realiza, para darte la idea de cómo funciona y puedas hacer uno
aunque sea muy sencillo.

Emepecemos por hablar de la diferencia con un compilador.

## Intérprete vs compilador

Cuando alguien comienza en las ciencias de la compilación, una de las primeras
cosas que escucha es acerca de lenguajes compilados y su diferencia con los
interpretados. Ambos tipos de progrmas tienen la característica de recibir
código fuente, pero la diferencia está en lo que devuelven.

Un **compilador traduce** el código fuente a otro lenguaje, normalmente a un
lenguaje máquina que puede ser ejecutado por un procesador de una arquitectura
específica. Pero esto no es necesariamente así, ya que un compilador traduce entre
cualquier lenguaje de entrada y de salida, como es el caso del compulador de Java
que no compila al lenguaje de una arquitectura de procesador específica, sino a
bytecode que puede ser ejecutado por la JVM. Si no sabes que es el bytecode, hablamos de
él [en este artículo](/2023/01/22/entendiendo-el-bytecode.html).

## Las etapas de un intérprete

Como un intérprete trata directamente con el código fuente así que
es leerlo para transformalo en un formato ejecutable. Entonces,


