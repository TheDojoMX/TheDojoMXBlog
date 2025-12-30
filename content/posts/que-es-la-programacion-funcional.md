---
title: "¿Qué es la programación funcional?"
date: 2019-03-30
author: "Héctor Patricio"
tags: ['fp', 'functional-programming', 'programación-funcional', 'elixir']
categories: ['comments:', 'true']
description: "¿Por qué se ha escuchado tanto de la programación funcional recientemente? En este artículo la explicamos de manera concisa."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1280/v1553485527/john-moeses-bauan-690280-unsplash_atpm3w.jpg"
draft: false
---

En los últimos años ha estado cobrando relevancia (de nuevo) la **programación funcional**. ¿Qué diferencias tiene con los estilos más usados?
En este artículo hablaremos de sus dos caracterísitcas más distintivas y el tipo de programas que se pueden crear con ella.

## Definición

Se puede definir la programación funcional así:

> Estilo de programación en el que se usan principalmente **funciones puras** y valores **inmutables**. En los lenguajes funcionales, todo es una expresión, es decir, todo tiene un valor inmutable.

Eso es todo, todas las demás cosas que lees cuando se menciona la programación funcional se derivan de estas dos características. Ahora tenemos que definir estas dos características y ver como nos proporcionan amplias capacidades para crear programas altamente legibles, rápidos y que pueden procesar grandes cantidades de datos.

## Funciones puras

Una función pura es una que no hace referencia a nada fuera de ella para trabajar. En los lenguajes que pueden usar el estilo funcional, todo se puede tratar como si fuera una función.
Los ejemplos esta vez los pondremos en JavaScript, ya que es el lenguaje más común en el que la programación funcional está teniendo auge.

```javascript
tasaIVA = 0.16;

/*
Función impura
*/
function calcularIVA(subtotal) {
  return subtotal * tasaIVA; // tasaIVA está definido fuera del ámbito de esta función
}

/* Esta función es pura */
function calcularIVAPura(subtotal, tasa) {
  return subtotal * tasa;
}
```

La primera función, `calcularIVA`, toma una variable que está fuera de ella para calcular su resultado. Esto es poco recomendable por varias razones, entre ellas:
* Si vemos la función por separado, tener uno o varios valores que no sabemos de dónde vienen hace el código poco mantenible y entendible.
* Si alguna parte del código modifica el valor sin que nos demos cuenta, nuestros cálculos serán erróneos.
* Modificar los datos que están afuera y saber exactamente a todo lo que vamos a afectar cuando el programa crezca es muy difícil.
* Los más importante: **las funciones no dependen del contexto de ejecución, sólo de sus parámetros**.

En cambio, la función `calcularIVAPura` es una función que no depende de valores que no sabemos de dónde vienen para trabajar. Tiene la característica de que siempre que la llamemos con los mismos argumentos, va a devolver el mismo valor. Tampoco modifica nada en el exterior. Cuando modifiquemos un valor sabemos exactamente a qué vamos a afectar.

Veamos ahora una a una de las ventajas que proporciona usar funciones puras.

### Transparencia referencial

Dentro de un contexto en el que se use la función, sabiendo que la función siempre que sea llamada con ciertos parámetros devolverá lo mismo, *podemos sustituir la función con su valor directamente*. Esto nos permite crear programas más legibles inicialmente.

La tranparencia referencial hace que las funciones sean *cacheables* (a través de técnicas como la programación dinámica y la [memoización](http://nereida.deioc.ull.es/~lpp/perlexamples/node170.html)) y *predecibles*: al saber que una función llamada con los mismos parámetros devolverá lo mismo, podemos almacenar ese valor en vez de volver a llamar la función y usarlo directamente. Si la función es costosa en tiempo o procesamiento, el cachearla hará nuestro programa más eficiente.

<!-- ¿Qué ventajas da esto, podrías preguntarte? Pensemos en algunas cosas que propociona la transparencia referencial: -->

### Evaluación diferida (*lazy evaluation*)

Para los lenguajes funcionales más puros, todo se puede tratar como una función. Al saber que las funciones no dependen del contexto para funcionar correctamente, puedo evaluarlas ahora mismo o más tarde. Para evitar procesamiento innecesario, los lenguajes funcionales difieren la evaluación de las funciones y valores hasta que realmente se requiera el valor para alguna otra operación. Mientras el valor está sólamente definido, sin haber sido procesado. La evaluación diferida es muy conveniente sobre todo al trabajar con colecciones de datos grandes u operaciones gigantes. Algunas de las ventajas de la evaluación diferida son las siguientes:

* **Ahorro en tiempo de procesamiento**. Si defino un valor que es una función que corre sobre una colección de un millón de elementos, no tendré que esperar al procesamiento inicial porque no lo hará hasta que realmente ocupe los valores. Si por alguna razón no se ocupa ese valor más adelante en el programa, ese procesamiento ya nos lo ahorramos definitivamente.
* **Ahorro en memoria**. Cuando definimos colecciones muy grandes, los lenguajes con evaluación diferida no reservarán la memoria que van a ocupar inmediatamente, sino hasta que hagamos referencia a este valor para su procesamiento. De igual manera, si nunca se ocupó este valor o se canceló en algún punto del programa, nos ahorramos esa memoria.
* **Colecciones diferidas**. Algunos lenguajes de programación incluyen colecciones que nunca cargan en memoria todos lo valores que
van necisitar nunca, sino que los van generando uno a uno. Esto permite crear colecciones **infinitas** conceptualmente, o procesar conjuntos de datos muy muy grandes sin staurar la memoria.

Al preferir la evaluación diferida a la anticipada (eager), el estilo de programación funcional intenta evitar la iteración al máximo grado posible. Para trabajar con colecciones de datos u operaciones reptitivas se prefieren otras técnicas:

* **Recursividad**. La función se llama a sí misma con valores diferentes, produciendo eventualmente el resultado deseado.
* **Operaciones sobre colecciones y rangos**. Se busca aplicar funciones como `map`, que aplica una función a todos los elementos de una lista o `reduce` que transforma todos los elementos de una lista en uno solo.
* **Comprensión de listas (*list comprehension*)**. Se crean nuevas listas a partir de lo que parece la iteración de una colección. Muy parecido a como lo hace la función map, pero recibiendo el código directamente en vez de una función.

Esto permite que las operaciones sobre coleeciones sigan pudiendo ser evaluadas de manera diferida: no se aplican las funciones hasta que de verdad se necesita.

### Concurrencia

Lo repetimos: al no depender del contexto de de evaluación sino únicamente de sus valores de entrada, las funciones pueden ser corridas cuando sea y *donde sea*. Esto permite que las funciones puedan ser ejecutadas en un proceso concurrentes. Si el lenguaje de programción lo permite, estos procesos concurrentes se pueden ejecutar *paralelamente*.

Una aplicación de esto es el patrón [MapReduce](https://research.google.com/archive/mapreduce-osdi04-slides/index-auto-0002.html) que Google propuso para proceamiento de grandes cantidades de datos, y que es la base de [Hadoop](https://hadoop.apache.org/).

Por último, debemos notar que la concurrencia y el paralelismo se llevan bien, pero no son lo mismo. Para aclararlo te recomendamos la [siguiente plática de Rob Pike](https://blog.golang.org/concurrency-is-not-parallelism), uno de los creadores de el lenguaje Go (que no es funcional). Resumen: concurrencia es la composición de diferentes procesos independientes, mientras el paralelismo es la ejecución *simultánea* de estos procesos.

Como puedes ver, la programación funcional se posiciona como una muy buena opción para tratamiento y procesamiento de GRANDES cantidades de datos, y sus patrones han inspirado arquitecturas de procesamiento famosas.

Ahora hablemos de la segunda característica importante de la programación funcional.

## Valores Inmutables

Esta característica implica que todos los valores que se definen y almacenan en un programa son finales, no pueden ser modificados. ¿Cómo hacemos entonces para llegar a los valores que necesitamos? En un programa funcional, **siempre se crean nuevos valores a partir de los antiguos**. Esto implica que en un lenguaje funcional no existe el paso por referencia. Siempre que se pasa un valor a una función, se crea una copia independiente de estos valores. Tampoco existen las transformaciones "in place". Si quiero reordenar una lista, por ejemplo,  necesariamente crearé una nueva colección, esta vez con los valores ordenados, manteniendo la colección original intacta.

En general en los lenguajes funcionales todo es una expresión, es decir: *cada cosa que se pueda escribir tiene un valor inmutable*.

¿Cómo ayuda que los valores sean inmutables?

### Existencia de funciones puras

Al no permitir que un elemento externo modifique los valores que se han pasado, podemos estar seguros que los datos de la función permanecerán intactos. En lenguajes que permiten la modificación de los tipos de datos compuestos (diccionarios, listas, arrays o tuplas) es posible que alguien modifique un valor que se le pasó a la función sin que nos percatemos, pero la inmutabilidad lo previene.

### Independencia de ejecución

Tener valores que no van ser modificados por ninguna razón habilita la independencia de ejecución tanto en tiempo como en espacio. En tiempo de ejecución podemos mandar a ejecutar la función en otro procesador o máquina completamente diferente o diferir su ejecución hasta que sea necesario.

### Código legible y menos errores

Nunca más en la vida (mientras uses FP) volverás a dudar si una función devuelve el valor o lo modifica en la misma variable. Evitarás todos esos errores en los que pensabas que una función devolvía algo modificado y en realidad no devolvía nada no pasarán más.

Por supuesto que este depende del lenguaje, pero tú mismo puedes seguir los mismos principios en tu código si usas un lenguaje como JavaScript que no es completamente fucnional pero permite aplicar los ideas principales.


## Cómo hacer programas usables

Todos los programas útiles escriben en memoria, pintan algo en la pantalla, consultan una base de datos o un servicio web o mandan una respuesta HTTP. Si las funciones puras no deben tocar nada del exterior, ¿cómo hacer un programa que tenga un uso?

Los programas escritos con lenguajes o en un estilo funcional usan *principalmente* funciones puras para su diseño, pero no son el único tipo de funciones que ocupan, justo para permitir la entrada y salida de datos del sistema. Lo importante es separar las funciones que lo hacen de las que son puras.

## Otros características

Para finalizar hablemos de algunas de las características que los diseñadores de programas funcionales han añandido para hacer la programación más fácil.


### Pattern Matching

En algunos lenguajes funcionales no existe el concepto de asignación como lo conocemos en los lenguajes imperativos. El símbolo `=` representa algo parecido a lo que representa en las ecuaciones matemáticas: estamos afirmando la equivalencia entre dos valores, no asignándola. Por ejemplo en Elixir, las siguientes sentencias son válidas:

```elixir

a = 5

5 = a
```

La primera expresión puede parecer una asginación, pero en realidad, lo que está haciendo es "enlazar" el valor `5` a la variable recientemente creada, para hacer posible que tu aserción sea verdadera.

En el segundo caso en tiempo de ejecución el programa se limita a verificar que es verdad tu afirmación: si `a` tiene el valor `5`, el programa continuará sin ningún problema, pero si no, surgirá un error en tiempo de ejecución. El pattern matching funciona a nivel también de parámetros:

```elixir

defmodule fibonacci do
  def fib(1), do: 1
  def fib(2), do: 1
  def fib(n), do: fib(n-1) + fib(n-2)
end

```

Cada clausula de la función entrará sólo si se manda a llamar a la función con el parámetro que empareje con el declarado en los parámetros.

### Funciones de orden superior

En realidad ya hablamos un poco de ellas. Una función de orden superior puede recibir funciones como parámetros (recuerda que la funciones a final de cuenta simplemente son otro tipo de valores inmutables) o regresar funciones como parámetros.

Un ejemplo en JavaScript:

```javascript

// Devuelve una función que recibe un parámetro y multiplica por el número provisto
function producir_multiplicador(por_cuanto) {
  return ((n) => n * por_cuanto)
}

doblar = producir_multiplicador(2)
triplicar = producir_multiplicador(3)

doblar(5) // 10
triplicar(5) // 15

```

Esto es una técnica común para producir código más adecuado al dominio de tu problema.


### Conclusión

No hablamos de varias cosas que la programación funcional provee o permite realizar, como la composición de funciones, la aplicación parcial y los caombinadores, pero en artículos futuros hablaremos de algunos recursos que te ayudarán aprenderla.

Esperamo haber aclarado algunos conceptos que se oyen alrededor de la programación funcional y cómo es que estos son habilitados por sus dos caracterísitcas principales: funciones puras y valores inmutables.

No dudes en dejarnos algún comentario si algo no quedó claro.
