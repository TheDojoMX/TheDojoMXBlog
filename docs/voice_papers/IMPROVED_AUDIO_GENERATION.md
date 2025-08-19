# Improved Audio Generation with Duration-Based Chunking

## Overview

The Voice Papers audio generation has been significantly improved to handle long scripts reliably. The new system addresses the issue where ElevenLabs API would fail when generating audio longer than 10 minutes.

## Key Features

### 1. **Duration-Based Chunking**
- Audio is automatically split into **5-6 minute chunks** regardless of model
- Each chunk contains approximately 18,000 characters
- Prevents API timeouts and failures on long scripts
- Maintains voice consistency across chunks using request stitching

### 2. **State Management & Recovery**
- Generation progress is saved after each chunk
- If the process fails, it can resume from where it left off
- Completed chunks are preserved and reused
- State files are stored in `.{filename}_state/` directories

### 3. **Cost Tracking & Reporting**
- Every API call is logged with character count and cost
- Detailed cost report generated after completion
- Shows cost breakdown per chunk
- Total cost calculation based on model pricing

### 4. **Improved Reliability**
- Automatic retry on timeouts (up to 3 attempts)
- Progressive backoff between retries
- Chunk-by-chunk processing with state saves
- Fallback audio stitching if pydub is not installed

## Usage

### Default Behavior (Improved Mode)
```bash
voice-papers document.pdf
```
- Uses duration-based chunking (5-6 min per chunk)
- Saves state for recovery
- Generates cost report
- Shows progress for each chunk

### Legacy Mode
```bash
voice-papers document.pdf --use-legacy-tts
```
- Uses original character limits (may fail on long scripts)
- No state management
- No cost tracking

## File Structure

When using improved mode, additional files are created:

```
project_name/
├── educational_script.txt         # The generated script
├── educational_lecture.mp3        # Final audio file
└── .educational_lecture_state/    # State directory
    ├── synthesis_state_xxxxx.json # Generation state
    ├── cost_report.txt           # Detailed cost breakdown
    └── chunks/                   # Individual audio chunks
        ├── chunk_000.mp3
        ├── chunk_001.mp3
        └── ...
```

## Cost Information

### Pricing (as of 2024)
- **Flash models**: $0.33 per 1M characters
- **Turbo models**: $0.50 per 1M characters  
- **Multilingual models**: $0.90 per 1M characters

### Example Cost Calculation
For a 20-minute educational lecture using flash model:
- ~4 chunks × 18,000 chars = 72,000 characters
- Cost: 72,000 / 1,000,000 × $0.33 = **$0.024**

## Recovery from Failures

If generation fails:

1. **Automatic Resume**: Simply run the same command again
   ```bash
   voice-papers document.pdf
   ```
   The system will detect existing chunks and continue from where it stopped.

2. **Check State**: View the state file to see progress
   ```bash
   cat project_name/.educational_lecture_state/synthesis_state_*.json
   ```

3. **View Cost Report**: Check generation costs
   ```bash
   cat project_name/.educational_lecture_state/cost_report.txt
   ```

## Troubleshooting

### "Audio generation failed after 10 minutes"
This is exactly what the improved mode prevents. Make sure you're NOT using `--use-legacy-tts`.

### "Warning: pydub not installed"
Audio will still be generated, but stitching may have small gaps. Install pydub for seamless audio:
```bash
pip install pydub
```

### "Chunk generation keeps failing"
1. Check your API key and quota
2. Try reducing chunk size by modifying `DURATION_BASED_LIMITS` in the code
3. Check network connectivity
4. Review the state file for specific error messages

## Benefits Over Legacy Mode

| Feature | Improved Mode | Legacy Mode |
|---------|---------------|-------------|
| Max script length | Unlimited | ~10 minutes |
| Failure recovery | ✅ Yes | ❌ No |
| Cost tracking | ✅ Yes | ❌ No |
| Progress visibility | ✅ Per chunk | ⚠️ Total only |
| API timeout handling | ✅ Automatic retry | ❌ Fails |
| Voice consistency | ✅ Request stitching | ✅ Request stitching |
| Chunk storage | ✅ Persistent | ❌ Memory only |

## Technical Details

### Character Limits
The improved synthesizer uses these limits for ~5-6 minute chunks:
- Flash/Turbo models: 18,000 characters (reduced from 39,500)
- Multilingual models: 9,500 characters (unchanged)

### Request Stitching
The system maintains voice consistency by:
- Tracking request IDs from previous chunks
- Passing up to 3 previous IDs to the API
- Ensuring smooth transitions between chunks

### State File Format
```json
{
  "job_id": "a1b2c3d4",
  "status": "completed",
  "total_chunks": 4,
  "completed_chunks": ["chunk_000", "chunk_001", "chunk_002", "chunk_003"],
  "total_characters": 72000,
  "total_cost": 0.02376,
  "model": "flash",
  "voice": "hectorip",
  "chunks_info": [...]
}
```

## Recommendations

1. **Always use improved mode** (default) for scripts longer than 5 minutes
2. **Install pydub** for better audio stitching: `pip install pydub`
3. **Check cost reports** to monitor API usage
4. **Keep state directories** until you're sure generation is complete
5. **Use --script-only** first to verify content before generating audio