---
title: "A Philosophy of Software Design: Ocultar información"
date: 2020-03-07
author: "Héctor Patricio"
tags: ['APoSD', 'interfaces', 'módulo', 'complejidad', 'diseño-de-software']
description: "Ocultar información es una de las claves para reducir la complejidad, veamos algunas maneras de lograrlo."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1800/v1583357998/IMG_3866_owfbzj.jpg"
draft: false
---

> La idea básica es que cada módulo debería encapsular algunas piezas de conocimiento, que representen decisiones de diseño. - **John Ousterhout**

En [el artículo anterior](https://blog.thedojo.mx/2020/03/02/a-philosophy-of-software-design-los-modulos-deben-ser-profundos.html) vimos por qué es bueno que los módulos sean profundos, es decir, oculten detalles de implementación y funcionalidades detrás de una interfaz lo más sencilla posible. En este y los siguientes artículos vamos a ver maneras prácticas de lograr esto, basado en ejemplos de ["A Philosophy of Software Design"](https://amzn.to/2H92nwA).

En este artículo hablaremos de cómo **ocultar información** que no es necesaria saber para usar los módulos, ya que complicaría su uso, creando [carga cognitiva](https://blog.thedojo.mx/2020/02/26/tres-formas-de-identificar-la-caomplejidad-posd6.html#carga-cognitiva), uno de los síntomas y consecuencias de la complejidad innecesaria.

Para saber cómo esconder la información debemos entender por dónde se escapa, prácticas comunes que llevan a un mal diseño y que pueden hacer que nuestro programa sea difícil de entender y mantener.

## Fugas de información

Tener fuga de información es revelar información que no deberíamos, porque se rompe el propósito del encapsulamiento en el módulo.

Recuerda la cita del principio: un módulo tiene que ocultar y mantener _decisiones de diseño_. Si esta decisión cambia y tienes que modificar varios módulos, tienes una fuga de información. En otras palabras, **una fuga de información sucede cuando una decisión de diseño se ve reflejada en varios módulos**.

Ejemplo. Piensa en una clase se conecte a una API para obtener información relacionada con los códigos postales. Para todos los usuarios de esta clase, debería ser **irrelevante** qué API se está usando, si es una API HTTP externa, un archivo gigantesco con todos los datos, una base de datos o lo que sea, mientras la clase cumpla con su trabajo.

Si al hacer cambios en esta decisión de diseño tienes que cambiar otras cosas a parte de esta clase, tienes algún tipo de fuga de información. ¿Ya pensaste en las formas en las que se puede escapar la información?

John Ousterhout sugiere hacerte la siguiente pregunta:

> ¿Cómo puedo reorganizar estas clases para que esta parte del conocimiento general sólo afecte a esta clase?

Veamos un ejemplo de una fuga de información. Piensa en una aplicación en la que la principal tarea sea obtener el estado del clima y mostrarlo al usuario. Para esto usaremos una API que nos dará los datos y nosotros seremos los encargados de mostrarla.

Una pieza de información importante para obtener el clima es ala ubicación. Considera que la API actual recibe el nombre de la ciudad para devolver las predicciones meteorológicas.

Veamos dos diseños:

1. En este escenario hacemos que la inicialización de la clase o cada una de las llamadas a sus métodos para obtener los diferentes valores manden el nombre de la ciudad de los datos que buscamos. Así, si buscamos los datos acerca de México mandamos "México" como parámetro para obtener la temperatura.

2. En otro escenario decidimos que aunque la API reciba el nombre de la ciudad, nuestra clase recibirá las coordenadas e internamente obtendremos el nombre de la ciudad de esas coordenadas y lo mandaremos a la API. Es probable que para esta transformación usemos otra clase u otro paquete.

¿Qué diseño te parece correcto?

En el diseño 1 estamos revelando información acerca de  _la implementación_ de esta API específicamente. ¿Qué pasaría si tenemos que cambiar de API y la próxima necesita las coordenadas en vez de el nombre de la ciudad? Tendríamos que cambiar el diseño en la clase de la API y en los lugares en los que se usa.

En el segundo diseño estamos ocultando más detalles detalles de implementación, ya que las coordenadas son una forma más natural de comunicar lugares y es probable que se lo que se obtenga del usuario (por ejemplo, desde su geolocalización por dispositivo). La transformación de las coordenadas en un nombre de ciudad quita carga del usuario de nuestra clase.

¿Puedes pensar en otros ejemplos? En el libro [PoSD](https://amzn.to/2H92nwA) vienen algunos.

En el próximo artículo hablaremos de otra forma de fugas de información: la descomposición temporal.
