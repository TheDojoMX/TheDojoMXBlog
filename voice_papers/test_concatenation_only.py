#!/usr/bin/env python3
"""Test script to specifically test concatenation method."""

import sys
from pathlib import Path
import os

# Add the voice_papers module to the path
sys.path.insert(0, str(Path(__file__).parent))

from voice_papers.agents.crew_manager import CrewManager

def test_concatenation_method():
    """Test only concatenation synthesis method."""
    
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
    """
    
    title = "Scale in AI Test"
    
    # Create crew manager with unique project name
    crew_manager = CrewManager(
        language="English",
        project_name="concat_test_unique",
        technical_level="accessible",
        duration_minutes=5,
        conversation_mode="enhanced",
        tone="academic",
        focus="explanatory"
    )
    
    print("🧪 Testing ONLY Concatenation Method")
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
        print(concatenation_result[:500] + "...")
    except Exception as e:
        print(f"❌ Concatenation failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n✨ Test completed!")

if __name__ == "__main__":
    test_concatenation_method()