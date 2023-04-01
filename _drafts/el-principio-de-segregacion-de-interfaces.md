---
title: "El principio de segregación de Interfaces"
date: 2023-03-26
author: Héctor Patricio
tags: solid principios-solid isp
comments: true
excerpt: "Analicemos el cuarto principio de SOLID: El principio de segregación de interfaces, y veamos qué tanto vale la pena tenerlo en cuenta en nuetros desarrollos."
header:
  overlay_image:https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1669958588/3018709125_star_explosion_Highly_detailed__surrealism__trending_on_art_station__triadic_color_scheme__smooth__sharp_focus__matte__elegant__the_most_beautiful_image_ever_seen__illustration__digital_paint__dark__gloomy__octane_render__8k__4k__aexjen.png
  teaser:https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1669958588/3018709125_star_explosion_Highly_detailed__surrealism__trending_on_art_station__triadic_color_scheme__smooth__sharp_focus__matte__elegant__the_most_beautiful_image_ever_seen__illustration__digital_paint__dark__gloomy__octane_render__8k__4k__aexjen.png
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Continuemos con el estudio de los principios SOLID. En esta ocasión hablaremos del cuarto principio: El principio de segregación de interfaces.

Recuerda que el objetivo de estos artículos **no es explicártelos como si fueran una religión que estás mal si no sigues**, sino analizarlos bajo una luz crítica y decidir si de verdad son útiles o podemos usar otro principio.

Analicemos primero el enunciado, junto con algunos ejemplos y veamos si nos conviene aplicarlo directamente o no.

## El principio de segregación de interfaces

La frase que define el principio es:

> Los clientes no deberían ser forzados a depender de interfaces que no usan.

Creo que el nombre y este enunciado lo hace sonar demasiado complicado para lo que es: se trata de pensar bien tus interfaces para que no sean lo más sencillo que se pueda. _"Los clientes"_ son todas las partes del código que usan **una interfaz**.

Al hacer tus interfaces lo más sencillas que puedas, evitarás que los clientes tengan que implementar métodos que no usan, y que no deberían tener que implementar.

Pongamos un ejemplo de la vida real:

¿Te ha tocado llenar un formulario que te pregunta cosas que no te aplican? Por ejemplo un formulario que te pregunta por los datos de tus hijos independientemente si no tienes o no. Sin duda es molesto y una pérdida de tiempo. Aquí, te están forzando a cumplir con una interfaz que no usas.

Lo mismo exactamente puede pasar con el software. Si una interfaz, por ejemplo, al usar un método con muchos parámetros obligatorios que no siempre se ocupan, o una clase con métodos que corresponden a otros usos.

Esto se puede dar cuando tienes una clase o una función que implementa algo que puede ser ocupado en diversos lugares (estos son sus _clientes_). Imagina que los diferentes lugares tienen ligeras variaciones, por las que hay que modificar la interfaz para que se pueda usar en cada uno de ellos. Hacer esto te llevaría a crear una interfaz complicada de usar y además frágil.

Es por esto que John Ousterhout da varios consejos relacionados:

1. Mientras más simple la interfaz, mejor.
2. Son mejores los módulos de propósito **general**, que después puedan ser especializados o combinados para crear interfaces específicas, para cada caso.
3. Crear las interfaces pensando en el caso más común.

Sin embargo, este último consejo de Ousterhout puede ir en contra de este principio, pero aquí preferimos la practicidad sobre la pureza. Más adelante daremos un ejemplo.

## Ejmplos

