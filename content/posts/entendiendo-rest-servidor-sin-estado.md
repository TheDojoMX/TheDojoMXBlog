---
title: "Entendiendo REST: conexión sin estado"
date: 2019-08-03
author: "Héctor Patricio"
tags: ['REST', 'stateless', 'thomas-fielding']
description: "¿Cómo mantener la información entre peticiones en un sistema REST? Entendamos las ventajas y desventajas"
featuredImage: "https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1564879566/nick-hillier-yD5rv8_WzxA-unsplash_cthqzt.jpg"
draft: false
---

Hemos venido hablando de las características que componen a un sistema REST. En el último artículo [hablamos de la arquitectura cliente-servidor](/2019/07/04/entendiendo-rest-arquitectura-cliente-servidor.html). Esta es la primera característica fundamental de un sistema REST. Ahora pasemos a la siguiente característica-limitante que Thomas Fielding establece para los sistemas REST: **conexión sin estado**.

## ¿Qué es el estado de un sistema?

El estado de una aplicación son todos los datos que usa para operar en un momento determinado.

Como ejemplo podemos pensar en una aplicación de ventas en línea. El estado de esta aplicación, para un usuario específico son sus datos de identificación, su bolsa de compras y los productos que ha estado viendo o que tiene en su lista de deseos, así como datos que no son identificables directamente desde la interfaz de usuario como los tokens de sesión, su historial de visita de las páginas y productos (piensa en Amazon) y los productos que ha comprado anteriormente en esta página.

Todos estos datos necesarios para operar tanto a nivel interno como para la interfaz de usuario son el estado de la aplicación para este usuario. **Puedes entender el estado como el contexto de una aplicación**. Todas las aplicaciones y programas usables tienen uno. Entonces, ¿a qué nos referimos con conexiones sin estado?

## Conexión sin estado

Dando por supuesto que estamos trabajando en un sistema con arquitectura de red [cliente-servidor](/2019/07/04/entendiendo-rest-arquitectura-cliente-servidor.html), las dos partes comparten la información (el estado) necesaria para realizar las operaciones. La pregunta es: ¿en qué lado mantengo esta información durante la operación? Damos por supuesto que el almacenamiento de información a largo plazo está localizado en algún lado del servidor. Pero en el momento de la operación, ¿quién mantiene estos datos memoria operativa?

En el ejemplo del que hablamos: ¿quién mantiene en memoria la bolsa de compras del usuario, el cliente (el navegador web) o el servidor? Cualquiera de los dos podría llevarlo a cabo. Veamos los dos casos, empecemos por una conexión que "recuerda" el estado.

Imagínate la siguiente conversación:

- Cliente(C): Vamos a empezar a trabajar con el usuario *hectorip*
- Servidor(S): De acuerdo
- C: Dame su bolsa de compras
- S: Tiene estos 5 artículos guardados
- C: Comprar todos los artículos de su bolsa
- S: Ok, serán $500
- C: el cliente quiere pagar
- S: le he cobrado todo lo de su bolsa

El tipo de conversación que acabamos de ver sería una **conexión con estado**: cada uno de los mensajes depende del mensaje anterior para poder entender de qué estábamos hablando. Intenta leerla de regreso y lo notarás.

Ahora veamos cómo sería un conversación que no recuerda los mensajes anteriores:

- C: Dame la bolsa de compra de *hectorip*
- S: hectorip tiene estos 5 artículos en su bolsa
- C: hectorip quiere comprar todos los artículos de su bolsa
- S: Ok, serán $500 por todos los artículos de la bolsa de compra
- C: hectorip quiere realizar un pago por $500 por los artículos en su bolsa de compras
- S: He cobrado $500 a hectorip por el pedido de los artículos en su bolsa de compras

Si revisamos la conversación anterior, podemos entender cada mensaje leído individualmente, sin necesitar el contexto completo de la conversación.

La primera conversación (conexión con estado) tiene algunas ventajas claras:

- Los mensajes son más cortos
- La conversación es más fluída
- Se transfiere menos información de un lado a otro

Pero también tiene desventajas. ¿Qué pasa si esta conversación se interrumpe y se intenta retomar? *Hay que empezar la conversación desde cero.* ¿Qué pasa si el servidor, por algún error olvida de lo que estábamos hablando? *Hay que reiniciar la conversación.* ¿Qué pasa si quiero continuar la compra en otro servidor? *Hay que reiniciar la conversación con el nuevo servidor.*

# Características de conexión sin estado

Hablemos de las características de una conexión sin estado.

La primera característica es que *no necesitamos* que la conexión a nivel de sesión de red sea persistente, es decir, que se mantenga un canal de comunicación abierto que pueda mantener en memoria la información de los procesos actuales.

Segundo, no podemos (ni debemos) asumir que el servidor mantendrá los datos del cliente automáticamente por medio de reconocer al cliente. En cada una de las peticiones que se hacen al servidor, **deben venir todos los datos necesarios para que el servidor mantenga realice la operación**, no se puede confiar en que las peticiones anteriores transfirieron esa información y no es necesario repetirla.

Hasta ahora parece que esto presenta más problemas que ventajas. Revisemos por qué alguien querría trabajar con un sistema así.

## Ventajas de mantener el servidor sin estado

1. **Replicación de servidores**. Al no tener que mantener el estado o conexiones persistentes con una instancia del servidor, una conexión sin estado puede permitir que la petición sea atendida por cualquier instancia del código del servidor que tenga el mismo código que las peticiones anteriores, ya que toda la información necesaria para atender esas peticiones estará incluida.

2. **Escalabilidad**. Esto es una consecuencia inmediata de la ventaja anterior: poder replicar los servidores permite distribuir la carga entre muchas computadoras y aplicar técnicas de balanceo para poder atender a muchos más clientes de lo que se podría en un sistema que requiera mantener estados.

3. **Servicios más sencillos**. Quitarle la responsabilidad de mantener el contexto de las operaciones actuales a los servicios hace que su código sea más sencillo y por lo tanto más mantenible.

4. **Menos carga en los servidores**. Al no tener que mantener conexiones persistentes, ni tener que mantener procesos o memoria relacionada con los clientes con los que está operando, se reduce la carga en memoria operativa de los servidores (teóricamente). Esto también implica que el servidor ni siquiera tiene que estar corriendo mientras no esté activamente respondiendo una petición (como las funciones lambda).

La siguiente imagen ilustra una técnica común para atender a muchos clientes.

![Diagrama de replicación de servidores](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1200/v1564887852/PNG_image-428CDB12FF65-1_ojrpoo.png)

## Desventajas

1. **Complejidad de las peticiones**. La complejidad de las peticiones aumenta al necesitar mantener en el cliente toda la información necesaria para reconstruir el estado en cada petición en un servidor desde cero. Por lo tanto, la complejidad de los clientes aumenta. y el tamaño de las peticiones se incrementa.

3. **Mayor carga en la red**. Como las peticiones son más complejas y generalmente contienen más información para poder recuperar el contexto efectivamente, el viaje de información en la red es mayor en tamaño.


## Conexiones que mantienen estado

En los últimos años la mayoría de las conexiones que se levantan en programas creados con la arquitectura cliente-servidor son creados con conexiones que no mantienen el estado. Sin embargo, también se puede mantener una conexión con estado en la arquitectura cliente-servidor. Hay varias formas de lograr esto, pero la principal característica es que debe haber una manera de relacionar al cliente que está solicitando los servicios con el servidor que está atendiéndolo, por lo general la manera de hacerlo es con conexiones persistentes que se mantienen abiertas mientras el proceso de uso de los servicios dura.

Esto viene con sus propios retos, pero tecnologías actuales como [Elixir](/2019/06/02/por-que-deberias-aprender-elixir.html), Phoenix y los WebSockets hacen el camino más fácil. En otro post hablaremos de cómo podemos aprovechar esta arquitectura y en qué casos nos conviene.

## Conclusión

La segunda característica definida de los sistemas REST es importante porque permite que los servicios sean más confiables, disponibles y flexibles en tamaño (escalables). Como cada decisión que se toma en el desarrollo, esta viene con sus propias desventajas: al hacer más complejas las peticiones, la base de código es más difícil de mantener en general (del lado del cliente), pero permite características importantes en los sistemas que tienen que atender a una gran cantidad de clientes.

En el siguiente artículo hablaremos de la tercera característica de los sistemas REST: la capacidad de ser cachear información.