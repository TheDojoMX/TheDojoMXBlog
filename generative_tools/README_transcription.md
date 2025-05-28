# Script de Transcripción de Videos

Este script utiliza Deepgram Nova2 para transcribir videos automáticamente.

## Configuración

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar variables de entorno:**
   Crea un archivo `.env` en la raíz del proyecto con:
   ```
   DEEPGRAM_API_KEY=tu_clave_de_api_de_deepgram_aqui
   ```

3. **Obtener clave de API de Deepgram:**
   - Ve a [https://console.deepgram.com/](https://console.deepgram.com/)
   - Crea una cuenta o inicia sesión
   - Genera una nueva clave de API

## Uso

```bash
python generative_tools/video_transcript.py ruta/al/video.mp4
```

### Ejemplos:

```bash
# Transcribir un video específico
python generative_tools/video_transcript.py mi_video.mp4

# Transcribir un video con ruta completa
python generative_tools/video_transcript.py /ruta/completa/al/video.mov
```

## Características

- **Modelo Nova2**: Utiliza el modelo más avanzado de Deepgram
- **Extracción automática de audio**: Funciona con cualquier formato de video compatible con moviepy
- **Organización automática**: Guarda las transcripciones en la carpeta `transcripts/`
- **Formato inteligente**: Incluye puntuación, párrafos y separación por hablantes
- **Idioma español**: Configurado por defecto para español (se puede cambiar en el código)

## Archivos generados

Las transcripciones se guardan en la carpeta `transcripts/` con el formato:
```
transcripts/nombre_del_video_transcript.txt
```

## Formatos de video soportados

Cualquier formato compatible con moviepy:
- MP4
- MOV
- AVI
- MKV
- WMV
- FLV
- Y muchos más...

## Notas

- El script crea automáticamente la carpeta `transcripts` si no existe
- Los archivos de audio temporales se eliminan automáticamente después del procesamiento
- Si hay algún error, se mostrará un mensaje descriptivo 