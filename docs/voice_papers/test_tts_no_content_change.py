#!/usr/bin/env python3
"""Test that TTS optimizer doesn't change content."""

import sys
from pathlib import Path

# Add the voice_papers module to the path
sys.path.insert(0, str(Path(__file__).parent))

from voice_papers.agents.tts_optimizer import optimize_script_for_tts

def test_content_preservation():
    """Test that content is preserved exactly."""
    
    # Test cases with awkward phrasing that might tempt rewriting
    test_cases = [
        # Awkward but must be preserved
        ("The algorithm it processes data very fast way.", 
         ["The algorithm it processes data very fast way"]),
        
        # Bad grammar but must be preserved
        ("Results shows 95% accuracy was achieved.",
         ["Results shows 95% accuracy was achieved"]),
        
        # Repetitive but must be preserved
        ("The model model uses neural networks networks for processing.",
         ["The model model uses neural networks networks for processing"]),
        
        # Short choppy sentences
        ("AI is powerful. It learns. It adapts. It improves.",
         ["AI is powerful", "It learns", "It adapts", "It improves"]),
        
        # Technical with markdown
        ("The **algorithm** achieves *95%* accuracy with `neural networks`.",
         ["The algorithm achieves 95% accuracy with neural networks"]),
    ]
    
    print("🧪 Testing TTS Content Preservation")
    print("=" * 60)
    
    all_passed = True
    for input_text, expected_phrases in test_cases:
        result = optimize_script_for_tts(input_text)
        
        # Check that all expected phrases are present (ignoring punctuation changes)
        result_normalized = result.replace('.', ' ').replace(',', ' ').replace('!', ' ').replace('?', ' ')
        passed = all(phrase in result_normalized for phrase in expected_phrases)
        
        # Check that no common "improvements" were made
        bad_changes = [
            "very fast way" in input_text and "very quickly" in result,
            "Results shows" in input_text and "Results show " in result and "Results shows" not in result,
            "model model" in input_text and result.count("model") < 2,
        ]
        
        if any(bad_changes):
            passed = False
        
        status = "✅" if passed else "❌"
        all_passed = all_passed and passed
        print(f"\n{status} Input: {repr(input_text[:50])}")
        print(f"   Output: {repr(result[:50])}")
        
        if not passed:
            print(f"   Expected phrases: {expected_phrases}")
            print(f"   Full output: {repr(result)}")
            print(f"   Normalized: {repr(result_normalized[:100])}")
    
    return all_passed

def test_tts_markup_only():
    """Test that only markup is added."""
    
    script = """# Educational Content

This is an important concept. The algorithm achieves high accuracy.

## Technical Details

The neural network uses deep learning techniques."""
    
    print("\n\n🧪 Testing TTS Markup Addition Only")
    print("=" * 60)
    
    optimized = optimize_script_for_tts(script)
    
    print("📄 Original:")
    print(script)
    print("\n📄 Optimized:")
    print(optimized)
    
    # Check content preservation (case insensitive for emphasis)
    optimized_lower = optimized.lower()
    checks = [
        "important concept" in optimized_lower,
        "algorithm achieves high accuracy" in optimized_lower,
        "neural network uses deep learning" in optimized_lower,
        "educational content" in optimized_lower,
        "technical details" in optimized_lower,
    ]
    
    # Check markup addition
    markup_checks = [
        "<break time=" in optimized,  # Break tags added
        any(word in optimized for word in ["ALGORITHM", "NEURAL", "DEEP LEARNING", "DATOS", "IMPORTANTE"]),  # Emphasis added
        "#" not in optimized,  # Markdown removed
    ]
    
    print("\n📊 Content Preservation:")
    for i, check in enumerate(checks):
        print(f"   {'✅' if check else '❌'} Content {i+1} preserved")
    
    print("\n📊 Markup Addition:")
    for i, check in enumerate(markup_checks):
        print(f"   {'✅' if check else '❌'} Markup check {i+1}")
    
    return all(checks) and any(markup_checks)

def main():
    """Run all tests."""
    print("🚀 Testing TTS Optimizer Content Preservation\n")
    
    # Test content preservation
    content_passed = test_content_preservation()
    
    # Test markup only
    markup_passed = test_tts_markup_only()
    
    print("\n" + "=" * 60)
    if content_passed and markup_passed:
        print("✅ All tests passed! Content is preserved.")
    else:
        print("❌ Some tests failed - content may be modified")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())