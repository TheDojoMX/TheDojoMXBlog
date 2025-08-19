#!/usr/bin/env python3
"""Test TTS optimizer heading formatting."""

import sys
from pathlib import Path

# Add the voice_papers module to the path
sys.path.insert(0, str(Path(__file__).parent))

from voice_papers.agents.tts_optimizer import optimize_script_for_tts

def test_heading_formatting():
    """Test that headings get appropriate pauses."""
    
    script_with_headings = """# Main Title

This is the introduction paragraph.

## Section One

First section content goes here.

### Subsection 1.1

Details about subsection.

## Section Two

Another main section.

# Another Main Title

Final content here."""
    
    print("🧪 Testing TTS Heading Formatting")
    print("=" * 60)
    
    print("📄 Original:")
    print(script_with_headings)
    
    optimized = optimize_script_for_tts(script_with_headings)
    
    print("\n📄 Optimized with heading pauses:")
    print("=" * 60)
    print(optimized)
    
    # Check for appropriate breaks
    print("\n📊 Analysis:")
    if '<break time="2.0s"/>' in optimized:
        print("✅ Found 2.0s breaks for main headings")
    if '<break time="1.5s"/>' in optimized:
        print("✅ Found 1.5s breaks for subheadings")
    if 'Main Title' in optimized and 'Section One' in optimized:
        print("✅ Heading text preserved")
    
    return True

def main():
    """Run heading test."""
    print("🚀 Testing TTS Optimizer Heading Support\n")
    
    test_heading_formatting()
    
    print("\n✨ Test completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())