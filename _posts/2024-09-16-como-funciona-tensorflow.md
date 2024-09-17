---
title: ¿Cómo funciona TensorFlow?
date: 2024-09-16
author: Héctor Patricio
tags: tensorflow machine-learning ai deep-learning
comments: true
excerpt: >-
  TensorFlow permite crear modelos de aprendizaje automático sin que te tengas
  que plear con la forma en la que se hacen los cálculos en los ejecutores. Hablemos
  más de cómo funciona.
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1450/v1725143057/gabriel-izgi-cfQEO_1S0Rs-unsplash_ihiase.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_450/v1725143057/gabriel-izgi-cfQEO_1S0Rs-unsplash_ihiase.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

**TensorFlow** es una de las herramientas más populares e influyentes
en el campo de la del aprendizaje automático. En este artículo vamos a ver
qué es exactamente y cómo funciona.

## ¿Qué es TensorFlow?

Siempre que hablamos de TensorFlow se dice que es una "biblioteca (o librería)
para hacer aprendizaje automático, pero este definición no es muy
explícita y por eso vamos a ver _cómo nos permite_ crear modelos de
aprendizaje.

Para crear modelos de aprendizaje automático, tenemos que hacer muchos cálculos
matemáticos, la gran mayoría son operaciones de multiplicación de matrices.
Estos cálculos no son eficientes en un procesador tradicional y por eso se
requiere de toda la ayuda que se pueda conseguir para hacerlos lo más rápido
posible y gastando menos energía.

Es aquí donde entra **TensorFlow**, una biblioteca que permite _representar_ estos
cálculos mediante grafos de cómputo y después ejecutarlos en procesadores
especializados como tarjetas gráficas y otros procesadores eficientes en
operaciones matemáticas pesadas. Además, TensorFlow abstrae al usuario final (tú),
de los detalles de implementación de muchas funciones y operaciones matemáticas
que se usan mucho en el aprendizaje automático. Y finalmente, con su _API_ de alto
nivel, **Keras**, te permite crear diferentes tipos de redes neuronales sin
que tengas que pelearte con los detalles de implementación.

Y es aquí donde empieza lo interesante. ¿Qué es un grafo de cómputo? ¿Cómo
llegamos a él y para qué nos sirve? Veamos.

## Grafos de cómputo de TensorFlow

Para entenderlo, vamos a ver un ejemplo sencillo de un cálculo y su
representación, por ejemplo, sumemos dos números, que llamaremos X y Y.

¿Cómo representa TensorFlow esto? Este es el grafo de cómputo que podemos ver con
una herramienta de análisis de TensorFlow llamada TensorBoard:

![Imagen de un grafo de cómputo de TensorFlow](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_250/v1726379906/Screenshot_2024-09-14_at_23.53.34_1_izykn5.png){: .align-center}

Puedes pensar en este grafo como una serie de nodos que representan cada uno
una operación sobre conjuntos de datos numéricos llamados tensores. Cuando
ejecutamos este grafo, los tensores _fluyen_ por estos nodos, transformándose
en cada uno, hasta que obtenemos el resultado final de la operación. (Los nodos
que dicen `Identity` son operaciones de copia o lectura de valores, útiles para
el funcionamiento interno de  TensorFlow).

La otra cosa que podemos notar hasta abajo de la gráfica son los dos nodos que
representan nuestros números simples: X scalar y Y scalar, ya que los definimos
como números simples, que también pueden pensarse como tensores de una dimensión.

Formalmente, TensorFlow te da una serie de estructuras de datos, que puedes
ir construyendo poco a poco para definir todas las operaciones que necesites hacer.

En una red neuronal, estos grafos son mucho más complicados, pero justo ese es
el trabajo de TensorFlow: ayudarte a definirlos y a ejecutarlos en el hardware
más conveniente para tu proyecto.

Usar los grafos de cómputo de TF te permite varias cosas más:

- **Optimización de las operaciones**: TensorFlow tiene todo un sistema de optimización
llamado `Grappler`, que se encarga varias optimizaciones.
- **Paralelización**. Con las operaciones divididas, TensorFlow puede verificar
qué operaciones son independientes y puede ejecutarlas en otros procesadores
si están disponibles.
- **Exportación**. Una vez teniendo las operaciones definidas en un grafo, no necesitamos
de Python para ejecutarlas, así que TensorFlow puede ejecutarlas en otros dispositivos
y usando otros lenguajes.

Esta definición de grafos de cómputo no es la única forma de trabajar con TensorFlow,
ya que desde su versión 2.0, también permite trabajar con un modo más imperativo,
que se siente más integrado con Python y más dinámico: la ejecución adelantada (en
inglés: _eager execution_). Con esta forma de ejecución, las operaciones se van
ejecutando inmediatamente después de definirlas. Esto es más fácil de programar y
de leer, pero deja poco espacio para la optimización. Es justamente como la comparación
entre un lenguaje compilado y uno interpretado.

## TensorFlow y Keras

Keras era otra biblioteca que se creó por separado, para hacer más fácil de usar
la versión 1.0 de TensorFlow, que era bastante más verbosa de programar (por sólo
soportar grafos de cómputo estáticos).Sin embargo, en la versión 2.0 de TensorFlow,
Keras se volvió parte del paquete.

Keras te permite crear modelos de aprendizaje profundo de manera sencilla. Es la
manera fácil de usar TensorFlow, pero también te permite complicarte tanto como quieras
o necesites (esperamos que sea esto último). Keras usa el principio de "revelación
progresiva de la complejidad", lo que significa que puedes empezar de manera muy
sencilla e ir aprendiendo cosas conforme vayas avanzando en hacer cosas más complejas.

Así que la forma más común de usar TensorFlow para crear tus modelos de machine
learning es mediante la interfaz de Keras, que además de todo te provee de
utilidades que son de uso muy común en las redes neuronales. Por ejemplo, provee
regularizadores, inicializadores, funciones de activación, optimizadores, y muchas
utilidades más. Es por eso que ya casi no se concibe el uso de TensorFlow para
casos comunes sin usar Keras.

## TensorFlow y MLIR

MLIR es una herramienta para crear compiladores hecha por parte del mismo
equipo que hizo LLVM, la infraestructura para compiladores que está detrás
de la mayoría de los compiladores modernos.

La especialidad de MLIR es hacer traducciones para arquitecturas de hardware no
tradicionales,usando un lenguaje intermedio multi-capa al que le puedes agregar
más plugins para diferentes arquitecturas de ejecutores. MLIR es muy usado
para computación de alto rendimiento, justamente la que necesitamos para
crear modelo de aprendizaje automático complejos en tiempos y con costos
razonables.

Así que TensorFlow, aprovechando este sistema, usa MLIR para compilar los
grafos de cómputo y los modelos para hardware específico, para que se pueda
obtener el mejor rendimiento posible.

## TensorFlow y su relación con el hardware

Después de la sección anterior, es muy probable que la relación de TF con
el hardware quede muy clara: TensorFlow ayuda a que se pueda compilar
de mejor manera el código con los cálculos para poder ejecutarlo
en el hardware especializado.

**IF** soporta gran variedad de tipos de hardware y es por eso que hasta el
momento es la biblioteca de machine learning con mejor soporte para
distribuir tus modelos en diferentes dispositivos, desde procesadores
especializados hasta que corran directamente en tu teléfono o navegador.

## Conclusión

Si quieres hacer machine learning, lo más probable es que tengas que
aprender TensorFlow, una herramienta muy útil para hacer los modelos usados
hoy.

Espero que lo que hablamos sobre TensorFlow en este artículo te haya ayudado
a entenderlo un poco más. En otro artículo hablaremos de su competidor
más directo: **PyTorch**.
