---
title: "¿Son aplicables y prácticos los principios SOLID?"
date: 2023-06-17
author: "Héctor Patricio"
tags: ['solid', 'principios']
description: "Los principios SOLID son algo que se considera como 'axiomas' de las buenas prácticas del software. Pero, ¿son realmente útiles?"
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1686348260/conrad-crawford-k3s7LZzX5xU-unsplash_p4cdwc.jpg"
draft: false
---

Los **principios SOLID**, se enseñan como verdades incuestionables sobre el buen desarrollo de software. Aunque, justo por la educación, antes era completamente partidario de estos, con el tiempo me fui dando cuenta de varias de las fallas que presentan.

En este artículo te voy a hablar de las fallas generales como conjunto, pero también es un índice para una serie de artículos que escribí sobre cada uno de ellos, analizándolo a profundidad.

## Ambigüedad

Cuando buscas la explicación sobre cómo aplicar alguno de estos principios, normalmente encuentras muchas explicaciones diferentes. Algunas de estas explicaciones se contraponen, siguen siendo ambiguas, o de plano no se entienden.

Con el principio que más pasa es con el "Single Responsibility" (SRP), en el cuál diferentes personas no nos ponemos de acuerdo respecto a lo que una "Responsabilidad" significa. Pero también pasa con la aplicación de los demás principios a diferentes entornos de programación.

## Complican exageradamente el código

La aplicación sin razonamiento profundo de estos principios puede complicar el código de manera exagerada, sobre todo en lenguajes inflexibles o con sistemas de tipos complicados (sí, te estoy viendo a ti, **Java**), que justo es donde más se aplica.

El ejemplo más claro de esto es el "Dependency Inversion Principle", que te lleva a hacer cosas bastante raras en el código para lograrlo, como ya dije, sobre todo cuando el sistema de tipos te lo complica.

Y aunque es cierto que a veces es necesario y bastante útil hacer lo que este principio propone, para mi el 80% del software no lo necesita y sólo estás haciendo una sobre-ingeniería que no se justifica.

## Se usan como un código moral

Los principios SOLID, entre otras cosas, normalmente se usan para avergonzar a las personas que no los conocen o no los aplican. Normalmente hablan de tu valía como desarrollador@ de software basado en el supuesto conocimiento de cosas como estas, y otros principio o reglas (completamente) arbitrarias, sobre todo basadas en el libro Clean Code.

Esta revoltura de principios morales y conveniencia técnica es un **gran error para la comunidad de software**, ya que lleva a la sobre-ingeniería, a la aplicación ciega de principios y técnicas que no tienen sentido en tu caso particular e incluso al desprecio del trabajo de otros programadores.

Para mi, este es el punto más grave, tal vez no directamente de los principios SOLID, sino de la forma en la que se enseñan.

## Análisis más profundo

En este blog hemos escrito 5 artículos analizando cada uno de los principios que lo componen, viendo si conviene aplicarlos y describiendo alternativas. En la mayoría de los casos incluso hablamos de principios más profundos (lo que nos hace ver que los "principios SOLID" debería ser algo como "reglas SOLID").

Aquí los puedes ver:

- SRP: [Análisis de los Principios SOLID: Principio de Responsabilidad Única](/2022/12/01/analisis-de-los-principios-solid-principio-de-responsabilidad-unica.html)
- OCP: [El Principio Abierto/Cerrado](/2022/12/03/el-principio-abierto-cerrado-open-closed.html)
- LSP: [El Principio de Sustitución de Liskov](/2023/03/06/el-principio-de-substitucion-de-liskov.html)
- ISP: [El Principio de Segregación de Interfaces](/2023/04/01/el-principio-de-segregacion-de-interfaces.html)
- DIP: [El Principio de Inversión de Dependencias](/2023/04/22/el-principio-de-inversion-de-dependencias.html)

Espero que estos artículos te sirvan para analizar más profundamente lo que todos enseñan como dogmas que se deben de seguir al pie de la letra, bajo la amenaza de no ser un buen programador o programadora que se irá al infierno de los desarrolladores si no lo sigue.
