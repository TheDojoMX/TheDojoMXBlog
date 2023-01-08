---
title: "Ejercicio: programando un perceptrón con Python"
date: 07-01-2023
author: Héctor Patricio
tags: machine-learning ia inteligencia-artificial
comments: true
excerpt: "Programemos un perceptrón en Python para entender a fondo como funciona y poder construir sobre eso para temas más complejos."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_crop,h_600,w_1200/v1673056123/DALL_E_2023-01-06_19.47.48_-_Perceptron_artistic_digital_paint_high_quality_detailed_wpoohz.png
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_crop,h_600,w_300/v1673056123/DALL_E_2023-01-06_19.47.48_-_Perceptron_artistic_digital_paint_high_quality_detailed_wpoohz.png
  overlay_filter: rgba(0, 0, 0, 0.5)
---

En este post platicaremos acerca de cómo funciona un perceptrón con un ejemplo de código y las técnicas que utiliza para aproximar una función a partir de datos.

Si no tienes claro lo que es un perceptrón, puedes leer nuestro [artículo anterior](/2021/03/25/intro-a-machine-learning-entendiendo-perceptron.html){:target="_blank"}. Ahí también explicamos las bases de funcionamiento. En este artículo lo vamos a ilustrar de la manera más sencilla posible.

## El conjunto de datos

Recuerda que para poder crear un algoritmo de machine learning necesitamos un conjunto de datos, ya que el punto es que este algoritmo _aprenda_ de estos datos.

Los datos que un perceptrón puede clasificar deben poder ser separados en mínimo dos clases por alguna característica, ya que si representáramos al perceptrón como una función, es un línea recta en un plano de dos variables (o su equivalente dependiendo del espacio y sus dimensiones, lo que en para más de tres dimensiones llamamos un _hiperespacio_ matemáticamente).

No es necesario que los datos _sólo_ puedan estar divididos en dos clases, por ejemplo, imagínate un conjunto de datos que representa los dígitos escritos a mano, del 0 al 9 (este es conocido como el [MNIST dataset](https://www.tensorflow.org/datasets/catalog/mnist)). Cada dígito es una clase, pero un perceptrón nos puede servir para clasificar un solo número, por ejemplo, el 5. El perceptrón serviría para clasificar si un dígito es un 5 o no, lo importante es que el conjunto de datos que representa el 5 sea más o menos separable de los demás dígitos.

Con esto te puedes empezar a dar cuenta de que el perceptrón es el bloque de construcción más básico de las redes neuronales. Por ejemplo, ¿cómo haríamos para clasificar todos los números del conjunto del que hablamos arriba? Necesitamos un perceptrón por cada número, y tomamos el que más confianza nos devuelva.

Ahora sí veamos qué dataset usaremos nosotros. Ejemplos usando el MNIST o el [Iris](https://archive.ics.uci.edu/ml/datasets/iris) encontrarás en muchos lados, así que vamos a escoger uno diferente.
Este es una alternativa a Iris y se conoce como el [Penguin dataset](https://github.com/allisonhorst/palmerpenguins).

El conjunto de datos de los pingüinos tiene 344 registros etiquetados, cada uno con máximo 6 características (a parte de la etiqueta). Tiene 3 etiquetas diferentes: Adelie, Chinstrap y Gentoo. Las columnas del dataset son:

1. **species**: especie del pingüino, esta es la clase o etiqueta
2. **island**: isla donde fue visto el pingüino, tiene 3 valores diferentes: Dream, Torgersen, or Biscoe
3. **bill_lenth_mm**: longitud de la pico del pingüino
4. **bill_depth_mm**: profundidad de la pico del pingüino
5. **flipper_length_mm**: longitud de la aleta del pingüino
6. **body_mass_g**: masa del cuerpo del pingüino
7. **sex**: sexo del pingüino

Tenemos que explorar los datos brevemente para ver qué variables podemos usar para separar. Como este no es el objetivo de este artículo vamos a ver una imagen en la que comparan por pares las variables y seleccionemos las que nos ayuden a separar mejor las clases. Vamos a hacerlo sólamente con dos variables para que el código nos quede más sencillo y se comprenda la idea principal.

La siguiente imagen es una gráfica de dos variables: la anchura del pico (**bill_depth_mm**) y el largo de su aleta (**flipper_length_mm**). Observa qué bien separa a la clase Gentoo de las otras dos.

![Gráfica de dos variables](https://res.cloudinary.com/hectorip/image/upload/v1673111878/a1f1d1b7-d87c-478d-b67a-c344c802f4d6_spefvh.png){: .align-center}

**Nota**: para el entrenamiento de una rede neuronal se hace una exploración mucho más profunda de los datos, pero para este ejemplo no es necesario.

## Repaso del funcionamiento básico

El perceptrón es un algoritmo de aprendizaje **supervisado**, por lo que necesita datos etiquetados, es decir, _las características junto con su clase_. El trabajo del perceptrón es encontrar los parámetros para una función matemática que defina la frontera de separación entre las clases.

Esta función matemática es una línea recta en un plano de dos dimensiones, o un plano en un espacio de tres dimensiones, o un **hiperplano** en un espacio de más de tres dimensiones. Puedes pensar en todos estos términos matemáticos como el equivalente a una linea recta en cualquier espacio.

## El algoritmo

El perceptron es busca ajustar una función lineal que separa las clases. En este caso separaremos "Gentoo" de "no es un Gentoo". El algoritmos nos dirá "1" si es un Gentoo y "0" si no lo es. Una función lieneal tiene la forma:

```python
y = w1 * x1 + w2 * x2 + b
```

Con un término `wn * xn` para cada variable de entrada, y un término `b` para el sesgo. El perceptrón ajusta los valores de `w1`, `w2`, y `b` para que la función lineal se ajuste a los datos.

Podemos empezar combinando las dos variables que elegimos de la siguiente manera:

```python
y = w1 * penguins['bill_depth_mm'] + w2 * penguins['flipper_length_mm'] + b
```

**Nota**: En este ejemplo no usaremos `numpy` o `pandas`, para hacer la programación lo más tradicional posible. Más adelante nos empezaremos a meter en `numpy`, `pandas` y esas cosas que parecen magia negra.

Esto nos dará un número que tenemos que convertir en un 1 o un 0. Usemos una función sencilla. Todos lo números negativos los convertimos en un 0 y todos los positivos y el 0 en un 1. Esto se puede programar sencillo. Vamos a llamar a esta función `paso`:

```python
def paso(x):
    if x < 0:
        return 0
    else:
        return 1
```

Ahora podemos usar esta función para convertir la salida de la función lineal en un 1 o un 0:

```python
def clasificar(x, w1, w2, b):
    """Recibe una fila de datos y devuelve 1 si es Gentoo y 0 si no lo es"""
    return paso(w1 * x["bill_depth_mm"] + w2 * x["flipper_length_mm"] + b)
```

Nuestra función de clasificación ya está lista. Pero el trabajo del perceptrón es encontrar los valores de **los parámetros**: `w1`, `w2`, y `b`. Creemos el algoritmo que define estos valores, que llamaremos `entrenar`. Esta función aprende a base de prueba y error. Para aprender hace lo siguiente:

  1. Clasifica cada dato de entrenamiento
  2. Verifica si la etiqueta es correcta (para esto necesitamos las etiquetas de los datos de entrenamiento)
  3. Ajusta sus parámetros: cambiar los valores de `w1`, `w2`, y `b` para que la función lineal se ajuste a los datos.
  4. Repite el proceso

Este proceso puede terminar por dos razones:

  1. Se alcanza un número máximo de iteraciones
  2. Se alcanza un resultado satisfactorio (ej. el número de elementos mal clasificados es menor a un umbral)

Para hacerlo sencillo vamos a hacer que el algoritmo se ejecute un número fijo de veces:

```python

def entrenar(datos, iteraciones):
    # inicializamos los parámetros, esto puede ser aleatorio o cero, como lo hacemos aquí
    w1 = w2 = b = 0
    while iteraciones > 0:
        iteraciones -= 1
        for x in datos:
            etiqueta_real = int(x["species"] == "Gentoo")
            clase = clasificar(x, w1, w2, b)

            if etiqueta_real == 1 and clase == 0:
                # Aquí tenemos un Gentoo mal clasificado, tenemos que
                # aumentar w1 y w2 para que la función lineal se acerque
                # a la etiqueta real
                w1 += x["bill_depth_mm"]
                w2 += x["flipper_length_mm"]
                b += 1  # Valor escogido arbitrariamente
            elif etiqueta_real == 0 and clase == 1:
                # Aquí tenemos un NO Gentoo mal clasificado, tenemos que
                # disminuir w1 y w2 para que la función lineal se acerque
                # a la etiqueta real
                w1 -= x["bill_depth_mm"]
                w2 -= x["flipper_length_mm"]
                b -= 1  # valor escogido arbitrariamente
        print("Iteración", iteraciones, "w1:", w1, "w2:", w2, "b:", b)
    return w1, w2, b
```

Podríamos decir que esto es básicamente todo el algoritmo del perceptrón. Ahora podemos entrenar nuestro perceptrón con los datos de entrenamiento. Antes le hacemos unas cuantas modificaciones para que sea más fácil de usar:

```python
# cargar el archivo CSV con los datos de entrenamiento como diccionario, el archivo está en la carpeta data, un nivel arriba
with open("../data/penguins.csv") as csvfile:
    data = list(csv.DictReader(csvfile))

# Limpiando los los datos, eliminando los que no tienen bill_depth_mm o flipper_length_mm
data = [
    row
    for row in data
    if row["bill_depth_mm"] != "NA" and row["flipper_length_mm"] != "NA"
]

for row in data:
    row["bill_depth_mm"] = float(row["bill_depth_mm"])
    row["flipper_length_mm"] = float(row["flipper_length_mm"])

```

Estos datos ya está listos para para ser usados. Ahora podemos entrenar el perceptrón:

```python
# Escogemos las iteraciones arbitrariamente
w1, w2, b = entrenar(data, 100)
```

Lo podemos probar con los mismos datos de entrenamiento:

```python
def probar(data, w1, w2, b):
    correctos = 0
    incorrectos = 0
    for x in data:
        clase = clasificar(x, w1, w2, b)
        etiqueta_real = int(x["species"] == "Gentoo")

        if clase == etiqueta_real:
            correctos += 1
        else:
            incorrectos += 1

      print("\n\nResultados:")
      print(f"Correctos: {correctos} - {(correctos / len(data)) * 100}%")
      print(f"Incorrectos: {incorrectos} - {(incorrectos / len(data)) * 100}%")
probar(data, w1, w2, b)
```

Y el resultado es:

```shell
Resultados:
Correctos: 219 - 64.03508771929825%
Incorrectos: 123 - 35.96491228070175%
```

Parece que nuestro perceptrón no logró ni siquiera aprender bien con los datos de entrenamiento. ¿Qué pasa si aumentamos las iteraciones, digamos a 1000?

```python
w1, w2, b = entrenar(data, 1000)
probar(data, w1, w2, b)
```

El resultado es:

```shell
Resultados:
Correctos: 342 - 100%
Incorrectos: 0 - 0.0%
```

Parece que con las suficientes iteraciones el perceptrón logra aprender a clasificar perfectamente los datos de entrenamiento. **Tip**: siempre debes dudar de un algoritmo de inteligencia artificial que clasifique perfectamente, eso puede indicar que se sobreajustó a los datos de entrenamiento y cuando encuentre datos no vistos, fallará.

Para evitarlo, necesitamos probarlo con datos que no ha visto antes. Para esto vamos a dividir los datos en dos grupos, uno para entrenamiento y otro para pruebas:

```python
# Dividir los datos en dos grupos, uno para entrenamiento y otro para pruebas
import random
random.shuffle(data)
entrenamiento = data[:int(len(data) * 0.8)]
pruebas = data[int(len(data) * 0.8):]

w1, w2, b = entrenar(entrenamiento, 1000)
probar(pruebas, w1, w2, b)

```

El resultado es:

```shell
Resultados:
Correctos: 69 - 100.0%
Incorrectos: 0 - 0.0%
```

Y como vemos, sigue funcionando bien con este dataset sencillo. Esta es le estructura básica de un perceptrón, pero en realidad le faltan muchas partes para que funcione de manera general sin gastar demasiado tiempo de cómputo. Por ejemplo, en este código simplemente sumamos o restamos el valor de las variables a w1 y w2. Estos saltos pueden ser muy bruscos y hacernos saltar fácilmente el valor que necesitamos. Para evitar esto, se usa otro parámetro para la función de entrenamiento llamado "ritmo de aprendizaje" (learning rate - lr).

Vamos a incluirlo en nuestro código:

```python

def entrenar(datos, iteraciones, lr=0.01):
    # inicializamos los parámetros, esto puede ser aleatorio o cero, como lo hacemos aquí
    w1 = w2 = b = 0
    while iteraciones > 0:
        iteraciones -= 1
        for x in datos:
            etiqueta_real = int(x["species"] == "Gentoo")
            clase = clasificar(x, w1, w2, b)

            if etiqueta_real == 1 and clase == 0:
                # Aquí tenemos un Gentoo mal clasificado, tenemos que
                # aumentar w1 y w2 para que la función lineal se acerque
                # a la etiqueta real
                w1 += x["bill_depth_mm"] * lr
                w2 += x["flipper_length_mm"] * lr
                b += 1 * lr  # Valor escogido arbitrariamente
            elif etiqueta_real == 0 and clase == 1:
                # Aquí tenemos un NO Gentoo mal clasificado, tenemos que
                # disminuir w1 y w2 para que la función lineal se acerque
                # a la etiqueta real
                w1 -= x["bill_depth_mm"] * lr
                w2 -= x["flipper_length_mm"] * lr
                b -= 1 * lr  # valor escogido arbitrariamente
        print("Iteración", iteraciones, "w1:", w1, "w2:", w2, "b:", b)
    return w1, w2, b
```

Y ahora vamos a probarlo de nuevo con 100 iteraciones y el lr default:

```python
w1, w2, b = entrenar(entrenamiento, 100)
probar(pruebas, w1, w2, b)
```

En esta versión podemos ver que con muchas menos iteraciones el perceptrón logra clasificar correctamente los datos de prueba. El resultado es:

```shell
Resultados:
Correctos: 69 - 100.0%
Incorrectos: 0 - 0.0%
```
