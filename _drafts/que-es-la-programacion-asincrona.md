---
title: "¿Qué es la programación asíncrona?"
date: 2024-10-28
author: Héctor Patricio
tags: async/await concurrencia javascript
comments: true
excerpt: "Entender la programación asíncrona es un requisito si eres un desarrollador de
software que quiere sacar el mejor rendimiento de una computadora, hablemos de qué es y cómo dominarla."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1702917369/artisanalphoto-MJcb7ZhNeUA-unsplash_s6toxn.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1702917369/artisanalphoto-MJcb7ZhNeUA-unsplash_s6toxn.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

La programación asíncrona es uno de los primeros temas avanzados que encontrarás
al programar, especialmente si desarrollas aplicaciones web. Esto es aún más
común si haces **JavaScript**, que es un lenguaje que se usa en entornos de
ejecución asíncronos.

En este artículo la explicaremos para que puedas programar de manera asíncrona
con seguridad.

## ¿Por qué existe? - El caso de la programación asíncrona

Imagínate un proceso de la vida real en el que tengas una conjunto de recursos
limitados, que sean completamente necesarios para terminar el trabajo. Por ejemplo,
imagina que quieres hacer una comida especial, en la que necesitas usar un horno.
En el horno puedes poner un platillo a la vez, ya que requiere un tiempo y temperatura
específica. Pero este platillo especial tal vez va acompañado de una sopa que puedes
hacer mientras el platillo principal está en el horno.

En términos computacionales, estas dos tareas están sucediendo de manera concurrente,
aunque tú literalmente no estés haciendo ambas cosas al mismo tiempo. No vale la pena que
te sientes a esperar a que el lomo del horno esté listo para empezar a hacer la sopa.
Puedes hacer la sopa mientras esperas, ya que no ocupan los mismos recursos.

Exactamente pasa lo mismo en los programas de computadora, se tienen que ejecutar tareas
que usan recursos compartidos o lentos, como por ejemplo el sistema de archivos o la red.
En la programación web también se da que el programa está esperando la respuesta de el
usuario y mientras tanto puede seguir haciendo otras cosas. Aquí es donde entra la programación
asíncrona.

## ¿Qué es la programación asíncrona?

Para entenderla primero tenemos que entender la programación tradicional o
síncrona (creo que la palabra correcta en español es _sincrónica_).

En la programación tradicional, las cosas siempre suceden en un orden estricto:
una instrucción empieza y hasta que no se termina, no se ejecuta la siguiente.
Observa el siguiente código, en Python, para a abrir un arhivo:

```python
with open("archivo.txt", "r") as file:
    data = file.read()
    print("Archivo leído")
print("Log final")
```

El resultado de este código es:

```log
Archivo leído
Log final
```

En este código todo sucede de manera perfectamente secuencial.

Pero en lenguajes con programación asíncrona, esta operación que es tardada
en términos computacionales se puede hacer de manera asíncrona, es decir
fuera de orden.

```js
const fs = require("fs");

fs.readFile("archivo.txt", "utf8", (err, data) => {
    console.log("Archivo leído");
});

console.log("Esperando a que se lea el archivo");
```

El resultado de este código es:

```log
Esperando a que se lea el archivo
Archivo leído
```

Observa cómo en esta versión, el código que está ANTES: `console.log("Archivo leído")`,
se ejecuta DESPUÉS. Esto es una demostración de código asíncrono.

La explicación a esto está en que con la programación asíncrona podemos modificar
**cuándo se ejecutan las cosas**. Pero otra visión es que se pueden ejecutar cosas
en diferentes "lados" o "momentos" y tú elegir **cuándo** usas los resultados de
la ejecución.

Usamos este ejemplo de abrir un archivo porque por su naturaleza es lento (comparado)
con cálculos u operaciones comunes.

La **programación asíncrona** es un forma de ejecutar las acciones de tu programa en
la que no se espera siempre que una acción o instrucción termine para continuar
con el programa.

Como vimos en el primer ejemplo, en la programación síncrona (también llamada
_bloqueante_ [blocking]), ninguna acción comienza hasta que le previa haya terminado.
En la programación asíncrona, con técnicas o palabras reservadas específicas le
indicamos al motor de ejecución que no es necesario a que una acción termine para
continuar con la siguiente, pero también le podemos decir qué hacer cuando la
acción termine. Por esto mismo, la programación asíncrona también se conoce como
_no bloqueante_ (non-blocking).

## Para qué sirve la programación asíncrona

Veamos las restricciones que tenemos, para entender por qué es útil. Cuando
creas un sistema, la velocidad de ejecución puede verse limitada por dos
categorías de cosas:

- De los cálculos que estás haciendo
- De la información que estás obteniendo o guardando en algún lugar

En el primer caso, llamamos a la ejecución **CPU bound** y en el segundo **I/O bound**.
En español me gusta llamarle **limitado por el procesador** y **limitado por la entrada
y salida de datos**.

### CPU bound - limitado por la cantidad de cálculos que puedes hacer

Cuando tu programa es pesado en los cálculos que tiene que hacer, como cuando
tienes que procesar multimedia, hacer multiplicación de matrices o cosas
similares, puedes decir que tu programa es **CPU bound**, o que está limitado por
el poder de procesamiento. Es decir, mientras más poderoso sea el procesador,
más rápido será tu programa. Esto también es cierto si tienes múltiples
procesadores _y puedes distribuir el cómputo entre ellos_, por ejemplo:

- Si tienes un procesador con múltiples cores o múltiples hilos de ejecución físicos
- Si tienes múltiples computadoras en una red

En el primer caso, necesitas una plataforma que te ayude a utilizar el poder
de procesamiento de los múltiples cores, sea implícitamente o explícitamente. Por
ejemplo plataformas como la **máquina virtual de Erlang** (llamada BEAM), automáticamente distribuyen
la carga en los múltiples cores disponibles. En otros lenguajes como en Python,
tienes que hacerlo explícitamente, pero incluso eso tiene limitaciones. Pero
esto que te estoy diciendo es **programación concurrente**.

La programación asíncrona se puede ver como una herramienta para manejar la
programación concurrente y hacerla más sencilla. Piénsala como en una capa de
abstracción sobre la programación concurrente, que te permite **expresar de forma
explícita** que otras partes del programa _pueden_ estarse ejecutando en otro
tiempo o en otro _espacio_ (proceso o hilo).

### I/O bound - limitado por la velocidad de entrada y salida de datos

Cuando un programa consume o produce mucha información tiene que
ponerla en algún lugar. Este lugar puede ser:

- La memoria RAM
- El disco duro (o sistema de archivos)
- La red (mandarla o pedirla a otra computadora)

Cuando tu programa hace mucho esto, se dice que el programa está limitado por la
velocidad de entrada y salida de datos, o **I/O bound**.

La programación asíncrona te puede ayudar de manera más sencilla, sobre todo en
el caso de las peticiones de red. ¿Cómo? Justo en el ejemplo de 

## Conclusión

Entender la programación asíncrona es esencial en la programación moderna, muchos
lenguajes y sobre todo _entornos de ejecución_ lo implementan. Entenderla y usarla
te ayudará a crear programas más eficientes y que cumplan con el rendimiento que
tus usuario esperan.
