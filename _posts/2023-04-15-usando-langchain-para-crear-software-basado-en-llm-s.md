---
title: "Usando LangChain 🦜 para crear software basado en LLM's"
date: 2023-04-15
author: Héctor Patricio
tags: langchain llm tutorial
comments: true
excerpt: "Vamos a ver cómo funciona LangChain, una herramienta que le puede dar oídos, ojos y manos a tu modelo de lenguaje preferido."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_crop,g_face,h_550,w_1024/v1681538471/DALL_E_2023-04-14_23.53.02_-_a_green_parrot_in_a_cybernetic_setting_plotting_a_plan_to_conquer_the_universe_digital_illustration_detailed_cinematic_light_ff6lm8.png
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_crop,g_face,h_550,w_1024/v1681538471/DALL_E_2023-04-14_23.53.02_-_a_green_parrot_in_a_cybernetic_setting_plotting_a_plan_to_conquer_the_universe_digital_illustration_detailed_cinematic_light_ff6lm8.png
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Los grandes modelos de lenguaje o LLM's (Large Language Models) han sido noticia en este 2023. Es por eso que han surgido muchos proyectos y herramientas que permiten crear software basado en estas herramientas.

En este artículo vamos a poner un pequeño tutorial de una herramienta creada para hacer aplicaciones basadas en LLM's: [LangChain](https://python.langchain.com/en/latest/index.html).

## ¿Qué es LangChain?

Las aplicaciones basadas en procesamiento de lenguaje natural, sea como una herramienta de comunicación o como su producto principal, normalmente requieren fuentes de información para potenciar sus capacidades.

También es una muy buena idea que estas aplicaciones puedan actuar por sí mismas usando las instrucciones creadas por un LLM. Para hacer esto podemos usar **agentes**.

**LangChain** provee componentes que te permiten lograr estas dos tareas, para que tú los uses como quieras, pero también te provee
de cadenas de componentes (_[composición](/) de software, ¿te suena?_) con casos de uso comunes, digamos que prefabricados, para hacer software basado en LLM's de manera más rápida.

Hablemos de qué componentes te provee LangChain para empezar a construir tus programas basados en LLM's.

## Componentes principales

LangChain provee varios tipos de componentes, muchos de los cuales son abstracciones de los conceptos más usados en la interacción con LLM's, veamos algunos de ellos:

- **Texto**. La abstracción más básica es la que representa un texto cualquiera que le mandamos a un LLM. Este texto puede provenir de diferentes fuentes, como archivos, por ejemplo.

- **Divisores de texto**. Generalmente, un modelo de lenguaje no puede consumir mucho texto al mismo tiempo, por lo que para poder procesar textos grandes hay que mandárselos por partes. Este componente se encarga de ayudarte a dividir el texto en partes que el LLM pueda procesar.

- **Índices**. Es una abstracción que presenta el texto de mejor manera para que un LLM pueda acceder a la información mejor. Los índices se tienen que guardar de alguna manera y LangChain provee una interfaz para guardarlos en una base de datos especializada.

- **Modelo**. Esto es la interfaz con un modelo de lenguaje. Te lo puedes imaginar como el equivalente a un conector a base de datos, abstraen los detalles de la conexión y te dan una interfaz común.

- **Agente**. Un agente puede recibir instrucciones en forma de alguna abstracción de texto, para ejecutar acciones en _sistemas externos_ o consultando para consultar al LLM.

- **Cadena**. Las cadenas son conjuntos de componentes que sirven para resolver problemas comunes o crear aplicaciones completas.

Ya que entendemos las cosas que LangChain nos da, veamos cómo usarlas.

## Creando una aplicación de ejemplo

Vamos a crear una aplicación que nos permita consultar todos los posts de este blog y contestar preguntas. Por suerte, existe una cadena que ya nos permite hacer esto.

### Instalación

Primero veamos los requisitos: además de LangChain, necesitas los siguientes paquetes:

- openai
- chromadb
- tiktoken

Por lo que tu requirements.txt debería verse así:

```bash
langchain
openai
chromadb
tiktoken
```

Aquí, recomiendo usar un entorno virtual con [Anaconda](https://www.anaconda.com/products/distribution), sobre todo si tienes planes de seguir trabajando con cosas relacionadas con
procesamiento de datos.

Para hacer la creación e instalación puedes correr los siguientes comandos si tienes `conda`:

```bash

conda create -n entorno_langchain pip
conda activate entorno_langchain
pip install requeriments.txt

```

Aquí `entorno_langchain` es el nombre de nuestro entorno virtual y puede ser cualquiera que tú quieras.
También, para empezar, necesito una fuente de datos para empezar a probar, por lo que voy a copiar algunos posts de este blog, que están en formato markdown y pueden ser consumidas sin ningún programa adicional. Voy a crear una carpeta llamada docs y dentro copiaré los archivos markdown de este blog, que están en _posts. Tú puedes poner ahí los diferentes archivos que quieras consultar, tal vez directamente en docs.

Mi estructura de archivos se ve así (mi carpeta de trabajo es `thedojo_agent`):

```bash

thedojo_agent
├── docs
│   ├── _posts
│   │   ├── 2018-10-28-bienvenidos.md
... muchos archivos más
├── requeriments.txt
```

Teniendo esto listo podemos seguir el ejemplo básico del tutorial de LangChain.

## Creando un script mínimo que funciona

Dentro de un archivo que se llame `main.py` vamos a escribir el siguiente código:

```python

from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator

loader = TextLoader("./docs/_posts/2023-04-07-cuando-separar-el-codigo.md")
index = VectorstoreIndexCreator().from_loaders([loader])


query = "¿Cuándo separar el código?"
print(index.query(query))

query = "¿Qué es un módulo?"
print(index.query_with_sources(query))

```

Primero importamos el componente `TextLoader` que nos permitirá cargar texto de un archivo y el componente `VectorstoreIndexCreator` que nos permitirá crear un índice y almacenarlo como un vector.

Ya nos estamos empezando a meter en cosas que no son tan conocidas. Vamos a explicarlas. Un índice es parecido a lo que se hace en las bases de datos, se analiza la información del texto para guardarle de manera organizada, para que cuando necesitemos encontrar algo, sea fácil de encontrar. Por ejemplo, podría estar organizado por palabras clave y con las referencias a donde se puede encontrar en los textos.

Que se guarde como un vector tiene que ver con la forma en que trabajan los modelos de lenguaje. Lo que en realidad ve un modelo es una lista de tokens, que son números que representan el texto. Cuando un modelo te da una respuesta, te da una lista de tokens junto con la probabilidad de que cada token vaya en ese orden. Esto son los "embeddings", y a final de cuenta son colecciones de números, como listas, lo que se conoce como vectores en este mundo del procesamiento de datos.

Así que primero generamos un índice, que consiste en un conjunto de vectores y después lo guardamos.

Eso es justo lo que hacen las dos líneas que siguen al import.

```python
loader = TextLoader("./docs/_posts/2023-04-07-cuando-separar-el-codigo.md")
index = VectorstoreIndexCreator().from_loaders([loader])
```

Después de esto, ahora consultamos el texto de dos formas:

1. Primero que nos de la respuesta solita.
2. Que nos de la respuestas junto con la fuente de donde la sacó.

Este ejemplo básico ya empieza a hacer por nosotros lo que queríamos en un principio: consultar un texto y obtener una respuesta.

Vamos a ir un poco más hondo en el código.

### ¿Qué hace VectorstoreIndexCreator?

La parte que más magia esconde es el objeto `VectorstoreIndexCreator`. Este objeto es una composición de otros que cumplen estos roles:

1. Un "cortador" de texto, que ayuda a procesar el texto de la fuente.
2. Un modelo de lenguaje para generar los embeddings.
3. Un almacén de datos, en nuestro caso, un `Vectorstore`, o una base de datos que almacene vectores.

El objeto ya hace por nosotros todo el trabajo, el flujo de información, desde la fuente, que en el ejemplo es un texto cargado desde un conjunto de archivos, hasta el almacén de datos, que en el ejemplo es ChromaDB, que es una base de datos que almacena vectores.

ChromaDB puede correr en memoria o como servidor, pero aquí corre como base de datos en memoria, usando por debajo DuckDB, una base de datos completamente en memoria, así que cuando salgas del programa, se borra todo.

Vamos a dejar para un artículo futuro la creación de un índice, explicando sus parámetros.

Si quieres ver un ejmplo funcionando, Alex y yo hicimos un ejemplo y platicamos más de esto en este directo:

<iframe width="560" height="315" src="https://www.youtube.com/embed/IamEow08Zas" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

---

¡Esperamos tus comentarios!