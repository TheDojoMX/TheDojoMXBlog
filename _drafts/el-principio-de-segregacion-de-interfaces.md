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

¿Te ha tocado llenar un formulario que te pregunta cosas que no te aplican? Por ejemplo un formulario que te pregunta por los datos de tus hijos independientemente si no tienes o no. Sin duda es molesto y una pérdida de tiempo.
## Generado automáticamente

El principio de segregación de interfaces es un concepto de diseño que se enfoca en dividir los sistemas en componentes independientes, cada uno de los cuales tiene una función claramente definida y una interfaz bien definida. El objetivo de la segregación de interfaces es reducir la interdependencia entre los componentes y aumentar la modularidad del sistema, lo que puede mejorar la flexibilidad, escalabilidad, mantenibilidad y seguridad del sistema.

En términos simples, el principio de segregación de interfaces implica separar los distintos componentes de un sistema en módulos distintos, cada uno con una función específica y bien definida. Cada módulo debe tener una interfaz clara y definida que permita la comunicación con otros módulos. Al mantener los módulos separados e interconectados solo a través de sus interfaces, se minimiza la complejidad y se reduce la posibilidad de que cambios en un módulo afecten a otros.

Este principio se aplica en una amplia variedad de sistemas, desde software y hardware hasta sistemas organizacionales y de gestión de proyectos. Por ejemplo, en el diseño de software, la segregación de interfaces se puede lograr mediante la implementación de interfaces claras y bien definidas para cada módulo del software, lo que permite una comunicación clara y efectiva entre los componentes. En una organización, la segregación de interfaces se puede lograr mediante la creación de equipos y departamentos separados, cada uno con su propia función y responsabilidades claramente definidas.