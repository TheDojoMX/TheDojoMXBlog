# Petición de Investigación: Bases de Datos para Series de Tiempo

## Objetivo
Investigar en profundidad las bases de datos especializadas en series de tiempo (TSDB) para escribir un artículo técnico completo y preciso dirigido a desarrolladores de software.

## Temas a Investigar

### 1. Fundamentos de Series de Tiempo
- Definición técnica precisa de serie de tiempo
- Componentes: timestamp, valores, tags/labels, fields
- Patrones de acceso típicos (escrituras vs lecturas)
- Volúmenes de datos típicos en producción
- Casos de uso reales en la industria (con ejemplos concretos)

### 2. Limitaciones de Bases de Datos Relacionales

**Investigar:**
- Benchmarks específicos comparando PostgreSQL/MySQL vs TSDBs
- Problemas de rendimiento en agregaciones temporales (ejemplos con tiempos reales)
- Ineficiencias en almacenamiento (ratios de compresión comparativos)
- Costos de índices B-tree para consultas por rangos temporales
- Casos documentados de migraciones de RDBMS a TSDB y sus resultados

**Necesito:**
- Ejemplos de consultas SQL lentas vs equivalentes en TSDB
- Datos de consumo de espacio: mismo dataset en PostgreSQL vs InfluxDB/TimescaleDB
- Gráficas o números de rendimiento de operaciones comunes

### 3. Características Técnicas de TSDBs

**Para cada característica, investigar:**

#### Compresión
- Algoritmos específicos: Gorilla (Facebook), Delta-of-delta encoding, LZ4, Snappy
- Ratios de compresión reales documentados
- Trade-offs entre compresión y velocidad de query
- Ejemplos concretos: "dataset X de 10GB se comprime a Y GB"

#### Índices y Estructuras de Datos
- LSM trees vs B-trees
- Time-sharding y particionamiento temporal
- Skip indexes, bloom filters para series temporales
- Cómo funciona el ordenamiento por timestamp

#### Retention Policies
- Implementación técnica de políticas de retención
- Ejemplos de configuración en diferentes TSDBs
- Downsampling: técnicas y algoritmos
- Continuous aggregates: cómo funcionan internamente

#### Modelo de Escritura
- Write-ahead logs (WAL) específicos para TSDBs
- Batch vs streaming inserts
- Benchmarks de throughput (puntos/segundo)
- Manejo de late-arriving data

### 4. Comparativa Detallada de TSDBs Populares

**Para cada base de datos investigar:**

#### InfluxDB
- Arquitectura (v2 vs v3)
- Lenguaje Flux: sintaxis, curva de aprendizaje
- Modelo de licenciamiento (OSS vs Enterprise vs Cloud)
- Casos de uso documentados
- Limitaciones conocidas
- Benchmarks independientes

#### TimescaleDB
- Cómo funciona como extensión de PostgreSQL
- Hypertables: implementación técnica
- Compresión columnar
- Continuous aggregates
- Casos de éxito documentados
- Comparativa con PostgreSQL vanilla

#### Prometheus
- Arquitectura pull-based
- Modelo de datos (métricas, labels)
- Lenguaje PromQL
- Limitaciones de almacenamiento local
- Integraciones con long-term storage (Thanos, Cortex, Mimir)
- Casos de uso en Kubernetes

#### VictoriaMetrics
- Mejoras sobre Prometheus
- Ratios de compresión vs Prometheus
- Benchmarks de rendimiento
- Compatibilidad con ecosistema Prometheus
- Casos de adopción reales

#### QuestDB
- Arquitectmo de almacenamiento columnar
- SQL optimizado para tiempo
- Performance en inserts (claims de millones/segundo)
- Casos de uso en trading/finanzas
- Comparativas con otras TSDBs

#### Otras menciones relevantes
- ClickHouse (como TSDB)
- Apache Druid
- Apache Pinot
- M3DB
- Graphite (legacy)

### 5. Criterios de Selección

**Investigar:**
- Métricas para decidir cuándo migrar de RDBMS a TSDB
- Umbrales de volumen de datos
- Patrones de consulta que indican necesidad de TSDB
- Costos de operación comparativos
- Casos donde TSDB NO es la mejor opción

### 6. Ejemplos Prácticos y Código

**Buscar o crear:**
- Schema de tabla relacional para métricas vs modelo TSDB
- Ejemplos de queries comparativos (SQL vs Flux vs PromQL)
- Configuración de retention policies (código real)
- Configuración de continuous aggregates
- Scripts de inserción de datos de ejemplo

### 7. Benchmarks y Datos Duros

**Recopilar:**
- Time Series Benchmark Suite (TSBS) results
- Benchmarks independientes publicados
- Casos de estudio con números reales
- Comparativas de consumo de recursos (CPU, RAM, disco)

## Formato de Salida Esperado

Por favor estructura tu investigación así:

1. **Resumen ejecutivo** (2-3 párrafos)
2. **Fundamentos** con definiciones y ejemplos
3. **Análisis de limitaciones de RDBMS** con datos concretos
4. **Características técnicas de TSDBs** explicadas en profundidad
5. **Comparativa detallada** de las 5 TSDBs principales
6. **Tabla comparativa** con métricas clave
7. **Criterios de decisión** con ejemplos
8. **Ejemplos de código** listos para usar
9. **Referencias y fuentes** (papers, documentación oficial, benchmarks)

## Fuentes Preferidas

- Documentación oficial de cada TSDB
- Papers académicos sobre compresión temporal y estructuras de datos
- Benchmarks independientes (no marketing)
- Blog posts técnicos de ingenieros (Netflix, Uber, Cloudflare, etc.)
- GitHub repos con comparativas
- Conferencias técnicas (talks de InfluxDays, KubeCon, etc.)

## Contexto Adicional

El artículo es para un blog técnico en español dirigido a desarrolladores intermedios/avanzados. Necesito:
- Información precisa y verificable
- Ejemplos concretos sobre teoría abstracta
- Números y benchmarks reales
- Trade-offs honestos (no marketing)
- Explicaciones que asuman conocimiento de bases de datos pero no de TSDBs específicas

## Preguntas Clave a Responder

1. ¿Cuál es el punto de inflexión donde una RDBMS se vuelve inadecuada para series de tiempo?
2. ¿Cómo funciona realmente la compresión Gorilla y por qué es tan efectiva?
3. ¿Cuáles son las diferencias arquitecturales fundamentales entre InfluxDB y TimescaleDB?
4. ¿Por qué Prometheus no es adecuado para long-term storage?
5. ¿Qué TSDB es mejor para qué caso de uso específico?
6. ¿Cuáles son los costos ocultos de adoptar una TSDB especializada?

## Profundidad Esperada

- Nivel técnico: intermedio-avanzado
- Incluir detalles de implementación cuando sean relevantes
- Evitar marketing speak, necesito hechos técnicos
- Priorizar información práctica sobre teórica
- Incluir warnings y limitaciones conocidas

---

**Fecha de entrega esperada:** [FECHA]
**Formato:** Markdown con código, tablas y referencias
**Extensión esperada:** 3000-5000 palabras de investigación
