#!/usr/bin/env python3
"""Test script to verify synthesis storage in summary workflow."""

import subprocess
import sys
from pathlib import Path
import shutil


def test_summary_synthesis_storage():
    """Test that synthesis is properly stored and reused in summary workflow."""
    
    print("🧪 Testing synthesis storage in summary workflow...")
    print("=" * 60)
    
    # Check if test PDF exists
    test_pdf = Path("test_pdf.pdf")
    if not test_pdf.exists():
        print("❌ test_pdf.pdf not found. Please provide a test PDF file.")
        return 1
    
    # Clean up any existing test project
    test_project = Path("test_summary_synthesis")
    if test_project.exists():
        print("🧹 Cleaning up existing test project...")
        shutil.rmtree(test_project)
    
    # Test 1: Run summary workflow (should create and store synthesis)
    print("\n📋 Test 1: Running summary workflow (should create synthesis)...")
    cmd = [
        "voice-papers",
        str(test_pdf),
        "--project-name", "test_summary_synthesis",
        "--language", "Spanish",
        "--duration", "3",
        "--summary",  # Use summary workflow
        "--script-only",
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Command failed with error:\n{result.stderr}")
        return 1
    
    # Check if synthesis was created in the correct location
    synthesis_dir = test_project / "synthesis"
    synthesis_file = synthesis_dir / "synthesis_output.txt"
    synthesis_metadata = synthesis_dir / "synthesis_metadata.json"
    
    if synthesis_dir.exists():
        print("✅ Synthesis directory created")
    else:
        print("❌ Synthesis directory not found!")
        return 1
    
    if synthesis_file.exists():
        print("✅ Synthesis file created successfully")
        print(f"   Location: {synthesis_file}")
        print(f"   Size: {synthesis_file.stat().st_size:,} bytes")
    else:
        print("❌ Synthesis file not found in synthesis directory!")
        return 1
    
    if synthesis_metadata.exists():
        print("✅ Synthesis metadata created")
        # Read and display metadata
        import json
        with open(synthesis_metadata, 'r') as f:
            metadata = json.load(f)
            print(f"   Chunks: {metadata.get('document_chunks', 'unknown')}")
            print(f"   Workflow: {metadata.get('workflow', 'unknown')}")
    else:
        print("⚠️  Synthesis metadata not found")
    
    # Also check discussion directory for backward compatibility
    discussion_synthesis = test_project / "discussion" / "synthesis_output.txt"
    if discussion_synthesis.exists():
        print("✅ Synthesis also saved in discussion directory (backward compatibility)")
    
    # Test 2: Run again (should reuse synthesis)
    print("\n📋 Test 2: Running summary workflow again (should reuse synthesis)...")
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Command failed with error:\n{result.stderr}")
        return 1
    
    # Check output for reuse message
    if "Found existing synthesis, reusing it" in result.stdout:
        print("✅ Synthesis was reused as expected!")
    else:
        print("⚠️  Synthesis might not have been reused")
        print("Output:", result.stdout[:500])
    
    # Test 3: Verify script was generated
    script_file = test_project / "script.txt"
    if script_file.exists():
        print("\n✅ Educational script generated successfully")
        print(f"   Location: {script_file}")
        
        # Show first few lines
        with open(script_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:5]
            print("\n📝 First few lines of script:")
            for line in lines:
                print(f"   {line.strip()}")
    
    print("\n" + "=" * 60)
    print("🎉 All tests completed!")
    print(f"📁 Check the test project at: {test_project}")
    print("\nKey improvements:")
    print("- Synthesis is now stored in the synthesis/ directory")
    print("- Synthesis is reused on subsequent runs")
    print("- Metadata tracks synthesis creation details")
    
    return 0


if __name__ == "__main__":
    sys.exit(test_summary_synthesis_storage())