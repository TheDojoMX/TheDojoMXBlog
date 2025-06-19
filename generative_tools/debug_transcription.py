#!/usr/bin/env python3
"""
Script de diagnóstico para identificar problemas en la transcripción
"""

import os
import time
import subprocess
from pathlib import Path
from video_clipper import VideoClipper


def diagnose_transcription_issue():
    """Diagnostica problemas en el proceso de transcripción."""

    print("🔍 Iniciando diagnóstico de transcripción...\n")

    # Verificar configuración básica
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY no configurado")
        return False
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        print(f"✅ OpenAI API Key configurado: {api_key[:8]}...")

    # Buscar video de prueba
    clips_dir = Path("clips_verticales")
    test_video = None

    for video_file in clips_dir.rglob("*.mp4"):
        if video_file.exists():
            test_video = video_file
            break

    if not test_video:
        print("❌ No se encontró un video de prueba en clips_verticales/")
        print(
            "💡 Copia un video .mp4 en la carpeta clips_verticales/ para diagnosticar"
        )
        return False

    print(f"📹 Video de prueba: {test_video}")

    # Verificar duración del video
    try:
        cmd = [
            "ffprobe",
            "-v",
            "quiet",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            str(test_video),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        duration = float(result.stdout.strip())
        print(f"⏱️  Duración del video: {duration:.2f} segundos")

        if duration > 600:  # 10 minutos
            print("⚠️ Video muy largo - esto puede causar problemas de timeout")

    except Exception as e:
        print(f"❌ Error obteniendo duración: {str(e)}")
        return False

    # Probar extracción de audio
    print("\n🎵 Probando extracción de audio...")
    try:
        from video_transcriber import extract_audio_from_video

        start_time = time.time()
        audio_path = extract_audio_from_video(str(test_video))
        audio_extraction_time = time.time() - start_time

        print(f"✅ Audio extraído en {audio_extraction_time:.2f} segundos")
        print(f"📁 Archivo de audio: {audio_path}")

        # Verificar tamaño del audio
        audio_size = os.path.getsize(audio_path)
        print(f"📊 Tamaño del audio: {audio_size / (1024*1024):.2f} MB")

        # Límite de Whisper
        if audio_size > 25 * 1024 * 1024:
            print("⚠️ Archivo de audio muy grande para Whisper (>25MB)")
            print("💡 El sistema debería usar transcripción por segmentos")

        # Limpiar archivo temporal
        if os.path.exists(audio_path):
            os.remove(audio_path)
            print("🗑️ Archivo temporal limpiado")

    except Exception as e:
        print(f"❌ Error en extracción de audio: {str(e)}")
        return False

    # Probar conexión con OpenAI (transcripción simple)
    print("\n🎙️ Probando conexión con OpenAI Whisper...")
    try:
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Crear un archivo de audio muy pequeño para probar
        print("📝 Creando archivo de audio de prueba pequeño...")

        # Extraer solo 5 segundos del video
        test_audio = "test_audio_5sec.wav"
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(test_video),
            "-t",
            "5",  # Solo 5 segundos
            "-vn",  # Sin video
            "-acodec",
            "pcm_s16le",
            "-ar",
            "16000",  # Sample rate más bajo
            "-ac",
            "1",  # Mono
            test_audio,
        ]

        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            print(f"❌ Error creando audio de prueba: {result.stderr}")
            return False

        audio_creation_time = time.time() - start_time
        print(f"✅ Audio de prueba creado en {audio_creation_time:.2f} segundos")

        # Verificar tamaño
        test_size = os.path.getsize(test_audio)
        print(f"📊 Tamaño del audio de prueba: {test_size / 1024:.2f} KB")

        # Intentar transcripción simple
        print("🤖 Probando transcripción simple con OpenAI...")
        start_time = time.time()

        with open(test_audio, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="es",
                response_format="text",
            )

        transcription_time = time.time() - start_time
        print(f"✅ Transcripción completada en {transcription_time:.2f} segundos")
        print(f"📝 Resultado ({len(response)} caracteres): {response[:100]}...")

        # Limpiar archivo de prueba
        os.remove(test_audio)
        print("🗑️ Archivo de prueba limpiado")

    except Exception as e:
        print(f"❌ Error en transcripción de prueba: {str(e)}")
        return False

    # Probar transcripción con timestamps
    print("\n🕐 Probando transcripción con timestamps...")
    try:
        # Crear audio aún más pequeño
        tiny_audio = "tiny_test_audio.wav"
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(test_video),
            "-t",
            "3",  # Solo 3 segundos
            "-vn",
            "-acodec",
            "pcm_s16le",
            "-ar",
            "16000",
            "-ac",
            "1",
            tiny_audio,
        ]

        subprocess.run(cmd, capture_output=True, text=True, timeout=15)

        start_time = time.time()
        with open(tiny_audio, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="es",
                response_format="verbose_json",
                timestamp_granularities=["word"],
            )

        timestamp_time = time.time() - start_time
        print(
            f"✅ Transcripción con timestamps completada en {timestamp_time:.2f} segundos"
        )

        if hasattr(response, "words") and response.words:
            print(f"📊 Palabras con timestamps: {len(response.words)}")
        else:
            print("⚠️ No se obtuvieron timestamps por palabra")

        # Limpiar
        os.remove(tiny_audio)

    except Exception as e:
        print(f"❌ Error en transcripción con timestamps: {str(e)}")
        print("💡 Posible causa: timestamp_granularities no soportado en tu cuenta")

    print("\n🎉 Diagnóstico completado!")
    print("\n💡 Recomendaciones:")
    print(
        "- Si la extracción de audio es lenta, el problema puede ser el tamaño del video"
    )
    print("- Si la transcripción simple falla, verifica tu API key de OpenAI")
    print(
        "- Si solo falla con timestamps, tu cuenta podría no tener acceso a esa funcionalidad"
    )
    print("- Videos >10 minutos pueden causar timeouts")

    return True


if __name__ == "__main__":
    diagnose_transcription_issue()
