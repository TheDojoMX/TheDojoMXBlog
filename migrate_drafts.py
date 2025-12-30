#!/usr/bin/env python3
"""
Script para migrar drafts de Jekyll a Hugo
"""
import re
from pathlib import Path

jekyll_drafts = Path("_drafts")
hugo_posts = Path("content/posts")

hugo_posts.mkdir(parents=True, exist_ok=True)


def clean_title(title: str) -> str:
    title = title.strip().strip('"').strip("'")
    title = title.replace('"', "'")
    return title


def parse_tags(tags_str: str) -> list:
    tags_str = tags_str.strip()
    if tags_str.startswith('[') and tags_str.endswith(']'):
        inner = tags_str[1:-1]
        tags = [t.strip() for t in inner.split(',') if t.strip()]
        return tags
    tags = [t.strip() for t in re.split(r'[\s,]+', tags_str) if t.strip()]
    return tags


def convert_draft(jekyll_file: Path) -> bool:
    try:
        with open(jekyll_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error leyendo {jekyll_file.name}: {e}")
        return False

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not match:
        # Si no tiene front matter, crear uno basico
        title = jekyll_file.stem.replace('-', ' ').title()
        new_content = f'---\ntitle: "{title}"\ndraft: true\n---\n\n{content}'
        output_file = hugo_posts / jekyll_file.name
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True

    front_matter = match.group(1)
    body = match.group(2)

    title_match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', front_matter, re.MULTILINE)
    date_match = re.search(r'^date:\s*(.+?)\s*$', front_matter, re.MULTILINE)
    author_match = re.search(r'^author:\s*(.+?)\s*$', front_matter, re.MULTILINE)
    tags_match = re.search(r'^tags:\s*(.+?)\s*$', front_matter, re.MULTILINE)
    excerpt_match = re.search(r'^excerpt:\s*["\']?(.*?)["\']?\s*$', front_matter, re.MULTILINE)
    overlay_image = re.search(r'overlay_image:\s*(.+?)\s*$', front_matter, re.MULTILINE)

    new_front_matter = "---\n"

    if title_match:
        title = clean_title(title_match.group(1))
        new_front_matter += f'title: "{title}"\n'
    else:
        filename_title = jekyll_file.stem.replace('-', ' ').title()
        new_front_matter += f'title: "{filename_title}"\n'

    if date_match:
        date_val = date_match.group(1).strip()
        date_parsed = re.match(r'(\d{4}-\d{2}-\d{2})', date_val)
        if date_parsed:
            new_front_matter += f'date: {date_parsed.group(1)}\n'

    if author_match:
        author = author_match.group(1).strip()
        new_front_matter += f'author: "{author}"\n'

    if tags_match:
        tags = parse_tags(tags_match.group(1))
        if tags:
            new_front_matter += f'tags: {tags}\n'

    if excerpt_match:
        excerpt = clean_title(excerpt_match.group(1))
        new_front_matter += f'description: "{excerpt}"\n'

    if overlay_image:
        img_url = overlay_image.group(1).strip()
        new_front_matter += f'featuredImage: "{img_url}"\n'

    # Marcar como draft
    new_front_matter += "draft: true\n"
    new_front_matter += "---\n\n"

    new_content = new_front_matter + body
    output_file = hugo_posts / jekyll_file.name

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    except Exception as e:
        print(f"Error escribiendo {output_file}: {e}")
        return False


def main():
    print("Migrando drafts de Jekyll a Hugo...\n")

    if not jekyll_drafts.exists():
        print(f"No se encontro {jekyll_drafts}")
        return

    drafts = sorted(jekyll_drafts.glob("*.md"))
    migrated = 0
    failed = 0

    for draft in drafts:
        if convert_draft(draft):
            migrated += 1
            print(f"OK {draft.name}")
        else:
            failed += 1
            print(f"FAIL {draft.name}")

    print(f"\nResumen:")
    print(f"   Migrados: {migrated}")
    print(f"   Fallidos: {failed}")


if __name__ == "__main__":
    main()
