"""Light Editor agent for minimal readability improvements."""

from crewai import Agent, Task, LLM
from typing import Dict, Any


def get_light_editor_agent(llm: LLM, language: str = "Spanish") -> Agent:
    """Create a Light Editor agent for minimal readability corrections."""
    
    language_rules = {
        "Spanish": """
        REGLAS ESPECÍFICAS PARA ESPAÑOL:
        - Corregir concordancia de género y número (el/la, los/las)
        - Arreglar tiempos verbales incorrectos solo si son errores obvios
        - Añadir artículos faltantes (el, la, los, las, un, una)
        - Corregir preposiciones mal usadas (a, de, en, por, para)
        - Mantener el estilo y tono original
        - NO cambiar vocabulario técnico
        - NO reescribir oraciones completas
        """,
        "English": """
        SPECIFIC RULES FOR ENGLISH:
        - Fix subject-verb agreement (singular/plural)
        - Add missing articles (a, an, the) where necessary
        - Correct obvious verb tense errors
        - Fix preposition usage
        - Maintain original style and tone
        - DO NOT change technical vocabulary
        - DO NOT rewrite entire sentences
        """
    }
    
    return Agent(
        role=f"Light {language} Editor",
        goal=f"Make minimal edits for readability in {language} while preserving content and style",
        backstory=f"""You are a light copy editor who makes ONLY the minimum necessary corrections 
        for readability in {language}. You fix obvious grammatical errors but preserve the author's 
        voice, style, and all content.
        
        Your approach:
        - Fix ONLY clear grammatical errors
        - Add missing articles or prepositions
        - Correct verb conjugations if obviously wrong
        - Fix gender/number agreement in Spanish
        - NEVER change technical terms or concepts
        - NEVER rewrite for "better style"
        - NEVER add or remove content
        - Preserve ALL ideas and information
        
        You make texts readable, not perfect. Think of yourself as fixing typos and basic grammar,
        not as a style editor or content creator.
        
        {language_rules.get(language, language_rules["English"])}
        
        CRITICAL: If the text is already readable, return it unchanged. Less is more.""",
        llm=llm,
        verbose=True,
        max_iter=1,
    )


def create_light_editing_task(
    content: str,
    language: str = "Spanish",
    title: str = ""
) -> str:
    """Create a task for light editing."""
    
    task_description = f"""
Apply MINIMAL editing to make this text readable in {language}.

CONTENT TO EDIT:
{content}

YOUR MISSION: Fix only obvious errors that affect readability. Preserve everything else.

ALLOWED CORRECTIONS:
1. **Grammar fixes (ONLY if clearly wrong)**:
   - Subject-verb agreement
   - Gender/number agreement (Spanish)
   - Verb conjugations
   - Missing articles (el, la, un, the, a)
   - Wrong prepositions

2. **Punctuation (ONLY if missing or wrong)**:
   - Add missing periods at end of sentences
   - Fix comma splices
   - Add missing question marks (¿? in Spanish)

3. **Spacing and formatting**:
   - Fix double spaces
   - Ensure proper paragraph breaks

NOT ALLOWED:
❌ Rewriting sentences for "better flow"
❌ Changing vocabulary (even if repetitive)
❌ Adding transitions or connectors
❌ Removing content
❌ Changing technical terms
❌ "Improving" style
❌ Making it "sound better"

EXAMPLES FOR {language.upper()}:
"""
    
    if language.lower() in ["spanish", "español"]:
        task_description += """
WRONG: "Los resultado muestran" → RIGHT: "Los resultados muestran"
WRONG: "El sistema utiliza tres metodo" → RIGHT: "El sistema utiliza tres métodos"
WRONG: "La algoritmo" → RIGHT: "El algoritmo"
WRONG: "Está basado a" → RIGHT: "Está basado en"

BUT KEEP:
- Technical terms exactly as they are
- Sentence structure (even if awkward)
- All content and ideas
- Original tone and style
"""
    else:
        task_description += """
WRONG: "The results shows" → RIGHT: "The results show"
WRONG: "The system use three method" → RIGHT: "The system uses three methods"
WRONG: "It are based on" → RIGHT: "It is based on"
WRONG: "A algorithm" → RIGHT: "An algorithm"

BUT KEEP:
- Technical terms exactly as they are
- Sentence structure (even if awkward)
- All content and ideas
- Original tone and style
"""
    
    task_description += f"""

OUTPUT: Return the text with minimal corrections applied. If no corrections are needed, return it unchanged.

Remember: You're a light editor, not a rewriter. When in doubt, don't change it.
"""
    
    return task_description


def create_readability_check_task(
    original: str,
    edited: str,
    language: str = "Spanish"
) -> str:
    """Create a task to verify minimal editing was applied."""
    
    return f"""
Compare these two versions and verify that only minimal editing was applied:

ORIGINAL:
{original}

EDITED:
{edited}

CHECK:
1. Were only grammatical errors fixed?
2. Is all content preserved?
3. Are technical terms unchanged?
4. Is the style preserved?
5. Were unnecessary changes avoided?

If the editing went beyond minimal corrections, flag the specific issues.
"""