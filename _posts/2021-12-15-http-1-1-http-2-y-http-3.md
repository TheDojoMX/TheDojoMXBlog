---
title: "HTTP 1.1, HTTP/2 y HTTP/3"
date: 2021-12-15
author: Héctor Patricio
tags: HTTP web network
comments: true
excerpt: "HTTP es el estándar que permite que internet exista como hoy lo conocemos, hablemos de sus avances y lo que puede ofrecerte la última versión: HTTP/3."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1120/v1639894600/erick-chevez-DcS2NQF-Ers-unsplash_tbv7pu.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_320/v1639894600/erick-chevez-DcS2NQF-Ers-unsplash_tbv7pu.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

HTTP es el estándar más importante de la web actual, porque permite la transmisión de información entre los diferentes actores de la red. Hablemos un poco de su evolución como estándar para servir mejor a los intereses de la industria y de los usuarios y de su estado actual.

**TL;DR** | HTTP/3 hará que tus páginas web descarguen mucho más rápido, gracias a que trabaja de forma diferente a bajo nivel. Empieza a aprenderlo porque esto vendrá con nuevos retos para los desarrolladores.

## ¿Qué es HTTP?

El **Protocolo de Transferencia de Hyper-Texto** (**H**yper **T**ext **T**ransfer **P**rotocol) es un estándar definido en el [RFC 2616](https://tools.ietf.org/html/rfc2616) que permite la comunicación entre dos computadoras a nivel de aplicación, es decir, a nivel de software y con contenido relacionado a lo que tu aplicación de red está haciendo.

El que sea un protocolo a nivel de aplicación también implica que necesita otros protocolos debajo de él para encargarse de otras partes del proceso de comunicación, como la conexión física, la conexión de software, el transporte de datos y el enrutamiento de la información.

HTTP es un protocolo con arquitectura **cliente-servidor**, en el que un cliente hace _peticiones_ (requests) al servidor y el servidor contesta con la información solicitada, a lo que nos referimos como _respuesta_ (response).

La parte de hyper-texto nacio por la necesidad de transferir información más rica que el texto plano, es decir, con metadatos, links a otra parte de la información u otros documentos. Al agregar imágenes, videos y otro tipo de información multimedia lo estamos convirtiendo en **Hypermedia**, información relacionada entre sí que no es puro texto.

## HTTP/1.1

Este es el estándar que la mayoría de nosotros consideraríamos como "HTTP", ha estado en uso por bastante tiempo. La versión 1.0 fue liberada en 1996, pero en 1997 se liberó la versión 1.1, que es lo que la mayoría de los devs que "crecimos" junto con la web llamaríamos _HTTP_.

Las limitaciones técnicas de HTTP/1.1 son lo que han hecho que necesitemos un nuevo estándar, ya que la web actual requiere muchas más descargas que cuando se creó. En 2021 se descargan aproximadamente 1.9 MB en promedio por página, pero esto repartido en múltiples archivos HTML, CSS, JavaScript e imágenes (74 en promedio). Puedes ver más información sobre el tamaño de las páginas web aquí: [HTTP Archive - Page Weight](https://httparchive.org/reports/page-weight)

HTTP 1.1 solamente permite descargar un archivo a la vez, por lo que los navegadores tienen que abrir múltiples conexiones a un mismo servidor, limitadas por los recursos de la computadora. Esto crea un cuello de botella que puede hacer que la experiencia en web no sea óptima.

Por eso llegó HTTP/2.
## HTTP/2

En 2015 por fin llegó una especificación más adecuada para la web moderna que HTTP/1.1: [HTTP/2](https://datatracker.ietf.org/doc/html/rfc7540).

HTTP/2 se centra en la _multiplexación de conexiones_, es decir, permite mantener varias "conversaciones" con el servidor al mismo tiempo en la misma conexión. Esto permite la descarga de múltiples archivos simultáneamente sin tener que consumir tantos recursos como en HTTP/1.1.

El problema con HTTP/2 es que sigue funcionando sobre TCP, que no permite la multiplexación de conexiones, así al intentar la descarga de archivos paralelamente se pueden producir cuellos de botella ya que si se presentan problemas de descarga con un archivo, hay que esperar hasta que llegue el paquete que corrija el error, pudiendo este tardar mucho tiempo por estar en la misma conexión en la que se están descargando otros archivos.

Esto último causa que HTTP/2 sea insuficiente para las necesidades actuales, e incluso más lento que HTTP/1.1 en muchos casos de uso de la vida real: cuando las conexiones son poco estables. HTTP/2 fue bastante promovido por Google por un tiempo, pero ahora ha sido reemplazado por HTTP/3, que promete ser mucho mejor.

## HTTP/3

El último borrador del estándar fue publicado en [Mayo de 2021](https://quicwg.org/base-drafts/draft-ietf-quic-http.html#name-delegation-to-quic), o sea que es muy, muy nuevo, todavía no está en uso ampliamente y el estándar todavía no es el final.

HTTP/3 es básicamente las mejoras propuestas por HTTP/2 sobre una nueva capa de transporte que no es TCP: [QUIC](https://quicwg.org/). QUIC está basado en UDP, **pero establece la forma de crear canales con control de flujo, cifrado y multiplexación** para poder servir mejor a la web moderna.

QUIC permite [usar TLS](https://www.rfc-editor.org/rfc/rfc9000.html) para establecer los parámetros de cifrado e incluso permite adelantar el intercambio de información antes de negociar completamente los parámetros de cifrado, haciendo un poco más débil el cifrado pero incrementando la velocidad de descarga.

## Benchmarks

HTTP/3 es mucho mucho más rápido que HTTP/1.1 y mucho más _confiable y rápido_ que HTTP/2. En el artículo [HTTP/3 is Fast](https://requestmetrics.com/web-performance/http3-is-fast) podrás encontrar una comparación del comportamiento de las tres versiones variando diferentes factores, como la confiabilidad y distancia de la conexión.

## Conclusiones

Mantenernos actualizados con respecto a las nuevas tecnologías es muy importante para ofrecerles lo mejor a los usuarios de nuestro software, sean desarrolladores o usuarios finales. Si quieres empezar a usar HTTP/3 échale un ojo a tus servidores HTTP, por ejemplo [NGINX ya tiene planes para soportarlo completamente](https://www.nginx.com/blog/our-roadmap-quic-http-3-support-nginx/), [Traefik ya lo soporta de manera experimental](https://doc.traefik.io/traefik/master/routing/entrypoints/#http3), pero parece que Apache [no lo hará por ahora](https://www.reddit.com/r/apache/comments/o6a86x/why_is_apache_failing_to_implement_quic_http3/).

También si usas algún servicio de servidores administrados AWS, GCP, Azure, DigitalOcean o similar, revisa su documentación para verificar si puedes activarlo. También debes tener en cuenta que no todos los navegadores lo soportan, pero los que lo hagan se beneficiarán enormemente de que lo actives. Puedes revisar la lista de compatibilidad constantemente aquí: [Can I Use HTTP/3?](https://caniuse.com/http3).
