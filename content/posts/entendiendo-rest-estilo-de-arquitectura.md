---
title: "Entendiendo REST. El estilo de Arquitectura."
date: 2019-06-15
author: "Héctor Patricio"
tags: ['api', 'rest', 'restful', 'arquitectura']
description: "Empieza a entender qué es REST y por qué ha sido tan importante en la web moderna. Hablemos de la motivación que llevó a crearlo"
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1560431077/frances-gunn-57430-unsplash_gywlwi.jpg"
draft: false
---

En el [artículo anterior de la serie](/2019/05/06/diseno-y-desarrollo-de-una-api-desde-cero.html) hablamos un poco de lo que es una API REST. En este artículo empezaremos a ver qué es REST y por qué surgió.

Antes de empezar con lo nuestro, hablemos de lo que NO es una API REST.

## Esto no es REST

Actualmente, muchos desarrolladores (yo me contaba entre ellos), llaman API REST a cualquier servicio Web que corra sobre HTTP, sirva recursos (objetos o elementos que representan un objeto) o cosas parecidas y use JSON como lenguaje de transferencia de datos.
De estas cosas, sólo la parte de servir recursos (en realidad _representaciones_ de recursos) tiene que ver con una API REST. El estilo arquitectural REST no obliga el uso de HTTP y mucho menos de JSON.

Dada esta tendencia de llamar API REST a cualquier cosa que funcione sobre HTTP, debemos estar de acuerdo en que la mayoría de las API's ni siquiera _intenta_ ser REST.
Algunas son RPC (Remote Procedure Call) sobre HTTP simplemente. Otro mal uso que he escuchado es que cualquier cosa que sirva JSON es llamada API REST, pero como ya dijimos el estilo arquitectural REST ni siquiera fuerza el uso de JSON (y no todas las API's que sirven XML son SOAP).

Con esto no queremos decir que el que un servicio no sea REST lo haga malo o de mala calidad, de hecho, muchas veces (la mayoría) no se necesita cumplir con las características de REST y con cumplir con algunas de las características o principios de diseño de REST es suficiente.

En artículos posteriores vamos a hablar de las seis características que **sí** definen una arquitectura REST, las vamos a cambiar un poco del orden tradicional que se explica en la mayoría de los tutoriales (y seguiremos el de la tesis original) para que tenga más sentido la forma en que las explicamos.

Las características de las que hablaremos son en cierto modo _restricciones_ (constraints, como lo dice la tesis original): una cosa es definida por las cosas que _no_ puede o _no_ debe hacer.

## Arquitectura

Cuando hablamos de REST (REpresentational State Transfer) estamos hablando se un **estilo de arquitectura**.

La definición del estilo de arquitectura REST la hizo [Thomas Fielding](https://www.ics.uci.edu/~fielding/) en su tesis doctoral, que puedes descargar y leer completa [aquí](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm), en ella explica lo que lo llevó a definirla y diseñarla tal como es.

Fielding hace la distinción entre tres conceptos que parecerían lo mismo a simple vista.

- **Estilo de arquitectura o estilo arquitectural**: Es un conjunto de restricciones que limitan cómo los elementos de una arquitectura (componentes del software, conectores y datos) pueden interactuar entre sí y las características que deben tener. En la arquitectura de espacios físicos podemos pensar en los estilos más amplios que a veces escuchamos mencionados: Barroco, Moderno, Post-moderno. En la arquitectura de software, **REST cae en esta categoría**.

- **Diseño arquitectural**: Es la aplicación de un estilo de arquitectura. Podemos pensar en esto como las guías que definen cómo una arquitectura se implementará. El diseño arquitectural en los edificios podría pensarse en la aplicación de las reglas del diseño arquitectural a un tipo de edificio específico tu catedral o castillo 🤔.

- **Arquitectura**: Fielding la define como una abstracción del estado de un sistema en un momento determinado. La arquitectura es la concreción de un diseño arquitectural. En el ejemplo de los edificios puedes pensar en esto como en los planos de la catedral barroca.

Hablando de arquitectura [Simon Brown](https://simonbrown.je/), que es actualmente una da las grandes mentes en el campo de la arquitectura de software, la define como la *todo lo relacionado con el diseño de un sistema de software, desde la estructura del código hasta cómo funciona a alto nivel, pasando por cómo el software es puesto en producción*. Es responsabilidad de la arquitectura definir las siguientes características y funciones del sistema:

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

Como podemos ver, la arquitectura de software tiene muchas cosas de preocuparse. Pues bueno, el estilo de arquitectura ayuda a resolver varias de estas preocupaciones predefiniendo algunas cosas la estructura y el comportamiento del sistema mediante las características y limitaciones que establece.

¿Qué de estas cosas ataca REST? Hablemos de ellas.

## Cosas que REST intenta resolver

Todo este embrollo de arquitectura-diseño-estilos fue definido con un fin en mente: estudiar los estilos y las características de las arquitecturas para poder llegar a la resolución de los problemas concretos que los sistemas tienen.

Las cosas que REST intenta ayudar a resolver concretamente son las siguientes.

### Rendimiento

Una de las principales cosas que este estilo de arquitectura quiere atacar es el rendimiento de las aplicaciones. El rendimiento se refiere tanto a la capacidad real como percibida de cumplir con **lo que se espera de un sistema de software** en términos de velocidad de respuesta.

Esto implica que tanto la aplicación como la red (recordemos que siempre estamos hablando de aplicaciones web) debe responder en un tiempo razonable.

Varias de las restricciones y características que REST establece están relacionadas directamente con este punto.

### Facilidad de Modificación

Fielding elabora esto como uno de los puntos más grandes que las arquitecturas deben atender. A final de cuentas un sistema no se puede quedar estático, y facilitar el trabajo para nosotros mismos en el futuro o para otras personas debería ser una prioridad.

Los cinco puntos que Fielding considera que definen la facilidad de modifición son:

- **Facilidad de evolución**. Es la capacidad que tiene un sistema de que sus componentes cambien sin afectar directamente negativamente a los demás y por lo tanto el estado general del sistema.

- **Extensibilidad**. Es la capacidad de agregar funcionalidades o capacidades a un sistema.
- **Facilidad de personalización**. Es la capacidad de un elemento de poder adaptarse temporalmente para dar un servicio que no siempre da, sin afectar negativamente el sistema en general.

- **Facilidad de configuración**. Se refiere a poder cambiar la configuración o modificar un sistema en producción mediante configuraciones, es decir, sin cambios en el código.

- **Facilidad de reutilización**. Se puede explicar como la capacidad de los componentes de un sistema de ser usados sin modificaciones en otros sistemas.

### Visibilidad

La visibilidad es la capacidad de monitorear un componente del sistema e incluso mediar la interacción entre dos componentes. Este tipo específico de visibilidad (recientemente llamado observabilidad), puede mejorar el sistema de muchas maneras como mediante cachés, capas intermedias para mejorar la escalabilidad, monitoreo activo y la seguridad al observar la comunicación de los componentes y actuar, tal como un firewall lo hace.

### Portabilidad

Uno de los puntos que se necesita resolver de algunas aplicaciones, es que la solución pueda correr en diferentes entornos. A esto se refiere la portabilidad para Fielding, que un sistema pueda correr sin cambios en diferentes instalaciones y sin grandes cambios.

### Escalabilidad

¿Cuántos usuarios al mismo tiempo puede soportar tu aplicación? ¿Qué pasa si de repente llegan diez veces más usuarios de los que esperabas? La respuesta a estas preguntas está directamente relacionada con la escalabilidad de la aplicación.

Fielding la define como la capacidad de los componentes de soportar un número grande de interacciones, que se ve impactada no sólo por la cantidad sino por la frecuencia de interacciones.

### Simplicidad

Un buen desarrollo debe ser tan simple como sea posible. Si se añade complejidad extra a la innata del problema en cuestión será más difícil de mantener.

Estas cuestiones y cosas importantes acerca de todas las aplicaciones son lo que llevó a Fielding a definir REST y a agregar las características/restricciones que puso.

Fielding resume tres características en lo que el llama simplicidad:

- **Complejidad**. Es la cantidad de componentes interconectados. Mientras menos sea, mejor.
- **Facilidad de comprensión**. ¿Qué tan preparado está el sistema para poder ser entendido fácilmente?
- **Verificabilidad**. ¿Se puede verificar que la solución y los datos que entrega el sistema sean correctos?


## Conclusión

Todas estas características y necesidades de un sistema de software de fácil mantenimiento son las que llevaron a la creación de el estilo arquitectural REST. Sirven para entender por qué definió las 6 restricciones que un sistema REST debe cumplir, pero algo interesante que se menciona a través de su tesis es que cada una de las decisiones es un intercambio de valor que hay que sopesar.

**¿Por qué deberías elegir REST?**

>El estilo arquitectural REST te ayuda a resolver problemas que pueden empezar a dar dolores de cabeza desde el principio, al dar una guía de cómo debería comportarse tu aplicación para cumplir con las cualidades mencionadas arriba.

No debemos olvidar que toda selección es **necesariamente** un intercambio de valor. Se pierde algo por ganar otra cosa. La pregunta que siempre hay que tener en mente es:

> ¿Qué me conviene más en este caso?

En el siguiente artículo analizaremos la primera restricción de  REST: la arquitectura cliente-servidor.