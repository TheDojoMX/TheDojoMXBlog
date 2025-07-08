#!/usr/bin/env python3
"""Test script to verify robust URL extraction with multiple fallbacks."""

import sys
from pathlib import Path


def test_extraction_methods(url: str):
    """Test different extraction methods to debug issues."""
    
    print(f"🧪 Testing extraction methods for: {url}")
    print("=" * 80)
    
    # Test 1: Try the improved extractor
    print("\n1️⃣ Testing improved extractor...")
    try:
        from voice_papers.utils.web_reader_improved import ImprovedWebArticleExtractor
        extractor = ImprovedWebArticleExtractor()
        
        # Test each method individually
        methods = [
            ('_extract_with_markdown_preservation', 'Advanced markdown'),
            ('_extract_with_newspaper_markdown', 'Newspaper with markdown'),
            ('_extract_basic_with_structure', 'Basic with structure'),
            ('_extract_with_html2text_direct', 'Direct html2text'),
        ]
        
        for method_name, description in methods:
            print(f"\n   Testing {description}...")
            try:
                method = getattr(extractor, method_name)
                title, content = method(url)
                print(f"   ✅ Success! Title: {title[:60]}...")
                print(f"   Content length: {len(content):,} chars")
                
                # Save successful extraction
                filename = f"test_{method_name}.md"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"# {title}\n\n{content}")
                print(f"   💾 Saved to: {filename}")
                
                # If one method works, we're good
                return True
                
            except Exception as e:
                print(f"   ❌ Failed: {e}")
                
    except Exception as e:
        print(f"❌ Failed to load improved extractor: {e}")
    
    # Test 2: Try the basic extractor
    print("\n2️⃣ Testing basic extractor...")
    try:
        from voice_papers.utils.web_reader import extract_text_from_url
        title, content = extract_text_from_url(url)
        print(f"✅ Basic extractor succeeded!")
        print(f"Title: {title}")
        print(f"Content length: {len(content):,} chars")
        return True
        
    except Exception as e:
        print(f"❌ Basic extractor failed: {e}")
    
    return False


def test_cli_with_url(url: str):
    """Test CLI extraction with the URL."""
    import subprocess
    
    print(f"\n3️⃣ Testing CLI extraction...")
    
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
            
            # Check for cache files
            from voice_papers.utils.web_reader import generate_cache_filename
            cache_filename = generate_cache_filename(url)
            cache_dir = Path("projects") / "web_cache"
            
            txt_path = cache_dir / cache_filename
            md_path = cache_dir / cache_filename.replace('.txt', '.md')
            
            if txt_path.exists():
                print(f"✅ Text file created: {txt_path}")
                print(f"   Size: {txt_path.stat().st_size:,} bytes")
                
            if md_path.exists():
                print(f"✅ Markdown file created: {md_path}")
                print(f"   Size: {md_path.stat().st_size:,} bytes")
                
                # Show first part of content
                with open(md_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print("\n📄 First 300 characters of extracted content:")
                    print("-" * 40)
                    print(content[:300])
                    print("-" * 40)
                    
        else:
            print("❌ CLI extraction failed!")
            print("Error output:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Failed to run CLI: {e}")


def analyze_url_issues(url: str):
    """Analyze potential issues with URL extraction."""
    import requests
    from bs4 import BeautifulSoup
    
    print(f"\n🔍 Analyzing URL: {url}")
    print("-" * 60)
    
    try:
        # Check URL accessibility
        response = requests.get(url, timeout=10, allow_redirects=True)
        print(f"✅ URL accessible: Status {response.status_code}")
        
        if response.history:
            print(f"🔄 Redirected through:")
            for r in response.history:
                print(f"   - {r.url} [{r.status_code}]")
            print(f"   → Final URL: {response.url}")
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Check for common content containers
        print("\n📊 Content analysis:")
        
        containers = {
            'article': len(soup.find_all('article')),
            'main': len(soup.find_all('main')),
            'div.content': len(soup.select('div.content')),
            'div.post': len(soup.select('div.post')),
            '.available-content': len(soup.select('.available-content')),
            '.body.markup': len(soup.select('.body.markup')),
            'p tags': len(soup.find_all('p')),
            'h1 tags': len(soup.find_all('h1')),
            'h2 tags': len(soup.find_all('h2')),
        }
        
        for selector, count in containers.items():
            if count > 0:
                print(f"   ✓ {selector}: {count}")
            else:
                print(f"   ✗ {selector}: 0")
        
        # Check page structure
        print(f"\n📐 Page structure:")
        print(f"   Total text length: {len(soup.get_text()):,} chars")
        
        # Look for title
        title_tag = soup.find('title')
        if title_tag:
            print(f"   Title tag: {title_tag.text.strip()[:60]}...")
            
        h1_tag = soup.find('h1')
        if h1_tag:
            print(f"   First H1: {h1_tag.get_text().strip()[:60]}...")
            
    except Exception as e:
        print(f"❌ Failed to analyze URL: {e}")


def main():
    """Main test function."""
    # Default test URL (Substack)
    test_url = "http://substack.com/inbox/post/167238739"
    
    if len(sys.argv) > 1:
        test_url = sys.argv[1]
    
    print("🚀 Robust URL Extraction Test")
    print("=" * 80)
    
    # Analyze URL first
    analyze_url_issues(test_url)
    
    # Test extraction methods
    print("\n")
    success = test_extraction_methods(test_url)
    
    # Test CLI
    print("\n")
    test_cli_with_url(test_url)
    
    # Summary
    print("\n" + "=" * 80)
    if success:
        print("✅ Extraction successful with fallback methods!")
        print("\nKey improvements:")
        print("- Multiple fallback methods for content detection")
        print("- Better handling of redirects")
        print("- More flexible content area detection")
        print("- Direct html2text fallback for difficult pages")
        print("- Automatic HTTP to HTTPS upgrade")
    else:
        print("❌ All extraction methods failed")
        print("\nPossible issues:")
        print("- Page might require JavaScript")
        print("- Content might be behind authentication")
        print("- Site might have aggressive anti-bot measures")
        print("- Unusual HTML structure")


if __name__ == "__main__":
    main()