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
    
    # ============== CREW DISCUSSION TASKS ==============
    
    @staticmethod
    def initial_analysis_task(
        paper_title: str,
        paper_content: str,
        language: str,
        conversation_agents: list,
        focus: str
    ) -> str:
        """Create initial analysis task for conversation agents."""
        return f"""
            Analyze the synthesis of the paper titled "{paper_title}" and provide your perspective.
            
            Paper synthesis:
            {paper_content}
            
            CRITICAL: ONLY CONVERSATION AGENTS participate in this analysis:
            - Base agents (Coordinator, Scientific Reviewer, Critical Thinker)
            - Specialized domain agents
            
            EXCLUDED FROM ANALYSIS: Master Educational Science Communicator & Storyteller and Comedy Communicator (work in post-production)
            
            Each participating agent should:
            1. Read and understand the paper from your specific role's perspective
            2. Identify key points relevant to your expertise
            3. Prepare questions or concerns to discuss
            4. Consider the implications from your unique viewpoint
            
            SPECIALIZED AGENTS: Pay special attention to domain-specific aspects that only you can address.
            
            This should be a comprehensive TECHNICAL analysis where EVERY conversation agent contributes their specialized perspective.
            
            Language: {language}
            """
    
    @staticmethod
    def specialist_deep_dive_task(
        conversation_specialists: list,
        language: str,
        focus: str
    ) -> str:
        """Create specialist deep dive task."""
        return f"""
                    SPECIALIZED AGENTS DEEP DIVE: Domain expertise from TECHNICAL conversation agents only.
                    
                    PARTICIPATING SPECIALIZED AGENTS (technical focus):
                    {", ".join([f"- {agent.role}: {agent.goal}" for agent in conversation_specialists])}
                    
                    EXCLUDED: Comedy Communicator (works in post-production phase)
                    
                    Each specialized agent should:
                    1. Provide deep domain-specific insights about the paper
                    2. Identify methodological issues specific to your field
                    3. Highlight implications that only someone with your expertise would notice
                    4. Suggest domain-specific improvements or alternative approaches
                    5. Connect this work to other research in your specialized area
                    
                    This is YOUR moment to shine with specialized knowledge that the base agents cannot provide.
                    Focus on TECHNICAL DEPTH and DOMAIN EXPERTISE.
                    Format as a detailed specialist consultation with clear attribution to each expert.
                    
                    Language: {language}
                    """
    
    @staticmethod
    def qa_session_task(
        conversation_agents: list,
        specialized_agents: list,
        language: str,
        focus: str
    ) -> str:
        """Create Q&A session task."""
        return f"""
            Based on the initial analysis, conduct a DYNAMIC Q&A session where technical conversation agents ask each other specific questions about the paper synthesis.
            
            PARTICIPATING AGENTS (technical conversation only):
            - Base conversation agents (Coordinator, Scientific Reviewer, Critical Thinker) 
            - ALL specialized domain agents
            
            EXCLUDED FROM CONVERSATION: Master Educational Science Communicator & Storyteller and Comedy Communicator (work in post-production)
            
            Instructions for multi-agent technical conversation:
            1. ALL TECHNICAL CONVERSATION AGENTS should ask pointed questions to other agents
            2. SPECIALIZED AGENTS should ask domain-specific questions that challenge assumptions
            3. BASE AGENTS should ask specialists to clarify complex domain concepts
            4. Agents must respond to questions directed at them with detailed technical answers
            5. Follow-up questions and clarifications are encouraged
            6. Challenge each other's assumptions respectfully
            7. Build on each other's ideas and insights
            8. Create a natural back-and-forth technical dialogue
            
            SPECIALIZED AGENTS: This is crucial - ask questions only YOU would think to ask!
            
            Focus areas for technical questions:
            - Domain-specific methodological concerns
            - Interdisciplinary connections and conflicts
            - Alternative interpretations from different expert perspectives
            - Practical applications in each specialist's field
            - Potential limitations or biases from multiple viewpoints
            
            Format this as a realistic TECHNICAL conversation with clear speaker identification for ALL conversation participants.
            Keep the tone SERIOUS and TECHNICAL - humor will be added later in post-production.
            
            Language: {language}
            """
    
    @staticmethod
    def debate_task(
        conversation_agents: list,
        specialized_agents: list,
        language: str,
        focus: str
    ) -> str:
        """Create debate task."""
        return f"""
            Organize a structured technical debate where conversation agents with different viewpoints engage in deeper discussion.
            
            PARTICIPATING AGENTS (technical conversation only):
            - Base conversation agents (Coordinator, Scientific Reviewer, Critical Thinker)
            - ALL specialized domain agents  
            
            EXCLUDED FROM DEBATE: Master Educational Science Communicator & Storyteller and Comedy Communicator (work in post-production)
            
            Technical debate structure:
            1. Present the main controversial points or interpretations from the paper
            2. Have TECHNICAL CONVERSATION AGENTS take different positions and argue their cases
            3. SPECIALIZED AGENTS: Argue from your domain expertise - what would your field say?
            4. Allow for rebuttals and counter-arguments between different expert perspectives
            5. Explore edge cases and hypothetical scenarios from multiple disciplinary angles
            6. Find areas of agreement and persistent disagreements between different specialties
            7. Synthesize different viewpoints into a richer technical understanding
            
            This should feel like a real interdisciplinary TECHNICAL conference where:
            - Different specialists bring unique perspectives that sometimes conflict
            - Domain experts interrupt each other (politely) to make field-specific points
            - Ideas evolve through interaction between different areas of expertise
            - New insights emerge from cross-disciplinary exchange
            - There's intellectual tension between different specialist viewpoints
            
            SPECIALIZED AGENTS: Don't hold back - defend your field's perspective!
            
            Make it conversational and dynamic, but keep TECHNICAL FOCUS - humor will be added later.
            
            Language: {language}
            """
    
    @staticmethod
    def collaborative_synthesis_task(
        conversation_agents: list,
        specialized_agents: list,
        language: str,
        focus: str
    ) -> str:
        """Create collaborative synthesis task."""
        return f"""
            Conduct a collaborative synthesis where technical conversation agents work together to build a comprehensive understanding.
            
            PARTICIPATING AGENTS (technical conversation only):
            - Base conversation agents (Coordinator, Scientific Reviewer, Critical Thinker)
            - ALL specialized domain agents
            
            EXCLUDED FROM SYNTHESIS: Master Educational Science Communicator & Storyteller and Comedy Communicator (work in post-production)
            
            Technical collaborative process:
            1. ALL TECHNICAL CONVERSATION AGENTS contribute their key insights from the discussions
            2. SPECIALIZED AGENTS highlight unique perspectives only your field can provide
            3. Agents build on each other's contributions in real-time
            4. Identify connections between different specialist perspectives
            5. Resolve conflicting interpretations through interdisciplinary dialogue
            6. Co-create new insights that emerge from cross-domain discussion
            7. Establish consensus on the most important takeaways from ALL conversation perspectives
            
            This should be a generative TECHNICAL conversation where:
            - Ideas from one specialist spark new ideas in other specialists
            - The group intelligence exceeds individual specialist perspectives
            - Agents actively listen and respond to insights from other domains
            - The conversation flows naturally between different areas of expertise
            - New understanding emerges from interdisciplinary interaction
            - Each specialist's unique knowledge contributes to the whole
            
            SPECIALIZED AGENTS: Share insights that ONLY someone with your expertise would have!
            
            Format as natural TECHNICAL conversation with organic transitions between specialist viewpoints.
            Keep SERIOUS and FOCUSED - entertainment will be added later in post-production.
            
            Language: {language}
            """
    
    @staticmethod
    def final_discussion_task(
        conversation_agents: list,
        specialized_agents: list,
        language: str,
        focus: str
    ) -> str:
        """Create final discussion task."""
        return f"""
            Based on all previous conversations and analyses, conduct a final comprehensive technical discussion that synthesizes insights from conversation agents.
            
            PARTICIPATING AGENTS (technical conversation only):
            - Base conversation agents (Coordinator, Scientific Reviewer, Critical Thinker)
            - ALL specialized domain agents
            
            EXCLUDED: Master Educational Science Communicator & Storyteller and Comedy Communicator (they will process this output in post-production)
            
            The final technical discussion should:
            1. Synthesize insights from the Q&A, specialist deep dive, debate, and collaborative sessions
            2. Cover all major points of the paper from multiple expert perspectives
            3. Include the rich specialist perspectives developed through agent interactions
            4. Address concerns and criticisms that emerged from different domains
            5. Explore implications and applications discussed by various specialists
            6. Be comprehensive and technically rigorous for expert audiences
            7. Highlight unique insights that could ONLY come from having multiple specialist perspectives
            
            CRITICAL: This final technical discussion must incorporate:
            - Domain-specific insights from ALL specialist conversation agents
            - Cross-disciplinary connections discovered during discussions
            - Unique perspectives that emerged from interdisciplinary dialogue
            - Technical depth and rigor appropriate for expert audiences
            
            This is the FINAL technical conversation output that will be handed to the post-production team.
            Make it comprehensive, rigorous, and rich with all the insights gathered.
            Keep it TECHNICAL and SERIOUS - post-production will handle accessibility and entertainment.
            
            Language: {language}
            """
    
    @staticmethod
    def comedy_enhancement_task(
        tone_instructions: str,
        language: str,
        focus: str
    ) -> str:
        """Create comedy enhancement task."""
        return f"""
                POST-PRODUCTION PHASE 1: COMEDY ENHANCEMENT
                
                You are receiving ALL the serious technical conversations from the conversation phase.
                Your job is to add appropriate humor and entertainment value while maintaining respect for the science.
                
                Technical content processed so far includes:
                - Initial analysis from all conversation agents
                - Specialized domain expert deep dive
                - Dynamic Q&A sessions between experts  
                - Interdisciplinary technical debates
                - Collaborative synthesis
                - Final comprehensive technical discussion
                
                Review ALL this technical content and:
                1. Identify moments where humor can enhance understanding
                2. Create clever analogies that make complex concepts memorable
                3. Find amusing but respectful observations about the research
                4. Develop entertaining examples that illustrate key points
                5. Add witty commentary that makes the discussion more engaging
                6. Use wordplay and clever observations appropriate to the topic
                7. Insert humor that bridges different specialist perspectives
                8. Make technical debates more entertaining without losing substance
                9. Add comic relief to dense technical discussions
                10. Create memorable one-liners that help key concepts stick
                
                Your goal is to make the content more accessible and entertaining WITHOUT undermining the scientific rigor.
                Think Neil deGrasse Tyson explaining astrophysics - serious science, but delivered with wit and charm.
                
                The output should be the SAME technical content but now enhanced with appropriate humor and entertainment.
                You are NOT writing the final script - you're adding humor to the technical discussions.
                
                {tone_instructions}
                
                Language: {language}
                """
    
    @staticmethod
    def educational_script_task(
        paper_title: str,
        has_humor_agent: bool,
        technical_instructions: str,
        duration_instructions: str,
        language_instructions: str,
        language: str,
        focus: str,
        tone: str
    ) -> str:
        """Create educational script task."""
        return f"""
            POST-PRODUCTION PHASE 2: EDUCATIONAL SCRIPT CREATION
            
            Transform ALL the rich content into a comprehensive educational lecture text.
            
            DOCUMENT TITLE: {paper_title}
            
            You are receiving the complete output, which includes:
            - Initial analysis from all conversation agents
            - Specialized domain expert deep dive
            - Dynamic Q&A sessions between experts
            - Interdisciplinary technical debates
            - Collaborative synthesis
            - Final comprehensive technical discussion
            {"- Comedy-enhanced version with appropriate humor" if has_humor_agent else ""}
            
            Your job is to distill ALL this rich content into a single educator voice.
            
            The script MUST follow the Voice Papers style guide structure:
            
            1. NARRATIVE STRUCTURE (from style guide):
               - START with a hook that's SPECIFIC to the paper's topic. Choose from these types:
                 • Escenario relatable: Create a scenario relevant to the paper's subject
                 • Contexto histórico: Find a historical moment related to the field
                 • Alarma/problema: Identify a current challenge in the domain
                 • Pregunta intrigante: Pose a thought-provoking question about the topic
               - The hook MUST relate directly to the paper's content, not use generic examples
               - THEN naturally introduce "{paper_title}" after the hook, if not stated explicitly do not use it
               - Structure as three acts when possible: Problema → Solución → Implicaciones
               - NEVER start with: "En resumen", "Hoy vamos a hablar de", "Este es un resumen de"
            
            2. CONVERSATIONAL TONE (Voice Papers style):
               - Written as a SINGLE EDUCATOR speaking directly (use "tú"/"usted")
               - Use frequent rhetorical questions: "¿Parece simple, no?", "¿Te suena familiar?"
               - Show personality: "En mi opinión...", "Lo que más me sorprende es..."
            3. TECHNICAL EXPLANATIONS (Voice Papers layered approach):
               - Start with the simplest version of the concept
               - Add complexity gradually in layers
               - Define terms naturally in flow: "esto se llama X, que básicamente significa..."
               - Use MINIMUM 2-3 analogies per script from everyday life
            
            4. RHYTHM AND FLOW (style guide requirements):
               - Mix sentence lengths: short for impact, long for explanation
               - Natural transitions: "Ahora bien...", "Pero aquí está lo interesante..."
               - Create expectation: "En un momento veremos algo sorprendente..."
               - Strategic pauses and emphasis for voice delivery
            
            5. STORYTELLING (academic narrative from style guide):
               - Humanize when possible: "Los investigadores se sorprendieron cuando..."
               - Create narrative tension before revealing findings
            
            6. CORE REQUIREMENTS:
               - Include ALL key insights from conversations and specialist exchanges
               - Flow naturally with smooth transitions between concepts
               - Write as continuous text for voice actor (no headers/formatting)
               - Address listener directly: "puedes imaginar", "te darás cuenta"
               - End with practical implications and thought-provoking questions
               - Incorporate depth from ALL agent conversations
            
            STYLE GUIDE CHECKLIST - ALL ITEMS MANDATORY:
            ✓ Hook: Used one of the 4 exact types from style guide?
            ✓ Direct address: Speaking to "tú" throughout?
            ✓ Transitions: Natural connectors between ideas?
            ✓ Rhythm: Varied sentence lengths for flow?
            
            CRITICAL DIDACTIC STRUCTURE:
            - INTRODUCTION: Hook → Title → Preview 
            - DEVELOPMENT: Layered explanations with examples
            - CONCLUSION: Clear recap ("Hemos visto que...", "Para cerrar...")
            - The script should not be necessarily inspirational, it should be a technical explanation of content
            NATURAL LANGUAGE REQUIREMENTS:
            - AVOID: fundamental, crucial, esencial, revelador, fascinante, delve, robust <- THIS IS MANDATORY
            - USE: importante, interesante, sorprendente, resulta que, descubrimos que
            - Sound like explaining to a curious friend, not generating content
            
            CRITICAL - MULTI-SPECIALIST INTEGRATION:
            19. Weave in insights that could ONLY come from having multiple specialist perspectives
            20. Include cross-disciplinary connections discovered during discussions
            21. Incorporate domain-specific knowledge from ALL participating specialists
            
            {"23. Naturally integrate the entertaining elements added by the Comedy Communicator" if has_humor_agent else ""}
            {"24. Demonstrate the value of interdisciplinary analysis throughout" if has_humor_agent else "23. Demonstrate the value of interdisciplinary analysis throughout"}
            
            {technical_instructions}
            
            {duration_instructions}
            
            {language_instructions}
            
            Language: {language}
            """
    
    @staticmethod
    def original_initial_analysis_task(
        paper_title: str,
        paper_content: str,
        conversation_agents: list,
        specialized_agents: list,
        language: str,
        focus: str
    ) -> str:
        """Create original initial analysis task."""
        return f"""
            Analyze the synthesis of the paper titled "{paper_title}" and provide your perspective.
            
            Paper synthesis:
            {paper_content}
            
            PARTICIPATING AGENTS (technical conversation only):
            - Base conversation agents (Coordinator, Scientific Reviewer, Critical Thinker)
            - ALL specialized domain agents
            
            EXCLUDED FROM ANALYSIS: Master Educational Science Communicator & Storyteller and Comedy Communicator (work in post-production)
            
            Each participating conversation agent should:
            1. Read and understand the paper from your specific role's perspective
            2. Identify key points relevant to your expertise
            3. Prepare questions or concerns to discuss
            4. Consider the implications from your unique viewpoint
            
            SPECIALIZED AGENTS: Include your domain-specific insights that only you can provide.
            
            Keep this TECHNICAL and SERIOUS - entertainment will be added later in post-production.
            
            Language: {language}
            """
    
    @staticmethod
    def original_discussion_task(
        conversation_agents: list,
        specialized_agents: list,
        language: str,
        focus: str
    ) -> str:
        """Create original discussion task."""
        return f"""
            Based on the initial analysis, conduct a thorough technical discussion of the paper synthesis involving conversation agents.
            
            PARTICIPATING AGENTS (technical conversation only):
            - Base conversation agents (Coordinator, Scientific Reviewer, Critical Thinker)
            - ALL specialized domain agents
            
            EXCLUDED FROM DISCUSSION: Master Educational Science Communicator & Storyteller and Comedy Communicator (they process the output in post-production)
            
            The technical discussion should:
            1. Cover all major points of the paper
            2. Include different perspectives from conversation agents (base + specialists)
            3. Address potential concerns and criticisms from multiple expert viewpoints
            4. Explore implications and applications from various specialist domains
            5. Be comprehensive and technically rigorous
            
            SPECIALIZED AGENTS: This is your chance to contribute domain expertise!
            
            Create a rich technical dialogue that showcases multiple expert perspectives.
            This is the FINAL conversation output that will be handed to the post-production team.
            Keep it TECHNICAL and SERIOUS - post-production will handle accessibility and entertainment.
            
            Language: {language}
            """
    
    @staticmethod
    def original_comedy_task(
        tone_instructions: str,
        language: str,
        focus: str
    ) -> str:
        """Create original comedy task."""
        return f"""
                POST-PRODUCTION PHASE 1: COMEDY ENHANCEMENT
                
                You are receiving the serious technical conversations from the conversation phase.
                Your job is to add appropriate humor and entertainment value while maintaining respect for the science.
                
                Technical content processed so far includes:
                - Initial analysis from all conversation agents
                - Comprehensive technical discussion between all expert perspectives
                
                Review ALL this technical content and:
                1. Identify moments where humor can enhance understanding
                2. Create clever analogies that make complex concepts memorable
                3. Find amusing but respectful observations about the research
                4. Develop entertaining examples that illustrate key points
                5. Add witty commentary that makes the discussion more engaging
                6. Use wordplay and clever observations appropriate to the topic
                7. Insert humor that bridges different specialist perspectives
                8. Make the technical discussion more entertaining without losing substance
                9. Add comic relief to dense technical discussions
                10. Create memorable one-liners that help key concepts stick
                
                Your goal is to make the content more accessible and entertaining WITHOUT undermining the scientific rigor.
                Think Neil deGrasse Tyson explaining astrophysics - serious science, but delivered with wit and charm.
                
                The output should be the SAME technical content but now enhanced with appropriate humor and entertainment.
                You are NOT writing the final script - you're adding humor to the technical discussions.
                
                {tone_instructions}
                
                Language: {language}
                """
    
    @staticmethod
    def original_educational_script_task(
        paper_title: str,
        has_humor_agent: bool,
        technical_instructions: str,
        duration_instructions: str,
        language_instructions: str,
        language: str,
        focus: str,
        tone: str
    ) -> str:
        """Create original educational script task."""
        return f"""
            POST-PRODUCTION PHASE 2: EDUCATIONAL SCRIPT CREATION
            
            Transform the conversation into a comprehensive educational lecture text.
            
            You are receiving the complete output from the conversation phase, which included:
            - Initial analysis from all conversation agents
            - Comprehensive discussion between all expert perspectives
            {"- Comedy-enhanced version with appropriate humor" if has_humor_agent else ""}
            
            Your job is to distill ALL this rich content into a single educator voice.
            
            The script MUST follow the Voice Papers style guide:
            
            1. NARRATIVE STRUCTURE (mandatory from style guide):
               - Hook: Use one of the 4 exact types (escenario, histórico, alarma, pregunta)
               - Development: Three acts when possible (Problema → Solución → Implicaciones)
               - Closure: Practical conclusions with future vision
            
            2. CONVERSATIONAL ELEMENTS (required):
               - Single educator voice speaking directly ("tú"/"usted")
               - Rhetorical questions throughout: "¿No es sorprendente?"
               - Personal touches: "En mi opinión...", "Me fascina que..."
               - Direct address: "puedes imaginar", "te darás cuenta"
            
            3. TECHNICAL EXPLANATIONS (layered approach):
               - Start simple, add complexity gradually
               - Define terms naturally in flow
               - Minimum 2-3 everyday analogies
               - Connect abstract to concrete
            
            4. ENGAGEMENT TECHNIQUES:
               - Create expectation and suspense
               - Guide thinking with questions
               - Include "aha!" moments
               - Moments of wonder and curiosity
            
            5. INTEGRATION REQUIREMENTS:
               - Include ALL specialist perspectives
               - Show cross-disciplinary connections
               - Weave insights naturally (not "experts said")
               - Write as YOU teaching, not summarizing
            
            6. FORMAT:
               - Continuous text for voice (no headers/marks)
               - Natural flow between concepts
               - End with practical implications and questions
               - Plain text optimized for speech
            
            CRITICAL DIDACTIC TECHNIQUES - MANDATORY:
            21. INTRODUCTION must include a compelling preview/roadmap: Start with an engaging hook and then preview what the listener will learn - "En los próximos minutos vas a descubrir...", "Te voy a mostrar tres ideas que cambiarán tu forma de pensar sobre...", etc.
            22. CONCLUSION must include a clear summary: End with a recap of the main points covered - "Hemos visto que...", "En resumen, tres puntos clave...", "Para cerrar, recordemos que...", etc.
            23. AVOID TYPICAL LLM WORDS: Never use overused AI-generated words like "fundamental", "crucial", "clave" (as adjective), "esencial", "revelador", "fascinante", "delve into", "explore", "unpack", "dive deep", "robust", "compelling", etc.
            24. USE NATURAL LANGUAGE: Instead of LLM words, use conversational alternatives like "importante", "interesante", "sorprendente", "nos ayuda a entender", "vamos a ver", "resulta que", "descubrimos que", etc.
            25. SOUND HUMAN: Write as if explaining to a friend over coffee, not as if generating academic content
            {"21. Naturally integrate the entertaining elements added by the Comedy Communicator" if has_humor_agent else ""}
            
            {technical_instructions}
            
            {duration_instructions}
            
            {language_instructions}
            
            Language: {language}
            """
    
    @staticmethod
    def synthesis_task(
        chunks: list,
        paper_title: str,
        language: str,
        focus: str
    ) -> str:
        """Create synthesis task for chunked document analysis."""
        return f"""
            You have received detailed analyses of all {len(chunks)} sections of the paper "{paper_title}".
            
            Create a comprehensive synthesis that EXTRACTS and PRESENTS the actual content, NOT a meta-analysis about the paper.
            
            CRITICAL: Present the IDEAS, FINDINGS, and ARGUMENTS themselves, not descriptions of them.
            
            WRONG: "The paper discusses three main approaches to..."
            RIGHT: "The three approaches are: 1) X works by... 2) Y achieves... 3) Z enables..."
            
            WRONG: "The authors present evidence showing..."
            RIGHT: "The evidence shows that X increased by 47% when..."
            
            Structure your synthesis as follows:
            
            **FIRST LINE - TITLE:** Extract and place the actual document title as the very first line
            - If title is provided: "{paper_title}"
            - If no title found in content, extract it from the document
            - Format: Just the title text on its own line, no prefix
            
            **TLDR:** (3-5 bullet points) - COMES AFTER THE TITLE
            - The core discovery/argument in one clear statement
            - 2-3 key findings with specific details
            - The main implication or breakthrough
            
            **MAIN THESIS/ARGUMENT:**
            State the central claim or discovery directly. What IS the finding, not what the paper says about it.
            
            **KEY POINTS WITH SUPPORTING EVIDENCE:**
            1. First major point: [State it directly]
               - Evidence: [Specific data, results, or reasoning]
               - Why it matters: [Direct implication]
            
            2. Second major point: [State it directly]
               - Evidence: [Specific data, results, or reasoning]
               - Why it matters: [Direct implication]
            
            [Continue for all major points]
            
            **SECONDARY INSIGHTS:**
            - List additional findings, observations, or contributions
            - Include specific details, numbers, or mechanisms
            
            **EXAMPLES AND APPLICATIONS:**
            - Concrete examples given in the paper
            - Real-world applications or use cases
            - Specific scenarios or case studies
            
            **METHODOLOGY HIGHLIGHTS:** (if relevant)
            - Key approaches or techniques used
            - Novel methods introduced
            - Important experimental details
            
            **CONCLUSIONS AND IMPLICATIONS:**
            - What can we now do/know that we couldn't before?
            - Specific future directions mentioned
            - Concrete impact on the field
            
            Remember: You are extracting and organizing the ACTUAL CONTENT, not describing what the paper contains.
            Write as if you are teaching the concepts directly, not reviewing a paper.
            """
    
    @staticmethod
    def technical_chunk_analysis_task(
        chunk: Any,
        language: str
    ) -> str:
        """Create technical chunk analysis task."""
        return f"""
                    Extract ALL factual knowledge from this section.
                    
                    CRITICAL RULES:
                    1. NEVER use meta-language: "el documento presenta", "se discute", "el análisis aborda"
                    2. Extract THE ACTUAL KNOWLEDGE: facts, concepts, examples, explanations
                    3. If text mentions "tres enfoques", EXTRACT what those approaches ARE
                    4. Present ALL objective information: data, definitions, claims, methods
                    
                    EXTRACT:
                    - Facts and data (ALL numbers, dates, measurements)
                    - Concepts (definitions, what things ARE)
                    - Statements made (claims, positions, declarations)
                    - Examples (ALL instances, cases, applications mentioned)
                    - Explanations (how things work, why things happen)
                    - Comparisons (X vs Y, differences, similarities)
                    - Methods/processes (steps, procedures, techniques)
                    
                    WRONG: "El documento presenta tres enfoques"
                    RIGHT: "Los tres enfoques son: [extract actual approaches]"
                    
                    WRONG: "Se discute una innovadora reducción de costos del 40%"
                    RIGHT: "Reducción de costos: 40%"
                    
                    WRONG: "El análisis revela fascinantes implicaciones"
                    RIGHT: "Implicaciones: [list actual implications mentioned]"
                    
                    Content to analyze:
                    {chunk.content}
                    
                    Extract ALL knowledge. Present facts, not descriptions of facts.
                    """
    
    @staticmethod
    def technical_synthesis_task(
        chunks: list,
        paper_title: str,
        language: str
    ) -> str:
        """Create technical synthesis task."""
        return f"""
                You have received objective analyses of all {len(chunks)} sections.
                
                Create an OBJECTIVE KNOWLEDGE SYNTHESIS that extracts ALL factual content without interpretation.
                
                CRITICAL RULES:
                1. FIRST LINE MUST BE THE TITLE: Extract and place the document title as the very first line
                   - If title is provided: "{paper_title}"
                   - If no title found, extract from content
                   - Format: Just the title text, no "Title:" prefix
                2. NO META-LANGUAGE: Never say "se presenta", "se discute", "se aborda"
                3. Extract THE ACTUAL KNOWLEDGE: facts, concepts, declarations, examples
                4. Present ALL objective information: data, definitions, explanations, methods
                5. Remove ALL interpretive language and subjective adjectives
                
                EXTRACT AND PRESENT:
                - Facts and data (numbers, statistics, measurements)
                - Concepts and definitions (what things ARE)
                - Declarations made (statements, claims, positions)
                - Examples provided (cases, instances, applications)
                - Explanations given (how things work)
                - Methods described (processes, procedures)
                - Comparisons made
                - Historical information
                
                WRONG: "Se abordan las implicaciones revolucionarias del model as a service"
                RIGHT: "El 'model as a service': 1) Definición: X, 2) Funciona mediante: Y, 3) Ejemplos: Z"
                
                WRONG: "El innovador análisis presenta tres métodos"
                RIGHT: "Los tres métodos son: método A [qué es y cómo funciona], método B [descripción], método C [proceso]"
                
                Structure (AFTER TITLE):
                - Key facts and data points
                - Concepts and definitions
                - Statements and claims made
                - Examples and applications
                - Methods and processes
                - Results and findings
                
                Present ALL extractable knowledge. Zero interpretation. Complete objectivity.
                """
    
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