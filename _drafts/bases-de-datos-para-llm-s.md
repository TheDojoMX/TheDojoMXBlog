---
title: "Bases de datos para LLM's"
date: 2025-03-07
author: Héctor Patricio
tags: llms bases-de-datos
comments: true
excerpt: "¿Qué tipo de datos se requieren para crear proyectos útiles usando LLM's? En este artículo lo veremos."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1742691554/chen-zy-ccr9dAWi0hw-unsplash_omykun.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1742691554/chen-zy-ccr9dAWi0hw-unsplash_omykun.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Los LLM's llegaron para cambiar la forma en la que usamos la computadora.
Pero sus limitaciones y casos de uso que nos abren, requieren que los
utilicemos en conjunto con otras tecnologías y nuevas arquitecturas, para
hacer software confiable, útil y que cumpla con lo que el usuario necesita.

Una parte importante es la fuente de información, ya que no podemos confiar en
ellos como fuentes de información confiable. ¿En qué tipos de bases de
datos podemos guardar información para crear programas en combinación con
los modelos generativos que sirvan lo mejor posible?

En este artículo vamos a hablar de eso, pero empecemos entendiendo por qué
se necesitan bases de datos con capacidades diferentes.

## ¿Por qué se necesitan bases de datos con capacidades especiales?

Pensemos en algunos de los casos que los LLMs pueden ser útiles para resolver:

- **Chatbots** más sofisticados que los basados en reglas, con mayor flexibilidad
- Sistemas de **creación de contenido** en general
- **Agentes autónomos** más inteligentes
- **Asistentes personales** que analizan el contexto y lo usan para tomar decisiones

Para que un LLM sea realmente útil en cualquiera de estos contextos
necesitamos que tenga acceso a información actualizada y relevante.
Para hacer un chatbot que pueda responder preguntas sobre cualquier tema
no podemos confiar en lo que el modelo tiene codificado en sus parámetros, primero
porque puede estar desactualizado y segundo porque es propenso a errores,
lo que se conoce como _alucinaciones_. Ni los modelos más avanzados se
escapan de eso, y de hecho algunos investigadores piensan que mientras
más "capaz" sea el modelo, más propenso a cometer alucinaciones.

Dependiendo del caso se requieren algunas características que se esperan del software
en general pero que los LLM's no son especialmente buenos para cumplir, por ejemplo:

1. **Velocidad**: Casi todos los programas que encaran al usuario final requieren responder lo
más rápido posible.
2. **Exactitud**: En la mayoría de los casos necesitamos que la información que nos proporciona
el LLM sea lo más exacta posible, muchas veces no necesitamos una precisión absoluta, pero por lo
menos que no sea errónea la respuesta.
3. **Frescura en la información**: La información que usamos en el día a día cambia y si tenemos
un sistema que la usa, debe tener acceso a lo más actualizado.
4. **Capacidad de atender a muchos usuarios**: A veces el mismo sistema debe poder atender
a muchos usuarios. Esto nos enfrenta con dos problemas principalmente: la capacidad de cómputo
requerida para manejar todas las peticiones y el costo de correr los modelos.

Es por eso que los proyectos basados en LLM's utilizan técnicas para lograr dos cosas principalmente:

1. **Darle información correcta, actualizada y sucinta al LLM**: Esto ataca los problemas de velocidad,
exactitud y frescura de la información.
2. **Reducir la cantidad de tokens que consume el LLM**: Esto también nos puede ayudar con casi
todos los puntos de arriba, pero principalmente con el costo.

La técnica principal se llama _RAG_ (Retrieval Augmented Generation). Hablemos brevemente de ella.

## ¿Qué es RAG?

La técnica o arquitectura RAG consiste básicamente en usar una base de datos para almacenar
la información relevante que le vamos a inyectar al LLM dependiendo de la tarea que
tenga que realizar.

## Bases de datos para proyectos con LLM's

Debido a las características que requerimos del software y las cosas que los LLM's
nos quitan "naturalmente", debemos complementarlos con otras tecnologías que nos
ayuden a tener un sistema que cumpla con las expectativas.

### Bases de datos vectoriales

Los modelos de lenguaje pueden generar texto, pero también pueden generar vectores. Estos vectores
representan el significado de los textos en un espacio vectorial. En inglés se les conoce como
_embeddings_ y en español casi no se usa la traducción pero les podemos llamar _incorporaciones_.

El punto es que al transformar el texto en un vector que representa su significado podemos
hacer operaciones con los vectores para encontrar textos que sean similares o relacionados.
Y aunque esto lo podríamos programar manualmente, una programa especializado en eso nos sería
de mucha ayuda.

### Bases de datos de grafos

Las bases de datos de grafos sirven muy bien para representar principalmente
relaciones entre entidades. Este tipo de representación es muy útil para modelar
sistemas de información, y por lo tanto para crear búsquedas semánticas y
recomendaciones por similitud.

Aunque este tipo de bases de datos tienen menos relevancia en los proyectos para LLM's,
te pueden ayudar para crear mejores sistemas que contesten mejor a las peticiones de los
usuarios y que abaraten el costo de las respuestas por el uso de tokens.

Específicamente, a los sistemas que usan una base de datos de grafos para enriquecer
las respuestas les llaman _GraphRAG_ (Graph-based Retrieval Augmented Generation).

## Conclusiones

Las bases de datos vectoriales y de grafos son herramientas poderosas que
te pueden ayudar a cumplir con las expectativas y necesidades de los proyectos
que son típicos de desarrollar con LLM's. Para usarlas correctamente hay que
comprender su funcionamiento lo suficiente, pero no es necesario que te
vayas a cada detalle.

Cuando estamos desarrollando software siempre aplica el dicho de usar la herramienta
correcta para el problema y este es un ejemplo claro de la aplicación de este principio.
Pero siempre hay que equilibrarlo con la simplicidad y recordando que cada pieza de
software o hardware que agreguemos al proyecto aumenta la complejidad y el costo
de correr y mantener el proyecto.
