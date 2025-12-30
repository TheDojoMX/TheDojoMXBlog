---
title: "El principio de segregación de Interfaces"
date: 2023-04-01
author: "Héctor Patricio"
tags: ['solid', 'principios-solid', 'isp']
description: "Analicemos el cuarto principio de SOLID: El principio de segregación de interfaces, y veamos qué tanto vale la pena tenerlo en cuenta en nuetros desarrollos."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1669958588/3018709125_star_explosion_Highly_detailed__surrealism__trending_on_art_station__triadic_color_scheme__smooth__sharp_focus__matte__elegant__the_most_beautiful_image_ever_seen__illustration__digital_paint__dark__gloomy__octane_render__8k__4k__aexjen.png"
draft: false
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

## Ejemplos de aplicación

Empecemos con un ejemplo que nos pude ayudar a entender el problema y la solución mediante un conjunto de clases.

Usemos un ejemplo común este blog: una plataforma para enviar mensajes a diferentes canales, como Telegram, WhatsApp, Messenger, Instagram. Una forma de representar la interfaz de un mensaje sería la siguiente:

![Clase única](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_350/v1680394988/clase_texto_ylaj7m.png){: .align-center}

Aunque podríamos nombrar algunos de estos argumentos como opcionales (lo cuál evitaría que en estricto sentido los clientes estén forzados a usarlos), la interfaz sigue siendo confusa e impráctica. Por ejemplo, si quieres mandar algo por SMS, no tienes la opción de mandar tarjetas multimedia.

Una mejor solución sería crear un interfaz base, con especializaciones para cada caso. Por ejemplo:

![Composición de clases](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_800/v1680398494/Screen_Shot_2023-04-01_at_19.21.23_m7wuws.png){: .align-center}

Esta forma no sigue la herencia (un mensaje con tarjetas es un mensaje de texto), sino la composición (un mensaje con tarjetas tiene un mensaje de texto). Esto nos permite tener una interfaz más sencilla y fácil de usar, que puede ser especializada por cada caso.

## Llevándolo al extremo

Si llevamos este consejo al extremo, podemos quedar con una cantidad tan grande de interfaces y tan especializadas que el código quedaría más difícil de entender y mantener. Imagínate el infierno que sería navegar por ese código. **Recuerda que las interfaces son simplemente la parte accesible de una funcionalidad**. Ousterhout dice que a veces, la complejidad viene de la cantidad de cosas con las que tenemos que tratar.

Además, separar el código a veces conlleva código extra: el que se usa para seleccionar qué interfaz o código usar.

Así que la pregunta básica es: ¿cuándo debo separar o romper código que hace algo en partes más pequeñas? Pensar que este principio es la guía más fuerte es un error, el análisis debe ir mucho más al fondo, no sólo pensar en las interfaces y si alguien está "obligado" a implementar o lidiar con cosas que no usa.

Por ejemplo, ¿qué pasa si el 90% de las veces que vayas a usar un módulo como una función vas a usarla en la versión más complejas? ¿Valdrá la pena separarla en dos funciones? Yo creo que vale más la pena que los lugares donde no la usas completa, se trate de manera especial.

Para un análisis más profundo, escribiré un artículo basado en el capítulo "Better Together o Better Apart?" de [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php) de John Ousterhout.

## Conclusión

Aunque es una buena idea que las interfaces sean demasiado complejas para no forzar al código que las usa a implementar cosas que no le corresponden, llevarlo al extremo podría hacer que tu base de código sea más compleja de lo que empezó.

Este principio de diseño no debería ser la única fuente de decisión para saber si deber _segregar_ o como diríamos más cotidianamente _separar_ una interfaz. Recuerda que al separar la interfaz estás separando la implementación y la lógica de tu programa, por lo que debes pensarlo muy bien antes de hacerlo.

Finalmente, es muy poco probable que te pase algo similar si piensas en hacer interfaces que sean lo más sencillo posible.
