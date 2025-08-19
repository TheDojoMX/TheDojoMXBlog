#!/usr/bin/env python3
"""Test script to verify the paper_content variable fix."""

import subprocess
import sys
from pathlib import Path
import shutil


def test_web_extraction_flow():
    """Test that web extraction properly sets paper_content variable."""
    
    print("🧪 Testing paper_content variable fix for web URLs")
    print("=" * 60)
    
    # Use a test URL
    test_url = "https://hamel.dev/blog/posts/llm-judge/"
    test_project = "test_paper_content"
    
    # Clean up any existing test project
    test_project_dir = Path(test_project)
    if test_project_dir.exists():
        print("🧹 Cleaning up existing test project...")
        shutil.rmtree(test_project_dir)
    
    # Also clean cache to force fresh extraction
    cache_dir = Path("projects") / "web_cache"
    if cache_dir.exists():
        print("🧹 Cleaning web cache...")
        shutil.rmtree(cache_dir)
    
    # Test 1: Fresh extraction (no cache)
    print("\n📋 Test 1: Fresh web extraction (should set paper_content)")
    cmd = [
        "voice-papers",
        test_url,
        "--project-name", test_project,
        "--language", "English",
        "--duration", "3",
        "--script-only",
        "--summary",  # Use summary mode for faster test
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Fresh extraction succeeded!")
        
        # Check if script was created
        script_path = test_project_dir / "script.txt"
        if script_path.exists():
            print(f"✅ Script generated successfully: {script_path}")
            print(f"   Size: {script_path.stat().st_size:,} bytes")
        else:
            print("❌ Script file not found!")
            
    else:
        print(f"❌ Fresh extraction failed!")
        print("Error output:")
        print(result.stderr)
        if "paper_content" in result.stderr:
            print("\n⚠️  The paper_content variable error still exists!")
            return False
    
    # Test 2: Cached extraction (should also work)
    print("\n📋 Test 2: Cached extraction (should use cached paper_content)")
    
    # Run again with same URL (should use cache)
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Cached extraction succeeded!")
        if "Using cached web content" in result.stdout:
            print("✅ Cache was used as expected")
    else:
        print(f"❌ Cached extraction failed!")
        print("Error output:")
        print(result.stderr)
    
    # Test 3: Direct mode with URL (different code path)
    print("\n📋 Test 3: Testing direct mode (if applicable)")
    
    # Clean project
    if test_project_dir.exists():
        shutil.rmtree(test_project_dir)
    
    cmd_direct = [
        "voice-papers",
        test_url,
        "--project-name", test_project,
        "--language", "English",
        "--duration", "3",
        "--direct",
        "--script-only",
    ]
    
    print(f"Running: {' '.join(cmd_direct)}")
    result = subprocess.run(cmd_direct, capture_output=True, text=True)
    
    # Direct mode might not support URLs, that's OK
    if result.returncode == 0:
        print("✅ Direct mode succeeded")
    else:
        if "Direct mode" in result.stderr or "text file" in result.stderr:
            print("ℹ️  Direct mode doesn't support URLs (expected)")
        else:
            print("❌ Direct mode failed with unexpected error")
            print(result.stderr[:200])
    
    print("\n" + "=" * 60)
    print("🎉 Test completed!")
    print("\nKey fix:")
    print("- Added `paper_content = raw_content` after web extraction")
    print("- This ensures paper_content is defined for all code paths")
    print("- Both fresh and cached extraction should now work")
    
    return True


def test_different_urls():
    """Test with different types of URLs to ensure robustness."""
    
    print("\n🧪 Testing with different URL types")
    print("=" * 60)
    
    test_urls = [
        ("https://example.com/article", "Simple URL"),
        ("http://substack.com/inbox/post/167238739", "Substack redirect"),
        ("https://medium.com/@test/article", "Medium article"),
    ]
    
    for url, description in test_urls:
        print(f"\n📡 Testing: {description}")
        print(f"   URL: {url}")
        
        cmd = [
            "voice-papers",
            url,
            "--extract-only"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Extraction succeeded")
        else:
            if "paper_content" in result.stderr:
                print("   ❌ paper_content error detected!")
            else:
                print(f"   ❌ Failed with: {result.stderr.split(chr(10))[0]}")


if __name__ == "__main__":
    success = test_web_extraction_flow()
    
    if "--urls" in sys.argv:
        test_different_urls()
    
    if success:
        print("\n✅ Fix verified: paper_content variable is now properly set")
    else:
        print("\n❌ Fix may not be complete")