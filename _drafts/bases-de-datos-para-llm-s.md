---
title: "Bases de datos para LLM's"
date: 2025-03-07
author: Héctor Patricio
tags: llms bases-de-datos
comments: true
excerpt: "¿Qué tipo de datos se requieren para crear proyectos útiles usando LLM's?"
header:
  overlay_image: 
  teaser: 
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Los LLM's llegaron para cambiar la forma en la que usamos la computadora.
Pero sus limitaciones y casos de uso que nos abren, requieren que los
utilicemos en conjunto con otras tecnologías y nuevas arquitecturas, para
hacer software confiable, útil y que cumpla con lo que el usuario necesita.

Una parte importante es la fuente de información, ¿en qué tipos de bases de
datos podemos guardar información para crear programas en combinación con
los modelos generativos que sirvan lo mejor posible?

En este artículo vamos a hablar de eso, pero empecemos entendiendo por qué
se necesitan bases de datos con capacidades diferentes.

## ¿Por qué se necesitan bases de datos con capacidades especiales?

Pensemos en algunos de los casos que los LLMs pueden ser útiles para resolver:

- Chatbots más sofisticados que los basados en reglas, con mayor flexibilidad
- Sistemas de creación de contenido en general
- Agentes autónomos más inteligentes
- Asistentes personales que analizan el contexto

Para que un LLM sea realmente útil en cualquiera de estos contextos
necesitamos que tenga acceso a información actualizada y relevante, por ejemplo,
para hacer un chatbot que pueda responder preguntas sobre cualquier tema
no podemos confiar en lo que el modelo tiene codificado en sus parámetros, primero
porque puede estar desactualizado y segundo porque es propenso a errores,
lo que se conoce como _alucinación_.

Dependiendo del caso se requieren algunas características que se esperan del software
en general pero que los LLM's no son especialmente buenos para cumplir, por ejemplo:

1. **Velocidad**: Casi todos los programas que encaran al usuario final requieren responder lo
más rápido posible.
2. **Exactitud**:
3. **Frescura en la información**:
4. **Capacidad de atender a muchos usuarios**:

## Bases de datos para proyectos con LLM's

Debido a las características que requerimos del software y las cosas que los LLM's
nos quitan "naturalmente", debemos complementarlos con otras tecnologías que nos
ayuden a tener un sistema que cumpla con las expectativas.

### Bases de datos vectoriales

### Bases de datos de grafos

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
