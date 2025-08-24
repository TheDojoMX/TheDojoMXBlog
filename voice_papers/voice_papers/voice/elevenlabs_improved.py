"""Improved ElevenLabs synthesizer with better chunking, state management, and cost tracking."""

import os
import json
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from datetime import datetime
import hashlib
from elevenlabs import ElevenLabs

# Try to import pydub for better audio stitching, fallback to direct concatenation
try:
    from pydub import AudioSegment

    HAS_PYDUB = True
except ImportError:
    HAS_PYDUB = False
    print("Warning: pydub not installed. Audio stitching will use fallback method.")
    print("Install with: pip install pydub")


class ElevenLabsImprovedSynthesizer:
    """Improved ElevenLabs voice synthesizer with duration-based chunking and state management."""

    # Model mapping from short names to full ElevenLabs model IDs
    MODEL_MAP = {
        "flash": "eleven_flash_v2_5",  # Fastest model
        "turbo": "eleven_turbo_v2_5",  # Fast model
        "v3": "eleven_v3",  # V3 model
        "multilingual": "eleven_multilingual_v2",  # Multilingual support
        "english": "eleven_monolingual_v1",  # Best quality for English
    }

    # Character limits based on target audio duration (5-6 minutes per chunk)
    # Calculated based on average speech rate of 150-180 words/minute
    # and average word length of 5-6 characters + spaces
    DURATION_BASED_LIMITS = {
        "eleven_flash_v2_5": 18000,  # ~5-6 minutes of audio (reduced from 39500)
        "eleven_flash_v2": 18000,  # ~5-6 minutes of audio (reduced from 29500)
        "eleven_turbo_v2_5": 18000,  # ~5-6 minutes of audio
        "eleven_turbo_v2": 18000,  # ~5-6 minutes of audio
        "eleven_multilingual_v2": 9500,  # Keep original (already ~3 minutes)
        "eleven_multilingual_v1": 9500,  # Keep original
        "eleven_v3": 2500,  # Keep original
        "eleven_monolingual_v1": 9500,  # Keep original
        "default": 9500,
    }

    # Voice mapping
    VOICE_MAP = {
        "ana": "m7yTemJqdIqrcNleANfX",  # Ana - Spanish female voice
        # "hectorip": "njx36XSgu0GyZ0cOjzj0",  # HectorIP - Custom voice (old)
        "hectorip": "aCSsHgeLIBCZsdlBEwpH",  # HectorIP - Custom voice
        "rachel": "sDh3eviBhiuHKi0MjTNq",  # Rachel - English female voice (default)
    }

    # Default voice settings
    DEFAULT_VOICE_SETTINGS = {
        "stability": 0.5,
        "similarity_boost": 0.8,
        "style": 0.0,
        "use_speaker_boost": True,
    }

    # ElevenLabs pricing per 1000 characters (as of 2024)
    PRICING_PER_1K_CHARS = {
        "eleven_flash_v2_5": 0.00033,  # $0.33 per 1M chars
        "eleven_flash_v2": 0.00033,
        "eleven_turbo_v2_5": 0.0005,  # $0.50 per 1M chars
        "eleven_turbo_v2": 0.0005,
        "eleven_multilingual_v2": 0.0009,  # $0.90 per 1M chars
        "eleven_multilingual_v1": 0.0009,
        "eleven_v3": 0.0009,
        "eleven_monolingual_v1": 0.0009,
        "default": 0.0009,
    }

    # Note: Actual credits are returned by the API in the 'character-cost' header
    # Flash models have discounted pricing (~0.5 credits per character)
    # The API will return the actual credits charged

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY not found")
        self.client = ElevenLabs(api_key=self.api_key, timeout=None)

    def synthesize_with_state(
        self,
        text: str,
        output_path: Path,
        voice_id: Optional[str] = None,
        model: str = "flash",
        voice_name: Optional[str] = None,
        stability: Optional[float] = None,
        similarity_boost: Optional[float] = None,
        style: Optional[float] = None,
        use_speaker_boost: Optional[bool] = None,
        resume: bool = True,
    ) -> Tuple[bool, Dict]:
        """
        Synthesize text with state management for recovery and cost tracking.

        Returns:
            Tuple of (success: bool, stats: dict with cost and chunk info)
        """
        # Create state directory
        state_dir = output_path.parent / f".{output_path.stem}_state"
        state_dir.mkdir(parents=True, exist_ok=True)

        # Generate unique ID for this synthesis job
        job_id = hashlib.md5(f"{text[:100]}{output_path}".encode()).hexdigest()[:8]
        state_file = state_dir / f"synthesis_state_{job_id}.json"
        chunks_dir = state_dir / "chunks"
        chunks_dir.mkdir(exist_ok=True)

        # Load or initialize state
        state = (
            self._load_state(state_file)
            if resume and state_file.exists()
            else {
                "job_id": job_id,
                "status": "started",
                "total_chunks": 0,
                "completed_chunks": [],
                "failed_chunks": [],
                "request_ids": [],
                "total_characters": len(text),
                "total_cost": 0.0,
                "total_credits": 0,
                "model": model,
                "voice": voice_name or voice_id,
                "started_at": datetime.now().isoformat(),
                "chunks_info": [],
            }
        )

        try:
            # Determine voice
            if voice_name:
                used_voice = self.VOICE_MAP.get(voice_name, self.VOICE_MAP["rachel"])
                print(f"Using voice: {voice_name} ({used_voice})")
            elif voice_id:
                used_voice = voice_id
                print(f"Using voice ID: {voice_id}")
            else:
                used_voice = self.VOICE_MAP["rachel"]
                print(f"Using default voice: rachel ({used_voice})")

            # Map model
            model_id = self.MODEL_MAP.get(model, self.MODEL_MAP["flash"])
            print(f"Using ElevenLabs model: {model} ({model_id})")

            # Get character limit for duration-based chunking
            max_chars = self.DURATION_BASED_LIMITS.get(
                model_id, self.DURATION_BASED_LIMITS["default"]
            )
            print(f"Using duration-based limit: {max_chars} chars (~5-6 min audio)")

            # Prepare voice settings
            voice_settings = {
                "stability": stability
                if stability is not None
                else self.DEFAULT_VOICE_SETTINGS["stability"],
                "similarity_boost": similarity_boost
                if similarity_boost is not None
                else self.DEFAULT_VOICE_SETTINGS["similarity_boost"],
                "style": style
                if style is not None
                else self.DEFAULT_VOICE_SETTINGS["style"],
                "use_speaker_boost": use_speaker_boost
                if use_speaker_boost is not None
                else self.DEFAULT_VOICE_SETTINGS["use_speaker_boost"],
                "ttd_stability": 0.5,
            }

            # Split text into chunks
            chunks = self._split_text_into_chunks(text, max_chars)
            state["total_chunks"] = len(chunks)

            print(
                f"Text split into {len(chunks)} chunks for ~{len(chunks) * 5}-{len(chunks) * 6} minutes total"
            )

            # Process chunks
            for i, chunk in enumerate(chunks):
                chunk_id = f"chunk_{i:03d}"

                # Skip if already completed
                if chunk_id in state["completed_chunks"]:
                    print(f"Skipping already completed {chunk_id}")
                    continue

                chunk_path = chunks_dir / f"{chunk_id}.mp3"
                chunk_info = {
                    "id": chunk_id,
                    "index": i,
                    "characters": len(chunk),
                    "credits": 0,  # Will be updated with actual from API
                    "path": str(chunk_path),
                    "status": "processing",
                }

                print(
                    f"\nProcessing {chunk_id} ({i + 1}/{len(chunks)}) - {len(chunk)} chars (estimated)"
                )

                # Synthesize chunk with retries
                success, request_id, cost, credits_used = self._synthesize_chunk(
                    chunk,
                    chunk_path,
                    used_voice,
                    model_id,
                    voice_settings,
                    state["request_ids"][-3:] if state["request_ids"] else None,
                )

                if success:
                    chunk_info["status"] = "completed"
                    chunk_info["request_id"] = request_id
                    chunk_info["cost"] = cost
                    chunk_info["credits"] = credits_used
                    chunk_info["estimated_credits"] = len(
                        chunk
                    )  # Store original estimate for comparison
                    state["completed_chunks"].append(chunk_id)
                    if request_id:
                        state["request_ids"].append(request_id)
                    state["total_cost"] += cost
                    state["total_credits"] += credits_used
                    print(
                        f"✅ {chunk_id} completed - Cost: ${cost:.4f} | Credits: {credits_used:,} actual (estimated: {len(chunk):,})"
                    )
                else:
                    chunk_info["status"] = "failed"
                    state["failed_chunks"].append(chunk_id)
                    print(f"❌ {chunk_id} failed")

                state["chunks_info"].append(chunk_info)

                # Save state after each chunk
                self._save_state(state_file, state)

                # Delay between chunks
                if i < len(chunks) - 1 and success:
                    delay = 2 if model == "flash" else 5
                    print(f"Waiting {delay}s before next chunk...")
                    time.sleep(delay)

            # Stitch chunks together
            if state["completed_chunks"]:
                print(
                    f"\n🔗 Stitching {len(state['completed_chunks'])} audio chunks..."
                )
                success = self._stitch_chunks(
                    chunks_dir, state["completed_chunks"], output_path
                )

                if success:
                    state["status"] = "completed"
                    state["completed_at"] = datetime.now().isoformat()
                    print(f"✅ Audio saved to: {output_path}")
                    print(
                        f"💰 Total cost: ${state['total_cost']:.4f} | Credits used: {state['total_credits']:,} (actual from API)"
                    )
                    print(
                        f"⏱️  Estimated duration: {len(state['completed_chunks']) * 5}-{len(state['completed_chunks']) * 6} minutes"
                    )
                else:
                    state["status"] = "failed_stitching"
                    return False, state
            else:
                state["status"] = "failed_no_chunks"
                return False, state

            # Save final state
            self._save_state(state_file, state)

            # Create cost report
            self._create_cost_report(state_dir, state)

            return True, state

        except Exception as e:
            print(f"❌ Synthesis failed: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
            self._save_state(state_file, state)
            return False, state

    def _synthesize_chunk(
        self,
        text: str,
        output_path: Path,
        voice_id: str,
        model_id: str,
        voice_settings: Dict,
        previous_request_ids: Optional[List[str]] = None,
    ) -> Tuple[bool, Optional[str], float, int]:
        """Synthesize a single chunk with retries. Returns (success, request_id, cost, credits)."""
        max_retries = 3

        for attempt in range(max_retries):
            try:
                # Calculate estimated cost and credits (will be updated with actual from API)
                char_count = len(text)
                cost = (char_count / 1000) * self.PRICING_PER_1K_CHARS.get(
                    model_id, self.PRICING_PER_1K_CHARS["default"]
                )
                credits = char_count  # Initial estimate, API will return actual
                print(f"Voice settings: {voice_settings}")
                # Make API call
                with self.client.text_to_speech.with_raw_response.convert(
                    voice_id=voice_id,
                    text=text,
                    model_id=model_id,
                    voice_settings=voice_settings,
                    output_format="mp3_44100_128",
                    previous_request_ids=previous_request_ids if model_id != "eleven_v3" else None,
                ) as response:
                    # Extract various useful headers from API response
                    headers = response._response.headers
                    request_id = headers.get("request-id")
                    history_item_id = headers.get("history-item-id")
                    tts_latency = headers.get("tts-latency-ms")

                    # Extract actual character cost from API (credits used)
                    actual_credits = headers.get("character-cost")
                    if actual_credits:
                        actual_credits = int(actual_credits)
                        # Recalculate cost based on actual credits charged
                        cost = (actual_credits / 1000) * self.PRICING_PER_1K_CHARS.get(
                            model_id, self.PRICING_PER_1K_CHARS["default"]
                        )
                        # Log if actual credits differ significantly from estimate
                        if (
                            abs(actual_credits - credits) > credits * 0.1
                        ):  # More than 10% difference
                            discount_rate = (credits - actual_credits) / credits * 100
                            print(
                                f"  💸 Credit discount applied: {discount_rate:.1f}% ({credits} estimated → {actual_credits} actual)"
                            )
                    else:
                        # Fallback to calculated credits if header not available
                        actual_credits = credits

                    # Log performance info if available
                    if tts_latency:
                        print(f"  ⏱️  TTS latency: {tts_latency}ms")

                    # Save audio
                    with open(output_path, "wb") as f:
                        for chunk in response.data:
                            f.write(chunk)

                    return True, request_id, cost, actual_credits

            except Exception as e:
                error_msg = str(e).lower()
                if "timeout" in error_msg or "timed out" in error_msg:
                    if attempt < max_retries - 1:
                        wait_time = 10 * (attempt + 1)
                        print(
                            f"  Timeout on attempt {attempt + 1}, waiting {wait_time}s..."
                        )
                        time.sleep(wait_time)
                    else:
                        print(f"  Failed after {max_retries} timeout attempts")
                        return False, None, 0.0, 0
                else:
                    print(f"  Non-timeout error: {str(e)}")
                    return False, None, 0.0, 0

        return False, None, 0.0, 0

    def _stitch_chunks(
        self, chunks_dir: Path, chunk_ids: List[str], output_path: Path
    ) -> bool:
        """Stitch audio chunks together."""
        if HAS_PYDUB:
            try:
                combined = AudioSegment.empty()

                for chunk_id in sorted(chunk_ids):
                    chunk_path = chunks_dir / f"{chunk_id}.mp3"
                    if chunk_path.exists():
                        audio = AudioSegment.from_mp3(chunk_path)
                        combined += audio
                    else:
                        print(f"Warning: Missing chunk {chunk_id}")

                # Export combined audio
                combined.export(output_path, format="mp3", bitrate="128k")
                return True

            except Exception as e:
                print(f"Pydub stitching failed: {e}")
                # Fall through to direct concatenation

        # Direct concatenation (works but may have small gaps between chunks)
        try:
            print("Using direct file concatenation for audio stitching...")
            with open(output_path, "wb") as outfile:
                for chunk_id in sorted(chunk_ids):
                    chunk_path = chunks_dir / f"{chunk_id}.mp3"
                    if chunk_path.exists():
                        with open(chunk_path, "rb") as infile:
                            outfile.write(infile.read())
            return True
        except Exception as e:
            print(f"Direct concatenation failed: {e}")
            return False

    def _split_text_into_chunks(self, text: str, max_chars: int) -> List[str]:
        """Split text into chunks that respect sentence boundaries."""
        chunks = []
        current_chunk = ""

        # Split by paragraphs first
        paragraphs = text.split("\n\n")

        for paragraph in paragraphs:
            if not paragraph.strip():
                continue

            # If adding this paragraph would exceed limit, save current chunk
            if len(current_chunk) + len(paragraph) > max_chars and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""

            # If single paragraph is too long, split by sentences
            if len(paragraph) > max_chars:
                sentences = paragraph.split(". ")
                for sentence in sentences:
                    if (
                        len(current_chunk) + len(sentence) + 2 > max_chars
                        and current_chunk
                    ):
                        chunks.append(current_chunk.strip())
                        current_chunk = ""
                    current_chunk += sentence + ". "
            else:
                current_chunk += paragraph + "\n\n"

        # Add remaining text
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def _load_state(self, state_file: Path) -> Dict:
        """Load synthesis state from file."""
        try:
            with open(state_file, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Could not load state: {e}")
            return {}

    def _save_state(self, state_file: Path, state: Dict):
        """Save synthesis state to file."""
        try:
            with open(state_file, "w") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"Could not save state: {e}")

    def _create_cost_report(self, state_dir: Path, state: Dict):
        """Create a detailed cost report."""
        report_path = state_dir / "cost_report.txt"

        try:
            with open(report_path, "w") as f:
                f.write("ElevenLabs Synthesis Cost Report\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Job ID: {state['job_id']}\n")
                f.write(f"Started: {state['started_at']}\n")
                f.write(f"Completed: {state.get('completed_at', 'N/A')}\n")
                f.write(f"Status: {state['status']}\n\n")

                f.write("Summary:\n")
                f.write(f"- Total characters: {state['total_characters']:,}\n")
                f.write(f"- Total chunks: {state['total_chunks']}\n")
                f.write(f"- Completed chunks: {len(state['completed_chunks'])}\n")
                f.write(f"- Failed chunks: {len(state['failed_chunks'])}\n")
                f.write(f"- Model used: {state['model']}\n")
                f.write(f"- Voice used: {state['voice']}\n\n")

                f.write("Cost Breakdown:\n")
                f.write(f"- Total cost: ${state['total_cost']:.4f}\n")
                f.write(
                    f"- Total credits used: {state.get('total_credits', 0):,} (actual API charge)\n"
                )
                f.write(
                    f"- Cost per 1K chars: ${self.PRICING_PER_1K_CHARS.get(self.MODEL_MAP.get(state['model'], 'default'), 0.0009):.4f}\n"
                )
                credits_per_char = (
                    state.get("total_credits", 0) / state["total_characters"]
                    if state["total_characters"] > 0
                    else 0
                )
                f.write(f"- Average credits per character: {credits_per_char:.2f}\n")
                if credits_per_char < 0.7:
                    f.write(
                        f"  👉 You're getting a discount! Flash models charge ~{credits_per_char:.2f} credits/char\n"
                    )
                f.write("\n")

                if state.get("chunks_info"):
                    f.write("Chunk Details:\n")
                    for chunk in state["chunks_info"]:
                        credits_actual = chunk.get("credits", chunk["characters"])
                        credits_est = chunk.get(
                            "estimated_credits", chunk["characters"]
                        )
                        f.write(
                            f"- {chunk['id']}: {chunk['characters']} chars, "
                            f"${chunk.get('cost', 0.0):.4f}, "
                            f"{credits_actual:,} credits"
                        )
                        if credits_actual != credits_est:
                            f.write(
                                f" (saved {credits_est - credits_actual:,} credits)"
                            )
                        f.write(f", status: {chunk['status']}\n")

                # Estimate audio duration
                completed_chunks = len(state["completed_chunks"])
                f.write(
                    f"\nEstimated Audio Duration: {completed_chunks * 5}-{completed_chunks * 6} minutes\n"
                )

                # Credit usage summary
                f.write(f"\nCredit Usage Summary:\n")
                if completed_chunks > 0:
                    avg_credits_per_min = int(
                        state.get("total_credits", 0) / (completed_chunks * 5.5)
                    )
                    f.write(
                        f"- Average credits per minute of audio: {avg_credits_per_min:,}\n"
                    )

                    # Calculate savings if using Flash model
                    estimated_credits = sum(
                        c.get("estimated_credits", c["characters"])
                        for c in state.get("chunks_info", [])
                    )
                    actual_credits = state.get("total_credits", 0)
                    if actual_credits < estimated_credits:
                        savings = estimated_credits - actual_credits
                        savings_percent = savings / estimated_credits * 100
                        f.write(
                            f"- Total credits saved: {savings:,} ({savings_percent:.1f}% discount)\n"
                        )
                        f.write(
                            f"- Cost savings: ${(savings / 1000 * self.PRICING_PER_1K_CHARS.get(self.MODEL_MAP.get(state['model'], 'default'), 0.0009)):.4f}\n"
                        )

                f.write(
                    f"\nNote: Your remaining credits depend on your ElevenLabs plan.\n"
                )

            print(f"📊 Cost report saved to: {report_path}")

        except Exception as e:
            print(f"Could not create cost report: {e}")


# For backward compatibility, update the existing synthesizer
def create_improved_synthesizer():
    """Create an improved ElevenLabs synthesizer instance."""
    return ElevenLabsImprovedSynthesizer()
