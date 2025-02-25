---
title: "¿Qué es una Knowledge Graph?"
date: 2024-11-23
author: Héctor Patricio
tags: knowledge-graphs neo4j graph-databases
comments: true
excerpt: "Hablemos de herramientas para representar el conocimiento y cómo implementar una: las Knowledge Graphs."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1440/v1732492633/steve-busch-L6WNhz2Mrvc-unsplash_d5x69k.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_440/v1732492633/steve-busch-L6WNhz2Mrvc-unsplash_d5x69k.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Muchas cosas en el mundo real se pueden representar como una serie de
relaciones entre diferentes entidades. Por ejemplo, una red social se puede
representar como un conjunto de personas y sus relaciones. En este post vamos
a usar esta misma idea para representar **la estructura del conocimiento**: 
cómo están relacionadas las diferentes ideas que podemos tener sobre
un tema.

Antes, profundicemos un poco en las herramientas teóricas que nos van a ayudar
a entender esto de manera más clara. Hablemos primero de cómo representar de
manera conveniente las relaciones entre diferentes entidades: los **grafos**.

## ¿Qués un grafo?

Un grafo es una estructura matemática que tiene dos tipos de elementos:

1. **Nodos**: Se usan para representar las entidades.
2. **Aristas**: Son las relaciones entre los nodos.

Estamos muy acostumbrados a usar grafos, normalmente con más elementos, pero
el concepto es el mismo. En un grafo lo más importante no son las características
de los nodos, sino las relaciones que existen entre ellos.

## ¿Qué es una Knowledge Graph?

Un Knowledge Graph o Grafo de Conocimiento es un grafo que representa la estructura
de la información que tenemos sobre un tema. Su función principal es ayudar a
encontrar conexiones entre conceptos y así poder entender mejor el tema.

Esto a algunos les puede parecer una idea rara, pero todas las búsquedas 
semánticas útiles, como las de Google usan un grafo de conocimiento por debajo
para entender mejor lo que estamos buscando.

## Implementando una Knowledge Graph

## ¿Por qué no usar una base de datos relacional?

### ¿Por qué no usar una base de datos documental?

## Conclusión
