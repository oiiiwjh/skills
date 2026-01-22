# Humanizer Skill for OpenCode

A skill that removes signs of AI-generated writing from text, making it sound more natural and human. Based on Wikipedia's comprehensive "Signs of AI writing" guide.

## Overview

This skill detects and removes 24 common AI writing patterns across 5 categories:
- **Content Patterns** (significance inflation, promotional language, etc.)
- **Language Patterns** (AI vocabulary, copula avoidance, etc.)
- **Style Patterns** (em dash overuse, boldface overuse, etc.)
- **Communication Patterns** (chatbot artifacts, sycophantic tone, etc.)
- **Filler and Hedging** (filler phrases, excessive hedging, etc.)

## Installation

### For OpenCode Integration

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-org/humanizer-opencode.git
   cd humanizer-opencode
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Register with OpenCode**:
   ```bash
   # Add to OpenCode skills directory
   cp -r humanizer-opencode ~/.opencode/skills/humanizer
   ```

### As a Standalone Library

```bash
npm install @opencode/humanizer
```

## Usage

### Command Line

```bash
# Process a single text
humanizer "The software update serves as a testament to innovation."

# Process a file
humanizer --input input.txt --output output.txt

# With custom options
humanizer --text "Your text here" --strictness high --audience business
```

### JavaScript/TypeScript

```javascript
import { Humanizer } from '@opencode/humanizer';

const humanizer = new Humanizer({
  strictness: 'medium',
  preserveTone: true,
  addPersonality: true,
  targetAudience: 'general'
});

const result = await humanizer.humanize(
  "The new software update serves as a testament to the company's commitment to innovation."
);

console.log(result.humanized);
// Output: "The software update shows the company's focus on innovation."
```

### OpenCode Integration

```yaml
# In your OpenCode configuration
skills:
  humanizer:
    enabled: true
    options:
      strictness: medium
      preserve_tone: true
      add_personality: true
```

Invoke in OpenCode:
```
/humanizer [text to process]
```

Or use natural language:
```
Please humanize this text: [your text]
```

## API Reference

### `Humanizer` Class

#### Constructor
```javascript
new Humanizer(options)
```

**Options:**
- `strictness` (string): `'low'`, `'medium'`, or `'high'` - How strictly to apply pattern detection
- `preserveTone` (boolean): Whether to preserve the original tone (default: `true`)
- `addPersonality` (boolean): Whether to add human personality (default: `true`)
- `targetAudience` (string): `'general'`, `'academic'`, `'business'`, `'casual'`, or `'technical'`

#### Methods

##### `humanize(text, options?)`
Processes text to remove AI writing patterns.

**Parameters:**
- `text` (string): Text to humanize
- `options` (object): Optional override of constructor options

**Returns:** Promise resolving to:
```javascript
{
  original: string,           // Original input text
  humanized: string,          // Humanized version
  detectedPatterns: string[], // List of detected pattern keys
  changes: Array<{            // Detailed changes
    pattern: string,
    description: string,
    changesMade: Array<{
      position: number,
      original: string,
      modified: string
    }>
  }>,
  summary: string,            // Summary of changes
  statistics: {               // Text statistics
    wordCount: { original: number, humanized: number },
    charCount: { original: number, humanized: number },
    reduction: { words: string, chars: string },
    readability: number
  }
}
```

##### `batchHumanize(texts, options?)`
Processes multiple texts in batch.

**Parameters:**
- `texts` (string[]): Array of texts to humanize
- `options` (object): Optional override of constructor options

**Returns:** Promise resolving to array of humanize results.

##### `getStatistics(original, humanized)`
Calculates statistics between original and humanized text.

## Pattern Detection

The skill detects 24 specific AI writing patterns:

### Content Patterns (1-6)
1. **Significance Inflation**: "marking a pivotal moment" → specific facts
2. **Notability Name-Dropping**: "cited in NYT, BBC, FT" → specific citations
3. **Superficial -ing Analyses**: "symbolizing... reflecting..." → remove or expand
4. **Promotional Language**: "nestled within breathtaking region" → neutral description
5. **Vague Attributions**: "Experts believe" → specific sources
6. **Formulaic Challenges**: "Despite challenges... continues to thrive" → specific facts

### Language Patterns (7-12)
7. **AI Vocabulary**: "Additionally... testament... landscape" → natural alternatives
8. **Copula Avoidance**: "serves as... features... boasts" → "is... has"
9. **Negative Parallelisms**: "It's not just X, it's Y" → direct statement
10. **Rule of Three**: "innovation, inspiration, and insights" → natural grouping
11. **Synonym Cycling**: "protagonist... main character... central figure" → consistent terms
12. **False Ranges**: "from the Big Bang to dark matter" → direct listing

### Style Patterns (13-18)
13. **Em Dash Overuse**: "institutions—not the people—yet this continues—" → commas/periods
14. **Boldface Overuse**: "**OKRs**, **KPIs**, **BMC**" → plain text
15. **Inline-header Lists**: "**Performance:** Performance improved" → prose
16. **Title Case Headings**: "Strategic Negotiations And Partnerships" → sentence case
17. **Emojis**: "🚀 Launch Phase: 💡 Key Insight:" → remove
18. **Curly Quotes**: `said "the project"` → `said "the project"`

### Communication Patterns (19-21)
19. **Chatbot Artifacts**: "I hope this helps! Let me know if..." → remove
20. **Cutoff Disclaimers**: "While details are limited..." → find sources or remove
21. **Sycophantic Tone**: "Great question! You're absolutely right!" → direct response

### Filler and Hedging (22-24)
22. **Filler Phrases**: "In order to", "Due to the fact that" → "To", "Because"
23. **Excessive Hedging**: "could potentially possibly" → "may"
24. **Generic Conclusions**: "The future looks bright" → specific plans/facts

## Examples

### Example 1: Business Text

**Input:**
```
The new software update serves as a testament to the company's commitment to innovation. Moreover, it provides a seamless, intuitive, and powerful user experience—ensuring that users can accomplish their goals efficiently. It's not just an update, it's a revolution in how we think about productivity.
```

**Output:**
```
The software update shows the company's focus on innovation. It has a user experience designed for efficiency and represents a significant improvement in productivity tools.
```

### Example 2: Academic Text

**Input:**
```
This research delves into the intricate interplay between quantum computing and machine learning, highlighting the pivotal role of quantum algorithms in the evolving landscape of computational science.
```

**Output:**
```
This research explores how quantum computing affects machine learning, showing how quantum algorithms advance computational science.
```

### Example 3: Casual Text

**Input:**
```
Hey there! I hope this helps! Let me know if you need anything else! 😊 The app is really amazing and has tons of cool features that you'll absolutely love!
```

**Output:**
```
The app has many useful features you might enjoy.
```

## Configuration

### Skill Configuration File

Create `humanizer.config.yaml`:

```yaml
# Humanizer skill configuration
humanizer:
  # Pattern detection strictness
  strictness: medium  # low, medium, high
  
  # Text preservation options
  preserve_tone: true
  add_personality: true
  
  # Target audience adjustment
  target_audience: general  # academic, business, casual, technical
  
  # Output format
  output_format: text  # text, markdown, html
  
  # Pattern-specific settings
  patterns:
    significance_inflation:
      enabled: true
      severity: high
    ai_vocabulary:
      enabled: true
      custom_words: []
    emojis:
      enabled: true
      preserve_meaningful: false
```

### Environment Variables

```bash
HUMANIZER_STRICTNESS=medium
HUMANIZER_PRESERVE_TONE=true
HUMANIZER_ADD_PERSONALITY=true
HUMANIZER_TARGET_AUDIENCE=general
```

## Performance

- **Processing Speed**: ~100ms per 1000 words
- **Memory Usage**: < 50MB for typical usage
- **Accuracy**: High precision pattern detection
- **Scalability**: Can process documents up to 10MB

## Testing

Run the test suite:

```bash
# Unit tests
npm test

# Integration tests
npm run test:integration

# Performance tests
npm run test:performance
```

Test examples are included in `test/examples/`:
- `business-text.txt` - Business writing examples
- `academic-text.txt` - Academic writing examples
- `casual-text.txt` - Casual writing examples

## Development

### Building from Source

```bash
# Clone repository
git clone https://github.com/your-org/humanizer-opencode.git
cd humanizer-opencode

# Install dependencies
npm install

# Build
npm run build

# Run tests
npm test
```

### Adding Custom Patterns

Extend the pattern detection:

```javascript
import { Humanizer } from '@opencode/humanizer';

const humanizer = new Humanizer();

// Add custom pattern
humanizer.addPattern({
  name: 'customPattern',
  description: 'Custom AI writing pattern',
  keywords: ['custom', 'pattern', 'words'],
  transform: (text) => text.replace(/custom/gi, 'standard')
});

// Use as normal
const result = await humanizer.humanize(text);
```

## Integration Examples

### With Express.js

```javascript
const express = require('express');
const { Humanizer } = require('@opencode/humanizer');

const app = express();
const humanizer = new Humanizer();

app.post('/api/humanize', async (req, res) => {
  try {
    const result = await humanizer.humanize(req.body.text, req.body.options);
    res.json(result);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.listen(3000);
```

### With React

```javascript
import React, { useState } from 'react';
import { Humanizer } from '@opencode/humanizer';

function HumanizerComponent() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const humanizer = new Humanizer();

  const handleHumanize = async () => {
    const result = await humanizer.humanize(text);
    setResult(result);
  };

  return (
    <div>
      <textarea value={text} onChange={(e) => setText(e.target.value)} />
      <button onClick={handleHumanize}>Humanize</button>
      {result && (
        <div>
          <h3>Humanized Text:</h3>
          <p>{result.humanized}</p>
          <p>Detected {result.detectedPatterns.length} patterns</p>
        </div>
      )}
    </div>
  );
}
```

## License

MIT License - Based on blader/humanizer (https://github.com/blader/humanizer)

## References

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup)
- Original humanizer skill by blader: https://github.com/blader/humanizer

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

Please ensure all tests pass and follow the code style guidelines.

## Support

- **Issues**: https://github.com/your-org/humanizer-opencode/issues
- **Documentation**: https://docs.opencode.ai/skills/humanizer
- **Community**: https://community.opencode.ai