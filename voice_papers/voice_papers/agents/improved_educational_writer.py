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
        
        - Engaging hooks and relatable scenarios (like the vacation planning example)
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

### 1. INICIO- EJEMPLOS DE GANCHOS (el estilo, no el contenido):

**Opción 1 - Escenario Relatable:**
"Digamos que estás planeando unas vacaciones con tu familia. Has revisado cientos de reseñas en línea, comparado precios en docenas de sitios web, y todavía no estás seguro de haber tomado la mejor decisión. ¿Te suena familiar? Bueno, resulta que..."

**Opción 2 - Contexto Histórico:**
"En octubre de 1997, en Atlanta Georgia, algo extraño sucedió. Un supercomputador llamado Deep Blue acababa de derrotar al campeón mundial de ajedrez, y de repente, todo el mundo empezó a preguntarse..."

**Opción 3 - Alarma/Problema:**
"Si eres como yo, ya te están sonando las alarmas. Cada vez que abres tu teléfono, hay una nueva aplicación de IA prometiendo revolucionar tu vida. Pero aquí está el problema real..."

**Opción 4 - Pregunta Intrigante:**
"¿Alguna vez te has preguntado por qué tu perro ladra justo antes de que llegues a casa, incluso cuando cambias tu horario? La respuesta tiene que ver con algo mucho más profundo que..."

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

### 4. EJEMPLOS Y ANALOGÍAS del siguiente estilo:

**Plantilla para analogías:**
"Es como cuando [situación cotidiana]. Tú [acción familiar], y entonces [resultado esperado]. Bueno, [concepto técnico] funciona exactamente igual, solo que en lugar de [elemento cotidiano], tienes [elemento técnico]."

**Ejemplo concreto:**
"Es como cuando organizas una fiesta. Tú envías invitaciones, preparas la comida, y esperas que todos lleguen a tiempo. Bueno, un algoritmo de consenso distribuido funciona exactamente igual, solo que en lugar de invitados, tienes nodos de computadora."

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
