---
title: "¿Qué es un API?"
date: 2023-03-15
author: Héctor Patricio
tags:
comments: true
excerpt: "Definamos que es un 'Application Programming Interface' en el desarrollo de software."
header:
  overlay_image: #image
  teaser: #image
  overlay_filter: rgba(0, 0, 0, 0.5)
---

A veces limitamos el uso de la palabra **API** a un programa que nos regresa información mediante una conexión web, generalmente en un formato que una máquina puede procesar. Pero muchas otras veces se usa de manera más amplia. En este artículo hablaremos de otras acepciones y qué tiene que ver con la buena programación.

## Application Programming Interface

La realidad es que el inicialismo "API" es casi auto-explicativo: Interfaz de Programación de Aplicación. Bueno, vamos a analizarlo un poco.

### Interfaz

Primeramente es un **interfaz**. Una interfaz es el lugar en donde dos sistemas o entidades convergen e **interactúan**. Podemos entender como interfaz a la parte que te permite usar un aparato electrónico, por ejemplo. En una computadora, su interfaz para los humanos son el teclado, la pantalla y el mouse o trackpad. En una televisión, la interfaz es la pantalla, el control remoto y los controles integrados en el cuerpo principal.

La interfaz normalmente **esconde** la mayor parte del sistema y muestra solamente las partes que son relevantes o _que se pueden usar_ por un sistema externo. En el caso de la computadora, ver o interactuar directamente con el procesador o la RAM no nos interesa, por eso la computadora expone un conjunto limitado de todas las características que la componen. Esta interfaz en realidad representa una **abstracción** de lo que el sistema completo es. Este elemento habilita y simplifica el uso de este sistema.

Las interfaces definen **la forma** de un sistema para entidades externas a él.

### Interfaz de Programación

Ya que sabemos que es una interfaz, ahora agreguemos el siguiente término: **programación**. Que sea un interfaz de programación nos indica la forma en la que esta interfaz puede ser usada: mediante el fino arte de la programación. Otra forma en la que creo que suena bien la traducción es _Interfaz Programática_. Así como las interfaces visuales se entienden mediante la visión, las interfaces programáticas se entienden y usan con **programas**.

¿Qué hace que una interfaz pueda ser usada de manera sencilla por un programa? Listemos algunas de las características:

1. La comunicación con la interfaz se puede hacer por medio un programa. La manera más sencilla es por medio de texto plano en formatos establecidos o formatos binarios. Estos pueden ser, por ejemplo, HTTP y para facilitar más las cosas JSON o XML. Hay formatos binarios usados como Protcolbuffers. Pero no **tiene** que ser ninguno de estos. Mientras el formato se pueda procesar de manera automática con un programa, es una interfaz de programación. Por ejemplo, una aplicación podría escribir a un archivo y la otra simplemente leerlo de ahí (ejem. así funcionan los _sockets_ en UNIX). O por ejemplo, la "aplicación" puede ser cargada en el mismo espacio de memoria y ser usada por el mismo entorno de ejecución.
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
