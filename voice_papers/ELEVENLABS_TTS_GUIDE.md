# Guía de Optimización TTS para ElevenLabs

## Instrucciones para el Agente Optimizador TTS

### 1. Control de Pausas (Break Tags)

**Uso Correcto:**
```xml
<break time="0.5s" />  <!-- Pausa corta -->
<break time="1.0s" />  <!-- Pausa media -->
<break time="1.5s" />  <!-- Pausa larga -->
<break time="2.0s" />  <!-- Pausa dramática -->
<break time="3.0s" />  <!-- Máximo permitido -->
```

**Mejores Prácticas:**
- Usar con moderación (el exceso causa inestabilidad)
- Máximo 3 segundos por pausa
- Ideal para transiciones y énfasis dramático

### 2. Control de Pronunciación

**Para Modelos con Soporte de Fonemas (Flash v2, Turbo v2, English v1):**
```xml
<phoneme alphabet="cmu-arpabet" ph="M AE1 D IH0 S AH0 N">Madison</phoneme>
<phoneme alphabet="cmu-arpabet" ph="T EH1 K N AH0 L OW0 JH IY0">technology</phoneme>
```

**Para Otros Modelos (Usando Alias):**
```xml
<lexeme>
  <grapheme>AI</grapheme>
  <alias>inteligencia artificial</alias>
</lexeme>

<lexeme>
  <grapheme>ML</grapheme>
  <alias>machine learning</alias>
</lexeme>
```

### 3. Énfasis y Emoción

**NO USAR MARKDOWN** - ElevenLabs no procesa markdown correctamente

**En su lugar, usar:**
- Contexto narrativo para guiar la emoción
- Escritura fonética para énfasis: "increíble" → "increíIble"
- Mayúsculas estratégicas: "ESTO es importante"
- Guiones para separación: "in-cre-í-ble"

### 4. Estructura Óptima

**Párrafos:**
- Máximo 3-4 oraciones por párrafo
- Separar con líneas en blanco
- Cada párrafo debe ser una unidad temática

**Oraciones:**
- Mantener entre 15-25 palabras
- Variar longitud para ritmo natural
- Evitar subordinadas complejas

### 5. Transiciones Naturales

**Conectores Conversacionales:**
- "Y resulta que..." <break time="0.5s" />
- "Pero aquí está lo interesante..." <break time="1.0s" />
- "Ahora bien..." <break time="0.5s" />
- "Lo fascinante es que..." <break time="0.5s" />

### 6. Manejo de Términos Técnicos

**Opciones según el modelo:**

1. **Con soporte de fonemas:**
   ```xml
   El <phoneme alphabet="cmu-arpabet" ph="D IY1 P L ER2 N IH0 NG">deep learning</phoneme> revolucionó...
   ```

2. **Sin soporte de fonemas:**
   ```xml
   El <lexeme><grapheme>deep learning</grapheme><alias>dip lerning</alias></lexeme> revolucionó...
   ```

3. **Escritura fonética simple:**
   - "algorithm" → "algo-ritmo"
   - "neural" → "neu-RAL"

### 7. Control de Velocidad

- Configurar velocidad entre 0.7 y 1.2
- Para contenido técnico: 0.9-1.0
- Para conclusiones importantes: 0.8-0.9

### 8. Checklist de Optimización

- [ ] Eliminar TODO el markdown (**bold**, *italic*, etc.)
- [ ] Reemplazar énfasis con técnicas fonéticas o mayúsculas
- [ ] Añadir break tags en transiciones importantes
- [ ] Usar phoneme/lexeme tags para términos difíciles
- [ ] Verificar longitud de oraciones (15-25 palabras)
- [ ] Separar párrafos claramente
- [ ] Incluir conectores conversacionales naturales
- [ ] NO usar más de 5-6 break tags por minuto de audio

### 9. Ejemplos de Transformación

**INCORRECTO (con markdown):**
```
La **inteligencia artificial** está *transformando* nuestro mundo.
```

**CORRECTO (optimizado para ElevenLabs):**
```
La INTELIGENCIA ARTIFICIAL <break time="0.5s" /> está trans-for-MAN-do nuestro mundo.
```

**INCORRECTO (pausas excesivas):**
```
Esto <break time="1s" /> es <break time="1s" /> muy <break time="1s" /> importante.
```

**CORRECTO (pausas estratégicas):**
```
Esto es muy importante. <break time="1.5s" /> Porque cambia todo lo que sabíamos.
```

### 10. Formato Final

El texto optimizado debe:
- Ser limpio y legible
- Usar solo tags XML de ElevenLabs
- NO contener markdown
- Fluir naturalmente al leerlo
- Estar listo para enviar directamente a la API