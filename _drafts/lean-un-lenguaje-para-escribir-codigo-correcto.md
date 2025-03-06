---
title: 'Lean: un lenguaje para escribir código correcto'
date: 2025-03-01
author: Héctor Patricio
tags: lean programación-funcional verificación formal
comments: true
excerpt: >-
  Cada vez es más importante crear sistemas que estén bien verificados y que
  provean garantías sobre su funcionamiento. Lean te puede ayudar a lograrlo.
header:
  overlay_image: >-
    https://res.cloudinary.com/hectorip/image/upload/c_scale,w_1400/v1702275274/shubham-dhage-ONtKHht3aOE-unsplash_sgwtqx.jpg
  teaser: >-
    https://res.cloudinary.com/hectorip/image/upload/c_scale,w_400/v1702275274/shubham-dhage-ONtKHht3aOE-unsplash_sgwtqx.jpg
  overlay_filter: 'rgba(0, 0, 0, 0.5)'
---

La verificación de sistemas es muy importante para lograr aplicaciones que se
encarguen de tareas importantes, en las que no se puede permitir que el software
falle durante su ejecución en manos de los usuarios. Por ejemplo, sistemas que
manejan una gran cantidad de dinero, maquinaria industrial, los programas
que controlan naves espaciales, aviones o vehículos. A este software se le
llama de **misión crítica**, ya que vidas o grandes cantidades de recursos
dependen de él.

La verificación de sistemas se encarga de asegurarnos que no tenemos ningún
hoyo lógico en nuestro programa, es decir, que no hay ningún error en la
parte de la lógica que vaya a hacer fallar el software mientras se ejecute.
Sabemos que una falla lógica (una división por cero, un ciclo infinito, un cálculo erróneo,
un tipo de dato no esperado y muchas otras cosas) puede causar cualquiera de las
siguientes consecuencias:

- El software entrega una respuesta incorrecta
- El software se cuelga y no responde
- El sistema colapsa y se reinicia
- El sistema toma acciones incorrectas

Para asegurarnos de crear software más confiable, existen lenguajes que nos permiten
probar que nuestros sistemas hacen lo que queremos que hagan. Uno de ellos es
[Lean](https://leanprover.github.io/), del que hablaremos en este artículo.

## ¿Qué es Lean?

**Lean** es un lenguaje de programación para crear sistemas verificados.
Lean también es un probador de teoremas interactivo, así que es una gran herramienta
para científicos y matemáticos que quieren verificar sus ideas.
Fue creado por **Leonardo de Moura** mientras trabajaba en **Microsoft Research**. Lean 4
es la última versión al momento de escribir este artículo.

## Introducción a Lean

Para empezar a usar Lean puedes seguir las instrucciones de la
[documentación oficial](https://leanprover.github.io/lean4/getting_started.html).

## Tu primer programa en Lean

Creemos un programa en Lean para verificar algo sencillo: el algoritmo de Luhn. Este
algoritmo se usa para validar los números de las tarjetas de crédito. 

```lean
def luhn_check (n : ℕ) : bool :=
begin
end
```

## Conclusión

La verificación de sistemas es algo de lo que no te podrás escapar si quieres
hacer software confiable que cumpla misiones importantes.
