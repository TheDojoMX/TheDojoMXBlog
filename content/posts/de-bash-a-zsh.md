---
title: "De Bash a Zsh"
date: 2020-07-16
author: "Alejandro Santamaría"
tags: ['shell', 'zsh', 'bash', 'terminal']
description: "Zsh es el nuevo shell default de MacOS Catalina. Entiende las principales diferencias entre Bash y Zsh."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1586794238/B29C980A-0E0F-444F-9F25-EFAB95FDBD4E_r9qk5v.jpg"
draft: false
---

Con la reciente liberación de MacOS Catalina, Apple anunció que entre alguno de los cambios al sistema operativo, se utilizará a partir de esta versión un nuevo _shell_ que de manera regular se utilizaba en la app Terminal y en otras aplicaciones utilizadas por los desarrolladores para interactuar con la Mac a través de la línea de comandos.

El shell que se utilizaba previo a esta versión era **Bash** (_Bourne Again Shell_) y el que se utilizará ahora es **Zsh**.

## ¿Qué es un shell?

En resumen, un shell es un programa que permite **controlar la computadora a través de comandos de texto**, normalmente se trata de interfaces de texto interactivo, donde el usuario podrá ir **tecleando comandos para obtener información** o ejecutar comandos y obtener resultados a través de la misma interfaz.

A lo largo de la historia se han creado diferentes shells, cada uno con una serie de comandos que ponen a disposición de los usuarios **funcionalidades específicas** de sus sistemas operativos. ¿Y porqué estaría alguien interesado en usar un shell y una línea de comandos para controlar una computadora? Para entenderlo hay que viajar un poco en el tiempo.

### Historia

Inicialmente, controlar una computadora era una tarea difícil, las primeras de ellas se controlaban mediante diferentes dispositivos (interruptores, tarjetas perforadas, etc.) que "cargaban" en memoria las distintas piezas de información que serían procesados en forma de programas. Este proceso era regularmente **tedioso y sujeto a errores**.

En algunos casos, el primer programa que se cargaba en memoria era un programa que permitía cargar instrucciones adicionales a través de la lectura de datos en las mismas tarjetas perforadas. De igual forma, los resultados de la ejecución normalmente se plasmaban en papel o tarjetas similares a las que se utilizaban para su carga.

Conforme fueron evolucionando los computadores, los programas permitieron el uso de dispositivos de entrada más amigables para el usuario de la computadora, como Teletipos, que permitían enviar comandos desde teclados y terminales remotas al ordenador (remoto en un sentido práctico, quizás de un cuarto a otro). Esta forma de transmitir comandos y obtener resultados era mucho más sencilla que estar cargando información a través de interruptores o tarjetas perforadas.

La pregunta natural es: si esto fue la primer evolución hacia un uso más sencillo de las computadoras, **¿por qué se sigue utilizando?**

Aunque la evolución de las computadoras ha seguido su curso y la interacción Humano-Computador ha avanzado en diferentes vertientes, por ejemplo, **mediante la implementación de interfaces gráficas**, el uso de la interfaz de línea de comandos se ha mantenido vigente por diversas razones:

1. Por su **versatilidad**, es posible utilizarlo para resolver distintos tipos de problemas y con distintos tipos de opciones que harían muy difícil su integración completa en una interfaz gráfica.

2. Por su **poder**, al tener acceso a las funciones centrales del sistema operativo, también contempla casos de uso para los cuales las interfaces gráficas no están preparados.

3. Permite crear programas que hacen uso de las capacidades nativas y extendidas del sistema operativo y ejecutar dichos programas o scripts en distintas modalidades, por ejemplo, de manera repetitiva a través de trabajos programados (cron jobs) o en conjunto con otros programas (por ejemplo con ambientes de desarrollo integrados). A esto le podemos llamar **automatización de tareas**.

El programa de shell específico (en este caso Bash o Zsh), definen su interfaz con el usuario, no sólo en la manera en la que presentarán la linea de comando sino también en las **capacidades y comandos que soportan de manera nativa**, en general, podemos encontrar algunas de estas características:

* Una sintaxis que define los comandos y secuencias de comando que el shell 'entenderá'.
* Comandos que darán acceso a las 'operaciones' que el shell puede ejecutar .
* Funciones que permiten agrupar comandos para ejecutar labores más complejas.
* Parámetros para almacenar valores para su uso durante la ejecución de las funciones y comandos.
* Expansión que define la forma en la que los parámetros en un comando son aplicados.
* Flujo y redirección que controla las entradas y salidas de y desde los comandos.
* Ejecución que define lo que sucede cuando cada comando corre.
* Scripting que permite ejecutar archivos que contienen una lista de comandos y/o funciones.

## ¿Porqué razón puede estar cambiando Apple de un shell a otro?

Existen varias posibilidades, la primera de ellas es que aunque Apple utiliza Bash desde OSX Jaguar, no había actualizado Bash desde la versión 3.2 liberada en el 2007, es decir casi el mismo año en el que se liberó el primer iPhone. Es probable que una de las razones por las que esto sucedió fue que Bash cambió su licencia de uso de **GNU GPL 2 a una licencia GNU GPLv3**, y dicho cambio incluía restricciones que quizás no fueron del todo favorables a Apple.

Así que migrar a Zsh es una opción refrescante. La versión que está incluida en Catalina es la 5.7.1 y utiliza una versión de licenciamiento **MIT que es menos restrictiva que la GPLv3**.

## ¿Qué sucederá con Bash, tendré que dejar de usarlo?

No necesariamente, aunque Zsh será el shell por default para todas las nuevas cuentas de usuario creadas en macOS Catalina, si tu hiciste un upgrade del Sistema Operativo, tu cuenta seguirá utilizando por default Bash. Pero siempre tendrás opción de configurar el shell que desees por default de manera voluntaria, incluso a alguno distinto a Zsh o Bash.

A nivel general, Bash y Zsh tienen un nivel de compatibilidad bastante alto ya que **ambos están basados en el aún más antiguo Bourne Shell**, de tal forma que la mayoría de los scripts y comandos existentes funcionarán sin ningún cambio en Zsh.

La ventaja real de Zsh es la inclusión de funcionalidades que hacen trabajar con él más fácil (funcionalidades no incluidas por default en la versión vieja de Bash), entre algunas de mis funcionalidades favoritas están:

* Auto completado de comandos
* Auto corrección de comandos
* Integración con algunos sistemas de uso común para desarrolladores (git)

## ¿Qué sucederá con mis scripts hechos en Bash?

En general, correrán de igual forma a como lo venían haciendo, sin embargo en casos muy peculiares podrías requerir modificarlos o simplemente agregar #!/bin/bash (_shebang_) para forzar a que el script utilice el shell de Bash que sigue incluyéndose en MacOS.

Puedes usar temporalmente uno u otro shell simplemente invocando su nombre en la línea de comandos (`zsh` o `bash`).

En la Mac, podrás configurar el shell default en las Preferencias del Sistema, en el panel de Usuarios y Grupos, podrás seleccionar la cuenta de un usuario y en las Opciones Avanzadas podrás seleccionar uno de los shells disponibles.

## Conclusión y referencias

Dominar tu shell **hará que tu trabajo diario sea más sencillo** ya que podrás configurar funcionalidades que aumenten tus capacidades como desarrollador y en conjunto con el conocimiento a profundidad de tu interfaz de desarrollo, podrá hacerte mucho más eficiente al momento de administrar y ejecutar comandos que tengan que ver con tus proyectos.

Algunos recursos que te ayudarán:

* La [documentación de Zsh](http://zsh.sourceforge.net/)
* Configuración Zsh es mediante [Oh My Zsh](https://ohmyz.sh/)
* ¿Donde se configuran las funcionalidades de Zsh? En `~/.zshrc`.
* ¿Cómo  saber que shell estoy usando?

```bash
echo $0
```
o

```bash
echo $SHELL
```

* ¿Cómo configurar Zsh como mi shell default?

```bash
chsh -s /bin/zsh
```

* ¿Cómo activar el autocomplete?

```bash
autoload -U compinit && compinit
```

* ¿Cómo activar la extensión para git?

```bash
autoload -Uz vcs_info
```

* ¿Cómo configurar el cambio de directorio automático?
```bash
setopt autocd
```

### Referencias

* [Bash academy](https://www.bash.academy/)
* [Discusión en YCombinator](https://news.ycombinator.com/item?id=10737639)
* [Zsh tips](http://www.rayninfo.co.uk/tips/zshtips.html?LMCL=bNg6o6)
* [10 trucos de Zsh](http://leahneukirchen.org/blog/archive/2008/02/10-zsh-tricks-you-may-not-know.html)
* [Zsh Guide](http://zsh.sourceforge.net/Guide/zshguide.html)
* [Advanced Bash-Scripting Guide](http://www.tldp.org/LDP/abs/html/)
* [Bash by example](http://matt.might.net/articles/bash-by-example/)
* Libro: [From Bash to Zsh](https://amzn.to/32phs95)
