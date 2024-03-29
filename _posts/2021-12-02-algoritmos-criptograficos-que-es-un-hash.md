---
title: "Algoritmos criptográficos: ¿Qué es un Hash?"
date: 2021-12-02
author: Héctor Patricio
tags: criptografía, hash, cifrado
comments: true
excerpt: "Continuemos con las bases de la criptogrfía para desarrolladores, hablemos de lo que es una función hash y cómo puede servirte en tus aplicaciones."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1120/v1638504578/steven-lasry-UC8hqc0udqY-unsplash_xmtlvb.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_320/v1638504578/steven-lasry-UC8hqc0udqY-unsplash_xmtlvb.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Dentro del mundo del desarrollo se escucha bastante sobre **funciones hash** y, en realidad, se usan para múltiples cosas. En este artículo vamos a hablar de lo que es una función hash, los diferentes tipos que hay y cómo pueden servirte para desarrollar software.

## ¿Qué es un función hash?

La idea y el nombre de un función hash viene de la cocina: _hash_ se traduce literalmente como "picadillo", y se usa precisamente porque eso hace una función hash con los datos que le pasemos.

![Un platillo que parece picadillo](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_500/v1638503321/melissa-walker-horn-ufs4w3Jn73I-unsplash_q4m1qy.jpg){:.align-center}

Las funciones hash reciben una entrada y normalmente te devuelven un valor de tamaño fijo. Estos datos parecen "picadillo", es imposible para los humanos distinguir los argumentos que recibió _a partir de la salida_. Las funciones hash más simples _mapean_ los valores de entrada a un número pequeño, [aquí puedes ver algunos ejemplos](https://www.cs.hmc.edu/~geoff/classes/hmc.cs070.200101/homework10/hashfuncs.html). Estas funciones las puedes considerar como un mapeo de valores (con posibilidades infinitas) a un conjunto de valores finitos. Por eso, una función hash de esta naturaleza se considera como una relación del valor de entrada con su "contenedor" o "bucket" como le dirían en inglés.

Las funciones hash son como navajas suizas, ya que pueden ser utilizadas para ocultar datos, para crear estructuras de datos llamadas __hash tables__, para comparar datos, para crear firmas digitales (verificación de integridad) y muchas otras cosas. Tienen muchos usos dentro y fuera de la criptografía.

Existen diferentes tipos de funciones hash para los diferentes usos, las características que normalmente verás en hashes son:

1. Entregan un resultado de tamaño fijo sin importar el tamaño de la entrada
2. Son rápidas relativamente
3. Son deterministas, es decir, siempre que le demos el mismo valor, dará el mismo resultado
4. Es imposible recuperar la entrada original, porque se pierden datos

Algo que contaría como una función hash podría ser tan sencilla como obtener el sobrante de una división entera para los números enteros:

```python
def hash_simple(x):
    return x % 10
```

Esta función cumple con todas las características de las que hablamos arriba, y es una función hash **no criptográfica** o **no segura**, es decir, no se puede confiar en ella para proteger información.

Algunos ejemplos de funciones hash no criptográficas son:
- [SeaHash](https://docs.rs/seahash/2.0.0/seahash/)
- [fnv1a](https://github.com/sindresorhus/fnv1a)
- La función `hash` de Python o de tu lenguaje preferido

Ahora hablemos de qué características tiene una función hash criptográfica segura.

## Funciones hash criptográficas

La característica principal de una función hash segura es que su resultado es completamente impredecible, no revela ningún tipo de información sobre la entrada original, tanto para los humanos como para _una computadora_, es resistente a análisis estadísticos.

Para asegurarnos de esto, una función hash segura cumple con tres características formales:

1. Es resistente a encontrar una **preimagen**
2. Es resistente a encontrar una **segunda preimagen**
3. Es resistente a **colisiones**

¿Qué es eso de las **_preimágenes_**? En criptografía se llama **preimagen** a todos los valores que le podemos dar a una función hash. La **imagen** es el resultado de aplicar la función hash a una _preimagen_.

Esta ilustración lo puede dejar un poco más claro:

![Diagrama sobre imágenes y preimágnes](https://res.cloudinary.com/hectorip/image/upload/v1638509732/Ilustracio%CC%81n_sin_ti%CC%81tulo_9_qrerag.png){:.align-center}

Ahora hablemos sobre lo que significa cada punto de la seguridad.  El primer punto se refiere a que dada una **imagen** o un _hash_, como normalmente le llamamos al resultado de una función hash, es imposible encontrar la entrada original, o algún otro valor que resulte en ese hash. Si este punto no se cumple, los siguientes dos tampoco.

El segundo punto, la resistencia a la segunda preimagen, es que dado un valor de entrada (praimagen) y su hash correspondiente (imagen), es imposible encontrar otro valor de entrada que se resulte en el mismo hash, o la misma imagen.

El tercer punto, **la resistencia a colisiones** se refiere a que es cerca de imposible encontrar (o fabricar) dos valores de entrada que den el mismo hash (dos preimágenes que resulten en la misma imagen).

En resumen: para un hash seguro **es casi imposible encontrar dos valores que den el mismo hash, teniendo ejemplos de hasheado o no**, así como encontrar el valor que generó cierto hash.

## Algunas funciones hash criptográficamente seguras

Las dos funciones hash criptográficas más populares son [MD5](https://es.wikipedia.org/wiki/MD5) y [SHA-1](https://es.wikipedia.org/wiki/SHA-1). Actualmente (2021) a ambas se les han encontrado vulnerabilidades, sobre todo en el campo de las colisiones, para ambas es posible generar colisiones de manera arbitraria.

_"SHA"_ es un acrónimo que significa Algoritmo de Hasheo Seguro ("Secure Hash Algorithm") y es un "título" dado a los algoritmos de hasheo que son seleccionados por la **NIST** (National Institute of Standards and Technology de Estados Unidos).

Ahora sí hablemos de algunas funciones hash criptográficas todavía consideradas seguras:

1. [SHA-2](https://es.wikipedia.org/wiki/SHA-2). SHA-2 es la familia sucesora de SHA-1, y consiste de 4 funciones hash que difieren en el tamaño de bits de su salida: SHA-224, SHA-256, SHA-384 y SHA-512. Las dos más usadas son SHA-256 y SHA-512. Hasta 2021 no se le han encontrado vulnerabilidades que hagan que sean no recomendadas. La desventaja es que la familia SHA-2 es más lenta que SHA-1.

2. [SHA-3](https://es.wikipedia.org/wiki/SHA-3). SHA-3 es la cuarta versión de SHA y el algoritmo se escogió de un concurso organizado por la NIST en 2007. En 2012 se anunció que el algoritmo seleccionado era [Keccak](https://en.wikipedia.org/wiki/Keccak), un algoritmo muy diferente de SHA-1 y SHA-2. Esta familia de algoritmos también define cuatro funciones hash, SHA3-224, SHA3-256, SHA3-384 y SHA3-512. Pero además define 2 algoritmos extra que pueden dar resultados variables. Puedes ver la página del equipo de Keccak en [Keccak Team](https://keccak.team/keccak.html).

3. [BLAKE2](https://www.blake2.net/). Es un algoritmo sucesor de BLAKE, uno de los participantes en el concurso por SHA-3. BLAKE2 es mucho más rápido que Keccak, casi igual de seguro, pero más parecido a SHA-2, que es la razón por la que no se eligió a BLAKE como el SHA-3. Es una muy buena opción para usarse en caso de que requieras un función hash segura y que la velocidad sea muy importante, ya que es más rápida incluso que SHA-1.

Como puedes ver, tenemos para escoger entre las funciones hash todavía consideradas seguras.

## ¿Qué función hash usar?

Ahora que tenemos un sucesor de SHA-2, la que deberías usar en la mayoría de tus proyectos es **SHA3-256**, ya que provee de la suficiente seguridad, está estandarizada y es probable que sea implementada como instrucciones del procesador en el futuro. Si te importa muchísimo la velocidad en tu proyecto ahora mismo, deberías usar BLAKE2, que también es muy popular y está implementada en muchos lenguajes de programación.

## ¿Sirven para guardar passwords?

Un error común es pensar que estas funciones pueden servir para guardar passwords de forma segura en nuestras aplicaciones. En el siguiente artículo hablaremos de por qué no sirven para eso y qué otras funciones podrías usar.
