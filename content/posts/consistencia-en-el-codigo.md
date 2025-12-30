---
title: "Consistencia en el código"
date: 2022-06-02
author: "Héctor Patricio"
tags: ['consistencia', 'base-de-código', 'posd']
description: "La consistencia y uniformidad en una base de código son muy importantes, en este artículo veremos cómo podemos lograrlo y en qué cosas debes poner atención."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1280/v1654205989/joshua-dow-E17e1LZV0dg-unsplash_toh95b.jpg"
draft: false
---

Una de las mejores formas de ayudar a que tu código sea fácil de mantener es hacer que el estilo tanto de formateo como de programación en general sea consistente. Analicemos este concepto que se menciona en "A Philosophy of Software Design".

## ¿Qué es la consistencia en el código?

Básicamente, significa que las que cosas o el código que hace lo mismo luzca y se programen igual y las piezas de código que no hacen los mismo, luzcan y se programen diferente.

Hay varios factores a tomar en cuenta respecto a la consistencia del código, que trataremos en las siguientes sub-secciones.

### Nombres

Para empezar, los nombres deben ser consistentes, tanto en estilo como en semántica. Es decir, si decidiste usar **camelCase**, debes buscar usarlo en todos lados. Muchos guías de estilo y linters incluso lo sugieren un estilo, o es común tener una costumbre dependiendo del lenguaje (por ejemplo en JS y Java se acostumbra mucho el **camelCase**, mientras que en Python se recomienda usar **snake_case**).

El segundo punto, la semántica tiene que ver con que siempre te refieras a la misma idea con el mismo nombre, por ejemplo, si estás modelando algo que tiene que ver con boletos para un evento, es buena idea nombrar a las variables siempre de la misma forma, como `ticket`, en vez de nombrarlas `ticket`, `bill`, `entrance_ticket`, etc.

Si decides usar nombres como `i`, `j` o `n` para numerar cosas o en bloques, asegúrate de que tengan la misma semántica en todos lados, por ejemplo, usa `i` para el primer índice en un ciclo, y `j` para un índice interno.

Tener un sistema de nombrado consistente hará que la **carga cognitiva** que requiere programar en tu base de código disminuya.

### Interfaces

Crear una interfaz (o una clase abstracta, o una estructura, o un protocolo) o cualquier cosa que sirva para definir un _contrato_ para un conjunto de módulos que hagan cosas similares, permitirá que tú código sea más fácil y rápido de entender. Basta con entender una sola de las implementaciones para comprender todas las demás.

El ejemplo perfecto son los métodos de pago en un sistema de eCommerce. En vez de inventar cada vez un una nueva interfaz, puedes definir que la interfaz común sea algo como:

```python

class PaymentMethod:
    """
    Defines the interface for all payment methods
    """
    def charge(self, amount):
        pass
    def refund(self, amount):
        pass
    def void(self):
        pass

```

Si tu lenguaje no tiene, puedes documentar y dejar claro para tu equipo cómo deben cumplirse las interfaces y contratos entre los diferentes módulos.

### Patrones de diseño y principios de programación

Muchas soluciones comunes a problemas comunes que encontramos en el desarrollo se han definido claramente y nombrado, para poder ser usadas y entendidas como una receta por muchos programadores.

A estas soluciones las llamamos **patrones de diseño** y la familiaridad con ellos, pueden hacer que tú base de código se más fácil de mantener. Usarlos cuando es adecuado, puede ayudarte a darle consistencia a tu código, lo mismo que otro principios de programación, como por ejemplo, inversión de dependencias.

Sólo debes tener en cuenta que para que tu equipo se beneficie de esto, debe _conocer_ estas soluciones, ya que ese es uno de los principales objetivos de los patrones: que los programadores tengan un lenguaje común de soluciones que los ayuden a comunicarse más fácil.

## Invariantes

Una **condición que siempre se cumple** en tu programa es una invariante. Por ejemplo, muchos los lenguajes funcionales te aseguran que todo es una expresión, por lo que siempre puedes usar cualquier construcción del lenguaje como algo que te devuelve un valor.

Establecer invariantes en tu base de código y estilo de programación, ayudará a que el código sea consistente. Por ejemplo, en JQuery se creo la invariante de que todas las funciones que usan un elemento, devuelven este mismo elemento, por lo que puedes encadenar llamadas y siempre funcionará.

Piensa en cosas que puedas hacer invariantes y ayudarás a que tu código sea más consistente.

## Asegura la consistencia en el código

Hay varias formas de asegurar que tu equipo cree código consistente, no son excluyentes, sino que se ayudan unas a otras.

La primera forma, y la más fuerte, es mediante el aseguramiento automático del cumplimiento de las reglas que pueden ser representadas en alguna herramienta. Por ejemplo, los **linters**, verificadores de complejidad del código, combinados con las herramientas dadas por los sistemas de versionamiento  de código (ver [git hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)).

Este conjunto de herramientas podría verificar y obligar que se cumplan las reglas de formateo de código y otras medidas de calidad.

Otra herramienta es la **documentación**, y yo diría que es la más importante porque es en la que se define todas las cosas que deberían ser uniformes y trasciende a las personas, estructuras de equipo y herramientas. Es muy importante que (de preferencia) al iniciar el proyecto crees una guía de estilo y sugerencias de uniformidad que ayuden a tu equipo a crear código uniforme. Como te imaginarás, esto es trabajo extra, pero vale la pena.

Finalmente _tienes_ que promover la consistencia con tu ejemplo y mediante las revisiones de código, si las tienes. Cuando escribas código nuevo, busca la guía de estilo y las convenciones. Si no son explícitas, observa el código para que veas lo que puedes extraer como convención.

## Mantén la consistencia

Es muy fácil querer cambiar algo porque encontramos una forma diferente de hacer las cosas que preferimos por gusto o porque es un poquito mejor. En estos casos, tienes que pensar muy bien si vale la pena romper la consistencia de tu base de código por una mejora.

Como en muchas ocasiones en el código, esto implica un intercambio de valor y como responsable de esta decisión, tienes que evaluar los pros y los contras. Piensa: ¿me va a dar tanta ventaja como para que valga la pena meter esta complejidad extra? ¿vale tanto la pena para que haga replique este cambio en todo los otros lugares en los qu se hace esto?

## Conclusión

Mantener la consistencia, en la base de código es algo que vale la pena para reducir el esfuerzo cognitivo que a los desarrolladores les cuesta trabajar en tu código. Esto ayudará a que tu código sea mantenible y sea más probable que tenga una larga vida.
