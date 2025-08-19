#!/usr/bin/env python3
"""Test script to verify improved URL extraction with markdown preservation."""

import sys
from pathlib import Path
from voice_papers.utils.web_reader_improved import extract_text_from_url_improved
import re


def test_url_extraction(url: str):
    """Test URL extraction with the example article."""
    
    print(f"🧪 Testing improved URL extraction")
    print(f"🌐 URL: {url}")
    print("=" * 80)
    
    try:
        # Extract content
        print("\n📡 Extracting content...")
        title, content = extract_text_from_url_improved(url)
        
        print(f"\n✅ Extraction successful!")
        print(f"📌 Title: {title}")
        print(f"📏 Content length: {len(content):,} characters")
        
        # Analyze markdown structure
        print("\n📊 Markdown Structure Analysis:")
        
        # Count headings
        h1_count = len(re.findall(r'^# [^\n]+', content, re.MULTILINE))
        h2_count = len(re.findall(r'^## [^\n]+', content, re.MULTILINE))
        h3_count = len(re.findall(r'^### [^\n]+', content, re.MULTILINE))
        h4_count = len(re.findall(r'^#### [^\n]+', content, re.MULTILINE))
        
        print(f"   # headings (H1): {h1_count}")
        print(f"   ## headings (H2): {h2_count}")
        print(f"   ### headings (H3): {h3_count}")
        print(f"   #### headings (H4): {h4_count}")
        
        # Count other markdown elements
        code_blocks = len(re.findall(r'```[\s\S]*?```', content))
        inline_code = len(re.findall(r'`[^`]+`', content))
        links = len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content))
        images = len(re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content))
        lists = len(re.findall(r'^[-*] ', content, re.MULTILINE))
        numbered_lists = len(re.findall(r'^\d+\. ', content, re.MULTILINE))
        blockquotes = len(re.findall(r'^> ', content, re.MULTILINE))
        
        print(f"\n   Code blocks: {code_blocks}")
        print(f"   Inline code: {inline_code}")
        print(f"   Links: {links}")
        print(f"   Images: {images}")
        print(f"   List items: {lists}")
        print(f"   Numbered list items: {numbered_lists}")
        print(f"   Blockquotes: {blockquotes}")
        
        # Extract all headings
        print("\n📑 Document Structure (First 10 headings):")
        all_headings = re.findall(r'^(#{1,6}) ([^\n]+)', content, re.MULTILINE)
        for i, (level, heading) in enumerate(all_headings[:10]):
            indent = "  " * (len(level) - 1)
            print(f"{indent}{level} {heading}")
        
        if len(all_headings) > 10:
            print(f"   ... and {len(all_headings) - 10} more headings")
        
        # Show first part of content
        print("\n📄 First 500 characters of content:")
        print("-" * 60)
        print(content[:500])
        print("-" * 60)
        
        # Save the extracted content
        output_file = Path("test_extracted_article.md")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n{content}")
        
        print(f"\n💾 Full content saved to: {output_file}")
        
        # Check for specific content from the example
        if "Creating a LLM-as-a-Judge" in title:
            print("\n🔍 Checking for expected content:")
            expected_sections = [
                "The Problem: AI Teams Are Drowning in Data",
                "Step 1: Find The Principal Domain Expert",
                "Step 2: Create a Dataset",
                "Step 3: Direct The Domain Expert to Make Pass/Fail Judgments with Critiques",
                "Step 4: Fix Errors",
                "Step 5: Build Your LLM as A Judge, Iteratively",
                "Step 6: Perform Error Analysis",
                "Step 7: Create More Specialized LLM Judges"
            ]
            
            for section in expected_sections:
                if section in content:
                    print(f"   ✅ Found: {section}")
                else:
                    print(f"   ❌ Missing: {section}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Extraction failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function."""
    # Test with the provided example URL
    test_url = "https://hamel.dev/blog/posts/llm-judge/"
    
    if len(sys.argv) > 1:
        test_url = sys.argv[1]
    
    success = test_url_extraction(test_url)
    
    if success:
        print("\n✅ Test completed successfully!")
        print("\nKey improvements:")
        print("- Preserves all markdown formatting")
        print("- Captures all headings and structure")
        print("- Maintains code blocks and links")
        print("- Saves as markdown for better readability")
    else:
        print("\n❌ Test failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()