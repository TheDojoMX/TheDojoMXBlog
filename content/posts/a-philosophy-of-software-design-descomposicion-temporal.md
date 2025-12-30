---
title: "A Philosophy of Software Design: Descomposición Temporal"
date: 2020-03-16
author: "Héctor Patricio"
tags: ['APoSD', 'descomposición-temporal', 'software-design', 'complexity', 'interfaces']
description: "Una forma de dejar escapar información es mediante forzar el orden de las operaciones de un módulo. Veamos cómo evitarlo."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1584251653/A240034B-230E-4BA2-843D-32357D921811_mwdnzk.jpg"
draft: false
---

En el artículo pasado hablamos de una forma de evitar una fuga de información, que consiste en encapsular una decisión de diseño en un módulo.

Otra forma de dejar escapar información no relevante para los usuarios de una pieza de software es mediante obligarlos a usarla siempre de la misma forma, con el mismo orden de operaciones reglas de operación implícita. Esto se llama descomposición temporal. Hablemos más de ella.

## Qué es la descomposición temporal

> En descomposición temporal, la estructura de un sistema corresponde **al orden en el tiempo** en el que las operaciones **ocurrirán**. - John Ousterhout

La descomposición temporal implica repetir o separar una decisión de diseño por causa del _orden en que se usan diferentes partes del sistema_.

![Descomposición temporal](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1584345818/A85931E4-BBF3-4301-98D3-ACE20942AF9E_hugdbz.png)

## Ejemplos

John Ousterhout menciona un ejercicio que puso a sus alumnos en el que tenían que crear un programa implementando el protocolo HTTP.

Algunos equipos crearon una clase para recibir el mensaje desde la red y _otra clase para leerlo_, creando así un caso claro de descomposición temporal: como las operaciones sucedían en diferentes momentos (primero recibes y luego lees y procesas) los separaron lógicamente en dos clases que se usaban siempre una detrás de otra. La fuga de información se dio porque para recibir un paquete HTTP _tienes que leer_ parte del mensaje y entonces la lógica de lectura del mensaje está en _ambas clases_.

Otro ejemplo más o menos obvio es la lectura y escritura de archivos. Si quieres trabajar con archivos, el orden de las operaciones es la siguiente:

1. Abrir y leer
2. Operar con información del archivo
3. Escribir el archivo

Un diseño que deja escapar información sería tener dos clases diferentes para la parte de escritura y lectura, cada una con código repetido que sabe leer el formato del archivo.

Ejemplo 3: imagina las diferentes situaciones en las que un elemento de datos cambia _de estado_ a través de su ciclo de vida. Puede ser una solicitud de crédito, un reporte, un blogpost, etc.

Es tentador crear diferentes entidades de datos y clases para representar algún estado en específico, ya que podría hacer que nuestro código fuera un poco más explícito cuando llamamos las clases o métodos.

Pero si no hay operaciones especiales que correspondan a ese estado, o datos únicos para esta etapa, crear un módulo específico implicaría descomposición temporal: estarías dividiendo o duplicando conocimiento a través de diferentes módulos debido al orden en que suceden los eventos.

## Composición de funciones

En los lenguajes funcionales es común usar una serie de funciones aplicadas a una entidad de datos. Por ejemplo en Elixir es común hacer lo siguiente.

```elixir
# El operador |> Toma el resultado de la función o valor
# de la expresión anterior (o a su izquierda) y lo manda
# como primer parámetro a la función a la derecha, parecido
# a una redirección de salida de Unix

" the dojo "
  |> String.trim # Limpiar los espacios sobrante a la cadena " the dojo "
  |> String.split(" ")  # Separar la cadena
  |> Enum.map(&(String.capitalize(&1)))  # Poner en mayúsculas cada uno de los elementos
  |> Enum.join  # Volver a juntar la cadena

# Resultado: "The Dojo"
```

Este ejemplo es un poco exagerado para la función que realiza: poner un texto con capitalización estilo título, Todas Las Iniciales En Mayúsculas.

La idea viene de las matemáticas y se llama "composición funcional" y como se puede ver es excelente para usar funciones _existentes_ en la creación de procesos más complejos. Una de las virtudes de esta técnica es la **reutilización** de las funciones.

Sin embargo, queriendo aplicar esta idea, puedes cometer el error modificar tus módulos (en lenguajes funcionales: funciones), para aplicar esta técnica y _terminar con funciones que siempre se usen una tras otra_, esperando la entrada de la misma función y mandando su resultado siempre a la misma función. Algo así:

```elixir
"datos"
  |> MiModulo.mi_funcion_1
  |> MiModulo.mi_funcion_2
  |> MiModulo.mi_funcion_3
```

Esto es un error que yo he cometido y que ha hecho mi código _muy difícil de mantener_, ya que al cambiar una función de esta cadena tengo que cambiar las demás, haciéndolas no reutilizables.

## Solución a la descomposición temporal

La solución propuesta por [A Philosophy of Software Design](https://amzn.to/2GdeHi5) es muy sencilla: **concentra todas las operaciones relacionadas con una decisión de diseño en un módulo**.

Si nada necesita ser conocido fuera de este módulo (ni detalles de la implementación, ni el orden de operación), has logrado un diseño más limpio. Esto puede implicar que la clase se haga más grande, pero es una mejor solución comparada con tener información repartida por todos lados.

Así, si la decisión de diseño cambia, _sólo tienes que cambiar la implementación_ y no la interfaz ni mucho menos su uso.

En el siguiente artículo veremos finalmente una serie de recomendaciones para evitar las fugas de información y como no llevarlo demasiado lejos.
