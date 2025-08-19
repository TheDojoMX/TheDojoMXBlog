#!/usr/bin/env python3
"""
Script de prueba para analizar transcripción y generar clips sugeridos
"""

import os
import json
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def analyze_transcript_for_clips():
    """Analiza la transcripción existente para identificar clips"""

    # Configurar OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Leer transcripción
    transcript_file = Path(
        "transcripciones/Fundamentos técnicos esenciales para desarrolladores_transcript.txt"
    )

    if not transcript_file.exists():
        print("❌ No se encontró archivo de transcripción")
        return

    with open(transcript_file, "r", encoding="utf-8") as f:
        transcript = f.read()

    print(f"📝 Transcripción cargada: {len(transcript)} caracteres")

    # Prompt para análisis
    prompt = f"""Analiza la siguiente transcripción de un video educativo/técnico de aproximadamente 211 segundos y identifica entre 5-7 momentos interesantes para crear clips cortos.

CRITERIOS para cada clip:
- Duración ideal: 45 segundos (±15 segundos)
- Debe ser AUTO-CONTENIDO (concepto completo)
- Debe tener un HOOK o ser llamativo
- Debe tener valor educativo/entretenimiento

TRANSCRIPCIÓN:
{transcript}

Responde SOLO en formato JSON válido con esta estructura:
[
  {{
    "titulo": "Descripción corta del clip",
    "inicio_estimado": 0,
    "duracion_estimada": 45,
    "razon": "Por qué es interesante",
    "hook": "Frase o concepto llamativo",
    "tipo": "educativo|consejo|historia|pregunta"
  }}
]

Los tiempos deben distribuirse proporcionalmente a lo largo del video de 211 segundos."""

    try:
        print("\n🤖 Analizando con OpenAI...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        # Obtener respuesta
        content = response.choices[0].message.content
        print("\n📄 Respuesta de OpenAI:")
        print(content)

        # Intentar parsear JSON
        import re

        json_match = re.search(r"\[.*\]", content, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            clips = json.loads(json_str)

            print(f"\n✅ Se identificaron {len(clips)} clips:")
            for i, clip in enumerate(clips, 1):
                print(f"\n📹 Clip {i}:")
                print(f"  Título: {clip['titulo']}")
                print(f"  Inicio: {clip['inicio_estimado']}s")
                print(f"  Duración: {clip['duracion_estimada']}s")
                print(f"  Tipo: {clip['tipo']}")
                print(f"  Hook: {clip['hook']}")
                print(f"  Razón: {clip['razon']}")

            # Guardar resultados
            output_file = "clips_analysis_result.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(clips, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Análisis guardado en: {output_file}")

        else:
            print("❌ No se pudo extraer JSON válido de la respuesta")

    except Exception as e:
        print(f"❌ Error analizando transcripción: {str(e)}")


if __name__ == "__main__":
    analyze_transcript_for_clips()
