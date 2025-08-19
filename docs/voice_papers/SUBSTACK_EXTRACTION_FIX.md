# Substack URL Extraction Fix

## Problem
The URL `http://substack.com/inbox/post/167238739` failed to extract because:
1. It's a redirect URL that goes to the actual article
2. HTTP needs to be upgraded to HTTPS for proper handling
3. Substack has specific content structure that needs special selectors

## Solution

### 1. Redirect Handling
- Added redirect detection and logging in both extractors
- Uses the final URL after redirects for better content detection
- Example: `http://substack.com/inbox/post/167238739` → `https://simonw.substack.com/p/gemma-3n-context-engineering-and`

### 2. HTTPS Upgrade
- Automatically upgrades HTTP URLs to HTTPS
- Many modern sites require HTTPS and reject HTTP requests
- Prevents SSL-related extraction failures

### 3. Substack-Specific Selectors
Added content selectors specific to Substack's HTML structure:
```python
'.available-content',
'.body.markup',
'div.post-content',
'div.body.markup',
'.post .available-content',
```

### 4. Improved Error Handling
- Better error messages with stack traces for debugging
- Fallback methods if primary extraction fails
- Preserves Substack's article structure (subtitles, author info)

## How It Works

1. **URL Processing**:
   - Strips whitespace
   - Upgrades HTTP to HTTPS
   - Validates URL format

2. **Extraction Flow**:
   - Follows redirects automatically
   - Tries multiple extraction methods
   - Uses Substack-specific selectors
   - Preserves markdown formatting

3. **Content Preservation**:
   - Maintains heading hierarchy
   - Preserves links and formatting
   - Keeps code blocks and lists
   - Extracts subtitles if present

## Testing

Use `test_substack_extraction.py` to verify:
```bash
# Test both redirect and direct URLs
python test_substack_extraction.py

# Test CLI extraction
python test_substack_extraction.py --cli
```

## Examples

### Redirect URL
```
Input: http://substack.com/inbox/post/167238739
Redirects to: https://simonw.substack.com/p/gemma-3n-context-engineering-and
Extracts: "Gemma 3n, Context Engineering and a whole lot of Claude Code"
```

### Direct Substack URL
```
Input: https://example.substack.com/p/article-title
Extracts: Full article with markdown formatting
```

## Benefits

1. **Works with inbox links**: Handles Substack's redirect URLs
2. **Preserves formatting**: Maintains the newsletter's structure
3. **Complete extraction**: Gets all content including embedded elements
4. **Automatic HTTPS**: Prevents protocol-related failures
5. **Better debugging**: Clear error messages for troubleshooting