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

> A. Los módulos de alto nivel no deberían depender de los módulos de bajo nivel, ambos deben depender de abstracciones.
> B. Las abstracciones no deberían depender de los detalles, los detalles deben depender de las abstracciones.

Esto es el principio de Sustitución de Liskov, pero llevado al extremo. Veamos algunos ejemplos en Python.

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
...........

## Crítica de Dan North

> While there is nothing fundamentally wrong with DIP, I don’t think it is an overstatement to say that our obsession with dependency inversion has single-handedly caused billions of dollars in irretrievable sunk cost and waste over the last couple of decades. - **Dan North**

En resumen, [Dan North](https://dannorth.net/2021/03/16/cupid-the-back-story/) dice que aunque el principio en sí mismo no tiene nada de malo, el hecho de que nos obsesionemos con la _inversión de dependencias_ ha causado miles de millones de dólares en pérdidas irreversibles.

The real principle here is option inversion. A dependency is only interesting when there might be multiple ways of providing it, and you only need to invert the relationship when you believe the wiring is important enough to become a separate concern. That’s quite a high bar, and mostly all you ever need is a main method.

> The promise of “you can just swap out the database” evaporates as soon as you try to, well, swap out the database.

Veamos otra cita de Dan North:

> **Most dependencies don’t need inverting, because most dependencies aren’t options, they are just the way we are going to do it this time.** So my - by now entirely unsurprising - suggestion is to write simple code, by focusing on use rather than reuse.

## Conclusión

En este artículo hemos visto el principio de Inversión de Dependencias, el cual nos dice que las clases de alto nivel no deben depender de las clases de bajo nivel, sino que ambas deben depender de abstracciones.
