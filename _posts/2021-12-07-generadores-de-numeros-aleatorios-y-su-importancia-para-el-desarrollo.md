---
title: "Generadores de números aleatorios y su importancia"
date: 2021-12-07
author: Héctor Patricio
tags: prng criptografía randomness aleatoriedad
comments: true
excerpt: "Los números aleatorios son muy importantes para el desarrollo, sobre todo para la seguridad de la información y la criptografía."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1120/v1638939680/erica-li-UCGvgdlbYGk-unsplash_iucni9.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_320/v1638939680/erica-li-UCGvgdlbYGk-unsplash_iucni9.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Muy comúnmente los sistemas informáticos requieren de valores aleatorios para diferentes procesos, por ejemplo, para ordenar las cosas, para seleccionar elementos de un conjunto, para simulaciones, para tomar diferentes caminos en un proceso (como los videojuegos).

Un lugar en el que los valores aleatorios tienen una importancia especial es **en criptografía** y en la seguridad informática. De hecho, los números aleatorios están muy relacionados con la generación de valores usables en criptografía como llaves, por ejemplo.

Veamos cómo se generan y cómo puedes usar correctamente los generadores de números aleatorios, pero antes empecemos a hablar de qué es la aleatoriedad y cómo podemos entenderla intuitivamente.

## Aleatoriedad

La aleatoriedad tiene que ver con la _probabilidad_ de obtener cierto valor de un conjunto (universo) de valores posibles. Los valores aleatorios son impredecibles, no puedes asegurar que uno tiene más probabilidades de salir que otro. Ahora conecta los dos conceptos anteriores: para que un valor sea aleatorio debe de ser extraído de un conjunto de valores con la misma probabilidad de aparecer, lo que se conoce como una **distribución uniforme**.

**Ejemplo:** una moneda lanzada puede entregar dos valores, cara o cruz (águila o sol en México). Es imposible asegurar que va a salir uno u otro valor, debido a que ambos valores tienen la misma probabilidad de salir. Y muchos procesos físicos se comportan de esta misma manera.

Si en el universo de valores posibles es más probable que salga cierto valor, entonces empezamos a perder aleatoriedad, imagínate por ejemplo el caso de una moneda o dado cargado.

Los humanos percibimos un valor como aleatorio si _parece_ poco probable que hayamos obtenido ese valor específicamente, pero no siempre es así.

La aleatoriedad se puede medir a través de _entropía_, que es la cantidad de información disponible en todo el espacio de valores. La entropía es la sumatoria de la probabilidad de aparecer de cada valor multiplicado por su logaritmo base 2, y **se mide en bits**. Una generador con aleatoriedad perfecta entrega **tantos bits de entropía como valores posibles**.

## Generadores de números aleatorios

Los programadores podemos usar la aleatoriedad si tenemos un **generador de números aleatorios**.

Un generador de números aleatorios es un programa que te entrega una **serie de bits** aleatorios, es decir, impredecibles desde el punto de vista externo. Estos bits se pueden usar entonces para crear un número aleatorio.

Haya generadores de diferentes tipos dependiendo de su fuente de entropía (información impredecible) y de cómo la usen. Hablemos de los diferentes tipos, sus características, y cómo usarlos.

## True Random Number Generators

A esta clase de generadores también se le conoce simplemente como **generadores de números aleatorios** (Random Number Generators o **RNG's**). Los RNGs toman su fuente de entropía de **lugares físicos**, dado que el mundo real es impredecible. Miden las variaciones en los semiconductores, la manera en la que mueves el ratón, el teclado, información de los sensores de la computadora, el micrófono, la red y muchas otras cosas. Hay algunos que toman su entropía de procesos cuánticos incluso, conocidos como **generadores de números aleatorios cuánticos** o _QRNGs_.

Estos elementos físicos son fuentes confiables de entropía, pero no podemos confiar en nuestra manera de medirla o "capturarla", además de que pueden ser sesgados por un usuario malintencionado o atacante. Además son lentos para generar los bits aleatorios que las aplicaciones pueden requerir.

Es normal que un RNG se quede sin suficiente entropía para servir a las aplicaciones que lo usan, por lo que terminaría bloqueándola o haciéndola insegura.

Es por esto que los generadores de números aleatorios a menudo se complementan de los generadores de números pseudo-aleatorios, de los que hablaremos a continuación.

## Pseudo-Random Number Generators

Los generadores de números pseudo-aleatorios (**PRNGs**) son aquellos que no toman su fuente de entropía de lugares físicos, sino que la generan a partir de una semilla o _seed_. Siempre que reciban la misma semilla generarán la misma secuencia de bits que _parece_ aleatoria, pero en realidad es determinista.

Si conocemos la semilla y el algoritmo, podríamos predecir la secuencia de bits que resultará en cada llamada. Si la distribución de probabilidad de los bits es uniforme o cerca de uniforme, entonces la secuencia de bits parecerá aleatoria, lo cuál es útil para la mayoría de las aplicaciones.

Los PRNGs no se quedan sin entropía para seguir sirviendo bits, ya que la generan artificialmente, normalmente con algoritmos matemáticos y _piscinas_ o _pools_ de bits.

Una forma de crear un PRNG es usando como semilla un RNG, que tome su fuente de lugares físicos y _expendiendo_ esta entropía a un número más grande de bits. Esto lo hace mediante la actualización de un estado interno mediante la recepción de bits verdaderamente aleatorios de un RNG.

## Cryptographically Secure Pseudo-Random Number Generators

Los PRNGs critpográficamente seguros requieren dos características extras para ser usados en criptografía:

1. **Discreción hacia adelante**. En inglés conocida como **forward secrecy**, se refiere a que es imposible predecir los bits que generará a continuación.

2. **Discreción hacia atás**. Se refiere a que, dados los bits de un número aleatorio generado, es imposible conocer los bits que le precedieron, que se entregaron en llamadas anteriores.

Cuando hablamos de **"imposible**" en términos de criptografía, normalmente nos referimos a que es _computacionalmente infactible_ resolver el problema propuesto. Para que esto sea cierto basta con que no exista un **algoritmo de tiempo polinomial** que funcione para resolver el problema.

En pocas palabras, los PRNGs criptográficos son _impredecibles completamente_.

## Ejemplos

Algunos PRNGs que puedes usar son:

- **/dev/urandom** de los sistemas UNIX: genera bits aleatorios combinando lecturas del uso del sistema (RNG de hardware) y un generador por software, de manera que haya siempre suficientes bits. Si quieres conocer más a detalle cómo funciona, este artículo te lo explicará: [Understanding random number generators and their limitations on Linux](https://www.redhat.com/en/blog/understanding-random-number-generators-and-their-limitations-linux).

- **[Meresenne Twister](https://github.com/ESultanik/mtwister)**: genera bits aleatorios con una distribución uniforme, pero no sirve para criptografía porque es predecible. Dada cierta cantidad de bits es posible predecir la secuencia de bits que generará a continuación. Aún así, el MT se comporta mejor que algunos otros PRNGs incluidos en los lenguajes de programación.

- **PRNG's en procesadores**: Tanto AMD (desde 2015), como Intel (Desde 2013) tienen PRNGs embebidos dentro de los procesadores que pueden ser usados mediante instrucciones específicas (RDRAND y RDSEED).

- **Fortuna**. Es un algoritmo criptográficamente seguro diseñado en 2003, en el que están basadas la generación de números aleatorios de MacOS y iOS.

## Cómo usar un PRNG

Si quieres generar números aleatorios para uso general, sin garantía de que sea impredecible, puedes usar un PRNG común implementado en tu lenguage de programación favorito. Generalmente las funciones `rand()` de Python o `mt_rand()` de PHP son bastante buenas para esto.

Sin embargo, para generar números aleatorios para criptografía, debes usar un PRNG especializado, generalmente basado en los provistos por el sistema operativo.

Aunque podrías escribir una función que se comunique con el sistema operativo para obtener un flujo de bits aleatorios, tendrías que hacer lo suficiente para asegurarte de que esos bits sean de calidad (con una alta entropía). Es por esto que como desarrollador es mejor usar las implementaciones de la biblioteca estándar de criptografía de tu lenguaje, a menos que tengas requerimientos muy específicos, y sobre todo, sepas cómo verificar que tienes la entropía suficiente.

## Conclusión

Conocer cómo funciona un PRNG, a parte de algo interesante, es útil para no usarlos mal. Siempre que requieras números aleatorios para usarlos con relación a la seguridad de la información, **deberías usar un PRNG criptográfico**. En cualquier otro caso, un PRNG como el _Meresenne Twister_ es suficiente. Además, ahora sabes que los RNGs basados en procesos físicos, a pesar de las garantías de entropía que prometen, no son muy confiables en el sentido de que no siempre están disponibles, pero hay soluciones de hardware especializadas que te pueden ayudar si tienes un problema muy específico.

Finalmente, la mejor opción para usar un PRNG es confiar en la implementación de la plataforma y lenguaje en el que estés trabajando.
