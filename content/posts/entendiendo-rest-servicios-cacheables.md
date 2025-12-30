---
title: "Entendiendo REST: Servicios cacheables"
date: 2019-10-27
author: "Héctor Patricio"
tags: ['categories:']
categories: ['comments:', 'true']
description: "Los servicios REST deben ser cacheables, aprendamos lo que esto significa y cómo podemos lograrlo."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1570679826/laura-ockel-nIEHqGSymRU-unsplash_gsspla.jpg"
draft: false
---

La tercera característica que [Thomas R. Fielding](https://twitter.com/fielding) (Roy Fielding a partir de ahora) establece para los sistemas **REST** es la capacidad de que su información sea cacheable. Veamos lo que esto significa y por qué es una característica importante. Empecemos por definir el caché.

## ¿Qué es _el caché_?

Originalmente el caché se refiere a un tipo especial de memoria _muy rápida_ en los procesadores, que guarda _temporalmente_ información que tiene gran probabilidad de volver a ser utilizada _dentro de poco tiempo_ (en los procesadores hablamos de nano-segundos).

Al evitar que el procesador vuelva a consultar la RAM (muy lenta en [comparación con la memoria caché](https://gist.github.com/jboner/2841832)), las operaciones se realizan a mucha mayor velocidad.

![Latencia de diferentes tipos de memoria](https://i.imgur.com/k0t1e.png)

La memoria caché de los procesadores tiene una gran desventaja: **es muy muy pequeña**. Esto presenta retos:

- ¿Qué guardo aquí para maximizar la eficacia de este espacio de almacenamiento?
- ¿Cómo decido cuándo borrar o sobre-escribir la información que tengo aquí?
- ¿Qué pasa si la información original cambia mientras estoy ocupando los datos guardados en la memoria caché?

Hablaremos más adelante de estas preguntas en nuestro propio contexto, pero hay técnicas para poder contestarlas con cierta eficacia, que los [procesadores han logrado implementar](http://user.it.uu.se/~yi/pdf-files/2014/euc14.pdf).

Así que puedes pensar en el caché como en una memoria que es más rápida (aunque más limitada). Se utiliza con el objetivo de hacer un sistema más rápido y a veces más eficiente.

## Caché en los sistemas REST

Esta característica se basa en las dos que ya hablamos: [servicios sin estado](/2019/08/03/entendiendo-rest-servidor-sin-estado.html) y [arquitectura cliente-servidor](/2019/07/04/entendiendo-rest-arquitectura-cliente-servidor.html).

Lo que se define como "cacheabilidad" en los sistemas REST es la capacidad
de estos sistemas para _etiquetar_ de alguna forma las respuestas para que
otros mecanismos intermedios funcionen como un caché.

Así el sistema puede atender más peticiones, en menos tiempo, con menos
recursos (comparado con un sistema sin caché).

Estos sistemas o mecanismos intermedios (existen entre el cliente y el servidor) deben ser por lo general transparentes para los desarrolladores,
no deben afectar la manera en que los servicios se consumen.

En sistemas web que usan **HTTP** para comunicarse el sistema de "etiquetado" que permite que una respuesta sea cacheada son **las cabeceras**. Estas permiten a los diferentes actores en el proceso de comunicación (servidor local, proxy, proxy reverso, navegador o cliente final, entre otros), saber quién debería cachear la información y por cuánto tiempo o cómo decidir si deben renovar la información. Las cabeceras HTTP comúnmente usadas para esto son:

- `Expires`: especifica hasta cuándo se puede considerar fresca o válida la información.
- `Cache-control`: Es usado para especificar directivas de caché que deben ser respetadas por todos lo puntos por los que pasa la información. Puedes ver los posibles valores y su especifacación aquí: [Cache-Control Header](https://tools.ietf.org/html/rfc2616#section-14.9)
- `Vary`: es usada para indicar qué otras cabeceras se deben tomar en cuenta para decidir si el servidor puede reutilizar una respuesta o no.
- `Etag`: identifica a una respueste de manera única, puede usarse para pedir una respuesta nueva de un mismo endpoint, y en combinación con la cabecera `If-None-Match`

Existen otras cabeceras usadas para lograr un control correcto del caché como `If-Modified-Since`.

## Ventajas del caché

El caché se establece como una de las características de REST porque proporciona ventajas para el uso y la escalabilidad de los sistemas. Veamos algunas de ellas.

### Aumenta la percepción de velocidad

Al guardar las respuestas que es más probable que vuelvan a salir, un sistema REST puede contestar una gran cantidad de sus peticiones a la velocidad que el caché lo permita, es decir, muy rápido.

### Consumo de recursos reducido

El uso caché se parece mucho a una técnica de programación llamada **dynamic programming** que consiste en guardar temporalmente los resultados de operaciones costosas en tiempo. Esto permite que
nos ahorremos el procesamiento de muchas respuestas que no se necesitan
de nuevo porque están almacendas. Además se reduce el ancho de banda
consumido porque muchas peticiones ni siquiera tienen que llegar al servidor.

### Sistemas más fáciles de escalar

Los sistemas que usan caché son capaces de aguantar más peticiones
simultáneas por la razón que vimos anteriormente: se reduce el consumo de recursos. Además, si se require crecer el sistema se deben poner menos recursos. Para algunos sistemas, el caché es lo único que tiene que crecer
cuando se requiere atender a más usuarios simultáneos.

## Retos de cachear

Toda solución tecnológica implica ventajas y desventajas. Entonces ¿qué desventajas o retos implica usar un sistema de caché?

### Frescura

> Sólo hay dos cosas difíciles en Ciencias de Computación: invalidación de caché y nombrar cosas. - Phil Karlton

El reto más grande e importante de tener un sistema de caché es lograr un
equilibrio entre mantener la información el mayor tiempo posible y tener
información correcta y actualizada. Si se almacena en caché por demasiado
tiempo algo, esta información se vuelve vieja y por lo tanto puede estar desactualizada. Por el otro lado si se guarda por muy poco tiempo puede
llevar a que los sistemas de caché se sub-utilicen y provean pocos
beneficios.

### Diseño del sistema

Designar qué partes del sistema pueden ser cacheables y asignar los
etiquetados de las respuestas correctamente puede aumentar la complejidad del sistema en general.

### Inconsistencia

El uso de caché puede llevar a inconsistencias de información entre diferentes clientes por periodos de tiempo de diferente duración. Esto es en parte consecuencia de la dificultad de mantener el caché fresco, pero además tiene que ver con la manera en que los clientes piden la información. **Si tus clientes no pueden soportar la mínima variación en la información porque tendría consecuencias graves, es mejor no cachear.**

## Conclusión

El caché es una parte olvidada de los sistemas REST, el constraint menos mencionado. Pero es importante que les permite funcionar mejor cuando tenemos bastante carga. Mantenerlo funcionando bien es un reto, pero los sistemas que quieren ser escalables y resistentes deben implementar alguna forma de cachear.

Roy Fielding menciona que es importante porque cualquier
sistema expuesto a clientes desconocidos tiene el peligro de recibir una
gran cantidad de carga súbitamente, y si tu servicio no está preparado o es
fácil de escalar, fallarás.

Si quieres leer un artículo más completo con otras referencias sobre el caché en REST y en HTTP te recomiendo [REST better: HTTP Cache](https://odino.org/rest-better-http-cache/), en inglés.

En el siguiente artículo veremos la cuarta restricción de los sistemas REST: la interfaz uniforme, la más amplia de las restricciones, pero una de las más útiles.
