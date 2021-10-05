---
title: "A Philosophy of Software Design: Los módulos deben ser profundos"
date: 2020-03-02
author: Héctor Patricio
tags: módulo PoSD ousterhout complejidad función
comments: true
excerpt: "Veamos algunos lineamientos para el diseño de funciones/clases/módulos que ayudarán a reducir la complejidad de tus sistemas de software."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1583214655/IMG_3431_xcydpt.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_200/v1583214655/IMG_3431_xcydpt.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Para reducir la complejidad de los programas es importante tener técnicas definidas. La primera que vamos a analizar es la organización y separación de código a alto nivel, es decir separación en módulos.

## Por qué es importante la separación

Antes de empezar a hablar de cómo deberíamos diseñar nuestros módulos hablemos de por qué es importante la separación.

La mejor forma de resolver un problema complejo es mediante _la descomposición_ del problema en problemas más sencillos. Estos problemas se resuelven individualmente, idealmente de de manera independiente en un módulo por separado para cada uno. De esta manera podemos hacer software más mantenible y fácil de entender. Incluso se puede dividir mejor el trabajo.

La división del problema permite además **ocultar** información no relevante para el problema en cuestión.

Esta división del trabajo es diferente dependiendo del paradigma del lenguaje de programación que usemos, así que veamos a qué nos referimos con un **módulo**.

## ¿Qué es un módulo?

Una definición fácil y amplia de "módulo" dada por ["A Philosophy of Software Design"](https://amzn.to/2H92nwA) es: _todo aquello que agrupe código, proveyendo separación de funcionalidad_, es decir que agrupe comportamiento en detrás de una _interfaz_.

Un módulo puede ser una función, una clase, un paquete o cosas similares dependiendo del lenguaje de programación. Un módulo incluso puede ser una API HTTP u otro programa.

Como resumen: **un módulo permite hacer _algo_ mediante una interfaz.**

Ahora bien, ¿qué es la interfaz de un módulo?

## Interfaces

Ya hemos hablado sobre [lo que es una interfaz](https://www.youtube.com/watch?v=n8MxyHG0j3Q&t), pero para resumir: es el punto en donde un sistema, en este caso específico, un módulo, se encuentra con otro (otro módulo o código que lo usa).

Un módulo tiene una interfaz que permite a otras partes del sistema usarlo. Usaremos el caso más sencillo, una función. La interfaz de una función es su firma: su nombre, los parámetros que recibe y lo que devuelve.

Veamos un ejemplo:

```python
archivo = open("my_file.md", "w") # Devuelve un apuntador a un archivo abierto
```

La interfaz de la función es su nombre `open` (nos permite identificarla y comunica información sobre lo que hace), el nombre del archivo como primer parámetro y el modo de operación en el segundo.

Dependiendo de la forma de agrupar la interfaz de los módulos varía, pero recuerda esto: **la interfaz es la parte visible del módulo hacia otros módulos**.

## Diseño de módulos

Aquí entramos en lo importante: los módulos deberían ser lo más profundos posible.

¿A qué nos referimos con un módulo profundo? Puedes imaginarte un módulo como un rectángulo en el que su interfaz es el largo de la base y su funcionalidad es la altura. Un módulo profundo es aquel que tiene una altura elevada comparada con el largo de la base.

Observa la siguiente imagen:

![Módulos profundos vs superficiales](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_500/v1630554161/Ilustracio%CC%81n_sin_ti%CC%81tulo_zchwj3.png)

Un módulo profundo tiene una **interfaz sencilla** o fácil de usar para la mayoría de los casos de uso y provee de mucha funcionalidad, hace mucho por ti.

Un módulo superficial tiene una interfaz compleja o difícil de usar y provee poca funcionalidad.

Esto no es absoluto: la relación entre la complejidad de la interfaz es relativa a la funcionalidad que provee, por ejemplo, si un módulo hace muchas cosas por ti, puede que requiera muchos datos. La relación interfaz/funcionalidad debe ser razonable para considerar que el módulo es profundo.

Abrir archivos en la mayoría de los lenguajes es un ejemplo de una función profunda: con una interfaz muy pequeña (el nombre y el modo), la función se encarga de todos los detalles de implementación de apertura y creación del archivo. No te debes de preocupar por cosas como el sistema de archivos, el guardado físico en el disco, por verificar si hay memoria, etc.

En el caso contrario, los _getters_ y _setters_ que se acostumbra usar en algunos lenguajes de programación (Java) son ejemplo de funciones poco profundas, generalmente no hacen algo más que devolver el valor de la propiedad.

Ejemplo: Piensa en un aparato electrónico. En una televisión, sus control remoto te permiten acceder a las funcionalidades de encender el panel de iluminación, captar la señal del canal, decodificarlo y saltar entre diferentes canales, todo sin preocuparte tú por los detalles. Sólo la usas y ya. Mientras más detalles de implementación oculte es más fácil de usar.

## Ventajas de los módulos profundos

Encontrar un equilibrio entre la cantidad de código que metes en un módulo y la interfaz que expone tiene varias ventajas:

- El código se puede re-usar en otras partes del sistema
- Evitas la acumulación de interfaces, es decir, tener demasiadas interfaces (funciones, clases o módulos) que tienes que aprender a usar y que hacen poco por ti
- La expansión de cambios (tener que tocar muchos lados del sistema para hacer un cambio relativamente pequeño)

Finalmente, recuerda que una de las funciones que proveen los módulos es _ocultar_ la complejidad. ¿Cuántas veces has visto lo que hacen las funciones prefabricadas de tu lenguaje de programación? Es probable que ninguna. Los módulos profundos te permiten ocultar mayor cantidad de información, hace más fácil trabajar con ellos y simplifica el sistema en general.
