---
title: "Crea hashes resistentes a balas con Keccak (también llamado SHA-3)"
date: 2022-10-12
author: Héctor Patricio
tags: criptografia crypto hash keccak
comments: true
excerpt: "¿Por qué deberías usar SHA-3 para tus nuevos desarrollos? No hay pretexto ya para que uses lo mejor y más probado"
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_crop,h_400,w_1200,x_0,y_386/v1665632333/DALL_E_2022-10-12_22.38.45_cmmlql.png
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_crop,h_150,w_300,x_0,y_386/v1665632333/DALL_E_2022-10-12_22.38.45_cmmlql.png
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Ya hemos hablado en este blog de lo que es un [hash](/2021/12/02/algoritmos-criptograficos-que-es-un-hash.html) e incluso qué hashes puedes usar para guardar tus [passwords de manera segura](/2021/12/03/algoritmos-criptograficos-hashes-seguros-para-alamcenar-passwords.html).

En este artículo vamos a hablar de uno en específico, el que estamos seguros que deberías usar para cualquier uso futuro en tus programas y sistemas, el que ha sido nombrado como el Secure Hash Algorithm 3 (SHA-3): **Keccak**.

## ¿Qué es Keccak?

[Keccak](https://keccak.team/) es una familia de funciones, creadas para cubrir la necesidad de un sucesor de la versión 2 del _Secure Hash Algorithm_, que tiene algunas limitaciones y vulnerabilidades (por ejemplo, el ataque de extensión de longitud).

Está basada en una construcción de esponja, y usa internamente una función criptográfica llamada **Keccak-f**, que se encarga de permutar (cambiar de lugar o mezclar) los bits de la entrada de manera segura.

Después de haber ganado la competición para la versión 3 del _Secure Hash Algorithm_, y por lo tanto ser nombrada **SHA-3**, ha sido estandarizada en diferentes documentos para diferentes usos. La estandarización implica que ha sido examinada y analizada criptográficamente por organismos internacionales, empresas e individuales para estar seguros de que no tiene deficiencias como función hash criptográfica.

Un punto interesante es que uno de los diseñadores de esta función, también participó en la creación del actual AES: [Joan Daemen](https://cs.ru.nl/~joan/), probablmente es un investigador al que le debamos prestar más atención, ya que casi toda nuestra seguridad actual y futura está influida por él.

## ¿Qué es una construcción de esponja?

La "arquitectura" interna de Keccak se distingue de otras funciones hashes criptográficas por ser tener una construcción de esponja. ¿Qué es esto y por qué nos importa como desarrolladores de software?

Una construcción de esponja implica que la entrada de datos pasa sucesivamente (de manera iterativa) por una función que siempre devuelve una cantidad fija de bits y por lo tanto podemos pensar que los _absorbe_. Al _absorber_ estos bits, su estado interno cambia y esto hace que se comporte de manera segura. La analogía con una esponja se acaba aquí, ya que, a diferencia de una esponja real, no podemos "exprimir" a la función para que nos devuelva los bits que ya absorbió. En la imagen siguiente ilustramos la construcción a grandes rangos de Keccak.

![arquitectura interna de Keccak]()
---

¿Por qué nos interesa esto? Las funciones de esponja pueden ser configuradas para que absorban más o menos bits y por lo tanto son bastante flexibles, lo que permite crear funciones configurables y que pueden crear salidas de diferentes tamaños.
