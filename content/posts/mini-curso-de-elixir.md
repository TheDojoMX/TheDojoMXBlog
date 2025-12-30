---
title: "Mini-curso de Elixir"
date: 2024-05-05
author: "Héctor Patricio"
tags: ['elixir', 'curso', 'beam']
description: ">-"
featuredImage: "null"
draft: true
---

En este artículo vamos aprender el lenguaje Elixir desde cero. Asumimos que ya
sabes programar, sobre todo
algún lenguaje orientado a objetos, ya que ocuparemos conceptos de estos
para hacer comparaciones y explicar algunas cosas.

Si quieres saber por qué te conviene aprender Elixir, tenemos
[otro artículo que habla de eso](/2019/06/02/por-que-deberias-aprender-elixir.html){:target="_blank"}.
Además, si necesitas recursos más extensos, este
artículo te puede dar algunos: [Aprendiendo Elixir](https://hectorip.com/2018/12/27/aprendiendo-elixir.html){:target="_blank"}.

Elixir es un lenguaje moderno que combina productividad con rendimiento. Ahora sí, empecemos.


## Instalación y preparación del entorno

La instalación, como siempre, varía dependiendo de tu sistema operativo, puedes
encontrar las instrucciones detalladas en la [página oficial](https://elixir-lang.org/install.html){:target="_blank"}.

Pero antes de que te vayas, si estás en Mac, puedes usar Homebrew con el
siguiente comando:

```bash
brew install elixir
```

Si estás en Linux en una distribución basada en Debian, puedes usar `apt`:

```bash
sudo apt install erlang-dev elixir
```

Para comprobar que lo tienes instalado, vamos usar una de las herramientas
con las que más te vas a familiarizar en Elixir, **iex**. Escribe en tu terminal:

```bash
iex
```

**iex** es un REPL (Read-Eval-Print Loop) que te permite ejecutar código
en Elixir de manera interactiva. Si ves algo parecido a esto, ya estamos
del otro lado:

![iex](https://res.cloudinary.com/hectorip/image/upload/c_scale,w_800/v1714951708/Screenshot_2024-05-05_at_17.27.40_rtaz8c.png){: .align-center}

Hagamos la primera prueba con Elixir: escribe cualquier operación matamática
que harías con el lenguaje que conoces y presiona Enter. Cuando quieras terminar
presciona `Ctrl + C` dos veces, esto te sacará de **iex**.

### Editor de código

Para escribir el código te recomiendo usar Visual Studio Code que tiene buen
soporte y buenas extensiones para Elixir. Estas son las primeras que recomiendo:

1. [ElixirLS](https://marketplace.visualstudio.com/items?itemName=JakeBecker.elixir-ls){:target="_blank"}:
Es la extensión más adecuada para soportar Elixir para Visual Studio Code.
2. [Elixir Formatter](https://marketplace.visualstudio.com/items?itemName=saratravi.elixir-formatter){:target="_blank"}:
te ayuda a formatear tu código con la herramienta oficial de Elixir
(`mix format`).

Esto es básicamente todo lo que necesitas para empezar a trabajar en Elixir.
Ahora sí empecemos con su sintaxis y características básicas.

## Sintaxis y conceptos básicos

En este tutorial no vamos a explicar ningún concepto básico de programación
que no sea específico de Elixir o de lenguajes funcionales (en realidad creo que no
existe ningún concepto exclusivo completamente de Elixir). Tampoco es el
objetivo que esto sea una referencia del lenguaje, sino subirte lo más pronto
posible a crear programas que funcionen.
