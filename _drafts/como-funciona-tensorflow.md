---
title: "¿Cómo funciona TensorFlow?"
date: 2024-03-08
author: Héctor Patricio
tags:
comments: true
excerpt: "Escribe aquí un buen resumen de tu artículo"
header:
  overlay_image: #image
  teaser: #image
  overlay_filter: rgba(0, 0, 0, 0.5)
---

TensorFlow es una de las herramientas más populares e influyentes
en el mundo de la inteligencia artificial. En este artículo vamos a ver 
qué es exactamente y cómo funciona.

## ¿Qué es Tensoflow?

Para crear modelos de inteligencia artificial, hay que hacer muchos cálculos  
matemáticos, la mayoría de ellos son operaciones de multiplicación de matrices.
Estos cálculos son muy pesados para un procesador tradicional y por eso se
requiere de toda la ayuda posible para hacer estos cálculos más eficientes.

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
en **TensorFlow**. La operación es la siguiente:

```python
Y = W * X + b
```
Esta es la ecuación que un perceptrón simple. Vemos cómo la representa TensorFlow.
Para que esto sea útil, cada una de las operaciones se hace sobre tensores, es decir,
sobre un conjunto de datos numéricos de varias dimensiones.

¿Cómo representa TensorFlow esto? Este es el grafo de cómputo que representa esa
operación:

![Grafo de cómputo de TensorFlow](/assets/images/tensorflow-graph.png)


Puedes pensar en este grafo como una serie de nodos que representan cada uno una operación
sobre TENSORES.


