# Voice Papers

Convierte artículos académicos y páginas web en guiones educativos de audio usando IA multi-agente.

## Características

- **Extracción de contenido**: Soporta PDFs y artículos web
- **IA Multi-agente**: Diferentes perspectivas para análisis completo
- **Síntesis de voz**: Integración con ElevenLabs y Cartesia
- **Niveles técnicos**: Simple, accesible, o técnico
- **Múltiples idiomas**: Español, inglés y otros idiomas soportados
- **Modos de conversación**: Original (4 tareas) o mejorado (7 tareas con conversaciones dinámicas)
- **Tonos de conversación**: Académico, casual, humorístico, o juguetón
- **Agentes dinámicos**: Detección automática de contenido con agentes especializados
- **Separación de roles**: Agentes de conversación vs. agentes de post-producción

## Arquitectura de Agentes

### 🔄 **Flujo de Trabajo**
```
FASE 1: CONVERSACIÓN TÉCNICA SERIA
├── Agentes de conversación analizan y discuten
├── Múltiples rondas de intercambio de ideas
├── Conversaciones dinámicas entre especialistas
└── Generación de insights técnicos ricos

FASE 2: POST-PRODUCCIÓN SECUENCIAL
├── 🎭 Comedy Communicator: Añade humor al contenido técnico (opcional)
├── 📝 Educational Writer: Procesa TODAS las conversaciones → script educativo
├── 🎙️ Voice Director: Optimiza script → versión final para locución
└── Script final listo para locución
```

**¿Por qué esta separación?**
- **Conversaciones más naturales**: Los especialistas conversan SIN interferencia de roles de producción
- **Mejor calidad técnica**: Educational Writer tiene acceso a TODO el contenido conversacional
- **Humor más efectivo**: Comedy Communicator puede revisar TODO y añadir humor estratégicamente
- **Roles claros**: Cada agente hace lo que mejor sabe hacer
- **Evita confusión**: Los editores no participan en la filmación 🎬

## Tonos de Conversación

### 🎓 **Académico** (`--tone academic`) - **PREDETERMINADO**
- Tono serio y erudito
- Lenguaje científico preciso
- Enfoque en rigor intelectual y evidencia
- Estilo profesional y autoritativo

### ☕ **Casual** (`--tone casual`)
- Lenguaje relajado y conversacional
- Como explicar a un amigo inteligente
- Ejemplos cotidianos y analogías accesibles
- Evita formalidad académica excesiva

### 😄 **Humorístico** (`--tone humorous`)
- Humor apropiado y respetuoso
- Analogías divertidas y observaciones ingeniosas
- Estilo de comunicadores como Neil deGrasse Tyson
- Mantiene rigor científico con entretenimiento
- **Añade agente "Comedy Communicator" 🎭**

### 🎈 **Juguetón** (`--tone playful`)
- Enfoque ligero y entusiasta
- Metáforas creativas y escenarios imaginativos
- Sentido de asombro y emoción
- Experimentos mentales y preguntas "¿qué pasaría si?"
- **Añade agente "Comedy Communicator" 🎭**

## Agente Especial de Humor

### 🎭 **Comedy Communicator** (añadido automáticamente con tonos `humorous` y `playful`)
- **Objetivo**: Añadir humor apropiado y ingenio para hacer el contenido más atractivo
- **Especialidad**: Combina rigor científico con entretenimiento inteligente
- **Estilo**: Piensa en Neil deGrasse Tyson meets stand-up comedy
- **Función**: Uso de analogías, observaciones ingeniosas y humor ligero
- **Trabaja en**: Fase de post-producción - revisa TODO el contenido técnico y añade humor estratégicamente
- **Ventaja**: Puede ver toda la conversación completa y añadir humor coherente, no chistes dispersos

## Modos de Conversación

### Modo Original (`--conversation-mode original`)
El flujo clásico ahora con separación de post-producción:
1. **Análisis inicial** - Conversación técnica entre especialistas
2. **Discusión general** - Conversación técnica profunda 
3. **Comedy enhancement** - Añade humor (opcional, solo con tonos `humorous`/`playful`)
4. **Escritura educativa** - Se transforma en script educativo
5. **Dirección de voz** - Optimización final para locución

### Modo Mejorado (`--conversation-mode enhanced`) - **PREDETERMINADO**
Flujo extendido con separación clara de conversación y post-producción:

**FASE 1: CONVERSACIÓN TÉCNICA SERIA**
1. **Análisis inicial** - Análisis desde múltiples perspectivas técnicas
2. **Deep dive especializado** - Expertos en dominios específicos profundizan
3. **Ronda de preguntas cruzadas** - Los especialistas se hacen preguntas específicas entre sí
4. **Debate de perspectivas contrarias** - Discusión estructurada con argumentos técnicos
5. **Síntesis colaborativa** - Los especialistas construyen entendimiento conjunto
6. **Discusión final técnica** - Síntesis de todas las conversaciones técnicas previas

**FASE 2: POST-PRODUCCIÓN SECUENCIAL**
7. **Comedy enhancement** - Añade humor apropiado (opcional, solo con tonos `humorous`/`playful`)
8. **Escritura educativa** - Script incorporando toda la riqueza conversacional
9. **Dirección de voz** - Optimización final para locución

El modo mejorado produce conversaciones más dinámicas, naturales y profundas entre los agentes especializados, seguido de una post-producción profesional.

## Instalación

```bash
pip install -e .
```

## Uso

### Comando básico con tono
```bash
voice-papers paper.pdf --tone humorous
```

### Con todas las opciones
```bash
voice-papers paper.pdf \
  --conversation-mode enhanced \
  --tone playful \
  --duration 10 \
  --technical-level accessible
```

### Ejemplos de tonos
```bash
# Estilo académico serio
voice-papers paper.pdf --tone academic

# Conversación relajada 
voice-papers paper.pdf --tone casual

# Con humor apropiado
voice-papers paper.pdf --tone humorous

# Juguetón y entusiasta
voice-papers paper.pdf --tone playful
```

## Configuración

Crea un archivo `.env` con tus claves API:

```env
OPENAI_API_KEY=tu_clave_openai
ELEVENLABS_API_KEY=tu_clave_elevenlabs
CARTESIA_API_KEY=tu_clave_cartesia  # Opcional
```

## Estructura de Salida

```
projects/
└── tu_proyecto/
    ├── discussion/
    │   ├── crew_structure.json     # Estructura del crew
    │   ├── final_result.txt        # Resultado final
    │   ├── task_1_output.txt       # Análisis inicial
    │   ├── task_2_output.txt       # Deep dive especializado (modo enhanced)
    │   ├── task_3_output.txt       # Preguntas cruzadas (modo enhanced)
    │   ├── task_4_output.txt       # Debate técnico (modo enhanced)
    │   ├── task_5_output.txt       # Síntesis colaborativa (modo enhanced)
    │   ├── task_6_output.txt       # Discusión final técnica
    │   ├── task_7_output.txt       # Comedy enhancement (opcional)
    │   ├── task_8_output.txt       # Escritura educativa
    │   └── task_9_output.txt       # Dirección de voz
    ├── educational_script.txt      # Script final
    ├── educational_lecture.mp3     # Audio generado
    └── extracted_text.txt          # Texto extraído del PDF
```

**Nota**: El número de tareas varía según el modo:
- **Modo original**: 3-5 tareas (sin/con humor)
- **Modo enhanced**: 7-9 tareas (sin/con humor)

## Agentes del Sistema

### 💬 **Agentes de Conversación Base** (siempre presentes en análisis y discusiones)
- **Coordinador**: Modera y coordina la discusión
- **Revisor Científico**: Evalúa metodología y rigor
- **Pensador Crítico**: Cuestiona y desafía ideas

### 🎬 **Agentes de Post-Producción** (siempre presentes, trabajan al final)
- **Comedy Communicator**: Añade humor apropiado al contenido técnico (opcional, con tonos `humorous` y `playful`)
- **Escritor Educativo**: Transforma conversaciones en script educativo
- **Director de Voz**: Optimiza script para locución perfecta

### 🎯 **Agentes Especializados** (se añaden dinámicamente según el contenido)

#### 🤖 **Inteligencia Artificial** (detectado automáticamente)
- **Investigador de IA**: Perspectiva técnica y metodológica
- **Filósofo de IA**: Implicaciones éticas y filosóficas
- **Pesimista de IA**: Riesgos y preocupaciones de seguridad
- **Entusiasta de IA**: Potencial positivo y aplicaciones
- **Novato en IA**: Preguntas básicas y perspectiva de principiante

#### 🏥 **Medicina y Biología** (detectado automáticamente)
- **Investigador Médico**: Metodología clínica y medicina basada en evidencia
- **Bioético**: Implicaciones éticas de la investigación médica
- **Clínico**: Perspectiva práctica y aplicaciones en atención al paciente
- **Defensor del Paciente**: Representa perspectivas y preocupaciones de pacientes

#### 🔬 **Física y Química** (detectado automáticamente)
- **Físico Teórico**: Marcos teóricos y modelos matemáticos
- **Científico Experimental**: Diseño experimental y metodología
- **Comunicador Científico**: Traducción de conceptos complejos para audiencias generales
- **Escéptico Científico**: Cuestiona afirmaciones extraordinarias y demanda evidencia rigurosa

#### 🧠 **Psicología y Neurociencia** (detectado automáticamente)
- **Científico Cognitivo**: Procesos cognitivos y mecanismos cerebrales
- **Psicólogo Clínico**: Aplicaciones prácticas para salud mental
- **Neurocientífico**: Datos de neuroimagen y mecanismos neurales
- **Economista Conductual**: Conexión entre hallazgos psicológicos y toma de decisiones

#### 💰 **Economía y Finanzas** (detectado automáticamente)
- **Economista**: Teoría económica y evidencia empírica
- **Analista Financiero**: Implicaciones de mercado y perspectivas de inversión
- **Asesor de Políticas**: Implicaciones políticas y aplicaciones gubernamentales
- **Defensor del Consumidor**: Representa a personas afectadas por políticas económicas

#### 💻 **Tecnología e Ingeniería** (detectado automáticamente)
- **Ingeniero de Software**: Implementación técnica y calidad de código
- **Experto en Seguridad**: Implicaciones de seguridad y vulnerabilidades
- **Diseñador UX**: Experiencia del usuario e interacción humano-computadora
- **Emprendedor Tecnológico**: Viabilidad comercial y potencial de mercado

## Detección Automática de Contenido

El sistema detecta automáticamente el tipo de contenido usando palabras clave avanzadas:

- **IA/ML**: artificial intelligence, machine learning, neural network, transformer, etc.
- **Medicina**: medicine, clinical, therapy, diagnosis, genome, virus, vaccine, etc.
- **Ciencias**: physics, quantum, chemistry, molecule, nuclear, particle, etc.
- **Psicología**: psychology, neuroscience, cognitive, brain, behavior, fMRI, etc.
- **Economía**: economics, finance, market, GDP, investment, cryptocurrency, etc.
- **Tecnología**: engineering, software, algorithm, cybersecurity, cloud, etc.

Cuando se detecta contenido especializado, se añaden automáticamente **4-5 agentes especializados** a los **3 agentes de conversación base**, creando equipos de **7-8 agentes conversacionales** para discusiones más ricas y específicas al dominio.

Con tonos `humorous` o `playful`, se añade además el **Comedy Communicator** en post-producción.

**Total de agentes en el sistema**:
- **3 agentes de conversación base** (siempre)
- **4-5 agentes especializados** (según contenido detectado)  
- **2 agentes de post-producción base** (Educational Writer, Voice Director)
- **1 agente de humor** (Comedy Communicator, opcional)

**Resultado**: **9-11 agentes** total trabajando en el proyecto.

## Ejemplos

### Procesar PDF con humor
```bash
voice-papers mi_paper.pdf \
  --tone humorous \
  --conversation-mode enhanced \
  --duration 15
```

### Solo generar script casual
```bash
voice-papers https://example.com/article.html \
  --script-only \
  --tone casual \
  --conversation-mode enhanced
```

### Tono juguetón para contenido técnico
```bash
voice-papers paper_tecnico.pdf \
  --tone playful \
  --technical-level accessible \
  --duration 20
``` 