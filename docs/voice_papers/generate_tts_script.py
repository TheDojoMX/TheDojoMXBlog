#!/usr/bin/env python3
"""
Script CLI para generar versiones TTS optimizadas de scripts educativos.

Este script toma un script educativo existente y genera una versión optimizada
para Text-to-Speech con etiquetas de pausa, markdown para énfasis y mejor ritmo.
"""

import click
import sys
from pathlib import Path

# Añadir el directorio voice_papers al path
sys.path.append(str(Path(__file__).parent / "voice_papers"))

from voice_papers.utils.tts_script_generator import (
    generate_tts_script_for_project,
    batch_generate_tts_scripts,
    compare_scripts,
    generate_tts_script,
)


@click.group()
def cli():
    """Generador de scripts TTS optimizados para Voice Papers."""
    pass


@cli.command()
@click.argument("script_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    help="Ruta de salida para el script TTS optimizado",
)
@click.option(
    "--language", "-l", default="Spanish", help="Idioma del script (default: Spanish)"
)
@click.option(
    "--voice-provider",
    "-v",
    default="elevenlabs",
    type=click.Choice(["elevenlabs", "cartesia"]),
    help="Proveedor de TTS a optimizar (default: elevenlabs)",
)
@click.option(
    "--compare",
    "-c",
    is_flag=True,
    help="Mostrar comparación entre el script original y el optimizado",
)
def optimize(script_path, output, language, voice_provider, compare):
    """
    Optimiza un script educativo individual para TTS.

    SCRIPT_PATH: Ruta al script educativo original (.txt)
    """
    click.echo(f"🎤 Optimizando script para {voice_provider} TTS...")

    # Generar ruta de salida si no se especifica
    if not output:
        output = script_path.parent / f"{script_path.stem}_tts_{voice_provider}.txt"

    try:
        # Generar script optimizado
        optimized_script = generate_tts_script(
            educational_script_path=script_path,
            output_path=output,
            language=language,
            voice_provider=voice_provider,
        )

        click.echo(f"✅ Script TTS optimizado generado exitosamente!")
        click.echo(f"📍 Ubicación: {output}")

        # Mostrar comparación si se solicita
        if compare:
            compare_scripts(script_path, output)

    except Exception as e:
        click.echo(f"❌ Error al optimizar el script: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("project_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--voice-provider",
    "-v",
    default="elevenlabs",
    type=click.Choice(["elevenlabs", "cartesia"]),
    help="Proveedor de TTS a optimizar (default: elevenlabs)",
)
@click.option(
    "--language", "-l", default="Spanish", help="Idioma del script (default: Spanish)"
)
@click.option(
    "--compare",
    "-c",
    is_flag=True,
    help="Mostrar comparación entre el script original y el optimizado",
)
def project(project_path, voice_provider, language, compare):
    """
    Optimiza el script educativo de un proyecto específico.

    PROJECT_PATH: Ruta al directorio del proyecto que contiene educational_script.txt
    """
    click.echo(f"📁 Procesando proyecto: {project_path.name}")

    # Generar script TTS para el proyecto
    tts_script_path = generate_tts_script_for_project(
        project_path=project_path, voice_provider=voice_provider, language=language
    )

    if tts_script_path:
        click.echo(f"✅ Script TTS generado exitosamente!")

        # Mostrar comparación si se solicita
        if compare:
            original_path = project_path / "educational_script.txt"
            compare_scripts(original_path, tts_script_path)
    else:
        click.echo(f"❌ No se pudo generar el script TTS", err=True)
        sys.exit(1)


@cli.command()
@click.argument("projects_dir", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--voice-provider",
    "-v",
    default="elevenlabs",
    type=click.Choice(["elevenlabs", "cartesia"]),
    help="Proveedor de TTS a optimizar (default: elevenlabs)",
)
@click.option(
    "--language",
    "-l",
    default="Spanish",
    help="Idioma de los scripts (default: Spanish)",
)
def batch(projects_dir, voice_provider, language):
    """
    Optimiza scripts educativos para todos los proyectos en un directorio.

    PROJECTS_DIR: Directorio que contiene múltiples proyectos
    """
    click.echo(f"🔄 Procesando todos los proyectos en: {projects_dir}")

    # Procesar todos los proyectos
    batch_generate_tts_scripts(
        projects_dir=projects_dir, voice_provider=voice_provider, language=language
    )


@cli.command()
@click.argument("original_path", type=click.Path(exists=True, path_type=Path))
@click.argument("tts_path", type=click.Path(exists=True, path_type=Path))
def compare_cmd(original_path, tts_path):
    """
    Compara un script original con su versión TTS optimizada.

    ORIGINAL_PATH: Ruta al script original
    TTS_PATH: Ruta al script TTS optimizado
    """
    click.echo("📊 Comparando scripts...")
    compare_scripts(original_path, tts_path)


@cli.command()
def demo():
    """
    Muestra un ejemplo de cómo se ve un script optimizado para TTS.
    """
    click.echo("🎤 EJEMPLO DE OPTIMIZACIÓN TTS")
    click.echo("=" * 50)

    original_text = """
    La inteligencia artificial es una tecnología fascinante que está transformando nuestro mundo. 
    Los algoritmos de machine learning pueden procesar grandes cantidades de datos para encontrar patrones complejos. 
    Esto tiene implicaciones importantes para el futuro de la humanidad.
    """

    optimized_text = """
    La **inteligencia artificial** es una tecnología que está ***transformando completamente*** nuestro mundo. <break time="1s"/>
    
    Los algoritmos de *machine learning* pueden procesar grandes cantidades de *datos*... <break time="0.5s"/> 
    y es que encuentran patrones complejos que nosotros no podríamos ver. <break time="1s"/>
    
    Esto tiene **implicaciones importantes** para el futuro de la humanidad... <break time="1.5s"/>
    Y aquí viene lo interesante...
    """

    click.echo("📝 TEXTO ORIGINAL:")
    click.echo(original_text.strip())

    click.echo("\n🎤 TEXTO OPTIMIZADO PARA TTS:")
    click.echo(optimized_text.strip())

    click.echo("\n🎯 CARACTERÍSTICAS AÑADIDAS:")
    click.echo("• **Negrita** para énfasis fuerte")
    click.echo("• *Cursiva* para énfasis suave")
    click.echo('• <break time="Xs"/> para pausas estratégicas')
    click.echo("• ... para pausas naturales")
    click.echo("• Conectores conversacionales")
    click.echo("• Párrafos más cortos")
    click.echo("• Frases de transición atractivas")


if __name__ == "__main__":
    cli()
