---
title: "Usando combinadores para programar"
date: 2023-08-24
author: Héctor Patricio
tags: fp programación-funcional combinadores
comments: true
excerpt: "Hablemos de lo que es un combinador y cómo se usan para crear buen código funcional"
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,e_oil_paint:30,w_1450/v1693028283/arnaud-gillard-cj3m-DNCBNA-unsplash_asn55x.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,e_oil_paint:30,w_450/v1693028283/arnaud-gillard-cj3m-DNCBNA-unsplash_asn55x.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

## ¿Qué es un combinador?

Vayamos por partes: un combinador es simplemente una función con características especiales. En el _cálculo lambda_, un combinador es una función que no tiene variables libres, es decir, que no depende de ningún valor externo a ella misma. Además, un combinador sólo puede estar formado por otros combinadores.

Prácticamente unn combinador es una función que:

- No tiene efectos secundarios
- No depende de ningún estado externo

Basado en estas características definidas, se han definido una serie de combinadores útiles que permite crear código funcional de manera más sencilla y elegante. Veamos algunos de ellos.


## Algunos Cobinadores

Los combinadores conocidos tienen nombres de letras o combinaciones de letras. En esta sección los explicaremos uno a uno. Y daremos algunos ejemplos de cómo usarlos.

### `I` o Identidad

El combinador más sencillo es el llamado Identidad, y no hace más que devolver el valor que recibe. Es el equivalente al operador neutro de la suma, el `0`, o el de la multiplicación, el `1`.

```js
const I = x => x
```

En un libro llamado **"To Mock a Mockingbird"** de _Raymond Smullyan_, se les pone nombres de aves a cada combinador, ya que el usa una analogía basada en aves para explicarlos.

### `K` o Constante

El combinador `K` es el que recibe dos valores y devuelve el primero. Es decir, es una función que ignora el segundo valor y SIEMPRE devuelve el primer valor.

```js
const K = x => y => x
```

### `KI` o Flip


## Ejemplos de uso


##