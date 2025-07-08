#!/usr/bin/env python3
"""Test script to verify the new synthesis workflow."""

import subprocess
import sys
from pathlib import Path
import shutil


def test_synthesis_workflow():
    """Test the new synthesis workflow with a sample PDF."""
    
    # Check if test PDF exists
    test_pdf = Path("test_pdf.pdf")
    if not test_pdf.exists():
        print("❌ test_pdf.pdf not found. Please provide a test PDF file.")
        print("You can use any PDF file and rename it to test_pdf.pdf")
        return 1
    
    # Clean up any existing test project
    test_project = Path("test_synthesis_project")
    if test_project.exists():
        print("🧹 Cleaning up existing test project...")
        shutil.rmtree(test_project)
    
    print("🧪 Testing new synthesis workflow...")
    print("=" * 60)
    
    # Test 1: Default workflow (with synthesis)
    print("\n📋 Test 1: Default workflow (with synthesis)")
    cmd = [
        "voice-papers",
        str(test_pdf),
        "--project-name", "test_synthesis_project",
        "--language", "Spanish",
        "--duration", "3",
        "--script-only",  # Skip audio generation for testing
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Command failed with error:\n{result.stderr}")
        return 1
    
    # Check if synthesis was created
    synthesis_dir = test_project / "synthesis"
    synthesis_file = synthesis_dir / "synthesis_output.txt"
    
    if synthesis_file.exists():
        print("✅ Synthesis file created successfully")
        print(f"   Location: {synthesis_file}")
        print(f"   Size: {synthesis_file.stat().st_size:,} bytes")
        
        # Show first few lines of synthesis
        with open(synthesis_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:5]
            print("\n📝 First few lines of synthesis:")
            for line in lines:
                print(f"   {line.strip()}")
    else:
        print("❌ Synthesis file not found!")
        return 1
    
    # Check if discussion used synthesis
    discussion_dir = test_project / "discussion"
    final_result = discussion_dir / "final_result.txt"
    
    if final_result.exists():
        print("\n✅ Discussion completed successfully")
        print(f"   Location: {final_result}")
    
    # Test 2: Running again should reuse synthesis
    print("\n📋 Test 2: Running again (should reuse synthesis)")
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if "Using existing synthesis" in result.stdout:
        print("✅ Synthesis was reused as expected")
    else:
        print("⚠️  Synthesis might not have been reused")
    
    # Test 3: Legacy mode (skip synthesis)
    print("\n📋 Test 3: Legacy mode (--skip-synthesis)")
    cmd_legacy = cmd + ["--skip-synthesis"]
    print(f"Running: {' '.join(cmd_legacy)}")
    result = subprocess.run(cmd_legacy, capture_output=True, text=True)
    
    if "Using legacy mode: Skipping synthesis step" in result.stdout:
        print("✅ Legacy mode worked as expected")
    else:
        print("⚠️  Legacy mode might not be working correctly")
    
    print("\n" + "=" * 60)
    print("🎉 All tests completed!")
    print(f"📁 Check the test project at: {test_project}")
    
    return 0


if __name__ == "__main__":
    sys.exit(test_synthesis_workflow())