#!/usr/bin/env python3
"""
Ejemplo de uso de los nuevos parámetros de estabilidad de ElevenLabs
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from voice_papers.voice.synthesizer import get_synthesizer


def main():
    # Texto de prueba
    text = """
    ¡Hola! Este es un ejemplo de síntesis de voz con parámetros de estabilidad mejorados.
    
    Con los nuevos parámetros, ahora puedes controlar:
    - La estabilidad de la voz (consistencia vs. expresividad)
    - La similitud con la voz original
    - El nivel de estilo y expresión
    - El boost del hablante para mayor claridad
    
    Estos parámetros te permiten obtener exactamente la calidad de voz que necesitas 
    para tu proyecto específico.
    """

    # Crear sintetizador
    synthesizer = get_synthesizer("elevenlabs")

    # Directorio de salida
    output_dir = Path("ejemplos_estabilidad")
    output_dir.mkdir(exist_ok=True)

    # Configuraciones de ejemplo
    configuraciones = [
        {
            "nombre": "default",
            "descripcion": "Configuración predeterminada optimizada",
            "params": {},
        },
        {
            "nombre": "muy_estable",
            "descripcion": "Máxima estabilidad para narración profesional",
            "params": {
                "stability": 0.85,
                "similarity_boost": 0.9,
                "style": 0.0,
                "use_speaker_boost": True,
            },
        },
        {
            "nombre": "expresivo",
            "descripcion": "Más expresivo y emocional",
            "params": {
                "stability": 0.35,
                "similarity_boost": 0.7,
                "style": 0.15,
                "use_speaker_boost": True,
            },
        },
        {
            "nombre": "equilibrado",
            "descripcion": "Balance entre estabilidad y expresividad",
            "params": {
                "stability": 0.55,
                "similarity_boost": 0.8,
                "style": 0.05,
                "use_speaker_boost": True,
            },
        },
    ]

    print("🎙️  Generando ejemplos de síntesis con diferentes configuraciones...")
    print("=" * 60)

    for config in configuraciones:
        print(f"\n📝 Generando: {config['nombre']}")
        print(f"   Descripción: {config['descripcion']}")

        # Mostrar parámetros
        if config["params"]:
            print("   Parámetros:")
            for param, value in config["params"].items():
                print(f"   - {param}: {value}")
        else:
            print("   Parámetros: Valores predeterminados")

        # Generar audio
        output_path = output_dir / f"ejemplo_{config['nombre']}.mp3"

        try:
            success = synthesizer.synthesize(
                text=text,
                output_path=output_path,
                voice_name="hectorip",  # Usar tu voz personalizada
                model="flash",
                **config["params"],
            )

            if success:
                print(f"   ✅ Audio generado: {output_path}")
            else:
                print(f"   ❌ Error al generar audio para {config['nombre']}")

        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

    print("\n" + "=" * 60)
    print("🎧 Ejemplos completados!")
    print(f"📁 Archivos guardados en: {output_dir.absolute()}")
    print("\n💡 Consejos de uso:")
    print("- Usa alta estabilidad (0.7-0.9) para narraciones profesionales")
    print("- Usa baja estabilidad (0.3-0.5) para contenido más dramático")
    print("- Mantén el estilo en 0.0 para máxima estabilidad")
    print("- Usa similarity_boost alto (0.8-1.0) para mejor fidelidad")
    print("- Siempre habilita speaker_boost para mayor claridad")


if __name__ == "__main__":
    main()
