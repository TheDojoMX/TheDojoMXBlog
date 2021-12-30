---
title: "El tiempo monótono"
date: 2021-12-26
author: Héctor Patricio
tags: monótono tiempo conteo
comments: true
excerpt: "¿Cómo se cuenta el tiempo en una computadora? En este artículo hablaremos del tiempo monótono, un contador en el qye puedes confiar para hacer calculos relativos a periodos de tiempo en tus programas."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1120/v1639894527/daniel-mirlea-Zpq06Q5ltJY-unsplash_mhq5ms.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_320/v1639894527/daniel-mirlea-Zpq06Q5ltJY-unsplash_mhq5ms.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Saber cuánto tiempo ha pasado desde cierto evento en nuestro programa es algo que podemos requerir en algunos casos. Uno de los casos que más he visto, es cuando se está midiendo el tiempo que tarda una parte del programa manualmente.

El tiempo monótono es un concepto que todo programador debería conocer, para evitar errores y código frágil al _medir_ el tiempo en los programas.

## El reloj de "pared"

Lo primero que se nos viene a la cabeza cuando se trata de medir el tiempo entre dos eventos de nuestro programa es usar alguna función de nuestro lenguaje de programación que obtenga la fecha y hora actual del sistema. Un ejemplo en Python sería:

```python
import time

start = time.time()
# hacer algo (lo que queremos medir)
end = time.time()
diff = end - start

print(diff)
```

Esto puede parecer inofensivo, pero tiene una falla que hace a nuestro programa frágil ante eventualidades fuera del sistema. La función `time.time()` devuelve un número de segundos desde el 1 de Enero de 1970 (esta fecha conocida como el **Epoch**) como un flotante. Este número siempre será incremental, es decir, no _debería_ devolverte un número menor que una llamada previa. Sin embargo, para calcular ese número de segundos (conocido como el **Tiempo Unix**), Python se basa en la hora del _sistema_ en el que está corriendo el programa.

¿Alcanzas a notar por qué esta forma de calcular cuánto tiempo ha pasado desde un evento es frágil? Por ejemplo, imagina que entre una medida de tiempo (en nuestro programa, la variable `start`) y la siguiente(`end`), ocurriera un cambio de hora en el sistema. Puede ser que alguien esté jugando con las configuraciones o que por pura casualidad el sistema haya ajustado el tiempo por uno de los segundos de ajuste de nuestro calendario (leap seconds) o que corra durante el cambio de hora por el horario de verano.

Todas estas circunstancias podrían afectar como mide el tiempo tu programa si usamos el reloj del sistema. Es aquí en donde entra el tiempo o reloj monótono.

## El tiempo monótono

El reloj monótono es un contador del sistema que sólo avanza hacia adelante contando a partir de un punto arbitrario en el pasado. Este reloj no tiene conexión con el calendario y el tiempo real del sistema, sino que siemplemente sirve para medir el tiempo que ha pasado (**siempre en aumento**) desde el punto que se eligió.

Así, este reloj es confiable para medir el tiempo que pasó entre dos eventos, podemos tener la seguridad de que el una llamada posterior a la lectura de este reloj _siempre_ va a devolver algo mayor que la lectura anterior.

La manera de usarlo en Python también es mediante el módulo `time`:

```python
import time

start = time.monotonic()
# hacer algo (lo que queremos medir)
end = time.monotonic()
diff = end - start
print(diff)

```

La función `time.monotonic()` devuelve el tiempo monótono como un flotante en segundos. Con estas dos puntos que recorren un


Con vergüenza te comento que la primera vez que escuché de este concepto fue con más de 10 años de carrera, mediante el libro [Elixir para Alquimistas](https://books.altenwald.com/book/elixir) de Manuel Rubio, un libro que recomiendo mucho.



