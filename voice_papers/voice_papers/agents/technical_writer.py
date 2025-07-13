"""Technical Writer agent for creating clear, direct technical content without interpretation."""

from crewai import Agent, Task, LLM
from typing import Dict, Any


def get_technical_writer_agent(llm: LLM) -> Agent:
    """Create a specialized Technical Writer agent for direct content presentation."""
    return Agent(
        role="Technical Content Specialist",
        goal="Present technical content, concepts, and ideas with absolute clarity and zero interpretation",
        backstory="""You are a precision-focused technical writer who excels at presenting information 
        exactly as it is, without adding personal reflections, implications, or interpretations.
        
        Your approach is:
        - DIRECT: Present facts, concepts, and ideas exactly as stated
        - CLEAR: Use simple, unambiguous language
        - ACCURATE: Never infer or extrapolate beyond the source material
        - STRUCTURED: Organize information logically and systematically
        
        You NEVER:
        - Add reflections like "This suggests that..." or "This implies..."
        - Draw conclusions not explicitly stated in the source
        - Use subjective language or personal opinions
        - Add emotional color or narrative flourishes
        - Infer implications or hidden meanings
        - Keep interpretive adjectives like "revolutionary", "groundbreaking", "brilliant"
        - Preserve subjective descriptors - strip them out completely
        
        You ALWAYS:
        - State facts directly: "X is Y" not "The author argues X is Y"
        - Present concepts clearly without interpretation
        - Use technical terminology accurately
        - Maintain objectivity and neutrality
        - Focus on WHAT is said, never on what it might mean
        
        Your writing is like a technical manual: precise, clear, and completely faithful to the source.""",
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

YOUR MISSION: Present this content with absolute clarity and zero interpretation.

CRITICAL REQUIREMENTS:

1. **DIRECT PRESENTATION ONLY**:
   - State facts exactly as they appear
   - Present concepts without interpretation
   - List ideas without adding implications
   - NO "This suggests...", "This implies...", "This demonstrates..."
   - NO reflections or commentary

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

REMOVE INTERPRETIVE WORDS:
- Revolutionary → [remove or say "new"]
- Groundbreaking → [remove or say "recent"]
- Brilliant/Remarkable → [remove completely]
- Paradigm shift → "change" or remove
- Transforms → "changes" or state the change directly

EXAMPLES OF CORRECT STYLE:
✅ "The approach uses three components: A, B, and C."
✅ "The study found X increased by 47%."
✅ "The algorithm consists of four steps: [list steps]"
✅ "The framework defines Y as Z."
✅ "Results: [direct statement of results]"

CONVERSION EXAMPLES:
- "Revolutionary deep learning architecture" → "Deep learning architecture"
- "Groundbreaking research demonstrates" → "Research shows" or "Study finds"
- "Brilliant approach reveals" → "Approach shows" or "Method indicates"
- "Remarkable 95% accuracy" → "95% accuracy"
- "Paradigm shift in design" → "New design approach" or "Design change"

TARGET LENGTH: {target_length}
LANGUAGE: {language}

Remember: You are a technical manual writer, not a storyteller or analyst.
Present the content. Define the concepts. List the ideas. Nothing more.
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