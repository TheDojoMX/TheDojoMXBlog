"""Improved synthesis agents that preserve content spirit."""

from typing import List, Dict, Any
from crewai import Agent, Task, Crew
from ..utils.improved_chunker import ContentType, ImprovedChunk


def create_content_analyzer_agent(llm) -> Agent:
    """Create an agent that analyzes content while preserving its essence."""
    return Agent(
        role="Content Essence Extractor",
        goal="Extract and preserve the true spirit, insights, and unique perspective of each content section",
        backstory="""You are a master at understanding not just WHAT content says, but HOW it says it 
        and WHY it matters. You can distinguish between different types of content - academic research,
        blog posts, news articles, technical docs - and adapt your analysis accordingly.
        
        You never impose a generic "paper" or "document" frame on content. Instead, you treat each
        piece as what it actually is: a research study, a personal reflection, a news report, 
        a technical guide, or whatever form it takes.
        
        You preserve the author's voice, whether it's formal, conversational, technical, or narrative.
        You understand that HOW something is communicated is often as important as WHAT is communicated.""",
        llm=llm,
        verbose=True
    )


def create_synthesis_architect_agent(llm) -> Agent:
    """Create an agent that builds comprehensive synthesis while maintaining authenticity."""
    return Agent(
        role="Synthesis Architect",
        goal="Create a rich, multi-dimensional synthesis that captures both content and character",
        backstory="""You are brilliant at seeing how different pieces fit together to form a complete
        picture. But unlike typical summarizers, you don't flatten everything into bland academic prose.
        
        You understand that:
        - A blog post's conversational asides might be as important as its main points
        - A research paper's methodology reveals as much as its conclusions  
        - A news article's framing shapes its message
        - Technical documentation's examples illuminate its concepts
        
        You build syntheses that preserve not just information, but insight, not just facts, but
        perspective, not just content, but character. You know that the best synthesis makes someone
        feel like they've truly understood the original, not just read about it.""",
        llm=llm,
        verbose=True
    )


def create_improved_synthesis_task(
    chunks: List[ImprovedChunk],
    document_title: str,
    content_type: ContentType,
    synthesizer_agent: Agent
) -> Task:
    """Create synthesis task that preserves content essence."""
    
    # Build context about what we're synthesizing
    chunk_contexts = set(chunk.context_type for chunk in chunks)
    chunk_tones = set(chunk.tone for chunk in chunks)
    
    content_type_descriptions = {
        ContentType.ACADEMIC_PAPER: "research study",
        ContentType.BLOG_POST: "blog post",
        ContentType.NEWS_ARTICLE: "news article", 
        ContentType.TECHNICAL_DOCUMENTATION: "technical documentation",
        ContentType.BOOK_CHAPTER: "book chapter",
        ContentType.GENERAL_TEXT: "written work"
    }
    
    content_description = content_type_descriptions.get(content_type, "content")
    
    # Synthesis approach based on content type
    synthesis_approaches = {
        ContentType.ACADEMIC_PAPER: """
        - Thread together the research journey from problem to solution
        - Highlight methodological choices and their implications
        - Connect findings to broader scientific context
        - Preserve the logical flow of argumentation
        - Note limitations and future directions""",
        
        ContentType.BLOG_POST: """
        - Maintain the conversational flow and personal voice
        - Preserve anecdotes, examples, and stylistic flourishes
        - Keep the narrative arc intact
        - Highlight practical takeaways and personal insights
        - Retain the author's personality and perspective""",
        
        ContentType.NEWS_ARTICLE: """
        - Preserve the journalistic structure (lead, body, context)
        - Maintain the factual progression and timeline
        - Keep quotes and attributions in context
        - Note any bias or framing in the reporting
        - Highlight the broader implications of the news""",
        
        ContentType.TECHNICAL_DOCUMENTATION: """
        - Organize concepts from basic to advanced
        - Preserve all technical specifications and parameters
        - Keep code examples and their explanations connected
        - Maintain the logical flow of instructions
        - Highlight dependencies and prerequisites""",
        
        ContentType.BOOK_CHAPTER: """
        - Preserve the chapter's role in the larger narrative
        - Maintain thematic development and callbacks
        - Keep character or concept evolution clear
        - Note literary devices and stylistic choices
        - Connect to overarching book themes""",
        
        ContentType.GENERAL_TEXT: """
        - Identify and preserve the core narrative structure
        - Maintain the author's unique perspective
        - Keep key examples and illustrations
        - Preserve the emotional or intellectual journey
        - Note what makes this piece distinctive"""
    }
    
    approach = synthesis_approaches.get(content_type, synthesis_approaches[ContentType.GENERAL_TEXT])
    
    # Build the synthesis task
    task_description = f"""
You have received detailed analyses of all {len(chunks)} sections of the {content_description} titled "{document_title}".

CRITICAL: This is a {content_description}, NOT a generic "paper" or "document". Treat it as such throughout your synthesis.

Content Overview:
- Type: {content_description}
- Sections analyzed: {', '.join(sorted(chunk_contexts))}
- Tones detected: {', '.join(sorted(chunk_tones))}
- Total sections: {len(chunks)}

YOUR SYNTHESIS MISSION:

1. **Preserve the Content's True Nature**
   - This is a {content_description} - refer to it as such
   - Don't impose academic framing on non-academic content
   - Keep the original work's character and voice alive

2. **START WITH A TLDR (CRITICAL REQUIREMENT)**
   Begin your synthesis with "TLDR:" followed by 3-5 bullet points:
   - The main argument, discovery, or message in one clear sentence
   - 2-3 key insights, findings, or takeaways
   - The primary implication or "so what?" factor
   
   Make the TLDR punchy and memorable - it should make someone want to read more.

3. **Build Multi-Dimensional Understanding** (After the TLDR)
   - WHAT: The core ideas, facts, and information
   - HOW: The way ideas are presented and developed
   - WHY: The purpose, motivation, and significance
   - WHO: The voice, perspective, and intended audience

4. **Synthesis Approach for {content_description}**:
   {approach}

5. **Create Natural Connections**
   - Show how different sections build on each other
   - Identify recurring themes and evolving ideas
   - Note contrasts, tensions, or contradictions
   - Highlight unique insights that emerge from the whole

6. **Preserve Original Spirit**
   - If it's conversational, keep that warmth
   - If it's technical, maintain that precision
   - If it's narrative, preserve that flow
   - If it's analytical, retain that rigor

7. **Write for Understanding**
   - Someone reading your synthesis should feel like they've engaged with the original
   - Include specific examples, quotes, or details that capture essence
   - Don't just report what was said - convey how and why it matters

REMEMBER: You're not writing a book report. You're creating a rich, faithful representation
of {content_description} that preserves both its intellectual content and its essential character.

Write your synthesis as if you're sharing the fascinating insights from this {content_description}
with someone who wants to truly understand it, not just know about it.

Focus on making the IDEAS and INSIGHTS come alive, not on documenting that you read something.
"""
    
    return Task(
        description=task_description,
        agent=synthesizer_agent,
        expected_output=f"A comprehensive, authentic synthesis of the {content_description} that preserves its essence"
    )


def create_chunk_analysis_prompt_improved(
    chunk: ImprovedChunk,
    document_title: str,
    content_type: ContentType
) -> str:
    """Create an improved prompt for chunk analysis."""
    
    content_type_descriptions = {
        ContentType.ACADEMIC_PAPER: "research study",
        ContentType.BLOG_POST: "blog post",
        ContentType.NEWS_ARTICLE: "news article",
        ContentType.TECHNICAL_DOCUMENTATION: "technical guide",
        ContentType.BOOK_CHAPTER: "book chapter",
        ContentType.GENERAL_TEXT: "piece"
    }
    
    content_desc = content_type_descriptions.get(content_type, "content")
    
    # Specific extraction goals by content type
    extraction_goals = {
        ContentType.ACADEMIC_PAPER: """
        - Research questions and hypotheses
        - Methodological details and justifications
        - Specific findings with data
        - Theoretical contributions
        - Limitations acknowledged""",
        
        ContentType.BLOG_POST: """
        - Main message or story
        - Personal insights and experiences
        - Practical tips or advice
        - Engaging examples or anecdotes
        - Author's unique perspective""",
        
        ContentType.NEWS_ARTICLE: """
        - Key facts (who, what, when, where, why)
        - Sources and attributions
        - Context and background
        - Multiple perspectives presented
        - Implications or future developments""",
        
        ContentType.TECHNICAL_DOCUMENTATION: """
        - Concepts being explained
        - Step-by-step procedures
        - Code examples and outputs
        - Common issues and solutions
        - Best practices highlighted""",
        
        ContentType.GENERAL_TEXT: """
        - Central ideas and arguments
        - Supporting evidence or examples
        - Unique insights or perspectives
        - Connections to broader themes
        - Memorable phrases or concepts"""
    }
    
    goals = extraction_goals.get(content_type, extraction_goals[ContentType.GENERAL_TEXT])
    
    # Context-aware instructions
    if chunk.context_type == "introduction":
        context_focus = "Pay special attention to how the topic is framed and why it matters."
    elif chunk.context_type == "conclusion":
        context_focus = "Focus on key takeaways, future implications, and closing thoughts."
    elif chunk.context_type == "methodology":
        context_focus = "Extract specific methods, tools, and procedural details."
    elif chunk.context_type == "results":
        context_focus = "Capture specific findings, data points, and outcomes."
    elif chunk.context_type == "example":
        context_focus = "Preserve the example in detail - it illuminates the broader concept."
    else:
        context_focus = "Extract the core contributions of this section."
    
    return f"""
Analyze this {chunk.context_type.replace('_', ' ')} section from the {content_desc}: "{document_title}"

This is part {chunk.chunk_index + 1} of {chunk.total_chunks} from a {content_desc}.
The tone is {chunk.tone}.

{context_focus}

Extract and preserve these elements from this {content_desc}:
{goals}

CRITICAL INSTRUCTIONS:
1. Write about the IDEAS, not about "the document" or "the author"
2. If this is a {chunk.tone} {content_desc}, maintain that {chunk.tone} character
3. Include specific details that make this section unique and valuable
4. Note HOW things are communicated, not just what
5. Preserve any distinctive voice, style, or perspective

Content:
{chunk.content}

Provide a rich extraction that captures both the information AND the spirit of this section.
Write as if you're sharing fascinating insights, not filing a report.
"""


class ImprovedSynthesisManager:
    """Manages the improved synthesis process."""
    
    def __init__(self, llm):
        self.llm = llm
        self.content_analyzer = create_content_analyzer_agent(llm)
        self.synthesis_architect = create_synthesis_architect_agent(llm)
    
    def run_synthesis(
        self,
        chunks: List[ImprovedChunk],
        document_title: str,
        content_type: ContentType
    ) -> Dict[str, Any]:
        """Run the improved synthesis process."""
        
        # Create chunk analysis tasks
        chunk_tasks = []
        for chunk in chunks:
            task = Task(
                description=create_chunk_analysis_prompt_improved(
                    chunk, document_title, content_type
                ),
                agent=self.content_analyzer,
                expected_output=f"Rich analysis of {chunk.context_type} section preserving its essence"
            )
            chunk_tasks.append(task)
        
        # Create synthesis task
        synthesis_task = create_improved_synthesis_task(
            chunks, document_title, content_type, self.synthesis_architect
        )
        
        # Build crew
        crew = Crew(
            agents=[self.content_analyzer, self.synthesis_architect],
            tasks=chunk_tasks + [synthesis_task],
            verbose=True
        )
        
        # Run synthesis
        result = crew.kickoff()
        
        return {
            "synthesis": str(result),
            "content_type": content_type.value,
            "chunks_analyzed": len(chunks),
            "document_title": document_title
        }