---
title: "Entendiendo la cohesión y el acoplamiento en el software"
date: 2021-09-06
author: Héctor Patricio
tags: Cohesión acoplamiento software
comments: true
excerpt: "En este artículo intentamos establecer de manera sencilla qué son la cohesión, el acomplamiento y cómo afectan al diseño de tu software y el código"
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,e_oil_paint:30,w_1200/v1620272565/sam-loyd-qy27JnsH9sU-unsplash_ibulfd.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,e_oil_paint:30,w_300/v1620272565/sam-loyd-qy27JnsH9sU-unsplash_ibulfd.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Siempre se dice que una buena base de código tiena alta cohesión, pero bajo acoplamiento. ¿Cómo se puede entender esto? ¿Cómo podemos llevar este principio a la práctica? En este artículo vamos a definir cada uno de esos términos de manera sencilla, con ejemplos y cómo llegar a la aplicación real de estos términos.

## Cohesión

La **cohesión** de los módulos en el desarrollo de software se refiere al grado en el que sus componentes internos se relacionan entre sí. Es decir, un módulo tiene **alta cohesión** si todos sus componentes trabajan para un mismo objetivo y no para cosas dispares.

Este grado de cohesión permitirá que el componente utilice menos otros módulos externos.

Para lograr esto tu módulo debe enfocarse en hacer una sola cosa, en tratar con un aspecto específico de tu problema general. Pongamos un ejemplo:

Imagina que estás creando un chatbot, un programa que, usando las API's de los aplicaciones de comunicación te permite interactuar con tus usuarios en forma de chat. El sistema tiene como requerimiento que la lógica de conversación sea fácil de reemplazar y mantener.

## Acoplamiento


### Tipos de acoplamiento


## Cómo lograr alta cohesión y bajo acomplamiento


## Conclusiones