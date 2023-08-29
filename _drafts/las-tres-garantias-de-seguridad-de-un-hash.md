---
title: "Las tres garantías de seguridad de un hash"
date: 2023-08-20
author: Héctor Patricio
tags:
comments: true
excerpt: ""
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,e_oil_paint:11,w_1400/v1692582347/neom-bhKqZNZeAR0-unsplash_refcre.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,e_oil_paint:11,w_400/v1692582347/neom-bhKqZNZeAR0-unsplash_refcre.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

En este artículo profundizaremos sobre las garantías de seguridad mínimas que una función hash debe cumplir para ser criptográficamente segura. En un artículo anterior: [¿Qué es un hash?](/2021/12/02/algoritmos-criptograficos-que-es-un-hash.html) ya hablamos más detalladamente de la definición y de los algoritmos que puedes usar aún hoy de manera segura.

Empecemos por una pequeña definición de lo que es una función hash en la criptografía.

## ¿Qué es un hash?

Un hash es una función que te devuelve un valor de tamaño fijo independientemente del tamaño de la entrada, esto implica una compresión de datos. Las funciones hash que son usadas en criptografía, tienen la característica de entregar valores completamente _impredecibles_, tanto para un humano como para una computadora. Es decir que no hay manera de saber qué valor va a entregar una función hash para un valor dado si no le has pasado ese valor antes.

Lo anterior no quiere decir que las funciones hash devuelvan algo diferente cada vez que las ejecutas, sino que para un valor dado, siempre devuelven el mismo resultado, y aquí es donde radica su utilidad.

Un hash perfecto se comportaría como un generador de valores aleatorios, pero debido a lo que hemos dicho anteriormente, deben ser **deterministas** al mismo tiempo que **impredecibles**.

Para medir la seguridad de una función hash, se usan tres pruebas, que se conocen como las garantía de seguridad de un hash. 

Estas garantías son:

1. Resistencia a la primera preimagen
2. Resistencia a la segunda preimagen
3. Resistencia a la colisión

Cada una de estas garantías se refiere a un tipo de ataque que se puede hacer a una función hash. Vamos a explicarlas pero antes aclaremos algunos términos.

## Imagen y preimagen

En matemáticas, una función es una relación entre dos conjuntos de valores, uno de entrada y uno de salida. En la mayoría la de las funciones matemáticas comunes, cada valor de entrada tiene un único valor de salida.

Tomemos como ejemplo: `f(x) = x + 1`, esta función toma un valor `x` y le suma `1`, por lo que cada valor de `x` tiene un único valor de salida, porque sabemos que un número cualquiera tiene solamente un sucesor.

Cuando vemos una función así no es común que nos definan el conjunto de entrada, así que asumimos que el conjunto de entrada o **dominio** es el conjunto de los números reales, y el conjunto de salida o **codominio** es el conjunto de los números reales.

Pensemos en el dominio y codominio como conjuntos amplios en los que los valores de entrada y salida _podrían estar_. La **imagen** de una función es el conjunto de valores que _están_ en el codominio, es decir, los valores que la función _puede_ devuelve. La **preimagen** es el conjunto de valores que _pueden_ ser entrada de la función.

En términos prácticos para nosotros los programadores, la imagen es casi equivalente al codominio, y la preimagen es el dominio.

Esta imagen sacada de Wikipedia lo ilustra un poco mejor:

![Imagen vs Codomino](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_600/v1693144037/Codomain2_kzda4n.svg){: .align-center}


La imagen es el área amarilla, mientras que Y es el codominio, y X es el dominio.

Ahora sí, hablemos de la primera garantía de seguridad de un hash.

## Resistencia a la primera preimagen

Aquí debes poner atención a los valores que se tienen para hacer la prueba de seguridad. Presta atención a cuando se dice "dado un valor".

En la primera garantía es: **Dada** una _imagen_ es computacionalmente inviable encontrar una _preimagen_ que la genere.

En palabra de nosotros los programadores: Dado un hash, es computacionalmente inviable encontrar un valor que al ser pasado a la función hash, genere ese hash. 


## Conclusión

En este artículo vimos las tres garantías de seguridad que debe cumplir una función hash para ser criptográficamente segura. Te sirven para identificar por tu cuenta
