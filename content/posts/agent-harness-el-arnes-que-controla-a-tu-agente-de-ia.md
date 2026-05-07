---
title: "Agent Harness: el arnés que controla a tu agente de IA"
date: 2026-03-21
author: "Héctor Patricio"
tags: ['agentes', 'inteligencia-artificial', 'arquitectura', 'seguridad', 'llm', 'python', 'diseño-de-software', 'guardrails', 'observabilidad']
description: "Exploramos la arquitectura de un Agent Harness: guardrails, circuit breakers, sandboxing y observabilidad para mantener a tus agentes bajo control en producción."
featuredImage: ""
draft: true
---

En enero de 2025, un agente de IA con acceso a una base de datos de producción ejecutó un `DELETE FROM orders` sin cláusula `WHERE`. El desarrollador le había dado permisos de escritura "para que pudiera actualizar estados de pedidos". El agente interpretó una instrucción ambigua del usuario, construyó la query, la ejecutó y borró 14,000 registros en tres segundos. No había rollback automático, no había confirmación humana, no había límites de alcance.

Ese agente no tenía arnés.

Los agentes de IA pueden navegar problemas complejos, tomar decisiones, ejecutar código, llamar APIs y transformar datos. Pero sin controles adecuados, cada acción autónoma es una caída potencial: pueden borrar datos de producción, gastar miles de dólares en tokens en un loop infinito, filtrar información sensible o ejecutar código malicioso inyectado por un atacante.

En ingeniería de software, el concepto de *harness* (arnés) no es nuevo. Un **test harness** es la infraestructura que envuelve tu código bajo prueba: lo ejecuta, captura sus salidas, verifica que se comporta correctamente y reporta fallos. No modifica el código que prueba, pero lo contiene y lo observa. Cuando hablamos de un **Agent Harness**, estamos aplicando la misma idea a un sistema mucho más impredecible: un agente de IA con capacidad de actuar en el mundo.

En artículos anteriores hemos hablado sobre [patrones de diseño para sistemas con IA](/posts/patrones-de-diseno-para-sistemas-con-ia/) y las [vulnerabilidades del OWASP Top 10 para LLMs](/posts/owasp-top-10-para-llms-las-nuevas-vulnerabilidades/). Ahora vamos a entrar en el *cómo*: la infraestructura concreta que necesitas construir alrededor de tus agentes para que sean seguros, observables y controlables.

## ¿Qué es un Agent Harness?

Un Agent Harness es la **infraestructura que envuelve a un agente de IA para controlarlo, monitorearlo y limitarlo**. No es el agente en sí. No es el modelo de lenguaje. No es la lógica de negocio. Es todo lo que existe *alrededor* del agente para asegurar que se comporta dentro de los límites aceptables.

Un Agent Harness se compone de varios subsistemas:

- **Guardrails**: barreras de contención que validan las entradas y salidas del agente.
- **Circuit breakers**: mecanismos que cortan la ejecución cuando algo sale mal.
- **Rate limiters**: controles de velocidad y presupuesto (tokens, tiempo, dinero).
- **Sandboxing**: aislamiento del agente respecto al sistema y al mundo exterior.
- **Logging y tracing**: registro detallado de cada decisión y acción.
- **Métricas y alertas**: observabilidad en tiempo real del comportamiento del agente.

Si has leído nuestra serie sobre [A Philosophy of Software Design](/posts/a-philosophy-of-software-design-los-modulos-deben-ser-profundos/), reconocerás aquí el principio de los **módulos profundos**: el harness debe tener una interfaz simple hacia el resto del sistema (inyectas un agente, obtienes un agente controlado) pero una implementación rica y profunda que maneja toda la complejidad de control, monitoreo y seguridad. El usuario del agente no debería tener que preocuparse por los detalles del harness; simplemente debería poder confiar en que el agente está bajo control.

Un Agent Harness aplica en producción la misma estructura de un test harness: preparar, ejecutar, capturar, verificar, limpiar. La diferencia es que opera de forma continua, con datos reales y consecuencias reales.

## El principio de mínimo privilegio aplicado a agentes

El principio de mínimo privilegio (*Principle of Least Privilege*, PoLP) es uno de los fundamentos de la seguridad informática desde que Saltzer y Schroeder lo formalizaron en 1975. La idea es simple: cada componente de un sistema solo debe tener acceso a los recursos que necesita para cumplir su función, nada más.

Aplicado a agentes de IA, este principio se vuelve crítico. En el [OWASP Top 10 para LLMs](/posts/owasp-top-10-para-llms-las-nuevas-vulnerabilidades/), la vulnerabilidad de **"Excessive Agency"** (agencia excesiva) está entre las más peligrosas. Ocurre cuando un agente tiene permisos que exceden lo que necesita para su tarea. Un agente de servicio al cliente que puede leer la base de datos de clientes *y también* ejecutar queries de escritura tiene exactamente el perfil del incidente que describimos al inicio.

### Permisos granulares por acción

La implementación correcta del mínimo privilegio en agentes requiere pensar en permisos a nivel de *acción*, no de *herramienta*. No basta con decir "el agente puede usar la herramienta de base de datos". Necesitas especificar:

- **Qué operaciones** puede hacer: solo SELECT, no INSERT ni DELETE.
- **Sobre qué datos**: solo la tabla `products`, no `users`.
- **Con qué frecuencia**: máximo 10 queries por minuto.
- **Con qué alcance**: solo registros del usuario actual, no de todos los usuarios.

Veamos cómo se ve esto en código:

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

class Permission(Enum):
    DB_READ = "db:read"
    DB_WRITE = "db:write"
    API_CALL = "api:call"
    FILE_READ = "file:read"
    FILE_WRITE = "file:write"
    EMAIL_SEND = "email:send"
    CODE_EXECUTE = "code:execute"

@dataclass
class AgentPermissions:
    """Define los permisos granulares de un agente."""
    allowed: set[Permission] = field(default_factory=set)
    rate_limits: dict[Permission, int] = field(default_factory=dict)  # acciones/minuto
    scope_filters: dict[Permission, Callable] = field(default_factory=dict)

    def check(self, permission: Permission, context: dict) -> bool:
        if permission not in self.allowed:
            return False
        if permission in self.scope_filters:
            return self.scope_filters[permission](context)
        return True

# Un agente de soporte solo puede leer datos y enviar emails
support_agent_permissions = AgentPermissions(
    allowed={Permission.DB_READ, Permission.EMAIL_SEND},
    rate_limits={
        Permission.DB_READ: 20,       # 20 queries por minuto
        Permission.EMAIL_SEND: 5,     # 5 emails por minuto
    },
    scope_filters={
        Permission.DB_READ: lambda ctx: ctx.get("table") in ("products", "orders"),
    }
)
```

Este enfoque es radicalmente diferente a lo que hacen muchos frameworks de agentes hoy, donde el agente tiene acceso completo a todas las herramientas que se le registran. La filosofía UNIX de "cada programa hace una cosa bien" aplica perfectamente aquí: cada agente debe tener un conjunto mínimo de capacidades, bien definidas y bien acotadas.

### La regla de la confirmación humana

Para acciones con consecuencias irreversibles, el mínimo privilegio incluye un componente humano. El agente puede *proponer* acciones destructivas, pero un humano debe *aprobarlas*. Esto se conoce como el patrón **Human-in-the-Loop** (HITL). No es una debilidad del sistema; es una fortaleza. Reconoce honestamente que los LLMs pueden equivocarse y que ciertas acciones no tienen un botón de "deshacer".

## Guardrails: barreras de contención

Los guardrails son el componente más visible de un Agent Harness. Son las barreras que verifican qué entra al agente y qué sale de él. Imagínalos como los muros de contención en una carretera de montaña: no te impiden conducir, pero evitan que te vayas al precipicio.

### Input guardrails: validar qué entra

Los input guardrails filtran y validan lo que llega al agente antes de que lo procese. Esto incluye:

- **Detección de prompt injection**: identificar intentos de manipular las instrucciones del agente. Como discutimos en el artículo sobre [OWASP para LLMs](/posts/owasp-top-10-para-llms-las-nuevas-vulnerabilidades/), la inyección de prompts es la vulnerabilidad más crítica en sistemas con LLMs.
- **Validación de formato**: asegurar que los datos de entrada cumplen los esquemas esperados.
- **Filtrado de contenido**: detectar contenido que viola las políticas del sistema (contenido ofensivo, datos sensibles, etc.).
- **Límites de tamaño**: evitar que entradas excesivamente grandes agoten los recursos.

```python
from typing import Any

@dataclass
class GuardrailResult:
    passed: bool
    reason: str = ""
    modified_input: Any = None

class InputGuardrail:
    """Guardrail que valida la entrada antes de enviarla al agente."""

    def __init__(self, validators: list[Callable]):
        self.validators = validators

    def validate(self, user_input: str, context: dict) -> GuardrailResult:
        for validator in self.validators:
            result = validator(user_input, context)
            if not result.passed:
                return result
            if result.modified_input is not None:
                user_input = result.modified_input
        return GuardrailResult(passed=True, modified_input=user_input)

# Ejemplo ILUSTRATIVO de detección de prompt injection por patrones.
# ADVERTENCIA: esta detección por substrings NO es una protección real.
# Un atacante la evade trivialmente con variaciones ortográficas,
# Unicode homoglyphs o reformulaciones. En producción, usa un
# clasificador entrenado o un guardrail basado en LLM como segunda capa.
def detect_injection(user_input: str, context: dict) -> GuardrailResult:
    suspicious_patterns = [
        "ignora las instrucciones",
        "ignore previous instructions",
        "olvida tu sistema",
        "actúa como si fueras",
        "you are now",
        "system prompt override",
    ]
    input_lower = user_input.lower()
    for pattern in suspicious_patterns:
        if pattern in input_lower:
            return GuardrailResult(
                passed=False,
                reason=f"Posible inyección de prompt detectada: '{pattern}'"
            )
    return GuardrailResult(passed=True)

def limit_input_length(user_input: str, context: dict) -> GuardrailResult:
    max_length = context.get("max_input_length", 4000)
    if len(user_input) > max_length:
        return GuardrailResult(
            passed=False,
            reason=f"Entrada excede el límite de {max_length} caracteres"
        )
    return GuardrailResult(passed=True)
```

### Output guardrails: validar qué sale

Los output guardrails son igual de importantes, quizás más. Mientras que los input guardrails protegen al agente del mundo, los output guardrails protegen al mundo del agente. Verifican que las respuestas y acciones del agente sean:

- **Conformes al formato esperado**: la respuesta tiene la estructura correcta.
- **Libres de información sensible**: no se filtran datos personales, claves API, ni secretos.
- **Coherentes con la tarea**: el agente no se desvió a un tema o acción fuera de su alcance.
- **Seguras para ejecutar**: si el agente genera código o comandos, estos son seguros.

```python
import re

def detect_sensitive_data(output: str, context: dict) -> GuardrailResult:
    """Detecta datos sensibles en la salida del agente.

    Nota: estos patrones son aproximaciones. La regex de tarjetas
    de crédito captura falsos positivos (cualquier secuencia de 16
    dígitos agrupada en cuatro) y tiene falsos negativos (ej: American
    Express usa un formato diferente). En producción, complementa
    con validación de checksum (Luhn) y patrones por emisor.
    """
    patterns = {
        "credit_card": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "api_key": r"\b(sk-|pk_|api[_-]key[_-]?)[a-zA-Z0-9]{20,}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    }
    for data_type, pattern in patterns.items():
        if re.search(pattern, output):
            return GuardrailResult(
                passed=False,
                reason=f"Dato sensible detectado en salida: {data_type}"
            )
    return GuardrailResult(passed=True)
```

### Guardrails determinísticos vs guardrails basados en LLM

Aquí hay una distinción fundamental que muchos equipos pasan por alto. Existen dos tipos de guardrails:

**Guardrails determinísticos** usan reglas fijas: expresiones regulares, listas de bloqueo, validaciones de esquema JSON, límites numéricos. Son rápidos, predecibles y no se pueden evadir con creatividad lingüística. Si una regex busca números de tarjeta de crédito, los va a encontrar sin importar cómo el agente intente disfrazarlos (bueno, casi).

**Guardrails basados en LLM** usan otro modelo de lenguaje para evaluar si la entrada o salida del agente es aceptable. Son más flexibles y pueden entender el *significado* de un texto, no solo su forma. Pero tienen un problema profundo: son vulnerables a los mismos ataques que intentan prevenir. Si un atacante puede manipular al agente principal con prompt injection, potencialmente puede manipular al modelo guardian también.

La estrategia correcta es **combinar ambos tipos**. Los guardrails determinísticos son la primera línea de defensa: rápidos, baratos y confiables. Los guardrails basados en LLM son la segunda línea: más inteligentes pero más costosos y menos predecibles.

```python
class LayeredGuardrail:
    """Guardrail en capas: primero determinístico, luego basado en LLM."""

    def __init__(self, deterministic_checks, llm_check=None):
        self.deterministic = deterministic_checks
        self.llm_check = llm_check  # Solo se llama si pasa los determinísticos

    def validate(self, text: str, context: dict) -> GuardrailResult:
        # Capa 1: Checks rápidos y determinísticos
        for check in self.deterministic:
            result = check(text, context)
            if not result.passed:
                return result

        # Capa 2: Check semántico con LLM (más lento, más costoso)
        if self.llm_check is not None:
            return self.llm_check(text, context)

        return GuardrailResult(passed=True)
```

### El problema de la evasión

Un guardrail que el agente puede aprender a evadir no es un guardrail, es una sugerencia. Este es un problema real y profundo. Si un agente de IA observa que ciertos patrones en su salida son rechazados por los guardrails, puede aprender (dentro de una misma conversación o a través de fine-tuning) a formular la misma información de maneras que pasen los filtros.

La solución no es hacer guardrails más inteligentes indefinidamente (eso es una carrera armamentista perdida). La solución es implementar **defensa en profundidad**: múltiples capas de protección independientes, de modo que evadir una capa no comprometa todo el sistema. Este es el mismo principio que usamos en seguridad de redes: firewalls, IDS, segmentación, cifrado, cada capa aporta protección independiente.

## Circuit breakers y rate limiters para agentes

El patrón **Circuit Breaker**, popularizado por Michael Nygard en "Release It!", fue diseñado para sistemas distribuidos: cuando un servicio externo falla repetidamente, dejas de llamarlo por un tiempo para evitar cascadas de fallos. Aplicado a agentes de IA, este patrón se vuelve aún más importante porque los fallos de un agente no son solo técnicos, pueden tener consecuencias en el mundo real.

### Cuándo cortar la ejecución

Un circuit breaker para agentes debe activarse cuando detecta:

- **Loops de razonamiento**: el agente repite las mismas acciones o genera las mismas herramientas en ciclos. Esto es sorprendentemente común. Un agente que intenta resolver un error llamando a la misma herramienta con los mismos parámetros diez veces es un agente atrapado en un loop.
- **Consumo excesivo de tokens**: el agente está gastando más tokens de lo esperado para la tarea. Esto puede indicar que está "divagando" o que la tarea es más compleja de lo anticipado.
- **Tiempo excesivo**: si un agente lleva 10 minutos en una tarea que debería tomar 30 segundos, algo anda mal.
- **Errores consecutivos**: si las últimas N llamadas a herramientas fallaron, el agente probablemente no va a resolver el problema por sí solo.

```python
import time
from collections import deque

@dataclass
class CircuitBreakerConfig:
    max_iterations: int = 50
    max_tokens: int = 100_000
    max_time_seconds: float = 300.0  # 5 minutos
    max_consecutive_errors: int = 5
    loop_detection_window: int = 10
    loop_similarity_threshold: float = 0.9

class AgentCircuitBreaker:
    """Circuit breaker que detiene al agente cuando detecta comportamiento anómalo."""

    def __init__(self, config: CircuitBreakerConfig):
        self.config = config
        self.iterations = 0
        self.tokens_used = 0
        self.start_time = time.time()
        self.consecutive_errors = 0
        self.recent_actions: deque = deque(maxlen=config.loop_detection_window)

    def record_iteration(self, action: str, tokens: int, success: bool):
        self.iterations += 1
        self.tokens_used += tokens
        self.recent_actions.append(action)

        if success:
            self.consecutive_errors = 0
        else:
            self.consecutive_errors += 1

    def should_trip(self) -> tuple[bool, str]:
        """Verifica si el circuit breaker debe activarse."""
        elapsed = time.time() - self.start_time

        if self.iterations >= self.config.max_iterations:
            return True, f"Límite de iteraciones alcanzado: {self.iterations}"

        if self.tokens_used >= self.config.max_tokens:
            return True, f"Presupuesto de tokens agotado: {self.tokens_used}"

        if elapsed >= self.config.max_time_seconds:
            return True, f"Tiempo máximo excedido: {elapsed:.1f}s"

        if self.consecutive_errors >= self.config.max_consecutive_errors:
            return True, f"Errores consecutivos: {self.consecutive_errors}"

        if self._detect_loop():
            return True, "Loop de razonamiento detectado"

        return False, ""

    def _detect_loop(self) -> bool:
        """Detecta si el agente está atrapado en un loop."""
        if len(self.recent_actions) < self.config.loop_detection_window:
            return False

        # Buscar patrones repetitivos en las acciones recientes
        actions = list(self.recent_actions)
        # Verificar si la mitad más reciente es igual a la mitad anterior
        mid = len(actions) // 2
        first_half = actions[:mid]
        second_half = actions[mid:mid + len(first_half)]
        matches = sum(1 for a, b in zip(first_half, second_half) if a == b)
        similarity = matches / len(first_half) if first_half else 0
        return similarity >= self.config.loop_similarity_threshold
```

### Presupuestos de tokens y dinero

Un concepto que se vuelve crítico en producción es el **presupuesto por tarea**. No solo cuántos tokens puede usar un agente en total, sino cuántos puede usar *por tarea individual*. Esto conecta directamente con la realidad económica de operar agentes: una llamada a GPT-4 o Claude con una ventana de contexto grande puede costar varios dólares. Un agente en loop puede generar facturas de miles de dólares en minutos.

```python
@dataclass
class Budget:
    max_tokens: int
    max_cost_usd: float
    max_api_calls: int

    tokens_used: int = 0
    cost_usd: float = 0.0
    api_calls: int = 0

    def consume(self, tokens: int, cost: float):
        self.tokens_used += tokens
        self.cost_usd += cost
        self.api_calls += 1

    def is_exhausted(self) -> tuple[bool, str]:
        if self.tokens_used >= self.max_tokens:
            return True, f"Tokens: {self.tokens_used}/{self.max_tokens}"
        if self.cost_usd >= self.max_cost_usd:
            return True, f"Costo: ${self.cost_usd:.2f}/${self.max_cost_usd:.2f}"
        if self.api_calls >= self.max_api_calls:
            return True, f"Llamadas API: {self.api_calls}/{self.max_api_calls}"
        return False, ""
```

### Fallbacks: qué hacer cuando el circuit breaker se activa

Cuando el circuit breaker corta la ejecución de un agente, necesitas un plan B. El circuit breaker no es un interruptor binario de "funciona / no funciona"; es el inicio de un flujo de *degradación elegante* (*graceful degradation*). Las opciones, en orden de preferencia, son:

1. **Respuesta parcial**: devuelve al usuario lo que el agente logró hasta el momento de la interrupción. Si el agente completó 3 de 5 pasos antes de que el circuit breaker se activara, esos 3 pasos pueden ser útiles. Esto requiere que el harness capture resultados intermedios, no solo el resultado final.
2. **Escalación humana**: notificar a un operador humano para que tome el control. En un chatbot de soporte, esto es frecuentemente lo correcto: transferir a un agente humano con el contexto de lo que el agente de IA ya intentó.
3. **Modelo de respaldo**: reintentar con un modelo menos capaz pero más predecible y barato. Si Claude Sonnet falló por un loop de razonamiento, un modelo más pequeño con instrucciones más estrictas puede resolver la tarea.
4. **Caché**: si la pregunta es similar a una anterior, devolver la respuesta cacheada.
5. **Respuesta genérica pre-armada**: el último recurso. Mejor que nada, pero solo si las opciones anteriores no aplican.

La elección del fallback depende del contexto y del motivo de la interrupción. Un trip por exceso de tokens sugiere que un modelo más barato podría funcionar. Un trip por loop de razonamiento sugiere que el agente necesita intervención humana. Lo importante es que la estrategia de fallback esté definida y probada *antes* de que ocurra el fallo, no después.

## Gestión de costos: la dimensión olvidada del harness

En producción, el costo de tokens es frecuentemente la razón número uno por la que un agente se apaga. He visto equipos gastar decenas de miles de dólares al mes porque sus agentes entraban en loops de razonamiento verbosos o generaban contextos innecesariamente largos. El harness necesita un *budget manager* de costos como componente de primera clase, no como algo que se agrega después del primer susto financiero.

La clase `Budget` que vimos arriba es un buen comienzo, pero un sistema de producción necesita presupuestos a múltiples niveles:

- **Por request**: un límite duro que corta la ejecución si una sola tarea excede lo esperado.
- **Por sesión**: acumula el gasto de todas las tareas de un usuario en una conversación.
- **Por usuario/tenant**: límites mensuales o diarios por cliente, útiles en sistemas multi-tenant.
- **Global**: un circuit breaker financiero que detiene *todo el sistema* si el gasto total se dispara, posiblemente indicando un ataque o un bug.

Además del presupuesto, necesitas **alertas de anomalías de costo**: si el costo promedio por tarea sube un 50% de un día a otro, algo cambió (un prompt más largo, un modelo diferente, un bug en el loop). Detectar estas anomalías temprano es la diferencia entre un susto y una catástrofe financiera.

## Observabilidad: ver lo que el agente hace

La observabilidad en sistemas agénticos es fundamentalmente más difícil que en sistemas tradicionales porque las decisiones no son deterministas y el "por qué" de cada acción está enterrado en las representaciones internas del modelo. Cuando un agente toma una decisión incorrecta en producción, necesitas poder reconstruir su cadena de razonamiento completa.

### Tracing distribuido para agentes

El estándar OpenTelemetry, que ya es el estándar *de facto* para tracing distribuido, se adapta naturalmente a los sistemas agénticos. Cada ejecución de un agente genera un **trace** compuesto por **spans**:

- **Span raíz**: la tarea completa del agente.
- **Span de razonamiento**: cada paso de pensamiento del agente.
- **Span de herramienta**: cada llamada a una herramienta externa.
- **Span de LLM**: cada llamada al modelo de lenguaje.
- **Span de guardrail**: cada validación de entrada/salida.

```python
from contextlib import contextmanager
import uuid
import time as time_module
import logging

logger = logging.getLogger("agent_harness")

@dataclass
class Span:
    name: str
    trace_id: str
    span_id: str
    parent_id: str | None
    start_time: float
    end_time: float | None = None
    attributes: dict = field(default_factory=dict)
    status: str = "OK"

    def finish(self, status: str = "OK"):
        self.end_time = time_module.time()
        self.status = status

class AgentTracer:
    """Trazador ligero para agentes de IA."""

    def __init__(self):
        self.spans: list[Span] = []
        self.current_trace_id = str(uuid.uuid4())

    @contextmanager
    def span(self, name: str, parent_id: str | None = None, **attributes):
        s = Span(
            name=name,
            trace_id=self.current_trace_id,
            span_id=str(uuid.uuid4()),
            parent_id=parent_id,
            start_time=time_module.time(),
            attributes=attributes,
        )
        try:
            yield s
        except Exception as e:
            s.finish(status=f"ERROR: {e}")
            raise
        else:
            s.finish()
        finally:
            self.spans.append(s)
            logger.info(
                "span_completed",
                extra={
                    "span_name": s.name,
                    "trace_id": s.trace_id,
                    "duration_ms": (s.end_time - s.start_time) * 1000
                    if s.end_time
                    else None,
                    "status": s.status,
                    **s.attributes,
                },
            )
```

En producción, OpenTelemetry se complementa con herramientas de observabilidad específicas para agentes de IA como **LangSmith**, **Langfuse** y **Arize Phoenix**, que además de traces ofrecen métricas de costo por request, dashboards de calidad de respuesta y evals automáticas. Estas herramientas se integran con OpenTelemetry estándar y proporcionan una vista especializada que las herramientas de observabilidad genéricas (Datadog, Grafana) no cubren bien por sí solas.

### Logging estructurado de decisiones

El logging en un sistema agéntico debe responder la pregunta más importante: **¿por qué el agente hizo lo que hizo?** Para esto, cada decisión del agente se debe registrar con su contexto completo:

- **Qué herramientas consideró** y cuál eligió.
- **Qué argumentos pasó** a la herramienta.
- **Qué obtuvo como resultado**.
- **Cómo interpretó el resultado** para decidir el siguiente paso.

Este nivel de detalle puede parecer excesivo, pero es absolutamente necesario para debugging en producción.

### Métricas clave

Las métricas que debes monitorear en un sistema agéntico van más allá de las típicas de un servicio web:

| Métrica | Qué te dice | Alerta si... |
|---------|------------|--------------|
| **Latencia por tarea (P50, P95, P99)** | Cuánto tarda el agente en completar una tarea | P95 > umbral del SLA |
| **Costo por tarea** | Cuánto cuesta en tokens/dinero cada tarea | > presupuesto asignado |
| **Tasa de éxito** | Porcentaje de tareas completadas exitosamente | < 90% |
| **Tasa de escalación** | Porcentaje de tareas que requieren intervención humana | Aumento repentino |
| **Profundidad de razonamiento** | Cuántos pasos toma el agente por tarea | Aumento sin mejora en calidad |
| **Tasa de trips del circuit breaker** | Con qué frecuencia se activa el circuit breaker | > 5% de las tareas |
| **Tokens desperdiciados** | Tokens usados en loops, reintentos fallidos, etc. | > 20% del total |

## Sandboxing: aislar al agente del mundo

Si el principio de mínimo privilegio es el "qué" (qué puede hacer el agente), el sandboxing es el "dónde" (en qué entorno se ejecutan sus acciones). Sandboxing significa ejecutar al agente en un entorno aislado donde sus acciones no pueden afectar al sistema principal.

### Ejecución de código en contenedores

Cuando un agente genera y ejecuta código, esa ejecución debe ocurrir en un contenedor efímero con:

- **Sistema de archivos aislado**: el agente no puede leer ni escribir fuera de su directorio asignado.
- **Red restringida**: el agente solo puede acceder a las APIs autorizadas, no a Internet abierto.
- **Recursos limitados**: CPU, memoria y tiempo de ejecución acotados.
- **Sin persistencia**: el contenedor se destruye después de la ejecución.

Este es el mismo principio que usan los playgrounds de código en línea (como Replit o los Jupyter notebooks de Google Colab) y los agentes de código como Claude Code o Codex. La diferencia es que en producción necesitas automatizar completamente el ciclo de vida del contenedor.

```python
import subprocess
import tempfile
import os

@dataclass
class SandboxConfig:
    max_memory_mb: int = 512
    max_cpu_seconds: int = 30
    allowed_network: list[str] = field(default_factory=list)
    allowed_imports: set[str] = field(default_factory=lambda: {
        "json", "math", "datetime", "re", "collections",
        "itertools", "functools", "typing", "dataclasses",
    })

class CodeSandbox:
    """Sandbox para ejecutar código generado por agentes."""

    def __init__(self, config: SandboxConfig):
        self.config = config

    def validate_code(self, code: str) -> GuardrailResult:
        """Valida el código antes de ejecutarlo."""
        # Verificar imports peligrosos
        import ast
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return GuardrailResult(passed=False, reason=f"Error de sintaxis: {e}")

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module = alias.name.split(".")[0]
                    if module not in self.config.allowed_imports:
                        return GuardrailResult(
                            passed=False,
                            reason=f"Import no permitido: {module}"
                        )
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module = node.module.split(".")[0]
                    if module not in self.config.allowed_imports:
                        return GuardrailResult(
                            passed=False,
                            reason=f"Import no permitido: {module}"
                        )

        # Verificar llamadas peligrosas
        dangerous_calls = {"eval", "exec", "compile", "__import__", "open",
                           "getattr", "setattr", "delattr", "globals", "locals"}
        dangerous_attrs = {"__builtins__", "__import__", "__subclasses__",
                           "__class__", "__bases__", "__mro__"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in dangerous_calls:
                    return GuardrailResult(
                        passed=False,
                        reason=f"Llamada peligrosa detectada: {node.func.id}"
                    )
            # Detectar acceso a atributos peligrosos (ej: __builtins__)
            if isinstance(node, ast.Attribute) and node.attr in dangerous_attrs:
                return GuardrailResult(
                    passed=False,
                    reason=f"Acceso a atributo peligroso: {node.attr}"
                )

        return GuardrailResult(passed=True)

    def execute(self, code: str) -> dict:
        """Ejecuta código en un entorno aislado.

        ADVERTENCIA: esta implementación con subprocess es solo
        ilustrativa. En producción, envía el código a un contenedor
        efímero a través de una API. Ver nota debajo del bloque.
        """
        validation = self.validate_code(code)
        if not validation.passed:
            return {"success": False, "error": validation.reason}

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as f:
            f.write(code)
            temp_path = f.name

        try:
            # Entorno mínimo: NO heredar os.environ, que puede
            # contener API keys, tokens y otros secretos.
            # En producción, PATH debería apuntar a un directorio
            # con solo el binario de Python, no a /usr/bin (que
            # da acceso a curl, wget, nc, etc.).
            safe_env = {
                "PATH": "/usr/bin:/bin",
                "HOME": "/tmp",
                "PYTHONDONTWRITEBYTECODE": "1",
                "LANG": "en_US.UTF-8",
            }
            result = subprocess.run(
                ["python", temp_path],
                capture_output=True,
                text=True,
                timeout=self.config.max_cpu_seconds,
                env=safe_env,
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Tiempo de ejecución excedido"}
        finally:
            os.unlink(temp_path)
```

**Sobre la validación AST: no confíes en ella como defensa.** La validación AST que acabamos de ver es un filtro superficial que un atacante sofisticado puede evadir. Por ejemplo, los f-strings que contienen accesos a atributos peligrosos (`f"{''.__class__.__mro__[1].__subclasses__()}"`) se representan como nodos `JoinedStr` en el AST, no como accesos a atributos individuales, así que pasan la verificación sin problemas. La construcción dinámica de strings y otras técnicas de ofuscación también evaden este tipo de análisis estático. La validación AST es un *filtro de conveniencia* que atrapa errores accidentales, no una barrera de seguridad.

**La defensa real es el contenedor.** En producción, *jamás* ejecutes código generado por un LLM en el mismo proceso o máquina que tu servicio. Necesitas contenedores efímeros con aislamiento real: Docker con gVisor o Firecracker, o servicios de ejecución remota como E2B o Modal. La interfaz de un sandbox de producción se ve así:

```python
class ProductionSandbox:
    """Interfaz para sandbox de producción.
    Implementaciones reales: E2B, Modal, Docker con gVisor, AWS Lambda."""

    async def execute(self, code: str, timeout: int = 30) -> SandboxResult:
        # Envía el código a un contenedor efímero aislado
        # a través de una API. Nunca ejecuta en el proceso actual.
        ...
```

El `CodeSandbox` con `subprocess` que mostramos arriba es *solo para ilustrar la estructura*. No lo uses como punto de partida para producción.

### Niveles de aislamiento

En la práctica, hay tres niveles de aislamiento:

1. **Nivel de proceso**: el agente corre en su propio proceso con recursos limitados.
2. **Nivel de contenedor**: el agente corre en un contenedor con filesystem y red aislados.
3. **Nivel de máquina virtual**: el agente corre en una VM completa (máximo aislamiento, máximo costo).

La elección del nivel depende del riesgo. Un agente que solo genera texto puede correr a nivel de proceso. Un agente que ejecuta código necesita al menos nivel de contenedor. Un agente que interactúa con sistemas críticos de infraestructura debería correr en una VM.

## Implementando un harness básico en Python

Ahora vamos a unir todas las piezas en un harness completo que puedas usar como punto de partida. Este ejemplo usa decoradores y composición para crear un sistema modular, siguiendo los principios de módulos profundos que discutimos en la serie sobre [A Philosophy of Software Design](/posts/a-philosophy-of-software-design-los-modulos-deben-ser-profundos/).

```python
from functools import wraps
from typing import Any, Callable
import logging
import time as time_mod

logger = logging.getLogger("agent_harness")


class AgentHarness:
    """
    Harness completo para agentes de IA.

    Uso:
        harness = AgentHarness(
            permissions=support_agent_permissions,
            input_guardrails=[detect_injection, limit_input_length],
            output_guardrails=[detect_sensitive_data],
            circuit_breaker_config=CircuitBreakerConfig(max_iterations=30),
            budget=Budget(max_tokens=50_000, max_cost_usd=1.0, max_api_calls=20),
        )

        @harness.wrap
        def my_agent(task: str) -> str:
            # Tu lógica de agente aquí
            return result
    """

    def __init__(
        self,
        permissions: AgentPermissions,
        input_guardrails: list[Callable] | None = None,
        output_guardrails: list[Callable] | None = None,
        circuit_breaker_config: CircuitBreakerConfig | None = None,
        budget: Budget | None = None,
    ):
        self.permissions = permissions
        self.input_guard = InputGuardrail(input_guardrails or [])
        self.output_guard = InputGuardrail(output_guardrails or [])
        self.circuit_breaker = AgentCircuitBreaker(
            circuit_breaker_config or CircuitBreakerConfig()
        )
        self.budget = budget or Budget(
            max_tokens=100_000, max_cost_usd=5.0, max_api_calls=50
        )
        self.tracer = AgentTracer()

    def wrap(self, agent_fn: Callable) -> Callable:
        """Decorador que envuelve una función de agente con el harness completo."""

        @wraps(agent_fn)
        def wrapped(task: str, **kwargs) -> dict[str, Any]:
            with self.tracer.span("agent_execution", task=task) as root_span:

                # 1. Input guardrails
                with self.tracer.span("input_validation", parent_id=root_span.span_id):
                    input_result = self.input_guard.validate(task, kwargs)
                    if not input_result.passed:
                        logger.warning(f"Input rechazado: {input_result.reason}")
                        return {
                            "success": False,
                            "error": f"Input validation failed: {input_result.reason}",
                            "stage": "input_guardrail",
                        }
                    if input_result.modified_input is not None:
                        task = input_result.modified_input

                # 2. Verificar presupuesto
                exhausted, reason = self.budget.is_exhausted()
                if exhausted:
                    logger.warning(f"Presupuesto agotado: {reason}")
                    return {
                        "success": False,
                        "error": f"Budget exhausted: {reason}",
                        "stage": "budget_check",
                    }

                # 3. Ejecutar agente
                try:
                    with self.tracer.span(
                        "agent_logic", parent_id=root_span.span_id
                    ):
                        result = agent_fn(task, **kwargs)
                except Exception as e:
                    logger.error(f"Agente falló con excepción: {e}")
                    self.circuit_breaker.record_iteration(
                        action=f"exception:{type(e).__name__}",
                        tokens=0,
                        success=False,
                    )
                    return {
                        "success": False,
                        "error": str(e),
                        "stage": "agent_execution",
                    }

                # 4. Output guardrails
                with self.tracer.span(
                    "output_validation", parent_id=root_span.span_id
                ):
                    output_text = str(result)
                    output_result = self.output_guard.validate(output_text, kwargs)
                    if not output_result.passed:
                        logger.warning(f"Output rechazado: {output_result.reason}")
                        return {
                            "success": False,
                            "error": f"Output validation failed: {output_result.reason}",
                            "stage": "output_guardrail",
                        }

                # 5. Circuit breaker check
                trip, trip_reason = self.circuit_breaker.should_trip()
                if trip:
                    logger.error(f"Circuit breaker activado: {trip_reason}")
                    return {
                        "success": False,
                        "error": f"Circuit breaker tripped: {trip_reason}",
                        "stage": "circuit_breaker",
                    }

                return {"success": True, "result": result}

        return wrapped
```

Y así se usa en la práctica:

```python
# Configurar el harness
harness = AgentHarness(
    permissions=AgentPermissions(
        allowed={Permission.DB_READ, Permission.API_CALL},
        rate_limits={Permission.DB_READ: 10, Permission.API_CALL: 5},
    ),
    input_guardrails=[detect_injection, limit_input_length],
    output_guardrails=[detect_sensitive_data],
    circuit_breaker_config=CircuitBreakerConfig(
        max_iterations=30,
        max_tokens=50_000,
        max_time_seconds=120.0,
    ),
    budget=Budget(max_tokens=50_000, max_cost_usd=1.0, max_api_calls=20),
)

# Envolver tu agente
@harness.wrap
def customer_support_agent(task: str, **kwargs) -> str:
    """Agente de soporte al cliente con harness de seguridad."""
    # Aquí va la lógica de tu agente: llamadas al LLM,
    # uso de herramientas, razonamiento, etc.
    response = call_llm(task)  # Tu función de LLM
    return response

# Ejecutar de forma segura
result = customer_support_agent("¿Cuál es el estado de mi pedido #12345?")
if result["success"]:
    print(result["result"])
else:
    print(f"Error en etapa '{result['stage']}': {result['error']}")
```

Este harness es deliberadamente simple. En producción necesitarías agregar persistencia de traces, integración con sistemas de alertas, un sistema de permisos más sofisticado conectado a tu IAM, y probablemente ejecutar los guardrails de forma asíncrona para no agregar latencia excesiva. Pero la estructura fundamental es la correcta: **cada acción del agente pasa por un pipeline de validación, control y registro**.

Como mencionamos en [Creando código de Python robusto](/posts/creando-codigo-de-python-robusto/), la robustez no viene de escribir código "perfecto", sino de construir las capas de protección correctas alrededor de tu código. El Agent Harness es exactamente eso: la capa de protección que convierte un agente peligroso en un agente confiable.

## El harness no es opcional

Déjame terminar con algo que no debería ser controversial pero aún lo es en muchos equipos: **el harness no es una característica opcional que puedes agregar después**. Es un requisito fundamental para poner un agente en producción.

Cada componente que hemos discutido resuelve un problema real:

- **Sin guardrails**, tu agente puede filtrar datos sensibles o ser manipulado por un atacante.
- **Sin circuit breakers**, tu agente puede entrar en un loop infinito y agotar tu presupuesto de tokens.
- **Sin observabilidad**, no tienes idea de por qué tu agente hizo lo que hizo cuando algo sale mal.
- **Sin sandboxing**, un agente que ejecuta código generado puede comprometer toda tu infraestructura.
- **Sin mínimo privilegio**, un agente comprometido tiene acceso a todo tu sistema.

La buena noticia es que no necesitas construir todo esto desde cero. Frameworks como Guardrails AI, NeMo Guardrails de NVIDIA, y las capacidades de guardrails integradas en los SDKs de OpenAI y Anthropic proporcionan piezas del rompecabezas. Pero entender los principios fundamentales, que es lo que hemos hecho en este artículo, te permite evaluar estas herramientas críticamente y adaptarlas a tus necesidades.

El harness no limita lo que tu agente puede lograr. Limita lo que puede destruir cuando se equivoca.

### Referencias y fuentes clave

1. Saltzer, J. H. y Schroeder, M. D. (1975). "The Protection of Information in Computer Systems". *Proceedings of the IEEE*, 63(9). Formaliza el principio de mínimo privilegio.
2. Nygard, M. (2007, 2018). *Release It! Design and Deploy Production-Ready Software*. Pragmatic Bookshelf. Introduce el patrón Circuit Breaker para sistemas distribuidos.
3. OWASP (2025). *OWASP Top 10 for LLM Applications*. https://owasp.org/www-project-top-10-for-large-language-model-applications/. Define "Excessive Agency" como vulnerabilidad critica.
4. Ousterhout, J. (2018). *A Philosophy of Software Design*. Yaknyam Press. Principios de modulos profundos y ocultamiento de informacion aplicados aqui al diseno del harness.
5. OpenTelemetry Project (2024). *OpenTelemetry Specification*. https://opentelemetry.io/docs/specs/. Estandar para tracing distribuido aplicable a sistemas agenticos.
6. Guardrails AI (2025). *Guardrails Framework*. https://www.guardrailsai.com/. Framework open source para input/output guardrails en sistemas LLM.
7. NVIDIA NeMo Guardrails (2025). https://github.com/NVIDIA/NeMo-Guardrails. Framework de guardrails programables para aplicaciones LLM.
8. Greshake, K. et al. (2023). "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection". *arXiv:2302.12173*. Documenta ataques de inyeccion indirecta contra agentes.
9. Anthropic (2025). "Building Effective Agents". Blog post que describe patrones de arquitectura agentica incluyendo guardrails y controles.
10. OpenAI (2025). *Agents SDK - Guardrails*. https://openai.github.io/openai-agents-python/guardrails/. Documentacion del sistema de guardrails del SDK de agentes de OpenAI.
