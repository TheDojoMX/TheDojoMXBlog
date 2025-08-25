"""Crew management and orchestration."""

import os
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from crewai import Crew, Task, Agent
from crewai.llm import LLM
from ..config import OPENAI_API_KEY, MODEL_NAME, PROJECTS_DIR
from .roles import get_roles_for_topic
from .o3_llm import O3LLM
from .tts_optimizer import get_tts_optimizer_agent, create_tts_optimization_task
from .focus_agents import get_focus_agents, get_focus_specific_prompts
from .technical_writer import get_technical_writer_agent, create_technical_writing_task
from .light_editor import get_light_editor_agent, create_light_editing_task
from .conversational_enhancer import (
    get_conversational_enhancer_agent,
    create_conversational_enhancement_task,
)
from .exhaustive_extractor import (
    create_exhaustive_extractor_agent,
    MultiPassAnalyzer,
    create_comprehensive_extraction_task,
    CoverageVerifier,
)
from .dynamic_agent_generator import DynamicAgentGenerator
from .prompts.comprehensive_prompts import ComprehensivePrompts

# Import centralized prompts
from .prompts import (
    PromptComposer,
    SystemPrompts,
    TaskPrompts,
    StyleGuides,
    Constraints
)


class CrewManager:
    """Manages the CrewAI setup and execution."""

    def __init__(
        self,
        language: str = "English",
        project_name: str = "default",
        pdf_path: Path = None,
        technical_level: str = "accessible",
        duration_minutes: int = 5,
        conversation_mode: str = "enhanced",
        tone: str = "academic",
        focus: str = "explanatory",
        synthesis_method: str = "concatenation",
        generate_knowledge_graph: bool = True,
        depth: str = "comprehensive",  # New parameter for extraction depth
    ):
        self.language = language
        self.project_name = project_name
        self.technical_level = technical_level
        self.duration_minutes = duration_minutes
        self.conversation_mode = conversation_mode
        self.tone = tone
        self.focus = focus
        self.synthesis_method = synthesis_method
        self.generate_knowledge_graph = generate_knowledge_graph
        self.depth = depth  # Store extraction depth

        # If pdf_path is provided, create project in same directory as PDF
        if pdf_path:
            pdf_dir = pdf_path.parent
            self.project_dir = pdf_dir / project_name
        else:
            # Fallback to old behavior
            self.project_dir = PROJECTS_DIR / project_name

        self.discussion_dir = self.project_dir / "discussion"
        self.synthesis_dir = self.project_dir / "synthesis"

        # Create project directories
        self.project_dir.mkdir(parents=True, exist_ok=True)
        self.discussion_dir.mkdir(parents=True, exist_ok=True)
        self.synthesis_dir.mkdir(parents=True, exist_ok=True)

        # Use o3-mini with custom LLM wrapper that handles parameter restrictions
        self.llm = O3LLM(api_key=OPENAI_API_KEY, model="o3-mini")
        
        # Initialize prompt composer
        self.prompt_composer = PromptComposer()

    def _get_base_agents_for_focus(self) -> List[Agent]:
        """Get base agents for non-critical focus modes."""
        agents = []

        # Coordinator for all modes - using centralized prompts
        coordinator_backstory = self.prompt_composer.compose_agent_prompt(
            agent_type="research_coordinator",
            focus=self.focus,
            language=self.language,
            tone=self.tone
        )
        
        agents.append(
            Agent(
                role="Research Coordinator",
                goal="Facilitate productive discussion about the paper's content",
                backstory=coordinator_backstory,
                llm=self.llm,
                verbose=True,
            )
        )

        # Scientific Reviewer for explanatory modes - using centralized prompts
        if self.focus != "story":  # Story mode doesn't need scientific review
            methodology_backstory = self.prompt_composer.compose_agent_prompt(
                agent_type="methodology_explainer",
                focus=self.focus,
                language=self.language,
                tone=self.tone
            )
            
            agents.append(
                Agent(
                    role="Methodology Explainer",
                    goal="Explain the research methodology and approach as described in the paper",
                    backstory=methodology_backstory,
                    llm=self.llm,
                    verbose=True,
                )
            )

        # CRITICAL: Always include post-production agents
        # Use technical writer for technical focus, otherwise improved educational writer
        if self.focus == "technical":
            agents.append(get_technical_writer_agent(self.llm))
        else:
            from .improved_educational_writer import get_improved_educational_writer
            agents.append(get_improved_educational_writer(self.llm))

        # Comedy Communicator - only for humorous/playful tones
        if self.tone in ["humorous", "playful"]:
            comedy_backstory = self.prompt_composer.compose_agent_prompt(
                agent_type="comedy_communicator",
                focus=self.focus,
                language=self.language,
                tone=self.tone
            )
            
            agents.append(
                Agent(
                    role="Comedy Communicator",
                    goal="Add appropriate humor while maintaining educational value",
                    backstory=comedy_backstory,
                    llm=self.llm,
                    verbose=True,
                )
            )

        return agents

    def create_crew_for_paper(
        self, paper_content: str, paper_title: str, use_synthesis: bool = True
    ) -> Crew:
        """Create a crew dynamically based on paper content.

        Args:
            paper_content: The original paper content
            paper_title: The paper title
            use_synthesis: Whether to create and use synthesis first (default: True)
        """
        import click

        # Create synthesis first if requested (default behavior)
        if use_synthesis:
            click.echo(
                "🔬 Creating comprehensive synthesis first (new default workflow)..."
            )
            synthesis_content = self.create_synthesis(paper_content, paper_title)
            # Use synthesis for crew discussion instead of raw content
            content_for_discussion = synthesis_content
        else:
            # Use raw content (old behavior, kept for compatibility)
            content_for_discussion = paper_content

        # Simple topic detection based on title and content
        topic = self._detect_topic(paper_title + " " + content_for_discussion[:1000])

        # Get agents based on focus mode
        if self.focus == "critical":
            # Use existing critical agents
            agents = get_roles_for_topic(topic, self.llm, self.tone)
        else:
            # Use focus-specific agents
            focus_agents = get_focus_agents(self.focus, self.llm)
            # Add base agents (Coordinator and Scientific Reviewer) for non-critical modes
            base_agents = self._get_base_agents_for_focus()
            agents = base_agents + focus_agents

        # Choose task creation method based on conversation mode
        if self.conversation_mode == "enhanced":
            tasks = self._create_tasks(content_for_discussion, paper_title, agents)
        else:
            tasks = self._create_original_tasks(
                content_for_discussion, paper_title, agents
            )

        return Crew(agents=agents, tasks=tasks, verbose=True)

    def create_synthesis(
        self,
        paper_content: str,
        paper_title: str,
        synthesis_method: str = None,
        generate_knowledge_graph: bool = None,
    ) -> str:
        """Create a comprehensive synthesis of the paper content using chunking.
        This is extracted from run_summary_workflow to be reusable."""
        from ..utils.document_chunker import DocumentChunker
        from ..utils.improved_chunker import ImprovedDocumentChunker, ContentType
        from .improved_synthesis import ImprovedSynthesisManager
        import click

        # Use instance defaults if not specified
        if synthesis_method is None:
            synthesis_method = self.synthesis_method
        if generate_knowledge_graph is None:
            generate_knowledge_graph = self.generate_knowledge_graph

        # Check if we should use improved synthesis
        use_improved = (
            os.getenv("USE_IMPROVED_SYNTHESIS", "true").lower() == "true"
            and synthesis_method != "original"
        )

        # Check for existing synthesis with the specific method
        synthesis_filename = (
            f"synthesis_{synthesis_method}.txt"
            if synthesis_method != "original"
            else "synthesis_output.txt"
        )

        # Check if synthesis already exists
        synthesis_path = self.synthesis_dir / synthesis_filename
        if synthesis_path.exists():
            click.echo("📊 Using existing synthesis...")
            with open(synthesis_path, "r", encoding="utf-8") as f:
                return f.read()

        if use_improved and synthesis_method in ["concatenation", "knowledge_graph"]:
            click.echo("✨ Using improved synthesis (content-aware)")
            # Use improved synthesis
            improved_manager = ImprovedSynthesisManager(self.llm)
            improved_chunker = ImprovedDocumentChunker(chunk_size=10000, overlap=500)

            # Detect content type
            content_type = improved_chunker.detect_content_type(
                paper_content, paper_title
            )
            click.echo(f"📝 Content type detected: {content_type.value}")

            # Chunk with improved method
            chunks = improved_chunker.chunk_document(
                paper_content, paper_title, content_type
            )

            click.echo(f"📊 Document chunked into {len(chunks)} sections...")

            # Show contexts
            unique_contexts = list(set(chunk.context_type for chunk in chunks))
            click.echo("📑 Content structure:")
            for context in unique_contexts:
                count = sum(1 for c in chunks if c.context_type == context)
                click.echo(
                    f"   • {context.replace('_', ' ').title()}: {count} section(s)"
                )

            # Run improved synthesis
            result = improved_manager.run_synthesis(
                chunks,
                paper_title,
                content_type,
                method=synthesis_method,
                generate_knowledge_graph=generate_knowledge_graph,
            )
            synthesis_result = result["synthesis"]

            # Save synthesis
            with open(synthesis_path, "w", encoding="utf-8") as f:
                f.write(synthesis_result)

            # Save knowledge graph if available
            if "knowledge_graph" in result:
                with open(
                    self.synthesis_dir / "knowledge_graph.json", "w", encoding="utf-8"
                ) as f:
                    f.write(result["knowledge_graph"])

            # Save additional metadata
            synthesis_data = {
                "project": self.project_name,
                "document_title": paper_title,
                "content_type": content_type.value,
                "document_chunks": len(chunks),
                "chunk_contexts": [chunk.context_type for chunk in chunks],
                "synthesis_length": len(synthesis_result),
                "improved_synthesis": True,
                "synthesis_method": result.get("method", synthesis_method),
                "includes_knowledge_graph": "knowledge_graph" in result,
            }

            # Save metadata
            with open(
                self.synthesis_dir / "synthesis_metadata.json", "w", encoding="utf-8"
            ) as f:
                json.dump(synthesis_data, f, indent=2, ensure_ascii=False)

            method_display = (
                f"{synthesis_method} + knowledge graph"
                if synthesis_method == "concatenation" and generate_knowledge_graph
                else synthesis_method
            )
            click.echo(f"✅ Improved synthesis ({method_display}) completed and saved")
            return synthesis_result

        else:
            # Original synthesis
            click.echo("📑 Using original synthesis method")
            chunker = DocumentChunker(chunk_size=10000, overlap=200)
            chunks = chunker.chunk_document(paper_content, paper_title)

            click.echo(
                f"📊 Document chunked into {len(chunks)} sections for deep analysis..."
            )

            # Show section titles
            unique_sections = []
            for chunk in chunks:
                base_section = chunk.section_title.split(" (Part")[0]
                if base_section not in unique_sections:
                    unique_sections.append(base_section)

            if len(unique_sections) <= 10:
                click.echo("📑 Sections found:")
                for section in unique_sections:
                    click.echo(f"   • {section}")

        # For original synthesis, create agents using centralized prompts
        chunk_analyzer_backstory = self.prompt_composer.compose_agent_prompt(
            agent_type="document_analyzer",
            focus=self.focus,
            language=self.language,
            tone=self.tone
        )
        
        chunk_analyzer = Agent(
            role="Deep Document Analyzer",
            goal="Extract comprehensive insights from each section of the document",
            backstory=chunk_analyzer_backstory,
            llm=self.llm,
            verbose=True,
        )

        synthesizer_backstory = self.prompt_composer.compose_agent_prompt(
            agent_type="master_synthesizer",
            focus=self.focus,
            language=self.language,
            tone=self.tone
        )
        
        synthesizer = Agent(
            role="Master Synthesizer",
            goal="Combine all section analyses into a comprehensive, coherent understanding",
            backstory=synthesizer_backstory,
            llm=self.llm,
            verbose=True,
        )

        # Create tasks for chunk analysis
        chunk_tasks = []
        for i, chunk in enumerate(chunks):
            chunk_task = Task(
                description=chunker.create_chunk_summary_prompt(chunk, paper_title),
                agent=chunk_analyzer,
                expected_output=f"Comprehensive analysis of {chunk.section_title}",
            )
            chunk_tasks.append(chunk_task)

        # Create synthesis task using centralized task prompt
        synthesis_task_description = TaskPrompts.synthesis_task(
            chunks=chunks,
            paper_title=paper_title,
            language=self.language,
            focus=self.focus
        )
        
        synthesis_task = Task(
            description=synthesis_task_description,
            agent=synthesizer,
            expected_output="A content-focused synthesis presenting the actual findings, arguments, and evidence",
        )

        # Build task list: all chunk tasks + synthesis
        all_tasks = chunk_tasks + [synthesis_task]

        # Create crew with synthesis agents
        synthesis_crew = Crew(
            agents=[chunk_analyzer, synthesizer],
            tasks=all_tasks,
            verbose=True,
            embedder={"provider": "openai", "config": {"api_key": OPENAI_API_KEY}},
        )

        # Run the synthesis crew
        click.echo("🔬 Running deep document analysis and synthesis...")
        result = synthesis_crew.kickoff()

        # Save synthesis data
        synthesis_data = {
            "project": self.project_name,
            "paper_title": paper_title,
            "document_chunks": len(chunks),
            "chunk_sections": [chunk.section_title for chunk in chunks],
            "synthesis_length": len(str(result)),
        }

        # Save synthesis metadata
        with open(
            self.synthesis_dir / "synthesis_metadata.json", "w", encoding="utf-8"
        ) as f:
            json.dump(synthesis_data, f, indent=2, ensure_ascii=False)

        # Save chunk analyses for debugging
        for i, task in enumerate(chunk_tasks):
            with open(
                self.synthesis_dir / f"chunk_{i + 1}_analysis.txt",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(f"Section: {chunks[i].section_title}\n")
                f.write(f"Characters: {chunks[i].end_char - chunks[i].start_char}\n")
                f.write("=" * 50 + "\n")
                f.write(str(task.output))

        # Save synthesis output
        synthesis_result = str(synthesis_task.output)
        with open(synthesis_path, "w", encoding="utf-8") as f:
            f.write(synthesis_result)

        click.echo("✅ Synthesis completed and saved")
        return synthesis_result

    def _detect_topic(self, text: str) -> str:
        """Advanced topic detection based on keywords and content analysis."""
        text_lower = text.lower()

        # AI and Machine Learning
        if any(
            term in text_lower
            for term in [
                "artificial intelligence",
                "machine learning",
                "neural network",
                "deep learning",
                "ai",
                "llm",
                "transformer",
                "gpt",
                "bert",
                "reinforcement learning",
                "computer vision",
                "natural language processing",
                "nlp",
                "convolutional",
                "lstm",
                "gan",
                "generative adversarial",
            ]
        ):
            return "AI"

        # Medicine and Biology
        if any(
            term in text_lower
            for term in [
                "medicine",
                "medical",
                "biology",
                "biomedical",
                "clinical",
                "therapy",
                "disease",
                "treatment",
                "diagnosis",
                "patient",
                "drug",
                "pharmaceutical",
                "genome",
                "dna",
                "protein",
                "cell",
                "virus",
                "bacteria",
                "vaccine",
            ]
        ):
            return "Medicine"

        # Physics and Chemistry
        if any(
            term in text_lower
            for term in [
                "physics",
                "quantum",
                "relativity",
                "particle",
                "chemistry",
                "chemical",
                "molecule",
                "atom",
                "nuclear",
                "thermodynamics",
                "electromagnetic",
                "mechanics",
                "photon",
                "electron",
                "ion",
                "catalyst",
                "reaction",
            ]
        ):
            return "Science"

        # Psychology and Neuroscience
        if any(
            term in text_lower
            for term in [
                "psychology",
                "psychological",
                "neuroscience",
                "brain",
                "cognitive",
                "behavior",
                "behavioral",
                "mental",
                "consciousness",
                "perception",
                "memory",
                "learning",
                "emotion",
                "neuronal",
                "synaptic",
                "fmri",
                "eeg",
            ]
        ):
            return "Psychology"

        # Economics and Finance
        if any(
            term in text_lower
            for term in [
                "economics",
                "economic",
                "finance",
                "financial",
                "market",
                "trading",
                "investment",
                "gdp",
                "inflation",
                "monetary",
                "fiscal",
                "cryptocurrency",
                "blockchain",
                "banking",
                "economy",
                "revenue",
                "profit",
                "cost",
            ]
        ):
            return "Economics"

        # Technology and Engineering
        if any(
            term in text_lower
            for term in [
                "engineering",
                "technology",
                "software",
                "hardware",
                "computer science",
                "algorithm",
                "programming",
                "database",
                "network",
                "security",
                "cyber",
                "internet",
                "web",
                "mobile",
                "cloud",
                "architecture",
                "system",
            ]
        ):
            return "Technology"

        return "General"

    def _create_tasks(
        self, paper_content: str, paper_title: str, agents: List[Agent]
    ) -> List[Task]:
        """Create tasks for the crew with enhanced conversational interaction."""
        tasks = []

        # Identify agent types
        base_agent_count = 5
        specialized_agents = (
            agents[base_agent_count:] if len(agents) > base_agent_count else []
        )
        has_humor_agent = len(agents) > base_agent_count and any(
            agent.role == "Comedy Communicator" for agent in agents
        )

        # Separate conversation agents from post-production agents
        conversation_agents = [
            agent
            for agent in agents
            if agent.role
            not in [
                "Master Educational Science Communicator & Storyteller",
                "Comedy Communicator",
            ]
        ]
        post_production_agents = [
            agent
            for agent in agents
            if agent.role
            in [
                "Master Educational Science Communicator & Storyteller",
                "Comedy Communicator",
            ]
        ]

        # Initial analysis task - CONVERSATION AGENTS ONLY (NO HUMOR)
        initial_analysis_description = TaskPrompts.initial_analysis_task(
            paper_title=paper_title,
            paper_content=paper_content,
            language=self.language,
            conversation_agents=conversation_agents,
            focus=self.focus
        )
        
        tasks.append(
            Task(
                description=initial_analysis_description,
                agent=agents[0],  # Coordinator leads
                expected_output="Comprehensive technical analysis from conversation agents only (no post-production agents)",
            )
        )

        # SPECIALIZED AGENT DEEP DIVE - CONVERSATION AGENTS ONLY (NO HUMOR)
        if specialized_agents:
            # Find specialized agents that aren't post-production
            conversation_specialists = [
                agent
                for agent in specialized_agents
                if agent.role
                not in [
                    "Master Educational Science Communicator & Storyteller",
                    "Comedy Communicator",
                ]
            ]
            if conversation_specialists:
                lead_specialist = conversation_specialists[0]
                specialist_task_description = TaskPrompts.specialist_deep_dive_task(
                    conversation_specialists=conversation_specialists,
                    language=self.language,
                    focus=self.focus
                )
                
                tasks.append(
                    Task(
                        description=specialist_task_description,
                        agent=lead_specialist,
                        expected_output=f"Deep technical specialist analysis from {len(conversation_specialists)} domain experts",
                    )
                )

        # Q&A Session task
        qa_task_description = TaskPrompts.qa_session_task(
            conversation_agents=conversation_agents,
            specialized_agents=specialized_agents,
            language=self.language,
            focus=self.focus
        )
        
        tasks.append(
            Task(
                description=qa_task_description,
                agent=agents[2],  # Critical Thinker facilitates
                expected_output="Dynamic technical Q&A conversation between conversation agents only (no post-production or humor)",
            )
        )

        # Debate task
        debate_task_description = TaskPrompts.debate_task(
            conversation_agents=conversation_agents,
            specialized_agents=specialized_agents,
            language=self.language,
            focus=self.focus
        )
        
        tasks.append(
            Task(
                description=debate_task_description,
                agent=agents[1],  # Scientific Reviewer moderates debate
                expected_output="Rich interdisciplinary technical debate between conversation agents only (no post-production or humor)",
            )
        )

        # Collaborative synthesis task
        collaborative_task_description = TaskPrompts.collaborative_synthesis_task(
            conversation_agents=conversation_agents,
            specialized_agents=specialized_agents,
            language=self.language,
            focus=self.focus
        )
        
        tasks.append(
            Task(
                description=collaborative_task_description,
                agent=agents[0],  # Coordinator leads synthesis
                expected_output="Collaborative technical synthesis conversation from conversation agents only (no post-production or humor)",
            )
        )

        # Final discussion task
        final_discussion_description = TaskPrompts.final_discussion_task(
            conversation_agents=conversation_agents,
            specialized_agents=specialized_agents,
            language=self.language,
            focus=self.focus
        )
        
        tasks.append(
            Task(
                description=final_discussion_description,
                agent=agents[2],  # Critical Thinker facilitates final discussion
                expected_output="Final comprehensive technical discussion ready for post-production processing",
            )
        )

        # POST-PRODUCTION PHASE 1: Comedy Communicator adds humor (if present)
        if has_humor_agent:
            humor_agent = next(
                agent for agent in agents if agent.role == "Comedy Communicator"
            )
            tone_instructions = self._get_tone_instructions()
            comedy_task_description = TaskPrompts.comedy_enhancement_task(
                tone_instructions=tone_instructions,
                language=self.language,
                focus=self.focus
            )
            
            tasks.append(
                Task(
                    description=comedy_task_description,
                    agent=humor_agent,
                    expected_output="Technical content enhanced with appropriate humor and entertainment while maintaining scientific accuracy",
                )
            )

        # POST-PRODUCTION PHASE 2: Educational/Technical Writer processes ALL content
        if self.focus == "technical":
            educational_writer = next(
                agent
                for agent in agents
                if agent.role == "Technical Content Specialist"
            )
        else:
            educational_writer = next(
                agent
                for agent in agents
                if agent.role == "Master Educational Science Communicator & Storyteller"
            )

        technical_instructions = self._get_technical_instructions()
        duration_instructions = self._get_duration_instructions()
        language_instructions = self._get_language_instructions()

        if self.focus == "technical":
            # Technical writing task - zero interpretation
            # Get the previous task output (final discussion or comedy-enhanced)
            previous_task_context = tasks[-1] if tasks else None

            technical_task_desc = f"""
            Transform the previous task outputs into a technical presentation with ZERO interpretation.
            
            DOCUMENT TITLE: {paper_title}
            
            You must review ALL previous outputs and create a technical document that:
            1. Presents ONLY factual information
            2. Removes ALL interpretive language (revolutionary, groundbreaking, etc.)
            3. States findings directly without implications
            4. Uses technical manual style - clear and objective
            5. Never adds "this suggests", "this implies", etc.
            
            {
                create_technical_writing_task(
                    content="Use the complete discussion from all previous tasks",
                    title=paper_title,
                    target_length="comprehensive",
                    language=self.language,
                )
            }
            """

            technical_task = Task(
                description=technical_task_desc,
                agent=educational_writer,
                expected_output="Technical presentation with zero interpretation - only facts and concepts as stated",
                context=[previous_task_context] if previous_task_context else [],
            )
            tasks.append(technical_task)
        else:
            # Regular educational writing task
            educational_task_description = TaskPrompts.educational_script_task(
                paper_title=paper_title,
                has_humor_agent=has_humor_agent,
                technical_instructions=technical_instructions,
                duration_instructions=duration_instructions,
                language_instructions=language_instructions,
                language=self.language,
                focus=self.focus,
                tone=self.tone
            )
            
            tasks.append(
                Task(
                    description=educational_task_description,
                    agent=educational_writer,
                    expected_output="FINAL publication-ready educational script incorporating ALL conversation insights"
                    + (" and humor" if has_humor_agent else ""),
                )
            )

        return tasks

    def _create_original_tasks(
        self, paper_content: str, paper_title: str, agents: List[Agent]
    ) -> List[Task]:
        """Create original tasks for the crew (4-task structure) but with proper conversation/post-production separation."""
        tasks = []

        # Identify agent types
        base_agent_count = 5
        specialized_agents = (
            agents[base_agent_count:] if len(agents) > base_agent_count else []
        )
        has_humor_agent = len(agents) > base_agent_count and any(
            agent.role == "Comedy Communicator" for agent in agents
        )

        # Separate conversation agents from post-production agents
        conversation_agents = [
            agent
            for agent in agents
            if agent.role
            not in [
                "Master Educational Science Communicator & Storyteller",
                "Comedy Communicator",
            ]
        ]
        post_production_agents = [
            agent
            for agent in agents
            if agent.role
            in [
                "Master Educational Science Communicator & Storyteller",
                "Comedy Communicator",
            ]
        ]

        # Original Initial analysis task - CONVERSATION AGENTS ONLY (NO HUMOR)
        initial_analysis_description = TaskPrompts.original_initial_analysis_task(
            paper_title=paper_title,
            paper_content=paper_content,
            conversation_agents=conversation_agents,
            specialized_agents=specialized_agents,
            language=self.language,
            focus=self.focus
        )
        
        tasks.append(
            Task(
                description=initial_analysis_description,
                agent=agents[0],  # Coordinator leads
                expected_output="Initial technical analysis and key points from conversation agents (no post-production agents)",
            )
        )

        # Original Discussion task - CONVERSATION AGENTS ONLY (NO HUMOR)
        discussion_task_description = TaskPrompts.original_discussion_task(
            conversation_agents=conversation_agents,
            specialized_agents=specialized_agents,
            language=self.language,
            focus=self.focus
        )
        
        tasks.append(
            Task(
                description=discussion_task_description,
                agent=agents[2],  # Critical Thinker facilitates discussion
                expected_output="Comprehensive technical discussion from conversation agents ready for post-production processing",
            )
        )

        # POST-PRODUCTION PHASE 1: Comedy Communicator adds humor (if present)
        if has_humor_agent:
            humor_agent = next(
                agent for agent in agents if agent.role == "Comedy Communicator"
            )
            tone_instructions = self._get_tone_instructions()
            comedy_task_description = TaskPrompts.original_comedy_task(
                tone_instructions=tone_instructions,
                language=self.language,
                focus=self.focus
            )
            
            tasks.append(
                Task(
                    description=comedy_task_description,
                    agent=humor_agent,
                    expected_output="Technical content enhanced with appropriate humor and entertainment while maintaining scientific accuracy",
                )
            )

        # POST-PRODUCTION PHASE 2: Master Educational Science Communicator & Storyteller transforms conversations
        educational_writer = next(
            agent
            for agent in agents
            if agent.role == "Master Educational Science Communicator & Storyteller"
        )
        technical_instructions = self._get_technical_instructions()
        duration_instructions = self._get_duration_instructions()
        language_instructions = self._get_language_instructions()

        original_educational_task_description = TaskPrompts.original_educational_script_task(
            paper_title=paper_title,
            has_humor_agent=has_humor_agent,
            technical_instructions=technical_instructions,
            duration_instructions=duration_instructions,
            language_instructions=language_instructions,
            language=self.language,
            focus=self.focus,
            tone=self.tone
        )
        
        tasks.append(
            Task(
                description=original_educational_task_description,
                agent=educational_writer,
                expected_output="FINAL publication-ready educational script incorporating insights from all conversation agents"
                + (" and humor" if has_humor_agent else ""),
            )
        )

        return tasks

    def _get_technical_instructions(self) -> str:
        """Get technical level specific instructions."""
        if self.technical_level == "technical":
            return """
            CRITICAL TECHNICAL REQUIREMENTS - THIS IS MANDATORY:
            15. YOU MUST include comprehensive technical depth throughout the entire script
            16. EXPLAIN IN DETAIL: experimental design, control groups, statistical methods used
            17. INCLUDE SPECIFIC NUMBERS: sample sizes (e.g. "54 participants"), p-values, effect sizes, confidence intervals
            18. DISCUSS METHODOLOGY THOROUGHLY: EEG analysis methods, data collection procedures, analysis pipelines
            19. ADDRESS LIMITATIONS AND CONFOUNDS: what could bias results, alternative explanations
            20. USE TECHNICAL TERMS CORRECTLY: neural connectivity, spectral analysis, statistical significance, but ALWAYS explain them
            21. COMPARE TO OTHER STUDIES: how does this fit with existing research in the field
            22. DISCUSS THEORETICAL IMPLICATIONS: what theories does this support or challenge
            23. INCLUDE TECHNICAL DETAILS: electrode placement, signal processing, statistical tests used
            24. EXPLAIN THE "HOW" not just the "WHAT": how did they measure cognitive load, how did they analyze connectivity
            25. DISCUSS FUTURE RESEARCH: specific methodological improvements, follow-up studies needed
            26. BE PRECISE WITH TERMINOLOGY: use exact scientific language for concepts
            27. This should feel like a technical seminar for graduate students or researchers
            """
        elif self.technical_level == "accessible":
            return """
            ACCESSIBLE LEVEL REQUIREMENTS:
            15. Focus on core concepts and main findings rather than technical details
            16. Use everyday analogies to explain complex ideas
            17. Emphasize practical implications and real-world applications
            18. Keep technical jargon to a minimum, always explaining when used
            19. Focus on the "why this matters" rather than the "how they did it"
            20. Make connections to things the audience already understands
            """
        else:  # simple
            return """
            SIMPLE LEVEL REQUIREMENTS - FOR NON-TECHNICAL AUDIENCE:
            15. AVOID ALL TECHNICAL JARGON - use only everyday language
            16. Use SIMPLE analogies from daily life (like cooking, sports, relationships)
            17. Focus ONLY on "what this means for YOU" - direct personal relevance
            18. Explain concepts as if talking to a curious friend with no scientific background
            19. NO scientific terms without VERY simple explanations (e.g., "neurons - the tiny messengers in your brain")
            20. Use SHORT sentences and familiar words only
            21. Focus on PRACTICAL takeaways: "What can you do with this information?"
            22. Tell STORIES and use EXAMPLES from everyday situations
            23. Ask rhetorical questions that connect to personal experience: "¿Alguna vez has notado que...?"
            24. Make it feel like a friendly conversation, not a lecture
            25. Focus on the BIG PICTURE and skip complex details entirely
            26. Use comparisons to things everyone knows: "like your smartphone battery", "like driving a car"
            27. This should sound like explaining to a family member who's genuinely curious but has no technical background
            """

    def _get_language_instructions(self) -> str:
        """Get language-specific instructions, especially for avoiding anglicisms."""
        if self.language.lower() == "english":
            return ""  # No special instructions for English
        else:
            return f"""
            LANGUAGE REQUIREMENTS FOR {self.language.upper()}:
            
            CRITICAL: AVOID ANGLICISMS whenever possible and use proper {self.language} terms:
            - Instead of "link" use "enlace" or "vínculo"
            - Instead of "feedback" use "retroalimentación" or "respuesta"
            - Insted of "puzzle" use "rompecabezas" or "problema"
            - Instead of "performance" use "rendimiento" or "desempeño"
            - Instead of "input/output" use "entrada/salida"
            - Instead of "update" use "actualizar" or "poner al día"
            
            EXCEPTIONS - You CAN use anglicisms for:
            1. Very new technical terms with no established translation (e.g., "blockchain", "ChatGPT")
            2. Proper names of tools/companies (e.g., "TensorFlow", "GitHub", "OpenAI")
            3. Widely adopted terms in scientific literature (e.g., "machine learning" vs "aprendizaje automático")
            4. When the Spanish term is more confusing than helpful
            
            GENERAL RULES:
            - Always prioritize natural {self.language} expressions
            - Use {self.language} sentence structures and idioms
            - Make it sound like a native {self.language} speaker wrote it
            - When you must use an anglicism, briefly explain it if needed
            """

    def _get_duration_instructions(self) -> str:
        """Get duration specific instructions with dynamic word count calculation."""
        # Cálculo dinámico: aproximadamente 150 palabras por minuto de audio
        word_count_min = self.duration_minutes * 140
        word_count_max = self.duration_minutes * 160

        # Determinar el nivel de profundidad basado en la duración
        if self.duration_minutes <= 3:
            depth_guidance = """
            - Focus on 1-2 main concepts only
            - Keep explanations concise but complete
            - Include one compelling example per main point
            - Go straight to the point without much additional context
            """
        elif self.duration_minutes <= 7:
            depth_guidance = """
            - Cover 2-4 key concepts with moderate explanations
            - Include detailed examples and clear analogies
            - Provide necessary basic context
            - Allow some exploration of implications
            """
        elif self.duration_minutes <= 15:
            depth_guidance = """
            - Address 4-6 main concepts with moderate depth
            - Include multiple examples and analogies per concept
            - Provide relevant historical and theoretical context
            - Explore implications and practical applications
            - Include brief discussion of methodology if relevant
            """
        else:  # 16+ minutos
            depth_guidance = """
            - Conduct a COMPREHENSIVE and IN-DEPTH analysis
            - Cover all main aspects of the topic
            - Include detailed context and extensive theoretical framework
            - Explain methodology, limitations and alternative interpretations
            - Provide multiple examples, analogies and real-world applications
            - Include detailed discussion of implications and future directions
            - Allow deep exploration of related concepts and broader significance
            - Should feel like a comprehensive academic lecture, not a summary
            """

        return f"""
        DURATION REQUIREMENT: EXACTLY {self.duration_minutes} minutes of content ({word_count_min}-{word_count_max} words) - THIS IS MANDATORY
        
        DEPTH GUIDANCE FOR {self.duration_minutes} MINUTES:
        {depth_guidance}
        
        TECHNICAL CALCULATION:
        - Target reading speed: ~150 words per minute
        - Word range: {word_count_min}-{word_count_max} words
        - If content is too short, EXPAND significantly with more detail and depth
        - If too long, maintain quality but adjust information density
        """

    def _get_word_count_target(self) -> str:
        """Get word count target based on duration with dynamic calculation."""
        word_count_min = self.duration_minutes * 140
        word_count_max = self.duration_minutes * 160
        return f"{word_count_min}-{word_count_max}"

    def _get_tone_instructions(self) -> str:
        """Get tone-specific instructions for agents."""
        if self.tone == "humorous":
            return """
            TONE REQUIREMENTS - HUMOROUS:
            - Use appropriate humor, wit, and clever analogies to make content engaging
            - Include light jokes and funny observations that enhance understanding
            - Use entertaining examples and amusing comparisons
            - Keep humor respectful and relevant to the topic
            - Think science communicators like Neil deGrasse Tyson or Bill Nye
            - Use wordplay, puns, and clever observations when appropriate
            - Make the audience smile while learning
            - Avoid offensive humor or jokes that undermine the science
            """
        elif self.tone == "playful":
            return """
            TONE REQUIREMENTS - PLAYFUL:
            - Use a light, energetic, and enthusiastic approach
            - Include creative metaphors and imaginative scenarios
            - Use exclamations and expressive language appropriately
            - Create a sense of wonder and excitement about the topic
            - Think of it like explaining to a curious friend who loves learning
            - Use "what if" scenarios and thought experiments
            - Be animated and engaging without being silly
            - Maintain scientific accuracy while being entertaining
            """
        elif self.tone == "casual":
            return """
            TONE REQUIREMENTS - CASUAL:
            - Use relaxed, conversational language
            - Speak as if talking to a smart friend over coffee
            - Use everyday examples and relatable analogies
            - Avoid overly formal academic language
            - Include personal asides and conversational touches
            - Make it feel like a friendly explanation, not a lecture
            - Use "you know" and similar conversational markers sparingly
            - Keep it accessible but not dumbed down
            """
        else:  # academic
            return """
            TONE REQUIREMENTS - ACADEMIC:
            - Maintain serious, scholarly tone throughout
            - Use precise scientific language and terminology
            - Focus on accuracy and intellectual rigor
            - Provide thorough, evidence-based analysis
            - Keep the discussion professional and authoritative
            - This is the default, serious academic approach
            """

    def run_crew_and_save_discussion(self, crew: Crew, paper_title: str) -> str:
        """Run the crew and save all discussion data."""
        # Run the crew
        result = crew.kickoff()

        # Save crew structure
        crew_info = {
            "project_name": self.project_name,
            "paper_title": paper_title,
            "language": self.language,
            "agents": [
                {"role": agent.role, "goal": agent.goal, "backstory": agent.backstory}
                for agent in crew.agents
            ],
            "tasks": [
                {
                    "description": task.description,
                    "expected_output": task.expected_output,
                    "agent_role": task.agent.role if task.agent else None,
                }
                for task in crew.tasks
            ],
        }

        # Save crew structure
        with open(
            self.discussion_dir / "crew_structure.json", "w", encoding="utf-8"
        ) as f:
            json.dump(crew_info, f, indent=2, ensure_ascii=False)

        # Save final result
        with open(self.discussion_dir / "final_result.txt", "w", encoding="utf-8") as f:
            f.write(str(result))

        # Save individual task outputs if available
        for i, task in enumerate(crew.tasks):
            if hasattr(task, "output") and task.output:
                with open(
                    self.discussion_dir / f"task_{i + 1}_output.txt",
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.write(str(task.output))

        return str(result)

    def run_summary_workflow(self, paper_content: str, paper_title: str) -> str:
        """Run improved workflow with chunking: Document → Chunk Analysis → Synthesis → Educational Writer."""
        # Import improved educational writer and chunker
        from .improved_educational_writer import (
            get_improved_educational_writer,
            create_enhanced_educational_task,
        )
        from ..utils.document_chunker import DocumentChunker

        # Import click for consistent output
        import click

        # Check if synthesis already exists
        synthesis_path = self.synthesis_dir / "synthesis_output.txt"
        existing_synthesis = None

        if synthesis_path.exists():
            click.echo("📊 Found existing synthesis, reusing it...")
            with open(synthesis_path, "r", encoding="utf-8") as f:
                existing_synthesis = f.read()

        # Chunk the document
        chunker = DocumentChunker(chunk_size=10000, overlap=200)
        chunks = chunker.chunk_document(paper_content, paper_title)

        if not existing_synthesis:
            click.echo(
                f"📊 Document chunked into {len(chunks)} sections for deep analysis..."
            )

            # Show section titles
            unique_sections = []
            for chunk in chunks:
                base_section = chunk.section_title.split(" (Part")[0]
                if base_section not in unique_sections:
                    unique_sections.append(base_section)

            if len(unique_sections) <= 10:
                click.echo("📑 Sections found:")
                for section in unique_sections:
                    click.echo(f"   • {section}")

        # Create agents based on focus mode using centralized prompts
        if self.focus == "technical":
            # Use objective knowledge extraction agents for zero interpretation
            chunk_analyzer_backstory = self.prompt_composer.compose_agent_prompt(
                agent_type="objective_content_analyzer",
                focus=self.focus,
                language=self.language,
                tone=self.tone
            )
            
            chunk_analyzer = Agent(
                role="Objective Content Analyzer",
                goal="Extract ALL factual knowledge from each section with zero interpretation",
                backstory=chunk_analyzer_backstory,
                llm=self.llm,
                verbose=True,
            )

            synthesizer_backstory = self.prompt_composer.compose_agent_prompt(
                agent_type="objective_knowledge_synthesizer",
                focus=self.focus,
                language=self.language,
                tone=self.tone
            )
            
            synthesizer = Agent(
                role="Objective Knowledge Synthesizer",
                goal="Combine section analyses into a comprehensive collection of extracted knowledge",
                backstory=synthesizer_backstory,
                llm=self.llm,
                verbose=True,
            )

            educational_writer = get_technical_writer_agent(self.llm)
        else:
            # Use standard agents for other focus modes
            chunk_analyzer_backstory = self.prompt_composer.compose_agent_prompt(
                agent_type="document_analyzer",
                focus=self.focus,
                language=self.language,
                tone=self.tone
            )
            
            chunk_analyzer = Agent(
                role="Deep Document Analyzer",
                goal="Extract comprehensive insights from each section of the document",
                backstory=chunk_analyzer_backstory,
                llm=self.llm,
                verbose=True,
            )

            synthesizer_backstory = self.prompt_composer.compose_agent_prompt(
                agent_type="master_synthesizer",
                focus=self.focus,
                language=self.language,
                tone=self.tone
            )
            
            synthesizer = Agent(
                role="Master Synthesizer",
                goal="Combine all section analyses into a comprehensive, coherent understanding",
                backstory=synthesizer_backstory,
                llm=self.llm,
                verbose=True,
            )

            educational_writer = get_improved_educational_writer(self.llm)

        # Initialize chunk_tasks here so it's accessible in all branches
        chunk_tasks = []

        # Check if we need to create synthesis or use existing
        if existing_synthesis:
            # Skip chunk analysis and synthesis tasks, go directly to educational
            click.echo("📝 Creating educational script from existing synthesis...")

            # Get the enhanced task description with synthesis
            task_description = create_enhanced_educational_task(
                educational_writer,
                self.language,
                self.duration_minutes,
                self.technical_level,
                self.tone,
            )

            # Prepend the synthesis to the task
            full_task_description = f"""
            Transform this comprehensive synthesis into an engaging educational script.
            
            Title: {paper_title}
            
            Synthesis to transform:
            {existing_synthesis}
            
            ---
            
            {task_description}
            """

            educational_task = Task(
                description=full_task_description,
                agent=educational_writer,
                expected_output=f"A natural, engaging {self.duration_minutes}-minute educational script in {self.language}",
            )

            # Create crew with only educational writer
            crew = Crew(
                agents=[educational_writer],
                tasks=[educational_task],
                verbose=True,
            )

            # Run the crew
            result = crew.kickoff()

        else:
            # Original workflow: create synthesis first
            # Create tasks for chunk analysis
            chunk_tasks = []
            for i, chunk in enumerate(chunks):
                if self.focus == "technical":
                    # Objective knowledge extraction prompt - zero interpretation
                    chunk_description = TaskPrompts.technical_chunk_analysis_task(
                        chunk=chunk,
                        language=self.language
                    )
                    expected = f"All objective knowledge from {chunk.section_title} - zero interpretation"
                else:
                    chunk_description = chunker.create_chunk_summary_prompt(
                        chunk, paper_title
                    )
                    expected = f"Comprehensive analysis of {chunk.section_title}"

                chunk_task = Task(
                    description=chunk_description,
                    agent=chunk_analyzer,
                    expected_output=expected,
                )
                chunk_tasks.append(chunk_task)

            # Create synthesis task using centralized prompts
            if self.focus == "technical":
                synthesis_description = TaskPrompts.technical_synthesis_task(
                    chunks=chunks,
                    paper_title=paper_title,
                    language=self.language
                )
            else:
                synthesis_description = TaskPrompts.synthesis_task(
                    chunks=chunks,
                    paper_title=paper_title,
                    language=self.language,
                    focus=self.focus
                )

            synthesis_task = Task(
                description=synthesis_description,
                agent=synthesizer,
                expected_output="Technical synthesis with facts only - zero interpretation"
                if self.focus == "technical"
                else "A content-focused synthesis presenting the actual findings, arguments, and evidence",
            )

            # Get the task description based on focus
            if self.focus == "technical":
                task_description = create_technical_writing_task(
                    content="Previous synthesis content will be used",
                    title=paper_title,
                    target_length="comprehensive",
                    language=self.language,
                )
                expected_output = (
                    "Technical presentation with zero interpretation - facts only"
                )
            else:
                task_description = create_enhanced_educational_task(
                    educational_writer,
                    self.language,
                    self.duration_minutes,
                    self.technical_level,
                    self.tone,
                )
                expected_output = f"A natural, engaging {self.duration_minutes}-minute educational script in {self.language}"

            educational_task = Task(
                description=task_description,
                agent=educational_writer,
                expected_output=expected_output,
            )

            # Build task list: all chunk tasks + synthesis + educational
            all_tasks = chunk_tasks + [synthesis_task, educational_task]

            # Create crew with all agents
            crew = Crew(
                agents=[chunk_analyzer, synthesizer, educational_writer],
                tasks=all_tasks,
                verbose=True,
                embedder={"provider": "openai", "config": {"api_key": OPENAI_API_KEY}},
            )

            # Run the crew
            result = crew.kickoff()

        # Save the summary workflow data
        crew_data = {
            "project": self.project_name,
            "paper_title": paper_title,
            "language": self.language,
            "technical_level": self.technical_level,
            "duration_minutes": self.duration_minutes,
            "tone": self.tone,
            "workflow": "summary_with_chunking",
            "document_chunks": len(chunks),
            "chunk_sections": [chunk.section_title for chunk in chunks],
            "agents": [
                {"role": agent.role, "goal": agent.goal} for agent in crew.agents
            ],
            "tasks": [
                {
                    "description": task.description[:200] + "...",
                    "type": (
                        "chunk_analysis"
                        if i < len(chunk_tasks)
                        else "synthesis"
                        if i == len(chunk_tasks)
                        else "educational"
                    ),
                }
                for i, task in enumerate(crew.tasks)
            ],
        }

        # Save crew structure
        with open(
            self.discussion_dir / "summary_crew_structure.json", "w", encoding="utf-8"
        ) as f:
            json.dump(crew_data, f, indent=2, ensure_ascii=False)

        # Save final result
        with open(
            self.discussion_dir / "summary_final_result.txt", "w", encoding="utf-8"
        ) as f:
            f.write(str(result))

        # Only save chunk analyses and synthesis if we created them
        if not existing_synthesis:
            # Save chunk analyses for debugging
            for i, task in enumerate(chunk_tasks):
                with open(
                    self.discussion_dir / f"chunk_{i + 1}_analysis.txt",
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.write(f"Section: {chunks[i].section_title}\n")
                    f.write(
                        f"Characters: {chunks[i].end_char - chunks[i].start_char}\n"
                    )
                    f.write("=" * 50 + "\n")
                    f.write(str(task.output))

            # Save synthesis output to both locations for compatibility
            synthesis_content = str(synthesis_task.output)

            # Save to discussion directory (for backward compatibility)
            with open(
                self.discussion_dir / "synthesis_output.txt", "w", encoding="utf-8"
            ) as f:
                f.write(synthesis_content)

            # Also save to synthesis directory (consistent with create_synthesis method)
            with open(
                self.synthesis_dir / "synthesis_output.txt", "w", encoding="utf-8"
            ) as f:
                f.write(synthesis_content)

            # Save synthesis metadata
            synthesis_data = {
                "project": self.project_name,
                "paper_title": paper_title,
                "document_chunks": len(chunks),
                "chunk_sections": [chunk.section_title for chunk in chunks],
                "synthesis_length": len(synthesis_content),
                "workflow": "summary",
            }

            with open(
                self.synthesis_dir / "synthesis_metadata.json", "w", encoding="utf-8"
            ) as f:
                json.dump(synthesis_data, f, indent=2, ensure_ascii=False)
        else:
            click.echo("✅ Reused existing synthesis from synthesis directory")

        return str(result)

    def run_direct_educational_workflow(
        self, text_content: str, title: str = ""
    ) -> str:
        """Direct workflow that passes text straight to the Educational Writer."""
        from .improved_educational_writer import (
            get_improved_educational_writer,
            create_enhanced_educational_task,
        )

        # Get the improved educational writer
        educational_writer = get_improved_educational_writer(self.llm)

        # Use the enhanced task creation
        direct_task_description = create_enhanced_educational_task(
            educational_writer,
            self.language,
            self.duration_minutes,
            self.technical_level,
            self.tone,
        )

        # Prepend the text content to the task description
        full_task_description = f"""
        Transform this text content into an engaging educational script.
        
        Title/Topic: {title if title else "Educational Content"}
        
        Content to transform:
        {text_content}
        
        ---
        
        {direct_task_description}
        """

        direct_task = Task(
            description=full_task_description,
            agent=educational_writer,
            expected_output="Natural, engaging educational script ready for voice synthesis",
        )

        # Create a minimal crew with just the educational writer
        minimal_crew = Crew(
            agents=[educational_writer], tasks=[direct_task], verbose=True
        )

        # Run the crew
        result = minimal_crew.kickoff()

        # Save the result
        output_path = self.project_dir / "direct_educational_script.txt"
        final_script = str(result).strip()

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_script)

        return final_script

    def run_tts_optimization_workflow(
        self,
        educational_script: str,
        language: str = "Spanish",
        voice_provider: str = "elevenlabs",
    ) -> str:
        """Optimize an educational script for TTS synthesis with enhanced formatting and rhythm."""
        # Get the TTS optimizer agent
        tts_agent = get_tts_optimizer_agent(self.llm)

        # Create the TTS optimization task
        optimization_task_description = create_tts_optimization_task(
            tts_agent, educational_script, language, voice_provider
        )

        optimization_task = Task(
            description=optimization_task_description,
            agent=tts_agent,
            expected_output="TTS-optimized educational script with enhanced formatting, emphasis markers, strategic pauses, and natural rhythm patterns",
        )

        # Create a minimal crew with just the TTS optimizer
        tts_crew = Crew(agents=[tts_agent], tasks=[optimization_task], verbose=True)

        # Run the optimization
        result = tts_crew.kickoff()

        # Save TTS optimization data for debugging
        tts_data = {
            "project": self.project_name,
            "language": language,
            "voice_provider": voice_provider,
            "workflow": "tts_optimization",
            "original_script_length": len(educational_script),
            "optimized_script_length": len(str(result)),
            "agent": {"role": tts_agent.role, "goal": tts_agent.goal},
        }

        # Save TTS crew structure
        with open(
            self.discussion_dir / "tts_optimization_structure.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(tts_data, f, indent=2, ensure_ascii=False)

        # Save TTS optimization result
        with open(
            self.discussion_dir / "tts_optimization_result.txt", "w", encoding="utf-8"
        ) as f:
            f.write(str(result))

        return str(result).strip()

    def has_existing_discussion(self) -> bool:
        """Check if there's an existing discussion that can be reused."""
        final_result_path = self.discussion_dir / "final_result.txt"
        return final_result_path.exists() and final_result_path.stat().st_size > 0

    def run_reuse_discussion_workflow(self, paper_title: str = "") -> str:
        """Reuse existing discussion and only regenerate the final educational script."""
        from .improved_educational_writer import (
            get_improved_educational_writer,
            create_enhanced_educational_task,
        )

        # Check if discussion exists
        final_result_path = self.discussion_dir / "final_result.txt"
        if not final_result_path.exists():
            raise FileNotFoundError(
                f"No existing discussion found at {final_result_path}"
            )

        # Read the existing discussion
        with open(final_result_path, "r", encoding="utf-8") as f:
            existing_discussion = f.read()

        if not existing_discussion.strip():
            raise ValueError("Existing discussion file is empty")

        # Get the improved educational writer
        educational_writer = get_improved_educational_writer(self.llm)

        # Use the enhanced task creation with the existing discussion
        reuse_task_description = create_enhanced_educational_task(
            educational_writer,
            self.language,
            self.duration_minutes,
            self.technical_level,
            self.tone,
        )

        # Prepend the existing discussion to the task description
        full_task_description = f"""
        Transform this existing discussion/analysis into an engaging educational script.
        
        Title/Topic: {paper_title if paper_title else "Educational Content"}
        
        Previous Discussion/Analysis to transform:
        {existing_discussion}
        
        ---
        
        {reuse_task_description}
        """

        reuse_task = Task(
            description=full_task_description,
            agent=educational_writer,
            expected_output="Natural, engaging educational script ready for voice synthesis, based on existing discussion",
        )

        # Create a minimal crew with just the educational writer
        reuse_crew = Crew(agents=[educational_writer], tasks=[reuse_task], verbose=True)

        # Run the crew
        result = reuse_crew.kickoff()

        # Save reuse workflow data for debugging
        reuse_data = {
            "project": self.project_name,
            "paper_title": paper_title,
            "language": self.language,
            "technical_level": self.technical_level,
            "duration_minutes": self.duration_minutes,
            "tone": self.tone,
            "workflow": "reuse_discussion",
            "existing_discussion_length": len(existing_discussion),
            "final_script_length": len(str(result)),
            "agent": {"role": educational_writer.role, "goal": educational_writer.goal},
        }

        # Save reuse crew structure
        with open(
            self.discussion_dir / "reuse_discussion_structure.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(reuse_data, f, indent=2, ensure_ascii=False)

        # Save reuse result
        with open(
            self.discussion_dir / "reuse_discussion_result.txt", "w", encoding="utf-8"
        ) as f:
            f.write(str(result))

        return str(result).strip()

    def run_light_edit_flow(
        self, educational_script: str, paper_title: str = ""
    ) -> str:
        """Run light editing flow to improve readability before TTS optimization.

        This flow:
        1. Takes the educational script from summary workflow
        2. Applies minimal editing for grammar and readability
        3. Preserves all content and technical accuracy
        4. Returns the lightly edited script

        Args:
            educational_script: The script to edit
            paper_title: Title of the paper

        Returns:
            The lightly edited script
        """
        print(f"✏️  Applying light {self.language} editing for readability...")

        # Create light editor agent
        light_editor = get_light_editor_agent(self.llm, self.language)

        # Create editing task
        editing_task_description = create_light_editing_task(
            content=educational_script, language=self.language, title=paper_title
        )

        editing_task = Task(
            description=editing_task_description,
            agent=light_editor,
            expected_output=f"Educational script with minimal grammar corrections for {self.language} readability",
        )

        # Create a minimal crew with just the editor
        editing_crew = Crew(agents=[light_editor], tasks=[editing_task], verbose=True)

        # Run the crew
        result = editing_crew.kickoff()

        # Save editing data
        editing_data = {
            "project": self.project_name,
            "paper_title": paper_title,
            "language": self.language,
            "workflow": "light_edit",
            "original_length": len(educational_script),
            "edited_length": len(str(result)),
            "agent": {"role": light_editor.role, "goal": light_editor.goal},
        }

        # Save editing workflow data
        with open(
            self.discussion_dir / "light_edit_workflow.json", "w", encoding="utf-8"
        ) as f:
            json.dump(editing_data, f, indent=2, ensure_ascii=False)

        # Save both versions for comparison
        with open(
            self.discussion_dir / "script_before_edit.txt", "w", encoding="utf-8"
        ) as f:
            f.write(educational_script)

        with open(
            self.discussion_dir / "script_after_edit.txt", "w", encoding="utf-8"
        ) as f:
            f.write(str(result))

        print("✅ Light editing completed")
        return str(result).strip()

    def run_conversational_enhancement(
        self, technical_script: str, paper_title: str = ""
    ) -> str:
        """Apply minimal conversational touch to technical content for better readability.

        This is specifically for technical focus mode to create a version that's
        slightly more natural to read aloud while preserving all technical content.

        Args:
            technical_script: The technical script to enhance
            paper_title: Title of the paper

        Returns:
            The script with minimal conversational enhancements
        """
        import click

        click.echo("💬 Adding conversational touch for natural reading...")

        # Import the technical conversational functions
        from .conversational_enhancer import (
            get_technical_conversational_agent,
            create_technical_conversational_task
        )

        # Use different agent and task based on focus
        if self.focus == "technical":
            # For technical focus, restructure the knowledge naturally
            enhancer = get_technical_conversational_agent(self.llm)
            enhancement_task_description = create_technical_conversational_task(
                content=technical_script, language=self.language, title=paper_title
            )
            expected_output = f"Naturally structured presentation of objective knowledge in {self.language}"
        else:
            # For other focuses, just add minimal connectors
            enhancer = get_conversational_enhancer_agent(self.llm)
            enhancement_task_description = create_conversational_enhancement_task(
                content=technical_script, language=self.language, title=paper_title
            )
            expected_output = f"Technical script with minimal conversational enhancements for natural {self.language} reading"

        enhancement_task = Task(
            description=enhancement_task_description,
            agent=enhancer,
            expected_output=expected_output,
        )

        # Create a minimal crew
        enhancement_crew = Crew(
            agents=[enhancer], tasks=[enhancement_task], verbose=True
        )

        # Run the crew
        result = enhancement_crew.kickoff()

        # Save enhancement data
        enhancement_data = {
            "project": self.project_name,
            "paper_title": paper_title,
            "language": self.language,
            "workflow": "conversational_enhancement",
            "focus": self.focus,
            "original_length": len(technical_script),
            "enhanced_length": len(str(result)),
            "agent": {"role": enhancer.role, "goal": enhancer.goal},
        }

        # Save workflow data
        with open(
            self.discussion_dir / "conversational_enhancement_workflow.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(enhancement_data, f, indent=2, ensure_ascii=False)

        # Save both versions
        with open(
            self.discussion_dir / "technical_script_original.txt", "w", encoding="utf-8"
        ) as f:
            f.write(technical_script)

        with open(
            self.discussion_dir / "technical_script_conversational.txt",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(str(result))

        click.echo("✅ Conversational enhancement completed")
        return str(result).strip()

    def run_comprehensive_extraction_workflow(
        self, content: str, title: str, verify_coverage: bool = True
    ) -> str:
        """Run comprehensive multi-pass extraction workflow for complete content preservation.
        
        Args:
            content: The content to extract from
            title: The title of the content
            verify_coverage: Whether to verify coverage and enhance if needed
            
        Returns:
            Comprehensive extraction of all content
        """
        print(f"🔬 Starting comprehensive extraction with depth: {self.depth}")
        
        # Initialize analyzers
        multi_pass = MultiPassAnalyzer(self.llm)
        verifier = CoverageVerifier(self.llm) if verify_coverage else None
        agent_generator = DynamicAgentGenerator(self.llm)
        
        # Step 1: Run multi-pass analysis
        print("📊 Running multi-pass content analysis...")
        analysis_results = multi_pass.run_multi_pass_analysis(content, title)
        
        # Save analysis results
        analysis_path = self.synthesis_dir / "multi_pass_analysis.json"
        with open(analysis_path, "w", encoding="utf-8") as f:
            json.dump(analysis_results['content_analysis'], f, indent=2, ensure_ascii=False)
        
        # Step 2: Generate dynamic agents based on content
        print("🤖 Generating specialized agents based on content...")
        dynamic_agents = agent_generator.generate_agents_for_content(
            content, title, analysis_results['content_analysis']
        )
        
        # Step 3: Create exhaustive extractor
        exhaustive_extractor = create_exhaustive_extractor_agent(self.llm)
        
        # Step 4: Run comprehensive extraction
        print(f"📝 Running {self.depth} extraction...")
        extraction_task = create_comprehensive_extraction_task(
            content=content,
            title=title,
            extractor_agent=exhaustive_extractor,
            multi_pass_results=analysis_results,
            language=self.language
        )
        
        # Create crew with all specialized agents
        all_agents = dynamic_agents + [exhaustive_extractor]
        extraction_crew = Crew(
            agents=all_agents,
            tasks=[extraction_task],
            verbose=True
        )
        
        # Run extraction
        extraction_result = extraction_crew.kickoff()
        extracted_content = str(extraction_result)
        
        # Step 5: Verify coverage if requested
        if verify_coverage:
            print("✅ Verifying extraction coverage...")
            coverage_check = verifier.verify_coverage(content, extracted_content)
            
            # Save coverage report
            coverage_path = self.synthesis_dir / "coverage_verification.json"
            with open(coverage_path, "w", encoding="utf-8") as f:
                json.dump(coverage_check, f, indent=2, ensure_ascii=False)
            
            print(f"📊 Coverage: {coverage_check['coverage_checks']['coverage_percentage']:.1f}%")
            
            # If coverage is insufficient, enhance
            if not coverage_check['is_comprehensive']:
                print("🔧 Enhancing extraction to improve coverage...")
                completion_task = verifier.create_completion_task(
                    coverage_check['missing_elements'],
                    extracted_content,
                    exhaustive_extractor
                )
                
                completion_crew = Crew(
                    agents=[exhaustive_extractor],
                    tasks=[completion_task],
                    verbose=True
                )
                
                enhanced_result = completion_crew.kickoff()
                extracted_content = str(enhanced_result)
                
                # Re-verify
                final_check = verifier.verify_coverage(content, extracted_content)
                print(f"📊 Final coverage: {final_check['coverage_checks']['coverage_percentage']:.1f}%")
        
        # Save comprehensive extraction
        extraction_path = self.synthesis_dir / f"comprehensive_extraction_{self.depth}.txt"
        with open(extraction_path, "w", encoding="utf-8") as f:
            f.write(extracted_content)
        
        print(f"💾 Saved comprehensive extraction to: {extraction_path}")
        
        return extracted_content
    
    def run_exhaustive_workflow(self, paper_content: str, paper_title: str) -> str:
        """Run exhaustive extraction workflow followed by educational transformation.
        
        This is the most comprehensive workflow that ensures nothing is lost.
        """
        print("🚀 Starting EXHAUSTIVE extraction workflow...")
        
        # Step 1: Run comprehensive extraction with exhaustive depth
        original_depth = self.depth
        self.depth = "exhaustive"  # Force exhaustive depth
        
        extracted_content = self.run_comprehensive_extraction_workflow(
            paper_content, paper_title, verify_coverage=True
        )
        
        self.depth = original_depth  # Restore original depth
        
        # Step 2: Transform to educational format with completeness focus
        print("📚 Transforming to educational format with completeness focus...")
        
        # Get comprehensive prompts
        comp_prompts = ComprehensivePrompts()
        educational_prompt = comp_prompts.get_educational_completeness_prompt(
            self.language, self.duration_minutes, self.depth
        )
        
        # Create educational writer with completeness focus
        from .improved_educational_writer import get_improved_educational_writer
        educational_writer = get_improved_educational_writer(self.llm)
        
        # Override the agent's goal for completeness
        educational_writer.goal = "Transform content into COMPLETE educational script ensuring ALL information is preserved"
        
        # Create transformation task
        transform_task = Task(
            description=f"""
            {educational_prompt}
            
            Title: {paper_title}
            
            Content to transform (PRESERVE EVERYTHING):
            {extracted_content}
            """,
            agent=educational_writer,
            expected_output=f"Complete educational script in {self.language} with ALL content preserved"
        )
        
        # Run transformation
        transform_crew = Crew(
            agents=[educational_writer],
            tasks=[transform_task],
            verbose=True
        )
        
        result = transform_crew.kickoff()
        final_script = str(result)
        
        # Save the exhaustive educational script
        script_path = self.project_dir / f"exhaustive_educational_script_{self.depth}.txt"
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(final_script)
        
        print(f"✅ Exhaustive workflow complete! Script saved to: {script_path}")
        
        return final_script
    
    def run_technical_preservation_workflow(
        self, paper_content: str, paper_title: str
    ) -> str:
        """Run technical preservation workflow that maintains all technical details.
        
        This workflow is optimized for technical audiences who need complete accuracy.
        """
        print("🔬 Starting technical preservation workflow...")
        
        # Step 1: Extract with technical focus
        comp_prompts = ComprehensivePrompts()
        technical_prompt = comp_prompts.get_technical_preservation_prompt("technical")
        
        # Create technical extractor
        technical_extractor = Agent(
            role="Technical Content Preservation Specialist",
            goal="Preserve ALL technical content with complete accuracy",
            backstory=technical_prompt,
            llm=self.llm,
            verbose=True
        )
        
        # Create extraction task
        extraction_task = Task(
            description=f"""
            Extract and preserve ALL technical content from this document.
            
            Title: {paper_title}
            
            CRITICAL: Preserve every formula, equation, algorithm, data point, and technical specification.
            
            Content:
            {paper_content}
            
            Remember: NO simplification, NO summarization. Keep EVERYTHING technical.
            """,
            agent=technical_extractor,
            expected_output="Complete technical content with all details preserved"
        )
        
        # Run extraction
        extraction_crew = Crew(
            agents=[technical_extractor],
            tasks=[extraction_task],
            verbose=True
        )
        
        technical_result = extraction_crew.kickoff()
        technical_content = str(technical_result)
        
        # Step 2: Create technical documentation
        from .technical_writer import get_technical_writer_agent
        tech_writer = get_technical_writer_agent(self.llm)
        
        # Override for preservation focus
        tech_writer.goal = "Create comprehensive technical documentation preserving all details"
        
        doc_task = Task(
            description=f"""
            Create comprehensive technical documentation from this extracted content.
            
            Requirements:
            1. Keep ALL technical details
            2. Maintain precise terminology
            3. Preserve all formulas and equations
            4. Include all code and algorithms
            5. Document all methodologies
            6. Keep all data and results
            
            Title: {paper_title}
            
            Technical Content:
            {technical_content}
            
            Language: {self.language}
            """,
            agent=tech_writer,
            expected_output=f"Comprehensive technical documentation in {self.language}"
        )
        
        # Run documentation
        doc_crew = Crew(
            agents=[tech_writer],
            tasks=[doc_task],
            verbose=True
        )
        
        final_result = doc_crew.kickoff()
        final_documentation = str(final_result)
        
        # Save technical documentation
        doc_path = self.project_dir / "technical_preservation_documentation.txt"
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(final_documentation)
        
        print(f"✅ Technical preservation complete! Documentation saved to: {doc_path}")
        
        return final_documentation