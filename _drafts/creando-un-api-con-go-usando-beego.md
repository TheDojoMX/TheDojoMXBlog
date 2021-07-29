---
title: "Creando un API con GO: Usando Beego"
date: 2021-03-31
author: Héctor Patricio
tags:
comments: true
excerpt: "Hagamos una pequeña API en Go usando Beego, mientras intentamos seguir los principios de Domain Driven Design"
header:
  overlay_image: #image
  teaser: #image
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Vamos a probar el poder y la facilidad de Beego, un framework creado en China, en dónde las exigencias respecto a lo que deben soportar los sistemas en cuanto a concurrencia y escalabilidad son fuertes.

Para hacer la prueba vamos a crear un proyecto más o menos interesante: vamos a hacer un diccionario inverso. Tú das la descripción de la palabra, y la API nos devuelve una serie de opciones con un valor de certeza. Para lograr esto vamos a necesitar un modelo.
