---
title: "Problemas difíciles de la computación y su relación con la criptografía: NP-Hard"
date: 2023-02-03
author: Héctor Patricio
tags: criptografía computer-science cs complejidad-computacional
comments: true
excerpt: "En esta serie de posts vamos a hablar de una serie de problemas difíciles de la ciencia de la computación y su relación con la criptografía."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_crop,h_700,w_1400/v1675031879/marek-okon-dHUhghn9mrI-unsplash_p3ng6t.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_crop,h_350,w_700/v1675031879/marek-okon-dHUhghn9mrI-unsplash_p3ng6t.jpg
  overlay_filter: rgba(0, 0, 0, 0.6)
usemathjax: true
---

La intuición a veces nos dice que cualquier cálculo numérico _debería_ ser muy fácil para una computadora. Sin embargo, hay problemas numéricos y no numéricos que son imposibles de resolver para las computadoras actuales, independientemente de su poder de procesamiento.

La **criptografía** actual está soportada por una serie de problemas que _suponemos muy difíciles_ de resolver de la ciencias de la computación.

En esta serie de artículos vamos a estar hablando de ellos para entenderlos a profundidad y sobre todo para entender cómo es que se relacionan con los algoritmos criptográficos, como con los algoritmos de llave pública, como Diffie-Hellman y RSA.

Pero primero hablemos de lo que consideramos un problema difícil de la computación y la complejidad computacional.

## Complejidad computacional

La complejidad computacional se puede entender como la **cantidad de operaciones** que un algoritmo ejecuta para finalizar. Esta cantidad de operaciones es una función (en el sentido _matemático_) de la entrada del problema. Puedes pensar en una función como una relación entre la entrada y el tiempo de ejecución.

Por ejemplo, si te piden contar todas las letras "a" e una cadena, esto podría resolverse de la siguiente manera en Python:

```python
def contar_a(string):
    count = 0
    for char in string:
        if char == "a":
            count += 1
    return count
```

¿Cuántas operaciones tarda este algoritmo? Como dijimos _depende_ de la entrada. Esa relación de dependencia es una función. Lo que la función nos dice es _qué relación existe_ entre la entrada y la cantidad de operaciones que se ejecutan.

En este ejemplo específico, tenemos que hacer  1 ó 2 operaciones por cada letra de la entrada, y esto no cambia, independientemente de la longitud de esta cadena de entrada. Por lo tanto la función que describe la relación entre la entrada y la cantidad de operaciones es:

$$f(n) = 2n$$

Donde $n$ es la longitud de la cadena de entrada. Como esta relación crece proporcionalmente a la entrada, es decir, lo mismo que crece la entrada crece el tiempo de ejecución, decimos que este algoritmo es de complejidad lineal.

## Tiempo polinomial (P)

Un polinomio es una expresión matemática que consiste en sumas, restas, multiplicaciones, divisiones y potencias de números.

Un algoritmo es de complejidad polinomial si su tiempo de ejecución es una función que consiste en multiplicaciones, sumas o elevaciones a _ciertas_ potencias del tamaño de la entrada. Algunos ejemplos de complejidad polinomial son:

$$f(n) = 2n$$

$$f(n) = 3n^2$$

$$f(n) = 4n^3$$

$$f(n) = n^{log(n)}$$

En la práctica, si un algoritmo es tiene complejidad polinomial quiere decir que su ejecución es más o menos rápida (o por lo menos posible en caso de polinomios muy grandes) para cualquier entrada.

## La notación Big O

La notación más usada para expresar la complejidad no es la de una función común como lo hemos hecho hasta ahora. Normalmente, lo que nos interesa es expresar o conocer **el peor de los casos** para un algoritmo específico. Por ejemplo, si estamos observando un algoritmo de búsqueda como el siguiente:

```python
  def buscar(lista, elemento):
      for i in range(len(lista)):
          if lista[i] == elemento:
              return i
      return -1
```

El peor de los casos es cuando el elemento esté en el último lugar. Por lo tanto, su complejidad en el peor de los casos depende directamente de la longitud de la lista de entrada. Podemos expresar esta complejidad con una función como:

$$f(n) = n$$

Pero la notación Big O nos permite expresar esto de una manera más simple:

$$O(n)$$

En el ejemplo de arriba, de la búsqueda de las letras "a" en una cadena, la complejidad que calculamos expresada como función en el peor de los casos es:

$$f(n) = 2n$$

En la notación Big O se eliminan todas los valores constantes, y por la tanto esta complejidad se expresa como:

$$O(n)$$

Equivalente al ejemplo anterior. Lo que tienes que recordar de la notación Big O es que te da un **límite superior** de operaciones que se ejecutarán para un algoritmo.

En este artículo no vamos a hablar de cómo calcular más complejidades, pero probablemente lo hagamos en uno futuro.

Ahora, con esta notación, estamos listos para seguir hablando de las clases de complejidad.

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
