# URL Extraction Improvements

## Overview

Improved URL content extraction to preserve all relevant content, including headings, markdown formatting, and document structure. This ensures that articles maintain their original formatting and no content is lost during extraction.

## Key Improvements

### 1. New Improved Web Reader (`web_reader_improved.py`)

Created a new `ImprovedWebArticleExtractor` class with:

- **Markdown Preservation**: Converts HTML to proper markdown format
- **Complete Heading Extraction**: Captures all H1-H6 headings with proper hierarchy
- **Structure Preservation**: Maintains lists, code blocks, blockquotes, tables, and links
- **Better Title Detection**: Uses multiple sources (JSON-LD, Open Graph, Twitter meta, H1 tags)
- **Content Area Detection**: Smart detection of main content area using multiple selectors
- **Format Preservation**: Keeps code blocks with language hints, inline code, and special formatting

### 2. HTML to Markdown Conversion

Uses `html2text` library with optimized settings:
- Preserves links and images
- Maintains code block formatting
- Keeps list structure (ordered and unordered)
- Preserves blockquotes and tables
- No line wrapping for better readability

### 3. Updated CLI Handling

Modified the CLI to:
- Skip `clean_paper_text()` for web content (preserves markdown)
- Save extracted content as both `.md` and `.txt` files
- Store markdown version for better preservation
- Maintain backward compatibility with text files

## Example: hamel.dev Article

Testing with `https://hamel.dev/blog/posts/llm-judge/` now captures:

- **Title**: "Creating a LLM-as-a-Judge That Drives Business Results"
- **All Section Headings**: All 7 main steps plus subsections
- **Code Blocks**: JSON examples, Python code snippets
- **Images**: Screenshots and diagrams
- **Lists**: Step-by-step instructions
- **Links**: References to external resources

## Technical Details

### Extraction Methods (in order of preference)

1. **Advanced Markdown Extraction**: 
   - Finds main content area
   - Converts HTML to markdown preserving structure
   - Handles complex formatting

2. **Newspaper3k with Markdown Conversion**:
   - Uses newspaper3k for text extraction
   - Enhances with HTML structure analysis
   - Converts to markdown format

3. **Basic Structure Extraction**:
   - Fallback method
   - Extracts headings, paragraphs, lists manually
   - Creates basic markdown structure

### Content Detection Selectors

```python
content_selectors = [
    "article",
    '[role="main"]',
    '.article-content',
    '.post-content',
    '.entry-content',
    '.prose',  # Common in modern frameworks
    '.markdown-body',  # GitHub style
    # ... and many more
]
```

### Markdown Elements Preserved

- Headings (H1-H6) → `#` to `######`
- Paragraphs → Plain text with spacing
- Code blocks → ` ```language ... ``` `
- Inline code → `` `code` ``
- Links → `[text](url)`
- Images → `![alt](src)`
- Lists → `- item` or `1. item`
- Blockquotes → `> quote`
- Tables → Markdown table format
- Horizontal rules → `---`
- Bold/Italic → `**bold**` / `*italic*`

## Usage

### Command Line

```bash
# Extract and save markdown from URL
voice-papers https://example.com/article --extract-only

# Process URL with full pipeline (uses improved extraction)
voice-papers https://example.com/article --script-only
```

### Python API

```python
from voice_papers.utils.web_reader_improved import extract_text_from_url_improved

title, markdown_content = extract_text_from_url_improved(url)
```

## Benefits

1. **Complete Content**: No missing headings or sections
2. **Better Structure**: Maintains document hierarchy
3. **Code Preservation**: Code blocks remain formatted
4. **Link Preservation**: All links are maintained
5. **Readability**: Markdown format is human-readable
6. **Synthesis Quality**: Better input leads to better AI processing

## Testing

Use `test_url_extraction_improved.py` to verify:
- Heading extraction
- Markdown element counts
- Document structure
- Content completeness

## Future Enhancements

1. Support for more complex HTML structures
2. Better handling of interactive elements
3. Extraction of metadata (author, date, tags)
4. Support for multi-page articles
5. Custom extraction rules per domain