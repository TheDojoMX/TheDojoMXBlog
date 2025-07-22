"""Example usage of the centralized prompt management system.

This file demonstrates how to use the new prompt system to create agents
and tasks with consistent, maintainable prompts.
"""

from crewai import Agent, Task, LLM
from .composer import PromptComposer, compose_agent_backstory, compose_task_instructions


# Example 1: Creating an Educational Writer Agent with the new system
def create_educational_writer_new(llm: LLM, focus: str = "explanatory") -> Agent:
    """Create an educational writer using centralized prompts."""
    
    # Compose the agent backstory from centralized components
    backstory = compose_agent_backstory(
        agent_type="educational_writer",
        focus=focus,
        language="Spanish",
        tone="academic",
        additional_context="You excel at creating engaging educational podcast scripts."
    )
    
    return Agent(
        role="Master Educational Science Communicator & Storyteller",
        goal="Transform complex content into engaging educational narratives",
        backstory=backstory,
        llm=llm,
        verbose=True
    )


# Example 2: Creating a Technical Writer Agent
def create_technical_writer_new(llm: LLM) -> Agent:
    """Create a technical writer using centralized prompts."""
    
    backstory = compose_agent_backstory(
        agent_type="objective_knowledge_extractor",
        focus="technical",
        language="Spanish"
    )
    
    return Agent(
        role="Objective Knowledge Extractor",
        goal="Extract and present factual content with proper attribution",
        backstory=backstory,
        llm=llm,
        verbose=True
    )


# Example 3: Creating an Educational Writing Task
def create_educational_task_new(content: str, title: str, duration: int = 5) -> str:
    """Create an educational writing task using centralized prompts."""
    
    return compose_task_instructions(
        task_type="educational_writing",
        title=title,
        content=content,
        language="Spanish",
        duration=duration,
        focus="explanatory",
        tone="academic"
    )


# Example 4: Creating a Technical Extraction Task
def create_technical_task_new(content: str, title: str) -> str:
    """Create a technical extraction task using centralized prompts."""
    
    return compose_task_instructions(
        task_type="technical_extraction",
        title=title,
        content=content,
        language="Spanish",
        target_length="comprehensive"
    )


# Example 5: Using the PromptComposer directly for custom needs
def create_custom_agent_with_overrides(llm: LLM) -> Agent:
    """Example of creating a custom agent with specific overrides."""
    
    composer = PromptComposer()
    
    # Get base backstory
    backstory = composer.compose_agent_prompt(
        agent_type="content_synthesizer",
        focus="critical",
        language="English",
        tone="professional"
    )
    
    # Add custom context
    custom_context = """
    You specialize in pharmaceutical research papers and understand
    the importance of accurately representing clinical trial data.
    """
    
    backstory_with_custom = composer.compose_agent_prompt(
        agent_type="content_synthesizer",
        focus="critical",
        language="English",
        tone="professional",
        additional_context=custom_context
    )
    
    return Agent(
        role="Pharmaceutical Research Synthesizer",
        goal="Create accurate syntheses of clinical research",
        backstory=backstory_with_custom,
        llm=llm,
        verbose=True
    )


# Example 6: Getting constraints and style guides
def demonstrate_constraint_usage():
    """Show how to access constraints and style guides."""
    
    composer = PromptComposer()
    
    # Get avoided words for technical writing in Spanish
    technical_avoided = composer.get_avoided_words_list(
        focus="technical",
        language="Spanish"
    )
    print(f"Words to avoid in technical Spanish: {technical_avoided[:5]}...")
    
    # Get transition words for different purposes
    addition_transitions = composer.get_transition_words("addition", "Spanish")
    contrast_transitions = composer.get_transition_words("contrast", "Spanish")
    
    print(f"Addition transitions: {addition_transitions}")
    print(f"Contrast transitions: {contrast_transitions}")
    
    # Access style guides directly
    from .style_guides import StyleGuides
    
    voice_papers_style = StyleGuides.get_style_guide("voice_papers")
    print(f"Voice Papers tone: {voice_papers_style['tone']['overall']}")


# Example 7: Dynamic prompt creation from templates
def create_hook_from_template():
    """Example of creating a hook using templates."""
    
    composer = PromptComposer()
    
    # Create a relatable scenario hook
    hook = composer.create_dynamic_prompt(
        template_type="hook",
        values={
            "subtype": "relatable_scenario",
            "scenario": "intentas explicar un concepto complejo a un amigo",
            "elaboration": "Las palabras se enredan y el mensaje se pierde",
            "connection_to_topic": "Así es como la ciencia a menudo falla en comunicarse"
        },
        include_constraints=False,
        include_style=False
    )
    
    print(f"Generated hook: {hook}")


# Example 8: Migrating an existing agent function
def migrate_existing_agent_example():
    """Show how to migrate an existing agent to use centralized prompts."""
    
    # OLD WAY (hardcoded backstory):
    def create_agent_old(llm: LLM) -> Agent:
        return Agent(
            role="Educational Writer",
            goal="Transform content into educational narratives",
            backstory="""You are an expert at transforming complex research papers...
            [LONG HARDCODED BACKSTORY HERE]
            You must follow specific style guidelines...
            Avoid these words: fundamental, crucial...
            """,
            llm=llm
        )
    
    # NEW WAY (using centralized prompts):
    def create_agent_new(llm: LLM) -> Agent:
        backstory = compose_agent_backstory(
            agent_type="educational_writer",
            focus="explanatory",
            language="Spanish",
            tone="academic"
        )
        
        return Agent(
            role="Educational Writer",
            goal="Transform content into educational narratives",
            backstory=backstory,
            llm=llm
        )
    
    print("Migration complete! Backstory now comes from centralized system.")


# Example 9: Batch creating multiple agents with consistent styling
def create_focus_agents(llm: LLM, language: str = "Spanish") -> dict:
    """Create multiple focus-specific agents with consistent prompts."""
    
    agents = {}
    
    for focus in ["explanatory", "technical", "critical", "practical"]:
        backstory = compose_agent_backstory(
            agent_type=f"{focus}_focus",
            focus=focus,
            language=language,
            tone="academic"
        )
        
        agents[focus] = Agent(
            role=f"{focus.title()} Focus Expert",
            goal=f"Provide {focus} analysis and presentation",
            backstory=backstory,
            llm=llm,
            verbose=True
        )
    
    return agents


if __name__ == "__main__":
    # Run examples
    print("=== Centralized Prompt System Examples ===\n")
    
    print("1. Demonstrating constraint usage:")
    demonstrate_constraint_usage()
    
    print("\n2. Creating hook from template:")
    create_hook_from_template()
    
    print("\n3. Migration example:")
    migrate_existing_agent_example()
    
    print("\n✅ The centralized prompt system is ready to use!")
    print("   - All prompts are now in one place")
    print("   - Easy to maintain and update")
    print("   - Consistent across all agents")
    print("   - Reusable components")