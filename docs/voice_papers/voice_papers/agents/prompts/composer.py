"""Prompt composer for Voice Papers agents.

This module provides utilities to compose prompts from various components,
combining system prompts, task prompts, constraints, and style guides.
"""

from typing import Dict, Any, Optional, List
from .system_prompts import SystemPrompts
from .task_prompts import TaskPrompts
from .style_guides import StyleGuides
from .constraints import Constraints
from .templates import PromptTemplates


class PromptComposer:
    """Compose prompts from centralized components."""
    
    def __init__(self):
        """Initialize the prompt composer."""
        self.system_prompts = SystemPrompts
        self.task_prompts = TaskPrompts
        self.style_guides = StyleGuides
        self.constraints = Constraints
        self.templates = PromptTemplates
    
    def compose_agent_prompt(
        self,
        agent_type: str,
        focus: Optional[str] = None,
        language: str = "Spanish",
        tone: str = "academic",
        additional_context: Optional[str] = None
    ) -> str:
        """Compose a complete agent prompt with all components.
        
        Args:
            agent_type: Type of agent (e.g., 'educational_writer')
            focus: Optional focus mode
            language: Target language
            tone: Desired tone
            additional_context: Any additional context to append
            
        Returns:
            Complete composed agent prompt
        """
        # Get base system prompt
        try:
            system_prompt = self.system_prompts.get_prompt(agent_type)
        except ValueError:
            system_prompt = self.system_prompts.EDUCATIONAL_WRITER  # Default
        
        # Add style guide information
        style_info = self._format_style_info(
            self.style_guides.combine_styles("voice_papers", focus, language, tone)
        )
        
        # Add constraints
        constraints_info = self._format_constraints_info(focus, language)
        
        # Compose final prompt
        parts = [system_prompt]
        
        if style_info:
            parts.append(f"\n\nSTYLE GUIDELINES:\n{style_info}")
        
        if constraints_info:
            parts.append(f"\n\nCONSTRAINTS:\n{constraints_info}")
        
        if additional_context:
            parts.append(f"\n\nADDITIONAL CONTEXT:\n{additional_context}")
        
        return "\n".join(parts)
    
    def compose_task_prompt(
        self,
        task_type: str,
        task_params: Dict[str, Any],
        override_components: Optional[Dict[str, Any]] = None
    ) -> str:
        """Compose a task prompt with optional overrides.
        
        Args:
            task_type: Type of task
            task_params: Parameters for the task
            override_components: Optional components to override
            
        Returns:
            Complete composed task prompt
        """
        # Get base task prompt
        base_prompt = self.task_prompts.get_task_prompt(task_type, **task_params)
        
        # Apply any overrides
        if override_components:
            base_prompt = self._apply_overrides(base_prompt, override_components)
        
        return base_prompt
    
    def create_dynamic_prompt(
        self,
        template_type: str,
        values: Dict[str, str],
        include_constraints: bool = True,
        include_style: bool = True
    ) -> str:
        """Create a dynamic prompt from templates.
        
        Args:
            template_type: Type of template to use
            values: Values to fill in the template
            include_constraints: Whether to include constraints
            include_style: Whether to include style guidelines
            
        Returns:
            Dynamically created prompt
        """
        # Get and fill template
        if hasattr(self.templates, f"{template_type.upper()}_TEMPLATES"):
            templates = getattr(self.templates, f"{template_type.upper()}_TEMPLATES")
            if isinstance(templates, dict) and values.get("subtype"):
                template = templates.get(values["subtype"], "")
            else:
                template = templates
        else:
            template = ""
        
        filled_template = self.templates.fill_template(template, values)
        
        # Add constraints and style if requested
        parts = [filled_template]
        
        if include_constraints:
            constraints = self._get_relevant_constraints(values.get("focus"), values.get("language"))
            if constraints:
                parts.append(f"\n\nConstraints:\n{constraints}")
        
        if include_style:
            style = self._get_relevant_style(values.get("style_type", "voice_papers"))
            if style:
                parts.append(f"\n\nStyle Guidelines:\n{style}")
        
        return "\n".join(parts)
    
    def get_avoided_words_list(self, focus: str = None, language: str = "Spanish") -> List[str]:
        """Get a list of words to avoid for the given context."""
        return list(self.constraints.get_avoided_words(focus, language))
    
    def get_transition_words(self, transition_type: str, language: str = "Spanish") -> List[str]:
        """Get appropriate transition words."""
        return self.templates.get_transitions(transition_type, language)
    
    # ============== PRIVATE HELPER METHODS ==============
    
    def _format_style_info(self, style_guide: Dict[str, Any]) -> str:
        """Format style guide information for inclusion in prompt."""
        lines = []
        
        if "tone" in style_guide:
            lines.append(f"Tone: {style_guide['tone'].get('overall', 'conversational')}")
        
        if "structure" in style_guide:
            structure = style_guide["structure"]
            if "opening" in structure:
                lines.append(f"Opening: {structure['opening'].get('duration', '30 seconds')} hook")
            
        if "language" in style_guide:
            lang = style_guide["language"]
            if "voice" in lang:
                lines.append(f"Voice: {lang['voice']}")
        
        return "\n".join(lines)
    
    def _format_constraints_info(self, focus: str, language: str) -> str:
        """Format constraints information for inclusion in prompt."""
        lines = []
        
        # Avoided words
        avoided_words = self.constraints.get_avoided_words(focus, language)
        if avoided_words:
            lines.append(f"Avoid these words/phrases: {', '.join(list(avoided_words)[:10])}...")
        
        # Rules
        if focus:
            rules = self.constraints.get_rules(focus)
            if rules and "attribution_required" in rules:
                lines.append(f"Attribution required for: {', '.join(rules['attribution_required'])}")
        
        return "\n".join(lines)
    
    def _apply_overrides(self, base_prompt: str, overrides: Dict[str, Any]) -> str:
        """Apply override components to a base prompt."""
        prompt = base_prompt
        
        # Override specific sections
        for key, value in overrides.items():
            if key == "append":
                prompt += f"\n\n{value}"
            elif key == "prepend":
                prompt = f"{value}\n\n{prompt}"
            elif key == "replace":
                for old, new in value.items():
                    prompt = prompt.replace(old, new)
        
        return prompt
    
    def _get_relevant_constraints(self, focus: str, language: str) -> str:
        """Get constraints relevant to the current context."""
        constraints = []
        
        avoided = list(self.constraints.get_avoided_words(focus, language))[:5]
        if avoided:
            constraints.append(f"- Avoid: {', '.join(avoided)}")
        
        rules = self.constraints.get_rules(focus or "general")
        if rules:
            constraints.append(f"- Follow {focus or 'general'} rules")
        
        return "\n".join(constraints)
    
    def _get_relevant_style(self, style_type: str) -> str:
        """Get style guidelines relevant to the current context."""
        style = self.style_guides.get_style_guide(style_type)
        
        if not style:
            return ""
        
        lines = []
        if "description" in style:
            lines.append(f"- Style: {style['description']}")
        
        if "tone" in style and "overall" in style["tone"]:
            lines.append(f"- Tone: {style['tone']['overall']}")
        
        return "\n".join(lines)


# ============== CONVENIENCE FUNCTIONS ==============

def compose_agent_backstory(
    agent_type: str,
    **kwargs
) -> str:
    """Convenience function to compose an agent backstory.
    
    Args:
        agent_type: Type of agent
        **kwargs: Additional parameters for composition
        
    Returns:
        Composed agent backstory
    """
    composer = PromptComposer()
    return composer.compose_agent_prompt(agent_type, **kwargs)


def compose_task_instructions(
    task_type: str,
    **kwargs
) -> str:
    """Convenience function to compose task instructions.
    
    Args:
        task_type: Type of task
        **kwargs: Task parameters
        
    Returns:
        Composed task instructions
    """
    composer = PromptComposer()
    return composer.compose_task_prompt(task_type, kwargs)