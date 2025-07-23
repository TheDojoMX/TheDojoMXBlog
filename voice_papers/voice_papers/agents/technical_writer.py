"""Technical Writer agent using centralized prompt management."""

from crewai import Agent, Task, LLM
from typing import Dict, Any
from .prompts import PromptComposer, TaskPrompts


def get_technical_writer_agent(llm: LLM) -> Agent:
    """Create a specialized Objective Knowledge Extractor agent using centralized prompts."""
    composer = PromptComposer()
    
    # The OBJECTIVE_KNOWLEDGE_EXTRACTOR prompt already has everything we need
    backstory = composer.compose_agent_prompt(
        agent_type="objective_knowledge_extractor",
        focus="technical",
        language="Spanish",
        tone="academic"
    )
    
    return Agent(
        role="Objective Knowledge Extractor",
        goal="Extract and present all factual content, concepts, and knowledge with zero interpretation",
        backstory=backstory,
        llm=llm,
        verbose=True,
        max_iter=2,
    )


def create_technical_writing_task(
    content: str,
    title: str,
    target_length: str = "comprehensive",
    language: str = "English"
) -> str:
    """Create a task description for objective knowledge extraction.
    
    Now uses centralized TaskPrompts system.
    """
    return TaskPrompts.technical_extraction_task(
        title=title,
        content=content,
        language=language,
        target_length=target_length
    )


def create_technical_summary_task(
    synthesis: str,
    paper_title: str,
    max_length: int = 2000
) -> str:
    """Create a task for technical summary without interpretation."""
    
    return f"""
Create a technical summary of "{paper_title}" based on this synthesis.

SYNTHESIS:
{synthesis}

REQUIREMENTS:
1. Maximum {max_length} characters
2. NO interpretation or implications
3. ONLY state explicit facts and findings
4. Use technical language
5. Structure: Overview → Key Concepts → Main Findings → Methods (if applicable)

FORMAT:
## Overview
[Direct statement of what this is about]

## Key Concepts
- Concept 1: [definition]
- Concept 2: [definition]

## Main Findings
1. [Direct statement of finding]
2. [Direct statement of finding]

## Methods (if mentioned)
- [Direct description of methods]

Remember: Technical accuracy without interpretation.
"""


class TechnicalWriterConfig:
    """Configuration for technical writing style.
    
    Now pulls configuration from centralized system.
    """
    
    @classmethod
    def get_avoid_words(cls) -> list:
        """Get words to avoid from centralized constraints."""
        composer = PromptComposer()
        return composer.get_avoided_words_list(focus="technical", language="Spanish")
    
    @classmethod
    def get_transitions(cls) -> list:
        """Get technical transitions from centralized templates."""
        # These are still specific to technical writing
        return [
            "The process includes:",
            "Components:",
            "The method consists of:",
            "Requirements:",
            "Specifications:",
            "The algorithm uses:",
            "Parameters:",
            "The system contains:"
        ]
    
    @classmethod
    def get_structure_templates(cls) -> dict:
        """Get structure templates from centralized system."""
        from .prompts import PromptTemplates
        # Use centralized technical templates
        return PromptTemplates.TECHNICAL_TEMPLATES


def get_technical_writer_with_config(llm: LLM, config: Dict[str, Any] = None) -> Agent:
    """Create a technical writer with specific configuration."""
    
    base_config = {
        "style": "technical_manual",
        "interpretation_level": "zero",
        "structure": "hierarchical",
        "language": "precise"
    }
    
    if config:
        base_config.update(config)
    
    style_instructions = f"""
    Configuration:
    - Style: {base_config['style']}
    - Interpretation: {base_config['interpretation_level']}
    - Structure: {base_config['structure']}
    - Language: {base_config['language']}
    """
    
    agent = get_technical_writer_agent(llm)
    agent.backstory += f"\n\n{style_instructions}"
    
    return agent