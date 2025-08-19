"""Utility for generating TTS-optimized scripts from educational scripts."""

import os
from pathlib import Path
from typing import Optional

from crewai import Task, Crew
from langchain_openai import ChatOpenAI

from ..agents.tts_optimizer import get_tts_optimizer_agent, create_tts_optimization_task
from ..config import OPENAI_API_KEY, MODEL_NAME


def generate_tts_script(
    educational_script_path: Path,
    output_path: Optional[Path] = None,
    language: str = "Spanish",
    voice_provider: str = "elevenlabs",
    model_name: str = MODEL_NAME,
) -> str:
    """
    Generate a TTS-optimized version of an educational script.

    Args:
        educational_script_path: Path to the original educational script
        output_path: Path where to save the TTS-optimized script (optional)
        language: Language of the script (default: Spanish)
        voice_provider: TTS provider to optimize for (default: elevenlabs)
        model_name: LLM model to use for optimization

    Returns:
        The TTS-optimized script as a string
    """
    # Verify input file exists
    if not educational_script_path.exists():
        raise FileNotFoundError(
            f"Educational script not found: {educational_script_path}"
        )

    # Read the original script
    with open(educational_script_path, "r", encoding="utf-8") as f:
        original_script = f.read()

    # Initialize LLM
    llm = ChatOpenAI(model=model_name, temperature=0.1, api_key=OPENAI_API_KEY)

    # Create TTS optimizer agent
    tts_agent = get_tts_optimizer_agent(llm)

    # Create optimization task
    task_description = create_tts_optimization_task(
        agent=tts_agent,
        educational_script=original_script,
        language=language,
        voice_provider=voice_provider,
    )

    # Create and execute the task
    optimization_task = Task(
        description=task_description,
        agent=tts_agent,
        expected_output=f"TTS-optimized script with markdown emphasis, break tags, and natural speech patterns for {voice_provider}",
    )

    # Create crew with single agent
    crew = Crew(agents=[tts_agent], tasks=[optimization_task], verbose=True)

    # Execute the optimization
    print(f"🎤 Optimizing script for {voice_provider} TTS...")
    result = crew.kickoff()

    # Extract the optimized script
    optimized_script = result.raw if hasattr(result, "raw") else str(result)

    # Save to output path if specified
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(optimized_script)
        print(f"📝 TTS-optimized script saved to: {output_path}")

    return optimized_script


def generate_tts_script_for_project(
    project_path: Path, voice_provider: str = "elevenlabs", language: str = "Spanish"
) -> Optional[Path]:
    """
    Generate TTS-optimized script for an existing project.

    Args:
        project_path: Path to the project directory
        voice_provider: TTS provider to optimize for
        language: Language of the script

    Returns:
        Path to the generated TTS script, or None if original script not found
    """
    # Look for educational script
    educational_script_path = project_path / "educational_script.txt"

    if not educational_script_path.exists():
        print(f"❌ No educational script found in {project_path}")
        return None

    # Generate output path
    tts_script_path = project_path / f"educational_script_tts_{voice_provider}.txt"

    try:
        # Generate TTS-optimized script
        optimized_script = generate_tts_script(
            educational_script_path=educational_script_path,
            output_path=tts_script_path,
            language=language,
            voice_provider=voice_provider,
        )

        print(f"✅ TTS-optimized script generated successfully!")
        print(f"📍 Location: {tts_script_path}")

        return tts_script_path

    except Exception as e:
        print(f"❌ Error generating TTS script: {e}")
        return None


def batch_generate_tts_scripts(
    projects_dir: Path, voice_provider: str = "elevenlabs", language: str = "Spanish"
) -> None:
    """
    Generate TTS-optimized scripts for all projects in a directory.

    Args:
        projects_dir: Directory containing project folders
        voice_provider: TTS provider to optimize for
        language: Language of the scripts
    """
    if not projects_dir.exists():
        print(f"❌ Projects directory not found: {projects_dir}")
        return

    # Find all project directories
    project_dirs = [d for d in projects_dir.iterdir() if d.is_dir()]

    if not project_dirs:
        print(f"❌ No project directories found in {projects_dir}")
        return

    print(f"🔄 Processing {len(project_dirs)} projects...")

    success_count = 0
    for project_dir in project_dirs:
        print(f"\n📁 Processing project: {project_dir.name}")

        result = generate_tts_script_for_project(
            project_path=project_dir, voice_provider=voice_provider, language=language
        )

        if result:
            success_count += 1

    print(f"\n✅ Batch processing complete!")
    print(f"📊 Successfully processed {success_count}/{len(project_dirs)} projects")


def compare_scripts(original_path: Path, tts_path: Path) -> None:
    """
    Compare original and TTS-optimized scripts and show differences.

    Args:
        original_path: Path to original script
        tts_path: Path to TTS-optimized script
    """
    if not original_path.exists():
        print(f"❌ Original script not found: {original_path}")
        return

    if not tts_path.exists():
        print(f"❌ TTS script not found: {tts_path}")
        return

    # Read both scripts
    with open(original_path, "r", encoding="utf-8") as f:
        original = f.read()

    with open(tts_path, "r", encoding="utf-8") as f:
        tts_optimized = f.read()

    # Basic comparison stats
    original_words = len(original.split())
    tts_words = len(tts_optimized.split())

    original_paragraphs = len([p for p in original.split("\n\n") if p.strip()])
    tts_paragraphs = len([p for p in tts_optimized.split("\n\n") if p.strip()])

    # Count TTS-specific elements
    break_count = tts_optimized.count("<break time=")
    bold_count = tts_optimized.count("**")
    italic_count = tts_optimized.count("*") - bold_count * 2
    ellipsis_count = tts_optimized.count("...")

    print(f"\n📊 SCRIPT COMPARISON REPORT")
    print(f"{'='*50}")
    print(f"Original script:")
    print(f"  📝 Words: {original_words}")
    print(f"  📄 Paragraphs: {original_paragraphs}")
    print(f"\nTTS-optimized script:")
    print(f"  📝 Words: {tts_words}")
    print(f"  📄 Paragraphs: {tts_paragraphs}")
    print(f"  ⏸️  Break tags: {break_count}")
    print(f"  🔊 Bold emphasis: {bold_count // 2}")
    print(f"  💬 Italic emphasis: {italic_count // 2}")
    print(f"  ⏱️  Ellipsis pauses: {ellipsis_count}")

    # Show word count change
    word_diff = tts_words - original_words
    if word_diff > 0:
        print(f"  📈 Word count increased by {word_diff}")
    elif word_diff < 0:
        print(f"  📉 Word count decreased by {abs(word_diff)}")
    else:
        print(f"  📊 Word count unchanged")

    print(f"\n🎯 TTS OPTIMIZATION FEATURES ADDED:")
    print(f"  • Strategic pauses for natural speech rhythm")
    print(f"  • Emphasis markers for vocal stress")
    print(f"  • Shorter paragraphs for better TTS processing")
    print(f"  • Natural conversational connectors")
    print(f"  • Technical term emphasis")
