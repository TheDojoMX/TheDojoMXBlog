# Content Detection Improvements

## Problem
"Could not identify main content area" error when extracting from certain URLs.

## Solution

### 1. Enhanced Content Detection (`_find_main_content_area`)

**Multi-pass approach with decreasing thresholds:**
- First pass: Look for content with >300 characters
- Second pass: Lower threshold to >100 characters
- Fallback 1: Find element with most paragraphs
- Fallback 2: Find any div with >500 characters

**Expanded selector list:**
```python
# Added many more selectors including:
'.content',
'div.content', 
'div.post',
'div.entry',
'.page-content',
'.site-content',
'#primary',
'.hentry',
# And Medium/Substack specific ones
```

### 2. Graceful Fallback to Full Body

If no specific content area is found:
- Uses the entire `<body>` element
- Applies more aggressive cleaning when using full body
- Removes navigation, headers, footers carefully

### 3. New Direct HTML2Text Method

Added `_extract_with_html2text_direct` as final fallback:
- Converts entire HTML to markdown using html2text
- Bypasses complex content detection
- Works with unusual HTML structures

### 4. Improved Error Handling

- Better error messages with specific failure reasons
- Debug output shows which selector/method succeeded
- Stack traces for debugging extraction failures

### 5. Better Cleaning for Full Body

When using full body as fallback:
- Removes nav, header, footer elements
- Preserves headers with substantial content (>200 chars)
- Removes cookie notices, GDPR notices
- Removes social sharing widgets

## Extraction Flow

1. **Advanced Markdown Extraction**
   - Tries to find specific content area
   - Falls back to full body if needed
   - Converts to clean markdown

2. **Newspaper3k with Markdown**
   - Uses newspaper library
   - Enhances with HTML structure
   - Converts to markdown

3. **Basic Structure Extraction**
   - Manual heading/paragraph extraction
   - Works with simple HTML

4. **Direct HTML2Text** (NEW)
   - Converts entire HTML to markdown
   - Most permissive method
   - Final fallback

## Testing

Use `test_robust_extraction.py` to:
- Test each extraction method individually
- Analyze URL structure
- Debug content detection issues
- Verify CLI extraction

```bash
# Test any problematic URL
python test_robust_extraction.py "http://example.com/article"

# Test with CLI flag
python test_robust_extraction.py "http://example.com/article" --cli
```

## Examples of Fixed Issues

1. **Substack Redirects**
   - `http://substack.com/inbox/post/167238739`
   - Now handles redirect and extracts content

2. **Sites with Unusual Structure**
   - No `<article>` tag
   - Content in nested divs
   - Now uses multiple fallbacks

3. **Sites with Minimal Markup**
   - Just `<div>` containers
   - Now detected by paragraph count or text length

## Benefits

1. **More Robust**: Multiple fallback methods ensure extraction succeeds
2. **Better Debugging**: Clear messages about which method worked
3. **Flexible Detection**: Works with various HTML structures
4. **Graceful Degradation**: Falls back to simpler methods if needed
5. **Full Content**: Even difficult sites get extracted completely