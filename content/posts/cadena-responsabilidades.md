---
title: "Patrón de diseño: Cadena de responsabilidad"
date: 2019-02-10
author: "Esteban Galicia"
tags: ['python', 'patrones', 'SOLID', 'Chain-of-Responsibility', 'design-patterns']
description: "Manejar múltiples handlers, conocidos y no conocidos."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_800/v1550949447/mike-alonzo-3347-unsplash_cwqcud.jpg"
draft: false
---

#### Propósito

 > Asegurar el bajo acoplamiento entre un _request_ y su _receiver_ dando a múltiples objetos oportunidad de manejar el _request_

Hace unas semanas me enfrenté a un tema de procesar un mensaje de un usuario y darle tratamiento por medio de un algoritmo de Natrual Language Processing. Antes de pasar el mensaje por el set de algoritmos apropiados hay que darle una serie de tratamientos previos:

 1. Eliminar los acentos y solo dejar en ASCII el mensaje.
 2. Pasar el mensaje a lowercase.

A primera luz, un código que puede fácilmente satisfacer es:

```python

message = "Dios bendiga a los héroes que nos dieron el internet."
message = message.lower()
message = message.replace("á","a").replace("é","e") \
    .replace("í","i").replace("ó","o").replace("ú","u")
print(message)
# dios bendiga a los heroes que nos dieron el internet.
```
Funcionó, se cumplió el objetivo.

El problema sobrevino en el momento que los algoritmos posteriores requieren más modificaciones en la cadena original.
Poco a poco se fue agregando y agregando código para tareas como eliminar emojis, eliminar signos de puntuación, contraer palabras como *hooooooola* en *hola* y en el futuro no se sabe que más cosas habrá que hacer a la cadena original, pueden ser cosas tan diversas como "A cada cadena que se procese quiero que se quede un historial de la cadena original", en ese momento hay que ir a reescribir código quebrantando el principio [****open/closed****](https://en.wikipedia.org/wiki/Open–closed_principle) "_software entities (classes, modules, functions, etc.) should be open for extension, but closed for modification_".

#### Solución

El patrón de diseño *Chain of responsibility* como premisa principal es que más de una entidad de software (clase y/o función) pueda atender una petición. Dichas entidades pueden ser conocidas y de hecho se acaban implementando, pero también pueden ser desconocidas y esas no las podemos implementar pero debemos ser capaces de implementarlas en un futuro.

Pero, si el código anterior es muy sencillo, no veo caso de hacerlo _complejo_; a medida que los requerimientos van cambiando en el tiempo es muy probable que ese código se acabe agrupando en una función y esa función no hará más que crecer y entre más lo haga perderá el foco y se convertirá en una función que hará de todo, no cumplirá con otro principio ([single responsibility](https://refactoring.guru/images/patterns/content/chain-of-responsibility/chain-of-responsibility.png)) _una entidad debe hacer solo una cosa y hacerla bien_, la función además de escribir en disco tiene que pasar la frase a minúsculas, reemplazar caracteres no ASCII con caracteres ASCII por mencionar algo. El partir una gran función (gran ~= muchas responsabilidades) en muchas más pequeñas facilita la escritura de test unitarios y propicia a la re usabilidad de esa función en distintas partes de nuestro proyecto principalmente.


En este patrón la petición (_request_) es mandada de entidad en entidad (cada entidad es un eslabón de la cadena o _handler_), cada entidad maneja la petición y la pasa al siguiente eslabón hasta que se terminen los eslabones de la cadena o uno de ellos decida que hay que regresar un valor.

![Representación gráfica](/assets/images/chain-of-responsibility.jpg)

Siguiendo con el problema original, el código propuesto es el siguiente [(aquí uno en Java)](https://www.tutorialspoint.com/design_pattern/chain_of_responsibility_pattern.htm):

```python
def to_lower(message=""):
    if not isinstance(message,str):
        raise ValueError("Message is not a string")
    return message.strip().lower()

def to_ascii(message):
    if not isinstance(message,str):
        raise ValueError("Message is not a string")
    message = message.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    return message

def to_disk(message):
    FILENAME = "historial.log"
    if not isinstance(message,str):
        raise ValueError("Message is not a string")
    with open(FILENAME,"a",encoding="UTF-8") as fp:
        fp.write(f"{message}\n")
    return message

def remove_all_punctuation(message):
    #all code to remove punctuation marks
    return message

class Pipe:
    def __init__(self,message):
        self._message = message
        self.processors = []

    def add_process(self,process_function):
        self.processors.append(process_function)

    def run(self):
        for process in self.processors:
            self._message = process(self._message)
        return self._message

pipe=Pipe("Dios bendiga a los héroes que nos dieron el internet.")
pipe.add_process(to_disk)
pipe.add_process(to_lower)
pipe.add_process(to_ascii)
pipe.add_process(remove_all_punctuation)
new_message=pipe.run()
print(new_message)

```

El código anterior es un código más profesional, más fácil de mantener ya que cumplimos con el principio _open/closed_ y de paso de responsabilidad única.

Podemos ir agregando funciones de procesamiento de manera más legible, también podemos quitarlas a voluntad dado que el nivel de acoplamiento es muy bajo. A todo ésto hay que añadir la ventaja de facilidad al escribir test unitarios que dan pie para el CI/CD.

Se puede pensar al inicio que es una sobre-ingeniería para algo tan sencillo, pero los negocios son tan cambiantes en el tiempo que se vuelve un poco ingenuo pensar que lo que escribamos nunca lo tendremos que modificar, ¿Por qué no diseñar software que pueda ser modificable en el ahora y el futuro?. Este tema de los patrones de diseño es un tema muy extenso que poco a poco iremos cubriendo con entradas en este blog dando ejemplos sencillos como el anterior.

Lo importante es quedarse con el concepto de qué es lo que hace el patrón y no con la implementación como tal del código, en Java el código anterior puede ser muy diferente, sin embargo cumple el patrón. Tuve conciencia de esto leyendo que en un principio, en los años dorados de C, este patrón se implementaba con listas enlazadas,a su vez implementadas con apuntadores.

Saludos y no dudes en ejercer tu derecho de réplica :) , discutamos un poco al respecto :D.
