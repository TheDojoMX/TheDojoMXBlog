---
title: "Formas de hacer una API con Go"
date: 2020-09-20
author: "Héctor Patricio"
tags: ['go', 'apis', 'beego', 'gorilla-mux', 'gin-go', 'go-lang']
description: "Exploramos diferentes formas en las que puedes crear una API con Go, el lenguaje enfocado en la eficiencia de los programas permitiendo productividad para los programadores."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/v1594271709/CA5123E3-5CCD-4A32-A4D0-2DE9B27A13E8_pfxvrn.jpg"
draft: false
---

Go es uno de los lenguajes modernos más usados. Ya hablamos de [por qué deberías aprenderlo](/2019/09/01/por-que-deberias-aprender-go.html).

Ahora hablemos de un caso de uso práctico: **úsalo para crear una API HTTP**. En este artículo nos enfocaremos en la parte de comunicación HTTP y la generación de respuestas adecuadas.

La funcionalidad básica de tu API puede o no adaptarse completamente a Go (no es es tan fácil de escribir como un lenguaje dinámico como Python), pero definitivamente es un **lenguaje excelente** para crear interfaces de comunicación web, debido a su alto rendimiento y eficiencia.

Puedes ver algunas de las comparativas en los siguientes artículos:

- [Comparando el rendimiento de Go, NodeJS y Elixir](https://stressgrid.com/blog/benchmarking_go_vs_node_vs_elixir/). TL;DR: Go y Elixir llegan a manejar más de 100k conexiones sin ningún problema, Node empieza con problemas desde 30k y el más eficiente en cómputo y memoria utilizada _por mucho_ es **Go**.

- [Comparación de frameworks web ligeros](https://github.com/mroth/phoenix-showdown). Este artículo es un poco viejo, pero el resumen es que Gin (un framework web ligero de Go) es el que más peticiones soporta por segundo y con una consistencia excelente.

![Comparativa de micro-frameworks Web](https://res.cloudinary.com/hectorip/image/upload/v1574629781/Screenshot_2019-11-24_15.09.25_ozqwcu.png)

Hablemos de tres formas de crear una API sobre HTTP para tu próximo proyecto. Pero antes hablemos de una opción simple que no cubre muchos casos pero que se oye recomendada por todo internet.

## La biblioteca estándar

Cuando hice mi primer proyecto en Go, gran parte de la investigación sobre qué usar para crear un proyecto de una API web apuntaba a los **paquetes nativos** de Go.

Go tiene una biblioteca estándar que cubre **muchas** de las necesidades de un desarrollador moderno. Si has programado en él podrás estar de acuerdo en que se siente como subirte en hombros de gigantes, debido a que las personas que lo diseñaron y construyeron son _las mismas personas que sentaron las bases para los sistemas operativos modernos_. Imagínate cuánta experiencia tienen.

En la biblioteca estándar podemos encontrar un paquete que se llama `net/http` con el que puedes hacer, un servidor web con direccionamiento de rutas sencillo (la base de tu API) **con muy pocas líneas de código**. Puedes recibir peticiones HTTP, procesarlas y devolver una respuesta HTTP. El ciclo básico request -> response.

Aquí hay un ejemplo:

```go
package main

import (
	"fmt"
	"net/http"
)

// Implementando rutas HTTP
func main() {
	http.HandleFunc("/", handler)
	http.ListenAndServe("localhost:8080", nil) // iniciando el servidor
}

// handler recibe la petición http y la procesa para devolver una respuesta http
func handler(response http.ResponseWriter, request *http.Request) {
	fmt.Fprintf(response, "Hola Go API's") // Falta responder JSON
}
```

Si tu API es sencilla, expone pocas URLs y sabes que no requerirás mucho en campo de las peticiones HTTP (procesamiento de parámetros, manejo de rutas, etc.) la biblioteca estándar es una solución buena, pero para otros casos se queda un poco corta, ya que tendrías que implementar varias cosas a mano.

Su uso es sencillo como acabas de ver. Usar un framework web tiene el costo de agregar complejidad a **cambio de funcionalidades que no tienes que desarrollar tú**. Pero aquí te compartimos un artículo en el que un experto hablá de por qué _él_ prefiere no usar frameworks: [Why I Don't Use Go Web Frameworks](https://medium.com/code-zen/why-i-don-t-use-go-web-frameworks-1087e1facfa4).

Por eso te presentamos las opciones más comunes y algunos ejemplos.

## Gorilla Web Toolkit

![Gorilla Web Toolkit logo](https://avatars2.githubusercontent.com/u/489566?s=200&v=4){: .align-center}

[Gorilla Toolkit](https://www.gorillatoolkit.org/) es un conjunto de herramientas para web que, entre otras cosas tiene:

- Un router más completo que el de la biblioteca estándar: *Gorilla Mux*. Es compatible con el tipo de dato nativo de Go para las peticiones. Además incluye:
  - Ruteadores secundarios, para que organices mejor tu código.
  - Inversión de URL's: te permite generar la URL a partir de un identificador.
  - Matches complejos
- Middlewares: logging, compresión, recuperación
- Manejo de sesiones con cookies seguras
- Implementación de WebSockets y RPC
- Conversión de valores de entrada en `struct` de Go

Gorilla Toolkit **no es un framework**, puedes usar cada de sus herramientas por separado, como las vayas necesitando. Así que puede empezar con la librería estándar y agregar lo que necesitas de Gorilla poco a poco.

## Gin
![Gin go logo](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_250/v1600730661/color_whycuu.png){: .align-center}

[Gin](https://github.com/gin-gonic/gin) es un framework web para Go bastante completo que clama ser el más rápido de todos los frameworks web para Go. Ya está en su versión 1, por lo que puedes usarlo con confianza en proyectos serios.

Gin usa [httpRouter](https://github.com/julienschmidt/httprouter) que tiene funciones parecidas a Gorilla Mux, pero que dice escalar mejor que el de la librería estándar incluso.

Tiene utilidades incluídas para hacer render de XML, JSON, YAML y ProtoBuf, o sea que es perfecto para crear diferentes tipos de API's.

Además, tiene un montón de cosas más que puedes explorar en su documentación, que es muy completa y con muchos ejemplos, por si fuera poco.

## Beego

![Beego logo](https://beego.me/static/img/beego_purple.png){: .align-center}

[Beego](https://beego.me/) es un framweork que se especializa en API's RESTful e intenta usar lo mejor posibles las características de Go como las interfaces y las estructuras embebidas. Parece que está hecho en China.

Las cuatro características que resalta son:

1. Fácil de usar: es MVC  y tiene herramientas incluídas para poder desarrollar más fácilmente.
2. Inteligente: tiene características de ruteo avanzadas junto con monitoreo integrado que te permiten observar el estado de tu API.
3. Modular: su estructura interna está compuesta por varios módulos que te permiten avanzar rápidamente.
4. Alto desempeño

Es un framework bastante completo, que cumple con todo lo mínimo necesario para que puedas empezar a desarrollar tu API eficientemente, pero parece que tiene un defecto: al ser hecho en china, la documentación no está pulida completamente y puede que haya poca información en tutoriales y otras páginas.

## Echo

![Logo de Echo](https://cdn.labstack.com/images/echo-logo.svg){: .align-center}

[Echo](https://echo.labstack.com/) se promociona como el framework web minimalista. Tiene soporte para HTTP/2, ruteo sin uso de memoria dinámica (para mejor desempeño), TLS automático, middlewares flexibles y funciones utilitarias para responder fácilmente las peticiones web en cualquier formato.

En algunos benchmarks **echo** parece ser más rápido que Gin.

Tiene desarrollo bastante activo y la documentación contiene ejemplos suficientes, junto con algunas recetas y para que logres avanzar rápido.

## Conclusión

Existen múltiples opciones para crear tu API en Go. Hay para escoger dependiendo de tus gustos y de lo más importante para tu proyecto.
