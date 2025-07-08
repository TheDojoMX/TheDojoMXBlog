# 🎤 TTS Optimizer Agent

Un agente especializado para optimizar scripts educativos para síntesis de voz (Text-to-Speech), mejorando la calidad del audio final mediante marcado estratégico, pausas naturales y énfasis apropiado.

## 🎯 Características Principales

### ✨ Optimizaciones TTS
- **Énfasis con Markdown**: Negritas y cursivas para guiar la pronunciación
- **Pausas Estratégicas**: Tags `<break time="Xs"/>` para control temporal
- **Ritmo Natural**: Puntos suspensivos y conectores conversacionales
- **Párrafos Cortos**: Estructura optimizada para procesamiento TTS
- **Términos Técnicos**: Marcado especial para pronunciación correcta

### 🔧 Compatibilidad
- **ElevenLabs**: Optimización específica para su procesamiento
- **Cartesia**: Ajustes para mejor rendimiento
- **Español/Inglés**: Patrones de ritmo específicos por idioma
- **Extensible**: Fácil añadir nuevos proveedores TTS

## 🚀 Uso Rápido

### Script CLI Principal

```bash
# Optimizar un script individual
python generate_tts_script.py optimize projects/mi_proyecto/educational_script.txt

# Optimizar para un proveedor específico
python generate_tts_script.py optimize mi_script.txt -v cartesia

# Optimizar con comparación
python generate_tts_script.py optimize mi_script.txt -c

# Optimizar un proyecto completo
python generate_tts_script.py project projects/mi_proyecto/

# Procesamiento en lote
python generate_tts_script.py batch projects/

# Ver ejemplo de optimización
python generate_tts_script.py demo
```

### Desde Python

```python
from voice_papers.utils.tts_script_generator import generate_tts_script
from pathlib import Path

# Generar script TTS optimizado
optimized_script = generate_tts_script(
    educational_script_path=Path("mi_script.txt"),
    language="Spanish",
    voice_provider="elevenlabs"
)

print(optimized_script)
```

## 📊 Ejemplo de Transformación

### Antes (Script Original)
```
La inteligencia artificial es una tecnología fascinante que está transformando nuestro mundo. Los algoritmos de machine learning pueden procesar grandes cantidades de datos para encontrar patrones complejos. Esto tiene implicaciones importantes para el futuro de la humanidad.
```

### Después (Optimizado para TTS)
```
La **inteligencia artificial** es una tecnología que está ***transformando completamente*** nuestro mundo. <break time="1s"/>

Los algoritmos de *machine learning* pueden procesar grandes cantidades de *datos*... <break time="0.5s"/> 
y es que encuentran patrones complejos que nosotros no podríamos ver. <break time="1s"/>

Esto tiene **implicaciones importantes** para el futuro de la humanidad... <break time="1.5s"/>
Y aquí viene lo interesante...
```

## 🎨 Tipos de Optimización

### 1. Énfasis y Marcado
- `**texto**` - Énfasis fuerte (negrita)
- `*texto*` - Énfasis suave (cursiva)
- `***texto***` - Énfasis máximo (muy ocasional)

### 2. Control de Pausas
- `<break time="0.5s"/>` - Pausa corta
- `<break time="1s"/>` - Pausa media
- `<break time="1.5s"/>` - Pausa larga
- `<break time="2s"/>` - Pausa extra larga

### 3. Ritmo Natural
- `...` - Pausas conversacionales
- `... y es que...` - Conectores explicativos
- `... pero aquí está el detalle...` - Transiciones con suspenso

### 4. Estructura Optimizada
- **Párrafos cortos**: Máximo 3 oraciones
- **Oraciones manejables**: Máximo 25 palabras
- **Términos técnicos**: Marcado para pronunciación
- **Transiciones naturales**: Conectores conversacionales

## 🔧 Configuración Avanzada

### Personalización por Proveedor

```python
# Para ElevenLabs
optimized = generate_tts_script(
    script_path,
    voice_provider="elevenlabs",
    language="Spanish"
)

# Para Cartesia
optimized = generate_tts_script(
    script_path,
    voice_provider="cartesia",
    language="Spanish"
)
```

### Personalización por Idioma

El agente ajusta automáticamente:
- **Español**: "Y es que...", "Resulta que...", "Ahora bien..."
- **Inglés**: "What's interesting is...", "Here's the thing..."
- **Patrones de ritmo**: Específicos para cada idioma

## 📈 Comparación de Resultados

El sistema genera automáticamente estadísticas de optimización:

```
📊 SCRIPT COMPARISON REPORT
==================================================
Original script:
  📝 Words: 1,247
  📄 Paragraphs: 12

TTS-optimized script:
  📝 Words: 1,289
  📄 Paragraphs: 18
  ⏸️  Break tags: 23
  🔊 Bold emphasis: 15
  💬 Italic emphasis: 8
  ⏱️  Ellipsis pauses: 12
  📈 Word count increased by 42

🎯 TTS OPTIMIZATION FEATURES ADDED:
  • Strategic pauses for natural speech rhythm
  • Emphasis markers for vocal stress
  • Shorter paragraphs for better TTS processing
  • Natural conversational connectors
  • Technical term emphasis
```

## 🎵 Patrones de Optimización

### Conectores Conversacionales
- "Y es que..." - Explicaciones
- "Resulta que..." - Revelaciones sorprendentes
- "Ahora bien..." - Cambios de tema
- "Aquí viene lo interesante..." - Engagement

### Pausas Estratégicas
- **Después de afirmaciones importantes**: `<break time="0.5s"/>`
- **Entre conceptos principales**: `<break time="1s"/>`
- **Antes de conclusiones**: `<break time="1.5s"/>`
- **Para efecto dramático**: `<break time="2s"/>`

### Énfasis Técnico
- **Términos clave**: Automáticamente marcados en negrita
- **Conceptos secundarios**: Cursiva para suave énfasis
- **Puntos cruciales**: Triple énfasis (***) usado con moderación

## 🔄 Flujo de Trabajo

1. **Análisis del script original** - Identificación de estructura
2. **Segmentación inteligente** - División en párrafos óptimos
3. **Marcado de términos** - Identificación de conceptos clave
4. **Inserción de pausas** - Colocación estratégica de breaks
5. **Optimización de ritmo** - Añadir conectores naturales
6. **Validación final** - Verificación de fluidez para TTS

## 🛠️ Instalación y Configuración

### Requisitos
```bash
pip install crewai
pip install langchain-openai
pip install click
```

### Variables de Entorno
```bash
export OPENAI_API_KEY=tu_clave_openai
```

### Ejecutar
```bash
# Hacer ejecutable
chmod +x generate_tts_script.py

# Usar directamente
./generate_tts_script.py optimize mi_script.txt
```

## 🎛️ Comandos Disponibles

### `optimize` - Optimizar script individual
```bash
python generate_tts_script.py optimize SCRIPT_PATH [OPTIONS]
```

### `project` - Optimizar proyecto completo
```bash
python generate_tts_script.py project PROJECT_PATH [OPTIONS]
```

### `batch` - Procesamiento en lote
```bash
python generate_tts_script.py batch PROJECTS_DIR [OPTIONS]
```

### `compare` - Comparar scripts
```bash
python generate_tts_script.py compare ORIGINAL_PATH TTS_PATH
```

### `demo` - Ver ejemplo
```bash
python generate_tts_script.py demo
```

## 📁 Estructura de Archivos

```
voice_papers/
├── agents/
│   └── tts_optimizer.py          # Agente principal
├── utils/
│   └── tts_script_generator.py   # Utilidades de generación
└── ...

generate_tts_script.py             # Script CLI principal
TTS_OPTIMIZER_README.md            # Esta documentación
```

## 🔮 Características Futuras

- **Análisis de sentimientos**: Pausas basadas en tono emocional
- **Pronunciación personalizada**: Guías fonéticas automáticas
- **Optimización por voz**: Ajustes específicos para cada voz
- **Métricas de calidad**: Evaluación automática de TTS
- **Integración directa**: Conexión con APIs de síntesis
- **Plantillas personalizables**: Estilos de optimización ajustables

## 🤝 Contribuir

Para añadir nuevos proveedores TTS o idiomas:

1. Editar `get_provider_specific_guidelines()` en `tts_optimizer.py`
2. Añadir patrones de idioma en `get_language_specific_guidelines()`
3. Actualizar las opciones en el CLI
4. Probar con scripts reales

## 📞 Soporte

Para problemas o sugerencias:
- Revisar logs de CrewAI para errores del agente
- Verificar claves API de OpenAI
- Comprobar formato de archivos de entrada
- Consultar ejemplos en `demo` command

---

*El TTS Optimizer Agent es parte del ecosistema Voice Papers, diseñado para crear experiencias de audio educativo de alta calidad mediante optimización inteligente de scripts.* 