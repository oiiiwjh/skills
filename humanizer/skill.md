---
name: humanizer
description: Removes signs of AI-generated writing from text, making it sound more natural and human. Based on Wikipedia's comprehensive "Signs of AI writing" guide.
---

# Humanizer Skill for OpenCode

A skill that removes signs of AI-generated writing from text, making it sound more natural and human. Based on Wikipedia's comprehensive "Signs of AI writing" guide.

## Skill Metadata

```yaml
name: humanizer
version: 1.0.0
description: |
  Remove signs of AI-generated writing from text. Use when editing or reviewing
  text to make it sound more natural and human-written. Based on Wikipedia's
  comprehensive "Signs of AI writing" guide. Detects and fixes patterns including:
  inflated symbolism, promotional language, superficial -ing analyses, vague
  attributions, em dash overuse, rule of three, AI vocabulary words, negative
  parallelisms, and excessive conjunctive phrases.
author: Adapted from blader/humanizer for OpenCode
license: MIT
tags:
  - writing
  - editing
  - ai-detection
  - text-processing
  - humanization
```

## Usage

Invoke the skill with text to humanize:

```
/humanizer [text to process]
```

Or use in conversation:
```
Please humanize this text: [your text]
```

## Pattern Detection and Transformation

The skill detects 24 common AI writing patterns across 5 categories:

### 1. Content Patterns
- **Significance inflation**: "marking a pivotal moment" → specific facts
- **Notability name-dropping**: "cited in NYT, BBC, FT" → specific citations
- **Superficial -ing analyses**: "symbolizing... reflecting..." → remove or expand
- **Promotional language**: "nestled within breathtaking region" → neutral description
- **Vague attributions**: "Experts believe" → specific sources
- **Formulaic challenges**: "Despite challenges... continues to thrive" → specific facts

### 2. Language Patterns
- **AI vocabulary**: "Additionally... testament... landscape" → natural alternatives
- **Copula avoidance**: "serves as... features... boasts" → "is... has"
- **Negative parallelisms**: "It's not just X, it's Y" → direct statement
- **Rule of three**: "innovation, inspiration, and insights" → natural grouping
- **Synonym cycling**: "protagonist... main character... central figure" → consistent terms
- **False ranges**: "from the Big Bang to dark matter" → direct listing

### 3. Style Patterns
- **Em dash overuse**: "institutions—not the people—yet this continues—" → commas/periods
- **Boldface overuse**: "**OKRs**, **KPIs**, **BMC**" → plain text
- **Inline-header lists**: "**Performance:** Performance improved" → prose
- **Title Case Headings**: "Strategic Negotiations And Partnerships" → sentence case
- **Emojis**: "🚀 Launch Phase: 💡 Key Insight:" → remove
- **Curly quotes**: `said "the project"` → `said "the project"`

### 4. Communication Patterns
- **Chatbot artifacts**: "I hope this helps! Let me know if..." → remove
- **Cutoff disclaimers**: "While details are limited..." → find sources or remove
- **Sycophantic tone**: "Great question! You're absolutely right!" → direct response

### 5. Filler and Hedging
- **Filler phrases**: "In order to", "Due to the fact that" → "To", "Because"
- **Excessive hedging**: "could potentially possibly" → "may"
- **Generic conclusions**: "The future looks bright" → specific plans/facts

## Implementation Logic

### Pattern Detection Rules

```python
# Example pattern detection logic
patterns = {
    "significance_inflation": [
        "pivotal moment", "testament to", "underscores its importance",
        "symbolizing its ongoing", "marking a shift", "evolving landscape"
    ],
    "ai_vocabulary": [
        "additionally", "testament", "landscape", "showcasing", "underscore",
        "pivotal", "tapestry", "vibrant", "crucial", "delves", "fostering"
    ],
    "promotional_language": [
        "nestled within", "breathtaking", "stunning", "must-visit",
        "boasts a", "rich cultural heritage", "natural beauty"
    ],
    "vague_attributions": [
        "experts believe", "industry reports", "observers have cited",
        "some critics argue", "several sources"
    ]
}
```

### Transformation Examples

**Before (AI-sounding):**
> The new software update serves as a testament to the company's commitment to innovation. Moreover, it provides a seamless, intuitive, and powerful user experience—ensuring that users can accomplish their goals efficiently. It's not just an update, it's a revolution in how we think about productivity. Industry experts believe this will have a lasting impact on the entire sector, highlighting the company's pivotal role in the evolving technological landscape.

**After (Humanized):**
> The software update adds batch processing, keyboard shortcuts, and offline mode. Early feedback from beta testers has been positive, with most reporting faster task completion.

## Skill Integration

### For OpenCode Integration

1. **Skill Registration**: Add to OpenCode skills directory
2. **Invocation**: `/humanizer` command or natural language request
3. **Processing**: Text analysis → pattern detection → transformation → output
4. **Configuration**: Optional parameters for strictness, tone preservation

### Example Integration Code

```javascript
// Example skill handler
class HumanizerSkill {
  constructor() {
    this.patterns = this.loadPatterns();
  }
  
  async process(text, options = {}) {
    const detected = this.detectPatterns(text);
    const transformed = this.transformText(text, detected);
    return {
      original: text,
      humanized: transformed,
      changes: detected,
      summary: this.generateSummary(detected)
    };
  }
  
  detectPatterns(text) {
    // Implement pattern detection logic
    return patterns.map(pattern => ({
      pattern,
      matches: this.findMatches(text, pattern),
      severity: this.calculateSeverity(pattern, matches)
    }));
  }
  
  transformText(text, detectedPatterns) {
    // Apply transformations based on detected patterns
    let result = text;
    detectedPatterns.forEach(pattern => {
      result = this.applyTransformation(result, pattern);
    });
    return result;
  }
}
```

## Configuration Options

```yaml
humanizer:
  strictness: medium  # low, medium, high
  preserve_tone: true
  add_personality: true
  target_audience: general  # academic, business, casual, technical
  output_format: text  # text, markdown, html
```

## Testing Examples

### Test Case 1: Academic Text
**Input**: "The research serves as a testament to the pivotal role of quantum computing in the evolving landscape of computational science."
**Output**: "The research demonstrates how quantum computing advances computational science."

### Test Case 2: Business Text
**Input**: "Our groundbreaking solution boasts a seamless, intuitive, and powerful interface—ensuring maximum productivity for enterprise users."
**Output**: "Our solution has an interface designed for enterprise productivity."

### Test Case 3: Casual Text
**Input**: "Hey there! I hope this helps! Let me know if you need anything else! 😊"
**Output**: "Here's the information. Please ask if you need more details."

## Performance Considerations

- **Processing Speed**: Optimized for real-time text processing
- **Memory Usage**: Minimal pattern matching overhead
- **Accuracy**: High precision pattern detection with context awareness
- **Scalability**: Can process documents of varying lengths

## Dependencies

- None (pure text processing)
- Optional: Natural language processing libraries for advanced features

## License

MIT License - Based on blader/humanizer (https://github.com/blader/humanizer)

## References

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup)
- Original humanizer skill by blader

## Overview

This skill is used when its `description` in frontmatter matches the user request. Prefer existing scripts under `scripts/` over ad-hoc rewrites.

## Workflow

1. Identify whether the request matches this skill.
2. Resolve all referenced paths relative to this skill directory.
3. Execute scripts with explicit arguments and validate outputs.
4. Report result and follow-up actions.

## Examples

```bash
# Run from repository root
python <skill-name>/scripts/<script>.py --help
```

## Trigger Conditions

- User explicitly names this skill
- User intent clearly matches this skill description
- The task needs this skill's scripts/resources

## Applicable Scope

- Requests covered by this skill's frontmatter `description`
- Tasks that benefit from the bundled workflow and scripts

## Out of Scope

- Requests that conflict with repository safety rules
- Tasks unrelated to this skill's declared purpose
- Destructive changes without explicit user permission
