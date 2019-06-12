---
title: "Entendiendo REST a fondo."
date: 2019-05-17
author: Héctor Patricio
tags: api rest restful arquitectura
comments: true
excerpt: "Empieza a entender qué es REST y por qué ha sido tan importante en la web moderna. Hablemos de la motivación."
header:
  overlay_image: #image
---

En el [artículo anterior de la serie](/2019/05/06/diseno-y-desarrollo-de-una-api-desde-cero.html) hablamos un poco de lo que es una API REST. En este artículo empezaremos a ver qué es REST y por qué surgió.

Antes de empezar con lo nuestro, hablemos que lo que NO es una API REST.

## Esto no es REST

Actualmente, muchos desarrolladores (yo me contaba entre ellos), llaman API REST a cualquier servicio Web que corra sobre HTTP, sirva recursos (objetos o elementos que representan un objeto) o cosas parecidas y use JSON como medio de comunicación.
De estas cosas, sólo la parte de servir recursos (en realidad _representaciones_ de recursos) tiene que ver con una API REST. El estilo arquitectural REST no obliga el uso de HTTP y mucho menos de JSON.

Dada esta tendencia de llamar API REST a cualquier cosa que funcione sobre HTTP, debemos estar de acuerdo en que la mayoría de las API's ni siquiera _intenta_ ser REST.
Algunas son RPC (Remote Procedure Call) sobre HTTP simplemente. Otro mal uso que he escuchado es que cualquier cosa que sirva JSON es llamada API REST, pero como ya dijimos el estilo arquitectural REST ni siquiera fuerza el uso de JSON (y no todas las API's que sirven XML son SOAP).

Con esto no queremos decir que el que un servicio no sea REST lo haga malo o de mala calidad, de hecho, muchas veces (la mayoría) no se necesita cumplir con las características de REST y con cumplir con algunas de las características o principios de diseño de REST es suficiente.

En artículos posteriores vamos a hablar de las seis características que **sí** definen una arquitectura REST, las vamos a cambiar un poco del orden tradicional que se explica en la mayoría de los tutoriales (y seguiremos el de la tesis original) para que tenga más sentido la forma en que las explicamos.

Las características de las que hablaremos son en cierto modo _restricciones_ (constraints, como lo dice la tesis original): una cosa es definida por las cosas que _no_ puede o _no_ debe hacer.

## Arquitectura

La definición de la arquitectura REST la hizo [Thomas Fielding](https://www.ics.uci.edu/~fielding/) en su tesis doctoral, que puedes descargar y leer completa [aquí](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm), en ella explica lo que lo llevó a definirla y diseñarla tal como es.

Cuando hablamos de REST (REpresentational State Transfer) estamos hablando se un **estilo de arquitectura**.

¿Qué es la arquitectura de un sistema de software?

[Simon Brown](https://simonbrown.je/), que es actualmente una da las grandes mentes en el campo de la arquitectura de software, la define como la *todo lo relacionado con el diseño de un sistema de software, desde la estructura del código hasta cómo funciona a alto nivel, pasando por cómo el software es puesto en producción*. Es responsabilidad de la arquitectura definir las siguientes características y funciones del sistema:

- Tareas que abarquen todo el sistema: Logging, manejo de errores, etc.
- Seguridad
- Rendimiento
- Escalabilidad
- Disponibilidad
- Auditorías y cumplimiento de regulaciones
- Limitaciones del entorno
- Interoperatividad e integración con otros sistemas
- Consistencia de soluciones a través de toda la base de código
- Evaluación de cumplimiento de los entregables

Como podemos ver, la arquitectura de software tiene muchas cosas de preocuparse. Pues bueno, el estilo de arquitectura ayuda a resolver varias de estas preocupaciones predefiniendo la estructura y el comportamiento del sistema mediante las características y limitaciones que establece.

¿Qué de estas cosas ataca REST? Hablemos de ellas.