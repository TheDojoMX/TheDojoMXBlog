---
title: ¿Cómo funciona TensorFlow?
date: 2024-08-31
author: Héctor Patricio
tags: null
comments: true
excerpt: >-
  TensorFlow permite crear modelos de aprendizaje automático sin que te tengas
  que plear con la forma en la que se hacen los cálculos en los ejecutores. Hablemos
  más de cómo funciona.
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1450/v1725143057/gabriel-izgi-cfQEO_1S0Rs-unsplash_ihiase.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_450/v1725143057/gabriel-izgi-cfQEO_1S0Rs-unsplash_ihiase.jpg
  overlay_filter: 'rgba(0, 0, 0, 0.5)'
---

**TensorFlow** es una de las herramientas más populares e influyentes
en el campo de la inteligencia artificial. En este artículo vamos a ver
qué es exactamente y cómo funciona.

## ¿Qué es TensorFlow?

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

Para entenderlo, vamos a ver un ejemplo sencillo de un cálculo y su representaciónoooo

ooo

oooo

2. second
3. third

2. second
3. third

2. second
3. third

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

Keras es un framework que te permite crear modelos de aprendizaje profundo de manera sencilla.
¿Cómo se relaciona con TensorFlow? Con Keras declaras tus modelos y TensorFlow se encarga de
transformarlos en un grafo de cómputo que se puede ejecutar en el hardware que tengas disponible.

## TensorFlow vs PyTorch

Pytorch es una alternativa a TensoFlow con un modelos de programación más dinámicos

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
