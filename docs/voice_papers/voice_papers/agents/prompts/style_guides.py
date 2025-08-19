"""Style guides for Voice Papers agents.

This module centralizes all style guidelines, including formatting,
tone, structure, and presentation rules.
"""

from typing import Dict, Any, List


class StyleGuides:
    """Centralized storage for Voice Papers style guides."""
    
    # ============== VOICE PAPERS STYLE GUIDE ==============
    
    VOICE_PAPERS_STYLE = {
        "name": "Voice Papers Educational Podcast Style",
        "description": "Transform academic content into engaging educational narratives",
        
        "structure": {
            "opening": {
                "hook_types": [
                    "relatable_scenario",
                    "historical_context", 
                    "current_problem",
                    "provocative_question"
                ],
                "duration": "30 seconds",
                "requirements": [
                    "Must be specific to the paper topic",
                    "Should create immediate engagement",
                    "Natural transition to main content"
                ]
            },
            "body": {
                "organization": "logical_progression",
                "elements": [
                    "Clear explanations",
                    "Relevant examples",
                    "Smooth transitions",
                    "Layered complexity"
                ],
                "pacing": "varied_for_engagement"
            },
            "conclusion": {
                "duration": "30 seconds",
                "elements": [
                    "Key insight summary",
                    "Future implications",
                    "Thought-provoking closure"
                ]
            }
        },
        
        "tone": {
            "overall": "conversational_yet_informative",
            "characteristics": [
                "Warm and approachable",
                "Intellectually engaging",
                "Respectful of audience intelligence",
                "Enthusiastic without hyperbole"
            ],
            "avoid": [
                "Condescending explanations",
                "Excessive formality",
                "Hyperbolic language",
                "Meta-references"
            ]
        },
        
        "language": {
            "sentence_variety": True,
            "technical_terms": "explain_on_first_use",
            "pronouns": "inclusive_second_person",
            "voice": "active_preferred"
        }
    }
    
    # ============== TECHNICAL STYLE GUIDE ==============
    
    TECHNICAL_STYLE = {
        "name": "Technical Content Extraction Style",
        "description": "Extract and present objective knowledge without interpretation",
        
        "structure": {
            "organization": "hierarchical_categories",
            "sections": [
                "Facts and Data",
                "Concepts and Definitions",
                "Methods and Processes",
                "Results and Findings"
            ],
            "formatting": {
                "headers": "clear_descriptive",
                "lists": "bullet_points",
                "emphasis": "minimal"
            }
        },
        
        "presentation": {
            "facts": "direct_statement",
            "opinions": "attributed_always",
            "data": "precise_numbers",
            "processes": "step_by_step"
        },
        
        "language": {
            "tone": "neutral_objective",
            "terminology": "precise_technical",
            "transitions": "minimal_factual",
            "interpretation": "none"
        }
    }
    
    # ============== CONVERSATIONAL ENHANCEMENT STYLE ==============
    
    CONVERSATIONAL_STYLE = {
        "name": "Conversational Enhancement Style",
        "description": "Add natural speech patterns without changing content",
        
        "enhancements": {
            "connectors": [
                "Additionally", "Furthermore", "However",
                "In fact", "For instance", "Meanwhile"
            ],
            "softeners": [
                "It turns out", "Interestingly enough",
                "As it happens", "Curiously"
            ],
            "emphasis": [
                "particularly", "especially", "notably"
            ]
        },
        
        "rules": {
            "preserve_meaning": "absolute",
            "changes": "minimal",
            "tone_shift": "subtle"
        }
    }
    
    # ============== FOCUS-SPECIFIC STYLES ==============
    
    FOCUS_STYLES = {
        "explanatory": {
            "progression": "simple_to_complex",
            "examples": "abundant_and_relatable",
            "explanations": "step_by_step",
            "assumptions": "minimal_prior_knowledge"
        },
        
        "technical": {
            "precision": "high",
            "attribution": "rigorous",
            "structure": "logical_systematic",
            "objectivity": "absolute"
        },
        
        "critical": {
            "analysis": "balanced",
            "evidence": "examined",
            "perspectives": "multiple",
            "tone": "thoughtful_questioning"
        },
        
        "practical": {
            "focus": "applications",
            "examples": "real_world",
            "structure": "problem_solution",
            "actionability": "high"
        }
    }
    
    # ============== LANGUAGE-SPECIFIC STYLES ==============
    
    LANGUAGE_STYLES = {
        "Spanish": {
            "formality": "informal_tu",
            "cultural_references": "latin_american",
            "idioms": "common_natural",
            "sentence_structure": "varied_engaging"
        },
        
        "English": {
            "formality": "conversational_professional",
            "cultural_references": "international",
            "idioms": "limited_clear",
            "sentence_structure": "clear_direct"
        }
    }
    
    # ============== TONE VARIATIONS ==============
    
    TONE_STYLES = {
        "academic": {
            "formality": "moderate",
            "precision": "high",
            "examples": "scholarly",
            "vocabulary": "sophisticated_but_clear"
        },
        
        "casual": {
            "formality": "low",
            "precision": "moderate",
            "examples": "everyday",
            "vocabulary": "simple_accessible"
        },
        
        "professional": {
            "formality": "moderate_high",
            "precision": "high",
            "examples": "industry_relevant",
            "vocabulary": "business_appropriate"
        }
    }
    
    # ============== HELPER METHODS ==============
    
    @classmethod
    def get_style_guide(cls, style_name: str) -> Dict[str, Any]:
        """Get a complete style guide by name.
        
        Args:
            style_name: Name of the style guide
            
        Returns:
            Dictionary containing style guide rules
        """
        style_map = {
            "voice_papers": cls.VOICE_PAPERS_STYLE,
            "technical": cls.TECHNICAL_STYLE,
            "conversational": cls.CONVERSATIONAL_STYLE
        }
        return style_map.get(style_name, cls.VOICE_PAPERS_STYLE)
    
    @classmethod
    def get_focus_style(cls, focus: str) -> Dict[str, Any]:
        """Get style rules for a specific focus.
        
        Args:
            focus: The focus type
            
        Returns:
            Dictionary of focus-specific style rules
        """
        return cls.FOCUS_STYLES.get(focus, {})
    
    @classmethod
    def get_language_style(cls, language: str) -> Dict[str, Any]:
        """Get language-specific style rules.
        
        Args:
            language: Target language
            
        Returns:
            Dictionary of language-specific style rules
        """
        return cls.LANGUAGE_STYLES.get(language, {})
    
    @classmethod
    def get_tone_style(cls, tone: str) -> Dict[str, Any]:
        """Get tone-specific style rules.
        
        Args:
            tone: Desired tone
            
        Returns:
            Dictionary of tone-specific style rules
        """
        return cls.TONE_STYLES.get(tone, {})
    
    @classmethod
    def combine_styles(cls, base_style: str, focus: str = None, 
                      language: str = "Spanish", tone: str = "academic") -> Dict[str, Any]:
        """Combine multiple style guides into a unified guide.
        
        Args:
            base_style: The base style guide to use
            focus: Optional focus-specific modifications
            language: Language-specific modifications
            tone: Tone-specific modifications
            
        Returns:
            Combined style guide dictionary
        """
        combined = cls.get_style_guide(base_style).copy()
        
        if focus:
            combined["focus_modifications"] = cls.get_focus_style(focus)
        
        if language:
            combined["language_modifications"] = cls.get_language_style(language)
            
        if tone:
            combined["tone_modifications"] = cls.get_tone_style(tone)
            
        return combined