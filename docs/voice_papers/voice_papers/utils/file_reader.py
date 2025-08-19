"""File reading utilities for markdown and text files."""

from pathlib import Path
from typing import Union, Tuple, Optional
import re


def extract_title_from_markdown(content: str, debug: bool = False) -> Optional[str]:
    """Extract title from markdown content."""
    if debug:
        print("🔍 Debug: Extracting title from markdown content")
    
    lines = content.split('\n')
    
    # Strategy 1: Look for H1 header with # syntax
    for line in lines[:20]:  # Check first 20 lines
        line = line.strip()
        if line.startswith('# ') and not line.startswith('##'):
            title = line[2:].strip()
            if title and len(title) > 3:
                if debug:
                    print(f"✅ Debug: Found H1 title: '{title}'")
                return title
    
    # Strategy 2: Look for title in frontmatter
    if content.startswith('---'):
        try:
            frontmatter_end = content.index('---', 3)
            frontmatter = content[3:frontmatter_end]
            for line in frontmatter.split('\n'):
                if line.strip().startswith('title:'):
                    title = line.split(':', 1)[1].strip().strip('"').strip("'")
                    if title:
                        if debug:
                            print(f"✅ Debug: Found frontmatter title: '{title}'")
                        return title
        except ValueError:
            pass
    
    # Strategy 3: Look for first non-empty line that looks like a title
    for line in lines[:10]:
        line = line.strip()
        if line and len(line) > 10 and len(line) < 200:
            # Skip lines that are likely not titles
            if any(skip in line.lower() for skip in ['http', 'www.', '@', 'copyright', '©']):
                continue
            if re.match(r'^[-*_]{3,}$', line):  # Skip horizontal rules
                continue
            if line.startswith(('- ', '* ', '+ ', '1. ')):  # Skip list items
                continue
            
            if debug:
                print(f"✅ Debug: Using first substantial line as title: '{line}'")
            return line
    
    if debug:
        print("❌ Debug: No title found in markdown")
    return None


def extract_title_from_text(content: str, debug: bool = False) -> Optional[str]:
    """Extract title from plain text content."""
    if debug:
        print("🔍 Debug: Extracting title from text content")
    
    lines = content.split('\n')
    
    # Strategy 1: Look for "Title:" prefix
    for line in lines[:20]:
        line = line.strip()
        if line.lower().startswith('title:'):
            title = line.split(':', 1)[1].strip()
            if title and len(title) > 3:
                if debug:
                    print(f"✅ Debug: Found explicit title: '{title}'")
                return title
    
    # Strategy 2: Look for title patterns (all caps, surrounded by empty lines, etc.)
    prev_empty = True
    for i, line in enumerate(lines[:30]):
        current_line = line.strip()
        next_empty = i + 1 >= len(lines) or not lines[i + 1].strip()
        
        if current_line and prev_empty and next_empty:
            # Line surrounded by empty lines
            if len(current_line) > 10 and len(current_line) < 200:
                # Check if it looks like a title
                word_count = len(current_line.split())
                if 3 <= word_count <= 20:
                    # Skip obvious non-titles
                    if not any(skip in current_line.lower() for skip in [
                        'abstract', 'introduction', 'conclusion', 'references',
                        'http', 'www.', '@', 'page', 'chapter', 'section'
                    ]):
                        if debug:
                            print(f"✅ Debug: Found isolated line as title: '{current_line}'")
                        return current_line
        
        prev_empty = not current_line
    
    # Strategy 3: First substantial line
    for line in lines[:15]:
        line = line.strip()
        if line and len(line) > 15 and len(line) < 200:
            # Skip lines that are likely not titles
            if any(skip in line.lower() for skip in ['http', 'www.', '@', 'copyright', '©']):
                continue
            if re.match(r'^\d+\.?\s', line):  # Skip numbered items
                continue
            
            word_count = len(line.split())
            if 3 <= word_count <= 20:
                if debug:
                    print(f"✅ Debug: Using first substantial line as title: '{line}'")
                return line
    
    if debug:
        print("❌ Debug: No title found in text")
    return None


def read_markdown_file(file_path: Union[str, Path]) -> Tuple[Optional[str], str]:
    """Read a markdown file and extract title and content."""
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title
    title = extract_title_from_markdown(content)
    
    # If no title found, try generic text extraction
    if not title:
        title = extract_title_from_text(content)
    
    # If still no title, use filename
    if not title:
        title = file_path.stem.replace('_', ' ').replace('-', ' ').title()
    
    return title, content


def read_text_file(file_path: Union[str, Path]) -> Tuple[Optional[str], str]:
    """Read a text file and extract title and content."""
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Text file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title
    title = extract_title_from_text(content)
    
    # If no title found, use filename
    if not title:
        title = file_path.stem.replace('_', ' ').replace('-', ' ').title()
    
    return title, content


def read_document_file(file_path: Union[str, Path], debug: bool = False) -> Tuple[Optional[str], str]:
    """
    Read a document file (markdown or text) and extract title and content.
    
    Args:
        file_path: Path to the document file
        debug: Enable debug output for title extraction
        
    Returns:
        Tuple of (title, content)
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Determine file type and read accordingly
    if file_path.suffix.lower() in ['.md', '.markdown']:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        title = extract_title_from_markdown(content, debug=debug)
    elif file_path.suffix.lower() in ['.txt', '.text']:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        title = extract_title_from_text(content, debug=debug)
    else:
        raise ValueError(f"Unsupported file type: {file_path.suffix}")
    
    # Fallback to filename if no title found
    if not title:
        title = file_path.stem.replace('_', ' ').replace('-', ' ').title()
        if debug:
            print(f"💡 Debug: Using filename as title: '{title}'")
    
    return title, content