---
title: ¿Cómo funciona TensorFlow?
date: 2024-08-31
author: Héctor Patricio
tags: tensorflow machine-learning ai deep-learning
comments: true
excerpt: >-
  TensorFlow permite crear modelos de aprendizaje automático sin que te tengas
  que plear con la forma en la que se hacen los cálculos en los ejecutores. Hablemos
  más de cómo funciona.
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1450/v1725143057/gabriel-izgi-cfQEO_1S0Rs-unsplash_ihiase.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_450/v1725143057/gabriel-izgi-cfQEO_1S0Rs-unsplash_ihiase.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

**TensorFlow** es una de las herramientas más populares e influyentes
en el campo de la del aprendizaje automático. En este artículo vamos a ver
qué es exactamente y cómo funciona.

## ¿Qué es TensorFlow?

Siempre que hablamos de TensorFlow se dice que es una "biblioteca (o librería,
o framework) para hacer aprendizaje automático, pero este definición no es muy
explícita y por eso vamos a ver cómo nos permite crear modelos de aprendizaje.

Para crear modelos de aprendizaje automático, tenemos que hacer muchos cálculos
matemáticos, la gran mayoría son operaciones de multiplicación de matrices.
Estos cálculos no son eficientes en un procesador tradicional y por eso se
requiere de toda la ayuda que se pueda conseguir para hacerlos lo más rápido
posible y gastando menos energía.

Es aquí donde entra **TensorFlow**, una biblioteca que permite _representar_ estos
cálculos mediante grafos de cómputo y después ejecutarlos en procesadores
especializados como tarjetas gráficas y otros procesadores eficientes en
operaciones matemáticas pesadas. Además, TensorFlow abstrae al usuario final (tú),
de los detalles de implementación de muchas funciones y operaciones matemáticas
que se usan mucho en el aprendizaje automático. Y finalmente, con su _API_ de alto
nivel, **Keras**, te permite crear diferentes tipos de redes neuronales sin
que tengas que pelearte con los detalles de implementación.

Y es aquí donde empieza lo interesante. ¿Qué es un grafo de cómputo? ¿Cómo
llegamos a él y para qué nos sirve? Veamos.

## Grafos de cómputo de TensorFlow

Para entenderlo, vamos a ver un ejemplo sencillo de un cálculo y su
representación

```python
Y = W * X + b
```

Esta es la ecuación que un perceptrón. ¿Cómo representa TensorFlow esto? Este
es el grafo de cómputo que escribir este código nos da:

![Imagen de un grafo de cómputo de TensorFlow]()

Puedes pensar en este grafo como una serie de nodos que representan cada uno
una operación sobre conjuntos de datos numéricos llamados tensores. Cuando
ejecutamos este grafo, los tensores _fluyen_ por estos nodos, transformándose
en cada uno, hasta que obtenemos el resultado final de la operación.

De ahí viene el nombre de la biblioteca: **TensorFlow**.

## Ejecución de un grafo de cómputo

Todo esto de los grafos de cómputo tiene un objetivo específico: poder ejecutar
las operaciones de manera eficiente en diferentes tipos de hardware, desde
procesadores comunes hasta hardware especializado en cómputo de alto
rendimiento.

## TensorFlow y Keras

Keras es un framework que te permite crear modelos de aprendizaje profundo de manera sencilla.

¿Cómo se relaciona con TensorFlow? Con Keras declaras tus modelos y TensorFlow se encarga de
transformarlos en un grafo de cómputo que se puede ejecutar en el hardware que tengas disponible.

## TensorFlow vs PyTorch

PyTorch es una alternativa a TensorFlow con un modelos de programación más dinámicos

## TensorFlow y MLIR

MLIR es una herramienta para crear compiladores creada por el mismo equipo
que hizo LLVM, la infraestructura para compiladores que está detrás de
la mayoría de los compiladores modernos.

La especialidad de MLIR es hacer traducciones para arquitecturas de hardware no
tradicionales,usando un lenguaje intermedio multi-capa (al que le puedes agregar)
más plugins para diferentes arquitecturas.

## TensorFlow y su relación con el hardware

Después de la sección anterior, es muy probable que la relación de TF con el hardware quede muy clara: TensorFlow ayuda a que se pueda compilar de mejor manera el código con los cálculos
para poder ejecutarlo en el hardware especializado.

## Conclusión

Espero que lo que hablamos sobre TensorFlow en este artículo te haya ayudado
a entenderlo un poco más. En otro artículo hablaremos de su competidor más directo: **PyTorch**.
