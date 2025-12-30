---
title: "¿Por qué deberías aprender Go?"
date: 2019-09-01
author: "Héctor Patricio"
tags: ['go', 'golang', 'lenguajes-de-programación']
description: "Go es un lenguaje muy relevante en algunas áreas del desarrollo de software. Aprende para qué deberías usarlo y por qué te conviene aprenderlo."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/v1567376344/google-servers-datacenter_bs7xzt.png"
draft: false
---

> Go es **eficiente, escalable y productivo**. - _Rob Pike_

Go es un lenguaje popular por los rumores que hay acerca de él, como que es el lenguaje que va a matar a C, o que es muy muy rápido y poderoso. En este artículo vamos a hablar de qué cosas son ciertas y en qué casos te conviene aprender Go.

Empecemos hablando de cómo y por qué nació.

## Historia de Go

> Go fue diseñado por Google para resolver sus problemas, y Google tiene _grandes_ problemas. - _Rob Pike_

Go fue creado dentro de Google por un grupo de desarrolladores de software y científicos de la computación **MUY experimentados**. Las tres personas que lo iniciaron a pensar y diseñar en 2007 fueron Robert Griesemer, Rob Pike y **Ken Thompson** (sí, el co-creador de UNIX, grep y muchas cosas más). De ese tamaño son las personas que lo diseñaron, y así se siente el lenguaje cuando lo usas.

Después de una serie de correos y discusiones sobre el diseño, empezaron a trabajar en él y [lo presentaron como proyecto Open Source en 2009](https://www.youtube.com/watch?v=rKnDgT73v8s), a partir de ahí muchas personas tanto de dentro como de fuera de Google han contribuido a su desarrollo.

## Características de Go

Go fue concebido pensando en los problemas que los diseñadores veían en los sistemas de Google: su proceso de desarrollo estaba entorpecido por las herramientas que usaban.

Según Rob Pike, todo era demasiado lento: demasiado lento de compilar, demasiado lento de construir, demasiado lento de pensar. Cuando decimos que el tiempo de compilación era demasiado largo nos referimos a que podía llegar a tomar _varias horas_ para compilar un sistema.

También había una "explosión de complejidad". Así que Go fue pensado para ser simple, de una "simplicidad radical". Por lo tanto, carece de características que otros lenguajes sí tienen, pero hacen que los programas sean complejos.

> La simplicidad es la clave del buen software. - _The Go Programming Language_

Analicemos las características de Go, un lenguaje pensado para trabajar en sistemas muy grandes de manera simple.

### Procedural, con flexibilidad para orientación a objetos

El paradigma principal de Go es el procedural se parece mucho a C en este aspecto. Sus principales medios de organización son las funciones y los paquetes, aunque permite crear un tipo débil de organización muy parecida a los objetos mediante `structs`.

Aquí puedes ver un 'Hello world':

```go
package main
import "fmt"

func main() {
  fmt.Printf("¡Hola Go!\n")
}

```

### Tipado estático y fuerte

Go es un lenguaje fuertemente tipado, lo cuál significa varias cosas:

* La declaración de variables implica el tipo de valor que estará asociado a esta instancia del nombre, por lo que no puede usarse para guardar otro tipo de valor. En Go no necesariamente se tiene que decir explícitamente el tipo de valor a usarse, puede ser inferido:

```go

miNombre := "Héctor"  // La variable es un string

```
Esto es verificado en tiempo de compilación, por lo que podrás estar tranquilo de que Go no te dejará correr programas usando variables como lo que no son.

* No existe la conversión o forzamiento de tipos automática e implícita, como en JS, que intenta realizar la operación aunque los tipos de valor usados no tengan sentido en la operación. En Go, si intentas hacer una operación con tipos no compatibles el programa puede no compilar o fallar en tiempo de ejecución.

### Rápida compilación

Pensado para sistemas muy grandes, justo como los desarrollados en Google, Go se toma en serio el tiempo de complicación y es muy rápido al compilar los programas, a diferencia de Java, C o C++. Esto está apoyado por tres pilares:

- Las dependencias están puestas al principio de cada archivo, por lo que no hay que buscar en todo el programa por dependencias perdidas.
- Las dependencias no forman ciclos, por lo que pueden organizarse para que sean compiladas independientemente, incluso de manera paralela.
- El programa objeto compilado de cada paquete exporta información útil para sus dependencias que puede ser usada sin tener que leer todo el paquete.

### Manejo de dependencias y paquetes

Go tiene en su biblioteca estándar más de 100 paquetes y la comunidad de Go cada vez contribuye más paquetes. Go viene con la herramienta para la línea de comandos `go` que es fácil de usar para manejar proyectos creados con Go. La herramienta `go` nos ayuda a administrar nuestras dependencias: descargarlas, limpiarlas e instalarlas.

### Manejo de memoria

Go tiene manejo automático de memoria, lo que quiere decir que tal como en Java o Python, no tienes que preocuparte de liberar la memoria manualmente. Sin embargo, esta característica lo hace poco práctico para sistemas que requieran tratamiento de datos en tiempo real demasiado fuerte y preciso.

## Concurrencia

![La mascota de Go haciendo el trabajo](https://res.cloudinary.com/hectorip/image/upload/v1567320490/Go-routines-gopher_vgcpbt.jpg)

A esta característica decidimos dedicarle un poco más de espacio. Debido a que el mundo de la computación ha cambiado desde que se escribieron los primeros programas, en los que se contaba con sólo un procesador, el equipo de Go le dio gran importancia a la capacidad de **crear programas con un muy buen diseño concurrente**. Eventualmente estos programas podrían correr en _paralelo_ aprovechando los sistemas de computación que existen actualmente, con múltiples procesadores.

Go permite crear procesos concurrente de manera muy sencilla:

```go

go myFunc()

```

Eso es todo. Go ejecutará la función `myFunc` de manera concurrente (se ejecuta de manera independiente al programa principal o a otras funciones concurrentes). Esto es una **goroutine**.

Go soporta dos modelos de concurrencia:

- **Comunicación de procesos secuenciales** (Communicating Sequential Processes - CSP), en la que cada proceso tiene sus propias variables, y se transfieren información entre ellos mediante mensajes. En el caso de Go es a través de *canales*.

- **Multi-hilo con memoria compartida**. En este tipo de concurrencia todos los procesos escriben sobre el mismo espacio de memoria, es decir, comparten variables, pero debe haber algúna forma de coordinación entre ellos para que no choquen ni se bloqueen mutuamente al tomar un recurso.

**La concurrencia es uno de los puntos más fuertes de Go.**

## Ventajas de Go sobre otros lenguajes

Hablemos de en qué casos son buenos para usar Go.

### Eficiencia al correr

Go no corre sobre ninguna máquina virtual. Crea ejecutables para los sistemas operativos a los que apunta, que contienen todo lo necesario para poder ejecutarse sin necesidad de tener algo instalado allí. Al ser compilado, Go es mucho más eficiente para correr que otros lenguajes interpretados, como JS, Python o Ruby. Consume menos memoria y su velocidad se acerca a la de C.

### Legibilidad

Go fue pensado para ser _simple_. Sus estructuras, su sintaxis y su filosofía lo hacen fácil de leer y de aprender. Es cierto que no es tan legible como Python o Ruby, por ejemplo, pero es mucho más legible que otros lenguajes con características similares como C++ o Java.

### Usable

Una de las promesas de Go desde el principio era poder hacer mucho con poco. Y es algo que cumple completamente. Su librería estándar está diseñada y construida por **verdaderos titanes** de la ingeniería del software, practicantes de esto por más tiempo que la vida de muchos de los que leerán este artículo. El siguiente ejemplo es un servidor web con una ruta, sin usar ningún framework o biblioteca extra, sino la pura biblioteca estándar de Go.

```go
package main

import (
    "fmt"
    "net/http"
)

func main() {
    http.HandleFunc("/", HelloServer)
    http.ListenAndServe(":8080", nil)
}

func HelloServer(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello, %s!", r.URL.Path[1:])  // te saluda de regreso
}

```

## Desventajas

### Sistema de tipos

Esta no es una desventaja como tal de Go, sino una creada por el ecosistema de desarrollo actual: al haber tantos lenguajes que hacen manejo de valores y tipos de dato automáticamente, al programar en _cualquier_ lenguaje tipado, incluyendo Go, muchos sienten que están desperdiciando su tiempo.

## Relativamente joven

Go tiene a penas 10 años de haber salido a la luz, 12 desde que se empezó a diseñar. El tiempo de vida de un lenguaje influye en su usabilidad y la conveniencia de varias formas:

- La comunidad que ha desarrollado
- Las herramientas disponibles
- Los errores encontrados
- Experiencias de otros desarrolladores con diferentes tipos y tamaños de sistemas

Considera esto si tienes que hacer un proyecto grande.

## Proyectos que lo usan

Muchos proyectos importantes del mundo de la infraestructura, orquestación de servidores, contenedores, bases de datos y herramientas para programadores lo usan. Algunos ejemplos:

- Docker
- Kubernetes
- Terraform y Vault (casi todos las herramientas de HashiCorp)
- [InfluxDB](https://www.influxdata.com/)
- [Caddy](https://github.com/caddyserver/caddy)

Esto te debería dar una idea de la importancia de Go en el ecosistema de desarrollo. Grandes proyectos lo usan, grandes empresas lo usan.

## Go vs Rust

¿Cuál de los dos lenguajes va a lograr efectivamente reemplazar a C, con características más modernas y como un lenguaje más adaptado a las necesidades actuales?

Esto es pura opinión: Rust es un mejor candidato para reemplazar a C por sus características de manejo de memoria. Pero Rust no es un lenguaje tan fácil de aprender o empezar com Go.

En Go puedes hacer muchas cosas que haces con C razonablemente bien, sin tanta complicación y sin tener que manejar la memoria manualmente o semi-manualmente. La prueba está en todos los proyectos que manejan cosas de bajo nivel.

Más adelante tendremos un artículo de por qué deberías aprender Rust.

## Conclusión

Go es un lenguaje relevante en 2019, 10 años después de haber nacido y lo seguirá siendo por muchos años, sobre todo por los proyectos ya desarrollados en él y las características de las que hablamos en este artículo. Aprenderlo te dará una herramienta más para desarrollar programas que valgan la pena y cumplan con lo esperado.

Pero como [Shane Parrish](https://fs.blog/about/) dice: Go es "simple pero no fácil". Es sencillo empezar a programar con él, pero dominar sus conceptos requiere estudio y esfuerzo.

Go se siente como una herencia de **gente muy sabia haciendo un lenguaje para hacer cosas grandes**. No te arrepentirás de aprenderlo.
