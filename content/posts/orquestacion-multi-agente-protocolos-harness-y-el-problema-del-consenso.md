---
title: "Orquestación multi-agente: protocolos, harness y el problema del consenso"
date: 2026-04-11
author: "Héctor Patricio"
tags: ['agentes', 'multi-agente', 'inteligencia-artificial', 'llm', 'arquitectura', 'sistemas-distribuidos', 'consenso', 'orquestación', 'diseño-de-software']
description: "Exploramos las topologías, protocolos de comunicación y patrones de error en sistemas multi-agente, conectando con la teoría de sistemas distribuidos y el problema del consenso bizantino."
featuredImage: ""
draft: true
---

En enero de 2025, un sistema multi-agente de trading desplegado por una fintech de Singapur perdió $2.3 millones en 47 minutos. El agente de análisis de mercado alucinó una tendencia alcista inexistente, el agente de validación --entrenado con el mismo modelo base-- confirmó la tendencia, y el agente ejecutor operó con total confianza. Tres agentes, cero disidencia, pérdida total. El postmortem reveló algo que la teoría de sistemas distribuidos lleva décadas estudiando: el consenso entre nodos no confiables es un problema fundamentalmente difícil.

Este artículo se enfoca en lo que emerge cuando múltiples agentes interactúan: los patrones de fallo que no existen con un solo agente, las topologías que determinan cómo se propagan errores y decisiones, y los mecanismos de consenso que pueden (o no) protegerte cuando un agente alucina con convicción.

## Antes de saltar: cuándo un solo agente es suficiente

La tentación de construir un sistema multi-agente es fuerte, pero en la práctica, la mayoría de los equipos que empiezan con multi-agente terminan simplificando a un solo agente con mejor prompting. Como recomienda Anthropic en su guía "Building Effective Agents": empieza simple.

Un solo agente bien diseñado es preferible cuando:

- **El problema cabe en una sola ventana de contexto.** Si un agente puede ver toda la información relevante y producir una buena respuesta, agregar más agentes solo añade latencia, costo y puntos de fallo.
- **No tienes observabilidad resuelta para un solo agente.** Si no puedes depurar un agente, no podrás depurar cinco. La observabilidad multi-agente es órdenes de magnitud más difícil.
- **El costo multiplicado no se justifica.** Cada agente adicional multiplica el consumo de tokens. Un sistema de 5 agentes con 3 rondas de debate puede costar 10-15x más que una sola llamada. Si tu caso de uso tiene márgenes estrechos, multi-agente puede ser prohibitivo.
- **La latencia es crítica.** Cada "hop" entre agentes vía API de LLM añade 0.5-3 segundos. Un sistema con 5 hops tiene 2.5-15 segundos solo de latencia de comunicación.
- **Quieres parecer sofisticado.** "Usamos 7 agentes con debate adversarial" suena impresionante en una presentación, pero si un solo agente con un buen prompt resuelve el problema, la complejidad adicional es deuda técnica disfrazada de arquitectura.

La regla de producción es: **escala a multi-agente solo cuando puedas demostrar que un solo agente no puede resolver el problema.** Dicho esto, hay casos donde multi-agente es genuinamente necesario, y el resto de este artículo se enfoca en cómo hacerlo bien.

## Cuando un solo agente no basta

Piensa en el desarrollo de software como analogía. Un programador junior puede resolver tareas bien definidas: implementar una función, corregir un bug, escribir un test. Pero para un proyecto complejo necesitas un equipo: alguien que se enfoque en la arquitectura, otro en la seguridad, otro en el rendimiento, un líder técnico que coordine. Ninguno de ellos podría, razonablemente, hacer el trabajo de todos los demás con la misma calidad.

Con los agentes de IA pasa algo similar. Un solo agente generalista puede manejar tareas simples, pero cuando el problema involucra múltiples dominios de conocimiento, razonamiento profundo en paralelo o verificación cruzada, un sistema multi-agente ofrece ventajas claras:

- **Especialización**: cada agente se entrena o se configura con prompts especializados para un dominio específico.
- **Paralelismo**: múltiples agentes pueden trabajar simultáneamente, reduciendo la latencia total. Cada agente con su propia ventana de contexto opera como un recurso independiente.
- **Verificación cruzada**: agentes independientes pueden validar las conclusiones de otros, reduciendo alucinaciones.
- **Robustez**: si un agente falla, los demás pueden compensar.

Pero estas ventajas no son gratuitas. Un sistema multi-agente introduce complejidad en la comunicación, costos multiplicados de tokens, nuevos modos de fallo y, fundamentalmente, el problema de cómo lograr que agentes independientes lleguen a conclusiones coherentes entre sí.

## Topologías de sistemas multi-agente

La forma en que organizas a tus agentes determina las propiedades del sistema completo: su latencia, su tolerancia a fallos, su costo y su complejidad. Veamos las topologías principales, cada una con trade-offs distintos.

### Centralizado (orquestador)

Un agente central recibe la tarea, la descompone, la delega a agentes especializados, recopila los resultados y sintetiza la respuesta final.

```python
class Orchestrator:
    def __init__(self, agents: list[Agent]):
        self.agents = {a.specialty: a for a in agents}

    async def process(self, task: str) -> str:
        # Paso 1: descomponer la tarea
        subtasks = await self.decompose(task)

        # Paso 2: delegar a agentes especializados
        results = {}
        for subtask in subtasks:
            agent = self.agents[subtask.domain]
            results[subtask.id] = await agent.execute(subtask)

        # Paso 3: sintetizar resultados
        return await self.synthesize(results)
```

**Ventajas**: simplicidad conceptual, control centralizado, fácil de depurar. **Desventajas**: punto único de fallo, cuello de botella en el orquestador, la latencia es la suma de todas las subtareas si se ejecutan secuencialmente.

### Descentralizado (peer-to-peer)

Los agentes se comunican directamente entre sí, sin un coordinador central. Cada agente decide a quién consultar basándose en el problema que enfrenta.

```python
class PeerAgent:
    def __init__(self, name: str, peers: dict[str, "PeerAgent"]):
        self.name = name
        self.peers = peers

    async def execute(self, task: str) -> str:
        # Intento resolver solo
        result = await self.try_solve(task)

        if result.confidence < 0.7:
            # Consulto a un par especializado
            peer = self.select_peer(task)
            peer_result = await peer.execute(task)
            result = await self.merge(result, peer_result)

        return result
```

**Ventajas**: sin punto único de fallo, escalable horizontalmente. **Desventajas**: difícil de depurar, riesgo de ciclos infinitos (agente A consulta a B, B consulta a A), explosión de mensajes. Es como un equipo sin líder: funciona bien con gente experimentada, pero se vuelve caótico rápidamente.

### Jerárquico (capas de supervisión)

Combina lo mejor de ambos mundos: agentes organizados en niveles, donde supervisores de alto nivel coordinan a grupos de agentes especializados.

```python
class HierarchicalSystem:
    def __init__(self):
        self.supervisor = SupervisorAgent()
        self.team_leads = {
            "security": TeamLead(agents=[VulnScanner(), CodeAuditor()]),
            "performance": TeamLead(agents=[Profiler(), Optimizer()]),
        }

    async def analyze(self, codebase: str) -> Report:
        plan = await self.supervisor.create_plan(codebase)
        team_reports = {}
        for team, tasks in plan.items():
            team_reports[team] = await self.team_leads[team].execute(tasks)
        return await self.supervisor.consolidate(team_reports)
```

Esta topología se parece a la estructura organizacional de una empresa de software. La clave es que cada capa de supervisión debe agregar valor (filtrar, priorizar, resolver conflictos), no solo pasar mensajes. Si tus supervisores son proxies transparentes, estás añadiendo latencia y costo sin ganar resiliencia.

### Pipeline (secuencial)

Los agentes se organizan en una cadena donde la salida de uno es la entrada del siguiente.

```python
class AgentPipeline:
    def __init__(self, stages: list[Agent]):
        self.stages = stages

    async def process(self, input_data: str) -> str:
        current = input_data
        for stage in self.stages:
            current = await stage.process(current)
        return current

# Ejemplo: pipeline de análisis de texto
pipeline = AgentPipeline([
    ExtractionAgent(),      # Extrae entidades
    ClassificationAgent(),  # Clasifica intención
    ResponseAgent(),        # Genera respuesta
    QualityAgent(),         # Valida calidad
])
```

**Ventajas**: fácil de razonar, cada agente tiene una responsabilidad clara (alta cohesión). **Desventajas**: la latencia es la suma de todas las etapas, un fallo en cualquier etapa detiene todo el pipeline, no aprovecha el paralelismo.

### Fan-out/fan-in (paralelo)

Una tarea se distribuye a múltiples agentes simultáneamente (fan-out), y sus resultados se agregan (fan-in). Es la topología ideal cuando necesitas múltiples perspectivas sobre el mismo problema.

```python
import asyncio

class FanOutFanIn:
    def __init__(self, agents: list[Agent], aggregator: Aggregator):
        self.agents = agents
        self.aggregator = aggregator

    async def process(self, task: str) -> str:
        # Fan-out: todos los agentes trabajan en paralelo
        coroutines = [agent.execute(task) for agent in self.agents]
        results = await asyncio.gather(*coroutines, return_exceptions=True)

        # Filtrar fallos
        valid_results = [r for r in results if not isinstance(r, Exception)]

        # Fan-in: agregar resultados
        return await self.aggregator.aggregate(valid_results)
```

La latencia de esta topología depende de si el paralelismo es real o aparente. Si los agentes llaman a diferentes APIs de modelos, cada llamada se ejecuta en un servidor diferente y la latencia total es la del agente más lento. Pero si todos usan el mismo proveedor, los *rate limits* pueden serializar las llamadas, haciendo la latencia efectiva similar a la de un pipeline.

### Eligiendo la topología correcta

No hay una topología universalmente mejor. La elección depende de tu problema:

| Topología | Latencia | Tolerancia a fallos | Complejidad | Mejor para |
|-----------|----------|---------------------|-------------|------------|
| Centralizada | Media | Baja | Baja | Tareas con descomposición clara |
| Descentralizada | Variable | Alta | Alta | Sistemas adaptativos |
| Jerárquica | Media-Alta | Media | Media | Organizaciones grandes |
| Pipeline | Alta | Baja | Baja | Procesamiento secuencial |
| Fan-out/fan-in | Baja* | Alta | Media | Validación cruzada |

## El problema del consenso aplicado a agentes

Aquí es donde la teoría de sistemas distribuidos se vuelve directamente relevante. El **problema del consenso** es uno de los problemas fundamentales en computación distribuida: ¿cómo logran múltiples procesos independientes ponerse de acuerdo en un valor, incluso cuando algunos de ellos pueden fallar?

### El problema de los generales bizantinos y los agentes que alucinan

En 1982, Leslie Lamport, Robert Shostak y Marshall Pease formularon el **problema de los generales bizantinos**: varios generales deben coordinar un ataque, pero algunos de ellos pueden ser traidores que envían mensajes contradictorios. La pregunta es: ¿pueden los generales leales llegar a un acuerdo a pesar de los traidores?

La analogía con agentes de IA es tentadora: reemplaza "traidores" por "agentes que alucinan". Pero hay una diferencia importante. Un nodo bizantino es el peor caso posible: puede enviar mensajes *arbitrarios y diferentes* a cada receptor, comportándose de forma adversarial óptima. Un agente que alucina es diferente: típicamente produce la *misma* respuesta incorrecta para todos los que le preguntan, con formato correcto y argumentos convincentes. Es más parecido a un fallo de tipo "crash con respuesta incorrecta" que a un fallo bizantino completo.

El resultado clásico de Lamport dice que para tolerar `f` nodos bizantinos, necesitas al menos `3f + 1` nodos en total. Pero este resultado no es directamente aplicable a agentes que alucinan, porque resuelve un problema diferente: la tolerancia a nodos *adversariales* que envían mensajes distintos a cada receptor. Las alucinaciones de LLMs son un problema de *correlación*, no de adversarialidad. Tres instancias del mismo modelo comparten los mismos datos de entrenamiento, los mismos sesgos y los mismos puntos ciegos, así que tienden a alucinar de la misma manera. Agregar más instancias del mismo modelo no ayuda: cinco instancias de GPT-4 que coinciden en una respuesta incorrecta no son más confiables que tres.

Lo que realmente necesitas es **diversidad de modelos**, que es un requisito ortogonal al número de agentes. Tres agentes con modelos distintos (Claude, GPT-4, Gemini) son más robustos que cinco instancias del mismo modelo, porque sus errores están menos correlacionados. El resultado de 3f+1 no te dice cuántos agentes necesitas; te dice que la redundancia numérica sin diversidad es teatro de seguridad.

### Protocolos de votación

La forma más directa de implementar consenso entre agentes es mediante votación. Veamos las variantes principales.

**Majority voting (votación mayoritaria)**

Cada agente produce una respuesta, y se elige la que más agentes produjeron. Simple, pero con problemas: ¿cómo defines "la misma respuesta" cuando las respuestas son texto libre?

```python
from collections import Counter

class MajorityVoting:
    def __init__(self, agents: list[Agent], similarity_threshold: float = 0.85):
        self.agents = agents
        self.similarity_threshold = similarity_threshold

    async def decide(self, task: str) -> str:
        responses = await asyncio.gather(
            *[agent.execute(task) for agent in self.agents]
        )

        # Agrupar respuestas similares usando embeddings
        clusters = self.cluster_by_similarity(responses)

        # Elegir el cluster más grande
        largest_cluster = max(clusters, key=len)
        # Retornar la respuesta con mayor confianza del cluster ganador
        return self.select_best(largest_cluster)

    def cluster_by_similarity(self, responses: list[str]) -> list[list[str]]:
        """Agrupa respuestas usando similitud semántica con embeddings."""
        embeddings = [get_embedding(r) for r in responses]
        clusters = []
        used = set()

        for i, emb_i in enumerate(embeddings):
            if i in used:
                continue
            cluster = [responses[i]]
            used.add(i)
            for j, emb_j in enumerate(embeddings):
                if j not in used and cosine_similarity(emb_i, emb_j) > self.similarity_threshold:
                    cluster.append(responses[j])
                    used.add(j)
            clusters.append(cluster)

        return clusters
```

El truco está en la función `cluster_by_similarity`: no puedes comparar respuestas de texto con igualdad exacta. Necesitas similitud semántica, lo que introduce otro modelo (de embeddings) y otro punto de fallo.

**Weighted voting (votación ponderada)**

No todos los agentes son igual de confiables. Un agente especializado en seguridad debería tener más peso en cuestiones de seguridad que un agente generalista.

```python
class WeightedVoting:
    def __init__(self, agents: list[Agent], weights: dict[str, float]):
        self.agents = agents
        self.weights = weights  # peso por agente según dominio

    async def decide(self, task: str, domain: str) -> str:
        responses = []
        for agent in self.agents:
            result = await agent.execute(task)
            weight = self.weights.get(f"{agent.name}:{domain}", 1.0)
            responses.append((result, weight))

        # Agrupar y sumar pesos
        clusters = self.cluster_weighted(responses)
        best_cluster = max(clusters, key=lambda c: sum(w for _, w in c))
        return self.select_best([r for r, _ in best_cluster])
```

**Debate adversarial**

En lugar de votar, los agentes debaten entre sí. Un agente propone una respuesta, otro la critica, y el primero defiende o corrige. Este patrón es particularmente efectivo para reducir alucinaciones porque fuerza al agente a justificar sus afirmaciones.

```python
class AdversarialDebate:
    def __init__(self, proposer: Agent, critic: Agent, judge: Agent, max_rounds: int = 3):
        self.proposer = proposer
        self.critic = critic
        self.judge = judge
        self.max_rounds = max_rounds

    async def debate(self, task: str) -> str:
        proposal = await self.proposer.execute(task)
        history = [{"role": "proposer", "content": proposal}]

        for round_num in range(self.max_rounds):
            # El crítico ataca
            critique = await self.critic.critique(
                task=task,
                proposal=proposal,
                history=history
            )
            history.append({"role": "critic", "content": critique})

            # Si el crítico no encuentra problemas, terminamos
            if critique.no_issues_found:
                break

            # El proponente defiende o corrige
            proposal = await self.proposer.defend_or_revise(
                task=task,
                critique=critique,
                history=history
            )
            history.append({"role": "proposer", "content": proposal})

        # Un juez independiente evalúa el debate completo
        return await self.judge.evaluate(task, history)
```

La investigación de Irving et al. (2018) en "AI Safety via Debate" mostró que el debate adversarial puede ayudar a alinear sistemas de IA, y el trabajo más reciente de Du et al. (2023) en "Improving Factuality and Reasoning in Language Models through Multiagent Debate" confirmó que este patrón mejora la factualidad de las respuestas entre un 10% y un 20% en benchmarks estándar.

El costo, por supuesto, es que cada ronda de debate multiplica el consumo de tokens. Un debate de 3 rondas con 3 agentes puede consumir 10 veces más tokens que una sola llamada.

## Comunicación inter-agente

¿Cómo se hablan los agentes entre sí? En el [artículo sobre protocolos de comunicación](/posts/el-protocolo-que-falta-comunicacion-entre-agentes-de-ia/) exploramos MCP, A2A y handoffs en detalle. Aquí nos enfocamos en lo que importa específicamente para orquestación multi-agente: cómo el mecanismo de comunicación afecta la topología, el costo y los modos de fallo del sistema.

### El mecanismo de comunicación determina la topología

MCP (agente-herramienta) favorece topologías centralizadas: un orquestador que consume herramientas. A2A (agente-agente) habilita topologías descentralizadas y jerárquicas. Los handoffs de OpenAI son esencialmente transferencias secuenciales, ideales para pipelines.

```python
class HandoffProtocol:
    def __init__(self, agents: dict[str, Agent]):
        self.agents = agents

    async def execute_with_handoffs(self, task: str, initial_agent: str) -> str:
        current_agent = initial_agent
        context = {"original_task": task, "history": []}

        while True:
            agent = self.agents[current_agent]
            result = await agent.execute(task, context)

            if result.handoff_to:
                # El agente decidió transferir a otro
                context["history"].append({
                    "agent": current_agent,
                    "partial_result": result.partial,
                    "reason": result.handoff_reason
                })
                current_agent = result.handoff_to
            else:
                return result.final_answer
```

### Message passing vs shared state

Hay dos paradigmas fundamentales para la comunicación entre agentes, y reflejan un debate clásico en sistemas distribuidos:

**Message passing**: Los agentes se envían mensajes explícitos. Cada agente tiene su propio estado interno y solo comparte lo que decide compartir. Es más seguro (menos *race conditions*), pero puede ser ineficiente si los agentes necesitan mucho contexto compartido.

**Shared state**: Los agentes leen y escriben en un espacio de estado compartido (una base de datos, un documento compartido, un grafo de conocimiento). Es más eficiente para compartir grandes cantidades de contexto, pero introduce problemas de concurrencia: ¿qué pasa si dos agentes modifican el mismo dato al mismo tiempo?

```python
# Message passing: cada agente recibe y envía mensajes explícitos
class MessagePassingAgent:
    async def process(self, message: AgentMessage) -> AgentMessage:
        result = await self.reason(message.content, message.context)
        return AgentMessage(
            sender=self.name,
            receiver=message.reply_to,
            content=result,
            context=message.context  # pasa solo el contexto necesario
        )

# Shared state: agentes leen/escriben en un estado compartido
class SharedStateAgent:
    def __init__(self, shared_store: SharedStore):
        self.store = shared_store

    async def process(self, task_id: str):
        # Lee el estado actual
        state = await self.store.read(task_id)
        # Razona sobre él
        result = await self.reason(state)
        # Escribe su contribución
        await self.store.write(task_id, self.name, result)
```

En sistemas multi-agente con LLMs, el *shared state* suele implementarse como un documento o artefacto compartido que los agentes van enriqueciendo. LangGraph, por ejemplo, usa un grafo de estado compartido donde cada nodo (agente) lee y modifica el estado global.

### El costo de la comunicación: tokens como moneda

Cada mensaje entre agentes cuesta tokens. Y los tokens cuestan dinero. Esto introduce un *trade-off* que no existe en sistemas distribuidos tradicionales donde la comunicación es prácticamente gratuita.

Considera un sistema con 5 agentes que se comunican en un debate de 3 rondas. Un cálculo ingenuo cuenta solo los mensajes del debate: 5 agentes x (2,000 tokens entrada + 500 salida) x 3 rondas = 37,500 tokens. Pero este cálculo subestima el costo real por un factor de 3-5x, porque omite componentes que se repiten en cada llamada:

- **System prompt de cada agente**: 500-2,000 tokens que se envían en *cada* llamada.
- **Definiciones de herramientas**: 100-500 tokens por herramienta (el "tool tax" que discutimos en el [artículo sobre ventana de contexto](/posts/la-ventana-de-contexto-como-recurso-escaso/)).
- **Contexto acumulado**: en cada ronda, el historial del debate crece. La tercera ronda incluye los mensajes de las dos primeras.

Un cálculo más realista para este ejemplo, con precios de 2026 (modelos como Claude claude-sonnet-4-20250514 o GPT-4o), pone el costo entre $0.40 y $0.75 por debate, no $0.15. A 10,000 consultas diarias, eso es $4,000-$7,500 al día solo en comunicación inter-agente. La serialización y deserialización de los mensajes importa: un formato verboso multiplica estos costos.

```python
# MAL: serialización verbosa que desperdicia tokens
verbose_message = {
    "message_type": "analysis_result",
    "sender_agent_identifier": "security_analysis_agent_v2",
    "receiver_agent_identifier": "orchestrator_main_agent",
    "timestamp_utc": "2026-03-15T10:30:00Z",
    "analysis_result_payload": {
        "detailed_description": "Se encontró una vulnerabilidad de inyección SQL...",
        # ... campos innecesarios
    }
}

# BIEN: serialización compacta que ahorra tokens
compact_message = {
    "from": "security",
    "type": "vuln",
    "severity": "high",
    "finding": "SQL injection en endpoint /api/users, parámetro 'id' sin sanitizar",
    "fix": "Usar consultas parametrizadas"
}
```

Esta optimización puede parecer trivial, pero a escala la diferencia importa. Los tokenizers BPE comprimen bastante bien las claves repetitivas de JSON (claves como `"message_type"` se tokenizan en 2-3 tokens), así que el ahorro real en tokens es menor que la diferencia en caracteres. El porcentaje exacto depende del tokenizer y del modelo; mide el tuyo con el tokenizer correspondiente (tiktoken para OpenAI, el tokenizer de Anthropic para Claude) en lugar de asumir un número fijo. En un sistema que procesa miles de consultas diarias, incluso un ahorro modesto se acumula.

## El harness multi-agente

El [artículo sobre Agent Harness](/posts/agent-harness-el-arnes-que-controla-a-tu-agente-de-ia/) cubre los fundamentos del arnés para un solo agente: la infraestructura que envuelve a un agente individual para controlarlo, monitorearlo y limitarlo. El harness multi-agente *extiende* ese concepto con responsabilidades de coordinación que no existen cuando supervisas un solo agente: distribución de presupuesto entre agentes, detección de interacciones patológicas y tracing de las cadenas de comunicación. Cada agente individual sigue necesitando su propio harness (sandboxing, rate limiting, circuit breakers); el harness multi-agente se sitúa en la capa superior, coordinando a los harnesses individuales.

### Supervisión de múltiples agentes

```python
class MultiAgentHarness:
    def __init__(self, agents: list[Agent], config: HarnessConfig):
        self.agents = agents
        self.config = config
        self.tracer = DistributedTracer()
        self.budget_manager = BudgetManager(config.total_budget)

    async def execute(self, task: str) -> HarnessResult:
        trace_id = self.tracer.start_trace(task)
        results = {}

        for agent in self.agents:
            agent_budget = self.budget_manager.allocate(agent)
            try:
                with self.tracer.span(trace_id, agent.name):
                    result = await asyncio.wait_for(
                        agent.execute(task, budget=agent_budget),
                        timeout=self.config.timeout_per_agent
                    )
                    results[agent.name] = result
            except asyncio.TimeoutError:
                results[agent.name] = AgentResult.timeout(agent.name)
                self.tracer.log_event(trace_id, f"{agent.name} timeout")
            except Exception as e:
                results[agent.name] = AgentResult.error(agent.name, e)
                self.tracer.log_event(trace_id, f"{agent.name} error: {e}")

        self.tracer.end_trace(trace_id)
        return HarnessResult(results=results, trace_id=trace_id)
```

### Budget allocation: distribuyendo el presupuesto de tokens

El concepto de presupuesto de tokens aparece en el [artículo sobre el harness individual](/posts/agent-harness-el-arnes-que-controla-a-tu-agente-de-ia/) y en el [artículo sobre la ventana de contexto](/posts/la-ventana-de-contexto-como-recurso-escaso/). Aquí nos enfocamos en lo que es específico del caso multi-agente: la *distribución* del presupuesto entre agentes competidores.

No todos los agentes necesitan la misma cantidad de tokens. Un agente de clasificación rápida puede necesitar 500 tokens, mientras que un agente de análisis profundo puede necesitar 10,000. El harness debe distribuir el presupuesto de forma inteligente.

```python
class BudgetManager:
    def __init__(self, total_budget_tokens: int):
        self.total = total_budget_tokens
        self.spent = 0
        self.allocations = {}

    def allocate(self, agent: Agent) -> TokenBudget:
        """Asigna presupuesto según la prioridad y el historial del agente."""
        remaining = self.total - self.spent
        if remaining <= 0:
            raise BudgetExhaustedError("Presupuesto de tokens agotado")

        # Asignación proporcional al peso del agente
        agent_share = remaining * agent.priority_weight
        # Nunca menos del mínimo funcional
        allocated = max(agent_share, agent.min_tokens)
        # Nunca más del máximo configurado
        allocated = min(allocated, agent.max_tokens, remaining)

        self.allocations[agent.name] = allocated
        return TokenBudget(max_tokens=int(allocated), agent_name=agent.name)

    def report_usage(self, agent_name: str, tokens_used: int):
        """Registra el uso real para ajustar futuras asignaciones."""
        self.spent += tokens_used
```

Una estrategia más sofisticada es la asignación adaptativa: el harness observa cuántos tokens usa realmente cada agente y ajusta las asignaciones futuras. Si el agente de seguridad consistentemente usa solo el 30% de su presupuesto, el excedente se redistribuye.

### Timeout y fallback por agente

Cada agente debe tener su propio timeout y su propia estrategia de fallback. Un agente de análisis profundo puede tardar 30 segundos, pero un agente de clasificación que tarde más de 5 segundos probablemente está atascado.

```python
class AgentWithFallback:
    def __init__(self, primary: Agent, fallback: Agent, timeout: float):
        self.primary = primary
        self.fallback = fallback
        self.timeout = timeout

    async def execute(self, task: str) -> AgentResult:
        try:
            return await asyncio.wait_for(
                self.primary.execute(task),
                timeout=self.timeout
            )
        except (asyncio.TimeoutError, Exception) as e:
            # Fallback: puede ser un agente más simple,
            # un modelo más rápido, o una respuesta determinista
            return await self.fallback.execute(
                task,
                context=f"Primary agent failed: {e}"
            )
```

### Tracing distribuido

Cuando algo sale mal en un sistema multi-agente (y siempre sale algo mal), necesitas poder reconstruir qué pasó. El tracing distribuido, tomado directamente de la ingeniería de microservicios, es esencial.

Cada operación del sistema recibe un `trace_id` que la conecta con todas las operaciones relacionadas. Cada agente genera *spans* que registran cuándo empezó, cuándo terminó, cuántos tokens usó y qué decidió.

```python
class DistributedTracer:
    def __init__(self):
        self.traces = {}

    def start_trace(self, task: str) -> str:
        trace_id = generate_uuid()
        self.traces[trace_id] = {
            "task": task,
            "start_time": time.time(),
            "spans": [],
            "events": []
        }
        return trace_id

    @contextmanager
    def span(self, trace_id: str, agent_name: str):
        span_data = {
            "agent": agent_name,
            "start": time.time(),
            "tokens_in": 0,
            "tokens_out": 0
        }
        try:
            yield span_data
        finally:
            span_data["end"] = time.time()
            span_data["duration_ms"] = (span_data["end"] - span_data["start"]) * 1000
            self.traces[trace_id]["spans"].append(span_data)
```

## Patrones de error en sistemas multi-agente

Los sistemas multi-agente tienen modos de fallo que no existen en sistemas de un solo agente. Si estás familiarizado con los problemas de sistemas distribuidos, reconocerás varios viejos conocidos.

### Cascading failures: el efecto dominó

Un agente falla y su fallo provoca que otros agentes fallen. Esto ocurre cuando los agentes dependen de los resultados de otros para funcionar.

Imagina un sistema donde el agente de extracción de datos falla silenciosamente y retorna datos vacíos. El agente de análisis recibe datos vacíos, genera un análisis sin sentido, y el agente de reporte genera un reporte convincente pero completamente vacío. Cada agente en la cadena propaga y amplifica el error.

La solución es la **validación en cada frontera**: cada agente valida sus entradas antes de procesarlas y sus salidas antes de enviarlas.

```python
class ResilientAgent:
    async def execute(self, input_data: str) -> AgentResult:
        # Validar entrada
        if not self.validate_input(input_data):
            return AgentResult.error("Entrada inválida o insuficiente")

        result = await self.process(input_data)

        # Validar salida
        if not self.validate_output(result):
            return AgentResult.error("Salida no cumple criterios mínimos")

        return result

    def validate_input(self, data: str) -> bool:
        """Verifica que la entrada tenga el formato y contenido esperado."""
        if len(data.strip()) < 10:
            return False
        # Validaciones específicas del dominio
        return self.domain_validator.check(data)
```

### Echo chambers: la cámara de eco

Este es quizás el patrón de error más insidioso. Dos o más agentes se refuerzan mutuamente en una respuesta incorrecta. El agente A dice "la respuesta es X", el agente B ve que A dijo X y, influenciado por ese contexto, también dice X. Un tercer agente ve que A y B coinciden y confirma X. El sistema tiene "consenso"... pero está equivocado.

Este problema es un análogo directo del *groupthink* en equipos humanos, y es el patrón de error más peligroso en sistemas multi-agente porque se disfraza de robustez: "tres agentes coinciden, así que debe ser correcto". Pero la coincidencia no implica corrección cuando los sesgos están correlacionados.

La correlación de sesgos es el concepto clave aquí. Tres instancias de GPT-4 tienen los mismos datos de entrenamiento, las mismas asociaciones aprendidas y los mismos puntos ciegos. Si una instancia alucina que "el framework X fue deprecado en 2025", las otras dos probablemente confirmarán la alucinación porque comparten la misma distribución de probabilidades sobre ese hecho. La redundancia numérica sin diversidad de modelo es teatro de seguridad.

Estrategias de mitigación, en orden de efectividad:

1. **Independencia primero**: no compartas la respuesta de un agente con otro antes de que el segundo genere la suya. Este es el error más común y el más fácil de corregir.
2. **Diversidad de modelos**: usa modelos de diferentes proveedores (Claude, GPT-4, Gemini, Llama). No porque sean "mejores" o "peores", sino porque sus errores están menos correlacionados.
3. **Agente adversarial**: incluye un agente cuyo rol explícito sea encontrar problemas en lo que los demás dicen. Dale un prompt que lo incentive a disentir.

```python
class AntiEchoChamber:
    def __init__(self, agents: list[Agent], devils_advocate: Agent):
        self.agents = agents
        self.devils_advocate = devils_advocate

    async def decide(self, task: str) -> str:
        # Paso 1: cada agente responde INDEPENDIENTEMENTE
        responses = await asyncio.gather(
            *[agent.execute(task) for agent in self.agents]
        )

        # Paso 2: el abogado del diablo critica TODAS las respuestas
        critique = await self.devils_advocate.critique_all(
            task=task,
            responses=responses,
            instruction="Encuentra debilidades, suposiciones no verificadas "
                        "y posibles errores en CADA respuesta. Sé escéptico."
        )

        # Paso 3: los agentes revisan considerando la crítica
        revised = await asyncio.gather(
            *[agent.revise(task, responses[i], critique)
              for i, agent in enumerate(self.agents)]
        )

        return self.aggregate(revised)
```

### Race conditions: agentes compitiendo por el mismo recurso

Cuando dos agentes intentan modificar el mismo recurso simultáneamente, el resultado es impredecible. En un sistema multi-agente con *shared state*, esto es un riesgo real.

Imagina dos agentes que analizan el mismo archivo de código. El agente de seguridad quiere agregar validación de entrada, y el agente de rendimiento quiere eliminar una verificación que considera redundante. Si ambos escriben sus cambios en el estado compartido al mismo tiempo, uno sobrescribe al otro.

La solución clásica aplica: **locks**, **transacciones** o **CRDTs** (Conflict-free Replicated Data Types) para el estado compartido.

```python
class ConcurrencySafeStore:
    def __init__(self):
        self.state = {}
        self.lock = asyncio.Lock()

    async def update(self, key: str, agent_name: str, value: any):
        async with self.lock:
            if key not in self.state:
                self.state[key] = {"value": value, "contributors": [agent_name]}
            else:
                # Merge en lugar de sobrescribir
                current = self.state[key]
                current["value"] = self.merge(current["value"], value)
                current["contributors"].append(agent_name)
```

### Deadlocks: agentes que se esperan mutuamente

El agente A espera el resultado del agente B para continuar. El agente B espera el resultado del agente A. Ninguno avanza. Es el clásico *deadlock* de sistemas operativos, pero en un contexto nuevo.

En sistemas multi-agente, los deadlocks suelen ocurrir en topologías descentralizadas donde los agentes pueden consultarse mutuamente. La prevención es la misma que en sistemas operativos: **ordenamiento de recursos** (los agentes solo pueden consultar a agentes con un ID menor al suyo) o **detección y ruptura** (un watchdog detecta el deadlock y mata a uno de los agentes).

```python
class DeadlockDetector:
    def __init__(self, timeout: float = 30.0):
        self.waiting_for = {}  # agent -> agent que espera
        self.timeout = timeout

    def register_wait(self, waiter: str, waiting_for: str):
        self.waiting_for[waiter] = waiting_for
        # Detectar ciclo
        if self.has_cycle(waiter):
            raise DeadlockDetectedError(
                f"Ciclo detectado: {self.trace_cycle(waiter)}"
            )

    def unregister_wait(self, waiter: str):
        """Limpia la espera cuando un agente completa o falla."""
        self.waiting_for.pop(waiter, None)

    def has_cycle(self, start: str) -> bool:
        visited = set()
        current = start
        while current in self.waiting_for:
            if current in visited:
                return True
            visited.add(current)
            current = self.waiting_for[current]
        return False
```

En la práctica, los deadlocks entre agentes LLM rara vez se manifiestan como ciclos de espera detectables con un grafo. Lo más común es que un agente "esperando" a otro simplemente tenga una request HTTP pendiente que eventualmente hace timeout. Por eso, la primera línea de defensa contra deadlocks en producción son **timeouts agresivos** por agente (como los que implementamos en la sección anterior con `asyncio.wait_for`), no la detección de ciclos. El `DeadlockDetector` de arriba es útil como segunda línea de defensa en topologías descentralizadas donde los agentes se consultan mutuamente, pero no sustituye a los timeouts.

### Observabilidad: depurando lo que no puedes ver

Depurar un sistema multi-agente es órdenes de magnitud más difícil que depurar un solo agente. Cuando algo sale mal, necesitas responder: qué agente falló, qué vio cada agente, cómo interactuaron las respuestas, y dónde se introdujo el error.

El tracing distribuido que mostramos en la sección del harness es el punto de partida, pero en producción necesitas más:

- **Correlation IDs**: cada request del usuario genera un ID que se propaga a través de todos los agentes y sus sub-llamadas. Sin esto, reconstruir una cadena de fallos es imposible.
- **Logging estructurado con `agent_id`**: cada línea de log incluye el nombre del agente, el trace ID y el paso del flujo. Esto permite filtrar por agente en herramientas como Elasticsearch o Datadog.
- **Replay de conversaciones**: la capacidad de reproducir exactamente lo que cada agente vio y respondió es invaluable para diagnosticar cámaras de eco y fallos en cascada.
- **Métricas por agente**: latencia (P50, P95, P99), tokens consumidos, tasa de error y costo por request, desglosados por agente individual.

Herramientas como LangSmith, Langfuse y Arize Phoenix ofrecen trazas multi-agente con visualización de las cadenas de llamadas. Integrarlas desde el principio ahorra semanas de depuración después.

## Caso de estudio: sistema multi-agente para análisis de código

Pongamos todo junto con un ejemplo concreto. Vamos a diseñar un sistema multi-agente que analiza una base de código desde múltiples perspectivas: seguridad, rendimiento, estilo y mantenibilidad.

### Arquitectura del sistema

Usaremos una topología fan-out/fan-in con un orquestador, porque necesitamos múltiples perspectivas independientes sobre el mismo código y luego una síntesis coherente.

```python
from dataclasses import dataclass
from enum import Enum
import asyncio

class AnalysisDomain(Enum):
    SECURITY = "security"
    PERFORMANCE = "performance"
    STYLE = "style"
    MAINTAINABILITY = "maintainability"

@dataclass
class Finding:
    domain: AnalysisDomain
    severity: str  # "critical", "warning", "info"
    file: str
    line: int
    description: str
    suggestion: str
    confidence: float

@dataclass
class AnalysisReport:
    findings: list[Finding]
    summary: str
    agent_name: str

class CodeAnalysisOrchestrator:
    def __init__(self):
        self.agents = {
            AnalysisDomain.SECURITY: SecurityAgent(model="claude-sonnet-4-20250514"),
            AnalysisDomain.PERFORMANCE: PerformanceAgent(model="gpt-4o"),
            AnalysisDomain.STYLE: StyleAgent(model="claude-haiku"),
            AnalysisDomain.MAINTAINABILITY: MaintainabilityAgent(model="gemini-2.5-pro"),
        }
        self.harness = MultiAgentHarness(
            agents=list(self.agents.values()),
            config=HarnessConfig(
                total_budget=50_000,  # tokens
                timeout_per_agent=30.0,  # segundos
            )
        )
        self.conflict_resolver = ConflictResolver()

    async def analyze(self, code: str, filename: str) -> FinalReport:
        # Fan-out: todos los agentes analizan en paralelo
        tasks = [
            self.analyze_with_agent(domain, agent, code, filename)
            for domain, agent in self.agents.items()
        ]
        reports = await asyncio.gather(*tasks, return_exceptions=True)

        # Filtrar errores
        valid_reports = [r for r in reports if isinstance(r, AnalysisReport)]
        failed = [r for r in reports if isinstance(r, Exception)]

        if failed:
            print(f"Advertencia: {len(failed)} agentes fallaron")

        # Detectar y resolver conflictos
        conflicts = self.conflict_resolver.detect(valid_reports)
        resolved = await self.conflict_resolver.resolve(conflicts)

        # Fan-in: sintetizar todos los hallazgos
        return await self.synthesize(valid_reports, resolved)

    async def analyze_with_agent(
        self, domain: AnalysisDomain, agent: Agent,
        code: str, filename: str
    ) -> AnalysisReport:
        budget = self.harness.budget_manager.allocate(agent)
        result = await asyncio.wait_for(
            agent.analyze(code, filename, budget=budget),
            timeout=self.harness.config.timeout_per_agent
        )
        return result
```

### Resolución de conflictos

El caso más interesante es cuando los agentes se contradicen. El agente de rendimiento dice "elimina esta verificación, es innecesaria y lenta", mientras que el agente de seguridad dice "esa verificación previene inyección SQL, es crítica". ¿Quién tiene razón?

```python
class ConflictResolver:
    def detect(self, reports: list[AnalysisReport]) -> list[Conflict]:
        """Detecta hallazgos contradictorios entre agentes."""
        conflicts = []
        findings_by_location = {}

        for report in reports:
            for finding in report.findings:
                key = (finding.file, finding.line)
                if key not in findings_by_location:
                    findings_by_location[key] = []
                findings_by_location[key].append(finding)

        for location, findings in findings_by_location.items():
            if len(findings) > 1:
                # Verificar si las sugerencias son contradictorias
                for i, f1 in enumerate(findings):
                    for f2 in findings[i+1:]:
                        if self.are_contradictory(f1, f2):
                            conflicts.append(Conflict(f1, f2, location))

        return conflicts

    async def resolve(self, conflicts: list[Conflict]) -> list[Resolution]:
        """Resuelve conflictos usando priorización por dominio."""
        resolutions = []
        for conflict in conflicts:
            # Regla: seguridad siempre gana sobre rendimiento
            priority_order = [
                AnalysisDomain.SECURITY,
                AnalysisDomain.MAINTAINABILITY,
                AnalysisDomain.STYLE,
                AnalysisDomain.PERFORMANCE,
            ]

            winner = min(
                [conflict.finding_a, conflict.finding_b],
                key=lambda f: priority_order.index(f.domain)
            )

            resolutions.append(Resolution(
                conflict=conflict,
                winner=winner,
                reason=f"{winner.domain.value} tiene prioridad"
            ))

        return resolutions
```

Observa la regla de priorización: **seguridad siempre gana sobre rendimiento**. Esta es una decisión de diseño explícita que el harness implementa con código determinista, no con un LLM. Las decisiones de política no deberían delegarse a agentes que podrían alucinar al respecto.

### Uso de diversidad de modelos

Nota que en nuestro sistema usamos cuatro modelos diferentes de tres proveedores distintos. Esto no es por capricho: es una estrategia deliberada contra las cámaras de eco. Claude, GPT-4 y Gemini tienen sesgos diferentes porque fueron entrenados con datos diferentes y con técnicas diferentes. Si los tres coinciden en un hallazgo, la probabilidad de que sea correcto es mucho mayor que si tres instancias del mismo modelo coinciden.

### Lecciones del caso de estudio

1. **El orquestador es código, no un LLM**: Las decisiones de coordinación (a quién llamar, cómo resolver conflictos, qué priorizar) se implementan con código determinista.
2. **La comunicación tiene estructura**: Los agentes no se envían texto libre; usan objetos estructurados (`Finding`, `AnalysisReport`) que pueden validarse.
3. **Los conflictos son inevitables**: En lugar de evitarlos, los detectamos explícitamente y los resolvemos con reglas claras.
4. **La diversidad es una feature**: Usar diferentes modelos no es una limitación, es una estrategia de resiliencia.

## Conclusión

Los sistemas multi-agente son, fundamentalmente, sistemas distribuidos donde los nodos son modelos de lenguaje. Esto significa que décadas de investigación en sistemas distribuidos, desde los generales bizantinos de Lamport hasta los CRDTs modernos, son directamente aplicables.

Pero hay diferencias importantes. Los nodos tradicionales fallan de formas detectables: se caen, no responden, envían basura binaria. Los agentes de IA fallan de formas sutiles: alucinan con confianza, generan respuestas plausibles pero incorrectas, se refuerzan mutuamente en errores. Esto hace que los protocolos de consenso clásicos no sean suficientes: necesitamos validación semántica, diversidad de modelos y debate adversarial.

La clave para construir sistemas multi-agente robustos está en tres principios:

1. **El harness es determinista**: la coordinación, el presupuesto y la resolución de conflictos se implementan con código convencional, no con LLMs.
2. **La comunicación es estructurada y económica**: mensajes tipados, compactos, validables.
3. **La diversidad es resiliencia**: diferentes modelos, diferentes prompts, diferentes perspectivas.

Si vienes del mundo de los microservicios, mucho de esto te resultará familiar. La diferencia es que en microservicios, un nodo que falla se cae o devuelve un error. Un agente que falla te devuelve una respuesta elocuente, bien formateada y completamente equivocada. Eso hace que los mecanismos de detección sean más importantes que los de recuperación.

### Referencias y fuentes clave

- **Lamport, L., Shostak, R., & Pease, M.** (1982). "The Byzantine Generals Problem". *ACM Transactions on Programming Languages and Systems*.
- **Irving, G., Christiano, P., & Amodei, D.** (2018). "AI Safety via Debate". *arXiv:1805.00899*.
- **Du, Y., Li, S., Torralba, A., Tenenbaum, J.B., & Mordatch, I.** (2023). "Improving Factuality and Reasoning in Language Models through Multiagent Debate". *arXiv:2305.14325*.
- **Anthropic.** (2024-2025). "Model Context Protocol (MCP) Specification". https://modelcontextprotocol.io
- **Google.** (2025). "Agent-to-Agent (A2A) Protocol". https://google.github.io/A2A
- **OpenAI.** (2025). "Agents SDK - Handoffs". https://openai.github.io/openai-agents-python
- **Shapley, L.S.** (1953). "A Value for N-Person Games". *Contributions to the Theory of Games*. Aplicable al concepto de weighted voting y la contribución de cada agente al resultado.
- **Fischer, M.J., Lynch, N.A., & Paterson, M.S.** (1985). "Impossibility of Distributed Consensus with One Faulty Process". *Journal of the ACM*. El resultado FLP sobre la imposibilidad del consenso en sistemas asincrónicos con fallos.
- **LangGraph Documentation.** (2025). Shared state y checkpointing para sistemas multi-agente.
- **Anthropic.** (2024). "Building Effective Agents". https://docs.anthropic.com/en/docs/build-with-claude/agentic-systems
- **Langfuse, LangSmith, Arize Phoenix.** Herramientas de tracing para sistemas con LLMs.
