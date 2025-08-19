#!/usr/bin/env python3
"""Test the full technical focus workflow."""

import sys
from pathlib import Path
import tempfile

# Add the voice_papers module to the path
sys.path.insert(0, str(Path(__file__).parent))

def test_technical_focus():
    """Test the complete technical focus workflow."""
    
    # Create a test document with interpretive language
    test_content = """
# Revolutionary Breakthrough in Machine Learning

This groundbreaking paper presents a paradigm-shifting approach that fundamentally 
transforms our understanding of neural networks. The brilliant researchers have 
achieved remarkable results that suggest profound implications for the future of AI.

## Methodology

The elegant methodology employs a sophisticated three-phase approach:
1. Data collection from 10,000 samples
2. Training using a novel algorithm with 50 epochs
3. Validation on separate test sets

## Results

The fascinating results demonstrate:
- An impressive 97.2% accuracy rate
- Revolutionary 65% reduction in training time
- Remarkable memory efficiency improvements of 40%

These extraordinary findings imply that future systems could be dramatically more efficient.

## Conclusions

This transformative research opens exciting new possibilities and suggests a 
fundamental shift in how we approach machine learning. The implications are profound.
"""
    
    print("🧪 Testing Technical Focus Mode - Full Workflow")
    print("=" * 60)
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_content)
        temp_path = f.name
    
    print(f"📄 Created test file: {temp_path}")
    print("\n📝 Input content preview (with interpretation):")
    print(test_content[:300] + "...")
    
    # Run the CLI with technical focus
    import subprocess
    cmd = [
        sys.executable, "-m", "voice_papers.cli",
        temp_path,
        "--focus", "technical",
        "--project-name", "test_technical_focus",
        "--script-only",  # Don't generate audio
        "--summary",  # Use summary mode for faster test
        "--no-knowledge-graph"  # Skip knowledge graph
    ]
    
    print("\n🚀 Running voice_papers with --focus technical")
    print(f"Command: {' '.join(cmd)}")
    print("=" * 60)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Command completed successfully")
            
            # Check the output file
            project_dir = Path("projects/test_technical_focus")
            script_path = project_dir / "educational_script.txt"
            
            if script_path.exists():
                with open(script_path, 'r') as f:
                    output = f.read()
                
                print("\n📄 Technical Output Preview:")
                print("=" * 60)
                print(output[:800] + "...")
                
                # Check for interpretation words
                interpretation_words = [
                    "revolutionary", "groundbreaking", "brilliant", "remarkable",
                    "fascinating", "elegant", "extraordinary", "transformative",
                    "paradigm", "profound", "suggests", "implies"
                ]
                
                output_lower = output.lower()
                found_words = [word for word in interpretation_words if word in output_lower]
                
                print("\n📊 Analysis:")
                print(f"   Interpretation words in output: {len(found_words)}")
                if found_words:
                    print(f"   ⚠️  Found: {', '.join(found_words[:5])}...")
                else:
                    print("   ✅ No interpretation words found!")
                
            else:
                print("❌ Output file not found")
                
        else:
            print(f"❌ Command failed with code {result.returncode}")
            print("STDERR:", result.stderr)
            
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
    test_technical_focus()