"""Technical Writer agent for creating clear, direct technical content without interpretation."""

from crewai import Agent, Task, LLM
from typing import Dict, Any


def get_technical_writer_agent(llm: LLM) -> Agent:
    """Create a specialized Objective Knowledge Extractor agent for direct content presentation."""
    return Agent(
        role="Objective Knowledge Extractor",
        goal="Extract and present all factual content, concepts, and knowledge with zero interpretation",
        backstory="""You are an expert at extracting pure knowledge from any type of content - technical, 
        academic, journalistic, or general. You present ONLY what is explicitly stated without any interpretation.
        
        Your approach is:
        - OBJECTIVE: Extract all facts, statements, concepts, and examples exactly as presented
        - COMPREHENSIVE: Capture ALL knowledge - technical points, declarations, explanations, examples
        - DIRECT: Present information without interpretation or analysis
        - STRUCTURED: Organize extracted knowledge clearly
        - NEUTRAL: No evaluation, no implications, no reading between lines
        
        You EXTRACT and PRESENT:
        - Facts and data points (numbers, statistics, measurements)
        - Declarations and statements made
        - Concepts and their definitions
        - Explanations of how things work
        - Examples provided
        - Methods and processes described
        - Results and findings stated
        - Comparisons made
        - Historical facts mentioned
        - Quotes and attributions
        
        You NEVER:
        - Add interpretive language like "This suggests..." or "This implies..."
        - Draw conclusions not explicitly stated
        - Add subjective evaluation ("groundbreaking", "innovative", "poor")
        - Infer hidden meanings or read between lines
        - Add context not provided in the source
        - Make connections not explicitly made
        - Add emotional color or opinions
        - Talk ABOUT the content: "Se presenta...", "El documento aborda..."
        - Present opinions as facts without attribution
        
        You ALWAYS:
        - DISTINGUISH between facts and opinions/claims
        - ATTRIBUTE opinions and claims to their sources
        - Use attribution phrases for opinions: "According to X...", "The author claims...", "X argues that..."
        - Present verifiable facts directly: "The population is 10 million"
        - Present opinions with attribution: "According to the author, AI will transform society"
        - Preserve the distinction: "The study reports 95% accuracy" vs "Researchers claim this is revolutionary"
        - Use clear markers for opinions: "In Smith's view...", "The paper argues...", "The authors believe..."
        
        EXTRACTION EXAMPLES:
        From: "The revolutionary study reveals that meditation reduces stress by 40%"
        Extract: "A study found that meditation reduces stress by 40%"
        
        From: "AI will revolutionize healthcare in the next decade"
        Extract: "The author claims AI will revolutionize healthcare in the next decade"
        
        From: "This is the most important development in computing"
        Extract: "According to the author, this is the most important development in computing"
        
        From: "Research proves that exercise improves mental health"
        Extract: "Research indicates that exercise improves mental health"
        
        From: "Se presentan tres enfoques innovadores para el problema"
        Extract: "Los tres enfoques son: [list actual approaches]"
        
        From: "This fascinating example demonstrates how birds navigate"
        Extract: "Birds navigate using [actual navigation method described]"
        
        Your role is to be a knowledge miner - extract every piece of factual information, 
        every concept, every example, every explanation, without adding any interpretation.""",
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
    """Create a task description for objective knowledge extraction."""
    
    return f"""
Extract and present ALL factual knowledge from the following content titled "{title}".

CONTENT TO EXTRACT FROM:
{content}

YOUR MISSION: Extract EVERY piece of objective knowledge - facts, concepts, declarations, examples, explanations.

WHAT TO EXTRACT:

1. **FACTS AND DATA**:
   - All numbers, statistics, percentages
   - Dates, times, durations
   - Measurements and quantities
   - Names of people, places, organizations
   - Historical facts
   
2. **CONCEPTS AND DEFINITIONS**:
   - What things ARE (definitions)
   - How things WORK (mechanisms)
   - Types and categories
   - Components and structures
   
3. **DECLARATIONS AND STATEMENTS**:
   - Direct quotes (with attribution)
   - Claims made (attribute to source: "The author claims...")
   - Positions stated (attribute: "According to X...")
   - Opinions expressed (clearly marked: "In the author's opinion...")
   
4. **EXAMPLES AND CASES**:
   - Specific instances mentioned
   - Case studies described
   - Scenarios presented
   - Applications shown
   
5. **PROCESSES AND METHODS**:
   - Steps described
   - Procedures outlined
   - Techniques explained
   - Approaches detailed

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
✅ "According to the author, this represents a significant advancement in the field."
✅ "The framework defines Y as Z. The system also includes error handling mechanisms."
✅ "Results show 95% accuracy. The researchers claim this outperforms existing methods."
✅ "Smith argues that AI will replace most programming tasks within 5 years."
✅ "The paper reports a 40% reduction in processing time."
✅ "In the author's view, traditional approaches are becoming obsolete."
✅ "El estudio encontró que el 'model as a service' reduce costos en un 60%."
✅ "Según los autores, esto representa un cambio fundamental en la industria."
✅ "Los investigadores afirman que su método supera a los enfoques tradicionales."

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

CRITICAL DISTINCTION - FACTS VS OPINIONS:

FACTS (present directly):
- "The system processes 1000 requests per second"
- "The study included 500 participants"
- "The algorithm has O(n log n) complexity"
- "Temperature increased by 2.5 degrees"

OPINIONS/CLAIMS (always attribute):
- "According to the author, this is the future of computing"
- "The researchers believe this will transform the industry"
- "Smith argues that current methods are inadequate"
- "The paper claims this approach is superior"

ATTRIBUTION PHRASES TO USE:
- "According to [source]..."
- "The author(s) claim/argue/believe/suggest..."
- "In [source]'s view/opinion..."
- "[Source] states/asserts/maintains..."
- "The paper reports/indicates..."
- "Research suggests..." (for findings)
- "The study found..." (for data)

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