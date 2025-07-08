#!/usr/bin/env python3
"""Test script to verify Substack URL extraction with redirect handling."""

import sys
from pathlib import Path


def test_substack_extraction():
    """Test extraction from Substack URLs including redirect handling."""
    
    # Test URLs including the problematic one
    test_urls = [
        "http://substack.com/inbox/post/167238739",  # Redirect URL
        "https://simonw.substack.com/p/gemma-3n-context-engineering-and",  # Direct URL
    ]
    
    print("🧪 Testing Substack URL extraction")
    print("=" * 80)
    
    for url in test_urls:
        print(f"\n📡 Testing URL: {url}")
        print("-" * 60)
        
        try:
            # Try improved extractor
            from voice_papers.utils.web_reader_improved import extract_text_from_url_improved
            
            print("Using improved extractor...")
            title, content = extract_text_from_url_improved(url)
            
            print(f"✅ Extraction successful!")
            print(f"📌 Title: {title}")
            print(f"📏 Content length: {len(content):,} characters")
            
            # Check for Substack-specific content
            print("\n🔍 Content Analysis:")
            
            # Check if content looks like markdown
            has_headings = '#' in content
            has_links = '[' in content and '](' in content
            has_lists = '\n- ' in content or '\n* ' in content
            has_blockquotes = '\n> ' in content
            
            print(f"   Has markdown headings: {has_headings}")
            print(f"   Has markdown links: {has_links}")
            print(f"   Has lists: {has_lists}")
            print(f"   Has blockquotes: {has_blockquotes}")
            
            # Show first 500 chars
            print("\n📄 First 500 characters:")
            print("-" * 40)
            print(content[:500])
            print("-" * 40)
            
            # Save the content
            filename = f"test_substack_{test_urls.index(url) + 1}.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n{content}")
            print(f"\n💾 Saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            
            # Try basic extractor as fallback
            try:
                print("\n🔄 Trying basic extractor...")
                from voice_papers.utils.web_reader import extract_text_from_url
                
                title, content = extract_text_from_url(url)
                print(f"✅ Basic extraction successful!")
                print(f"📌 Title: {title}")
                print(f"📏 Content length: {len(content):,} characters")
                
            except Exception as e2:
                print(f"❌ Basic extraction also failed: {e2}")
                import traceback
                traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("✅ Test completed!")
    print("\nTips for Substack extraction:")
    print("- Redirects are now handled automatically")
    print("- Substack-specific selectors added")
    print("- Content structure preserved")
    print("- Works with both inbox and direct article URLs")


def test_cli_extraction():
    """Test extraction using the CLI."""
    import subprocess
    
    print("\n🧪 Testing CLI extraction with Substack URL")
    print("=" * 80)
    
    url = "http://substack.com/inbox/post/167238739"
    
    cmd = [
        "voice-papers",
        url,
        "--extract-only"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ CLI extraction successful!")
            print("\nOutput:")
            print(result.stdout)
            
            # Check if cache file was created
            from voice_papers.utils.web_reader import generate_cache_filename
            cache_filename = generate_cache_filename(url)
            cache_path = Path("projects") / "web_cache" / cache_filename
            markdown_path = Path("projects") / "web_cache" / cache_filename.replace('.txt', '.md')
            
            if cache_path.exists():
                print(f"\n✅ Cache file created: {cache_path}")
                print(f"   Size: {cache_path.stat().st_size:,} bytes")
                
            if markdown_path.exists():
                print(f"✅ Markdown file created: {markdown_path}")
                print(f"   Size: {markdown_path.stat().st_size:,} bytes")
                
        else:
            print("❌ CLI extraction failed!")
            print("\nError:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Failed to run CLI: {e}")


if __name__ == "__main__":
    test_substack_extraction()
    
    if "--cli" in sys.argv:
        test_cli_extraction()