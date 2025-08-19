# Direct Mode for Voice Papers

The direct mode allows you to quickly transform any text content into an educational script using only the Educational Writer agent, bypassing the full multi-agent discussion workflow.

## Usage

### From a text file:
```bash
uv run python -m voice_papers.cli your_text.txt --direct
```

### From stdin:
```bash
echo "Your text content here" | uv run python -m voice_papers.cli - --direct
```

### With custom options:
```bash
uv run python -m voice_papers.cli content.txt --direct \
  --language Spanish \
  --duration 5 \
  --technical-level technical \
  --tone casual
```

### Using --text-file option:
```bash
uv run python -m voice_papers.cli any_source --direct --text-file my_content.txt
```

## Options

All standard Voice Papers options work with direct mode:
- `--language`: Target language (default: Spanish)
- `--duration`: Target duration in minutes (1-60)
- `--technical-level`: simple, accessible, or technical
- `--tone`: academic, casual, humorous, or playful
- `--script-only`: Generate only the script without audio
- `--voice-provider`: elevenlabs or cartesia
- `--voice-id` / `--voice`: Voice selection options

## When to Use Direct Mode

Direct mode is ideal when:
- You have pre-processed or curated text content
- You want the fastest possible script generation
- You don't need multi-agent analysis and discussion
- You're iterating quickly on content transformation

## Workflow Comparison

### Default mode (full workflow):
PDF/URL → Text Extraction → Multi-Agent Discussion → Educational Writer → Voice Director → Audio

### Summary mode (`--summary`):
PDF/URL → Text Extraction → Chunking → Summary → Educational Writer → Audio

### Direct mode (`--direct`):
Text → Educational Writer → Audio

## Example

```bash
# Create a simple text file
cat > quantum_intro.txt << EOF
Quantum mechanics is the branch of physics that describes matter and energy at the smallest scales.
At this scale, particles exhibit wave-particle duality and can exist in superposition.
EOF

# Transform it into an educational script
uv run python -m voice_papers.cli quantum_intro.txt --direct --duration 3

# Or use stdin for quick tests
echo "AI is transforming how we work" | uv run python -m voice_papers.cli - --direct --duration 1
```

The Educational Writer will transform your content into an engaging, natural-sounding educational script following best practices for educational content creation.