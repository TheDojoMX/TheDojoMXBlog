---
title: "A Philosophy of Software Design: Organiza bien los sistemas en capas"
date: 2020-09-01
author: "Héctor Patricio"
tags: ['comments:', 'true']
description: "Resuelve problemas de organización de código mediante un sistema en capas."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1440/v1598938866/96510D0F-CE11-46AB-9B3D-6EA0F8EA4C23_nfdcvu.jpg"
draft: false
---

Hemos escuchado muchísimo acerca de los sistemas en capas como _Modelo-Vista-Controlador_, Modelo-Vista-Template, Modelo-Vista-*, _MV-lo-que-sea_ etc. y eso es porque la mayoría de los sistemas actuales se organiza así: **en capas**. Además, nuestros módulos se dividen naturalmente en capas con diferentes funciones (como código que usa a otro).

Hablemos de por qué es efectiva esta forma de organización (o patrón de arquitectura)
de código, de sus características y cómo podemos aprovecharla para sacar el máximo provecho.

## Características de los sistemas en capas

Sabemos que la mejor forma de organización de un proyecto es **descomponerlo** en partes independientes que **oculten** información de otras.

La comunicación entre las diferentes partes se da por medio de una **interfaz**. Esta interfaz, es la **API** del componente, ya que será usada de manera automática por otra parte del programa.

En un sistema en capas el conjunto de elementos pertenecientes a una capa sólo se puede comunicar con la capa superior y con la capa inferior.

Si un sistema tiene 10 capas, cada componente puede comunicarse máximo con 2 capas.
En los sistemas más comunes, como el de 3 capas (MVC, MVT, MV*), sólamente la capa intermedia (el controlador, por ejemplo) puede comunicarse con dos capas, mientras que las otras sólo se comunican con la intermedia.

[John Ousterhout](https://amzn.to/2GdeHi5) usa la división en capas para explicar cómo se organiza el software con respecto al usuario final: la capa de "hasta arriba" es la que interactúa directamente con el usuario y la de "hasta abajo" es la más alejada del usuario, generalmente el núcleo de tu sistema.

Hablemos ahora de las mejores prácticas según [A Philosphy of Software Design](https://amzn.to/2GdeHi5).

## Diferente capa, diferente abstracción

El concepto que debes tener más claro para descomponer tu software en capas es que cada capa debe tener sus propias abstracciones. Ousterhout da el ejemplo de un sistema de archivos:

1. La capa que interactúa con el mundo exterior o la más alta, tiene la abstracción de un archivo
2. La siguiente capa tiene la abstracción de bloques de memoria y caché
3. La siguiente capa maneja directamente los bloques en el disco

Esta abstracción es efectiva porque cada capa trabaja con abstracciones diferentes y no repiten ninguna entre ellas.

Esta es la idea básica que debes checar en tus diseños, si notas que una abstracción no cambia de una capa a otra, algo está saliendo mal. ¿Cómo puedes identificarlas?

### Funciones de paso

Estos son funciones que no hacen nada mas que mandar llamar una función de la siguiente capa, normalmente para cumplir con la limitante de comunicación entre capas.

Esto indica que no hay una división clara de responsabilidad entre clases o módulos. Para resolver este problema tienes que asegurarte de que la interfaz y la funcionalidad de este punto de tu sistema estén en el mismo módulo.

Evitar este tipo de métodos te evitará complicar la interfaz sin añadir ninguna funcionalidad.

### Variables pasadas

Similar al caso anterior, si tienes una variable que recibes en la llamada de tu módulo y no haces nada con ella mas que pasarla a una capa inferior, estás mezclando las abstracciones entre capas.

A veces son necesarias, pero el manejarlas crea complejidad. Dependiendo del paradigma y el lenguaje de programación deberías buscar una solución adecuada.

Por ejemplo, en lenguajes orientados a objetos podrías guardar todos lo valores a los que necesitas constante acceso desde diferentes lugares un una variable de "contexto" y que generalmente está almacenada en un lugar en el que todas tus funciones puedan acceder. Algunos frameworks usan su variable de `settings` para poner información necesaria ahí.

Los siguientes dos consejos tratan más los diferentes niveles de código que capas del sistema.

### Evita lo más que puedas los decoradores

Ousterhout habla en contra del patrón decorador. Este patrón consiste en envolver clases, objetos o funciones con otros, con el fin de extender la funcionalidad. Los decoradores intentan mantener una interfaz muy similar o exactamente igual al elemento original.

Un ejemplo es la clase de Java `BufferedInputStream` es un decorador de `InputStream`, añadiéndole el buffering.

Los decoradores pueden crear un montón de funciones y variables de pasada y agregar un montón de código de soporte sin de verdad agregar tanta funcionalidad como código.

**APoSD** (el libro) sugiere crear entidades separadas cuando sea posible y evitar el sobreuso de este patrón, a menos que de verdad tenga sentido, por ejemplo: cuando tienes un módulo muy profundo que con un decorador vas a poder reutilizar todo con muy poco código de soporte.

### Abstracciones diferentes entre la interfaz y la implementación

Tu código debería de exponer en su interfaz la abstracción más conveniente para los usuarios de tu módulo, sin importar las abstracciones más convenientes para manejar los datos internamente.

Por este principio, es muy normal que las abstracciones de la interfaz no sean las mismas interfaces que tu implementación usa.

Un ejemplo: imagina que estás escribiendo un componente que te permite editar texto. **¿Cuál es la unidad básica con la que el usuario de tu módulo interactuará?**

Puede ser un carácter, una línea, un párrafo. Ya que tu la visualización del texto es en líneas, lo más conveniente para la implementación es una abstracción que represente una línea de texto.

Pero para el usuario de la clase que maneja texto lo más conveniente es una interfaz que use carácteres porque es más fácil de usar, se quita la responsabilidad de manejar las líneas.

Entonces tu clase queda así: internamente representa el texto como un conjunto de líneas, pero las interfaces lo usan como si fuera un conjunto de caractéres en los que puedes insertar y borrar sin preocuparte por la organización en líneas.

## Conclusión

La separación en capas permitirá que tu código esté mejor organizado y que sea más fácil de entender. Tener cuidado con la forma en que las capas se organizan, cómo se dividen responsabilidades y las interfaces que cada capa expone hará mucho más mantenible y entendible tu base de código.
