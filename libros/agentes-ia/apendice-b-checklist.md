# Apendice B: Checklist Completo de Produccion

Este checklist consolida todos los controles discutidos a lo largo del libro en una referencia unica, organizada por fase de deployment. Cada item incluye su identificador, descripcion y el capitulo de referencia.

No todos los items aplican a todos los agentes. Un chatbot interno de baja criticidad puede omitir la verificacion formal y el sandboxing. Un agente que ejecuta transacciones financieras necesita cada uno de ellos. La regla general: **el nivel de rigor debe ser proporcional al impacto de un fallo**.

---

## Fase 1: Pre-Deploy (Antes del despliegue)

### Diseno y definicion

- [ ] **DEF-01**: Definicion PEAS documentada (performance, environment, actuators, sensors). (Cap. 1)
- [ ] **DEF-02**: Alcance del agente definido explicitamente: que puede hacer y que NO puede hacer. (Cap. 1)
- [ ] **DEF-03**: Modelo de amenazas documentado: superficie de ataque mapeada. (Cap. 9)
- [ ] **DEF-04**: Presupuesto de contexto calculado: tokens asignados a cada componente (system prompt, datos, historial, razonamiento). (Cap. 5)

### Seguridad

- [ ] **SEC-01**: Principio de minimo privilegio implementado. El agente solo tiene acceso a herramientas y datos estrictamente necesarios. (Cap. 8)
- [ ] **SEC-02**: Confirmacion humana requerida para acciones irreversibles (DELETE, DROP, transacciones financieras, envio de emails). (Cap. 8)
- [ ] **SEC-03**: Input guardrails activos: deteccion de prompt injection, validacion de formato, filtrado de contenido, limites de tamano. (Cap. 8)
- [ ] **SEC-04**: Output guardrails activos: validacion de formato de salida, deteccion de datos sensibles (PII), coherencia. (Cap. 8)
- [ ] **SEC-05**: Contratos tipados con validacion semantica para todas las interfaces agente-herramientas y agente-agente. (Cap. 10)
- [ ] **SEC-06**: Sandboxing para ejecucion de codigo: contenedor efimero sin acceso a red ni filesystem del host. (Cap. 8)
- [ ] **SEC-07**: API keys en secrets manager, rotacion automatica, nunca en codigo fuente. (Cap. 9)
- [ ] **SEC-08**: Datos sensibles nunca en el system prompt. (Cap. 9)
- [ ] **SEC-09**: Separacion de privilegios: el agente que lee datos NO es el mismo que ejecuta acciones destructivas. (Cap. 9)
- [ ] **SEC-10**: Defensa en profundidad: al menos 3 capas de defensa independientes para cada vector de ataque. (Cap. 9)

### Testing

- [ ] **TST-01**: Unit tests para componentes deterministicos (parsers, validadores, guardrails). (Cap. 11)
- [ ] **TST-02**: Integration tests con mocks del LLM. (Cap. 11)
- [ ] **TST-03**: End-to-end tests con LLM real para flujos criticos. (Cap. 11)
- [ ] **TST-04**: Evaluaciones (evals) con dataset de al menos 50 casos. (Cap. 11)
- [ ] **TST-05**: Property-based tests para invariantes de seguridad (e.g., "nunca ejecuta rm -rf", "siempre escala a humano cuando confianza < umbral"). (Cap. 11)
- [ ] **TST-06**: Red teaming completado y documentado: prompt injection directo e indirecto, jailbreaking, exfiltracion de datos. (Cap. 11)
- [ ] **TST-07**: Tests de carga para la concurrencia esperada. (Cap. 11)
- [ ] **TST-08**: Tests de regresion para prompts (ejecutar evals tras cada cambio de prompt). (Cap. 11)

### Resiliencia

- [ ] **RES-01**: Circuit breaker configurado: corta al detectar loops, consumo excesivo de tokens o tiempo excesivo. (Cap. 8)
- [ ] **RES-02**: Fallback a modo deterministico cuando el LLM falla o el circuit breaker se activa. (Cap. 8, 14)
- [ ] **RES-03**: Timeouts configurados en cada capa: llamadas al LLM, herramientas, bases de datos, flujo completo. (Cap. 14)
- [ ] **RES-04**: Reintentos con backoff exponencial y jitter para errores transitorios (429, 500, timeouts). (Cap. 14)
- [ ] **RES-05**: Idempotencia en acciones criticas: ejecutar la misma accion dos veces produce el mismo resultado. (Cap. 14)
- [ ] **RES-06**: Presupuesto de tokens por tarea con corte graceful si se excede. (Cap. 5, 8)
- [ ] **RES-07**: Graceful degradation documentada: tabla de modos de fallo con comportamiento degradado para cada componente. (Cap. 14)

---

## Fase 2: Deploy (Durante el despliegue)

### Observabilidad

- [ ] **OBS-01**: Tracing distribuido configurado: un trace con span por cada paso (razonamiento, tool call, validacion). (Cap. 14)
- [ ] **OBS-02**: Metricas clave exportadas: latencia (p50/p95/p99), tokens por tarea, costo por tarea, tasa de exito, tasa de fallback. (Cap. 14)
- [ ] **OBS-03**: Logging estructurado en cada paso: JSON con trace_id, paso del agente, tokens consumidos, decision tomada. (Cap. 14)
- [ ] **OBS-04**: Audit log inmutable: toda accion del agente queda registrada en un log append-only. (Cap. 8, 9)
- [ ] **OBS-05**: Health check endpoint que verifica conectividad con LLM provider, base de datos y servicios dependientes. (Cap. 14)

### Costos

- [ ] **CST-01**: Presupuesto diario/mensual definido con alertas al 50% y 80%. (Cap. 14)
- [ ] **CST-02**: Model router implementado: consultas simples dirigidas a modelo economico, consultas complejas a modelo capable. (Cap. 14)
- [ ] **CST-03**: Cache de respuestas para consultas repetitivas. (Cap. 14)
- [ ] **CST-04**: Dashboard de costos con desglose por flujo, usuario y agente. (Cap. 14)

### Operaciones

- [ ] **OPS-01**: Deployment con capacidad de rollback (canario o blue-green). (Cap. 14)
- [ ] **OPS-02**: Rate limiting por usuario y por agente. (Cap. 8)
- [ ] **OPS-03**: Versionado de prompts: cada cambio de prompt es un artefacto versionado y desplegado con el mismo rigor que el codigo. (Cap. 14)
- [ ] **OPS-04**: Plan de respuesta a incidentes documentado: quien es notificado, como se desactiva el agente, como se recupera. (Cap. 14)

---

## Fase 3: Post-Deploy (Operacion continua)

### Monitoreo continuo

- [ ] **MON-01**: Alertas configuradas para: circuit breaker trips, costos anormales, degradacion de calidad, errores consecutivos. (Cap. 14)
- [ ] **MON-02**: Metricas de negocio vinculadas: correlacion entre metricas del agente y metricas de negocio (tasa de resolucion, satisfaccion del usuario). (Cap. 14)
- [ ] **MON-03**: Capacidad de replay: poder reproducir una ejecucion pasada con los mismos inputs para debugging. (Cap. 14)
- [ ] **MON-04**: Retention de logs definida: logs detallados 30 dias, metricas agregadas 1 ano, audit logs indefinido. (Cap. 14)

### Mejora continua

- [ ] **MEJ-01**: Revision mensual de costos vs valor generado (ROI). (Cap. 14)
- [ ] **MEJ-02**: Ejecucion periodica de la suite de evals para detectar degradacion por cambios de modelo. (Cap. 11)
- [ ] **MEJ-03**: Actualizacion de la base de conocimiento con casos nuevos (memoria episodica). (Cap. 6)
- [ ] **MEJ-04**: Re-ejecucion de red teaming tras cambios significativos en el sistema o el modelo. (Cap. 11)

---

**Total: 48 items.** Marca como N/A los que no apliquen a tu caso, con justificacion documentada. Los que aplican, verificalos antes de cada despliegue.

---
