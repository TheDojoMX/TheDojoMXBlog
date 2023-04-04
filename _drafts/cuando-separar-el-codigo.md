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

Dominar la división de software en módulos es una pilar del buen diseño de software. Veamos algunos de los criterios que John Ousterhout propone en su libro [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php), precisamente en el capítulo nueve que llama "¿Mejor juntos o separados?" (_"Better together or better apart?"_). Empecemos hablando de cuándo es mejor dejarlo junto.

Lo que tienes que mantener enfrente es que la meta de hacerte es pregunta es disminuir complejidad de tu código en general, pero también de hacerlo más fácil de evolucionar haciéndolo **más modular**.

## Cuando dejarlo junto o combinarlo

**Acceso a la información**. La primera cosa que hay que considerar es la información con la que el módulo trata. Si es un sólo conjunto de información que en sí mismo es difícil de separar, entonces el código que trata con él **debería permanecer junto**.

## Ejemplos

Hablemos de algunos ejemplos en los que se puede ver claramente los diferentes criterios para sepa rar dejar combinado el código.

### Funcionalidad de UNDO (Deshacer)

John Ousterhout da el ejemplo de la funcionalidad de "deshacer" en editor de texto. Eso que sucede cuando das `CTRL+Z` en casi cualquier programa.

¿En qué consiste? En que cuando se realiza una acción, se guarda para que pueda ser contrarrestada con la acción contraria. Esta función puede ser implementada en el módulo central del editor o fuera de él. ¿Cuál es la mejor opción?

## Abriendo y modificando archivos

Cuando escribimos archivos y escribimos en ellos, normalmente no se va todo el contenido directamente a disco. En vez de eso, guardamos los datos en un área temporal llamada buffer. Cuando el buffer se llena o se manda una orden, los datos pasan al disco duro.

La pregunta es: ¿la implementación del buffer debe ir pegada al código que maneja los archivos? O, ¿debería ser un módulo separado?

## Conclusión

Aprender a separar tu código es algo que se logra con la práctica y que sin duda vale la pena hacer, porque un código con una complejidad controlada logra un equilibrio entre módulos demasiado pequeños (que hacen muy poco) y demasiado grandes (que juntan mucha información).