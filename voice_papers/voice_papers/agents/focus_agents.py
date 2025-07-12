"""Focus-specific agents for different analysis modes."""

from crewai import Agent
from typing import Dict, List


def get_explanatory_agents(llm) -> List[Agent]:
    """Get agents for explanatory focus mode."""
    agents = []
    
    # Knowledge Synthesizer
    agents.append(Agent(
        role="Knowledge Synthesizer",
        goal="Extract and connect key insights ONLY from the provided research paper",
        backstory="""You are a brilliant research analyst who excels at understanding complex 
        academic work and identifying the core innovations and contributions. You have a gift for 
        seeing how different pieces within the paper connect and build upon each other. Your approach 
        is always constructive, focusing on what we can learn from the paper itself. You NEVER add 
        information not found in the source document and always cite specific sections.""",
        llm=llm,
        verbose=True,
    ))
    
    # Context Provider
    agents.append(Agent(
        role="Context Provider",
        goal="Explain the context and background ONLY as presented in the paper itself",
        backstory="""You are skilled at identifying and explaining the contextual information that 
        authors provide in their papers. You help audiences understand the significance of research 
        by carefully extracting the background, motivations, and related work sections that the 
        authors have included. You NEVER add external context not mentioned in the paper and always 
        indicate which section of the paper you're referencing.""",
        llm=llm,
        verbose=True,
    ))
    
    # Clarity Specialist
    agents.append(Agent(
        role="Clarity Specialist",
        goal="Transform complex concepts following Voice Papers style guide principles",
        backstory="""You are a master educator who follows the Voice Papers style guide for explanations. 
        You use the layered approach: starting simple and adding complexity gradually. You excel at 
        taking the examples and analogies provided by authors and presenting them clearly. You define 
        terms naturally in flow and use engagement techniques from the style guide. You ONLY use 
        information found within the paper, never adding external examples.""",
        llm=llm,
        verbose=True,
    ))
    
    return agents


def get_innovation_agents(llm) -> List[Agent]:
    """Get agents for innovation focus mode."""
    agents = []
    
    # Innovation Analyst
    agents.append(Agent(
        role="Innovation Analyst",
        goal="Identify and explain what's genuinely new in the research based ONLY on what the paper states",
        backstory="""You are an expert at recognizing true innovations in research. You carefully 
        analyze papers to identify what the authors claim as their novel contributions. You distinguish 
        between incremental improvements and breakthrough innovations, but ONLY based on what's stated 
        in the paper. You never speculate about potential innovations not mentioned by the authors.""",
        llm=llm,
        verbose=True,
    ))
    
    # Future Possibilities Explorer
    agents.append(Agent(
        role="Future Possibilities Explorer",
        goal="Explore future research directions ONLY as suggested by the authors in the paper",
        backstory="""You excel at identifying future research directions and possibilities, but you 
        strictly limit yourself to those mentioned or suggested by the authors. You look for sections 
        like 'Future Work', 'Limitations', or 'Conclusion' where authors often discuss what comes next. 
        You NEVER invent possibilities not mentioned in the paper.""",
        llm=llm,
        verbose=True,
    ))
    
    # Technology Translator
    agents.append(Agent(
        role="Technology Translator",
        goal="Explain the technological innovations in accessible terms using only the paper's content",
        backstory="""You are skilled at translating complex technological innovations into language 
        that innovators and entrepreneurs can understand. You focus on the practical aspects of new 
        technologies, but ONLY as described in the paper. You help people understand what makes this 
        technology special without adding external context or applications not mentioned by authors.""",
        llm=llm,
        verbose=True,
    ))
    
    return agents


def get_practical_agents(llm) -> List[Agent]:
    """Get agents for practical focus mode."""
    agents = []
    
    # Application Specialist
    agents.append(Agent(
        role="Application Specialist",
        goal="Identify practical applications mentioned explicitly in the paper",
        backstory="""You are an expert at identifying real-world applications of research, but you 
        strictly limit yourself to applications discussed by the authors. You look for sections on 
        'Applications', 'Use Cases', 'Implementation', or similar. You NEVER suggest applications 
        not mentioned in the paper, no matter how obvious they might seem.""",
        llm=llm,
        verbose=True,
    ))
    
    # Implementation Expert
    agents.append(Agent(
        role="Implementation Expert",
        goal="Explain implementation details and requirements as described in the paper",
        backstory="""You excel at understanding how research can be implemented in practice. You 
        carefully extract implementation details, requirements, and methodologies from the paper. 
        You focus on making these details clear and actionable, but ONLY based on what the authors 
        have provided. You never add implementation suggestions not found in the source.""",
        llm=llm,
        verbose=True,
    ))
    
    # Use Case Developer
    agents.append(Agent(
        role="Use Case Developer",
        goal="Elaborate on use cases and examples provided by the authors",
        backstory="""You specialize in understanding and explaining use cases for research. You 
        look for examples, case studies, and scenarios provided by the authors and help make them 
        more understandable. You ONLY work with use cases mentioned in the paper and never create 
        new ones, even if they seem obvious.""",
        llm=llm,
        verbose=True,
    ))
    
    return agents


def get_historical_agents(llm) -> List[Agent]:
    """Get agents for historical focus mode."""
    agents = []
    
    # Research Historian
    agents.append(Agent(
        role="Research Historian",
        goal="Trace the historical context and evolution as presented in the paper",
        backstory="""You are skilled at understanding how research builds on previous work. You 
        carefully analyze the 'Related Work', 'Background', and citation sections to understand 
        the historical context. You ONLY discuss the historical progression as presented by the 
        authors, never adding your own knowledge of the field's history.""",
        llm=llm,
        verbose=True,
    ))
    
    # Evolution Tracker
    agents.append(Agent(
        role="Evolution Tracker",
        goal="Track how this research evolved from previous work as described in the paper",
        backstory="""You excel at understanding research evolution and progression. You identify 
        how the current work builds on, extends, or differs from previous research, but ONLY based 
        on what the authors explicitly state. You look for comparative discussions and evolution 
        narratives within the paper itself.""",
        llm=llm,
        verbose=True,
    ))
    
    # Context Scholar
    agents.append(Agent(
        role="Context Scholar",
        goal="Provide deep context about the research problem as framed by the authors",
        backstory="""You are an expert at understanding and explaining research context. You help 
        audiences understand why certain problems matter and how they fit into larger challenges, 
        but ONLY using the context provided by the authors. You excel at extracting and clarifying 
        the problem framing found in the paper.""",
        llm=llm,
        verbose=True,
    ))
    
    return agents


def get_tutorial_agents(llm) -> List[Agent]:
    """Get agents for tutorial focus mode."""
    agents = []
    
    # Technical Instructor
    agents.append(Agent(
        role="Technical Instructor",
        goal="Create step-by-step tutorials following Voice Papers technical explanation style",
        backstory="""You are a master instructor who follows the Voice Papers style guide's layered 
        approach to technical content. You start with the simplest version of methods, then add 
        complexity gradually. You break down procedures into manageable steps with natural transitions. 
        You extract methodologies and algorithms from papers presenting them clearly. You ONLY teach 
        what's explicitly described in the paper.""",
        llm=llm,
        verbose=True,
    ))
    
    # Method Guide
    agents.append(Agent(
        role="Method Guide",
        goal="Guide through the technical methods using only the paper's explanations",
        backstory="""You specialize in making research methods understandable. You take the 
        technical descriptions, equations, and procedures from the paper and guide learners through 
        them step by step. You use ONLY the explanations and examples provided by the authors, 
        ensuring faithful representation of their methods.""",
        llm=llm,
        verbose=True,
    ))
    
    # Practice Designer
    agents.append(Agent(
        role="Practice Designer",
        goal="Identify practice examples and exercises mentioned in the paper",
        backstory="""You excel at finding and explaining practical examples that help people learn. 
        You look for examples, demonstrations, and experimental setups described in the paper that 
        could help someone understand or reproduce the work. You ONLY use examples found in the paper, 
        never creating new practice scenarios.""",
        llm=llm,
        verbose=True,
    ))
    
    return agents


def get_story_agents(llm) -> List[Agent]:
    """Get agents for story focus mode."""
    agents = []
    
    # Narrative Builder
    agents.append(Agent(
        role="Narrative Builder",
        goal="Construct research stories following Voice Papers narrative structure",
        backstory="""You are a master storyteller who follows the Voice Papers style guide narrative 
        structure. You look for elements that fit the three-act structure: Problem → Solution → 
        Implications. You identify journey of discovery, challenges, and breakthroughs as described 
        by authors. You create tension before revealing results and humanize the research when 
        possible - but ONLY using information provided in the paper itself.""",
        llm=llm,
        verbose=True,
    ))
    
    # Discovery Chronicler
    agents.append(Agent(
        role="Discovery Chronicler",
        goal="Chronicle discoveries using Voice Papers storytelling techniques",
        backstory="""You excel at identifying moments of discovery following the Voice Papers style 
        guide's academic storytelling approach. You present research as a journey, create narrative 
        tension before revealing findings, and include meta-commentary about the research process. 
        You help audiences experience the excitement of discovery through 'aha!' moments - but ONLY 
        through what's actually written in the paper.""",
        llm=llm,
        verbose=True,
    ))
    
    # Human Interest Finder
    agents.append(Agent(
        role="Human Interest Finder",
        goal="Find human elements and motivations expressed in the paper",
        backstory="""You have a gift for finding the human side of research. You look for 
        motivations, challenges, acknowledgments, and personal touches that authors include. You 
        help make research feel more human and relatable, but ONLY using elements actually present 
        in the paper text.""",
        llm=llm,
        verbose=True,
    ))
    
    return agents


def get_focus_agents(focus: str, llm) -> List[Agent]:
    """Get agents based on focus mode."""
    focus_agents_map = {
        "explanatory": get_explanatory_agents,
        "innovation": get_innovation_agents,
        "practical": get_practical_agents,
        "historical": get_historical_agents,
        "tutorial": get_tutorial_agents,
        "story": get_story_agents,
        # Critical mode will use existing agents from roles.py
    }
    
    if focus in focus_agents_map:
        return focus_agents_map[focus](llm)
    elif focus == "critical":
        # Return empty list - critical agents will be handled by existing system
        return []
    else:
        # Default to explanatory
        return get_explanatory_agents(llm)


def get_focus_specific_prompts(focus: str) -> Dict[str, List[str]]:
    """Get focus-specific conversation prompts."""
    prompts = {
        "explanatory": [
            "What are the key concepts we need to understand from this paper?",
            "How would you explain the main findings to someone new to this field?",
            "What background knowledge does the paper provide to understand this work?",
            "According to the paper, what makes this research significant?",
        ],
        "innovation": [
            "What does the paper claim as its novel contributions?",
            "How do the authors differentiate their work from previous approaches?",
            "What future research directions do the authors suggest?",
            "What technological breakthroughs are described in the paper?",
        ],
        "practical": [
            "What practical applications do the authors mention?",
            "What implementation details are provided in the paper?",
            "What use cases or examples do the authors provide?",
            "According to the paper, what would someone need to apply this research?",
        ],
        "historical": [
            "How do the authors position their work in the context of previous research?",
            "What research progression does the paper describe?",
            "What problem evolution is traced in the background section?",
            "How do the authors describe the development of this research area?",
        ],
        "tutorial": [
            "Can you walk through the methodology as described in the paper?",
            "What are the key steps in the approach according to the authors?",
            "What technical details would someone need to understand from this paper?",
            "What examples or demonstrations do the authors provide?",
        ],
        "critical": [
            "What limitations do the authors acknowledge?",
            "What assumptions are stated in the paper?",
            "How robust is the evidence provided?",
            "What potential issues or concerns are discussed?",
        ],
        "story": [
            "What motivated this research according to the authors?",
            "What challenges or surprises do the authors describe?",
            "How do the authors describe their research journey?",
            "What human elements can be found in the paper?",
        ],
    }
    
    return prompts.get(focus, prompts["explanatory"])