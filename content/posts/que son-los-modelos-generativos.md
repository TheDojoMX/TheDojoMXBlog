---
title: "¿Qué son los modelos generativos?"
date: 2020-12-30
author: "Alejandro Santamaría"
tags: ['ai', 'ml', 'gans']
description: "En este artículo exploramos qué es un modelo generativo, cómo te pueden servir y el estado del arte en este campo."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1609313335/nathan-roser-XX0vmOvQ3GA-unsplash_iath8r.jpg"
draft: false
---

Los modelos generativos permiten a una máquina "aprender" los patrones que existen en los datos con los que son entrenadas y a partir de dicho aprendizaje, son capaces de **generar datos similares** que en algunos casos pueden ser casi tan "reales" como los que se utilizaron inicialmente para su entrenamiento.

Mediante este tipo de modelos pueden generarse nuevos datos que tienen distintas aplicaciones, entre ellas, generar datos que otros sistemas de aprendizaje podrán utilizar para su entrenamiento, sin necesidad de que dichos datos existan previamente.

En particular, las **Redes Neuronales Generativas Adversariales (GAN's)** pueden generar nuevas imágenes que se parecen o son similares a las imágenes con las que fueron entrenadas, pero que individualmente son distintas a todas ellas.

El funcionamiento de una Red Neuronal Adversarial consiste en la operación simultánea de dos redes neuronales que son "adversarias", una de dichas redes es la encargada de generar imágenes y la segunda es la encargada de discriminar aquellas imágenes que no se parecen a lo que constituye una imágen real.

Algunos modelos avanzados pueden verse en:

* [This Person Does Not Exist](https://thispersondoesnotexist.com/)
* [This Waifu Does Not Exist](https://www.thiswaifudoesnotexist.net/)
* [This Furson Does Not Exist](https://thisfursonadoesnotexist.com/)

Como parte de un proyecto de investigación, utilizamos una red adversarial para generar imágenes de zapatos, dichas redes utilizan, modelos convolucionales para ir entendiendo las imágenes en segmentos cada vez más pequeños hasta tener una definición y similitud suficiente para reemplazar la imagen original.

La calidad de los modelos generados se incrementa conforme el número de iteraciones va aumentando, en general, se van almacenando nuevas muestras de las imágenes generadas cada cierto número de iteraciones de tal forma se puede observar si el modelo sigue mejorando, si ya se estancó o si se está degradando, aunque existen algunas métricas que pueden ayudar a identificar el punto óptimo donde puede detenerse el entrenamiento.

Algunas de las peculiaridades de estos modelos es que son relativamente sensibles a la uniformidad y el número de imágenes utilizadas, sin embargo, también es cierto que los modelos han ido mejorando y en algunos casos pueden generar imágenes de gran calidad con menos datos de entrenamiento. Por ejemplo, estas imágenes fueron generadas con sólo 500 datos de entrenamiento mediante un Modelo Generador Adversarial Eficiente:

[Data Efficient GANs](https://github.com/mit-han-lab/data-efficient-gans)

## Usos de los generadores adversariales

Hablemos de algunos de los usos que pueden tener en la práctica este tipo de redes.

### Mejorar la seguridad

Un discriminador optimiza su capacidad para detectar imágenes que no son reales (las que emite el generador), de tal forma que dicho discriminador adquiere la capacidad de identificar imágenes que no son reales y que pueden estar siendo utilizadas para generar identidades falsas en sistemas que por ejemplo requieren fotografías.

### En el sector salud

La capacidad de detectar anomalías (trabajo del discriminador) puede utilizarse para identificar células o formaciones anómalas (como el cáncer) al ser entrenado mediante imágenes de tejidos u órganos saludables.

### En el sector de medios digitales

Ya que generadores adversariales pueden utilizarse para generar imágenes que no existían o generar imágenes a partir de un conjunto de imágenes preexistentes, dicha generación puede de igual forma generar modelos en tercera dimensión a partir de imágenes en dos dimensiones o hacer combinaciones de modelos preexistentes.

Esto puede usarse como material para la producción de contenido visual e incluso animaciones de video o bien como inspiración para que un diseñador genere nuevos personajes.

Algunos generadores pueden ayudar a corregir defectos en imágenes, removiendo o completando partes de la imágen que sobraban o que estaban faltantes, o si es el caso, a dar color a imágenes en blanco y negro.

De igual forma permiten crear una “interpolación” de imágenes para “regenerarlas” en una mayor resolución. Desde luego la eficacia dependerá de las imágenes utilizadas para su entrenamiento.

Algunas de estas aplicaciones pueden “traducir” las imágenes de un dominio a otro, por ejemplo, convirtiendo una imágen satelital en un mapa de niveles o generando fotografías a partir de bosquejos.

## Conclusión

Los modelos generativos pueden ser una gran herramienta para diferentes industrias, aprender a usarlos y generarlos te puede ayudar a entrar en un campo que tiene cada vez más alta demanda: el uso de datos para la creación automática de programas (Machine Learning).
