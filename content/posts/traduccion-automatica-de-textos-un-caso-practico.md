---
title: "Traducción automática: API's vs tu propio modelo"
date: 2020-07-22
author: "Alejandro Santamaría"
tags: ['apis', 'machine-learning', 'AI']
description: "Exploremos las opciones que tienes para realizar traducciones automáticas de texto en tus proyectos."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1586794230/B91A9E8E-0A54-490B-AE3B-0A639064716E_iwwqyx.jpg"
draft: false
---

Traducir texto es una tarea frecuente y que puede realizarse de diferentes maneras, en este artículo queremos explorar algunas de ellas.

Existen sitios donde la traducción puede hacerse en línea, como en [Google Translate](https://translate.google.com.mx/?hl=es), sin embargo, en muchos casos existe un límite en la cantidad de texto que puedes traducir.

También puedes utilizar **APIs que pueden ayudarte a hacer dicho trabajo**, dichas APIs también tiene límites por traducción.

Una solución que nos resulta interesante es la traducción utilizando algún modelo de **Aprendizaje de Máquina** que ya haya sido previamente entrenado.  En este artículo podrás explorar estos diferentes métodos y el código que podrías utilizar para llevarlo a cabo, entendiendo las ventajas y desventajas que cada método ofrece.

Hablemos de los diferentes métodos.

## Interfaz gráfica

Google Translate te permite traducir 5,000 palabras a la vez en su interfaz. Si lo vas a hacer pocas veces y los textos no rebasan esa cantidad de palabras, ¿para qué construir algo?

Esta opción nos recuerda que a veces la mejor solución es que no programemos nada.

**Ventajas**: Inmediata, fácil de usar y sin costo.
**Desventajas**: Requiere intervención humana cada que se tenga que traducir algo.

## API's

Si quieres automatizar las tareas de traducción para integrarlas en un sistema más grande o generar salidas que se queden almacenadas en archivos o bases de datos, una solución es crear un programa que consuma una API de traducción.

Algunas opciones son:

* **Cloud Translation** de Google Cloud Platform. Tiene dos niveles de traducción: el básico que soporta el modelo tradicional de traducción y el avanzado que permite customizar los modelos de traducción además de incluir glosarios y otras monerías.

* [Watson Language Translator](https://www.ibm.com/watson/services/language-translator/) permite traducir una gran cantidad de formatos de texto en muchos lenguajes. La única desventaja es que las API’s de IBM no son las más hermosas y en general sus sitemas de administración fallan bastante.

* **Otras**. En [RapidAPI](https://rapidapi.com/collection/google-translate-api-alternatives) puedes encontrar una colección actualizada de las alternativas a Google Translation API.

Para desarrollar esta pieza de software, lo más recomendable sería crear un wrapper alrededor de la API y exponer a las demás partes del programa sólo los métodos para poder realizar la tarea de traducción, abstrayendo completamente los detalles de cómo se realiza. De esta manera podrías cambiar de API fácilmente (implementando las llamadas a la nueva API) sin irrumpir en la mayoría del programa.

Además esta forma de hacerlo también sería compatible con el siguiente método:

* **AutoML Translation**. Pertenece también a GCP y permite entrenar un modelo mediante el envío de pares de frases para entrenar un modelo que posteriormente puedes usar para hacer traducciones sobre un dominio específico. Es el que más trabajo implicaría de tu parte pero es el que más flexibilidad de tiene.

### Ventajas

Puedes olvidarte completamente de los detalles de implementación de la traducción, del hosting y mantenimiento de esta parte y probablemente las traducciones son muy precisas, como estamos acostumbrados a las de Google.

### Desventajas

Generalmente esta comodidad viene un costo económico que varía dependiendo del uso. La flexibilidad y capacidad de configuración de las API’s es variada y si no funciona como esperas es muy probable que no puedas hacer nada por mejorar la traducción.

## Modelo pre-entrenado de Aprendizaje de Máquina

Los modelos de Aprendizaje Profundo que se han desarrollado de manera importante en los últimos años han sustituido los modelos previos que utilizaban el conocimiento de lingüistas y décadas de investigación estadística.

Una peculiaridad de un modelo de Aprendizaje Profundo es que logra detectar patrones de uso de los lenguajes y utilizar dichos patrones para realizar la traducción de uno a otro. Dichos patrones no tienen una representación equivalente de una palabra en un idioma a otra en un idioma distinto, sino que combinan los patrones internos de uso de las palabras en un idioma y después aplican los patrones que el otro idioma utilizaría. Eso hace que los traductores que utilizan aprendizaje profundo sean mucho más precisos y que las traducciones sean mucho más naturales, además de que pueden adaptarse a casos de uso específicos que los modelos anteriores no contemplaban. ¿Por qué? Porque podemos entrenarlos utilizando un conjunto de datos de entrenamiento que se enfoquen en un dominio específico del lenguaje (ej. traducción de subtítulos de películas, o traducción de textos técnicos).

A pesar de ello, uno de los impedimentos más relevantes para su entrenamiento es que hasta hace algunos años, entrenar un modelo requería grandes cantidades de cómputo y memoria, cosa que ha ido cambiando conforme la industria ha ido evolucionando y los principales proveedores de cómputo han puesto a disposición del mundo, plataformas en la nube donde puede adquirirse poder computacional y de procesamiento de manera sencilla (AWS, Google, Microsoft, IBM, Oracle, etc.). De igual forma, las compañías que crean procesadores especializados (NVIDIA, AMD) también han logrado reducir los costos y poner en manos de cada vez más desarrolladores, tarjetas de video con Unidades de Procesamiento Gráfico (GPUs) a precios cada vez más accesibles.

El modelo genérico de un sistema de traducción basado en Aprendizaje de Máquina consta de dos piezas principales (cada una de ellas una red neuronal por sí misma):

1. Un  codificador de secuencias de palabras (que serían oraciones del texto) que aprende a codificar palabras como un arreglo de números que representa el significado de la oración.

2. Un decodificador de números, que toma un arreglo de números en general y los transforma en oraciones.

La peculiaridad es que en el paso 1 obtenemos ese arreglo de números utilizando el lenguaje de orígen y la decodificación la hacemos hacia el lenguaje destino.

Para poder capturar los patrones y relaciones que existen entre las palabras en una oración, es necesario que la red neuronal cuente con la capacidad de recordar las palabras dentro de una oración, ya que las relaciones de una palabra cualquiera serán mucho más fuertes con ciertas palabras que con otras, por ejemplo la relación entre “la” y “relación” será mucho más fuerte que “él” y “relación”, no esperaríamos poder encontrar un texto donde “él” y “relación” estén presentes en dicho orden específico.

Esta capacidad de “recordar” de una red neuronal no existe en una red neuronal tradicional, donde las entradas pasan y son procesadas por todas las capas de la red sin hacer referencia a las palabras que pasaron antes o las palabras que pasaron después, por ello es que estos algoritmos utilizan un tipo de red neuronal llamado recurrente donde la última entrada influye en la siguiente predicción, esto permite a la red neuronal recurrente “aprender” el “significado” de cada palabra dentro de un contexto.

En tiempos recientes, se han mejorado los modelos de procesamiento del “significado” de las palabras dentro de un contexto utilizando Transformadores que van incluso más allá del simple contexto de una palabra dentro de una oración, modelando las relaciones cruzadas entre cualquier palabra (previa o posterior) en vez de considerar únicamente el orden.

Estos modelos requieren mucho más operaciones matemáticas durante su entrenamiento pero los patrones que pueden identificar las hacen mucho más poderosas, aún así los modelos de recurrentes arrojan resultados bastante aceptables.

Existen casos en particular donde no es necesario entrenar tu propia red neuronal recurrente, ya que es probable que alguien más lo haya hecho ya. Esto puede ahorrarte muchas horas de procesamiento de información y el entrenamiento y validación del proceso de entrenamiento.

El proceso que se sigue es:

1. Obtener un corpus o conjunto de datos sobre el problema que quieres resolver (por ejemplo, textos en el idioma de origen y en el idioma destino.
2. Limpieza y normalización de este corpus que remueva errores o piezas de los textos que sean incompletas o por ejemplo se puede decidir utilizar todas las palabras en minúsculas, separar las oraciones por ciertos símbolos de puntuación, etc. estas decisiones deberán tomarse teniendo en cuenta los objetivos para los cuales utilizaremos nuestro modelo de traducción, no es lo mismo un traductor de textos formateados de manera regular a textos que por ejemplo se vayan a utilizar como subtítulos para películas. Los pasos que normalmente se utilizarán tendrán como mínimo, código para separar las oraciones, y normalizar el texto.

### Utilizando un modelo de traducción prefabricado

Si quieres experimentar con este tipo de modelos te recomiendo empezar por el uso de un modelo pre-entrenado y dependiendo de los resultados evaluar si es necesario entrenar uno especializado en la tarea que estás buscando resolver.

Aunque hay varios modelos disponibles, te dejo la liga a un framework hecho en C++ y que tiene un número mínimo de dependencias, se llama [Marian Neural Machine Translation](https://marian-nmt.github.io/quickstart/) y como parte de sus peculiaridades es que es eficiente, puede utilizar varios procesadores gráficos para el entrenamiento y soporta el uso de CPU o GPU para la traducción (al poder utilizar sólo CPU hace que el modelo pueda utilizarse en computadoras que no tienen tantos recursos).

Y aquí hay un modelo pre-entrenado que puede utilizarse para traducciones de español a inglés: [Spanish to English Translation](https://github.com/ageitgey/spanish-to-english-translation)

Si tuvieras necesidad de entrenar la red neuronal sería necesario que tuvieras datos paralelos, es decir el mismo texto en los dos idiomas entre los cuales quieres hacer la traducción. Aquí te dejamos la liga a uno de ellos: [The open parallel corpus](http://opus.nlpl.eu/)

### Ventajas

* Puede adaptarse mediante el entrenamiento, a un estilo o tipo específico de textos (textos científicos, técnicos, informales, subtítulos, etc.)
* Puede utilizarse en modo “offline” sin necesidad de estar conectado a alguna fuente externa de internet.
* No tiene costos o límites de uso, más que aquellos resultado de operar el modelo una vez entrenado (y de entrenarlo si fuera necesario hacerlo).

### Desventajas

* Entrenarlo requiere una gran cantidad de datos y un proceso de limpieza/normalización que no son técnicamente sencillos.
* Es probable que no sea sencillo alcanzar el nivel de entrenamiento que las grandes compañías han utilizado para entrenar sus propios modelos (porque seguramente tienen fuentes bastante grandes de datos/procesadores gráficos/etc).
* Escalarlo para su uso masivo puede ser todo un reto.
* Las redes neuronales son cajas negras por lo que si se detecta algún error en la traducción normalmente será muy difícil saber en qué parte de los datos de entrenamiento se introdujo el error y por lo tanto será difícil removerlo.

En el siguiente artículo te contaremos cómo nos fue con las pruebas.
