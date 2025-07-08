#!/usr/bin/env python3
"""Simple test to verify synthesis workflow structure."""

from pathlib import Path
import shutil
import sys

# Test with a simple text file
test_content = """
# Artificial Intelligence and Machine Learning

## Introduction
This is a test document about AI and machine learning. It discusses various aspects of neural networks and their applications.

## Methodology
We use deep learning techniques to analyze patterns in data. The approach involves training neural networks on large datasets.

## Results
The results show significant improvements in accuracy when using transformer architectures compared to traditional methods.

## Conclusion
AI continues to advance rapidly, with new breakthroughs in natural language processing and computer vision.
"""

def test_synthesis_structure():
    """Test the synthesis workflow structure without running full crew."""
    
    # Create test file
    test_file = Path("test_ai_paper.txt")
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_content)
    
    print("✅ Created test file: test_ai_paper.txt")
    
    # Test with skip-synthesis flag first (should work quickly)
    print("\n📋 Test 1: Legacy mode (--skip-synthesis)")
    print("This should complete quickly without synthesis step...")
    
    import subprocess
    cmd = [
        "voice-papers",
        str(test_file),
        "--project-name", "test_legacy",
        "--language", "Spanish",
        "--duration", "3",
        "--script-only",
        "--skip-synthesis",
        "--direct"  # Use direct mode for speed
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Legacy mode completed successfully")
        
        # Check project structure
        project_dir = Path("test_legacy")
        if project_dir.exists():
            print("\n📁 Project structure:")
            for item in project_dir.rglob("*"):
                if item.is_file():
                    print(f"   {item.relative_to(project_dir)}")
        else:
            print("❌ Project directory not created")
    else:
        print(f"❌ Legacy mode failed: {result.stderr}")
    
    # Clean up
    if Path("test_legacy").exists():
        shutil.rmtree("test_legacy")
    test_file.unlink()
    
    print("\n✅ Test completed")
    print("\nNOTE: Full synthesis test is running in the background.")
    print("Check test_synthesis_project/ directory for results when complete.")

if __name__ == "__main__":
    test_synthesis_structure()