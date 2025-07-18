"""Voice synthesis providers."""

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Tuple, Dict
import requests
from elevenlabs import ElevenLabs
import time
from ..config import ELEVENLABS_API_KEY, CARTESIA_API_KEY
from .elevenlabs_improved import ElevenLabsImprovedSynthesizer


class VoiceSynthesizer(ABC):
    """Abstract base class for voice synthesizers."""

    @abstractmethod
    def synthesize(
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
    ) -> bool:
        """Synthesize text to speech and save to file."""
        pass


class ElevenLabsSynthesizer(VoiceSynthesizer):
    """ElevenLabs voice synthesizer with configurable models and voice settings."""

    # Model mapping from short names to full ElevenLabs model IDs
    MODEL_MAP = {
        "flash": "eleven_flash_v2_5",  # Fastest model
        "turbo": "eleven_turbo_v2_5",  # Fast model
        "v3": "eleven_v3",  # V3 model
        "multilingual": "eleven_multilingual_v2",  # Multilingual support
        "english": "eleven_monolingual_v1",  # Best quality for English
    }

    # Character limits per model (with safety buffer)
    # For improved synthesizer, these are overridden with duration-based limits
    CHARACTER_LIMITS = {
        "eleven_flash_v2_5": 39500,  # 40,000 with buffer (original)
        "eleven_flash_v2": 29500,  # 30,000 with buffer (original)
        "eleven_turbo_v2_5": 39500,  # 40,000 with buffer (original)
        "eleven_turbo_v2": 29500,  # 30,000 with buffer (original)
        "eleven_multilingual_v2": 9500,  # 10,000 with buffer
        "eleven_multilingual_v1": 9500,  # 10,000 with buffer
        "eleven_v3": 9500,  # 10,000 with buffer
        "eleven_monolingual_v1": 9500,  # 10,000 with buffer (legacy)
        # Add fallback for any unknown models
        "default": 9500,
    }
    
    # Option to use improved synthesizer with duration-based chunking
    USE_IMPROVED_SYNTHESIZER = os.getenv("ELEVENLABS_USE_IMPROVED", "true").lower() == "true"

    # Voice mapping from short names to ElevenLabs voice IDs
    VOICE_MAP = {
        "ana": "m7yTemJqdIqrcNleANfX",  # Ana - Spanish female voice
        "hectorip": "njx36XSgu0GyZ0cOjzj0",  # HectorIP - Custom voice
        "rachel": "sDh3eviBhiuHKi0MjTNq",  # Rachel - English female voice (default)
    }

    # Default voice settings for optimal quality and stability
    DEFAULT_VOICE_SETTINGS = {
        "stability": 0.65,  # Higher stability for more consistent output
        "similarity_boost": 0.8,  # Strong similarity to original voice
        "style": 0.0,  # Minimal style exaggeration to avoid instability
        "use_speaker_boost": True,  # Boost similarity to original speaker
    }

    def __init__(self):
        if not ELEVENLABS_API_KEY:
            raise ValueError("ELEVENLABS_API_KEY not found in environment")
        self.client = ElevenLabs(api_key=ELEVENLABS_API_KEY, timeout=None)

    def synthesize(
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
    ) -> bool:
        """Synthesize text using ElevenLabs with configurable model, voice, and quality settings."""
        # Use improved synthesizer if enabled (default)
        if self.USE_IMPROVED_SYNTHESIZER:
            print("🚀 Using improved ElevenLabs synthesizer with duration-based chunking")
            improved_synth = ElevenLabsImprovedSynthesizer(ELEVENLABS_API_KEY)
            success, stats = improved_synth.synthesize_with_state(
                text=text,
                output_path=output_path,
                voice_id=voice_id,
                model=model,
                voice_name=voice_name,
                stability=stability,
                similarity_boost=similarity_boost,
                style=style,
                use_speaker_boost=use_speaker_boost,
                resume=True
            )
            return success
        
        # Original implementation
        try:
            # Determine voice to use: voice_name (mapped) > voice_id (direct) > default
            if voice_name:
                used_voice = self.VOICE_MAP.get(voice_name, self.VOICE_MAP["rachel"])
                print(f"Using voice: {voice_name} ({used_voice})")
            elif voice_id:
                used_voice = voice_id
                print(f"Using voice ID: {voice_id}")
            else:
                used_voice = self.VOICE_MAP["rachel"]  # Default to rachel
                print(f"Using default voice: rachel ({used_voice})")

            # Map short model name to full model ID
            model_id = self.MODEL_MAP.get(model, self.MODEL_MAP["flash"])
            print(f"Using ElevenLabs model: {model} ({model_id})")

            # Prepare voice settings with custom values or defaults
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
            }

            print(
                f"Voice settings: stability={voice_settings['stability']:.2f}, "
                f"similarity_boost={voice_settings['similarity_boost']:.2f}, "
                f"style={voice_settings['style']:.2f}, "
                f"use_speaker_boost={voice_settings['use_speaker_boost']}"
            )

            # Get character limit for the specific model
            max_chars = self.CHARACTER_LIMITS.get(
                model_id, self.CHARACTER_LIMITS["default"]
            )
            print(f"Using character limit: {max_chars} for model {model_id}")
            audio_chunks = []

            if len(text) <= max_chars:
                # Text is short enough, synthesize directly
                print(
                    f"Text length ({len(text)} chars) within limit, synthesizing directly"
                )
                audio = self.client.text_to_speech.convert(
                    voice_id=used_voice,
                    text=text,
                    model_id=model_id,
                    voice_settings=voice_settings,
                    output_format="mp3_44100_128",  # High quality output
                )
                audio_chunks.append(audio)
            else:
                # Split text into chunks
                chunks = self._split_text_into_chunks(text, max_chars)
                print(
                    f"Text too long ({len(text)} chars), splitting into {len(chunks)} chunks (max {max_chars} chars per chunk)"
                )

                # Track request IDs for stitching (max 3 as per ElevenLabs API)
                request_ids = []

                for i, chunk in enumerate(chunks):
                    print(f"Synthesizing chunk {i+1}/{len(chunks)}...")

                    # Add retry logic for timeouts
                    max_retries = 3
                    for attempt in range(max_retries):
                        try:
                            # Use with_raw_response to get request-id from headers
                            with self.client.text_to_speech.with_raw_response.convert(
                                voice_id=used_voice,
                                text=chunk,
                                model_id=model_id,
                                voice_settings=voice_settings,
                                output_format="mp3_44100_128",  # High quality output
                                previous_request_ids=request_ids[-3:]
                                if request_ids
                                else None,  # Max 3 IDs
                            ) as response:
                                # Extract request-id from headers for stitching
                                request_id = response._response.headers.get(
                                    "request-id"
                                )
                                if request_id:
                                    request_ids.append(request_id)
                                    print(
                                        f"✅ Chunk {i+1} generated with request-id: {request_id}"
                                    )
                                else:
                                    print(f"⚠️  No request-id received for chunk {i+1}")

                                # Get audio data from response and create iterable wrapper
                                audio_data = response.data
                                audio_chunks.append(audio_data)
                            break
                        except Exception as e:
                            error_msg = str(e).lower()
                            if "timeout" in error_msg or "timed out" in error_msg:
                                if attempt < max_retries - 1:
                                    wait_time = 10 * (
                                        attempt + 1
                                    )  # Longer wait for timeouts: 10, 20, 30 seconds
                                    print(
                                        f"Timeout on attempt {attempt + 1}, waiting {wait_time}s before retry..."
                                    )
                                    time.sleep(wait_time)
                                else:
                                    print(
                                        f"❌ Failed after {max_retries} timeout attempts"
                                    )
                                    raise e
                            else:
                                # Non-timeout errors, fail immediately
                                print(f"❌ Non-timeout error: {str(e)[:100]}...")
                                raise e

                    # Add delay between chunks to avoid rate limiting
                    # (shorter delay for flash model, longer for quality models)
                    if i < len(chunks) - 1:
                        delay = 2 if model == "flash" else 5
                        print(f"Waiting {delay} seconds before next chunk...")
                        time.sleep(delay)

                # Log stitching summary
                if len(request_ids) > 1:
                    print(
                        f"🔗 Request stitching used: {len(request_ids)} chunks linked for better continuity"
                    )

            # Save all audio chunks to file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                for audio_chunk in audio_chunks:
                    for chunk in audio_chunk:
                        f.write(chunk)

            print(f"✅ Audio saved successfully to: {output_path}")
            return True
        except Exception as e:
            print(f"❌ ElevenLabs synthesis failed: {e}")
            return False

    def _split_text_into_chunks(self, text: str, max_chars: int) -> list[str]:
        """Split text into chunks that respect sentence boundaries."""
        chunks = []
        current_chunk = ""

        # Split by paragraphs first, then sentences
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
                    if len(current_chunk) + len(sentence) > max_chars and current_chunk:
                        chunks.append(current_chunk.strip())
                        current_chunk = ""
                    current_chunk += sentence + ". "
            else:
                current_chunk += paragraph + "\n\n"

        # Add remaining text
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks


class CartesiaSynthesizer(VoiceSynthesizer):
    """Cartesia voice synthesizer."""

    def __init__(self):
        if not CARTESIA_API_KEY:
            raise ValueError("CARTESIA_API_KEY not found in environment")
        self.api_key = CARTESIA_API_KEY

    def synthesize(
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
    ) -> bool:
        """Synthesize text using Cartesia. Voice settings parameters are ignored for Cartesia."""
        try:
            # Placeholder implementation - adjust based on Cartesia API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            data = {
                "text": text,
                "voice_id": voice_id or "default",
                "output_format": "mp3",
            }

            # Note: This is a placeholder URL - replace with actual Cartesia endpoint
            response = requests.post(
                "https://api.cartesia.ai/tts/stream", headers=headers, json=data
            )

            if response.status_code == 200:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(response.content)
                return True

            return False
        except Exception as e:
            print(f"Cartesia synthesis failed: {e}")
            return False


def get_synthesizer(provider: str = "elevenlabs") -> VoiceSynthesizer:
    """Get a voice synthesizer instance."""
    if provider.lower() == "elevenlabs":
        return ElevenLabsSynthesizer()
    elif provider.lower() == "cartesia":
        return CartesiaSynthesizer()
    else:
        raise ValueError(f"Unknown provider: {provider}")
