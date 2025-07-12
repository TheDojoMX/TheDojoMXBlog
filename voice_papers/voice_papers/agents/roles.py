"""Agent role definitions for different paper types."""

from typing import Dict, List
from crewai import Agent
from crewai.llm import LLM


def get_humorous_agent(llm: LLM) -> Agent:
    """Get a humorous agent to add levity to discussions."""
    return Agent(
        role="Comedy Communicator",
        goal="Add appropriate humor and wit to make the discussion more engaging while maintaining respect for the topic",
        backstory="You are a science comedian and communicator who knows how to make complex topics entertaining without undermining their importance. You use analogies, witty observations, and light humor to keep audiences engaged. Think Neil deGrasse Tyson meets stand-up comedy - intelligent, respectful, but definitely fun.",
        llm=llm,
        verbose=True,
    )


def get_base_roles(llm: LLM) -> List[Agent]:
    """Get base roles that are always needed."""
    return [
        Agent(
            role="Coordinator",
            goal="Coordinate the discussion and ensure all perspectives are heard",
            backstory="You are an experienced moderator who ensures productive discussions",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="Scientific Reviewer",
            goal="Verify the soundness and methodology of the paper",
            backstory="You are a rigorous scientist who evaluates research methodology and conclusions",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="Critical Thinker",
            goal="Question assumptions and challenge ideas presented",
            backstory="You are a skeptical academic who questions everything and looks for flaws",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="Educational Writer",
            goal="Create engaging educational content in the style of popular science educators",
            backstory="You are a skilled science communicator who explains complex topics in an accessible, engaging way like 3Blue1Brown or other popular educators",
            llm=llm,
            verbose=True,
        ),
    ]


def get_ai_specific_roles(llm: LLM) -> List[Agent]:
    """Get roles specific to AI papers."""
    return [
        Agent(
            role="AI Researcher",
            goal="Provide technical insights on AI methodology and implications",
            backstory="You are an AI researcher with deep technical knowledge",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="AI Philosopher",
            goal="Discuss philosophical implications of AI research",
            backstory="You are a philosopher specializing in AI ethics and implications",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="AI Doomer",
            goal="Raise concerns about potential risks and negative consequences",
            backstory="You are concerned about AI safety and potential existential risks",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="AI Enthusiast",
            goal="Highlight positive potential and applications",
            backstory="You are optimistic about AI's potential to solve problems",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="AI Newcomer",
            goal="Ask basic questions that others can answer",
            backstory="You know little about AI but are curious and ask good questions",
            llm=llm,
            verbose=True,
        ),
    ]


def get_medicine_roles(llm: LLM) -> List[Agent]:
    """Get roles specific to medicine and biology papers."""
    return [
        Agent(
            role="Medical Researcher",
            goal="Evaluate clinical methodology and medical evidence",
            backstory="You are a medical researcher with expertise in clinical trials and evidence-based medicine",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="Bioethicist",
            goal="Address ethical implications of medical research",
            backstory="You are a bioethicist concerned with patient welfare and research ethics",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="Clinician",
            goal="Provide practical medical perspective and real-world applications",
            backstory="You are a practicing physician who translates research into patient care",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="Patient Advocate",
            goal="Represent patient perspectives and concerns",
            backstory="You advocate for patient rights and understand how medical research affects real people",
            llm=llm,
            verbose=True,
        ),
    ]


def get_science_roles(llm: LLM) -> List[Agent]:
    """Get roles specific to physics and chemistry papers."""
    return [
        Agent(
            role="Theoretical Physicist",
            goal="Analyze theoretical frameworks and mathematical models",
            backstory="You are a theoretical physicist who understands complex mathematical concepts and physical laws",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="Experimental Scientist",
            goal="Evaluate experimental design and methodology",
            backstory="You are an experimental scientist who designs and conducts rigorous experiments",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="Science Communicator",
            goal="Translate complex scientific concepts for general audiences",
            backstory="You specialize in making complex physics and chemistry accessible to everyone",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="Science Skeptic",
            goal="Question extraordinary claims and demand rigorous evidence",
            backstory="You are skeptical of bold claims and always demand reproducible evidence",
            llm=llm,
            verbose=True,
        ),
    ]


def get_psychology_roles(llm: LLM) -> List[Agent]:
    """Get roles specific to psychology and neuroscience papers."""
    return [
        Agent(
            role="Cognitive Scientist",
            goal="Analyze cognitive processes and brain mechanisms",
            backstory="You study how the mind works and how brain activity relates to behavior",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="Clinical Psychologist",
            goal="Evaluate practical applications for mental health",
            backstory="You work with patients and understand how research applies to therapy and treatment",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="Neuroscientist",
            goal="Analyze brain imaging and neural mechanism data",
            backstory="You specialize in understanding brain structure and function through advanced techniques",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="Behavioral Economist",
            goal="Connect psychological findings to real-world decision making",
            backstory="You study how psychological biases affect human behavior and decision making",
            llm=llm,
            verbose=True,
        ),
    ]


def get_economics_roles(llm: LLM) -> List[Agent]:
    """Get roles specific to economics and finance papers."""
    return [
        Agent(
            role="Economist",
            goal="Analyze economic theory and empirical evidence",
            backstory="You are an economist who evaluates models, data, and policy implications",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="Financial Analyst",
            goal="Evaluate market implications and investment perspectives",
            backstory="You analyze markets and understand how economic research affects investments",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="Policy Advisor",
            goal="Consider policy implications and government applications",
            backstory="You advise on economic policy and understand how research influences government decisions",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="Consumer Advocate",
            goal="Represent everyday people affected by economic policies",
            backstory="You advocate for consumers and workers, focusing on real-world impacts of economic changes",
            llm=llm,
            verbose=True,
        ),
    ]


def get_technology_roles(llm: LLM) -> List[Agent]:
    """Get roles specific to technology and engineering papers."""
    return [
        Agent(
            role="Software Engineer",
            goal="Evaluate technical implementation and code quality",
            backstory="You are a software engineer who builds systems and understands technical trade-offs",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="Security Expert",
            goal="Analyze security implications and vulnerabilities",
            backstory="You specialize in cybersecurity and understand how technology can be exploited or protected",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="UX Designer",
            goal="Consider user experience and human-computer interaction",
            backstory="You design user interfaces and understand how people interact with technology",
            llm=llm,
            verbose=True,
        ),
        Agent(
            role="Tech Entrepreneur",
            goal="Evaluate commercial viability and market potential",
            backstory="You start tech companies and understand how technical innovations become products",
            llm=llm,
            verbose=True,
        ),
    ]


def get_roles_for_topic(topic: str, llm: LLM, tone: str = "academic") -> List[Agent]:
    """Get appropriate roles based on paper topic and conversation tone."""
    base_roles = get_base_roles(llm)

    topic_lower = topic.lower()

    # AI and Machine Learning
    if topic_lower == "ai":
        specialized_roles = base_roles + get_ai_specific_roles(llm)
    # Medicine and Biology
    elif topic_lower == "medicine":
        specialized_roles = base_roles + get_medicine_roles(llm)
    # Physics and Chemistry
    elif topic_lower == "science":
        specialized_roles = base_roles + get_science_roles(llm)
    # Psychology and Neuroscience
    elif topic_lower == "psychology":
        specialized_roles = base_roles + get_psychology_roles(llm)
    # Economics and Finance
    elif topic_lower == "economics":
        specialized_roles = base_roles + get_economics_roles(llm)
    # Technology and Engineering
    elif topic_lower == "technology":
        specialized_roles = base_roles + get_technology_roles(llm)
    else:
        # Default to base roles for other topics
        specialized_roles = base_roles

    # Add humorous agent if tone requires it
    if tone in ["humorous", "playful"]:
        specialized_roles.append(get_humorous_agent(llm))

    return specialized_roles
