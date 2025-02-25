---
title: "¿Qué son los requerimientos funcionales?"
date: 2024-11-23
author: Héctor Patricio
tags:  arquitectura 
comments: true
excerpt: "El análisis de requerimientos es una parte fundamental del desarrollo de software y es importantísima
para crear sistemas exitosos."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1731216878/isabelle-mannino-USOSteP8hOw-unsplash_cbxmst.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1731216878/isabelle-mannino-USOSteP8hOw-unsplash_cbxmst.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

**"Requerimientos funcionales"** es una expresión muy rebuscada para un concepto
muy sencillo relacionado con el diseño de los sistemas de software: **las
cosas que tu sistema HACE**.

En este artículo hablaremos de formas de encontrarlos, definirlos, documentarlos
y tenerlos listos para la siguiente etapa del desarrollo de software.

## Cómo definir las funciones de un sistemas

La primera tarea como arquitecto de software tiene que ver con la de
**entender completamente** lo que el software tiene que HACER. El software
normalmente tiene unas pocas funciones principales, pero muchas tareas
secundarias o terciarias que las soportan, y es por eso que descubrirlas
y describirlas todas no es una tarea sencilla.

## Cómo encontrarlos

La forma más eficiente de encontrar los requerimientos funcionales o funciones
que debe tener tu sistema es viviendo el proceso o problema que tu sistema va a
resolver. Es por esto que algunos de los mejores sistemas son creados por gente
que "se rasca su propia comezón" (_"scratch their own itch"_). Es decir, que
resuelven un problema que ellos mismos viven o han vivido, y que por eso
mismo **entienden a fondo**.

Una de las ventajas de atender un problema que tú vives, es que tienes
retroalimentación inmediata sobre si el sistema resuelve el problema o no.

Pero esto no siempre es posible, sobre todo cuando construyes software como
profesión, porque no siempre puedes dedicar tiempo y recursos suficientes para
tú realizar la operación de lo que quieres resolver, o simplemente no es práctico.
Así que la segunda mejor opción que tenemos es **platicar con los usuarios**.

Aquí es donde entran un montón de habilidades "blandas". Un mejor nombre para estas
habilidades es _"habilidades personales e interpersonales"_. O habilidades básicas
humanas. Así que, a menos que tengas a alguien en tu equipo que lo haga por ti,
(y que siempre vaya a estar contigo), te conviene desarrollarlas.

## Cómo documentarlos

No existe una forma aceptada por todos para documentar nada en el software,
dependiendo de la cultura del equipo y de la empresa en general. Veamos algunas
de las formas más comunes. Cabe mencionar que estas formas no son excluyentes,
se pueden combinar para ver diferentes aspectos de una misma función.

### Historias de Usuario

En este estilo de documentación, describes las funciones del sistema desde la
perspectiva del usuario. Se lleva muy bien con procesos modernos de desarrollo de
productos digitales, relacionados con el desarrollo ágil de software.

Tienen el siguiente formato:

- Como [rol de usuario]
- Quiero [acción/función]
- Para [beneficio/valor]

Como puedes ver, antes de empezar a crear historias de usuario, debes por lo menos
tener un idea de las personas que van a usar el sistema y lo roles que desempeñan.
Después, describes la función que va a realizar, desde su punto de vista, pero
también intentando mostrar cómo funcionará internamente el sistema para cumplir
con esa función.

Y finalmente, la razón de existencia de esta función: cómo es que beneficia al usuario
o la empresa que crea el software. Esta última parte es muy importante, ya que nos
hace pensar en si realmente es necesario tener esta función o no.

### Casos de Uso

Este tipo de documentación viene de la época en la que se prefería el desarrollo en cascada,
pero a mi me sigue pareciendo muy útil. Es más formal y detallada, incluye:

- Actores (usuarios o sistemas externos) involucrados
- Flujo principal: el caso en el que todo sale bien
- Flujos alternativos: los casos en los que algo sale mal o se manejan de otra manera
- Precondiciones y postcondiciones: cómo está el sistema antes y después de la ejecución

En muchos sistemas de documentación, los casos de uso requieren un identificador para
referirse a ellos en etapas posteriores, como cuando se hacen pruebas o se crean
tareas específicas para el equipo de desarrollo.

Los recomiendo mucho en el caso de sistemas o funciones críticas, en donde es
necesario pensar más a profundidad antes de empezar a desarrollar.
Puedes encontrar un ejemplo y una plantilla aquí:
[Casos de uso](https://lsi2.ugr.es/~mvega/docis/casos%20de%20uso.pdf).

## Cómo mantenerlos actualizados

El software es dinámico, y no basta con definir o documentar cómo funciona una
sola vez, tenemos que mantener actualizadas las funciones documentadas del
sistema o agregar nuevas conforme vayan apareciendo.

Aquí tienes algunas sugerencias para mantener actualizados los requerimientos:

### Revisar y actualizar

Si tienes suficiente personal, siempre debería haber un owner de la documentación
y esta persona debería revisar y asegurarse que los diferentes miembros del equipo
mantengan actualizadas las funciones documentadas y documenten las nuevas.

### Control de versiones

Es buena idea mantener los documentos de requerimientos bajo control de versiones,
igual que el código. De hecho, una de las mejores formas de hacer documentación es
tratarla exactamente como código, como se sugiere en [Docs as Code](https://www.writethedocs.org/guide/docs-as-code/).

Cada cambio debería ir acompañado de:

- Fecha del cambio
- Razón del cambio
- Persona responsable
- Impacto en el sistema

### Trazabilidad

Puedes mantener una matriz de trazabilidad que conecte los requerimientos con:

- El código que los implementa
- Las pruebas que los verifican
- Otra documentación relacionada

Para que esta matriz sea útil, se debe de incluir su actualización en el proceso
de desarrollo y considerarse dentro de la definición de "terminado" de una tarea (_definition of done_).
Esto es buena idea sólo si tienes un equipo grande y un proyecto complejo, ya que requiere
bastante trabajo en sí mismo.

### Comunicación efectiva

Esto es esencial para todos los procesos de desarrollo de software, pero debes asegurarte
que mientras más avance tu proyecto y más gente se involucre, más se haga:

- Que todos los cambios en los requerimientos sean comunicados a equipo de desarrollo y puestos en un documento que los describa
- Que las personas involucradas en el proyecto sepan de los cambios y sientan que su voz es escuchada, también registrando sus comentarios y sugerencias

Es importante dejar la registro de la comunicación y las decisiones tomadas para que el
conocimiento del software sea accesible para todos.

### Una alternativa: Design Documents

Los Design Documents son documentos que se usan en algunas big techs para documentar cómo se
va implementar una función. Como es natural, estos documentos son bastante técnicos y
algo tardados, pero incluyen por lo menos una descripción de la función que se quiere
implementar y _cómo se va a implementar_.

Están pensados para obtener consenso sobre la forma en la que se va a hacer algo y
son una buena idea si tienes un equipo de desarrollo maduro que puede llegar rápido
a compromisos para lograr implementar algo.

Un conjunto histórico de estos documentos, puede ser una buena alternativa para
documentar los requerimientos funcionales de un sistema.

## Conclusión

Entender lo que necesitamos que haga nuestro software es el primer paso para crear
software útil. Los requisitos funcionales o funciones y su documentación son una herramienta
para mantener un registro histórico y asegurarnos de que entendemos lo que se requiere.
Esto también puede servir para obtener aprobación de las personas interesadas en que
el software se realice y evitar malentendidos en el futuro.

También facilitan la estimación de recursos y tiempos, y permiten un desarrollo más eficiente
y enfocado. Finalmente, mejoran la comunicación entre todas las partes involucradas.

Es importante dedicar el tiempo y esfuerzo necesarios para documentarlos adecuadamente
(en mi opinión más como una herramienta de entendimiento que como una obligación) y mantenerlos
actualizados durante la vida del proyecto. Un sistema bien diseñado comienza con funciones
bien definidas, entendidas y gestionadas.
