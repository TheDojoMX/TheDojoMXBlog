---
title: "Análisis de los principios SOLID: Principio de Responsabilidad Única"
date: 2022-12-01
author: "Héctor Patricio"
tags: ['solid', 'principios']
description: "¿Son útiles los principios SOLID? En esta serie empezaremos una exploración para ver si podemos aplicarlos mejor o si vale la pena seguirlos."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1010/v1669958588/2113646631_star_explosion_Highly_detailed__surrealism__trending_on_art_station__triadic_color_scheme__smooth__sharp_focus__matte__elegant__the_most_beautiful_image_ever_seen__illustration__digital_paint__dark__gloomy__octane_render__8k__4k__otkltm.png"
draft: false
---

En esta serie de artículos vamos a hablar sobre los cinco **principios SOLID**. Se dice que todo programador que quiera crear código mantenible y _"limpio"_ debe conocer y usar. La estructura de los artículos llevará la siguiente forma:

- Explicación del principio
- Ejemplos y contraejemplos para pensar
- Críticas y alternativas

Esta serie de artículos surge debido a que **aunque son poco entendidos por la mayoría de los programadores**, estos principios se toman como _verdades universales_ que hay que seguir. Si queremos desarrollar buen software, no podemos ir por allí solamente aceptando lo que _la mayoría_ dice que está bien sin entenderlo a fondo y cuestionarlo.

Así que esta serie estará enfocada más bien en el lado débil de los principios SOLID y ver si tenemos mejores alternativas, o por lo menos, ver cuando podemos usarlos y cuando no.

Empecemos diseccionando el primer principio de los aclamados SOLID: el principio de Responsabilidad Única. Como verás a lo largo de los artículos, estos principios casi siempre se aplican con ejemplos de programación orientada a objetos, por lo que los verás explicados con _"clases"_ y _"objetos"_.

## El principio de Responsabilidad Única

Este principio se puede enunciar como:

> "Una clase debe tener una única razón para ser modificada" según en libro _Rober Martin_.

Otros lo enuncian como:

> Una clase debe hacer sólo una cosa y hacerla bien.

Esto es un resumen del principio que nos puede servir para ayudarnos a pensar sobre las _responsabilidades_ que nuestro código tiene, específicamente una clase. Pero, ¿qué es una _responsabilidad_? Aquí es donde empiezan a entrar los problemas al definir este principio y a tomar pasos prácticos para aplicarlo. Pensemos en algunos ejemplos:

- Una clase que se encarga de transformar un archivo de un formato en otro debería encargarse sólo de esta transformación. ¿En dónde empieza y dónde acaba la _responsabilidad_ de esta clase? ¿Tiene que encargarse de leer y guardar el archivo? ¿Debe existir una clase para guardar el archivo y otra para leerlo?

- Una clase que se encarga de la comunicación con la API, transformando las peticiones del programa interno en peticiones HTTP y transformando las respuestas de la API en objetos y tipos de datos internos. ¿Dónde acaba su _responsabilidad_?¿Es la encargada de verificar la condición de la red? ¿Se encarga de verificar que los datos sean correctos, o es responsabilidad de otra clase?

Como puedes ver, el principio, aunque suena simple, deja muchas cosas sin resolver y vagas, por lo que pocos encuentran un manera clara de aplicarlo. A mi me parece que tiene aplicaciones, pero solamente si acotamos más su alcance y definimos algunos límites, incluso cambiando el enfoque del consejo.

## El problema

El gran problema con este consejo es que la definición de lo que una **responsabilidad** significa es completamente arbitraria. Todo dependerá de quién esté dividiendo el problema más grande en _responsabilidades_. Además, esta división puede tener diferentes niveles de granularidad, por lo que una sola _responsabilidad_ a cierto nivel puede significar varias _responsabilidades_ en un nivel más bajo.

## Transformando el principio

¿Cuál es la _esencia_ del principio? Para mi el corazón de este consejo tiene que ver con controlar la **información** que una clase maneja. También tiene que ver con el **cambio**. Finalmente el consejo tiene que ver con la cantidad de información que podemos mantener en nuestra mente en un tiempo específico. Si una pieza de código hace demasiadas cosas, será difícil de entender y por lo tanto propensa a errores y omisiones.

La primera  cosa de la que vamos a hablar es de la **información**. La idea de que se encapsule una responsabilidad en un una clase es que si la información que tenemos sobre un problema cambia, se propague por la menor cantidad de código posible en nuestra base, rediciendo el impacto y la posibilidad de crear problemas.

Entonces, lo primero que tenemos que pensar es si el nivel de granularidad del que se está hablando (clases) es el correcto. Para mi, no se puede establecer un nivel de granularidad tan fijo, sino que dependerá del programador que decida dónde **encapsular o esconder** la información que esta responsabilidad maneja. Puede que sea un módulo, paquete, clase o función. Hay problemas grandes y pequeños.

Para aplicar esto, piensa:

- ¿Qué procedimientos, información y datos va a manejar esta pieza de código? Si no tienes claro esto, puede que te falte pensar un poco más en problema, e incluso dividirlo mejor.
- ¿Cómo puedo aislar la información que esta pieza de código maneja, de tal forma que si cambiar, no afecte a todo lo que está fuera de ella?
- ¿De dónde viene y a dónde va la información que esta pieza de código transforma?
- ¿Cómo puedo definir _exactamente_ qué hace esta pieza de código? Esta definición junto con la justificación de la decisión debería estar bien documentada.

## Técnicas para concretar el principio

- Divide en problemas (responsabilidades) bien definidas tu problema principal. No hay una forma correcta de hacerlo, estas divisiones siempre serán arbitrarias, así que trata de documentar estas decisiones lo mejor posible. Estas decisiones deben ser fáciles de entender en la medida de lo posible.

- Define exactamente que hará cada pieza de código que tenga una interfaz. Un módulo, una clase y una función tienen una interfaz, una parte que permite a otras piezas de código usar su funcionalidad interna. La función de esta interfaz es _esconder_ los detalles de implementación permitiendo el uso de la funcionalidad encapsulada. También esto debe estar bien documentado en el lugar adecuado. Documenta lo que hace, no cómo lo hace.

Estos dos puntos anteriores los puedes aplicar recursivamente a nivel cada vez más bajo, hasta que consideres que el problema es lo suficientemente pequeño como para resolverlo directamente.

El último consejo tiene varias partes, por lo que trataremos en un subtítulo aparte.

## Evita las fugas de información

Aunque tengamos completamente claro lo que una clase, módulo o función hace, nuestros detalles de implementación pueden dejar escapar información que no es conveniente que esté fuera de ella.

Piensa por ejemplo en la clase que se comunica con la API. ¿Qué pasaría si pasaras directamente los errores que la API da hacia las demás partes del código? Si esta parte cambia en el futuro, afectarás a todas estas partes que consumen esos errores.

Puedes seguir estos consejos para evitar fugas de información:

- Define estructuras de datos para comunicar información entre clases, módulos y funciones que sean uniformes a todos. Si alguien necesita un formato diferente, sólo lo transformará dentro de sus límites, siempre encargándose de devolver y  recibir la información en el formato correcto.

- Evita las dependencias temporales. Siempre que tienes que llamar las mismas funciones, clases o módulos en el mismo orden quiere decir que tienes una dependencia temporal. La información se está escapando en el orden de las llamadas. Piensa si estas piezas de código en realidad debieron ser una sola pieza.

- Evita usar la misma abstracción a diferentes niveles. Imagínate que estás haciendo una aplicación para editar texto. Tienes una clase central que se encarga de mantener el estado del texto. Esta clase tiene la interfaz básica para realizar todas las transformaciones necesarias básicas, pero no le puedes exponer esto al usuario. El usuario necesita comandos como Copiar, Pegar y Cortar. Sería una mala idea usar estas mismas abstracciones en tu clase central, porque encadenaría completamente tu interfaz con tu centro y viceversa. Por eso, la clase que maneja el código debe tener abstracciones más básicas, adecuadas para crear funcionalidades como Copiar, Pegar, Cortar, u otras, si se necesitara.

Todos estos consejos se tratan de mejor manera en el libro "A Philosophy of Software Design" de John Ousterhout, pero también me gustaría hacer eco de un consejo de Dan North: **Busca crear código simple.**

Esta fue la crítica y aplicación del principio de Responsabilidad Única. En el siguiente artículo veremos el principio de Abierto/Cerrado (Open/Closed Principle).
