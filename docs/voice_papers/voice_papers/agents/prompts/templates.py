"""Reusable prompt templates for Voice Papers agents.

This module contains template components that can be mixed and matched
to create custom prompts dynamically.
"""

from typing import Dict, List, Any, Optional


class PromptTemplates:
    """Reusable prompt template components."""
    
    # ============== HOOK TEMPLATES ==============
    
    HOOK_TEMPLATES = {
        "relatable_scenario": """
¿Te ha pasado que {scenario}? {elaboration}. 
{connection_to_topic}""",
        
        "historical_context": """
En {year/period}, {historical_event}. {significance}.
{connection_to_present}""",
        
        "current_problem": """
{problem_statement}. {why_it_matters}.
{transition_to_solution}""",
        
        "provocative_question": """
{question}? {follow_up_thought}.
{invitation_to_explore}"""
    }
    
    # ============== TRANSITION TEMPLATES ==============
    
    TRANSITIONS = {
        "addition": [
            "Además", "También", "Asimismo", "Igualmente",
            "Additionally", "Furthermore", "Moreover", "Also"
        ],
        "contrast": [
            "Sin embargo", "No obstante", "Por otro lado", "Aunque",
            "However", "Nevertheless", "On the other hand", "Although"
        ],
        "cause_effect": [
            "Por lo tanto", "Como resultado", "En consecuencia", "Así que",
            "Therefore", "As a result", "Consequently", "Thus"
        ],
        "example": [
            "Por ejemplo", "Como", "Tal como", "A modo de ilustración",
            "For example", "Such as", "Like", "To illustrate"
        ],
        "sequence": [
            "Primero", "Luego", "Después", "Finalmente",
            "First", "Then", "Next", "Finally"
        ],
        "emphasis": [
            "De hecho", "En realidad", "Es más", "Sobre todo",
            "In fact", "Actually", "Indeed", "Especially"
        ]
    }
    
    # ============== EXPLANATION TEMPLATES ==============
    
    EXPLANATION_PATTERNS = {
        "simple_definition": "{term} es {definition}.",
        
        "expanded_definition": """
{term} se refiere a {basic_definition}. 
En términos más simples, {simple_explanation}.
{example_or_context}""",
        
        "analogy": """
{concept} es como {familiar_thing}. 
{how_they_are_similar}. 
{key_difference_if_any}""",
        
        "process": """
El proceso de {process_name} funciona así:
1. {step_1}
2. {step_2}
3. {step_3}
{outcome}""",
        
        "comparison": """
Mientras que {option_a} {characteristic_a},
{option_b} {characteristic_b}.
{key_insight}"""
    }
    
    # ============== CLOSURE TEMPLATES ==============
    
    CLOSURE_TEMPLATES = {
        "summary": """
{key_insight_recap}. {why_it_matters}.
{thought_to_ponder}""",
        
        "future_looking": """
{current_understanding}. {future_possibility}.
{invitation_to_think}""",
        
        "call_to_action": """
{main_takeaway}. {practical_application}.
{encouragement}""",
        
        "philosophical": """
{broader_implication}. {universal_truth}.
{closing_reflection}"""
    }
    
    # ============== ATTRIBUTION TEMPLATES ==============
    
    ATTRIBUTION_TEMPLATES = {
        "claim": "Según {source}, {claim}",
        "belief": "{source} cree que {belief}",
        "argument": "{source} argumenta que {argument}",
        "finding": "El estudio encontró que {finding}",
        "opinion": "En opinión de {source}, {opinion}",
        "data": "Los datos muestran que {data_point}",
        "research": "La investigación indica que {result}"
    }
    
    # ============== TECHNICAL TEMPLATES ==============
    
    TECHNICAL_TEMPLATES = {
        "component_list": """
{system_name} consta de {number} componentes:
- {component_1}: {description_1}
- {component_2}: {description_2}
- {component_3}: {description_3}""",
        
        "specification": """
{parameter}: {value} {unit}
Rango: {min_value} - {max_value}
Condiciones: {conditions}""",
        
        "algorithm": """
Algoritmo {name}:
Entrada: {input_description}
Proceso: {process_description}
Salida: {output_description}
Complejidad: {complexity}"""
    }
    
    # ============== QUESTION TEMPLATES ==============
    
    QUESTION_PATTERNS = {
        "rhetorical": "¿{question}?",
        "leading": "¿{setup}? {answer_hint}",
        "exploratory": "¿Qué pasaría si {scenario}?",
        "reflective": "¿Alguna vez te has preguntado {topic}?",
        "challenging": "¿Y si todo lo que sabemos sobre {topic} estuviera equivocado?"
    }
    
    # ============== HELPER METHODS ==============
    
    @classmethod
    def get_hook_template(cls, hook_type: str) -> str:
        """Get a hook template by type."""
        return cls.HOOK_TEMPLATES.get(hook_type, "")
    
    @classmethod
    def get_transitions(cls, transition_type: str, language: str = "Spanish") -> List[str]:
        """Get transition words/phrases by type and language."""
        all_transitions = cls.TRANSITIONS.get(transition_type, [])
        if language == "Spanish":
            return [t for t in all_transitions if not t[0].isupper() or t[0] in "ÁÉÍÓÚÑ"]
        else:
            return [t for t in all_transitions if t[0].isupper() and t[0] not in "ÁÉÍÓÚÑ"]
    
    @classmethod
    def fill_template(cls, template: str, values: Dict[str, str]) -> str:
        """Fill a template with provided values.
        
        Args:
            template: Template string with {placeholders}
            values: Dictionary of placeholder values
            
        Returns:
            Filled template string
        """
        result = template
        for key, value in values.items():
            result = result.replace(f"{{{key}}}", value)
        return result
    
    @classmethod
    def combine_templates(cls, templates: List[str], connector: str = " ") -> str:
        """Combine multiple templates with a connector."""
        return connector.join(templates)
    
    @classmethod
    def create_custom_template(cls, structure: Dict[str, Any]) -> str:
        """Create a custom template from a structure definition.
        
        Args:
            structure: Dictionary defining the template structure
            
        Returns:
            Custom template string
        """
        parts = []
        
        if "opening" in structure:
            parts.append(structure["opening"])
            
        if "body" in structure:
            if isinstance(structure["body"], list):
                parts.extend(structure["body"])
            else:
                parts.append(structure["body"])
                
        if "closing" in structure:
            parts.append(structure["closing"])
            
        return "\n\n".join(parts)