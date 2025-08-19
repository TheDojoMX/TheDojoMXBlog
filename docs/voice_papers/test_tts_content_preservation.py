#!/usr/bin/env python3
"""Test script to verify TTS Optimizer preserves content."""

import sys
from pathlib import Path
import re

# Add the voice_papers module to the path
sys.path.insert(0, str(Path(__file__).parent))

from voice_papers.agents.crew_manager import CrewManager

def extract_core_content(text):
    """Extract the core educational content by removing TTS markup and formatting."""
    # Remove TTS markup
    text = re.sub(r'<break[^>]*/?>', '', text)
    text = re.sub(r'<phoneme[^>]*>([^<]+)</phoneme>', r'\1', text)
    text = re.sub(r'<lexeme[^>]*>.*?</lexeme>', '', text)
    
    # Convert emphasized words back to normal (for comparison)
    # Keep the words but remove extra emphasis
    text = text.lower()
    
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def test_tts_content_preservation():
    """Test that TTS optimization preserves educational content."""
    
    original_script = """
    # Los Modelos de Lenguaje: Una Revolución en la Inteligencia Artificial
    
    Los modelos de lenguaje de gran escala representan un avance significativo en la inteligencia artificial.
    Estos sistemas, como GPT-4 y Claude, demuestran capacidades extraordinarias en múltiples dominios.
    
    ## Capacidades Clave
    
    Los modelos de lenguaje destacan en varias áreas importantes:
    
    1. Comprensión y generación de lenguaje natural
    2. Generación y depuración de código
    3. Razonamiento matemático complejo
    4. Escritura creativa y narrativa
    
    ## Proceso de Entrenamiento
    
    El entrenamiento utiliza arquitectura transformer con mecanismos de autoatención.
    El proceso incluye:
    - Preentrenamiento en corpus de texto masivos
    - Ajuste fino para tareas específicas
    - Aprendizaje por refuerzo con retroalimentación humana
    
    ## Aplicaciones Prácticas
    
    Las aplicaciones actuales incluyen chatbots inteligentes, asistentes de programación,
    herramientas de generación de contenido y plataformas educativas avanzadas.
    Estas aplicaciones demuestran la versatilidad y el poder de los modelos modernos.
    """
    
    print("🧪 Testing TTS Content Preservation")
    print("=" * 60)
    
    # Create crew manager
    crew_manager = CrewManager(
        language="Spanish",
        project_name="tts_test_preservation",
        technical_level="accessible",
        duration_minutes=5,
        conversation_mode="enhanced",
        tone="academic",
        focus="explanatory"
    )
    
    try:
        # Get TTS optimizer
        from voice_papers.agents.tts_optimizer import get_tts_optimizer_agent, create_tts_optimization_task
        from crewai import Crew, Task
        
        tts_agent = get_tts_optimizer_agent(crew_manager.llm)
        
        # Create TTS optimization task
        tts_task = Task(
            description=create_tts_optimization_task(
                tts_agent, original_script, language="Spanish", voice_provider="elevenlabs"
            ),
            agent=tts_agent,
            expected_output="TTS-optimized script with markup but same educational content"
        )
        
        # Run optimization
        tts_crew = Crew(
            agents=[tts_agent],
            tasks=[tts_task],
            verbose=True
        )
        
        result = tts_crew.kickoff()
        optimized_script = str(result)
        
        print("✅ TTS optimization completed")
        print(f"📏 Original length: {len(original_script)} characters")
        print(f"📏 Optimized length: {len(optimized_script)} characters")
        
        # Extract core content for comparison
        original_content = extract_core_content(original_script)
        optimized_content = extract_core_content(optimized_script)
        
        print(f"\n📊 Content Analysis:")
        print(f"📝 Original core content length: {len(original_content)} characters")
        print(f"📝 Optimized core content length: {len(optimized_content)} characters")
        
        # Check if core content is preserved
        content_similarity = len(set(original_content.split()) & set(optimized_content.split())) / max(len(set(original_content.split())), len(set(optimized_content.split())))
        
        print(f"🎯 Content similarity: {content_similarity:.2%}")
        
        if content_similarity > 0.85:  # 85% word overlap should indicate preserved content
            print("✅ Content appears to be preserved!")
        else:
            print("❌ Content may have been modified!")
            print("\n🔍 Original core content sample:")
            print(original_content[:200] + "...")
            print("\n🔍 Optimized core content sample:")
            print(optimized_content[:200] + "...")
        
        # Check for TTS markup additions
        has_breaks = '<break' in optimized_script
        has_emphasis = any(word.isupper() and len(word) > 3 for word in optimized_script.split())
        
        print(f"\n🎛️ TTS Markup Analysis:")
        print(f"   Break tags added: {'✅' if has_breaks else '❌'}")
        print(f"   Emphasis added: {'✅' if has_emphasis else '❌'}")
        
        print(f"\n📝 Optimized script preview:")
        print(optimized_script[:500] + "...")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n✨ Test completed!")

if __name__ == "__main__":
    test_tts_content_preservation()