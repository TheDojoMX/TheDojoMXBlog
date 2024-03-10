---
title: "¿Qué producimos los desarrolladores de software?"
date: 2024-03-09
author: Héctor Patricio
tags: software ingenieria-de-software arquitectura
comments: true
excerpt: "Tu proceso de desarrollo de software produce muchas más cosas que sólamente software corriendo. En este artículo hablaremos de otros resultados de trabajo"
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1702186060/hunter-reilly-O7NHbnjrz94-unsplash_dntxcb.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1702186060/hunter-reilly-O7NHbnjrz94-unsplash_dntxcb.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Para algunos, la respuesta a la pregunta del título es simplemente "_software_", porque parece tan obvia que el mismo nombre lo dice. Y aunque el **software** tiene una definición concreta, en este artículo vamos a desmunazar los productos de un proceso de desarrollo de software. Lo que quiero que veas es que el desarrollo de software no sólamente es crear programas que fucncionen, ya que para que el software sea efectivo tiene que **evolucionar**, y aquí entra el punto importante. 


## ¿Qué es un sistema de software?
Un sistema de software incluye varias cosas, algunas obvias, otras no tanto. Vamos a analizar de la más a la menos visible.

### El software corriendo.

Esta es la parte más visible y en la que muchos se quedarían. El software en 
ejecución significa una computadora ejecutando instrucciones que cumplan con 
el propósito del software. Si pudiéramos hacer que la computadora ejecutara lo 
que necesitamos de mnanera mágica, sin tener que darle instrucciones a sus 
diferentes partes, esta parte seguiría existiendo.

Ejemplos del software en ejecución son:

- Una página web mostrando la infomación que un cliente necesita
- Word recibiendo las instrucciones de tu teclado y mostrando lo que escribes en la pantalla
- _grep_ buscando la expresión regular que quieres encontrar en un conjunto de documentos

A veces, dependiendo del proceso pactado, no entregamos el software corriendo, sino entregamos
_artefactos_ que tienen que ser ejecutados para poner el software corriendo.

### Ejecutables
Los ejecutables son los _artefactos_ que hacen que sea posible realizar las tareas que 
pensamos para nuestro software. Estos artefactos pueden tomar muchas formas,
por ejemplo, pueden ser archivos compilados .exe, empaquetados .dmg (de MacOS),
o incluso compilados que contienen instrucciones para una arquitectura de procesador
específica.

En el caso de lenguajes y plataformas interpretadas, los ejecutables son a veces
directamente el código fuente que además requiere que el usuario final tenga
cierto entorno preparado en su computadora para poder correr.

### Código fuente
El código fuente, para mi, es la parte medular de los resultados de un proceso de desarrollo
de software. Tiene la información necesaria para realizar las tareas que el software
tiene que hacer y tras pasar por un proceso (compilación, empaquetamiento, despliegue, etc),
se pueden producir los ejecutables que darán vida al software ejecutándose.

El entregar el código fuente al usuario final dependerá del acuerdo comercial al que se 
llegue al inciar el proyecto (por ejemplo, le podemos entregar el puro ejecutable como hace
la mayoría del software comercial o de fuente cerrada), pero también podríamos entregar 
el código fuente entero para que la persona que lo recibe pueda hacer cosas importantes:

- Revisarlo: con el fin de que el software cumpla exactamente con lo que se desea y no tenga
funciones ocultas no deseadas
- Extenderlo: crear nuevas funciones o mejorar las existentes
- Repararlo: si se encuentra alguna falla, eliminarla
- Mantenerlo: A veces, las dependencias del software van quedando desactulizadas y hay que hacer
modificaciones en este para que siga funcionando
- Actualizarlo: llevarlo a nuevas versiones de su lenguaje o hacer que compile o produzca ejecutable
para nuevas plataformas 

Como puedes ver, si quieres que tu software evolucione y se adapte a nuevas necesidades o incluso
simplemente para que se mantenga funcional a través del tiempo, lo ideal es que tengas
el código fuente a tu disposición. Es aceptado que el código funete debe incluir un conjunto de pruebas
automáticas que permitan verificar su funcionamiento más eficientemente. Estas prubas pueden incluir:

- Pruebas unitarias: las que prueban las unidades más básicas del código, como funciones o métodos
- Pruebas de integración: corren el sistema como si fueran un usuario y permiten verifcar que funcione correctamente

Pero el código fuente no basta para que el mantenimiento a través del tiempo sea óptimo.


### Documentación
Esta palabra tan temida por los desarrolladores de software en realidad es uno de nuestos
productos y a la vez insumos más importantes. La documentación es información sobre el 
software puesta en un lugar persistente.

Esta documentación debe incluir por lo menos:

1. Explicación de lo que el sistema hace. Es lo que le llamaríamos "los requerimientos".
2. Diseño del sistema: Se habla de cómo está construido el sistema, por qué se pensó de esta forma y cómo
eso cumple con lo que se requería. Incluye la arquitectura a diferentes niveles y el registro de las decisiones
junto con su justificación.
3. Documentación técnica. En esta parte se habla de la tecnología usada: los lenguajes usados, las plataformas
sobre las que corre, las bases de datos, los sistemas operativos etc. Además una buena idea es incluir
las bases sobre las que se escogieron estos elementos.
4. Documentación para desarrolladores. Esta es la documentación que habla de lo que un desarrollador
tiene que hacer para seguir desarrollando el proyecto o para hacer que el software se ejecute, sea 
desplegarlo en un sistema de usuario final o producir los ejecutables. Esta documentaión incluye la 
documentación del código en el que se describe su funcionamiento interno y el diseño que tiene.
5. Manual de usuario. Opcional, pero dependiendo de la complejidad de las fucniones que el softwae haga
y de su intefaz, puede convertise en un elemento absolutamente necesario. En este se describen
a detalle las cosas que el usuaio puede hacer y las consecuencias de estas acciones.

Hasta aquí se quedarían algunos, ¿pero podemos ir más allá? Sobre todo pensemos en que, para que el software
sea exitoso, necesita evolucionar. ¿Quién crea nuevo código?

### Un equipo funcional
En teoría, con todo lo anterior cualquier desarrollador de software podría tomar un proyecto y seguirlo evolucionando,
pero esta teoría se queda lejos de la práctica por varias razones. La primera es que necesariamente
todos los artefactos anteriores van a tener defectos o estar incompletos, por lo que para que un nuevo
equipo o desarrllador tome el proyecto requerirá hacer lo que llamamos **"arqueología de software"**, intentando completar
y entender las decisiones no documentadas y todas las demás partes de información faltantes.

Aún si los artefactos producidos estuvieran completos, el que un nuevo equipo tome el proyecto requiere tiempo y
esfuerzo para estudiarlos y empezar a producir nuevas funciones o a corregir errores. Si queremos que 
el proceso de desarrollo continue rápidamente, lo mejor es que el equipo que lo desarrolló lo siga evolucionando.

Los mejores proyectos de software incluyen a un grupo de personas  que conocen la forma de desarrollo más 
eficiente, las partes delicadas del proyecto, los fallos pendientes por componer, y las cosas que le faltan.

Además, este grupo de personas tienen una forma de trabajar y de coordinación eficiente que puede ayudarlos
a ser más productivos.

Con esto podemos concluir que el resultado del proceso de desarrollo de software no es solo una serie de artefactos,
sino que también puede inlcuir a un equipo de personas que sereian los más adecuados para seguirlo desarrollando.

Pero hablemos de un elemento no tangible.


### Nuevo conocimiento

Siempre que alguien escribe software, su mente se modifica de tal manera que volver a su estado
anterior es imposible. Este nuevo estado en el que la mente del programador se encuentra
contine información sobre el problema que acaba de resolever, de tal manera que si 
desapareciera todo el código fuente y toda la documentación junto con los ejecutables, para 
este desarrollador no sería tan desastroso porque volver a producrilos le tomaría una 
fracción del tiempo que ya gastó en hacerlos.

Esta modificación en la mente de las personas es un elemento no visible pero sin duda valioso,
que permite crear cada vez software más complejo y con mayores capacidades.


## Conclusión
El proceso de desarrollo de software no sólamente produce software corriendo o ejecutables.
Nuestro trabajo produce otras cosas de valor de las que deberíamos ser conscientes y buscar 
optimizar, evitando la simpleza de pensar que lo único que vale es el software corriendo, que cómo puedes ver en este
artíulo, es una parte mínima de todo el valor que puedes producir, eso sin contar el valor que 
tu software produce al ser ejecutado por las personas que le pueden sacar provecho.
