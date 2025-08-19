#!/usr/bin/env python3
"""Test the light edit flow."""

import sys
from pathlib import Path
import tempfile

# Add the voice_papers module to the path
sys.path.insert(0, str(Path(__file__).parent))

def test_light_edit_flow():
    """Test the complete light edit flow."""
    
    # Create a test document with grammar errors
    test_content = """
# Los Avance en IA

## Introducción

La inteligencia artificial está cambiando el mundo. Los resultado de investigación 
reciente muestran que la algoritmo pueden superar a humanos en muchas tarea.

## Los Método Principal

El sistema utiliza tres metodo principal:
1. Aprendizaje profundo con red neuronal
2. Procesamiento de lenguaje natural avanzado
3. Visión computacional para analizar imagen

## Resultado

Los experimento demuestran:
- Precisión de 95% en clasificación de dato
- Reducción de 40% en tiempo de procesamiento
- Mejora significativa en eficiencia energética

## Conclusión

Este avance representa un paso importante en desarrollo de IA.
La tecnología está basado a principios sólidos y ofrece resultado prometedor.
"""
    
    print("🧪 Testing Light Edit Flow")
    print("=" * 60)
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_content)
        temp_path = f.name
    
    print(f"📄 Created test file: {temp_path}")
    print("\n📝 Input content (with grammar errors):")
    print("- 'Los resultado' (should be 'Los resultados')")
    print("- 'la algoritmo' (should be 'el algoritmo')")
    print("- 'tres metodo' (should be 'tres métodos')")
    print("- 'está basado a' (should be 'está basada en')")
    
    # Run the CLI with summary + light edit
    import subprocess
    cmd = [
        sys.executable, "-m", "voice_papers.cli",
        temp_path,
        "--summary",
        "--light-edit",
        "--project-name", "test_light_edit",
        "--script-only",
        "--no-knowledge-graph"
    ]
    
    print("\n🚀 Running voice_papers with --summary --light-edit")
    print("=" * 60)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Command completed successfully")
            
            # Check the output file
            project_dir = Path("/tmp/test_light_edit")
            script_path = project_dir / "educational_script.txt"
            
            if script_path.exists():
                with open(script_path, 'r') as f:
                    output = f.read()
                
                print("\n📄 Final Output (excerpt):")
                print("=" * 60)
                print(output[:800] + "...")
                
                # Check if basic errors were fixed
                print("\n📊 Grammar Check:")
                
                errors_fixed = [
                    ("Los resultados" in output, "Gender agreement: 'Los resultados'"),
                    ("el algoritmo" in output or "los algoritmos" in output, "Gender agreement: 'el algoritmo'"),
                    ("tres métodos" in output, "Number agreement: 'tres métodos'"),
                    ("basada en" in output or "basado en" in output, "Preposition: 'basado en'"),
                ]
                
                for fixed, description in errors_fixed:
                    print(f"   {'✅' if fixed else '❌'} {description}")
                
                # Check that content is preserved
                content_preserved = [
                    "95%" in output,
                    "40%" in output,
                    "inteligencia artificial" in output.lower(),
                    "aprendizaje profundo" in output.lower(),
                ]
                
                if all(content_preserved):
                    print("\n✅ Content preserved correctly")
                else:
                    print("\n⚠️  Some content may have been modified")
                
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
    test_light_edit_flow()