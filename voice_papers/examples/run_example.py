#!/usr/bin/env python3
"""Example script for running Voice Papers with Mexican Spanish."""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from voice_papers.utils.pdf_reader import extract_text_from_pdf
from voice_papers.agents.crew_manager import CrewManager
from voice_papers.voice.synthesizer import get_synthesizer
from voice_papers.config import ELEVENLABS_VOICE_ID


def run_example():
    """Run the Mexican Spanish example."""

    # Read the sample paper
    sample_paper_path = Path(__file__).parent / "sample_paper.txt"

    with open(sample_paper_path, "r", encoding="utf-8") as f:
        paper_content = f.read()

    paper_title = "Inteligencia Artificial y el Futuro de la Computación"
    project_name = "ejemplo_ia_espanol"
    language = "Spanish"

    print(f"🇲🇽 Ejecutando ejemplo en español mexicano")
    print(f"📄 Artículo: {paper_title}")
    print(f"📁 Proyecto: {project_name}")

    try:
        # Create crew manager
        print("🤖 Configurando equipo de IA...")
        crew_manager = CrewManager(
            language=language,
            project_name=project_name,
            pdf_path=sample_paper_path,
            conversation_mode="enhanced",  # Usar el modo mejorado por defecto
            tone="casual",  # Usar tono casual para el ejemplo
        )

        # Create and run crew
        print("💭 Creando equipo de discusión...")
        crew = crew_manager.create_crew_for_paper(paper_content, paper_title)

        print("🗣️  Ejecutando discusión (esto puede tomar varios minutos)...")
        final_script = crew_manager.run_crew_and_save_discussion(crew, paper_title)

        # Save the final script
        script_path = crew_manager.project_dir / "guion_podcast.txt"
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(final_script)

        print(f"📝 Guión del podcast guardado en: {script_path}")

        # Synthesize voice
        print("🎙️  Generando audio...")
        synthesizer = get_synthesizer("elevenlabs")

        audio_path = crew_manager.project_dir / "podcast_espanol.mp3"
        success = synthesizer.synthesize(
            final_script,
            audio_path,
            ELEVENLABS_VOICE_ID,
            model="flash",
            voice_name="hectorip",
        )

        if success:
            print(f"🎧 Audio guardado en: {audio_path}")
        else:
            print("❌ La síntesis de audio falló")

        print(f"✅ ¡Proyecto completado! Revisar: {crew_manager.project_dir}")
        print(f"📁 Archivos de discusión en: {crew_manager.discussion_dir}")

    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    run_example()
