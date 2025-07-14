#!/usr/bin/env python3
"""Test that TTS optimizer removes markdown without changing content."""

import sys
from pathlib import Path

# Add the voice_papers module to the path
sys.path.insert(0, str(Path(__file__).parent))

from voice_papers.agents.tts_optimizer import remove_markdown_formatting, optimize_script_for_tts

def test_markdown_removal():
    """Test markdown removal function."""
    
    test_cases = [
        # Headers
        ("# This is a header\nContent here", "This is a header\nContent here"),
        ("## Section Title\nText", "Section Title\nText"),
        
        # Bold
        ("This is **bold text** here", "This is bold text here"),
        ("This is __also bold__ text", "This is also bold text"),
        
        # Italic
        ("This is *italic text* here", "This is italic text here"),
        ("This is _also italic_ text", "This is also italic text"),
        
        # Mixed
        ("**Bold** and *italic* and `code`", "Bold and italic and code"),
        
        # Lists
        ("- Item 1\n- Item 2", "Item 1\nItem 2"),
        ("1. First\n2. Second", "First\nSecond"),
        
        # Links
        ("Check [this link](http://example.com)", "Check this link"),
        
        # Code blocks
        ("```python\nprint('hello')\n```", "print('hello')"),
    ]
    
    print("🧪 Testing Markdown Removal")
    print("=" * 60)
    
    all_passed = True
    for input_text, expected in test_cases:
        result = remove_markdown_formatting(input_text)
        passed = result == expected
        all_passed &= passed
        
        status = "✅" if passed else "❌"
        print(f"{status} Input: {repr(input_text[:30])}")
        if not passed:
            print(f"   Expected: {repr(expected)}")
            print(f"   Got:      {repr(result)}")
    
    return all_passed

def test_full_optimization():
    """Test full TTS optimization with markdown content."""
    
    script_with_markdown = """# Revolutionary Discovery

This **groundbreaking** research presents a *paradigm-shifting* approach.

## Key Findings

- The algorithm achieves **95% accuracy**
- Processing speed improved by *65%*
- Memory usage reduced

The `neural network` uses **deep learning** to process data.

### Conclusion

This *transformative* research opens **exciting** possibilities.
"""
    
    expected_content_preserved = [
        "Revolutionary Discovery",
        "groundbreaking research presents a paradigm-shifting approach",
        "Key Findings",
        "The algorithm achieves 95% accuracy",
        "Processing speed improved by 65%",
        "Memory usage reduced",
        "neural network uses deep learning",
        "Conclusion",
        "transformative research opens exciting possibilities"
    ]
    
    print("\n🧪 Testing Full TTS Optimization")
    print("=" * 60)
    
    optimized = optimize_script_for_tts(script_with_markdown)
    
    print("📄 Original (with markdown):")
    print(script_with_markdown[:200] + "...")
    print("\n📄 Optimized (markdown removed):")
    print(optimized[:200] + "...")
    
    # Check that all content is preserved
    all_content_preserved = True
    for content in expected_content_preserved:
        if content.lower() not in optimized.lower():
            print(f"❌ Missing content: {content}")
            all_content_preserved = False
    
    # Check that markdown is removed
    markdown_removed = True
    markdown_patterns = ["**", "*", "##", "###", "```", "`", "- ", "1. "]
    for pattern in markdown_patterns:
        if pattern in optimized and pattern != "- ":  # Allow hyphen in text
            print(f"❌ Markdown still present: {pattern}")
            markdown_removed = False
    
    if all_content_preserved and markdown_removed:
        print("\n✅ All content preserved and markdown removed!")
    else:
        if not all_content_preserved:
            print("\n❌ Some content was lost")
        if not markdown_removed:
            print("\n❌ Some markdown still present")
    
    return all_content_preserved and markdown_removed

def main():
    """Run all tests."""
    print("🚀 Testing TTS Optimizer Markdown Removal\n")
    
    # Test basic markdown removal
    basic_passed = test_markdown_removal()
    
    # Test full optimization
    full_passed = test_full_optimization()
    
    print("\n" + "=" * 60)
    if basic_passed and full_passed:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())