---
title: "Claridad de  Saša Jurić"
date: 2022-12-30
author: "Héctor Patricio"
tags: ['claridad', 'código-claro', 'pláticas']
description: "Todos quisiéramos tener bases de código perfectas, fáciles de mantener y totalmente claras. Esto es casi imposible, pero podemos acercarnos. Vemos cómo."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1672204121/ivan-bandura-8VePVILfCKU-unsplash_bhsnsa.jpg"
draft: false
---

<figure>
    <figcaption class="caption-audio">Escucha este artículo:</figcaption>
    <audio style="width: 100%;"
        controls
        src="https://res.cloudinary.com/hectorip/video/upload/v1672460944/clarity-2_vrm0vk.wav">
            <a href="https://res.cloudinary.com/hectorip/video/upload/v1672460944/clarity-2_vrm0vk.wav">
                Descargar audio
            </a>
    </audio>
</figure>

Hablemos de las cosas que hacen más entendible y claro tu código.

Muchas de estas ideas están basadas en la plática ["Clarity" de Saša Jurić](https://www.youtube.com/watch?v=6sNmJtoKDCo) de la Elixir Conf EU de 2021, de hecho, podríamos considerar este artículo como un análisis y extensión de esa plática.

- Cuando trabajamos con bases de código normalmente necesitamos entenderlas. Incluso aunque vayamos a escribir algo nuevo necesitamos entender lo demás para poder integrarlo. Esto lo hacemos mediante la lectura de código.

- Los escritores del código nos transmiten información mediante ese código, lo quieran o no.

- La forma en la que obtenemos conocimiento del código es leyéndolo.

## ¿Qué es la claridad y por qué es mejor que 'el código limpio'?

La claridad como se define en esta plática, es qué tan bien una pieza de código comunica sus verdaderas intenciones. El código claro puede ser entendido sin mucho esfuerzo por alguien que conoce bien el lenguaje: se entiende tanto el problema como la solución que el autor escogió.

La claridad nos hace más eficientes y efectivos. Primero porque obtenemos información más rápido y segundo porque obtenemos la información correcta.

Finalmente, la claridad le da poder al equipo porque hace que cualquiera pueda tomar el código y trabajar con él, en vez de sólo el autor, como muchos estamos acostumbrados.

Para conseguir claridad se tiene que invertir tiempo constantemente. Tienes que recordar que el código es una herramienta de comunicación con otros seres humanos, no sólo con la máquina.

![Claridad es más concreto que otros términos](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_800/v1672409158/Screen_Shot_2022-12-28_at_9.37.57_aje64x.png)

## Prácticas que mejoran la claridad

Hablemos de cosas que tú y tu equipo pueden hacer para producir código más claro.

### Revisión de código

Esto es la práctica de un equipo de integrar el código a la rama principal solamente cuando ha sido evaluado por cierto números de miembros del equipo. El foco principal de la revisión debería ser la claridad del código.

Para facilitar el proceso, tanto el autor como el revisor pueden seguir ciertas reglas para que el resultado sea código más claro y la revisión sea más fácil.

El que envía el código puede facilitar el trabajo del revisor de tres maneras:

1. Envía solicitudes de integración pequeñas: siempre es más fácil de entender poco código que mucho.
2. Commits pequeños como unidades de cambio más fáciles de tratar individualmente. Un commit no debería tener cambios en muchos lugares para no hacerlo demasiado difícil de entender.
3. Clarifica tu código lo mejor posible: la historia de los commits debería estar estructurada linealmente. Además debería revisar su código para asegurarse de que está lo más claro posible.

El revisor:

1. Sugerir y mandar mejoras. El revisor debería señalar todos los puntos en los que se le hizo difícil entender el código. También podría mandar los cambios directamente, como un pull request al autor, invirtiendo los papeles temporalmente.

2. Sincronizar. Es importante tener sesiones si algo no se puede resolver. Estas sesiones de pair programming servirán para clarificar todo aquello que siga siendo confuso.

### Prácticas en el código

Saša sugiere seguir las prácticas de progrmación comunes **aplicables al código**:

1. Nombrar variables y funciones de manera explicativa.
2. Seguir los idiomas y patrones de programación _aplicables_ a tu caso.

### Separación de responsabilidades

Pero además, podemos seguir lo que en español llamamos "separación de responsabilidades" (en inglés "separation of concerns"). Esta idea Dijkstra lo mencionó en su artículo [On the scientific thougth](https://www.cs.utexas.edu/users/EWD/transcriptions/EWD04xx/EWD447.html). Dijkstra se refería a la forma de pensar en los asuntos complejos desde diferentes ángulos para poder "ignorar" temporalmente los aspectos que no tienen que ver con ese ángulo. Esto permitirá que podamos entender mejor el sistema entero poco a poco.

En el código lo podemos aplicar haciendo que nuestro código esté separado en módulos que sólo abarquen un aspecto del problema. Esto es imposible de hacer perfectamente, pero nuestro código debería tender hacia allá lo más posible. Por ejemplo, algo que normalmente se hace muy bien es separar el código que maneja la lógica de los datos de la interfaz. Recuerda: **esto es importante porque permitirá al lector solo lidiar con un problema a la vez**.

Si ponemos todos los conceptos posibles de programación en una pieza de código (aquí cito directamente a Saša) "¿Quién va a ser capaz de entender algo de eso?"

![Imagen: Separación de responsabilidades en una base de código](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_800/v1672409162/Screen_Shot_2022-12-30_at_8.05.42_ycvhe7.png)

---

**Advertencia**: Una idea que Saša menciona bastante es la de no seguir arquitecturas o ideas sólo porque un líder de opinión o alguien con autoridad lo dice. Si haces esto **puede que la parte más compleja de tu código sea tu arquitectura**, lo cuál es un grave error porque el trabajo de la arquitectura deberías ser crear un sistema más claro.

> "Consider te actual situation you're dealing with, [..], don't just do something because some thought leader or authority says so, even if that person is me. Just think contextually, think inside of your situation." - Saša Jurić

> "Considera tu situación actual, [..], no hagas algo sólo porque un líder de opinión o alguien con autoridad lo dice, incluso si esa persona soy yo. Simplemente piensa contextualmente, piensa en tu situación." - Saša Jurić

## Testing

¿Para qué creamos tests? Obviamente, para probar. ¿Pero qué queremos probar? Saša afirma que queremos probar **el comportamiento del software**. Así, las "unidades" que queremos probar son las unidades de comportamiento y no las unidades de código. Otra recomendación es evitar hacer mocks agresivos, solamente en dónde sea estrictamente necesario para lograr comportamientos repetibles. Esto es porque, el uso de dobles en los tests (como los mocks) complica el código de pruebas, pero también complica el código de producción.

Cuando los tests son demasiado complicados o están ligados a la implementación en vez del al comportamiento externo, vas a tener que dividirte entre arreglar los test o arreglar el código de producción, lo cuál es frustrante y una mala idea para tu productividad en general. Un test debe ser fácil de entender y comunicar exactamente lo que está probando, nada más, nada menos.

Recomendación: Libro [Unit Testing](https://www.manning.com/books/unit-testing) de Vladimir Khorikov. Saša lo recomienda como una muy buena lectura.

![Recomendación de libro TDD por Saša Jurić: Unit Testing de editorial Manning](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_800/v1672450947/Screen_Shot_2022-12-30_at_12.03.25_nedtbg.png)

## Conclusión

Una de las tareas más importantes cuando hacemos código es hacer que comunique claramente el problema que resuelve y cómo lo resuelve. Si hacemos eso, lograremos que nuestro equipo o nosotros mismos podamos continuar con el trabajo y lo mejor: evolucionarlo.

En la siguiente imagen verás el resumen de las recomendaciones de Saša Jurić para escribir código más claro:

![Usa el código para comunicarte, revisa el código, separación de responsabilidades y prueba el comportamiento del código](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_800/v1672450967/Screen_Shot_2022-12-30_at_18.48.20_hekzsv.png).

Puedes ver la charla completa en [YouTube](https://www.youtube.com/watch?v=6sNmJtoKDCo). [Manuel Rubio](https://twitter.com/mronerlang) y yo platicamos extensamente sobre ese tema:

<iframe width="560" height="315" src="https://www.youtube.com/embed/Gswx3ko3A_E" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Finalmente, te recomiendo mucho el artículo en el que Manuel Rubio hizo su propio resumen en [el blog de Altenwald](https://altenwald.org/2021/09/27/claridad/).
