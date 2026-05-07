---
title: "La ventana de contexto como recurso escaso: estrategias de manejo para agentes"
date: 2026-03-24
author: "Héctor Patricio"
tags: ['llm', 'agentes', 'contexto', 'arquitectura', 'inteligencia-artificial', 'rag', 'memoria', 'diseño-de-software']
description: "La ventana de contexto de un LLM es un recurso finito, caro y crítico. Exploramos estrategias para gestionarla eficientemente en agentes de IA."
featuredImage: ""
draft: true
---

Si alguna vez programaste un sistema embebido con 2 KB de RAM, sabes lo que se siente trabajar con recursos verdaderamente escasos. Cada byte importa. Cada decisión de qué guardar y qué descartar tiene consecuencias directas en la funcionalidad del sistema. Ahora piensa en un agente de IA basado en un LLM: su "memoria de trabajo" es la ventana de contexto, y aunque medida en miles o millones de tokens en vez de bytes, es igualmente finita, igualmente cara, e igualmente crítica para el rendimiento.

En este artículo vamos a tratar la ventana de contexto como lo que es: un recurso computacional que debe gestionarse con la misma disciplina con la que un sistema operativo gestiona la RAM. Hablaremos de qué va dentro de ese espacio, por qué se degrada la calidad cuando lo llenamos sin criterio, y qué estrategias concretas podemos aplicar para construir agentes que usen su contexto de forma inteligente.

## La ventana de contexto es la RAM de tu agente

En un sistema operativo, la RAM es el espacio donde vive todo lo que el procesador necesita para trabajar: el código en ejecución, las variables, las estructuras de datos temporales. Si la RAM se llena, el sistema empieza a paginar a disco, y el rendimiento se degrada dramáticamente. Eventualmente, si no hay forma de liberar memoria, el proceso muere con un **Out of Memory**.

La ventana de contexto de un LLM cumple una función análoga. Es el espacio donde el modelo "ve" todo lo que necesita para generar su siguiente respuesta. A diferencia de la RAM, la ventana de contexto no pagina automáticamente: cuando se llena, simplemente se trunca el inicio, se pierde información, o se rechaza la petición. No hay segunda oportunidad.

Pero hay una diferencia aún más sutil y peligrosa: **llenar la ventana de contexto no produce un error visible**. El modelo sigue generando respuestas. Lo que cambia es la calidad. Es como un memory leak silencioso que no crashea tu programa pero lo hace cada vez más lento e impredecible. Y en el caso de los agentes, donde cada paso añade más contenido al contexto, este problema se amplifica con cada iteración.

Como vimos en el artículo sobre [patrones de diseño para sistemas con IA](/posts/patrones-de-diseno-para-sistemas-con-ia/), los sistemas basados en LLMs introducen formas nuevas de complejidad. La gestión del contexto es una de las más importantes y menos discutidas.

## Anatomía de la ventana de contexto

Para gestionar un recurso, primero hay que entender qué lo consume. Veamos qué va dentro de la ventana de contexto de un agente típico:

### 1. El system prompt

Es la "constitución" del agente: sus instrucciones base, personalidad, restricciones. En agentes complejos, esto puede ocupar fácilmente entre 1,000 y 10,000 tokens. Es un costo fijo que pagas en cada invocación.

### 2. Las definiciones de herramientas

Cada herramienta que el agente puede usar necesita una descripción en el contexto: nombre, descripción, parámetros con sus tipos, ejemplos. A esto le llamaremos el **tool tax**: el impuesto que pagas por cada herramienta registrada, la use o no. El tool tax varía entre 100 y 500 tokens por herramienta según el proveedor, la complejidad de los parámetros y la longitud de las descripciones (los formatos de definición de herramientas se han optimizado significativamente en 2025-2026). Si tienes 30 herramientas disponibles, podrías estar gastando entre 3,000 y 15,000 tokens solo en decirle al modelo qué puede hacer. Mide tu tool tax real con el tokenizer de tu modelo para tener un presupuesto preciso.

### 3. El historial de conversación

Cada mensaje del usuario y cada respuesta del agente se acumulan. En un agente multi-paso que ejecuta 10 acciones, el historial puede crecer rápidamente a decenas de miles de tokens.

### 4. Los resultados de herramientas

Cuando un agente hace una búsqueda en la web, lee un archivo o consulta una base de datos, el resultado se inyecta en el contexto. Un solo resultado de búsqueda puede aportar 2,000 tokens. Cinco búsquedas y ya consumiste 10,000 tokens solo en resultados.

### 5. El espacio para la respuesta

El modelo necesita tokens disponibles para generar su respuesta. Si todo el presupuesto está consumido por el input, no queda espacio para pensar.

Pensemos en esto como un **presupuesto de contexto** (context budget):

```python
# Modelo simplificado de presupuesto de contexto
class ContextBudget:
    def __init__(self, max_tokens: int):
        self.max_tokens = max_tokens
        self.system_prompt_tokens = 0
        self.tool_definitions_tokens = 0
        self.history_tokens = 0
        self.tool_results_tokens = 0
        self.reserved_for_output = 4096  # Reservar espacio para la respuesta

    @property
    def available(self) -> int:
        used = (
            self.system_prompt_tokens
            + self.tool_definitions_tokens
            + self.history_tokens
            + self.tool_results_tokens
            + self.reserved_for_output
        )
        return max(0, self.max_tokens - used)

    @property
    def utilization(self) -> float:
        return 1.0 - (self.available / self.max_tokens)
```

En marzo de 2026, las ventanas de contexto varían considerablemente: Gemini ofrece hasta 2M tokens, Claude hasta 200K, y GPT-4o hasta 128K. Podrías pensar que con estos tamaños tienes espacio de sobra. Pero hagamos cuentas para un agente de investigación típico con una ventana de 200K tokens:

| Componente | Tokens estimados |
|---|---|
| System prompt | 3,000 |
| 20 herramientas | 8,000 |
| 15 pasos de conversación | 30,000 |
| 10 resultados de herramientas | 25,000 |
| Reserva para respuesta | 4,096 |
| **Total** | **70,096** |

Más de la mitad del contexto consumido, y eso sin contar que muchos de esos tokens son ruido que no aporta a la tarea actual. La eficiencia del contexto no solo se mide en cuánto cabe, sino en cuánto de lo que cabe es realmente útil.

## El problema de la degradación: "Lost in the middle"

Aquí es donde la analogía con la RAM se rompe parcialmente y la realidad del LLM es **peor**. En la RAM, un byte en la posición 0x0000 se lee con la misma fiabilidad que uno en 0xFFFF. En un LLM, la posición importa.

En 2023, un grupo de investigadores de Stanford publicó un paper seminal: "Lost in the Middle: How Language Models Use Long Contexts". Su hallazgo fue revelador y algo perturbador: **los LLMs tienen una curva de atención en forma de U**. Recuerdan bien lo que está al principio del contexto (efecto de primacía) y lo que está al final (efecto de recencia), pero tienden a "olvidar" la información que está en el centro.

Este fenómeno se validó con las pruebas de "needle in a haystack" (aguja en un pajar), donde se coloca un dato específico en diferentes posiciones de un contexto largo y se mide si el modelo lo puede recuperar. Los resultados muestran consistentemente que la capacidad de recuperación decae en las posiciones centrales.

### ¿Cómo afecta esto a los agentes?

En un agente multi-paso, el problema se manifiesta de forma particularmente insidiosa. Imagina un agente que ejecuta 20 pasos para completar una tarea de investigación:

- **Paso 1-3**: El agente recibe las instrucciones y hace búsquedas iniciales. Esta información está al inicio del contexto.
- **Paso 8-12**: El agente encuentra datos críticos que son centrales para la tarea. Esta información queda en el **medio** del contexto.
- **Paso 18-20**: El agente necesita sintetizar todo. Pero los datos críticos del medio son precisamente los que el modelo recuerda peor.

Es como si un investigador tomara notas detalladas al principio y al final de su jornada, pero las notas del mediodía estuvieran borrosas. Y peor aún, el investigador no sabe que están borrosas: cree que las puede leer perfectamente.

En el artículo sobre [cómo razonan los LLMs](/posts/como-razonan-los-llms-de-turing-a-inference-time-scaling/), discutimos las capacidades y limitaciones de los transformadores. El fenómeno de "lost in the middle" es una consecuencia directa de cómo funciona el mecanismo de atención: con ventanas de contexto muy largas, los pesos de atención se diluyen y los tokens centrales reciben menos "atención" que los de los extremos.

```python
# Simulación conceptual del efecto "lost in the middle"
# NOTA: Esto NO modela el mecanismo de atención real de un transformer.
# En un transformer, la atención usa softmax sobre productos punto entre
# queries y keys, y el efecto U-shape emerge de la interacción entre
# posiciones relativas aprendidas y la distribución de la información.
# Esta fórmula solo ilustra la forma general de la curva observada
# empíricamente en los experimentos de Liu et al.
import numpy as np

def attention_weight_approximation(position: int, context_length: int) -> float:
    """
    Aproximación empírica de la curva de recuperación observada
    en los experimentos "Lost in the Middle", NO del mecanismo de atención.
    Las posiciones al inicio y al final muestran mejor recuperación.
    """
    # Normalizar posición a [0, 1]
    normalized = position / context_length

    # Curva en U: alta recuperación al inicio y al final
    primacy = np.exp(-5 * normalized)          # Decae desde el inicio
    recency = np.exp(-5 * (1 - normalized))    # Crece hacia el final
    baseline = 0.1                             # Recuperación base mínima

    return primacy + recency + baseline

# Las posiciones centrales muestran ~50% menor recuperación
# que las posiciones en los extremos
```

Esto no es solo un problema académico. Tiene consecuencias prácticas directas: un agente que "olvida" las instrucciones del paso 7 cuando va en el paso 20 puede contradecirse, repetir trabajo, o simplemente ignorar información crucial que ya recopiló.

## Estrategias de compresión de contexto

Ahora que entendemos el problema, hablemos de soluciones concretas para gestionar el contexto.

### Resumen progresivo (*summarization*): comprimir el historial

La estrategia más directa: cuando el historial crece más allá de un umbral, pedirle al propio LLM (o a uno más pequeño y barato) que resuma los pasos anteriores. El resumen reemplaza el historial detallado.

```python
from dataclasses import dataclass, field

@dataclass
class ConversationManager:
    messages: list = field(default_factory=list)
    summary: str = ""
    max_detail_tokens: int = 20_000
    summarize_fn: callable = None  # Función que llama al LLM para resumir

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self._maybe_compress()

    def _maybe_compress(self):
        total_tokens = self._estimate_tokens()
        if total_tokens > self.max_detail_tokens:
            # Separar mensajes recientes (mantener detalle)
            # de mensajes antiguos (comprimir)
            midpoint = len(self.messages) // 2
            old_messages = self.messages[:midpoint]
            recent_messages = self.messages[midpoint:]

            # Resumir los mensajes antiguos
            new_summary = self.summarize_fn(
                previous_summary=self.summary,
                messages=old_messages
            )
            self.summary = new_summary
            self.messages = recent_messages

    def get_context(self) -> list:
        """Retorna el contexto optimizado para el LLM."""
        context = []
        if self.summary:
            context.append({
                "role": "system",
                "content": f"Resumen de la conversación previa:\n{self.summary}"
            })
        context.extend(self.messages)
        return context

    def _estimate_tokens(self) -> int:
        # Estimación burda: 1 token ~ 4 caracteres en español.
        # En la práctica, los tokenizers BPE tienen ratios variables
        # (entre 3 y 5 chars/token según el vocabulario y el idioma).
        # Para presupuestos precisos, usa tiktoken o el tokenizer del modelo.
        return sum(len(m["content"]) // 4 for m in self.messages)
```

La ventaja de esta estrategia es que preserva la información semántica importante mientras reduce drásticamente el uso de tokens. La desventaja es que toda compresión implica pérdida. Los detalles específicos (números exactos, nombres, fechas) pueden perderse en el resumen.

### Ventana deslizante (*sliding window*)

Inspirada directamente en los protocolos de red y en las técnicas de procesamiento de señales, la sliding window es brutal pero efectiva: mantén solo los últimos N mensajes y descarta el resto.

Es lo que hacemos naturalmente en una conversación humana: recordamos las últimas frases que nos dijeron, pero no podemos repetir textualmente lo que alguien nos dijo hace 30 minutos.

```python
def sliding_window(messages: list, window_size: int = 10) -> list:
    """Mantener solo los últimos N mensajes."""
    if len(messages) <= window_size:
        return messages
    return messages[-window_size:]
```

Es simple, predecible y fácil de razonar. Pero es también la que más información pierde. Se usa mejor en combinación con otras estrategias.

### Memoria jerárquica: resúmenes de resúmenes

Esta es la estrategia más sofisticada y se inspira directamente en cómo los sistemas de archivos manejan los datos: con niveles de abstracción. Imagina tres niveles:

1. **Nivel 0 (detalle completo)**: Los últimos 5 mensajes tal cual.
2. **Nivel 1 (resúmenes recientes)**: Resúmenes de los bloques de mensajes anteriores (cada 5-10 mensajes se resumen en un párrafo).
3. **Nivel 2 (resumen ejecutivo)**: Un resumen de los resúmenes, que captura solo los hechos y decisiones clave de toda la conversación.

```python
@dataclass
class HierarchicalMemory:
    """Memoria jerárquica inspirada en niveles de caché."""
    l0_messages: list = field(default_factory=list)  # Detalle completo
    l1_summaries: list = field(default_factory=list)  # Resúmenes de bloques
    l2_summary: str = ""                              # Resumen ejecutivo

    l0_max: int = 5      # Últimos 5 mensajes en detalle
    l1_max: int = 10     # Hasta 10 resúmenes de bloques
    summarize_fn: callable = None

    def add_message(self, message: dict):
        self.l0_messages.append(message)

        # Cuando L0 se llena, comprimir a L1
        if len(self.l0_messages) > self.l0_max:
            overflow = self.l0_messages[:-self.l0_max]
            self.l0_messages = self.l0_messages[-self.l0_max:]

            block_summary = self.summarize_fn(overflow)
            self.l1_summaries.append(block_summary)

            # Cuando L1 se llena, comprimir a L2
            if len(self.l1_summaries) > self.l1_max:
                old_summaries = self.l1_summaries[:-self.l1_max]
                self.l1_summaries = self.l1_summaries[-self.l1_max:]

                self.l2_summary = self.summarize_fn(
                    [self.l2_summary] + old_summaries
                )

    def build_context(self) -> str:
        parts = []
        if self.l2_summary:
            parts.append(f"[Contexto general]: {self.l2_summary}")
        for i, s in enumerate(self.l1_summaries):
            parts.append(f"[Bloque {i+1}]: {s}")
        for m in self.l0_messages:
            parts.append(f"[{m['role']}]: {m['content']}")
        return "\n\n".join(parts)
```

La información más reciente tiene máximo detalle, y conforme envejece, se comprime progresivamente. Los datos "calientes" (recientes, relevantes) merecen más espacio que los datos "fríos" (antiguos, de referencia).

### Map-reduce sobre contexto largo

Cuando la información que debemos procesar excede la ventana de contexto, podemos aplicar el mismo patrón de map-reduce que usamos en sistemas distribuidos, como discutimos en el artículo sobre [la diferencia entre concurrencia y paralelismo](/posts/la-diferencia-entre-concurrencia-y-paralelismo/): dividir el problema, procesar en paralelo y combinar los resultados.

```python
async def map_reduce_context(
    documents: list[str],
    question: str,
    llm_call: callable,
    chunk_size: int = 4000
) -> str:
    # MAP: Procesar cada documento de forma independiente
    partial_answers = []
    for doc in documents:
        chunks = split_into_chunks(doc, chunk_size)
        for chunk in chunks:
            answer = await llm_call(
                f"Basándote en este fragmento, responde: {question}\n\n"
                f"Fragmento: {chunk}"
            )
            partial_answers.append(answer)

    # REDUCE: Combinar respuestas parciales
    combined = "\n".join(partial_answers)
    final_answer = await llm_call(
        f"Sintetiza estas respuestas parciales en una "
        f"respuesta coherente a: {question}\n\n"
        f"Respuestas parciales:\n{combined}"
    )
    return final_answer
```

Este patrón tiene un costo: múltiples llamadas al LLM incrementan la latencia y el gasto. Pero permite procesar cantidades de información que simplemente no cabrían en una sola ventana de contexto.

## RAG como extensión del contexto

RAG (Retrieval-Augmented Generation) extiende la capacidad del agente más allá del contexto: en lugar de meter toda la información en la ventana desde el inicio, guardamos la información en un índice externo y solo recuperamos los fragmentos relevantes cuando los necesitamos.

### Cuándo buscar vs cuándo recordar

Esta es una de las decisiones de diseño más importantes para un agente: ¿qué vive permanentemente en el contexto y qué se busca bajo demanda?

```python
class ContextStrategy:
    """Decidir si una información debe estar en contexto o en RAG."""

    # Información que DEBE estar en el contexto directo:
    ALWAYS_IN_CONTEXT = [
        "instrucciones del sistema",       # El agente las necesita siempre
        "estado actual de la tarea",       # Crítico para el paso actual
        "últimas acciones y resultados",   # Necesario para continuidad
        "restricciones de seguridad",      # No negociable
    ]

    # Información que DEBE ir a RAG (búsqueda bajo demanda):
    ALWAYS_IN_RAG = [
        "documentación de referencia",     # Solo se busca cuando se necesita
        "historial de conversaciones pasadas",  # Memoria a largo plazo
        "base de conocimiento del dominio",     # Enorme, parcialmente relevante
        "logs y registros",                     # Voluminosos
    ]

    # Zona gris: depende del uso
    DEPENDS = [
        "resultados de herramientas previas",  # ¿Se necesitarán otra vez?
        "definiciones de herramientas",         # ¿Se usarán todas?
        "ejemplos few-shot",                    # ¿Mejoran la calidad?
    ]
```

El artículo sobre [RAG en 2026](/posts/rag-en-2026-la-paradoja-de-la-simplicidad/) profundiza en las técnicas específicas de implementación. Lo relevante aquí es la decisión arquitectónica: RAG no es una alternativa a la gestión del contexto, es un complemento. Un agente bien diseñado usa ambas cosas: gestiona activamente lo que está en contexto y busca en RAG lo que necesita bajo demanda.

### El trade-off entre contexto inyectado y contexto generado

Hay un trade-off sutil que pocos discuten: cada fragmento que inyectas vía RAG ocupa espacio que el modelo podría usar para "pensar". Un modelo con 100K tokens de contexto que tiene 95K ocupados por documentos inyectados tiene solo 5K tokens para razonar.

Esto conecta directamente con lo que discutimos en [Cómo razonan los LLMs](/posts/como-razonan-los-llms-de-turing-a-inference-time-scaling/): las técnicas como chain-of-thought requieren espacio en la ventana de contexto para que el modelo desarrolle su razonamiento. Si llenamos el contexto con datos, estamos literalmente quitándole espacio para pensar.

Mi regla práctica de partida es: **no uses más del 60-70% de la ventana para datos inyectados**. El resto debe quedar disponible para el razonamiento del modelo y la generación de la respuesta. Este porcentaje no viene de un estudio formal, sino de la experiencia práctica construyendo agentes: es el rango donde he observado que el modelo mantiene calidad de razonamiento sin desperdiciar capacidad.

Dicho esto, este porcentaje depende fuertemente del modelo. Algunos modelos (como Claude) mantienen buena calidad de recuperación hasta el 85-90% de su ventana, mientras que otros se degradan significativamente después del 50%. Un modelo con 2M tokens que usa 1.2M (60%) puede comportarse de forma muy diferente que uno con 128K que usa 77K (60%). **La recomendación real es: mide la calidad de las respuestas de tu modelo a diferentes niveles de utilización con pruebas de tipo "needle-in-a-haystack" y establece tu límite basándote en datos, no en reglas generales.** El 60-70% es un punto de partida conservador, no una ley universal.

## Memoria externa y bases de datos vectoriales

No basta con tener los datos en un índice externo: necesitas poder encontrar los correctos rápidamente. Aquí es donde entran las bases de datos vectoriales.

### Short-term vs long-term memory

Un agente sofisticado necesita dos tipos de memoria:

**Memoria a corto plazo (working memory)**:
- Es la ventana de contexto actual.
- Contiene el estado inmediato de la tarea.
- Se pierde cuando termina la sesión.
- Es rápida pero limitada.

**Memoria a largo plazo (persistent memory)**:
- Está en una base de datos externa (vectorial o relacional).
- Persiste entre sesiones.
- Contiene aprendizajes, preferencias del usuario, hechos del dominio.
- Es prácticamente ilimitada pero requiere un mecanismo de recuperación.

```python
from dataclasses import dataclass

@dataclass
class AgentMemorySystem:
    """Sistema de memoria dual para agentes."""

    # Memoria a corto plazo: lo que el agente "tiene en mente"
    short_term: list  # Mensajes y resultados recientes

    # Memoria a largo plazo: lo que el agente "sabe"
    long_term_store: object  # Base de datos vectorial

    async def recall(self, query: str, top_k: int = 5) -> list[str]:
        """
        Buscar en memoria a largo plazo.
        Equivalente a un page fault: el dato no está en RAM,
        hay que buscarlo en disco.
        """
        results = await self.long_term_store.search(
            query=query,
            limit=top_k
        )
        return [r.content for r in results]

    async def memorize(self, content: str, metadata: dict = None):
        """
        Guardar en memoria a largo plazo.
        Equivalente a escribir a disco: lento pero persistente.
        """
        embedding = await self.long_term_store.embed(content)
        await self.long_term_store.insert(
            content=content,
            embedding=embedding,
            metadata=metadata or {}
        )

    async def get_working_context(self, query: str = None) -> list:
        """
        Construir el contexto de trabajo combinando
        memoria a corto y largo plazo.
        """
        context = list(self.short_term)

        # Si hay una consulta activa, enriquecer con memoria a largo plazo
        if query:
            relevant = await self.recall(query)
            context.insert(0, {
                "role": "system",
                "content": f"Información relevante de tu memoria:\n"
                           + "\n".join(relevant)
            })

        return context
```

### Embeddings como índice

Los embeddings vectoriales son el mecanismo de indexación que permite buscar en la memoria a largo plazo. Funcionan como un índice invertido pero en espacio semántico: en lugar de buscar por palabras clave exactas, buscamos por significado.

Un embedding toma un fragmento de texto y lo convierte en un vector numérico de alta dimensionalidad (768, 1536 o 3072 dimensiones típicamente). Textos con significado similar producen vectores cercanos en este espacio. Cuando el agente necesita recordar algo, convierte su consulta en un vector y busca los vectores más cercanos en la base de datos.

### El patrón "Memory Bank"

El patrón Memory Bank va más allá de simplemente guardar y buscar. Organiza la memoria en categorías funcionales, cada una con su propia estrategia de retención y recuperación:

```python
class MemoryBank:
    """
    Banco de memoria organizado por tipo de información.
    Cada banco tiene su propia política de retención.
    """

    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.banks = {
            "facts": {
                "description": "Hechos verificados sobre el dominio",
                "retention": "permanent",
                "collection": "agent_facts"
            },
            "procedures": {
                "description": "Procedimientos aprendidos",
                "retention": "permanent",
                "collection": "agent_procedures"
            },
            "interactions": {
                "description": "Resúmenes de interacciones pasadas",
                "retention": "90_days",
                "collection": "agent_interactions"
            },
            "scratch": {
                "description": "Notas temporales durante una tarea",
                "retention": "session",
                "collection": "agent_scratch"
            }
        }

    async def store(self, content: str, bank: str, metadata: dict = None):
        config = self.banks[bank]
        await self.vector_store.upsert(
            collection=config["collection"],
            content=content,
            metadata={
                **(metadata or {}),
                "bank": bank,
                "retention": config["retention"]
            }
        )

    async def query(self, question: str, banks: list[str] = None, top_k: int = 5):
        """Buscar en bancos específicos o en todos."""
        target_banks = banks or list(self.banks.keys())
        results = []
        for bank in target_banks:
            config = self.banks[bank]
            bank_results = await self.vector_store.search(
                collection=config["collection"],
                query=question,
                limit=top_k
            )
            results.extend(bank_results)

        # Re-rankear por relevancia global
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]
```

Este patrón es especialmente útil para agentes que deben operar durante períodos largos o a través de múltiples sesiones. Permite que el agente "aprenda" de sus interacciones pasadas sin necesidad de mantener todo en la ventana de contexto.

## Context-aware tool selection: reducir el tool tax

Recuerda nuestro cálculo del presupuesto de contexto: 20 herramientas podían consumir 8,000 tokens. Pero, ¿realmente necesita el agente ver las 20 herramientas en cada paso?

Si un agente está en el paso de "escribir un informe", no necesita ver la definición de la herramienta de "eliminar archivos" o "enviar correos". Inyectar todas las herramientas disponibles en cada paso es como cargar todas las bibliotecas de un lenguaje de programación en memoria cuando tu programa solo usa tres.

### Selección dinámica de herramientas

La idea es simple pero poderosa: en lugar de definir todas las herramientas en el system prompt, seleccionamos dinámicamente cuáles inyectar basándonos en la tarea actual.

```python
class DynamicToolSelector:
    """
    Selecciona las herramientas relevantes para el paso actual
    en lugar de inyectar todas.
    """

    def __init__(self, all_tools: list[dict], vector_store):
        self.all_tools = {t["name"]: t for t in all_tools}
        self.vector_store = vector_store

        # Indexar las descripciones de herramientas
        for tool in all_tools:
            self.vector_store.index(
                id=tool["name"],
                content=f"{tool['name']}: {tool['description']}",
                metadata={"category": tool.get("category", "general")}
            )

    def select_tools(
        self,
        task_description: str,
        max_tools: int = 5,
        always_include: list[str] = None
    ) -> list[dict]:
        """
        Seleccionar las herramientas más relevantes para la tarea actual.
        """
        # Herramientas que siempre deben estar disponibles
        selected = []
        if always_include:
            for name in always_include:
                if name in self.all_tools:
                    selected.append(self.all_tools[name])

        # Buscar herramientas relevantes por similitud semántica
        remaining_slots = max_tools - len(selected)
        if remaining_slots > 0:
            results = self.vector_store.search(
                query=task_description,
                limit=remaining_slots
            )
            for result in results:
                tool_name = result.id
                if tool_name not in [t["name"] for t in selected]:
                    selected.append(self.all_tools[tool_name])

        return selected
```

### Agrupación por fases

Otra estrategia, más determinista, es agrupar herramientas por fase de la tarea:

```python
TOOL_PHASES = {
    "research": ["web_search", "read_file", "query_database"],
    "analysis": ["calculate", "compare", "summarize"],
    "writing": ["create_document", "format_text", "spell_check"],
    "communication": ["send_email", "post_message", "schedule_meeting"],
}

def get_tools_for_phase(phase: str, all_tools: dict) -> list:
    """Retornar solo las herramientas de la fase actual."""
    tool_names = TOOL_PHASES.get(phase, [])
    return [all_tools[name] for name in tool_names if name in all_tools]
```

Esta segunda estrategia es menos flexible pero más predecible. Si conectamos esto con las ideas de [A Philosophy of Software Design](/posts/a-philosophy-of-software-design-los-modulos-deben-ser-profundos/), estamos aplicando el principio de crear interfaces estrechas: en cada momento, el agente solo ve las herramientas que necesita, reduciendo la complejidad cognitiva del modelo (y el consumo de tokens).

La reducción puede ser dramática. En un agente con 30 herramientas, si en promedio cada paso solo necesita 5, pasamos de 12,000 tokens de tool tax a 2,000. Eso son 10,000 tokens liberados para información útil en cada iteración.

## Ejemplo práctico: un sistema completo de gestión de contexto

Vamos a integrar todo lo anterior en un sistema cohesivo. Este es un agente de investigación que debe buscar información, analizarla y producir un informe, gestionando su contexto de forma inteligente durante todo el proceso.

```python
from dataclasses import dataclass, field
from enum import Enum

class AgentPhase(Enum):
    PLANNING = "planning"
    RESEARCH = "research"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"

@dataclass
class ContextManagedAgent:
    """
    Agente con gestión explícita de contexto.
    Trata la ventana de contexto como un recurso escaso.
    """
    max_context_tokens: int = 200_000  # Ajustar según el modelo usado
    reserved_for_output: int = 4_096
    max_tool_budget: int = 3_000     # Máximo para definiciones de herramientas
    max_history_budget: int = 40_000  # Máximo para historial

    # Componentes
    memory: HierarchicalMemory = field(default_factory=HierarchicalMemory)
    tool_selector: DynamicToolSelector = None
    memory_bank: MemoryBank = None
    current_phase: AgentPhase = AgentPhase.PLANNING

    # Métricas de uso
    _token_usage_log: list = field(default_factory=list)

    async def build_prompt(self, user_message: str) -> dict:
        """
        Construir el prompt optimizando el uso de contexto.
        Cada componente tiene un presupuesto asignado.
        """
        budget = ContextBudget(self.max_context_tokens)

        # 1. System prompt (costo fijo, pero podemos adaptarlo por fase)
        system_prompt = self._get_phase_system_prompt()
        budget.system_prompt_tokens = estimate_tokens(system_prompt)

        # 2. Herramientas (selección dinámica basada en la fase)
        tools = self.tool_selector.select_tools(
            task_description=user_message,
            max_tools=5
        )
        budget.tool_definitions_tokens = estimate_tokens(str(tools))

        # 3. Contexto de memoria (jerárquico)
        history_context = self.memory.build_context()
        budget.history_tokens = estimate_tokens(history_context)

        # 4. Si hay presupuesto, enriquecer con memoria a largo plazo
        rag_context = ""
        if budget.available > 5_000:
            relevant_memories = await self.memory_bank.query(
                question=user_message,
                top_k=3
            )
            rag_context = "\n".join(
                [f"- {m.content}" for m in relevant_memories]
            )
            budget.tool_results_tokens = estimate_tokens(rag_context)

        # 5. Verificar que no excedemos el presupuesto
        if budget.available < self.reserved_for_output:
            # Emergencia: comprimir más agresivamente
            self.memory.force_compress()
            history_context = self.memory.build_context()

        # Registrar uso para análisis
        self._token_usage_log.append({
            "phase": self.current_phase.value,
            "utilization": budget.utilization,
            "available": budget.available
        })

        messages = [
            {"role": "system", "content": history_context},
        ]
        if rag_context:
            messages.append(
                {"role": "system", "content": f"Datos relevantes:\n{rag_context}"}
            )
        messages.append({"role": "user", "content": user_message})

        return {
            "system": system_prompt,
            "tools": tools,
            "messages": messages
        }

    def _get_phase_system_prompt(self) -> str:
        """System prompt adaptado a la fase actual. Más corto = más eficiente."""
        base = "Eres un agente de investigación."
        phase_instructions = {
            AgentPhase.PLANNING: (
                "Estás en la fase de planificación. "
                "Descompón la tarea en pasos concretos."
            ),
            AgentPhase.RESEARCH: (
                "Estás investigando. Busca información relevante "
                "y extrae los datos clave de forma concisa."
            ),
            AgentPhase.ANALYSIS: (
                "Estás analizando la información recopilada. "
                "Identifica patrones y conclusiones."
            ),
            AgentPhase.SYNTHESIS: (
                "Estás escribiendo el informe final. "
                "Sintetiza todo en un documento coherente."
            ),
        }
        return f"{base} {phase_instructions[self.current_phase]}"

    async def transition_phase(self, new_phase: AgentPhase):
        """Al cambiar de fase, comprimir el contexto de la fase anterior."""
        # Guardar un resumen de la fase que termina en memoria a largo plazo
        phase_summary = self._summarize_current_phase()
        await self.memory_bank.store(
            content=phase_summary,
            bank="procedures",
            metadata={"phase": self.current_phase.value}
        )
        # Comprimir memoria a corto plazo
        self.memory.force_compress()
        self.current_phase = new_phase
```

Observa cómo cada componente tiene un presupuesto asignado, cómo la selección de herramientas es dinámica por fase, y cómo la transición entre fases incluye una compresión explícita del contexto. No dejamos que el contexto crezca sin control: lo gestionamos activamente.

## Prompt caching: la optimización de producción que no puedes ignorar

Una de las optimizaciones más impactantes para agentes en producción es el **prompt caching** (o context caching), disponible en Anthropic, Google y OpenAI desde 2024-2025. La idea es simple pero poderosa: cuando el prefijo de tu prompt (system prompt + definiciones de herramientas) no cambia entre requests, el proveedor cachea los KV-cache internos de esos tokens, lo que reduce tanto la latencia como el costo de forma significativa (hasta un 90% de descuento en tokens cacheados con Anthropic).

Para un agente con herramientas, esto tiene implicaciones arquitectónicas directas: **estructura tu contexto para maximizar los cache hits**. Eso significa poner el contenido estable (system prompt, definiciones de herramientas, instrucciones fijas) al principio del prompt, y el contenido variable (historial, resultados de herramientas, mensaje del usuario) al final. El proveedor puede reutilizar el cache del prefijo estable entre llamadas.

```python
# Estructura optimizada para prompt caching:
# 1. System prompt (estable → se cachea)
# 2. Definiciones de herramientas (estable → se cachea)
# 3. Contexto de memoria (variable → NO se cachea)
# 4. Historial reciente (variable → NO se cachea)
# 5. Mensaje del usuario (variable → NO se cachea)
#
# Los puntos 1-2 forman el "prefijo estable" que el proveedor
# puede cachear entre requests, reduciendo costo y latencia.
```

En la práctica, un agente bien estructurado puede reducir el costo por request entre un 50% y un 80% gracias al prompt caching, especialmente en conversaciones largas donde el system prompt y las herramientas se repiten en cada llamada. Esta es probablemente la optimización de producción con mejor relación esfuerzo-impacto para agentes con herramientas.

## ¿Ventanas más grandes resolverán el problema?

Las ventanas de contexto siguen creciendo -- Gemini ya ofrece 2M de tokens, Claude 200K -- pero la experiencia de producción en 2025-2026 ha *confirmado* que más contexto no significa mejores resultados. Las ventanas más grandes no eliminan la necesidad de gestionarlas; de hecho, la hacen más urgente. El costo escala linealmente con el tamaño del contexto, el efecto "lost in the middle" puede amplificarse con ventanas más largas, y decidir qué información es relevante sigue siendo un problema de ingeniería de software, no solo de capacidad. Con 2M de tokens disponibles, los costos se disparan si no eres selectivo, y la gestión inteligente del contexto es más importante que nunca.

## Conclusión

La ventana de contexto es el recurso más importante y menos gestionado en los agentes de IA actuales. Tratarla como un recurso infinito es un error de diseño que produce agentes que se degradan silenciosamente conforme avanzan en tareas complejas.

Las estrategias que presentamos (compresión jerárquica, RAG como extensión, memoria dual, selección dinámica de herramientas) no son opcionales para agentes en producción. Son tan fundamentales como la gestión de memoria en un sistema operativo.

La próxima vez que diseñes un agente, pregúntate: ¿cuál es mi presupuesto de contexto? ¿Qué porcentaje está dedicado a información realmente útil para el paso actual? ¿Qué puedo mover a memoria externa? ¿Qué puedo comprimir sin perder lo esencial?

Un agente que gestiona su contexto activamente no solo es más eficiente en tokens y costo: produce mejores resultados porque el modelo trabaja con información relevante, no con ruido acumulado.

## Referencias y fuentes clave

- **"Lost in the Middle: How Language Models Use Long Contexts"** - Liu et al., 2023. Stanford University. El paper que cuantificó el problema de degradación por posición en ventanas de contexto largas.
- **"Needle in a Haystack" tests** - Greg Kamradt, 2023. Metodología ampliamente adoptada para medir la capacidad de recuperación de información en contextos largos.
- **"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"** - Lewis et al., 2020. Meta AI. El paper original de RAG que fundamentó el patrón de extensión de contexto con recuperación.
- **"MemGPT: Towards LLMs as Operating Systems"** - Packer et al., 2023. UC Berkeley. Propuesta de tratar la gestión de contexto como gestión de memoria virtual, con paginación explícita.
- **"Attention Is All You Need"** - Vaswani et al., 2017. Google Brain. El paper original del Transformer, fundamental para entender por qué la posición en el contexto importa.
- **"A Philosophy of Software Design"** - John Ousterhout, 2018. Los principios de diseño modular y ocultamiento de información aplicados aquí a la arquitectura de agentes.
- **Anthropic Claude Documentation** - Context window best practices, 2025. Guías prácticas sobre gestión de contexto en aplicaciones con Claude.
- **OpenAI Cookbook** - "How to maximize context window efficiency", 2025. Patrones prácticos para gestión de tokens.
