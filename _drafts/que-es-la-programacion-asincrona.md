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

Un código equivalente pero usando async/await sería:

```js

const a = 1
const b = 2
let c = 0

async function sum() {
  c = a + b
}

async function main() {
  await sum()
}
main()
console.log("c vale ", c)

```

En este caso, tenemos que hacer dos cosas para que funcione de manera asíncrona, la primera es declarar la función `sum` como `async` y la segunda es usar la palabra reservada `await` para esperar a que la función `sum` termine de ejecutarse.