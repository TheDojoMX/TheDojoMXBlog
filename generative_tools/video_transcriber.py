import os
import tempfile
from pathlib import Path
from google.cloud import speech
import moviepy as mp
import begin
from dotenv import load_dotenv
import uuid
from openai import OpenAI
import math
import subprocess

load_dotenv()

# Límite de tamaño para Whisper (25 MB en bytes)
WHISPER_SIZE_LIMIT = 25 * 1024 * 1024  # 25 MB


def diagnose_system():
    """
    Diagnóstica el sistema para identificar posibles problemas.
    """
    print("🔍 Diagnóstico del sistema...")

    # Verificar directorio temporal
    temp_dir = tempfile.gettempdir()
    print(f"📁 Directorio temporal del sistema: {temp_dir}")
    print(f"📁 Existe: {os.path.exists(temp_dir)}")
    print(
        f"📁 Escribible: {os.access(temp_dir, os.W_OK) if os.path.exists(temp_dir) else 'No existe'}"
    )

    # Verificar directorio de trabajo actual
    current_dir = os.getcwd()
    print(f"📁 Directorio actual: {current_dir}")
    print(f"📁 Escribible: {os.access(current_dir, os.W_OK)}")

    # Verificar moviepy
    try:
        import moviepy

        print(f"🎬 MoviePy versión: {moviepy.__version__}")
    except Exception as e:
        print(f"❌ Error con MoviePy: {e}")

    # Verificar Google Cloud credentials
    google_creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    has_google_cloud = False
    if google_creds:
        print(f"🔑 Google Cloud credentials configurado: {google_creds}")
        if os.path.exists(google_creds):
            if google_creds.endswith(".json"):
                print(f"✅ Archivo de credenciales JSON válido")
                has_google_cloud = True
            else:
                print(
                    f"❌ El archivo no es un JSON de credenciales (parece ser una API key)"
                )
        else:
            print(f"❌ Archivo de credenciales no encontrado")
    else:
        print("⚠️  GOOGLE_APPLICATION_CREDENTIALS no configurado")

    # Verificar OpenAI API Key
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    if has_openai:
        openai_key = os.getenv("OPENAI_API_KEY")
        print(f"✅ OpenAI API Key configurado: {openai_key[:8]}...")
    else:
        print("⚠️  OPENAI_API_KEY no configurado")

    # Determinar qué servicio se usaría
    print("\n🎯 Servicio de transcripción que se usaría:")
    if has_google_cloud:
        print("✅ Google Cloud Speech-to-Text")
    elif has_openai:
        print("✅ OpenAI Whisper")
    else:
        print("❌ Ningún servicio disponible - configurar Google Cloud o OpenAI")

    return temp_dir, current_dir


def get_safe_temp_dir():
    """
    Obtiene un directorio temporal seguro, con fallback al directorio actual.
    """
    # Intentar directorio temporal del sistema
    temp_dir = tempfile.gettempdir()
    if os.path.exists(temp_dir) and os.access(temp_dir, os.W_OK):
        return temp_dir

    # Fallback: usar directorio actual
    current_dir = os.getcwd()
    if os.access(current_dir, os.W_OK):
        temp_subdir = os.path.join(current_dir, "temp_audio")
        os.makedirs(temp_subdir, exist_ok=True)
        return temp_subdir

    # Último recurso: directorio home del usuario
    home_dir = os.path.expanduser("~")
    temp_subdir = os.path.join(home_dir, "temp_audio")
    os.makedirs(temp_subdir, exist_ok=True)
    return temp_subdir


def extract_audio_from_video(video_path: str, audio_path: str = None) -> str:
    """
    Extrae el audio de un video MP4 y lo guarda como archivo WAV.

    Args:
        video_path: Ruta al archivo de video MP4
        audio_path: Ruta de salida para el archivo de audio (opcional)

    Returns:
        Ruta del archivo de audio extraído
    """
    if audio_path is None:
        # Crear archivo temporal con nombre único para evitar conflictos
        temp_dir = get_safe_temp_dir()
        print(f"📁 Directorio temporal: {temp_dir}")

        # Generar nombre único para evitar conflictos
        unique_id = str(uuid.uuid4())[:8]
        video_name = Path(video_path).stem
        audio_path = os.path.join(temp_dir, f"{video_name}_{unique_id}_audio.wav")

    print(f"🎬 Extrayendo audio de: {video_path}")
    print(f"📍 Archivo de audio temporal: {audio_path}")

    try:
        # Verificar que el video existe
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"El archivo de video no existe: {video_path}")

        # Extraer audio usando moviepy
        video = mp.VideoFileClip(video_path)

        if video.audio is None:
            raise ValueError(f"El video no contiene pista de audio: {video_path}")

        audio = video.audio

        # Verificar directorio de destino
        audio_dir = os.path.dirname(audio_path)
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir, exist_ok=True)

        audio.write_audiofile(audio_path, logger=None)

        # Limpiar recursos
        audio.close()
        video.close()

        # Verificar que el archivo se creó correctamente
        if not os.path.exists(audio_path):
            raise FileNotFoundError(
                f"No se pudo crear el archivo de audio: {audio_path}"
            )

        print(f"🎵 Audio extraído exitosamente en: {audio_path}")
        print(f"📊 Tamaño del archivo: {os.path.getsize(audio_path)} bytes")

        return audio_path

    except Exception as e:
        print(f"❌ Error al extraer audio: {str(e)}")
        # Intentar limpiar cualquier archivo parcialmente creado
        if audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
                print(f"🗑️  Archivo temporal parcial eliminado: {audio_path}")
            except:
                pass
        raise


def transcribe_audio_with_google_cloud(
    audio_path: str, language_code: str = "es-MX"
) -> str:
    """
    Transcribe un archivo de audio usando Google Cloud Speech-to-Text.

    Args:
        audio_path: Ruta al archivo de audio
        language_code: Código de idioma (default: es-MX para español mexicano)

    Returns:
        Texto transcrito
    """
    # Verificar que existe la clave de API
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

    # Verificar que el archivo de audio existe
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Archivo de audio no encontrado: {audio_path}")

    print(f"🎙️  Transcribiendo audio: {audio_path}")
    print(f"📊 Tamaño del archivo: {os.path.getsize(audio_path)} bytes")

    try:
        # Inicializar cliente de Google Cloud Speech
        client = speech.SpeechClient()

        # Leer archivo de audio
        with open(audio_path, "rb") as audio_file:
            content = audio_file.read()

        if len(content) == 0:
            raise ValueError(f"El archivo de audio está vacío: {audio_path}")

        audio = speech.RecognitionAudio(content=content)

        # Configurar parámetros de reconocimiento
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,  # Tasa de muestreo común para WAV
            language_code=language_code,
            enable_automatic_punctuation=True,
            enable_word_time_offsets=False,
            model="latest_long",  # Modelo optimizado para audio largo
        )

        # Realizar transcripción
        response = client.recognize(config=config, audio=audio)

        # Extraer texto de la respuesta
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript + " "

        if not transcript.strip():
            raise ValueError(
                "No se pudo transcribir el audio. Verificar calidad del audio o configuración."
            )

        print(f"✅ Transcripción completada ({len(transcript)} caracteres)")
        return transcript.strip()

    except Exception as e:
        print(f"❌ Error durante la transcripción: {str(e)}")
        raise


def split_audio_if_needed(
    audio_path: str, max_size_bytes: int = WHISPER_SIZE_LIMIT
) -> list:
    """
    Divide un archivo de audio en segmentos si es demasiado grande.

    Args:
        audio_path: Ruta al archivo de audio
        max_size_bytes: Tamaño máximo permitido en bytes

    Returns:
        Lista de rutas de archivos de audio (puede ser solo el original si no es muy grande)
    """
    file_size = os.path.getsize(audio_path)

    if file_size <= max_size_bytes:
        print(f"📏 Archivo de audio dentro del límite ({file_size:,} bytes)")
        return [audio_path]

    print(
        f"📏 Archivo demasiado grande ({file_size:,} bytes), dividiendo en segmentos..."
    )

    try:
        # Cargar el audio para dividirlo
        audio_clip = mp.AudioFileClip(audio_path)
        duration = audio_clip.duration

        # Estimar cuántos segmentos necesitamos basado en tamaño
        # Usar un factor de seguridad para asegurar que cada segmento sea menor al límite
        safety_factor = 0.8  # 80% del límite para seguridad
        estimated_segments = math.ceil(file_size / (max_size_bytes * safety_factor))
        segment_duration = duration / estimated_segments

        print(
            f"📊 Duración total: {duration:.1f}s, dividiendo en {estimated_segments} segmentos de ~{segment_duration:.1f}s"
        )

        # Crear segmentos
        segment_paths = []
        base_path = Path(audio_path)

        for i in range(estimated_segments):
            start_time = i * segment_duration
            end_time = min((i + 1) * segment_duration, duration)

            segment_path = (
                base_path.parent / f"{base_path.stem}_segment_{i+1}{base_path.suffix}"
            )

            print(
                f"🔄 Creando segmento {i+1}/{estimated_segments} ({start_time:.1f}s - {end_time:.1f}s)..."
            )

            # Extraer segmento con configuración muy básica
            segment_clip = audio_clip.subclipped(start_time, end_time)

            # Escribir con configuración mínima (solo especificar el path)
            segment_clip.write_audiofile(str(segment_path))
            segment_clip.close()

            segment_paths.append(str(segment_path))
            segment_size = os.path.getsize(segment_path)
            print(
                f"✅ Segmento {i+1}/{estimated_segments}: {segment_size:,} bytes ({end_time-start_time:.1f}s)"
            )

        audio_clip.close()
        return segment_paths

    except Exception as e:
        print(f"❌ Error dividiendo audio: {str(e)}")
        print("🔄 Intentando transcripción directa (puede fallar por tamaño)...")
        return [audio_path]


def split_audio_with_ffmpeg(
    audio_path: str, max_size_bytes: int = WHISPER_SIZE_LIMIT
) -> list:
    """
    Divide un archivo de audio usando ffmpeg directamente (más confiable).

    Args:
        audio_path: Ruta al archivo de audio
        max_size_bytes: Tamaño máximo permitido en bytes

    Returns:
        Lista de rutas de archivos de audio
    """
    file_size = os.path.getsize(audio_path)

    if file_size <= max_size_bytes:
        print(f"📏 Archivo de audio dentro del límite ({file_size:,} bytes)")
        return [audio_path]

    print(
        f"📏 Archivo demasiado grande ({file_size:,} bytes), dividiendo con ffmpeg..."
    )

    try:
        # Obtener duración del audio usando ffprobe
        cmd_duration = [
            "ffprobe",
            "-v",
            "quiet",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            audio_path,
        ]
        result = subprocess.run(cmd_duration, capture_output=True, text=True)
        duration = float(result.stdout.strip())

        # Calcular número de segmentos necesarios (con margen de seguridad)
        safety_factor = 0.8
        estimated_segments = math.ceil(file_size / (max_size_bytes * safety_factor))
        segment_duration = duration / estimated_segments

        print(
            f"📊 Duración total: {duration:.1f}s, dividiendo en {estimated_segments} segmentos de ~{segment_duration:.1f}s"
        )

        # Crear segmentos usando ffmpeg
        segment_paths = []
        base_path = Path(audio_path)

        for i in range(estimated_segments):
            start_time = i * segment_duration
            segment_path = (
                base_path.parent
                / f"{base_path.stem}_ffmpeg_segment_{i+1}{base_path.suffix}"
            )

            # Comando ffmpeg para extraer segmento
            cmd_segment = [
                "ffmpeg",
                "-y",
                "-i",
                audio_path,
                "-ss",
                str(start_time),
                "-t",
                str(segment_duration),
                "-c",
                "copy",  # Copiar sin re-codificar (más rápido)
                str(segment_path),
            ]

            print(f"🔄 Creando segmento {i+1}/{estimated_segments} con ffmpeg...")
            result = subprocess.run(cmd_segment, capture_output=True, text=True)

            if result.returncode == 0 and os.path.exists(segment_path):
                segment_size = os.path.getsize(segment_path)
                print(f"✅ Segmento {i+1}/{estimated_segments}: {segment_size:,} bytes")
                segment_paths.append(str(segment_path))
            else:
                print(f"❌ Error creando segmento {i+1}: {result.stderr}")

        return segment_paths if segment_paths else [audio_path]

    except Exception as e:
        print(f"❌ Error con ffmpeg: {str(e)}")
        print("🔄 Usando método MoviePy como fallback...")
        return split_audio_if_needed(audio_path, max_size_bytes)


def transcribe_audio_segments_with_whisper(
    audio_segments: list, language_code: str = "es"
) -> str:
    """
    Transcribe múltiples segmentos de audio usando OpenAI Whisper.

    Args:
        audio_segments: Lista de rutas de archivos de audio
        language_code: Código de idioma

    Returns:
        Texto transcrito combinado
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    full_transcript = ""

    for i, audio_path in enumerate(audio_segments, 1):
        print(f"🎙️  Transcribiendo segmento {i}/{len(audio_segments)}: {audio_path}")

        try:
            with open(audio_path, "rb") as audio_file:
                response = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language_code,
                    response_format="text",
                )

            segment_transcript = response.strip()
            if segment_transcript:
                full_transcript += segment_transcript + " "
                print(
                    f"✅ Segmento {i} transcrito ({len(segment_transcript)} caracteres)"
                )
            else:
                print(f"⚠️  Segmento {i} sin contenido transcribible")

        except Exception as e:
            print(f"❌ Error transcribiendo segmento {i}: {str(e)}")
            continue

    return full_transcript.strip()


def transcribe_audio_with_openai_whisper(
    audio_path: str, language_code: str = "es"
) -> str:
    """
    Transcribe un archivo de audio usando OpenAI Whisper, dividiendo si es necesario.

    Args:
        audio_path: Ruta al archivo de audio
        language_code: Código de idioma (default: es para español)

    Returns:
        Texto transcrito
    """
    # Verificar que existe la clave de API
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set")

    # Verificar que el archivo de audio existe
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Archivo de audio no encontrado: {audio_path}")

    print(f"🎙️  Transcribiendo audio con OpenAI Whisper: {audio_path}")
    print(f"📊 Tamaño del archivo: {os.path.getsize(audio_path)} bytes")

    try:
        # Dividir el archivo si es necesario
        audio_segments = split_audio_with_ffmpeg(audio_path)

        if len(audio_segments) == 1:
            # Archivo pequeño, transcripción directa
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            with open(audio_path, "rb") as audio_file:
                response = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language_code,
                    response_format="text",
                )

            transcript = response.strip()
        else:
            # Archivo grande, transcripción por segmentos
            transcript = transcribe_audio_segments_with_whisper(
                audio_segments, language_code
            )

            # Limpiar archivos de segmentos temporales
            for segment_path in audio_segments:
                if segment_path != audio_path and os.path.exists(segment_path):
                    try:
                        os.remove(segment_path)
                        print(
                            f"🗑️  Segmento temporal eliminado: {os.path.basename(segment_path)}"
                        )
                    except:
                        pass

        if not transcript:
            raise ValueError(
                "No se pudo transcribir el audio. Verificar calidad del audio."
            )

        print(f"✅ Transcripción completada con Whisper ({len(transcript)} caracteres)")
        return transcript

    except Exception as e:
        print(f"❌ Error durante la transcripción con Whisper: {str(e)}")
        raise


def transcribe_video(
    video_path: str,
    output_file: str = None,
    language_code: str = "es-MX",
    keep_audio: bool = False,
    use_whisper: bool = None,
) -> str:
    """
    Transcribe un video MP4 completo.

    Args:
        video_path: Ruta al archivo de video MP4
        output_file: Archivo donde guardar la transcripción (opcional)
        language_code: Código de idioma para la transcripción
        keep_audio: Si mantener el archivo de audio extraído
        use_whisper: Forzar uso de Whisper (None = autodetectar)

    Returns:
        Texto transcrito
    """
    print(f"🎬 Iniciando transcripción de video: {video_path}")

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video no encontrado: {video_path}")

    # Determinar qué servicio usar
    if use_whisper is None:
        # Autodetectar: preferir Google Cloud si está bien configurado
        google_creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        has_google_cloud = (
            google_creds
            and os.path.exists(google_creds)
            and google_creds.endswith(".json")
        )
        has_openai = bool(os.getenv("OPENAI_API_KEY"))

        if has_google_cloud:
            use_whisper = False
            print("🔧 Usando Google Cloud Speech-to-Text")
        elif has_openai:
            use_whisper = True
            print("🔧 Usando OpenAI Whisper")
        else:
            raise ValueError(
                "No se encontró configuración válida para Google Cloud ni OpenAI"
            )

    audio_path = None
    try:
        # Extraer audio
        audio_path = extract_audio_from_video(video_path)

        # Transcribir audio con el servicio elegido
        if use_whisper:
            # Convertir código de idioma de Google a código de OpenAI
            lang_map = {
                "es-MX": "es",
                "es-ES": "es",
                "es": "es",
                "en-US": "en",
                "en-GB": "en",
                "en": "en",
                "fr": "fr",
                "de": "de",
                "it": "it",
                "pt": "pt",
            }
            whisper_lang = lang_map.get(language_code, language_code.split("-")[0])
            transcript = transcribe_audio_with_openai_whisper(audio_path, whisper_lang)
        else:
            transcript = transcribe_audio_with_google_cloud(audio_path, language_code)

        # Guardar transcripción si se especifica archivo de salida
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(transcript)
            print(f"📝 Transcripción guardada en: {output_file}")

        return transcript

    except Exception as e:
        print(f"❌ Error durante la transcripción del video: {str(e)}")
        raise

    finally:
        # Limpiar archivo de audio temporal si no se quiere mantener
        if audio_path and not keep_audio and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
                print(f"🗑️  Archivo de audio temporal eliminado: {audio_path}")
            except Exception as cleanup_error:
                print(f"⚠️  No se pudo eliminar el archivo temporal: {cleanup_error}")


def transcribe_audio_file_directly(
    audio_path: str,
    output_file: str = None,
    language_code: str = "es-MX",
    use_whisper: bool = None,
) -> str:
    """
    Transcribe un archivo de audio directamente (sin extraer de video).

    Args:
        audio_path: Ruta al archivo de audio
        output_file: Archivo donde guardar la transcripción (opcional)
        language_code: Código de idioma para la transcripción
        use_whisper: Forzar uso de Whisper (None = autodetectar)

    Returns:
        Texto transcrito
    """
    print(f"🎙️  Transcribiendo archivo de audio directo: {audio_path}")

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Archivo de audio no encontrado: {audio_path}")

    # Determinar qué servicio usar
    if use_whisper is None:
        # Autodetectar: preferir Google Cloud si está bien configurado
        google_creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        has_google_cloud = (
            google_creds
            and os.path.exists(google_creds)
            and google_creds.endswith(".json")
        )
        has_openai = bool(os.getenv("OPENAI_API_KEY"))

        if has_google_cloud:
            use_whisper = False
            print("🔧 Usando Google Cloud Speech-to-Text")
        elif has_openai:
            use_whisper = True
            print("🔧 Usando OpenAI Whisper")
        else:
            raise ValueError(
                "No se encontró configuración válida para Google Cloud ni OpenAI"
            )

    try:
        # Transcribir audio con el servicio elegido
        if use_whisper:
            # Convertir código de idioma de Google a código de OpenAI
            lang_map = {
                "es-MX": "es",
                "es-ES": "es",
                "es": "es",
                "en-US": "en",
                "en-GB": "en",
                "en": "en",
                "fr": "fr",
                "de": "de",
                "it": "it",
                "pt": "pt",
            }
            whisper_lang = lang_map.get(language_code, language_code.split("-")[0])
            transcript = transcribe_audio_with_openai_whisper(audio_path, whisper_lang)
        else:
            transcript = transcribe_audio_with_google_cloud(audio_path, language_code)

        # Guardar transcripción si se especifica archivo de salida
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(transcript)
            print(f"📝 Transcripción guardada en: {output_file}")

        return transcript

    except Exception as e:
        print(f"❌ Error durante la transcripción del audio: {str(e)}")
        raise


@begin.start
def main(
    video_path=None,
    output_file=None,
    language="es-MX",
    keep_audio=False,
    diagnose=False,
    whisper=False,
):
    """
    Transcribe un video MP4 o archivo de audio usando Google Cloud Speech-to-Text o OpenAI Whisper.

    Args:
        video_path: Ruta al archivo de video MP4 o audio WAV/MP3
        output_file: Archivo donde guardar la transcripción (opcional)
        language: Código de idioma para la transcripción (default: es-MX)
        keep_audio: Si mantener el archivo de audio extraído (default: False)
        diagnose: Solo ejecutar diagnóstico del sistema (default: False)
        whisper: Forzar uso de OpenAI Whisper (default: False, autodetectar)
    """
    if diagnose:
        diagnose_system()
        return

    if not video_path:
        print("❌ Error: Debes proporcionar video_path o usar --diagnose")
        return

    try:
        # Detectar si es archivo de audio o video por extensión
        file_ext = Path(video_path).suffix.lower()
        audio_extensions = [".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg"]
        video_extensions = [".mp4", ".avi", ".mov", ".mkv", ".webm"]

        if file_ext in audio_extensions:
            print(f"🎙️  Detectado archivo de audio: {file_ext}")
            transcript = transcribe_audio_file_directly(
                audio_path=video_path,
                output_file=output_file,
                language_code=language,
                use_whisper=whisper if whisper else None,
            )
        elif file_ext in video_extensions:
            print(f"🎬 Detectado archivo de video: {file_ext}")
            transcript = transcribe_video(
                video_path=video_path,
                output_file=output_file,
                language_code=language,
                keep_audio=keep_audio,
                use_whisper=whisper if whisper else None,
            )
        else:
            print(f"⚠️  Extensión desconocida: {file_ext}")
            print("🔄 Intentando como video...")
            transcript = transcribe_video(
                video_path=video_path,
                output_file=output_file,
                language_code=language,
                keep_audio=keep_audio,
                use_whisper=whisper if whisper else None,
            )

        print("\n" + "=" * 50)
        print("TRANSCRIPCIÓN COMPLETADA")
        print("=" * 50)
        print(transcript[:500] + "..." if len(transcript) > 500 else transcript)

    except Exception as e:
        print(f"❌ Error durante la transcripción: {str(e)}")
        print("\n🔍 Ejecutando diagnóstico automático...")
        diagnose_system()
        return
