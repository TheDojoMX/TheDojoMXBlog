"""Dynamic agent generation based on content analysis."""

from typing import List, Dict, Any, Optional
from crewai import Agent
import re


class DynamicAgentGenerator:
    """Generates specialized agents based on content analysis."""
    
    def __init__(self, llm):
        self.llm = llm
        
        # Define agent templates for different domains
        self.agent_templates = {
            'machine_learning': {
                'role': 'Machine Learning Specialist',
                'goal': 'Extract and explain all ML concepts, algorithms, and results',
                'backstory': """You are an ML expert who understands neural networks, 
                training procedures, datasets, metrics, and optimization techniques. 
                You explain complex ML concepts clearly while preserving all technical details."""
            },
            'mathematics': {
                'role': 'Mathematics Expert',
                'goal': 'Extract and explain all mathematical concepts, proofs, and formulas',
                'backstory': """You are a mathematician who can explain theorems, proofs, 
                equations, and mathematical reasoning. You preserve all mathematical rigor 
                while making concepts accessible."""
            },
            'biology': {
                'role': 'Biology Specialist',
                'goal': 'Extract and explain all biological concepts, processes, and findings',
                'backstory': """You are a biologist who understands molecular processes, 
                organisms, ecosystems, and experimental procedures. You explain biological 
                mechanisms thoroughly while keeping all scientific details."""
            },
            'physics': {
                'role': 'Physics Expert',
                'goal': 'Extract and explain all physics concepts, laws, and experiments',
                'backstory': """You are a physicist who understands fundamental forces, 
                quantum mechanics, relativity, and experimental physics. You explain 
                physical phenomena completely while preserving all equations and data."""
            },
            'chemistry': {
                'role': 'Chemistry Specialist',
                'goal': 'Extract and explain all chemical concepts, reactions, and properties',
                'backstory': """You are a chemist who understands molecular structures, 
                reactions, synthesis, and chemical properties. You explain chemical 
                processes thoroughly with all technical details."""
            },
            'economics': {
                'role': 'Economics Expert',
                'goal': 'Extract and explain all economic concepts, models, and data',
                'backstory': """You are an economist who understands markets, policies, 
                models, and economic indicators. You explain economic theories and 
                data comprehensively."""
            },
            'psychology': {
                'role': 'Psychology Specialist',
                'goal': 'Extract and explain all psychological concepts, studies, and findings',
                'backstory': """You are a psychologist who understands human behavior, 
                cognitive processes, research methods, and therapeutic approaches. 
                You explain psychological concepts with all supporting evidence."""
            },
            'medicine': {
                'role': 'Medical Expert',
                'goal': 'Extract and explain all medical concepts, procedures, and findings',
                'backstory': """You are a medical professional who understands diseases, 
                treatments, anatomy, and clinical procedures. You explain medical 
                information thoroughly with all clinical details."""
            },
            'software': {
                'role': 'Software Engineering Expert',
                'goal': 'Extract and explain all code, algorithms, and technical implementations',
                'backstory': """You are a software engineer who understands programming 
                languages, algorithms, system design, and best practices. You explain 
                code and technical concepts completely with all implementation details."""
            },
            'statistics': {
                'role': 'Statistics Specialist',
                'goal': 'Extract and explain all statistical methods, analyses, and results',
                'backstory': """You are a statistician who understands probability, 
                hypothesis testing, regression, and data analysis. You explain 
                statistical methods and results with complete detail."""
            }
        }
    
    def detect_domains(self, content: str, title: str) -> List[str]:
        """Detect domains present in the content."""
        text = f"{title} {content}".lower()
        
        domain_keywords = {
            'machine_learning': [
                'neural', 'network', 'training', 'model', 'dataset', 'accuracy',
                'loss', 'gradient', 'backpropagation', 'tensorflow', 'pytorch',
                'classification', 'regression', 'clustering', 'deep learning'
            ],
            'mathematics': [
                'theorem', 'proof', 'lemma', 'equation', 'integral', 'derivative',
                'matrix', 'vector', 'topology', 'algebra', 'calculus', 'geometry'
            ],
            'biology': [
                'cell', 'protein', 'dna', 'rna', 'gene', 'organism', 'species',
                'evolution', 'ecosystem', 'metabolism', 'enzyme', 'bacteria'
            ],
            'physics': [
                'quantum', 'particle', 'force', 'energy', 'momentum', 'wave',
                'relativity', 'field', 'thermodynamics', 'mechanics', 'photon'
            ],
            'chemistry': [
                'molecule', 'reaction', 'compound', 'element', 'bond', 'catalyst',
                'synthesis', 'oxidation', 'reduction', 'polymer', 'organic'
            ],
            'economics': [
                'market', 'price', 'supply', 'demand', 'gdp', 'inflation',
                'trade', 'policy', 'investment', 'finance', 'economy'
            ],
            'psychology': [
                'behavior', 'cognitive', 'memory', 'perception', 'emotion',
                'personality', 'disorder', 'therapy', 'mental', 'consciousness'
            ],
            'medicine': [
                'patient', 'treatment', 'disease', 'diagnosis', 'clinical',
                'surgery', 'medication', 'symptom', 'therapy', 'medical'
            ],
            'software': [
                'code', 'function', 'algorithm', 'data structure', 'api',
                'database', 'framework', 'programming', 'software', 'debug'
            ],
            'statistics': [
                'p-value', 'correlation', 'regression', 'variance', 'mean',
                'median', 'hypothesis', 'significance', 'confidence', 'sample'
            ]
        }
        
        detected_domains = []
        domain_scores = {}
        
        for domain, keywords in domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                domain_scores[domain] = score
        
        # Sort by score and take top domains
        sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
        detected_domains = [domain for domain, score in sorted_domains[:3] if score >= 2]
        
        return detected_domains
    
    def extract_specific_topics(self, content: str, domain: str) -> List[str]:
        """Extract specific topics within a domain."""
        topics = []
        
        if domain == 'machine_learning':
            # Look for specific ML techniques
            ml_patterns = [
                r'(?:convolutional|recurrent|transformer|attention)',
                r'(?:supervised|unsupervised|reinforcement)\s+learning',
                r'(?:classification|regression|clustering|generation)',
                r'(?:GAN|VAE|BERT|GPT|ResNet|LSTM|GRU)'
            ]
            for pattern in ml_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    topics.append(pattern.replace('(?:', '').replace(')', '').replace('|', '/'))
        
        elif domain == 'software':
            # Look for programming languages and frameworks
            lang_patterns = [
                r'\b(?:Python|JavaScript|Java|C\+\+|Rust|Go|TypeScript)\b',
                r'\b(?:React|Vue|Angular|Django|Flask|Spring|Node\.js)\b',
                r'\b(?:Docker|Kubernetes|AWS|Azure|GCP)\b'
            ]
            for pattern in lang_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                topics.extend(matches)
        
        return list(set(topics))[:5]  # Return top 5 unique topics
    
    def create_domain_expert(self, domain: str, specific_topics: List[str] = None) -> Agent:
        """Create a domain-specific expert agent."""
        template = self.agent_templates.get(domain)
        
        if not template:
            # Create a generic expert for unknown domains
            return Agent(
                role=f'{domain.title()} Domain Expert',
                goal=f'Extract and explain all {domain}-related concepts and information',
                backstory=f"""You are an expert in {domain} who can identify and explain 
                all relevant concepts, ensuring complete extraction of domain-specific knowledge.""",
                llm=self.llm,
                verbose=True
            )
        
        # Customize backstory with specific topics if provided
        backstory = template['backstory']
        if specific_topics:
            backstory += f"\n\nYou have particular expertise in: {', '.join(specific_topics)}"
        
        return Agent(
            role=template['role'],
            goal=template['goal'],
            backstory=backstory,
            llm=self.llm,
            verbose=True
        )
    
    def create_methodology_analyst(self, has_experiments: bool = False) -> Agent:
        """Create an agent specialized in methodology analysis."""
        if has_experiments:
            return Agent(
                role='Experimental Methodology Analyst',
                goal='Extract complete experimental design, procedures, and validation methods',
                backstory="""You are an expert in experimental design and research methodology. 
                You extract:
                - Hypotheses and research questions
                - Experimental setup and controls
                - Data collection procedures
                - Statistical analyses
                - Validation and verification methods
                - Limitations and assumptions
                You ensure all methodological details are preserved for reproducibility.""",
                llm=self.llm,
                verbose=True
            )
        else:
            return Agent(
                role='Analytical Methodology Expert',
                goal='Extract complete analytical methods and procedures',
                backstory="""You are an expert in analytical methods and procedures. 
                You extract:
                - Analytical frameworks used
                - Step-by-step procedures
                - Tools and techniques employed
                - Decision criteria
                - Quality measures
                You document methods comprehensively.""",
                llm=self.llm,
                verbose=True
            )
    
    def create_data_specialist(self, has_statistics: bool = False) -> Agent:
        """Create an agent specialized in data and statistics."""
        if has_statistics:
            return Agent(
                role='Statistical Data Analyst',
                goal='Extract all data, statistics, and quantitative results',
                backstory="""You are a data scientist who specializes in statistical analysis. 
                You extract:
                - All numerical data and measurements
                - Statistical test results and p-values
                - Confidence intervals and effect sizes
                - Data visualizations and trends
                - Model parameters and performance metrics
                - Comparative analyses
                Every number and statistical result must be preserved.""",
                llm=self.llm,
                verbose=True
            )
        else:
            return Agent(
                role='Data Documentation Specialist',
                goal='Extract all data, examples, and evidence',
                backstory="""You are a specialist in documenting data and evidence. 
                You extract:
                - All data points and measurements
                - Examples and case studies
                - Supporting evidence
                - Observations and findings
                - Patterns and trends
                No data point is too small to include.""",
                llm=self.llm,
                verbose=True
            )
    
    def create_implementation_expert(self, has_code: bool = False) -> Agent:
        """Create an agent for implementation details."""
        if has_code:
            return Agent(
                role='Code Implementation Expert',
                goal='Extract all code, algorithms, and implementation details',
                backstory="""You are a software architect who documents implementations. 
                You extract:
                - Complete code snippets and algorithms
                - API definitions and interfaces
                - Configuration and setup instructions
                - Dependencies and requirements
                - Performance considerations
                - Error handling and edge cases
                All code and technical details must be preserved exactly.""",
                llm=self.llm,
                verbose=True
            )
        else:
            return Agent(
                role='Process Implementation Specialist',
                goal='Extract all implementation and procedural details',
                backstory="""You are an implementation specialist who documents processes. 
                You extract:
                - Step-by-step procedures
                - Implementation guidelines
                - Best practices and recommendations
                - Common pitfalls and solutions
                - Resource requirements
                Every implementation detail must be captured.""",
                llm=self.llm,
                verbose=True
            )
    
    def generate_agents_for_content(
        self, 
        content: str, 
        title: str,
        content_analysis: Dict[str, Any]
    ) -> List[Agent]:
        """Generate a custom set of agents based on content analysis."""
        agents = []
        
        # Detect domains in content
        domains = self.detect_domains(content, title)
        
        # Create domain experts for detected domains
        for domain in domains[:3]:  # Limit to top 3 domains
            specific_topics = self.extract_specific_topics(content, domain)
            agent = self.create_domain_expert(domain, specific_topics)
            agents.append(agent)
        
        # Add methodology expert if applicable
        if content_analysis.get('has_methodology'):
            has_experiments = 'experiment' in content.lower() or 'hypothesis' in content.lower()
            agents.append(self.create_methodology_analyst(has_experiments))
        
        # Add data specialist if there's significant data
        if content_analysis.get('has_results') or 'data' in content.lower():
            has_statistics = bool(re.search(r'p[- ]?value|significance|correlation|regression', content, re.IGNORECASE))
            agents.append(self.create_data_specialist(has_statistics))
        
        # Add implementation expert if there's code or procedures
        if content_analysis.get('has_code'):
            agents.append(self.create_implementation_expert(has_code=True))
        elif 'implementation' in content.lower() or 'procedure' in content.lower():
            agents.append(self.create_implementation_expert(has_code=False))
        
        # Always add a generalist to catch anything missed
        agents.append(self.create_generalist_agent())
        
        return agents
    
    def create_generalist_agent(self) -> Agent:
        """Create a generalist agent to catch anything domain experts might miss."""
        return Agent(
            role='Comprehensive Content Analyst',
            goal='Ensure no information is missed by identifying and extracting any remaining content',
            backstory="""You are a meticulous analyst who ensures completeness. 
            After domain experts have extracted their specialized content, you:
            - Identify any information not yet captured
            - Extract general insights and observations
            - Preserve context and connections between ideas
            - Document any meta-information about the content
            - Ensure the narrative flow is maintained
            You are the final safety net ensuring absolute completeness.""",
            llm=self.llm,
            verbose=True
        )