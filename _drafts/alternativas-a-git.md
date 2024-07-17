---
title: Alternativas a Git
date: 2024-04-30T00:00:00.000Z
author: Héctor Patricio
tags: git version-control fossil pijul
comments: true
excerpt: >-
  Git es una herramienta compleja, ya que no fue pensada desde el principio para
  tener buena experiencia de usuario, veamos algunas alternativas.
header:
  overlay_image: >-
    https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1450/v1714573988/osman-rana-yM3T1vYh8Oc-unsplash_gwkcc2.jpg
  teaser: >-
    https://res.cloudinary.com/hectorip/image/upload/c_scale,w_450/v1714573988/osman-rana-yM3T1vYh8Oc-unsplash_gwkcc2.jpg
  overlay_filter: 'rgba(0, 0, 0, 0.5)'
---

Git es una herramienta que se considera *obligatoria* para los desarrolladores
modernos por ser el programa usado para versionamiento de código usado por
la mayoría de los proyectos.

Pero no es ningún secreto que Git es una herramienta difícil de comprender y
que el 90% de los desarrolladores le dan **el uso más básico**, temiendo romper algo
y por eso tener que usar comandos más avanzados.

Hablemos de por qué es así y después veamos algunas alternativas interesantes.

## Los orígenes de Git

Al igual que otros sistemas de control de versiones, Git nació como soporte al
desarrollo de uno de los proyectos de software más importantes de todos los
tiempos: el kernel de Linux. Fue creado por **Linus Torvalds**.

Su objetivo no era ser una herramienta de uso masivo y fácil de usar, sino
trabajar sin las limitantes de las herramientas que existían en ese momento.
Y claramente, Linus lo creó a su manera. Algo interesante es que se llama
"Git" porque en inglés británico es una palabra despectiva que se usa para
llamar a alguien tonto o desagradable. Linus nombra sus proyectos como a sí
mismo, y como cualquiera lo podría llamar así a él, decidió ponerle ese nombre
a su sistema de manejo de versiones.

**Git** empezó a ser usado por la comunidad de Linux en 2005 y después por otros
proyectos Open Source, pero su éxito se disparó cuando en 2008 surgió GitHub
que facilitó su uso. Por ser una herramienta tan útil, ahora la tenemos como el
estándar en versionmiento de código.

Pero no es el único sistema de control de versiones moderno, hablemos de
dos alternativas.

## Fossil

Fossil fue creado por el autor de SQLite, [**Richard Hipp**](https://www.hwaci.com/drh/), y al igual que Git,nació
para soportar a este proyecto de software libre, el principal de su Hipp.

Al buscar un sistema de control de versiones moderno, Richard no encontró nada que lo convenciera
al cien por ciento, por lo que decidió crear Fossil, con las siguientes características:

1. **Integración de Wiki y Tickets**: Fossil tiene incluye estas herramientas a las que Hipp y
su equipo estaban acostumbrados.
2. **Foro y chat**: Fossil está pensado para también ser el centro de conversación del proyecto.
3. **Autosync**: permite que los cambios se sincronicen automáticamente sin tener que andar haciendo
magia con las ramas y los commits.

Personalmente, me gusta mucho la idea de tener todo integrado en un mismo
sistema, y pienso que el que sistemas como Jira y Confluence se integren directamente
con GitHub, Bitbucket y cosas similares, es una señal de que esta integración
es un muy buena idea que ayuda a que el proceso de software sea más fluido.

Puedes encontrar más información en [fossil-scm.org](https://fossil-scm.org/),
para instalarlo por tu cuenta. Pero también existe una versión hosteada en la
que de manera gratuita podrás tener el servicio de Fossil, equivalente a
GitHub: [Chisel](https://chiselapp.com/).

## Pijul

Pijul es un sistema de control de versiones basado en la troría de parches (patch theory)
y que está pensado para ser matemáticamente correcto. Además, a diferencia de Git, sí
está pensado para ser lo más fácil de usar sin cometer errores catastróficos.

Puedes encontrarlo en [pijul.org](https://pijul.org/), te recomiendo que si quieres probar algo fundamentalmente diferente a Git, pero con las mismas funciones externas, le des una oportunidad.

## Conclusión

No vamos a reemplazar a Git en el corto plazo y probablmente nunca lo hagamos
por lo extendido que está su uso (piensa en el efecto Lindsey), pero es bueno
saber que existen alternativas. Estas herramientas
nos enseñan cosas interesantes sobre el desarrollo de software, por ejemplo, que casi
siempre hay más de una forma de lograr lo que queremos.
ojalá que en el futuro, Git tome algunas de las ideas de estos proyectos y
