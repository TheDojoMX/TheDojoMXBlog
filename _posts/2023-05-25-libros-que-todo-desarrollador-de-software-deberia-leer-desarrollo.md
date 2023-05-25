---
title: "Libros que todo desarrollador de software debería leer: desarrollo"
date: 2023-05-25
author: Héctor Patricio
tags: libros desarrollo-de-software
comments: true
excerpt: "Hablemos ahora de los libros relacionados con desarrollo de software que te ayudarán a mejorar tu carrera y a tener mejores proyectos."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,e_oil_paint:19,w_1400/v1684180864/A2F74C59-DAC0-411A-970A-0BF85AD55F91_1_201_a_t4llcq.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,e_oil_paint:19,w_400/v1684180864/A2F74C59-DAC0-411A-970A-0BF85AD55F91_1_201_a_t4llcq.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Ya hablamos en un [artículo anterior](https://blog.thedojo.mx/2023/05/13/libros-que-todo-desarrollador-de-software-deberia-leer-cs.html) sobre
los libros que te haría bien leer en el tema de ciencias de la computación.
Ahora vamos a hablar sobre el tema de desarrollo de software, cómo crear mejor software y con mejor calidad.
En este artículo también se incluyen libros sobre ingeniería de software por ser la disciplina más
confiable para crear software de calidad.

Empecemos con las recomendaciones, espero que te sirvan.

### A Philosophy of Software Design - John Ousterhout

[![Portada de a Philosophy of Software Design](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_350/v1684113024/Screen_Shot_2023-05-14_at_19.10.08_ocrzmo.png){: .align-center}](https://web.stanford.edu/~ouster/cgi-bin/book.php){:target="_blank" rel="noopener"}

Este es un libro que te da muchos consejos sobre cómo crear bases de código que sean más fáciles de evolucionar, mantener y sobre todo, de entender. Está escrito por [John Ousterhout](https://web.stanford.edu/~ouster/cgi-bin/home.php), el creador de RAMCloud, TCL/TK y co-autor del algoritmo de consenso para sistemas distribuidos [Raft](https://raft.github.io/).

Es un libro muy práctico y corto, que da consejos concretos _sin grandes ínfulas de superioridad_ sobre cómo escribir mejor código. El tema principal es la complejidad, cuáles son sus síntomas y cómo puedes evitarla o manejarla. El libro se centra en _en la experiencia del autor_ tanto escribiendo código y haciendo sistemas, como enseñando a otros a hacerlo en su clase **"Software Design Studio"**.

Esto último (lo de dar clases) le da una visión privilegiada: ver los errores comunes que cometen los principiantes le permite atacar directamente los problemas en los que nos metemos por un mal **diseño**.

Ousterhout se centra en los temas que para mi son los fundamentales de desarrollo de software:

1. La complejidad y sus causas
2. La abstracción
3. La modularidad y los criterios para dividir un sistema en módulos
4. Ocultar información de forma efectiva
5. La mejor forma de comunicar información al resto del equipo

Si quieres darle una probada antes de comprarlo, puedes leer el [primer capítulo](https://web.stanford.edu/~ouster/cgi-bin/book.php){:target="_blank" rel="noopener"}.

Y en este blog tenemos varios artículos hablando de sus ideas, puedes buscarlos con la etiqueta [APoSD](https://blog.thedojo.mx/tags/#aposd){:target="_blank"}.

Puedes comprarlo aquí: [A Philosophy of Software Design](https://amzn.to/3q4NEwd){:target="_blank"}

### Making Software - Editado por Andy Oram & Greg Wilson

[![Portada de Making Software](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_350/v1684245311/Screen_Shot_2023-05-16_at_7.54.35_djc8uk.png){: .align-center}](https://www.oreilly.com/library/view/making-software/9780596808310/){:target="_blank" rel="noopener"}

En este libro se habla de las prácticas _comunes_ que **creemos que nos ayudarán** a desarrollar mejor software, pero desde el punto de vista del escepticismo. Se analizan estas prácticas y nos dice si realmente nos ayudan o no, y **por qué**, todo esto con base en estudios realizados a lo largo del tiempo en muchos equipos, junto con las opiniones de expertos en el tema.

Los resultados probablemente te sorprendan, pero hay que recordar que ninguna práctica se comporta de la misma manera universalmente, es decir, lo que te sirva a ti puede no servirle a otro equipo. Así que aunque es una buena guía, nada es una verdad absoluta.

Creo que este libro es **fundamental** para desarrollar una relación sana con las "buenas prácticas" y cuestionarte todas las cosas que te dicen respecto al desarrollo de software.

Puedes comprarlo aquí: [Making Software](https://amzn.to/3oxZHBK){:target="_blank"}

### Modern Software Engineering - Dave Farley

[![Portada de Modern Software Engineering](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_350/v1684993243/61qXAFawZVL._AC_UF1000_1000_QL80__mbrnes.jpg){: .align-center}](https://www.davefarley.net/?p=352){:target="_blank" rel="noopener"}

Escrito por un gran ingeniero de software con mucha experiencia, explica técnicas efectivas para la organización del trabajo y la liberación de software lo más rápido posible. Dave es un proponente muy fuerte de la entrega continua y de la automatización de pruebas, y en este libro explica las técnicas asociadas a estos temas.

Además explica por qué la ingeniería de software no tiene que ser una carga burocrática. La premisa básica es que toda práctica que no nos ayude a hacer mejor software más rápido, es una mala idea y no debería contar como "ingeniería".

Puedes comprarlo aquí: [Modern Software Engineering](https://amzn.to/3MzYXnD){:target="_blank"}

## The Mythical Man-Month - Frederick Brooks

[![Portada de The Mythical Man-Month](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_350/v1684992740/51Al66uQmcL._SX433_BO1_204_203_200__f2yws3.jpg){: .align-center}](https://en.wikipedia.org/wiki/The_Mythical_Man-Month){:target="_blank" rel="noopener"}

Frederick Brooks era un ingeniero de la computación que trabajó en el IBM System/360 y en el OS/360, sistemas muy grandes y que le dieron para después describir su experiencia en la serie de ensayos que conforman este libro.

Como te lo podrás imaginar, aprendió mucho en los proyectos que realizó, sobre todo de la administración de equipos. En estos ensayos podrás llevarte sus aprendizajes. El además es el autor de otros ensayos como "No Silver Bullet" y de la famosa frase:

> "Adding manpower to a late software project makes it later."

> "Añadir personal a un proyecto de software atrasado, lo atrasa más."

Puedes comprar el libro aquí: [The Mythical Man-Month](https://amzn.to/3q8IG1D){:target="_blank"}, pero también puedes leer la primera edición de forma gratuita aquí: [The Mythical Man-Month en la universidad de Virginia](https://web.eecs.umich.edu/~weimerw/2018-481/readings/mythical-man-month.pdf){:target="_blank"}.

### Refactoring - Martin Fowler

[![Portada de Refactoring](https://res.cloudinary.com/hectorip/image/upload/v1684994739/refact2_og8gz8.jpg){: .align-center}](https://martinfowler.com/books/refactoring.html){:target="_blank" rel="noopener"}

Uno de los grandes clásicos en el desarrollo de software, establece la importancia y la forma en la que puedes refactorizar tu código. Refactorizar significa cambiar la implementación de tu código, haciéndola mejor, sin cambiar su funcionamiento externo, o la función que provee.

Martin Fowler también es uno de los más grandes nombres en el campo del desarrollo de software por su gran experiencia tanto desarrollando software como escribiendo, por lo que puedes estar seguro de que sus consejos son de gran valor.

Puedes comprarlo aquí: [Refactoring](https://amzn.to/3osHZj6){:target="_blank"}

## Conclusión

Estos son los libros que pude pensar como las mejores recomendaciones para aprender desarrollo de software.

No incluyo deliberadamente el más famoso de todos por lo menos entre los desarrolladores latinoamericanos: Clean Code. ¿Por qué? Aunque dice cosas útiles, muchas son obvias, explicadas mejor en otros libros y además el tono de superioridad que tiene el autor es muy molesto. Quienes lo han interiorizado se creen mejores simplemente por conocer esos consejos, que (_aquí viene lo peor_) a veces son contraproducentes.

Si tienes alguna recomendación extra, puedes dejarla en los comentarios.
