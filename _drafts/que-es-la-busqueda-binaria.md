---
title: "¿Qué es la búsqueda binaria?"
date: 2023-11-01
author: Héctor Patricio
tags: algoritmos búsqueda
comments: true
excerpt: "Hablemos de un algoritmo sencillo que incluso utilizamos en la vida real pero que es
muy importante en el mundo de la computación."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1729489258/nastya-kvokka-Ifk3WssHNRw-unsplash_m2u7vh.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1729489258/nastya-kvokka-Ifk3WssHNRw-unsplash_m2u7vh.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Uno de los algoritmos más fáciles de entender, que incluso sin preparación
aplicamos en la vida real y que se enseña en las primeras clases de programación
es la **búsqueda binaria**. Vamos a hablar de este algoritmo y su relación
profunda con las ciencias de la computación y la información en general.

## Búsqueda binaria en la vida real

¿Alguna ves has jugado "Adivina Quién"? Es un juego de mesa en el que cada
jugador tiene un tablero con un conjunto de personajes con características
físicas distintas, como el color de pelo, diferentes accesorios, y otros rasgos
distintivos. Cada jugador escoge secretamente un personaje y el otro lo tiene que
adivinar, haciendo preguntas que le permitan ir eliminando a los personajes que
el otro jugador no ha elegido. ¿Cuál es la mejor estrategia para adivinar con la 
menor cantidad de preguntas? Podrías pensar que es por cosas muy distintivas, por
ejemplo, si hay dos personajes con sombrero, y preguntas si tiene sombrero,
puede parecer una buena estrategia, pero no lo es.

En este caso, suponiendo que tenemos 40 personajes y solo dos tienen sombrero y
suponiendo que tienes 40 personajes, sólo 5% de las veces te ayudará reducir
significativamente el número de personajes, por lo que la mayoría de las veces
será una pregunta extra si la haces inicialmente. Lo mejor es empezar por las
características que dividan el conjunto de personajes en dos grupos más o menos
iguales. Por ejemplo, si hay 40 personajes y 20 tienen el pelo largo y 20 el corto,
la pregunta si el personaje tiene el pelo largo, te dejará con 20 personajes.

El algoritmo de búsqueda binaria se aplica para encontrar un valor en una
colección _ordenada_ de elementos. Piénsalo en términos de la vida real. Si
tienes que adivinar un número del 1 al 100 con el menor número de intentos posible,
¿por dónde te conviene empezar?

La mejor forma es empezar desde la mitad, es decir desde el 50. De esta manera,
eliminas con una sola pregunta la mitad del espacio de búsqueda. Por ejemplo si
preguntas si es 50 y te dicen que no, que es mayor, ya no tienes que preocuparte
por los números del 1 al 50.