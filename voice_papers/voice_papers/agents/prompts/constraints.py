"""Constraints and rules for Voice Papers agents.

This module centralizes all constraints like avoided words, phrases,
and other rules that agents should follow.
"""

from typing import List, Set, Dict


class Constraints:
    """Centralized storage for agent constraints and rules."""
    
    # ============== AVOIDED WORDS ==============
    
    # Universal avoided words (apply to all agents)
    UNIVERSAL_AVOIDED_WORDS = {
        # Overused adjectives
        "fundamental", "crucial", "esencial", "primordial", "vital",
        "fascinante", "intrigante", "revelador", "asombroso",
        "groundbreaking", "revolutionary", "remarkable", "brilliant",
        "paradigm shift", "game-changing", "cutting-edge",
        
        # Academic clichés
        "delve", "explore", "unpack", "dive deep", "deep dive",
        "robust", "comprehensive", "compelling",
        "furthermore", "moreover", "nevertheless",
        
        # Conclusion phrases
        "In conclusion", "To summarize", "In summary",
        "It's important to note", "It's worth noting",
        
        # Meta-language
        "Let's explore", "Join me as we", "Together we'll discover",
        "In this episode", "Today we'll discuss",
        
        # Empty phrases
        "actually", "basically", "essentially", "simply put",
        "at the end of the day", "when all is said and done"
    }
    
    # Focus-specific avoided words
    TECHNICAL_AVOIDED_WORDS = {
        "revolutionary", "groundbreaking", "fascinating", "remarkable",
        "suggests", "implies", "demonstrates", "reveals", "shows that",
        "interestingly", "surprisingly", "notably", "importantly",
        "profound", "significant implications", "paradigm shift",
        "transforms", "revolutionizes", "disrupts"
    }
    
    EDUCATIONAL_AVOIDED_WORDS = {
        "Hoy vamos a hablar de", "En este episodio", "Este es un resumen",
        "vamos a explorar", "acompáñame mientras", "juntos descubriremos"
    }
    
    # ============== RULES AND PATTERNS ==============
    
    # Rules for technical writing
    TECHNICAL_RULES = {
        "attribution_required": [
            "opinions", "claims", "beliefs", "arguments", "positions"
        ],
        "attribution_phrases": [
            "According to", "The author claims", "X argues that",
            "In X's view", "The paper reports", "Research suggests",
            "The study found", "Según", "El autor afirma"
        ],
        "fact_markers": [
            "The system processes", "The study included",
            "The algorithm has", "Temperature increased by"
        ],
        "avoid_interpretation": [
            "This suggests", "This implies", "This demonstrates",
            "This reveals", "This shows that"
        ]
    }
    
    # Rules for educational writing
    EDUCATIONAL_RULES = {
        "required_elements": [
            "hook", "context", "main_content", "implications", "closure"
        ],
        "conversational_phrases": [
            "Si eres como yo", "Probablemente ya pensaste",
            "Te voy a contar", "Imagina por un momento",
            "¿Te ha pasado que", "¿Parece simple, no?"
        ],
        "transition_phrases": [
            "Ahora bien", "Pero espera", "Y esto nos lleva",
            "¿Recuerdas cuando", "Lo cual significa",
            "Y aquí es donde todo se conecta"
        ]
    }
    
    # ============== LANGUAGE-SPECIFIC CONSTRAINTS ==============
    
    SPANISH_CONSTRAINTS = {
        "avoid_anglicisms": {
            "machine learning": "aprendizaje automático",
            "deep learning": "aprendizaje profundo",
            "framework": "marco de trabajo",
            "benchmark": "punto de referencia"
        },
        "natural_expressions": [
            "De hecho", "Es decir", "Por ejemplo",
            "En otras palabras", "Dicho de otro modo"
        ]
    }
    
    ENGLISH_CONSTRAINTS = {
        "avoid_redundancy": {
            "very unique": "unique",
            "completely exhausted": "exhausted",
            "absolutely essential": "essential"
        }
    }
    
    # ============== FORMATTING RULES ==============
    
    FORMATTING_RULES = {
        "numbers": {
            "spell_out_under": 10,  # Spell out numbers under 10
            "use_digits_for": ["percentages", "statistics", "measurements"],
            "format_large_numbers": True  # Use commas: 1,000,000
        },
        "quotes": {
            "use_smart_quotes": True,
            "attribution_style": "said_before_quote"  # "X said, 'quote'"
        },
        "lists": {
            "min_items_for_bullet": 3,
            "parallel_structure": True
        }
    }
    
    # ============== HELPER METHODS ==============
    
    @classmethod
    def get_avoided_words(cls, focus: str = None, language: str = "Spanish") -> Set[str]:
        """Get the set of avoided words for a specific focus and language.
        
        Args:
            focus: The focus type (e.g., 'technical', 'educational')
            language: The target language
            
        Returns:
            Set of words to avoid
        """
        avoided = cls.UNIVERSAL_AVOIDED_WORDS.copy()
        
        # Add focus-specific words
        if focus == "technical":
            avoided.update(cls.TECHNICAL_AVOIDED_WORDS)
        elif focus == "educational":
            avoided.update(cls.EDUCATIONAL_AVOIDED_WORDS)
        
        return avoided
    
    @classmethod
    def get_rules(cls, rule_type: str) -> Dict:
        """Get rules for a specific type.
        
        Args:
            rule_type: Type of rules (e.g., 'technical', 'educational', 'formatting')
            
        Returns:
            Dictionary of rules
        """
        rule_map = {
            "technical": cls.TECHNICAL_RULES,
            "educational": cls.EDUCATIONAL_RULES,
            "formatting": cls.FORMATTING_RULES
        }
        return rule_map.get(rule_type, {})
    
    @classmethod
    def get_language_constraints(cls, language: str) -> Dict:
        """Get language-specific constraints.
        
        Args:
            language: Target language (e.g., 'Spanish', 'English')
            
        Returns:
            Dictionary of language constraints
        """
        constraint_map = {
            "Spanish": cls.SPANISH_CONSTRAINTS,
            "English": cls.ENGLISH_CONSTRAINTS
        }
        return constraint_map.get(language, {})
    
    @classmethod
    def should_avoid_word(cls, word: str, focus: str = None, language: str = "Spanish") -> bool:
        """Check if a word should be avoided.
        
        Args:
            word: The word to check
            focus: The focus type
            language: The target language
            
        Returns:
            True if the word should be avoided
        """
        avoided_words = cls.get_avoided_words(focus, language)
        return word.lower() in {w.lower() for w in avoided_words}