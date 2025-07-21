"""Conversational enhancer agent for adding light conversational touch to technical content."""

from crewai import Agent, Task
from typing import Optional


def get_conversational_enhancer_agent(llm) -> Agent:
    """Create a Conversational Enhancer agent that adds subtle conversational elements."""
    return Agent(
        role="Minimal TTS Enhancer",
        goal="Add ONLY essential connector words to improve text-to-speech flow without changing content",
        backstory="""You are an expert at making technical content flow better for TTS synthesis.
        You make EXTREMELY MINIMAL changes - only adding essential connector words where absolutely necessary.
        You NEVER add explanations, examples, or change the meaning. Your changes are barely noticeable.
        Think of yourself as adding only the minimum punctuation and connectors needed for natural speech.""",
        llm=llm,
        verbose=True,
    )


def create_conversational_enhancement_task(
    content: str,
    language: str = "Spanish",
    title: str = ""
) -> str:
    """Create task for adding conversational touch to technical content."""
    
    language_connectors = {
        "Spanish": {
            "connectors": ["Ahora bien", "Por otro lado", "Es decir", "En otras palabras", 
                          "Además", "Sin embargo", "Por ejemplo", "De hecho", "Así que",
                          "Entonces", "Como resultado", "Por lo tanto"],
            "softeners": ["podemos ver que", "es interesante notar que", "vale la pena mencionar que",
                         "como veremos", "esto significa que", "lo que encontramos es que"],
            "transitions": ["Pasando a", "Si miramos", "Cuando consideramos", "Al examinar"],
        },
        "English": {
            "connectors": ["Now", "On the other hand", "That is", "In other words",
                          "Additionally", "However", "For instance", "In fact", "So",
                          "Therefore", "As a result", "Consequently"],
            "softeners": ["we can see that", "it's interesting to note that", "it's worth mentioning that",
                         "as we'll see", "this means that", "what we find is that"],
            "transitions": ["Moving on to", "If we look at", "When we consider", "Examining"],
        }
    }
    
    lang_data = language_connectors.get(language, language_connectors["Spanish"])
    
    return f"""
Add ONLY the MINIMUM connector words needed for text-to-speech flow. DO NOT modify content.

DOCUMENT: {title if title else "Technical Content"}

CONTENT TO ENHANCE:
{content}

ULTRA-MINIMAL CHANGES ONLY - YOU MUST:

1. ADD ONLY THESE SPECIFIC CONNECTORS (maximum 5-10 in the entire text):
   - Between abrupt transitions: "{lang_data['connectors'][0]}", "{lang_data['connectors'][1]}"
   - For clarification: "{lang_data['connectors'][2]}"
   - Maximum ONE connector every 3-4 paragraphs
   
2. FORBIDDEN CHANGES:
   - NO adding phrases like "es interesante", "vale la pena", etc.
   - NO softening statements
   - NO adding explanations
   - NO restructuring
   - NO new sentences
   - NO tone changes
   - NO additional content

3. PRESERVE 99% OF THE TEXT:
   - Keep EXACT same structure
   - Keep EXACT same content
   - Keep EXACT same examples
   - Keep EXACT same technical terms
   - Only add 1-2 word connectors where ABSOLUTELY necessary

EXAMPLE (notice how minimal the change is):
BEFORE: "El sistema tiene tres componentes. El primer componente procesa datos."
AFTER: "El sistema tiene tres componentes. Ahora bien, el primer componente procesa datos."

That's IT. One connector added. Nothing else.

CRITICAL: If the text already flows well, ADD NOTHING. Better to add too little than too much.

Your output should be 99% identical to the input, with only 5-10 single-word or two-word connectors added.

Language: {language}
"""