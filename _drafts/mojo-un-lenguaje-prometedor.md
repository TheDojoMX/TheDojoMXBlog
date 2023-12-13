---
title: "Mojo 🔥: un lenguaje prometedor"
date: 2023-11-01
author: Héctor Patricio
tags: mojo python machine-learning
comments: true
excerpt: "El ecosistema de desarrollo está cambiando y se están diseñando nuevos lenguajes de programación y entornos de ejecución más adecuados para los problemas actuales. Hablemos de Mojo."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1702275251/shubham-dhage-cLhjmsyby3Q-unsplash_ucy8y3.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1702275251/shubham-dhage-cLhjmsyby3Q-unsplash_ucy8y3.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

[Chris Lattner](https://www.nondot.org/sabre/){:target="_blank"}, uno de los creadores de [LLVM](https://llvm.org) y [Swift](https://www.swift.org/), ha estado desarrollando un nuevo lenguaje basado en la sintaxis de **Python** pero pensado para atacar su punto más débil: **la velocidad de ejecución**.

Este lenguaje se llama [Mojo](https://modular.com/mojo), y está siendo publicitado como un lenguaje para hacer aplicaciones de **inteligencia artificial**. Como ya dijimos, su enfoque principal está en ser un lenguaje que produzca programar eficientes, por lo que puede ser usado para cualquier aplicación que requiera alto rendimiento o hacer una gran cantidad de cálculos, justo como las aplicaciones de _machine learning_.

En este artículo veremos el motivo detrás de su nacimiento, sus características y analizaremos si te conviene aprenderlo o deberías buscar alguna otra alternativa. Primero, entendamos la fundación de Mojo.

## MLIR - Representación intermedia multi-capa

LLVM es un proyecto que se define como infraestructura para la construcción de compiladores. Imagínate que es como un framework para construir compiladores. Muchos de los lenguajes actuales están creados usando este proyecto. Por ejemplo [Rust](https://rust.org), Swift y [Julia](https://julialang.org) están construidos sobre LLVM.

Una de las partes que hace muy útil a LLVM es su **representación intermedia**. Esta representación intermedia permite que los diferentes lenguajes de programación que funcionan sobre él se aprovechen de las optimizaciones que LLVM hace sobre el código intermedio. El flujo del código es el siguiente:

1. El código fuente es compilado a código intermedio (**IR**).
2. El **IR** es optimizado.
3. El **IR** es compilado a código de máquina.

De hecho, se dice que Swift es sólo azúcar sintáctico sobre la representación intermedia de LLVM, es decir, que se parace mucho a esta representación intermedia y aprovecha sus características.

MLIR (Multi-layer Intermediate Representation o Representación intermedia multi-capa) es una representación intermedia de más alto nivel que la representación intermedia trad  icional. No en el sentido de que sea más fácil de entender para los humanos, sino que en vez de mapearse directamente con una infraestructura de compilación, representa un modelo más abstracto que puede ser mapeado a diferentes infraestructuras de compilación, de manera especializada para cada una de ellas.

El objetivo de MLIR es crear herramientas para construir compiladores que se adapten a ejecutores específicos (por ejemplo GPU's), sin tener que crear una nueva representación intermedia.

## Entra Mojo

Toda esta explicación anterior es para entender que Mojo es para MLIR lo que Swift es para LLVM. Aprovecha gran parte de las características de MLIR para crear un lenguaje de programación que pueda aprovechar ejecutores especializados en cómputo de alto rendimiento como GPU's y TPU's, pero presentando una sintaxis más amigable para los humanos, a diferencia de CUDA, o C++, por ejemplo.

Mojo te ayuda aprovechar el paralelismo masivo de los GPU's sin tener que preocuparte por aprender un nuevo lenguaje o siquiera tener que pensar en dónde finalmente se ejecutará tu programa.

## Características de Mojo

Las pruebas iniciales de Mojo revelan que puede ser hasta **68,000** veces más rápido que Python en ciertas tareas (sí, leíste bien **sesenta y ocho mil**), mientras que C++ llega a ser **_sólo_ 5,000** veces más rápido. Claro, esto no habla muy bien de Python, pero debes pensar en que su objetivo no es ser un lenguaje de alto rendimiento, sino un lenguaje de alto nivel y fácil de usar.

Mojo quiere aprovechar la facilidad de uso de Python junto con su ecosistema de bibliotecas y desarrollos para hacer un ecosistema de desarrollo de inteligencia artificial más rápido y fácil de usar.

## ¿Deberías aprenderlo?



## Conclusión



