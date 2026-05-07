# Capitulo 2: El Loop Agentico Es un While True Bien Pensado

> "Tu agente es un loop. La diferencia entre un loop util y uno destructivo es el diseno."

---

Todo agente de IA, desde un chatbot que busca en Google hasta un sistema autonomo que escribe y despliega codigo, se reduce a lo mismo: un loop. Percibir el estado del mundo, razonar sobre que hacer, ejecutar una accion y observar el resultado. Repetir hasta terminar --o hasta que algo salga mal.

Este ciclo es tan fundamental para los agentes de IA como el ciclo **fetch-decode-execute** lo es para un procesador. Asi como una CPU repite incansablemente el proceso de buscar la siguiente instruccion, decodificarla y ejecutarla, un agente repite el proceso de observar, pensar y actuar. Y asi como entender el ciclo de un procesador es clave para entender la computacion, entender el loop agentico es clave para construir agentes que funcionen.

En el Capitulo 1 definimos que es un agente: un sistema que percibe, razona y actua. Ahora vamos a abrir el capo y mirar el motor. En este capitulo desarmaremos el loop pieza por pieza. Exploraremos sus origenes en la teoria de control y la cibernetica, analizaremos el framework ReAct que lo popularizo en el mundo de los LLMs, implementaremos un agente completo desde cero en Python puro, y confrontaremos el problema mas profundo: decidir cuando parar.

Al final, tendras un agente ejecutable de menos de 100 lineas, sin frameworks, que puedes usar como punto de partida para cualquier proyecto.

---

## 2.1 Del ciclo OODA al PID al ReAct: la misma idea en tres siglos

El loop agentico no nacio con los LLMs. Sus raices se extienden decadas --incluso siglos-- atras, hasta la teoria de control, la cibernetica y la doctrina militar. Antes de hablar de `Thought -> Action -> Observation`, necesitamos hablar de tres ideas fundamentales que lo preceden.

### El ciclo OODA de John Boyd

En los anos 60, el coronel John Boyd de la Fuerza Aerea de Estados Unidos desarrollo un modelo para entender como los pilotos de combate toman decisiones bajo presion extrema. Lo llamo el **ciclo OODA**: **Observe, Orient, Decide, Act** (Observar, Orientar, Decidir, Actuar).

La idea central de Boyd era simple pero poderosa: el combatiente que recorre este ciclo mas rapido que su oponente gana. No importa si tu avion es mas rapido o tu armamento es superior. Si el otro piloto observa la situacion, se orienta, decide y actua antes que tu, estas perdido.

Lo interesante del modelo de Boyd es la fase de **orientacion**. No es simplemente "mirar los datos". Es filtrar la informacion a traves de tu experiencia previa, tu cultura, tu entrenamiento, tus modelos mentales. Es la fase donde conviertes datos crudos en comprension. Hay una analogia util --aunque imperfecta-- con lo que hace un LLM cuando recibe un prompt con contexto: filtra la informacion a traves de representaciones aprendidas durante el entrenamiento para generar una respuesta.

Vale notar que Boyd nunca publico sus ideas en papers revisados por pares; las presento en briefings y documentos internos que circularon informalmente. La analogia con OODA tiene valor como intuicion, no como especificacion tecnica.

### El loop de control PID

En ingenieria de control, el controlador **PID** (Proporcional-Integral-Derivativo) es quizas el mecanismo de retroalimentacion mas exitoso de la historia. Tu aire acondicionado, el control de crucero de tu carro, un drone manteniendose estable en el aire: todos usan alguna variante de este loop.

El principio es elegante:

1. **Mides** el estado actual del sistema (la temperatura de la habitacion)
2. **Calculas** el error: la diferencia entre el estado actual y el estado deseado (faltan 3 grados para llegar a 22 grados C)
3. **Aplicas** una correccion proporcional al error (inyecta mas frio)
4. **Repites**

Lo crucial aqui es el concepto de **retroalimentacion negativa**: cada accion reduce la brecha entre donde estas y donde quieres estar. El sistema converge porque cada iteracion del loop lo acerca al objetivo. Esta es exactamente la misma intuicion detras de un agente que observa el resultado de su ultima accion y decide si necesita hacer mas o si ya termino.

El PID tiene una ventaja que los agentes de IA envidian: convergencia garantizada bajo condiciones conocidas. Si tu sistema es lineal e invariante en el tiempo, puedes demostrar matematicamente que el controlador PID va a converger al valor deseado. Con un agente LLM no tienes esa garantia. El LLM puede decidir en cualquier momento que necesita "investigar un poco mas", y tu loop diverge en lugar de converger.

### La cibernetica de Norbert Wiener

Norbert Wiener, en su libro *Cybernetics* (1948), formalizo la idea de que los sistemas inteligentes, sean biologicos o mecanicos, funcionan a traves de **ciclos de retroalimentacion**. Wiener argumentaba que la diferencia entre un sistema "inteligente" y uno mecanico no esta en sus componentes, sino en su capacidad para usar la informacion sobre sus propias acciones para ajustar su comportamiento futuro.

Esta idea fue revolucionaria. Antes de Wiener, la ingenieria pensaba en sistemas abiertos: entrada, proceso, salida. Wiener cerro el loop y dijo: la salida afecta la siguiente entrada. Y ese cierre del loop es lo que produce comportamiento aparentemente inteligente.

### La conexion con Polya

Hay una conexion que no quiero dejar pasar. George Polya, en su clasico *How to Solve It* (1945), propuso cuatro fases para resolver cualquier problema:

1. **Entender** el problema
2. **Concebir un plan**
3. **Ejecutar** el plan
4. **Verificar** el resultado

Observar, orientar/planear, actuar, verificar. Es el mismo loop. La resolucion de problemas, ya sea por un matematico, un piloto de combate, un termostato o un agente de IA, sigue la misma estructura fundamental: un ciclo de percepcion, razonamiento, accion y retroalimentacion.

La retroalimentacion es la estructura fundamental del comportamiento dirigido a un objetivo. Sin el paso de verificacion, sin cerrar el loop, simplemente estas ejecutando instrucciones a ciegas.

### El patron comun

Lo que une a OODA, PID, Wiener y Polya es un patron que precede a todos ellos:

```
percibir -> razonar -> actuar -> observar -> repetir
```

Este patron emerge independientemente en dominios tan distintos como la doctrina militar, la ingenieria de control, la cibernetica y la heuristica matematica. Eso no es coincidencia. Es evidencia de que el ciclo de retroalimentacion es una estructura fundamental para cualquier sistema que interactua con un ambiente y persigue un objetivo.

Los agentes de IA son la encarnacion mas reciente de esta idea ancestral.

---

## 2.2 ReAct: el loop canonico de los agentes LLM

En octubre de 2022, Shunyu Yao y sus colegas de Princeton publicaron el paper "ReAct: Synergizing Reasoning and Acting in Language Models" [Yao et al., 2022]. Este paper establecio el framework conceptual que domina la arquitectura de agentes de IA hasta hoy.

### La intuicion detras de ReAct

Antes de ReAct, habia dos lineas de investigacion separadas. Por un lado, el **chain-of-thought prompting** [Wei et al., 2022] mostraba que hacer que los LLMs "piensen en voz alta" mejoraba dramaticamente su rendimiento en tareas de razonamiento. Por otro lado, la investigacion en **agentes autonomos** exploraba como los LLMs podian usar herramientas y APIs para interactuar con el mundo.

La contribucion de ReAct fue unir ambas ideas en un solo loop:

1. **Thought** (Pensamiento): El agente razona explicitamente sobre la situacion actual, que informacion necesita y cual deberia ser su siguiente paso.
2. **Action** (Accion): El agente ejecuta una accion concreta: buscar en una API, consultar una base de datos, ejecutar codigo, llamar a una herramienta.
3. **Observation** (Observacion): El agente recibe el resultado de su accion y lo incorpora a su contexto.

Y luego el loop se repite: el agente genera un nuevo pensamiento basado en la observacion, decide la siguiente accion, observa el resultado, y asi sucesivamente hasta que decide que tiene una respuesta final.

Los resultados empiricos de ReAct fueron convincentes. En HotpotQA (razonamiento multi-salto con preguntas que requieren buscar en Wikipedia), ReAct supero tanto al chain-of-thought puro como a los enfoques de solo-accion. En tareas de decision interactiva como ALFWorld y WebShop, ReAct supero a metodos basados en aprendizaje por refuerzo e imitacion por margenes absolutos del 34% y 10% respectivamente, con apenas uno o dos ejemplos de contexto [Yao et al., 2022].

### Por que funciona: la separacion de concerns

La genialidad de ReAct esta en algo que los programadores conocemos bien: la **separacion de responsabilidades**. Al separar explicitamente el razonamiento (Thought) de la ejecucion (Action), el sistema obtiene varias ventajas:

**Trazabilidad**: Puedes ver exactamente por que el agente tomo cada decision. No es una caja negra que misteriosamente produce un resultado. Cada paso tiene un pensamiento asociado que explica la logica.

**Recuperacion de errores**: Si una accion falla o devuelve informacion inesperada, el paso de Thought permite al agente re-evaluar su estrategia en lugar de continuar ciegamente. Esto es analogo al principio de Polya de verificar el resultado antes de continuar.

**Grounding**: Al anclar el razonamiento en observaciones reales del mundo (resultados de APIs, contenido de archivos, respuestas de bases de datos), el agente reduce las alucinaciones. No esta inventando hechos; esta razonando sobre datos reales.

Como vimos en el Capitulo 1, los agentes son sistemas que perciben, razonan y actuan. La separacion entre la "inteligencia" (el LLM razonando) y la "logica" (las herramientas ejecutando acciones concretas) es un principio fundamental para construir sistemas robustos. ReAct es la encarnacion mas pura de este principio.

---

## 2.3 Anatomia del ciclo Thought-Action-Observation

Veamos como se ve el loop ReAct en su forma mas basica. No necesitas LangChain ni ningun framework para entender la mecanica:

```python
def react_loop(llm, tools, question, max_steps=10):
    """El loop ReAct en su forma mas pura.

    Args:
        llm: cliente del LLM con metodo .generate(prompt) -> str
        tools: dict de {nombre: herramienta} con metodo .execute(args)
        question: la pregunta o tarea del usuario
        max_steps: limite de iteraciones (heuristica de terminacion)

    Returns:
        La respuesta final del agente, o un mensaje de error.
    """
    # El historial acumula thoughts, actions y observations
    history = f"Pregunta: {question}\n"

    for step in range(max_steps):
        # THOUGHT: el LLM razona sobre que hacer
        prompt = f"""{history}
Genera tu siguiente pensamiento y accion.
Formato:
Thought: [tu razonamiento]
Action: [nombre_herramienta(argumentos)]
Si ya tienes la respuesta final:
Thought: [razonamiento final]
Answer: [respuesta]"""

        response = llm.generate(prompt)

        # Si el LLM decidio que ya tiene la respuesta
        if "Answer:" in response:
            return extract_answer(response)

        # ACTION: extraer y ejecutar la accion
        thought = extract_thought(response)
        action_name, action_args = extract_action(response)
        history += f"\nThought: {thought}\n"
        history += f"Action: {action_name}({action_args})\n"

        # OBSERVATION: ejecutar la herramienta y obtener resultado
        try:
            observation = tools[action_name].execute(action_args)
        except Exception as e:
            observation = f"Error: {e}"

        history += f"Observation: {observation}\n"

    return "Error: se alcanzo el limite de pasos sin respuesta"
```

Observa la estructura: es literalmente un `for` loop con tres pasos internos. Todo el "magic" de los agentes de IA se reduce a esto. El LLM genera texto que se parsea para extraer acciones, las acciones se ejecutan, y los resultados se agregan al contexto para la siguiente iteracion.

Hay tres funciones auxiliares que hacen el parsing del texto:

```python
import re

def extract_thought(response: str) -> str:
    """Extrae el pensamiento del LLM."""
    match = re.search(r"Thought:\s*(.+?)(?:\n|$)", response, re.DOTALL)
    return match.group(1).strip() if match else ""

def extract_action(response: str) -> tuple[str, str]:
    """Extrae nombre de herramienta y argumentos."""
    match = re.search(r"Action:\s*(\w+)\((.+?)\)", response)
    if match:
        return match.group(1), match.group(2)
    raise ValueError(f"No se pudo extraer accion de: {response}")

def extract_answer(response: str) -> str:
    """Extrae la respuesta final."""
    match = re.search(r"Answer:\s*(.+)", response, re.DOTALL)
    return match.group(1).strip() if match else response
```

El parsing es deliberadamente simple. En produccion, usarias el mecanismo nativo de tool calling de tu proveedor de LLM (OpenAI function calling, Anthropic tool use, etc.), que devuelve JSON estructurado en lugar de texto libre. Pero la mecanica del loop es identica.

### El flujo de datos

Para visualizar el flujo, piensa en tres "carriles" que corren en paralelo:

```
Paso 1:
  Thought:      "Necesito buscar informacion sobre X"
  Action:       search("X")
  Observation:  "X es un framework para Y, creado en 2023..."

Paso 2:
  Thought:      "Ahora necesito saber como se instala X"
  Action:       search("instalar X")
  Observation:  "Para instalar X, ejecuta: pip install x..."

Paso 3:
  Thought:      "Tengo toda la informacion necesaria"
  Answer:       "X es un framework para Y. Se instala con pip install x..."
```

Cada paso genera exactamente un pensamiento, una accion y una observacion. El historial completo se pasa al LLM en cada iteracion, lo que le permite razonar sobre todo lo que ha hecho hasta ahora. Esto es crucial: el agente tiene "memoria" de sus acciones previas porque el historial crece con cada paso.

Pero esa memoria tiene un costo. Cada paso agrega tokens al historial. En un agente que ejecuta 15 pasos, el historial puede crecer a decenas de miles de tokens. En el Capitulo 3 veremos por que esto es un problema serio y como manejarlo.

---

## 2.4 Implementa un agente minimo en Python puro

Vamos a construir un agente funcional completo en menos de 100 lineas. Este agente puede buscar informacion y hacer calculos simples. No usa ningun framework: solo Python estandar y una API de LLM.

```python
"""
agente_minimo.py - Un agente ReAct completo en Python puro.
Requisitos: pip install openai
Uso: python agente_minimo.py "Cual es la poblacion de Mexico multiplicada por 2?"
"""

import json
import re
import sys
import math
from openai import OpenAI

# --- Herramientas ---

class SearchTool:
    """Busqueda simulada (reemplaza con una API real)."""
    name = "search"
    description = "Busca informacion. Uso: search(consulta)"

    # Base de conocimiento minima para demostrar el concepto
    KB = {
        "poblacion mexico": "La poblacion de Mexico es aproximadamente 130 millones (2024).",
        "poblacion brasil": "La poblacion de Brasil es aproximadamente 216 millones (2024).",
        "capital francia": "La capital de Francia es Paris.",
    }

    def execute(self, query: str) -> str:
        query_lower = query.lower().strip('"').strip("'")
        for key, value in self.KB.items():
            if key in query_lower:
                return value
        return f"No se encontro informacion sobre: {query}"


class CalculatorTool:
    """Calculadora segura."""
    name = "calculator"
    description = "Evalua expresiones matematicas. Uso: calculator(expresion)"

    SAFE_NAMES = {
        "abs": abs, "round": round, "min": min, "max": max,
        "sum": sum, "pow": pow, "sqrt": math.sqrt,
        "pi": math.pi, "e": math.e,
    }

    def execute(self, expression: str) -> str:
        expr = expression.strip('"').strip("'")
        try:
            result = eval(expr, {"__builtins__": {}}, self.SAFE_NAMES)
            return str(result)
        except Exception as e:
            return f"Error en calculo: {e}"


# --- Motor del agente ---

SYSTEM_PROMPT = """Eres un agente de investigacion. Resuelve la tarea del usuario
usando las herramientas disponibles.

Herramientas:
- search(consulta): busca informacion
- calculator(expresion): evalua expresiones matematicas

En cada paso, responde con EXACTAMENTE este formato:
Thought: [tu razonamiento sobre que hacer]
Action: [herramienta(argumentos)]

Cuando tengas la respuesta final:
Thought: [razonamiento final]
Answer: [tu respuesta completa]

IMPORTANTE: Usa solo UNA accion por paso. No inventes datos."""


def run_agent(question: str, max_steps: int = 8) -> str:
    """Ejecuta el agente ReAct."""
    client = OpenAI()  # Usa OPENAI_API_KEY del entorno
    tools = {t.name: t for t in [SearchTool(), CalculatorTool()]}

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    for step in range(max_steps):
        # Llamar al LLM
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.0,
            max_tokens=500,
        )
        text = response.choices[0].message.content

        # Verificar si hay respuesta final
        if "Answer:" in text:
            answer = re.search(r"Answer:\s*(.+)", text, re.DOTALL)
            print(f"\n--- Paso {step + 1}: RESPUESTA FINAL ---")
            print(text)
            return answer.group(1).strip() if answer else text

        # Extraer y ejecutar accion
        action_match = re.search(r"Action:\s*(\w+)\((.+?)\)", text)
        if not action_match:
            messages.append({"role": "assistant", "content": text})
            messages.append({
                "role": "user",
                "content": "Formato incorrecto. Usa: Action: herramienta(args)"
            })
            continue

        tool_name = action_match.group(1)
        tool_args = action_match.group(2)

        print(f"\n--- Paso {step + 1} ---")
        print(f"Thought: {re.search(r'Thought:(.+?)Action:', text, re.DOTALL).group(1).strip() if re.search(r'Thought:(.+?)Action:', text, re.DOTALL) else '?'}")
        print(f"Action: {tool_name}({tool_args})")

        # Ejecutar herramienta
        if tool_name not in tools:
            observation = f"Error: herramienta '{tool_name}' no existe."
        else:
            observation = tools[tool_name].execute(tool_args)

        print(f"Observation: {observation}")

        # Agregar al historial
        messages.append({"role": "assistant", "content": text})
        messages.append({
            "role": "user",
            "content": f"Observation: {observation}"
        })

    return "Error: limite de pasos alcanzado sin respuesta."


if __name__ == "__main__":
    question = sys.argv[1] if len(sys.argv) > 1 else (
        "Cual es la poblacion de Mexico multiplicada por 2?"
    )
    print(f"Pregunta: {question}\n")
    result = run_agent(question)
    print(f"\nResultado final: {result}")
```

Son 95 lineas de codigo funcional (sin contar comentarios ni lineas en blanco). No hay magia. No hay framework. Es un `for` loop que alterna entre llamar al LLM y ejecutar herramientas.

Para ejecutarlo:

```bash
export OPENAI_API_KEY="tu-api-key"
python agente_minimo.py "Cual es la poblacion de Mexico multiplicada por 2?"
```

El agente producira algo como:

```
Pregunta: Cual es la poblacion de Mexico multiplicada por 2?

--- Paso 1 ---
Thought: Necesito buscar la poblacion de Mexico primero.
Action: search("poblacion mexico")
Observation: La poblacion de Mexico es aproximadamente 130 millones (2024).

--- Paso 2 ---
Thought: Ahora necesito multiplicar 130 millones por 2.
Action: calculator(130_000_000 * 2)
Observation: 260000000

--- Paso 3: RESPUESTA FINAL ---
Thought: Ya tengo la informacion necesaria para responder.
Answer: La poblacion de Mexico es aproximadamente 130 millones.
Multiplicada por 2, el resultado es 260,000,000 (260 millones).

Resultado final: La poblacion de Mexico es aproximadamente 130 millones.
Multiplicada por 2, el resultado es 260,000,000 (260 millones).
```

Tres pasos. Dos llamadas a herramientas. Una respuesta correcta. Este agente minimo es tu punto de referencia. A lo largo del libro lo iremos extendiendo con guardrails, memoria, observabilidad y control de costos.

---

## 2.5 El problema de la terminacion: cuando tu agente no sabe parar

Aqui llegamos al problema mas profundo y mas dificil del loop agentico. Un loop que se ejecuta es util. Un loop que no se detiene es un desastre. Como vimos en el Capitulo 0 con el agente que hizo 847 llamadas a una API en 45 minutos, la diferencia entre un agente productivo y uno destructivo a menudo es la respuesta a una sola pregunta: **cuando debe parar?**

### El halting problem y los agentes

En 1936, Alan Turing demostro uno de los resultados mas fundamentales de las ciencias de la computacion: es **imposible** construir un algoritmo general que determine si cualquier programa arbitrario va a terminar o ejecutarse para siempre. Este es el famoso **problema de la parada** (halting problem).

Un agente de IA es un programa. Un agente ejecutando un loop ReAct es, en esencia, una maquina que decide en cada paso si continuar o detenerse basandose en su propio estado. El resultado de Turing nos dice que **no existe un metodo general** para determinar si un agente arbitrario va a terminar. En la practica, para un agente concreto con un limite de iteraciones, la terminacion es trivialmente garantizable. Pero un agente sin esos limites, que decide dinamicamente si continuar, hereda la indecidibilidad del problema general.

La equivalencia entre maquinas de Turing y programas reales descansa en la tesis de Church-Turing, que es una tesis ampliamente aceptada, no un teorema demostrado. Pero sus implicaciones practicas son claras.

### Las cuatro formas en que tu agente no sabe parar

En la practica, el problema se manifiesta de formas concretas y dolorosas:

1. **Loops infinitos de herramientas**: El agente busca informacion, no la encuentra, la busca de otra manera, no la encuentra, y repite ad infinitum.

2. **Ciclos de auto-correccion**: El agente detecta un error, intenta corregirlo, introduce un nuevo error, intenta corregir ese, y asi sucesivamente.

3. **Indecision**: El agente no puede determinar si tiene suficiente informacion para responder y sigue buscando mas datos indefinidamente.

4. **Perfeccionismo**: El agente sigue refinando una respuesta que ya es suficientemente buena, consumiendo recursos sin mejorar significativamente la calidad.

### Heuristicas de terminacion

Como no podemos resolver el problema de la parada en general, hacemos lo que siempre hacemos en ciencias de la computacion cuando nos topamos con un problema intratable: usamos **heuristicas**. Estrategias que funcionan razonablemente bien en la practica, aunque no garantizan la solucion optima en todos los casos.

**1. Limite maximo de pasos (`max_steps`)**

La mas simple y la mas importante. Estableces un numero maximo de iteraciones y el agente se detiene cuando lo alcanza, sin importar que. Es brutal pero efectivo: garantiza que el agente siempre termina.

```python
MAX_STEPS = 15  # Nunca mas de 15 iteraciones

for step in range(MAX_STEPS):
    result = agent_step()
    if result.is_final:
        return result

return "Limite de pasos alcanzado sin respuesta definitiva"
```

En la practica, la mayoria de los agentes en produccion necesitan menos de 10 pasos para completar sus tareas. Shankar et al. [2025] encuestaron a 306 practicantes y encontraron que el 68% de los agentes ejecutan un maximo de 10 pasos. Si tu agente necesita regularmente mas de 15 pasos, probablemente necesitas redisenar la tarea, no aumentar el limite.

**2. Deteccion de ciclos**

Monitorear si el agente esta repitiendo las mismas acciones o generando los mismos pensamientos. Si se detecta un ciclo, forzar la terminacion o cambiar de estrategia.

```python
def detect_cycle(recent_actions: list[str], window: int = 6) -> bool:
    """Detecta si el agente esta repitiendo acciones.

    Busca ciclos de cualquier periodo: compara la primera mitad
    de las acciones recientes con la segunda mitad.
    """
    if len(recent_actions) < window:
        return False

    for period in range(1, len(recent_actions) // 2 + 1):
        segment = recent_actions[-(2 * period):]
        first_half = segment[:period]
        second_half = segment[period:]
        if first_half == second_half:
            return True

    return False
```

**3. Presupuesto de tokens o tiempo**

En produccion, el limite mas real suele ser economico. Cada llamada al LLM cuesta tokens, y los tokens cuestan dinero.

```python
import time

class TerminationPolicy:
    """Politica de terminacion para un agente."""

    def __init__(
        self,
        max_steps: int = 15,
        max_tokens: int = 100_000,
        max_time_seconds: int = 300,
        max_consecutive_errors: int = 3,
    ):
        self.max_steps = max_steps
        self.max_tokens = max_tokens
        self.max_time_seconds = max_time_seconds
        self.max_consecutive_errors = max_consecutive_errors

        self.steps = 0
        self.tokens_used = 0
        self.start_time = time.time()
        self.consecutive_errors = 0
        self.recent_actions: list[str] = []

    def record_step(self, action: str, tokens: int, success: bool):
        self.steps += 1
        self.tokens_used += tokens
        self.recent_actions.append(action)
        if success:
            self.consecutive_errors = 0
        else:
            self.consecutive_errors += 1

    def should_stop(self) -> tuple[bool, str]:
        if self.steps >= self.max_steps:
            return True, f"Limite de pasos: {self.steps}"
        if self.tokens_used >= self.max_tokens:
            return True, f"Presupuesto de tokens: {self.tokens_used}"
        elapsed = time.time() - self.start_time
        if elapsed >= self.max_time_seconds:
            return True, f"Tiempo maximo: {elapsed:.0f}s"
        if self.consecutive_errors >= self.max_consecutive_errors:
            return True, f"Errores consecutivos: {self.consecutive_errors}"
        if detect_cycle(self.recent_actions):
            return True, "Ciclo detectado"
        return False, "OK"
```

**4. Umbral de confianza**

El agente evalua su propia confianza en que ha completado la tarea. Si su confianza supera un umbral, se detiene.

```python
def should_stop_confidence(llm, history: str, task: str) -> bool:
    """El agente evalua si ya termino."""
    prompt = f"""
Tarea: {task}
Historial: {history}

En una escala de 0 a 1, que tan seguro estas de que la tarea
esta completa y la respuesta es correcta? Responde solo con un numero.
"""
    confidence = float(llm.generate(prompt))
    return confidence > 0.85
```

Esta heuristica es util pero tiene un costo: una llamada extra al LLM en cada paso. Y el LLM puede ser excesivamente optimista o pesimista sobre su propia confianza. Usala como complemento, no como unica defensa.

La mejor practica es combinar varias de estas heuristicas. Un agente bien disenado se detiene cuando **cualquiera** de estas condiciones se cumple: alcanzo el limite de pasos, supero el umbral de confianza, agoto su presupuesto de tokens, o detecto un ciclo.

---

## 2.6 Variantes del loop: reflexion, planificacion, ejecucion paralela

El loop ReAct basico fue solo el comienzo. Investigadores y practitioners han desarrollado variantes que abordan sus limitaciones. Cada variante modifica algun aspecto del ciclo fundamental para obtener mejores resultados en ciertos escenarios. Pero todas comparten la misma estructura subyacente: el while True con retroalimentacion.

### Reflexion: anadiendo auto-critica al loop

Reflexion, propuesto por Noah Shinn et al. [Shinn et al., 2023], parte de una observacion simple pero profunda: los humanos no solo pensamos y actuamos, tambien **reflexionamos sobre nuestros errores** y aprendemos de ellos.

El loop de Reflexion anade una capa adicional al ciclo ReAct:

1. **Ejecutar** el loop ReAct estandar para intentar resolver la tarea
2. **Evaluar** el resultado (fue correcto? fue exitoso?)
3. Si fallo: **Reflexionar** sobre que salio mal y generar feedback textual
4. **Reintentar** con el feedback de la reflexion incorporado al contexto

```python
def reflexion_loop(llm, tools, task, evaluator, max_reflections=3):
    """Loop con auto-reflexion: aprende de sus propios errores.

    Args:
        llm: modelo de lenguaje
        tools: herramientas disponibles
        task: la tarea a resolver
        evaluator: funcion que evalua si el resultado es correcto
        max_reflections: maximo numero de intentos con reflexion
    """
    reflections = []

    for attempt in range(max_reflections):
        # Construir contexto con reflexiones previas
        context = task
        if reflections:
            context += "\n\nReflexiones de intentos anteriores:\n"
            context += "\n".join(
                f"- Intento {i+1}: {r}" for i, r in enumerate(reflections)
            )

        # Ejecutar un intento
        result = react_loop(llm, tools, context)

        # Evaluar
        evaluation = evaluator(result, task)
        if evaluation.success:
            return result

        # Generar reflexion sobre el fallo
        reflection_prompt = f"""
Tarea: {task}
Tu intento: {result}
Evaluacion: {evaluation.feedback}

Reflexiona brevemente: que salio mal y que deberias hacer
diferente en el siguiente intento?"""

        reflection = llm.generate(reflection_prompt)
        reflections.append(reflection)

    return f"No se pudo completar despues de {max_reflections} intentos."
```

La conexion con Polya es directa: el cuarto paso de su metodo es **verificar el resultado**. Reflexion sistematiza esa verificacion y la convierte en aprendizaje dentro de la misma sesion.

Los resultados empiricos son alentadores. Reflexion mejoro el rendimiento en HumanEval (generacion de codigo) en un 11% absoluto sobre el baseline, y mostro mejoras del 8% sobre enfoques de solo-refinamiento sin reflexion explicita [Shinn et al., 2023]. La reflexion no es un simple "intentar de nuevo"; es un **meta-razonamiento** que identifica patrones de fallo y los convierte en guia para el siguiente intento.

### LATS: convertir el loop en busqueda en arbol

Language Agent Tree Search (LATS), propuesto por Andy Zhou et al. [Zhou et al., 2023], toma una idea diferente: por que comprometerse con un solo camino de razonamiento cuando puedes explorar varios?

LATS convierte el loop lineal de ReAct en una **busqueda en arbol**. En lugar de un solo camino Thought -> Action -> Observation, el agente genera multiples pensamientos posibles, evalua cual es mas prometedor, y explora las ramas mas prometedoras primero.

La analogia con las ciencias de la computacion es inmediata: esto esta inspirado en **Monte Carlo Tree Search (MCTS)**, la tecnica que uso AlphaGo para derrotar a Lee Sedol. La estructura del arbol es similar: cada nodo es un estado del agente y cada arista es una accion. Pero hay una diferencia clave: mientras MCTS clasico usa rollouts estocasticos para estimar el valor de un nodo, LATS usa el propio LLM como funcion de valor.

```python
class LATSNode:
    """Un nodo en el arbol de busqueda del agente."""
    def __init__(self, state: str, parent=None):
        self.state = state
        self.parent = parent
        self.children: list["LATSNode"] = []
        self.value: float = 0.0
        self.visits: int = 0

def lats_search(llm, tools, task, n_candidates=3, max_depth=10):
    """Busqueda en arbol para agentes: explora multiples caminos."""
    root = LATSNode(state=f"Tarea: {task}")

    for depth in range(max_depth):
        # SELECCION: elegir el nodo mas prometedor (UCB1)
        node = select_best_node(root)

        # EXPANSION: generar multiples acciones candidatas
        candidates = []
        for _ in range(n_candidates):
            thought_action = llm.generate(
                f"{node.state}\nGenera un pensamiento y accion:"
            )
            candidates.append(thought_action)

        # EVALUACION: puntuar cada candidato con el LLM
        for candidate in candidates:
            score = float(llm.generate(
                f"Evalua que tan prometedora es esta accion "
                f"para resolver la tarea (0-10): {candidate}"
            ))
            child = LATSNode(
                state=node.state + "\n" + candidate,
                parent=node
            )
            child.value = score
            node.children.append(child)

        # SIMULACION: ejecutar la mejor rama
        best_child = max(node.children, key=lambda c: c.value)
        action_name, action_args = extract_action(best_child.state)
        observation = tools[action_name].execute(action_args)
        best_child.state += f"\nObservation: {observation}"

        # BACKPROPAGATION: actualizar valores hacia arriba
        backpropagate(best_child, observation)

        if is_task_complete(observation, task):
            return extract_final_answer(best_child)

    return get_best_path_answer(root)
```

La ventaja de LATS es obvia en tareas donde el primer intento puede fallar. El costo tambien es obvio: mucho mas computo. LATS alcanzo 92.7% en HumanEval [Zhou et al., 2023], pero a un precio de 10-50x mas tokens que un ReAct basico. Un LATS con 10 niveles de profundidad y 3 candidatos puede costar $0.50-2.00 por query.

### Plan-and-Execute: separar planificacion de ejecucion

El patron **Plan-and-Execute** toma un enfoque diferente: en lugar de razonar paso a paso en cada iteracion, primero se genera un **plan completo** y luego se ejecuta.

```python
def plan_and_execute(llm, tools, task):
    """Primero planifica, luego ejecuta paso a paso."""
    # FASE 1: Planificacion
    plan_prompt = f"""
Tarea: {task}

Genera un plan paso a paso para resolver esta tarea.
Cada paso debe ser una accion concreta y ejecutable.
Formato:
1. [accion]
2. [accion]
..."""

    plan = llm.generate(plan_prompt)
    steps = parse_plan(plan)

    results = []

    # FASE 2: Ejecucion
    for i, step in enumerate(steps):
        execution_prompt = f"""
Plan original: {plan}
Pasos completados: {results}
Paso actual ({i+1}/{len(steps)}): {step}

Ejecuta este paso. Decide que herramienta usar.
"""
        thought_action = llm.generate(execution_prompt)
        action_name, action_args = extract_action(thought_action)
        observation = tools[action_name].execute(action_args)
        results.append({
            "step": step,
            "action": action_name,
            "result": observation
        })

    # FASE 3: Sintesis
    synthesis_prompt = f"""
Tarea original: {task}
Resultados de cada paso: {json.dumps(results, indent=2)}
Sintetiza una respuesta final."""

    return llm.generate(synthesis_prompt)
```

La ventaja principal es la coherencia: el agente tiene una vision global del problema antes de empezar a actuar. La desventaja es la rigidez: si el plan inicial es malo, todo el esfuerzo posterior puede ser desperdiciado. Las implementaciones sofisticadas incluyen un mecanismo de **replanificacion** cuando un paso falla o produce resultados inesperados.

### Tabla comparativa

| Variante | Costo relativo | Latencia relativa | Cuando usarla |
|---|---|---|---|
| ReAct basico | 1x | 1x | Mayoria de casos. Empieza aqui. |
| Reflexion | 2-3x | 2-3x | Tareas donde el retry es mas barato que fallar |
| Plan-and-Execute | 1.5-2x | 1.5x | Tareas complejas con estructura clara |
| LATS | 10-50x | 5-20x | Solo para tareas de muy alto valor |

La recomendacion practica es clara: **empieza con ReAct basico**. La mayoria de las veces es suficiente. Solo escala a variantes mas caras cuando tengas evidencia de que el agente basico no cumple tus metricas de rendimiento, y siempre mide el costo marginal contra la mejora obtenida.

---

## 2.7 Inference-time scaling: por que pensar mas tiempo produce mejores resultados

Hay un fenomeno que conecta directamente con el loop agentico y que esta transformando la arquitectura de los agentes modernos: el **inference-time scaling**.

### El cambio de paradigma

Durante anos, la forma de mejorar los LLMs era hacer modelos mas grandes: mas parametros, mas datos de entrenamiento, mas GPUs. Esto se conoce como **training-time scaling** y sigue la ley de escalamiento de Kaplan et al. [2020].

Pero a partir de 2024, un segundo eje de escalamiento emergio: en lugar de solo hacer el modelo mas grande, darle **mas tiempo para pensar** durante la inferencia. El modelo "razona" mas antes de responder, y los resultados mejoran dramaticamente.

La evidencia es solida. Snell et al. [2024] demostraron que la asignacion optima de computo en inferencia permite que un modelo pequeno supere a uno 14 veces mas grande. OpenAI o1 alcanzo 83.3% en AIME 2024, comparado con 13% de GPT-4o [OpenAI, 2024]. DeepSeek-R1, usando refuerzo puro sin trazas de razonamiento supervisadas, mejoro la precision en AIME de 15.6% a 71% a traves de cadenas de razonamiento extendidas, alcanzando 86.7% con votacion por mayoria [DeepSeek-AI, 2025].

### La conexion con los agentes

El inference-time scaling y el loop agentico son dos manifestaciones de la misma idea: **mas computo en inferencia produce mejores resultados**. La diferencia es donde se invierte ese computo:

- **Chain-of-thought interno**: El modelo genera tokens de razonamiento antes de responder. Cada token adicional agrega una "capa de computacion" que extiende la profundidad efectiva del transformador. Li et al. [2024] demostraron formalmente que con T pasos de CoT, incluso transformadores de profundidad constante pueden resolver problemas solubles por circuitos booleanos de tamano T, elevandolos de AC-cero a PTIME en el limite.

- **Loop agentico externo**: El agente genera multiples turnos de razonamiento-accion-observacion. Cada paso del loop es una invocacion completa del LLM con mas informacion en el contexto.

En ambos casos, el modelo invierte mas recursos computacionales para llegar a una mejor respuesta. La diferencia es que el chain-of-thought interno es automatico (el modelo decide cuantos tokens de razonamiento generar), mientras que el loop agentico es explicito (el programador define la estructura del loop y las herramientas disponibles).

### Implicaciones practicas

El inference-time scaling tiene tres implicaciones directas para los constructores de agentes:

**1. Modelos mas baratos pueden ser suficientes.** Si un modelo pequeno con un buen loop agentico puede superar a un modelo grande sin loop, la optimizacion no esta solo en elegir el modelo mas caro. Esta en disenar el loop correctamente.

**2. El costo se mueve de entrenamiento a inferencia.** Los analistas proyectan que la demanda de computo en inferencia excedera a la de entrenamiento por 118x para 2026, y que la inferencia consumira el 75% del computo total de IA para 2030. Esto significa que la eficiencia del loop agentico --cuantos pasos necesita, cuantos tokens consume por paso-- se convierte en una variable economica critica.

**3. No hay una estrategia unica que domine.** Un estudio a gran escala que proceso mas de 30 mil millones de tokens con ocho LLMs open-source encontro que ninguna estrategia de escalamiento en inferencia domina universalmente. La estrategia optima depende del modelo, la dificultad del problema y el presupuesto disponible. Esto refuerza la recomendacion de empezar simple (ReAct) y escalar solo cuando los datos lo justifiquen.

---

## 2.8 Control flow: de lo imperativo a los grafos de estado

Hasta ahora hemos tratado al agente como un proceso secuencial: piensa, actua, observa, repite. Pero cuando los agentes se vuelven mas complejos, necesitamos pensar de forma mas sofisticada sobre como fluye el control.

### Agentes imperativos

El approach mas simple es el **imperativo**: el agente es un script que ejecuta pasos en secuencia, con condicionales y loops explicitos. Es el modelo que hemos visto hasta ahora.

Funciona para agentes simples, pero se vuelve inmanejable cuando hay multiples caminos posibles segun el resultado de cada paso, necesitas paralelismo, o quieres que el agente pueda "retroceder" a un estado anterior.

### Agentes declarativos: grafos de estado

El approach alternativo es **declarativo**: en lugar de escribir el flujo paso a paso, defines los **estados posibles** del agente y las **transiciones** entre ellos. El agente es una **maquina de estados finitos**.

```python
from enum import Enum
from dataclasses import dataclass, field
from typing import Callable

class AgentState(Enum):
    REASONING = "reasoning"
    SEARCHING = "searching"
    CALCULATING = "calculating"
    SYNTHESIZING = "synthesizing"
    DONE = "done"
    ERROR = "error"

@dataclass
class StateGraph:
    """Un grafo de estados para un agente."""
    nodes: dict[AgentState, Callable] = field(default_factory=dict)
    edges: dict[AgentState, dict[str, AgentState]] = field(
        default_factory=dict
    )

    def add_node(self, name: AgentState, fn: Callable):
        self.nodes[name] = fn

    def add_edge(
        self, from_state: AgentState,
        condition: str, to_state: AgentState
    ):
        if from_state not in self.edges:
            self.edges[from_state] = {}
        self.edges[from_state][condition] = to_state

    def run(self, initial_state: AgentState, context: dict, max_steps=20):
        """Ejecuta el grafo desde el estado inicial."""
        current = initial_state

        for _ in range(max_steps):
            if current in (AgentState.DONE, AgentState.ERROR):
                return context

            node_fn = self.nodes[current]
            result = node_fn(context)
            context.update(result.get("state_updates", {}))
            condition = result.get("transition", "default")

            if current in self.edges and condition in self.edges[current]:
                current = self.edges[current][condition]
            else:
                current = AgentState.ERROR
                context["error"] = f"Sin transicion para '{condition}'"

        context["error"] = "Limite de pasos del grafo alcanzado"
        return context
```

Este enfoque de grafos de estado es el que frameworks como **LangGraph** han adoptado, y es el que ha demostrado ser mas robusto para agentes en produccion. La ventaja es que las transiciones son explicitas y auditables: puedes ver exactamente que estados son posibles y que condiciones llevan a cada uno.

La desventaja es la complejidad adicional en la definicion del grafo. Para agentes simples con 3-5 pasos, el approach imperativo es mas claro. Para agentes complejos con multiples caminos, manejo de errores sofisticado y necesidad de retroceso, los grafos de estado son la mejor opcion.

---

## Takeaway del capitulo

Detras de toda la magia de los agentes no hay mas que un `while True` bien pensado. El loop agentico --percibir, razonar, actuar, observar, repetir-- es la misma estructura que ha aparecido independientemente en la doctrina militar (OODA), la ingenieria de control (PID), la cibernetica (Wiener) y la heuristica matematica (Polya).

ReAct formalizo este loop para los agentes LLM y sigue siendo el framework dominante. Sus variantes --Reflexion, LATS, Plan-and-Execute-- son extensiones que intercambian mas computo por mejores resultados, pero todas comparten la misma estructura subyacente.

El problema mas dificil no es hacer que el loop funcione; es hacer que se detenga. Implementa siempre `max_steps`, presupuestos de tokens, deteccion de ciclos y limites de tiempo. Un agente sin politica de terminacion es un `while True` sin `break`.

Y recuerda: empieza con ReAct basico. La mayoria de las veces es suficiente. Solo escala a variantes mas caras cuando tengas evidencia empirica de que el rendimiento justifica el costo adicional.

En el proximo capitulo veremos que el historial que crece con cada paso del loop tiene un costo que va mas alla de los tokens: la ventana de contexto es un recurso finito, caro y sorprendentemente fragil.

---

### Notas y referencias

- [Yao et al., 2022] Shunyu Yao, Jeffrey Zhao, Dian Yu et al. "ReAct: Synergizing Reasoning and Acting in Language Models." ICLR 2023. arXiv:2210.03629.
- [Wei et al., 2022] Jason Wei, Xuezhi Wang, Dale Schuurmans et al. "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." NeurIPS 2022. arXiv:2201.11903.
- [Shinn et al., 2023] Noah Shinn, Federico Cassano, Ashwin Gopinath et al. "Reflexion: Language Agents with Verbal Reinforcement Learning." NeurIPS 2023. arXiv:2303.11366.
- [Zhou et al., 2023] Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman et al. "Language Agent Tree Search Unifies Reasoning, Acting, and Planning." ICML 2024. arXiv:2310.04406.
- [Yao et al., 2023] Shunyu Yao, Dian Yu, Jeffrey Zhao et al. "Tree of Thoughts: Deliberate Problem Solving with Large Language Models." NeurIPS 2023. arXiv:2305.10601.
- [Snell et al., 2024] Charlie Snell, Jaehoon Lee, Kelvin Xu, Aviral Kumar. "Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters." arXiv:2408.03314.
- [OpenAI, 2024] "Learning to Reason with LLMs." OpenAI Blog.
- [DeepSeek-AI, 2025] Daya Guo et al. "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning." arXiv:2501.12948.
- [Li et al., 2024] Zhiyuan Li, Hong Liu, Denny Zhou, Tengyu Ma. "Chain of Thought Empowers Transformers to Solve Inherently Serial Problems." ICLR 2024. arXiv:2402.12875.
- [Kaplan et al., 2020] Jared Kaplan et al. "Scaling Laws for Neural Language Models." arXiv:2001.08361.
- [Shankar et al., 2025] "Measuring Agents in Production." 306 practicantes encuestados.
- [Wiener, 1948] Norbert Wiener. *Cybernetics: Or Control and Communication in the Animal and the Machine*. MIT Press.
- [Polya, 1945] George Polya. *How to Solve It*. Princeton University Press.
- [Turing, 1936] Alan Turing. "On Computable Numbers, with an Application to the Entscheidungsproblem." Proceedings of the London Mathematical Society.
