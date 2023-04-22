---
title: "El principio de Inversión de Dependencias"
date: 2023-04-20
author: Héctor Patricio
tags: solid dependency-inversion inversion-dependencias
comments: true
excerpt: "Analicemos el principio de Inversión de Dependencias, el último principio de SOLID y veamos si conviene, además cuándo aplicarlo."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1682052442/milad-fakurian-PGdW_bHDbpI-unsplash_teqmvg.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1682052442/milad-fakurian-PGdW_bHDbpI-unsplash_teqmvg.jpg
  overlay_filter: rgba(0, 0, 0, 0.6)
---

Este es el artículo final sobre el análisis de los principios SOLID. En este artículo veremos el principio de **Inversión de Dependencias**, el cual nos dice que las clases de alto nivel no deben depender de las clases de bajo nivel, sino que ambas deben **depender de abstracciones**.

Veamos qué tan útil es en la vida real, aplicándolo día a día, cuáles son las formas de implementarlo y algunos ejemplos, asó como **algunas críticas**.

## Principio de Inversión de Dependencias

El principio se establece en dos partes:

    A. Los módulos de alto nivel no deberían depender de los módulos de bajo nivel, ambos deben depender de abstracciones.

    B. Las abstracciones no deberían depender de los detalles, los detalles deben depender de las abstracciones.

Esto es el principio de **Sustitución de Liskov**, pero llevado al extremo. Veamos algunos ejemplos en Python.

```python

class Database:
    def connect(self):
        pass

    def disconnect(self):
        pass

    def query(self, sql):
        pass

class MySQLDatabase(Database):
    def connect(self):
        print("Connecting to MySQL")

    def disconnect(self):
        print("Disconnecting from MySQL")

    def query(self, sql):
        print("Querying MySQL")

class PostgreSQLDatabase(Database):
    def connect(self):
        print("Connecting to PostgreSQL")

    def disconnect(self):
        print("Disconnecting from PostgreSQL")

    def query(self, sql):
        print("Querying PostgreSQL")

class DatabaseManager:
    def __init__(self, database):
        self.database = database

    def connect(self):
        self.database.connect()

    def disconnect(self):
        self.database.disconnect()

    def query(self, sql):
        self.database.query(sql)

class Model:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def save(self):
        self.database_manager.query("INSERT INTO ...")

my_model = Model(DatabaseManager(MySQLDatabase()))
```

En este ejemplo vemos claramente como la clase `Model` no depende directamente de una clase concreta de base de datos, sino que depende de una abstracción, la clase `DatabaseManager`. De esta manera el código de "alto nivel", es decir, el modelo, no depende de un código de "bajo nivel", la base de datos.

Aquí **alto nivel**, se refiere a la lógica de negocio, mientras que **bajo nivel** se refiere a la implementaciones de cosas no diferenciadas, como conexiones a base de datos y otras cosas similares.

Esto se ve muy sencillo aquí, justo en un lenguaje de tipado dinámico. Pero en lenguajes de tipado estático, como Java, esto se vuelve un poco más complicado, sobre todo cuando quieres que las clases se puedan cambiar de manera dinámica.

Es por esto que nació la técnica de **Inyección de Dependencias**, la cual consiste en inyectar una dependencia en una clase, en lugar de crearla dentro de la clase (la cuál tiene múltiples formas de aplicación). También se puede usar la **Inversión de Control**, que consiste en que en vez de que sea la clase o el método principal el que instancie alguna dependencia, sea un "contenedor", que normalmente es un framework, el que se encargue de instanciar las dependencias y pasarlas a la clase o método que las necesita. Puedes leer más sobre [DI vs IoC](https://medium.com/ssense-tech/dependency-injection-vs-dependency-inversion-vs-inversion-of-control-lets-set-the-record-straight-5dc818dc32d1).

Finalmente, existe también el descubrimiento de servicios, en el que se "pide" an **Localizador de Servicios** que nos de lo que necesitamos para trabajar. Puedes leer sobre la aplicación de esto aquí, en un artículo de Martin Fowler: [Inversion of Control Containers and the Dependency Injection pattern](https://martinfowler.com/articles/injection.html)

A mi gusto, todo esto es muy complicado. Veamos algunas críticas a este principio.

## Crítica de Dan North

Analicemos la crítica de [Dan North](https://dannorth.net/about/) (un reconocido desarrollador de software, consultor y coach) a este principio, al que no le parecen útiles los principios SOLID, sino que prefiere el código simple:

> While there is nothing fundamentally wrong with DIP, I don’t think it is an overstatement to say that our obsession with dependency inversion has single-handedly caused billions of dollars in irretrievable sunk cost and waste over the last couple of decades. - **Dan North**

En resumen, [Dan North](https://dannorth.net/2021/03/16/cupid-the-back-story/) dice que aunque el principio en sí mismo no tiene nada de malo, el hecho de que nos obsesionemos con la _inversión de dependencias_ ha causado miles de millones de dólares en pérdidas irreversibles.

Veamos otra cita de **Dan North**:

> **Most dependencies don’t need inverting, because most dependencies aren’t options, they are just the way we are going to do it this time.** So my - by now entirely unsurprising - suggestion is to write simple code, by focusing on use rather than reuse.

Esta cita la podemos traducir como:

> La mayoría de las dependencias no necesitan invertirse, porque la mayoría de las dependencias no son opciones, son simplemente la forma en que lo haremos esta vez. Así que mi - en este momento, completamente predecible - sugerencia **es escribir código simple, centrándose en el uso en lugar de en la reutilización**.

Estoy completamente de acuerdo con esta crítica. La mayoría de veces no vas a necesitar reemplazar algo. Es mejor enfocarse en lo que va a suceder 98% de las veces que hacer algo súper complejo o que requiera de una gran cantidad de código en sí mismo como pegamento para que funcione.

Según el que propuso este principio, debería aplicarse siempre. Siempre deberías conectar cosas abstractas con otras cosas abstractas y luego hay algo que "rellena" estas cosas abstractas, o a lo que le puedes pedir que te de una implementación concreta de algo abstracto. **Repito:** a mi gusto es muy complicado y no es necesario en la mayoría de los casos.

Sin embargo, creo que hay casos, sobre todo aquellos en los que tienes concretamente los casos en las que las implementaciones pueden variar, en los que sí es útil. Por ejemplo imagina algo que tenga que conectarse a diferentes API's para proveer el mismo servicio, como por ejemplo, para enviar mensajes de texto a través de múltiples canales. En este caso, sí es útil, porque puedes tener una interfaz que defina el comportamiento de un servicio de mensajería, y luego múltiples implementaciones de esta interfaz, una para cada canal de mensajería, e inyectar las implementaciones de forma dinámica o mediante configuración.

## Conclusión

En este artículo hemos visto el principio de Inversión de Dependencias, el cual nos dice que las clases de alto nivel no deben depender de las clases de bajo nivel, sino que ambas deben depender de abstracciones.

Aunque puede ser útil en ciertos casos, para mi **bastante específicos**, creo que intentar aplicarlo siempre ha creado más problemas que luego hacen código difícil de entender y mantener, agregándole complejidad al código innecesariamente. Es mejor tener interfaces bien diseñadas, que sea fácil entenderlas y mantener en la cabeza.

En general, respecto a los principios SOLID, opino algo muy similar a lo que Dan North menciona: es más importante escribir código simple, que se entienda fácilmente.

