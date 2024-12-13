---
title: "Un concepto importante: los buffers"
date: 2024-12-08
author: Héctor Patricio
tags: software-development programming técnicas-de-programación buffer
comments: true
excerpt: "Los buffers son una herramienta poderosa que puedes usar para resolver problemas."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1733894437/philip-oroni-0Nh06vUjbLw-unsplash_q3mcrp.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1733894437/philip-oroni-0Nh06vUjbLw-unsplash_q3mcrp.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

El concepto de buffer es usado por todos lados en el desarrollo de software, sin embargo siento
que es un concepto poco entendido. En este artículo vamos a hablar de qué son, para qué se usan
y cómo pueden ayudarte a resolver problemas.

## ¿Qué es un buffer?

Primero hablemos de dónde viene la idea de los buffers. Un buffer es un concepto general en
los sistemas que sirve para guardar algo temporalmente, pero que sin falta llega a su
destino final normalmente a diferente velocidad o ritmo con el que se generó. No traduzco la
palabra, ya que no hay una traducción que capture de manera completa el concepto. Sin embargo,
en diferentes contextos, buffer se podría traducir como:

- Amortiguador
- Almacén temporal
- Regulador

Esta última palabra te puede empezar a sonar, ya que en el desarrollo de software usamos
los buffers para _regular_ el flujo de datos entre diferentes sistemas o componentes.

## Buffers en acción

Ahora veamos algunos ejemplos de este concepto que seguro conoces o has visto aplicados en
software. Recuerda que lo que estamos buscando entender es el concepto, por lo que vamos a
explicar cómo el ejemplo es un buffer, pero no vamos a entrar en detalles de la implementación.

### Escritura en archivos

Cuando escribimos en un archivo, los sistemas operativos usan buffers para guardar los datos
en memoria antes de escribirlos en su destino final, ya que si escribiera directamente en el disco
byte por byte, será muy lento.

## ¿Cómo pueden ayudarte a diseñar mejor software?

## Conclusión

Los buffers son una herramienta poderosa que puedes usar para resolver problemas.
