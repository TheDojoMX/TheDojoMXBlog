"""Command line interface for Voice Papers."""

import os
import click
from pathlib import Path
import re
from urllib.parse import urlparse
from .utils.pdf_reader import extract_text_from_pdf, extract_title_and_text_from_pdf
from .utils.web_reader import extract_text_from_url, generate_cache_filename
from .utils.text_cleaner import clean_paper_text, extract_title_from_text
from .utils.file_reader import read_document_file
from .agents.crew_manager import CrewManager
from .voice.synthesizer import get_synthesizer
from .config import ELEVENLABS_VOICE_ID
from .utils.file_backup import backup_existing_file, get_filename_with_focus


@click.command()
@click.argument("input_source", type=str)
@click.option(
    "--language", "-l", default="Spanish", help="Language for the educational content"
)
@click.option(
    "--voice-provider",
    "-v",
    default="elevenlabs",
    type=click.Choice(["elevenlabs", "cartesia"]),
    help="Voice synthesis provider",
)
@click.option(
    "--voice-id", default=None, help="Voice ID for synthesis (overrides --voice)"
)
@click.option(
    "--voice",
    default="hectorip",
    type=click.Choice(["ana", "hectorip", "rachel"]),
    help="Voice selection: ana (Spanish female), hectorip (custom), rachel (English female)",
)
@click.option(
    "--model",
    "-m",
    default="flash",
    type=click.Choice(["flash", "turbo", "v3", "multilingual", "english"]),
    help="ElevenLabs model: flash (fastest), turbo (fast), v3 (newer), multilingual (quality), english (best quality)",
)
@click.option(
    "--stability",
    default=None,
    type=click.FloatRange(0.0, 1.0),
    help="Voice stability (0.0-1.0): Higher values = more consistent, lower = more emotional. Default: 0.65",
)
@click.option(
    "--similarity-boost",
    default=None,
    type=click.FloatRange(0.0, 1.0),
    help="Similarity boost (0.0-1.0): Higher values = more similar to original voice. Default: 0.8",
)
@click.option(
    "--style",
    "voice_style",
    default=None,
    type=click.FloatRange(0.0, 1.0),
    help="Style exaggeration (0.0-1.0): Higher values = more style, may reduce stability. Default: 0.0",
)
@click.option(
    "--speaker-boost",
    default=None,
    type=bool,
    help="Enable speaker boost for improved voice clarity. Default: True",
)
@click.option(
    "--project-name",
    "-p",
    default=None,
    help="Project name (defaults to filename or URL-derived name)",
)
@click.option(
    "--script-only",
    is_flag=True,
    help="Generate only the script without audio synthesis",
)
@click.option(
    "--audio-from-script",
    type=click.Path(exists=True, path_type=Path),
    help="Generate audio from existing script file",
)
@click.option(
    "--technical-level",
    "-t",
    default="accessible",
    type=click.Choice(["simple", "accessible", "technical"]),
    help="Technical level: simple (non-technical audience), accessible (general), technical (experts)",
)
@click.option(
    "--duration",
    "-d",
    default=5,
    type=click.IntRange(min=1, max=60),
    help="Target duration in minutes (1-60 minutes)",
)
@click.option(
    "--conversation-mode",
    "-c",
    default="enhanced",
    type=click.Choice(["original", "enhanced"]),
    help="Conversation mode: original (4 tasks), enhanced (7 tasks with multi-agent conversations)",
)
@click.option(
    "--tone",
    default="academic",
    type=click.Choice(["academic", "casual", "humorous", "playful"]),
    help="Conversation tone: academic (serious), casual (relaxed), humorous (funny but respectful), playful (light and entertaining)",
)
@click.option(
    "--debug-title",
    is_flag=True,
    help="Show debug information for title extraction process",
)
@click.option(
    "--extract-only",
    is_flag=True,
    help="Extract text from PDF/URL only and save to file, skip if already a text document",
)
@click.option(
    "--summary",
    is_flag=True,
    help="Use simplified workflow: Document → Summary → Educational Writer (skips multi-agent discussion)",
)
@click.option(
    "--light-edit",
    is_flag=True,
    help="Apply light editing for readability after summary (fixes grammar, keeps content intact)",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable detailed debug logging to see workflow progress",
)
@click.option(
    "--direct",
    is_flag=True,
    help="Use direct workflow: Text → Educational Writer only (fastest, for pre-processed content)",
)
@click.option(
    "--text-file",
    type=click.Path(exists=True, path_type=Path),
    help="Read text content from file for --direct mode (alternative to PDF/URL input)",
)
@click.option(
    "--tts-optimize",
    is_flag=True,
    help="Generate additional TTS-optimized version of the script with enhanced formatting for voice synthesis",
)
@click.option(
    "--reuse-discussion",
    is_flag=True,
    help="Reuse existing discussion from previous run and only regenerate final script and TTS version",
)
@click.option(
    "--skip-synthesis",
    is_flag=True,
    help="Skip the synthesis step and use raw content directly (legacy behavior)",
)
@click.option(
    "--use-legacy-tts",
    is_flag=True,
    help="Use legacy TTS without duration-based chunking (not recommended for long scripts)",
)
@click.option(
    "--tts-only",
    type=click.Path(exists=True, path_type=Path),
    help="Reprocess only TTS optimization from existing educational script",
)
@click.option(
    "--synthesis-method",
    default="concatenation",
    type=click.Choice(["concatenation", "knowledge_graph", "original"]),
    help="Synthesis method: concatenation (direct + knowledge graph by default), knowledge_graph (structured only), original (compressed)"
)
@click.option(
    "--no-knowledge-graph",
    is_flag=True,
    help="Skip generating knowledge graph (generated by default with concatenation method)"
)
@click.option(
    "--focus",
    default="explanatory",
    type=click.Choice(
        [
            "explanatory",
            "innovation",
            "practical",
            "historical",
            "tutorial",
            "critical",
            "story",
            "technical",
            "all",
        ]
    ),
    help="Analysis focus mode: explanatory (default), innovation, practical, historical, tutorial, critical, story, technical (zero interpretation), or all",
)
def main(
    input_source: str,
    language: str,
    voice_provider: str,
    voice_id: str,
    voice: str,
    model: str,
    stability: float,
    similarity_boost: float,
    voice_style: float,
    speaker_boost: bool,
    project_name: str,
    script_only: bool,
    audio_from_script: Path,
    technical_level: str,
    duration: int,
    conversation_mode: str,
    tone: str,
    debug_title: bool,
    extract_only: bool,
    summary: bool,
    light_edit: bool,
    debug: bool,
    direct: bool,
    text_file: Path,
    tts_optimize: bool,
    reuse_discussion: bool,
    skip_synthesis: bool,
    use_legacy_tts: bool,
    tts_only: Path,
    synthesis_method: str,
    no_knowledge_graph: bool,
    focus: str,
):
    """Generate an educational audio lecture from a document (PDF, MD, TXT) or web article.

    INPUT_SOURCE can be:
    - PDF file path (.pdf)
    - Markdown file path (.md, .markdown)
    - Text file path (.txt)
    - Web article URL
    
    For --direct mode, use "-" to read from stdin.

    Workflow modes:
    - Default: Document → Concatenation Synthesis + Knowledge Graph → Multi-agent discussion → Educational transformation
    - --summary: Document → Concatenation Synthesis + Knowledge Graph → Educational Writer (faster, skips multi-agent discussion)
    - --direct: Text → Educational Writer only (fastest, for pre-processed content)
    - --skip-synthesis: Use legacy behavior without synthesis step
    
    Synthesis Methods (NEW DEFAULT: concatenation + knowledge graph):
    - concatenation (default): Direct content extraction + knowledge graph generation
    - knowledge_graph: Only structured knowledge graph extraction
    - original: Legacy compressed synthesis
    - Use --no-knowledge-graph to skip knowledge graph generation

    Use --extract-only to only extract and clean text from PDF/URL sources,
    skipping the generation process. Text files are skipped since no extraction is needed.

        TTS Optimization:
    Use --tts-optimize to generate an additional version of the script optimized for
    Text-to-Speech synthesis with enhanced formatting, emphasis markers, strategic pauses,
    and rhythm patterns for more natural voice output.

    Reuse Discussion:
    Use --reuse-discussion to skip the multi-agent conversation and reuse existing discussion
    from a previous run. This quickly regenerates only the final educational script and TTS
    version using the existing conversation results.

    Voice Quality Settings:
    - --stability: Higher values (0.7-0.9) for consistent narration, lower (0.3-0.5) for expressive delivery
    - --similarity-boost: Higher values (0.8-1.0) for better voice matching, lower for more variation
    - --style: Keep at 0.0 for stability, increase (0.1-0.3) for more character expression
    - --speaker-boost: Enable for clearer voice reproduction (recommended)

    Audio Generation (NEW):
    - Duration-based chunking: Audio is automatically split into 5-6 minute chunks
    - State management: Generation progress is saved and can be resumed if interrupted
    - Cost tracking: API usage and costs are logged in .state directories
    - --use-legacy-tts: Use original TTS without improvements (not recommended for long scripts)
    """

    # Handle TTS-only reprocessing
    if tts_only:
        click.echo(f"🎯 Reprocessing TTS optimization from: {tts_only.name}")

        # Read the educational script
        with open(tts_only, "r", encoding="utf-8") as f:
            educational_script = f.read()

        # Determine project directory
        output_dir = tts_only.parent
        project_name = tts_only.stem.replace("_educational_script", "")
        
        # Extract title from the script content (first line) or use project name
        lines = educational_script.strip().split('\n')
        if lines and not lines[0].startswith(('TLDR:', '**', '#', '-')):
            paper_title = lines[0].strip()
        else:
            paper_title = project_name.replace("_", " ").replace("-", " ").title()

        # Initialize crew manager for TTS optimization
        crew_manager = CrewManager(
            language=language,
            project_name=project_name,
            technical_level=technical_level,
            duration_minutes=duration,
            conversation_mode=conversation_mode,
            tone=tone,
            focus=focus,
            synthesis_method=synthesis_method,
            generate_knowledge_graph=not no_knowledge_graph,
        )

        click.echo("🎯 Generating TTS-optimized version...")
        
        # For technical focus, add conversational touch before TTS optimization
        if focus == "technical":
            click.echo("💬 Adding conversational touch for better readability...")
            conversational_script = crew_manager.run_conversational_enhancement(
                educational_script, paper_title=paper_title
            )
            
            # Save conversational version
            conv_filename = get_filename_with_focus(f"{project_name}_conversational", focus)
            conv_script_path = output_dir / conv_filename
            backup_existing_file(conv_script_path)
            with open(conv_script_path, "w", encoding="utf-8") as f:
                f.write(conversational_script)
            click.echo(f"📝 Conversational script saved to: {conv_script_path}")
            
            # Use conversational version for TTS
            tts_script = crew_manager.run_tts_optimization_workflow(
                conversational_script, language, voice_provider
            )
        else:
            tts_script = crew_manager.run_tts_optimization_workflow(
                educational_script, language, voice_provider
            )

        # Save TTS-optimized script with focus mode
        tts_filename = get_filename_with_focus(f"{project_name}_tts_optimized", focus)
        tts_script_path = output_dir / tts_filename

        # Backup existing file if it exists
        backup_existing_file(tts_script_path)

        with open(tts_script_path, "w", encoding="utf-8") as f:
            f.write(tts_script)

        click.echo(f"🎙️  TTS-optimized script saved to: {tts_script_path}")

        # Generate audio if not script-only mode
        if not script_only:
            # Resolve voice settings
            if not voice_id:
                voice_id = ELEVENLABS_VOICE_ID if voice == "hectorip" else None

            # Apply TTS mode setting
            if use_legacy_tts:
                os.environ["ELEVENLABS_USE_IMPROVED"] = "false"
                click.echo("⚠️  Using legacy TTS (may fail on long scripts)")
            else:
                os.environ["ELEVENLABS_USE_IMPROVED"] = "true"
                click.echo("✨ Using improved TTS with duration-based chunking")

            synthesizer = get_synthesizer(voice_provider)

            click.echo("🎵 Generating audio from TTS-optimized script...")
            if voice_provider == "elevenlabs":
                click.echo("🎛️  Voice Quality Settings:")
                click.echo(
                    f"   Stability: {stability if stability is not None else 'Default (0.65)'}"
                )
                click.echo(
                    f"   Similarity Boost: {similarity_boost if similarity_boost is not None else 'Default (0.8)'}"
                )
                click.echo(
                    f"   Style: {voice_style if voice_style is not None else 'Default (0.0)'}"
                )
                click.echo(
                    f"   Speaker Boost: {speaker_boost if speaker_boost is not None else 'Default (True)'}"
                )

            audio_filename = get_filename_with_focus(
                f"{project_name}_educational_lecture", focus, ".mp3"
            )
            audio_path = output_dir / audio_filename
            success = synthesizer.synthesize(
                tts_script,
                audio_path,
                voice_id,
                model=model,
                voice_name=voice,
                stability=stability,
                similarity_boost=similarity_boost,
                style=voice_style,
                use_speaker_boost=speaker_boost,
            )

            if success:
                click.echo(f"🎧 Audio saved to: {audio_path}")
                click.echo(
                    "📻 Audio generated using TTS-optimized script for better voice quality"
                )
            else:
                click.echo("❌ Audio synthesis failed")
        else:
            click.echo("⏭️  Skipping audio generation (script-only mode)")

        click.echo("✅ TTS reprocessing completed!")
        return

    # Handle audio generation from existing script
    if audio_from_script:
        click.echo(f"🎙️  Generating audio from script: {audio_from_script.name}")

        # Read the script content
        with open(audio_from_script, "r", encoding="utf-8") as f:
            script_content = f.read()

        # Determine output directory (same as script location)
        output_dir = audio_from_script.parent

        # Set environment variable for legacy TTS if requested
        if use_legacy_tts:
            os.environ["ELEVENLABS_USE_IMPROVED"] = "false"
            click.echo("⚠️  Using legacy TTS (may fail on long scripts)")
        else:
            os.environ["ELEVENLABS_USE_IMPROVED"] = "true"
            click.echo("✨ Using improved TTS with duration-based chunking")

        # Generate audio
        synthesizer = get_synthesizer(voice_provider)

        # Use provided voice_id or default
        if not voice_id and voice_provider == "elevenlabs":
            voice_id = ELEVENLABS_VOICE_ID

        # Show voice quality settings
        if voice_provider == "elevenlabs":
            click.echo("🎛️  Voice Quality Settings:")
            click.echo(
                f"   Stability: {stability if stability is not None else 'Default (0.65)'}"
            )
            click.echo(
                f"   Similarity Boost: {similarity_boost if similarity_boost is not None else 'Default (0.8)'}"
            )
            click.echo(
                f"   Style: {voice_style if voice_style is not None else 'Default (0.0)'}"
            )
            click.echo(
                f"   Speaker Boost: {speaker_boost if speaker_boost is not None else 'Default (True)'}"
            )

        # For audio-from-script, don't add focus to filename
        audio_path = output_dir / "educational_lecture.mp3"
        success = synthesizer.synthesize(
            script_content,
            audio_path,
            voice_id,
            model=model,
            voice_name=voice,
            stability=stability,
            similarity_boost=similarity_boost,
            style=voice_style,
            use_speaker_boost=speaker_boost,
        )

        if success:
            click.echo(f"🎧 Audio saved to: {audio_path}")
        else:
            click.echo("❌ Audio synthesis failed")

        return

    # Handle direct mode
    if direct:
        click.echo("🚀 Using direct mode: Text → Educational Writer")

        # Get text content
        if text_file:
            click.echo(f"📄 Reading text from: {text_file.name}")
            # Use the file reader to handle both text and markdown
            title, text_content = read_document_file(text_file, debug=debug_title)

            # Set project name
            if not project_name:
                project_name = f"direct_{text_file.stem}"

        else:
            # Check if input_source is stdin indicator or a text file
            if input_source == "-":
                click.echo("📝 Reading from stdin...")
                import sys

                text_content = sys.stdin.read()
                title = "Direct Input"
                if not project_name:
                    project_name = "direct_stdin"

            else:
                # Handle direct text file input
                direct_file = Path(input_source)
                if not direct_file.exists():
                    click.echo(f"❌ File not found: {input_source}")
                    raise click.Abort()

                if direct_file.suffix.lower() not in [".txt", ".md", ".markdown"]:
                    click.echo(f"❌ For direct mode, file must be .txt, .md, or .markdown: {input_source}")
                    raise click.Abort()

                # Use the file reader to handle both text and markdown
                title, text_content = read_document_file(direct_file, debug=debug_title)

                # Set project name
                if not project_name:
                    project_name = f"direct_{direct_file.stem}"

        # Create crew manager for direct mode
        crew_manager = CrewManager(
            language=language,
            project_name=project_name,
            pdf_path=None,
            technical_level=technical_level,
            duration_minutes=duration,
            conversation_mode=conversation_mode,
            tone=tone,
            focus=focus,
            synthesis_method=synthesis_method,
            generate_knowledge_graph=not no_knowledge_graph,
        )

        # Run direct workflow
        click.echo("🤖 Running direct educational transformation...")
        final_script = crew_manager.run_direct_educational_workflow(text_content, title)
        
        # Apply light editing if requested
        if light_edit:
            click.echo(f"✏️  Applying light {language} editing for readability...")
            final_script = crew_manager.run_light_edit_flow(final_script, title)
            click.echo("✅ Light editing completed")

        # Save the script with focus mode in filename
        script_filename = get_filename_with_focus("educational_script", focus)
        script_path = crew_manager.project_dir / script_filename

        # Backup existing file if it exists
        backup_existing_file(script_path)

        with open(script_path, "w", encoding="utf-8") as f:
            f.write(final_script)

        click.echo(f"📝 Educational script saved to: {script_path}")

        # Generate TTS-optimized version if requested
        if tts_optimize:
            click.echo("🎯 Generating TTS-optimized version...")
            
            # For technical focus, add conversational touch before TTS optimization
            if focus == "technical":
                click.echo("💬 Adding conversational touch for better readability...")
                conversational_script = crew_manager.run_conversational_enhancement(
                    final_script, paper_title=paper_title
                )
                
                # Save conversational version
                conv_filename = get_filename_with_focus("educational_script_conversational", focus)
                conv_script_path = crew_manager.project_dir / conv_filename
                backup_existing_file(conv_script_path)
                with open(conv_script_path, "w", encoding="utf-8") as f:
                    f.write(conversational_script)
                click.echo(f"📝 Conversational script saved to: {conv_script_path}")
                
                # Use conversational version for TTS
                tts_script = crew_manager.run_tts_optimization_workflow(
                    conversational_script, language, voice_provider
                )
            else:
                tts_script = crew_manager.run_tts_optimization_workflow(
                    final_script, language, voice_provider
                )

            tts_filename = get_filename_with_focus("educational_script_tts", focus)
            tts_script_path = crew_manager.project_dir / tts_filename

            # Backup existing file if it exists
            backup_existing_file(tts_script_path)

            with open(tts_script_path, "w", encoding="utf-8") as f:
                f.write(tts_script)

            click.echo(f"🎙️  TTS-optimized script saved to: {tts_script_path}")

        # Generate audio if not script-only
        if not script_only:
            click.echo("🎙️  Generating audio...")
            # Apply TTS mode setting
            if use_legacy_tts:
                os.environ["ELEVENLABS_USE_IMPROVED"] = "false"
            else:
                os.environ["ELEVENLABS_USE_IMPROVED"] = "true"
            synthesizer = get_synthesizer(voice_provider)

            if not voice_id and voice_provider == "elevenlabs":
                voice_id = ELEVENLABS_VOICE_ID

            # Show voice quality settings
            if voice_provider == "elevenlabs":
                click.echo("🎛️  Voice Quality Settings:")
                click.echo(
                    f"   Stability: {stability if stability is not None else 'Default (0.65)'}"
                )
                click.echo(
                    f"   Similarity Boost: {similarity_boost if similarity_boost is not None else 'Default (0.8)'}"
                )
                click.echo(
                    f"   Style: {voice_style if voice_style is not None else 'Default (0.0)'}"
                )
                click.echo(
                    f"   Speaker Boost: {speaker_boost if speaker_boost is not None else 'Default (True)'}"
                )

            # Use TTS-optimized script if available, otherwise use regular script
            script_for_audio = tts_script if tts_optimize else final_script
            audio_filename = get_filename_with_focus(
                "educational_lecture", focus, ".mp3"
            )
            audio_path = crew_manager.project_dir / audio_filename
            success = synthesizer.synthesize(
                script_for_audio,
                audio_path,
                voice_id,
                model=model,
                voice_name=voice,
                stability=stability,
                similarity_boost=similarity_boost,
                style=voice_style,
                use_speaker_boost=speaker_boost,
            )

            if success:
                click.echo(f"🎧 Audio saved to: {audio_path}")
                if tts_optimize:
                    click.echo(
                        "📻 Audio generated using TTS-optimized script for better voice quality"
                    )
            else:
                click.echo("❌ Audio synthesis failed")
        else:
            click.echo("⏭️  Skipping audio generation (script-only mode)")

        click.echo(f"✅ Direct mode completed! Check: {crew_manager.project_dir}")
        return

    # Detect if input is URL or file path
    def is_url(source: str) -> bool:
        try:
            result = urlparse(source)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    is_web_article = is_url(input_source)

    # Determine project name and source info
    if is_web_article:
        if not project_name:
            # Extract project name from URL
            parsed_url = urlparse(input_source)
            path_parts = [p for p in parsed_url.path.split("/") if p]
            if path_parts:
                project_name = path_parts[-1].replace("-", "_").replace(".html", "")
            else:
                domain = parsed_url.netloc.replace("www.", "").replace(".", "_")
                project_name = f"web_article_{domain}"

        click.echo(f"🌐 Processing web article: {input_source}")
        source_path = None
    else:
        # It's a file path
        source_path = Path(input_source)
        if not source_path.exists():
            click.echo(f"❌ File not found: {input_source}")
            raise click.Abort()

        if not project_name:
            project_name = source_path.stem

        # Determine file type
        suffix = source_path.suffix.lower()
        if suffix == ".txt":
            click.echo(f"📄 Processing text file: {source_path.name}")
        elif suffix in [".md", ".markdown"]:
            click.echo(f"📝 Processing markdown file: {source_path.name}")
        elif suffix == ".pdf":
            click.echo(f"📄 Processing PDF: {source_path.name}")
        else:
            click.echo(f"❌ Unsupported file type: {suffix}")
            raise click.Abort()

    click.echo(f"Project: {project_name}")
    click.echo(f"Language: {language}")
    click.echo(f"Technical level: {technical_level}")
    click.echo(f"Target duration: {duration} minutes")
    click.echo(f"Voice provider: {voice_provider}")
    click.echo(f"Voice: {voice}")
    click.echo(f"Model: {model}")
    click.echo(f"Conversation mode: {conversation_mode}")
    click.echo(f"Conversation tone: {tone}")
    click.echo(f"Focus mode: {focus}")

    # Show voice quality settings
    if voice_provider == "elevenlabs":
        click.echo("🎛️  Voice Quality Settings:")
        click.echo(
            f"   Stability: {stability if stability is not None else 'Default (0.65)'}"
        )
        click.echo(
            f"   Similarity Boost: {similarity_boost if similarity_boost is not None else 'Default (0.8)'}"
        )
        click.echo(
            f"   Style: {voice_style if voice_style is not None else 'Default (0.0)'}"
        )
        click.echo(
            f"   Speaker Boost: {speaker_boost if speaker_boost is not None else 'Default (True)'}"
        )

    # Handle extract-only mode
    if extract_only:
        click.echo("🔍 Extract-only mode activated")

        if is_web_article:
            # Handle web article extraction
            cache_filename = generate_cache_filename(input_source)
            cache_dir = Path("projects") / "web_cache"
            cache_dir.mkdir(parents=True, exist_ok=True)
            extracted_text_path = cache_dir / cache_filename

            if extracted_text_path.exists():
                click.echo(f"✅ Web content already extracted: {extracted_text_path}")
                return
            else:
                click.echo("🌐 Extracting content from web article...")
                title, raw_content = extract_text_from_url(input_source)

                # For web content, preserve markdown formatting
                click.echo("📝 Preserving article structure...")
                # Save with title and markdown content
                full_content = f"Title: {title}\n\n{raw_content}"

                # Save as markdown file for better preservation
                markdown_path = cache_dir / cache_filename.replace(".txt", ".md")
                with open(markdown_path, "w", encoding="utf-8") as f:
                    f.write(full_content)

                # Also save as txt for compatibility
                with open(extracted_text_path, "w", encoding="utf-8") as f:
                    f.write(full_content)
                click.echo(
                    f"✅ Web content extracted and saved to: {extracted_text_path}"
                )
                return
        else:
            # Handle local file
            if source_path.suffix.lower() in [".txt", ".md", ".markdown"]:
                click.echo("⏭️  Input is already a text/markdown file, no extraction needed")
                click.echo(f"📄 File: {source_path}")
                return
            elif source_path.suffix.lower() == ".pdf":
                # Handle PDF extraction
                extracted_text_path = (
                    source_path.parent / f"{source_path.stem}_extracted_text.txt"
                )

                if extracted_text_path.exists():
                    click.echo(f"✅ PDF text already extracted: {extracted_text_path}")
                    return
                else:
                    click.echo("📄 Extracting text and title from PDF...")
                    extracted_title, raw_text = extract_title_and_text_from_pdf(
                        source_path, debug=debug_title
                    )

                    # Clean the extracted text
                    click.echo("🧹 Cleaning paper text...")
                    paper_content = clean_paper_text(raw_text)

                    # Save cleaned text in same directory as PDF
                    with open(extracted_text_path, "w", encoding="utf-8") as f:
                        f.write(paper_content)

                    if extracted_title:
                        click.echo(f"📋 Título extraído: {extracted_title}")

                    click.echo(
                        f"✅ PDF text extracted and saved to: {extracted_text_path}"
                    )
                    return
            else:
                click.echo(f"❌ Unsupported file type for extraction: {source_path.suffix}")
                raise click.Abort()

    try:
        if is_web_article:
            # Handle web article
            cache_filename = generate_cache_filename(input_source)
            cache_dir = Path("projects") / "web_cache"
            cache_dir.mkdir(parents=True, exist_ok=True)
            extracted_text_path = cache_dir / cache_filename

            if extracted_text_path.exists():
                click.echo(f"🌐 Using cached web content: {extracted_text_path.name}")
                with open(extracted_text_path, "r", encoding="utf-8") as f:
                    cached_content = f.read()
                # Extract title from cached content but keep full content
                lines = cached_content.split("\n")
                title_line = lines[0] if lines else ""
                if title_line.startswith("Title: "):
                    paper_title = title_line.replace("Title: ", "")
                else:
                    paper_title = project_name.replace("_", " ").title()
                # Use the complete cached content without modifications
                paper_content = cached_content
            else:
                # Extract from web
                click.echo("🌐 Extracting content from web article...")
                title, raw_content = extract_text_from_url(input_source)
                paper_title = title
                # Set paper_content to the raw content for web articles
                paper_content = raw_content

                # For web content, preserve markdown formatting
                click.echo("📝 Preserving article structure...")
                # Save with title and markdown content
                full_content = f"Title: {title}\n\n{raw_content}"

                # Save as markdown file for better preservation
                markdown_path = cache_dir / cache_filename.replace(".txt", ".md")
                with open(markdown_path, "w", encoding="utf-8") as f:
                    f.write(full_content)

                # Also save as txt for compatibility
                with open(extracted_text_path, "w", encoding="utf-8") as f:
                    f.write(full_content)
                click.echo(f"🌐 Web content cached to: {extracted_text_path}")
        else:
            # Handle local file (PDF, MD, or TXT)
            suffix = source_path.suffix.lower()
            
            if suffix in [".txt", ".md", ".markdown"]:
                # Handle text/markdown file directly
                click.echo(f"📄 Reading {suffix} file...")
                extracted_title, raw_text = read_document_file(source_path, debug=debug_title)

                # For markdown files, preserve formatting; for text files, clean them
                if suffix in [".md", ".markdown"]:
                    click.echo("📝 Preserving markdown formatting...")
                    paper_content = raw_text  # Keep markdown as-is
                else:
                    click.echo("🧹 Cleaning text content...")
                    paper_content = clean_paper_text(raw_text)

                # No need to save extracted text for these files since source is already text
                extracted_text_path = None
            elif suffix == ".pdf":
                # Handle PDF file
                extracted_text_path = (
                    source_path.parent / f"{source_path.stem}_extracted_text.txt"
                )

                if extracted_text_path.exists():
                    click.echo(
                        f"📄 Using existing extracted text: {extracted_text_path.name}"
                    )
                    with open(extracted_text_path, "r", encoding="utf-8") as f:
                        paper_content = f.read()
                    # Try to extract title from existing content
                    extracted_title = extract_title_from_text(
                        paper_content, debug=debug_title
                    )
                else:
                    # Extract title and text from PDF
                    click.echo("📄 Extracting text and title from PDF...")
                    extracted_title, raw_text = extract_title_and_text_from_pdf(
                        source_path, debug=debug_title
                    )

                    # Clean the extracted text
                    click.echo("🧹 Cleaning paper text...")
                    paper_content = clean_paper_text(raw_text)

                    # Save cleaned text in same directory as PDF
                    with open(extracted_text_path, "w", encoding="utf-8") as f:
                        f.write(paper_content)
                    click.echo(f"📄 Cleaned PDF text saved to: {extracted_text_path}")
            else:
                click.echo(f"❌ Unsupported file type: {suffix}")
                raise click.Abort()

            # Use extracted title if available, otherwise fallback to filename
            if extracted_title:
                paper_title = extracted_title
                click.echo(f"📋 Título extraído del documento: {paper_title}")
                if debug_title:
                    click.echo("✅ Debug: Title extraction successful!")
            else:
                paper_title = (
                    source_path.stem.replace("_", " ").replace("-", " ").title()
                )
                click.echo(f"📋 Usando nombre del archivo como título: {paper_title}")
                if debug_title:
                    click.echo(
                        f"⚠️  Debug: Title extraction failed, using filename. Use --debug-title for details."
                    )
                else:
                    click.echo(
                        f"💡 Consejo: Si el título no es correcto, usa --debug-title para diagnosticar"
                    )

        # Handle "all" mode - generate all focus types
        if focus == "all":
            click.echo("🔄 Generating ALL focus modes...")
            focus_modes = [
                "explanatory",
                "innovation",
                "practical",
                "historical",
                "tutorial",
                "critical",
                "story",
            ]

            for current_focus in focus_modes:
                click.echo(f"\n{'=' * 60}")
                click.echo(f"🎯 Processing focus mode: {current_focus.upper()}")
                click.echo(f"{'=' * 60}\n")

                # Create crew manager for this focus
                focus_crew_manager = CrewManager(
                    language=language,
                    project_name=project_name,
                    pdf_path=source_path,
                    technical_level=technical_level,
                    duration_minutes=duration,
                    conversation_mode=conversation_mode,
                    tone=tone,
                    focus=current_focus,
                    synthesis_method=synthesis_method,
                    generate_knowledge_graph=not no_knowledge_graph,
                )

                # Run the appropriate workflow for this focus
                if summary:
                    final_script = focus_crew_manager.run_summary_workflow(
                        paper_content, paper_title, skip_synthesis=skip_synthesis
                    )
                else:
                    final_script = focus_crew_manager.run_workflow(
                        paper_content, paper_title, use_synthesis=not skip_synthesis
                    )

                # Save the script with focus mode
                script_filename = get_filename_with_focus(
                    "educational_script", current_focus
                )
                script_path = focus_crew_manager.project_dir / script_filename
                backup_existing_file(script_path)
                with open(script_path, "w", encoding="utf-8") as f:
                    f.write(final_script)
                click.echo(
                    f"📝 {current_focus.capitalize()} script saved to: {script_path}"
                )

                # Generate TTS if requested
                if tts_optimize:
                    # For technical focus, add conversational touch before TTS optimization
                    if current_focus == "technical":
                        click.echo("💬 Adding conversational touch for better readability...")
                        conversational_script = focus_crew_manager.run_conversational_enhancement(
                            final_script, paper_title=paper_title
                        )
                        
                        # Save conversational version
                        conv_filename = get_filename_with_focus(
                            "educational_script_conversational", current_focus
                        )
                        conv_script_path = focus_crew_manager.project_dir / conv_filename
                        backup_existing_file(conv_script_path)
                        with open(conv_script_path, "w", encoding="utf-8") as f:
                            f.write(conversational_script)
                        click.echo(f"📝 Conversational script saved to: {conv_script_path}")
                        
                        # Use conversational version for TTS
                        tts_script = focus_crew_manager.run_tts_optimization_workflow(
                            conversational_script, language, voice_provider
                        )
                    else:
                        tts_script = focus_crew_manager.run_tts_optimization_workflow(
                            final_script, language, voice_provider
                        )
                    
                    tts_filename = get_filename_with_focus(
                        "educational_script_tts", current_focus
                    )
                    tts_script_path = focus_crew_manager.project_dir / tts_filename
                    backup_existing_file(tts_script_path)
                    with open(tts_script_path, "w", encoding="utf-8") as f:
                        f.write(tts_script)
                    click.echo(
                        f"🎙️  {current_focus.capitalize()} TTS script saved to: {tts_script_path}"
                    )

                # Generate audio if not script-only
                if not script_only:
                    if not voice_id:
                        voice_id = ELEVENLABS_VOICE_ID if voice == "hectorip" else None

                    synthesizer = get_synthesizer(voice_provider)
                    script_for_audio = tts_script if tts_optimize else final_script
                    audio_filename = get_filename_with_focus(
                        "educational_lecture", current_focus, ".mp3"
                    )
                    audio_path = focus_crew_manager.project_dir / audio_filename

                    success = synthesizer.synthesize(
                        script_for_audio,
                        audio_path,
                        voice_id,
                        model=model,
                        voice_name=voice,
                        stability=stability,
                        similarity_boost=similarity_boost,
                        style=voice_style,
                        use_speaker_boost=speaker_boost,
                    )

                    if success:
                        click.echo(
                            f"🎧 {current_focus.capitalize()} audio saved to: {audio_path}"
                        )
                    else:
                        click.echo(
                            f"❌ Audio synthesis failed for {current_focus} mode"
                        )

            click.echo(f"\n{'=' * 60}")
            click.echo("✅ All focus modes completed!")
            click.echo(f"Check your results in: {crew_manager.project_dir}")
            return

        # Regular single focus mode processing
        # Create crew manager
        crew_manager = CrewManager(
            language=language,
            project_name=project_name,
            pdf_path=source_path,  # This might be None for web articles, need to check if CrewManager handles this
            technical_level=technical_level,
            duration_minutes=duration,
            conversation_mode=conversation_mode,
            tone=tone,
            focus=focus,
            synthesis_method=synthesis_method,
            generate_knowledge_graph=not no_knowledge_graph,
        )

        # Check if reusing existing discussion
        if reuse_discussion:
            click.echo("🔄 Checking for existing discussion to reuse...")
            if crew_manager.has_existing_discussion():
                click.echo(
                    "✅ Found existing discussion! Generating final script from previous conversation..."
                )
                final_script = crew_manager.run_reuse_discussion_workflow(paper_title)
                
                # Apply light editing if requested
                if light_edit:
                    click.echo(f"✏️  Applying light {language} editing for readability...")
                    final_script = crew_manager.run_light_edit_flow(final_script, paper_title)
                    click.echo("✅ Light editing completed")

                # Save the final script with focus mode
                script_filename = get_filename_with_focus("educational_script", focus)
                script_path = crew_manager.project_dir / script_filename

                # Backup existing file if it exists
                backup_existing_file(script_path)

                with open(script_path, "w", encoding="utf-8") as f:
                    f.write(final_script)

                click.echo(f"📝 Educational script saved to: {script_path}")

                # Generate TTS-optimized version if requested
                if tts_optimize:
                    click.echo("🎯 Generating TTS-optimized version...")
                    
                    # For technical focus, add conversational touch before TTS optimization
                    if focus == "technical":
                        click.echo("💬 Adding conversational touch for better readability...")
                        conversational_script = crew_manager.run_conversational_enhancement(
                            final_script, paper_title=title
                        )
                        
                        # Save conversational version
                        conv_filename = get_filename_with_focus("educational_script_conversational.txt", focus)
                        conv_script_path = crew_manager.project_dir / conv_filename
                        backup_existing_file(conv_script_path)
                        with open(conv_script_path, "w", encoding="utf-8") as f:
                            f.write(conversational_script)
                        click.echo(f"📝 Conversational script saved to: {conv_script_path}")
                        
                        # Use conversational version for TTS
                        tts_script = crew_manager.run_tts_optimization_workflow(
                            conversational_script, language, voice_provider
                        )
                    else:
                        tts_script = crew_manager.run_tts_optimization_workflow(
                            final_script, language, voice_provider
                        )

                    tts_filename = get_filename_with_focus(
                        "educational_script_tts.txt", focus
                    )
                    tts_script_path = crew_manager.project_dir / tts_filename

                    # Backup existing file if it exists
                    backup_existing_file(tts_script_path)

                    with open(tts_script_path, "w", encoding="utf-8") as f:
                        f.write(tts_script)

                    click.echo(f"🎙️  TTS-optimized script saved to: {tts_script_path}")

                # Also save a copy of extracted text in project directory for reference
                project_extracted_text = crew_manager.project_dir / "extracted_text.txt"
                with open(project_extracted_text, "w", encoding="utf-8") as f:
                    f.write(paper_content)

                if not script_only:
                    # Synthesize voice
                    click.echo("🎙️  Generating audio...")
                    # Apply TTS mode setting
                    if use_legacy_tts:
                        os.environ["ELEVENLABS_USE_IMPROVED"] = "false"
                    else:
                        os.environ["ELEVENLABS_USE_IMPROVED"] = "true"
                    synthesizer = get_synthesizer(voice_provider)

                    # Use provided voice_id or default
                    if not voice_id and voice_provider == "elevenlabs":
                        voice_id = ELEVENLABS_VOICE_ID

                    # Show voice quality settings
                    if voice_provider == "elevenlabs":
                        click.echo("🎛️  Voice Quality Settings:")
                        click.echo(
                            f"   Stability: {stability if stability is not None else 'Default (0.65)'}"
                        )
                        click.echo(
                            f"   Similarity Boost: {similarity_boost if similarity_boost is not None else 'Default (0.8)'}"
                        )
                        click.echo(
                            f"   Style: {voice_style if voice_style is not None else 'Default (0.0)'}"
                        )
                        click.echo(
                            f"   Speaker Boost: {speaker_boost if speaker_boost is not None else 'Default (True)'}"
                        )

                    # Use TTS-optimized script if available, otherwise use regular script
                    script_for_audio = tts_script if tts_optimize else final_script
                    audio_filename = get_filename_with_focus(
                        "educational_lecture.mp3", focus
                    )
                    audio_path = crew_manager.project_dir / audio_filename

                    # Backup existing audio file if it exists
                    backup_existing_file(audio_path)
                    success = synthesizer.synthesize(
                        script_for_audio,
                        audio_path,
                        voice_id,
                        model=model,
                        voice_name=voice,
                        stability=stability,
                        similarity_boost=similarity_boost,
                        style=voice_style,
                        use_speaker_boost=speaker_boost,
                    )

                    if success:
                        click.echo(f"🎧 Audio saved to: {audio_path}")
                        if tts_optimize:
                            click.echo(
                                "📻 Audio generated using TTS-optimized script for better voice quality"
                            )
                    else:
                        click.echo("❌ Audio synthesis failed")
                else:
                    click.echo("⏭️  Skipping audio generation (script-only mode)")

                click.echo(
                    f"✅ Reuse discussion completed! Check: {crew_manager.project_dir}"
                )
                return
            else:
                click.echo("⚠️  No existing discussion found. Running full workflow...")

        # Check if using summary mode
        if summary:
            click.echo(
                "📄 Using enhanced summary workflow (synthesis + direct to educational writer)..."
            )
            click.echo(f"📊 Document length: {len(paper_content):,} characters")
            click.echo("🔍 This workflow will:")
            click.echo("   1. Chunk the document into manageable sections")
            click.echo("   2. Deeply analyze each section to preserve details")
            click.echo("   3. Synthesize all analyses into comprehensive understanding")
            click.echo(
                "   4. Transform directly into educational script (skipping multi-agent discussion)"
            )
            click.echo(
                "🤖 Setting up AI crew (Enhanced Summary mode - 3 specialized agents)..."
            )
            final_script = crew_manager.run_summary_workflow(paper_content, paper_title)
            
            # Apply light editing if requested
            if light_edit:
                click.echo(f"✏️  Applying light {language} editing for readability...")
                final_script = crew_manager.run_light_edit_flow(final_script, paper_title)
                click.echo("✅ Light editing completed")
        else:
            # Original full workflow
            tasks_count = "7 tasks" if conversation_mode == "enhanced" else "4 tasks"
            click.echo(
                f"🤖 Setting up AI crew ({conversation_mode} mode - {tasks_count})..."
            )

            # Create and run crew
            click.echo("💭 Creating discussion crew...")

            # Detect topic to show user what type of content was detected
            detected_topic = crew_manager._detect_topic(
                paper_title + " " + paper_content[:1000]
            )
            agents_info = {
                "AI": "🤖 AI specialists (Researcher, Philosopher, Doomer, Enthusiast, Newcomer)",
                "Medicine": "🏥 Medical specialists (Researcher, Bioethicist, Clinician, Patient Advocate)",
                "Science": "🔬 Science specialists (Theoretical Physicist, Experimental Scientist, Communicator, Skeptic)",
                "Psychology": "🧠 Psychology specialists (Cognitive Scientist, Clinical Psychologist, Neuroscientist, Behavioral Economist)",
                "Economics": "💰 Economics specialists (Economist, Financial Analyst, Policy Advisor, Consumer Advocate)",
                "Technology": "💻 Technology specialists (Software Engineer, Security Expert, UX Designer, Tech Entrepreneur)",
                "General": "📚 General specialists (only base agents)",
            }

            # Calculate agent count (base 5 + specialized agents)
            specialist_counts = {
                "AI": 5,
                "Medicine": 4,
                "Science": 4,
                "Psychology": 4,
                "Economics": 4,
                "Technology": 4,
                "General": 0,
            }
            agent_count = 5 + specialist_counts.get(detected_topic, 0)

            # Add humor agent if applicable
            humor_bonus = ""
            if tone in ["humorous", "playful"]:
                agent_count += 1
                humor_bonus = " + 1 Comedy Communicator 🎭"

            specialist_info = agents_info.get(detected_topic, "no specialists")

            click.echo(f"🎯 Content detected: {detected_topic}")
            click.echo(
                f"👥 Using {agent_count} agents: 5 base + {specialist_info}{humor_bonus}"
            )

            # Default behavior now includes synthesis unless explicitly skipped
            use_synthesis = not skip_synthesis
            if use_synthesis:
                click.echo(
                    "🔬 NEW DEFAULT: Creating comprehensive synthesis before discussion..."
                )
            else:
                click.echo("⚠️  Using legacy mode: Skipping synthesis step")

            crew = crew_manager.create_crew_for_paper(
                paper_content, paper_title, use_synthesis=use_synthesis
            )

            click.echo("🗣️  Running discussion (this may take several minutes)...")
            final_script = crew_manager.run_crew_and_save_discussion(crew, paper_title)
            
            # Apply light editing if requested
            if light_edit:
                click.echo(f"✏️  Applying light {language} editing for readability...")
                final_script = crew_manager.run_light_edit_flow(final_script, paper_title)
                click.echo("✅ Light editing completed")

        # Save the final script
        script_filename = get_filename_with_focus("educational_script.txt", focus)
        script_path = crew_manager.project_dir / script_filename

        # Backup existing file if it exists
        backup_existing_file(script_path)

        with open(script_path, "w", encoding="utf-8") as f:
            f.write(final_script)

        click.echo(f"📝 Educational script saved to: {script_path}")

        # Generate TTS-optimized version if requested
        if tts_optimize:
            click.echo("🎯 Generating TTS-optimized version...")
            
            # For technical focus, add conversational touch before TTS optimization
            if focus == "technical":
                click.echo("💬 Adding conversational touch for better readability...")
                conversational_script = crew_manager.run_conversational_enhancement(
                    final_script, paper_title=paper_title
                )
                
                # Save conversational version
                conv_filename = get_filename_with_focus("educational_script_conversational", focus)
                conv_script_path = crew_manager.project_dir / conv_filename
                backup_existing_file(conv_script_path)
                with open(conv_script_path, "w", encoding="utf-8") as f:
                    f.write(conversational_script)
                click.echo(f"📝 Conversational script saved to: {conv_script_path}")
                
                # Use conversational version for TTS
                tts_script = crew_manager.run_tts_optimization_workflow(
                    conversational_script, language, voice_provider
                )
            else:
                tts_script = crew_manager.run_tts_optimization_workflow(
                    final_script, language, voice_provider
                )

            tts_filename = get_filename_with_focus("educational_script_tts", focus)
            tts_script_path = crew_manager.project_dir / tts_filename

            # Backup existing file if it exists
            backup_existing_file(tts_script_path)

            with open(tts_script_path, "w", encoding="utf-8") as f:
                f.write(tts_script)

            click.echo(f"🎙️  TTS-optimized script saved to: {tts_script_path}")

        # Also save a copy of extracted text in project directory for reference
        project_extracted_text = crew_manager.project_dir / "extracted_text.txt"
        with open(project_extracted_text, "w", encoding="utf-8") as f:
            f.write(paper_content)

        if not script_only:
            # Synthesize voice
            click.echo("🎙️  Generating audio...")
            # Apply TTS mode setting
            if use_legacy_tts:
                os.environ["ELEVENLABS_USE_IMPROVED"] = "false"
            else:
                os.environ["ELEVENLABS_USE_IMPROVED"] = "true"
            synthesizer = get_synthesizer(voice_provider)

            # Use provided voice_id or default
            if not voice_id and voice_provider == "elevenlabs":
                voice_id = ELEVENLABS_VOICE_ID

            # Show voice quality settings
            if voice_provider == "elevenlabs":
                click.echo("🎛️  Voice Quality Settings:")
                click.echo(
                    f"   Stability: {stability if stability is not None else 'Default (0.65)'}"
                )
                click.echo(
                    f"   Similarity Boost: {similarity_boost if similarity_boost is not None else 'Default (0.8)'}"
                )
                click.echo(
                    f"   Style: {voice_style if voice_style is not None else 'Default (0.0)'}"
                )
                click.echo(
                    f"   Speaker Boost: {speaker_boost if speaker_boost is not None else 'Default (True)'}"
                )

            # Use TTS-optimized script if available, otherwise use regular script
            script_for_audio = tts_script if tts_optimize else final_script
            audio_filename = get_filename_with_focus("educational_lecture.mp3", focus)
            audio_path = crew_manager.project_dir / audio_filename

            # Backup existing audio file if it exists
            backup_existing_file(audio_path)
            success = synthesizer.synthesize(
                script_for_audio,
                audio_path,
                voice_id,
                model=model,
                voice_name=voice,
                stability=stability,
                similarity_boost=similarity_boost,
                style=voice_style,
                use_speaker_boost=speaker_boost,
            )

            if success:
                click.echo(f"🎧 Audio saved to: {audio_path}")
                if tts_optimize:
                    click.echo(
                        "📻 Audio generated using TTS-optimized script for better voice quality"
                    )
            else:
                click.echo("❌ Audio synthesis failed")
        else:
            click.echo("⏭️  Skipping audio generation (script-only mode)")

        click.echo(f"✅ Project completed! Check: {crew_manager.project_dir}")
        click.echo(f"📁 Discussion files in: {crew_manager.discussion_dir}")

    except Exception as e:
        click.echo(f"❌ Error: {e}")
        raise click.Abort()


if __name__ == "__main__":
    main()
