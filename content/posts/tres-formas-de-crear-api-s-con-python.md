---
title: "Tres formas de crear API's con Python"
date: 2019-03-12
author: "Héctor Patricio"
tags: ['api', 'python', 'hug', 'django-rest-framework', 'flask']
description: "¿Vas a hacer una API? Aprende la mejor forma de hacer desde la más sencilla hasta la más completa."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1552198393/brian-patrick-tagalog-704059-unsplash_z3kdwg.jpg"
draft: false
---

Es una tarea común para un desarrollador el diseñar e implementar una API web. Veremos tres herramientas para desarrollar tu API, de lo más sencillo a lo más completo: Hug, Flask y Django Rest Framework.

## Hug

[Hug](http://www.hug.rest/) es una pequeña biblioteca para crear API's muy fáciles de entender y mantener.
Provee un serie de herramientas que permiten hacer tu API muy rápidamente, con poco código
y siguiendo las mejores prácticas. Hug no es una biblioteca exclusiva para hacer API's web, sino que se enfoca
en permitirte crear API's en el más amplio sentido de la palabra: una intefaz para permitir el uso automatizado (mediante código) de tu programa.

Si haces una API en Hug, podrás exponerla a parte de en web como un módulo de Python o a la interfaz de línea de comandos.

Con hug, puedes hacer algo tan sencillo como lo siguiente:

```python
import hug

@hug.get()
def hola_apis():
  return {"mensaje": "Hola API's"}
```

¡Y listo! Lo anterior es una API lista para ser consumida, no necesitas crear ni configuración ni caberceras ni nada más (aunque claro que las puedes poner).

Hug provee de cosas interesantes:

* Documentación automática
* Verificación y validación de parámetros -> usando el type hinting de Python 3
* Versionamiento de API's (una de las cosas más difíciles de hacer bien en el ciclo de vida de una API)
* Múltiples tipos de salida con sólo cambiar la configuración
* Extensibilidad y flexibilidad

Hug es compatible con WSGI (Web Server Gateway Interface) por lo que puedes ponerlo en producción usando Gunicorn o uWSGI detrás de un servidor HTTP como proxy reverso (NGINX o Apache, entre otros).

Aquí tienes un post introcutorio a Hug:

* [Crear APIs REST con Python y Hug](http://laesporadelhongo.com/crear-apis-rest-con-python-y-hug/)

**Cuándo usarlo:** No he usado Hug en producción aún, pero promete ser muy bueno, sobre todo con las exigencias del mundo actual. Lo recomendaría para proyectos pequeños y medianos y para exponer bibliotecas o módulos que ya existen en alguna parte de código como versiones Web o CLI.



## Flask

[Flask](http://flask.pocoo.org/) es una herramienta flexible para programar proyectos web en Python. Provee una capa mínima de ruteo y compatibilidad con WSGI, así como funcionalidades y helpers comunes para las tarea más comunes en desarrollo web.

Entre las características de Flask están:

* Integración por default con [Jinja2](http://jinja.pocoo.org/docs/2.10/)
* Soporte de cookies de sesión seguras
* Servidor web para desarrollo y debuggeo

Personalmente, considero Flask como la opción más flexible para desarrollar proyectos web en Python. Además permite empezar fácil. Y comparándolo con otras opciones, es mucho más ligero, permitiéndote integrar tus propias opciones para diferentes partes del proyecto. Si tu proyecto es muy poco común o muy especializado, Flask es la mejor opción.

Aquí un pequeño ejemplo de cómo se empiza con Flask (sacado de su documentación en su mayoría)

```python
from flask import Flask, jsonify
app = Flask(__name__)
@app.route("/")
def hello():
    return jsonify({"message": "Hello World!"})
```

Así es: puedes empezar con un solo archivo, Flask hizo todo por ti.

Flask también tiene bastantes módulos que te ayudan a desarrollar funcionalidades más rápido y con poco código.

Si quieres aprender más aquí tienes algunos recursos:

* [Creando una API y aplicación web con Flask](https://blog.nearsoftjobs.com/crear-un-api-y-una-aplicaci%C3%B3n-web-con-flask-6a76b8bf5383)

* [Diseñando APIs con Flask](https://www.youtube.com/watch?v=lYeAvnHcZy8)

* [Construir una API rest con Flask](http://nightdeveloper.net/construir-flask-python/)

Más adelante tendremos nuestro propio post 😉.

**Cuándo usarlo:** Personalmente lo uso para proyectos pequeños o medianos que sé que no crecerán demasiado en características en el mediano plazo. Si tienes que hacer cosas complicadas, Flask requiere bastante experiencia técnia y de arquitectura para que no se te vaya de las manos el proyecto, **su flexibilidad puede trabajar en tu contra en estos casos**.


## Django y Django Rest Framework

Django es un framework MVT (Model-View-Template, su propia variante del MVC) para desarrollar proyectos web robustos de manera rápida.

Django provee:

* Un sistema de templating propio
* Un ORM (Object Relational Mapper – una capa de abstracción de la base de datos)
* Ruteo robusto
* Sistema de configuración robusto y adaptable
* Interfaz de administración automática
* Administración de usuarios

...y muchas otras cosas más. Como verás es mucho más robusto(viene por default con más cosas) que los otros dos, pero también es el que tiene la mayor curva de aprendizaje. Si encuentras algo para lo que no esté preparado Django o DRF éste es el caso en el que se requiere más experiencia técnica para modificarlo.

Django posee muchísimos paquetes para extenderlo en funciones y uno de los más famosos es el Django REST Framework (DRF a partir de ahora), que provee todas las funcionalidades que te imagines para desarrollar una API de manera sencilla y con pocas líneas de código.

El DRF permite crear endpoints a partir de modelos, relaciones entre modelos, endpoints customizados basados en clases y un montón de cosas más. Se enfoca en crear API's navegables.

Además nos da una interfaz para para pruebas desde el navegador web con todas las facilidades del mundo.

Puedes pensar en Django y DRF como una navaja suiza con todo lo que necesitas para desarrollar una API un poco más compleja de manera rápida.

No pondremos el ejemplo de código aquí, porque en este caso el código se reparte entre varios archivos, pero te compartimos los siguientes recursos por si quieres irte por este camino y sients que es lo que necesitas:

* [¿Qué es Django?](https://tutorial.djangogirls.org/es/django/) - ESte es uno de los mejores tutoriales de Django en internet, muy completo, así que vale la pena que lo sigas si quieres aprenderlo.

* [Introducción a Django REST Framework](https://www.paradigmadigital.com/dev/introduccion-django-rest-framework/) - Este post lo puedes seguir una vez que tengas una comprensión básica de Django.

**Cuándo usarlo:** Django es mi elección para proyectos que se que pueden requerir caracterísitcas enterprise, pueden crecer en funcionalidades en el mediano plazo y estas funcionalidades no están demasiado fuera de lo común. Si quieres desarrollar algo rápidamente en estas condiciones, no hay nada que pensar: usa Django, con él (después de la curva de aprendizaje), estarás haciendo cosas medianamente complejas en muy poco tiempo, además de que su inmensa cantidad de módulos para hacer muchísimas cosas sin tanto trabajo te facilitará la vida.


## Conclusión

Algo que hay que tener en mente siempre es que se debe de elegir la herramienta adecuada para el trabajo a la mano. En los tres casos de las herramientas propuestas anteriormente tienes que analizar muy bien tus necesidades antes de decidirte por una, pero incluso podrías usar una para una etapa del proyecto y cambiarla en una fase posterior.

Esperamos que esta pequeña guía acerca de las opciones para elegir la mejor herramienta para crear tu API con flask te sea útil, y si tienes alguna opinión/experiencia diferente es bienvenida en los comentarios.
