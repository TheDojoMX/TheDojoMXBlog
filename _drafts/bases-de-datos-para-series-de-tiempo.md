---
title: "Bases de datos para series de tiempo"
date: 2024-12-07
author: Héctor Patricio
tags: series-de-tiempo bases-de-datos bd data-science
comments: true
excerpt: "¿Qué bases de datos puedes usar para guardar datos generados de manera periódica? Hablemos de por qué es importante escoger la herramienta correcta."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1736399971/veri-ivanova-p3Pj7jOYvnM-unsplash_cf1uue.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_450/v1736399971/veri-ivanova-p3Pj7jOYvnM-unsplash_cf1uue.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

La series de tiempo tienen características especiales. Normalmente, los puntos de datos
consisten un par de valores: un identificador (el momento en el que sucedió) y un valor
(el valor que se observó).

Estas características hacen que trabajar con ellas sea diferente, porque además
se producen muchos de estos puntos de datos. Hablemos de cómo nos conviene almacenarlos.
Además, veremos que tienen de especial las bases de datos para series de tiempo.

## ¿Por qué no usar una base de datos relacional?

Una base de datos relacional pensada en transacciones (OLTP) es muy flexible y sin duda
puedes almacenar pares de valores de tiempo y el valor medido sin ninguna dificultad.

El problema viene cuando quieres hacer consultas sobre grandes cantidades de datos.

## ¿Qué hace una base de datos de series de tiempo?

Las bases de datos de series de tiempo:

## Ejemplos de bases de datos para series temporales

## Conclusión

La conclusión es sencilla: usa la herramienta adecuada para los datos que tienes que
almacenar y procesar. Por algo existen herramientas especializadas en tipos de datos
específicos. Personas con más experiencia se han dado cuenta de la necesidad de
crear especializaciones en este tipo de datos.
