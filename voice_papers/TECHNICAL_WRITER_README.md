# Technical Writer Focus Mode

A specialized focus mode that presents content with **zero interpretation**, removing all subjective language and presenting only facts, data, and concepts as stated.

## Purpose

The technical writer is designed for situations where you need:
- Pure factual presentation without commentary
- Technical documentation style output
- No implications or suggestions beyond what's explicitly stated
- Removal of all interpretive adjectives and subjective language
- Clear, direct presentation of methods, results, and specifications

## How It Works

### 1. **Strips Interpretive Language**
Automatically removes words like:
- Revolutionary → "new"
- Groundbreaking → "recent" 
- Brilliant/Remarkable → removed
- Paradigm shift → "change"
- Suggests/Implies → removed
- Demonstrates → "shows"

### 2. **Presents Only Facts**
- States findings directly: "The model achieves 95.3% accuracy"
- Lists methods without commentary: "Uses gradient descent optimization"
- Defines concepts without interpretation: "X is defined as Y"

### 3. **Zero Added Context**
- No implications beyond what's stated
- No "this means that..." interpretations
- No subjective evaluations
- No emotional language

## Usage

```bash
# Use technical focus for zero-interpretation output
python -m voice_papers.cli paper.pdf --focus technical

# Works with all synthesis methods
python -m voice_papers.cli paper.pdf --focus technical --synthesis-method concatenation

# For direct technical presentation
python -m voice_papers.cli paper.pdf --focus technical --summary
```

## Example Output

### Input (with interpretation):
```
This groundbreaking research demonstrates a paradigm shift in neural 
network design. The results suggest profound implications for AI development.
The model achieves remarkable 95.3% accuracy.
```

### Output (technical, no interpretation):
```
## Deep Learning Architecture

This research presents a new approach in neural network design.

## Key Findings
- The model achieves 95.3% accuracy on benchmark datasets.
- Training time is reduced by 47% compared to baseline methods.
```

## When to Use

Use the technical focus mode when you need:

1. **Technical Documentation** - Creating reference materials
2. **Objective Summaries** - No editorial content
3. **Specification Extraction** - Just the facts
4. **Method Documentation** - Clear procedural information
5. **Data Presentation** - Results without interpretation

## Comparison with Other Modes

| Focus Mode | Interpretation | Style | Best For |
|------------|---------------|-------|----------|
| Explanatory | Moderate | Educational | Teaching concepts |
| Technical | **ZERO** | Manual-like | Documentation |
| Innovation | High | Excited | Highlighting breakthroughs |
| Story | Very High | Narrative | Engagement |

## Technical Agents

The technical focus uses three specialized agents:

1. **Technical Analyst** - Extracts specifications and data
2. **Concept Definer** - Defines terms precisely as stated
3. **Method Documentor** - Documents procedures exactly

## Configuration

The technical writer is configured to:
- Remove ALL subjective language
- Use simple, clear technical language
- Present information hierarchically
- Focus on accuracy over engagement
- Maintain source fidelity

## Tips

- Best for technical papers, specifications, and research methods
- Not recommended for educational content (too dry)
- Excellent for creating reference documentation
- Ideal when you need "just the facts"
- Perfect for avoiding AI interpretation bias