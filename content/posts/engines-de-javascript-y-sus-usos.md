---
title: "Engines de JavaScript y sus usos"
date: 2023-12-14
author: "Héctor Patricio"
tags: ['javascript-engine', 'v8', 'chakra']
description: "En este artículo hablaremos de los diferente engines de JavaScript que existen, dónde los puedes encontrar y para qué los puedes usar."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1701323922/garett-mizunaka-xFjti9rYILo-unsplash_mh0wys.jpg"
draft: false
---

Ya hemos explicado antes qué es un [engine de JavaScript](/2020/05/17/que-es-un-engine-de-javascript.html). Como resumen, es el programa encargado de correr tus programas de JavaScript: recibe tus archivos o código de JS y ejecuta las acciones en el sistema operativo en el que se está ejecutando.

Estos engines actualmente son programas complejos que no solamente interpretan el código, sino que lo analizan y compilan a código máquina para que sea más eficiente su ejecución.

En este artículo vamos a hablar de algunos engines de JavaScript populares y en dónde puedes encontrar su código o sus ejecutables para que los puedas usar. Pero antes hablemos de la utilidad que puede tener un motor de JS fuera de un navegador.

## Usos de un motor de JS

A veces, queremos darle a nuestros usuarios una manera de ejecutar código de manera arbitraria o de modificar el sistema mediante instrucciones que ellos mismos metan en nuestras plataformas o programas. En vez de crear todo un lenguaje o de implementar nuestro propio compilador o intérprete, podemos embeber o incluir un motor de un lenguaje conocido y con implementaciones robustas y disponibles para su uso. **Esta es exactamente el caso de uso que los engines de JS que podemos encontrar implementados cumplen**.

Un ejemplo de quién usa engine fuera de un navegador es un proyecto que ha cambiado el mundo del desarrollo web y que es muy popular: **NodeJS**, es un entorno de ejecución de JavaScript que se basa en el motor V8 de Google y que sirve principalmente para crear aplicaciones web. Mediante el uso de V8, puedes crear servidores web usando JavaScript, y Node se encarga de envolverlo para que puedas usar todas funcionalidades que te ofrece el sistema operativo en el que se está ejecutando.

Otro ejemplo de uso de un motor de JS fuera de un browser es [MongoDB](https://www.mongodb.com/docs/manual/release-notes/3.2-javascript/), que usa el motor SpiderMonkey de Mozilla para ejecutar código de JavaScript en sus bases de datos.

Si buscas más, puedes encontrar un montón de ejemplos en los que un motor de JavaScript es usado fuera de un navegador.

## Engines de JavaScript

Ahora sí, hablemos de los diferentes motores de JavaScript en orden de popularidad.

### V8

Es el motor desarrollado por Google, usado principalmente en Chrome, NodeJS y Deno. Actualmente también está detrás de Microsoft Edge. Es el más popular y el que más desarrollo tiene. Está escrito en C++ y ha tenido varias iteraciones, mejorando los componentes internos. Además cuenta con un JIT compiler que lo hace eficiente en la mayoría de los casos. Otra ventaja de V8 es que puede ejecutar también [WebAssembly](https://webassembly.org/).

Si quieres desarrollar algo que tenga soporte completo del estándar ECMAScript, sea estable y tenga buen rendimiento, con V8 no te puedes equivocar. La desventaja es que tendrás que usarlo como un biblioteca de C++, o por lo menos customizarlo un poco para que se adapte a tus necesidades y hagas los puentes con tu programa, plataforma o lenguaje de programación, tal como Deno (que está escrito en Rust).

Puedes ver su blog técnico aquí: [https://v8.dev/blog](https://v8.dev/blog). Además, si quieres aprender cómo hacer complejos o quieres contribuir, su código fuente está disponible de manera abierta en GitHub: [V8 Github](https://github.com/v8/v8).

### SpiderMonkey

Este motor de JS está desarrollado por Mozilla y es usado en Firefox, Servo y en MongoDB. Igual que V8, está escrito en C++, pera también incluye partes en [Rust](https://www.rust-lang.org/) e incluso en JavaScript. A parte de ejecutar JS, también puede ejecutar WebAssembly.

Si tienes un proyecto en Rust o C++, SpiderMonkey puede ser una gran opción. La principal diferencia con V8 es la velocidad de desarrollo, puedes esperar menos cambios que puedan romper tu código, pero también menos mejoras y actualizaciones, que con V8.

Puedes ver su documentación aquí: [SpiderMonkey](https://firefox-source-docs.mozilla.org/js/index.html).

### ChakraCore

Este motor fue desarrollado por Microsoft y es usado en Chakra (que es un _runtime_ de JS incluye otras cosas más como API's para poder darle más funcionalidad al engine), que a su vez era usado en Edge y Windows (Edge ahora usa Chromium).

ChakraCore está escrito en C++ y C, y presenta una API en C para usarlo en proyectos compatibles con esto. Puede ser compilado para cualquier sistema operativo de 64 bits, pero solamente para Windows para procesadores ARM y de 32 bits. Ya que Microsoft lo dejó de usar, se piensa ahora completamente como un proyecto a cargo de la comunidad.

En las pruebas que yo hice, fue el más fácil de compilar y usar, pero si te fijas en su repositorio, no tiene un desarrollo tan activo.

Puedes ver su documentación aquí: [ChakraCore](https://github.com/chakra-core/ChakraCore). Nota como no está bajo el nombre de chakra-core y no en el repositorio de Microsoft.

### JavaScriptCore

Este es el motor desarrollado por Apple, usado en Safari principalmente. Al igual que los otros, está escrito en C y C++, pero tiene bindings para Objective-C, Swift y C. Así, se puede usar para darle la capacidad a aplicaciones de iOS y macOS de ejecutar código de JS, pero si tienes algo más en C en que puedas envolverlo, sin ningún problemas puedes usarlo en cualquier proyecto.

Puedes ver su documentación aquí: [JavaScriptCore](https://developer.apple.com/documentation/javascriptcore).

### Rhino

También es desarrollado por Mozilla, pero esta vez escrito en Java. Rhino viene incluido en algunas distribuciones de Java. Así que si tienes un proyecto en Java, Rhino es una gran opción, pero debes estar atento a las características que soporta, porque parece que su desarrollo no está tan activo.

Puedes ver su documentación aquí: [Rhino](https://github.com/mozilla/rhino).


## Engines ligeros

Existen una gran variedad de engines de JS más ligeros, no con todas las características de los que acabamos de ver, con la idea de que los puedas embeber en proyectos que dispongan de pocos recursos, tal como sistemas embebidos o proyectos de IoT. Otro buen caso de uso para estos es cuando no requieras las funcionalidades completas de JS sino simplemente soporte básico en tu programa.

Aquí una lista de los más populares:

-  [QuickJS](https://bellard.org/quickjs/): Desarrollado por Fabrice Bellard, quien también creó [FFmpeg](https://www.ffmpeg.org/). QuickJS sólo pesa 210Kb en su forma más sencilla.
- [Duktape](https://duktape.org/): También es muy pequeño, promete funcionar en sistemas con 160Kb de memoria y 64Kb de RAM. Está escrito en C y soporta la ES2015 o ES6.
- [Espruino](https://github.com/espruino/Espruino). Corre en sistemas con 128Kb de memoria y 8Kb de RAM. Está escrito también en C y está pensado para darle soporte a sus propias tarjetas de microncontroladores de bajo consumo, programadas en JS. Pero aún así, lo puedes usar en cualquier proyecto que sea compatible con su API de C o correrlo directamente.

## Conclusión

Espero que esta lista de motores de JavaScript te sea útil para conocer más del ecosistema del que muchos sólo somos usuarios y para entender que JS te puede servir para darles superpoderes a tus sistemas y plataformas. Ya hay muchos proyectos que te permiten hacerlo reduciendo el trabajo al mínimo.
