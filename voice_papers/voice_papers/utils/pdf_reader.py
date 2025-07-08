"""PDF reading utilities with improved extraction methods."""

from pathlib import Path
import pypdf
import pdfplumber

try:
    import fitz  # PyMuPDF

    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False
import re
from typing import Union, Tuple, Optional


def extract_title_from_academic_pdf(
    pdf_path: Union[str, Path], debug: bool = False
) -> Optional[str]:
    """Advanced title extraction specifically designed for academic papers."""
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if debug:
        print(f"🔍 Debug: Advanced academic PDF title extraction from {pdf_path.name}")

    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = pypdf.PdfReader(file)

            # Strategy 1: Check metadata first
            if pdf_reader.metadata and pdf_reader.metadata.title:
                title = pdf_reader.metadata.title.strip()
                if debug:
                    print(f"📊 Debug: Found metadata title: '{title}'")

                # Clean and validate metadata title
                title = re.sub(r"\s+", " ", title)
                if (
                    title
                    and len(title) > 5
                    and len(title) < 300
                    and not re.match(r"^[A-Z0-9_\-\.]+$", title)
                    and not title.lower().startswith(("untitled", "document", "paper"))
                ):
                    if debug:
                        print(f"✅ Debug: Using metadata title: '{title}'")
                    return title
                elif debug:
                    print(
                        f"❌ Debug: Metadata title rejected (len={len(title)}, pattern check)"
                    )
            elif debug:
                print("📊 Debug: No metadata title found")

            # Strategy 2: Multi-page academic analysis
            if len(pdf_reader.pages) > 0:
                # Extract text from first 2-3 pages to get more context
                full_text = ""
                pages_to_check = min(3, len(pdf_reader.pages))

                for page_num in range(pages_to_check):
                    page_text = pdf_reader.pages[page_num].extract_text()
                    full_text += f"\n--- PAGE {page_num + 1} ---\n" + page_text

                if debug:
                    print(
                        f"📄 Debug: Extracted text from {pages_to_check} pages ({len(full_text)} chars)"
                    )

                # Method 2A: Academic paper structure analysis
                title = _extract_academic_title_patterns(full_text, debug)
                if title:
                    return title

                # Method 2B: Content-based analysis
                title = _extract_title_by_content_analysis(full_text, debug)
                if title:
                    return title

    except Exception as e:
        error_msg = f"Warning: Could not extract title from PDF: {e}"
        if debug:
            print(f"💥 Debug: {error_msg}")
        else:
            print(error_msg)

    if debug:
        print("❌ Debug: No title found with advanced method")
    return None


def _extract_academic_title_patterns(text: str, debug: bool = False) -> Optional[str]:
    """Extract title using academic paper structure patterns."""
    if debug:
        print("🎓 Debug: Analyzing academic paper structure...")

    # Common academic paper section markers
    section_markers = [
        r"\babstract\b",
        r"\bkeywords?\b",
        r"\bintroduction\b",
        r"\b1\.?\s+(introduction|background)",
        r"\bmethodology\b",
        r"\brelated\s+work\b",
        r"\bliterature\s+review\b",
        r"\bexperiment(al)?\s+(setup|design|results)\b",
    ]

    # Split by pages first
    pages = text.split("--- PAGE")
    first_page = pages[1] if len(pages) > 1 else text  # Skip the empty first part

    # Remove common header/footer patterns
    lines = first_page.split("\n")
    cleaned_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Skip obvious header/footer content
        if any(
            pattern in line.lower()
            for pattern in [
                "doi:",
                "arxiv:",
                "page ",
                "published",
                "conference",
                "proceedings",
                "copyright",
                "©",
                "@",
                ".com",
                ".org",
                ".edu",
                "http",
                "volume",
                "issue",
                "issn",
                "isbn",
                "submitted",
                "accepted",
                "journal",
                "acm",
                "ieee",
                "springer",
            ]
        ):
            continue

        # Skip lines that are mostly numbers or formatting
        if re.match(r"^[\d\s\.\-\(\)]+$", line):
            continue

        # Skip very short lines that are likely artifacts
        if len(line) < 8:
            continue

        # Clean up the line
        line = re.sub(r"\s+", " ", line)
        cleaned_lines.append(line)

    if debug:
        print(f"📋 Debug: Academic analysis - found {len(cleaned_lines)} clean lines")
        print("📋 Debug: First 8 clean lines:")
        for i, line in enumerate(cleaned_lines[:8]):
            print(f"  {i+1}. '{line[:80]}{'...' if len(line) > 80 else ''}'")

    # Look for title before first section marker
    full_clean_text = "\n".join(cleaned_lines)

    for marker_pattern in section_markers:
        match = re.search(marker_pattern, full_clean_text, re.IGNORECASE)
        if match:
            before_section = full_clean_text[: match.start()].strip()
            potential_titles = [
                l.strip() for l in before_section.split("\n") if l.strip()
            ]

            if debug:
                print(
                    f"📍 Debug: Found section marker '{match.group()}' at position {match.start()}"
                )
                print(
                    f"📍 Debug: Content before marker has {len(potential_titles)} lines"
                )

            # Analyze potential titles before the section
            for i, candidate in enumerate(potential_titles):
                if _is_likely_academic_title(candidate, debug):
                    if debug:
                        print(
                            f"✅ Debug: Academic title found before '{match.group()}': '{candidate}'"
                        )
                    return candidate

    # Fallback: Look for title-like patterns in first few lines
    for i, line in enumerate(cleaned_lines[:10]):
        if _is_likely_academic_title(line, debug):
            if debug:
                print(f"✅ Debug: Academic title found by pattern matching: '{line}'")
            return line

    if debug:
        print("❌ Debug: No academic title pattern found")
    return None


def _extract_title_by_content_analysis(text: str, debug: bool = False) -> Optional[str]:
    """Extract title using content analysis and scoring."""
    if debug:
        print("📊 Debug: Content analysis for title extraction...")

    # Split into lines and clean
    lines = text.split("\n")
    candidates = []

    for i, line in enumerate(lines[:50]):  # Check first 50 lines across pages
        line = line.strip()
        if not line or "--- PAGE" in line:
            continue

        # Skip obvious non-title content
        if any(
            skip in line.lower()
            for skip in [
                "abstract",
                "keyword",
                "introduction",
                "author",
                "email",
                "university",
                "department",
                "doi:",
                "arxiv:",
                "copyright",
                "©",
                "@",
                "http",
                "page ",
                "figure",
                "table",
                "section",
                "chapter",
            ]
        ):
            continue

        # Skip lines that are mostly numbers or symbols
        if re.match(r"^[\d\s\.\-\(\)\[\]]+$", line):
            continue

        # Clean and score the line
        line = re.sub(r"\s+", " ", line).strip()
        if len(line) < 10 or len(line) > 200:
            continue

        score = _score_title_candidate(line, i)
        if score > 20:  # Minimum threshold
            candidates.append((score, line, i))

    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        best_score, best_title, position = candidates[0]

        if debug:
            print(f"🏆 Debug: Content analysis top 3 candidates:")
            for j, (score, title, pos) in enumerate(candidates[:3]):
                print(
                    f"  {j+1}. Score: {score}, Line: {pos+1}, Title: '{title[:60]}{'...' if len(title) > 60 else ''}'"
                )

        if best_score >= 30:
            if debug:
                print(
                    f"✅ Debug: Content analysis title (score: {best_score}): '{best_title}'"
                )
            return best_title
        elif debug:
            print(f"❌ Debug: Best content score {best_score} below threshold (30)")

    if debug:
        print("❌ Debug: No title found by content analysis")
    return None


def _is_likely_academic_title(text: str, debug: bool = False) -> bool:
    """Check if a text line is likely to be an academic paper title."""
    if len(text) < 10 or len(text) > 200:
        return False

    word_count = len(text.split())
    if word_count < 3 or word_count > 20:
        return False

    # Academic title characteristics
    score = 0

    # Length and word count in good range
    if 20 <= len(text) <= 120:
        score += 20
    if 4 <= word_count <= 15:
        score += 15

    # Proper capitalization
    words = text.split()
    capital_words = sum(1 for word in words if word and word[0].isupper())
    if capital_words >= len(words) * 0.6:  # Most words capitalized (title case)
        score += 20
    elif text[0].isupper():  # At least starts with capital
        score += 10

    # Common academic keywords boost
    academic_keywords = [
        "analysis",
        "approach",
        "framework",
        "method",
        "model",
        "system",
        "study",
        "research",
        "investigation",
        "evaluation",
        "assessment",
        "optimization",
        "algorithm",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "neural network",
        "data",
        "learning",
    ]

    text_lower = text.lower()
    keyword_matches = sum(1 for keyword in academic_keywords if keyword in text_lower)
    score += keyword_matches * 5

    # Punctuation patterns
    if ":" in text and text.count(":") == 1:  # Subtitle pattern
        score += 10

    # Avoid obvious non-titles
    bad_patterns = [
        r"\b(this|these|we|our|the authors?)\b",
        r"\b(table|figure|page|section)\s+\d+",
        r"\bemail\b",
        r"@",
        r"\bhttp\b",
    ]

    for pattern in bad_patterns:
        if re.search(pattern, text_lower):
            score -= 20

    return score >= 40


def _score_title_candidate(text: str, position: int) -> int:
    """Score a potential title candidate."""
    score = 0

    # Position bonus (earlier is better)
    if position <= 5:
        score += 30
    elif position <= 15:
        score += 20
    elif position <= 30:
        score += 10

    # Length bonus
    if 20 <= len(text) <= 120:
        score += 20
    elif 15 <= len(text) <= 150:
        score += 15

    # Word count bonus
    word_count = len(text.split())
    if 5 <= word_count <= 12:
        score += 20
    elif 3 <= word_count <= 18:
        score += 15

    # Capitalization bonus
    if text[0].isupper():
        score += 10

    # Special character penalty
    special_count = len(re.findall(r"[^\w\s\-:,.]", text))
    if special_count > len(text) * 0.1:
        score -= 15

    return score


def extract_title_from_pdf(
    pdf_path: Union[str, Path], debug: bool = False
) -> Optional[str]:
    """Extract the title from PDF - tries academic method first, then fallback to original."""
    # Try the new academic-focused method first
    title = extract_title_from_academic_pdf(pdf_path, debug)
    if title:
        return title

    # If that fails, try the original method as fallback
    if debug:
        print("🔄 Debug: Falling back to original extraction method...")

    pdf_path = Path(pdf_path)

    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = pypdf.PdfReader(file)

            # Original metadata check
            if pdf_reader.metadata and pdf_reader.metadata.title:
                title = pdf_reader.metadata.title.strip()
                title = re.sub(r"\s+", " ", title)
                if title and len(title) > 3 and len(title) < 300:
                    if not re.match(r"^[A-Z0-9_\-\.]+$", title):
                        if debug:
                            print(
                                f"✅ Debug: Using metadata title (fallback): '{title}'"
                            )
                        return title

            # Original content extraction as last resort
            if len(pdf_reader.pages) > 0:
                first_page_text = pdf_reader.pages[0].extract_text()
                lines = first_page_text.split("\n")

                for i, line in enumerate(lines[:10]):
                    line = line.strip()
                    if (
                        len(line) > 10
                        and not re.match(r"^\d+$", line)
                        and not re.match(r"^Page \d+", line, re.IGNORECASE)
                        and len(line.split()) >= 3
                    ):
                        if debug:
                            print(f"✅ Debug: Using fallback content title: '{line}'")
                        return line

    except Exception as e:
        if debug:
            print(f"💥 Debug: Fallback method failed: {e}")

    return None


def extract_text_with_pdfplumber(pdf_path: Union[str, Path]) -> str:
    """Extract text using pdfplumber - best for complex layouts."""
    pdf_path = Path(pdf_path)
    text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"pdfplumber extraction failed: {e}")
        return ""

    return text.strip()


def extract_text_with_pymupdf(pdf_path: Union[str, Path]) -> str:
    """Extract text using PyMuPDF - fast and handles various encodings well."""
    if not HAS_PYMUPDF:
        print("PyMuPDF not available, skipping...")
        return ""

    pdf_path = Path(pdf_path)
    text = ""

    try:
        pdf_document = fitz.open(str(pdf_path))
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text() + "\n"
        pdf_document.close()
    except Exception as e:
        print(f"PyMuPDF extraction failed: {e}")
        return ""

    return text.strip()


def extract_text_with_pypdf(pdf_path: Union[str, Path]) -> str:
    """Extract text using PyPDF - fallback method."""
    pdf_path = Path(pdf_path)
    text = ""

    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = pypdf.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"PyPDF extraction failed: {e}")
        return ""

    return text.strip()


def clean_extracted_text(text: str) -> str:
    """Clean extracted text to fix common issues."""
    # Fix hyphenated words at line breaks
    text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)

    # Fix common extraction artifacts
    text = re.sub(r"ﬁ", "fi", text)
    text = re.sub(r"ﬂ", "fl", text)
    text = re.sub(r"ﬀ", "ff", text)

    # Remove page numbers at line starts/ends
    text = re.sub(r"\n\d+\n", "\n", text)
    text = re.sub(r"^\d+\s", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s\d+$", "", text, flags=re.MULTILINE)

    # Fix paragraph breaks
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Don't collapse all newlines - preserve paragraph structure
    # Only fix multiple spaces within lines
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        # Fix multiple spaces within the line
        line = re.sub(r" +", " ", line)
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()


def extract_text_from_pdf(pdf_path: Union[str, Path], method: str = "auto") -> str:
    """
    Extract text content from a PDF file using multiple methods.

    Args:
        pdf_path: Path to the PDF file
        method: Extraction method - "auto", "pdfplumber", "pymupdf", or "pypdf"

    Returns:
        Extracted text content
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if method == "pdfplumber":
        text = extract_text_with_pdfplumber(pdf_path)
    elif method == "pymupdf":
        text = extract_text_with_pymupdf(pdf_path)
    elif method == "pypdf":
        text = extract_text_with_pypdf(pdf_path)
    elif method == "auto":
        # Try methods in order of reliability
        # print("Attempting text extraction with pdfplumber...")
        # text = extract_text_with_pdfplumber(pdf_path)
        text = None

        if not text or len(text) < 100:
            print("pdfplumber failed or returned insufficient text, trying PyMuPDF...")
            text = extract_text_with_pymupdf(pdf_path)

        if not text or len(text) < 100:
            print("PyMuPDF failed or returned insufficient text, trying PyPDF...")
            text = extract_text_with_pypdf(pdf_path)

        if not text:
            raise ValueError("All PDF extraction methods failed")
    else:
        raise ValueError(f"Unknown extraction method: {method}")

    # Clean the extracted text
    text = clean_extracted_text(text)
    return text


def extract_title_and_text_from_pdf(
    pdf_path: Union[str, Path], debug: bool = False, extraction_method: str = "auto"
) -> Tuple[Optional[str], str]:
    """Extract both title and text content from a PDF file."""
    title = extract_title_from_pdf(pdf_path, debug=debug)
    text = extract_text_from_pdf(pdf_path, method=extraction_method)
    return title, text
