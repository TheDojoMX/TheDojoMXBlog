"""Text cleaning utilities for academic papers."""

import re
from typing import List, Optional


class PaperTextCleaner:
    """Cleans academic paper text for better processing."""

    def __init__(self):
        self.reference_patterns = [
            r"\bReferences\b.*$",
            r"\bBibliography\b.*$",
            r"\bWorks Cited\b.*$",
            r"\bCitations\b.*$",
        ]

        self.footer_patterns = [
            r"^\d+\s*$",  # Page numbers alone
            r"^Page \d+.*$",
            r"^\s*©.*$",  # Copyright notices
            r"^\s*doi:.*$",  # DOI lines
            r"^\s*ISSN.*$",  # ISSN numbers
            r"^\s*ISBN.*$",  # ISBN numbers
        ]

        self.header_patterns = [
            r"^[A-Z\s]{10,}\s*$",  # ALL CAPS headers
            r"^.*Conference.*\d{4}.*$",  # Conference headers
            r"^.*Proceedings.*$",  # Proceedings headers
            r"^.*Journal.*Vol.*$",  # Journal headers
        ]

    def clean_paper_text(self, text: str) -> str:
        """Clean academic paper text for discussion."""
        lines = text.split("\n")
        cleaned_lines = []

        # Remove references section and everything after
        in_references = False
        for line in lines:
            # Check if we've hit the references section
            if any(
                re.search(pattern, line, re.IGNORECASE)
                for pattern in self.reference_patterns
            ):
                in_references = True
                break

            if not in_references:
                cleaned_lines.append(line)

        # Clean individual lines
        final_lines = []
        for line in cleaned_lines:
            cleaned_line = self._clean_line(line)
            if cleaned_line and not self._is_unwanted_line(cleaned_line):
                final_lines.append(cleaned_line)

        # Join and clean up spacing
        cleaned_text = "\n".join(final_lines)
        cleaned_text = self._normalize_spacing(cleaned_text)
        cleaned_text = self._remove_citation_noise(cleaned_text)

        return cleaned_text

    def _clean_line(self, line: str) -> str:
        """Clean individual line."""
        # Remove excessive whitespace
        line = re.sub(r"\s+", " ", line.strip())

        # Remove weird encoding artifacts but preserve more characters
        # Include unicode letters, numbers, and common punctuation
        line = re.sub(r"[^\w\s\.\,\;\:\!\?\(\)\[\]\-\+\=\%\$\&\@\#\'\"\–\—\/\°\•\…\'\'\"\"\´\`]", " ", line)

        # Remove standalone numbers at start of line (likely page numbers)
        line = re.sub(r"^\d+\s+", "", line)

        return line.strip()

    def _is_unwanted_line(self, line: str) -> bool:
        """Check if line should be removed."""
        # Don't remove very short lines if they could be titles/headers
        # (they often appear alone and have meaningful content)
        if len(line) < 3:  # Only remove truly empty/tiny lines
            return True

        # Check against footer patterns
        if any(
            re.match(pattern, line, re.IGNORECASE) for pattern in self.footer_patterns
        ):
            return True

        # Check against header patterns - but be more selective
        # Don't remove lines that could be section titles
        if any(
            re.match(pattern, line, re.IGNORECASE) for pattern in self.header_patterns
        ):
            # Additional check: if it's a potential title (has actual words), keep it
            word_count = len(re.findall(r'\b\w+\b', line))
            if word_count >= 2:  # Has at least 2 words, probably a title
                return False
            return True

        # Remove lines that are mostly punctuation or numbers
        # But be less aggressive - preserve potential titles
        alpha_content = re.sub(r"[\s\d\.\,\;\:\!\?\(\)\[\]\-]", "", line)
        if len(alpha_content) < 2 and len(line) > 20:  # Long line with no letters
            return True

        return False

    def _normalize_spacing(self, text: str) -> str:
        """Normalize spacing in text."""
        # Fix multiple spaces
        text = re.sub(r" +", " ", text)

        # Fix multiple newlines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Remove spaces before punctuation
        text = re.sub(r" +([.,;:!?])", r"\1", text)

        # Add space after punctuation if missing
        text = re.sub(r"([.,;:!?])([A-Za-z])", r"\1 \2", text)

        return text.strip()

    def _remove_citation_noise(self, text: str) -> str:
        """Remove inline citations and other academic noise."""
        # Remove inline citations like [1], [Smith et al., 2020], etc.
        text = re.sub(r"\[[^\]]*\d[^\]]*\]", "", text)

        # Remove et al. citations in parentheses
        text = re.sub(r"\([^)]*et al[^)]*\)", "", text)

        # Remove year-only citations like (2020), (2019-2021)
        text = re.sub(r"\(\s*\d{4}[^\)]*\)", "", text)

        # Remove figure and table references
        text = re.sub(r"[Ff]igure\s+\d+[a-z]?", "Figure", text)
        text = re.sub(r"[Tt]able\s+\d+[a-z]?", "Table", text)
        text = re.sub(r"[Ss]ection\s+\d+[\.\d]*", "Section", text)

        # Remove appendix references
        text = re.sub(r"[Aa]ppendix\s+[A-Z]\d*", "Appendix", text)

        # Clean up double spaces created by removals
        text = re.sub(r" +", " ", text)

        return text


def clean_paper_text(text: str) -> str:
    """Convenience function to clean paper text."""
    cleaner = PaperTextCleaner()
    return cleaner.clean_paper_text(text)


def extract_title_from_text(text: str, debug: bool = False) -> Optional[str]:
    """Extract title from the beginning of a text document with improved reliability."""
    lines = text.strip().split("\n")
    candidates = []

    if debug:
        print(f"🔍 Debug: Extracting title from text ({len(text)} characters)")

    # Clean and prepare lines
    cleaned_lines = []
    for line in lines[:20]:  # Check first 20 lines
        line = line.strip()
        if line:
            # Clean up common text artifacts
            line = re.sub(r"\s+", " ", line)  # Multiple spaces to single
            cleaned_lines.append(line)

    if debug:
        print(
            f"📄 Debug: Found {len(cleaned_lines)} meaningful lines in first 20 lines"
        )
        print("📋 Debug: First few lines:")
        for i, line in enumerate(cleaned_lines[:5]):
            print(f"  {i+1}. '{line[:80]}{'...' if len(line) > 80 else ''}'")

    # Analyze each potential title line
    for i, line in enumerate(cleaned_lines[:12]):  # Check first 12 meaningful lines
        if len(line) < 5 or len(line) > 250:  # Skip too short or too long
            continue

        # Skip obvious non-titles
        if any(
            pattern in line.lower()
            for pattern in [
                "abstract",
                "keywords",
                "introduction",
                "table of contents",
                "contents",
                "references",
                "bibliography",
                "appendix",
                "doi:",
                "issn",
                "isbn",
                "copyright",
                "©",
                "author:",
                "by:",
                "date:",
                "version:",
                "university",
                "department",
                "faculty",
                "email:",
                "@",
                "conference",
                "proceedings",
                "journal",
                "volume",
                "issue",
                "http",
                ".com",
                ".org",
                ".edu",
                "www.",
            ]
        ):
            if debug:
                print(
                    f"⏭️  Debug: Skipping line {i+1} (contains excluded pattern): '{line[:50]}...'"
                )
            continue

        # Skip lines that are mostly numbers, dates, or codes
        if re.match(r"^[\d\.\-\s/]+$", line):
            if debug:
                print(f"⏭️  Debug: Skipping line {i+1} (mostly numbers): '{line}'")
            continue

        # Skip lines that look like author names (simple pattern)
        if re.match(r"^[A-Z][a-z]+\s+[A-Z][a-z]+(\s+[A-Z][a-z]+)*$", line):
            if debug:
                print(f"⏭️  Debug: Skipping line {i+1} (looks like author): '{line}'")
            continue

        # Skip lines that are all caps and short (likely headers)
        if line.isupper() and len(line) < 50:
            if debug:
                print(f"⏭️  Debug: Skipping line {i+1} (all caps header): '{line}'")
            continue

        # Calculate title likelihood score
        score = 0

        # Position bonus (earlier is better, but first line might be metadata)
        if i <= 2:
            score += 25
        elif i <= 5:
            score += 15
        elif i <= 8:
            score += 5

        # Length bonus (titles are usually not too short or too long)
        if 15 <= len(line) <= 120:
            score += 20
        elif 10 <= len(line) <= 180:
            score += 15
        elif 5 <= len(line) <= 220:
            score += 10

        # Word count bonus (titles usually have 3-15 words)
        word_count = len(line.split())
        if 4 <= word_count <= 12:
            score += 20
        elif 3 <= word_count <= 15:
            score += 15
        elif 2 <= word_count <= 18:
            score += 10

        # Capitalization patterns
        if re.match(r"^[A-Z]", line):  # Starts with capital
            score += 10

        # Title case bonus
        words = line.split()
        title_case_words = sum(
            1 for word in words if word and len(word) > 1 and word[0].isupper()
        )
        if title_case_words >= len(words) * 0.6:  # Most words are capitalized
            score += 15

        # Sentence case bonus (first word cap, others mostly lowercase)
        if (
            words
            and words[0][0].isupper()
            and sum(1 for word in words[1:] if word and word[0].islower())
            >= len(words[1:]) * 0.7
        ):
            score += 12

        # Avoid lines with too many special characters
        special_chars = len(re.findall(r"[^\w\s\-]", line))
        if special_chars > len(line) * 0.15:  # More than 15% special chars
            score -= 15

        # Bonus for common title characteristics
        if ":" in line and line.count(":") == 1:  # Single colon (subtitle pattern)
            score += 8

        # Penalty for parentheses (often metadata)
        if "(" in line and ")" in line:
            score -= 5

        # Bonus if followed by empty line or significantly different content
        if i + 1 < len(cleaned_lines):
            next_line = cleaned_lines[i + 1]
            if not next_line or len(next_line) > len(line) * 1.4:
                score += 12
        elif i + 1 < len(lines) and not lines[i + 1].strip():  # Empty line after
            score += 10

        # Bonus if it's the only substantial line in first few positions
        substantial_lines_before = sum(
            1 for j in range(i) if j < len(cleaned_lines) and len(cleaned_lines[j]) > 20
        )
        if substantial_lines_before == 0 and len(line) > 20:
            score += 15

        # Look for patterns that suggest this is content, not title
        content_patterns = [
            r"\b(this|these|that|those|the)\s+(paper|article|study|research|work|document)\b",
            r"\b(we|our|us|authors?)\b",
            r"\b(abstract|summary|introduction|conclusion)\b",
            r"\bfigure\s+\d+\b",
            r"\btable\s+\d+\b",
        ]

        if any(re.search(pattern, line.lower()) for pattern in content_patterns):
            score -= 20

        candidates.append((score, line, i))

        if debug:
            print(
                f"📊 Debug: Line {i+1} score: {score} - '{line[:60]}{'...' if len(line) > 60 else ''}'"
            )

    # Find best candidate
    if candidates:
        # Sort by score (highest first)
        candidates.sort(key=lambda x: x[0], reverse=True)
        best_score, best_title, best_position = candidates[0]

        if debug:
            print(f"🏆 Debug: Top 3 title candidates:")
            for i, (score, title, pos) in enumerate(candidates[:3]):
                print(
                    f"  {i+1}. Score: {score}, Position: {pos+1}, Title: '{title[:60]}{'...' if len(title) > 60 else ''}'"
                )

        # Only return if score meets minimum threshold
        if best_score >= 30:  # Minimum confidence threshold
            if debug:
                print(f"✅ Debug: Using title (score: {best_score}): '{best_title}'")
            return best_title
        elif debug:
            print(f"❌ Debug: Best score {best_score} below threshold (30)")
    elif debug:
        print("❌ Debug: No title candidates found")

    # Fallback: look for text before common section markers
    full_text = "\n".join(cleaned_lines[:8])

    for separator in [
        "Abstract",
        "ABSTRACT",
        "Keywords",
        "KEYWORDS",
        "Introduction",
        "INTRODUCTION",
        "1.",
        "1 ",
    ]:
        if separator in full_text:
            if debug:
                print(f"📍 Debug: Found separator '{separator}'")
            before_separator = full_text[: full_text.find(separator)].strip()
            lines_before = [
                l.strip() for l in before_separator.split("\n") if l.strip()
            ]
            if lines_before:
                potential_title = lines_before[-1]
                if (
                    10 <= len(potential_title) <= 200
                    and len(potential_title.split()) >= 3
                    and not any(
                        skip in potential_title.lower()
                        for skip in ["author", "by:", "email", "@"]
                    )
                ):
                    if debug:
                        print(f"✅ Debug: Using fallback title: '{potential_title}'")
                    return potential_title
                elif debug:
                    print(
                        f"❌ Debug: Fallback title invalid: '{potential_title[:50]}...' ({len(potential_title)} chars, {len(potential_title.split())} words)"
                    )

    if debug:
        print("❌ Debug: No title found, will use filename")
    return None
