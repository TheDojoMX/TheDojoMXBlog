---
title: "20 bibliotecas de Python que deberías estar usando"
date: 2021-12-01
author: Héctor Patricio
tags: python books bibliotecas
comments: true
excerpt: "Exploremos cinco bibliotecas que el libro del '20 Python Libraries You Aren't Using' recomienda y que te podrían servir para tu próximo desarrollo en Python."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1120/v1638419376/hans-isaacson-rlqkZ1DlOnU-unsplash_rsaim0.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_340/v1638419376/hans-isaacson-rlqkZ1DlOnU-unsplash_rsaim0.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

El libro ["20 Python Libraries You Aren't Using (But Should)"](https://freecomputerbooks.com/20-Python-Libraries%20You-Are-Not-Using-But-Should.html#downloadLinks) de [Caleb Hattingh](https://github.com/cjrh) es un lectura corta que recomienda bibliotecas de Python muy útiles que pueden ayudarte a desarrollar software de manera más efectiva y rápida.

![Portada de 20 python libraries](https://res.cloudinary.com/hectorip/image/upload/v1638418876/20_python_rlf1b2.png){: .align-center}

Veamos las 5 que me parece más importante conocer y tú puedes leer el libro para ver el detalle y entender las otras 15.

## En la biblioteca estándar de Python

Estas bibliotecas no las tendrás que instalar porque vienen con todas las instalaciones normales de Python, pero son poco usadas.

1. [collections](https://docs.python.org/3/library/collections.html) - Contiene un conjunto de clases y funciones para trabajar con estructuras de datos especializadas en alguna función. Por ejemplo provee de diccionarios que mantienen el orden, listas de doble acceso, tuplas nombradas y hasta un diccionario especializado en contadores. En el canal de YouTube hemos hecho algunos videos sobre estos contenedores, puedes verlas aquí: [Python Collections](https://www.youtube.com/watch?v=DrhHkPI7spU&list=PLfeFnTZNTVDMDCoBzZ6XynugZTFDzEjiB)

2. [sched](https://docs.python.org/3/library/sched.html) - Trabaja con tareas programadas de manera sencilla, este módulo nos da la clase `scheduler` que nos permite programar, encolar y ejecutar tareas entre otras cosas.

## Bibliotecas desarrolladas por la comunidad

1. [hug](https://www.hug.rest/) - Es una biblioteca de Python que nos permite crear **API**'s en el sentido general de la palabra. Nos permite crear interfaces de tres tipos: de consola, de módulo y REST. Contiene una serie de utilidades para que puedas exponer tu API de la manera más sencilla posible, documentación automática, aprovechamiento de las sugerencias de tipos de Python, entre muchas otras cosas. Esta es una Biblioteca que realmente recomiendo si quieres crear una API verdaderamente rápido.

2. [arrow](https://arrow.readthedocs.io/en/latest/) - te permite manejar las fechas y tiempos de mejor manera que sólamente con los tipos de datos nativos de Python. Centraliza todas las funciones de fechas y tiempos en vez de estar repartidas en varios módulos, trabaja por default con fechas y horas que incluyen la zona horaria (UTC), soporta el estándar [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601), tiene funciones de "humanización" de fechas y tiempos, etc.

3. [boltons](https://boltons.readthedocs.io/en/latest/) - contiene una gran colección de tipos de datos y funciones que los creadores y contribuidores piensan que le hacen falta a la biblioteca estándar de Python. Para Octubre de 2021 tenía _83 tipos de datos y 171 funciones_, hablemos de tamaño. Las utilidades que provee son muy variadas, y te pueden ayudar para una gran cantidad de casos. Por ejemplo, tiene utilidades para colecciones, para manejo de caché, trabajo con tipos de datos, utilidades para debuggear, ente muchas otras ayudas.


## Conclusión

La verdad es que cada una de las bibliotecas arriba mencionadas debería tener su propio artículo o video, esperamos que podamos extender sobre algunas de ellas en el futuro. Por lo mientras, puedes leer el libro y aprender más sobre las bibliotecas que recomienda, sólo ten en cuenta que algunas pueden estar sin mantenimiento por la edad que tiene el libro. Aquí te dejamos el resumen que hicimos en el canal y con suerte [en este link puedes descargar](https://pepa.holla.cz/wp-content/uploads/2016/10/20-python-libraries-you-arent-using-but-should.pdf) el libro en PDF, aunque es un libro que puedes seguir leyendo en Safari, la biblioteca online de O'Reilly o leer gratuito en línea: [aquí](https://www.oreilly.com/content/20-python-libraries-you-arent-using-but-should/). Déjanos un comentario si quieres que hagamos el análisis de alguna biblioteca en el futuro.

<iframe width="560" height="315" src="https://www.youtube.com/embed/T5xHzP1Ex5s" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>