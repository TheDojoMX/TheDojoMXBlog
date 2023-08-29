---
title: "Las tres garantías de seguridad de un hash"
date: 2023-08-28
author: Héctor Patricio
tags:
comments: true
excerpt: ""
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,e_oil_paint:11,w_1400/v1692582347/neom-bhKqZNZeAR0-unsplash_refcre.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,e_oil_paint:11,w_400/v1692582347/neom-bhKqZNZeAR0-unsplash_refcre.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

En este artículo profundizaremos sobre las garantías de seguridad mínimas que una función hash debe cumplir para ser criptográficamente segura. En un artículo anterior: [¿Qué es un hash?](/2021/12/02/algoritmos-criptograficos-que-es-un-hash.html) ya hablamos más detalladamente de la definición y de los algoritmos que puedes usar aún hoy de manera segura.

Empecemos por una pequeña definición de lo que es una función hash en la criptografía.

## ¿Qué es un hash?

Un hash es una función que te devuelve un valor de tamaño fijo independientemente del tamaño de la entrada, esto implica una compresión de datos. Las funciones hash que son usadas en criptografía, tienen la característica de entregar valores completamente _impredecibles_, tanto para un humano como para una computadora. Es decir que no hay manera de saber qué valor va a entregar una función hash para un valor dado si no le has pasado ese valor antes.

Lo anterior no quiere decir que las funciones hash devuelvan algo diferente cada vez que las ejecutas, sino que para un valor dado, siempre devuelven el mismo resultado, y aquí es donde radica su utilidad.

Un hash perfecto se comportaría como un generador de valores aleatorios, pero debido a lo que hemos dicho anteriormente, deben ser **deterministas** al mismo tiempo que **impredecibles**.

Para medir la seguridad de una función hash, se usan tres pruebas, que se conocen como las garantía de seguridad de un hash. 

Estas garantías son:

1. Resistencia a la primera preimagen
2. Resistencia a la segunda preimagen
3. Resistencia a la colisión

Cada una de estas garantías se refiere a un tipo de ataque que se puede hacer a una función hash. Vamos a explicarlas pero antes aclaremos algunos términos.

## Imagen y preimagen

En matemáticas, una función es una relación entre dos conjuntos de valores, uno de entrada y uno de salida. En la mayoría la de las funciones matemáticas comunes, cada valor de entrada tiene un único valor de salida.

Tomemos como ejemplo: $f(x) = x + 1$, esta función toma un valor $x$ y le suma $1$, por lo que cada valor de $x$ tiene un único valor de salida, porque sabemos que un número cualquiera tiene solamente un sucesor.

Pero no todas las funciones se comportan así, por ejemplo: $f(x) = x^2$. En esta función el valor 4 puede ser generado por dos valores de entrada diferentes: $2$ y $-2$.

Cuando vemos una función así no es común que nos definan el conjunto de entrada, así que asumimos que el conjunto de entrada o **dominio** es el conjunto de los números reales, y el conjunto de salida o **codominio** es el conjunto de los números reales.

Pensemos en el dominio y codominio como conjuntos amplios en los que los valores de entrada y salida _podrían estar_. La **imagen** de una función es el conjunto de valores que _están_ en el codominio, es decir, los valores que la función _puede_ devuelve. La **preimagen** es el conjunto de valores que _pueden_ ser entrada de la función.

En términos prácticos para nosotros los programadores, la imagen es casi equivalente al codominio, y la preimagen es el dominio.

Esta imagen sacada de Wikipedia lo ilustra un poco mejor:

![Imagen vs Codomino](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_600/v1693144037/Codomain2_kzda4n.svg){: .align-center}

La imagen es el área amarilla, mientras que Y es el codominio, y X es el dominio. Lo último que nos hace falta saber es que aunque imagen y preimagen son los conjuntos de entradas y salidas del algoritmo, también nos podemos referir así a un valor individual de este conjunto.

Apliquemos los aprendido al ejemplo de la función $f(x) = x^2$. El dominio es el conjunto de los números reales, y el codominio también es el conjunto de los números reales. La imagen es el conjunto de los **números reales positivos que tengan una raíz cuadrada**, y la preimagen es el conjunto de los números reales. Un ejemplo concreto: para el valor `4` considerado como resultado de la función o **imagen**, tendría _dos_ preimágenes: $2$ y $-2$.

Ahora sí, hablemos de la primera garantía de seguridad de un hash.

## Resistencia a la primera preimagen

Aquí debes poner atención a los valores _que se dan_ para hacer la prueba de seguridad. Presta atención a cuando se dice "dado un valor", estos son la valores que suponemos que ya se conocen.

En la primera garantía es: **Dada** una _imagen_ es computacionalmente inviable encontrar una _preimagen_ que la genere.

En palabras de programadores: Dado un hash, es computacionalmente inviable encontrar un valor que al ser pasado a la función hash, genere ese hash.

¿Por qué decimos **un** valor que genere ese hash y no **el** valor que genere ese hash? Porque para un valor de salida, puede haber más de un valor de entrada que lo genere. Especialmente para los hashes, su conjunto de valores posibles es infinito: todas las combinaciones de bits posibles de cualquier tamaño.

¿Cuál es el tamaño del conjunto de posibles salida? Eso depende del hash usado y su número de bits. Por ejemplo, el SHA-256 genera hashes de 256 bits, por lo que su conjunto de posibles valores es $2^{256}$, que es un número muy grande, pero no infinito, por lo que es posible que dos valores generen el mismo hash. Cada uno de esos valores sería _una preimagen_ de un hash dado.

Entonces ya tenemos todo el escenario: nos han dado un hash y tenemos que encontrar uno de los infinitos valores que pueden producir ese hash, una preimagen.

Pues bien, para un hash criptográficamente seguro esta operación debe de ser imposible de realizar de manera más eficiente que usando fuerza bruta, es decir, probando todos los valores posibles hasta encontrar uno que genere el hash dado.

Para que un hash sea considerado seguro, hallar una preimagen por fuerza bruta debería tomar $2^{n}$ operaciones, donde $n$ es el número de bits del hash. Por ejemplo, para el SHA-256, que tiene 256 bits, toma $2^{256}$ operaciones, que es un número muy grande, computacionalmente inviable.

Por ejemplo, imagina que puedes hacer 1 millón de operaciones por segundo, aproximadamente $2^{19}$. Encontrar una primera preimagen para el SHA-256 te tomaría $2^{256} / 2^{19}$, es decir $2^247$ segundos, mientras que lo que se calcula que ha durado el universo son $2^{38}$ segundos.

Pongamos un ejemplo en Python. Supongamos que la función `hash` es un hash seguro, y que la función `mensaje_aleatorio` devuelve un mensaje diferente cada vez. Pon atención en lo que recibe la función `primera_preimagen`:

```python
def primera_preimagen(h):
    m = mensaje_aleatorio()
    while hash(m) != h:
        m = mensaje_aleatorio()
    return m
```

Este debería ser el mejor ataque que se pueda hacer sobre un hash seguro.

## Resistencia a la segunda preimagen

Esta garantía de seguridad es muy parecida a la primera, pero lo que se recibe aquí es una _preimagen_ y se debe encontrar otra preimagen que genere el mismo hash.

La garantía de seguridad debería ser la misma: encontrar una segunda preimagen debería ser computacionalmente inviable, es decir, que tomaría $2^{n}$ operaciones, donde $n$ es el número de bits del hash.

Pongamos un ejemplo en Python. Observa que usamos la función `primera_preimagen` que definimos antes:

```python
def segunda_preimagen(m):
    h = hash(m)
    m2 = primera_preimagen(h)
    return m2
```

Este ataque no implica más que hashear el mensaje y encontrar una primera preimagen de ese hash. Si el hash es resistente a la primera preimagen, entonces también lo será a la segunda.

Parece que esta garantía no tiene mucho sentido, pero vayamos a la tercera y la más conocida.

## Resistencia a colisiones

Una colisión es cuando dos valores diferentes generan el mismo hash. Ya mencionamos que, al tener un conjunto infinito de valores de entrada y tener un conjunto muy grande (_pero limitado_) de valores de salida, es inevitable que suceda esto, de hecho, en este caso, un conjunto infinito de valores de entrada generan el mismo hash.

Pero hagamos un caso concreto. Imagina que tu hash recibirá cadenas de bits de 512 bits, y generará un hash de 256 bits. Esto significa que el conjunto de posibles valores de entrada es $2^{512}$ y el de posibles valores de salida es $2^{256}$. A cada valor de salida le corresponden $2^{512}/2^{256} = 2^{512-256}$ valores de entrada, es decir, que para cada valor de salida hay $2^{256}$ valores de entrada que generan el mismo hash.

Bueno, pues la tercera garantía de seguridad indica que **debe ser computacionalmente inviable encontrar una colisión**. En este caso no se nos da nada, ni una imagen (hash), ni una preimagen (valor de entrada). Se puede escoger cualquier valor de entrada para encontrar una colisión.

Aquí entra la segunda garantía de seguridad, si la función hash es resistente a la segunda preimagen, es resistente a colisiones. En Python, el mejor algoritmo para encontrar una colisión debería ser el siguiente para un hash seguro:

```python
def encontrar_colision():
    m = mensaje_aleatorio()
    return encontrar_segunda_preimagen(m)
```

La garantía de seguridad que debe de cumplir un hash seguro es que encontrar una colisión debería tomar $2^{n/2}$ operaciones, donde $n$ es el número de bits del hash. Por ejemplo, para el SHA-256, que tiene 256 bits, tomaría $2^{128}$ operaciones, que sigue siendo un número muy grande, computacionalmente inviable.

¿Por qué $2^{n/2}$? Porque es más fácil encontrar _un par_ de valores que generen el mismo hash sin tener restricciones, que encontrar _un valor_ que genere un hash dado.

Si haces $N$ hashes, puedes tener ~$N^2$ oportunidades para encontrar una colisión por que puedes comparar cada hash con todos los demás. Esto es lo que se conoce como la paradoja del cumpleaños.

## Cómo se vuelve inseguro un hash

Un hash seguro se comporta de manera completamente impredecible con respecto a su valor de entrada. Los hashes inseguros empiezan a dar muestras de regularidad en sus salidas o tienen salidas demasiado pequeñas.

De esta manera, es posible encontrar métodos estadísticos para analizar las salidas y así encontrar patrones que permitan encontrar colisiones o preimágenes más fácilmente.

## Conclusión

En este artículo vimos las tres garantías de seguridad que debe cumplir una función hash para ser criptográficamente segura. Te sirven para entender claramente de lo que se habla cuando se han encontrado colisiones en un hash, y poder evaluar la gravedad de la situación.
