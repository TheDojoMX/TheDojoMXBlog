---
title: "Orígenes de la deuda técnica"
date: 2020-10-19
author: "Héctor Patricio"
tags: ['deuda-técnica', 'arquitectura', 'diseño-de-software']
description: "¿Qué es la deuda técnica y cómo podemos hacer para dominarla al máximo?"
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1585958469/17CDCA65-B853-4433-AE63-AACCFF577A3B_ufg1pl.jpg"
draft: false
---

Tuvimos una plática con [Sagrario Meneses](https://twitter.com/sagmmd) sobre la **deuda técnica** y cómo podemos atacarla. En este artículo te presentamos un pequeño resumen de lo que es y algunas sugerencias sobre su manejo.

## ¿Qué es la deuda técnica?

La definición corta de deuda técnica es: **todo aquello que hace que el software sea más difícil de producir y desarrollar**.

La deuda técnica es **invisible** para los miembros no directamente relacionados con el desarrollo del proyecto; para los que participan en ellos no siempre es fácil de ver.

Esto incluye algunas cosas concretas como:

- Los valores fijos que pueden cambiar en el futuro y en realidad deberían ser fáciles de cambiar sin tener que modificar el código (_hardcoding_)

- Falta de información: cuando nadie sabe sobre cómo trabaja cierta parte del sistema o qué hace cierta pieza de código

- Falta de distribución de información y conocimiento: cuando muy pocas personas saben sobre una parte del sistema y se convierten en cuello de botella

- Falta de diseño explícito

- Malas elecciones sobre diseño o tecnologías

- Mezcla de diseños y estilos de programación diferente sin guía

- Bugs que nadie conoce

Sagrario comparó la deuda técnica con **deberle dinero a la mafia**: no la puedes negociar, y cuando te supera estás en grandes problemas. Así que más vale que la aprendamos a controlar porque la deuda técnica puede hacer colapsar tu sistema.

## Formas de hacer visible la deuda técnica

Una forma que nos parece súper efectiva para hacer visible (literalmente) la deuda técnica: ponerlo en tablero de control en un espacio, idealmente, **físico**, que esté a la vista tanto del equipo técnico como del equipo administrativo. Este tablero fosforescente recordará a todos que hay temas importantes para atender antes de que la mafia venga a cobrarte.

En el caso de equipos remotos, el sustituto es un tablero de la herramienta de control que uses (Jira, Trello, Asana, Monday) que contenga temas importantes con respecto a las cosas que se pueden mejorar del sistema.

Finalmente, tus herramientas de desarrollo te pueden dar ideas valiosas de las cosas que tienes que mejorar de tu código:

- Te ayudan a listar las tareas pendientes (TODO's)
- Te advierten sobre posibles problemas de código
- Si tienes una guía de estilo configurada, te dan advertencias sobre este punto también.

## Prácticas para evitarla y dominarla

Para poder reducir la deuda técnica hacen falta dos
cosas:

1. Pruebas, **principalmente unitarias**. Esto permitirá encontrar los errores más rápidamente, pero además refactorizar sin miedo.
2. Lineamientos estrictos respecto a las acciones en el proyecto. Sagrario lo llamó _disciplina_, es decir, tener reglas y los procesos necesarios para hacer que estas reglas sean seguidas.

## Otros temas

También, hablamos de otros temas como el rol de arquitecta de software que tiene en Linio. De esto podemos sacar dos cosas relevantes:

1. Aunque no se se sentía completamente lista para el puesto, aplicó para obtenerlo, y por eso está en una posición en la que está aprendiendo mucho. Sin miedo al éxito.
2. A veces la ataca el síndrome del impostor, con el que siente que no pertenece allí, **pero continua trabajando y estudiando**.
3. Mantiene la humildad sabiendo que no por tener el "_título_" es todopoderosa y ahora tiene autoridad sobre todos.

## Conclusión

Disfrutamos mucho la plática con una experimentada desarrolladora de software que ha ido tomando nuevos roles y responsabilidades en la misma empresa, que también se ha ido transformando. Puedes aprender mucho de ella y de las preguntas que se hicieron en vivo:

<iframe width="560" height="315" src="https://www.youtube.com/embed/7E_xzjMwZMU" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
