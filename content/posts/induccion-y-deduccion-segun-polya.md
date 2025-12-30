---
title: "Inducción y Deducción para desarrolladores de software"
date: 2019-12-14
author: "Héctor Patricio"
tags: ['polya', 'problem-solving', 'how-to-solve-it', 'problemas', 'libros']
description: "Aprende de los conceptos de inducción y deducción según George Polya los explica en How to Solve It"
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1575746191/verne-ho-0LAJfSNa-xQ-unsplash_prh7gv.jpg"
draft: false
---

Este es el tercer artículo acerca del libro ["How to Solve It"](https://amzn.to/2P8HJA8) de George Polya. Puedes ver los dos artículos anteriores aquí:

- [Técnicas para resolver problemas](/2019/09/27/tecnicas-para-resolver-problemas.html)
- [Heurística](/2019/10/03/el-arte-de-resolver-problemas-la-heuristica.html)

Con este artículo cerraremos con las ideas que George Polya desarrolló para resolver problemas.

## Deducción

Tratar de resolver problemas por deducción significa **aplicar principios o
conocimiento general a un caso específico**. Por ejemplo para un problema
práctico en el que tenemos encontrar la longitud de un cable tensor para una
antena, sabemos que podemos aplicar el teorema de Pitágoras.

Algunos ejemplos para los programadores:

- Encontrar el elemento más grande o más pequeño en una lista. (Una forma de resolverlo es ordenar los elementos).
- Revisar que un elemento no está repetido en una colección de elementos. (Indexado)
- Asegurarse de que las operaciones son atendidas en el orden en que se solicitaron en un entorno con múltiples ejecutores. (Colas)

Lo difícil de la deducción es encontrar *qué principios, teoremas o formas
de resolución de problemas aplican para el problema que tenemos que resolver*. Para esto nos pueden ayudar las técnicas platicadas en los artículos anteriores: ¿He resuelto un problema similar? *¿Qué técnica fue usada?* ¿Qué principios sirvieron para la resolución de ese problema? Y, a mi parecer la más útil: ¿puedo usar el resultado o el proceso de resolución de un otro problema?

### Deducción en el desarrollo de Software

Imagínate un problema que te trae un cliente, como sigue: tienen un proceso que necesita recorrer una lista muy grande de clientes por la noche y tienen algunos errores intermitentes, a veces termina, a veces no y cuándo no termina hay que investigar quién no pudo ser procesado y aplicar el proceso individualmente.

Si has tenido experiencia en procesos parecidos y te has enfrentado con problemas similares, seguro que empezaste a pensar en soluciones. Eso es deducción, aunque las reglas no estén formalmente establecidas en tu mente.

¿Cómo usamos la deducción entonces? Conociendo soluciones o diseño de solución a problemas que se repiten y que podemos aplicar directamente o combinar para resolver el problema actual.

¿Te suena? Esto es algo que se repite vez tras vez: tener las **bases de las ciencias de la computación**, conocer diferentes algoritmos, estructuras de datos, tipos de datos abstractos, patrones de diseño, principios de diseño de software te ayudará a resolver los problemas de manera eficaz.

Así que la lección es clara: intenta ampliar tus conocimientos básicos para que puedas hacerte más hábil resolviendo problemas.

Tener un registro palpable de tus aprendizajes como una serie de notas te permitirá repasarlos y consultarlos cuando los necesites.

## Inducción

> La inducción es el proceso de descubrir **leyes generales** mediante la **observación y combinación** de casos particulares. - *George Polya*

La inducción es uno de los mecanismos de resolución de problemas más difíciles de llevar a la práctica. Funciona en forma inversa a la deducción:

Consiste en partir de observaciones específicas (ejemplos y contra-ejemplos) y llevarlas a **generalizaciones** que puedan ser aplicadas en otros casos o que apliquen en muchas otras situaciones situaciones.

Polya deja claro una cosa: aunque en las ciencias físicas y naturales la inducción es completamente válida y natural, y generar conocimiento sólamente basado en esto es aceptable, pero en las matemáticas debes poder tener **demostraciones** de que lo que propones es cierto.

### Inducción matemática

Polya habla de otro tipo de inducción de la que opina que no debería llamarse así, y que comparte muy poco con el proceso que acabamos de describir y puede llegar a confundir a la gente: la **inducción matemática**. Este tipo de inducción se refiere al método que los matemáticos emplean para **demostrar** que cierta aserción es un teorema o no.

Si has estudiado inducción matemática no la confundas.

### Inducción en el desarrollo de software

El desarrollo de software no es un área que viva aislada de las demás áreas y seguro te has encontrado con este tipo problemas si ya llevas tiempo desarrollando: las personas que requieren el software llevan **ejemplos** de  problemas que regularmente tienen que resolver, en vez de la explicación completa y las reglas completamente establecidas.

Nuestros clientes, en general, no se han dado a la tarea de establecer las reglas por las que algo funciona de la manera en que lo hace, ni las excepciones, ni los casos únicos. Es nuestra tarea casi siempre **descubrir las reglas que subyacen a la operación del negocio de los clientes.** Para esto tenemos que aplicar la inducción.

Este paso es completamente necesario para desarrollar software, ya que son **estas reglas** las que ponemos en los programas, las probamos con los tests y lo que hace valioso al software.

Así que tenemos que ser lo más hábiles que nuestras circunstancias lo permitan haciendo inducción. **¿Cómo podemos mejorar?**

### Desarrollando tus capacidades de Inducción

Polya da varios de consejos para aplicar la inducción, veamos algunos pasos.

#### Las tres herramientas de la inducción

Primero entendamos cómo funciona el proceso de inducción. La inducción usa tres procesos para poder llegar a sus descubrimientos:

1. **Generalización**. Tomas un ejemplo e intentas quitarle las cosas que lo hacen único para crear una regla general.
2. **Analogía**. La generalización está basada en analogías: la aplicación de los mismos principios observados a otros casos.
3. **Especialización**. Aplicas tus descubrimientos a casos particulares y descubres casos **especiales** que hacen que tengas que ajustar

Ahora vemos los pasos que podrías seguir para llevar a cabo tu proceso.

#### Reunir ejemplos y ocurrencias

Primero, tienes que juntar o generar ejemplos del fenómeno o evento que estás resolviendo. En el caso de un sistema tendrías que solicitarle al cliente la mayor cantidad de situaciones que tenga disponibles.

"Generar" ejemplos ciertamente es algo difícil, porque al no conocer las reglas puede que te equivoques varias veces. Justamente es un proceso de prueba y error.

#### Hacer hipótesis

Después de **observar** los ejemplos y tratar de descubrir un patrón entre ellos, establece **explícitamente** una hipótesis: un supuesto plausible que explique la relación entre los ejemplos y que permita generar otros.

#### Comprobar o refutar la hipótesis

Después de tener una hipótesis, ahora tienes un "problema para probar", como les llama Polya. Intenta demostrar que la hipótesis es cierta. Polya afirma que en la matemáticas no existe autoridad que una demostración rigurosa, pero en nuestra área, el desarrollo de software, a menudo es impráctico tener dicha demostración, así que podrías comprobar con más ejemplos (o ejemplos sintéticos) que tu hipótesis o propuesta se mantiene cierta en todos los casos conocidos.

Si logras comprobarla, puedes avanzar a lo siguiente. Si encuentras un caso que no esté cubierto por tu hipótesis actual puedes ajustarla. Lo  mejor de este proceso es que es cíclico: no hay un límite de veces que lo puedes aplicar hasta que tengas "las regla0s" lo suficientemente claras.

Si lo piensas, se parece mucho al _método científico_ que nos enseñaron cuando nos hablaban de ciencia: observación -> hipótesis -> experimento -> conclusiones.

## Conclusión

La inducción y la deducción son dos procesos que aplicamos normalmente, sin saberlo, en nuestra resolución diaria de problemas. Identificarlos y formalizar su estructura nos puede ayudar a ser mejor en ellos. No pierdas la oportunidad de aprender y ampliar tus capacidades de resolución de problemas.

Además, la información que encontrarás en "How To Solve It" te ayudará a ser mejor resolviendo problemas, por lo que tu capacidad como desarrollador de software se verá potenciada: **es nuestra principal tarea**.
