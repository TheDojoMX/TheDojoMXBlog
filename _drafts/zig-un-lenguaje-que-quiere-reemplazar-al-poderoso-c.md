---
title: "Zig: un lenguaje que quiere reemplazar al poderoso C"
date: 2024-03-10
author: Héctor Patricio
tags: zig zig-lang c c-lang
comments: true
excerpt: "Zig es un lenguaje prometedor que quiere reemplazar a C y competir con Rust por ser el nuevo lenguaje de sistemas. Hablemos de sus promesas y características."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1747718313/mariola-grobelska-EJBwRJZMOCQ-unsplash_rugsm8.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1747718313/mariola-grobelska-EJBwRJZMOCQ-unsplash_rugsm8.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Recientemente hemos visto una ola de lenguajes listos para destronar
a los lenguajes de programación que forman la base de casi toda nuestra
computación actual: C y C++. Lenguajes como Rust y Go quieren reemplazarlos,
pero tenemos a otro competidor que apunta directamente hacia C y parece
que se está acercando aunque no tiene todavía una versión completamente estable.

En este artículo vamos a hablar de las características de Zig y cómo es que
planea reemplazar a C.

## Las características de Zig

[Zig](https://ziglang.org/) es actualmente desarrollado por la Zig Software
Foundation, una organización sin fines de lucro que básicamente fue creada para
seguir desarrollando el lenguaje. Pero [**Andrew Kelley**](https://andrewkelley.me/),
lo empezó en 2015 con la idea de retar la forma en la que hacemos software.

Kelley es un programador con experiencia en C principalmente y mientras trabajaba en su
proyecto "Genesis Digital Audio Workstation" se decidió para crear Zig.
En sus propias palabras: _"mi meta es crear un lenguaje más pragmático que C."_

Algunas de las características que presenta en el artículo en el que
habla por primera vez de Zig son:

1. **Pragmatismo**. Ser pragmático es lo mismo que ser práctico. Zig es un lenguaje
   que se enfoca en resolver problemas reales y no en ser un lenguaje teórico, y quiere
   ayudarte a lograr lo que necesitas hacer mejor que otros lenguajes.
2. **Óptimo**. Debe de ser iguale de rápido o más que C y más fácil de escribir.
3. **Seguridad en memoria**. Es la segunda característica más importante del lenguaje, Kelley
  dice que va en el asiento del copiloto.
4. **Legible**. zig debería evitar la sintaxis compleja y tener una forma canónica de hacer las cosas
  dando como resultado un código que sea fácil de leer, aunque te tengas que esforzar un poco para escribirlo.

## Algunas decisiones de diseño

Se dice que los lenguajes de programación están creados por los miedos de sus diseñadores.
Por ejemplo, si alguien quiere hacer un nuevo lenguaje viniendo de lenguajes que
tardan mucho en compilar, por ejemplo C++, va a intentar hacer un lenguaje
que compile rápido, como fue le caso de Go.

Veamos algunas decisiones de diseño de Zig.

### Interoperabilidad completa con C

C tiene una dominación histórica en el mundo de la programación de sistemas. Muchos de los
sistemas importantes están escritos en C. Así es que Zig tiene como una decisón de diseño
crear programas que puedan ser usados desde C o al revés. Así que Zig es compatible con la
C ABI.

La **C ABI** (Application Binary Interface) es un conjunto de convenciones y reglas que
define cómo los programas compilados en C interactúan a nivel de código máquina.

### Uso de tipos opcionales

El manejo de valores vacíos o nulos es uno de los grandes problemas en todo el desarrollo de
software. Así que Zig ha elegido usar tipos opcionales, es decir, valores que desde el
sistemas de tipos declaras que pueden contener un valor o no. Así el compilador te puede
ayudar a no dispararte en el pie dejando como nulo o aceptando un nulo en una variable donde
siempre debería haber un valor. Además, te puede ayudar a verificar que estás considerando
todos los casos posibles cuando tienes variables opcionales.

### Manejo de errores

Zig utiliza tipos de datos primitivos para manejar errores. Estos son los Error Sets y
Error Unions. Con estos dos tipos de datos puedes crear funciones que devuelvan un error
y manejarlo de forma más elegante.

### Otras características

Zig tiene otras características muy interesantes nacidas directamente del uso que su
principal creador, Andrew Kelley, hizo de C desde hace mucho tiempo. Por ejemplo tiene
características para evitar el preprocesador de C, por ejemplo, sintaxis directa para
compilación condicional.

## Algunos proyectos importantes en Zig

Aunque todavía no tenemos una versión 100% estable de Zig, ya tenemos proyectos que
están haciendo olas en el mundo de la programación programados en Zig. Hablemos de
algunos de ellos:

- [Bun](https://bun.sh/): Bun es un nuevo runtime de JavaScript que caracteriza
por su gran velocidad de ejecución. Aunque no tiene todas las características de
Node.js todavía, se lo lleva por mucho en rendimiento.

- [TigerBeetle](https://github.com/tigerbeetle/tigerbeetle): TigerBeetle es una
base de datos financiera distribuida. Como te imaginarás, todo aquello que se quiera
usar en un entorno financiero serio debe ofrecer características fuertes de rendimiento
y seguridad.

- [Ghostty](https://github.com/ghostty-org/ghostty): Ghostty es un emulador de terminal
escrito por el mismo creador de Terraform, Mitchell Hashimoto, que está intentando hacer
todas las cosas bien.

## Conclusión

Si estás metido en el desarrollo de sistemas, sin duda Zig es un lenguaje que vale la pena
voltear a ver, pero también si quieres aprender más sobre desarrollo de software a bajo nivel
con ideas modernas.