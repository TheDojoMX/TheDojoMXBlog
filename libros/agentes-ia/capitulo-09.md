# Capitulo 9: RAG -- La Paradoja de la Simplicidad

> "El 80% de los problemas de RAG son problemas de retrieval, no de generacion."

---

En el Capitulo 8 aprendimos a verificar que nuestros agentes funcionan correctamente. Ahora vamos a abordar el patron mas importante para conectar agentes con datos reales: **Retrieval-Augmented Generation** (RAG). Y vamos a descubrir que, despues de anos de complejidad creciente, las implementaciones simples siguen ganando.

RAG fue declarado "muerto" varias veces desde 2024. Cada vez que un proveedor anuncio ventanas de contexto mas grandes -- Gemini con 2 millones de tokens, Claude con 200K -- alguien publico un post titulado "RAG is dead". Y cada vez, la prediccion resulto incorrecta. Las ventanas de contexto mas grandes no eliminaron la necesidad de RAG por tres razones practicas: el costo de llenar un contexto de 2 millones de tokens es prohibitivo para la mayoria de las aplicaciones, la latencia crece linealmente con el tamano del contexto, y el fenomeno "Lost in the Middle" [Liu et al., 2023] degrada la calidad cuando hay demasiada informacion en el contexto.

RAG sigue vivo. Lo que cambio es nuestra comprension de que funciona y que no.

---

## 9.1 RAG en teoria vs RAG en produccion

### La promesa

La idea de RAG es elegante. Lewis et al. (2020) la formalizaron en su paper seminal: en lugar de confiar exclusivamente en el conocimiento que el modelo aprendio durante el entrenamiento, le proporcionamos informacion relevante recuperada de una base de datos en el momento de la generacion [Lewis et al., 2020]. Esto resuelve dos problemas fundamentales de los LLMs: el conocimiento desactualizado y las alucinaciones sobre datos especificos.

El pipeline clasico tiene tres fases:

```
Pregunta del usuario
    -> [1. Retrieval] Buscar documentos relevantes
    -> [2. Augmentation] Inyectar documentos en el contexto
    -> [3. Generation] Generar respuesta basada en los documentos
```

En teoria, es simple. En la practica, cada fase esconde decisiones criticas que determinan si tu sistema funciona o no.

### La realidad en produccion

Estos son los problemas reales que encuentras al desplegar RAG:

**Problema 1: la calidad del retrieval define el techo.** Si tus documentos recuperados no contienen la respuesta, el LLM no puede inventarla correctamente (o la inventara, lo cual es peor). Ningun modelo de generacion, por poderoso que sea, puede compensar un retrieval deficiente. Esta es la razon detras de la afirmacion que abre este capitulo: el 80% de los problemas de RAG son problemas de retrieval.

**Problema 2: el chunking importa mas de lo que parece.** Como divides tus documentos en fragmentos ("chunks") determina que puede encontrar el retriever. Un chunk demasiado pequeno pierde contexto; uno demasiado grande diluye la relevancia.

**Problema 3: los embeddings no son magicos.** Un embedding es una representacion numerica de un fragmento de texto en un espacio vectorial. La similitud coseno entre dos embeddings mide su "cercania semantica". Pero "cercania semantica" no siempre significa "relevante para la pregunta". La pregunta "como instalo Python?" y el fragmento "la instalacion de Python requiere descargar el instalador" son semanticamente cercanos. Pero la pregunta "que version de Python necesito para Django 5?" y el fragmento "Django 5 requiere Python 3.10+" pueden no ser tan cercanos en el espacio de embeddings, a pesar de que el fragmento contiene exactamente la respuesta.

**Problema 4: la evaluacion es difícil.** Como sabes si tu sistema RAG esta funcionando bien? "Le pregunte 10 cosas y respondio bien" no es suficiente. Necesitas metricas sistematicas, y esas metricas son mas complicadas de lo que parecen.

---

## 9.2 Chunking, embeddings y el arte de la indexacion

### La paradoja del chunking

El hallazgo mas sorprendente de los ultimos dos anos: **las implementaciones simples de chunking frecuentemente superan a las complejas**.

El benchmark de chunking de NVIDIA (2024) encontro que el chunking a nivel de pagina -- una de las estrategias mas simples -- logro la mayor precision (0.648) con la menor varianza en 5 datasets. Esto contradice la intuicion de que tecnicas sofisticadas basadas en semantica debian funcionar mejor.

Por que ocurre esto? La razon es que las tecnicas de chunking "inteligente" -- que intentan dividir por secciones semanticas, por parrafos tematicos o por estructura del documento -- introducen complejidad y puntos de fallo adicionales sin un beneficio proporcional. Un splitter recursivo simple con overlap captura la mayoria de la informacion relevante porque los embeddings modernos son lo suficientemente robustos para manejar fragmentos que no tienen limites "perfectos".

Veamos las estrategias principales:

```python
from dataclasses import dataclass


@dataclass
class Chunk:
    texto: str
    metadata: dict
    id: str


class ChunkerPorTamano:
    """Chunking por tamano fijo con overlap.
    Simple, robusto, y sorprendentemente efectivo."""

    def __init__(
        self,
        tamano: int = 512,
        overlap: int = 64,
    ):
        self.tamano = tamano
        self.overlap = overlap

    def chunk(self, texto: str, metadata: dict | None = None) -> list[Chunk]:
        metadata = metadata or {}
        chunks = []
        inicio = 0
        indice = 0

        while inicio < len(texto):
            fin = inicio + self.tamano
            fragmento = texto[inicio:fin]

            # Intentar cortar en un limite de oracion o parrafo
            if fin < len(texto):
                # Buscar el ultimo punto, salto de linea o punto y coma
                for sep in ["\n\n", "\n", ". ", "; "]:
                    ultimo_sep = fragmento.rfind(sep)
                    if ultimo_sep > self.tamano * 0.5:  # al menos mitad del chunk
                        fragmento = fragmento[: ultimo_sep + len(sep)]
                        fin = inicio + len(fragmento)
                        break

            chunks.append(
                Chunk(
                    texto=fragmento.strip(),
                    metadata={
                        **metadata,
                        "chunk_index": indice,
                        "char_start": inicio,
                        "char_end": fin,
                    },
                    id=f"{metadata.get('doc_id', 'doc')}_{indice}",
                )
            )

            inicio = fin - self.overlap
            indice += 1

        return chunks


class ChunkerContextual:
    """Chunking contextual: agrega contexto del documento a cada chunk.
    Inspirado en Contextual Retrieval de Anthropic, que redujo
    fallos de retrieval en 35% [Anthropic, 2024]."""

    def __init__(
        self,
        chunker_base: ChunkerPorTamano,
        cliente_llm,
    ):
        self.chunker_base = chunker_base
        self.llm = cliente_llm

    def chunk_con_contexto(
        self,
        texto_completo: str,
        metadata: dict | None = None,
    ) -> list[Chunk]:
        chunks_base = self.chunker_base.chunk(texto_completo, metadata)

        chunks_enriquecidos = []
        for chunk in chunks_base:
            # Generar un resumen breve del contexto del chunk
            contexto = self._generar_contexto(texto_completo, chunk.texto)
            chunk_enriquecido = Chunk(
                texto=f"{contexto}\n\n{chunk.texto}",
                metadata={**chunk.metadata, "tiene_contexto": True},
                id=chunk.id,
            )
            chunks_enriquecidos.append(chunk_enriquecido)

        return chunks_enriquecidos

    def _generar_contexto(self, documento: str, fragmento: str) -> str:
        """Usa un LLM barato para generar contexto del fragmento."""
        prompt = (
            f"Este fragmento es parte de un documento más largo. "
            f"Escribe 1-2 oraciones que sitúen este fragmento en "
            f"el contexto del documento completo.\n\n"
            f"Documento (primeros 500 chars): {documento[:500]}...\n\n"
            f"Fragmento: {fragmento[:300]}\n\n"
            f"Contexto:"
        )
        return self.llm.completar(prompt, max_tokens=100)
```

La recomendacion practica: **empieza con un splitter recursivo de 512-1024 tokens con 10-20% de overlap**. Solo agrega complejidad (chunking contextual, chunking semantico) cuando tus metricas de evaluacion demuestren que es necesario.

### Embeddings: lo que importa y lo que no

Invertir semanas optimizando embeddings rara vez produce mejoras significativas comparado con mejorar la calidad de los datos de entrada. La ley de Pareto aplicada a RAG: el 80% del impacto viene de tener buenos datos y un chunking razonable; solo el 20% viene de la eleccion del modelo de embeddings.

Dicho esto, la eleccion del modelo de embeddings no es irrelevante. Los factores que si importan:

```python
from dataclasses import dataclass


@dataclass
class ConfiguracionEmbeddings:
    """Configuracion para el modelo de embeddings."""
    modelo: str
    dimensiones: int
    max_tokens: int
    costo_por_millon_tokens: float
    latencia_promedio_ms: float

    def costo_indexacion(self, total_tokens: int) -> float:
        """Costo de indexar un corpus completo."""
        return (total_tokens / 1_000_000) * self.costo_por_millon_tokens

    def ram_indice_hnsw(self, num_vectores: int) -> float:
        """RAM estimada para un indice HNSW en GB."""
        # Cada vector: dimensiones * 4 bytes (float32)
        # HNSW overhead: ~1.5x del tamano base
        bytes_por_vector = self.dimensiones * 4 * 1.5
        return (num_vectores * bytes_por_vector) / (1024**3)


# Modelos populares en 2026
MODELOS_EMBEDDINGS = {
    "text-embedding-3-small": ConfiguracionEmbeddings(
        modelo="text-embedding-3-small",
        dimensiones=1536,
        max_tokens=8191,
        costo_por_millon_tokens=0.02,
        latencia_promedio_ms=50,
    ),
    "text-embedding-3-large": ConfiguracionEmbeddings(
        modelo="text-embedding-3-large",
        dimensiones=3072,
        max_tokens=8191,
        costo_por_millon_tokens=0.13,
        latencia_promedio_ms=80,
    ),
    "voyage-3": ConfiguracionEmbeddings(
        modelo="voyage-3",
        dimensiones=1024,
        max_tokens=32000,
        costo_por_millon_tokens=0.06,
        latencia_promedio_ms=60,
    ),
}

# Ejemplo de calculo:
# 1 millon de documentos, promedio 500 tokens cada uno
config = MODELOS_EMBEDDINGS["text-embedding-3-small"]
total_tokens = 1_000_000 * 500
print(f"Costo indexacion: ${config.costo_indexacion(total_tokens):.2f}")
print(f"RAM indice HNSW: {config.ram_indice_hnsw(1_000_000):.1f} GB")
# Costo indexacion: $10.00
# RAM indice HNSW: 8.6 GB
```

El cuello de botella que nadie menciona: los indices HNSW necesitan estar en RAM para consultas rapidas. Un millon de vectores de 1536 dimensiones requiere aproximadamente 8.6 GB solo para el indice. Esto es un costo operacional real que se subestima sistematicamente en los tutoriales.

---

## 9.3 Implementacion practica: de Naive RAG a produccion

### Naive RAG con PostgreSQL + pgvector

PostgreSQL con pgvector es suficiente para la mayoria de los casos. Las ventajas son enormes: una sola base de datos (simplicidad operacional), transacciones ACID para metadatos + vectores, un solo sistema que monitorear, menor costo de infraestructura.

```python
import asyncpg
import json
from dataclasses import dataclass


@dataclass
class ResultadoBusqueda:
    chunk_id: str
    texto: str
    metadata: dict
    score: float


class RAGStore:
    """Almacen RAG basado en PostgreSQL + pgvector."""

    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool = None

    async def conectar(self):
        self.pool = await asyncpg.create_pool(self.dsn)
        async with self.pool.acquire() as conn:
            # Crear extension y tabla si no existen
            await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS chunks (
                    id TEXT PRIMARY KEY,
                    texto TEXT NOT NULL,
                    metadata JSONB DEFAULT '{}',
                    embedding vector(1536),
                    created_at TIMESTAMP DEFAULT NOW()
                );
            """)
            # Indice HNSW para busqueda rapida
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS chunks_embedding_idx
                ON chunks
                USING hnsw (embedding vector_cosine_ops)
                WITH (m = 16, ef_construction = 64);
            """)

    async def insertar_chunks(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]],
    ):
        """Inserta chunks con sus embeddings."""
        async with self.pool.acquire() as conn:
            for chunk, emb in zip(chunks, embeddings):
                await conn.execute(
                    """
                    INSERT INTO chunks (id, texto, metadata, embedding)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (id) DO UPDATE
                    SET texto = $2, metadata = $3, embedding = $4
                    """,
                    chunk.id,
                    chunk.texto,
                    json.dumps(chunk.metadata),
                    str(emb),
                )

    async def buscar(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        filtro_metadata: dict | None = None,
    ) -> list[ResultadoBusqueda]:
        """Busca los chunks mas similares al query."""
        async with self.pool.acquire() as conn:
            # Busqueda vectorial con cosine distance
            if filtro_metadata:
                # Filtrar por metadata antes de busqueda vectorial
                condiciones = " AND ".join(
                    f"metadata->>'{k}' = '{v}'"
                    for k, v in filtro_metadata.items()
                )
                query = f"""
                    SELECT id, texto, metadata,
                           1 - (embedding <=> $1) as score
                    FROM chunks
                    WHERE {condiciones}
                    ORDER BY embedding <=> $1
                    LIMIT $2
                """
            else:
                query = """
                    SELECT id, texto, metadata,
                           1 - (embedding <=> $1) as score
                    FROM chunks
                    ORDER BY embedding <=> $1
                    LIMIT $2
                """

            rows = await conn.fetch(query, str(query_embedding), top_k)

            return [
                ResultadoBusqueda(
                    chunk_id=row["id"],
                    texto=row["texto"],
                    metadata=json.loads(row["metadata"]),
                    score=float(row["score"]),
                )
                for row in rows
            ]
```

Cuando NO usar PostgreSQL para vectores: cuando tienes mas de 10-50 millones de vectores, cuando necesitas sub-10ms de latencia consistente, o cuando necesitas busqueda distribuida. Alternativas como Qdrant, Weaviate o Pinecone justifican su complejidad adicional solo en esos escenarios.

### El pipeline RAG completo

```python
class PipelineRAG:
    """Pipeline RAG completo: query -> retrieval -> generation."""

    def __init__(
        self,
        store: RAGStore,
        cliente_embeddings,
        cliente_llm,
        top_k: int = 5,
        score_minimo: float = 0.3,
    ):
        self.store = store
        self.embeddings = cliente_embeddings
        self.llm = cliente_llm
        self.top_k = top_k
        self.score_minimo = score_minimo

    async def responder(
        self,
        pregunta: str,
        filtro: dict | None = None,
    ) -> dict:
        """Responde una pregunta usando RAG."""

        # 1. RETRIEVAL: buscar documentos relevantes
        query_emb = self.embeddings.encode(pregunta)
        resultados = await self.store.buscar(
            query_embedding=query_emb,
            top_k=self.top_k,
            filtro_metadata=filtro,
        )

        # Filtrar por score minimo
        relevantes = [r for r in resultados if r.score >= self.score_minimo]

        if not relevantes:
            return {
                "respuesta": "No encontré información relevante para responder.",
                "fuentes": [],
                "confianza": 0.0,
            }

        # 2. AUGMENTATION: construir contexto
        contexto = self._construir_contexto(relevantes)

        # 3. GENERATION: generar respuesta
        prompt = self._construir_prompt(pregunta, contexto)
        respuesta = self.llm.completar(prompt)

        return {
            "respuesta": respuesta,
            "fuentes": [
                {
                    "chunk_id": r.chunk_id,
                    "score": r.score,
                    "texto": r.texto[:200],
                }
                for r in relevantes
            ],
            "confianza": sum(r.score for r in relevantes) / len(relevantes),
        }

    def _construir_contexto(
        self, resultados: list[ResultadoBusqueda],
    ) -> str:
        """Construye el contexto a partir de los resultados."""
        partes = []
        for i, r in enumerate(resultados, 1):
            partes.append(
                f"[Fuente {i}] (relevancia: {r.score:.2f})\n{r.texto}"
            )
        return "\n\n---\n\n".join(partes)

    def _construir_prompt(self, pregunta: str, contexto: str) -> str:
        return (
            f"Responde la siguiente pregunta basándote ÚNICAMENTE "
            f"en el contexto proporcionado. Si el contexto no contiene "
            f"suficiente información para responder, dilo explícitamente. "
            f"Cita las fuentes usando [Fuente N].\n\n"
            f"Contexto:\n{contexto}\n\n"
            f"Pregunta: {pregunta}\n\n"
            f"Respuesta:"
        )
```

---

## 9.4 Evaluacion de RAG: metricas que importan

La evaluacion de RAG es mas complicada que la evaluacion de un LLM vanilla porque tienes **dos componentes independientes** que evaluar: la calidad del retrieval y la calidad de la generacion. Un fallo en cualquiera de los dos produce un resultado malo, pero las causas y las soluciones son diferentes.

### Metricas de retrieval

Estas metricas evaluan si el sistema encuentra los documentos correctos:

**Precision@k**: De los k documentos recuperados, cuantos son relevantes?

**Recall@k**: De todos los documentos relevantes que existen, cuantos aparecen en los top k?

**NDCG (Normalized Discounted Cumulative Gain)**: Mide no solo si los documentos relevantes aparecen, sino si aparecen **en las primeras posiciones**. Un documento relevante en la posicion 1 vale mas que en la posicion 5. NDCG correlaciona mas fuertemente con la calidad end-to-end del sistema RAG que las metricas binarias de relevancia [Label Your Data, 2026].

**MRR (Mean Reciprocal Rank)**: El inverso de la posicion del primer documento relevante, promediado sobre todas las queries. Si el primer documento relevante siempre esta en posicion 1, MRR = 1.0.

```python
import numpy as np
from dataclasses import dataclass


@dataclass
class MetricasRetrieval:
    precision_at_k: float
    recall_at_k: float
    ndcg_at_k: float
    mrr: float


def calcular_precision_at_k(
    recuperados: list[str], relevantes: set[str], k: int,
) -> float:
    """Precision@k: proporcion de documentos relevantes en top k."""
    top_k = recuperados[:k]
    relevantes_en_top_k = sum(1 for doc in top_k if doc in relevantes)
    return relevantes_en_top_k / k


def calcular_recall_at_k(
    recuperados: list[str], relevantes: set[str], k: int,
) -> float:
    """Recall@k: proporcion de documentos relevantes recuperados."""
    if not relevantes:
        return 1.0
    top_k = recuperados[:k]
    relevantes_en_top_k = sum(1 for doc in top_k if doc in relevantes)
    return relevantes_en_top_k / len(relevantes)


def calcular_ndcg_at_k(
    recuperados: list[str],
    relevancia: dict[str, float],
    k: int,
) -> float:
    """NDCG@k: Normalized Discounted Cumulative Gain.
    Premia documentos relevantes en posiciones altas."""
    top_k = recuperados[:k]

    # DCG: Discounted Cumulative Gain
    dcg = sum(
        relevancia.get(doc, 0.0) / np.log2(i + 2)
        for i, doc in enumerate(top_k)
    )

    # IDCG: DCG ideal (documentos ordenados por relevancia)
    relevancias_ordenadas = sorted(relevancia.values(), reverse=True)[:k]
    idcg = sum(
        rel / np.log2(i + 2)
        for i, rel in enumerate(relevancias_ordenadas)
    )

    if idcg == 0:
        return 0.0
    return dcg / idcg


def calcular_mrr(
    recuperados: list[str], relevantes: set[str],
) -> float:
    """MRR: Mean Reciprocal Rank."""
    for i, doc in enumerate(recuperados):
        if doc in relevantes:
            return 1.0 / (i + 1)
    return 0.0


def evaluar_retrieval(
    recuperados: list[str],
    relevantes: set[str],
    relevancia: dict[str, float] | None = None,
    k: int = 5,
) -> MetricasRetrieval:
    """Evalua todas las metricas de retrieval."""
    if relevancia is None:
        # Binario: relevante = 1.0, no relevante = 0.0
        relevancia = {doc: 1.0 for doc in relevantes}

    return MetricasRetrieval(
        precision_at_k=calcular_precision_at_k(recuperados, relevantes, k),
        recall_at_k=calcular_recall_at_k(recuperados, relevantes, k),
        ndcg_at_k=calcular_ndcg_at_k(recuperados, relevancia, k),
        mrr=calcular_mrr(recuperados, relevantes),
    )
```

### Metricas de generacion

Estas metricas evaluan la calidad de la respuesta generada:

**Faithfulness (Fidelidad)**: La respuesta se basa en los documentos recuperados o esta alucinando? Esta es la metrica mas critica para RAG. RAGAS la evalua descomponiendo la respuesta en afirmaciones individuales y verificando si cada una tiene soporte en el contexto [Es et al., 2023].

**Answer Relevancy (Relevancia de la respuesta)**: La respuesta contesta la pregunta que se hizo?

**Context Precision**: Los chunks recuperados que se usaron son realmente necesarios? Un context precision bajo significa que estas recuperando informacion irrelevante que diluye el contexto.

**Context Recall**: Los chunks recuperados contienen toda la informacion necesaria para responder?

```python
class EvaluadorRAG:
    """Evaluador de pipeline RAG con metricas de retrieval y generacion."""

    def __init__(self, cliente_llm, cliente_embeddings):
        self.llm = cliente_llm
        self.embeddings = cliente_embeddings

    def evaluar_faithfulness(
        self,
        respuesta: str,
        contexto: list[str],
    ) -> float:
        """Evalua si la respuesta es fiel al contexto proporcionado.
        Usa LLM-as-judge para descomponer y verificar afirmaciones."""

        prompt = (
            f"Analiza la siguiente respuesta y determina qué proporción "
            f"de sus afirmaciones están respaldadas por el contexto.\n\n"
            f"Contexto:\n"
            + "\n---\n".join(contexto)
            + f"\n\nRespuesta: {respuesta}\n\n"
            f"Instrucciones:\n"
            f"1. Lista cada afirmación factual en la respuesta.\n"
            f"2. Para cada una, indica si está respaldada por el contexto "
            f"(SÍ/NO).\n"
            f"3. Al final, da un score de 0.0 a 1.0 representando la "
            f"proporción de afirmaciones respaldadas.\n\n"
            f"Score (solo el número):"
        )
        resultado = self.llm.completar(prompt, max_tokens=10)
        try:
            return float(resultado.strip())
        except ValueError:
            return 0.5

    def evaluar_relevancia_respuesta(
        self,
        pregunta: str,
        respuesta: str,
    ) -> float:
        """Evalua si la respuesta es relevante para la pregunta."""
        emb_pregunta = self.embeddings.encode(pregunta)
        emb_respuesta = self.embeddings.encode(respuesta)

        # Similitud coseno
        similitud = np.dot(emb_pregunta, emb_respuesta) / (
            np.linalg.norm(emb_pregunta) * np.linalg.norm(emb_respuesta)
        )
        return float(max(0, similitud))

    def evaluar_caso_completo(
        self,
        pregunta: str,
        respuesta: str,
        contexto_recuperado: list[str],
        docs_relevantes_reales: set[str] | None = None,
        docs_recuperados: list[str] | None = None,
    ) -> dict:
        """Evaluacion completa de un caso RAG."""
        resultado = {
            "faithfulness": self.evaluar_faithfulness(
                respuesta, contexto_recuperado,
            ),
            "relevancia_respuesta": self.evaluar_relevancia_respuesta(
                pregunta, respuesta,
            ),
        }

        if docs_relevantes_reales and docs_recuperados:
            metricas_retrieval = evaluar_retrieval(
                docs_recuperados, docs_relevantes_reales, k=5,
            )
            resultado["retrieval"] = {
                "precision@5": metricas_retrieval.precision_at_k,
                "recall@5": metricas_retrieval.recall_at_k,
                "ndcg@5": metricas_retrieval.ndcg_at_k,
                "mrr": metricas_retrieval.mrr,
            }

        return resultado
```

### RAGAS: el framework estandar

RAGAS (Retrieval Augmented Generation Assessment) se ha consolidado como el framework de evaluacion mas usado para sistemas RAG [Es et al., 2023]. Su filosofia es evaluar retrieval y generacion de forma independiente, usando LLM-as-judge para las metricas de generacion.

```python
# Ejemplo de uso con RAGAS
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from datasets import Dataset

# Dataset de evaluacion
eval_data = {
    "question": [
        "¿Cuál es la política de devoluciones?",
        "¿Cuánto cuesta el plan premium?",
    ],
    "answer": [
        "Las devoluciones se aceptan dentro de 30 días con ticket original.",
        "El plan premium cuesta $99/mes con facturación anual.",
    ],
    "contexts": [
        [
            "Política: Devoluciones dentro de 30 días con ticket original. "
            "No se aceptan productos abiertos."
        ],
        [
            "Precios 2026: Plan básico $29/mes. Plan premium $99/mes "
            "(facturación anual) o $119/mes (mensual)."
        ],
    ],
    "ground_truth": [
        "Devoluciones dentro de 30 días con ticket original.",
        "El plan premium cuesta $99/mes con facturación anual.",
    ],
}

dataset = Dataset.from_dict(eval_data)
resultado = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    ],
)
print(resultado)
# {'faithfulness': 0.92, 'answer_relevancy': 0.88,
#  'context_precision': 0.85, 'context_recall': 0.90}
```

La regla practica: **invierte mas tiempo en construir un sistema de evaluacion que en optimizar la arquitectura**. Sin metricas, estas adivinando.

---

## 9.5 Patrones avanzados: re-ranking, query decomposition, hybrid search

### Hybrid search: lo mejor de dos mundos

La busqueda hibrida combina busqueda vectorial (dense) con busqueda lexica (sparse, tipicamente BM25). La combinacion suele superar a cualquiera de las dos por separado porque capturan tipos de relevancia diferentes:

- **Dense (vectorial)**: captura similitud *semantica*. "Perro" y "canino" estan cerca. Buena para parafraseo y preguntas conceptuales.
- **Sparse (BM25)**: captura coincidencia *lexica*. Busca las palabras exactas. Buena para nombres propios, codigos, terminos tecnicos, numeros de referencia.

En benchmarks comparativos, la busqueda hibrida con Reciprocal Rank Fusion (RRF) alcanzo NDCG@10 de 0.85, representando una mejora del 18% sobre busqueda dense unicamente [Dennyson, 2025].

```python
import math
from collections import defaultdict


class BuscadorHibrido:
    """Combina busqueda vectorial y lexica usando Reciprocal Rank Fusion."""

    def __init__(
        self,
        store_vectorial: RAGStore,
        buscador_bm25,
        cliente_embeddings,
        peso_dense: float = 0.6,
        peso_sparse: float = 0.4,
        k_rrf: int = 60,
    ):
        self.store = store_vectorial
        self.bm25 = buscador_bm25
        self.embeddings = cliente_embeddings
        self.peso_dense = peso_dense
        self.peso_sparse = peso_sparse
        self.k_rrf = k_rrf

    async def buscar(
        self,
        query: str,
        top_k: int = 10,
    ) -> list[ResultadoBusqueda]:
        """Busqueda hibrida con Reciprocal Rank Fusion."""

        # 1. Busqueda dense (vectorial)
        query_emb = self.embeddings.encode(query)
        resultados_dense = await self.store.buscar(
            query_embedding=query_emb, top_k=top_k * 2,
        )

        # 2. Busqueda sparse (BM25)
        resultados_sparse = self.bm25.buscar(query, top_k=top_k * 2)

        # 3. Fusionar con RRF
        scores_rrf = defaultdict(float)
        textos = {}

        for rank, r in enumerate(resultados_dense):
            scores_rrf[r.chunk_id] += (
                self.peso_dense / (self.k_rrf + rank + 1)
            )
            textos[r.chunk_id] = r

        for rank, r in enumerate(resultados_sparse):
            scores_rrf[r.chunk_id] += (
                self.peso_sparse / (self.k_rrf + rank + 1)
            )
            if r.chunk_id not in textos:
                textos[r.chunk_id] = r

        # Ordenar por score RRF
        ranking = sorted(
            scores_rrf.items(), key=lambda x: x[1], reverse=True,
        )[:top_k]

        return [
            ResultadoBusqueda(
                chunk_id=chunk_id,
                texto=textos[chunk_id].texto,
                metadata=textos[chunk_id].metadata,
                score=score,
            )
            for chunk_id, score in ranking
        ]
```

### Re-ranking: "recupera amplio, refina estrecho"

El patron "retrieve wide, rerank narrow" consistentemente supera a recuperar menos resultados directamente. La idea es recuperar un conjunto amplio de candidatos (20-50) con busqueda rapida pero imprecisa, y luego reordenarlos con un modelo mas preciso pero mas lento.

Los cross-encoders son los modelos mas usados para re-ranking. A diferencia de los bi-encoders (que generan embeddings independientes para query y documento), los cross-encoders procesan query y documento juntos, produciendo scores de relevancia mas precisos:

```python
class Reranker:
    """Re-ranking de resultados usando un cross-encoder."""

    def __init__(self, modelo_reranker: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        from sentence_transformers import CrossEncoder
        self.modelo = CrossEncoder(modelo_reranker)

    def rerankar(
        self,
        query: str,
        resultados: list[ResultadoBusqueda],
        top_k: int = 5,
    ) -> list[ResultadoBusqueda]:
        """Reordena resultados por relevancia usando cross-encoder."""
        if not resultados:
            return []

        # Crear pares (query, documento) para el cross-encoder
        pares = [(query, r.texto) for r in resultados]

        # Obtener scores de relevancia
        scores = self.modelo.predict(pares)

        # Combinar scores con resultados y reordenar
        scored = list(zip(resultados, scores))
        scored.sort(key=lambda x: x[1], reverse=True)

        return [
            ResultadoBusqueda(
                chunk_id=r.chunk_id,
                texto=r.texto,
                metadata=r.metadata,
                score=float(s),
            )
            for r, s in scored[:top_k]
        ]


class PipelineRAGAvanzado:
    """Pipeline RAG con busqueda hibrida y re-ranking."""

    def __init__(
        self,
        buscador: BuscadorHibrido,
        reranker: Reranker,
        cliente_llm,
    ):
        self.buscador = buscador
        self.reranker = reranker
        self.llm = cliente_llm

    async def responder(self, pregunta: str) -> dict:
        # Paso 1: Recuperar amplio (20 candidatos)
        candidatos = await self.buscador.buscar(pregunta, top_k=20)

        # Paso 2: Refinar estrecho (top 5 despues de re-ranking)
        relevantes = self.reranker.rerankar(pregunta, candidatos, top_k=5)

        # Paso 3: Generar respuesta
        contexto = "\n\n---\n\n".join(
            f"[Fuente {i+1}] {r.texto}" for i, r in enumerate(relevantes)
        )
        prompt = (
            f"Responde basándote ÚNICAMENTE en el contexto.\n\n"
            f"Contexto:\n{contexto}\n\n"
            f"Pregunta: {pregunta}\n\nRespuesta:"
        )
        respuesta = self.llm.completar(prompt)

        return {
            "respuesta": respuesta,
            "fuentes": [
                {"id": r.chunk_id, "score": r.score}
                for r in relevantes
            ],
        }
```

Anthropic demostro que combinar chunking contextual con re-ranking redujo fallos de retrieval en 67% [Anthropic, 2024]. Esa combinacion -- contexto en los chunks + re-ranking despues del retrieval -- es una de las mejoras con mejor relacion costo/beneficio.

### Query decomposition: divide y venceras

Para preguntas complejas que requieren informacion de multiples fuentes, descomponer la query en sub-queries puede mejorar dramaticamente el recall:

```python
class DescomponedorDeQueries:
    """Descompone preguntas complejas en sub-queries mas especificas."""

    def __init__(self, cliente_llm):
        self.llm = cliente_llm

    def descomponer(self, pregunta: str) -> list[str]:
        """Descompone una pregunta compleja en sub-queries."""
        prompt = (
            f"Descompón la siguiente pregunta en 2-4 sub-preguntas "
            f"más específicas que, juntas, permitan responder la "
            f"pregunta original. Si la pregunta ya es simple, "
            f"devuélvela tal cual.\n\n"
            f"Pregunta: {pregunta}\n\n"
            f"Sub-preguntas (una por línea):"
        )

        respuesta = self.llm.completar(prompt, max_tokens=200)
        sub_queries = [
            q.strip().lstrip("- ").lstrip("1234567890. ")
            for q in respuesta.strip().split("\n")
            if q.strip()
        ]

        return sub_queries if sub_queries else [pregunta]


# Uso
descomponedor = DescomponedorDeQueries(llm)
sub_queries = descomponedor.descomponer(
    "¿Cómo se comparan los costos y el rendimiento de "
    "PostgreSQL vs Qdrant para RAG con 5 millones de documentos?"
)
# Sub-queries generadas:
# 1. "¿Cuánto cuesta operar PostgreSQL con pgvector para 5M vectores?"
# 2. "¿Cuánto cuesta operar Qdrant para 5M vectores?"
# 3. "¿Cuál es el rendimiento (latencia, throughput) de pgvector con 5M vectores?"
# 4. "¿Cuál es el rendimiento de Qdrant con 5M vectores?"
```

---

## 9.6 RAG como herramienta del agente

En capitulos anteriores construimos agentes con el patron ReAct (Capitulo 3). La integracion mas natural de RAG con agentes es como una **herramienta** que el agente decide cuando usar. Esto transforma RAG de un pipeline rigido a un componente flexible que el agente invoca cuando necesita informacion.

```python
from dataclasses import dataclass
from typing import Any


@dataclass
class Herramienta:
    nombre: str
    descripcion: str
    ejecutar: Any  # Callable


class HerramientaRAG:
    """RAG como herramienta para un agente ReAct."""

    def __init__(self, pipeline_rag: PipelineRAG):
        self.rag = pipeline_rag

    def como_herramienta(self) -> Herramienta:
        return Herramienta(
            nombre="buscar_conocimiento",
            descripcion=(
                "Busca información en la base de conocimiento interna. "
                "Úsala cuando necesites datos específicos sobre políticas, "
                "productos, procedimientos o cualquier información que no "
                "tengas en tu conocimiento base. Input: la pregunta o "
                "tema a buscar."
            ),
            ejecutar=self._buscar,
        )

    async def _buscar(self, query: str) -> str:
        resultado = await self.rag.responder(query)

        if resultado["confianza"] < 0.3:
            return (
                "No encontré información suficientemente relevante. "
                "Considera reformular la búsqueda o indicar que no "
                "tienes la información."
            )

        fuentes = "\n".join(
            f"- [{f['chunk_id']}] (score: {f['score']:.2f})"
            for f in resultado["fuentes"]
        )
        return (
            f"Información encontrada (confianza: "
            f"{resultado['confianza']:.2f}):\n\n"
            f"{resultado['respuesta']}\n\n"
            f"Fuentes consultadas:\n{fuentes}"
        )
```

Esto crea un patron llamado **Agentic RAG**: el agente decide autonomamente cuando hacer retrieval, que buscar, y si la informacion recuperada es suficiente. Es mas flexible que un pipeline RAG rigido porque el agente puede:

1. Decidir que **no necesita** buscar (ya tiene la informacion).
2. **Reformular** la query si los primeros resultados no son satisfactorios.
3. Hacer **multiples busquedas** para preguntas complejas.
4. **Combinar** informacion de RAG con su conocimiento base.

---

## 9.7 Cuando RAG NO es la respuesta

RAG no es una bala de plata. Hay escenarios donde no es la mejor opcion:

**Cuando los datos caben en el contexto y el costo es aceptable.** Si tu base de conocimiento son 50 paginas de documentacion y tu agente tiene una ventana de 200K tokens, simplemente mete todo en el contexto. Es mas simple, mas determinista y evita los falsos negativos del retrieval.

**Cuando necesitas razonamiento sobre la totalidad de los datos.** "Cual es la tendencia de ventas de los ultimos 12 meses?" requiere agregar datos, no recuperar fragmentos. Aqui necesitas acceso a una base de datos con SQL, no RAG.

**Cuando los datos son altamente estructurados.** Tablas, bases de datos relacionales, APIs con endpoints especificos. RAG esta disenado para texto no estructurado o semi-estructurado. Para datos estructurados, una herramienta de consulta directa (SQL, API) es mas precisa.

**Cuando la latencia es critica.** Un pipeline RAG agrega 200-500ms de latencia (embedding de la query + busqueda vectorial + generacion). Si tu aplicacion necesita respuestas en menos de 1 segundo incluyendo la generacion, RAG puede ser un cuello de botella.

**Cuando los datos cambian minuto a minuto.** RAG requiere indexacion. Si tus datos cambian constantemente (precios en tiempo real, inventario), la latencia de indexacion puede hacer que las respuestas esten desactualizadas. Considera una herramienta de consulta en tiempo real en lugar de RAG.

### La tabla de decision

| Escenario | RAG es buena opcion? | Alternativa |
|-----------|---------------------|-------------|
| Documentacion interna (100+ paginas) | Si | -- |
| Base de conocimiento pequeña (<50 paginas) | Quizas | Context stuffing |
| Datos estructurados (BD relacional) | No | SQL / API directa |
| Datos en tiempo real | No | Consulta en vivo |
| Preguntas de agregacion (totales, promedios) | No | Analytics / SQL |
| Multiples documentos heterogeneos | Si | -- |
| Corpus que crece con el tiempo | Si | -- |

---

## 9.8 Costos que se ignoran: indexacion, actualizacion y mantenimiento

El costo de mantener un sistema RAG no es solo la API del LLM. Estos son los costos operacionales que se subestiman sistematicamente:

**Indexacion inicial**: Procesar un corpus de 1 millon de documentos con embeddings cuesta entre $10 y $65 dependiendo del modelo (ver la tabla de MODELOS_EMBEDDINGS en la seccion 9.2). Pero el costo de computo para chunking, limpieza y procesamiento puede ser comparable.

**Re-indexacion**: Cuando cambias el modelo de embeddings (porque salio uno mejor, porque necesitas mas dimensiones, porque el proveedor descontinuo el modelo actual), tienes que re-indexar **todo**. Esto no es trivial para corpus grandes.

**Mantenimiento del indice**: Los indices HNSW consumen RAM de forma proporcional al numero de vectores. Agregar, eliminar y actualizar documentos requiere reconstruir partes del indice.

**Evaluacion continua**: Como vimos en la seccion 9.4, necesitas un pipeline de evaluacion que corra periodicamente para detectar degradacion en la calidad del retrieval.

```python
@dataclass
class CostosRAG:
    """Calcula los costos operacionales de un sistema RAG."""
    num_documentos: int
    tokens_promedio_por_doc: int
    modelo_embeddings: ConfiguracionEmbeddings
    consultas_por_dia: int
    costo_llm_por_consulta: float

    @property
    def costo_indexacion_usd(self) -> float:
        total_tokens = self.num_documentos * self.tokens_promedio_por_doc
        return self.modelo_embeddings.costo_indexacion(total_tokens)

    @property
    def ram_requerida_gb(self) -> float:
        return self.modelo_embeddings.ram_indice_hnsw(self.num_documentos)

    @property
    def costo_mensual_consultas_usd(self) -> float:
        # Costo de embedding de queries + costo de generacion LLM
        costo_embedding_queries = (
            self.consultas_por_dia
            * 30
            * 100  # ~100 tokens por query
            / 1_000_000
            * self.modelo_embeddings.costo_por_millon_tokens
        )
        costo_generacion = (
            self.consultas_por_dia * 30 * self.costo_llm_por_consulta
        )
        return costo_embedding_queries + costo_generacion

    def resumen(self) -> str:
        return (
            f"--- Costos RAG ---\n"
            f"Documentos: {self.num_documentos:,}\n"
            f"Indexación (una vez): ${self.costo_indexacion_usd:.2f}\n"
            f"RAM para índice: {self.ram_requerida_gb:.1f} GB\n"
            f"Costo mensual consultas: "
            f"${self.costo_mensual_consultas_usd:.2f}\n"
        )


# Ejemplo
costos = CostosRAG(
    num_documentos=500_000,
    tokens_promedio_por_doc=500,
    modelo_embeddings=MODELOS_EMBEDDINGS["text-embedding-3-small"],
    consultas_por_dia=1000,
    costo_llm_por_consulta=0.03,
)
print(costos.resumen())
# --- Costos RAG ---
# Documentos: 500,000
# Indexación (una vez): $5.00
# RAM para índice: 4.3 GB
# Costo mensual consultas: $900.18
```

---

## 9.9 Decisiones arquitectonicas: la guia practica

### Empieza simple, complejiza con evidencia

La arquitectura RAG recomendada para empezar es:

1. **Chunking**: Splitter recursivo, 512 tokens, 10% overlap.
2. **Embeddings**: text-embedding-3-small (o equivalente de tu proveedor).
3. **Store**: PostgreSQL + pgvector.
4. **Retrieval**: Busqueda vectorial basica, top 5.
5. **Generacion**: Tu LLM preferido con prompt que instruya fidelidad al contexto.

Esto te toma de cero a un sistema funcional en un dia. Luego mide con RAGAS y solo agrega complejidad cuando los datos lo justifiquen:

| Problema detectado | Solucion | Complejidad |
|-------------------|----------|-------------|
| Bajo recall: no encuentra documentos relevantes | Busqueda hibrida (agregar BM25) | Media |
| Baja precision: recupera muchos irrelevantes | Re-ranking con cross-encoder | Media |
| Preguntas complejas fallan | Query decomposition | Media |
| Chunks pierden contexto | Chunking contextual | Media-Alta |
| Escala insuficiente (>10M docs) | Migrar a Qdrant/Weaviate | Alta |

### El pipeline de evaluacion es mas importante que la arquitectura

Sin metricas, no puedes saber si un cambio mejora o empeora tu sistema. El orden correcto es:

1. Implementar RAG basico.
2. Construir pipeline de evaluacion con RAGAS.
3. Medir baseline.
4. Iterar con cambios medidos.

**Nunca** implementes re-ranking, busqueda hibrida o chunking contextual "porque es mejor practica". Implementalo porque tus metricas mostraron que tu recall o tu precision son insuficientes, y mide el impacto despues de cada cambio.

---

## Takeaway del capitulo

RAG ha madurado. Las soluciones simples funcionan, PostgreSQL es una opcion viable para la mayoria de los casos, y la complejidad debe justificarse con datos. Como en todo el desarrollo de software, la simplicidad es una virtud.

Los puntos clave:

1. **El 80% de los problemas son de retrieval.** Si tu RAG genera malas respuestas, primero investiga que esta recuperando. Mejora el retrieval antes de tocar la generacion.
2. **El chunking simple funciona.** Un splitter recursivo de 512 tokens con overlap es suficiente para empezar. Solo complejiza con evidencia.
3. **Mide antes de optimizar.** RAGAS y metricas de retrieval (Precision@k, Recall@k, NDCG) son tu brujula. Sin metricas, estas adivinando.
4. **Hybrid search + re-ranking** es la mejora con mejor relacion costo/beneficio cuando el retrieval basico no es suficiente.
5. **RAG no siempre es la respuesta.** Para datos estructurados usa SQL, para datos en tiempo real usa consultas en vivo, para bases de conocimiento pequenas considera context stuffing.
6. **Los costos operacionales son reales.** RAM para indices, re-indexacion al cambiar modelos, evaluacion continua. Calculalos antes de comprometerte con una arquitectura.

La paradoja de la simplicidad se resume asi: despues de explorar docenas de arquitecturas sofisticadas, la industria descubrio que Naive RAG + buena calidad de datos + evaluacion sistematica produce resultados que compiten con pipelines diez veces mas complejos. La complejidad no es un merito; la efectividad si.
