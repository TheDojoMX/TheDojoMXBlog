#!/usr/bin/env python3
"""
Example usage of comprehensive extraction features.

This script demonstrates how to use the new extraction depth levels
and comprehensive workflows to ensure complete content preservation.
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a CLI command and display the description."""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}\n")
    
    result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
    return result.returncode == 0

def main():
    """Demonstrate different extraction depth levels and modes."""
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     COMPREHENSIVE EXTRACTION FEATURES DEMONSTRATION      ║
    ╚══════════════════════════════════════════════════════════╝
    
    This example shows how to use the new extraction features
    to ensure complete content preservation from papers.
    """)
    
    # Check if we have a test PDF
    test_pdf = Path("projects/your_brain/your_brain_gpt.pdf")
    if not test_pdf.exists():
        print(f"⚠️  Test PDF not found: {test_pdf}")
        print("Please provide a PDF file to test with")
        return
    
    # Example 1: Standard extraction (default)
    print("\n" + "="*60)
    print("EXAMPLE 1: STANDARD EXTRACTION")
    print("="*60)
    print("""
    Standard extraction with comprehensive depth (default).
    This extracts all meaningful content while maintaining readability.
    """)
    
    cmd1 = f"""uv run python -m voice_papers.cli \\
        "{test_pdf}" \\
        --language English \\
        --depth comprehensive \\
        --project-name test_standard \\
        --script-only \\
        --duration 10"""
    
    if run_command(cmd1, "Running standard comprehensive extraction"):
        print("✅ Standard extraction completed!")
    
    # Example 2: Exhaustive extraction
    print("\n" + "="*60)
    print("EXAMPLE 2: EXHAUSTIVE EXTRACTION")
    print("="*60)
    print("""
    Exhaustive extraction preserves EVERYTHING.
    Nothing is summarized, all details are kept.
    """)
    
    cmd2 = f"""uv run python -m voice_papers.cli \\
        "{test_pdf}" \\
        --language English \\
        --depth exhaustive \\
        --project-name test_exhaustive \\
        --script-only \\
        --duration 15"""
    
    if run_command(cmd2, "Running exhaustive extraction"):
        print("✅ Exhaustive extraction completed!")
    
    # Example 3: Preserve-all mode
    print("\n" + "="*60)
    print("EXAMPLE 3: PRESERVE-ALL MODE")
    print("="*60)
    print("""
    Special mode that uses exhaustive extraction workflow
    with multi-pass analysis and coverage verification.
    """)
    
    cmd3 = f"""uv run python -m voice_papers.cli \\
        "{test_pdf}" \\
        --language English \\
        --preserve-all \\
        --project-name test_preserve_all \\
        --script-only \\
        --duration 20"""
    
    if run_command(cmd3, "Running preserve-all workflow"):
        print("✅ Preserve-all workflow completed!")
    
    # Example 4: Technical preservation
    print("\n" + "="*60)
    print("EXAMPLE 4: TECHNICAL PRESERVATION")
    print("="*60)
    print("""
    Technical preservation mode for complete accuracy.
    Maintains all formulas, code, and technical specifications.
    """)
    
    cmd4 = f"""uv run python -m voice_papers.cli \\
        "{test_pdf}" \\
        --language English \\
        --technical-preservation \\
        --project-name test_technical \\
        --script-only"""
    
    if run_command(cmd4, "Running technical preservation"):
        print("✅ Technical preservation completed!")
    
    # Example 5: Comparison of depth levels
    print("\n" + "="*60)
    print("EXAMPLE 5: DEPTH LEVEL COMPARISON")
    print("="*60)
    print("""
    Compare different extraction depths on the same content.
    """)
    
    depths = ["summary", "standard", "comprehensive", "exhaustive"]
    
    for depth in depths:
        cmd = f"""uv run python -m voice_papers.cli \\
            "{test_pdf}" \\
            --language English \\
            --depth {depth} \\
            --project-name test_depth_{depth} \\
            --script-only \\
            --duration 5"""
        
        if run_command(cmd, f"Running {depth} extraction"):
            print(f"✅ {depth.capitalize()} extraction completed!")
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY OF EXTRACTION MODES")
    print("="*60)
    print("""
    📊 EXTRACTION DEPTH LEVELS:
    
    1. SUMMARY (10-20% content)
       - Main points only
       - Quick overview
       - Best for: Getting the gist
    
    2. STANDARD (40-60% content)
       - Important information with detail
       - Good balance
       - Best for: General understanding
    
    3. COMPREHENSIVE (70-90% content)
       - All meaningful content
       - Full detail on important parts
       - Best for: Thorough understanding
    
    4. EXHAUSTIVE (100-120% content)
       - Everything preserved
       - Adds explanations
       - Best for: Complete replacement of original
    
    🚀 SPECIAL MODES:
    
    • --preserve-all
      Uses exhaustive workflow with verification
      Ensures absolutely nothing is lost
    
    • --technical-preservation
      Optimized for technical accuracy
      Keeps all formulas, code, specifications
    
    • --verify-coverage
      Checks extraction completeness
      Enhances if content is missing
    
    💡 TIPS:
    
    - Use 'exhaustive' or --preserve-all for critical documents
    - Use 'comprehensive' for most educational content
    - Use 'standard' when time is limited
    - Use 'summary' only for quick overviews
    - Always use --technical-preservation for papers with code/formulas
    """)

if __name__ == "__main__":
    main()