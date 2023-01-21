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

Se llama _bytecode_ porque normalmente es una secuencia de bytes que representan tanto las instrucciones como los datos.

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

La **Bogdan/Björn Erlang Abstract Machine** (BEAM) tiene un [set de instrucciones](http://www.cs-lab.org/historical_beam_instruction_set.html), que constituyen su bytecode. Estos aunque están semi-documentados aquí, no están documentados oficialmente y pueden cambiar en cada release.

Cuando compilas una archivo de Elixir, se crea un archivo con el mismo nombre de tu módulo, pero con la extensión `.beam`. Este archivo contiene el bytecode de tu programa. Para poder verlo en nuestro editor, necesitamos herramientas especiales. Para VSCode, podemos usar la extensión [BEAMdasm](https://marketplace.visualstudio.com/items?itemName=Valentin.beamdasm).

Aquí podemos ver el ejemplo de lo que genera el programa anterior:

```bash
Module:  Elixir.Hello

Attributes: [{vsn, [72315C84EFAF57A23F8E5FD7551E9C5D]}]

Compilation Info: [{version, 8.2.2}, {options, [no_spawn_compiler_process, from_core, no_core_prepare, no_auto_import]}, {source, /Users/hectorip/Development/elixir/hello_world/hello_world.exs}]


//Function  Elixir.Hello:__info__/1
label01:  func_info            Elixir.Hello __info__ 1
label02:  select_val           X[0] label09 [attributes, label08, compile, label08, deprecated, label07, exports_md5, label06, functions, label05, macros, label07, md5, label08, module, label04, struct, label03]
label03:  move                 nil X[0]
          return
label04:  move                 Elixir.Hello X[0]
          return
label05:  move                 [{greet, 0}] X[0]
          return
label06:  move                 7~�t�jO;_���lS X[0]
          return
label07:  move                 nil X[0]
          return
label08:  move                 X[0] X[1]
          move                 Elixir.Hello X[0]
          call_ext_only        2 erlang:get_module_info/2
label09:  call_only            1 label17

//Function  Elixir.Hello:greet/0
label10:  func_info            Elixir.Hello greet 0 //line hello_world.exs, 2
label11:  move                 Hello, world! X[0]
          call_ext_only        1 Elixir.IO:puts/1 //line hello_world.exs, 3

//Function  Elixir.Hello:module_info/0
label12:  func_info            Elixir.Hello module_info 0
label13:  move                 Elixir.Hello X[0]
          call_ext_only        1 erlang:get_module_info/1

//Function  Elixir.Hello:module_info/1
label14:  func_info            Elixir.Hello module_info 1
label15:  move                 X[0] X[1]
          move                 Elixir.Hello X[0]
          call_ext_only        2 erlang:get_module_info/2

//Function  Elixir.Hello:-inlined-__info__/1-/1
label16:  func_info            Elixir.Hello -inlined-__info__/1- 1
label17:  jump                 label16
          int_code_end
```

### Ejemplo con JavaScript

También podemos ver el bytecode de JavaScript. Si tienes instalado `node` en tu computadora.

## Resumen

El bytecode es un producto secundario e intermedio de la compilación en algunos lenguajes y entornos de ejecución. En algunos casos es directamente el objeto que la máquina virtual ejecuta y en otros se puede pensar como un caché de la ejecución que se puede usar en las ejecuciones posteriores de un programa para mejorar el rendimiento.

A veces se puede usar el bytecode con otros propósitos, por ejemplo, para hacer optimizaciones en tiempo de ejecución, que es lo que hacen los compiladores bajo de demanda o JIt's.

## Aprende más

* [Bytecode](https://en.wikipedia.org/wiki/Bytecode) en Wikipedia
