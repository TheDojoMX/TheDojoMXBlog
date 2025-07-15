"""Technical Writer agent for creating clear, direct technical content without interpretation."""

from crewai import Agent, Task, LLM
from typing import Dict, Any


def get_technical_writer_agent(llm: LLM) -> Agent:
    """Create a specialized Technical Writer agent for direct content presentation."""
    return Agent(
        role="Technical Content Specialist",
        goal="Present technical content with clarity, minimal transitions, and zero interpretation",
        backstory="""You are a precision-focused technical writer who excels at presenting information 
        accurately while maintaining readability through minimal, factual connections.
        
        Your approach is:
        - DIRECT: Present facts, concepts, and ideas exactly as stated
        - CLEAR: Use simple, unambiguous language
        - ACCURATE: Never infer or extrapolate beyond the source material
        - STRUCTURED: Organize information logically with minimal transitions
        - CONNECTED: Use simple, factual transitions only ("Additionally", "Furthermore", "Next")
        
        You NEVER:
        - Add interpretive language like "This suggests..." or "This implies..."
        - Draw conclusions not explicitly stated in the source
        - Use subjective language or personal opinions
        - Add emotional color or narrative flourishes
        - Infer implications or hidden meanings
        - Use interpretive adjectives like "revolutionary", "groundbreaking", "brilliant"
        - Add evaluative connections like "Interestingly" or "Surprisingly"
        - Talk ABOUT the content: "Se abordan las implicaciones...", "El documento presenta..."
        - Mention the discussion process or paper structure
        
        You ALWAYS:
        - State facts directly: "X is Y" not "The author argues X is Y"
        - Present THE IDEAS THEMSELVES, not that they were discussed
        - WRONG: "Se abordan las implicaciones del model as a service"
        - RIGHT: "El 'model as a service' implica X, Y, Z"
        - WRONG: "Se presentan tres enfoques"
        - RIGHT: "Los tres enfoques son: 1) X funciona mediante... 2) Y utiliza... 3) Z permite..."
        - Use technical terminology accurately
        - Maintain objectivity and neutrality
        - Add minimal factual transitions: "The system includes...", "Components consist of...", "The process involves..."
        - Use simple connectors: "Additionally", "Furthermore", "Subsequently", "Next"
        
        ACCEPTABLE TRANSITIONS (factual only):
        - "The system includes three components."
        - "Additionally, the algorithm processes data in parallel."
        - "The method consists of four steps."
        - "Furthermore, the framework supports multiple protocols."
        - "Next, the process validates inputs."
        - "The architecture contains five layers."
        
        Your writing maintains technical accuracy while using minimal connections for readability.""",
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
    """Create a task description for technical writing."""
    
    return f"""
Create a technical presentation of the following content titled "{title}".

CONTENT TO PRESENT:
{content}

YOUR MISSION: Present THE IDEAS AND CONCEPTS THEMSELVES with absolute clarity and zero interpretation.

CRITICAL REQUIREMENTS:

1. **DIRECT PRESENTATION ONLY**:
   - Present THE IDEAS, not that they were discussed
   - State facts exactly as they appear
   - Present concepts without interpretation
   - List ideas without adding implications
   - NO "This suggests...", "This implies...", "This demonstrates..."
   - NO reflections or commentary
   - NO META-LANGUAGE: Never say "Se presenta", "Se aborda", "Se discute"
   - EXTRACT AND PRESENT THE ACTUAL CONTENT

2. **STRUCTURE**:
   - Use clear headings and subheadings
   - Present information in logical order
   - Use bullet points for lists
   - Number sequences or steps
   - Group related concepts together

3. **LANGUAGE RULES**:
   - Use simple, technical language
   - Define technical terms when first used
   - Avoid adjectives that add interpretation
   - No emotional or subjective language
   - Be concise and precise
   - Add minimal factual transitions for flow: "Additionally", "Furthermore", "The system also"
   - Use simple structural connectors: "consists of", "includes", "contains"

4. **CONTENT FIDELITY**:
   - ONLY include factual information
   - STRIP OUT all interpretive language from source
   - Remove adjectives like "revolutionary", "brilliant", "remarkable"
   - Convert subjective statements to objective facts
   - NEVER add examples not in the source
   - NEVER draw conclusions not stated
   - NEVER add context or background
   - NEVER interpret or analyze

5. **FORMATTING**:
   - Use markdown for structure
   - Clear hierarchy with headers
   - Bullet points for lists
   - Code blocks for technical content
   - Tables where appropriate

EXAMPLES OF WHAT TO AVOID:
❌ "This revolutionary approach transforms how we think about..."
❌ "The implications of this finding are profound..."
❌ "This suggests a new paradigm in..."
❌ "Interestingly, the authors reveal..."
❌ "This demonstrates the power of..."
❌ "This groundbreaking research..."
❌ "The brilliant approach..."
❌ "Remarkable findings..."
❌ "Se abordan las implicaciones del model as a service..."
❌ "El documento presenta tres enfoques principales..."
❌ "La discusión se centra en..."
❌ "Se exploran las ventajas de..."
❌ "Los autores argumentan que..."

REMOVE INTERPRETIVE WORDS:
- Revolutionary → [remove or say "new"]
- Groundbreaking → [remove or say "recent"]
- Brilliant/Remarkable → [remove completely]
- Paradigm shift → "change" or remove
- Transforms → "changes" or state the change directly

EXAMPLES OF CORRECT STYLE:
✅ "The approach uses three components: A, B, and C."
✅ "The study found X increased by 47%. Additionally, processing time decreased by 30%."
✅ "The algorithm consists of four steps: [list steps]. Furthermore, each step operates independently."
✅ "The framework defines Y as Z. The system also includes error handling mechanisms."
✅ "Results show 95% accuracy. The method processes 1000 items per second."
✅ "El 'model as a service' implica: 1) reducción de costos, 2) escalabilidad automática, 3) mantenimiento simplificado"
✅ "Los tres enfoques son: enfoque A utiliza X, enfoque B emplea Y, enfoque C implementa Z"
✅ "La arquitectura consta de cinco capas: capa de entrada, procesamiento, análisis, optimización y salida"

CONVERSION EXAMPLES:
- "Revolutionary deep learning architecture" → "Deep learning architecture"
- "Groundbreaking research demonstrates" → "Research shows" or "Study finds"
- "Brilliant approach reveals" → "Approach shows" or "Method indicates"
- "Remarkable 95% accuracy" → "95% accuracy"
- "Paradigm shift in design" → "New design approach" or "Design change"
- "Se abordan las implicaciones del MaaS" → "El MaaS implica X, Y, Z"
- "El documento presenta tres enfoques" → "Los tres enfoques son: A, B, C"
- "Se discuten las ventajas" → "Las ventajas incluyen: 1) X, 2) Y, 3) Z"
- "La síntesis explora" → [Present the actual content being explored]
- "Se analizan los resultados" → "Los resultados muestran..."

TARGET LENGTH: {target_length}
LANGUAGE: {language}

Remember: You are a technical manual writer, not a storyteller or analyst.
Present the content. Define the concepts. List the ideas. Nothing more.

CRITICAL: Never talk ABOUT what was discussed. Present THE ACTUAL IDEAS that were discussed.
If the synthesis says "Se exploran tres métodos", you write "Los tres métodos son: [actual methods]"
"""


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
    """Configuration for technical writing style."""
    
    # Words to avoid (interpretive/subjective)
    AVOID_WORDS = [
        "revolutionary", "groundbreaking", "fascinating", "remarkable",
        "suggests", "implies", "demonstrates", "reveals", "shows that",
        "interestingly", "surprisingly", "notably", "importantly",
        "profound", "significant implications", "paradigm shift",
        "transforms", "revolutionizes", "disrupts"
    ]
    
    # Preferred technical transitions
    TECHNICAL_TRANSITIONS = [
        "The process includes:",
        "Components:",
        "The method consists of:",
        "Requirements:",
        "Specifications:",
        "The algorithm uses:",
        "Parameters:",
        "The system contains:"
    ]
    
    # Structure templates
    STRUCTURE_TEMPLATES = {
        "definition": "{term} is {definition}",
        "list": "{category}:\n- {item1}\n- {item2}\n- {item3}",
        "process": "Steps:\n1. {step1}\n2. {step2}\n3. {step3}",
        "comparison": "{A} uses {method1}. {B} uses {method2}.",
        "specification": "{component}: {specification}"
    }


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