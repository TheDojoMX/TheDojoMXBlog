---
title: "A Philosophy of Software Design: Tres formas de identificar la complejidad"
date: 2020-02-26
author: "Héctor Patricio"
tags: ['ousterhout', 'complejidad', 'diseño-de-software', 'posd']
description: "Aprende a descubrir y medir la complejidad en tus proyectos"
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1582698547/scott-webb-186119-unsplash_hholsr.jpg"
draft: false
---

> "Controlar la complejidad es la esencia de la programación" - Brian W. Kernighan

Muchas mentes brillantes dedicadas al desarrollo de software han estado de acuerdo en que el principal problema al crear y mantener programas es el manejo de la complejidad.

Podemos decir que algo complejo es aquello que está **compuesto por muchas piezas relacionadas entre ellas**. [Ousterhout](http://web.stanford.edu/~ouster/cgi-bin/home.php) lo define de manera práctica _como todo aquello que hace que el software sea difícil de entender, escribir o mantener_.

> La complejidad es más visible para los lectores que para los escritores [del código]. Si escribes una pieza de código que parece simple para ti, pero otras personas piensan que es compleja, entonces es **compleja**. - John Ousterhout

Philosophy of Software Design habla de tres formas de identificar un programa más complejo de lo que debería ser:

1. Amplificación de cambios
2. Carga cognitiva
3. Desconocidos desconocidos

Identificar la complejidad es una **habilidad crítica para el buen diseño de software**, te permitirá crear sistemas más simples y evitará que gastes recursos en desarrollar soluciones que son demasiado complejas.

## Amplificación de cambios

Este síntoma de la complejidad se hace obvio cuando estás haciendo un cambio que debió haber sido sencillo y tienes que tocar 7 archivos, 3 clases y 4 funciones. Se refiere a que una funcionalidad que parece sencilla del programa está repartida en muchos lados y para lograr hacer un cambio hay que tocar muchas partes del sistema.

Esto se pude dar cuando parámetros o valores que pueden estar centralizados o referenciados se ponen fijos a través de muchos archivos. También cuando código que se podría reutilizar se copia y pega.

## Carga cognitiva

Si tienes que mantener muchas cosas en la cabeza para poder entender el sistema, es complejo. Puede que tengas que entender y aprender muchas cosas acerca del funcionamiento del programa para usarlo bien y no causar un desastre. Cuando algo no tiene una interfaz simple, causa carga cognitiva.

El ejemplo son las funciones de lenguajes de programación que nunca aprendemos a usar porque tienen parámetros que aunque siempre son los mismos son requeridos por no tener un default decente. O por ejemplo, aquellas funciones que no recuerdas si cambian los parámetros o devuelven uno nuevo.

Aunque programas más cortos están relacionados con baja carga cognitiva, no siempre es el caso debido a que ese poco código que existe sea difícil de entender.

## Desconocidos desconocidos

¿Tienes miedo de cambiar algo porque no sabes lo que pueda pasar y no hay ni documentación a la que puedas referirte? En este caso el sistema tiene información **que no sabes que no sabes**.

Un desconocido desconocido es aquella información que ni siquiera sabemos que estaba ahí y que no conocíamos, como algunas características del código, parámetros ocultos y comportamientos que no son fáciles de detectar ni están documentados.

¿Recuerdas la broma que dice: _"Cuando escribí este código sólo Dios y yo sabíamos lo que hacía, ahora sólo Dios sabe"_? Muchas veces nos pasa así con el código y es el ejemplo perfecto de los desconocidos desconocidos, sobre todo para otros programadores.

## Medición de la complejidad

Un sistema puede ser complejo independientemente de su tamaño, es decir, hay sistemas no tan grandes que son muy complejos.

Para determinar la complejidad se puede pensar en la siguiente fórmula.

![Fórmula para calcular la complejidad](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1581460560/Untitled_Artwork_3_oljybd.jpg)


Esto lo podríamos explicar como:

> La complejidad total de un sistema es la sumatoria de la complejidad de cada una de sus partes multiplicada por el tiempo que los desarrolladores pasan en esa parte del código.

Esta complejidad puede evitar que avances tanto como deberías, pero el primer paso es identificarla como lo viste aquí. En los siguientes artículos hablaremos de técnicas para reducir la complejidad.