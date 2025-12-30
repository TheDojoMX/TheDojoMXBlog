---
title: "Versiona mejor tu código: versionamiento semántico y commits convencionales"
date: 2021-12-04
author: "Héctor Patricio"
tags: ['versionamiento', 'git', 'commits']
description: "Hablemos de cómo versionar tu código para beneficiar a tu equipo y a tus usuarios usando el sistema de vesionamiento semántico y los commits convencionales."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1120/v1638685910/lilzidesigns-EjhKmWfLI2c-unsplash_se9qtf.jpg"
draft: false
---

Una de las mejores cosas que podemos hacer por nosotros mismos y por nuestro equipo es versionar nuestro código y qué mejor que hacerlo de las mejores formas conocidas hasta el momento.

En este artículo hablaremos de dos cosas conectadas: el **versionamiento semántico** y los **"commits convencionales"**.

## ¿Por qué es importante?

Organizar y manejar tu código de tal manera que puedas crear diferentes versiones del sistema que estás programando, cambiar entre ellas o regresar una anterior, es un requerimiento de todos los procesos de desarrollo actuales.

Además, presentar tu software a los usuarios finales en versiones iterativamente mejores es una buena práctica que te permitirá liberar más rápido, más seguido y frecuentemente con mejor calidad. Para lograr esto es importante **comunicar correctamente lo que está cambiando en cada versión**.

La herramienta más usada para versionar nuestro código es **git**, pero no establece ningún lineamiento en la forma en la que liberamos el software para los usuarios finales. Así que veamos primeramente una forma de comunicar nuestros cambios de manera correcta y efectiva y después una forma de hacerlo conectarlo con nuestro proceso de trabajo con git.

## Versionamiento semántico

El versionamiento semántico (Semantic Versioning o SemVer) es una forma de **comunicar a nuestros usuarios finales los tipos de cambios introducidos en las nuevas versiones.**

Esto es muy importante porque, como seguramente habrás experimentado, un proyecto de software requiere de muchas dependencias y cuando alguna de ellas no funciona bien, tiene algunos bugs, o no es compatible con lo que ya existía, nos podemos meter en serios problemas. Y mientras más grande es el proyecto, más dependencias necesitarás, lo que agranda el problema.

Lo que **SemVer** propone es una sintaxis formal que nos permite entender el tipo de cambios introducidos en cada versión. Esta sintaxis constituye un lenguaje formal que puede ser usado para resolver automáticamente problemas de dependencias si se usa correctamente.

Antes de ver un ejemplo de una versión semántica es importante que aclaremos que esta se usa para software que tiene una interfaz establecida. Esta interfaz formal está completamente documentada para que otros programadores o usuarios finales pueden usar tu software. A esta interfaz le llamaremos **API** (Application Programming Interface)[^1] a partir de ahora. Ahora sí, una versión en SemVer se ve así:

```
1.0.2
```

El primer número es la versión mayor, en este caso 1. El segundo número es la versión menor, en este caso 0. El tercer número es la versión del parche, en este caso 2.

Ahora bien, ¿que significa cuando cambian estos números?

1. Cuando cambia la versión mayor, se introducen cambios que hacen que la API sea incompatible con la versión anterior. Imagínate por ejemplo que se remueve alguna función o módulo que ya no se necesita. También puede ser que aunque no cambie explícitamente el contrato externo, cambie el significado de una operación.

2. Cuando cambia la versión menor, se han introducido cambios o mejoras que no hacen incompatible a la API con versiones anteriores. Imagínate algo como agregarle nuevos parámetros a una función, pero que soporta valores default para que pueda seguir siendo llamada de la forma anterior. O también puede ser que agregas nuevas partes que no afectan a la forma en la que se usan las antiguas.

3. Cuando cambia la versión de parche, no se ha introducido cambios externos a la interfaz por diseño, sino que se han arreglado errores que causaban mal funcionamiento.

Después de estos tres elementos pueden venir otros detalles, como por ejemplo la versón de prelanzamiento y metadatos de la compilación.

En el documento oficial [Versionamiento Semántico 2.0](https://semver.org/lang/es/) puedes ver más detalles sobre cómo trabajar con él, pero sobre todo notarás lo importante y serio que es que comuniquemos correctamente lo que está pasando con el software que hacemos, sobre todo si otros dependen de él. También podrás ver como las cadenas resultantes de semantic versioning son un lenguaje formal en el que se puede confiar para programar resolución de dependencias, hasta tienen un regex para reconocerlas.

Ahora veamos una herramienta que te ayudará a llevar cuenta del tipo de cambios que se van introduciendo en tu software y base de código.

## Commits convencionales

Los [commits convencionales (Conventional Commits)](https://conventionalcommits.org/) son una forma de estructurar tus mensajes de cada commit para comunicar explícitamente lo que estás cambiando. El objetivo es que 1) puedas saber exactamente lo que el equipo ha cambiado en cada nueva versión o rama y 2) poder automatizar la creación de versiones semánticas y registros de cambios (changelog).

Un commit convencional tiene la siguiente estructura:

```
<tipo de commit> [ámbito (opcional)]: <descripción>

[cuerpo (opcional)]

[notas finales (opcional)]
```

Los tipos de commit directamente establecidos por la especificación son:

1. fix: Se trata de una corrección de un bug. Este tipo de commit se relaciona con una nueva versión de parche.
2. feat: Se trata de una nueva función o módulo. Este tipo de commits se relaciona con una nueva versión menor.
3. BREAKING CHANGE: No es un tipo de commit sino una nota final. Siempre que se incluyan debe generarse una nueva versión mayor en la siguiente liberación.

Si se incluye un símbolo de admiración después del tipo de commit como de esta forma `feat!` significa que este commit introduce un cambio que rompe la compatibilidad con la versión anterior.

El **ámbito** puede referirse a la base de código o módulo al que se aplicó el cambio.

Veamos algunos ejemplos:

```
feat(core): Ahora podemos usar ARGON2i para cifrar las contraseñas
```

```
fix!: Removemos la compatibilidad con SHA-1 debido a que no es seguro

Se encontró que SHA-1 no es seguro debido a que se pueden fabricar colisiones y por lo tanto hemos removido el soporte en la plataforma
```

```
feat: Añadimos el soporte de Sal para todas las funciones de hasheo

BREAKING CHANGE: Todas las firmas de función ahora requieren el parámetro `salt`
```

Básicamente en esto consisten los commits convencionales y si tu base de código los sigue, podrás usar herramientas para automatizar la creación de versiones semánticas y registros de cambios (changelog), ademas de mejorar drásticamente la información que se encuentra en los repositorios y cuándo sucedieron los cambios.

Puedes ver la especificación completa, más tipos de commits, ejemplos y las herramientas que te facilitarán la vida en [la página oficial en español](https://conventionalcommits.org/es/).
## Conclusión

Comunicar correctamente el estado de nuestros sistemas y módulos hacia nuestros usuarios finales es una tarea muy importante para los desarrolladores de software profesionales. Como podrás haber notado, para que esto tenga utilidad, el requisito previo es que exista documentación formal de tu software.

Espero que estas herramientas te ayuden a crear software que sea más fácil usar, mantener y más disfrutable tanto para ti como para tus usuarios finales.

[^1]: Aquí puedes ver por qué se llama una API a la interfaz que presenta una pieza de software a otra: [API's con Hug](https://youtu.be/n8MxyHG0j3Q)