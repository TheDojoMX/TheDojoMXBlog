"""Conversational enhancer agents using centralized prompt management."""

from crewai import Agent, Task
from typing import Optional
from .prompts import PromptComposer, TaskPrompts


def get_conversational_enhancer_agent(llm) -> Agent:
    """Create a Conversational Enhancer agent using centralized prompts."""
    composer = PromptComposer()
    
    backstory = composer.compose_agent_prompt(
        agent_type="conversational_enhancer",
        focus="minimal",
        language="Spanish",
        tone="neutral"
    )
    
    return Agent(
        role="Minimal TTS Enhancer",
        goal="Add ONLY essential connector words to improve text-to-speech flow without changing content",
        backstory=backstory,
        llm=llm,
        verbose=True,
    )


def get_technical_conversational_agent(llm) -> Agent:
    """Create a specialized agent for technical content using centralized prompts."""
    composer = PromptComposer()
    
    backstory = composer.compose_agent_prompt(
        agent_type="technical_conversational",
        focus="technical",
        language="Spanish",
        tone="neutral"
    )
    
    return Agent(
        role="Technical Knowledge Presenter",
        goal="Present extracted objective knowledge in a natural, flowing structure for spoken delivery",
        backstory=backstory,
        llm=llm,
        verbose=True,
    )


def create_conversational_enhancement_task(
    content: str,
    language: str = "Spanish",
    title: str = ""
) -> str:
    """Create task for adding conversational touch to technical content.
    
    Now uses centralized TaskPrompts system.
    """
    return TaskPrompts.conversational_enhancement_task(
        content=content,
        language=language,
        enhancement_level="light"
    )


def create_technical_conversational_task(
    content: str,
    language: str = "Spanish",
    title: str = ""
) -> str:
    """Create task for presenting technical/objective content in a natural structure.
    
    Uses centralized prompts but with specific technical conversational requirements.
    """
    # Create a custom prompt that combines conversational enhancement with technical requirements
    composer = PromptComposer()
    
    # Get base conversational task and customize for technical content
    base_prompt = TaskPrompts.conversational_enhancement_task(
        content=content,
        language=language,
        enhancement_level="full"  # Full conversational transformation for technical
    )
    
    # Add technical-specific requirements
    technical_addon = f"""

SPECIFIC FOR TECHNICAL CONTENT:
- Present ALL extracted knowledge in natural flow
- Group related concepts logically
- Create smooth transitions between topics
- Build from basic to complex when possible
- Preserve ALL facts, data, and technical accuracy

DOCUMENT: {title if title else "Objective Knowledge"}
"""
    
    return base_prompt + technical_addon