---
title: "El protocolo que falta: comunicación entre agentes de IA más allá del texto libre"
date: 2026-04-02
author: "Héctor Patricio"
tags: ['agentes', 'protocolos', 'MCP', 'A2A', 'inteligencia-artificial', 'sistemas-distribuidos', 'arquitectura', 'llm']
description: "Así como HTTP estandarizó la web, los agentes de IA necesitan protocolos de comunicación estandarizados. Analizamos MCP, A2A, los paralelos con sistemas distribuidos y qué necesita un verdadero protocolo de agentes."
featuredImage: ""
draft: true
---

En 1991, Tim Berners-Lee publicó HTTP/0.9: un protocolo mínimo con un único método GET, sin headers, que devolvía texto plano. Nadie sabía que ese pequeño protocolo de transferencia de hipertexto se convertiría en el pegamento invisible de la web moderna. Para 1996, cuando HTTP/1.0 se formalizó como RFC 1945, ya era evidente que la estandarización no fue un lujo: fue la condición necesaria para que internet dejara de ser un experimento académico y se convirtiera en la infraestructura que conocemos.

Hoy estamos viviendo un momento similar con los agentes de IA. Tenemos agentes que pueden razonar, usar herramientas, planificar y ejecutar tareas complejas. Pero cuando necesitan comunicarse entre sí, la situación se parece mucho a la internet pre-HTTP: cada framework, cada laboratorio y cada empresa define su propio formato de comunicación. Texto libre, JSON ad-hoc, formatos propietarios.

En la serie de artículos sobre [Entendiendo REST](/2019/06/15/entendiendo-rest-estilo-de-arquitectura.html) analizamos cómo un estilo arquitectural bien diseñado puede definir la forma en que sistemas distribuidos se comunican. También en [HTTP/1.1, HTTP/2 y HTTP/3](/2021/12/15/http-1-1-http-2-y-http-3.html) vimos cómo un protocolo evoluciona para adaptarse a las necesidades cambiantes de la industria. Ahora, es momento de preguntarnos: **¿cuál es el HTTP de los agentes de IA?**

La respuesta corta es que todavía no existe. Pero varios candidatos están compitiendo por serlo, y las lecciones de la historia nos pueden ayudar a entender qué funcionará y qué no.

## Lecciones de los protocolos clásicos: qué los hace funcionar

Antes de analizar los protocolos emergentes para agentes, vale la pena entender qué hace que un protocolo de comunicación sea exitoso. No todos los protocolos sobreviven. Los que lo hacen comparten ciertas características fundamentales.

### Contratos claros

TCP/IP funciona porque define un contrato inequívoco: cómo se establece una conexión (el famoso three-way handshake), cómo se transmiten los datos (en segmentos numerados), cómo se confirma la recepción (ACKs) y cómo se cierra la conexión. No hay ambigüedad. Cada participante sabe exactamente qué esperar del otro.

HTTP llevó esta idea al nivel de aplicación. Una petición HTTP tiene una estructura predecible: un método (GET, POST, PUT, DELETE), una URI que identifica el recurso, headers que definen metadatos y opcionalmente un cuerpo. La respuesta tiene un código de estado numérico que comunica el resultado de manera no ambigua: 200 es éxito, 404 es recurso no encontrado, 500 es error del servidor. Este contrato permite que un navegador desarrollado en Japón se comunique perfectamente con un servidor desarrollado en Brasil, sin que sus creadores se hayan conocido jamás.

### Versionado y evolución

Como analizamos en el artículo sobre [HTTP/1.1, HTTP/2 y HTTP/3](/2021/12/15/http-1-1-http-2-y-http-3.html), los protocolos exitosos evolucionan sin romper lo existente. HTTP/2 introdujo multiplexación de conexiones, pero un servidor HTTP/2 puede negociar hacia abajo con un cliente que solo habla HTTP/1.1. HTTP/3 reemplazó TCP por QUIC como capa de transporte, pero la semántica de la aplicación se mantuvo esencialmente igual.

gRPC, el framework de Google para RPCs de alto rendimiento, usa Protocol Buffers con un sistema de versionado explícito. Los campos nuevos son opcionales por defecto, lo que permite que clientes antiguos se comuniquen con servidores nuevos sin romperse.

### Manejo de errores predecible

Un protocolo que no define cómo manejar errores es un protocolo incompleto. TCP retransmite paquetes perdidos. HTTP define códigos de error semánticos. gRPC tiene un sistema de códigos de estado (OK, CANCELLED, DEADLINE_EXCEEDED, NOT_FOUND, PERMISSION_DENIED) que permite a los clientes reaccionar programáticamente a diferentes tipos de fallos.

Esta lección es especialmente relevante para los agentes de IA, donde los errores son fundamentalmente diferentes: un agente puede dar una respuesta incorrecta sin generar ningún error técnico. ¿Cómo codificas "la respuesta es plausible pero no estoy seguro" en un código de estado?

### La regla de oro: simplicidad

Los protocolos que sobreviven son los que pueden explicarse en pocas páginas. El RFC de HTTP/1.0 (RFC 1945, publicado en 1996) tenía 60 páginas. El de TCP (RFC 793) tenía 85. En contraste, las especificaciones de SOAP y WS-\* sumaban miles de páginas, y ya sabemos quién ganó esa batalla. Roy Fielding describió REST como un estilo arquitectural, no como un protocolo, y precisamente esa flexibilidad fue su mayor fortaleza.

## El estado actual: MCP, A2A y el caos organizado

Entremos al presente. En 2025 y 2026, tres propuestas principales compiten por definir cómo se comunican los agentes de IA. Cada una ataca el problema desde un ángulo diferente, y entenderlas requiere entender qué problema específico está resolviendo cada una.

### Model Context Protocol (MCP): el USB-C de los agentes

Anthropic lanzó MCP en noviembre de 2024 como un protocolo abierto para conectar modelos de lenguaje con herramientas y fuentes de datos externas. La analogía que mejor lo describe es la de un **puerto USB-C**: así como USB-C estandarizó la conexión entre dispositivos y periféricos, MCP estandariza la conexión entre un agente y las herramientas que puede usar.

MCP se basa en **JSON-RPC 2.0**, el mismo protocolo de llamadas a procedimientos remotos que ya se usa ampliamente en editores de código (el Language Server Protocol de VS Code es primo hermano de MCP). La arquitectura es simple y elegante:

- **Host**: La aplicación que contiene al modelo de lenguaje (Claude Desktop, Cursor, VS Code, tu aplicación personalizada).
- **Client**: El componente que se comunica con los servidores MCP desde dentro del host.
- **Server**: Un servicio que expone herramientas, recursos o prompts al modelo.

Un servidor MCP puede exponer, por ejemplo, acceso a una base de datos, a un sistema de archivos, a una API externa o a cualquier funcionalidad que quieras darle a tu agente. Originalmente, la comunicación se transportaba sobre STDIO (para servidores locales), pero para marzo de 2026 los **remote MCP servers** son una feature de primera clase: se comunican sobre HTTP con Server-Sent Events (SSE) o WebSocket como transporte de streaming, con autenticación **OAuth 2.1** nativa. El ecosistema ha crecido masivamente, con hubs como Smithery y el MCP Registry oficial que facilitan el descubrimiento de servidores disponibles.

> **Nota**: La especificación MCP sigue evolucionando rápidamente. Consulta la documentación oficial en [modelcontextprotocol.io](https://modelcontextprotocol.io) para el estado más actualizado.

Veamos cómo se ve una interacción MCP a nivel de mensajes JSON-RPC:

```json
// El cliente descubre las herramientas disponibles
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}

// El servidor responde con las herramientas y sus schemas
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "buscar_producto",
        "description": "Busca productos en el catálogo",
        "inputSchema": {
          "type": "object",
          "properties": {
            "query": { "type": "string" },
            "categoria": { "type": "string" }
          },
          "required": ["query"]
        }
      }
    ]
  }
}

// El cliente invoca una herramienta
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "buscar_producto",
    "arguments": {
      "query": "laptop gaming",
      "categoria": "electrónica"
    }
  }
}
```

Para diciembre de 2025, MCP reportaba más de 97 millones de descargas mensuales de sus SDKs, con más de 10,000 servidores activos en producción. OpenAI adoptó oficialmente el protocolo en marzo de 2025, integrándolo en ChatGPT Desktop. Múltiples IDEs y herramientas de desarrollo (Claude Desktop, Cursor, VS Code, Windsurf, entre otros) lo soportan de forma nativa. En diciembre de 2025, Anthropic donó MCP a la **Agentic AI Foundation (AAIF)** bajo la Linux Foundation, con Anthropic, OpenAI y Block como co-fundadores.

**Pero MCP tiene un límite fundamental**: resuelve la comunicación entre un agente y sus herramientas, pero **no** la comunicación entre agentes. Es como si tuviéramos un estándar excelente para que un navegador hable con plugins, pero no para que dos navegadores se comuniquen entre sí.

### Agent-to-Agent Protocol (A2A): la propuesta de Google

Google lanzó A2A en abril de 2025 precisamente para llenar el vacío que MCP deja. Si MCP es el USB-C, A2A es más parecido a HTTP: define cómo dos agentes que no se conocen entre sí pueden descubrirse, comunicarse y colaborar.

A2A introduce varios conceptos clave:

**Agent Card**: Un documento JSON que cada agente publica en `/.well-known/agent.json`, describiendo su identidad, capacidades, habilidades específicas y requisitos de autenticación. Es el equivalente a un currículum profesional que cada agente lleva colgado del cuello.

```json
{
  "name": "agente-analisis-financiero",
  "description": "Analiza estados financieros y genera reportes",
  "url": "https://agentes.ejemplo.com/financiero",
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false
  },
  "skills": [
    {
      "id": "analisis-balance",
      "name": "Análisis de Balance General",
      "description": "Analiza un balance general y detecta anomalías",
      "inputModes": ["application/json"],
      "outputModes": ["application/json", "text/markdown"]
    }
  ],
  "authentication": {
    "schemes": ["oauth2"]
  }
}
```

**Tasks**: La unidad fundamental de trabajo. Un agente cliente crea una tarea que pasa por un ciclo de vida definido: `submitted` -> `working` -> `completed` (o `failed`, `canceled`). Las tareas pueden ser instantáneas o de larga duración.

**Artifacts**: Los resultados que un agente genera al completar una tarea. Pueden ser documentos, imágenes, datos estructurados o cualquier tipo de contenido, organizados en "Parts" (la unidad mínima de contenido).

Toda la comunicación en A2A ocurre sobre **HTTP(S)** usando **JSON-RPC 2.0** como formato de payload, soportando tres modos de interacción: request/response síncrono, streaming con Server-Sent Events (SSE) y notificaciones push asíncronas.

La versión 0.3 del protocolo, publicada en 2025, añadió soporte para gRPC y la capacidad de firmar digitalmente las Agent Cards, un requisito fundamental para escenarios empresariales donde necesitas verificar que un agente es quien dice ser.

A2A fue contribuido a la Linux Foundation como proyecto open source bajo licencia Apache 2.0, con más de 50 socios tecnológicos incluyendo a AWS, Microsoft y Salesforce.

### OpenAI Agents SDK y los "handoffs"

OpenAI tomó un camino diferente. En lugar de definir un protocolo de comunicación entre agentes independientes, su Agents SDK (lanzado en marzo de 2025 como evolución del proyecto experimental Swarm) define un mecanismo de **handoffs** dentro de un mismo sistema.

Un handoff permite que un agente delegue una tarea a otro agente especializado. Los handoffs se representan como herramientas para el LLM: si tienes un agente llamado "Agente de Reembolsos", el LLM ve una herramienta llamada `transfer_to_refund_agent` que puede invocar.

```python
from agents import Agent, handoff

agente_soporte = Agent(
    name="Soporte General",
    instructions="Atiende consultas generales. Si el cliente "
                 "quiere un reembolso, transfiere al agente de reembolsos.",
    handoffs=[
        handoff(agente_reembolsos),
        handoff(agente_ventas)
    ]
)

agente_reembolsos = Agent(
    name="Agente de Reembolsos",
    instructions="Procesa solicitudes de reembolso.",
    tools=[verificar_orden, procesar_reembolso]
)
```

Este enfoque es pragmático y funciona bien dentro de un mismo sistema, pero no resuelve el problema de la interoperabilidad entre sistemas de diferentes organizaciones. No es un protocolo de comunicación: es un patrón de orquestación interna.

OpenAI también contribuyó **AGENTS.md** a la AAIF, una especificación que funciona como un archivo de instrucciones para agentes de código (adoptado por más de 60,000 proyectos open source), pero esto es más una convención que un protocolo de comunicación.

### El problema: cada laboratorio crea su propio estándar

Hay un chiste clásico en la ingeniería de software: "Lo bueno de los estándares es que hay muchos para elegir." La situación actual con los protocolos de agentes encaja perfectamente en el famoso [xkcd sobre estándares](https://xkcd.com/927/): alguien ve 14 estándares competidores, decide crear uno universal, y ahora hay 15.

Pero la situación no es tan caótica como parece. Si lo analizamos con cuidado, MCP y A2A no compiten directamente: operan en **capas diferentes**. MCP estandariza cómo un agente accede a herramientas y datos (la capa vertical, agente-a-herramienta). A2A estandariza cómo dos agentes colaboran entre sí (la capa horizontal, agente-a-agente). Un sistema completo podría usar ambos: cada agente usa MCP internamente para conectarse con sus herramientas, y A2A externamente para comunicarse con otros agentes.

También hay propuestas adicionales como el **Agent Network Protocol (ANP)**, que agrega una capa de descubrimiento descentralizado usando endpoints `/.well-known/agent-descriptions` y un sistema de negociación de protocolos basado en lenguaje natural. Y el **Agent Communication Protocol (ACP)**, que se enfoca en escenarios empresariales.

### El costo oculto de la comunicación: latencia, tokens y dinero

Antes de seguir con los requisitos teóricos, hay que hablar de la cruda realidad de producción: la comunicación entre agentes no es gratis. Cada "hop" entre agentes que pasa por la API de un LLM añade entre 0.5 y 3 segundos de latencia. Un sistema con 5 hops ya acumula de 2.5 a 15 segundos solo de latencia de comunicación, sin contar el procesamiento real.

Esto tiene consecuencias directas en el diseño. He visto equipos abandonar arquitecturas multi-agente elegantes porque la latencia total excedía el SLA del producto. La regla práctica es: **cada agente adicional en una cadena debe justificar la latencia que introduce**. Si un solo agente con mejor prompting puede resolver el problema en 2 segundos, no lo conviertas en una cadena de 3 agentes que tarda 8 segundos.

Además del tiempo, cada mensaje entre agentes consume tokens (y por tanto dinero). El contexto de la tarea, los system prompts y los metadatos del protocolo se repiten en cada llamada. Un protocolo eficiente debe minimizar esta redundancia, por ejemplo, usando referencias a contextos compartidos en lugar de copiar el contexto completo en cada mensaje.

## ¿Qué necesita un protocolo de agentes?

Independientemente de qué protocolo gane la carrera (o si terminamos con un ecosistema complementario), hay requisitos fundamentales que cualquier solución seria debe resolver. Pensemos en estos desde los principios de diseño de software que hemos discutido en la serie sobre [A Philosophy of Software Design](/2019/07/04/a-philosophy-of-software-design-programacion-tactica-vs-estrategica.html).

### Discovery: ¿cómo sabe un agente qué puede hacer otro?

En la web, descubrir servicios es relativamente sencillo: tienes URLs, DNS, y motores de búsqueda. Para los agentes, el problema es más sutil. Un agente necesita saber no solo *dónde* está otro agente, sino *qué* puede hacer, *cómo* espera recibir la información y *qué garantías* ofrece.

A2A resuelve esto con las Agent Cards en `/.well-known/agent.json`. ANP propone un directorio de descubrimiento más elaborado. Pero ninguna solución ha resuelto completamente el problema de **descubrimiento semántico**: ¿cómo busco "un agente que pueda analizar sentimiento en textos en español con precisión mayor al 90%"? Las descripciones en texto natural son ambiguas, y los schemas estructurados no capturan toda la semántica.

Este es un problema que recuerda al que enfrentó la web con UDDI (Universal Description, Discovery and Integration) para servicios SOAP. UDDI intentó crear un directorio universal de servicios web y fracasó espectacularmente. La web resolvió el descubrimiento de otra forma: con links, motores de búsqueda y documentación legible por humanos. ¿Será similar para los agentes?

En la práctica de producción, el service discovery de agentes se resuelve hoy con tres patrones: **registros estáticos** (archivos de configuración que listan los agentes disponibles y sus endpoints), **registros dinámicos** (adaptaciones de herramientas como Consul o etcd donde los agentes se registran al iniciar), y **convenciones de descubrimiento** como la Agent Card de A2A en `/.well-known/agent.json` o los registros de servidores MCP. Ninguno resuelve el descubrimiento semántico abierto, pero cubren los casos más comunes en producción.

### Negociación de capacidades

Dos agentes que se encuentran necesitan negociar cómo van a comunicarse. ¿Qué formatos de entrada y salida soportan? ¿Qué nivel de confiabilidad ofrecen? ¿Pueden hacer streaming o solo request/response? ¿Cuánto tardan típicamente en responder?

ANP propone algo fascinante: una **negociación de meta-protocolo** donde los agentes usan lenguaje natural para acordar los detalles de su comunicación. Esto es conceptualmente elegante pero introduce una capa de incertidumbre que contradice el principio de los contratos claros que mencionamos arriba. Si dos agentes tienen que "ponerse de acuerdo" sobre cómo van a hablar, la conversación sobre la conversación puede fallar.

La alternativa es más aburrida pero más robusta: capacidades enumeradas explícitamente en una especificación, como lo hace A2A con sus Agent Cards. Es lo que Tim Berners-Lee habría elegido: prefirió que HTTP soportara un conjunto finito de métodos bien definidos en lugar de un protocolo "extensible infinitamente".

### Contratos de entrada y salida (schemas)

Aquí es donde la experiencia con APIs tradicionales es directamente aplicable. Un agente que ofrece un servicio debe publicar un schema que defina exactamente qué espera recibir y qué va a devolver. JSON Schema es el candidato natural para esto, y tanto MCP como A2A ya lo usan.

Pero los agentes de IA agregan una complicación: la salida no es determinista. El mismo input puede producir diferentes outputs en diferentes invocaciones. ¿Cómo capturas eso en un schema? Una posibilidad es incluir metadatos de confianza:

```json
{
  "result": {
    "analysis": "El balance muestra una posición de liquidez saludable...",
    "confidence": 0.87,
    "model_used": "claude-4-sonnet",
    "reasoning_tokens": 2048,
    "alternatives_considered": 3
  }
}
```

Esto se conecta con lo que discutimos en [Patrones de diseño para sistemas con IA](/2026/02/15/patrones-de-diseno-para-sistemas-con-ia.html): el principio de separar la inteligencia de la lógica. El schema debe capturar no solo el resultado sino los metadatos que permitan al agente consumidor decidir qué tan confiable es la respuesta.

### Manejo de estado y sesiones

Los protocolos clásicos van desde completamente sin estado (HTTP 1.1 en su forma pura, como analizamos en [Entendiendo REST: Servidor sin Estado](/2019/07/02/entendiendo-rest-servidor-sin-estado.html)) hasta completamente con estado (una conexión TCP). Los agentes de IA necesitan algo intermedio.

Una conversación entre agentes puede durar segundos (una consulta simple) o días (un proyecto de investigación colaborativo). El protocolo necesita soportar ambos extremos. A2A resuelve esto con su modelo de Tasks que tienen un ciclo de vida y un identificador persistente. Una tarea puede crearse, recibir actualizaciones incrementales y completarse en cualquier momento, similar a cómo una conexión WebSocket mantiene estado pero permite mensajes independientes.

### Autenticación y autorización entre agentes

Este es quizá el problema más difícil y menos resuelto. Cuando un humano usa una API, se autentica con una API key o un token OAuth. Pero cuando un agente autónomo necesita actuar en nombre de un usuario humano y comunicarse con otro agente que actúa en nombre de otro usuario, las cadenas de confianza se vuelven complicadas.

A2A soporta OAuth 2.0 en sus Agent Cards, y la versión 0.3 introdujo la firma digital de Agent Cards. Pero queda abierta una pregunta fundamental: ¿cómo se delega autorización en una cadena de agentes? Si el Agente A le pide al Agente B que use al Agente C para completar una tarea, ¿qué permisos tiene el Agente C? ¿Puede actuar con los mismos privilegios del usuario original?

Este es el problema de la **delegación de autoridad**, bien conocido en la seguridad informática. Protocolos como Macaroons (de Google) y SPIFFE/SPIRE intentan resolverlo para microservicios, pero adaptarlos al contexto de agentes de IA con comportamiento no determinista agrega una nueva dimensión de riesgo.

## El paralelo con los sistemas distribuidos

Si estudias la teoría de sistemas distribuidos, te darás cuenta de que los problemas de comunicación entre agentes de IA no son nuevos. Son versiones modernas de problemas que la ciencia de la computación lleva décadas estudiando. Hablamos de esta relación entre la computación teórica y la práctica en [Máquinas de Turing no deterministas y problemas NP](/2023/02/10/maquinas-de-turing-no-deterministas-y-problemas-np.html), y aquí el paralelo es igual de revelador.

### El problema de los generales bizantinos aplicado a agentes

El problema de los generales bizantinos, formulado por Lamport, Shostak y Pease en 1982, describe una situación en la que un grupo de generales debe acordar un plan de ataque, pero algunos de ellos pueden ser traidores que envían información falsa. La pregunta es: ¿cómo pueden los generales leales llegar a un consenso?

Traducido al mundo de los agentes: ¿cómo puede un sistema multi-agente llegar a una conclusión correcta cuando algunos agentes pueden estar produciendo resultados incorrectos (por alucinaciones, sesgos del entrenamiento, o incluso manipulación adversarial)?

La investigación reciente explora esta conexión. El trabajo más relevante es **"IBGP: Imperfect Byzantine Generals Problem"** (Sun et al., 2024), que formaliza una versión refinada del problema para sistemas multi-agente comunicativos: el consenso no necesita ser perfecto sino *suficientemente bueno*. Esto refleja la naturaleza inherentemente probabilística de los LLMs: no necesitamos que todos los agentes estén de acuerdo en la respuesta exacta, sino que el sistema converja hacia una respuesta útil.

Vale aclarar que estas son investigaciones preliminares, no resultados consolidados al nivel del teorema original de Lamport-Shostak-Pease. Otros trabajos en la misma línea incluyen **BlockAgents** (Zhang et al., 2024), que propone un mecanismo de consenso llamado *proof-of-thought*, y **CP-WBFT** (Li et al., 2025), un mecanismo de tolerancia a fallos ponderado por confianza. En conjunto, sugieren que los sistemas multi-agente pueden ser más resilientes que los sistemas distribuidos clásicos si aprovechan la capacidad de los LLMs para evaluar la calidad de las respuestas de otros agentes, pero estas ideas todavía están en fase experimental.

### La tensión CAP en sistemas multi-agente

El teorema CAP de Brewer, en su formulación técnica precisa, establece que un sistema distribuido de registros de lectura/escritura no puede garantizar simultáneamente linearizabilidad (Consistencia), Disponibilidad y tolerancia a Particiones de red. Aunque CAP se refiere específicamente a almacenamiento distribuido, la tensión que describe es una metáfora útil para pensar en sistemas multi-agente:

- **Consistencia** (en el sentido informal): Todos los agentes tienen la misma información y producen respuestas coherentes entre sí.
- **Disponibilidad**: Cualquier agente puede responder a una solicitud en un tiempo razonable.
- **Tolerancia a Particiones**: El sistema sigue funcionando aunque algunos agentes sean inalcanzables.

En la práctica, los sistemas multi-agente de hoy sacrifican consistencia (aceptan que diferentes agentes pueden dar respuestas ligeramente diferentes) a favor de disponibilidad y tolerancia a particiones, de forma análoga a los sistemas AP como DynamoDB o Cassandra.

Pero hay contextos donde la consistencia importa. Si dos agentes financieros están procesando la misma transacción, no puedes aceptar inconsistencias. Aquí necesitarías algo parecido al consenso distribuido (como Raft o Paxos) adaptado al contexto agéntico.

### Tolerancia a fallos

En sistemas distribuidos clásicos, un nodo falla de manera clara: se cae, se desconecta, o produce un error. Los agentes de IA fallan de formas mucho más sutiles. Un agente puede:

- Responder con información incorrecta pero plausible (alucinación).
- Responder correctamente pero con un nivel de detalle insuficiente.
- Responder fuera de su dominio de competencia sin señalarlo.
- Responder de forma diferente ante la misma pregunta (no determinismo).

Los protocolos de agentes necesitan mecanismos para detectar y manejar estos tipos de fallos que no existen en los sistemas distribuidos tradicionales. Una aproximación prometedora es la de **agentes verificadores**: un tercer agente que evalúa la calidad de la interacción entre dos agentes, similar a cómo un load balancer con health checks detecta nodos enfermos, pero con evaluación semántica.

## Hacia un estándar: qué podemos aprender de la historia

La historia de la estandarización tecnológica está llena de lecciones que aplican directamente al momento actual de los protocolos de agentes.

### La guerra de los navegadores y la estandarización web

En los años 90, Netscape e Internet Explorer implementaban HTML y JavaScript de formas incompatibles. Los desarrolladores tenían que escribir código diferente para cada navegador, una pesadilla que retrasó el avance de la web durante años.

La solución no vino de que un navegador "ganara" la guerra. Vino del W3C, un organismo neutral que definió estándares que todos los navegadores aceptaron implementar (eventualmente). La creación de la **Agentic AI Foundation (AAIF)** bajo la Linux Foundation en diciembre de 2025 parece seguir el mismo camino: un espacio neutral donde competidores (Anthropic, OpenAI, Google, Microsoft, AWS) pueden acordar estándares comunes.

### SOAP vs REST vs GraphQL

La batalla entre SOAP y REST es especialmente instructiva. SOAP nació en Microsoft e IBM como un protocolo formal con especificaciones extensas (WS-Security, WS-ReliableMessaging, WS-Addressing... la lista de especificaciones "WS-*" parecía infinita). REST, en cambio, era un estilo arquitectural descrito en una tesis doctoral, sin un protocolo formal.

REST ganó no porque fuera técnicamente superior en todos los aspectos (SOAP tenía mejor soporte para transacciones y seguridad empresarial), sino porque era **más simple de adoptar**. Un desarrollador podía hacer su primera llamada REST con `curl` en un minuto. Hacer lo mismo con SOAP requería configurar un framework, generar stubs desde un WSDL y pelear con namespaces XML.

La lección para los protocolos de agentes es clara: **la simplicidad gana**. El protocolo que se adopte masivamente será el que un desarrollador pueda implementar en una tarde, no el que tenga la especificación más completa. MCP entendió esto: su diseño basado en JSON-RPC 2.0 es simple y pragmático. A2A también lo entendió, usando JSON-RPC sobre HTTP(S) con conceptos claros (Agent Cards, Tasks, Artifacts).

Después vino GraphQL (de Facebook, en 2015), que no reemplazó a REST sino que coexistió con él, ofreciendo ventajas específicas para ciertos casos de uso (consultas flexibles, evitar over-fetching). Es probable que el ecosistema de protocolos de agentes siga un patrón similar: múltiples protocolos coexistiendo, cada uno optimizado para un caso de uso diferente.

### El papel de los RFCs y la AAIF

Los RFCs (Request for Comments) han sido el mecanismo más exitoso para estandarizar protocolos de internet. Su nombre es engañosamente modesto: un RFC publicado no es una "solicitud de comentarios" sino una especificación formal que define cómo funciona parte de internet.

La AAIF podría jugar un papel similar para los protocolos de agentes. Sus proyectos fundacionales (MCP, AGENTS.md y goose) son un punto de partida, pero el verdadero valor estará en el proceso de estandarización que facilite: propuestas públicas, revisión por pares, implementaciones de referencia y tests de conformidad.

El riesgo es que la AAIF se convierta en un "comité de estándares" que produzca especificaciones infladas y desconectadas de la realidad (como le pasó a CORBA y a partes de SOAP). La historia sugiere que los mejores estándares emergen del uso práctico y luego se formalizan, no al revés.

## Ejemplo práctico: implementando un protocolo simple de comunicación entre agentes

Para hacer tangible todo lo que hemos discutido, implementemos un protocolo minimalista de comunicación entre agentes usando JSON-RPC 2.0 sobre HTTP. No pretende ser un estándar completo sino una ilustración de los conceptos fundamentales.

### Definición del protocolo

Nuestro protocolo define tres operaciones:

1. **`agent/discover`**: Obtener las capacidades de un agente.
2. **`task/create`**: Crear una tarea para que un agente la ejecute.
3. **`task/status`**: Consultar el estado de una tarea.

```python
"""
Protocolo simple de comunicación entre agentes.
Implementación de referencia usando JSON-RPC 2.0 sobre HTTP.
"""

import json
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any


class TaskStatus(Enum):
    SUBMITTED = "submitted"
    WORKING = "working"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentCard:
    """Tarjeta de identidad del agente: quién es y qué puede hacer."""
    name: str
    description: str
    version: str
    skills: list[dict]
    input_modes: list[str] = field(
        default_factory=lambda: ["application/json"]
    )
    output_modes: list[str] = field(
        default_factory=lambda: ["application/json"]
    )


@dataclass
class Task:
    """Unidad fundamental de trabajo entre agentes."""
    id: str
    status: TaskStatus
    input_data: dict
    skill_id: str
    result: Any = None
    error: str | None = None


class AgentServer(BaseHTTPRequestHandler):
    """
    Servidor que implementa el protocolo de agente.
    Cada instancia representa un agente con capacidades específicas.

    Nota: BaseHTTPRequestHandler es single-threaded. En producción
    usarías FastAPI con async/await, o al menos ThreadingHTTPServer,
    para manejar múltiples requests concurrentes. Este ejemplo prioriza
    la claridad sobre la robustez.
    """

    # Almacenamiento compartido a nivel de clase. En producción usarías
    # una base de datos con protección contra acceso concurrente.
    # Lo inicializamos aquí por simplicidad; en código real, usa __init__
    # del servidor o inyección de dependencias para evitar estado mutable
    # compartido entre instancias.
    tasks: dict[str, Task] = {}

    # Definición del agente - personalizar por cada agente
    agent_card = AgentCard(
        name="agente-resumen",
        description="Resume textos largos extrayendo los puntos clave",
        version="0.1.0",
        skills=[
            {
                "id": "resumir-texto",
                "name": "Resumir texto",
                "description": "Genera un resumen conciso de un texto largo",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "texto": {"type": "string"},
                        "max_palabras": {
                            "type": "integer",
                            "default": 200
                        }
                    },
                    "required": ["texto"]
                }
            }
        ]
    )

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        body = json.loads(self.rfile.read(content_length))

        # Despachar según el método JSON-RPC
        method = body.get("method")
        params = body.get("params", {})
        req_id = body.get("id")

        handlers = {
            "agent/discover": self._handle_discover,
            "task/create": self._handle_create_task,
            "task/status": self._handle_task_status,
        }

        handler = handlers.get(method)
        if handler is None:
            self._send_error(req_id, -32601, f"Método no encontrado: {method}")
            return

        try:
            result = handler(params)
            self._send_response(req_id, result)
        except Exception as e:
            self._send_error(req_id, -32000, str(e))

    def _handle_discover(self, params: dict) -> dict:
        """Devuelve la Agent Card con las capacidades del agente."""
        return asdict(self.agent_card)

    def _handle_create_task(self, params: dict) -> dict:
        """Crea una nueva tarea y la procesa."""
        skill_id = params.get("skill_id")
        input_data = params.get("input", {})

        # Verificar que el skill existe
        valid_skills = [s["id"] for s in self.agent_card.skills]
        if skill_id not in valid_skills:
            raise ValueError(
                f"Skill '{skill_id}' no disponible. "
                f"Skills disponibles: {valid_skills}"
            )

        task = Task(
            id=str(uuid.uuid4()),
            status=TaskStatus.SUBMITTED,
            input_data=input_data,
            skill_id=skill_id
        )

        # En un sistema real, aquí llamarías al LLM
        # Por ahora, simulamos el procesamiento
        task.status = TaskStatus.COMPLETED
        task.result = {
            "resumen": f"Resumen del texto ({len(input_data.get('texto', ''))} chars)",
            "confidence": 0.92,
            "palabras_originales": len(
                input_data.get("texto", "").split()
            ),
        }

        self.tasks[task.id] = task
        return {
            "task_id": task.id,
            "status": task.status.value
        }

    def _handle_task_status(self, params: dict) -> dict:
        """Consulta el estado y resultado de una tarea."""
        task_id = params.get("task_id")
        task = self.tasks.get(task_id)

        if task is None:
            raise ValueError(f"Tarea no encontrada: {task_id}")

        response = {
            "task_id": task.id,
            "status": task.status.value
        }
        if task.status == TaskStatus.COMPLETED:
            response["result"] = task.result
        if task.error:
            response["error"] = task.error
        return response

    def _send_response(self, req_id: int, result: dict):
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": result
        }
        self._write_json(200, response)

    def _send_error(self, req_id: int, code: int, message: str):
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": code, "message": message}
        }
        # HTTP 200 es correcto aquí: en JSON-RPC 2.0, los errores de
        # aplicación se comunican en el cuerpo JSON (campo "error"),
        # no mediante códigos HTTP. El código HTTP solo refleja el
        # estado del transporte, no de la lógica de negocio.
        self._write_json(200, response)

    def _write_json(self, status: int, data: dict):
        payload = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8080), AgentServer)
    print("Agente escuchando en http://localhost:8080")
    server.serve_forever()
```

### El cliente: un agente que descubre y usa a otro

```python
"""
Cliente que descubre y utiliza otro agente mediante el protocolo.
"""

import json
import requests


def jsonrpc_call(url: str, method: str, params: dict = None) -> dict:
    """Envía una petición JSON-RPC 2.0."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {}
    }
    resp = requests.post(url, json=payload)
    data = resp.json()

    if "error" in data:
        raise RuntimeError(
            f"Error del agente: {data['error']['message']}"
        )
    return data["result"]


def main():
    agent_url = "http://localhost:8080"

    # 1. Descubrir las capacidades del agente remoto
    card = jsonrpc_call(agent_url, "agent/discover")
    print(f"Agente encontrado: {card['name']}")
    print(f"Descripción: {card['description']}")
    print(f"Skills disponibles:")
    for skill in card["skills"]:
        print(f"  - {skill['id']}: {skill['description']}")

    # 2. Verificar que tiene el skill que necesitamos
    skill_ids = [s["id"] for s in card["skills"]]
    if "resumir-texto" not in skill_ids:
        print("El agente no tiene la capacidad que necesitamos")
        return

    # 3. Crear una tarea
    texto_largo = """
    Los sistemas multi-agente representan un cambio de paradigma en la
    inteligencia artificial. En lugar de un único modelo monolítico que
    intenta resolver todos los problemas, múltiples agentes especializados
    colaboran, cada uno aportando su expertise en un dominio específico.
    Esta arquitectura refleja cómo funcionan los equipos humanos: un
    cirujano no necesita saber de anestesiología, pero necesita comunicarse
    efectivamente con el anestesiólogo.
    """

    result = jsonrpc_call(agent_url, "task/create", {
        "skill_id": "resumir-texto",
        "input": {
            "texto": texto_largo,
            "max_palabras": 50
        }
    })

    print(f"\nTarea creada: {result['task_id']}")
    print(f"Estado: {result['status']}")

    # 4. Consultar el resultado
    status = jsonrpc_call(agent_url, "task/status", {
        "task_id": result["task_id"]
    })
    print(f"\nResultado:")
    print(json.dumps(status, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
```

Este ejemplo ilustra los conceptos fundamentales: descubrimiento de capacidades, contratos de entrada/salida con schemas, gestión de tareas con ciclo de vida, y comunicación sobre un protocolo estándar (JSON-RPC 2.0). Un protocolo de producción añadiría autenticación (OAuth 2.1), streaming con SSE, manejo de tareas asíncronas de larga duración, reintentos con backoff exponencial, circuit breakers, y un servidor async (FastAPI o similar) capaz de manejar concurrencia real. La estructura básica es la misma, pero la distancia entre este ejemplo pedagógico y un sistema de producción es significativa.

## Conclusión: el protocolo como infraestructura invisible

La historia de los protocolos nos enseña que la verdadera infraestructura es invisible. Nadie piensa en HTTP cuando abre una página web. Nadie piensa en TCP cuando hace una videollamada. Los protocolos exitosos se convierten en el aire que respira la tecnología: omnipresentes e imperceptibles.

El ecosistema de agentes de IA está en un momento que recuerda a la web de mediados de los 90. Tenemos las piezas tecnológicas (LLMs potentes, frameworks de agentes maduros, la necesidad de interoperabilidad), pero nos falta el pegamento estandarizado que permita construir sobre ellas sin reinventar la rueda cada vez.

Las señales son prometedoras. La convergencia alrededor de JSON-RPC 2.0 como formato base, la creación de la AAIF como organismo neutral, y la complementariedad natural entre MCP (agente-a-herramienta) y A2A (agente-a-agente) sugieren que el ecosistema se está moviendo hacia una estandarización pragmática, no por decreto de arriba hacia abajo sino por evolución orgánica. Como discutimos en [De agentes teóricos a agentes en producción](/2026/02/15/de-agentes-teoricos-a-agentes-en-produccion.html), la transición de demos a producción exige exactamente este tipo de infraestructura invisible.

Los desafíos pendientes son significativos: el descubrimiento semántico de agentes, la delegación segura de autoridad en cadenas de agentes, la tolerancia a fallos no deterministas y el consenso en sistemas donde los participantes pueden alucinar. Pero estos son problemas solubles, y la historia de los sistemas distribuidos nos da décadas de investigación sobre las que construir.

El protocolo que falta no será perfecto. Ningún protocolo lo es en su primera versión. Pero como dijo Jon Postel en su famosa ley de robustez: **"Sé conservador en lo que envías, sé liberal en lo que aceptas."** Quizá esa sea la mejor guía para el futuro de la comunicación entre agentes: protocolos estrictos en la estructura, tolerantes en la interpretación.

## Referencias y fuentes clave

1. Lamport, L., Shostak, R., & Pease, M. (1982). "The Byzantine Generals Problem." *ACM Transactions on Programming Languages and Systems*, 4(3), 382-401.

2. Sun, Y., et al. (2024). "IBGP: Imperfect Byzantine Generals Problem for Zero-Shot Robustness in Communicative Multi-Agent Systems." *arXiv:2410.16237*.

3. Zhang, J., et al. (2024). "BlockAgents: Towards Byzantine-Robust LLM-Based Multi-Agent Coordination via Blockchain." *Proceedings of the ACM Turing Award Celebration Conference*.

4. Li, X., et al. (2025). "Rethinking the Reliability of Multi-agent Systems: A Perspective from Byzantine Fault Tolerance." *arXiv:2511.10400*.

5. Anthropic. (2024). "Introducing the Model Context Protocol." Documentación oficial en modelcontextprotocol.io.

6. Google. (2025). "Announcing the Agent2Agent Protocol (A2A)." Google Developers Blog.

7. A2A Protocol Specification v0.3. (2025). a2a-protocol.org/v0.3.0/specification/.

8. Model Context Protocol Specification. (2025). modelcontextprotocol.io/specification/2025-11-25.

9. OpenAI. (2025). "OpenAI Agents SDK - Handoffs." Documentación oficial en openai.github.io/openai-agents-python.

10. Linux Foundation. (2025). "Announces the Formation of the Agentic AI Foundation (AAIF)."

11. Agent Network Protocol Technical White Paper. (2025). *arXiv:2508.00007*.

12. Fielding, R. T. (2000). "Architectural Styles and the Design of Network-Based Software Architectures." Doctoral dissertation, University of California, Irvine.

13. JSON-RPC 2.0 Specification. jsonrpc.org/specification.

14. Postel, J. (1981). "Transmission Control Protocol." RFC 793, IETF.

15. Berners-Lee, T., Fielding, R., & Frystyk, H. (1996). "Hypertext Transfer Protocol -- HTTP/1.0." RFC 1945, IETF.
