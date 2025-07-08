# Technical Documentation

## Architecture

Voice Papers is built with a modular architecture consisting of:

### Core Components

1. **Agent System (`voice_papers.agents`)**
   - `roles.py`: Defines agent roles and specializations
   - `crew_manager.py`: Manages CrewAI orchestration

2. **Voice Synthesis (`voice_papers.voice`)**
   - `synthesizer.py`: Abstract interface and provider implementations

3. **Utilities (`voice_papers.utils`)**
   - `pdf_reader.py`: PDF text extraction

4. **CLI (`voice_papers.cli`)**
   - Command-line interface implementation

### Dependencies

- **CrewAI**: Multi-agent orchestration framework
- **OpenAI**: LLM backend (requires o3 model)
- **ElevenLabs**: Primary voice synthesis provider
- **Cartesia**: Alternative voice synthesis provider
- **PyPDF**: PDF text extraction
- **Click**: CLI framework

## Agent Workflow

### 1. Paper Analysis
The `CrewManager` analyzes the paper content to determine appropriate agent roles:

```python
def _detect_topic(self, text: str) -> str:
    # Simple keyword-based topic detection
    # Returns topic classification (AI, General, etc.)
```

### 2. Dynamic Team Creation
Based on the detected topic, creates specialized agents:

```python
def get_roles_for_topic(topic: str, llm: LLM) -> List[Agent]:
    base_roles = get_base_roles(llm)
    if topic == "AI":
        return base_roles + get_ai_specific_roles(llm)
    return base_roles
```

### 3. Task Execution
Four main tasks are executed sequentially:

1. **Initial Analysis**: Each agent analyzes the paper from their perspective
2. **Discussion**: Agents engage in multi-perspective dialogue
3. **Script Writing**: Podcast writer creates engaging script
4. **Voice Optimization**: Voice director optimizes for audio delivery

### 4. Output Generation
Results are saved in structured format:

```
projects/paper_name/
├── discussion/
│   ├── crew_structure.json    # Agent configuration
│   ├── final_result.txt       # Complete output
│   └── task_*_output.txt      # Individual task results
├── podcast_script.txt         # Final script
└── podcast.mp3                # Generated audio
```

## Voice Synthesis

### Provider Interface

```python
class VoiceSynthesizer(ABC):
    @abstractmethod
    def synthesize(self, text: str, output_path: Path, voice_id: Optional[str] = None) -> bool:
        pass
```

### ElevenLabs Implementation

Uses the official ElevenLabs Python SDK:

```python
def synthesize(self, text: str, output_path: Path, voice_id: Optional[str] = None) -> bool:
    audio = self.client.generate(
        text=text,
        voice=voice_id or "21m00Tcm4TlvDq8ikWAM",
        model="eleven_monolingual_v1"
    )
    # Stream and save audio
```

### Cartesia Implementation

HTTP API integration (placeholder implementation):

```python
def synthesize(self, text: str, output_path: Path, voice_id: Optional[str] = None) -> bool:
    response = requests.post(
        "https://api.cartesia.ai/tts/stream",
        headers=headers,
        json=data
    )
    # Save response content
```

## Configuration Management

Environment variables are managed through `config.py`:

```python
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "o3-2025-04-16")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")
```

## Error Handling

- PDF reading errors are caught and reported
- Voice synthesis failures are handled gracefully
- CrewAI execution errors are propagated with context
- CLI provides user-friendly error messages

## Performance Considerations

- CrewAI execution can be time-intensive (several minutes per paper)
- Voice synthesis time depends on text length and provider
- Large PDFs may require chunking for optimal processing
- Project files are saved incrementally to prevent data loss

## Extension Points

### Adding New Voice Providers

1. Implement `VoiceSynthesizer` interface
2. Add provider to `get_synthesizer()` factory function
3. Update CLI options

### Adding New Agent Roles

1. Define roles in `roles.py`
2. Add topic detection logic in `crew_manager.py`
3. Update task creation for new workflows

### Supporting New Document Types

1. Create new reader in `utils/`
2. Update CLI to accept new file types
3. Modify content extraction pipeline

## Testing

Test structure (to be implemented):

```
tests/
├── test_agents/
├── test_voice/
├── test_utils/
└── test_cli/
```

## Deployment

The application can be deployed as:

1. **Standalone CLI**: Direct installation via pip/uv
2. **Docker Container**: Containerized deployment
3. **Web Service**: FastAPI wrapper around core functionality
4. **Cloud Function**: Serverless paper processing