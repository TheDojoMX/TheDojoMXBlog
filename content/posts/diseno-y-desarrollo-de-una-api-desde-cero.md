---
title: "Diseño y desarrollo de una API RESTful desde cero - La importancia de diseñar tu API"
date: 2019-05-06
author: "Héctor Patricio"
tags: ['apis', 'rest', 'soap']
description: "El primer artículo de la serie. ¿Por qué es importante diseñar de antemano tu API? Compararemos dos de los estilos más populares: SOAP vs REST"
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1557201862/edho-pratama-149011-unsplash_jlppci.jpg"
draft: false
---

En este post explicaré **los principios básicos de diseño de una API**. Esta primera parte es bastante teórica, empezaremos con la práctica (no con la programación, sino con el diseño) en un post posterior.

Primero hablemos de la importancia del diseño o la arquitectura de la API. En la serie de posts hablaremos de API's para consumo web, a través de HTTP, ya que son las de mayor uso y popularidad.

## La importancia de diseñar tu API

Aunque parezca una tarea aburrida, innecesaria o burocrática, elegir un estilo de diseño de API's te servirá de las siguientes maneras:

1. **Mayor facilidad de desarrollo**. Tener una forma de nombrar los endpoints (los links con los que los sistemas externos interactúan), una estrucutra de respuesta, un estándar de errores y otras cuestiones definidas de antemano te permitirá pasar directo al diseño e implementación de las funcionalidades cuando llegue el momento. Si escoges usar una estructura de diseño común y popular puede que incluso haya herramientas que te faciliten la tarea. Nuestra API estará preparada para ser mantenible y escalable.
2. **Familiariadad**. Si sigues un patrón de diseño común, cuando otros desarrolladores usen tu API la entenderán más fácil y podrán comenzar a sacarle provecho más rápido.
3. **Menos documentación**. Aprovechando lo anterior, puede que gran parte de la estructura y prácticas comunes del patrón que escogiste ya estén documentadas, por lo que normalmente tendrás que documentar sólamente las partes que son especeificas de tu API.

El trabajo extra que pongas en diseñar tu API o por lo menos escoger un patrón de diseño común te ahorrará trabajo en el futuro, a tu equipo y a otros desarrolladores.

Dependiendo de la época y las necesidades han surgido varios estilos o patrones de diseño comunes. Aquí hablaremos de dos de los más usados a lo largo del tiempo y de los más populares.

## SOAP (Simple Object Access Protocol)

Este es el estilo de servicios más usado en el mundo empresarial. En realidad es un protocolo que establece desde la manera de comunicación hasta el lenguaje usado para transferir datos, entre otras cosas.
Su nombre es un acrónimo que signfica *Simple Object Access Protocol (Protocolo simple de acceso a objetos)* y fue desarrollado por Microsoft inicialmente. El lenguaje que se usa para transferir datos es [XML](https://www.w3schools.com/xml/xml_whatis.asp) y tiene varios estándares que definen cada aspecto de la comunicación, por lo que no se queda en sólo un estilo de diseño de API's. Su objetivo original era definir cómo acceder y usar servicios web.

Una de las partes más fuertes del protocolo es la manera en que establece un contrato con el cliente acerca de la forma de usar los serivicios que expone. El archivo [WSDL](https://www.w3.org/TR/2001/NOTE-wsdl-20010315) contiene la descripción de los serivcios expuestos en un lenguaje exclusivamente creado para eso, el *Web Service Description Language*, que se vale de XML. En este archivo define los servicios que la API provee, mediante la definición de una colección de endpoints, mensajes y tipos de datos. Este documento permite automatizar la creación de clientes mediante código.

### Ventajas de SOAP

1. **Pensado para transacciones complejas**. Una parte de SOAP está pensada para usarse con **transacciones**. Si lo que requieres es que tu API realice transacciones [ACID](https://en.wikipedia.org/wiki/ACID_(computer_science)), trabajar con SOAP te facilitará la vida.
2. **Establece cada parte de la comunicación**. Esto puede ser una ventaja o una desventaja, pero si estás con una tecnología que lo permite y aprovecha, trabajar con SOAP puede ser rápido y sin dolor, ya que los estándares estarán implementados en la platafoma/lenguaje y las herramientas de programación pueden aprovecharse de los estándares para facilitarte la vida.
3. **Interfaz definida**. Mediante el documento WSDL, SOAP permite la lectura de la interfaz (los endpoints), los tipos de datos y sus mensajes, así como las acciones que se pueden realizar de manera automatizada, lo que hace sencillo entender y consumir la API, incluso de manera automatizada mediante una herramienta que cree el cliente automáticamente o un paquete de tu lenguaje que te facilite la vida.

### Desventajas de SOAP.

1. **XML**. Parsear y procesar XML es en geneal más difícil y requiere más pasos que hacer con otros lenguajes de transmisión de datos usados con otros estilos de API's, pero esta deventaja sólo aplica si tu lenguaje y herramientas de desarrollo no soportan completamente los protocolos establecidos por SOAP. Así que la experiencia que tengas con SOAP depende en gran medida de las cosas implementadas por los lenguajes y herramientas en que programarás en el lenguaje (por ejmplo, los IDE's para C# y Java soportan recibir el WSDL para automatizar gran parte del proceso de crear un cliente)
2. **Velocidad**. Al ser un protocolo más complejo, aumenta la cantidad de procesamiento y transferencia de datos requerido para funcionar, lo que lo hace más lento que otras alternativas. Además, no es fácilmente cacheable, por lo que cada respuesta tiene que ser única y por lo tanto requiere mayores recursos.

### Conclusión acerca de SOAP

Muchos desarrolladores, sobre todo con poca experiencia, se escandalizan cuando tienen que trabajar en un API SOAP, sobre todo las generaciones recientes, y sí es un problema cuando tus herramientas no hacen fácil trabajar con este tipo de API's (como con cualquier otro tipo de desarrollo, tecnología o protocolo). Sin embargo, sus características las hacen ideales para API's transaccionales, por lo que es conveniente escorger este tipo de API's en los casos adecuados. Además, puedes beneficiarte de su forma de establecer la interfaz de manera clara y estricta. **Cada herramienta fue creada con un propósito y tiene sus usos adecuados.**

## API's RESTful

Una API REST aprovecha el diseño de las peticiones HTTP para crear servicios web con interfaces intuitivas.
REST son las siglas de "Representational State Transfer" (Transferencia de Estado Representacional), que es un estilo de arquitectura de sistemas distribuidos (podemos pensar en la web como un sistema distribuido).
Este estilo establece 6 características que se deben de cumplir para que un sistema sea considerado RESTful:

1. Arquitectura cliente-servidor. Existe un programa encargado de hacer peticiones (cliente) y uno encargado de responderlas (servidor).
2. Interfaz uniforme. Todos los clientes deberían acceder a la misma interfaz. Si el servidor cumple con la interfaz, puede haber un número ilimitado de clientes independientes que cambian sin dependencias entre ellos o con la implementación del servidor. *Esta es una de las razones principales por las que las API's REST son tan usadas actualmente.* Este punto lo trataremos más a profundidad en el siguiente artículo. Pero para cumplir esto mencionemos brevemente qué principios debe seguir esta interfaz para que cumpla con este propósito:
  - **Basada en *recursos***. Las URL's de los endpoints hacen referencia a _recursos_, es decir, a elementos de datos que pueden ser representados como objetos con un tipo, datos asociados, relaciones con otros objetos y las operaciones que se pueden realizar sobre él.
  - **Manipulación de recursos mediante *representaciones***. La API no devuelve nunca el recurso original al cliente que lo solicita o solicita una operación sobre él, sino que lo hace a través de alguna _representación_ de este recurso. Una representación es un subconjunto de los datos de recurso transmitido en un lenguaje adecuado: HTML, XML, JSON, MessagePack, etc.
  - **Mensajes autodescriptivos**. Cada mensaje tiene suficiente información en sí mismo para ser procesado.
  - **HATEOAS**. Estas son las siglas de **Hypermedia As The Engine Of Applicaton State** (Hypermedia como el motor del estado de la aplicación). La palabra [hypermedia](https://smartbear.com/learn/api-design/what-is-hypermedia/) se refiere a un formato de texto (o hypertexto) que contiene links hacia otros documentos, imágenes, video y audio. Es una forma de mostrar las relaciones que existen conceptualmente en una red de información, incluyendo formatos más allá del texto. Por lo tanto, este punto se refiere a que la API debería ser navegable con la información expuesta en cada respuesta, las relaciones con otros recursos, los links a otros documentos y achivos. [El autor](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven) de la deficinición de API's REST hace enfásis en que no está casada con ningúna forma de transporte o protocolo de comunicación, pero su implementación bien puede depender de que el protocolo de comunicación tenga las características básicas como el usar URI's para identificación. Todo el estado de la aplicación necesaria para funcionar será transmitido a partir de hypermedia. En el caso del HTTP, se usan las URL's con su cadena da consulta (query string), las cabeceras y los cuerpos de petición y respuesta para mantener este estado.

3. Sistema sin estado. Las conexiones entre los sistemas (cliente y servidor) no deberían dependender de un estado creado o mantenido a través de peticiones anteiores. Todo lo necesario para generar una respuesta se encuentra en la petición actual.
4. Cacheable. Las respuestas pueden ser guardadas para ser contestadas más rápidamente por el mismo servidor o por un sistema intermedio.
5. Sistema en capas. El sistema puede estar construido por varias capas de servicio y esto debe ser transparente para los clientes (no tienen que modificar sus llamadas).
6. Código bajo demanda. El servidor debe ser capaz de envíar código a cliente para que sea ejecutado.


### Ventajas de REST


1. **Flexibilidad**. REST no define el lenguaje de transferencia de datos, el tipo de autenticación y otros detalles de la comunicación que se dejan a discreción de los implementadores. En la actualidad, la mayoría de las API's REST usan JSON como lenguaje de transeferencia, pero bien podrían usar XML o MessagePack, incluso un lenguaje propietario.
2. **Popularidad**. La extensión de uso de API's RESTful ha hecho que proliferen herramientas para construirlas, probarlas y ponerlas en producción, por le que es muy sencillo desarrollarlas, aunque no deja de presentar retos.
3. **Escalabilidad**. Esta es una de las razones por las que las API rest se han vuelto tan populares. Incrementar la cantidad de usuarios que se pueden atender con una API RESTful es más sencillo que son SOAP debido a la cacheabilidad y a que las conexiones sin estado permiten escalamiento horizontal (replicación de servidores) y por lo tanto los costos se abaratan. La mayoría de las API's grandes conocidas siguen este estilo.

### Desventajas de REST

1. **Flexibilidad**. La flexibilidad es un don y maldición. Cuando a las personas se les permite hacer lo que sea, harán hasta lo inimaginable, por lo que se pueden encontrar implementaciones horribles y sin una guía definida nuestra propia API puede quedar hecha un asco.
2. **Transacciones**. REST no establece una manera de manejar operaciones transaccionales, por lo que la implementación queda completamente del lado del diseño. Hay que tener en cuenta el manejo del estado, replicación de servidores, consistencia y [condiciones de carrera](https://es.wikipedia.org/wiki/Condici%C3%B3n_de_carrera). Esto no hace sencillo trabajar con transacciones en API's REST.
3. **Seguridad**. No estamos diciendo que REST sea más inseguro que SOAP, sino REST no establece los medios de protección de interacciones e información, por lo que queda completamente como decisión de los desarrolladores y arquitectos del sistema. Sin una implementación adecuada tu API quedará vulnerable.


## Otros estilos

Han surgido nuevas maneras de consumir y diseñar API's como [GraphQL](https://graphql.org/learn/) y [gRPC](https://grpc.io/), pero cada una merece su propio artículo.

## Nuestra API

Para crear nuestra API elegiremos el estilo RESTful, por su popularidad y porque lo que aprendamos tendrá aplicaciones útiles inmeditas y en el futuro.

En el camino aprenderemos:

- Cómo dieseñar una API RESTful
- Buenas prácticas de transferencia de datos y de estado
- Cómo comunicar errores
- Crear una estructura de mensajes intuitiva
- Versionamiento de nuestra API
- Nombrado de los endpoints
- Seguridad

El ejercicio será el siguiente:

> Crear una API que permita crear listas de vocabularios. Un usuario se registra y puede crear tantos vocabularios como desee. Un vocabulario consiste de una lista de palabras ordenadas por tiempo de inserción y su definción, que puede ser tomada del diccionario (fija) o definida por el usuario. Además una palabra puede tener imágenes adjuntas.

Esta aplicación nos permitirá poner en práctica y aprender de todos los puntos antes mencionados y otros. No te pierdas el siguiente artículo.
