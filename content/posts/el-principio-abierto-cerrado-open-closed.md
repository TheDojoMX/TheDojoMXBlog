---
title: "El principio Abierto/Cerrado (Open/Closed)"
date: 2022-12-03
author: "Héctor Patricio"
tags: ['solid', 'open/closed', 'abierto/cerrado']
description: "Hablemos del segundo principio mencionado en los principios SOLID: el principio Open/Closed, que habla de cómo tratar de los cambios en el código"
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1048/v1669958588/470909777_supernova_explosion_Highly_detailed__surrealism__trending_on_art_station__triadic_color_scheme__smooth__sharp_focus__matte__elegant__the_most_beautiful_image_ever_seen__illustration__digital_paint__dark__gloomy__octane_render__8k__ilkvuz.png"
draft: false
---

El principio Abierto/Cerrado, originalmente establecido por Bertrand Meyer en 1988 (pero popularizado por [Robert Martin](https://drive.google.com/file/d/0BwhCYaYDn8EgN2M5MTkwM2EtNWFkZC00ZTI3LWFjZTUtNTFhZGZiYmUzODc1/view?resourcekey=0-FsS837CGML599A_o5D-nAw){:target="_blank"}), es para mi uno de los más útiles en el conjunto (tal vez el más útil) de SOLID.

Vamos a analizarlo, ver sus caso de uso y finalmente a establecer sus relaciones con otros principios de diseño de software que te pueden ayudar a crear mejores programas.

## El principio Abierto/Cerrado

Este principio establece que:

> Cualquier módulo de software debería estar abierto para la extensión, pero cerrado para modificación.

Otra vez nos encontramos con palabras vagas que tenemos que examinar, pero por suerte en este principio es más fácil llegar a una conclusión.

En pocas palabras cuando tengas que modificar el comportamiento de un programa, lo último que deberías hacer siempre es modificar el código que ya existe, más bien, debes crear módulos (clases, métodos, funciones, paquetes) que permitan modificar su comportamiento agregando **código nuevo**.

No hay ningún mecanismo casi en ningún lenguaje de programación que te permita "cerrar" o "abrir" módulos, así que estas ideas son puramente conceptuales y guías de comportamiento.

## Aplicaciones y ejemplos

La forma de ejemplo más clásica de aplicarlo es mediante la preparación de tus módulos o clases para usar **polimorfismo**. Por ejemplo, imagínate que estás haciendo una aplicación para procesar pagos y quieres cobrar por diferentes medios. Cada uno de estos medios es un "método de pago". Si implementas cada uno de estos métodos como dependientes de una clase padre, mediante la herencia, clases abstractas, protocolos o interfaces, tu procesador principal podrá, por ejemplo, llamar al método `procesar` de cada clase, sin importar el tipo de método de pago que sea o sus detalles de implementación.

En el ejemplo anterior, cuando quieras implementar un nuevo método de pago, simplemente creas un nuevo módulo que cumpla con las especificaciones de la clase padre y no tendrás que modificar el código existente. Así solo has añadido código nuevo y has eliminado la probabilidad de afectar cosas que ya existían y funcionaban bien.

Como puedes ver, los principios de funcionamiento de estas técnicas tienen que ver con dos cosas:

- Ocultar información (esconder la mayor cantidad de detalles de implementación de tus módulos, detrás de una interfaz)

- Programación por contrato, cumplir con una interfaz dada para que otros módulos puedan usarla con seguridad. De esto hablaremos en otro artículo, pero quiero que veas como es un tema que se va a repetir.

## Aplicaciones más amplias

Este principio también se puede aplicar a niveles diferentes del sistema, por ejemplo a nivel arquitectónico.

Un situación en que puedes usar esta estrategia es cuando tienes un módulo que quieres cambiar pero no quieres deshacer o poner en riesgo el funcionamiento de todo el sistema, ya que puede tener consecuencias catastróficas.

Para aplicarlo, tienes que dejar intacto el módulo de la funcionalidad afectada, mientras lo envuelves con tu nuevo código, usándolo como la interfaz principal cuando te conviene y reemplazándolo poco a poco cuando te sientas seguro.

Como puedes notar, para poder aplicar esta técnica, los módulos deben ser completamente independientes o no podrías de ninguna manera aislar los cambios que estás intentando hacer. Esto casi siempre se logra con paso de mensajes, como por ejemplo una interfaz RPC, ReST o respetando un contrato (interfaz).

## Otros ideas parecidas

Lo primero que quiero que notes es que este principio tiene mucho que ver con la **separación de funciones**, la **ocultación de información** y el respeto a la interfaces.

Espero que para este momento te empieces a dar cuenta de que todo lo que llamamos "principios SOLID" tienen en el fondo: **Ocultar Información**. Esto ha sido ha hablado mucho por [David L. Parnas](https://levelup.gitconnected.com/open-closed-principle-is-nothing-about-the-code-270f1c04bebf){:target="_blank"}, y para mi, es gran parte de lo que se requiere para hacer gran software que pueda ser mantenido y funcional mucho tiempo.

Esta mismo concepto ha sido tratado por otras personas, como Alistair Cockburn con su concepto de ["Variación protegida"](https://martinfowler.com/ieeeSoftware/protectedVariation.pdf){:target="_blank"}.

La idea natural del concepto, puedes entenderla más fácilmente con máquinas reales:

- Una cámara con lentes intercambiables que, cuando requieres una nueva óptica, pones un lente con el mismo conector (interfaz)

- Un carro, que cuando una llanta se poncha se la puedes cambiar, o si requieres para un terreno diferente, puedes ponerle llantas de otro tipo.

El punto es darle a tu sistema puntos "naturales" de extensión, en los que los cambios puedan caber sin hacer grandes cambios en todo el sistema.

## Los límites de la extensión

Es natural que llegue el punto en el que no puedas seguir extendiendo el sistema y tengas que cambiar código que ya está funcionando, nada de lo que estamos diciendo es una ley absoluta o moral que te tengas que sentir mal por no cumplir, recuerda que todo esto es por tu conveniencia, la de tus desarrollos y de tu equipo.
