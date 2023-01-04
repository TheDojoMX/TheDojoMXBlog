---
title: "Ejercicio: programando un perceptrón"
date: 07-01-2023
author: Héctor Patricio
tags: machine-learning ia
comments: true
excerpt: "Programemos un perceptrón en Python para entender a fondo como funciona y poder construir sobre eso para temas más complejos."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,e_oil_paint:30,w_1400/v1618030907/arseny-togulev-MECKPoKJYjM-unsplash_nakl3a.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,e_oil_paint:30,w_300/v1618030907/arseny-togulev-MECKPoKJYjM-unsplash_nakl3a.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

En este post platicaremos acerca de cómo funciona un perceptrón a nivel de código y las técnicas que utiliza para aproximar una función a partir de datos.

Si no tienes claro lo que es un perceptrón, puedes leer nuestro [artículo anterior](/2021/03/25/intro-a-machine-learning-entendiendo-perceptron.html){:target="_blank"}. Ahí también explicamos las bases de funcionamiento. En este artículo lo vamos a ilustrar.

Escogimos: <https://www.data-is-plural.com/>

## El conjunto de datos

Recuerda que para poder crear un algoritmo de machine learning necesitamos un conjunto de datos, ya que el punto es que este algoritmo _aprenda_ de estos datos.

Los datos que un perceptrón puede clasificar deben estar divididos en dos clases completamente separables, ya que si representáramos al perceptrón como una función, es un línea recta en un plano de dos variables (o su equivalente dependiendo del espacio y sus dimensiones, lo que en para más de tres dimensiones llamamos un _hiperespacio_ matemáticamente).

No es necesario que los datos _sólo_ puedan estar divididos en dos clases, por ejemplo, imagínate un conjunto de datos que representa los dígitos escritos a mano, del 0 al 9 (este es conocido como el [MNIST dataset](https://www.tensorflow.org/datasets/catalog/mnist)). Cada dígito es una clase, pero un perceptrón nos puede servir para clasificar un solo número, por ejemplo, el 5. El perceptrón serviría para clasificar si un dígito es un 5 o no, lo importante es que el conjunto de datos que representa el 5 sea más o menos separable de los demás dígitos.

Con esto te puedes empezar a dar cuenta de que el perceptrón es el bloque de construcción más básico de las redes neuronales. Por ejemplo, ¿cómo haríamos para clasificar todos los números del conjunto del que hablamos arriba? Necesitamos un perceptrón por cada número, y tomamos el que más confianza nos devuelva.

Ahora sí veamos qué dataset usaremos nosotros. Ejemplos usando el MNIST o el [Iris](https://archive.ics.uci.edu/ml/datasets/iris) encontrarás en muchos lados, así que vamos a escoger uno diferente.
Este es una alternativa a Iris y se conoce como el [Penguin dataset](https://github.com/allisonhorst/palmerpenguins). Para facilitarnos la vida, lo vamos a extraer de la biblioteca [Vega datasets](https://vega.github.io/vega-datasets/) que lo tiene como un conjunto de ejemplos.

El conjunto de datos de los pingüinos tiene 344 registros etiquetados, cada uno con máximo 6 características (a parte de la etiqueta). Tiene 3 etiquetas diferentes: Adelie, Chinstrap y Gentoo. Las columnas del dataset son:

1. **species**: especie del pingüino, esta es la clase o etiqueta
2. **island**: isla donde fue visto el pingüino, tiene 3 valores diferentes: Dream, Torgersen, or Biscoe
3. **culmen_lenth_mm**: longitud de la pico del pingüino
4. **culmen_depth_mm**: profundidad de la pico del pingüino
5. **flipper_length_mm**: longitud de la aleta del pingüino
6. **body_mass_g**: masa del cuerpo del pingüino
7. **sex**: sexo del pingüino

Tenemos que explorar los datos brevemente para ver qué variables podemos usar para separar. Como este no es el obejtivo de este artículo vamos a usar las variables **culmen_lenth_mm** y **culmen_depth_mm**.

## Repaso del funcionamiento básico

El perceptrón es un algoritmo de aprendizaje **supervisado**, por lo que necesita datos etiquetados, es decir, las características junto con su clase. El trabajo del perceptrón es encontrar los parámetros para una función matemática que defina la frontera de separación entre las clases.

Esta función matemática es una línea recta en un plano de dos dimensiones, o un plano en un espacio de tres dimensiones, o un **hiperplano** en un espacio de más de tres dimensiones. Puedes pensar en todos estos términos matemáticos como el equivalente a una linea recta en cualquier espacio.s

## Resultado
