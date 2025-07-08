# Credit Tracking Update for ElevenLabs

## Overview

The ElevenLabs audio generation now accurately tracks **actual credits charged** by the API, not just estimates. This is especially important for Flash models which offer discounted pricing.

## Key Improvements

### 1. Actual Credit Usage from API

The system now reads the `character-cost` header from the ElevenLabs API response, which contains the **actual credits charged** for each request.

**Example:**
- Input text: 54 characters
- Estimated credits: 54 (1 credit per character)
- **Actual credits charged: 27** (Flash model discount)
- Savings: 50%

### 2. Credit Information Display

When generating audio, you'll see:

```
Processing chunk_000 (1/4) - 18000 chars (estimated)
  💸 Credit discount applied: 50.0% (18000 estimated → 9000 actual)
  ⏱️  TTS latency: 134ms
✅ chunk_000 completed - Cost: $0.0030 | Credits: 9,000 actual (estimated: 18,000)
```

### 3. Enhanced Cost Report

The cost report now includes:

```
Cost Breakdown:
- Total cost: $0.0240
- Total credits used: 72,000 (actual API charge)
- Average credits per character: 0.50
  👉 You're getting a discount! Flash models charge ~0.50 credits/char

Chunk Details:
- chunk_000: 18000 chars, $0.0060, 9,000 credits (saved 9,000 credits), status: completed
- chunk_001: 18000 chars, $0.0060, 9,000 credits (saved 9,000 credits), status: completed

Credit Usage Summary:
- Average credits per minute of audio: 3,273
- Total credits saved: 72,000 (50.0% discount)
- Cost savings: $0.0240
```

## API Headers Used

The system now extracts these headers from ElevenLabs API responses:

- **`character-cost`**: Actual credits charged (most important!)
- **`request-id`**: Unique request identifier
- **`history-item-id`**: Audio item ID in your history
- **`tts-latency-ms`**: Generation time in milliseconds

## Pricing & Credits

### Current Models (2024)

| Model | Price per 1M chars | Credits per char | Typical discount |
|-------|-------------------|------------------|------------------|
| Flash | $0.33 | ~0.5 | 50% off |
| Turbo | $0.50 | ~0.7-0.8 | 20-30% off |
| Multilingual | $0.90 | 1.0 | None |
| English | $0.90 | 1.0 | None |

### Understanding Credits

- **1 credit = 1 character** (base rate)
- Flash models use advanced compression: ~0.5 credits per character
- Turbo models have moderate discount: ~0.7-0.8 credits per character
- Your actual usage depends on the model and content

## Benefits

1. **Accurate Cost Tracking**: Know exactly what you're being charged
2. **Discount Visibility**: See how much you're saving with Flash/Turbo models
3. **Better Planning**: Understand your credit usage patterns
4. **Performance Metrics**: See TTS latency for each chunk

## Example Output

For a 20-minute educational lecture using Flash model:

```
💰 Total cost: $0.0120 | Credits used: 36,000 (actual from API)
⏱️  Estimated duration: 20-24 minutes

Credit Usage Summary:
- Average credits per minute of audio: 1,800
- Total credits saved: 36,000 (50.0% discount)
- Cost savings: $0.0120
```

## Technical Implementation

The key change is in `_synthesize_chunk()`:

```python
# Extract actual character cost from API (credits used)
actual_credits = headers.get("character-cost")
if actual_credits:
    actual_credits = int(actual_credits)
    # Recalculate cost based on actual credits charged
    cost = (actual_credits / 1000) * PRICING_PER_1K_CHARS[model_id]
```

This ensures all credit and cost calculations are based on what ElevenLabs actually charges, not estimates.