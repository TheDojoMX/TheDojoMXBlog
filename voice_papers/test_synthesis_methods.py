#!/usr/bin/env python3
"""Test script to compare synthesis methods."""

import sys
from pathlib import Path
import os

# Add the voice_papers module to the path
sys.path.insert(0, str(Path(__file__).parent))

from voice_papers.agents.crew_manager import CrewManager

def test_synthesis_methods():
    """Test both concatenation and knowledge_graph synthesis methods."""
    
    # Test content
    test_content = """
    # Scale in AI: The Defining Feature of Modern AI
    
    If I could use only one word to describe AI post-2020, it would be scale. The AI models
    behind applications like ChatGPT, Google's Gemini, and Midjourney are at such a
    scale that they're consuming a nontrivial portion of the world's electricity.
    
    ## The Scaling Consequences
    
    The scaling up of AI models has two major consequences:
    
    1. AI models are becoming more powerful and capable of more tasks
    2. Training requires resources that only a few organizations can afford
    
    This has led to the emergence of "model as a service" - models developed by few 
    organizations are made available for others to use as a service.
    
    ## Foundation Models
    
    Foundation models emerged from large language models. They use self-supervision
    to grow to unprecedented scale. A language model encodes statistical information
    about languages, telling us how likely a word is to appear in a given context.
    
    ## Applications
    
    Modern AI enables applications like:
    - ChatGPT for conversational AI
    - GitHub Copilot for code generation  
    - Midjourney for image generation
    
    These represent the culmination of decades of technology advancement.
    """
    
    title = "Scale in AI: The Defining Feature"
    
    # Create crew manager
    crew_manager = CrewManager(
        language="English",
        project_name="synthesis_test",
        technical_level="accessible",
        duration_minutes=5,
        conversation_mode="enhanced",
        tone="academic",
        focus="explanatory"
    )
    
    print("🧪 Testing Synthesis Methods")
    print("=" * 50)
    
    # Test concatenation method
    print("\n1️⃣ Testing Concatenation Method...")
    try:
        concatenation_result = crew_manager.create_synthesis(
            test_content, title, synthesis_method="concatenation"
        )
        print("✅ Concatenation synthesis completed")
        print(f"📏 Length: {len(concatenation_result)} characters")
        print("📝 Sample:")
        print(concatenation_result[:300] + "...")
    except Exception as e:
        print(f"❌ Concatenation failed: {e}")
    
    print("\n" + "=" * 50)
    
    # Test knowledge graph method
    print("\n2️⃣ Testing Knowledge Graph Method...")
    try:
        kg_result = crew_manager.create_synthesis(
            test_content, title, synthesis_method="knowledge_graph"
        )
        print("✅ Knowledge graph synthesis completed")
        print(f"📏 Length: {len(kg_result)} characters")
        print("📝 Sample:")
        print(kg_result[:300] + "...")
    except Exception as e:
        print(f"❌ Knowledge graph failed: {e}")
    
    print("\n" + "=" * 50)
    
    # Test original method
    print("\n3️⃣ Testing Original Method...")
    try:
        original_result = crew_manager.create_synthesis(
            test_content, title, synthesis_method="original"
        )
        print("✅ Original synthesis completed")
        print(f"📏 Length: {len(original_result)} characters")
        print("📝 Sample:")
        print(original_result[:300] + "...")
    except Exception as e:
        print(f"❌ Original failed: {e}")
    
    print("\n✨ Test completed!")

if __name__ == "__main__":
    test_synthesis_methods()