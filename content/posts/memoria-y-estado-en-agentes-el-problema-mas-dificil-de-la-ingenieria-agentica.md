---
title: "Memoria y estado en agentes: el problema central de la ingeniería agéntica"
date: 2026-03-27
author: "Héctor Patricio"
tags: ['agentes', 'inteligencia-artificial', 'memoria', 'estado', 'llm', 'arquitectura', 'diseño-de-software', 'langgraph']
description: "El manejo de memoria y estado es uno de los desafíos de ingeniería centrales en sistemas agénticos. Exploramos los tipos de memoria, patrones de persistencia, estrategias de olvido y cómo implementar un sistema de memoria robusto."
featuredImage: ""
draft: true
---

Cada mañana, el agente despierta en blanco. Puede razonar y resolver problemas, pero no sabe qué proyectos tiene pendientes ni qué errores cometió la semana pasada. Esta condición, conocida como **amnesia anterógrada**, es exactamente la situación en la que se encuentran la mayoría de los agentes de IA hoy: procesan información, pero no acumulan experiencia.

En artículos anteriores hemos explorado [cómo razonan los LLMs](/posts/como-razonan-los-llms-de-turing-a-inference-time-scaling/), los [patrones de diseño para sistemas con IA](/posts/patrones-de-diseno-para-sistemas-con-ia/) y las lecciones de llevar [agentes teóricos a producción](/posts/de-agentes-teoricos-a-agentes-en-produccion/). Pero hay un problema que atraviesa todos estos temas y que, en mi opinión, es **uno de los más difíciles de resolver en la ingeniería agéntica**: el manejo de memoria y estado. Es el problema que toca más disciplinas simultáneamente y donde las decisiones equivocadas tienen mayor impacto en la calidad del sistema completo.

¿Por qué? Porque combina problemas de múltiples disciplinas: teoría de bases de datos, sistemas operativos, psicología cognitiva, recuperación de información y sistemas distribuidos. No existe una solución general. Cada sistema de agentes necesita una estrategia de memoria diseñada para su caso de uso específico.

En este artículo vamos a explorar el problema a fondo, desde los fundamentos teóricos hasta la implementación práctica.

## Tipos de memoria en agentes

Para entender el problema de la memoria en agentes, conviene primero mirar cómo funciona la memoria en los seres humanos. La neurociencia cognitiva ha identificado varios tipos de memoria que trabajan en conjunto, y esta taxonomía resulta directamente útil para diseñar sistemas de memoria artificial.

### Memoria de trabajo (*working memory*): la ventana de contexto activa

La **working memory** (memoria de trabajo) en humanos es ese espacio mental limitado donde mantienes la información que estás procesando activamente. Cuando haces una multiplicación mental, los números que estás manipulando están en tu memoria de trabajo. Su capacidad es famosamente limitada: George Miller propuso en 1956 que podemos mantener aproximadamente 7 elementos (más o menos 2) simultáneamente, aunque investigaciones posteriores, como las de Cowan (2001), sugieren un límite más bajo, cercano a 4 elementos.

En un agente basado en LLM, la working memory es la **ventana de contexto**. Es toda la información que el modelo puede "ver" en un momento dado: el prompt del sistema, el historial de conversación, las herramientas disponibles y cualquier dato que hayamos inyectado. Con modelos como GPT-4o o Claude, esta ventana puede ser de 128K a 200K tokens, pero sigue siendo finita y, lo más importante, **costosa**. Cada token que metes en la ventana de contexto cuesta dinero y tiempo de procesamiento.

```python
# La ventana de contexto es la "working memory" del agente
contexto = {
    "system_prompt": "Eres un agente de soporte técnico...",  # ~500 tokens
    "herramientas": [...],                                      # ~2000 tokens
    "historial_conversacion": [...],                            # ~variable
    "datos_recuperados": [...],                                 # ~variable
    # Total: debe caber en la ventana de contexto del modelo
}
```

El problema fundamental es que, a diferencia de la memoria de trabajo humana que puede "comprimir" información (piensas en "mi dirección" en vez de recordar cada carácter), la ventana de contexto es literal: cada palabra ocupa espacio. No hay compresión nativa.

### Memoria a corto plazo (*short-term memory*): dentro de una sesión

La **memoria a corto plazo** en un agente corresponde a todo lo que el agente recuerda dentro de una sesión de interacción. Incluye el historial de la conversación, los resultados de herramientas que ha usado, las decisiones que ha tomado y su razonamiento.

En la práctica, esta memoria suele implementarse como una lista de mensajes que crece con cada interacción:

```python
class ShortTermMemory:
    def __init__(self, max_tokens: int = 100_000):
        self.messages: list[dict] = []
        self.max_tokens = max_tokens
        self.current_tokens = 0

    def add(self, role: str, content: str):
        tokens = self._count_tokens(content)
        # Cuando nos acercamos al límite, debemos decidir qué olvidar
        while self.current_tokens + tokens > self.max_tokens:
            self._evict_oldest()
        self.messages.append({"role": role, "content": content})
        self.current_tokens += tokens

    def _evict_oldest(self):
        """Estrategia más simple: eliminar el mensaje más antiguo"""
        if self.messages:
            removed = self.messages.pop(0)
            self.current_tokens -= self._count_tokens(removed["content"])
```

El problema aquí es sutil pero importante: cuando eliminas mensajes antiguos para hacer espacio, puedes perder contexto crítico. Imagina un agente de soporte que al inicio de la conversación recibió la información de que el usuario es un cliente enterprise con SLA prioritario. Si esa información se elimina por ser "antigua", el agente podría empezar a dar respuestas genéricas.

### Memoria a largo plazo (*long-term memory*): entre sesiones

La **memoria a largo plazo** permite que un agente recuerde información entre sesiones completamente diferentes. Es la diferencia entre un asistente que te trata como un extraño cada vez que hablas con él y uno que recuerda tus preferencias, tu contexto y tu historial.

En los humanos, la memoria a largo plazo se subdivide en tres categorías que resultan muy útiles para el diseño de agentes:

**Memoria episódica**: recuerdos de experiencias específicas. "La última vez que el usuario pidió un reporte de ventas, prefirió formato CSV". Son como snapshots de interacciones pasadas con contexto temporal. En un agente, se implementan típicamente como registros indexados por tiempo con metadatos sobre el resultado de la interacción.

**Memoria semántica**: conocimiento general abstracto, separado de experiencias específicas. "Los reportes de ventas se generan con la herramienta X y requieren acceso a la base de datos Y". Es conocimiento que el agente ha adquirido pero que ya no está atado a un episodio particular. En la práctica, se implementa con bases de datos vectoriales o grafos de conocimiento.

**Memoria procedimental**: conocimiento de cómo hacer cosas. "Para generar un reporte, primero consulto la API de ventas, luego formateo los datos, luego genero el PDF". En sistemas de agentes, esto se traduce en workflows aprendidos, plantillas de acción o incluso código generado dinámicamente que el agente reutiliza.

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class MemoryType(Enum):
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"

@dataclass
class MemoryEntry:
    content: str
    memory_type: MemoryType
    timestamp: datetime
    importance: float  # 0.0 a 1.0
    access_count: int = 0
    last_accessed: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)

    def apply_decay(self, decay_rate: float = 0.01):
        """Aplica decaimiento temporal a la importancia y actualiza
        el marcador de último acceso. NOTA: esta función MUTA el objeto
        (actualiza importance y last_accessed). Si necesitas el valor
        sin mutar, usa calculate_decayed_importance()."""
        now = datetime.now()
        hours_since_access = (
            now - self.last_accessed
        ).total_seconds() / 3600
        self.importance *= (1 - decay_rate) ** hours_since_access
        self.last_accessed = now

    def calculate_decayed_importance(self, decay_rate: float = 0.01) -> float:
        """Calcula la importancia con decaimiento SIN mutar el objeto.
        Útil para scoring y ordenamiento sin efectos secundarios."""
        hours_since_access = (
            datetime.now() - self.last_accessed
        ).total_seconds() / 3600
        return self.importance * (1 - decay_rate) ** hours_since_access
```

La analogía con la memoria humana no es solo pedagógica: nos da un marco de diseño genuinamente útil. Así como un ser humano no intenta recordar cada detalle de cada día, un agente necesita mecanismos para decidir qué vale la pena guardar y qué puede olvidar.

## El estado como ciudadano de primera clase

Si la memoria es lo que el agente "sabe", el **estado** es "en qué punto se encuentra". Y gestionar el estado correctamente es fundamental para construir agentes confiables. Piénsalo así: cuando pausas un videojuego y lo retomas tres días después, esperas estar exactamente donde lo dejaste. Los agentes en producción necesitan la misma capacidad.

### State machines para agentes

Una de las lecciones más importantes que hemos aprendido al pasar [de agentes teóricos a agentes en producción](/posts/de-agentes-teoricos-a-agentes-en-produccion/) es que los agentes confiables necesitan estados bien definidos. Un agente que "simplemente razona en bucle" es difícil de depurar, de monitorear y de recuperar cuando algo falla.

Las **máquinas de estado finitas** (FSMs) son uno de los formalismos más antiguos de la computación, y resulta que son perfectas para modelar el comportamiento de agentes:

```python
from enum import Enum, auto
from typing import Callable

class AgentState(Enum):
    IDLE = auto()
    ANALYZING = auto()
    PLANNING = auto()
    EXECUTING = auto()
    WAITING_FOR_TOOL = auto()
    REVIEWING = auto()
    ERROR_RECOVERY = auto()
    COMPLETED = auto()

class AgentStateMachine:
    TRANSITIONS: dict[AgentState, set[AgentState]] = {
        AgentState.IDLE: {AgentState.ANALYZING},
        AgentState.ANALYZING: {AgentState.PLANNING, AgentState.ERROR_RECOVERY},
        AgentState.PLANNING: {AgentState.EXECUTING, AgentState.ANALYZING},
        AgentState.EXECUTING: {
            AgentState.WAITING_FOR_TOOL,
            AgentState.REVIEWING,
            AgentState.ERROR_RECOVERY
        },
        AgentState.WAITING_FOR_TOOL: {
            AgentState.EXECUTING,
            AgentState.ERROR_RECOVERY
        },
        AgentState.REVIEWING: {
            AgentState.COMPLETED,
            AgentState.PLANNING  # Volver a planificar si no está satisfecho
        },
        AgentState.ERROR_RECOVERY: {
            AgentState.ANALYZING,
            AgentState.IDLE
        },
    }

    def __init__(self):
        self.current_state = AgentState.IDLE
        self.state_history: list[tuple[AgentState, datetime]] = []

    def transition(self, new_state: AgentState):
        if new_state not in self.TRANSITIONS.get(self.current_state, set()):
            raise InvalidTransitionError(
                f"No se puede ir de {self.current_state} a {new_state}"
            )
        self.state_history.append((self.current_state, datetime.now()))
        self.current_state = new_state
```

Esta estructura explícita tiene beneficios enormes: puedes saber exactamente en qué punto está un agente, puedes validar que las transiciones son legales, puedes generar métricas por estado y puedes detectar cuando un agente está "atascado" en un ciclo.

### Checkpointing: guardar para resumir

El **checkpointing** es la práctica de guardar el estado completo de un agente en un momento dado para poder reanudarlo después. Es un concepto que viene directamente de los sistemas operativos, donde los procesos se suspenden y reanudan constantemente.

Un buen sistema de checkpointing debe capturar:

1. **El estado de la máquina de estados** (en qué paso está)
2. **La memoria de trabajo** (qué tiene en contexto)
3. **La memoria a corto plazo** (el historial de la sesión)
4. **Los resultados intermedios** (outputs de herramientas, datos parciales)
5. **Los metadatos de ejecución** (cuántos tokens ha consumido, tiempo transcurrido)

```python
import json
from pathlib import Path

@dataclass
class AgentCheckpoint:
    agent_id: str
    state: AgentState
    working_memory: dict
    short_term_memory: list[dict]
    intermediate_results: list[dict]
    metadata: dict
    timestamp: datetime = field(default_factory=datetime.now)

    def save(self, checkpoint_dir: Path):
        filepath = checkpoint_dir / f"{self.agent_id}_{self.timestamp.isoformat()}.json"
        filepath.write_text(json.dumps(self._serialize(), indent=2))
        return filepath

    @classmethod
    def load(cls, filepath: Path) -> "AgentCheckpoint":
        data = json.loads(filepath.read_text())
        return cls._deserialize(data)
```

### Rollback: volver atrás cuando algo falla

Si el checkpointing es "guardar partida", el **rollback** es "cargar partida". Y en agentes de producción, necesitas rollback constantemente. Un agente que llama a una API externa y obtiene un error, un agente que genera una respuesta incoherente, un agente que entra en un loop infinito: todos necesitan la capacidad de volver a un estado anterior conocido y tomar un camino diferente.

**La trampa de los side effects**: el checkpointing de agentes es, en realidad, un problema de transacciones distribuidas disfrazado. Puedes revertir el estado interno del agente (su memoria, su posición en la máquina de estados), pero **no puedes revertir las acciones externas** que ya ejecutó: emails enviados, pagos procesados, APIs llamadas, mensajes publicados. Por eso, en producción, tu estrategia de checkpointing debe clasificar las acciones del agente en dos categorías:

- **Reversibles**: lecturas de base de datos, búsquedas, cálculos internos. Se pueden deshacer sin consecuencias.
- **Irreversibles**: envío de emails, transferencias de dinero, publicaciones, llamadas a APIs externas con efectos. Estas requieren confirmación humana *antes* de ejecutarse, o al menos un mecanismo de compensación (como enviar un email de corrección).

El patrón es similar al de las transacciones en bases de datos, pero con una limitación importante: los principios ACID solo aplican completamente dentro de los límites de tu sistema. Los side effects externos están fuera de tu control transaccional.

```python
class RollbackManager:
    def __init__(self, max_checkpoints: int = 10):
        self.checkpoints: list[AgentCheckpoint] = []
        self.max_checkpoints = max_checkpoints

    def save_checkpoint(self, agent) -> AgentCheckpoint:
        checkpoint = AgentCheckpoint(
            agent_id=agent.id,
            state=agent.state_machine.current_state,
            working_memory=agent.working_memory.copy(),
            short_term_memory=agent.short_term_memory.messages.copy(),
            intermediate_results=agent.results.copy(),
            metadata={"tokens_used": agent.tokens_used}
        )
        self.checkpoints.append(checkpoint)
        if len(self.checkpoints) > self.max_checkpoints:
            self.checkpoints.pop(0)  # Mantener solo los N más recientes
        return checkpoint

    def rollback(self, agent, steps_back: int = 1):
        """Restaurar el agente a un estado anterior"""
        if steps_back > len(self.checkpoints):
            raise RollbackError("No hay suficientes checkpoints")
        checkpoint = self.checkpoints[-(steps_back)]
        agent.restore_from_checkpoint(checkpoint)
        # Eliminar los checkpoints posteriores al punto de restauración
        self.checkpoints = self.checkpoints[:-(steps_back)]
```

### LangGraph y su modelo de estado

LangGraph, el sucesor de LangChain que mencionamos en [nuestro artículo sobre agentes en producción](/posts/de-agentes-teoricos-a-agentes-en-produccion/), adopta explícitamente el estado como concepto central. En LangGraph, defines un **grafo de estados** donde cada nodo es una función que transforma el estado y cada arista define las transiciones posibles.

Lo interesante de LangGraph es que el estado es un objeto tipado (generalmente un `TypedDict` o un `Pydantic BaseModel`) que se pasa entre nodos y se persiste automáticamente. Esto resuelve el checkpointing de forma nativa:

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver

class AgentState(TypedDict):
    messages: list[dict]
    current_plan: str
    tools_results: list[dict]
    iteration_count: int

def analyze_node(state: AgentState) -> AgentState:
    """Cada nodo recibe el estado, lo transforma y lo devuelve"""
    # El framework se encarga de persistir el estado automáticamente
    return {
        **state,
        "current_plan": generate_plan(state["messages"]),
        "iteration_count": state["iteration_count"] + 1
    }

# El checkpointer persiste cada transición de estado
checkpointer = SqliteSaver.from_conn_string("checkpoints.db")
graph = StateGraph(AgentState)
graph.add_node("analyze", analyze_node)
# ... más nodos y aristas
app = graph.compile(checkpointer=checkpointer)
```

Esta aproximación es poderosa porque hace que la gestión de estado sea **declarativa** en lugar de imperativa. No tienes que recordar guardar el estado manualmente; el framework lo hace por ti en cada transición.

## Persistencia de memoria

Una vez que entendemos los tipos de memoria y la importancia del estado, la pregunta natural es: ¿cómo persistimos todo esto de forma eficiente? Aquí convergen técnicas de bases de datos, recuperación de información y sistemas operativos.

### Bases de datos vectoriales para memoria semántica

La memoria semántica (conocimiento general) se beneficia enormemente de las **bases de datos vectoriales**. La idea es simple pero potente: cada pieza de conocimiento se convierte en un vector numérico (embedding) que captura su significado semántico. Cuando el agente necesita recordar algo relevante, busca los vectores más cercanos a su consulta actual.

Hablamos extensamente de esto en [nuestro artículo sobre patrones de diseño para sistemas con IA](/posts/patrones-de-diseno-para-sistemas-con-ia/), donde describimos el patrón RAG (Retrieval-Augmented Generation). Pero en el contexto de memoria para agentes, el RAG toma un matiz diferente: no solo recuperas documentos externos, sino **las propias experiencias y conocimientos del agente**.

```python
import chromadb
from sentence_transformers import SentenceTransformer

class SemanticMemory:
    def __init__(self, collection_name: str = "agent_memory"):
        self.client = chromadb.PersistentClient(path="./agent_memory_db")
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")

    def store(self, content: str, metadata: dict):
        embedding = self.encoder.encode(content).tolist()
        self.collection.add(
            documents=[content],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[f"mem_{datetime.now().timestamp()}"]
        )

    def recall(self, query: str, n_results: int = 5) -> list[dict]:
        """Recuperar las memorias más relevantes para la consulta"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return [
            {"content": doc, "metadata": meta, "distance": dist}
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            )
        ]
```

### Los costos ocultos de la memoria a largo plazo

Antes de elegir una estrategia de memoria, hay que hablar del elefante en la habitación: **los costos operativos**. Cada componente de la memoria a largo plazo tiene un precio que se acumula rápidamente en producción:

**Costo de embedding**: cada nueva memoria que guardas necesita convertirse en un vector. Con un modelo de embeddings como `text-embedding-3-small` de OpenAI, cuesta aproximadamente $0.02 por millón de tokens. Parece poco, pero un agente activo puede generar cientos de memorias por día, y el costo se multiplica por el número de usuarios.

**Costo de almacenamiento**: mantener un índice vectorial en un servicio gestionado (Pinecone, Weaviate Cloud, Qdrant Cloud) tiene un costo mensual base más un costo por vector almacenado. Para millones de memorias de agentes, esto puede llegar a cientos de dólares al mes.

**Latencia de retrieval**: cada búsqueda vectorial añade latencia al request del agente. Una búsqueda en un índice local (ChromaDB, FAISS) tarda 5-50ms. En un servicio remoto, la latencia de red suma 50-200ms adicionales. Cuando tu agente hace 2-3 búsquedas de memoria por turno, esto se nota en la experiencia del usuario.

**Costo de contexto**: las memorias recuperadas ocupan tokens en la ventana de contexto. Si recuperas 5 memorias de 200 tokens cada una, estás usando 1,000 tokens adicionales por llamada al LLM. A escala, este costo de contexto suele ser mayor que el costo del embedding original.

La decisión de "qué vale la pena memorizar" no es solo técnica: es económica. Un agente interno de bajo volumen puede permitirse memorizar todo. Un agente de atención al cliente con millones de sesiones necesita políticas estrictas de retención y un presupuesto de memoria por usuario.

### Almacenes clave-valor (*key-value stores*) para memoria episódica

La memoria episódica se organiza mejor en **key-value stores** porque sus patrones de acceso son diferentes: necesitas buscar por tiempo, por tipo de evento, por resultado. Redis, DynamoDB o incluso SQLite funcionan bien aquí:

```python
import sqlite3
from contextlib import contextmanager

class EpisodicMemory:
    def __init__(self, db_path: str = "episodes.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS episodes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    context TEXT NOT NULL,
                    action_taken TEXT NOT NULL,
                    outcome TEXT NOT NULL,
                    success BOOLEAN NOT NULL,
                    importance REAL DEFAULT 0.5,
                    metadata TEXT DEFAULT '{}'
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_event_type
                ON episodes(event_type)
            """)

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def record_episode(self, event_type: str, context: str,
                       action: str, outcome: str, success: bool,
                       importance: float = 0.5):
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO episodes (timestamp, event_type, context, "
                "action_taken, outcome, success, importance) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (datetime.now().isoformat(), event_type, context,
                 action, outcome, success, importance)
            )

    def recall_similar_situations(self, event_type: str,
                                   limit: int = 5) -> list[dict]:
        """¿Qué hizo el agente en situaciones similares?"""
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT * FROM episodes WHERE event_type = ? "
                "ORDER BY importance DESC, timestamp DESC LIMIT ?",
                (event_type, limit)
            )
            return [dict(zip([d[0] for d in cursor.description], row))
                    for row in cursor.fetchall()]
```

### El patrón "Memory Bank" con archivos

Un patrón que ha ganado popularidad, especialmente en agentes de desarrollo de software, es el **memory bank**: archivos de texto plano (generalmente Markdown) que el agente lee al inicio de cada sesión y actualiza al final. Es simple, versionable con Git y legible tanto por humanos como por agentes.

La idea es tener una estructura como:

```
memory_bank/
  project_context.md      # Qué es este proyecto, decisiones clave
  current_tasks.md        # En qué está trabajando el agente
  learned_patterns.md     # Patrones que ha descubierto
  errors_and_fixes.md     # Errores comunes y cómo resolverlos
  user_preferences.md     # Preferencias del usuario
```

Es un enfoque rudimentario pero sorprendentemente efectivo para ciertos casos de uso. Su limitación principal es que escala mal: cuando los archivos crecen demasiado, no caben en la ventana de contexto y necesitas mecanismos de selección, lo que te lleva de vuelta al problema de la relevancia que veremos más adelante.

### MemGPT: paginación de memoria inspirada en sistemas operativos

Una de las ideas más elegantes en memoria para agentes viene de **MemGPT**, un sistema que aplica conceptos de sistemas operativos a la gestión de memoria de LLMs. Su innovación clave es que el propio LLM decide *activamente* cuándo hacer page-in y page-out, usando herramientas para gestionar su propia memoria en lugar de depender de un sistema externo. La analogía con sistemas operativos es directa:

- **La ventana de contexto del LLM** es como la **RAM** de un computador: rápida pero limitada.
- **La memoria externa** (bases de datos, archivos) es como el **disco duro**: abundante pero lenta de acceder.
- **MemGPT** implementa un sistema de **memoria virtual** con paginación, exactamente como lo hace un sistema operativo.

El sistema operativo resuelve el problema de tener más datos que RAM mediante la **paginación**: divide la memoria en bloques (páginas) y las mueve entre RAM y disco según se necesiten. MemGPT hace lo mismo con la ventana de contexto:

```python
class MemGPTStyle:
    """Implementación simplificada del patrón MemGPT.
    Nota: en MemGPT real, el LLM invoca estas operaciones
    como herramientas; aquí las controlamos externamente."""

    def __init__(self, context_window_size: int, page_size: int = 2000):
        self.context_window_size = context_window_size
        self.page_size = page_size
        # "RAM" - lo que está en la ventana de contexto
        self.active_pages: list[MemoryPage] = []
        # "Disco" - almacenamiento externo
        self.external_storage = ExternalStorage()

    def page_in(self, query: str):
        """Cargar páginas relevantes del almacenamiento externo al contexto"""
        relevant_pages = self.external_storage.search(query)
        for page in relevant_pages:
            if self._context_has_space():
                self.active_pages.append(page)
            else:
                # Page out: mover la página menos usada al disco
                self._evict_least_recently_used()
                self.active_pages.append(page)

    def page_out(self, page: MemoryPage):
        """Mover una página del contexto al almacenamiento externo"""
        self.external_storage.store(page)
        self.active_pages.remove(page)

    def _evict_least_recently_used(self):
        """LRU: exactamente como en un sistema operativo"""
        if self.active_pages:
            lru_page = min(self.active_pages, key=lambda p: p.last_accessed)
            self.page_out(lru_page)
```

Esta idea es poderosa porque nos permite razonar sobre la memoria de agentes usando décadas de investigación en sistemas operativos. Algoritmos como LRU (Least Recently Used), LFU (Least Frequently Used) y Clock, que se enseñan en cualquier curso de sistemas operativos, aplican directamente aquí.

## El problema de la relevancia

Aquí llegamos a lo que considero el núcleo más difícil del problema de la memoria en agentes: **no todo debe recordarse, y decidir qué es importante es en sí mismo un problema de IA**.

Un ser humano no recuerda cada segundo de su vida. Tu cerebro constantemente decide qué consolidar en memoria a largo plazo y qué descartar. Los recuerdos con carga emocional fuerte se consolidan más fácilmente; los detalles triviales se olvidan. Este proceso de **filtrado** es esencial: sin él, estarías abrumado por información irrelevante.

Los agentes enfrentan exactamente el mismo problema. Si un agente recuerda todo, su memoria se vuelve ruidosa y las búsquedas de información relevante pierden precisión. Si recuerda muy poco, pierde contexto valioso. El balance es delicado.

### Relevance scoring

Una estrategia es asignar una **puntuación de relevancia** a cada pieza de información y usar esa puntuación para decidir qué guardar y qué recuperar. Los factores que influyen en la relevancia pueden incluir:

```python
def calculate_relevance(
    memory_entry: MemoryEntry,
    current_context: str,
    current_time: datetime
) -> float:
    """Calcular la relevancia de una memoria dado el contexto actual"""

    # 1. Similitud semántica con el contexto actual
    semantic_similarity = compute_cosine_similarity(
        encode(memory_entry.content),
        encode(current_context)
    )

    # 2. Recencia: las memorias recientes son más relevantes
    hours_ago = (current_time - memory_entry.timestamp).total_seconds() / 3600
    recency_score = 1.0 / (1.0 + 0.1 * hours_ago)  # Decaimiento hiperbólico

    # 3. Importancia intrínseca (asignada al crear la memoria)
    importance = memory_entry.importance

    # 4. Frecuencia de acceso: si se usa mucho, probablemente es importante
    access_score = min(1.0, memory_entry.access_count / 10.0)

    # Combinación ponderada
    relevance = (
        0.4 * semantic_similarity +
        0.25 * recency_score +
        0.2 * importance +
        0.15 * access_score
    )
    return relevance
```

Este enfoque viene del paper de **"Generative Agents"** de Park et al. (2023), donde simularon agentes que vivían en un pueblo virtual y necesitaban recordar interacciones con otros agentes. Usaron exactamente esta combinación de recencia, importancia y relevancia para decidir qué memorias recuperar.

### Estrategias de olvido

Tan importante como recordar es **olvidar**. Aquí podemos tomar prestados patrones de los sistemas de caché, que llevan décadas resolviendo exactamente este problema:

**LRU (Least Recently Used)**: elimina las memorias que llevan más tiempo sin accederse. Simple y efectivo, pero puede eliminar información importante que simplemente no ha sido relevante recientemente.

**TTL (Time to Live)**: cada memoria tiene una fecha de expiración. Útil para información que sabes que tiene vigencia limitada (como el estado de un sistema externo), pero no funciona bien para conocimiento atemporal.

**Importance-based**: solo elimina memorias cuya importancia ha caído por debajo de un umbral. Es la estrategia más sofisticada pero requiere un buen sistema de scoring.

```python
class ForgettingStrategy:
    """Estrategias de olvido inspiradas en sistemas de caché"""

    @staticmethod
    def lru_forget(memories: list[MemoryEntry], max_size: int) -> list[MemoryEntry]:
        """Eliminar las memorias menos recientemente usadas"""
        sorted_by_access = sorted(
            memories, key=lambda m: m.last_accessed, reverse=True
        )
        return sorted_by_access[:max_size]

    @staticmethod
    def importance_forget(
        memories: list[MemoryEntry],
        threshold: float = 0.1
    ) -> list[MemoryEntry]:
        """Eliminar memorias cuya importancia ha decaído bajo el umbral"""
        # Primero aplicar el decaimiento de todas las memorias
        for mem in memories:
            mem.apply_decay()
        return [m for m in memories if m.importance >= threshold]

    @staticmethod
    def hybrid_forget(
        memories: list[MemoryEntry],
        max_size: int,
        min_importance: float = 0.1
    ) -> list[MemoryEntry]:
        """Combinación: primero filtrar por importancia, luego por LRU"""
        important = [m for m in memories if m.importance >= min_importance]
        if len(important) <= max_size:
            return important
        return sorted(
            important, key=lambda m: m.last_accessed, reverse=True
        )[:max_size]
```

La estrategia híbrida suele ser la más efectiva en la práctica: protege las memorias marcadas como importantes mientras usa LRU para el resto.

## Consistencia de estado en sistemas multi-agente

Hasta ahora hemos hablado de un solo agente. Pero los sistemas de producción rara vez tienen un solo agente. Los [patrones de diseño para sistemas con IA](/posts/patrones-de-diseno-para-sistemas-con-ia/) como Orquestador-Trabajador implican múltiples agentes colaborando. Y aquí aparece un viejo conocido de la ingeniería de software: **el problema de la concurrencia**.

Como exploramos en [nuestro artículo sobre la diferencia entre concurrencia y paralelismo](/posts/la-diferencia-entre-concurrencia-y-paralelismo/), la concurrencia es sobre la **composición de tareas independientes que interactúan entre sí**. En sistemas multi-agente, los agentes son esas tareas independientes, y la memoria compartida es donde interactúan.

### Estado compartido vs. paso de mensajes

Hay dos paradigmas fundamentales para la comunicación entre agentes concurrentes:

**Estado compartido (Shared State)**: todos los agentes leen y escriben en la misma memoria. Es simple de implementar pero peligroso. Es como tener múltiples hilos accediendo a la misma variable global sin locks: receta para el desastre.

**Paso de mensajes (Message Passing)**: los agentes se comunican exclusivamente enviándose mensajes. Cada agente mantiene su propia memoria privada. Es más seguro pero puede ser más complejo de implementar.

En la práctica, la mayoría de los sistemas multi-agente usan un **híbrido**: memoria privada para cada agente con un canal compartido para coordinación:

```python
import asyncio
from asyncio import Queue

class AgentCommunication:
    """Sistema de comunicación entre agentes basado en message passing"""

    def __init__(self):
        self.channels: dict[str, Queue] = {}
        self.shared_blackboard: dict = {}  # Estado compartido controlado
        # Nota: asyncio.Lock() protege contra acceso concurrente
        # dentro de un solo event loop (un proceso). Para múltiples
        # procesos, necesitarías un lock distribuido (Redis, ZooKeeper, etc.)
        self._lock = asyncio.Lock()

    async def send_message(self, from_agent: str, to_agent: str, message: dict):
        """Enviar mensaje a otro agente (message passing)"""
        channel_key = f"channel_{to_agent}"
        if channel_key not in self.channels:
            self.channels[channel_key] = Queue()
        await self.channels[channel_key].put({
            "from": from_agent,
            "content": message,
            "timestamp": datetime.now().isoformat()
        })

    async def receive_message(self, agent_id: str) -> dict | None:
        """Recibir el siguiente mensaje (no bloqueante)"""
        channel_key = f"channel_{agent_id}"
        if channel_key in self.channels and not self.channels[channel_key].empty():
            return await self.channels[channel_key].get()
        return None

    async def update_shared_state(self, agent_id: str, key: str, value):
        """Actualizar estado compartido con lock (mutual exclusion)"""
        async with self._lock:
            self.shared_blackboard[key] = {
                "value": value,
                "updated_by": agent_id,
                "timestamp": datetime.now().isoformat()
            }
```

### Condiciones de carrera (*race conditions*) en agentes

Las **race conditions** son un problema real en sistemas multi-agente. Imagina dos agentes que trabajan en paralelo sobre un problema de soporte al cliente:

1. Agente A lee el estado del ticket: "abierto"
2. Agente B lee el estado del ticket: "abierto"
3. Agente A resuelve el problema y marca el ticket como "resuelto"
4. Agente B, que no sabe que A ya lo resolvió, también intenta resolverlo

Esto no solo desperdicia recursos, puede generar respuestas contradictorias al usuario. Las soluciones son las mismas que en programación concurrente clásica:

- **Locks / Mutexes**: solo un agente puede acceder a un recurso a la vez
- **Optimistic Concurrency Control**: permitir acceso simultáneo pero detectar y resolver conflictos
- **Event Sourcing**: en lugar de modificar estado directamente, registrar eventos y derivar el estado

```python
class OptimisticLockMemory:
    """Memoria compartida con control de concurrencia optimista"""

    def __init__(self):
        self.store: dict[str, dict] = {}

    async def read(self, key: str) -> tuple[any, int]:
        """Retorna el valor y su versión"""
        entry = self.store.get(key, {"value": None, "version": 0})
        return entry["value"], entry["version"]

    async def write(self, key: str, value, expected_version: int) -> bool:
        """Escribe solo si la versión no ha cambiado (CAS - Compare And Swap)"""
        current = self.store.get(key, {"value": None, "version": 0})
        if current["version"] != expected_version:
            return False  # Alguien más modificó el valor, conflicto
        self.store[key] = {
            "value": value,
            "version": expected_version + 1
        }
        return True
```

Este patrón de Compare-And-Swap (CAS) es el mismo que usan las bases de datos para manejar transacciones concurrentes. Otra vez, décadas de investigación en sistemas distribuidos nos dan las herramientas para resolver estos problemas.

## Ejemplo práctico: implementando un sistema de memoria completo

Vamos a integrar todo lo que hemos discutido en un sistema de memoria cohesivo para un agente. Este ejemplo muestra cómo las piezas encajan:

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import json

class AgentMemorySystem:
    """Sistema de memoria completo para un agente de IA"""

    def __init__(
        self,
        agent_id: str,
        context_window_tokens: int = 128_000,
        reserved_tokens: int = 4_000  # Para el system prompt y herramientas
    ):
        self.agent_id = agent_id
        self.available_tokens = context_window_tokens - reserved_tokens

        # Tres tipos de memoria
        self.working_memory = WorkingMemory(max_tokens=self.available_tokens)
        self.episodic_memory = EpisodicMemory(
            db_path=f"memory/{agent_id}_episodes.db"
        )
        self.semantic_memory = SemanticMemory(
            collection_name=f"{agent_id}_knowledge"
        )

        # Gestión de estado
        self.state_machine = AgentStateMachine()
        self.rollback_manager = RollbackManager()

        # Estrategia de olvido
        self.forgetting = ForgettingStrategy()

    async def prepare_context(self, user_query: str) -> dict:
        """
        Preparar el contexto óptimo para una llamada al LLM.
        Este es el método central: decide qué poner en la
        ventana de contexto basándose en la relevancia.
        """
        # 1. Recuperar memorias episódicas relevantes
        similar_episodes = self.episodic_memory.recall_similar_situations(
            event_type=self._classify_query(user_query),
            limit=3
        )

        # 2. Recuperar conocimiento semántico relevante
        relevant_knowledge = self.semantic_memory.recall(
            query=user_query,
            n_results=5
        )

        # 3. Obtener el historial de conversación reciente
        recent_messages = self.working_memory.get_recent(max_tokens=50_000)

        # 4. Construir el contexto priorizando por relevancia
        #    Nota: las memorias inyectadas consumen tokens de la ventana.
        #    Establece un presupuesto máximo (ej. 10-15% de la ventana)
        #    para evitar desplazar el historial de conversación actual.
        context = {
            "recent_conversation": recent_messages,
            "relevant_knowledge": [
                k["content"] for k in relevant_knowledge
                if k["distance"] < 0.7  # Solo memorias suficientemente cercanas
            ],
            "similar_past_experiences": [
                {
                    "situation": ep["context"],
                    "action": ep["action_taken"],
                    "result": ep["outcome"],
                    "success": ep["success"]
                }
                for ep in similar_episodes
            ],
            "current_state": self.state_machine.current_state.name
        }

        # 5. Checkpoint antes de procesar
        self.rollback_manager.save_checkpoint(self)

        return context

    async def process_result(
        self,
        user_query: str,
        agent_response: str,
        tool_results: list[dict],
        success: bool
    ):
        """Después de que el agente responde, actualizar todas las memorias"""

        # 1. Actualizar working memory
        self.working_memory.add("user", user_query)
        self.working_memory.add("assistant", agent_response)

        # 2. Registrar episodio
        self.episodic_memory.record_episode(
            event_type=self._classify_query(user_query),
            context=user_query,
            action=agent_response[:500],  # Truncar para no llenar la BD
            outcome=json.dumps(tool_results)[:500],
            success=success,
            importance=self._assess_importance(user_query, success)
        )

        # 3. Extraer conocimiento semántico si aplica
        if success and tool_results:
            knowledge = self._extract_knowledge(
                user_query, agent_response, tool_results
            )
            if knowledge:
                self.semantic_memory.store(
                    content=knowledge,
                    metadata={
                        "source": "agent_experience",
                        "timestamp": datetime.now().isoformat(),
                        "query_type": self._classify_query(user_query)
                    }
                )

        # 4. Aplicar estrategia de olvido periódicamente
        if self.working_memory.message_count() > 100:
            self._consolidate_memories()

    def _assess_importance(self, query: str, success: bool) -> float:
        """Evaluar qué tan importante es recordar esta interacción"""
        importance = 0.5  # Base

        # Los fracasos son más importantes de recordar (aprendemos de errores)
        if not success:
            importance += 0.3

        # Las consultas que involucran herramientas son más significativas
        if any(keyword in query.lower()
               for keyword in ["error", "urgente", "producción", "crítico"]):
            importance += 0.2

        return min(1.0, importance)

    def _consolidate_memories(self):
        """
        Consolidar la working memory:
        mover información importante a memoria a largo plazo
        y olvidar lo trivial.
        """
        old_messages = self.working_memory.get_old_messages(
            older_than_messages=50
        )

        for msg in old_messages:
            # Evaluar si vale la pena guardar en memoria a largo plazo
            if self._assess_importance(msg["content"], True) > 0.6:
                self.semantic_memory.store(
                    content=msg["content"],
                    metadata={"source": "consolidated", "role": msg["role"]}
                )

        # Eliminar los mensajes antiguos de la working memory
        self.working_memory.trim_old(keep_recent=50)
```

Este sistema no es perfecto (ninguno lo es), pero ilustra cómo los diferentes componentes se coordinan: la working memory maneja lo inmediato, la memoria episódica registra experiencias, la memoria semántica acumula conocimiento, y las estrategias de olvido evitan que todo se desborde.

Un detalle importante: al inyectar memorias recuperadas en la ventana de contexto, respeta un presupuesto de tokens. Si tu ventana es de 128K tokens y ya tienes el system prompt, las herramientas y el historial de conversación, el espacio disponible para memorias puede ser sorprendentemente pequeño. Mide cuántos tokens consumen tus memorias inyectadas y establece un límite explícito para evitar desplazar información más relevante del contexto actual.

## Herramientas de memoria en producción

Antes de implementar memoria desde cero, vale la pena conocer las herramientas disponibles en 2026. El ecosistema ha madurado considerablemente:

- **[Mem0](https://mem0.ai/)**: una capa de memoria para agentes que abstrae el almacenamiento vectorial, la extracción de hechos y la gestión de relevancia. Se integra con los principales frameworks y proveedores de LLMs.
- **[Zep](https://www.getzep.com/)**: enfocado en memoria conversacional con extracción automática de entidades y hechos. Ofrece APIs de búsqueda semántica y temporal.
- **LangGraph Memory**: el sistema de checkpointing y memory store integrado en LangGraph, con persistencia nativa y soporte para memoria a largo plazo entre sesiones.
- **Funcionalidades nativas de los proveedores**: tanto Anthropic como OpenAI y Google ofrecen features de memoria a nivel de API que simplifican casos de uso comunes.

La decisión entre construir tu propio sistema de memoria o usar una herramienta existente depende del volumen, la complejidad de tu caso de uso y cuánto control necesitas. Para la mayoría de los proyectos, empezar con una herramienta existente y migrar a una solución custom solo cuando encuentres limitaciones concretas es el camino más pragmático.

## Conclusión: la memoria como ventaja competitiva

El manejo de memoria y estado es el problema que separa a los agentes de demostración de los agentes de producción. Un agente sin memoria está condenado a repetir errores, a tratar a cada usuario como un extraño y a desperdiciar tokens redescubriendo información que ya tenía.

Las lecciones clave que hemos explorado son:

1. **La taxonomía de la memoria humana es un marco de diseño útil**: working memory, episódica, semántica y procedimental mapean directamente a patrones de implementación.

2. **El estado debe ser explícito**: las máquinas de estado hacen que los agentes sean depurables, monitoreables y recuperables. Como aprendimos en la serie de [A Philosophy of Software Design](/posts/a-philosophy-of-software-design-los-modulos-deben-ser-profundos/), la complejidad se combate con interfaces claras y módulos profundos. El estado explícito es una forma de reducir complejidad.

3. **Los sistemas operativos ya resolvieron muchos de estos problemas**: paginación, caching, control de concurrencia. La idea de MemGPT de aplicar memoria virtual a LLMs es solo el principio.

4. **Olvidar es tan importante como recordar**: las estrategias de olvido inspiradas en caché (LRU, TTL, importance-based) son esenciales para mantener la calidad de la memoria.

5. **La concurrencia en multi-agente requiere los mismos patrones que en software clásico**: locks, CAS, message passing. Los problemas no son nuevos; las soluciones tampoco.

El campo avanza rápidamente. Sistemas como MemGPT, frameworks como LangGraph y la investigación en agentes generativos están convergiendo hacia arquitecturas de memoria cada vez más sofisticadas. Pero los fundamentos, como siempre en la ingeniería de software, vienen de décadas de investigación en sistemas operativos, bases de datos y sistemas distribuidos.

La próxima vez que construyas un agente, no empieces por el prompt ni por la selección del modelo. Empieza por la pregunta: **¿cómo va a recordar?**

## Referencias y fuentes clave

- **Park, J. S., et al. (2023)**. "Generative Agents: Interactive Simulacra of Human Behavior". Stanford University. El paper fundacional sobre agentes generativos con sistemas de memoria basados en recencia, importancia y relevancia.
- **Packer, C., et al. (2023)**. "MemGPT: Towards LLMs as Operating Systems". UC Berkeley. Introduce la analogía entre paginación en sistemas operativos y gestión de ventana de contexto en LLMs.
- **Miller, G. A. (1956)**. "The Magical Number Seven, Plus or Minus Two". Psychological Review. El trabajo clásico sobre los límites de la memoria de trabajo humana.
- **Cowan, N. (2001)**. "The Magical Number 4 in Short-Term Memory". Behavioral and Brain Sciences. Revisión del límite de Miller, proponiendo un límite más bajo de 4 ± 1 elementos.
- **Wei, J., et al. (2022)**. "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models". Google Research. Técnicas de razonamiento paso a paso que impactan cómo los agentes procesan información en su memoria de trabajo.
- **LangGraph Documentation (2024-2026)**. Framework de grafos de estado para agentes con checkpointing nativo y gestión de estado declarativa.
- **Tulving, E. (1972)**. "Episodic and Semantic Memory". La distinción clásica entre tipos de memoria que fundamenta las categorías usadas en este artículo.
- **Tanenbaum, A. S. (2014)**. "Modern Operating Systems". Los algoritmos de reemplazo de páginas (LRU, LFU, Clock) que inspiran las estrategias de olvido en agentes.
- **Lamport, L. (1978)**. "Time, Clocks, and the Ordering of Events in a Distributed System". Fundamentos teóricos de consistencia en sistemas distribuidos, aplicables a la memoria compartida en sistemas multi-agente.
