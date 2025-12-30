---
title: "¿Qué son los agentes inteligentes?"
date: 2025-05-16
author: "Héctor Patricio"
tags: ['agente', 'IA', 'inteligencia-artificial', 'agents']
description: "La palabra 'agente' anda por todos lados desde la salida de los LLM's. Hablemos de lo que son y cómo"
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1440/v1739597131/ryan-klaus-Xa0BLOXVxrQ-unsplash_necdjp.jpg"
draft: false
---

Con la llegada de los LLM's, el término "agente" empezó a ganar más popularidad y
lo oímos por todos lados. En este artículo vamos a hablar de qué son, para entenderlo
lo mejor posible y no dejarnos llevar por el hype.

## ¿Qué es un agente?

Este es un concepto que ha sido muy difícil de definir y por muchaos lados encuentras definiciones diferentes.
En ester artículo vamos a dar una definicón sencilla y que nos parece práctica y que captura la idea principal
de toda esta ola de crear programas que puedan comportarse como agentes.

Primeo vamos a la etimología de la palabra: viene del latín "agere" que significa "hacer", "actuar", "mover", entre
otros significados. En pocas palabras, un agente es cualquier entidad que puede tomar decisiones y actuar.
Esta definición confiere bastante flexibilidad, pero conlleva en el fondo un idea que para mi es
la característica principal: la **autonomía**.

En el caso de sistemas de software, vamos a definir a un agente como un **programa** que tiene un **objetivo** y para
lograrlo puede tomar decisiones **autónomas**. Estas decisiones pueden ser tomadas basadas en su **percepción**
del entorno, en su estado interno (incluida la memoria) o en una combinación de estas cosas. Finalmente un agente
puede **actuar** para modificar su contexto y lograr su objetivo. Una característica que no siempre se cumple
pero que a veces está implícita es que el agente está funcionando de manera _constante_, o sea que no es
un programa que prendas y apagues, sino que está corriendo todo el tiempo.

En esta definición sencilla, encontramos varias partes clave que debe tener un programa para ser considerado un agente:

- **Objetivo**: El agente debe tener un objetivo claro que quiere lograr y por lo tanto una manera de medir su éxito.
- **Autonomía**: El agente debe ser capaz de tomar decisiones para los diferentes casos que se le presenten.
- **Percepción**: Aunque no es completamente necesario, muchos agentes tienen la capacidad de leer su entorno para
tomar mejores decisiones.
- **Actuación**: Los agentes pueden ser capaces de modificar su entorno, de hecho, esta, junto con el objetivo
es lo que le da sentido al concepto de agente.
- **Estado interno**: Debido a que las tareas que realizan los agentes pueden ser complejas, muchas veces es 
necesario mantener un estado interno que les permita ejecutar un plan de múltiples pasos, y para eso necesitan un
registro interno. Este estado interno puede incluir diferentes tipos de memorias: a corto plazo, a largo plazo, cachés, etc.

¿En qué se diferencia un agente de un programa normal? Para mi la principal diferencia es la capacidad de tomar
algún tipo de decisión autónoma y ejecutarla.

## ¿Por qué tanto alboroto con los agentes?

Como podrás notar, lo que acabamos de describir se puede lograr con cualquier programa desde hace mucho tiempo,
de hecho, tenemos ejemplos de programas que llamamos agentes desde hace década, justo porque cumplen con algunas 
de las características que describimos.

Por ejemplo:

- Los programas que monitorean el estado de un servidor y mandan las estadísticas a un concentrador para tomar decisiones.
- Los agentes encargado de actualizar automáticamente tus sistemas operativos, como el Windows Update Agent.
- Programas encargados de negociar entre protocolos de comunicación, como en el caso de DHCP o DNS, o SMTP.

Todos estos programas cumplen con la capacidad de tomar decisiones autónomas, cooperar con su entorno y ejecutar acciones
para lograr su objetivo. Pero, ¿entonces por qué el boom actual?

Una da las partes más difíciles de construir un programa que se pueda considerar un agentes es la de la
toma de decisiones. Los algoritmos internos capaces de adaptarse a muchas situaciones y tomar decisiones
sin que fueran explícitamente programados para eso son muy muy difíciles de construir. ¿Pero qué pasa si
podemos usar las nuevas tecnologías como el _corazón_ de un agente?

Justamente, los LLM's cons su capacidad limitada de razonamiento, toma de decisiones, adaptación, conocimiento
general y capacidad de generar texto bien formado (para usarlo en protocolos de comunicación), son una tecnología
perfecta para servir como los motores de decisión de un agente, todas las demás partes: la memoria, la observación
del contexto o el entorno, el estado interno y la capacidad de actuar son temas que ya teníamos más o menos resueltos.

Es por esto que los LLM's y los nuevos sistemas capaces de adaptarse a una cantidad inimaginable de entradas
de información y adaptar su respuesta y comportamiento a ellas, así como la capacidad de ser modificados
para comportarse mejor para casos específicos, han creado una ola de software basado en la idea de los agentes.

## Conclusión

Ahora ya sabes lo que es un agente de software, por qué decimos en esta última ola que los modernos son _inteligentes_
y qué está impulsando toda la emoción que se ve por todos lados.Los agentes son herramientas poderosas
para crear sistemas que hagan cosas complejas, normalmente con poca programación pero mucho
control de nuestro lado. Viene una época en la que cada vez se usarán más, por lo que te conviene
conocerlos y aprender a usar esta técnica de desarrollo. En un artículo futuro vamos a ver cómo crear
diferentes tipos de agentes con capacidades cada vez más complejas.
