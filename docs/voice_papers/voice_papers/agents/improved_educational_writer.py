"""Improved Educational Writer agent using centralized prompt management."""

from crewai import Agent, Task
from typing import Dict, List
from .prompts import PromptComposer, TaskPrompts


def get_improved_educational_writer(llm) -> Agent:
    """Create an improved Educational Writer using centralized prompts."""
    composer = PromptComposer()
    
    # Compose backstory from centralized system
    backstory = composer.compose_agent_prompt(
        agent_type="educational_writer",
        focus="explanatory",  # Default focus for this agent
        language="Spanish",   # Default language
        tone="academic",      # Default tone
        additional_context="""
        You have studied the best science communicators and developed your own unique style that combines:
        - Three-act narrative structure (Problem → Solution → Implications)
        - Strategic questions that guide the listener's thinking
        - Historical context and real-world applications when available
        
        You understand that great science communication isn't about simplifying—it's about 
        creating bridges from familiar concepts to new discoveries. Your scripts sound like 
        a knowledgeable friend sharing fascinating insights over coffee."""
    )
    
    return Agent(
        role="Master Educational Science Communicator & Storyteller",
        goal="Transform technical content into captivating podcast narratives following the Voice Papers style guide",
        backstory=backstory,
        llm=llm,
        verbose=True,
        max_iter=3,  # Allow iterations to refine the output
    )


def get_natural_language_guidelines() -> Dict[str, List[str]]:
    """Get comprehensive guidelines for natural language generation.
    
    Now pulls from centralized constraints system.
    """
    composer = PromptComposer()
    
    # Get avoided words from centralized system
    avoided_words = composer.get_avoided_words_list(focus="educational", language="Spanish")
    
    # Keep specific start phrases to avoid (these are specific to educational context)
    avoid_at_start = [
        "En resumen",
        "Hoy vamos a hablar de",
        "Este es un resumen de",
        "En este episodio",
        "Hoy exploramos",
        "Vamos a analizar",
    ]
    
    return {
        "avoid_words": avoided_words,
        "avoid_at_start": avoid_at_start,
    }


def create_enhanced_educational_task(
    agent: Agent, language: str, duration: int, technical_level: str, tone: str
) -> str:
    """Create an enhanced task description for the Educational Writer.
    
    Now uses centralized TaskPrompts system.
    """
    # Map technical_level to focus for backwards compatibility
    focus_map = {
        "accessible": "explanatory",
        "technical": "technical", 
        "advanced": "critical",
        "practical": "practical"
    }
    focus = focus_map.get(technical_level, "explanatory")
    
    # Use centralized task prompt system
    # Note: The actual content and title will be provided when the task is created
    return TaskPrompts.educational_writing_task(
        title="[Title will be provided]",
        content="[Content will be provided]", 
        language=language,
        duration=duration,
        focus=focus,
        tone=tone
    )
