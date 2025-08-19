#!/usr/bin/env python3
"""Test script for the technical writer focus mode."""

import sys
from pathlib import Path

# Add the voice_papers module to the path
sys.path.insert(0, str(Path(__file__).parent))

from voice_papers.agents.crew_manager import CrewManager
from voice_papers.agents.technical_writer import get_technical_writer_agent, create_technical_writing_task
from crewai import Crew, Task

def test_technical_writer():
    """Test the technical writer for zero-interpretation output."""
    
    # Sample content with interpretation-heavy language
    sample_content = """
    # Revolutionary Deep Learning Architecture
    
    This groundbreaking research demonstrates a paradigm shift in neural network design.
    The authors brilliantly reveal how their innovative approach transforms the field.
    
    ## Key Findings
    
    The results suggest profound implications for AI development:
    - The model achieves 95.3% accuracy on benchmark datasets
    - Training time is reduced by 47% compared to baseline methods
    - Memory usage decreases by 32% through novel optimization
    
    These remarkable findings imply that future AI systems could be significantly more efficient.
    The fascinating approach opens new possibilities for scaling.
    
    ## Methodology
    
    The researchers employ a three-stage process:
    1. Data preprocessing using tokenization
    2. Model training with gradient descent
    3. Evaluation on held-out test sets
    
    This elegant methodology demonstrates the power of systematic approaches.
    """
    
    print("🧪 Testing Technical Writer (Zero Interpretation)")
    print("=" * 60)
    
    # Create crew manager with technical focus
    crew_manager = CrewManager(
        language="English",
        project_name="technical_test",
        technical_level="technical",
        duration_minutes=5,
        conversation_mode="enhanced",
        tone="academic",
        focus="technical"
    )
    
    # Get the technical writer
    technical_writer = get_technical_writer_agent(crew_manager.llm)
    
    # Create technical writing task
    task = Task(
        description=create_technical_writing_task(
            content=sample_content,
            title="Deep Learning Architecture Study",
            target_length="comprehensive",
            language="English"
        ),
        agent=technical_writer,
        expected_output="Technical presentation with zero interpretation"
    )
    
    # Run the task
    crew = Crew(
        agents=[technical_writer],
        tasks=[task],
        verbose=True
    )
    
    print("\n📝 Input Content Preview:")
    print(sample_content[:300] + "...")
    print("\n" + "=" * 60)
    print("🔧 Processing with Technical Writer...")
    print("=" * 60 + "\n")
    
    result = crew.kickoff()
    
    print("\n" + "=" * 60)
    print("✅ Technical Writer Output:")
    print("=" * 60)
    print(result)
    
    # Check for interpretation words
    interpretation_words = [
        "revolutionary", "groundbreaking", "brilliantly", "remarkable",
        "fascinating", "elegant", "demonstrates", "suggests", "implies",
        "profound", "paradigm shift", "transforms"
    ]
    
    result_lower = str(result).lower()
    found_words = [word for word in interpretation_words if word in result_lower]
    
    print("\n" + "=" * 60)
    print("📊 Analysis:")
    print(f"   Interpretation words removed: {len([w for w in interpretation_words if w not in result_lower])}/{len(interpretation_words)}")
    if found_words:
        print(f"   ⚠️  Still contains: {', '.join(found_words)}")
    else:
        print("   ✅ All interpretation words successfully removed!")
    
    print("\n✨ Test completed!")

if __name__ == "__main__":
    test_technical_writer()