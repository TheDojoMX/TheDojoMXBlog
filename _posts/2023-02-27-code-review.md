---
title: "Code Review: La practica Milenaria que seguimos haciendo mal."
date: 2023-02-27
author: Sagrario Meneses
tags: crecimiento-profesional comunidad mentoria programación productividad
excerpt: "¿Quieres saber si haces una buena revisión de código? Estas en el lugar correcto."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1677550573/221453137-8e8b0887-953a-43f4-a34d-a1f36c7deb00_wxg5wx.png
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1677550573/221453137-8e8b0887-953a-43f4-a34d-a1f36c7deb00_wxg5wx.png
  overlay_filter: rgba(0, 0, 0, 0.5)
---

## ¿Qué es un "Code Review"?

Es la práctica que realizan los equipos de ingeniería de software para verificar los cambios de código antes de fusionarlos con el código fuente principal.

## Dónde se aplica

En todas partes, cuando eres miembro de un equipo, como colaborador individual o como estudiante. Tienes la oportunidad de involucrarte, contribuir y dar tu opinión a código escrito por otra persona. Algunos ejemplos:

### Durante una sesión de "pair programming"

> "Dos cabezas piensan mejor que una."

Revisando una pieza de código con alguien más, los desarrolladores podemos hacer recomendaciones, mejoras y adiciones a un sistema en tiempo real.

### En aplicaciones de control de versiones, tales como

- El Pull Request (PR) en GitHub.
- El Merge Request (MR) en GitLab.

Estas funciones permiten a los desarrolladores proponer cambios en un código propiedad de otra persona. Es una forma de revisar y discutir cambios propuestos antes de fusionarlos, lo que permite a otros desarrolladores dejar comentarios, solicitar cambios o aprobar una solicitud de forma asíncrona.

### En cualquier fragmento de código propuesto

Hay otros canales o formas de compartir código con un equipo. A veces, los desarrolladores lo hacen a través de Slack (u otros servicios de mensajería) u otra, simplemente compartiendo enlaces.
Si como desarrollador notas algo para mejorar o agregar, tu equipo de tecnología debe ser el lugar que permita que esas interacciones y comentarios sucedan orgánicamente.

## Beneficios de la revisión de código

Esta práctica aumenta significativamente el trabajo en equipo. Involucrarse con el código de los demás e involucrar a otros en tus contribuciones aumenta el éxito en la creación de productos. Algunos de los beneficios son:

### Solución 77 temprana de errores
>
> "Aquel de ustedes que esté libre de romper producción, que tire la primera piedra."

Como humanos, los ingenieros de software no están exentos de cometer errores, y es una gran ventaja contar con un equipo que te apoye, revise y libere tareas en conjunto. Durante una revisión de código, estos errores se pueden detectar y corregir.

### Mejorar la calidad
>
> "Es más barato hacer las cosas bien la primera vez."

Establecer reglas en el estilo de código que aumenten la legibilidad, el mantenimiento y la escalabilidad del código ayuda a escribir software de calidad.

### Intercambio de conocimientos

El Code Review es una excelente herramienta para recibir y dar retroalimentación, aprender las mejores prácticas de los desarrolladores con más experiencia e intercambiar soluciones.

### Sincronización

Con esta práctica, se puede saber en qué está trabajando cada miembro del equipo, evitar duplicación de esfuerzos y mantenerse actualizado con la lógica del negocio.

## Primeros pasos

Una buena idea para aplicar correctamente esta práctica en tu equipo es establecer reglas antes de empezar.

- Establezca una plantilla de descripción con los puntos mínimos que el equipo necesitará para comprender el contexto y el propósito de una solicitud de cambios de código y apliquen esa plantilla de manera consistente en todas las solicitudes futuras.
- El número mínimo de revisores para aprobar un fragmento de código; esto dependerá del tamaño del equipo.
- Canales o herramientas de comunicación al equipo cuando un código este listo para ser revisado.
- El tiempo entre las revisiones, es decir, que si un desarrollador marca un fragmento de código listo para revisarse y el equipo hace sugerencias o solicita cambios, y seguido de eso el desarrollador aplica los cambios solicitados, debe establecerse la cantidad de tiempo que debe pasar para solicitar una nueva revisión. Esta regla puede ser útil en equipos grandes que están involucrados en diferentes sistemas y necesitan dividir el tiempo entre el desarrollo y la revisión. En equipos pequeños, una regla de este tipo es opcional.

## Revisión efectiva
>
> "Una buena revisión necesita de experiencia y profesionalismo y no de nivel de seniority."

Solo algunos desarrolladores son capaces de aplicar una buena revisión del código, esa es la razón principal por la que escribir esta publicación. El Code Review no es una práctica nueva en lo absoluto. Por el contrario, ha existido durante décadas, desde que las personas comenzaran a escribir código. Una de las primeras referencias a esta práctica como proceso formal se encuentra en el libro "The Mythical Man-Month" de Fred Brooks, publicado en 1975.

Entonces, ¿por qué te pareció un tema importante? he estado trabajando con equipos de Ingeniería de Software durante aproximadamente 12 años y sigo leyendo comentarios que tienen un tono vago o agresivo o que carecen de explicación y contexto, lo que dificulta la aplicación efectiva de cambios en el código.

### La revisión de código *NO ES* una práctica para

- Demostrar superioridad.
- Hacer que otros se sientan inseguros.
- Imponer estilos de codificación.
- En resumen, ser un idiota.

![No](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_350/v1677550574/221453027-36a424b8-7ff5-4b17-bc8a-9bda2e223c22_rahapd.png){: .align-center}

Aquí algunos ejemplos.

![code example](https://res.cloudinary.com/hectorip/image/upload/c_scale,q_100,w_800/v1677550576/221453038-b93d320a-5389-40e8-bf58-cd24b42910c4_ta57tb.png){: .align-center}

Mala revisión:
"Este código es malo. ¿Por qué estás haciendo una búsqueda lineal?"

Buena revisión:
"Este bloque de código podría optimizarse mediante el uso de una búsqueda binaria en lugar de una lineal. Esto mejoraría el rendimiento al buscar en grandes conjuntos de datos".

Como puedes ver en la mala revisión, hay más críticas que propuestas de alternativas o solución, o carece de la explicación del por qué se debe mejorar el código. Por el otro lado, la buena revisión ofrece una optimización, explicando por qué el enfoque diferente puede mejorar la función.

Más malos ejemplos:

- "Este código apesta". - Esto no es útil y no proporciona comentarios ni sugerencias para mejorar.

- "No entiendo lo que estás tratando de hacer aquí". - Esto es desdeñoso y no proporciona comentarios constructivos. Si hay una duda genuina de la implementación lo ideal es expresar esa duda lo mejor posible.

- "Yo no lo haría de esta manera". - Este comentario no es útil y le faltan razones o sugerencias para mejorar el código en revisión.

Los comentarios en una revisión del código deben ser específicos, constructivos y aplicables, evitando agresiones personales, un lenguaje desdeñoso y generalizaciones.

Evite por completo el uso de signos de exclamación e íconos para enfatizar comentarios negativos. Por último, recuerda que las malas interpretaciones son comunes en la comunicación escrita y pueden ocurrir aunque la intención sea buena.

### La revisión de código *SI ES* una práctica para

- Incentivar el trabajo en equipo.
- Reconocer el buen trabajo.
- Ser flexible con los estilos de código y aprender de el equipo.
- En resumen, es para ser un miembro del equipo.

![approved symbol](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_350/v1677550578/221453050-3cc5f85d-a2bd-4f67-9aa6-9a0e1ddf76b2_hol1iu.png){: .align-center}

*Aquí te dejo una sugerencia poderosa*, no solo comentes lo que consideres que se puede cambiar o mejorar, sino también comenta lo que te gustó en una implementación, por ejemplo:

- "¡Buen trabajo! Este código está muy bien organizado y es fácil de entender. Aprecio especialmente cómo usaste las funciones integradas en la biblioteca estándar de Go para simplificar el código. ¡Sigue con el excelente trabajo!""

Adicionalmente, recuerda tomarte el tiempo. El trabajo es exigente y, a veces, no dedicamos suficiente tiempo a las revisiones, y comentamos "¡LGTM!" (Me parece bien) para seguir adelante, pero recordemos que el otro desarrollador dedicó tiempo a trabajar en esos cambios, por lo que vale la pena revisarlos con cuidado.

Otra sugerencia que les dejo es establecer convenciones para los comentarios como lo es el uso del prefijo "NIT" (*nitpicker*), este se usa para sugerir un cambio, que no bloquea ni impide que ese el código en revisión sea aceptado o fusionado; es simplemente una "perfección" a la que estas apuntando pero que puede ser ignorada. Para obtener más información sobre convenciones de este tipo visten este [sitio](https://conventionalcomments.org/).

## Mi código es el que esta en revisión

Por último, ser la persona que recibe las revisiones también requiere práctica.

1. No te lo tomes como algo personal.
Aunque recibas un mal comentario, recuerda que el objetivo del equipo siempre será entregar un software de calidad. Se está revisando una parte de tu código, no su persona o tu trabajo en sí.

2. Se un miembro de equipo.
Otras personas usarán el código que escribiste hoy. Por lo tanto, es fundamental estar abierto a modificar tu trabajo por el bien del equipo y del producto final.

3. Responde positivamente a los comentarios.
Habrá casos en los que, como desarrollador que escribió el código en revisión, tendrás razones para creer que es la solución que debe fusionarse, sin embargo, si alguien solicita cambios o sugiere algo, debes comunicar tus razones de forma clara y justificada.

4. Participa en el intercambio de revisiones.
No seas solo un espectador que genera código para ser revisado. Considera que independientemente de tu nivel, la experiencia que se obtiene leyendo código al máximo no se ve superada por nada.

## Conclusión

Estamos en el año 2023, y la IA nos acompaña a diario en nuestras actividades, algunas prácticas desaparecerán pero los diferenciadores permanecerán. Una máquina puede decirnos qué está mal o dónde se puede mejorar una parte del código, sin embargo, la calidez, la empatía y el apoyo que otro ser humano puede brindarnos no se puede reemplazar (todavía), sigamos practicándolo y demos lo mejor de nosotros en todos los procesos en los que participamos.
