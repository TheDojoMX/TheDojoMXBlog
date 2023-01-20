---
title: "Entendiendo el bytecode"
date: 2023-01-19
author: Héctor Patricio
tags: bytecode complación intérprete
comments: true
excerpt: "En algunos lenguajes de programación se genera algo que llamamos bytecode antes de que se ejecute. Hablemos de qué es para que lo entiendas mejor."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1674189353/1829084045_mad_cat_scientist_looking_into_a_black_screen_with_binary_code__detailed_concept_art___artstation__H_bttvyj.png
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_300/v1674189353/1829084045_mad_cat_scientist_looking_into_a_black_screen_with_binary_code__detailed_concept_art___artstation__H_bttvyj.png
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Tanto para Java como para otros lenguajes que son interpretados, por ejemplo Python o JavaScript, se genera una representación intermedia como resultado de la ejecución o compilación. A este código le llamamos bytecode.

Hablemos de qué es y para qué existe.

## ¿Qué es el bytecode?

El bytecode es una representación intermedia de tu programa que tiene dos características principales:

1. No es tan legible como el código fuente, por ser más compacta.
2. Es independiente de la arquitectura de la máquina, por lo que siempre es la misma representación para tu máquina virtual.

El objetivo del bytecode entonces es conservar la semántica de tu programa, pero de una forma que sea más fácil de ejecutar en una máquina virtual o el intérprete.

## Ejemplo de un bytecode

Veamos el ejemplo de Elixir y el código de bytes que produce, para entender el con un ejemplo.

```elixir
defmodule Hello do
  def greet do
    IO.puts "Hello, world!"
  end
end
```

El proceso que Elixir sigue para ejecutarse es el siguiente:

![Procesamiento de Elixir al Bytecode de BEAM](https://res.cloudinary.com/hectorip/image/upload/v1674191298/58786d8c955aaa5df2ebdb5a2c2790da5216b705_bllv3i.png){: .align-center}

Fuente: [Getting each stage of Elixir’s compilation all the way to the BEAM bytecode](https://elixirforum.com/t/getting-each-stage-of-elixirs-compilation-all-the-way-to-the-beam-bytecode/1873/7).
