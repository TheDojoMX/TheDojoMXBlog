#!/usr/bin/env python3
"""Test script to verify hook improvements in educational scripts."""

import subprocess
import sys
from pathlib import Path
import re


def test_hook_improvements():
    """Test that educational scripts start with hooks and avoid 'En resumen' at the beginning."""
    
    print("🧪 Testing hook improvements in educational scripts...")
    print("=" * 60)
    
    # Check if test PDF exists
    test_pdf = Path("test_pdf.pdf")
    if not test_pdf.exists():
        print("❌ test_pdf.pdf not found. Please provide a test PDF file.")
        return 1
    
    # Test with a short script to see the beginning
    print("\n📋 Generating a test script to check the introduction...")
    cmd = [
        "voice-papers",
        str(test_pdf),
        "--project-name", "test_hook_project",
        "--language", "Spanish",
        "--duration", "3",
        "--script-only",
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Command failed with error:\n{result.stderr}")
        return 1
    
    # Check the generated script
    script_path = Path("test_hook_project") / "script.txt"
    
    if script_path.exists():
        print("\n✅ Script generated successfully")
        
        # Read the beginning of the script
        with open(script_path, 'r', encoding='utf-8') as f:
            script_content = f.read()
            first_500_chars = script_content[:500]
            
        print("\n📝 First 500 characters of the script:")
        print("-" * 60)
        print(first_500_chars)
        print("-" * 60)
        
        # Check for problematic starts
        problematic_starts = [
            "En resumen",
            "Hoy vamos a hablar de",
            "Este es un resumen de",
            "En este episodio",
            "Hoy exploramos",
            "Vamos a analizar",
        ]
        
        script_start = script_content[:100].lower()
        found_problems = []
        
        for problem in problematic_starts:
            if problem.lower() in script_start:
                found_problems.append(problem)
        
        if found_problems:
            print(f"\n❌ Found problematic starts: {', '.join(found_problems)}")
            print("The script should start with a hook instead!")
        else:
            print("\n✅ No problematic starts found")
            
        # Check for good hook patterns
        hook_patterns = [
            r'^¿[^?]+\?',  # Starts with a question
            r'^Imagina',    # Starts with "Imagina"
            r'^Hay algo',   # Starts with "Hay algo"
            r'^Piensa',     # Starts with "Piensa"
            r'^¿Alguna vez', # Starts with "¿Alguna vez"
            r'^¿Qué pasaría', # Starts with "¿Qué pasaría"
            r'^¿Te has preguntado', # Starts with "¿Te has preguntado"
        ]
        
        found_hook = False
        for pattern in hook_patterns:
            if re.match(pattern, script_content.strip(), re.IGNORECASE):
                found_hook = True
                print("✅ Script starts with a good hook!")
                break
        
        if not found_hook:
            print("\n⚠️  Script might not start with a strong hook")
            print("Consider starting with a question or intriguing statement")
        
        # Check if title is mentioned after the hook
        lines = script_content.split('\n')
        title_mentioned = False
        
        # Check first few paragraphs for title mention
        first_paragraphs = '\n'.join(lines[:10])
        if test_pdf.stem in first_paragraphs or "test_pdf" in first_paragraphs.lower():
            title_mentioned = True
            print("✅ Title is mentioned in the introduction")
        else:
            print("⚠️  Title might not be mentioned clearly in the introduction")
            
    else:
        print("❌ Script file not found!")
        return 1
    
    print("\n" + "=" * 60)
    print("🎉 Hook improvement test completed!")
    print(f"📁 Check the full script at: {script_path}")
    
    return 0


if __name__ == "__main__":
    sys.exit(test_hook_improvements())