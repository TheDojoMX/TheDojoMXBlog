#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de timestamps en video_clipper.py
"""

import os
import json
from pathlib import Path
from video_clipper import VideoClipper


def test_timestamps_functionality():
    """Prueba la funcionalidad de timestamps."""

    print("🧪 Iniciando prueba de funcionalidad de timestamps...\n")

    # Buscar un video de prueba en la carpeta clips_verticales
    clips_dir = Path("clips_verticales")
    test_video = None

    # Buscar archivos de video
    for video_file in clips_dir.rglob("*.mp4"):
        if video_file.exists():
            test_video = video_file
            break

    if not test_video:
        print("❌ No se encontró un video de prueba en clips_verticales/")
        print("💡 Copia un video .mp4 en la carpeta clips_verticales/ para probar")
        return False

    print(f"📹 Usando video de prueba: {test_video}")

    try:
        # Crear instancia del clipper
        clipper = VideoClipper(str(test_video))

        # Test 1: Verificar que se puede obtener duración
        duration = clipper.get_video_duration()
        print(f"⏱️  Duración del video: {duration:.2f} segundos")

        # Test 2: Transcribir con timestamps (solo una pequeña parte para prueba rápida)
        print("\n📝 Transcribiendo con timestamps...")
        transcript = clipper.transcribe_video_with_timestamps()

        if transcript:
            print(f"✅ Transcripción exitosa: {len(transcript)} caracteres")

            # Verificar si tenemos timestamps
            if clipper.transcript_with_timestamps:
                print("✅ Timestamps obtenidos exitosamente")

                # Mostrar información de timestamps
                timestamp_data = clipper.transcript_with_timestamps
                print(f"   - Idioma detectado: {timestamp_data.get('language', 'N/A')}")
                print(
                    f"   - Duración: {timestamp_data.get('duration', 'N/A')} segundos"
                )
                print(
                    f"   - Palabras con timestamps: {len(timestamp_data.get('words', []))}"
                )
                print(f"   - Segmentos: {len(timestamp_data.get('segments', []))}")

                # Test 3: Probar extracción de segmento con timestamps
                if duration > 10:  # Solo si el video es suficientemente largo
                    print("\n🎯 Probando extracción de segmento con timestamps...")
                    segment_start = 2.0  # Empezar en segundo 2
                    segment_duration = min(5.0, duration - 3)  # 5 segundos o menos

                    segment_text = clipper.extract_transcript_segment_with_timestamps(
                        segment_start, segment_duration
                    )

                    if segment_text:
                        print(f"✅ Segmento extraído: {len(segment_text)} caracteres")
                        print(f"   Contenido: {segment_text[:100]}...")
                    else:
                        print("⚠️  No se pudo extraer segmento")

                else:
                    print("⚠️  Video muy corto para probar extracción de segmentos")

            else:
                print("⚠️  No se obtuvieron timestamps, usando método de fallback")
        else:
            print("❌ Error en transcripción")
            return False

        # Test 4: Verificar archivos generados
        print("\n📁 Verificando archivos generados:")
        if clipper.transcript_file.exists():
            print(f"✅ Transcripción de texto: {clipper.transcript_file}")
        if clipper.transcript_json_file.exists():
            print(f"✅ Timestamps JSON: {clipper.transcript_json_file}")

        print("\n🎉 Prueba de timestamps completada exitosamente!")
        return True

    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        return False


if __name__ == "__main__":
    # Verificar configuración
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY no configurado")
        print("💡 Configura tu API key de OpenAI para ejecutar esta prueba")
        exit(1)

    success = test_timestamps_functionality()

    if success:
        print("\n✅ Todas las pruebas pasaron!")
    else:
        print("\n❌ Algunas pruebas fallaron")
