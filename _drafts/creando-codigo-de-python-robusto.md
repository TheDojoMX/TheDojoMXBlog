---
title: "Creando código de Python robusto, Parte 1"
date: 2022-12-23
author: Héctor Patricio
tags: python
toc: true
comments: true
excerpt: "Normalmente no basta con saber lo básico de un lenguaje para hacer código que sea fácil de mantener y seguro. Hablemos de algunas maneras de hacer código robusto con Python."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_fill,g_north,h_350,q_59,w_1200,x_100,y_100/v1661094369/DALL_E_2022-08-12_11.14.36_-_dangerous_green_and_black_python_ready_to_byte_digital_art_bgspv1.png
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_fill,g_north,h_150,q_59,w_300,x_100,y_100/v1661094369/DALL_E_2022-08-12_11.14.36_-_dangerous_green_and_black_python_ready_to_byte_digital_art_bgspv1.png
  overlay_filter: rgba(0, 0, 0, 0.5)
---

En esta serie de posts vamos a hablar de algunas cosas que harán que tu código de Python sea:

- resistente al paso del tiempo
- más fácil de entender, de mantener y cambiar
- que evite errores difíciles de encontrar

En este artículo vamos a empezar a hablar de cómo hacer código que sea resistente al paso del tiempo.

## El tiempo y los cambios

En realidad el puro paso del tiempo no le hace nada a ninguna cosa. A lo que nos referimos con esta expresión es que las cosas **cambian** con el tiempo. Estos cambios pueden afectar a partes de tu código aunque estas en sí misma no sufran ninguna modificación. Veamos cómo puedes protegerte con algunos tips específicamente para Python.

### Serialización

En algunos casos, es necesario guardar información que es resultado de la operación de un programa, sea como un paso intermedio para poder recuperar el cálculo en caso de fallo (como un punto de revisión) o para que otros procesos lo tomen.

Sobre todo en procesos que llevan una gran cantidad de cálculo, algunos programadores están acostumbrados a usar el módulo `pickle` de Python para guardar información en un archivo. Este módulo es muy útil para guardar _objetos_ de Python en un archivo, pero presenta algunas características inconvenientes:

- Es inseguro, ya que permite ejecutar código arbitrario al cargar un archivo (hay que truquearlo, pero es posible).
- Es **inestable**, ya que permitirá crear una versión de un objeto que no sea compatible con la versión actual del código.

Aunque la seguridad es muy importante, el punto que queremos tratar ahorita es la inestabilidad. Por ejemplo, si alguna clase de tu código evoluciona, agregando nuevos atributos, el archivo que guardaste y que ahora puedes cargar, creará una versión del objeto sin las características y las guardas que le hayas puesto a la nueva versión. Esto va a causar problemas no detectables hasta que el código que carga el archivo se ejecute.

### Alternativas a Pickle

Siempre que quieras serializar parte de un programa, enfócate en los **datos**. No en las clases o los objetos. Así, para guardar datos puedes usar cualquier otro formato de serialización que no se meta con el código directo de Python. Algunas opciones son:

- [JSON](https://barcelonageeks.com/serializar-y-deserializar-json-complejo-en-python/): usa el paquete `json` para exportar y cargar los datos resultado de las computaciones. Tendrás que convertir tus objetos a diccionarios y listas, pero esto es fácil de hacer y no te afectará cuando cambies tu código.

- [Protocol Buffers](https://blog.conan.io/2019/03/06/Serializing-your-data-with-Protobuf.html): es un formato binario definido por Google para acelarar la comunicación entre diferentes servicios. Es más complicado que usar JSON, pero más eficiente si tienes muchos datos.

- [MessagePack](https://msgpack.org/index.html): usa el paquete `msgpack` para serializar datos en un formato binario. Es más rápido y también más pequeño que JSON, aunque no es tan fácil de leer.

## Trabajando con fechas

Otra razón por la que tu código puede dar problemas con el paso del tiempo es por un trato incorrecto de las fechas y horas. Cuando una aplicación tiene que recibir datos de horas o fechas de usuarios de diferentes partes del mundo (casi todas las aplicaciones web), es importante asegurarnos de que entendemos bien lo que nos quieren decir y de comunicarnos correctamente con ellos.

Las zonas horarias son un gran dolor de cabeza para los desarrolladores, pero espero que podamos escribir un artículo más amplio sobre eso en el futuro. Por ahora, vamos a hablar de cómo trabajar con fechas y horas en Python.

Si no sabes nada de las zonas horarias te recomiendo leer esto: [Fundamentos de la zona horaria](https://learn.microsoft.com/es-es/dotnet/standard/datetime/time-zone-overview#time-zone-essentials)

### Fechas ingenuas vs fechas conscientes de la zona horaria

Esta traducción la siento un poco forzada pero en inglés son _naive_ y _timezone aware_. (¿Alguien tiene una mejor idea?)

En Python, las fechas y horas se representan con objetos de la clase `datetime`. Esta clase tiene dos subclases: `datetime.datetime` y `datetime.date`. Cuando la usas así, directamente sin especificar una zona horaria, estás usando una fecha ingenua. Por ejemplo:

```python
from datetime import datetime

fecha = datetime.now() # Esta fecha no incluye ninguna información sobre la zona horaria

```

Aunque esto funciona bien para programas que sólo van a correr en tu computadora y que _siempre_ van a correr nadamás para ti, no es suficiente cuando esta información va a ser compartida o se tiene que guardar para el uso futuro.

La forma de usar una fecha consciente de la zona horaria en Python es:

```python
from datetime import datetime, timezone


fecha = datetime.now(tz=timezone.utc) # Esta fecha incluye información sobre la zona horaria, en este caso UTC

```

De esta manera nos protegemos para no dar por sentado en qué zona horaria se creo cierto dato o a que zona horaria se refiere cierta fecha. A partir de Python 3.9 tenemos disponible un paquete que se llama `zoneinfo` que nos permite trabajar con zonas horarias sin tener que instalar nada extra (excepto en Windows donde es probable que necesites los datos de [tzdata](https://pypi.org/project/tzdata/)). Si estás usando Python 3.8 o anterior, puedes instalar el paquete `pytz` para poder usar zonas horarias o importar desde `backports.zoneinfo` (también se tiene que instalar). Aquí hay un ejemplo:

```python
from datetime import datetime
from zoneinfo import ZoneInfo

fecha = datetime.now(tz=ZoneInfo("America/Mexico_City")) # Esta fecha incluye información sobre la zona horaria, en este caso la de México
# datetime.datetime(2022, 12, 24, 20, 2, 21, 887237, tzinfo=zoneinfo.ZoneInfo(key='America/Mexico_City'))

```

Así puedes crear siempre fechas con zonas horarias para que no tengas problemas a la hora de reutilizarla. Ahora hablemos de por qué es recomendable siempre usar la zona horaria UTC.

### El tiempo universal coordinado (UTC)

**UTC** son las siglas para **Universal Time Coordinated** o el **Tiempo Universal Coordinado**. Este es un estándar para determinar la hora universal. Incluye todos los detalles de cómo obtener el tiempo, la coordinación, cómo tratar los segundos faltantes en el calendario gregoriano, etc. etc. etc. Coordinar el tiempo es un asunto muy complejo.

UTC, a diferencia de lo que creemos los programadores **no es una zona horaria**, aunque nosotros lo usemos así. Antes se conocía como **GMT** (Greenwich Mean Time), pero otros de sus alias son "Z time" o "Zulu time". Puedes leer el estándar, las motivaciones y la historia en este documento de la (BIPM)[]: [Coordinated Universal Time](https://www.bipm.org/documents/20126/28435864/working-document-ID-3644/2a6ce17c-7b50-4164-9bee-64f77bfad895).

Aunque **UTC** es el estándar, **GMT** pasó a ser el nombre de la zona horaria que no tiene diferencia con el UTC. Ahora ya sabes entonces que lo que los programadores llamamos "UTC" es en realidad la zona horaria "GMT".

¿A qué viene todo esto? Es recomendado que siempre que tengas que guardar fechas y horas antes las conviertas en fechas conscientes de la zona en  UTC.
