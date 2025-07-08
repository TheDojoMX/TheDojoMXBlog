"""Web article reading utilities."""

import re
import requests
from typing import Union, Tuple
from urllib.parse import urlparse
from pathlib import Path
import hashlib
import random
import time
from newspaper import Article
from bs4 import BeautifulSoup


class WebArticleExtractor:
    """Extracts article content from web URLs with anti-blocking measures."""

    def __init__(self):
        self.session = requests.Session()
        self._setup_session()

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

        # Configure timeouts and other session parameters
        self.session.timeout = 30

        # Add random delay to avoid detection
        time.sleep(random.uniform(0.5, 2.0))

    def extract_article_from_url(self, url: str) -> Tuple[str, str]:
        """
        Extract article content and title from a URL.

        Args:
            url: The URL to extract content from

        Returns:
            Tuple of (title, content)

        Raises:
            Exception: If content extraction fails
        """
        if not self._is_valid_url(url):
            raise ValueError(f"Invalid URL: {url}")

        print(f"🌐 Extracting content from: {url}")

        # Try newspaper3k first with custom config
        try:
            return self._extract_with_newspaper(url)
        except Exception as e:
            print(f"Newspaper3k failed: {e}")

        # Fallback to BeautifulSoup with better session
        try:
            return self._extract_with_beautifulsoup(url)
        except Exception as e:
            raise Exception(f"Both extraction methods failed. Last error: {e}")

    def _extract_with_newspaper(self, url: str) -> Tuple[str, str]:
        """Extract using newspaper3k library with custom configuration."""
        # Configure newspaper with better headers
        config = {
            "headers": self.session.headers,
            "timeout": 30,
            "follow_meta_refresh": True,
            "memoize_articles": False,
        }

        article = Article(url, **config)

        # Add random delay
        time.sleep(random.uniform(1.0, 3.0))

        article.download()
        article.parse()

        if not article.text.strip():
            raise Exception("No content extracted with newspaper3k")

        title = article.title or self._extract_title_from_url(url)
        content = article.text.strip()

        return title, content

    def _extract_with_beautifulsoup(self, url: str) -> Tuple[str, str]:
        """Fallback extraction using BeautifulSoup with anti-blocking measures."""
        print("🔄 Trying BeautifulSoup extraction...")

        # Add additional headers specific to the domain
        domain = urlparse(url).netloc
        additional_headers = self._get_domain_specific_headers(domain)

        # Create a new session for this request
        session = requests.Session()
        session.headers.update(self.session.headers)
        session.headers.update(additional_headers)

        # Add random delay
        time.sleep(random.uniform(2.0, 4.0))

        try:
            response = session.get(url, timeout=30, allow_redirects=True)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print("🚫 403 Forbidden - trying alternative approach...")
                return self._try_alternative_extraction(url, session)
            raise

        soup = BeautifulSoup(response.content, "lxml")

        # Extract title
        title_element = soup.find("title")
        title = (
            title_element.get_text().strip()
            if title_element
            else self._extract_title_from_url(url)
        )

        # Remove unwanted elements
        for element in soup(
            ["script", "style", "nav", "header", "footer", "aside", "form", "iframe"]
        ):
            element.decompose()

        # Try to find main content
        content = self._extract_main_content(soup)

        if not content.strip():
            raise Exception("No content extracted with BeautifulSoup")

        return title, content

    def _get_domain_specific_headers(self, domain: str) -> dict:
        """Get headers specific to certain domains."""
        headers = {}

        if "fastcompany.com" in domain:
            headers.update(
                {
                    "Referer": "https://www.google.com/",
                    "Sec-Ch-Ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Platform": '"Windows"',
                }
            )
        elif "medium.com" in domain:
            headers.update(
                {"Referer": "https://medium.com/", "X-Requested-With": "XMLHttpRequest"}
            )
        elif any(
            news_site in domain
            for news_site in ["nytimes.com", "wsj.com", "bloomberg.com"]
        ):
            headers.update({"Referer": "https://www.google.com/", "Priority": "u=0, i"})

        return headers

    def _try_alternative_extraction(
        self, url: str, session: requests.Session
    ) -> Tuple[str, str]:
        """Try alternative extraction methods for blocked requests."""
        print("🔄 Attempting alternative extraction...")

        # Strategy 1: Try with minimal headers and longer delay
        minimal_session = requests.Session()
        minimal_session.headers.clear()
        minimal_session.headers.update(
            {"User-Agent": "Mozilla/5.0 (compatible; Educational Content Extractor)"}
        )

        # Add much longer delay for aggressive blocking
        delay = random.uniform(8.0, 15.0)
        print(f"⏳ Waiting {delay:.1f} seconds to avoid detection...")
        time.sleep(delay)

        try:
            response = minimal_session.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "lxml")

            # Try simple extraction
            title = soup.find("title")
            title = (
                title.get_text().strip() if title else self._extract_title_from_url(url)
            )

            # Get all text content
            content = soup.get_text(separator="\n", strip=True)

            if len(content) > 1000:  # Minimum viable content
                return title, content
            else:
                raise Exception("Insufficient content extracted")

        except Exception as e:
            print(f"Minimal approach failed: {e}")

        # Strategy 2: Try with different User-Agent rotation
        for attempt in range(3):
            try:
                print(f"🔄 Attempt {attempt + 1}/3 with rotated headers...")

                # Create completely new session each time
                new_session = requests.Session()
                new_session.headers.clear()

                # Rotate through different browser signatures
                user_agents = [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
                    "Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
                    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                ]

                selected_ua = random.choice(user_agents)
                new_session.headers.update(
                    {
                        "User-Agent": selected_ua,
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Language": "en-US,en;q=0.5",
                        "Accept-Encoding": "gzip, deflate",
                        "Connection": "keep-alive",
                        "Upgrade-Insecure-Requests": "1",
                    }
                )

                # Add even longer delays between attempts
                delay = random.uniform(12.0, 20.0)
                print(f"⏳ Waiting {delay:.1f} seconds before attempt...")
                time.sleep(delay)

                response = new_session.get(url, timeout=30, allow_redirects=True)
                response.raise_for_status()

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "lxml")

                    # Try simple extraction
                    title = soup.find("title")
                    title = (
                        title.get_text().strip()
                        if title
                        else self._extract_title_from_url(url)
                    )

                    # Get all text content
                    content = soup.get_text(separator="\n", strip=True)

                    if len(content) > 1000:
                        print(f"✅ Success with User-Agent: {selected_ua[:50]}...")
                        return title, content

            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < 2:  # Not the last attempt
                    time.sleep(random.uniform(5.0, 10.0))

        # Strategy 3: Last resort - try to suggest alternative approach
        raise Exception(
            f"All extraction methods failed for {url}. This site uses advanced bot protection (DataDome). Consider: 1) Using archive.org/web/ version of the URL, 2) Finding the same article on a different site, or 3) Copying the content manually to a text file."
        )

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main article content from soup with improved selectors."""
        # Enhanced article selectors (ordered by preference)
        article_selectors = [
            "article",
            '[role="main"]',
            ".article-content",
            ".post-content",
            ".entry-content",
            ".story-content",
            ".article-body",
            ".post-body",
            ".story-body",
            ".content-body",
            ".main-content",
            ".primary-content",
            ".post-wrapper",
            ".article-wrapper",
            "main",
            "#content",
            ".content",
        ]

        # Try each selector
        for selector in article_selectors:
            elements = soup.select(selector)
            if elements:
                # Get text from the first matching element
                content = elements[0].get_text(separator="\n", strip=True)
                if len(content) > 500:  # Minimum content length
                    return self._clean_extracted_content(content)

        # Enhanced fallback: get paragraph text with better filtering
        paragraphs = soup.find_all("p")
        content_parts = []

        for p in paragraphs:
            text = p.get_text().strip()
            if len(text) > 20:  # Filter out very short paragraphs
                content_parts.append(text)

        content = "\n".join(content_parts)
        return self._clean_extracted_content(content)

    def _clean_extracted_content(self, content: str) -> str:
        """Clean extracted content."""
        # Remove excessive whitespace
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r" {2,}", " ", content)

        # Remove common unwanted patterns
        unwanted_patterns = [
            r"Subscribe to.*newsletter",
            r"Sign up for.*",
            r"Follow us on.*",
            r"Advertisement",
            r"ADVERTISEMENT",
            r"Cookie Policy",
            r"Privacy Policy",
            r"Terms of Service",
        ]

        for pattern in unwanted_patterns:
            content = re.sub(pattern, "", content, flags=re.IGNORECASE)

        return content.strip()

    def _extract_title_from_url(self, url: str) -> str:
        """Extract a title from URL path."""
        parsed_url = urlparse(url)
        path = parsed_url.path.strip("/")

        if path:
            # Get the last part of the path and clean it
            title = path.split("/")[-1]
            title = re.sub(r"[.-]", " ", title)
            title = re.sub(r"\.[^.]*$", "", title)  # Remove file extension
            return title.replace("-", " ").replace("_", " ").title()

        return parsed_url.netloc

    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False


def extract_text_from_url(url: str) -> Tuple[str, str]:
    """
    Extract article content and title from a URL.

    Args:
        url: The URL to extract content from

    Returns:
        Tuple of (title, content)
    """
    # Try improved extractor first for better markdown preservation
    try:
        from .web_reader_improved import extract_text_from_url_improved
        return extract_text_from_url_improved(url)
    except ImportError:
        # Fallback to basic extractor if improved version not available
        pass
    except Exception as e:
        print(f"Improved extraction failed, falling back to basic: {e}")
    
    # Fallback to original extractor
    extractor = WebArticleExtractor()
    return extractor.extract_article_from_url(url)


def generate_cache_filename(url: str) -> str:
    """Generate a cache filename from URL."""
    # Create a hash of the URL for filename
    url_hash = hashlib.md5(url.encode()).hexdigest()[:10]

    # Extract domain for human readability
    domain = urlparse(url).netloc.replace("www.", "")
    domain = re.sub(r"[^\w.-]", "_", domain)

    return f"{domain}_{url_hash}_extracted_text.txt"
