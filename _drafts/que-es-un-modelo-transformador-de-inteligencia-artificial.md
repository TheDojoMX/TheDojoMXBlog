---
title: "¿Qué es un modelo transformador de inteligencia artificial?"
date: 2023-02-26
author: Héctor Patricio
tags: transformers transformadores gpt-3 inteligencia-artificial
comments: true
excerpt: "Con GPT-3 y Dall-e 2 ha explotado de nuevo el interés en las capacidades de los modelos de inteligencia artifical generativos. En este post vamos a hablar de la arquitectura en la que están basados."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1350/v1675031892/vinicius-amnx-amano-IPemgbj9aDY-unsplash_cttyeh.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_450/v1675031892/vinicius-amnx-amano-IPemgbj9aDY-unsplash_cttyeh.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

En los últimos años los modelos de inteligencia artificial generativos han avanzado mucho. Esto es en parte gracias a una nueva arquitectura para las redes neuronales llamada _transformer_ o de transformador, como les llamaremos en este artículo. Hablemos de en qué consiste esta arquitectura y por qué es tan revolucionaria o porque ha ayudado tanto a avanzar en el campo de la inteligencia artificial.

## Redes neuronales recurrentes (RNN)

Estas eran el estándar para hacer varias tareas, entre ellas la traducción. Las redes neuronales recurrentes se llaman así porque sus entradas se alimentan en ciclos, es decir, en vez de siempre mandar su salida a las siguientes capas, también manda la salida a capas anteriores o a la misma capa.

Esta arquitectura permite que la red desarrolle memoria, algo que sirve bien para tratar con textos porque normalmente las palabras que van adelante están influidas por las que están antes.

Sin embargo, el entrenamiento de este tipo de redes neuronales requiere de mucho tiempo y recursos. Además, su memoria no es tan buena como para manejar textos muy largos. Así que la traducción o tratamiento de textos largos no les salía muy bien.

Además, la forma secuencial de tratar las palabras las hace difíciles de entrenar. Aquí es cuando los investigadores de Google diseñaron otra arquitectura.

## Redes neuronales de transformador (Transformers)

Es una arquitectura más sencilla que las utilizadas anteriormente. Los transformadores están construidos en gran parte por mecanismos de **atención**. Podemos decir que tiene tres componentes principales:

1. Codificación de posición
2. Mecanismo de atención
3. Mecanismo de auto-atención

Hablemos de cada una de estas partes más detenidamente, explicadas para un desarrollador de software.

### Codificación de posición

Esta es la primera innovación del modelo transformador. En vez de procesar las palabras como una secuencia para conservar su orden, lo que limita el paralelismo o la capacidad de procesar varias palabras a la vez, se crean tuplas que contienen la palabra y su posición en el texto. Esto permite que la red pueda procesar varias palabras a la vez.
La posición del texto como se explica en [Attention is all you need](https://arxiv.org/abs/1706.03762) depende de una función basada en el seno y coseno, no un número entero de dónde se encontró en el texto.

### Atención

El mecanismo de atención le da un peso diferente a cada palabra en función, con respecto a la palabra que ese está procesando. Este peso determina en donde se está "fijando" el modelo para procesar la palabra actual. Por ejemplo, imagina que se está traduciendo:

> "The cat is angry"

### Auto-atención

El mecanismo de atención anterior tiene que ver con la influencia que otras partes del texto o de la entrada tienen en la palabra que se está procesando. El mecanismo de auto-atención tiene que ver con la influencia que la palabra que se está procesando tiene en otras partes del texto o de la entrada.

Este mecanismo de auto-atención permite que el modelo encuentre patrones a través de muchos ejemplos de entrenamiento. Estos patrones tienen que ver con el significado de la palabra, los sinónimos, la gramática, etc.

Esta es la parte más importante de un transformador y es lo que hace que los modelos que tienen esta arquitectura sean tan poderosos.

## Conclusión

Las redes neuronales con arquitectura de transformador permiten lograr cosas que no creíamos posibles y son la base de los grandes modelos de lengua natural como GPT-3. Conocer un poco más cómo funcionan nos puede dar una idea de lo que son capaces y sus límites, además de que es bastante interesante. Si quieres que hablemos de algún tema en específico puedes dejarnos un comentario.
