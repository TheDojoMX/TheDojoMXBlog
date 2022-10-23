---
title: "Crea hashes resistentes a balas con Keccak (también llamado SHA-3)"
date: 2022-10-12
author: Héctor Patricio
tags: criptografia crypto hash keccak
comments: true
excerpt: "¿Por qué deberías usar SHA-3 para tus nuevos desarrollos? No hay pretexto ya para que uses lo mejor y más probado"
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_crop,h_400,w_1200,x_0,y_386/v1665632333/DALL_E_2022-10-12_22.38.45_cmmlql.png
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_crop,h_150,w_300,x_0,y_386/v1665632333/DALL_E_2022-10-12_22.38.45_cmmlql.png
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Ya hemos hablado en este blog de lo que es un [hash](/2021/12/02/algoritmos-criptograficos-que-es-un-hash.html) e incluso qué hashes puedes usar para guardar tus [passwords de manera segura](/2021/12/03/algoritmos-criptograficos-hashes-seguros-para-alamcenar-passwords.html).

En este artículo vamos a hablar de uno en específico, el que estamos seguros que deberías usar para cualquier uso futuro en tus programas y sistemas, el que ha sido nombrado como el Secure Hash Algorithm 3 ([SHA-3](https://www.nist.gov/publications/sha-3-standard-permutation-based-hash-and-extendable-output-functions?pub_id=919061)): **Keccak**.

## ¿Qué es Keccak?

[Keccak](https://keccak.team/) es una familia de funciones, creadas para cubrir la necesidad de un sucesor de la versión 2 del _Secure Hash Algorithm_, que tiene algunas limitaciones y vulnerabilidades (por ejemplo, el ataque de extensión de longitud).

Está basada en una construcción de esponja, y usa internamente una función criptográfica llamada **Keccak-f**, que se encarga de permutar (cambiar de lugar o mezclar) los bits de la entrada de manera segura.

Después de haber ganado la competición para la versión 3 del _Secure Hash Algorithm_, y por lo tanto ser nombrada **SHA-3**, ha sido estandarizada en diferentes documentos para diferentes usos. La estandarización implica que ha sido examinada y analizada criptográficamente por organismos internacionales, empresas e individuales para estar seguros de que no tiene deficiencias como función hash criptográfica.

Un punto interesante es que uno de los diseñadores de esta función, también participó en la creación del actual AES: [Joan Daemen](https://cs.ru.nl/~joan/), probablmente es un investigador al que le debamos prestar más atención, ya que casi toda nuestra seguridad actual y futura está influida por él.

## ¿Qué es una construcción de esponja?

La "arquitectura" interna de Keccak se distingue de otras funciones _hash criptográficas_ por ser tener una **construcción de esponja**. SHA-1 y SHA-2 usan una construcción de [Merkle–Damgård](https://www.coursera.org/lecture/crypto/the-merkle-damgard-paradigm-Hfnu9).

 ¿Qué es una **construcción de esponja** y por qué nos importa como desarrolladores de software?

Una construcción de esponja usa una función de _permutación_ (en el caso de Keccak esta función se llama **keccak-f**). Un función de permutación mapea todas las combinaciones posibles de bits en la entrada a todas las combinaciones posibles de esa misma cantidad de bits, intercambiándolas. Por ejemplo, imagina una función que acepta 3 bits y devuelve 4 bits, y que intercambia los bits de la siguiente manera:

```center
000 --(f)--> 010
001 --(f)--> 100
010 --(f)--> 001
011 --(f)--> 111
100 --(f)--> 000
101 --(f)--> 110
110 --(f)--> 101
111 --(f)--> 011
```

Observa como ninguna de las combinaciones se repite en ninguno de los dos lados. **keccak-f** es una permutación de 1600 bits.

La construcción de esponja divide los bits de la salida en dos partes: _velocidad_ y _capacidad_. Esta división arbitraria, en el caso de **Keccak** depende de la versión que se quiera usar. La parte de la _velocidad_ define cuántas veces se tiene que aplicar la función, ya que mientras más grande sea, más rápido se conseguirá el tamaño deseado. La parte de la _capacidad_ define qué tan segura es la función, mientras más grande sea, más segura es la construcción de esponja (y más pequeña es la parte de velocidad, por lo que la función hash tardará más).

Keccak empieza este ciclo con un estado inicial de puros ceros. La entrada se divide en bloques del tamaño de la velocidad (si es más pequeña que la velocidad, se [aplica un padding](https://crypto.stackexchange.com/questions/40511/padding-in-keccak-sha3-hashing-algorithm)). Se aplica un XOR entre cada bloque y el primer bloque de la velocidad, y se le da como entrada a la función de permutación. Esto se hace **tantas veces como bloques haya**. Esta fue la etapa de absorción.

Finalmente, para obtener el hash, se "exprime" la función, siendo el primer bloque del resultado la parte de la _velocidad_ de la última iteración y para obtener los siguientes bloques se aplica la función de permutación sucesivamente hasta obtener la cantidad de bytes requeridos. La siguiente imagen ilustra el proceso (con una permutación de 8 bits y una velocidad de  5 bits):

![Arquitectura interna de una función construcción de esponja](https://res.cloudinary.com/hectorip/image/upload/v1666498363/Screen_Shot_2022-10-22_at_21.51.41_h0u7s0.png){: .align-center }
---

Ahora ya sabes cómo funciona a grandes rasgos **Keccak** internamente. **¿Por qué nos interesa esto?** Las funciones de esponja pueden ser configuradas para que absorban más o menos bits y por lo tanto son bastante flexibles, lo que permite crear funciones configurables y que pueden crear salidas de diferentes tamaños.

## Tamaños de Keccak

Keccak ofrece los mismos tamaños de salida que SHA-2. Existen las siguientes versiones:

* **SHA-3-224**: 224 bits
* **SHA-3-256**: 256 bits
* **SHA-3-384**: 384 bits
* **SHA-3-512**: 512 bits

Como siempre, mientras más grande sea la salida, más bits de seguridad ofrece y más difícil es de ser vulnerada.

## Usando Keccak

El siguiente ejemplo muestra cómo usar Keccak como SHA-3-256 en Python (SHA-3 está disponible desde la versión 3.6 de Python):

```python
from hashlib import sha3_256

hash = sha3_256(b"Hello world").hexdigest()
# resultado '369183d3786773cef4e56c7b849e7ef5f742867510b676d6b38f8e38a222d8a2'

```

Aquí hay un ejemplo en Go:

```go
package main
import (
 "fmt"
 "golang.org/x/crypto/sha3"
)

func main() {
 s := "hello world"

 // Un hash de 256 bits
 h := sha3.New256()
 h.Write([]byte(s))

 bs := h.Sum(nil) // terminamos la cadena

 fmt.Println(s) // hello world
 fmt.Printf("%x\n", bs) // 369183d3786773cef4e56c7b849e7ef5f742867510b676d6b38f8e38a222d8a2
}
```

Aquí hay una implementación de Java:

```java

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class Main {
  public static void main(String[] args) {
    MessageDigest md;
    try {
      md = MessageDigest.getInstance("SHA3-256");
    } catch (NoSuchAlgorithmException e) {
      throw new IllegalArgumentException(e);
    }
    byte[] result = md.digest("Hello world".getBytes());
    System.out.println(Main.bytesToHex(result));
  }

  public static String bytesToHex(byte[] bytes) {
    StringBuilder sb = new StringBuilder();
    for (byte b : bytes) {
      sb.append(String.format("%02x", b));
    }
    return sb.toString();
  }

}
```

Además, aquí puedes ver ejemplos de cómo usar Keccak (SHA-3) en otros lenguajes:

* [SHA-3 en JavaScript o TypeScript](https://www.npmjs.com/package/sha3)
* [SHA-3 en Ruby](https://github.com/johanns/sha3)
* [SHA-3 en Elixir, usando Erlang](https://www.erlang.org/doc/man/crypto.html#type-hash_algorithm)

## ¿Por qué usar Keccak?

SHA-3 o Keccak es una función más fuerte, sin vulnerabilidades conocidas, estandarizada y lista para ser usada como reemplazo de SHA-2 en cualquier lado sin grandes cambios. No hay pretexto para no usarla si existe una buena implementación en tu lenguaje.
