import os
import begin
import dspy
from dotenv import load_dotenv
from datetime import datetime
import json
from typing import Dict, List
import google.generativeai as genai
from openai import OpenAI
import anthropic
from slugify import slugify

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


@begin.start
def generate_descriptions(topic, text, output_file=None):
    """
    Genera descripciones para redes sociales usando múltiples modelos de IA.

    Args:
        topic: El tema central a destacar
        text: El fragmento de texto a convertir
        output_file: Archivo donde guardar los resultados (opcional)
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
            model = genai.GenerativeModel("gemini-pro")
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
        output_file = f"descriptions_{slugify(topic)}_{timestamp}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "topic": topic,
                "original_text": text,
                "timestamp": timestamp,
                "results": results,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Resultados guardados en: {output_file}")


# if __name__ == "__main__":
#     generate_descriptions()
