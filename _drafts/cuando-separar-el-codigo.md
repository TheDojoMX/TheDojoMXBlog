---
title: "Cuando separar el código"
date: 2023-04-01
author: Héctor Patricio
tags: aposd ousterhout diseño-de-software
comments: true
excerpt: "¿Cuándo es buena idea que lo existe en un clase o función lo descompongas en varios elementos? En este artículo veremos algunos criterios para tomar esta decisión."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1680411928/risto-kokkonen-HAIDBanzi8o-unsplash_okktgd.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1680411928/risto-kokkonen-HAIDBanzi8o-unsplash_okktgd.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Hay quienes afirman que mientras más pequeñas sean tus clases o funciones, mejor. Hasta llegan a poner un límite de la líneas que pueden ir en un método o función. Esto crea código súper fragmentado que llega a ser complejo por el simple hecho de tener muchos elementos individuales que luego se tienen que unir mediante más código. Además, trazar la causa de algo a través de un código similar es casi imposible o, por lo menos, te puede tomar mucho tiempo.

Es por eso que otros proponentes sobre diseño de software mencionan que mientras más cosas estén detrás de un interfaz y que oculten una implementación, mejor. Esto implica que las funciones y los métodos deben tener un tamaño razonable, sin llegar a ser demasiado grandes. Y este es el punto de este artículo, ¿cómo sabemos cuando es buena idea separar el código en otro módulo? Recuerda que a lo que nos referimos con módulo es cualquier construcción de tu lenguaje que permita encapsular una implementación: clases, funciones, paquetes, etc.

Dominar la división de software en módulos es una pilar del buen diseño de software. Veamos algunos de los criterios que John Ousterhout propone en su libro [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php), precisamente en el capítulo nueve que llama "¿Mejor juntos o separados?" (_"Better together or better apart?"_).

## Cuando separar el código

## Cuando dejarlo junto o unirlo

## Ejemplos

## Conclusión
