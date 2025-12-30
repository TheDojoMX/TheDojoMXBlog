---
title: "La regla del 'Cero, Uno o Infinito"
date: 2021-12-10
author: "Héctor Patricio"
tags: ['zero-one-infinity', 'design', 'reglas']
description: "A veces necesitamos reglas que nos ayuden a desarrollar mejor software. La regal de 'Cero, Uno o Infinito' es una guía para que creemos software más usable."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1120/v1639259189/michael-dziedzic-uZr0oWxrHYs-unsplash_koqk3a.jpg"
draft: false
---

La regla del 'Cero, Uno o Infinito' es una guía para diseñar software que sea más fácil de usar, tanto para otros desarrolladores como para los usuarios finales. La regla en inglés es:

> “Allow none of foo, one of foo, or any number of foo.” - Willem van der Poel

Esta regla establece que respecto a la existencia de elementos, deberías permitir que no exista ninguno, solamente uno o un número arbitrario (potencialmente infinito, mientras las limitantes ) de estos elementos. La idea **principal es que no existan límites arbitrarios impuestos por alguna idea sin explicación**.

Algunos ejemplos de esta regla, puesta en práctica:

- Una estructura de datos no limita arbitrariamente el grado de anidado que puede tener
- No existe un normalmente un límite impuesto de recursividad (más allá del dado por el tamaño del _stack_ de ejecución)
- En las bases de datos relacionales existen tres cardinalidades: 1-1 (permitir una), 1-N (un padre puede tener muchos hijos), N-N (varios artículos pueden pertenecer a la misma categoría y un artículo puede tener varias categorías)
- Los caracteres especiales básicos de las expresiones regulares son: `.` (un carácter cualquiera), `+` (uno o más caracteres), `*` (cualquier número de caracteres).

Y esta regla parece que también existe en la naturaleza:

- La procreación es ilimitada mientras los recursos sean suficientes (puedes tener N hijos)
- Tus ancestros directos son uno de cada género (tienes un padre y una madre)
- Tus ancestros indirectos pueden ser infinitos (tu linea genealógica y los hijos de tus hijos pueden ser infinitos)
- Cuando tienes un límite de uno y lo abres para dos, ¿entonces por qué no abrirlo para tres? Si aplicamos esta regla recursivamente llegamos infinito
- En un consejo de administración hay una (1) persona encargada con acceso a la información de un sistema o un equipo (N - infinito)
- Como conjunto, un vehículo puede transportar N pasajeros, luego limitado por el caso de negocio o modelo específico. Cuando esta lleno puede transportar cero personas más

Ahora veamos algunos ejemplos en los que puedes poner límites arbitrarios sin darte cuenta.

## Modelando bases da datos

En modelados de bases de datos. Imagínate que tienes que modelar una tipo de usuario en el que te dicen que tienes que guardar diez propiedades arbitrarias. Podrías cometer el error de crear específicamente diez campos para guardar estas propiedades, lo cuál crearía un límite arbitrario en la capacidad de guardar estas propiedades. La mejor forma de modelarlo sería con una relación 1-N, ya que te da la flexibilidad de aumentar o reducir este límite mediante lógica específica para el caso de uso.

Lo mismo podrías pensar en cuanto a asignación de categorías, tags, comentarios, etc.

## Modelando software

Veamos algunos ejemplos que te puedes encontrar creando software.

### CTRL-Z

Imagina que tienes que diseñar un editor de texto y estás pensando en agregar la funcionalidad de "deshacer". Primeramente piensas que es buena idea solamente permitir que se deshaga la acción inmediata anterior, así que lo implementas como una variable que se está sustituyendo constantemente.

Pero ahora quieres permitir que se deshagan más acciones. ¿Cuál sería tu siguiente límite? El límite natural tendría que ser "infinito" o "hasta el principio del tiempo", ya que cualquier otro límite sería arbitrario y difícil de comprender o justificar. Así que tu implementación cambia de una variable a una pila de acciones que va manteniendo tantas acciones como sea posible.

### Modelando una conversaciǿn

Ahora estamos creando un modelo para almacenar y correr una conversación de un chatbot con un usuario. Cada mensaje puede comportarse de tres maneras: darle la oportunidad al usuario de contestar con una respuesta fija, llevar a otro mensaje sin darle oportunidad al usuario de contestar, o terminar la conversación.

Como puedes observar, esto es un caso perfecto de la regla del 'Cero, Uno o Infinito'. Un mensaje puede tener cero mensajes siguientes, por lo que termina la conversación. Puede tener un solo mensaje siguiente, que es cuando continuamos sin esperar respuesta. O puede tener N mensajes siguientes, uno correspondiente a cada respuesta posible de parte del usuario. Imponer un número limitado de respuestas posibles dentro de tu sistema no una buen idea, ya que limita sin razón alguna la flexibilidad de nuestro sistema.


## Críticas a la regla del 'Cero, Uno o Infinito'

Una de las principales críticas a esta regla es que **está dejando fuera el dos**, que también es un número muy especial para ciertos casos: muchas cosas en la naturaleza vienen en pares. Los booleanos, prendido/apagado, arriba/abajo, izquierda/derecha.

En mi opinión es un número que también se debe considerar, pero solo en caso de que los dos elementos carguen un significado como en los ejemplos anteriores, normalmente son cosas opuestas que se relacionan con un centro, pero incluso, si no se considera un número especial, podemos modelar estos casos siguiendo la regla del 'Cero, Uno o Infinito': si tomamos como punto de referencia uno de estos valores, el otro es nuestro _"uno"_ que estamos permitiendo.

## Conclusión

Aprender principios de diseño de software te ayudará a crear mejores sistemas que puedan ser usados más fácilmente tanto por otros desarrolladores como por usuario. Espero que este pequeño ejemplo te lleve a aprender otros principios que puedas aplicar en tu trabajo diario. Déjanos un comentario si quieres que lo platiquemos más profundamente o con otros ejemplos.
