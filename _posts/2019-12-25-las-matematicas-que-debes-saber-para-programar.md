---
title: "Las matemáticas que debes saber para programar"
date: 2019-12-25
author: Héctor Patricio
tags: math matemáticas aprender
comments: true
excerpt: "¿Qué tantas matemáticas necesitas para programar? En este artículo lo veremos."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_fill,g_custom,h_1000,w_1400,x_0/v1586794249/7CD56C0C-C8F6-448E-891B-348469AAF598_h9jpih.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_fill,g_custom,h_1000,w_1400,x_0/v1586794249/7CD56C0C-C8F6-448E-891B-348469AAF598_h9jpih.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Cuando se habla de **matemáticas** muchas personas prefieren cambiar de tema.

Pero las matemáticas son la base de muchas otras ciencias incluida la computación. Podríamos considerar las ciencias de la computación como **una rama de las matemáticas**, pero que ha evolucionado todavía más allá de ellas.

Para programar con eficacia no necesitas saber muchas matemáticas, con el entendimiento básico es suficiente. En este artículo hablaremos de aquello que debes dominar.

Si ya programas, ya _usas_ matemáticas. Saber más te ayudará a programar mejor, pero para eso necesitamos saber qué matemáticas necesitas. Antes, hagamos un esfuerzo por _entender_ qué son las matemáticas.

## ¿Qué son las matemáticas?

**Definir las matemáticas es difícil.** Según lo que (de manera _muy irresponsable_) nos han enseñado en la escuela, las matemáticas son el tratamiento de los **números**. Eso está muy lejos de la realidad, y ya te habrás dado cuenta si has avanzado lo suficiente en esta área del conocimiento.

Es cierto, las matemáticas más elementales se pueden reducir a números, pero no es su centro, el espíritu de su estudio.

Algunas definiciones que encontré útiles:

> Las matemáticas son la manera que tenemos de elevar a la categoría de un arte nuestros **esfuerzos cognoscitivos**. - **Fausto Ongay**

Ongay también menciona que la etimología de la palabra matemáticas tiene que ver con **conocer o saber**. Así, en cierta medida las matemáticas se pueden pensar como la ciencia **de la certidumbre**. Es decir, de saber algo con certeza y poder verificarlo.

> La matemática, como una expresión de la mente humana, refleja la voluntad activa, la razón contemplativa, y el deseo de la perfección. Sus elementos básicos son: lógica e intuición, análisis y construcción, generalidad y particularidad. - **Richard Courant**

En esta definición más abstracta se mencionan los elementos usados para lograr su cometido: lógica, intuición, análisis, construcción (o síntesis), generalidad (inducción), particularidad (deducción). Ya hablamos un poco de esto en los artículos acerca de las idea de [George Polya](http://bit.ly/39madQm).

Si quieres adentrarte en esto el libro [**¿Qué son las matemáticas?**](http://bit.ly/2F4Dn8N) habla de ello a fondo.

Pero no estamos aquí para filosofar acerca de las matemáticas. Lo único que quiero quede claro con esto es que las matemáticas no tienen que ver con sólo con **números**, sino con el _razonamiento_, _certidumbre_ y resolución de problemas.

## Matemáticas Básicas

Empecemos hablando brevemente de las matemáticas que debes conocer como programador y como ser humano funcional.

### Operaciones básicas

Saber operar con números en la vida cotidiana es una habilidad que todos necesitamos. Pero más importante aún es entender el significado de estas operaciones:

- ¿Qué significa **una multiplicación**?
- ¿Qué significa **una división**?
- ¿Qué significado tiene el **elevar un número a una potencia**?

Entender esto te ayudará a **resolver problemas** que es la actividad principal que se realiza cuando programas. Todo lo demás está alrededor de esto.

### Probabilidad y estadística

Tener las nociones de estas áreas es una de las herramientas más útiles a la hora de resolver problemas y sobre todo atacarlos prácticamente. Varias de las áreas de la ciencia de la computación basan sus resultados y procesos en estas dos áreas.

Un ejemplo es la **criptografía**: los algoritmos de cifrado como **AES** trabajan con una llave que es usada para cifrar y descifrar el mensaje. Asignar el tamaño de la llave depende totalmente de la _probabilidad_ de que un atacante sea capaz de adivinar la llave en un número de intentos razonable.

Ahora imagina que la llave tiene 128 bits de longitud. Aquí entra otro par de conceptos importantes para la computación.

### Combinaciones y permutaciones

¿Cuál es el número de llaves diferentes que se pueden generar con 128 bits? La respuesta es: 2^128 (2 elevado a la potencia 128). _¿Cómo llegamos a esa respuesta?_ Esto se conoce como **conteo** en matemáticas y las bases son la **permutación** y la **combinación** de elementos. En este caso es la permutación de 2 elementos que permiten repetición en 128 lugares.

¿Qué probabilidad hay de que alguien encuentre esa llave por suerte en el primer intento?

La respuesta es 1/2^128. Tan cerca de cero para ser considerada prácticamente imposible de adivinar incluso en un número de intentos razonable.

La criptografía y varias áreas están llenas de probabilidad y estadística (como el aprendizaje automático y el análisis de datos, aunque más avanzadas).

Si sientes que necesitas un recordatorio aquí hay un curso que enseña desde lo más básico: [Conteo, combinaciones y permutaciones en Khan Academy](http://bit.ly/2rrL4mb). Este también es un curso que enseña probabilidad y estadística desde cero.

## Lógica (Matemáticas discretas)

Las matemáticas discretas son una de las áreas más abstractas de las matemáticas cuando las vemos en papel pero en realidad tratamos con ellas a diario. Podemos definir las matemáticas discretas como _el estudio de las cosas que se pueden contar, sean finitas o infinitas_.

La **lógica** es uno de los campos de estudio de las matemáticas discretas. Se enfoca en estudiar **el razonamiento** y sobre todo _si el razonamiento es **correcto**_.

Para lograr esto la lógica se vale del estudio de las **proposiciones** (o afirmaciones) y sus relaciones. Una proposición es un enunciado que dice algo que puede ser _verdadero_ o _falso_. En matemáticas se dice que tiene un **valor de verdad**.

Dos proposiciones se pueden relacionar mediante un _conector_ (en electrónica: compuertas lógicas, en programación son operadores booleanos). Los conectores más conocidos son el **or** (o) y el **and**(y).

Esto da origen a demostraciones tanto matemáticas como prácticas. En el desarrollo de sistemas se pueden usar para demostrar que tu algoritmo o solución es correcto, es decir, va a funcionar con los datos de entrada propuestos que cumplan con los valores de verdad.

¿Son absolutamente necesarias para programar? Las demostraciones no, pero serán útiles si quieres crear demostraciones de que un algoritmo funciona sin tener que crear miles de ejemplos que convenzan a alguien. **Lo que sí es necesario entender es el funcionamiento de los conectores lógicos, no hay programa que se escape de ellos.**

### Conjuntos

El estudio de los conjuntos es una parte de las matemáticas discretas que se enfoca en estudiar elementos (objetos) que se agrupan por alguna característica en común. Los conjuntos son de gran utilidad para resolver muchos problemas matemáticos y la criptografía actual esta fuertemente basada en algunos problemas que tienen que ver con el cálculo de ciertos conjuntos.

¿Me sirve para trabajar en el día a día? Para cierto tipo de problemas es más cómodo trabajar con conjuntos que con los tipos de datos comunes de colecciones a los que estamos acostumbrados los programadores. Tratar tu colección (lista, tupla, etc.) como un conjunto matemático te permitirá efectuar operaciones como la **intersección de conjuntos** (elementos en común), la **unión** (todos los elementos únicos encontrados en dos o más conjuntos). Si el lenguaje de programación tiene este tipo de dato te va a dar un buen empujón.

Por cierto, el resultado de las consultas en SQL (lenguaje de manejo de datos para la mayoría de las bases de datos) se comportan como conjuntos matemáticos.

¿Quieres aprender matemáticas discretas? Aquí tienes un pequeño curso: [Curso de matemáticas discretas](http://bit.ly/2EWToND).

Eso es todo lo que necesitas para programar básicamente. Mientras mejor seas en estos campos, mejor podrás aprovecharlos para programar mejor o para entender mejor los programas de otros.

### Sistemas numéricos

Los sistemas numéricos son un tipo de conjuntos que se conforman de todas las cifras que pueden formarse con una cantidad determinada de símbolos que representan los números. El número de símbolos le da nombre al sistema: si hay dos símbolos (0, 1) es binario, si hay tres (0, 1, 2), ternario, etc.

Para programar es muy conveniente que entiendas básicamente cómo se define un sistema numérico y que conozcas por lo menos cuatro:

- **Decimal**. Incluye los símbolos que conocemos como dígitos (0, 1, 2,.., 9). Su base es el 10.
- **Binario**. Es el sistema numérico con el que los microprocesadores pueden trabajar. Por eso es importante conocerlos. Sólo se pueden usar dos valores: 0 y 1.  Su base es el 2.
- **Hexadecimal**. Se usa por conveniencia para representar números binarios de manera abreviada, por su compatibilidad entre bases (16 = 2^4). Su base es el 16 y los símbolos o valores extra que incluye a parte de los dígitos comunes son las letras de la A a la F.
- **Octal**. Su base es el 8 y también se usa para abreviar números decimales. Usa los dígitos del 0 al 7.

El sistema decimal lo usamos en la vida diaria. Con entender básicamente el binario y hexadecimal estarás bien.

## Matemáticas avanzadas y especificas

En muchas áreas de la programación se usan matemáticas más avanzadas, sobre todo en áreas que están sonando mucho recientemente: análisis de datos e inteligencia artificial. Si quieres entender a fondo estas y otras áreas del desarrollo de sistemas, es conveniente tener un conocimiento amplio en algunas de las siguientes áreas:

- **Probabilidad y estadística avanzada**. Saber acerca de variables aleatorias, distribuciones de probabilidad, análisis Bayesiano, etc. Esto te permitirá analizar datos tanto exploratoria como predictivamente.
- **Álgebra lineal**. El álgebra y la resolución de ecuaciones que representan líneas en el plano cartesiano. Esto te ayudará a tratar con conjuntos de datos. Muchas de los resultados de los algoritmos de Machine Learning son ecuaciones lineales.
- **Ecuaciones diferenciales**. Esto es la resolución de sistemas de ecuaciones y sus derivadas. Esto tiene aplicaciones en todo lo que tenga que ver con cambios respecto a alguna variable, como el tiempo.

Hablé de los campos finales pero para entender esto debes tener conocimiento previo:

- Geometría Analítica
- Álgebra
- Trigonometría
- Cálculo Integral y diferencial
- Cálculo Vectorial

Por suerte, para los campos de los que habla arriba no tienes que saber todo esto, a menos que quieras ser el desarrollador de los algoritmos originales. Generalmente somos usuarios de bibliotecas creadas por genios que ya hacen lo que necesitamos.

## No te preocupes

Saber matemáticas avanzadas no es necesario para ser ser un programador exitoso si tu campo de desarrollo no lo necesita dentro de su dominio. Por supuesto que aprender cosas así de difíciles te hará más hábil para resolver problemas, tal como saber física o química avanzada te harían más hábil.

Fuera de las matemáticas básicas y un control decente e intuitivo de la lógica, no es necesario que seas [Terence Tao](http://bit.ly/2StKLCz), a menos que el campo en el que estés trabajando esté directamente relacionado con eso, tal
como tendrías que saber lo suficiente de finanzas si estuvieras haciendo una app financiera o de administración de empresas si estuvieras haciendo una aplicación o plataforma para este campo.

Aquí hay un video curso en el que se explican más ampliamente lo que algunos llaman ["matemáticas para programadores"](http://bit.ly/2rvD6Zi).
