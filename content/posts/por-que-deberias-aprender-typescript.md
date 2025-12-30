---
title: "¿Por qué deberías aprender TypeScript?"
date: 2021-12-06
author: "Héctor Patricio"
tags: ['javascript', 'typescript', 'js', 'ts']
description: "TypeScript es un lenguaje muy popular actualmente, ¿te conviene aprenderlo? Veamos algunas características y desventajas para ayudarte a decidir."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1120/v1638857085/dominik-lange-Lej_oqHljbk-unsplash_gxaixe.jpg"
draft: false
---

TypeScript es uno de los lenguajes que más ha sonado en los últimos años. En este artículo vamos a hablar de por qué es una buena idea que lo aprendas y las ventajas que te puede dar.

## Acerca de TypeScript

El propósito de TypeScript es tener un lenguaje adecuado para crear grandes sistemas que compile a JS. En realidad, todo programa válido en JS también es Válido en TypeScript. La principal diferencia que verás en TypeScript con respecto a JS es que este soporta anotaciones e inferencia de tipos de datos y los verifica en tiempo de compilación. Así que si tu programa no pasa la verificación de tipos, ni siquiera podrá llegar a correr. Algunas de las características de TypeScript son:

1. **Anotaciones de tipos.** Puedes especificar el tipo de dato de una variable o función.
2. **Inferencia de tipos.** No requiere que se especifique el tipo de dato de una variable explicitamente, ya que lo puede inferir por los valores que le asignas.
3. **Verificación de tipos.** Verifica que tu programa cumpla con los contratos de los tipos de datos.
4. **Borrado de tipos.** Se refiere a la eliminación de tipos de datos de un programa antes de dejarlo listo para correr pero después de verificarlo.
5. **Compilación a una versión específica de JS**. Puedes especificar a qué versión de JS se compilará tu programa.
6. **Genéricos**. Puedes crear funciones que reciban tipos de datos variables.

Es por esto que muchos lo ven como un **JavaScript tipado**. Es cierto que cumplir con los contratos de los tipos es un trabajo extra, pero es una buena idea y un trabajo que vale la pena cuando tienes que hacer un sistema grande. El tipado estático puede protegerte de errores al mismo tiempo que es una capa extra de documentación.

TypeScript (de aquí en adelante le diremos **TS**) fue creado por Microsoft y lanzado al público ne 2012 todavía sin una versión estable. Detrás de él está (Anders Hejlsberg)[https://twitter.com/ahejlsberg], también diseñador de C#, y creador de Delphi y Turbo Pascal. En 2021 vamos en la versión **4.5**, con muchísimos avances desde su primera versión pública.

## ¿Por qué deberías aprender TypeScript?

Ya empezamos a hablar de algunas ventajas en la descripción de lo que es TS. Veamos otras con más detenimiento.

### Reduces los errores en producción

`undefined is not a function` es uno de los errores que más estamos acostumbrados a ver cuando programaos en JS. Este es un error causado por que algo que esperábamos que tuviera una función no la tiene en tiempo de ejecución. Con TypeScript, esto no sucede, ya que te obliga a cumplir con un contrato de tipo de objeto y si no cuenta con cierto atributo, ni siquiera compila. Por ejemplo:

```ts
type Person = {
  name: string;
  age: number;
  sayHello: () => string;
}
const hector: Person  = {
  name: 'Héctor',
  age: 30
};
```

Este código te dará un error **cuando lo intentes compilar** diciendo que el objeto asignado a Héctor no tiene la propiedad ```sayHello```, protegiéndote así de que se te pase algo que creías que estaba bien a producción. Lo mismo sucedería si la propiedad existiera, pero la función tuviera diferentes tipos de entrada y de salida.

Como todo en la programación, esto es un arma de doble filo, ya que puede reducir el tiempo "crudo" de desarrollo, es decir, el tiempo que te lleva programar por primera vez algo listo pra probar, pero reducirá el tiempo total de desarrollo sobre todo si tu programa es grande.

Como punto final, es que probablemente **ni siquiera tengas que correr el código para darte cuenta de que está mal**, ya que tu editor de código, aprovechándose de la características de TS, te avisará que algo está mal ahí.

### Tu editor o IDE puede ser más útil

La información extra que el sistema de inferencia de TS da, o las anotaciones de tipos que tú pones, le dan información al editor que le permite ayudarte de mejor manera, con autocompletados más eficientes, aviso de incumplimiento de contratos en los tipos, etc. Esto contrarresta el tiempo que te llevará extra trabajar con esos tipos.

### La refactorización será más fácil

Tener una capa de protección en forma de un sistema de tipos es una capa extra de información que evitará que rompas tu código si lo cambias para mejorarlo manteniendo la funcionalidad. Pero además de eso, muchas herramientas ofrecen funciones de refactorización automática que se aprovecharán de esta misma información para hacerla de manera más segura y efectiva.

## Desventajas de TypeScript

Personalmente, y lo digo como alguien que ha trabajado tanto en lenguajes con tipado estático y dinámico, creo que para un programador que ha estado acostumbrado a trabajar con tipado dinámico toda su vida sufrirá un poco cuando lo pongas a trabajar en lenguajes como TypeScript y hay situaciones en las que te metes en un verdadero embrollo tratando de cumplir con el sistema de tipos. Esto puede causar algunos retrasos, pero como lo hemos mencionado a lo largo del artículo, los beneficios de usar TS en un sistema grande superan con creces estas restricciones añadidas.

Otra desventaja del código de TypeScript es que puede pasar que el código se vea menos legible si se llena de tipos, pero con el tiempo los programadores pueden aprender en dónde vale la pena poner anotaciones de tipos explícitas contra aprovecharse de la inferencia automática de TS.

## ¿Quieres aprender TypeScript?

Algunos recursos gratuitos que puedes usar para aprender TS:

1. [Tackling TypeScript](https://exploringjs.com/tackling-ts/toc.html) del Dr. Alex Rauschmayer
2. [The TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) de Microsoft

Estos dos recursos están en inglés. Algunos recursos en español:

1. [Curso práctico desde cero](https://www.youtube.com/watch?v=8fnhN1HRPB4)
2. [Curso Práctico Rápido desde cero para Iniciantes](https://www.youtube.com/watch?v=Xxqh0RoWxNc)

Una herramienta de pago que recomiendo muchísimo, tanto por su contenido como por su técnica didáctica es [Execute Program](https://www.executeprogram.com/) creada por [Gary Bernhardt](https://destroyallsoftware.com).

## Conclusión

Si quieres continuar con sistemas serios para entornos que solamente ejecuten JS, una de tus mejore opciones es TypeScript. Las restricciones y la información extra que proporciona el sistema de tipos sobre tu código común supercargará tu proceso de desarrollo desde las herramientas de programación como el editor hasta la protección contra errores en tiempo de compilación.
