# Capitulo 15: Herramientas y Frameworks -- El Mapa del Ecosistema

> "El framework no es la arquitectura. El framework es la infraestructura que soporta tu arquitectura. Elige el framework despues de definir la arquitectura, no antes."
>
> -- Harrison Chase, "Why You Should Outsource Your Agentic Infrastructure, But Own Your Cognitive Architecture" [2024]

---

En el capitulo anterior establecimos los principios de ingenieria para llevar agentes a produccion. Ahora toca responder una pregunta practica que todo equipo enfrenta al comenzar: que herramientas uso?

El ecosistema de frameworks para agentes de IA en 2026 es vasto y cambia rapido. Nuevos frameworks aparecen cada semana. Los existentes se fusionan, se renombran y pivotan. Elegir mal puede costarte meses de trabajo cuando el framework queda abandonado o toma una direccion incompatible con tus necesidades.

Este capitulo no es un tutorial de cada framework. Es una guia de decision. Para cada herramienta, respondemos tres preguntas: que resuelve, cuando usarla y cuando *no* usarla. Al final, proporcionamos criterios claros para la decision mas importante de todas: cuando usar un framework y cuando construir lo tuyo.

La distincion clave la articulo Harrison Chase: tu **infraestructura agentica** (persistencia, tracing, deployment) puede y debe delegarse a un framework. Tu **arquitectura cognitiva** (como tu agente razona, que herramientas usa, como decide) debes controlarla tu [Chase, 2024].

---

## 15.1 LangChain y LangGraph: la evolucion

### El arco de LangChain

LangChain fue el primer framework dominante para aplicaciones con LLMs, lanzado a finales de 2022. Su propuesta original era ser una "cadena" de componentes: conectar un LLM con herramientas, memoria y prompts de forma modular.

La critica principal fue que LangChain era demasiado abstracto. Envolvia operaciones simples en capas de abstraccion innecesarias. Un `llm.invoke("Hola")` se convertia en una cadena de clases con nombres como `RunnableSequence`, `RunnablePassthrough` y `RunnableLambda` que oscurecian lo que realmente estaba pasando. Era la antitesis de los "modulos profundos" de Ousterhout: mucha interfaz, poca sustancia.

Harrison Chase reconocio esto publicamente en su retrospectiva de tres anos: "Los mejores patrones estan mucho mas entendidos hoy" [Chase, 2025]. La respuesta de LangChain fue LangGraph.

### LangGraph: agentes como grafos

LangGraph redefinio la propuesta: en lugar de cadenas lineales, los agentes son **grafos de estado**. Cada nodo es una funcion que recibe y modifica un estado compartido. Las aristas definen transiciones, que pueden ser condicionales, ciclicas o paralelas.

```python
"""
Ejemplo conceptual de un agente con LangGraph.
Muestra la estructura de grafo de estado, no la implementacion completa.
"""

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class AgentState:
    """Estado compartido entre nodos del grafo.

    En LangGraph real, esto hereda de TypedDict o usa
    el sistema de anotaciones de LangGraph.
    """
    messages: list[dict] = field(default_factory=list)
    current_step: str = "start"
    tool_results: list[dict] = field(default_factory=list)
    should_continue: bool = True
    iterations: int = 0
    max_iterations: int = 10


# --- Nodos del grafo ---

def reason_node(state: AgentState) -> AgentState:
    """Nodo de razonamiento: el LLM decide que hacer."""
    # En produccion: llamada al LLM con el estado actual
    state.iterations += 1
    state.current_step = "reason"
    return state


def tool_node(state: AgentState) -> AgentState:
    """Nodo de herramientas: ejecuta la herramienta seleccionada."""
    # En produccion: ejecutar herramienta y agregar resultado
    state.current_step = "tool"
    return state


def respond_node(state: AgentState) -> AgentState:
    """Nodo de respuesta: genera la respuesta final."""
    state.current_step = "respond"
    state.should_continue = False
    return state


# --- Routing condicional ---

def should_use_tool(state: AgentState) -> Literal["tool", "respond"]:
    """Decide si necesita una herramienta o puede responder."""
    if state.iterations >= state.max_iterations:
        return "respond"
    # En produccion: analizar la salida del LLM
    # para determinar si pidio una herramienta
    return "respond"


# --- Definicion del grafo ---
# En LangGraph real:
#
# from langgraph.graph import StateGraph, END
#
# graph = StateGraph(AgentState)
# graph.add_node("reason", reason_node)
# graph.add_node("tool", tool_node)
# graph.add_node("respond", respond_node)
#
# graph.set_entry_point("reason")
# graph.add_conditional_edges("reason", should_use_tool)
# graph.add_edge("tool", "reason")  # Despues de tool, razona de nuevo
# graph.add_edge("respond", END)
#
# app = graph.compile()
```

### Capacidades de produccion

LangGraph Platform, generalmente disponible desde 2025, ofrece tres opciones de deployment:

- **Cloud (SaaS)**: deployment mas rapido, Langchain gestiona todo.
- **Hibrido**: plano de control SaaS, plano de datos en tu infraestructura (para datos sensibles).
- **Self-hosted**: toda la plataforma en tu infraestructura.

Funcionalidades clave para produccion:

- **Persistencia durable**: el estado del agente se guarda automaticamente en cada paso. Si la ejecucion falla, puede reanudarse donde quedo.
- **Human-in-the-loop**: capacidad de pausar la ejecucion, inspeccionar el estado, modificarlo y reanudar.
- **Memoria**: tanto memoria de trabajo (para el razonamiento en curso) como memoria persistente (entre sesiones).
- **Streaming**: transmision de resultados parciales al usuario mientras el agente trabaja.

### Cuando si, cuando no

**Usa LangGraph cuando:**
- Necesitas flujos complejos con ramificaciones y ciclos.
- Requieres persistencia de estado y human-in-the-loop.
- Tu equipo ya tiene experiencia con el ecosistema LangChain.
- Necesitas deployment gestionado (LangGraph Platform).

**No uses LangGraph cuando:**
- Tu agente es lineal (entrada -> LLM -> respuesta). Es sobreingenieria.
- Quieres entender exactamente que pasa en cada paso. La abstraccion del grafo puede oscurecer la logica.
- Tu agente es simple y las abstracciones de LangGraph anaden complejidad innecesaria. En ese caso, una llamada directa al API del LLM con un loop while es suficiente.

---

## 15.2 CrewAI: agentes como equipos

### El modelo mental

CrewAI modela agentes como miembros de un equipo humano. Cada agente tiene un **rol**, un **objetivo**, una **historia de fondo** (backstory) y un conjunto de **herramientas**. Los agentes se organizan en **crews** (equipos) que ejecutan **tareas** de forma secuencial o paralela.

El modelo es intuitivo para personas sin experiencia tecnica profunda: "tengo un investigador que busca informacion, un escritor que redacta el contenido, y un editor que lo revisa." CrewAI traduce esa descripcion a un sistema multi-agente funcional.

```python
"""
Estructura conceptual de CrewAI.
En produccion, usa la API real de CrewAI.
"""

from dataclasses import dataclass, field


@dataclass
class CrewAgent:
    """Un agente en CrewAI: rol + objetivo + herramientas."""
    role: str
    goal: str
    backstory: str
    tools: list[str] = field(default_factory=list)
    verbose: bool = True
    allow_delegation: bool = False  # Puede delegar a otros agentes?
    max_iterations: int = 15


@dataclass
class CrewTask:
    """Una tarea asignada a un agente."""
    description: str
    expected_output: str
    agent: CrewAgent
    context: list["CrewTask"] = field(default_factory=list)


# Ejemplo: equipo de investigacion
researcher = CrewAgent(
    role="Investigador Senior",
    goal="Encontrar informacion precisa y actualizada sobre el tema",
    backstory="Eres un investigador experto con 15 anos de experiencia "
              "en analisis de informacion tecnica.",
    tools=["web_search", "arxiv_search"],
)

writer = CrewAgent(
    role="Escritor Tecnico",
    goal="Redactar un articulo claro y bien estructurado",
    backstory="Eres un escritor tecnico que traduce conceptos complejos "
              "a lenguaje accesible sin perder precision.",
    tools=["text_editor"],
)

# Las tareas se ejecutan en secuencia:
# investigar -> escribir
research_task = CrewTask(
    description="Investiga las tendencias actuales en {topic}",
    expected_output="Un resumen de 500 palabras con fuentes",
    agent=researcher,
)

write_task = CrewTask(
    description="Escribe un articulo basado en la investigacion",
    expected_output="Un articulo de 1500 palabras",
    agent=writer,
    context=[research_task],  # Recibe el output de la investigacion
)
```

### Evolucion en 2026

CrewAI ha evolucionado significativamente:

- **CrewAI Flows**: arquitectura orientada a eventos para orquestacion enterprise, con control granular sobre cada paso.
- **Memoria con Qdrant Edge**: backend de almacenamiento vectorial para el sistema de memoria de los agentes.
- **CrewAI AMP** (Agent Management Platform): plataforma enterprise para gestionar la adopcion de agentes a escala, desde desarrollo hasta produccion.
- **Mas de 100,000 desarrolladores certificados** a traves de cursos en learn.crewai.com [CrewAI, 2026].

### Cuando si, cuando no

**Usa CrewAI cuando:**
- Necesitas multi-agente con roles diferenciados.
- Tu equipo prefiere un modelo mental intuitivo (roles, objetivos, tareas).
- Quieres un prototipo rapido de un sistema multi-agente.
- Necesitas integracion enterprise con la plataforma AMP.

**No uses CrewAI cuando:**
- Necesitas control granular sobre cada paso del razonamiento. CrewAI abstrae mucha logica interna.
- Tus flujos son complejos con ramificaciones dinamicas. LangGraph es mejor para grafos de estado.
- Quieres evitar dependencia en un framework relativamente joven cuyo API puede cambiar.

---

## 15.3 Microsoft Agent Framework: la convergencia enterprise

### De AutoGen y Semantic Kernel a Agent Framework

Microsoft mantuvo dos frameworks para agentes durante 2024-2025: **AutoGen** (enfocado en investigacion y multi-agente) y **Semantic Kernel** (enfocado en enterprise con integracion Azure). La confusion era predecible: cual usar?

En octubre de 2025, Microsoft anuncio la fusion: **Microsoft Agent Framework**, que combina las abstracciones de agentes de AutoGen con las capacidades enterprise de Semantic Kernel [Microsoft, 2025].

En febrero de 2026, el framework alcanzo el estatus de Release Candidate para Python y .NET, con API estable y todas las funcionalidades planeadas para la version 1.0 completas. El objetivo de GA (General Availability) es Q1 2026 [Microsoft, 2026].

### Que ofrece

- **Abstracciones de agentes simples** heredadas de AutoGen: crear agentes con pocas lineas de codigo.
- **Capacidades enterprise** de Semantic Kernel: gestion de sesiones con estado, type safety, middleware, telemetria.
- **Flujos de trabajo basados en grafos**: orquestacion explicita de multi-agente.
- **Soporte multi-lenguaje**: Python y .NET como ciudadanos de primera clase.
- **Integracion con Azure**: deployment, identidad, almacenamiento, observabilidad nativos.

```python
"""
Estructura conceptual de Microsoft Agent Framework.
Basado en la documentacion publica del Release Candidate.
"""

from dataclasses import dataclass
from typing import Protocol


class AgentRuntime(Protocol):
    """Runtime que gestiona el ciclo de vida de los agentes."""

    async def send_message(
        self, agent_id: str, message: dict
    ) -> dict: ...

    async def register_agent(
        self, agent_id: str, agent: "BaseAgent"
    ) -> None: ...


@dataclass
class BaseAgent:
    """Agente base en Microsoft Agent Framework.

    Combina la simplicidad de AutoGen con las capacidades
    enterprise de Semantic Kernel.
    """
    agent_id: str
    name: str
    instructions: str
    model: str = "gpt-4o"

    async def handle_message(
        self, message: dict, runtime: AgentRuntime
    ) -> dict:
        """Procesa un mensaje y retorna una respuesta.

        El runtime gestiona el estado de la sesion, telemetria
        y middleware automaticamente.
        """
        # En produccion: el framework gestiona la llamada al LLM,
        # tool calling, y gestion de estado.
        return {"content": "Respuesta del agente"}
```

### Cuando si, cuando no

**Usa Microsoft Agent Framework cuando:**
- Tu organizacion esta invertida en el ecosistema Azure/Microsoft.
- Necesitas soporte para .NET ademas de Python.
- Requieres integracion enterprise (identidad, gobernanza, compliance).
- Ya usas Semantic Kernel o AutoGen y quieres migrar al framework unificado.

**No uses Microsoft Agent Framework cuando:**
- No estas en el ecosistema Microsoft. Las ventajas enterprise son irrelevantes sin Azure.
- Necesitas un framework maduro hoy. Aunque el RC es estable, el ecosistema de comunidad es mas pequeno que LangGraph o CrewAI.
- Prefieres un ecosistema puramente open source sin inclinacion hacia un proveedor de cloud especifico.

---

## 15.4 DSPy: programacion declarativa de LLMs

### Un enfoque radicalmente diferente

DSPy (Stanford NLP Group) toma un enfoque fundamentalmente distinto a todos los demas frameworks: en lugar de escribir prompts, **programas con firmas declarativas** y dejas que el framework optimice los prompts automaticamente [Khattab et al., 2023].

La idea es poderosa: asi como un compilador optimiza codigo de alto nivel a instrucciones de maquina, DSPy "compila" especificaciones de alto nivel a prompts optimizados para el modelo y la tarea especificos.

```python
"""
Ejemplo conceptual de DSPy.
Muestra la filosofia de programacion declarativa, no la API exacta.
"""

from dataclasses import dataclass
from typing import Optional


# En DSPy real, esto se define con decoradores y firmas:
#
# class ClassifyTicket(dspy.Signature):
#     """Clasifica un ticket de soporte en categoria y prioridad."""
#     ticket_text: str = dspy.InputField()
#     category: str = dspy.OutputField()
#     priority: str = dspy.OutputField()
#
# classify = dspy.ChainOfThought(ClassifyTicket)
# result = classify(ticket_text="Mi servidor no responde")

# El punto clave: NO escribiste un prompt.
# DSPy genera y optimiza el prompt automaticamente.


@dataclass
class DSPySignature:
    """Representacion conceptual de una firma DSPy.

    La firma define QUE quieres (input -> output).
    DSPy decide COMO lograrlo (el prompt optimo).
    """
    name: str
    description: str
    input_fields: dict[str, str]   # nombre -> descripcion
    output_fields: dict[str, str]  # nombre -> descripcion


# Firma para clasificacion de tickets
ticket_classifier = DSPySignature(
    name="ClassifyTicket",
    description="Clasifica un ticket de soporte tecnico",
    input_fields={
        "ticket_text": "El texto del ticket del usuario",
    },
    output_fields={
        "category": "La categoria del problema (network, database, auth, other)",
        "priority": "La prioridad (low, medium, high, critical)",
    },
)


@dataclass
class DSPyModule:
    """Representacion conceptual de un modulo DSPy.

    Los modulos componen firmas con estrategias de razonamiento.
    """
    signature: DSPySignature
    strategy: str = "chain_of_thought"  # predict, chain_of_thought, react


@dataclass
class DSPyOptimizer:
    """El optimizador es lo que hace unico a DSPy.

    Toma un modulo + datos de entrenamiento y encuentra
    los mejores prompts/ejemplos automaticamente.
    """
    strategy: str  # "bootstrap_fewshot", "mipro", "better_together"
    metric: str    # Funcion de evaluacion
    num_trials: int = 50

    def optimize(self, module: DSPyModule, train_data: list) -> dict:
        """Optimiza el modulo con los datos de entrenamiento.

        Returns:
            Configuracion optimizada (prompts, ejemplos, etc.)
        """
        # DSPy prueba multiples combinaciones de:
        # - Instrucciones del prompt
        # - Ejemplos few-shot
        # - Estrategias de razonamiento
        # y selecciona la combinacion que maximiza la metrica.
        return {"optimized_prompt": "...", "few_shot_examples": []}
```

### El poder de la optimizacion automatica

Lo que distingue a DSPy es el concepto de **optimizadores** (antes llamados "teleprompters"). Un optimizador toma:

1. Un modulo DSPy (que define la tarea).
2. Un dataset de entrenamiento (ejemplos de input/output correctos).
3. Una metrica de evaluacion.

Y produce un prompt optimizado que maximiza la metrica. DSPy 3.1 (version actual en marzo 2026) incluye optimizadores como:

- **BootstrapFewShot**: selecciona los mejores ejemplos few-shot automaticamente.
- **MIPRO**: optimiza instrucciones y ejemplos de forma conjunta.
- **BetterTogether**: meta-optimizador que combina optimizacion de prompts con fine-tuning de pesos en secuencias configurables.

### Cuando si, cuando no

**Usa DSPy cuando:**
- Tienes datos de evaluacion y quieres optimizacion sistematica de prompts.
- Construyes pipelines de multiples modulos (RAG, agentes, clasificacion).
- Quieres un enfoque mas cercano a la programacion que al prompt engineering.
- Necesitas reproducibilidad: la misma especificacion + datos produce el mismo prompt optimizado.

**No uses DSPy cuando:**
- No tienes datos de evaluacion. Sin datos, el optimizador no puede optimizar.
- Tu caso de uso es simple (un solo prompt, un solo modelo). DSPy anade complejidad innecesaria.
- Necesitas control fino sobre el prompt exacto que se envia al modelo. DSPy genera prompts automaticamente, y a veces son verbosos o inesperados.
- Tu equipo no tiene experiencia con ML. La curva de aprendizaje de DSPy es mas pronunciada que la de otros frameworks.

---

## 15.5 OpenAI Agents SDK

### De Swarm a produccion

OpenAI lanzo Swarm en 2024 como un framework experimental para multi-agente. En marzo de 2025 (actualizado en 2026), lo reemplazo con el **Agents SDK**: un framework de produccion con primitivas minimas pero poderosas.

La filosofia de OpenAI es minimalista: tres primitivas cubren la mayoria de los casos.

### Las tres primitivas

```python
"""
Las tres primitivas del OpenAI Agents SDK.
"""

from dataclasses import dataclass, field
from typing import Callable, Optional


# --- Primitiva 1: Agent ---

@dataclass
class OpenAIAgent:
    """Un agente es un LLM con instrucciones y herramientas.

    En el SDK real:
    from agents import Agent
    agent = Agent(
        name="Support Agent",
        instructions="Ayudas a resolver tickets de soporte...",
        tools=[search_knowledge_base, create_ticket],
    )
    """
    name: str
    instructions: str
    tools: list[Callable] = field(default_factory=list)
    model: str = "gpt-4o"
    handoffs: list["OpenAIAgent"] = field(default_factory=list)


# --- Primitiva 2: Handoff ---
# Un agente puede delegar a otro agente.
# El SDK gestiona la transferencia de contexto automaticamente.

triage_agent = OpenAIAgent(
    name="Triage Agent",
    instructions="Clasifica el ticket y delega al agente correcto.",
)

billing_agent = OpenAIAgent(
    name="Billing Agent",
    instructions="Resuelve problemas de facturacion.",
    tools=[],  # lookup_invoice, process_refund, etc.
)

technical_agent = OpenAIAgent(
    name="Technical Agent",
    instructions="Resuelve problemas tecnicos.",
    tools=[],  # check_server_status, restart_service, etc.
)

# El triage agent puede delegar a billing o technical
triage_agent.handoffs = [billing_agent, technical_agent]


# --- Primitiva 3: Guardrail ---

@dataclass
class InputGuardrail:
    """Valida el input antes de que llegue al agente.

    En el SDK real:
    @input_guardrail
    async def check_toxicity(ctx, agent, input):
        # Validar input
        return GuardrailResult(output_info={"safe": True})
    """
    name: str
    validate: Callable


@dataclass
class OutputGuardrail:
    """Valida el output antes de que llegue al usuario."""
    name: str
    validate: Callable
```

### Funcionalidades de produccion

El SDK incluye:

- **Tracing integrado**: visualizacion y debugging de flujos agenticos desde el dashboard de OpenAI.
- **Function tools**: cualquier funcion Python se convierte en herramienta con generacion automatica de schema y validacion con Pydantic.
- **Sessions**: capa de memoria persistente para mantener contexto entre ejecuciones.
- **Human-in-the-loop**: mecanismos integrados para involucrar humanos.
- **MCP integration**: tool calling a servidores MCP que funciona igual que function tools nativos.

### Cuando si, cuando no

**Usa OpenAI Agents SDK cuando:**
- Tu proveedor principal es OpenAI y quieres la integracion mas estrecha con sus modelos.
- Prefieres un API minimalista con pocas abstracciones.
- Necesitas multi-agente con handoffs (un agente delega a otro).
- Quieres tracing y monitoreo integrado sin configuracion adicional.

**No uses OpenAI Agents SDK cuando:**
- Quieres independencia de proveedor. El SDK esta optimizado para modelos de OpenAI.
- Necesitas flujos de trabajo complejos con grafos de estado. LangGraph es mas expresivo.
- Requieres soporte para modelos open source o locales. El SDK asume modelos de OpenAI.

---

## 15.6 Anthropic Claude Agent SDK

### El SDK detras de Claude Code

El Claude Agent SDK (renombrado del Claude Code SDK para reflejar su alcance mas amplio) proporciona acceso programatico a las mismas herramientas, loop agentico y gestion de contexto que alimentan a Claude Code.

```python
"""
Estructura conceptual del Claude Agent SDK.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ClaudeAgentConfig:
    """Configuracion de un agente Claude.

    El SDK real ofrece herramientas integradas:
    - Operaciones de archivos (leer, escribir, editar)
    - Comandos de shell
    - Busqueda web
    - Integracion con servidores MCP
    """
    model: str = "claude-sonnet-4"
    instructions: str = ""
    tools: list[str] = field(default_factory=list)
    max_tokens: int = 4096
    mcp_servers: list[dict] = field(default_factory=list)

    # Subagentes para paralelizacion
    enable_subagents: bool = False
    max_concurrent_subagents: int = 3


# Ejemplo conceptual de uso:
#
# from claude_agent_sdk import Agent
#
# agent = Agent(
#     model="claude-sonnet-4",
#     instructions="Eres un agente de analisis de datos...",
#     tools=["file_read", "file_write", "shell"],
#     mcp_servers=[
#         {"name": "database", "url": "http://localhost:8080/mcp"},
#     ],
# )
#
# result = await agent.run("Analiza los datos de ventas del Q1")
```

### Funcionalidades clave

- **Herramientas integradas**: operaciones de archivos, shell, busqueda web y MCP sin configuracion adicional.
- **Subagentes**: paralelizacion nativa donde puedes lanzar multiples subagentes para trabajar en tareas simultaneas.
- **MCP nativo**: integracion con Model Context Protocol para extender las capacidades del agente con servidores MCP personalizados.
- **Remote Control**: relay HTTPS que mantiene el codigo fuente y las variables de entorno en la maquina local.

### Cuando si, cuando no

**Usa Claude Agent SDK cuando:**
- Tu proveedor principal es Anthropic y quieres la integracion mas estrecha con Claude.
- Necesitas capacidades de coding agent (operaciones de archivos, shell).
- Quieres subagentes para paralelizacion de tareas.
- Necesitas integracion nativa con MCP.

**No uses Claude Agent SDK cuando:**
- Quieres independencia de proveedor. El SDK esta optimizado para Claude.
- El SDK esta en etapas tempranas (v0.1.x en Python) y el API puede cambiar.
- Necesitas flujos de trabajo complejos con grafos de estado. LangGraph sigue siendo mas maduro para esto.

---

## 15.7 Tabla comparativa

La siguiente tabla resume las caracteristicas clave de cada framework en marzo de 2026:

```
| Criterio               | LangGraph      | CrewAI        | MS Agent Fwk  | DSPy          | OpenAI SDK    | Claude SDK    |
|------------------------|----------------|---------------|----------------|---------------|---------------|---------------|
| Modelo mental          | Grafos estado  | Equipos/roles | Agentes+Runtime| Firmas+Optim  | 3 primitivas  | Agent loop    |
| Madurez                | Alta           | Media-Alta    | Media (RC)     | Media         | Media-Alta    | Baja (v0.1)   |
| Multi-agente           | Si (nativo)    | Si (core)     | Si (nativo)    | Limitado      | Si (handoffs) | Si (subagents)|
| Persistencia estado    | Si (durable)   | Si (Flows)    | Si (sesiones)  | No nativo     | Si (sessions) | No nativo     |
| Human-in-the-loop      | Si (nativo)    | Si            | Si             | No nativo     | Si            | No nativo     |
| Independencia provider | Alta           | Alta          | Incl. Azure    | Alta          | Baja (OpenAI) | Baja (Claude) |
| Deployment gestionado  | Si (Platform)  | Si (AMP)      | Si (Azure)     | No            | Si (OpenAI)   | No            |
| Curva aprendizaje      | Alta           | Baja-Media    | Media          | Alta          | Baja          | Baja          |
| Comunidad/ecosistema   | Grande         | Grande        | Media          | Media         | Grande        | Pequena       |
| Open source            | Si (MIT)       | Si            | Si             | Si (MIT)      | Si (MIT)      | Si            |
| MCP integrado          | Via extensiones| Via tools     | Via extensiones| No            | Si (nativo)   | Si (nativo)   |
| Optimizacion prompts   | No             | No            | No             | Si (core)     | No            | No            |
| Lenguajes              | Python, JS     | Python        | Python, .NET   | Python        | Python, TS    | Python, TS    |
```

---

## 15.8 Criterios para elegir framework vs construir propio

### El arbol de decision

La decision entre usar un framework y construir tu propia solucion no es binaria. Es un espectro. Aqui esta el arbol de decision que recomendamos:

```python
"""
Arbol de decision para elegir framework de agentes.
"""


def choose_framework(
    team_size: int,
    agent_complexity: str,  # "simple", "medium", "complex"
    provider_preference: str,  # "openai", "anthropic", "multi", "local"
    need_multi_agent: bool,
    need_persistence: bool,
    need_hitl: bool,  # human-in-the-loop
    enterprise_requirements: bool,
    have_eval_data: bool,
    timeline_weeks: int,
) -> str:
    """Recomienda un framework basado en los requisitos.

    Returns:
        Recomendacion con justificacion.
    """

    # Caso 1: Agente simple, sin multi-agente
    if agent_complexity == "simple" and not need_multi_agent:
        if provider_preference == "openai":
            return (
                "OpenAI Agents SDK o llamada directa al API. "
                "Para un agente simple, un loop while con tool calling "
                "es suficiente. No necesitas un framework."
            )
        if provider_preference == "anthropic":
            return (
                "Claude Agent SDK o llamada directa al API de Anthropic. "
                "Tool use + un loop while cubre el caso."
            )
        return (
            "Llamada directa al API del proveedor con un loop while. "
            "No necesitas framework para un agente simple."
        )

    # Caso 2: Necesitas optimizacion automatica de prompts
    if have_eval_data and agent_complexity in ("medium", "complex"):
        return (
            "Considera DSPy para la optimizacion de prompts, "
            "combinado con otro framework para orquestacion si "
            "necesitas multi-agente o persistencia."
        )

    # Caso 3: Enterprise con ecosistema Microsoft
    if enterprise_requirements and provider_preference != "anthropic":
        return (
            "Microsoft Agent Framework. Integracion nativa con Azure, "
            ".NET support, gobernanza enterprise. Espera a GA (Q1 2026) "
            "para produccion critica."
        )

    # Caso 4: Multi-agente complejo con flujos dinamicos
    if need_multi_agent and agent_complexity == "complex":
        if need_persistence and need_hitl:
            return (
                "LangGraph. Es el mas maduro para grafos de estado "
                "complejos con persistencia y human-in-the-loop."
            )
        return (
            "LangGraph para flujos complejos, o CrewAI si prefieres "
            "un modelo mental de roles/equipos mas intuitivo."
        )

    # Caso 5: Multi-agente con roles claros
    if need_multi_agent and agent_complexity == "medium":
        return (
            "CrewAI. Su modelo de roles/tareas/equipos es intuitivo "
            "y suficiente para multi-agente de complejidad media."
        )

    # Caso 6: Prototipo rapido
    if timeline_weeks <= 2:
        return (
            "OpenAI Agents SDK o CrewAI. Ambos permiten tener "
            "un prototipo funcional en dias, no semanas."
        )

    # Default
    return (
        "Evalua LangGraph (mas flexible) vs CrewAI (mas intuitivo) "
        "segun la complejidad de tus flujos."
    )
```

### Cuando construir tu propio framework

Hay escenarios legitimos para construir tu propia solucion:

1. **Tu caso de uso es muy especifico** y ningun framework existente se adapta sin contorsiones significativas.
2. **Necesitas control total** sobre cada llamada al LLM, cada decision de routing, cada byte de contexto.
3. **Tu equipo tiene la capacidad** de mantener la infraestructura (persistencia, tracing, deployment) a largo plazo.
4. **Los costos de dependencia** superan los beneficios. Un framework que cambia su API cada 6 meses puede costar mas en migraciones que en desarrollo propio.

La guia de Chase sigue siendo valida: delega la infraestructura agentica (persistencia, tracing, deployment) a herramientas maduras (OpenTelemetry, PostgreSQL, Docker). Pero controla tu arquitectura cognitiva: como tu agente razona, que herramientas usa, como decide [Chase, 2024].

### El patron hibrido

En la practica, la mayoria de los equipos exitosos usan un patron hibrido:

- **Infraestructura**: OpenTelemetry para tracing, PostgreSQL para persistencia, Docker/Kubernetes para deployment.
- **Orquestacion**: un framework (LangGraph, CrewAI, o SDK del proveedor) para el loop agentico y la gestion de estado.
- **Logica de negocio**: codigo propio para guardrails, contratos tipados, routing de modelos, y la logica especifica de su dominio.

Este patron te da lo mejor de ambos mundos: no reinventas la rueda en infraestructura, pero mantienes control sobre la logica que diferencia tu producto.

---

## Takeaway del capitulo

El ecosistema de frameworks para agentes en 2026 es amplio pero esta convergiendo en patrones claros:

- **LangGraph** es la opcion mas madura para flujos complejos con grafos de estado, persistencia y human-in-the-loop. Su complejidad se justifica para agentes sofisticados, pero es sobreingenieria para casos simples.

- **CrewAI** ofrece el modelo mental mas intuitivo (roles, equipos, tareas) y es excelente para multi-agente de complejidad media. Su plataforma enterprise (AMP) lo posiciona para adopcion corporativa.

- **Microsoft Agent Framework** es la apuesta enterprise con integracion Azure y soporte .NET. Promete simplicidad de AutoGen con robustez de Semantic Kernel. Espera a GA para produccion critica.

- **DSPy** es unico en su enfoque de optimizacion automatica de prompts. Poderoso si tienes datos de evaluacion, pero su curva de aprendizaje es pronunciada y su enfoque es ortogonal al de los demas frameworks.

- **OpenAI Agents SDK** y **Claude Agent SDK** son las opciones naturales si estas comprometido con un proveedor especifico. Minimalistas, bien integrados, pero te atan a un ecosistema.

- **Construir tu propio framework** es viable si tu caso de uso es muy especifico, tienes capacidad de mantenimiento y necesitas control total. Pero la mayoria de los equipos se benefician del **patron hibrido**: infraestructura delegada + logica de negocio propia.

La regla de oro: **elige el framework despues de definir tu arquitectura cognitiva, no antes.** El framework es infraestructura. Tu arquitectura es lo que te diferencia.

---

## Referencias

- Chase, H. "Why You Should Outsource Your Agentic Infrastructure, But Own Your Cognitive Architecture." blog.langchain.com, julio 2024.
- Chase, H. "Reflections on Three Years of Building LangChain." blog.langchain.com, octubre 2025.
- LangChain. "LangGraph Platform is now Generally Available." blog.langchain.com, 2025.
- LangChain. "Building LangGraph: Designing an Agent Runtime from First Principles." blog.langchain.com, 2025.
- CrewAI. "The Leading Multi-Agent Platform." crewai.com, 2026.
- Microsoft. "Introducing Microsoft Agent Framework: The Open-Source Engine for Agentic AI Apps." devblogs.microsoft.com/foundry, 2025.
- Microsoft. "Migrate your Semantic Kernel and AutoGen projects to Microsoft Agent Framework Release Candidate." devblogs.microsoft.com, febrero 2026.
- Khattab, O., et al. "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines." *ICLR*, 2024.
- OpenAI. "New Tools for Building Agents." openai.com/index, 2025.
- Anthropic. "Building Agents with the Claude Agent SDK." anthropic.com/engineering, 2026.
- Anthropic. "Building Effective Agents." anthropic.com/research, diciembre 2024.
- Ousterhout, J. *A Philosophy of Software Design*. 2da edicion, 2021.
