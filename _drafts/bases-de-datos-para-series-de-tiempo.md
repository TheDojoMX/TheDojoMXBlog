---
title: "Bases de datos para series de tiempo"
date: 2024-12-07
author: Héctor Patricio
tags: series-de-tiempo bases-de-datos bd data-science
comments: true
excerpt: "¿Qué bases de datos puedes usar para guardar datos generados de manera periódica? Hablemos de por qué es importante escoger la herramienta correcta."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1736399971/veri-ivanova-p3Pj7jOYvnM-unsplash_cf1uue.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_450/v1736399971/veri-ivanova-p3Pj7jOYvnM-unsplash_cf1uue.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

En este artículo hablaremos de las series de tiempo, uno de los tipos de datos más comunes en la informática moderna.

La series de tiempo tienen características especiales, en estas los puntos de datos
consisten un par de valores: un identificador (el momento en el que sucedió) y un valor
(el valor que se observó).

Estas características hacen que trabajar con ellas sea diferente, porque además
se producen muchos de estos puntos de datos. Hablemos de cómo nos conviene almacenarlos.
Además, veremos que tienen de especial las bases de datos para series de tiempo.

## ¿Qué son las series de tiempo realmente?

<!-- TODO: Expandir definición -->
- Par timestamp + valor
- Tags/labels (servidor, región, métrica)
- Características: alta frecuencia de escritura, datos inmutables, consultas por rangos temporales
- Ejemplos concretos: métricas de CPU cada 10s, precios de acciones, sensores IoT

## ¿Por qué no usar una base de datos relacional?

Una base de datos relacional pensada en transacciones (OLTP) es muy flexible y sin duda
puedes almacenar pares de valores de tiempo y el valor medido sin ninguna dificultad.

### Problemas de rendimiento

- Consultas de agregación temporal lentas (AVG últimas 24h, MAX por hora, etc.)
- Índices B-tree no optimizados para consultas por rangos de tiempo
- Ejemplo de consulta lenta en PostgreSQL vs TSDB

### Problemas de almacenamiento

- Sin compresión especializada para datos temporales
- Desperdicio de espacio con valores repetidos
- Crecimiento lineal sin políticas de retención automáticas

### Ejemplo práctico

- Mostrar esquema en tabla relacional
- Comparar tamaño de almacenamiento
- Comparar tiempo de consulta para "promedio de CPU por servidor en última semana"

## ¿Qué hace especial a una base de datos de series de tiempo?

<!-- TODO: Características clave -->

### 1. Compresión optimizada

- Algoritmos específicos: delta encoding, gorilla compression
- Ejemplo: de 1GB a 100MB con datos reales
- Compresión por columnas temporales

### 2. Índices temporales especializados

- Ordenamiento automático por timestamp
- Skip indexes para búsquedas rápidas
- Particionamiento automático por tiempo

### 3. Políticas de retención (Retention policies)

- Eliminación automática de datos antiguos
- Configuración: "mantener datos crudos 7 días, agregados 90 días"
- Gestión de espacio sin intervención manual

### 4. Agregaciones continuas (Continuous aggregates)

- Pre-cálculo de métricas comunes
- Materialización automática de promedios por hora/día
- Consultas instantáneas en datos agregados

### 5. Downsampling automático

- Reducir resolución de datos antiguos
- De 1s a 1min a 1h conforme envejecen
- Conservar tendencias sin almacenar todos los puntos

### 6. Modelo de escritura optimizado

- Escrituras inmutables (append-only)
- Batch inserts optimizados
- Alto throughput (millones de puntos/segundo)

## Ejemplos de bases de datos para series temporales

<!-- TODO: Comparar opciones populares -->

### InfluxDB

- Descripción: TSDB pura, lenguaje Flux
- Casos de uso: monitoreo de infraestructura, IoT
- Ventajas: retention policies integradas, UI incluida
- Desventajas: licencia comercial en v3, curva de aprendizaje de Flux

### TimescaleDB

- Descripción: Extensión de PostgreSQL
- Casos de uso: cuando ya usas PostgreSQL, necesitas SQL estándar
- Ventajas: compatibilidad total con ecosistema PostgreSQL, SQL familiar
- Desventajas: requiere tuning manual, menor compresión que TSDBs puras

### Prometheus

- Descripción: TSDB enfocada en métricas y alerting
- Casos de uso: monitoreo de aplicaciones, Kubernetes
- Ventajas: pull model, alerting integrado, ecosistema maduro
- Desventajas: retención limitada (local), no para long-term storage

### VictoriaMetrics

- Descripción: Compatible con Prometheus, alto rendimiento
- Casos de uso: reemplazo de Prometheus a escala, long-term storage
- Ventajas: compresión superior, menor uso de recursos
- Desventajas: menos funcionalidades de alerting que Prometheus

### QuestDB

- Descripción: TSDB con SQL, muy rápida para ingestas
- Casos de uso: finanzas, trading de alta frecuencia
- Ventajas: SQL estándar, rendimiento excepcional en writes
- Desventajas: comunidad más pequeña, menos herramientas

### Tabla comparativa

| Base de datos | Lenguaje query | Compresión | Retención auto | Mejor para |
|---------------|----------------|------------|----------------|------------|
| InfluxDB | Flux | Alta | Sí | IoT, DevOps |
| TimescaleDB | SQL | Media | Manual | Apps PostgreSQL |
| Prometheus | PromQL | Media | Limitada | Métricas K8s |
| VictoriaMetrics | PromQL | Muy alta | Sí | Escala grande |
| QuestDB | SQL | Alta | Manual | Finanzas |

## ¿Cuándo usar una TSDB?

<!-- TODO: Criterios de decisión -->

### Señales de que necesitas una TSDB:

- Más de 10,000 puntos de datos por segundo
- Consultas frecuentes por rangos de tiempo
- Datos con timestamp como dimensión principal
- Necesidad de retención automática
- Agregaciones temporales (promedios por hora/día)

### Cuándo NO necesitas una TSDB:

- Pocos datos (< 1M puntos)
- Actualizaciones frecuentes de valores históricos
- Relaciones complejas entre entidades
- Transacciones ACID críticas

## Conclusión

La conclusión es sencilla: usa la herramienta adecuada para los datos que tienes que
almacenar y procesar. Por algo existen herramientas especializadas en tipos de datos
específicos. Personas con más experiencia se han dado cuenta de la necesidad de crear especializaciones en este tipo de datos.
