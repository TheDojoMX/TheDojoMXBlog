---
title: "¿Qué es una API?"
date: 2023-03-18
author: "Héctor Patricio"
tags: ['apis', 'abstracción', 'diseño-de-software', 'definiciones']
description: "Definamos que es un 'Application Programming Interface' en el desarrollo de software. Y con este entendimiento, hablemos de cómo hacer mejores API's."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/v1674189353/266979132_mad_alligator_scientist_looking_at_a_screen_with_binary_code__concept_art___artstation__HQ__4k_nkojwn.png"
draft: false
---

A veces limitamos el uso de la palabra **API** a un programa que nos regresa información mediante una conexión web, generalmente en un formato que una máquina puede procesar. Pero muchas otras veces se usa de manera más amplia. En este artículo hablaremos de otras acepciones y qué tiene que ver con la buena programación.

## Application Programming Interface

La realidad es que el inicialismo "API" es casi auto-explicativo: Interfaz de Programación de Aplicación. Bueno, vamos a analizarlo un poco.

### Interfaz

Primeramente es un **interfaz**. Una interfaz es el lugar en donde dos sistemas o entidades convergen e **interactúan**. Podemos entender como interfaz a la parte que te permite usar un aparato electrónico, por ejemplo. En una computadora, su interfaz para los humanos son el teclado, la pantalla y el mouse o trackpad. En una televisión, la interfaz es la pantalla, el control remoto y los controles integrados en el cuerpo principal.

La interfaz normalmente **esconde** la mayor parte del sistema y muestra solamente las partes que son relevantes o _que se pueden usar_ por un sistema externo. En el caso de la computadora, ver o interactuar directamente con el procesador o la RAM no nos interesa, por eso la computadora expone un conjunto limitado de todas las características que la componen. Esta interfaz en realidad representa una **abstracción** de lo que el sistema completo es. Este elemento habilita y simplifica el uso de este sistema. Las interfaces definen **la forma** de un sistema para entidades externas a él.

Una interfaz podría entenderse como un iceberg: la parte "visible" o con la que puedes interactuar es la punta, mientras que la gran masa es la funcionalidad que está oculta y a la que no puedes acceder.

![Una interfaz es como un Iceberg](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_800/v1679188585/Ilustracio%CC%81n_sin_ti%CC%81tulo_3_fi05qn.png){: .align-center}

(Probablemente ese iceberg está mal dibujado: [The topple of an iceberg: You're drawing it wrong](https://axbom.com/iceberg/))

### Interfaz de Programación

Ya que sabemos que es una interfaz, ahora agreguemos el siguiente término: **programación**. Que sea un interfaz de programación nos indica la forma en la que esta interfaz puede ser usada: mediante el fino arte de la programación. Otra forma en la que creo que suena bien la traducción es _Interfaz Programática_. Así como las interfaces visuales se entienden mediante la visión, las interfaces programáticas se entienden y usan con **programas**.

¿Qué hace que una interfaz pueda ser usada de manera sencilla por un programa? Listemos algunas de las características:

1. La comunicación con la interfaz se puede hacer por medio un programa. La manera más sencilla es por medio de texto plano en formatos establecidos o formatos binarios. Estos pueden ser, por ejemplo, HTTP y para facilitar más las cosas JSON o XML. Hay formatos binarios usados como [Protcol Buffers](https://protobuf.dev/). Pero no **tiene** que ser ninguno de estos. Mientras el formato se pueda procesar de manera automática con un programa, es una interfaz de programación. Por ejemplo, una aplicación podría escribir a un archivo y la otra simplemente leerlo de ahí (ejem. así funcionan los _sockets_ en UNIX). O por ejemplo, la "aplicación" puede ser cargada en el mismo espacio de memoria y ser usada por el mismo entorno de ejecución.
2. La interfaz puede recibir peticiones o instrucciones creadas por un programa. Muy en la línea del punto anterior, la interfaz debe exponer formas de que otro programa la llame mediante medios programables.

Si la interfaz cumple con esto, entonces es una interfaz de programación.

### Interfaz de Programación de Aplicación

El último término nos dice a quién la pertenece esta interfaz: **a otra APLICACIÓN**. Esto nos dice que la interfaz pertenece a un programa para que **otro programa se comunique**.

Resumen: un API es lo que permite la comunicación entre dos programas de manera automática, es decir, sin que tengan que intervenir humanos en esa comunicación. Le permite a un programa usar otro.

Con el tiempo, lo que llamamos _"aplicación"_ se ha extendido para referirse a cualquier programa o parte de un programa, como un módulo, una clase, etc.

### Uso de "API" en el contexto actual

Recapitulemos: una API es una interfaz entre dos programas, que permite a ambos una comunicación unidireccional o bidireccional.

El uso más común tiene que ver con interfaces que tienen comunicación a través de una red de computadoras, como Internet. Normalmente son un servidores HTTP que pueden responder con formatos que pueden ser procesados de automáticamente de manera sencilla, los más comunes son JSON y XML.
Dependiendo de los estándares que sigan, estas API's pueden ser llamadas **RPC** (Remote Procedure Call), **ReST** (Representational State Transfer) o **SOAP** (Simple Object Access Protocol).

Este tipo de comunicación a través de la red tiene varias versiones, no sólo HTTP. Por ejemplo, existen alternativas más modernas como **gRPC** (Google Remote Procedure Call), que usa HTTP2 como medio de transporte y Protocol Buffers com formato de serialización (el lenguaje que puede ser fácilmente procesado por otro programa).

Seguro existen muchas otras formas de crear un API en un sistema distribuido pero la idea básica ya la tienes. Este es el uso más común de la palabra.

Ahora hablemos de otro uso de la palabra: en el diseño de software.

### API's en el diseño de software

Cuando se usa la palabra API en contexto de diseño de software, normalmente se refiere a la interfaz que otro sistema, módulo, o en general, componente del software presenta.

Por ejemplo, podemos decir que una clase tiene un API en el sentido de que presenta una cara a los demás parte del sistema para que lo usen, pero sobre todo **oculta** la implementación de las funciones que da. Como te podrás dar cuenta, una API es la parte pragmática de una [abstracción](/2023/03/13/que-es-la-abstraccion.html), y por eso es importante entenderlas.

El diseño del API de tus módulos, clases y aplicaciones en general es importantísimo para hacer buen software.

Retomando lo que siempre repetimos en este blog: **las interfaces bien diseñadas te permiten ocultar información** que no quieres que otras partes del sistema tengan en cuenta.

Por ejemplo en [Elixir](https://elixirlang.com), la forma de crear separación entre diferentes partes del sistema, a parte de módulos, son lo que llamamos **aplicaciones**. Esta aplicación puede tener un API bien definida que permita que sea 1) fácil de usar 2) que oculte todos los detalles de implementación posibles para que no se escape nada de información no concerniente a otras aplicaciones.

### Cómo diseñar una buena API

En esta sección voy a mencionar lo que a mi me ha servido para crear interfaces que, al mismo tiempo que son fáciles de usar, son efectivas escondiendo información.

**Las interfaces deben tener una complejidad relativa a la funcionalidad que están ocultando**. Es decir si tienes una función o clase que hace muy poquito, como por ejemplo, hacer un cálculo sencillo y casi auto-explicativo, no te conviene que tengas que pasar veinte datos diferentes para que lo puedas usar, lo único que vas a lograr es que tu programa sea más complicado de usar. En cambio, si la funcionalidad que está detrás de la API es grande y compleja, por supuesto que vale más la pena que la interfaz sea más compleja y requiera que pienses más para usarla.

Como analogía: el control de una bicicleta consiste en un manubrio análogo, mientras que el de un avión tiene decenas (¿tal vez más de 100?) de botones.

Esto está muy relacionado con el concepto que John Ousterhout presenta en ["A Philosophy of Software Design"](https://amzn.to/2H92nwA): crear módulos profundos, es decir, que tengan una interfaz lo más pequeña posible en relación con su funcionalidad, que debe ser lo más grande posible. Como un iceberg.

**Documenta bien las interfaces**. No sirve de mucho una interfaz que nadie sepa como usar. Como en las películas de ciencia ficción donde encuentran aparatos que nadie tiene idea de cómo funcionan, así nos puede pasar con una pieza de software. La documentación de la interfaz debe incluir, además de los nombres de los métodos o llamadas, los tipos de datos esperados (enteros, flotantes, cadenas, fechas), el comportamiento dependiendo de la entrada y el tipo y estructura de la información que devuelve. Es supremamente importante además que se mencione si el uso de la interfaz tiene un efecto secundario, como el disparo de un correo, la creación o manipulación de un archivo.

**Explica la razón de ser**. Esta parte de la documentación cuenta como un ejercicio que tiene dos objetivos: aclararte a ti mismo la razón de la existencia de la interfaz (aquí te vas a dar cuenta de que tal vez no vale la pena crearla o de que debe ser diferente de alguna forma). Si encuentras una buena explicación, entonces definitivamente el contenedor que tiene una API debe ser creado, y lo que vale la pena ser creado en programación, vale la pena ser documentado.

**No ocultes información demasiado temprano**. Los puntos anteriores te pueden ayudar a no caer en este error, pero por si las dudas vamos a dejarlo claro: no tienes por qué separar o crear abstracciones de todo y ponerlo detrás de una API. La separación de implementaciones a final de cuentas puede crear una carga extra: cómo transferir la información. El caso más claro es el de las interfaces que se comunican a través de un red, en las que necesitamos usar una capa de transporte. Pero en otras ocasiones también implica un poco de trabajo extra, que puede no valer la pena si no estamos en la etapa correcta.

## Ventajas de usar un API bien diseñada

Usar un API tiene varias ventajas, pero yo veo tres principales que pueden llevar tu desarrollo a niveles que no esperabas. Hablemos de ellas y tú evaluarás si es algo que te interese.

### Menor carga cognitiva

Al separar tu software en varios componentes o aplicaciones que trabajen mediante interfaces, puedes reducir el número de cosas que tienes que mantener en la cabeza debido a que no te preocuparás por todos los detalles: solamente te interesarás por la interacción entre las API's o tu software y un API.

Esto es justo lo que pasa cuando un front-end se hace separado de un backend. Después de establecer la forma de la API, cuando trabajas en un lado, en front por ejemplo, sólo te preocupas de mostrar los datos que sabes a recibir de la interfaz sin preocuparte de los detalles de procesamiento o de almacenamiento de información de los que el backend se hace cargo.

### Mejor evolución del software

Esto se logra gracias a que, si los diferentes componentes de un sistema están comunicados por API's claramente definidas, que además protejan bien los detalles de implementación de escaparse, estas partes pueden cambiarse internamente sin necesidad de afectar a otras parte si la forma de la interfaz se respeta. Además permite extender el software si creamos otro componente con la misma interfaz pero otro funcionamiento, por ejemplo.

Podríamos decir que las piezas son intercambiables, tal como cuando tienes un foco que se descompone y quieres reemplazarlo por otro, o simplemente quieres cambiar tu viejo foco incandescente por uno de led. Mientras consigas uno con la misma interfaz y que trabaje con el mismo voltaje, no importa la "implementación", es decir, cómo cumpla con su función de entregar luz: podría ser otro incandescente, fluorescente, de led, o incluso podrías poner una cámara o un ventilador.

Esto se puede llevar al extremo si la interfaz que estás usando está estandarizada y tienes un programa que sepa utilizar este tipo de interfaces automáticamente. Por ejemplo esa es la idea de ReST y GraphQL.

![Power plug](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_800/v1679188820/paul-hanaoka-RJkKjLu8I9I-unsplash_o5k8ex.jpg){: .align-center}

Las interfaces proveen la función de **"plug and play"**, mientras el aparato tenga la misma interfaz, podemos conectar cualquier cosa, como en los contactos eléctricos.

### Mejor separación del trabajo

Esto se puede inferir del comentario que hicimos, en el primer punto de las ventajas de usar un API. Si creas una interfaz estable y bien documentada, puedes delegar el trabajo de implementar las funciones detrás de esa interfaz a otra personas, otro equipo o de plano otra empresa.

En Open Source, por ejemplo, después de definir la API de un componente y hacer una implementación de referencia, se deja en manos de la comunidad crear otras implementaciones de ese módulo.

## Cómo decidir los módulos

Finalmente, surge la pregunta, ¿cómo puedo decidir qué irá detrás de una interfaz y cómo crear la separación de funciones entre módulos?

De eso hablaremos en un artículo futuro, basándonos en un artículo de David L. Parnas, ["On the Criteria to be Used in Decomposing Systems into Modules"](https://www.win.tue.nl/~wstomv/edu/2ip30/references/criteria_for_modularization.pdf).

## Conclusión

Lo importante de saber que es un API es entender su función y tener técnicas para diseñarlas lo mejor posible. Recuerda, un API no se limita a un servidor web que sirve JSON, sino que es toda aquella interfaz que puede ser usada con un programa. De ahí que los navegadores expongan API's como la File API, Fetch API, Device API, [etc.](https://www.educative.io/answers/what-are-browser-apis){:target="_blank"}, que no tienen nada que ver con una API de un servidor web, sino con el **uso de otras partes del software** y que mediante esta interfaz nos olvidamos de los detalles de implementación.

Cuando a ti te toque diseñar un API, recuerda su principal función: separar dos partes de un software al mismo tiempo que permites la comunicación.
