---
title: "Descomponiendo tu aplicación en módulos"
date: 2023-03-18
author: Héctor Patricio
tags: módulos diseño arquitectura
comments: true
excerpt: "La tarea principal de un desarrollador de software es "
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

David Parnas explica en ["On the Criteria to be Used in Decomposing Systems into Modules"](https://www.win.tue.nl/~wstomv/edu/2ip30/references/criteria_for_modularization.pdf) diferentes formas o criterios de dividir un sistema en módulos.

La primera y que el piensa que era la más común cuando se escribió el artículo, es la de dividir el programa en sus pasos lógicos. Imagínate que el trabajo de tu programa es transformar un texto en imágenes, crear una publicación personalizada del texto y las imágenes y enviarlo a diferentes destinatarios.

El proceso puede tener las siguientes etapas:

1. Obtener el texto
2. Generar las imágenes
3. Crear la publicación, basado en la plantilla para cada destinatario
4. Enviar la publicación a los destinatarios

Usando el primer y más tradicional criterio, entonces, lo que haríamos sería crear un módulo para cada una de las etapas.

Usando el segundo criterio, los módulos no corresponterían tal vez directamente con los pasos de la transformación...

## Recursos para aprender más

El artículo en el que está basado este artículo es ["On the Criteria to be Used in Decomposing Systems into Modules"](https://www.win.tue.nl/~wstomv/edu/2ip30/references/criteria_for_modularization.pdf).

Otro recurso del que tal vez ya estés harto de escuchar si lees este blog es [A Philosophy of Software Design](https://www.amazon.com/Philosophy-Software-Design-John-Ousterhout/dp/1732102201). Aquí se explican varios principios para poder descomponer tu aplicación en módulos de forma efectiva, tomando como principal referencia este artículo de Parnas, y expandiéndolo con la experiencia de Ousterhout.

## Conclusión

Descomponer tus aplicaciones en módulos es algo esencial en el desarrollo de software. Pensarlo un poco antes de hacerlo nos dará una gran ventaja para crear software de mejor calidad, que sea más fácil de mantener y que podamos evolucionar mejor.

Esta descomposición no siempre te va a salir bien a la primera, por lo que hay que tener la capacidad de evaluar la efectividad de tu diseño y la humildad para reconocer o aceptar los puntos débiles y cambiarlos. Es cierto que ciertas plataformas lo hacen mejor que otras, por lo que también es un gran punto a considerar cuando estés eligiendo la tecnología para tu próximo proyecto.

Sigue cultivando esta habilidad, porque es de lo más importante que un desarrollador de software puede saber, pensando también que a futuro tal vez seamos en gran parte diseñadores mientras la implementación estará a cargo de máquinas (te estoy viendo, [Codex](https://openai.com/blog/openai-codex)).
