#!/usr/bin/env python3
"""Test technical writer to ensure no meta-language."""

import sys
from pathlib import Path
import tempfile

# Add the voice_papers module to the path
sys.path.insert(0, str(Path(__file__).parent))

def test_technical_no_meta():
    """Test that technical focus avoids meta-language."""
    
    # Create a test document with content that typically triggers meta-language
    test_content = """
# Model as a Service (MaaS) Architecture

## Overview
This paper presents a comprehensive analysis of Model as a Service architectures. 
The discussion explores three main approaches and their implications.

## Approaches
The document addresses the following methodologies:
1. API-based deployment with RESTful interfaces
2. Containerized models using Docker and Kubernetes
3. Serverless functions for on-demand inference

## Implications
The analysis reveals several key implications:
- Cost reduction of 40% compared to traditional deployment
- Scalability improvements allowing 10x traffic handling
- Simplified maintenance reducing downtime by 75%

## Technical Specifications
The paper discusses technical requirements:
- Memory: 8GB minimum, 16GB recommended
- CPU: 4 cores for basic models, 8+ for complex models
- Network: 100Mbps sustained throughput
- Storage: 50GB for model artifacts

## Conclusions
The synthesis presents compelling evidence for MaaS adoption in enterprise settings.
"""
    
    print("🧪 Testing Technical Focus - No Meta-Language")
    print("=" * 60)
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_content)
        temp_path = f.name
    
    print(f"📄 Created test file: {temp_path}")
    print("\n📝 Input content (with meta-language):")
    print("- 'The paper presents...'")
    print("- 'The discussion explores...'")
    print("- 'The document addresses...'")
    print("- 'The analysis reveals...'")
    print("- 'The synthesis presents...'")
    
    # Run the CLI with technical focus
    import subprocess
    cmd = [
        sys.executable, "-m", "voice_papers.cli",
        temp_path,
        "--focus", "technical",
        "--project-name", "test_no_meta",
        "--script-only",
        "--summary",
        "--no-knowledge-graph"
    ]
    
    print("\n🚀 Running voice_papers with --focus technical")
    print("=" * 60)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Command completed successfully")
            
            # Check the output file
            project_dir = Path("/tmp/test_no_meta")
            script_path = project_dir / "educational_script_technical.txt"
            
            if script_path.exists():
                with open(script_path, 'r') as f:
                    output = f.read()
                
                print("\n📄 Technical Output:")
                print("=" * 60)
                print(output)
                print("=" * 60)
                
                # Check for meta-language
                print("\n📊 Analysis:")
                
                # Meta-language to avoid
                meta_phrases = [
                    "se presenta", "se discute", "se aborda", "se explora",
                    "el documento", "el paper", "el análisis", "la síntesis",
                    "los autores", "se menciona", "se describe"
                ]
                
                output_lower = output.lower()
                found_meta = [phrase for phrase in meta_phrases if phrase in output_lower]
                
                if found_meta:
                    print(f"❌ Found meta-language: {', '.join(found_meta)}")
                else:
                    print("✅ No meta-language found!")
                
                # Check for direct presentation
                direct_indicators = [
                    "implica:", "son:", "incluye:", "consta de:",
                    "Los tres", "El modelo", "La arquitectura"
                ]
                found_direct = [ind for ind in direct_indicators if ind in output]
                
                if found_direct:
                    print(f"✅ Found direct presentation: {', '.join(found_direct[:3])}")
                
            else:
                print("❌ Output file not found")
                
        else:
            print(f"❌ Command failed with code {result.returncode}")
            if result.stderr:
                print("STDERR:", result.stderr[:500])
            
    except subprocess.TimeoutExpired:
        print("❌ Command timed out")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Cleanup
        Path(temp_path).unlink(missing_ok=True)
        print("\n🧹 Cleaned up test file")
    
    print("\n✨ Test completed!")

if __name__ == "__main__":
    test_technical_no_meta()