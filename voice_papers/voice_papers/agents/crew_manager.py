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

    def _get_base_agents_for_focus(self) -> List[Agent]:
        """Get base agents for non-critical focus modes."""
        agents = []

        # Coordinator for all modes
        agents.append(
            Agent(
                role="Research Coordinator",
                goal="Facilitate productive discussion about the paper's content",
                backstory="""You are an experienced research coordinator who ensures discussions 
            stay focused on the paper's content. You help organize thoughts and ensure all 
            important points from the paper are covered. You ONLY discuss what's in the paper.""",
                llm=self.llm,
                verbose=True,
            )
        )

        # Scientific Reviewer for explanatory modes
        if self.focus != "story":  # Story mode doesn't need scientific review
            agents.append(
                Agent(
                    role="Methodology Explainer",
                    goal="Explain the research methodology and approach as described in the paper",
                    backstory="""You are skilled at understanding and explaining research methodologies. 
                You help audiences understand how the research was conducted, what methods were used, 
                and why. You ONLY explain methods actually described in the paper.""",
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
            agents.append(
                Agent(
                    role="Comedy Communicator",
                    goal="Add appropriate humor while maintaining educational value",
                    backstory="""You are a science comedy writer who knows how to make learning fun 
                without sacrificing accuracy. You add wit, clever observations, and playful elements 
                that enhance understanding. You work only with the paper's content, finding the 
                inherent humor in the research itself.""",
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

        # For original synthesis, create agents
        chunk_analyzer = Agent(
            role="Deep Document Analyzer",
            goal="Extract comprehensive insights from each section of the document",
            backstory="""You are a meticulous researcher who never misses important details.
            You have the ability to understand complex arguments, identify key evidence,
            and recognize the significance of findings. You preserve depth and nuance.""",
            llm=self.llm,
            verbose=True,
        )

        synthesizer = Agent(
            role="Master Synthesizer",
            goal="Combine all section analyses into a comprehensive, coherent understanding",
            backstory="""You are brilliant at seeing the big picture while retaining important
            details. You can identify patterns across sections, understand how arguments build,
            and create a unified narrative that captures both breadth and depth.""",
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

        # Create synthesis task
        synthesis_task = Task(
            description=f"""
            You have received detailed analyses of all {len(chunks)} sections of the paper "{paper_title}".
            
            Create a comprehensive synthesis that EXTRACTS and PRESENTS the actual content, NOT a meta-analysis about the paper.
            
            CRITICAL: Present the IDEAS, FINDINGS, and ARGUMENTS themselves, not descriptions of them.
            
            WRONG: "The paper discusses three main approaches to..."
            RIGHT: "The three approaches are: 1) X works by... 2) Y achieves... 3) Z enables..."
            
            WRONG: "The authors present evidence showing..."
            RIGHT: "The evidence shows that X increased by 47% when..."
            
            Structure your synthesis as follows:
            
            **TLDR:** (3-5 bullet points)
            - The core discovery/argument in one clear statement
            - 2-3 key findings with specific details
            - The main implication or breakthrough
            
            **MAIN THESIS/ARGUMENT:**
            State the central claim or discovery directly. What IS the finding, not what the paper says about it.
            
            **KEY POINTS WITH SUPPORTING EVIDENCE:**
            1. First major point: [State it directly]
               - Evidence: [Specific data, results, or reasoning]
               - Why it matters: [Direct implication]
            
            2. Second major point: [State it directly]
               - Evidence: [Specific data, results, or reasoning]
               - Why it matters: [Direct implication]
            
            [Continue for all major points]
            
            **SECONDARY INSIGHTS:**
            - List additional findings, observations, or contributions
            - Include specific details, numbers, or mechanisms
            
            **EXAMPLES AND APPLICATIONS:**
            - Concrete examples given in the paper
            - Real-world applications or use cases
            - Specific scenarios or case studies
            
            **METHODOLOGY HIGHLIGHTS:** (if relevant)
            - Key approaches or techniques used
            - Novel methods introduced
            - Important experimental details
            
            **CONCLUSIONS AND IMPLICATIONS:**
            - What can we now do/know that we couldn't before?
            - Specific future directions mentioned
            - Concrete impact on the field
            
            Remember: You are extracting and organizing the ACTUAL CONTENT, not describing what the paper contains.
            Write as if you are teaching the concepts directly, not reviewing a paper.
            """,
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
            if agent.role not in ["Master Educational Science Communicator & Storyteller", "Comedy Communicator"]
        ]
        post_production_agents = [
            agent
            for agent in agents
            if agent.role in ["Master Educational Science Communicator & Storyteller", "Comedy Communicator"]
        ]

        # Initial analysis task - CONVERSATION AGENTS ONLY (NO HUMOR)
        tasks.append(
            Task(
                description=f"""
            Analyze the synthesis of the paper titled "{paper_title}" and provide your perspective.
            
            Paper synthesis:
            {paper_content}
            
            CRITICAL: ONLY CONVERSATION AGENTS participate in this analysis:
            - Base agents (Coordinator, Scientific Reviewer, Critical Thinker)
            - Specialized domain agents
            
            EXCLUDED FROM ANALYSIS: Master Educational Science Communicator & Storyteller and Comedy Communicator (work in post-production)
            
            Each participating agent should:
            1. Read and understand the paper from your specific role's perspective
            2. Identify key points relevant to your expertise
            3. Prepare questions or concerns to discuss
            4. Consider the implications from your unique viewpoint
            
            SPECIALIZED AGENTS: Pay special attention to domain-specific aspects that only you can address.
            
            This should be a comprehensive TECHNICAL analysis where EVERY conversation agent contributes their specialized perspective.
            
            Language: {self.language}
            """,
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
                if agent.role not in ["Master Educational Science Communicator & Storyteller", "Comedy Communicator"]
            ]
            if conversation_specialists:
                lead_specialist = conversation_specialists[0]
                tasks.append(
                    Task(
                        description=f"""
                    SPECIALIZED AGENTS DEEP DIVE: Domain expertise from TECHNICAL conversation agents only.
                    
                    PARTICIPATING SPECIALIZED AGENTS (technical focus):
                    {", ".join([f"- {agent.role}: {agent.goal}" for agent in conversation_specialists])}
                    
                    EXCLUDED: Comedy Communicator (works in post-production phase)
                    
                    Each specialized agent should:
                    1. Provide deep domain-specific insights about the paper
                    2. Identify methodological issues specific to your field
                    3. Highlight implications that only someone with your expertise would notice
                    4. Suggest domain-specific improvements or alternative approaches
                    5. Connect this work to other research in your specialized area
                    
                    This is YOUR moment to shine with specialized knowledge that the base agents cannot provide.
                    Focus on TECHNICAL DEPTH and DOMAIN EXPERTISE.
                    Format as a detailed specialist consultation with clear attribution to each expert.
                    
                    Language: {self.language}
                    """,
                        agent=lead_specialist,
                        expected_output=f"Deep technical specialist analysis from {len(conversation_specialists)} domain experts",
                    )
                )

        # NUEVA TAREA: Ronda de Preguntas Cruzadas - CONVERSATION AGENTS ONLY (NO HUMOR)
        tone_instructions = self._get_tone_instructions()
        tasks.append(
            Task(
                description=f"""
            Based on the initial analysis, conduct a DYNAMIC Q&A session where technical conversation agents ask each other specific questions about the paper synthesis.
            
            PARTICIPATING AGENTS (technical conversation only):
            - Base conversation agents (Coordinator, Scientific Reviewer, Critical Thinker) 
            - ALL specialized domain agents
            
            EXCLUDED FROM CONVERSATION: Master Educational Science Communicator & Storyteller and Comedy Communicator (work in post-production)
            
            Instructions for multi-agent technical conversation:
            1. ALL TECHNICAL CONVERSATION AGENTS should ask pointed questions to other agents
            2. SPECIALIZED AGENTS should ask domain-specific questions that challenge assumptions
            3. BASE AGENTS should ask specialists to clarify complex domain concepts
            4. Agents must respond to questions directed at them with detailed technical answers
            5. Follow-up questions and clarifications are encouraged
            6. Challenge each other's assumptions respectfully
            7. Build on each other's ideas and insights
            8. Create a natural back-and-forth technical dialogue
            
            SPECIALIZED AGENTS: This is crucial - ask questions only YOU would think to ask!
            
            Focus areas for technical questions:
            - Domain-specific methodological concerns
            - Interdisciplinary connections and conflicts
            - Alternative interpretations from different expert perspectives
            - Practical applications in each specialist's field
            - Potential limitations or biases from multiple viewpoints
            
            Format this as a realistic TECHNICAL conversation with clear speaker identification for ALL conversation participants.
            Keep the tone SERIOUS and TECHNICAL - humor will be added later in post-production.
            
            Language: {self.language}
            """,
                agent=agents[2],  # Critical Thinker facilitates
                expected_output="Dynamic technical Q&A conversation between conversation agents only (no post-production or humor)",
            )
        )

        # NUEVA TAREA: Debate de Perspectivas Contrarias - CONVERSATION AGENTS ONLY (NO HUMOR)
        tasks.append(
            Task(
                description=f"""
            Organize a structured technical debate where conversation agents with different viewpoints engage in deeper discussion.
            
            PARTICIPATING AGENTS (technical conversation only):
            - Base conversation agents (Coordinator, Scientific Reviewer, Critical Thinker)
            - ALL specialized domain agents  
            
            EXCLUDED FROM DEBATE: Master Educational Science Communicator & Storyteller and Comedy Communicator (work in post-production)
            
            Technical debate structure:
            1. Present the main controversial points or interpretations from the paper
            2. Have TECHNICAL CONVERSATION AGENTS take different positions and argue their cases
            3. SPECIALIZED AGENTS: Argue from your domain expertise - what would your field say?
            4. Allow for rebuttals and counter-arguments between different expert perspectives
            5. Explore edge cases and hypothetical scenarios from multiple disciplinary angles
            6. Find areas of agreement and persistent disagreements between different specialties
            7. Synthesize different viewpoints into a richer technical understanding
            
            This should feel like a real interdisciplinary TECHNICAL conference where:
            - Different specialists bring unique perspectives that sometimes conflict
            - Domain experts interrupt each other (politely) to make field-specific points
            - Ideas evolve through interaction between different areas of expertise
            - New insights emerge from cross-disciplinary exchange
            - There's intellectual tension between different specialist viewpoints
            
            SPECIALIZED AGENTS: Don't hold back - defend your field's perspective!
            
            Make it conversational and dynamic, but keep TECHNICAL FOCUS - humor will be added later.
            
            Language: {self.language}
            """,
                agent=agents[1],  # Scientific Reviewer moderates debate
                expected_output="Rich interdisciplinary technical debate between conversation agents only (no post-production or humor)",
            )
        )

        # NUEVA TAREA: Conversación de Síntesis Colaborativa - CONVERSATION AGENTS ONLY (NO HUMOR)
        tasks.append(
            Task(
                description=f"""
            Conduct a collaborative synthesis where technical conversation agents work together to build a comprehensive understanding.
            
            PARTICIPATING AGENTS (technical conversation only):
            - Base conversation agents (Coordinator, Scientific Reviewer, Critical Thinker)
            - ALL specialized domain agents
            
            EXCLUDED FROM SYNTHESIS: Master Educational Science Communicator & Storyteller and Comedy Communicator (work in post-production)
            
            Technical collaborative process:
            1. ALL TECHNICAL CONVERSATION AGENTS contribute their key insights from the discussions
            2. SPECIALIZED AGENTS highlight unique perspectives only your field can provide
            3. Agents build on each other's contributions in real-time
            4. Identify connections between different specialist perspectives
            5. Resolve conflicting interpretations through interdisciplinary dialogue
            6. Co-create new insights that emerge from cross-domain discussion
            7. Establish consensus on the most important takeaways from ALL conversation perspectives
            
            This should be a generative TECHNICAL conversation where:
            - Ideas from one specialist spark new ideas in other specialists
            - The group intelligence exceeds individual specialist perspectives
            - Agents actively listen and respond to insights from other domains
            - The conversation flows naturally between different areas of expertise
            - New understanding emerges from interdisciplinary interaction
            - Each specialist's unique knowledge contributes to the whole
            
            SPECIALIZED AGENTS: Share insights that ONLY someone with your expertise would have!
            
            Format as natural TECHNICAL conversation with organic transitions between specialist viewpoints.
            Keep SERIOUS and FOCUSED - entertainment will be added later in post-production.
            
            Language: {self.language}
            """,
                agent=agents[0],  # Coordinator leads synthesis
                expected_output="Collaborative technical synthesis conversation from conversation agents only (no post-production or humor)",
            )
        )

        # Existing Discussion task - CONVERSATION AGENTS FINAL TECHNICAL SUMMARY
        tasks.append(
            Task(
                description=f"""
            Based on all previous conversations and analyses, conduct a final comprehensive technical discussion that synthesizes insights from conversation agents.
            
            PARTICIPATING AGENTS (technical conversation only):
            - Base conversation agents (Coordinator, Scientific Reviewer, Critical Thinker)
            - ALL specialized domain agents
            
            EXCLUDED: Master Educational Science Communicator & Storyteller and Comedy Communicator (they will process this output in post-production)
            
            The final technical discussion should:
            1. Synthesize insights from the Q&A, specialist deep dive, debate, and collaborative sessions
            2. Cover all major points of the paper from multiple expert perspectives
            3. Include the rich specialist perspectives developed through agent interactions
            4. Address concerns and criticisms that emerged from different domains
            5. Explore implications and applications discussed by various specialists
            6. Be comprehensive and technically rigorous for expert audiences
            7. Highlight unique insights that could ONLY come from having multiple specialist perspectives
            
            CRITICAL: This final technical discussion must incorporate:
            - Domain-specific insights from ALL specialist conversation agents
            - Cross-disciplinary connections discovered during discussions
            - Unique perspectives that emerged from interdisciplinary dialogue
            - Technical depth and rigor appropriate for expert audiences
            
            This is the FINAL technical conversation output that will be handed to the post-production team.
            Make it comprehensive, rigorous, and rich with all the insights gathered.
            Keep it TECHNICAL and SERIOUS - post-production will handle accessibility and entertainment.
            
            Language: {self.language}
            """,
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
            tasks.append(
                Task(
                    description=f"""
                POST-PRODUCTION PHASE 1: COMEDY ENHANCEMENT
                
                You are receiving ALL the serious technical conversations from the conversation phase.
                Your job is to add appropriate humor and entertainment value while maintaining respect for the science.
                
                Technical content processed so far includes:
                - Initial analysis from all conversation agents
                - Specialized domain expert deep dive
                - Dynamic Q&A sessions between experts  
                - Interdisciplinary technical debates
                - Collaborative synthesis
                - Final comprehensive technical discussion
                
                Review ALL this technical content and:
                1. Identify moments where humor can enhance understanding
                2. Create clever analogies that make complex concepts memorable
                3. Find amusing but respectful observations about the research
                4. Develop entertaining examples that illustrate key points
                5. Add witty commentary that makes the discussion more engaging
                6. Use wordplay and clever observations appropriate to the topic
                7. Insert humor that bridges different specialist perspectives
                8. Make technical debates more entertaining without losing substance
                9. Add comic relief to dense technical discussions
                10. Create memorable one-liners that help key concepts stick
                
                Your goal is to make the content more accessible and entertaining WITHOUT undermining the scientific rigor.
                Think Neil deGrasse Tyson explaining astrophysics - serious science, but delivered with wit and charm.
                
                The output should be the SAME technical content but now enhanced with appropriate humor and entertainment.
                You are NOT writing the final script - you're adding humor to the technical discussions.
                
                {tone_instructions}
                
                Language: {self.language}
                """,
                    agent=humor_agent,
                    expected_output="Technical content enhanced with appropriate humor and entertainment while maintaining scientific accuracy",
                )
            )

        # POST-PRODUCTION PHASE 2: Educational/Technical Writer processes ALL content
        if self.focus == "technical":
            educational_writer = next(
                agent for agent in agents if agent.role == "Technical Content Specialist"
            )
        else:
            educational_writer = next(
                agent for agent in agents if agent.role == "Master Educational Science Communicator & Storyteller"
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
            
            {create_technical_writing_task(
                content="Use the complete discussion from all previous tasks",
                title=paper_title,
                target_length="comprehensive",
                language=self.language
            )}
            """
            
            technical_task = Task(
                description=technical_task_desc,
                agent=educational_writer,
                expected_output="Technical presentation with zero interpretation - only facts and concepts as stated",
                context=[previous_task_context] if previous_task_context else []
            )
            tasks.append(technical_task)
        else:
            # Regular educational writing task
            tasks.append(
                Task(
                    description=f"""
            POST-PRODUCTION PHASE 2: EDUCATIONAL SCRIPT CREATION
            
            Transform ALL the rich content into a comprehensive educational lecture text.
            
            DOCUMENT TITLE: {paper_title}
            
            You are receiving the complete output, which includes:
            - Initial analysis from all conversation agents
            - Specialized domain expert deep dive
            - Dynamic Q&A sessions between experts
            - Interdisciplinary technical debates
            - Collaborative synthesis
            - Final comprehensive technical discussion
            {"- Comedy-enhanced version with appropriate humor" if has_humor_agent else ""}
            
            Your job is to distill ALL this rich content into a single educator voice.
            
            The script MUST follow the Voice Papers style guide structure:
            
            1. NARRATIVE STRUCTURE (from style guide):
               - START with one of these hook types, not exactly, just use the style guide:
                 • Escenario relatable: "Digamos que estás planeando unas vacaciones con tu familia..."
                 • Contexto histórico: "En octubre de 1997, en Atlanta Georgia..."
                 • Alarma/problema: "Si eres como yo, ya te están sonando las alarmas..."
                 • Pregunta intrigante: "¿Alguna vez te has preguntado por qué...?"
               - THEN naturally introduce "{paper_title}" after the hook, if not stated explicitly do not use it
               - Structure as three acts when possible: Problema → Solución → Implicaciones
               - NEVER start with: "En resumen", "Hoy vamos a hablar de", "Este es un resumen de"
            
            2. CONVERSATIONAL TONE (Voice Papers style):
               - Written as a SINGLE EDUCATOR speaking directly (use "tú"/"usted")
               - Use frequent rhetorical questions: "¿Parece simple, no?", "¿Te suena familiar?"
               - Show personality: "En mi opinión...", "Lo que más me sorprende es..."
            3. TECHNICAL EXPLANATIONS (Voice Papers layered approach):
               - Start with the simplest version of the concept
               - Add complexity gradually in layers
               - Define terms naturally in flow: "esto se llama X, que básicamente significa..."
               - Use MINIMUM 2-3 analogies per script from everyday life
            
            4. RHYTHM AND FLOW (style guide requirements):
               - Mix sentence lengths: short for impact, long for explanation
               - Natural transitions: "Ahora bien...", "Pero aquí está lo interesante..."
               - Create expectation: "En un momento veremos algo sorprendente..."
               - Strategic pauses and emphasis for voice delivery
            
            5. STORYTELLING (academic narrative from style guide):
               - Humanize when possible: "Los investigadores se sorprendieron cuando..."
               - Create narrative tension before revealing findings
            
            6. CORE REQUIREMENTS:
               - Include ALL key insights from conversations and specialist exchanges
               - Flow naturally with smooth transitions between concepts
               - Write as continuous text for voice actor (no headers/formatting)
               - Address listener directly: "puedes imaginar", "te darás cuenta"
               - End with practical implications and thought-provoking questions
               - Incorporate depth from ALL agent conversations
            
            STYLE GUIDE CHECKLIST - ALL ITEMS MANDATORY:
            ✓ Hook: Used one of the 4 exact types from style guide?
            ✓ Direct address: Speaking to "tú" throughout?
            ✓ Transitions: Natural connectors between ideas?
            ✓ Rhythm: Varied sentence lengths for flow?
            
            CRITICAL DIDACTIC STRUCTURE:
            - INTRODUCTION: Hook → Title → Preview ("En los próximos minutos descubrirás...")
            - DEVELOPMENT: Layered explanations with examples
            - CONCLUSION: Clear recap ("Hemos visto que...", "Para cerrar...")
            - The script should not be necessarily inspirational, it should be a technical explanation of content
            NATURAL LANGUAGE REQUIREMENTS:
            - AVOID: fundamental, crucial, esencial, revelador, fascinante, delve, robust <- THIS IS MANDATORY
            - USE: importante, interesante, sorprendente, resulta que, descubrimos que
            - Sound like explaining to a curious friend, not generating content
            
            CRITICAL - MULTI-SPECIALIST INTEGRATION:
            19. Weave in insights that could ONLY come from having multiple specialist perspectives
            20. Include cross-disciplinary connections discovered during discussions
            21. Incorporate domain-specific knowledge from ALL participating specialists
            
            {"23. Naturally integrate the entertaining elements added by the Comedy Communicator" if has_humor_agent else ""}
            {"24. Demonstrate the value of interdisciplinary analysis throughout" if has_humor_agent else "23. Demonstrate the value of interdisciplinary analysis throughout"}
            
            {technical_instructions}
            
            {duration_instructions}
            
            {language_instructions}
            
            Language: {self.language}
            """,
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
            if agent.role not in ["Master Educational Science Communicator & Storyteller", "Comedy Communicator"]
        ]
        post_production_agents = [
            agent
            for agent in agents
            if agent.role in ["Master Educational Science Communicator & Storyteller", "Comedy Communicator"]
        ]

        # Original Initial analysis task - CONVERSATION AGENTS ONLY (NO HUMOR)
        tasks.append(
            Task(
                description=f"""
            Analyze the synthesis of the paper titled "{paper_title}" and provide your perspective.
            
            Paper synthesis:
            {paper_content}
            
            PARTICIPATING AGENTS (technical conversation only):
            - Base conversation agents (Coordinator, Scientific Reviewer, Critical Thinker)
            - ALL specialized domain agents
            
            EXCLUDED FROM ANALYSIS: Master Educational Science Communicator & Storyteller and Comedy Communicator (work in post-production)
            
            Each participating conversation agent should:
            1. Read and understand the paper from your specific role's perspective
            2. Identify key points relevant to your expertise
            3. Prepare questions or concerns to discuss
            4. Consider the implications from your unique viewpoint
            
            SPECIALIZED AGENTS: Include your domain-specific insights that only you can provide.
            
            Keep this TECHNICAL and SERIOUS - entertainment will be added later in post-production.
            
            Language: {self.language}
            """,
                agent=agents[0],  # Coordinator leads
                expected_output="Initial technical analysis and key points from conversation agents (no post-production agents)",
            )
        )

        # Original Discussion task - CONVERSATION AGENTS ONLY (NO HUMOR)
        tasks.append(
            Task(
                description=f"""
            Based on the initial analysis, conduct a thorough technical discussion of the paper synthesis involving conversation agents.
            
            PARTICIPATING AGENTS (technical conversation only):
            - Base conversation agents (Coordinator, Scientific Reviewer, Critical Thinker)
            - ALL specialized domain agents
            
            EXCLUDED FROM DISCUSSION: Master Educational Science Communicator & Storyteller and Comedy Communicator (they process the output in post-production)
            
            The technical discussion should:
            1. Cover all major points of the paper
            2. Include different perspectives from conversation agents (base + specialists)
            3. Address potential concerns and criticisms from multiple expert viewpoints
            4. Explore implications and applications from various specialist domains
            5. Be comprehensive and technically rigorous
            
            SPECIALIZED AGENTS: This is your chance to contribute domain expertise!
            
            Create a rich technical dialogue that showcases multiple expert perspectives.
            This is the FINAL conversation output that will be handed to the post-production team.
            Keep it TECHNICAL and SERIOUS - post-production will handle accessibility and entertainment.
            
            Language: {self.language}
            """,
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
            tasks.append(
                Task(
                    description=f"""
                POST-PRODUCTION PHASE 1: COMEDY ENHANCEMENT
                
                You are receiving the serious technical conversations from the conversation phase.
                Your job is to add appropriate humor and entertainment value while maintaining respect for the science.
                
                Technical content processed so far includes:
                - Initial analysis from all conversation agents
                - Comprehensive technical discussion between all expert perspectives
                
                Review ALL this technical content and:
                1. Identify moments where humor can enhance understanding
                2. Create clever analogies that make complex concepts memorable
                3. Find amusing but respectful observations about the research
                4. Develop entertaining examples that illustrate key points
                5. Add witty commentary that makes the discussion more engaging
                6. Use wordplay and clever observations appropriate to the topic
                7. Insert humor that bridges different specialist perspectives
                8. Make the technical discussion more entertaining without losing substance
                9. Add comic relief to dense technical discussions
                10. Create memorable one-liners that help key concepts stick
                
                Your goal is to make the content more accessible and entertaining WITHOUT undermining the scientific rigor.
                Think Neil deGrasse Tyson explaining astrophysics - serious science, but delivered with wit and charm.
                
                The output should be the SAME technical content but now enhanced with appropriate humor and entertainment.
                You are NOT writing the final script - you're adding humor to the technical discussions.
                
                {tone_instructions}
                
                Language: {self.language}
                """,
                    agent=humor_agent,
                    expected_output="Technical content enhanced with appropriate humor and entertainment while maintaining scientific accuracy",
                )
            )

        # POST-PRODUCTION PHASE 2: Master Educational Science Communicator & Storyteller transforms conversations
        educational_writer = next(
            agent for agent in agents if agent.role == "Master Educational Science Communicator & Storyteller"
        )
        technical_instructions = self._get_technical_instructions()
        duration_instructions = self._get_duration_instructions()
        language_instructions = self._get_language_instructions()

        tasks.append(
            Task(
                description=f"""
            POST-PRODUCTION PHASE 2: EDUCATIONAL SCRIPT CREATION
            
            Transform the conversation into a comprehensive educational lecture text.
            
            You are receiving the complete output from the conversation phase, which included:
            - Initial analysis from all conversation agents
            - Comprehensive discussion between all expert perspectives
            {"- Comedy-enhanced version with appropriate humor" if has_humor_agent else ""}
            
            Your job is to distill ALL this rich content into a single educator voice.
            
            The script MUST follow the Voice Papers style guide:
            
            1. NARRATIVE STRUCTURE (mandatory from style guide):
               - Hook: Use one of the 4 exact types (escenario, histórico, alarma, pregunta)
               - Development: Three acts when possible (Problema → Solución → Implicaciones)
               - Closure: Practical conclusions with future vision
            
            2. CONVERSATIONAL ELEMENTS (required):
               - Single educator voice speaking directly ("tú"/"usted")
               - Rhetorical questions throughout: "¿No es sorprendente?"
               - Personal touches: "En mi opinión...", "Me fascina que..."
               - Direct address: "puedes imaginar", "te darás cuenta"
            
            3. TECHNICAL EXPLANATIONS (layered approach):
               - Start simple, add complexity gradually
               - Define terms naturally in flow
               - Minimum 2-3 everyday analogies
               - Connect abstract to concrete
            
            4. ENGAGEMENT TECHNIQUES:
               - Create expectation and suspense
               - Guide thinking with questions
               - Include "aha!" moments
               - Moments of wonder and curiosity
            
            5. INTEGRATION REQUIREMENTS:
               - Include ALL specialist perspectives
               - Show cross-disciplinary connections
               - Weave insights naturally (not "experts said")
               - Write as YOU teaching, not summarizing
            
            6. FORMAT:
               - Continuous text for voice (no headers/marks)
               - Natural flow between concepts
               - End with practical implications and questions
               - Plain text optimized for speech
            
            CRITICAL DIDACTIC TECHNIQUES - MANDATORY:
            21. INTRODUCTION must include a compelling preview/roadmap: Start with an engaging hook and then preview what the listener will learn - "En los próximos minutos vas a descubrir...", "Te voy a mostrar tres ideas que cambiarán tu forma de pensar sobre...", etc.
            22. CONCLUSION must include a clear summary: End with a recap of the main points covered - "Hemos visto que...", "En resumen, tres puntos clave...", "Para cerrar, recordemos que...", etc.
            23. AVOID TYPICAL LLM WORDS: Never use overused AI-generated words like "fundamental", "crucial", "clave" (as adjective), "esencial", "revelador", "fascinante", "delve into", "explore", "unpack", "dive deep", "robust", "compelling", etc.
            24. USE NATURAL LANGUAGE: Instead of LLM words, use conversational alternatives like "importante", "interesante", "sorprendente", "nos ayuda a entender", "vamos a ver", "resulta que", "descubrimos que", etc.
            25. SOUND HUMAN: Write as if explaining to a friend over coffee, not as if generating academic content
            {"21. Naturally integrate the entertaining elements added by the Comedy Communicator" if has_humor_agent else ""}
            
            {technical_instructions}
            
            {duration_instructions}
            
            {language_instructions}
            
            Language: {self.language}
            """,
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

        # Create agents based on focus mode
        if self.focus == "technical":
            # Use technical agents for zero interpretation
            chunk_analyzer = Agent(
                role="Technical Document Analyzer",
                goal="Extract facts, data, and specifications from each section with zero interpretation",
                backstory="""You are a technical documentation specialist. You extract information
                exactly as stated without adding any interpretation, implications, or subjective language.
                You remove interpretive adjectives like 'revolutionary', 'groundbreaking', etc.
                You present only facts, methods, and results.""",
                llm=self.llm,
                verbose=True,
            )

            synthesizer = Agent(
                role="Technical Synthesizer",
                goal="Combine section analyses into a factual, objective technical summary",
                backstory="""You combine technical information without interpretation. You organize
                facts, data, and methods in a clear structure. You never add implications or suggestions
                beyond what's explicitly stated. You maintain objectivity and technical accuracy.""",
                llm=self.llm,
                verbose=True,
            )

            educational_writer = get_technical_writer_agent(self.llm)
        else:
            # Use standard agents for other focus modes
            chunk_analyzer = Agent(
                role="Deep Document Analyzer",
                goal="Extract comprehensive insights from each section of the document",
                backstory="""You are a meticulous researcher who never misses important details.
                You have the ability to understand complex arguments, identify key evidence,
                and recognize the significance of findings. You preserve depth and nuance.""",
                llm=self.llm,
                verbose=True,
            )

            synthesizer = Agent(
                role="Master Synthesizer",
                goal="Combine all section analyses into a comprehensive, coherent understanding",
                backstory="""You are brilliant at seeing the big picture while retaining important
                details. You can identify patterns across sections, understand how arguments build,
                and create a unified narrative that captures both breadth and depth.""",
                llm=self.llm,
                verbose=True,
            )

            educational_writer = get_improved_educational_writer(self.llm)

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
                    # Technical analysis prompt - zero interpretation
                    chunk_description = f"""
                    Extract technical information from this section.
                    
                    CRITICAL RULES:
                    1. NEVER use meta-language: "el documento presenta", "se discute", "el análisis aborda"
                    2. Extract and list THE ACTUAL CONTENT, not that it was discussed
                    3. If the text says "tres enfoques principales", LIST what those approaches ARE
                    4. Present data, specifications, and methods directly
                    
                    WRONG: "El documento presenta tres enfoques"
                    RIGHT: "Los tres enfoques son: [list actual approaches if mentioned]"
                    
                    WRONG: "Se discute una reducción de costos del 40%"
                    RIGHT: "Reducción de costos: 40%"
                    
                    Content to analyze:
                    {chunk.content}
                    
                    Extract and present the ACTUAL technical information. If specific details aren't provided, state what IS provided.
                    """
                    expected = f"Direct technical content from {chunk.section_title} - no meta-language"
                else:
                    chunk_description = chunker.create_chunk_summary_prompt(chunk, paper_title)
                    expected = f"Comprehensive analysis of {chunk.section_title}"
                
                chunk_task = Task(
                    description=chunk_description,
                    agent=chunk_analyzer,
                    expected_output=expected,
                )
                chunk_tasks.append(chunk_task)

            # Create synthesis task
            if self.focus == "technical":
                synthesis_description = f"""
                You have received technical analyses of all {len(chunks)} sections.
                
                Create a TECHNICAL SYNTHESIS that presents ONLY the facts, data, and specifications.
                
                CRITICAL RULES:
                1. NO META-LANGUAGE: Never say "se presenta", "se discute", "se aborda"
                2. Present THE ACTUAL TECHNICAL CONTENT, not that it was discussed
                3. List specifications, methods, and results directly
                4. Remove ALL interpretive language
                
                WRONG: "Se abordan las implicaciones del model as a service"
                RIGHT: "El 'model as a service' implica: 1) X, 2) Y, 3) Z"
                
                WRONG: "El análisis presenta tres métodos"
                RIGHT: "Los tres métodos son: método A [descripción], método B [descripción], método C [descripción]"
                
                Structure:
                - Technical specifications and data
                - Methods and algorithms (as lists or steps)
                - Results and measurements (exact numbers)
                - System components and architecture
                
                Present ONLY factual technical information. Zero interpretation.
                """
            else:
                synthesis_description = f"""
                You have received detailed analyses of all {len(chunks)} sections of the paper "{paper_title}".
                
                Create a comprehensive synthesis that EXTRACTS and PRESENTS the actual content, NOT a meta-analysis about the paper.
                
                CRITICAL: Present the IDEAS, FINDINGS, and ARGUMENTS themselves, not descriptions of them.
                
                WRONG: "The paper discusses three main approaches to..."
                RIGHT: "The three approaches are: 1) X works by... 2) Y achieves... 3) Z enables..."
                
                WRONG: "The authors present evidence showing..."
                RIGHT: "The evidence shows that X increased by 47% when..."
                
                Structure your synthesis as follows:
                
                **TLDR:** (3-5 bullet points)
                - The core discovery/argument in one clear statement
                - 2-3 key findings with specific details
                - The main implication or breakthrough
                
                **MAIN THESIS/ARGUMENT:**
                State the central claim or discovery directly. What IS the finding, not what the paper says about it.
                
                **KEY POINTS WITH SUPPORTING EVIDENCE:**
                1. First major point: [State it directly]
                   - Evidence: [Specific data, results, or reasoning]
                   - Why it matters: [Direct implication]
                
                2. Second major point: [State it directly]
                   - Evidence: [Specific data, results, or reasoning]
                   - Why it matters: [Direct implication]
                
                [Continue for all major points]
                
                **SECONDARY INSIGHTS:**
                - List additional findings, observations, or contributions
                - Include specific details, numbers, or mechanisms
                
                **EXAMPLES AND APPLICATIONS:**
                - Concrete examples given in the paper
                - Real-world applications or use cases
                - Specific scenarios or case studies
                
                **METHODOLOGY HIGHLIGHTS:** (if relevant)
                - Key approaches or techniques used
                - Novel methods introduced
                - Important experimental details
                
                **CONCLUSIONS AND IMPLICATIONS:**
                - What can we now do/know that we couldn't before?
                - Specific future directions mentioned
                - Concrete impact on the field
                
                Remember: You are extracting and organizing the ACTUAL CONTENT, not describing what the paper contains.
                Write as if you are teaching the concepts directly, not reviewing a paper.
                
                For educational purposes, also note:
                - The most fascinating aspects that will engage listeners
                - The "aha!" moments and surprising insights  
                - The practical implications
                - The bigger picture and future directions
                """
            
            synthesis_task = Task(
                description=synthesis_description,
                agent=synthesizer,
                expected_output="Technical synthesis with facts only - zero interpretation" if self.focus == "technical" else "A content-focused synthesis presenting the actual findings, arguments, and evidence",
            )

            # Get the task description based on focus
            if self.focus == "technical":
                task_description = create_technical_writing_task(
                    content="Previous synthesis content will be used",
                    title=paper_title,
                    target_length="comprehensive",
                    language=self.language
                )
                expected_output = "Technical presentation with zero interpretation - facts only"
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
                    "type": "chunk_analysis"
                    if i < len(chunk_tasks)
                    else "synthesis"
                    if i == len(chunk_tasks)
                    else "educational",
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
