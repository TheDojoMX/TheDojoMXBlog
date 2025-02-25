---
title: "Zig: un lenguaje que quiere reemplazar al poderoso C"
date: 2024-03-10
author: Héctor Patricio
tags:
comments: true
excerpt: "Escribe aquí un buen resumen de tu artículo"
header:
  overlay_image: #image
  teaser: #image
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Recientemente hemos visto una ola de lenguajes listos para destronar
a los lenguajes de programación que forman la base de casi toda nuestra
computación actual: C y C++. Lenguajes como Rust y Go quieren reemplazarlos,
pero tenemos a otro competidor que apunta directamente hacia C y parece
que se está acercando aunque no tiene todavía una versión completamente estable.

En este artículo vamos a hablar de las características de Zig y cómo es que
planea reemplazar a C.

## Las características de Zig

[Zig](https://ziglang.org/) es actualmente desarrollado por la Zig Software
Foundation, una organización sin fines de lucro que básicamente fue creada para
seguir desarrollando el lenguaje. Pero **Andrew Kelley**, lo empezó en 2015 con
la idea de retar la forma en la que hacemos software.

Kelley es un programador con experiencia en C principalmente y mientras trabajaba en su
proyecto "Genesis Digital Audio Workstation" se decidió para crear Zig.
En sus propias palabras: _"mi meta es crear un lenguaje más pragmático  que C."_

Algunas de las características que presenta en el artículo en el que
habla por primera vez de Zig son:

1. **Pragmatismo**. Ser pragmático es lo mismo que ser práctico. Zig es un lenguaje
   que se enfoca en resolver problemas reales y no en ser un lenguaje teórico.
2. **Seguridad en memoria**
