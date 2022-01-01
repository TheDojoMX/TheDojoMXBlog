---
title: "Criptografía para desarrolladores: Códigos de autenticación de mensajes"
date: 2021-12-30
author: Héctor Patricio
tags:
comments: true
excerpt: "Escribe aquí un buen resumen de tu artículo"
header:
  overlay_image: #image
  teaser: #image
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Ya hemos hablado de los cifrados de bloque, de flujo y de los hashes, ahora hablemos de un híbrido entre ellos que funciona como un hash pero usa una llave como un cifrado. El uso principal de este tipo de algoritmos es la autenticación y verificación de mensajes, pero también pueden ser usados para generar derivados de una llave, por su carácter pseudo-aleatorio. 

En general este tipo de algoritmos se llaman **hashes con llave** o _Keyed Hashes_. Empecemos a hablar del tipo más sencillo y usado: la generación de códigos de autenticación de mensajes.

## Message Authentication Codes (MACs)

Un código de autenticación de mensajes es una función que recibe un mensaje y _una llave_ (secreta) y devuelve lo que llamamos una etiqueta, que es una cadena de bits de los tamaños comunes en los hashes.

En este tipo de algoritmos, si mantenemos la llave secreta, y la compartimos solamente con quien necesitamos verificar la autenticidad del mensaje, podemos comprobar el _origen_ (gracias a que sabemos que la llave está protegida) y que el mensaje está intacto (gracias a que las propiedades del hash).

Una forma de crear un hash con llave es simplemente poniendo la llave antes o después del mensaje que queremos autenticar y usando un algoritmo de hashing normal, **aunque ninguna de las dos formas es muy segura**, ya que es vulnerable a ataques de [_extensión de longitud_](https://en.wikipedia.org/wiki/Length_extension_attack) o de [_tamaño de llave_](^1). Un ejemplo en Python sería el siguiente:

```python

from hashlib import sha3_512

key = b'mi llave super secreta'
message = b'mi mensaje que puede o no ser secreto, pero del que me importa el origen y que no haya sido cambiado'

tag = sha3_512(key + message).hexdigest()

```

(Afortunadamente, ningún algoritmo de la familia SHA-3 es vulnerable a los ataques de extensión de longitud, por eso lo usamos aquí para el ejemplo)

A nuestra contraparte le enviamos el mensaje junto con el tag y para verificar la autenticidad del mensaje el receptor debe hacer exactamente la misma operación, por lo que necesita tener previamente la llave. Si el tag resultante es igual, quiere decir que el mensaje es auténtico y no ha sido modificado, reemplazado o viene de alguien que no tiene la llave.

Para que un MAC sea seguro, debe ser imposible crear un tag que parezca venir de alguien con la llave, sea por falsificarlo directamente o por poder adivinar la llave.

Los MACs más comunes son los que están basados en hashes, conocidos como **HMAC**, un término que seguro has visto si has estado desarrollando por algún tiempo.

## Códigos de autenticación de mensajes basados en hashes (HMAC)

Un _Hash based Message Authentication Code_ es un MAC creado a partir de un hash, operando de una manera diferente a simplemente poner antes o después la llave. Los HMACs hacen uso de dos valores adicionales, un padding interno y un padding externo. Los combinan con la llave para crear una etiqueta que no sea vulnerable a ataques de extensión de tamaño ni del tamaño de la llave.

Sin embargo, se conocen ataques efectivos contra los HMACs que permiten falsificar tags computando **2^64 operaciones** en promedio, lo cuál no es cualquier cosa, pero un atacante motivado (y con recursos) podría lograrlo sin problemas.
