---
title: "Un concepto importante: los buffers"
date: 2024-12-30
author: Héctor Patricio
tags: software-development programming técnicas-de-programación buffer
comments: true
excerpt: "Los buffers son una herramienta poderosa que puedes usar para resolver problemas. Hablemos de algunos ejemplos y cómo te pueden ayudar a diseñar mejor software."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1733894437/philip-oroni-0Nh06vUjbLw-unsplash_q3mcrp.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1733894437/philip-oroni-0Nh06vUjbLw-unsplash_q3mcrp.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

El concepto de buffer es usado por todos lados en el desarrollo de software, pero siento
que es un concepto poco entendido. En este artículo vamos a hablar de qué son los buffers,
para qué se usan y cómo pueden ayudarte a resolver problemas y diseñar mejor software.

## ¿Qué es un buffer?

Primero hablemos de dónde viene la idea de los buffers. Un buffer es un concepto importante en
teoría de sistemas. Los buffers se utilizan para almacenar temporalmente datos, asegurando que
eventualmente lleguen a su destino final. Esto ocurre a una velocidad o ritmo diferente al
que fueron generados originalmente.

Traducir la palabra _"buffer"_ es difícil, porque no hay un concepto en español que abarque
todos los usos que se le dan en el desarrollo de software.Algunos ejemplos de uso de buffers en el desarrollo de software son:

- Amortiguador
- Almacén temporal
- Memoria intermedia
- Regulador

Esta última palabra te puede empezar a sonar, ya que en el desarrollo de software usamos
los buffers para _regular_ el flujo de datos entre diferentes sistemas o componentes.
Los buffers causan retrasos intencionales en el flujo de datos.

Empecemos a hablar de cómo se usan en el desarrollo de software.

## Buffers en acción

Estos son algunos ejemplos de este concepto que seguro conoces o has visto aplicados en
software. Recuerda que lo que estamos buscando entender es el concepto, por lo que vamos a
explicar cómo el ejemplo es un buffer, pero no vamos a entrar en detalles de la implementación.

### Escritura en archivos

Cuando escribimos en un archivo, los sistemas operativos usan buffers para guardar los datos
en memoria antes de escribirlos en su destino final, ya que si escribiera directamente en el disco
byte por byte, sería muy lento. Además, escribir directamente en el disco por cada byte que un
programa mande a escribir causaría problemas de estabilidad y rendimiento. Aquí no tenemos que
explicar mucho por qué un buffer, ya que es el ejemplo más común. Incluso en varios lenguajes
de programación los objetos que se usan para escribir en los archivos tienen "Buffer" o "Buffered"
en su nombre.

### Uso de servicios remotos

Usar un servicio o una función a través de la red (un servicio remoto) es costoso en tiempo
y recursos en comparación con cualquier cálculo local que se haga. Por eso es buena idea
usar buffers para guardar información antes de hacer una llamada a un servicio remoto.
Por ejemplo, en desarrollo web, cuando se hace un auto-completado o búsqueda mientras se sigue
escribiendo, el programa espera a que el campo tenga un número de caracteres para hacer
una llamada al servicio de búsqueda que pueda tener sentido.

### Caching

Este ejemplo no podía faltar. El caché es un tipo de buffer que guarda información _temporalmente_
con varios objetivos:

1. Ahorrar cómputo
2. Acelerar el acceso a la información
3. Evitar la sobrecarga de los recursos

Como sabemos, lo más difícil del cachee es decidir primero qué guardar y luego cómo
refrescarlo para que se no sea obsoleto.

### Buffering de contenido multimedia

Debido a que el contenido multimedia es muy pesado, un buen reproductor o sistema de streaming
casi siempre incluye un buffer que va descargando el contenido a mayo velocidad y un poco
adelantado para tener un reproducción fluida. Si no lo incluimos, estamos a merced de la velocidad
y las intermitencias de la red.

## ¿Cómo pueden ayudarte a diseñar mejor software?

Escribir software usando buffers es más complejo que hacerlo sin ellos, ya que son una pieza más
que puede causar problemas y que en algún momento vas a tener que depurar. Pero los buffers complican
el código y las pruebas de software, son indispensables para el buen rendimiento y la estabilidad de los
sistemas. Incluso algunos lenguajes de programación como Java, tienen buffers incorporados en su
librería estándar.

Recuerda, usar buffers te va a ayudar a escribir software:

- Más estable
- Con mejor rendimiento
- Más resiliente
- Más eficiente

Así que te conviene buscar oportunidades para usarlos lo mejor posible.

## Conclusión

Los buffers son interesantes. Son una herramienta poderosa que puedes usar para resolver
problemas con mejor calidad y que te permiten crear características arquitectónicas
deseables, a costa de hacer el código un poco más complejo. Sin embargo, si los ocultas
correctamente detrás de interfaces efectivas, los documentas bien y los pruebas,
te ayudarán mucho.
