---
title: "Algoritmos criptográficos: hashes seguros para alamcenar passwords"
date: 2021-12-03
author: Héctor Patricio
tags: criptografía hash password
comments: true
excerpt: "Muchos desarrolladores cometen el error de usar un hash criptográfico seguro como SHA-256 para almacenar passwords en la base de datos. Veamos por qué no es conveniente."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1120/v1638592882/susan-wilkinson--ZgqdP78I4g-unsplash_uchtnu.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_300/v1638592882/susan-wilkinson--ZgqdP78I4g-unsplash_uchtnu.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Una práctica común para solucionar la identificación de usuarios es registrarlos con su nombre de usuario y contraseña. Para no almacenar su contraseña directamente, es una costumbre _hashearla_. Como aprendiste [en el artículo anterior](/2021/12/02/algoritmos-criptograficos-que-es-un-hash.html), un hash es una función que impide recuperar el valor original ya que simplemente la información se pierde.

Los hashes seguros hacen casi imposible encontrar una colisión (que dos passwords te devuelvan un mismo hash), por lo que parecerían una buena solución para crear un valor único para cada usuario. Debido a que son deterministas, cuando el usuario te da su password, calculamos el hash de nuevo, lo comparamos con el hash almacenado y verificamos si coinciden. En este caso, el usuario está autenticado.

¿Pero qué hash puedes usar para hashear un password? Todos hemos escuchado _que no se debe usar MD5 para hashear passwords_, pero la razón por la que se menciona que esto es un error normalmente no es la correcta. Se argumento que MD5 es un hash que está "roto", ya que es posible romper su seguridad con menos esfuerzo computacional del que su tamaño requeriría. Esto es cierto, pero no es la razón principal por la que no deberías usar MD5 para passwords.

La verdadera razón por la que nunca debes usar MD5 para esto es que **no está diseñado para esa función**, y puede ser atacado de manera sencilla y efectiva.

Hablemos de algunos tipos de ataques que pueden sufrir los sistemas de almacenamiento de información que usan un hash seguro normal para hashear sus passwords.

## Ataques de fuerza bruta

Un hash seguro que no presenta vulnerabilidades tiene la característica de que no hay una forma más inteligente de atacarlo que mediante probar todos los valores posibles de entrada. Por ejemplo, si sabemos que un sistema acepta letras y números y la mínima contraseña es de 6 carácteres, tendríamos que probar todas las combinaciones posibles de letras y números a partir de 6 carácteres.

Eso suena a que es mucho, sin embargo, con los hashes seguros no es un problema para los atacantes ya que estos hashes son muy eficientes y están pensados para correr lo más rápido posible.

Alguien con la suficiente motivación y paciencia podría lanzar un ataque de fuerza bruta con _hardware especializado_ y encontrar un password que coincida con el hash. Esto se puede hacer con hardware común como CPU's  y GPU's domésticos, que llegan a procesar cientos de miles de passwords **por segundo**, o con hardware especializado en hashear (FPGA's y ASIC's).

Herramientas como [hashcat](https://hashcat.net/hashcat/) te permiten hacer este tipo de ataques, pero lo más interesante es que debido a que conocemos la naturaleza de la información, podemos dirigir el ataque de manera un poco más inteligente, usando diccionarios de palabras y contraseñas comunes, haciendo todavía más probable romper la seguridad de estos sistemas.

Repitamos: lo que permite este tipo de ataques son los objetivos de diseño de las funciones hash seguras: que sean rápidas, y eficientes en memoria. Esta es la primera razón por la que **nunca debiste usar MD5** es esta. Pero, como podrás deducir, lo mismo aplica para cualquiera de familia SHA (SHA-1, SHA-2, SHA-3 y los que vengan), BLAKE, BLAKE2 y los que vengan. No importa que estas funciones sigan siendo seguras para otros usos.

## Ataques con tablas arcoiris (Rainbow Tables)

Imagínate que eres un atacante que quiere descubrir los passwords de los usuarios de diferentes sitios y sabes que todos usan SHA-256. En vez de hacer una ataque de fuerza bruta cada vez, preparas una tabla con dos columnas: el hash y el password. En la columna de passwords pondrás valores que sabes que pueden servir de passwords a los usuarios.

Esto que acabamos de describir es una versión sencilla de una **Rainbow table**, una colección de valores precalculados organizados para que, una vez teniendo el hash, puedas buscar el password correspondiente en la tabla. Se hace un intercambio de procesamiento por memoria. Las Rainbow Tables completas son un poco más complejas que lo que acabamos de describir, puedes leer más sobres ellas en este artículo: [Rainbow Tables](https://www.ionos.com/digitalguide/server/security/rainbow-tables/)

Debido al mal uso de los passwords y de los algoritmos para hasheo seguro, existen rainbow tables para millones de valores de todos los algoritmos. Aunque siguen siendo una amenaza, las Rainbow tables están cayendo en desuso, en favor de otros métodos más modernos y aprovechándose del poder de cómputo actual.

## Protección contra ataques a hasheo de passwords

La forma de protegerse contra valores precalculados y ataques de diccionario es más o menos sencilla: antes de hashear el password, agrega un valor aleatorio extra que puedas recuperar fácilmente y añadir cada vez que verificas el password. Esto se conoce como **salting**, siendo el valor aleatoria el **salt**.

Aunque es cierto que esto lo podrías hacer con cualquier algoritmo de hasheo seguro, se queda sin resolver el segundo problema: ¿Cómo nos protegemos contra ataques de fuerza bruta con hardware muy poderoso? Esto sólo se puede resolver de una forma: usando algoritmos que te obliguen a usar mucho procesamiento o mucha memoria, o ambos. Estas deben ser precisamente las metas de diseño de los algoritmos especializados en hasheo de passwords.

Hablemos de algunos de ellos y finalizarmos con el que deberías usar actualmente en 2021.

## Hashes seguros para passwords

Como ya lo dijimos, estos hashes deben ayudarte con una cosa principal además de ser seguros criptográficamente: ser costos en proceamiento y/o memoria, lo que se traduce en lentitud.

Pero además, algunos de estos algoritmos te ayudana a "salar" el password de manera automática, lo que es una ventaja para reducir errores en la implementación de esta práctica.

En esta sección hablaremos de los algoritmos, cómo cumplen con estas características y si los puedes seguir usando.


### PBKDF2


[PBKDF2](https://www.ietf.org/rfc/rfc2898.txt) - Es un acrónimo que significa "Password Based Key Derivation Function", versión 2.0 y que básicamente aplica un algoritmo de hasheo seguro a una contraseña repetidas veces. Puedes configurar el número de iteraciones, el algoritmo de hasheo, el tamaño del resultado y te pide el _salt_ para funcionar. Fue usada por varios frameworks de desarrollo web como Django, pero actualmente no se considera segura porque aunque es exigente en cómputo para una computadora normal, es débil contra hardware especializado.

### bcrypt

[bcrypt](https://www.usenix.org/legacy/event/usenix99/provos/provos.pdf) - Es un algoritmo diseñado específicamente con el objetivo de estar preparado para el mejoramiento que el hardware va teniendo, ya que tiene una "dificultad" configurable. Te provee **automáticamente de un salt seguro**, por lo que no recaerá en ti la responsabilidad de conseguirlo como en PBKDF2. Está basado en blowfish, otro algoritmo de cifrado que ha permanecido seguro. Bcrypt fue presentado en 1999 y sigue siendo considerado más o menos seguro, su recomendación está en duda ya que es posible atacarlo con hardware especializado y de bajo costo. [Este estudio de 2011](https://www.usenix.org/system/files/conference/woot14/woot14-malvoni.pdf) explica como se puede atacar con hardware especializado en cómputo paralelo y predijo muy bien que bcrypt no permanecería super seguro por mucho tiempo.

### scrypt

[scrypt](https://datatracker.ietf.org/doc/html/rfc7914) - Es una función diseñada para cubrir las carencias de PBKDF2 y bcrypt. Es tanto computacionalmente intensiva como pesada en memoria, por lo que no es tan fácil atacarla con hardware especializado. Es un función de muy reciente presentación, [Colin Percival la presentó en 2009](https://www.tarsnap.com/scrypt/scrypt.pdf). Es una secuencia de funciones pesadas en memoria que impide que sea atacada fácilmente con GPU's. FPGA's y ASIC's. Es una función que puedes usar conseguridad todavía ya que no se han encontrado ataques efectivos contra ella. Al igual que bcrypt, _sala_ (usa un salt) automáticamente, lo que le facilita la vida al desarrollador.

### Argon2

[Argon2](https://github.com/P-H-C/phc-winner-argon2/blob/master/argon2-specs.pdf) - Es la función más avanzada y con mejores garantías para generación de hashes resistentes a ataques con fuerza bruta. Es la ganadora del [Password Hashing Competition](https://www.password-hashing.net/) en 2015. Se dice que Argon2 es el estado del arte en lo que se refiere a hashing de passwords. Tiene tres variaciones principales: Argond2d, Argon2i y Argon2id.

¿Cuándo usar cada una?

- **Argon2d**  es más rápida pero al mismo tiempo está mejor protegida contra ataques de fuerza bruta de hardware especializado, por la forma en la que usa la memoria, sin embargo, es más vulnerable a ataques [side-channel](https://www.rambus.com/blogs/side-channel-attacks/). Es recoemndada cuando tus atacantes no tengan posibilidad de realizar estos ataques, como en servidores de backend y para generación criptomonedas.

- **Argon2i** es más lenta, más computacionalmente intensiva y resistente contra side-channel attacks, es la recomendada para hashear passwords. Da varias "pasadas" a los argumentos de entradda, por lo que es más dificil de atacar.

- **Argon2id** es un híbrido entre estas las dos variaciones anteriores, protegida parcialmente contra ataques side-channel al mismo tiempo que más computacionalmente intensiva que Argon2d. La recomendación es que si estás en incertidumbre uses Argon2d.

Argon2 permite configurar:

1. Memoria usada: mientras más memoria se use, más resistente será el hash y menos vulnerable será a ataques de fuerza bruta.

2. Número de iteraciones sobre la memororia. Esto lo hace más computacionalmente intensivo, de igual forma haciéndolo más dificil de atacar, haciendo la generación de hashes más lenta.

3. Grado de paralelismo. Es el número de hilos que se usan para generar el hash, el tiempo de ejecución variará dependiendo de la configuración.

4. Tamaño del hash, el salt y el tag. Esto también varía el grado de resistencia de tus hashes.

 En el artículo ["Cómo escoger los parámetros de Argon2"](https://www.twelve21.io/how-to-choose-the-right-parameters-for-argon2/) se describe una forma de escoger los parámetros de Argon2.

 Finalmente, aunque Argon2 no incluye la generación del salt en el argumento mismo, las implementaciones de Argon2 incluyen una función de generación de salt automática para que no tengas que hacerlo tú.


 ## Conclusión

Si estas haciendo una aplicación lo más recomendable es que uses scrypt o Argon2i. 