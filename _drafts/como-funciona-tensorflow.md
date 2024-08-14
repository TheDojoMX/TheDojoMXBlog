---
title: ¿Cómo funciona TensorFlow?
date: 2024-03-08T00:00:00.000Z
author: Héctor Patricio
tags: null
comments: true
excerpt: >-
  TensorFlow permite crear modelos de aprendizaje automático sin que te tengas
  que plear con los cáluculos, hablemos de cómo lo hace.
header:
  overlay_image: null
  teaser: null
  overlay_filter: 'rgba(0, 0, 0, 0.5)'
---
TensorFlow es una de las herramientas más populares e influyentes
en el campo de la inteligencia artificial. En este artículo vamos a ver
qué es exactamente y cómo funciona.

## ¿Qué es Tensoflow?

Para crear modelos de inteligencia artificial, hay que hacer muchos cálculos  
matemáticos, la mayoría de ellos son operaciones de multiplicación de matrices.
Estos cálculos son no son eficientes en un procesador tradicional y por eso se
requiere de toda la ayuda posible para hacer estos cálculos menos costosos.

Es aquí donde entra TensorFlow, una biblioteca que permite _representar_ estos
cálculos mediante grafos de operaciones y después ejecutarlos en procesadores
especializados como tarjetas gráficas y otros procesadores especializados en
operaciones matemáticas pesadas.

Esta representación que TensorFlow crea, también se puede compilar para ejecutarse
en otros dispisitivos de cómputo, por ejemplo cosas menos poderosas como
dispositivos móviles o computadoras de bajo consumo, pero también en dispositivos
de alto rendimiento com TPUs (Tensor Processing Units) de Google.

Y es aquí donde entra lo interesante. ¿Qué es un grafo de cómputo? ¿Cómo
llegamos a él y cómo lo ejecutamos después?

## Grafos de cómputo de TensorFlow

Para entenderlo, vamos a ver un ejemplo sencillo de un cálculo y su representación
en **TensorFlow**:

```python
Y = W * X + b
```

Esta es la ecuación que un perceptrón simple. Vemos cómo la representa TensorFlow.
Para que esto sea útil, cada una de las operaciones se hace sobre tensores, es decir,
sobre un conjunto de datos numéricos de varias dimensiones.

¿Cómo representa TensorFlow esto? Este es el grafo de cómputo que representa esa
operación:

Puedes pensar en este grafo como una serie de nodos que representan cada uno
una operación sobre TENSORES, es decir, conjuntos de datos numéricos de más de dos dimensiones,

## Cómo se ejecuta un grafo de cómputo

Después de representar el cálculo en un grafo, abrstrayendo el orden y las operaciones que se deben eejecutar,
viene la parte de ahora sí hacer los cálculos.

## TensorFlow y Keras

Keras te ayuda declarar redes neuronales de manera sencilla.

## TensorFlow vs PyTorch

Pytorch es una alternativa a TensoFlow con un modelos de programación más

## Tensoflow y MLIR

MLIR es una herramienta para crear compiladores creada por el mismo equipo
que hizo LLVM, la infraestructura para compiladores que está detrás de
la mayoría de los compiladores modernos.

La especialidad de MLIR es hacer traducciones para arquitecturas de hardware no
traciionales,usando un lenguaje intermedio multicapa (al que le puedes agregar)
más plugins para diferentes arquitecturas.

## Tensorflow y su relación con el hardware

Después de la sección anterior, es muy probable que la relación de TF con el hardware quede muy clara: TensorFlow ayuda a que se pueda compilar de mejor manera el código con los cálculos
para poder ejecutarlo en el hardware especializado.

## Conclusión

Espero que lo que hablamos sobre TensorFlow en este artículo te haya ayudado
a entenderlo un poco más. En otro artículo hablaremos de su competidor más directo: **PyTorch**.
