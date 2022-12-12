---
title: "¿Por qué aprender Rust en 2023?"
date: 2022-12-10
author: Héctor Patricio
tags: rust aprendizaje lenguajes-de-programacion
comments: true
excerpt: "¿Por qué es Rust uno de los lenguajes más amados de la actualiad? ¿Te conviene aprenderlo? Vamos a platicar de eso en este artículo."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_crop,h_400,w_1024/v1670303988/DALL_E_2022-12-05_13.19.43_-_rust_on_a_gold_wall_digital_art_illustration_cinematic_m5cplm.png
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_crop,h_200,w_512/v1670303988/DALL_E_2022-12-05_13.19.43_-_rust_on_a_gold_wall_digital_art_illustration_cinematic_m5cplm.png
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Rust se ha establecido como uno de los lenguajes más queridos entre los desarrolladores en los últimos años y desde 2016 está en el número uno, según la encuesta anual de [Stack Overflow](https://insights.stackoverflow.com/survey/2016#technology-most-loved-dreaded-and-wanted). Esto no es de extrañar, ya que Rust es un lenguaje que ofrece **muchas cosas buenas** a aquellos que lo usan.

En este artículo vamos a hablar de algunas de sus características, las ventajas de su ecosistema, y por qué te conviene aprenderlo. Además vamos a hablar de cuándo no es tan buena idea.

## Historia y concepción

> No siempre fue así de claro, pero el lenguaje de programación Rust trata acerca de _empoderamiento_: no importa qué tipo de código estés escribiendo ahora, Rust te habilita para llegar más lejos, para programar con confianza en una variedad de dominios más amplia que la que antes hacías. - Nicholas Matsakis and Aaron Turon

Rust nació en 2006 como un proyecto personal de [Graydon Hoare](https://github.com/graydon), un empleado de Mozilla en ese entonces, que siempre ha trabajado en lado de los compiladores. Después de mostrárselo a su jefe, a Mozilla le interesó como una alternativa mejor que C y C++ para crear su motor de renderizado web llamado [Servo](https://servo.org/). Y, efectivamente, Servo actualmente estás escrito en Rust.

### Idea detrás de Rust

Según [la entrevista](https://www.infoq.com/news/2012/08/Interview-Rust/) que le hicieron a Graydon, en Rust quiso implementar todas las características que le parecían interesantes y amadas de otros lenguajes, pero para un lenguaje dedicado a la creación sistemas, con la teoría de que las concesiones y condiciones que hacen que lenguajes como C y C++ siempre fueran favorecidos, han cambiado desde que nacieron.

Así que Rust nació con la **seguridad de memoria y la concurrencia en mente**, pensando que el internet y la apertura que este provee hace que estas características sean muy importantes. Hablemos de estas características.

## Características de Rust

Rust en un lenguaje que quiere reemplazar a C y C++, por lo que necesita características que les compitan y los mejoren, hablemos de tres de ellas con las que lo está intentando.

### Rendimiento

C y C++ se distinguen por ser los lenguajes para creación de sistemas más eficientes, y por eso Rust tiene que ser por lo menos tan eficiente como ellos. Rust, en la mayoría de los casos logra equipararse al rendimiento de C y C++.

Aquí puedes ver algunas mediciones de Rust contra C++: [Benchmarks Rust vs C++](https://programming-language-benchmarks.vercel.app/cpp-vs-rust). Y aquí hay otros un poco más entendibles: [Rust vs C](https://levelup.gitconnected.com/which-is-faster-rust-or-c-lets-find-out-who-is-the-usain-bolt-87495c774c8). La conclusión a la que podemos llegar es que Rust es un contendiente muy serio para C y C++ en cuanto a velocidad y eficiencia.

Lo que tenemos que recordar es que Rust provee características que C y C++, que hacen más fácil y segura la programación, por lo que si es casi tan rápido como estos, más sus características extra, entonces es una gran oferta para los desarrolladores.

### Seguridad de memoria

La seguridad de memoria se refiere a la propiedad de los entornos de ejecución de los programas que te **asegura que las referencias a memoria siempre son válidas**. Si has programado en C y C++ has experimentado un entorno no seguro en memoria: puedes acceder a registros de memoria que no han sido inicializados y por lo tanto contienen información incierta. Para que la memoria siempre sea segura se necesita que siempre sea alocada por el programa y se del tipo y tamaño correcto.

Un programa que no es seguro en memoria puede dar bugs aleatorios o fallar aleatoriamente sin explicación alguna. Además también puede ser inseguro respecto a la integridad de tus datos, ya que las fallas en el manejo de memoria pueden ser explotadas de formas creativas por los atacantes para acceder a información sensible.

Uno de los objetivos de diseño en Rust es que sea seguro de memoria, para mi uno de los distintivos más grandes con C y C++.

¿Cómo logra Rust la seguridad de memoria? Mediante un sistema de verificación estático de [_prestamos_ y _pertenencia_](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html). En artículos futuros explicaremos cómo se logra la seguridad de memoria con este sistema.

### Productividad

Como lo dice la cita del principio, la ventaja principal de Rust es que te permite ser más productivo en diferentes aspectos de la programación. Rust tiene a [cargo](https://doc.rust-lang.org/cargo/), el manejador de paquetes que además te ayuda a ...

[abstracciones sin costo](https://boats.gitlab.io/blog/post/zero-cost-abstractions/)

> Rust solves pain points present in many other languages, providing a solid step forward with a limited number of downsides. - Jake Goulding

## Entorno

### Comunidad

### Recursos para aprender

## Conclusión
