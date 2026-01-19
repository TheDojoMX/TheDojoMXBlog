---
title: "Bases de datos para series de tiempo"
date: 2025-12-29
author: "Héctor Patricio"
tags: ['series-de-tiempo', 'bases-de-datos', 'data-science', 'tsdb', 'timescaledb', 'prometheus']
description: "¿Qué bases de datos puedes usar para guardar datos generados de manera periódica? Hablemos de por qué es importante escoger la herramienta correcta."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1736399971/veri-ivanova-p3Pj7jOYvnM-unsplash_cf1uue.jpg"
draft: true
---

En este artículo hablaremos de las series de tiempo, uno de los tipos de datos más comunes en la informática moderna.

La series de tiempo tienen características especiales, en estas los puntos de datos
consisten un par de valores: un identificador (el momento en el que sucedió) y un valor
(el valor que se observó).

Estas características hacen que trabajar con ellas sea diferente, porque además
se producen muchos de estos puntos de datos. Hablemos de cómo nos conviene almacenarlos.
Además, veremos que tienen de especial las bases de datos para series de tiempo.

## ¿Qué son las series de tiempo realmente?

Una serie de tiempo es una secuencia de puntos de datos ordenados cronológicamente.
Cada punto consiste en al menos dos elementos: un **timestamp** (el momento exacto
en que se registró) y un **valor** (la medición observada en ese instante).

En la práctica, los puntos de datos suelen incluir también **tags** o **labels**
que proporcionan contexto adicional. Por ejemplo, una métrica de uso de CPU
podría incluir etiquetas como el nombre del servidor, la región del datacenter
o el nombre de la aplicación. Esto permite filtrar y agrupar los datos de
maneras útiles.

Las series de tiempo tienen características distintivas que las diferencian
de otros tipos de datos:

- **Alta frecuencia de escritura**: los datos llegan constantemente, a veces
  miles o millones de puntos por segundo, a veces también **a intervalos regulares**
- **Datos inmutables**: una vez registrado un punto, rara vez se modifica, y generalmente
no tiene sentido que haya actualizaciones
- **Consultas por rangos temporales**: las preguntas típicas son "¿qué pasó
  en las últimas 24 horas?" o "¿cuál fue el promedio del último mes?"
- **Importancia del orden**: el timestamp es la dimensión principal de análisis

Algunos ejemplos concretos de series de tiempo que probablemente ya conoces:

- Métricas de infraestructura: uso de CPU cada 10 segundos, memoria disponible,
  requests por segundo
- Datos financieros: precios de acciones, tipos de cambio, volumen de transacciones
- IoT y sensores: temperatura de un refrigerador industrial, vibración de
  maquinaria, consumo eléctrico
- Métricas de aplicación: latencia de endpoints, errores por minuto, usuarios
  activos

## ¿Por qué no usar una base de datos relacional?

Una base de datos relacional pensada en transacciones (OLTP) es muy flexible y sin duda
puedes almacenar pares de valores de tiempo y el valor medido sin ninguna dificultad. Pero
veamos algunas de las razones por las que no es buena idea usar este tipo de bases de datos.

### Problemas de rendimiento

Las consultas de agregación temporal se vuelven lentas conforme crece la tabla.
Calcular el promedio de las últimas 24 horas o el máximo por hora requiere
escanear millones de filas, incluso con índices bien diseñados.

Los índices _B-tree_, el tipo más común en bases de datos relacionales, no están
optimizados para consultas por rangos de tiempo. Un índice B-tree funciona bien
para búsquedas exactas (`WHERE timestamp = X`), pero para rangos
(`WHERE timestamp BETWEEN X AND Y`) debe recorrer muchos nodos del árbol.

Considera esta consulta típica en PostgreSQL:

```sql
-- Promedio de CPU por servidor en la última semana
SELECT server_id, AVG(cpu_usage)
FROM metrics
WHERE timestamp > NOW() - INTERVAL '7 days'
GROUP BY server_id;
```

Con 100 millones de filas, esta consulta puede tardar minutos. En una TSDB
especializada, la misma operación toma segundos gracias a índices temporales
y datos pre-agregados.

### Problemas de almacenamiento

Las bases de datos relacionales no tienen compresión especializada para datos
temporales. Los timestamps consecutivos suelen diferir por pocos segundos, pero
se almacenan como valores completos de 8 bytes cada uno. Lo mismo ocurre con
valores numéricos que cambian poco entre mediciones.

Además, hay desperdicio de espacio con valores repetidos. Si el `server_id` es
"web-server-prod-01" y tienes un millón de mediciones, esa cadena se almacena
(o referencia) un millón de veces.

El crecimiento es lineal y sin control automático. Si generas 1GB de datos
por día, en un año tendrás 365GB. Sin políticas de retención automáticas,
debes implementar scripts manuales para purgar datos antiguos.

### Ejemplo práctico

Veamos cómo se vería un esquema típico en PostgreSQL para guardar una
serie de métricas:

```sql
CREATE TABLE metrics (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    server_id VARCHAR(100) NOT NULL,
    metric_name VARCHAR(50) NOT NULL,
    value DOUBLE PRECISION NOT NULL
);

CREATE INDEX idx_metrics_time ON metrics(timestamp);
CREATE INDEX idx_metrics_server ON metrics(server_id, timestamp);
```

Este esquema funciona, pero tiene algunos problemas:

- Cada fila ocupa ~150 bytes (con overhead de PostgreSQL)
- 1 millón de puntos = ~150MB
- 1 billón de puntos = ~150GB

En una TSDB como TimescaleDB con compresión habilitada, el mismo billón de
puntos puede ocupar 15-30GB, una reducción de 5-10x.

## ¿Qué hace especial a una base de datos de series de tiempo?

Las TSDBs están diseñadas desde cero para manejar
las características únicas de los datos temporales. Veamos qué las hace diferentes.

### 1. Compresión optimizada

Las TSDBs usan algoritmos de compresión específicos para datos con las características
que hemos mencionado:

- **Delta encoding**: en lugar de guardar cada timestamp completo, se guarda
  la diferencia con el anterior. Si los datos llegan cada 10 segundos, solo
  se almacena "10" en lugar de timestamps completos
- **Gorilla compression**: desarrollado por Facebook, comprime valores
  flotantes aprovechando que mediciones consecutivas suelen ser similares
- **Dictionary encoding**: para tags repetidos como nombres de servidores

El resultado es muy conveniente: datos que ocuparían 1GB en PostgreSQL pueden
reducirse a 100MB o menos en una TSDB con compresión habilitada.

### 2. Índices temporales especializados

Las TSDBs organizan los datos de forma que las consultas temporales sean
naturalmente eficientes:

- **Ordenamiento automático por timestamp**: los datos se almacenan
  físicamente en orden cronológico, eliminando la necesidad de ordenar en cada query
- **Skip indexes**: permiten saltar bloques enteros de datos que no coinciden
  con el rango temporal buscado
- **Particionamiento automático por tiempo**: los datos se dividen en
  "chunks" por período (hora, día, semana, etc.), permitiendo escanear solo las
  particiones relevantes

### 3. Políticas de retención

Una de las características más útiles es la gestión automática del ciclo de
vida de los datos, es decir, cuánto tiempo permanecen almacenados. Las TSDBs
permiten definir:

- **Eliminación automática**: configuras "eliminar datos mayores a 30 días"
  y la TSDB lo hace automáticamente
- **Políticas diferenciadas por tipo de dato**: puedes mantener datos crudos 7 días,
  agregados por hora 90 días, y agregados por día indefinidamente
- **Sin intervención manual**: no necesitas cron jobs ni scripts de limpieza

### 4. Agregaciones continuas (Continuous aggregates)

Las TSDBs pueden pre-calcular métricas comunes en segundo plano:

- **Materialización automática**: defines "quiero el promedio por hora de
  cada métrica" y la TSDB mantiene esos cálculos actualizados, guardados físicamente, esto nodos
da lo que parecen _consultas instantáneas_: preguntar "¿cuál fue el promedio de CPU ayer?"
  no requiere escanear millones de filas, solo leer el valor pre-calculado
- **Actualización incremental**: cuando llegan nuevos datos, solo se
recalcula lo necesario

### 5. Downsampling automático

Hacer "downsampling" es reducir la cantidad de datos retenidos siguiendo alguna política.
También se entiende como bajar la "resolución" de datos antiguos para ahorrar espacio.
Hacer esto tiene múltiples facetas:

- **Resolución variable por antigüedad**: datos del último día a resolución
  de 1 segundo, última semana a 1 minuto, último mes a 1 hora
- **Conservación de tendencias**: aunque se pierda la granularidad, las tendencias
  generales se mantienen~~
- **Configuración declarativa**: defines las reglas una vez y la TSDB las
  aplica automáticamente

### 6. Modelo de escritura optimizado

Las TSDBs están optimizadas para el patrón de escritura típico de series
de tiempo, normalmente son "append-only": los datos nuevos siempre se
agregan al final, sin necesidad de buscar dónde insertar y sin cambiar datos anteriores.
También se hacen **batch inserts**, pueden recibir miles de puntos en una sola operación,
lo que reduce la sobrecarga.

## Principales opciones en el mercado

Existen varias opciones maduras de TSDBs en el mercado. Cada una tiene sus fortalezas
y casos de uso ideales.

### InfluxDB

InfluxDB es una de las más conocidas. Usa su propio lenguaje de consultas
llamado Flux (aunque también soporta InfluxQL, similar a SQL). Es usada para
monitoreo de infraestructura e IoT.
**Ventajas**: retention policies integradas, interfaz web incluida, buena
documentación y comunidad activa.
**Desventajas**: Flux tiene una curva de aprendizaje significativa si vienes de SQL.

### TimescaleDB

TimescaleDB es una extensión de PostgreSQL que le agrega capacidades de TSDB.
Es la opción natural si ya usas PostgreSQL y no quieres aprender un nuevo
sistema.

**Ventajas**: compatibilidad total con el ecosistema PostgreSQL (pg_dump,
replicación, extensiones), SQL estándar, fácil migración.

**Desventajas**: requiere tuning manual para obtener el mejor rendimiento,
la compresión es menor que en TSDBs puras.~~

### QuestDB

QuestDB es una TSDB relativamente nueva enfocada en rendimiento extremo,
especialmente para ingestas masivas. Usa SQL estándar.

**Ventajas**: tiene un rendimiento excepcional en escrituras (millones
de filas por segundo), ideal para finanzas y trading de alta frecuencia.

**Desventajas**: comunidad más pequeña que las opciones anteriores, menos
integraciones disponibles.

### Tabla comparativa

| Base de datos | Lenguaje query | Compresión | Retención auto | Mejor para |
|---------------|----------------|------------|----------------|------------|
| InfluxDB | Flux | Alta | Sí | IoT, DevOps |
| TimescaleDB | SQL | Media | Manual | Apps PostgreSQL |
| QuestDB | SQL | Alta | Manual | Finanzas |

## ¿Cuándo usar una TSDB?

No siempre necesitas una base de datos especializada. Recuerda que cada pieza
de sotware extra que introduzcas en tu sistema aumenta la carga de mantenimiento
y la complejidad en genral. Veamos algunos consejos para tomar la decisión.

### Cuándo SÍ necesitas una TSDB

- **Consultas temporales frecuentes**: "dame el promedio de la última hora"
  es una pregunta común
- **Timestamp como dimensión principal**: el tiempo es el eje principal de
  análisis, no las relaciones entre entidades
- **Necesidad de políticas de retención automáticas**: quieres que los datos viejos se
  eliminen o compriman sin intervención manual
- **Agregaciones temporales eficientes**: necesitas promedios, máximos o mínimos por
  hora, día o semana de forma eficiente

### Cuándo NO necesitas una TSDB

- **Volumen bajo**: menos de un millón de puntos en total
- ~~**Actualizaciones frecuentes**: necesitas modificar valores históricos
  regularmente (las TSDBs asumen datos inmutables)~~
- ~~**Relaciones complejas**: tus datos tienen muchas relaciones entre
  entidades que necesitas consultar (JOINs complejos)~~
- ~~**Transacciones ACID críticas**: necesitas garantías estrictas de
  consistencia que las TSDBs sacrifican por rendimiento~~

## Conclusión

La conclusión es sencilla: usa la herramienta adecuada para los datos que tienes que
almacenar y procesar. Por algo existen herramientas especializadas en tipos de datos
específicos. Personas con más experiencia se han dado cuenta de la necesidad de crear especializaciones en este tipo de datos.

~~Si trabajas con métricas de infraestructura, datos de sensores, logs con
timestamps o cualquier dato que se genere continuamente en el tiempo, vale
la pena evaluar una TSDB. La inversión inicial en aprender una nueva
herramienta se paga rápidamente con consultas más rápidas, menor uso de
almacenamiento y menos mantenimiento operativo.~~

~~Mi recomendación para empezar:~~

~~- **Si ya usas PostgreSQL**: prueba TimescaleDB, la transición es mínima~~
~~- **Si usas Kubernetes**: Prometheus + VictoriaMetrics es una combinación probada~~
~~- **Si empiezas de cero con IoT o métricas**: InfluxDB tiene buena documentación~~
~~- **Si necesitas máximo rendimiento en escrituras**: evalúa QuestDB~~

~~El mundo de las series de tiempo es amplio, pero estas herramientas te
darán una base sólida para cualquier proyecto que involucre datos temporales.~~
