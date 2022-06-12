---
title: "Resumen: Historia de los lenguajes de programación"
date: 2022-06-11
author: Héctor Patricio
tags: libros programming-languages
comments: true
excerpt: "Hablemos del libro 'Historia de los lenguajes de programación' de Manuel Rubio, que nos cuenta acerca del nacimiento de los primeros lenguajes."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1280/v1654281870/jr-korpa-9XngoIpxcEo-unsplash_c6yihq.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_320/v1654281870/jr-korpa-9XngoIpxcEo-unsplash_c6yihq.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

¿Te has preguntado cómo nacieron los primeros lenguajes de programación? Manuel Rubio, autor de ['Historia de los lenguajes de programación'](https://altenwald.com/book/histlangprog), nos habla lo explica de manera cronológica en el primer tomo de esta obra.

## Resumen general

El libro habla de manera más o menos cronológica del nacimiento de los primero lenguajes de programación, desde la época de 1940. La forma en que lo narra te hace comprender claramente por qué eran necesarios y las diferentes tendencias que se dieron.

El libro abarca hasta el año 1960, poco antes del nacimiento de Lisp. Hablemos ahora de las fases que el libro cubre a grandes rasgos.

## El nacimiento de la computación automática

El primer capítulo trata sobe el nacimiento de la computación como la conocemos, cómo **Alan Turing**, **Alonzo Church** definieron lo que conocemos como computable, gracias al ["Problema de la decisión"](https://paginas.matem.unam.mx/videos/2017/marzo-2017/seminario-junior/427-acerca-del-problema-de-la-decision), definido en los diez problemas del matemático David Hilbert.

Además habla de las contribuciones de [John Von Neumann](https://www.britannica.com/biography/John-von-Neumann) para el diseño y la concreción de las computadoras como medios físicos.

El segundo capítulo habla del camino independiente que tuvo **Konrad Zuse**, en la creación de máquinas automáticas para la computación de problemas lógicos y matemáticos. Habla de cómo hizo la **Z1, Z2 y Z3**, computadoras mecánicas, cada una mejor que la otra. Además habla de la creación de un lenguaje de programación teórico llamado **Plankalkül**.

Estos dos capítulos son muy interesantes porque nos ayudan a comprender cómo la computación automática es algo que estaba muy cerca de ser logrado por la década de 1930, por diferentes mentes y de formas parecidas.

## Los primero lenguajes que corrían en computadoras

Los siguientes capítulos nos van hablando de la progresión de los lenguajes de programación, todos guiados principalmente por dos cosas:

1. La capacidad de la computaras existentes, pero sobre todo, sus _límitaciones_.
2. La intención de los usuarios de la computadora.

No vamos a hablar de cada uno de los capítulos y lenguajes que se mencionan en el libro, pero hablemos de la progresión general que se fue dando y cómo se acercaban cada vez más los lenguajes que conocemos hoy.

Las primeras computadoras programables requerían que se recablearan, es decir, esta era su forma de entrada de información, sin embargo, se empezaron a crear tablas de instrucciones que ayudaban a programar. Tenemos por ejemplo el [ENIAC Short Code](https://hopl.info/showlanguage2.prx?exp=6030).

También, durante esta época empezaron a crearse cosas que damos por sentado, pero que seguramente surgieron naturalmente durante el trabajo del día a día de las primeras _programadoras_:

1. La **subrutina**, como una plantilla de código reutilizable a la que sólo se le agregaban los datos en lugares designados para ello.
2. El **punto de ruptura**, que es una pausa en la ejecución de un programa, para revisar el estado general del sistema y el programa.

Después de esto empezaron a nacer los primeros lenguajes _ensambladores_. Un lenguaje **ensamblador** es un conjunto de instrucciones apegadas al procesador que lo correrá, que sustituyen las instrucciones en binario y que para pasar a código máquina necesitan una fase de transformación, que los primeros programadores llamaban la fase de "ensamblaje". En este sentido, lo que conocemos como lenguajes ensambladores, debieron haberse llamado [_lenguajes ensamblados_](https://softwareengineering.stackexchange.com/questions/405080/why-is-assembly-language-called-assembly).

Estos lenguajes correspondían a su propia computadora y que por lo tanto, _no se podían usar en ningún otro lado_. Tenemos como ejemplo (y primer lenguaje ensamblador reconocido) el **ARC Assembly de Kathleen Booth**. Así surgieron más lenguajes de este estilo, cada uno para su máquina específica hasta la creación de los primeros intérpretes y compiladores.

## El primer intérprete

¿Qué nacio primero? Los compiladores o los intérpretes? Pues resulta que lo primero que permitió usar un lenguaje de alto nivel, es decir, algo no relacionado directamente con las instrucciones de específicas de un procesador, fue un **intérprete** propuesto por John Mauchly en 1949. Este fue llamado primero _Brief Code_ y después _Short Code_.

Un intérprete es un programa que transforma un lenguaje de alto nivel en código máquina, es decir, instrucciones para el procesador para el que este intérprete está implementado y además lo ejecuta.

**Short Code** fue un lenguaje pensado para representar y resolver expresiones matemáticas. Fue implementado para el **BINAC** en 1949 y para el **UNIVAC I** en 1950, por William Schmitt. Aquí empieza la historia de los lenguajes que no están pegados a la arquitectura de un procesador.

## El primer compilador

Una de las primeras programadoras, **Grace Hopper**, después haber estado programando de forma arcaica mucho tiempo, comenzó a crear una colección de _subrutinas_ para facilitarse el trabajo. Así que su trabajo se fue convirtiendo en juntar una serie de subrutinas que lograran la tarea en cuestión.

El siguiente paso natural, por lo tanto, fue la automatización de este proceso, de juntar o _compilar_ todas estas partes de código en un programa final. Así fue que nació el primer compilador, creado por Grace Hopper, el **A-0** para la [UNIVAC I](https://www.computinghistory.org.uk/det/5487/Grace-Hopper-completes-the-A-0-Compiler/).

Después de esto siguieron surgiendo compiladores, como el A-1, A-2, MATH-MATIC, ARITH-MATIC, por ejemplo. Estos lenguajes y compiladores surgieron por las diferentes necesidades de las empresas que poseían una computadora y un equipo capaz de desarrollar estos lenguajes.

### Fortran I y II

La mayor desventaja de los lenguajes creados en la década de los 50's es que representaban un gran intercambio entre velocidad _de programación_ por velocidad _de ejecución_. Es por eso que **John Backus** hizo la propuesta de un lenguaje que fuera fácil de programar, y por lo tanto de enseñar, y que al mismo tiempo no representara una gran diferencia en velocidad de ejecución.

Así presentó el informe sobre FORTRAN (**FOR**mula **TRAN**slator), en el que se mencionaban justo estas dos fortalezas: escribir en alto nivel fórmulas matemáticas al mismo tiempo que compilar un programa muy eficiente en ejecución para la computadora **IBM 704**.

Aquí se empiezan a ver las malas capacidades de estimación de los desarrolladores: John Backus dijo que la implementación primera versión tomaría 6 meses, pero en realidad tomó 2 años y medio, 5 veces más.

Sin embargo, el resultado de FORTRAN como producto fue impecable: a diferencia de los demás compiladores y lenguajes tenía una muy buena documentación que permitió su adopción masiva, convirtiéndose en la mejor arma de IBM para vender más computadoras, y en el estándar en América (sobre todo Estados Unidos) para la industria, debido a que después de implementó para otras computadoras de IBM.

### Algol 58

Aunque FORTRAN había tenido mucho éxito como lenguaje en la industria, no había un lenguaje estándar para hacer computación científica, ni en América ni en Europa, por lo que no se podían compartir los resultados ni los programas entre universidades ni instituciones.

Así nació la iniciativa de crear un lenguaje estándar para la industria y la academia, que permitiera compartir los resultados entre diferentes grupos de personas. La GAMM ([Gesellschaft für angewandte Mathematik und Mechanik](https://www.gamm-ev.de/en/) [Asociación de Matemáticas Aplicadas y Mecánica]), que es el equivalente a la ACM ([Association for Computing Machinery](https://www.acm.org/) [Asociación de Mecánica Computacional]) se pusieron de acuerdo para crear una especificación de un lenguaje que sirviera este propósito, reuniendo personas con mucha experiencia en la creación de lenguajes y en la programación de compiladores.

El resultado de esto fue el **International Algebraic Language**, después conocido como **ALGOL**. Este lenguaje tenía las mejores características de los lenguajes modernos de aquella época, sin embargo, tenía un serio problema: sus implementaciones eran inconsistentes, por lo que no pudo cumplir su objetivo de tener una herramienta estandarizada para crear y compartir programas.

La creación de esta recomendación, sin embargo, estableció las bases de cooperación entre las asociaciones relacionadas con la computación de Europa y América.

### COBOL

Hemos estado hablando de lenguajes usados para computación científica y cálculos matemáticos, sea en la academia o en la industria. **Grace Hopper**, una gran visionaria por lo que podemos ver, se dio cuenta de que los negocios necesitaban ayuda con cosas más mundanas: contaduría, inventarios, etc. De hecho, en retrospectiva, eso es algo que se estaba notando con lenguajes como [FLOW-MATIC](https://en.wikipedia.org/wiki/FLOW-MATIC) y [AIMACO](https://en.wikipedia.org/wiki/AIMACO), especializados en tareas de procesamiento de datos, menos científicos y con instrucciones más adaptadas al mundo de los negocios.

Así que **Hopper** se dio a la tarea de juntar a la gente necesaria para diseñar un lenguaje que cumpliera con estas características y que detuviera la proliferación innecesaria de lenguajes de negocio. Así nació el comité para diseñar **COBOL**, un lenguaje que cumpliera con las necesidades de las empresas.

COBOL, en vez de enfocarse en matemáticas y fórmulas se enfocaría principalmente en palabras en inglés para hacerlo más fácil de programar y aplicar a las necesidades del día a día de los negocios. En el libro de Manuel puedes ver los detalles y los retos a los que tuvo que enfrentarse este comité.

La especificación de COBOL se terminó en 1960, pero su implementación se tomó otros años. Para mi, COBOL es el lenguaje que precede a la gran mayoría de los que usamos hoy, como Java, Python, PHP, etc., ya que estos están enfocados en problemas de negocio más que en computación científica o matemática.

### Otros lenguajes

No mencioné un montón de lenguajes, compiladores y computadoras que Manuel toca en libro, por lo que te recomiendo su lectura si quieres una visión más amplia del desarrollo de nuestra industria desde su nacimiento, la evolución de las necesidades y cómo los comercios, la academia y el gobierno se conjuntaron para ir creando lo que se fue necesitando hasta llegar al rico entorno que tenemos hoy.

## Aprendizajes

Este libro, más allá de contarte la historia de la programación entre los años 1940-1960, te comunica varias lecciones que puedes aprender si lees entre líneas. A continuación listo mis aprendizajes.

### Perseverancia

La historia de **Konrad Zuse** me enseña que no siempre es necesario estar con un grupo de personas pensando igual o siquiera que te entiendan para crear algo.

**Konrad** persiguió sus intereses con perseverancia y logró cosas muy parecidas a lo que los grupos de principales de desarrollo de la computación lograron años después. Claro, él es una excepción, pero es una muestra de qué tan lejos te pueden llevar tus intereses.

### Acerca de los equipos de trabajo

Para crear algo que vale la pena, como un lenguaje de programación, que es una creación bastante compleja, casi siempre hace falta la cooperación de muchas personas por un periodo sostenido (como ya vimos, hay excepciones). En por lo menos dos de los lenguajes mencionados arriba, se tuvieron que poner de acuerdo múltiples grupos de personas para lograr un objetivo común, como crear un lenguaje que cubriera las necesidades de un grupo amplio de personas e instituciones y evitar problemas estilo la "Torre de Babel".

### Vender las ideas

Una de las cosas que se menciona en el libro es que **"la gente es alérgica al cambio"**. Esto pasó con la idea primeramente de hacer intérpretes y después de los compiladores.

Es por eso que las personas que tuvieron la idea inicialmente tuvieron que luchar porque otras personas tomaran sis ideas en serio, convencerlas de que valía la pena y poner de acuerdo a un grupo de personas.

Tener la habilidad de **vender tus ideas** es algo que te ayudará a avanzar en tu carrera y conseguir tus objetivos.

### Siempre habrá celadores

Cuando se presentaban ideas que permitían abrir el campo hacia personas menos educadas que las que ya estaban, o que quitaban barreras para que otros programaran, siempre había personas que se sentían amenazadas y se oponían a esto.

Esa es una actitud que seguimos viendo hasta hoy. Hay muchos "profesionales" que desprecias a las personas que no son tan educadas como ellos o que entran en el campo del desarrollo de software sin educación formal.

Podemos ver en retrospectiva lo equivocados que estaban y podemos entender lo equivocados que están hoy los que tienen la misma actitud.

## Conclusión

El primer volumen de "Historia de los Lenguajes de Programación" es un libro que te puede enseñar mucho sobre tu industria y te puede dejar muchas lecciones. Lo recomiendo mucho a todos los desarrolladores de software que tengan interés en la historia y la filosofía de lo que hacen día a día y creo que debería ser una lectura obligatoria para todos los estudiantes de carreras afines a la computación.

Aquí nos puedes ver platicando con el autor y como bonus tenemos a Camilo Chacón Sartori como invitado, platicando de su libro [Mentes Geniales](https://www.youtube.com/watch?v=FgbJdgBFS58):

<iframe width="560" height="315" src="https://www.youtube.com/embed/xYClAk5LDyo" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

---

Puedes comprar aquí el libro por sólo 12 Euros: [Historia de los lenguajes de programación, Años 1940-1959](https://altenwald.com/book/histlangprog).
