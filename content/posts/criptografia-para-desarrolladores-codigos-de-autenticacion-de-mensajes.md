---
title: "Criptografía para desarrolladores: Códigos de autenticación de mensajes"
date: 2021-12-30
author: "Héctor Patricio"
tags: ['mac', 'hamc', 'aes', 'security', 'cryptography']
description: "A veces vemos nombres como HMAC-MD4 o AES-CMAC y no sabemos lo que significa. En este artículo hablaremos de los diferentes tipos de MAC y por qué son importantes."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1120/v1641020242/ethmessages--o90yRQoXAM-unsplash_tmjc6s.jpg"
draft: false
---

Ya hemos hablado de los cifrados de bloque, de flujo y de los hashes, ahora hablemos de un híbrido entre ellos que funciona como un hash pero usa una llave como un cifrado. El uso principal de este tipo de algoritmos es la autenticación y verificación de mensajes, pero también pueden ser usados para generar derivados de una llave, por su carácter pseudo-aleatorio.

En general este tipo de algoritmos se llaman **hashes con llave** o _Keyed Hashes_. Empecemos a hablar del tipo más sencillo y usado: la generación de códigos de autenticación de mensajes.

## Message Authentication Codes (MACs)

Un código de autenticación de mensajes es una función que recibe un mensaje y _una llave_ (secreta) y devuelve lo que llamamos una etiqueta, que es una cadena de bits de los tamaños comunes en los hashes.

En este tipo de algoritmos, si mantenemos la llave secreta, y la compartimos solamente con quien necesitamos verificar la autenticidad del mensaje, podemos comprobar el _origen_ (gracias a que sabemos que la llave está protegida) y que el mensaje está intacto (gracias a que las propiedades del hash).

Una forma de crear un hash con llave es simplemente poniendo la llave antes o después del mensaje que queremos autenticar y usando un algoritmo de hashing normal, **aunque ninguna de las dos formas es muy segura**, ya que es vulnerable a ataques de [_extensión de longitud_](https://en.wikipedia.org/wiki/Length_extension_attack) o se pueden encontrar colisiones si se usa una llave de tamaño variable. Un ejemplo en Python sería el siguiente:

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

Un _Hash based Message Authentication Code_ es un MAC creado a partir de un hash, operando de una manera diferente a simplemente poner antes o después la llave. Los HMACs hacen uso de dos valores adicionales, un padding interno y un padding externo. Los combinan con la llave para crear una etiqueta que no sea vulnerable a los ataques de extensión de longitud.

La construcción de HMAC funciona así:

1. Se combina la llave con el padding interno mediante la operación XOR.
2. Se hashea la la combinación de la llave y el padding interno junto con el mensaje del que queremos crear la etiqueta (a esto lo llamaremos H1).
3. Se combina la llave con el padding externo mediante la operación XOR.
4. Se hashea la la combinación de la llave y el padding externo junto con H1, el resultado de esto es la etiqueta de autenticación.

Sin embargo, se conoce un ataque efectivos contra los HMACs que permiten falsificar tags computando **2^n/2 operaciones** en promedio, lo cuál no es cualquier cosa, pero un atacante motivado (y con recursos) podría lograrlo sin problemas si **n**, el tamanño interno del estado del hash es muy pequeño. Un hash moderno tiene un estado de 512 bits, por lo que un ataque de tamaño de 2^n512/2 = 2^256 es impráctico.

Ya que un HMAC están basado en un algoritmo de hash, cuando se nombra se usa el nombre de este, por ejemplo: HMAC-SHA-256 o HMAC-SHA-3-512.

## Códigos de autenticación de mensajes basados en cifrados de bloque (CMAC)

Ya que los hashes pueden estar basados en cifrados de bloque, una construcción más directa es usar un cifrado de bloque como la base para un MAC. Así nacen lo CMACs, códigos de autenticación de mensajes basados en cifrados de bloque, por ejemplo AES-CMAC.
Aunque se siguen usando en algunos protocolos de seguridad, los más MACs más eficientes son los que no se basan en Hashes o cifrados de bloque, sino que tienen un diseño independiente.

## MACs con diseño independiente

Un MAC seguro es más fácil de lograr que un hash completamente funcional y seguro o que un cifrado de bloque con las mismas características, ya que al usar un llave secreta evitan que se pueda atacar tan fácilmente como un hash y al exponer una etiqueta pequeña, revelan menos información que un cifrado de bloque.

Es por eso que un MAC no requiere todo el poder de un hash ni de un cifrado de bloque. Gracias a esto se han dieseñado algortimos que usan esta ventaja para ser más eficientes. Hablemos de tres ejemplos:

1. [SipHash](http://cr.yp.to/siphash/siphash-20120918.pdf): Es una familia de algoritmos optimizada para autenticar mensajes cortos, originalmente diseñada para reemplazar las funciones hash en los diccionarios implmentados como hashtables.
2. [Poly1305](http://cr.yp.to/mac/poly1305-20050329.pdf): Es una función de autenticación de mensajes muy rápida y eficiente, más que cualquiera basada completamente en un algoritmo de bloque o un hash, usada para autenticar paquetes en dispositivos de bajo rendimiento en Android, por ejemplo.
3. [Pelican 2.0](https://eprint.iacr.org/2005/088.pdf): Es un MAC basado en AES (Rijndael), pero que no utiliza todo su poder y que funciona de forma eficiente gracias a esto. Sin embargo, este algoritmo no está implementado en ningún lugar importante.

Si lo que buscas es eficiencia, manteniendo la seguridad relativa de tus etiquetas de autenticación, este tipo de MACs son los que deberías usar.

## Conclusión

Conocer sobre los códigos de autenticación de mensajes es importante para no navegar perdidos entre todas esas siglas que luego vemos en las suites de seguridad de IPSec, TLS, SSL, SSH, HTTPS, etc. Ahora ya sabes lo que significa HMAC-SHA-512, AES-CMAC o Poly1305.