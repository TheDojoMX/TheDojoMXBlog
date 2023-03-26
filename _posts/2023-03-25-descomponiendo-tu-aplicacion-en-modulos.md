---
title: "Descomponiendo tu aplicación en módulos"
date: 2023-03-25
author: Héctor Patricio
tags: módulos diseño arquitectura
comments: true
excerpt: "La tarea principal de un desarrollador de software es crear software que funcione, pero además que sea mantenible y entendible. Dividir en módulos es una técnica que te puede ayudar. Hablemos de algunas formas de hacerlo."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1679205046/javier-miranda-3yQY9GPM8Mg-unsplash_nkacdz.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1679205046/javier-miranda-3yQY9GPM8Mg-unsplash_nkacdz.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Hay un dicho que tiene que ver con la guerra que es un gran consejo para crear gran software:

> Divide y vencerás

Dividir un problema para resolverlo por partes tiene muchas ventajas, en este artículo vamos a hablar de ellas, así como de las técnicas y los criterios que puedes seguir para hacerlo efectivamente. Específicamente, en este artículo vamos a hablar de cómo dividir la aplicación en módulos. Pero antes definamos lo que es un módulo.

## ¿Qué es un módulo?

En este artículo los módulos son cualquier cosa que encapsule una implementación detrás de una API o interfaz. Los módulos tienen diferentes nombres dependiendo del lenguaje de programación, pueden ser:

- Paquetes en Python
- Módulos en JavaScript
- Clases y paquetes en Java
- Bibliotecas en C
- Aplicaciones en Erlang o Elixir
- Un microservicio en una arquitectura de distribuida
- Otro sistema

Esta lista no es para nada exhaustiva, pero comunica la idea de lo que es un módulo conceptualmente, repitiendo: cualquier artefacto que encapsule una implementación o funcionalidad detrás de una API, es decir que tenga una _asignación de responsabilidad_ (según David L. Parnas).

### Ventajas de dividir tu aplicación en módulos

¿Qué es más sencillo? ¿Subir 100 escalones de 15cm o dar un salto de 15m? Humanamente ni siquiera es posible dar un salto de 15m, por lo que tenemos que recurrir a usar las escaleras.

Lo mismo sucede intelectualmente, la mayoría de los problemas que resolvemos en programación son más grandes de lo que puede caber en nuestra mente en un tiempo determinado. Es por esto que tenemos que descomponer los problemas en partes más pequeñas.

La modularización te permite cambiar el sistema de forma más sencilla, mientras respetes la interfaz entre los módulos (su _API_), puedes cambiar el módulo que resuelve cierta parte del problema sin afectar el sistema entero. A esto a veces le llaman **programación por contrato**.

Crear módulos lo más independientes posible te permite reutilizarlos en otros sistemas, lo que llamamos reutilización de código. Si sigues los lineamientos de tu lenguajes de programación, probablemente puedas crear el artefacto para distribuirlo y que incluso otras personas lo usen.

Finalmente, dependiendo de lo independiente que sean los módulos, puedes asignarle la tarea de la implementación a otras personas.

### Desventajas

Al igual que si pudiéramos mágicamente dar un salto de 15m nos evitaría construir unas escaleras, con todo lo que ello implica, el uso de módulos en tu aplicación agregar algo más de complejidad.

En primera, se requiere una infraestructura para que los módulos puedan comunicarse entre sí. Si los módulos son construcciones naturales de tus sistema de programación, entonces sólo tienes que preocuparte por usarlos bien y crear interfaces convenientes.

Pero si estás haciendo sistemas independientes, microservicios, etc. entonces también tienes que preocuparte por el transporte de información, la seguridad, etc. Este tipo de modularidad convierte tu aplicación en un sistema distribuido, lo que agrega gran complejidad.

Además, dividir en módulos introduce el riesgo de crear complejidad adicional debida a las dependencias entre los módulos.

Pero normalmente, las ventajas de modularizar te habilitan para lograr cosas que no es posible hacer de otra forma, así que ahora surge la pregunta, ¿por dónde empiezo?

## Criterios para dividir tu aplicación en módulos

Esto en realidad es una exploración de las diferentes formas en las que tu aplicación podría estar dividida y las abstracciones que creas. ¿Los divido por grupos de funcionalidades? ¿Por el tipo de información a los que tienen acceso? ¿Por el lugar en el que van a estar implementados? ¿Por el nivel de abstracción?

David Parnas explica en ["On the Criteria to be Used in Decomposing Systems into Modules"](https://www.win.tue.nl/~wstomv/edu/2ip30/references/criteria_for_modularization.pdf) dos diferentes formas o criterios de dividir un sistema en módulos:

1. La que él piensa que era la más común cuando se escribió el artículo, es la de dividir el programa en sus pasos lógicos. Después de hacer un diagrama de flujo del proceso que quieres automatizar o representar, los pasos del diagrama se convierten en módulos.

2. La segunda forma es la de dividir o "cortar" el programa en módulos por _especialidad_, es decir, por las cosas que saben hacer y que ocultan de los demás módulos. Estos módulos encapsulan **decisiones de diseño**.

## Ejemplo práctico: una pasarela de pago

La función de una pasarela de pago es procesar las transacciones de pago de los usuarios. Debe registrar datos como quién hace el pago, a quién se lo hace, el monto, la fecha y hora, el método de pago y el estado de la transacción.

Hagamos el ejercicio de descomponer el sistema en módulos. Primero usemos el primer criterio. Pensando en el flujo de operaciones que se tienen que hacer podemos pensar en los siguientes pasos:

1. Recibir los datos de la transacción a ejecutar.
2. Recibir los datos de pago del usuario.
3. Validar los datos de la transacción.
4. Intentar ejecutar la transacción.
5. Registrar el estado de la transacción.
6. Notificar a los involucrados del resultado de la operación.

Vamos a delimitar las funciones para hacerlo más sencillo: pongamos que sólo se puede pagar con tarjeta de crédito y que se notificará al usuario por correo electrónico.

Los módulos que podríamos crear usando este flujo son:

1. **Módulo de recepción de datos**. Este sistema recibe los datos de la transacción a ejecutar y los pone en una base de datos. También se encarga de validarlos.

2. **Módulo de recepción de datos del usuario**. Recibe los datos de pago del usuario y actualiza el registro de la transacción.

3. **Módulo de ejecución de la transacción**. Lee los datos de la transacción de la base de datos e intenta ejecutar la transacción, actualizando el registro con el resultado de la operación.

4. **Módulo de notificación**. Es capaz de leer el registro de la base de datos para extraer los datos de la transacción y enviar un correo electrónico al usuario.

5. **Módulo central**. Se encarga de coordinar el funcionamiento de los demás módulos, los llama en el orden correcto y maneja los errores.

Este diseño sin duda funcionaría, pero tiene algunas desventajas. ¿Qué pasaría si se aumentara la información que se tiene que registrar de la transacción? A todos los módulos les afectaría, ya que todos leen de un repositorio central que es la base de datos. ¿Y si en vez de recibir los datos por separado, se quisiera leer todos los datos de un archivo para ejecutar pagos en masa? Por lo menos dos módulos saldrían afectados, el de recepción de información de la transacción y de información del usuario.

Para dividir el trabajo en varios equipos, antes tendría que establecerse la forma en la que se van a guardar los datos en la base de datos y cualquier cambio les afectaría a todos.

### Dividiendo por especialidad

En vez de dividirlo por el flujo de operaciones, como si fuera una cadena de producción usemos el criterio de la especialidad, o de **ocultar información**. ¿Cuáles son las decisiones de diseño que quisiéramos ocultar detrás de una interfaz?

Usando este criterio podemos tener los siguientes módulos:

1. **Módulo de recepción de información**. Recibe todos los datos, tanto de la transacción como se pago y los valida. Envía estos datos al almacenamiento indicado mediante una interfaz. ¿Qué decisiones de diseño oculta? La forma en la que se reciben y validan los datos

2. **Módulo de registro de transacciones**. Recibe la información de las transacciones, las almacena y es capaz de devolver la transacción solicitada. También puede actualizar los datos de una transacción y borrarla. ¿Qué decisiones de diseño oculta? La forma en la que se _persiste_ la información. Ninguno de los otros módulos necesita saber cómo se almacenan los datos.

3. **Módulo de procesamiento de transacciones.**. Este módulo recibe los datos absolutamente necesarios para procesar una transacción con la institución bancaria, la ejecuta y devuelve un estado de la transacción. Tiene funciones para ejecutar, re-intentar y revertir transacciones. ¿Qué decisiones de diseño oculta? La comunicación con la institución bancaria, la forma en la que se reciben los datos de estas y el procesamiento de errores en la transacción.

4. **Módulo de notificaciones**. Es capaz de mandar notificaciones por correo electrónico, recibiendo los datos de los destinatarios y el mensaje que se tiene que mandar. ¿Qué decisiones de diseño oculta? La forma de comunicación con los medios de transporte de notificaciones, en este caso, el correo electrónico.

5. **Módulo de coordinación o central**. Es el encargado de usar los módulos anteriores para procesar el pago.

La principal diferencia de este diseño con el anterior, es la forma en la que los módulos se comunican y la información que cada módulo debe de tener. Cualquier cambio en la implementación de sus funciones no afectará a los demás módulos, sobre todo cambios en la persistencia de la información, que era un punto crítico en el diseño anterior.

¿Que pasa si quisiéramos cambiar la forma en la que se reciban los datos, por ejemplo, con el archivo para procesar los pagos en masa? El módulo de recepción de información se vería afectado o reemplazado, pero los demás módulos no.

Si queremos dividir el trabajo en equipos, cada equipo puede trabajar en un módulo siempre y cuando se establezca la interfaz de su módulo, y las dependencias entre ellos se reducen.

## Resumen

No existe una forma absolutamente correcta de dividir tu sistema, casi siempre es subjetiva y todas presentan ventajas y desventajas. Pero una decisión con la que no te puedes equivocar es la de aislar los detalles de implementación y las decisiones de diseño en módulos autocontenidos.

Piensa en un módulo como en una caja que _sabe hacer algo_ y que puedes usar en varios lugares de tus sistema, no como en un paso de un proceso, que normalmente lo casa con esa posición y lo hace poco reutilizable, además de que puede hacer que no esté tan autocontenido como debería, dejando escapar información que crea dependencias entre módulos.

## Recursos para aprender más

El artículo en el que está basado este artículo es ["On the Criteria to be Used in Decomposing Systems into Modules"](https://www.win.tue.nl/~wstomv/edu/2ip30/references/criteria_for_modularization.pdf) de David L. Parnas.

Otro recurso del que tal vez ya estés harto de escuchar si lees este blog es [A Philosophy of Software Design](https://www.amazon.com/Philosophy-Software-Design-John-Ousterhout/dp/1732102201). Aquí se explican varios principios para poder descomponer tu aplicación en módulos de forma efectiva, tomando como principal referencia este artículo de Parnas, y expandiéndolo con la experiencia de Ousterhout.

## Conclusión

Descomponer tus aplicaciones en módulos es algo esencial en el desarrollo de software. Pensarlo un poco antes de hacerlo nos dará una gran ventaja para crear software de mejor calidad, que sea más fácil de mantener y que podamos evolucionar mejor.

Esta descomposición no siempre te va a salir bien a la primera, por lo que hay que tener la capacidad de evaluar la efectividad de tu diseño y la humildad para reconocer o aceptar los puntos débiles y cambiarlos. Es cierto que ciertas plataformas te pueden ayudar a descomponer mejor tu aplicación que otras, por lo que también es un gran punto a considerar cuando estés eligiendo la tecnología para tu próximo proyecto.

Sigue cultivando esta habilidad, porque es de lo más importante que un desarrollador de software puede saber, pensando también que a futuro tal vez seamos en gran parte diseñadores mientras la implementación estará a cargo de máquinas (te estoy viendo, [Codex](https://openai.com/blog/openai-codex)).
