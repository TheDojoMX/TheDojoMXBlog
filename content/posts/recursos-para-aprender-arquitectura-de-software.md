---
title: "Recursos para aprender Arquitectura de Software"
date: 2020-07-15
author: "Héctor Patricio"
tags: ['podcast', 'thedojomx', 'arquitecturaarquitectura_de_software', 'libros']
description: "¿Qué es la arquitectura de software y cómo puedes empezar a aprenderla? Aquí te damos un resumen de una plática muy interesante que tuvimos."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1594271692/EC077014-9C45-4FCA-A0BA-7CB7B0D25FAB_l9gvh7.jpg"
draft: false
---

Tuvimos una plática con [Agustín Ramos](https://twitter.com/machinesareus) acerca de la arquitectura de software y lo que debes aprender para practicarla. Este pequeño artículo incluye nuestro resumen y las recomendaciones de Agustín.

## ¿Qué es la arquitectura de software?

La arquitectura del software incluye el **diseño del sistema** a alto nivel: la descomposición del sistema en módulos, la descripción de las responsabilidades de cada uno y sus relaciones.

También incluye las prácticas y herramientas que permitirán que el proyecto cumpla con los **atributos de calidad** o requerimientos no funcionales.

Todo lo anterior está basado en un análisis de las _funciones_ y _atributos de calidad_ del sistema.

# El proceso

En la plática tocamos 5 etapas del desarrollo de una arquitectura:

1. **Descubrimiento y definición de los atributos de calidad.** Básicamente consiste en entender el problema, escuchar a todos los involucrados en el proyecto y definir los atributos del software que no están directamente relacionados con la funcionalidad, pero que debe de cumplir.

2. **Diseño del sistema.** Generalmente te ayudarás de estilos de arquitectura y patrones de diseño para llegar a los objetivos funcionales y no funcionales.

3. **Validación del diseño.** Mediante la creación de prototipos se puede validar que las asunciones principales acerca del diseño y su relación con los atributos de calidad se cumplen. Esto puede derivar en _cambios_ sobre el diseño que lo mejoren.

4. **Comunicación del diseño.** Después de definir la arquitectura es importante comunicar el diseño al equipo mediante un exposición directa y la documentación. Esta documentación debe incluir la mayor información posible sobre la razón de las decisiones y la evolución de la arquitectura.

5. **Seguimiento del diseño.** Esto incluye varias cosas:
    * _Verificación de que el equipo está siguiendo el diseño._ Esto se logra con revisiones constantes con el equipo: programación en parejas y revisión de código.
    * _El diseño nunca está está escrito en piedra_. Después de las revisiones de código se descubrirán cosas que no están funcionando como se esperaba, por lo que será necesario modificar el diseño y dejar registro de los cambios y las decisiones tomadas.

## Consejos específicos

Los arquitectos de software deben encontrar la solución más simple posible porque si no va a ser rígida.

Acerca de la **documentación**, Agustín recomienda, exponerla al equipo en una junta y hacer un video de esto, que se le pase a cada integrante del equipo. Se puede seguir el marco llamado ["Arquitectura 4 + 1"](https://www.cs.ubc.ca/~gregor/teaching/papers/4+1view-architecture.pdf) que se compone de:

* Vista de Componentes
* Vista de Desarrollo
* Vista de Procesos
* Vista Física
* Vista de Casos (Este es el +1)

Además, tenemos que mantener una bitácora de los cambios y los factores que los impulsaron, esto puede ser mediante los [Architectural Decision Records](https://adr.github.io/).

## Cómo empezar

Agustín nos recomendó algunos recursos para que empieces a aprender:

- [Object Design - Rebecca Wirfs-Brock](https://www.goodreads.com/book/show/179204.Object_Design?from_search=true&from_srp=true&qid=3yFmpRp03n&rank=6)
- [Software Architecture in Practice](https://www.goodreads.com/book/show/70143.Software_Architecture_in_Practice?from_search=true&from_srp=true&qid=mnXRSoVML7&rank=1)
- Como alternativa al libro anterior  se recomienda Technical Report sobre arquitectura del Software Engineering Institute, encontré varios, tienes un ejemplo [aquí](https://pure.au.dk/portal/files/20484966/tech-report-5.pdf).
- [Design it! - Micheal Keeling](https://pragprog.com/titles/mkdsa/)
- La serie [Pattern-orinted Software Architecture]()


Para aprender patrones de diseño se habló de los siguientes libros:

- [Patrones de Diseño - Erich Gamma, et Al.](https://www.amazon.com.mx/dp/0201633612?tag=amz-mkt-chr-mx-20&ascsubtag=1ba00-01000-a0087-mac00-other-nomod-mx000-pcomp-feature-scomp-wm-5&ref=aa_scomp)
- [The patterns handbook](https://www.amazon.com/Patterns-Handbook-Techniques-Strategies-Applications/dp/0521648181)
- La serie [Pattern language of program design (5 libros)](https://www.amazon.com.mx/Pattern-Languages-Program-Design-Coplien/dp/0201607344/ref=sr_1_3?dchild=1&keywords=Pattern+Languages+of+Program+Design&qid=1594823984&s=books&sr=1-3)

Y entre los libros que se mencionan como la fuente de las ideas de patrones y diseño:

- [The nature of order de Christopher Alexander](https://www.amazon.com.mx/Phenomenon-Life-Building-Nature-Universe/dp/0972652914/ref=pd_sim_14_1/132-2199838-9714154?_encoding=UTF8&pd_rd_i=0972652914&pd_rd_r=43c91cc2-6447-4629-a6d7-fb29dc8fd2d7&pd_rd_w=gNuac&pd_rd_wg=g8gOe&pf_rd_p=a62f455d-612d-4136-9fd7-44067fe2cd11&pf_rd_r=86FX03JZ655BENFVMSC0&psc=1&refRID=86FX03JZ655BENFVMSC0) y los otros libros de él como [A timeless way of building](https://www.amazon.com.mx/Professor-Department-Architecture-Christopher-Alexander/dp/0195024028/ref=pd_sim_14_3/132-2199838-9714154?_encoding=UTF8&pd_rd_i=0195024028&pd_rd_r=c4dd6dad-be5f-4a11-a037-a4ecd8f56915&pd_rd_w=CYjKZ&pd_rd_wg=x61DA&pf_rd_p=a62f455d-612d-4136-9fd7-44067fe2cd11&pf_rd_r=JWAJ48WRNHYPDZ8RC2R1&psc=1&refRID=JWAJ48WRNHYPDZ8RC2R1)
- [The art of Scalability](https://www.amazon.com.mx/Art-Scalability-Architecture-Organizations-Enterprise/dp/0134032802/ref=sr_1_1?__mk_es_MX=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=the+art+of+scalability&qid=1594824264&s=books&sr=1-1)

## El capítulo

De todos modos no te pierdas el capítulo, que estuvo muy bueno:

<iframe width="560" height="315" src="https://www.youtube.com/embed/vfu5PsSH7us" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

