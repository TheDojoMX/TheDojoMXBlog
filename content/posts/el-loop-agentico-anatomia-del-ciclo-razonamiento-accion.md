---
title: "El loop agéntico: anatomía del ciclo razonamiento-acción"
date: 2026-03-18
author: "Héctor Patricio"
tags: ['agentes', 'inteligencia-artificial', 'llm', 'react', 'loops', 'arquitectura', 'ciencias-de-la-computación']
description: "Todo agente de IA se reduce a un loop: percibir, razonar, actuar, observar. Exploramos la anatomía de este ciclo fundamental, sus variantes y sus límites teóricos."
featuredImage: ""
draft: true
---

Todo agente de IA, desde un chatbot que busca en Google hasta un sistema autónomo que escribe y despliega código, se reduce a lo mismo: un loop. Percibir el estado del mundo, razonar sobre qué hacer, ejecutar una acción y observar el resultado. Repetir hasta terminar (o hasta que algo salga mal).

Este ciclo es tan fundamental para los agentes de IA como el ciclo **fetch-decode-execute** lo es para un procesador. Así como una CPU repite incansablemente el proceso de buscar la siguiente instrucción, decodificarla y ejecutarla, un agente repite el proceso de observar, pensar y actuar. Y así como entender el ciclo de un procesador es clave para entender la computación, entender el loop agéntico es clave para entender (y construir) agentes que funcionen.

En este artículo vamos a desarmar este loop pieza por pieza. Exploraremos sus orígenes en la teoría de control y la cibernética, analizaremos el framework ReAct que lo popularizó en el mundo de los LLMs, veremos las variantes más importantes, y confrontaremos el problema más difícil de todos: decidir cuándo parar. Al final, implementaremos un agente desde cero en Python, sin frameworks, para que veas que detrás de toda la magia no hay más que un `while True` bien pensado.

## Los orígenes: el ciclo OODA y el loop de control

El loop agéntico no nació con los LLMs. Sus raíces se extienden décadas atrás, hasta la teoría de control, la cibernética y la doctrina militar. Antes de hablar de `Thought -> Action -> Observation`, necesitamos hablar de tres ideas fundamentales que lo preceden.

### El ciclo OODA de John Boyd

En los años 60, el coronel John Boyd de la Fuerza Aérea de Estados Unidos desarrolló un modelo para entender cómo los pilotos de combate toman decisiones bajo presión extrema. Lo llamó el **ciclo OODA**: **Observe, Orient, Decide, Act** (Observar, Orientar, Decidir, Actuar). (Vale notar que Boyd nunca publicó sus ideas en papers revisados por pares; las presentó en briefings y documentos internos que circularon informalmente.)

La idea central de Boyd era simple pero poderosa: el combatiente que recorre este ciclo más rápido que su oponente gana. No importa si tu avión es más rápido o tu armamento es superior. Si el otro piloto observa la situación, se orienta, decide y actúa antes que tú, estás perdido.

Lo interesante del modelo de Boyd es la fase de **orientación**. No es simplemente "mirar los datos". Es filtrar la información a través de tu experiencia previa, tu cultura, tu entrenamiento, tus modelos mentales. Es la fase donde conviertes datos crudos en comprensión. Hay una analogía útil (aunque imperfecta) con lo que hace un LLM cuando recibe un prompt con contexto: filtra la información a través de representaciones aprendidas durante el entrenamiento para generar una respuesta. La analogía tiene límites claros: OODA es un modelo mental informal para la toma de decisiones humana, no un framework algorítmico validado empíricamente. Su valor aquí es como intuición, no como especificación técnica.

### El loop de control PID

En ingeniería de control, el controlador PID (Proporcional-Integral-Derivativo) es quizás el mecanismo de feedback más exitoso de la historia. Tu aire acondicionado, el control de crucero de tu carro, un drone manteniéndose estable en el aire: todos usan alguna variante de este loop.

El principio es elegante:

1. **Mides** el estado actual del sistema (la temperatura de la habitación)
2. **Calculas** el error: la diferencia entre el estado actual y el estado deseado (faltan 3 grados para llegar a 22°C)
3. **Aplicas** una corrección proporcional al error (inyecta más frío)
4. **Repites**

Lo crucial aquí es el concepto de **retroalimentación negativa**: cada acción reduce la brecha entre donde estás y donde quieres estar. El sistema converge porque cada iteración del loop lo acerca al objetivo. Esta es exactamente la misma intuición detrás de un agente que observa el resultado de su última acción y decide si necesita hacer más o si ya terminó.

### La cibernética de Norbert Wiener

Norbert Wiener, en su libro *Cybernetics* (1948), formalizó la idea de que los sistemas inteligentes, sean biológicos o mecánicos, funcionan a través de **ciclos de retroalimentación**. Wiener argumentaba que la diferencia entre un sistema "inteligente" y uno mecánico no está en sus componentes, sino en su capacidad para usar la información sobre sus propias acciones para ajustar su comportamiento futuro.

Esta idea fue revolucionaria. Antes de Wiener, la ingeniería pensaba en sistemas abiertos: entrada, proceso, salida. Wiener cerró el loop y dijo: la salida afecta la siguiente entrada. Y ese cierre del loop es lo que produce comportamiento aparentemente inteligente.

### La conexión con Polya

Hay una conexión que no quiero dejar pasar. En artículos anteriores hemos hablado extensamente del método de George Polya para resolver problemas, descrito en ["El arte de resolver problemas: la heurística"](/2019/10/03/el-arte-de-resolver-problemas-la-heuristica.html) y en ["Técnicas para resolver problemas"](/2019/09/27/tecnicas-para-resolver-problemas.html). Polya propuso cuatro fases para resolver cualquier problema:

1. **Entender** el problema
2. **Concebir un plan**
3. **Ejecutar** el plan
4. **Verificar** el resultado

¿Te suena? Observar, orientar/planear, actuar, verificar. Es el mismo loop. La resolución de problemas, ya sea por un matemático, un piloto de combate, un termostato o un agente de IA, sigue la misma estructura fundamental: un ciclo de percepción, razonamiento, acción y retroalimentación.

La retroalimentación es la estructura fundamental del comportamiento dirigido a un objetivo, como argumentamos en ["Inducción y deducción para desarrolladores de software"](/2019/12/14/induccion-y-deduccion-segun-polya.html). Sin el paso de verificación, sin cerrar el loop, simplemente estás ejecutando instrucciones a ciegas.

## ReAct: el loop canónico de los agentes LLM

En octubre de 2022, Shunyu Yao y sus colegas de Princeton publicaron el paper "ReAct: Synergizing Reasoning and Acting in Language Models". Este paper estableció el framework conceptual que domina la arquitectura de agentes de IA hasta hoy.

### La intuición detrás de ReAct

Antes de ReAct, había dos líneas de investigación separadas. Por un lado, el **chain-of-thought prompting** (como discutimos en ["Cómo razonan los LLMs"](/2026/02/15/como-razonan-los-llms-de-turing-a-inference-time-scaling.html)) mostraba que hacer que los LLMs "piensen en voz alta" mejoraba dramáticamente su rendimiento en tareas de razonamiento. Por otro lado, la investigación en **agentes autónomos** exploraba cómo los LLMs podían usar herramientas y APIs para interactuar con el mundo.

La contribución de ReAct fue unir ambas ideas en un solo loop:

1. **Thought** (Pensamiento): El agente razona explícitamente sobre la situación actual, qué información necesita y cuál debería ser su siguiente paso.
2. **Action** (Acción): El agente ejecuta una acción concreta: buscar en una API, consultar una base de datos, ejecutar código, llamar a una herramienta.
3. **Observation** (Observación): El agente recibe el resultado de su acción y lo incorpora a su contexto.

Y luego el loop se repite: el agente genera un nuevo pensamiento basado en la observación, decide la siguiente acción, observa el resultado, y así sucesivamente hasta que decide que tiene una respuesta final.

### Por qué funciona: la separación de concerns

La genialidad de ReAct está en algo que los programadores conocemos bien: la **separación de responsabilidades**. Al separar explícitamente el razonamiento (Thought) de la ejecución (Action), el sistema obtiene varias ventajas:

**Trazabilidad**: Puedes ver exactamente por qué el agente tomó cada decisión. No es una caja negra que misteriosamente produce un resultado. Cada paso tiene un pensamiento asociado que explica la lógica.

**Recuperación de errores**: Si una acción falla o devuelve información inesperada, el paso de Thought permite al agente re-evaluar su estrategia en lugar de continuar ciegamente. Esto es análogo al principio de Polya de verificar el resultado antes de continuar.

**Grounding**: Al anclar el razonamiento en observaciones reales del mundo (resultados de APIs, contenido de archivos, respuestas de bases de datos), el agente reduce las alucinaciones. No está inventando hechos; está razonando sobre datos reales.

Como exploramos en ["Patrones de diseño para sistemas con IA"](/2026/02/15/patrones-de-diseno-para-sistemas-con-ia.html), la separación entre la "inteligencia" (el LLM razonando) y la "lógica" (las herramientas ejecutando acciones concretas) es un principio fundamental para construir sistemas robustos. ReAct es la encarnación más pura de este principio.

### Implementación básica del loop ReAct

Veamos cómo se ve el loop ReAct en su forma más básica. No necesitas LangChain ni ningún framework para entender la mecánica:

```python
def react_loop(llm, tools, question, max_steps=10):
    """El loop ReAct en su forma más pura."""
    # El historial acumula thoughts, actions y observations
    history = f"Pregunta: {question}\n"

    for step in range(max_steps):
        # THOUGHT: el LLM razona sobre qué hacer
        prompt = f"""{history}
Genera tu siguiente pensamiento y acción.
Formato:
Thought: [tu razonamiento]
Action: [nombre_herramienta(argumentos)]
Si ya tienes la respuesta final:
Thought: [razonamiento final]
Answer: [respuesta]"""

        response = llm.generate(prompt)

        # Si el LLM decidió que ya tiene la respuesta
        if "Answer:" in response:
            return extract_answer(response)

        # ACTION: extraer y ejecutar la acción
        thought = extract_thought(response)
        action_name, action_args = extract_action(response)
        history += f"\nThought: {thought}\n"
        history += f"Action: {action_name}({action_args})\n"

        # OBSERVATION: ejecutar la herramienta y obtener resultado
        observation = tools[action_name].execute(action_args)
        history += f"Observation: {observation}\n"

    return "Error: se alcanzó el límite de pasos sin respuesta"
```

Observa la estructura: es literalmente un `for` loop con tres pasos internos. Todo el "magic" de los agentes de IA se reduce a esto. El LLM genera texto que se parsea para extraer acciones, las acciones se ejecutan, y los resultados se agregan al contexto para la siguiente iteración.

## Variantes del loop

El loop ReAct básico fue solo el comienzo. Investigadores y practitioners han desarrollado variantes que abordan sus limitaciones. Cada variante modifica algún aspecto del ciclo fundamental para obtener mejores resultados en ciertos escenarios.

### Reflexion: añadiendo auto-crítica al loop

Reflexion, propuesto por Noah Shinn et al. en 2023, parte de una observación simple pero profunda: los humanos no solo pensamos y actuamos, también **reflexionamos sobre nuestros errores** y aprendemos de ellos.

El loop de Reflexion añade una capa adicional al ciclo ReAct:

1. **Ejecutar** el loop ReAct estándar para intentar resolver la tarea
2. **Evaluar** el resultado (¿fue correcto? ¿fue exitoso?)
3. Si falló: **Reflexionar** sobre qué salió mal y generar feedback textual
4. **Reintentar** con el feedback de la reflexión incorporado al contexto

```python
def reflexion_loop(llm, tools, task, max_reflections=3):
    """Loop con auto-reflexión: aprende de sus propios errores."""
    reflections = []

    for attempt in range(max_reflections):
        # Ejecutar un intento con las reflexiones previas como contexto
        context = build_context(task, reflections)
        result = react_loop(llm, tools, context)

        # Evaluar el resultado
        evaluation = evaluate_result(result, task)

        if evaluation.success:
            return result

        # Generar reflexión sobre el fallo
        reflection_prompt = f"""
Tarea: {task}
Intento #{attempt + 1}: {result}
Evaluación: {evaluation.feedback}

Reflexiona: ¿Qué salió mal? ¿Qué deberías hacer diferente
en el siguiente intento?"""

        reflection = llm.generate(reflection_prompt)
        reflections.append(reflection)

    return "No se pudo completar la tarea después de reflexionar"
```

La conexión con Polya es directa: el cuarto paso de su método es **verificar el resultado**. Reflexion sistematiza esta verificación y la convierte en aprendizaje dentro de la misma sesión.

### LATS: convertir el loop en búsqueda en árbol

Language Agent Tree Search (LATS), propuesto por Andy Zhou et al. en 2023, toma una idea diferente: ¿por qué comprometerse con un solo camino de razonamiento cuando puedes explorar varios?

LATS convierte el loop lineal de ReAct en una **búsqueda en árbol**. En lugar de un solo camino Thought -> Action -> Observation, el agente genera múltiples pensamientos posibles, evalúa cuál es más prometedor, y explora las ramas más prometedoras primero.

La analogía con las ciencias de la computación es inmediata: esto está inspirado en **Monte Carlo Tree Search (MCTS)**, la técnica que usó AlphaGo para derrotar a Lee Sedol. La estructura del árbol es similar: cada nodo es un estado del agente y cada arista es una acción. Pero hay una diferencia clave: mientras MCTS clásico usa rollouts estocásticos para estimar el valor de un nodo, LATS usa el propio LLM como función de valor. El agente usa una combinación de exploración y explotación para navegar el espacio de posibilidades.

```python
class LATSNode:
    """Un nodo en el árbol de búsqueda del agente."""
    def __init__(self, state, parent=None):
        self.state = state        # El historial hasta este punto
        self.parent = parent
        self.children = []
        self.value = 0.0          # Qué tan prometedor es este nodo
        self.visits = 0

def lats_search(llm, tools, task, n_candidates=3, max_depth=10):
    """Búsqueda en árbol para agentes: explora múltiples caminos."""
    root = LATSNode(state=f"Tarea: {task}")

    for iteration in range(max_depth):
        # SELECCIÓN: elegir el nodo más prometedor para expandir
        node = select_best_node(root)  # UCB1 o similar

        # EXPANSIÓN: generar múltiples acciones candidatas
        candidates = []
        for _ in range(n_candidates):
            thought_action = llm.generate(
                f"{node.state}\nGenera un pensamiento y acción:"
            )
            candidates.append(thought_action)

        # EVALUACIÓN: puntuar cada candidato
        for candidate in candidates:
            score = llm.generate(
                f"Evalúa qué tan prometedora es esta acción "
                f"para resolver la tarea (0-10): {candidate}"
            )
            child = LATSNode(
                state=node.state + "\n" + candidate,
                parent=node
            )
            child.value = float(score)
            node.children.append(child)

        # SIMULACIÓN: ejecutar la acción del mejor candidato
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

La ventaja de LATS es obvia en tareas donde el primer intento puede fallar: en lugar de un solo camino que puede llevar a un callejón sin salida, el agente tiene múltiples opciones. El costo también es obvio: mucho más cómputo (y por tanto más tokens, más latencia, más dinero). En producción, LATS multiplica el consumo de tokens por 10-50x respecto a un ReAct básico: generar 3 candidatos por nodo, evaluar cada uno con el LLM y explorar múltiples ramas se acumula rápidamente. Un LATS con 10 niveles de profundidad y 3 candidatos puede costar $0.50-2.00 por query. Para la mayoría de los casos de uso, ReAct básico o Reflexion ofrecen una mejor relación costo-beneficio. Reserva LATS para tareas de alto valor donde el costo de fallar supera significativamente el costo del cómputo adicional.

| Variante | Costo relativo | Latencia relativa | Cuándo usarla |
|---|---|---|---|
| ReAct básico | 1x | 1x | Mayoría de casos |
| Reflexion | 2-3x | 2-3x | Tareas donde el retry es más barato que fallar |
| LATS | 10-50x | 5-20x | Solo para tareas de muy alto valor |
| Plan-and-Execute | 1.5-2x | 1.5x | Tareas complejas con estructura clara |

### Plan-and-Execute: separar planificación de ejecución

El patrón **Plan-and-Execute** toma un enfoque diferente: en lugar de razonar paso a paso en cada iteración, primero se genera un **plan completo** y luego se ejecuta.

La idea es intuitiva. Cuando te enfrentas a un problema complejo, no empiezas a hacer cosas al azar. Primero piensas en la estrategia general, descompones el problema en subproblemas, y luego atacas cada subproblema. Esto es exactamente lo que Polya recomienda en su segundo paso: **concebir un plan**.

```python
def plan_and_execute(llm, tools, task):
    """Primero planifica, luego ejecuta paso a paso."""
    # FASE 1: Planificación
    plan_prompt = f"""
Tarea: {task}

Genera un plan paso a paso para resolver esta tarea.
Cada paso debe ser una acción concreta y ejecutable.
Formato:
1. [acción]
2. [acción]
...
"""
    plan = llm.generate(plan_prompt)
    steps = parse_plan(plan)

    results = []

    # FASE 2: Ejecución
    for i, step in enumerate(steps):
        execution_prompt = f"""
Plan original: {plan}
Pasos completados: {results}
Paso actual ({i+1}/{len(steps)}): {step}

Ejecuta este paso. Decide qué herramienta usar.
"""
        thought_action = llm.generate(execution_prompt)
        action_name, action_args = extract_action(thought_action)
        observation = tools[action_name].execute(action_args)
        results.append({
            "step": step,
            "action": action_name,
            "result": observation
        })

    # FASE 3: Síntesis
    synthesis_prompt = f"""
Tarea original: {task}
Resultados de cada paso: {results}
Sintetiza una respuesta final.
"""
    return llm.generate(synthesis_prompt)
```

La ventaja principal es la coherencia: el agente tiene una visión global del problema antes de empezar a actuar. La desventaja es la rigidez: si el plan inicial es malo, todo el esfuerzo posterior puede ser desperdiciado. Por eso, las implementaciones más sofisticadas incluyen un mecanismo de **replanificación** cuando un paso falla o produce resultados inesperados.

## El problema de la terminación

Aquí llegamos al problema más profundo y más difícil del loop agéntico. Un loop que se ejecuta es útil. Un loop que no se detiene es un desastre. ¿Cuándo debe parar un agente?

### El halting problem y los agentes

En 1936, Alan Turing demostró uno de los resultados más fundamentales de las ciencias de la computación: es **imposible** construir un algoritmo general que determine si cualquier máquina de Turing va a terminar o ejecutarse para siempre. Este es el famoso **problema de la parada** (halting problem), y como exploramos en ["Cómo razonan los LLMs: de las máquinas de Turing al inference-time scaling"](/2026/02/15/como-razonan-los-llms-de-turing-a-inference-time-scaling.html), tiene implicaciones profundas para cualquier sistema computacional. (La equivalencia entre máquinas de Turing y programas reales descansa en la tesis de Church-Turing, que es una tesis ampliamente aceptada, no un teorema demostrado.)

Ahora bien, un agente de IA es un programa. Un agente ejecutando un loop ReAct es, en esencia, una máquina que decide en cada paso si continuar o detenerse basándose en su propio estado. El resultado de Turing nos dice que **no existe un método general** para determinar si un agente arbitrario va a terminar. En la práctica, para un agente concreto con un límite de iteraciones, la terminación es trivialmente garantizable. Pero un agente sin esos límites, que decide dinámicamente si continuar, hereda la indecidibilidad del problema general.

En la práctica, esto se manifiesta de formas concretas y dolorosas:

- **Loops infinitos de herramientas**: El agente busca información, no la encuentra, la busca de otra manera, no la encuentra, y repite ad infinitum.
- **Ciclos de auto-corrección**: El agente detecta un error, intenta corregirlo, introduce un nuevo error, intenta corregir ese, y así sucesivamente.
- **Indecisión**: El agente no puede determinar si tiene suficiente información para responder y sigue buscando más datos indefinidamente.
- **Perfeccionismo**: El agente sigue refinando una respuesta que ya es suficientemente buena, consumiendo recursos sin mejorar significativamente la calidad.

### Heurísticas de terminación

Como no podemos resolver el problema de la parada en general, hacemos lo que siempre hacemos en ciencias de la computación cuando nos topamos con un problema intratable: usamos **heurísticas**. Esto conecta directamente con lo que discutimos en ["El arte de resolver problemas: la heurística"](/2019/10/03/el-arte-de-resolver-problemas-la-heuristica.html): cuando no hay un algoritmo perfecto, usamos estrategias que funcionan razonablemente bien en la práctica.

Veamos las heurísticas de terminación más comunes:

**1. Límite máximo de pasos (`max_steps`)**

La más simple y la más importante. Estableces un número máximo de iteraciones y el agente se detiene cuando lo alcanza, sin importar qué. Es brutal pero efectivo: garantiza que el agente siempre termina.

```python
MAX_STEPS = 15  # Nunca más de 15 iteraciones

for step in range(MAX_STEPS):
    result = agent_step()
    if result.is_final:
        return result

return "Límite de pasos alcanzado sin respuesta definitiva"
```

**2. Umbral de confianza**

El agente evalúa su propia confianza en que ha completado la tarea. Si su confianza supera un umbral, se detiene.

```python
def should_stop(llm, history, task):
    """¿El agente cree que ya terminó?"""
    prompt = f"""
Tarea: {task}
Historial: {history}

En una escala de 0 a 1, ¿qué tan seguro estás de que la tarea
está completa y la respuesta es correcta? Responde solo con un número.
"""
    confidence = float(llm.generate(prompt))
    return confidence > 0.85
```

**3. Detección de ciclos**

Monitorear si el agente está repitiendo las mismas acciones o generando los mismos pensamientos. Si se detecta un ciclo, forzar la terminación o cambiar de estrategia.

```python
def detect_cycle(history, window=6):
    """Detecta si el agente está repitiendo acciones.

    Busca ciclos de cualquier periodo: compara la primera mitad
    de las acciones recientes con la segunda mitad. Esto detecta
    periodos 1, 2, 3, etc. siempre que la ventana sea >= 2*periodo.
    """
    recent_actions = extract_actions(history)[-window:]
    if len(recent_actions) < 4:
        return False

    # Verificar ciclos de diferentes periodos (1, 2, 3, ...)
    for period in range(1, len(recent_actions) // 2 + 1):
        # Tomar las últimas 2*period acciones
        segment = recent_actions[-(2 * period):]
        first_half = segment[:period]
        second_half = segment[period:]
        if first_half == second_half:
            return True

    return False
```

**4. Presupuesto de tokens o tiempo**

En producción, el límite más real suele ser económico. Cada llamada al LLM cuesta tokens, y los tokens cuestan dinero. Un agente que consume 100,000 tokens buscando una respuesta trivial es un agente mal diseñado.

```python
class TokenBudget:
    """Controla el gasto de tokens del agente."""
    def __init__(self, max_tokens=50_000):
        self.max_tokens = max_tokens
        self.used_tokens = 0

    def can_continue(self):
        return self.used_tokens < self.max_tokens

    def record_usage(self, tokens):
        self.used_tokens += tokens
        if self.used_tokens > self.max_tokens * 0.9:
            print(f"ADVERTENCIA: {self.used_tokens}/{self.max_tokens} "
                  f"tokens usados (90%+)")
```

La mejor práctica es combinar varias de estas heurísticas. Un agente bien diseñado se detiene cuando cualquiera de estas condiciones se cumple: alcanzó el límite de pasos, superó el umbral de confianza, agotó su presupuesto de tokens, o detectó un ciclo.

## Control flow vs data flow en agentes

Hasta ahora hemos hablado del loop agéntico como un proceso secuencial: piensa, actúa, observa, repite. Pero cuando los agentes se vuelven más complejos, necesitamos pensar de forma más sofisticada sobre cómo fluye el control y los datos.

### Agentes imperativos: paso a paso

El approach más simple es el **imperativo**: el agente es un script que ejecuta pasos en secuencia, con condicionales y loops explícitos. Es el modelo que hemos visto hasta ahora.

```python
def agente_imperativo(task):
    plan = create_plan(task)
    for step in plan:
        if step.type == "search":
            result = search_tool(step.query)
        elif step.type == "calculate":
            result = calculator(step.expression)
        elif step.type == "write":
            result = write_file(step.content)
        # ...más condicionales para cada tipo de acción
    return synthesize_results()
```

Esto funciona para agentes simples, pero se vuelve inmanejable cuando:

- Hay múltiples caminos posibles según el resultado de cada paso
- Necesitas paralelismo (ejecutar varias acciones simultáneamente)
- Quieres que el agente pueda "retroceder" a un estado anterior
- El flujo tiene ciclos complejos (no solo un loop principal)

### Agentes declarativos: grafos de estado

El approach alternativo es **declarativo**: en lugar de escribir el flujo paso a paso, defines los **estados posibles** del agente y las **transiciones** entre ellos. El agente es una **máquina de estados finitos**.

Este es el enfoque que frameworks como **LangGraph** han adoptado, y como discutimos en ["De agentes teóricos a agentes en producción"](/2026/02/15/de-agentes-teoricos-a-agentes-en-produccion.html), es el que ha demostrado ser más robusto para agentes en producción.

La idea es representar al agente como un **grafo dirigido**:

- **Nodos**: representan estados o acciones del agente (razonar, buscar, calcular, responder)
- **Aristas**: representan transiciones condicionales (si el resultado de la búsqueda fue insuficiente, volver a buscar; si fue suficiente, pasar a sintetizar)
- **Estado global**: un diccionario con toda la información acumulada que los nodos pueden leer y modificar

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
    state: dict = field(default_factory=dict)

    def add_node(self, name: AgentState, fn: Callable):
        self.nodes[name] = fn

    def add_edge(self, from_state: AgentState,
                 condition: str, to_state: AgentState):
        if from_state not in self.edges:
            self.edges[from_state] = {}
        self.edges[from_state][condition] = to_state

    def run(self, initial_state: AgentState, context: dict):
        """Ejecuta el grafo desde el estado inicial."""
        self.state = context
        current = initial_state

        while current not in (AgentState.DONE, AgentState.ERROR):
            # Ejecutar el nodo actual
            node_fn = self.nodes[current]
            result = node_fn(self.state)

            # Determinar la transición
            self.state.update(result.get("state_updates", {}))
            condition = result.get("transition", "default")

            if current in self.edges and condition in self.edges[current]:
                current = self.edges[current][condition]
            else:
                current = AgentState.ERROR

        return self.state
```

La ventaja del grafo de estados es que puedes **visualizar** el comportamiento del agente, **verificar** que no hay estados inalcanzables o transiciones faltantes, e implementar **checkpointing** de forma natural (simplemente guarda el estado y el nodo actual para poder resumir después).

Un detalle importante: aunque un grafo de estados finito tiene poder computacional limitado, un grafo con un **diccionario de estado** que puede crecer arbitrariamente no pierde poder expresivo. El grafo define las transiciones y el diccionario funciona como memoria. No estamos perdiendo capacidad al usar grafos de estado; simplemente estamos organizando el agente de una forma más manejable. Y el twist clave es que la transición en cada nodo no está hardcodeada: la genera dinámicamente el LLM basándose en el contexto actual.

## Ejemplo práctico: un loop agéntico desde cero

Vamos a implementar un agente completo en Python, sin frameworks, que pueda responder preguntas usando herramientas. Este ejemplo integra todos los conceptos que hemos discutido: el loop ReAct, heurísticas de terminación, detección de ciclos y un diseño basado en grafos de estado simplificado.

```python
"""
Un agente ReAct completo, implementado desde cero.
Sin LangChain. Sin LangGraph. Sin magia.
"""
import json
import re
from dataclasses import dataclass, field
from typing import Any

# --- Herramientas ---

def calculator(expression: str) -> str:
    """Evalúa una expresión matemática de forma segura."""
    import ast
    import operator

    # Operadores permitidos
    ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def _eval_node(node):
        """Evalúa un nodo AST aritmético de forma segura."""
        if isinstance(node, ast.Expression):
            return _eval_node(node.body)
        elif isinstance(node, ast.Constant) and isinstance(
            node.value, (int, float)
        ):
            return node.value
        elif isinstance(node, ast.BinOp) and type(node.op) in ops:
            left = _eval_node(node.left)
            right = _eval_node(node.right)
            return ops[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp) and type(node.op) in ops:
            return ops[type(node.op)](_eval_node(node.operand))
        else:
            raise ValueError(
                f"Operación no permitida: {ast.dump(node)}"
            )

    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval_node(tree)
        return f"Resultado: {result}"
    except (ValueError, SyntaxError) as e:
        return f"Error al calcular: {e}"


def search_knowledge(query: str) -> str:
    """Simula una búsqueda en una base de conocimiento."""
    knowledge = {
        "python": "Python es un lenguaje de programación interpretado, "
                  "creado por Guido van Rossum en 1991.",
        "turing": "Alan Turing (1912-1954) fue un matemático británico, "
                  "considerado el padre de la computación moderna.",
        "loop": "Un loop (bucle) es una estructura de control que repite "
                "un bloque de código mientras se cumpla una condición.",
        "agente": "Un agente de IA es un sistema que percibe su entorno "
                  "y toma acciones para lograr objetivos.",
    }
    query_lower = query.lower()
    results = []
    for key, value in knowledge.items():
        if key in query_lower:
            results.append(value)
    if results:
        return " | ".join(results)
    return f"No se encontró información sobre: {query}"


# Registro de herramientas disponibles
TOOLS = {
    "calculator": {
        "fn": calculator,
        "description": "Evalúa expresiones matemáticas. "
                       "Uso: calculator(expresión)"
    },
    "search": {
        "fn": search_knowledge,
        "description": "Busca información en la base de conocimiento. "
                       "Uso: search(consulta)"
    },
}


# --- El Agente ---

@dataclass
class AgentStep:
    """Representa un paso del agente."""
    thought: str
    action: str | None = None
    action_input: str | None = None
    observation: str | None = None
    is_final: bool = False
    answer: str | None = None


@dataclass
class AgentConfig:
    """Configuración del agente con heurísticas de terminación."""
    max_steps: int = 10
    max_tokens_budget: int = 50_000
    cycle_detection_window: int = 3


class ReActAgent:
    """Agente ReAct completo con heurísticas de terminación."""

    def __init__(self, llm, tools: dict, config: AgentConfig = None):
        self.llm = llm
        self.tools = tools
        self.config = config or AgentConfig()
        self.history: list[AgentStep] = []
        self.tokens_used = 0

    def _build_system_prompt(self) -> str:
        tool_descriptions = "\n".join(
            f"- {name}: {info['description']}"
            for name, info in self.tools.items()
        )
        return f"""Eres un agente que resuelve tareas paso a paso.

Herramientas disponibles:
{tool_descriptions}

En cada paso, genera EXACTAMENTE uno de estos formatos:

OPCIÓN A - Si necesitas usar una herramienta:
Thought: [tu razonamiento sobre qué hacer]
Action: [nombre_herramienta]
Action Input: [argumento para la herramienta]

OPCIÓN B - Si ya tienes la respuesta final:
Thought: [tu razonamiento final]
Final Answer: [tu respuesta]

IMPORTANTE: Usa la información de observaciones anteriores.
No repitas acciones que ya ejecutaste."""

    def _build_step_prompt(self, question: str) -> str:
        prompt = self._build_system_prompt()
        prompt += f"\n\nPregunta del usuario: {question}\n"

        for step in self.history:
            prompt += f"\nThought: {step.thought}\n"
            if step.is_final:
                prompt += f"Final Answer: {step.answer}\n"
            else:
                prompt += f"Action: {step.action}\n"
                prompt += f"Action Input: {step.action_input}\n"
                prompt += f"Observation: {step.observation}\n"

        return prompt

    def _parse_response(self, response: str) -> AgentStep:
        """Parsea la respuesta del LLM en un AgentStep."""
        step = AgentStep(thought="")

        # Extraer Thought
        thought_match = re.search(
            r"Thought:\s*(.+?)(?=\n(?:Action|Final Answer):)",
            response, re.DOTALL
        )
        if thought_match:
            step.thought = thought_match.group(1).strip()

        # ¿Es respuesta final?
        final_match = re.search(
            r"Final Answer:\s*(.+)", response, re.DOTALL
        )
        if final_match:
            step.is_final = True
            step.answer = final_match.group(1).strip()
            return step

        # Extraer Action y Action Input
        action_match = re.search(r"Action:\s*(.+)", response)
        input_match = re.search(r"Action Input:\s*(.+)", response)

        if action_match:
            step.action = action_match.group(1).strip()
        if input_match:
            step.action_input = input_match.group(1).strip()

        return step

    def _detect_cycle(self) -> bool:
        """Detecta si el agente está repitiendo acciones.

        Busca ciclos de cualquier periodo comparando la primera mitad
        de las acciones recientes con la segunda mitad.
        """
        actions = [
            f"{s.action}:{s.action_input}" for s in self.history
            if not s.is_final
        ]
        if len(actions) < 4:
            return False

        # Verificar ciclos de periodo 1, 2, 3, ...
        max_period = min(len(actions) // 2,
                         self.config.cycle_detection_window)
        for period in range(1, max_period + 1):
            segment = actions[-(2 * period):]
            if segment[:period] == segment[period:]:
                return True

        return False

    def _execute_action(self, step: AgentStep) -> str:
        """Ejecuta la acción y devuelve la observación."""
        if step.action not in self.tools:
            return (f"Error: herramienta '{step.action}' no existe. "
                    f"Disponibles: {list(self.tools.keys())}")

        tool_fn = self.tools[step.action]["fn"]
        try:
            return tool_fn(step.action_input)
        except Exception as e:
            return f"Error ejecutando {step.action}: {e}"

    def run(self, question: str) -> str:
        """Ejecuta el loop agéntico completo."""
        self.history = []
        self.tokens_used = 0

        for step_num in range(self.config.max_steps):
            # Verificar presupuesto de tokens
            if self.tokens_used > self.config.max_tokens_budget:
                return (f"Presupuesto de tokens agotado "
                        f"({self.tokens_used} tokens usados). "
                        f"Mejor respuesta parcial: "
                        f"{self._best_partial_answer()}")

            # Detectar ciclos
            if self._detect_cycle():
                return (f"Ciclo detectado después de {step_num} pasos. "
                        f"El agente está repitiendo las mismas acciones. "
                        f"Mejor respuesta parcial: "
                        f"{self._best_partial_answer()}")

            # Generar el siguiente paso
            prompt = self._build_step_prompt(question)
            response = self.llm.generate(prompt)
            # Estimación burda: ~1.3 tokens por palabra en español.
            # En producción, usa el tokenizer de tu modelo (tiktoken
            # para OpenAI, etc.) para un conteo preciso.
            self.tokens_used += int(
                (len(prompt.split()) + len(response.split())) * 1.3
            )

            # Parsear la respuesta
            step = self._parse_response(response)

            # ¿Respuesta final?
            if step.is_final:
                self.history.append(step)
                return step.answer

            # Ejecutar la acción
            step.observation = self._execute_action(step)
            self.history.append(step)

            print(f"[Paso {step_num + 1}] "
                  f"Thought: {step.thought[:80]}...")
            print(f"  Action: {step.action}({step.action_input})")
            print(f"  Observation: {step.observation[:100]}...")
            print()

        return (f"Límite de {self.config.max_steps} pasos alcanzado. "
                f"Mejor respuesta parcial: "
                f"{self._best_partial_answer()}")

    def _best_partial_answer(self) -> str:
        """Intenta dar la mejor respuesta parcial posible."""
        if not self.history:
            return "No se pudo generar ninguna respuesta."

        observations = [
            s.observation for s in self.history
            if s.observation and "Error" not in s.observation
        ]
        if observations:
            return f"Basado en {len(observations)} observaciones: " + \
                   observations[-1]
        return self.history[-1].thought
```

Para usar este agente, solo necesitas un wrapper alrededor de cualquier LLM:

```python
# Ejemplo de uso con un LLM hipotético
class SimpleLLM:
    """Wrapper minimalista para cualquier API de LLM."""
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate(self, prompt: str) -> str:
        # Aquí iría la llamada a OpenAI, Anthropic, etc.
        # response = client.chat.completions.create(...)
        # return response.choices[0].message.content
        pass

# Crear y ejecutar el agente
llm = SimpleLLM(api_key="tu-api-key")
agent = ReActAgent(
    llm=llm,
    tools=TOOLS,
    config=AgentConfig(
        max_steps=10,
        max_tokens_budget=30_000,
        cycle_detection_window=3
    )
)

answer = agent.run("¿Cuánto es 2^10 y quién inventó la computación?")
print(f"Respuesta final: {answer}")
```

Observa que todo el agente son unas 150 líneas de Python. No hay magia. No hay frameworks opacos. Es un loop `for` con parsing de texto, ejecución de funciones y acumulación de historial. Eso es todo lo que un agente de IA es en su núcleo.

Los frameworks como LangChain, LangGraph y CrewAI añaden cosas valiosas: mejor manejo de errores, checkpointing, serialización del estado, observabilidad, integración con múltiples proveedores de LLMs. Pero el corazón es esto: un loop que piensa, actúa y observa.

## El loop es simple. Lo difícil es todo lo demás.

Hemos recorrido un camino largo: desde los pilotos de combate de John Boyd y los termostatos de la cibernética, pasando por el paper de ReAct y sus variantes, hasta un agente implementado desde cero en Python.

La conclusión más importante es que el loop agéntico en sí es **conceptualmente simple**. Es un `while True` con tres pasos. Es el mismo patrón que Polya describió para resolver problemas matemáticos, que Wiener formalizó para sistemas cibernéticos, y que Boyd usó para modelar combate aéreo. Percibir, razonar, actuar, verificar. Repetir.

Lo verdaderamente difícil son las preguntas que rodean al loop:

**¿Cuándo parar?** Como vimos, el halting problem nos dice que no hay solución general. Usamos heurísticas: límites de pasos, presupuestos de tokens, detección de ciclos, umbrales de confianza. Ninguna es perfecta, pero la combinación funciona razonablemente bien.

**¿Qué hacer cuando falla?** Las variantes como Reflexion nos dan un mecanismo para aprender de los errores dentro de la misma sesión. LATS nos permite explorar múltiples caminos. Plan-and-Execute nos da una visión global antes de actuar. Cada variante aborda un modo de fallo diferente.

**¿Cómo organizar el flujo?** Los agentes simples funcionan bien con un loop imperativo. Los agentes complejos necesitan grafos de estado, máquinas de estados finitos, o alguna otra forma de estructurar las transiciones posibles. La elección entre control flow imperativo y declarativo no es solo una preferencia estética; determina qué tan fácil es depurar, verificar y extender el agente.

**¿Cómo manejar la latencia percibida?** En producción, un agente que tarda 30 segundos en responder pero muestra su razonamiento en streaming es mucho más aceptable que uno que muestra un spinner durante 30 segundos y luego da la respuesta. Diseñar el loop para emitir thoughts y observaciones parciales en tiempo real (via streaming o Server-Sent Events) es fundamental para la experiencia del usuario. No es solo una optimización de UX: el streaming también permite al usuario detectar tempranamente cuando el agente va por mal camino e intervenir.

**¿Cómo evitar trabajo redundante?** En el loop ReAct, es común que el agente llame a la misma herramienta con los mismos argumentos más de una vez. En producción, implementa un caché de resultados de herramientas dentro de cada sesión del agente: si la herramienta es idempotente (búsquedas, lecturas de base de datos) y los argumentos son idénticos, devuelve el resultado cacheado en lugar de ejecutar la herramienta de nuevo. Esto ahorra latencia, tokens y dinero.

**¿Cómo escalar?** En producción, como discutimos en ["De agentes teóricos a agentes en producción"](/2026/02/15/de-agentes-teoricos-a-agentes-en-produccion.html) y en ["Patrones de diseño para sistemas con IA"](/2026/02/15/patrones-de-diseno-para-sistemas-con-ia.html), el loop agéntico se enfrenta a desafíos de latencia, costo, observabilidad y confiabilidad que trascienden su estructura fundamental.

El loop es el heartbeat del agente. Pero así como entender el ciclo fetch-decode-execute de un procesador no te convierte automáticamente en un arquitecto de CPUs, entender el loop agéntico es solo el primer paso para construir agentes que funcionen en el mundo real. El siguiente paso es enfrentarse a la complejidad del mundo real: APIs que fallan, LLMs que alucinan, usuarios que hacen preguntas ambiguas, y presupuestos que se agotan.

El loop es simple. Todo lo demás es ingeniería.

## Referencias y fuentes clave

- **Yao, S. et al. (2022)**. "ReAct: Synergizing Reasoning and Acting in Language Models". arXiv:2210.03629. El paper fundacional del framework ReAct.
- **Shinn, N. et al. (2023)**. "Reflexion: Language Agents with Verbal Reinforcement Learning". arXiv:2303.11366. Introduce la auto-reflexión en loops agénticos.
- **Zhou, A. et al. (2023)**. "Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models". arXiv:2310.04406. LATS y la aplicación de búsqueda en árbol inspirada en MCTS a agentes.
- **Wei, J. et al. (2022)**. "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models". arXiv:2201.11903. El paper que popularizó el chain-of-thought.
- **Boyd, J. (1987)**. "A Discourse on Winning and Losing". Briefings no publicados y no revisados por pares que introdujeron el ciclo OODA. Disponibles a través del archivo de la Air University.
- **Wiener, N. (1948)**. *Cybernetics: Or Control and Communication in the Animal and the Machine*. MIT Press. El texto fundacional de la cibernética.
- **Polya, G. (1945)**. *How to Solve It*. Princeton University Press. El método clásico de resolución de problemas.
- **Turing, A. (1936)**. "On Computable Numbers, with an Application to the Entscheidungsproblem". Proceedings of the London Mathematical Society. El paper donde se demuestra el halting problem.
- **Wang, L. et al. (2023)**. "Plan-and-Solve Prompting". arXiv:2305.04091. Separación de planificación y ejecución en agentes.
