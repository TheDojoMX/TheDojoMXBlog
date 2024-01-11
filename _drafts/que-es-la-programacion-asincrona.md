---
title: "¿Qué es la programación asíncrona?"
date: 2023-12-16
author: Héctor Patricio
tags: async/await concurrencia javascript
comments: true
excerpt: "Entender la programación asíncrona es un requisito si eres un desarrollador de software que quiere sacar el mejor rendimiento de una computadora, hablemos de qué es y cómo dominarla."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1702917369/artisanalphoto-MJcb7ZhNeUA-unsplash_s6toxn.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1702917369/artisanalphoto-MJcb7ZhNeUA-unsplash_s6toxn.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Cuando empiezas a programar, uno de los temas que se presentan pronto, es el de la programación asíncrona y sobre todo si empiezas con **JavaScript**, ya que es un lenguaje que se ha implementado con un modelo de ejecución asíncrono.

## ¿Qué es la programación asíncrona?

Para entenderla primero tenemos que entender la programación tradicional o síncrona (creo que la palabra correcta en español es _sincrónica_).

En la programación las cosas siempre suceden en un orden estricto, una instrucción empieza y hasta que no se termina, no se ejecuta la siguiente. Observa el siguiente código:

```js
consta a = 1
const b = 2
let c = 0

c = a + b
console.log("c vale ", c)
```

En este código, primero se declaran las variables `a`, `b` y `c`, después se asigna el valor de `a + b` a `c` y finalmente se imprime el valor de `c`. Todo esto sucede en un orden estricto como la mayoría de los programadores esperamos.

Pero ahora observa este código:

```js
const a = 1
const b = 2
let c = 0
setImmediate(() => {
  c = a + b
})
console.log("c vale ", c)
```

El único cambio que hicimos aquí es el uso de la función `setImmediate`, que es una función que recibe otra función como parámetro y la ejecuta en el siguiente ciclo de ejecución del _event loop_ de **Node.js** o el ejecutor en el que esté.

Un código que puede ser similar pero usando async/await sería:

```js

const a = 1
const b = 2
let c = 0

async function sum() {
  c += a + b
}

async function main() {
  await sum()
  await sum()
}
main()
console.log("c vale ", c)  # c vale 3

```

Esto es específico de JS, pero como son palabras en inglés debería ser sencillo de entender. Tenemos que hacer dos cosas para que funcione de manera asíncrona, la primera es declarar la función `sum` como `async` y la segunda es usar la palabra reservada `await` para esperar a que la función `sum` termine de ejecutarse, además de declarar la función `main` como `async` también, ya que no podemos usar `await` en una función que no sea `async` o fuera de un módulo de JavaScript.

Pero aquí vemos claramente le efecto: nos dice que 3 es el valor de `c`, cuando en realidad esperaríamos que fuera 6, ya que `sum` se ejecuta dos veces.

La explicación a esto está en que con la programación asíncrona podemos modificar **cuándo se ejecutan las cosas**. Pero otra visión es que se pueden ejecutar cosas en diferentes "lados" o "momentos" y tú elegir **cuándo** usas los resultados de la ejecución.

## Definición

La programación asíncrona es un forma de ejecutar las acciones de tu programa en la que no se espera siempre que una acción o instrucción termine para continuar con el progrma.

Como vimos en el primer ejemplo, en la programación síncrona (también llamada _bloqueante_ [blocking]), ninguna acción comienza hasta que le previa haya terminado. En la programación asíncrona, con técnicas o palabras reservadas específicas le indicamos al motor de ejecución que no es necesario a que una acción termine para continuar con la siguiente, pero también le podemos decir qué hacer cuando la acción termine. Por esto mismo, la programación asíncrona también se conoce como _no bloqueante_ (non-blocking).

## Para qué sirve la programación asíncrona

Antes de explicar directamente cómo podemos usar la programación asíncrona para mejorar nuestros programas, veamos las restricciones que tenemos. Cuando estás construyendo un programa, la velocidad ejecución puede depender o verse limitada por dos cosas:

- De los cálculos que estás haciendo
- De la información que estás obteniendo o guardando en algún lugar

En el primer caso, llamamos a la ejecución **CPU bound** y en el segundo **I/O bound**.

### CPU bound

Cuando tu programa es pesado en los cálculos que tiene que hacer, como cuando tienes que procesar multimedia, hacer multiplicación de matrices o cosas similares, puedes decir que tu programa es **CPU bound**, o que está limitado por el poder de procesamiento.

En este caso, la programación asíncrona te puede ayudar si tienes múltiples **ejecutores** en los que puedas distribuir el cómputo. Por ejemplo:

- Si tienes un procesador con múltiples cores o múltiples hilos de ejecución
- Si tienes múltiples computadoras que pueden hacer el cómputo

En el primer caso, necesitas una plataforma que te ayude a utilizar el poder de procesamiento de los múltiples cores, sea implícitamente o explícitamente. Por ejemplo plataformas como la máquina virtual de Erlang, automáticamente distribuyen la carga en los múltiples cores disponibles. En otros lenguajes como en Python, tienes que hacerlo explícitamente.

### I/O bound

Cuando un programa consume o produce mucha información normalmente tiene que ponerla en algún lugar. Estos lugares pueden ser:

- La memoria RAM
- El disco duro
- La red (mandarla o pedirla a un servidor)

En estos casos, se dice que el programa está limitado por la velocidad de entrada y salida de datos, o **I/O bound**.

La programación asíncrona te puede ayudar de manera más sencilla, sobre todo en el caso de las peticiones de red. ¿Cómo? Si hacemos que la

## Conclusión

...