# 🎛️ Mejoras de Estabilidad y Calidad de Voz

## ✨ Nuevas Características

Se han agregado parámetros avanzados de control de calidad para la síntesis de voz con ElevenLabs:

### 🎚️ Parámetros de Calidad

#### **Stability** (Estabilidad)
- **Rango**: 0.0 - 1.0
- **Predeterminado**: 0.65
- **Descripción**: Controla la consistencia vs. expresividad de la voz
- **Uso**:
  - **Alto (0.7-0.9)**: Para narraciones profesionales, podcasts, contenido educativo
  - **Medio (0.5-0.7)**: Balance entre estabilidad y expresión
  - **Bajo (0.3-0.5)**: Para contenido dramático, emocional, conversacional

#### **Similarity Boost** (Mejora de Similitud)
- **Rango**: 0.0 - 1.0
- **Predeterminado**: 0.8
- **Descripción**: Qué tan similar debe ser la voz generada a la voz original
- **Uso**:
  - **Alto (0.8-1.0)**: Para máxima fidelidad a la voz original
  - **Medio (0.6-0.8)**: Permite variación manteniendo el carácter
  - **Bajo (0.3-0.6)**: Más variación creativa

#### **Style** (Estilo)
- **Rango**: 0.0 - 1.0
- **Predeterminado**: 0.0
- **Descripción**: Nivel de exageración del estilo original
- **Uso**:
  - **0.0**: Máxima estabilidad (recomendado)
  - **0.1-0.3**: Ligera expresión adicional
  - **0.4+**: Puede reducir la estabilidad

#### **Speaker Boost** (Mejora del Hablante)
- **Tipo**: Boolean
- **Predeterminado**: True
- **Descripción**: Mejora la claridad y similitud con el hablante original
- **Recomendación**: Siempre habilitado para mejor calidad

## 🖥️ Uso desde CLI

### Ejemplos Básicos

```bash
# Configuración para narración profesional
voice-papers paper.pdf \
  --stability 0.8 \
  --similarity-boost 0.9 \
  --style 0.0 \
  --speaker-boost

# Configuración para contenido expresivo
voice-papers paper.pdf \
  --stability 0.4 \
  --similarity-boost 0.7 \
  --style 0.15 \
  --speaker-boost

# Usando valores predeterminados optimizados
voice-papers paper.pdf  # Sin parámetros adicionales
```

### Todas las Opciones de Voz

```bash
voice-papers input.pdf \
  --voice hectorip \
  --model multilingual \
  --stability 0.65 \
  --similarity-boost 0.8 \
  --style 0.0 \
  --speaker-boost \
  --tone academic \
  --duration 10
```

## 💻 Uso Programático

```python
from voice_papers.voice.synthesizer import get_synthesizer

# Crear sintetizador
synthesizer = get_synthesizer("elevenlabs")

# Síntesis con parámetros personalizados
success = synthesizer.synthesize(
    text="Tu texto aquí",
    output_path=Path("output.mp3"),
    voice_name="hectorip",
    model="flash",
    stability=0.75,           # Alta estabilidad
    similarity_boost=0.85,    # Alta similitud
    style=0.0,               # Sin exageración de estilo
    use_speaker_boost=True   # Mejora de claridad
)
```

## 🎯 Configuraciones Recomendadas

### 📚 **Contenido Educativo/Académico**
```python
stability=0.8
similarity_boost=0.9
style=0.0
use_speaker_boost=True
```
- Máxima claridad y consistencia
- Ideal para explicaciones técnicas

### 🎙️ **Podcasts/Narraciones**
```python
stability=0.7
similarity_boost=0.8
style=0.0
use_speaker_boost=True
```
- Balance entre naturalidad y consistencia
- Sonido profesional

### 🎭 **Contenido Dramático/Emocional**
```python
stability=0.4
similarity_boost=0.7
style=0.15
use_speaker_boost=True
```
- Más expresión y variación emocional
- Mantiene la calidad

### ⚡ **Uso General (Predeterminado)**
```python
stability=0.65
similarity_boost=0.8
style=0.0
use_speaker_boost=True
```
- Configuración optimizada para la mayoría de casos

## 🔧 Características Técnicas

### Mejoras Implementadas

1. **Configuración por Defecto Optimizada**: Valores predeterminados basados en mejores prácticas
2. **Formato de Alta Calidad**: Output en `mp3_44100_128` automáticamente
3. **Logging Detallado**: Muestra la configuración de calidad utilizada
4. **Compatibilidad Completa**: Los parámetros son opcionales, código existente sigue funcionando
5. **Validación de Rangos**: Verificación automática de valores válidos en CLI

### Configuración Predeterminada

```python
DEFAULT_VOICE_SETTINGS = {
    "stability": 0.65,        # Balance óptimo
    "similarity_boost": 0.8,  # Alta fidelidad
    "style": 0.0,            # Máxima estabilidad
    "use_speaker_boost": True # Mejor claridad
}
```

## 📊 Comparación de Resultados

| Configuración | Claridad | Consistencia | Expresividad | Uso Ideal |
|---------------|----------|--------------|--------------|-----------|
| **Profesional** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | Educativo, corporativo |
| **Equilibrada** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Podcasts, general |
| **Expresiva** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Narrativa, dramático |

## 🔍 Solución de Problemas

### Audio Inconsistente
- **Incrementa** `stability` (0.7-0.9)
- **Reduce** `style` (0.0-0.1)

### Audio Muy Monótono
- **Reduce** `stability` (0.4-0.6)
- **Incrementa** `style` (0.1-0.2)

### Baja Calidad de Voz
- **Incrementa** `similarity_boost` (0.8-1.0)
- **Habilita** `use_speaker_boost`

### Artefactos de Audio
- **Reduce** `style` a 0.0
- **Incrementa** `stability`

## 🚀 Ejemplo Completo

```bash
# Ejecutar el ejemplo incluido
python examples/ejemplo_estabilidad.py

# Esto generará 4 archivos de audio con diferentes configuraciones:
# - ejemplo_default.mp3 (configuración predeterminada)
# - ejemplo_muy_estable.mp3 (máxima estabilidad)
# - ejemplo_expresivo.mp3 (más emocional)
# - ejemplo_equilibrado.mp3 (balance óptimo)
```

¡Ahora puedes obtener exactamente la calidad de voz que necesitas para cada proyecto! 🎯 