#!/usr/bin/env python3
"""
Script para migrar posts de Jekyll a Hugo (formato Blowfish)
"""
import os
import re
from pathlib import Path

# Directorios
jekyll_posts = Path("_posts")
hugo_posts = Path("content/posts")

# Crear directorio si no existe
hugo_posts.mkdir(parents=True, exist_ok=True)


def clean_title(title: str) -> str:
    """Limpia el titulo para evitar problemas con TOML/YAML"""
    # Remover comillas existentes
    title = title.strip().strip('"').strip("'")
    # Remover comillas dobles internas en lugar de escaparlas
    title = title.replace('"', "'")
    return title


def parse_tags(tags_str: str) -> list:
    """Parsea tags de Jekyll (separados por espacio) a lista"""
    tags_str = tags_str.strip()
    # Si ya es formato array YAML [tag1, tag2], extraer contenido
    if tags_str.startswith('[') and tags_str.endswith(']'):
        inner = tags_str[1:-1]
        tags = [t.strip() for t in inner.split(',') if t.strip()]
        return tags
    # Separar por espacios o comas
    tags = [t.strip() for t in re.split(r'[\s,]+', tags_str) if t.strip()]
    return tags


def convert_post(jekyll_file: Path) -> bool:
    """Convierte un post de Jekyll a Hugo"""
    try:
        with open(jekyll_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error leyendo {jekyll_file.name}: {e}")
        return False

    # Extraer front matter
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not match:
        print(f"No se pudo parsear: {jekyll_file.name}")
        return False

    front_matter = match.group(1)
    body = match.group(2)

    # Parsear datos del front matter
    title_match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', front_matter, re.MULTILINE)
    date_match = re.search(r'^date:\s*(.+?)\s*$', front_matter, re.MULTILINE)
    author_match = re.search(r'^author:\s*(.+?)\s*$', front_matter, re.MULTILINE)
    tags_match = re.search(r'^tags:\s*(.+?)\s*$', front_matter, re.MULTILINE)
    excerpt_match = re.search(r'^excerpt:\s*["\']?(.*?)["\']?\s*$', front_matter, re.MULTILINE)
    categories_match = re.search(r'^categories:\s*(.+?)\s*$', front_matter, re.MULTILINE)

    # Extraer imagen del header si existe
    overlay_image = re.search(r'overlay_image:\s*(.+?)\s*$', front_matter, re.MULTILINE)

    # Construir nuevo front matter para Hugo
    new_front_matter = "---\n"

    # Titulo
    if title_match:
        title = clean_title(title_match.group(1))
        new_front_matter += f'title: "{title}"\n'
    else:
        # Usar nombre del archivo como titulo
        filename_title = jekyll_file.stem
        filename_title = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename_title)
        filename_title = filename_title.replace('-', ' ').title()
        new_front_matter += f'title: "{filename_title}"\n'

    # Fecha - extraer del nombre del archivo o del front matter
    date_str = None
    filename_date = re.match(r'^(\d{4}-\d{2}-\d{2})', jekyll_file.name)
    if filename_date:
        date_str = filename_date.group(1)
    elif date_match:
        date_val = date_match.group(1).strip()
        date_parsed = re.match(r'(\d{4}-\d{2}-\d{2})', date_val)
        if date_parsed:
            date_str = date_parsed.group(1)

    if date_str:
        new_front_matter += f'date: {date_str}\n'

    # Autor
    if author_match:
        author = author_match.group(1).strip()
        new_front_matter += f'author: "{author}"\n'

    # Tags
    if tags_match:
        tags = parse_tags(tags_match.group(1))
        if tags:
            new_front_matter += f'tags: {tags}\n'

    # Categories
    if categories_match:
        categories = parse_tags(categories_match.group(1))
        if categories:
            new_front_matter += f'categories: {categories}\n'

    # Description (excerpt)
    if excerpt_match:
        excerpt = clean_title(excerpt_match.group(1))
        new_front_matter += f'description: "{excerpt}"\n'

    # Imagen destacada
    if overlay_image:
        img_url = overlay_image.group(1).strip()
        new_front_matter += f'featuredImage: "{img_url}"\n'

    new_front_matter += "draft: false\n"
    new_front_matter += "---\n\n"

    # Contenido final
    new_content = new_front_matter + body

    # Nombre del archivo (sin la fecha al inicio)
    filename = jekyll_file.name
    filename = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename)

    # Guardar
    output_file = hugo_posts / filename
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    except Exception as e:
        print(f"Error escribiendo {output_file}: {e}")
        return False


def main():
    print("Iniciando migracion de posts Jekyll a Hugo...\n")

    if not jekyll_posts.exists():
        print(f"Error: No se encontro el directorio {jekyll_posts}")
        return

    posts = sorted(jekyll_posts.glob("*.md"))
    migrated = 0
    failed = 0

    for post in posts:
        if convert_post(post):
            migrated += 1
            print(f"OK {post.name}")
        else:
            failed += 1
            print(f"FAIL {post.name}")

    print(f"\nResumen:")
    print(f"   Migrados: {migrated}")
    print(f"   Fallidos: {failed}")
    print(f"   Total: {len(posts)}")


if __name__ == "__main__":
    main()
