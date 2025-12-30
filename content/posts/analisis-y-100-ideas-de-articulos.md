---
title: "Análisis editorial y 100 ideas de artículos (<1000 palabras)"
description: "Mapa de temas del canal y 100 ideas accionables, listas para escribir en menos de 1000 palabras."
draft: true
---

# Objetivo

Romper bloqueo creativo con: (1) análisis de líneas editoriales actuales, (2) formatos exprés para posts cortos y (3) 100 ideas concretas, alineadas con los temas y audiencia del canal.

# Análisis editorial (qué ya cubre el canal)

- Arquitectura y diseño: APoSD, SOLID, modularidad, REST, separación en capas, claridad.
- Ciencias de la computación y lenguajes: compiladores/intérpretes, motores JS, Go, TypeScript, Elixir, Rust, OCaml, Lean/Agda.
- Sistemas: concurrencia, asincronía, buffers, networking (HTTP 1.1/2/3), performance.
- Datos: fundamentos, DDIA, TSDB (borrador), DuckDB (borrador), modelado.
- Seguridad/cripto: hashes, MAC, aleatoriedad, introducciones prácticas.
- IA/LLM: LangChain, agentes, transformadores, selección de lecturas.
- Productividad/aprendizaje: Zettelkasten, creatividad, libros esenciales, patrones de aprendizaje.

# Formatos exprés (<1000 palabras)

- 3×3: 3 decisiones, 3 trade‑offs, 3 errores, con un mini ejemplo.
- FAQ de 5 preguntas: respuestas claras + snippet/diagrama mínimo.
- Checklist accionable: 7–10 ítems con criterio de verificación.
- “Una decisión, sus consecuencias”: 500–700 palabras con 1 diagrama.
- Mini receta técnica: problema → pasos → pitfalls → cómo validar.

# 100 ideas de artículos (agrupadas por tema)

## A. Arquitectura y diseño (15)

1) Checklist de NFRs en 15 minutos — prioriza 5 atributos y define escenarios medibles; formato checklist.
2) Tu primer ADR en 10 minutos — plantilla mínima y ejemplo real; cuándo cerrar/deprecar.
3) C4 rápido para tu producto — contenedores clave, responsabilidades, 3 riesgos y mitigaciones.
4) Anti‑patrones de arquitectura que veo a diario — 5 síntomas, costo oculto y corrección inmediata.
5) Decisiones reversibles vs irreversibles — heurísticas, ejemplos y cómo tratarlas en PRs.
6) Monolito modular vs microservicios — cuándo sí/no, señales y migración prudente.
7) Qué documentar de verdad en arquitectura — ADRs, escenarios de calidad y diagramas con intención.
8) Asegurando operabilidad desde el diseño — métricas, health checks, trazas y presupuestos de error.
9) Diseñar para cambios de requisitos — puntos de variación, límites de contexto y antifrágil.
10) Trade‑offs de caching en arquitectura — dónde colocar cachés y cómo invalidarlas sin dolor.
11) Organizando la documentación viva — docs‑as‑code, cadencias y responsables.
12) “Arquitectura por moda” y cómo evitarla — criterios, riesgos y preguntas incómodas.
13) Costos ocultos de la complejidad accidental — señales, medición y poda dirigida.
14) Escoger límites de contexto en 5 pasos — señales de dominio, cohesión y cambios coordinados.
15) Atributos de calidad que más impactan negocio — latencia, disponibilidad, seguridad, costo.

## B. Diseño de sistemas (12)

16) 5 decisiones con mayor impacto — datos compartidos, colas, idempotencia, cachés, particionamiento.
17) Colas vs eventos vs streams — latencia, orden, entrega, mantenimiento.
18) Idempotencia bien aplicada — claves, ventanas de tiempo, deduplicación y auditoría.
19) Diseña para picos ×10 — shed, límites, pre‑warming, degradación elegante.
20) Acotar blast radius — particionado lógico, límites de permisos y circuit breakers.
21) Outbox y consistencia — patrón, esquema mínimo y reintentos seguros.
22) Retries con jitter y presupuestos — cuándo reintentar, backoff y timeouts coordinados.
23) Backpressure en pipelines — señales, propagación y amortiguadores.
24) Versionado de contratos entre servicios — compatibilidad, feature flags, migraciones.
25) Observabilidad centrada en flujos — trazas de casos críticos y métricas por etapa.
26) Gestión de claves y secretos en sistemas distribuidos — rotación, scopes y auditoría.
27) Estrategias de caché multi‑capa — CDN, edge, app, DB; invalidación segura.

## C. Datos y bases de datos (12)

28) Elegir una TSDB en 5 preguntas — cardinalidad, ingestión, retención, compresión, ecosistema.
29) DuckDB para análisis local — 7 recetas prácticas y validación de resultados.
30) Índices: cuándo, cuál y por qué — B‑Tree, Hash, GIN; patrones de consulta.
31) Modelado de datos: 5 trampas comunes — IDs, fechas, normalizar vs desnormalizar, soft‑delete, auditoría.
32) Consistencia eventual sin dolor — dónde aplica, reconciliación y tolerancia a duplicados.
33) Particionamiento efectivo — por rango/hash, hotspots, métricas para ajustar.
34) Esquemas evolutivos — migraciones con cero downtime y control de versiones.
35) Diseñar catálogos que escalan — filtrado, orden estable y paginación cursor.
36) Minimizar costo en la capa de datos — índices que sobran, compresión y almacenamiento frío.
37) Data contracts entre equipos — esquemas, linaje y validación automática.
38) Estrategias de caching para lecturas pesadas — materialización, TTL, invalidación por evento.
39) Diseñar auditoría y cumplimiento desde el esquema — trazabilidad, retenciones y RGPD.

## D. Concurrencia y sistemas (12)

40) Buffers y backpressure explicados — señales de saturación, tamaños y límites prácticos.
41) Async: 4 patrones que sí necesitas — fan‑out/in, pipelines, cancelación, timeouts.
42) Timeouts y presupuestos coordinados — desde frontend a DB con números concretos.
43) Circuit breakers sin frameworks — implementación mínima y métricas clave.
44) Planificar capacidad sin adivinar — throughput objetivo, percentiles y márgenes.
45) Reintentos que no rompen todo — idempotencia, jitter, límites y dead letters.
46) Memoria y leaks en servicios — patrones de uso, perfiles y límites por contenedor.
47) Control de concurrencia a alto nivel — colas, semáforos, pools y fairness.
48) Programación dirigida por latencia — mapear rutas calientes, targets p95/p99.
49) Manejo de reloj y tiempo — monotonic vs wall clock, expiraciones y ventanas.
50) Plan de degradación controlada — modos “lite”, cola de espera y mensajes claros.
51) Arranque y apagado seguros — ganchos, drenado de tráfico y persistencia.

## E. APIs y plataforma web (10)

52) Versionado de APIs sin drama — semver, rutas, flags y comunicación.
53) Paginación que escala — offset vs cursor, orden estable y límites.
54) Idempotencia en APIs de pagos — claves, expiración, replays y reconciliación.
55) Rate limits efectivos — token bucket, identidad, 429 con hints.
56) Errores como parte del contrato — códigos, dominios de error y retriables.
57) Webhooks confiables — entrega al menos‑una‑vez, firma y reintentos.
58) Documenta APIs que sí se usan — ejemplos útiles, curl/HTTPie y casos límite.
59) Seguridad pragmática en APIs — authn/z, scopes, rotación y secretos.
60) HTTP/3 para devs — QUIC, impacto en latencia y debugging básico.
61) Testing de contratos entre servicios — esquemas, generadores y CI.

## F. IA/LLMs en práctica (10)

62) Memoria de agentes: opciones mínimas — episódica, vector, herramientas e índices.
63) Guardrails para LLMs — validadores, límites de tokens, políticas y evals.
64) Bases vectoriales sin hype — dimensiones, filtros, latencia, costo.
65) Sistemas híbridos reglas+LLM — orquestación, fallback y pruebas.
66) Evaluación de prompts como código — datasets, métricas y CI.
67) Recuperación aumentada de contexto (RAG) — chunking con sentido y ranking.
68) Observabilidad para LLMs — trazas, costos por llamada y cuotas.
69) Calidad y seguridad en respuestas — detección de alucinaciones y firmas.
70) Patrones de herramientas (tool use) — diseño de funciones y límites.
71) Cómo elegir modelos hoy — latencia, costo, contexto, privacidad y SLA.

## G. Programación funcional y lenguajes (10)

72) Óptica (lentes) con ejemplos cotidianos — get/set, composición y validación.
73) Patrones de composición en Elixir — pipelines, behaviours y supervisión mínima.
74) OCaml en 30 minutos útiles — pattern matching, módulos y cuándo conviene.
75) Rust vs Go: propiedad y mutabilidad — concurrencia y envío de mensajes.
76) TypeScript más seguro — tipos para errores, brand types y narrowings.
77) Motores JS en la práctica — JIT, perfiles y “cuando te afecta”.
78) Intérprete vs compilador — impacto en DX, performance y herramientas.
79) Lean/Agda: cuándo valen la pena — dominios críticos y prototipos formales.
80) Composición sobre herencia, de verdad — ejemplos con límites y trade‑offs.
81) Errores como valores — diseño de APIs con resultado explícito.

## H. Seguridad y criptografía (7)

82) Hashes: el mínimo que debes saber — sal, costo y migración de contraseñas.
83) MAC vs firmas — cuándo usar cada una y errores comunes.
84) Cifrado en reposo y en tránsito — claves, rotación y escopos.
85) Gestión de secretos para devs — vaults, inyección y auditoría.
86) Threat modeling en 30 minutos — activos, actores, mitigaciones.
87) Tokens: JWT vs alternativas — expiración, revocación y scopes.
88) Seguridad pragmática en pipelines CI/CD — secretos, artefactos y firmas.

## I. Productividad y aprendizaje (7)

89) Zettelkasten para devs — notas atómicas, backlinks y repaso espaciado.
90) Cómo leer DDIA sin atascarte — ruta, ejercicios y resúmenes.
91) Ultralearning aplicado a devs — mapa de habilidades y proyectos.
92) Cómo preparar charlas técnicas — guion, demos y anti‑sorpresas.
93) Documentación que se lee — patrones, tono y ejemplos mínimos.
94) Mejora tu code review — checklist, sesgos y feedback útil.
95) Estrategias de aprendizaje en equipo — guilds, katas y rotación.

## J. DevOps y observabilidad (5)

96) Métricas que importan — SLI/SLO, p95/p99 y alertas con intención.
97) Logging útil — niveles, trazabilidad de requests y sampling.
98) Tracing distribuido sin dolor — spans clave y budgets de muestreo.
99) Health checks de verdad — readiness, liveness y manejo de fallas.
100) Postmortems que enseñan — 5 preguntas y acciones con dueño.

# Siguientes pasos

- Elige 3–5 ideas y convierto cada una en outline con front matter en `_drafts` hoy mismo.
- Si prefieres mini‑serie, propongo NFRs → ADRs → C4 como secuencia, cada una <1000 palabras con plantillas.

---

# Serie: HPC con GPU (CUDA, Triton, PyTorch, Gluon/MXNet) — 20 artículos

Formato por post (<1000 palabras): qué y por qué, 1–2 conceptos clave, práctica guiada, pitfalls y una “entrega” (gist/Colab). Requisitos mínimos: GPU con drivers CUDA 12.x, CUDA Toolkit, nvcc, PyTorch con CUDA, Triton (pip). Sin GPU: usar Colab con GPU.

1) Mapa del terreno: por qué GPU y HPC
- Objetivo: entender cuándo conviene GPU y qué cubrirá la serie.
- Práctica: identificar tareas candidatas (cómputo denso, paralelismo regular, poco branching).
- Entrega: checklist de “síntomas GPU” aplicado a tu proyecto actual.

2) Setup sin dolor: drivers, CUDA Toolkit y verificación
- Objetivo: dejar el entorno listo (nvcc, PyTorch CUDA, Triton).
- Práctica: `nvidia-smi`, `deviceQuery`, `torch.cuda.is_available()`; validar compatibilidades.
- Troubleshooting: drivers incompatibles, WSL2 en Windows, fallback a CPU, versiones CUDA/PyTorch.
- Entrega: reporte breve de versiones y propiedades del dispositivo.

3) Tensores en GPU con PyTorch: lo esencial
- Objetivo: mover datos y medir CPU vs GPU.
- Práctica: `to(device)`, `dtype`, pinned memory; diferencia transferencia vs cómputo.
- Entrega: micro‑benchmark elementwise y conclusiones.

4) Triton 101: tu primer kernel (suma de vectores)
- Objetivo: escribir y lanzar un kernel en Triton.
- Práctica: kernel de suma; bloques, grid; medir speedup.
- Entrega: gist con kernel y timings reproducibles.

5) Triton 102: transformaciones elementwise y broadcasting
- Objetivo: kernels expresivos sin perder legibilidad.
- Práctica: normalización, activaciones, clamp; tamaños de bloque.
- Entrega: comparativa vs PyTorch nativo y cuándo usar Triton.

6) CUDA C++ 101: tu primer kernel “a mano”
- Objetivo: compilar, lanzar y depurar un kernel básico.
- Práctica: vector add con configuración de lanzamiento; chequeo de errores CUDA.
- Entrega: proyecto mínimo con `nvcc` y resultados.

7) CUDA: hilos, bloques, warps e indexación segura
- Objetivo: dominar el modelo de ejecución e indexado.
- Práctica: stride loops; límites; validación de resultados.
- Entrega: patrón de indexación reusable con pruebas.

8) Memoria GPU: global, shared, constant y coalescing
- Objetivo: maximizar throughput con acceso ordenado.
- Práctica: copia strided vs coalesced; efecto en ancho de banda.
- Entrega: gráfico simple de throughput vs patrón de acceso.

9) Reducciones en GPU: sumas a escala
- Objetivo: reducción eficiente con memoria compartida.
- Práctica: naive vs reducción en árbol; atomics vs shared.
- Entrega: comparación de latencias y error numérico.

10) Scan (prefix sum): base de muchos algoritmos
- Objetivo: implementar exclusive scan estilo Blelloch.
- Práctica: upsweep/downsweep; casos borde; validación.
- Entrega: pruebas con tamaños grandes y aleatorios.

11) Matmul I: baseline ingenuo
- Objetivo: entender el costo y límites del naive.
- Práctica: kernel naive; medir FLOPS efectivos y techo teórico.
- Entrega: baseline para futuras optimizaciones.

12) Roofline model: límites teóricos de tu GPU
- Objetivo: entender cuándo estás limitado por memoria vs cómputo.
- Práctica: calcular arithmetic intensity; ubicar kernels en el modelo; identificar cuellos de botella.
- Entrega: gráfico roofline con tus kernels y análisis de oportunidades.

13) Matmul II: tiling y shared memory
- Objetivo: reuso de datos para rendimiento.
- Práctica: tiles, sincronización, tamaños óptimos iniciales.
- Entrega: speedup vs naive y análisis de cuellos de botella.

13) Warp‑level primitives: shuffles y reducciones por warp
- Objetivo: optimizar sin shared cuando conviene.
- Práctica: reducción por warp; combinar con shared a nivel bloque.
- Entrega: informe de latencia y uso de registros.

14) Debugging GPU: cuda-gdb, compute-sanitizer y errores típicos
- Objetivo: diagnosticar crashes, race conditions y accesos fuera de rango.
- Práctica: uso de cuda-memcheck, compute-sanitizer; patrones de error comunes.
- Entrega: checklist de debugging y casos resueltos.

15) Streams y solapamiento: esconder latencia de I/O
- Objetivo: mezclar cómputo y transferencias asíncronas.
- Práctica: dos streams, memcpy async + kernel; pinned memory.
- Entrega: timeline conceptual y mejora observada.

16) Perfilado y ocupación: Nsight Compute/Systems y heurísticas prácticas
- Objetivo: medir lo correcto: occupancy, SM util, DRAM throughput, warp stalls.
- Práctica: Nsight Compute para kernels, Nsight Systems para timeline; nvprof está deprecado.
- Interpretación: identificar métricas clave (achieved occupancy, memory throughput, SOL%).
- Entrega: tabla de cuellos de botella y plan de optimización priorizado.

17) CuBLAS/cuDNN: cuándo librerías ganan (y cómo envolver)
- Objetivo: usar librerías de alto rendimiento sin reescribir la rueda.
- Práctica: `cublasSgemm`; layout/leading dims; verificar precisión.
- Entrega: criterio simple "lib vs kernel propio" por caso de uso.

18) Extensiones CUDA para PyTorch: custom ops con autograd
- Objetivo: integrar kernels en PyTorch con gradientes.
- Práctica: extensión C++/CUDA mínima; `backward` custom o aproximado.
- Entrega: módulo instalable y ejemplo de entrenamiento.

19) Triton avanzada: reducción y matmul con heurísticas
- Objetivo: usar Triton para kernels de mayor rendimiento.
- Práctica: reducción en Triton; matmul con tiling configurable.
- Entrega: benchmark vs PyTorch y notas de tuning.

20) JAX/XLA y TensorRT: compilación y deployment optimizado
- Objetivo: entender compilación ahead-of-time y optimizaciones para inferencia.
- Práctica: exportar modelo PyTorch a ONNX/TensorRT; comparar con JAX/XLA JIT.
- Entrega: tabla de trade‑offs (flexibilidad vs rendimiento) y casos de uso.

21) Mixed precision y Tensor Cores: rendimiento real
- Objetivo: usar FP16/BF16 de forma segura.
- Práctica: AMP en PyTorch; validación de estabilidad; cuándo usar Tensor Cores.
- Nota: gradient checkpointing para memoria vs velocidad.
- Entrega: speedup real con tolerancia de error documentada.

22) Caso de estudio end-to-end: training loop optimizado
- Objetivo: integrar múltiples técnicas en un problema real.
- Práctica: dataset custom, dataloaders, custom kernels, mixed precision, profiling iterativo.
- Entrega: código completo, comparación baseline vs optimizado, lecciones aprendidas.
