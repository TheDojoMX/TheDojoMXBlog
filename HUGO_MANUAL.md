# Manual de Hugo para The Dojo MX Blog

## Comandos esenciales

### Desarrollo local
```bash
# Servidor de desarrollo con drafts
hugo server -D

# Servidor de desarrollo sin drafts
hugo server

# El sitio estara en http://localhost:1313
```

### Compilar para produccion
```bash
# Compilar sitio optimizado
hugo --gc --minify

# El sitio se genera en docs/ (configurado para GitHub Pages)
```

### Crear nuevo post
```bash
hugo new posts/mi-nuevo-post.md
```

Esto crea un archivo con el front matter basico en `content/posts/`.

---

## Estructura del proyecto

```
.
├── archetypes/          # Templates para nuevo contenido
│   └── default.md
├── config/_default/     # Configuracion
│   ├── hugo.toml        # Config principal
│   ├── params.toml      # Parametros del theme
│   ├── languages.es.toml # Config de idioma
│   └── menus.es.toml    # Menu de navegacion
├── content/             # Contenido del sitio
│   ├── posts/           # Posts del blog
│   ├── about.md         # Pagina About
│   └── _index.md        # Pagina principal
├── static/              # Archivos estaticos (imagenes, css, js)
├── themes/blowfish/     # Theme
└── docs/                # Sitio compilado (output)
```

---

## Front matter de un post

```yaml
---
title: "Titulo del post"
date: 2024-01-15
author: "Hector Patricio"
tags: ['tag1', 'tag2', 'tag3']
categories: ['categoria']
description: "Descripcion corta para SEO y previews"
featuredImage: "https://url-de-imagen.jpg"
draft: false
---

Contenido del post aqui...
```

### Campos importantes:
- `title`: Titulo del post
- `date`: Fecha de publicacion (YYYY-MM-DD)
- `tags`: Lista de etiquetas
- `description`: Resumen para SEO y cards
- `featuredImage`: Imagen destacada (opcional)
- `draft`: `true` para borradores, `false` para publicar

---

## Workflow tipico

### 1. Crear nuevo post
```bash
hugo new posts/2024-01-15-mi-post.md
```

### 2. Editar el post
Abre `content/posts/2024-01-15-mi-post.md` y escribe.

### 3. Preview local
```bash
hugo server -D
```
Abre http://localhost:1313 - los cambios se reflejan en tiempo real.

### 4. Publicar
Cambia `draft: false` en el front matter.

```bash
hugo --gc --minify
git add .
git commit -m "Nuevo post: mi-post"
git push
```

---

## Diferencias clave con Jekyll

| Jekyll | Hugo |
|--------|------|
| `_posts/2024-01-15-titulo.md` | `content/posts/titulo.md` |
| `_config.yml` | `config/_default/hugo.toml` |
| `bundle exec jekyll serve` | `hugo server` |
| `bundle exec jekyll build` | `hugo` |
| Liquid templates `{{ }}` | Go templates `{{ }}` |
| Front matter con `excerpt:` | Front matter con `description:` |
| `_layouts/` | `themes/blowfish/layouts/` |

---

## Configuracion del theme (Blowfish)

El archivo `config/_default/params.toml` controla el theme:

```toml
# Apariencia
colorScheme = "noir"           # Esquema de colores
defaultAppearance = "dark"     # dark o light
autoSwitchAppearance = true    # Cambio automatico dia/noche

# Funcionalidades
enableSearch = true            # Buscador
enableCodeCopy = true          # Boton copiar codigo

# Homepage
[homepage]
layout = "page"
showRecent = true
showRecentItems = 25
cardView = true

# Articulos
[article]
showDate = true
showAuthor = true
showTableOfContents = true
showTaxonomies = true
showWordCount = true
```

---

## Tips utiles

### Imagenes locales
Pon imagenes en `static/images/` y referencialas como:
```markdown
![Descripcion](/images/mi-imagen.jpg)
```

### Shortcodes utiles de Blowfish
```markdown
<!-- Alerta -->
{{< alert >}}
Texto de alerta
{{< /alert >}}

<!-- Badge -->
{{< badge >}}
Nuevo
{{< /badge >}}

<!-- Codigo con titulo -->
{{< highlight python "linenos=table,hl_lines=2" >}}
def hello():
    print("Hello")  # Esta linea resaltada
{{< /highlight >}}
```

### Ver todos los posts (incluyendo drafts)
```bash
hugo list all
```

### Limpiar cache
```bash
hugo --gc
```

---

## Trabajando con Drafts

En Hugo, los drafts son posts con `draft: true` en el front matter.

### Ver drafts en desarrollo
```bash
hugo server -D
```
La flag `-D` incluye los drafts.

### Listar todos los drafts
```bash
hugo list drafts
```

### Publicar un draft
Cambia `draft: true` a `draft: false` en el front matter del post.

### Crear nuevo draft
```bash
hugo new posts/mi-borrador.md
```
Por defecto se crea con `draft: true`.

---

## Troubleshooting

### El post no aparece
1. Verifica que `draft: false`
2. Verifica que la fecha no es futura
3. Reinicia el servidor

### Error de YAML
- No uses comillas dobles dentro de valores entre comillas dobles
- Usa comillas simples para valores con caracteres especiales

### Cambios no se reflejan
```bash
# Detener servidor y limpiar cache
hugo --gc
hugo server -D
```

---

## Referencias

- [Documentacion de Hugo](https://gohugo.io/documentation/)
- [Theme Blowfish](https://blowfish.page/)
- [Shortcodes de Blowfish](https://blowfish.page/docs/shortcodes/)
