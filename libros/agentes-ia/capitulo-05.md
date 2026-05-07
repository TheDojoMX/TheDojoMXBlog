# Capitulo 5: El Harness -- El Arnes Que Controla a Tu Agente

> "Un agente sin harness es como un proceso con permisos de root: cuestion de tiempo antes de que algo salga catastróficamente mal. No es cuestion de *si*, sino de *cuando*."

---

En el Capitulo 0 abrimos con sangre: un agente que ejecuto un `DELETE FROM orders` sin clausula `WHERE` y borro 14,000 registros en tres segundos. Otro que genero una factura de $47,000 en un loop de once dias. Otro que filtro datos confidenciales de Meta a empleados sin autorizacion.

Cada uno de esos incidentes tenia algo en comun: el agente no tenia arnes.

En los capitulos anteriores construimos las piezas del agente: el loop agentico (Capitulo 2), la gestion de contexto (Capitulo 3) y el sistema de memoria (Capitulo 4). Ahora vamos a construir la infraestructura que envuelve al agente para controlarlo, monitorearlo y limitarlo. Porque un agente con buena memoria, un loop bien disenado y acceso a herramientas poderosas, pero sin controles, es simplemente una amenaza mas sofisticada.

En ingenieria de software, el concepto de *harness* (arnes) no es nuevo. Un **test harness** es la infraestructura que envuelve tu codigo bajo prueba: lo ejecuta, captura sus salidas, verifica que se comporta correctamente y reporta fallos. No modifica el codigo que prueba, pero lo contiene y lo observa. Cuando hablamos de un **Agent Harness**, estamos aplicando la misma idea a un sistema mucho mas impredecible: un agente de IA con capacidad de actuar en el mundo.

Birgitta Bockeler, en un articulo publicado en la serie de Martin Fowler sobre IA generativa, define el **harness engineering** como la disciplina emergente de construir y mantener la coleccion de especificaciones, checks de calidad y guias de workflow que controlan los diferentes niveles de loops dentro de un sistema agentico [Bockeler, 2026]. OpenAI, por su parte, reporto que su equipo tardo cinco meses en construir el harness que les permitio crear un producto de mas de un millon de lineas de codigo usando Codex como agente de desarrollo [OpenAI, 2026].

El harness no es una caracteristica opcional que puedes agregar despues. Es un requisito fundamental para poner un agente en produccion.

---

## 5.1 Que es un Agent Harness

Un Agent Harness es la **infraestructura que envuelve a un agente de IA para controlarlo, monitorearlo y limitarlo**. No es el agente en si. No es el modelo de lenguaje. No es la logica de negocio. Es todo lo que existe *alrededor* del agente para asegurar que se comporta dentro de los limites aceptables.

Siguiendo los principios de los **modulos profundos** de Ousterhout [Ousterhout, 2018], el harness debe tener una interfaz simple hacia el resto del sistema (inyectas un agente, obtienes un agente controlado) pero una implementacion rica y profunda que maneja toda la complejidad de control, monitoreo y seguridad. El usuario del agente no deberia tener que preocuparse por los detalles del harness; simplemente deberia poder confiar en que el agente esta bajo control.

Un Agent Harness se compone de seis subsistemas:

1. **Guardrails**: barreras de contencion que validan las entradas y salidas del agente.
2. **Circuit breakers**: mecanismos que cortan la ejecucion cuando algo sale mal.
3. **Rate limiters y presupuestos**: controles de velocidad y gasto (tokens, tiempo, dinero).
4. **Sandboxing**: aislamiento del agente respecto al sistema y al mundo exterior.
5. **Logging y tracing**: registro detallado de cada decision y accion.
6. **Metricas y alertas**: observabilidad en tiempo real del comportamiento del agente.

Cada uno de estos subsistemas resuelve un tipo especifico de fallo:

| Subsistema | Fallo que previene | Ejemplo del Cap. 0 |
|---|---|---|
| Guardrails | Acciones fuera de alcance | El DELETE sin WHERE |
| Circuit breakers | Loops infinitos, gastos descontrolados | El loop de $47,000 |
| Rate limiters | Consumo excesivo de recursos | Agente que hace 847 llamadas API |
| Sandboxing | Ejecucion de codigo malicioso | Agente que ejecuta DROP TABLE |
| Logging/tracing | Fallo silencioso ("todo OK" pero nada funciona) | Dashboard mostrando 200 OK |
| Metricas/alertas | Deteccion tardia de anomalias | 11 dias sin que nadie note el loop |

---

## 5.2 El principio de minimo privilegio aplicado a agentes

El principio de minimo privilegio (*Principle of Least Privilege*, PoLP) es uno de los fundamentos de la seguridad informatica desde que Saltzer y Schroeder lo formalizaron en 1975. La idea es simple: cada componente de un sistema solo debe tener acceso a los recursos que necesita para cumplir su funcion, nada mas.

Aplicado a agentes de IA, este principio se vuelve critico. En el OWASP Top 10 para LLMs [OWASP, 2025], la vulnerabilidad de **"Excessive Agency"** (agencia excesiva) esta entre las mas peligrosas. Ocurre cuando un agente tiene permisos que exceden lo que necesita para su tarea. El agente de servicio al cliente del Capitulo 0 que podia leer la base de datos *y tambien* ejecutar queries de escritura tenia exactamente este perfil.

### Permisos granulares por accion

La implementacion correcta del minimo privilegio en agentes requiere pensar en permisos a nivel de *accion*, no de *herramienta*. No basta con decir "el agente puede usar la herramienta de base de datos". Necesitas especificar:

- **Que operaciones** puede hacer: solo SELECT, no INSERT ni DELETE.
- **Sobre que datos**: solo la tabla `products`, no `users`.
- **Con que frecuencia**: maximo 10 queries por minuto.
- **Con que alcance**: solo registros del usuario actual, no de todos los usuarios.

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable


class Permission(Enum):
    """Permisos granulares para acciones de agentes."""
    DB_READ = "db:read"
    DB_WRITE = "db:write"
    API_CALL = "api:call"
    FILE_READ = "file:read"
    FILE_WRITE = "file:write"
    EMAIL_SEND = "email:send"
    CODE_EXECUTE = "code:execute"


@dataclass
class AgentPermissions:
    """Define los permisos granulares de un agente.

    Los permisos se definen a nivel de accion (no de herramienta)
    y pueden incluir filtros de alcance por contexto.
    """
    allowed: set[Permission] = field(default_factory=set)
    rate_limits: dict[Permission, int] = field(
        default_factory=dict
    )  # acciones/minuto
    scope_filters: dict[Permission, Callable] = field(
        default_factory=dict
    )

    def check(self, permission: Permission, context: dict) -> bool:
        """Verifica si una accion esta permitida en el contexto dado."""
        if permission not in self.allowed:
            return False
        if permission in self.scope_filters:
            return self.scope_filters[permission](context)
        return True


# Ejemplo: un agente de soporte solo puede leer datos
# y enviar emails, con restricciones de alcance
support_agent_permissions = AgentPermissions(
    allowed={Permission.DB_READ, Permission.EMAIL_SEND},
    rate_limits={
        Permission.DB_READ: 20,    # 20 queries por minuto
        Permission.EMAIL_SEND: 5,  # 5 emails por minuto
    },
    scope_filters={
        Permission.DB_READ: lambda ctx: ctx.get("table") in (
            "products", "orders"
        ),
    },
)

# Ejemplo: un agente de analisis puede leer todo pero
# no puede escribir ni ejecutar codigo
analysis_agent_permissions = AgentPermissions(
    allowed={Permission.DB_READ, Permission.API_CALL, Permission.FILE_READ},
    rate_limits={
        Permission.DB_READ: 50,
        Permission.API_CALL: 10,
    },
)
```

Este enfoque es radicalmente diferente a lo que hacen muchos frameworks de agentes hoy, donde el agente tiene acceso completo a todas las herramientas que se le registran. La filosofia UNIX de "cada programa hace una cosa bien" aplica perfectamente aqui: cada agente debe tener un conjunto minimo de capacidades, bien definidas y bien acotadas.

### La regla de la confirmacion humana

Para acciones con consecuencias irreversibles, el minimo privilegio incluye un componente humano. El agente puede *proponer* acciones destructivas, pero un humano debe *aprobarlas*. Esto se conoce como el patron **Human-in-the-Loop** (HITL). No es una debilidad del sistema; es una fortaleza. Reconoce honestamente que los LLMs pueden equivocarse y que ciertas acciones no tienen un boton de "deshacer".

```python
from enum import Enum


class ApprovalLevel(Enum):
    AUTO = "auto"           # Se ejecuta sin aprobacion
    NOTIFY = "notify"       # Se ejecuta y notifica
    APPROVE = "approve"     # Requiere aprobacion humana antes


# Clasificacion de acciones por nivel de aprobacion
ACTION_APPROVAL_MAP = {
    "search_web": ApprovalLevel.AUTO,
    "read_database": ApprovalLevel.AUTO,
    "send_email": ApprovalLevel.NOTIFY,
    "update_record": ApprovalLevel.APPROVE,
    "delete_record": ApprovalLevel.APPROVE,
    "execute_code": ApprovalLevel.APPROVE,
    "transfer_funds": ApprovalLevel.APPROVE,
}


def requires_human_approval(action: str) -> bool:
    """Determina si una accion requiere aprobacion humana."""
    level = ACTION_APPROVAL_MAP.get(action, ApprovalLevel.APPROVE)
    return level == ApprovalLevel.APPROVE
```

La implementacion del HITL en produccion tipicamente involucra un sistema de colas donde las acciones pendientes de aprobacion se almacenan con un timeout. Si nadie aprueba en N minutos, la accion se cancela y el agente recibe una notificacion de que debe buscar una alternativa.

---

## 5.3 Guardrails: validacion de entrada y salida en runtime

Los guardrails son las barreras que verifican que entra al agente y que sale de el. Imaginalos como los muros de contencion en una carretera de montana: no te impiden conducir, pero evitan que te vayas al precipicio.

### Input guardrails: validar que entra

Los input guardrails filtran y validan lo que llega al agente antes de que lo procese:

- **Deteccion de prompt injection**: identificar intentos de manipular las instrucciones del agente.
- **Validacion de formato**: asegurar que los datos de entrada cumplen los esquemas esperados.
- **Filtrado de contenido**: detectar contenido que viola las politicas del sistema.
- **Limites de tamano**: evitar que entradas excesivamente grandes agoten los recursos.

```python
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class GuardrailResult:
    """Resultado de una validacion de guardrail."""
    passed: bool
    reason: str = ""
    modified_input: Any = None


class InputGuardrail:
    """Pipeline de validacion de entrada.

    Ejecuta una lista de validadores en secuencia.
    Si alguno falla, rechaza la entrada.
    Si alguno modifica la entrada, pasa la version
    modificada al siguiente validador.
    """

    def __init__(self, validators: list[Callable]):
        self.validators = validators

    def validate(
        self, user_input: str, context: dict
    ) -> GuardrailResult:
        for validator in self.validators:
            result = validator(user_input, context)
            if not result.passed:
                return result
            if result.modified_input is not None:
                user_input = result.modified_input
        return GuardrailResult(passed=True, modified_input=user_input)


# --- Validadores individuales ---

def detect_injection(
    user_input: str, context: dict
) -> GuardrailResult:
    """Deteccion BASICA de prompt injection por patrones.

    ADVERTENCIA: esta deteccion por substrings NO es una
    proteccion real. Un atacante la evade trivialmente con
    variaciones ortograficas, Unicode homoglyphs o
    reformulaciones. En produccion, usa un clasificador
    entrenado o un guardrail basado en LLM como segunda capa.
    """
    suspicious_patterns = [
        "ignora las instrucciones",
        "ignore previous instructions",
        "olvida tu sistema",
        "actua como si fueras",
        "you are now",
        "system prompt override",
        "jailbreak",
    ]
    input_lower = user_input.lower()
    for pattern in suspicious_patterns:
        if pattern in input_lower:
            return GuardrailResult(
                passed=False,
                reason=(
                    f"Posible inyeccion de prompt: '{pattern}'"
                ),
            )
    return GuardrailResult(passed=True)


def limit_input_length(
    user_input: str, context: dict
) -> GuardrailResult:
    """Rechaza entradas que exceden un limite de caracteres."""
    max_length = context.get("max_input_length", 4000)
    if len(user_input) > max_length:
        return GuardrailResult(
            passed=False,
            reason=f"Entrada excede el limite de {max_length} caracteres",
        )
    return GuardrailResult(passed=True)
```

### Output guardrails: validar que sale

Los output guardrails son igual de importantes, quizas mas. Mientras que los input guardrails protegen al agente del mundo, los output guardrails protegen al mundo del agente. Verifican que las respuestas y acciones del agente sean conformes al formato esperado, libres de informacion sensible, coherentes con la tarea y seguras para ejecutar.

```python
import re


def detect_sensitive_data(
    output: str, context: dict
) -> GuardrailResult:
    """Detecta datos sensibles en la salida del agente.

    NOTA: estos patrones son aproximaciones. La regex de
    tarjetas de credito captura falsos positivos y tiene
    falsos negativos. En produccion, complementa con
    validacion de checksum (Luhn) y patrones por emisor.
    """
    patterns = {
        "credit_card": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
        "api_key": r"\b(sk-|pk_|api[_-]key[_-]?)[a-zA-Z0-9]{20,}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "email_internal": r"\b[A-Za-z0-9._%+-]+@(internal|corp)\.[a-z]+\b",
    }
    for data_type, pattern in patterns.items():
        if re.search(pattern, output):
            return GuardrailResult(
                passed=False,
                reason=f"Dato sensible detectado: {data_type}",
            )
    return GuardrailResult(passed=True)


def validate_json_output(
    output: str, context: dict
) -> GuardrailResult:
    """Verifica que la salida sea JSON valido si se espera JSON."""
    import json

    if not context.get("expect_json", False):
        return GuardrailResult(passed=True)
    try:
        json.loads(output)
        return GuardrailResult(passed=True)
    except json.JSONDecodeError as e:
        return GuardrailResult(
            passed=False,
            reason=f"JSON invalido: {e}",
        )
```

### Guardrails deterministicos vs guardrails basados en LLM

Existen dos tipos fundamentales de guardrails, y la distincion es critica:

**Guardrails deterministicos** usan reglas fijas: expresiones regulares, listas de bloqueo, validaciones de esquema JSON, limites numericos. Son rapidos (microsegundos), predecibles (siempre producen el mismo resultado para la misma entrada) y no se pueden evadir con creatividad linguistica.

**Guardrails basados en LLM** usan otro modelo de lenguaje para evaluar si la entrada o salida del agente es aceptable. Son mas flexibles y pueden entender el *significado* de un texto, no solo su forma. Pero tienen un problema profundo: son vulnerables a los mismos ataques que intentan prevenir. Si un atacante puede manipular al agente principal con prompt injection, potencialmente puede manipular al modelo guardian tambien.

La estrategia correcta es **combinar ambos tipos** en un patron de capas:

```python
class LayeredGuardrail:
    """Guardrail en capas: primero deterministico, luego LLM.

    La primera capa es rapida, barata y confiable.
    La segunda capa es mas inteligente pero mas costosa
    y menos predecible. Solo se invoca si la primera
    capa no detecta problemas.
    """

    def __init__(
        self,
        deterministic_checks: list[Callable],
        llm_check: Callable | None = None,
    ):
        self.deterministic = deterministic_checks
        self.llm_check = llm_check

    def validate(
        self, text: str, context: dict
    ) -> GuardrailResult:
        # Capa 1: checks rapidos y deterministicos
        for check in self.deterministic:
            result = check(text, context)
            if not result.passed:
                return result

        # Capa 2: check semantico con LLM (mas lento, mas caro)
        if self.llm_check is not None:
            return self.llm_check(text, context)

        return GuardrailResult(passed=True)


# Ejemplo de uso
output_guardrail = LayeredGuardrail(
    deterministic_checks=[
        detect_sensitive_data,
        validate_json_output,
    ],
    llm_check=None,  # Agregar un clasificador LLM en produccion
)
```

Un guardrail que el agente puede aprender a evadir no es un guardrail, es una sugerencia. La solucion no es hacer guardrails mas inteligentes indefinidamente (eso es una carrera armamentista perdida). La solucion es implementar **defensa en profundidad**: multiples capas de proteccion independientes, de modo que evadir una capa no comprometa todo el sistema. Es el mismo principio que usamos en seguridad de redes: firewalls, IDS, segmentacion, cifrado.

---

## 5.4 Circuit breakers: cuando cortar la ejecucion

El patron **Circuit Breaker**, popularizado por Michael Nygard en *Release It!* [Nygard, 2007], fue disenado para sistemas distribuidos: cuando un servicio externo falla repetidamente, dejas de llamarlo por un tiempo para evitar cascadas de fallos. Aplicado a agentes de IA, este patron se vuelve aun mas importante porque los fallos de un agente no son solo tecnicos --pueden tener consecuencias en el mundo real.

### Cuando activar el circuit breaker

Un circuit breaker para agentes debe activarse cuando detecta:

- **Loops de razonamiento**: el agente repite las mismas acciones en ciclos. Un agente que intenta resolver un error llamando a la misma herramienta con los mismos parametros diez veces es un agente atrapado en un loop.
- **Consumo excesivo de tokens**: el agente esta gastando mas tokens de lo esperado. Esto puede indicar que esta "divagando" o que la tarea es mas compleja de lo anticipado.
- **Tiempo excesivo**: si un agente lleva 10 minutos en una tarea que deberia tomar 30 segundos, algo anda mal.
- **Errores consecutivos**: si las ultimas N llamadas a herramientas fallaron, el agente probablemente no va a resolver el problema por si solo.

```python
import time
from collections import deque
from dataclasses import dataclass, field


@dataclass
class CircuitBreakerConfig:
    """Configuracion del circuit breaker.

    Cada umbral es un punto de corte independiente.
    Si cualquiera se excede, el breaker se activa.
    """
    max_iterations: int = 50
    max_tokens: int = 100_000
    max_time_seconds: float = 300.0  # 5 minutos
    max_consecutive_errors: int = 5
    max_cost_usd: float = 5.0
    loop_detection_window: int = 10
    loop_similarity_threshold: float = 0.9


class AgentCircuitBreaker:
    """Circuit breaker que detiene al agente cuando detecta
    comportamiento anomalo.

    A diferencia de un circuit breaker de microservicios
    (que tiene estados Open/Half-Open/Closed), este opera
    por tarea: se inicializa al comenzar una tarea y
    se consulta en cada iteracion del loop agentico.
    """

    def __init__(self, config: CircuitBreakerConfig):
        self.config = config
        self.iterations = 0
        self.tokens_used = 0
        self.cost_usd = 0.0
        self.start_time = time.time()
        self.consecutive_errors = 0
        self.recent_actions: deque = deque(
            maxlen=config.loop_detection_window
        )

    def record_iteration(
        self,
        action: str,
        tokens: int,
        cost: float = 0.0,
        success: bool = True,
    ):
        """Registra una iteracion del loop agentico."""
        self.iterations += 1
        self.tokens_used += tokens
        self.cost_usd += cost
        self.recent_actions.append(action)

        if success:
            self.consecutive_errors = 0
        else:
            self.consecutive_errors += 1

    def should_trip(self) -> tuple[bool, str]:
        """Verifica si el circuit breaker debe activarse.

        Retorna (True, razon) si debe activarse,
        (False, "") si todo esta dentro de limites.
        """
        elapsed = time.time() - self.start_time

        if self.iterations >= self.config.max_iterations:
            return True, (
                f"Limite de iteraciones: {self.iterations}"
            )

        if self.tokens_used >= self.config.max_tokens:
            return True, (
                f"Presupuesto de tokens agotado: {self.tokens_used:,}"
            )

        if elapsed >= self.config.max_time_seconds:
            return True, (
                f"Tiempo maximo excedido: {elapsed:.1f}s"
            )

        if self.consecutive_errors >= self.config.max_consecutive_errors:
            return True, (
                f"Errores consecutivos: {self.consecutive_errors}"
            )

        if self.cost_usd >= self.config.max_cost_usd:
            return True, (
                f"Presupuesto economico agotado: ${self.cost_usd:.2f}"
            )

        if self._detect_loop():
            return True, "Loop de razonamiento detectado"

        return False, ""

    def _detect_loop(self) -> bool:
        """Detecta si el agente esta atrapado en un loop.

        Compara la primera y segunda mitad de las acciones
        recientes. Si son iguales (o casi), hay un ciclo.
        """
        actions = list(self.recent_actions)
        if len(actions) < self.config.loop_detection_window:
            return False

        mid = len(actions) // 2
        first_half = actions[:mid]
        second_half = actions[mid : mid + len(first_half)]
        matches = sum(
            1 for a, b in zip(first_half, second_half) if a == b
        )
        similarity = matches / len(first_half) if first_half else 0
        return similarity >= self.config.loop_similarity_threshold

    def reset(self):
        """Reinicia el circuit breaker para una nueva tarea."""
        self.iterations = 0
        self.tokens_used = 0
        self.cost_usd = 0.0
        self.start_time = time.time()
        self.consecutive_errors = 0
        self.recent_actions.clear()
```

### Fallbacks: que hacer cuando el circuit breaker se activa

Cuando el circuit breaker corta la ejecucion, necesitas un plan B. El circuit breaker no es un interruptor binario; es el inicio de un flujo de **degradacion elegante** (*graceful degradation*). Las opciones, en orden de preferencia:

1. **Respuesta parcial**: devuelve al usuario lo que el agente logro hasta el momento de la interrupcion. Si el agente completo 3 de 5 pasos, esos 3 pasos pueden ser utiles.
2. **Escalacion humana**: notificar a un operador humano para que tome el control. En un chatbot de soporte, esto es frecuentemente lo correcto.
3. **Modelo de respaldo**: reintentar con un modelo menos capaz pero mas predecible y barato. Si el modelo frontera fallo por un loop de razonamiento, un modelo mas pequeno con instrucciones mas estrictas puede resolver la tarea.
4. **Cache**: si la pregunta es similar a una anterior, devolver la respuesta cacheada.
5. **Respuesta generica**: el ultimo recurso. Mejor que nada, pero solo si las opciones anteriores no aplican.

```python
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class FallbackChain:
    """Cadena de fallbacks que se ejecuta cuando el circuit
    breaker se activa.

    Cada fallback se prueba en orden hasta que uno tiene exito.
    """
    strategies: list[Callable]

    def execute(
        self, task: str, partial_result: Any, trip_reason: str
    ) -> dict:
        for strategy in self.strategies:
            try:
                result = strategy(task, partial_result, trip_reason)
                if result is not None:
                    return {
                        "success": True,
                        "result": result,
                        "fallback": strategy.__name__,
                    }
            except Exception:
                continue
        return {
            "success": False,
            "error": f"Todos los fallbacks fallaron. Trip: {trip_reason}",
        }


def return_partial(task, partial, reason):
    """Retorna el resultado parcial si existe."""
    if partial:
        return f"Resultado parcial (ejecucion interrumpida: {reason}): {partial}"
    return None


def escalate_to_human(task, partial, reason):
    """Escala a un operador humano."""
    # En produccion, esto envia a una cola de soporte
    return (
        f"Esta tarea ha sido escalada a un operador humano. "
        f"Razon: {reason}. Contexto parcial disponible."
    )


# Configuracion tipica de fallbacks
default_fallbacks = FallbackChain(
    strategies=[
        return_partial,
        escalate_to_human,
    ]
)
```

---

## 5.5 Rate limiting y presupuestos: tu agente necesita limite de gasto

Un concepto que se vuelve critico en produccion es el **presupuesto por tarea**. No solo cuantos tokens puede usar un agente en total, sino cuantos puede usar *por tarea individual*. Esto conecta directamente con la realidad economica de operar agentes: una llamada a un modelo frontera con una ventana de contexto grande puede costar varios dolares. Un agente en loop puede generar facturas de miles de dolares en minutos.

### Presupuestos a multiples niveles

Un sistema de produccion necesita presupuestos jerarquicos:

```python
import time
from dataclasses import dataclass, field


@dataclass
class Budget:
    """Control de presupuesto para una tarea de agente.

    Cada dimension (tokens, costo, llamadas API) es un
    limite independiente. Si cualquiera se agota, la tarea
    se detiene.
    """
    max_tokens: int
    max_cost_usd: float
    max_api_calls: int
    max_wall_time_seconds: float = 300.0

    tokens_used: int = 0
    cost_usd: float = 0.0
    api_calls: int = 0
    start_time: float = field(default_factory=time.time)

    def consume(self, tokens: int, cost: float):
        """Registra consumo de una llamada al LLM."""
        self.tokens_used += tokens
        self.cost_usd += cost
        self.api_calls += 1

    def is_exhausted(self) -> tuple[bool, str]:
        """Verifica si algun limite se alcanzo."""
        if self.tokens_used >= self.max_tokens:
            return True, (
                f"Tokens: {self.tokens_used:,}/{self.max_tokens:,}"
            )
        if self.cost_usd >= self.max_cost_usd:
            return True, (
                f"Costo: ${self.cost_usd:.2f}/${self.max_cost_usd:.2f}"
            )
        if self.api_calls >= self.max_api_calls:
            return True, (
                f"Llamadas API: {self.api_calls}/{self.max_api_calls}"
            )
        elapsed = time.time() - self.start_time
        if elapsed >= self.max_wall_time_seconds:
            return True, (
                f"Tiempo: {elapsed:.0f}s/{self.max_wall_time_seconds:.0f}s"
            )
        return False, ""

    @property
    def remaining_tokens(self) -> int:
        return max(0, self.max_tokens - self.tokens_used)

    @property
    def remaining_cost(self) -> float:
        return max(0.0, self.max_cost_usd - self.cost_usd)


@dataclass
class BudgetManager:
    """Gestiona presupuestos a multiples niveles.

    En produccion, necesitas limites en cuatro niveles:
    - Por request: limite duro por tarea individual
    - Por sesion: acumula el gasto de una conversacion
    - Por usuario/tenant: limites diarios o mensuales
    - Global: circuit breaker financiero del sistema completo
    """
    per_request: Budget
    per_session: Budget
    per_user: Budget

    def can_proceed(self) -> tuple[bool, str]:
        """Verifica los tres niveles de presupuesto."""
        for name, budget in [
            ("request", self.per_request),
            ("session", self.per_session),
            ("user", self.per_user),
        ]:
            exhausted, reason = budget.is_exhausted()
            if exhausted:
                return False, f"Presupuesto {name} agotado: {reason}"
        return True, ""

    def consume(self, tokens: int, cost: float):
        """Registra consumo en los tres niveles."""
        self.per_request.consume(tokens, cost)
        self.per_session.consume(tokens, cost)
        self.per_user.consume(tokens, cost)
```

### Alertas de anomalias de costo

Ademas del presupuesto, necesitas **alertas de anomalias**: si el costo promedio por tarea sube un 50% de un dia a otro, algo cambio (un prompt mas largo, un modelo diferente, un bug en el loop). Detectar estas anomalias temprano es la diferencia entre un susto y una catastrofe financiera.

```python
from collections import deque
import statistics


class CostAnomalyDetector:
    """Detecta anomalias en el costo de tareas del agente.

    Usa una ventana deslizante para calcular la media y
    desviacion estandar del costo historico. Una tarea
    que excede la media + N desviaciones estandar es
    anomala.
    """

    def __init__(
        self,
        window_size: int = 100,
        threshold_std: float = 2.5,
    ):
        self.costs: deque = deque(maxlen=window_size)
        self.threshold_std = threshold_std

    def record_cost(self, cost: float) -> dict | None:
        """Registra un costo y retorna una alerta si es anomalo."""
        if len(self.costs) < 10:
            self.costs.append(cost)
            return None

        mean = statistics.mean(self.costs)
        std = statistics.stdev(self.costs)
        threshold = mean + self.threshold_std * std

        self.costs.append(cost)

        if cost > threshold and std > 0:
            return {
                "alert": "cost_anomaly",
                "cost": cost,
                "mean": mean,
                "std": std,
                "threshold": threshold,
                "deviation": (cost - mean) / std,
            }
        return None
```

---

## 5.6 Sandboxing: aislamiento como defensa en profundidad

Si el principio de minimo privilegio es el "que" (que puede hacer el agente), el sandboxing es el "donde" (en que entorno se ejecutan sus acciones). Sandboxing significa ejecutar al agente en un entorno aislado donde sus acciones no pueden afectar al sistema principal.

### Por que necesitas sandboxing

El caso mas peligroso es un agente que genera y ejecuta codigo. En 2025-2026, con la popularidad de agentes de codigo como Claude Code, Codex, Devin y Cursor, la ejecucion de codigo generado por IA se ha vuelto rutinaria. Pero ejecutar codigo generado por un LLM en el mismo proceso o maquina que tu servicio es como darle root a un programa que acabas de descargar de Internet.

El incidente del Capitulo 0 --el agente de Replit que ejecuto un `DROP TABLE` en produccion y luego genero 4,000 registros falsos para cubrirlo-- es el ejemplo perfecto de por que el sandboxing no es opcional.

### Niveles de aislamiento

En la practica, hay tres niveles de aislamiento con trade-offs diferentes:

**Nivel 1 -- Proceso aislado**: el agente corre en su propio proceso con recursos limitados. Aislamiento minimo: comparten kernel y filesystem. Adecuado para agentes que solo generan texto, no ejecutan codigo.

**Nivel 2 -- Contenedor**: el agente corre en un contenedor Docker con filesystem y red aislados. Es el minimo aceptable para agentes que ejecutan codigo. Sin embargo, Docker comparte el kernel del host, asi que una vulnerabilidad de escape de contenedor (container escape) da acceso al host completo.

**Nivel 3 -- MicroVM**: el agente corre en una maquina virtual ligera (Firecracker, gVisor). Cada sandbox tiene su propio kernel, lo que proporciona aislamiento a nivel de hardware via KVM. Es el estandar de la industria en 2026 para ejecucion de codigo no confiable.

Las plataformas especializadas han madurado significativamente. E2B reporta que paso de 40,000 sesiones de sandbox por mes en marzo de 2024 a aproximadamente 15 millones por mes en marzo de 2025, con alrededor del 50% de las empresas Fortune 500 ejecutando cargas de trabajo agenticas en sus sandboxes [E2B, 2025]. Modal usa contenedores gVisor con soporte para GPUs. Daytona ofrece tiempos de arranque en frio de menos de 90ms con contenedores Kata.

### Implementacion basica de validacion de codigo

Antes de enviar codigo a un sandbox, una validacion a nivel de AST puede atrapar errores accidentales (aunque **no** es una defensa de seguridad contra un atacante sofisticado):

```python
import ast
from dataclasses import dataclass, field


@dataclass
class SandboxConfig:
    """Configuracion del sandbox para ejecucion de codigo."""
    max_memory_mb: int = 512
    max_cpu_seconds: int = 30
    allowed_imports: set[str] = field(
        default_factory=lambda: {
            "json", "math", "datetime", "re", "collections",
            "itertools", "functools", "typing", "dataclasses",
            "statistics", "decimal", "fractions",
        }
    )
    blocked_builtins: set[str] = field(
        default_factory=lambda: {
            "eval", "exec", "compile", "__import__",
            "open", "getattr", "setattr", "delattr",
            "globals", "locals", "breakpoint",
        }
    )


class CodeValidator:
    """Validacion estatica de codigo antes de enviarlo al sandbox.

    ADVERTENCIA: esta validacion AST es un filtro de conveniencia
    que atrapa errores accidentales. NO es una barrera de seguridad.
    Un atacante sofisticado puede evadirla con f-strings,
    construccion dinamica de strings u otras tecnicas de
    ofuscacion. La defensa real es el contenedor aislado.
    """

    def __init__(self, config: SandboxConfig):
        self.config = config

    def validate(self, code: str) -> GuardrailResult:
        # 1. Parsear el AST
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return GuardrailResult(
                passed=False, reason=f"Error de sintaxis: {e}"
            )

        # 2. Verificar imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module = alias.name.split(".")[0]
                    if module not in self.config.allowed_imports:
                        return GuardrailResult(
                            passed=False,
                            reason=f"Import no permitido: {module}",
                        )
            elif isinstance(node, ast.ImportFrom) and node.module:
                module = node.module.split(".")[0]
                if module not in self.config.allowed_imports:
                    return GuardrailResult(
                        passed=False,
                        reason=f"Import no permitido: {module}",
                    )

        # 3. Verificar llamadas a funciones peligrosas
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if (
                    isinstance(node.func, ast.Name)
                    and node.func.id in self.config.blocked_builtins
                ):
                    return GuardrailResult(
                        passed=False,
                        reason=(
                            f"Llamada bloqueada: {node.func.id}"
                        ),
                    )

        return GuardrailResult(passed=True)
```

**La defensa real es el contenedor.** En produccion, jamas ejecutes codigo generado por un LLM en el mismo proceso o maquina que tu servicio. La interfaz de un sandbox de produccion se reduce a esto:

```python
from dataclasses import dataclass


@dataclass
class SandboxResult:
    success: bool
    stdout: str = ""
    stderr: str = ""
    error: str = ""
    execution_time_ms: float = 0.0


class ProductionSandbox:
    """Interfaz para sandbox de produccion.

    Implementaciones reales: E2B (Firecracker microVMs),
    Modal (gVisor), Daytona (Kata containers),
    o tu propio Docker con gVisor.

    Cada llamada a execute() crea un contenedor efimero
    que se destruye al terminar.
    """

    async def execute(
        self,
        code: str,
        timeout_seconds: int = 30,
        memory_limit_mb: int = 512,
    ) -> SandboxResult:
        # Envia el codigo a un contenedor efimero aislado
        # a traves de una API. Nunca ejecuta en el proceso actual.
        ...
```

---

## 5.7 Observabilidad: logs, traces y metricas para agentes

La observabilidad en sistemas agenticos es fundamentalmente mas dificil que en sistemas tradicionales porque las decisiones no son deterministas y el "por que" de cada accion esta enterrado en las representaciones internas del modelo. Cuando un agente toma una decision incorrecta en produccion, necesitas poder reconstruir su cadena de razonamiento completa.

### Tracing distribuido para agentes

El estandar OpenTelemetry, que ya es el estandar *de facto* para tracing distribuido, se adapta naturalmente a los sistemas agenticos. Cada ejecucion de un agente genera un **trace** compuesto por **spans**:

- **Span raiz**: la tarea completa del agente.
- **Span de razonamiento**: cada paso de pensamiento del agente.
- **Span de herramienta**: cada llamada a una herramienta externa.
- **Span de LLM**: cada llamada al modelo de lenguaje.
- **Span de guardrail**: cada validacion de entrada/salida.

```python
from contextlib import contextmanager
from dataclasses import dataclass, field
import time as time_module
import uuid
import logging

logger = logging.getLogger("agent_harness")


@dataclass
class Span:
    """Un span de tracing para agentes."""
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

    @property
    def duration_ms(self) -> float | None:
        if self.end_time is None:
            return None
        return (self.end_time - self.start_time) * 1000


class AgentTracer:
    """Trazador ligero para agentes de IA.

    En produccion, reemplaza esto con OpenTelemetry real
    y exporta a tu backend de observabilidad (Jaeger,
    Datadog, etc.).
    """

    def __init__(self):
        self.spans: list[Span] = []
        self.current_trace_id = str(uuid.uuid4())

    @contextmanager
    def span(
        self,
        name: str,
        parent_id: str | None = None,
        **attributes,
    ):
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
                    "duration_ms": s.duration_ms,
                    "status": s.status,
                    **s.attributes,
                },
            )

    def get_trace_summary(self) -> dict:
        """Resume el trace completo para inspeccion."""
        return {
            "trace_id": self.current_trace_id,
            "total_spans": len(self.spans),
            "total_duration_ms": sum(
                s.duration_ms for s in self.spans
                if s.duration_ms is not None
            ),
            "errors": [
                s.name for s in self.spans
                if s.status.startswith("ERROR")
            ],
        }
```

### Metricas clave para agentes en produccion

Las metricas que debes monitorear van mas alla de las tipicas de un servicio web:

| Metrica | Que te dice | Alerta si... |
|---|---|---|
| Latencia por tarea (P50/P95/P99) | Cuanto tarda el agente en completar una tarea | P95 > umbral del SLA |
| Costo por tarea | Cuanto cuesta en tokens/dinero cada tarea | > presupuesto asignado |
| Tasa de exito | Porcentaje de tareas completadas exitosamente | < 90% |
| Tasa de escalacion | Porcentaje que requiere intervencion humana | Aumento repentino |
| Profundidad de razonamiento | Cuantos pasos toma el agente por tarea | Aumento sin mejora en calidad |
| Tasa de trips del circuit breaker | Con que frecuencia se activa el circuit breaker | > 5% de las tareas |
| Tokens desperdiciados | Tokens usados en loops, reintentos fallidos | > 20% del total |
| Tasa de rechazo de guardrails | Porcentaje de entradas/salidas rechazadas | Cambio brusco en cualquier direccion |

En produccion, OpenTelemetry se complementa con herramientas de observabilidad especificas para agentes como **LangSmith**, **Langfuse** y **Arize Phoenix**, que ademas de traces ofrecen metricas de costo por request, dashboards de calidad de respuesta y evaluaciones automaticas.

---

## 5.8 Uniendo las piezas: un harness completo en Python

Ahora vamos a integrar todos los componentes en un harness completo que puedas usar como punto de partida. Este ejemplo usa el patron decorador para crear un sistema modular:

```python
from functools import wraps
from typing import Any, Callable
import logging
import time as time_mod

logger = logging.getLogger("agent_harness")


class AgentHarness:
    """Harness completo para agentes de IA.

    Envuelve cualquier funcion de agente con el pipeline
    completo de control: input guardrails -> verificacion
    de presupuesto -> ejecucion -> output guardrails ->
    circuit breaker check -> logging.

    Uso:
        harness = AgentHarness(
            permissions=support_agent_permissions,
            input_guardrails=[detect_injection, limit_input_length],
            output_guardrails=[detect_sensitive_data],
            circuit_breaker_config=CircuitBreakerConfig(),
            budget=Budget(max_tokens=50_000, max_cost_usd=1.0,
                          max_api_calls=20, max_wall_time_seconds=120),
        )

        @harness.wrap
        def my_agent(task: str) -> str:
            # Tu logica de agente aqui
            return result
    """

    def __init__(
        self,
        permissions: AgentPermissions,
        input_guardrails: list[Callable] | None = None,
        output_guardrails: list[Callable] | None = None,
        circuit_breaker_config: CircuitBreakerConfig | None = None,
        budget: Budget | None = None,
        fallbacks: FallbackChain | None = None,
    ):
        self.permissions = permissions
        self.input_guard = InputGuardrail(input_guardrails or [])
        self.output_guard = InputGuardrail(output_guardrails or [])
        self.circuit_breaker = AgentCircuitBreaker(
            circuit_breaker_config or CircuitBreakerConfig()
        )
        self.budget = budget or Budget(
            max_tokens=100_000,
            max_cost_usd=5.0,
            max_api_calls=50,
        )
        self.fallbacks = fallbacks or default_fallbacks
        self.tracer = AgentTracer()

    def wrap(self, agent_fn: Callable) -> Callable:
        """Decorador que envuelve una funcion de agente
        con el harness completo."""

        @wraps(agent_fn)
        def wrapped(task: str, **kwargs) -> dict[str, Any]:
            with self.tracer.span(
                "agent_execution", task=task
            ) as root_span:

                # 1. Input guardrails
                with self.tracer.span(
                    "input_validation",
                    parent_id=root_span.span_id,
                ):
                    input_result = self.input_guard.validate(
                        task, kwargs
                    )
                    if not input_result.passed:
                        logger.warning(
                            f"Input rechazado: {input_result.reason}"
                        )
                        return {
                            "success": False,
                            "error": input_result.reason,
                            "stage": "input_guardrail",
                        }
                    if input_result.modified_input is not None:
                        task = input_result.modified_input

                # 2. Verificar presupuesto
                exhausted, reason = self.budget.is_exhausted()
                if exhausted:
                    logger.warning(
                        f"Presupuesto agotado: {reason}"
                    )
                    return {
                        "success": False,
                        "error": reason,
                        "stage": "budget_check",
                    }

                # 3. Ejecutar agente
                result = None
                try:
                    with self.tracer.span(
                        "agent_logic",
                        parent_id=root_span.span_id,
                    ):
                        result = agent_fn(task, **kwargs)
                except Exception as e:
                    logger.error(f"Agente fallo: {e}")
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
                    "output_validation",
                    parent_id=root_span.span_id,
                ):
                    output_text = str(result)
                    output_result = self.output_guard.validate(
                        output_text, kwargs
                    )
                    if not output_result.passed:
                        logger.warning(
                            f"Output rechazado: {output_result.reason}"
                        )
                        return {
                            "success": False,
                            "error": output_result.reason,
                            "stage": "output_guardrail",
                        }

                # 5. Circuit breaker check
                trip, trip_reason = self.circuit_breaker.should_trip()
                if trip:
                    logger.error(
                        f"Circuit breaker: {trip_reason}"
                    )
                    # Intentar fallbacks
                    return self.fallbacks.execute(
                        task, result, trip_reason
                    )

                return {"success": True, "result": result}

        return wrapped
```

Y asi se usa en la practica:

```python
# Configurar el harness
harness = AgentHarness(
    permissions=AgentPermissions(
        allowed={Permission.DB_READ, Permission.API_CALL},
        rate_limits={
            Permission.DB_READ: 10,
            Permission.API_CALL: 5,
        },
    ),
    input_guardrails=[detect_injection, limit_input_length],
    output_guardrails=[detect_sensitive_data],
    circuit_breaker_config=CircuitBreakerConfig(
        max_iterations=30,
        max_tokens=50_000,
        max_time_seconds=120.0,
        max_cost_usd=1.0,
    ),
    budget=Budget(
        max_tokens=50_000,
        max_cost_usd=1.0,
        max_api_calls=20,
    ),
)


# Envolver tu agente con el harness
@harness.wrap
def customer_support_agent(task: str, **kwargs) -> str:
    """Agente de soporte al cliente con harness de seguridad."""
    # Aqui va la logica de tu agente: llamadas al LLM,
    # uso de herramientas, razonamiento, etc.
    response = call_llm(task)  # Tu funcion de LLM
    return response


# Ejecutar de forma segura
result = customer_support_agent(
    "Cual es el estado de mi pedido #12345?"
)
if result["success"]:
    print(result["result"])
else:
    print(f"Error en etapa '{result['stage']}': {result['error']}")
```

Este harness es deliberadamente simple. En produccion necesitarias agregar persistencia de traces, integracion con sistemas de alertas, un sistema de permisos mas sofisticado conectado a tu IAM, ejecucion asincrona de guardrails para no agregar latencia excesiva, y probablemente rate limiting con ventana deslizante en lugar de limites por minuto estrictos. Pero la estructura fundamental es la correcta: **cada accion del agente pasa por un pipeline de validacion, control y registro**.

---

## Takeaway del capitulo

El harness es lo que separa un prototipo de un sistema de produccion. Construye el harness antes de darle herramientas al agente, no despues.

Cada componente resuelve un problema real:

1. **Sin guardrails**, tu agente puede filtrar datos sensibles o ser manipulado por un atacante. La defensa en profundidad (deterministico + LLM) es la estrategia correcta.

2. **Sin circuit breakers**, tu agente puede entrar en un loop infinito y agotar tu presupuesto de tokens. Configura limites de iteraciones, tokens, tiempo, costo y deteccion de ciclos.

3. **Sin presupuestos**, no hay limite de gasto. Implementa presupuestos jerarquicos (por request, por sesion, por usuario, global) y alertas de anomalias.

4. **Sin sandboxing**, un agente que ejecuta codigo generado puede comprometer toda tu infraestructura. Usa microVMs (Firecracker) o contenedores con gVisor para aislamiento real.

5. **Sin observabilidad**, no tienes idea de por que tu agente hizo lo que hizo cuando algo sale mal. Tracing distribuido con OpenTelemetry y metricas especificas para agentes son el minimo.

6. **Sin minimo privilegio**, un agente comprometido tiene acceso a todo tu sistema. Define permisos a nivel de accion, no de herramienta, e implementa Human-in-the-Loop para acciones irreversibles.

La buena noticia es que no necesitas construir todo esto desde cero. Frameworks como Guardrails AI, NeMo Guardrails de NVIDIA, y las capacidades de guardrails integradas en los SDKs de OpenAI y Anthropic proporcionan piezas del rompecabezas. Pero entender los principios fundamentales te permite evaluar estas herramientas criticamente y adaptarlas a tus necesidades.

El harness no limita lo que tu agente puede lograr. Limita lo que puede destruir cuando se equivoca.

---

### Notas y referencias

- [Saltzer y Schroeder, 1975] J. H. Saltzer y M. D. Schroeder. "The Protection of Information in Computer Systems." *Proceedings of the IEEE*, 63(9). Formaliza el principio de minimo privilegio.
- [Nygard, 2007] Michael Nygard. *Release It! Design and Deploy Production-Ready Software*. Pragmatic Bookshelf. Introduce el patron Circuit Breaker para sistemas distribuidos.
- [Ousterhout, 2018] John Ousterhout. *A Philosophy of Software Design*. Yaknyam Press. Principios de modulos profundos aplicados al diseno del harness.
- [OWASP, 2025] "OWASP Top 10 for LLM Applications 2025." Define "Excessive Agency" como vulnerabilidad critica en sistemas con LLMs.
- [Bockeler, 2026] Birgitta Bockeler. "Harness Engineering." *martinfowler.com*. Define harness engineering como disciplina: context engineering + restricciones arquitectonicas + gestion de entropia.
- [OpenAI, 2026] "Harness Engineering: Leveraging Codex in an Agent-First World." *openai.com*. Caso practico: 1M lineas de codigo en 5 meses con harness para Codex.
- [E2B, 2025] E2B Platform. Datos de adopcion: 40K a 15M sesiones/mes en un ano, ~50% Fortune 500.
- [OpenTelemetry, 2024] OpenTelemetry Project. *OpenTelemetry Specification*. Estandar para tracing distribuido.
- [Greshake et al., 2023] Kai Greshake et al. "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection." *arXiv:2302.12173*.
- [Arize AI, 2025] "Why AI Agents Break: A Field Analysis of Production Failures." Arize Blog.
