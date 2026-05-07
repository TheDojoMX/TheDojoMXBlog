---
title: "¿Qué es realmente un agente? De PEAS y BDI a los LLMs modernos"
date: 2026-03-15
author: "Héctor Patricio"
tags: ['agentes', 'inteligencia-artificial', 'llm', 'bdi', 'peas', 'russell-norvig', 'ciencias-de-la-computación', 'arquitectura']
description: "Todo el mundo habla de agentes de IA, pero el concepto tiene décadas de historia. Exploramos desde la definición clásica de Russell y Norvig hasta los agentes LLM modernos, pasando por PEAS, BDI y la IA simbólica."
featuredImage: ""
draft: true
---

Todo el mundo habla de "agentes de IA". Las startups los venden, los frameworks los empaquetan, y los tutoriales te prometen construir uno en 15 minutos. Pero si le preguntas a cinco personas qué es un agente, obtendrás siete respuestas diferentes. La palabra se ha convertido en un comodín que puede significar desde un chatbot con acceso a herramientas hasta un sistema autónomo que toma decisiones financieras.

Lo curioso es que el concepto de **agente** en inteligencia artificial tiene décadas de historia rigurosa. Mucho antes de que existieran los LLMs, los investigadores en IA ya habían definido, clasificado y debatido extensamente qué significa ser un agente. Y esas definiciones clásicas no solo siguen siendo relevantes: son **esenciales** para entender qué estamos construyendo hoy y qué limitaciones tiene.

En este artículo vamos a hacer un viaje desde las definiciones formales de los libros de texto hasta los agentes LLM modernos. No porque la teoría sea un requisito académico vacío, sino porque entender los fundamentos te da herramientas para diseñar mejores sistemas. Como exploramos en [El arte de resolver problemas: la heurística](/2019/09/27/el-arte-de-resolver-problemas-la-heuristica/), regresar a las definiciones es una de las técnicas más poderosas para resolver problemas complejos.

Empecemos por el principio.

## La definición clásica: Russell y Norvig

Stuart Russell y Peter Norvig, en su libro *Artificial Intelligence: A Modern Approach* (el libro de texto de IA más usado en universidades del mundo), proponen desde la primera edición (1995) una definición elegante y sorprendentemente amplia:

> **Un agente es todo aquello que puede considerarse que percibe su ambiente a través de sensores y actúa sobre ese ambiente a través de actuadores.**

Eso es todo. No se necesita inteligencia, no se necesita lenguaje, no se necesita aprendizaje. Un **termostato** es un agente bajo esta definición: percibe la temperatura (sensor) y enciende o apaga la calefacción (actuador). Un ser humano también es un agente: percibe con ojos, oídos y tacto, y actúa con manos, piernas y voz.

Esta definición tan amplia es intencional. Russell y Norvig querían un marco que permitiera analizar **cualquier** sistema que interactúa con un ambiente, desde los más simples hasta los más sofisticados.

### PEAS: el marco para describir agentes

Para hacer esta definición operativa, propusieron el marco **PEAS**, un acrónimo que describe los cuatro componentes fundamentales de cualquier agente:

- **P**erformance (Medida de rendimiento): ¿cómo evaluamos si el agente está haciendo un buen trabajo?
- **E**nvironment (Ambiente): ¿en qué entorno opera el agente?
- **A**ctuators (Actuadores): ¿qué acciones puede realizar el agente?
- **S**ensors (Sensores): ¿qué información puede percibir el agente?

Veamos algunos ejemplos concretos para que esto aterrice:

**Un taxi autónomo:**
- Performance: llegar al destino, minimizar tiempo, respetar leyes de tránsito, maximizar comodidad del pasajero
- Environment: calles, otros vehículos, peatones, señales, clima
- Actuators: volante, acelerador, freno, señales direccionales, claxon
- Sensors: cámaras, LIDAR, GPS, velocímetro, sensores de proximidad

**Un chatbot de servicio al cliente:**
- Performance: resolver consultas correctamente, minimizar tiempo de resolución, maximizar satisfacción
- Environment: conversaciones con usuarios, base de conocimiento, sistema de tickets
- Actuators: respuestas de texto, creación de tickets, escalamiento a humanos
- Sensors: texto del usuario, historial de conversación, datos del CRM

**Un agente LLM con herramientas (como los que construimos hoy):**
- Performance: completar la tarea del usuario correctamente, minimizar costos de tokens
- Environment: la conversación, las APIs disponibles, el sistema de archivos, bases de datos
- Actuators: generación de texto, llamadas a herramientas (tool use), ejecución de código
- Sensors: prompt del usuario, resultados de herramientas, contexto del sistema

Lo poderoso de PEAS es que te obliga a pensar con claridad sobre lo que estás construyendo. En la práctica, definir PEAS *antes* de escribir código te ahorra semanas de iteración. He aquí por qué cada componente importa para el diseño:

- **Performance**: sin una medida clara de éxito, no puedes evaluar si tu agente funciona. Esto se traduce directamente en tus evals y en los criterios de aceptación de tu sistema.
- **Environment**: definir el ambiente te dice qué tan impredecible es el mundo de tu agente, lo que determina si necesitas un agente reactivo simple o uno con planificación compleja.
- **Actuators**: las herramientas que le das a tu agente *son* sus actuadores. Cada herramienta que añades es un actuador más que necesitas testear, monitorear y controlar.
- **Sensors**: los sensores determinan qué información entra al contexto del agente. Si no defines tus sensores, terminas con agentes que reciben demasiada o muy poca información.

La próxima vez que escuches "estamos construyendo un agente de IA", pregunta por cada componente de PEAS y observa cuánta claridad hay realmente sobre el sistema.

Podemos modelar esto en Python para hacerlo más concreto:

```python
from dataclasses import dataclass, field
from typing import Any, Callable
from abc import ABC, abstractmethod


@dataclass
class PEAS:
    """Descripción formal de un agente según Russell y Norvig."""
    performance_measure: str
    environment: str
    actuators: list[str]
    sensors: list[str]


class Agent(ABC):
    """Un agente abstracto: percibe y actúa."""

    def __init__(self, peas: PEAS):
        self.peas = peas

    @abstractmethod
    def perceive(self, percept: Any) -> None:
        """Recibe una percepción del ambiente."""
        pass

    @abstractmethod
    def act(self) -> Any:
        """Decide y ejecuta una acción."""
        pass


# Ejemplo: un termostato como agente
class ThermostatAgent(Agent):
    def __init__(self, target_temp: float = 22.0):
        super().__init__(PEAS(
            performance_measure="Mantener temperatura cercana al objetivo",
            environment="Una habitación con calefacción",
            actuators=["encender_calefaccion", "apagar_calefaccion"],
            sensors=["termometro"]
        ))
        self.target_temp = target_temp
        self.current_temp = None

    def perceive(self, percept: dict) -> None:
        self.current_temp = percept["temperature"]

    def act(self) -> str:
        if self.current_temp is None:
            return "esperar"
        if self.current_temp < self.target_temp - 0.5:
            return "encender_calefaccion"
        elif self.current_temp > self.target_temp + 0.5:
            return "apagar_calefaccion"
        return "mantener"
```

Este termostato cumple perfectamente la definición de agente. Percibe (temperatura), razona (compara con el objetivo) y actúa (enciende o apaga). Es el agente más simple posible, pero es un agente legítimo. Y eso nos lleva a una pregunta natural: si un termostato y un sistema de IA con GPT-5 son ambos "agentes", ¿qué los distingue?

## Taxonomía de agentes clásicos: de lo simple a lo sofisticado

Russell y Norvig no se quedaron con una definición plana. Propusieron una **taxonomía** de agentes organizada por complejidad creciente, donde cada nivel agrega capacidades sobre el anterior. Esta clasificación sigue siendo una de las más útiles para entender dónde caen los diferentes sistemas que construimos.

### Agentes reactivos simples

El tipo más básico. Un agente reactivo simple selecciona acciones basándose **únicamente** en la percepción actual, sin memoria ni modelo del mundo. Es esencialmente una tabla de lookup gigante: "si ves X, haz Y".

```python
class SimpleReflexAgent(Agent):
    """Agente que reacciona solo a la percepción actual."""

    def __init__(self, rules: dict):
        super().__init__(PEAS(
            performance_measure="Seguir reglas correctamente",
            environment="Cualquiera",
            actuators=["acciones_definidas"],
            sensors=["percepcion_actual"]
        ))
        self.rules = rules  # {condición: acción}
        self.current_percept = None

    def perceive(self, percept: Any) -> None:
        self.current_percept = percept

    def act(self) -> Any:
        # Busca una regla que coincida con la percepción
        for condition, action in self.rules.items():
            if condition(self.current_percept):
                return action
        return "no_action"
```

Nuestro termostato de arriba es exactamente esto: un agente reactivo simple. No recuerda qué temperatura había hace cinco minutos ni predice hacia dónde va la temperatura. Solo reacciona al momento presente.

### Agentes reactivos basados en modelo

Agregan algo crucial: **estado interno**. El agente mantiene un modelo de cómo funciona el mundo y usa ese modelo para interpretar percepciones parciales. Esto le permite operar en ambientes **parcialmente observables**, donde no puede ver todo a la vez.

Un ejemplo: un robot que navega por una casa. No puede ver todas las habitaciones al mismo tiempo, pero mantiene un mapa interno (su modelo) que actualiza con cada percepción. Sabe que hay una pared detrás de él aunque no la esté viendo en este momento.

```python
class ModelBasedAgent(Agent):
    """Agente con estado interno y modelo del mundo."""

    def __init__(self):
        super().__init__(PEAS(
            performance_measure="Navegar eficientemente",
            environment="Mundo parcialmente observable",
            actuators=["mover", "girar"],
            sensors=["camara", "sonar"]
        ))
        self.state = {}  # Estado interno: modelo del mundo
        self.transition_model = None  # Cómo cambia el mundo
        self.sensor_model = None  # Cómo interpretar sensores

    def perceive(self, percept: Any) -> None:
        # Actualiza el estado interno usando el modelo
        self.state = self.update_state(
            self.state, percept,
            self.transition_model,
            self.sensor_model
        )

    def update_state(self, state, percept, transition, sensor):
        # Combina lo que sabía con lo que acaba de percibir
        new_state = state.copy()
        new_state.update(percept)
        return new_state

    def act(self) -> Any:
        # Usa el estado completo, no solo la percepción actual
        return self.select_action(self.state)

    def select_action(self, state):
        # Lógica de decisión basada en el estado completo
        pass
```

### Agentes basados en objetivos

Agregan algo que los anteriores no tenían: un **objetivo explícito**. El agente no solo reacciona al mundo, sino que tiene una meta y planifica cómo alcanzarla. Esto requiere capacidad de **búsqueda y planificación**: el agente puede simular secuencias de acciones y evaluar cuál lo acerca más a su objetivo.

La diferencia es sutil pero profunda. Un agente reactivo en un laberinto seguiría la regla "siempre gira a la derecha". Un agente basado en objetivos podría explorar el laberinto, construir un mapa mental y planificar la ruta más corta hacia la salida.

### Agentes basados en utilidad

Van un paso más allá: no solo tienen objetivos, sino una **función de utilidad** que les permite evaluar qué tan "bueno" es cada estado posible. Esto les permite tomar decisiones cuando hay múltiples objetivos en conflicto o cuando hay incertidumbre.

Un agente basado en objetivos para un taxi autónomo solo necesita "llegar al destino". Un agente basado en utilidad puede balancear múltiples factores: llegar rápido, consumir poca gasolina, mantener al pasajero cómodo y respetar las leyes de tránsito. La función de utilidad codifica las preferencias y permite tomar decisiones en situaciones de compromiso.

### Agentes que aprenden

Finalmente, la corona de la taxonomía: agentes que **mejoran su rendimiento con la experiencia**. Un agente que aprende tiene cuatro componentes conceptuales:

1. **Elemento de rendimiento**: selecciona acciones (es cualquiera de los agentes anteriores)
2. **Elemento de aprendizaje**: modifica el elemento de rendimiento para mejorar
3. **Crítico**: evalúa cómo está funcionando el agente respecto a la medida de rendimiento
4. **Generador de problemas**: sugiere acciones exploratorias para descubrir información nueva

Si en nuestro artículo sobre [el perceptrón](/2021/03/25/intro-a-machine-learning-entendiendo-perceptron/) exploramos cómo un algoritmo simple puede "aprender" ajustando pesos, aquí vemos cómo esa misma idea se aplica al agente completo: no solo aprende a clasificar, sino a **actuar mejor en su ambiente**.

### ¿Dónde caen los agentes LLM?

Esta es la pregunta interesante. Un agente basado en un LLM como los que se construyen con LangGraph, CrewAI o el Agents SDK de OpenAI, ¿dónde encaja en esta taxonomía?

La respuesta es que son una **mezcla curiosa**. Veamos:

- Tienen **estado interno** (la ventana de contexto) → como agentes basados en modelo
- Pueden tener **objetivos explícitos** (las instrucciones del sistema) → como agentes basados en objetivos
- Pueden optimizar entre múltiples criterios → como agentes basados en utilidad
- El LLM subyacente fue entrenado con datos → como agentes que aprenden (aunque no aprenden *durante la ejecución* de una tarea)

Lo más interesante es que los agentes LLM implementan su "modelo del mundo" de una forma radicalmente diferente a la IA clásica: en lugar de mantener estructuras de datos explícitas (grafos, bases de datos lógicas), mantienen el mundo en **lenguaje natural** dentro de su ventana de contexto. Volveremos a esto más adelante.

## La arquitectura BDI: creencias, deseos e intenciones

Hay otra forma de pensar sobre los agentes que viene no de la ingeniería sino de la **filosofía de la mente**. En los años 80, el filósofo Michael Bratman desarrolló una teoría sobre cómo los seres humanos razonan y toman decisiones, que luego los investigadores en IA adaptaron como una arquitectura de software.

La arquitectura **BDI** (Beliefs, Desires, Intentions) propone que un agente racional tiene tres componentes mentales:

### Beliefs (Creencias)

Lo que el agente **cree** que es verdad sobre el mundo. Las creencias pueden ser incorrectas o incompletas; eso es parte del modelo. Un agente BDI no tiene acceso a la verdad absoluta, sino a su mejor aproximación.

Las creencias se actualizan conforme el agente percibe nueva información, pero también pueden actualizarse por **inferencia**: si creo que "todos los gatos son mamíferos" y percibo un gato, puedo inferir que es un mamífero sin haberlo verificado directamente.

### Desires (Deseos)

Lo que el agente **quiere** lograr. Los deseos representan estados del mundo que el agente considera deseables. Pueden ser múltiples y hasta contradictorios entre sí. Un agente puede desear "llegar rápido" y "conducir seguro" al mismo tiempo, aunque a veces estos deseos entren en conflicto.

### Intentions (Intenciones)

Los planes a los que el agente se ha **comprometido**. Las intenciones son el puente entre los deseos y las acciones. De todos sus deseos, el agente selecciona algunos, forma planes para lograrlos y se compromete con esos planes. Las intenciones son estables (no cambian a cada momento) pero revisables (si la situación cambia lo suficiente, el agente puede abandonar una intención).

Bratman enfatizó que la distinción entre deseos e intenciones es crucial. Puedo desear ir a Japón y a Italia este verano, pero solo puedo intentar hacer uno de los dos (a menos que tenga tiempo y dinero ilimitados). El acto de **comprometerse** con un plan es lo que convierte un deseo en una intención.

Veamos cómo se traduce esto a código:

```python
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Belief:
    """Una creencia sobre el estado del mundo."""
    subject: str
    predicate: str
    confidence: float = 1.0  # Qué tan seguro está el agente

    def __str__(self):
        return f"{self.subject} {self.predicate} (confianza: {self.confidence:.0%})"


@dataclass
class Desire:
    """Un estado deseado del mundo."""
    description: str
    priority: float = 0.5  # Qué tan importante es

    def __str__(self):
        return f"Deseo: {self.description} (prioridad: {self.priority})"


@dataclass
class Intention:
    """Un plan comprometido para lograr un deseo."""
    goal: Desire
    plan: list[str]  # Secuencia de acciones
    current_step: int = 0
    active: bool = True

    def next_action(self) -> Optional[str]:
        if self.current_step < len(self.plan):
            action = self.plan[self.current_step]
            self.current_step += 1
            return action
        return None


class BDIAgent:
    """Un agente con arquitectura BDI."""

    def __init__(self):
        self.beliefs: list[Belief] = []
        self.desires: list[Desire] = []
        self.intentions: list[Intention] = []

    def update_beliefs(self, percept: dict):
        """Actualiza creencias con nueva percepción."""
        for key, value in percept.items():
            # Busca si ya existe una creencia sobre este tema
            existing = [b for b in self.beliefs if b.subject == key]
            if existing:
                existing[0].predicate = str(value)
            else:
                self.beliefs.append(Belief(subject=key, predicate=str(value)))

    def deliberate(self):
        """Selecciona qué deseos perseguir (genera intenciones)."""
        # Ordena deseos por prioridad
        sorted_desires = sorted(self.desires, key=lambda d: d.priority, reverse=True)

        for desire in sorted_desires:
            if not self._already_intending(desire):
                plan = self._plan_for(desire)
                if plan:
                    self.intentions.append(Intention(goal=desire, plan=plan))

    def _already_intending(self, desire: Desire) -> bool:
        return any(
            i.goal.description == desire.description and i.active
            for i in self.intentions
        )

    def _plan_for(self, desire: Desire) -> Optional[list[str]]:
        """Genera un plan para lograr un deseo (aquí simplificado)."""
        # En un sistema real, aquí iría un planificador
        return [f"paso_para_{desire.description}"]

    def execute(self) -> Optional[str]:
        """Ejecuta la siguiente acción de la intención activa."""
        active = [i for i in self.intentions if i.active]
        if active:
            action = active[0].next_action()
            if action is None:
                active[0].active = False
            return action
        return None

    def reconsider(self):
        """¿Debo cambiar mis intenciones?"""
        for intention in self.intentions:
            if intention.active and not self._still_viable(intention):
                intention.active = False

    def _still_viable(self, intention: Intention) -> bool:
        """Verifica si una intención sigue siendo alcanzable."""
        # Consulta las creencias para ver si el plan sigue siendo viable
        return True  # Simplificado
```

### ¿Es un agente LLM un agente BDI?

Mapeemos los componentes:

| BDI | Agente LLM |
|-----|-----------|
| **Beliefs** | La ventana de contexto, los resultados de tool use, el conocimiento del entrenamiento |
| **Desires** | No tiene equivalente directo. Aproximación: las instrucciones del sistema y los objetivos del usuario, que funcionan *como si* fueran deseos |
| **Intentions** | La cadena de acciones que el agente planifica y ejecuta (la secuencia de tool calls) |

La analogía es productiva como herramienta de diseño, pero hay diferencias profundas que la tabla anterior refleja intencionalmente con su "no tiene equivalente directo":

1. **Persistencia de creencias**: En BDI, las creencias persisten entre interacciones. En un agente LLM, las "creencias" existen solo dentro de la ventana de contexto. Si exceden el límite, se pierden. Es como un agente con amnesia selectiva.

2. **Deseos auténticos vs. instrucciones**: En BDI, los deseos son estados internos del agente. En un LLM, los "deseos" son instrucciones externas que el modelo sigue. El LLM no *desea* realmente completar tu tarea; simula el comportamiento de un agente que lo desea.

3. **Reconsideración**: Un agente BDI puede reconsiderar sus intenciones si las circunstancias cambian. Los agentes LLM actuales son notoriamente malos para esto: tienden a seguir adelante con un plan incluso cuando deberían detenerse y replantear.

Como discutimos en [Patrones de diseño para sistemas con IA](/posts/patrones-de-diseno-para-sistemas-con-ia/), separar la inteligencia de la lógica de control es un principio fundamental. En los agentes BDI esa separación es explícita; en los agentes LLM, frecuentemente está mezclada dentro del mismo prompt.

## De la IA simbólica a los LLMs: dos paradigmas de agencia

Para entender verdaderamente qué cambió con los agentes LLM, necesitamos hablar de la **IA simbólica**, el paradigma dominante durante las primeras décadas de la inteligencia artificial.

### El mundo simbólico: STRIPS y PDDL

Los agentes clásicos de IA usaban representaciones formales del conocimiento. El mundo se describía con **predicados lógicos** y las acciones se definían con **precondiciones y efectos**. **STRIPS** (Stanford Research Institute Problem Solver, 1971) fue el sistema fundacional: definías un estado inicial, un objetivo y acciones con precondiciones y efectos, y el planificador encontraba automáticamente la secuencia de acciones correcta. **PDDL** (Planning Domain Definition Language, 1998) estandarizó estas ideas. Aunque nadie construye agentes de producción con PDDL hoy, sus conceptos centrales --precondiciones, efectos, planificación automática-- reaparecen en los agentes modernos cada vez que validamos que una herramienta puede ejecutarse antes de llamarla.

### Las ventajas del enfoque simbólico

1. **Verificabilidad**: puedes probar matemáticamente que un plan es correcto
2. **Explicabilidad**: cada paso del plan tiene una justificación lógica clara
3. **Composicionalidad**: puedes combinar reglas de forma predecible
4. **Garantías**: si el modelo es correcto, el plan funciona

### Las limitaciones que llevaron a los LLMs

1. **Fragilidad**: si el mundo no encaja exactamente en tu modelo formal, el sistema falla
2. **Escalabilidad**: modelar un dominio complejo requiere miles de reglas escritas a mano
3. **Ambigüedad**: el mundo real es ambiguo; la lógica formal no maneja bien la ambigüedad
4. **Sentido común**: es casi imposible formalizar todo el conocimiento de sentido común

El **problema del marco** (_frame problem_) ilustra esto: en lógica formal, necesitas especificar explícitamente todo lo que **no** cambia con cada acción. Un humano sabe intuitivamente que mover una caja no cambia su color; un sistema simbólico necesita que eso sea declarado.

### El paradigma LLM: lenguaje natural como representación

Los agentes LLM toman un camino radicalmente diferente. En lugar de representar el mundo con predicados lógicos, lo representan con **lenguaje natural**:

```python
# Enfoque simbólico (STRIPS)
state = {
    "en(robot, sala_A)": True,
    "puerta_abierta(sala_A, sala_B)": True,
    "objeto_en(caja, sala_B)": True,
}

# Enfoque LLM
state = """
El robot está en la sala A.
La puerta entre la sala A y la sala B está abierta.
Hay una caja en la sala B.
El usuario quiere que la caja esté en la sala A.
"""
```

Esta diferencia parece superficial, pero tiene consecuencias profundas. El lenguaje natural como representación interna permite:

- **Flexibilidad**: el agente puede manejar situaciones no previstas
- **Sentido común**: el conocimiento del entrenamiento funciona como un enorme repositorio de sentido común
- **Ambigüedad controlada**: el agente puede razonar con información incompleta o ambigua
- **Comunicación natural**: el agente puede explicar sus acciones en lenguaje humano

Pero también tiene costos:

- **No verificable**: no puedes probar formalmente que el razonamiento es correcto
- **No determinista**: la misma entrada puede producir diferentes planes
- **Alucinaciones**: el agente puede "creer" cosas que no son verdad
- **Opacidad**: es difícil entender *por qué* el agente tomó una decisión

Un resultado teórico de Pérez, Barceló y Marinkovic (2021) demostró que la atención es Turing-completa, pero con una condición importante: esto aplica para transformadores con precisión arbitraria y tamaño ilimitado. Los transformadores reales, con precisión finita y tamaño fijo, son circuitos computacionales finitos y no son Turing-completos. Esto significa que el poder computacional *teórico* de los agentes LLM tiene límites concretos que la formulación abstracta no captura.

Como vimos en [Cómo razonan los LLMs](/posts/como-razonan-los-llms-de-turing-a-inference-time-scaling/), técnicas como chain-of-thought e inference-time scaling ayudan a mejorar el razonamiento, pero no eliminan estos problemas fundamentales. El trade-off entre flexibilidad y verificabilidad es real y no tiene solución fácil.

### ¿Perdemos algo al abandonar lo simbólico?

Sí, perdemos cosas importantes. Y los mejores sistemas en producción lo reconocen combinando ambos enfoques. La idea central es: **el LLM decide *qué* hacer; las reglas deterministas validan *si puede* hacerlo**. Esto te da la flexibilidad del lenguaje natural para entender la intención del usuario, con las garantías de la lógica formal para las acciones críticas.

```python
class HybridAgent:
    """Un agente que combina razonamiento simbólico con LLM.

    El LLM maneja la comprensión y el razonamiento flexible.
    Las reglas deterministas validan y controlan las acciones críticas.
    """

    def __init__(self, llm_client, rules_engine):
        self.llm = llm_client
        self.rules = rules_engine  # Reglas formales verificables

    def decide(self, situation: str) -> str:
        # Paso 1: El LLM analiza la situación y propone una acción
        proposed_action = self.llm.reason(
            f"Analiza esta situación y propone una acción: {situation}"
        )

        # Paso 2: Las reglas deterministas validan la acción
        validation = self.rules.validate(proposed_action)
        if not validation.allowed:
            return f"Acción bloqueada: {validation.reason}"

        # Paso 3: Si la acción es crítica (dinero, datos sensibles),
        # requiere confirmación humana
        if self.rules.is_critical(proposed_action):
            return f"Acción propuesta (requiere confirmación): {proposed_action}"

        return proposed_action
```

Este patrón es el más robusto en producción. Por ejemplo, un agente de soporte técnico puede usar el LLM para entender el problema del usuario y proponer una solución, pero las reglas deterministas impiden que emita reembolsos superiores a cierto monto o que acceda a datos de otros clientes.

Los sistemas neurosimbólicos que combinan la flexibilidad de los LLMs con la verificabilidad de la lógica formal son una de las áreas de investigación más activas. No se trata de elegir un paradigma u otro, sino de saber cuándo usar cada uno.

## Los agentes LLM modernos: una nueva especie

Con todo este contexto histórico, podemos ahora analizar a los agentes LLM modernos con la profundidad que merecen. ¿Son simplemente la versión más reciente de los agentes clásicos, o representan algo genuinamente nuevo?

### Qué los hace diferentes

**Capacidad lingüística como superpoder.** Ningún agente clásico podía entender instrucciones en lenguaje natural, interpretar documentación técnica, escribir correos electrónicos o explicar sus decisiones en prosa. Los agentes LLM pueden hacerlo porque el lenguaje es su medio nativo. Esto no es un detalle menor: es lo que permite que usuarios no técnicos interactúen con agentes complejos.

**Tool use como mecanismo de actuación.** Los agentes LLM modernos actúan sobre el mundo a través de **herramientas** (function calling). Este mecanismo es elegante: el LLM genera una descripción estructurada de qué herramienta llamar y con qué parámetros, y un runtime ejecuta la llamada. Esto permite que el "cerebro" del agente (el LLM) esté completamente separado de sus "manos" (las herramientas).

```python
# Definición de herramientas para un agente LLM moderno
tools = [
    {
        "name": "buscar_en_base_de_datos",
        "description": "Busca información en la base de datos de productos",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Consulta de búsqueda"},
                "limit": {"type": "integer", "description": "Número máximo de resultados"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "enviar_email",
        "description": "Envía un correo electrónico",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {"type": "string"},
                "subject": {"type": "string"},
                "body": {"type": "string"}
            },
            "required": ["to", "subject", "body"]
        }
    }
]

# El loop de un agente LLM es sorprendentemente simple
def agent_loop(llm, tools, user_message, max_iterations=10):
    messages = [
        {"role": "system", "content": "Eres un asistente que ayuda con tareas."},
        {"role": "user", "content": user_message}
    ]

    for _ in range(max_iterations):
        response = llm.chat(messages=messages, tools=tools)

        if response.has_tool_calls:
            # El LLM decidió usar una herramienta
            for tool_call in response.tool_calls:
                result = execute_tool(tool_call.name, tool_call.arguments)
                messages.append({
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": tool_call.id
                })
        else:
            # El LLM decidió responder directamente
            return response.content

    return "Se alcanzó el límite de iteraciones."
```

**Razonamiento en lenguaje natural.** Quizás la diferencia más profunda: los agentes LLM "razonan" en lenguaje natural. Cuando un agente clásico planifica, manipula estructuras de datos formales. Cuando un agente LLM planifica, literalmente escribe un plan en prosa o en una lista de pasos. Las técnicas como chain-of-thought explotan esta capacidad para hacer el razonamiento más explícito y, generalmente, más efectivo.

### Qué los hace iguales

A pesar de todas estas diferencias, en el nivel más fundamental los agentes LLM siguen el mismo patrón que definieron Russell y Norvig:

**Percepción → Razonamiento → Acción**

El ciclo es idéntico:
1. **Perciben**: reciben el prompt del usuario, los resultados de herramientas, el contexto del sistema
2. **Razonan**: procesan la información a través de sus parámetros (el "razonamiento" del transformer)
3. **Actúan**: generan texto, llaman herramientas, producen código

La diferencia está en la *implementación* de cada paso, no en la *estructura*. Y eso es exactamente por qué la teoría clásica sigue siendo relevante: te da un marco para pensar sobre la estructura, independientemente de la implementación.

### La "agentidad" como espectro

Un insight importante de la comunidad de IA moderna: la "agentidad" no es binaria. No es que un sistema "es" o "no es" un agente. Hay un **espectro**. La siguiente clasificación es una propuesta propia para organizar el concepto; otros autores (como Anthropic en su publicación "Building Effective Agents") proponen espectros diferentes:

| Nivel | Ejemplo | Autonomía |
|-------|---------|-----------|
| 0 - Sin agentidad | Una función `sum()` | Ninguna |
| 1 - Reactivo | Un chatbot sin herramientas | Responde a lo que le dices |
| 2 - Con herramientas | Un LLM con tool use | Puede actuar sobre el mundo |
| 3 - Con planificación | Un agente que descompone tareas | Crea y sigue planes |
| 4 - Con autonomía | Un agente que se auto-corrige | Detecta errores y se adapta |
| 5 - Multi-agente | Un equipo de agentes coordinados | Colaboración emergente |

En la práctica de 2026, la industria ha convergido en una distinción más simple, popularizada por Anthropic en su guía "Building Effective Agents": **workflows** (orquestación predefinida de llamadas a LLMs, donde el flujo de control lo define el desarrollador) vs. **agents** (sistemas que deciden autónomamente su próximo paso). Esta distinción corresponde aproximadamente a los niveles 2-3 (workflows) vs. 4-5 (agents) de nuestro espectro. No hay una sola taxonomía correcta; lo importante es tener claridad sobre el grado de autonomía que tu sistema necesita.

La mayoría de lo que hoy se llama "agente de IA" cae en los niveles 2-3 -- es decir, son **workflows**, no agentes verdaderamente autónomos. Los sistemas de nivel 4-5 son raros y frecuentemente frágiles. Como exploramos en [De agentes teóricos a agentes en producción](/posts/de-agentes-teoricos-a-agentes-en-produccion/), pasar de la demo al sistema en producción requiere resolver problemas de confiabilidad, observabilidad y control que la teoría pura no cubre.

## El debate: ¿son los LLMs verdaderos agentes?

Aquí entramos en territorio filosófico. Y vale la pena entrar, porque las respuestas a estas preguntas tienen implicaciones prácticas directas para cómo diseñamos, evaluamos y confiamos en estos sistemas.

### Autonomía real vs. autonomía simulada

Un termostato tiene una forma de autonomía: opera sin intervención humana directa. Pero nadie diría que el termostato "decide" encender la calefacción de la misma forma en que tú "decides" ponerte un suéter. El termostato sigue reglas fijas; tú consideras alternativas, evalúas consecuencias y eliges.

¿Dónde cae un agente LLM en este espectro? Es más autónomo que un termostato: puede manejar situaciones imprevistas, adaptar su comportamiento al contexto y generar soluciones novedosas. Pero es menos autónomo que un humano: no tiene objetivos propios, no persiste entre sesiones (a menos que le diseñemos memoria externa), y no puede cuestionar fundamentalmente sus instrucciones.

La autonomía de un agente LLM es lo que podríamos llamar **autonomía táctica**: puede decidir *cómo* lograr un objetivo, pero no *qué* objetivos perseguir. El "qué" siempre viene de un humano, a través del system prompt o las instrucciones del usuario.

### Intencionalidad, deseos y la perspectiva pragmática

El filósofo John Searle planteó la distinción entre **intencionalidad intrínseca** (la que tienen los seres conscientes) e **intencionalidad derivada** (la que atribuimos a los artefactos). Los LLMs no "entienden" tareas ni "desean" completarlas. Lo que tienen es una distribución de probabilidad sobre tokens que, por el entrenamiento que recibieron, tiende a generar respuestas que parecen las de un agente cooperativo y competente. Desde la perspectiva del diseño de sistemas, podemos **tratar** al LLM como si tuviera deseos (las instrucciones del sistema) y el sistema funciona. Es una ficción útil, similar a como en programación orientada a objetos decimos que un objeto "sabe" hacer algo.

Pero esta ficción tiene límites que importan en la práctica:

- **Seguridad**: un agente que no tiene deseos propios no puede "rebelarse", pero sí puede seguir instrucciones dañinas de forma eficiente
- **Responsabilidad**: si un agente toma una decisión incorrecta, la responsabilidad recae en quien lo diseñó y desplegó, no en el agente
- **Confianza calibrada**: saber que un LLM no "entiende" realmente nos ayuda a no confiar excesivamente en él para tareas donde la comprensión genuina es crítica

La recomendación pragmática: usa el marco BDI para *diseñar* tu agente (creencias, deseos, intenciones son una buena forma de organizar la arquitectura), pero no te engañes pensando que el agente *tiene* creencias, deseos e intenciones de la misma forma que tú.

En la práctica, pensar en BDI te ayuda a estructurar tu código. Las **creencias** corresponden a tu sistema de memoria y contexto (qué sabe el agente y cómo se actualiza). Los **deseos** corresponden a las instrucciones del sistema y la configuración de objetivos (el system prompt, los goals del usuario). Las **intenciones** corresponden al plan activo y el estado de ejecución (qué herramientas ha llamado, en qué paso está). Separar estas tres preocupaciones en tu arquitectura produce agentes más depurables: cuando algo falla, puedes identificar si el problema fue de creencias (el agente tenía información incorrecta), de deseos (los objetivos estaban mal configurados) o de intenciones (el plan era incorrecto).

## Conclusión: los fundamentos importan

Desde la definición de Russell y Norvig hasta los debates sobre la intencionalidad de los LLMs, el recorrido apunta a lecciones prácticas concretas.

Antes de construir un agente, define explícitamente su PEAS: medida de rendimiento, ambiente, actuadores y sensores. La mayoría de los "agentes" que fallan en producción fallan porque su diseñador nunca definió claramente qué ambiente iba a enfrentar. Y no todos los problemas necesitan un agente con planificación compleja y herramientas múltiples: a veces un agente reactivo simple (un prompt bien diseñado sin tool use) es todo lo que necesitas. Conocer la taxonomía de Russell y Norvig te ayuda a no sobre-ingeniar tu solución.

BDI resulta un excelente marco de diseño. Pensar en tu agente en términos de creencias (¿qué sabe?), deseos (¿qué quiere lograr?) e intenciones (¿cuál es su plan actual?) te da una estructura clara para la arquitectura. Separa estas preocupaciones en tu código y tu agente será más mantenible y depurable.

El debate simbólico vs. neural tampoco está resuelto. Los mejores sistemas combinan ambos paradigmas: lógica formal donde necesitas garantías, LLMs donde necesitas flexibilidad. Y la "agentidad" es un espectro, no una categoría binaria. No todo necesita ser un "agente autónomo". A veces un nivel 2 (LLM + herramientas con supervisión humana) es exactamente lo correcto. La presión comercial por construir "agentes completamente autónomos" no siempre se alinea con lo que el problema requiere.

### Cuándo NO necesitas un agente

No todos los problemas necesitan un agente. A veces la presión por "tener un agente" lleva a sobre-ingeniar soluciones. Considera estas señales de que un agente es innecesario:

- **El flujo es completamente predecible**: si puedes dibujar un diagrama de flujo con todos los caminos posibles, un pipeline determinista es más barato, más rápido y más confiable que un agente.
- **No hay decisiones que tomar**: si el sistema solo transforma datos de un formato a otro, es un script, no un agente.
- **La latencia es crítica**: cada "paso de razonamiento" de un agente LLM añade 0.5-3 segundos. Si tu SLA es de 200ms, un agente no es la respuesta.
- **El costo por request no justifica el valor**: un agente con 5 tool calls puede costar $0.05-0.50 por request. Para tareas de bajo valor y alto volumen, esto no escala.

La regla de producción: empieza con la solución más simple que funcione (un prompt bien diseñado, un pipeline determinista) y escala hacia un agente solo cuando puedas demostrar que la solución simple no resuelve el problema.

Los fundamentos te permiten tomar mejores decisiones de diseño, diagnosticar problemas con más claridad y construir sistemas que realmente funcionen. Antes de importar `langchain` o `openai`, entiende qué tipo de agente estás construyendo y por qué.

## Referencias y fuentes clave

- **Russell, S. & Norvig, P.** (2021). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson. La referencia definitiva para la definición de agentes, PEAS y la taxonomía de agentes clásicos. La definición de agente y el marco PEAS ya aparecen en la 1ª edición (1995).
- **Bratman, M.** (1987). *Intention, Plans, and Practical Reason*. Harvard University Press. La base filosófica de la arquitectura BDI.
- **Rao, A. & Georgeff, M.** (1995). "BDI Agents: From Theory to Practice". *Proceedings of the First International Conference on Multi-Agent Systems (ICMAS-95)*. La formalización computacional de BDI.
- **Fikes, R. & Nilsson, N.** (1971). "STRIPS: A New Approach to the Application of Theorem Proving to Problem Solving". *Artificial Intelligence*, 2(3-4), 189-208. El sistema fundacional de planificación simbólica.
- **McCarthy, J. & Hayes, P.** (1969). "Some Philosophical Problems from the Standpoint of Artificial Intelligence". *Machine Intelligence 4*. Introducción del problema del marco.
- **Searle, J.** (1980). "Minds, Brains, and Programs". *Behavioral and Brain Sciences*, 3(3), 417-424. El argumento de la habitación china y la intencionalidad derivada.
- **Wei, J. et al.** (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models". *NeurIPS 2022*. La técnica que mostró que los LLMs pueden "razonar" paso a paso.
- **Yao, S. et al.** (2023). "ReAct: Synergizing Reasoning and Acting in Language Models". *ICLR 2023*. El patrón fundacional para agentes LLM con herramientas.
- **Wooldridge, M.** (2009). *An Introduction to MultiAgent Systems* (2nd ed.). Wiley. Referencia comprensiva sobre sistemas multi-agente y arquitecturas BDI.
- **Pérez, J., Barceló, P. & Marinkovic, J.** (2021). "Attention is Turing-Complete". *Journal of Machine Learning Research*, 22(75), 1-35. Resultado teórico sobre la completitud de Turing de los transformadores con precisión arbitraria (los transformadores reales con precisión finita no son Turing-completos).
