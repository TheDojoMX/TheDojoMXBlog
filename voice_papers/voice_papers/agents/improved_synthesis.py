"""Improved synthesis agents that preserve content spirit."""

from typing import List, Dict, Any
import json
from crewai import Agent, Task, Crew
from ..utils.improved_chunker import ContentType, ImprovedChunk


def create_content_analyzer_agent(llm) -> Agent:
    """Create an agent that extracts actual content from sections."""
    return Agent(
        role="Content Extractor",
        goal="Extract the actual ideas, concepts, arguments and findings from each content section",
        backstory="""You are an expert at extracting the substance from content. You focus on:
        - The actual ideas being presented
        - Specific concepts and how they work
        - Arguments and the evidence supporting them
        - Concrete findings and results
        - Real examples and applications
        
        You NEVER talk about how content is presented or written. You extract WHAT is said,
        not HOW it's said. You present ideas directly as if explaining them yourself.""",
        llm=llm,
        verbose=True
    )


def create_synthesis_architect_agent(llm) -> Agent:
    """Create an agent that builds comprehensive content synthesis."""
    return Agent(
        role="Content Synthesizer",
        goal="Create a comprehensive synthesis that directly presents the ideas, concepts and findings",
        backstory="""You are excellent at synthesizing complex content into clear, direct explanations.
        You focus exclusively on:
        - Presenting the main ideas and concepts
        - Explaining how things work
        - Listing findings and conclusions
        - Providing supporting arguments and evidence
        - Including relevant examples
        
        You NEVER describe writing style, tone, or presentation. You present content AS IF YOU
        ARE THE EXPERT explaining these ideas directly. No meta-commentary.""",
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
    
    # Content extraction approach based on type
    synthesis_approaches = {
        ContentType.ACADEMIC_PAPER: """
        - State the research problem and hypotheses
        - Explain the methodology used
        - List all findings with specific data
        - Present the conclusions
        - Mention limitations and future work""",
        
        ContentType.BLOG_POST: """
        - Extract the main message or thesis
        - List key insights and lessons
        - Include specific examples mentioned
        - Note practical applications
        - Capture any unique perspectives""",
        
        ContentType.NEWS_ARTICLE: """
        - State what happened (who, what, when, where, why)
        - List key facts and figures
        - Include important quotes
        - Note context and background
        - Mention implications""",
        
        ContentType.TECHNICAL_DOCUMENTATION: """
        - List concepts being explained
        - Include technical specifications
        - Present code examples as given
        - State step-by-step procedures
        - Note requirements and dependencies""",
        
        ContentType.BOOK_CHAPTER: """
        - Summarize key events or concepts
        - List main ideas presented
        - Note important developments
        - Include key examples
        - State conclusions reached""",
        
        ContentType.GENERAL_TEXT: """
        - Extract main ideas and arguments
        - List supporting evidence
        - Include examples provided
        - Note key insights
        - State conclusions"""
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

1. **EXTRACT AND PLACE THE TITLE (CRITICAL - FIRST LINE)**
   - Extract the actual title of the {content_description} from the content
   - If no explicit title is found, create a descriptive title based on the main topic
   - Place this as the VERY FIRST LINE of your synthesis
   - Format: Just the title text, no quotes or "Title:" prefix

2. **Extract Actual Content**
   - Present ideas, concepts, and findings directly
   - NO meta-analysis about writing style or presentation
   - State facts and arguments as if you're the expert

3. **START WITH A TLDR (CRITICAL REQUIREMENT - AFTER TITLE)**
   After the title, begin with "TLDR:" followed by 3-5 bullet points:
   - The main finding, concept, or thesis
   - 2-3 key supporting points or discoveries
   - The primary conclusion or application
   
   Be direct and factual - state what the content says.

4. **Main Content Sections** (After TLDR, max 5 sentences per section)
   
   **Brief Description** (2-3 sentences max):
   - What this content is about
   - Its main purpose or goal
   
   **Key Concepts Explained**:
   - Define and explain main concepts
   - How these concepts work or relate
   
   **Main Ideas and Arguments**:
   - List the primary claims or findings
   - Include supporting evidence for each
   - Use specific data, examples, or reasoning provided
   
   **Conclusions**:
   - Final conclusions or recommendations
   - Practical applications or implications

5. **Content Extraction for {content_description}**:
   {approach}

6. **Critical Rules**:
   - NEVER say "the author discusses" or "the paper presents"
   - NEVER describe tone, style, or writing quality
   - NEVER give opinions about the content
   - ALWAYS present ideas directly: "X is Y" not "The author argues X is Y"
   - ALWAYS use specific examples and data from the content

REMEMBER: You're extracting and presenting the actual content, not describing it.

EXAMPLE SYNTHESIS START:
Advanced Machine Learning Approaches for Real-Time Data Processing

TLDR:
- Three novel approaches enable 10x faster real-time processing
- Hybrid architectures combine supervised and unsupervised methods effectively
- Applications show 87% accuracy improvement in production systems
- New framework reduces computational costs by 60%

[Rest of synthesis follows...]

WRONG: "The paper discusses three approaches to machine learning"
RIGHT: "The three approaches to machine learning are: 1) Supervised learning uses labeled data... 2) Unsupervised learning finds patterns... 3) Reinforcement learning optimizes rewards..."

Present the content AS THE CONTENT, not as a description of content.
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
1. Extract and present the actual IDEAS, concepts, and findings
2. NEVER mention "the document", "the author", or how things are written
3. Include specific data, examples, and evidence from this section
4. Present information directly as facts, not as "the author's claims"
5. Focus ONLY on WHAT is said, never on HOW it's communicated

Content:
{chunk.content}

Extract the key information from this section. Present it directly and factually.
Do not describe or analyze the writing - just extract the content itself.
"""


def create_knowledge_graph_extractor_agent(llm) -> Agent:
    """Create an agent that extracts knowledge graph from content."""
    return Agent(
        role="Knowledge Graph Builder",
        goal="Extract entities, concepts, and relationships to build a knowledge graph",
        backstory="""You are an expert at identifying key concepts, entities, and their relationships
        in content. You build structured knowledge representations that capture the essence of
        complex information in a graph format.""",
        llm=llm,
        verbose=True
    )


class ImprovedSynthesisManager:
    """Manages the improved synthesis process."""
    
    def __init__(self, llm):
        self.llm = llm
        self.content_analyzer = create_content_analyzer_agent(llm)
        self.synthesis_architect = create_synthesis_architect_agent(llm)
        self.knowledge_graph_extractor = create_knowledge_graph_extractor_agent(llm)
    
    def run_concatenation_synthesis(
        self,
        chunks: List[ImprovedChunk],
        document_title: str,
        content_type: ContentType
    ) -> Dict[str, Any]:
        """Run synthesis by concatenating chunk extractions without compression."""
        
        # Create chunk extraction tasks
        chunk_results = []
        for i, chunk in enumerate(chunks):
            task = Task(
                description=create_chunk_analysis_prompt_improved(
                    chunk, document_title, content_type
                ),
                agent=self.content_analyzer,
                expected_output=f"Direct extraction of content from {chunk.context_type} section"
            )
            
            # Create a mini crew for each chunk
            chunk_crew = Crew(
                agents=[self.content_analyzer],
                tasks=[task],
                verbose=False
            )
            
            result = chunk_crew.kickoff()
            # ImprovedChunk doesn't have section_title, use context_type instead
            section_name = getattr(chunk, 'section_title', None) or f"{chunk.context_type.title()} (Part {i+1})"
            chunk_results.append({
                "section": section_name,
                "type": chunk.context_type,
                "content": str(result)
            })
        
        # Create final formatting task
        formatting_prompt = f"""
        You have extracted content from {len(chunks)} sections. Now organize them into a coherent summary.
        
        DO NOT COMPRESS OR SYNTHESIZE FURTHER. Simply organize the extracted content logically.
        
        CRITICAL: Start with the document title as the VERY FIRST LINE, then TLDR section, then content.
        
        Sections to organize:
        {json.dumps(chunk_results, indent=2)}
        
        Format as:
        
        {document_title}
        
        TLDR:
        • [Main finding/concept]
        • [Key supporting points]
        • [Primary conclusion]
        
        Then organize all content by logical grouping (methodology, findings, examples, etc.)
        """
        
        formatting_task = Task(
            description=formatting_prompt,
            agent=self.synthesis_architect,
            expected_output="Organized presentation of all extracted content"
        )
        
        final_crew = Crew(
            agents=[self.synthesis_architect],
            tasks=[formatting_task],
            verbose=True
        )
        
        final_result = final_crew.kickoff()
        
        return {
            "synthesis": str(final_result),
            "content_type": content_type.value,
            "chunks_analyzed": len(chunks),
            "document_title": document_title,
            "method": "concatenation"
        }
    
    def run_knowledge_graph_synthesis(
        self,
        chunks: List[ImprovedChunk],
        document_title: str,
        content_type: ContentType
    ) -> Dict[str, Any]:
        """Run synthesis by first extracting a knowledge graph."""
        
        # First pass: Extract knowledge graph
        kg_prompt = f"""
        Analyze this {content_type.value} titled "{document_title}" and extract a knowledge graph.
        
        Create a JSON structure with:
        {{
            "main_concepts": [
                {{
                    "name": "concept name",
                    "definition": "what it is",
                    "properties": ["key properties"],
                    "examples": ["specific examples"]
                }}
            ],
            "relationships": [
                {{
                    "from": "concept1",
                    "to": "concept2",
                    "type": "relationship type",
                    "description": "how they relate"
                }}
            ],
            "findings": [
                {{
                    "statement": "the finding",
                    "evidence": "supporting data",
                    "implications": "what it means"
                }}
            ],
            "methodology": {{
                "approach": "method used",
                "steps": ["step1", "step2"],
                "tools": ["tools/techniques used"]
            }},
            "applications": [
                {{
                    "use_case": "application",
                    "benefit": "why it's useful",
                    "example": "specific instance"
                }}
            ]
        }}
        
        Content chunks:
        {[chunk.content for chunk in chunks]}
        """
        
        kg_task = Task(
            description=kg_prompt,
            agent=self.knowledge_graph_extractor,
            expected_output="Knowledge graph in JSON format"
        )
        
        kg_crew = Crew(
            agents=[self.knowledge_graph_extractor],
            tasks=[kg_task],
            verbose=True
        )
        
        kg_result = kg_crew.kickoff()
        
        # Second pass: Convert knowledge graph to natural synthesis
        synthesis_prompt = f"""
        Convert this knowledge graph into a natural, readable synthesis.
        
        Knowledge Graph:
        {kg_result}
        
        Create a synthesis that:
        1. FIRST LINE: Place the document title "{document_title}" as the very first line
        2. Starts with TLDR (3-5 bullet points) - AFTER the title
        3. Explains main concepts clearly
        4. Presents findings with evidence
        5. Includes methodology if relevant
        6. Lists applications and examples
        
        CRITICAL: Present the actual content, not descriptions of it.
        Write as if you're teaching these concepts directly.
        """
        
        synthesis_task = Task(
            description=synthesis_prompt,
            agent=self.synthesis_architect,
            expected_output="Natural synthesis from knowledge graph"
        )
        
        final_crew = Crew(
            agents=[self.synthesis_architect],
            tasks=[synthesis_task],
            verbose=True
        )
        
        final_result = final_crew.kickoff()
        
        return {
            "synthesis": str(final_result),
            "knowledge_graph": str(kg_result),
            "content_type": content_type.value,
            "chunks_analyzed": len(chunks),
            "document_title": document_title,
            "method": "knowledge_graph"
        }
    
    def run_synthesis(
        self,
        chunks: List[ImprovedChunk],
        document_title: str,
        content_type: ContentType,
        method: str = "concatenation",
        generate_knowledge_graph: bool = True
    ) -> Dict[str, Any]:
        """Run synthesis using the specified method."""
        if method == "knowledge_graph":
            return self.run_knowledge_graph_synthesis(chunks, document_title, content_type)
        elif method == "concatenation" and generate_knowledge_graph:
            # Generate both concatenation and knowledge graph
            concat_result = self.run_concatenation_synthesis(chunks, document_title, content_type)
            kg_result = self.run_knowledge_graph_synthesis(chunks, document_title, content_type)
            
            # Combine results
            return {
                "synthesis": concat_result["synthesis"],
                "knowledge_graph": kg_result["knowledge_graph"],
                "content_type": content_type.value,
                "chunks_analyzed": len(chunks),
                "document_title": document_title,
                "method": "concatenation_with_kg"
            }
        else:
            return self.run_concatenation_synthesis(chunks, document_title, content_type)