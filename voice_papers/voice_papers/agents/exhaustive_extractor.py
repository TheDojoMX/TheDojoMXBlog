"""Exhaustive content extractor for complete information preservation."""

from typing import List, Dict, Any, Tuple, Set
from crewai import Agent, Task
import re
import json


def create_exhaustive_extractor_agent(llm) -> Agent:
    """Create an agent focused on extracting ALL information from content."""
    return Agent(
        role="Exhaustive Content Extractor",
        goal="Extract and preserve EVERY piece of information, concept, detail, and nuance from the content",
        backstory="""You are a meticulous information extractor with an obsessive attention to detail.
        Your mission is to ensure NOTHING is lost from the original content. You:
        
        - Extract every fact, figure, and data point
        - Preserve all technical specifications and formulas
        - Capture complete methodologies and procedures
        - Include all examples, case studies, and applications
        - Maintain all arguments with their supporting evidence
        - Document limitations, assumptions, and future work
        - Keep all references and citations
        
        You NEVER summarize or condense. You expand and explain while preserving everything.
        If something seems minor, you still include it. Your output is comprehensive, not concise.""",
        llm=llm,
        verbose=True,
        max_iter=3,
    )


def create_structure_mapper_agent(llm) -> Agent:
    """Create an agent that maps the complete structure of the document."""
    return Agent(
        role="Document Structure Analyst",
        goal="Map the complete hierarchical structure and logical flow of the document",
        backstory="""You are an expert at understanding document architecture. You identify:
        
        - Main sections and subsections
        - Logical flow and connections between parts
        - Key transitions and relationships
        - Document type and genre conventions
        - Implicit structure in unstructured text
        
        You create a complete map that ensures no section is overlooked.""",
        llm=llm,
        verbose=True,
    )


def create_concept_extractor_agent(llm) -> Agent:
    """Create an agent that extracts all concepts and their relationships."""
    return Agent(
        role="Concept and Theory Extractor",
        goal="Identify and extract ALL concepts, theories, definitions, and their relationships",
        backstory="""You specialize in identifying every concept mentioned in academic and technical content.
        
        You extract:
        - Every defined term and its complete definition
        - All theories and frameworks mentioned
        - Conceptual relationships and dependencies
        - Technical terminology with explanations
        - Domain-specific knowledge
        - Implicit concepts that are referenced but not defined
        
        You ensure the reader will understand every single concept mentioned.""",
        llm=llm,
        verbose=True,
    )


def create_evidence_gatherer_agent(llm) -> Agent:
    """Create an agent that gathers all evidence, data, and examples."""
    return Agent(
        role="Evidence and Data Gatherer",
        goal="Collect ALL data points, evidence, examples, and supporting materials",
        backstory="""You are a forensic evidence collector for academic content. You gather:
        
        - Every number, statistic, and measurement
        - All experimental results and observations
        - Complete examples and case studies
        - Every piece of supporting evidence
        - All figures, tables, and chart data
        - Code snippets and algorithms
        - Quotes and testimonials
        
        Nothing is too small or insignificant. You preserve the complete evidence base.""",
        llm=llm,
        verbose=True,
    )


def create_methodology_expert_agent(llm) -> Agent:
    """Create an agent specialized in extracting methodologies and procedures."""
    return Agent(
        role="Methodology and Process Expert",
        goal="Extract complete methodologies, procedures, and implementation details",
        backstory="""You specialize in understanding and documenting how things are done. You extract:
        
        - Complete research methodologies
        - Step-by-step procedures
        - Implementation details
        - Experimental setups
        - Analysis techniques
        - Tools and technologies used
        - Validation methods
        - Reproducibility information
        
        You ensure someone could replicate or understand the complete process.""",
        llm=llm,
        verbose=True,
    )


def create_insight_synthesizer_agent(llm) -> Agent:
    """Create an agent that extracts all insights, conclusions, and implications."""
    return Agent(
        role="Insight and Implication Analyzer",
        goal="Extract ALL conclusions, insights, implications, and future directions",
        backstory="""You identify and elaborate on every insight and implication in the content:
        
        - All stated conclusions
        - Implicit insights
        - Practical applications
        - Theoretical implications
        - Future research directions
        - Limitations and caveats
        - Open questions
        - Connections to other work
        
        You ensure no insight or implication is missed.""",
        llm=llm,
        verbose=True,
    )


class MultiPassAnalyzer:
    """Orchestrates multi-pass analysis for comprehensive extraction."""
    
    def __init__(self, llm):
        self.llm = llm
        self.structure_mapper = create_structure_mapper_agent(llm)
        self.concept_extractor = create_concept_extractor_agent(llm)
        self.evidence_gatherer = create_evidence_gatherer_agent(llm)
        self.methodology_expert = create_methodology_expert_agent(llm)
        self.insight_synthesizer = create_insight_synthesizer_agent(llm)
        self.exhaustive_extractor = create_exhaustive_extractor_agent(llm)
    
    def analyze_content_type(self, content: str, title: str) -> Dict[str, Any]:
        """Analyze content to determine type and characteristics."""
        # Look for indicators of content type
        indicators = {
            'research_paper': [
                'abstract', 'methodology', 'results', 'conclusion',
                'hypothesis', 'experiment', 'findings', 'discussion'
            ],
            'technical_doc': [
                'installation', 'configuration', 'api', 'function',
                'parameter', 'usage', 'example', 'syntax'
            ],
            'blog_post': [
                'posted', 'update', 'thoughts', 'opinion',
                'recently', 'today', 'personal', 'experience'
            ],
            'tutorial': [
                'step', 'how to', 'guide', 'learn',
                'beginner', 'advanced', 'exercise', 'practice'
            ],
            'analysis': [
                'analysis', 'review', 'comparison', 'evaluation',
                'assessment', 'critique', 'examination'
            ]
        }
        
        content_lower = content.lower()
        scores = {}
        
        for content_type, keywords in indicators.items():
            score = sum(1 for keyword in keywords if keyword in content_lower)
            scores[content_type] = score
        
        # Determine primary type
        primary_type = max(scores, key=scores.get) if max(scores.values()) > 0 else 'general'
        
        # Check for specific sections
        has_methodology = any(term in content_lower for term in ['methodology', 'method', 'approach', 'procedure'])
        has_results = any(term in content_lower for term in ['results', 'findings', 'outcomes', 'data'])
        has_code = bool(re.search(r'```|def |class |function |import |{.*}|\[.*\]', content))
        has_formulas = bool(re.search(r'[∑∫∂∇×·]|\\[a-zA-Z]+|[\^_]{|E=|F=|P\(', content))
        
        return {
            'primary_type': primary_type,
            'has_methodology': has_methodology,
            'has_results': has_results,
            'has_code': has_code,
            'has_formulas': has_formulas,
            'complexity': self._assess_complexity(content),
            'topics': self._extract_main_topics(content, title)
        }
    
    def _assess_complexity(self, content: str) -> str:
        """Assess content complexity level."""
        # Simple heuristic based on technical terms and sentence structure
        technical_terms = len(re.findall(r'\b[A-Z][a-z]+[A-Z]\w*\b|\b\w+ization\b|\b\w+ivity\b', content))
        avg_sentence_length = len(content.split()) / max(len(content.split('.')), 1)
        
        if technical_terms > 50 or avg_sentence_length > 25:
            return 'high'
        elif technical_terms > 20 or avg_sentence_length > 18:
            return 'medium'
        else:
            return 'low'
    
    def _extract_main_topics(self, content: str, title: str) -> List[str]:
        """Extract main topics from content."""
        # Combine title and content for topic extraction
        text = f"{title} {content[:2000]}"  # Use first 2000 chars for efficiency
        
        # Extract capitalized phrases (likely important concepts)
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        # Extract technical terms
        technical = re.findall(r'\b(?:algorithm|model|system|framework|method|technique|approach|analysis|theory)\b', text.lower())
        
        # Combine and deduplicate
        topics = list(set(capitalized[:10] + technical[:5]))  # Limit for performance
        
        return topics
    
    def run_multi_pass_analysis(self, content: str, title: str) -> Dict[str, Any]:
        """Run comprehensive multi-pass analysis on content."""
        
        # First, analyze content characteristics
        content_analysis = self.analyze_content_type(content, title)
        
        results = {
            'content_analysis': content_analysis,
            'passes': {}
        }
        
        # Pass 1: Structure Mapping
        structure_task = Task(
            description=f"""
            Analyze the complete structure of this document titled "{title}".
            
            Map out:
            1. All main sections and subsections
            2. The logical flow and progression
            3. How different parts connect
            4. Any implicit structure in the text
            5. Key transition points
            
            Content to analyze:
            {content[:5000]}  # First 5000 chars for structure
            
            Provide a complete structural map that ensures nothing is overlooked.
            """,
            agent=self.structure_mapper,
            expected_output="Complete hierarchical structure map of the document"
        )
        
        # Pass 2: Concept Extraction
        concept_task = Task(
            description=f"""
            Extract EVERY concept, theory, and definition from this document.
            
            Include:
            1. All defined terms with complete definitions
            2. Every theory or framework mentioned
            3. Conceptual relationships
            4. Technical terminology
            5. Domain-specific knowledge
            6. Implicit concepts that are referenced
            
            Content to analyze:
            {content}
            
            Ensure you capture EVERY single concept for complete understanding.
            """,
            agent=self.concept_extractor,
            expected_output="Comprehensive list of all concepts with explanations"
        )
        
        # Pass 3: Evidence Gathering
        evidence_task = Task(
            description=f"""
            Gather ALL evidence, data, and examples from this document.
            
            Collect:
            1. Every number, statistic, percentage
            2. All experimental results
            3. Complete examples and case studies
            4. All supporting evidence
            5. Data from figures and tables
            6. Code snippets and algorithms
            7. Quotes and references
            
            Content to analyze:
            {content}
            
            Nothing is too small. Preserve the complete evidence base.
            """,
            agent=self.evidence_gatherer,
            expected_output="Complete collection of all evidence and data"
        )
        
        # Pass 4: Methodology Extraction (if applicable)
        if content_analysis['has_methodology']:
            methodology_task = Task(
                description=f"""
                Extract the complete methodology and procedures from this document.
                
                Document:
                1. Research methodology
                2. Step-by-step procedures
                3. Implementation details
                4. Experimental setup
                5. Analysis techniques
                6. Tools and technologies
                7. Validation methods
                
                Content to analyze:
                {content}
                
                Ensure someone could replicate or fully understand the process.
                """,
                agent=self.methodology_expert,
                expected_output="Complete methodology documentation"
            )
            results['passes']['methodology'] = methodology_task
        
        # Pass 5: Insight Synthesis
        insight_task = Task(
            description=f"""
            Extract ALL insights, conclusions, and implications from this document.
            
            Identify:
            1. All stated conclusions
            2. Implicit insights
            3. Practical applications
            4. Theoretical implications
            5. Future directions
            6. Limitations and caveats
            7. Open questions
            8. Connections to other work
            
            Content to analyze:
            {content}
            
            Ensure no insight or implication is missed.
            """,
            agent=self.insight_synthesizer,
            expected_output="Complete synthesis of all insights and implications"
        )
        
        results['passes']['structure'] = structure_task
        results['passes']['concepts'] = concept_task
        results['passes']['evidence'] = evidence_task
        results['passes']['insights'] = insight_task
        
        return results


def create_comprehensive_extraction_task(
    content: str,
    title: str,
    extractor_agent: Agent,
    multi_pass_results: Dict[str, Any],
    language: str = "English"
) -> Task:
    """Create a task for comprehensive content extraction."""
    
    # Build comprehensive context from multi-pass analysis
    content_type = multi_pass_results['content_analysis']['primary_type']
    complexity = multi_pass_results['content_analysis']['complexity']
    topics = multi_pass_results['content_analysis']['topics']
    
    task_description = f"""
    Create a COMPREHENSIVE extraction of ALL information from this {content_type} titled "{title}".
    
    CRITICAL REQUIREMENTS:
    
    1. **COMPLETENESS IS MANDATORY**
       - Include EVERY fact, concept, and detail
       - NO summarization or condensation
       - If in doubt, include it
       - Better to be exhaustive than concise
    
    2. **PRESERVE ALL TECHNICAL CONTENT**
       - Keep all formulas and equations
       - Include all code snippets
       - Maintain all data and statistics
       - Document all methodologies
    
    3. **EXPAND AND EXPLAIN**
       - Add explanations for complex concepts
       - Provide context for technical terms
       - Clarify implicit assumptions
       - Connect related ideas
    
    4. **STRUCTURE FOR COMPREHENSION**
       - Organize logically following source structure
       - Use clear headings and sections
       - Maintain relationships between concepts
       - Ensure smooth flow of ideas
    
    5. **EVIDENCE-BASED PRESENTATION**
       - Include all examples
       - Keep all supporting data
       - Maintain all references
       - Preserve all case studies
    
    Content Analysis:
    - Type: {content_type}
    - Complexity: {complexity}
    - Main Topics: {', '.join(topics[:10])}
    - Has Methodology: {multi_pass_results['content_analysis']['has_methodology']}
    - Has Code: {multi_pass_results['content_analysis']['has_code']}
    - Has Formulas: {multi_pass_results['content_analysis']['has_formulas']}
    
    Source Content:
    {content}
    
    TARGET LANGUAGE: {language}
    
    Remember: Your goal is to ensure the reader understands EVERYTHING from the original,
    not just the highlights. Be comprehensive, not concise.
    """
    
    return Task(
        description=task_description,
        agent=extractor_agent,
        expected_output=f"Complete, exhaustive extraction of all content in {language}"
    )


class CoverageVerifier:
    """Verifies that extracted content covers all original material."""
    
    def __init__(self, llm):
        self.llm = llm
    
    def extract_key_elements(self, text: str) -> Set[str]:
        """Extract key elements from text for comparison."""
        elements = set()
        
        # Extract numbers and statistics
        numbers = re.findall(r'\b\d+(?:\.\d+)?%?\b', text)
        elements.update(numbers)
        
        # Extract technical terms (capitalized words, acronyms)
        technical = re.findall(r'\b[A-Z][A-Za-z]+\b|\b[A-Z]{2,}\b', text)
        elements.update(technical)
        
        # Extract quoted text
        quotes = re.findall(r'"([^"]+)"|\'([^\']+)\'', text)
        elements.update([q[0] or q[1] for q in quotes])
        
        # Extract formulas and equations (simplified)
        formulas = re.findall(r'[A-Z]\s*=\s*[^\.]+', text)
        elements.update(formulas)
        
        return elements
    
    def verify_coverage(self, original: str, extracted: str) -> Dict[str, Any]:
        """Verify that extraction covers all original content."""
        original_elements = self.extract_key_elements(original)
        extracted_elements = self.extract_key_elements(extracted)
        
        missing_elements = original_elements - extracted_elements
        coverage_percentage = (len(extracted_elements & original_elements) / 
                             max(len(original_elements), 1)) * 100
        
        # Check for specific content types
        checks = {
            'has_all_numbers': all(num in extracted for num in re.findall(r'\b\d+(?:\.\d+)?%?\b', original)),
            'has_technical_terms': len(extracted_elements & original_elements) > len(original_elements) * 0.8,
            'is_longer': len(extracted.split()) >= len(original.split()) * 0.8,  # Should be at least 80% as long
            'coverage_percentage': coverage_percentage
        }
        
        return {
            'missing_elements': list(missing_elements)[:20],  # First 20 missing elements
            'coverage_checks': checks,
            'is_comprehensive': coverage_percentage > 85 and checks['has_all_numbers']
        }
    
    def create_completion_task(self, missing_elements: List[str], partial_extraction: str, agent: Agent) -> Task:
        """Create a task to complete extraction with missing elements."""
        task_description = f"""
        The following extraction is missing important elements. Please complete it by adding:
        
        Missing Elements:
        {chr(10).join(f'- {element}' for element in missing_elements)}
        
        Current Extraction:
        {partial_extraction}
        
        Add the missing information while maintaining the flow and structure.
        Expand on these elements with full context and explanation.
        """
        
        return Task(
            description=task_description,
            agent=agent,
            expected_output="Completed extraction with all missing elements included"
        )