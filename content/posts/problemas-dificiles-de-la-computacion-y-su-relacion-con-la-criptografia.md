---
title: "Problemas difíciles de la computación y su relación con la criptografía: Problemas NP"
date: 2023-02-03
author: "Héctor Patricio"
tags: ['criptografía', 'computer-science', 'cs', 'complejidad-computacional']
description: "En esta serie de posts vamos a hablar de una serie de problemas difíciles de la ciencia de la computación y su relación con la criptografía."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_crop,h_700,w_1400/v1675031879/marek-okon-dHUhghn9mrI-unsplash_p3ng6t.jpg"
draft: false
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

## Complejidad polinomial (P)

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

Equivalente al ejemplo anterior. Lo que tienes que recordar de la notación Big O es que te da un **límite superior** de operaciones que se ejecutarán para un algoritmo. Este límite lo podemos pensar como una línea que el algoritmo nunca va a tocar y mucho menos a rebasar, esto se llama una asíntota en matemáticas, por lo que también se le conoce como **notación asintótica**.

En este artículo no vamos a hablar de cómo calcular más complejidades, pero probablemente lo hagamos en uno futuro. A este tipo de cálculo, o análisis de algoritmos se le llama **"análisis asintótico"**.

Ahora, con esta notación, estamos listos para seguir hablando de las clases de complejidad.

## Complejidad súper polinomial

Una clase que estaría bien separar de los polinomios que acabamos de hablar, es la de los tiempos _súper polinomiales_. Estos algoritmos tienen una complejidad que crece muy rápido con respecto a su entrada. Por ejemplo:

$$O(n^{n ^ 2})$$

$$O(n!)$$

$$O(2^n)$$

Estos tres ejemplos crecen más rápido que cualquier función polinomial que común que podamos representar como $$O(n^k)$$, siendo k _una constante_ (que normalmente es un número pequeño).

A esta clase de complejidad la empezamos ya a considerar como problemas intratables en la computación. Pero hablemos, dentro de los tiempos súper polinomiales de otra clase característica.

### Complejidad Exponencial (EXP)

La clase de complejidad exponencial se expresa como $$O(2^n)$$. Cuando un algoritmo tiene un complejidad de esta categoría o mayor, se considera completamente incalculable.

Por ejemplo, si midiéramos la entrada en bits y tuviéramos una entrada de 100 bits, el número de operaciones sería $$2^{100}$$. Suponiendo que una buena computadora pudiera hacer 1,000,000 de operaciones por segundo, esta tardaría $$2^{81}$$ segundos en completar el cálculo. Sin embargo, calculamos que el universo "sólo" ha existido por menos de $$2^{34}$$. Así de grande es la complejidad exponencial.

Te preguntarás si con una computadora más rápida podemos resolver el problema. Veamos el récord de la computadora más poderosa en 2023, que puede hacer 1,000,000,000,000,000,000 de operaciones por segundo. Esto es $$2^{59.8}$$. Esto significa que una computadora de este tamaño tardaría $$2^{40.2}$$ segundos. "Poco" más que la edad del universo.

Este tipo de algoritmos son los que hay que ejecutar para encontrar una llave por fuerza bruta. Si quieres por ejemplo encontrar una llave de [AES](/2020/12/03/tipos-de-algoritmos-criptograficos.html#aes), tendrías que hacer $$2^128$$ intentos, en el peor de los casos.

## Tiempos polinomiales no deterministas (NP)

Hasta ahora hemos hablado de tiempos polinomiales que estamos seguros que _siempre_ se van a comportar como los conocemos o incluso van a mejorar.

Para las clases que hemos hablado existe su equivalente _no determinista_.

¿Qué tiene que ver el determinismo con la complejidad? El determinismo en las clases anteriores significa que sabemos con certeza que el resultado está abajo de la línea de complejidad que la notación Big O describe.

En el caso de los tiempos polinomiales no deterministas significa que una máquina de Turing no determinista puede resolver el problema en un tiempo polinomial. El que la máquina sea no determinista significa que no sabemos si el resultado está abajo de la línea de complejidad que la notación Big O describe, o que a veces lo logrará y otras veces no.

Esto en otras palabras, significa que para los problemas con complejidad NP se puede **adivinar** una solución en un tiempo finito no muy grande, pero no se puede encontrar esta solución o garantizar que se encontrará en un tiempo razonable para cada una de las entradas del algoritmo.

Otra característica que tienen los problemas NP es que aunque encontrar una solución sea difícil, verificarla es fácil.

Un ejemplo de un problema NP es el de encontrar una llave de [AES](/2020/12/03/tipos-de-algoritmos-criptograficos.html#aes) cuando conocemos el texto plano. Usando la fuerza bruta por ejemplo, podríamos encontrar la llave en un golpe de suerte y podríamos verificar que la llave es la correcta comparando el texto plano con el texto descifrado, si son iguales, entonces la llave es correcta.

Muchos de los problemas NP tienen que ver con combinatoria, con problemas que tienen que ver con la cantidad de combinaciones posibles que hay en un conjunto de elementos, justo como las llaves criptográficas.

## NP-Complete

Los problemas NP-Complete son la clase más difícil de resolver dentro de los problemas NP. Estos problemas se pueden transformar en otros problemas NP-complete, lo que significa que si se puede resolver un problema NP-complete, se puede resolver cualquier otro problema NP-complete en un tiempo razonable.

## Problemas que creemos que son difíciles y problemas NP

La criptografía actual se basa en problemas que creemos que son por lo menos NP. ¿Por qué usamos la palabra "creemos"? Porque no podemos probar que son NP, pero hasta el momento nadie ha encontrado una forma de resolverlos en tiempo polinomial, pero creemos que lo pueden ser. Lo ideal sería usar problemas que sean NP-Complete, pero no hay muchos problemas NP-Complete que se puedan usar en la criptografía, además de que existe la posibilidad de que si resuelven un problema NP-Complete, se resuelvan todos los problemas NP-Complete, lo que rompería la criptografía actual.

## Conclusión

La criptografía moderna se basa en problemas muy difíciles de resolver para cualquier computadora, para los que no existe un algoritmo eficiente que pueda encontrar una solución garantizada cada vez. Algunos de estos problemas son fáciles de verificar una vez que se propone una solución y son justo estos los que son más útiles para la criptografía.

Lo más interesante es que la criptografía simétrica crea un problema NP con sus llaves: encontrar una llave de cifrado es casi imposible en un tiempo razonable, pero verificar si es correcta si se tiene el tiempo original es muy fácil.

En los próximos artículos hablaremos específicamente de algunos de estos problemas, sobre todo aquellos en los que la criptografía asimétrica se basa.
