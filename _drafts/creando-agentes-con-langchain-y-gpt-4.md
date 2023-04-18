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

En este contexto, además de una cosa que puede actuar por sí mismo, se entiende que puede hacer dos cosas más:

- Decidir qué hacer y qué herramienta usar
- Aprender a usar herramientas automáticamente (si le proporcionas las cosas que necesita)

## Agentes en LangChain

LangChain provee de un conjunto de agentes prefabricados.