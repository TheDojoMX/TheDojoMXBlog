---
title: "A Philosophy of Software Design: Crea módulos de propósito general"
date: 2020-04-02
author: "Héctor Patricio"
tags: ['APoSD', 'módulos', 'generalización', 'module', 'class']
description: "Crear módulos o clases demasiado específicas puede llevar a tu código a ser difícil de mantener, veamos por qué te conviene crear módulos de propósito general."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1584726013/D750CDED-7745-4A56-8B3D-5CD33D2893E6_vqdgzb.jpg"
draft: false
---

Una burla común hacia los programadores es que todo lo queremos hacer _demasiado general_. Nos piden una funcionalidad y en ese momento empezamos a pensar en todos los casos en los que podría ser usado en el universo.

Hay muchos consejos **en contra** de escribir código que abarque
muchos casos. En este artículo vamos a hablar de las ventajas y
desventajas de módulos de **propósito general**, es decir, vamos a
hablar en contra de la sabiduría popular.

Pero además hablaremos **del equilibrio** y cómo lograrlo.

## Especificidad de un módulo

Puedes pensar en la especialización de un módulo (o del código en general) como en continuo que va desde algo que se puede utilizar en muchos muchos casos (las bibliotecas estándar) hasta código que sólo sirve para un uso muy acotado y es muy difícil de cambiar.

![Gráfica del continuo de especificidad](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1585279283/7655B57E-A45D-4832-A0D6-41670C22D6CA_boy7ej.png)

Un módulo específico está dedicado a cumplir _una sola función_ en el sistema y sólo se puede usar para eso. Si los pensáramos como conectores para un dispositivo, como un celular, podrías decir que es la conexión especial que Nokia, Apple o Sony Ericsson se inventaron en su tiempo para cargar.

Un módulo de propósito general se puede usar para varios casos con _poca modificación_, o creando un módulo más específico a partir de él. En el mismo ejemplo de los dispositivos electrónicos puede compararse al estándar USB que sirve para múltiples cosas y puede ser usado en muchos aparatos diferentes.

## Módulos específicos

El caso más extremo del código específico es el que llamamos _hardcoding_. Es tan específico que sirve sólo para una instancia muy pequeña de un problema y _no es fácil de modificar en producción_.

Se entiende como _hardcoding_ a poner directamente en el código un valor fijo que pudiera variar en el futuro: configuración de IP's, conexión a bases de datos, nombres de usuario, etc. Y es uno de los casos extremos de [programación táctica](https://blog.thedojo.mx/2020/02/11/a-philosophy-of-software-design-programacion-tactica-vs-estrategica.html#desarrollo-t%C3%A1ctico). Por lo tanto, y esto todos lo sabemos, es una **muy mala  práctica** para crear código mantenible e incluso para la practicidad en el desarrollo.

El siguiente nivel de especificidad y con el que casi todos nos quedamos contentos es cuando creamos un módulo (una clase, por ejemplo), para una _función específica_ de nuestro sistema y que _sólo puede usarse ahí_.

Usemos como ejemplo un programa para registrar publicaciones impresas como libros, revistas, periódicos, panfletos, etc. Una manera de diseñarlo es creando en el módulo una función para cada tipo de publicación:

```python

def registrar_libro(...):
  pass

def registrar_revista(...):
  pass

...

def registrar_panfleto(...):
  pass

```

Esto nos llevaría a tener una interfaz muy amplia y generalmente funciones o módulos poco profundos. Además, si agregamos un nuevo tipo de publicación se tendría que crear una nueva función para atenderlo.

## Módulos de propósito general

Un módulo de propósito general puede tener, casi siempre, una interfaz más sencilla que un módulo de propósito específico. Siguiendo con el ejemplo de los libros, en vez de crear una función para cada uno de los tipos de publicación se podría crear una general:

```python

def registrar_publicacion(...):
  pass


def registrar_tipo_de_publicacion(...):
  pass

```

Esto permitiría tener una interfaz más sencilla con aplicaciones _más amplias_, con más usos.

El ejemplo mencionado por [A Philosophy of Software Design](https://amzn.to/2GdeHi5) es el de un editor de texto con interfaz gráfica. La clase encargada de almacenar el texto en memoria deber tener las capacidades para modificarlo.

Piensa en las operaciones que los editores de texto dan: insertar texto, borrar texto hacia adelante, borrar texto hacia atrás, seleccionar, copiar, pegar. Ousterhout menciona que implementar una función _específica_ para cada una de estas operaciones crea complejidad no necesaria. Un diseño más general permite hacer tres operaciones: insertar texto, borrar texto y mover el cursor. Todas las operaciones se pueden lograr con estas otras tres, teniendo una interfaz más sencilla.

Este debería ser nuestro objetivo: crear interfaces sencillas que hagan mucho por nosotros.

## ¿Por qué hacer módulos de propósito general?

El principal motivo que [A Philosophy of Software Design](https://amzn.to/2GdeHi5) menciona es que los módulos de propósito general [son más profundos](https://blog.thedojo.mx/2020/03/02/a-philosophy-of-software-design-los-modulos-deben-ser-profundos.html#dise%C3%B1o-de-m%C3%B3dulos) es decir, encierran más funcionalidad con una interfaz pequeña.

Hacerlo contribuye a que tu código esconda más información y por lo tanto su uso sea más simple.

Además los módulos demasiado específicos crean **acoplamiento** en el sistema que no es sano: los usuarios del módulo tienen que adaptarse a una interfaz mu específica.

Los módulos de propósito general te pueden quitar trabajo en el futuro, al requerir menos modificación y poder reutilizar su código para crear nuevas funcionalidades, como en el caso extremo de las bibliotecas estándar.

Y por último una interfaz demasiado específica puede filtrar información no necesaria.

## Equilibrio

La clave para elegir qué tan específico es tu módulo es la forma en la que lo vas a utilizar: tu pieza de código tiene que ser **tan general** como puedas sin que dificulte demasiado su uso actual.

Tienes que evaluar qué tanto desvía del uso específico inmediato el que modifiques la interfaz para crear algo que pueda ser reutilizado.

## Conclusión

Crear módulos de "no tan específicos" puede ayudarte a:

1. **Ocultar mejor la información**.
2. **Crear interfaces más concisas**.
3. **Reutilizar mejor el código**.

Tienes que buscar el equilibrio entre crear un módulo tan específico que sólo uses una vez, contra un módulo que cubra todos los casos del mundo. El equilibrio está en un módulo que no sea difícil de utilizar para tu problema a la mano pero que puede ser (o este siendo) utilizado en varios lugares y de varias formas si es el caso.

Tu "yo" del futuro te agradecerá si logras encontrar el equilibrio, porque podrás crear funcionalidades más rápido, _acelerar_: una característica de la programación estratégica.

En el próximo artículo hablaremos de los sistemas en capas y cómo aprovechar sus particularidades para crear diseños que dominen la complejidad.
