#!/usr/bin/env python3
"""Test script to verify new default behavior."""

import sys
from pathlib import Path
import os

# Add the voice_papers module to the path
sys.path.insert(0, str(Path(__file__).parent))

from voice_papers.agents.crew_manager import CrewManager

def test_new_defaults():
    """Test the new default behavior of concatenation + knowledge graph."""
    
    # Test content
    test_content = """
    # Large Language Models: A Breakthrough in AI
    
    Large Language Models (LLMs) represent a significant breakthrough in artificial intelligence.
    These models, such as GPT-4, Claude, and Gemini, demonstrate remarkable capabilities across
    multiple domains including text generation, code completion, and reasoning.
    
    ## Key Capabilities
    
    LLMs excel in several areas:
    1. Natural language understanding and generation
    2. Code generation and debugging
    3. Mathematical reasoning
    4. Creative writing and storytelling
    
    ## Training Process
    
    LLMs are trained using transformer architecture with self-attention mechanisms.
    The training process involves:
    - Pre-training on vast text corpora
    - Fine-tuning for specific tasks
    - Reinforcement Learning from Human Feedback (RLHF)
    
    ## Applications
    
    Current applications include chatbots, coding assistants, content generation tools,
    and educational platforms. These applications demonstrate the versatility and power
    of modern language models.
    """
    
    title = "Large Language Models Overview"
    
    # Test default behavior (should be concatenation + knowledge graph)
    print("🧪 Testing New Default Behavior")
    print("=" * 60)
    print("Expected: Concatenation + Knowledge Graph generation")
    print("=" * 60)
    
    # Create crew manager with default settings
    crew_manager = CrewManager(
        language="English",
        project_name="test_defaults_2024",
        technical_level="accessible",
        duration_minutes=5,
        conversation_mode="enhanced",
        tone="academic",
        focus="explanatory"
        # Note: not specifying synthesis_method or generate_knowledge_graph
        # Should use new defaults: concatenation + knowledge graph
    )
    
    print(f"🔧 Synthesis method: {crew_manager.synthesis_method}")
    print(f"🧠 Generate knowledge graph: {crew_manager.generate_knowledge_graph}")
    print()
    
    try:
        result = crew_manager.create_synthesis(test_content, title)
        print("✅ Synthesis completed successfully!")
        print(f"📏 Result length: {len(result)} characters")
        print("\n📝 Result preview:")
        print(result[:400] + "...")
        
        # Check if knowledge graph file was created
        kg_path = crew_manager.synthesis_dir / "knowledge_graph.json"
        if kg_path.exists():
            print("\n🧠 ✅ Knowledge graph file created!")
            with open(kg_path, 'r') as f:
                kg_content = f.read()
            print(f"📊 Knowledge graph size: {len(kg_content)} characters")
        else:
            print("\n🧠 ❌ Knowledge graph file NOT found")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n✨ Test completed!")

if __name__ == "__main__":
    test_new_defaults()