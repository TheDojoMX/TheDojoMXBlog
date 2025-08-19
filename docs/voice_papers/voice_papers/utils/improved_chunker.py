"""Improved document chunking with flexible content type handling."""

import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ContentType(Enum):
    """Types of content that can be processed."""
    ACADEMIC_PAPER = "academic_paper"
    BLOG_POST = "blog_post"
    NEWS_ARTICLE = "news_article"
    TECHNICAL_DOCUMENTATION = "technical_documentation"
    BOOK_CHAPTER = "book_chapter"
    GENERAL_TEXT = "general_text"


@dataclass
class ImprovedChunk:
    """Enhanced chunk with better metadata."""
    content: str
    context_type: str  # e.g., "introduction", "main_argument", "evidence", "conclusion"
    chunk_index: int
    total_chunks: int
    start_char: int
    end_char: int
    key_concepts: List[str] = None
    tone: str = "neutral"  # e.g., "technical", "conversational", "narrative"
    
    @property
    def section_title(self) -> str:
        """Generate a section title for compatibility."""
        return f"{self.context_type.replace('_', ' ').title()}"
    
    @property
    def is_first(self) -> bool:
        return self.chunk_index == 0
    
    @property
    def is_last(self) -> bool:
        return self.chunk_index == self.total_chunks - 1


class ImprovedDocumentChunker:
    """Flexible document chunking that preserves content spirit."""
    
    def __init__(self, chunk_size: int = 10000, overlap: int = 500):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def detect_content_type(self, text: str, filename: str = "") -> ContentType:
        """Detect the type of content based on structure and language."""
        text_lower = text.lower()[:3000]  # Check first 3000 chars
        
        # Academic paper indicators
        if any(keyword in text_lower for keyword in [
            "abstract", "methodology", "results", "conclusion", "references",
            "doi:", "journal", "peer-reviewed", "hypothesis"
        ]):
            return ContentType.ACADEMIC_PAPER
        
        # Technical documentation
        if any(keyword in text_lower for keyword in [
            "installation", "api reference", "configuration", "usage",
            "parameters", "returns:", "example:", "code block"
        ]):
            return ContentType.TECHNICAL_DOCUMENTATION
        
        # Blog post indicators
        if any(keyword in text_lower for keyword in [
            "posted on", "comments", "share this", "tags:", "category:",
            "previous post", "next post", "subscribe"
        ]) or filename.lower().endswith(('.html', '.htm')):
            return ContentType.BLOG_POST
        
        # News article
        if any(keyword in text_lower for keyword in [
            "breaking:", "update:", "reporter", "correspondent",
            "according to sources", "press release", "statement"
        ]):
            return ContentType.NEWS_ARTICLE
        
        # Book chapter
        if any(keyword in text_lower for keyword in [
            "chapter", "table of contents", "isbn", "publisher",
            "copyright", "edition", "preface"
        ]):
            return ContentType.BOOK_CHAPTER
        
        return ContentType.GENERAL_TEXT
    
    def chunk_document(
        self, 
        text: str, 
        title: str = "",
        content_type: Optional[ContentType] = None,
        preserve_tone: bool = True
    ) -> List[ImprovedChunk]:
        """Chunk document while preserving its spirit and structure."""
        
        # Detect content type if not provided
        if content_type is None:
            content_type = self.detect_content_type(text, title)
        
        # Detect document tone
        tone = self._detect_tone(text)
        
        # Choose chunking strategy based on content type
        if content_type == ContentType.ACADEMIC_PAPER:
            return self._chunk_academic_paper(text, title, tone)
        elif content_type == ContentType.BLOG_POST:
            return self._chunk_blog_post(text, title, tone)
        elif content_type == ContentType.NEWS_ARTICLE:
            return self._chunk_news_article(text, title, tone)
        elif content_type == ContentType.TECHNICAL_DOCUMENTATION:
            return self._chunk_technical_docs(text, title, tone)
        else:
            return self._chunk_general_text(text, title, tone)
    
    def _detect_tone(self, text: str) -> str:
        """Detect the overall tone of the document."""
        sample = text[:2000].lower()
        
        # Technical tone indicators
        technical_score = sum([
            sample.count(term) for term in [
                "algorithm", "implementation", "performance", "optimization",
                "analysis", "methodology", "framework", "architecture"
            ]
        ])
        
        # Conversational tone indicators
        conversational_score = sum([
            sample.count(term) for term in [
                "you", "your", "we'll", "let's", "imagine", "think about",
                "?", "!", "here's", "that's"
            ]
        ])
        
        # Narrative tone indicators
        narrative_score = sum([
            sample.count(term) for term in [
                "story", "journey", "experience", "felt", "realized",
                "discovered", "happened", "remember"
            ]
        ])
        
        # Determine dominant tone
        scores = {
            "technical": technical_score,
            "conversational": conversational_score,
            "narrative": narrative_score
        }
        
        max_score = max(scores.values())
        if max_score > 5:  # Threshold for significant tone
            return max(scores, key=scores.get)
        return "neutral"
    
    def _identify_logical_sections(self, text: str) -> List[Tuple[int, int, str]]:
        """Identify logical sections in any document type."""
        sections = []
        lines = text.split('\n')
        
        # Pattern for various section headers
        header_patterns = [
            # Markdown headers
            (r'^#{1,6}\s+(.+)$', 'markdown'),
            # Numbered sections
            (r'^(\d+\.?\s+[A-Z].+)$', 'numbered'),
            # Title case headers (at least 3 words)
            (r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+){2,})$', 'title_case'),
            # All caps headers
            (r'^([A-Z\s]{4,})$', 'all_caps'),
            # Underlined headers
            (r'^(.+)\n[=-]+$', 'underlined'),
        ]
        
        current_pos = 0
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            if not line_stripped:
                continue
            
            for pattern, style in header_patterns:
                match = re.match(pattern, line_stripped)
                if match:
                    # Calculate character position
                    char_pos = len('\n'.join(lines[:i]))
                    
                    # Close previous section
                    if sections:
                        sections[-1] = (sections[-1][0], char_pos, sections[-1][2])
                    
                    # Start new section
                    header_text = match.group(1) if style != 'underlined' else lines[i-1].strip()
                    sections.append((char_pos, -1, header_text))
                    break
        
        # Close last section
        if sections:
            sections[-1] = (sections[-1][0], len(text), sections[-1][2])
        
        return sections
    
    def _chunk_academic_paper(self, text: str, title: str, tone: str) -> List[ImprovedChunk]:
        """Chunk academic paper with research-aware structure."""
        chunks = []
        sections = self._identify_logical_sections(text)
        
        # Academic context mapping
        context_map = {
            "abstract": ["abstract", "summary", "resumen"],
            "introduction": ["introduction", "background", "introducción"],
            "methodology": ["method", "approach", "methodology", "materials"],
            "results": ["results", "findings", "outcomes", "resultados"],
            "discussion": ["discussion", "analysis", "implications"],
            "conclusion": ["conclusion", "conclusions", "future work"],
            "references": ["references", "bibliography", "citations"]
        }
        
        if sections:
            for start, end, section_title in sections:
                section_content = text[start:end].strip()
                
                # Determine context type
                context_type = "body"
                section_lower = section_title.lower()
                for ctx, keywords in context_map.items():
                    if any(kw in section_lower for kw in keywords):
                        context_type = ctx
                        break
                
                # Extract key concepts from section
                key_concepts = self._extract_key_concepts(section_content)
                
                # Chunk large sections
                if len(section_content) > self.chunk_size:
                    sub_chunks = self._break_section_intelligently(
                        section_content, section_title, start, context_type, tone, key_concepts
                    )
                    chunks.extend(sub_chunks)
                else:
                    chunks.append(ImprovedChunk(
                        content=section_content,
                        context_type=context_type,
                        chunk_index=len(chunks),
                        total_chunks=-1,
                        start_char=start,
                        end_char=end,
                        key_concepts=key_concepts,
                        tone=tone
                    ))
        else:
            # Fallback to intelligent chunking
            chunks = self._chunk_general_text(text, title, tone)
        
        # Update total chunks
        for chunk in chunks:
            chunk.total_chunks = len(chunks)
        
        return chunks
    
    def _chunk_blog_post(self, text: str, title: str, tone: str) -> List[ImprovedChunk]:
        """Chunk blog post preserving narrative flow."""
        chunks = []
        
        # Blog posts often have natural breaks
        paragraphs = text.split('\n\n')
        current_chunk = ""
        current_start = 0
        
        for i, paragraph in enumerate(paragraphs):
            if len(current_chunk) + len(paragraph) > self.chunk_size and current_chunk:
                # Determine context based on position
                if i < len(paragraphs) * 0.2:
                    context = "introduction"
                elif i > len(paragraphs) * 0.8:
                    context = "conclusion"
                else:
                    context = "main_content"
                
                chunks.append(ImprovedChunk(
                    content=current_chunk.strip(),
                    context_type=context,
                    chunk_index=len(chunks),
                    total_chunks=-1,
                    start_char=current_start,
                    end_char=current_start + len(current_chunk),
                    tone=tone
                ))
                current_chunk = paragraph + "\n\n"
                current_start += len(current_chunk)
            else:
                current_chunk += paragraph + "\n\n"
        
        # Add remaining content
        if current_chunk.strip():
            chunks.append(ImprovedChunk(
                content=current_chunk.strip(),
                context_type="conclusion" if len(chunks) > 0 else "main_content",
                chunk_index=len(chunks),
                total_chunks=-1,
                start_char=current_start,
                end_char=len(text),
                tone=tone
            ))
        
        # Update totals
        for chunk in chunks:
            chunk.total_chunks = len(chunks)
        
        return chunks
    
    def _chunk_news_article(self, text: str, title: str, tone: str) -> List[ImprovedChunk]:
        """Chunk news article preserving journalistic structure."""
        # Similar to blog but with news-specific context
        chunks = self._chunk_blog_post(text, title, tone)
        
        # Adjust context types for news
        for i, chunk in enumerate(chunks):
            if i == 0:
                chunk.context_type = "lead"  # Opening paragraph(s)
            elif i < len(chunks) * 0.3:
                chunk.context_type = "key_facts"
            elif i < len(chunks) * 0.7:
                chunk.context_type = "details"
            else:
                chunk.context_type = "background"
        
        return chunks
    
    def _chunk_technical_docs(self, text: str, title: str, tone: str) -> List[ImprovedChunk]:
        """Chunk technical documentation preserving code and examples."""
        chunks = []
        
        # Identify code blocks
        code_pattern = r'```[\s\S]*?```|^    .*$'
        
        # Split while preserving code blocks
        parts = re.split(f'({code_pattern})', text, flags=re.MULTILINE)
        
        current_chunk = ""
        current_start = 0
        
        for part in parts:
            if re.match(code_pattern, part):
                # It's a code block
                if len(current_chunk) + len(part) > self.chunk_size * 1.5:  # Allow larger chunks for code
                    if current_chunk:
                        chunks.append(ImprovedChunk(
                            content=current_chunk.strip(),
                            context_type="explanation",
                            chunk_index=len(chunks),
                            total_chunks=-1,
                            start_char=current_start,
                            end_char=current_start + len(current_chunk),
                            tone="technical"
                        ))
                    current_chunk = part
                    current_start += len(part)
                else:
                    current_chunk += part
            else:
                # Regular text
                if len(current_chunk) + len(part) > self.chunk_size and current_chunk:
                    chunks.append(ImprovedChunk(
                        content=current_chunk.strip(),
                        context_type="documentation",
                        chunk_index=len(chunks),
                        total_chunks=-1,
                        start_char=current_start,
                        end_char=current_start + len(current_chunk),
                        tone="technical"
                    ))
                    current_chunk = part
                    current_start += len(part)
                else:
                    current_chunk += part
        
        # Add remaining
        if current_chunk.strip():
            chunks.append(ImprovedChunk(
                content=current_chunk.strip(),
                context_type="documentation",
                chunk_index=len(chunks),
                total_chunks=-1,
                start_char=current_start,
                end_char=len(text),
                tone="technical"
            ))
        
        # Update totals
        for chunk in chunks:
            chunk.total_chunks = len(chunks)
        
        return chunks
    
    def _chunk_general_text(self, text: str, title: str, tone: str) -> List[ImprovedChunk]:
        """Intelligent chunking for general text."""
        chunks = []
        
        # Try to identify natural breaks
        # First, try double newlines (paragraphs)
        paragraphs = text.split('\n\n')
        
        current_chunk = ""
        current_start = 0
        chunk_start = 0
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) > self.chunk_size and current_chunk:
                # Save current chunk
                chunks.append(ImprovedChunk(
                    content=current_chunk.strip(),
                    context_type=self._determine_context_by_content(current_chunk),
                    chunk_index=len(chunks),
                    total_chunks=-1,
                    start_char=chunk_start,
                    end_char=current_start,
                    tone=tone
                ))
                current_chunk = paragraph + "\n\n"
                chunk_start = current_start
            else:
                current_chunk += paragraph + "\n\n"
            
            current_start += len(paragraph) + 2  # +2 for \n\n
        
        # Add remaining
        if current_chunk.strip():
            chunks.append(ImprovedChunk(
                content=current_chunk.strip(),
                context_type=self._determine_context_by_content(current_chunk),
                chunk_index=len(chunks),
                total_chunks=-1,
                start_char=chunk_start,
                end_char=len(text),
                tone=tone
            ))
        
        # Update totals
        for chunk in chunks:
            chunk.total_chunks = len(chunks)
        
        return chunks
    
    def _break_section_intelligently(
        self,
        content: str,
        section_title: str,
        section_start: int,
        context_type: str,
        tone: str,
        key_concepts: List[str]
    ) -> List[ImprovedChunk]:
        """Break large sections while preserving logical units."""
        sub_chunks = []
        
        # Look for sub-sections or logical breaks
        paragraphs = content.split('\n\n')
        current_chunk = ""
        current_start = 0
        part_num = 1
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) > self.chunk_size and current_chunk:
                sub_chunks.append(ImprovedChunk(
                    content=current_chunk.strip(),
                    context_type=context_type,
                    chunk_index=-1,
                    total_chunks=-1,
                    start_char=section_start + current_start,
                    end_char=section_start + current_start + len(current_chunk),
                    key_concepts=key_concepts if part_num == 1 else None,
                    tone=tone
                ))
                current_chunk = paragraph + "\n\n"
                current_start += len(current_chunk)
                part_num += 1
            else:
                current_chunk += paragraph + "\n\n"
        
        # Add remaining
        if current_chunk.strip():
            sub_chunks.append(ImprovedChunk(
                content=current_chunk.strip(),
                context_type=context_type,
                chunk_index=-1,
                total_chunks=-1,
                start_char=section_start + current_start,
                end_char=section_start + len(content),
                key_concepts=key_concepts if part_num == 1 else None,
                tone=tone
            ))
        
        return sub_chunks
    
    def _extract_key_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text."""
        # Simple keyword extraction
        # In practice, you might use NLP libraries for better extraction
        concepts = []
        
        # Look for emphasized terms
        emphasized = re.findall(r'\*\*(.+?)\*\*|__(.+?)__|"(.+?)"', text)
        for groups in emphasized:
            for term in groups:
                if term and len(term) > 3:
                    concepts.append(term)
        
        # Look for capitalized terms (potential proper nouns/concepts)
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        for term in capitalized[:10]:  # Limit to top 10
            if term not in concepts and len(term) > 5:
                concepts.append(term)
        
        return concepts[:15]  # Return top 15 concepts
    
    def _determine_context_by_content(self, content: str) -> str:
        """Determine context type by analyzing content."""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["introduce", "overview", "begin", "start"]):
            return "introduction"
        elif any(word in content_lower for word in ["conclude", "summary", "final", "end"]):
            return "conclusion"
        elif any(word in content_lower for word in ["example", "demonstrate", "illustrate"]):
            return "example"
        elif any(word in content_lower for word in ["argue", "propose", "suggest", "claim"]):
            return "argument"
        elif any(word in content_lower for word in ["evidence", "data", "study", "research"]):
            return "evidence"
        else:
            return "main_content"
    
    def create_improved_chunk_prompt(
        self,
        chunk: ImprovedChunk,
        document_title: str,
        content_type: ContentType
    ) -> str:
        """Create analysis prompt that preserves document spirit."""
        
        # Position context
        position_context = ""
        if chunk.is_first:
            position_context = "This is the opening section."
        elif chunk.is_last:
            position_context = "This is the final section."
        else:
            position_context = f"This is section {chunk.chunk_index + 1} of {chunk.total_chunks}."
        
        # Content type context
        type_descriptions = {
            ContentType.ACADEMIC_PAPER: "academic research",
            ContentType.BLOG_POST: "blog article",
            ContentType.NEWS_ARTICLE: "news report",
            ContentType.TECHNICAL_DOCUMENTATION: "technical documentation",
            ContentType.BOOK_CHAPTER: "book chapter",
            ContentType.GENERAL_TEXT: "document"
        }
        
        content_description = type_descriptions.get(content_type, "content")
        
        # Context-specific instructions
        context_instructions = {
            "abstract": "Focus on the main research question, methodology overview, and key findings.",
            "introduction": "Identify the problem being addressed, motivation, and approach overview.",
            "methodology": "Extract the specific methods, techniques, and procedures used.",
            "results": "Capture the specific findings, data, and outcomes presented.",
            "discussion": "Note the interpretations, implications, and connections to broader context.",
            "conclusion": "Identify the summary of findings, contributions, and future directions.",
            "lead": "Extract the who, what, when, where, why, and how.",
            "key_facts": "Focus on the main facts and immediate context.",
            "documentation": "Preserve technical details, parameters, and usage examples.",
            "main_content": "Extract the core ideas, arguments, and supporting details."
        }
        
        specific_instructions = context_instructions.get(
            chunk.context_type,
            "Extract the main ideas and important details."
        )
        
        # Tone-specific guidance
        tone_guidance = {
            "technical": "Preserve technical terminology and precise details.",
            "conversational": "Note the informal style and personal touches.",
            "narrative": "Capture the story elements and flow.",
            "neutral": "Focus on the factual content."
        }
        
        tone_instruction = tone_guidance.get(chunk.tone, "")
        
        return f"""
Analyze this section from the {content_description} titled "{document_title}".

Context: {chunk.context_type.replace('_', ' ').title()} section
{position_context}
Tone: {chunk.tone}
{f"Key concepts identified: {', '.join(chunk.key_concepts)}" if chunk.key_concepts else ""}

YOUR TASK:
{specific_instructions}
{tone_instruction}

IMPORTANT GUIDELINES:
1. DO NOT refer to this as "the paper" or "the document" - treat it as the actual content it is
2. Preserve the author's voice and style - don't academicize casual content or casualize formal content  
3. Focus on WHAT is being communicated, not the medium (avoid "the author writes", "the text states")
4. Capture insights as they are presented - as facts, opinions, stories, or arguments
5. Maintain the original perspective (first-person stays first-person, etc.)
6. Note any unique stylistic elements that give the content character
7. If this is {chunk.context_type} content, ensure you capture elements specific to that type

Content to analyze:
{chunk.content}

Create a rich analysis that someone could use to understand this section's contribution to the whole.
Write as if you're explaining the IDEAS THEMSELVES, not summarizing a document about them.
"""