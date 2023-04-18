---
title: "Creando agentes con LangChain y GPT-4"
date: 2023-04-17
author: Héctor Patricio
tags: langchain gpt4 agentes
comments: true
excerpt: "Ya vimos como empezar a usar LangChain, avancemos a algo más interesante: crear agentes que puedan interactuar con el exterior."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,q_54,w_1200/v1681776700/DALL_E_2023-04-14_23.49.15_-_a_parrot_in_a_cybernetic_setting_plotting_a_great_plan_to_conquer_the_universe_digital_art_digital_illustration_detailed_cinematic_lightning_pkrwml.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,q_54,w_1200/v1681776700/DALL_E_2023-04-14_23.49.15_-_a_parrot_in_a_cybernetic_setting_plotting_a_great_plan_to_conquer_the_universe_digital_art_digital_illustration_detailed_cinematic_lightning_pkrwml.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

En este pequeño tutorial vamos a hablar de cómo puedes crear agentes que interactúen con el mundo exterior, usando LangChain y como modelo de lenguaje GPT-4. Como siempre, la mejor manera de aprender es haciendo algo, por lo que vamos a crear un agente

### ¿Qué es un agente?

En este contexto, además de una cosa que puede actuar por sí mismo, se entiende que un agente puede hacer dos cosas más:

- Decidir qué hacer y qué herramienta usar
- Aprender a usar herramientas automáticamente (si le proporcionas las cosas que necesita)

Los agentes tradicionalmente se entienden como programas que trabajan de manera autónoma y con su propio espacio de memoria, con los que te comunicas por medio de mensajes, pero que no tienes el control completo sobre ellos. Un agente puede decidir qué hacer con tu mensaje.

Combinando ambos contextos, un agente es un pedazo del programa que actúa autónomamente, que decide cómo lograr lo que has pedido y que aprende a hacerlo por su cuenta. Al estar basado en un LLM, no está garantizado su éxito.
## Agentes en LangChain

LangChain provee de un conjunto de agentes prefabricados.