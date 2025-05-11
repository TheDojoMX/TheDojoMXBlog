---
title: "Bases de datos para LLM's"
date: 2025-05-10
author: Héctor Patricio
tags: llms bases-de-datos vectores grafos embeddings
comments: true
excerpt: "Los LLM's nos permiten crear softeware que no creíamos posible hasta hacer poco. Pero necesitan que les demos información de manera especial. ¿Qué tipo de bases datos se requieren para crear proyectos útiles? En este artículo lo veremos."
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
ellos como fuentes de información exactas. ¿En qué tipos de bases de
datos podemos guardar información para crear programas en combinación con
los modelos generativos que sirvan lo mejor posible?

En este artículo vamos a hablar de eso, pero empecemos entendiendo por qué
se necesitan bases de datos con capacidades especiales.

## ¿Por qué se necesitan bases de datos con capacidades especiales?

Pensemos en algunos de los casos que los LLMs pueden ser útiles para resolver:

- **Chatbots** más sofisticados que los basados en reglas, con mayor capacidad de respuesta y flexibilidad en
en el tipo de respuestas que puede dar.
- Sistemas de **creación de contenido** en general, que nos dan mejores ideas
o resultados finales de alta calidad.
- **Agentes autónomos** más inteligentes que pueden tomar decisiones y realizar
tareas más complejas.
- **Asistentes personales** que analizan el contexto, juntan información y la
usan para poder darnos ayuda en diferentes áreas.

Para que un LLM sea realmente útil en cualquiera de estos contextos
necesitamos que tenga acceso a información **actualizada** y **relevante**.
Para hacer un chatbot que pueda responder preguntas sobre cualquier tema
no podemos confiar en lo que el modelo tiene codificado en sus parámetros, primero
porque puede estar desactualizado y segundo porque es propenso a cometer errores,
lo que se conoce como _alucinaciones_. Ni los modelos más avanzados se
escapan de eso, y de hecho algunos investigadores piensan que mientras
más "capaz" sea el modelo, más propenso a cometer alucinaciones. En mi experiencia,
pasa exactamente eso, un LLM muy avanzado puede hacer invenciones cada vez más
convincentes, pero que siguen sin estar apegadas a la realidad.

### Lo que esperamos del software

Dependiendo del caso se requieren algunas características que se esperan del software
en general pero que los LLM's no son especialmente buenos para cumplir, por ejemplo:

1. **Velocidad**: Casi todos los programas que encaran al usuario final requieren responder lo
más rápido posible.
2. **Exactitud**: En la mayoría de los casos necesitamos que la información que nos proporciona
el LLM sea lo más exacta posible, muchas veces no necesitamos una precisión absoluta, pero por lo
menos esperamos que no sea completamente errónea la respuesta.
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

La técnica principal se llama en inglés _Retrieval Augmented Generation_ (**RAG**). Hablemos brevemente de ella.

## ¿Qué es RAG?

La técnica o arquitectura RAG consiste básicamente en usar una base de datos para almacenar
la información relevante que le vamos a inyectar al LLM dependiendo de la tarea que
tenga que realizar. La parte difícil está compuesta por dos etapas, que podemos resumir en dos preguntas:

1. ¿Cómo preparo la información para que el LLM pueda usarla?
2. ¿Cómo hago que cuando el LLM necesite información, pueda acceder a ella de manera rápida y eficiente?

No vamos a profundizar mucho en la implementación de RAG, pero uno de los puntos
más importantes para tener un sistema exitoso es la base de datos que usamos para
almacenar la información, que tiene que ver más con la segunda pregunta.

## Bases de datos para proyectos con LLM's

Hablemos de dos tipos diferentes de bases de datos que pueden ayudar a tu sistema a cumplir con
lo que se espera de un sistema de software, mientras aprovechamos las capacidades de los LLM's.

### Bases de datos vectoriales

Los modelos de lenguaje pueden generar texto, pero también pueden generar vectores. Estos vectores
representan el significado de los textos en un espacio vectorial. En inglés se les conoce como
_embeddings_ y en español casi no se usa la traducción pero les podemos llamar _incorporaciones_.

El punto es que al transformar el texto en un vector que representa _su significado_ podemos
hacer operaciones con los vectores para encontrar textos que sean similares o relacionados.
Y aunque esto lo podríamos programar manualmente, una programa especializado en eso nos sería
de mucha ayuda. Además, los vectores que te dan los modelos de lenguaje tienen una dimensión
muy grande, por lo que no es fácil de manejarlos con técnicas tradicionales.

Para que tu LLM tenga acceso a información relevante, una técnica transformar toda la información
que quieres que el LLM pueda usar en _embeddings_ y guardarlos en una base de datos vectorial.
Las bases de datos vectoriales pueden ayudarte a _traer_ (**R**etrieval) la información más
relevante cuando la necesites, de manera rápida y eficiente.

Aquí te presento algunos ejemplos de bases de datos vectoriales que puedes usar:

- **[Faiss](https://github.com/facebookresearch/faiss)**: No es propiamente una base de datos, sino una
biblioteca open-source creada por Facebook AI Research, muy eficiente en búsqueda
y clustering de vectores densos. Se usa comúnmente embebida en aplicaciones Python/C++ para
implementar búsquedas vectoriales locales. También puede ser usado para crear tu propia base
de datos vectorial.
- **[Milvus](https://milvus.io/)**: Es de código abierto, diseñada para escalabilidad horizontal
y manejo de miles de millones de vectores. Ofrece un servicio completo (con clustering, replicación) ideal
para APIs de búsqueda semántica. También tienen una versión gestionada llamada Zilliz Cloud.
- **[Pinecone](https://www.pinecone.io/)**: Plataforma SaaS especializada en vectores. Es una de las formas
más sencillas de empezar y ofrecen una capa gratuita para pequeños proyectos.
- **[ChromaDB](https://www.chromadb.dev/)**: Otro proyecto open-source, que ha evolucionado a no solamente
ser una base de datos de vectores sino también de documentos, con funciones como búsqueda de texto completo,
filtrado de metadatos y almacenamiento multi-modal. También es una de las formas más sencillas de empezar
porque puedes embeberla en tu proyecto de forma sencilla.
- **[Weaviate](https://weaviate.io/)**: Es un proyecto open source hecho en Go. Su enfoque es completamente
ser una base de datos pensada para servir a aplicaciones de inteligencia artificial, sobre todo a
aquellas basadas en texto. Te puede ayudar desde convertir tus documentos en vectores y almacenarlos,
hasta hacer búsquedas de diferentes tipos.
- **[Qdrant](https://qdrant.tech/)**: Otro motor open-source con características a los anteriores, desarrollado
en Rust, pero que ofrece características enterprise, tiene versiones gestionadas y parece que es
usado en proyectos grandes.
- **PostgreSQL** tiene la extensión PGVector para almacenar y comparar embeddings en columnas de una tabla, por
lo que si ya tienes una aplicación y no quieres agregar una nueva pieza de tecnología que mantener,
el viejo confiable PostgreSQL puede ser una buena opción.

### Bases de datos de grafos

Las bases de datos de grafos sirven muy bien para representar relaciones entre entidades.
Este tipo de representación es muy útil para modelar sistemas de información, y por lo tanto
para crear búsquedas semánticas y recomendaciones por similitud o temas relacionados.

Aunque este tipo de bases de datos tienen menos relevancia en los proyectos para LLM's,
te pueden ayudar para crear mejores sistemas que contesten mejor a las peticiones de los
usuarios y que abaraten el costo de las respuestas por el uso de tokens.

A los sistemas que usan una base de datos de grafos para enriquecer las respuestas les llaman
_GraphRAG_ (Graph-based Retrieval Augmented Generation). Aquí puedes usar las clásicas bases de datos
de grafos de toda la vida:

- **[Neo4j](https://neo4j.com/)**: Igual un desarrollo de código abierto, con versiones gestionadas y
enterprise. Si quieres irte por el camino fácil, esta es una de las mejores opciones, por su
confiabilidad y soporte.
- **[ArangoDB](https://www.arangodb.com/)**: Es una base datos híbrida, pensada tanto para grafos
como para vectores, promete cubrir los dos lados de los que hablamos en este artículo: la flexibilidad
de los vectores con la capacidad de grafos. No es open-source, pero tienen una versión de comunidad
para que puedas probarla.
- **[Dgraph](https://dgraph.io/)**: Es una base de datos de grafos open-source, recientemente adquirida
por una empresa llamada Hypermode, enfocada en desarrollo de software con LLM's. Promete procesar
terabytes de datos y responder en tiempo real.

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
