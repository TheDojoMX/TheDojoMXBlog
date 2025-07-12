"""TTS Optimizer agent for creating Text-to-Speech optimized scripts."""

from crewai import Agent, LLM
from typing import Dict, List


def get_tts_optimizer_agent(llm: LLM) -> Agent:
    """Create a specialized TTS Optimizer agent for voice synthesis."""
    return Agent(
        role="ElevenLabs TTS Optimization Specialist",
        goal="Transform educational scripts into perfectly optimized versions for ElevenLabs TTS using proper XML controls and phonetic techniques",
        backstory="""You are a specialized Text-to-Speech engineer with deep expertise in ElevenLabs' voice synthesis platform.
        You understand that ElevenLabs DOES NOT process markdown formatting and requires specific techniques:
        
        - XML break tags for pauses: <break time="1.5s" /> (max 3 seconds, use sparingly)
        - Phoneme tags for pronunciation: <phoneme alphabet="cmu-arpabet" ph="...">word</phoneme>
        - Lexeme/alias tags for models without phoneme support
        - Phonetic spelling and strategic capitalization for emphasis (NOT markdown)
        - Natural speech patterns through context and narrative flow
        
        You know that excessive break tags cause instability, and that emphasis must be achieved through:
        - Using CAPITALS for strong emphasis
        - Context and narrative cues for emotional delivery
        - Natural speech patterns and punctuation
        
        Your optimizations create scripts that sound natural, engaging, and professional when processed
        by ElevenLabs, avoiding all markdown and using only techniques that ElevenLabs actually supports.""",
        llm=llm,
        verbose=True,
        max_iter=2,
    )


def get_tts_optimization_guidelines() -> Dict[str, List[str]]:
    """Get comprehensive guidelines for TTS optimization."""
    return {
        "break_tags": [
            '<break time="0.5s" />',  # Short pause
            '<break time="1.0s" />',  # Medium pause
            '<break time="1.5s" />',  # Long pause
            '<break time="2.0s" />',  # Dramatic pause
            '<break time="3.0s" />',  # Maximum allowed
        ],
        "emphasis_techniques": [
            "PALABRA CLAVE",  # Capital letters for strong emphasis
            "IMPORTANTE",  # Full capitals for maximum emphasis
            "FASCINANTE",  # Natural emphasis through capitals
            "DESCUBRIMIENTO",  # Key terms in capitals
        ],
        "phoneme_examples": [
            '<phoneme alphabet="cmu-arpabet" ph="T EH1 K N AH0 L OW0 JH IY0">technology</phoneme>',
            '<phoneme alphabet="cmu-arpabet" ph="AY1 EH2 L">AI</phoneme>',
        ],
        "lexeme_examples": [
            '<lexeme><grapheme>AI</grapheme><alias>inteligencia artificial</alias></lexeme>',
            '<lexeme><grapheme>ML</grapheme><alias>machine learning</alias></lexeme>',
        ],
        "rhythm_elements": [
            "Y resulta que",  # Natural connector
            "Pero aquí está lo interesante",  # Suspense builder
            "Ahora bien",  # Topic transition
        ],
        "paragraph_structure": [
            "max_sentences_per_paragraph: 3-4",
            "max_words_per_sentence: 15-25",
            "clear_paragraph_separation",
        ],
    }


def create_tts_optimization_task(
    agent: Agent,
    educational_script: str,
    language: str = "Spanish",
    voice_provider: str = "elevenlabs",
) -> str:
    """Create a task for TTS optimization of educational scripts."""

    guidelines = get_tts_optimization_guidelines()

    return f"""
TRANSFORM the following educational script into a TTS-optimized version for {voice_provider} synthesis in {language}.

ORIGINAL SCRIPT:
{educational_script}

YOUR MISSION: Create a version specifically optimized for Text-to-Speech that will sound natural, engaging, and professional when converted to audio.

CRITICAL TTS OPTIMIZATION REQUIREMENTS:

1. **EMPHASIS TECHNIQUES (NO MARKDOWN)**:
   - Use CAPITAL LETTERS for strong emphasis: "La INTELIGENCIA ARTIFICIAL"
   - Use full CAPITALS for important words: "Esto es IMPORTANTE"
   - Use phoneme tags for precise control when needed: <phoneme alphabet="cmu-arpabet" ph="...">word</phoneme>
   - NEVER use markdown (**bold** or *italic*) - ElevenLabs doesn't process it

2. **STRATEGIC PAUSES (USE SPARINGLY)**:
   - Add <break time="0.5s" /> for brief emphasis
   - Add <break time="1.0s" /> between major concepts
   - Add <break time="1.5s" /> before key revelations
   - Add <break time="2.0s" /> for dramatic effect (rare)
   - Maximum: <break time="3.0s" /> (absolute limit)
   - WARNING: Excessive breaks cause audio instability
   - Example: "Este descubrimiento cambió todo. <break time="1.5s" /> Porque por primera vez..."

3. **NATURAL RHYTHM (CONTEXT-BASED)**:
   - Use narrative context to guide pacing
   - Add conversational connectors: "Y resulta que", "Ahora bien"
   - Build suspense through word choice: "Pero aquí está lo FASCINANTE"
   - Let ElevenLabs infer pauses from punctuation and context
   - Example: "Los resultados fueron sorprendentes. Y resulta que nadie esperaba..."

4. **PARAGRAPH STRUCTURE**:
   - Maximum 3 sentences per paragraph
   - Maximum 25 words per sentence for optimal TTS processing
   - Use short, impactful sentences for key points
   - Separate complex ideas into digestible chunks

5. **CONVERSATIONAL CONNECTORS**:
   - Add natural speech patterns: "Y resulta que...", "Pero esto es solo el comienzo...", "Aquí viene lo interesante..."
   - Use transition phrases that sound natural in speech
   - Include rhetorical questions for engagement: "¿Te has preguntado alguna vez...?"

6. **TECHNICAL TERM HANDLING**:
   - For models with phoneme support: <phoneme alphabet="cmu-arpabet" ph="D IY1 P L ER2 N IH0 NG">deep learning</phoneme>
   - For other models: <lexeme><grapheme>deep learning</grapheme><alias>dip lerning</alias></lexeme>
   - Or use simple CAPITALS: "ALGORITMO", "NEURAL"
   - Keep technical terms natural and clear
   - NEVER use markdown italics for terms

7. **PACING CONTROL**:
   - Vary sentence length for natural rhythm
   - Short sentences for impact: "Esto cambió todo."
   - Medium sentences for explanation
   - Longer sentences for detailed context (but never over 25 words)

8. **EMOTIONAL TONE MARKERS**:
   - Use CAPITALS for excitement: "Esto es INCREÍBLE"
   - Use natural emphasis: "FASCINANTE", "SORPRENDENTE"
   - Use narrative context for emotional guidance
   - Let voice model infer emotion from content
   - Speed settings: 0.7-1.2 (slower for important parts)

9. **SECTION TRANSITIONS**:
   - Mark major transitions with longer breaks: <break time="1.5s"/>
   - Use bridge phrases: "Y ahora, algo aún más fascinante..."
   - Signal topic changes clearly for listener orientation

10. **FINAL STRUCTURE**:
    - Keep the same content and message
    - Maintain the educational flow
    - Optimize ONLY for TTS rendering
    - Test readability by reading aloud mentally

VOICE PROVIDER SPECIFIC OPTIMIZATION for {voice_provider}:
{get_provider_specific_guidelines(voice_provider)}

LANGUAGE SPECIFIC CONSIDERATIONS for {language}:
{get_language_specific_guidelines(language)}

OUTPUT FORMAT:
- Return ONLY the optimized script text
- Include all TTS markup and formatting
- Maintain the original content structure
- Do NOT add explanatory text or comments about the changes
- The output should be ready to send directly to the TTS system

QUALITY CHECK:
- Every paragraph should have natural speech rhythm
- Technical terms should be clearly marked for emphasis
- Transitions should flow smoothly with appropriate pauses
- The script should sound engaging when read aloud
- Sentence length should be optimal for TTS processing
"""


def get_provider_specific_guidelines(provider: str) -> str:
    """Get specific guidelines for different TTS providers."""
    if provider.lower() == "elevenlabs":
        return """
        ELEVENLABS SPECIFIC:
        - NO MARKDOWN - use CAPITALS for emphasis
        - Break tags: use sparingly, max 3 seconds
        - Phoneme tags supported for Flash v2, Turbo v2, English v1
        - Lexeme/alias tags for other models
        - Natural speech patterns through context
        - Speed control: 0.7-1.2 range
        """
    elif provider.lower() == "cartesia":
        return """
        CARTESIA SPECIFIC:
        - Use clear emphasis markers
        - Shorter break times may work better
        - Focus on natural rhythm patterns
        - Clear paragraph separation helps processing
        """
    else:
        return """
        GENERAL TTS OPTIMIZATION:
        - Use standard SSML break tags
        - Moderate emphasis with markdown
        - Clear paragraph structure
        - Natural speech patterns
        """


def get_language_specific_guidelines(language: str) -> str:
    """Get specific guidelines for different languages."""
    if language.lower() in ["spanish", "español"]:
        return """
        SPANISH SPECIFIC:
        - Use natural Spanish rhythm patterns
        - "Y es que..." for explanatory transitions
        - "Resulta que..." for surprising revelations
        - "Ahora bien..." for topic shifts
        - Pay attention to word stress for technical terms
        """
    elif language.lower() == "english":
        return """
        ENGLISH SPECIFIC:
        - Use natural English speech patterns
        - "What's interesting is..." for transitions
        - "Here's the thing..." for emphasis
        - "Now, here's where it gets interesting..." for engagement
        """
    else:
        return """
        GENERAL LANGUAGE OPTIMIZATION:
        - Use natural speech patterns for the target language
        - Add appropriate transition phrases
        - Consider cultural speech rhythm patterns
        - Maintain conversational flow
        """


def optimize_script_for_tts(
    script: str, language: str = "Spanish", voice_provider: str = "elevenlabs"
) -> str:
    """
    Standalone function to optimize a script for TTS without using the full agent system.
    Useful for quick optimizations or batch processing.
    """
    # Basic TTS optimization rules
    optimized_lines = []

    # Split into paragraphs
    paragraphs = script.split("\n\n")

    for i, paragraph in enumerate(paragraphs):
        if not paragraph.strip():
            continue

        # Split into sentences
        sentences = paragraph.split(". ")

        # Process each sentence
        processed_sentences = []
        for j, sentence in enumerate(sentences):
            if not sentence.strip():
                continue

            # Add period back if it was removed by split
            if (
                not sentence.endswith(".")
                and not sentence.endswith("!")
                and not sentence.endswith("?")
            ):
                sentence += "."

            # Add emphasis to key technical terms (simple heuristic)
            sentence = add_basic_emphasis(sentence)

            # Add breaks for natural rhythm
            if j == 0 and i > 0:  # First sentence of new paragraph
                sentence = f'<break time="1s"/>{sentence}'

            processed_sentences.append(sentence)

        # Join sentences with natural pauses
        paragraph_text = " ".join(processed_sentences)

        # Add paragraph-level formatting
        if i > 0:
            paragraph_text = f"\n\n{paragraph_text}"

        optimized_lines.append(paragraph_text)

    return "".join(optimized_lines)


def add_basic_emphasis(sentence: str) -> str:
    """Add basic emphasis to technical terms and key concepts using ElevenLabs-compatible techniques."""
    # Map of terms to their emphasized versions (phonetic or capitals)
    emphasis_map = {
        "inteligencia artificial": "INTELIGENCIA ARTIFICIAL",
        "machine learning": "MACHINE LEARNING",
        "deep learning": "DEEP LEARNING",
        "redes neuronales": "REDES NEURONALES",
        "algoritmo": "ALGORITMO",
        "algoritmos": "ALGORITMOS",
        "datos": "DATOS",
        "investigación": "INVESTIGACIÓN",
        "estudio": "ESTUDIO",
        "experimento": "EXPERIMENTO",
        "resultado": "RESULTADO",
        "descubrimiento": "DESCUBRIMIENTO",
        "análisis": "ANÁLISIS",
        "metodología": "METODOLOGÍA",
    }

    sentence_lower = sentence.lower()
    for term, emphasized in emphasis_map.items():
        if term in sentence_lower:
            # Case-insensitive replacement while preserving original case where possible
            import re
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            sentence = pattern.sub(emphasized, sentence)

    return sentence
