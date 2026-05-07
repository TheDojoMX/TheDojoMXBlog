---
title: "RAG en 2026: la paradoja de la simplicidad y el regreso de PostgreSQL"
date: 2026-02-15
author: "Héctor Patricio"
tags: ['rag', 'bases-de-datos', 'postgresql', 'llms', 'arquitectura', 'embeddings', 'inteligencia-artificial']
description: "Analizamos el estado de RAG en 2026: por qué las arquitecturas simples siguen ganando, cuándo PostgreSQL con pgvector es suficiente, y las 10 variantes de RAG que deberías conocer."
featuredImage: ""
draft: true
---

<!-- Palabra estimada total: ~4,100 palabras -->

## Introducción: RAG no está muerto, pero ha cambiado

<!-- ~350 palabras -->

Contextualizar: RAG (Retrieval-Augmented Generation) fue declarado "muerto" varias
veces desde 2024, pero sigue siendo el patrón dominante para conectar LLMs con
datos propios. Lo que sí cambió es nuestra comprensión de qué funciona y qué no.

Puntos clave:
- La predicción de "RAG está muerto" vs la realidad
- Ventanas de contexto más grandes (Gemini 2M, Claude 200K) no eliminaron la
  necesidad de RAG
- El costo y la latencia de meter todo en el contexto siguen siendo prohibitivos

## La paradoja de la simplicidad

<!-- ~600 palabras -->

El hallazgo más sorprendente de los últimos dos años: las implementaciones simples
de RAG frecuentemente superan a las complejas. Analizar por qué.

### Chunking simple vs chunking "inteligente"

Estudios y experiencias prácticas muestran que el chunking por tamaño fijo con
overlap funciona tan bien o mejor que técnicas sofisticadas basadas en semántica.
Por qué ocurre esto.

### El mito de los embeddings perfectos

Invertir semanas optimizando embeddings rara vez produce mejoras significativas
comparado con mejorar la calidad de los datos de entrada. La ley de Pareto
aplicada a RAG.

### Lecciones de la ingeniería de software: la tecnología aburrida gana

Conectar con la filosofía del blog sobre "tecnología aburrida" (referencia al post
sobre escoger tu stack). Las soluciones probadas y entendidas suelen ser mejores
que las novedosas.

## PostgreSQL + pgvector: cuándo es suficiente (y cuándo no)

<!-- ~700 palabras -->

Análisis técnico de usar PostgreSQL como base de datos vectorial en lugar de
soluciones especializadas.

### pgvector en 2026: estado actual

pgvector ha madurado significativamente. Soporte para HNSW, IVFFlat, mejoras de
rendimiento en las últimas versiones. Qué tan lejos llega.

### Ventajas de usar una sola base de datos

Simplicidad operacional, transacciones ACID para metadatos + vectores, un solo
sistema que monitorear, menor costo de infraestructura. La complejidad operacional
es un costo que se subestima.

### Cuándo NO usar PostgreSQL para vectores

Cuando tienes más de 10-50 millones de vectores, cuando necesitas sub-10ms de
latencia consistente, cuando necesitas búsqueda distribuida. Alternativas: Qdrant,
Weaviate, Pinecone y cuándo justifican su complejidad.

### El costo real: mantener índices en RAM

El cuello de botella que nadie menciona: los índices HNSW necesitan estar en RAM
para consultas rápidas. Un millón de vectores de 1536 dimensiones requiere ~6GB
solo para el índice. Calcular costos reales.

## Las 10 arquitecturas de RAG que deberías conocer

<!-- ~1,200 palabras -->

Catálogo de las variantes de RAG más relevantes en 2026, con una breve descripción
de cuándo usar cada una.

### 1. RAG Básico (Naive RAG)

Chunk -> Embed -> Retrieve -> Generate. Cuándo es suficiente: la mayoría de las veces.

### 2. RAG con Re-ranking

Añadir un paso de re-ranking después de la recuperación para mejorar la relevancia.
Cross-encoders como Cohere Rerank o modelos open source.

### 3. RAG Híbrido (Sparse + Dense)

Combinar búsqueda vectorial con búsqueda léxica (BM25). Por qué la combinación
suele superar a cualquiera de las dos por separado.

### 4. GraphRAG

Usar grafos de conocimiento para estructurar relaciones entre documentos. Cuándo la
estructura relacional importa más que la similitud semántica. Referencia al trabajo
de Microsoft.

### 5. Agentic RAG

Un agente decide qué fuentes consultar, cuándo refinar la consulta, y cuándo la
respuesta es suficiente. Más flexible pero más difícil de controlar.

### 6. Corrective RAG (CRAG)

El sistema evalúa la calidad de los documentos recuperados y decide si necesita
buscar más o de forma diferente. Self-correction integrado.

### 7. Self-RAG

El modelo genera reflexiones sobre si necesita recuperar información, si la
información recuperada es relevante, y si su respuesta es fiel a las fuentes.

### 8. RAG Multimodal

Recuperación y generación con imágenes, tablas y texto. ColPali y otros enfoques
de embeddings multimodales.

### 9. RAG con Cache Semántico

Cachear respuestas a preguntas semánticamente similares para reducir latencia y
costos. GPTCache y alternativas.

### 10. RAG Adaptativo

El sistema elige dinámicamente la estrategia de RAG según la complejidad de la
pregunta: a veces no necesita recuperación, a veces necesita múltiples pasos.

## Memoria vs RAG: cuándo la memoria contextual gana

<!-- ~500 palabras -->

Explorar la tendencia emergente de sistemas de memoria para agentes que
complementan o reemplazan a RAG clásico.

### Memoria episódica vs memoria semántica

Diferenciar entre recordar interacciones pasadas (episódica) y tener acceso a
conocimiento estructurado (semántica). RAG es mejor para semántica, memoria
para episódica.

### Mem0, Zep y el ecosistema de memoria para agentes

Herramientas que implementan memoria persistente para agentes. Cuándo usar
memoria en lugar de (o además de) RAG.

### La convergencia: sistemas que combinan RAG + memoria

La arquitectura más robusta no elige entre RAG y memoria, sino que usa ambos
para diferentes tipos de información.

## Decisiones arquitectónicas prácticas

<!-- ~500 palabras -->

Guía de decisión para implementar RAG en un proyecto real.

### Empieza simple, complejiza con evidencia

Implementa RAG básico primero. Mide. Solo añade complejidad cuando los datos
muestren que es necesario.

### El pipeline de evaluación es más importante que la arquitectura

Invierte más tiempo en construir un sistema de evaluación (RAGAS, TruLens) que
en optimizar la arquitectura. Sin métricas, estás adivinando.

### Costos que se ignoran: indexación, actualización y mantenimiento

El costo de mantener un sistema RAG no es solo la API del LLM. Indexar documentos
nuevos, re-indexar cuando cambias el modelo de embeddings, y monitorear la calidad
son costos operacionales reales.

## Conclusión: la madurez del pragmatismo

<!-- ~250 palabras -->

Resumen: RAG ha madurado. Las soluciones simples funcionan, PostgreSQL es una opción
viable para la mayoría, y la complejidad debe justificarse con datos. Como en todo el
desarrollo de software, la simplicidad es una virtud.

---

## Resumen de investigación

RAG en 2025-2026 atraviesa una consolidación paradójica: después de años de pipelines cada vez más complejas, evidencia significativa muestra que arquitecturas simples frecuentemente igualan o superan a las elaboradas, mientras PostgreSQL con pgvector gana credibilidad seria como infraestructura de producción.

**La paradoja de la simplicidad.** El benchmark de chunking de NVIDIA (2024) encontró que page-level chunking — una de las estrategias más simples — logró la mayor precisión (0.648) con la menor varianza en 5 datasets. Contextual Retrieval de Anthropic mostró que prepender contexto a chunks antes de embeddings redujo fallos de retrieval 35%, y 67% combinado con reranking. Mejorar fundamentos (mejor contexto de chunks, búsqueda híbrida BM25+vector, reranker) produce más retorno que complejidad arquitectónica.

**El regreso de PostgreSQL.** pgvector 0.8.0 (octubre 2024) añadió iterative index scanning para queries filtradas. Timescale demostró 28x menor latencia p95 que Pinecone's storage-optimized index a 75% menos costo en 50M vectores. Instacart migró de Elasticsearch a PostgreSQL + pgvector con 80% de ahorro. Consenso emergente: para <10-100M vectores, PostgreSQL con pgvector es el default pragmático.

**Variantes avanzadas: nicho pero importantes.** GraphRAG (Microsoft, 2024) excele en queries de sensemaking global. RAPTOR (Stanford/ICLR 2024) mejora razonamiento multi-step con 20% de mejora absoluta en QuALITY. Self-RAG y Corrective-RAG introducen loops de auto-evaluación. HyDE mejora retrieval zero-shot generando un documento hipotético antes de buscar.

**Context windows largos vs RAG.** "Lost in the Middle" (Liu et al., TACL 2024) estableció que el rendimiento degrada significativamente para información en el medio de contextos largos (curva U). Los context windows no eliminan la necesidad de retrieval; la complementan.

**Calidad de datos > arquitectura.** 42% de implementaciones RAG fallidas citan limpieza de datos como causa primaria. Chunking strategy es la decisión técnica de mayor apalancamiento.

---

### Referencias y recursos

#### Surveys y fundamentos

1. **Gao, Y., Xiong, Y., et al. (2024).** "Retrieval-Augmented Generation for Large Language Models: A Survey." [https://arxiv.org/abs/2312.10997](https://arxiv.org/abs/2312.10997) — Survey fundacional clasificando RAG en Naive, Advanced y Modular. La referencia más citada para categorización de arquitecturas RAG.

2. **Gupta, S., et al. (2024).** "A Comprehensive Survey of Retrieval-Augmented Generation (RAG)." [https://arxiv.org/abs/2410.12837](https://arxiv.org/abs/2410.12837) — Survey más actual trazando la evolución de RAG desde conceptos fundacionales hasta estado del arte.

3. **Agentic RAG Survey. (2025).** "Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG." [https://arxiv.org/abs/2501.09136](https://arxiv.org/abs/2501.09136) — Survey definitivo de Agentic RAG: agentes autónomos con planning, tool use, retrieval multi-step y auto-reflexión.

#### Variantes de RAG

4. **Edge, D., et al. (2024).** "From Local to Global: A Graph RAG Approach to Query-Focused Summarization." *Microsoft Research*. [https://arxiv.org/abs/2404.16130](https://arxiv.org/abs/2404.16130) — GraphRAG: grafos de conocimiento con resúmenes jerárquicos de comunidades. Mejoras sustanciales para sensemaking global en corpora de millones de tokens.

5. **Sarthi, P., et al. (2024).** "RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval." *ICLR 2024*. [https://arxiv.org/abs/2401.18059](https://arxiv.org/abs/2401.18059) — Árbol jerárquico de resúmenes recursivos. 20% mejora absoluta en QuALITY con GPT-4.

6. **Asai, A., et al. (2023).** "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection." [https://arxiv.org/abs/2310.11511](https://arxiv.org/abs/2310.11511) — Modelo que decide adaptativamente cuándo hacer retrieval y critica sus propias generaciones con tokens de reflexión.

7. **Yan, S-Q., et al. (2024).** "Corrective Retrieval Augmented Generation." [https://arxiv.org/abs/2401.15884](https://arxiv.org/abs/2401.15884) — Evaluador de relevancia con acciones correctivas: refinamiento de conocimiento o búsqueda web como fallback.

8. **Gao, L., et al. (2023).** "Precise Zero-Shot Dense Retrieval without Relevance Labels." *ACL 2023*. [https://arxiv.org/abs/2212.10496](https://arxiv.org/abs/2212.10496) — HyDE: genera documento hipotético antes de buscar, mejorando retrieval zero-shot.

#### Context windows vs RAG

9. **Liu, N.F., et al. (2024).** "Lost in the Middle: How Language Models Use Long Contexts." *TACL*. [https://arxiv.org/abs/2307.03172](https://arxiv.org/abs/2307.03172) — Curva U de rendimiento en contextos largos: información en el medio se pierde. Los context windows no eliminan la necesidad de RAG.

10. **Meilisearch. (2024).** "RAG vs. long-context LLMs: A side-by-side comparison." [https://www.meilisearch.com/blog/rag-vs-long-context-llms](https://www.meilisearch.com/blog/rag-vs-long-context-llms) — Long-context LLMs superan a RAG cuando hay recursos abundantes, pero RAG es más cost-efficient. Framework de decisión práctico.

#### PostgreSQL y pgvector

11. **Timescale. (2024).** "pgvector Is Now Faster than Pinecone at 75% Less Cost." [https://www.timescale.com/blog/pgvector-is-now-as-fast-as-pinecone-at-75-less-cost](https://www.timescale.com/blog/pgvector-is-now-as-fast-as-pinecone-at-75-less-cost) — 50M vectores: 28x menor latencia p95 y 16x mayor throughput que Pinecone a 75% menos costo.

12. **PostgreSQL Project. (2024).** "pgvector 0.8.0 Released." [https://www.postgresql.org/about/news/pgvector-080-released-2952/](https://www.postgresql.org/about/news/pgvector-080-released-2952/) — Iterative index scanning para HNSW/IVFFlat, mejoras de rendimiento significativas.

13. **AWS Database Blog. (2024).** "Supercharging vector search with pgvector 0.8.0 on Aurora PostgreSQL." [https://aws.amazon.com/blogs/database/supercharging-vector-search-performance-and-relevance-with-pgvector-0-8-0-on-amazon-aurora-postgresql/](https://aws.amazon.com/blogs/database/supercharging-vector-search-performance-and-relevance-with-pgvector-0-8-0-on-amazon-aurora-postgresql/) — Hasta 9x más rápido y 100x resultados más relevantes con pgvector 0.8.0.

14. **Render. (2025).** "Simplify Your AI Stack with PostgreSQL and pgvector." [https://render.com/articles/simplify-ai-stack-managed-postgresql-pgvector](https://render.com/articles/simplify-ai-stack-managed-postgresql-pgvector) — Caso Instacart: 80% ahorro de costos migrando de Elasticsearch a PostgreSQL + pgvector.

#### Vector databases

15. **Shakudo. (2026).** "Top 9 Vector Databases as of February 2026." [https://www.shakudo.io/blog/top-9-vector-databases](https://www.shakudo.io/blog/top-9-vector-databases) — Comparación actual de opciones: Pinecone, Qdrant, Milvus, Weaviate vs pgvector.

16. **LiquidMetal AI. (2025).** "Vector Database Comparison." [https://liquidmetal.ai/casesAndBlogs/vector-comparison/](https://liquidmetal.ai/casesAndBlogs/vector-comparison/) — Mercado vector DB creció de $1.73B en 2024 hacia proyección de $10.6B para 2032.

#### Chunking y retrieval

17. **Anthropic. (2024).** "Contextual Retrieval." [https://www.anthropic.com/news/contextual-retrieval](https://www.anthropic.com/news/contextual-retrieval) — Prepender contexto a chunks reduce fallos de retrieval 35%, con reranking 67%. ~$1.02 por millón de chunks.

18. **Firecrawl. (2025).** "Best Chunking Strategies for RAG in 2025." [https://www.firecrawl.dev/blog/best-chunking-strategies-rag-2025](https://www.firecrawl.dev/blog/best-chunking-strategies-rag-2025) — Benchmark NVIDIA: page-level chunking gana con 0.648 accuracy y menor desviación estándar.

19. **Weaviate. (2024).** "Chunking Strategies to Improve LLM RAG Pipeline Performance." [https://weaviate.io/blog/chunking-strategies-for-rag](https://weaviate.io/blog/chunking-strategies-for-rag) — Guía práctica: overlap 10-20%, selección de tamaño por tipo de query.

#### Embeddings

20. **Ailog RAG. (2026).** "Best Embedding Models 2025: MTEB Scores & Leaderboard." [https://app.ailog.fr/en/blog/guides/choosing-embedding-models](https://app.ailog.fr/en/blog/guides/choosing-embedding-models) — Cohere embed-v4 (65.2), OpenAI text-embedding-3-large (64.6), BGE-M3 (63.0). Scores MTEB no predicen bien rendimiento en retrieval.

21. **Hugging Face / MTEB.** "MTEB: Massive Text Embedding Benchmark Leaderboard." [https://huggingface.co/spaces/mteb/leaderboard](https://huggingface.co/spaces/mteb/leaderboard) — Benchmark canónico para evaluación de modelos de embedding.

#### Filosofía y lecciones de producción

22. **McKinley, D. (2015, actualizado 2025).** "Choose Boring Technology." [https://mcfunley.com/choose-boring-technology](https://mcfunley.com/choose-boring-technology) — Fundamento filosófico: "innovation tokens" limitados. Usa PostgreSQL por default.

23. **Timescale/Medium. (2025).** "Stop Over-Engineering AI Apps: The Case for Boring Technologies." [https://medium.com/timescale/stop-over-engineering-ai-apps-the-case-for-boring-technologies-cbf12a09ec3e](https://medium.com/timescale/stop-over-engineering-ai-apps-the-case-for-boring-technologies-cbf12a09ec3e) — PostgreSQL, BM25 y pipelines establecidos como default antes de vector DBs dedicados.

24. **Towards Data Science. (2024).** "Six Lessons Learned Building RAG Systems in Production." [https://towardsdatascience.com/six-lessons-learned-building-rag-systems-in-production/](https://towardsdatascience.com/six-lessons-learned-building-rag-systems-in-production/) — 42% de fallos por calidad de datos. Chunking strategy como decisión de mayor apalancamiento.

25. **kapa.ai. (2024).** "RAG Best Practices: Lessons from 100+ Technical Teams." [https://www.kapa.ai/blog/rag-best-practices](https://www.kapa.ai/blog/rag-best-practices) — Lecciones de 100+ equipos: metadata filtering, reranking, evaluación, tuning específico de dominio.

- **"Designing Data-Intensive Applications"** - Martin Kleppmann
- **RAGAS:** framework de evaluación para RAG
- Posts del blog: "Bases de datos para LLMs", "Bases de datos para series de tiempo", "Guía para escoger tu stack"
