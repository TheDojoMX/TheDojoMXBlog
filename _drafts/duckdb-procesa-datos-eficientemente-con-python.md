---
title: 'DuckDB: procesa datos eficientemente con Python'
date: 2024-06-25T00:00:00.000Z
author: Héctor Patricio
tags: DuckDB Python
comments: true
excerpt: Escribe aquí un buen resumen de tu artículo
header:
  overlay_image: null
  teaser: null
  overlay_filter: 'rgba(0, 0, 0, 0.5)'
---
El procesamiento de datos para obtener valor de ellos es una de las tareas que toda plataforma o aplicación
moderna tiene. Existen bases de datos especializadas en este tipo de trabajos, llamados OLAP (Online Analytical Processing: Procesamiento Analítico en Línea), por ejemplo BigQueru, SnowFlake o RedShift.
Estas bases de datos funcionan como servicios separados y tienes que mantenerlos y darles servicio (o pagar
por servicios administrados, como en los ejemplos de arriba) para poder seguir
usándolos.

Pero, gracias a DuckDB, no tiene por que ser así. En este artículo hablaremos de qué es, cómo funciona
y cómo puedes empezar con DuckDB.

## ¿Qué es DuckDB?

4a6e0b3d-6e64-4cec-ad92-1e3ad1818ce0
Así como SQLite es un base de datos transaccional que corre directamente "dentro"
de tu programa, permitiendo tener la funcionalidad de una base de datos relacional
sin tener que isntalar y mantener un servidor por separado, DuckDB te permite
tener una base de datos con interfaz SQL especializada en cargas analíticas.

O sea, lo que SQlite es para bases de datos transaccionales, DuckDB es para
bases de datos analíticas. Ya te imaginarás lo mucho que eso puede
ayudarte para empezar a hacer análisis de datos pesados en tus aplicaciones
o aplicaciones de análisis de datos puros con poco esfuerzo.

## ¿Cómo funciona DuckDB?

DuckDB es una base de datos analítica que se ejecuta en memoria. Puede cargar datos de distintas fuentes.

## Empezando con DuckDB

## Ejercicio: 100M row challenge

Veamos qué tan rápido es tanto en desarrollo como en ejecución hacer cosas con DuckDB.
Hace tiempo surgió en la comunidad de Java
