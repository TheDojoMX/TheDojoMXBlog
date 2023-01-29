---
title: "Problemas difíciles de la computación y su relación con la criptografía: NP-Hard"
date: 2023-02-03
author: Héctor Patricio
tags: criptografía computer-science cs complejidad-computacional
comments: true
excerpt: "En esta serie de posts vamos a hablar de una serie de problemas difíciles de la ciencia de la computación y su relación con la criptografía."
header:
  overlay_image: #image
  teaser: #image
  overlay_filter: rgba(0, 0, 0, 0.5)
usemathjax: true
---

La criptografía actual está soportada por una serie de problemas que suponemos muy difíciles de resolver de la ciencias de la computación. En esta serie de artículos vamos a estar hablando de ellos para entenderlos a profundidad y sobre todo para entender cómo es que se relacionan con los algoritmos criptográficos, principalmente con los algoritmos de llave pública, cmo Diffie-Hellman y RSA.

Primero hablemos de lo que consideramos un problema difícil de la computación y la complejidad computacional.

## Complejidad computacional

La complejidad computacional se puede entender como la **cantidad de operaciones** que un algoritmo ejecuta para finalizar. Esta cantidad de operaciones es una función (en el sentido _matemático_) de la entrada del problema.

Por ejemplo si te piden contar todas las letras "a" e una cadena, esto podría resolverse de la siguiente manera en Python:

```python
  def contar_a(string):
      count = 0
      for char in string:
          if char == "a":
              count += 1
      return count
```

¿Cuántas operaciones tarda este algoritmo? Como dijimos _depende_ de la entrada. Esa relación de dependencia es una función. Lo que la función nos dice es _qué relación existe_ entre la entrada y la cantidad de operaciones que se ejecutan.

En este ejemplo específico, tenemos que hacer 2 operaciones por cada letra de la entrada, y esto no cambia, independientemente de la longitud de esta cadena de entrada. Por lo tanto la función que describe la relación entre la entrada y la cantidad de operaciones es:

$$f(n) = 2n$$

Donde $n$ es la longitud de la cadena de entrada. Esta función es una función lineal, y se puede representar gráficamente de la siguiente manera:

## Tiempo polinomial (P)

Un algoritmo es de complejidad polinomial si su tiempo de ejecución es una función que consiste en multiplicaciones, sumas o elevaciones a _ciertas_ potencias del tamaño de la entrada. Algunos ejemplos de complejidad polinomial son:

$$f(n) = 2n$$

$$f(n) = 3n^2$$

$$f(n) = 4n^3$$

$$f(n) = n^{log(n)}$$

En la práctica, si un algoritmo es tiene complejidad polinomial quiere decir que su ejecución es más o menos rápida (o por lo menos posible en caso de polinomios muy grandes) para cualquier entrada.

## La notación Big O

La notación más usada para expresar esas complejidades no es una función como lo hemos hecho hasta ahora. Normalmente, lo que nos interesa es expresar o conocer **el peor de los casos** para un algoritmo específico. Por ejemplo, si estamos observando un algoritmo de búsqueda como el siguiente:

```python
  def buscar(lista, elemento):
      for i in range(len(lista)):
          if lista[i] == elemento:
              return i
      return -1
```

Sabemos que el peor de los casos es cuando el elemento esté en el último lugar. Por lo tanto, su complejidad depende directamente de la longitud de la lista de entrada. Podemos expresar esta complejidad como:

$$O(n)$$

En este artículo no vamos a hablar de cómo calcular esas complejidades, pero si quieres saber más, te recomiendo este artículo: [Big O Cheatsheet](https://www.bigocheatsheet.com/).

### Tiempo súper polinomial (SP)

Una clase que estaría bien separar de los polinomios es la de los tiempos súper polinomiales. Estos algoritmos son polinomiales, pero con un polinomio muy grande. Por ejemplo:

$$f(n) = 2^{n^2}$$

### Tiempos polinomiales no deterministas (NP)

### Exponencial (EXP)

## Problemas que creemos que son difíciles

## Problema de la factorización

En los siguientes artículos vamos a estar hablando de los siguientes problemas:

- Campos de Galois en curvas elípticas
- Algo más
