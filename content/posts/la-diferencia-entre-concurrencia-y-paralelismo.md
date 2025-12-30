---
title: "La diferencia entre concurrencia y paralelismo"
date: 2019-04-17
author: "Héctor Patricio"
tags: ['concurrencia', 'paralelismo', 'go', 'elixir']
categories: ['comments:', 'true']
description: "Muchos programadores confunden la concurrencia con el paralelismo, aunque son conceptos que se relacionan, no son lo mismo"
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1555480885/zhipeng-ya-348674-unsplash_lgerdr.jpg"
draft: false
---

Los términos **concurrencia** y **paralelismo** siempre han sido relevantes en el entorno de la computación y desarrollo de software. Hablemos de la diferencia entre ellos y cómo podemos aplicarlos en nuestros programas.
Son conceptos relacionados, pero decir que uno es el otro es como decir que las naranjas y manzanas son iguales.

Empecemos por el concepto más sencillo: el paralelismo.

## Paralelismo

Se refiere a la **_ejecución simultánea_** de varios procesos computacionales. Esto significa que se requieren varios medios de ejecución física: varios procesadores (o un procesador con varios núcleos) o varias computadoras (sistemas distribuidos) y la suficiente memoria para mantenerlos. Los procesos pueden estar relacionados entre ellos, para realizar una misma tarea, **o no**.

El paralelismo está relacionado con la capacidad del sistema en el que se ejecuta el programa, con sus recursos disponibles y que el software lo pueda aprovechar.

[Rob Pike](https://en.wikipedia.org/wiki/Rob_Pike), uno de los creadores del lenguaje Go, dice que el mundo real es paralelo. Y pensemos un poco: suceden muchas cosas al mismo tiempo, algunas relacionadas entre ellas, otras no.

Veamos algunos ejemplos concretos de paralelismo en la vida real.

#### El torneo de ajedrez

Imagínate un torneo de ajedrez en el que entran 100 personas a participar pero tiene como límite de tiempo un día. Para lograr terminar a tiempo se tienen que jugar varias partidas _simultáneamente_. Aunque una partida no afecta el resultado de otra que se esté jugando al mismo tiempo, esas partidas sí afectan partidas futuras si el torneo se pensó en varias etapas. La cantidad de partidas simultáneas que se puedan jugar dependerá tanto del número de jugadores como de los recursos disponibles: lugares, para jugar, tableros, conjuntos de piezas, etc, y del diseño del torneo. Esto es un ejemplo de paralelismo con procesos relacionados.

#### Un grupo musical

A menos que sea el hombre orquesta, una persona no puede tocar todos los instrumentos para producir una canción compleja. Cada miembro del grupo toma un instrumento y se encarga de producir las notas correctas en el momento adecuado. Esto es otro ejemplo de un proceso paralelo con tareas relacionadas entre sí.

#### Un grupo tomando clase

Ahora piensa en un profesor que imparte clases a sus alumnos. Cada alumno tomando notas es un proceso corriendo al mismo tiempo. Un alumno produce sus propias notas con su estilo y contenido para consulta posterior. Esto es un ejemplo de paralelismo con tareas no relacionadas, ya que las notas de todos los alumnos no tienen por qué converger.

### Ejemplos de programas paralelos

Hablemos de algunos sistemas y programas que pueden o necesitan ejecutar tareas en paralelo.

1. **Las computadoras actuales**. Las computadoras actuales en general cuentan con un procesador con por lo menos dos núcleos. Cada núcleo es capaz de correr un proceso por lo que esa computadora, si el software lo aprovecha, puede correr dos procesos a la vez. Insistimos: los procesos no necesariamente están relacionados.

2. **Red de Bitcoin**. Cuando se crea un nuevo bloque en el blockchain de la red de Bitcoin, muchas computadoras, llamadas "mineros", compiten para encontrar la solución a un problema matemático para el que se requiere gran capacidad de cómputo. Todas empiezan al mismo tiempo y la primera que termine gana una cantidad de bitcoins por haber encontrado la solución. Entonces: las computadoras trabajan en paralelo _compitiendo_ para encontrar una solución lo más rápido posible.

3. **Sistemas web modernos**. Casi todos los sistemas web modernos que tienen que atender a una cantidad considerable de usuarios ocupan varios sistemas computacionales para poder responder las peticiones en un tiempo razonable. La primera división que se hace generalmente tiene que ver con la base de datos y el programa encargado de recibir y procesar las peticiones web. Al trabajar en computadoras diferentes que pueden funcionar al mismo tiempo, se vuelve un sistema paralelo. Algunas arquitecturas más complejas incluyen un _balanceador de carga_, que distribuye las peticiones a diferentes computadoras encargadas de procesar las peticiones, y se levantan tantas como se necesiten.

Como decíamos al principio, casi todos los sistemas computacionales modernos se valen del paralelismo para funcionar decentemente. Ahora pasemos a hablar de un concepto un poco menos fácil de entender.

## Concurrencia

Esta palabra intuitivamente la entendemos como la confluencia o el encuentro de varias cosas o procesos en un sólo lugar al mismo tiempo. Cuando un lugar está lleno de gente decimos que "está muy concurrido". Esto nos puede llevar a confundir el término con paralelismo. En cuanto a las ciencias computacionales, es algo totalmente diferente: es una manera de diseñar, componer o estructurar programas. **Concurrencia**, entonces, se puede definir de la siguiente forma:

> La composición de elementos (funciones, procesos, programas, etc) que se ejecutan independientemente pero **interactúan** entre sí. No necesariamente se ejecutan al mismo tiempo.

Hablamos de composición en el sentido de "acomodo" o "estructura" e incluso "diseño".

Por lo tanto, un programa concurrente es uno que se vale de distintos procesos indpendientes para lograr su objetivo, que pueden o no correr al mismo tiempo exactamente.
Pongamos unos ejemplos de la vida real.

#### El podcaster

Piensa en una persona que quiere grabar un podcast. Para facilitarse la vida ha escrito su proceso en una lista de tareas:
1. Crear borrador de los temas y el script
2. Grabar el episodio
3. Editar y decorar el episodio
4. Publicarlo en los sitios de podcast mas populares

¿Son estos procesos independientes? Lo cierto es que cada uno necesita una entrada (que PUEDE venir del proceso anterior), pero no necesariamente la entrada producida por el proceso anterior. Es decir:

1. Crear el borrador -> Independiente
2. Grabar el episodio -> Puede o no ocupar un borrador, es mejor idea tener uno.
3. Editar -> Requiere una grabación que editar y decorar y produce un episodio final.
4. Publicar -> Requiere un episodio que publicar

Por lo tanto, estos procesos se pueden ejecutar independientemente. Entonces, con estas tareas (y la manera de organizarlas) podemos tener un proceso de creación de podcasts concurrente. Imagina por ejemplo que el podcaster decide crear una parte del borrador, digamos 5 minutos, y grabarlos, sólo para escucharse a sí mismo y probar el tono y el _feeling_. Después repite la operación hasta tener 30 minutos de contenido. Este es un proceso que podemos decir que es concurrente porque aunque no podía grabar y escribir el borrador al mismo tiempo, estas tareas se estaban completando 'al mismo tiempo', no hizo una después de otra hasta completarla.

Imagínate el proceso algo así:

![Proceso del podcaster](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1555523914/IMG_0033_1_btpgl3.jpg)


Concurrencia es **manejar** varias tareas en un periodo de tiempo, aunque no se ejecuten simultáneamente. Pero podríamos hacer este proceso paralelo al integrar a más personas: una persona que escriba el borrador, empezando un poco antes que el encargado de hablar al micrófono comience. Así aceleramos el proceso. O los encargados de editar y publicar pueden estar trabajando en episodios anteriores
mientras se graba uno nuevo.


#### El ajedrecista

Ahora imagina a un Gran Maestro (GM) del ajedrez al que retan a enfrentarse con 10 personas a ciegas al mismo tiempo.
El ajedrecista acepta y juega contra los 10 formados en círculo. Para lograr esto (además de jugar muy bien ajedrez), el gran maestro debe establecer un orden para cada openente y, por lo menos en su mente, una manera de retomar cada juego cuando sea el turno. Las tareas (los juegos), vistos desde el lado del GM están relacionadas en el sentido de que cada una suma dificultad al encuentro, cada uno hace más difícil ganar al siguiente. Este proceso no puede paralelizarse porque perdería todo el sentido.


![El ajedrecista](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1555523924/IMG_0037_pkqalv.jpg)


#### Un equipo de trabajo

Pensemos en un equipo que tiene que desarrollar un programa más o menos complejo. El equipo está compuesto por un desarrollador backend, un frontend y un UX/UI. Además los coordina un administrador de proyectos (PM). El PM puede diseñar una forma de trabajo que permita a cada uno de los miembros trabajar en
diferentes partes del proyecto para avanzar más rápido. Para lograr esta coordinación se necesita trabajo extra: reportes, juntas y coordinación de tareas, para no empezar algo de lo que no se tenga claridad.

### Ejemplos de programas concurrentes

Ahora hablemos de algunos ejemplos de programas concurrentes, de la vida real:

1. **Sistema operativo**. Un sistema operativo ejecuta muchas tareas relacionadas entre sí para lograr que un sistema de hardware sea usable para los humanos, por ejemplo: leer entrada del ratón y el teclado, mostrar el resultado de los procesos en pantallas, ejecutar el reloj, ejecutar muchos programas que hacen de tu experiencia agradable (spotify, administrador de ventanas), servicios de red. Aunque las computadoras actuales tienen varios procesdores, no se acercan al número de tareas con las que un sistema opertivo **trata** al mismo tiempo. Como decíamos en la sección de paralelismo, actualmente casi todas las computadoras pueden correr varios procesos al mismo tiempo, por lo que puede que el sistema operativo se aproveche de esto. La siguiente ilustración es un ejemplo de cómo trataría en sistema operativo la entrada del texto "AB":

![Sistema operativo concurrente](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1555523897/IMG_0035_1_emhyju.jpg)


2. **Servidor Web**. Los servidores web están diseñados para atender a muchos clientes (usuarios) dentro de un corto espacio de tiempo. Un servidor web está tratando con varios usuarios al mismo tiempo sin que necesariamente todas sus tareas se ejecuten simultáneamente: atiende a cada usuario en muy corto periodo de tiempo y pasarse al siguiente. Puede funcionar en paralelo si cuenta con los recursos computacionales suficiente. Se parece al ajedrecista, "juega" con muchos usuarios al mismo tiempo, dividiendo sus recursos por tiempo.

3. **Navegador**. Un navegador web es un sistema naturalmente concurrente. Cada una las pestañas que tienes abiertas puede contar como una de las tareas con las que el pobre navegador web tiene que trabajar para mantenerte contento. No es necesario que esté corriendo el código de todas al mismo tiempo para funcionar, sino que usa métodos diversos para identificar exactamente qué debe estar ejecutando en cada instante.

Algo que debemos hacer notar es que un sistema concurrente generalmente realiza _**más trabajo**_ que uno secuencial, ya que tiene que coordinar las diversas tareas independientes y la utilización de recursos. Para lograrlo, existen varias técnicas, llamadas [modelos de concurrencia](https://stackoverflow.com/questions/4153118/list-of-concurrency-models).

## En el desarrollo del software

Los lenguajes tienen diferentes maneras de permitirte aprovechar los recursos de cómputo para crear programas concurrentes y paralelos:

- **Hilos (threads)**. La forma más común en que lo permiten es mediante hilos: subprocesos que se coordinan entre sí, que ocupan menos memoria que un proceso normal y comparten memoria con otros hilos y con el proceso padre.

- **Procesos**. Programas que corren en su propio espacio de memoria independientemente de otros procesos. Lo que hace un proceso no le afecta a otro, por lo que hay que diseñar y mantener maneras de comunicarlos.

- **Tareas y Futuros**. Estas son una abstracción sobre los procesos e hilos, que son los elementos más básicos de concurrencia. JavaScript con los callbacks (futuros), las promesas (futuros) y posteriormente con Async/Await (tareas) permiten crear programas que deben ser concurrentes.

## Conclusión

Como resumen:

> La concurrencia tiene que ver con el diseño del software, mientras que el paralelismo tiene que ver con la ejecución.

Por ejemplo, un sistema operativo es concurrente y aplica a diversas técnicas para coordinar todos los procesos que necesita para que logre hacer una computadora usable para los humanos. Este sistema no necesariamente es paralelo (y por mucho tiempo no lo pudieron ser), ya que si no cuenta con más de un medio físico para la ejecución simultánea de tareas o procesos recurre a técnicas de compartimiento de procesador que hacen que para los humanos parezca que ejecuta muchas tareas al mismo tiempo.

La concurrencia permite aprovechar sistemas que permitan ejecución paralela para lograr la tarea a la mano más rápidamente.

Saber crear sistemas concurrentes es una de las habilidades más importantes para un desarrollador moderno, independientemente del área en la que trabajes.

Gran parte del contenido de este post fue extraído de esta charla: [Concurrency is not Parallelism](https://blog.golang.org/concurrency-is-not-parallelism).
