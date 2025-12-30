---
title: "Guía para escoger tu stack: por qué deberías escoger tecnología aburrida"
date: 2020-03-11
author: "Héctor Patricio"
tags: ['arquitectura', 'infraestructura', 'decisiones-técnicas']
description: "Si quieres hacer feliz a un desarrollador, dale una tecnología nueva y brillante. En este artículo hablamos de por qué es mejor idea escoger tecnología probada."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1583644548/9641A743-5E78-4719-9F90-6D77F1CD4E1E_xhawu6.jpg"
draft: false
---

Este artículo está basado en la presentación [Choose Boring Technology](http://boringtechnology.club) de [Dan McKinley](https://mcfunley.com/).

No hay nada que haga más feliz a un desarrollador que trabajar con el último de los frameworks, lenguaje de programación o herramienta que salió el mes pasado.

Este problema se incrementa si trabajas en web, específicamente en JavaScript, donde cada semana tenemos un framework nuevo.

Pero hacer esto puede llevar a tu empresa o producto al desastre, como ha pasado muchas veces. Veamos algunas de las razones.

## Qué es la tecnología _aburrida_

Cuando hablamos de tecnología _aburrida_ en este artículo nos referimos a aquello que no es nuevo y brillante como el último framework: cosas que se han usado por mucho tiempo y que a nadie le emocionaría usar porque no es novedoso.

### Ejemplos

**Tecnología brillante**:

* El último lenguaje de programación para hacer concurrencia (Crystal, Pony o algo así)
* Aunque tenga tiempo existiendo, la cosa que casi nadie en el mundo usa (como OCaml o Ío)
* La base de datos, servidor web, etc. en la que no has trabajado antes pero quieres usar para complementar tu stack ("Vamos a agregarle CouchDB, creo que puede resolver el problema mejor").

No tiene que ser completamente nuevo, puede ser novedoso sólo _para ti y tu equipo_.

**Tecnología aburrida**:

* Una modesta instalación de Python, Django y PostgreSQL
* La instalación común de PHP con Laravel y las tecnologías asociadas
* Java con Spring
* El framework y lenguaje con el que trabajas normalmente y tienes más experiencia

Con tecnología aburrida _no nos referimos a cosas malas_, sino a cosas que no son emocionantes por nuevas.

Hablemos ahora de por qué es casi siempre más provechoso escoger "tecnología aburrida".

## La capacidad de innovar es limitada

Piensa que tu empresa o producto tiene una capacidad limitada de resolver problemas, generalmente determinada por el tiempo para salir al mercado (o aprovechar una nueva oportunidad de negocio) y por el dinero disponible. El autor de la presentación facilita pensarlo diciendo que tienes unas cuántas "Innovation tokens" o _monedas de innovación_. Mientras más limitantes tengas, como el tiempo o el dinero, menos de monedas de innovación tienes.

Si quieres resolver un problema de manera novedosa, puede que eso requiera todas tus moneditas, o incluso más. Y generalmente es aquí donde _cualquier negocio_ quiere gastar sus energías. Esto se explica viendo a las empresas como si fueran humanos.


> Si piensas en la innovación como un recurso escaso, empieza a perder sentido también estar en las líneas frontales de innovación en bases de datos. O de paradigmas de programación. El punto no es que esas cosas no puedan funcionar. Claro que pueden funcionar. **Pero el software que ha existido por más tiempo tiende a necesitar menos cuidado y atención que el software que acaba de salir**. - Dan McKinley

### Pirámide de Maslow

Abraham Maslow propuso en los 60's una [jerarquía de las necesidades humanas](https://es.wikipedia.org/wiki/Pir%C3%A1mide_de_Maslow), conocida como la Pirámide de Maslow, en la que se habla de diferentes tipos de necesidades jerarquizadas, desde las fisiológicas hasta las emocionales.

Su tesis principal es que tienen que cumplirse las de la base de la pirámide (fisiológicas; comer, dormir, respirar) **antes** de cumplirse las de la punta (moralidad, creatividad, etc).

![Pirmámide de Maslow](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1584127283/6D71EA5B-8CC6-454B-B342-6287A9845189_edyfje.png)

Lo que explica Maslow acerca la satisfacción de las necesidades tiene lógica: _no puedes_ preocuparte por cosas como si la filosofía de los estoicos es correcta si no tienes lo suficiente para comer hoy, o no has dormido en tres días. O peor aún, no puedes pensar en tu movimiento siguiente si te estás quedando sin aire.

Lo mismo pasa a nivel tecnológico y de supervivencia en las empresas o proyectos: no puedes pensar en formas de beneficiar a tu cliente, de resolver ese problema tan difícil de manera innovadora si te estás pelando con mantener viva en producción una base de datos.

Así que desde el punto de vista económico tiene completo sentido: escoger tecnología lo más fácil de entender, en la que tengas experiencia o sea fácil encontrar expertos que te guíen, tiene más lógica que escoger lo más nuevo.

![Pirámide de necesidades Tenológicas](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1584127281/604612EB-0432-4D88-B1B4-CBAAEFF7042D_hyfu6z.png)

## La tecnología 'aburrida' es más segura

> Existen sólo dos tipos de lenguajes: de los que la gente se queja y los que nadie usa. - Bjarne Stroustrup

La tecnología como los lenguajes, librerías, bases de datos y en general software y hardware que lleva mucho tiempo existiendo es más confiable en el sentido de que conocemos sus fallas, sus limitantes y existen personas que nos pueden contar sus usos y malos usos.

Todos los proyectos de software respetables tienen una lista de errores conocidos, que puedes consultar en su documentación y el tiempo estimado en que se resolverá, si no se resolverá y las formas de darle la vuelta. En pocas palabras ya sabes que esa tecnología apesta y sabes _por qué_.

Una tecnología nueva no tiene esto, y las sorpresas que la esperan pueden ser muy grandes y desagradables. Pero aquí entramos en el campo del riesgo y el conocimiento humano.

### Cosas que no sabes que no sabes

Todas las cosas que son capaces de ser aprehendidas por la mente humana caen en una de cuatro categorías:

- **Cosas que no sabes que sabes.** Son cosas que sabes inconscientemente, como caminar, respirar, mover tus manos, etc. Puede haber otras menos automáticas, que se pueden descubrir con un poco de razonamiento, como la ortografía de una palabra o gramática. Por ejemplo, sabes conjugar en modo subjuntivo la mayoría de los verbos de tu idioma pero si no has estudiado la gramática del lenguaje tal vez ni siquiera sabes que existía el modo subjuntivo.

- **Cosas que sabes que sabes.** Este es lo que entendemos como "conocimiento" cuando hablamos de él. Por ejemplo sabes que escribir está dentro de tus habilidades. O sabes que puedes sumar.

- **Cosas que no sabes que no sabes.** Cosas que estás consciente de no saber, como física cuántica o análisis de variable compleja. Mientras más sepas de algo, más probable es que te des cuenta que no sabes otras muchas cosas de ese mismo tema. De ahí la frase: "Sólo sé que no sé nada".

- **Cosas que no sabes que no sabes.** Esto es lo que nos pone en riesgo. Aquí caen muchos eventos futuros y la mayor parte del conocimiento disponible está en esta área para cualquier persona. Por ejemplo, no sabemos que no sabemos las causas de un desplome económico. De esto ni siquiera podemos hablar porque _no sabemos_ que existe. Esto es lo que podemos nombrar como _incertidumbre_.

La quinta categoría, que [N. N. Taleb](https://www.fooledbyrandomness.com/) describe en su libro [Cisne Negro](https://amzn.to/2xqIzmH), son las cosas que no podemos saber, como el futuro o las causas de algo en el pasado.

![Teoría del conocimiento](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1584164642/CEA9E5D1-1E77-4543-8256-DB6C195CBCFB_dwvf1j.png)

¿Por qué es importante esto? La cantidad de cosas que _sabemos_ que no sabemos o que fallan de un proyecto "aburrido" o probado pueden ser muchas, pero _sabemos_ que ahí están y nos podemos proteger contra ellas. Aún hay cosas que no sabemos que no sabemos, la incertidumbre nunca se elimina, pero son menores al tener más experiencia colectiva sobre algo.

En las tecnologías de reciente creación hay mucha información que _no sabemos que no sabemos_. La cantidad de incertidumbre es mucho mayor, incluso con cosas no relacionadas directamente con la tecnología, como el entorno en el que se está creando. ¿Matarán mañana al proyecto?

Reducir la incertidumbre al máximo posible debe ser uno de los objetivos de cualquier buen arquitecto o diseñador de software.

## Integración

Cuando hablamos de tecnología probada, no sólo nos referimos a componentes individuales sino a conjuntos de tecnologías usados para resolver un problema comúnmente. Piensa en PHP + MySQL + Memcache, Python (Django) + PostgreSQL + Redis.

Una dificultad extra de usar la tecnología más nueva es que es probable que la tecnología que ya estamos usando no se lleve bien, pero no lo sabremos hasta que la probemos y encontremos las nuevas dificultades.

### Sistemas en producción y número de piezas

Mantener algo en producción es difícil y requiere trabajo y planeación. No porque puedas empezar a usar Neo4J en cinco minutos significa que debas usarla en tu próximo proyecto, ya que el número de elementos diferentes que uses en tu sistema está _directamente relacionado con la dificultad de mantener tu sistema en producción y estable_.

Deberías buscar _resolver el mayor número de problemas con el menor número de tecnologías posible._ Hacerlo te evitará crear una maraña de sistemas imposible de entender y **mantener**.

![Comparación entre un sistema simple y uno complejo](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1584168893/71161A7B-26AA-4A71-9318-CC74AD810385_yivlr9.png)

## Ecosistema

Escoger tecnología que ha sido usada por mucho tiempo y que ya no es novedosa, permite que te aproveches de un cuerpo de conocimiento que ya está disponible para que aprendas, un montón de problemas resueltos y compartidos por otros y un ecosistema maduro que te permitirá avanzar en tus problemas específicos más rápido.

No hay nada peor cuando estás desarrollando que encontrarte con un problema incomprensible (y una pregunta sin respuestas en Stack Overflow) o con un bug que no ha sido resuelto en tu lenguaje o herramienta. No estoy diciendo que es el fin del mundo, pero seguramente algo que te pudo tomar 10 minutos con la ayuda de otros ahora te costará dos días resolviendo ese obscuro problema.

### Dominio de la tecnología

Trabajar con la misma tecnología repetidamente hará que tu conocimiento en esa tecnología se vuelva como andar en bicicleta: pasarás al campo de la competencia inconsciente, la usarás casi como si fuera parte de tu cuerpo y podrás enfocarte más rápido en resolver tus problemas específicos.

Una desventaja que viene con esto es la famosa frase "Aquel con un martillo piensa que todo es un clavo", pero se puede evitar manteniéndote al pendiente de los avances tecnológicos en proyectos de juguete y empapándote de nuevas cosas mediante el estudio continuo, para que no se pierda la frescura de lo que haces.

Después de pensar en todo esto, aún hay veces que conviene integrar ya sea una tecnología que no se estaba manteniendo en el proyecto o lo más nuevo.

## Cuando integrar nueva tecnología

El caso principal en el que conviene integrar una nueva tecnología tiene que ver con un equilibrio en los costos. La principal pregunta que debes hacer es: ¿facilita mis tareas TANTO esta tecnología que equilibra el trabajo extra que tendré que hacer?

Con "trabajo extra" nos referimos a todo lo mencionado en los puntos anteriores, la curva de aprendizaje, la carga añadida de nueva infraestructura, las dificultades no encontradas aún, etc. Puede haber casos en los que una tecnología nueva supere todo esto, dándote una productividad mayor o permitiéndote hacer cosas que son muy muy difíciles de lograr con la tecnología actual.

## Conclusión

Es más conveniente tanto para ti como para el negocio que tus golpes de dopamina vengan por el lado de resolver problemas emocionantes _útiles para algún cliente y para el negocio_, que por andar resolviendo problemas oscuros que nadie le proveen mucho valor (tal vez aprendizaje, pero se puede obtener de otras formas).

**Enfoca tus esfuerzos en cosas útiles para el negocio.**
