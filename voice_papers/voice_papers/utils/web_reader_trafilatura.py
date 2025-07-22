"""Web article reading using Trafilatura for robust extraction."""

import trafilatura
from typing import Tuple, Optional
from urllib.parse import urlparse
import requests
import time
import random


class TrafilaturaExtractor:
    """Extracts article content from web URLs using Trafilatura."""
    
    def __init__(self):
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self):
        """Configure session with realistic headers."""
        # Modern User-Agents
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
        ]
        
        selected_ua = random.choice(user_agents)
        
        headers = {
            "User-Agent": selected_ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        
        self.session.headers.update(headers)
    
    def extract_article_from_url(self, url: str) -> Tuple[str, str]:
        """
        Extract article content and title from a URL using Trafilatura.
        
        Args:
            url: The URL to extract content from
            
        Returns:
            Tuple of (title, content)
            
        Raises:
            Exception: If content extraction fails
        """
        print(f"🌐 Extracting content with Trafilatura from: {url}")
        
        # Add small delay to be polite
        time.sleep(random.uniform(0.5, 1.5))
        
        try:
            # Fetch the page using our session (with proper headers)
            response = self.session.get(url, timeout=30, allow_redirects=True)
            response.raise_for_status()
            
            # Handle redirects
            if response.history:
                print(f"🔄 Redirected to: {response.url}")
                url = response.url
            
            # Use Trafilatura to extract content
            # It handles encoding automatically
            html = response.content
            
            # Extract with Trafilatura
            # include_formatting=True preserves some structure
            # include_links=True keeps links
            # output_format='markdown' gives us markdown output
            content = trafilatura.extract(
                html,
                output_format='markdown',
                include_formatting=True,
                include_links=True,
                include_images=True,
                include_tables=True,
                deduplicate=True,
                url=url,  # Helps with relative URLs
                favor_precision=True,  # Better precision
                include_comments=False,  # Skip comments
                target_language='en',  # Ensure English extraction
            )
            
            if not content:
                # Try with different settings if first attempt fails
                print("⚠️  First extraction attempt failed, trying with relaxed settings...")
                content = trafilatura.extract(
                    html,
                    output_format='markdown',
                    include_formatting=True,
                    include_links=True,
                    favor_recall=True,  # More content, less precision
                )
            
            if not content:
                raise Exception("Trafilatura could not extract any content")
            
            # Extract metadata for title
            metadata = trafilatura.extract_metadata(html, url)
            
            # Get title from metadata or extract from content
            title = None
            if metadata:
                title = metadata.title or metadata.sitename
            
            if not title:
                # Try to extract from first line if it's a heading
                lines = content.split('\n')
                if lines and lines[0].startswith('#'):
                    title = lines[0].strip('#').strip()
                    # Remove title from content if found
                    content = '\n'.join(lines[1:]).strip()
                else:
                    # Fallback to URL-based title
                    title = self._extract_title_from_url(url)
            
            # Ensure we have clean content
            content = content.strip()
            
            # Add title as first line if not already there
            if not content.startswith(f"# {title}"):
                content = f"# {title}\n\n{content}"
            
            print(f"✅ Extracted {len(content)} characters of content")
            print(f"📑 Title: {title}")
            
            return title, content
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch URL: {e}")
        except Exception as e:
            raise Exception(f"Extraction failed: {e}")
    
    def _extract_title_from_url(self, url: str) -> str:
        """Extract a title from URL path as fallback."""
        parsed_url = urlparse(url)
        path = parsed_url.path.strip("/")
        
        if path:
            # Get the last part of the path and clean it
            title = path.split("/")[-1]
            title = title.replace("-", " ").replace("_", " ")
            # Remove file extension if any
            if "." in title:
                title = title.rsplit(".", 1)[0]
            return title.title()
        
        return parsed_url.netloc


def extract_text_from_url_trafilatura(url: str) -> Tuple[str, str]:
    """
    Extract article content and title from a URL using Trafilatura.
    
    Args:
        url: The URL to extract content from
        
    Returns:
        Tuple of (title, content)
    """
    extractor = TrafilaturaExtractor()
    return extractor.extract_article_from_url(url)