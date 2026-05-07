# Capitulo 14: De la Demo al Deploy -- Ingenieria de Produccion

> "El mercado de agentes de IA se proyecta a $52 mil millones para 2030. Pero Gartner predice que mas del 40% de proyectos agenticos seran cancelados para finales de 2027 por costos escalantes y ROI incierto. La diferencia entre los que sobreviven y los que no esta en la ingenieria."

---

En los capitulos anteriores construimos patrones de diseno, harnesses, contratos tipados, suites de testing, protocolos de comunicacion y sistemas multi-agente. Tenemos todas las piezas. Ahora toca responder la pregunta que separa a los prototipos de los sistemas que generan valor: como llevas todo esto a produccion?

La distancia entre una demo que impresiona en una reunion y un sistema que atiende usuarios reales las 24 horas del dia es un abismo. Ese abismo no se cruza con mas prompts ni con modelos mas grandes. Se cruza con ingenieria: checklists rigurosos, monitoreo continuo, estrategias de deployment que permitan rollback, gestion de versiones de prompts y control de costos desde el dia uno.

Este capitulo es el manual de operaciones. No hay teoria nueva. Es la aplicacion disciplinada de todo lo que hemos construido, orientada a un solo objetivo: que tu agente funcione de forma confiable, observable y economicamente viable en el mundo real.

---

## 14.1 El abismo entre demo y produccion

### Lo que funciona en la demo

En la demo, el agente tiene un prompt cuidadosamente pulido que funciona para los tres casos de prueba que preparaste. La latencia no importa porque esperas pacientemente. Los costos no importan porque son centavos. No hay usuarios concurrentes. No hay datos reales con formatos inesperados. No hay adversarios intentando romper el sistema.

### Lo que falla en produccion

En produccion, todo lo anterior se invierte:

- **Variabilidad de inputs.** Los usuarios escriben con errores, en multiples idiomas, con formatos inesperados. El prompt que funcionaba en la demo falla con el 20% de los inputs reales.
- **Concurrencia.** Cientos de usuarios simultaneos significan cientos de llamadas al LLM, cada una con latencia variable y costo acumulativo.
- **Costos acumulativos.** Un agente que cuesta $0.05 por ejecucion y se ejecuta 10,000 veces al dia genera una factura de $15,000 mensuales. Agentes no optimizados pueden costar $10-$100 por sesion [Moltbook-AI, 2026].
- **Degradacion silenciosa.** El modelo se actualiza y su comportamiento cambia. Un prompt que funcionaba deja de funcionar sin que nadie se de cuenta.
- **Seguridad bajo ataque.** Usuarios maliciosos intentan prompt injection, exfiltracion de datos y abuso del sistema.

La estadistica es reveladora: los precios de tokens de modelos frontier cayeron de $30 por millon de tokens en el lanzamiento de GPT-4 en 2023 a menos de $3 por millon para modelos comparables en Q1 de 2026, y los modelos economicos estan por debajo de $0.15 por millon [Silicon Data, 2026]. Pero incluso con precios mas bajos, los costos se desbordan sin control porque los agentes consumen tokens de forma multiplicativa en cada paso del loop agentico.

---

## 14.2 El checklist de produccion

Antes de desplegar cualquier agente, revisa este checklist. Cada item referencia el capitulo donde se explica en detalle.

### Seguridad (15 items)

```python
"""
Checklist de seguridad pre-despliegue para agentes de IA.
Cada item debe verificarse antes de pasar a produccion.
"""

SECURITY_CHECKLIST = {
    # --- Permisos y acceso ---
    "SEC-01": {
        "item": "Principio de minimo privilegio implementado",
        "description": "El agente solo tiene acceso a las herramientas y datos "
                       "estrictamente necesarios para su tarea.",
        "capitulo_ref": "Cap. 8 (Harness)",
        "verificacion": "Revisar AgentPermissions: sin permisos comodin (*)",
    },
    "SEC-02": {
        "item": "Confirmacion humana para acciones irreversibles",
        "description": "Toda accion que modifique datos, envie emails o ejecute "
                       "transacciones financieras requiere aprobacion humana.",
        "capitulo_ref": "Cap. 8 (HITL), Cap. 13 (Human-in-the-Loop)",
        "verificacion": "Test E2E: intentar accion destructiva sin aprobacion -> bloqueada",
    },
    "SEC-03": {
        "item": "Input guardrails activos",
        "description": "Deteccion de prompt injection, validacion de formato, "
                       "filtrado de contenido, limites de tamano.",
        "capitulo_ref": "Cap. 8 (Guardrails)",
        "verificacion": "Ejecutar suite de red teaming (Cap. 11)",
    },
    "SEC-04": {
        "item": "Output guardrails activos",
        "description": "Validacion de formato de salida, deteccion de datos "
                       "sensibles (PII), coherencia, seguridad.",
        "capitulo_ref": "Cap. 8 (Guardrails)",
        "verificacion": "Verificar que PII nunca aparece en respuestas",
    },
    "SEC-05": {
        "item": "Contratos tipados con validacion semantica",
        "description": "Pydantic models con validadores custom para todas las "
                       "interfaces entre agentes y herramientas.",
        "capitulo_ref": "Cap. 10 (Contratos Tipados)",
        "verificacion": "100% de interfaces cubiertas con modelos Pydantic",
    },
    "SEC-06": {
        "item": "Sandboxing para ejecucion de codigo",
        "description": "Si el agente genera o ejecuta codigo, lo hace en un "
                       "contenedor efimero sin acceso a red ni filesystem del host.",
        "capitulo_ref": "Cap. 8 (Sandboxing)",
        "verificacion": "Test: intento de acceso a filesystem host -> denegado",
    },
    "SEC-07": {
        "item": "Audit log inmutable",
        "description": "Toda accion del agente queda registrada en un log que "
                       "no puede ser modificado ni eliminado.",
        "capitulo_ref": "Cap. 8 (Observabilidad), Cap. 9 (Seguridad)",
        "verificacion": "Log append-only verificado",
    },
    "SEC-08": {
        "item": "Rate limiting por usuario y por agente",
        "description": "Limites de peticiones por minuto/hora para prevenir "
                       "abuso y costos desbordados.",
        "capitulo_ref": "Cap. 8 (Rate Limiters)",
        "verificacion": "Test: exceder limite -> error 429",
    },
    "SEC-09": {
        "item": "API keys rotadas y sin hardcodear",
        "description": "Credenciales en secrets manager, rotacion automatica, "
                       "nunca en codigo fuente.",
        "capitulo_ref": "Cap. 9 (Seguridad)",
        "verificacion": "Escaneo de repositorio con herramientas de deteccion de secretos",
    },
    "SEC-10": {
        "item": "Red teaming completado",
        "description": "Suite de ataques ejecutada: prompt injection directo e "
                       "indirecto, jailbreaking, exfiltracion de datos.",
        "capitulo_ref": "Cap. 11 (Red Teaming)",
        "verificacion": "Reporte de red teaming documentado y hallazgos remediados",
    },
    "SEC-11": {
        "item": "Defensa en profundidad implementada",
        "description": "Multiples capas de proteccion independientes, asumiendo "
                       "que cada una puede ser evadida.",
        "capitulo_ref": "Cap. 9 (Seguridad)",
        "verificacion": "Al menos 3 capas de defensa para cada vector de ataque",
    },
    "SEC-12": {
        "item": "Datos sensibles nunca en el prompt",
        "description": "El system prompt no contiene API keys, contrasenas ni "
                       "datos de clientes reales.",
        "capitulo_ref": "Cap. 9 (OWASP Top 10)",
        "verificacion": "Revision manual del system prompt",
    },
    "SEC-13": {
        "item": "Modelo de amenazas documentado",
        "description": "Superficie de ataque mapeada: prompt del sistema, datos "
                       "de RAG, herramientas, datos de entrenamiento.",
        "capitulo_ref": "Cap. 9 (Modelo de Amenazas)",
        "verificacion": "Documento de modelo de amenazas revisado por equipo",
    },
    "SEC-14": {
        "item": "Separacion de privilegios entre herramientas",
        "description": "El agente que lee datos NO es el mismo que ejecuta "
                       "acciones destructivas.",
        "capitulo_ref": "Cap. 9 (Seguridad para Agentes Multi-herramienta)",
        "verificacion": "Verificar aislamiento de herramientas de lectura vs escritura",
    },
    "SEC-15": {
        "item": "Plan de respuesta a incidentes con agentes",
        "description": "Procedimiento documentado para cuando el agente falla: "
                       "quien es notificado, como se desactiva, como se recupera.",
        "capitulo_ref": "Este capitulo (14.4)",
        "verificacion": "Simulacro de incidente ejecutado",
    },
}
```

### Observabilidad (8 items)

```python
OBSERVABILITY_CHECKLIST = {
    "OBS-01": {
        "item": "Tracing distribuido configurado",
        "description": "Cada ejecucion del agente genera un trace con span por "
                       "cada paso: razonamiento, tool call, validacion.",
        "verificacion": "Ejecutar flujo completo y verificar trace en dashboard",
    },
    "OBS-02": {
        "item": "Metricas clave exportadas",
        "description": "Latencia (p50/p95/p99), tokens por tarea, costo por "
                       "tarea, tasa de exito, tasa de fallback.",
        "verificacion": "Dashboard con las 5 metricas visibles",
    },
    "OBS-03": {
        "item": "Logging estructurado en cada paso",
        "description": "Logs en JSON con trace_id, paso del agente, tokens "
                       "consumidos, decision tomada.",
        "verificacion": "Query de logs por trace_id retorna flujo completo",
    },
    "OBS-04": {
        "item": "Alertas configuradas",
        "description": "Alertas para: circuit breaker trips, costos anormales, "
                       "degradacion de calidad, errores consecutivos.",
        "verificacion": "Simular cada condicion de alerta y verificar notificacion",
    },
    "OBS-05": {
        "item": "Metricas de negocio vinculadas",
        "description": "Conectar metricas del agente con metricas de negocio: "
                       "tasa de resolucion, satisfaccion del usuario, NPS.",
        "verificacion": "Dashboard con correlacion agente <-> negocio",
    },
    "OBS-06": {
        "item": "Retention de logs definida",
        "description": "Politica de retencion: logs detallados 30 dias, "
                       "metricas agregadas 1 ano, audit logs indefinido.",
        "verificacion": "Politica documentada y aplicada",
    },
    "OBS-07": {
        "item": "Capacidad de replay de ejecuciones",
        "description": "Poder reproducir una ejecucion pasada del agente con "
                       "los mismos inputs para debugging.",
        "verificacion": "Replay de 3 ejecuciones recientes exitoso",
    },
    "OBS-08": {
        "item": "Health check endpoint",
        "description": "Endpoint /health que verifica conectividad con LLM "
                       "provider, base de datos, y servicios dependientes.",
        "verificacion": "Curl al endpoint retorna estado de cada dependencia",
    },
}
```

### Resiliencia (7 items)

```python
RESILIENCE_CHECKLIST = {
    "RES-01": {
        "item": "Circuit breaker configurado",
        "description": "Corta ejecucion al detectar: loops de razonamiento, "
                       "consumo excesivo de tokens, tiempo excesivo.",
        "verificacion": "Test: agente en loop -> circuit breaker corta en < 30s",
    },
    "RES-02": {
        "item": "Fallback a modo deterministico",
        "description": "Cuando el LLM falla o el circuit breaker se activa, "
                       "el sistema cae a reglas deterministicas.",
        "verificacion": "Test: LLM no disponible -> respuesta deterministica",
    },
    "RES-03": {
        "item": "Timeouts configurados en cada capa",
        "description": "Timeout para llamadas al LLM, herramientas, bases de "
                       "datos, y para el flujo completo del agente.",
        "verificacion": "Verificar timeouts en configuracion",
    },
    "RES-04": {
        "item": "Reintentos con backoff exponencial",
        "description": "Errores transitorios (429, 500, timeouts) se reintentan "
                       "con backoff exponencial y jitter.",
        "verificacion": "Test: error 429 -> reintento con delay creciente",
    },
    "RES-05": {
        "item": "Idempotencia en acciones criticas",
        "description": "Ejecutar la misma accion dos veces produce el mismo "
                       "resultado (previene duplicados por retry).",
        "verificacion": "Test: ejecutar accion 2 veces -> resultado identico",
    },
    "RES-06": {
        "item": "Presupuesto de tokens por tarea",
        "description": "Limite maximo de tokens por ejecucion del agente. "
                       "Si se excede, la ejecucion se detiene gracefully.",
        "verificacion": "Test: tarea costosa -> corte en limite de tokens",
    },
    "RES-07": {
        "item": "Graceful degradation documentada",
        "description": "Para cada componente que puede fallar, esta documentado "
                       "que pasa y cual es el comportamiento degradado.",
        "verificacion": "Tabla de modos de fallo completa",
    },
}
```

### Testing (8 items)

```python
TESTING_CHECKLIST = {
    "TST-01": "Unit tests para componentes deterministicos (parsers, validadores)",
    "TST-02": "Integration tests con mocks del LLM",
    "TST-03": "End-to-end tests con LLM real para flujos criticos",
    "TST-04": "Evaluations (evals) con dataset de al menos 50 casos",
    "TST-05": "Property-based tests para invariantes de seguridad",
    "TST-06": "Red teaming completado y documentado",
    "TST-07": "Tests de carga para concurrencia esperada",
    "TST-08": "Tests de regresion para prompts (ejecutar evals tras cada cambio)",
}
```

### Costos (5 items)

```python
COST_CHECKLIST = {
    "CST-01": "Presupuesto diario/mensual definido con alertas al 50% y 80%",
    "CST-02": "Model router implementado (consultas simples -> modelo barato)",
    "CST-03": "Cache de respuestas para consultas repetitivas",
    "CST-04": "Dashboard de costos con desglose por flujo/usuario/agente",
    "CST-05": "Revision mensual de costos vs valor generado (ROI)",
}
```

Este checklist tiene 43 items. No todos aplican a todos los agentes. Un chatbot interno de baja criticidad puede omitir la verificacion formal y el sandboxing. Un agente que ejecuta transacciones financieras necesita cada uno de ellos. La regla general: **el nivel de rigor debe ser proporcional al impacto de un fallo** (ver Capitulo 10, seccion 10.5).

---

## 14.3 Monitoreo y alertas para agentes

### Por que el monitoreo tradicional no alcanza

Los agentes de IA tienen propiedades que el monitoreo de aplicaciones web tradicionales no captura:

1. **No determinismo.** La misma entrada puede producir diferentes salidas. Un error HTTP 200 no significa que la respuesta sea correcta.
2. **Costos por token.** A diferencia de una peticion HTTP que cuesta lo mismo sin importar el contenido, el costo de una llamada al LLM depende del numero de tokens procesados.
3. **Latencia variable.** La latencia depende de la longitud del contexto, la carga del proveedor, y el numero de pasos del agente. P95 puede ser 10x mayor que P50.
4. **Calidad como metrica.** No basta con que el agente responda; importa *que tan bien* responde. Esto requiere evaluaciones automatizadas que van mas alla de codigos de estado.

Empresas con agentes en produccion reportan que el monitoreo adecuado previene el 80% de los incidentes antes de que lleguen a los usuarios [AI-AgentsPlus, 2026].

### Las metricas que importan

```python
"""
Sistema de metricas para agentes en produccion.
Integra con OpenTelemetry para exportacion a cualquier backend.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import time
from typing import Optional
from contextlib import contextmanager


class AgentOutcome(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    FALLBACK = "fallback"          # Cayo a modo deterministico
    CIRCUIT_BREAKER = "circuit_breaker"  # Circuit breaker lo detuvo
    TIMEOUT = "timeout"
    BUDGET_EXCEEDED = "budget_exceeded"


@dataclass
class AgentExecutionMetrics:
    """Metricas de una ejecucion individual del agente."""
    trace_id: str
    agent_id: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    outcome: Optional[AgentOutcome] = None

    # Tokens
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0

    # Costo
    cost_usd: float = 0.0

    # Latencia
    total_latency_ms: float = 0.0
    llm_latency_ms: float = 0.0
    tool_latency_ms: float = 0.0

    # Pasos del agente
    reasoning_steps: int = 0
    tool_calls: int = 0
    guardrail_rejections: int = 0

    # Calidad (si hay evaluador automatico)
    quality_score: Optional[float] = None

    @property
    def tokens_per_step(self) -> float:
        if self.reasoning_steps == 0:
            return 0.0
        return self.total_tokens / self.reasoning_steps

    @property
    def cost_per_step(self) -> float:
        if self.reasoning_steps == 0:
            return 0.0
        return self.cost_usd / self.reasoning_steps


@dataclass
class AgentAggregateMetrics:
    """Metricas agregadas para dashboard de monitoreo."""
    period_start: datetime
    period_end: datetime
    total_executions: int = 0
    successful: int = 0
    failed: int = 0
    fallbacks: int = 0
    circuit_breaker_trips: int = 0
    timeouts: int = 0
    budget_exceeded: int = 0

    # Latencia
    latency_p50_ms: float = 0.0
    latency_p95_ms: float = 0.0
    latency_p99_ms: float = 0.0

    # Costos
    total_cost_usd: float = 0.0
    avg_cost_per_execution: float = 0.0
    total_tokens: int = 0

    # Calidad
    avg_quality_score: Optional[float] = None

    @property
    def success_rate(self) -> float:
        if self.total_executions == 0:
            return 0.0
        return self.successful / self.total_executions

    @property
    def fallback_rate(self) -> float:
        if self.total_executions == 0:
            return 0.0
        return self.fallbacks / self.total_executions


class AgentMonitor:
    """Monitor central para agentes en produccion.

    Recopila metricas de cada ejecucion y calcula agregados.
    En produccion, exporta a OpenTelemetry, Datadog o Prometheus.
    """

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self._executions: list[AgentExecutionMetrics] = []
        self._alert_rules: list[dict] = []

    def add_alert_rule(
        self,
        name: str,
        condition: str,
        threshold: float,
        window_minutes: int = 5,
        action: str = "notify",
    ) -> None:
        """Registra una regla de alerta.

        Args:
            name: nombre descriptivo de la alerta
            condition: metrica a evaluar (success_rate, cost_rate, latency_p95)
            threshold: umbral que dispara la alerta
            window_minutes: ventana de tiempo para evaluar
            action: accion a tomar (notify, page, disable_agent)
        """
        self._alert_rules.append({
            "name": name,
            "condition": condition,
            "threshold": threshold,
            "window_minutes": window_minutes,
            "action": action,
        })

    @contextmanager
    def track_execution(self, trace_id: str):
        """Context manager para rastrear una ejecucion del agente.

        Uso:
            with monitor.track_execution("trace-123") as metrics:
                metrics.input_tokens = 500
                metrics.output_tokens = 200
                # ... ejecutar agente ...
                metrics.outcome = AgentOutcome.SUCCESS
        """
        metrics = AgentExecutionMetrics(
            trace_id=trace_id,
            agent_id=self.agent_id,
            started_at=datetime.now(),
        )
        start_time = time.monotonic()
        try:
            yield metrics
        except Exception:
            metrics.outcome = AgentOutcome.FAILURE
            raise
        finally:
            metrics.ended_at = datetime.now()
            metrics.total_latency_ms = (time.monotonic() - start_time) * 1000
            metrics.total_tokens = metrics.input_tokens + metrics.output_tokens
            self._executions.append(metrics)
            self._evaluate_alerts()

    def _evaluate_alerts(self) -> None:
        """Evalua las reglas de alerta contra las metricas recientes."""
        for rule in self._alert_rules:
            window = timedelta(minutes=rule["window_minutes"])
            recent = [
                e for e in self._executions
                if e.started_at > datetime.now() - window
            ]
            if not recent:
                continue

            if rule["condition"] == "success_rate":
                successes = sum(
                    1 for e in recent if e.outcome == AgentOutcome.SUCCESS
                )
                rate = successes / len(recent)
                if rate < rule["threshold"]:
                    self._fire_alert(rule, rate)

            elif rule["condition"] == "cost_rate":
                total_cost = sum(e.cost_usd for e in recent)
                cost_per_minute = total_cost / rule["window_minutes"]
                if cost_per_minute > rule["threshold"]:
                    self._fire_alert(rule, cost_per_minute)

    def _fire_alert(self, rule: dict, current_value: float) -> None:
        """Dispara una alerta. En produccion: PagerDuty, Slack, email."""
        # Placeholder - integrar con sistema de alertas real
        print(
            f"ALERTA [{rule['name']}]: "
            f"valor actual = {current_value:.3f}, "
            f"umbral = {rule['threshold']}, "
            f"accion = {rule['action']}"
        )


# === Configuracion recomendada de alertas ===

def configure_standard_alerts(monitor: AgentMonitor) -> None:
    """Configura las alertas minimas recomendadas para produccion."""

    # Tasa de exito cae por debajo del 90%
    monitor.add_alert_rule(
        name="low_success_rate",
        condition="success_rate",
        threshold=0.90,
        window_minutes=5,
        action="page",  # Despertar a alguien
    )

    # Costos se disparan (mas de $1/minuto)
    monitor.add_alert_rule(
        name="cost_spike",
        condition="cost_rate",
        threshold=1.0,  # USD por minuto
        window_minutes=5,
        action="disable_agent",  # Cortar el agente
    )

    # Tasa de exito cae por debajo del 95% (warning)
    monitor.add_alert_rule(
        name="degraded_success_rate",
        condition="success_rate",
        threshold=0.95,
        window_minutes=15,
        action="notify",  # Slack
    )
```

### Integracion con OpenTelemetry

OpenTelemetry se ha convertido en el estandar abierto para observabilidad de agentes de IA. Su grupo de trabajo sobre IA define convenciones semanticas especificas para llamadas a LLMs, incluyendo atributos como `gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens` y `gen_ai.usage.output_tokens` [OpenTelemetry, 2025].

```python
"""
Integracion basica con OpenTelemetry para tracing de agentes.
"""

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)

# Configuracion del tracer
provider = TracerProvider()
processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint="http://localhost:4317")
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("agent-service")


async def execute_agent_with_tracing(agent, user_input: str) -> dict:
    """Ejecuta un agente con tracing de OpenTelemetry.

    Cada paso del agente genera un span hijo, permitiendo
    visualizar el flujo completo en Jaeger, Grafana Tempo, etc.
    """
    with tracer.start_as_current_span(
        "agent.execute",
        attributes={
            "agent.id": agent.agent_id,
            "agent.input_length": len(user_input),
        },
    ) as root_span:
        # Paso 1: Razonamiento
        with tracer.start_as_current_span("agent.reason") as reason_span:
            reasoning = await agent.reason(user_input)
            reason_span.set_attribute(
                "gen_ai.usage.input_tokens", reasoning.input_tokens
            )
            reason_span.set_attribute(
                "gen_ai.usage.output_tokens", reasoning.output_tokens
            )
            reason_span.set_attribute(
                "gen_ai.request.model", reasoning.model_used
            )

        # Paso 2: Tool calls (si las hay)
        for tool_call in reasoning.tool_calls:
            with tracer.start_as_current_span(
                f"agent.tool.{tool_call.name}"
            ) as tool_span:
                result = await agent.execute_tool(tool_call)
                tool_span.set_attribute("tool.name", tool_call.name)
                tool_span.set_attribute("tool.success", result.success)
                tool_span.set_attribute(
                    "tool.latency_ms", result.latency_ms
                )

        # Paso 3: Respuesta final
        with tracer.start_as_current_span("agent.respond"):
            response = await agent.generate_response(reasoning)

        root_span.set_attribute("agent.outcome", "success")
        root_span.set_attribute("agent.total_steps", reasoning.total_steps)
        root_span.set_attribute(
            "agent.total_tokens", reasoning.total_tokens
        )

        return response
```

### Herramientas de observabilidad en 2026

El ecosistema de observabilidad para agentes ha madurado significativamente:

- **Langfuse** (open source): tracing, evaluaciones, analytics de prompts. Self-hosteable. Buena opcion para equipos que quieren control total.
- **Braintrust**: evaluaciones y monitoreo con enfoque en calidad de respuestas. Fuerte en A/B testing de prompts.
- **Arize Phoenix** (open source): tracing y evaluaciones con integracion nativa de OpenTelemetry.
- **LangSmith** (LangChain): tracing, evaluaciones y monitoreo integrado con LangGraph. La opcion natural si ya usas el ecosistema LangChain.
- **OpenTelemetry + Grafana/Jaeger**: la solucion mas flexible. Requiere mas configuracion pero te da control total y evita vendor lock-in.

La recomendacion: comienza con OpenTelemetry como capa de instrumentacion (es un estandar abierto) y elige el backend segun tus necesidades. Si ya usas Grafana, exporta ahi. Si necesitas evaluaciones integradas, considera Langfuse o Braintrust.

---

## 14.4 Estrategias de deployment para agentes

### El problema: los agentes no son microservicios normales

Un microservicio web tradicional es deterministico: la misma entrada produce la misma salida. Puedes hacer un blue-green deployment, verificar que los tests pasan y tener confianza en que el nuevo release funciona.

Un agente no es deterministico. La misma entrada puede producir diferentes salidas. Peor aun: un cambio en el prompt puede mejorar el 80% de los casos y empeorar el 20% restante. Los tests pasan, pero la calidad degrada para un subconjunto de usuarios que no estaba cubierto en el dataset de evaluacion.

Esto requiere estrategias de deployment adaptadas.

### Blue-green para agentes

El deployment blue-green mantiene dos entornos identicos: "blue" (produccion actual) y "green" (nueva version). El trafico se redirige de uno a otro de forma atomica.

Para agentes, el blue-green se adapta asi:

```python
"""
Configuracion de deployment blue-green para agentes.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Environment(Enum):
    BLUE = "blue"
    GREEN = "green"


@dataclass
class AgentDeploymentConfig:
    """Configuracion de un deployment de agente."""
    environment: Environment
    prompt_version: str
    model: str
    model_version: str
    harness_config_version: str
    guardrails_version: str
    tools_version: str
    deployed_at: str
    health_check_passed: bool = False
    eval_score: Optional[float] = None  # Resultado de evals automaticas


class BlueGreenDeployer:
    """Deployment blue-green para agentes.

    El flujo es:
    1. Deploy nueva version en entorno inactivo (green)
    2. Ejecutar health checks
    3. Ejecutar suite de evaluaciones automaticas
    4. Si pasan, cambiar trafico a green
    5. Monitorear metricas durante ventana de observacion
    6. Si todo bien, green se convierte en el nuevo blue
    7. Si algo falla, rollback inmediato al blue original
    """

    def __init__(self):
        self.active: Environment = Environment.BLUE
        self.configs: dict[Environment, Optional[AgentDeploymentConfig]] = {
            Environment.BLUE: None,
            Environment.GREEN: None,
        }

    async def deploy_to_inactive(
        self, config: AgentDeploymentConfig
    ) -> bool:
        """Deploy al entorno inactivo."""
        inactive = self._get_inactive()
        config.environment = inactive

        # 1. Deploy
        self.configs[inactive] = config

        # 2. Health check
        config.health_check_passed = await self._run_health_check(config)
        if not config.health_check_passed:
            return False

        # 3. Evaluaciones automaticas
        config.eval_score = await self._run_evals(config)
        min_eval_score = 0.85  # Umbral minimo de calidad
        if config.eval_score < min_eval_score:
            print(
                f"Eval score {config.eval_score:.2f} < "
                f"minimo {min_eval_score}. Deployment cancelado."
            )
            return False

        return True

    async def switch_traffic(self) -> None:
        """Cambia el trafico al entorno inactivo."""
        inactive = self._get_inactive()
        self.active = inactive
        print(f"Trafico redirigido a {self.active.value}")

    async def rollback(self) -> None:
        """Rollback al entorno anterior."""
        self.active = self._get_inactive()
        print(f"Rollback: trafico regresado a {self.active.value}")

    def _get_inactive(self) -> Environment:
        if self.active == Environment.BLUE:
            return Environment.GREEN
        return Environment.BLUE

    async def _run_health_check(self, config: AgentDeploymentConfig) -> bool:
        """Verifica que el agente responde correctamente."""
        # En produccion: llamada real al endpoint de health
        return True

    async def _run_evals(self, config: AgentDeploymentConfig) -> float:
        """Ejecuta la suite de evaluaciones automaticas."""
        # En produccion: ejecutar promptfoo o similar con dataset de eval
        return 0.92
```

### Canary releases para agentes

El canary release es la estrategia de menor riesgo para agentes. En lugar de redirigir todo el trafico de golpe, envia un porcentaje pequeno (2-5%) a la nueva version y monitorea.

```python
"""
Canary release para agentes: envia un porcentaje del trafico
a la nueva version y monitorea metricas de calidad.
"""

import random
from dataclasses import dataclass


@dataclass
class CanaryConfig:
    """Configuracion de canary release."""
    canary_percentage: float = 0.05  # 5% del trafico
    min_sample_size: int = 100       # Minimo de ejecuciones antes de evaluar
    quality_threshold: float = 0.90  # Score minimo de calidad
    cost_threshold_multiplier: float = 1.5  # No mas de 1.5x el costo actual
    auto_promote_at: float = 0.20    # Promover automaticamente al 20%
    auto_rollback_below: float = 0.80  # Rollback si calidad cae debajo


class CanaryRouter:
    """Router que dirige trafico entre version estable y canary."""

    def __init__(self, config: CanaryConfig):
        self.config = config
        self.canary_metrics: list[dict] = []
        self.stable_metrics: list[dict] = []

    def route(self, request_id: str) -> str:
        """Decide si una peticion va a canary o estable.

        Usa hashing del request_id para que el mismo usuario
        siempre vaya a la misma version (sticky routing).
        """
        hash_value = hash(request_id) % 100
        if hash_value < self.config.canary_percentage * 100:
            return "canary"
        return "stable"

    def record_canary_result(self, quality_score: float, cost: float) -> None:
        self.canary_metrics.append({
            "quality": quality_score,
            "cost": cost,
        })

    def record_stable_result(self, quality_score: float, cost: float) -> None:
        self.stable_metrics.append({
            "quality": quality_score,
            "cost": cost,
        })

    def evaluate_canary(self) -> str:
        """Evalua si el canary debe promoverse, mantenerse o revertirse.

        Returns:
            "promote": aumentar porcentaje de canary
            "hold": mantener porcentaje actual (necesita mas datos)
            "rollback": revertir, el canary es peor
        """
        if len(self.canary_metrics) < self.config.min_sample_size:
            return "hold"

        canary_quality = sum(
            m["quality"] for m in self.canary_metrics
        ) / len(self.canary_metrics)
        stable_quality = sum(
            m["quality"] for m in self.stable_metrics
        ) / len(self.stable_metrics)

        canary_cost = sum(
            m["cost"] for m in self.canary_metrics
        ) / len(self.canary_metrics)
        stable_cost = sum(
            m["cost"] for m in self.stable_metrics
        ) / len(self.stable_metrics)

        # Rollback si la calidad esta muy por debajo
        if canary_quality < self.config.auto_rollback_below:
            return "rollback"

        # Rollback si los costos se disparan
        if canary_cost > stable_cost * self.config.cost_threshold_multiplier:
            return "rollback"

        # Promover si la calidad es buena
        if canary_quality >= self.config.quality_threshold:
            return "promote"

        return "hold"
```

La clave del canary para agentes: la metrica de evaluacion no es solo "responde sin errores" (como en un microservicio web). Es "la calidad de las respuestas es al menos tan buena como la version anterior". Esto requiere evaluaciones automaticas en cada ejecucion, lo cual anade latencia y costo. La alternativa es evaluar una muestra y extrapolar.

### Shadow deployment (modo sombra)

Una tercera estrategia, particularmente util para cambios grandes de prompt o modelo: ejecutar la nueva version en paralelo con la version de produccion, sin que el usuario vea los resultados de la nueva version. Esto permite comparar calidad sin riesgo.

El costo es doble (ejecutas ambas versiones), pero el riesgo es cero. Util para cambios de modelo (por ejemplo, migrar de GPT-4o a Claude Sonnet) donde el comportamiento puede cambiar significativamente.

---

## 14.5 Gestion de versiones de prompts

### El problema: los prompts son codigo

Un prompt es codigo. Cambiarlo cambia el comportamiento del sistema. Pero a diferencia del codigo, los prompts rara vez tienen las mismas protecciones: no estan versionados en git, no tienen tests automatizados, y un cambio de una palabra puede degradar la calidad para un subconjunto de usuarios.

El 75% de las empresas integran IA generativa para 2026 [Getmaxim, 2026]. La necesidad de gestion sistematica de prompts es una realidad operativa, no un lujo.

### Principios de gestion de prompts

1. **Prompts en repositorio, no en base de datos.** El prompt es parte del codigo del agente. Vive en git, tiene historial, tiene code review.
2. **Versionado semantico.** Los prompts siguen semver: MAJOR (cambio de comportamiento), MINOR (mejora compatible), PATCH (correccion de typos).
3. **Evaluaciones en cada cambio.** Cada cambio de prompt ejecuta la suite de evals. Si el score baja, el cambio no pasa.
4. **Deployment desacoplado.** Puedes cambiar el prompt sin redesplegar la aplicacion. Esto permite iteracion rapida.

```python
"""
Sistema de gestion de versiones de prompts.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import hashlib
import json


@dataclass
class PromptVersion:
    """Una version especifica de un prompt."""
    prompt_id: str
    version: str              # Semver: "1.2.3"
    content: str              # El texto del prompt
    variables: list[str]      # Variables que acepta: ["user_input", "context"]
    model_target: str         # Modelo para el que fue optimizado
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = ""
    change_description: str = ""
    eval_score: Optional[float] = None
    eval_dataset_version: str = ""

    @property
    def content_hash(self) -> str:
        """Hash del contenido para detectar cambios."""
        return hashlib.sha256(self.content.encode()).hexdigest()[:12]

    def render(self, **kwargs) -> str:
        """Renderiza el prompt con las variables proporcionadas."""
        result = self.content
        for var in self.variables:
            if var in kwargs:
                result = result.replace(f"{{{{{var}}}}}", str(kwargs[var]))
        return result


@dataclass
class PromptRegistry:
    """Registro central de prompts versionados.

    En produccion, esto se respalda con un archivo YAML en el repositorio
    o con un servicio de configuracion como LaunchDarkly o Unleash.
    """
    prompts: dict[str, list[PromptVersion]] = field(default_factory=dict)
    active_versions: dict[str, str] = field(default_factory=dict)

    def register(self, version: PromptVersion) -> None:
        """Registra una nueva version de prompt."""
        if version.prompt_id not in self.prompts:
            self.prompts[version.prompt_id] = []
        self.prompts[version.prompt_id].append(version)

    def activate(self, prompt_id: str, version: str) -> None:
        """Activa una version especifica de un prompt.

        Solo debe llamarse despues de que las evaluaciones
        automaticas hayan pasado.
        """
        versions = self.prompts.get(prompt_id, [])
        matching = [v for v in versions if v.version == version]
        if not matching:
            raise ValueError(
                f"Version {version} no encontrada para {prompt_id}"
            )

        prompt_version = matching[0]
        if prompt_version.eval_score is None:
            raise ValueError(
                "No se puede activar un prompt sin evaluaciones ejecutadas"
            )
        if prompt_version.eval_score < 0.85:
            raise ValueError(
                f"Eval score {prompt_version.eval_score:.2f} < 0.85 minimo"
            )

        self.active_versions[prompt_id] = version

    def get_active(self, prompt_id: str) -> PromptVersion:
        """Obtiene la version activa de un prompt."""
        version = self.active_versions.get(prompt_id)
        if version is None:
            raise ValueError(f"No hay version activa para {prompt_id}")

        versions = self.prompts[prompt_id]
        matching = [v for v in versions if v.version == version]
        return matching[0]

    def rollback(self, prompt_id: str) -> str:
        """Rollback a la version anterior del prompt.

        Returns:
            La version a la que se hizo rollback.
        """
        versions = self.prompts.get(prompt_id, [])
        if len(versions) < 2:
            raise ValueError("No hay version anterior para rollback")

        # La penultima version
        previous = versions[-2]
        self.active_versions[prompt_id] = previous.version
        return previous.version
```

### El flujo de cambio de un prompt

1. El desarrollador modifica el prompt y hace commit en git.
2. El CI ejecuta la suite de evaluaciones (promptfoo u otra herramienta).
3. Si el eval score es >= umbral (85%), el cambio pasa code review.
4. Tras la aprobacion, el prompt se activa en el `PromptRegistry`.
5. El deployment se hace con canary: 5% del trafico usa el nuevo prompt.
6. Si las metricas de calidad se mantienen durante la ventana de observacion (ej: 2 horas), se promueve al 100%.
7. Si degradan, rollback automatico a la version anterior.

Este flujo es identico al de deployment de codigo, adaptado a la naturaleza no determinista de los prompts.

---

## 14.6 Costos en produccion y optimizacion

### La anatomia del costo de un agente

El costo de un agente no es solo el costo de la llamada al LLM. Es la suma de multiples componentes:

```
Costo total por ejecucion =
    tokens de input (system prompt + contexto + historial)
  + tokens de output (razonamiento + respuesta)
  + tokens de tool calls (N llamadas * tokens por llamada)
  + costo de embeddings (si usa RAG)
  + costo de infraestructura (compute, almacenamiento)
  + costo de observabilidad (tracing, logging)
```

Para un agente multi-paso tipico:
- **System prompt**: 500-2,000 tokens (se paga en cada iteracion del loop)
- **Contexto/historial**: 1,000-10,000 tokens (crece con cada paso)
- **Output por paso**: 200-1,000 tokens
- **Tool calls**: 300-500 tokens por llamada

Un agente que ejecuta 5 pasos con un system prompt de 1,500 tokens y contexto creciente puede consumir facilmente 25,000-50,000 tokens por ejecucion. A $3/millon de tokens de input, eso es $0.075-$0.15 por ejecucion. Multiplicado por 10,000 ejecuciones diarias: $750-$1,500 por dia, o $22,500-$45,000 por mes.

Despues del lanzamiento, una organizacion puede esperar entre $3,200 y $13,000 mensuales en costos operativos que incluyen tokens del API del LLM, hosting de bases de datos vectoriales, monitoreo, ajuste de prompts y mantenimiento de seguridad [Sparkout Tech, 2026].

### Estrategias de optimizacion

Las estrategias de optimizacion se organizan por impacto y facilidad de implementacion.

#### Nivel 1: Model routing (impacto alto, facil)

Como vimos en el Capitulo 13 (patron Model Router), dirigir consultas simples a modelos pequenos y baratos reduce costos 60-85% sin perdida significativa de calidad [Ong et al., 2025].

```python
"""
Ejemplo de router de costos que selecciona el modelo
mas barato capaz de resolver la tarea.
"""

# Precios aproximados Q1 2026 (USD por millon de tokens)
MODEL_PRICING = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "claude-haiku": {"input": 0.25, "output": 1.25},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "claude-sonnet": {"input": 3.00, "output": 15.00},
    "o1": {"input": 15.00, "output": 60.00},
    "claude-opus": {"input": 15.00, "output": 75.00},
}

# Relacion de costo: el modelo mas caro es 100x mas caro
# que el mas barato. La diferencia importa a escala.
```

#### Nivel 2: Caching (impacto alto, medio)

Cachear respuestas para consultas repetitivas o similares. Anthropic ofrece un 90% de descuento en tokens de input cacheados. Si tu agente tiene un system prompt largo que se repite en cada ejecucion, el prompt caching puede reducir el 20-30% de la factura [Fast.io, 2026].

```python
"""
Cache semantico basico para respuestas de agentes.
Usa hashing del input para cache exacto.
Para cache semantico (inputs similares), usa embeddings.
"""

import hashlib
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class CachedResponse:
    response: dict
    created_at: float
    ttl_seconds: int
    hit_count: int = 0


class AgentResponseCache:
    """Cache de respuestas para consultas repetitivas."""

    def __init__(self, default_ttl: int = 3600):
        self._cache: dict[str, CachedResponse] = {}
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0

    def _make_key(self, agent_id: str, user_input: str) -> str:
        content = f"{agent_id}:{user_input}"
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, agent_id: str, user_input: str) -> Optional[dict]:
        key = self._make_key(agent_id, user_input)
        cached = self._cache.get(key)
        if cached is None:
            self.misses += 1
            return None

        # Verificar TTL
        if time.time() - cached.created_at > cached.ttl_seconds:
            del self._cache[key]
            self.misses += 1
            return None

        cached.hit_count += 1
        self.hits += 1
        return cached.response

    def put(
        self,
        agent_id: str,
        user_input: str,
        response: dict,
        ttl: Optional[int] = None,
    ) -> None:
        key = self._make_key(agent_id, user_input)
        self._cache[key] = CachedResponse(
            response=response,
            created_at=time.time(),
            ttl_seconds=ttl or self.default_ttl,
        )

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return self.hits / total
```

#### Nivel 3: Optimizacion de prompts (impacto medio, facil)

- Reducir el system prompt al minimo necesario.
- Comprimir el historial de conversacion (resumir en lugar de incluir todo).
- Usar pocas instrucciones pero claras (less is more).
- Eliminar ejemplos redundantes en el few-shot.

#### Nivel 4: Presupuestos por tarea (impacto medio, medio)

Establecer limites en tres niveles: por peticion (`max_tokens`), por tarea (presupuesto total del agente para un flujo), y por dia/mes (gasto maximo). Alertar al 50% y 80% del presupuesto para poder ajustar antes de alcanzar el limite [Moltbook-AI, 2026].

```python
"""
Presupuesto de tokens por tarea con alertas.
"""

from dataclasses import dataclass


@dataclass
class TokenBudget:
    """Presupuesto de tokens para una tarea del agente."""
    max_tokens: int
    alert_at_50_pct: bool = True
    alert_at_80_pct: bool = True
    _consumed: int = 0

    def consume(self, tokens: int) -> None:
        self._consumed += tokens
        usage_pct = self._consumed / self.max_tokens

        if self.alert_at_50_pct and usage_pct >= 0.50 and (
            (self._consumed - tokens) / self.max_tokens < 0.50
        ):
            self._alert(50)

        if self.alert_at_80_pct and usage_pct >= 0.80 and (
            (self._consumed - tokens) / self.max_tokens < 0.80
        ):
            self._alert(80)

    def has_budget(self) -> bool:
        return self._consumed < self.max_tokens

    @property
    def remaining(self) -> int:
        return max(0, self.max_tokens - self._consumed)

    @property
    def usage_percentage(self) -> float:
        return self._consumed / self.max_tokens

    def _alert(self, pct: int) -> None:
        print(
            f"ALERTA: presupuesto de tokens al {pct}% "
            f"({self._consumed}/{self.max_tokens})"
        )
```

#### Nivel 5: Reducir pasos del agente (impacto alto, dificil)

El factor multiplicativo mas grande es el numero de pasos del loop agentico. Un agente que toma 20 pasos cuando 3 bastarian esta desperdiciando tokens. Estrategias:

- Mejorar el prompt para que el agente sea mas eficiente en su razonamiento.
- Proveer herramientas mas poderosas (una herramienta que resuelve en 1 llamada vs 5 herramientas que requieren composicion).
- Usar modelos con mejores capacidades de planificacion (los modelos de razonamiento como o1 o DeepSeek-R1 a veces resuelven en menos pasos).

La combinacion de model routing y caching tipicamente entrega 40-60% de ahorro. Agregar optimizacion de prompts y presupuestos puede llevar el ahorro total al 60-80% [Fast.io, 2026].

---

## Takeaway del capitulo

La ingenieria de produccion para agentes es lo que separa a los proyectos que generan valor de los que se cancelan:

- **El checklist de 43 items** cubre seguridad, observabilidad, resiliencia, testing y costos. No todos aplican a todos los agentes, pero el nivel de rigor debe ser proporcional al impacto de un fallo.

- **El monitoreo de agentes** va mas alla de HTTP status codes. Necesitas metricas de tokens, costos, calidad y tasa de fallback. OpenTelemetry es el estandar abierto para instrumentacion.

- **El deployment de agentes** requiere estrategias adaptadas al no determinismo. Canary releases con evaluacion de calidad son la opcion de menor riesgo. Shadow deployment es ideal para cambios grandes de modelo.

- **Los prompts son codigo.** Deben vivir en git, tener versionado semantico, ejecutar evaluaciones en CI, y desplegarse con canary.

- **Los costos se desbordan sin control.** Model routing + caching entregan 40-60% de ahorro. Presupuestos por tarea previenen sorpresas. Revision mensual de ROI es obligatoria.

El principio rector: **trata a tu agente con el mismo rigor que le darias a un servicio financiero.** Porque en produccion, un agente mal configurado puede causar tanto dano como un bug en un sistema de pagos.

---

## Referencias

- OpenTelemetry. "AI Agent Observability - Evolving Standards and Best Practices." opentelemetry.io/blog, 2025.
- Braintrust. "AI Observability Tools: A Buyer's Guide to Monitoring AI Agents in Production (2026)." braintrust.dev/articles, 2026.
- Moltbook-AI. "AI Agent Cost Optimization Guide 2026: Reduce Spend by 60-80%." moltbook-ai.com, 2026.
- Fast.io. "AI Agent Token Cost Optimization: Complete Guide for 2026." fast.io/resources, 2026.
- Silicon Data. "Understanding LLM Cost Per Token: A 2026 Practical Guide." silicondata.com/blog, 2026.
- Sparkout Tech. "AI Agent Development Cost in 2026 - Pricing, MVP, ROI & Budget Guide." sparkouttech.com, 2026.
- Getmaxim. "Managing Prompt Versions: Effective Strategies for Large Teams Using AI Agents." getmaxim.ai/articles, 2026.
- AI-AgentsPlus. "AI Agent Monitoring and Observability: Production Best Practices." ai-agentsplus.com/blog, 2026.
- Ong, I., et al. "RouteLLM: Learning to Route LLMs with Preference Data." *ICLR*, 2025.
- Anthropic. "Building Effective Agents." anthropic.com/research, diciembre 2024.
- Huyen, C. *AI Engineering: Building Applications with Foundation Models*. O'Reilly, 2025.
