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

LangChain provee varios tipos de componentes, muchos de los cuáles son abstracciones de los conceptos más usados en la interacción con LLM's.