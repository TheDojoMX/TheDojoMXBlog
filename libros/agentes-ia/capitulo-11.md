# Capitulo 11: Orquestacion Multi-Agente y el Problema del Consenso

> "Un solo agente bien disenado suele ser mejor que tres mal coordinados."

---

En el Capitulo 10 exploramos como los agentes se comunican: patrones, protocolos y manejo de fallos. Ahora vamos a abordar lo que ocurre cuando multiples agentes necesitan trabajar juntos hacia un objetivo comun: la **orquestacion**.

En enero de 2025, un sistema multi-agente de trading desplegado por una fintech de Singapur perdio $2.3 millones en 47 minutos. El agente de analisis de mercado alucino una tendencia alcista inexistente. El agente de validacion -- entrenado con el mismo modelo base -- confirmo la tendencia. El agente ejecutor opero con total confianza. Tres agentes, cero disidencia, perdida total. El postmortem revelo algo que la teoria de sistemas distribuidos lleva decadas estudiando: el consenso entre nodos no confiables es un problema fundamentalmente dificil [Lamport, Shostak y Pease, 1982].

Este capitulo se enfoca en lo que emerge cuando multiples agentes interactuan: las topologias que determinan como se propagan decisiones y errores, los patrones de orquestacion que funcionan en produccion, los mecanismos de consenso que pueden (o no) protegerte cuando un agente alucina, y la observabilidad que necesitas para depurar estos sistemas.

---

## 11.1 Cuando un solo agente es suficiente (la mayoria de las veces)

### Resiste la tentacion

La tentacion de construir un sistema multi-agente es fuerte. "Usamos 7 agentes con debate adversarial" suena impresionante en una presentacion. Pero en la practica, la mayoria de los equipos que empiezan con multi-agente terminan simplificando a un solo agente con mejor prompting. Como recomienda Anthropic en su guia "Building Effective Agents": empieza simple [Anthropic, 2024].

Un solo agente bien disenado es preferible cuando:

- **El problema cabe en una sola ventana de contexto.** Si un agente puede ver toda la informacion relevante y producir una buena respuesta, agregar mas agentes solo anade latencia, costo y puntos de fallo.
- **No tienes observabilidad resuelta para un solo agente.** Si no puedes depurar un agente, no podras depurar cinco. La observabilidad multi-agente es ordenes de magnitud mas dificil.
- **El costo multiplicado no se justifica.** Cada agente adicional multiplica el consumo de tokens. Un sistema de 5 agentes con 3 rondas de debate puede costar 10-15x mas que una sola llamada.
- **La latencia es critica.** Cada "hop" entre agentes via API de LLM anade 0.5-3 segundos. Un sistema con 5 hops tiene 2.5-15 segundos solo de latencia de comunicacion.

### Arbol de decision: solo o multi?

```python
"""
Arbol de decision para determinar si necesitas multi-agente.
Usa esto antes de complicar tu arquitectura.
"""

from dataclasses import dataclass
from enum import Enum


class Recommendation(Enum):
    SINGLE_AGENT = "single_agent"
    MULTI_AGENT = "multi_agent"
    MAYBE_MULTI = "maybe_multi_agent"


@dataclass
class SystemRequirements:
    """Requisitos del sistema que informan la decision."""
    fits_single_context: bool  # el problema cabe en una ventana
    requires_multiple_domains: bool  # necesita expertise diverso
    needs_cross_validation: bool  # beneficia de verificacion cruzada
    has_observability: bool  # ya tienes observabilidad para 1 agente
    latency_budget_ms: int  # presupuesto de latencia total
    cost_sensitive: bool  # los costos son una preocupacion
    error_tolerance: str  # "high", "medium", "low"


def should_use_multi_agent(reqs: SystemRequirements) -> dict:
    """Evalua si un sistema multi-agente se justifica.

    Retorna la recomendacion con justificacion.
    """
    reasons_for = []
    reasons_against = []

    # Factor 1: Complejidad del problema
    if not reqs.fits_single_context:
        reasons_for.append(
            "El problema no cabe en una sola ventana de contexto"
        )
    else:
        reasons_against.append(
            "Un solo agente puede ver toda la informacion"
        )

    # Factor 2: Dominios multiples
    if reqs.requires_multiple_domains:
        reasons_for.append(
            "Se requiere expertise de multiples dominios"
        )

    # Factor 3: Verificacion cruzada
    if reqs.needs_cross_validation and reqs.error_tolerance == "low":
        reasons_for.append(
            "Baja tolerancia a errores + necesidad de validacion cruzada"
        )

    # Factor 4: Observabilidad
    if not reqs.has_observability:
        reasons_against.append(
            "Sin observabilidad para un agente, multi-agente "
            "sera imposible de depurar"
        )

    # Factor 5: Latencia
    if reqs.latency_budget_ms < 5000:
        reasons_against.append(
            f"Presupuesto de latencia ({reqs.latency_budget_ms}ms) "
            f"demasiado ajustado para multi-agente"
        )

    # Factor 6: Costo
    if reqs.cost_sensitive:
        reasons_against.append(
            "Multi-agente multiplica costos 3-15x"
        )

    # Decision
    score = len(reasons_for) - len(reasons_against)
    if score >= 2:
        recommendation = Recommendation.MULTI_AGENT
    elif score >= 0:
        recommendation = Recommendation.MAYBE_MULTI
    else:
        recommendation = Recommendation.SINGLE_AGENT

    return {
        "recommendation": recommendation.value,
        "reasons_for": reasons_for,
        "reasons_against": reasons_against,
        "note": (
            "Empieza con un solo agente y escala solo cuando "
            "puedas demostrar que no es suficiente."
        ),
    }


# Ejemplo: sistema de atencion al cliente
resultado = should_use_multi_agent(SystemRequirements(
    fits_single_context=True,
    requires_multiple_domains=False,
    needs_cross_validation=False,
    has_observability=True,
    latency_budget_ms=3000,
    cost_sensitive=True,
    error_tolerance="medium",
))
print(f"Recomendacion: {resultado['recommendation']}")
# -> "single_agent"

# Ejemplo: sistema de analisis de seguridad de codigo
resultado = should_use_multi_agent(SystemRequirements(
    fits_single_context=False,
    requires_multiple_domains=True,
    needs_cross_validation=True,
    has_observability=True,
    latency_budget_ms=30000,
    cost_sensitive=False,
    error_tolerance="low",
))
print(f"Recomendacion: {resultado['recommendation']}")
# -> "multi_agent"
```

La regla de produccion es: **escala a multi-agente solo cuando puedas demostrar que un solo agente no puede resolver el problema.** Dicho esto, hay casos donde multi-agente es genuinamente necesario, y el resto de este capitulo se enfoca en como hacerlo bien.

### Cuando un solo agente no basta

Piensa en el desarrollo de software como analogia. Un programador puede resolver tareas bien definidas: implementar una funcion, corregir un bug. Pero para un proyecto complejo necesitas un equipo: alguien para la arquitectura, otro para la seguridad, otro para el rendimiento, un lider tecnico que coordine.

Con los agentes ocurre algo similar. Un solo agente generalista maneja tareas simples, pero cuando el problema involucra multiples dominios de conocimiento, razonamiento profundo en paralelo o verificacion cruzada, un sistema multi-agente ofrece ventajas claras:

- **Especializacion**: cada agente se configura con prompts especializados para un dominio.
- **Paralelismo**: multiples agentes trabajan simultaneamente, reduciendo la latencia total.
- **Verificacion cruzada**: agentes independientes validan las conclusiones de otros.
- **Robustez**: si un agente falla, los demas pueden compensar.

Pero estas ventajas no son gratuitas. Introducen complejidad en la comunicacion, costos multiplicados de tokens, nuevos modos de fallo y el problema del consenso.

---

## 11.2 Topologias: centralizada, descentralizada y jerarquica

La forma en que organizas tus agentes determina las propiedades del sistema completo: latencia, tolerancia a fallos, costo y complejidad de depuracion.

### Centralizada (orquestador)

Un agente central recibe la tarea, la descompone, la delega a agentes especializados, recopila los resultados y sintetiza la respuesta final.

```python
"""
Topologia centralizada: un orquestador coordina agentes especializados.
"""

import asyncio
from dataclasses import dataclass
from typing import Any


@dataclass
class SubTask:
    """Subtarea generada por el orquestador."""
    id: str
    domain: str
    description: str
    input_data: dict
    priority: int = 1


@dataclass
class AgentResult:
    """Resultado de un agente."""
    agent_name: str
    output: Any
    confidence: float
    tokens_used: int
    duration_ms: float
    error: str | None = None

    @classmethod
    def timeout(cls, name: str) -> "AgentResult":
        return cls(name, None, 0.0, 0, 0, "timeout")

    @classmethod
    def from_error(cls, name: str, error: Exception) -> "AgentResult":
        return cls(name, None, 0.0, 0, 0, str(error))


class Agent:
    """Agente base con especialidad."""
    def __init__(self, name: str, specialty: str):
        self.name = name
        self.specialty = specialty

    async def execute(self, subtask: SubTask) -> AgentResult:
        raise NotImplementedError


class CentralizedOrchestrator:
    """Orquestador central que descompone, delega y sintetiza.

    Ventajas: control total, facil de depurar, flujo predecible.
    Desventajas: punto unico de fallo, cuello de botella.
    """

    def __init__(self, agents: list[Agent]):
        self.agents = {a.specialty: a for a in agents}

    async def process(self, task: str) -> dict:
        """Flujo completo: descomponer -> delegar -> sintetizar."""
        # Paso 1: descomponer la tarea en subtareas
        subtasks = await self._decompose(task)

        # Paso 2: delegar a agentes especializados
        results = {}
        for subtask in subtasks:
            agent = self.agents.get(subtask.domain)
            if agent is None:
                results[subtask.id] = AgentResult.from_error(
                    "orquestador",
                    ValueError(f"No hay agente para: {subtask.domain}"),
                )
                continue

            try:
                result = await asyncio.wait_for(
                    agent.execute(subtask),
                    timeout=30.0,
                )
                results[subtask.id] = result
            except asyncio.TimeoutError:
                results[subtask.id] = AgentResult.timeout(agent.name)

        # Paso 3: sintetizar resultados
        return await self._synthesize(task, results)

    async def _decompose(self, task: str) -> list[SubTask]:
        """Descompone una tarea en subtareas.
        En produccion: el LLM analiza la tarea y genera subtareas."""
        # Simulacion
        return [
            SubTask("st-1", "seguridad", "Analizar vulnerabilidades", {}),
            SubTask("st-2", "rendimiento", "Analizar cuellos de botella", {}),
        ]

    async def _synthesize(
        self, original_task: str, results: dict[str, AgentResult]
    ) -> dict:
        """Combina los resultados de los agentes.
        En produccion: el LLM sintetiza un reporte coherente."""
        successful = {
            k: v for k, v in results.items()
            if v.error is None
        }
        failed = {
            k: v for k, v in results.items()
            if v.error is not None
        }

        return {
            "task": original_task,
            "successful_analyses": len(successful),
            "failed_analyses": len(failed),
            "total_tokens": sum(
                r.tokens_used for r in results.values()
            ),
            "results": {
                k: {"output": v.output, "confidence": v.confidence}
                for k, v in successful.items()
            },
        }
```

**Ventajas**: simplicidad conceptual, control centralizado, facil de depurar.
**Desventajas**: punto unico de fallo, cuello de botella en el orquestador, la latencia es la suma de todas las subtareas si se ejecutan secuencialmente.

### Descentralizada (peer-to-peer)

Los agentes se comunican directamente entre si, sin un coordinador central. Cada agente decide a quien consultar basandose en el problema.

```python
"""
Topologia descentralizada: agentes se comunican peer-to-peer.
"""

import asyncio


class PeerAgent:
    """Agente que puede consultar a sus pares directamente.

    Ventajas: sin punto unico de fallo, escalable.
    Desventajas: riesgo de ciclos, dificil de depurar.
    """

    def __init__(self, name: str, specialty: str):
        self.name = name
        self.specialty = specialty
        self.peers: dict[str, "PeerAgent"] = {}
        self._max_delegation_depth = 3  # prevenir ciclos infinitos

    def register_peer(self, peer: "PeerAgent"):
        self.peers[peer.specialty] = peer

    async def execute(
        self, task: str, depth: int = 0
    ) -> AgentResult:
        """Intenta resolver la tarea, consultando pares si es necesario."""
        # Proteccion contra ciclos
        if depth >= self._max_delegation_depth:
            return AgentResult(
                self.name, "Limite de delegacion alcanzado",
                confidence=0.3, tokens_used=100, duration_ms=50,
            )

        # Intentar resolver solo
        result = await self._try_solve(task)

        if result.confidence < 0.7:
            # Buscar un par que pueda ayudar
            best_peer = self._select_peer(task)
            if best_peer:
                peer_result = await best_peer.execute(
                    task, depth=depth + 1
                )
                # Combinar mi resultado con el del par
                result = await self._merge_results(result, peer_result)

        return result

    async def _try_solve(self, task: str) -> AgentResult:
        """Intento de resolucion individual."""
        # En produccion: llamada al LLM
        return AgentResult(
            self.name, f"Analisis de {self.specialty}",
            confidence=0.65, tokens_used=500, duration_ms=2000,
        )

    def _select_peer(self, task: str) -> "PeerAgent | None":
        """Selecciona el par mas apropiado para la tarea."""
        # Logica de seleccion basada en la tarea
        # En produccion: el LLM decide a quien consultar
        for specialty, peer in self.peers.items():
            if specialty != self.specialty:  # no consultarse a si mismo
                return peer
        return None

    async def _merge_results(
        self, my_result: AgentResult, peer_result: AgentResult
    ) -> AgentResult:
        """Combina mi resultado con el de un par."""
        # En produccion: el LLM sintetiza ambos resultados
        combined_confidence = max(
            my_result.confidence, peer_result.confidence
        )
        return AgentResult(
            agent_name=f"{my_result.agent_name}+{peer_result.agent_name}",
            output=f"Combinado: {my_result.output} | {peer_result.output}",
            confidence=combined_confidence,
            tokens_used=my_result.tokens_used + peer_result.tokens_used,
            duration_ms=my_result.duration_ms + peer_result.duration_ms,
        )
```

### Jerarquica (capas de supervision)

Combina lo mejor de ambos mundos: agentes organizados en niveles, donde supervisores coordinan grupos de agentes especializados.

```python
"""
Topologia jerarquica: supervisores coordinan equipos de agentes.
"""

import asyncio


class TeamLead:
    """Lider de equipo: coordina un grupo de agentes especializados."""

    def __init__(self, name: str, agents: list[Agent]):
        self.name = name
        self.agents = agents

    async def execute(self, tasks: list[SubTask]) -> dict:
        """Distribuye tareas entre los miembros del equipo."""
        results = {}
        # Ejecutar tareas en paralelo dentro del equipo
        coroutines = []
        for i, task in enumerate(tasks):
            agent = self.agents[i % len(self.agents)]
            coroutines.append(agent.execute(task))

        agent_results = await asyncio.gather(
            *coroutines, return_exceptions=True
        )

        for i, result in enumerate(agent_results):
            if isinstance(result, Exception):
                results[tasks[i].id] = AgentResult.from_error(
                    self.agents[i % len(self.agents)].name, result
                )
            else:
                results[tasks[i].id] = result

        return results


class HierarchicalOrchestrator:
    """Orquestador jerarquico con supervisores y equipos.

    Estructura:
      Supervisor (nivel 2)
        ├── TeamLead: Seguridad
        │   ├── VulnScanner
        │   └── CodeAuditor
        └── TeamLead: Rendimiento
            ├── Profiler
            └── Optimizer
    """

    def __init__(self, teams: dict[str, TeamLead]):
        self.teams = teams

    async def process(self, task: str) -> dict:
        """Distribuye trabajo entre equipos en paralelo."""
        # En produccion: el LLM supervisor decide la distribucion
        team_tasks = {
            "seguridad": [
                SubTask("s1", "seguridad", "Scan de vulns", {}),
                SubTask("s2", "seguridad", "Audit de codigo", {}),
            ],
            "rendimiento": [
                SubTask("p1", "rendimiento", "Profiling", {}),
                SubTask("p2", "rendimiento", "Optimizar queries", {}),
            ],
        }

        # Equipos trabajan en paralelo
        coroutines = {
            team_name: team.execute(tasks)
            for team_name, team in self.teams.items()
            if team_name in team_tasks
            for tasks in [team_tasks[team_name]]
        }

        team_results = await asyncio.gather(
            *coroutines.values(), return_exceptions=True
        )

        return {
            "teams": list(coroutines.keys()),
            "results": dict(zip(coroutines.keys(), team_results)),
        }
```

Esta topologia se parece a la estructura organizacional de una empresa. La clave es que cada capa de supervision debe agregar valor (filtrar, priorizar, resolver conflictos), no solo pasar mensajes. Si tus supervisores son proxies transparentes, estas anadiendo latencia y costo sin ganar resiliencia.

### Comparativa de topologias

| Topologia | Latencia | Tolerancia a fallos | Complejidad | Mejor para |
|-----------|----------|---------------------|-------------|------------|
| Centralizada | Media | Baja | Baja | Tareas con descomposicion clara |
| Descentralizada | Variable | Alta | Alta | Sistemas adaptativos |
| Jerarquica | Media-Alta | Media | Media | Organizaciones grandes |
| Pipeline | Alta (suma) | Baja | Baja | Procesamiento secuencial |
| Fan-out/fan-in | Baja* | Alta | Media | Validacion cruzada |

*La latencia de fan-out/fan-in es la del agente mas lento, no la suma.

---

## 11.3 Patrones de orquestacion: pipeline, scatter-gather y voting

### Pipeline: procesamiento secuencial

Los agentes se organizan en una cadena donde la salida de uno es la entrada del siguiente. Es el patron mas natural cuando el trabajo tiene fases claras.

```python
"""
Patron pipeline: agentes procesan en secuencia.
Cada etapa transforma los datos para la siguiente.
"""

import asyncio
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PipelineStageResult:
    """Resultado de una etapa del pipeline."""
    stage_name: str
    output: Any
    confidence: float
    tokens_used: int
    duration_ms: float


@dataclass
class PipelineResult:
    """Resultado completo del pipeline."""
    stages: list[PipelineStageResult]
    final_output: Any
    total_tokens: int
    total_duration_ms: float
    success: bool
    error: str | None = None


class PipelineStage:
    """Etapa individual del pipeline."""

    def __init__(self, name: str, min_confidence: float = 0.5):
        self.name = name
        self.min_confidence = min_confidence

    async def process(self, input_data: Any) -> PipelineStageResult:
        raise NotImplementedError


class AgentPipeline:
    """Pipeline de agentes con validacion entre etapas.

    Cada etapa valida que su entrada cumple requisitos minimos
    antes de procesar. Si una etapa produce un resultado con
    confianza menor al umbral, el pipeline se detiene.
    """

    def __init__(
        self,
        stages: list[PipelineStage],
        stop_on_low_confidence: bool = True,
    ):
        self.stages = stages
        self.stop_on_low_confidence = stop_on_low_confidence

    async def run(self, initial_input: Any) -> PipelineResult:
        """Ejecuta el pipeline completo."""
        current_input = initial_input
        stage_results: list[PipelineStageResult] = []
        total_tokens = 0
        start_time = time.time()

        for stage in self.stages:
            try:
                result = await stage.process(current_input)
                stage_results.append(result)
                total_tokens += result.tokens_used

                # Verificar confianza
                if (
                    self.stop_on_low_confidence
                    and result.confidence < stage.min_confidence
                ):
                    elapsed = (time.time() - start_time) * 1000
                    return PipelineResult(
                        stages=stage_results,
                        final_output=result.output,
                        total_tokens=total_tokens,
                        total_duration_ms=elapsed,
                        success=False,
                        error=(
                            f"Etapa '{stage.name}' produjo confianza "
                            f"{result.confidence:.2f} < "
                            f"{stage.min_confidence:.2f}"
                        ),
                    )

                current_input = result.output

            except Exception as e:
                elapsed = (time.time() - start_time) * 1000
                return PipelineResult(
                    stages=stage_results,
                    final_output=None,
                    total_tokens=total_tokens,
                    total_duration_ms=elapsed,
                    success=False,
                    error=f"Error en etapa '{stage.name}': {e}",
                )

        elapsed = (time.time() - start_time) * 1000
        return PipelineResult(
            stages=stage_results,
            final_output=current_input,
            total_tokens=total_tokens,
            total_duration_ms=elapsed,
            success=True,
        )


# Ejemplo: pipeline de procesamiento de documentos
class ExtractorStage(PipelineStage):
    async def process(self, input_data: Any) -> PipelineStageResult:
        # En produccion: LLM extrae entidades del documento
        return PipelineStageResult(
            stage_name=self.name,
            output={
                "entidades": ["Acme Corp", "Q3 2026"],
                "tipo": "reporte_financiero",
            },
            confidence=0.92,
            tokens_used=1500,
            duration_ms=2100,
        )


class ClassifierStage(PipelineStage):
    async def process(self, input_data: Any) -> PipelineStageResult:
        # En produccion: LLM clasifica el contenido
        return PipelineStageResult(
            stage_name=self.name,
            output={
                **input_data,
                "clasificacion": "urgente",
                "departamento": "finanzas",
            },
            confidence=0.88,
            tokens_used=800,
            duration_ms=1500,
        )


class ResponseStage(PipelineStage):
    async def process(self, input_data: Any) -> PipelineStageResult:
        # En produccion: LLM genera respuesta final
        return PipelineStageResult(
            stage_name=self.name,
            output={
                "respuesta": "El reporte de Acme Corp Q3 2026 "
                             "requiere atencion inmediata.",
                "acciones": ["Notificar a finanzas", "Agendar revision"],
            },
            confidence=0.85,
            tokens_used=2000,
            duration_ms=2500,
        )


async def demo_pipeline():
    pipeline = AgentPipeline([
        ExtractorStage("extractor", min_confidence=0.7),
        ClassifierStage("clasificador", min_confidence=0.7),
        ResponseStage("generador", min_confidence=0.7),
    ])

    result = await pipeline.run("Documento financiero de entrada...")
    print(f"Exito: {result.success}")
    print(f"Tokens totales: {result.total_tokens}")
    print(f"Duracion: {result.total_duration_ms:.0f}ms")
    print(f"Etapas: {[s.stage_name for s in result.stages]}")
```

**Ventajas**: facil de razonar, cada agente tiene una responsabilidad clara (alta cohesion), facil de probar etapa por etapa.
**Desventajas**: la latencia es la suma de todas las etapas, un fallo en cualquier etapa detiene todo, no aprovecha el paralelismo.

### Scatter-gather: fan-out/fan-in

Una tarea se distribuye a multiples agentes simultaneamente (scatter/fan-out), y sus resultados se agregan (gather/fan-in). Es la topologia ideal cuando necesitas multiples perspectivas sobre el mismo problema.

```python
"""
Patron scatter-gather (fan-out/fan-in).
Multiples agentes analizan el mismo problema en paralelo.
"""

import asyncio
import time
from dataclasses import dataclass
from typing import Any


@dataclass
class ScatterGatherConfig:
    """Configuracion del patron scatter-gather."""
    timeout_per_agent: float = 30.0
    min_responses: int = 1  # minimo de respuestas requeridas
    require_all: bool = False  # requerir TODAS las respuestas


class ScatterGather:
    """Distribuye una tarea a N agentes y agrega resultados.

    La latencia total es la del agente mas lento (no la suma),
    lo cual es una ventaja significativa sobre el pipeline.
    """

    def __init__(
        self,
        agents: list[Agent],
        config: ScatterGatherConfig = ScatterGatherConfig(),
    ):
        self.agents = agents
        self.config = config

    async def execute(self, task: str) -> dict:
        """Fan-out: todos los agentes trabajan en paralelo.
        Fan-in: agregar resultados."""
        start_time = time.time()

        # Scatter: lanzar todos los agentes en paralelo
        coroutines = [
            self._execute_with_timeout(agent, task)
            for agent in self.agents
        ]
        raw_results = await asyncio.gather(
            *coroutines, return_exceptions=True
        )

        # Separar exitos de fallos
        successes = []
        failures = []
        for i, result in enumerate(raw_results):
            if isinstance(result, Exception):
                failures.append({
                    "agent": self.agents[i].name,
                    "error": str(result),
                })
            elif result.error:
                failures.append({
                    "agent": result.agent_name,
                    "error": result.error,
                })
            else:
                successes.append(result)

        # Verificar que tenemos suficientes respuestas
        if len(successes) < self.config.min_responses:
            raise RuntimeError(
                f"Solo {len(successes)} agentes respondieron, "
                f"se requieren {self.config.min_responses}. "
                f"Fallos: {failures}"
            )

        elapsed = (time.time() - start_time) * 1000

        # Gather: agregar resultados
        aggregated = self._aggregate(successes)

        return {
            "result": aggregated,
            "agents_responded": len(successes),
            "agents_failed": len(failures),
            "failures": failures,
            "total_tokens": sum(r.tokens_used for r in successes),
            "total_duration_ms": elapsed,
        }

    async def _execute_with_timeout(
        self, agent: Agent, task: str
    ) -> AgentResult:
        """Ejecuta un agente con timeout."""
        subtask = SubTask(
            id=f"sg-{agent.name}",
            domain=agent.specialty,
            description=task,
            input_data={"task": task},
        )
        return await asyncio.wait_for(
            agent.execute(subtask),
            timeout=self.config.timeout_per_agent,
        )

    def _aggregate(self, results: list[AgentResult]) -> dict:
        """Agrega resultados de multiples agentes.

        Estrategia: promediar confianza, combinar outputs.
        En produccion: un LLM sintetiza los resultados.
        """
        avg_confidence = sum(
            r.confidence for r in results
        ) / len(results)

        return {
            "combined_output": [
                {"agent": r.agent_name, "output": r.output}
                for r in results
            ],
            "avg_confidence": avg_confidence,
            "max_confidence": max(r.confidence for r in results),
            "consensus": self._check_consensus(results),
        }

    def _check_consensus(self, results: list[AgentResult]) -> dict:
        """Verifica si los agentes estan de acuerdo."""
        # Simplificado: en produccion usarias similitud semantica
        confidences = [r.confidence for r in results]
        spread = max(confidences) - min(confidences)

        return {
            "agreement_level": "high" if spread < 0.15 else (
                "medium" if spread < 0.30 else "low"
            ),
            "confidence_spread": spread,
        }
```

**Ventajas**: latencia = max(agentes), no suma; tolerancia a fallos (si un agente falla, los demas compensan); ideal para validacion cruzada.
**Desventajas**: consume mas tokens (N agentes procesan la misma tarea), los rate limits del proveedor pueden serializar las llamadas si todos usan el mismo modelo.

### Voting: consenso por votacion

Los agentes votan sobre la respuesta correcta. Es el patron mas directo para implementar consenso, pero tiene sutilezas importantes.

```python
"""
Patron voting: multiples agentes votan sobre la respuesta.
Incluye votacion simple, ponderada y debate adversarial.
"""

import asyncio
from dataclasses import dataclass
from typing import Any


# --- Votacion por mayoria ---

class MajorityVoting:
    """Cada agente produce una respuesta. Se elige la mas comun.

    El desafio: "la misma respuesta" en texto libre es ambiguo.
    Necesitas similitud semantica, no igualdad exacta.
    """

    def __init__(
        self,
        agents: list[Agent],
        similarity_threshold: float = 0.85,
    ):
        self.agents = agents
        self.similarity_threshold = similarity_threshold

    async def decide(self, task: str) -> dict:
        # Todos los agentes responden en paralelo
        subtasks = [
            SubTask(f"vote-{a.name}", a.specialty, task, {})
            for a in self.agents
        ]
        results = await asyncio.gather(
            *[a.execute(st) for a, st in zip(self.agents, subtasks)],
            return_exceptions=True,
        )

        valid_results = [
            r for r in results if not isinstance(r, Exception)
        ]

        if not valid_results:
            raise RuntimeError("Ningun agente pudo responder")

        # Agrupar respuestas similares
        clusters = self._cluster_responses(valid_results)

        # El cluster mas grande gana
        winner = max(clusters, key=len)
        best_in_cluster = max(winner, key=lambda r: r.confidence)

        return {
            "winner": best_in_cluster.output,
            "confidence": best_in_cluster.confidence,
            "votes": len(winner),
            "total_agents": len(valid_results),
            "consensus_ratio": len(winner) / len(valid_results),
            "clusters": len(clusters),
        }

    def _cluster_responses(
        self, results: list[AgentResult]
    ) -> list[list[AgentResult]]:
        """Agrupa respuestas semanticamente similares.

        En produccion: usar embeddings y similitud coseno.
        Aqui simplificamos con igualdad de strings.
        """
        clusters: list[list[AgentResult]] = []
        used = set()

        for i, r1 in enumerate(results):
            if i in used:
                continue
            cluster = [r1]
            used.add(i)
            for j, r2 in enumerate(results):
                if j not in used and self._are_similar(r1, r2):
                    cluster.append(r2)
                    used.add(j)
            clusters.append(cluster)

        return clusters

    def _are_similar(
        self, r1: AgentResult, r2: AgentResult
    ) -> bool:
        """Verifica similitud semantica entre dos respuestas.
        En produccion: embeddings + similitud coseno."""
        # Simplificacion: comparar strings
        return str(r1.output) == str(r2.output)


# --- Votacion ponderada ---

class WeightedVoting:
    """Votacion donde cada agente tiene un peso diferente
    segun su expertise en el dominio de la tarea.

    Un agente de seguridad tiene mas peso en cuestiones
    de seguridad que un agente generalista.
    """

    def __init__(
        self,
        agents: list[Agent],
        weights: dict[str, dict[str, float]],
    ):
        self.agents = agents
        # weights[agent_name][domain] = peso
        self.weights = weights

    async def decide(self, task: str, domain: str) -> dict:
        subtasks = [
            SubTask(f"wv-{a.name}", a.specialty, task, {})
            for a in self.agents
        ]
        results = await asyncio.gather(
            *[a.execute(st) for a, st in zip(self.agents, subtasks)],
            return_exceptions=True,
        )

        weighted_results = []
        for result in results:
            if isinstance(result, Exception):
                continue
            weight = self.weights.get(
                result.agent_name, {}
            ).get(domain, 1.0)
            weighted_results.append((result, weight))

        if not weighted_results:
            raise RuntimeError("Sin resultados validos")

        # Seleccionar el resultado con mayor peso * confianza
        best = max(
            weighted_results,
            key=lambda rw: rw[0].confidence * rw[1],
        )

        return {
            "winner": best[0].output,
            "confidence": best[0].confidence,
            "weight": best[1],
            "weighted_score": best[0].confidence * best[1],
            "agent": best[0].agent_name,
        }


# --- Debate adversarial ---

class AdversarialDebate:
    """Un agente propone, otro critica, un juez evalua.

    Este patron reduce alucinaciones porque fuerza al
    agente a justificar sus afirmaciones. Irving et al.
    (2018) mostraron que el debate adversarial mejora
    la alineacion. Du et al. (2023) confirmaron una
    mejora de 10-20% en factualidad.
    """

    def __init__(
        self,
        proposer: Agent,
        critic: Agent,
        judge: Agent,
        max_rounds: int = 3,
    ):
        self.proposer = proposer
        self.critic = critic
        self.judge = judge
        self.max_rounds = max_rounds

    async def debate(self, task: str) -> dict:
        """Ejecuta el debate: proponer -> criticar -> defender."""
        history = []
        tokens_total = 0

        # Propuesta inicial
        proposal_subtask = SubTask(
            "debate-proposal", self.proposer.specialty, task, {}
        )
        proposal = await self.proposer.execute(proposal_subtask)
        history.append({
            "role": "proposer",
            "content": proposal.output,
        })
        tokens_total += proposal.tokens_used

        for round_num in range(self.max_rounds):
            # El critico ataca
            critique_subtask = SubTask(
                f"debate-critique-{round_num}",
                self.critic.specialty,
                f"Critica esta propuesta: {proposal.output}",
                {"history": history},
            )
            critique = await self.critic.execute(critique_subtask)
            history.append({
                "role": "critic",
                "content": critique.output,
            })
            tokens_total += critique.tokens_used

            # El proponente defiende o corrige
            defense_subtask = SubTask(
                f"debate-defense-{round_num}",
                self.proposer.specialty,
                f"Defiende o corrige ante: {critique.output}",
                {"history": history},
            )
            defense = await self.proposer.execute(defense_subtask)
            history.append({
                "role": "proposer",
                "content": defense.output,
            })
            tokens_total += defense.tokens_used
            proposal = defense  # actualizar propuesta

        # El juez evalua el debate completo
        judge_subtask = SubTask(
            "debate-judge", self.judge.specialty,
            f"Evalua este debate y da un veredicto: {history}",
            {"history": history},
        )
        verdict = await self.judge.execute(judge_subtask)
        tokens_total += verdict.tokens_used

        return {
            "verdict": verdict.output,
            "confidence": verdict.confidence,
            "rounds": self.max_rounds,
            "total_tokens": tokens_total,
            "history_length": len(history),
        }
```

El costo del debate es significativo: cada ronda multiplica el consumo de tokens. Un debate de 3 rondas con 3 agentes puede consumir 10x mas tokens que una sola llamada. Con precios de 2026, eso puede ser $0.40-$0.75 por debate. A 10,000 consultas diarias: $4,000-$7,500 al dia.

---

## 11.4 El problema del consenso aplicado a agentes

### Los generales bizantinos y los agentes que alucinan

En 1982, Leslie Lamport, Robert Shostak y Marshall Pease formularon el **problema de los generales bizantinos**: varios generales deben coordinar un ataque, pero algunos pueden ser traidores que envian mensajes contradictorios. La pregunta: pueden los generales leales llegar a un acuerdo a pesar de los traidores?

La analogia con agentes de IA es tentadora: reemplaza "traidores" por "agentes que alucinan". Pero hay una diferencia crucial. Un nodo bizantino puede enviar mensajes *arbitrarios y diferentes* a cada receptor, comportandose de forma adversarial. Un agente que alucina produce la *misma* respuesta incorrecta para todos, con formato correcto y argumentos convincentes. Es mas parecido a un fallo de tipo "crash con respuesta incorrecta" que a un fallo bizantino completo [Sun et al., 2024].

El resultado clasico de Lamport dice que para tolerar `f` nodos bizantinos necesitas al menos `3f + 1` nodos. Pero este resultado no es directamente aplicable a agentes LLM porque resuelve un problema diferente: la tolerancia a nodos *adversariales*. Las alucinaciones de LLMs son un problema de **correlacion**, no de adversarialidad.

Tres instancias del mismo modelo comparten los mismos datos de entrenamiento, los mismos sesgos y los mismos puntos ciegos. Si una instancia alucina que "el framework X fue deprecado en 2025", las otras dos probablemente confirmaran la alucinacion porque comparten la misma distribucion de probabilidades. La redundancia numerica sin diversidad de modelo es teatro de seguridad.

### Diversidad de modelos: la verdadera defensa

Lo que realmente necesitas es **diversidad de modelos**. Tres agentes con modelos distintos (Claude, GPT-4, Gemini) son mas robustos que cinco instancias del mismo modelo, porque sus errores estan menos correlacionados.

```python
"""
Consenso con diversidad de modelos.
Usa diferentes proveedores para reducir la correlacion de errores.
"""

import asyncio
from dataclasses import dataclass


@dataclass
class ModelConfig:
    """Configuracion de un modelo LLM."""
    provider: str  # "anthropic", "openai", "google"
    model: str     # "claude-sonnet-4-20250514", "gpt-4o", "gemini-2.5-pro"
    weight: float = 1.0  # peso en la votacion


class DiverseConsensus:
    """Consenso entre agentes con modelos diversos.

    La clave: los errores de modelos diferentes estan
    menos correlacionados que los de instancias del
    mismo modelo. Esto rompe las camaras de eco.
    """

    def __init__(self, model_configs: list[ModelConfig]):
        self.configs = model_configs
        self._validate_diversity()

    def _validate_diversity(self):
        """Verifica que hay diversidad real de proveedores."""
        providers = set(c.provider for c in self.configs)
        if len(providers) < 2:
            import warnings
            warnings.warn(
                f"Solo {len(providers)} proveedor(es) configurados. "
                f"La diversidad de modelos requiere multiples "
                f"proveedores para ser efectiva."
            )

    async def reach_consensus(
        self,
        task: str,
        min_agreement: float = 0.66,
    ) -> dict:
        """Busca consenso entre modelos diversos.

        1. Cada modelo responde INDEPENDIENTEMENTE (sin ver
           las respuestas de los otros).
        2. Se agrupan las respuestas por similitud semantica.
        3. Se aplica votacion ponderada.
        4. Si no hay consenso, se ejecuta una segunda ronda
           donde cada modelo ve las respuestas de los otros
           y puede cambiar su respuesta.
        """
        # Ronda 1: respuestas independientes
        responses = await self._independent_round(task)

        # Verificar consenso
        consensus = self._evaluate_consensus(responses)

        if consensus["agreement_ratio"] >= min_agreement:
            return {
                "result": consensus["winner"],
                "confidence": consensus["confidence"],
                "round": 1,
                "agreement": consensus["agreement_ratio"],
                "method": "independent_consensus",
            }

        # Ronda 2: debate informado (cada modelo ve las otras respuestas)
        revised = await self._informed_round(task, responses)
        consensus = self._evaluate_consensus(revised)

        return {
            "result": consensus["winner"],
            "confidence": consensus["confidence"],
            "round": 2,
            "agreement": consensus["agreement_ratio"],
            "method": "informed_consensus",
        }

    async def _independent_round(self, task: str) -> list[dict]:
        """Ronda donde cada modelo responde sin ver a los otros."""
        # En produccion: llamadas paralelas a diferentes APIs
        responses = []
        for config in self.configs:
            response = {
                "provider": config.provider,
                "model": config.model,
                "weight": config.weight,
                "output": f"Respuesta de {config.model}",
                "confidence": 0.85,
            }
            responses.append(response)
        return responses

    async def _informed_round(
        self, task: str, previous_responses: list[dict]
    ) -> list[dict]:
        """Ronda donde cada modelo ve las respuestas de los otros."""
        context = (
            "Otros agentes respondieron:\n"
            + "\n".join(
                f"- {r['model']}: {r['output']}"
                for r in previous_responses
            )
            + "\n\nConsidera sus perspectivas y da tu respuesta final."
        )
        # En produccion: nueva llamada al LLM con el contexto adicional
        return previous_responses  # simplificado

    def _evaluate_consensus(self, responses: list[dict]) -> dict:
        """Evalua el nivel de consenso entre las respuestas."""
        if not responses:
            return {"winner": None, "confidence": 0.0, "agreement_ratio": 0.0}

        # Simplificado: en produccion usar embeddings
        # Seleccionar la respuesta con mayor peso * confianza
        best = max(
            responses,
            key=lambda r: r["confidence"] * r["weight"],
        )

        return {
            "winner": best["output"],
            "confidence": best["confidence"],
            "agreement_ratio": 1.0,  # simplificado
        }
```

### Investigacion reciente en consenso para agentes LLM

La investigacion en 2025-2026 explora activamente la conexion entre tolerancia a fallos bizantinos y agentes LLM:

- **IBGP (Imperfect Byzantine Generals Problem)** [Sun et al., 2024] formaliza una version del problema donde el consenso no necesita ser perfecto, sino *suficientemente bueno*. Esto refleja la naturaleza probabilistica de los LLMs.

- **CP-WBFT (Confidence Probe-Based Weighted BFT)** [Li et al., 2025] propone un mecanismo que aprovecha la capacidad intrinseca de los LLMs para evaluar la calidad de las respuestas de otros agentes, usando "sondas de confianza" para ponderar votos.

- **DecentLLMs** [Jo, 2025] adopta el algoritmo de Mediana Geometrica para la agregacion de scores entre agentes, que es resiliente a ataques bizantinos mientras se mantenga una mayoria honesta.

- **BlockAgents** [Zhang et al., 2024] propone *proof-of-thought*: un mecanismo de consenso donde los agentes deben demostrar su razonamiento (analogo a proof-of-work en blockchain) antes de que su respuesta cuente.

Estas investigaciones son preliminares, no resultados consolidados. Pero sugieren que los sistemas multi-agente pueden ser mas resilientes que los sistemas distribuidos clasicos si aprovechan la capacidad de los LLMs para evaluar la calidad de las respuestas de otros agentes.

---

## 11.5 Patrones de fallo en sistemas multi-agente

### Alucinacion amplificada en cadena

El patron de fallo mas insidioso: un agente alucina, otro confirma la alucinacion, y un tercero la amplifica. Cada paso anade credibilidad al error.

```python
"""
Deteccion y mitigacion de alucinacion en cadena.
"""

from dataclasses import dataclass


@dataclass
class ChainValidation:
    """Resultado de validacion en cadena."""
    step: int
    agent: str
    claim: str
    verified: bool
    verification_method: str


class ChainHallucinationDetector:
    """Detecta cuando agentes se refuerzan mutuamente en un error.

    Estrategia: verificar cada afirmacion con un metodo
    independiente del LLM (deterministico o de otra fuente).
    """

    def __init__(self, deterministic_verifiers: dict):
        # verifiers[dominio] = funcion_de_verificacion
        self.verifiers = deterministic_verifiers

    def validate_chain(
        self,
        chain: list[dict],  # [{"agent": ..., "claim": ..., "domain": ...}]
    ) -> list[ChainValidation]:
        """Valida cada eslabón de la cadena de afirmaciones."""
        validations = []

        for i, step in enumerate(chain):
            domain = step.get("domain", "general")
            verifier = self.verifiers.get(domain)

            if verifier:
                verified = verifier(step["claim"])
                method = "deterministic"
            else:
                # Sin verificador deterministico: marcar como no verificado
                verified = None
                method = "unverified"

            validations.append(ChainValidation(
                step=i,
                agent=step["agent"],
                claim=step["claim"],
                verified=verified,
                verification_method=method,
            ))

        return validations

    def detect_echo_chamber(
        self, validations: list[ChainValidation]
    ) -> dict:
        """Detecta si los agentes estan en una camara de eco."""
        unverified = [v for v in validations if v.verified is None]
        verified_false = [v for v in validations if v.verified is False]

        risk_level = "low"
        if len(unverified) > len(validations) * 0.5:
            risk_level = "medium"
        if verified_false:
            risk_level = "high"

        return {
            "risk_level": risk_level,
            "unverified_claims": len(unverified),
            "false_claims": len(verified_false),
            "total_claims": len(validations),
            "recommendation": (
                "Agregar verificadores deterministicos "
                "para los dominios sin cobertura"
                if risk_level != "low"
                else "Cadena de verificacion saludable"
            ),
        }
```

### Deadlock agentico

Agente A espera a B, B espera a A. En sistemas multi-agente esto ocurre cuando dos agentes se consultan mutuamente sin un mecanismo de ruptura.

```python
"""
Deteccion y prevencion de deadlocks entre agentes.
"""

import asyncio
import time


class DeadlockDetector:
    """Detecta deadlocks en la comunicacion entre agentes.

    Usa un grafo de espera: si detecta un ciclo,
    rompe el deadlock cancelando la peticion mas reciente.
    """

    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout
        # wait_graph[agent_a] = agent_b significa "A espera a B"
        self._wait_graph: dict[str, str] = {}
        self._lock = asyncio.Lock()

    async def register_wait(
        self, waiter: str, waiting_for: str
    ) -> bool:
        """Registra que un agente esta esperando a otro.
        Retorna False si esto crearia un deadlock."""
        async with self._lock:
            # Verificar si crear esta arista genera un ciclo
            if self._would_create_cycle(waiter, waiting_for):
                return False  # deadlock detectado, no registrar

            self._wait_graph[waiter] = waiting_for
            return True

    async def release_wait(self, waiter: str):
        """Marca que un agente ya no esta esperando."""
        async with self._lock:
            self._wait_graph.pop(waiter, None)

    def _would_create_cycle(
        self, start: str, target: str
    ) -> bool:
        """Verifica si agregar start -> target crea un ciclo."""
        visited = {start}
        current = target

        while current in self._wait_graph:
            if current in visited:
                return True  # ciclo detectado
            visited.add(current)
            current = self._wait_graph[current]

        return current in visited


class DeadlockSafeAgent:
    """Agente con proteccion contra deadlocks."""

    def __init__(
        self,
        name: str,
        detector: DeadlockDetector,
    ):
        self.name = name
        self.detector = detector

    async def request(
        self,
        target_name: str,
        target_agent,
        task: str,
    ) -> dict:
        """Envia una peticion con proteccion contra deadlock."""
        can_wait = await self.detector.register_wait(
            self.name, target_name
        )

        if not can_wait:
            return {
                "error": "deadlock_prevented",
                "message": (
                    f"Peticion de {self.name} a {target_name} "
                    f"crearia un deadlock"
                ),
            }

        try:
            # Ejecutar con timeout como segunda capa de proteccion
            result = await asyncio.wait_for(
                target_agent.execute(task),
                timeout=self.detector.timeout,
            )
            return {"result": result}
        except asyncio.TimeoutError:
            return {
                "error": "timeout",
                "message": f"{target_name} no respondio en tiempo",
            }
        finally:
            await self.detector.release_wait(self.name)
```

### Explosion de costos

Cada hop entre agentes consume tokens. Sin control, los costos se desbordan rapidamente.

```python
"""
Control de costos en sistemas multi-agente.
"""

import time
from dataclasses import dataclass, field


@dataclass
class CostTracker:
    """Rastrea y limita los costos de un sistema multi-agente."""
    max_budget_usd: float
    cost_per_1k_input_tokens: float = 0.003  # ejemplo: Claude Sonnet
    cost_per_1k_output_tokens: float = 0.015

    # Estado interno
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    _spent_usd: float = 0.0
    _alerts: list[str] = field(default_factory=list)

    def record_usage(
        self,
        agent_name: str,
        input_tokens: int,
        output_tokens: int,
    ):
        """Registra el uso de tokens de un agente."""
        cost = (
            (input_tokens / 1000) * self.cost_per_1k_input_tokens
            + (output_tokens / 1000) * self.cost_per_1k_output_tokens
        )
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self._spent_usd += cost

        # Alertas por umbral
        usage_pct = self._spent_usd / self.max_budget_usd
        if usage_pct > 0.90 and "90%" not in str(self._alerts):
            self._alerts.append(
                f"ALERTA: 90% del presupuesto consumido "
                f"(${self._spent_usd:.2f}/${self.max_budget_usd:.2f})"
            )

    def can_continue(self) -> bool:
        """Verifica si hay presupuesto disponible."""
        return self._spent_usd < self.max_budget_usd

    def remaining_budget(self) -> dict:
        return {
            "spent_usd": round(self._spent_usd, 4),
            "remaining_usd": round(
                self.max_budget_usd - self._spent_usd, 4
            ),
            "usage_pct": round(
                (self._spent_usd / self.max_budget_usd) * 100, 1
            ),
            "total_tokens": (
                self.total_input_tokens + self.total_output_tokens
            ),
            "alerts": self._alerts,
        }
```

### Fallo silencioso colectivo

Todos los agentes acuerdan en algo incorrecto. Este es el patron de error del caso del trading: tres agentes, cero disidencia, pero la respuesta era erronea. La mitigacion requiere tres estrategias complementarias:

1. **Independencia primero**: no compartas la respuesta de un agente con otro antes de que el segundo genere la suya.
2. **Diversidad de modelos**: usa modelos de diferentes proveedores.
3. **Agente adversarial**: incluye un agente cuyo rol explicito sea encontrar problemas.

```python
"""
Anti-echo chamber: prevencion de fallo silencioso colectivo.
"""

import asyncio


class AntiEchoChamber:
    """Sistema que previene camaras de eco entre agentes.

    Combina las tres estrategias: independencia,
    diversidad y adversarialidad.
    """

    def __init__(
        self,
        primary_agents: list[Agent],
        devils_advocate: Agent,
    ):
        self.agents = primary_agents
        self.devils_advocate = devils_advocate

    async def decide(self, task: str) -> dict:
        """Proceso de decision resistente a echo chambers."""

        # Paso 1: cada agente responde INDEPENDIENTEMENTE
        # (no ven las respuestas de los otros)
        subtasks = [
            SubTask(f"ind-{a.name}", a.specialty, task, {})
            for a in self.agents
        ]
        responses = await asyncio.gather(
            *[a.execute(st) for a, st in zip(self.agents, subtasks)],
            return_exceptions=True,
        )
        valid_responses = [
            r for r in responses if not isinstance(r, Exception)
        ]

        # Paso 2: el abogado del diablo critica TODAS las respuestas
        critique_input = "\n".join(
            f"Agente {r.agent_name}: {r.output}"
            for r in valid_responses
        )
        critique_subtask = SubTask(
            "devils-critique",
            self.devils_advocate.specialty,
            f"Encuentra debilidades y errores en CADA respuesta. "
            f"Se esceptico:\n{critique_input}",
            {},
        )
        critique = await self.devils_advocate.execute(critique_subtask)

        # Paso 3: los agentes revisan considerando la critica
        revised_subtasks = [
            SubTask(
                f"rev-{a.name}", a.specialty,
                f"Reconsidera tu respuesta a la luz de esta critica: "
                f"{critique.output}\nTu respuesta original: {r.output}",
                {},
            )
            for a, r in zip(self.agents, valid_responses)
        ]
        revised = await asyncio.gather(
            *[
                a.execute(st)
                for a, st in zip(self.agents, revised_subtasks)
            ],
            return_exceptions=True,
        )

        valid_revised = [
            r for r in revised if not isinstance(r, Exception)
        ]

        # Paso 4: votacion final
        # Los agentes que cambiaron de opinion reciben
        # un bonus de confianza (mostraron flexibilidad)
        return {
            "original_responses": len(valid_responses),
            "revised_responses": len(valid_revised),
            "critique_applied": True,
            "final_result": (
                valid_revised[0].output if valid_revised else None
            ),
        }
```

---

## 11.6 Observabilidad y debugging en sistemas multi-agente

### Por que la observabilidad multi-agente es diferente

La observabilidad de un solo agente ya es compleja (como vimos en el Capitulo 8). La observabilidad multi-agente es ordenes de magnitud mas dificil porque necesitas rastrear interacciones *entre* agentes, no solo las acciones de cada uno.

El desafio central es la **propagacion de contexto entre fronteras**: cuando un trace cruza de un agente a otro, el contexto (trace ID, span ID, baggage) debe propagarse correctamente. En 2025-2026, OpenTelemetry ha emergido como el estandar de facto, con convenciones semanticas especificas para agentes de IA desarrolladas por Google, Microsoft y Cisco [OpenTelemetry, 2025].

### Tracing distribuido para agentes

```python
"""
Tracing distribuido para sistemas multi-agente.
Basado en los conceptos de OpenTelemetry.
"""

import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field


@dataclass
class Span:
    """Un span representa una operacion dentro de un trace."""
    trace_id: str
    span_id: str = field(
        default_factory=lambda: str(uuid.uuid4())[:8]
    )
    parent_span_id: str | None = None
    agent_name: str = ""
    operation: str = ""
    start_time: float = field(default_factory=time.time)
    end_time: float | None = None
    attributes: dict = field(default_factory=dict)
    events: list[dict] = field(default_factory=list)
    status: str = "OK"

    @property
    def duration_ms(self) -> float | None:
        if self.end_time is None:
            return None
        return (self.end_time - self.start_time) * 1000


class MultiAgentTracer:
    """Tracer distribuido para sistemas multi-agente.

    Registra cada operacion con su contexto completo:
    - Que agente la ejecuto
    - Cuanto tardo
    - Cuantos tokens uso
    - Que decidio
    - Que errores encontro

    En produccion: usa OpenTelemetry SDK con exportadores
    a Jaeger, Zipkin, o Datadog.
    """

    def __init__(self):
        self._traces: dict[str, list[Span]] = {}

    def start_trace(self, task: str) -> str:
        """Inicia un nuevo trace para una tarea."""
        trace_id = str(uuid.uuid4())[:12]
        self._traces[trace_id] = []

        # Span raiz
        root_span = Span(
            trace_id=trace_id,
            agent_name="system",
            operation="task_start",
            attributes={"task": task[:200]},
        )
        self._traces[trace_id].append(root_span)
        return trace_id

    @contextmanager
    def agent_span(
        self,
        trace_id: str,
        agent_name: str,
        operation: str,
        parent_span_id: str | None = None,
    ):
        """Context manager que crea un span para una operacion de agente."""
        span = Span(
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            agent_name=agent_name,
            operation=operation,
        )

        try:
            yield span
            span.status = "OK"
        except Exception as e:
            span.status = "ERROR"
            span.events.append({
                "name": "exception",
                "attributes": {
                    "exception.type": type(e).__name__,
                    "exception.message": str(e),
                },
                "timestamp": time.time(),
            })
            raise
        finally:
            span.end_time = time.time()
            if trace_id in self._traces:
                self._traces[trace_id].append(span)

    def add_event(
        self,
        trace_id: str,
        agent_name: str,
        event_name: str,
        attributes: dict | None = None,
    ):
        """Agrega un evento a un trace (como un log estructurado)."""
        spans = self._traces.get(trace_id, [])
        # Encontrar el span activo del agente
        active_spans = [
            s for s in spans
            if s.agent_name == agent_name and s.end_time is None
        ]
        if active_spans:
            active_spans[-1].events.append({
                "name": event_name,
                "attributes": attributes or {},
                "timestamp": time.time(),
            })

    def get_trace_summary(self, trace_id: str) -> dict:
        """Resumen del trace para depuracion."""
        spans = self._traces.get(trace_id, [])
        if not spans:
            return {"error": "Trace not found"}

        total_duration = None
        if spans[0].end_time:
            total_duration = (
                (spans[-1].end_time or time.time())
                - spans[0].start_time
            ) * 1000

        agents_involved = list(set(s.agent_name for s in spans))
        errors = [
            s for s in spans if s.status == "ERROR"
        ]

        return {
            "trace_id": trace_id,
            "total_spans": len(spans),
            "agents_involved": agents_involved,
            "total_duration_ms": total_duration,
            "errors": [
                {
                    "agent": s.agent_name,
                    "operation": s.operation,
                    "events": s.events,
                }
                for s in errors
            ],
            "span_tree": self._build_span_tree(spans),
        }

    def _build_span_tree(
        self, spans: list[Span]
    ) -> list[dict]:
        """Construye un arbol de spans para visualizacion."""
        return [
            {
                "agent": s.agent_name,
                "operation": s.operation,
                "duration_ms": s.duration_ms,
                "status": s.status,
                "tokens": s.attributes.get("tokens_used", "N/A"),
            }
            for s in spans
        ]


# Ejemplo de uso
async def demo_tracing():
    tracer = MultiAgentTracer()
    trace_id = tracer.start_trace("Analizar vulnerabilidades en codebase")

    # Agente orquestador
    with tracer.agent_span(
        trace_id, "orquestador", "decompose_task"
    ) as span:
        span.attributes["subtasks_created"] = 2
        await asyncio.sleep(0.1)  # simular trabajo

    # Agente de seguridad
    with tracer.agent_span(
        trace_id, "seguridad", "scan_vulnerabilities"
    ) as span:
        span.attributes["tokens_used"] = 3500
        span.attributes["vulns_found"] = 3
        tracer.add_event(
            trace_id, "seguridad",
            "vulnerability_detected",
            {"type": "sql_injection", "severity": "high"},
        )
        await asyncio.sleep(0.2)

    # Agente de rendimiento
    with tracer.agent_span(
        trace_id, "rendimiento", "profile_code"
    ) as span:
        span.attributes["tokens_used"] = 2800
        span.attributes["bottlenecks_found"] = 1
        await asyncio.sleep(0.15)

    # Resumen
    summary = tracer.get_trace_summary(trace_id)
    import json
    print(json.dumps(summary, indent=2, default=str))
```

### Metricas clave para monitoreo

Las metricas que debes rastrear en un sistema multi-agente van mas alla de las metricas individuales del Capitulo 8:

```python
"""
Metricas clave para sistemas multi-agente.
"""

import time
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class MultiAgentMetrics:
    """Metricas de un sistema multi-agente en produccion.

    Estas son las metricas que deben estar en tu dashboard.
    """

    # Metricas por agente
    agent_latency_ms: dict[str, list[float]] = field(
        default_factory=lambda: defaultdict(list)
    )
    agent_token_usage: dict[str, list[int]] = field(
        default_factory=lambda: defaultdict(list)
    )
    agent_error_count: dict[str, int] = field(
        default_factory=lambda: defaultdict(int)
    )
    agent_timeout_count: dict[str, int] = field(
        default_factory=lambda: defaultdict(int)
    )

    # Metricas del sistema
    total_tasks: int = 0
    successful_tasks: int = 0
    consensus_reached: int = 0
    echo_chamber_detected: int = 0
    circuit_breaker_trips: int = 0
    budget_exhausted_count: int = 0

    # Metricas de comunicacion
    messages_sent: int = 0
    messages_failed: int = 0
    avg_hops_per_task: list[int] = field(default_factory=list)

    def record_agent_call(
        self,
        agent_name: str,
        latency_ms: float,
        tokens: int,
        success: bool,
    ):
        self.agent_latency_ms[agent_name].append(latency_ms)
        self.agent_token_usage[agent_name].append(tokens)
        if not success:
            self.agent_error_count[agent_name] += 1

    def dashboard(self) -> dict:
        """Genera datos para el dashboard de monitoreo."""

        def percentile(data: list[float], p: float) -> float:
            if not data:
                return 0.0
            sorted_data = sorted(data)
            idx = int(len(sorted_data) * p / 100)
            return sorted_data[min(idx, len(sorted_data) - 1)]

        agent_stats = {}
        for name in self.agent_latency_ms:
            latencies = self.agent_latency_ms[name]
            tokens = self.agent_token_usage[name]
            agent_stats[name] = {
                "calls": len(latencies),
                "latency_p50_ms": percentile(latencies, 50),
                "latency_p95_ms": percentile(latencies, 95),
                "latency_p99_ms": percentile(latencies, 99),
                "avg_tokens": (
                    sum(tokens) / len(tokens) if tokens else 0
                ),
                "errors": self.agent_error_count[name],
                "timeouts": self.agent_timeout_count[name],
                "error_rate": (
                    self.agent_error_count[name] / len(latencies)
                    if latencies else 0
                ),
            }

        success_rate = (
            self.successful_tasks / self.total_tasks
            if self.total_tasks > 0 else 0
        )

        return {
            "system": {
                "total_tasks": self.total_tasks,
                "success_rate": success_rate,
                "consensus_rate": (
                    self.consensus_reached / self.total_tasks
                    if self.total_tasks > 0 else 0
                ),
                "echo_chambers_detected": self.echo_chamber_detected,
                "circuit_breaker_trips": self.circuit_breaker_trips,
                "messages_failed_rate": (
                    self.messages_failed / self.messages_sent
                    if self.messages_sent > 0 else 0
                ),
            },
            "agents": agent_stats,
        }
```

---

## 11.7 Cuando NO usar multi-agente

Para cerrar el capitulo, una lista concreta de senales de que multi-agente no es la solucion:

1. **Tu agente unico no esta optimizado.** Antes de agregar mas agentes, asegurate de que tu agente unico tiene el mejor prompt posible, las herramientas correctas y el contexto adecuado. La mayoria de las veces, un mejor prompt supera a un sistema multi-agente mediocre.

2. **No tienes observabilidad.** Si no puedes depurar un agente, no podras depurar cinco. Implementa tracing, logging y metricas para un solo agente antes de escalar.

3. **Tu latencia es critica.** Si necesitas respuestas en menos de 2 segundos, multi-agente probablemente no es viable. Cada hop agrega 0.5-3 segundos.

4. **Tus margenes son estrechos.** Multi-agente multiplica costos 3-15x. Si tu caso de uso tiene margenes de $0.10 por consulta, no puedes pagar $0.75 por debate.

5. **Quieres parecer sofisticado.** "7 agentes con debate adversarial" suena impresionante pero es deuda tecnica disfrazada de arquitectura si un solo agente resuelve el problema.

6. **Todos tus agentes usan el mismo modelo.** La diversidad de modelos es lo que hace valioso al multi-agente. Cinco instancias de GPT-4 no son mas confiables que una.

La regla de oro: **empieza con un solo agente, mide sus limitaciones, y escala a multi-agente solo cuando tengas evidencia concreta de que un solo agente no es suficiente.**

---

## Takeaway del capitulo

Multi-agente es poderoso pero peligroso. Empieza con un solo agente, escala cuando sea necesario, y cuando lo hagas, trata el consenso entre agentes con el mismo rigor que la teoria de sistemas distribuidos trata el consenso entre nodos.

Las topologias (centralizada, descentralizada, jerarquica) determinan las propiedades fundamentales del sistema. No hay topologia universalmente mejor; la eleccion depende de tu problema.

Los patrones de orquestacion (pipeline, scatter-gather, voting) tienen trade-offs claros en latencia, costo y robustez. El pipeline es simple pero secuencial; scatter-gather aprovecha el paralelismo; voting implementa consenso pero multiplica costos.

El consenso entre agentes LLM es diferente del consenso clasico: las alucinaciones son un problema de correlacion, no de adversarialidad. La diversidad de modelos es la defensa real, no la redundancia numerica.

La observabilidad multi-agente requiere tracing distribuido, metricas por agente y por sistema, y deteccion de patrones patologicos como camaras de eco y deadlocks.

---

## Referencias

- Lamport, L., Shostak, R., Pease, M. "The Byzantine Generals Problem." ACM Transactions on Programming Languages and Systems, 4(3), 1982.
- Anthropic. "Building Effective Agents." anthropic.com/research, diciembre 2024.
- Irving, G., Christiano, P., Amodei, D. "AI Safety via Debate." arXiv:1805.00899, 2018.
- Du, Y., et al. "Improving Factuality and Reasoning in Language Models through Multiagent Debate." arXiv:2305.14325, 2023.
- Sun, Y., et al. "IBGP: Imperfect Byzantine Generals Problem for Multi-Agent Systems." arXiv, 2024.
- Li, et al. "CP-WBFT: A Confidence Probe-Based Weighted Byzantine Fault Tolerant Consensus Mechanism." arXiv, 2025.
- Jo, Y. "Byzantine-Robust Decentralized Coordination of LLM Agents." arXiv:2507.14928, 2025.
- Zhang, et al. "BlockAgents: Proof-of-Thought Consensus for Multi-Agent Systems." arXiv, 2024.
- OpenTelemetry. "AI Agent Observability - Evolving Standards and Best Practices." opentelemetry.io/blog, 2025.
- "The Orchestration of Multi-Agent Systems: Architectures, Protocols, and Enterprise Adoption." arXiv:2601.13671, enero 2026.
- Park, J. S., et al. "Generative Agents: Interactive Simulacra of Human Behavior." arXiv:2304.03442, 2023.
- Dibia, V. "Designing Multi-Agent Systems: Principles, Patterns, and Implementation." 2025.
