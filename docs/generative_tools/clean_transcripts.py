#!/usr/bin/env python3
"""
Script para limpiar transcripciones existentes y verificar que se guarden correctamente
"""

import os
from pathlib import Path


def clean_transcripts():
    """Limpia transcripciones existentes para probar el guardado correcto."""

    transcripts_dir = Path("transcripciones")

    if not transcripts_dir.exists():
        print("📁 Directorio transcripciones/ no existe")
        return

    print("🧹 Limpiando transcripciones existentes...\n")

    # Mostrar archivos existentes
    existing_files = list(transcripts_dir.glob("*"))
    if existing_files:
        print("📂 Archivos existentes:")
        for file in existing_files:
            size = file.stat().st_size
            print(f"   - {file.name} ({size} bytes)")

        response = input("\n¿Eliminar todos estos archivos? (y/N): ")

        if response.lower() == "y":
            for file in existing_files:
                try:
                    file.unlink()
                    print(f"🗑️ Eliminado: {file.name}")
                except Exception as e:
                    print(f"❌ Error eliminando {file.name}: {e}")

            print("\n✅ Limpieza completada")
            print(
                "💡 Ahora puedes probar la transcripción y verificar que se guarde correctamente"
            )
        else:
            print("🛑 Cancelado por el usuario")
    else:
        print("📂 No hay archivos para limpiar")


def show_transcript_structure():
    """Muestra la estructura esperada de archivos de transcripción."""

    print("\n📋 Estructura esperada de archivos de transcripción:")
    print("""
    📁 transcripciones/
    ├── {nombre_video}_transcript.txt                           ← Texto simple
    └── {nombre_video}_transcript_with_timestamps.json          ← Con timestamps
    
    Ejemplo para video "mi_video.mp4":
    📁 transcripciones/
    ├── mi_video_transcript.txt
    └── mi_video_transcript_with_timestamps.json
    """)


if __name__ == "__main__":
    clean_transcripts()
    show_transcript_structure()
