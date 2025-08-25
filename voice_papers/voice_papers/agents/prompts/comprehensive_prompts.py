"""Comprehensive prompts focused on completeness over engagement."""

from typing import Dict, List, Optional


class ComprehensivePrompts:
    """Prompts that prioritize exhaustive content coverage."""
    
    @staticmethod
    def get_exhaustive_extraction_prompt(
        language: str = "English",
        depth: str = "exhaustive",
        content_type: str = "document"
    ) -> str:
        """Get prompt for exhaustive content extraction."""
        
        depth_instructions = {
            "summary": """
            Extract the main points and key information.
            Focus on essential concepts and conclusions.
            """,
            "standard": """
            Extract all important information with reasonable detail.
            Include main concepts, supporting evidence, and conclusions.
            """,
            "comprehensive": """
            Extract ALL information with full detail.
            Include every concept, all evidence, complete methodologies.
            Preserve technical details and specific examples.
            """,
            "exhaustive": """
            COMPLETE EXTRACTION - NOTHING CAN BE MISSED:
            - Every single fact, figure, and data point
            - All concepts with full explanations
            - Complete methodologies with every step
            - All examples, case studies, and applications
            - Every piece of evidence and supporting material
            - All limitations, assumptions, and caveats
            - Full technical specifications and formulas
            - Complete code snippets and algorithms
            - All references and citations
            
            If you're unsure whether to include something, INCLUDE IT.
            Better to have too much detail than too little.
            """
        }
        
        return f"""
        Your mission is to create a {depth} extraction of this {content_type}.
        
        CRITICAL REQUIREMENTS FOR {depth.upper()} EXTRACTION:
        
        {depth_instructions.get(depth, depth_instructions["comprehensive"])}
        
        EXTRACTION PRINCIPLES:
        
        1. **COMPLETENESS OVER CONCISENESS**
           - Include everything, don't summarize
           - Expand on technical concepts
           - Provide full context
           - Keep all numerical data
        
        2. **PRESERVE TECHNICAL ACCURACY**
           - Maintain exact terminology
           - Keep all formulas and equations
           - Preserve code exactly as shown
           - Include all measurements with units
        
        3. **STRUCTURED PRESENTATION**
           - Organize following source structure
           - Use clear section headers
           - Maintain logical flow
           - Connect related concepts
        
        4. **EXPLANATORY ADDITIONS**
           - Add clarifications for complex terms
           - Provide context for acronyms
           - Explain implicit assumptions
           - Define technical terminology
        
        5. **EVIDENCE PRESERVATION**
           - Include all data tables
           - Keep all figures and charts data
           - Preserve all examples
           - Maintain all citations
        
        TARGET LANGUAGE: {language}
        
        Remember: Your goal is COMPLETE UNDERSTANDING, not entertainment.
        The reader should not need to refer to the original after reading your extraction.
        """
    
    @staticmethod
    def get_technical_preservation_prompt(focus: str = "technical") -> str:
        """Get prompt for preserving technical content."""
        
        if focus == "technical":
            return """
            TECHNICAL CONTENT PRESERVATION:
            
            You MUST preserve ALL technical content exactly:
            
            1. **FORMULAS AND EQUATIONS**
               - Keep exact mathematical notation
               - Preserve all variables and symbols
               - Include derivations if present
               - Maintain equation numbering
            
            2. **CODE AND ALGORITHMS**
               - Preserve exact syntax
               - Keep all comments
               - Include import statements
               - Maintain indentation
               - Document all parameters
            
            3. **DATA AND RESULTS**
               - All numerical values with units
               - Complete statistical results
               - Full experimental data
               - All performance metrics
            
            4. **TECHNICAL SPECIFICATIONS**
               - System requirements
               - Hardware specifications
               - Software versions
               - Configuration details
               - Protocol descriptions
            
            5. **METHODOLOGICAL DETAILS**
               - Complete procedures
               - All parameters and settings
               - Validation methods
               - Error handling
               - Edge cases
            
            NO SIMPLIFICATION - The technical audience needs ALL details.
            """
        else:
            return """
            CONTENT PRESERVATION WITH EXPLANATIONS:
            
            Preserve all content while adding explanations:
            
            1. **TECHNICAL CONCEPTS**
               - Keep the technical term
               - Add a clear explanation
               - Provide an analogy if helpful
               - Include practical examples
            
            2. **FORMULAS AND DATA**
               - Show the formula/data
               - Explain what it means
               - Describe its significance
               - Connect to main ideas
            
            3. **SPECIALIZED TERMINOLOGY**
               - Define on first use
               - Provide context
               - Use consistently
               - Connect to familiar concepts
            
            The goal is complete preservation with added accessibility.
            """
    
    @staticmethod
    def get_completeness_checklist() -> List[str]:
        """Get checklist for verifying completeness."""
        return [
            "All section headings from source included?",
            "Every data point and statistic preserved?",
            "All technical terms defined or explained?",
            "Complete methodology documented?",
            "All examples and case studies included?",
            "Every conclusion and finding captured?",
            "All limitations and caveats noted?",
            "Future work and implications included?",
            "All references and citations preserved?",
            "No content summarized or condensed?",
            "Technical specifications complete?",
            "All formulas and equations included?",
            "Code snippets preserved exactly?",
            "Visual data (charts/graphs) described?",
            "Logical flow maintained?",
            "Relationships between concepts clear?",
            "Context provided for all claims?",
            "Supporting evidence included?",
            "No important details omitted?",
            "Reader can understand without original?"
        ]
    
    @staticmethod
    def get_coverage_enhancement_prompt(
        missing_elements: List[str],
        coverage_percentage: float
    ) -> str:
        """Get prompt for enhancing coverage with missing elements."""
        
        return f"""
        COVERAGE ENHANCEMENT REQUIRED
        
        Current coverage: {coverage_percentage:.1f}%
        Target coverage: 95% minimum
        
        The following critical elements are missing and MUST be added:
        
        MISSING ELEMENTS:
        {chr(10).join(f'• {element}' for element in missing_elements)}
        
        ENHANCEMENT INSTRUCTIONS:
        
        1. **LOCATE AND EXPAND**
           - Find where each missing element belongs
           - Add it with full context
           - Explain its significance
           - Connect to existing content
        
        2. **VERIFY COMPLETENESS**
           - Check no other elements were missed
           - Ensure smooth integration
           - Maintain logical flow
           - Preserve all relationships
        
        3. **NO REMOVAL**
           - Keep all existing content
           - Only add missing information
           - Expand rather than replace
           - Build on what's there
        
        After enhancement, the extraction must be COMPLETE.
        """
    
    @staticmethod
    def get_depth_specific_instructions(depth: str) -> Dict[str, str]:
        """Get specific instructions for each depth level."""
        
        instructions = {
            "summary": {
                "goal": "Create a concise overview of main points",
                "include": "Key concepts, main findings, important conclusions",
                "exclude": "Minor details, extensive examples, full methodologies",
                "length": "10-20% of original",
                "use_case": "Quick understanding of main ideas"
            },
            "standard": {
                "goal": "Provide comprehensive coverage of important content",
                "include": "All major concepts, supporting evidence, methodologies, key examples",
                "exclude": "Redundant information, excessive technical detail",
                "length": "40-60% of original",
                "use_case": "Good understanding without reading original"
            },
            "comprehensive": {
                "goal": "Extract all meaningful content with full detail",
                "include": "Everything important, all evidence, complete methods, all examples",
                "exclude": "Only truly redundant content",
                "length": "70-90% of original",
                "use_case": "Complete understanding of the material"
            },
            "exhaustive": {
                "goal": "Preserve absolutely everything with explanatory additions",
                "include": "EVERYTHING - no exceptions, plus clarifications",
                "exclude": "NOTHING - include even minor details",
                "length": "100-120% of original (with explanations)",
                "use_case": "Complete replacement for original document"
            }
        }
        
        return instructions.get(depth, instructions["comprehensive"])
    
    @staticmethod
    def get_educational_completeness_prompt(
        language: str,
        duration: int,
        depth: str = "comprehensive"
    ) -> str:
        """Get educational script prompt focused on completeness."""
        
        return f"""
        Transform this content into a COMPLETE educational script in {language}.
        
        PRIORITY: COMPLETENESS OVER ENTERTAINMENT
        
        Your script must ensure the listener understands EVERYTHING from the source material.
        
        REQUIREMENTS FOR {depth.upper()} COVERAGE:
        
        1. **SYSTEMATIC COVERAGE**
           - Follow the source structure
           - Cover every major section
           - Include all key points
           - Don't skip technical details
        
        2. **COMPLETE EXPLANATIONS**
           - Define every technical term
           - Explain all concepts fully
           - Provide context for all claims
           - Include all supporting evidence
        
        3. **DATA AND EVIDENCE**
           - Include all important numbers
           - Preserve statistical results
           - Keep experimental findings
           - Maintain all examples
        
        4. **TECHNICAL ACCURACY**
           - Use correct terminology
           - Preserve precise meanings
           - Keep technical relationships
           - Maintain logical rigor
        
        5. **DEPTH BEFORE BREVITY**
           - Better to be thorough than brief
           - Include details that matter
           - Explain complex parts fully
           - Don't rush through difficult sections
        
        TARGET DURATION: {duration} minutes (but ONLY if content requires it)
        
        IMPORTANT: If covering everything properly requires more time, 
        prioritize completeness. It's better to deliver {duration + 5} minutes 
        of complete content than {duration} minutes with gaps.
        
        STRUCTURE:
        1. Brief introduction (30 seconds max)
        2. Systematic content coverage (bulk of time)
        3. Conclusion with key takeaways (30 seconds max)
        
        NO ENTERTAINMENT HOOKS - Start with substance immediately.
        NO DRAMATIC NARRATIVES - Focus on information transfer.
        NO UNNECESSARY ANALOGIES - Only use when truly helpful.
        
        Your success is measured by how completely you cover the material,
        not by how engaging the delivery is.
        """