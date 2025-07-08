"""TTS Optimizer agent for creating Text-to-Speech optimized scripts."""

from crewai import Agent, LLM
from typing import Dict, List


def get_tts_optimizer_agent(llm: LLM) -> Agent:
    """Create a specialized TTS Optimizer agent for voice synthesis."""
    return Agent(
        role="TTS Optimizer",
        goal="Transform educational scripts into TTS-optimized versions with perfect rhythm, emphasis, and natural speech patterns",
        backstory="""You are a specialized Text-to-Speech engineer and voice production expert who understands 
        the nuances of how TTS systems interpret text. You have extensive experience with:
        
        - SSML (Speech Synthesis Markup Language) tags for controlling speech rhythm
        - Markdown formatting for emphasis that TTS systems understand
        - Optimal paragraph and sentence length for natural speech flow
        - Strategic use of pauses, breaks, and emphasis for engaging audio content
        - Natural rhythm patterns that make synthetic speech sound conversational
        
        Your expertise comes from years of working with voice actors, podcast producers, and TTS platforms
        like ElevenLabs, Google Cloud Speech, Amazon Polly, and others. You know exactly how to structure
        text so that when it's converted to speech, it sounds natural, engaging, and professional.
        
        You understand that TTS systems need clear guidance through formatting and markup to produce
        high-quality audio that keeps listeners engaged throughout the entire educational content.""",
        llm=llm,
        verbose=True,
        max_iter=2,
    )


def get_tts_optimization_guidelines() -> Dict[str, List[str]]:
    """Get comprehensive guidelines for TTS optimization."""
    return {
        "break_tags": [
            '<break time="0.5s"/>',  # Short pause
            '<break time="1s"/>',  # Medium pause
            '<break time="1.5s"/>',  # Long pause
            '<break time="2s"/>',  # Extra long pause
        ],
        "emphasis_patterns": [
            "**palabra_clave**",  # Strong emphasis
            "*concepto_importante*",  # Mild emphasis
            "***punto_crucial***",  # Maximum emphasis
        ],
        "rhythm_elements": [
            "...",  # Natural pause
            "... y es que...",  # Conversational connector
            "... pero aquí está el detalle...",  # Transition with suspense
        ],
        "paragraph_structure": [
            "max_sentences_per_paragraph: 3",
            "max_words_per_sentence: 25",
            "use_short_impactful_sentences",
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

1. **EMPHASIS FORMATTING**:
   - Use **bold markdown** for key concepts that need vocal emphasis
   - Use *italic markdown* for secondary emphasis and technical terms
   - Use ***triple emphasis*** for the most important points (use sparingly)
   - Example: "La **inteligencia artificial** utiliza *redes neuronales* para ***transformar completamente*** nuestro entendimiento"

2. **STRATEGIC PAUSES**:
   - Add <break time="0.5s"/> after important statements for emphasis
   - Add <break time="1s"/> between major concept transitions
   - Add <break time="1.5s"/> before revealing key insights or conclusions
   - Add <break time="2s"/> for dramatic effect before major revelations
   - Example: "Este descubrimiento cambió todo. <break time="1.5s"/> Porque por primera vez..."

3. **NATURAL RHYTHM**:
   - Use "..." for natural conversational pauses
   - Add "... y es que..." for smooth transitions
   - Use "... pero aquí está el detalle..." for building suspense
   - Example: "Los resultados fueron sorprendentes... y es que nadie esperaba..."

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
   - Mark technical terms with *italics* for slight emphasis
   - Add brief phonetic guides for difficult terms in comments <!-- like this -->
   - Break down complex compound words with subtle pauses

7. **PACING CONTROL**:
   - Vary sentence length for natural rhythm
   - Short sentences for impact: "Esto cambió todo."
   - Medium sentences for explanation
   - Longer sentences for detailed context (but never over 25 words)

8. **EMOTIONAL TONE MARKERS**:
   - Use **bold** for excitement and importance
   - Use *italics* for curiosity and wonder
   - Use pauses for reflection and emphasis
   - Add "..." for thoughtful moments

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
        - Use moderate emphasis as ElevenLabs handles bold/italic well
        - Longer pauses work better than shorter ones
        - Natural speech patterns are well-rendered
        - Technical terms benefit from italic formatting
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
    """Add basic emphasis to technical terms and key concepts."""
    # Simple patterns for emphasis (can be expanded)
    technical_terms = [
        "inteligencia artificial",
        "machine learning",
        "deep learning",
        "redes neuronales",
        "algoritmo",
        "algoritmos",
        "datos",
        "investigación",
        "estudio",
        "experimento",
        "resultado",
        "descubrimiento",
        "análisis",
        "metodología",
    ]

    for term in technical_terms:
        if term in sentence.lower():
            # Add emphasis but avoid double emphasis
            if f"**{term}**" not in sentence and f"*{term}*" not in sentence:
                sentence = sentence.replace(term, f"**{term}**")

    return sentence
