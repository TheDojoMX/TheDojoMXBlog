# Capitulo 13: Patrones de Diseno para Sistemas con IA

> "Los patrones de diseno clasicos no desaparecen con la IA, se transforman."

---

En el Capitulo 12 exploramos las restricciones fisicas del hardware que determinan donde y como puedes correr tus agentes. Ahora vamos a subir un nivel de abstraccion: dado el hardware disponible y las caracteristicas peculiares de los sistemas basados en LLMs, como los disenamos?

Los sistemas con IA tienen propiedades fundamentalmente diferentes al software tradicional. Las respuestas son no deterministas. La latencia es variable e impredecible. Los costos escalan con el volumen de tokens, no con el volumen de peticiones. Los errores son sutiles: una respuesta incorrecta puede ser indistinguible de una correcta a menos que tengas conocimiento del dominio. Estas propiedades requieren patrones de diseno que manejen incertidumbre, costos y calidad de forma explicita.

Pero no estamos partiendo de cero. En 1994, la Gang of Four (GoF) publico *Design Patterns: Elements of Reusable Object-Oriented Software*, catalogando 23 patrones que siguen siendo la base del diseno de software [Gamma et al., 1994]. Esos patrones no desaparecen con la IA. Se transforman, se extienden y se combinan de formas nuevas.

Este capitulo presenta los patrones emergentes para sistemas con IA, los conecta con sus antecedentes clasicos y -- siguiendo el espiritu de "Building Effective Agents" de Anthropic [2024] -- enfatiza que la simplicidad sigue siendo la virtud principal.

---

## 13.1 El principio fundamental: separar la inteligencia de la logica

### El error mas comun

El error mas comun al construir sistemas con IA es mezclar llamadas a LLMs con la logica de negocio. Es como mezclar SQL directo en tus templates HTML: funciona en la demo, se convierte en pesadilla en produccion.

El LLM debe tratarse como un componente mas, aislado detras de interfaces claras. Es un "oraculo probabilistico" que genera hipotesis. La logica determinista que lo rodea decide que hacer con esas hipotesis.

Este principio conecta directamente con dos pilares del diseno clasico:

**Ocultamiento de informacion de Parnas [1972].** Los modulos deben ocultar decisiones de diseno que probablemente cambien. Tu aplicacion no debe saber si esta usando GPT-4, Claude o un modelo local. La interfaz es la misma; la implementacion esta oculta.

**Modulos profundos de Ousterhout [2018].** Un buen modulo tiene una interfaz simple y una implementacion rica. Un wrapper superficial de LLM que simplemente reenvie la peticion al API y devuelva el texto crudo viola este principio. Un modulo profundo anade validacion, reintentos, fallbacks, logging, metricas y transformacion de formato detras de una interfaz simple.

```python
"""
Anti-patron vs patron: integracion de LLM en logica de negocio.
"""

# === ANTI-PATRON: LLM mezclado con logica de negocio ===

import httpx


async def process_support_ticket_bad(ticket_text: str) -> dict:
    """NO HAGAS ESTO: logica de negocio mezclada con llamada al LLM."""
    # Llamada directa al API mezclada con logica
    response = await httpx.AsyncClient().post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": "Bearer sk-..."},
        json={
            "model": "gpt-4",
            "messages": [{"role": "user", "content": f"Clasifica: {ticket_text}"}],
        },
    )
    classification = response.json()["choices"][0]["message"]["content"]

    # Logica de negocio directamente acoplada al formato de respuesta
    if "urgente" in classification.lower():
        # Enviar alerta... pero que pasa si el LLM cambia su formato?
        pass

    return {"classification": classification}


# === PATRON CORRECTO: separacion de responsabilidades ===

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class TicketPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class TicketClassification:
    """Contrato tipado para la clasificacion de tickets."""
    priority: TicketPriority
    category: str
    confidence: float
    suggested_action: str


class Classifier(ABC):
    """Interfaz abstracta para clasificadores.

    Oculta si el clasificador es un LLM, un modelo ML clasico,
    o un conjunto de reglas. La logica de negocio no lo sabe ni le importa.
    """

    @abstractmethod
    async def classify(self, text: str) -> TicketClassification:
        ...


class LLMClassifier(Classifier):
    """Clasificador basado en LLM.

    Modulo profundo: interfaz simple, implementacion rica.
    Maneja reintentos, validacion, fallbacks y metricas internamente.
    """

    def __init__(self, model_client, fallback: "Classifier | None" = None):
        self.client = model_client
        self.fallback = fallback

    async def classify(self, text: str) -> TicketClassification:
        try:
            # Llamada al LLM con structured output
            raw = await self.client.generate_structured(
                prompt=f"Clasifica este ticket de soporte: {text}",
                schema=TicketClassification,
            )
            # Validacion semantica
            if raw.confidence < 0.3:
                raise ValueError("Confianza demasiado baja")
            return raw

        except Exception:
            if self.fallback:
                return await self.fallback.classify(text)
            # Default seguro: escalar a humano
            return TicketClassification(
                priority=TicketPriority.HIGH,
                category="requires_human_review",
                confidence=0.0,
                suggested_action="Escalar a agente humano",
            )


class RuleBasedClassifier(Classifier):
    """Clasificador deterministico basado en reglas.

    Funciona como fallback cuando el LLM falla.
    """

    KEYWORD_RULES = {
        "urgente": TicketPriority.HIGH,
        "caido": TicketPriority.CRITICAL,
        "error": TicketPriority.MEDIUM,
        "pregunta": TicketPriority.LOW,
    }

    async def classify(self, text: str) -> TicketClassification:
        text_lower = text.lower()
        for keyword, priority in self.KEYWORD_RULES.items():
            if keyword in text_lower:
                return TicketClassification(
                    priority=priority,
                    category="keyword_match",
                    confidence=0.6,
                    suggested_action=f"Detectado por keyword: {keyword}",
                )
        return TicketClassification(
            priority=TicketPriority.MEDIUM,
            category="unclassified",
            confidence=0.3,
            suggested_action="Requiere revision manual",
        )
```

La diferencia critica: la logica de negocio trabaja con `Classifier` y `TicketClassification`, no con strings crudos ni con APIs HTTP. Si cambias de proveedor de LLM, de modelo, o incluso de enfoque completo (de LLM a ML clasico), la logica de negocio no se entera.

---

## 13.2 Patron 1: AI Gateway (Puerta de enlace de IA)

### Descripcion y mecanica

El AI Gateway es un punto de entrada unico para todas las interacciones con modelos de IA en tu organizacion. Centraliza autenticacion, rate limiting, logging, caching, routing y metricas. Es el equivalente del API Gateway en microservicios, adaptado a las peculiaridades de los LLMs.

```python
"""
Implementacion de un AI Gateway para agentes de produccion.
"""

import time
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any
from collections import defaultdict
import asyncio


@dataclass
class GatewayConfig:
    """Configuracion del AI Gateway."""
    rate_limit_rpm: int = 60  # requests por minuto
    cache_ttl_seconds: int = 3600  # 1 hora
    max_tokens_per_request: int = 4096
    budget_limit_daily_usd: float = 100.0
    enable_logging: bool = True


@dataclass
class GatewayMetrics:
    """Metricas del gateway en tiempo real."""
    total_requests: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    total_tokens_used: int = 0
    total_cost_usd: float = 0.0
    errors: int = 0
    latency_sum_ms: float = 0.0

    @property
    def cache_hit_rate(self) -> float:
        total = self.cache_hits + self.cache_misses
        return self.cache_hits / total if total > 0 else 0.0

    @property
    def avg_latency_ms(self) -> float:
        return self.latency_sum_ms / self.total_requests if self.total_requests > 0 else 0.0


class AIGateway:
    """AI Gateway centralizado.

    Todas las llamadas a modelos de IA pasan por aqui.
    Responsabilidades:
    - Rate limiting por usuario/aplicacion
    - Caching de respuestas identicas
    - Tracking de costos y presupuesto
    - Logging estructurado de cada interaccion
    - Routing a diferentes proveedores/modelos
    """

    def __init__(self, config: GatewayConfig):
        self.config = config
        self.metrics = GatewayMetrics()
        self._cache: dict[str, tuple[Any, float]] = {}  # hash -> (response, timestamp)
        self._rate_limiter: dict[str, list[float]] = defaultdict(list)

    def _check_rate_limit(self, client_id: str) -> bool:
        """Verifica que el cliente no exceda el rate limit."""
        now = time.time()
        window_start = now - 60.0  # ventana de 1 minuto

        # Limpia timestamps viejos
        self._rate_limiter[client_id] = [
            ts for ts in self._rate_limiter[client_id]
            if ts > window_start
        ]

        if len(self._rate_limiter[client_id]) >= self.config.rate_limit_rpm:
            return False

        self._rate_limiter[client_id].append(now)
        return True

    def _cache_key(self, model: str, prompt: str, params: dict) -> str:
        """Genera clave de cache determinista."""
        content = json.dumps(
            {"model": model, "prompt": prompt, **params},
            sort_keys=True,
        )
        return hashlib.sha256(content.encode()).hexdigest()

    def _check_cache(self, key: str) -> Any | None:
        """Busca en cache. Retorna None si no hay hit o si expiro."""
        if key in self._cache:
            response, timestamp = self._cache[key]
            if time.time() - timestamp < self.config.cache_ttl_seconds:
                self.metrics.cache_hits += 1
                return response
            else:
                del self._cache[key]
        self.metrics.cache_misses += 1
        return None

    def _check_budget(self, estimated_cost: float) -> bool:
        """Verifica que no se exceda el presupuesto diario."""
        return (self.metrics.total_cost_usd + estimated_cost
                <= self.config.budget_limit_daily_usd)

    async def request(
        self,
        client_id: str,
        model: str,
        prompt: str,
        params: dict | None = None,
        cacheable: bool = True,
    ) -> dict:
        """Procesa una solicitud a traves del gateway.

        Args:
            client_id: identificador del cliente/aplicacion
            model: nombre del modelo a usar
            prompt: el prompt a enviar
            params: parametros adicionales (temperature, max_tokens, etc.)
            cacheable: si la respuesta puede cachearse

        Returns:
            Respuesta del modelo con metadatos del gateway
        """
        params = params or {}
        self.metrics.total_requests += 1
        start_time = time.time()

        # 1. Rate limiting
        if not self._check_rate_limit(client_id):
            self.metrics.errors += 1
            return {
                "error": "rate_limit_exceeded",
                "retry_after_seconds": 60,
            }

        # 2. Verificar presupuesto
        estimated_cost = params.get("max_tokens", 1000) * 0.00003  # estimacion
        if not self._check_budget(estimated_cost):
            self.metrics.errors += 1
            return {
                "error": "budget_exceeded",
                "daily_spent": self.metrics.total_cost_usd,
                "daily_limit": self.config.budget_limit_daily_usd,
            }

        # 3. Cache lookup
        if cacheable:
            cache_key = self._cache_key(model, prompt, params)
            cached = self._check_cache(cache_key)
            if cached is not None:
                latency = (time.time() - start_time) * 1000
                self.metrics.latency_sum_ms += latency
                return {
                    "response": cached,
                    "cached": True,
                    "latency_ms": latency,
                }

        # 4. Llamada al modelo (aqui iria la llamada real al API)
        response = await self._call_model(model, prompt, params)

        # 5. Actualizar metricas
        tokens_used = response.get("usage", {}).get("total_tokens", 0)
        cost = tokens_used * 0.00003  # costo simplificado
        self.metrics.total_tokens_used += tokens_used
        self.metrics.total_cost_usd += cost

        # 6. Guardar en cache
        if cacheable:
            self._cache[cache_key] = (response, time.time())

        latency = (time.time() - start_time) * 1000
        self.metrics.latency_sum_ms += latency

        # 7. Log estructurado
        if self.config.enable_logging:
            self._log_request(client_id, model, tokens_used, cost, latency)

        return {
            "response": response,
            "cached": False,
            "latency_ms": latency,
            "tokens_used": tokens_used,
            "cost_usd": cost,
        }

    async def _call_model(self, model: str, prompt: str, params: dict) -> dict:
        """Llamada al modelo. En produccion, aqui va la logica de routing."""
        # Placeholder - en produccion usa el SDK del proveedor
        return {
            "content": f"[Respuesta de {model}]",
            "usage": {"total_tokens": 500},
        }

    def _log_request(
        self,
        client_id: str,
        model: str,
        tokens: int,
        cost: float,
        latency: float,
    ) -> None:
        """Log estructurado para auditoria y debugging."""
        # En produccion: enviar a OpenTelemetry, Datadog, etc.
        pass

    def get_dashboard(self) -> dict:
        """Retorna metricas para el dashboard de monitoreo."""
        return {
            "total_requests": self.metrics.total_requests,
            "cache_hit_rate": f"{self.metrics.cache_hit_rate:.1%}",
            "avg_latency_ms": f"{self.metrics.avg_latency_ms:.1f}",
            "total_cost_today": f"${self.metrics.total_cost_usd:.2f}",
            "total_tokens": self.metrics.total_tokens_used,
            "error_count": self.metrics.errors,
        }
```

### Comparacion con patrones clasicos

El AI Gateway es una combinacion de tres patrones GoF:

- **Facade**: oculta la complejidad de multiples proveedores de IA detras de una interfaz unificada.
- **Proxy**: interpone logica de control (rate limiting, caching, logging) entre el cliente y el servicio real.
- **Strategy** (parcial): puede enrutar a diferentes modelos segun el contexto.

La diferencia clave con un API Gateway tradicional: el AI Gateway necesita entender el concepto de **tokens**, **costo por token** y **cacheo semantico** (dos prompts diferentes pueden tener la misma intencion y la misma respuesta valida).

---

## 13.3 Patron 2: Router de modelos (Model Router)

### Descripcion y mecanica

Un clasificador evalua cada consulta entrante y la envia al modelo mas apropiado. Consultas simples van a modelos pequenos y baratos; consultas complejas van a modelos grandes y costosos.

Reportes de la industria muestran reducciones de costo del 60-85% sin perdida significativa de calidad. El paper RouteLLM de LMSYS demostro que routers entrenados con datos de preferencia humana pueden mantener el 95% de la calidad de GPT-4 con 85% de reduccion de costos [Ong et al., 2024/2025].

```python
"""
Implementacion de un Model Router para agentes.
"""

from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod


class ModelTier(Enum):
    SMALL = "small"    # Phi-4 mini, Llama 3.2 3B, Gemma 3 4B
    MEDIUM = "medium"  # Llama 3.1 8B, GPT-4o-mini, Claude Haiku
    LARGE = "large"    # GPT-4o, Claude Sonnet, Llama 3.1 70B
    FRONTIER = "frontier"  # o1, Claude Opus, DeepSeek-R1


@dataclass
class ModelOption:
    """Configuracion de un modelo disponible."""
    name: str
    tier: ModelTier
    cost_per_1k_input_tokens: float
    cost_per_1k_output_tokens: float
    avg_latency_ms: int
    max_context_tokens: int


@dataclass
class RoutingDecision:
    """Resultado de la decision de routing."""
    model: ModelOption
    reason: str
    estimated_cost: float
    complexity_score: float


class RoutingStrategy(ABC):
    """Estrategia de routing. Patron Strategy del GoF."""

    @abstractmethod
    def route(self, query: str, context: dict) -> ModelTier:
        ...


class KeywordRouter(RoutingStrategy):
    """Router basado en heuristicas de keywords.

    Rapido y determinista. Buen punto de partida.
    No requiere llamadas adicionales al LLM.
    """

    COMPLEXITY_SIGNALS = {
        # Senales de alta complejidad
        "high": [
            "analiza", "compara", "evalua", "sintetiza",
            "explica por que", "razonamiento", "multi-paso",
            "pros y contras", "arquitectura", "disena",
        ],
        # Senales de baja complejidad
        "low": [
            "que es", "define", "lista", "cual es",
            "cuando", "donde", "cuanto", "si o no",
        ],
    }

    def route(self, query: str, context: dict) -> ModelTier:
        query_lower = query.lower()
        query_length = len(query.split())

        # Heuristica 1: longitud del query
        if query_length > 200:
            return ModelTier.LARGE

        # Heuristica 2: keywords de complejidad
        high_signals = sum(
            1 for kw in self.COMPLEXITY_SIGNALS["high"]
            if kw in query_lower
        )
        low_signals = sum(
            1 for kw in self.COMPLEXITY_SIGNALS["low"]
            if kw in query_lower
        )

        if high_signals >= 2:
            return ModelTier.LARGE
        if high_signals == 1 and low_signals == 0:
            return ModelTier.MEDIUM
        return ModelTier.SMALL


class CascadingRouter(RoutingStrategy):
    """Router que empieza con el modelo mas barato y escala si no es suficiente.

    Combina Strategy con Chain of Responsibility:
    intenta con el mas barato primero, escala si la confianza es baja.
    """

    CONFIDENCE_THRESHOLD = 0.7

    def route(self, query: str, context: dict) -> ModelTier:
        # Empieza siempre con SMALL
        # La logica de escalacion esta en el executor, no aqui
        return ModelTier.SMALL


class ModelRouter:
    """Router central que selecciona el modelo optimo para cada consulta.

    Implementa el patron Strategy: la estrategia de routing es
    intercambiable sin cambiar el resto del sistema.
    """

    def __init__(
        self,
        models: list[ModelOption],
        strategy: RoutingStrategy,
    ):
        self.models = {m.tier: m for m in models}
        self.strategy = strategy

    def select_model(self, query: str, context: dict | None = None) -> RoutingDecision:
        """Selecciona el modelo optimo para la consulta."""
        context = context or {}
        tier = self.strategy.route(query, context)
        model = self.models[tier]

        # Estimar tokens y costo
        estimated_input_tokens = len(query.split()) * 1.3  # aprox
        estimated_output_tokens = 500  # estimacion conservadora
        estimated_cost = (
            estimated_input_tokens / 1000 * model.cost_per_1k_input_tokens
            + estimated_output_tokens / 1000 * model.cost_per_1k_output_tokens
        )

        return RoutingDecision(
            model=model,
            reason=f"Routed to {model.name} ({tier.value})",
            estimated_cost=estimated_cost,
            complexity_score=0.0,  # calculado por la estrategia
        )


# Ejemplo de uso
AVAILABLE_MODELS = [
    ModelOption("phi4-mini", ModelTier.SMALL, 0.0001, 0.0002, 50, 16384),
    ModelOption("gpt-4o-mini", ModelTier.MEDIUM, 0.00015, 0.0006, 300, 128000),
    ModelOption("claude-sonnet", ModelTier.LARGE, 0.003, 0.015, 800, 200000),
    ModelOption("deepseek-r1", ModelTier.FRONTIER, 0.004, 0.016, 3000, 128000),
]

router = ModelRouter(
    models=AVAILABLE_MODELS,
    strategy=KeywordRouter(),
)

# Consultas de diferente complejidad
queries = [
    "Que es Python?",
    "Analiza las diferencias arquitectonicas entre REST y GraphQL",
    "Lista los paises de America del Sur",
    "Disena una arquitectura multi-agente para un sistema de trading",
]

print("=== Decisiones de routing ===\n")
for q in queries:
    decision = router.select_model(q)
    print(f"  Query: '{q[:60]}...'")
    print(f"  -> {decision.model.name} (${decision.estimated_cost:.4f})")
    print()
```

### Comparacion con patrones clasicos

El Router es el patron **Strategy** del GoF aplicado a modelos de IA. La familia de algoritmos (modelos) es intercambiable, y un clasificador selecciona la estrategia automaticamente basandose en el contenido de la consulta.

Tambien tiene elementos de **Chain of Responsibility**: en el `CascadingRouter`, la consulta pasa por una cadena de modelos de menor a mayor capacidad hasta que uno produce una respuesta satisfactoria.

---

## 13.4 Patron 3: Cascada con fallbacks deterministicos (Fallback Chain)

### Descripcion y mecanica

Cuando un LLM falla o produce una respuesta de baja confianza, el sistema cae a un nivel inferior de sofisticacion, hasta llegar a una respuesta determinista garantizada. Es la red de seguridad que asegura que tu sistema **siempre** responde.

```python
"""
Patron Cascada con Fallbacks Deterministicos.
Tres niveles: LLM principal -> LLM backup -> respuesta determinista.
"""

import asyncio
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Any


@dataclass
class FallbackResult:
    """Resultado con informacion sobre que nivel de la cascada respondio."""
    content: Any
    level: int  # 0 = primario, 1 = secundario, 2+ = fallback deterministico
    provider: str
    confidence: float
    fallback_reason: str | None = None


class FallbackLevel(ABC):
    """Un nivel en la cadena de fallbacks."""

    @abstractmethod
    async def attempt(self, input_data: dict) -> FallbackResult | None:
        """Intenta producir una respuesta. Retorna None si falla."""
        ...


class LLMLevel(FallbackLevel):
    """Nivel basado en LLM con timeout y validacion de confianza."""

    def __init__(
        self,
        provider: str,
        timeout_seconds: float,
        min_confidence: float,
        level: int,
    ):
        self.provider = provider
        self.timeout_seconds = timeout_seconds
        self.min_confidence = min_confidence
        self.level = level

    async def attempt(self, input_data: dict) -> FallbackResult | None:
        try:
            result = await asyncio.wait_for(
                self._call_llm(input_data),
                timeout=self.timeout_seconds,
            )
            if result and result.confidence >= self.min_confidence:
                return result
            return None  # Confianza insuficiente -> siguiente nivel
        except asyncio.TimeoutError:
            return None  # Timeout -> siguiente nivel
        except Exception:
            return None  # Error -> siguiente nivel

    async def _call_llm(self, input_data: dict) -> FallbackResult:
        """Llamada al LLM. Placeholder para implementacion real."""
        return FallbackResult(
            content=f"Respuesta de {self.provider}",
            level=self.level,
            provider=self.provider,
            confidence=0.85,
        )


class DeterministicLevel(FallbackLevel):
    """Nivel deterministico: siempre responde, sin LLM."""

    def __init__(self, rules: dict[str, str], default_response: str):
        self.rules = rules
        self.default_response = default_response

    async def attempt(self, input_data: dict) -> FallbackResult:
        query = input_data.get("query", "").lower()

        # Buscar en reglas
        for keyword, response in self.rules.items():
            if keyword in query:
                return FallbackResult(
                    content=response,
                    level=99,  # nivel deterministico
                    provider="rules_engine",
                    confidence=1.0,  # deterministico = 100% confiable en formato
                )

        # Default: siempre tiene una respuesta
        return FallbackResult(
            content=self.default_response,
            level=99,
            provider="default_response",
            confidence=1.0,
        )


class FallbackChain:
    """Cadena de fallbacks que garantiza una respuesta.

    Implementa Chain of Responsibility del GoF:
    cada nivel intenta manejar la solicitud.
    Si falla, la pasa al siguiente nivel.
    El nivel deterministico final SIEMPRE responde.
    """

    def __init__(self, levels: list[FallbackLevel]):
        self.levels = levels
        self._metrics = {"attempts_by_level": {}, "total_requests": 0}

    async def execute(self, input_data: dict) -> FallbackResult:
        """Ejecuta la cadena. Garantiza retornar una respuesta."""
        self._metrics["total_requests"] += 1

        for i, level in enumerate(self.levels):
            result = await level.attempt(input_data)
            if result is not None:
                level_name = type(level).__name__
                self._metrics["attempts_by_level"][level_name] = (
                    self._metrics["attempts_by_level"].get(level_name, 0) + 1
                )
                if i > 0:
                    result.fallback_reason = (
                        f"Niveles 0-{i-1} fallaron o tuvieron confianza insuficiente"
                    )
                return result

        # Esto no deberia pasar si el ultimo nivel es deterministico
        raise RuntimeError("Todos los niveles de la cadena fallaron")


# Ejemplo: cadena para un chatbot de soporte
chain = FallbackChain([
    # Nivel 0: LLM principal (rapido, agresivo en timeout)
    LLMLevel("claude-sonnet", timeout_seconds=5.0, min_confidence=0.7, level=0),
    # Nivel 1: LLM backup (mas tiempo, menos exigente)
    LLMLevel("gpt-4o-mini", timeout_seconds=10.0, min_confidence=0.5, level=1),
    # Nivel 2: Siempre responde
    DeterministicLevel(
        rules={
            "precio": "Puedes consultar nuestros precios en example.com/precios",
            "horario": "Nuestro horario es de lunes a viernes, 9:00 a 18:00",
            "contacto": "Puedes contactarnos en soporte@example.com",
        },
        default_response=(
            "No pude procesar tu consulta automaticamente. "
            "Un agente humano te atendera en breve. "
            "Referencia: #{ticket_id}"
        ),
    ),
])
```

### Cuando usar y cuando no

**Usar cuando:**
- La disponibilidad es mas importante que la calidad perfecta.
- El sistema esta en produccion y un "no respondo" es inaceptable.
- Tienes reglas de negocio conocidas que cubren los casos mas comunes.

**NO usar cuando:**
- La calidad de la respuesta es critica (diagnosticos medicos, asesoria legal).
- El fallback deterministico daria informacion incorrecta o danina.
- El costo de una respuesta incorrecta es mayor que el costo de no responder.

El **antipatron** a evitar: usar el fallback como excusa para no mejorar el sistema principal. Si el 30% de las consultas caen al nivel deterministico, tienes un problema en tu nivel primario, no una prueba de que el fallback funciona.

---

## 13.5 Patron 4: Evaluador-Optimizador (Evaluator-Optimizer)

### Descripcion y mecanica

Un LLM genera una respuesta; otro (o el mismo) la evalua y proporciona retroalimentacion; el generador itera hasta alcanzar un umbral de calidad. Es el equivalente automatizado de la revision de codigo.

Madaan et al. [2023] formalizaron este patron en "Self-Refine", demostrando ~20% de mejora absoluta en 7 tareas distintas.

```python
"""
Patron Evaluador-Optimizador.
Un generador produce, un evaluador critica, el generador mejora.
"""

from dataclasses import dataclass


@dataclass
class Evaluation:
    """Resultado de la evaluacion."""
    score: float  # 0.0 a 1.0
    feedback: str
    passes_threshold: bool
    issues: list[str]


@dataclass
class GenerationResult:
    """Resultado del ciclo completo de generacion-evaluacion."""
    content: str
    final_score: float
    iterations: int
    evaluation_history: list[Evaluation]


class EvaluatorOptimizer:
    """Ciclo de generacion-evaluacion-refinamiento.

    Conecta con el patron Observer del GoF: el evaluador observa
    la salida del generador y reacciona.

    Tambien conecta con la heuristica de Polya:
    "Puedes verificar el resultado? Puedes obtenerlo de otra forma?"
    """

    def __init__(
        self,
        generator,  # modelo que genera
        evaluator,  # modelo que evalua (puede ser el mismo u otro)
        quality_threshold: float = 0.8,
        max_iterations: int = 3,
    ):
        self.generator = generator
        self.evaluator = evaluator
        self.quality_threshold = quality_threshold
        self.max_iterations = max_iterations

    async def generate(self, task: str) -> GenerationResult:
        """Ejecuta el ciclo de generacion-evaluacion."""
        history = []
        current_content = ""

        for iteration in range(self.max_iterations):
            # Paso 1: Generar (o refinar)
            if iteration == 0:
                prompt = f"Realiza la siguiente tarea:\n{task}"
            else:
                prompt = (
                    f"Tarea original: {task}\n\n"
                    f"Tu respuesta anterior:\n{current_content}\n\n"
                    f"Feedback del evaluador:\n{history[-1].feedback}\n\n"
                    f"Problemas detectados: {history[-1].issues}\n\n"
                    f"Mejora tu respuesta basandote en el feedback."
                )

            current_content = await self.generator.generate(prompt)

            # Paso 2: Evaluar
            eval_prompt = (
                f"Evalua la siguiente respuesta para la tarea: {task}\n\n"
                f"Respuesta:\n{current_content}\n\n"
                f"Evalua de 0.0 a 1.0. Identifica problemas especificos."
            )
            evaluation = await self.evaluator.evaluate(eval_prompt)
            history.append(evaluation)

            # Paso 3: Decidir si terminar
            if evaluation.passes_threshold:
                break

        return GenerationResult(
            content=current_content,
            final_score=history[-1].score if history else 0.0,
            iterations=len(history),
            evaluation_history=history,
        )
```

### Riesgos del patron

1. **Bucles infinitos.** Sin un limite de iteraciones estricto, el generador y el evaluador pueden entrar en un ciclo donde cada iteracion cambia algo pero nunca satisface al evaluador. Siempre pon un `max_iterations`.

2. **Costo multiplicado.** Cada iteracion cuesta tokens. Con 3 iteraciones, pagas ~6x (3 generaciones + 3 evaluaciones). Asegurate de que la mejora en calidad justifica el costo.

3. **Acuerdo en lo incorrecto.** Dos LLMs del mismo proveedor pueden compartir los mismos sesgos y confirmar errores mutuamente. La diversidad de modelos (evaluador de un proveedor diferente al generador) reduce este riesgo.

---

## 13.6 Patron 5: Human-in-the-Loop (Humano en el ciclo)

### Descripcion y mecanica

El agente autonomo opera hasta llegar a un punto de decision critico, donde pausa y solicita aprobacion humana. Es el patron que separa a los agentes de demo de los agentes de produccion.

```python
"""
Patron Human-in-the-Loop para agentes de produccion.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import uuid
import time


class ApprovalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    TIMEOUT = "timeout"


class RiskLevel(Enum):
    LOW = "low"        # ejecucion automatica
    MEDIUM = "medium"  # notificacion post-ejecucion
    HIGH = "high"      # aprobacion pre-ejecucion
    CRITICAL = "critical"  # aprobacion + segunda revision


@dataclass
class ApprovalRequest:
    """Solicitud de aprobacion humana."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    action: str = ""
    context: dict = field(default_factory=dict)
    risk_level: RiskLevel = RiskLevel.HIGH
    status: ApprovalStatus = ApprovalStatus.PENDING
    created_at: float = field(default_factory=time.time)
    timeout_seconds: float = 300.0  # 5 minutos por defecto
    reviewer: str | None = None
    decision_reason: str = ""


class HumanApprovalGate:
    """Gate de aprobacion humana.

    Principio: las acciones irreversibles o de alto impacto
    SIEMPRE requieren aprobacion humana.

    Las acciones de bajo riesgo se ejecutan automaticamente
    pero se registran para auditoria.
    """

    def __init__(self):
        self._pending: dict[str, ApprovalRequest] = {}

    def assess_risk(self, action: str, params: dict) -> RiskLevel:
        """Evalua el nivel de riesgo de una accion.

        En produccion, esto seria una combinacion de:
        - Reglas deterministicas (DELETE siempre es HIGH)
        - Clasificador ML
        - Politicas de la organizacion
        """
        action_lower = action.lower()

        # Acciones criticas: siempre necesitan aprobacion
        critical_actions = ["delete", "drop", "transfer", "payment", "deploy"]
        if any(a in action_lower for a in critical_actions):
            return RiskLevel.CRITICAL

        # Acciones de alto riesgo
        high_risk = ["update", "modify", "send_email", "create_user"]
        if any(a in action_lower for a in high_risk):
            return RiskLevel.HIGH

        # Acciones de riesgo medio
        medium_risk = ["write", "create", "schedule"]
        if any(a in action_lower for a in medium_risk):
            return RiskLevel.MEDIUM

        return RiskLevel.LOW

    async def gate(self, action: str, params: dict) -> dict:
        """Evalua si la accion requiere aprobacion y actua en consecuencia.

        Returns:
            {"approved": bool, "reason": str, "risk_level": str}
        """
        risk = self.assess_risk(action, params)

        if risk == RiskLevel.LOW:
            return {
                "approved": True,
                "reason": "Riesgo bajo: ejecucion automatica",
                "risk_level": risk.value,
                "requires_human": False,
            }

        if risk == RiskLevel.MEDIUM:
            return {
                "approved": True,
                "reason": "Riesgo medio: ejecucion con notificacion post-hoc",
                "risk_level": risk.value,
                "requires_human": False,
                "notify_after": True,
            }

        # HIGH y CRITICAL: requieren aprobacion previa
        request = ApprovalRequest(
            action=action,
            context=params,
            risk_level=risk,
        )
        self._pending[request.id] = request

        return {
            "approved": False,
            "reason": f"Riesgo {risk.value}: requiere aprobacion humana",
            "risk_level": risk.value,
            "requires_human": True,
            "approval_id": request.id,
            "timeout_seconds": request.timeout_seconds,
        }

    def approve(self, approval_id: str, reviewer: str, reason: str = "") -> bool:
        """El humano aprueba una accion pendiente."""
        if approval_id in self._pending:
            req = self._pending[approval_id]
            req.status = ApprovalStatus.APPROVED
            req.reviewer = reviewer
            req.decision_reason = reason
            return True
        return False

    def reject(self, approval_id: str, reviewer: str, reason: str) -> bool:
        """El humano rechaza una accion pendiente."""
        if approval_id in self._pending:
            req = self._pending[approval_id]
            req.status = ApprovalStatus.REJECTED
            req.reviewer = reviewer
            req.decision_reason = reason
            return True
        return False
```

Este patron es lo que en el Capitulo 8 llamamos "el arnes" en su version mas visible para el usuario. La clave esta en la funcion `assess_risk`: define un continuo entre autonomia total y supervision total, no un binario "automatico o manual".

---

## 13.7 Los patrones de Lakshmanan aplicados a agentes

Valliappa Lakshmanan, en su trabajo sobre patrones de IA generativa [Lakshmanan y Hapke, 2025], identifica 32 patrones para construir aplicaciones con IA generativa. Cinco de ellos son especialmente relevantes para agentes en produccion:

### Trustworthy Generation (Generacion confiable)

A medida que los agentes pasan de responder preguntas a tomar acciones, la confiabilidad se vuelve critica. Este patron establece que toda generacion debe ir acompanada de mecanismos de verificacion proporcionales al impacto de la accion.

En la practica, esto se traduce en: nunca ejecutes directamente la salida de un LLM. Siempre pasa por validacion -- y el nivel de validacion debe escalar con el riesgo.

### Grammar (Salidas estructuradas)

Las salidas de texto libre son la fuente de la mayoria de los bugs en sistemas con agentes. Este patron exige que toda comunicacion entre componentes use formatos estructurados (JSON Schema, Pydantic models) con validacion estricta.

Como advierte Lakshmanan: "debes ser cuidadoso con como tu proveedor de LLM implementa structured outputs" -- no todos los proveedores garantizan que la salida cumpla el schema 100% de las veces.

### Reflection (Reflexion)

La reflexion define la autonomia real de un agente: la capacidad de evaluar y criticar su propia salida. Un agente que solo genera no es autonomo; un agente que genera, evalua y mejora si es.

La observacion clave es que frecuentemente es mas facil verificar calidad que pre-especificar perfeccion. Un agente que genera codigo, lo ejecuta, verifica que pase los tests y lo mejora si no pasa es mas confiable que uno que intenta generar codigo perfecto en el primer intento.

### Long-term Memory (Memoria a largo plazo)

Los agentes persistentes necesitan diferentes tipos de almacenamiento para diferentes tipos de informacion. No existe un unico mecanismo de memoria que sirva para todo. Embeddings vectoriales para busqueda semantica, bases de datos relacionales para datos estructurados, grafos para relaciones entre entidades.

### Code Execution (Ejecucion de codigo)

Para tareas que requieren precision -- calculos, transformaciones de datos, consultas a bases de datos -- el patron optimo no es que el LLM genere la respuesta directamente, sino que genere **codigo** que se ejecuta en un sandbox. El resultado del codigo es confiable; la generacion del codigo es la parte que puede fallar.

---

## 13.8 Antipatrones comunes en sistemas con IA

### Antipatron 1: El LLM como martillo

No todo requiere un LLM. Usar un LLM para validar formatos de email, para parsear JSON bien formado, para hacer calculos aritmeticos o para filtrar listas por un criterio simple es sobreingenieria costosa.

**La regla**: si puedes escribirlo en menos de 50 lineas de codigo con tests, no necesitas un LLM.

```python
"""
Ejemplos de sobreingenieria con LLMs.
"""

# ANTI-PATRON: usar LLM para validar email
async def validate_email_bad(email: str) -> bool:
    """NO HAGAS ESTO."""
    response = await llm.generate(f"Es '{email}' un email valido? Responde si o no.")
    return "si" in response.lower()


# CORRECTO: regex
import re

EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

def validate_email_good(email: str) -> bool:
    """Determinista, instantaneo, gratis, 100% correcto."""
    return bool(EMAIL_PATTERN.match(email))


# ANTI-PATRON: usar LLM para calcular
async def calculate_total_bad(prices: list[float]) -> float:
    """NO HAGAS ESTO."""
    response = await llm.generate(f"Suma estos numeros: {prices}")
    return float(response)


# CORRECTO: Python
def calculate_total_good(prices: list[float]) -> float:
    """Determinista, instantaneo, gratis, 100% correcto."""
    return sum(prices)
```

### Antipatron 2: Wrapper superficial de LLM

Un "wrapper" que simplemente agrega una llamada HTTP al API del LLM sin anadirle validacion, reintentos, fallbacks ni metricas viola el principio de modulos profundos de Ousterhout [2018]. La interfaz y la implementacion tienen la misma complejidad: no hay valor agregado.

### Antipatron 3: Prompts monoliticos

Un system prompt de 5,000 tokens que intenta cubrir todos los casos posibles. En lugar de un modulo profundo con una interfaz simple, tienes un modulo superficial con una interfaz enorme. La solucion: descomponer en componentes especializados, cada uno con su propio prompt enfocado.

### Antipatron 4: Orquestacion prematura

"Usamos 7 agentes con debate adversarial" suena impresionante. Pero si un solo agente con un mejor prompt resuelve el mismo problema, los 7 agentes son deuda tecnica disfrazada de arquitectura. Como discutimos en el Capitulo 11: empieza con un solo agente, mide sus limitaciones, y escala solo cuando tengas evidencia concreta.

### Antipatron 5: Ausencia de evaluaciones

Desplegar un agente sin un pipeline de evaluaciones (evals) es como desplegar software sin tests. El no determinismo de los LLMs hace que esto sea **mas** peligroso que el software tradicional, no menos. Si no puedes medir la calidad, no puedes mejorarla [Subramaniam y Fowler, 2025].

---

## 13.9 DeepSeek y el momento Linux de la IA: modelos abiertos como patron arquitectonico

### El evento

En enero de 2025, DeepSeek publico R1: un modelo de 671 mil millones de parametros con arquitectura MoE, entrenado por menos de 6 millones de dolares, con licencia MIT. El mercado bursatil perdio un billon de dolares en un dia. Nvidia perdio $589 mil millones en capitalizacion -- la mayor perdida de un solo dia para cualquier empresa en la historia [CNBC, 2025].

Mas alla del drama financiero, DeepSeek demostro algo tecnico concreto: **los modelos open-weight pueden competir con los mejores modelos propietarios para una amplia gama de tareas de produccion** a un costo ~6.6x menor por token [Gao et al., 2025].

### La analogia con Linux: valida pero imperfecta

La comunidad bautizo esto como "el momento Linux de la IA". La comparacion tiene merito:

- Linux demostro que el software abierto podia competir con las alternativas propietarias.
- DeepSeek demostro que los modelos abiertos pueden competir con los modelos propietarios.
- En ambos casos, la reaccion inicial fue escepticismo seguida de adopcion gradual.

Pero la analogia es imperfecta en un aspecto fundamental. Linux democratizo software a traves de contribuciones colaborativas de codigo. Cualquiera con una computadora puede contribuir a Linux. La IA open-source tiene barreras mucho mas altas: entrenar un modelo requiere datos masivos y computo costoso. DeepSeek libera los pesos del modelo, pero no los datos de entrenamiento ni el pipeline completo [WEF, 2025; Allen, 2025].

Como senala Daron Acemoglu (MIT, Premio Nobel): las tecnicas usadas por DeepSeek -- MoE, RL, destilacion -- fueron todas pioneras en Estados Unidos. DeepSeek demostro excelencia en ingenieria al combinar metodos existentes de forma elegante, no un avance algoritmico fundamental [Acemoglu, 2025].

### Implicaciones para la arquitectura de agentes

Para quienes construimos agentes, el legado de DeepSeek es pragmatico:

**Modelos abiertos como opcion real.** Antes de DeepSeek, usar modelos open-weight era una concesion de calidad a cambio de privacidad o costo. Despues de DeepSeek, es una opcion arquitectonica valida para produccion.

**Despliegue local viable.** Con modelos abiertos competitivos y las tecnicas de cuantizacion del Capitulo 12, es viable correr agentes completamente on-premise. Esto resuelve preocupaciones de privacidad, latencia y dependencia de proveedores.

**Fine-tuning accesible.** Con pesos abiertos, el fine-tuning para dominios especificos se vuelve accesible para equipos pequenos. Un modelo de 7B parametros puede fine-tunearse en una sola GPU con QLoRA (bitsandbytes) en horas.

```python
"""
Patron de abstraccion de proveedor de modelo.
Permite alternar entre modelos propietarios y abiertos.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class ModelProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL_OLLAMA = "ollama"
    LOCAL_VLLM = "vllm"


@dataclass
class ModelConfig:
    """Configuracion agnistica de proveedor."""
    provider: ModelProvider
    model_name: str
    endpoint: str
    api_key: str | None = None
    max_tokens: int = 4096
    temperature: float = 0.0


class ModelClient(ABC):
    """Interfaz unificada para cualquier proveedor de modelo.

    Este patron permite que tu agente funcione con:
    - APIs propietarias (OpenAI, Anthropic)
    - Modelos abiertos locales (Ollama, vLLM)
    - Modelos fine-tuneados propios

    Sin cambiar una sola linea de la logica del agente.
    """

    @abstractmethod
    async def generate(self, messages: list[dict], **kwargs) -> str:
        ...

    @abstractmethod
    async def generate_structured(self, messages: list[dict], schema: type, **kwargs):
        ...


class OllamaClient(ModelClient):
    """Cliente para modelos locales via Ollama.

    Ideal para:
    - Agentes on-premise con requisitos de privacidad
    - Triage rapido con modelos pequenos (Phi-4 mini, Llama 3.2 3B)
    - Fine-tuning local con modelos abiertos
    """

    def __init__(self, config: ModelConfig):
        self.config = config
        self.base_url = config.endpoint or "http://localhost:11434"

    async def generate(self, messages: list[dict], **kwargs) -> str:
        # httpx.AsyncClient POST a /api/chat
        return "[respuesta local]"

    async def generate_structured(self, messages: list[dict], schema: type, **kwargs):
        # Ollama soporta structured outputs via JSON mode
        return schema()


class AnthropicClient(ModelClient):
    """Cliente para Claude via API de Anthropic."""

    def __init__(self, config: ModelConfig):
        self.config = config

    async def generate(self, messages: list[dict], **kwargs) -> str:
        # anthropic.AsyncAnthropic().messages.create(...)
        return "[respuesta cloud]"

    async def generate_structured(self, messages: list[dict], schema: type, **kwargs):
        # Usar tool_use para structured outputs
        return schema()


def create_client(config: ModelConfig) -> ModelClient:
    """Factory que crea el cliente apropiado segun el proveedor.

    Patron Factory Method del GoF.
    """
    clients = {
        ModelProvider.LOCAL_OLLAMA: OllamaClient,
        ModelProvider.ANTHROPIC: AnthropicClient,
        # ... otros proveedores
    }
    client_class = clients.get(config.provider)
    if not client_class:
        raise ValueError(f"Proveedor no soportado: {config.provider}")
    return client_class(config)
```

---

## 13.10 Una taxonomia para elegir el patron correcto

No existe un patron universalmente mejor. La eleccion depende de las caracteristicas de tu problema:

```python
"""
Framework de decision para seleccion de patrones de diseno.
"""

from dataclasses import dataclass


@dataclass
class SystemCharacteristics:
    """Caracteristicas del sistema que determinan el patron apropiado."""
    determinism_required: str  # "high", "medium", "low"
    latency_tolerance_ms: int
    budget_per_query_usd: float
    error_impact: str  # "low", "medium", "high", "critical"
    volume_per_day: int
    needs_human_oversight: bool


def recommend_patterns(chars: SystemCharacteristics) -> list[dict]:
    """Recomienda patrones basados en las caracteristicas del sistema."""
    patterns = []

    # Siempre recomendar: AI Gateway
    patterns.append({
        "pattern": "AI Gateway",
        "reason": "Centralizar control, costos y observabilidad",
        "priority": "SIEMPRE",
    })

    # Alto volumen + presupuesto limitado -> Router
    if chars.volume_per_day > 1000 and chars.budget_per_query_usd < 0.01:
        patterns.append({
            "pattern": "Model Router",
            "reason": "Alto volumen con presupuesto limitado requiere routing inteligente",
            "priority": "ALTA",
        })

    # Alta disponibilidad requerida -> Fallback Chain
    if chars.error_impact in ("high", "critical"):
        patterns.append({
            "pattern": "Fallback Chain",
            "reason": "El impacto de no responder es alto",
            "priority": "ALTA",
        })

    # Calidad critica -> Evaluator-Optimizer
    if chars.error_impact == "critical" and chars.latency_tolerance_ms > 5000:
        patterns.append({
            "pattern": "Evaluator-Optimizer",
            "reason": "Calidad critica + tolerancia a latencia permite iteraciones",
            "priority": "MEDIA",
        })

    # Acciones de alto riesgo -> Human-in-the-Loop
    if chars.needs_human_oversight or chars.error_impact == "critical":
        patterns.append({
            "pattern": "Human-in-the-Loop",
            "reason": "Acciones de alto impacto requieren supervision humana",
            "priority": "CRITICA",
        })

    # Determinismo alto + bajo presupuesto -> considerar NO usar IA
    if chars.determinism_required == "high" and chars.budget_per_query_usd < 0.001:
        patterns.append({
            "pattern": "NO uses IA",
            "reason": (
                "Si necesitas determinismo alto con presupuesto minimo, "
                "codigo tradicional es la mejor opcion"
            ),
            "priority": "CONSIDERAR",
        })

    return patterns


# Ejemplo: sistema de clasificacion de tickets
ticket_system = SystemCharacteristics(
    determinism_required="medium",
    latency_tolerance_ms=3000,
    budget_per_query_usd=0.005,
    error_impact="medium",
    volume_per_day=5000,
    needs_human_oversight=False,
)

print("=== Patrones recomendados para clasificacion de tickets ===\n")
for rec in recommend_patterns(ticket_system):
    print(f"  [{rec['priority']}] {rec['pattern']}")
    print(f"    {rec['reason']}\n")

# Ejemplo: sistema de aprobacion de creditos
credit_system = SystemCharacteristics(
    determinism_required="high",
    latency_tolerance_ms=10000,
    budget_per_query_usd=0.05,
    error_impact="critical",
    volume_per_day=500,
    needs_human_oversight=True,
)

print("=== Patrones recomendados para aprobacion de creditos ===\n")
for rec in recommend_patterns(credit_system):
    print(f"  [{rec['priority']}] {rec['pattern']}")
    print(f"    {rec['reason']}\n")
```

### Composicion de patrones

Los patrones no son mutuamente exclusivos. La configuracion mas comun en produccion combina varios:

1. **AI Gateway** como punto de entrada (siempre).
2. **Model Router** para dirigir consultas simples a modelos baratos.
3. **Fallback Chain** en cada nivel del router para garantizar disponibilidad.
4. **Evaluator-Optimizer** para las consultas criticas que pasan al modelo grande.
5. **Human-in-the-Loop** como ultima linea de defensa para acciones irreversibles.

Esta composicion es natural: cada patron resuelve un problema diferente, y juntos cubren el espectro completo de incertidumbre, costo y riesgo.

---

## Takeaway del capitulo

Los patrones de diseno para sistemas con IA son extensiones naturales de los patrones clasicos, adaptados a las particularidades del software no determinista:

- **Separa la inteligencia de la logica.** El LLM es un componente, no el sistema. Aislalo detras de interfaces claras (Parnas, Ousterhout).

- **AI Gateway** centraliza control y observabilidad. Es el equivalente del API Gateway para sistemas con IA. Usalo siempre.

- **Model Router** reduce costos 60-85% dirigiendo consultas al modelo apropiado. Es el patron Strategy del GoF aplicado a modelos.

- **Fallback Chain** garantiza disponibilidad cayendo a niveles menos sofisticados pero mas confiables. Es Chain of Responsibility del GoF.

- **Evaluator-Optimizer** mejora calidad mediante ciclos de generacion-evaluacion. Es costoso; reservalo para tareas de alto impacto.

- **Human-in-the-Loop** es el patron que separa demos de produccion. Las acciones irreversibles siempre requieren aprobacion humana.

- Los **antipatrones** mas comunes son: usar LLM como martillo, wrappers superficiales, prompts monoliticos, orquestacion prematura y ausencia de evaluaciones.

- **DeepSeek y los modelos abiertos** habilitan una nueva opcion arquitectonica: agentes on-premise con modelos open-weight competitivos, eliminando dependencia de proveedores.

El principio rector sigue siendo el mismo que los autores clasicos nos ensenan: **reducir la complejidad, crear abstracciones profundas y separar responsabilidades**. La IA no cambia los fundamentos del buen diseno de software; los extiende.

---

## Referencias

- Gamma, E., Helm, R., Johnson, R. y Vlissides, J. *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley, 1994.
- Ousterhout, J. *A Philosophy of Software Design*. 2da edicion, 2021.
- Parnas, D. L. "On the Criteria To Be Used in Decomposing Systems into Modules." *Communications of the ACM*, 15(12), 1972.
- Anthropic. "Building Effective Agents." anthropic.com/research, diciembre 2024.
- Google. "Developer's Guide to Multi-Agent Patterns in ADK." developers.googleblog.com, 2025.
- Lakshmanan, V. y Hapke, H. *Generative AI Design Patterns: Solutions to Common Challenges When Building GenAI Agents and Applications*. O'Reilly, 2025.
- Ong, I., et al. "RouteLLM: Learning to Route LLMs with Preference Data." *ICLR*, 2025.
- Madaan, A., et al. "Self-Refine: Iterative Refinement with Self-Feedback." *NeurIPS*, 2023.
- Subramaniam, B. y Fowler, M. "Emerging Patterns in Building GenAI Products." martinfowler.com, 2025.
- Heiland, L., Hauser, M. y Bogner, J. "Design Patterns for AI-based Systems: A Multivocal Literature Review." *CAIN*, 2023.
- DeepSeek-AI. "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning." *arXiv:2501.12948*, 2025.
- DeepSeek-AI. "DeepSeek-V3 Technical Report." *arXiv:2412.19437*, 2024.
- Gao, T., et al. "A Comparison of DeepSeek and Other LLMs." *arXiv:2502.03688*, 2025.
- Allen, G. C. "DeepSeek, Huawei, Export Controls, and the Future of the U.S.-China AI Race." CSIS, 2025.
- Acemoglu, D. "A Sputnik Moment for AI?" *Project Syndicate*, 2025.
- CNBC. "Nvidia drops nearly 17% as China's cheaper AI model DeepSeek sparks global tech sell-off." 2025.
- World Economic Forum. "What is open-source AI and how could DeepSeek change the industry?" 2025.
- HuggingFace. "One Year Since the 'DeepSeek Moment'." 2026.
- OWASP. "Top 10 for LLM Applications 2025." genai.owasp.org, 2024.
- Polya, G. *How to Solve It*. 1945.
