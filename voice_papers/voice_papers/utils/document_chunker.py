"""Document chunking utilities for better summarization."""

import re
from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class DocumentChunk:
    """Represents a chunk of the document with metadata."""

    content: str
    section_title: str
    chunk_index: int
    total_chunks: int
    start_char: int
    end_char: int

    @property
    def is_first(self) -> bool:
        return self.chunk_index == 0

    @property
    def is_last(self) -> bool:
        return self.chunk_index == self.total_chunks - 1


class DocumentChunker:
    """Intelligent document chunking for academic papers."""

    def __init__(self, chunk_size: int = 10000, overlap: int = 500):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.section_patterns = [
            # Main sections
            r"^(Abstract|Executive Summary|Resumen Ejecutivo)\s*$",
            r"^(Introduction|Introducción|Introduction and Context)\s*$",
            r"^(Methodology|Research Methodology|Metodología)\s*$",
            r"^(Results|Main Findings|Resultados|Findings)\s*$",
            r"^(Discussion|Analysis|Discusión|Critical Analysis)\s*$",
            r"^(Conclusion|Conclusions|Conclusión|Conclusiones)\s*$",
            r"^(References|Bibliography|Referencias)\s*$",
            # Subsections
            r"^(\d+\.?\s+.+)$",  # Numbered sections
            r"^([A-Z][^.!?]+)$",  # Title case lines that could be headers
        ]

    def chunk_document(self, text: str, title: str = "") -> List[DocumentChunk]:
        """Chunk document intelligently, preserving section boundaries when possible."""
        if not text or len(text.strip()) == 0:
            # Return a single chunk for empty documents
            return [
                DocumentChunk(
                    content=text,
                    section_title="Document",
                    chunk_index=0,
                    total_chunks=1,
                    start_char=0,
                    end_char=len(text),
                )
            ]

        # # First, try to identify sections
        # sections = self._identify_sections(text)

        # if sections:
        #     # Chunk by sections, respecting boundaries
        #     print(f"Sections found: {sections}")
        #     return self._chunk_by_sections(text, sections, title)
        # else:
        #     # Fall back to simple chunking with overlap
        #     print("No sections found, falling back to simple chunking")
        return self._simple_chunk(text, title)

    def _identify_sections(self, text: str) -> List[Tuple[int, int, str]]:
        """Identify section boundaries in the document."""
        lines = text.split("\n")
        sections = []
        current_section = "Introduction"
        section_start = 0

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            # Check if this line matches any section pattern
            for pattern in self.section_patterns:
                if re.match(pattern, line, re.IGNORECASE):
                    # Calculate character position
                    char_pos = len("\n".join(lines[:i]))
                    if sections:
                        # Close previous section
                        sections[-1] = (sections[-1][0], char_pos, sections[-1][2])
                    # Start new section
                    sections.append((char_pos, -1, line))
                    current_section = line
                    break

        # Close last section
        if sections:
            sections[-1] = (sections[-1][0], len(text), sections[-1][2])

        return sections

    def _chunk_by_sections(
        self, text: str, sections: List[Tuple[int, int, str]], title: str
    ) -> List[DocumentChunk]:
        """Chunk document by sections, breaking large sections if needed."""
        chunks = []

        for start, end, section_title in sections:
            section_content = text[start:end].strip()

            if len(section_content) <= self.chunk_size:
                # Section fits in one chunk
                chunks.append(
                    DocumentChunk(
                        content=section_content,
                        section_title=section_title,
                        chunk_index=len(chunks),
                        total_chunks=-1,  # Will update later
                        start_char=start,
                        end_char=end,
                    )
                )
            else:
                # Break large section into smaller chunks
                section_chunks = self._break_section_into_chunks(
                    section_content, section_title, start
                )
                chunks.extend(section_chunks)

        # Update total chunks count
        for chunk in chunks:
            chunk.total_chunks = len(chunks)

        return chunks

    def _break_section_into_chunks(
        self, content: str, section_title: str, section_start: int
    ) -> List[DocumentChunk]:
        """Break a large section into smaller chunks with overlap."""
        chunks = []
        current_pos = 0

        while current_pos < len(content):
            # Find chunk boundaries
            chunk_start = max(0, current_pos - self.overlap if current_pos > 0 else 0)
            chunk_end = min(current_pos + self.chunk_size, len(content))

            # Try to break at paragraph boundaries
            if chunk_end < len(content):
                # Look for paragraph break near the end
                paragraph_break = content.rfind(
                    "\n\n", chunk_start + self.chunk_size // 2, chunk_end
                )
                if paragraph_break > chunk_start:
                    chunk_end = paragraph_break
                else:
                    # Look for sentence break
                    sentence_break = max(
                        content.rfind(
                            ". ", chunk_start + self.chunk_size // 2, chunk_end
                        ),
                        content.rfind(
                            ".\n", chunk_start + self.chunk_size // 2, chunk_end
                        ),
                    )
                    if sentence_break > chunk_start:
                        chunk_end = sentence_break + 1

            chunk_content = content[chunk_start:chunk_end].strip()

            chunks.append(
                DocumentChunk(
                    content=chunk_content,
                    section_title=f"{section_title} (Part {len(chunks) + 1})",
                    chunk_index=-1,  # Will update later
                    total_chunks=-1,  # Will update later
                    start_char=section_start + chunk_start,
                    end_char=section_start + chunk_end,
                )
            )

            # Move to next chunk
            current_pos = chunk_end - self.overlap

        return chunks

    def _simple_chunk(self, text: str, title: str) -> List[DocumentChunk]:
        """Simple chunking with overlap for documents without clear sections."""
        chunks = []
        current_pos = 0
        
        # Ensure we have valid chunk size and overlap
        if self.chunk_size <= 0:
            self.chunk_size = 10000
        if self.overlap < 0 or self.overlap >= self.chunk_size:
            self.overlap = min(500, self.chunk_size // 10)

        # Add progress tracking
        import click
        total_length = len(text)
        
        while current_pos < len(text):
            # Show progress
            progress = (current_pos / total_length) * 100
            if len(chunks) % 5 == 0 and chunks:  # Log every 5 chunks
                click.echo(f"   📄 Chunking progress: {progress:.1f}% ({len(chunks)} chunks created)")
            
            # Calculate chunk boundaries
            chunk_start = current_pos
            chunk_end = min(current_pos + self.chunk_size, len(text))

            # Try to break at natural boundaries if not at end of text
            if chunk_end < len(text):
                # Look for paragraph boundary
                search_start = max(chunk_start, chunk_end - self.chunk_size // 4)
                para_break = text.rfind("\n\n", search_start, chunk_end)
                
                if para_break > chunk_start:
                    chunk_end = para_break
                else:
                    # Look for sentence boundary
                    sent_break = text.rfind(". ", search_start, chunk_end)
                    if sent_break > chunk_start:
                        chunk_end = sent_break + 1
                    else:
                        # Look for line break
                        line_break = text.rfind("\n", search_start, chunk_end)
                        if line_break > chunk_start:
                            chunk_end = line_break

            # Extract chunk content
            chunk_content = text[chunk_start:chunk_end].strip()
            
            # Only add non-empty chunks
            if chunk_content:
                chunks.append(
                    DocumentChunk(
                        content=chunk_content,
                        section_title=f"Section {len(chunks) + 1}",
                        chunk_index=len(chunks),
                        total_chunks=-1,  # Will update later
                        start_char=chunk_start,
                        end_char=chunk_end,
                    )
                )

            # Move to next position
            # Ensure we make progress to avoid infinite loop
            if chunk_end <= current_pos:
                current_pos += self.chunk_size
            else:
                # Move forward but maintain overlap
                current_pos = chunk_end - self.overlap
                # Ensure we don't go backwards
                if current_pos <= chunk_start:
                    current_pos = chunk_end

        # Update total chunks count
        for chunk in chunks:
            chunk.total_chunks = len(chunks)

        return chunks

    def create_chunk_summary_prompt(
        self, chunk: DocumentChunk, paper_title: str
    ) -> str:
        """Create a prompt for summarizing a specific chunk."""
        position_context = ""
        if chunk.is_first:
            position_context = "This is the beginning of the document."
        elif chunk.is_last:
            position_context = "This is the final part of the document."
        else:
            position_context = (
                f"This is part {chunk.chunk_index + 1} of {chunk.total_chunks}."
            )

        return f"""
Analyze this section from the paper "{paper_title}".
Section: {chunk.section_title}
{position_context}

Extract and preserve:
1. Key findings, insights, and arguments
2. Important data, statistics, or evidence
3. Novel concepts or frameworks introduced
4. Connections to other parts (if mentioned)
5. Implications and significance
6. Any controversies or debates
7. Technical details that matter

Content:
{chunk.content}

Create a comprehensive summary that captures the DEPTH and NUANCE of this section.
Don't just list points - explain the reasoning, evidence, and why it matters.
"""
