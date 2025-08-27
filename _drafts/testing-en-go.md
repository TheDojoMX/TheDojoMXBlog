---
title: "Testing en Go"
date: 2025-08-19
author: Héctor Patricio
tags: go golang testing unit-testing
comments: true
excerpt: "Aprende los conceptos fundamentales de testing en Go, junto con herramientas prácticas para hacerlos de forma práctica y sencilla."
header:
  overlay_image: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1747718313/mariola-grobelska-EJBwRJZMOCQ-unsplash_rugsm8.jpg
  teaser: https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1747718313/mariola-grobelska-EJBwRJZMOCQ-unsplash_rugsm8.jpg
  overlay_filter: rgba(0, 0, 0, 0.5)
---

Las pruebas de software son una parte importante de cualquier proyecto que
queremos que perdure en el tiempo. Los lenguajes modernos, como Go, tienen
herramientas que te permiten hacer pruebas de forma efectiva y sencilla, sin
tener que pelearte con instalaciones o configuraciones complejas.

Hablemos de los diferentes tips de testing y cómo puedes hacerlos en Go.

## Testing básico

El tipo de pruebas más básico que podemos hacer son las pruebas unitarias.

Las pruebas unitarias son pruebas que se hacen sobre una unidad de código.

Por ejemplo, si tenemos una función que suma dos números, podemos hacer una
prueba unitaria para verificar que la función suma dos números correctamente.

```go

func Sum(a, b int) int {
  return a + b
}
```

La podemos probar con un test unitario de la siguiente manera:

```go

func TestSum(t *testing.T) {
  result := Sum(1, 2)
  if result != 3 {
    t.Errorf("Sum(1, 2) = %d; want 3", result)
  }
}
```


