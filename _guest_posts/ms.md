# Trabajando con LLM's para mejorar la salud mental

> El genio está fuera de la botella. Necesitamos avanzar en el desarrollo de inteligencia artificial, pero también necesitamos ser conscientes de los riesgos. - Stephen Hawking

En Mindsurf hemos estado estudiando, experimentando y trabajando con LLM's desde hace más de un año para mejorar la aplicación de salud mental que estamos desarrollando. El objetivo principal es ayudar al mayor número de personas posible a mejorar su salud mental. En este artículo te queremos contar el proceso que hemos seguido, nuestros resultados y lo que hemos aprendido.

Pero empecemos por lo básico, para entender de qué estamos hablando.

## ¿Qué es un LLM?

Un LLM es un "Large Language Model", o un **Gran Modelo de Lenguaje**. Puedes imaginarlo como un programa que ha consumido una gran cantidad de texto (básicamente todo el texto disponible en el internet) y que ha aprendido a generar texto que se parece mucho al que ha consumido.

Con "aprendido" nos referimos a que ha creado una representación interna, codificada en **parámetros**. El número de parámetros que un modelo de lenguaje como GPT tiene actualmente está en los **miles de millones** y es por eso que se los llamamos "grandes".

Los LLM's son muy buenos manejando el lenguaje humano, sin embargo, no son una base de datos llena de información verificada como verdadera, o que tenga sentido. Son modelos estadísticos que aprenden a generar texto que se parece mucho al que han consumido, pero esto no necesariamente es verdadero o útil.

Es por eso que, aunque se pueden usar como una parte de una aplicación, necesitan accesorios que los ayuden a generar texto con varias características:

- Relevante para el usuario final
- Verificable
- Basado en la realidad
- Útil
- Con las características de redacción deseadas, como empatía, humor, etc.

Todo esto además puede variar dependiendo de la parte de la aplicación y el ciclo de uso en el que el usuario se encuentre.

Antes de seguir, veamos por qué puede ser útil para ayudar a la salud mental.

## ¿Por qué es útil para la atención a la salud mental?

Un modelo de lenguaje, al ser tan bueno para escribir, puede servir para generar respuestas empáticas, adecuadas al usuario y relevantes, sobre todo si tiene una base confiable de la cuál sacar información.

Además, al evitar el texto repetitivo, la experiencia de intercambiar o recibir mensajes de texto se vuelve más natural.

De hecho desde que salió a luz GPT, se han escrito incontables artículos de cómo las personas usan estos modelos para cosas relacionadas con la salud mental, como por ejemplo:

- Terapia de texto con GPT-3
- Para sentirse menos solo
- Para escribir un diario y obtener consejos sobre lo que se escribe

Basta con hacer una búsqueda en Google para encontrar muchos más ejemplos.

Pero usarlo sin ningún tipo de supervisión médica humana, o sin ningún entrenamiento extra conlleva riesgos que pueden resultar en daños a la salud mental de las personas. Es por eso que en Mindsurf, al mismo tiempo que queremos aprovechar las nuevas tecnologías, estamos buscando la manera de hacerlas seguras y confiables, pero además de potenciarlas.

## ¿Cómo se puede mejorar?

Para lograr que un LLM sea útil para la salud mental, estamos haciendo varias cosas:

1. **Darle fuentes de información confiables.** Hemos creado un programa que a parte de consultar el LLM, lo usa para codificar información de salud mental de fuentes verificadas, para usarla posteriormente de la generación de respuestas con información relevante y verificada.
2. **Entrenarlo con datos de salud mental.** Los modelos de lenguaje se pueden ajustar de manera fina para que a parte de escribir muy bien, puedan escribir mejor con estilos o temas específicos. Estamos trabajando en crear un modelo que sea experto en temas de salud mental al mismo tiempo que puede adoptar varias funciones para generar texto.
3. **Verificación y pruebas.** Una parte esencial de crear una aplicación útil para la salud mental de las personas ha sido crear modelos robustos de pruebas que nos ayuden a verificar que el modelo se comporta como deseamos. Con cada iteración del producto fortalecemos estos modelos de pruebas internas que nos ayudan a ajustar mejor el modelo y crear mejores prompts.
4. **Supervisión.** Finalmente, ¿cómo sabemos que los diferentes modelos usado están haciendo lo que deben? Contamos con un sistema de supervisión de conversaciones anonimizado que nos permite comprobar el comportamiento de los modelos en producción, para obtener retroalimentación y mejorarlos, además de asegurarnos de que no está haciendo nada que resulte perjudicial para los usuarios.

Todo esto está guiado por un equipo de psicólogos, científicos de datos y expertos en experiencia conversacional que cooperan para crear la mejor experiencia posible. Además, estamos aprovechando nuestra experiencia en el desarrollo de un producto conversacional previa a los LLM's, que nos permite avanzar más rápido y con mayor seguridad.

Finalmente, contamos con una gran cantidad de programas, mensajes y acciones que la tecnología de los LLM's nos está ayudando a potenciar y multiplicar. Todo esto se suma a las otras tecnologías que usamos para crear una experiencia conversacional de alta calidad: los modelos predictivos para recomendación de contenido, la plataforma de conversación y nuestra servicio para agendar terapias con psicólogos certificados.

## Resultados

Hemos notado que el tiempo de conversación y el uso de la plataforma ha aumentado en un XX%, lo que nos demuestra que los usuarios están teniendo una mejor experiencia. Los usuarios se expresan de manera más abierta, por más tiempo y con mayor frecuencia.

Los usuarios se sienten más motivados a usar las otras partes de la plataforma, como nuestros programas de atención a los trastornos, _que han sido mejorados con la ayuda de los LLM's_.

Así, vemos que el uso de los LLM's para la atención a la salud mental tiene un brillante futuro que puede ayudar a muchas personas.

## ¿Qué sigue?

Aunque hemos avanzado bastante, tenemos un largo camino por recorrer. Tenemos varias iniciativas corriendo en paralelo.

### Modelos privados

Cada usuario debería tener un modelo completamente personalizado que se adapte completamente a sus necesidades.

Este modelo debería ser completamente privado, al mismo tiempo que pueda ser supervisado por un experto en salud mental para evitar que este tenga efectos perjudiciales. Estamos trabajando en una plataforma que permita esto, con costos accesibles al alcance de cualquier persona.

### Mejorar el costo

El costos de entrenar un modelo de lenguajes es muy alto y por lo tanto su uso de recursos computacionales también. Usar estos modelos aumenta el costo de operación del servicio, por lo que estamos trabajando en reducir al mínimo este costo, con el objetivo de llevarlo al mayo número de personas al menor costo posible.

### Creación de modelos bajo demanda

Muchas empresas se están dando cuenta de la importancia de la salud mental en su organización. Estamos trabajando en una forma de que cada una las instituciones que trabajan con nosotros puedan ajustar la plataforma a su cultura, valores y necesidades específicas.

Esto permitirá fortalecer la cultura de la empresa, al mismo tiempo que se mejora la salud mental de los empleados, lo que se traduce en un mejor ambiente de trabajo y mayor productividad.

## Conclusión

Durante los meses que llevamos aprovechando los LLM's tanto internamente, como en producción en los últimos meses, hemos visto que tienen un gran potencial para mejorar la salud mental de las personas. Queremos seguir trabajando en esta dirección para que cada vez más personas puedan tener acceso a una mejor salud mental y se conozcan cada vez mejor para poder vivir una vida más plena, enfrentando los retos de la vida con ayuda de la tecnología.

