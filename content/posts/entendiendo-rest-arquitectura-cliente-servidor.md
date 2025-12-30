---
title: "Entendiendo REST: Arquitectura cliente-servidor"
date: 2019-07-04
author: "Héctor Patricio"
tags: ['REST', 'cliente-servidor']
description: "Hablemos de la arquitectura cliente-servidor y por qué es adecuada para REST."
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1260/v1562217908/krzysztof-kowalik-KiH2-tdGQRY-unsplash_v0vf7l.jpg"
draft: false
---

> El propósito de construir software no es crear una topología de interacciones específicas, o usar un tipo particular de componente; es crear un sistema que cumpla y exceda las necesidades de la aplicación. - Thomas Fielding

Ya hablamos de las [motivaciones detrás del estilo arquitectural REST](/2019/06/15/entendiendo-rest-estilo-de-arquitectura.html){:taget=blank}. Ahora empecemos con la primera de sus características o restricciones, que la empieza a definir: la arquitectura cliente-servidor.

## ¿Qué es la arquitectura cliente-servidor?

Esta arquitectura de aplicación divide un sistema en dos componentes:

- **Cliente**: Es un programa o proceso que solicita un servicio y usa la información provista para sus propios objetivos.

- **Servidor**: Programa o proceso que ofrece un conjunto de servicios y espera por peticiones para ejecutar o dar estos servicios.

La principal característica de la arquitectura cliente-servidor es que logra una _separación de responsabilidades clara_.

En palabras de [Gregory R. Andrews](https://homepages.cwi.nl/~marcello/SAPapers/And91.pdf){:target=blank}, el cliente es un proceso desencadenante mientras que el servidor es un proceso reactivo. Es decir el servidor no puede envíar datos o empezar procesos que un cliente no le ha solicitado.

La arquitectura básica de un sistema cliente-servidor es esta:

![Esquema cliente-servidor](https://res.cloudinary.com/hectorip/image/upload/v1562699566/PNG_image-ABC17A5C0944-1_wpyk2e.png)

<!-- Recordemos que todos los diseños o arquitecturas implican un intercambio de valor entre varias características, en este caso un poco de simplicidad por la separación de responsabilidades claras. -->

Veamos sus ventajas y desventajas.

## Ventajas

Hablemos de los beneficios que trae usar la arquitectura cliente-servidor.

### Separación clara de responsabilidades

La funcionalidad del sistema se divide en dos partes (por lo menos), como el nombre lo indica en parte de dar los servicios (generalmente de datos) y la parte de atender al usuario (humanos o programa) final.

El cliente y el servidor tienen funciones completamente distintas y cada uno puede cambiar por su lado sin afectar al otro, a esto le podemos llamar "evolución independiente".

El ejemplo que tenemos es el del navegador y las páginas que visitamos normalmente en internet. Mientras sigan cumpliendo con el protocolo establecido de comunicación (HTTP) van a poder seguir comunicándose y transfiriendo información, sin interferir la manera en que estén implementados sus procesos internos.

### División de complejidad

La misma división de la que hablamos en el punto anterior permite dividir la complejidad en dos partes por lo que cada una por su lado es más fácil de entender y desarrollar que el sistema completo.

Por lo tanto, se sigue el mismo principio que se usa para desarrollar software complejo en general: **divide y vencerás**. Esto permite que podamos dividir el trabajo limpiamente en diferentes etapas de desarrollo o entre diferentes equipos, que lo único que requieren es una interfaz de comunicación clara.

Esto no quiere decir que la complejidad _general_ se reduzca. De esto hablaremos en las desventajas.

### Múltiples versiones y reusabilidad

La implementación de la interfaz de comunicación es el único requisito indispensable para que un sistema cliente-servidor pueda seguir funcionando. Esto permite que un servidor pueda tener un número indefinido de clientes diferentes que puedan consumir su interfaz y viceversa. En el caso de REST implementar el servidor con la API permite crear tantos clientes como se necesite:

- página web
- aplicación móvil
- sistema embebido
- SDK para servidores

Sólo para ilustrar:

![Ilustración de cliente-servidor multi-cliente](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_800/v1562294072/PNG_image-5618E8EA3C0D-1_vk18wv.png)

Tener N versiones de los clientes o poder crear una sin tener que volver a a replicar la funcionalidad del servidor ha hecho que las API's se vuelvan sumamente populares.

### Simplificación de escalamiento

Poder tener separado el servidor permite que podamos escalarlo de forma independiente dependiendo del número de clientes a los que va a atender. Si necesitamos dar un servicio a escala mundial podemos replicar nuestros servidores (usando las arquitecturas adecuadas para esto) sin afectar a los clientes y sin que ellos se enteren y por lo tanto tengan que hacer algún cambio.

## Desventajas

Todo en la vida viene con desventajas asociadas y generalmente directamente proporcionales a sus ventajas. Y otra vez: intercambiamos valor entre diferentes partes de la aplicación. Analicemos algunas de estos intercambios que hacemos al aplicar la arquitectura cliente-servidor.

### Complejidad general aumentada

Cuando dividimos la aplicación y funciones completas en dos partes, aunque la complejidad de cada parte es menos que la general, la complejidad general aumenta porque hay que agregar elementos al sistema:

- Interfaces de comunicación entre cliente y servidor
- Mantenimiento o forma de recuperación del estado general de la aplicación
- Protocolos de comunicación de red cuando es el caso


### Centralización de la información

El servidor es el responsable de almacenar la información y procesarla para darle servicio a los diferentes clientes que los soliciten, lo cual, aunque hace más fácil su administración, representa la desventaja de tener la información centralizada en el sistema que actúa como servidor. Si este sistema se corrompe de alguna forma, los clientes necesitan otras fuentes de información para eliminar este problema.

Combinar cliente-servidor con otra arquitecturas ayuda a mitigar esta falla. Por ejemplo, se puede implementar el patrón de replicación de repositorio en el lado de los proveedores de servicio.

Pero, un momento, ¿acaso no es cliente-servidor la única arquitectura que existe para sistemas web o sistemas distribuidos?

## Otras arquitecturas

La arquitectura para aplicaciones distribuidas más escuchada es la cliente-servidor, pero no es ni de lejos la única. Analicemos otras dos arquitecturas comunes y dónde se usan. Si quieres ver la lista completa que Fielding analiza puedes revisar la sección 2 de [su tesis doctoral](https://www.ics.uci.edu/~fielding/pubs/dissertation/fielding_dissertation.pdf).

### Peer to Peer

En este estilo está compuesta por nodos equivalentes, es decir, que tiene la misma función (aunque pueden tener diferente información) y que se distribuyen la carga que soporta el sistema entero según las capacidades de cada uno y a veces se proporcionan servicios entre ellos. Un mismo nodo puede cambiar entre funciones o roles en la red dependiendo de la demanda.

En esta arquitectura no hay por definición un nodo más importante que otro y si alguno de toda la red falla, puede ser sustituido por otro si tiene la información replicada.

Las redes de torrents, el blockchain y programas como Ares o LimeWire funcionaban de esta forma.

Una red peer-to-peer puede lucir así:

![Ejemplo de red peer to peer](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_871/v1561266301/PNG_image-CC8B051C8851-1_r78hfc.png)

Las redes peer-to-peer son una de las mejores formas de crear sistemas distribuidos resistentes y descentralizados, es decir, que no concentran la información en un sólo punto que se vuelve el más delicado e importante de todos.

### Pipe and Filter

En este patrón, la información pasa por una series de "filtros" o nodos que la procesan y van dejando la información en un nuevo estado o con nuevas propiedades y que pasan la información al siguiente nodo. Este patrón es el que siguen los pipelines de datos normalmente, en el que la información que es producida por una fuente externa es procesada a través de una serie de pasos, que pueden incluir la recolección, limpieza, almacenamiento, etc.

![Ilustración de pipe and filter](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_800/v1562217820/PNG_image-C00985E33227-1_mevaqa.png)


## Conclusión

> Los estilos arquitectónicos el diseño de un sistema deben adecuarse a las necesidades de ese sistema, no al revés. - Thomas Fielding

¿A qué necesidades nos adaptamos?

A la necesidad de tener una separación clara entre las funciones de datos y procesos de negocio y las interfaces de usuario: sean usuarios finales humanos u otros programas que consumen información.

La arquitectura cliente-servidor permite simplificar el trabajo del lado del servidor al no tener que preocuparse por todas las distintas situaciones en las que sus datos o procesos van a ser usados.

Esto nos lleva a que sus procesos sean **reutilizables** por todos los clientes que sepan comunicarse con el servidor (léase: usar su interfaz). A su vez los clientes son más fáciles de crear por no tener en ellos mismos toda la lógica del negocio y poder enfocarse en las funcionalidades de la entidad al que le van servir.

Y por último, esta separación permite que el servidor sea fácil de escalar al nivel del servicio requerido.

Para los propósitos de REST la arquitectura Cliente-servidor es muy adecuada. Sus beneficios superan sus desventajas para este caso de uso particular.