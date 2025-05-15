import os
import begin
import dspy
from dotenv import load_dotenv
from datetime import datetime
import yaml
from typing import Dict, List
import google.generativeai as genai
from openai import OpenAI
import anthropic
from slugify import slugify
from pathlib import Path

# Cargar variables de entorno
load_dotenv()

# Configurar clientes de API solo si existen las claves
openai_client = None
if os.getenv("OPENAI_API_KEY"):
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if os.getenv("GOOGLE_API_KEY"):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

claude_client = None
if os.getenv("ANTHROPIC_API_KEY"):
    claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Crear directorio para resultados si no existe
RESULTS_DIR = Path("description_results")
RESULTS_DIR.mkdir(exist_ok=True)


def save_as_markdown(data: dict, output_file: str):
    """Guarda los resultados en formato Markdown."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# Descripción para TikTok\n\n")
        f.write(f"**Tema:** {data['topic']}\n\n")
        f.write(f"**Texto Original:**\n\n{data['original_text']}\n\n")
        f.write(f"**Generado el:** {data['timestamp']}\n\n")

        f.write("## Resultados\n\n")
        for model, result in data["results"].items():
            f.write(f"### {model.upper()}\n\n")
            f.write(f"{result}\n\n")
            f.write("---\n\n")


@begin.start
def generate_descriptions(topic, text, output_file=None, markdown=False):
    """
    Genera descripciones para redes sociales usando múltiples modelos de IA.

    Args:
        topic: El tema central a destacar
        text: El fragmento de texto a convertir
        output_file: Archivo donde guardar los resultados (opcional)
        markdown: Si es True, guarda en formato Markdown en lugar de YAML
    """
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
{text}"""

    results = {}
    # Generar con GPT-4 si está disponible
    if openai_client:
        try:
            gpt_response = openai_client.chat.completions.create(
                model="o1-mini", messages=[{"role": "user", "content": prompt}]
            )
            results["o1-mini"] = gpt_response.choices[0].message.content
        except Exception as e:
            results["o1-mini"] = f"Error: {str(e)}"
    else:
        print("⚠️  OpenAI API key no encontrada. Saltando modelo GPT-4.")

    # Generar con Gemini si está disponible
    if os.getenv("GOOGLE_API_KEY"):
        try:
            model = genai.GenerativeModel("gemini-2.5-pro-preview-03-25")
            gemini_response = model.generate_content(prompt)
            results["gemini"] = gemini_response.text
        except Exception as e:
            results["gemini"] = f"Error: {str(e)}"
    else:
        print("⚠️  Google API key no encontrada. Saltando modelo Gemini.")

    # Generar con Claude si está disponible
    if claude_client:
        try:
            claude_response = claude_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}],
            )
            results["claude"] = claude_response.content[0].text
        except Exception as e:
            results["claude"] = f"Error: {str(e)}"
    else:
        print("⚠️  Anthropic API key no encontrada. Saltando modelo Claude.")

    if not results:
        print(
            "❌ No se encontraron claves de API para ningún modelo. No se generaron resultados."
        )
        return

    # Guardar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if output_file is None:
        extension = ".md" if markdown else ".yaml"
        output_file = f"descriptions_{slugify(topic)}_{timestamp}{extension}"

    # Asegurar que el archivo se guarde en la carpeta de resultados
    output_path = RESULTS_DIR / output_file

    output_data = {
        "topic": topic,
        "original_text": text,
        "timestamp": timestamp,
        "results": results,
    }

    if markdown:
        save_as_markdown(output_data, output_path)
    else:
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(output_data, f, allow_unicode=True, sort_keys=False, width=1000)

    print(f"Resultados guardados en: {output_path}")
