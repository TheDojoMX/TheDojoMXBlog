---
title: "Formatos de marcado de texto que deberías aprender"
date: 2019-12-20
author: "Héctor Patricio"
tags: ['markdown', 'restructured-text', 'asciidoc', 'latex']
description: "A veces tienes que crear documentos de texto con un algún tipo de formato visual. Aprende lenguajes de marcado que te facilitarán la vida."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1576563210/raychan-QtHYdJsBRFU-unsplash_mpyus4.jpg"
draft: false
---

Parte del trabajo de un desarrollador es crear documentos con un formato fácil de entender y agradable a la vista, para crear documentación, registrar decisiones, escribir manuales, etc. La forma común de hacerlos es un procesador de textos como Word o Google Docs, pero generalmente batallamos sobre todo con el formateo y embellecimiento de documento.

En este artículo te platicaré de **tres alternativas** que pueden hacer tu vida más fácil: Markdown, reStructuredText, AsciiDoc.

Todos estos lenguajes pueden producir múltiples formatos de salida: HTML, PDF, Word, entre otros. Y lo mejor es que estas salidas son personalizables.

## Markdown

Es el formato de marcado de texto simple más conocido por ser el usado en muchos lados (GitHub, por ejemplo) para darle un poco de formato semántico al texto.

Puedes crear los estilos de texto más comunes directamente:

* **negritas**
* _cursivas_
* [enlaces](/)
* Imágenes:

![Imagen de ejemplo](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_100/v1559453194/luis-dille-1098834-unsplash_vndt6g.jpg)

También permite crear listas no numeradas, como la anterior, numeradas, tablas (con las sintaxis extendidas pero no con la definición original) y una serie de títulos de diferente jerarquía equivalentes a los headers de HTML (h1, h2... h6).

De hecho, esta entrada está escrita con Markdown. Markdown es tan popular que existen aplicaciones completamente dedicadas a él como [MacDown](http://bit.ly/2M7YmLL
), [Focused](http://bit.ly/38Zhohc) y [Typora](http://bit.ly/2S4MX38). Además, diferentes empresas han creado sus propios dialectos o adaptaciones para que sea más fácil de usar en su caso específico.

Si aún no lo sabes usar, vale la pena que le eches un ojo: [Guía de Markdown en español](http://bit.ly/38S2l8G). Tardarás unos minutos en aprender lo básico que es muy útil para el 80% de los casos en los que lo ocuparas.

Markdown es muy bueno para crear documentos individuales pero, ¿qué pasa si el texto que quieres escribir es más extenso? Tal vez el texto está compuesto por muchas partes, como un libro o una documentación extensa. Hay quienes dicen que [no deberías usar Markdown para crear tu documentación](http://bit.ly/2sOpmJg).

Las siguientes herramientas están mejor que preparadas que Markdown para eso, permiten crear cuerpos de textos más extensos.

## reStructuredText

Este formato de texto es adecuado para crear cuerpos de texto más complejos que con Markdown. Tienes las mismas capacidades de formateo de texto que con Markdown: negritas, cursivas, cabeceras, links, imágenes, listas, tablas, etc.

Pero reStructuredText provee **más opciones** para formatear el texto, ya que fue creado para hacer _documentos técnicos_ además de documentos de carácter general.

**reStructuredText** parece ser parte de [docutils](http://bit.ly/2ECmEt2) originalmente, creado como una revisión de se [StructuredText](http://bit.ly/35NkdQk) y [Setext](http://bit.ly/2PIAdgT).

Sus herramientas te permitirán crear texto marcado con **mejor semántica** que Markdown, más estandarizado (RST no tiene 'sabores' o dialectos) y con herramientas adaptadas a la documentación de código. Entre otras cosas RST provee:

- Más formatos de listas:
  - Listas de definición
  - Listas de parámetros
  - Numeración de listas arbitrariamente
- Bloques de texto pre-formateado (para código)
- Bloques de documentación de pruebas
- Citas
- Notas a pie de página
- **Directivas**, una manera de extender el lenguaje con construcciones propias
- Hyperlinks con diferentes destinos: externos, internos, etc.

Esta última característica permite crear documentos interconectados que son muy útiles para textos amplios.

RST es el formato default de [Sphinx](http://bit.ly/35Jb6QP) una herramienta de documentación de código creada en Python que te puede ayudar a crear documentación muy bonita.

Aquí hay una introducción a RST en inglés: [A reStructuredText Primer](http://bit.ly/2rdQn8y).

## AsciiDoc

> Incluso el software más brillante es inútil sin buena documentación. - Documentación de AsciiDoc

**AsciiDoc** fue creado para hacer **tan fácil como escribir un email** la escritura de cualquier tipo de documento, sea este un artículo, un texto en prosa, un libro o documentación técnica.

El creador asegura que una de las causas de que se nos haga tan difícil escribir está relacionada con que los editores de texto nos distraen con cosas como el formateo o paja que no es necesaria. AsciiDoc se enfoca en que puedas escribir sin preocuparte por el formato, dando una sintaxis natural, fluída y que no estorba, mientras te permite preparar el texto para crear formatos de salida hermosos.

> Usa AsciiDoc para marcado de documentos. De verdad. En verdad es legible, fácil de procesar y mucho más flexible que XML. - Linus Torvalds

Al igual que Markdown y RST, AsciiDoc provee de medios básicos para dar formato al texto. Pero AsciiDoc es el que más herramientas de los tres platicados aquí tiene. Además de ofrecet todo lo de las dos herrmientas anteriores tiene:


- Más formatos de párrafo: párrafos de introducción y pre-formateados fáciles.
- Secciones prediseñadas: cuadros de aviso, de notas, etc.
- Estilos de lista parecidos a los de RST.
- Formateo y sintaxis de código con notas, como la siguiente:
![Ejemplo de notas](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_700/v1576905208/Screenshot_2019-12-20_23.12.38_mdhrfj.png)
- Barras laterales
- Macros
- Generación de tablas desde CSV
- Videos
- Muchas muchas cosas más...

Sin duda AsciiDoc es el más completo de los formatos que hemos visto en este artículo. Aquí hay una [introducción en inglés](http://bit.ly/2PKzdZN) y aquí un [libro en español](http://bit.ly/2rgL3Bt). AsciiDoc es tan completo que varios autores de libros lo han escogido para crear sus escritos.


## ¿Cuál uso, entonces?

Mi conclusión personal es la siguiente:

1. Si tienes que hacer un documento pequeño, sin mucho formato y en el que la velocidad de entrega es lo más importante usa Markdown, ya que su popularidad te permitirá entregar el documento en el menor tiempo posible. Por ejemplo, en GitHub subes un archivo "*.md" y automáticamente lo muestra formateado.

2. ¿Tienes que hacer documentación de código que posiblemente deba ir en línea o al lado del código? reStructuredText está especializado en eso y con sus herramientas y entonrno te facilitará la vida.

3. Para todo lo demás, usa **AsciiDoc**. Una vez que lo sabes usar y combinado con AsciiDoctor (su procesador) y [Pandoc](http://bit.ly/2Q2zbeE) (un transformador de formatos) puedes crear cosas muy complejas muy rápidamente.

## Conclusión

Si eres como los programadores clásicos, odias usar Word, Docs o lo que sea por el problema que es formatear mientras escribes y amas la simplicidad del texto plano ayudado con herramientas que te permiten crear mejores cosas.

Estos lenguajes de marcado de texto te dan lo mejor de los dos mundos. Requieren un poco más de trabajo para empezar que los editores *"lo que ves es lo que obtienes"*, pero la productividad que te dan después paga con creces.

¿Qué opinas? ¿Vale la pena aprenderlos?