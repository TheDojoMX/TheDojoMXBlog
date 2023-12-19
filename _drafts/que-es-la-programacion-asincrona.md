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

Para entenderla primero tenemos que entender la programación tradicional o síncrona.

En la programación las cosas siempre suceden en un orden estricto, una instrucción empieza y hasta que no se termina, no se ejecuta la siguiente. Observa el siguiente código:

```js
consta a = 1
const b = 2
let c = 0

c = a + b
console.log("c vale ", c)
```
