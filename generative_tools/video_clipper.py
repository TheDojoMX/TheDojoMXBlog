#!/usr/bin/env python3
"""
Video Clipper - Generador de clips verticales a partir de videos largos

Convierte videos largos horizontales en clips cortos verticales optimizados para TikTok/Instagram.
Incluye generación automática de descripciones para cada clip.
"""

import os
import json
import math
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
import begin
from dotenv import load_dotenv
from openai import OpenAI

# Importar nuestro transcriptor existente
from video_transcriber import (
    transcribe_video,
    transcribe_audio_with_openai_whisper,
    extract_audio_from_video,
)

# Importar funciones del generador de descripciones
import google.generativeai as genai
import anthropic
from slugify import slugify

load_dotenv()

# Configuración
TRANSCRIPTS_DIR = Path("transcripciones")
CLIPS_DIR = Path("clips_verticales")
METADATA_DIR = Path("metadatos")
DESCRIPTIONS_DIR = Path("description_results")

# Crear directorios si no existen
for dir_path in [TRANSCRIPTS_DIR, CLIPS_DIR, METADATA_DIR, DESCRIPTIONS_DIR]:
    dir_path.mkdir(exist_ok=True)

# Configurar clientes de API para descripciones
openai_descriptions_client = None
if os.getenv("OPENAI_API_KEY"):
    openai_descriptions_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if os.getenv("GOOGLE_API_KEY"):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

claude_descriptions_client = None
if os.getenv("ANTHROPIC_API_KEY"):
    claude_descriptions_client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )


class VideoClipper:
    def __init__(self, video_path: str):
        self.video_path = Path(video_path)
        self.video_name = self.video_path.stem

        # Rutas de archivos
        self.transcript_file = TRANSCRIPTS_DIR / f"{self.video_name}_transcript.txt"
        self.transcript_json_file = (
            TRANSCRIPTS_DIR / f"{self.video_name}_transcript_with_timestamps.json"
        )
        self.clips_dir = CLIPS_DIR / self.video_name
        self.metadata_file = METADATA_DIR / f"{self.video_name}_clips.json"

        # Crear directorio específico para este video
        self.clips_dir.mkdir(exist_ok=True)

        # Cliente OpenAI para análisis con timeout
        self.openai_client = (
            OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                timeout=300.0,  # 5 minutos de timeout
            )
            if os.getenv("OPENAI_API_KEY")
            else None
        )

        # Almacenar transcripción con timestamps
        self.transcript_with_timestamps = None

    def get_video_duration(self) -> float:
        """Obtiene la duración del video en segundos."""
        cmd = [
            "ffprobe",
            "-v",
            "quiet",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            str(self.video_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return float(result.stdout.strip())

    def transcribe_video_with_timestamps(self) -> str:
        """Transcribe el video y guarda tanto el texto como los timestamps."""
        print(f"📝 Transcribiendo video con timestamps: {self.video_path}")

        # Verificar si ya tenemos la transcripción con timestamps
        if self.transcript_json_file.exists() and self.transcript_file.exists():
            print(
                f"✅ Transcripción con timestamps ya existe: {self.transcript_json_file}"
            )
            with open(self.transcript_file, "r", encoding="utf-8") as f:
                text_transcript = f.read()
            with open(self.transcript_json_file, "r", encoding="utf-8") as f:
                self.transcript_with_timestamps = json.load(f)
            return text_transcript

        if not self.openai_client:
            print("❌ OpenAI API key no configurada, necesaria para timestamps")
            return ""

        try:
            # Extraer audio del video
            print("🎵 Extrayendo audio del video...")
            audio_path = extract_audio_from_video(str(self.video_path))

            # Verificar tamaño del archivo de audio
            audio_size = os.path.getsize(audio_path)
            print(f"📊 Tamaño del archivo de audio: {audio_size / (1024*1024):.2f} MB")

            # Límite de Whisper es 25MB
            WHISPER_SIZE_LIMIT = 25 * 1024 * 1024  # 25 MB

            if audio_size > WHISPER_SIZE_LIMIT:
                print(
                    f"⚠️ Archivo muy grande ({audio_size / (1024*1024):.2f} MB > 25 MB)"
                )
                print(
                    "🔄 Usando sistema de transcripción por segmentos con timestamps..."
                )
                # Usar sistema de segmentos pero intentar obtener timestamps
                return self._transcribe_large_file_with_timestamps(audio_path)

            # Estrategia 1: Intentar con timestamps por palabra Y segmento
            try:
                print("🎙️ Estrategia 1: Transcribiendo con timestamps por palabra...")
                print(
                    "⏳ Esto puede tomar unos minutos dependiendo del tamaño del archivo..."
                )

                with open(audio_path, "rb") as audio_file:
                    response = self.openai_client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language="es",
                        response_format="verbose_json",
                        timestamp_granularities=[
                            "word",
                            "segment",
                        ],  # Solicitar ambos tipos
                    )

                print("✅ Transcripción con timestamps completada")

                # Extraer texto simple para compatibilidad
                text_transcript = response.text

                # Almacenar transcripción con timestamps
                self.transcript_with_timestamps = {
                    "text": response.text,
                    "language": response.language,
                    "duration": response.duration,
                    "words": [
                        {
                            "word": word.word,
                            "start": word.start,
                            "end": word.end,
                        }
                        for word in (
                            response.words if hasattr(response, "words") else []
                        )
                    ],
                    "segments": [
                        {
                            "id": segment.id,
                            "start": segment.start,
                            "end": segment.end,
                            "text": segment.text,
                            "avg_logprob": segment.avg_logprob,
                            "compression_ratio": segment.compression_ratio,
                            "no_speech_prob": segment.no_speech_prob,
                            "temperature": segment.temperature,
                        }
                        for segment in (
                            response.segments if hasattr(response, "segments") else []
                        )
                    ],
                }

                # Verificar si obtuvimos datos detallados
                words_count = len(self.transcript_with_timestamps.get("words", []))
                segments_count = len(
                    self.transcript_with_timestamps.get("segments", [])
                )

                print(
                    f"✅ Timestamps obtenidos: {words_count} palabras, {segments_count} segmentos"
                )

                if words_count > 0 or segments_count > 0:
                    return self._save_and_return_transcript(text_transcript, audio_path)
                else:
                    print(
                        "⚠️ No se obtuvieron timestamps detallados, intentando estrategia 2..."
                    )
                    raise Exception("No timestamps obtenidos")

            except Exception as timestamp_error:
                print(f"⚠️ Error en estrategia 1: {str(timestamp_error)}")
                print(
                    "📝 Estrategia 2: Transcripción con solo timestamps de segmento..."
                )

                try:
                    # Estrategia 2: Solo timestamps de segmento
                    with open(audio_path, "rb") as audio_file:
                        response = self.openai_client.audio.transcriptions.create(
                            model="whisper-1",
                            file=audio_file,
                            language="es",
                            response_format="verbose_json",
                            timestamp_granularities=["segment"],  # Solo segmentos
                        )

                    text_transcript = response.text

                    # Almacenar transcripción con timestamps de segmento
                    self.transcript_with_timestamps = {
                        "text": response.text,
                        "language": response.language,
                        "duration": response.duration,
                        "words": [],  # Sin palabras con timestamps
                        "segments": [
                            {
                                "id": segment.id,
                                "start": segment.start,
                                "end": segment.end,
                                "text": segment.text,
                                "avg_logprob": segment.avg_logprob,
                                "compression_ratio": segment.compression_ratio,
                                "no_speech_prob": segment.no_speech_prob,
                                "temperature": segment.temperature,
                            }
                            for segment in (
                                response.segments
                                if hasattr(response, "segments")
                                else []
                            )
                        ],
                    }

                    segments_count = len(
                        self.transcript_with_timestamps.get("segments", [])
                    )
                    print(
                        f"✅ Timestamps de segmento obtenidos: {segments_count} segmentos"
                    )

                    if segments_count > 0:
                        return self._save_and_return_transcript(
                            text_transcript, audio_path
                        )
                    else:
                        print(
                            "⚠️ No se obtuvieron timestamps de segmento, intentando estrategia 3..."
                        )
                        raise Exception("No segment timestamps obtenidos")

                except Exception as fallback_error:
                    print(f"⚠️ Error en estrategia 2: {str(fallback_error)}")
                    print("📝 Estrategia 3: Transcripción básica con verbose_json...")

                    try:
                        # Estrategia 3: Transcripción básica con verbose_json (puede dar segmentos automáticamente)
                        with open(audio_path, "rb") as audio_file:
                            response = self.openai_client.audio.transcriptions.create(
                                model="whisper-1",
                                file=audio_file,
                                language="es",
                                response_format="verbose_json",  # Sin timestamp_granularities
                            )

                        text_transcript = response.text

                        # Almacenar transcripción básica pero verificar si hay segments
                        self.transcript_with_timestamps = {
                            "text": response.text,
                            "language": response.language,
                            "duration": response.duration,
                            "words": [],  # Sin palabras con timestamps
                            "segments": [
                                {
                                    "id": segment.id,
                                    "start": segment.start,
                                    "end": segment.end,
                                    "text": segment.text,
                                    "avg_logprob": segment.avg_logprob,
                                    "compression_ratio": segment.compression_ratio,
                                    "no_speech_prob": segment.no_speech_prob,
                                    "temperature": segment.temperature,
                                }
                                for segment in (
                                    response.segments
                                    if hasattr(response, "segments")
                                    else []
                                )
                            ],
                        }

                        segments_count = len(
                            self.transcript_with_timestamps.get("segments", [])
                        )
                        print(
                            f"✅ Transcripción básica completada: {segments_count} segmentos automáticos"
                        )

                        return self._save_and_return_transcript(
                            text_transcript, audio_path
                        )

                    except Exception as final_fallback_error:
                        print(f"❌ Error en estrategia 3: {str(final_fallback_error)}")
                        print(
                            "🔄 Usando sistema de transcripción por segmentos como último recurso..."
                        )
                        # Limpiar archivo temporal antes del fallback final
                        if os.path.exists(audio_path):
                            os.remove(audio_path)

                        # Fallback final al sistema anterior
                        transcript = transcribe_video(
                            video_path=str(self.video_path),
                            output_file=str(self.transcript_file),
                            language_code="es-MX",
                            use_whisper=True,
                        )

                        # Crear datos básicos de transcripción sin timestamps
                        self.transcript_with_timestamps = {
                            "text": transcript,
                            "language": "es",
                            "duration": self.get_video_duration(),
                            "words": [],  # Sin palabras con timestamps
                            "segments": [],  # Sin segmentos con timestamps
                        }

                        # Guardar transcripción con timestamps (aunque sin timestamps reales)
                        with open(
                            self.transcript_json_file, "w", encoding="utf-8"
                        ) as f:
                            json.dump(
                                self.transcript_with_timestamps,
                                f,
                                indent=2,
                                ensure_ascii=False,
                            )

                        print(f"✅ Transcripción guardada: {self.transcript_file}")
                        print(
                            f"✅ Datos de transcripción guardados: {self.transcript_json_file}"
                        )
                        print(
                            "⚠️ Sin timestamps disponibles - se usará método proporcional"
                        )

                        return transcript

        except Exception as e:
            print(f"❌ Error en transcripción con timestamps: {str(e)}")
            print("🔄 Usando sistema de transcripción como fallback final...")
            # Fallback a transcripción simple
            transcript = transcribe_video(
                video_path=str(self.video_path),
                output_file=str(self.transcript_file),
                language_code="es-MX",
                use_whisper=True,
            )

            # Crear datos básicos de transcripción sin timestamps
            self.transcript_with_timestamps = {
                "text": transcript,
                "language": "es",
                "duration": self.get_video_duration(),
                "words": [],  # Sin palabras con timestamps
                "segments": [],  # Sin segmentos con timestamps
            }

            # Guardar transcripción con timestamps (aunque sin timestamps reales)
            with open(self.transcript_json_file, "w", encoding="utf-8") as f:
                json.dump(
                    self.transcript_with_timestamps, f, indent=2, ensure_ascii=False
                )

            print(f"✅ Transcripción guardada: {self.transcript_file}")
            print(f"✅ Datos de transcripción guardados: {self.transcript_json_file}")
            print("⚠️ Sin timestamps disponibles - se usará método proporcional")

            return transcript

    def _transcribe_large_file_with_timestamps(self, audio_path: str) -> str:
        """Transcribe archivos grandes dividiendo en segmentos e intentando obtener timestamps."""
        print("🔄 Transcribiendo archivo grande en segmentos con timestamps...")

        # Para archivos grandes, usar el sistema anterior pero intentar mejorar
        transcript = transcribe_video(
            video_path=str(self.video_path),
            output_file=str(self.transcript_file),
            language_code="es-MX",
            use_whisper=True,
        )

        # TODO: Implementar división en chunks y transcripción con timestamps
        # Por ahora, crear estructura básica
        self.transcript_with_timestamps = {
            "text": transcript,
            "language": "es",
            "duration": self.get_video_duration(),
            "words": [],
            "segments": [],
        }

        # Guardar transcripción
        with open(self.transcript_json_file, "w", encoding="utf-8") as f:
            json.dump(self.transcript_with_timestamps, f, indent=2, ensure_ascii=False)

        print(f"✅ Transcripción de archivo grande guardada: {self.transcript_file}")
        print(f"✅ Datos guardados: {self.transcript_json_file}")
        print("⚠️ Archivo grande - sin timestamps detallados disponibles")

        # Limpiar archivo temporal
        if os.path.exists(audio_path):
            os.remove(audio_path)

        return transcript

    def _save_and_return_transcript(self, text_transcript: str, audio_path: str) -> str:
        """Guarda la transcripción y datos de timestamps, luego limpia archivos temporales."""
        # Guardar transcripción de texto simple
        with open(self.transcript_file, "w", encoding="utf-8") as f:
            f.write(text_transcript)

        # Guardar transcripción con timestamps
        with open(self.transcript_json_file, "w", encoding="utf-8") as f:
            json.dump(self.transcript_with_timestamps, f, indent=2, ensure_ascii=False)

        # Limpiar archivo de audio temporal
        if os.path.exists(audio_path):
            os.remove(audio_path)

        print(f"✅ Transcripción guardada: {self.transcript_file}")
        print(f"✅ Datos de transcripción guardados: {self.transcript_json_file}")

        # Mostrar información sobre timestamps disponibles
        if self.transcript_with_timestamps and self.transcript_with_timestamps.get(
            "words"
        ):
            print(
                f"🕐 Timestamps por palabra disponibles: {len(self.transcript_with_timestamps['words'])} palabras"
            )
        elif self.transcript_with_timestamps and self.transcript_with_timestamps.get(
            "segments"
        ):
            print(
                f"🕐 Timestamps por segmento disponibles: {len(self.transcript_with_timestamps['segments'])} segmentos"
            )
        else:
            print("⚠️ Sin timestamps disponibles - se usará método proporcional")

        return text_transcript

    def extract_transcript_segment_with_timestamps(
        self, start_time: float, duration: float
    ) -> str:
        """Extrae un segmento de la transcripción usando timestamps reales."""

        if not self.transcript_with_timestamps:
            print("⚠️ No hay timestamps disponibles, usando método proporcional")
            return self.extract_transcript_segment_proportional(start_time, duration)

        end_time = start_time + duration
        segment_words = []

        # Usar palabras con timestamps si están disponibles
        if (
            "words" in self.transcript_with_timestamps
            and self.transcript_with_timestamps["words"]
        ):
            for word_info in self.transcript_with_timestamps["words"]:
                word_start = word_info.get("start", 0)
                word_end = word_info.get("end", word_start)

                # Si la palabra está en nuestro rango de tiempo
                if word_start >= start_time and word_end <= end_time:
                    segment_words.append(word_info["word"])
                # Si la palabra cruza el inicio de nuestro segmento
                elif word_start < start_time and word_end > start_time:
                    segment_words.append(word_info["word"])
                # Si la palabra cruza el final de nuestro segmento
                elif word_start < end_time and word_end > end_time:
                    segment_words.append(word_info["word"])

        # Usar segmentos si las palabras no están disponibles
        elif (
            "segments" in self.transcript_with_timestamps
            and self.transcript_with_timestamps["segments"]
        ):
            for segment in self.transcript_with_timestamps["segments"]:
                segment_start = segment.get("start", 0)
                segment_end = segment.get("end", segment_start)

                # Si el segmento se superpone con nuestro rango
                if not (segment_end < start_time or segment_start > end_time):
                    segment_words.append(segment["text"])

        if segment_words:
            result = " ".join(segment_words).strip()
            print(f"📝 Segmento extraído con timestamps: {len(result)} caracteres")
            return result
        else:
            print(
                "⚠️ No se encontraron palabras en el rango, usando método proporcional"
            )
            return self.extract_transcript_segment_proportional(start_time, duration)

    def extract_transcript_segment_proportional(
        self, start_time: float, duration: float
    ) -> str:
        """Método de fallback: extrae segmento usando proporciones (método original)."""

        # Leer transcripción simple si no está cargada
        if not hasattr(self, "_simple_transcript"):
            with open(self.transcript_file, "r", encoding="utf-8") as f:
                self._simple_transcript = f.read()

        transcript = self._simple_transcript
        video_duration = self.get_video_duration()
        total_chars = len(transcript)

        # Calcular posiciones aproximadas en el texto
        start_ratio = start_time / video_duration
        end_ratio = (start_time + duration) / video_duration

        start_pos = int(total_chars * start_ratio)
        end_pos = int(total_chars * end_ratio)

        # Asegurar que no nos salimos del rango
        start_pos = max(0, start_pos)
        end_pos = min(total_chars, end_pos)

        # Extraer el segmento
        segment = transcript[start_pos:end_pos].strip()

        # Si el segmento es muy corto, expandir un poco
        if len(segment) < 100 and end_pos < total_chars:
            end_pos = min(total_chars, end_pos + 200)
            segment = transcript[start_pos:end_pos].strip()

        return segment

    def analyze_transcript_for_clips(
        self, transcript: str, target_duration: int = 60
    ) -> List[Dict]:
        """Analiza la transcripción para identificar momentos interesantes para clips."""

        if not self.openai_client:
            print("❌ OpenAI API key no configurada")
            return []

        video_duration = self.get_video_duration()

        prompt = f"""Analiza la siguiente transcripción de un video educativo/técnico de {video_duration:.0f} segundos y identifica entre 5-8 momentos interesantes para crear clips cortos.

CRITERIOS para cada clip:
- Duración ideal: {target_duration} segundos, pero puede durar hasta3 minutos si vale la pena
- Debe ser AUTO-CONTENIDO (concepto completo)
- Debe tener un HOOK o ser llamativo
- Debe tener valor educativo para las siguientes audiencias:
    - Programadores
    - Desarrolladores
    - Ingenieros de software
    - Estudiantes de programación
    - Entusiastas de la tecnología
    - Cualquier persona que quiera aprender sobre programación
    - Interesados en inteligencia artificial
Las descripciones para las plataformas deben ser amplias, serias y no usar emojis, deben ampliar sobre el contenido del clip
y por qué puedes aprender algo nuevo de él. No se tiene que hablar sobre el video como "este video es sobre..." sino que se debe hablar
sobre el contenido del clip, por ejemplo: "El lenguaje de programación python es un lenguaje de programación que..." y finalmente debe
incluir un hook o frase llamativa que sea interesante para el lector.


TRANSCRIPCIÓN:
{transcript}

Responde SOLO en formato JSON válido con esta estructura:
[
  {{
    "titulo": "Descripción corta del clip",
    "inicio_estimado": 0,
    "duracion_estimada": 60,
    "razon": "Por qué es interesante",
    "hook": "Frase o concepto llamativo",
    "tipo": "educativo|consejo|historia|pregunta",
    "descripcion_para_tiktok": "Descripción para TikTok"
  }}
]

Los tiempos deben distribuirse proporcionalmente a lo largo del video de {video_duration:.0f} segundos."""

        try:
            response = self.openai_client.chat.completions.create(
                model="o3-2025-04-16",  # no cambiar
                messages=[{"role": "user", "content": prompt}],
                # temperature=0.3,
            )

            # Intentar parsear JSON
            import re

            content = response.choices[0].message.content

            # Extraer JSON del contenido (por si hay texto adicional)
            json_match = re.search(r"\[.*\]", content, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                clips = json.loads(json_str)

                print(f"✅ Identificados {len(clips)} clips potenciales")
                return clips
            else:
                print("❌ No se pudo extraer JSON válido de la respuesta")
                return []

        except Exception as e:
            print(f"❌ Error analizando transcripción: {str(e)}")
            return []

    def extract_video_segment(
        self, start_time: float, duration: float, output_path: str
    ) -> bool:
        """Extrae un segmento del video original."""

        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(self.video_path),
            "-ss",
            str(start_time),
            "-t",
            str(duration),
            "-c",
            "copy",  # Copiar sin re-codificar para velocidad
            output_path,
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return True
            else:
                print(f"❌ Error extrayendo segmento: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error ejecutando ffmpeg: {str(e)}")
            return False

    def convert_to_vertical(self, input_path: str, output_path: str) -> bool:
        """Convierte un clip horizontal a formato vertical (9:16) con resolución 1080x1920."""

        # Comando ffmpeg corregido para resolución vertical 1080x1920 con aspect ratio forzado
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            # Usar filter_complex para conversión vertical con resolución exacta
            "-filter_complex",
            "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,setsar=1[fg];"
            "[0:v]scale=1080:1920,boxblur=30:15,setsar=1[bg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2:shortest=1,setsar=1[out]",
            "-map",
            "[out]",
            "-map",
            "0:a",
            "-c:a",
            "copy",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-aspect",
            "9:16",  # Forzar aspect ratio 9:16
            "-s",
            "1080x1920",  # Forzar resolución de salida
            output_path,
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return True
            else:
                print(f"❌ Error convirtiendo a vertical: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error en conversión vertical: {str(e)}")
            return False

    def generate_clips(self, clips_data: List[Dict], transcript: str) -> List[Dict]:
        """Genera todos los clips verticales."""

        successful_clips = []

        for i, clip_info in enumerate(clips_data, 1):
            print(f"\n🎬 Procesando clip {i}/{len(clips_data)}: {clip_info['titulo']}")

            # Nombres de archivos
            safe_title = "".join(
                c for c in clip_info["titulo"] if c.isalnum() or c in (" ", "-", "_")
            ).rstrip()
            safe_title = safe_title.replace(" ", "_")[:50]  # Limitar longitud

            horizontal_clip = (
                self.clips_dir / f"clip_{i:02d}_{safe_title}_horizontal.mp4"
            )
            vertical_clip = self.clips_dir / f"clip_{i:02d}_{safe_title}_vertical.mp4"

            # Extraer segmento de transcripción correspondiente usando timestamps
            print(f"  📝 Extrayendo transcripción del segmento...")
            clip_transcript = self.extract_transcript_segment_with_timestamps(
                clip_info["inicio_estimado"], clip_info["duracion_estimada"]
            )

            # Extraer segmento horizontal
            print(f"  ⏂ Extrayendo segmento...")
            if self.extract_video_segment(
                clip_info["inicio_estimado"],
                clip_info["duracion_estimada"],
                str(horizontal_clip),
            ):
                # Convertir a vertical
                print(f"  📱 Convirtiendo a formato vertical...")
                if self.convert_to_vertical(str(horizontal_clip), str(vertical_clip)):
                    # Limpiar archivo horizontal temporal
                    horizontal_clip.unlink()

                    # Agregar información del clip exitoso
                    clip_result = clip_info.copy()
                    clip_result.update(
                        {
                            "archivo": str(vertical_clip),
                            "transcripcion_segmento": clip_transcript,
                            "procesado_exitosamente": True,
                            "fecha_creacion": datetime.now().isoformat(),
                        }
                    )
                    successful_clips.append(clip_result)
                    print(f"  ✅ Clip {i} completado: {vertical_clip}")
                else:
                    print(f"  ❌ Error convirtiendo clip {i}")
            else:
                print(f"  ❌ Error extrayendo clip {i}")

        return successful_clips

    def save_metadata(self, clips_data: List[Dict]):
        """Guarda metadatos de los clips generados."""

        metadata = {
            "video_original": str(self.video_path),
            "transcripcion": str(self.transcript_file),
            "transcripcion_con_timestamps": str(self.transcript_json_file)
            if self.transcript_json_file.exists()
            else None,
            "tiene_timestamps": bool(self.transcript_with_timestamps),
            "fecha_procesamiento": datetime.now().isoformat(),
            "total_clips": len(clips_data),
            "clips": clips_data,
        }

        # Agregar información sobre la duración del video y timestamps si está disponible
        if self.transcript_with_timestamps:
            metadata["video_duracion"] = self.transcript_with_timestamps.get(
                "duration", self.get_video_duration()
            )
            metadata["idioma_detectado"] = self.transcript_with_timestamps.get(
                "language", "es"
            )

        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"📋 Metadatos guardados: {self.metadata_file}")

    def generate_clip_description(
        self, clip_transcript: str, topic: str
    ) -> Dict[str, str]:
        """Genera descripciones para redes sociales para un clip específico."""

        prompt = f"""Convierte el siguiente fragmento en una **descripción educativa para TikTok** (máx. 1000 caracteres).
Pautas:
- Usa un tono serio pero relajado, sin emojis.
- Explica con claridad el **tema central** que indico a continuación.  
- Organiza las ideas en párrafos breves y conectados.
- Si el fragmento menciona datos, autores o estudios, incluye **1 – 2 referencias** al final (fuente + año o URL corta). 
- Cierra con **5 – 6 etiquetas** relevantes en español (puedes mezclar inglés si es habitual), todas precedidas por "#".
- No hables como el interlocutor, sino como alguien que describe lo que se habla en el video.
- Toma un enfoque práctico y haz recomendaciones directas al lector cuando sea conveniente

**Tema central:** {topic}
**Fragmento a convertir:**
{clip_transcript}"""

        results = {}

        # Generar con OpenAI si está disponible
        if openai_descriptions_client:
            try:
                gpt_response = openai_descriptions_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                results["gpt-4o-mini"] = gpt_response.choices[0].message.content
            except Exception as e:
                results["gpt-4o-mini"] = f"Error: {str(e)}"

        # Generar con Gemini si está disponible
        if os.getenv("GOOGLE_API_KEY"):
            try:
                model = genai.GenerativeModel("gemini-2.5-pro-preview-03-25")
                gemini_response = model.generate_content(prompt)
                results["gemini"] = gemini_response.text
            except Exception as e:
                results["gemini"] = f"Error: {str(e)}"

        # Generar con Claude si está disponible
        if claude_descriptions_client:
            try:
                claude_response = claude_descriptions_client.messages.create(
                    model="claude-3-haiku-20241022",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}],
                )
                results["claude"] = claude_response.content[0].text
            except Exception as e:
                results["claude"] = f"Error: {str(e)}"

        return results

    def save_clip_descriptions(self, clip_data: Dict, descriptions: Dict[str, str]):
        """Guarda las descripciones de un clip en formato markdown."""

        clip_name = slugify(clip_data["titulo"])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        description_file = DESCRIPTIONS_DIR / f"clip_{clip_name}_{timestamp}.md"

        with open(description_file, "w", encoding="utf-8") as f:
            f.write(f"# Descripción para Clip: {clip_data['titulo']}\n\n")
            f.write(f"**Tema:** {clip_data['titulo']}\n\n")
            f.write(f"**Tipo:** {clip_data.get('tipo', 'educativo')}\n\n")
            f.write(f"**Hook:** {clip_data.get('hook', 'N/A')}\n\n")
            f.write(
                f"**Duración:** {clip_data.get('duracion_estimada', 'N/A')} segundos\n\n"
            )
            f.write(f"**Generado el:** {timestamp}\n\n")

            f.write("## Descripciones Generadas\n\n")
            for model, result in descriptions.items():
                if not result.startswith("Error:"):
                    f.write(f"### {model.upper()}\n\n")
                    f.write(f"{result}\n\n")
                    f.write("---\n\n")

        print(f"📝 Descripciones guardadas: {description_file}")
        return description_file

    def process_video(self, target_duration: int = 45) -> bool:
        """Procesa el video completo: transcripción → análisis → clips."""

        print(f"🎬 Procesando video: {self.video_path}")
        print(f"📁 Clips se guardarán en: {self.clips_dir}")

        try:
            # 1. Transcribir video con timestamps
            transcript = self.transcribe_video_with_timestamps()

            if not transcript:
                print("❌ No se pudo transcribir el video")
                return False

            # 2. Analizar transcripción
            print(f"\n🤖 Analizando transcripción para identificar clips...")
            clips_data = self.analyze_transcript_for_clips(transcript, target_duration)

            if not clips_data:
                print("❌ No se pudieron identificar clips interesantes")
                return False

            # 3. Generar clips (ya no necesitamos pasar transcript, usamos timestamps internos)
            print(f"\n🎞️  Generando {len(clips_data)} clips verticales...")
            successful_clips = self.generate_clips(clips_data, transcript)

            # 4. Guardar metadatos incluyendo información de timestamps
            self.save_metadata(successful_clips)

            # 5. Generar descripciones para cada clip
            for clip in successful_clips:
                print(f"\n🤖 Generando descripción para clip: {clip['titulo']}")
                descriptions = self.generate_clip_description(
                    clip["transcripcion_segmento"], clip["titulo"]
                )
                self.save_clip_descriptions(clip, descriptions)

            print(f"\n✅ Proceso completado!")
            print(
                f"📊 Clips generados exitosamente: {len(successful_clips)}/{len(clips_data)}"
            )
            print(f"📂 Directorio de salida: {self.clips_dir}")

            if self.transcript_with_timestamps:
                print(
                    f"🕐 Transcripción con timestamps disponible para precisión mejorada"
                )

            return len(successful_clips) > 0

        except Exception as e:
            print(f"❌ Error durante el procesamiento: {str(e)}")
            return False


@begin.start
def main(video_path, target_duration=45):
    """
    Genera clips verticales a partir de un video largo horizontal.

    Args:
        video_path: Ruta al video original
        target_duration: Duración objetivo para cada clip en segundos (default: 45)
    """

    if not video_path:
        print("❌ Error: Debes proporcionar la ruta del video")
        return

    if not os.path.exists(video_path):
        print(f"❌ Error: No se encontró el video: {video_path}")
        return

    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY no configurado")
        return

    # Convertir target_duration a int
    target_duration = int(target_duration)

    # Crear el procesador y ejecutar
    clipper = VideoClipper(video_path)
    success = clipper.process_video(target_duration)

    if success:
        print(f"\n🎉 ¡Proceso completado exitosamente!")
    else:
        print(f"\n❌ El proceso falló o no se generaron clips")


if __name__ == "__main__":
    main()
