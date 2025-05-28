#!/usr/bin/env python3
"""
Script para transcribir videos usando Deepgram Nova2.
Extrae el audio del video y genera una transcripción en texto.
"""

import os
import sys
from pathlib import Path
import tempfile
import begin
from dotenv import load_dotenv
from deepgram import DeepgramClient, PrerecordedOptions, FileSource
from moviepy.editor import VideoFileClip

# Cargar variables de entorno
load_dotenv()


@begin.start
def transcribe_video(video_path: str):
    """
    Transcribe un video usando Deepgram Nova2.

    Args:
        video_path: Ruta al archivo de video a transcribir
    """
    # Verificar que el archivo de video existe
    if not os.path.exists(video_path):
        print(f"Error: El archivo {video_path} no existe.")
        sys.exit(1)

    # Obtener la clave de API de Deepgram
    deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")
    if not deepgram_api_key:
        print(
            "Error: DEEPGRAM_API_KEY no está configurada en las variables de entorno."
        )
        sys.exit(1)

    # Crear la carpeta transcripts si no existe
    transcripts_dir = Path("transcripts")
    transcripts_dir.mkdir(exist_ok=True)

    # Obtener el nombre del archivo sin extensión
    video_file = Path(video_path)
    video_name = video_file.stem

    # Nombre del archivo de transcripción
    transcript_file = transcripts_dir / f"{video_name}_transcript.txt"

    print(f"Procesando video: {video_path}")
    print(f"Transcripción se guardará en: {transcript_file}")

    try:
        # Extraer audio del video
        print("Extrayendo audio del video...")
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            temp_audio_path = temp_audio.name

        # Usar moviepy para extraer el audio
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(temp_audio_path, verbose=False, logger=None)
        audio.close()
        video.close()

        print("Audio extraído exitosamente.")

        # Configurar Deepgram
        print("Iniciando transcripción con Deepgram Nova2...")
        deepgram = DeepgramClient(deepgram_api_key)

        # Leer el archivo de audio
        with open(temp_audio_path, "rb") as audio_file:
            buffer_data = audio_file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        # Configurar opciones para Nova2
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            punctuate=True,
            paragraphs=True,
            language="es",  # Español por defecto, cambia si es necesario
            diarize=True,  # Separar por hablantes
            utterances=True,
        )

        # Realizar la transcripción
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

        # Extraer el texto de la transcripción
        transcript_text = ""
        if response.results and response.results.channels:
            for alternative in response.results.channels[0].alternatives:
                if alternative.transcript:
                    transcript_text = alternative.transcript
                    break

        if not transcript_text:
            print("Error: No se pudo obtener la transcripción del audio.")
            sys.exit(1)

        # Guardar la transcripción
        with open(transcript_file, "w", encoding="utf-8") as f:
            f.write(f"Transcripción de: {video_file.name}\n")
            f.write("=" * 50 + "\n\n")
            f.write(transcript_text)

        print(f"✅ Transcripción completada exitosamente!")
        print(f"📄 Archivo guardado en: {transcript_file}")

    except Exception as e:
        print(f"Error durante la transcripción: {str(e)}")
        sys.exit(1)

    finally:
        # Limpiar archivo temporal
        if "temp_audio_path" in locals() and os.path.exists(temp_audio_path):
            os.unlink(temp_audio_path)
            print("Archivo temporal de audio eliminado.")


if __name__ == "__main__":
    begin.start()
