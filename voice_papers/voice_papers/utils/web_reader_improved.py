"""Improved web article reading utilities with markdown preservation."""

import re
import requests
from typing import Union, Tuple, Optional, List
from urllib.parse import urlparse
from pathlib import Path
import hashlib
import random
import time
from bs4 import BeautifulSoup, NavigableString, Tag
import html2text
from newspaper import Article


class ImprovedWebArticleExtractor:
    """Extracts article content from web URLs with markdown preservation and complete content capture."""

    def __init__(self):
        self.session = requests.Session()
        self._setup_session()
        # Configure html2text for markdown conversion
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.h2t.ignore_images = False
        self.h2t.body_width = 0  # Don't wrap lines
        self.h2t.protect_links = True
        self.h2t.unicode_snob = True  # Use unicode for special characters
        self.h2t.skip_internal_links = False
        self.h2t.inline_links = True
        self.h2t.wrap_links = False
        self.h2t.mark_code = True

    def _setup_session(self):
        """Configure session with realistic headers to avoid blocking."""
        # Modern User-Agents (updated December 2024)
        user_agents = [
            # Chrome on Windows
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            # Chrome on macOS
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            # Firefox on Windows
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
            # Safari on macOS
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
            # Chrome on Linux
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        ]

        # Select a random User-Agent
        selected_ua = random.choice(user_agents)

        # Comprehensive headers to appear more human
        headers = {
            "User-Agent": selected_ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",  # Do Not Track
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }

        self.session.headers.update(headers)
        self.session.timeout = 30

        # Add random delay to avoid detection
        time.sleep(random.uniform(0.5, 2.0))

    def extract_article_from_url(self, url: str) -> Tuple[str, str]:
        """
        Extract article content and title from a URL with markdown formatting.

        Args:
            url: The URL to extract content from

        Returns:
            Tuple of (title, markdown_content)

        Raises:
            Exception: If content extraction fails
        """
        # Handle common URL issues
        url = url.strip()
        if url.startswith("http://") and not url.startswith("https://"):
            # Some sites require HTTPS
            https_url = url.replace("http://", "https://", 1)
            print(f"🔒 Upgrading to HTTPS: {https_url}")
            url = https_url
            
        if not self._is_valid_url(url):
            raise ValueError(f"Invalid URL: {url}")

        print(f"🌐 Extracting content from: {url}")

        # Try advanced markdown extraction first
        try:
            return self._extract_with_markdown_preservation(url)
        except Exception as e:
            print(f"Advanced extraction failed: {e}")
            import traceback
            traceback.print_exc()

        # Fallback to newspaper3k with markdown conversion
        try:
            return self._extract_with_newspaper_markdown(url)
        except Exception as e:
            print(f"Newspaper3k failed: {e}")

        # Fallback to basic extraction
        try:
            return self._extract_basic_with_structure(url)
        except Exception as e:
            print(f"Basic extraction failed: {e}")
            
        # Final fallback - use html2text directly
        try:
            return self._extract_with_html2text_direct(url)
        except Exception as e:
            raise Exception(f"All extraction methods failed. Last error: {e}")

    def _extract_with_markdown_preservation(self, url: str) -> Tuple[str, str]:
        """Extract content while preserving markdown structure and all headings."""
        print("📝 Using advanced markdown extraction...")
        
        # Add delay
        time.sleep(random.uniform(1.0, 3.0))
        
        # Get the page with redirect handling
        response = self.session.get(url, timeout=30, allow_redirects=True)
        response.raise_for_status()
        
        # Handle redirects - use final URL for better extraction
        if response.history:
            print(f"🔄 Redirected to: {response.url}")
            url = response.url
        
        soup = BeautifulSoup(response.content, "lxml")
        
        # Extract title
        title = self._extract_best_title(soup, url)
        
        # Find main content area
        main_content = self._find_main_content_area(soup)
        
        if not main_content:
            # Try a more aggressive fallback - use the whole body
            print("⚠️  Could not identify specific content area, using full body")
            main_content = soup.body
            if not main_content:
                raise Exception("Could not find any content in the page")
        
        # Clean the content area
        self._clean_content_area(main_content)
        
        # Convert to markdown preserving structure
        markdown_content = self._convert_to_markdown_preserving_structure(main_content, title)
        
        if len(markdown_content.strip()) < 500:
            raise Exception("Insufficient content extracted")
        
        return title, markdown_content

    def _extract_with_newspaper_markdown(self, url: str) -> Tuple[str, str]:
        """Extract using newspaper3k and convert to markdown."""
        print("📰 Using newspaper3k with markdown conversion...")
        
        config = {
            "headers": self.session.headers,
            "timeout": 30,
            "follow_meta_refresh": True,
            "memoize_articles": False,
        }

        article = Article(url, **config)
        
        # Add delay
        time.sleep(random.uniform(1.0, 3.0))
        
        article.download()
        article.parse()
        
        if not article.text.strip():
            raise Exception("No content extracted with newspaper3k")
        
        title = article.title or self._extract_title_from_url(url)
        
        # Get the HTML for better structure preservation
        response = self.session.get(url, timeout=30)
        soup = BeautifulSoup(response.content, "lxml")
        
        # Try to find the article content in HTML
        main_content = self._find_article_content_newspaper_fallback(soup, article.text)
        
        if main_content:
            # Convert the structured HTML to markdown
            markdown_content = self._convert_to_markdown_preserving_structure(main_content, title)
        else:
            # Fallback: Convert plain text to basic markdown
            markdown_content = f"# {title}\n\n{article.text}"
        
        return title, markdown_content

    def _extract_basic_with_structure(self, url: str) -> Tuple[str, str]:
        """Basic extraction with structure preservation."""
        print("🔄 Using basic extraction with structure...")
        
        time.sleep(random.uniform(2.0, 4.0))
        
        response = self.session.get(url, timeout=30, allow_redirects=True)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "lxml")
        
        # Extract title
        title = self._extract_best_title(soup, url)
        
        # Remove unwanted elements
        for element in soup(["script", "style", "nav", "footer", "aside", "form", "iframe"]):
            element.decompose()
            
        # For Substack, be careful with header removal as it might contain the title
        if 'substack.com' not in url:
            for element in soup(["header"]):
                element.decompose()
        
        # Find all content with structure
        content_parts = []
        content_parts.append(f"# {title}\n")
        
        # Extract main content with headings
        main_selectors = [
            "article", '[role="main"]', ".article-content", ".post-content",
            ".entry-content", ".story-content", "main", "#content", ".content"
        ]
        
        main_content = None
        for selector in main_selectors:
            elements = soup.select(selector)
            if elements:
                main_content = elements[0]
                break
        
        if not main_content:
            main_content = soup.body
        
        # Extract structured content
        for element in main_content.descendants:
            if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                level = int(element.name[1])
                heading_text = element.get_text().strip()
                if heading_text:
                    content_parts.append(f"\n{'#' * level} {heading_text}\n")
            elif element.name == 'p':
                text = element.get_text().strip()
                if len(text) > 20:
                    content_parts.append(f"{text}\n")
            elif element.name == 'pre' or (element.name == 'code' and element.parent.name != 'pre'):
                code_text = element.get_text().strip()
                if code_text:
                    if element.name == 'pre':
                        content_parts.append(f"```\n{code_text}\n```\n")
                    else:
                        content_parts.append(f"`{code_text}`")
            elif element.name in ['ul', 'ol']:
                list_items = element.find_all('li', recursive=False)
                if list_items:
                    content_parts.append("")
                    for li in list_items:
                        marker = "- " if element.name == 'ul' else f"{list_items.index(li) + 1}. "
                        content_parts.append(f"{marker}{li.get_text().strip()}")
                    content_parts.append("")
            elif element.name == 'blockquote':
                quote_text = element.get_text().strip()
                if quote_text:
                    content_parts.append(f"> {quote_text}\n")
        
        markdown_content = "\n".join(content_parts)
        markdown_content = self._clean_markdown_content(markdown_content)
        
        return title, markdown_content

    def _find_main_content_area(self, soup: BeautifulSoup) -> Optional[Tag]:
        """Find the main content area of the page."""
        # Try various selectors for main content
        content_selectors = [
            # Substack specific
            '.available-content',
            '.body.markup',
            'div.post-content',
            'div.body.markup',
            '.post .available-content',
            # Medium specific
            '.section-content',
            '.postArticle-content',
            # General selectors
            "article",
            '[role="main"]',
            '.article-content',
            '.post-content',
            '.entry-content',
            '.prose',  # Common in modern frameworks
            '.markdown-body',  # GitHub style
            '.content-body',
            '.story-body',
            '.article-body',
            '.post-body',
            '.blog-post',
            '.blog-content',
            'main article',
            'main .content',
            '#main-content',
            '#content',
            '.content',
            '.main-content',
            '.primary-content',
            '.container article',
            '.container .content',
            'div.content',
            'div.post',
            'div.entry',
            'div.page-content',
            '.page-content',
            '.site-content',
            '#primary',
            '.hentry',
        ]
        
        # First pass: Try selectors with content check
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                # Check if element has substantial content
                element = elements[0]
                text_length = len(element.get_text().strip())
                # Lower threshold for first pass
                if text_length > 300:
                    print(f"✅ Found content area with selector: {selector} ({text_length} chars)")
                    return element
        
        # Second pass: Try selectors with even lower threshold
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                element = elements[0]
                text_length = len(element.get_text().strip())
                if text_length > 100:
                    print(f"✅ Found content area with selector: {selector} ({text_length} chars)")
                    return element
        
        # Fallback 1: Look for the element with the most paragraph tags
        potential_containers = soup.find_all(['div', 'section', 'main', 'article', 'body'])
        best_container = None
        max_paragraphs = 0
        
        for container in potential_containers:
            paragraphs = container.find_all('p')
            if len(paragraphs) > max_paragraphs:
                max_paragraphs = len(paragraphs)
                best_container = container
        
        if best_container and max_paragraphs > 2:
            print(f"✅ Found content area by paragraph count: {max_paragraphs} paragraphs")
            return best_container
        
        # Fallback 2: Look for any div with substantial text
        all_divs = soup.find_all('div')
        for div in all_divs:
            # Skip if it has too many nested divs (likely a container)
            nested_divs = div.find_all('div')
            if len(nested_divs) > 20:
                continue
                
            text_length = len(div.get_text().strip())
            if text_length > 500:
                print(f"✅ Found content area by text length in div: {text_length} chars")
                return div
        
        return None

    def _clean_content_area(self, content: Tag) -> None:
        """Clean the content area by removing unwanted elements."""
        # Remove script, style, and other non-content elements
        for tag in content(['script', 'style', 'noscript', 'iframe']):
            tag.decompose()
        
        # Remove navigation and header/footer elements when using full body
        if content.name == 'body':
            for tag in content(['nav', 'header', 'footer']):
                # Be careful with header - it might contain the title
                if tag.name == 'header':
                    # Check if it has substantial content
                    header_text = tag.get_text().strip()
                    if len(header_text) < 200:  # Likely just navigation
                        tag.decompose()
                else:
                    tag.decompose()
        
        # Remove common UI elements
        for selector in [
            '.social-share', '.share-buttons', '.newsletter-signup',
            '.related-posts', '.advertisement', '.ads', '.sidebar',
            '.comments', '.comment-form', '[class*="subscribe"]',
            '[class*="newsletter"]', '[class*="popup"]', '[class*="modal"]',
            '.cookie-notice', '.gdpr-notice', '[class*="cookie"]',
            '.footer', '.site-footer', '#footer',
            '.navigation', '.site-navigation', 
            '[class*="share"]', '[class*="social"]',
            '.author-bio', '.author-box',  # Keep author info in article context
        ]:
            for element in content.select(selector):
                element.decompose()

    def _convert_to_markdown_preserving_structure(self, content: Tag, title: str) -> str:
        """Convert HTML content to markdown while preserving all structure."""
        # Start with the title
        markdown_parts = [f"# {title}\n"]
        
        # For Substack, check if there's a subtitle
        subtitle = content.find('h3', class_='subtitle')
        if subtitle:
            markdown_parts.append(f"\n*{subtitle.get_text().strip()}*\n")
            subtitle.decompose()  # Remove it so it's not processed again
        
        # Process content recursively
        def process_element(element, depth=0):
            if isinstance(element, NavigableString):
                text = str(element).strip()
                if text:
                    return text
                return ""
            
            if not isinstance(element, Tag):
                return ""
            
            # Handle different tags
            if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                level = int(element.name[1])
                text = element.get_text().strip()
                if text and text != title:  # Avoid duplicating the title
                    return f"\n{'#' * level} {text}\n"
            
            elif element.name == 'p':
                text = element.get_text().strip()
                if text:
                    return f"{text}\n"
            
            elif element.name == 'pre':
                code = element.get_text()
                # Try to detect language from class
                lang = ""
                if element.get('class'):
                    classes = ' '.join(element.get('class'))
                    lang_match = re.search(r'language-(\w+)', classes)
                    if lang_match:
                        lang = lang_match.group(1)
                return f"```{lang}\n{code}\n```\n"
            
            elif element.name == 'code':
                if element.parent and element.parent.name == 'pre':
                    return ""  # Already handled by pre
                return f"`{element.get_text()}`"
            
            elif element.name == 'blockquote':
                lines = element.get_text().strip().split('\n')
                return '\n'.join(f"> {line}" for line in lines if line) + '\n'
            
            elif element.name == 'ul':
                items = []
                for li in element.find_all('li', recursive=False):
                    items.append(f"- {li.get_text().strip()}")
                return '\n'.join(items) + '\n' if items else ""
            
            elif element.name == 'ol':
                items = []
                for i, li in enumerate(element.find_all('li', recursive=False), 1):
                    items.append(f"{i}. {li.get_text().strip()}")
                return '\n'.join(items) + '\n' if items else ""
            
            elif element.name == 'a':
                text = element.get_text().strip()
                href = element.get('href', '')
                if text and href and not href.startswith('#'):
                    return f"[{text}]({href})"
                return text
            
            elif element.name == 'img':
                alt = element.get('alt', '')
                src = element.get('src', '')
                if src:
                    return f"![{alt}]({src})\n"
                return ""
            
            elif element.name == 'strong' or element.name == 'b':
                return f"**{element.get_text()}**"
            
            elif element.name == 'em' or element.name == 'i':
                return f"*{element.get_text()}*"
            
            elif element.name == 'hr':
                return "\n---\n"
            
            elif element.name == 'br':
                return "\n"
            
            elif element.name == 'table':
                # Basic table support
                rows = element.find_all('tr')
                if not rows:
                    return ""
                
                table_md = []
                for i, row in enumerate(rows):
                    cells = row.find_all(['td', 'th'])
                    if cells:
                        row_text = " | ".join(cell.get_text().strip() for cell in cells)
                        table_md.append(f"| {row_text} |")
                        
                        # Add separator after header row
                        if i == 0:
                            separator = " | ".join("---" for _ in cells)
                            table_md.append(f"| {separator} |")
                
                return '\n'.join(table_md) + '\n' if table_md else ""
            
            # For other elements, process children
            results = []
            for child in element.children:
                result = process_element(child, depth + 1)
                if result:
                    results.append(result)
            
            return '\n'.join(results)
        
        # Process all children of the content
        for child in content.children:
            result = process_element(child)
            if result:
                markdown_parts.append(result)
        
        # Join and clean
        markdown_content = '\n'.join(markdown_parts)
        return self._clean_markdown_content(markdown_content)

    def _find_article_content_newspaper_fallback(self, soup: BeautifulSoup, article_text: str) -> Optional[Tag]:
        """Try to find the HTML element containing the article text."""
        # Get first few words of article text for matching
        article_words = article_text.split()[:20]
        search_text = ' '.join(article_words)
        
        # Look for elements containing this text
        for element in soup.find_all(['article', 'div', 'section', 'main']):
            if search_text in element.get_text():
                return element
        
        return None

    def _extract_best_title(self, soup: BeautifulSoup, url: str) -> str:
        """Extract the best title from various sources."""
        # Try multiple title sources in order of preference
        
        # 1. Look for article title in structured data
        json_ld = soup.find('script', type='application/ld+json')
        if json_ld:
            try:
                import json
                data = json.loads(json_ld.string)
                if isinstance(data, dict):
                    if 'headline' in data:
                        return data['headline']
                    elif 'name' in data:
                        return data['name']
            except:
                pass
        
        # 2. Look for Open Graph title
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            return og_title.get('content').strip()
        
        # 3. Look for Twitter title
        twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
        if twitter_title and twitter_title.get('content'):
            return twitter_title.get('content').strip()
        
        # 4. Look for h1 in article
        article = soup.find('article')
        if article:
            h1 = article.find('h1')
            if h1:
                return h1.get_text().strip()
        
        # 5. Look for any h1
        h1 = soup.find('h1')
        if h1:
            return h1.get_text().strip()
        
        # 6. Use title tag
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text().strip()
            # Clean common suffixes
            for suffix in [' | ', ' - ', ' — ', ' · ']:
                if suffix in title:
                    title = title.split(suffix)[0].strip()
            return title
        
        # 7. Fallback to URL
        return self._extract_title_from_url(url)

    def _clean_markdown_content(self, content: str) -> str:
        """Clean and format markdown content."""
        # Remove excessive blank lines
        content = re.sub(r'\n{4,}', '\n\n\n', content)
        
        # Remove trailing spaces
        content = '\n'.join(line.rstrip() for line in content.split('\n'))
        
        # Ensure headings have blank lines around them
        content = re.sub(r'(\n#{1,6} [^\n]+)\n(?![\n#])', r'\1\n\n', content)
        content = re.sub(r'(?<!\n\n)(#{1,6} [^\n]+)', r'\n\n\1', content)
        
        # Ensure code blocks have blank lines around them
        content = re.sub(r'(\n```[^\n]*\n[\s\S]*?\n```)\n(?!\n)', r'\1\n\n', content)
        content = re.sub(r'(?<!\n\n)(```[^\n]*\n)', r'\n\n\1', content)
        
        # Remove common footer patterns
        footer_patterns = [
            r'\n+Subscribe to.*?newsletter.*?$',
            r'\n+Sign up for.*?$',
            r'\n+Follow us on.*?$',
            r'\n+Share this.*?$',
            r'\n+Tags:.*?$',
            r'\n+Posted in.*?$',
            r'\n+Filed under.*?$',
        ]
        
        for pattern in footer_patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
        
        return content.strip()
    
    def _extract_with_html2text_direct(self, url: str) -> Tuple[str, str]:
        """Direct extraction using html2text as final fallback."""
        print("🔧 Using direct html2text extraction...")
        
        time.sleep(random.uniform(1.0, 2.0))
        
        response = self.session.get(url, timeout=30, allow_redirects=True)
        response.raise_for_status()
        
        # Handle redirects
        if response.history:
            print(f"🔄 Redirected to: {response.url}")
            url = response.url
        
        # Parse with BeautifulSoup first to get title
        soup = BeautifulSoup(response.content, "lxml")
        title = self._extract_best_title(soup, url)
        
        # Detect encoding properly
        encoding = response.encoding
        if encoding is None or encoding == 'ISO-8859-1':
            # Try to detect from content
            if response.content.startswith(b'\xef\xbb\xbf'):  # UTF-8 BOM
                encoding = 'utf-8-sig'
            else:
                # Try UTF-8 first
                try:
                    response.content.decode('utf-8')
                    encoding = 'utf-8'
                except UnicodeDecodeError:
                    # Fall back to response.apparent_encoding or latin-1
                    encoding = response.apparent_encoding or 'latin-1'
        
        # Decode content with proper encoding
        try:
            html_content = response.content.decode(encoding)
        except (UnicodeDecodeError, AttributeError):
            # If all else fails, try with errors='replace'
            html_content = response.content.decode('utf-8', errors='replace')
        
        # Use html2text directly on the HTML
        markdown_content = self.h2t.handle(html_content)
        
        # Clean up the markdown
        markdown_content = self._clean_markdown_content(markdown_content)
        
        # Ensure we have content
        if len(markdown_content.strip()) < 100:
            raise Exception("Insufficient content extracted with html2text")
        
        # Prepend title if not already in content
        if title and title not in markdown_content[:200]:
            markdown_content = f"# {title}\n\n{markdown_content}"
        
        return title, markdown_content

    def _extract_title_from_url(self, url: str) -> str:
        """Extract a title from URL path."""
        parsed_url = urlparse(url)
        path = parsed_url.path.strip("/")
        
        if path:
            # Get the last part of the path and clean it
            title = path.split("/")[-1]
            title = re.sub(r'[.-]', ' ', title)
            title = re.sub(r'\.[^.]*$', '', title)  # Remove file extension
            return title.replace("-", " ").replace("_", " ").title()
        
        return parsed_url.netloc

    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False


def extract_text_from_url_improved(url: str) -> Tuple[str, str]:
    """
    Extract article content and title from a URL with improved markdown preservation.

    Args:
        url: The URL to extract content from

    Returns:
        Tuple of (title, markdown_content)
    """
    extractor = ImprovedWebArticleExtractor()
    result = extractor.extract_article_from_url(url)
    
    # Ensure we always return a tuple
    if isinstance(result, tuple) and len(result) == 2:
        return result
    elif isinstance(result, str):
        # If only one string returned, use it as content and extract title from it
        lines = result.split('\n')
        if lines and lines[0].startswith('# '):
            title = lines[0][2:].strip()
            content = '\n'.join(lines[1:])
            return title, content
        else:
            # Fallback title
            return "Untitled", result
    else:
        raise ValueError(f"Unexpected return type from extractor: {type(result)}")