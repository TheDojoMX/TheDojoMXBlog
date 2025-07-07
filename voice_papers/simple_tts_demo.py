#!/usr/bin/env python3
"""
Demostración simple del optimizador TTS sin usar CrewAI
"""

import sys
from pathlib import Path


# Función simplificada de optimización TTS
def optimize_for_tts(text: str) -> str:
    """Optimiza un texto para TTS con negritas, cursivas y pausas."""

    # Dividir en párrafos
    paragraphs = text.split("\n\n")
    optimized_paragraphs = []

    for paragraph in paragraphs:
        if not paragraph.strip():
            continue

        # Dividir en oraciones
        sentences = []
        current_sentences = paragraph.split(". ")

        for i, sentence in enumerate(current_sentences):
            if not sentence.strip():
                continue

            # Agregar punto si no lo tiene
            if (
                not sentence.endswith(".")
                and not sentence.endswith("!")
                and not sentence.endswith("?")
            ):
                sentence += "."

            # Optimizar términos técnicos
            sentence = enhance_technical_terms(sentence)

            # Agregar conectores conversacionales
            sentence = add_conversational_connectors(sentence, i)

            # Agregar pausas estratégicas
            sentence = add_strategic_pauses(sentence, i, len(current_sentences))

            sentences.append(sentence)

        # Unir oraciones con espacios
        optimized_paragraph = " ".join(sentences)
        optimized_paragraphs.append(optimized_paragraph)

    return "\n\n".join(optimized_paragraphs)


def enhance_technical_terms(sentence: str) -> str:
    """Mejora términos técnicos con énfasis."""
    technical_terms = {
        "inteligencia artificial": "**inteligencia artificial**",
        "machine learning": "*machine learning*",
        "algoritmos": "*algoritmos*",
        "benchmark": "*benchmark*",
        "checkpoints": "**checkpoints**",
        "automatización": "**automatización**",
        "agentes": "*agentes*",
        "modelos de lenguaje": "*modelos de lenguaje*",
        "entorno simulado": "*entorno simulado*",
        "fallback": "**fallback**",
        "API cerradas": "*API cerradas*",
        "open weights": "**open weights**",
    }

    for term, replacement in technical_terms.items():
        if term in sentence.lower() and replacement not in sentence:
            # Buscar la versión exacta en el texto original
            words = sentence.split()
            for i, word in enumerate(words):
                if term.split()[0].lower() in word.lower():
                    # Intentar reemplazar el término completo
                    original_text = sentence
                    # Usar reemplazo case-insensitive
                    import re

                    sentence = re.sub(
                        re.escape(term),
                        replacement,
                        sentence,
                        flags=re.IGNORECASE,
                        count=1,
                    )
                    break

    return sentence


def add_conversational_connectors(sentence: str, position: int) -> str:
    """Añade conectores conversacionales naturales."""
    if position == 0:
        # Primera oración del párrafo
        if "Imagina" in sentence:
            return sentence.replace("Imagina", "Imagina por un momento")
        elif "En este" in sentence:
            return sentence.replace("En este", "Y es que en este")

    # Añadir conectores ocasionales
    if "Por ejemplo" in sentence:
        sentence = sentence.replace(
            "Por ejemplo,", 'Por ejemplo... <break time="0.5s"/>'
        )

    if "Es decir" in sentence:
        sentence = sentence.replace("Es decir,", 'Es decir... <break time="0.5s"/>')

    return sentence


def add_strategic_pauses(sentence: str, position: int, total: int) -> str:
    """Añade pausas estratégicas para mejor ritmo."""

    # Pausas después de preguntas
    if sentence.strip().endswith("?"):
        sentence = sentence.rstrip() + ' <break time="1s"/>'

    # Pausas antes de revelaciones importantes
    if any(
        keyword in sentence.lower()
        for keyword in ["resulta que", "sin embargo", "no obstante", "pero"]
    ):
        sentence = '<break time="0.5s"/> ' + sentence

    # Pausa larga al final de conceptos importantes
    if any(
        keyword in sentence.lower()
        for keyword in ["limitaciones", "desafíos", "soluciones"]
    ):
        sentence = sentence.rstrip() + ' <break time="1s"/>'

    # Añadir elipsis para ritmo natural
    if "que" in sentence and len(sentence.split()) > 15:
        sentence = sentence.replace(" que ", "... que ")

    return sentence


def create_tts_demo():
    """Crea una demostración del optimizador TTS."""

    # Leer el script original
    script_path = Path("projects/agent_company/agent_company/educational_script.txt")

    if not script_path.exists():
        print(f"❌ No se encontró el script en: {script_path}")
        return

    print("🎤 DEMOSTRACIÓN TTS OPTIMIZER")
    print("=" * 50)

    with open(script_path, "r", encoding="utf-8") as f:
        original_text = f.read()

    # Tomar solo los primeros 3 párrafos para la demo
    paragraphs = [p for p in original_text.split("\n\n") if p.strip()]
    sample_text = "\n\n".join(paragraphs[:3])

    print("\n📝 TEXTO ORIGINAL (muestra):")
    print("-" * 30)
    print(sample_text[:500] + "...")

    # Optimizar para TTS
    optimized_text = optimize_for_tts(sample_text)

    print("\n🎤 TEXTO OPTIMIZADO PARA TTS:")
    print("-" * 30)
    print(optimized_text)

    # Guardar versión completa optimizada
    full_optimized = optimize_for_tts(original_text)
    output_path = script_path.parent / "educational_script_tts_demo.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_optimized)

    print(f"\n✅ Script completo optimizado guardado en:")
    print(f"📍 {output_path}")

    # Estadísticas
    original_words = len(original_text.split())
    optimized_words = len(full_optimized.split())
    break_count = full_optimized.count("<break time=")
    bold_count = full_optimized.count("**") // 2
    italic_count = (full_optimized.count("*") - bold_count * 4) // 2

    print(f"\n📊 ESTADÍSTICAS DE OPTIMIZACIÓN:")
    print(f"📝 Palabras originales: {original_words}")
    print(f"📝 Palabras optimizadas: {optimized_words}")
    print(f"⏸️  Pausas añadidas: {break_count}")
    print(f"🔊 Términos en negrita: {bold_count}")
    print(f"💬 Términos en cursiva: {italic_count}")

    print(f"\n🎯 CARACTERÍSTICAS AÑADIDAS:")
    print(f"• Énfasis con **negrita** e *cursiva*")
    print(f'• Pausas estratégicas <break time="Xs"/>')
    print(f"• Conectores conversacionales naturales")
    print(f"• Optimización de términos técnicos")
    print(f"• Mejor ritmo para síntesis de voz")


if __name__ == "__main__":
    create_tts_demo()
