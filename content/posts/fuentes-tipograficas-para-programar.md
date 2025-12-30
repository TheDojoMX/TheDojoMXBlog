---
title: "Las mejores fuentes tipográficas para programar"
date: 2019-04-19
author: "Héctor Patricio"
tags: ['fuente', 'editor', 'ide', 'monospace']
description: "Las mejores fuentes para tu editor de código."
featuredImage: "https://cdn-images-1.medium.com/max/2046/0*Jf0p8R5uMnhStfHR.png"
draft: false
---

Personalizar el entorno de programación se ha convertido en uno de los temas más relevantes para los desarrolladores de software, nos permite ser más productivos y estar más contentos en general con el trabajo día a día. No dudo que el lugar en el que más pasamos tiempo los desarrolladores sea el editor de texto o IDE, y, por lo tanto, aprender a personalizarlo es bastante importante. Uno de los aspectos más importantes del editor de texto es la fuente tipográfica.

En éste artículo presentaré las fuentes que me parecen más interesantes diseñadas para programar, además de otras que aunque no fueron diseñadas para los programadores exclusivamente, hacen un gran trabajo. Aunque parezca un tema superfluo, tener un entorno adaptado a nuestros gustos, tanto estética como funcionalmente, es increíblemente efectivo para ser más productivos. Pero antes de empezar unas notas acerca de la tipografía.

## Fuentes tipográficas

Las fuentes usadas usadas en entornos cotidianos, como este post, en los procesadores de texto, en la mayoría de los textos impresos, libros y revistas son fuentes *espaciadas proporcionalmente*, las letras ocupan espacio horizontal proporcional a lo anchas que son naturalmente, así la **i** y la **m** ocupan diferente espacio horizontal:

> *iiiiiiiiii*
---
> *mmmmmmmmmm*

¿Podrías decir que es el mismo número de letras? Son 10 de cada una.

Las fuentes espaciadas proporcionalmente facilitan la lectura o el escaneo de **palabras enteras**, por lo que nos permiten leer más rápido. Sin embargo, tienen algunas desventajas: los los signos de puntuación, las letras delgadas y otros símbolos son fáciles de pasar por alto. **Algo que no conviene en la programación**, como ya sabrás.

Por la razón anterior, y [otras mencionadas en esta pregunta de Stack Overflow](http://stackoverflow.com/questions/218623/why-use-monospace-fonts-in-your-ide), los programadores estamos acostumbrados a usar fuentes *monoespaciadas* o con *espaciado fijo*. En este tipo de fuentes las letras ocupan el mismo espacio horizontal sin importar el ancho natural de la letra en cuestión, incluidos los signos de puntuación. Así se puede crear una “cuadrícula” de letras. Veamos otra vez el ejemplo de las letras **i** y **m**:

```
  iiiiiiiiii
  mmmmmmmmmm
```

Ahora puedes afirmar que hay el mismo número de caracteres aunque no sepas exactamente cuántos. ¿Cómo ayuda esto a los programadores? Aquí un ejemplo:

>if !i, do: func()

```elixir
if !i, do: func()
```

¿En qué tipo de fuente es más legible la expresión anterior? Al dar un espaciado fijo a cada letra podemos distinguir mejor los dos caracteres que existen. Por ejemplo, en la fuente monoespaciada podemos ver claramente el símbolo de negación.

Después de entender esto sabemos porque muchas de las fuentes usadas para programar llevan en su nombre “Mono”, quiere decir que es una fuente monoespaciada. Ahora sólo un detalle más acerca de algunas fuentes: las ligaduras.

## Ligaduras

Las ligaduras en las fuentes tipográficas suceden cuando el conjunto de caracteres se ha diseñado para que algunos conjuntos especiales de dos o tres caracteres puedan ser representados con un solo trazo o glifo. Lo normal era en letras como la **f** y la **i**, para que el espacio no quedara desproporcionado. Puedes leer más a detalle sobre las ligaduras tradicionales en este artículo: [Ligaduras](http://www.tiposconcaracter.es/ligaduras/). Aquí hay unos ejemplos de las ligaduras tradicionales:

![Ligaduras tradicionales](https://cdn-images-1.medium.com/max/2000/0*kZ5QtY4t8GMhrtLl.jpg)

Ahora bien, las ligaduras se pueden usar para mostrar caracteres especiales más legibles y entendibles como en el caso de los conjuntos de caracteres: =>, !=, ==. Varias fuentes han aprovechado las ligaduras para poder llevar esto a la realidad. Lo triste de esto es que no todos los editores de texto, IDE’s y terminales los soportan. Algo que debe quedar claro que sólo cambia la *representación* del texto, no los caracteres realmente escritos, por lo que no produce ningún problema con el código fuente.

Ahora sí, hablemos de algunas de las fuentes bonitas que podemos usar.

## Fira Code

![Fira code](https://cdn-images-1.medium.com/max/2000/0*_wmY1HhArgNtf--1.jpg)

Una fuente con ligaduras diseñada exclusivamente para programadores. Open Source y gratuita, la pueden encontrar en su [repositorio de Github](https://github.com/tonsky/FiraCode). Es derivada de Fira Mono y añade las ligaduras. Aquí un ejemplo de cómo cambian los caracteres en ligadura, extraído del repo de Github:

![Ligaduras de Fira Code](https://cdn-images-1.medium.com/max/2160/0*8Ud6Ss4VPLcR2nKi.png)

Si le quieren dar una oportunidad la pueden probar con [VS Code](https://code.visualstudio.com/).

## Monoid

Fuente monoespaciada semicondensada, también con ligaduras. Esta fuente al ser más condensada que Fira Code, permite tener más texto (código) en la pantalla, sin perder demasiada legibilidad. En [Medium](https://medium.com/larsenwork-andreas-larsen/designing-a-coding-font-b10cabd594fc#.chvb73c3c) explica las decisiones de diseño que tomó a través de varios artículos.

![](https://cdn-images-1.medium.com/max/2000/0*judcRlccKzjXz-8F.png)

## Hasklig

Fuente diseñada por y para programadores de Haskell (aunque no limitada para ellos), debido al extenso uso que hace de los símbolos compuestos como =>, ==, >-, -<<, ::, el creador decidió hacer un fork de la fuente Source Code Pro y añadirle ligaduras. Se puede descargar en su [repositorio de Github](https://github.com/i-tu/Hasklig).
 Aquí un ejemplo de cómo luce:

![](https://cdn-images-1.medium.com/max/2000/0*J4JomQCofwrPbqAV.png)

Y aquí cómo se verían esos caracteres en [Source Code Pro](https://github.com/adobe-fonts/source-code-pro):

![](https://cdn-images-1.medium.com/max/2000/0*OOk-BjFh8OLHN19E.png)

### Input

Input es una familia de fuentes tipográficas específicamente diseñadas para programadores, con propuestas bastante interesantes: ofrece fuentes proporcionales, monoespaciadas, serif y sans-serif.

¿Fuentes proporcionales para el código? David Jonathan Ross, el diseñador, dice que las fuentes monoespaciadas ni siquiera llegan a tomar en cuenta el grosor de la fuente, por lo que a veces el resaltado de la sintaxis puede producir resultados extraños, debido a que su espacio horizontal se mantiene constante, así las letras anchas se aplastan y las mayúsculas parecen estiradas al lado de las minúsculas.

![](https://cdn-images-1.medium.com/max/2000/0*aRObIWuheijDt52-.png)

Para resolver esto, su fuente proporcional intenta importar los atributos que hacen que una fuente monoespaciada sea atractiva: **símbolos de puntuación grandes, espaciado generoso y caracteres fáciles de reconocer individualmente**.

![](https://cdn-images-1.medium.com/max/2000/0*DRcoyMX3o-_lh5RH.png)

Una gran cualidad de esta fuente es que es completamente personalizable. Se pueden personalizar caracteres como **i**, **a**, **l**, **0** (cero) y también se puede escoger que tan condensada (espacio horizontal) está la fuente, este es muy valioso en el caso de tener una pantalla pequeña con líneas de código largas.

En su [página oficial](http://input.fontbureau.com) pueden encontrar una muestra, esto es un ejemplo de cómo puede llegar a verse:

![](https://cdn-images-1.medium.com/max/2000/0*iuA1UTTDs1xqUjBY.png)

El ejemplo anterior es con fuente monoespaciada, a mí me sigue gustando más.

En la [página de personalización](http://input.fontbureau.com/download/?customize) pueden descargarla completamente gratis para uso personal, en el caso de usarse en publicaciones y en web se tiene que pagar por ella.

### Operator Mono

Esta fuente la vi usada en un tutorial [Laracasts](http://laracasts.com) y me enamoré de ella, es una fuente monoespaciada sans-serif, diseñada para programadores y diseñadores, que tiene una característica que la hace muy notable: el estilo itálico cambia completamente del normal, se vuelve una fuente más estilizada, simulando las letras manuscritas.

![](https://cdn-images-1.medium.com/max/2046/0*Jf0p8R5uMnhStfHR.png)

Sus creadores pusieron [especial énfasis en las llaves y los corchetes](http://www.typography.com/blog/tag/Monospace).

Esta fuente no tiene ligaduras (aunque hay un proyecto que se las pone: [aquí](https://github.com/kiliman/operator-mono-lig)), no es Open Source y tiene un costo de $199 USD por los 10 estilos básicos. Se puede comprar en su [sitio oficial](http://www.typography.com/fonts/operator/overview/).

Si el tema de resaltado de sintaxis que usas hace buen uso de las cursivas esta fuente luce absolutamente hermosa.

## Proggy Fonts

Este sitio tiene varias fuentes de la familia Proggy, lucen con un toque retro pero se ven muy bien, sobre todo si te gusta el estilo de 8 bits.

Aquí un ejemplo:

![Ejemplo Proggy Square](https://raw.githubusercontent.com/bluescan/proggyfonts/master/ProggyVector/ProggyVector_SampleVS.png)

En el sitio puedes encontrar otras fuentes exclusivas para programar, todas gratis.

## Bonus

En [Programming Fonts](http://programmingfonts.org/) puedes encontrar más opciones si no te convenció ninguna de las que mostramos aquí. También puedes probar muchos [estilos diferentes](https://app.programmingfonts.org/).

En [este repo de Github](https://github.com/chrissimpkins/codeface) puedes encontrar más ejemplos.

_Nota: Este post es una actualización [de otro](https://medium.com/@HectorIP/fuentes-tipogr%C3%A1ficas-para-programadores-7d93c55f1223) que hice tiempo._
