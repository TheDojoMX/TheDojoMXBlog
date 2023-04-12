---
title: "Composición en el software"
date: 2023-04-07
author: Héctor Patricio
tags:
comments: true
excerpt: "La composición es algo muy mencionado en la programación funcional, vamos a ver cómo se aplica al desarrollo de software también fuera de ella."
header:
  overlay_image: #image
  teaser: #image
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Composición:

> Es la acción de combinar componentes individuales para formar un todo más complejo.

Componer es la técnica más efectiva para construir software de manera organizada. La composición nos permite crear software complejo porque nos permite construir piezas pequeñas que resuelven problemas manejables y luego "juntarlas" para entregar la solución de nuestro problema.

Veamos algunas formas de hacer composición en el software y por qué es más efectivo que otras formas de reutilizar código.

## ¿Por que es importante aprender a usar la composición?

> Nuestra habilidad para descomponer un problema en partes, depende
directamente de nuestra habilidad para combinar soluciones. - **John Hughes**

John Hughes es un gran proponente e investigador de la programación funcional en la actualidad. Él propone que la composición es importante porque nos da la confianza de poder romper nuestros problemas en problemas más pequeños, sabiendo que después podremos juntarlos de manera efectiva para entregar una solución al problema original.

> Divide y vencerás

Una ventaja secundaria de dividir el software en piezas pequeñas, es que si diseñamos correctamente nuestros componentes y tenemos las herramientas adecuadas para unirlas después, podemos **reutilizar** las piezas que ya hemos construido en otras partes.

Veamos dos formas de aplicar la composición en el software.

## Composición de funciones

Las funciones son la unidad de abstracción más pequeña que tenemos en la programación. Crear un montón de pequeñas funciones útiles que resuelvan problemas generales, de manera completa y precisa, es muy buena idea.

¿Cómo aplicamos la composición? Puedes usar la composición al dividir tu problema principal en funciones sencillas y luego juntarlas.Veamos un ejemplo: vamos a crear un validador de passwords. El validador debe verificar las siguientes condiciones:

- Verificar una longitud mínima, que podría ser 8 caracteres.
- Checar que no tenga ciertas palabras (lista negra).
- Verificar que tiene un número
- Verificar que tiene un carácter especial

Podríamos hacer esto en una sola función que verificara todas estas características, una por una a través de un serie de if's. Pero veamos una implementación usando composición, y sus ventajas.

```python

def min_length(password, min_length):
    return len(password) >= min_length

def has_number(password):
    return any(char.isdigit() for char in password)

def has_special_char(password):
    return any(char in "!@#$%^&*()_+" for char in password)

def not_in_blacklist(password, blacklist=[]):
    if not blacklist:
      blacklist = ['password', '12345678']
    return not any(word in password for word in blacklist)

def validate_password(password, min_length, blacklist):
    return min_length(password, min_length) and \
           has_number(password) and \
           has_special_char(password) and \
           not_in_blacklist(password, blacklist)
```

Quiero que te fijes especialmente en la última función, `validate_password`. Aunque funciona, es un poco rígida. La composición puede ayudarnos a hacerla más flexible.

```python
validators = [
    lambda password: min_length(password, 8),
    has_number,
    has_special_char,
    lambda password: not_in_blacklist(password, ['palabra_uno', 'palabra_dos'])

]
def validate_password(password, min_length, blacklist, validators):
    return all(validator(password) for validator in validators)
```

## Composición de objetos

### ¿Por qué es más efectiva la composición de objetos que la herencia?

## ¿Cuál es el pegamento que te da tu lenguaje?

## Conclusión

Aprender a usar la composición es **obligatorio para desarrollar buen software**. Lo quieras o no, mientras desarrollas, siempre estás juntando componentes, es decir _componiendo_, si conoces las técnicas correctas, podrás crear software de mejor calidad de manera más rápida.
