# Capitulo 10: Comunicacion entre Agentes -- El Protocolo que Falta

> "Sin protocolo, la comunicacion entre agentes es como dos personas hablando idiomas diferentes: pueden gesticular, pueden intuir, pero no pueden colaborar con precision."

---

En el Capitulo 8 construimos el harness que controla a un agente individual. En el Capitulo 9 conectamos agentes con datos reales mediante RAG. Ahora vamos a abordar un problema que surge en cuanto necesitas que dos agentes trabajen juntos: **como se comunican**.

En 1991, Tim Berners-Lee publico HTTP/0.9: un protocolo minimo con un unico metodo GET, sin headers, que devolvia texto plano. Nadie sabia que ese pequeno protocolo de transferencia de hipertexto se convertiria en el pegamento invisible de la web moderna. Para 1996, cuando HTTP/1.0 se formalizo como RFC 1945, ya era evidente que la estandarizacion no fue un lujo: fue la condicion necesaria para que internet dejara de ser un experimento academico y se convirtiera en infraestructura.

Hoy vivimos un momento analogo con los agentes de IA. Tenemos agentes que razonan, usan herramientas, planifican y ejecutan tareas complejas. Pero cuando necesitan comunicarse entre si, la situacion se parece a la internet pre-HTTP: cada framework, cada laboratorio y cada empresa define su propio formato. Texto libre, JSON ad-hoc, formatos propietarios. El resultado es un ecosistema fragmentado donde la interoperabilidad es la excepcion, no la regla.

Este capitulo explora los patrones de comunicacion entre agentes, los protocolos emergentes que aspiran a convertirse en el "HTTP de los agentes" y las implementaciones practicas que puedes usar hoy.

---

## 10.1 Por que los agentes necesitan un protocolo de comunicacion

### El problema de la torre de Babel

Imagina este escenario: tu empresa tiene un agente de analisis financiero construido con LangGraph, un agente de generacion de reportes construido con CrewAI y un agente de atencion al cliente construido con el SDK de OpenAI. Quieres que colaboren: el agente financiero analiza los datos, pasa los resultados al generador de reportes, y el agente de atencion al cliente usa esos reportes para responder preguntas de los clientes.

El problema es que cada framework tiene su propia forma de representar tareas, resultados y errores. LangGraph usa grafos de estado con checkpointing. CrewAI define agentes con roles, metas y backstories. El SDK de OpenAI usa handoffs. No hay un formato comun para que el resultado de uno sea la entrada del otro.

Sin protocolo, terminas escribiendo adaptadores ad-hoc entre cada par de frameworks. Con tres frameworks, necesitas tres adaptadores. Con diez, necesitas cuarenta y cinco. La complejidad crece cuadraticamente, exactamente como pasaba con los formatos de documentos antes de que HTML estandarizara la web.

### Que hace que un protocolo sea exitoso

Antes de analizar los protocolos emergentes para agentes, vale la pena entender que hace que un protocolo de comunicacion sobreviva. No todos lo logran. Los que lo hacen comparten cuatro caracteristicas fundamentales [Fielding, 2000; Berners-Lee, 1996].

**Contratos claros.** TCP/IP funciona porque define un contrato inequivoco: como se establece una conexion (el three-way handshake), como se transmiten los datos (en segmentos numerados), como se confirma la recepcion (ACKs) y como se cierra la conexion. No hay ambiguedad. HTTP llevo esta idea al nivel de aplicacion: un metodo, una URI, headers y un cuerpo. La respuesta tiene un codigo de estado numerico que comunica el resultado de forma no ambigua.

**Versionado y evolucion.** Los protocolos exitosos evolucionan sin romper lo existente. HTTP/2 introdujo multiplexacion, pero un servidor HTTP/2 puede negociar hacia abajo con un cliente HTTP/1.1. gRPC usa Protocol Buffers con versionado explicito donde los campos nuevos son opcionales por defecto.

**Manejo de errores predecible.** TCP retransmite paquetes perdidos. HTTP define codigos de error semanticos. gRPC tiene codigos de estado (OK, CANCELLED, DEADLINE_EXCEEDED, NOT_FOUND, PERMISSION_DENIED) que permiten reaccionar programaticamente. Un protocolo que no define como manejar errores es un protocolo incompleto.

**Simplicidad.** El RFC de HTTP/1.0 tenia 60 paginas. El de TCP, 85. En contraste, las especificaciones de SOAP y WS-* sumaban miles de paginas. Ya sabemos quien gano esa batalla. La leccion: el protocolo que se adopte masivamente sera el que un desarrollador pueda implementar en una tarde.

### Lo que es diferente con agentes de IA

Los agentes de IA agregan complejidades que no existen en los protocolos clasicos:

**No determinismo.** Una API REST siempre devuelve el mismo resultado para la misma peticion (en condiciones ideales). Un agente puede devolver respuestas diferentes cada vez. El protocolo necesita mecanismos para comunicar niveles de confianza, no solo resultados.

**Errores semanticos.** Un agente puede responder con formato perfecto y contenido incorrecto. No hay un codigo de estado HTTP para "la respuesta es plausible pero podria ser una alucinacion". El protocolo necesita metadatos de confianza.

**Sesiones de larga duracion.** Una peticion HTTP tipica dura milisegundos. Una colaboracion entre agentes puede durar minutos, horas o dias. El protocolo necesita soportar tareas de larga duracion con actualizaciones incrementales.

**Negociacion de capacidades.** Dos agentes que se encuentran necesitan saber que puede hacer el otro, en que formatos trabaja y que nivel de confiabilidad ofrece. Esto va mucho mas alla de la negociacion de content-type de HTTP.

---

## 10.2 Patrones de comunicacion: request-response, pub-sub y blackboard

Antes de hablar de protocolos especificos, necesitamos entender los patrones fundamentales de comunicacion entre agentes. Estos patrones son independientes del protocolo y definen la *topologia logica* de la interaccion.

### Request-response: el patron mas simple

Un agente envia una solicitud a otro y espera una respuesta. Es el patron mas familiar porque replica la interaccion HTTP clasica: cliente pide, servidor responde.

```python
"""
Patron request-response entre agentes.
El patron mas simple: un agente pide, otro responde.
"""

import asyncio
import uuid
from dataclasses import dataclass, field
from typing import Any
from enum import Enum


class MessageType(Enum):
    REQUEST = "request"
    RESPONSE = "response"
    ERROR = "error"


@dataclass
class AgentMessage:
    """Mensaje estandar entre agentes."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: MessageType = MessageType.REQUEST
    sender: str = ""
    receiver: str = ""
    payload: dict = field(default_factory=dict)
    correlation_id: str | None = None  # para vincular respuesta con request
    confidence: float = 1.0  # nivel de confianza en la respuesta
    metadata: dict = field(default_factory=dict)


class RequestResponseAgent:
    """Agente que puede enviar requests y recibir responses."""

    def __init__(self, name: str, handler):
        self.name = name
        self.handler = handler  # funcion que procesa requests
        self._pending: dict[str, asyncio.Future] = {}

    async def send_request(
        self, target: "RequestResponseAgent", payload: dict
    ) -> AgentMessage:
        """Envia un request y espera la respuesta."""
        request = AgentMessage(
            type=MessageType.REQUEST,
            sender=self.name,
            receiver=target.name,
            payload=payload,
        )

        # Crear un Future para esperar la respuesta
        future = asyncio.get_event_loop().create_future()
        self._pending[request.id] = future

        # Enviar al agente destino y obtener respuesta
        response = await target.receive(request)
        return response

    async def receive(self, message: AgentMessage) -> AgentMessage:
        """Recibe un mensaje y genera una respuesta."""
        try:
            result = await self.handler(message.payload)
            return AgentMessage(
                type=MessageType.RESPONSE,
                sender=self.name,
                receiver=message.sender,
                payload=result,
                correlation_id=message.id,
                confidence=result.get("confidence", 1.0),
            )
        except Exception as e:
            return AgentMessage(
                type=MessageType.ERROR,
                sender=self.name,
                receiver=message.sender,
                payload={"error": str(e)},
                correlation_id=message.id,
                confidence=0.0,
            )


# Ejemplo de uso
async def analizar_sentimiento(payload: dict) -> dict:
    """Handler simulado para analisis de sentimiento."""
    texto = payload.get("texto", "")
    # En produccion aqui iria la llamada al LLM
    return {
        "sentimiento": "positivo",
        "score": 0.87,
        "confidence": 0.92,
    }


async def demo_request_response():
    analista = RequestResponseAgent("analista", analizar_sentimiento)
    coordinador = RequestResponseAgent("coordinador", lambda p: p)

    respuesta = await coordinador.send_request(
        analista, {"texto": "El producto es excelente"}
    )
    print(f"Respuesta: {respuesta.payload}")
    print(f"Confianza: {respuesta.confidence}")
```

**Ventajas**: simple, facil de razonar, facil de depurar. Cada interaccion es autocontenida.
**Desventajas**: sincronico por naturaleza, el solicitante se bloquea esperando la respuesta. No escala bien cuando multiples agentes necesitan colaborar simultaneamente.
**Mejor para**: consultas puntuales, delegacion simple de tareas, interacciones donde un agente necesita el resultado de otro antes de continuar.

### Pub-sub: comunicacion desacoplada

En el patron publicador-suscriptor, los agentes no se comunican directamente. En su lugar, publican mensajes en "canales" o "topicos", y los agentes interesados se suscriben a esos canales. El publicador no sabe (ni necesita saber) quien esta escuchando.

```python
"""
Patron pub-sub para comunicacion entre agentes.
Los agentes se comunican a traves de canales tematicos,
sin conocerse directamente.
"""

import asyncio
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable, Awaitable


@dataclass
class Event:
    """Evento publicado en un canal."""
    topic: str
    publisher: str
    data: dict
    event_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )
    timestamp: float = field(default_factory=lambda: __import__("time").time())


class MessageBroker:
    """Broker central que gestiona canales y suscripciones.

    En produccion, usarias Redis Pub/Sub, Apache Kafka
    o un servicio similar. Esta implementacion es educativa.
    """

    def __init__(self):
        self._subscribers: dict[
            str, list[Callable[[Event], Awaitable[None]]]
        ] = defaultdict(list)
        self._event_log: list[Event] = []

    def subscribe(
        self, topic: str, callback: Callable[[Event], Awaitable[None]]
    ):
        """Registra un callback para un topico."""
        self._subscribers[topic].append(callback)

    async def publish(self, event: Event):
        """Publica un evento a todos los suscriptores del topico."""
        self._event_log.append(event)
        callbacks = self._subscribers.get(event.topic, [])

        # Notificar a todos los suscriptores en paralelo
        if callbacks:
            await asyncio.gather(
                *[cb(event) for cb in callbacks],
                return_exceptions=True,
            )


class PubSubAgent:
    """Agente que se comunica via pub-sub."""

    def __init__(self, name: str, broker: MessageBroker):
        self.name = name
        self.broker = broker
        self.received_events: list[Event] = []

    def subscribe(self, topic: str):
        """Se suscribe a un topico."""
        self.broker.subscribe(topic, self._on_event)

    async def publish(self, topic: str, data: dict):
        """Publica un evento en un topico."""
        event = Event(topic=topic, publisher=self.name, data=data)
        await self.broker.publish(event)

    async def _on_event(self, event: Event):
        """Callback cuando llega un evento."""
        self.received_events.append(event)
        await self.handle_event(event)

    async def handle_event(self, event: Event):
        """Override en subclases para procesar eventos."""
        pass


# Ejemplo: pipeline de analisis con pub-sub
class AgenteExtractor(PubSubAgent):
    async def extraer(self, documento: str):
        # Simula extraccion de entidades
        entidades = {"personas": ["Juan"], "empresas": ["Acme"]}
        await self.publish("entidades.extraidas", {
            "documento_id": "doc-001",
            "entidades": entidades,
        })


class AgenteClasificador(PubSubAgent):
    async def handle_event(self, event: Event):
        if event.topic == "entidades.extraidas":
            # Clasificar las entidades recibidas
            clasificacion = {
                "tipo": "reporte_financiero",
                "relevancia": 0.95,
            }
            await self.publish("documento.clasificado", {
                "documento_id": event.data["documento_id"],
                "clasificacion": clasificacion,
                "entidades": event.data["entidades"],
            })


async def demo_pubsub():
    broker = MessageBroker()
    extractor = AgenteExtractor("extractor", broker)
    clasificador = AgenteClasificador("clasificador", broker)

    # El clasificador escucha las extracciones
    clasificador.subscribe("entidades.extraidas")

    # El extractor procesa un documento
    # Automaticamente notifica al clasificador
    await extractor.extraer("Reporte anual de Acme Corp...")
```

**Ventajas**: desacoplamiento total entre agentes (el publicador no conoce a los suscriptores), facil de agregar nuevos agentes sin modificar los existentes, soporta multiples consumidores del mismo evento.
**Desventajas**: dificil de rastrear el flujo de ejecucion (la causalidad se pierde en el broker), problemas de ordenamiento de mensajes, complejidad para manejar errores (si un suscriptor falla, los demas no se enteran).
**Mejor para**: pipelines de procesamiento asincrono, sistemas donde los agentes reaccionan a eventos, arquitecturas donde la composicion de agentes cambia frecuentemente.

### Blackboard: conocimiento compartido

El patron blackboard es un clasico de la inteligencia artificial distribuida que ha encontrado una segunda vida con los agentes LLM [Hayes-Roth, 1985]. En lugar de que los agentes se envien mensajes directamente, todos leen y escriben en un espacio de conocimiento compartido: el "pizarron".

Cada agente observa el estado actual del pizarron, decide si puede contribuir algo, y si puede, escribe su contribucion. El proceso continua hasta que el problema esta resuelto o se alcanza un limite.

```python
"""
Patron blackboard para colaboracion entre agentes.
Los agentes contribuyen a un espacio de conocimiento compartido.
"""

import asyncio
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class BlackboardEntry:
    """Una contribucion al pizarron."""
    key: str
    value: Any
    author: str
    timestamp: float = field(default_factory=time.time)
    confidence: float = 1.0
    version: int = 1


class Blackboard:
    """Espacio de conocimiento compartido entre agentes.

    En produccion, esto seria una base de datos con control de
    concurrencia (Redis, PostgreSQL con locks, etc.).
    """

    def __init__(self):
        self._entries: dict[str, BlackboardEntry] = {}
        self._history: list[BlackboardEntry] = []
        self._lock = asyncio.Lock()
        self._watchers: list[asyncio.Event] = []

    async def read(self, key: str) -> BlackboardEntry | None:
        """Lee una entrada del pizarron."""
        return self._entries.get(key)

    async def read_all(self) -> dict[str, BlackboardEntry]:
        """Lee todo el estado actual del pizarron."""
        return dict(self._entries)

    async def write(
        self,
        key: str,
        value: Any,
        author: str,
        confidence: float = 1.0,
    ):
        """Escribe una entrada en el pizarron con lock de concurrencia."""
        async with self._lock:
            existing = self._entries.get(key)
            version = (existing.version + 1) if existing else 1

            entry = BlackboardEntry(
                key=key,
                value=value,
                author=author,
                confidence=confidence,
                version=version,
            )
            self._entries[key] = entry
            self._history.append(entry)

            # Notificar a los watchers
            for event in self._watchers:
                event.set()

    async def wait_for_change(self, timeout: float = 30.0) -> bool:
        """Espera hasta que alguien escriba en el pizarron."""
        event = asyncio.Event()
        self._watchers.append(event)
        try:
            await asyncio.wait_for(event.wait(), timeout=timeout)
            return True
        except asyncio.TimeoutError:
            return False
        finally:
            self._watchers.remove(event)


class BlackboardAgent:
    """Agente que colabora via el patron blackboard."""

    def __init__(self, name: str, blackboard: Blackboard):
        self.name = name
        self.bb = blackboard

    async def can_contribute(self) -> bool:
        """Determina si este agente puede aportar algo al estado actual."""
        raise NotImplementedError

    async def contribute(self):
        """Hace una contribucion al pizarron."""
        raise NotImplementedError


class AgenteInvestigador(BlackboardAgent):
    """Investiga un tema y publica hallazgos en el pizarron."""

    async def can_contribute(self) -> bool:
        pregunta = await self.bb.read("pregunta")
        hallazgos = await self.bb.read("hallazgos")
        return pregunta is not None and hallazgos is None

    async def contribute(self):
        pregunta = await self.bb.read("pregunta")
        # En produccion: llamada al LLM con herramientas de busqueda
        hallazgos = {
            "fuentes": ["paper-A", "paper-B"],
            "resumen": f"Hallazgos sobre: {pregunta.value}",
        }
        await self.bb.write(
            "hallazgos", hallazgos, self.name, confidence=0.85
        )


class AgenteRedactor(BlackboardAgent):
    """Redacta un texto basado en los hallazgos del pizarron."""

    async def can_contribute(self) -> bool:
        hallazgos = await self.bb.read("hallazgos")
        borrador = await self.bb.read("borrador")
        return hallazgos is not None and borrador is None

    async def contribute(self):
        hallazgos = await self.bb.read("hallazgos")
        # En produccion: llamada al LLM para redactar
        borrador = f"Borrador basado en: {hallazgos.value['resumen']}"
        await self.bb.write(
            "borrador", borrador, self.name, confidence=0.80
        )


class AgenteRevisor(BlackboardAgent):
    """Revisa el borrador y publica correccion o aprobacion."""

    async def can_contribute(self) -> bool:
        borrador = await self.bb.read("borrador")
        revision = await self.bb.read("revision")
        return borrador is not None and revision is None

    async def contribute(self):
        borrador = await self.bb.read("borrador")
        # En produccion: llamada al LLM para revisar
        revision = {
            "aprobado": True,
            "comentarios": "El borrador es claro y preciso.",
        }
        await self.bb.write(
            "revision", revision, self.name, confidence=0.90
        )


class BlackboardController:
    """Controla el ciclo del blackboard: observar, decidir, actuar."""

    def __init__(
        self,
        blackboard: Blackboard,
        agents: list[BlackboardAgent],
        max_iterations: int = 20,
    ):
        self.bb = blackboard
        self.agents = agents
        self.max_iterations = max_iterations

    async def run(self) -> dict:
        """Ejecuta el ciclo del blackboard hasta que no haya mas
        contribuciones posibles o se alcance el limite."""
        for iteration in range(self.max_iterations):
            contributed = False
            for agent in self.agents:
                if await agent.can_contribute():
                    await agent.contribute()
                    contributed = True
                    break  # reiniciar el ciclo para reevaluar

            if not contributed:
                break  # ningun agente puede contribuir: terminamos

        return await self.bb.read_all()


async def demo_blackboard():
    bb = Blackboard()
    investigador = AgenteInvestigador("investigador", bb)
    redactor = AgenteRedactor("redactor", bb)
    revisor = AgenteRevisor("revisor", bb)

    controller = BlackboardController(
        bb, [investigador, redactor, revisor]
    )

    # Plantar la pregunta inicial
    await bb.write("pregunta", "Que es MCP?", "usuario")

    # Ejecutar: investigador -> redactor -> revisor
    resultado = await controller.run()
    for key, entry in resultado.items():
        print(f"  {key}: {entry.value} (por {entry.author})")
```

**Ventajas**: los agentes no necesitan conocerse entre si, el estado del problema esta centralizado y es observable, facil de agregar nuevos agentes que contribuyan nuevos tipos de conocimiento.
**Desventajas**: riesgo de condiciones de carrera si el control de concurrencia es deficiente, el pizarron puede crecer sin control, mas dificil de escalar horizontalmente que pub-sub.
**Mejor para**: problemas de sintesis donde multiples agentes contribuyen piezas de conocimiento, investigacion colaborativa, cualquier tarea donde el resultado emerge de contribuciones incrementales.

### Comparativa de patrones

| Patron | Acoplamiento | Escalabilidad | Depuracion | Caso de uso ideal |
|--------|-------------|---------------|------------|-------------------|
| Request-response | Alto | Baja | Facil | Delegacion simple |
| Pub-sub | Bajo | Alta | Dificil | Pipelines asincronos |
| Blackboard | Medio | Media | Media | Sintesis colaborativa |

La eleccion del patron no es excluyente. Un sistema real puede usar request-response para consultas puntuales, pub-sub para notificaciones de eventos y blackboard para la colaboracion en una tarea compleja. La clave es usar el patron correcto para cada tipo de interaccion.

---

## 10.3 MCP: Model Context Protocol -- el USB-C de los agentes

### Arquitectura y proposito

Anthropic lanzo MCP en noviembre de 2024 como un protocolo abierto para conectar modelos de lenguaje con herramientas y fuentes de datos externas. La analogia mas precisa es la de un **puerto USB-C**: asi como USB-C estandarizo la conexion entre dispositivos y perifericos, MCP estandariza la conexion entre un agente y las herramientas que puede usar.

MCP se basa en **JSON-RPC 2.0**, el mismo protocolo de llamadas a procedimientos remotos que ya se usa en editores de codigo (el Language Server Protocol de VS Code es primo hermano de MCP). La arquitectura define tres componentes [Anthropic, 2024]:

- **Host**: la aplicacion que contiene al modelo de lenguaje (Claude Desktop, Cursor, VS Code, tu aplicacion personalizada).
- **Client**: el componente que se comunica con los servidores MCP desde dentro del host.
- **Server**: un servicio que expone herramientas, recursos o prompts al modelo.

Un servidor MCP puede exponer acceso a una base de datos, a un sistema de archivos, a una API externa o a cualquier funcionalidad que quieras darle a tu agente. La comunicacion se transporta sobre HTTP con Server-Sent Events (SSE) para streaming, con autenticacion **OAuth 2.1** nativa en la especificacion de noviembre de 2025.

### El ecosistema en 2026

Para diciembre de 2025, MCP reportaba mas de 97 millones de descargas mensuales de sus SDKs, con mas de 10,000 servidores activos en produccion. OpenAI adopto oficialmente el protocolo en marzo de 2025, integrandolo en ChatGPT Desktop. Multiples IDEs (Claude Desktop, Cursor, VS Code, Windsurf) lo soportan nativamente. En diciembre de 2025, Anthropic dono MCP a la **Agentic AI Foundation (AAIF)** bajo la Linux Foundation, con Anthropic, OpenAI y Block como cofundadores.

La especificacion de noviembre de 2025 represento un salto significativo: expandio MCP de la simple invocacion sincronica de herramientas a una arquitectura capaz de soportar workflows seguros, de larga duracion y con requisitos empresariales. Las adiciones clave fueron capacidades asincronas, autorizacion modernizada con OAuth 2.1, y el primitivo experimental `Tasks` para tareas de larga duracion.

### Anatomia de una interaccion MCP

Veamos como se ve una interaccion MCP a nivel de mensajes JSON-RPC:

```python
"""
Implementacion simplificada de un servidor MCP.
Demuestra el descubrimiento de herramientas y la invocacion.
"""

import json
from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class MCPTool:
    """Definicion de una herramienta MCP."""
    name: str
    description: str
    input_schema: dict


@dataclass
class MCPServer:
    """Servidor MCP simplificado.

    Un servidor MCP real usaria el SDK oficial
    (mcp-python) con transporte HTTP+SSE. Esta version
    ilustra la mecanica del protocolo.
    """
    name: str
    version: str
    tools: list[MCPTool] = field(default_factory=list)
    _handlers: dict = field(default_factory=dict)

    def register_tool(
        self, name: str, description: str, schema: dict, handler
    ):
        """Registra una herramienta con su handler."""
        self.tools.append(MCPTool(name, description, schema))
        self._handlers[name] = handler

    def handle_jsonrpc(self, request: dict) -> dict:
        """Procesa una peticion JSON-RPC 2.0."""
        method = request.get("method")
        params = request.get("params", {})
        req_id = request.get("id")

        dispatch = {
            "initialize": self._handle_initialize,
            "tools/list": self._handle_tools_list,
            "tools/call": self._handle_tools_call,
        }

        handler = dispatch.get(method)
        if handler is None:
            return self._error(req_id, -32601, f"Method not found: {method}")

        try:
            result = handler(params)
            return {"jsonrpc": "2.0", "id": req_id, "result": result}
        except Exception as e:
            return self._error(req_id, -32000, str(e))

    def _handle_initialize(self, params: dict) -> dict:
        """Handshake inicial: intercambiar capacidades."""
        return {
            "protocolVersion": "2025-11-25",
            "serverInfo": {"name": self.name, "version": self.version},
            "capabilities": {
                "tools": {"listChanged": True},
            },
        }

    def _handle_tools_list(self, params: dict) -> dict:
        """Devuelve la lista de herramientas disponibles."""
        return {
            "tools": [
                {
                    "name": t.name,
                    "description": t.description,
                    "inputSchema": t.input_schema,
                }
                for t in self.tools
            ]
        }

    def _handle_tools_call(self, params: dict) -> dict:
        """Invoca una herramienta."""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        handler = self._handlers.get(tool_name)
        if handler is None:
            raise ValueError(f"Tool not found: {tool_name}")

        result = handler(arguments)
        return {
            "content": [{"type": "text", "text": json.dumps(result)}]
        }

    def _error(self, req_id, code: int, message: str) -> dict:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": code, "message": message},
        }


# Ejemplo: servidor MCP para busqueda de productos
server = MCPServer(name="catalogo-server", version="1.0.0")

def buscar_producto(args: dict) -> dict:
    query = args.get("query", "")
    # En produccion: consulta a la base de datos
    return {
        "productos": [
            {"id": "P001", "nombre": f"Resultado para: {query}", "precio": 99.99}
        ],
        "total": 1,
    }

server.register_tool(
    name="buscar_producto",
    description="Busca productos en el catalogo por nombre o categoria",
    schema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Termino de busqueda"},
            "categoria": {"type": "string", "description": "Categoria"},
        },
        "required": ["query"],
    },
    handler=buscar_producto,
)

# Simular interaccion completa
init_response = server.handle_jsonrpc({
    "jsonrpc": "2.0", "id": 1, "method": "initialize",
    "params": {"protocolVersion": "2025-11-25"},
})
print("Init:", json.dumps(init_response, indent=2))

tools_response = server.handle_jsonrpc({
    "jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {},
})
print("Tools:", json.dumps(tools_response, indent=2))

call_response = server.handle_jsonrpc({
    "jsonrpc": "2.0", "id": 3, "method": "tools/call",
    "params": {"name": "buscar_producto", "arguments": {"query": "laptop"}},
})
print("Call:", json.dumps(call_response, indent=2))
```

### El limite fundamental de MCP

MCP resuelve la comunicacion entre un agente y sus herramientas, pero **no** la comunicacion entre agentes. Es como si tuvieramos un estandar excelente para que un navegador hable con plugins, pero no para que dos navegadores se comuniquen entre si. Para eso necesitamos otro protocolo.

---

## 10.4 A2A: Agent-to-Agent Protocol -- la propuesta de Google

### Llenando el vacio

Google lanzo A2A en abril de 2025 precisamente para llenar el vacio que MCP deja. Si MCP es el USB-C, A2A es mas parecido a HTTP: define como dos agentes que no se conocen entre si pueden descubrirse, comunicarse y colaborar [Google, 2025].

A2A introduce varios conceptos clave:

**Agent Card.** Un documento JSON que cada agente publica en `/.well-known/agent.json`, describiendo su identidad, capacidades, habilidades especificas y requisitos de autenticacion. Es el equivalente a un curriculum profesional que cada agente lleva consigo.

**Tasks.** La unidad fundamental de trabajo. Un agente cliente crea una tarea que pasa por un ciclo de vida definido: `submitted` -> `working` -> `completed` (o `failed`, `canceled`). Las tareas pueden ser instantaneas o de larga duracion.

**Artifacts.** Los resultados que un agente genera al completar una tarea. Pueden ser documentos, imagenes, datos estructurados o cualquier tipo de contenido.

Toda la comunicacion ocurre sobre **HTTP(S)** usando **JSON-RPC 2.0**, soportando tres modos: request/response sincrono, streaming con SSE, y notificaciones push asincronas. La version 0.3 agrego soporte para gRPC y la capacidad de firmar digitalmente las Agent Cards.

La especificacion se organiza en capas: la capa 2 describe capacidades y comportamientos fundamentales independientes del protocolo, mientras que la capa 3 proporciona bindings concretos para JSON-RPC, gRPC y HTTP/REST.

### Implementacion: dos agentes comunicandose via A2A

```python
"""
Implementacion simplificada del protocolo A2A.
Dos agentes se descubren y colaboran.
"""

import json
import uuid
import time
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any


class TaskStatus(Enum):
    SUBMITTED = "submitted"
    WORKING = "working"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


@dataclass
class Skill:
    """Habilidad que un agente ofrece."""
    id: str
    name: str
    description: str
    input_modes: list[str] = field(
        default_factory=lambda: ["application/json"]
    )
    output_modes: list[str] = field(
        default_factory=lambda: ["application/json"]
    )


@dataclass
class AgentCard:
    """Tarjeta de identidad A2A del agente."""
    name: str
    description: str
    url: str
    version: str
    skills: list[Skill]
    capabilities: dict = field(default_factory=lambda: {
        "streaming": False,
        "pushNotifications": False,
    })
    authentication: dict = field(default_factory=lambda: {
        "schemes": ["bearer"]
    })


@dataclass
class TaskArtifact:
    """Resultado producido por un agente."""
    name: str
    parts: list[dict]  # [{"type": "text", "text": "..."}, ...]


@dataclass
class A2ATask:
    """Tarea A2A con ciclo de vida."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: TaskStatus = TaskStatus.SUBMITTED
    skill_id: str = ""
    input_data: dict = field(default_factory=dict)
    artifacts: list[TaskArtifact] = field(default_factory=list)
    error: str | None = None
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)


class A2AAgent:
    """Agente que implementa el protocolo A2A."""

    def __init__(self, card: AgentCard):
        self.card = card
        self._tasks: dict[str, A2ATask] = {}
        self._skill_handlers: dict[str, Any] = {}

    def register_skill_handler(self, skill_id: str, handler):
        """Registra un handler para una habilidad."""
        self._skill_handlers[skill_id] = handler

    # --- Metodos del servidor A2A ---

    def discover(self) -> dict:
        """Endpoint: /.well-known/agent.json"""
        return {
            "name": self.card.name,
            "description": self.card.description,
            "url": self.card.url,
            "version": self.card.version,
            "capabilities": self.card.capabilities,
            "skills": [
                {
                    "id": s.id,
                    "name": s.name,
                    "description": s.description,
                    "inputModes": s.input_modes,
                    "outputModes": s.output_modes,
                }
                for s in self.card.skills
            ],
            "authentication": self.card.authentication,
        }

    async def create_task(
        self, skill_id: str, input_data: dict
    ) -> A2ATask:
        """Crea y procesa una tarea."""
        # Verificar que la habilidad existe
        valid_ids = [s.id for s in self.card.skills]
        if skill_id not in valid_ids:
            raise ValueError(
                f"Skill '{skill_id}' no disponible. "
                f"Disponibles: {valid_ids}"
            )

        task = A2ATask(skill_id=skill_id, input_data=input_data)
        self._tasks[task.id] = task

        # Procesar la tarea
        task.status = TaskStatus.WORKING
        task.updated_at = time.time()

        try:
            handler = self._skill_handlers.get(skill_id)
            if handler is None:
                raise ValueError(f"No handler for skill: {skill_id}")

            result = await handler(input_data)
            task.artifacts.append(TaskArtifact(
                name="result",
                parts=[{"type": "text", "text": json.dumps(result)}],
            ))
            task.status = TaskStatus.COMPLETED
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)

        task.updated_at = time.time()
        return task

    def get_task_status(self, task_id: str) -> dict:
        """Consulta el estado de una tarea."""
        task = self._tasks.get(task_id)
        if task is None:
            raise ValueError(f"Task not found: {task_id}")
        return {
            "id": task.id,
            "status": task.status.value,
            "artifacts": [
                {"name": a.name, "parts": a.parts}
                for a in task.artifacts
            ],
            "error": task.error,
        }


class A2AClient:
    """Cliente que se comunica con agentes A2A remotos."""

    def __init__(self, name: str):
        self.name = name

    async def discover_agent(self, agent: A2AAgent) -> dict:
        """Descubre las capacidades de un agente remoto.
        En produccion: HTTP GET a /.well-known/agent.json"""
        return agent.discover()

    async def delegate_task(
        self, agent: A2AAgent, skill_id: str, input_data: dict
    ) -> A2ATask:
        """Delega una tarea a un agente remoto.
        En produccion: HTTP POST con JSON-RPC a /tasks/create"""
        card = await self.discover_agent(agent)
        print(f"[{self.name}] Descubrio agente: {card['name']}")
        print(f"  Skills: {[s['name'] for s in card['skills']]}")

        task = await agent.create_task(skill_id, input_data)
        print(f"[{self.name}] Tarea {task.id[:8]}... "
              f"status: {task.status.value}")
        return task


# Ejemplo: colaboracion entre agente financiero y agente de reportes
async def demo_a2a():
    # Agente financiero
    financiero = A2AAgent(AgentCard(
        name="agente-financiero",
        description="Analiza datos financieros y detecta anomalias",
        url="https://agentes.ejemplo.com/financiero",
        version="1.0.0",
        skills=[Skill(
            id="analisis-balance",
            name="Analisis de Balance",
            description="Analiza un balance y detecta anomalias",
        )],
    ))

    async def analizar_balance(data: dict) -> dict:
        return {
            "anomalias": [
                {"tipo": "gasto_inusual", "monto": 50000, "confianza": 0.89}
            ],
            "resumen": "Se detecto un gasto inusual en Q3",
            "confianza_global": 0.87,
        }

    financiero.register_skill_handler(
        "analisis-balance", analizar_balance
    )

    # Cliente: el orquestador delega al agente financiero
    orquestador = A2AClient("orquestador")
    task = await orquestador.delegate_task(
        financiero,
        "analisis-balance",
        {"periodo": "Q3-2026", "empresa": "Acme Corp"},
    )
    print(f"Resultado: {task.artifacts[0].parts[0]['text']}")
```

### MCP + A2A: complementarios, no competidores

La confusion mas comun es pensar que MCP y A2A compiten. No es asi: operan en **capas diferentes**. MCP estandariza como un agente accede a herramientas y datos (la capa vertical, agente-a-herramienta). A2A estandariza como dos agentes colaboran entre si (la capa horizontal, agente-a-agente).

Un sistema completo usaria ambos: cada agente usa MCP internamente para conectarse con sus herramientas, y A2A externamente para comunicarse con otros agentes.

```
┌─────────────────┐        A2A         ┌─────────────────┐
│  Agente A       │ <================> │  Agente B       │
│                 │  (agente-agente)   │                 │
│  ┌───────────┐  │                    │  ┌───────────┐  │
│  │ MCP Client│  │                    │  │ MCP Client│  │
│  └─────┬─────┘  │                    │  └─────┬─────┘  │
└────────┼────────┘                    └────────┼────────┘
         │ MCP                                  │ MCP
         │ (agente-herramienta)                 │
    ┌────┴────┐                            ┌────┴────┐
    │MCP Srv A│                            │MCP Srv B│
    │(DB, API)│                            │(Files)  │
    └─────────┘                            └─────────┘
```

Tambien existen propuestas adicionales como el **Agent Network Protocol (ANP)**, que agrega una capa de descubrimiento descentralizado, y el **Agent Communication Protocol (ACP)**, enfocado en escenarios empresariales. La Agentic AI Foundation (AAIF) bajo la Linux Foundation coordina la evolucion de estos estandares, con Anthropic, OpenAI, Google, Microsoft y AWS como participantes.

---

## 10.5 Serializacion y negociacion de capacidades

### El costo oculto de la serializacion

Cada mensaje entre agentes cuesta tokens. Y los tokens cuestan dinero. Esto introduce un trade-off que no existe en sistemas distribuidos tradicionales donde la comunicacion es practicamente gratuita.

Considera un sistema con 5 agentes que debaten en 3 rondas. Un calculo ingenuo: 5 agentes x (2,000 tokens entrada + 500 salida) x 3 rondas = 37,500 tokens. Pero esto subestima el costo real por un factor de 3-5x porque omite componentes repetidos en cada llamada: el system prompt de cada agente (500-2,000 tokens), las definiciones de herramientas (100-500 por herramienta), y el contexto acumulado (el historial crece con cada ronda).

Con precios de 2026, un debate completo cuesta entre $0.40 y $0.75. A 10,000 consultas diarias: $4,000-$7,500 al dia solo en comunicacion inter-agente. La forma en que serializas los mensajes importa:

```python
"""
Serializacion eficiente de mensajes entre agentes.
La diferencia entre serializacion verbosa y compacta
puede reducir el consumo de tokens en un 30-50%.
"""

# MAL: serializacion verbosa que desperdicia tokens
verbose_message = {
    "message_type": "analysis_result",
    "sender_agent_identifier": "security_analysis_agent_v2",
    "receiver_agent_identifier": "orchestrator_main_agent",
    "timestamp_utc": "2026-03-15T10:30:00Z",
    "analysis_result_payload": {
        "detailed_description": "SQL injection en endpoint /api/users",
        "vulnerability_severity_level": "high",
        "recommended_fix_description": "Usar consultas parametrizadas",
    }
}
# ~45 tokens solo en claves

# BIEN: serializacion compacta
compact_message = {
    "from": "security",
    "type": "vuln",
    "severity": "high",
    "finding": "SQL injection en /api/users, parametro 'id' sin sanitizar",
    "fix": "Usar consultas parametrizadas",
}
# ~20 tokens en claves: ~55% de reduccion en overhead


class EfficientSerializer:
    """Serializa mensajes entre agentes minimizando tokens.

    Estrategias:
    1. Claves cortas pero legibles
    2. Eliminar campos con valores por defecto
    3. Comprimir listas de resultados
    4. Usar referencias a contextos previos en vez de copiar
    """

    @staticmethod
    def serialize(message: dict, include_defaults: bool = False) -> dict:
        """Serializa eliminando campos con valores por defecto."""
        defaults = {
            "confidence": 1.0,
            "metadata": {},
            "error": None,
        }

        result = {}
        for key, value in message.items():
            if not include_defaults and key in defaults:
                if value == defaults[key]:
                    continue  # omitir valores por defecto
            result[key] = value
        return result

    @staticmethod
    def compress_context(
        full_context: list[dict], max_entries: int = 5
    ) -> list[dict]:
        """Comprime el contexto manteniendo solo lo esencial.

        En vez de copiar todo el historial en cada mensaje,
        mantiene los N mensajes mas recientes y un resumen.
        """
        if len(full_context) <= max_entries:
            return full_context

        # Mantener el primero (contexto original) y los ultimos N-1
        summary = {
            "role": "system",
            "content": (
                f"[Resumen: {len(full_context) - max_entries + 1} "
                f"mensajes anteriores omitidos]"
            ),
        }
        return [summary] + full_context[-(max_entries - 1):]
```

### Negociacion de capacidades

Dos agentes que se encuentran necesitan acordar como van a comunicarse. Que formatos de entrada y salida soportan? Pueden hacer streaming? Cuanto tardan tipicamente en responder?

A2A resuelve esto con las Agent Cards: capacidades enumeradas explicitamente. El Agent Network Protocol (ANP) propone una alternativa mas ambiciosa: una negociacion de meta-protocolo donde los agentes usan lenguaje natural para acordar los detalles. Esto es conceptualmente elegante pero introduce incertidumbre: si dos agentes tienen que "ponerse de acuerdo" sobre como hablar, la conversacion sobre la conversacion puede fallar.

La alternativa pragmatica es mas aburrida pero mas robusta:

```python
"""
Negociacion de capacidades entre agentes.
Determina si dos agentes son compatibles antes de colaborar.
"""

from dataclasses import dataclass


@dataclass
class AgentCapabilities:
    """Capacidades que un agente declara."""
    input_formats: list[str]   # ["application/json", "text/plain"]
    output_formats: list[str]  # ["application/json", "text/markdown"]
    max_input_tokens: int = 100_000
    supports_streaming: bool = False
    supports_async: bool = True
    typical_latency_ms: int = 2000  # latencia tipica en ms
    confidence_reporting: bool = True  # reporta nivel de confianza


def negotiate_capabilities(
    client_caps: AgentCapabilities,
    server_caps: AgentCapabilities,
) -> dict | None:
    """Negocia capacidades entre dos agentes.

    Retorna la configuracion acordada o None si son incompatibles.
    Similar a como HTTP negocia content-type via Accept headers.
    """
    # Encontrar formatos compatibles
    common_input = set(client_caps.output_formats) & set(
        server_caps.input_formats
    )
    common_output = set(server_caps.output_formats) & set(
        client_caps.input_formats
    )

    if not common_input or not common_output:
        return None  # incompatibles

    # Preferir JSON si esta disponible, si no el primero comun
    def prefer_json(formats: set) -> str:
        if "application/json" in formats:
            return "application/json"
        return next(iter(formats))

    return {
        "request_format": prefer_json(common_input),
        "response_format": prefer_json(common_output),
        "streaming": (
            client_caps.supports_streaming
            and server_caps.supports_streaming
        ),
        "async": (
            client_caps.supports_async
            and server_caps.supports_async
        ),
        "max_input_tokens": min(
            client_caps.max_input_tokens,
            server_caps.max_input_tokens,
        ),
        "confidence_reporting": (
            client_caps.confidence_reporting
            and server_caps.confidence_reporting
        ),
    }


# Ejemplo
client = AgentCapabilities(
    input_formats=["application/json"],
    output_formats=["application/json", "text/plain"],
    supports_streaming=True,
)
server = AgentCapabilities(
    input_formats=["application/json", "text/plain"],
    output_formats=["application/json"],
    supports_streaming=False,
)

agreement = negotiate_capabilities(client, server)
print(f"Acuerdo: {agreement}")
# {'request_format': 'application/json', 'response_format': 'application/json',
#  'streaming': False, 'async': True, ...}
```

---

## 10.6 Manejo de fallos en comunicacion distribuida

### Los fallos que no existen con un solo agente

Cuando dos o mas agentes se comunican a traves de una red, aparecen modos de fallo que son imposibles con un solo agente. Estos son los clasicos de los sistemas distribuidos, pero con un giro: los agentes de IA agregan fallos semanticos que no existen en los sistemas tradicionales.

**Timeout.** El agente B no responde. Puede estar caido, puede estar procesando, o puede haber un problema de red. El agente A no tiene forma de saber cual es el caso.

**Respuesta parcial.** El agente B empieza a responder (streaming) pero la conexion se corta a mitad. El agente A tiene media respuesta: usarla o descartarla?

**Respuesta incorrecta.** El agente B responde con formato perfecto pero contenido erroneo (alucinacion). No hay codigo de error; la respuesta *parece* correcta.

**Respuesta tardia.** El agente A ya hizo timeout y genero una respuesta alternativa. Luego llega la respuesta de B. Ahora hay dos respuestas para la misma peticion.

### Patron: reintentos con idempotencia

El primer mecanismo de defensa es el reintento, pero los reintentos sin idempotencia son peligrosos. Si la tarea es "envia un correo electronico", reintentar sin verificar si el correo ya se envio resulta en correos duplicados.

```python
"""
Reintentos con idempotencia para comunicacion entre agentes.
Garantiza que reintentar una operacion no produce efectos duplicados.
"""

import asyncio
import hashlib
import time
from dataclasses import dataclass


@dataclass
class RetryConfig:
    max_retries: int = 3
    base_delay: float = 1.0  # segundos
    max_delay: float = 30.0
    exponential_base: float = 2.0


class IdempotentAgentClient:
    """Cliente que reintenta con idempotencia.

    Cada peticion lleva un idempotency_key que permite al
    servidor detectar y deduplicar peticiones repetidas.
    """

    def __init__(self, config: RetryConfig = RetryConfig()):
        self.config = config
        self._response_cache: dict[str, dict] = {}

    def _generate_idempotency_key(
        self, skill_id: str, input_data: dict
    ) -> str:
        """Genera una clave unica para la combinacion de skill + input."""
        content = f"{skill_id}:{sorted(input_data.items())}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    async def send_with_retry(
        self,
        target_agent,
        skill_id: str,
        input_data: dict,
    ) -> dict:
        """Envia una peticion con reintentos y backoff exponencial."""
        idempotency_key = self._generate_idempotency_key(
            skill_id, input_data
        )

        # Si ya tenemos la respuesta cacheada, retornar
        if idempotency_key in self._response_cache:
            return self._response_cache[idempotency_key]

        last_error = None
        for attempt in range(self.config.max_retries + 1):
            try:
                result = await asyncio.wait_for(
                    target_agent.create_task(skill_id, input_data),
                    timeout=30.0,  # timeout por intento
                )

                # Cachear la respuesta para idempotencia
                response = {
                    "task_id": result.id,
                    "status": result.status.value,
                    "artifacts": [
                        {"name": a.name, "parts": a.parts}
                        for a in result.artifacts
                    ],
                }
                self._response_cache[idempotency_key] = response
                return response

            except asyncio.TimeoutError:
                last_error = f"Timeout en intento {attempt + 1}"
            except Exception as e:
                last_error = str(e)

            # Backoff exponencial con jitter
            if attempt < self.config.max_retries:
                delay = min(
                    self.config.base_delay
                    * (self.config.exponential_base ** attempt),
                    self.config.max_delay,
                )
                # Jitter: +/- 25% para evitar thundering herd
                import random
                jitter = delay * 0.25 * (2 * random.random() - 1)
                await asyncio.sleep(delay + jitter)

        raise RuntimeError(
            f"Todos los reintentos fallaron. Ultimo error: {last_error}"
        )
```

### Patron: circuit breaker para comunicacion inter-agente

El circuit breaker previene que un agente siga enviando peticiones a otro agente que esta fallando, evitando cascadas de fallos. Aplicamos el mismo patron que discutimos en el Capitulo 8 para el harness individual, pero ahora a nivel de comunicacion entre agentes.

```python
"""
Circuit breaker para comunicacion entre agentes.
Evita cascadas de fallos cuando un agente remoto falla.
"""

import time
from enum import Enum


class CircuitState(Enum):
    CLOSED = "closed"        # funcionando normal
    OPEN = "open"            # cortado, rechaza peticiones
    HALF_OPEN = "half_open"  # probando si el agente se recupero


class AgentCircuitBreaker:
    """Circuit breaker para la comunicacion con un agente remoto.

    Estados:
    - CLOSED: todo funciona, peticiones pasan normalmente.
    - OPEN: demasiados fallos, peticiones se rechazan inmediatamente.
    - HALF_OPEN: dejamos pasar una peticion de prueba.
    """

    def __init__(
        self,
        agent_name: str,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        half_open_max_calls: int = 1,
    ):
        self.agent_name = agent_name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: float = 0
        self.half_open_calls = 0

    def can_send(self) -> bool:
        """Verifica si se puede enviar una peticion."""
        if self.state == CircuitState.CLOSED:
            return True

        if self.state == CircuitState.OPEN:
            # Verificar si ya paso el tiempo de recuperacion
            elapsed = time.time() - self.last_failure_time
            if elapsed >= self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.half_open_calls = 0
                return True
            return False

        if self.state == CircuitState.HALF_OPEN:
            return self.half_open_calls < self.half_open_max_calls

        return False

    def record_success(self):
        """Registra una peticion exitosa."""
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
            self.failure_count = 0
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0  # resetear contador

    def record_failure(self):
        """Registra una peticion fallida."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN  # volver a abrir

        elif (
            self.state == CircuitState.CLOSED
            and self.failure_count >= self.failure_threshold
        ):
            self.state = CircuitState.OPEN

    def get_status(self) -> dict:
        return {
            "agent": self.agent_name,
            "state": self.state.value,
            "failures": self.failure_count,
            "threshold": self.failure_threshold,
        }


class ResilientAgentNetwork:
    """Red de agentes con circuit breakers por cada conexion.

    Cada par de agentes tiene su propio circuit breaker,
    permitiendo aislar fallos de agentes individuales.
    """

    def __init__(self):
        self._breakers: dict[str, AgentCircuitBreaker] = {}

    def get_breaker(self, agent_name: str) -> AgentCircuitBreaker:
        if agent_name not in self._breakers:
            self._breakers[agent_name] = AgentCircuitBreaker(agent_name)
        return self._breakers[agent_name]

    async def send(
        self,
        target_agent,
        skill_id: str,
        input_data: dict,
        fallback=None,
    ) -> dict:
        """Envia una peticion con proteccion de circuit breaker."""
        breaker = self.get_breaker(target_agent.card.name)

        if not breaker.can_send():
            if fallback:
                return await fallback(input_data)
            raise RuntimeError(
                f"Circuit breaker OPEN para {target_agent.card.name}. "
                f"Estado: {breaker.get_status()}"
            )

        try:
            result = await target_agent.create_task(skill_id, input_data)
            breaker.record_success()
            return {
                "status": result.status.value,
                "artifacts": [
                    {"name": a.name, "parts": a.parts}
                    for a in result.artifacts
                ],
            }
        except Exception as e:
            breaker.record_failure()
            if fallback and not breaker.can_send():
                return await fallback(input_data)
            raise

    def network_health(self) -> dict:
        """Vista general de la salud de la red de agentes."""
        return {
            name: breaker.get_status()
            for name, breaker in self._breakers.items()
        }
```

### Patron: dead letter queue para mensajes fallidos

Cuando un mensaje no puede ser entregado despues de todos los reintentos, no debe desaparecer silenciosamente. El patron dead letter queue (DLQ) captura estos mensajes para analisis posterior.

```python
"""
Dead letter queue para mensajes que no pudieron ser entregados.
Esencial para diagnosticar problemas en produccion.
"""

import time
from dataclasses import dataclass, field


@dataclass
class DeadLetter:
    """Mensaje que no pudo ser entregado."""
    original_message: dict
    target_agent: str
    error: str
    attempts: int
    first_attempt_at: float
    last_attempt_at: float = field(default_factory=time.time)


class DeadLetterQueue:
    """Almacena mensajes que no pudieron ser entregados.

    En produccion: usa una cola persistente (SQS, RabbitMQ)
    con alertas cuando la DLQ crece.
    """

    def __init__(self, max_size: int = 10_000):
        self._queue: list[DeadLetter] = []
        self.max_size = max_size

    def add(self, dead_letter: DeadLetter):
        if len(self._queue) >= self.max_size:
            self._queue.pop(0)  # FIFO: eliminar el mas viejo
        self._queue.append(dead_letter)

    def get_by_agent(self, agent_name: str) -> list[DeadLetter]:
        """Obtener mensajes fallidos para un agente especifico."""
        return [
            dl for dl in self._queue
            if dl.target_agent == agent_name
        ]

    def stats(self) -> dict:
        """Estadisticas de la DLQ para monitoreo."""
        by_agent: dict[str, int] = {}
        by_error: dict[str, int] = {}
        for dl in self._queue:
            by_agent[dl.target_agent] = (
                by_agent.get(dl.target_agent, 0) + 1
            )
            error_type = dl.error.split(":")[0]
            by_error[error_type] = by_error.get(error_type, 0) + 1

        return {
            "total": len(self._queue),
            "by_agent": by_agent,
            "by_error_type": by_error,
        }
```

---

## 10.7 El futuro: convergencia o fragmentacion

### Lecciones de la historia

La batalla entre SOAP y REST es especialmente instructiva. SOAP nacio en Microsoft e IBM como un protocolo formal con especificaciones extensas. REST, en cambio, era un estilo arquitectural descrito en una tesis doctoral. REST gano no porque fuera tecnicamente superior en todos los aspectos (SOAP tenia mejor soporte para transacciones empresariales), sino porque era **mas simple de adoptar** [Fielding, 2000]. Un desarrollador podia hacer su primera llamada REST con `curl` en un minuto. Hacer lo mismo con SOAP requeria configurar un framework, generar stubs desde un WSDL y pelear con namespaces XML.

La leccion para los protocolos de agentes: la simplicidad gana. MCP lo entendio: su diseno basado en JSON-RPC 2.0 es simple y pragmatico. A2A tambien, con conceptos claros (Agent Cards, Tasks, Artifacts).

Despues vino GraphQL (de Facebook, en 2015), que no reemplazo a REST sino que coexistio. Es probable que el ecosistema de protocolos de agentes siga un patron similar: multiples protocolos coexistiendo, cada uno optimizado para un caso de uso diferente.

### El escenario probable

MCP y A2A son complementarios. MCP resuelve la capa vertical (agente-herramienta), A2A la capa horizontal (agente-agente). La AAIF bajo la Linux Foundation coordina la convergencia, pero la historia sugiere que los mejores estandares emergen del uso practico y luego se formalizan, no al reves.

El riesgo es que la AAIF se convierta en un comite de estandares que produzca especificaciones infladas y desconectadas de la realidad (como le paso a CORBA). Los protocolos que sobreviviran seran los que los desarrolladores adopten por pragmatismo, no por mandato.

Lo que falta en ambos protocolos:

- **Descubrimiento semantico**: como busco "un agente que pueda analizar sentimiento en espanol con precision mayor al 90%"?
- **Delegacion de autoridad**: si el Agente A le pide al Agente B que use al Agente C, que permisos tiene C?
- **Manejo de errores semanticos**: un codigo de estado para "la respuesta es plausible pero no estoy seguro".
- **Negociacion de SLAs**: garantias de latencia, disponibilidad y costo entre agentes.

---

## 10.8 Ejercicio integrador: dos agentes colaborando

Para cerrar el capitulo, implementemos un escenario completo donde dos agentes colaboran usando los patrones que hemos discutido.

```python
"""
Ejercicio integrador: agente investigador y agente redactor
colaboran usando el patron blackboard con comunicacion
estructurada y manejo de fallos.
"""

import asyncio
import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class CollaborationConfig:
    """Configuracion para la colaboracion entre agentes."""
    max_iterations: int = 10
    timeout_per_agent: float = 30.0
    min_confidence: float = 0.7
    token_budget: int = 50_000


@dataclass
class ContributionLog:
    """Registro de una contribucion para trazabilidad."""
    agent: str
    action: str
    key: str
    confidence: float
    tokens_used: int
    duration_ms: float
    timestamp: float = field(default_factory=time.time)


class CollaborativeWorkspace:
    """Workspace que combina blackboard con logging y control de calidad."""

    def __init__(self, config: CollaborationConfig):
        self.config = config
        self.state: dict[str, Any] = {}
        self.log: list[ContributionLog] = []
        self.tokens_spent: int = 0
        self._lock = asyncio.Lock()

    async def contribute(
        self,
        agent_name: str,
        key: str,
        value: Any,
        confidence: float,
        tokens_used: int,
    ) -> bool:
        """Registra una contribucion con validaciones."""
        async with self._lock:
            # Verificar presupuesto de tokens
            if self.tokens_spent + tokens_used > self.config.token_budget:
                return False  # presupuesto agotado

            # Verificar confianza minima
            if confidence < self.config.min_confidence:
                self.log.append(ContributionLog(
                    agent=agent_name,
                    action="rejected_low_confidence",
                    key=key,
                    confidence=confidence,
                    tokens_used=0,
                    duration_ms=0,
                ))
                return False

            self.state[key] = {
                "value": value,
                "author": agent_name,
                "confidence": confidence,
            }
            self.tokens_spent += tokens_used

            self.log.append(ContributionLog(
                agent=agent_name,
                action="contributed",
                key=key,
                confidence=confidence,
                tokens_used=tokens_used,
                duration_ms=0,
            ))
            return True

    def summary(self) -> dict:
        """Resumen del workspace para monitoreo."""
        return {
            "state_keys": list(self.state.keys()),
            "total_contributions": len(self.log),
            "tokens_spent": self.tokens_spent,
            "tokens_remaining": (
                self.config.token_budget - self.tokens_spent
            ),
            "agents_involved": list(set(
                entry.agent for entry in self.log
            )),
        }


async def run_collaborative_research(pregunta: str):
    """Ejecuta una investigacion colaborativa entre agentes."""
    config = CollaborationConfig(
        max_iterations=10,
        timeout_per_agent=30.0,
        min_confidence=0.7,
        token_budget=50_000,
    )
    workspace = CollaborativeWorkspace(config)

    # Plantar la pregunta
    await workspace.contribute(
        "usuario", "pregunta", pregunta, confidence=1.0, tokens_used=0
    )

    # Fase 1: Investigacion
    # En produccion: llamada real al LLM con herramientas
    hallazgos = {
        "fuentes": [
            "MCP Specification 2025-11-25",
            "A2A Protocol v0.3",
        ],
        "datos_clave": [
            "MCP usa JSON-RPC 2.0",
            "A2A define Agent Cards para descubrimiento",
        ],
    }
    await workspace.contribute(
        "investigador", "hallazgos", hallazgos,
        confidence=0.88, tokens_used=3500,
    )

    # Fase 2: Redaccion
    borrador = (
        "Los protocolos MCP y A2A representan enfoques "
        "complementarios para la comunicacion entre agentes..."
    )
    await workspace.contribute(
        "redactor", "borrador", borrador,
        confidence=0.82, tokens_used=4200,
    )

    # Fase 3: Revision
    revision = {
        "aprobado": True,
        "mejoras": ["Agregar ejemplo de Agent Card"],
        "calidad": 0.85,
    }
    await workspace.contribute(
        "revisor", "revision", revision,
        confidence=0.90, tokens_used=2800,
    )

    print("=== Resumen de la colaboracion ===")
    print(json.dumps(workspace.summary(), indent=2))
    print(f"\n=== Estado final ===")
    for key, entry in workspace.state.items():
        print(f"  {key}: (autor: {entry['author']}, "
              f"confianza: {entry['confidence']})")

    return workspace


# Ejecutar
# asyncio.run(run_collaborative_research(
#     "Compara los protocolos MCP y A2A para agentes de IA"
# ))
```

---

## Takeaway del capitulo

Los protocolos de comunicacion son el "pegamento invisible" que hara posible sistemas multi-agente a escala. MCP resuelve la conexion agente-herramienta con una arquitectura simple basada en JSON-RPC 2.0. A2A resuelve la conexion agente-agente con Agent Cards, Tasks y Artifacts. Ambos son necesarios y complementarios.

Los patrones de comunicacion (request-response, pub-sub, blackboard) determinan la topologia logica de tu sistema y tienen trade-offs claros en acoplamiento, escalabilidad y facilidad de depuracion. Elige el patron correcto para cada tipo de interaccion.

El manejo de fallos en comunicacion distribuida requiere los mismos mecanismos que en microservicios (reintentos con idempotencia, circuit breakers, dead letter queues) mas mecanismos nuevos para fallos semanticos (validacion de confianza, verificacion cruzada).

La historia de los protocolos de internet sugiere que la simplicidad gana. El protocolo que se adopte masivamente sera el que un desarrollador pueda implementar en una tarde, no el que tenga la especificacion mas completa.

---

## Referencias

- Anthropic. "Model Context Protocol Specification." modelcontextprotocol.io, 2024-2025.
- Google. "Announcing the Agent2Agent Protocol (A2A)." Google Developers Blog, abril 2025.
- Fielding, R. T. "Architectural Styles and the Design of Network-Based Software Architectures." Tesis doctoral, UC Irvine, 2000.
- Berners-Lee, T., Fielding, R., Frystyk, H. "Hypertext Transfer Protocol -- HTTP/1.0." RFC 1945, 1996.
- Hayes-Roth, B. "A blackboard architecture for control." Artificial Intelligence, 26(3), 1985.
- Sun, Y., et al. "IBGP: Imperfect Byzantine Generals Problem for Multi-Agent Systems." arXiv, 2024.
- "The Orchestration of Multi-Agent Systems: Architectures, Protocols, and Enterprise Adoption." arXiv:2601.13671, enero 2026.
- "A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, and ANP." arXiv:2505.02279, mayo 2025.
