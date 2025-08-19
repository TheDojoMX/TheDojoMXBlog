#!/usr/bin/env python3
"""Test script to verify TLDR is added to synthesis."""

import subprocess
import sys
from pathlib import Path
import shutil
import re


def test_tldr_synthesis():
    """Test that synthesis includes TLDR section."""
    
    print("🧪 Testing TLDR in synthesis generation...")
    print("=" * 60)
    
    # Check if test PDF exists
    test_pdf = Path("test_pdf.pdf")
    if not test_pdf.exists():
        print("❌ test_pdf.pdf not found. Please provide a test PDF file.")
        return 1
    
    # Clean up any existing test project
    test_project = Path("test_tldr_project")
    if test_project.exists():
        print("🧹 Cleaning up existing test project...")
        shutil.rmtree(test_project)
    
    # Test 1: Generate synthesis with default workflow
    print("\n📋 Test 1: Generating synthesis with default workflow...")
    cmd = [
        "voice-papers",
        str(test_pdf),
        "--project-name", "test_tldr_project",
        "--language", "Spanish",
        "--duration", "3",
        "--script-only",
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Command failed with error:\n{result.stderr}")
        return 1
    
    # Check synthesis file
    synthesis_file = test_project / "synthesis" / "synthesis_output.txt"
    
    if synthesis_file.exists():
        print("✅ Synthesis file created")
        
        # Read and check for TLDR
        with open(synthesis_file, 'r', encoding='utf-8') as f:
            synthesis_content = f.read()
        
        # Check for TLDR section
        if "TLDR:" in synthesis_content:
            print("✅ TLDR section found in synthesis!")
            
            # Extract and display TLDR
            tldr_match = re.search(r'TLDR:(.*?)(?=\n\n|\Z)', synthesis_content, re.DOTALL)
            if tldr_match:
                tldr_content = tldr_match.group(1).strip()
                print("\n📝 TLDR Content:")
                print("-" * 40)
                print(tldr_content)
                print("-" * 40)
                
                # Count bullet points
                bullet_count = len(re.findall(r'^\s*[-•*]', tldr_content, re.MULTILINE))
                print(f"\n✅ Found {bullet_count} bullet points in TLDR")
        else:
            print("❌ TLDR section NOT found in synthesis!")
            print("\nFirst 500 characters of synthesis:")
            print(synthesis_content[:500])
    else:
        print("❌ Synthesis file not found!")
        return 1
    
    # Test 2: Test with summary workflow
    print("\n📋 Test 2: Testing TLDR in summary workflow...")
    
    # Clean project
    if test_project.exists():
        shutil.rmtree(test_project)
    
    cmd_summary = [
        "voice-papers",
        str(test_pdf),
        "--project-name", "test_tldr_project",
        "--language", "Spanish",
        "--duration", "3",
        "--summary",
        "--script-only",
    ]
    
    print(f"Running: {' '.join(cmd_summary)}")
    result = subprocess.run(cmd_summary, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Command failed with error:\n{result.stderr}")
        return 1
    
    # Check synthesis in summary workflow
    if synthesis_file.exists():
        with open(synthesis_file, 'r', encoding='utf-8') as f:
            synthesis_content = f.read()
        
        if "TLDR:" in synthesis_content:
            print("✅ TLDR section found in summary workflow synthesis!")
        else:
            print("❌ TLDR section NOT found in summary workflow synthesis!")
    
    # Test 3: Check if TLDR appears in final script
    script_file = test_project / "script.txt"
    if script_file.exists():
        with open(script_file, 'r', encoding='utf-8') as f:
            script_content = f.read()
        
        # TLDR should NOT appear in the final educational script
        if "TLDR:" not in script_content:
            print("✅ TLDR correctly excluded from final educational script")
        else:
            print("⚠️  TLDR found in educational script (it should be processed, not included directly)")
    
    print("\n" + "=" * 60)
    print("🎉 TLDR synthesis test completed!")
    print(f"📁 Check the synthesis at: {synthesis_file}")
    print("\nKey features:")
    print("- TLDR section with 3-5 bullet points")
    print("- Main argument in one sentence")
    print("- Key findings and implications")
    print("- Makes the synthesis scannable")
    
    return 0


if __name__ == "__main__":
    sys.exit(test_tldr_synthesis())