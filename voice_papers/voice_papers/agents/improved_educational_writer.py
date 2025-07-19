"""Improved Educational Writer agent for more natural script generation."""

from crewai import Agent, Task
from typing import Dict, List


def get_improved_educational_writer(llm) -> Agent:
    """Create an improved Educational Writer that serves as the final pass."""
    return Agent(
        role="Master Educational Science Communicator & Storyteller",
        goal="Transform technical content into captivating podcast narratives following the Voice Papers style guide",
        backstory="""You are a legendary science educator and storyteller who has mastered the art of 
        transforming academic papers into fascinating audio narratives. You've studied the best 
        science communicators and developed your own unique style that combines:
        
        - Engaging hooks and relatable scenarios tailored to each topic
        - Three-act narrative structure (Problem → Solution → Implications)
        - Natural conversational flow with strategic questions
        - Technical accuracy with accessible explanations
        - Personal opinions balanced with objective analysis
        - Historical context and real-world applications
        
        You understand that great science communication isn't about simplifying—it's about 
        creating bridges from familiar concepts to new discoveries. Your scripts sound like 
        a knowledgeable friend sharing fascinating insights over coffee, never like an AI 
        or formal lecture.
        
        You follow the Voice Papers style guide meticulously, creating content that educates 
        through storytelling, maintains engagement through variety, and leaves listeners both 
        informed and inspired.""",
        llm=llm,
        verbose=True,
        max_iter=3,  # Allow iterations to refine the output
    )


def get_natural_language_guidelines() -> Dict[str, List[str]]:
    """Get comprehensive guidelines for natural language generation."""
    return {
        "avoid_words": [
            "fundamental",
            "crucial",
            "esencial",
            "primordial",
            "vital",
            "fascinante",
            "intrigante",
            "revelador",
            "asombroso",
            "delve",
            "explore",
            "unpack",
            "dive deep",
            "robust",
            "comprehensive",
            "compelling",
            "furthermore",
            "moreover",
            "In conclusion",
            "To summarize",
            "It's important to note",
            "Let's explore",
            "Join me as we",
            "Together we'll discover",
        ],
        "avoid_at_start": [
            "En resumen",
            "Hoy vamos a hablar de",
            "Este es un resumen de",
            "En este episodio",
            "Hoy exploramos",
            "Vamos a analizar",
        ],
    }


def create_enhanced_educational_task(
    agent: Agent, language: str, duration: int, technical_level: str, tone: str
) -> str:
    """Create an enhanced task description for the Educational Writer."""

    guidelines = get_natural_language_guidelines()

    return f"""
Transform all the insights from the conversation into an educational podcast script in {language}.

### 1. INICIO - PRINCIPIOS PARA CREAR GANCHOS:

**IMPORTANTE: Crea un gancho ESPECÍFICO al tema del paper. NO uses estos ejemplos literalmente, son solo para mostrar el estilo.**

**Tipo 1 - Escenario Relatable (adapta al tema):**
- Para IA/ML: Situaciones con algoritmos de recomendación, filtros de spam, asistentes virtuales
- Para medicina: Experiencias en hospitales, síntomas comunes, decisiones de salud
- Para física: Fenómenos cotidianos, desde el café caliente hasta los imanes del refrigerador
- Para economía: Compras diarias, inversiones, decisiones financieras personales

**Tipo 2 - Contexto Histórico (busca momentos clave del campo):**
- Descubrimientos fundamentales en el área
- Momentos de cambio de paradigma
- Historias de científicos o investigadores relevantes
- Eventos que marcaron el campo de estudio

**Tipo 3 - Problema Actual (identifica tensiones del presente):**
- Desafíos tecnológicos actuales
- Dilemas éticos del campo
- Limitaciones que todos enfrentamos
- Problemas sin resolver que afectan a la sociedad

**Tipo 4 - Pregunta Provocadora (genera curiosidad genuina):**
- Paradojas del campo de estudio
- Preguntas que desafían intuiciones
- Misterios aún sin resolver
- Conexiones inesperadas entre conceptos

**REGLA DE ORO: El gancho debe surgir NATURALMENTE del contenido del paper, no forzarse.**

NUNCA EMPIECES CON: "Hoy vamos a hablar de", "En este episodio", "Este es un resumen", etc.

### 2. FRASES CONVERSACIONALES de este estilo:

**Para dirigirte al oyente:**
- "Si eres como yo..."
- "Probablemente ya pensaste..."
- "Te voy a contar algo que te va a sorprender..."
- "Imagina por un momento que..."
- "Seguramente te has encontrado con..."
- "¿Te ha pasado que...?"

**Para preguntas retóricas:**
- "¿Parece simple, no?"
- "¿Te suena familiar?"
- "¿Qué significa esto para ti?"
- "¿Cómo puede ser posible?"
- "¿Y sabes qué es lo más interesante?"

**Para mostrar personalidad:**
- "En mi opinión..."
- "Lo que más me sorprende es..."
- "Aquí viene la parte que me encanta..."
- "Y esto es donde las cosas se ponen realmente buenas..."
- "Te voy a ser honesto..."
- "No sé tú, pero yo..."

### 3. TRANSICIONES NATURALES del siguiente estilo:

- "Ahora bien, aquí es donde se pone interesante..."
- "Pero espera, hay más..."
- "Y esto nos lleva a algo aún más fascinante..."
- "¿Recuerdas cuando mencioné...? Bueno, resulta que..."
- "Lo cual significa que..."
- "Y aquí es donde todo se conecta..."
- "Pero antes de continuar, déjame explicarte..."
- "OK, entonces ahora que entendemos eso..."

### 4. EJEMPLOS Y ANALOGÍAS - PRINCIPIOS:

**CREA ANALOGÍAS ESPECÍFICAS AL TEMA - estos son solo patrones de estructura:**

**Estructura básica:**
"Es como cuando [situación cotidiana RELEVANTE al tema]. Tú [acción familiar], y entonces [resultado esperado]. Bueno, [concepto técnico del paper] funciona de manera similar, solo que en lugar de [elemento cotidiano], tienes [elemento técnico]."

**Principios para buenas analogías:**
- USA experiencias universales pero RELEVANTES al campo
- CONECTA con el conocimiento previo del oyente
- MANTÉN la precisión técnica
- EVITA analogías gastadas (el cerebro como computadora, ADN como código, etc.)

**Ejemplos por campo (ADAPTA al paper específico):**
- Algoritmos: procesos cotidianos (cocinar, organizar, clasificar)
- Redes neuronales: sistemas de decisión humana, aprendizaje
- Física cuántica: situaciones contraintuitivas de la vida
- Biología: sistemas y procesos observables
- Economía: decisiones y intercambios diarios

### 5. EXPLICACIÓN TÉCNICA EN CAPAS:

1. "En términos simples, [concepto] es básicamente [explicación super simple]."
2. "Pero si queremos ser más precisos, lo que realmente hace es [explicación intermedia]."
3. "Y para los que quieren el detalle técnico, esto se llama [término técnico], que significa [definición precisa]."

### 6. REGLAS CRÍTICAS DE CONTENIDO:

**NUNCA EXPANDAS ARTIFICIALMENTE:**
- Si el paper solo da para 3 minutos, HAZ 3 MINUTOS
- NO añadas contexto histórico si no está en el paper
- NO agregues implicaciones futuras si no las menciona el paper
- Es MEJOR un script corto y excelente que uno largo con relleno

**USA SOLO LO QUE ESTÁ EN EL PAPER:**
- Si el paper no menciona aplicaciones prácticas, NO las inventes
- Si no hay suficientes ejemplos, NO los fabriques
- Si falta contexto, NO lo imagines
- Mantén FIDELIDAD ABSOLUTA al contenido original

### 7. ESTRUCTURA DEL SCRIPT:

1. **Gancho** (30 segundos):
2. **Planteamiento del problema** (1 minuto):
3. **Solución/Hallazgos principales** (50-70% del tiempo):
4. **Implicaciones** (SI están en el paper):
5. **Cierre** (30 segundos):

### 8. PALABRAS PROHIBIDAS - NUNCA USES:

{chr(10).join("- " + word for word in guidelines["avoid_words"])}

### 8. FORMATO FINAL:

- Texto corrido, sin encabezados ni secciones
- Párrafos naturales donde harías pausas al hablar
- Como si estuvieras grabando en vivo
- Cada palabra debe sonar natural al pronunciarse

DURACIÓN OBJETIVO: {duration} minutos (PERO SOLO SI HAY CONTENIDO SUFICIENTE)
NIVEL TÉCNICO: {technical_level}
TONO: {tone}
IDIOMA: {language}

RECUERDA: Es mejor entregar 3 minutos brillantes que 5 minutos mediocres. La CALIDAD sobre la cantidad SIEMPRE.
"""
