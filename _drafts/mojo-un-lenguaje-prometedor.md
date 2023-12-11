---
title: "Mojo 🔥: un lenguaje prometedor"
date: 2023-11-01
author: Héctor Patricio
tags: mojo python machine-learning
comments: true
excerpt: "El ecosistema de desarrollo está cambiando y se están diseñando nuevos lenguajes de programación y entornos de ejecución más adecuados para los problemas actuales. Hablemos de Mojo."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1702275251/shubham-dhage-cLhjmsyby3Q-unsplash_ucy8y3.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1702275251/shubham-dhage-cLhjmsyby3Q-unsplash_ucy8y3.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

[Chris Lattner](https://www.nondot.org/sabre/){:target="_blank"}, uno de los creadores de [LLVM](https://llvm.org) y [Swift](https://www.swift.org/), ha estado desarrollando un nuevo lenguaje basado en la sintaxis de **Python** pero pensado para atacar su punto más débil: **la velocidad de ejecución**.

Este lenguaje se llama [Mojo](https://modular.com/mojo), y está siendo publicitado como un lenguaje para hacer aplicaciones de **inteligencia artificial**.

En este artículo veremos sus guías de diseño, sus características y analizaremos si te conviene aprenderlo o no tanto.

## Características

Las pruebas iniciales de Mojo revelan que puede ser hasta 68,000 (sí, leíste bien **sesenta y ocho mil**) veces más rápido que Python en ciertas tareas, mientras que C++ sólmente llega a ser 5,000 veces más rápido. Claro, esto no habla muy bien de Python, pero debes pensar en que su objetivo no es ser un lenguaje de alto rendimiento, sino un lenguaje de alto nivel y fácil de usar, y aquí es donde entra Mojo.