---
title: "Engines de JavaScript y sus usos"
date: 2023-10-14
author: Héctor Patricio
tags: javascript-engine v8 chakra
comments: true
excerpt: "En este artículo hablaremos de los diferente engines de JavaScript que existen, dónde los puedes encontrar y para qué los puedes usar."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1701323922/garett-mizunaka-xFjti9rYILo-unsplash_mh0wys.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1701323922/garett-mizunaka-xFjti9rYILo-unsplash_mh0wys.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Ya hemos explicado antes qué es un [engine de JavaScript](/2020/05/17/que-es-un-engine-de-javascript.html). Como resumen, es el programa encargado de correr tus programas de JavaScript: recibe tus archivos o código de JS y ejecuta las acciones en el sistema operativo en el que se está ejecutando.

Estos engines actualmente son programas complejos que no solamente interpretan el código, sino que lo analizan y compilan a código máquina para que sea más eficiente su ejecución.

En este artículo vamos a hablar de algunos engines de JavaScript populares y en dónde puedes encontrar su código o sus ejecutables para que los puedas usar. Pero antes hablemos de la utilidad que puede tener un motor de JS fuera de un navegador.

## Usos de un motor de JS

A veces, queremos darle a nuestros usuarios una manera de ejecutar código de manera arbitraria o de modificar el sistema mediante instrucciones que ellos mismos metan en nuestras plataformas o programas. En vez de crear todo un lenguaje o de implementar nuestro propio compilador o intérprete, podemos embeber o incluir un motor de un lenguaje conocido y con implementaciones robustas y disponibles para su uso. **Esta es exactamente el caso de uso que los engines de JS que podemos encontrar implementados cumplen**.

Un ejemplo de quién usa engine fuera de un navegador es un proyecto que ha cambiado el mundo del desarrollo web y que es muy popular: **NodeJS**, es un entorno de ejecución de JavaScript que se basa en el motor V8 de Google y que sirve principalmente para crear aplicaciones web. Mediante el uso de V8, puedes crear servidores web usando JavaScript, y Node se encarga de envolverlo para que puedas usar todas funcionalidades que te ofrece el sistema operativo en el que se está ejecutando.

Otro ejmplo de uso de un motor de JS fuera de un browser es [MongoDB](https://www.mongodb.com/docs/manual/release-notes/3.2-javascript/), que usa el motor SpiderMonkey de Mozilla para ejecutar código de JavaScript en sus bases de datos.

Si buscas más, puedes encontrar un montón de ejemplos en los que un motor de JavaScript es usado fuera de un navegador.

## Engines de JavaScript

Ahora sí, hablemos de los diferentes motores de JavaScript en orden de popularidad.
