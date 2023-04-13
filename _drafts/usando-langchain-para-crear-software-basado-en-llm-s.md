---
title: "Usando LangChain 🦜 para crear software basado en LLM's"
date: 2023-04-07
author: Héctor Patricio
tags:
comments: true
excerpt: "Escribe aquí un buen resumen de tu artículo"
header:
  overlay_image: #image
  teaser: #image
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Los grandes modelos de lenguaje o LLM's (Large Language Models) han sido noticia en este 2023. Es por eso que han surgido muchos proyectos y herramientas que permiten crear software basado en estas herramientas.

En este artículo vamos a poner un pequeño tutorial de una herramienta creada para hacer aplicaciones basadas en LLM's: [LangChain](https://python.langchain.com/en/latest/index.html).

## ¿Qué es LangChain?

Las aplicaciones basadas en procesamiento de lenguaje natural, sea como una herramienta de comunicación o como su producto principal, normalmente requieren fuentes de información para potenciar sus capacidades.

También es una muy buena idea que estas aplicaciones puedan actuar por sí mismas usando las instrucciones creadas por un LLM. Para hacer esto puede crear **agentes**.

**LangChain** provee componentes que te permiten lograr estas dos tareas, para que tú los uses como quieras, pero también te provee
de cadenas de componentes (_[composición](/) de software, ¿te suena?_) con casos de uso comunes, digamos que prefabricados para hacer software basado en LLM's de manera más rápida.

## Componentes principales

LangChain provee varios tipos de componentes, muchos de los cuales son abstracciones de los conceptos más usados en la interacción con LLM's, veamos algunos de ellos:

- **Texto**. La abstracción más básica es la que representa un texto cualquiera que le mandamos a un LLM.

- **Divisores de texto**. Generalmente, un modelo de lenguaje no puede consumir mucho texto al mismo tiempo, por lo que para poder procesar textos grandes hay que mandarlos por partes. Este componente se encarga de ayudarte a dividir el texto en partes que el LLM pueda procesar.

- **Índices**. Es una abstracción que presenta el texto de mejor manera para que un LLM pueda acceder a la información mejor.

- **Modelo**. Esto es la interfaz con un modelo de lenguaje. Te lo puedes imaginar como el equivalente a un conector a base de datos, abstraen los detalles de la conexión y te dan una interfaz común.

- **Agente**. Un agente puede recibir instrucciones en forma de alguna abstracción de texto, para ejecutar acciones en _sistemas externos_ o consultando para consultar al LLM.

- **Cadena**. Las cadenas son conjuntos de componentes que sirven para resolver problemas comunes o crear aplicaciones completas.

## Creando una aplicación de ejemplo

Vamos a crear una aplicación que nos permita consultar todos los posts de este blog y contestar preguntas. Por suerte, existe una cadena que ya nos permite hacer esto.
