"""Task prompts for Voice Papers agents.

This module centralizes all task-specific prompts and instructions
that are given to agents when creating tasks.
"""

from typing import Dict, Any, Optional
from .constraints import Constraints
from .style_guides import StyleGuides


class TaskPrompts:
    """Centralized storage for task-specific prompts."""
    
    # ============== EDUCATIONAL WRITING TASKS ==============
    
    @staticmethod
    def educational_writing_task(
        title: str,
        content: str,
        language: str = "Spanish",
        duration: int = 5,
        focus: str = "explanatory",
        tone: str = "academic"
    ) -> str:
        """Create an educational writing task prompt.
        
        Args:
            title: Title/topic of the content
            content: The content to transform
            language: Target language
            duration: Target duration in minutes
            focus: Focus mode (explanatory, technical, critical, practical)
            tone: Desired tone (academic, casual, professional)
            
        Returns:
            Complete task prompt
        """
        # Get constraints and style guides
        avoided_words = Constraints.get_avoided_words("educational", language)
        style_guide = StyleGuides.combine_styles("voice_papers", focus, language, tone)
        
        prompt = f"""
Transform this text content into an engaging educational script.

Title/Topic: {title}

Content to transform:
{content}

---

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

NUNCA EMPIECES CON: {', '.join([f'"{w}"' for w in ["Hoy vamos a hablar de", "En este episodio", "Este es un resumen"]])}

### 2. ESTRUCTURA DEL SCRIPT:

1. **Gancho** (30 segundos): Específico al tema
2. **Planteamiento del problema** (1 minuto): Contexto necesario
3. **Desarrollo principal** (50-70% del tiempo): Contenido core
4. **Implicaciones** (SI están en el paper): Aplicaciones reales
5. **Cierre** (30 segundos): Reflexión final

### 3. PALABRAS PROHIBIDAS - NUNCA USES:
{', '.join(avoided_words)}

### 4. FORMATO FINAL:
- Texto corrido, sin encabezados ni secciones
- Párrafos naturales donde harías pausas al hablar
- Como si estuvieras grabando en vivo
- Cada palabra debe sonar natural al pronunciarse

DURACIÓN OBJETIVO: {duration} minutos (PERO SOLO SI HAY CONTENIDO SUFICIENTE)
NIVEL TÉCNICO: {focus}
TONO: {tone}
IDIOMA: {language}

RECUERDA: Es mejor entregar 3 minutos brillantes que {duration} minutos mediocres. La CALIDAD sobre la cantidad SIEMPRE.
"""
        return prompt
    
    # ============== TECHNICAL EXTRACTION TASKS ==============
    
    @staticmethod
    def technical_extraction_task(
        title: str,
        content: str,
        language: str = "Spanish",
        target_length: str = "comprehensive"
    ) -> str:
        """Create a technical extraction task prompt.
        
        Args:
            title: Title of the content
            content: Content to extract from
            language: Target language
            target_length: Length target (comprehensive, concise, brief)
            
        Returns:
            Complete task prompt
        """
        technical_rules = Constraints.get_rules("technical")
        
        prompt = f"""
Extract and present ALL factual knowledge from the following content titled "{title}".

CONTENT TO EXTRACT FROM:
{content}

YOUR MISSION: Extract EVERY piece of objective knowledge - facts, concepts, declarations, examples, explanations.

WHAT TO EXTRACT:

1. **FACTS AND DATA**:
   - All numbers, statistics, percentages
   - Dates, times, durations
   - Measurements and quantities
   - Names of people, places, organizations
   - Historical facts
   
2. **CONCEPTS AND DEFINITIONS**:
   - What things ARE (definitions)
   - How things WORK (mechanisms)
   - Types and categories
   - Components and structures
   
3. **DECLARATIONS AND STATEMENTS**:
   - Direct quotes (with attribution)
   - Claims made (attribute to source: "The author claims...")
   - Positions stated (attribute: "According to X...")
   - Opinions expressed (clearly marked: "In the author's opinion...")
   
4. **EXAMPLES AND CASES**:
   - Specific instances mentioned
   - Case studies described
   - Scenarios presented
   - Applications shown
   
5. **PROCESSES AND METHODS**:
   - Steps described
   - Procedures outlined
   - Techniques explained
   - Approaches detailed

CRITICAL DISTINCTION - FACTS VS OPINIONS:

FACTS (present directly):
- "The system processes 1000 requests per second"
- "The study included 500 participants"
- "The algorithm has O(n log n) complexity"

OPINIONS/CLAIMS (always attribute):
- "According to the author, this is the future of computing"
- "The researchers believe this will transform the industry"
- "Smith argues that current methods are inadequate"

ATTRIBUTION PHRASES TO USE:
{', '.join(technical_rules.get('attribution_phrases', []))}

TARGET LENGTH: {target_length}
LANGUAGE: {language}

Remember: Extract knowledge, attribute opinions, present facts directly.
"""
        return prompt
    
    # ============== SYNTHESIS TASKS ==============
    
    @staticmethod
    def synthesis_task(
        title: str,
        sections: list,
        synthesis_type: str = "comprehensive"
    ) -> str:
        """Create a synthesis task prompt.
        
        Args:
            title: Document title
            sections: List of content sections to synthesize
            synthesis_type: Type of synthesis (comprehensive, concise, tldr)
            
        Returns:
            Complete synthesis task prompt
        """
        if synthesis_type == "tldr":
            max_bullets = 5
            instruction = "Create a TLDR with maximum 5 bullet points"
        elif synthesis_type == "concise":
            max_bullets = 10
            instruction = "Create a concise synthesis with key points"
        else:
            max_bullets = None
            instruction = "Create a comprehensive synthesis preserving all important information"
            
        prompt = f"""
Synthesize the extracted content from "{title}".

SECTIONS TO SYNTHESIZE:
{chr(10).join([f"Section {i+1}: {section[:200]}..." for i, section in enumerate(sections)])}

{instruction}

REQUIREMENTS:
1. Preserve ALL important information
2. Organize hierarchically
3. Maintain technical accuracy
4. Clear and coherent structure
5. No meta-language ("This document discusses...")
6. Present the actual content, not descriptions of it
"""
        
        if max_bullets:
            prompt += f"\n\nMaximum {max_bullets} bullet points for main insights."
            
        return prompt
    
    # ============== CONVERSATIONAL ENHANCEMENT TASKS ==============
    
    @staticmethod
    def conversational_enhancement_task(
        content: str,
        language: str = "Spanish",
        enhancement_level: str = "light"
    ) -> str:
        """Create a conversational enhancement task.
        
        Args:
            content: Content to enhance
            language: Target language
            enhancement_level: Level of enhancement (light, moderate, full)
            
        Returns:
            Complete enhancement task prompt
        """
        if enhancement_level == "light":
            instruction = "Add minimal connector words and phrases for better flow"
        elif enhancement_level == "moderate":
            instruction = "Add natural transitions and conversational elements"
        else:
            instruction = "Transform into fully conversational narrative"
            
        prompt = f"""
Enhance this content for natural speech delivery in {language}.

CONTENT:
{content}

ENHANCEMENT LEVEL: {enhancement_level}
INSTRUCTION: {instruction}

RULES:
1. Preserve ALL original meaning
2. Maintain factual accuracy
3. Add natural speech patterns
4. Improve flow for audio delivery
5. Keep changes minimal and purposeful

ALLOWED ADDITIONS:
- Connector words: "Additionally", "However", "In fact"
- Natural transitions: "It turns out", "As it happens"
- Clarifying phrases: "In other words", "That is to say"

MAINTAIN:
- Technical precision
- Original structure
- Key terminology
- Factual statements

LANGUAGE: {language}
"""
        return prompt
    
    # ============== TTS OPTIMIZATION TASKS ==============
    
    @staticmethod
    def tts_optimization_task(
        script: str,
        language: str = "Spanish",
        voice_provider: str = "elevenlabs"
    ) -> str:
        """Create a TTS optimization task.
        
        Args:
            script: Script to optimize
            language: Target language
            voice_provider: TTS provider (elevenlabs, cartesia)
            
        Returns:
            Complete TTS optimization task prompt
        """
        prompt = f"""
Optimize this educational script for {voice_provider} Text-to-Speech in {language}.

SCRIPT TO OPTIMIZE:
{script}

TTS OPTIMIZATION REQUIREMENTS:

1. **PRONUNCIATION FIXES**:
   - Spell out problematic acronyms
   - Add phonetic hints for ambiguous words
   - Break up complex terms

2. **PACING ADJUSTMENTS**:
   - Add natural pause indicators
   - Break long sentences
   - Ensure breathing points

3. **CLARITY IMPROVEMENTS**:
   - Simplify tongue-twisters
   - Clarify ambiguous pronunciations
   - Smooth awkward phrasings

4. **MAINTAIN**:
   - Educational value
   - Original meaning
   - Natural flow
   - Engagement level

LANGUAGE: {language}
VOICE PROVIDER: {voice_provider}

Output the optimized script ready for TTS processing.
"""
        return prompt
    
    # ============== HELPER METHODS ==============
    
    @classmethod
    def get_task_prompt(
        cls,
        task_type: str,
        **kwargs
    ) -> str:
        """Get a task prompt by type with parameters.
        
        Args:
            task_type: Type of task (educational_writing, technical_extraction, etc.)
            **kwargs: Task-specific parameters
            
        Returns:
            Complete task prompt
            
        Raises:
            ValueError: If task_type is not recognized
        """
        task_map = {
            "educational_writing": cls.educational_writing_task,
            "technical_extraction": cls.technical_extraction_task,
            "synthesis": cls.synthesis_task,
            "conversational_enhancement": cls.conversational_enhancement_task,
            "tts_optimization": cls.tts_optimization_task
        }
        
        if task_type not in task_map:
            raise ValueError(f"Unknown task type: {task_type}")
            
        return task_map[task_type](**kwargs)