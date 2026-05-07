---
title: "Patrones de diseño para sistemas con IA"
date: 2026-02-15
author: "Héctor Patricio"
tags: ['diseño-de-software', 'patrones', 'design-patterns', 'IA', 'llm', 'agentes', 'arquitectura', 'aposd']
description: "Exploramos los patrones de diseño emergentes para sistemas basados en LLMs y agentes de IA, y los comparamos con los patrones clásicos de diseño de software."
featuredImage: ""
draft: true
---

<!-- Palabra estimada total: ~3500-4000 palabras -->

En artículos anteriores hemos analizado a fondo los principios de diseño de software
a través de la serie sobre "A Philosophy of Software Design", los principios SOLID
y los patrones clásicos del GoF. Ahora, con la proliferación de sistemas basados en
LLMs y agentes de IA, han surgido patrones de diseño nuevos que merecen el mismo
análisis riguroso. En este artículo examinaremos los patrones más importantes,
los compararemos con sus equivalentes clásicos y discutiremos cuándo usarlos y
cuándo NO usarlos.

## ¿Por qué necesitamos nuevos patrones?

<!-- ~400 palabras -->

Los sistemas basados en IA tienen características fundamentalmente diferentes
al software tradicional: las respuestas son no deterministas, la latencia es
variable e impredecible, los costos escalan con el uso de tokens, y los errores
son sutiles (una respuesta incorrecta puede parecer correcta). Estas características
requieren patrones que manejen incertidumbre, costos y calidad de forma explícita.
Conectar con el concepto de complejidad del libro "A Philosophy of Software Design":
los sistemas con IA introducen nuevas formas de complejidad que debemos manejar con
módulos profundos y buenas abstracciones.

### El principio fundamental: separar la inteligencia de la lógica

<!-- ~200 palabras -->

El error más común al construir sistemas con IA es mezclar llamadas a LLMs con
la lógica de negocio. El principio rector debe ser tratar al LLM como un componente
más, aislado detrás de interfaces claras. Conectar con el principio de ocultamiento
de información de Parnas y la serie de APOSD del blog.

## Patrón 1: Orquestador-Trabajador (Orchestrator-Worker)

<!-- ~500 palabras -->

### Descripción y mecánica

<!-- ~250 palabras -->

Un LLM central actúa como orquestador: analiza la tarea, la descompone en subtareas
y las delega a agentes especializados (otros LLMs o herramientas). El orquestador
sintetiza los resultados. Diagrama del flujo. Ejemplo concreto: un sistema de
análisis de código donde el orquestador delega a un agente de seguridad, uno de
rendimiento y uno de estilo.

### Comparación con patrones clásicos

<!-- ~250 palabras -->

Relación directa con el patrón **Mediator** del GoF: un objeto central coordina
la comunicación entre objetos que no se conocen entre sí. También tiene elementos
del patrón **Facade**: oculta la complejidad de múltiples subsistemas detrás de
una interfaz simple. Diferencia clave: en el patrón clásico, el mediador sigue
reglas deterministas; aquí, el orquestador toma decisiones basándose en entendimiento
semántico. Ventajas: modularidad, especialización. Desventajas: latencia acumulada,
punto único de fallo.

## Patrón 2: Router (Enrutador de modelos)

<!-- ~500 palabras -->

### Descripción y mecánica

<!-- ~250 palabras -->

Un clasificador (puede ser un LLM pequeño, un modelo de clasificación, o reglas
heurísticas) evalúa cada consulta entrante y la envía al modelo más apropiado.
Consultas simples van a modelos pequeños y baratos; consultas complejas van a
modelos grandes y costosos. Reportes de la industria muestran reducciones de
costo del 60-70% sin pérdida significativa de calidad. Ejemplo: en un chatbot
de soporte, preguntas frecuentes van a un modelo de 7B, pero preguntas técnicas
complejas van a GPT-4 o Claude.

### Comparación con patrones clásicos

<!-- ~250 palabras -->

Directamente análogo al patrón **Strategy**: define una familia de algoritmos
(modelos) y hace que sean intercambiables. También tiene elementos de **Chain
of Responsibility**: la consulta pasa por una cadena que decide quién la maneja
(referenciar el post del blog sobre este patrón). La diferencia: en Strategy
clásico, el cliente elige la estrategia; aquí, un clasificador la elige
automáticamente basándose en el contenido. Métricas clave: costo por consulta,
latencia p95, tasa de escalación incorrecta.

## Patrón 3: Cascada con fallbacks (Cascading with Deterministic Fallbacks)

<!-- ~400 palabras -->

### Descripción y mecánica

<!-- ~200 palabras -->

Cuando un LLM falla o tarda demasiado, el sistema cae a un fallback determinista.
Estructura de tres niveles: LLM principal con timeout agresivo -> LLM secundario
más rápido -> respuesta determinista basada en reglas o plantillas. Ejemplo: un
sistema de generación de respuestas de email: Claude -> GPT-4-mini -> plantilla
predefinida basada en keywords.

### Cuándo usar y cuándo no

<!-- ~200 palabras -->

Usar cuando la disponibilidad es más importante que la calidad perfecta. Usar en
sistemas de producción donde un "no respondo" es inaceptable. NO usar cuando la
calidad de la respuesta es crítica (diagnósticos médicos, asesoría legal). El
antipatrón: usar el fallback como excusa para no mejorar el sistema principal.
Conectar con el principio de Ousterhout de "define errores fuera de existencia".

## Patrón 4: Evaluador-Optimizador (Evaluator-Optimizer)

<!-- ~500 palabras -->

### Descripción y mecánica

<!-- ~250 palabras -->

Un LLM genera una respuesta o solución; otro LLM la evalúa y proporciona
retroalimentación; el primer LLM itera hasta alcanzar un umbral de calidad.
Es un ciclo de generación-evaluación que puede repetirse N veces. Ejemplo:
generación de código donde un modelo escribe el código, otro lo revisa, y el
primero corrige basándose en la revisión. Variante: el evaluador puede ser un
conjunto de tests automatizados en lugar de otro LLM.

### Comparación con patrones clásicos

<!-- ~250 palabras -->

Relación con el patrón **Observer**: el evaluador observa la salida del generador
y reacciona. También se parece al patrón **Builder** iterativo: construye la
respuesta incrementalmente con validación en cada paso. Conexión profunda con la
fase "verificar" de la heurística de Polya: ¿puedes verificar el resultado?
¿puedes obtener el resultado de otra forma? El Evaluador-Optimizador automatiza
este paso. Riesgos: bucles infinitos, costo multiplicado, y la trampa de que
dos LLMs estén de acuerdo en algo incorrecto.

## Cuándo NO usar patrones de IA

<!-- ~400 palabras -->

### El antipatrón del LLM como martillo

<!-- ~200 palabras -->

No todo requiere un LLM. Si el problema tiene una solución determinista clara,
usa código tradicional. Ejemplos de sobreingeniería con IA: usar un LLM para
validar formatos de email, para parsear JSON, para hacer cálculos aritméticos.
La regla: si puedes escribirlo en menos de 50 líneas de código con tests, no
necesitas un LLM.

### Complejidad accidental vs esencial en sistemas con IA

<!-- ~200 palabras -->

Conectar con "A Philosophy of Software Design": cada capa de IA añade complejidad.
La complejidad esencial es la que viene del problema (entender lenguaje natural,
generar texto coherente). La complejidad accidental es la que nosotros añadimos
por malas decisiones de diseño (orquestar 5 agentes donde bastaría uno, usar
un LLM donde una regex funciona). Criterio: si la complejidad del sistema de IA
supera la complejidad del problema original, estás sobreingenierando.

## Una taxonomía para elegir el patrón correcto

<!-- ~300 palabras -->

Tabla de decisión basada en las características del problema: determinismo
requerido (alto/bajo), tolerancia a latencia (alta/baja), presupuesto
(limitado/amplio), criticidad de la respuesta (alta/baja). Mapear cada
combinación al patrón más adecuado. Incluir el caso "no uses IA" como
opción válida. Recordar que los patrones se pueden combinar: un Router
que envía a un pipeline con Evaluador-Optimizador para las consultas
complejas.

## Conclusión

<!-- ~200 palabras -->

Los patrones de diseño para sistemas con IA son una extensión natural de los
patrones clásicos, adaptados a las particularidades del software no determinista.
El principio rector sigue siendo el mismo que Ousterhout y los autores clásicos
nos enseñan: reducir la complejidad, crear abstracciones profundas y separar
responsabilidades. La IA no cambia los fundamentos del buen diseño de software;
los extiende.

---

## Resumen de investigación

Los patrones de diseño para sistemas de IA han madurado rápidamente entre 2023-2026. Tres laboratorios principales — Anthropic, OpenAI y Google — publicaron guías para practicantes que convergen en un vocabulario compartido, mientras trabajo académico ha catalogado estos patrones con revisiones rigurosas de literatura.

**El canon convergente.** Anthropic (diciembre 2024) define cinco patrones composables de workflow: Prompt Chaining, Routing, Parallelization, Orchestrator-Workers, y Evaluator-Optimizer. Google ADK (Cloud NEXT 2025) publica ocho patrones incluyendo Sequential Pipeline, Coordinator/Dispatcher, Parallel Fan-Out/Gather, y Generator-Critic. Martin Fowler y Bharani Subramaniam (Thoughtworks, febrero 2025) complementan con patrones orientados a producción: Evals, Hybrid Retriever, Query Rewriting, Reranker y Guardrails.

**El patrón Router como área de investigación independiente.** RouteLLM (LMSYS/ICLR 2025) demostró que routers entrenados reducen costos de inferencia hasta 85% manteniendo 95% de la calidad de GPT-4. El patrón Strategy del GoF subyace directamente: cada modelo o prompt es un algoritmo intercambiable.

**Los patrones GoF clásicos siguen siendo el sustrato.** Heiland et al. (CAIN 2023) catalogaron 70 patrones para sistemas de IA, encontrando que 36 son adaptaciones de patrones tradicionales de ingeniería de software. Chain of Responsibility mapea a pipelines de guardrails y middleware. Observer recure en monitoreo, telemetría y feedback loops.

**Los principios de Ousterhout aplican directamente.** "Módulos profundos con interfaces simples" es violado por el anti-patrón de wrappers superficiales de LLM. "Ocultamiento de información" mapea a encapsular detalles de prompt engineering detrás de interfaces limpias de agentes.

---

### Referencias y fuentes clave

#### Guías de patrones de los labs principales

1. **Anthropic. (2024).** "Building Effective Agents." [https://www.anthropic.com/research/building-effective-agents](https://www.anthropic.com/research/building-effective-agents) — Guía canónica: 5 patrones composables (Prompt Chaining, Routing, Parallelization, Orchestrator-Workers, Evaluator-Optimizer). Distingue workflows de agentes autónomos. Enfatiza simplicidad sobre frameworks complejos.

2. **Google. (2025).** "Developer's Guide to Multi-Agent Patterns in ADK." [https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) — 8 patrones con ejemplos de código: Sequential Pipeline, Coordinator/Dispatcher, Parallel Fan-Out/Gather, Hierarchical Decomposition, Generator-Critic, Iterative Refinement, Human-in-the-Loop, Composite.

3. **OpenAI. (2024).** "Swarm: Educational Framework for Multi-Agent Orchestration." [https://github.com/openai/swarm](https://github.com/openai/swarm) — Framework ligero basado en "routines" y "handoffs". Demuestra el patrón Orchestrator-Worker en su forma más simple. Supersedido por OpenAI Agents SDK.

4. **Subramaniam, B. & Fowler, M. (2025).** "Emerging Patterns in Building GenAI Products." *Thoughtworks*. [https://martinfowler.com/articles/gen-ai-patterns/](https://martinfowler.com/articles/gen-ai-patterns/) — Patrones validados en producción: Evals, Embeddings, RAG, Hybrid Retriever, Query Rewriting, Reranker, Guardrails. Aborda el problema de no-determinismo explícitamente.

5. **AWS Prescriptive Guidance. (2024-2025).** "Agentic AI Patterns and Workflows on AWS." [https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html) — Patrones enterprise-grade: Orchestrator, Evaluator Reflect-Refine Loop, Saga Orchestration, Human-in-the-Loop.

6. **Microsoft Azure Architecture Center. (2024-2025).** "AI Agent Orchestration Patterns." [https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) — Orchestrator-worker, routing, paralelización con guía de implementación Azure-specific.

#### Patrones específicos (papers académicos)

7. **Ong, I., et al. (2024/2025).** "RouteLLM: Learning to Route LLMs with Preference Data." *ICLR 2025*. [https://arxiv.org/abs/2406.18665](https://arxiv.org/abs/2406.18665) — Routers entrenados con datos de preferencia humana: 85% reducción de costos manteniendo 95% de calidad GPT-4 en MT Bench.

8. **Madaan, A., et al. (2023).** "Self-Refine: Iterative Refinement with Self-Feedback." *NeurIPS 2023*. [https://arxiv.org/abs/2303.17651](https://arxiv.org/abs/2303.17651) — Paper fundacional del Evaluator-Optimizer: un LLM como generador, evaluador y refinador en loop iterativo. ~20% mejora absoluta en 7 tareas.

9. **Asai, A., et al. (2024).** "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection." *ICLR 2024*. [https://arxiv.org/abs/2310.11511](https://arxiv.org/abs/2310.11511) — RAG adaptativo con tokens de reflexión. Base del patrón Evaluator-Optimizer y Agentic RAG.

10. **Shi, X., et al. (2024).** "Corrective Retrieval Augmented Generation (CRAG)." [https://arxiv.org/abs/2401.15884](https://arxiv.org/abs/2401.15884) — Evaluador de retrieval con acciones correctivas: implementa Guard/Validator en la etapa de recuperación.

11. **Siriwardhana, S., et al. (2025).** "Agentic Retrieval-Augmented Generation: A Survey." [https://arxiv.org/abs/2501.09136](https://arxiv.org/abs/2501.09136) — Survey de la intersección agentes + RAG: reflexión, planning, tool use y colaboración multi-agente en pipelines de retrieval.

#### Survey académico y catálogo

12. **Heiland, L., Hauser, M. & Bogner, J. (2023).** "Design Patterns for AI-based Systems: A Multivocal Literature Review." *CAIN 2023*. [https://arxiv.org/abs/2303.13173](https://arxiv.org/abs/2303.13173) — Survey más riguroso: 51 fuentes, 70 patrones únicos, 36 son adaptaciones de patrones clásicos de software. Categorías: arquitectura (25), deployment (16), implementación (9), seguridad (9).

13. **Huang, K. (2025).** "LLM Design Patterns: A Practical Guide." *Packt Publishing*. [https://www.packtpub.com/en-us/product/llm-design-patterns-9781836207023](https://www.packtpub.com/en-us/product/llm-design-patterns-9781836207023) — Tratamiento más completo en formato libro: prompt engineering, RAG, tool use, patrones agénticos, fine-tuning, RLHF, fairness.

#### Guardrails y anti-patrones

14. **OWASP GenAI Security Project. (2024).** "OWASP Top 10 for LLM Applications 2025." [https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) — Catálogo autoritativo de anti-patrones de seguridad: Prompt Injection, Sensitive Information Disclosure, Excessive Agency. Motiva directamente el patrón Guard/Validator.

15. **Guardrails AI. (2025).** "Guardrails Index." [https://github.com/guardrails-ai/guardrails](https://github.com/guardrails-ai/guardrails) — Implementación open-source del patrón Guard/Validator. Primer benchmark (febrero 2025) comparando 24 guardrails en 6 categorías de riesgo. Abstracción Guard-Validator-RAIL implementa Chain of Responsibility del GoF.

16. **Bowne-Anderson, H. (2024).** "Patterns and Anti-Patterns for Building with LLMs." [https://medium.com/marvelous-mlops/patterns-and-anti-patterns-for-building-with-llms-42ea9c2ddc90](https://medium.com/marvelous-mlops/patterns-and-anti-patterns-for-building-with-llms-42ea9c2ddc90) — Anti-patrones recurrentes: sobre-ingeniería con frameworks multi-agente, prompts monolíticos, exposición cruda de APIs, ausencia de evaluaciones.

17. **Glaforge, G. (2025).** "AI Agentic Patterns and Anti-Patterns." [https://glaforge.dev/talks/2025/12/02/ai-agentic-patterns-and-anti-patterns/](https://glaforge.dev/talks/2025/12/02/ai-agentic-patterns-and-anti-patterns/) — Patrones positivos y modos de falla lado a lado: sobre-dependencia de frameworks, sub-especificación de tareas, checkpoints de supervisión humana faltantes.

#### Clásicos de diseño de software

18. **Ousterhout, J. (2018, 2nd ed. 2021).** "A Philosophy of Software Design." [https://web.stanford.edu/~ouster/cgi-bin/aposd.php](https://web.stanford.edu/~ouster/cgi-bin/aposd.php) — Principios directamente aplicables: módulos profundos con interfaces simples, ocultamiento de información, diseño alrededor de errores. El anti-patrón de wrappers superficiales de LLM viola "deep modules".

19. **Gamma, E., Helm, R., Johnson, R. & Vlissides, J. (1994).** "Design Patterns: Elements of Reusable Object-Oriented Software." (GoF) — Strategy = Router LLM; Chain of Responsibility = pipeline de guardrails; Observer = telemetría y feedback; Decorator = wrappers de LLM aumentados (memoria, tools, retrieval).

20. **Polya, G. (1945).** "How to Solve It." — Las cuatro fases (entender, planear, ejecutar, verificar) mapean al Evaluator-Optimizer: "¿puedes verificar el resultado? ¿puedes obtenerlo de otra forma?"

- Posts del blog: serie "A Philosophy of Software Design", "Patrón de diseño: Cadena de responsabilidad", "Patrones de diseño: qué son y cuándo usarlos", "El principio abierto/cerrado", "¿Qué son los agentes inteligentes?"
