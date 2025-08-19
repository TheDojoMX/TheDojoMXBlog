# Voice Papers

Generate educational audio lectures from documents (PDF, Markdown, Text) and web articles using AI agents and voice synthesis.

## Overview

Voice Papers transforms various document formats **and web articles** into engaging educational content by:
1. **NEW:** Extracting content from PDF files, Markdown documents (.md), Text files (.txt), and web article URLs
2. Using CrewAI to create dynamic teams of AI agents that analyze content from different perspectives
3. Generating educational lecture scripts in the style of popular science educators (like 3Blue1Brown)
4. Converting scripts to audio using ElevenLabs or Cartesia voice synthesis
5. Creating animated videos with waveform visualizations in both vertical and horizontal formats

## Features

- **Multiple Input Formats**: Process PDF files, Markdown documents (.md), Text files (.txt), and web article URLs
- **Smart Content Caching**: Web articles are cached locally for future reference
- **Format Preservation**: Markdown formatting is preserved during processing for better structure retention
- **Dynamic AI Teams**: Automatically creates specialized agents based on content topics (AI researchers, philosophers, critics, etc.)
- **Multi-language Support**: Generate educational content in any language (Spanish by default)
- **Multiple Voice Providers**: Choose between ElevenLabs and Cartesia for audio synthesis
- **Structured Output**: Saves discussion transcripts, crew structures, and final scripts
- **CLI Interface**: Simple command-line tool for processing documents and articles
- **Educational Style**: Creates content in the engaging style of popular science educators

## Installation

```bash
# Clone and install dependencies
uv sync

# Or install manually
pip install -e .
```

## Configuration

Create a `.env` file with your API keys:

```env
OPENAI_API_KEY=your_openai_key
MODEL_NAME=o3-2025-04-16
ELEVENLABS_API_KEY=your_elevenlabs_key
ELEVENLABS_VOICE_ID=your_voice_id
CARTESIA_API_KEY=your_cartesia_key
```

## Usage

### Command Line

```bash
# Process a PDF file (defaults to Spanish)
voice-papers paper.pdf

# Process a Markdown file
voice-papers article.md

# Process a Text file
voice-papers notes.txt

# Process a web article URL
voice-papers "https://blog.research.google/2017/08/transformer-novel-neural-network.html"

# With options (works with all file types and URLs)
voice-papers paper.pdf --language English --voice-provider elevenlabs --project-name my_project
voice-papers article.md --language Spanish --script-only --duration 10
voice-papers "https://example.com/article" --language Spanish --script-only --duration 5

# Generate only the script without audio
voice-papers document.md --script-only

# Generate audio from existing script
voice-papers --audio-from-script /path/to/script.txt

# Direct mode for pre-processed content
voice-papers notes.txt --direct  # Skips extraction, directly processes content
```

### Python API

```python
from voice_papers.agents.crew_manager import CrewManager
from voice_papers.voice.synthesizer import get_synthesizer

# Create crew and generate discussion
manager = CrewManager(language="Spanish", project_name="my_paper", pdf_path=pdf_path)
crew = manager.create_crew_for_paper(paper_content, paper_title)
script = manager.run_crew_and_save_discussion(crew, paper_title)

# Generate audio
synthesizer = get_synthesizer("elevenlabs")
synthesizer.synthesize(script, "output.mp3", voice_id="your_voice_id")
```

## Project Structure

### For Local Files (PDF, Markdown, Text)
Each processed document creates a project directory in the same folder as the source file:

```
document_directory/
├── document.pdf/.md/.txt         # Original document
├── document_extracted_text.txt    # Cleaned extracted text (PDF only)
└── project_name/
    ├── discussion/
    │   ├── crew_structure.json    # Agent roles and tasks
    │   ├── final_result.txt       # Final discussion output
    │   └── task_*_output.txt      # Individual task outputs
    ├── educational_script.txt     # Final educational script
    ├── extracted_text.txt         # Copy of extracted text
    └── educational_lecture.mp3    # Generated audio
```

### For Web Articles
Web articles are cached and processed in a dedicated cache directory:

```
projects/
├── web_cache/
│   └── domain_hash_extracted_text.txt  # Cached article content
└── project_name/
    ├── discussion/
    │   ├── crew_structure.json         # Agent roles and tasks
    │   ├── final_result.txt            # Final discussion output
    │   └── task_*_output.txt           # Individual task outputs
    ├── educational_script.txt          # Final educational script
    ├── extracted_text.txt              # Copy of extracted text
    └── educational_lecture.mp3         # Generated audio
```

## Supported Input Formats

### PDF Files (.pdf)
- Academic papers with complex layouts
- Books and research documents
- Automatic title extraction from metadata or content

### Markdown Files (.md, .markdown)
- Blog posts and articles
- Documentation and tutorials
- Preserves formatting and structure
- Title extraction from H1 headers or frontmatter

### Text Files (.txt)
- Plain text documents
- Notes and simple content
- Title extraction from first lines or explicit "Title:" prefix

### Web Articles (URLs)
- Blog posts and online articles
- News and research publications
- Automatic content extraction and caching

## Agent Roles

The system dynamically creates agents based on document topics:

### Base Roles (Always Present)
- **Coordinator**: Manages discussion flow
- **Scientific Reviewer**: Validates methodology 
- **Critical Thinker**: Questions assumptions
- **Educational Writer**: Creates engaging educational script
- **Voice Director**: Optimizes for audio delivery

### AI Paper Specialists
- **AI Researcher**: Technical insights
- **AI Philosopher**: Ethical implications
- **AI Doomer**: Risk assessment
- **AI Enthusiast**: Positive applications
- **AI Newcomer**: Basic questions

## Examples

### Spanish Example

```bash
# Run the included Spanish example
python examples/run_example.py
```

This processes a sample AI paper in Spanish and generates an educational lecture using the configured ElevenLabs voice.

## Voice Providers

### ElevenLabs
- High-quality voice synthesis
- Multiple voice options
- Good multilingual support

### Cartesia
- Fast synthesis
- Real-time streaming capabilities
- Lower latency

## Video Creation

Voice Papers can now create animated videos from your audio lectures:

### Vertical Videos (1080x1920 - Perfect for TikTok/Instagram Stories)
```bash
# Create vertical video with sine waveform
python create_video.py audio.mp3 --waveform-style sine --orientation vertical

# Create vertical video with Mandelbrot fractal
python create_video.py audio.mp3 --waveform-style mandelbrot --gradient-style cosmic
```

### Horizontal Videos (1920x1080 - Perfect for YouTube/Twitter)
```bash
# Create horizontal video with circular waveform
python create_video.py audio.mp3 --waveform-style circular --orientation horizontal

# Create horizontal video with mathematical forms
python create_video.py audio.mp3 --waveform-style mathematical --orientation horizontal
```

### Video Styles Available:
- **circular**: Circular waveform with audio-reactive bars
- **sine**: Sine wave patterns that flow across the frame
- **mathematical/fractal**: Mathematical forms (Fibonacci spirals, Lissajous curves, polar roses)
- **mandelbrot**: Mandelbrot set with infinite zoom and audio-reactive colors

### Python API for Videos:
```python
from voice_papers.video import create_vertical_video, create_horizontal_video
from pathlib import Path

# Create vertical video (1080x1920)
create_vertical_video(
    audio_path=Path("lecture.mp3"),
    output_path=Path("vertical_video.mp4"),
    waveform_style="mandelbrot",
    gradient_style="cosmic"
)

# Create horizontal video (1920x1080)
create_horizontal_video(
    audio_path=Path("lecture.mp3"),
    output_path=Path("horizontal_video.mp4"),
    waveform_style="sine",
    gradient_style="sunset"
)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request

## License

MIT License - see LICENSE file for details.