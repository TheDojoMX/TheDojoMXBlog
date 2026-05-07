# Capitulo 3: La Ventana de Contexto Es Tu Recurso Mas Escaso

> "200K tokens suenan a mucho hasta que los llenas en 3 iteraciones."

---

Si alguna vez programaste un sistema embebido con 2 KB de RAM, sabes lo que se siente trabajar con recursos verdaderamente escasos. Cada byte importa. Cada decision de que guardar y que descartar tiene consecuencias directas en la funcionalidad del sistema. Ahora piensa en un agente de IA: su "memoria de trabajo" es la ventana de contexto, y aunque medida en miles de tokens en vez de bytes, es igualmente finita, igualmente cara, e igualmente critica.

En el capitulo anterior construimos el loop agentico y vimos como el historial crece con cada paso: cada pensamiento, cada accion, cada observacion se acumula en el contexto. Ahora vamos a confrontar las consecuencias de ese crecimiento. Porque la ventana de contexto no es solo un limite tecnico: es un recurso computacional cuya mala gestion degrada silenciosamente la calidad de tu agente, infla tus costos y produce fallos que ningun log de errores va a capturar.

En este capitulo trataremos la ventana de contexto como lo que es: un recurso que debe gestionarse con la misma disciplina con la que un sistema operativo gestiona la RAM. Hablaremos de que va dentro de ese espacio, por que se degrada la calidad cuando lo llenamos sin criterio, y que estrategias concretas podemos aplicar --con codigo Python para cada una.

---

## 3.1 Por que los tokens son como la RAM

En un sistema operativo, la RAM es el espacio donde vive todo lo que el procesador necesita para trabajar: el codigo en ejecucion, las variables, las estructuras de datos temporales. Si la RAM se llena, el sistema empieza a paginar a disco, y el rendimiento se degrada dramaticamente. Eventualmente, si no hay forma de liberar memoria, el proceso muere con un **Out of Memory**.

La ventana de contexto de un LLM cumple una funcion analoga. Es el espacio donde el modelo "ve" todo lo que necesita para generar su siguiente respuesta. A diferencia de la RAM, la ventana de contexto no pagina automaticamente: cuando se llena, simplemente se trunca el inicio, se pierde informacion, o se rechaza la peticion. No hay segunda oportunidad.

Pero hay una diferencia aun mas sutil y peligrosa: **llenar la ventana de contexto no produce un error visible**. El modelo sigue generando respuestas. Lo que cambia es la calidad. Es como un memory leak silencioso que no crashea tu programa pero lo hace cada vez mas lento e impredecible. Y en el caso de los agentes, donde cada paso del loop anade mas contenido al contexto, este problema se amplifica con cada iteracion.

### Anatomia de la ventana de contexto

Para gestionar un recurso, primero hay que entender que lo consume. Veamos que va dentro de la ventana de contexto de un agente tipico:

**1. El system prompt.** La "constitucion" del agente: sus instrucciones base, personalidad, restricciones. En agentes complejos, esto puede ocupar facilmente entre 1,000 y 10,000 tokens. Es un costo fijo que pagas en cada invocacion.

**2. Las definiciones de herramientas.** Cada herramienta que el agente puede usar necesita una descripcion en el contexto: nombre, descripcion, parametros con sus tipos, ejemplos. A esto le llamaremos el **tool tax**: el impuesto que pagas por cada herramienta registrada, la use o no. El tool tax varia entre 100 y 500 tokens por herramienta segun el proveedor, la complejidad de los parametros y la longitud de las descripciones. Si tienes 30 herramientas disponibles, podrias estar gastando entre 3,000 y 15,000 tokens solo en decirle al modelo que puede hacer.

**3. El historial de conversacion.** Cada mensaje del usuario y cada respuesta del agente se acumulan. En un agente multi-paso que ejecuta 10 acciones, el historial puede crecer rapidamente a decenas de miles de tokens.

**4. Los resultados de herramientas.** Cuando un agente hace una busqueda en la web, lee un archivo o consulta una base de datos, el resultado se inyecta en el contexto. Un solo resultado de busqueda puede aportar 2,000 tokens. Cinco busquedas y ya consumiste 10,000 tokens solo en resultados.

**5. El espacio para la respuesta.** El modelo necesita tokens disponibles para generar su respuesta. Si todo el presupuesto esta consumido por el input, no queda espacio para pensar.

### El presupuesto de contexto

Pensemos en esto como un **presupuesto de contexto** (context budget):

```python
from dataclasses import dataclass


@dataclass
class ContextBudget:
    """Modelo de presupuesto de contexto para un agente.

    Funciona como un presupuesto financiero: cada componente tiene
    una asignacion, y la suma no puede exceder el total disponible.
    """
    max_tokens: int
    system_prompt_tokens: int = 0
    tool_definitions_tokens: int = 0
    history_tokens: int = 0
    tool_results_tokens: int = 0
    reserved_for_output: int = 4096

    @property
    def used(self) -> int:
        return (
            self.system_prompt_tokens
            + self.tool_definitions_tokens
            + self.history_tokens
            + self.tool_results_tokens
            + self.reserved_for_output
        )

    @property
    def available(self) -> int:
        return max(0, self.max_tokens - self.used)

    @property
    def utilization(self) -> float:
        return self.used / self.max_tokens

    def report(self) -> str:
        """Imprime un reporte legible del presupuesto."""
        lines = [
            f"Presupuesto de contexto ({self.max_tokens:,} tokens):",
            f"  System prompt:      {self.system_prompt_tokens:>8,}",
            f"  Herramientas:       {self.tool_definitions_tokens:>8,}",
            f"  Historial:          {self.history_tokens:>8,}",
            f"  Resultados tools:   {self.tool_results_tokens:>8,}",
            f"  Reserva respuesta:  {self.reserved_for_output:>8,}",
            f"  ---",
            f"  Usado:              {self.used:>8,}",
            f"  Disponible:         {self.available:>8,}",
            f"  Utilizacion:        {self.utilization:>8.1%}",
        ]
        return "\n".join(lines)
```

Hagamos cuentas para un agente de investigacion tipico con una ventana de 200K tokens:

| Componente | Tokens estimados |
|---|---|
| System prompt | 3,000 |
| 20 herramientas | 8,000 |
| 15 pasos de conversacion | 30,000 |
| 10 resultados de herramientas | 25,000 |
| Reserva para respuesta | 4,096 |
| **Total** | **70,096** |

Mas de un tercio del contexto consumido, y eso sin contar que muchos de esos tokens son ruido que no aporta a la tarea actual. Con un modelo de 128K tokens, estarias al 55% de capacidad. Y si tu agente ejecuta 25 pasos en lugar de 15, facilmente llegas al 80%.

La eficiencia del contexto no solo se mide en cuanto cabe, sino en cuanto de lo que cabe es realmente util.

---

## 3.2 El costo oculto: latencia, dinero y degradacion de atencion

La ventana de contexto no solo tiene un limite de tamano. Llenarla tiene tres costos que los equipos subestiman sistematicamente.

### Costo 1: dinero

Cada token de entrada cuesta dinero. En marzo de 2026, los precios varian significativamente entre proveedores y modelos, pero como referencia: un agente que consume 100,000 tokens de entrada por tarea y procesa 1,000 tareas al dia esta enviando 100 millones de tokens diarios. A $3 por millon de tokens de entrada (un precio tipico de gama media), eso son $300 diarios, $9,000 mensuales solo en input. Cada token innecesario en el contexto es dinero tirado.

### Costo 2: latencia

Los transformadores procesan la secuencia de entrada completa antes de generar el primer token de salida. El tiempo de procesamiento crece (aproximadamente) linealmente con la longitud del contexto para el prefill, y cuadraticamente para la atencion en modelos sin optimizaciones como Flash Attention. Un contexto de 100K tokens tarda significativamente mas en procesarse que uno de 10K tokens. En un agente que ejecuta 15 pasos, esa latencia se acumula: cada paso procesa un contexto mas largo que el anterior.

### Costo 3: degradacion de atencion ("Lost in the Middle")

Este es el costo mas insidioso porque es invisible.

En 2023, un grupo de investigadores de Stanford publico un paper seminal: "Lost in the Middle: How Language Models Use Long Contexts" [Liu et al., 2023]. Su hallazgo fue revelador: **los LLMs tienen una curva de atencion en forma de U**. Recuerdan bien lo que esta al principio del contexto (efecto de primacia) y lo que esta al final (efecto de recencia), pero tienden a "olvidar" la informacion que esta en el centro.

Los numeros son concretos. Liu et al. midieron una caida de mas del 30% en precision en question answering multi-documento cuando el documento con la respuesta se movia de la posicion 1 a la posicion 10 en un contexto de 20 documentos. La informacion no desaparece del contexto --sigue ahi en los tokens--, pero el mecanismo de atencion del transformador le asigna menos peso.

La causa raiz esta en como funcionan los encodings posicionales, particularmente Rotary Position Embedding (RoPE), que introduce un efecto de decaimiento a largo plazo: los tokens al inicio y al final de la secuencia reciben mas atencion que los del medio.

```python
import numpy as np


def attention_recovery_curve(
    position: int, context_length: int
) -> float:
    """Aproximacion empirica de la curva de recuperacion
    observada en "Lost in the Middle".

    NOTA: Esto modela la forma de la curva observada en los
    experimentos, NO el mecanismo de atencion real del transformer.
    El efecto U-shape emerge de la interaccion entre posiciones
    relativas aprendidas y la distribucion de la informacion.
    """
    normalized = position / context_length
    primacy = np.exp(-5 * normalized)
    recency = np.exp(-5 * (1 - normalized))
    baseline = 0.1
    return primacy + recency + baseline


# Las posiciones centrales muestran ~50% menor recuperacion
# que las posiciones en los extremos
```

### Como afecta esto a los agentes

En un agente multi-paso, el problema se manifiesta de forma particularmente insidiosa. Imagina un agente que ejecuta 20 pasos para completar una tarea de investigacion:

- **Paso 1-3**: El agente recibe las instrucciones y hace busquedas iniciales. Esta informacion esta al inicio del contexto (primacia: alta recuperacion).
- **Paso 8-12**: El agente encuentra datos criticos que son centrales para la tarea. Esta informacion queda en el **medio** del contexto (baja recuperacion).
- **Paso 18-20**: El agente necesita sintetizar todo. Pero los datos criticos del medio son precisamente los que el modelo recuerda peor.

Es como si un investigador tomara notas detalladas al principio y al final de su jornada, pero las notas del mediodia estuvieran borrosas. Y peor aun, el investigador no sabe que estan borrosas: cree que las puede leer perfectamente.

Un estudio de Chroma en 2025 que evaluo 18 modelos frontera --incluyendo GPT-4.1, Claude Opus 4 y Gemini 2.5-- confirmo que **todos** los modelos muestran degradacion de rendimiento conforme la longitud del input aumenta. Los modelos mas recientes han reducido la severidad del problema, pero no lo han eliminado.

La industria ya reconoce esto como un desafio central. Segun datos de 2025, casi el 65% de los fallos en agentes de IA empresariales se atribuyen a **context drift** o perdida de memoria durante razonamiento multi-paso, no a agotamiento bruto del contexto. El contexto no se llena; se degrada.

---

## 3.3 Estrategias de compresion y gestion de contexto

Ahora que entendemos el problema, hablemos de soluciones concretas. Cada estrategia tiene trade-offs diferentes, y la eleccion correcta depende de tu caso de uso.

### Estrategia 1: Resumen progresivo (*progressive summarization*)

La estrategia mas directa: cuando el historial crece mas alla de un umbral, pedirle al propio LLM (o a uno mas pequeno y barato) que resuma los pasos anteriores. El resumen reemplaza el historial detallado.

```python
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class ConversationManager:
    """Gestiona el contexto con compresion automatica.

    Cuando el historial excede el umbral, los mensajes antiguos
    se comprimen en un resumen. Los mensajes recientes se mantienen
    en detalle completo.
    """
    messages: list = field(default_factory=list)
    summary: str = ""
    max_detail_tokens: int = 20_000
    summarize_fn: Callable = None  # Funcion que llama al LLM

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self._maybe_compress()

    def _maybe_compress(self):
        total_tokens = self._estimate_tokens()
        if total_tokens > self.max_detail_tokens:
            midpoint = len(self.messages) // 2
            old_messages = self.messages[:midpoint]
            recent_messages = self.messages[midpoint:]

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
                "content": (
                    f"Resumen de la conversacion previa:\n{self.summary}"
                )
            })
        context.extend(self.messages)
        return context

    def _estimate_tokens(self) -> int:
        # Estimacion: ~4 caracteres por token en espanol.
        # Para presupuestos precisos, usa tiktoken o el tokenizer
        # de tu modelo.
        return sum(len(m["content"]) // 4 for m in self.messages)
```

**Ventaja**: Preserva la informacion semantica importante mientras reduce drasticamente el uso de tokens. El agente "recuerda" que hizo, aunque no los detalles exactos.

**Desventaja**: Toda compresion implica perdida. Los detalles especificos (numeros exactos, nombres, fechas) pueden perderse en el resumen. Y el resumen en si cuesta tokens: necesitas una llamada extra al LLM para generarlo.

**Cuando usarla**: Agentes conversacionales de larga duracion, agentes de soporte al cliente, cualquier caso donde la continuidad semantica importa mas que los detalles exactos.

### Estrategia 2: Ventana deslizante (*sliding window*)

Inspirada directamente en los protocolos de red y en las tecnicas de procesamiento de senales, la sliding window es brutal pero efectiva: manten solo los ultimos N mensajes y descarta el resto.

```python
def sliding_window(messages: list, window_size: int = 10) -> list:
    """Mantener solo los ultimos N mensajes.

    Simple, predecible, facil de razonar. Tambien la que mas
    informacion pierde. Usala combinada con otras estrategias.
    """
    if len(messages) <= window_size:
        return messages
    return messages[-window_size:]
```

Es lo que hacemos naturalmente en una conversacion humana: recordamos las ultimas frases que nos dijeron, pero no podemos repetir textualmente lo que alguien nos dijo hace 30 minutos.

**Ventaja**: Simplicidad extrema. Cero latencia adicional. Cero costo adicional. Predecible.

**Desventaja**: Perdida total de informacion antigua. Si el agente necesita un dato del paso 2 cuando va en el paso 15, se perdio.

**Cuando usarla**: Como baseline o como complemento de otras estrategias. Nunca como unica defensa en agentes que ejecutan muchos pasos.

### Estrategia 3: Memoria jerarquica

La estrategia mas sofisticada y se inspira directamente en como los sistemas de archivos y las caches de un procesador manejan los datos: con niveles de abstraccion.

Imagina tres niveles:

1. **Nivel 0 (detalle completo)**: Los ultimos 5 mensajes tal cual.
2. **Nivel 1 (resumenes recientes)**: Resumenes de bloques de mensajes anteriores (cada 5-10 mensajes se resumen en un parrafo).
3. **Nivel 2 (resumen ejecutivo)**: Un resumen de los resumenes, que captura solo los hechos y decisiones clave de toda la conversacion.

```python
@dataclass
class HierarchicalMemory:
    """Memoria jerarquica inspirada en niveles de cache.

    L0: detalle completo (cache L1 del CPU)
    L1: resumenes de bloques (cache L2)
    L2: resumen ejecutivo (RAM principal)

    La informacion mas reciente tiene maximo detalle.
    Conforme envejece, se comprime progresivamente.
    """
    l0_messages: list = field(default_factory=list)
    l1_summaries: list = field(default_factory=list)
    l2_summary: str = ""

    l0_max: int = 5
    l1_max: int = 10
    summarize_fn: Callable = None

    def add_message(self, message: dict):
        self.l0_messages.append(message)

        if len(self.l0_messages) > self.l0_max:
            # Overflow de L0 -> comprimir a L1
            overflow = self.l0_messages[:-self.l0_max]
            self.l0_messages = self.l0_messages[-self.l0_max:]

            block_summary = self.summarize_fn(overflow)
            self.l1_summaries.append(block_summary)

            if len(self.l1_summaries) > self.l1_max:
                # Overflow de L1 -> comprimir a L2
                old_summaries = self.l1_summaries[:-self.l1_max]
                self.l1_summaries = self.l1_summaries[-self.l1_max:]

                self.l2_summary = self.summarize_fn(
                    [self.l2_summary] + old_summaries
                )

    def build_context(self) -> str:
        """Construye el contexto combinando los tres niveles."""
        parts = []
        if self.l2_summary:
            parts.append(f"[Contexto general]: {self.l2_summary}")
        for i, s in enumerate(self.l1_summaries):
            parts.append(f"[Bloque {i+1}]: {s}")
        for m in self.l0_messages:
            parts.append(f"[{m['role']}]: {m['content']}")
        return "\n\n".join(parts)
```

La analogia con la jerarquia de memoria de un computador es precisa: los datos "calientes" (recientes, relevantes) viven en cache rapida con maximo detalle. Los datos "tibios" viven en un nivel intermedio con compresion moderada. Los datos "frios" viven en almacenamiento comprimido con solo los hechos esenciales.

**Ventaja**: Balance optimo entre retencion de informacion y uso de tokens. Escala bien para sesiones largas.

**Desventaja**: Complejidad de implementacion. Multiples llamadas de resumen. La calidad depende criticamente de la funcion de resumen.

**Cuando usarla**: Agentes que ejecutan decenas de pasos, asistentes de larga duracion, cualquier caso donde necesitas equilibrar profundidad de historial con eficiencia de contexto.

### Estrategia 4: Seleccion dinamica de herramientas

Recuerda nuestro calculo del presupuesto de contexto: 20 herramientas podian consumir 8,000 tokens. Pero, realmente necesita el agente ver las 20 herramientas en cada paso?

Si un agente esta en el paso de "escribir un informe", no necesita ver la definicion de la herramienta de "eliminar archivos" o "enviar correos". Inyectar todas las herramientas disponibles en cada paso es como cargar todas las bibliotecas de un lenguaje de programacion en memoria cuando tu programa solo usa tres.

```python
class DynamicToolSelector:
    """Selecciona herramientas relevantes para el paso actual.

    En lugar de inyectar las 30 herramientas en cada invocacion,
    seleccionamos las 5-7 mas relevantes para la tarea actual.
    Ahorro tipico: 60-80% del tool tax.
    """

    def __init__(self, all_tools: list[dict], embedder):
        self.all_tools = {t["name"]: t for t in all_tools}
        self.embedder = embedder
        # Pre-computar embeddings de las descripciones
        self.tool_embeddings = {
            t["name"]: embedder.embed(
                f"{t['name']}: {t['description']}"
            )
            for t in all_tools
        }

    def select_tools(
        self,
        task_description: str,
        max_tools: int = 5,
        always_include: list[str] = None,
    ) -> list[dict]:
        """Selecciona las herramientas mas relevantes."""
        selected = []

        # Herramientas que siempre deben estar disponibles
        if always_include:
            for name in always_include:
                if name in self.all_tools:
                    selected.append(self.all_tools[name])

        # Buscar por similitud semantica
        task_embedding = self.embedder.embed(task_description)
        scores = {
            name: cosine_similarity(task_embedding, emb)
            for name, emb in self.tool_embeddings.items()
            if name not in (always_include or [])
        }

        # Seleccionar las mas relevantes
        sorted_tools = sorted(
            scores.items(), key=lambda x: x[1], reverse=True
        )
        remaining_slots = max_tools - len(selected)
        for name, score in sorted_tools[:remaining_slots]:
            selected.append(self.all_tools[name])

        return selected


def cosine_similarity(a, b) -> float:
    """Similaridad coseno entre dos vectores."""
    import numpy as np
    return float(
        np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    )
```

Anthropic ha adoptado un enfoque similar con su Tool Search nativo, donde el modelo puede buscar en un catalogo de herramientas en lugar de tenerlas todas en el contexto. La reduccion tipica del tool tax es del 60-80% cuando pasas de inyectar todas las herramientas a seleccionar dinamicamente las relevantes.

### Estrategia 5: Compresion de resultados de herramientas

Los resultados de herramientas son a menudo el mayor consumidor de tokens en agentes de investigacion. Una busqueda web puede devolver paginas enteras de texto, pero el agente solo necesita unos parrafos relevantes.

```python
def compress_tool_result(
    llm, result: str, task: str, max_tokens: int = 500
) -> str:
    """Comprime el resultado de una herramienta a lo esencial.

    En lugar de inyectar 2,000 tokens de una pagina web,
    extraemos los 200-500 tokens relevantes para la tarea.
    """
    if estimate_tokens(result) <= max_tokens:
        return result  # No necesita compresion

    prompt = f"""Extrae SOLO la informacion relevante para esta tarea:
Tarea: {task}

Resultado de herramienta:
{result}

Informacion relevante (se conciso, maximo {max_tokens} tokens):"""

    compressed = llm.generate(prompt, max_tokens=max_tokens)
    return compressed


def estimate_tokens(text: str) -> int:
    """Estimacion rapida de tokens (~4 chars/token en espanol)."""
    return len(text) // 4
```

**Ventaja**: Reduccion dramatica del consumo de tokens por resultados de herramientas. Un resultado de 2,000 tokens se reduce a 200-500 tokens relevantes.

**Desventaja**: Costo de una llamada adicional al LLM por cada compresion. Y la compresion puede perder detalles importantes si el modelo de compresion no entiende bien la tarea.

**Cuando usarla**: Siempre que los resultados de herramientas superen un umbral (por ejemplo, 500 tokens). Usa un modelo barato y rapido para la compresion.

### Estrategia 6: Map-reduce sobre contexto largo

Cuando la informacion que debemos procesar excede la ventana de contexto, podemos aplicar el mismo patron de **map-reduce** que usamos en sistemas distribuidos: dividir el problema, procesar cada parte y combinar los resultados.

```python
async def map_reduce_context(
    documents: list[str],
    question: str,
    llm_call,
    chunk_size: int = 4000,
) -> str:
    """Procesa documentos que no caben en una sola ventana.

    MAP: extraer informacion relevante de cada fragmento
    REDUCE: combinar las extracciones en una respuesta coherente
    """
    # MAP: procesar cada documento de forma independiente
    partial_answers = []
    for doc in documents:
        chunks = split_into_chunks(doc, chunk_size)
        for chunk in chunks:
            answer = await llm_call(
                f"Basandote en este fragmento, responde: "
                f"{question}\n\nFragmento: {chunk}"
            )
            partial_answers.append(answer)

    # REDUCE: combinar respuestas parciales
    combined = "\n".join(partial_answers)
    final_answer = await llm_call(
        f"Sintetiza estas respuestas parciales en una "
        f"respuesta coherente a: {question}\n\n"
        f"Respuestas parciales:\n{combined}"
    )
    return final_answer


def split_into_chunks(text: str, chunk_size: int) -> list[str]:
    """Divide texto en fragmentos de tamano aproximado."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0

    for word in words:
        current_chunk.append(word)
        current_size += len(word) // 4 + 1  # Estimacion de tokens
        if current_size >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_size = 0

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
```

**Ventaja**: Permite procesar cantidades de informacion que simplemente no cabrian en una sola ventana de contexto.

**Desventaja**: Multiples llamadas al LLM incrementan la latencia y el gasto. Y la fase de reduccion puede perder matices que solo son visibles cuando se ven todos los documentos juntos.

---

## 3.4 El efecto "Lost in the Middle" en la practica: donde poner la informacion critica

El fenomeno de "Lost in the Middle" no es solo un hallazgo academico. Tiene implicaciones directas para como estructuras el contexto de tu agente. Aqui van tres reglas practicas derivadas de la investigacion:

**Regla 1: Pon la informacion mas critica al inicio y al final del contexto.**

El system prompt va naturalmente al inicio (bien). Los resultados de la ultima herramienta van naturalmente al final (bien). Pero las instrucciones especificas de la tarea, las restricciones de seguridad y los datos criticos de pasos intermedios deben colocarse estrategicamente, no dejarse caer donde caigan.

**Regla 2: Resume los pasos intermedios, no los acumules.**

En lugar de mantener el historial completo de 20 pasos (donde los pasos 8-12 quedan en la zona muerta), resume los pasos antiguos y manten solo los recientes en detalle. Esto mueve la informacion critica de la zona media a las zonas de alta recuperacion.

**Regla 3: Repite la informacion clave al final del contexto.**

Si hay un dato critico que el agente necesita para su siguiente accion, no confies en que lo "recuerde" de hace 15 pasos. Inyectalo explicitamente al final del contexto, justo antes de pedirle al modelo que genere su respuesta.

```python
def build_optimized_context(
    system_prompt: str,
    summary: str,
    recent_messages: list,
    current_task: str,
    critical_data: str = "",
) -> list[dict]:
    """Construye un contexto optimizado para minimizar
    el efecto 'Lost in the Middle'.

    Estructura:
    1. System prompt (inicio - alta recuperacion)
    2. Resumen de pasos anteriores (zona media - comprimido)
    3. Mensajes recientes (pre-final - alta recuperacion)
    4. Datos criticos + tarea actual (final - maxima recuperacion)
    """
    context = [
        {"role": "system", "content": system_prompt},
    ]

    if summary:
        context.append({
            "role": "system",
            "content": f"Resumen de acciones previas:\n{summary}"
        })

    context.extend(recent_messages)

    # Inyectar datos criticos al final para maxima recuperacion
    if critical_data:
        context.append({
            "role": "system",
            "content": (
                f"DATOS CRITICOS para la tarea actual:\n{critical_data}"
            )
        })

    context.append({
        "role": "user",
        "content": current_task,
    })

    return context
```

---

## 3.5 El framework completo: ContextBudgetManager

Integremos todas las estrategias en un sistema cohesivo que monitorea el uso del contexto en tiempo real y aplica compresion automaticamente cuando se acerca a los limites.

```python
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional


class CompressionStrategy(Enum):
    NONE = "none"
    SLIDING_WINDOW = "sliding_window"
    SUMMARIZE = "summarize"
    HIERARCHICAL = "hierarchical"


@dataclass
class ContextBudgetManager:
    """Gestor completo de presupuesto de contexto.

    Monitorea el uso en tiempo real, emite alertas cuando se
    acerca a limites, y aplica compresion automaticamente.
    """
    max_tokens: int
    summarize_fn: Optional[Callable] = None

    # Umbrales de alerta y accion
    warning_threshold: float = 0.6   # 60%: emitir advertencia
    compress_threshold: float = 0.75  # 75%: comprimir automaticamente
    critical_threshold: float = 0.9   # 90%: compresion agresiva

    # Estado interno
    system_prompt: str = ""
    system_prompt_tokens: int = 0
    tool_definitions: list = field(default_factory=list)
    tool_definitions_tokens: int = 0
    messages: list = field(default_factory=list)
    summary: str = ""
    reserved_for_output: int = 4096

    # Metricas
    compressions_applied: int = 0
    tokens_saved: int = 0

    def set_system_prompt(self, prompt: str):
        self.system_prompt = prompt
        self.system_prompt_tokens = self._count_tokens(prompt)

    def set_tools(self, tools: list[dict]):
        self.tool_definitions = tools
        self.tool_definitions_tokens = sum(
            self._count_tokens(str(t)) for t in tools
        )

    def add_message(self, role: str, content: str):
        tokens = self._count_tokens(content)
        self.messages.append({
            "role": role,
            "content": content,
            "tokens": tokens,
        })
        self._check_and_compress()

    @property
    def history_tokens(self) -> int:
        return sum(m["tokens"] for m in self.messages)

    @property
    def summary_tokens(self) -> int:
        return self._count_tokens(self.summary) if self.summary else 0

    @property
    def total_used(self) -> int:
        return (
            self.system_prompt_tokens
            + self.tool_definitions_tokens
            + self.summary_tokens
            + self.history_tokens
            + self.reserved_for_output
        )

    @property
    def utilization(self) -> float:
        return self.total_used / self.max_tokens

    def _check_and_compress(self):
        """Aplica compresion segun el nivel de utilizacion."""
        util = self.utilization

        if util >= self.critical_threshold:
            self._compress(aggressive=True)
        elif util >= self.compress_threshold:
            self._compress(aggressive=False)
        elif util >= self.warning_threshold:
            print(
                f"[ContextBudget] ADVERTENCIA: {util:.0%} utilizado "
                f"({self.total_used:,}/{self.max_tokens:,} tokens)"
            )

    def _compress(self, aggressive: bool = False):
        """Comprime el historial para liberar espacio."""
        if not self.summarize_fn or len(self.messages) < 4:
            return

        before_tokens = self.history_tokens

        if aggressive:
            # Comprimir todo excepto los ultimos 3 mensajes
            cutpoint = max(len(self.messages) - 3, 1)
        else:
            # Comprimir la primera mitad
            cutpoint = len(self.messages) // 2

        old_messages = self.messages[:cutpoint]
        old_text = "\n".join(
            f"{m['role']}: {m['content']}" for m in old_messages
        )

        new_summary = self.summarize_fn(
            previous_summary=self.summary,
            new_content=old_text,
        )
        self.summary = new_summary
        self.messages = self.messages[cutpoint:]

        after_tokens = self.history_tokens + self.summary_tokens
        saved = before_tokens - after_tokens + (
            self.summary_tokens if not self.summary else 0
        )

        self.compressions_applied += 1
        self.tokens_saved += max(0, saved)

    def get_context(self) -> list[dict]:
        """Construye el contexto optimizado para el LLM."""
        context = [{"role": "system", "content": self.system_prompt}]

        if self.summary:
            context.append({
                "role": "system",
                "content": (
                    f"Resumen de interacciones previas:\n{self.summary}"
                )
            })

        for m in self.messages:
            context.append({"role": m["role"], "content": m["content"]})

        return context

    def get_stats(self) -> dict:
        """Retorna estadisticas de uso."""
        return {
            "max_tokens": self.max_tokens,
            "total_used": self.total_used,
            "utilization": f"{self.utilization:.1%}",
            "system_prompt": self.system_prompt_tokens,
            "tools": self.tool_definitions_tokens,
            "summary": self.summary_tokens,
            "history": self.history_tokens,
            "messages_count": len(self.messages),
            "compressions": self.compressions_applied,
            "tokens_saved": self.tokens_saved,
        }

    def _count_tokens(self, text: str) -> int:
        """Estimacion de tokens.

        En produccion, reemplaza con tiktoken o el tokenizer
        de tu modelo para conteos exactos.
        """
        return len(text) // 4
```

Este `ContextBudgetManager` es el equivalente para agentes de lo que `malloc` y `free` son para C: el mecanismo que te permite usar el recurso finito de forma controlada. La diferencia es que aqui la "liberacion" no es destruccion sino compresion.

---

## 3.6 RAG como extension del contexto

Hasta ahora hemos hablado de gestionar lo que **ya esta** en el contexto. Pero hay una pregunta de diseno mas fundamental: que deberia estar en el contexto en primer lugar?

RAG (Retrieval-Augmented Generation) extiende la capacidad del agente mas alla de la ventana de contexto: en lugar de meter toda la informacion desde el inicio, guardamos la informacion en un indice externo y solo recuperamos los fragmentos relevantes cuando los necesitamos.

### Que vive en el contexto vs que vive en RAG

```python
class ContextStrategy:
    """Guia de decision: contexto directo vs RAG."""

    # SIEMPRE en el contexto directo:
    ALWAYS_IN_CONTEXT = [
        "instrucciones del sistema",         # Critico siempre
        "estado actual de la tarea",         # Necesario para el paso actual
        "ultimas acciones y resultados",     # Continuidad inmediata
        "restricciones de seguridad",        # No negociable
    ]

    # SIEMPRE en RAG (busqueda bajo demanda):
    ALWAYS_IN_RAG = [
        "documentacion de referencia",       # Solo cuando se necesita
        "historial de sesiones pasadas",     # Memoria a largo plazo
        "base de conocimiento del dominio",  # Enorme, parcialmente relevante
        "logs y registros historicos",       # Voluminosos
    ]

    # DEPENDE del caso de uso:
    DEPENDS = [
        "resultados de herramientas previas",  # Se necesitaran otra vez?
        "definiciones de herramientas",         # Se usaran todas?
        "ejemplos few-shot",                    # Mejoran la calidad?
    ]
```

La decision clave es: para cada pieza de informacion, el costo de tenerla en contexto (tokens, degradacion de atencion) supera al costo de buscarla bajo demanda (latencia, riesgo de no encontrarla)?

### El trade-off entre contexto inyectado y contexto generado

Hay un trade-off sutil que pocos discuten: cada fragmento que inyectas via RAG ocupa espacio que el modelo podria usar para "pensar". Un modelo con 100K tokens de contexto que tiene 95K ocupados por documentos inyectados tiene solo 5K tokens para razonar.

Las tecnicas de inference-time scaling que discutimos en el capitulo anterior --chain-of-thought, razonamiento extendido-- requieren espacio en la ventana de contexto para que el modelo desarrolle su razonamiento. Si llenamos el contexto con datos, estamos literalmente quitandole espacio para pensar.

Mi regla practica de partida: **no uses mas del 60-70% de la ventana para datos inyectados**. El resto debe quedar disponible para el razonamiento del modelo y la generacion de la respuesta.

Dicho esto, este porcentaje depende fuertemente del modelo. Algunos modelos mantienen buena calidad de recuperacion hasta el 85-90% de su ventana. Otros se degradan despues del 50%. **La recomendacion real es: mide la calidad de las respuestas de tu modelo a diferentes niveles de utilizacion con pruebas de tipo "needle-in-a-haystack" y establece tu limite basandote en datos, no en reglas generales.** El 60-70% es un punto de partida conservador, no una ley universal.

---

## 3.7 Aislamiento de contexto: el patron multi-agente

Una de las estrategias mas efectivas para gestionar el contexto no es comprimir ni resumir, sino **dividir**.

En lugar de un solo agente con una ventana de contexto enorme tratando de hacer todo, usas multiples sub-agentes, cada uno con su propio contexto aislado y enfocado en una sub-tarea especifica.

Anthropic documento este patron en su investigador multi-agente: muchos agentes con contextos aislados superaron consistentemente a un agente unico con contexto compartido, en gran parte porque cada sub-agente podia dedicar toda su ventana de contexto a una sub-tarea especifica [Anthropic, 2025].

El principio es simple: la motivacion detras de la biblioteca Swarm de OpenAI fue la **separacion de concerns** --un equipo de agentes donde cada uno maneja sub-tareas especificas con sus propias herramientas, instrucciones y ventana de contexto.

```python
from dataclasses import dataclass


@dataclass
class SubAgent:
    """Un sub-agente con contexto aislado."""
    name: str
    system_prompt: str
    tools: list[str]
    max_context_tokens: int = 50_000

    def run(self, task: str, llm) -> str:
        """Ejecuta la sub-tarea con contexto limpio."""
        # Cada sub-agente empieza con contexto limpio
        # No hereda el historial de otros agentes
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": task},
        ]
        return llm.generate(messages)


class OrchestratorAgent:
    """Orquestador que divide tareas entre sub-agentes."""

    def __init__(self, sub_agents: list[SubAgent], llm):
        self.agents = {a.name: a for a in sub_agents}
        self.llm = llm

    def run(self, task: str) -> str:
        # 1. Descomponer la tarea
        subtasks = self._decompose(task)

        # 2. Asignar cada sub-tarea al agente apropiado
        results = {}
        for subtask in subtasks:
            agent = self.agents[subtask["agent"]]
            results[subtask["name"]] = agent.run(
                subtask["description"], self.llm
            )

        # 3. Sintetizar resultados
        # El orquestador solo ve los resultados finales,
        # no el historial completo de cada sub-agente
        return self._synthesize(task, results)

    def _decompose(self, task: str) -> list[dict]:
        """Usa el LLM para descomponer la tarea."""
        # Simplificado para ilustrar
        pass

    def _synthesize(self, task: str, results: dict) -> str:
        """Sintetiza los resultados de los sub-agentes."""
        pass
```

**Ventaja**: Cada sub-agente trabaja con un contexto limpio y enfocado. No hay degradacion por acumulacion de historial. Cada ventana de contexto se usa eficientemente.

**Desventaja**: El orquestador necesita manejar la comunicacion entre agentes, lo que introduce latencia y complejidad. La informacion que un sub-agente descubre no esta automaticamente disponible para otros.

**Cuando usarla**: Tareas complejas que se descomponen naturalmente en sub-tareas independientes. Sistemas que procesan multiples tipos de informacion (texto, codigo, datos).

---

## 3.8 Checklist de optimizacion de contexto

Antes de pasar al siguiente capitulo, aqui va una checklist practica para optimizar el uso del contexto en tu agente:

- [ ] **Mide tu tool tax.** Cuantos tokens consumen tus definiciones de herramientas? Si superan el 10% de tu ventana, considera seleccion dinamica.

- [ ] **Implementa un presupuesto de contexto.** Usa `ContextBudget` o similar para monitorear el uso en tiempo real. No esperes a que el contexto se llene para reaccionar.

- [ ] **Comprime resultados de herramientas.** Si un resultado de herramienta supera 500 tokens, comprimelo a lo esencial antes de inyectarlo al contexto.

- [ ] **Resume el historial progresivamente.** No mantengas 30 pasos en detalle completo. Resume los antiguos y manten solo los recientes.

- [ ] **Posiciona estrategicamente la informacion critica.** Pon los datos mas importantes al inicio y al final del contexto, no en el medio.

- [ ] **Mide la degradacion de tu modelo.** Ejecuta pruebas needle-in-a-haystack a diferentes niveles de utilizacion para conocer los limites reales de tu modelo, no los teoricos.

- [ ] **Considera aislamiento de contexto.** Si tu agente ejecuta mas de 15-20 pasos, evalua dividirlo en sub-agentes con contextos aislados.

- [ ] **Reserva espacio para pensar.** No uses mas del 60-70% de la ventana para datos inyectados. El modelo necesita espacio para razonar.

---

## Takeaway del capitulo

La ventana de contexto no es infinita, y llenarla sin criterio degrada silenciosamente la calidad de tu agente. Los 200K tokens que suenan a mucho se llenan rapidamente cuando sumas el system prompt, las herramientas, el historial y los resultados de tools. Y el problema no es solo de tamano: es de atencion. El fenomeno "Lost in the Middle" significa que incluso con espacio disponible, la informacion en la zona media del contexto se recupera con hasta 30% menos precision.

Gestiona el contexto con la misma disciplina con la que gestionas la RAM: monitorea el uso, comprime lo que puedes, descarta lo que no necesitas, y reserva espacio para lo que importa. Las estrategias --resumen progresivo, ventana deslizante, memoria jerarquica, seleccion dinamica de herramientas, compresion de resultados, aislamiento multi-agente-- no son mutuamente excluyentes. Los mejores agentes en produccion combinan varias.

En el proximo capitulo abordaremos el complemento natural de la gestion de contexto: la **memoria persistente**. Porque la ventana de contexto es la memoria de trabajo del agente --lo que tiene "en mente" ahora--, pero un agente que olvida todo entre sesiones es un agente que nunca aprende.

---

### Notas y referencias

- [Liu et al., 2023] Nelson F. Liu et al. "Lost in the Middle: How Language Models Use Long Contexts." Transactions of the ACL, 2024. Publicado inicialmente como arXiv:2307.03172, julio 2023.
- [Packer et al., 2023] Charles Packer, Sarah Wooders et al. "MemGPT: Towards LLMs as Operating Systems." arXiv:2310.08560, octubre 2023.
- [Anthropic, 2025] "Effective Context Engineering for AI Agents." Anthropic Engineering Blog.
- [LangChain, 2025] "Context Engineering for Agents." LangChain Blog.
- [Chroma, 2025] Evaluacion de 18 modelos frontera en tareas de contexto largo.
- [Park et al., 2023] Joon Sung Park et al. "Generative Agents: Interactive Simulacra of Human Behavior." UIST 2023. La funcion de scoring de memorias: importancia + recencia + relevancia.
- [Miller, 1956] George A. Miller. "The Magical Number Seven, Plus or Minus Two." Psychological Review.
- [Cowan, 2001] Nelson Cowan. "The magical number 4 in short-term memory." Behavioral and Brain Sciences.
