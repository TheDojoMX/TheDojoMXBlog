---
title: "Intro a Machine Learning: Entendiendo el perceptrón"
date: 2021-03-25
author: "Héctor Patricio"
tags: ['machine-learning', 'ml', 'aprendizaje-automático']
description: "En este artículo entenderemos las bases matemáticas y de programación de la unidad de construcción básica de lo que comercialmente se conoce como redes neuronales"
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1616115397/robynne-hu-HOrhCnQsxnQ-unsplash_sos5ux.jpg"
draft: false
---

Hablar de aprendizaje automático y los términos que lo rodean, muchas veces intimida a los desarrolladores. En esta serie de posts vamos a intentar explicar los conceptos detrás del aprendizaje automático y llevarlos a la práctica.

## Acerca de los nombres de las cosas

Antes de empezar a hablar de inteligencia artificial, aprendizaje automático, aprendizaje profundo y todas esas cosas, queremos hacer una nota sobre el nombrado en las asuntos de tecnología.

Primero, debemos recordar que la tecnología no existe en un entorno aislado, y generalmente no tiene uso por sí misma, sino que la usamos para servir a otras áreas. Es por eso que lo que conoceríamos por un nombre completamente acertado y descriptivo de acuerdo a sus características técnicas se tiene que renombrar para que otras personas no pertenecientes al área de desarrollo de software.

Así ha pasado vez tras vez con diferentes tecnologías:

- El objeto `XMLHttpRequest` de los navegadores y su uso se nombró como **AJAX** para que fuera más vendible
- Una página web avanzada y con más funcionalidades se empezó a llamar **Web App**
- Las técnicas relacionadas con aprovechar las nuevas características de los navegadores como el Service Worker, el archivo manifest se juntaron bajo un solo nombre más "vendible": **Progressive Web Apps**

Los ejemplos siguen y estoy seguro que en cada área del conocimiento suceden. Este "renombramiento" permite que la tecnología en cuestión sea más aceptada y difundida, aunque a veces puede llevar a un malentendido por parte del público en general que puede permear a los practicantes.

Esto es lo que ha pasado con los nombres que nos conciernen en este artículo, le llamamos _"Inteligencia Artificial"_ a toda una rama de las ciencias de la computación relacionada con imitar lo que entendemos como "inteligencia humana", pero las bases formales de esto podrían describirse con otros nombres más familiares para nosotros.

Este nombre permite que los avances sean aceptados y por lo menos el área de negocio entienda las capacidades de la tecnología, **no su funcionamiento**.

Cuando comprendas cómo funciona, tal vez veas que las redes neuronales no tienen nada que ver con las redes neuronales, o que en realidad el _aprendizaje automático_ es la aplicación de técnicas matemáticas y de ingeniería para aproximación de funciones, a veces muy complejas.

Ahora bien, eso no tiene nada de malo, sólo debemos aprender a no confundirnos con esos términos. Después de esta pequeña digresión, ahora si vayamos a lo que venimos: aprendamos aplicar estas técnicas.

## Perceptrones

Un **perceptrón** es un algoritmo que aproxima una función matemática sirve para **clasificar** su entrada entre **dos clases**. Un perceptrón puede tomar N entradas y devuelve un "Sí" o un "No".

Si eres un programador sin experiencia en ML, te puedes imaginar la función del perceptrón básicamente como un "IF". Es un clasificador binario que devuelve **Verdadero** si el objeto en cuestión pertenece al grupo seleccionado, **falso** en el caso contrario.

La diferencia está **en cómo se construye esta función**, nosotros no le damos reglas programadas al perceptrón para clasificar los objetos de cierta forma, sino que le damos ejemplos **etiquetados** y el perceptrón **aprende**: ajusta los parámetros de su función interna para dividir las dos clases lo mejor posible.

La fórmula básica para un perceptrón es una sumatoria de todos sus parámetros de entrada multiplicados por un factor llamado _peso_ para cada uno, más una constante llamada _sesgo_ o _bias_. Al resultado de esta suma se le aplica la **función de activación**, normalmente la función **step** que devuelve `0` (equivalente a falso) si la entrada es menor o igual que cero y `1` en cualquier otro caso.

Si llamamos `X` a los parámetros de entrada, `W` a los pesos aquí puedes ver la representación gráfica de un perceptrón:

![Representación gráfica de un perceptrón](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1616653024/Untitled_Artwork_2_fsqfcr.png){: .align-center}

Y aquí la ecuación matemática que lo representa:

![Ecuación de un perceptrón](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1616653048/Untitled_Artwork_3_fjoaaa.png){: .align-center}

### Entrenamiento

Como te podrás dar cuenta, el funcionamiento de un perceptrón es muy sencillo. Pero lo importante no es su funcionamiento cuando clasifica, _sino como aprende a clasificar_. Esta fase se llama **entrenamiento** o **training** y consiste en encontrar los pesos correctos para cada parámetro de entrada y el sesgo correcto.

El entrenamiento de un perceptrón toma un conjunto de ejemplos **clasificados** o **etiquetados** y encuentra los peso que pueden clasificar el mayor número de ejemplos correctamente. Este entrenamiento puede ser muy pesado dependiendo del número de entradas y ejemplos.

Es justo esto lo que hace que diferencia al machine learning de la programación tradicional. Tú programaste el algoritmo para encontrar los parámetros correctos, pero nunca las reglas específicas de clasificación.

## Redes Neuronales

Una red neuronal es un conjunto de perceptrones combinados para poder clasificar en más de dos clases, y para crear funciones de clasificación que van mucho más allá de nuestro nivel de comprensión.

Las redes neuronales generalmente usan perceptrones con una función de activación diferente, la función sigmoide que transforma cualquier entrada en un valor entre 0 y 1 (como una probabilidad).

En el siguiente artículo hablaremos más a detalle sobre eso.

## Las matemáticas necesarias

Para poder entender las **bases de funcionamiento** de todo lo que acabamos de mencionar, hay que saber trabajar con matemáticas de nivel universitario:

* Álgebra líneal
* Análisis o Cálculo Vectorial
* Ecuaciones diferenciales
* Probabilidad
* Estadística

Y, claro, todas las matemáticas que soportan estas: álgebra, trigonometría, geometría analítica, etc.

Si quieres aprender _profundamente_ esta área de la computación y estas técnicas y sientes que no tienes las bases matemáticas necesarias puedes estudiarlas aquí: [Khan Academy en Español](https://es.khanacademy.org/) (gratuito) o [Brilliant](https://brilliant.org/) (de pago).

Sin embargo, y espero no ser linchado por esto, para empezar a aplicar las técnicas de manera práctica **no las necesitas**. Puedes abrazar la parte pragmática y algorítmica y empezar a usar los paquetes y herramientas de ML.
