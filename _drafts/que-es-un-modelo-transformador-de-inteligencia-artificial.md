---
title: "¿Qué es un modelo transformador de inteligencia artificial?"
date: 2023-02-17
author: Héctor Patricio
tags: transformers transformadores gpt-3 inteligencia-artificial
comments: true
excerpt: "Con GPT-3 y Dall-e 2 ha explotado de nuevo el interés en las capacidades de los modelos de inteligencia artifical generativos. En este post vamos a hablar de la arquitectura en la que están basados."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1350/v1675031892/vinicius-amnx-amano-IPemgbj9aDY-unsplash_cttyeh.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_450/v1675031892/vinicius-amnx-amano-IPemgbj9aDY-unsplash_cttyeh.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

En los últimos años los modelos de inteligencia artificial generativos han avanzado mucho. Esto es en parte gracias a una nueva arquitectura para las redes neuronales llamada `transformer` o de transformador. En este artículo vamos a hablar en qué consiste y por qué es tan revolucionaria o porque ha ayudado tanto a avanzar en el campo de la inteligencia artificial.

## Redes neuronales recurrentes

Estas eran el estándar para hacer varias tareas, entre ellas la traducción. Las redes neuronales recurrentes se llaman así porque sus entradas se alimentan en ciclos, es decir, en vez de siempre mandar su salida a las siguientes capas, también manda la salida a capas anteriores.

Esta arquitectura permite que la red desarrolle memoria, algo que sirve bien para tratar con textos porque normalmente las palabras que van adelante están influidas por las que están antes.

Sin embargo, el entrenamiento de este tipo de redes neuronales requiere de mucho tiempo y recursos. Además, su memoria no es tan buena como para manejar textos muy largos. Así que la traducción o tratamiento de textos largos no les salía muy bien. Aquí es cuando los investigadores de Google diseñaron otra arquitectura.

## Redes neuronales de transformador

Es una arquitectura más sencilla que las utilizadas anteriormente, que tenían un codificador y un decodificador. Los transformadores están construidos completamente por mecanismos de **atención**. Pero las redes neuronales tienen otros componentes también. Podemos decir que tiene tres componentes principales:

1. Codificación de posición
2. Mecanismo de atención
3. Mecanismo de auto-atención

Hablemos de cada una de estas partes más detenidamente, como explicadas para un desarrollador de software y no un _matemático_.

### Codificación de posición

Esta es la primera innovación del modelo transformador. En vez de procesar las palabras como una secuencia para conservar su orden, lo que limita el paralelismo o la capacidad de procesar varias palabras a la vez, se crean tuplas que contienen la palabra y su posición en el texto. Esto permite que la red pueda procesar varias palabras a la vez.

### Atención

El mecanismo de atención le da un peso diferente a cada palabra en función.

### Auto-atención

## Conclusión

Las redes neuronales con arquitectura de transformador permiten lograr cosas que no creíamos posibles y son la base de los grandes modelos de lengua natural como GPT-3. Conocer un poco más cómo funcionan nos puede dar una idea de lo que son capaces y sus límites, además de que es bastante interesante. Si quieres que hablemos de algún tema en específico puedes dejarnos un comentario.
