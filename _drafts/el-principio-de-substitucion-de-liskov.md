---
title: "El principio de sustitución de Liskov"
date: 2023-03-01
author: Héctor Patricio
tags: lsp liskov solid principios
comments: true
excerpt: "El principio de sustitución de Liskov es uno de las reglas de comportamiento más famosas entre los desarrolladores. Hablemos de lo que significa."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1677648049/brett-jordan-DDupbpu4MS4-unsplash_jdapyu.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1677648049/brett-jordan-DDupbpu4MS4-unsplash_jdapyu.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

El tercer principio enunciado en los principios **SOLID** es el principio de sustitución de Liskov. ¿Qué significa y más importante, vale la pena seguirlo? Pero antes de hablar del principio, hablemos de **Barbara Liskov**, la persona que lo inspiró y que estableció los conceptos principales.

## Un poco de historia: Barbara Liskov

Barbara Liskov es una matemática muy reconocida en la comunidad de la computación. Es conocida por su trabajo en la teoría de la computación y la lógica matemática. También es conocida por su trabajo en el diseño de lenguajes de programación y la teoría de tipos. En 1987, Liskov publicó un artículo en el que presentó el principio de sustitución de Liskov.

En su libro, ["Mentes Geniales. La vida y obra de 12 grandes informáticos"](https://www.marcombo.com/mentes-geniales-la-vida-y-obra-de-12-grandes-informaticos-9788426733573/), Camilo Chacón nos da una semblanza de las contribuciones de Barbara a las ciencias de la computación. Sus principales estudios estuvieron en la teoría de tipos y los tipos abstractos de datos.

## El principio de sustitución de Liskov

El espíritu de este principio está basado en las ideas sobre **subtipado** de Bárbara Liskov. Estas ideas tienen muy poco que ver en realidad con herencia en los lenguajes de programación orientados a objetos,
