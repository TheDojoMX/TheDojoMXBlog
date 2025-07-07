#!/usr/bin/env python3
"""Generate audio from existing script."""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from voice_papers.voice.synthesizer import get_synthesizer
from voice_papers.config import ELEVENLABS_VOICE_ID


def generate_audio_from_script(script_path: str, output_path: str):
    """Generate audio from an existing script file."""

    script_path = Path(script_path)
    output_path = Path(output_path)

    if not script_path.exists():
        print(f"❌ Script file not found: {script_path}")
        return False

    # Read the script
    print(f"📖 Reading script from: {script_path}")
    with open(script_path, "r", encoding="utf-8") as f:
        script_content = f.read()

    print(f"📄 Script length: {len(script_content)} characters")

    # Generate audio
    print("🎙️  Generating audio with ElevenLabs...")
    try:
        synthesizer = get_synthesizer("elevenlabs")
        success = synthesizer.synthesize(
            script_content,
            output_path,
            ELEVENLABS_VOICE_ID,
            model="flash",
            voice_name="hectorip",
        )

        if success:
            print(f"🎧 Audio generated successfully: {output_path}")
            return True
        else:
            print("❌ Audio generation failed")
            return False

    except Exception as e:
        print(f"❌ Error during audio generation: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_audio.py <script_path> <output_path>")
        print(
            "Example: python generate_audio.py examples/ejemplo_ia_espanol/guion_podcast.txt examples/ejemplo_ia_espanol/audio_espanol.mp3"
        )
        sys.exit(1)

    script_path = sys.argv[1]
    output_path = sys.argv[2]

    success = generate_audio_from_script(script_path, output_path)
    if not success:
        sys.exit(1)
