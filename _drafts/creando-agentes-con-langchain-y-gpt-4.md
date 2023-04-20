---
title: "Creando agentes con LangChain y GPT-4"
date: 2023-04-17
author: Héctor Patricio
tags: langchain gpt4 agentes
comments: true
excerpt: "Ya vimos como empezar a usar LangChain, avancemos a algo más interesante: crear agentes que puedan interactuar con el exterior."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,q_54,w_1200/v1681776700/DALL_E_2023-04-14_23.49.15_-_a_parrot_in_a_cybernetic_setting_plotting_a_great_plan_to_conquer_the_universe_digital_art_digital_illustration_detailed_cinematic_lightning_pkrwml.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,q_54,w_1200/v1681776700/DALL_E_2023-04-14_23.49.15_-_a_parrot_in_a_cybernetic_setting_plotting_a_great_plan_to_conquer_the_universe_digital_art_digital_illustration_detailed_cinematic_lightning_pkrwml.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

En este pequeño tutorial vamos a hablar de cómo puedes crear agentes que interactúen con el mundo exterior, usando LangChain y como modelo de lenguaje GPT-4. Como siempre, la mejor manera de aprender es haciendo algo, por lo que vamos a crear un agente

### ¿Qué es un agente?

En este contexto, además de una cosa que puede actuar por sí mismo, se entiende que un agente puede hacer dos cosas más:

- Decidir qué hacer y qué herramienta usar
- Aprender a usar herramientas automáticamente (si le proporcionas las cosas que necesita)

Los agentes tradicionalmente se entienden como programas que trabajan de manera autónoma y con su propio espacio de memoria, con los que te comunicas por medio de mensajes, pero que no tienes el control completo sobre ellos. Un agente puede decidir qué hacer con tu mensaje.

Combinando ambos contextos, un agente es un pedazo del programa que actúa autónomamente, que decide cómo lograr lo que has pedido y que aprende a hacerlo por su cuenta. Al estar basado en un LLM, no está garantizado su éxito.

## Agentes en LangChain

LangChain provee de un conjunto de agentes prefabricados. Los más fáciles de usar están basados en un framework llamado ReAct, que propone una forma de crear estos agentes. Puedes ver el paper en el que se habla de ReAct en el siguiente documento: **[ReAct: Synergizing Reasoning and Acting in Language Models
](https://arxiv.org/abs/2210.03629)**.

Básicamente este framework da las guías para crear agentes que usen herramientas de manera efectiva. LangChain provee tres agentes básicos:

- **Zero-shot React Description**: Este agente puede usar herramientas para lograr sus objetivos, pero no puede aprender a usarlas por sí mismo.


### Creando un agente

El siguiente código crea un agente que puede usar herramientas para lograr sus objetivos:

```python
 # Creando un agente con LangChain

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI

llm = OpenAI(temperature=0)

tools = load_tools(["serpapi", "llm-math"], llm=llm)

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

print("Este agente puede buscar en Google y hacer aritmética básica.")
while True:
    query = input("Pregunta algo: ")
    if not query:
        break
    print(agent.run(query))

```

El código anterior es suficiente para crear una agente que tiene dos capacidades: buscar en internet con Google y hacer operaciones matemáticas básicas. El código es bastante simple, pero vamos a explicarlo paso a paso.

Como siempre, la primera parte es importar las funciones y tipos necesarios:

```python
from langchain.agents import load_tools # Es una función que te ayuda a cargar las herramientas que los agentes serán capaces de usar

from langchain.agents import initialize_agent # Es una función que te ayuda a crear un agente de manera sencilla

from langchain.agents import AgentType # Es un tipo que te ayuda a especificar el tipo de agente que quieres crear, contiene todos los tipos de agentes que LangChain provee

from langchain.llms import OpenAI # Es la clase que abstrae la conexión con el LLM que usaremos: GPT, creado por OpenAI

```

Después, creamos una instancia de conexión con el LLM:

```python
llm = OpenAI(temperature=0)
```

El que le digamos que queremos cero de temperatura significa que la respuesta será menos aleatoria, por lo que podemos pensar que será menos "creativa" o arriesgada. Esto es buena idea cuando quieres crear planes, usar herramientas con una interfaz formal, como una API. Para poder usarlo, tienes que poner en el entorno de ejecución la variable de entorno `OPENAI_API_KEY` con tu API key de OpenAI.

Seguido de esto, cargamos las herramientas que queremos que el agente pueda usar, indicando el modelo de lenguaje que usará para interactuar con ellas:

```python
tools = load_tools(["serpapi", "llm-math"], llm=llm)
```

La primera es una herramienta para buscar en Google, se llama [SerpApi](https://serpapi.com/), y permite usar la búsqueda que nosotros hacemos en Google mediante una interfaz más amigable para programas. La versión gratuita te da 100 búsquedas mensuales.

La segunda herramienta, `llm-math`, tiene como objetivo permitir que el agente haga matemáticas básicas, aunque tampoco están garantizadas porque se ejecuta código que el LLM devuelve. El prompt que usa es (lo traduzco a español después):

````
You are GPT-3, and you can't do math.

You can do basic math, and your memorization abilities are impressive, but you can't do any complex calculations that a human could not do in their head. You also have an annoying tendency to just make up highly specific, but wrong, answers.

So we hooked you up to a Python 3 kernel, and now you can execute code. If you execute code, you must print out the final answer using the print function. You MUST use the python package numpy to answer your question. You must import numpy as np.


Question: ${{Question with hard calculation.}}
```python
${{Code that prints what you need to know}}
print(${{code}})
```
```output
${{Output of your code}}
```
Answer: ${{Answer}}

Begin.

Question: What is 37593 * 67?

```python
import numpy as np
print(np.multiply(37593, 67))
```
```output
2518731
```
Answer: 2518731

Question: {question}

````

Traducido al español:

````

Eres GPT-3, y no puedes hacer matemáticas.

Puedes hacer matemáticas básicas, y tus habilidades de memorización son impresionantes, pero no puedes hacer ningún cálculo complejo que un humano no pudiera hacer en su cabeza. También tienes una tendencia molesta a inventar respuestas específicas, pero incorrectas.

Así que te conectamos a un kernel de Python 3, y ahora puedes ejecutar código. Si ejecutas código, debes imprimir el resultado final usando la función print. DEBES usar el paquete python numpy para responder tu pregunta. Debes importar numpy como np.

Pregunta: ${{Pregunta con cálculos duros.}}
```python
${{Código que imprime lo que necesitas saber}}
print(${{código}})
```
```output
${{Salida de tu código}}
```
```
Respuesta: ${{Respuesta}}

Comienza.

Pregunta: ¿Cuánto es 37593 * 67?

```python
import numpy as np
print(np.multiply(37593, 67))
```
```output
2518731
```
Respuesta: 2518731

Pregunta: {Pregunta}
````

Este módulo después extrae la respuesta de la salida del LLM y la ejecuta en un ejecutor de Python y extrae de aquí la respuesta.

Aunque por ser un ejecutor de Python tenemos garantizado que el cálculo es correcto, no tenemos garantizado que el código introducido sea adecuado, así que no confíes siempre en sus cálculos.
