---
title: "Composición en el software"
date: 2023-04-17
author: Héctor Patricio
tags: fp composición
comments: true
excerpt: "La composición es algo muy mencionado en la programación funcional, vamos a ver cómo se aplica al desarrollo de software también fuera de ella."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1679150874/sam-moghadam-khamseh-VwHzE0aFQfY-unsplash_lpqwqn.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1679150874/sam-moghadam-khamseh-VwHzE0aFQfY-unsplash_lpqwqn.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Composición:

> Es la acción de combinar componentes individuales para formar un sistema más complejo.

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

Las funciones son la unidad de abstracción más pequeña que tenemos en la programación. Crear pequeñas funciones útiles que resuelvan problemas generales, de manera **completa y precisa**, es muy buena idea.

¿Cómo aplicamos la composición? Puedes usar la composición al dividir tu problema principal en funciones sencillas y luego juntarlas.Veamos un ejemplo: vamos a crear un validador de contraseñas. Este debe verificar las siguientes condiciones:

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
def validate_password(password, min_length=8, blacklist=['b1', 'b2']):
    validators = [
        lambda password: min_length(password, 8),
        has_number,
        has_special_char,
        lambda password: not_in_blacklist(password, ['palabra_uno', 'palabra_dos'])
    ]
    return all(validator(password) for validator in validators)
```

Esta función es más flexible, pudiendo agregar o quitar validadores sin tener que modificar más código, simplemente modificando la lista de validadores, pero todavía no es como la queremos. ¿Qué pasas si queremos agregar el conjunto de errores por los que falla una validación? Tenemos que ir **acumulando**:

```python

def validate_password(password, min_length=8, blacklist=['b1', 'b2']):
    """Devuelve la lista de errores de la contraseña, si está vacía, la contraseña es válida"""
    validators = [
        {"validator": lambda password: min_length(password, 8), "mesage": "La contraseña es muy corta"},
        {"validator": has_number, "message": "La contraseña no tiene un número"},
        {"validator": has_special_char, "message": "La contraseña no tiene un carácter especial"},
        {"validator": lambda password: not_in_blacklist(password, ['palabra_uno', 'palabra_dos']), "message": "La contraseña tiene palabras prohibidas"}
    ]
    errors = []

    reduce(lambda errors, validator: errors.append(validator["message"]) if not validator["validator"](password) else errors, validators, errors)

    return errors

```

Aquí `reduce` que recibe una función, una lista de elementos por las que iterar y un valor inicial, nos ayuda a acumular los errores. Si quisiéramos hacerlo aún más flexible, podríamos hacer dos cosas:

- Hacer que la función `validate_password` reciba una lista de validadores (junto con el mensaje), en vez de tenerlos definidos dentro de la función
- Definir una clase `Validator` que tenga un método `validate` y un atributo `message` y que reciba una función y un mensaje en su constructor, para tener una interfaz más clara.

### Composición matemática

Este tipo de composición fue un poco más empírica, simplemente juntando funciones. A veces, cuando oigas de composición, se van a referir a la composición de funciones en sentido matemático. Veamos un ejemplo en Python:

```python
from string import ascii_letters

LETTERS = set(ascii_letters)

def quitar_no_ascii(texto):
    return ''.join([char for char in texto if char in LETTERS])

def reemplazar_acentos(texto):
    accents = {
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ó': 'o',
        'ú': 'u',
        'ñ': 'n'
    }
    return ''.join([accents.get(char, char) for char in texto])

def limpiar_cadena(texto):
    return quitar_no_ascii(reemplazar_acentos(texto))

```

El código anterior deja una cadena solamente con letras ASCII, sin acentos. Lo que ves en la función `limpiar_cadena` es una composición de funciones, en el sentido matemático, aplicar una función después de otra, o la salida de una como argumento de la otra.

Siempre que pienses en un proceso que lleve una cadena de pasos, lo puedes representar como una cadena de funciones. En lenguajes funcionales hay operadores para hacer esto.

Puedes pensar en este tipo de composición como en hacer **fluir** la información por un conjunto de funciones. Ejemplos en lenguajes como Haskell, Clojure y Elixir te pueden ayudar a expandir sobre esto, puedes buscarlo como "composición funcional".

## Composición de objetos

Otra técnica que te puede ayudar a crear mejor software es la composición de objetos. Esta se entiende como formar objetos más complejos a partir de objetos más simples. Aunque la **herencia** es una forma de composición, al hacer completamente dependientes una clase de otra, no es la mejor forma de crear objetos complejos. De hecho, hay grandes dudas sobre si la herencia es una buena idea. Pero no estamos aquí para discutir sobre las ventajas y desventajas de la herencia, sino para aprender a usar otros tipos de composición.

Una forma de crear objetos complejos, en vez de tener la relación "es un" que nos da la herencia, es tener la relación "tiene un". No estamos diciendo que la herencia nunca se deba usar, pero en muchas ocasiones podemos pensar en la composición como una alternativa mejor.

Observa el siguiente ejemplo, en el que representamos la información de un usuario y su relación con al entidad Empleado:

```python

class Usuario:
    def __init__(self, nombre, apellido, email, password):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email

class Empleado:
    def __init__(self, usuario, puesto, salario):
        self.info_usuario = usuario
        self.puesto = puesto
        self.salario = salario
```

Esta implementación está menos acoplada o es menos dependiente que la implementación basada en herencia. Por ejemplo, si queremos evolucionar la clase `Usuario`, no tenemos que hacer que nada de esto afecte directamente a la clase `Empleado`.

Otra forma de usar la composición es la **delegación**, a la que le dedicaremos más tiempo en un futuro. Esta te la puedes imaginar como que un objeto le deja todo el trabajo a otro a través, por ejemplo, de un método. Esto es más común en lenguajes no basados en clases, ya que se da de manera más natural, como en JavaScript, donde puedes usar `Object.assign` para copiar las propiedades de un objeto a otro.

## Conclusión

Aprender a usar la composición es **obligatorio para desarrollar buen software**. Lo quieras o no, mientras desarrollas, siempre estás juntando componentes, es decir _componiendo_, si conoces las técnicas correctas, podrás crear software de mejor calidad de manera más rápida.

Piensa en el desarrollo de software como el arte de deconstruir los problemas, resolverlos por cachitos y después juntar las soluciones de regreso para tener la solución completa.