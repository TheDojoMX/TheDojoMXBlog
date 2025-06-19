#!/usr/bin/env python3
"""
Script de transcripción segura - permite cancelar el proceso si se queda trabado
"""

import os
import sys
import time
import signal
import threading
from pathlib import Path
from video_clipper import VideoClipper


class SafeTranscriber:
    def __init__(self):
        self.process_cancelled = False
        self.current_step = ""

    def signal_handler(self, signum, frame):
        """Maneja la señal de cancelación (Ctrl+C)."""
        print(f"\n\n🛑 Proceso cancelado por el usuario en paso: {self.current_step}")
        print("🧹 Limpiando archivos temporales...")
        self.process_cancelled = True
        sys.exit(0)

    def progress_monitor(self, timeout_seconds=600):  # 10 minutos de timeout
        """Monitor que cancela el proceso si se queda trabado."""
        start_time = time.time()

        while not self.process_cancelled:
            elapsed = time.time() - start_time

            if elapsed > timeout_seconds:
                print(
                    f"\n⏰ TIMEOUT: El proceso ha tardado más de {timeout_seconds/60:.1f} minutos"
                )
                print(f"🛑 Paso actual: {self.current_step}")
                print("💡 Considera usar un video más corto o verificar tu conexión")
                self.process_cancelled = True
                os._exit(1)

            time.sleep(5)  # Verificar cada 5 segundos

    def safe_transcribe(self, video_path):
        """Transcribe un video de manera segura con monitoreo."""

        # Configurar manejador de señales
        signal.signal(signal.SIGINT, self.signal_handler)

        # Iniciar monitor de progreso en hilo separado
        monitor_thread = threading.Thread(target=self.progress_monitor, daemon=True)
        monitor_thread.start()

        try:
            print(f"🎬 Iniciando transcripción segura de: {video_path}")
            print("💡 Presiona Ctrl+C para cancelar en cualquier momento\n")

            # Verificar que el archivo existe
            if not os.path.exists(video_path):
                print(f"❌ Archivo no encontrado: {video_path}")
                return False

            # Crear clipper
            self.current_step = "Inicializando VideoClipper"
            print(f"📋 {self.current_step}...")
            clipper = VideoClipper(video_path)

            # Verificar duración del video
            self.current_step = "Obteniendo duración del video"
            print(f"📋 {self.current_step}...")
            duration = clipper.get_video_duration()
            print(f"⏱️ Duración: {duration:.2f} segundos ({duration/60:.1f} minutos)")

            if duration > 1800:  # 30 minutos
                print("⚠️ Video muy largo (>30 min) - esto puede tardar mucho tiempo")
                response = input("¿Continuar? (y/N): ")
                if response.lower() != "y":
                    print("🛑 Cancelado por el usuario")
                    return False

            # Iniciar transcripción
            self.current_step = "Transcribiendo con timestamps"
            print(f"📋 {self.current_step}...")
            print("⏳ Este es el paso que más tiempo toma...")

            start_time = time.time()
            transcript = clipper.transcribe_video_with_timestamps()
            transcription_time = time.time() - start_time

            if transcript:
                print(
                    f"✅ Transcripción completada en {transcription_time:.2f} segundos"
                )
                print(f"📝 Longitud: {len(transcript)} caracteres")

                # Verificar si tenemos timestamps
                if clipper.transcript_with_timestamps:
                    words_count = len(
                        clipper.transcript_with_timestamps.get("words", [])
                    )
                    segments_count = len(
                        clipper.transcript_with_timestamps.get("segments", [])
                    )

                    if words_count > 0:
                        print(f"🕐 Timestamps por palabra: {words_count}")
                    elif segments_count > 0:
                        print(f"🕐 Timestamps por segmento: {segments_count}")
                    else:
                        print("⚠️ Sin timestamps - usará método proporcional")

                return True
            else:
                print("❌ La transcripción falló")
                return False

        except KeyboardInterrupt:
            print("\n🛑 Proceso cancelado por el usuario")
            return False
        except Exception as e:
            print(f"\n❌ Error durante la transcripción: {str(e)}")
            print(f"🛑 Paso que falló: {self.current_step}")
            return False
        finally:
            self.process_cancelled = True


def main():
    """Función principal."""
    if len(sys.argv) < 2:
        print("❌ Uso: python safe_transcribe.py <ruta_del_video>")
        print("💡 Ejemplo: python safe_transcribe.py clips_verticales/mi_video.mp4")
        sys.exit(1)

    video_path = sys.argv[1]

    # Verificar configuración
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY no configurado")
        print("💡 Configura tu API key de OpenAI antes de continuar")
        sys.exit(1)

    # Ejecutar transcripción segura
    transcriber = SafeTranscriber()
    success = transcriber.safe_transcribe(video_path)

    if success:
        print("\n🎉 Transcripción completada exitosamente!")
        print("📁 Revisa los archivos generados en:")
        print(f"   - transcripciones/{Path(video_path).stem}_transcript.txt")
        print(
            f"   - transcripciones/{Path(video_path).stem}_transcript_with_timestamps.json"
        )
    else:
        print("\n❌ La transcripción falló o fue cancelada")


if __name__ == "__main__":
    main()
