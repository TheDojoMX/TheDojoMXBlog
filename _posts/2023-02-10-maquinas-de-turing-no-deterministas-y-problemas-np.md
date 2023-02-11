---
title: "Máquinas de Turing no deterministas y problemas NP"
date: 2023-02-08
author: Héctor Patricio
tags: turing ntm non-deterministic
comments: true
excerpt: "Hablemos de la relación que existe entre las máquinas de Turing no deterministas (NTM), la complejidad y los problemas NP."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1675835077/pawel-czerwinski-tMbQpdguDVQ-unsplash_amld7p.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1675835077/pawel-czerwinski-tMbQpdguDVQ-unsplash_amld7p.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

En el artículo anterior hablamos de las clases de complejidad y su relación con la criptografía. Hablamos brevemente de los problemas NP y de dijimos que pueden ser resueltos por una máquina de Turing no determinista en un tiempo razonable (complejidad polinomial).

En este artículo vamos a entender qué son las máquinas de Turing no deterministas, pero empecemos entendiendo la diferencia entre determinismo y no determinismo.

## Determinismo y no determinismo

En la física y las ciencias existen básicamente dos tipos de sistemas basados en el conocimiento que podemos tener de su comportamiento en un momento dado.

El primer tipo es el de los sistemas deterministas, en el que saber el estado actual del sistema y el evento (o la entrada del sistema) nos permite predecir el estado futuro del sistema, sin errores y con una precisión infinita. En estos sistemas existen una serie de reglas que no se pueden romper y que nos dan la capacidad saber exactamente lo que sucederá. Estos sistemas son casi siempre simplificaciones del mundo real o sistemas creados y diseñados por el hombre. Ejemplos de estos sistemas son:

- El juego de la vida
- El ajedrez
- El juego de Go
- Casi todos los problemas que analizamos en un clase de física son tratados como deterministas, por ejemplo, el movimiento de un proyectil, una mesa de billar, etc., aunque no lo sean realmente, se tratan como tales para simplificar el análisis.

El segundo tipo son los **sistemas no deterministas o estocásticos**. En estos sistemas no tenemos la información suficiente para poder predecir estados futuros del sistema de manera precisa, solamente podemos predecir probabilidades. Algunos ejemplos de estos sistemas son:

- El clima
- El comportamiento de una persona
- El comportamiento de un mercado de un mercado financiero
- Una selección aleatoria de elementos de un conjunto

En pocas palabras, en un sistema determinista podemos predecir la salida si conocemos la entrada con toda seguridad. En un sistema no determinista o estocástico sólo podemos dar una probabilidad de que algo suceda en el mejor de los casos.

## Máquinas de Turing deterministas

Si no sabes lo que es una máquina de Turing tradicional, una de las mejores explicaciones que hemos encontrado está en el libro ["La Mente nueva del Emperador"](/assets/pdfs/la_mente_nueva_del_emperador.pdf){:target="_blank"} de **Roger Penrose**.

Lo que debes saber es que estas representan un modelo universal de computación, todo lo que se puede computar (calcular, o conocer con certeza) se puede representar en una máquina de Turing. Te la puedes imaginar como una máquina que lee de una cinta infinita que contiene tanto las instrucciones como los datos de entrada. ¿Te suena? Es como funcionan las computadoras actualmente: el ejecutor es el CPU y la cinta es la memoria.

La máquina de Turing como se definió es determinista, es decir siempre para el la misma entrada obtendremos la misma salida. En cada punto de su cálculo la máquina de Turing sabe **exactamente qué hacer**.

Ahora hablemos de otro modelo de computación: las máquinas de Turing no deterministas.

## Máquinas de Turing no deterministas

Apliquemos el concepto del "no determinismo" al modelo de computación de lo que acabamos de hablar. Recordemos que la en la máquina de Turing tradicional, para un mismo estado y una misma entrada de datos (o eventos), siempre obtendremos la misma acción.
En contraparte, una máquina no determinista puede tener múltiples acciones para un mismo estado y una misma entrada o evento.

Esto implica que este tipo de computación también puede tener múltiples resultados posibles para un mismo conjunto de entrada.

El comportamiento de una máquina de Turing no determinista es hasta cierto grado impredecible. Incluso con las mismas entradas y estados, la máquina puede devolver diferentes resultados en diferentes ejecuciones.

Estas máquinas también fueron definidas (o más bien, mencionadas) en el mismo documento en que Turing definió las máquinas tradicionales: [ON COMPUTABLE NUMBERS, WITH AN APPLICATION TO THE ENTSCHEIDUNGSPROBLEM](/assets/pdfs/Turing_Paper_1936.pdf){:target="_blank"}. A estas él las llamó **máquinas de selección** (choice machines o *c-machine*). La definición más formal la podemos encontrar en  un documento escrito por Rabin y Scott en 1959: [Finite Automata and Their Decision Problems](/assets/pdfs/rabin_scott_1959.pdf){:target="_blank"}, en el que se habla de Autómatas Finitos No Deterministas (AFND), una especialización finita de las máquinas de Turing.

A diferencia de los sistemas no deterministas de los que hablamos arriba, las máquinas de Turing no deterministas no es que tengan una probabilidad de pasar de un estado a otro, sino que la máquina puede "seleccionar" una transición de un estado a otro. En el documento de Turing mencionado anteriormente, se menciona que estas máquinas son "operadas" por un humano, que **elige** qué camino tomar, por eso las llamó máquinas de selección. En referencias más modernas no se especifica el mecanismo de selección.

Para una misma entrada una máquina de Turing no determinista puede tener múltiples salidas posibles, algunas de ellas válidas y otras no. Para que una máquina de Turing encuentre el resultado correcto, **debe probar todas las posibles salidas y seleccionar la correcta**.

Una NTM (*Non-deterministic Turing Machine*, así la llamaremos a partir de ahora) es una construcción matemática que no existe en la vida real, es decir, no hay computadora que funcione como una NTM.

## Relación entre las máquinas de Turing deterministas y no deterministas

Se ha demostrado que para cada máquina de Turing no determinista existe una máquina de Turing determinista equivalente. Lo malo es que esta máquina de Turing determinista necesita **exponencialmente** más nodos o *pasos*. Por ejemplo, si una NTM necesita tiene 100 posibles estados, entonces la máquina de Turing equivalente necesitará aproximadamente 2^100 estados.

Y aquí es donde entra la relación con los problemas NP.

## Relación con los problemas NP

Como te darás cuenta, las NTM tienen mucho que ver con la combinatoria, porque necesitan probar todas las posibles combinaciones de estados y transiciones para encontrar la solución correcta.

Si ejecutáramos una NTM en una computadora, tendríamos que probar cada uno de esos estados. Esto es exactamente lo mismo que sucede con muchos problemas NP o NP-completo, para encontrar una solución se tienen que probar todas las posibles combinaciones en un conjunto de elementos.

Las siglas NP significan *Non-deterministic Polynomial* (polinomial no determinista), y esto significa que en una NTM hay por lo menos un camino que resuelve el problema en un tiempo polinomial. *El problema es saber cuál de todos los caminos*.

Y de ahí viene su nombre. Todos estos problemas tienen una solución que corre en tiempo polinomial, pero para encontrarla tenemos que *adivinar* o *probar todas las combinaciones*.

## Conclusión

Ahora que sabemos como funciona una máquina de Turing no determinista, que es una construcción teórica que nos sirve para hacer experimentos del pensamiento y  además que tienen una relación muy estrecha con la teoría de la complejidad y los problemas NP.
