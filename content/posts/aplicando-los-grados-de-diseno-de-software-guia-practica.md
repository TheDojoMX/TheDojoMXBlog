---
title: "Aplicando los grados de diseño de software: guía práctica"
author: "Héctor Patricio"
tags: ['diseño-de-software', 'arquitectura-de-software', 'diseño-de-sistemas']
description: "El diseño de software en práctica: artefactos, ejemplos, checklists y ejercicios para llevar a la práctica los cuatro niveles de diseño"
draft: true
---

> Este artículo es una continuación práctica del post [“Los diferentes grados de diseño de software”](/2024/10/19/los-diferentes-grados-de-diseno-de-software.html). Aquí bajamos las ideas a artefactos, decisiones, ejemplos y checklists aplicables.

## Introducción

En el artículo pasado, presentamos una taxonomía de los grados de diseño de software,
entendiendo como "grado" qué tan lejos estamos de la implementación en código. En este
artículo presentamos una forma de practicar cada uno de esos niveles.

Usaremos un _caso guía_ para ilustrarlo: una plataforma de cursos en línea con suscriptores,
catálogo, pagos y video bajo demanda.

## Mapa rápido de los niveles (qué, cómo y entregables)

- Arquitectura de soluciones: propósito, contexto, restricciones y grandes decisiones de “qué construir y por qué”.
- Arquitectura de software: atributos de calidad priorizados y decisiones estructurales para lograrlos.
- Diseño de sistemas: topología, datos, contratos y estrategias de escala/fiabilidad.
- Diseño de código: organización de módulos, APIs, patrones, pruebas y mantenibilidad.

- Entregables típicos por nivel: diagrama (C4), ADRs, escenarios de calidad, contratos API, diagramas de secuencia, esquemas de datos, checklists.

## Caso guía: “Plataforma para Cursos” (contexto y restricciones)

- Público objetivo: 50k usuarios activos/mes; picos en lanzamientos (x10).
- Requerimientos clave: catálogo, reproducción, pagos, comentarios, búsqueda, recomendaciones básicas.
- Restricciones: presupuesto acotado, time-to-market corto, privacidad/regulación, equipo de 6 devs.
- Métricas de éxito: activación, retención, conversión, SLO 99.9%, p95 < 200 ms en catálogo.

## Nivel 1 — Arquitectura de soluciones en práctica

- Entradas: objetivos de negocio, riesgos, presupuesto, compliance, capacidades del equipo.
- Decisiones: build vs buy, alcance MVP, dependencias externas, estrategia de datos/soberanía.
- Artefactos: mapa de stakeholders, objetivos medibles, mapa de capacidades, riesgos/mitigaciones, roadmap.
- Validación: suposiciones críticas, experimentos, hitos de negocio, costos estimados.
- Anti‑patrones: decidir por moda tecnológica, ignorar restricciones legales, no definir éxito.
- Ejercicio: redacta 3 objetivos y 5 riesgos con mitigación y criterio de éxito.

## Nivel 2 — Arquitectura de software (en práctica)

- Atributos de calidad como escenarios: latencia, disponibilidad (SLO/SLA), RPO/RTO, seguridad, operabilidad.
- ADRs iniciales: monolito modular vs microservicios; sincronía vs asíncronía; caching y colas; observabilidad.
- Diagramas C4 (Nivel 2): contenedores, responsabilidades y relaciones; límites de contexto.
- Análisis de trade‑offs: riesgos, sensibilidad, decisiones reversibles/irreversibles (ATAM lite).
- Operabilidad: métricas, trazas, logs, health checks; presupuestos de error.
- Anti‑patrones: confundir arquitectura con elección de framework, ignorar NFRs, sobre‑ingeniería.
- Ejercicio: escribe 5 escenarios de calidad priorizados y 2 ADRs que los ataquen.

## Nivel 3 — Diseño de sistemas (en práctica)

- Componentes y contratos: APIs, idempotencia, versionado, límites, cuotas y rate limits.
- Datos: modelo lógico, consistencia (fuerte/eventual), indexación, particionamiento, retención, GDPR.
- Flujos: diagramas de secuencia para inscripción, pago y entrega de contenido; compensaciones.
- Escala y resiliencia: cachés, colas, circuit breakers, backpressure, replicación/backup.
- Capacidad y costos: throughput objetivo, picos, dimensionamiento inicial, límites de proveedores.
- Anti‑patrones: “copiar recetas” sin casos de uso, ignorar backpressure, subestimar datos.
- Ejercicio: diagrama de secuencia de “compra + acceso” y definición de 3 contratos API.

## Nivel 4 — Diseño de código (en práctica)

- Organización: módulos por dominio (bounded contexts), ports & adapters, vertical slices vs capas.
- APIs y errores: contratos claros, invariantes, tipado útil, errores como parte del contrato.
- Pruebas: unitarias por invariantes, de contratos, de propiedades, contract testing entre servicios.
- Calidad continua: métricas de acoplamiento/cohesión, límites de complejidad, linters, migraciones seguras.
- No funcionales en código: performance (perfiles), seguridad (entrada, secretos), observabilidad (trazas/metrics).
- Anti‑patrones: “patrones por patrón”, nombres vagos, pruebas frágiles, mocks excesivos.
- Ejercicio: define límites de módulo para “catálogo” y “pagos”, más 3 contratos por módulo.

## Integración entre niveles y gobernanza

- Alineación top‑down/back‑propagation: cambios en NFRs deben reflejarse en ADRs, C4 y código.
- Documentación viva: docs‑as‑code, ADRs con cadencia, golden paths, tech radar interno.
- Revisiones: arquitectura trimestral, decisiones reversibles en PRs, métricas de calidad/operabilidad.

## Checklists rápidas por nivel

- Soluciones: objetivos claros, restricciones explícitas, riesgos priorizados, criterios de éxito, roadmap.
- Arquitectura de software: NFRs como escenarios, ADRs, C4 L2, observabilidad, trade‑offs documentados.
- Sistemas: contratos definidos, secuencias críticas modeladas, decisiones de datos, mecanismos de resiliencia.
- Código: límites de módulo, contratos de API, estrategia de pruebas, métricas de calidad, seguridad/observabilidad.

## Plantillas (para reutilizar)

- ADR (resumen): contexto, decisión, alternativas, consecuencias, fecha, estado.
- Escenario de calidad: estímulo, fuente, entorno, artefacto, respuesta, medida.
- C4: pautas para L1–L3 y convenciones de iconografía; enlaces de referencia.

## Lecturas recomendadas (complementarias)

- Team Topologies (Conway aplicado): estructura de equipos alineada a flujo.
- Accelerate: prácticas de entrega que correlacionan con desempeño.
- Release It!: patrones de resiliencia en producción.
- Site Reliability Engineering: SLOs, presupuestos de error y operabilidad.

## Siguientes pasos

- Aplica las plantillas a tu sistema actual; empieza por 3 ADRs y 5 NFRs medibles.
- Dibuja un C4 L2 y un diagrama de secuencia del flujo más crítico.
- Revisa trimestralmente NFRs vs métricas de producción y actualiza decisiones.
