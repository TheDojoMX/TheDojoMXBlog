#!/usr/bin/env python3
"""Test script for improved audio generation with chunking."""

import subprocess
import sys
from pathlib import Path
import json


def create_long_test_script():
    """Create a test script that would generate ~15 minutes of audio."""
    
    # Approximate: 150 words/minute, 5 chars/word = 750 chars/minute
    # 15 minutes = ~11,250 characters minimum
    # Let's create ~50,000 characters to ensure multiple chunks
    
    test_content = """# La Inteligencia Artificial y el Futuro de la Humanidad

Bienvenidos a este episodio educativo donde exploraremos uno de los temas más fascinantes y 
transformadores de nuestro tiempo: la inteligencia artificial y su impacto en el futuro de 
la humanidad.

## Introducción: ¿Qué es la Inteligencia Artificial?

La inteligencia artificial, o IA, es una rama de la informática que busca crear sistemas 
capaces de realizar tareas que típicamente requieren inteligencia humana. Pero, ¿qué 
significa esto realmente? Imagina una máquina que puede aprender de la experiencia, 
adaptarse a nuevas situaciones, y resolver problemas complejos sin ser programada 
explícitamente para cada tarea específica.

"""
    
    # Add more content to reach ~50,000 characters
    sections = [
        "## Historia y Evolución de la IA\n\nLa historia de la inteligencia artificial se remonta a la década de 1950, cuando pioneros como Alan Turing comenzaron a plantear preguntas fundamentales sobre si las máquinas podían pensar. Turing propuso su famoso test, conocido como el Test de Turing, que evalúa la capacidad de una máquina para exhibir comportamiento inteligente indistinguible del de un ser humano.\n\n",
        
        "## Los Fundamentos del Aprendizaje Automático\n\nEl aprendizaje automático es el corazón de la IA moderna. A diferencia de la programación tradicional, donde escribimos reglas explícitas para cada situación, el aprendizaje automático permite a las computadoras aprender patrones de los datos. Es como enseñar a un niño: en lugar de darle una lista interminable de reglas, le mostramos ejemplos y el niño aprende a generalizar.\n\n",
        
        "## Redes Neuronales y Deep Learning\n\nLas redes neuronales artificiales están inspiradas en el funcionamiento del cerebro humano. Imagina miles de neuronas artificiales conectadas entre sí, cada una procesando información y pasándola a las siguientes. Cuando estas redes tienen muchas capas, hablamos de aprendizaje profundo o deep learning.\n\n",
        
        "## Aplicaciones Transformadoras en la Medicina\n\nUno de los campos donde la IA está teniendo un impacto más profundo es la medicina. Los sistemas de IA pueden analizar imágenes médicas con una precisión que rivaliza o supera a la de los especialistas humanos. Por ejemplo, en la detección del cáncer de mama, algunos sistemas de IA han demostrado una precisión del 95%, reduciendo significativamente los falsos positivos y negativos.\n\n",
        
        "## La IA en la Vida Cotidiana\n\nAunque no siempre somos conscientes de ello, la inteligencia artificial ya está profundamente integrada en nuestra vida diaria. Desde los asistentes virtuales en nuestros teléfonos hasta los sistemas de recomendación en plataformas de streaming, la IA moldea nuestras experiencias digitales de maneras sutiles pero poderosas.\n\n",
        
        "## Desafíos Éticos y Sociales\n\nCon gran poder viene gran responsabilidad. La IA plantea importantes desafíos éticos que debemos abordar como sociedad. ¿Cómo garantizamos que los sistemas de IA sean justos y no perpetúen sesgos existentes? ¿Quién es responsable cuando una IA toma una decisión incorrecta? Estas preguntas no tienen respuestas fáciles.\n\n",
        
        "## El Impacto en el Mercado Laboral\n\nUna de las preocupaciones más comunes sobre la IA es su impacto en el empleo. Si bien es cierto que la automatización puede desplazar ciertos trabajos, la historia nos muestra que la tecnología también crea nuevas oportunidades. La clave está en la adaptación y el aprendizaje continuo.\n\n",
        
        "## IA y Creatividad: ¿Pueden las Máquinas ser Creativas?\n\nUna pregunta fascinante es si la IA puede ser verdaderamente creativa. Hemos visto sistemas de IA generar música, arte visual, poesía e incluso guiones de películas. Pero, ¿es esto verdadera creatividad o simplemente una sofisticada recombinación de patrones existentes?\n\n",
        
        "## El Futuro de la IA: Hacia la Inteligencia General Artificial\n\nActualmente, la mayoría de los sistemas de IA son especializados: excelentes en una tarea específica pero incapaces de transferir ese conocimiento a otros dominios. El santo grial de la investigación en IA es la Inteligencia General Artificial (AGI), sistemas que puedan igualar o superar la inteligencia humana en todos los aspectos.\n\n",
        
        "## Preparándonos para el Futuro\n\nComo individuos y como sociedad, debemos prepararnos para un futuro donde la IA será aún más prevalente. Esto significa no solo desarrollar habilidades técnicas, sino también fortalecer aquellas capacidades únicamente humanas: la empatía, la creatividad, el pensamiento crítico y la colaboración.\n\n"
    ]
    
    # Repeat content to reach target length
    full_content = test_content
    for _ in range(6):  # This should give us ~50,000+ characters
        for section in sections:
            full_content += section
            full_content += "Profundicemos más en este tema. " * 20 + "\n\n"
    
    # Add conclusion
    full_content += """
## Conclusión: Abraza el Cambio, Moldea el Futuro

La inteligencia artificial no es solo una tecnología del futuro; es una realidad del presente 
que está transformando nuestro mundo de maneras profundas y aceleradas. Como hemos visto a lo 
largo de este episodio, la IA tiene el potencial de resolver algunos de los desafíos más 
grandes de la humanidad, desde el cambio climático hasta las enfermedades incurables.

Sin embargo, este poder conlleva responsabilidades significativas. Debemos asegurarnos de que 
el desarrollo de la IA se guíe por principios éticos sólidos, que beneficie a toda la 
humanidad y no solo a unos pocos, y que respete los valores fundamentales que nos definen 
como seres humanos.

El futuro con IA no es algo que simplemente nos sucederá; es algo que estamos creando 
activamente con cada decisión que tomamos hoy. Ya seas un estudiante, un profesional, un 
emprendedor o simplemente una persona curiosa sobre el mundo, tienes un papel que desempeñar 
en la configuración de este futuro.

La pregunta no es si la IA transformará nuestro mundo - eso ya está sucediendo. La pregunta 
es: ¿cómo participarás tú en esta transformación? ¿Qué problemas te gustaría ver resueltos? 
¿Qué valores quieres que se reflejen en los sistemas de IA del mañana?

Te invito a continuar explorando, aprendiendo y, lo más importante, participando activamente 
en las conversaciones sobre el futuro de la IA. Porque al final del día, la inteligencia 
artificial es una herramienta creada por humanos, para humanos, y su éxito dependerá de 
nuestra sabiduría colectiva para usarla bien.

Gracias por acompañarme en este viaje educativo. Hasta la próxima, sigue aprendiendo, 
sigue cuestionando, y sigue soñando con un futuro mejor para todos.
"""
    
    return full_content


def test_improved_audio_generation():
    """Test the improved audio generation with a long script."""
    
    print("🧪 Testing Improved Audio Generation")
    print("=" * 60)
    
    # Create test script
    print("\n📝 Creating long test script...")
    test_script = create_long_test_script()
    test_file = Path("test_long_script.txt")
    
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_script)
    
    char_count = len(test_script)
    estimated_minutes = char_count / (150 * 5)  # 150 words/min * 5 chars/word
    
    print(f"✅ Created test script:")
    print(f"   - Characters: {char_count:,}")
    print(f"   - Estimated audio duration: {estimated_minutes:.1f} minutes")
    print(f"   - Expected chunks: {int(estimated_minutes / 5)} chunks")
    
    # Test 1: Generate with improved mode
    print("\n📋 Test 1: Improved audio generation")
    cmd = [
        "voice-papers",
        str(test_file),
        "--direct",
        "--project-name", "test_improved_audio",
        "--language", "Spanish",  
        "--voice", "ana",
        "--model", "flash",
        "--duration", str(int(estimated_minutes)),
        "--script-only"  # For testing, only generate script
    ]
    
    print(f"Running: {' '.join(cmd)}")
    print("\nNOTE: Using --script-only for testing. Remove this flag to test actual audio generation.")
    print("NOTE: Audio generation will take several minutes and incur API costs.\n")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Script generation completed successfully")
        
        # Check if state directory would be created
        state_dir = Path("test_improved_audio/.educational_lecture_state")
        if state_dir.exists():
            print(f"\n📁 State directory created: {state_dir}")
            
            # List state files
            for file in state_dir.rglob("*"):
                if file.is_file():
                    print(f"   - {file.relative_to(state_dir)}")
        
        print("\n💡 To test actual audio generation:")
        print("   1. Remove --script-only from the command")
        print("   2. Be aware this will incur ElevenLabs API costs")
        print("   3. Monitor the .state directory for progress")
        
    else:
        print(f"❌ Command failed: {result.stderr}")
    
    # Clean up
    if test_file.exists():
        test_file.unlink()
    
    print("\n" + "=" * 60)
    print("✅ Test script completed")
    print("\n📊 Expected behavior with actual audio generation:")
    print("   1. Script will be split into ~5-6 minute chunks")
    print("   2. Each chunk will be generated separately")
    print("   3. Progress will be saved after each chunk")
    print("   4. Cost report will be generated")
    print("   5. Audio chunks will be stitched together")


if __name__ == "__main__":
    test_improved_audio_generation()