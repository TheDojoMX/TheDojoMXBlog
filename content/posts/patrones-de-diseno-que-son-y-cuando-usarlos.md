---
title: "Patrones de diseño: qué son y cuándo usarlos"
date: 2019-02-23
author: "Héctor Patricio"
tags: ['design-patterns', 'gof', 'software-engineering', 'programación', '"patrones', 'de', 'diseño"']
description: "Los problemas que tienes hoy, otros los han resuelto antes. Aplica soluciones probadas a problemas que se repiten vez tras vez."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1220/v1551506407/photo-1456611984355-c05be968ebe9_nwptjx.jpg"
draft: false
---

Parte del conocimiento fundamental de un desarrollador profesional de software son los *Patrones de diseño* (Design Patterns). En este artículo explicamos de manera concisa:

1. Qué son
2. De dónde vienen
3. Por qué deberías aprender algunos cuantos
4. Por dónde empezar

## Qué son los patrones de diseño

"No hay nada nuevo bajo el sol": es una conocida frase que quiere decir que gran parte de los
problemas que la humanidad se ha enfrentado se siguen repitiendo vez tras vez. Aprovechando este conocimiento, los patrones de diseño se pueden definir como:

> Soluciones estándar a problemas conocidos (que se repiten) en el desarrollo de software

Es decir, son soluciones que sabemos que funcionan para problemas que sabemos que existen desde antes que nosotros los encontráramos. Así de sencillo.

## Composición

Los patrones de diseño de software, se componen de cuatro partes:

1. *Nombre.* Permite referirte al patrón unívocamente y hablar con otras personas sobre esta solución específica sin tener que explicarla.
2. *Problema.* La situación que resuelve el patrón específico. Incluye el contexto y los _síntomas_ que se tienen que dar para usar este patrón.
3. *Solución.* Describe todas las partes necesarias, su estructura y relacions que resuelven el problema _sin hablar de una implementación específica_, ya que un patrón se debe poder aplicar y adaptar a muchas situaciones diferentes.
4. *Consecuencias.* Los resultados de aplicar este patrón tanto negativos como positivos, con el fin de poder evaluar si es conveniente usarlo.

## Historia

Como muchas otras cosas en la joven industria del desarrollo del software, el concepto de patrones de diseño
fue adaptado de otro campo: la arquitectura, o el diseño de espacios físicos habitables.

El arquitecto [Christopher Alexander](https://en.wikipedia.org/wiki/Christopher_Alexander) se dio cuenta que al diseñar edificios y
ciudades era común encontrarse con situaciones que se repetían una y otra vez. Así que empezó a crear una colección de estos problemas
comunes y las soluciones que le habían funcionado, con lo que empezó a crear un "lenguaje de patrones". Aquellas personas
con las que compartía el conocimiento del problema y de la solución podían referirse a estos
por los nuevos nombres sin tener que explicarlo todo de nuevo.

En su libro _A Pattern Language (1977)_ puso por escrito una serie de patrones para situaciones
de diseño arquitectónico para casas y edificios.

Esto inspiró a [Kent Beck](https://en.wikipedia.org/wiki/Kent_Beck) y otras personas para usar
y hablar de soluciones parecidas para el desarrollo de software, aproximadamente 10 años
después de la publicación del libro.

[Erich Gamma](https://en.wikipedia.org/wiki/Erich_Gamma) y otros tres autores conocidos como la "Banda de los cuatro"(Gang of Four o [GoF](http://wiki.c2.com/?GangOfFour)) publicaron un libro
llamado _[Design Patterns: Elements of reusable Object-Oriented Software](http://wiki.c2.com/?DesignPatternsBook)_ que popularizó el término "Patrones de diseño" y mostró 23 patrones enfocados en la programación de sistemas y divididos en 3 categorías:

1. *Creacionales*: Se enfocan en la forma de crear nuevos objetos
2. *Estructurales*: Establecen la manera de relacionar objetos y clases (composición y herencia)
3. *De comportamiento*: Se centran principalmente entre la comunicación entre objetos.

Este es un libro obligado como referencia si quieres mejorar tus habilidades de desarrollo y diseño de software.

## Importancia

Conocer y usar los patrones de diseño nos da varias ventajas importantes:

1. Permite que usemos soluciones probadas (o evitemos soluciones refutadas) por el tiempo, en muchos proyectos y muchas otras personas y evitemos otras que no han funcionado tan bien.
2. Nos dan un lenguaje común que otras personas, que también entienden este "diccionario", pueden comprender sin la necesidad de una explicación detallada. Esto es de gran importancia porque gran parte del proceso de desarrollo es entender el código que otros escribieron. Si entiendes los patrones de diseño más comunes, será mucho más fácil que entiendas el código y la arquitectura de otros programas que los usan.
3. Nos dan la flexibilidad de construir sobre ellos. El que exista patrón que seguir no significa que siempre se tenga que implementar a la perfección, sin cambios. Estos patrones dan la capacidad de aprovechar las características que sirven para nuestro problema específico y agregar nuevas para adaptarlo completamente a nuestro problema.
4. Pueden reducir la complejidad de un proyecto si son bien usados.

## En contra de los patrones de diseño

Todo en la vida y sobre todo en el desarrollo de software representa un intercambio de valor. Damos algo a cambio de otro bien, y nos corresponde personalmente evaluar si una herramienta en una situación determinada es conveniente. Deberíamos evitar usar algo simplemente porque los demás dicen que lo debemos usar o es lo más utilizado por todos. Además tenemos que evitar caer en lo que Cal Newport llama la mentalidad de _["el mínimo beneficio"](http://www.helwyssocietyforum.com/the-any-benefit-mentality/)_, aquella en la que justificamos el uso de algo sólo porque nos da un pequeño beneficio, sin considerar lo que damos para obtenerlo.

Dado el sermón anterior, pensemos en los contras de los patrones de diseño:

1. La urgencia de aplicar nuestro recién adquirido conocimiento nos puede llevar a buscar aplicar soluciones complicadas en donde no pertenecen.
2. Algunos patrones han probado con el tiempo en realidad ser anti-patrones (te veo a ti [singleton](https://stackoverflow.com/questions/12755539/why-is-singleton-considered-an-anti-pattern)), soluciones que no se deberían aplicar nunca, o que es extremadamente difícil justificar su uso.
3. A veces, la necesidad de aplicarlos revela el mal diseño de alguna otra parte de nuestro sistema: desde la estructura de nuestro sistema, hasta el lenguaje y la elección de otras herramientas.
4. Los patrones de diseño tradicionales están casados con la programación orientada a objetos, que no siempre es la mejor para resolver el problema, aunque es lo más usado actualmente.

Hay toda una horda de programadores respetados que han hablado en contra de los patrones de diseño (como [Peter Norvig](http://norvig.com/design-patterns/design-patterns.pdf), para quien los patrones de diseño son flaquezas de tu lenguaje).

## Por dónde empezar

Habiendo hablado de las ventajas y advertencias, ¿por dónde puedes empezar, si te interesa?

Los siguientes recursos son útiles:

1. [Design Patters: Elements of reusable Object-Oriented Software](https://www.amazon.com/Design-Patterns-Object-Oriented-Addison-Wesley-Professional-ebook/dp/B000SEIBB8). El libro de referencia de los patrones de diseño clásicos. También está en español, aunque es un poco difícil de conseguir.
2. Para Python específicamente: [Python Patterns](https://github.com/faif/python-patterns) y

3. [Python 3 Patterns](https://python-3-patterns-idioms-test.readthedocs.io/en/latest/index.html)
4. [Head First Design Patterns](https://www.amazon.com/Head-First-Design-Patterns-Brain-Friendly/dp/0596007124). A este libro se refieren como una guía con bromillas tontas y super pedagógica.

Puedes encontrar una referencia completa de los patrones de diseño en [wikipedia](https://es.wikipedia.org/wiki/Patr%C3%B3n_de_dise%C3%B1o).

En este blog, publicaremos artículos dedicados a patrones de diseño, explicando cómo los hemos usado en nuestro trabajo diario, en los que explicaremos:

1. El patrón
2. Cómo reconocer una situación para usarlo
3. Su implementación (normalmente en Python)
4. Otras maneras de aplicarlo
5. Las desventajas de este patrón

## Conclusión

Un patrón de diseño es una solución "probada" aplicada a un problema conocido y repetido en diferentes circunstancias. A veces pueden fallar.

Conocer los patrones de diseño definitivamente te hará un mejor programador por su extendido uso. Aplicarlos _puede_ y _normalmente_ mejorará la arquitectura de tus programas y proyectos, **pero hay que ser cautelosos**. Aprender cómo se aplican es una buena inversión de tiempo, que te puede devolver grandes beneficios.

Gracias por leernos y no dudes en dejarnos tus comentarios.
