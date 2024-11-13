---
title: "¿Qué son los requerimientos funcionales?"
date: 2024-03-09
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
Puedes encontrar un ejemplo y una plantilla aquí: []

### Matrices de Requerimientos

Tablas estructuradas que contienen:
- ID del requerimiento
- Descripción
- Prioridad
- Estado
- Dependencias

## Cómo mantenerlos actualizados

Los requerimientos funcionales deben mantenerse actualizados conforme el sistema evoluciona. Algunas buenas prácticas para lograrlo son:

1. **Revisiones periódicas**: Programar revisiones regulares (por ejemplo, trimestrales) de los requerimientos con los usuarios principales y el equipo de desarrollo.

2. **Control de versiones**: Mantener los documentos de requerimientos bajo control de versiones, igual que el código. Cada cambio debe estar documentado con:
   - Fecha del cambio
   - Razón del cambio
   - Persona responsable
   - Impacto en el sistema

3. **Trazabilidad**: Mantener una matriz de trazabilidad que conecte los requerimientos con:
   - El código que los implementa
   - Las pruebas que los verifican
   - La documentación relacionada

4. **Proceso de cambios**: Establecer un proceso formal para solicitar y aprobar cambios en los requerimientos, que incluya:
   - Evaluación del impacto
   - Aprobación de stakeholders
   - Actualización de documentación relacionada

5. **Comunicación efectiva**: Asegurar que todos los cambios en los requerimientos sean comunicados a:
   - Equipo de desarrollo
   - Usuarios clave
   - Stakeholders relevantes

Mantener los requerimientos actualizados es crucial para el éxito continuo del proyecto y para asegurar que el sistema siga cumpliendo las necesidades de los usuarios.

## Conclusión

Los requerimientos funcionales son la base fundamental de cualquier proyecto de software exitoso. Son la guía que define qué debe hacer el sistema y cómo debe comportarse para satisfacer las necesidades de los usuarios. Una buena documentación y gestión de estos requerimientos:

- Reduce malentendidos y errores de interpretación
- Facilita la estimación de recursos y tiempos
- Permite un desarrollo más eficiente y enfocado
- Simplifica la validación y verificación del sistema
- Mejora la comunicación entre todas las partes involucradas

Es fundamental dedicar el tiempo y esfuerzo necesarios para documentarlos adecuadamente y mantenerlos actualizados durante todo el ciclo de vida del proyecto. Un sistema bien diseñado comienza con requerimientos funcionales bien definidos y gestionados.
