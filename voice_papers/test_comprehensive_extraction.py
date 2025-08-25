#!/usr/bin/env python3
"""Test script for comprehensive extraction features."""

import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from voice_papers.agents.crew_manager import CrewManager
from voice_papers.agents.exhaustive_extractor import (
    MultiPassAnalyzer,
    CoverageVerifier,
    create_exhaustive_extractor_agent,
)
from voice_papers.agents.dynamic_agent_generator import DynamicAgentGenerator
from voice_papers.config import OPENAI_API_KEY

def test_comprehensive_extraction():
    """Test the comprehensive extraction system with a sample document."""
    
    # Sample technical content
    sample_content = """
    # Understanding Neural Networks: A Comprehensive Guide
    
    ## Introduction
    Neural networks are computational models inspired by biological neural networks. 
    They consist of interconnected nodes (neurons) organized in layers that process 
    information using connectionist approaches to computation.
    
    ## Mathematical Foundation
    The fundamental equation for a neuron's output is:
    y = f(Σ(wi * xi) + b)
    
    Where:
    - xi represents input values
    - wi represents weights
    - b is the bias term
    - f is the activation function
    
    Common activation functions include:
    1. Sigmoid: σ(x) = 1/(1 + e^(-x))
    2. ReLU: f(x) = max(0, x)
    3. Tanh: tanh(x) = (e^x - e^(-x))/(e^x + e^(-x))
    
    ## Training Process
    Neural networks learn through backpropagation, which involves:
    
    1. Forward pass: Input data flows through the network
    2. Loss calculation: L = (1/n) * Σ(yi - ŷi)²
    3. Backward pass: Gradients computed using chain rule
    4. Weight update: w = w - α * ∂L/∂w
    
    The learning rate α typically ranges from 0.001 to 0.1.
    
    ## Implementation Example
    ```python
    import numpy as np
    
    class SimpleNeuralNetwork:
        def __init__(self, input_size, hidden_size, output_size):
            self.W1 = np.random.randn(input_size, hidden_size) * 0.01
            self.b1 = np.zeros((1, hidden_size))
            self.W2 = np.random.randn(hidden_size, output_size) * 0.01
            self.b2 = np.zeros((1, output_size))
        
        def forward(self, X):
            self.z1 = np.dot(X, self.W1) + self.b1
            self.a1 = np.maximum(0, self.z1)  # ReLU
            self.z2 = np.dot(self.a1, self.W2) + self.b2
            return self.z2
    ```
    
    ## Experimental Results
    In our experiments with the MNIST dataset:
    - Training accuracy: 98.7%
    - Validation accuracy: 97.2%
    - Test accuracy: 96.9%
    - Training time: 23.4 minutes
    - Number of parameters: 784,650
    
    ## Limitations
    Current limitations include:
    - Requires large amounts of labeled data
    - Computationally expensive for deep architectures
    - Susceptible to overfitting without regularization
    - Difficult to interpret learned representations
    
    ## Future Work
    Future research directions:
    - Exploring attention mechanisms
    - Developing more efficient training algorithms
    - Investigating neural architecture search
    - Improving interpretability methods
    """
    
    print("🧪 Testing Comprehensive Extraction System")
    print("=" * 60)
    
    # Test 1: Multi-pass analysis
    print("\n📊 Test 1: Multi-pass Analysis")
    print("-" * 40)
    
    # Create crew manager with exhaustive depth
    crew_manager = CrewManager(
        language="English",
        project_name="test_comprehensive",
        technical_level="technical",
        depth="exhaustive",
        focus="technical"
    )
    
    # Initialize analyzer
    analyzer = MultiPassAnalyzer(crew_manager.llm)
    
    # Run analysis
    print("Running content analysis...")
    analysis = analyzer.analyze_content_type(
        sample_content, 
        "Understanding Neural Networks"
    )
    
    print(f"✓ Content type detected: {analysis['primary_type']}")
    print(f"✓ Has methodology: {analysis['has_methodology']}")
    print(f"✓ Has code: {analysis['has_code']}")
    print(f"✓ Has formulas: {analysis['has_formulas']}")
    print(f"✓ Complexity: {analysis['complexity']}")
    print(f"✓ Topics: {', '.join(analysis['topics'][:5])}")
    
    # Test 2: Dynamic agent generation
    print("\n🤖 Test 2: Dynamic Agent Generation")
    print("-" * 40)
    
    agent_gen = DynamicAgentGenerator(crew_manager.llm)
    
    # Detect domains
    domains = agent_gen.detect_domains(sample_content, "Neural Networks")
    print(f"✓ Detected domains: {', '.join(domains)}")
    
    # Generate agents
    agents = agent_gen.generate_agents_for_content(
        sample_content,
        "Neural Networks",
        analysis
    )
    print(f"✓ Generated {len(agents)} specialized agents:")
    for agent in agents:
        print(f"  - {agent.role}")
    
    # Test 3: Coverage verification
    print("\n✅ Test 3: Coverage Verification")
    print("-" * 40)
    
    verifier = CoverageVerifier(crew_manager.llm)
    
    # Create a mock extraction (partial, for testing)
    partial_extraction = """
    Neural networks are computational models with interconnected nodes.
    They use backpropagation for learning.
    Common activation functions include sigmoid and ReLU.
    Training accuracy was 98.7%.
    """
    
    # Verify coverage
    coverage = verifier.verify_coverage(sample_content, partial_extraction)
    print(f"✓ Coverage percentage: {coverage['coverage_checks']['coverage_percentage']:.1f}%")
    print(f"✓ Is comprehensive: {coverage['is_comprehensive']}")
    print(f"✓ Missing elements found: {len(coverage['missing_elements'])}")
    if coverage['missing_elements']:
        print(f"  Sample missing: {', '.join(coverage['missing_elements'][:5])}")
    
    # Test 4: Exhaustive extraction
    print("\n📝 Test 4: Exhaustive Extraction (Quick Test)")
    print("-" * 40)
    
    # Create exhaustive extractor
    extractor = create_exhaustive_extractor_agent(crew_manager.llm)
    print(f"✓ Created extractor: {extractor.role}")
    print(f"✓ Goal: {extractor.goal[:100]}...")
    
    print("\n✅ All tests completed successfully!")
    print("=" * 60)
    
    # Test 5: Depth comparison
    print("\n📏 Test 5: Extraction Depth Comparison")
    print("-" * 40)
    
    from voice_papers.agents.prompts.comprehensive_prompts import ComprehensivePrompts
    
    prompts = ComprehensivePrompts()
    
    for depth in ["summary", "standard", "comprehensive", "exhaustive"]:
        instructions = prompts.get_depth_specific_instructions(depth)
        print(f"\n{depth.upper()}:")
        print(f"  Goal: {instructions['goal']}")
        print(f"  Length: {instructions['length']}")
        print(f"  Use case: {instructions['use_case']}")

if __name__ == "__main__":
    # Check for API key
    if not OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY not found in environment")
        print("Please set your OpenAI API key in the .env file")
        sys.exit(1)
    
    try:
        test_comprehensive_extraction()
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)