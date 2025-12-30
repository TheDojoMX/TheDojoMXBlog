---
title: "Cuando separar el código"
date: 2023-04-07
author: "Héctor Patricio"
tags: ['aposd', 'ousterhout', 'diseño-de-software']
description: "¿Cuándo es buena idea que lo existe en un clase o función lo descompongas en varios elementos? En este artículo veremos algunos criterios para tomar esta decisión."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1680411928/risto-kokkonen-HAIDBanzi8o-unsplash_okktgd.jpg"
draft: false
---

Hay quienes afirman que mientras más pequeñas sean tus clases o funciones, mejor. Hasta llegan a poner un límite de la líneas que pueden ir en un método o función. Esto crea código súper fragmentado que llega a ser complejo por el simple hecho de tener muchos elementos individuales que luego se tienen que unir mediante más código. Además, trazar la causa de algo a través de un código similar es casi imposible o, por lo menos, te puede tomar mucho tiempo.

Es por eso que otros proponentes sobre diseño de software mencionan que mientras más cosas estén detrás de un interfaz y que oculten una implementación, mejor. Esto implica que las funciones y los métodos deben tener un tamaño razonable, sin llegar a ser demasiado grandes. Y este es el punto de este artículo, ¿cómo sabemos cuando es buena idea separar el código en otro módulo? Recuerda que a lo que nos referimos con módulo es cualquier construcción de tu lenguaje que permita encapsular una implementación: clases, funciones, paquetes, etc.

Dominar la división de software en módulos es una pilar del buen diseño de software. Veamos algunos de los criterios que John Ousterhout propone en su libro [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php), precisamente en el capítulo nueve que llama "¿Mejor juntos o separados?" (_"Better together or better apart?"_). Empecemos hablando de cuándo es mejor dejarlo junto.

Lo que tienes que mantener enfrente es que la meta de hacerte es pregunta es disminuir complejidad de tu código en general, pero también de hacerlo más fácil de evolucionar haciéndolo **más modular**.

## Cuando dejarlo junto o combinarlo

**Acceso a la información**. Lo primero que hay que considerar es la información con la que el módulo trata. Si es un slo conjunto de información que en sí mismo es difícil de separar, entonces el código que trata con él **debería permanecer junto**. También te puedes imaginar un protocolo como HTTP, que para simplemente para verificar que el mensaje está bien formado, se requiere de un información para parsearlo. En este caso, el parseo y la verificación del mensaje deberían estar juntos.

**Cercanía semántica**. Si dos partes de código se pueden categorizar fácilmente bajo la misma categoría, muy probablemente ese código puede estar bajo la misma clase, módulo o paquete. El ejemplo que da Ousterhout tiene que ver con cadenas de texto y las funciones que las transforman.

**Dependencia**. Si siempre que quieras entender una parte, de código tienes que mirar a otra, estas dos piezas de código probablemente deben de vivir bajo el mismo módulo. Esto mismo aplica si se usan siempre (o casi siempre) juntas esas dos piezas de código.

**Eliminación de código duplicado**. Esta es una situación a la que hay que prestarle especial atención. Si notas que estás duplicando código en alguna parte, lo más sensato es juntarlo en un alguna clase o función y llamar desde los diferentes lugares en donde lo estás ocupando. Aquí hay que poner un poco de atención: si este código duplicado son unas pocas líneas, puede que no sea conveniente pasar por la molestia de crear un nuevo módulo y las cosas que se requieren para integrarlo en tu código actual. Algo todavía mejor que puedes hacer es refactorizar tu código para que en vez de se llame en diferentes lugares, se reduzca el número de lugares en donde se llama. Esto es posible sobre todo con las excepciones, dependiendo de  tu lenguaje de programación y su estilo de manejo de errores.

Juntar el código a veces traerá un beneficio extra: eliminarás interfaces que no necesitas. Imagínate dos piezas de código que siempre llamas en secuencia, por ejemplo, la función `obtenerHash` y `verificarHash`. Si el 99% de las veces necesitas verificar un hash después de crearlo y al revés, casi siempre que verificas un Hash es porque lo acabas de crear, entonces es mejor que ambas funciones estén juntas, algo como `crearHashVerificado`. Esto es una buena señal de que el código debería estar junto: **si terminas con menos interfaces que al principio, o con interfaces más sencillas**.

## Cuando separar el código

Algunas personas cuentan la líneas de código y creen que esto es un buen indicador de cuando romper una pieza de código en varias. Esto no es conveniente porque aunque es cierto que mientras más grande sea algo, más probable es que sea difícil de entender, no tiene por qué ser así si está bien organizado.

Un buen criterio para separar el código es por su **nivel de abstracción**. No es buena idea tener junto código general y específico para la misma funcionalidad en el mismo módulo, ya que cambios en las funcionalidades específicas podrían afectar a la implementación más general.

**Ejemplo**: imagina que tienes que crear un editor de texto. Un editor de texto tiene funciones generales como insertar texto donde está el cursor, pero también funcionalidades más específicas, como por ejemplo, seleccionar texto con una interfaz gráfica. Aquí decimos que la inserción de texto es general porque todos los editores de texto lo tienen, mientras que la selección de texto es específica porque no todos los editores de texto tienen una interfaz gráfica (piensa que puedes editar texto mediante instrucciones en un API, por ejemplo).

En este caso, dejar en el core solamente las funciones más básicas de edición de texto es buena idea. La selección y borrado de texto pueden ser implementados en otro módulo usando las funciones que el core provee.

Esto lo puedes ver en práctica en los sistemas diseñados en capas, sobre todo en los MVC: el modelo tiene toda la información específica del negocio, la vista todo lo relacionado con la interfaz hacia el exterior y el controlador la conexión entre estas dos partes. Hay componentes extra, como el ORM o el sistema que se encargue de persistir la información. Aunque esto es un buen comienzo, no es suficiente. Tu propio código debe ser organizado de forma que sea fácil de entender siguiendo estos principios.

## Ejemplo: funcionalidad de UNDO (Deshacer) en un editor de texto

John Ousterhout da el ejemplo de la funcionalidad de "deshacer" en editor de texto. Eso que sucede cuando das `CTRL+Z` en casi cualquier programa. ¿En qué consiste? En que cuando se realiza una acción, se guarda para que pueda ser contrarrestada con la acción contraria. Esta función puede ser implementada en el módulo central del editor o fuera de él. ¿Cuál es la mejor opción? Imagina que no sólo tienes que poder deshacer acciones directas en el texto, sino también cosas como selecciones o posicionamiento del cursor.

Una forma de hacerlo sería implementarlo directamente en el módulo o clase encargado de manejar el texto, guardando la lista de acciones que se pueden deshacer y cuando se invoque la acción de deshacer o rehacer, este módulo sería el encargado de ejecutar las acciones de regreso. Este diseño crearía una interacción un poco extraña entre el módulo de interfaz, por ejemplo y el módulo de texto, ya que las acciones de interfaz que se tengan que deshacer, viajarían hacia "arriba".

![arquitectura conjunta de lo descrito](https://res.cloudinary.com/hectorip/image/upload/v1680914313/separacion_gvalss.png){: .align-center}

Un mejor diseño sería separar completamente el módulo de encargado de mantener las acciones que se pueden deshacer, al que podemos llamar Historia. Este módulo sería encargado de guardar y administrar todas las acciones que el usuario tiene disponibles para rehacer o deshacer. Las acciones pueden estar autocontenidas: cada una tiene además información sobre cómo revertirla. ¿Quién pone las acciones en la historia? El módulo que realizó la acción. Por ejemplo, si es una inserción de texto, el encargado sería el módulo core, encargado de manejar el texto. Si es una selección visual, puede ser el módulo de interfaz de usuario. Las acciones son clases con una interfaz común que el módulo de historia puede invocar para deshacer o rehacer.

![Imagen separada](https://res.cloudinary.com/hectorip/image/upload/v1680914316/separacion_2_nnuihs.png){: .align-center}

## Conclusión

Aprender a separar tu código es algo que se logra con la práctica y que sin duda vale la pena hacer, porque un código con una complejidad controlada logra un equilibrio entre módulos demasiado pequeños (que hacen muy poco) y demasiado grandes (que juntan mucha información).

La guía principal para saber cuándo separar o juntar tu código es esta: escoge la estructura que genere menores dependencias, oculte mejor el conocimiento y cree interfaces más simples.
