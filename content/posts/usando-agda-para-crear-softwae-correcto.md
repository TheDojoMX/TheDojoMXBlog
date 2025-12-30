---
title: "Usando Agda para crear softwae correcto"
date: 2024-01-12
author: "Héctor Patricio"
tags: ['agda', 'fp', 'mathematics', 'matemáticas']
description: "Escribe aquí un buen resumen de tu artículo"
featuredImage: "#image"
draft: true
---

En este artículo hablaremos Agda, un lenguaje de programación con un sistema de tipos muy estricto
que te puede ayudar a crear pruebas de que tu software funciona bien a nivel teórica antes de programar
la implementación que va a producción.

## ¿Qué es Agda?

Agda es un lenguaje con un sistema de tipos dependientes, lo que significa en pocas palabras que el mismo
sistema de tipos es un lenguaje de programación con el que puedes realizar cálculos, pero también significa
que te vas a pelear mucho con él para definir las cosas **correctamente**.

Algunos lenguajes que son una competencia de Agda son: Lean, Idris y TLA+.

## Fundamentos teóricos

- Correspondencia Curry-Howard (proposiciones como tipos, pruebas como programas)
- Teoría de tipos de Martin-Löf
- Cómo los tipos expresan propiedades matemáticas

## Instalación y configuración

- Requisitos previos (GHC/Haskell)
- Instalación de Agda
- Configuración del editor (Emacs con agda-mode, VS Code)
- Primer programa "Hello World" en Agda

## Sintaxis básica de Agda

- Definición de tipos de datos
- Pattern matching
- Funciones y recursión
- Notación mixfix (operadores personalizados)
- Módulos e imports

## Tipos dependientes en acción

- Ejemplo: Vectores con longitud en el tipo (`Vec A n`)
- Ejemplo: Números naturales y propiedades
- Cómo el compilador previene errores de índice

## Escribiendo pruebas en Agda

- Cómo una prueba es simplemente un programa que type-checks
- Ejemplo: probar que la suma es conmutativa
- Ejemplo: probar propiedades de listas
- Uso de holes (`?`) para desarrollo interactivo

## Caso de estudio práctico

- Definir una especificación formal de un algoritmo simple (ej. ordenamiento)
- Implementar el algoritmo
- Probar que la implementación cumple la especificación

## Flujo de trabajo: del prototipo a producción

- Usar Agda para prototipar y verificar
- Extraer o reimplementar en lenguaje de producción
- Integración con Haskell (extracción de código)

## Limitaciones y consideraciones

- Curva de aprendizaje pronunciada
- No todos los programas son fáciles de verificar
- Tiempo de compilación/verificación
- Cuándo vale la pena usar Agda vs testing tradicional

## Recursos para aprender más

- "Programming Language Foundations in Agda" (PLFA)
- Documentación oficial
- Comunidad y foros
- Cursos y tutoriales recomendados

## Conclusión

- Resumen de beneficios de Agda
- Llamado a la acción: probar Agda en un proyecto pequeño
- El futuro de la verificación formal en desarrollo de software
