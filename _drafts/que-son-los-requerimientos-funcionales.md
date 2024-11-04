---
title: "¿Qué son los requerimientos funcionales?"
date: 2024-03-09
author: Héctor Patricio
tags:  arquitectura 
comments: true
excerpt: "El análisis de requerimientos es una parte fundamental del desarrollo de software y es importantísima
para crear sistemas exitosos."
header:
  overlay_image: #image 
  teaser: #image
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
resuelven un problema que ellos mismos viven o han vivido.

Pero esto no siempre es posible, sobre todo cuando construyes software como
profesión, porque no siempre puedes dedicar tiempo y recursos suficientes para
tú realizar la operación de lo que quieres resolver, o simplemente no es práctico.
Así que la segunda mejor opción que tenemos es **platicar con los usuarios**.

## Cómo documentarlos

Los requerimientos funcionales se pueden documentar de varias formas, pero aquí te presentamos las más comunes y efectivas:

### Historias de Usuario

Las historias de usuario son una forma ágil y centrada en el usuario de documentar requerimientos. Siguen el formato:

- "Como [rol de usuario]
- Quiero [acción/función]
- Para [beneficio/valor]"

### Casos de Uso

Documentación más formal y detallada que incluye:

- Actores involucrados
- Flujo principal
- Flujos alternativos
- Precondiciones y postcondiciones

### Especificaciones Funcionales

Documentos técnicos detallados que incluyen:
- Descripción detallada de la función
- Entradas y salidas esperadas
- Reglas de negocio aplicables
- Restricciones técnicas

### Diagramas y Modelos

Representaciones visuales como:
- Diagramas de flujo
- Modelos de datos
- Diagramas de secuencia
- Prototipos de interfaz

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
