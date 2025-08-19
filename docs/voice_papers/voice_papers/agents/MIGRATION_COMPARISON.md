# Migration Comparison: Educational Writer

This document shows the before/after comparison of migrating to the centralized prompt system.

## Key Changes

### 1. Agent Creation

**BEFORE (improved_educational_writer.py):**
```python
def get_improved_educational_writer(llm) -> Agent:
    return Agent(
        role="Master Educational Science Communicator & Storyteller",
        goal="Transform technical content into captivating podcast narratives...",
        backstory="""You are a legendary science educator and storyteller who has mastered the art of 
        transforming academic papers into fascinating audio narratives. You've studied the best 
        science communicators and developed your own unique style that combines:
        
        - Engaging hooks and relatable scenarios tailored to each topic
        - Three-act narrative structure (Problem → Solution → Implications)
        - Natural conversational flow with strategic questions
        [... 20+ more lines of hardcoded backstory ...]
        """,
        llm=llm,
        verbose=True,
        max_iter=3,
    )
```

**AFTER (improved_educational_writer_migrated.py):**
```python
def get_improved_educational_writer(llm) -> Agent:
    composer = PromptComposer()
    
    backstory = composer.compose_agent_prompt(
        agent_type="educational_writer",
        focus="explanatory",
        language="Spanish",
        tone="academic",
        additional_context="""[Only unique aspects specific to this agent]"""
    )
    
    return Agent(
        role="Master Educational Science Communicator & Storyteller",
        goal="Transform technical content into captivating podcast narratives...",
        backstory=backstory,  # ← Composed from centralized system
        llm=llm,
        verbose=True,
        max_iter=3,
    )
```

### 2. Avoided Words Management

**BEFORE:**
```python
def get_natural_language_guidelines() -> Dict[str, List[str]]:
    return {
        "avoid_words": [
            "fundamental",
            "crucial",
            "esencial",
            "primordial",
            "vital",
            "fascinante",
            # ... 60+ hardcoded words ...
        ],
        "avoid_at_start": [
            "En resumen",
            "Hoy vamos a hablar de",
            # ... more hardcoded phrases ...
        ],
    }
```

**AFTER:**
```python
def get_natural_language_guidelines() -> Dict[str, List[str]]:
    composer = PromptComposer()
    
    # Pull from centralized constraints
    avoided_words = composer.get_avoided_words_list(
        focus="educational", 
        language="Spanish"
    )
    
    return {
        "avoid_words": avoided_words,  # ← From centralized system
        "avoid_at_start": [...]  # Only unique ones kept here
    }
```

### 3. Task Creation

**BEFORE:**
```python
def create_enhanced_educational_task(...) -> str:
    guidelines = get_natural_language_guidelines()
    
    return f"""
Transform all the insights from the conversation into an educational podcast script in {language}.

### 1. INICIO - PRINCIPIOS PARA CREAR GANCHOS:

**IMPORTANTE: Crea un gancho ESPECÍFICO al tema del paper...**

[... 130+ lines of hardcoded task instructions ...]

PALABRAS PROHIBIDAS - NUNCA USES:
{chr(10).join("- " + word for word in guidelines["avoid_words"])}

[... more hardcoded instructions ...]
"""
```

**AFTER:**
```python
def create_enhanced_educational_task(...) -> str:
    # Map parameters for backwards compatibility
    focus = focus_map.get(technical_level, "explanatory")
    
    # Use centralized task prompt
    return TaskPrompts.educational_writing_task(
        title="Educational Podcast Script",
        content="[Content will be provided]",
        language=language,
        duration=duration,
        focus=focus,
        tone=tone
    )
    # All instructions now come from centralized system!
```

## Benefits Achieved

### 1. **Code Reduction**
- Original: 221 lines
- Migrated: ~100 lines
- **55% reduction** in code

### 2. **Single Source of Truth**
- Avoided words: Now in `constraints.py`
- Style guidelines: Now in `style_guides.py`
- Hook templates: Now in `templates.py`
- Agent backstories: Now in `system_prompts.py`

### 3. **Easier Updates**
- Change avoided words in ONE place → affects ALL agents
- Update style guidelines → automatically applied everywhere
- Add new hook types → available to all writers

### 4. **Better Organization**
```
Before: Everything mixed in one file
After:  
├── system_prompts.py    (What the agent IS)
├── task_prompts.py      (What the agent DOES)
├── style_guides.py      (HOW to do it)
├── constraints.py       (What NOT to do)
└── templates.py         (Reusable patterns)
```

### 5. **Flexibility Preserved**
- Can still add agent-specific context
- Can override when needed
- Backwards compatible API

## Migration Steps for Other Agents

1. **Identify what's unique** about the agent vs. what's common
2. **Move common parts** to centralized modules
3. **Keep unique parts** as additional_context
4. **Update imports** to use PromptComposer
5. **Test** to ensure same behavior

## Next Steps

To complete the migration:

1. Update the original `improved_educational_writer.py` to use the migrated version
2. Apply same pattern to other agents:
   - `technical_writer.py`
   - `conversational_enhancer.py`
   - `focus_agents.py`
   - etc.
3. Update `crew_manager.py` to use centralized prompts
4. Remove duplicate definitions