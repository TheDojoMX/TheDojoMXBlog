#!/usr/bin/env python3
"""Test the updated technical writer with minimal connections."""

import sys
from pathlib import Path

# Add the voice_papers module to the path
sys.path.insert(0, str(Path(__file__).parent))

def test_technical_writer():
    """Test the technical writer with a sample that needs connections."""
    
    # Create test content that would benefit from connections
    test_content = """
# Advanced Neural Architecture

This groundbreaking system achieves remarkable 98% accuracy. The revolutionary approach uses three layers.

## Components

The brilliant design includes:
- Input processing module with stunning efficiency
- Hidden layers showing remarkable patterns  
- Output layer with profound implications

## Results 

The fascinating findings demonstrate:
- 98% accuracy (extraordinary improvement)
- 50ms latency (revolutionary speed)
- 2GB memory usage (remarkable efficiency)

## Methodology

The paradigm-shifting approach employs parallel processing. It transforms traditional methods completely.
"""
    
    print("🧪 Testing Technical Writer with Minimal Connections")
    print("=" * 60)
    
    # Create a temporary file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_content)
        temp_path = f.name
    
    print(f"📄 Created test file: {temp_path}")
    print("\n📝 Input content (with interpretation):")
    print(test_content[:300] + "...")
    
    # Run the CLI with technical focus
    import subprocess
    cmd = [
        sys.executable, "-m", "voice_papers.cli",
        temp_path,
        "--focus", "technical",
        "--project-name", "test_technical_connections",
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
            project_dir = Path("projects/test_technical_connections")
            script_path = project_dir / "educational_script_technical.txt"
            
            if script_path.exists():
                with open(script_path, 'r') as f:
                    output = f.read()
                
                print("\n📄 Technical Output:")
                print("=" * 60)
                print(output)
                
                # Check for minimal connections
                print("\n📊 Analysis:")
                
                # Good connections to find
                good_connections = ["Additionally", "Furthermore", "The system", "consists of", "includes", "also"]
                found_good = [conn for conn in good_connections if conn in output]
                
                # Bad interpretive words to avoid
                bad_words = ["groundbreaking", "revolutionary", "brilliant", "remarkable", 
                           "fascinating", "profound", "paradigm", "extraordinary", "stunning"]
                found_bad = [word for word in bad_words if word.lower() in output.lower()]
                
                print(f"✅ Found minimal connections: {', '.join(found_good) if found_good else 'None'}")
                print(f"{'❌' if found_bad else '✅'} Interpretive words: {', '.join(found_bad) if found_bad else 'None found (good!)'}")
                
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
    test_technical_writer()