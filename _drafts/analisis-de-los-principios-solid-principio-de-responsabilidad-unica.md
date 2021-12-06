---
title: "Análisis de los principios SOLID: Principio de Responsabilidad Única"
date: 2021-07-30
author: Héctor Patricio
tags:
categories:
comments: true
excerpt: "Escribe aquí un buen resumen de tu artículo"
header:
  overlay_image: #image
  teaser: #image
  overlay_filter: rgba(0, 0, 0, 0.5)
---

En esta serie de artículos vamos a hablar sobre los cinco principios SOLID, debido a que son algo que se dice que todo programador que quiera crear código mantenible y "limpio" debe saber y usar. La estructura de los artículos llevará la siguiente forma:

- Explicación del principio
- Ejemplos de código
- Contraejemplos (si existen)
- Críticas y alternativas

Esta serie de artículos surge debido a que aunque son poco entendidos por la mayoría de los programadores, estos principios se toman como _verdades universales_ que hay que seguir. Si queremos desarrollar buen software, no podemos ir por allí solamente aceptando lo que _la mayoría_ dice que está bien sin entenderlo a fondo y cuestionarlo.

Empecemos diseccionando el primer principio de los aclamados SOLID: el principio de Responsabilidad Única.

## El principio de Responsabilidad Única

Este principio se puede enunciar como:

"Una clase debe tener una única razón para ser modificada"
