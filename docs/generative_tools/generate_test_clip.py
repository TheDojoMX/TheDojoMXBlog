#!/usr/bin/env python3
"""
Script para generar un clip de prueba en formato vertical
"""

import os
import json
import subprocess
from pathlib import Path


def generate_test_clip():
    """Genera el primer clip como prueba"""

    # Configuración
    video_path = "/Users/hectorip/Downloads/Fundamentos técnicos esenciales para desarrolladores.mp4"
    clips_dir = Path("clips_verticales/test")
    clips_dir.mkdir(parents=True, exist_ok=True)

    # Leer análisis de clips
    with open("clips_analysis_result.json", "r", encoding="utf-8") as f:
        clips = json.load(f)

    # Tomar el primer clip
    first_clip = clips[0]
    print(f"🎬 Generando clip de prueba: {first_clip['titulo']}")
    print(f"  📍 Inicio: {first_clip['inicio_estimado']}s")
    print(f"  ⏱️  Duración: {first_clip['duracion_estimada']}s")
    print(f"  🎯 Hook: {first_clip['hook']}")

    # Nombres de archivos
    horizontal_clip = clips_dir / "test_clip_horizontal.mp4"
    vertical_clip = clips_dir / "test_clip_vertical.mp4"

    # 1. Extraer segmento horizontal
    print("\n⏂ Extrayendo segmento horizontal...")
    extract_cmd = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-ss",
        str(first_clip["inicio_estimado"]),
        "-t",
        str(first_clip["duracion_estimada"]),
        "-c",
        "copy",
        str(horizontal_clip),
    ]

    result = subprocess.run(extract_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error extrayendo segmento: {result.stderr}")
        return False

    print(f"✅ Segmento horizontal creado: {horizontal_clip}")

    # 2. Convertir a formato vertical (9:16)
    print("\n📱 Convirtiendo a formato vertical...")

    # Comando más simple para conversión vertical
    convert_cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(horizontal_clip),
        "-vf",
        (
            "scale=720:1280:force_original_aspect_ratio=decrease,"
            "pad=720:1280:(ow-iw)/2:(oh-ih)/2:black@0.8"
        ),
        "-c:a",
        "copy",
        "-preset",
        "fast",
        str(vertical_clip),
    ]

    result = subprocess.run(convert_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error convirtiendo a vertical: {result.stderr}")
        return False

    print(f"✅ Clip vertical creado: {vertical_clip}")

    # 3. Limpiar archivo horizontal temporal
    horizontal_clip.unlink()
    print("🗑️  Archivo horizontal temporal eliminado")

    # 4. Verificar resultado
    if vertical_clip.exists():
        size = vertical_clip.stat().st_size
        print(f"\n🎉 ¡Clip generado exitosamente!")
        print(f"📂 Ubicación: {vertical_clip}")
        print(f"📊 Tamaño: {size:,} bytes")
        print(f"🎯 Título: {first_clip['titulo']}")
        print(f"💡 Hook: {first_clip['hook']}")
        return True
    else:
        print("❌ Error: No se pudo crear el clip")
        return False


if __name__ == "__main__":
    generate_test_clip()
