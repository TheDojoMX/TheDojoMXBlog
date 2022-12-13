---
title: "¿Por qué aprender Rust en 2023?"
date: 2022-12-13
author: Héctor Patricio
tags: rust aprendizaje lenguajes-de-programacion
comments: true
excerpt: "¿Por qué es Rust uno de los lenguajes más amados de la actualiad? ¿Te conviene aprenderlo? Vamos a platicar de eso en este artículo."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_crop,h_400,w_1024/v1670303988/DALL_E_2022-12-05_13.19.43_-_rust_on_a_gold_wall_digital_art_illustration_cinematic_m5cplm.png
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_crop,h_200,w_512/v1670303988/DALL_E_2022-12-05_13.19.43_-_rust_on_a_gold_wall_digital_art_illustration_cinematic_m5cplm.png
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Rust se ha establecido como uno de los lenguajes más queridos entre los desarrolladores en los últimos años y desde 2016 está en el número uno, según la encuesta anual de [Stack Overflow](https://insights.stackoverflow.com/survey/2016#technology-most-loved-dreaded-and-wanted). Esto no es de extrañar, ya que Rust es un lenguaje que ofrece **muchas cosas buenas** a aquellos que lo usan.

En este artículo vamos a hablar de algunas de sus características, las ventajas de su ecosistema, y por qué te conviene aprenderlo. Además vamos a hablar de cuándo no es tan buena idea.

## Historia y concepción

> No siempre fue así de claro, pero el lenguaje de programación Rust trata acerca de _empoderamiento_: no importa qué tipo de código estés escribiendo ahora, Rust te habilita para llegar más lejos, para programar con confianza en una variedad de dominios más amplia que la que antes hacías. - Nicholas Matsakis and Aaron Turon

Rust nació en 2006 como un proyecto personal de [Graydon Hoare](https://github.com/graydon), un empleado de Mozilla en ese entonces, que siempre ha trabajado en lado de los compiladores. Después de mostrárselo a su jefe, a Mozilla le interesó como una alternativa mejor que C y C++ para crear su motor de renderizado web llamado [Servo](https://servo.org/). Y, efectivamente, Servo actualmente estás escrito en Rust.

### Idea detrás de Rust

Según [la entrevista](https://www.infoq.com/news/2012/08/Interview-Rust/) que le hicieron a Graydon, en Rust quiso implementar todas las características que le parecían interesantes y amadas de otros lenguajes, pero para un lenguaje dedicado a la creación sistemas, con la teoría de que las concesiones y condiciones que hacen que lenguajes como C y C++ siempre fueran favorecidos, han cambiado desde que nacieron.

Así que Rust nació con la **seguridad de memoria y la concurrencia en mente**, pensando que el internet y la apertura que este provee hace que estas características sean muy importantes. Hablemos de estas características.

## Características de Rust

Rust en un lenguaje que quiere reemplazar a C y C++, por lo que necesita características que les compitan y los mejoren, hablemos de tres de ellas con las que lo está intentando.

### Rendimiento

C y C++ se distinguen por ser los lenguajes para creación de sistemas más eficientes, y por eso Rust tiene que ser por lo menos tan eficiente como ellos. Rust, en la mayoría de los casos logra equipararse al rendimiento de C y C++.

Aquí puedes ver algunas mediciones de Rust contra C++: [Benchmarks Rust vs C++](https://programming-language-benchmarks.vercel.app/cpp-vs-rust). Y aquí hay otros un poco más entendibles: [Rust vs C](https://levelup.gitconnected.com/which-is-faster-rust-or-c-lets-find-out-who-is-the-usain-bolt-87495c774c8). La conclusión a la que podemos llegar es que Rust es un contendiente muy serio para C y C++ en cuanto a velocidad y eficiencia.

Lo que tenemos que recordar es que Rust provee características que C y C++, que hacen más fácil y segura la programación, por lo que si es casi tan rápido como estos, más sus características extra, entonces es una gran oferta para los desarrolladores.

### Seguridad de memoria

La seguridad de memoria se refiere a la propiedad de los entornos de ejecución de los programas que te **asegura que las referencias a memoria siempre son válidas**. Si has programado en C y C++ has experimentado un entorno no seguro en memoria: puedes acceder a registros de memoria que no han sido inicializados y por lo tanto contienen información incierta. Para que la memoria siempre sea segura se necesita que siempre sea alocada por el programa y se del tipo y tamaño correcto.

Un programa que no es seguro en memoria puede dar bugs aleatorios o fallar aleatoriamente sin explicación alguna. Además también puede ser inseguro respecto a la integridad de tus datos, ya que las fallas en el manejo de memoria pueden ser explotadas de formas creativas por los atacantes para acceder a información sensible.

Uno de los objetivos de diseño en Rust es que sea seguro de memoria, para mi uno de los distintivos más grandes con C y C++.

¿Cómo logra Rust la seguridad de memoria? Mediante un sistema de verificación estático de [_prestamos_ y _pertenencia_](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html). En artículos futuros explicaremos cómo se logra la seguridad de memoria con este sistema.

### Productividad

Como lo dice la cita del principio, la ventaja principal de Rust es que te permite ser más productivo en diferentes aspectos de la programación.

Rust tiene a [cargo](https://doc.rust-lang.org/cargo/), el manejador de paquetes que además te ayuda a crear proyectos, correr las pruebas, realizar reportes diversos sobre tu código, compilar y administrar paquetes, etc.

Cargo te ayudará en formas que lenguajes más antiguos como C y C++ no pueden, no tendrás que crear los scripts de compilación a mano, o instalar un gestor de paquetes, etc.

### Abstracciones sin costo en tiempo de ejecución

Otra de las ventajas que Rust tiene para la productividad son las [abstracciones sin costo](https://boats.gitlab.io/blog/post/zero-cost-abstractions/) (zero-cost abstractions en inglés). Una abstracción sin costo se refiera a que puedes usar elementos de más alto nivel (que hacen más cosas por ti) en tus programas sin que esto genere un impacto negativo en el rendimiento del programa. Es decir, Rust genera el mismo código ensamblador sin importar si usas un for para sumar los elementos de un arrglo, si usas la función `fold` o todavía a más alto nivel la función `sum` en la que no tienes que hacer nada tú mismo. Sin duda estas abstracciones te pueden ayudar a ser más productivo, y lo mejor es que no tienes que pagar con rendimiento por ellas. Sabemos que las comidas gratis [no existen](https://en.wikipedia.org/wiki/There_ain%27t_no_such_thing_as_a_free_lunch), ¿quién o dónde se paga el costo de estas abstracciones? **Es el compilador** quien se encarga de que estas formas más fáciles de programar no te cuesten nada en tiempo de ejecución, por lo tanto, te costarán en tiempo de compilación.

Esto es un tema un poco controversial porque hay quienes dicen que estas no existen, pero yo creo sinceramente que su costo es tan bajo que podemos considerarlo como costo cero, además con las ganancias en productividad que se obtienen, se puede considerar como una ganancia neta.

> Rust resuelve puntos dolorosos presentes en muchos otros lenguajes, dando un sólido paso adelante con pocas desventajas - Jake Goulding

### Comunidad

La comunidad de Rust es vibrante y cada vez crece más. Rust cada vez se usa en más lugares y más empresas lo respaldan, es como una bola de nieve que se va haciendo cada vez más y más grande. Mi predicción es que la comunidad seguirá creciendo y desarrollando tanto Rust como paquetes y cosas prefabricadas para que sea cada vez más fácil crear software con Rust.

### Desventajas

Rust, como todo, no es una solución mágica que vaya a resolver todos los problemas de la creación de software como si fuera un hechizo mágico. Algunas de las desventajas que le veo son:

1. **Novedad.** Al ser un lenguaje tan nuevo, no hay tantos recursos desarrollados como para C, C++, Java o Python. Probablemente muchas de las cosas que hagas si trabajas en un dominio muy específico, las tendrás que programar desde cero o componer bugs al no haber tantas manos probándolo por mucho tiempo como en otros lenguajes.

2. **Dificultad de aprendizaje.** Rust tiene conceptos que no estamos acostumbrados a manejar en otros lenguajes. Simplemente, uno de sus conceptos básicos, el de préstamos y pertenencia, es algo que a muchos programadores nos costará trabajo. El sistema de tipos y la dificultad de que algo compile es algo más que se escucha por ahí respecto a la dificultad de aprender y usar Rust.

3. **Está siendo desarrollado muy activamente.** Esto puede ser tanto una ventaja como una desventaja, pero sin duda lo es para la estabilidad de tu código. Si algo cambia en una nueva versión del compilador, vas a tener que hacer un gran cambio en tu base de código o quedarte con tu versión atrasada. Por el lado bueno, a tu lenguaje base se le estarán agregando siempre nuevas y mejores funciones.

Finalmente, puede que no _necesites_ las cosas que te ofrece. El esfuerzo extra que tendrás que poner para hacer que el compilador acepte tus programas puede que valga la pena si el rendimiento, la seguridad en memoria o el acceso a bajo nivel no son algo que distinga a tu software, así que no te dejes llevar el miedo a perderte algo que no necesitas. Si estas haciendo un prototipo que tiene que salir lo más rápido posible, tal vez Rust no sea la mejor elección, por ejemplo.

## Conclusión

Rust es un lenguaje de programación moderno que ofrece grandes características para poder desarrollar software de diferentes niveles, desde sistemas a aplicaciones web, e incluso frontend con [WebAssembly](https://webassembly.org/). Puede que sus características de seguridad, rendimiento y productividad (por lo menos comparado con C++) sean una razón suficiente para que quieras aprenderlo.

Como desarrollador, también puedes pensar que Rust seguirá creciendo en popularidad y puede que el número de desarrolladores necesitados aumente en los próximos años, por lo que aprenderlo te abriría las posibilidades de encontrar buenos trabajos y bien pagados.

En los próximos artículos hablaremos de las herramientas ya desarrolladas para facilitar el trabajo con Rust, es decir, su entorno Open Source y también de recursos para aprender Rust. ¿Qué piensas? ¿Valdrá la pena aprenderlo?
