# Capitulo 4: Memoria y Estado -- El Problema Mas Dificil

> "Un agente sin memoria es un empleado con amnesia que llega cada manana sin recordar nada. Puede razonar, puede resolver problemas, puede usar herramientas. Pero no sabe que proyectos tiene pendientes, que errores cometio la semana pasada ni que preferencias tiene el cliente con el que esta hablando. Cada interaccion empieza desde cero."

---

En el capitulo anterior exploramos como la ventana de contexto es la RAM de tu agente: un recurso finito, caro y cuya mala gestion degrada silenciosamente la calidad del sistema. Vimos estrategias para comprimir y gestionar ese espacio. Pero hay un problema mas profundo que la ventana de contexto no resuelve por si sola: **la persistencia**.

Cuando la ventana de contexto se cierra --porque la sesion termina, el presupuesto de tokens se agota o simplemente el usuario cierra la pestana--, todo lo que el agente "sabia" desaparece. Las memorias, las decisiones, los patrones aprendidos: todo se evapora. Es como si un medico revisara tu historial clinico cada consulta, pero al final de la cita lo tirara a la basura.

Este problema no es solo tecnico. Es el problema que separa a los agentes de demostracion de los agentes de produccion. Un agente que no recuerda es una herramienta desechable. Un agente que recuerda es un asistente que mejora con el tiempo.

En este capitulo vamos a confrontar el problema de la memoria desde sus fundamentos. Exploraremos la taxonomia de la memoria humana y como mapea a decisiones de arquitectura. Implementaremos sistemas de persistencia y recuperacion con codigo Python real. Y abordaremos un aspecto que muchos ignoran: el arte de olvidar, porque un agente que recuerda todo se ahoga en ruido.

---

## 4.1 Tipos de memoria: la taxonomia cognitiva aplicada a agentes

Para disenar un sistema de memoria para agentes, conviene primero mirar como funciona la memoria en los seres humanos. La neurociencia cognitiva ha identificado varios tipos de memoria que trabajan en conjunto, y esta taxonomia resulta directamente util para disenar sistemas de memoria artificial. No es una analogia perfecta --el cerebro no es una base de datos--, pero nos da un marco de diseno genuinamente practico.

### Memoria de trabajo (*working memory*): la ventana de contexto activa

La **memoria de trabajo** en humanos es ese espacio mental limitado donde mantienes la informacion que estas procesando activamente. Cuando haces una multiplicacion mental, los numeros que estas manipulando estan en tu memoria de trabajo. George Miller propuso en 1956 que podemos mantener aproximadamente 7 elementos (mas o menos 2) simultaneamente, aunque investigaciones posteriores, como las de Cowan (2001), sugieren un limite mas bajo, cercano a 4 elementos.

En un agente basado en LLM, la memoria de trabajo **es** la ventana de contexto. Es toda la informacion que el modelo puede "ver" en un momento dado: el prompt del sistema, el historial de conversacion, las herramientas disponibles y cualquier dato que hayamos inyectado. Con modelos como GPT-4o, Claude o Gemini, esta ventana puede ser de 128K a 1M tokens, pero sigue siendo finita y costosa.

El problema fundamental es que, a diferencia de la memoria de trabajo humana que puede "comprimir" informacion (piensas en "mi direccion" en vez de recordar cada caracter), la ventana de contexto es literal: cada palabra ocupa espacio. No hay compresion nativa. Si quieres comprimir, tienes que implementarla tu, como vimos en el Capitulo 3 con las estrategias de resumen progresivo y memoria jerarquica.

### Memoria a corto plazo: dentro de una sesion

La **memoria a corto plazo** en un agente corresponde a todo lo que el agente recuerda dentro de una sesion de interaccion. Incluye el historial de la conversacion, los resultados de herramientas que ha usado, las decisiones que ha tomado y su razonamiento.

En la practica, esta memoria suele implementarse como una lista de mensajes que crece con cada interaccion:

```python
class ShortTermMemory:
    """Memoria a corto plazo: todo lo que el agente recuerda
    dentro de una sesion."""

    def __init__(self, max_tokens: int = 100_000):
        self.messages: list[dict] = []
        self.max_tokens = max_tokens
        self.current_tokens = 0

    def add(self, role: str, content: str):
        tokens = self._count_tokens(content)
        while self.current_tokens + tokens > self.max_tokens:
            self._evict_oldest()
        self.messages.append({"role": role, "content": content})
        self.current_tokens += tokens

    def _evict_oldest(self):
        """Estrategia mas simple: eliminar el mensaje mas antiguo."""
        if self.messages:
            removed = self.messages.pop(0)
            self.current_tokens -= self._count_tokens(removed["content"])

    def _count_tokens(self, text: str) -> int:
        # Estimacion: ~4 caracteres por token en espanol.
        # Para presupuestos precisos, usa tiktoken o el
        # tokenizer de tu modelo.
        return len(text) // 4

    def get_recent(self, max_tokens: int) -> list[dict]:
        """Retorna los mensajes mas recientes que caben en el presupuesto."""
        result = []
        tokens = 0
        for msg in reversed(self.messages):
            msg_tokens = self._count_tokens(msg["content"])
            if tokens + msg_tokens > max_tokens:
                break
            result.insert(0, msg)
            tokens += msg_tokens
        return result

    def message_count(self) -> int:
        return len(self.messages)
```

El problema aqui es sutil pero importante: cuando eliminas mensajes antiguos para hacer espacio, puedes perder contexto critico. Imagina un agente de soporte que al inicio de la conversacion recibio la informacion de que el usuario es un cliente enterprise con SLA prioritario. Si esa informacion se elimina por ser "antigua", el agente podria empezar a dar respuestas genericas. Es el mismo problema del "Lost in the Middle" que vimos en el capitulo anterior, pero agravado por la eliminacion activa de informacion.

### Memoria a largo plazo: entre sesiones

La **memoria a largo plazo** permite que un agente recuerde informacion entre sesiones completamente diferentes. Es la diferencia entre un asistente que te trata como un extrano cada vez que hablas con el y uno que recuerda tus preferencias, tu contexto y tu historial.

En los humanos, la memoria a largo plazo se subdivide en tres categorias que resultan muy utiles para el diseno de agentes:

**Memoria episodica**: recuerdos de experiencias especificas. "La ultima vez que el usuario pidio un reporte de ventas, prefirio formato CSV". Son como snapshots de interacciones pasadas con contexto temporal. En un agente, se implementan tipicamente como registros indexados por tiempo con metadatos sobre el resultado de la interaccion.

**Memoria semantica**: conocimiento general abstracto, separado de experiencias especificas. "Los reportes de ventas se generan con la herramienta X y requieren acceso a la base de datos Y". Es conocimiento que el agente ha adquirido pero que ya no esta atado a un episodio particular. En la practica, se implementa con bases de datos vectoriales o grafos de conocimiento.

**Memoria procedimental**: conocimiento de como hacer cosas. "Para generar un reporte, primero consulto la API de ventas, luego formateo los datos, luego genero el PDF". En sistemas de agentes, esto se traduce en workflows aprendidos, plantillas de accion o incluso codigo generado dinamicamente que el agente reutiliza.

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
    """Una unidad de memoria a largo plazo.

    Incluye metadatos para scoring de relevancia
    y mecanismos de decaimiento temporal.
    """
    content: str
    memory_type: MemoryType
    timestamp: datetime
    importance: float  # 0.0 a 1.0
    access_count: int = 0
    last_accessed: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)

    def calculate_decayed_importance(
        self, decay_rate: float = 0.01
    ) -> float:
        """Calcula la importancia con decaimiento temporal
        SIN mutar el objeto. Util para scoring y ordenamiento."""
        hours_since_access = (
            datetime.now() - self.last_accessed
        ).total_seconds() / 3600
        return self.importance * (1 - decay_rate) ** hours_since_access

    def access(self):
        """Registra un acceso a esta memoria (muta el objeto)."""
        self.access_count += 1
        self.last_accessed = datetime.now()
```

### El mapeo completo: taxonomia humana a decisiones de arquitectura

La analogia con la memoria humana no es solo pedagogica: nos da un marco de diseno genuinamente util. Veamos el mapeo completo:

| Tipo de memoria | Equivalente en agente | Implementacion tipica | Persistencia | Costo |
|---|---|---|---|---|
| Memoria de trabajo | Ventana de contexto | Prompt + historial | Ninguna (por request) | Alto (tokens de LLM) |
| Corto plazo | Historial de sesion | Lista de mensajes en memoria | Sesion | Bajo |
| Episodica | Registro de experiencias | Key-value store (SQLite, Redis) | Permanente | Bajo-medio |
| Semantica | Base de conocimiento | Base de datos vectorial | Permanente | Medio-alto |
| Procedimental | Workflows aprendidos | Archivos de configuracion, DAGs | Permanente | Bajo |

La decision de que tipo de memoria implementar depende de tu caso de uso. Un chatbot de soporte al cliente necesita memoria a corto plazo solida y memoria episodica para recordar interacciones previas del mismo usuario. Un agente de investigacion necesita memoria semantica fuerte para acumular conocimiento sobre un dominio. Un agente de desarrollo de software necesita memoria procedimental para recordar las convenciones del proyecto.

No todo agente necesita los cinco tipos. Empieza por la memoria de trabajo (obligatoria, es la ventana de contexto) y la memoria a corto plazo (el historial de sesion). Agrega los demas tipos solo cuando el caso de uso lo justifique.

---

## 4.2 El estado como ciudadano de primera clase

Si la memoria es lo que el agente "sabe", el **estado** es "en que punto se encuentra". Y gestionar el estado correctamente es fundamental para construir agentes confiables. Piensalo asi: cuando pausas un videojuego y lo retomas tres dias despues, esperas estar exactamente donde lo dejaste. Los agentes en produccion necesitan la misma capacidad.

### State machines para agentes

Una de las lecciones mas importantes al pasar de agentes teoricos a agentes en produccion es que los agentes confiables necesitan estados bien definidos. Un agente que "simplemente razona en bucle" es dificil de depurar, de monitorear y de recuperar cuando algo falla.

Las **maquinas de estado finitas** (FSMs) son uno de los formalismos mas antiguos de la computacion, y resulta que son perfectas para modelar el comportamiento de agentes:

```python
from enum import Enum, auto
from datetime import datetime


class AgentState(Enum):
    IDLE = auto()
    ANALYZING = auto()
    PLANNING = auto()
    EXECUTING = auto()
    WAITING_FOR_TOOL = auto()
    REVIEWING = auto()
    ERROR_RECOVERY = auto()
    COMPLETED = auto()


class InvalidTransitionError(Exception):
    pass


class AgentStateMachine:
    """Maquina de estados para un agente de IA.

    Define transiciones legales entre estados.
    Rechaza transiciones invalidas con una excepcion,
    lo que hace que los bugs sean ruidosos en lugar
    de silenciosos.
    """
    TRANSITIONS: dict[AgentState, set[AgentState]] = {
        AgentState.IDLE: {AgentState.ANALYZING},
        AgentState.ANALYZING: {
            AgentState.PLANNING,
            AgentState.ERROR_RECOVERY,
        },
        AgentState.PLANNING: {
            AgentState.EXECUTING,
            AgentState.ANALYZING,
        },
        AgentState.EXECUTING: {
            AgentState.WAITING_FOR_TOOL,
            AgentState.REVIEWING,
            AgentState.ERROR_RECOVERY,
        },
        AgentState.WAITING_FOR_TOOL: {
            AgentState.EXECUTING,
            AgentState.ERROR_RECOVERY,
        },
        AgentState.REVIEWING: {
            AgentState.COMPLETED,
            AgentState.PLANNING,  # Volver a planificar si no esta satisfecho
        },
        AgentState.ERROR_RECOVERY: {
            AgentState.ANALYZING,
            AgentState.IDLE,
        },
    }

    def __init__(self):
        self.current_state = AgentState.IDLE
        self.state_history: list[tuple[AgentState, datetime]] = []

    def transition(self, new_state: AgentState):
        allowed = self.TRANSITIONS.get(self.current_state, set())
        if new_state not in allowed:
            raise InvalidTransitionError(
                f"No se puede ir de {self.current_state} a {new_state}. "
                f"Transiciones permitidas: {allowed}"
            )
        self.state_history.append((self.current_state, datetime.now()))
        self.current_state = new_state

    def time_in_current_state(self) -> float:
        """Segundos en el estado actual. Util para detectar agentes
        'atascados' en un estado por demasiado tiempo."""
        if not self.state_history:
            return 0.0
        _, last_transition = self.state_history[-1]
        return (datetime.now() - last_transition).total_seconds()
```

Esta estructura explicita tiene beneficios enormes: puedes saber exactamente en que punto esta un agente, puedes validar que las transiciones son legales, puedes generar metricas por estado ("el 80% del tiempo lo pasa en WAITING_FOR_TOOL") y puedes detectar cuando un agente esta "atascado" en un ciclo (lleva 5 minutos en ERROR_RECOVERY sin progresar).

### Checkpointing: guardar para resumir

El **checkpointing** es la practica de guardar el estado completo de un agente en un momento dado para poder reanudarlo despues. Es un concepto que viene directamente de los sistemas operativos, donde los procesos se suspenden y reanudan constantemente, y del entrenamiento de redes neuronales, donde guardar checkpoints periodicamente es practica estandar para no perder horas de computo ante un fallo.

Un buen sistema de checkpointing debe capturar:

1. **El estado de la maquina de estados** (en que paso esta)
2. **La memoria de trabajo** (que tiene en contexto)
3. **La memoria a corto plazo** (el historial de la sesion)
4. **Los resultados intermedios** (outputs de herramientas, datos parciales)
5. **Los metadatos de ejecucion** (cuantos tokens ha consumido, tiempo transcurrido)

```python
import json
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class AgentCheckpoint:
    """Snapshot completo del estado de un agente."""
    agent_id: str
    state: AgentState
    working_memory: dict
    short_term_memory: list[dict]
    intermediate_results: list[dict]
    metadata: dict
    timestamp: datetime = field(default_factory=datetime.now)

    def save(self, checkpoint_dir: Path) -> Path:
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        filepath = (
            checkpoint_dir
            / f"{self.agent_id}_{self.timestamp.isoformat()}.json"
        )
        filepath.write_text(
            json.dumps(self._serialize(), indent=2, default=str)
        )
        return filepath

    def _serialize(self) -> dict:
        return {
            "agent_id": self.agent_id,
            "state": self.state.name,
            "working_memory": self.working_memory,
            "short_term_memory": self.short_term_memory,
            "intermediate_results": self.intermediate_results,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def load(cls, filepath: Path) -> "AgentCheckpoint":
        data = json.loads(filepath.read_text())
        return cls(
            agent_id=data["agent_id"],
            state=AgentState[data["state"]],
            working_memory=data["working_memory"],
            short_term_memory=data["short_term_memory"],
            intermediate_results=data["intermediate_results"],
            metadata=data["metadata"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )
```

### La trampa de los side effects

El checkpointing de agentes es, en realidad, un problema de transacciones distribuidas disfrazado. Puedes revertir el estado interno del agente (su memoria, su posicion en la maquina de estados), pero **no puedes revertir las acciones externas** que ya ejecuto: emails enviados, pagos procesados, APIs llamadas, mensajes publicados.

Por eso, en produccion, tu estrategia de checkpointing debe clasificar las acciones del agente en dos categorias:

- **Reversibles**: lecturas de base de datos, busquedas, calculos internos. Se pueden deshacer sin consecuencias.
- **Irreversibles**: envio de emails, transferencias de dinero, publicaciones, llamadas a APIs externas con efectos. Estas requieren confirmacion humana *antes* de ejecutarse, o al menos un mecanismo de compensacion.

El patron es similar al de las transacciones en bases de datos, pero con una limitacion importante: los principios ACID solo aplican completamente dentro de los limites de tu sistema. Los side effects externos estan fuera de tu control transaccional. Esto conecta directamente con el Agent Harness que veremos en el Capitulo 5, donde el patron Human-in-the-Loop actua como barrera antes de que el agente ejecute acciones irreversibles.

---

## 4.3 Persistencia y recuperacion: donde viven las memorias

Una vez que entendemos los tipos de memoria y la importancia del estado, la pregunta natural es: como persistimos todo esto de forma eficiente? Aqui convergen tecnicas de bases de datos, recuperacion de informacion y sistemas operativos.

### Bases de datos vectoriales para memoria semantica

La memoria semantica (conocimiento general) se beneficia enormemente de las **bases de datos vectoriales**. La idea es simple pero potente: cada pieza de conocimiento se convierte en un vector numerico (embedding) que captura su significado semantico. Cuando el agente necesita recordar algo relevante, busca los vectores mas cercanos a su consulta actual.

En el Capitulo 3 ya vimos el patron RAG (Retrieval-Augmented Generation). Pero en el contexto de memoria para agentes, el RAG toma un matiz diferente: no solo recuperas documentos externos, sino **las propias experiencias y conocimientos del agente**.

```python
import chromadb
from sentence_transformers import SentenceTransformer


class SemanticMemory:
    """Memoria semantica basada en embeddings y busqueda vectorial.

    Usa ChromaDB para almacenamiento y SentenceTransformers
    para generar embeddings. En produccion, considera pgvector
    si ya usas PostgreSQL, o Pinecone/Weaviate si necesitas
    escala o busqueda hibrida.
    """

    def __init__(self, collection_name: str = "agent_memory"):
        self.client = chromadb.PersistentClient(
            path="./agent_memory_db"
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")

    def store(self, content: str, metadata: dict):
        """Guarda una memoria con su embedding."""
        embedding = self.encoder.encode(content).tolist()
        self.collection.add(
            documents=[content],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[f"mem_{datetime.now().timestamp()}"],
        )

    def recall(
        self, query: str, n_results: int = 5
    ) -> list[dict]:
        """Recupera las memorias mas relevantes para la consulta."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
        )
        return [
            {
                "content": doc,
                "metadata": meta,
                "distance": dist,
            }
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            )
        ]

    def forget(self, older_than_hours: int = 720):
        """Elimina memorias mas antiguas que el umbral dado."""
        cutoff = (
            datetime.now()
            - timedelta(hours=older_than_hours)
        ).timestamp()
        # ChromaDB soporta filtrado por metadatos
        old_memories = self.collection.get(
            where={"timestamp": {"$lt": cutoff}}
        )
        if old_memories["ids"]:
            self.collection.delete(ids=old_memories["ids"])
```

### Eligiendo tu base de datos vectorial

La eleccion de la base de datos vectorial es una decision arquitectonica significativa. En 2026, el ecosistema ha madurado y hay opciones claras para cada caso:

**PostgreSQL + pgvector**: si ya usas PostgreSQL y tienes menos de 5 millones de vectores, pgvector es la opcion mas pragmatica. No introduces un nuevo componente en tu infraestructura, mantienes las garantias ACID que ya conoces y la complejidad operacional es minima. La limitacion principal es el rendimiento: a partir de unos pocos millones de vectores, los indices HNSW empiezan a consumir cantidades significativas de RAM y la latencia de busqueda se degrada.

**Pinecone**: la opcion mas simple si quieres un servicio gestionado. No tienes que pensar en infraestructura, escala automaticamente y el rendimiento es consistente. La desventaja es el costo y la dependencia de un vendor. Para equipos que prefieren invertir tiempo en la logica de negocio en lugar de en operaciones de bases de datos, es una eleccion solida.

**Weaviate**: destaca por su busqueda hibrida (combina busqueda vectorial con busqueda de texto completo), lo cual es particularmente util para memoria de agentes donde a veces necesitas buscar por significado semantico y otras veces por coincidencia exacta de terminos. Es open source y puede desplegarse on-premise.

**ChromaDB**: ideal para prototipos y proyectos pequenos. Se embebe directamente en tu aplicacion Python sin necesidad de un servidor externo. Su principal limitacion es que no escala bien para volumen de produccion con muchos usuarios concurrentes.

La regla general: **empieza con lo mas simple** (pgvector si ya tienes Postgres, ChromaDB si no) y migra a una solucion especializada solo cuando midas limitaciones concretas de rendimiento o escala.

### Almacenes clave-valor para memoria episodica

La memoria episodica se organiza mejor en **key-value stores** o bases de datos relacionales simples porque sus patrones de acceso son diferentes: necesitas buscar por tiempo, por tipo de evento, por resultado. Redis, DynamoDB o incluso SQLite funcionan bien aqui:

```python
import sqlite3
from contextlib import contextmanager


class EpisodicMemory:
    """Memoria episodica: registros de experiencias del agente
    indexados por tipo de evento y tiempo."""

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
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp
                ON episodes(timestamp)
            """)

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def record_episode(
        self,
        event_type: str,
        context: str,
        action: str,
        outcome: str,
        success: bool,
        importance: float = 0.5,
    ):
        """Registra un episodio en la memoria."""
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO episodes "
                "(timestamp, event_type, context, action_taken, "
                "outcome, success, importance) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    datetime.now().isoformat(),
                    event_type,
                    context,
                    action,
                    outcome,
                    success,
                    importance,
                ),
            )

    def recall_similar_situations(
        self, event_type: str, limit: int = 5
    ) -> list[dict]:
        """Que hizo el agente en situaciones similares?"""
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT * FROM episodes WHERE event_type = ? "
                "ORDER BY importance DESC, timestamp DESC LIMIT ?",
                (event_type, limit),
            )
            columns = [d[0] for d in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def recall_failures(self, limit: int = 10) -> list[dict]:
        """Recupera los fracasos recientes. Los errores son
        frecuentemente mas utiles que los exitos."""
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT * FROM episodes WHERE success = 0 "
                "ORDER BY timestamp DESC LIMIT ?",
                (limit,),
            )
            columns = [d[0] for d in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
```

### Grafos de conocimiento para relaciones complejas

Cuando la memoria del agente involucra relaciones complejas entre entidades --"el cliente X trabaja para la empresa Y, que tiene contrato con el equipo Z"-- las bases de datos vectoriales no son suficientes. Ahi es donde entran los **grafos de conocimiento**.

Un grafo de conocimiento modela entidades como nodos y relaciones como aristas. La ventaja sobre las bases de datos vectoriales es que preserva la estructura relacional de la informacion, lo que permite responder preguntas como "cuales son todos los clientes de la empresa Y que han reportado problemas con el producto Z?" sin depender de la similitud semantica.

Bases de datos como Neo4j permiten construir estos grafos y consultarlos con Cypher, un lenguaje de consultas orientado a grafos. El patron **GraphRAG** --combinar busqueda en grafos de conocimiento con generacion por LLM-- ha ganado traccion significativa porque produce respuestas mas precisas y trazables que el RAG vectorial puro para ciertos tipos de consultas.

La desventaja principal es la complejidad operacional. Mantener un grafo de conocimiento actualizado requiere un pipeline de extraccion de entidades y relaciones, que en si mismo es un problema de IA. Para la mayoria de los agentes, la combinacion de memoria episodica (SQLite) + memoria semantica (vectores) es suficiente. Los grafos de conocimiento entran en juego cuando las relaciones entre entidades son centrales para la tarea del agente.

---

## 4.4 MemGPT: paginacion de memoria inspirada en sistemas operativos

Una de las ideas mas elegantes en memoria para agentes viene de **MemGPT** [Packer et al., 2023], un sistema que aplica conceptos de sistemas operativos a la gestion de memoria de LLMs. La analogia es directa y poderosa:

- **La ventana de contexto del LLM** es como la **RAM** de un computador: rapida pero limitada.
- **La memoria externa** (bases de datos, archivos) es como el **disco duro**: abundante pero lenta de acceder.
- **MemGPT** implementa un sistema de **memoria virtual** con paginacion, exactamente como lo hace un sistema operativo.

La innovacion clave de MemGPT es que el propio LLM decide *activamente* cuando hacer page-in y page-out, usando herramientas (function calls) para gestionar su propia memoria. En lugar de depender de un sistema externo que decide que informacion inyectar, el agente tiene herramientas como `memory_search`, `memory_insert` y `memory_replace` que le permiten gestionar su contexto de forma autonoma.

El sistema operativo resuelve el problema de tener mas datos que RAM mediante la **paginacion**: divide la memoria en bloques (paginas) y las mueve entre RAM y disco segun se necesiten. MemGPT hace exactamente lo mismo con la ventana de contexto:

```python
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class MemoryPage:
    """Una pagina de memoria que puede moverse entre
    contexto activo y almacenamiento externo."""
    content: str
    page_id: str
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    importance: float = 0.5

    def access(self):
        self.last_accessed = datetime.now()
        self.access_count += 1


class MemGPTStyleMemory:
    """Implementacion simplificada del patron MemGPT.

    La ventana de contexto actua como RAM; el almacenamiento
    externo actua como disco. Las paginas se mueven entre
    ambos espacios segun politicas de eviccion.

    Nota: en MemGPT real, el LLM invoca estas operaciones
    como herramientas (function calls). Aqui las controlamos
    externamente para ilustrar el mecanismo.
    """

    def __init__(
        self,
        context_window_tokens: int,
        page_size_tokens: int = 2000,
    ):
        self.context_window_tokens = context_window_tokens
        self.page_size_tokens = page_size_tokens
        # "RAM" -- paginas activas en la ventana de contexto
        self.active_pages: list[MemoryPage] = []
        # "Disco" -- almacenamiento externo (en produccion,
        # esto seria una base de datos)
        self.external_pages: list[MemoryPage] = []

    def page_in(self, query: str) -> list[MemoryPage]:
        """Cargar paginas relevantes del almacenamiento externo
        al contexto activo. Equivalente a un page fault en un SO."""
        relevant = self._search_external(query)
        loaded = []
        for page in relevant:
            if not self._context_has_space():
                self._evict_lru()
            self.external_pages.remove(page)
            self.active_pages.append(page)
            page.access()
            loaded.append(page)
        return loaded

    def page_out(self, page: MemoryPage):
        """Mover una pagina del contexto al almacenamiento externo.
        Equivalente a escribir una pagina a disco."""
        if page in self.active_pages:
            self.active_pages.remove(page)
            self.external_pages.append(page)

    def _evict_lru(self):
        """LRU: expulsar la pagina menos recientemente usada.
        Exactamente como en un sistema operativo."""
        if self.active_pages:
            lru_page = min(
                self.active_pages,
                key=lambda p: p.last_accessed,
            )
            self.page_out(lru_page)

    def _context_has_space(self) -> bool:
        total_tokens = sum(
            len(p.content) // 4 for p in self.active_pages
        )
        return total_tokens + self.page_size_tokens <= self.context_window_tokens

    def _search_external(self, query: str) -> list[MemoryPage]:
        """Busca paginas relevantes en almacenamiento externo.
        En produccion, esto usaria busqueda vectorial."""
        # Simplificado: retorna las paginas mas importantes
        sorted_pages = sorted(
            self.external_pages,
            key=lambda p: p.importance,
            reverse=True,
        )
        return sorted_pages[:3]

    def get_active_context(self) -> str:
        """Construye el contexto a partir de las paginas activas."""
        return "\n\n".join(p.content for p in self.active_pages)
```

Esta idea es poderosa porque nos permite razonar sobre la memoria de agentes usando **decadas de investigacion en sistemas operativos**. Algoritmos como LRU (Least Recently Used), LFU (Least Frequently Used) y Clock, que se ensenan en cualquier curso de sistemas operativos, aplican directamente aqui. No estamos inventando algo nuevo; estamos aplicando soluciones probadas a un problema con la misma estructura fundamental.

---

## 4.5 El arte de olvidar: por que un agente que recuerda todo se ahoga

Aqui llegamos a lo que considero el nucleo mas contraintuitivo del problema de la memoria en agentes: **no todo debe recordarse, y decidir que es importante es en si mismo un problema de IA**.

Un ser humano no recuerda cada segundo de su vida. Tu cerebro constantemente decide que consolidar en memoria a largo plazo y que descartar. Los recuerdos con carga emocional fuerte se consolidan mas facilmente; los detalles triviales se olvidan. Este proceso de **filtrado** es esencial: sin el, estarias abrumado por informacion irrelevante. Jorge Luis Borges lo imagino en "Funes el memorioso": un personaje que recuerda absolutamente todo y cuya vida se convierte en una tortura de detalles inmanejables.

Los agentes enfrentan exactamente el mismo problema. Si un agente recuerda todo, su memoria se vuelve ruidosa y las busquedas de informacion relevante pierden precision. La base de datos vectorial empieza a devolver memorias tangencialmente relacionadas en lugar de las verdaderamente utiles. Si recuerda muy poco, pierde contexto valioso. El balance es delicado.

### Relevance scoring: la funcion que decide que recordar

Una estrategia central es asignar una **puntuacion de relevancia** a cada pieza de informacion y usar esa puntuacion para decidir que guardar y que recuperar. Los factores que influyen en la relevancia son los mismos que identificaron Park et al. en su influyente paper "Generative Agents" [Park et al., 2023], donde simularon agentes que vivian en un pueblo virtual:

```python
def calculate_relevance(
    memory_entry: MemoryEntry,
    current_context: str,
    current_time: datetime,
    encoder=None,
) -> float:
    """Calcula la relevancia de una memoria dado el contexto actual.

    Combina cuatro factores ponderados, siguiendo el patron
    de Park et al. (2023):
    - Similitud semantica con la tarea actual
    - Recencia temporal
    - Importancia intrinseca
    - Frecuencia de acceso
    """
    # 1. Similitud semantica con el contexto actual
    if encoder is not None:
        mem_vec = encoder.encode(memory_entry.content)
        ctx_vec = encoder.encode(current_context)
        dot = sum(a * b for a, b in zip(mem_vec, ctx_vec))
        norm_m = sum(a ** 2 for a in mem_vec) ** 0.5
        norm_c = sum(a ** 2 for a in ctx_vec) ** 0.5
        semantic_similarity = (
            dot / (norm_m * norm_c) if norm_m and norm_c else 0.0
        )
    else:
        semantic_similarity = 0.5  # Fallback sin encoder

    # 2. Recencia: las memorias recientes son mas relevantes
    hours_ago = (
        current_time - memory_entry.timestamp
    ).total_seconds() / 3600
    recency_score = 1.0 / (1.0 + 0.1 * hours_ago)

    # 3. Importancia intrinseca (asignada al crear la memoria)
    importance = memory_entry.calculate_decayed_importance()

    # 4. Frecuencia de acceso
    access_score = min(1.0, memory_entry.access_count / 10.0)

    # Combinacion ponderada
    relevance = (
        0.4 * semantic_similarity
        + 0.25 * recency_score
        + 0.2 * importance
        + 0.15 * access_score
    )
    return relevance
```

Los pesos (0.4, 0.25, 0.2, 0.15) no son universales. Dependen de tu caso de uso. Un agente de soporte al cliente podria ponderar mas la recencia (las interacciones recientes con este usuario son las mas relevantes). Un agente de investigacion podria ponderar mas la similitud semantica (lo que importa es el tema, no cuando lo aprendio). Trata estos pesos como hiperparametros que ajustas con datos reales de tu sistema.

### Estrategias de olvido: inspiracion desde los sistemas de cache

Tan importante como recordar es **olvidar**. Aqui podemos tomar prestados patrones de los sistemas de cache, que llevan decadas resolviendo exactamente este problema:

```python
from datetime import timedelta


class ForgettingPolicy:
    """Politicas de olvido inspiradas en sistemas de cache.

    Cada politica tiene trade-offs diferentes.
    La hibrida suele ser la mas efectiva en la practica.
    """

    @staticmethod
    def lru(
        memories: list[MemoryEntry], max_size: int
    ) -> list[MemoryEntry]:
        """Least Recently Used: elimina las memorias que llevan
        mas tiempo sin accederse.

        Ventaja: simple, funciona bien si el patron de acceso
        es predecible.
        Desventaja: puede eliminar informacion importante que
        simplemente no ha sido relevante recientemente.
        """
        sorted_by_access = sorted(
            memories,
            key=lambda m: m.last_accessed,
            reverse=True,
        )
        return sorted_by_access[:max_size]

    @staticmethod
    def ttl(
        memories: list[MemoryEntry],
        max_age_hours: int = 720,
    ) -> list[MemoryEntry]:
        """Time To Live: cada memoria tiene una fecha de expiracion.

        Ventaja: predecible, util para informacion con vigencia
        limitada (estado de un sistema externo).
        Desventaja: no funciona bien para conocimiento atemporal.
        """
        cutoff = datetime.now() - timedelta(hours=max_age_hours)
        return [m for m in memories if m.timestamp > cutoff]

    @staticmethod
    def importance_based(
        memories: list[MemoryEntry],
        threshold: float = 0.1,
    ) -> list[MemoryEntry]:
        """Solo retiene memorias cuya importancia (con decaimiento
        temporal aplicado) supera un umbral.

        Ventaja: preserva lo importante sin importar la edad.
        Desventaja: requiere un buen sistema de scoring.
        """
        return [
            m
            for m in memories
            if m.calculate_decayed_importance() >= threshold
        ]

    @staticmethod
    def hybrid(
        memories: list[MemoryEntry],
        max_size: int,
        min_importance: float = 0.1,
    ) -> list[MemoryEntry]:
        """Combinacion: primero filtrar por importancia,
        luego por LRU para respetar el limite de tamano.

        La estrategia hibrida protege las memorias marcadas
        como importantes mientras usa LRU para el resto.
        """
        important = [
            m
            for m in memories
            if m.calculate_decayed_importance() >= min_importance
        ]
        if len(important) <= max_size:
            return important
        return sorted(
            important,
            key=lambda m: m.last_accessed,
            reverse=True,
        )[:max_size]
```

### Los costos ocultos de la memoria a largo plazo

Antes de elegir una estrategia de memoria, hay que hablar del elefante en la habitacion: **los costos operativos**. Cada componente de la memoria a largo plazo tiene un precio que se acumula rapidamente en produccion:

**Costo de embedding**: cada nueva memoria que guardas necesita convertirse en un vector. Con un modelo de embeddings como `text-embedding-3-small` de OpenAI, cuesta aproximadamente $0.02 por millon de tokens. Parece poco, pero un agente activo puede generar cientos de memorias por dia, y el costo se multiplica por el numero de usuarios.

**Costo de almacenamiento**: mantener un indice vectorial en un servicio gestionado (Pinecone, Weaviate Cloud) tiene un costo mensual base mas un costo por vector almacenado. Para millones de memorias de agentes, esto puede llegar a cientos de dolares al mes.

**Latencia de retrieval**: cada busqueda vectorial anade latencia al request del agente. Una busqueda en un indice local (ChromaDB, FAISS) tarda 5-50ms. En un servicio remoto, la latencia de red suma 50-200ms adicionales. Cuando tu agente hace 2-3 busquedas de memoria por turno, esto se nota en la experiencia del usuario.

**Costo de contexto**: las memorias recuperadas ocupan tokens en la ventana de contexto. Si recuperas 5 memorias de 200 tokens cada una, estas usando 1,000 tokens adicionales por llamada al LLM. A escala, este costo de contexto suele ser mayor que el costo del embedding original.

La decision de "que vale la pena memorizar" no es solo tecnica: es economica. Un agente interno de bajo volumen puede permitirse memorizar todo. Un agente de atencion al cliente con millones de sesiones necesita politicas estrictas de retencion y un presupuesto de memoria por usuario.

---

## 4.6 El patron Memory Bank: archivos como memoria

Un patron que ha ganado popularidad, especialmente en agentes de desarrollo de software, es el **memory bank**: archivos de texto plano (generalmente Markdown) que el agente lee al inicio de cada sesion y actualiza al final. Es simple, versionable con Git y legible tanto por humanos como por agentes.

La estructura tipica es:

```
memory_bank/
  project_context.md      # Que es este proyecto, decisiones clave
  current_tasks.md        # En que esta trabajando el agente
  learned_patterns.md     # Patrones que ha descubierto
  errors_and_fixes.md     # Errores comunes y como resolverlos
  user_preferences.md     # Preferencias del usuario
```

Es un enfoque rudimentario pero sorprendentemente efectivo para ciertos casos de uso. Las ventajas son claras: no necesitas infraestructura adicional, los archivos son inspeccionables por humanos, y puedes versionar la memoria del agente junto con el codigo del proyecto. Las desventajas tambien: escala mal cuando los archivos crecen mas alla de lo que cabe en la ventana de contexto, y no soporta busqueda semantica.

Este patron es particularmente popular en agentes de codigo como Claude Code, Codex y Cursor, donde el agente necesita recordar las convenciones del proyecto, las decisiones arquitectonicas y los patrones preferidos del desarrollador. En estos casos, la memoria es relativamente pequena (decenas de KB, no GB) y la estructura es suficientemente simple para caber en la ventana de contexto.

---

## 4.7 Caso practico: eligiendo el stack de memoria

Vamos a integrar todo lo que hemos discutido en un sistema de memoria cohesivo. Antes del codigo, la pregunta mas importante es: **que patron de acceso tiene tu agente?**

| Patron de acceso | Stack recomendado | Ejemplo |
|---|---|---|
| Conversaciones cortas (1-5 turnos) | Solo working memory | Chatbot de preguntas frecuentes |
| Conversaciones largas (>10 turnos) | Working memory + resumen progresivo | Agente de soporte tecnico |
| Sesiones recurrentes del mismo usuario | + Memoria episodica (SQLite) | Asistente personal |
| Dominio de conocimiento amplio | + Memoria semantica (vectores) | Agente de investigacion |
| Relaciones complejas entre entidades | + Grafo de conocimiento (Neo4j) | Agente de compliance |
| Agente de codigo | Memory bank (archivos Markdown) | Agente de desarrollo |

Con esto claro, veamos un sistema completo:

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import json


class AgentMemorySystem:
    """Sistema de memoria completo para un agente de IA.

    Integra los tres tipos de memoria (working, episodica,
    semantica) con gestion de estado, checkpointing
    y estrategias de olvido.
    """

    def __init__(
        self,
        agent_id: str,
        context_window_tokens: int = 128_000,
        reserved_tokens: int = 12_000,
    ):
        self.agent_id = agent_id
        self.available_tokens = context_window_tokens - reserved_tokens

        # Tres tipos de memoria
        self.working_memory = ShortTermMemory(
            max_tokens=self.available_tokens
        )
        self.episodic_memory = EpisodicMemory(
            db_path=f"memory/{agent_id}_episodes.db"
        )
        self.semantic_memory = SemanticMemory(
            collection_name=f"{agent_id}_knowledge"
        )

        # Gestion de estado
        self.state_machine = AgentStateMachine()

        # Politica de olvido
        self.forgetting = ForgettingPolicy()

    def prepare_context(self, user_query: str) -> dict:
        """Prepara el contexto optimo para una llamada al LLM.

        Este es el metodo central: decide que poner en la
        ventana de contexto basandose en la relevancia.
        Respeta un presupuesto de tokens para memorias
        inyectadas (10-15% de la ventana disponible).
        """
        # 1. Recuperar memorias episodicas relevantes
        similar_episodes = self.episodic_memory.recall_similar_situations(
            event_type=self._classify_query(user_query),
            limit=3,
        )

        # 2. Recuperar conocimiento semantico relevante
        relevant_knowledge = self.semantic_memory.recall(
            query=user_query,
            n_results=5,
        )

        # 3. Obtener el historial de conversacion reciente
        memory_budget = int(self.available_tokens * 0.15)
        history_budget = self.available_tokens - memory_budget
        recent_messages = self.working_memory.get_recent(
            max_tokens=history_budget
        )

        # 4. Construir contexto priorizando por relevancia
        context = {
            "recent_conversation": recent_messages,
            "relevant_knowledge": [
                k["content"]
                for k in relevant_knowledge
                if k["distance"] < 0.7
            ],
            "similar_past_experiences": [
                {
                    "situation": ep["context"],
                    "action": ep["action_taken"],
                    "result": ep["outcome"],
                    "success": ep["success"],
                }
                for ep in similar_episodes
            ],
            "current_state": self.state_machine.current_state.name,
        }

        return context

    def process_result(
        self,
        user_query: str,
        agent_response: str,
        tool_results: list[dict],
        success: bool,
    ):
        """Despues de que el agente responde, actualizar
        todas las memorias."""
        # 1. Actualizar working memory
        self.working_memory.add("user", user_query)
        self.working_memory.add("assistant", agent_response)

        # 2. Registrar episodio
        self.episodic_memory.record_episode(
            event_type=self._classify_query(user_query),
            context=user_query,
            action=agent_response[:500],
            outcome=json.dumps(tool_results)[:500],
            success=success,
            importance=self._assess_importance(user_query, success),
        )

        # 3. Extraer conocimiento semantico si aplica
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
                    },
                )

        # 4. Consolidar si la working memory esta muy llena
        if self.working_memory.message_count() > 100:
            self._consolidate_memories()

    def _assess_importance(
        self, query: str, success: bool
    ) -> float:
        """Evalua que tan importante es recordar esta interaccion."""
        importance = 0.5
        # Los fracasos son mas importantes (aprendemos de errores)
        if not success:
            importance += 0.3
        # Palabras clave de alta prioridad
        high_priority = [
            "error", "urgente", "produccion", "critico", "fallo"
        ]
        if any(kw in query.lower() for kw in high_priority):
            importance += 0.2
        return min(1.0, importance)

    def _classify_query(self, query: str) -> str:
        """Clasifica el tipo de consulta para busqueda episodica.
        En produccion, usa un clasificador entrenado."""
        query_lower = query.lower()
        if any(w in query_lower for w in ["error", "fallo", "bug"]):
            return "troubleshooting"
        if any(w in query_lower for w in ["reporte", "datos", "metricas"]):
            return "data_request"
        if any(w in query_lower for w in ["como", "ayuda", "explicar"]):
            return "how_to"
        return "general"

    def _extract_knowledge(
        self, query: str, response: str, results: list[dict]
    ) -> Optional[str]:
        """Extrae conocimiento reutilizable de una interaccion
        exitosa. En produccion, usa un LLM para esto."""
        # Simplificado: guarda el par query-response si
        # involucro herramientas
        if results:
            return (
                f"Pregunta: {query[:200]}\n"
                f"Solucion: {response[:300]}"
            )
        return None

    def _consolidate_memories(self):
        """Mover informacion importante de working memory
        a memoria a largo plazo y olvidar lo trivial."""
        # Implementacion: resumir mensajes antiguos,
        # extraer hechos clave, guardar en semantic memory
        pass
```

Este sistema no es perfecto (ninguno lo es), pero ilustra como los diferentes componentes se coordinan: la working memory maneja lo inmediato, la memoria episodica registra experiencias, la memoria semantica acumula conocimiento, y las politicas de olvido evitan que todo se desborde.

---

## 4.8 Herramientas de memoria en produccion

Antes de implementar memoria desde cero, vale la pena conocer las herramientas disponibles en 2026. El ecosistema ha madurado considerablemente:

- **Mem0**: una capa de memoria para agentes que abstrae el almacenamiento vectorial, la extraccion de hechos y la gestion de relevancia. Se integra con los principales frameworks y proveedores de LLMs.
- **Zep**: enfocado en memoria conversacional con extraccion automatica de entidades y hechos. Ofrece APIs de busqueda semantica y temporal.
- **LangGraph Memory**: el sistema de checkpointing y memory store integrado en LangGraph, con persistencia nativa y soporte para memoria a largo plazo entre sesiones.
- **Letta** (antes MemGPT): la evolucion de MemGPT como plataforma, con APIs para gestion de memoria virtual, agentes con estado persistente y herramientas de memoria como ciudadanos de primera clase.
- **Funcionalidades nativas de los proveedores**: tanto Anthropic como OpenAI y Google ofrecen features de memoria a nivel de API que simplifican casos de uso comunes.

La decision entre construir tu propio sistema de memoria o usar una herramienta existente depende del volumen, la complejidad de tu caso de uso y cuanto control necesitas. Para la mayoria de los proyectos, empezar con una herramienta existente y migrar a una solucion custom solo cuando encuentres limitaciones concretas es el camino mas pragmatico.

---

## Takeaway del capitulo

La memoria es lo que convierte un agente de una herramienta desechable en un asistente que mejora con el tiempo. Las lecciones clave:

1. **La taxonomia de la memoria humana es un marco de diseno util**: working memory, episodica, semantica y procedimental mapean directamente a patrones de implementacion. No todo agente necesita los cinco tipos.

2. **El estado debe ser explicito**: las maquinas de estado hacen que los agentes sean depurables, monitoreables y recuperables. La complejidad se combate con interfaces claras.

3. **Los sistemas operativos ya resolvieron muchos de estos problemas**: paginacion, caching, control de concurrencia. MemGPT es solo el principio de aplicar estas ideas a agentes.

4. **Olvidar es tan importante como recordar**: las estrategias de olvido inspiradas en cache (LRU, TTL, importance-based) son esenciales para mantener la calidad de la memoria.

5. **La memoria tiene un costo**: embeddings, almacenamiento, latencia de retrieval, tokens de contexto. Disena la estrategia de memoria para tu caso de uso especifico, no como una solucion generica.

En el proximo capitulo vamos a construir el otro componente critico que falta: el **Agent Harness**, la infraestructura de control que envuelve al agente para que no destruya nada cuando se equivoca. Porque un agente con buena memoria pero sin controles es simplemente un agente que recuerda como causar dano de forma mas eficiente.

---

### Notas y referencias

- [Miller, 1956] George A. Miller. "The Magical Number Seven, Plus or Minus Two." *Psychological Review*, 63(2).
- [Cowan, 2001] Nelson Cowan. "The Magical Number 4 in Short-Term Memory." *Behavioral and Brain Sciences*, 24(1).
- [Park et al., 2023] Joon Sung Park, Joseph C. O'Brien et al. "Generative Agents: Interactive Simulacra of Human Behavior." *UIST 2023*. La funcion de scoring de memorias (recencia + importancia + relevancia).
- [Packer et al., 2023] Charles Packer, Sarah Wooders et al. "MemGPT: Towards LLMs as Operating Systems." *arXiv:2310.08560*. Memoria virtual con paginacion para LLMs.
- [Xu y Liang, 2025] "A-MEM: Agentic Memory for LLM Agents." *arXiv:2502.12110*. Sistema de memoria agentica basado en Zettelkasten.
- [Liu et al., 2023] Nelson F. Liu et al. "Lost in the Middle: How Language Models Use Long Contexts." *Stanford*, 2023.
- [Borges, 1944] Jorge Luis Borges. "Funes el memorioso." *Ficciones*. La parabola literaria de la memoria total.
