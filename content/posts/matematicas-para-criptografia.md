---
title: "Matemáticas para criptografía"
date: 2021-12-25
author: "Héctor Patricio"
tags: ['criptografía', 'matemáticas', 'álgebra']
description: "Veamos qué conocimientos matemáticos requieres para entender los algoritmos criptográficos, cómo funcionan y, en su caso, avanzar para que puedas diseñar los tuyos."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1120/v1639258119/anton-maksimov-juvnsky-hlc-O87pjUs-unsplash_gvco8p.jpg"
draft: false
---

¿Quieres entender por qué los algoritmos criptográficos pueden _prometer_ seguridad? Todos están basados en operaciones matemáticas, problemas difíciles de resolver, probabilidad y estadística.

Veamos un plan de estudios de matemáticas que podrías usar para adquirir las habilidades matemáticas necesarias para entender mejor los algoritmos criptográficos.

## Básico básico

Empecemos por los fundamentos más profundos que debes tener, que hasta pueden parecer obvios. Lo importante es que tengas _la seguridad de que los dominas_ y si no, te proporcionamos algunos recursos para que los repases.

### Álgebra

Es necesario conocer los procedimientos algebraicos a fondo porque en esto se basa la resolución de problemas de muchas otras áreas. Además la factorización es uno de los problemas más importantes de la criptografía actual, y aquí es donde aprenderás el concepto básico en práctica. Si sientes que te falta aprender un poco, puedes tomar estos cursos:

- [Álgebra 1 - Khan Academy](https://www.khanacademy.org/math/algebra)
- [Álgebra 2 - Khan Academy](https://www.khanacademy.org/math/algebra2)
- [Algebra básica - UNAM](https://www.coursera.org/learn/algebra-basica)
- [Curso de Álgebra en Platzi](https://platzi.com/cursos/algebra/)

### Probabilidad y estadística

Siempre que hablamos de que un algoritmo es seguro, lo decimos basados en la probabilidad de que alguien pueda encontrar una solución a un problema muy difícil en un _número de intentos razonable_.

Por ejemplo: confiamos en que la probabilidad de que alguien rompa un cifrado es cercana a cero, pero realmente esta probabilidad nunca es cero absoluto, sino algo como **1/2^128** por intento, pero alguien motivado podría hacer _miles de millones_ de intentos. Para poder calcular estas probabilidades hay que entender lo básico de probabilidad y estadística.

La probabilidad también te ayudará a entender lo que es una **distribución de probabilidad**, que es muy importante tanto para atacar algoritmos criptográficos como para verificar que las salidas de estos son seguras.

Puedes aprender un poco de esto en los siguientes cursos:

- [Probabilidad y estadística - Khan Academy](https://www.khanacademy.org/math/statistics-probability)
- [Estadística y Probabilidad - UNAM](https://www.coursera.org/learn/estadistica-probabilidad)

## Matemáticas discretas

Me atrevería a decir que esta es la rama **más importante de matemáticas** que debes de conocer como programador y como criptógrafo. La mayoría de los operaciones criptográficas y de algoritmos de programación están basadas en el conocimiento que aprenderás aquí. [Ya hemos mencionado](https://blog.thedojo.mx/2019/12/25/las-matematicas-que-debes-saber-para-programar.html#l%C3%B3gica-matem%C3%A1ticas-discretas) que las matemáticas discretas son el estudio de las cosas que se pueden contar, sean finitas o infinitas, a diferencia de las matemáticas continuas que estudian los números reales o cosas que son continuas, incontables y sin divisiones claras.

A continuación te listamos algunos de los temas que debes dominar o por lo menos conocer bien.

### Lógica

La lógica tiene la intención de formalizar el razonamiento de tal manera que lo podamos estudiar, entender y aplicar a otras áreas.

En este tema se habla de cosas como tablas de verdad, lógica proposicional, deducción, [teorías y lógica de primer orden](https://www.fing.edu.uy/~amiquel/fundamentos/teoriasymodelos.pdf), etc.

### Teoría de números

La teoría de números trata acerca de los números enteros, sus propiedades, operaciones y relaciones. Esta es **la base de varios problemas difíciles que sirven para crear los algoritmos criptográficos modernos**. En esta rama se estudia la divisibilidad, los números primos, la aritmética modular y los algoritmos relacionados con estas operaciones.

Si no vas a estudiar nada más, entender los temas de un curso de teoría de números enfocado en criptografía es suficiente para no sentirte sin rumbo. Estos cursos pueden ayudarte a aprender lo que necesitas:

- [Number Theory for Cryptography](https://www.coursera.org/learn/number-theory-cryptography)
- [Temario con Bibliografía y tareas del curso de Teoría de Números del CIMAT](http://personal.cimat.mx:8181/~hgallegos/teaching/teoriaDeNumeros/)
- [Mathematical foundations of cryptography](https://www.coursera.org/learn/mathematical-foundations-cryptography)
- [Yet Another Introductory Number Theory Textbook - Cryptology Emphasis](https://math.libretexts.org/Bookshelves/Combinatorics_and_Discrete_Mathematics/Yet_Another_Introductory_Number_Theory_Textbook_-_Cryptology_Emphasis_(Poritz))

### Combinatoria

Esta sub-rama de las matemáticas discretas tiene que ver con el _conteo, combinaciones y arreglos de objetos en estructuras discretas_ (con objetos claramente separados) como los grafos y conjuntos. Normalmente estas estructuras discretas contienen números, pero podrían contener palabras, textos, frases. La combinatoria incluye el conteo de objetos y combinaciones que llevamos a a cabo en probabilidad y estadística: las operaciones de combinación y permutación.

Algunos recursos que te ayudarán a aprender combinatoria a fondo se encuentran aquí: [Combinatorics and Discrete Mathematics](https://math.libretexts.org/Bookshelves/Combinatorics_and_Discrete_Mathematics) que tiene un conjunto de libros sobre combinatoria con diferentes enfoques.

### Cursos de matemáticas discretas generales

Algunos cursos y temarios que puedes tomar son:

- [Curso de matemáticas discretas](https://compilandoconocimiento.com/discretas/)
- [Temario sobre matemáticas discretas para Maestría en Ciencias de la Computación](https://posgrados.inaoep.mx/archivos/PosCsComputacionales/Curso_Propedeutico/TEMARIOS/2_MateDiscretas-VersionGeneral.pdf)

### Geometría analítica

Conocer las propiedades matemáticas de los objetos geométricos te ayudará a comprender intuitivamente algunas de los problemas difíciles en los que está basada la criptografía.

Algunos cursos que puedes tomar:

- [Trigonometría y geometría analítica - UNAM](https://www.coursera.org/learn/https://www.eusal.es/eusal/catalog/book/978-84-1311-463-7trigonometria)

## Álgebra lineal

El álgebra lineal tiene que ver con el estudio de ecuaciones lineales (que pueden ser graficadas en el plano cartesiano con una recta), sus soluciones y su tratamiento a través de vectores y matrices.

Muchas de las técnicas utilizadas en álgebra lineal son ocupadas en criptografía para crear algoritmos seguros que sean imposibles de revertir sin conocer la llave correcta. Un ejemplo es el algoritmo Rijndael, el actual AES.

Algunos recursos que te ayudarána a aprender matemáticas discretas son:

- [Aprendiendo Python con Álgebra Lineal](https://www.coursera.org/projects/aprendiendo-python-con-algebra-lineal)
- [Fundamentos de álgebra lineal](https://www.edx.org/course/fundamentos-de-algebra-lineal-2?index=product&queryID=4f34318ca69382d83eb24655d433f655&position=1)
- [Cómo funciona AES (Rijndael)](http://buzzard.ups.edu/courses/2013spring/projects/berger-aes-ups-434-2013.pdf)

## Opcionales

Si quieres avanzar a campos muy adelantados de la criptografía, debes estudias campos aún más específicos de las matemáticas discretas como:

- Teoría de grupos
- Teoría de grafos
- Retículas (algo muy importante para la criptografía post-cuántica)

## Cursos completos

Para finalizar, te quiero presentar recursos que tienen un conjunto completo básico de todas las matemáticas necesarias para entender los algoritmos criptográficos modernos.

- [MANUAL DE CRIPTOGRAFÍA: FUNDAMENTOS MATEMÁTICOS DE LA CRIPTOGRAFÍA PARA UN ESTUDIANTE DE GRADO](https://www.eusal.es/eusal/catalog/book/978-84-1311-463-7) - Tiene apartados para todos los tipos de algoritmos criptográficos usados en la actualidad, explicando su soporte matemático. Si quieres profundizar en algún tema de estos, podrías tomar el curso específico que sugerimos aquí.
- [Especialización en matemáticas discretas en Coursera](https://www.coursera.org/specializations/discrete-mathematics) - Tiene todos los temas relacionados con matemáticas para computación y criptografía divididos en varios cursos, lo puedes tomar de manera gratuita.
- [Mathematical foundations of Cryptography](https://www.coursera.org/learn/mathematical-foundations-cryptography?) - Tiene todos los temas necesarios para entender la criptografía, incluyendo los temas selectos de todas las matemáticas para ir directo al grano. Esto requerirá que tengas cubierto las matemáticas básicas para no perderte.
- [Temario de maestría en seguridad de la ISICAL](https://www.isical.ac.in/~rcbose/mtechCrS.pdf) - Tiene todos los cursos que alguien debería de tomar para especializarse en ciberseguridad, con temarios completos y bibliografía, lo que te puede servir como una guía si lo que prefieres es aprender de los libros.

Bonus: [Cryptogaphy, Boolean Functions and related problems](https://www.coursera.org/learn/cryptography-boolean-functions)

## Conclusión

Como podrás observar, hay una gran cantidad de recursos para aprender lo necesario para entender la criptografía a fondo, desde sus bases matemáticas. Puedes usar estas recomendaciones como guía, o ver los temas y buscar tus propios recursos para seguir aprendiendo. Si tienes alguna recomendación no dudes en compartirla con nosotros para poder actualizar nuestra lista y cada vez hacerla mejor.