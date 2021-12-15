---
title: "Criptografía VS computación cuántica"
date: 2021-12-11
author: Héctor Patricio
tags: criptografía, quantum, matemáticas
comments: true
excerpt: "Se ha escuchado mucho sobre que la criptografía está completamente acabada si la computación cuántica tiene éxito. Entendamos si esto es verdad."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1120/v1639258127/anton-maksimov-juvnsky-wrkNQmhmdvY-unsplash_zfe4zr.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_320/v1639258127/anton-maksimov-juvnsky-wrkNQmhmdvY-unsplash_zfe4zr.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

> “If you are not completely confused by quantum mechanics, you do not understand it.” - Richard Feynman

La computación cuántica es una tecnología muy prometedora que lleva _décadas_ en gestación y cada vez la vemos más cerca. Una de las cosas que más llama la atención es la capacidad de cómputo que las computadoras cuánticas pueden tener, en este artículo aclararemos de qué se trata todo esto y **cómo se relaciona con la criptografía**, uno de los campos más afectados.

Si no has escuchado mucho sobre la computación cuántica, este video de una presentación dada por [Ignacio Cirac](https://www.xataka.com/investigacion/algun-dia-se-construye-ordenador-cuantico-plenamente-funcional-sera-gracias-parte-a-este-cientifico-espanol-hablamos-ignacio-cirac) nos da una introducción a lo que promete y las bases de funcionamiento.

<iframe width="560" height="315" src="https://www.youtube.com/embed/WJ3r6btgzBM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

---

Ahora veamos a más detalle cómo **computa una máquina cuántica** y entendamos por qué no _toda la criptografía está perdida_, aunque tuviéramos una computadora cuántica funcional hoy mismo.

## Principios de funcionamiento de una computadora cuántica

Hablemos un poco de los _principios físicos y matemáticos_ que hacen especial a una computadora cuántica.

### Superposición cuántica

Una computadora cuántica está basada en el [principio de superposición cuántica](https://es.wikipedia.org/wiki/Superposici%C3%B3n_cu%C3%A1ntica), que establece, en palabras comunes, que una partícula tiene magnitudes físicas (como la posición o el momento) indeterminadas hasta que se realiza una medición sobre ellas. La partícula se comporta como si tuviera todos los estados posibles, algunos con más probabilidad que otros. Una forma fácil en la que se ha mencionado este principio es que **"puede estar en dos lugares a la vez"**.

Lo que se escapa de nuestra comprensión común de la física es que esto de tener múltiples estados **desaparece cuando lo observamos**, se dice que su _función de onda_ colapsa, lo que significa que la partícula "se decide" por uno de los múltiples estados en los que podía estar. La función de onda es la ecuación que describe todas las "probabilidades" de cada estado.

El ejercicio mental del [Gato de Schrödinger](https://www.youtube.com/watch?v=lzxKZx7we4s) te puede ayudar a imaginarlo, pero en [este video puedes de Quantum Fracture](https://www.youtube.com/watch?v=9JlOmEEyTOU) te ayudará a profundizar más en la complejidad del tema y como no es tan sencillo como "puede estar en dos estados a la vez", sino en un número _infinito de estados_.

Este artículo te explicará el principio de superposición cuántica sin matemáticas avanzadas: [Superposición, una aproximación sin matemáticas avanzadas a la motivación de la mecánica cuántica](https://www.elclaustro.edu.mx/agnosia/index.php/component/k2/item/427-superposicion-una-aproximacion-sin-matematicas-avanzadas-a-la-motivacion-de-la-mecanica-cuantica).

**Resumen:** Una particula como un átomo, un electron o un fotón, puede poseer múltiples estados físicos a la vez, con diferentes combinaciones entre todos sus posibles estados, dando lugar a _una infinidad de estados posibles_. Las probabilidades de cada estado están contenidas en su _función de onda_, y cuando medimos (miramos) una partícula se define en un estado de todos los posibles.

### Amplitud de onda y Qubits

Cada uno de los estados posibles de una partícula y sus probabilidades están representados en lo que se llama su **amplitud**. En el caso de la computación cuántica, nos interesa si una partícula _representa un cero o un uno_. Por esto, un **Qubit** (un bit cuántico) está representado por una amplitud de onda, que se puede entender parcialmente como la probabilidad de que ese bit sea cero o uno. Un qubit está caracterizado por dos amplitudes: una para el estado **cero** y otra para el estado **uno**. Estas amplitudes son números complejos, números que tienen un parte real y una parte imaginaria, como `2 + 3i`, por ejemplo.

Una _palabra_ o conjunto de qubits está representado por **2^n amplitudes**, donde n es el número de qubits. Así que en una palabra de 8 bits, tenemos 256 amplitudes de onda. Y aquí está el secreto de por qué la computación cuántica puede ser tan poderosa: **con sólo _n_ objetos (qubits), puedes almacenar y procesar 2^n números complejos, mientras que en una computadora clásica necesitarías 2^n espacios de memoria**.

### Compuertas cuánticas

Una compuerta cuántica es el equivalente cuántico a la compuertas lógicas clásicas. Son una serie de transformaciones que se le aplica a las amplitudes que caracterizan nuestro conjunto de qubits para obtener los resultados deseados.

Después de aplicarle un serie de compuertas cuánticas a los qubits, lo que se conoce como un **circuito cuántico**, se realiza una medición sobre uno o varios qubits para saber el resultado.

Las compuertas se comportan como multiplicaciones de matrices y vectores de gran tamaño, que serían imposibles de hacer para computadoras comunes, pero en la computadora cuántica se realizan mediante manipulaciones físicas que equivalen a estas transformaciones de matrices gigantescas.

No vamos a entrar en profundidad en este tema, pero si quieres leer más, [este artículo te puede servir](https://josueacevedo.medium.com/computaci%C3%B3n-cu%C3%A1ntica-compuertas-o-circuitos-cu%C3%A1nticos-27910f5338c8).

### Aceleración cuántica

Gracias a las cualidades de las computadoras cuánticas antes descritas, es posible resolver algunos problemas de la computación mediante nuevos algoritmos cuánticos que reducen el tiempo esperado de ejecución de O(2^n) a O(n^k), siendo _k_ una constante. Es decir: **aceleran la resolución de algunos problemas exponencialmente**.

Ahora que tenemos los conceptos más básicos de cómo funciona la computación cuántica y por qué puede ejecutar muchos más cálculos, hablemos de de algunas amenazas que presenta contra la criptografía.

## El algoritmo de Shor

Uno de los problemas en los que está basada la criptografía asimétrica actual, es el problema de la factorización de números primos, es decir, encontrar los componentes primos de un número entero. _Creemos_ que encontrar los factores de un número lo suficientemente grande es casi imposible para nuestras computadoras clásicas actuales, incluso las más poderosas.

El **algoritmo de Shor**, propuesto en 1995, traslada el problema de la factorización a otro problema difícil de las ciencias de la computación: encontrar el periodo de una función exponencial. Aquí puedes encontrar una explicación más a profundidad de esta transformación: [Period Finding](https://quantum-computing.ibm.com/composer/docs/iqx/guide/shors-algorithm#period-finding).

Lo importante de esta transformación es lo siguiente: **para una computadora cuántica, el problema de encontrar el periodo de una función exponencial no es tan difícil**. Una computadora cuántica resuelve este problema con una complejidad de O(log n) aproximadamente, ya que existen circuitos cuánticos que permiten encontrar el periodo de la función exponencial.

Esto significa que cuando una computadora cuántica tenga los suficientes qubits para representar los números que se usan en la generación de llaves asimétricas, la mayor parte de la criptografía asimétrica actual dejará de ser útil.

## El algoritmo de Grover

Buscar un elemento que cumpla cierta condición en un conjunto es uno de los problemas que nos ayudarían a romper la criptografía actual. Por ejemplo, imagina que tienes un texto cifrado con AES con una llave de 128 bits. Si quieres romper la seguridad, vas a tener que probar 2^128 llaves en promedio para encontrar la correcta.

El [algoritmo de Grover]() permite acelerar esta operación de manera cuadrática, es decir, te tomaría en promedio la raíz cuadrada de _n_ encontrar el elemento que cumpla con la condición. En el caso del ejemplo anterior te tomaría en promedio 2^(128/2) = 2^64 operaciones.

Lo mismo podría pasar para todos cifrados simétricos (que usan la misma llave para cifrar y descifrar) y hasheados, el ataque consistiría en un estilo de fuerza bruta más inteligente o _cuadráticamente más rápida_.

Sin embargo, como podrás notar, esto no es un problema tan grande, ya que para mantener el mismo nivel de seguridad que tenemos actualmente **bastaría con duplicar el tamaño de las llaves usadas**.

Esto seguirá siendo así mientras no se descubran debilidades en los algoritmos de cifrado simétricos o en las funciones de comprensión de los hashes que usamos.

## Criptografía post-quantum

Debido a las amenazas que presenta la computación cuántica a la criptografía de llave pública gracias al algoritmo de Shor, los criptográfos están manos a la obra diseñando nuevos algoritmos basados en otros principios aún no amenazados por la computación cuántica.

Algunos ejemplos que se ven prometedores son:

- Entramados (Lattice Cryptography)
- Códigos de corrección de errores (Error-correcting codes)
- Multivariada (Multivariate cryptography)

La explicación de cada uno de estos posibles caminos para la criptografía la dejaremos para otro artículo, déjanos un comentario si te interesa alguna en especial.

## Conclusión

La criptografía cuántica acelera la capacidad de cómputo, pero además es fundamentalmente _diferente_  de la computación clásica, lo que permite resolver problemas con otros métodos imposibles de alcanzar con la computación actual.

Pero no toda la **criptografía actual esta destinada a perderse con el avance de las computadas cuánticas**, solamente la criptografía asimétrica y toda aquella basada en la factorización de números primos.

Ciertamente, la criptografía simétrica se ve menguada por el poder de cómputo y los algoritmos cuánticos, pero no lo suficiente para darla por perdida, sino que bastará con fortalecerla con el mismo poder de cómputo cuántico.

Finalmente, los investigadores ya están trabajando en formas para sustituir lo que se va a romper.

