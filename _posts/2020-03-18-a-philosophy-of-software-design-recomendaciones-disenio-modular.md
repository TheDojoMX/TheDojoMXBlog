---
title: "A Philosophy of Software Design: Recomendaciones de diseño modular"
date: 2020-03-18
author: Héctor Patricio
tags: APoSD software-design complexity interfaces defaults
comments: true
excerpt: "Hablemos de algunos consejos para lograr ocultar la mayor cantidad de información posible en tus módulos, pero también de cómo no llevarlo demasiado lejos"
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1584519537/2E4D3407-0447-4034-BEFA-188831BF5971_x4th6g.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_200/v1584519537/2E4D3407-0447-4034-BEFA-188831BF5971_x4th6g.jpg
  overlay_filter: rgba(0, 0, 0, 0.6)
---

En los artículos anteriores hemos estado hablando de cómo evitar la complejidad mediante ocultar información.

En este daremos algunas recomendaciones más y hablaremos de cómo no llevar este principio al extremo.

Hablemos primero de consejos que te ayudarán a mantener oculta la información que debe de estarlo.

## Exponer lo menos posible estructuras de datos

Un error común cuando creamos un módulo es exponer las estructuras de datos internas hacia otros módulos. Esto hace el código que usa tu módulo sea _dependiente de detalles de implementación_ que no le conciernen y, como hemos repetido hasta el cansancio, que una decisión de diseño se vea reflejada en varios lugares.

Transforma las estructuras de datos internas en estructuras de uso general que no dependan de la implementación de tu módulo. Por ejemplo, si estás haciendo una conexión con una API de la que extraes información para otros lados del sistema, comunica esa información en una estructura de datos diseñada para tu sistema no dependiente de la API.

**Ejemplo**. Imagina un módulo de comunicación con diferentes API's de mensajería como WhatsApp, Messenger, etc. Cada una las API's avisa de la entrada de un nuevo mensaje con sus datos específicos y en su formato. Para que to módulo encapsule la mayo cantidad de decisiones de diseño posible debería crear una estructura de mensajes que los demás módulos _recibieran independientemente del medio por el que llegó el mensaje_. Lo mismo para responder: la función encargada de la respuesta debería recibir _siempre los mismos datos independientemente del mensajero que se esté usando_.

## Defaults útiles

Tal vez este punto merezca su propio artículo pero tratemos de resumirlo.

La idea de crear un módulo es, a parte de ocultar complejidad, crear un pieza de código que pueda ser _reutilizable_. Como la operación no es siempre exactamente igual, a veces hay que incluir parámetros que permitan modificar el comportamiento del módulo. Los parámetros pueden llegar a revelar detalles de implementación, así que es conveniente saber diseñarlos, primero _para no contaminar la interfaz_ y segundo _para mantener la interfaz fácil de usar_.

John Ousterhout habla como ejemplo de lo mal diseñada que está la interfaz de la clase `FileInputStream` de Java, que no es capaz de realizar una lectura con buffer sin que le pases una clase que lo hace explícitamente. La lectura de un archivo con un buffer **es normal**, generalmente no quieres leer un archivo sin tener el buffer disponible. Entonces el default de esta clase debería ser la lectura con buffer, _sin que se lo tengas que pedir explícitamente_.

**Los módulos deberían hacer lo normal o lo correcto siempre que sea posible, sin que se tenga que pedir explícitamente.** Es decir, tus módulos deberían estar diseñados para hacer el _caso más común_ muy fácil de usar.

> Las mejores funciones son las que obtienes sin siquiera saber que existen. - **John Ousterhout**

Un ejemplo de buen diseño son los lenguajes modernos con la codificación de las cadenas: son `utf-8` por default, ya que es 'lo correcto' y lo común.

Otro ejemplo son las funciones `split` (separar una cadena) y `join` (juntar los elementos de un array o lista en una cadena) de Python, Elixir y otros lenguajes: si no le pasas el carácter que usarán para dividir o pegar, lo harán por la cadena vacía, _facilitando un caso de uso muy común_.

Podemos aprender de estos buenos diseños para crear los propios. Por ejemplo, imagina que tienes un módulo que usa la fecha y hora para registrar algo. El caso _común_ es que registres algo en el momento inmediato que sucedió. Un buen default sería que el módulo _automáticamente_ registrara la hora actual sin esperarla del usuario, pero dando la opción de modificarla en caso de que se necesite. Un programa que hace esto es **Git**, registra automáticamente un commit con la hora en que lo hiciste pero tiene la opción de que la especifiques o modifiques.

## Aisla dentro de las clases y paquetes

Cuando trabajas con clases, es buena idea crear métodos independientes (privados en caso de ser posible), que oculten información _del resto de la clase_. Piensa en esto como en aplicar los principios anteriores a nivel de clase. Además las variables de clase o de instancia deberían ser usadas en el **menor número de lugares posible**.

Si estás usando un lenguaje funcional o procedural, _aplica este principio al nivel de tus paquetes_ (y definitivamente evita variables globales lo más que puedas).

Finalmente hablemos de cómo llevar todo esto demasiado lejos.

## La clase dios

En artículos pasados hablamos un poco de que es mejor crear clases grandes que encapsulen decisiones de diseño completas en vez de dividir esas decisiones de diseño. Pero si no tenemos cuidado, esto nos puede llevar a crear lo que algunos conoce como _'the God Class'_ o la clase dios.

Esta infame clase es la que en muchos sistemas se ha creado para mantener la mayoría de la información y operación, es decir, es una clase que lo _sabe_ y lo _puede_ todo. Crearla romería el propósito de ocultar información: **pasarías la mayor parte del tiempo trabajando en esta clase**, que por lo general sería muy complicada, teniendo tantas cosas que hacer. Así que _evítala a toda costa_.

## Ocultar información que sí se usa afuera

Sería un error grave de diseño hacer inaccesible (en lenguajes que lo permiten), o difícil de encontrar, información que se usa afuera de tu módulo. Un ejemplo que da [A Philosophy of Software Design](https://amzn.to/2GdeHi5) es en el caso de parámetros de configuración que afecten el rendimiento de una pieza de software y que sea absolutamente necesario conocer para operar bien (podría ser el método de conexión en una red, por ejemplo).

En el ejemplo de las API's de mensajería del que hablamos arriba, piensa por ejemplo que la parte del código encargada de generar un mensaje _necesita_ saber de dónde viene el mensaje para generar un mensaje adecuado al medio (si viene de SMS hará un mensaje mejor de 100 carácteres, por ejemplo).

O algo a lo que la mayoría de los lenguajes de programación nos obligan: especificar el modo de apertura de u archivo.

Sin embargo, tu trabajo como diseñador de software consiste en **minimizar** la información que se necesita fuera del módulo, para que sea lo más fácil de usar dentro de los límites.

## Conclusión

Este y los artículos anteriores quieren dejar claro algo: el trabajo principal de un módulo es ocultar información. Hay varias formas de lograrlo y detalles a los cuáles ponerles atención. Hacerlo creará código que sea más fácil de **entender y mantener**.

En el próximo artículo hablaremos de por qué es mejor crear módulos de propósito general.
